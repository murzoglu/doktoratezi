# Niteliksel Kol Yeniden İnşa — Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Alan skill'i:** Her niteliksel üretim/denetim adımında `niteliksel-arastirma-rehberi-t1dm` skill'i tetiklenir (otör-yetkinlik). Dış literatür gerektiğinde `evidentia` (yalnız literatür terimi). Metin kapanış denetimi `sci-audit`.

**Goal:** Tezin niteliksel kolunu (`new/` kaynak materyalleri = tek doğruluk kaynağı) verbatim alıntılı, COREQ-tam, triadik tasarımlı olarak ch02/03/04/05/07'de baştan kurmak; provenance'ı mevcut quote altyapısıyla güvenceye almak.

**Architecture:** İki katman. (1) **Kanon katmanı** (`niteliksel/`): `triadik tablo.xlsx`'ten yapılandırılmış triadik matris + genişletilmiş `quotes_used.csv` manifesti (verbatim'siz) + tema mimarisi v3 + codebook v3 + tazelenmiş COREQ-32; v2.0 arşive. (2) **Tez katmanı** (`chapters/`): de-identify verbatim alıntılarla (Aile no, rol, yaş) yeniden yazılan ch02–07. Her verbatim, manifest + `quote_integrity` parity ile izlenir.

**Tech Stack:** Quarto (Türkçe APA 7, apaquarto), Python 3 (openpyxl, pandas, csv, pytest), mevcut `niteliksel/dm_niteliksel_toolkit/quote_integrity.py`, `scripts/util/tez_checklist_verify.py`, `sci-audit` + Galileo denetim kapıları, pandoc (docx→metin, salt-okuma).

## Global Constraints

- **KVKK sert sınır:** Yayımlanan tezde gerçek ad/doğum tarihi/tanı tarihi **yok**; alıntı etiketi `(Aile <no>, <rol>, <yaş> yaş)`; künye türetilmiş yaş/süre. Ham kaynak (`niteliksel/new/`) + doğum tarihli türevler **git'e girmez** (Task 0.1 gitignore). Katılımcı verisi/alıntı **dış MCP/connector'a (evidentia/minerva/pipeworx) asla** gönderilmez; ajan hafızasına kimliksel veri yazılmaz. Dış araca yalnız literatür arama terimi.
- **Kanon:** `new/` v2.0'ı geçersiz kılar; v2.0 **arşive taşınır (silinmez)**; v2↔v3 farkı `reconciliation_v2_to_v3.md`'de raporlanır.
- **Örneklem sabit:** 7 aile / 21 görüşme; aile kodları `011, 014, 019, 020, 026, 201, 202` (zero-pad 3 hane). Rol kanonik: `mother | t1dm_child | healthy_sibling` (mevcut repo/manifest deseni; tez görünen etiketi "T1DM'li çocuk").
- **quote_id şeması (mevcut repo deseni):** `{aile_no}_{rol}_q{NNN}` (ör. `011_mother_q006`). CSV şemasına `triadik_eksen` sütunu **eklenir**; verbatim CSV'ye **yazılmaz** (verbatim yalnız tez/kanon metninde).
- **Alıntı bütünlüğü:** verbatim aynen; izin verilen tek müdahale `[…]` kesme ve `[açıklama]` ekleme; her müdahale `quote_integrity` uyarısını geçmeli.
- **RTA epistemolojisi:** inter-coder kappa/AC1 **üretilmez** (critical-friend + refleksivite raporlanır); frekans ≠ önem; her makro temada ≥1 negatif/aykırı örüntü (COREQ M31).
- **Render disiplini:** chapter düzenlemesi sonrası `_freeze/` + `outputs/quarto/thesis*` temizlenip `quarto render` (bkz. memory: render-freeze-include-gotcha).
- **Tez dili Türkçe; APA-TR sayı/ondalık biçimi; resmi format `tez-yazim/README.md` + `docs/tez-kilavuz/` üstündür.**

---

## Faz 0 — Yönetişim ve iskele

### Task 0.1: Ham kaynağı gitignore'a al (KVKK)

**Files:**
- Modify: `.gitignore` (Nitel kol veri sınırı bloğu, ~satır 209-227)

- [ ] **Step 1: `.gitignore`'a `new/` ve doğum-tarihli türevleri ekle**

`.gitignore`'daki "Nitel kol veri sınırı" bloğunun sonuna ekle:

```gitignore
# new/ ham kaynak (verbatim + doğum tarihi) ve doğum-tarihli türevler yerelde kalır
niteliksel/new/
niteliksel/**/triadik_matris_extracted.csv
niteliksel/**/*_identified.csv
```

- [ ] **Step 2: İzli-değil doğrula**

Run: `git check-ignore "niteliksel/new/triadik tablo.xlsx" && git status --short niteliksel/new/`
Expected: yol IGNORED döner; `git status` new/ göstermez.

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "kvkk: niteliksel/new ham kaynağı (doğum tarihi+verbatim) gitignore"
```

### Task 0.2: `new/` docx/xlsx → salt-okuma metin köprüsü (yerel, gitignored)

**Files:**
- Create: `niteliksel/scripts/util/new_source_to_text.py`

**Interfaces:**
- Produces: `niteliksel/new/_extracted/*.txt` (yerel; gitignored) — sonraki task'ler için okunaklı kaynak.

- [ ] **Step 1: Script'i yaz**

```python
#!/usr/bin/env python3
"""new/ docx+pdf -> düz metin (yerel, gitignored). KVKK: dış araca gitmez."""
import subprocess, pathlib
SRC = pathlib.Path(__file__).resolve().parents[2] / "new"
OUT = SRC / "_extracted"; OUT.mkdir(exist_ok=True)
for f in sorted(SRC.glob("*.docx")):
    subprocess.run(["pandoc", str(f), "-t", "plain", "-o", str(OUT / (f.stem + ".txt"))], check=True)
for f in sorted(SRC.glob("*.pdf")):
    subprocess.run(["pdftotext", str(f), str(OUT / (f.stem + ".txt"))], check=True)
print("OK ->", OUT)
```

- [ ] **Step 2: Çalıştır ve doğrula**

Run: `cd niteliksel && python3 scripts/util/new_source_to_text.py && ls new/_extracted/`
Expected: 5 .txt (docx) + covid .txt üretilir.

- [ ] **Step 3: Commit (yalnız script; _extracted gitignored)**

```bash
git add niteliksel/scripts/util/new_source_to_text.py
git commit -m "araç: new/ kaynak->metin köprüsü (yerel çıktı, gitignored)"
```

---

## Faz 1 — Kanon katmanı v3

### Task 1.1: Triadik matris çıkarımı (`triadik tablo.xlsx` → yapılandırılmış CSV, yerel)

**Files:**
- Create: `niteliksel/scripts/util/extract_triadic_matrix.py`
- Test: `niteliksel/tests/test_extract_triadic_matrix.py`
- Output (yerel, gitignored): `niteliksel/new/triadik_matris_extracted.csv`

**Interfaces:**
- Produces: satır şeması `aile_no,rol,triadik_eksen,verbatim_tr` — 1.2/1.3 ve ch04 curation'ın girdisi.

- [ ] **Step 1: Rol/aile/eksen eşlemeli çıkarım testini yaz**

```python
# niteliksel/tests/test_extract_triadic_matrix.py
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("ex", pathlib.Path(__file__).parents[1]/"scripts/util/extract_triadic_matrix.py")
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)

def test_role_map():
    assert ex.ROLE["ANNE"] == "mother"
    assert ex.ROLE["HASTA"] == "t1dm_child"
    assert ex.ROLE["KARDEŞ"] == "healthy_sibling"

def test_family_pad():
    assert ex.pad_family("11") == "011"
    assert ex.pad_family("201") == "201"

def test_axis_slugs_8():
    assert len(ex.AXIS_SLUGS) == 8
```

- [ ] **Step 2: Test'i çalıştır — FAIL beklenir**

Run: `cd niteliksel && python3 -m pytest tests/test_extract_triadic_matrix.py -q`
Expected: FAIL (module yok).

- [ ] **Step 3: Çıkarım script'ini yaz**

```python
#!/usr/bin/env python3
"""triadik tablo.xlsx -> uzun-format CSV (aile,rol,eksen,verbatim). Yerel/gitignored."""
import csv, pathlib, openpyxl
BASE = pathlib.Path(__file__).resolve().parents[2] / "new"
XLSX = BASE / "triadik tablo.xlsx"
OUT  = BASE / "triadik_matris_extracted.csv"
ROLE = {"ANNE": "mother", "HASTA": "t1dm_child", "KARDEŞ": "healthy_sibling", "KARDES": "healthy_sibling"}
AXIS_SLUGS = ["hastalik_algisi","kisit","gunluk_sosyal","ergenlik","kaybetme_korkusu",
              "kardes_yasantisi","annelik_donusum","ihtiyaclar"]
def pad_family(n): return n.strip().zfill(3)
def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)
    rows = list(wb.active.iter_rows(values_only=True))
    recs = []
    for r in rows[1:]:
        label = (r[0] or "").strip()
        if not label: continue
        parts = label.split()
        role = ROLE.get(parts[0].upper()); fam = pad_family(parts[-1])
        if not role: continue
        for j, slug in enumerate(AXIS_SLUGS, start=1):
            cell = r[j] if j < len(r) else None
            if cell and str(cell).strip():
                recs.append({"aile_no": fam, "rol": role, "triadik_eksen": slug,
                             "verbatim_tr": str(cell).strip()})
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["aile_no","rol","triadik_eksen","verbatim_tr"])
        w.writeheader(); w.writerows(recs)
    print(f"{len(recs)} hücre -> {OUT}")
if __name__ == "__main__": main()
```

- [ ] **Step 4: Test PASS + çıkarımı çalıştır**

Run: `cd niteliksel && python3 -m pytest tests/test_extract_triadic_matrix.py -q && python3 scripts/util/extract_triadic_matrix.py`
Expected: test PASS; ~110 hücre CSV yazılır (doluluk: 20+16+16+8+12+17+12+8).

- [ ] **Step 5: Commit (script + test; CSV gitignored)**

```bash
git add niteliksel/scripts/util/extract_triadic_matrix.py niteliksel/tests/test_extract_triadic_matrix.py
git commit -m "araç: triadik tablo -> uzun-format matris çıkarımı (+test)"
```

### Task 1.2: Tema mimarisi v3 + Rosetta (8 eksen ↔ 4 makro/17 alt-tema)

**Files:**
- Create: `niteliksel/03_analysis/codebook/theme_architecture_v3.md`

**Interfaces:**
- Consumes: `triadik_matris_extracted.csv` (eksenler), `new/_extracted/nitel ana.txt` (tema/alt-tema başlıkları).
- Produces: 4 makro tema + 17 alt-tema tanımı + 8-eksen Rosetta tablosu — ch04/1.3/codebook girdisi.

- [ ] **Step 1: Belgeyi yaz** — `nitel ana`'daki başlıklardan (spec §5 tablosu) 4 makro tema, 17 alt-tema; her alt-temaya baskın triadik eksen(ler) haritası; ince-örüntü (ergenlik 8/21, ihtiyaçlar 8/21) negatif-vaka işareti. Her tema için "merkezi düzenleyici işlev" cümlesi (frekans değil).

- [ ] **Step 2: Doğrula** — 4 tema, 17 alt-tema (3+6+4+4), 8 eksen tam kapsanmış.

Run: `grep -cE '^### Alt-tema' niteliksel/03_analysis/codebook/theme_architecture_v3.md`
Expected: 17.

- [ ] **Step 3: Commit**

```bash
git add niteliksel/03_analysis/codebook/theme_architecture_v3.md
git commit -m "kanon: tema mimarisi v3 (4 makro/17 alt-tema + 8-eksen Rosetta)"
```

### Task 1.3: Codebook v3 (kod ↔ eksen ↔ makro-tema)

**Files:**
- Create: `niteliksel/03_analysis/codebook/codebook_v3.md`

**Interfaces:**
- Consumes: `theme_architecture_v3.md`, `codebook_v2.md` (kod adları, korunacaklar), `triadik_matris_extracted.csv`.
- Produces: kanonik kod listesi (v3) — ch07 kod ağacı ekinin kaynağı.

- [ ] **Step 1: Belgeyi yaz** — v2'deki 23 kodu gözden geçir; new/ eksenleriyle hizala; her kodu (eksen, makro-tema, tanım, örnek quote_id) ile ver. v2→v3 kod değişimi tabloya işlenir.

- [ ] **Step 2: Doğrula** — her makro tema ≥1 kod; her eksen ≥1 kodla eşli.

- [ ] **Step 3: Commit**

```bash
git add niteliksel/03_analysis/codebook/codebook_v3.md
git commit -m "kanon: codebook v3 (kod<->eksen<->makro-tema)"
```

### Task 1.4: v2.0 arşivleme + reconciliation raporu

**Files:**
- Create: `niteliksel/archive/2026-07-29_pre_new_canon/` (git mv hedefi)
- Move: `niteliksel/qualitative_canonical_results_report.md`, `niteliksel/03_analysis/codebook/codebook_v2.md` → arşive
- Create: `niteliksel/03_analysis/reconciliation_v2_to_v3.md`

- [ ] **Step 1: Arşiv dizini + taşı**

```bash
mkdir -p niteliksel/archive/2026-07-29_pre_new_canon
git mv niteliksel/qualitative_canonical_results_report.md niteliksel/archive/2026-07-29_pre_new_canon/
git mv niteliksel/03_analysis/codebook/codebook_v2.md niteliksel/archive/2026-07-29_pre_new_canon/
```

- [ ] **Step 2: reconciliation raporunu yaz** — v2 (4 makro/6 journal, 23 kod, quote_id-only) vs v3 (new/ verbatim, 8 eksen, `{aile}_{rol}_q{NNN}` + eksen sütunu); tema adı/sayı farkları; "new supersedes" gerekçesi; hangi v2 kararının korunduğu (COREQ metodoloji, positionality, audit-trail).

- [ ] **Step 3: skill kanonik-kaynak referanslarını güncelle** — `niteliksel/CLAUDE.md` ve `.claude/skills/niteliksel-arastirma-rehberi-t1dm/SKILL.md` "Kanonik Kaynak Önceliği" bloğunda v2.0 → v3 (arşiv notuyla) işaretle.

- [ ] **Step 4: Commit**

```bash
git add -A niteliksel/archive niteliksel/03_analysis/reconciliation_v2_to_v3.md niteliksel/CLAUDE.md .claude/skills/niteliksel-arastirma-rehberi-t1dm/SKILL.md
git commit -m "kanon: v2.0 arşive + v2->v3 reconciliation (new supersedes)"
```

### Task 1.5: COREQ-32 tazeleme (new/ coreq'ten)

**Files:**
- Modify: `niteliksel/03_analysis/methodology/coreq_32_completed.md`

- [ ] **Step 1: `new/_extracted/nitel coreq uyumlu.txt` ile madde-madde karşılaştır** — eksik/kısmi maddeleri güncelle: uzman paneli (M?), senaryo-sorusu revizyonu (M17), gözlemci BA (M5), 21→7 davet/kabul (M12/13), veri güvenliği/şifreli (M?), member-reflection sınırı (M23), negatif vaka (M31). Etik onay `09.2023.201`, tarih `06.07.2023–25.10.2023`.

- [ ] **Step 2: Doğrula** — 32 madde tam; 2 kısmi (transkript-iadesi, formal kappa) şeffaf "yapılmadı".

Run: `grep -cE '^\| ?M?[0-9]+' niteliksel/03_analysis/methodology/coreq_32_completed.md` (≈32 satır)

- [ ] **Step 3: Commit**

```bash
git add niteliksel/03_analysis/methodology/coreq_32_completed.md
git commit -m "kanon: COREQ-32 new/ coreq belgesinden tazelendi"
```

### Task 1.6: `quotes_used.csv` manifestini v3 için hazırla (verbatim'siz)

**Files:**
- Modify: `niteliksel/06_manuscript_outputs/quotes_used.csv` (şemaya `triadik_eksen` sütunu ekle; v2 quote_id'leri v3 kaynak-dosyalarına göre revize edilecek — asıl doldurma ch04 task'lerinde)
- Modify: `niteliksel/dm_niteliksel_toolkit/quote_integrity.py` (yeni sütunu tolere et)
- Test: `niteliksel/tests/test_quote_integrity.py` (yeni sütun testi)

**Interfaces:**
- Consumes: mevcut `check_quotes(source_dir, quotes_csv)`.
- Produces: `triadik_eksen` sütunlu manifest; ch04/05/07 task'leri satır ekler.

- [ ] **Step 1: Önce `quote_integrity.py`'yi tümüyle oku** (Read tool) — `_read_source_text`, `check_quotes`, izin verilen kısaltma/mask mantığını anla; kırma.

- [ ] **Step 2: Yeni sütun için başarısız test yaz**

```python
def test_triadik_eksen_column_tolerated():
    # quotes_used.csv triadik_eksen sütunu içerince check_quotes hata vermemeli
    ...  # geçici csv: quote_id,aile_no,rol,tema,triadik_eksen,kaynak_dosya
```

- [ ] **Step 3: Test FAIL doğrula** → `cd niteliksel && python3 -m pytest tests/test_quote_integrity.py -q`

- [ ] **Step 4: `quote_integrity.py`'yi minimal genişlet** (opsiyonel sütunu yok say/koru), CSV başlığına `triadik_eksen` ekle.

- [ ] **Step 5: Test PASS** → `python3 -m pytest tests/test_quote_integrity.py -q`

- [ ] **Step 6: Commit**

```bash
git add niteliksel/06_manuscript_outputs/quotes_used.csv niteliksel/dm_niteliksel_toolkit/quote_integrity.py niteliksel/tests/test_quote_integrity.py
git commit -m "kanon: quotes_used.csv triadik_eksen sütunu + integrity toleransı (+test)"
```

### Task 1.7: Tez-düzeyi verbatim parity denetleyicisi

**Files:**
- Create: `scripts/util/thesis_quote_parity.py`
- Test: `tests/test_thesis_quote_parity.py`

**Interfaces:**
- Consumes: `chapters/*.qmd` (verbatim + `(Aile N, rol, yaş)` etiketi), `niteliksel/06_manuscript_outputs/quotes_used.csv`.
- Produces: exit 0=temiz, 1=eşsiz/kaçak alıntı — Faz 6 kapısı ve `tez_checklist_verify.py` alt-kontrolü.

- [ ] **Step 1: Başarısız test yaz** — sahte qmd + manifest ile: (a) etiketli her alıntı manifest'te (aile_no,rol) bulunmalı; (b) etikette gerçek ad/tarih deseni (ör. `\d{2}\.\d{2}\.\d{4}`) FAIL; (c) tanınmayan rol FAIL.

```python
# tests/test_thesis_quote_parity.py
import subprocess, sys, pathlib, tempfile, textwrap
SCRIPT = pathlib.Path(__file__).parents[1]/"scripts/util/thesis_quote_parity.py"
def run(qmd, csv):
    return subprocess.run([sys.executable, str(SCRIPT), "--chapter", qmd, "--manifest", csv], capture_output=True, text=True)
def test_date_in_label_fails(tmp_path):
    q = tmp_path/"c.qmd"; q.write_text('«...» (Aile 11, anne, 12.05.2011)\n', encoding="utf-8")
    m = tmp_path/"m.csv"; m.write_text("quote_id,aile_no,rol,tema,triadik_eksen,kaynak_dosya\n", encoding="utf-8")
    assert run(str(q), str(m)).returncode == 1
```

- [ ] **Step 2: Test FAIL doğrula** → `python3 -m pytest tests/test_thesis_quote_parity.py -q`

- [ ] **Step 3: Denetleyiciyi yaz** — regex ile `«…»`/`"…"` + `(Aile <no>, <rol>, <yaş> yaş)` etiketlerini yakala; rol yüzeyini (anne→mother, hasta/T1DM'li çocuk→t1dm_child, kardeş/sağlıklı kardeş→healthy_sibling) kanonikleştir; tarih/ad deseni varsa FAIL; her etiket (aile_no,rol) manifestte yoksa FAIL; özet rapor bas.

- [ ] **Step 4: Test PASS** → `python3 -m pytest tests/test_thesis_quote_parity.py -q`

- [ ] **Step 5: Commit**

```bash
git add scripts/util/thesis_quote_parity.py tests/test_thesis_quote_parity.py
git commit -m "denetim: tez-düzeyi verbatim parity + de-identify etiket kapısı (+test)"
```

---

## Faz 2 — ch03 Yöntem: COREQ tam hizası

### Task 2.1: ch03 "Nitel Kol" bölümünü COREQ-tam'a taşı

**Files:**
- Modify: `chapters/03_gerec_ve_yontem.qmd:181-` ("Nitel Kol" 6 alt-bölümü)

**Interfaces:**
- Consumes: `coreq_32_completed.md` (Task 1.5), `new/_extracted/nitel coreq uyumlu.txt`.

- [ ] **Step 1:** `niteliksel-arastirma-rehberi-t1dm` skill'iyle bölümü güncelle — ekle: uzman paneli/uzmanlık triangülasyonu, yansıtmalı senaryo-sorusu protokol revizyonu, gözlemci BA rolü + paralinguistik, 21 davet→7 kabul akışı, veri güvenliği/şifreli saklama, etik `09.2023.201`. Düzelt: metindeki "6 aile" → **7 aile** (varsa).

- [ ] **Step 2: "6 aile" kaçağı yok doğrula**

Run: `grep -niE '6 aile|altı aile' chapters/03_gerec_ve_yontem.qmd`
Expected: boş.

- [ ] **Step 3: COREQ guideline denetimi** → `sci-audit:guideline-check --type coreq` (ch03 nitel bölümü); HARD bulgu = 0.

- [ ] **Step 4: Türkçe imla** → `sci-audit:check-turkish` (bölüm); axis G HARD = 0.

- [ ] **Step 5: Commit**

```bash
git add chapters/03_gerec_ve_yontem.qmd
git commit -m "ch03: nitel yöntem COREQ-tam hizası (uzman panel/senaryo/BA/7 aile)"
```

---

## Faz 3 — ch04 Bulgular: verbatim + triadik (ÇEKİRDEK)

> Her tema task'i: (a) matristen quote_id seç + manifest satırları ekle, (b) temayı verbatim + triadik within-case okumayla yaz, (c) parity + imla + COREQ kapısı, (d) commit. Ultracode: tema-başı yazım + eksen-başı denetim yerel Workflow ile paralelleştirilebilir; **katılımcı verisi dış araca gitmez**.

### Task 3.0: ch04 nitel giriş + örneklem/çerçeve + künye çağrısı

**Files:**
- Modify: `chapters/04_bulgular.qmd:1376-1411` ("Niteliksel Kol Bulguları" + "Örneklem ve Analitik Çerçeve")

- [ ] **Step 1:** Örneklem (7 aile/21 görüşme), bilgi gücü, tema mimarisi v3 özeti, triadik okuma mantığı; ch07 künye tablosuna cross-ref.
- [ ] **Step 2:** Render freeze temizliği + kısmi render kontrolü (aşağı Task 6.1'de tam).
- [ ] **Step 3: Commit** → `git commit -m "ch04: nitel giriş + örneklem/çerçeve (v3)"`

### Task 3.1: Tema 1 — Sağlıklı kardeşin görünmeyen yükü (3 alt-tema)

**Files:**
- Modify: `chapters/04_bulgular.qmd:1412-1434`
- Modify: `niteliksel/06_manuscript_outputs/quotes_used.csv` (Tema 1 quote_id satırları)

**Interfaces:**
- Consumes: `triadik_matris_extracted.csv` (eksen: kardes_yasantisi, kisit), `theme_architecture_v3.md` (1.1–1.3).
- Produces: ch04 Tema 1 verbatim'li; manifest Tema 1 satırları.

- [ ] **Step 1:** Matristen sağlıklı-kardeş + ilgili anne/hasta hücrelerini seç (ör. Aile 11/19/26 kardeş); her alt-tema (1.1 gönüllü mahrumiyet, 1.2 nöbetçi kardeş, 1.3 adaletsizlik/hasta otoritesi) için ≥3 farklı aileden verbatim; negatif örüntü (adaleti "hastalığın gereği" kabul ama zedelenme sürüyor).
- [ ] **Step 2:** Seçilen her verbatim için manifest satırı ekle: `{aile}_{rol}_q{NNN},{aile},{rol},Tema 1,{eksen},chapters/04_bulgular.qmd`.
- [ ] **Step 3:** Temayı yaz — özet tablo + verbatim `(Aile N, sağlıklı kardeş, X yaş)` + triadik within-case okuma (aynı olayın anne/hasta/kardeş sesi).
- [ ] **Step 4: Parity + imla**

Run: `python3 scripts/util/thesis_quote_parity.py --chapter chapters/04_bulgular.qmd --manifest niteliksel/06_manuscript_outputs/quotes_used.csv`
Expected: exit 0. Ardından `sci-audit:check-turkish`.

- [ ] **Step 5: Commit** → `git commit -m "ch04 Tema1: sağlıklı kardeş yükü — verbatim + triadik"`

### Task 3.2: Tema 2 — Anneliğin tıbbi bakıcıya kayması (6 alt-tema)

**Files:**
- Modify: `chapters/04_bulgular.qmd:1435-1459`; `niteliksel/06_manuscript_outputs/quotes_used.csv`

**Interfaces:**
- Consumes: eksen `annelik_donusum, kaybetme_korkusu, ergenlik`; alt-tema 2.1–2.6.

- [ ] **Step 1:** Anne hücrelerinden 2.1 suçluluk, 2.2 tıbbi bakıcı/hipervijilans, 2.3 kaybetme korkusu, 2.4 ergenlik-otonomi, 2.5 mahremiyet/eş rolü, 2.6 kardeşte adalet ikilemi için ≥3 aileden verbatim; negatif örüntü (rolü normalleştirme ≠ yük yokluğu).
- [ ] **Step 2:** Manifest satırları (Tema 2).
- [ ] **Step 3:** Yaz — tablo + verbatim `(Aile N, anne, X yaş)` + triadik (anne kaygısı ↔ hasta normalizasyonu ↔ kardeş gözlemi).
- [ ] **Step 4: Parity + imla** (Task 3.1 Step 4 komutu).
- [ ] **Step 5: Commit** → `git commit -m "ch04 Tema2: anneliğin dönüşümü — verbatim + triadik"`

### Task 3.3: Tema 3 — Hastalığın içinden: T1DM'li çocuk (4 alt-tema)

**Files:**
- Modify: `chapters/04_bulgular.qmd:1460-1480`; `niteliksel/06_manuscript_outputs/quotes_used.csv`

**Interfaces:**
- Consumes: eksen `hastalik_algisi, gunluk_sosyal, kisit`; alt-tema 3.1–3.4.

- [ ] **Step 1:** Hasta hücrelerinden 3.1 normalleştirme/avantaj, 3.2 canım acıyor/tedavi yükü, 3.3 farklılık/utanç/stigma, 3.4 el üstünde tutulma/kontrol; negatif örüntü (normalleştirme söylemi ile örtük yük gerilimi).
- [ ] **Step 2:** Manifest satırları (Tema 3).
- [ ] **Step 3:** Yaz — tablo + verbatim `(Aile N, T1DM'li çocuk, X yaş)` + triadik.
- [ ] **Step 4: Parity + imla.**
- [ ] **Step 5: Commit** → `git commit -m "ch04 Tema3: hastalığın içinden — verbatim + triadik"`

### Task 3.4: Tema 4 — Aynı evde üç farklı deneyim (triadik, 4 alt-tema)

**Files:**
- Modify: `chapters/04_bulgular.qmd:1481-1529`; `niteliksel/06_manuscript_outputs/quotes_used.csv`

**Interfaces:**
- Consumes: 8 eksenin triadik kesişimi; alt-tema 4.1–4.4; en az 2 aile için tam triad (anne+hasta+kardeş yan yana).

- [ ] **Step 1:** 4.1 diyabetik düzen, 4.2 "bir şey olacak" korkusu, 4.3 ilgi/adalet/kontrol gerilimi, 4.4 küçük bakıcılar/hasta otoritesi; her alt-temada aynı aileden 3 ses (within-case) + kör-alan/ayrışma vurgusu.
- [ ] **Step 2:** Manifest satırları (Tema 4).
- [ ] **Step 3:** Yaz — triadik karşılaştırmalı okuma + "bütüncül çıktı" cümlesi (deneyim rol-bağımlı; normalleştirme≠tetikte-olma).
- [ ] **Step 4: Parity + imla.**
- [ ] **Step 5: Commit** → `git commit -m "ch04 Tema4: triadik karşılaştırmalı okuma — verbatim"`

### Task 3.5: Joint Display (H5 çekirdeği) nitel tarafını verbatim'le besle

**Files:**
- Modify: `chapters/04_bulgular.qmd:1530-` ("Karma Bulgulara Köprü / Joint Display")

**Interfaces:**
- Consumes: H5 diadik tutarlılık (nicel, DOKUNULMAZ) + Tema 2/4 verbatim örüntüleri.

- [ ] **Step 1:** Joint display'de nicel H5 hücrelerine karşı nitel verbatim örüntüsü (uyum/tamamlayıcılık/ayrışma/genişleme etiketiyle); nitel = "neden/nasıl", nicel = "ne kadar". Nicel sayı/yön değiştirilmez.
- [ ] **Step 2: `galileo_convergence_judge`** (nicel↔nitel ilişki) advisory + parity.
- [ ] **Step 3: Commit** → `git commit -m "ch04: joint display nitel tarafı verbatim'le beslendi (H5 çekirdek)"`

---

## Faz 4 — ch05 Tartışma + entegrasyon

### Task 4.1: 4 temayı literatürle yorumla + karma entegrasyon anlatısı

**Files:**
- Modify: `chapters/05_tartisma_ve_sonuc.qmd` (nitel yorumlama bölümleri)
- Modify: `references/references.bib` (yeni metodoloji/alan kaynakları)

**Interfaces:**
- Consumes: ch04 temaları; dış literatür `evidentia` (yalnız literatür terimi, RBŞ).

- [ ] **Step 1:** `evidentia` narratif derin-lit ile tema-başı alan literatürü getir (FMSF/Knafl, treatment burden, sibling burden, T1DM aile, stigma, informant discrepancy); her iddiaya DOI'li kaynak; bulunmayan = `gap`. **KVKK: sorguya yalnız literatür terimi; katılımcı verisi/verbatim gönderme.**
- [ ] **Step 2:** 4 temayı yorumla; convergence/complementarity/discordance/expansion anlatısını verbatim örüntülerle bağla; nitel temayı nedensellik/etki gibi sunma.
- [ ] **Step 3: Referans kapısı** → `/referans-kapisi` (7-adım: DOI/tam metin/Zotero/claim) yeni kaynaklar için; `bib_hygiene.py all` exit 0.
- [ ] **Step 4: claim-grounding + coreq/jars** → `sci-audit:claim-grounding` (axis B), `sci-audit:guideline-check --type jars` (karma).
- [ ] **Step 5: Commit** → `git commit -m "ch05: nitel temaların yorumu + karma entegrasyon (literatürlü)"`

---

## Faz 5 — ch02 arka plan + ch07 ekler

### Task 5.1: ch02 nitel arka plan güncelleme

**Files:**
- Modify: `chapters/02_genel_bilgiler.qmd` (nitel metodoloji arka planı)

- [ ] **Step 1:** RTA, multi-informant/triadik gelenek, niteliksel tanımlayıcı + fenomenolojik duyarlılık arka planını new/ + literatürle güncelle (v3 terminolojisiyle uyum).
- [ ] **Step 2: imla + claim** → `sci-audit:check-turkish` + `sci-audit:claim-grounding`.
- [ ] **Step 3: Commit** → `git commit -m "ch02: nitel metodoloji arka planı (v3 uyumu)"`

### Task 5.2: ch07 ekler — COREQ-32 tablosu + kod ağacı + de-identify künye + görüşme rehberi

**Files:**
- Modify: `chapters/07_ekler.qmd`
- Create (yerel, gitignored ara): künye türetme scripti girdisi `new/_extracted/Niteliksel demografik.txt`

**Interfaces:**
- Consumes: `coreq_32_completed.md`, `codebook_v3.md`, `Niteliksel demografik.docx` (tarih→yaş/süre türetme), `Niteliksel Araştırma Soruları.docx`.

- [ ] **Step 1: De-identify künye tablosu** — 7 aile × 3 rol: aile_no, rol, **yaş (yıl+ay)**, cinsiyet, **tanı süresi (yıl+ay)**, anne eğitimi. **Doğum/tanı TARİHİ YOK.** (Tarih→süre türetme demografik metinden; ara değer yerelde kalır.)
- [ ] **Step 2: COREQ-32 tablosu** (ekler) — `coreq_32_completed.md`'den; 30 tam + 2 kısmi.
- [ ] **Step 3: Kod ağacı/codebook eki** (COREQ M25) — `codebook_v3.md`'den.
- [ ] **Step 4: Görüşme rehberi eki** — rol-başı sorular (`Niteliksel Araştırma Soruları`'ndan; "6 aile" planlama metni **dahil edilmez**).
- [ ] **Step 5: Tarih/ad kaçağı denetimi**

Run: `grep -nE '[0-9]{2}\.[0-9]{2}\.[0-9]{4}' chapters/07_ekler.qmd`
Expected: boş (yayımda tarih yok).

- [ ] **Step 6: Commit** → `git commit -m "ch07: COREQ-32 + kod ağacı + de-identify künye + rehber ekleri"`

---

## Faz 6 — Doğrulama paketi ve tutarlılık

### Task 6.1: Tam render (freeze temizliği)

- [ ] **Step 1:** `rm -rf _freeze/thesis outputs/quarto/thesis*` (memory: render-freeze).
- [ ] **Step 2:** `quarto render thesis.qmd` — hata yok; nitel bölümler + ekler PDF/HTML'de.
- [ ] **Step 3: Commit** (yeniden üretilen çıktılar) → `git commit -m "render: v3 nitel kol (freeze temizliği sonrası)"`

### Task 6.2: Bütünlük denetim kapıları

- [ ] **Step 1: Tez-düzeyi parity (tüm nitel bölümler)**

Run: `for c in chapters/02_genel_bilgiler.qmd chapters/04_bulgular.qmd chapters/07_ekler.qmd; do python3 scripts/util/thesis_quote_parity.py --chapter $c --manifest niteliksel/06_manuscript_outputs/quotes_used.csv || exit 1; done`
Expected: hepsi exit 0.

- [ ] **Step 2: quote_integrity** → `cd niteliksel && python3 -m pytest tests/test_quote_integrity.py tests/test_extract_triadic_matrix.py -q` → PASS.

- [ ] **Step 3: sci-audit yedi eksen** → `sci-audit:audit` (nitel bölümler) — axis A referans, B claim, E `--type coreq`+`--type jars`, G Türkçe; HARD = 0.

- [ ] **Step 4: Galileo three-tier** → `galileo_judge` + `galileo_reference_prose` + `galileo_coherence_judge`; SOFT-block eşikleri geçildi/insan-override kayıtlı.

- [ ] **Step 5: Kapsamlı checklist** → `python3 scripts/util/tez_checklist_verify.py` — FAIL yok (K5-LIT/NUM kapıları dahil).

- [ ] **Step 6: AI-use kaydı** → `cd niteliksel && ./dmnitel log-ai-use` (evidentia/literatür kullanımı) + gerekirse `/sci-audit:ai-log`.

- [ ] **Step 7: Commit** (rapor/log güncellemeleri) → `git commit -m "doğrulama: nitel v3 tam denetim paketi (parity/coreq/jars/galileo/checklist)"`

### Task 6.3: Tutarlılık son taraması

- [ ] **Step 1:** `grep -rniE '6 aile|altı aile' chapters/ niteliksel/*.md` → boş (7 aile).
- [ ] **Step 2:** ch04↔ch05↔ch07 tema adları + cross-ref tutarlı; joint-display H5 hizası.
- [ ] **Step 3:** `references.bib` dangling yok (`bib_hygiene.py all` exit 0).
- [ ] **Step 4: Commit** (varsa düzeltmeler) → `git commit -m "tutarlılık: 7 aile + cross-ref + bib son tarama"`

---

## Self-Review notları (yazım sonrası)

- **Spec kapsamı:** K1 (Task 3.1–3.4 etiket + Task 1.7 kapı), K2 (Task 1.2–1.4), K3 (Faz 2–5 = ch02/03/04/05/07), K4 (Task 5.2 de-identify künye) — hepsi bir task'e bağlı.
- **Placeholder:** kod adımları gerçek kod içeriyor; prose adımları quote_id/eksen/gate ile somut.
- **Tip tutarlılığı:** rol kanoniği `mother|t1dm_child|healthy_sibling` her yerde (mevcut repo deseni; "patient" KULLANILMAZ); quote_id `{aile}_{rol}_q{NNN}`; aile_no zero-pad-3 tutarlı (extract ↔ manifest ↔ parity).
