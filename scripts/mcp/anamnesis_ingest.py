#!/usr/bin/env python3
"""anamnesis GraphRAG besleme runner'ı — tezin referans korpusunu indeksler.

Amaç: tezin `cite-ok` referanslarının yayımlanmış tam-metin/abstract içeriğini
anamnesis GraphRAG substratına yükleyip (ingest_document) + referanslar arası
kavram grafiğini kurar (upsert_triples). Böylece `/tez-literatur` sentezi ve
graphrag_query.py gerçek, provenance-damgalı bir bilgi tabanına dayanır.

Kaynak akışı (KVKK-güvenli — yalnız YAYIMLANMIŞ literatür):
  1. Ledger  (tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md)
     → citation key + DOI/PMID/PMCID + "kullanılan iddia" + durum çıkarılır.
  2. Tam metin/abstract sırayla denenir (ilk başarılı kullanılır):
       a) Europe PMC  (keyless, legal, abstract + varsa PMC tam metin)
       b) Minerva     (fulltext_by_doi — Roche korpusunda varsa)
     Erişilemezse ledger'daki "kullanılan iddia" özeti asgari içerik olur.
  3. anamnesis.ingest_document(doc_id=citation_key, ...) ile indekslenir.
  4. Ledger "kullanılan iddia"sından + sabit tez kavram sözlüğünden
     (T1DM, EMBU, aşırı-koruma, Beck, KİA ...) upsert_triples ile kavram
     grafiği kurulur: (referans) --supports--> (kavram).

KVKK: anamnesis'e YALNIZ yayımlanmış literatür + tez kavramları gider. Ham
katılımcı/aile/transkript/kimlikleyici ASLA. Row-level veri okunmaz.

Idempotent: her doc_id citation key'dir; tekrar çalıştırma üzerine-yazar.
Embedding: anamnesis worker-internal bge-m3 kullanır (dışarıdan vektör yok).

Kullanım:
  python3 scripts/mcp/anamnesis_ingest.py --dry-run          # sadece plan
  python3 scripts/mcp/anamnesis_ingest.py --limit 5          # ilk 5 referans
  python3 scripts/mcp/anamnesis_ingest.py                    # tüm cite-ok
  python3 scripts/mcp/anamnesis_ingest.py --include-exceptions
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anamnesis_client import AnamnesisClient, load_dotenv  # noqa: E402

_ROOT = Path(__file__).resolve().parents[2]
LEDGER = _ROOT / "tez-yazim" / "02_kanit-haritalari" / "referans-denetim-ledgeri.md"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
_CTX = ssl.create_default_context()
_UA = {"User-Agent": "t1dm-graphrag-ingest/1.0"}

# Tez kavram sözlüğü — kanonik varlık düğümleri (graph normalizasyonu).
# Anahtar: normalize kavram; değer: ledger "iddia" metninde aranacak tetikleyiciler.
CONCEPTS: dict[str, list[str]] = {
    "Tip 1 diyabet": ["t1dm", "tip 1", "type 1", "diyabet", "diabetes"],
    "Ebeveynlik tutumu": ["ebeveyn", "parenting", "ebeveynlik", "tutum"],
    "Aşırı koruma": ["aşırı koru", "overprotection", "aşırı-koru"],
    "Ebeveyn-çocuk ilişkisi": ["ebeveyn-çocuk", "parent-child", "ilişki"],
    "Anne depresyonu": ["depresyon", "depression", "beck", "anne depres"],
    "Kardeş uyumu": ["kardeş", "sibling"],
    "Psikososyal uyum": ["psikososyal", "psychosocial", "uyum", "adjustment"],
    "Çoklu bilgi kaynağı": ["çoklu bilgi", "informant", "multi-informant", "örtüş"],
    "Kronik hastalık": ["kronik", "chronic"],
    "Aile işlevselliği": ["aile işlev", "family functioning", "aile"],
    "Meta-analiz": ["meta-anali", "meta-analy", "meta analitik"],
    "HbA1c / metabolik kontrol": ["hba1c", "metabolik", "glisemik", "glycemic"],
}


def _http_get(url: str, timeout: int = 30) -> str | None:
    try:
        req = urllib.request.Request(url, headers=_UA)
        with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
            return r.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return None


# ----------------------------- ledger ayrıştırma ----------------------------
def parse_ledger(include_exceptions: bool = False) -> list[dict]:
    """Ledger tablosundan referans kayıtlarını çıkar."""
    if not LEDGER.exists():
        raise SystemExit("Ledger bulunamadı: %s" % LEDGER)
    refs: list[dict] = []
    seen: set[str] = set()
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 11:
            continue
        key = re.sub(r"[`]", "", cells[1]).strip()
        ids = cells[2]
        doi_m = re.search(r"DOI:\s*`([^`]+)`", ids)
        pmid_m = re.search(r"PMID:\s*`([^`]+)`", ids)
        pmcid_m = re.search(r"PMCID:\s*`([^`]+)`", ids)
        claim = cells[5].strip()
        section = cells[6].strip().strip("`")
        status = re.sub(r"[`]", "", cells[9]).strip()
        # Yalnız gerçek referans satırları (DOI veya PMID olan).
        if not (doi_m or pmid_m):
            continue
        if key in seen:
            continue
        seen.add(key)
        allowed = {"cite-ok"} | ({"full-text-exception"} if include_exceptions else set())
        if status not in allowed:
            continue
        refs.append(
            {
                "key": key,
                "doi": doi_m.group(1) if doi_m else "",
                "pmid": pmid_m.group(1) if pmid_m else "",
                "pmcid": pmcid_m.group(1) if pmcid_m else "",
                "claim": claim,
                "section": section,
                "status": status,
            }
        )
    return refs


# ------------------------- tam metin / abstract çekme -----------------------
def fetch_epmc(ref: dict) -> tuple[str, str]:
    """Europe PMC'den abstract (+ varsa PMC tam metin). (content, source)."""
    q = None
    if ref["doi"]:
        q = "DOI:%s" % ref["doi"]
    elif ref["pmid"]:
        q = "EXT_ID:%s AND SRC:MED" % ref["pmid"]
    if not q:
        return "", ""
    url = "%s/search?query=%s&format=json&resultType=core" % (
        EPMC,
        urllib.parse.quote(q),
    )
    body = _http_get(url)
    if not body:
        return "", ""
    try:
        data = json.loads(body)
        res = data.get("resultList", {}).get("result", [])
    except json.JSONDecodeError:
        return "", ""
    if not res:
        return "", ""
    a = res[0]
    parts = []
    if a.get("title"):
        parts.append("BAŞLIK: %s" % a["title"])
    if a.get("authorString"):
        parts.append("YAZARLAR: %s" % a["authorString"])
    if a.get("journalTitle"):
        parts.append(
            "KAYNAK: %s %s;%s:%s"
            % (
                a.get("journalTitle", ""),
                a.get("pubYear", ""),
                a.get("journalVolume", ""),
                a.get("pageInfo", ""),
            )
        )
    if a.get("abstractText"):
        parts.append("ÖZET: %s" % re.sub(r"<[^>]+>", "", a["abstractText"]))
    content = "\n".join(parts)
    # PMC tam metin (açık erişimse)
    if ref["pmcid"] and a.get("isOpenAccess") == "Y":
        ft = _http_get("%s/%s/fullTextXML" % (EPMC, ref["pmcid"]))
        if ft and len(ft) > 500:
            body_txt = re.sub(r"<[^>]+>", " ", ft)
            body_txt = re.sub(r"\s+", " ", body_txt).strip()
            if len(body_txt) > len(content):
                content = content + "\n\nTAM METİN:\n" + body_txt[:20000]
                return content, "europepmc-fulltext"
    return content, "europepmc-abstract" if content else ""


def fetch_minerva(ref: dict) -> tuple[str, str]:
    """Minerva bridge'inden DOI ile tam metin (varsa)."""
    if not ref["doi"]:
        return "", ""
    bridge = _ROOT / "scripts" / "mcp" / "minerva_evidence_bridge.py"
    if not bridge.exists():
        return "", ""
    import os
    import subprocess

    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(_ROOT)
    calls = [
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "ingest", "version": "1.0"},
                },
            }
        ),
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "minerva_literature_fulltext_by_doi",
                    "arguments": {"doi": ref["doi"]},
                },
            }
        ),
    ]
    try:
        proc = subprocess.run(
            [sys.executable, str(bridge)],
            input="\n".join(calls) + "\n",
            capture_output=True,
            text=True,
            timeout=90,
            env=env,
        )
    except (subprocess.TimeoutExpired, OSError):
        return "", ""
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line, strict=False)
        except json.JSONDecodeError:
            continue
        if d.get("id") != 2:
            continue
        c = d.get("result", {}).get("content", [])
        if not c:
            return "", ""
        txt = c[0].get("text", "")
        try:
            obj = json.loads(txt, strict=False)
        except json.JSONDecodeError:
            return "", ""
        content = obj.get("content") or ""
        title = obj.get("title") or ""
        if content and len(content) > 200:
            return ("BAŞLIK: %s\n\nTAM METİN:\n%s" % (title, content))[:20000], (
                "minerva-fulltext"
            )
    return "", ""


def build_content(ref: dict) -> tuple[str, str]:
    """Kaskad: EPMC → Minerva → ledger-iddia (asgari)."""
    for fetcher in (fetch_epmc, fetch_minerva):
        content, src = fetcher(ref)
        if content and len(content) > 200:
            return content, src
    # Asgari: ledger iddia özeti (her zaman KVKK-güvenli, yayımlanmış künye).
    ids = " ".join(
        filter(None, ["DOI:%s" % ref["doi"] if ref["doi"] else "", "PMID:%s" % ref["pmid"] if ref["pmid"] else ""])
    )
    return (
        "REFERANS: %s (%s)\nKULLANILAN İDDİA: %s"
        % (ref["key"], ids, ref["claim"])
    ), "ledger-claim"


# ------------------------------ kavram grafiği ------------------------------
def derive_triples(ref: dict) -> list[dict]:
    """Ledger iddia + bölüm metninden (referans)->(kavram) üçlüleri türet."""
    hay = (ref["claim"] + " " + ref["section"]).lower()
    triples: list[dict] = []
    for concept, triggers in CONCEPTS.items():
        if any(t in hay for t in triggers):
            triples.append(
                {
                    "subject": ref["key"],
                    "predicate": "supports_concept",
                    "object": concept,
                    "metadata": {"section": ref["section"], "status": ref["status"]},
                }
            )
    return triples


# --------------------------------- ana akış ---------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="sadece plan, yazma yok")
    ap.add_argument("--limit", type=int, default=0, help="ilk N referansla sınırla")
    ap.add_argument(
        "--include-exceptions",
        action="store_true",
        help="full-text-exception satırlarını da al",
    )
    ap.add_argument("--only-key", default="", help="tek citation key ile sınırla (test)")
    args = ap.parse_args()

    load_dotenv()
    refs = parse_ledger(include_exceptions=args.include_exceptions)
    if args.only_key:
        refs = [r for r in refs if r["key"] == args.only_key]
    if args.limit > 0:
        refs = refs[: args.limit]

    print("=== anamnesis GraphRAG besleme ===")
    print("Ledger referans (uygun durum): %d" % len(refs))
    if not refs:
        print("İşlenecek referans yok.")
        return 0

    if args.dry_run:
        for r in refs:
            tr = derive_triples(r)
            print(
                "  [PLAN] %-28s doi=%-28s kavram=%d"
                % (r["key"], r["doi"] or "-", len(tr))
            )
        print("(dry-run — hiçbir şey yazılmadı)")
        return 0

    client = AnamnesisClient().connect()
    before = client.corpus_stats()
    print("Önce: %s" % json.dumps(before, ensure_ascii=False))

    n_ing, n_tri, n_fail = 0, 0, 0
    all_triples: list[dict] = []
    src_hist: dict[str, int] = {}
    for i, ref in enumerate(refs, 1):
        content, src = build_content(ref)
        src_hist[src] = src_hist.get(src, 0) + 1
        try:
            client.ingest_document(
                text=content,
                doc_id=ref["key"],
                title=ref["key"],
                source=src,
                metadata={
                    "doi": ref["doi"],
                    "pmid": ref["pmid"],
                    "section": ref["section"],
                    "status": ref["status"],
                },
            )
            n_ing += 1
            tr = derive_triples(ref)
            all_triples.extend(tr)
            n_tri += len(tr)
            print(
                "  [%d/%d] %-28s src=%-20s kavram=%d"
                % (i, len(refs), ref["key"], src, len(tr))
            )
        except Exception as e:  # noqa: BLE001
            n_fail += 1
            print("  [%d/%d] %-28s HATA: %s" % (i, len(refs), ref["key"], str(e)[:80]))
        time.sleep(0.2)  # gateway'e nazik

    # Kavram üçlülerini toplu yaz (idempotent upsert).
    if all_triples:
        try:
            client.upsert_triples(all_triples)
            print("upsert_triples: %d üçlü yazıldı" % len(all_triples))
        except Exception as e:  # noqa: BLE001
            print("upsert_triples HATA: %s" % str(e)[:120])

    after = client.corpus_stats()
    print("Sonra: %s" % json.dumps(after, ensure_ascii=False))
    print(
        "Özet: ingest=%d başarısız=%d üçlü=%d kaynak=%s"
        % (n_ing, n_fail, n_tri, json.dumps(src_hist, ensure_ascii=False))
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
