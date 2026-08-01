#!/usr/bin/env python3
"""Kaynak-tekilliği denetçisi (HARD, deterministik).

Manüskript metnindeki her sayısal iddia (HR/oran/p gibi) üretilmiş artefaktta
(`04_extraction/*_extraction.csv` ve/veya `06_synthesis/*_meta.csv`) bulunmalıdır;
metne gömülü literal taşınamaz (playbook §4 kaynak-tekilliği; kök depodaki
`csr_numeric_trace_audit.py` deseninin SR uyarlaması).

Yöntem: manüskriptten sayı-benzeri token'ları çıkar; artefakt hücrelerindeki
sayı kümesiyle karşılaştır. Kaynak kümesinde bulunmayan her metin-sayısı blocker.
Yıl (1900–2099), saf tamsayı sayımlar (n) ve alıntılanan-literatür bağlamı
(parantez-içi atıf yakını) gürültüyü azaltmak için elenir.

Kullanım:
  python3 scripts/source_singularity_check.py <manuscript.md> \
      --sources 04_extraction/x_extraction.csv 06_synthesis/x_meta.csv
"""

from __future__ import annotations

import argparse
import re
import sys

from _common import Report, print_report, read_rows

# ondalıklı (tr virgül veya nokta) veya HR-benzeri sayılar; saf tamsayı hariç
_TEXT_NUM = re.compile(r"(?<![\w.,])\d{1,3}(?:[.,]\d+)(?![\w])")
_YEAR = re.compile(r"^(19|20)\d{2}$")


def _norm(tok: str) -> str:
    """'0,72' ve '0.72' aynı anahtara normalize."""
    return tok.replace(" ", "").replace(",", ".")


def _source_numbers(paths: list[str]) -> set[str]:
    nums: set[str] = set()
    for p in paths:
        for row in read_rows(p):
            for cell in row.values():
                if cell is None:
                    continue
                for m in re.findall(r"\d{1,3}(?:[.,]\d+)?", str(cell)):
                    nums.add(_norm(m))
    return nums


def check(manuscript: str, sources: list[str]) -> Report:
    rep = Report()
    src = _source_numbers(sources)
    if not src:
        rep.add("source_singularity", "warning",
                "kaynak artefaktlarında sayı bulunamadı; karşılaştırma zayıf",
                locator=",".join(sources))

    with open(manuscript, encoding="utf-8") as fh:
        text = fh.read()

    seen: set[str] = set()
    for m in _TEXT_NUM.finditer(text):
        tok = m.group(0)
        key = _norm(tok)
        if key in seen:
            continue
        seen.add(key)
        if _YEAR.match(tok.replace(",", "").replace(".", "")):
            continue
        if key not in src:
            # bağlam parçası (izleme kolaylığı)
            a, b = max(0, m.start() - 30), min(len(text), m.end() + 30)
            ctx = text[a:b].replace("\n", " ").strip()
            rep.add("source_singularity", "blocker",
                    f"metindeki '{tok}' kaynak artefaktlarda yok "
                    f"(gömülü literal?): …{ctx}…", locator=tok)
    return rep


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manuscript")
    ap.add_argument("--sources", nargs="+", required=True)
    ns = ap.parse_args(argv[1:])
    return print_report("source_singularity", check(ns.manuscript, ns.sources))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
