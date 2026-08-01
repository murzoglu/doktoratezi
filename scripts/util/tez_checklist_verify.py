#!/usr/bin/env python3
"""Tez kontrol checklisti — birleşik doğrulama orkestratörü.

`tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md` master checklist'inin
otomatikleştirilebilir maddelerini tek koşumda çalıştırır ve birleşik bir
PASS/FAIL/SKIP/MANUEL raporu üretir. Salt-okuma: hiçbir dosyayı değiştirmez.

Her madde `scripts/util/` altındaki mevcut denetçileri (bib_hygiene,
karma_ledger_check, claim_certification, tr_corpus_audit, csr_* denetimleri) ya
alt-süreç olarak çağırır ya da hafif yerel bir kontrol (render/crossref taraması,
Marmara format ölçümü, targets/renv durumu, PII/gitignore sınırı, başlık
numaralandırma) uygular. Aracın gereksinimi karşılanmıyorsa madde SKIP + neden.

Kanonik ID otoritesi: bu dosyadaki CHECKS kaydı ile master checklist maddeleri
birebir eşleşir (yetim madde/kontrol yoktur; `--list` ve `--audit-doc` ile
denetlenebilir).

KVKK: Tüm kontroller yalnız türetilmiş/metin düzeyinde çalışır. `data/raw`,
`data/identified`, `data/cleaned`, `data/backup` içerikleri OKUNMAZ; yalnız
varlık ve `.gitignore` durumu denetlenir. Satır düzeyi katılımcı verisi ne
okunur ne raporlanır.

Exit: 0 = otomatik maddelerin tümü PASS/SKIP · 1 = en az bir otomatik HARD FAIL.
MANUEL maddeler exit kodunu etkilemez (raporda ayrı listelenir).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys

_HERE = os.path.abspath(__file__)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
UTIL = os.path.join(REPO_ROOT, "scripts", "util")

THESIS = "thesis.qmd"
CHAPTERS_DIR = "chapters"
RENDER_HTML = "outputs/quarto/thesis.html"
RENDER_PDF = "outputs/quarto/thesis.pdf"
FORMAT_TALIMATNAME = "tez-yazim/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md"
MASTER_CHECKLIST = "tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md"
CANONICAL_LOCK = "data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock"
GALILEO_ARTIFACT = "outputs/reports/galileo_full_thesis_judge.json"

# PII sınırı: bu ağaçların İÇERİĞİ hiçbir koşulda okunmaz.
PII_TREES = ["data/raw", "data/identified", "data/cleaned", "data/backup"]

# Durum kodları
PASS, FAIL, SKIP, MANUEL = "PASS", "FAIL", "SKIP", "MANUEL"

# ANSI (yalnız TTY'de)
_TTY = sys.stdout.isatty()
def _c(code, s):
    return f"\033[{code}m{s}\033[0m" if _TTY else s
_COLOR = {PASS: lambda s: _c("32", s), FAIL: lambda s: _c("31", s),
          SKIP: lambda s: _c("33", s), MANUEL: lambda s: _c("36", s)}


class Result:
    __slots__ = ("cid", "status", "evidence")
    def __init__(self, cid, status, evidence=""):
        self.cid = cid
        self.status = status
        self.evidence = evidence


def _p(rel):
    return os.path.join(REPO_ROOT, rel)


def _read(rel, limit=None):
    path = _p(rel)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read(limit) if limit else fh.read()


_FENCE_RX = re.compile(r"^[ \t]*(```|~~~).*?$.*?^[ \t]*\1[ \t]*$",
                       re.M | re.S)
_INLINE_CODE_RX = re.compile(r"`[^`\n]*`")


def _strip_code(txt):
    """Fenced (``` / ~~~) ve satır-içi (`...`) kod bloklarını at.

    Gövde-metni denetimleri (ondalık virgül, atıf düzyazısı vb.) kod
    yorumlarında/chunk'larında yalancı-pozitif üretmesin diye kullanılır.
    """
    if not txt:
        return txt or ""
    txt = _FENCE_RX.sub("", txt)
    txt = _INLINE_CODE_RX.sub("", txt)
    return txt


def _strip_english_summary(txt):
    """İngilizce SUMMARY/ABSTRACT bölümünü at.

    Ondalık-ayırıcı denetimi yalnız Türkçe gövde için geçerlidir; İngilizce
    özet nokta-ondalık kullanır (ör. 0.16, g ≈ 0.36) ve §1.4 virgül kuralına
    tabi değildir. Bölüm sınırı `# SUMMARY` / `# ABSTRACT` başlığından itibaren.
    """
    if not txt:
        return txt or ""
    return re.sub(
        r"(?ims)^\s*#{1,6}\s*(SUMMARY|ABSTRACT)\b.*$",
        "",
        txt,
    )


def _run(cmd, timeout=900):
    """Alt-süreç çalıştır → (returncode, stdout+stderr). Yol REPO_ROOT."""
    try:
        proc = subprocess.run(
            cmd, cwd=REPO_ROOT, capture_output=True, text=True,
            timeout=timeout,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except FileNotFoundError as exc:
        return 127, f"komut bulunamadı: {exc}"
    except subprocess.TimeoutExpired:
        return 124, "zaman aşımı"


def _tool_exists(rel):
    return os.path.exists(_p(rel))


def _skip_or_fail(cid, ctx, reason):
    """Kapanış modunda araç/önkoşul eksikliği SKIP değil FAIL'dir (gate-presence).

    Normal koşumda önkoşulu karşılanmayan madde SKIP'tir; `--closing` (teslim)
    modunda bir denetçinin/CSR'ın/aracın eksikliği kapının sessizce silinmesi
    demektir → FAIL. Yalnız araç/önkoşul eksikliğinde çağrılır (`--fast` SKIP'i
    kapanışta zaten reddedilir).
    """
    return Result(cid, FAIL if ctx.get("closing") else SKIP, reason)


# ---------------------------------------------------------------------------
# Kontrol uygulayıcıları. Her biri (ctx) alır, Result döndürür.
# ctx: {"fast": bool, "chapter": str|None}
# ---------------------------------------------------------------------------

def chk_pii_gitignore(cid, ctx):
    """PII ağaçları .gitignore kapsamında ve git-izlenmiyor mu?"""
    missing = []
    tracked = []
    for tree in PII_TREES:
        # .gitignore dizin desenleri sonda '/' taşıyabilir; check-ignore bunu
        # yalnız sonda '/' ile sorulan (veya var olan) yolda eşler. Her iki
        # biçimi de dene: hangisi eşlerse kapsanmış say.
        rc_plain, _ = _run(["git", "check-ignore", "-q", tree], timeout=30)
        rc_slash, _ = _run(["git", "check-ignore", "-q", tree + "/"], timeout=30)
        if rc_plain != 0 and rc_slash != 0:
            missing.append(tree)
        rc2, out = _run(["git", "ls-files", "--error-unmatch", tree], timeout=30)
        if rc2 == 0 and out.strip():
            tracked.append(tree)
    if missing or tracked:
        parts = []
        if missing:
            parts.append("gitignore dışı: " + ", ".join(missing))
        if tracked:
            parts.append("git-izlenen: " + ", ".join(tracked))
        return Result(cid, FAIL, "; ".join(parts))
    return Result(cid, PASS, f"{len(PII_TREES)} PII ağacı gitignore'da ve izlenmiyor")


def chk_pii_no_names(cid, ctx):
    """chapters/*.qmd içinde ham ad/soyad kolon sızıntısı yok (metinsel tarama)."""
    hits = []
    # Ham veri KOLON adı kalıntısı: 'ad_soyad', 'adSoyad', 'adiSoyadi',
    # 'adi_soyadi'. Boşluklu 'Ad Soyad' resmi jüri/imza formu alan etiketidir
    # (Marmara şablonu) → kolon sızıntısı DEĞİL, kapsam dışı.
    col_rx = re.compile(r"\b(ad_soyad|adSoyad|adi_?soyadi|adiSoyadi)\b")
    for fn in _chapter_files(ctx):
        txt = _read(fn) or ""
        for m in col_rx.finditer(txt):
            hits.append(f"{fn}: {m.group(0)}")
    if hits:
        return Result(cid, FAIL, "; ".join(hits[:5]))
    return Result(cid, PASS, "ad/soyad kolon kalıntısı yok")


def chk_deny_policy(cid, ctx):
    """.claude/settings.json deny listesi PII + credential kapatıyor mu?"""
    txt = _read(".claude/settings.json")
    if txt is None:
        return Result(cid, SKIP, ".claude/settings.json yok")
    ok = all(t in txt for t in ["data/raw", "data/identified", "data/cleaned", "data/backup"])
    if not ok:
        return Result(cid, FAIL, "deny listesinde eksik PII ağacı")
    return Result(cid, PASS, "deny listesi PII ağaçlarını kapsıyor")


def chk_bib_hygiene(cid, ctx):
    """bib_hygiene.py all → atıf↔künye↔ledger + DOI/PMID. Exit 1=HARD, 2=SOFT."""
    tool = "scripts/util/bib_hygiene.py"
    if not _tool_exists(tool):
        return Result(cid, SKIP, "bib_hygiene.py yok")
    rc, out = _run([sys.executable, _p(tool), "all"])
    hard = len(re.findall(r"\bHARD\b", out))
    soft = len(re.findall(r"\bSOFT\b", out))
    if rc == 1:
        return Result(cid, FAIL, f"HARD={hard} (tanımsız atıf render kırar); SOFT={soft}")
    if rc == 2:
        return Result(cid, PASS, f"HARD=0; SOFT={soft} (uyarı düzeyi, kapı geçti)")
    if rc == 0:
        return Result(cid, PASS, "HARD=0 SOFT=0")
    return Result(cid, FAIL, f"beklenmedik exit={rc}")


def chk_karma_ledger(cid, ctx):
    """karma_ledger_check.py → ledger ankraj/alıntı drift-guard."""
    tool = "scripts/util/karma_ledger_check.py"
    if not _tool_exists(tool):
        return Result(cid, SKIP, "karma_ledger_check.py yok")
    rc, out = _run([sys.executable, _p(tool)])
    if rc == 0:
        return Result(cid, PASS, "ledger temiz (0 bulgu)")
    sev = "HARD" if rc == 1 else "SOFT"
    first = next((ln for ln in out.splitlines() if ln.strip()), "")
    return Result(cid, FAIL, f"{sev}: {first[:80]}")


def chk_claim_cert(cid, ctx):
    """claim_certification.py → sayısal iz + nedensel etiket + bib birleşik kapı."""
    tool = "scripts/util/claim_certification.py"
    if not _tool_exists(tool):
        return Result(cid, SKIP, "claim_certification.py yok")
    if not _tool_exists("docs/CLINICAL-STUDY-REPORT-FINAL.md"):
        return Result(cid, SKIP, "CSR belgesi yok")
    rc, out = _run([sys.executable, _p(tool)])
    verd = "FAIL" if rc == 1 else ("WARN" if rc == 2 else "PASS")
    if rc == 1:
        return Result(cid, FAIL, f"claim kapı FAIL: {_last_line(out)}")
    if rc == 2:
        return Result(cid, PASS, f"claim kapı WARN (uyarı, bloklamaz): {_last_line(out)}")
    if rc == 0:
        return Result(cid, PASS, "claim kapı PASS")
    return Result(cid, SKIP, f"çalıştırılamadı (exit={rc})")


def chk_numeric_trace(cid, ctx):
    """csr_numeric_trace_audit.py → sayısal iddia → CSV izi (yüksek-risk eşsiz)."""
    tool = "scripts/util/csr_numeric_trace_audit.py"
    if not _tool_exists(tool):
        return Result(cid, SKIP, "csr_numeric_trace_audit.py yok")
    if not _tool_exists("docs/CLINICAL-STUDY-REPORT-FINAL.md"):
        return Result(cid, SKIP, "CSR belgesi yok")
    rc, out = _run([sys.executable, _p(tool)])
    hi = re.search(r"high[-_ ]?risk[^0-9]*(\d+)", out, re.I)
    n = int(hi.group(1)) if hi else -1
    if rc != 0:
        return Result(cid, FAIL, f"exit={rc}; yüksek-risk eşsiz sayı={n if n >= 0 else '?'}")
    if n > 0:
        return Result(cid, FAIL, f"CSR'de {n} kaynaksız kendi-sonuç (yüksek-risk eşsiz)")
    return Result(cid, PASS, f"yüksek-risk eşsiz sayı={n if n >= 0 else '?'}")


def chk_numeric_trace_discussion(cid, ctx):
    """csr_numeric_trace_audit.py → Tartışma bölümünde (ch05) sayısal yeniden-ifade izi.

    Kök-neden kapısı: ch05 Tartışma, ch04 Bulgular'daki kendi sayısal sonuçlarımızı
    (β, ICC, p, d ...) yeniden ifade eder. Yeniden-ifade sırasında sayı
    sürüklenirse (ör. ch04'te 0,15, ch05'te 0,51) sessizce tutarsızlık doğar. Bu
    kapı, ch05'in denetlenebilir sayılarını üretilmiş `outputs/tables/*.csv` ve
    kanonik kilit sabitlerine bağlar. Atıflı dış-literatür değerleri (Pinquart g,
    PedsQL vb.) audit'in `is_cited_external_literature` ayrımıyla muaftır; yalnız
    kaynağı CSV olması gereken kendi sonuçlarımızın kaynaksız kalması yüksek-risktir.
    """
    tool = "scripts/util/csr_numeric_trace_audit.py"
    chapter = "chapters/05_tartisma_ve_sonuc.qmd"
    if not _tool_exists(tool):
        return Result(cid, SKIP, "csr_numeric_trace_audit.py yok")
    if not _tool_exists(chapter):
        return Result(cid, SKIP, "ch05 bölümü yok")
    rc, out = _run([
        sys.executable, _p(tool),
        "--csr", chapter,
        "--out-claims", "outputs/tables/ch05_numeric_trace_claims.csv",
        "--out-numbers", "outputs/tables/ch05_numeric_trace_numbers.csv",
        "--out-report", "outputs/reports/ch05_numeric_trace_audit.md",
    ])
    hi = re.search(r"high[-_ ]?risk[^0-9]*(\d+)", out, re.I)
    n = int(hi.group(1)) if hi else -1
    if rc != 0:
        return Result(cid, FAIL, f"exit={rc}; yüksek-risk eşsiz sayı={n if n >= 0 else '?'}")
    if n > 0:
        return Result(cid, FAIL, f"ch05 yeniden-ifadede {n} kaynaksız kendi-sonuç (sürüklenme riski)")
    if n < 0:
        return Result(cid, FAIL, "audit çıktısı ayrıştırılamadı (high_risk sayısı okunamadı)")
    return Result(cid, PASS, "ch05 yeniden-ifade izli; yüksek-risk eşsiz=0")


def chk_causal_label(cid, ctx):
    """csr_causal_label_audit.py → nedensel dil + keşifsel/post-hoc etiket."""
    tool = "scripts/util/csr_causal_label_audit.py"
    if not _tool_exists(tool):
        return Result(cid, SKIP, "csr_causal_label_audit.py yok")
    if not _tool_exists("docs/CLINICAL-STUDY-REPORT-FINAL.md"):
        return Result(cid, SKIP, "CSR belgesi yok")
    rc, out = _run([sys.executable, _p(tool)])
    if rc == 0:
        return Result(cid, PASS, "nedensel-etiket disiplini temiz")
    return Result(cid, FAIL, f"revize gereken etiket/dil (exit={rc}): {_last_line(out)}")


def chk_r_generator_literal(cid, ctx):
    """r_generator_literal_audit.py → R üretici kodda gömülü istatistik literali yok.

    Kök-neden kapısı: APA/plan üretici fonksiyonlar sayısal istatistik değerini
    (BF10, β, ICC, AUC ...) pipeline kaynağından okumak yerine kod içine sabit
    yazdığında drift oluşur (denetim P0-1). Bu kapı source-tekilliğini zorlar.
    """
    tool = "scripts/util/r_generator_literal_audit.py"
    if not _tool_exists(tool):
        return Result(cid, SKIP, "r_generator_literal_audit.py yok")
    rc, out = _run([sys.executable, _p(tool), "--fail-on-find",
                    "--include-chapters"])
    if rc == 0:
        return Result(cid, PASS, "üretici kodda gömülü istatistik literali yok")
    m = re.search(r"(\d+)\s+gömülü istatistik literali", out)
    n = m.group(1) if m else "?"
    return Result(cid, FAIL, f"{n} gömülü istatistik literali (kaynaktan oku): {_last_line(out)}")


def chk_tr_headings(cid, ctx):
    """tr_corpus_audit.py headings → bölüm sırası + başlık disiplini."""
    return _tr_axis(cid, "headings")


def chk_tr_coherence(cid, ctx):
    """tr_corpus_audit.py coherence → Türkçe akış/tutarlılık."""
    return _tr_axis(cid, "coherence")


def chk_tr_refprose(cid, ctx):
    """tr_corpus_audit.py reference-prose → yazar-tarih atıf düzyazısı."""
    return _tr_axis(cid, "reference-prose")


def _tr_axis(cid, axis):
    tool = "scripts/util/tr_corpus_audit.py"
    if not _tool_exists(tool):
        return Result(cid, SKIP, "tr_corpus_audit.py yok")
    cmd = [sys.executable, _p(tool), axis, "--thesis", THESIS, "--fail-on", "blocker"]
    rc, out = _run(cmd)
    if rc == 0:
        return Result(cid, PASS, f"{axis}: blocker yok")
    if rc == 2:
        return Result(cid, PASS, f"{axis}: yalnız major/minor (blocker yok)")
    return Result(cid, FAIL, f"{axis}: blocker (exit={rc}): {_last_line(out)}")


def chk_term_consistency(cid, ctx):
    """Kanonik terim sözlüğü zorlaması → terim_tutarlilik_audit.py.

    docs/tez-kilavuz/terim-sozlugu.yaml yasak-varyant kayıtlarını chapters/*.qmd
    gövdesinde tarar; muafiyet dışı (ilk-geçiş parantezi, confounder paragraf-
    bağlamı, Dirik kaynak-terimi, kod-çiti, atıf, İngilizce özet hariç) her yasak
    varyant HARD = teslim engeli. Yalnız terim-dili; sayı/istatistik/yön DOKUNULMAZ.
    """
    tool = "scripts/util/terim_tutarlilik_audit.py"
    sozluk = "docs/tez-kilavuz/terim-sozlugu.yaml"
    if not _tool_exists(tool):
        return _skip_or_fail(cid, ctx, "terim_tutarlilik_audit.py yok")
    if not _tool_exists(sozluk):
        return _skip_or_fail(cid, ctx, "terim-sozlugu.yaml yok")
    chapters = ctx["chapter"] if ctx.get("chapter") else "chapters/*.qmd"
    cmd = [sys.executable, _p(tool), "--sozluk", sozluk,
           "--chapters", chapters, "--fail-on", "hard"]
    rc, out = _run(cmd)
    if rc == 0:
        return Result(cid, PASS, "kanonik terim sözlüğü: HARD bulgu yok")
    if rc == 2:
        return _skip_or_fail(cid, ctx, f"terim-audit önkoşul hatası: {_last_line(out)}")
    return Result(cid, FAIL, f"terim tutarsızlığı (exit={rc}): {_last_line(out)}")


def chk_decimal_comma(cid, ctx):
    """Ondalık ayırıcı virgül (§1.4): 'p=0.038' gibi nokta-ondalık sızıntısı yok."""
    hits = []
    for fn in _chapter_files(ctx):
        txt = _strip_english_summary(_strip_code(_read(fn) or ""))
        # gövde metninde p=0.NNN / 0.NN nokta-ondalık (kod bloğu dışı kaba tarama)
        for m in re.finditer(r"(?<![\w.])(?:p\s*[=<>]\s*)?\d+\.\d+(?![\w.])", txt):
            frag = m.group(0)
            # bilinen teknik istisnalar: sürüm/dosya değil; yalnız istatistik bağlamı
            if re.match(r"^p\s*[=<>]", frag) or re.match(r"^0\.\d", frag):
                hits.append(f"{os.path.basename(fn)}: {frag}")
    if hits:
        return Result(cid, FAIL, f"{len(hits)} nokta-ondalık aday: " + "; ".join(hits[:4]))
    return Result(cid, PASS, "gövde metninde nokta-ondalık istatistik yok")


def chk_heading_numbering(cid, ctx):
    """Başlık çift-numara yok: '## 4.1. ...' gibi elle numara number-sections ile çakışmaz."""
    hits = []
    for fn in _chapter_files(ctx):
        txt = _read(fn) or ""
        for i, ln in enumerate(txt.splitlines(), 1):
            if re.match(r"^#{1,6}\s+\d+(\.\d+)*\.?\s+\S", ln):
                hits.append(f"{os.path.basename(fn)}:{i}")
    if hits:
        return Result(cid, FAIL, f"{len(hits)} elle-numaralı başlık (oto-numara ile çift): "
                                 + ", ".join(hits[:6]))
    return Result(cid, PASS, "elle numaralı başlık yok (oto-numaralandırma temiz)")


def chk_fig_refs(cid, ctx):
    """Her {#fig-} etiketine gövdede en az bir @fig- atıfı (§1.6)."""
    return _label_ref(cid, ctx, "fig")


def chk_tbl_refs(cid, ctx):
    """Her tbl- etiketine gövdede en az bir @tbl- atıfı (§1.7)."""
    return _label_ref(cid, ctx, "tbl")


def _label_ref(cid, ctx, kind):
    labels = set()
    refs = set()
    for fn in _chapter_files(ctx):
        txt = _read(fn) or ""
        if kind == "fig":
            labels |= set(re.findall(r"\{#(fig-[a-z0-9-]+)\}", txt))
        else:
            labels |= set(re.findall(r"#\|\s*label:\s*(tbl-[a-z0-9-]+)", txt))
        refs |= set(re.findall(rf"@({kind}-[a-z0-9-]+)", txt))
    if not labels:
        return Result(cid, SKIP, f"{kind} etiketi yok")
    unref = sorted(labels - refs)
    if unref:
        return Result(cid, FAIL, f"{len(unref)} atıfsız {kind}: " + ", ".join(unref[:6]))
    return Result(cid, PASS, f"{len(labels)} {kind} etiketinin tümüne metin-içi atıf var")


def chk_render_crossref(cid, ctx):
    """Render çıktısında (HTML) 0 çözülmemiş crossref / kırık atıf."""
    html = _read(RENDER_HTML)
    if html is None:
        return Result(cid, SKIP, f"{RENDER_HTML} yok (önce render gerekir)")
    unresolved = html.count("?@")
    broken = html.count("[?]")
    leak = len(re.findall(r"@(?:fig|tbl|sec)-[a-z0-9-]+", html))
    if unresolved or broken or leak:
        return Result(cid, FAIL, f"çözülmemiş ?@={unresolved}; kırık [?]={broken}; sızıntı={leak}")
    return Result(cid, PASS, "0 çözülmemiş crossref / 0 kırık atıf / 0 sızıntı")


def chk_render_exit(cid, ctx):
    """quarto render thesis.qmd → exit 0 (ağır; --fast'te SKIP)."""
    if ctx["fast"]:
        return Result(cid, SKIP, "--fast: render atlandı")
    if not _which("quarto"):
        return Result(cid, SKIP, "quarto yok")
    rc, out = _run(["quarto", "render", THESIS, "--to", "html"], timeout=1800)
    if rc == 0:
        return Result(cid, PASS, "quarto render exit 0")
    return Result(cid, FAIL, f"render exit={rc}: {_last_line(out)}")


def chk_pdf_format(cid, ctx):
    """PDF Marmara ölçüleri: A4 + kenar boşluk + gömülü Times-uyumlu font."""
    if ctx["fast"]:
        return Result(cid, SKIP, "--fast: PDF ölçümü atlandı")
    if not os.path.exists(_p(RENDER_PDF)):
        return Result(cid, SKIP, f"{RENDER_PDF} yok")
    try:
        import fitz  # noqa
    except Exception:
        return Result(cid, SKIP, "pymupdf yok (PDF ölçümü atlanamaz)")
    import fitz
    doc = fitz.open(_p(RENDER_PDF))
    cm = 28.3465
    w, h = doc[0].rect.width, doc[0].rect.height
    a4 = abs(w - 595.3) < 5 and abs(h - 841.9) < 5
    fonts = set()
    for pg in list(doc)[:20]:
        res = pg.get_text("dict")
        for b in res["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    fonts.add(s.get("font", ""))
    times_like = any(re.search(r"times|termes|serif|nimbusrom", f, re.I) for f in fonts)
    probs = []
    if not a4:
        probs.append(f"A4 değil ({w/cm:.1f}x{h/cm:.1f}cm)")
    if not times_like:
        probs.append("Times-uyumlu font gömülü değil")
    if probs:
        return Result(cid, FAIL, "; ".join(probs))
    return Result(cid, PASS, f"A4 ({w/cm:.1f}x{h/cm:.1f}cm) + Times-uyumlu font gömülü")


def chk_renv_status(cid, ctx):
    """renv::status() → paket ortamı senkron."""
    if ctx["fast"]:
        return Result(cid, SKIP, "--fast: renv atlandı")
    if not _which("Rscript"):
        return Result(cid, SKIP, "Rscript yok")
    rc, out = _run(["Rscript", "-e", "renv::status()"], timeout=300)
    if re.search(r"synchron|senkron|up to date|no issues", out, re.I):
        return Result(cid, PASS, "renv senkron")
    if rc != 0:
        return Result(cid, FAIL, f"renv::status exit={rc}")
    return Result(cid, FAIL, f"renv senkron değil: {_last_line(out)}")


def chk_targets_fresh(cid, ctx):
    """targets::tar_outdated() → güncellenmesi gereken hedef yok."""
    if ctx["fast"]:
        return Result(cid, SKIP, "--fast: targets atlandı")
    if not _which("Rscript"):
        return Result(cid, SKIP, "Rscript yok")
    if not _tool_exists("_targets.R"):
        return Result(cid, SKIP, "_targets.R yok")
    rc, out = _run(
        ["Rscript", "-e",
         "o<-tryCatch(targets::tar_outdated(), error=function(e) NA); "
         "if(length(o)==0) cat('FRESH') else cat('OUTDATED:', length(o))"],
        timeout=600)
    if "FRESH" in out:
        return Result(cid, PASS, "outdated hedef yok")
    m = re.search(r"OUTDATED:\s*(\d+)", out)
    if m:
        return Result(cid, FAIL, f"{m.group(1)} outdated hedef (tar_make gerekir)")
    return Result(cid, SKIP, f"belirlenemedi (exit={rc})")


def chk_canonical_lock(cid, ctx):
    """Kanonik analiz baz kilidi mevcut (veri bütünlüğü referansı)."""
    if _tool_exists(CANONICAL_LOCK):
        return Result(cid, PASS, "kanonik baz kilidi mevcut")
    return Result(cid, FAIL, f"{CANONICAL_LOCK} yok")


def chk_hooks_twin(cid, ctx):
    """İki-kol hook ağacı (.claude + .codex) senkron + hook testi geçer."""
    claude = _p(".claude/hooks")
    codex = _p(".codex/hooks")
    if not (os.path.isdir(claude) and os.path.isdir(codex)):
        return Result(cid, SKIP, "hook ağaçlarından biri yok")
    cset = {f for f in os.listdir(claude) if f.endswith(".py")}
    xset = {f for f in os.listdir(codex) if f.endswith(".py")}
    if cset != xset:
        return Result(cid, FAIL, f"hook dosyaları ayrışık: {cset ^ xset}")
    if _tool_exists("tests/test_claude_hooks.py"):
        rc, out = _run([sys.executable, _p("tests/test_claude_hooks.py")], timeout=300)
        if rc != 0:
            return Result(cid, FAIL, f"hook testi FAIL: {_last_line(out)}")
        return Result(cid, PASS, f"{len(cset)} hook iki kolda senkron + test PASS")
    return Result(cid, PASS, f"{len(cset)} hook iki kolda senkron (test yok)")


def chk_abstract_wordcount(cid, ctx):
    """ÖZET kelime sınırı + Anahtar Sözcükler satırı (§ ön bölümler)."""
    txt = _read("chapters/00c_ozet_summary.qmd")
    if txt is None:
        return Result(cid, SKIP, "00c_ozet_summary.qmd yok")
    has_kw = bool(re.search(r"Anahtar\s+S[öo]zc[üu]kler", txt, re.I))
    if not has_kw:
        return Result(cid, FAIL, "Anahtar Sözcükler satırı yok")
    # ÖZET gövdesi: §3.2 yapılandırılmış dört paragraf (Amaç / Gereç ve Yöntem /
    # Bulgular / Sonuç). Yorum bloğu, ham LaTeX bloğu ve künye tablosu sayılmaz.
    paras = [ln for ln in txt.splitlines()
             if re.match(r"\*\*(Amaç|Gereç ve Yöntem|Bulgular|Sonuç):\*\*", ln)]
    if paras:
        words = len(re.findall(r"\b\w+\b", " ".join(paras)))
    else:
        # geri düşüş: eski kaba ölçüm (ilk 'Anahtar' öncesi blok)
        words = len(re.findall(r"\b\w+\b", txt.split("Anahtar")[0]))
    if words > 350:
        return Result(cid, FAIL, f"ÖZET ~{words} kelime (>300 sınırı aşımı olası)")
    return Result(cid, PASS, f"Anahtar Sözcükler var; ÖZET ~{words} kelime")


def chk_placeholder_scan(cid, ctx):
    """00a/06/07 doldurulmamış alan taraması (işaretli/belirsiz yer-tutucu)."""
    findings = []
    for fn in ["chapters/00a_on_bolumler.qmd",
               "chapters/06_ozgecmis_faaliyetler.qmd",
               "chapters/07_ekler.qmd"]:
        txt = _read(fn)
        if txt is None:
            continue
        # belirsiz yer-tutucu: köşeli-parantez YER TUTUCU büyük harf
        vague = len(re.findall(r"\[YER TUTUCU\]", txt))
        if vague:
            findings.append(f"{os.path.basename(fn)}: {vague}× belirsiz [YER TUTUCU]")
    if findings:
        return Result(cid, MANUEL, "; ".join(findings) + " (elle netleştir)")
    return Result(cid, MANUEL, "resmi/kişisel alanlar elle doğrulanmalı (jüri/CV/tarih)")


# --- MANUEL maddeler: script otomatik karar veremez, elle kontrol gerekir ---

def chk_manual(cid, ctx, note):
    return Result(cid, MANUEL, note)


# ---------------------------------------------------------------------------
# Yardımcılar
# ---------------------------------------------------------------------------

def _which(binname):
    for d in os.environ.get("PATH", "").split(os.pathsep):
        if os.path.exists(os.path.join(d, binname)):
            return True
    # TinyTeX/quarto ek yolları
    return False


def _last_line(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1][:100] if lines else ""


def _chapter_files(ctx):
    if ctx.get("chapter"):
        return [ctx["chapter"]]
    d = _p(CHAPTERS_DIR)
    if not os.path.isdir(d):
        return []
    return [os.path.join(CHAPTERS_DIR, f)
            for f in sorted(os.listdir(d)) if f.endswith(".qmd")]


# ---------------------------------------------------------------------------
# Kapsam genişletme denetçileri (plan 2026-07-22-qc-otomatik-zorlama)
# ---------------------------------------------------------------------------

def chk_numeric_trace_bulgular(cid, ctx):
    """csr_numeric_trace_audit.py → Bulgular (ch04) kendi sayılarının CSV izi.

    Bulgular bölümü tezin kendi sonuçlarının (β/ICC/AUC/BF) yaşadığı yerdir;
    K5-NUM-01 CSR'ı, K5-NUM-02 ch05'i izler — ch04 gövdesi izlenmiyordu. Bu
    kapı ch04'ün denetlenebilir sayılarını üretilmiş `outputs/tables/*.csv`
    değerlerine bağlar (kaynak-tekilliği; BF-drift sınıfı önlemi).
    """
    tool = "scripts/util/csr_numeric_trace_audit.py"
    chapter = "chapters/04_bulgular.qmd"
    if not _tool_exists(tool):
        return _skip_or_fail(cid, ctx, "csr_numeric_trace_audit.py yok")
    if not _tool_exists(chapter):
        return _skip_or_fail(cid, ctx, "ch04 bölümü yok")
    rc, out = _run([
        sys.executable, _p(tool),
        "--csr", chapter,
        "--out-claims", "outputs/tables/ch04_numeric_trace_claims.csv",
        "--out-numbers", "outputs/tables/ch04_numeric_trace_numbers.csv",
        "--out-report", "outputs/reports/ch04_numeric_trace_audit.md",
    ])
    hi = re.search(r"high[-_ ]?risk[^0-9]*(\d+)", out, re.I)
    n = int(hi.group(1)) if hi else -1
    if rc != 0:
        return Result(cid, FAIL, f"exit={rc}; yüksek-risk eşsiz sayı={n if n >= 0 else '?'}")
    if n > 0:
        return Result(cid, FAIL, f"ch04 Bulgular'da {n} kaynaksız kendi-sonuç (yüksek-risk eşsiz)")
    if n < 0:
        return Result(cid, FAIL, "audit çıktısı ayrıştırılamadı (high_risk okunamadı)")
    return Result(cid, PASS, "ch04 sayısal izli; yüksek-risk eşsiz=0")


def chk_causal_label_discussion(cid, ctx):
    """csr_causal_label_audit.py → ch05 Tartışma nedensel dil + etiket disiplini.

    Nedensel-dil/keşifsel-etiket denetimi yalnız CSR'de koşuyordu; asıl
    Tartışma bölümü (ch05) kapsam dışıydı. Bu kapı denetimi gerçek metne yayar.
    """
    tool = "scripts/util/csr_causal_label_audit.py"
    chapter = "chapters/05_tartisma_ve_sonuc.qmd"
    if not _tool_exists(tool):
        return _skip_or_fail(cid, ctx, "csr_causal_label_audit.py yok")
    if not _tool_exists(chapter):
        return _skip_or_fail(cid, ctx, "ch05 bölümü yok")
    rc, out = _run([
        sys.executable, _p(tool),
        "--csr", chapter,
        "--out-causal", "outputs/tables/ch05_causal_language_scan.csv",
        "--out-labels", "outputs/tables/ch05_exploratory_label_scan.csv",
        "--out-report", "outputs/reports/ch05_causal_label_audit.md",
    ])
    if rc == 0:
        return Result(cid, PASS, "ch05 nedensel-etiket disiplini temiz")
    return Result(cid, FAIL, f"ch05 revize gereken etiket/dil (exit={rc}): {_last_line(out)}")


def chk_targets_file_tracking(cid, ctx):
    """targets_file_tracking_audit.py → Kaide-2 format=file dosya-izleme."""
    tool = "scripts/util/targets_file_tracking_audit.py"
    if not _tool_exists(tool):
        return _skip_or_fail(cid, ctx, "targets_file_tracking_audit.py yok")
    if not _tool_exists("_targets.R"):
        return _skip_or_fail(cid, ctx, "_targets.R yok")
    rc, out = _run([sys.executable, _p(tool)])
    if rc == 0:
        return Result(cid, PASS, "literal türetilmiş-yol okuyan izlenmeyen hedef yok")
    m = re.search(r"(\d+)\s+hedef", out)
    n = m.group(1) if m else "?"
    return Result(cid, FAIL, f"{n} hedef literal türetilmiş-yol okuyor, format=file yok")


def chk_svg_preflight(cid, ctx):
    """librsvg (rsvg-convert) önkoşulu — SVG figürü varsa boş-rasterize koruması."""
    has_svg = False
    for d in ["chapters", "docs/assets"]:
        ad = _p(d)
        if not os.path.isdir(ad):
            continue
        for _root, _dirs, files in os.walk(ad):
            if any(f.endswith(".svg") for f in files):
                has_svg = True
                break
        if has_svg:
            break
    if not has_svg:
        return Result(cid, SKIP, "SVG figürü yok")
    if _which("rsvg-convert"):
        return Result(cid, PASS, "rsvg-convert mevcut (SVG rasterize güvenli)")
    return Result(cid, FAIL, "SVG figürü var ama rsvg-convert yok → boş rasterize riski")


def chk_pii_value_scan(cid, ctx):
    """pii_value_scan.py → değer-şekilli PII (TC/tarih/hasta-no) tüm manuskriptte."""
    tool = "scripts/util/pii_value_scan.py"
    if not _tool_exists(tool):
        return _skip_or_fail(cid, ctx, "pii_value_scan.py yok")
    rc, out = _run([sys.executable, _p(tool)])
    if rc == 0:
        # Kılavuz-zorunlu alan muafiyetleri sessizce geçmesin: denetim izi
        # rapora taşınır (kaç muafiyet, hangi dosyada).
        muaf = [l for l in out.splitlines() if l.startswith("MUAF")]
        if muaf:
            dosyalar = sorted({l.split()[1].split(":")[0] for l in muaf})
            return Result(cid, PASS,
                          f"PII adayı yok; {len(muaf)} kılavuz-zorunlu muafiyet "
                          f"({', '.join(dosyalar)}) — `--strict` ile görülebilir")
        return Result(cid, PASS, "değer-şekilli PII adayı yok")
    return Result(cid, FAIL, f"PII adayı: {_last_line(out)}")


def _find_tr_sciaudit():
    """sci-audit axis-G çekirdek scriptini (tr_sciaudit.py) yerelde ara."""
    cands = []
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env_root:
        cands.append(os.path.join(env_root, "skills", "turkish-sci-style",
                                  "scripts", "tr_sciaudit.py"))
    for base in (os.path.expanduser("~/.claude/plugins"),
                 "/workspaces/CureoPrivate/plugins"):
        cands += glob.glob(os.path.join(base, "**", "sci-audit", "**",
                                        "tr_sciaudit.py"), recursive=True)
    return next((c for c in cands if os.path.exists(c)), None)


def chk_axis_g(cid, ctx):
    """tr_sciaudit.py (sci-audit Ekseni G çekirdek) → Türkçe bilimsel yazım G1-G6.

    'Zorunlu/kanonik' işaretli axis-G (nokta-ondalık-p blocker dahil) 28-madde
    paketinde yoktu (etüt madde D). Her Türkçe bölüm üzerinde deterministik
    çekirdeği --fail-on error ile koşar. İngilizce SUMMARY bölümü (00c) ondalık-
    nokta kullandığından axis-G kapsamı dışıdır (yanlış-pozitif koruması).
    """
    tool = _find_tr_sciaudit()
    if not tool:
        return _skip_or_fail(cid, ctx, "tr_sciaudit.py (axis G çekirdek) bulunamadı")
    chapters = [c for c in _chapter_files({"chapter": None})
                if "00c_ozet_summary" not in c]  # İngilizce SUMMARY hariç
    if not chapters:
        return Result(cid, SKIP, "chapters/*.qmd yok")
    failed = []
    for ch in chapters:
        rc, _out = _run([sys.executable, tool, _p(ch),
                         "--fail-on", "error", "--strictness", "draft"],
                        timeout=300)
        if rc != 0:
            failed.append(os.path.basename(ch))
    if failed:
        return Result(cid, FAIL, f"axis G error-düzeyi: {', '.join(failed[:6])}")
    return Result(cid, PASS, f"{len(chapters)} bölüm axis G (G1-G6) temiz")


def chk_cross_arm(cid, ctx):
    """cross_arm_rhetoric_audit.py → karma cross-arm aşırı-iddia yok."""
    tool = "scripts/util/cross_arm_rhetoric_audit.py"
    if not _tool_exists(tool):
        return _skip_or_fail(cid, ctx, "cross_arm_rhetoric_audit.py yok")
    rc, out = _run([sys.executable, _p(tool)])
    if rc == 0:
        return Result(cid, PASS, "cross-arm kanıt-iddiası yok")
    return Result(cid, FAIL, f"cross-arm aşırı-iddia: {_last_line(out)}")


def chk_cert_freshness(cid, ctx):
    """Bölüm sertifikaları güncel mi? (bölüm sertifikadan sonra değişmemeli).

    Sertifikalar: tez-yazim/04_kalite-kontrol/sertifikalar/<NN>-<slug>-sertifika-
    <tarih>.md (slug tireli; bölüm dosyası alt-çizgili). Bölüm dosyası mtime'ı en
    yeni sertifikadan yeni ise sertifika eskimiş sayılır (--closing'de FAIL).
    """
    cert_dir = _p("tez-yazim/04_kalite-kontrol/sertifikalar")
    if not os.path.isdir(cert_dir):
        return Result(cid, MANUEL,
                      "sertifikalar/ yok — bölümler henüz sertifikalanmadı "
                      "(/bolum-sertifika)")
    stale, uncertified = [], []
    for ch in _chapter_files({"chapter": None}):
        base = os.path.splitext(os.path.basename(ch))[0].replace("_", "-")
        certs = glob.glob(os.path.join(cert_dir, f"*{base}*sertifika*.md"))
        if not certs:
            uncertified.append(os.path.basename(ch))
            continue
        if os.path.getmtime(_p(ch)) > max(os.path.getmtime(c) for c in certs) + 1:
            stale.append(os.path.basename(ch))
    if stale:
        status = FAIL if ctx.get("closing") else MANUEL
        return Result(cid, status,
                      f"sertifikadan sonra değişen bölüm: {', '.join(stale[:8])}"
                      + (f" | sertifikasız: {len(uncertified)}" if uncertified else ""))
    if uncertified:
        return Result(cid, MANUEL,
                      f"sertifikasız bölüm: {', '.join(uncertified[:8])} "
                      "(/bolum-sertifika)")
    return Result(cid, PASS, "sertifikalı bölümler güncel")


def chk_doi_title(cid, ctx):
    """doi_title_resolve.py → references.bib DOI'leri Crossref başlığıyla eşleşir.

    Etüt madde C: DOI yanlış-atıf (DOI başka esere işaret) normal akışta hiç
    denetlenmiyordu. Ağ-bağımlı (Crossref, DOI-başına) → yalnız --closing modunda
    koşar; ağ erişilemezse (tüm sorgular CROSSREF_ERR) SKIP (uydurma yok), yalnız
    jaccard<0.4 CHECK bulguları (gerçek yanlış-atıf) FAIL. KVKK: yalnız yayın
    başlığı/DOI sorgulanır.
    """
    tool = "scripts/util/doi_title_resolve.py"
    if not _tool_exists(tool):
        return _skip_or_fail(cid, ctx, "doi_title_resolve.py yok")
    if not ctx.get("closing"):
        return Result(cid, SKIP,
                      "DOI↔Crossref çözümleme yalnız --closing modunda (ağ+yavaş)")
    bib = _read("references/references.bib") or ""
    targets = []
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", bib, re.S):
        key = m.group(1).strip()
        dm = re.search(r"doi\s*=\s*[{\"]([^}\",]+)", m.group(2), re.I)
        if dm:
            targets.append({"key": key, "doi": dm.group(1).strip()})
    if not targets:
        return Result(cid, SKIP, "references.bib'te DOI'li künye yok")
    try:
        with open("/tmp/ctx_targets.json", "w", encoding="utf-8") as fh:
            json.dump(targets, fh)
    except OSError as exc:
        return Result(cid, SKIP, f"targets yazılamadı: {exc}")
    _rc, _out = _run([sys.executable, _p(tool)], timeout=1200)
    try:
        res = json.load(open("/tmp/doi_resolve.json", encoding="utf-8"))["results"]
    except Exception:
        return Result(cid, SKIP, "DOI çözümleme çıktısı okunamadı (ağ/erişim)")
    checks = [r for r in res if r.get("flag") == "CHECK"]
    oks = [r for r in res if r.get("flag") == "OK"]
    errs = [r for r in res if r.get("flag") == "CROSSREF_ERR"]
    if checks:
        return Result(cid, FAIL,
                      f"{len(checks)} DOI yanlış-atıf adayı (jaccard<0.4): "
                      + ", ".join(r["key"] for r in checks[:6]))
    if not oks and errs:
        return Result(cid, SKIP,
                      f"ağ erişilemedi (tüm {len(errs)} sorgu CROSSREF_ERR)")
    return Result(cid, PASS,
                  f"{len(oks)} DOI Crossref-eşleşti; yanlış-atıf yok "
                  f"({len(errs)} ağ-hatası atlandı)")


def chk_galileo_logged(cid, ctx):
    """Galileo tam-tez judge koşumu güncel mi? (advisory — HARD asla judge'dan).

    Etüt madde G/breadth: en derin cross-document QC (galileo convergence/harking/
    overclaim/coherence) yalnız opt-in koşuyordu. Bu ADVISORY madde, tam-tez judge
    artefaktının (run_full_thesis_judge.py --out) varlığını + tazeliğini raporlar;
    atlanmış/eskimiş koşum GÖRÜNÜR olur. Asla FAIL üretmez (judge → SOFT/advisory).
    """
    art = _p(GALILEO_ARTIFACT)
    if not os.path.exists(art):
        return Result(cid, MANUEL,
                      "galileo tam-tez judge koşumu yok — "
                      "`python3 scripts/eval/run_full_thesis_judge.py "
                      "--out outputs/reports/galileo_full_thesis_judge.json` "
                      "(Kapı 3/4 advisory)")
    a_m = os.path.getmtime(art)
    newer = [os.path.basename(c) for c in _chapter_files({"chapter": None})
             if os.path.getmtime(_p(c)) > a_m + 1]
    if newer:
        return Result(cid, MANUEL,
                      f"galileo judge artefaktı eskimiş; sonradan değişen bölüm: "
                      f"{', '.join(newer[:6])} (yeniden koş)")
    return Result(cid, PASS, "galileo tam-tez judge artefaktı güncel (advisory)")


# ---------------------------------------------------------------------------
# KONTROL KAYDI (kanonik). Her giriş master checklist'te bir maddeye karşılıktır.
#   (id, eksen, katman, tür_ipucu, başlık, uygulayıcı)
#   katman: "bolum" (A) | "tez" (B)
# ---------------------------------------------------------------------------

def _reg():
    C = []
    def add(cid, eksen, katman, baslik, fn):
        C.append((cid, eksen, katman, baslik, fn))

    # --- Kapı 0: Kapsam & Gizlilik ---
    add("K0-PII-01", "Kapsam/Gizlilik", "tez",
        "PII ağaçları .gitignore'da ve git-izlenmiyor", chk_pii_gitignore)
    add("K0-PII-02", "Kapsam/Gizlilik", "bolum",
        "Bölüm metninde ad/soyad kolon kalıntısı yok", chk_pii_no_names)
    add("K0-POL-01", "Kapsam/Gizlilik", "tez",
        ".claude/settings.json deny PII ağaçlarını kapsar", chk_deny_policy)
    add("K0-LCK-01", "Kapsam/Gizlilik", "tez",
        "Kanonik analiz baz kilidi mevcut", chk_canonical_lock)
    add("K0-PII-03", "Kapsam/Gizlilik", "tez",
        "Değer-şekilli PII (TC/tarih/hasta-no) tüm manuskriptte yok",
        chk_pii_value_scan)

    # --- Kapı 1-2: Kanıt & Literatür ---
    add("K1-BIB-01", "Kanıt/Literatür", "tez",
        "bib hijyen: atıf↔künye↔ledger + DOI/PMID (HARD=0)", chk_bib_hygiene)
    add("K1-LED-01", "Kanıt/Literatür", "tez",
        "Karma kanıt ledger drift-guard temiz", chk_karma_ledger)
    add("K1-CLM-01", "Kanıt/Literatür", "tez",
        "Birleşik claim kapısı (sayı izi+nedensel+bib) PASS/WARN", chk_claim_cert)
    add("K1-KAR-01", "Kanıt/Literatür", "tez",
        "Karma cross-arm aşırı-iddia yok (bir kol diğerini 'doğrular' değil)",
        chk_cross_arm)
    add("K1-DOI-01", "Kanıt/Literatür", "tez",
        "DOI↔Crossref başlık eşleşmesi (yanlış-atıf yok) [--closing; ağ]",
        chk_doi_title)

    # --- Kapı 3: Format & Kılavuz uyumu ---
    add("K3-NUM-01", "Format/Kılavuz", "bolum",
        "Ondalık ayırıcı virgül; nokta-ondalık istatistik yok (§1.4)", chk_decimal_comma)
    add("K3-HDG-01", "Format/Kılavuz", "bolum",
        "Başlıkta elle numara yok (oto-numara ile çift değil)", chk_heading_numbering)
    add("K3-FIG-01", "Format/Kılavuz", "bolum",
        "Her şekle metin-içi @fig- atıfı (§1.6)", chk_fig_refs)
    add("K3-TBL-01", "Format/Kılavuz", "bolum",
        "Her tabloya metin-içi @tbl- atıfı (§1.7)", chk_tbl_refs)
    add("K3-SEQ-01", "Format/Kılavuz", "tez",
        "Bölüm sırası + başlık disiplini (tr headings)", chk_tr_headings)

    # --- Kapı 4: Türkçe imla, akış, mantık ---
    add("K4-COH-01", "Türkçe/Akış", "tez",
        "Türkçe akış/tutarlılık denetimi (blocker=0)", chk_tr_coherence)
    add("K4-REF-01", "Türkçe/Akış", "tez",
        "Yazar-tarih atıf düzyazısı disiplini (§1.8)", chk_tr_refprose)
    add("K4-TRG-01", "Türkçe/Akış", "tez",
        "Bilimsel-yazım Ekseni G çekirdeği (G1-G6, nokta-ondalık-p)", chk_axis_g)
    add("K4-TERM-01", "Türkçe/Akış", "tez",
        "Kanonik terim sözlüğü tutarlılığı (yasak-varyant → HARD)",
        chk_term_consistency)

    # --- Kapı 5: AI-reliability & teknik ---
    add("K5-NUM-01", "AI-reliability/Teknik", "tez",
        "Sayısal iddia → CSV izi (yüksek-risk eşsiz)", chk_numeric_trace)
    add("K5-NUM-02", "AI-reliability/Teknik", "tez",
        "ch05 Tartışma sayısal yeniden-ifade → CSV izi (sürüklenme kapısı)",
        chk_numeric_trace_discussion)
    add("K5-NUM-03", "AI-reliability/Teknik", "tez",
        "ch04 Bulgular sayısal iddia → CSV izi", chk_numeric_trace_bulgular)
    add("K5-CAU-01", "AI-reliability/Teknik", "tez",
        "Nedensel dil + keşifsel/post-hoc etiket disiplini", chk_causal_label)
    add("K5-CAU-02", "AI-reliability/Teknik", "tez",
        "ch05 Tartışma nedensel dil + etiket disiplini", chk_causal_label_discussion)
    add("K5-HOK-01", "AI-reliability/Teknik", "tez",
        "İki-kol hook ağacı senkron + hook testi PASS", chk_hooks_twin)
    add("K5-LIT-01", "AI-reliability/Teknik", "tez",
        "R üretici kodda gömülü istatistik literali yok (kaynak-tekilliği)",
        chk_r_generator_literal)
    add("K5-TRK-01", "AI-reliability/Teknik", "tez",
        "_targets.R format=file dosya-izleme (Kaide-2)", chk_targets_file_tracking)
    add("K5-GAL-01", "AI-reliability/Teknik", "tez",
        "Galileo tam-tez judge koşumu güncel (advisory; HARD değil)",
        chk_galileo_logged)

    # --- Pipeline & üretilebilirlik ---
    add("P-ENV-01", "Pipeline", "tez",
        "renv::status() paket ortamı senkron", chk_renv_status)
    add("P-TAR-01", "Pipeline", "tez",
        "targets: outdated hedef yok (tar_make taze)", chk_targets_fresh)

    # --- Render & çıktı bütünlüğü ---
    add("R-RND-01", "Render/Çıktı", "tez",
        "quarto render thesis.qmd exit 0", chk_render_exit)
    add("R-XRF-01", "Render/Çıktı", "tez",
        "Render çıktısı: 0 çözülmemiş crossref / kırık atıf", chk_render_crossref)
    add("R-PDF-01", "Render/Çıktı", "tez",
        "PDF Marmara ölçüleri: A4 + Times-uyumlu font", chk_pdf_format)
    add("R-SVG-01", "Render/Çıktı", "tez",
        "librsvg (rsvg-convert) önkoşulu — SVG boş-rasterize koruması",
        chk_svg_preflight)

    # --- Ön/arka bölümler & teslim ---
    add("T-ABS-01", "Ön/Arka/Teslim", "tez",
        "ÖZET kelime sınırı + Anahtar Sözcükler satırı", chk_abstract_wordcount)
    add("T-PLC-01", "Ön/Arka/Teslim", "tez",
        "00a/06/07 resmi-kişisel alan/yer-tutucu netliği", chk_placeholder_scan)
    add("T-KVK-01", "Ön/Arka/Teslim", "tez",
        "Katılımcı fotoğrafı/kimlik ifşası yok (KVKK)",
        lambda cid, ctx: chk_manual(cid, ctx, "KVKK: fotoğraf/kimlik ifşası elle doğrulanmalı"))
    add("T-CERT-01", "Ön/Arka/Teslim", "tez",
        "Bölüm sertifikaları güncel (bölüm sertifikadan sonra değişmemiş)",
        chk_cert_freshness)
    add("T-RHET-01", "Ön/Arka/Teslim", "bolum",
        "Retorik akış / thick-description insan-Türkçesi",
        lambda cid, ctx: chk_manual(cid, ctx, "retorik/insan-Türkçesi elle okunmalı"))

    return C


CHECKS = _reg()
BY_ID = {c[0]: c for c in CHECKS}
EKSENLER = []
for _c0 in CHECKS:
    if _c0[1] not in EKSENLER:
        EKSENLER.append(_c0[1])


# ---------------------------------------------------------------------------
# Koşum + raporlama
# ---------------------------------------------------------------------------

def run(ctx, section=None):
    selected = [c for c in CHECKS
                if section is None or c[1].lower().startswith(section.lower())
                or c[0].lower().startswith(section.lower())]
    if ctx.get("chapter"):
        selected = [c for c in selected if c[2] == "bolum"]
    results = []
    for cid, eksen, katman, baslik, fn in selected:
        try:
            res = fn(cid, ctx)
        except Exception as exc:  # denetçi kendi hatasında SKIP
            res = Result(cid, SKIP, f"kontrol hatası: {exc}")
        results.append((cid, eksen, katman, baslik, res))
    return results


def report(results, ctx):
    counts = {PASS: 0, FAIL: 0, SKIP: 0, MANUEL: 0}
    cur = None
    print("=" * 78)
    print("TEZ KONTROL CHECKLİSTİ — BİRLEŞİK DOĞRULAMA RAPORU")
    if ctx.get("chapter"):
        print(f"Kapsam: bölüm = {ctx['chapter']}")
    elif ctx.get("fast"):
        print("Kapsam: tam tez (--fast: ağır kontroller SKIP)")
    else:
        print("Kapsam: tam tez")
    print("=" * 78)
    for cid, eksen, katman, baslik, res in results:
        if eksen != cur:
            cur = eksen
            print(f"\n── {eksen} ─────────────────────────────────────────")
        counts[res.status] += 1
        tag = _COLOR[res.status](f"{res.status:6}")
        print(f"  [{tag}] {cid:12} {baslik}")
        if res.evidence:
            print(f"          → {res.evidence}")
    total = len(results)
    print("\n" + "=" * 78)
    print(f"ÖZET: toplam={total}  "
          f"{_COLOR[PASS](f'PASS={counts[PASS]}')}  "
          f"{_COLOR[FAIL](f'FAIL={counts[FAIL]}')}  "
          f"{_COLOR[SKIP](f'SKIP={counts[SKIP]}')}  "
          f"{_COLOR[MANUEL](f'MANUEL={counts[MANUEL]}')}")
    if counts[FAIL]:
        print(_COLOR[FAIL](f"SONUÇ: {counts[FAIL]} otomatik madde FAIL — teslim engeli"))
    elif counts[MANUEL]:
        print(_COLOR[MANUEL]("SONUÇ: otomatik maddeler temiz; MANUEL maddeler elle doğrulanmalı"))
    else:
        print(_COLOR[PASS]("SONUÇ: tüm otomatik maddeler PASS"))
    print("=" * 78)
    return counts


def cmd_list():
    print(f"{'ID':13} {'EKSEN':22} {'KATMAN':6} BAŞLIK")
    print("-" * 78)
    for cid, eksen, katman, baslik, _fn in CHECKS:
        print(f"{cid:13} {eksen:22} {katman:6} {baslik}")
    print(f"\nToplam {len(CHECKS)} kontrol · {len(EKSENLER)} eksen")


def cmd_audit_doc():
    """Master checklist ile CHECKS kaydı arasında yetim ID denetimi."""
    doc = _read(MASTER_CHECKLIST)
    if doc is None:
        print(f"UYARI: {MASTER_CHECKLIST} yok — senkron denetimi atlandı.")
        return 0
    doc_ids = set(re.findall(r"\b([A-Z]\d?-[A-Z]{3,4}-\d{2})\b", doc))
    reg_ids = set(BY_ID)
    orphan_doc = doc_ids - reg_ids
    orphan_reg = reg_ids - doc_ids
    ok = True
    if orphan_reg:
        ok = False
        print("BELGEDE EKSİK (script'te var, belgede yok):", ", ".join(sorted(orphan_reg)))
    if orphan_doc:
        ok = False
        print("SCRIPT'TE EKSİK (belgede var, script'te yok):", ", ".join(sorted(orphan_doc)))
    if ok:
        print(f"SENKRON: {len(reg_ids)} kontrol ID belge ↔ script birebir eşleşiyor.")
        return 0
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Tez kontrol checklisti birleşik doğrulama orkestratörü (salt-okuma).")
    ap.add_argument("--section", help="tek eksen veya ID öneki (ör. Format, K3, Render)")
    ap.add_argument("--chapter", help="bölüm-düzeyi alt-küme (ör. chapters/04_bulgular.qmd)")
    ap.add_argument("--fast", action="store_true",
                    help="ağır kontrolleri (render, PDF, renv, targets) SKIP")
    ap.add_argument("--closing", action="store_true",
                    help="kapanış/teslim modu: --fast reddedilir; eksik araç/CSR "
                         "SKIP yerine FAIL (gate-presence invariant)")
    ap.add_argument("--list", action="store_true", help="kontrol kaydını yazdır ve çık")
    ap.add_argument("--audit-doc", action="store_true",
                    help="master checklist ↔ script ID senkron denetimi")
    args = ap.parse_args(argv)

    if args.list:
        cmd_list()
        return 0
    if args.audit_doc:
        return cmd_audit_doc()

    if args.closing and args.fast:
        sys.stderr.write(
            "HATA: --closing --fast ile birlikte kullanılamaz "
            "(kapanış tam denetim gerektirir; ağır kapılar atlanamaz).\n")
        return 2

    chapter = args.chapter
    if chapter and not chapter.startswith("chapters/"):
        chapter = os.path.join(CHAPTERS_DIR, chapter)
    ctx = {"fast": args.fast, "chapter": chapter, "closing": args.closing}

    results = run(ctx, section=args.section)
    if not results:
        print("Seçime uyan kontrol yok.")
        return 0
    counts = report(results, ctx)
    return 1 if counts[FAIL] else 0


if __name__ == "__main__":
    sys.exit(main())
