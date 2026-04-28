# Doktora Tezi — Tip 1 Diyabet & Ebeveynlik Tutumu

Quarto + R doktora tezi: T1DM tanılı çocuklar, sağlıklı kardeşler ve annelerinde EMBU / Beck / KİA ölçek analizleri.

## Komutlar

```bash
# Tezi render et (chapters/ → outputs/quarto/)
quarto render

# Pipeline (targets) — path/raw manifest + KISIM II-XIII hash kontrollü veri yükleme/skor/SES/eksik veri/Tablo 1/DAG/PS/H1-H5/VI-XII/APA figür+tablo
Rscript -e 'targets::tar_make()'

# EMBU stage runner'ları (sırasıyla)
Rscript scripts/R/01_embu_stage1_standardize.R
Rscript scripts/R/02_embu_stage2_likert4.R
Rscript scripts/R/03_embu_stage3_family.R

# Testler (stopifnot tabanlı, çıktı sessizse PASS)
Rscript tests/test_embu_stage1.R
Rscript tests/test_embu_stage2_likert4.R
Rscript tests/test_embu_stage3_family.R

# Paket yönetimi
Rscript -e 'renv::status()'
Rscript -e 'renv::restore()'
```

## Mimari

- `thesis.qmd` — kök Quarto belgesi, `chapters/01..05_*.qmd` dosyalarını include eder
- `_targets.R` + `R/00_paths.R`, `R/01_io.R`, `R/07_reproducibility.R`, `R/10_derived_scores.R`, `R/11_ses_composites.R`, `R/12_missing_data_frames.R`, `R/13_table1_smd.R`, `R/14_causal_dag.R`, `R/15_propensity_score.R`, `R/16_h1_child_perception.R`, `R/17_h2_sibling_relationships.R`, `R/18_h3_parent_self_report.R`, `R/19_h4_beck_parenting_sem.R`, `R/20_h5_dyadic_concordance.R`, `R/21_robustness_sensitivity.R`, `R/22_bayesian_parallel.R`, `R/23_mediation.R`, `R/24_latent_profile.R`, `R/25_clinical_utility.R`, `R/26_network_analysis.R`, `R/27_dm_subanalyses.R`, `R/28_apa_figures.R`, `R/29_apa_tables.R`, `R/30_thesis_mapping.R`, `R/31_final_plans.R` — `targets` orkestrasyonu, hash kontrollü kanonik veri yükleme, türetilmiş skorlar, SES kompozitleri, eksik veri çerçeveleri, Tablo 1/SMD dengesi, Causal DAG stratejisi, PS/IPTW/Matching altyapısı, H1-H5 analizleri, KISIM VI-XII genişletilmiş analizleri, KISIM XIII/40-42 APA figür+tablo+bölüm/yayın planı ve KISIM XV-XVI risk/zaman paketi
- `R/` — **kütüphane** (saf fonksiyonlar, `source()` ile yüklenir, side-effect yok)
- `scripts/R/` — **runner**'lar (R/ fonksiyonlarını çağırıp dosya yazar)
- `tests/` — her R/ modülü için karşılık (`stopifnot` ile assertion)
- `data/raw/Raw Data - Final.csv` — tarihsel ham veri girişi; analiz için doğrudan kullanılmaz
- `data/processed/FINAL_REFERENCE__analysis_base_family.csv` ve `data/processed/FINAL_REFERENCE__analysis_base_long.csv` — kilitli kanonik analiz baz CSV'leri
- `outputs/tables/`, `outputs/figures/`, `outputs/models/` — analiz artefaktları (gitignored)
- `references/references.bib` + `apa.csl` — bibliyografya
- `renv/` + `renv.lock` — paket reprodüksiyonu

## Kritik domain bilgisi

- **Veri yapısı:** 482 satır = **241 aile × 2 katılımcı** (1 indeks çocuk + 1 kardeş). DM indeks aile 120, kontrol indeks aile 121. Her satır bağımsız değildir → multilevel/aile-içi ICC zorunlu.
- **EMBU formları:** Final kanonda 29 P-soru + 29 C-soru vardır; `q01-q29` ebeveyn ve çocuk formunda aynı semantik sırayı temsil eder. Kanonik formlar için bkz. [`docs/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md`](docs/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md) ve [`docs/KANONIK_KISALTILMIS_EMBU_COCUK.md`](docs/KANONIK_KISALTILMIS_EMBU_COCUK.md).
- **Kanonik form öncesi EMBU karar geçmişi arşivdedir.** Eski madde mimarisi, standardizasyon/refinement notları ve Stage 1-3 CSV raporları [`archive/2026-04-26_pre_canonical_embu/`](archive/2026-04-26_pre_canonical_embu/) altına taşınmıştır.
- **Likert standardı:** Final kanonik CSV'lerde EMBU-P ve EMBU-C itemları 4'lü Likert standardındadır.
- **Geçerli aralık dışı değerler** (ör. tipo `14`, `21`) Stage 1'de NA'ya çevrilir; kanonik form öncesi outlier raporları arşivdedir.
- **PII koruması:** `ad.*soyad` regex'iyle eşleşen kolonlar Stage 1'de düşürülür. `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/` `.gitignore`'da — **commit etmeyin**.
- **Aile anahtarı:** `aile_no` × `cocuk_no` birincil anahtar. Aileler arası eşleştirme `R/04_embu_stage3_family.R` üzerinden.

## Aktif analiz durumu (2026-04-26 itibarıyla)

- **Kanonik analiz baz kilidi yürürlükte.** Final CSV üzerinde herhangi bir değişiklikten önce [`data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`](data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock), kanonik P/C formları ve [`docs/FINAL_REFERENCE_VERI_HARITASI.md`](docs/FINAL_REFERENCE_VERI_HARITASI.md) okunmalıdır.
- Kanonik form öncesi dokümantasyon aktif karar kaynağı değildir; yalnız karar geçmişi olarak arşivde tutulur.
- **Paralel ilerleyen:** Beck Depresyon ve KİA (Kardeş İlişkileri Anketi).
- Yöntem kararlarının arşivi: [`docs/method_archive/`](docs/method_archive/).

## Yazım & dil

- Tez ana dili **Türkçe** (`lang: tr`); kod yorumları ve commit mesajları da Türkçe tercih edilir
- Quarto exec defaults: `echo: false`, `warning: false`, `message: false`, `freeze: auto`
