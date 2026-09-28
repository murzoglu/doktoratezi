#!/usr/bin/env python3
"""Render sonrasi docx kapak/dizin yerlesimini Marmara duzenine cevirir.

Dort is yapar:

0. **Varsayilan baslik blogu.** Quarto/Pandoc, `title`/`author` metadatasindan
   belgenin en basina `Title` ve `Author` stilli iki paragraf yazar. Marmara
   §2.1 kapagi (`chapters/00_kapak.qmd`) bunun yerine gectiginden bu iki
   paragraf silinir; metadata PDF/DOCX belge ozelliklerinde korunur.

1. **Sekil/tablo stilleri.** Quarto DOCX yazicisi hem sekil hem tablo basliklarini
   `ImageCaption` stiliyle yazar. Tablo basliklari `TableCaption` stiline ayrilir;
   boylece iki ayri Word dizin alani dogru kapsami izleyebilir.

2. **Dizin alanlari ve basliklari.** Quarto, `lof: true` / `lot: true` ayarina
   ragmen bu projedeki DOCX ciktisina sekil/tablo dizin alanlarini eklemiyor.
   Betik, baslik stillerini kullanan guncellenebilir Word `TOC` alanlarini ve
   Marmara §5'in istedigi "ŞEKİLLER DİZİNİ" / "TABLOLAR DİZİNİ" basliklarini
   ekler. Word acildiginda alanlar otomatik guncellenecek sekilde isaretlenir.

3. **Dizin sirasi.** Pandoc'un urettigi ICINDEKILER ve varsa SEKILLER/TABLOLAR
   dizinleri belgenin en basinda kalabilir. Marmara §5 resmi sirasi ise:

       Tez onayi -> Beyan -> Tesekkur -> ICINDEKILER -> KISALTMALAR
       -> SEKILLER -> TABLOLAR -> Ozet -> Summary

   Betik mevcut `<w:sdt>` dizin bloglarini ve ekledigi alanlari dogru capa
   basliginin (`KISALTMALAR`, `ÖZET`) hemen onune, arkasina sayfa sonu paragrafi
   ekleyerek tasir. PDF hattinda ayni sira on sayfa bolumlerindeki ham LaTeX
   (tableofcontents, listoffigures, listoftables) ile saglanir.

4. **Sayfa ve sekil akisi.** DOCX yazicisi kimi referans-dosya surumlerinde
   bos bir `sectPr` uretebilir; bu durumda Word belgeyi Letter boyutunda acar.
   Betik A4 ve Marmara kenar bosluklarini cikti belgesinde acikca tanimlar.
   Satir ici sekiller ortalanir ve basliklariyla ayni sayfada tutulur; metin,
   tablo ve sekil basliklarinin stili Marmara yerlesimine gore ayarlanir.

Idempotenttir: baslik blogu zaten silinmisse, stiller ayrilmissa ve dizin alanlari
zaten mevcutsa dosyaya dokunmaz.
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

FIGURE_INDEX = ("ŞEKİLLER DİZİNİ", "Image Caption")
TABLE_INDEX = ("TABLOLAR DİZİNİ", "Table Caption")
TOC_ENTRY_STYLES = tuple("TOC%d" % level for level in range(1, 10)) + (
    "TableofFigures",
)
TOC_TAB_NO_LEADER = '<w:tabs><w:tab w:val="right" w:pos="9072"/></w:tabs>'

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
_P_RE = re.compile(r"<w:p\b[^>]*/>|<w:p\b.*?</w:p>", re.S)
_TABLE_CAPTION_RE = re.compile(r"^\s*Tablo(?:\s|\u00a0)+\d+\.")
_PPR_RE = re.compile(r"<w:pPr>(?P<body>.*?)</w:pPr>", re.S)
_PPR_SELF_RE = re.compile(r"<w:pPr\s*/>")
_PSTYLE_RE = re.compile(r'<w:pStyle\b[^>]*w:val="(?P<style>[^"]+)"[^>]*/>')
_SECT_PR_RE = re.compile(
    r"<w:sectPr\b[^>]*?/>|<w:sectPr\b[^>]*>.*?</w:sectPr>", re.S
)
_PGSZ_RE = re.compile(r"<w:pgSz\b[^>]*/>")
_PGMAR_RE = re.compile(r"<w:pgMar\b[^>]*/>")

_A4_PAGE_SIZE = '<w:pgSz w:w="11906" w:h="16838"/>'
_A4_PAGE_MARGINS = (
    '<w:pgMar w:top="1134" w:right="1417" w:bottom="1134" '
    'w:left="1417" w:header="708" w:footer="708" w:gutter="0"/>'
)


def _paragraph_text(paragraph: str) -> str:
    return "".join(_TEXT_RE.findall(paragraph)).replace("\u00a0", " ").strip()


def _paragraph_style(paragraph: str) -> str | None:
    match = _PSTYLE_RE.search(paragraph)
    return match.group("style") if match is not None else None


def _set_paragraph_layout(
    paragraph: str,
    *,
    alignment: str | None = None,
    keep_next: bool = False,
    spacing: str | None = None,
    page_break_before: bool = False,
) -> str:
    """Paragrafin dogrudan yerlesim ayarlarini, metnine dokunmadan uygular."""
    match = _PPR_RE.search(paragraph)
    if match is not None:
        ppr = match.group(0)
        body = match.group("body")
        replace_start, replace_end = match.span()
    else:
        self_closing = _PPR_SELF_RE.search(paragraph)
        if self_closing is not None:
            ppr = self_closing.group(0)
            body = ""
            replace_start, replace_end = self_closing.span()
        else:
            opening = re.search(r"<w:p\b[^>]*>", paragraph)
            if opening is None:
                return paragraph
            body = ""
            ppr = "<w:pPr></w:pPr>"
            replace_start = replace_end = opening.end()

    updated = body
    if keep_next:
        if "<w:keepNext" not in updated:
            updated += "<w:keepNext/>"
        if "<w:keepLines" not in updated:
            updated += "<w:keepLines/>"
    if alignment is not None:
        replacement = '<w:jc w:val="%s"/>' % alignment
        if re.search(r"<w:jc\b[^>]*/>", updated):
            updated = re.sub(r"<w:jc\b[^>]*/>", replacement, updated, count=1)
        else:
            updated += replacement
    if spacing is not None:
        if re.search(r"<w:spacing\b[^>]*/>", updated):
            updated = re.sub(r"<w:spacing\b[^>]*/>", spacing, updated, count=1)
        else:
            updated += spacing
    if page_break_before and "<w:pageBreakBefore" not in updated:
        updated += "<w:pageBreakBefore/>"

    new_ppr = "<w:pPr>%s</w:pPr>" % updated
    if new_ppr == ppr:
        return paragraph
    return paragraph[:replace_start] + new_ppr + paragraph[replace_end:]


def _replace_style_ppr(styles_xml: str, style_id: str, ppr: str) -> tuple[str, bool]:
    """Bir paragraf stilinin yerlesim ayarini idempotent olarak yeniler."""
    pattern = re.compile(
        r'(<w:style\b[^>]*w:styleId="%s"[^>]*>.*?</w:style>)'
        % re.escape(style_id),
        re.S,
    )
    match = pattern.search(styles_xml)
    if match is None:
        return styles_xml, False

    block = match.group(1)
    if _PPR_RE.search(block):
        updated = _PPR_RE.sub(ppr, block, count=1)
    elif _PPR_SELF_RE.search(block):
        updated = _PPR_SELF_RE.sub(ppr, block, count=1)
    else:
        name = re.search(r"<w:name\b[^>]*/>", block)
        if name is None:
            return styles_xml, False
        updated = block[: name.end()] + ppr + block[name.end() :]

    if updated == block:
        return styles_xml, False
    return styles_xml[: match.start(1)] + updated + styles_xml[match.end(1) :], True


def _apply_marmara_layout_styles(styles_xml: str) -> tuple[str, list[str]]:
    """Ana metin ile sekil/tablo basliklarinin Word stilini duzenler."""
    specs = {
        "Normal": (
            '<w:pPr><w:widowControl/><w:spacing w:before="0" w:after="120" '
            'w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
        ),
        "ImageCaption": (
            '<w:pPr><w:keepLines/><w:widowControl/><w:spacing w:before="240" '
            'w:after="120" w:line="240" w:lineRule="auto"/>'
            '<w:jc w:val="left"/></w:pPr>'
        ),
        "TableCaption": (
            '<w:pPr><w:keepNext/><w:keepLines/><w:widowControl/>'
            '<w:spacing w:before="240" w:after="120" w:line="240" '
            'w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
        ),
    }
    actions: list[str] = []
    for style_id, ppr in specs.items():
        styles_xml, changed = _replace_style_ppr(styles_xml, style_id, ppr)
        if changed:
            actions.append("stil yerlesimi: %s" % style_id)
    return styles_xml, actions


def _apply_marmara_toc_leader_styles(styles_xml: str) -> tuple[str, list[str]]:
    """Dizin girdilerinde sayfa numarası sekmesini noktasız/lidersiz yapar."""
    actions: list[str] = []
    for style_id in TOC_ENTRY_STYLES:
        pattern = re.compile(
            r'(<w:style\b[^>]*w:styleId="%s"[^>]*>.*?</w:style>)'
            % re.escape(style_id),
            re.S,
        )
        match = pattern.search(styles_xml)
        if match is None:
            continue
        block = match.group(1)
        ppr_match = _PPR_RE.search(block)
        if ppr_match is None:
            continue

        ppr = ppr_match.group(0)
        updated = re.sub(r"<w:tabs>.*?</w:tabs>", TOC_TAB_NO_LEADER, ppr, flags=re.S)
        if updated == ppr:
            updated = updated.replace("<w:pPr>", "<w:pPr>" + TOC_TAB_NO_LEADER, 1)
        updated = re.sub(r'\s+w:leader="[^"]+"', "", updated)

        if updated == ppr:
            continue
        block = block[: ppr_match.start()] + updated + block[ppr_match.end() :]
        styles_xml = (
            styles_xml[: match.start(1)] + block + styles_xml[match.end(1) :]
        )
        actions.append("dizin nokta lideri kaldirildi: %s" % style_id)
    return styles_xml, actions


def _enforce_page_geometry(xml: str) -> tuple[str, bool]:
    """DOCX bolum tanimina A4 ve Marmara kenar bosluklarini yazar."""

    def replace(match: re.Match[str]) -> str:
        section = match.group(0)
        if section.rstrip().endswith("/>"):
            return "<w:sectPr>%s%s</w:sectPr>" % (
                _A4_PAGE_SIZE,
                _A4_PAGE_MARGINS,
            )
        opening = re.match(r"<w:sectPr\b[^>]*>", section)
        if opening is None:
            return section
        body = section[opening.end() : -len("</w:sectPr>")]
        body = _PGSZ_RE.sub("", body)
        body = _PGMAR_RE.sub("", body)
        return "%s%s%s%s</w:sectPr>" % (
            opening.group(0),
            _A4_PAGE_SIZE,
            _A4_PAGE_MARGINS,
            body,
        )

    updated = _SECT_PR_RE.sub(replace, xml)
    return updated, updated != xml


def _polish_inline_figures(xml: str) -> tuple[str, int, int]:
    """Sekilleri ortalar; sekil ve basligini ayni sayfada tutar."""
    matches = list(_P_RE.finditer(xml))
    parts: list[str] = []
    cursor = 0
    centered = 0
    bound = 0

    for index, match in enumerate(matches):
        paragraph = match.group(0)
        updated = paragraph
        if "<wp:inline" in paragraph:
            next_style = None
            for following in matches[index + 1 : index + 7]:
                candidate = following.group(0)
                if _paragraph_text(candidate):
                    next_style = _paragraph_style(candidate)
                    break
            bind_caption = next_style == "ImageCaption"
            updated = _set_paragraph_layout(
                paragraph,
                alignment="center",
                keep_next=bind_caption,
            )
            if updated != paragraph:
                centered += 1
                if bind_caption:
                    bound += 1
        parts.append(xml[cursor : match.start()])
        parts.append(updated)
        cursor = match.end()
    parts.append(xml[cursor:])
    return "".join(parts), centered, bound


def _compact_cover_spacers(xml: str) -> tuple[str, int]:
    """DOCX kapaklarindaki bos satirlari PDF kapak oranina gore duzenler."""
    matches = list(_P_RE.finditer(xml))
    cover_styles = {"KapakOrta", "KapakBaslik"}
    spacer_runs: list[list[int]] = []
    current_run: list[int] = []
    in_cover = False

    for index, match in enumerate(matches):
        paragraph = match.group(0)
        if 'w:type="page"' in paragraph:
            current_run = []
            in_cover = False
            continue
        style = _paragraph_style(paragraph)
        if style in cover_styles and (
            _paragraph_text(paragraph) or "<wp:inline" in paragraph
        ):
            if current_run:
                spacer_runs.append(current_run)
                current_run = []
            in_cover = True
            continue
        if not in_cover:
            continue
        if (
            not _paragraph_text(paragraph)
            and "<wp:inline" not in paragraph
            and "<w:br" not in paragraph
        ):
            current_run.append(index)
        else:
            current_run = []

    # Dört bosluk blogu sirasiyla kurum-baslik, baslik-ogrenci,
    # ogrenci-danisman ve danisman-sehir/yil aralarindadir.
    retained = (1, 3, 3, 6)
    removals: set[int] = set()
    for index, run in enumerate(spacer_runs):
        limit = retained[index % len(retained)]
        removals.update(run[limit:])

    if not removals:
        return xml, 0
    parts: list[str] = []
    cursor = 0
    for index, match in enumerate(matches):
        parts.append(xml[cursor : match.start()])
        if index not in removals:
            parts.append(match.group(0))
        cursor = match.end()
    parts.append(xml[cursor:])
    return "".join(parts), len(removals)


def _compact_summary_sections(xml: str) -> tuple[str, int, int]:
    """Ozet/Summary metnini icerigi degistirmeden tek sayfaya sigdirir."""
    matches = list(_P_RE.finditer(xml))
    parts: list[str] = []
    cursor = 0
    section: str | None = None
    compacted = 0
    page_breaks = 0

    for match in matches:
        paragraph = match.group(0)
        heading = _HEADING_NUM_RE.sub("", _paragraph_text(paragraph))
        style = _paragraph_style(paragraph)
        updated = paragraph
        if style == "Heading1":
            if heading == "ÖZET":
                section = "tr"
            elif heading == "SUMMARY":
                section = "en"
            elif heading == "GİRİŞ ve AMAÇ":
                section = None
                updated = _set_paragraph_layout(
                    paragraph,
                    page_break_before=True,
                )
                if updated != paragraph:
                    page_breaks += 1
            elif section is not None:
                section = None
        elif section is not None and (_paragraph_text(paragraph) or "<wp:inline" in paragraph):
            line = "276" if section == "tr" else "264"
            updated = _set_paragraph_layout(
                paragraph,
                spacing=(
                    '<w:spacing w:before="0" w:after="0" w:line="%s" '
                    'w:lineRule="auto"/>' % line
                ),
            )
            if updated != paragraph:
                compacted += 1

        parts.append(xml[cursor : match.start()])
        parts.append(updated)
        cursor = match.end()
    parts.append(xml[cursor:])
    return "".join(parts), compacted, page_breaks


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


def _split_caption_styles(xml: str) -> tuple[str, int]:
    """Tablo basliklarini sekil basligi stilinden ayirir."""
    tables = 0

    def replace(paragraph_match: re.Match[str]) -> str:
        nonlocal tables
        paragraph = paragraph_match.group(0)
        if 'w:pStyle w:val="ImageCaption"' not in paragraph:
            return paragraph
        if not _TABLE_CAPTION_RE.match(_paragraph_text(paragraph)):
            return paragraph
        tables += 1
        return paragraph.replace(
            'w:pStyle w:val="ImageCaption"',
            'w:pStyle w:val="TableCaption"',
            1,
        )

    return _P_RE.sub(replace, xml), tables


def _add_table_caption_style(styles_xml: str) -> tuple[str, bool]:
    """`TableCaption` stilini mevcut sekil basligi stilinden turetir."""
    if 'w:styleId="TableCaption"' in styles_xml:
        return styles_xml, False

    image_style = re.search(
        r'<w:style\b[^>]*w:styleId="ImageCaption"[^>]*>.*?</w:style>',
        styles_xml,
        re.S,
    )
    if image_style is None:
        return styles_xml, False

    table_style = image_style.group(0).replace(
        'w:styleId="ImageCaption"', 'w:styleId="TableCaption"', 1
    )
    table_style = table_style.replace(
        'w:name w:val="Image Caption"', 'w:name w:val="Table Caption"', 1
    )
    styles_xml = styles_xml.replace(
        "</w:styles>", "\n  %s\n</w:styles>" % table_style, 1
    )
    return styles_xml, True


def _caption_index_block(title: str, caption_style: str) -> str:
    """Belirtilen paragraf stili icin Word TOC alanli dizin blogu kurar."""
    instruction = 'TOC \\h \\z \\t "%s,1"' % caption_style
    return (
        '<w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr>'
        '<w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % title
        + '<w:p><w:pPr><w:pStyle w:val="TableofFigures"/></w:pPr>'
        '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
        '<w:r><w:instrText xml:space="preserve">%s</w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>' % instruction
    )


def _has_caption_index(xml: str, caption_style: str) -> bool:
    return 'TOC \\h \\z \\t "%s,1"' % caption_style in xml


def _insert_caption_indexes(xml: str) -> tuple[str, list[str]]:
    """Eksik sekil/tablo dizinlerini Ozet'in hemen onune yerlestirir."""
    indexes: list[tuple[str, str]] = []
    native_galleries = {
        "Image Caption": _find_sdt(xml, "List of Figures") is not None,
        "Table Caption": _find_sdt(xml, "List of Tables") is not None,
    }
    for title, caption_style in (FIGURE_INDEX, TABLE_INDEX):
        if native_galleries[caption_style] or _has_caption_index(xml, caption_style):
            continue
        indexes.append((title, caption_style))

    if not indexes:
        return xml, []

    anchor = _find_heading(xml, "ÖZET")
    if anchor is None:
        return xml, []
    insert = "\n    ".join(
        "%s\n    %s" % (_caption_index_block(title, style), PAGEBREAK_P)
        for title, style in indexes
    )
    xml = xml[: anchor[0]] + insert + "\n    " + xml[anchor[0] :]
    return xml, ["dizin alani eklendi: %s" % title for title, _ in indexes]


def _enable_field_updates(settings_xml: str) -> tuple[str, bool]:
    """Word'un acilista TOC alanlarini guncellemesini saglar."""
    if 'w:updateFields w:val="true"' in settings_xml:
        return settings_xml, False
    if "</w:settings>" not in settings_xml:
        return settings_xml, False
    return settings_xml.replace(
        "</w:settings>", '<w:updateFields w:val="true"/></w:settings>', 1
    ), True


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
    styles_xml = data.get("word/styles.xml", b"").decode("utf-8")
    settings_xml = data.get("word/settings.xml", b"").decode("utf-8")
    actions: list[str] = []

    xml, dropped = _drop_title_block(xml)
    actions.extend("baslik blogu silindi: %s" % d for d in dropped)

    xml, geometry_changed = _enforce_page_geometry(xml)
    if geometry_changed:
        actions.append("sayfa duzeni: A4 ve Marmara kenar bosluklari")

    for src, dst in REPLACEMENTS.items():
        if src in xml:
            xml = xml.replace(src, dst)
            actions.append("baslik: %s -> %s" % (src, dst))

    xml, moved = _move_indexes(xml)
    actions.extend("sira: %s" % m for m in moved)

    xml, table_count = _split_caption_styles(xml)
    if table_count:
        actions.append("tablo baslik stili ayrildi: %d" % table_count)

    styles_xml, style_added = _add_table_caption_style(styles_xml)
    if style_added:
        actions.append("stil eklendi: TableCaption")

    styles_xml, layout_actions = _apply_marmara_layout_styles(styles_xml)
    actions.extend(layout_actions)

    styles_xml, toc_leader_actions = _apply_marmara_toc_leader_styles(styles_xml)
    actions.extend(toc_leader_actions)

    xml, index_actions = _insert_caption_indexes(xml)
    actions.extend(index_actions)

    xml, centered, bound = _polish_inline_figures(xml)
    if centered:
        actions.append("sekil yerlesimi: %d ortalandi" % centered)
    if bound:
        actions.append("sekil-baslik baglantisi: %d" % bound)

    xml, compacted = _compact_cover_spacers(xml)
    if compacted:
        actions.append("kapak bosluklari: %d satir duzenlendi" % compacted)

    xml, summary_compacted, summary_breaks = _compact_summary_sections(xml)
    if summary_compacted:
        actions.append("ozet yerlesimi: %d paragraf duzenlendi" % summary_compacted)
    if summary_breaks:
        actions.append("ana bolum sayfa sonu: %d" % summary_breaks)

    settings_xml, updates_enabled = _enable_field_updates(settings_xml)
    if updates_enabled:
        actions.append("Word alan guncellemesi etkinlestirildi")

    if not actions:
        return []

    data["word/document.xml"] = xml.encode("utf-8")
    if styles_xml:
        data["word/styles.xml"] = styles_xml.encode("utf-8")
    if settings_xml:
        data["word/settings.xml"] = settings_xml.encode("utf-8")
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
