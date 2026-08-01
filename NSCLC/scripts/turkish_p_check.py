#!/usr/bin/env python3
"""Türkçe ondalık-imla denetçisi (HARD, deterministik).

Türkçe metinde ondalık ayırıcı **virgüldür**. İngilizce ondalık-nokta ile yazılmış
istatistik değerleri (özellikle `p`, `HR`, `%95 GA`, `I²`) blocker'dır
(sci-audit Axis G). İngilizce özet ayrı denetlenir (`--lang en` ile bu kontrol
gevşetilir; bu script yalnız TR metinler içindir).

Yakalananlar:
  - p = 0.03  /  p<0.001  /  p = .04   (nokta veya baştaki nokta)
  - HR 0.72 / OR 1.35 / RR 0.88       (nokta ile)
  - %95 CI 0.55-0.90                   (nokta ile)

Kullanım:
  python3 scripts/turkish_p_check.py <manuscript.md> [--lang tr|en]
`--lang en` verilirse kontrol atlanır (exit 0).
"""

from __future__ import annotations

import argparse
import re
import sys

from _common import Report, print_report

# p değeri nokta ile: 'p = 0.03', 'p<0.001', 'p = .04', 'p:0.5'
_P_DOT = re.compile(r"\bp\s*[=<>:]\s*\.?\d*\.\d+", re.IGNORECASE)
# etki ölçüsü nokta ile: HR/OR/RR/GA ardından nokta-ondalık
_EFFECT_DOT = re.compile(
    r"\b(HR|OR|RR|aHR|I\u00b2|I2)\b[^\d\n]{0,6}\d+\.\d+", re.IGNORECASE)
# %95 GA/CI aralığı nokta ile
_CI_DOT = re.compile(r"(?:%?95\s*(?:GA|CI|G\u00fcven))[^\d\n]{0,6}\d+\.\d+",
                     re.IGNORECASE)


def check(path: str) -> Report:
    rep = Report()
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    in_code = False
    for ln_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        for rx, label in ((_P_DOT, "p-değeri"),
                          (_EFFECT_DOT, "etki ölçüsü"),
                          (_CI_DOT, "%95 GA")):
            for m in rx.finditer(line):
                rep.add("turkish_p", "blocker",
                        f"{label} İngilizce ondalık-nokta ile: '{m.group(0).strip()}'"
                        " (Türkçe metinde virgül olmalı)",
                        locator=f"satır {ln_no}")
    return rep


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manuscript")
    ap.add_argument("--lang", default="tr", choices=["tr", "en"])
    ns = ap.parse_args(argv[1:])
    if ns.lang == "en":
        print("[turkish_p] --lang en: kontrol atlandı")
        return 0
    return print_report("turkish_p", check(ns.manuscript))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
