# Hash Doğrulama ve Veri Yükleme Runbook

**Kapsam:** KISIM II / 5  
**Kanonik kilit:** `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`  
**Uygulama:** `R/01_io.R`, `scripts/R/10_hash_validate_load.R`  
**Son güncelleme:** 2026-04-27

## 1. Temel Kural

Kanonik `FINAL_REFERENCE__analysis_base_family.csv` ve `FINAL_REFERENCE__analysis_base_long.csv` dosyaları hash doğrulaması geçmeden analiz nesnesi olarak yüklenmez.

Yükleme sırası:

1. Lock dosyası okunur ve `LOCKED_CANONICAL_ANALYSIS_BASE` statüsü doğrulanır.
2. CSV dosyasının SHA-256 özeti hesaplanır.
3. Hash, lock dosyasındaki beklenen değerle karşılaştırılır.
4. CSV okunur.
5. Satır ve sütun sayıları lock dosyasındaki değerlerle karşılaştırılır.
6. Veri nesnesine doğrulama attribute'ları eklenir.
7. Family ve long hazırlık katmanları yalnız faktör ve yapısal alan ekler.

## 2. Komutlar

```bash
Rscript tests/test_final_reference_loading.R
Rscript scripts/R/10_hash_validate_load.R
Rscript -e 'targets::tar_make()'
```

Runner çıktıları:

- `outputs/tables/final_reference_validation_manifest.csv`
- `outputs/tables/final_reference_load_summary.csv`

Bu dosyalar metadata düzeyindedir ve git dışıdır.

## 3. Targets Hattı

`_targets.R` içinde KISIM II veri hedefleri:

| Target | İçerik |
|---|---|
| `final_reference_paths` | Lock, family CSV ve long CSV yolları |
| `lock_file` | Kanonik lock dosyası |
| `family_csv`, `long_csv` | Kanonik CSV file target'ları |
| `final_reference_manifest` | Hash, satır ve sütun karşılaştırması |
| `df_family_raw`, `df_long_raw` | Doğrulanmış ham analiz nesneleri |
| `df_family`, `df_long` | Faktörleştirilmiş hazırlık nesneleri |
| `final_reference_loaded_summary` | Metadata özeti |
| `df_family_scored`, `df_long_scored` | KISIM II / 6 türetilmiş skor nesneleri |
| `df_family_ses` | KISIM II / 7 SES kompozitleri eklenmiş family nesnesi |
| `df_family_missing_fiml`, `df_family_missing_mi_primary` | KISIM II / 8 primary eksik veri frame'leri |
| `df_family_missing_mi_clinical_sensitivity` | KISIM II / 8 DM-klinik sensitivity MI frame'i |
| `table1_family_summary_table`, `table1_smd_balance_table` | KISIM III / 9 Tablo 1 ve SMD denge tabloları |
| `causal_dag_adjustment_sets_table`, `causal_dag_covariate_strategy_table` | KISIM III / 10 Causal DAG strateji tabloları |
| `df_family_propensity`, `propensity_balance_before_after_table` | KISIM III / 11 PS/IPTW/Matching nesneleri ve aggregate denge tablosu |
| `h1_primary_anova_table`, `h1_irt_status_table`, `h1_bayesian_plan_table` | KISIM V / 12 H1 çocuk algısı model, IRT ve Bayesian preflight tabloları |
| `h2_family_mean_welch_tests_table`, `h2_apim_fixed_effects_table`, `h2_olsen_kenny_latent_correlations_table` | KISIM V / 13 H2 kardeş ilişkisi family-mean, APIM ve dyadic CFA tabloları |
| `h3_primary_group_effects_table`, `h3_antidepressant_stratified_group_effects_table`, `h3_iptw_group_effects_table` | KISIM V / 14 H3 anne öz-rapor primary, antidepresan sensitivity ve IPTW tabloları |
| `h4_latent_sem_structural_paths_table`, `h4_multigroup_comparison_table`, `h4_bayesian_sem_plan_table` | KISIM V / 15 H4 Beck -> EMBU-P latent SEM, reduced multi-group screen ve Bayesian preflight tabloları |

`_targets/` satır-düzeyi veri cache'i içerebilir; bu klasör Git, OSF public paket ve Docker context dışında kalır.

## 4. Hazırlık Katmanı

`prepare_family()` şu alanları ekler:

- `aile_no_f`
- `group_f`
- `cinsiyet_idx_f`
- `cinsiyet_sib_f`
- `egitim_ord`
- `age_gap`
- `same_sex`
- `birth_order_diff`
- `tani_yasi`
- `hba1c_target`

`prepare_long()` şu alanları ekler:

- `aile_no_f`
- `role_f`
- `group_f`
- `family_role_f`
- `cinsiyet_f`
- `age_cat`

Bu katmanda ölçek toplamı, alt ölçek skoru, reverse coding veya imputation yapılmaz.

## 5. Docker Kullanımı

Varsayılan Docker imajı satır-düzeyi veriyi içermez. Tam veri doğrulama hattı için `data/processed` salt-okunur mount edilir:

```bash
docker run --rm \
  -v "$PWD/data/processed:/home/rstudio/project/data/processed:ro" \
  t1dm-ebeveyn-repro \
  bash -lc "Rscript scripts/R/07_verify_reproducibility.R && Rscript scripts/R/10_hash_validate_load.R && Rscript -e 'targets::tar_make()'"
```

Mount yoksa Docker varsayılan komutu yalnız veri gerektirmeyen hedefleri ve Quarto HTML render'ı çalıştırır.
