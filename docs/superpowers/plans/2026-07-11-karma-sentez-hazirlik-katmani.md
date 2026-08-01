# İki-Kol Karma Sentez Hazırlık Katmanı — Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Yazım motoru iki kanonik dosyayı (nicel CSR + nitel kanonik sonuçlar) tek doğruluk kaynağı alarak izlenebilir joint-display + çapraz-kol meta-çıkarım üretebilsin.

**Architecture:** İki kanonik `.qmd`'ye stabil ankraj → ankraj-provenanslı TSV kanıt-ledger → stdlib drift-guard checker → doldurulmuş sentez belgesi (joint-display + meta-çıkarım) → üretim bölümlerine (04/05) provisional taslak enjeksiyon + yönetişim bağlantısı.

**Tech Stack:** Python 3 stdlib (checker + unittest), Quarto/Markdown (ankraj, ledger TSV, sentez belgesi, tez bölümleri).

Tasarım: `docs/superpowers/specs/2026-07-11-karma-sentez-hazirlik-katmani-design.md`.

## Global Constraints

- **Kanonik girdiler:** nicel `docs/CLINICAL-STUDY-REPORT-FINAL.qmd`, nitel `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd`. Üretim tez dosyaları: `chapters/04_bulgular.qmd`, `chapters/05_tartisma_ve_sonuc.qmd`.
- **İlişki-türü sözlüğü (tam bu 4 değer):** `uyum`, `tamamlayıcılık`, `ayrışma`, `açıklayıcı-genişleme`.
- **Ledger TSV başlığı (tam bu sıra):** `id	odak	nicel_verdikt_ozet	nicel_ankraj	nitel_oruntu_ozet	nitel_ankraj	iliski_turu	karma_yorum_siniri` (sekme ayraç).
- **KVKK:** yalnız iki manuskript-düzeyi `.qmd` + türev katman okunur/yazılır; ham görüşme / `data/*` / `outputs/*` / `_targets/*` / aile-düzeyi satır **girmez**. Agregat verdikt + de-identified tema + ankraj-provenans.
- **Kaynaksız-sayı Stop kapısı:** sentez belgesi + tez taslaklarındaki her nicel değer `dosya#ankraj` provenanslı olmalı.
- **Kapı 0-5:** `chapters/04+05` enjeksiyonu `provisional-pass` işaretli; final değil.
- **Dil:** Türkçe. **Ondalık:** virgül (`p<0,001`). **Atıf:** AMA-11 (`ve`/`ve ark.`).
- **Bağımlılık:** stdlib-only (pytest **yok**); testler stdlib `unittest` (`tests/test_bib_hygiene.py` idiomu).
- **Ankraj hedefleri (11) ve ledger satırları (6):** spec §5 Bileşen 1/2 tablolarından; keşifte doğrulanan başlık satırlarından türetildi.

---

### Task 1: Stabil ankrajlar (iki kanonik dosya)

**Files:**
- Modify: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (7 başlık)
- Modify: `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` (4 başlık)

**Interfaces:**
- Produces: 11 stabil Quarto ankraj (`{#id}`) — ledger (Task 3) ve checker (Task 2) bunlara referans verir. Ankraj id'leri: `h1-karar`, `h2-karar`, `h3-karar`, `h4-karar`, `h5-karar`, `sec-sinopsis-verdikt`, `sec-genel-hipotez-ozet` (nicel); `tema-1`, `tema-2`, `tema-3`, `tema-4` (nitel).

- [ ] **Step 1: Nicel dosyaya 7 ankraj ekle**

Her başlık satırının sonuna ` {#id}` ekle (Edit tool ile, satır içeriği aynen korunur):

| Mevcut başlık | Yeni |
|---|---|
| `## 2.3 Sonuçların Yönetici Özeti` | `## 2.3 Sonuçların Yönetici Özeti {#sec-sinopsis-verdikt}` |
| `### 11.1.5 H1 Karar Kutusu` | `### 11.1.5 H1 Karar Kutusu {#h1-karar}` |
| `### 11.2.4 H2 Karar Kutusu` | `### 11.2.4 H2 Karar Kutusu {#h2-karar}` |
| `### 11.3.6 H3 Karar Kutusu` | `### 11.3.6 H3 Karar Kutusu {#h3-karar}` |
| `### 11.4.4 H4 Karar Kutusu` | `### 11.4.4 H4 Karar Kutusu {#h4-karar}` |
| `### 11.5.8 H5 Karar Kutusu` | `### 11.5.8 H5 Karar Kutusu {#h5-karar}` |
| `## 19.2 Hipotez Düzeyinde Özet Çıkarımlar` | `## 19.2 Hipotez Düzeyinde Özet Çıkarımlar {#sec-genel-hipotez-ozet}` |

- [ ] **Step 2: Nitel dosyaya 4 Tema ankrajı ekle**

| Mevcut başlık | Yeni |
|---|---|
| `## Tema 1 — Sağlıklı Kardeşin Görünmeyen Yükü` | `## Tema 1 — Sağlıklı Kardeşin Görünmeyen Yükü {#tema-1}` |
| `## Tema 2 — Annenin Tıbbi Bakıcı Rolüne Kayması` | `## Tema 2 — Annenin Tıbbi Bakıcı Rolüne Kayması {#tema-2}` |
| `## Tema 3 — T1DM Tanılı Çocuğun İçeriden Deneyimi` | `## Tema 3 — T1DM Tanılı Çocuğun İçeriden Deneyimi {#tema-3}` |
| `## Tema 4 — Aynı Evde Üç Farklı Deneyim` | `## Tema 4 — Aynı Evde Üç Farklı Deneyim {#tema-4}` |

- [ ] **Step 3: Ankrajları doğrula**

Run:
```bash
grep -c '{#h[1-5]-karar}' docs/CLINICAL-STUDY-REPORT-FINAL.qmd
grep -cE '{#sec-sinopsis-verdikt}|{#sec-genel-hipotez-ozet}' docs/CLINICAL-STUDY-REPORT-FINAL.qmd
grep -cE '{#tema-[1-4]}' niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd
```
Expected: `5`, `2`, `4`.

- [ ] **Step 4: Commit**

```bash
git add docs/CLINICAL-STUDY-REPORT-FINAL.qmd niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd
git commit -m "feat(karma-sentez): iki kanonik dosyaya 11 stabil ankraj (H_ karar + tema)"
```

---

### Task 2: Drift-guard checker + test (TDD)

**Files:**
- Create: `scripts/util/karma_ledger_check.py`
- Test: `tests/test_karma_ledger_check.py`

**Interfaces:**
- Produces: `check(ledger_path, root=REPO_ROOT) -> (severity:int, findings:list[tuple])` (severity 0 temiz / 1 HARD / 2 SOFT); `parse_ledger(text) -> list[dict]`; sabitler `COLUMNS`, `ILISKI_TURLERI`, `DEFAULT_LEDGER`; CLI `main(argv) -> int` (exit kodu = severity). Task 3 ledger'ı bununla doğrular; Task 5 playbook HARD=0 kapısı buna işaret eder.
- Consumes: Task 1 ankrajları (test fixtures kendi sahte dosyalarını kurar; canlı doğrulama Task 3'te).

- [ ] **Step 1: Testi yaz (failing)**

`tests/test_karma_ledger_check.py`:

```python
"""karma_ledger_check drift-guard testleri (stdlib unittest)."""
import importlib.util
import os
import tempfile
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_MOD = os.path.join(os.path.dirname(_HERE), "scripts", "util", "karma_ledger_check.py")
_spec = importlib.util.spec_from_file_location("karma_ledger_check", _MOD)
klc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(klc)

HEADER = "\t".join(klc.COLUMNS)


def _row(**kw):
    d = {c: "x" for c in klc.COLUMNS}
    d.update(kw)
    return "\t".join(d[c] for c in klc.COLUMNS)


class TestKarmaLedgerCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        with open(os.path.join(self.tmp, "nicel.qmd"), "w", encoding="utf-8") as f:
            f.write("### H1 Karar Kutusu {#h1-karar}\n"
                    "DM lehine reddetme yükselmesi gözlenmiştir.\n")
        with open(os.path.join(self.tmp, "nitel.qmd"), "w", encoding="utf-8") as f:
            f.write("## Tema 3 {#tema-3}\n"
                    "hastalığı hem normalleştirme hem yük olarak taşıma\n")

    def _led(self, *rows):
        p = os.path.join(self.tmp, "led.tsv")
        with open(p, "w", encoding="utf-8") as f:
            f.write(HEADER + "\n" + "\n".join(rows) + "\n")
        return p

    def _ok_row(self, **over):
        base = dict(
            id="h1", iliski_turu="açıklayıcı-genişleme",
            nicel_ankraj="nicel.qmd#h1-karar",
            nicel_verdikt_ozet="DM lehine reddetme yükselmesi",
            nitel_ankraj="nitel.qmd#tema-3",
            nitel_oruntu_ozet="normalleştirme hem yük olarak taşıma",
        )
        base.update(over)
        return _row(**base)

    def test_clean(self):
        sev, f = klc.check(self._led(self._ok_row()), root=self.tmp)
        self.assertEqual(sev, 0, f)

    def test_hard_missing_anchor(self):
        sev, _ = klc.check(self._led(self._ok_row(nicel_ankraj="nicel.qmd#YOK")), root=self.tmp)
        self.assertEqual(sev, 1)

    def test_hard_missing_file(self):
        sev, _ = klc.check(self._led(self._ok_row(nicel_ankraj="yok.qmd#h1-karar")), root=self.tmp)
        self.assertEqual(sev, 1)

    def test_soft_snippet_drift(self):
        sev, _ = klc.check(self._led(self._ok_row(nicel_verdikt_ozet="BURADA OLMAYAN CÜMLE")), root=self.tmp)
        self.assertEqual(sev, 2)

    def test_soft_invalid_iliski(self):
        sev, _ = klc.check(self._led(self._ok_row(iliski_turu="GECERSIZ")), root=self.tmp)
        self.assertEqual(sev, 2)

    def test_hard_dominates_soft(self):
        sev, _ = klc.check(
            self._led(self._ok_row(iliski_turu="GECERSIZ", nicel_ankraj="nicel.qmd#YOK")),
            root=self.tmp)
        self.assertEqual(sev, 1)

    def test_bad_header(self):
        p = os.path.join(self.tmp, "bad.tsv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("wrong\theader\n")
        with self.assertRaises(ValueError):
            klc.check(p, root=self.tmp)

    def test_bad_column_count(self):
        p = os.path.join(self.tmp, "bad2.tsv")
        with open(p, "w", encoding="utf-8") as f:
            f.write(HEADER + "\n" + "a\tb\n")
        with self.assertRaises(ValueError):
            klc.check(p, root=self.tmp)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Testin fail ettiğini gör**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_karma_ledger_check -v`
Expected: FAIL (`karma_ledger_check.py` yok → ImportError/FileNotFoundError).

- [ ] **Step 3: Checker'ı yaz**

`scripts/util/karma_ledger_check.py`:

```python
#!/usr/bin/env python3
"""Karma kanıt-ledger drift-guard.

Ledger'daki her ankrajın (`dosya#ankraj`) kaynak dosyada var olduğunu ve ilgili
verdikt/örüntü alıntısının kaynakta hâlâ geçtiğini doğrular. Ağsız, stdlib.

Exit: 0 temiz · 1 HARD (kayıp ankraj / kayıp dosya) · 2 SOFT (alıntı drift /
geçersiz ilişki türü). HARD, SOFT'a baskındır.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

_HERE = os.path.abspath(__file__)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DEFAULT_LEDGER = "tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv"
ILISKI_TURLERI = {"uyum", "tamamlayıcılık", "ayrışma", "açıklayıcı-genişleme"}
COLUMNS = [
    "id", "odak",
    "nicel_verdikt_ozet", "nicel_ankraj",
    "nitel_oruntu_ozet", "nitel_ankraj",
    "iliski_turu", "karma_yorum_siniri",
]

_WS = re.compile(r"\s+")


def _norm(text):
    return _WS.sub(" ", text).strip()


def parse_ledger(text):
    """TSV metnini satır sözlüklerine çevir. Başlık COLUMNS ile eşleşmeli."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        raise ValueError("ledger boş")
    header = lines[0].split("\t")
    if header != COLUMNS:
        raise ValueError(
            "ledger başlığı beklenen sütunlarla eşleşmiyor:\n"
            f"  beklenen: {COLUMNS}\n  bulunan:  {header}"
        )
    rows = []
    for i, ln in enumerate(lines[1:], start=2):
        cells = ln.split("\t")
        if len(cells) != len(COLUMNS):
            raise ValueError(f"satır {i}: {len(cells)} hücre, beklenen {len(COLUMNS)}")
        rows.append(dict(zip(COLUMNS, cells)))
    return rows


def _split_anchor(ref):
    """`dosya#ankraj` → (dosya, ankraj). Son `#` bölme noktasıdır."""
    if "#" not in ref:
        return ref, ""
    idx = ref.rfind("#")
    return ref[:idx], ref[idx + 1:]


def check(ledger_path, root=REPO_ROOT):
    """Ledger'ı doğrula → (severity, findings). severity: 0/1/2."""
    with open(ledger_path, encoding="utf-8") as fh:
        rows = parse_ledger(fh.read())

    findings = []
    cache = {}

    def _load(rel):
        if rel not in cache:
            path = os.path.join(root, rel)
            cache[rel] = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        return cache[rel]

    for row in rows:
        rid = row["id"]
        if row["iliski_turu"] not in ILISKI_TURLERI:
            findings.append(("SOFT", rid, f"geçersiz ilişki türü: {row['iliski_turu']!r}"))
        for kol, ank_col, ozet_col in (
            ("nicel", "nicel_ankraj", "nicel_verdikt_ozet"),
            ("nitel", "nitel_ankraj", "nitel_oruntu_ozet"),
        ):
            rel, anchor = _split_anchor(row[ank_col])
            text = _load(rel)
            if text is None:
                findings.append(("HARD", rid, f"{kol}: kaynak dosya yok: {rel}"))
                continue
            if not anchor or ("{#" + anchor + "}") not in text:
                findings.append(("HARD", rid, f"{kol}: ankraj bulunamadı: #{anchor} ({rel})"))
            ozet = row[ozet_col].strip()
            if ozet and _norm(ozet) not in _norm(text):
                findings.append(("SOFT", rid, f"{kol}: alıntı kaynakta geçmiyor (drift): {ozet[:40]!r}"))

    if any(sev == "HARD" for sev, _, _ in findings):
        severity = 1
    elif findings:
        severity = 2
    else:
        severity = 0
    return severity, findings


def _render(severity, findings):
    label = {0: "TEMİZ", 1: "HARD", 2: "SOFT"}[severity]
    out = [f"karma-ledger-check: {label} ({len(findings)} bulgu)"]
    for sev, rid, msg in findings:
        out.append(f"  [{sev}] {rid}: {msg}")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Karma kanıt-ledger drift-guard")
    ap.add_argument("--ledger", default=os.path.join(REPO_ROOT, DEFAULT_LEDGER))
    ap.add_argument("--root", default=REPO_ROOT)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    severity, findings = check(args.ledger, root=args.root)
    if args.json:
        print(json.dumps(
            {"severity": severity,
             "findings": [{"sev": s, "id": i, "msg": m} for s, i, m in findings]},
            ensure_ascii=False, indent=2))
    else:
        print(_render(severity, findings))
    return severity


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Testin geçtiğini gör**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_karma_ledger_check -v`
Expected: PASS (8 test).

- [ ] **Step 5: Commit**

```bash
git add scripts/util/karma_ledger_check.py tests/test_karma_ledger_check.py
git commit -m "feat(karma-sentez): stdlib drift-guard checker + unittest (ankraj/alıntı/ilişki-türü)"
```

---

### Task 3: Yapılandırılmış kanıt-ledger (TSV)

**Files:**
- Create: `tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv`

**Interfaces:**
- Consumes: Task 1 ankrajları + Task 2 checker (`check()` HARD=0 doğrulaması).
- Produces: kanonik kanıt-ledger — Task 4 sentez belgesi joint-display'i bundan türetir; Task 5 playbook buna işaret eder.

- [ ] **Step 1: Kaynak verdiktleri/örüntüleri oku**

Ankrajlı bölümleri oku ve her satır için **6-14 kelimelik verbatim** alıntı seç:
- Nicel: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` içinde `{#h1-karar}`…`{#h5-karar}` + `{#sec-genel-hipotez-ozet}` bölümleri (H_ Karar Kutusu net verdikt cümlesi).
- Nitel: `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` içinde `{#tema-1}`…`{#tema-4}` + `{#sec-capraz}` bölümleri (tema özü cümlesi).

Alıntı, ilgili dosyada **birebir** geçmeli (checker SOFT drift bunu yakalar); tek satırda geçen, ayırt edici bir parça seç.

- [ ] **Step 2: Ledger TSV'yi yaz**

`tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv` — başlık + 6 satır. Sütun sırası Global Constraints'teki başlıkla birebir; hücreler sekme ayraçlı; `iliski_turu` sözlükten (`uyum`/`tamamlayıcılık`/`ayrışma`/`açıklayıcı-genişleme`).

Satır iskeleti (id · odak · ankrajlar sabit; `*_ozet` ve `iliski_turu`/`karma_yorum_siniri` kaynaktan doldurulur):

| id | odak | nicel_ankraj | nitel_ankraj |
|---|---|---|---|
| `h1-cocuk` | H1 çocuk algısı (EMBU-C) | `docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h1-karar` | `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-3` |
| `h2-kardes` | H2 kardeş ilişkisi (KİA) | `docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h2-karar` | `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-1` |
| `h3-anne` | H3 anne öz-rapor (EMBU-P) | `docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h3-karar` | `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2` |
| `h4-beck` | H4 Beck → EMBU-P (SEM) | `docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h4-karar` | `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2` |
| `h5-diadik` | H5 diadik tutarlılık | `docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h5-karar` | `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4` |
| `meta-triad` | Triadik informant asimetrisi | `docs/CLINICAL-STUDY-REPORT-FINAL.qmd#sec-genel-hipotez-ozet` | `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#sec-capraz` |

`karma_yorum_siniri` her satırda kol-aşırı yorum sınırını taşır (ör. "nedensellik yok; nitel deneyimsel bağlam"). Nitel dosya H2'yi Tema 1 **ve** Tema 4'e bağlıyorsa (`…qmd:487`) `h2-kardes` satırının `nitel_oruntu_ozet`'i her iki temaya değinebilir; ankraj `#tema-1` kalır (ikinci tema sentez belgesinde §2'de açılır).

- [ ] **Step 3: Checker ile doğrula (HARD=0)**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/util/karma_ledger_check.py`
Expected: `karma-ledger-check: TEMİZ (0 bulgu)` (severity 0). SOFT drift çıkarsa alıntıyı kaynağa göre düzelt; HARD çıkarsa ankraj/dosya yolunu düzelt. **HARD=0 zorunlu.**

- [ ] **Step 4: Commit**

```bash
git add tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv
git commit -m "feat(karma-sentez): ankraj-provenanslı kanıt-ledger (H1-H5 + triadik meta, checker TEMİZ)"
```

---

### Task 4: Doldurulmuş sentez belgesi

**Files:**
- Create: `tez-yazim/05_entegrasyon/karma-sentez-kanonik.md`

**Interfaces:**
- Consumes: Task 3 ledger (joint-display §1 bundan türetilir).
- Produces: kanonik karma sentez belgesi — Task 5 (README/plan/qual pointer) ve Task 6 (04/05 taslak) buna işaret eder / bundan türetir.

- [ ] **Step 1: Belgeyi yaz (§0-§5)**

`tez-yazim/05_entegrasyon/karma-sentez-kanonik.md`, spec §5 Bileşen 3 yapısı:
- **§0** Otorite zinciri (`05_entegrasyon/README.md` → bu belge) + KVKK sınırı + kanonik-girdi beyanı (iki dosya, tam yol).
- **§1 Joint-display** (yorumsuz, BULGULAR-hazır): ledger'ın 6 satırından türetilmiş tablo — sütunlar: odak · nicel verdikt · nitel örüntü · ilişki türü · yorum sınırı. Her nicel/nitel hücre `dosya#ankraj` provenanslı.
- **§2 İlişki-türü gerekçelendirmesi:** her satır için neden o ilişki türü (H2 için Tema 1 + Tema 4 ikili bağı burada açılır).
- **§3 Çapraz-kol meta-çıkarımlar:** tek kolun tek başına vermediği ≥3 sonuç. En az biri: H5 triangülasyon-şartı-karşılanmadı (`#h5-karar`) + Tema 4 triadik-farklılık (`#tema-4`) → algı ayrışması ölçüm hatası değil, rol-temelli deneyim (nicel *büyüklük*, nitel *neden/nasıl*).
- **§4 TARTIŞMA köprü cümleleri:** 05'e enjekte edilecek taslak paragraflar (her biri ankraj-provenanslı).
- **§5 Karma-özel sınırlılık:** paralel örneklem farkı — nicel 241 aile (`CLAUDE.md` domain notu) vs nitel 7 aile (`niteliksel/CLAUDE.md`); iki kol aynı bireyleri örneklemez → birleştirme yorum düzeyinde, istatistiksel genelleme değil.

Kurallar: her nicel değer ankraj-provenanslı; kol-aşırı nedensel dil yok; ondalık virgül; Türkçe.

- [ ] **Step 2: Provenans tutarlılığını doğrula**

Run:
```bash
grep -oE '(docs/CLINICAL-STUDY-REPORT-FINAL\.qmd|niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar\.qmd)#[a-z0-9-]+' tez-yazim/05_entegrasyon/karma-sentez-kanonik.md | sort -u
```
Expected: yalnız Task 1'de tanımlı 11 ankrajdan alt-küme; hepsi kaynakta mevcut (Task 1 Step 3 ile çapraz kontrol).

- [ ] **Step 3: Commit**

```bash
git add tez-yazim/05_entegrasyon/karma-sentez-kanonik.md
git commit -m "feat(karma-sentez): doldurulmuş joint-display + çapraz-kol meta-çıkarım belgesi"
```

---

### Task 5: Yönetişim bağlantısı

**Files:**
- Modify: `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md`
- Modify: `tez-yazim/05_entegrasyon/README.md`
- Modify: `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd`
- Modify: `.claude/skills/t1dm-tez-rehberi/references/karma-yontem.md`
- Modify: `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`

**Interfaces:**
- Consumes: Task 3 ledger + Task 4 sentez belgesi (bunlara pointer verir).
- Produces: iki kanonik dosyaya + ledger + sentez belgesine + checker'a hizalı yönetişim.

- [ ] **Step 1: joint-display-plan re-point**

`nitel-nicel-joint-display-plan.md`: (a) "Kullanılacak Güvenli Nitel Kaynaklar" → `niteliksel/qualitative_canonical_results_report.md` yerine kanonik `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd`; (b) "Kullanılacak Nicel Kaynaklar" → var-olmayan `chapters/03_bulgular.qmd` yerine `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (+ üretim `chapters/04_bulgular.qmd`, `chapters/05_tartisma_ve_sonuc.qmd`); (c) "Taslak Tablo Alanları" başına not: doldurulmuş kanonik joint-display artık `karma-sentez-kanonik.md`'de; bu dosya **alan+ilişki sözlüğü** olarak kalır.

- [ ] **Step 2: README tek-otorite haritası**

`05_entegrasyon/README.md` "Tek-Otorite Haritası" tablosuna iki satır ekle: `karma-kanit-ledgeri.tsv` (ankraj-provenanslı kanıt-ledger + drift-guard `scripts/util/karma_ledger_check.py`) ve `karma-sentez-kanonik.md` (doldurulmuş joint-display + meta-çıkarım). "Joint display üretim zinciri" bloğunu iki kanonik dosya + ledger + checker + sentez belgesi + `04_bulgular`/`05_tartisma_ve_sonuc` akışına güncelle (eski `chapters/03_bulgular.qmd` referansını düzelt).

- [ ] **Step 3: Nitel dosya pointer notu**

`niteliksel_kanonik_sonuclar.qmd` `# Karma Tez Entegrasyonu {#sec-karma}` başlığının hemen altına bir satır: kanonik karma sentez (joint-display + meta-çıkarım) tek doğruluk kaynağı `tez-yazim/05_entegrasyon/karma-sentez-kanonik.md`'dir; buradaki tablo nitel-kol bakışıdır. Mevcut içerik/tablo **korunur** (silme yok).

- [ ] **Step 4: Skill karma-yontem bölümü**

`.claude/skills/t1dm-tez-rehberi/references/karma-yontem.md` sonuna "## Kanonik girdi + hazırlık katmanı" bölümü: iki kanonik dosya + `karma-kanit-ledgeri.tsv` + `karma-sentez-kanonik.md` + `karma_ledger_check.py` akışı; BULGULAR joint-display / TARTIŞMA meta-çıkarım için önce sentez belgesini oku, checker HARD=0 olmadan taslak final sayılmaz.

- [ ] **Step 5: Playbook Kapı adımı**

`bolum-finalizasyon-sertifikasyon-playbook.md`: BULGULAR ve TARTIŞMA bölüm sertifikasyonuna adım ekle — `python3 scripts/util/karma_ledger_check.py` çalıştır, **HARD=0** (severity ≠ 1) olmadan bölüm final/certified sayılmaz; SOFT bulguları sertifikada gerekçelendirilir.

- [ ] **Step 6: Doğrula + commit**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/util/karma_ledger_check.py` (hâlâ TEMİZ) ve nitel dosya ankrajları bozulmadı: `grep -cE '{#tema-[1-4]}' niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` → `4`.

```bash
git add tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md tez-yazim/05_entegrasyon/README.md niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd .claude/skills/t1dm-tez-rehberi/references/karma-yontem.md tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md
git commit -m "feat(karma-sentez): yönetişim bağlantısı (plan re-point, README/skill/playbook, qual pointer)"
```

---

### Task 6: Üretim bölümü taslak enjeksiyonu

**Files:**
- Modify: `chapters/04_bulgular.qmd`
- Modify: `chapters/05_tartisma_ve_sonuc.qmd`

**Interfaces:**
- Consumes: Task 4 sentez belgesi (joint-display §1 + köprü §4 + meta-çıkarım §3).
- Produces: 04/05'te provisional karma taslak (final sertifikasyon ayrı).

- [ ] **Step 1: 04_bulgular joint-display taslağı**

`chapters/04_bulgular.qmd` uygun bulgular sonu kesimine, `karma-sentez-kanonik.md` §1'den türetilmiş **yorumsuz** joint-display tablosunu ekle. İlk satır HTML yorumu: `<!-- TASLAK / provisional-pass — kaynak: tez-yazim/05_entegrasyon/karma-sentez-kanonik.md; sertifikasyon: Kapı 0-5 -->`. Kol-aşırı nedensel dil yok; her nicel değer ankraj-provenanslı; ondalık virgül.

- [ ] **Step 2: 05_tartisma meta-çıkarım taslağı**

`chapters/05_tartisma_ve_sonuc.qmd`'e `karma-sentez-kanonik.md` §3 + §4'ten türetilmiş **yorumlu** karma meta-çıkarım/köprü paragraflarını ekle; aynı `<!-- TASLAK / provisional-pass ... -->` işareti. Nitel = deneyimsel bağlam (nedensel değil); nicel = büyüklük/yön (mekanizma değil).

- [ ] **Step 3: Doğrula**

Run:
```bash
grep -c 'provisional-pass' chapters/04_bulgular.qmd chapters/05_tartisma_ve_sonuc.qmd
PYTHONDONTWRITEBYTECODE=1 python3 scripts/util/karma_ledger_check.py
```
Expected: her dosyada ≥1 `provisional-pass`; checker TEMİZ. (Quarto render etkilenen dosyalarda bozulmamalı — büyük render opsiyonel; bu oturumda söz dizimi/işaret kontrolü yeterli.)

- [ ] **Step 4: Commit**

```bash
git add chapters/04_bulgular.qmd chapters/05_tartisma_ve_sonuc.qmd
git commit -m "feat(karma-sentez): 04 joint-display + 05 meta-çıkarım provisional taslak enjeksiyonu"
```

---

## Notlar (uygulayıcı için)

- **KVKK sınırı hattır:** checker + ledger + sentez yalnız iki manuskript `.qmd`'ye dokunur; `data/*`/`outputs/*`/`_targets/*` `permissions.deny` kapsamındadır — açmaya çalışma.
- **Kaynaksız-sayı hook:** commit mesajı ve metinlerde çıplak sayı bırakma; her nicel değer `dosya#ankraj` taşısın (Stop kapısı aksi halde bloklar).
- **Task 1 nicel dosya** working-tree'de kullanıcının commit'lenmemiş dosyası olabilir; yalnız başlık satırlarına `{#id}` eklenir, başka içerik değişmez.
- **Ondalık virgül + AMA-11** tüm yeni metinlerde.
