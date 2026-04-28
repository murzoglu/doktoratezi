# Diseminasyon ve Yayın Planı

Bu plan KISIM XIII/42 için izlenecek üç-makale stratejisini ve açık bilim paketini tanımlar. Plan, satır-düzeyi veri paylaşımı içermez; yalnız aggregate tablo, figür, kod ve metodoloji artefaktları üzerinden yürütülür.

## Üç Makale Stratejisi

| Makale | Odak | Hedef |
|---|---|---|
| M1 | H1 + H5 çocuk algısı ve diadik tutarlılık | Pediatric Diabetes / Journal of Pediatric Psychology |
| M2 | H3 + H4 + mediation anne ruh sağlığı hattı | Diabetic Medicine / Journal of Family Psychology |
| M3 | Psikometrik validasyon + robustluk/Bayesian yöntem | Methods in Psychology / Frontiers in Psychology |

## Çekirdek Eşleme

- **M1:** `apa_t06`, `apa_t07`, `apa_t13`, `h1_forest`, `h5_ba_grid`, `h5_rsa_surface`
- **M2:** `apa_t10`, `apa_t11`, `apa_t12`, `apa_t14`, `h3_stratified_forest`, `h4_sem_path`, `mediation_effects`
- **M3:** `psychval_*`, `apa_t19`, `apa_t20`, `apa_t21`, `specification_curve`, `sensemakr_contour`, `bayesian_diagnostics`

## Açık Bilim Sınırı

- Kod, SAP, runbook, Quarto chapter'ları ve aggregate çıktılar public pakete uygundur.
- `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/`, satır-düzeyi `data/processed/*.csv`, `_targets/` ve credential dosyaları public pakete dahil edilmez.
- OSF ve Zenodo paketlerinde `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` paylaşılabilir; satır-düzeyi CSV paylaşımı controlled-access kararı gerektirir.

## Denetlenebilir Çıktılar

Bu plan `R/31_final_plans.R`, `scripts/R/32_final_plans_audit.R` ve `tests/test_final_plans.R` ile denetlenir. Aggregate CSV çıktıları `outputs/tables/final_plan_*.csv` altında üretilir.
