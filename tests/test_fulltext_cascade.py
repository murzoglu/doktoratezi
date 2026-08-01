"""fulltext_cascade.py Minerva entegrasyonu kontrat testleri — doktoratezi.

Minerva'yı OpenAthens/annas-reader ile tam paritede tam-metin kaskadına bağlar:
stdio MCP köprüsü (minerva_evidence_bridge) spawn edilir, initialize + tools/call
yapılır. Testler ağsız ve deterministik: MINERVA_BRIDGE env'iyle sahte stdio-MCP
köprüsüne yönlendirilir (gerçek Gravitee gateway'e çıkılmaz).

Run: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_fulltext_cascade.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CASCADE = REPO / "scripts" / "mcp" / "fulltext_cascade.py"

# Sahte stdio-MCP köprüsü: initialize + tools/call'a tek-satır JSON-RPC yanıtı
# verir. `MODE` ortam değişkeniyle OK / ERR davranışı seçilir.
_FAKE_BRIDGE = r'''
import sys, json, os
MODE = os.environ.get("FAKE_MODE", "ok")
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    m = json.loads(line)
    mid = m.get("id")
    meth = m.get("method")
    if meth == "initialize":
        sys.stdout.write(json.dumps({"jsonrpc":"2.0","id":mid,"result":{
            "protocolVersion":"2025-06-18","capabilities":{"tools":{}},
            "serverInfo":{"name":"fake-minerva","version":"0"}}}) + "\n")
        sys.stdout.flush()
    elif meth == "tools/call":
        if MODE == "err":
            payload = {"content":[{"type":"text","text":"HATA: GRAVITEE_VECTORSTORE_GATEWAY env tanimli degil."}],"isError":True}
        elif MODE == "echo":
            args = (m.get("params") or {}).get("arguments") or {}
            text = json.dumps({"received_arg_keys": sorted(args.keys())})
            payload = {"content":[{"type":"text","text":text + " " + "F"*400}],"isError":False}
        else:
            text = json.dumps({"doi":"10.1000/x","title":"Fake","content":"F"*600})
            payload = {"content":[{"type":"text","text":text}],"isError":False}
        sys.stdout.write(json.dumps({"jsonrpc":"2.0","id":mid,"result":payload}) + "\n")
        sys.stdout.flush()
    # notifications/initialized: yanit yok
'''


def _write_fake():
    fd, path = tempfile.mkstemp(suffix="_fakebridge.py")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(_FAKE_BRIDGE)
    return path


def _run_cascade(env_extra, doi="10.1000/x", title="Fake"):
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", **env_extra}
    p = subprocess.run(
        [sys.executable, str(CASCADE), "--tier", "minerva", "--doi", doi,
         "--title", title],
        capture_output=True, text=True, env=env, timeout=60)
    return p


class MinervaCascadeTests(unittest.TestCase):
    def test_help_default_includes_minerva(self):
        p = subprocess.run([sys.executable, str(CASCADE), "--help"],
                           capture_output=True, text=True, timeout=30)
        self.assertIn("minerva", p.stdout.lower())

    def test_minerva_tier_ok(self):
        fake = _write_fake()
        self.addCleanup(os.unlink, fake)
        p = _run_cascade({"MINERVA_BRIDGE": fake, "FAKE_MODE": "ok"})
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)
        out = json.loads(p.stdout)
        tier = next(t for t in out["tiers"] if t["tier"] == "minerva")
        self.assertTrue(tier["ok"], tier)
        self.assertGreater(tier.get("fulltext_len", 0), 200)

    def test_minerva_error_graceful(self):
        fake = _write_fake()
        self.addCleanup(os.unlink, fake)
        p = _run_cascade({"MINERVA_BRIDGE": fake, "FAKE_MODE": "err"})
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)  # asla çökmez
        out = json.loads(p.stdout)
        tier = next(t for t in out["tiers"] if t["tier"] == "minerva")
        self.assertFalse(tier["ok"], tier)

    def test_minerva_bridge_missing_graceful(self):
        p = _run_cascade({"MINERVA_BRIDGE": "/nonexistent/bridge.py"})
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)
        out = json.loads(p.stdout)
        tier = next(t for t in out["tiers"] if t["tier"] == "minerva")
        self.assertFalse(tier["ok"], tier)

    def test_no_gravitee_value_leak(self):
        # KVKK/güvenlik: hiçbir GRAVITEE anahtar değeri stdout'a sızmamalı.
        fake = _write_fake()
        self.addCleanup(os.unlink, fake)
        sentinel = "SENTINEL_SECRET_DO_NOT_LEAK_XYZ"
        p = _run_cascade({"MINERVA_BRIDGE": fake, "FAKE_MODE": "ok",
                          "GRAVITEE_VECTORSTORE_API_KEY": sentinel})
        self.assertNotIn(sentinel, p.stdout)

    def test_only_doi_title_args_sent(self):
        # KVKK: gateway'e yalnız {doi|title} gider (katılımcı/ham veri değil).
        fake = _write_fake()
        self.addCleanup(os.unlink, fake)
        p = _run_cascade({"MINERVA_BRIDGE": fake, "FAKE_MODE": "echo"})
        out = json.loads(p.stdout)
        tier = next(t for t in out["tiers"] if t["tier"] == "minerva")
        keys = set(json.loads(tier["sample"].split(" F")[0])["received_arg_keys"])
        self.assertTrue(keys <= {"doi", "title"}, keys)

    def test_credential_preflight_short_circuits(self):
        # GRAVITEE kimlik yoksa alt-süreç spawn edilmeden ok:False (openathens/
        # annas token-yokluğu ile simetri). Gerçek köprü yoluyla ama env+.env'siz.
        import shutil
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(d, ignore_errors=True))
        real_bridge = str(REPO / "scripts" / "mcp" / "minerva_evidence_bridge.py")
        env = {k: v for k, v in os.environ.items() if not k.startswith("GRAVITEE_")}
        env.update({"PYTHONDONTWRITEBYTECODE": "1", "CLAUDE_PROJECT_DIR": d,
                    "MINERVA_BRIDGE": real_bridge})
        p = subprocess.run(
            [sys.executable, str(CASCADE), "--tier", "minerva", "--doi", "10.1/x"],
            capture_output=True, text=True, env=env, timeout=60)
        out = json.loads(p.stdout)
        tier = next(t for t in out["tiers"] if t["tier"] == "minerva")
        self.assertFalse(tier["ok"], tier)
        self.assertIn("gravitee", tier.get("note", "").lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
