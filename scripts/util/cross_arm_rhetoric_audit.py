#!/usr/bin/env python3
"""Karma cross-arm retorik denetçisi (salt-okuma, stdlib, ağsız).

Karma yöntem disiplini: nitel ve nicel kollar birbirini "doğrulamaz/kanıtlamaz/
ispatlamaz" — bulgular yakınsar/tamamlar/genişletir (convergence), ama bir kol
diğerini KANITLAMAZ (JARS-Mixed; karma-sentez-kanonik). Bu araç, aynı cümlede
HEM nitel HEM nicel kol göstergesi VE bir "doğrula/kanıtla/ispatla" fiili geçen
cross-arm aşırı-iddia cümlelerini işaretler. `karma_ledger_check` yalnız 6
ledger satırını korurdu; bu araç §2-§5 + ch05 nesrine yayar (etüt madde H).

Tek-kol doğrulaması (ör. "nicel sonuçlar doğrulandı") KAPSAM DIŞI — yalnız iki
kolu birbirine bağlayan kanıt-iddiası işaretlenir (yanlış-pozitif koruması).

Exit: 0 = temiz · 1 = en az bir cross-arm aşırı-iddia.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

_HERE = os.path.abspath(__file__)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DEFAULT_PATHS = ["chapters"]

QUAL = re.compile(r"\b(nitel|tema|temalar|görüşme|gorusme|alınt|alint|RTA|"
                  r"refleksif|kod(?:lama)?)\b", re.IGNORECASE)
QUANT = re.compile(r"\b(nicel|regresyon|ANCOVA|beta|β|ICC|SEM|ölçek|olcek|"
                   r"katsayı|katsayi)\b|p\s*[<=>]", re.IGNORECASE)
# Yalnız AÇIK FİİL çekimleri (isim/homograf hariç): 'kanıtlar/kanıtların' İSİM
# (kanıt+lar), 'doğrulama aracı' İSİM'dir → eşleşmez. Fiil ekleri: -yan/-yor/
# -dığı/-makta/-mış/-dı vb. ('kanıtla-', 'doğrula-', 'ispatla-' + fiil eki).
_VERB_STEM = r"(?:doğrula|dogrula|kanıtla|kanitla|ispatla)"
_VERB_SUFFIX = (r"(?:yan|yen|yor|dığı|diği|duğu|düğü|makta|mekte|"
                r"mış|miş|muş|müş|dı|di|du|dü)")
CONFIRM = re.compile(rf"\b{_VERB_STEM}{_VERB_SUFFIX}\w*|"
                     r"\bteyit\s+ed(?:en|er|iyor|di|mekte)\w*", re.IGNORECASE)
# Olumsuzlama: cümle 'değil' içeriyorsa (doğru disiplin beyanı) VEYA fiil
# olumsuz çekimliyse cross-arm İDDİASI değildir → işaretleme.
NEG_SENT = re.compile(r"\bde[ğg]il\b", re.IGNORECASE)
NEG_VERB = re.compile(r"(ma|me)[zy]\b", re.IGNORECASE)

_FENCE = re.compile(r"^[ \t]*(```|~~~).*?$.*?^[ \t]*\1[ \t]*$", re.M | re.S)


def _strip_code(txt):
    return _FENCE.sub("", txt or "")


def _iter_files(paths):
    for p in paths:
        ap = p if os.path.isabs(p) else os.path.join(REPO_ROOT, p)
        if os.path.isdir(ap):
            for root, _d, files in os.walk(ap):
                for f in files:
                    if f.endswith((".qmd", ".md", ".Rmd")):
                        yield os.path.join(root, f)
        elif os.path.isfile(ap):
            yield ap


def scan(paths):
    findings = []
    for fn in _iter_files(paths):
        try:
            with open(fn, encoding="utf-8", errors="replace") as fh:
                text = _strip_code(fh.read())
        except OSError:
            continue
        rel = os.path.relpath(fn, REPO_ROOT)
        # Cümle bazlı: confirm + qual + quant birlikte VE olumsuzlama yoksa.
        for sent in re.split(r"(?<=[.!?])\s+", text):
            cm = CONFIRM.search(sent)
            if not cm:
                continue
            if NEG_SENT.search(sent):
                continue  # '...doğrulayan ... olarak değil' = doğru disiplin
            if NEG_VERB.search(cm.group(0)):
                continue  # 'doğrulamaz' = olumsuz fiil
            if QUAL.search(sent) and QUANT.search(sent):
                findings.append((rel, sent.strip()[:140]))
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Karma cross-arm retorik denetçisi (salt-okuma).")
    ap.add_argument("--paths", nargs="*", default=None)
    args = ap.parse_args(argv)
    findings = scan(args.paths if args.paths else DEFAULT_PATHS)
    if findings:
        print(f"CROSS-ARM AŞIRI-İDDİA: {len(findings)} cümle (bir kol diğerini "
              f"'doğrular/kanıtlar' — yakınsama diliyle değiştirin)")
        for rel, frag in findings[:20]:
            print(f"  {rel}: {frag}")
        return 1
    print("temiz: cross-arm kanıt-iddiası yok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
