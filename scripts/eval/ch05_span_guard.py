#!/usr/bin/env python3
"""ch05 klinisyen-uyarlama DOKUNULMAZ span bekçisi (salt-okuma).

Kaynak (git referansı) ile çalışma ağacındaki bölümü karşılaştırır; sayı/atıf/
çapraz-referans/etiket çokluklarının (multiset) birebir korunduğunu mekanik
doğrular. Düşme/mutasyon = FAIL. Eklenen abartı/halüsinasyonu YAKALAMAZ.
"""
from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter

DEFAULT_PATH = "chapters/05_tartisma_ve_sonuc.qmd"

PATTERNS = {
    "atif": r"\[@[^\]]+\]",
    "capraz_ref": r"@(?:tbl|fig|sec|eq)-[A-Za-z0-9_\-]+",
    "bolum_ref": r"§[0-9]+(?:\.[0-9]+)*",
    "sayi": r"(?<![A-Za-z0-9])[−\-]?[0-9]+(?:[.,][0-9]+)*(?![0-9])",
}


def spans(text: str) -> Counter:
    bag: Counter = Counter()
    for name, pat in PATTERNS.items():
        for m in re.finditer(pat, text):
            # Satır sarması mutasyon değildir: span içi boşluklar normalize edilir.
            bag[(name, re.sub(r"\s+", " ", m.group(0)))] += 1
    return bag


def read_ref(ref: str, path: str) -> str:
    return subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def main() -> int:
    ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PATH
    with open(path, encoding="utf-8") as fh:
        new = fh.read()
    old = read_ref(ref, path)

    old_bag, new_bag = spans(old), spans(new)
    missing = old_bag - new_bag
    added = new_bag - old_bag

    print(f"kaynak={ref}:{path}  span={sum(old_bag.values())}  yeni_span={sum(new_bag.values())}")
    if missing:
        print("\nDUSEN/MUTASYONA UGRAYAN (FAIL):")
        for (kind, val), n in sorted(missing.items()):
            print(f"  - [{kind}] {val!r} x{n}")
    if added:
        print("\nEKLENEN (inceleme gerektirir):")
        for (kind, val), n in sorted(added.items()):
            print(f"  + [{kind}] {val!r} x{n}")
    if not missing and not added:
        print("PASS: dusme yok, ekleme yok.")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
