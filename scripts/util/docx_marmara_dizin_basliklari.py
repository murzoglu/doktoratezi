#!/usr/bin/env python3
"""Render sonrasi docx kapak/dizin yerlesimini Marmara duzenine cevirir.

Uc is yapar:

0. **Varsayilan baslik blogu.** Quarto/Pandoc, `title`/`author` metadatasindan
   belgenin en basina `Title` ve `Author` stilli iki paragraf yazar. Marmara
   §2.1 kapagi (`chapters/00_kapak.qmd`) bunun yerine gectiginden bu iki
   paragraf silinir; metadata PDF/DOCX belge ozelliklerinde korunur.

1. **Baslik bicimi.** Quarto docx yazicisi `crossref-lof-title` / `crossref-lot-title`
   ezimini onurlandirmiyor; LOF/LOT dizin basliklari daima Turkce varsayilan
   "Şekil Listesi" / "Tablo Listesi" olarak yaziliyor. Marmara §5 buyuk harf
   "ŞEKİLLER DİZİNİ" / "TABLOLAR DİZİNİ" ister.

2. **Dizin sirasi.** Pandoc `--toc/--lof/--lot` ile uretilen ICINDEKILER, SEKILLER
   ve TABLOLAR dizinlerini daima belgenin en basina (baslik sayfasindan hemen
   sonra) koyar. Marmara §5 resmi sirasi ise:

       Tez onayi -> Beyan -> Tesekkur -> ICINDEKILER -> KISALTMALAR
       -> SEKILLER -> TABLOLAR -> Ozet -> Summary

   Betik uc `<w:sdt>` dizin blogunu bulundugu yerden alip dogru capa basliginin
   (`KISALTMALAR`, `ÖZET`) hemen onune, arkasina sayfa sonu paragrafi ekleyerek
   tasir. PDF hattinda ayni sira `chapters/00a` ve `chapters/00b` icindeki ham
   LaTeX (tableofcontents, listoffigures, listoftables) ile saglanir.

Idempotenttir: baslik blogu zaten silinmisse, baslik zaten buyuk harfse ve
dizinler zaten dogru capanin onunde duruyorsa dosyaya dokunmaz.
"""
from __future__ import annotations

import os
import re
import shutil
import sys
import tempfile
import zipfile

# Quarto post-render, uretilen ciktilari QUARTO_PROJECT_OUTPUT_FILES ile verir
# (satir-ayrik goreli yollar). Yoksa varsayilan tez ciktisi kullanilir.
DEFAULT_TARGETS = ["outputs/quarto/thesis.docx"]

REPLACEMENTS = {
    "Şekil Listesi": "ŞEKİLLER DİZİNİ",
    "Tablo Listesi": "TABLOLAR DİZİNİ",
}

# (dizin blogu docPartGallery degeri, tasinacagi ana baslik). Sira onemlidir:
# ayni capaya birden fazla dizin tasiniyorsa listedeki sirayla arka arkaya dizilir.
INDEX_MOVES = [
    ("Table of Contents", "KISALTMALAR"),
    ("List of Figures", "ÖZET"),
    ("List of Tables", "ÖZET"),
]

PAGEBREAK_P = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

_SDT_RE = re.compile(r"<w:sdt>.*?</w:sdt>", re.S)
_HEADING1_RE = re.compile(
    r'<w:p><w:pPr><w:pStyle w:val="Heading1"\s*/></w:pPr>(?P<body>.*?)</w:p>', re.S
)
_TEXT_RE = re.compile(r"<w:t[^>]*>([^<]*)</w:t>")
_HEADING_NUM_RE = re.compile(r"^\d+(?:\.\d+)*\.?\s+")
_BOOKMARK_TAIL_RE = re.compile(r"(?:\s*<w:bookmarkStart\b[^>]*/>)+\s*$")
_PAGEBREAK_RE = re.compile(r'<w:p><w:r><w:br w:type="page"\s*/></w:r></w:p>')
_BOOKMARK_RE = re.compile(r"<w:bookmark(?:Start|End)\b[^>]*/>")

# Quarto/Pandoc'un metadatadan urettigi varsayilan baslik blogu (Marmara §2.1
# kapagi bunun yerine gecer). Yalnizca govdenin en basindaki ardisik
# Title/Author/Date paragraflari silinir.
_TITLE_BLOCK_STYLES = ("Title", "Author", "Date", "Abstract", "AbstractTitle")
_BODY_RE = re.compile(r"(<w:body>)(.*)(</w:body>)", re.S)
_FIRST_P_RE = re.compile(
    r'^\s*<w:p>\s*<w:pPr>\s*<w:pStyle w:val="(?P<style>[^"]+)"\s*/>', re.S
)
_P_RE = re.compile(r"<w:p\b.*?</w:p>|<w:p\b[^>]*/>", re.S)


def _targets() -> list[str]:
    env = os.environ.get("QUARTO_PROJECT_OUTPUT_FILES", "").strip()
    if env:
        files = [f.strip() for f in env.splitlines() if f.strip()]
        return [f for f in files if f.lower().endswith(".docx")]
    return [t for t in DEFAULT_TARGETS if os.path.exists(t)]


def _find_sdt(xml: str, gallery: str) -> tuple[int, int] | None:
    """docPartGallery degeri verilen dizin blogunun (start, end) araligini dondurur."""
    needle = 'docPartGallery w:val="%s"' % gallery
    for m in _SDT_RE.finditer(xml):
        if needle in m.group(0):
            return m.start(), m.end()
    return None


def _find_heading(xml: str, text: str) -> tuple[int, int] | None:
    """Heading1 paragrafinin (anchor_start, paragraph_end) araligini dondurur.

    `anchor_start`, paragrafin hemen onundeki `<w:bookmarkStart/>` etiketlerini de
    kapsar; boylece dizin blogu yer imi ile basligin arasina girmez.

    Karsilastirma bolum numarasindan bagimsizdir: docx yazicisi
    `number-sections: true` altinda baslik metnini "1. ÖZET" olarak yazar; capa
    metni ("ÖZET") ile eslesmesi icin bastaki numara on-eki atilir.
    """
    for m in _HEADING1_RE.finditer(xml):
        raw = "".join(_TEXT_RE.findall(m.group("body"))).strip()
        if _HEADING_NUM_RE.sub("", raw) == text:
            start = m.start()
            tail = _BOOKMARK_TAIL_RE.search(xml, 0, start)
            if tail is not None and tail.end() == start:
                start = tail.start()
            return start, m.end()
    return None


def _already_placed(xml: str, sdt_end: int, anchor_start: int) -> bool:
    """Dizin blogu zaten capanin hemen onunde mi?

    Aradaki icerik yalnizca baska dizin bloklari, sayfa sonu paragraflari ve yer
    imlerinden olusuyorsa (yani gercek bir govde icerigi/baslik yoksa) blok yerinde
    kabul edilir. Ayni capaya birden fazla dizin tasindiginda (SEKILLER + TABLOLAR
    -> OZET) ikinci blok araya girdigi icin bu tolerans zorunludur; yoksa her
    koşumda yeni sayfa sonu eklenip idempotenslik bozulur.
    """
    if not 0 <= sdt_end <= anchor_start:
        return False
    between = xml[sdt_end:anchor_start]
    between = _SDT_RE.sub("", between)
    between = _PAGEBREAK_RE.sub("", between)
    between = _BOOKMARK_RE.sub("", between)
    return between.strip() == ""


def _drop_title_block(xml: str) -> tuple[str, list[str]]:
    """Govde basindaki varsayilan Title/Author baslik blogunu siler.

    Marmara §2.1 kapagi `chapters/00_kapak.qmd` icinden gelir; Pandoc'un
    metadatadan urettigi baslik blogu bu kapagin ONUNDE ayri bir sayfa olarak
    kalirdi. Yalnizca govdenin en basinda, kesintisiz duran baslik-blogu stilli
    paragraflar kaldirilir; ilk baska stildeki paragrafta durulur (idempotent).
    """
    m = _BODY_RE.search(xml)
    if m is None:
        return xml, []
    head, body, tail = m.group(1), m.group(2), m.group(3)
    dropped: list[str] = []
    while True:
        first = _FIRST_P_RE.match(body)
        if first is None or first.group("style") not in _TITLE_BLOCK_STYLES:
            break
        pm = _P_RE.search(body, first.start())
        if pm is None:
            break
        dropped.append(first.group("style"))
        body = body[: pm.start()] + body[pm.end() :]
    if not dropped:
        return xml, []
    return xml[: m.start()] + head + body + tail + xml[m.end() :], dropped


def _move_indexes(xml: str) -> tuple[str, list[str]]:
    moved: list[str] = []
    for gallery, anchor_text in INDEX_MOVES:
        span = _find_sdt(xml, gallery)
        anchor = _find_heading(xml, anchor_text)
        if span is None or anchor is None:
            continue
        if _already_placed(xml, span[1], anchor[0]):
            continue
        block = xml[span[0] : span[1]]
        xml = xml[: span[0]] + xml[span[1] :]
        anchor = _find_heading(xml, anchor_text)
        if anchor is None:  # pragma: no cover - capa silinemez
            continue
        insert = "%s\n    %s\n    " % (block, PAGEBREAK_P)
        xml = xml[: anchor[0]] + insert + xml[anchor[0] :]
        moved.append("%s -> %s" % (gallery, anchor_text))
    return xml, moved


def _patch_docx(path: str) -> list[str]:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "word/document.xml" not in names:
            return []
        data = {n: z.read(n) for n in names}

    xml = data["word/document.xml"].decode("utf-8")
    actions: list[str] = []

    xml, dropped = _drop_title_block(xml)
    actions.extend("baslik blogu silindi: %s" % d for d in dropped)

    for src, dst in REPLACEMENTS.items():
        if src in xml:
            xml = xml.replace(src, dst)
            actions.append("baslik: %s -> %s" % (src, dst))

    xml, moved = _move_indexes(xml)
    actions.extend("sira: %s" % m for m in moved)

    if not actions:
        return []

    data["word/document.xml"] = xml.encode("utf-8")
    fd, tmp = tempfile.mkstemp(suffix=".docx", dir=os.path.dirname(path) or ".")
    os.close(fd)
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for n in names:
                zout.writestr(n, data[n])
        shutil.move(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return actions


def main() -> int:
    targets = _targets()
    if not targets:
        return 0
    for t in targets:
        if not os.path.exists(t):
            continue
        actions = _patch_docx(t)
        if actions:
            print("[marmara-dizin] guncellendi: %s" % t)
            for a in actions:
                print("[marmara-dizin]   %s" % a)
        else:
            print("[marmara-dizin] degisiklik yok: %s" % t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
