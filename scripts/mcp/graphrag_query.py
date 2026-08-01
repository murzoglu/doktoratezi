#!/usr/bin/env python3
"""GraphRAG sorgu + sentez orkestratörü — tez yazımı bağlam motoru.

`/tez-literatur` ve tartışma yazımı için provenance-damgalı bağlam paketi üretir.
Üç retrieval sinyalini birleştirir:

  1. anamnesis.hybrid_query   FLAGSHIP chunk retrieval (bge-m3 vektör ∥ BM25 →
                              RRF → bge-reranker) ∪ bilgi grafiği genişletmesi.
  2. anamnesis.graph_neighbors  sorgu-kavramlarından n-hop komşu referanslar
                                (GraphRAG bağlam zenginleştirme).
  3. Galileo embedding          İKİNCİ-GÖRÜŞ çapraz-doğrulama: her getirilen
                                chunk'ı sorguya karşı bağımsız bir embedding
                                ailesiyle (3072-boyut) yeniden skorlar. İki
                                embedding ailesinin uyuşması = düşük hallüsinasyon
                                riski; uyuşmazlık = insan-incelemesi bayrağı.

Neden çapraz-doğrulama? anamnesis retrieval'ı worker-internal bge-m3 kullanır ve
dışarıdan vektör kabul etmez; Galileo'yu retrieval'a enjekte edemeyiz. Ama
getirilen chunk'ları bağımsız embedding (Azure text-embedding-3-large) ile yeniden skorlayarak tek-model
yanlılığını kırar ve "bu chunk gerçekten sorguyla ilgili mi?" sorusuna ikinci bir
kanıt katmanı ekleriz. Bu, tam-doğruluk hedefinin retrieval ayağıdır.

KVKK: sorgular ve getirilen literatür chunk'ları yayımlanmış içeriktir; ham
katılımcı verisi asla. Galileo'ya yalnız sorgu + literatür chunk'ı gider.

Kullanım:
  python3 scripts/mcp/graphrag_query.py "aşırı koruma ve metabolik kontrol" \
      --queries "parental overprotection glycemic control" --k 6
  python3 scripts/mcp/graphrag_query.py "..." --json > baglampaketi.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anamnesis_client import AnamnesisClient, load_dotenv  # noqa: E402

_ROOT = Path(__file__).resolve().parents[2]
_GALILEO = _ROOT / "scripts" / "eval" / "galileo_bridge.py"

# Sorgu → aday kavram düğümleri eşlemesi (graph genişletme için).
_CONCEPT_TRIGGERS = {
    "Tip 1 diyabet": ["diyabet", "diabetes", "t1dm", "tip 1"],
    "Aşırı koruma": ["aşırı koru", "overprotection"],
    "Ebeveynlik tutumu": ["ebeveyn", "parenting", "tutum"],
    "Ebeveyn-çocuk ilişkisi": ["ebeveyn-çocuk", "parent-child", "ilişki"],
    "Anne depresyonu": ["depres", "beck"],
    "Kardeş uyumu": ["kardeş", "sibling"],
    "Psikososyal uyum": ["psikososyal", "uyum", "adjustment"],
    "HbA1c / metabolik kontrol": ["hba1c", "metabolik", "glisemik", "glycemic"],
    "Meta-analiz": ["meta-anali", "meta-analy"],
}


def _galileo_claim_match(claim: str, source_text: str) -> float | None:
    """Galileo embedding cosine — Azure text-embedding-3-large (galileo_claim_source_match). None=erişilemez."""
    if not _GALILEO.exists():
        return None
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
                    "clientInfo": {"name": "graphrag", "version": "1.0"},
                },
            }
        ),
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "galileo_claim_source_match",
                    "arguments": {"claim": claim[:1000], "source_text": source_text[:2000]},
                },
            }
        ),
    ]
    try:
        proc = subprocess.run(
            [sys.executable, str(_GALILEO)],
            input="\n".join(calls) + "\n",
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line, strict=False)
        except json.JSONDecodeError:
            continue
        if d.get("id") == 2:
            c = d.get("result", {}).get("content", [])
            if c:
                try:
                    obj = json.loads(c[0].get("text", ""))
                    return obj.get("score")
                except (json.JSONDecodeError, TypeError):
                    return None
    return None


def _candidate_concepts(text: str) -> list[str]:
    low = text.lower()
    out = []
    for concept, trigs in _CONCEPT_TRIGGERS.items():
        if any(t in low for t in trigs):
            out.append(concept)
    return out


def graphrag_context(
    query: str,
    queries: list[str] | None = None,
    k: int = 6,
    cross_validate: bool = True,
) -> dict:
    """Birleşik GraphRAG bağlam paketi üret."""
    load_dotenv()
    client = AnamnesisClient().connect()

    # 1) FLAGSHIP hybrid retrieval
    hq = client.hybrid_query(query, queries=queries, k=k)
    chunks = hq.get("chunks", []) if isinstance(hq, dict) else []

    # 2) Graph genişletme: sorgu-kavramlarından komşu referanslar
    graph_expansion = {}
    for concept in _candidate_concepts(query + " " + " ".join(queries or [])):
        try:
            gn = client.graph_neighbors(concept, hops=1)
            if isinstance(gn, dict) and gn.get("found"):
                refs = sorted(
                    {
                        e.get("subject")
                        for e in gn.get("edges", [])
                        if e.get("subject") != concept
                    }
                )
                if refs:
                    graph_expansion[concept] = refs
        except Exception:  # noqa: BLE001
            continue

    # 3) Galileo ikinci-görüş çapraz-doğrulama (TAMAMLAYICI rol: post-retrieval).
    #    Galileo embedding, anamnesis bge-m3 hattına ENJEKTE EDİLMEZ;
    #    yalnız bağımsız ikinci-görüş skoru ve füzyon yeniden-sıralaması üretir.
    cross = {"enabled": cross_validate, "scored": 0, "flags": []}
    if cross_validate and chunks:
        # anamnesis sıra-tabanlı normalleştirme (skorlar RRF sonrası çok sıkışık olabilir)
        n = len(chunks)
        for anam_rank, ch in enumerate(chunks):
            ch["anamnesis_rank"] = anam_rank + 1
            txt = ch.get("text", "")
            if not txt:
                ch["galileo_score"] = None
                continue
            g = _galileo_claim_match(query, txt)
            ch["galileo_score"] = g
            if g is not None:
                cross["scored"] += 1

        # Füzyon skoru: ağırlıklı (anamnesis-sıra ⊕ galileo cosine).
        #  anamnesis RRF skorları bu korpusta sıkışık/degenere olabildiği için
        #  (doktrin dosyaları Türkçe BM25 anahtar-eşleşmesiyle üste çıkar),
        #  bağımsız ilgi ölçüsü galileo'ya daha yüksek ağırlık verilir.
        _W_ANAM, _W_GAL = 0.4, 0.6
        for ch in chunks:
            ar = ch.get("anamnesis_rank", n)
            anam_norm = (n - (ar - 1)) / n if n else 0.0
            g = ch.get("galileo_score")
            if g is not None:
                ch["fused_score"] = round(_W_ANAM * anam_norm + _W_GAL * g, 4)
            else:
                ch["fused_score"] = round(anam_norm, 4)

        fused_order = sorted(
            range(n), key=lambda i: chunks[i].get("fused_score", 0.0), reverse=True
        )

        # Uyuşmazlık bayrakları — İKİ YÖNLÜ:
        #  A) anamnesis üst-sıra ama galileo düşük → olası yanlış-pozitif (gürültü chunk).
        #  B) anamnesis alt-sıra ama galileo yüksek → gömülü ilgili kaynak (retrieval kaçırdı).
        for i, ch in enumerate(chunks):
            g = ch.get("galileo_score")
            if g is None:
                continue
            ar = ch.get("anamnesis_rank", n)
            if ar <= max(1, n // 3) and g < 0.40:
                cross["flags"].append(
                    {
                        "doc_id": ch.get("doc_id"),
                        "type": "olası-gürültü",
                        "anamnesis_rank": ar,
                        "galileo": round(g, 3),
                        "note": "üst-sırada ama gemini ilgisiz buluyor",
                    }
                )
            elif ar > max(1, (2 * n) // 3) and g > 0.60:
                cross["flags"].append(
                    {
                        "doc_id": ch.get("doc_id"),
                        "type": "gömülü-ilgili",
                        "anamnesis_rank": ar,
                        "galileo": round(g, 3),
                        "note": "alt-sırada ama gemini yüksek ilgi buluyor — füzyon öne çeker",
                    }
                )
        cross["fused_order"] = [chunks[i].get("doc_id") for i in fused_order]

    return {
        "query": query,
        "sub_queries": queries or [],
        "retrieval": hq.get("retrieval", {}) if isinstance(hq, dict) else {},
        "chunks": chunks,
        "graph_expansion": graph_expansion,
        "cross_validation": cross,
        "provenance_note": (
            "chunks: anamnesis bge-m3 (vector∥bm25→rrf→rerank); "
            "graph_expansion: D1 knowledge graph n-hop; "
            "galileo_score: bağımsız Azure text-embedding-3-large ikinci-görüş cosine; "
            "fused_score: anamnesis-sıra ⊕ galileo (post-retrieval yeniden-sıralama, "
            "bge-m3'e enjekte edilmez)."
        ),
    }


def _render_markdown(pkg: dict) -> str:
    lines = ["# GraphRAG Bağlam Paketi", ""]
    lines.append("**Sorgu:** %s" % pkg["query"])
    if pkg["sub_queries"]:
        lines.append("**Alt-sorgular:** %s" % ", ".join(pkg["sub_queries"]))
    r = pkg.get("retrieval", {})
    lines.append(
        "**Retrieval:** %s · k=%s · chunks=%s · graph_edges=%s"
        % (r.get("pipeline", "?"), r.get("k", "?"), r.get("chunks", "?"), r.get("graph_edges", "?"))
    )
    cv = pkg["cross_validation"]
    lines.append(
        "**Çapraz-doğrulama:** %d chunk gemini ile skorlandı · %d uyuşmazlık bayrağı"
        % (cv["scored"], len(cv["flags"]))
    )
    lines.append("")
    lines.append("## Getirilen Kanıt Chunk'ları (anamnesis sırası)")
    for i, ch in enumerate(pkg["chunks"], 1):
        g = ch.get("galileo_score")
        gtxt = ("%.3f" % g) if isinstance(g, (int, float)) else "n/a"
        fs = ch.get("fused_score")
        fstxt = (" · füzyon=%.3f" % fs) if isinstance(fs, (int, float)) else ""
        lines.append(
            "%d. **%s** (anamnesis=%.3f · galileo=%s%s)"
            % (i, ch.get("doc_id", "?"), ch.get("score", 0), gtxt, fstxt)
        )
        lines.append("   > %s" % ch.get("text", "")[:280].replace("\n", " "))
    fused = cv.get("fused_order")
    if fused:
        lines.append("")
        lines.append("## Füzyon Yeniden-Sıralaması (anamnesis-sıra ⊕ galileo)")
        lines.append("_Post-retrieval; bge-m3'e enjekte edilmez, yalnız insan/karar önceliği._")
        lines.append("")
        lines.append("%s" % " → ".join(fused))
    if pkg["graph_expansion"]:
        lines.append("")
        lines.append("## Bilgi Grafiği Genişletmesi")
        for concept, refs in pkg["graph_expansion"].items():
            lines.append("- **%s** → %s" % (concept, ", ".join(refs)))
    if cv["flags"]:
        lines.append("")
        lines.append("## ⚠️ Çapraz-Doğrulama Uyuşmazlıkları (insan incelemesi)")
        for f in cv["flags"]:
            lines.append(
                "- **%s** [%s] anamnesis-sıra=%s · galileo=%.3f — %s"
                % (
                    f.get("doc_id", "?"),
                    f.get("type", "?"),
                    f.get("anamnesis_rank", "?"),
                    f.get("galileo", 0.0),
                    f.get("note", ""),
                )
            )
    lines.append("")
    lines.append("_%s_" % pkg["provenance_note"])
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", help="ana doğal-dil sorgu (Türkçe olabilir)")
    ap.add_argument(
        "--queries",
        default="",
        help="virgülle ayrık ek alt-sorgular (multi-query recall için, İng. önerilir)",
    )
    ap.add_argument("--k", type=int, default=6, help="getirilecek chunk sayısı")
    ap.add_argument("--json", action="store_true", help="ham JSON çıktı")
    ap.add_argument(
        "--no-cross-validate",
        action="store_true",
        help="Galileo ikinci-görüş çapraz-doğrulamayı kapat (daha hızlı)",
    )
    args = ap.parse_args()

    subq = [s.strip() for s in args.queries.split(",") if s.strip()]
    pkg = graphrag_context(
        args.query,
        queries=subq or None,
        k=args.k,
        cross_validate=not args.no_cross_validate,
    )
    if args.json:
        print(json.dumps(pkg, ensure_ascii=False, indent=2))
    else:
        print(_render_markdown(pkg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
