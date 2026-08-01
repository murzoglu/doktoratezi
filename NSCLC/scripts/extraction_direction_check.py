#!/usr/bin/env python3
"""Çıkarım/meta yön-mantığı denetçisi (HARD, deterministik).

`04_extraction/<konu>_extraction.csv` (ve varsa `06_synthesis/<konu>_meta.csv`)
her satırında sayısal yön kaidelerini sınar (playbook §4):

  - hr > 0                       (HR≤0 imkânsız)
  - ci95_lo ≤ hr ≤ ci95_hi       (nokta tahmin GA içinde)
  - ci95_lo ≤ ci95_hi           (alt ≤ üst)
  - I² ∈ [0, 100]  (varsa i2 sütunu)
  - ORR/oran alanları ∈ [0, 100] (varsa)
  - p ∈ [0, 1]                  (varsa p sütunu)

Değeri boş/`unverified` olan alan atlanır (no-fabrication: eksik ≠ hata; ama
mevcut bir sayı yanlış yöndeyse blocker). LLM yoktur.

Kullanım:
  python3 scripts/extraction_direction_check.py 04_extraction/<konu>_extraction.csv
"""

from __future__ import annotations

import sys

from _common import Report, print_report, read_rows, to_float

_PCT_FIELDS = ("orr", "i2", "pd_l1", "oran")


def check(path: str) -> Report:
    rep = Report()
    rows = read_rows(path)
    if not rows:
        rep.add("extraction_dir", "blocker", "boş/başlıksız CSV", locator=path)
        return rep

    for i, r in enumerate(rows, start=2):  # 1=başlık
        sid = (r.get("study_id") or r.get("endpoint") or f"satır{i}").strip()
        hr = to_float(r.get("hr"))
        lo = to_float(r.get("ci95_lo"))
        hi = to_float(r.get("ci95_hi"))
        p = to_float(r.get("p"))

        if hr is not None and hr <= 0:
            rep.add("extraction_dir", "blocker",
                    f"HR={hr:g} ≤ 0 (imkânsız)", locator=sid)
        if lo is not None and hi is not None and lo > hi:
            rep.add("extraction_dir", "blocker",
                    f"ci95_lo ({lo:g}) > ci95_hi ({hi:g})", locator=sid)
        if hr is not None and lo is not None and hr < lo:
            rep.add("extraction_dir", "blocker",
                    f"HR ({hr:g}) < ci95_lo ({lo:g})", locator=sid)
        if hr is not None and hi is not None and hr > hi:
            rep.add("extraction_dir", "blocker",
                    f"HR ({hr:g}) > ci95_hi ({hi:g})", locator=sid)
        if p is not None and not (0.0 <= p <= 1.0):
            rep.add("extraction_dir", "blocker",
                    f"p={p:g} ∉ [0,1]", locator=sid)

        for f in _PCT_FIELDS:
            v = to_float(r.get(f))
            if v is not None and not (0.0 <= v <= 100.0):
                rep.add("extraction_dir", "blocker",
                        f"{f}={v:g} ∉ [0,%100]", locator=sid)

        # kaynak lokatörü olmadan sayı yazılmışsa uyarı (izlenebilirlik)
        has_num = any(x is not None for x in (hr, lo, hi, p))
        locator = (r.get("source_locator") or "").strip()
        pmid = (r.get("pmid_doi") or "").strip()
        if has_num and not locator and not pmid:
            rep.add("extraction_dir", "warning",
                    "sayısal değer var ama source_locator/pmid_doi boş "
                    "(izlenebilirlik)", locator=sid)
    return rep


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("kullanım: extraction_direction_check.py <extraction|meta.csv>",
              file=sys.stderr)
        return 2
    return print_report("extraction_dir", check(argv[1]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
