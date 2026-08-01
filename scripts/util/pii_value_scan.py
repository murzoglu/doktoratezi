#!/usr/bin/env python3
"""Değer-şekilli PII tarayıcı — tüm manuskript yüzeyi (salt-okuma).

`chk_pii_no_names` yalnız ham-veri KOLON adı kalıntısını (ad_soyad ...) ve
yalnız `chapters/` gövdesini tarıyordu. Bu araç, katılımcı PII'sinin DEĞER
biçimlerini (11-hane T.C. kimlik no, gün.ay.yıl doğum tarihi, hasta/protokol/
dosya numarası) TÜM manuskript dosyalarında (bölümler + CSR + ön/arka) tarar.
Kaba yıl (2024), n-sayısı (241), p-değeri gibi bilimsel sayılar KAPSAM DIŞI
kalacak biçimde desenler dardır.

KVKK: yalnız metin dosyaları okunur; `data/raw|identified|cleaned|backup` ve
`data/processed`/`outputs` satır düzeyi ASLA okunmaz.

Muafiyet: resmi tez kılavuzunun zorunlu kıldığı kişisel alanlar (Marmara SBE
şablonu §9 ÖZGEÇMİŞ: Doğum Tarihi, Tel) `ALLOWLIST` üzerinden dosya+sınıf+satır
bağlamı üçlüsüyle muaf tutulabilir; muaf bulgular "MUAF" satırı olarak yine
raporlanır. Katılımcı kimliğine ulaştırabilecek sınıflar (`NON_EXEMPTIBLE`:
T.C. kimlik no, hasta/protokol no) muaf edilemez. `--strict` tüm muafiyetleri
yok sayar.

Exit: 0 = aday PII değeri yok · 1 = en az bir aday (teslim engeli).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

_HERE = os.path.abspath(__file__)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))

# Varsayılan manuskript yüzeyi (data/ ağaçları HARİÇ — KVKK).
DEFAULT_GLOBS = [
    "chapters",  # tüm *.qmd
    "docs/CLINICAL-STUDY-REPORT-FINAL.md",
]

# Değer-şekilli PII desenleri (dar; bilimsel sayı yanlış-pozitifi düşük).
# Üçlü: (desen, insan-okunur etiket, sınıf anahtarı). Sınıf anahtarı muafiyet
# kaydının bağladığı kanonik addır.
PATTERNS = [
    # T.C. kimlik no: 11 hane, ilk hane 0 değil. Yıl(4)/n(2-3) eşleşmez.
    # Ondalık nokta komşuluğu HARİÇ (3951.12345678901 gibi yüksek-hassasiyet
    # kesirler T.C. no değildir → lookbehind/lookahead'e '.' eklendi).
    (re.compile(r"(?<![\d.])[1-9]\d{10}(?![\d.])"), "T.C. kimlik no (11 hane)",
     "tckn"),
    # Hasta/protokol/dosya numarası: etiket + 4+ hane.
    (re.compile(r"\b(?:hasta|protokol|dosya|başvuru|kay[ıi]t)\s*(?:no|numaras[ıi])?\s*[:=]?\s*\d{4,}\b",
                re.IGNORECASE), "hasta/protokol/dosya numarası", "hasta-no"),
    # Telefon: +90 veya 05xx ile 10-11 hane.
    (re.compile(r"(?<!\d)(?:\+90|0)\s?5\d{2}[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}(?!\d)"),
     "telefon numarası", "telefon"),
]

# --- Muafiyet kaydı (dar · gerekçeli · denetlenebilir) ---------------------
# Resmi tez kılavuzu bazı kişisel alanları ZORUNLU kılar (Marmara SBE
# "TEZ ŞABLONLARI-2026-2RV.docx" §9 ÖZGEÇMİŞ tablosu: Doğum Tarihi, Tel).
# Bu alanlar araştırmacının KENDİ bilgisidir; katılımcı PII'si değildir.
#
# Tasarım kararları:
#  1. Muafiyet manuskripte işaret koymadan verilir → render çıktısına hiçbir
#     şey sızmaz, tez metni temiz kalır.
#  2. Bir muafiyet ancak ÜÇ koşul birden tutarsa uygulanır: dosya + sınıf +
#     satır bağlam deseni. Böylece aynı dosyada etiketsiz/başka bir telefon
#     yine yakalanır.
#  3. Muaf bulgu sessizce yutulmaz; "MUAF" olarak raporlanır (denetim izi).
#  4. Muafiyet eklemek kod değişikliği gerektirir → bilinçli, gözden geçirilmiş
#     karar olmasını zorlar.
#
# NON_EXEMPTIBLE: katılımcı kimliğine ulaştırabilecek sınıflar. Bu sınıflar
# için kayıt yazılsa bile muafiyet UYGULANMAZ (aşağıda sertçe süzülür).
NON_EXEMPTIBLE = frozenset({"tckn", "hasta-no"})

ALLOWLIST = [
    {
        "dosya": "chapters/06_ozgecmis_faaliyetler.qmd",
        "sinif": frozenset({"telefon", "dogum-tarihi"}),
        "satir_deseni": re.compile(r"\*\*\s*(?:Tel|Do[ğg]um Tarihi)\s*\*\*",
                                   re.IGNORECASE),
        "gerekce": ("Marmara SBE tez şablonu §9 ÖZGEÇMİŞ zorunlu alanları "
                    "(Doğum Tarihi, Tel); araştırmacının kendi bilgisi, "
                    "katılımcı verisi değil"),
        "onay": "kullanıcı istisnai onayı · 2026-07-30",
    },
]

# Tam tarih (gg.aa.yyyy | gg/aa/yyyy | gg-aa-yyyy, yıl 19xx/20xx). Tek başına
# PII DEĞİLDİR (etik onayı / veri toplama / kabul tarihi gibi çalışma tarihleri
# meşrudur); yalnız aynı satırda doğum-bağlamı işareti varsa PII sayılır →
# yanlış-pozitif koruması.
DATE_RX = re.compile(
    r"(?<!\d)(0[1-9]|[12]\d|3[01])[./-](0[1-9]|1[0-2])[./-](?:19|20)\d{2}(?!\d)")
BIRTH_CUE = re.compile(r"do[ğg]um|\bbirth\b|\bd\.?o\.?b\b|do[ğg]\.", re.IGNORECASE)


def _iter_files(paths):
    for p in paths:
        ap = p if os.path.isabs(p) else os.path.join(REPO_ROOT, p)
        if os.path.isdir(ap):
            for root, _dirs, files in os.walk(ap):
                for f in files:
                    if f.endswith((".qmd", ".md", ".Rmd")):
                        yield os.path.join(root, f)
        elif os.path.isfile(ap):
            yield ap


def _exemption_for(rel, key, line):
    """Bu (dosya, sınıf, satır) üçlüsü için geçerli muafiyet kaydını döndür.

    Katılımcı kimliğine ulaştırabilecek sınıflar (NON_EXEMPTIBLE) hiçbir kayıtla
    muaf edilemez; kayıt yazılmış olsa bile burada süzülür.
    """
    if key in NON_EXEMPTIBLE:
        return None
    rel_norm = rel.replace(os.sep, "/")
    for entry in ALLOWLIST:
        if entry["dosya"] != rel_norm:
            continue
        if key not in entry["sinif"]:
            continue
        if not entry["satir_deseni"].search(line):
            continue
        return entry
    return None


def scan(paths, strict=False):
    """(bulgular, muaflar) döndür.

    `strict=True` ise muafiyet kayıtları yok sayılır ve her eşleşme bulgu olur
    (kapanış/teslim denetimi için tam görünürlük).
    """
    findings = []
    exempted = []
    for fn in _iter_files(paths):
        try:
            with open(fn, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        rel = os.path.relpath(fn, REPO_ROOT)
        for i, line in enumerate(text.splitlines(), 1):
            hits = []
            for rx, label, key in PATTERNS:
                m = rx.search(line)
                if m:
                    hits.append((label, key, m.group(0)))
            # Tam tarih yalnız doğum-bağlamında PII (çalışma tarihi muaf).
            if BIRTH_CUE.search(line):
                dm = DATE_RX.search(line)
                if dm:
                    hits.append(("doğum tarihi (bağlamlı)", "dogum-tarihi",
                                 dm.group(0)))
            for label, key, frag in hits:
                entry = None if strict else _exemption_for(rel, key, line)
                if entry is not None:
                    exempted.append((rel, i, label, frag, entry["gerekce"]))
                else:
                    findings.append((rel, i, label, frag))
    return findings, exempted


def _mask(frag):
    """PII değerini kısmen maskele (tam değeri log'a dökme)."""
    if len(frag) > 4:
        return frag[:2] + "•" * (len(frag) - 4) + frag[-2:]
    return "••••"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Değer-şekilli PII tarayıcı (salt-okuma).")
    ap.add_argument("--paths", nargs="*", default=None,
                    help="Taranacak dosya/dizinler (varsayılan: manuskript yüzeyi).")
    ap.add_argument("--strict", action="store_true",
                    help="Muafiyet kayıtlarını yok say; her eşleşmeyi bulgu say.")
    args = ap.parse_args(argv)
    paths = args.paths if args.paths else DEFAULT_GLOBS
    findings, exempted = scan(paths, strict=args.strict)

    # Muaf bulgular sessizce yutulmaz — denetim izi olarak her koşulda basılır.
    for rel, ln, label, frag, why in exempted[:20]:
        print(f"MUAF  {rel}:{ln} — {label}: {_mask(frag)}  [{why}]")

    if findings:
        print(f"PII ADAYI: {len(findings)} bulgu")
        for rel, ln, label, frag in findings[:20]:
            print(f"  {rel}:{ln} — {label}: {_mask(frag)}")
        return 1
    suffix = f" ({len(exempted)} muaf, gerekçeli)" if exempted else ""
    print(f"temiz: değer-şekilli PII adayı yok{suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
