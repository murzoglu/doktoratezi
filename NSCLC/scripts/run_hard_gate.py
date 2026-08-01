#!/usr/bin/env python3
"""NSCLC SR HARD-gate orkestratörü (deterministik; LLM yok).

sci-audit'in LLM eksenlerinden ÖNCE koşulan deterministik teslim-engeli kapısı
(playbook F7 Adım 0; sci-audit referansı §0/§3). Dört denetçiyi birleştirir:

  1. prisma_flow_check        — PRISMA akış aritmetiği
  2. extraction_direction_check — çıkarım/meta yön-mantığı (HR/GA/I²/ORR/p)
  3. source_singularity_check — metin sayıları ↔ artefakt (gömülü literal yasağı)
  4. turkish_p_check          — Türkçe ondalık-virgül imlası

Herhangi bir denetçide blocker varsa exit-kod 1 (teslim engeli). LLM-judge
(galileo) yalnız bu kapı temizse koşulur.

Kullanım:
  python3 scripts/run_hard_gate.py 07_manuscript/<konu>.md \
      --extraction 04_extraction/<konu>_extraction.csv \
      --meta       06_synthesis/<konu>_meta.csv \
      --prisma     03_screening/<konu>_prisma_counts.csv \
      --lang tr

Yol verilmeyen kontrol atlanır ve raporda SKIP olarak işaretlenir.
"""

from __future__ import annotations

import argparse
import os
import sys

import context_source_guard as cg
import extraction_direction_check as ed
import prisma_flow_check as pf
import source_singularity_check as ss
import turkish_p_check as tp
from _common import print_report


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manuscript")
    ap.add_argument("--extraction")
    ap.add_argument("--meta")
    ap.add_argument("--prisma")
    ap.add_argument("--lang", default="tr", choices=["tr", "en"])
    ns = ap.parse_args(argv[1:])

    exit_code = 0
    ran, skipped = [], []

    def run(name: str, cond: bool, fn):
        nonlocal exit_code
        if not cond:
            skipped.append(name)
            print(f"[{name}] SKIP (girdi verilmedi)")
            return
        rc = print_report(name, fn())
        ran.append(name)
        exit_code = exit_code or rc

    print("=== NSCLC SR HARD-gate (deterministik) ===")

    run("prisma_flow", bool(ns.prisma) and os.path.exists(ns.prisma),
        lambda: pf.check(ns.prisma))

    ext_ok = bool(ns.extraction) and os.path.exists(ns.extraction)
    run("extraction_dir", ext_ok, lambda: ed.check(ns.extraction))
    run("context_guard", ext_ok, lambda: cg.check(ns.extraction))
    if ns.meta and os.path.exists(ns.meta):
        run("meta_dir", True, lambda: ed.check(ns.meta))
        run("meta_context_guard", True, lambda: cg.check(ns.meta))

    sources = [p for p in (ns.extraction, ns.meta) if p and os.path.exists(p)]
    run("source_singularity", os.path.exists(ns.manuscript) and bool(sources),
        lambda: ss.check(ns.manuscript, sources))

    run("turkish_p", os.path.exists(ns.manuscript) and ns.lang == "tr",
        lambda: tp.check(ns.manuscript))

    print("=== özet ===")
    print(f"  koşulan: {', '.join(ran) or '—'}")
    print(f"  atlanan: {', '.join(skipped) or '—'}")
    print(f"  sonuç:   {'FAIL (blocker var)' if exit_code else 'PASS'}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
