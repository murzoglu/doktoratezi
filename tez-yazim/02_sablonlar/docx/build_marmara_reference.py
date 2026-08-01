#!/usr/bin/env python3
"""Marmara tez formatina uygun Pandoc reference-doc uretir.

Pandoc'un varsayilan reference.docx'ini alir ve Marmara Tez Formati
Talimatnamesi degerlerini enjekte eder:

 - §1.1 Kenar bosluklari: sol/sag 2,5 cm; ust/alt 2 cm; A4.
 - §2.1 Kapak stilleri (KapakOrta/KapakBaslik): ortalanmis TNR 12 pt; tez
   basligi kalin 14 pt.
 - §1.2 Ana metin: Times New Roman 12 pt, 1,5 satir araligi, iki yana yasli,
   girintisiz, paragraf arasi 6 nk.
 - §1.3 Basliklar: ana baslik (Heading1) bold 14 pt; diger basliklar
   (Heading2-9) bold 12 pt. Dizin basliklari (TOCHeading -> ICINDEKILER,
   SEKILLER DIZINI, TABLOLAR DIZINI) de §1.3'te "ana baslik" sayilir; bu
   nedenle Heading1'i devralir (Pandoc varsayilaninin bold-kapali/mavi/
   tema-fontlu TOCHeading tanimi kaldirilir).
 - §1.2 Dizin girdileri (TOC1-TOC9) ve kopruler siyah TNR; resmi sablonun
   TOC1 stiline (TNR bold, 11 pt, 1,5 aralik) uyar.
 - §1.6/§1.7 Sekil/tablo basliklari (Caption/ImageCaption/TableCaption):
   TNR 12 pt, tek satir araligi.

Kaynak: docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf +
        tez-yazim/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md

Not: Etiket kalinligi (§1.7 "Tablo 1." bold) reference-doc ile degil,
marmara-caption-bold.lua filtresi ile saglanir.

Kullanim (repo kokunden):
    python3 tez-yazim/02_sablonlar/docx/build_marmara_reference.py

Cikti:
    tez-yazim/02_sablonlar/docx/marmara-reference.docx
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

TNR = ('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
       'w:cs="Times New Roman"/>')

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DOCX = os.path.join(HERE, "marmara-reference.docx")


def replace_style(xml, style_id, new_ppr=None, new_rpr=None):
    """Bir stilin <w:pPr> ve/veya <w:rPr> bloklarini degistirir/ekler."""
    pat = re.compile(
        r'(<w:style [^>]*w:styleId="' + re.escape(style_id) + r'".*?</w:style>)',
        re.S)
    m = pat.search(xml)
    if not m:
        print(f"UYARI: {style_id} bulunamadi", file=sys.stderr)
        return xml
    blk = m.group(1)
    name_pat = re.compile(r'<w:name [^>]*?/>|<w:name [^>]*?>.*?</w:name>', re.S)
    if new_ppr is not None:
        if '<w:pPr>' in blk:
            blk = re.sub(r'<w:pPr>.*?</w:pPr>', new_ppr, blk, count=1, flags=re.S)
        else:
            blk = name_pat.sub(lambda mm: mm.group(0) + new_ppr, blk, count=1)
    if new_rpr is not None:
        if '<w:rPr>' in blk:
            blk = re.sub(r'<w:rPr>.*?</w:rPr>', new_rpr, blk, count=1, flags=re.S)
        else:
            if '</w:pPr>' in blk:
                blk = re.sub(r'(</w:pPr>)', r'\1' + new_rpr, blk, count=1)
            else:
                blk = name_pat.sub(lambda mm: mm.group(0) + new_rpr, blk, count=1)
    return xml[:m.start(1)] + blk + xml[m.end(1):]


def patch_styles(styles):
    # Normal: TNR 12pt, 1.5 aralik (line=360), justify, girintisiz, after=120 (6nk)
    normal_ppr = ('<w:pPr><w:spacing w:before="0" w:after="120" w:line="360" '
                  'w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>')
    normal_rpr = ('<w:rPr>' + TNR + '<w:sz w:val="24"/><w:szCs w:val="24"/>'
                  '<w:lang w:val="tr-TR"/></w:rPr>')
    styles = replace_style(styles, 'Normal', normal_ppr, normal_rpr)

    # Heading1 (ana bolum basligi): bold 14pt
    h1_ppr = ('<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" '
              'w:after="120" w:line="360" w:lineRule="auto"/>'
              '<w:outlineLvl w:val="0"/></w:pPr>')
    h1_rpr = ('<w:rPr>' + TNR + '<w:b/><w:bCs/><w:sz w:val="28"/>'
              '<w:szCs w:val="28"/><w:lang w:val="tr-TR"/></w:rPr>')
    styles = replace_style(styles, 'Heading1', h1_ppr, h1_rpr)

    # Heading2-9: bold 12pt
    for hid, lvl in [('Heading2', 1), ('Heading3', 2), ('Heading4', 3),
                     ('Heading5', 4), ('Heading6', 5), ('Heading7', 6),
                     ('Heading8', 7), ('Heading9', 8)]:
        hppr = ('<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="120" '
                'w:after="120" w:line="360" w:lineRule="auto"/>'
                '<w:outlineLvl w:val="' + str(lvl) + '"/></w:pPr>')
        hrpr = ('<w:rPr>' + TNR + '<w:b/><w:bCs/><w:sz w:val="24"/>'
                '<w:szCs w:val="24"/><w:lang w:val="tr-TR"/></w:rPr>')
        styles = replace_style(styles, hid, hppr, hrpr)

    # Caption / ImageCaption / TableCaption: TNR 12pt, tek satir araligi
    cap_ppr = ('<w:pPr><w:spacing w:before="120" w:after="120" w:line="240" '
               'w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>')
    cap_rpr = ('<w:rPr>' + TNR + '<w:sz w:val="24"/><w:szCs w:val="24"/>'
               '<w:lang w:val="tr-TR"/></w:rPr>')
    for cid in ['Caption', 'ImageCaption', 'TableCaption']:
        styles = replace_style(styles, cid, cap_ppr, cap_rpr)

    # Title / Subtitle / Author: TNR
    for tid, sz in [('Title', '36'), ('Subtitle', '28'), ('Author', '24')]:
        trpr = ('<w:rPr>' + TNR + '<w:b/><w:sz w:val="' + sz + '"/>'
                '<w:szCs w:val="' + sz + '"/><w:lang w:val="tr-TR"/></w:rPr>')
        styles = replace_style(styles, tid, None, trpr)

    # docDefaults: varsayilan font -> TNR 12pt
    styles = re.sub(
        r'<w:rPrDefault>.*?</w:rPrDefault>',
        '<w:rPrDefault><w:rPr>' + TNR + '<w:sz w:val="24"/><w:szCs w:val="24"/>'
        '<w:lang w:val="tr-TR" w:eastAsia="tr-TR" w:bidi="ar-SA"/>'
        '</w:rPr></w:rPrDefault>',
        styles, count=1, flags=re.S)

    # §1.2/§1.3 dizin katmani (TOCHeading + TOC1-9 + kopru rengi)
    styles = patch_toc_styles(styles)
    # §2.1 kapak katmani (Kapak Orta / Kapak Baslik)
    styles = patch_cover_styles(styles)
    return styles


def patch_cover_styles(styles):
    """§2.1 kapak stilleri: ortalanmis, tek aralikli, girintisiz TNR.

    Kapak (`chapters/00_kapak.qmd`) DOCX kolunda `custom-style` div'leriyle
    yazilir; Pandoc stili reference-doc'taki `<w:name>` degerine gore eslestirir.
    Kapaktaki tum yazilar 12 punto, tez basligi kalin 14 puntodur.
    """
    base_ppr = ('<w:pPr><w:spacing w:before="0" w:after="0" w:line="240" '
                'w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>')
    styles = add_style(styles,
                       '<w:style w:type="paragraph" w:styleId="KapakOrta">'
                       '<w:name w:val="Kapak Orta"/>'
                       '<w:basedOn w:val="Normal"/><w:qFormat/>'
                       + base_ppr +
                       '<w:rPr>' + TNR + '<w:sz w:val="24"/><w:szCs w:val="24"/>'
                       '<w:lang w:val="tr-TR"/></w:rPr></w:style>')
    styles = add_style(styles,
                       '<w:style w:type="paragraph" w:styleId="KapakBaslik">'
                       '<w:name w:val="Kapak Baslik"/>'
                       '<w:basedOn w:val="KapakOrta"/><w:qFormat/>'
                       + base_ppr +
                       '<w:rPr>' + TNR + '<w:b/><w:bCs/><w:sz w:val="28"/>'
                       '<w:szCs w:val="28"/><w:lang w:val="tr-TR"/></w:rPr>'
                       '</w:style>')
    return styles


def add_style(xml, style_xml):
    """Var olmayan bir stili styles.xml sonuna ekler (varsa dokunmaz)."""
    sid = re.search(r'w:styleId="([^"]+)"', style_xml).group(1)
    if 'w:styleId="' + sid + '"' in xml:
        return xml
    return xml.replace('</w:styles>', style_xml + '</w:styles>', 1)


# Metin genisligi (twip): A4 11906 - sol 1417 - sag 1417 = 9072.
# Dizin girdilerinde sayfa numarasi bu konumdaki nokta-onculu sag sekmeye yaslanir.
TOC_TAB = ('<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9072"/></w:tabs>')


def patch_toc_styles(styles):
    """§1.2/§1.3: dizin basliklari ve girdileri siyah TNR, ana baslik bold 14 pt.

    Pandoc varsayilani TOCHeading'i Heading1'den turetir ama bold'u kapatir
    (`<w:b w:val="0"/>`), tema fontuna (majorHAnsi) ve mavi renge (365F91)
    cevirir. Marmara §1.3 icindekiler/sekiller/tablolar dizinlerini "ana
    baslik" sayar (kalin, 14 punto) ve §1.2 ana metni siyah TNR ister; ayrica
    PDF hatti zaten `linkcolor/urlcolor/citecolor/toccolor: black` ile tamamen
    siyahtir. Bu nedenle override kaldirilir ve stil Heading1'i devralir.
    `outlineLvl 9` korunur; aksi halde dizin basliklari kendi dizinlerine
    girdi olarak dusen bir dongu olustururdu.
    """
    toch_ppr = ('<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" '
                'w:after="120" w:line="360" w:lineRule="auto"/>'
                '<w:outlineLvl w:val="9"/></w:pPr>')
    toch_rpr = '<w:rPr><w:lang w:val="tr-TR"/></w:rPr>'
    styles = replace_style(styles, 'TOCHeading', toch_ppr, toch_rpr)

    # TOC1-TOC9: Pandoc varsayilan reference.docx'inde tanimli degildir; alan
    # (field) guncellenince Word kendi yerlesik mavi/tema varsayilanlarini
    # uretir. Resmi Marmara sablonunun TOC1 stili (TNR, bold, 11 pt, 1,5
    # aralik) esas alinarak acikca tanimlanir.
    styles = add_style(styles,
                       '<w:style w:type="paragraph" w:styleId="TOC1">'
                       '<w:name w:val="toc 1"/><w:basedOn w:val="Normal"/>'
                       '<w:next w:val="Normal"/><w:uiPriority w:val="39"/>'
                       '<w:pPr>' + TOC_TAB +
                       '<w:spacing w:before="0" w:after="0" w:line="360" '
                       'w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
                       '<w:rPr>' + TNR + '<w:b/><w:bCs/><w:sz w:val="22"/>'
                       '<w:szCs w:val="22"/><w:lang w:val="tr-TR"/></w:rPr>'
                       '</w:style>')
    for lvl in range(2, 10):
        indent = 220 * (lvl - 1)
        styles = add_style(
            styles,
            '<w:style w:type="paragraph" w:styleId="TOC' + str(lvl) + '">'
            '<w:name w:val="toc ' + str(lvl) + '"/>'
            '<w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'
            '<w:uiPriority w:val="39"/>'
            '<w:pPr>' + TOC_TAB +
            '<w:spacing w:before="0" w:after="0" w:line="276" '
            'w:lineRule="auto"/><w:ind w:left="' + str(indent) + '"/>'
            '<w:jc w:val="left"/></w:pPr>'
            '<w:rPr>' + TNR + '<w:sz w:val="22"/><w:szCs w:val="22"/>'
            '<w:lang w:val="tr-TR"/></w:rPr></w:style>')

    # ŞEKİLLER/TABLOLAR DİZİNİ girdileri: Pandoc bu iki alani
    # `TOC \h \z \t "Image Caption" \c` biciminde uretir; `\c` anahtari alani
    # Word'de "table of figures" yapar, dolayisiyla girdiler TOC1 degil
    # `TableofFigures` stilini alir. §2.6/§2.7 yalniz etiketi ("Şekil 1.",
    # "Tablo 1.") kalin ister — o kalinlik caption'in kendi dogrudan bicimi
    # olarak (marmara-caption-bold.lua) tasinir; stil bu yuzden kalin DEGILDIR.
    styles = add_style(styles,
                       '<w:style w:type="paragraph" w:styleId="TableofFigures">'
                       '<w:name w:val="table of figures"/>'
                       '<w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'
                       '<w:uiPriority w:val="99"/>'
                       '<w:pPr>' + TOC_TAB +
                       '<w:spacing w:before="0" w:after="0" w:line="276" '
                       'w:lineRule="auto"/><w:ind w:left="567" w:hanging="567"/>'
                       '<w:jc w:val="left"/></w:pPr>'
                       '<w:rPr>' + TNR + '<w:sz w:val="22"/><w:szCs w:val="22"/>'
                       '<w:lang w:val="tr-TR"/></w:rPr></w:style>')

    # §1.2 "Ana metin siyah renkte": dizin girdileri TOC alaninin \h anahtariyla
    # koprulendigi icin Hyperlink karakter stilini devralir. Pandoc varsayilani
    # mavidir (4F81BD) -> tum dizin mavi cikar. PDF hattiyla parite icin siyah.
    styles = replace_style(styles, 'Hyperlink', None,
                           '<w:rPr><w:color w:val="000000"/></w:rPr>')
    styles = add_style(styles,
                       '<w:style w:type="character" w:styleId="FollowedHyperlink">'
                       '<w:name w:val="FollowedHyperlink"/>'
                       '<w:basedOn w:val="DefaultParagraphFont"/>'
                       '<w:uiPriority w:val="99"/>'
                       '<w:rPr><w:color w:val="000000"/></w:rPr></w:style>')
    return styles


def patch_document(doc):
    # A4 + kenar bosluklari (twips: 1cm=567). sol/sag 2,5cm=1417; ust/alt 2cm=1134.
    pgsz = '<w:pgSz w:w="11906" w:h="16838"/>'
    pgmar = ('<w:pgMar w:top="1134" w:right="1417" w:bottom="1134" '
             'w:left="1417" w:header="708" w:footer="708" w:gutter="0"/>')
    if '<w:pgSz' not in doc:
        doc = doc.replace('</w:sectPr>', pgsz + pgmar + '</w:sectPr>', 1)
    else:
        doc = re.sub(r'<w:pgSz[^>]*>', pgsz, doc, count=1)
        doc = re.sub(r'<w:pgMar[^>]*>', pgmar, doc, count=1)
    return doc


def main():
    tmp = tempfile.mkdtemp(prefix="marmara_ref_")
    try:
        base = os.path.join(tmp, "reference.docx")
        # Pandoc'un varsayilan reference.docx'ini al
        with open(base, "wb") as fh:
            subprocess.run(
                ["quarto", "pandoc", "--print-default-data-file", "reference.docx"],
                check=True, stdout=fh)
        # Ac
        ext = os.path.join(tmp, "ext")
        with zipfile.ZipFile(base) as z:
            z.extractall(ext)
        # Yamala
        sp = os.path.join(ext, "word", "styles.xml")
        dp = os.path.join(ext, "word", "document.xml")
        with open(sp, encoding="utf-8") as fh:
            styles = fh.read()
        with open(dp, encoding="utf-8") as fh:
            doc = fh.read()
        with open(sp, "w", encoding="utf-8") as fh:
            fh.write(patch_styles(styles))
        with open(dp, "w", encoding="utf-8") as fh:
            fh.write(patch_document(doc))
        # Yeniden paketle ([Content_Types].xml once)
        if os.path.exists(OUT_DOCX):
            os.remove(OUT_DOCX)
        with zipfile.ZipFile(OUT_DOCX, "w", zipfile.ZIP_DEFLATED) as z:
            ct = os.path.join(ext, "[Content_Types].xml")
            z.write(ct, "[Content_Types].xml")
            for root, _dirs, files in os.walk(ext):
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, ext)
                    if rel == "[Content_Types].xml":
                        continue
                    z.write(full, rel)
        print("Uretildi:", OUT_DOCX)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
