#!/usr/bin/env python3
"""Bağlam-kaynak koruması (HARD, deterministik).

Kaide (referans 04 §0): SR'de bir sayısal etki (HR/OS/PFS/ORR/GA) YALNIZ kanıt
katmanından (minerva/openathens/annas + birincil literatür) gelebilir. Bağlam
(ich/titck/eudamed/oecd/health-policy) ve arama-lead (socius-vigil/yok-akademik)
sunucuları sayı besleyemez.

Bu denetçi `04_extraction/*_extraction.csv` (ve varsa `06_synthesis/*_meta.csv`)
`source_tier` sütununu okur:

  source_tier ∈ {evidence, context, lead}

Kural:
  - Satırda sayısal etki alanı (hr/ci95_lo/ci95_hi/orr/estimate) DOLU ise
    source_tier == 'evidence' OLMALIDIR. 'context'/'lead' → blocker.
  - source_tier boş ama sayısal etki dolu ise → blocker (etiketlenmemiş kaynak).
  - source_tier geçersiz değer → blocker.

Kullanım:
  python3 scripts/context_source_guard.py 04_extraction/<konu>_extraction.csv
"""

from __future__ import annotations

import sys

from _common import Report, print_report, read_rows, to_float

_VALID = {"evidence", "context", "lead"}
_EFFECT_FIELDS = ("hr", "ci95_lo", "ci95_hi", "orr", "estimate")


def _has_effect(row: dict) -> bool:
    for f in _EFFECT_FIELDS:
        v = row.get(f)
        if v is None:
            continue
        s = str(v).strip()
        if s == "" or s.startswith("<"):  # <PLACEHOLDER> atla
            continue
        # 'estimate' metinsel olabilir (%45 / 14,2 ay); sayı varsa etki say
        if f == "estimate":
            if any(ch.isdigit() for ch in s):
                return True
            continue
        if to_float(s) is not None:
            return True
    return False


def check(path: str) -> Report:
    rep = Report()
    rows = read_rows(path)
    if not rows:
        rep.add("context_guard", "blocker", "boş/başlıksız CSV", locator=path)
        return rep

    has_col = "source_tier" in rows[0]
    if not has_col:
        rep.add("context_guard", "warning",
                "source_tier sütunu yok; kanıt≠bağlam koruması uygulanamıyor "
                "(şablona ekleyin)", locator=path)

    for i, r in enumerate(rows, start=2):
        sid = (r.get("study_id") or r.get("endpoint") or f"satır{i}").strip()
        if sid.startswith("<"):  # şablon placeholder satırı
            continue
        tier = (r.get("source_tier") or "").strip().lower()
        has_effect = _has_effect(r)

        if tier and tier not in _VALID:
            rep.add("context_guard", "blocker",
                    f"geçersiz source_tier '{tier}' (evidence|context|lead)",
                    locator=sid)
            continue

        if has_effect:
            if not tier:
                rep.add("context_guard", "blocker",
                        "sayısal etki var ama source_tier boş "
                        "(etiketlenmemiş kaynak)", locator=sid)
            elif tier != "evidence":
                rep.add("context_guard", "blocker",
                        f"sayısal etki '{tier}' katmanından besleniyor; "
                        "yalnız 'evidence' katmanı sayı verebilir "
                        "(bağlam/lead sayı veremez)", locator=sid)
    return rep


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("kullanım: context_source_guard.py <extraction|meta.csv>",
              file=sys.stderr)
        return 2
    return print_report("context_guard", check(argv[1]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
