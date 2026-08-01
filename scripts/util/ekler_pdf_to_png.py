#!/usr/bin/env python3
"""docs/ekler/*.pdf -> docs/assets/ekler/*.png donusturucu (tez EKLER bolumu).

Neden bu betik: Marmara Tez Yazim Kilavuzu §3.10 uyarinca olcek kullanim
izinleri, bilgilendirilmis gonullu olur formu ve bos veri toplama formlari
teze Ek olarak, her biri ayri sayfada girer. Tez uc formatta (docx/pdf/html)
render edildiginden bu belgelerin tek tip gomulme yolu sayfa gorseli
uretmektir; `.qmd` tarafinda gorseller `![](docs/assets/ekler/...)` ile
cagrilir.

KVKK: iki olcek izin belgesi Gmail ciktisidir ve ucuncu kisilerin kisisel
e-posta adreslerini icerir. Betik bu adreslerin YEREL kismini (@ oncesi)
maskeler; alan adi ve izin beyaninin metni okunur kalir (or.
`g...k@deu.edu.tr`). Maskeleme raster uzerinde geri donusu olmayan
sekilde yapilir; PNG'de gizlenen metin katmani kalmaz.

Bagimlilik: yalniz poppler-utils (`pdftoppm`, `pdftotext`, `pdftocairo`) ve
Python 3 standart kutuphanesi. Pillow/PyMuPDF GEREKMEZ.

Nasil calisir:
  1. `pdftotext -bbox` ile sayfadaki kelime kutulari + metni okunur; e-posta
     regex'i ile maskelenecek kelimeler bulunur.
  2. `pdftocairo -svg` ile ayni sayfanin glif konumlari (`<use x= y=>`)
     okunur; kelime kutusu icine dusen glifler soldan siralanip kelimenin
     karakterleriyle eslenir. Boylece `@` karakterinin tam x konumu bulunur
     ve maske yalniz yerel kismi kapatacak sekilde daraltilir.
  3. Maske ve kirpma gerekmeyen sayfalar dogrudan `pdftoppm -png` ile
     uretilir (en kucuk dosya). Digerleri `pdftoppm -ppm` ile ham raster
     olarak alinir; once maske dikdortgeni + uc nokta ("...") cizilir, sonra
     manifestteki kirpma kutusu uygulanir ve stdlib `zlib`/`struct` ile PNG
     olarak yazilir.

Kirpma: telefonla cekilmis taramalarda (or. etik kurul onayi) belgenin
cevresinde masa/arka plan payi kalir. Manifestteki `crop` alani sayfa-orani
(x0, y0, x1, y1) kutusudur; bu pay disarida birakilir, belge tez sayfasinda
daha buyuk goruntulenir. `dpi` alani o belge icin `--dpi` degerini ezer.

Kullanim:
  python3 scripts/util/ekler_pdf_to_png.py            # eksikleri uret
  python3 scripts/util/ekler_pdf_to_png.py --force    # hepsini yeniden uret
  python3 scripts/util/ekler_pdf_to_png.py --list     # manifesti yazdir
  python3 scripts/util/ekler_pdf_to_png.py --dpi 200  # cozunurluk

Cikis kodu: 0 basarili; 1 kaynak PDF eksik veya poppler cagrisi hatali.
"""
from __future__ import annotations

import argparse
import html
import math
import os
import re
import struct
import subprocess
import sys
import zlib
from dataclasses import dataclass

# --- Sabitler -------------------------------------------------------------

SRC_DIR = os.path.join("docs", "ekler")
OUT_DIR = os.path.join("docs", "assets", "ekler")
DEFAULT_DPI = 150

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
WORD_RE = re.compile(
    r'<word xMin="([\d.\-]+)" yMin="([\d.\-]+)" '
    r'xMax="([\d.\-]+)" yMax="([\d.\-]+)">(.*?)</word>'
)
USE_RE = re.compile(r'<use[^>]*?\sx="([\d.\-]+)"\s+y="([\d.\-]+)"')


@dataclass(frozen=True)
class EkBelge:
    """Tek bir alt-ek belgesi: kaynak PDF, alinacak sayfalar, cikti onu.

    `dpi` verilirse `--dpi` yerine bu belge icin o cozunurluk kullanilir
    (telefonla cekilmis taramalarda kaynak rasterin kendi cozunurlugunu
    yakalamak icin). `crop` verilirse sayfa, (x0, y0, x1, y1) sayfa-orani
    kutusuna kirpilir; boylece fotograf taramalarindaki masa/arka plan payi
    disarida kalir ve belge tez sayfasinda daha buyuk goruntulenir.
    """

    slug: str
    pdf: str
    pages: tuple  # 1 tabanli sayfa numaralari
    baslik: str
    redact_emails: bool = False
    note: str = ""
    dpi: int = 0  # 0 = --dpi degerini kullan
    crop: tuple = ()  # () = kirpma yok; aksi halde (x0, y0, x1, y1) oran


# Sira, tezdeki ek sirasini izler. Ek 1 onay/izin zinciri belgesidir; Ek 2
# alt ekleri chapters/03_gerec_ve_yontem.qmd "Veri Toplama Araclari" sirasiyla
# hizalidir: once olcek kullanim izinleri, sonra olur formu, demografik
# formlar ve olcek formlari (s-EMBU-C -> s-EMBU-P -> KIA -> Beck).
MANIFEST = (
    EkBelge(
        slug="ek1-etik-kurul-onayi",
        pdf="Etik Kurul Onay.pdf",
        pages=(1,),
        baslik="Ek 1. Etik kurul onayi (protokol 09.2023.201)",
        # Kaynak, telefon kamerasiyla cekilmis tek sayfalik bir taramadir
        # (metin katmani yok, gomulu JPEG ~202 ppi). Kirpma kutusu kagit
        # kenarina gore olculmustur; 200 dpi kaynak rasterin kendi
        # cozunurlugune denk duser.
        dpi=200,
        crop=(0.130, 0.031, 0.874, 0.877),
        note="Metin katmani olmadigindan maskeleme uygulanmaz; belgede e-posta/telefon yoktur.",
    ),
    EkBelge(
        slug="ek2a-embu-kullanim-izni",
        pdf="Gülay Dirik - EMBU.pdf",
        pages=(1, 5),
        baslik="Ek 2a. s-EMBU olcek kullanim izni",
        redact_emails=True,
        note="s.2-3 bos, s.4 kurumsal e-posta feragatnamesi oldugundan alinmadi.",
    ),
    EkBelge(
        slug="ek2b-kia-kullanim-izni",
        pdf="Ercan Alp - KIA.pdf",
        pages=(1,),
        baslik="Ek 2b. Kardes Iliskileri Anketi kullanim izni",
        redact_emails=True,
    ),
    EkBelge(
        slug="ek2c-olur-formu",
        pdf="Bilgilendirilmiş Gönüllü Olur Formu.pdf",
        pages=(1, 2, 3, 4),
        baslik="Ek 2c. Bilgilendirilmis Gonullu Olur Formu",
    ),
    EkBelge(
        slug="ek2d-demografik-diyabetik",
        pdf="Demografik Bilgiler - Diyabetik.pdf",
        pages=(1,),
        baslik="Ek 2d. Demografik ve Tibbi Bilgiler Formu - diyabetli cocuklar grubu",
    ),
    EkBelge(
        slug="ek2e-demografik-saglikli",
        pdf="Demografik Bilgiler - Sağlıklı.pdf",
        pages=(1,),
        baslik="Ek 2e. Demografik ve Tibbi Bilgiler Formu - saglikli kontrol grubu",
    ),
    EkBelge(
        slug="ek2f-embu-cocuk",
        pdf="EMBU Çocuk.pdf",
        pages=(1, 2),
        baslik="Ek 2f. Kisaltilmis Ebeveyn Tutumlari Olcegi - Cocuk Formu (s-EMBU-C)",
    ),
    EkBelge(
        slug="ek2g-embu-ebeveyn",
        pdf="EMBU Ebeveyn.pdf",
        pages=(1, 2),
        baslik="Ek 2g. Kisaltilmis Ebeveyn Tutumlari Olcegi - Ebeveyn Formu (s-EMBU-P)",
    ),
    EkBelge(
        slug="ek2h-kia",
        pdf="Kardeş İlişkileri Anketi.pdf",
        pages=(1, 2),
        baslik="Ek 2h. Kardes Iliskileri Anketi - Cocuk Formu",
    ),
    EkBelge(
        slug="ek2i-beck",
        pdf="Beck Depresyon.pdf",
        pages=(1, 2),
        baslik="Ek 2i. Beck Depresyon Envanteri - Ebeveyn Formu",
    ),
)


# --- Yardimcilar ----------------------------------------------------------


def _run(cmd, binary=False):
    """Poppler cagrisi; hata durumunda stderr ile birlikte yukselir."""
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "komut basarisiz: %s\n%s" % (" ".join(cmd), proc.stderr.decode("utf-8", "replace"))
        )
    return proc.stdout if binary else proc.stdout.decode("utf-8", "replace")


@dataclass
class MaskeKutusu:
    """Raster uzerinde temizlenecek alan (PDF punto biriminde)."""

    x0: float
    y0: float
    x1: float
    y1: float
    dots: bool = True  # kapatilan yere "..." isareti konsun mu


def _glifler(pdf_path: str, page: int):
    """Sayfadaki glif orijin konumlari (x, y) - pdftocairo SVG uzerinden."""
    svg = _run(["pdftocairo", "-svg", "-f", str(page), "-l", str(page), pdf_path, "-"])
    return [(float(m.group(1)), float(m.group(2))) for m in USE_RE.finditer(svg)]


def _kelimeler(pdf_path: str, page: int):
    """Sayfadaki kelime kutulari: (x0, y0, x1, y1, metin)."""
    xml = _run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), pdf_path, "-"])
    out = []
    for m in WORD_RE.finditer(xml):
        out.append(
            (
                float(m.group(1)),
                float(m.group(2)),
                float(m.group(3)),
                float(m.group(4)),
                html.unescape(m.group(5)),
            )
        )
    return out


def eposta_maskeleri(pdf_path: str, page: int):
    """Sayfadaki e-posta adreslerinin yerel kismini kapatan maske kutulari.

    Glif konumlari kelime kutusuna soldan hizalanarak karakter indeksine
    eslenir; `@` glifi en genis ilerlemeye sahip oldugundan indeks eslemesi
    ayrica genislik olcutuyle capraz dogrulanir. Esleme guvenilmezse kelimenin
    tamami kapatilir (guvenli taraf).
    """
    words = _kelimeler(pdf_path, page)
    if not any(EMAIL_RE.search(w[4]) for w in words):
        return []

    glyphs = _glifler(pdf_path, page)
    masks = []
    for x0, y0, x1, y1, text in words:
        m = EMAIL_RE.search(text)
        if not m:
            continue

        tam_kutu = MaskeKutusu(x0, y0, x1, y1, dots=True)
        inside = sorted(
            [g for g in glyphs if x0 - 0.5 <= g[0] < x1 and y0 - 1.0 <= g[1] <= y1 + 1.0],
            key=lambda g: g[0],
        )
        # Glif sayisi karakter sayisindan az ise soldan esleme guvenilmez.
        if len(inside) < len(text):
            masks.append(tam_kutu)
            continue

        s = m.start()  # yerel kismin ilk karakteri
        at = text.index("@", s)
        if at - s < 3:  # maskelenecek ic karakter yok
            masks.append(MaskeKutusu(inside[s][0], y0, inside[at][0], y1))
            continue

        # `@` glifi en genis ilerlemeye sahip olmalidir; +-2 indeks icinde
        # en genis ilerlemeyi arayarak indeks kaymasina karsi dogrula.
        def ilerleme(i):
            if i + 1 < len(inside):
                return inside[i + 1][0] - inside[i][0]
            return x1 - inside[i][0]

        aday = [i for i in range(max(s + 1, at - 2), min(len(inside) - 1, at + 3))]
        if aday:
            at = max(aday, key=ilerleme)
        if at - s < 3:
            masks.append(tam_kutu)
            continue

        mx0 = inside[s + 1][0]
        mx1 = inside[at - 1][0]
        if mx1 - mx0 < 1.0 or mx1 > x1:
            masks.append(tam_kutu)
            continue
        masks.append(MaskeKutusu(mx0, y0, mx1, y1))
    return masks


# --- PPM okuma / PNG yazma (stdlib) --------------------------------------


def _ppm_oku(blob: bytes):
    """Binary PPM (P6) -> (genislik, yukseklik, bytearray RGB)."""
    if not blob.startswith(b"P6"):
        raise RuntimeError("beklenen PPM (P6) basligi bulunamadi")
    fields, pos = [], 2
    while len(fields) < 3:
        while pos < len(blob) and blob[pos : pos + 1].isspace():
            pos += 1
        if blob[pos : pos + 1] == b"#":
            while blob[pos : pos + 1] not in (b"\n", b""):
                pos += 1
            continue
        start = pos
        while pos < len(blob) and not blob[pos : pos + 1].isspace():
            pos += 1
        fields.append(int(blob[start:pos]))
    pos += 1  # basliktan sonraki tek beyaz karakter
    w, h, maxval = fields
    if maxval != 255:
        raise RuntimeError("yalniz 8-bit PPM destekleniyor (maxval=%d)" % maxval)
    return w, h, bytearray(blob[pos : pos + w * h * 3])


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


def _png_yaz(path: str, w: int, h: int, rgb: bytearray, dpi: int) -> None:
    """Filtresiz (type 0) RGB PNG; pHYs ile fiziksel cozunurluk gomulur."""
    stride = w * 3
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += rgb[y * stride : (y + 1) * stride]
    ppm = int(round(dpi / 0.0254))
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n")
        fh.write(_png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)))
        fh.write(_png_chunk(b"pHYs", struct.pack(">IIB", ppm, ppm, 1)))
        fh.write(_png_chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        fh.write(_png_chunk(b"IEND", b""))


def _dikdortgen(rgb: bytearray, w: int, h: int, x0, y0, x1, y1, color=(255, 255, 255), outward=True):
    """Dikdortgen doldurur. `outward=True` kenarlari disari yuvarlar; boylece
    alt-piksel kirpilmasi nedeniyle maskenin kenarinda kalan anti-aliasing
    kalintisi (dusuk cozunurlukte gorunur hale gelen ince iz) silinir."""
    if outward:
        px0, py0 = math.floor(x0), math.floor(y0)
        px1, py1 = math.ceil(x1), math.ceil(y1)
    else:
        px0, py0 = int(round(x0)), int(round(y0))
        px1, py1 = int(round(x1)), int(round(y1))
    px0, px1 = max(0, px0), min(w, px1)
    py0, py1 = max(0, py0), min(h, py1)
    if px1 <= px0 or py1 <= py0:
        return
    satir = bytes(color) * (px1 - px0)
    for y in range(py0, py1):
        off = (y * w + px0) * 3
        rgb[off : off + len(satir)] = satir


def maskeleri_uygula(rgb: bytearray, w: int, h: int, masks, dpi: int) -> None:
    """Maske kutularini beyazla doldurur ve yerine "..." isareti cizer."""
    k = dpi / 72.0
    for mk in masks:
        px0, py0 = mk.x0 * k, mk.y0 * k
        px1, py1 = mk.x1 * k, mk.y1 * k
        _dikdortgen(rgb, w, h, px0, py0, px1, py1)
        if not mk.dots:
            continue
        genislik = px1 - px0
        nokta = max(2.0, 1.3 * k)
        if genislik < 5 * nokta:
            continue
        # Uc nokta, kutunun ortasinda ve taban cizgisine yakin (0.72 yukseklik).
        merkez_y = py0 + 0.72 * (py1 - py0)
        orta = (px0 + px1) / 2.0
        for i in (-1, 0, 1):
            cx = orta + i * 2.0 * nokta
            _dikdortgen(
                rgb,
                w,
                h,
                cx - nokta / 2,
                merkez_y - nokta / 2,
                cx + nokta / 2,
                merkez_y + nokta / 2,
                color=(40, 40, 40),
                outward=False,
            )


# --- Uretim ---------------------------------------------------------------


def cikti_adi(belge: EkBelge, sira: int) -> str:
    return "%s-s%02d.png" % (belge.slug, sira)


def _kirp(w: int, h: int, rgb: bytearray, crop):
    """Sayfa-orani kutusuna gore rasteri kirpar -> (w, h, rgb)."""
    x0 = max(0, min(w - 1, int(round(crop[0] * w))))
    y0 = max(0, min(h - 1, int(round(crop[1] * h))))
    x1 = max(x0 + 1, min(w, int(round(crop[2] * w))))
    y1 = max(y0 + 1, min(h, int(round(crop[3] * h))))
    cw, ch = x1 - x0, y1 - y0
    out = bytearray(cw * ch * 3)
    for j in range(ch):
        src = ((y0 + j) * w + x0) * 3
        out[j * cw * 3 : (j + 1) * cw * 3] = rgb[src : src + cw * 3]
    return cw, ch, out


def sayfa_uret(pdf_path: str, page: int, out_path: str, dpi: int, redact: bool, crop=()) -> None:
    masks = eposta_maskeleri(pdf_path, page) if redact else []
    if not masks and not crop:
        # Maske/kirpma gerekmiyor: poppler'in kendi PNG kodlayicisi en kucuk
        # dosyayi urettiginden dogrudan onu kullan.
        blob = _run(
            ["pdftoppm", "-r", str(dpi), "-png", "-f", str(page), "-l", str(page), pdf_path],
            binary=True,
        )
        with open(out_path, "wb") as fh:
            fh.write(blob)
        return

    blob = _run(
        ["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page), pdf_path],
        binary=True,
    )
    w, h, rgb = _ppm_oku(blob)
    # Maske konumlari tam sayfa uzerinde olculdugunden kirpmadan once uygulanir.
    if masks:
        maskeleri_uygula(rgb, w, h, masks, dpi)
    if crop:
        w, h, rgb = _kirp(w, h, rgb, crop)
    _png_yaz(out_path, w, h, rgb, dpi)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--src", default=SRC_DIR, help="kaynak PDF dizini")
    ap.add_argument("--out", default=OUT_DIR, help="cikti PNG dizini")
    ap.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help="raster cozunurlugu (manifestte dpi verilmis belgeler icin gecersiz)",
    )
    ap.add_argument("--force", action="store_true", help="mevcut ciktilari yeniden uret")
    ap.add_argument("--list", action="store_true", help="manifesti yazdir ve cik")
    args = ap.parse_args(argv)

    if args.list:
        for belge in MANIFEST:
            print(
                "%-28s %-42s sayfa=%-8s dpi=%-4s kirpma=%s"
                % (
                    belge.slug,
                    belge.pdf,
                    ",".join(map(str, belge.pages)),
                    belge.dpi or args.dpi,
                    "var" if belge.crop else "yok",
                )
            )
        return 0

    eksik = [b.pdf for b in MANIFEST if not os.path.isfile(os.path.join(args.src, b.pdf))]
    if eksik:
        for ad in eksik:
            print("HATA: kaynak PDF bulunamadi: %s" % os.path.join(args.src, ad), file=sys.stderr)
        return 1

    os.makedirs(args.out, exist_ok=True)
    uretilen = atlanan = 0
    for belge in MANIFEST:
        pdf_path = os.path.join(args.src, belge.pdf)
        belge_dpi = belge.dpi or args.dpi
        for sira, page in enumerate(belge.pages, start=1):
            out_path = os.path.join(args.out, cikti_adi(belge, sira))
            if os.path.exists(out_path) and not args.force:
                atlanan += 1
                continue
            sayfa_uret(pdf_path, page, out_path, belge_dpi, belge.redact_emails, belge.crop)
            uretilen += 1
            print(
                "uretildi: %s  (%s s.%d, %d dpi%s%s)"
                % (
                    out_path,
                    belge.pdf,
                    page,
                    belge_dpi,
                    ", maskeli" if belge.redact_emails else "",
                    ", kirpilmis" if belge.crop else "",
                )
            )

    print("\nOzet: %d uretildi, %d atlandi (--force ile yeniden uretilir)." % (uretilen, atlanan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
