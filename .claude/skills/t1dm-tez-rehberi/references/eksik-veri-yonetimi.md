# Eksik Veri Yönetimi — FIML, MI, Yapısal Eksiklik, NMAR Delta

**Ne zaman oku:** Eksik veri raporlanırken, mice/MI parametre seçimi, FIML lavaan kurulumu,
naniar görselleştirmesi, NMAR delta-tipping point analizi, MAR/MCAR test kararı, yapısal
eksiklik (HbA1c sadece DM'de) işlemi.

**Kaynaklar:** Enders (2022) *Applied Missing Data Analysis* (2nd ed.); van Buuren (2018)
*Flexible Imputation of Missing Data* (2nd ed.); Rubin (1987) *Multiple Imputation for
Nonresponse in Surveys*; Little (1988) MCAR test; Carpenter & Kenward (2013) — sensitivity.

---

## Üç Çerçeveli Strateji (Bu Projenin Kanonu)

`R/12_missing_data_frames.R` üzerinden üç paralel çerçeve üretilir:

| Çerçeve | Teknik | Kullanım |
|---------|--------|----------|
| **Primary FIML** (`df_family_missing_fiml_primary`) | Full Information Maximum Likelihood (lavaan içinde `missing = "fiml"`) | H4 SEM modeli, multivariate normality varsayımı yumuşak |
| **Primary MI** (`df_family_missing_mi_primary`) | mice (m = 50, maxit = 30) | H1, H2, H3 frequentist modeller; pooled estimates |
| **DM Klinik Sensitivity MI** (`df_family_missing_mi_clinical_sensitivity`) | mice (HbA1c/dm_yili dahil) | DM grubunda hastalık ağırlığı moderasyonu |
| **Complete Case** (`df_family_missing_complete_case_primary`) | Listwise | YALNIZCA bilgi kaybı görsel referansı; primer yorum DEĞİL |

**Karar mantığı:** Birincil yorum FIML (SEM) veya MI (multilevel/regresyon) altında MAR
varsayımıyla; NMAR delta duyarlılığı ek kontrol.

---

## Eksik Veri Mekanizmaları (Rubin 1976)

| Mekanizma | Tanım | Bu Projedeki Örnek |
|-----------|-------|---------------------|
| **MCAR** (Missing Completely At Random) | Eksiklik gözlemlenen veya gözlenmeyen değerlerden bağımsız | Skala fotokopi hatası |
| **MAR** (Missing At Random) | Eksiklik gözlenen değişkenlerle açıklanabilir | EMBU-C bazı maddelerde yaş kovaryatına bağlı atlama |
| **MNAR** (Missing Not At Random) | Eksiklik gözlemlenmeyen değerlerle ilişkili | Beck'te ağır depresif anne anketi tamamlamamış olabilir |
| **Structural Missing** | Tasarım gereği yok | Kontrol grubunda HbA1c, dm_yili |

**Yapısal eksiklik MI/FIML imputasyonunun KAPSAMI DIŞINDADIR.** Kontrol grubunda HbA1c'yi
imputlama isteme — bu, hastalığı imput etmek demek olur.

---

## MCAR Testi (Little 1988)

```r
library(naniar)

# Sadece analitik değişkenlerde
mcar_vars <- df_family_ses |>
  select(group_dm, ses_latent, age_gap, cocuk_sayisi,
         embu_p_sicaklik_mean, embu_p_asiri_koruma_mean, embu_p_reddetme_mean, embu_p_karsilastirma_mean,
         beck_total)

mcar_result <- naniar::mcar_test(mcar_vars)
print(mcar_result)
# H0: MCAR. Eğer p < .05 → MCAR reddedilir, MAR veya MNAR varsay.
```

**Bu projede:** `missing_mcar_test_table` target'ı bu sonucu kayda alır. Kanonik durum:
MCAR reddedilir → MAR varsayımı altında MI/FIML.

---

## Görselleştirme (`naniar`)

```r
library(naniar); library(ggplot2)

# Eksiklik özet matrisi
vis_miss(mcar_vars)

# Her satır için kombinasyon paterni
gg_miss_upset(mcar_vars, nsets = 8)

# Eksiklik × diğer değişken
ggplot(mcar_vars, aes(x = ses_latent, y = beck_total)) +
  geom_miss_point() +
  facet_wrap(~ group_dm)
```

`R/12_missing_data_frames.R` içinde `missing_pattern_summary_table` bu desenleri tablo
formatında üretir.

---

## Multiple Imputation (MI) — `mice`

### Parametre Seçimi (Bu Projeye Sabitlenmiş)

```r
library(mice)

# m = 50: imputation sayısı. Eski "m=5" kuralı modası geçmiş.
#   Graham, Olchowski & Gilreath (2007): %50 eksiklik için m=40+ gerekir.
# maxit = 30: Markov chain iter sayısı. Kovaryatlar arası karmaşık ilişki için 30 yeterli.
# method: değişken tipine göre belirlenir
```

`R/12_missing_data_frames.R::run_missing_imputation_set(missing_results, m = 50L, maxit = 30L)`
fonksiyonu bunu yürütür.

### Method Plan (Değişken Tipine Göre)

```r
# Otomatik method
method <- mice::make.method(df)

# Manuel düzeltme:
method["beck_total"]      <- "pmm"        # Sürekli, yarı-sürekli (toplam)
method["embu_p_sicaklik_mean"] <- "pmm"        # Standardize sürekli
method["group_dm"]        <- ""           # Imputation YOK (zaten dolu)
method["hba1c"]           <- ""           # Yapısal eksiklik (kontrolde missing tasarım)
method["antidepressant"]  <- "logreg"     # Binary
method["medication_class"]<- "polyreg"    # Multinomial
method["birth_order"]     <- "polr"       # Ordinal
```

`missing_mice_method_plan_table` bu eşlemeyi belgeler.

### Predictor Matrix

```r
predictor_matrix <- mice::quickpred(df, mincor = 0.10, minpuc = 0.25)
# Her değişken için en az r = .10 korelasyonlu olanlar predictor

# Yapısal değişkenleri imputasyon zincirinden çıkar
predictor_matrix["hba1c", ]   <- 0
predictor_matrix[, "hba1c"]   <- 0
predictor_matrix["dm_yili", ] <- 0
predictor_matrix[, "dm_yili"] <- 0

imp <- mice(
  data = df_family_ses,
  m = 50, maxit = 30,
  method = method,
  predictorMatrix = predictor_matrix,
  seed = 20260427
)
```

### Convergence Diagnostics

```r
# Trace plotları
plot(imp, c("beck_total", "embu_p_sicaklik_mean"))
# Farklı zincirler birbirine örtüşmeli (mixing)

# Densite karşılaştırması (gözlenen vs imput)
densityplot(imp, ~ beck_total)

# Stripplot (madde-bazlı)
stripplot(imp, beck_total ~ .imp, pch = 20, cex = 1.2)
```

**Karar:** Trace plotunda trend görünüyorsa `maxit` artır (40, 50). Densite uyuşmazsa
method'u sorgula (örn. PMM yerine norm.predict).

### Pooling (Rubin's Rules)

```r
fit_imp <- with(imp, lmer(embu_p_sicaklik_mean ~ group_dm + ses_latent_z + (1 | aile_no_f)))
pooled <- pool(fit_imp)
summary(pooled, conf.int = TRUE, conf.level = 0.95)
```

**Etki büyüklüğü pooling:** `mice::pool.scalar()` veya manuel.

---

## FIML — `lavaan`

```r
library(lavaan)

fit_h4 <- lavaan::sem(
  model      = h4_sem_model,
  data       = df_family_ses,
  missing    = "fiml",       # Full Information Maximum Likelihood
  estimator  = "MLR",        # Robust ML; WLSMV ordinal item için
  fixed.x    = FALSE
)

# Ordinal SEM (H4 için)
fit_h4_wlsmv <- lavaan::sem(
  model      = h4_sem_model,
  data       = df_family_ses,
  ordered    = paste0("beck_q", sprintf("%02d", 1:21)),
  estimator  = "WLSMV",
  missing    = "pairwise"   # WLSMV ile FIML doğrudan çalışmaz; pairwise alternatif
)
```

**Kritik:** WLSMV + FIML doğrudan desteklenmez. Pairwise deletion veya MI öncesi imputasyon
ile WLSMV birleşimi.

---

## NMAR Delta-Tipping Point Analizi

MAR varsayımının ne kadar tutması gerektiğini test eder. Carpenter & Kenward (2013):

```r
library(mice)

# Delta grid (örn. -0.5, -0.25, 0, +0.25, +0.5 SD shift)
delta <- seq(-0.5, 0.5, by = 0.25)

post_func <- function(delta_val, var = "beck_total") {
  function(imp_object) {
    completed <- mice::complete(imp_object, "long", include = TRUE)
    completed[[var]] <- ifelse(
      is.na(completed[[var]]),
      completed[[var]] + delta_val * sd(completed[[var]], na.rm = TRUE),
      completed[[var]]
    )
    return(completed)
  }
}

results <- map_dfr(delta, function(d) {
  imp_d <- mice(df_family_ses, m = 20, maxit = 20,
                  post = list(beck_total = post_func(d)),
                  seed = 20260427)
  fit <- with(imp_d, lmer(embu_p_sicaklik_mean ~ group_dm + (1 | aile_no_f)))
  pooled <- pool(fit)
  data.frame(delta = d, est = summary(pooled)$estimate[2],
             ci_low = summary(pooled, conf.int = TRUE)$`2.5 %`[2],
             ci_high = summary(pooled, conf.int = TRUE)$`97.5 %`[2])
})

# Tipping point: hangi delta'da etki sıfıra yaklaşıyor?
ggplot(results, aes(delta, est)) +
  geom_line() + geom_ribbon(aes(ymin = ci_low, ymax = ci_high), alpha = 0.2) +
  geom_hline(yintercept = 0, linetype = "dashed")
```

`missing_nmar_delta_grid_table` bu sonucu kayda alır.

**Yorum:** Etki büyüklüğü delta = ±0.5 SD shift'e dayanıyorsa MAR'a duyarlı. Yorumda
"NMAR'a robust" diyebilirsin.

---

## Yapısal Eksiklik (Bu Projeye Özel)

### HbA1c, dm_yili (Sadece DM Grubunda Tanımlı)

```r
# Yanlış: tüm hastaları tek model kovaryatı yap
m_wrong <- lmer(outcome ~ group_dm * hba1c + (1 | aile_no_f), data = df_family_ses)
# Hata: hba1c kontrolde NA → grup × hba1c interaction terimi NA

# Doğru: DM-only stratum sensitivity
df_dm_only <- df_family_ses |> filter(group_dm == 1)
m_dm <- lm(outcome ~ hba1c + dm_yili + ses_latent_z + age_gap_z, data = df_dm_only)

# Tüm örneklem analizinde HbA1c HARİÇ
m_total <- lmer(outcome ~ group_dm + ses_latent_z + age_gap_z + (1 | aile_no_f),
                 data = df_family_ses)
```

**Bu kararın gerekçesi `chapters/02_yontem.qmd` içinde belgelenir; ön-kayıt referansı
`osf.io/pytfe`.**

### Klinik Sensitivity MI

`df_family_missing_mi_clinical_sensitivity` çerçevesi DM-only altkümede HbA1c eksikliğini
imput eder; sonuçlar primer yorumun bir uzantısı olarak raporlanır.

---

## Madde-Bazlı Eksiklik (Ölçek İçi)

EMBU/Beck/KİA maddeleri için:

- **Beck:** Madde-tek-eksikliği bile toplamı NA bırakır (kanonik kural).
- **EMBU/KİA alt ölçek ortalamaları:** Madde mevcutluğu ≥ %50 ise hesaplanır.

Madde-düzeyi MI (örn. mice on items, ardından subscale türetme) — mümkün ama bu projede
varsayılan değil. Çünkü:
- Madde sayısı yüksek (29 EMBU + 21 Beck + 48 KİA)
- mice convergence riski artar
- FIML SEM tercih edilir (H4 için zaten WLSMV)

Eğer madde-düzeyi imputasyon gerekirse:

```r
imp_items <- mice(items_only, m = 30, maxit = 50, method = "pmm",
                   seed = 20260427)
# Sonra her imputed dataset için subscale skorla
imp_long <- mice::complete(imp_items, "long", include = TRUE)
imp_long <- imp_long |>
  rowwise() |>
  mutate(embu_c_sicaklik_mean = mean(c_across(starts_with("embu_c_q_sicaklik_")), na.rm = TRUE)) |>
  ungroup()
imp_with_scores <- as.mids(imp_long)
```

---

## Eksik Veri Tablosu (Raporlama)

```r
library(finalfit)

df_family_ses |>
  ff_glimpse() |>
  pluck("Continuous")

# Veya naniar
miss_var_summary(df_family_ses)
miss_case_summary(df_family_ses)
```

**Tez Tablo eki:** Her değişken için n_missing, %_missing, eksiklik mekanizması (MAR/structural).
`missing_variable_summary_table` ve `missing_block_summary_table` bunu üretir.

---

## Türkçe APA Sablonu

> "Eksik veri analizi `mice` paketinde m = 50 ve maxit = 30 ile çoklu atama (multiple
> imputation) prosedürüyle yürütülmüştür (van Buuren, 2018). Birincil çerçevede sürekli
> değişkenler için predictive mean matching (PMM), kategorik değişkenler için logistic ve
> polytomous regression yöntemleri kullanılmıştır (`R/12_missing_data_frames.R`). DM-spesifik
> klinik değişkenler (HbA1c, dm_yili) tasarım kaynaklı yapısal eksiklik olduğundan
> imputasyon zincirine dahil edilmemiş, yalnız DM altkümesinde duyarlılık analizi
> çerçevesinde kullanılmıştır. MAR varsayımı altında pooled (Rubin kuralları) tahminler
> raporlanmış, NMAR'a duyarlılık delta-tipping point grid (δ = −0.5, …, +0.5 SD) ile
> incelenmiştir; etki büyüklüğü tahmini δ = ±0.25 SD shift'e robusttur (Tablo Y)."

---

## Sık Yapılan Hatalar

1. **Listwise deletion ile devam etme** — bu projenin protokolünde zayıflık olarak
   raporlanmış sayılır.
2. **`m = 5` ile yetinmek** — Graham 2007 sonrası modası geçmiş. m ≥ 40.
3. **HbA1c'yi tüm örnekleme imput** — yapısal eksikliği bilinçli imput etmek bilim ihlali.
4. **MCAR testi yok diye atlamak** — naniar::mcar_test bir satır.
5. **Convergence diagnostiklerini ihmal** — trace plot her zaman incele.
6. **Pooled estimates yerine ortalama estimate'ı raporlamak** — Rubin kuralları SE doğru
   düzeltmesi için zorunlu.
7. **NMAR sensitivity yok** — etik açıdan zayıflık; en azından delta = ±0.25 SD raporla.
8. **FIML + WLSMV kombinasyonu olduğunu sanmak** — desteklenmez; pairwise veya MI öncesi.
9. **Madde-düzeyi vs. skor-düzeyi imputasyon karışıklığı** — bu projede skor-düzeyi
   varsayılan, madde-düzeyi sadece psikometrik validasyon raporlarında.
10. **Beck için %50 madde kuralı uygulamak** — yanlış. Beck için tüm 21 madde tam olmalı.
