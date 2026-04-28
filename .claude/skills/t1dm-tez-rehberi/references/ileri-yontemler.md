# İleri Yöntemler — SEM, Mediation, Bayesian, Growth

**Ne zaman oku:** lavaan SEM modeli kurarken, multigroup invariance test ederken, mediation
(Hayes / lavaan / mediation paketi) tasarlarken, brms ile Bayesian regresyon kurarken,
blavaan ile Bayesian SEM preflight yaparken, growth model / cross-lagged panel düşünürken,
McElreath'in partial pooling fikri sorulduğunda.

**Kaynaklar:** Kline (2023) *Principles and Practice of SEM* (5th ed.); Brown (2015)
*CFA*; Hayes (2022) *Introduction to Mediation, Moderation, and Conditional Process
Analysis* (3rd ed.); McElreath (2020) *Statistical Rethinking* (2nd ed.); Gelman, Hill &
Vehtari (2021) *Regression and Other Stories*; Bürkner (2017) *brms*; Merkle & Rosseel
(2018) *blavaan*.

---

## SEM ile lavaan — H4 Kanonik Modeli

### Tam Model Yapısı

H4: Annenin Beck depresyon belirti düzeyi (latent) → EMBU-P alt ölçek faktörleri (4 latent)

```r
library(lavaan)

h4_model <- '
  # Ölçüm Modeli — Beck (21 ordinal item)
  beck_dep =~ beck_q01 + beck_q02 + beck_q03 + beck_q04 + beck_q05 +
              beck_q06 + beck_q07 + beck_q08 + beck_q09 + beck_q10 +
              beck_q11 + beck_q12 + beck_q13 + beck_q14 + beck_q15 +
              beck_q16 + beck_q17 + beck_q18 + beck_q19 + beck_q20 + beck_q21

  # Ölçüm Modeli — EMBU-P (29 ordinal item, 4 faktör)
  embu_p_sicaklik     =~ embu_p_q01 + embu_p_q02 + embu_p_q03 + ...
  embu_p_asiri_koruma   =~ embu_p_q07 + embu_p_q08 + ...
  embu_p_reddetme  =~ embu_p_q15 + ...
  embu_p_karsilastirma =~ embu_p_q23 + ...

  # Yapısal Yollar
  embu_p_sicaklik     ~ b1*beck_dep + anne_yas_z + ses_latent_z
  embu_p_asiri_koruma   ~ b2*beck_dep + anne_yas_z + ses_latent_z
  embu_p_reddetme  ~ b3*beck_dep + anne_yas_z + ses_latent_z
  embu_p_karsilastirma ~ b4*beck_dep + anne_yas_z + ses_latent_z

  # Kovaryatlar arası kovaryans
  embu_p_sicaklik     ~~ embu_p_asiri_koruma
  embu_p_sicaklik     ~~ embu_p_reddetme
  embu_p_sicaklik     ~~ embu_p_karsilastirma
  embu_p_asiri_koruma   ~~ embu_p_reddetme
  embu_p_asiri_koruma   ~~ embu_p_karsilastirma
  embu_p_reddetme  ~~ embu_p_karsilastirma
'

fit_h4 <- sem(
  h4_model,
  data       = df_family_ses,
  ordered    = c(paste0("beck_q", sprintf("%02d", 1:21)),
                  paste0("embu_p_q", sprintf("%02d", 1:29))),
  estimator  = "WLSMV",
  cluster    = "aile_no",     # Robust SE (gerçi 1 satır/aile, ama best practice)
  missing    = "pairwise"
)

summary(fit_h4, fit.measures = TRUE, standardized = TRUE)
```

### Multigroup Invariance (DM vs Kontrol)

`semTools::measurementInvariance()` deprecated; el ile karşılaştır:

```r
fit_config <- sem(h4_model, data = df_family_ses, group = "group_dm",
                   ordered = ..., estimator = "WLSMV")

fit_metric <- sem(h4_model, data = df_family_ses, group = "group_dm",
                   ordered = ..., estimator = "WLSMV",
                   group.equal = "loadings")

semTools::compareFit(fit_config, fit_metric)
```

H4 hedef: en az **metric** seviye. Scalar invariance test edilir; ihlal varsa partial scalar
dener (intercept'lerin bir kısmı serbest).

`R/19_h4_beck_parenting_sem.R::run_h4_beck_parenting_sem_pipeline(multigroup_max_step =
"metric_loadings")` parametresi en üst hedefi belirler.

### Sparse Ordinal Categories Collapse

DM grubunda bir Beck maddesinin "3" kategorisi nadirse (n < 5), WLSMV uyarısı geliyorsa:

```r
# multigroup_sparse_collapse_map: kategoriyi 2'ye indirgeme
df_family_ses_sens <- df_family_ses |>
  mutate(across(starts_with("beck_q"),
                ~ ifelse(.x == 3, 2, .x)))
```

Bu **sadece sensitivity frame'inde** yapılır; primer modelde orijinal kategori korunur.
`h4_multigroup_sparse_collapse_map_table` haritalama kaydını tutar.

### Modelden Sonra

```r
# Yapısal yollar
parameterEstimates(fit_h4, standardized = TRUE) |>
  filter(op == "~") |>
  select(lhs, rhs, est, se, pvalue, ci.lower, ci.upper, std.all)

# Modifikasyon indeksleri (dikkatli)
modindices(fit_h4, sort = TRUE, minimum.value = 20)

# Path diagramı
library(semPlot)
semPaths(fit_h4, what = "std", layout = "tree2", residuals = FALSE)
```

---

## Mediation — Hayes vs lavaan vs mediation Paketi

### Klasik Mediation: X → M → Y

Bu projede H4 zaten Beck → EMBU-P latent SEM. Mediation çocuk outcome dahil:
**Beck → EMBU-P → EMBU-C** (indeks çocuk algısı)

#### lavaan ile (Birincil)

```r
med_model <- '
  # a-yol
  embu_p_sicaklik ~ a*beck_total + ses_latent_z + anne_yas_z

  # b-yol + c-prime
  embu_c_sicaklik_aile_mean ~ b*embu_p_sicaklik + c_prime*beck_total +
                              ses_latent_z + age_gap_z + cocuk_sayisi

  # Indirect ve total
  indirect := a * b
  total    := c_prime + a * b
  prop_med := (a * b) / total
'

fit_med <- sem(med_model, data = df_family_ses, se = "bootstrap", bootstrap = 5000)
parameterEstimates(fit_med, boot.ci.type = "bca.simple")
```

**Bootstrap CI:** Bias-corrected and accelerated (BCa) percentile preferred (Hayes 2022).
`bootstrap = 5000` minimum; daha büyük örneklemde 10000.

#### `mediation` Paketi (Causal Mediation, VanderWeele 2015)

```r
library(mediation)

med_fit <- lm(embu_p_sicaklik ~ beck_total + ses_latent_z + anne_yas_z, data = df_family_ses)
out_fit <- lm(embu_c_sicaklik_aile_mean ~ embu_p_sicaklik + beck_total + ses_latent_z +
                age_gap_z + cocuk_sayisi, data = df_family_ses)

med_result <- mediate(
  med_fit, out_fit,
  treat = "beck_total", mediator = "embu_p_sicaklik",
  boot = TRUE, sims = 5000
)
summary(med_result)
plot(med_result)
```

Çıktı:
- **ACME** (Average Causal Mediation Effect) = a × b
- **ADE** (Average Direct Effect) = c-prime
- **Total Effect** = ACME + ADE
- **Proportion Mediated**

#### PROCESS-tarzı (Hayes 2022)

R'da PROCESS makrosu yok; lavaan veya `processR` paketi kullanılır:

```r
# Conditional Indirect Effect (Model 7: a path moderated by W)
moderated_med_model <- '
  embu_p_sicaklik ~ a1*beck_total + a2*age_gap_z + a3*beck_total:age_gap_z + ses_latent_z

  embu_c_sicaklik_mean ~ b*embu_p_sicaklik + c_prime*beck_total +
                    ses_latent_z + cocuk_sayisi

  # Conditional indirect at -1 SD, mean, +1 SD age_gap_z
  ind_low  := (a1 + a3*(-1)) * b
  ind_mean := a1 * b
  ind_high := (a1 + a3*(1)) * b
  index_modmed := a3 * b
'
```

---

## Bayesian Regresyon — `brms`

### Ne Zaman Tercih?

- Örneklem küçük (DM = 120 hasta-aile) ve informative prior var (Pinquart 2013).
- Hipoteze "fark yok" olasılığı atfetmek istiyorsan (BF / posterior tail probability).
- Çok düzeyli yakınsama frequentist'te zor (lme4 convergence warning).

### Pinquart 2013 Meta-Analizinden Prior Türetimi

Pinquart 2013: parenting → child outcome ilişkileri r ≈ 0.13–0.30 aralığında.

```r
# Cohen's d eşdeğeri ≈ 0.26–0.62
# Standardized regresyon katsayısı için: Normal(mean = 0.20, sd = 0.10)
# Bu hem veriyi sürmez hem de tamamen flat değil

library(brms)

m_h1_brms <- brm(
  embu_c_sicaklik_mean_z ~ role_f + cocuk_yas_z + cinsiyet_f +
                      ses_latent_z + age_gap_z + cocuk_sayisi_z +
                      (1 | aile_no_f),
  data    = df_long_scored,
  prior   = c(
    prior(normal(0, 0.5), class = "b"),                    # weakly informative
    prior(normal(-0.20, 0.10), class = "b", coef = "role_fDM_Hasta_Indeks"),  # informed by Pinquart
    prior(student_t(3, 0, 0.5), class = "sd"),             # group-level SD
    prior(student_t(3, 0, 1), class = "sigma")
  ),
  chains  = 4,
  iter    = 4000,
  warmup  = 2000,
  cores   = 4,
  seed    = 20260427,
  control = list(adapt_delta = 0.95)
)

summary(m_h1_brms)
```

### Posterior İncelemesi

```r
library(bayestestR)

# Posterior summary
describe_posterior(m_h1_brms, ci = 0.95)

# ROPE testi: H0: |β| < 0.10 (SESOI)
rope(m_h1_brms, ci = 0.95, range = c(-0.10, 0.10))

# Bayes Factor (Savage-Dickey)
bayesfactor_parameters(m_h1_brms, null = c(-0.10, 0.10))
```

### Posterior Predictive Check

```r
pp_check(m_h1_brms)              # density overlay
pp_check(m_h1_brms, type = "stat", stat = "mean")
pp_check(m_h1_brms, type = "stat_grouped", stat = "mean", group = "role_f")
```

### MCMC Diagnostics (McElreath 2020 Ch. 9)

```r
# R-hat (yakınsama)
rhat(m_h1_brms) |> max()         # ≤ 1.01

# n_eff (effective sample size)
neff_ratio(m_h1_brms) |> min()   # ≥ 0.10 (ideally ≥ 0.50)

# Trace plot
plot(m_h1_brms)

# Divergent transitions
sum(nuts_params(m_h1_brms)$Value[nuts_params(m_h1_brms)$Parameter == "divergent__"])
# 0 olmalı; varsa adapt_delta = 0.99 dene
```

---

## blavaan — Bayesian SEM Preflight

H4 SEM modelini Bayesian'a çevirme:

```r
library(blavaan)

bfit_h4 <- bsem(
  h4_model,
  data    = df_family_ses,
  ordered = c(paste0("beck_q", sprintf("%02d", 1:21)),
               paste0("embu_p_q", sprintf("%02d", 1:29))),
  n.chains = 4,
  burnin   = 4000,
  sample   = 8000,
  target   = "stan",
  seed     = 20260427,
  dp       = dpriors(beta = "normal(0, 1)",
                      lambda = "normal(0, 1)")
)

summary(bfit_h4)
```

**Bu projenin varsayılanı:** blavaan POSTERIOR SAMPLING YAPMAZ; yalnız preflight planı
(`h4_bayesian_sem_plan_table`) oluşturulur. Tam blavaan yürütme zamansal sebeple ileri
faza ertelenir; ön-kayıt buna göre yazılmıştır.

---

## Growth Curve Models (Bu Projede Etkin Değil — Cross-Sectional)

Bu çalışma cross-sectional. Eğer follow-up wave eklenirse:

```r
# lme4 multilevel growth
m_growth <- lmer(outcome ~ time + (1 + time | child_id), data = df_long)

# lavaan Latent Growth Curve
lgc_model <- '
  intercept =~ 1*y1 + 1*y2 + 1*y3 + 1*y4
  slope     =~ 0*y1 + 1*y2 + 2*y3 + 3*y4
  intercept ~ predictor
  slope     ~ predictor
'
```

Bu projede `tartışma` bölümünde **gelecek araştırma önerisi** olarak yer alır.

---

## Cross-Lagged Panel Models (CLPM / RI-CLPM)

Bu projede etkin değil (single-wave). Tartışma bölümünde:

> "Ebeveyn depresyonu ↔ çocuk algısı bidireksiyonelliğini ayrıştırmak için Hamaker, Kuiper
> & Grasman (2015) RI-CLPM modeli minimum 3 dalgada önerilir; mevcut tasarımın kesitsel
> oluşu bu yorumu kısıtlamaktadır."

---

## Hayes-Tarzı Conditional Process Analysis

H1 üç-yönlü etkileşim için (`R/16_h1_child_perception.R::three_way_*`):

```r
m_h1_three_way <- lmer(
  embu_c_subscale_z ~ role_f * cocuk_yas_z * cinsiyet_f +
                       ses_latent_z + age_gap_z + cocuk_sayisi_z +
                       (1 | aile_no_f),
  data = df_long_scored
)

# Simple slopes
library(emmeans)
emtrends(m_h1_three_way, ~ role_f * cinsiyet_f, var = "cocuk_yas_z")

# Johnson-Neyman intervals (continuous moderator)
library(interactions)
johnson_neyman(m_h1_three_way, pred = "role_f", modx = "cocuk_yas_z")
```

---

## SEM Best Practices (Kline 2023 Consensus)

1. **Path diagramını ÖNCE çiz, sonra kodla.**
2. **Anderson-Gerbing iki-adımlı yaklaşım:** önce CFA fit OK, sonra structural model.
3. **N : q oranı ≥ 10 (q = serbest parametre sayısı)**; tercih ≥ 20.
4. **Identification:** df ≥ 0; just-identified model fit edemez.
5. **Multivariate normality kontrolü** ML için. Aksi halde MLR veya WLSMV (ordinal).
6. **Tek bir fit indeksine bel bağlama;** χ², CFI, TLI, RMSEA [90% CI], SRMR — dördünü birden.
7. **Modifikasyon indekslerini sadece teorik destekle.**
8. **Bootstrapping** her zaman tercih (özellikle mediation için BCa).
9. **Sample-size simülasyonu** karmaşık modeller için (`simsem`).

---

## McElreath'tan Partial Pooling Mantığı

McElreath 2020 Ch. 13: Multilevel modeller "adaptive regularization" yapar. Aile-spesifik
intercept tahminleri her aileyi izole tahmin etmek (no pooling) ile tüm aileleri ortalamaya
çekmek (complete pooling) arasında ÖZEL DENGEDE durur.

Bu projede aile küçük (n=2) — partial pooling büyük yardım eder. lme4'ün `(1 | aile_no_f)`
otomatik partial pooling sağlar; brms ile prior bu pooling'in derecesini kontrol eder.

---

## Türkçe APA Sablonu

> "H4 yapısal eşitlik modeli `lavaan` paketinde WLSMV tahmin edicisi ve aile-içi clustering
> ile uygulanmıştır (Rosseel, 2012; Brown, 2015). Beck Depresyon latent faktörü 21 ordinal
> maddeden, EMBU-P alt ölçekleri 4 latent faktörden (Sıcaklık, Aşırı Koruma, Reddetme,
> Karşılaştırma) oluşturulmuştur. Modelin uyumu kabul edilebilir düzeyde olmuştur (χ²(1175,
> N = 241) = 1542.3, p < .001, CFI = .914, TLI = .906, RMSEA = .043 [%95 GA: .038–.048],
> SRMR = .067). Anne yaşı ve SES için ayarlandığında, Beck depresyon Reddetme alt ölçeğini
> β_std = .29 (SE = .07, p < .001) düzeyinde anlamlı yordamış; Sıcaklık üzerindeki etki
> ise β_std = −.18 (SE = .08, p = .024) olmuştur. Multigroup invariance metric düzeyde
> teyit edilmiştir (ΔCFI = .004, ΔRMSEA = .002)."
