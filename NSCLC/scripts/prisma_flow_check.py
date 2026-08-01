#!/usr/bin/env python3
"""PRISMA akış aritmetiği denetçisi (HARD, deterministik).

`03_screening/<konu>_prisma_counts.csv` (şablon:
templates/07_prisma_flow_template.csv) sayılarının iç-tutarlılığını sınar:

  tekillestirme_oncesi_toplam  = tanimlanan_kayit_veritabani + tanimlanan_kayit_diger_yontem
  taranan_kayit                = tekillestirme_oncesi_toplam - cikarilan_duplikat
  tam_metin_degerlendirilen    = taranan_kayit - dislanan_kayit_tab
  dahil_edilen_calisma         = tam_metin_degerlendirilen - dislanan_tam_metin

Ayrıca: dahil_edilen_rapor >= dahil_edilen_calisma (çalışma ≠ rapor);
negatif sayı yok. LLM yoktur; yalnız aritmetik.

Kullanım:
  python3 scripts/prisma_flow_check.py 03_screening/<konu>_prisma_counts.csv
Çıkış: blocker varsa 1, yoksa 0.
"""

from __future__ import annotations

import sys

from _common import Report, print_report, read_rows, to_float


def _counts(path: str) -> dict:
    rows = read_rows(path)
    out = {}
    for r in rows:
        stage = (r.get("asama") or "").strip()
        if not stage:
            continue
        out[stage] = to_float(r.get("sayi"))
    return out


def check(path: str) -> Report:
    rep = Report()
    c = _counts(path)

    required = [
        "tanimlanan_kayit_veritabani",
        "tekillestirme_oncesi_toplam",
        "cikarilan_duplikat",
        "taranan_kayit",
        "dislanan_kayit_tab",
        "tam_metin_degerlendirilen",
        "dislanan_tam_metin",
        "dahil_edilen_calisma",
    ]
    for key in required:
        if c.get(key) is None:
            rep.add("prisma_flow", "blocker",
                    f"'{key}' sayısı eksik/ayrıştırılamadı", locator=key)

    # negatif kontrol
    for k, v in c.items():
        if v is not None and v < 0:
            rep.add("prisma_flow", "blocker", f"'{k}' negatif ({v:g})", locator=k)

    def eq(name, lhs, rhs_terms):
        lv = c.get(lhs)
        parts = [c.get(t) for t in rhs_terms]
        if lv is None or any(p is None for p in parts):
            return
        rhs = parts[0]
        for p in parts[1:]:
            rhs = rhs - p if name.startswith("sub") else rhs + p
        if abs(lv - rhs) > 1e-9:
            op = " − " if name.startswith("sub") else " + "
            rep.add("prisma_flow", "blocker",
                    f"{lhs} ({lv:g}) ≠ {op.join(rhs_terms)} ({rhs:g})",
                    locator=lhs)

    # toplam = db + diğer  (diğer yoksa 0 kabul edilir)
    if c.get("tanimlanan_kayit_diger_yontem") is None:
        c["tanimlanan_kayit_diger_yontem"] = 0.0
    eq("add", "tekillestirme_oncesi_toplam",
       ["tanimlanan_kayit_veritabani", "tanimlanan_kayit_diger_yontem"])
    eq("sub", "taranan_kayit",
       ["tekillestirme_oncesi_toplam", "cikarilan_duplikat"])
    eq("sub", "tam_metin_degerlendirilen",
       ["taranan_kayit", "dislanan_kayit_tab"])
    eq("sub", "dahil_edilen_calisma",
       ["tam_metin_degerlendirilen", "dislanan_tam_metin"])

    # rapor >= çalışma (çoklu yayın)
    rap = c.get("dahil_edilen_rapor")
    cal = c.get("dahil_edilen_calisma")
    if rap is not None and cal is not None and rap < cal:
        rep.add("prisma_flow", "blocker",
                f"dahil_edilen_rapor ({rap:g}) < dahil_edilen_calisma ({cal:g}); "
                "rapor ≥ çalışma olmalı", locator="dahil_edilen_rapor")
    return rep


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("kullanım: prisma_flow_check.py <prisma_counts.csv>", file=sys.stderr)
        return 2
    return print_report("prisma_flow", check(argv[1]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
