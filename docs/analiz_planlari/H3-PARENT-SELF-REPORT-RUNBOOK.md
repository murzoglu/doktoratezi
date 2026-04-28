# H3 Anne Öz-Rapor Runbook

**Kapsam:** KISIM V / 14  
**Uygulama:** `R/18_h3_parent_self_report.R`, `scripts/R/19_h3_parent_self_report_audit.R`  
**Son güncelleme:** 2026-04-28

## 1. Analiz Çerçevesi

H3, aile düzeyindeki anne öz-rapor EMBU-P alt ölçeklerini DM ve kontrol aileleri arasında karşılaştırır:

- `embu_p_sicaklik_mean`
- `embu_p_asiri_koruma_mean`
- `embu_p_reddetme_mean`
- `embu_p_karsilastirma_mean`

Birincil model SAP 14.1 ile uyumludur:

```r
outcome ~ group_f + anne_yas_z + ses_latent_z + age_gap_z + cocuk_sayisi
```

`scale(...)` terimleri analiz öncesinde deterministik z-skor kolonlarına çevrilir. `cocuk_sayisi`, SAP taslağındaki gibi ham aile büyüklüğü kovaryatı olarak tutulur.

## 2. Duyarlılık Katmanları

Antidepresan duyarlılık analizi üç çerçevede çalışır:

| Çerçeve | Formül | Eşik |
|---|---|---|
| Tüm anneler, AD ayarlı | `outcome ~ group_f + anne_antidepresan_f + anne_yas_z + ses_latent_z` | Her grup için en az 5 |
| Antidepresan kullanmayan | `outcome ~ group_f + anne_yas_z + ses_latent_z` | Her grup için en az 5 |
| Yalnız antidepresan kullanan | `outcome ~ group_f + anne_yas_z + ses_latent_z` | Her grup için en az 5 |

IPTW versiyonu, KISIM III / 11 propensity score hattındaki `iptw_trimmed` ağırlığını kullanır:

```r
outcome ~ group_f + anne_yas_z + ses_latent_z
```

IPTW standart hatları `sandwich::vcovHC(type = "HC3")` ile hesaplanır. `sandwich` yoksa model-based varyans etiketiyle fallback yapılır.

## 3. Komutlar

```bash
Rscript tests/test_h3_parent_self_report.R
Rscript scripts/R/19_h3_parent_self_report_audit.R
Rscript -e 'targets::tar_make()'
```

Runner yalnız aggregate tablo üretir; satır düzeyi analiz frame'i, PS ağırlıkları veya model frame'i dosyaya yazılmaz.

## 4. Outputs

| Output | İçerik |
|---|---|
| `outputs/tables/h3_scaling_summary.csv` | Z-skor merkez ve ölçek parametreleri |
| `outputs/tables/h3_outcome_descriptives.csv` | EMBU-P alt ölçek betimleyicileri, grup bazında |
| `outputs/tables/h3_antidepressant_counts.csv` | Antidepresan kullanım sayıları ve DM-Kontrol SMD |
| `outputs/tables/h3_primary_fixed_effects.csv` | Birincil ANCOVA tüm katsayıları |
| `outputs/tables/h3_primary_group_effects.csv` | `group_fDM` etkisi, CI, standardize beta ve FDR |
| `outputs/tables/h3_primary_diagnostics.csv` | Model n, R2, AIC/BIC ve grup sayıları |
| `outputs/tables/h3_antidepressant_stratified_group_effects.csv` | AD-ayarlı ve AD-stratified `group_fDM` etkileri |
| `outputs/tables/h3_iptw_fixed_effects.csv` | IPTW model tüm katsayıları |
| `outputs/tables/h3_iptw_group_effects.csv` | IPTW `group_fDM` etkisi, HC3 SE, CI, FDR |
| `outputs/tables/h3_iptw_diagnostics.csv` | IPTW model tanıları ve ağırlık özetleri |
| `outputs/tables/h3_target_summary.csv` | Pipeline kapsam özeti |

## 5. Gerçek Veri Audit Özeti

`scripts/R/19_h3_parent_self_report_audit.R` son çalıştırmada şu kapsamı doğruladı:

| Metrik | Değer |
|---|---:|
| Aile sayısı | 241 |
| PS/IPTW satırı | 241 |
| Antidepresan kullanımı, toplam | 46 |
| Antidepresan kullanımı, DM | 35 |
| Antidepresan kullanımı, kontrol | 11 |
| Primary model | 4 |
| Stratified fitted satır | 12 / 12 |
| IPTW model | 4 |
| Maksimum trimmed IPTW | 1.361 |

Primary ve IPTW `group_fDM` etkilerinde H3 içinde FDR < .05 sonuç yoktur. Bu bulgu klinik veya nedensel yokluk iddiası olarak değil, SAP'de tanımlı total-effect model altında gözlenen küçük ve belirsiz grup farkları olarak raporlanmalıdır.
