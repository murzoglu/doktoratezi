# H2 Kardeş İlişkisi Runbook

**Kapsam:** KISIM V / 13  
**Uygulama:** `R/17_h2_sibling_relationships.R`, `scripts/R/18_h2_sibling_relationships_audit.R`  
**Son güncelleme:** 2026-04-28

## 1. Kapsam

Bu hat Kardeş İlişkileri Anketi / SRQ yüksek-düzey skorları için H2 analizlerini üretir. Analizler iki düzeyde yürütülür:

- `long` çocuk satırı: index ve kardeş bildirimleri, aile içinde bağımlı.
- `family_mean` aile satırı: iki çocuğun SRQ ortalaması, grup karşılaştırması ve moderasyon.

Runner satır-düzeyi analiz verisi yazmaz; yalnız aggregate test, model, diagnostic ve CFA tabloları üretir.

## 2. Outcome Seti

| Outcome | Boyut |
|---|---|
| `srq_ho_warmth_mean` | Sıcaklık / yakınlık |
| `srq_ho_status_mean` | Statü / güç |
| `srq_ho_conflict_mean` | Çatışma |
| `srq_ho_rivalry_mean` | Rekabet |

`df_long_scored`, `df_family_ses` ile `aile_no` üzerinden birleştirilir. Family-level kovaryatlar analiz aşamasında eklenir:

```text
age_gap + same_sex + ses_latent
```

`age_gap` ve `ses_latent` z-skorlanır; merkez/ölçek metadata'sı `h2_scaling_summary.csv` içinde tutulur.

## 3. Analiz Bileşenleri

| Bileşen | Uygulama |
|---|---|
| Aile-mean Welch | Her SRQ boyutu için aile ortalaması üzerinden DM-Kontrol Welch t-test |
| Etki büyüklüğü | DM - Kontrol mean difference CI + Hedges g yaklaşık CI |
| APIM / dyadic mixed | `outcome ~ group_f * family_role_f + age_gap_z`, random `~1 | aile_no_f`, role-specific residual variance |
| Age-gap moderation | Family-mean `outcome ~ group_f * age_gap_z * same_sex + ses_latent_z`, Type III ANOVA |
| Olsen-Kenny CFA | `srq_4`, `srq_20`, `srq_36` quarreling item setiyle distinguishable dyad CFA |

Olsen-Kenny CFA aktif skor haritasındaki quarreling item setini kullanır; item düzeyi ölçüm hatasını ayıran latent index-sibling korelasyonu `h2_olsen_kenny_latent_correlations.csv` içinde raporlanır.

## 4. Çıktılar

| Çıktı | İçerik |
|---|---|
| `h2_scaling_summary.csv` | Z-skor merkez/ölçek değerleri |
| `h2_long_descriptives.csv` | Grup × aile rolü SRQ dağılımları |
| `h2_family_mean_descriptives.csv` | Aile-mean SRQ dağılımları |
| `h2_family_mean_welch_tests.csv` | Welch t-test, mean difference, Hedges g, FDR |
| `h2_apim_fixed_effects.csv` | APIM fixed-effect tahminleri |
| `h2_apim_diagnostics.csv` | APIM model diagnostic'leri |
| `h2_age_gap_moderation_fixed_effects.csv` | Moderasyon LM katsayıları |
| `h2_age_gap_moderation_anova.csv` | Type III moderation ANOVA |
| `h2_age_gap_moderation_diagnostics.csv` | Moderasyon model diagnostic'leri |
| `h2_olsen_kenny_status.csv` | Dyadic CFA başarı/skip/fail durumu |
| `h2_olsen_kenny_fit_measures.csv` | Dyadic CFA fit ölçüleri |
| `h2_olsen_kenny_latent_correlations.csv` | Index-sibling latent korelasyonu |
| `h2_olsen_kenny_parameter_estimates.csv` | CFA parametre tahminleri |
| `h2_target_summary.csv` | Pipeline kapsama özeti |

## 5. Komutlar

```bash
Rscript tests/test_h2_sibling_relationships.R
Rscript scripts/R/18_h2_sibling_relationships_audit.R
Rscript -e 'targets::tar_make()'
```

## 6. Targets

| Target | İçerik |
|---|---|
| `h2_sibling_relationships_results` | H2 sonuç listesi |
| `h2_family_mean_welch_tests_table` | Aile-mean Welch sonuçları |
| `h2_apim_fixed_effects_table` | APIM fixed effects |
| `h2_age_gap_moderation_anova_table` | Age-gap × same-sex moderation ANOVA |
| `h2_olsen_kenny_status_table` | Dyadic CFA durum tablosu |
| `h2_olsen_kenny_fit_measures_table` | Dyadic CFA fit ölçüleri |
| `h2_olsen_kenny_latent_correlations_table` | Latent index-sibling korelasyonu |
| `h2_target_summary` | Pipeline özeti |
