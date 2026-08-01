#!/usr/bin/env python3
"""
thesis_quote_parity.py -- Tez-duzeyi verbatim parity denetleyicisi

chapters/*.qmd dosyalarindaki verbatim alintilari + (Aile N, rol, yas) etiketlerini
yakalar ve sunlari denetler:

  (a) Etiketli her alinti niteliksel/06_manuscript_outputs/quotes_used.csv
      manifestinde (aile_no, rol) ciftiyle eslesmeli.
  (b) Etikette tarih deseni (DD.MM.YYYY, DD/MM/YY vb.) -> FAIL
      (KVKK de-identify kapisi); yas alaninda gercek ad deseni de aranir.
  (c) Taninmayan rol yuzeyi -> FAIL -- CANONICAL_ROLES kapisi aktiftir.

Desteklenen alinti bicimleri:
  guillemet alinti   (Aile N, rol, yas ifadesi)
  kirvik tirnak      (Aile N, rol, yas ifadesi)   [U+201C / U+201D]

Yas ifadesi: "N yas" veya "N yas M ay"

Rol yuzey -> kanonik:
  anne                       -> mother
  hasta / hasta cocuk        -> t1dm_child
  T1DM'li cocuk              -> t1dm_child
  kardes / saglikli kardes   -> healthy_sibling

Cikti: exit 0 = temiz, 1 = eslenmemis/kacak alinti

CLI:
  python3 thesis_quote_parity.py --chapter bolum.qmd --manifest quotes_used.csv
"""

import argparse
import csv
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Rol kanoniklestirme haritasi (Turkce yuzey -> kanonik)
# Normalizasyon: .strip().lower() uygulanir; apostrof varyantlari dahil.
# _ROL_MAP_EXTRA kaldirildi; tek harita.
# ---------------------------------------------------------------------------
ROL_MAP: dict[str, str] = {
    # Anne
    "anne": "mother",
    "mother": "mother",
    # Hasta cocuk / T1DM'li cocuk
    "hasta": "t1dm_child",
    "hasta \xe7ocuk": "t1dm_child",              # "hasta çocuk"
    "t1dm’li \xe7ocuk": "t1dm_child",       # T1DM'li çocuk (U+2019)
    "t1dm'li \xe7ocuk": "t1dm_child",             # T1DM'li çocuk (ASCII ')
    "t1dm‘li \xe7ocuk": "t1dm_child",        # T1DM'li çocuk (U+2018)
    "t1dm_child": "t1dm_child",
    "patient": "t1dm_child",
    # Saglikli kardes / kardes
    "kardeş": "healthy_sibling",             # "kardeş"
    "kardes": "healthy_sibling",
    "sağlıklı kardeş": "healthy_sibling",  # "sağlıklı kardeş"
    "saglikli kardes": "healthy_sibling",
    "sağlıklı kardes": "healthy_sibling",
    "saglikli kardeş": "healthy_sibling",
    "healthy_sibling": "healthy_sibling",
    "sibling": "healthy_sibling",
}

# Kabul edilen kanonik roller -- audit_chapter'da aktif kapidan gecmesi zorunlu
CANONICAL_ROLES: frozenset[str] = frozenset({"mother", "t1dm_child", "healthy_sibling"})

# ---------------------------------------------------------------------------
# Regex desenleri
# ---------------------------------------------------------------------------

# Verbatim alinti govdesi: guillemet veya kirvik cift tirnak (U+201C / U+201D)
_LEFT_CURLY = "“"   # "
_RIGHT_CURLY = "”"  # "

_QUOTE_BODY = (
    "(?:"
    "«[^»]+»"                              # « guillemet »
    "|"
    + _LEFT_CURLY + "[^" + _RIGHT_CURLY + "]+" + _RIGHT_CURLY  # " kirvik tirnak "
    + ")"
)

# Etiket: (Aile N, rol, yas ifadesi)
_LABEL = r"\(Aile\s+(\d+),\s*([^,]+?),\s*([^)]+?)\)"

QUOTE_LABEL_RE = re.compile(
    _QUOTE_BODY + r"\s*" + _LABEL,
    re.UNICODE,
)

# KVKK denetimleri
DATE_RE = re.compile(
    r"\d{1,2}[./]\d{1,2}[./]\d{2,4}",
    re.UNICODE,
)

# Ad deseni: art arda iki buyuk harfli Turkce/Latin sozcuk (Ilk Soyad).
# YALNIZ yas alanina uygulanir -- rol alanindaki buyuk harfli yuzey
# formlari (Saglikli Kardes, Hasta Cocuk) false-positive uretir.
NAME_RE = re.compile(
    "[A-Z\xc7ĞİI\xd6Ş\xdc]"      # buyuk harf (Latin+Turkce)
    "[a-z\xe7ğıi\xf6ş\xfc]{2,}"  # kucuk harf, min 2
    r"\s+"
    "[A-Z\xc7ĞİI\xd6Ş\xdc]"
    "[a-z\xe7ğıi\xf6ş\xfc]{2,}",
    re.UNICODE,
)


# ---------------------------------------------------------------------------
# Yardimci fonksiyonlar
# ---------------------------------------------------------------------------

def _normalize_aile_no(raw: str) -> str:
    """On sifirlari kaldirir: '011' -> '11', '201' -> '201'."""
    return str(int(raw.strip()))


def load_manifest(manifest_path: str) -> set[tuple[str, str]]:
    """
    Manifest CSV'yi yukler; (normalize_aile_no, canonical_rol) kumesi doner.
    """
    pairs: set[tuple[str, str]] = set()
    with open(manifest_path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            aile_no = row.get("aile_no", "").strip()
            rol = row.get("rol", "").strip()
            if aile_no and rol:
                try:
                    pairs.add((_normalize_aile_no(aile_no), rol))
                except ValueError:
                    pairs.add((aile_no, rol))
    return pairs


def canonicalize_rol(surface: str) -> str | None:
    """Rol yuzeyini kanonik forma cevirir; taninmiyorsa None doner.

    Etiketler nesir icinde satir sonuna sarabildiginden ic bosluklar
    (bosluk, satir sonu, sekme) tek boslu ga indirgenir; boylece
    "saglikli\\nkardes" da "saglikli kardes" olarak taninir.
    """
    normalized = re.sub(r"\s+", " ", surface).strip().lower()
    return ROL_MAP.get(normalized)


# ---------------------------------------------------------------------------
# Denetim
# ---------------------------------------------------------------------------

def audit_chapter(qmd_path: str, manifest_path: str) -> list[str]:
    """
    QMD dosyasini denetler; bulunan hata listesini doner.
    Bos liste -> temiz.

    Kontrol sirasi:
      (b) DATE_RE: etiket genelinde tarih deseni
      (b) NAME_RE: YALNIZ yas alaninda ad deseni (rol alani kapsam disi)
      (c) Rol kanoniklestirme + CANONICAL_ROLES aktif kapisi
      (a) Manifest eslesme
    """
    errors: list[str] = []
    manifest = load_manifest(manifest_path)

    text = Path(qmd_path).read_text(encoding="utf-8")
    matches = list(QUOTE_LABEL_RE.finditer(text))

    if not matches:
        return errors  # Etiketli alinti yok -> temiz

    for m in matches:
        aile_no_raw: str = m.group(1).strip()
        rol_surface: str = m.group(2).strip()
        yas_expr: str = m.group(3).strip()
        label_full: str = m.group(0)

        # (b) Tarih deseni -> FAIL (KVKK) -- etiket genelinde
        if DATE_RE.search(label_full):
            errors.append(
                f"KVKK-TARIH: Etikette tarih deseni bulundu. "
                f"Etiket: '{label_full}'"
            )
            continue

        # (b) Ad deseni -> FAIL (KVKK) -- YALNIZ yas alaninda ara.
        # Rol alaninda buyuk harfli yuzey formlar bekleniyor (Saglikli Kardes,
        # Hasta Cocuk); rol alanina NAME_RE uygulamak false-positive uretir.
        if NAME_RE.search(yas_expr):
            errors.append(
                f"KVKK-AD: Yas alaninda ad deseni bulundu. "
                f"Etiket: '{label_full}'"
            )
            continue

        # (c) Taninmayan rol -> FAIL (CANONICAL_ROLES aktif kapisi)
        canonical = canonicalize_rol(rol_surface)
        if canonical is None or canonical not in CANONICAL_ROLES:
            errors.append(
                f"TANIMSIZ-ROL: '{rol_surface}' kanoniklestirilemiyor "
                "ya da CANONICAL_ROLES disinda. "
                "Bilinen yuzeyler: anne, hasta, hasta cocuk, T1DM'li cocuk, "
                "kardes, saglikli kardes. "
                f"Etiket: '{label_full}'"
            )
            continue

        # (a) Manifest eslesme -> FAIL
        try:
            aile_no_norm = _normalize_aile_no(aile_no_raw)
        except ValueError:
            aile_no_norm = aile_no_raw

        if (aile_no_norm, canonical) not in manifest:
            errors.append(
                f"MANIFEST-EKSIK: (aile_no={aile_no_raw}, rol={canonical}) "
                "quotes_used.csv'de bulunamadi. "
                f"Etiket: '{label_full}'"
            )

    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _default_manifest() -> str:
    """Repo kokunden kanonik manifest yolunu cozumler."""
    return str(
        Path(__file__).parents[2]
        / "niteliksel"
        / "06_manuscript_outputs"
        / "quotes_used.csv"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tez bolumu verbatim parity denetleyicisi"
    )
    parser.add_argument(
        "--chapter",
        required=True,
        help="Denetlenecek .qmd dosyasi yolu",
    )
    parser.add_argument(
        "--manifest",
        default=_default_manifest(),
        help=(
            "Manifest CSV yolu "
            "(varsayilan: niteliksel/06_manuscript_outputs/quotes_used.csv)"
        ),
    )
    args = parser.parse_args()

    errors = audit_chapter(args.chapter, args.manifest)

    if errors:
        print(f"[HATA] {len(errors)} parity sorunu bulundu:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("[TEMIZ] Verbatim parity denetimi gecti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
