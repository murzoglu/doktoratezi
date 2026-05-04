# SES Kompozit Türetme Runbook

**Kapsam:** KISIM II / 7  
**Uygulama:** `R/11_ses_composites.R`, `scripts/R/12_derive_ses_audit.R`  
**Son güncelleme:** 2026-04-27

## 1. Kapsam

Bu katman final CSV dosyalarını değiştirmez. SES değişkenleri `df_family_scored` üzerinde üretilir ve `df_family_ses` hedefi olarak `_targets/` cache'inde tutulur.

## 2. Üç Katman

| Katman | Değişkenler |
|---|---|
| A: deterministik aile SES alanları | `max_aile_egitim`, `mean_aile_egitim`, `egitim_fark`, `cift_kazanc`, `kalabalik_indeksi` |
| B: materyal indeks | `material_index`, `material_quintile` |
| C: kompozit/latent SES | `ses_composite_eq`, `ses_hollingshead`, `ses_latent` |

Yüksek değer daha avantajlı SES anlamına gelir. Materyal indeks yönü ev sahipliği, oda sayısı ve araba sahipliği anchor'ı ile pozitif SES yönüne sabitlenir.

## 3. Model Kararları

| Karar | Uygulama |
|---|---|
| Materyal indeks | `ev_sahipligi`, `ev_oda_sayisi`, `arabaniz_var_mi` üzerinde polychoric PCA |
| Ev sahipliği diagnostic | `abs(loading) < 0.20` ise `ev_sahipligi` materyal indeksten çıkarılır |
| Eş-ağırlıklı kompozit | `edu_z`, `isei_z`, `material_z` ortalaması |
| Hollingshead tipi kompozit | `(3 * edu_z + 5 * isei_z) / 8` |
| Latent SES | `SES =~ egitim_durumu + es_egitim_durumu + aile_isei08 + material_index`, WLSMV |

## 4. Komutlar

```bash
Rscript tests/test_ses_composites.R
Rscript scripts/R/12_derive_ses_audit.R
Rscript -e 'targets::tar_make()'
```

Runner çıktıları:

- `outputs/tables/ses_diagnostics.csv`
- `outputs/tables/ses_material_loadings.csv`
- `outputs/tables/ses_cfa_fit_measures.csv`
- `outputs/tables/ses_component_summary.csv`
- `outputs/tables/ses_correlation_table.csv`
- `outputs/tables/ses_target_summary.csv`

Bu dosyalar aggregate/metadata düzeyindedir ve git dışıdır. Satır-düzeyi `df_family_ses` dışarı yazılmaz.

## 5. Targets

| Target | İçerik |
|---|---|
| `ses_results` | SES kompozit sonuç listesi |
| `df_family_ses` | SES eklenmiş family analiz nesnesi |
| `ses_diagnostics_table` | materyal indeks + latent CFA diagnostic |
| `ses_material_loadings_table` | materyal PCA değişken yükleri |
| `ses_cfa_fit_measures_table` | latent SES fit ölçüleri |
| `ses_component_summary_table` | SES değişken kapsam özeti |
| `ses_correlation_summary_table` | SES bileşen korelasyonları |
| `ses_target_summary` | eklenen kolon ve satır özeti |
