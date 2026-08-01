#!/usr/bin/env python3
"""R üretici kodunda gömülü istatistik literali denetimi (kaynak-tekilliği kapısı).

Kök-neden: Sonuç-sentezi/plan tabloları gibi APA üretici fonksiyonlar, sayısal
istatistik değerlerini (BF10, β, ICC, AUC, CFI ...) pipeline kaynağından okumak
yerine kod içine SABİT yazdığında; kaynak yeniden çalıştırılınca literaller
kopar (denetim P0-1: "BF10=8.12" / "10,55" driftinin sebebi).

Bu araç R/ ve scripts/R/ altında, "üretici" bağlamda (data.frame/tibble/tribble
içinde APA-benzeri Türkçe/BF/istatistik string'i üreten satırlarda) gömülü
sayısal istatistik literallerini işaretler. Salt-okuma; ham veri okumaz.

Politika:
  - Beyaz liste: eşik/sınıflandırma sabitleri (BF>10, ROPE ±0.10 gibi kural
    sabitleri), seed, n_boot, indeks, format basamağı (%.2f), yıl.
  - Kara liste tetikleyici: data.frame/tibble/tribble/paste0 bağlamında
    "BF10="/"BF₁₀"/"β="/"ICC="/"AUC=" gibi istatistik etiketiyle bitişik
    serbest sayısal literal.

Çıkış: bulgu yoksa exit 0; --fail-on-find ile bulgu varsa exit 1.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SCAN_DIRS = ["R", os.path.join("scripts", "R")]

# İstatistik etiketi + bitişik serbest sayısal literal (üretici string içinde).
# ör: "BF10=8.12", "BF₁₀ = 10,55", "ICC=0.32", "AUC=0.61", "β = 0,16"
STAT_LABEL_LITERAL_RE = re.compile(
    r"(?i)(BF10|BF₁₀|\bICC\b|\bAUC\b|\bCFI\b|\bTLI\b|\bSRMR\b|\bRMSEA\b|"
    r"\bβ\b|\bbeta\b|\bd\b|Cohen|\bV\b|Cram[eé]r)\s*[=:]\s*"
    r"[-+]?\d+[.,]\d+"
)

# Üretici bağlam işaretleri: bu anahtarlardan biri aynı fonksiyon/blokta ise
# literal "rapor edilen sayı" niteliği taşır (eşik sabiti değil).
GENERATOR_CONTEXT_RE = re.compile(
    r"(?i)(data\.frame\(|tibble\(|tribble\(|paste0\(|paste\(|"
    r"Ana_bulgu|claim_boundary|Sonuc|Karar|synthesis|evidence_map|result_synthesis)"
)

# Beyaz liste: bunlar eşik/kural/biçim sabitidir, drift riski taşımaz.
WHITELIST_LINE_RE = re.compile(
    r"(?i)(prior_sd|rope|seed|n_boot|nboot|%\.?\d*[fdg]|"
    r"if\s*\(.*bf|>\s*10\b|>\s*3\b|>\s*30\b|>\s*100\b|"
    r"1/3|1/10|0\.10\b|0,10\b|width|height|dpi|"
    r"scale_|coord_|theme_|element_|linewidth|alpha\s*=|size\s*=)"
)

# Kaynak-türevli satır işareti: satırda bir pipeline kaynak değişkeni/erişimi
# varsa (ör. .bf_h1, tar_read, x$bf10, *_table), birincil değer zaten
# kaynaktan geliyordur; kalan literaller ikincil bağlamdır -> flag'lenmez.
SOURCE_REF_RE = re.compile(
    r"(\.[a-z_][a-z0-9_]*|tar_read|\$bf10|\$BIC|\$Entropy|\$estimate|"
    r"[a-z_]+_table\b|[a-z_]+_posterior\b|apa_fmt_)"
)

# Doğrulama/test fixture dosyaları: bilerek sabit referans değeri taşırlar.
FIXTURE_PATH_RE = re.compile(r"(?i)(verify_|test_|_audit_fixture|fixture)")

# Yorum satırı (denetim notu içinde geçen örnek literaller sayılmaz).
COMMENT_RE = re.compile(r"^\s*#")


@dataclass
class Finding:
    path: str
    line_no: int
    text: str


def _iter_r_files():
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            if name.endswith(".R"):
                yield os.path.join(base, name)


def _iter_chapter_files():
    base = os.path.join(ROOT, "chapters")
    if not os.path.isdir(base):
        return
    for name in sorted(os.listdir(base)):
        if name.endswith(".qmd"):
            yield os.path.join(base, name)


# Quarto R chunk sınırları: ```{r ...} ... ```
_CHUNK_OPEN_RE = re.compile(r"^[ \t]*`{3,}\s*\{r[ ,}]")
_FENCE_RE = re.compile(r"^[ \t]*`{3,}\s*$")


def _apply_literal_rule(rel_path, chunk):
    """chunk = [(orig_idx, raw_line)] — aynı kaynak-tekilliği kuralını uygular."""
    out: list[Finding] = []
    for pos, (idx, raw) in enumerate(chunk):
        line = raw.rstrip("\n")
        if COMMENT_RE.match(line):
            continue
        if not STAT_LABEL_LITERAL_RE.search(line):
            continue
        if WHITELIST_LINE_RE.search(line):
            continue
        if SOURCE_REF_RE.search(line):
            continue
        lo = max(0, pos - 3)
        hi = min(len(chunk), pos + 4)
        ctx = "".join(chunk[j][1] for j in range(lo, hi))
        if GENERATOR_CONTEXT_RE.search(ctx):
            out.append(Finding(rel_path, idx + 1, line.strip()))
    return out


def _scan_qmd_chunks(path: str) -> list[Finding]:
    """Bir .qmd içindeki inline ```{r}``` chunk'larını üretici-literal için tara.

    Yalnız R chunk bölgeleri taranır; düzyazı ve diğer diller (python vb.)
    kapsam dışı. R/ tarayıcısıyla aynı kara/beyaz-liste + üretici-bağlam kuralı.
    """
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    out: list[Finding] = []
    rel = os.path.relpath(path, ROOT)
    in_chunk = False
    chunk: list[tuple[int, str]] = []
    for i, raw in enumerate(lines):
        if not in_chunk and _CHUNK_OPEN_RE.match(raw):
            in_chunk, chunk = True, []
            continue
        if in_chunk and _FENCE_RE.match(raw):
            out.extend(_apply_literal_rule(rel, chunk))
            in_chunk, chunk = False, []
            continue
        if in_chunk:
            chunk.append((i, raw))
    if in_chunk and chunk:  # kapanmamış chunk (savunmacı)
        out.extend(_apply_literal_rule(rel, chunk))
    return out


def _scan_file(path: str) -> list[Finding]:
    out: list[Finding] = []
    if FIXTURE_PATH_RE.search(os.path.basename(path)):
        return out  # doğrulama/test fixture: sabit referans değeri beklenir
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    # Fonksiyon/blok bağlamını basitçe pencere ile tahmin et: aynı satırda ya da
    # yakın komşulukta üretici bağlam işareti varsa literal "rapor" sayılır.
    for i, raw in enumerate(lines):
        line = raw.rstrip("\n")
        if COMMENT_RE.match(line):
            continue
        if not STAT_LABEL_LITERAL_RE.search(line):
            continue
        if WHITELIST_LINE_RE.search(line):
            continue
        if SOURCE_REF_RE.search(line):
            continue  # birincil değer kaynaktan geliyor; literal ikincildir
        # bağlam: bu satır veya ±3 satır içinde üretici işareti
        lo = max(0, i - 3)
        hi = min(len(lines), i + 4)
        ctx = "".join(lines[lo:hi])
        if GENERATOR_CONTEXT_RE.search(ctx):
            out.append(Finding(os.path.relpath(path, ROOT), i + 1, line.strip()))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fail-on-find", action="store_true",
                    help="bulgu varsa exit 1 (checklist kapısı)")
    ap.add_argument("--include-chapters", action="store_true",
                    help="R/ + scripts/R yanı sıra chapters/*.qmd inline {r} "
                         "chunk'larını da tara (kaynak-tekilliği gövdeye yayılır)")
    ap.add_argument("--paths", nargs="*",
                    help="Yalnız verilen .qmd dosyalarının {r} chunk'larını tara "
                         "(test/hedefli koşum; R/ dizinleri atlanır)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    findings: list[Finding] = []
    if args.paths:
        for path in args.paths:
            findings.extend(_scan_qmd_chunks(path))
    else:
        for path in _iter_r_files():
            findings.extend(_scan_file(path))
        if args.include_chapters:
            for path in _iter_chapter_files():
                findings.extend(_scan_qmd_chunks(path))

    if not args.quiet:
        if findings:
            print(f"[r_generator_literal_audit] {len(findings)} gömülü istatistik "
                  f"literali (üretici bağlam):")
            for f in findings:
                print(f"  {f.path}:{f.line_no}: {f.text}")
            print("\nÇözüm: değeri elle yazmak yerine ilgili pipeline tablosundan "
                  "(bayes_*_posterior_table, *_fit_table, performance_table ...) oku.")
        else:
            print("[r_generator_literal_audit] PASS: üretici kodda gömülü "
                  "istatistik literali yok.")

    if findings and args.fail_on_find:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
