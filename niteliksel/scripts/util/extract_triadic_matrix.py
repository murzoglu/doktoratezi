#!/usr/bin/env python3
"""triadik tablo.xlsx -> uzun-format CSV (aile,rol,eksen,verbatim). Yerel/gitignored."""
import csv, pathlib, openpyxl

BASE = pathlib.Path(__file__).resolve().parents[2] / "new"
XLSX = BASE / "triadik tablo.xlsx"
OUT  = BASE / "triadik_matris_extracted.csv"

ROLE = {"ANNE": "mother", "HASTA": "t1dm_child", "KARDEŞ": "healthy_sibling", "KARDES": "healthy_sibling"}
AXIS_SLUGS = ["hastalik_algisi","kisit","gunluk_sosyal","ergenlik","kaybetme_korkusu",
              "kardes_yasantisi","annelik_donusum","ihtiyaclar"]

def pad_family(n):
    return n.strip().zfill(3)

def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)
    rows = list(wb.active.iter_rows(values_only=True))
    recs = []
    for r in rows[1:]:
        label = (r[0] or "").strip()
        if not label:
            continue
        parts = label.split()
        role = ROLE.get(parts[0].upper())
        fam = pad_family(parts[-1])
        if not role:
            continue
        for j, slug in enumerate(AXIS_SLUGS, start=1):
            cell = r[j] if j < len(r) else None
            if cell and str(cell).strip():
                recs.append({"aile_no": fam, "rol": role, "triadik_eksen": slug,
                             "verbatim_tr": str(cell).strip()})
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["aile_no","rol","triadik_eksen","verbatim_tr"])
        w.writeheader()
        w.writerows(recs)
    print(f"{len(recs)} hücre -> {OUT}")

if __name__ == "__main__":
    main()
