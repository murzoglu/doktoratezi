#!/usr/bin/env python3
"""Genel stdio MCP köprü tool-caller — bağımlılıksız, stdlib-only.

Bu repodaki stdio MCP köprülerinin (minerva_evidence_bridge, galileo_bridge,
zotero_refs_bridge) araçlarını komut satırından / interaktif-olmayan ajan
oturumundan çağırmak için tek giriş noktasıdır. Köprüler Ona'nın yerleşik
araç setine enjekte edilmediğinde (`.mcp.json` Claude Code formatındadır) bu
sarmalayıcı, `exec` üzerinden aynı JSON-RPC tools/call sözleşmesini konuşur.

Yaptığı iş:
  1. `.env`'i yükler (os.environ'da olmayan anahtarlar için; interaktif-olmayan
     çağrılarda .bashrc auto-load devreye girmez), değer ASLA yazdırılmaz.
  2. Hedef köprüye `initialize` → `tools/call` gönderir (stdio, satır-JSON-RPC).
  3. Aracın sonucunu döndürür: content[].text varsa onu, yoksa ham result JSON.

KVKK: dış gateway'e yalnız çağıran tarafından verilen argümanlar gider; bu
sarmalayıcı ham katılımcı/aile verisi enjekte etmez — çağıran içerikten sorumlu.

Köprü kısayolları (script yolu yerine ad kullanılabilir):
  minerva  → scripts/mcp/minerva_evidence_bridge.py
  galileo  → scripts/eval/galileo_bridge.py
  zotero   → scripts/mcp/zotero_refs_bridge.py

Kullanım:
  python3 scripts/mcp/mcp_tool_call.py <köprü> <araç> '<json_args>'
  python3 scripts/mcp/mcp_tool_call.py <köprü> --list
  echo '<json_args>' | python3 scripts/mcp/mcp_tool_call.py <köprü> <araç> -

Örnekler:
  python3 scripts/mcp/mcp_tool_call.py galileo galileo_judge \
      '{"text":"...","section_type":"results"}'
  python3 scripts/mcp/mcp_tool_call.py minerva minerva_literature_search \
      '{"query":"parental rejection type 1 diabetes","mode":"hybrid","k":5}'
  python3 scripts/mcp/mcp_tool_call.py zotero --list
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTO = "2025-06-18"

BRIDGES = {
    "minerva": ROOT / "scripts" / "mcp" / "minerva_evidence_bridge.py",
    "galileo": ROOT / "scripts" / "eval" / "galileo_bridge.py",
    "zotero": ROOT / "scripts" / "mcp" / "zotero_refs_bridge.py",
}


def _load_dotenv() -> None:
    """os.environ'da anahtar yoksa .env'i yükle (değer basılmaz)."""
    envf = ROOT / ".env"
    if not envf.exists():
        return
    for line in envf.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def _resolve_bridge(name: str) -> Path:
    """Kısayol adını veya doğrudan script yolunu köprü Path'ine çevir."""
    if name in BRIDGES:
        return BRIDGES[name]
    p = Path(name)
    if not p.is_absolute():
        p = ROOT / p
    return p


def _rpc(bridge: Path, calls: list[dict], timeout: int = 180) -> list[dict]:
    """Köprüye initialize + verilen çağrıları gönder; id sırasına göre yanıtlar."""
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(ROOT)
    reqs = [
        {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": PROTO, "capabilities": {},
                "clientInfo": {"name": "ona-tool-call", "version": "1.0"},
            },
        }
    ] + calls
    stdin = "\n".join(json.dumps(r) for r in reqs) + "\n"
    proc = subprocess.run(
        ["python3", str(bridge)],
        input=stdin, capture_output=True, text=True,
        cwd=str(ROOT), env=env, timeout=timeout,
    )
    out: list[dict] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not out:
        tail = "\n".join(proc.stderr.splitlines()[-8:])
        raise SystemExit(f"NO_RESPONSE from {bridge.name}. stderr tail:\n{tail}")
    return out


def _by_id(msgs: list[dict], id_: int) -> dict | None:
    for m in msgs:
        if m.get("id") == id_:
            return m
    return None


def _emit_result(msg: dict) -> int:
    """tools/call yanıtını yazdır; content[].text varsa metni, yoksa ham JSON."""
    if "error" in msg:
        print(json.dumps(msg["error"], ensure_ascii=False, indent=2))
        return 1
    result = msg.get("result", {})
    content = result.get("content")
    if isinstance(content, list):
        for c in content:
            if c.get("type") == "text":
                print(c.get("text", ""))
        return 0
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    bridge = _resolve_bridge(argv[1])
    if not bridge.exists():
        raise SystemExit(f"Köprü bulunamadı: {bridge}")

    _load_dotenv()

    # --list: araçları listele
    if len(argv) >= 3 and argv[2] in ("--list", "-l"):
        msgs = _rpc(bridge, [{"jsonrpc": "2.0", "id": 2,
                              "method": "tools/list", "params": {}}])
        r = _by_id(msgs, 2) or {}
        tools = r.get("result", {}).get("tools", [])
        for t in tools:
            print(f"{t.get('name')}\t{t.get('description', '')[:100]}")
        return 0

    if len(argv) < 4:
        raise SystemExit("Kullanım: mcp_tool_call.py <köprü> <araç> '<json_args>'")
    tool = argv[2]
    raw = argv[3]
    if raw == "-":
        raw = sys.stdin.read()
    try:
        args = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Geçersiz JSON argüman: {exc}")

    msgs = _rpc(bridge, [{"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                          "params": {"name": tool, "arguments": args}}])
    r = _by_id(msgs, 2)
    if r is None:
        raise SystemExit("tools/call yanıtı alınamadı.")
    return _emit_result(r)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
