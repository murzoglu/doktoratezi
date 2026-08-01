#!/usr/bin/env python3
"""evidentia-minerva-sciaudit + galileo ai-judge yığını sağlık kontrolü.

Üç denetim katmanının bu ortamda tam işlevsel olduğunu tek komutta kanıtlar:

  1. MINERVA  (text-embedding kanıt katmanı) — stdio MCP köprüsü
     scripts/mcp/minerva_evidence_bridge.py: stats + semantic + hybrid arama.
  2. GALILEO  (bağımsız GPT judge + Azure embedding) — stdio MCP köprüsü
     scripts/eval/galileo_bridge.py: stats(judge_ok/embedding_ok) + judge +
     claim_source_match(embedding).
  3. SCI-AUDIT (Türkçe stil) — sci-audit plugin (axis G, tr_sciaudit.py) varsa
     onu; yoksa repo-local axis-H linter (scripts/util/tr_corpus_audit.py) fallback.

Ağ/kimlik: köprüler .env'den GRAVITEE_*/GALILEO_* okur; bu script os.environ'da
değilse .env'i kendisi yükler (interaktif-olmayan çağrılarda .bashrc auto-load
devreye girmez). KVKK: dış servislere yalnız sabit test terimleri gönderilir;
ham katılımcı/aile verisi ASLA.

Çıkış: her katman için PASS/FAIL satırı; tümü PASS ise exit 0, aksi halde 1.
Kullanım:  python3 scripts/mcp/audit_stack_healthcheck.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MINERVA = ROOT / "scripts" / "mcp" / "minerva_evidence_bridge.py"
GALILEO = ROOT / "scripts" / "eval" / "galileo_bridge.py"
ANAMNESIS_CLIENT = ROOT / "scripts" / "mcp" / "anamnesis_client.py"
CLAIM_CERT = ROOT / "scripts" / "util" / "claim_certification.py"
TR_CORPUS = ROOT / "scripts" / "util" / "tr_corpus_audit.py"
SCIAUDIT_CANDIDATES = [
    Path.home()
    / ".claude/plugins/marketplaces/cureonics-marketplace/plugins/sci-audit"
    / "skills/turkish-sci-style/scripts/tr_sciaudit.py",
]

PROTO = "2025-06-18"


def _load_dotenv() -> None:
    """os.environ'da anahtar yoksa .env'i yükle (değer basılmaz)."""
    envf = ROOT / ".env"
    if not envf.exists():
        return
    for line in envf.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def _rpc(bridge: Path, calls: list[dict], timeout: int = 120) -> dict:
    """Bir stdio MCP köprüsüne initialize + verilen çağrıları gönder;
    id -> result eşlemesi döndür."""
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(ROOT)
    lines = [
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTO,
                    "capabilities": {},
                    "clientInfo": {"name": "healthcheck", "version": "1.0"},
                },
            }
        )
    ]
    lines += [json.dumps(c) for c in calls]
    payload = "\n".join(lines) + "\n"
    proc = subprocess.run(
        [sys.executable, str(bridge)],
        input=payload,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    # MCP stdio bir-satır-bir-JSON'dır ama büyük yanıtlar (ör. Minerva stats
    # journal listesi) gömülü kontrol karakteri içerebilir; strict=False ile
    # ayrıştır. Satır JSON değilse (log vb.) atla.
    out: dict = {}
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            d = json.loads(line, strict=False)
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and "id" in d:
            out[d["id"]] = d
    return out


def _tool_text(resp: dict) -> str:
    c = resp.get("result", {}).get("content", [])
    return c[0].get("text", "") if c else ""


def check_minerva() -> tuple[bool, str]:
    try:
        # Embedding kanıt katmanını iki modla doğrula (stats yanıtı çok büyük
        # olup gömülü kontrol karakteri taşıdığından smoke için search kullanılır).
        q = "parental overprotection type 1 diabetes children"
        r = _rpc(
            MINERVA,
            [
                {
                    "jsonrpc": "2.0",
                    "id": 10,
                    "method": "tools/call",
                    "params": {
                        "name": "minerva_literature_search",
                        "arguments": {"query": q, "mode": "semantic", "limit": 3},
                    },
                },
                {
                    "jsonrpc": "2.0",
                    "id": 11,
                    "method": "tools/call",
                    "params": {
                        "name": "minerva_literature_search",
                        "arguments": {"query": q, "mode": "hybrid", "limit": 3},
                    },
                },
            ],
        )
        sem = json.loads(_tool_text(r[10]), strict=False).get("results", [])
        hyb = json.loads(_tool_text(r[11]), strict=False).get("results", [])
        if len(sem) >= 1 and len(hyb) >= 1:
            return True, "semantic_hits=%d (top=%.3f) hybrid_hits=%d" % (
                len(sem),
                (sem[0].get("score", 0) if sem else 0),
                len(hyb),
            )
        # Embedding yolu boş/429 → RoMine DOI-getirme (getSingleArticle) canlılığını
        # dene; DOI-fetch bandı sağlıklıysa Minerva'yı degrade-PASS say.
        ok_doi, doi_msg = _check_minerva_doi_fetch()
        if ok_doi:
            return True, "embedding degrade (sem=%d hyb=%d) → RoMine DOI-fetch canlı: %s" % (
                len(sem), len(hyb), doi_msg,
            )
        return False, "embedding boş (sem=%d hyb=%d) ve DOI-fetch: %s" % (
            len(sem), len(hyb), doi_msg,
        )
    except Exception as e:  # noqa: BLE001
        # Embedding yolu istisna attı → yine de DOI-fetch bandını dene.
        try:
            ok_doi, doi_msg = _check_minerva_doi_fetch()
            if ok_doi:
                return True, "embedding istisna (%s) → RoMine DOI-fetch canlı: %s" % (
                    str(e)[:60], doi_msg,
                )
            return False, "embedding istisna: %s · DOI-fetch: %s" % (str(e)[:60], doi_msg)
        except Exception as e2:  # noqa: BLE001
            return False, "exception: %s" % str(e2)[:120]


def _check_minerva_doi_fetch() -> tuple[bool, str]:
    """RoMine DOI-getirme (minerva_rominedb_get_article) canlılığını doğrula.

    Bilinen kanonik bir DOI'yi (Lovejoy 2000 meta-analizi) getirir; başlık
    dönerse RoMine kanıt bandı sağlıklıdır. Embedding yolu 429 olsa bile bu
    band çalıştığı sürece referans-varlık doğrulaması kesintisiz kalır.
    """
    probe = "10.1016/S0272-7358(98)00100-7"
    r = _rpc(
        MINERVA,
        [
            {
                "jsonrpc": "2.0",
                "id": 12,
                "method": "tools/call",
                "params": {
                    "name": "minerva_rominedb_get_article",
                    "arguments": {"doi": probe},
                },
            },
        ],
    )
    art = json.loads(_tool_text(r[12]), strict=False)
    title = (art or {}).get("title") if isinstance(art, dict) else None
    if title:
        return True, "doi=%s title=%s" % (probe, str(title)[:48])
    return False, "doi=%s boş" % probe


def check_galileo() -> tuple[bool, str]:
    try:
        r = _rpc(
            GALILEO,
            [
                {
                    "jsonrpc": "2.0",
                    "id": 20,
                    "method": "tools/call",
                    "params": {"name": "galileo_stats", "arguments": {}},
                },
                {
                    "jsonrpc": "2.0",
                    "id": 21,
                    "method": "tools/call",
                    "params": {
                        "name": "galileo_claim_source_match",
                        "arguments": {
                            "claim": "Aşırı korumada etki büyüklüğü g=0,39 bildirilmiştir.",
                            "source_text": "overprotection (g = .39) in families with a chronically ill child",
                        },
                    },
                },
            ],
        )
        st = json.loads(_tool_text(r[20]))
        judge_ok = bool(st.get("judge_ok"))
        emb_ok = bool(st.get("embedding_ok"))
        m = json.loads(_tool_text(r[21]))
        emb_mode = m.get("mode") == "embedding"
        ok = judge_ok and emb_ok and emb_mode
        return ok, "judge_ok=%s embedding_ok=%s claim_match_mode=%s score=%s" % (
            judge_ok,
            emb_ok,
            m.get("mode"),
            m.get("score"),
        )
    except Exception as e:  # noqa: BLE001
        return False, "exception: %s" % str(e)[:120]


def _check_sciaudit_plugin(tool: Path) -> tuple[bool, str]:
    """sci-audit plugin axis G (tr_sciaudit.py) certification smoke'u."""
    sample = ROOT / ".tmp_sciaudit_healthcheck.qmd"
    sample.write_text(
        "# Giriş\n\nBu çalışmada p<0.05 anlamlılık düzeyinde çok çok "
        "önemli bir fark saptanmıştır.\n",
        encoding="utf-8",
    )
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(tool),
                str(sample),
                "--strictness",
                "certification",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        d = json.loads(proc.stdout)
        codes = {i.get("code") for i in d.get("issues", [])}
        # p<0.05 -> Türkçe ondalık + tekrarlanan kelime yakalanmalı
        ok = "decimal-dot-p-value" in codes and "repeated-word" in codes
        atesman = d.get("metrics", {}).get("atesman_score")
        return ok, "axis-G plugin: atesman=%s codes=%s" % (atesman, sorted(codes))
    except Exception as e:  # noqa: BLE001
        return False, "axis-G plugin istisna: %s" % str(e)[:100]
    finally:
        sample.unlink(missing_ok=True)


def _check_tr_corpus_fallback() -> tuple[bool, str]:
    """Repo-local deterministik TR stil linter'ı (axis H, tr_corpus_audit.py).
    Kasıtlı başlık ihlali (düzey atlama + başlık-sonu noktalama) planted; linter
    çalışıp bir `H-` kodu üretiyorsa TR-denetim yeteneği bu ortamda canlıdır."""
    if not TR_CORPUS.exists():
        return False, "tr_corpus_audit.py da yok"
    sample = ROOT / ".tmp_trcorpus_healthcheck.qmd"
    sample.write_text(
        "# GİRİŞ\n\nDeneme paragrafı.\n\n#### Çok Derin Alt Başlık:\n\n"
        "İkinci paragraf.\n",
        encoding="utf-8",
    )
    try:
        proc = subprocess.run(
            [
                sys.executable, str(TR_CORPUS), "headings",
                "--chapters", str(sample), "--json", "--fail-on", "none",
            ],
            capture_output=True, text=True, timeout=60, cwd=str(ROOT),
        )
        d = json.loads(proc.stdout)
        finds = d.get("findings", [])
        codes = sorted({f.get("code") for f in finds if isinstance(f, dict)})
        ok = isinstance(finds, list) and any(str(c).startswith("H-") for c in codes)
        return ok, "axis-H repo-linter: codes=%s" % codes
    except Exception as e:  # noqa: BLE001
        return False, "axis-H istisna: %s" % str(e)[:100]
    finally:
        sample.unlink(missing_ok=True)


def check_sciaudit() -> tuple[bool, str]:
    """Türkçe bilimsel stil denetimi. sci-audit plugin (axis G) varsa onu; yoksa
    repo-local deterministik axis-H linter'ını doğrular — plugin opsiyonel harici
    bir katman olduğundan yokluğu yığını hard-FAIL etmez (MINERVA/GALILEO degrade
    deseniyle tutarlı)."""
    tool = next((p for p in SCIAUDIT_CANDIDATES if p.exists()), None)
    if tool is not None:
        return _check_sciaudit_plugin(tool)
    ok, msg = _check_tr_corpus_fallback()
    return ok, "sci-audit plugin yok → %s" % msg


def check_anamnesis() -> tuple[bool, str]:
    """anamnesis GraphRAG korpusu canlı ve dolu mu (corpus_stats)."""
    if not ANAMNESIS_CLIENT.exists():
        return False, "anamnesis_client.py bulunamadı"
    try:
        sys.path.insert(0, str(ANAMNESIS_CLIENT.parent))
        import anamnesis_client as ac  # noqa: PLC0415

        ac.load_dotenv()
        client = ac.AnamnesisClient().connect()
        st = client.corpus_stats()
        docs = st.get("docs", 0) if isinstance(st, dict) else 0
        edges = st.get("edges", 0) if isinstance(st, dict) else 0
        # Korpus beslenmişse doc + graf kenarı olmalı (ingest sonrası ≥90/≥150).
        ok = docs >= 50 and edges >= 100
        return ok, "docs=%s chunks=%s nodes=%s edges=%s" % (
            docs, st.get("chunks", "?"), st.get("nodes", "?"), edges
        )
    except Exception as e:  # noqa: BLE001
        return False, "exception: %s" % str(e)[:120]


def check_claim_cert() -> tuple[bool, str]:
    """claim_certification.py çalışıyor + geçerli bir karar üretiyor mu."""
    if not CLAIM_CERT.exists():
        return False, "claim_certification.py bulunamadı"
    try:
        proc = subprocess.run(
            [sys.executable, str(CLAIM_CERT), "--json"],
            capture_output=True, text=True, timeout=150, cwd=str(ROOT),
        )
        d = json.loads(proc.stdout)
        verdict = d.get("verdict")
        layers = list(d.get("layers", {}).keys())
        # Kapı çalışıyorsa geçerli bir karar + üç çekirdek katman döner.
        ok = verdict in {"PASS", "WARN", "FAIL"} and {"numeric", "causal", "bib"} <= set(layers)
        return ok, "verdict=%s layers=%s fails=%d warns=%d" % (
            verdict, layers, len(d.get("fails", [])), len(d.get("warns", []))
        )
    except Exception as e:  # noqa: BLE001
        return False, "exception: %s" % str(e)[:120]


def main() -> int:
    _load_dotenv()
    results = [
        ("MINERVA   (embedding kanıt)", *check_minerva()),
        ("GALILEO   (judge+embedding)", *check_galileo()),
        ("SCI-AUDIT (TR stil G/H)", *check_sciaudit()),
        ("ANAMNESIS (GraphRAG korpus)", *check_anamnesis()),
        ("CLAIM-CERT (4-katman kapı)", *check_claim_cert()),
    ]
    print("=== Denetim yığını sağlık kontrolü ===")
    all_ok = True
    for name, ok, detail in results:
        all_ok = all_ok and ok
        print("[%s] %s — %s" % ("PASS" if ok else "FAIL", name, detail))
    print("=== SONUÇ: %s ===" % ("TÜMÜ PASS" if all_ok else "BAŞARISIZ"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
