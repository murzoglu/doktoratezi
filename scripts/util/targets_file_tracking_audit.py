#!/usr/bin/env python3
"""`_targets.R` dosya-izleme (format="file") linter'ı — Kaide-2 (salt-okuma).

Sayısal Bütünlük Kaideleri (AGENTS.md) Kaide-2: bir hedefin okuduğu türetilmiş
CSV/RDS `_targets.R`'de `format = "file"` ile izlenir; kaynak artefakt değişince
içerik-hash geçersizlemesi tetiklenir, stale değer okunmaz. Bu denetçi, bir
`tar_target(...)` gövdesinde `data/processed/...` veya `outputs/...` altındaki
bir yolu DOĞRUDAN LİTERAL olarak bir okuma fonksiyonuna (read_csv/read.csv/
readRDS/read_rds/fread/readr::read_*) geçiren ama aynı hedefte `format = "file"`
taşımayan durumları işaretler. Yardımcı fonksiyon üzerinden okunan (yol literali
gövdede olmayan) hedefler KAPSAM DIŞI (yanlış-pozitif düşük).

Exit: 0 = izlenmeyen literal-yol okuma yok · 1 = en az bir Kaide-2 ihlali adayı.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

_HERE = os.path.abspath(__file__)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
TARGETS = "_targets.R"

READ_FN = re.compile(
    r"\b(?:readr::)?(?:read_csv|read_csv2|read\.csv|read\.csv2|readRDS|read_rds|fread|read_tsv|read\.delim)\s*\(",
    re.IGNORECASE,
)
TRACKED_PATH = re.compile(r'["\'](?:\./)?(data/processed/|outputs/)[^"\']+["\']')
FORMAT_FILE = re.compile(r"format\s*=\s*[\"']file[\"']")


def _iter_tar_target_blocks(src):
    """`tar_target(` konumlarından dengeli-parantez blokları çıkar."""
    for m in re.finditer(r"\btar_target\s*\(", src):
        i = m.end() - 1  # açan '(' konumu
        depth = 0
        j = i
        while j < len(src):
            ch = src[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    yield src[i:j + 1]
                    break
            j += 1


def audit(path):
    ap = path if os.path.isabs(path) else os.path.join(REPO_ROOT, path)
    if not os.path.exists(ap):
        return None, []
    with open(ap, encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    findings = []
    for block in _iter_tar_target_blocks(src):
        # Hedef adı (ilk argüman) — raporlama için.
        name_m = re.match(r"\(\s*([A-Za-z0-9._]+)", block)
        name = name_m.group(1) if name_m else "?"
        if not READ_FN.search(block):
            continue
        paths = TRACKED_PATH.findall(block)  # yalnız desen kökünü döndürür
        literal_paths = re.findall(r'["\'](?:\./)?((?:data/processed/|outputs/)[^"\']+)["\']', block)
        if not literal_paths:
            continue
        if FORMAT_FILE.search(block):
            continue
        findings.append((name, sorted(set(literal_paths))))
    return src, findings


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="_targets.R format=file dosya-izleme linter'ı (salt-okuma).")
    ap.add_argument("--targets", default=TARGETS)
    args = ap.parse_args(argv)
    src, findings = audit(args.targets)
    if src is None:
        print(f"SKIP: {args.targets} yok")
        return 0
    if findings:
        print(f"KAİDE-2 İHLALİ ADAYI: {len(findings)} hedef literal türetilmiş-yol "
              f"okuyor ama format=\"file\" taşımıyor")
        for name, paths in findings[:20]:
            print(f"  tar_target({name}): " + ", ".join(paths))
        return 1
    print("temiz: literal türetilmiş-yol okuyan izlenmeyen hedef yok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
