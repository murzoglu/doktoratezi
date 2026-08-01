#!/usr/bin/env python3
"""Tam tez GPT-5.4 judge orkestratörü (Galileo bağımsız ikinci-görüş).

Her chapters/*.qmd bölümünü GPT-5.4 LLM-as-judge'a gönderir:
faithfulness / groundedness / citation_support / marmara_compliance / hallucination_risk.
Büyük bölümler başlık sınırlarında güvenli parçalara bölünür (judge token bütçesi).

KVKK: gateway'e YALNIZ manuskript metni gönderilir; ham veri/transkript/kimlikleyici ASLA.
Çıktı: JSON (stdout) — konsolide rapora beslenir.
"""
import json, os, re, sys, time
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import galileo_bridge as g

REPO = os.environ.get("CLAUDE_PROJECT_DIR") or str(Path(__file__).resolve().parents[2])
CH = os.path.join(REPO, "chapters")

# İçerik bölümleri (ön/arka madde judge kapsamı dışı: kısaltma listesi, özgeçmiş, ekler
# statik/placeholder ağırlıklı). Judge gövde metni bölümlerine odaklanır.
SECTIONS = [
    ("00c_ozet_summary.qmd", "ozet"),
    ("01_giris_ve_amac.qmd", "giris"),
    ("02_genel_bilgiler.qmd", "genel_bilgiler"),
    ("03_gerec_ve_yontem.qmd", "yontem"),
    ("04_bulgular.qmd", "bulgular"),
    ("05_tartisma_ve_sonuc.qmd", "tartisma"),
]

MAX_CHARS = 12000  # judge başına güvenli metin bütçesi


def strip_code_fences(txt):
    """R/python chunk'larını çıkar — judge yalnız düzyazıyı değerlendirsin."""
    out, keep = [], True
    for line in txt.splitlines():
        s = line.strip()
        if s.startswith("```"):
            keep = not keep if s.startswith("```{") or s == "```" else keep
            # basit toggle: ``` her görüldüğünde durum değiştir
            keep = not keep
            continue
        if keep:
            out.append(line)
    return "\n".join(out)


def chunk_by_headings(txt, max_chars=MAX_CHARS):
    """Metni ## başlık sınırlarında max_chars altı parçalara böl."""
    if len(txt) <= max_chars:
        return [txt]
    blocks, cur = [], []
    for line in txt.splitlines():
        if line.startswith("## ") and cur and sum(len(x) for x in cur) > max_chars * 0.5:
            blocks.append("\n".join(cur)); cur = []
        cur.append(line)
        if sum(len(x) for x in cur) > max_chars:
            blocks.append("\n".join(cur)); cur = []
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(
        description="Tam tez Galileo judge orkestratörü.")
    ap.add_argument("--out", help="JSON çıktısını bu dosyaya da yaz "
                                  "(K5-GAL-01 tazelik artefaktı).")
    args = ap.parse_args(argv)
    results = []
    for fname, stype in SECTIONS:
        path = os.path.join(CH, fname)
        if not os.path.exists(path):
            continue
        raw = open(path, encoding="utf-8").read()
        body = strip_code_fences(raw)
        chunks = chunk_by_headings(body)
        for ci, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            for attempt in range(2):
                try:
                    j = g.t_galileo_judge({"text": chunk, "section_type": stype})
                    results.append({
                        "file": fname, "section": stype,
                        "chunk": ci + 1, "chunks_total": len(chunks),
                        "chars": len(chunk),
                        "scores": j["scores"],
                        "rationale": j.get("rationale", "")[:400],
                        "flagged": j.get("flagged_spans", [])[:5],
                        "parse_error": j.get("parse_error", False),
                    })
                    break
                except Exception as e:
                    if attempt == 1:
                        results.append({"file": fname, "section": stype,
                                        "chunk": ci + 1, "error": str(e)[:200]})
                    else:
                        time.sleep(2)
    payload = {"judge_model_env": "GALILEO_JUDGE_MODEL",
               "n_evals": len(results), "results": results}
    blob = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(blob)
    print(blob)


if __name__ == "__main__":
    main()
