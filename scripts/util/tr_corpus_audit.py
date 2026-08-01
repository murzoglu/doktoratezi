#!/usr/bin/env python3
"""Tez Dil & İfade Denetçisi — axis H (çevrimdışı, bağımlılıksız).

sci-audit plugin'inin YANINDA (Galileo gibi) çalışan repo-yerel korpus
analizcisi. Üç yetkinliği deterministik olarak denetler:

  headings         — başlık kaskadı, resmi bölüm sırası (§5), büyük-harf/bağlaç
                     (§1.3); kod-çiti farkında (```{r} içindeki `#` başlık DEĞİL).
  coherence        — bölümler-arası yakın-duplikat/mükerrerlik, kısaltma (00b)
                     çapraz-kontrolü, geçiş-belirteci seyrekliği.
  reference-prose  — raportör-fiil monotonluğu, parantetik/anlatısal denge,
                     Tartışma sıfır-atıf boşluğu.

Ağ çağrısı yapmaz; yalnız açıkça verilen manuskript dosyalarını okur; rapor
dışında dosya yazmaz. Bulgu şeması sci-audit `Issue`'yu genişletir (+file/line/
section). Exit: 0 temiz · 1 blocker (HARD) · 2 yalnız major (SOFT) — bib_hygiene
ile uyumlu. Provenans: kurallar `marmara-tez-formati-talimatnamesi.md` §1.3/§5.
"""
from __future__ import annotations

import argparse
import glob as _glob
import json
import pathlib
import re
import zlib
from dataclasses import dataclass, field, asdict

# ---------------------------------------------------------------------------
# Kanonik kurallar — provenans ile ENCODE (runtime-parse değil; §5 değiştirilemez)
# ---------------------------------------------------------------------------

# talimatname §5 RESMİ BÖLÜM SIRASI (değiştirilemez); drift-guard testi bunu
# gerçek talimatnameden parse edip eşitler (parse_canonical_order).
CANONICAL_ORDER: list[str] = [
    "Tez onayı", "Beyan", "Teşekkür", "İçindekiler", "Kısaltmalar",
    "Şekiller", "Tablolar", "Özet", "Summary", "Giriş ve Amaç",
    "Genel Bilgiler", "Gereç ve Yöntem", "Bulgular", "Tartışma ve Sonuç",
    "Kaynaklar", "Özgeçmiş", "Bilimsel Faaliyetler", "Ekler",
]

# Render aşamasında otomatik üretilenler (ayrı dosya değil) — eksikse ihlal sayılmaz.
AUTO_GENERATED = {"içindekiler", "şekiller", "tablolar"}

# talimatname §1.3 — bağlaçlar her başlıkta küçük harf kalabilir.
CONJUNCTIONS = {"ve", "ile", "veya", "ya", "da", "ve/veya"}

# Dosya rolleri (kök tez montajı; thesis.qmd include sırası).
FRONT_STEMS = {"00a_on_bolumler", "00b_kisaltmalar", "00c_ozet_summary"}
BODY_STEMS = {
    "01_giris_ve_amac", "02_genel_bilgiler", "03_gerec_ve_yontem",
    "04_bulgular", "05_tartisma_ve_sonuc",
}
BACK_STEMS = {"06_ozgecmis_faaliyetler", "07_ekler"}

# Gövde bölümlerinin beklenen tek H1 başlığı (normalize karşılaştırma).
EXPECTED_H1 = {
    "01_giris_ve_amac": "giriş ve amaç",
    "02_genel_bilgiler": "genel bilgiler",
    "03_gerec_ve_yontem": "gereç ve yöntem",
    "04_bulgular": "bulgular",
    "05_tartisma_ve_sonuc": "tartışma ve sonuç",
}

# Atıf yoğunluğu politikası — kodlu (sessiz muafiyet yok).
#   expect_zero   : atıfsız bölüm beklenir (kendi sonuç bölümü) → yalnız info
#   expect_nonzero: literatürle karşılaştırılan bölüm → 0 atıf SOFT-block
CITATION_DENSITY_POLICY = {
    "04_bulgular": "expect_zero",
    "05_tartisma_ve_sonuc": "expect_nonzero",
}

# Meşru çapraz-bölüm eko çiftleri (yöntem↔bulgu tekrarı, bulgu↔tartışma geri-çağrısı)
# — yakın-duplikat taramasında bastırılır (yanlış-pozitif önleme).
SUPPRESS_PAIRS = {
    frozenset({"03_gerec_ve_yontem", "04_bulgular"}),
    frozenset({"04_bulgular", "05_tartisma_ve_sonuc"}),
}

# Yerleşik/standart kısaltmalar (00b'ye eklenmesi gerekmeyen; §1.5) — undeclared
# taramasında beyaz-liste.
STANDARD_ABBREV = {
    "WHO", "IDF", "ISPAD", "ADA", "DSM", "ICD", "ABD", "AB", "TÜİK", "TÜBİTAK",
    "HIV", "AIDS", "DNA", "RNA", "USA", "UK", "EU", "SD", "SE", "CI", "OR",
    "RR", "HR", "ANOVA", "ANCOVA", "SPSS", "APA", "ICMJE", "COPE", "WAME",
    "PDF", "DOI", "PMID", "URL", "AI", "GA",
}

# Raportör-fiil kökleri (§ atıf anlatımı doğallığı) — önceki clause'da aranır.
REPORTING_STEMS = [
    "göster", "bildir", "bulun", "bulmuş", "sapta", "belirt", "vurgula",
    "kaydet", "rapor", "öne sür", "savun", "ortaya koy", "işaret", "tanımla",
    "öner", "gözlem", "değin", "aktar", "ele al", "incele",
]

# Paragraf-başı geçiş/bağlayıcı belirteçleri (akış sürekliliği).
TRANSITION_MARKERS = [
    "ayrıca", "bununla birlikte", "ancak", "dolayısıyla", "bu nedenle",
    "öte yandan", "sonuç olarak", "ilk olarak", "buna karşın", "nitekim",
    "böylece", "diğer yandan", "bu bağlamda", "benzer şekilde", "buna göre",
    "bu çerçevede", "özetle", "son olarak", "bu doğrultuda", "ne var ki",
    "bu nedenle", "kaldı ki", "üstelik", "aksine",
]

# ---------------------------------------------------------------------------
# Türkçe-farkında büyük/küçük harf + tokenizasyon
# ---------------------------------------------------------------------------


def tr_upper(s: str) -> str:
    """Türkçe büyük harf (i→İ, ı→I korunur)."""
    return s.replace("i", "İ").replace("ı", "I").upper()


def tr_lower(s: str) -> str:
    """Türkçe küçük harf (I→ı, İ→i korunur)."""
    return s.replace("I", "ı").replace("İ", "i").lower()


def norm_title(s: str) -> str:
    """Başlık normalize: Türkçe küçük harf + boşluk daralt."""
    return " ".join(tr_lower(s).split())


_WORD_RE = re.compile(r"[a-zA-ZçğıöşüÇĞİÖŞÜ]{2,}")
_BRACKET_CITE_RE = re.compile(r"\[[^\]]*?@[^\]]+\]")
_BARE_CITE_RE = re.compile(r"(?<![\[\w@])-?@[A-Za-z0-9][\w:.#$%&+?<>~/-]*")


def _strip_citations(text: str) -> str:
    """[@key]/[@a; @b] ve @key atıflarını metinden çıkar (token gürültüsü)."""
    text = _BRACKET_CITE_RE.sub(" ", text)
    text = _BARE_CITE_RE.sub(" ", text)
    return text


def tokenize_tr(s: str) -> list[str]:
    """Türkçe kelime token'ları (küçük harf; atıf/sayı/istatistik çıkarılır)."""
    s = _strip_citations(s)
    s = tr_lower(s)
    return _WORD_RE.findall(s)


# ---------------------------------------------------------------------------
# Kod-çiti + HTML-yorum farkında tarayıcı (en kritik primitive)
# ---------------------------------------------------------------------------


def strip_fenced(text: str) -> list[tuple[int, str]]:
    """Kod-çiti (```/~~~), `#|` cell-option ve HTML-yorum dışındaki satırları
    (1-tabanlı satır no ile) döndür. ```{r} içindeki `#` yorumları BAŞLIK DEĞİLDİR.
    """
    out: list[tuple[int, str]] = []
    in_fence = False
    fence_tok = ""
    in_comment = False
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if in_fence:
            if stripped.startswith(fence_tok):
                in_fence = False
            continue
        # HTML yorum bloğu (tek satır veya çok satır)
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if stripped.startswith("<!--"):
            if "-->" not in line:
                in_comment = True
            continue
        # kod-çiti aç
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = True
            fence_tok = "```" if stripped.startswith("```") else "~~~"
            continue
        # cell-option satırı
        if stripped.startswith("#|"):
            continue
        out.append((i, line))
    return out


# ---------------------------------------------------------------------------
# Bulgu şeması (sci-audit Issue'yu genişletir)
# ---------------------------------------------------------------------------

# code → varsayılan severity (blocker=HARD · major=SOFT · minor=advisory).
CODE_SEVERITY = {
    "H-HC1": "blocker", "H-HC3": "blocker", "H-ORD": "blocker", "H-HC6a": "blocker",
    "H-HC2": "major", "H-HC4": "major", "H-HC5": "major",
    "H-DUP": "major", "H-ABBR": "major", "H-DISCZERO": "major",
    "H-RED": "minor", "H-VERB": "minor", "H-BRAK": "minor", "H-RATIO": "minor",
    "H-TRANS": "minor", "H-FIT": "minor", "H-HC6b": "minor", "H-HC6c": "minor",
    "H-HC7": "minor", "H-DENS": "minor", "H-ABBR-UNUSED": "minor",
    "H-ABBR-FIRSTUSE": "minor", "H-INFO": "minor",
}

_SEV_RANK = {"blocker": 1, "major": 2, "minor": 3}


@dataclass
class Finding:
    """axis-H bulgusu — sci-audit şeması + file/line/section/peer."""
    code: str
    message: str
    file: str = ""
    line: int | None = None
    section: str = ""
    evidence: str = ""
    peer: dict | None = None
    axis: str = "H"
    severity: str = ""

    def __post_init__(self):
        if not self.severity:
            self.severity = CODE_SEVERITY.get(self.code, "minor")


def _f(code: str, message: str, **kw) -> Finding:
    return Finding(code=code, message=message, **kw)


# ---------------------------------------------------------------------------
# Başlık çıkarımı (çit-farkında; trailing {..} ayır; derinlik 1–6)
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_ATTR_RE = re.compile(r"\{([^}]*)\}\s*$")


def extract_headings(text: str) -> list[dict]:
    """Kod-çiti/yorum dışı, kolon-0 başlıkları {depth,title,attrs,line}."""
    heads: list[dict] = []
    for lineno, line in strip_fenced(text):
        m = _HEADING_RE.match(line)
        if not m:
            continue
        depth = len(m.group(1))
        raw = m.group(2)
        attrs = ""
        am = _ATTR_RE.search(raw)
        if am:
            attrs = am.group(1)
            raw = raw[: am.start()].rstrip()
        heads.append({"depth": depth, "title": raw, "attrs": attrs, "line": lineno})
    return heads


def _heading_words(title: str) -> list[str]:
    """Başlığı kelimelere ayır; çevre noktalama/parantez soy (case testi için)."""
    words = []
    for tok in title.split():
        w = tok.strip("().,:;—–-*_“”\"'")
        if w:
            words.append(w)
    return words


def _is_abbrevish(w: str) -> bool:
    """Kısaltma-benzeri token (case testinde atlanır): büyük-harf ağırlıklı/rakamlı."""
    letters = [c for c in w if c.isalpha()]
    if not letters:
        return True
    if any(ch.isdigit() for ch in w):
        return True
    if all(c == tr_upper(c) for c in letters) and len(letters) >= 2:
        return True
    return False


def _starts_upper(w: str) -> bool:
    first = next((c for c in w if c.isalpha()), "")
    return first != "" and first == tr_upper(first)


# ---------------------------------------------------------------------------
# headings alt-analizcisi
# ---------------------------------------------------------------------------


def _stem(path: str) -> str:
    return pathlib.Path(path).stem


def check_case(heads: list[dict], file: str) -> list[Finding]:
    """§1.3 büyük-harf/bağlaç: H1 ALLCAPS (HARD), H2 Title, H3 sentence (advisory)."""
    out: list[Finding] = []
    for h in heads:
        depth, title = h["depth"], h["title"]
        words = _heading_words(title)
        if not words:
            continue
        if depth == 1:
            # ana başlık: bağlaç dışı her sözcük tamamen büyük harf
            for w in words:
                if tr_lower(w) in CONJUNCTIONS:
                    if w != tr_lower(w):
                        out.append(_f("H-HC6a",
                                      f"Ana başlıkta bağlaç büyük harfle: '{w}' (bağlaç küçük olmalı).",
                                      file=file, line=h["line"], section=title, evidence=title))
                    continue
                if _is_abbrevish(w):
                    continue
                if w != tr_upper(w):
                    out.append(_f("H-HC6a",
                                  f"Ana başlık tamamı büyük harf değil: '{w}'.",
                                  file=file, line=h["line"], section=title, evidence=title))
        elif depth == 2:
            for w in words:
                if tr_lower(w) in CONJUNCTIONS or _is_abbrevish(w):
                    continue
                if not _starts_upper(w):
                    out.append(_f("H-HC6b",
                                  f"1. düzey alt başlıkta sözcük büyük harfle başlamıyor: '{w}' (Başlık Düzeni).",
                                  file=file, line=h["line"], section=title, evidence=title))
        elif depth == 3:
            first = next((w for w in words if not _is_abbrevish(w)), "")
            if first and not _starts_upper(first):
                out.append(_f("H-HC6c",
                              f"2. düzey alt başlık büyük harfle başlamıyor: '{first}'.",
                              file=file, line=h["line"], section=title, evidence=title))
    return out


def check_cascade(heads: list[dict], file: str) -> list[Finding]:
    """Düzey atlama (H-HC1 HARD), derinlik>3 (H-HC2), ilk-başlık/çoklu-H1 (H-HC3/4),
    body'de {.unnumbered} (H-HC5), başlık sonu noktalama (H-HC7)."""
    out: list[Finding] = []
    stem = _stem(file)
    prev_depth = None
    h1_count = 0
    for idx, h in enumerate(heads):
        depth, title = h["depth"], h["title"]
        if depth == 1:
            h1_count += 1
        # H-HC2 derinlik > 3
        if depth > 3:
            out.append(_f("H-HC2", f"Başlık derinliği 3'ü aşıyor (düzey {depth}).",
                          file=file, line=h["line"], section=title, evidence=title))
        # H-HC1 düzey atlama
        if prev_depth is not None and depth > prev_depth + 1:
            out.append(_f("H-HC1",
                          f"Başlık düzey atlaması: H{prev_depth}→H{depth} (ara düzey yok).",
                          file=file, line=h["line"], section=title, evidence=title))
        prev_depth = depth
        # H-HC7 başlık sonu noktalama
        if title.rstrip().endswith((".", ":", ";", ",")):
            out.append(_f("H-HC7", "Başlık sonunda noktalama işareti var.",
                          file=file, line=h["line"], section=title, evidence=title))
        # H-HC5 body'de numaralı başlıkta {.unnumbered}
        if stem in BODY_STEMS and ".unnumbered" in h["attrs"]:
            out.append(_f("H-HC5", "Gövde bölümünde numaralı başlıkta {.unnumbered}.",
                          file=file, line=h["line"], section=title, evidence=title))
    # H-HC3 ilk başlık H1 değil / beklenen H1 değil
    if heads:
        first = heads[0]
        if first["depth"] != 1:
            out.append(_f("H-HC3",
                          f"Bölümün ilk başlığı H1 değil (H{first['depth']}).",
                          file=file, line=first["line"], section=first["title"],
                          evidence=first["title"]))
        elif stem in EXPECTED_H1 and norm_title(first["title"]) != EXPECTED_H1[stem]:
            out.append(_f("H-HC3",
                          f"Gövde bölümü ilk H1 beklenenden farklı: '{first['title']}' "
                          f"(beklenen: {EXPECTED_H1[stem]}).",
                          file=file, line=first["line"], section=first["title"],
                          evidence=first["title"]))
    # H-HC4 gövde bölümünde çoklu H1
    if stem in BODY_STEMS and h1_count > 1:
        out.append(_f("H-HC4", f"Gövde bölümünde birden fazla H1 ({h1_count}).", file=file))
    return out


def build_assembled_h1_sequence(thesis_path: str) -> list[dict]:
    """thesis.qmd include sırası + enjekte satır-içi H1'lerden montajlı H1 dizisi."""
    thesis = pathlib.Path(thesis_path)
    base = thesis.parent
    seq: list[dict] = []
    inc_re = re.compile(r"\{\{<\s*include\s+(\S+?\.qmd)\s*>\}\}")
    for lineno, line in strip_fenced(thesis.read_text(encoding="utf-8")):
        m = inc_re.search(line)
        if m:
            inc = (base / m.group(1)).resolve()
            if inc.exists():
                for h in extract_headings(inc.read_text(encoding="utf-8")):
                    if h["depth"] == 1:
                        seq.append({"title": h["title"], "file": str(inc), "line": h["line"]})
            continue
        hm = _HEADING_RE.match(line)
        if hm and len(hm.group(1)) == 1:
            raw = hm.group(2)
            am = _ATTR_RE.search(raw)
            if am:
                raw = raw[: am.start()].rstrip()
            seq.append({"title": raw, "file": str(thesis), "line": lineno})
    return seq


def check_section_order(seq: list[dict]) -> list[Finding]:
    """Montajlı H1 dizisini §5 kanonik sıraya göre denetle (H-ORD HARD)."""
    out: list[Finding] = []
    norm_canon = [norm_title(c) for c in CANONICAL_ORDER]
    last_idx = -1
    last_title = ""
    observed = set()
    for h in seq:
        nt = norm_title(h["title"])
        if nt not in norm_canon:
            continue  # bilinmeyen H1 (montaj-dışı) atlanır
        observed.add(nt)
        idx = norm_canon.index(nt)
        if idx < last_idx:
            out.append(_f("H-ORD",
                          f"Resmi bölüm sırası ihlali: '{h['title']}' ('{last_title}' sonrasında; "
                          f"§5 sırasında önce gelmeli).",
                          file=h["file"], line=h["line"], section=h["title"],
                          evidence=h["title"]))
        else:
            last_idx = idx
            last_title = h["title"]
    # eksik zorunlu bölümler (otomatik-üretilen hariç)
    for i, nt in enumerate(norm_canon):
        if nt in AUTO_GENERATED:
            continue
        if nt not in observed:
            out.append(_f("H-ORD",
                          f"Zorunlu bölüm montajda yok: '{CANONICAL_ORDER[i]}' (§5).",
                          file="thesis.qmd", section=CANONICAL_ORDER[i]))
    return out


def run_headings(files: list[str], thesis: str | None) -> list[Finding]:
    """headings alt-analizcisi: cascade + case (her dosya) + section-order (montaj)."""
    out: list[Finding] = []
    for fp in files:
        text = pathlib.Path(fp).read_text(encoding="utf-8")
        heads = extract_headings(text)
        out += check_cascade(heads, fp)
        out += check_case(heads, fp)
    if thesis:
        out += check_section_order(build_assembled_h1_sequence(thesis))
    return out


# ---------------------------------------------------------------------------
# Paragraf segmentasyonu + korpus çözümü
# ---------------------------------------------------------------------------


def segment_paragraphs(text: str) -> list[dict]:
    """Kod-çiti/yorum dışı prose paragrafları {text,line}; başlık/tablo/liste/div hariç."""
    lines = strip_fenced(text)
    paras: list[dict] = []
    buf: list[str] = []
    start_line = None
    for lineno, line in lines:
        s = line.strip()
        is_break = (
            s == "" or s.startswith("#") or s.startswith("|") or s.startswith(">")
            or s.startswith(":::") or s.startswith("- ") or s.startswith("* ")
            or s.startswith("!") or re.match(r"^\d+\.\s", s) or s.startswith("$$")
        )
        if is_break:
            if buf:
                paras.append({"text": " ".join(buf), "line": start_line})
                buf = []
                start_line = None
            continue
        if not buf:
            start_line = lineno
        buf.append(s)
    if buf:
        paras.append({"text": " ".join(buf), "line": start_line})
    return paras


def resolve_corpus(thesis: str | None, chapters: list[str]) -> list[str]:
    """Denetlenecek dosya listesi: --thesis varsa include sırası, yoksa --chapters glob."""
    if thesis:
        base = pathlib.Path(thesis).parent
        inc_re = re.compile(r"\{\{<\s*include\s+(\S+?\.qmd)\s*>\}\}")
        files: list[str] = []
        for _, line in strip_fenced(pathlib.Path(thesis).read_text(encoding="utf-8")):
            m = inc_re.search(line)
            if m:
                p = (base / m.group(1)).resolve()
                if p.exists():
                    files.append(str(p))
        if files:
            return files
    files = []
    for pat in chapters:
        files += sorted(_glob.glob(pat))
    return files


# ---------------------------------------------------------------------------
# 00b kısaltma termbase
# ---------------------------------------------------------------------------


def load_termbase(abbrev_path: str | None, terms: str | None) -> dict:
    """00b `| Kısaltma | Açıklama |` tablosu + --terms → {abbr_upper} ve token seti."""
    abbrevs: set[str] = set()
    if abbrev_path and pathlib.Path(abbrev_path).exists():
        for _, line in strip_fenced(pathlib.Path(abbrev_path).read_text(encoding="utf-8")):
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            key = cells[0]
            if not key or key.lower() in ("kısaltma", "kisaltma") or set(key) <= set("-: "):
                continue
            abbrevs.add(key)
    term_tokens: set[str] = set()
    for a in abbrevs:
        term_tokens |= set(tokenize_tr(a))
    if terms:
        for t in terms.split(","):
            term_tokens |= set(tokenize_tr(t))
    return {"abbrevs": abbrevs, "term_tokens": term_tokens}


# ---------------------------------------------------------------------------
# coherence: yakın-duplikat + kısaltma-drift + geçiş belirteci
# ---------------------------------------------------------------------------

_SHINGLE_N = 5
_MIN_TOKENS = 25


def _shingles(tokens: list[str]) -> set[int]:
    if len(tokens) < _SHINGLE_N:
        return set()
    return {
        zlib.crc32(" ".join(tokens[i:i + _SHINGLE_N]).encode("utf-8"))
        for i in range(len(tokens) - _SHINGLE_N + 1)
    }


def _prose_ratio(tokens: list[str], term_tokens: set[str]) -> float:
    if not tokens:
        return 0.0
    non_term = sum(1 for t in tokens if t not in term_tokens)
    return non_term / len(tokens)


def near_duplicates(corpus: list[dict], term_tokens: set[str]) -> list[Finding]:
    """Shingle + containment/Jaccard ile çapraz/iç-bölüm yakın-duplikat & mükerrerlik."""
    units = []  # {id, file, line, tokens, shingles, snippet}
    for para in corpus:
        toks = tokenize_tr(para["text"])
        if len(toks) < _MIN_TOKENS:
            continue
        if _prose_ratio(toks, term_tokens) <= 0.5:
            continue  # terim-yoğun eşleşme (meşru yöntem/ölçek tekrarı) bastır
        sh = _shingles(toks)
        if not sh:
            continue
        units.append({
            "id": len(units), "file": para["file"], "line": para["line"],
            "tokens": toks, "sh": sh, "snip": para["text"][:120],
        })
    # ters-indeks önfiltre
    inv: dict[int, list[int]] = {}
    for u in units:
        for s in u["sh"]:
            inv.setdefault(s, []).append(u["id"])
    cand: set[frozenset] = set()
    for ids in inv.values():
        if len(ids) < 2:
            continue
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                cand.add(frozenset({ids[i], ids[j]}))
    out: list[Finding] = []
    for pair in cand:
        a, b = sorted(pair)
        ua, ub = units[a], units[b]
        inter = len(ua["sh"] & ub["sh"])
        if not inter:
            continue
        containment = inter / min(len(ua["sh"]), len(ub["sh"]))
        union = len(ua["sh"] | ub["sh"])
        jacc = inter / union if union else 0.0
        cross = ua["file"] != ub["file"]
        if cross and frozenset({_stem(ua["file"]), _stem(ub["file"])}) in SUPPRESS_PAIRS:
            continue  # meşru yöntem↔bulgu / bulgu↔tartışma eko bastırma
        peer = {"file": ub["file"], "line": ub["line"]}
        if containment >= 0.80:
            out.append(_f("H-DUP",
                          f"Yakın-duplikat paragraf (containment={containment:.2f}): "
                          f"{_stem(ua['file'])}↔{_stem(ub['file'])}.",
                          file=ua["file"], line=ua["line"], evidence=ua["snip"], peer=peer))
        elif 0.40 <= jacc < 0.80:
            out.append(_f("H-RED",
                          f"Mükerrer/örtüşen anlatım (Jaccard={jacc:.2f}): "
                          f"{_stem(ua['file'])}↔{_stem(ub['file'])}.",
                          file=ua["file"], line=ua["line"], evidence=ua["snip"], peer=peer))
    out.sort(key=lambda f: (_SEV_RANK[f.severity], f.file, f.line or 0))
    return out


_ACRONYM_RE = re.compile(r"\b([A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ0-9\-]{1,7})\b")
# Karışık-kaap / önek-tireli kısaltmalar (ör. s-EMBU-C, EBIC-LASSO, sNB) için
# ek "kullanım" tespiti: küçük harf önek + büyük gövde ya da harf+rakam karışımı.
# _ACRONYM_RE yalnız büyük-harf-başı token yakaladığından bunları kaçırıp
# yanlış H-ABBR-UNUSED üretiyordu; bu ikinci geçiş o yanlış-pozitifi kapatır.
_MIXEDCASE_ABBR_RE = re.compile(
    r"\b([A-Za-zçğıöşüÇĞİÖŞÜ]+(?:-[A-Za-z0-9çğıöşüÇĞİÖŞÜ()]+)+|"  # tireli: s-EMBU-C
    r"[A-Za-zçğıöşüÇĞİÖŞÜ]*[A-Z][A-Za-z]*[0-9][A-Za-z0-9]*|"       # harf+rakam: BDI2
    r"[a-zçğıöşü][A-ZÇĞİÖŞÜ]{2,})"                                  # camelCase: sNB
)


def abbrev_crosscheck(corpus_texts: dict[str, str], termbase: dict) -> list[Finding]:
    """00b çift-yönlü: tanımsız (SOFT), kullanılmayan (advisory)."""
    out: list[Finding] = []
    abbrevs = {a for a in termbase["abbrevs"]}
    abbrev_upper = {tr_upper(a) for a in abbrevs}
    # metinde geçen akronim sayımı
    counts: dict[str, int] = {}
    first_loc: dict[str, tuple[str, int]] = {}
    for fp, text in corpus_texts.items():
        clean = "\n".join(l for _, l in strip_fenced(text))
        clean = _strip_citations(clean)
        for ln, line in enumerate(clean.splitlines(), start=1):
            for m in _ACRONYM_RE.finditer(line):
                tok = m.group(1)
                counts[tok] = counts.get(tok, 0) + 1
                first_loc.setdefault(tok, (fp, ln))
    used_norm = {tr_upper(t) for t in counts}
    # İkinci geçiş: karışık-kaap/tireli kısaltma kullanımlarını da "kullanıldı"
    # kümesine ekle (H-ABBR-UNUSED yanlış-pozitiflerini önler). Bunlar tanımsız
    # (H-ABBR) sayımına dahil edilmez; yalnız UNUSED drift kontrolünü besler.
    for fp, text in corpus_texts.items():
        clean = _strip_citations("\n".join(l for _, l in strip_fenced(text)))
        for m in _MIXEDCASE_ABBR_RE.finditer(clean):
            used_norm.add(tr_upper(m.group(1)))
    # tanımsız (≥2 kez, standart-liste dışı, 00b dışı)
    for tok, n in sorted(counts.items()):
        up = tr_upper(tok)
        if n < 2 or up in abbrev_upper or tok in STANDARD_ABBREV or up in STANDARD_ABBREV:
            continue
        fp, ln = first_loc[tok]
        out.append(_f("H-ABBR",
                      f"Metinde geçen kısaltma 00b/Kısaltmalar listesinde yok: '{tok}' ({n}×).",
                      file=fp, line=ln, evidence=tok))
    # kullanılmayan 00b girdisi (drift)
    for a in sorted(abbrevs):
        if tr_upper(a) not in used_norm:
            out.append(_f("H-ABBR-UNUSED",
                          f"00b'de tanımlı ama metinde kullanılmayan kısaltma: '{a}'.",
                          file="chapters/00b_kisaltmalar.qmd", evidence=a))
    return out


def transition_markers(corpus: list[dict]) -> list[Finding]:
    """Paragraf-başı geçiş belirteci seyrekliği (dosya bazında; advisory)."""
    out: list[Finding] = []
    by_file: dict[str, list[dict]] = {}
    for p in corpus:
        by_file.setdefault(p["file"], []).append(p)
    for fp, paras in by_file.items():
        if len(paras) < 8:
            continue
        hits = 0
        for p in paras:
            low = tr_lower(p["text"].lstrip())
            if any(low.startswith(m) for m in TRANSITION_MARKERS):
                hits += 1
        ratio = hits / len(paras)
        if ratio < 0.08:
            out.append(_f("H-TRANS",
                          f"Geçiş belirteci seyrek: {hits}/{len(paras)} paragraf "
                          f"(oran {ratio:.2f}); akış sürekliliği zayıf olabilir.",
                          file=fp))
    return out


def run_coherence(files: list[str], termbase: dict) -> list[Finding]:
    corpus: list[dict] = []
    texts: dict[str, str] = {}
    for fp in files:
        text = pathlib.Path(fp).read_text(encoding="utf-8")
        texts[fp] = text
        for para in segment_paragraphs(text):
            corpus.append({"file": fp, "line": para["line"], "text": para["text"]})
    out: list[Finding] = []
    out += near_duplicates(corpus, termbase["term_tokens"])
    out += abbrev_crosscheck(texts, termbase)
    out += transition_markers(corpus)
    return out


# ---------------------------------------------------------------------------
# reference-prose: raportör-fiil + parantetik denge + Tartışma sıfır-atıf
# ---------------------------------------------------------------------------


def _count_citations(text: str) -> tuple[int, int]:
    """(parantetik [@..] site sayısı, anlatısal @key site sayısı)."""
    clean = "\n".join(l for _, l in strip_fenced(text))
    bracket = len(_BRACKET_CITE_RE.findall(clean))
    narrative = len(_BARE_CITE_RE.findall(_BRACKET_CITE_RE.sub(" ", clean)))
    return bracket, narrative


def reporting_verb_monotony(text: str, file: str) -> list[Finding]:
    """Parantetik atıf öncesi raportör-fiil monotonluğu (advisory)."""
    clean = "\n".join(l for _, l in strip_fenced(text))
    stem_counts: dict[str, int] = {}
    with_verb = 0
    total = 0
    for m in _BRACKET_CITE_RE.finditer(clean):
        total += 1
        pre = tr_lower(clean[max(0, m.start() - 80):m.start()])
        matched = None
        for stem in REPORTING_STEMS:
            if stem in pre:
                matched = stem
                break
        if matched:
            with_verb += 1
            stem_counts[matched] = stem_counts.get(matched, 0) + 1
    out: list[Finding] = []
    if with_verb >= 12:
        top_stem, top_n = max(stem_counts.items(), key=lambda kv: kv[1])
        share = top_n / with_verb
        if share > 0.40:
            out.append(_f("H-VERB",
                          f"Raportör-fiil monotonluğu: '{top_stem}…' atıfların "
                          f"%{share * 100:.0f}'inde ({top_n}/{with_verb}); çeşitlendirin.",
                          file=file, evidence=top_stem))
    return out


def bracket_monotony(text: str, file: str) -> list[Finding]:
    """Trailing-bracket baskınlığı (parantetik/anlatısal denge; advisory)."""
    bracket, narrative = _count_citations(text)
    total = bracket + narrative
    out: list[Finding] = []
    if total >= 15:
        share = bracket / total
        if share > 0.90:
            out.append(_f("H-BRAK",
                          f"Atıfların %{share * 100:.0f}'i parantetik ([@..]); anlatısal "
                          f"(Yazar (yıl)) biçim {narrative}/{total}. Denge/çeşitlilik zayıf.",
                          file=file, evidence=f"bracket={bracket}, narrative={narrative}"))
    return out


def citation_density(text: str, file: str) -> list[Finding]:
    """Politika-güdümlü atıf yoğunluğu; Tartışma sıfır-atıf = SOFT (H-DISCZERO)."""
    bracket, narrative = _count_citations(text)
    total = bracket + narrative
    stem = _stem(file)
    policy = CITATION_DENSITY_POLICY.get(stem)
    out: list[Finding] = []
    if policy == "expect_nonzero" and total == 0:
        out.append(_f("H-DISCZERO",
                      "Tartışma bölümü literatürle karşılaştırma gerektirir ama 0 inline "
                      "atıf içeriyor (§3.7); bulgular kaynaklarla ilişkilendirilmeli.",
                      file=file))
    elif policy == "expect_zero":
        if total > 0:
            out.append(_f("H-INFO",
                          f"Bulgular bölümünde {total} atıf var (§3.6 yorumsuz sunum bekler).",
                          file=file))
    elif stem in BODY_STEMS and total == 0:
        out.append(_f("H-DENS", "Gövde bölümünde inline atıf yok.", file=file))
    return out


def run_reference_prose(files: list[str]) -> list[Finding]:
    out: list[Finding] = []
    for fp in files:
        text = pathlib.Path(fp).read_text(encoding="utf-8")
        out += reporting_verb_monotony(text, fp)
        out += bracket_monotony(text, fp)
        out += citation_density(text, fp)
    return out


# ---------------------------------------------------------------------------
# Orkestrasyon + rapor + CLI
# ---------------------------------------------------------------------------


def _summary(findings: list[Finding]) -> dict:
    s = {"blocker": 0, "major": 0, "minor": 0}
    for f in findings:
        s[f.severity] = s.get(f.severity, 0) + 1
    return s


def run_all(files: list[str], thesis: str | None, termbase: dict) -> dict:
    """headings + coherence + reference-prose birleşik koşum."""
    headings = run_headings(files, thesis)
    coherence = run_coherence(files, termbase)
    refprose = run_reference_prose(files)
    findings = headings + coherence + refprose
    return {
        "counts": {"files": len(files)},
        "headings": [asdict(f) for f in headings],
        "coherence": [asdict(f) for f in coherence],
        "reference_prose": [asdict(f) for f in refprose],
        "findings": [asdict(f) for f in findings],
        "summary": _summary(findings),
    }


def _severity_code(summary: dict, fail_on: str) -> int:
    if fail_on == "none":
        return 0
    if summary.get("blocker"):
        return 1
    if fail_on == "blocker":
        return 0
    return 2 if summary.get("major") else 0


def _render_report(res: dict) -> str:
    order = {"blocker": "HARD", "major": "SOFT-block", "minor": "advisory"}
    lines = ["# Tez Dil & İfade Denetimi (axis H)", "",
             f"- Dosya: {res['counts']['files']} · "
             f"HARD: {res['summary'].get('blocker', 0)} · "
             f"SOFT: {res['summary'].get('major', 0)} · "
             f"advisory: {res['summary'].get('minor', 0)}", ""]
    for sev in ("blocker", "major", "minor"):
        group = [f for f in res["findings"] if f["severity"] == sev]
        lines.append(f"## {order[sev]} ({len(group)})")
        if not group:
            lines.append("- (yok)")
        for f in group:
            loc = f["file"]
            if f["line"]:
                loc += f":{f['line']}"
            peer = ""
            if f.get("peer"):
                peer = f" ↔ {f['peer']['file']}:{f['peer'].get('line')}"
            lines.append(f"- `{f['code']}` {loc}{peer} — {f['message']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Tez Dil & İfade Denetçisi (axis H)")
    p.add_argument("command", choices=["headings", "coherence", "reference-prose", "all"])
    p.add_argument("--thesis", help="thesis.qmd (montaj sırası + bölüm-sırası denetimi)")
    p.add_argument("--chapters", nargs="*", default=["chapters/*.qmd"])
    p.add_argument("--abbrev", default="chapters/00b_kisaltmalar.qmd")
    p.add_argument("--terms", default="diyabet,depresyon,ebeveyn,kardeş,ölçek,yöntem")
    p.add_argument("--json", action="store_true")
    p.add_argument("--out")
    p.add_argument("--fail-on", choices=["blocker", "major", "none"], default="major")
    a = p.parse_args(argv)

    files = resolve_corpus(a.thesis, a.chapters)
    termbase = load_termbase(a.abbrev, a.terms)

    if a.command == "headings":
        findings = run_headings(files, a.thesis)
    elif a.command == "coherence":
        findings = run_coherence(files, termbase)
    elif a.command == "reference-prose":
        findings = run_reference_prose(files)
    else:
        res = run_all(files, a.thesis, termbase)
        if a.out:
            pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            pathlib.Path(a.out).write_text(_render_report(res), encoding="utf-8")
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(_render_report(res))
        return _severity_code(res["summary"], a.fail_on)

    res = {
        "counts": {"files": len(files)},
        "findings": [asdict(f) for f in findings],
        "summary": _summary(findings),
    }
    if a.out:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.out).write_text(_render_report(res), encoding="utf-8")
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(_render_report(res))
    return _severity_code(res["summary"], a.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
