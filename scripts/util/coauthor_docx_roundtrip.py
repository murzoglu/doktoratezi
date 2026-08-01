#!/usr/bin/env python3
"""Ortak yazar DOCX round-trip: repo erisimi olmayan ortak yazardan online
(Word Online / Google Docs "Degisiklikleri Izle") duzeltme almak ve nesir
duzeltmelerini .qmd bolumlerine guvenli sekilde geri tasimak icin yardimci.

Neden bu akis: Ortak yazar Roche GitHub'inda; repoya erisim veremiyoruz. Tek
gercekci kanal, `quarto render` ile uretilen .docx'i paylasip Word/Google
Docs'ta "Track Changes" ile duzelttirmek. Bu betik iki yonu yonetir:

  export  -> Ortak yazara gidecek docx'i hazirlar (mevcut render ciktisini
             kopyalar; istege bagli tarih damgali ad). Ortak yazar tarayicidan
             acar, Degisiklikleri Izle acik sekilde duzeltir, geri gonderir.

  import  -> Donen docx'ten TUM izlenen degisiklikleri (insertion/deletion) ve
             yorumlari cikarir; her degisikligi baglam metniyle birlikte hangi
             chapters/*.qmd dosyasi + satirina denk geldigini fuzzy eslesmeyle
             ONERIR. Otomatik yazMAZ; insan onayina bir rapor (markdown + json)
             uretir.

Neden otomatik yaz-geri yok: DOCX, Quarto kod chunk'larini, capraz referanslari
(@sek-..., @tbl-...) ve ::: div'lerini kaybeder. Korlemesine geri yazmak bu
yapilari bozar ve sayisal-butunluk kaidesini ihlal edebilir. Bu nedenle betik
"neyi nerede degistir" onerir; nesir duzeltmesini insan/ajan uygular. Boylece
"sayi/tablo/figur dokunulmaz, yalniz nesir duzeltilir" ilkesi korunur.

Bagimlilik: yalniz `pandoc` (3.x) ve Python 3 standart kutuphanesi. python-docx
GEREKMEZ; docx yorumlari dogrudan zip/XML'den okunur.

Kullanim:
  # 1) Ortak yazara gidecek dosyayi hazirla
  python3 scripts/util/coauthor_docx_roundtrip.py export \
      --render outputs/quarto/thesis.docx \
      --out outbox/thesis_ortak-yazar_2026-07-30.docx

  # 2) Donen dosyayi coz (rapor + json uret)
  python3 scripts/util/coauthor_docx_roundtrip.py import \
      --edited inbox/thesis_ortak-yazar_donus.docx \
      --report outputs/coauthor/roundtrip_rapor.md \
      --json   outputs/coauthor/roundtrip_degisiklikler.json

Cikis kodu: import'ta degisiklik/yorum bulunursa 0; parse hatasi olursa 1.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field, asdict
from datetime import date

# --- Sabitler -------------------------------------------------------------

CHAPTERS_DIR = "chapters"
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# Fuzzy eslesme icin: baglamdan bu kadar karakter cikarip .qmd icinde arariz
CONTEXT_CHARS = 60
# difflib benzerlik esigi (0-1); altinda "dusuk guven" isaretlenir
MATCH_THRESHOLD = 0.55


# --- Yardimcilar ----------------------------------------------------------

def _run_pandoc(args: list[str]) -> str:
    """pandoc'u calistir, stdout'u dondur."""
    try:
        res = subprocess.run(
            ["pandoc", *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        sys.exit("HATA: pandoc bulunamadi. Ortamda pandoc 3.x gerekli.")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"HATA: pandoc basarisiz:\n{exc.stderr}")
    return res.stdout


def _norm(text: str) -> str:
    """Bosluk normalize et (fuzzy eslesme icin)."""
    return re.sub(r"\s+", " ", text).strip()


# --- EXPORT ---------------------------------------------------------------

def cmd_export(args: argparse.Namespace) -> int:
    src = args.render
    if not os.path.isfile(src):
        sys.exit(
            f"HATA: render ciktisi yok: {src}\n"
            f"Once `quarto render thesis.qmd` calistir."
        )
    out = args.out
    if out is None:
        stamp = date.today().isoformat()
        os.makedirs("outbox", exist_ok=True)
        out = f"outbox/thesis_ortak-yazar_{stamp}.docx"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    shutil.copy2(src, out)
    print(f"[export] Ortak yazara gidecek dosya hazir: {out}")
    print(
        "\nOrtak yazara ilet:\n"
        "  1. Dosyayi Word Online veya Google Docs'ta ac.\n"
        "  2. Duzenle > 'Degisiklikleri Izle' (Track Changes) ACIK olsun.\n"
        "  3. Yalniz METIN/NESIR duzelt; tablo icindeki sayilara, sekillere\n"
        "     ve numaralara dokunma (bunlar analiz kodundan uretiliyor).\n"
        "  4. Bitince .docx olarak indirip sana geri gonder.\n"
    )
    return 0


# --- IMPORT: izlenen degisiklikler (pandoc) -------------------------------

# pandoc --track-changes=all ciktisi soyle span'ler uretir:
#   [silinen]{.deletion author="X" date="..."}
#   [eklenen]{.insertion author="X" date="..."}
SPAN_RE = re.compile(
    r"\[(?P<text>[^\]]*)\]\{\.(?P<kind>deletion|insertion)"
    r"(?:\s+author=\"(?P<author>[^\"]*)\")?"
    r"(?:\s+date=\"(?P<date>[^\"]*)\")?[^}]*\}"
)


@dataclass
class Change:
    kind: str                # "deletion" | "insertion" | "comment"
    text: str                # degisen/eklenen/silinen metin (yorumda: yorum govdesi)
    author: str = ""
    date: str = ""
    context_before: str = ""
    context_after: str = ""
    anchor: str = ""         # yorumun bagli oldugu metin (yalniz comment)
    match_file: str = ""
    match_line: int = 0
    match_score: float = 0.0
    match_excerpt: str = ""
    confidence: str = ""     # "yuksek" | "dusuk" | "eslesmedi"


def _strip_spans(text: str) -> str:
    """pandoc track-changes span markup'ini cikar, yalniz duz metin birak.
    Ornek: '…[hata]{.deletion author=\"X\"}[duzeltme]{.insertion …}…' ->
    '…hataduzeltme…'. Fuzzy eslesme icin baglam markup'tan arindirilir."""
    return _norm(SPAN_RE.sub(lambda m: m.group("text"), text))


def _extract_tracked_changes(edited_docx: str) -> list[Change]:
    md = _run_pandoc([edited_docx, "--track-changes=all", "-t", "markdown"])
    changes: list[Change] = []
    for m in SPAN_RE.finditer(md):
        start, end = m.span()
        # baglami markup'tan arindirarak al (komsu ins/del span'leri temizlenir)
        before = _strip_spans(md[max(0, start - CONTEXT_CHARS * 2):start])[-CONTEXT_CHARS:]
        after = _strip_spans(md[end:end + CONTEXT_CHARS * 2])[:CONTEXT_CHARS]
        changes.append(
            Change(
                kind=m.group("kind"),
                text=m.group("text"),
                author=m.group("author") or "",
                date=m.group("date") or "",
                context_before=before,
                context_after=after,
            )
        )
    return changes


# --- IMPORT: yorumlar (dogrudan XML) --------------------------------------

def _extract_comments(edited_docx: str) -> list[Change]:
    """word/comments.xml'den yorumlari, word/document.xml'den de yorumun
    bagli oldugu metni (commentRangeStart..End arasi) cikarir."""
    comments: list[Change] = []
    with zipfile.ZipFile(edited_docx) as z:
        names = set(z.namelist())
        if "word/comments.xml" not in names:
            return comments
        comments_xml = z.read("word/comments.xml")
        document_xml = z.read("word/document.xml") if "word/document.xml" in names else b""

    # comments.xml: id -> (author, date, text)
    croot = ET.fromstring(comments_xml)
    meta: dict[str, tuple[str, str, str]] = {}
    for c in croot.findall(f"{W_NS}comment"):
        cid = c.get(f"{W_NS}id", "")
        author = c.get(f"{W_NS}author", "")
        cdate = c.get(f"{W_NS}date", "")
        texts = [t.text or "" for t in c.iter(f"{W_NS}t")]
        meta[cid] = (author, cdate, "".join(texts))

    # document.xml: her yorum id'sinin bagli oldugu metni topla
    anchors: dict[str, str] = {}
    if document_xml:
        droot = ET.fromstring(document_xml)
        active: dict[str, list[str]] = {}
        for el in droot.iter():
            tag = el.tag
            if tag == f"{W_NS}commentRangeStart":
                cid = el.get(f"{W_NS}id", "")
                active[cid] = []
            elif tag == f"{W_NS}commentRangeEnd":
                cid = el.get(f"{W_NS}id", "")
                if cid in active:
                    anchors[cid] = "".join(active.pop(cid))
            elif tag == f"{W_NS}t":
                for cid in active:
                    active[cid].append(el.text or "")

    for cid, (author, cdate, text) in meta.items():
        anchor = _norm(anchors.get(cid, ""))
        comments.append(
            Change(
                kind="comment",
                text=_norm(text),
                author=author,
                date=cdate,
                anchor=anchor,
                context_before=anchor[:CONTEXT_CHARS],
            )
        )
    return comments


# --- IMPORT: .qmd fuzzy eslesme -------------------------------------------

def _load_chapter_lines() -> list[tuple[str, int, str, str]]:
    """(dosya, satir_no, ham_satir, normalize_satir) listesi dondurur."""
    rows: list[tuple[str, int, str, str]] = []
    if not os.path.isdir(CHAPTERS_DIR):
        return rows
    for fn in sorted(os.listdir(CHAPTERS_DIR)):
        if not fn.endswith(".qmd"):
            continue
        path = os.path.join(CHAPTERS_DIR, fn)
        with open(path, encoding="utf-8") as fh:
            for i, line in enumerate(fh, start=1):
                rows.append((path, i, line.rstrip("\n"), _norm(line)))
    return rows


def _best_match(needle: str, corpus: list[tuple[str, int, str, str]]) -> tuple[str, int, float, str]:
    """needle'i .qmd satirlarinda ara; en iyi (dosya, satir, skor, alinti)."""
    needle_n = _norm(needle)
    if not needle_n:
        return ("", 0, 0.0, "")
    best = ("", 0, 0.0, "")
    sm = difflib.SequenceMatcher()
    sm.set_seq2(needle_n)
    for path, lineno, raw, norm in corpus:
        if not norm:
            continue
        sm.set_seq1(norm)
        # Uzunluk farkina dayanikli skor: probe'un ne kadarinin bu satirda
        # (siraya duyarli) yer aldigini olc. .qmd satiri probe'dan cok daha
        # uzun olabilir (uzun paragraflar tek satir); duz ratio bunu haksiz
        # cezalandirir. Tum ortak bloklarin toplami / probe uzunlugu daha adil.
        matched = sum(b.size for b in sm.get_matching_blocks())
        coverage = matched / len(needle_n) if needle_n else 0.0
        score = max(sm.ratio(), coverage)
        if needle_n in norm:
            score = max(score, 0.95)
        if score > best[2]:
            best = (path, lineno, score, raw.strip())
    return best


def _assign_matches(changes: list[Change]) -> None:
    corpus = _load_chapter_lines()
    for ch in changes:
        # Eslesme icin cevre baglami kullan: kisa bir kelime (or. "hesaplanmis")
        # tek basina yaygin oldugundan yanlis satira eslesir. Silmede silinen
        # metin cumleye ait oldugundan baglam+metin, eklemede yalniz baglam
        # (eklenen metin henuz .qmd'de yok) en guvenilir probe'dur.
        if ch.kind == "deletion":
            probe = f"{ch.context_before} {ch.text} {ch.context_after}".strip()
        elif ch.kind == "insertion":
            probe = f"{ch.context_before} {ch.context_after}".strip()
        else:  # comment
            probe = ch.anchor or ch.text
        path, lineno, score, excerpt = _best_match(probe, corpus)
        ch.match_file = path
        ch.match_line = lineno
        ch.match_score = round(score, 3)
        ch.match_excerpt = excerpt
        if not path:
            ch.confidence = "eslesmedi"
        elif score >= MATCH_THRESHOLD:
            ch.confidence = "yuksek"
        else:
            ch.confidence = "dusuk"


# --- IMPORT: rapor uretimi ------------------------------------------------

def _write_report(changes: list[Change], report_path: str, edited_docx: str) -> None:
    os.makedirs(os.path.dirname(report_path) or ".", exist_ok=True)
    ins = [c for c in changes if c.kind == "insertion"]
    dele = [c for c in changes if c.kind == "deletion"]
    com = [c for c in changes if c.kind == "comment"]
    authors = sorted({c.author for c in changes if c.author})

    lines: list[str] = []
    lines.append("# Ortak Yazar DOCX Round-Trip Raporu\n")
    lines.append(f"- Kaynak dosya: `{edited_docx}`")
    lines.append(f"- Uretim: {date.today().isoformat()}")
    lines.append(f"- Yazar(lar): {', '.join(authors) if authors else '(belirtilmemis)'}")
    lines.append(
        f"- Ozet: {len(ins)} ekleme, {len(dele)} silme, {len(com)} yorum "
        f"(toplam {len(changes)} degisiklik)\n"
    )
    lines.append(
        "> Bu rapor OTOMATIK YAZMAZ. Her oneriyi kontrol edip nesir "
        "duzeltmesini ilgili `.qmd` satirina elle/ajanla uygula. Tablo ici "
        "sayilar, sekiller ve capraz-referanslar kod uretimlidir; bunlara "
        "dokunma.\n"
    )

    def _emit(title: str, items: list[Change]) -> None:
        if not items:
            return
        lines.append(f"\n## {title} ({len(items)})\n")
        for i, c in enumerate(items, start=1):
            loc = (
                f"`{c.match_file}:{c.match_line}`"
                if c.match_file else "_(eslesme yok)_"
            )
            conf = {
                "yuksek": "✅ yuksek",
                "dusuk": "⚠️ dusuk",
                "eslesmedi": "❌ eslesmedi",
            }.get(c.confidence, c.confidence)
            lines.append(f"### {i}. {loc} — guven: {conf} (skor {c.match_score})")
            if c.kind == "comment":
                lines.append(f"- **Yorum:** {c.text}")
                if c.anchor:
                    lines.append(f"- **Bagli metin:** …{c.anchor}…")
            else:
                verb = "Ekle" if c.kind == "insertion" else "Sil"
                lines.append(f"- **{verb}:** `{c.text}`")
                if c.context_before or c.context_after:
                    lines.append(
                        f"- **Baglam:** …{c.context_before} "
                        f"⟦{c.text}⟧ {c.context_after}…"
                    )
            if c.match_excerpt:
                lines.append(f"- **.qmd satiri:** `{c.match_excerpt}`")
            lines.append("")

    _emit("Silmeler (deletion)", dele)
    _emit("Eklemeler (insertion)", ins)
    _emit("Yorumlar (comment)", com)

    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"[import] Rapor yazildi: {report_path}")


def cmd_import(args: argparse.Namespace) -> int:
    edited = args.edited
    if not os.path.isfile(edited):
        sys.exit(f"HATA: donen docx yok: {edited}")

    changes = _extract_tracked_changes(edited)
    changes.extend(_extract_comments(edited))

    if not changes:
        print(
            "[import] Izlenen degisiklik veya yorum bulunamadi.\n"
            "  - Ortak yazar 'Degisiklikleri Izle' ACIK duzelttiginden emin ol.\n"
            "  - Google Docs'ta 'Oneri modu' + yorumlar da desteklenir."
        )
        # bos da olsa temiz cikis (0): parse basarili
        return 0

    _assign_matches(changes)
    _write_report(changes, args.report, edited)

    if args.json:
        os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump([asdict(c) for c in changes], fh, ensure_ascii=False, indent=2)
        print(f"[import] JSON yazildi: {args.json}")

    low = sum(1 for c in changes if c.confidence != "yuksek")
    print(
        f"[import] {len(changes)} degisiklik islendi; "
        f"{low} tanesi dusuk-guven/eslesmedi (elle kontrol gerek)."
    )
    return 0


# --- CLI ------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Ortak yazar DOCX round-trip (export/import).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("export", help="Ortak yazara gidecek docx'i hazirla")
    pe.add_argument(
        "--render",
        default="outputs/quarto/thesis.docx",
        help="quarto render ciktisi (varsayilan: outputs/quarto/thesis.docx)",
    )
    pe.add_argument("--out", default=None, help="hedef docx (varsayilan: outbox/…tarih.docx)")
    pe.set_defaults(func=cmd_export)

    pi = sub.add_parser("import", help="Donen docx'ten degisiklik+yorum cikar")
    pi.add_argument("--edited", required=True, help="ortak yazardan donen docx")
    pi.add_argument(
        "--report",
        default="outputs/coauthor/roundtrip_rapor.md",
        help="markdown rapor cikti yolu",
    )
    pi.add_argument(
        "--json",
        default="outputs/coauthor/roundtrip_degisiklikler.json",
        help="json cikti yolu (bos birakmak icin --json '')",
    )
    pi.set_defaults(func=cmd_import)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
