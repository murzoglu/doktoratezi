#!/usr/bin/env python3
"""thesis_semantic — Şerit B ham-vektör deterministik semantik kontroller (spec §4.3).

İki CI-ilgili kontrol, `semantic_core` (Azure text-embedding-3-large) üstünde:

  bib-dup     references.bib başlıklarında semantik yakın-duplikat (Jaccard'ın
              kaçırdığı çeviri/parafraz/transliterasyon dup'larını yakalar).
  redundancy  bölümler-arası semantik paragraf tekrarı (CRC32-shingle'ın
              kaçırdığı parafraz-tekrarı).

Gate duruşu (spec §8): tekrar/near-benzerlik = advisory (exit 2). bib near-dup
yalnız `--strict` ile ve cosine >= HARD eşik olduğunda HARD (exit 1). LLM judge
burada YOK (bu modül deterministik cosine).

Degrade (spec §4.3): galileo embedding erişilemezse SESSİZ ATLAMA YOK —
bib-dup `bib_hygiene` lexical Jaccard'a düşer + not; redundancy `tr_corpus_audit`
coherence'a yönlendiren not verir. KVKK: yalnız manuskript/bib metni gönderilir
(semantic_core tripwire ayrıca zorlar).

Çıkış: 0 temiz · 1 HARD (yalnız --strict + bib near-dup) · 2 SOFT/advisory.
Kullanım:
  python3 scripts/util/thesis_semantic.py bib-dup [--strict] [--json]
  python3 scripts/util/thesis_semantic.py redundancy [--chapters 'chapters/*.qmd'] [--json]
"""
from __future__ import annotations

import argparse
import glob as _glob
import json
import os
import pathlib
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EVAL = os.path.join(os.path.dirname(_HERE), "eval")
for _p in (_HERE, _EVAL):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import semantic_core as sc   # noqa: E402
import bib_hygiene as bh     # noqa: E402

# Varsayılan eşikler (semantic_core'dan miras; galileo.local.md/.env yönetir).
BIB_HARD_MIN = sc.DEDUP_SIM_MIN          # >= bu cosine = gerçek duplikat (0.96 kalibre)
BIB_ADVISORY_MIN = 0.90                   # [advisory, HARD) arası = incele
REDUNDANCY_MIN = 0.88                     # near-duplicate paragraf (same-topic 0.82'nin üstü)

_MIN_PARA_WORDS = 25                      # kısa/başlık bloklarını ele


# ---------------------------------------------------------------- bib-dup
def _bib_items(bib_path: str):
    entries = bh.parse_bib(pathlib.Path(bib_path).read_text(encoding="utf-8"))
    return [{"key": e["key"], "title": e["fields"].get("title", "")}
            for e in entries if e["fields"].get("title")]


def cmd_bib_dup(bib_path: str, advisory_min: float, hard_min: float,
                strict: bool) -> tuple[dict, int]:
    items = _bib_items(bib_path)
    try:
        pairs = sc.dedup_matrix(items, threshold=advisory_min)
    except sc.EmbeddingUnavailable as e:
        # DEGRADE — sessiz atlama yok: string Jaccard'a düş + not.
        entries = bh.parse_bib(pathlib.Path(bib_path).read_text(encoding="utf-8"))
        lex = bh.check_dedup(entries)
        res = {"command": "bib-dup", "mode": "lexical-fallback",
               "note": "embedding erişilemez (%s) → bib_hygiene Jaccard" % str(e)[:80],
               "hard": [], "advisory": lex, "n_entries": len(items)}
        return res, (2 if lex else 0)
    hard = [p for p in pairs if p["sim"] >= hard_min]
    adv = [p for p in pairs if p["sim"] < hard_min]
    res = {"command": "bib-dup", "mode": "embedding", "n_entries": len(items),
           "hard": hard, "advisory": adv, "hard_min": hard_min,
           "advisory_min": advisory_min}
    if strict and hard:
        code = 1
    elif hard or adv:
        code = 2
    else:
        code = 0
    return res, code


# ------------------------------------------------------------- redundancy
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)


def _paragraphs(files: list[str]) -> list[tuple[str, str]]:
    """Manuskript paragraflarını (kod-fence + başlık dışı, >= _MIN_PARA_WORDS) çıkar."""
    out: list[tuple[str, str]] = []
    for f in files:
        try:
            txt = pathlib.Path(f).read_text(encoding="utf-8")
        except OSError:
            continue
        txt = _FENCE_RE.sub("", txt)                 # kod bloklarını at
        for blk in re.split(r"\n\s*\n", txt):
            blk = blk.strip()
            if not blk or blk.startswith("#") or blk.startswith(":::"):
                continue
            # YAML/attr/liste-ağırlıklı blokları ele
            if len(re.findall(r"\w+", blk)) < _MIN_PARA_WORDS:
                continue
            out.append((os.path.relpath(f), blk))
    return out


def cmd_redundancy(chapters: list[str], threshold: float) -> tuple[dict, int]:
    files = sorted({p for c in chapters for p in _glob.glob(c)})
    paras = _paragraphs(files)
    if not paras:
        return {"command": "redundancy", "mode": "empty", "pairs": [],
                "note": "paragraf bulunamadı"}, 0
    try:
        pairs = sc.redundancy_pairs([t for _, t in paras], threshold=threshold)
    except sc.EmbeddingUnavailable as e:
        # DEGRADE — sessiz atlama yok: deterministik CRC32 katmanına yönlendir.
        return {"command": "redundancy", "mode": "unavailable",
                "note": "embedding erişilemez (%s) → scripts/util/tr_corpus_audit.py "
                        "coherence (CRC32-shingle) kullanın" % str(e)[:80],
                "pairs": []}, 0
    rich = [{"a": {"file": paras[p["a"]][0], "excerpt": paras[p["a"]][1][:90]},
             "b": {"file": paras[p["b"]][0], "excerpt": paras[p["b"]][1][:90]},
             "sim": p["sim"]} for p in pairs]
    res = {"command": "redundancy", "mode": "embedding",
           "n_paragraphs": len(paras), "threshold": threshold, "pairs": rich}
    return res, (2 if rich else 0)


# -------------------------------------------------------------------- CLI
def _render(res: dict) -> str:
    cmd = res.get("command")
    lines = ["# thesis_semantic — %s (%s)" % (cmd, res.get("mode")), ""]
    if res.get("note"):
        lines += ["> %s" % res["note"], ""]
    if cmd == "bib-dup":
        lines += ["## HARD — gerçek duplikat (cosine >= %s)" % res.get("hard_min", "?")]
        lines += [f"- `{p['a']}` ↔ `{p['b']}` (sim={p['sim']})" for p in res.get("hard", [])] or ["- (yok)"]
        lines += ["", "## advisory — yakın (incele)"]
        lines += [f"- `{p['a']}` ↔ `{p['b']}` (sim={p['sim']})" for p in res.get("advisory", [])] or ["- (yok)"]
    elif cmd == "redundancy":
        lines += ["## advisory — semantik paragraf tekrarı (sim >= %s)" % res.get("threshold", "?")]
        for p in res.get("pairs", []):
            lines += [f"- {p['a']['file']} ↔ {p['b']['file']} (sim={p['sim']})",
                      f"    A: {p['a']['excerpt']}…", f"    B: {p['b']['excerpt']}…"]
        if not res.get("pairs"):
            lines += ["- (yok)"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Tez semantik kontrolleri (Şerit B)")
    p.add_argument("command", choices=["bib-dup", "redundancy"])
    p.add_argument("--bib", default="references/references.bib")
    p.add_argument("--chapters", nargs="*", default=["chapters/*.qmd"])
    p.add_argument("--advisory-min", type=float, default=BIB_ADVISORY_MIN)
    p.add_argument("--hard-min", type=float, default=BIB_HARD_MIN)
    p.add_argument("--redundancy-min", type=float, default=REDUNDANCY_MIN)
    p.add_argument("--strict", action="store_true",
                   help="bib near-dup cosine >= hard-min ise HARD (exit 1)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--out")
    a = p.parse_args(argv)

    if a.command == "bib-dup":
        res, code = cmd_bib_dup(a.bib, a.advisory_min, a.hard_min, a.strict)
    else:
        res, code = cmd_redundancy(a.chapters, a.redundancy_min)

    if a.out:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.out).write_text(_render(res), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else _render(res))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
