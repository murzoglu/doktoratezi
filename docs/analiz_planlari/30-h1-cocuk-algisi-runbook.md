# H1 Çocuk Algısı Runbook

**Kapsam:** KISIM V / 12  
**Uygulama:** `R/16_h1_child_perception.R`, `scripts/R/17_h1_child_perception_audit.R`  
**Son güncelleme:** 2026-04-28

## 1. Kapsam

Bu hat EMBU-C çocuk algısı alt ölçekleri için H1 analizlerini üretir. Long-format çocuk verisi kullanılır; iki çocuk aynı aile içinde kümelendiği için tüm ana modellerde `aile_no_f` random intercept olarak yer alır. Runner satır-düzeyi analiz verisi yazmaz; yalnız aggregate model, diagnostic ve plan tabloları üretir.

## 2. Analitik Veri Çerçevesi

`df_long_scored`, `df_family_ses` ile `aile_no` üzerinden birleştirilir. Family-level kovaryatlar long frame'e analiz aşamasında eklenir:

```text
ses_latent + age_gap + cocuk_sayisi
```

Sürekli kovaryatlar model için z-skorlanır ve ölçekleme metadata'sı `h1_scaling_summary.csv` altında saklanır.

## 3. Birincil Model

Dört EMBU-C alt ölçeği için primary mixed ANCOVA:

```text
outcome ~ role_f + cocuk_yas_z + cinsiyet_f + ses_latent_z + age_gap_z + cocuk_sayisi_z + (1 | aile_no_f)
```

Outcome seti:

| Outcome | Alt ölçek |
|---|---|
| `embu_c_sicaklik_mean` | Duygusal sıcaklık |
| `embu_c_asiri_koruma_mean` | Aşırı koruma |
| `embu_c_reddetme_mean` | Reddetme |
| `embu_c_karsilastirma_mean` | Karşılaştırma |

`role_f`, dört düzeyli grup/rol değişkenidir: `Kontrol_Indeks`, `Kontrol_Kardes`, `DM_Hasta_Indeks`, `DM_Hasta_Kardes`.

## 4. Genişletme Modelleri

| Bileşen | Uygulama |
|---|---|
| 3-way | `role_f * cocuk_yas_z * cinsiyet_f` + DAG kovaryatları + random intercept |
| IRT GRM | Her EMBU-C alt ölçeği için `mirt::mirt(..., itemtype = "graded")` |
| IRT theta modeli | EAP theta skoru primary mixed ANCOVA formülüyle yeniden modellenir |
| Bayesian | `brms` prior/model/seed planı doğrulanır; MCMC sampling default audit/targets içinde çalıştırılmaz |

Bayesian sampling bilinçli olarak manuel tutulur; aksi halde her `targets::tar_make()` Stan sampling maliyetini tetikler. Çalıştırılacaksa `fit_h1_bayesian_model()` açıkça çağrılır ve çıktı `outputs/models/` altında ayrı kararla saklanır.

## 5. Çıktılar

| Çıktı | İçerik |
|---|---|
| `h1_analysis_frame_summary.csv` | Rol/grup sayıları ve outcome tamamlanma özeti |
| `h1_scaling_summary.csv` | Z-skor merkez ve ölçek değerleri |
| `h1_outcome_descriptives.csv` | Rol bazlı dağılım, missing, floor/ceiling |
| `h1_primary_fixed_effects.csv` | Primary mixed model fixed-effect tahminleri ve CI |
| `h1_primary_anova.csv` | Type III / Satterthwaite ANCOVA tabloları |
| `h1_primary_role_pairwise.csv` | `role_f` pairwise karşılaştırmaları, Holm + H1 FDR |
| `h1_primary_diagnostics.csv` | ICC, R2, singularity, AIC/BIC |
| `h1_three_way_tests.csv` | Role x age x sex etkileşim testleri |
| `h1_three_way_emmeans_grid.csv` | 8, 12, 16 yaş grid tahminleri |
| `h1_irt_status.csv` | GRM başarı/skip/fail durumu |
| `h1_irt_item_parameters.csv` | GRM item discrimination/threshold parametreleri |
| `h1_irt_theta_fixed_effects.csv` | Theta mixed model fixed-effect tahminleri |
| `h1_irt_theta_anova.csv` | Theta mixed model Type III tabloları |
| `h1_bayesian_plan.csv` | Bayesian model ve prior preflight |
| `h1_target_summary.csv` | Pipeline kapsama özeti |

## 6. Komutlar

```bash
Rscript tests/test_h1_child_perception.R
Rscript scripts/R/17_h1_child_perception_audit.R
Rscript -e 'targets::tar_make()'
```

## 7. Targets

| Target | İçerik |
|---|---|
| `h1_child_perception_results` | H1 sonuç listesi |
| `h1_primary_fixed_effects_table` | Primary mixed model fixed effects |
| `h1_primary_anova_table` | Primary ANCOVA tabloları |
| `h1_primary_role_pairwise_table` | Rol karşılaştırmaları |
| `h1_three_way_tests_table` | 3-way etkileşim testleri |
| `h1_irt_status_table` | IRT GRM durum tablosu |
| `h1_irt_item_parameters_table` | IRT item parametreleri |
| `h1_irt_theta_fixed_effects_table` | IRT theta mixed model tahminleri |
| `h1_bayesian_plan_table` | Bayesian preflight planı |
| `h1_target_summary` | Pipeline özeti |
