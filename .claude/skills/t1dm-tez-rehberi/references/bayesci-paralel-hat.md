# KISIM XII — Bayesci Paralel Hat

> SAP v3.0 §37–39. **Tüm primer hipotezler için frequentist + Bayesian dual reporting standardı.**
> brms multilevel + Bayes Factor + WAIC/LOO + model stacking. **[KISMEN AKTİF]** —
> H1 preflight için brms zaten kullanılıyor; tüm hipotezler için genişletilmesi gerekir.

## Niye Bayesian Paralel?

Tezin savunmasında jüri sorabilir:
- "Etki ne kadar kesin?" — Frequentist CI ≠ olasılık aralığı; Bayesian credible interval direkt olasılık.
- "Etki anlamsız çıktı; sıfır mı?" — Frequentist'te ayırt edilemez; Bayesian BF + ROPE çözer.
- "Önceki literatür beklentilerini nasıl entegre ettiniz?" — Pinquart 2013 meta-analiz prior.

> **Tezde dual reporting kuralı:** Her primer hipotez için **frequentist (p, FDR) + Bayesian
> (BF, ROPE, pd)** birlikte tablo halinde sunulur.

## 1. H1 Bayesian Multilevel (brms)

### Pinquart-temelli prior derivation

Pinquart 2013 meta-analiz: kronik hastalık × ebeveynlik d ≈ 0.40, %95 CI [0.25, 0.55] →
**SD ≈ 0.077**. Tezde **3× geniş prior** (skeptical / weakly informative).

```r
library(brms); library(bayestestR); library(bayesplot)

run_h1_bayesian <- function(df_long, outcome) {
  priors <- c(
    # Group fixed effects (DM-Kontrol fark beklentisi)
    prior(normal(0.30, 0.50),  class = b, coef = "role_fDM_Hasta_Indeks"),
    prior(normal(0.20, 0.50),  class = b, coef = "role_fDM_Hasta_Kardes"),
    prior(normal(-0.10, 0.30), class = b, coef = "role_fKontrol_Kardes"),

    # Diğer fixed effects — daha geniş
    prior(normal(0, 1),        class = b),

    # Random effect SD (Gelman 2006 weak-half-Cauchy)
    prior(student_t(3, 0, 2.5), class = sd),

    # Residual SD
    prior(student_t(3, 0, 2.5), class = sigma)
  )

  fml <- as.formula(paste(outcome,
    "~ role_f + scale(cocuk_yas) + cinsiyet_f + scale(ses_latent) +
       scale(age_gap) + (1 | aile_no_f)"))

  m_bayes <- brms::brm(
    fml, data = df_long,
    family = gaussian(),
    prior = priors,
    chains = 4, iter = 4000, warmup = 1500,
    seed = 20260427,
    cores = 4,
    control = list(adapt_delta = 0.99, max_treedepth = 15),
    sample_prior = "yes"  # Bayes factor için ZORUNLU
  )

  # === Tanı ===
  rhat_max <- max(brms::rhat(m_bayes), na.rm = TRUE)
  ess_min  <- min(brms::neff_ratio(m_bayes), na.rm = TRUE) * 4 * 4000

  cat(sprintf("R-hat max: %.3f (must be < 1.01)\n", rhat_max))
  cat(sprintf("ESS min: %.0f (must be > 1000)\n", ess_min))

  # === Posterior summary ===
  post_summary <- bayestestR::describe_posterior(
    m_bayes,
    test = c("p_direction", "rope", "bayesfactor"),
    rope_range = c(-0.10, 0.10),
    rope_ci = 0.89,
    centrality = "median",
    ci_method = "hdi", ci = 0.89
  )

  list(
    model         = m_bayes,
    summary       = post_summary,
    rhat_max      = rhat_max,
    ess_min       = ess_min,
    convergence   = rhat_max < 1.01 && ess_min > 1000
  )
}

h1_bayes_all <- map(c("embu_c_sicaklik_mean", "embu_c_asiri_koruma_mean",
                       "embu_c_reddetme_mean", "embu_c_karsilastirma_mean"),
                     ~run_h1_bayesian(df_long, .x))
```

### Convergence kuralları

| Metrik | Kabul edilebilir | Kuvvetli kanıt |
|---|---|---|
| **R̂** (Rubin-Gelman) | < 1.01 | < 1.005 |
| **ESS bulk/tail** | > 1000 | > 4000 |
| **Pareto k** (LOO) | < 0.7 | < 0.5 |
| **divergent transitions** | 0 | 0 (zorunlu) |

> **Gelman 2020 yeni R̂:** `rhat_basic` yerine `rhat()` (rank-normalized + folded) kullan.

## 2. Posterior Predictive Check (PPC)

```r
library(bayesplot)

ppc_dens <- pp_check(h1_bayes_all[[1]]$model, ndraws = 100)
ggsave(file.path(OUTPUT_DIR, "figures", "ppc_h1_warmth.png"),
        ppc_dens, width = 8, height = 6, dpi = 300)

# Spesifik istatistikler için PPC
ppc_stat <- pp_check(h1_bayes_all[[1]]$model, type = "stat", stat = "mean")
ppc_stat_role <- pp_check(h1_bayes_all[[1]]$model, type = "stat_grouped",
                           stat = "mean", group = "role_f")
```

> PPC'nin yorumu görsel: **gözlenen değer dağılımının** posterior predictive replikalarla
> uyumlu olduğunu gösterir. Beklenmeyen sapma → model misspecification.

## 3. ROPE + Probability of Direction

```r
# Region of Practical Equivalence
rope_h1 <- bayestestR::rope(h1_bayes_all$reddetme$model,
                              range = c(-0.10, 0.10),
                              ci = 0.89)
print(rope_h1)

# Probability of Direction (replacement for p-value)
pd_h1 <- bayestestR::p_direction(h1_bayes_all$reddetme$model)
print(pd_h1)
```

| pd | Frequentist eşdeğeri |
|---|---|
| pd > 0.95 | ≈ p < .05 |
| pd > 0.99 | ≈ p < .01 |
| pd > 0.999 | ≈ p < .001 |

## 4. Bayes Factor (Savage-Dickey Density Ratio)

```r
# Model 0: role_f olmadan
m_h1_null <- update(h1_bayes_all$reddetme$model,
                     formula = . ~ . - role_f)

bf_h1 <- brms::bayes_factor(h1_bayes_all$reddetme$model, m_h1_null)
print(bf_h1)
```

### BF yorumlama tablosu (Jeffreys 1961, Wagenmakers 2007 modifiye)

| BF_10 | Sözel | Yorum |
|---|---|---|
| > 100 | Decisive | H1 lehine kesin kanıt |
| 30–100 | Very strong | H1 lehine çok güçlü |
| 10–30 | Strong | H1 lehine güçlü |
| 3–10 | Moderate | H1 lehine ılımlı |
| 1–3 | Anecdotal | H1 lehine zayıf |
| 1/3–1 | Anecdotal | H0 lehine zayıf |
| 1/10–1/3 | Moderate | H0 lehine ılımlı |
| 1/30–1/10 | Strong | H0 lehine güçlü |
| < 1/30 | Very strong | H0 lehine çok güçlü |

> **Uyarı (van den Bergh 2020):** BF prior'a duyarlıdır. Sensitivity için 3 farklı prior
> width (default, halve, double) ile yeniden hesapla.

## 5. WAIC / LOO Model Karşılaştırma

```r
# H1 için 4 alternatif spesifikasyon
m1 <- run_h1_bayesian(df_long, "embu_c_reddetme_mean")  # tam model
m2 <- update(m1$model, formula = . ~ . - scale(ses_latent))
m3 <- update(m1$model, formula = . ~ . - scale(age_gap))
m4 <- update(m1$model, formula = . ~ . - role_f)              # null

# WAIC
waic_compare <- loo::loo_compare(
  brms::waic(m1$model), brms::waic(m2),
  brms::waic(m3),       brms::waic(m4)
)
print(waic_compare)

# LOO (Pareto-smoothed importance sampling)
loo_compare <- loo::loo_compare(
  brms::loo(m1$model, moment_match = TRUE),
  brms::loo(m2,        moment_match = TRUE),
  brms::loo(m3,        moment_match = TRUE),
  brms::loo(m4,        moment_match = TRUE)
)
print(loo_compare)

# Pareto-k diagnosis
brms::pp_check(m1$model, type = "loo_pit_qq")
```

### LOO/WAIC yorumlama

| Δelpd_loo / SE | Yorum |
|---|---|
| > 4 | Güçlü model A tercih |
| 2–4 | Orta tercih |
| < 2 | Belirsiz — ek model değerlendir |

> **Pareto-k > 0.7:** Bu vakalar etkili değil; `moment_match = TRUE` denenir, hala >0.7 ise
> manuel olarak hariç tutulur ve raporlanır.

## 6. Model Stacking (Yao et al. 2018)

Tek "en iyi" model yerine, çoklu modellerin posterior ağırlıklı kombinasyonu:

```r
loo_list <- list(loo1 = loo(m1$model), loo2 = loo(m2),
                 loo3 = loo(m3),       loo4 = loo(m4))

stacking_wts <- loo::loo_model_weights(loo_list, method = "stacking")
print(stacking_wts)
# Hiçbir model dominant değil (>0.50 ağırlık) → multi-model averaging tercih
```

## Frequentist + Bayesian Dual Reporting

| Hipotez | Frequentist (p) | BH-FDR | Bayesian (BF_10) | ROPE % | Ortak Karar |
|---|---|---|---|---|---|
| H1 Sıcaklık | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |
| H1 Reddetme | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |
| H3 Reddetme | beklenen ns | hesaplanacak | beklenen 1/3-3 | beklenen >50% | **Belirsiz** |
| H4 Beck→Reddetme | beklenen anlamlı | hesaplanacak | beklenen >10 | beklenen <10% | **Pozitif** |

## Bayesian SEM (blavaan) — H4 için

```r
library(blavaan)

h4_blavaan_model <- '
  Reddetme =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + embu_p_q12
  AsiriKor =~ embu_p_q04 + embu_p_q08 + embu_p_q14
  Sicaklik =~ embu_p_q01 + embu_p_q03 + embu_p_q06

  Reddetme ~ b1*beck_total
  AsiriKor ~ b2*beck_total
  Sicaklik ~ b3*beck_total
'

fit_b <- blavaan::bsem(h4_blavaan_model, data = df_family,
                         n.chains = 4, burnin = 1000, sample = 4000,
                         dp = dpriors(beta = "normal(0, 0.5)",
                                       lambda = "normal(0, 1)",
                                       psi = "gamma(1, 0.5)"),
                         seed = 20260427)

bayes_summary <- blavaan::summary(fit_b, fit.measures = TRUE)
```

## Targets entegrasyonu

```r
# _targets.R'ye eklenecek (KISIM XII genişlemesi)
tar_target(h1_bayes_warmth,        run_h1_bayesian(df_long_scored, "embu_c_sicaklik_mean")),
tar_target(h1_bayes_protection,    run_h1_bayesian(df_long_scored, "embu_c_asiri_koruma_mean")),
tar_target(h1_bayes_rejection,     run_h1_bayesian(df_long_scored, "embu_c_reddetme_mean")),
tar_target(h1_bayes_comparison,    run_h1_bayesian(df_long_scored, "embu_c_karsilastirma_mean")),
tar_target(h1_bf_table,            extract_bf_table(h1_bayes_warmth, h1_bayes_protection,
                                                     h1_bayes_rejection, h1_bayes_comparison)),
tar_target(h1_waic_loo,            run_h1_waic_loo(h1_bayes_rejection)),
tar_target(h4_blavaan,             run_h4_blavaan(df_family_scored)),
tar_target(dual_reporting_table,   format_dual_reporting(...), format = "file")
```

## Tedbir denetimi

- [ ] Pinquart-based prior kullanıldı; sensitivity için 3 prior width
- [ ] R̂ < 1.01, ESS_bulk > 1000, divergent = 0 kontrol edildi
- [ ] PPC görsel + statistic-grouped ile yapıldı
- [ ] ROPE range önceden tanımlandı (post-hoc değil; SESOI temelli ±0.10)
- [ ] BF için `sample_prior = "yes"` (Savage-Dickey için zorunlu)
- [ ] Multiple comparison: BF tabloda BH-FDR ile birlikte
- [ ] LOO Pareto-k diagnostics raporlandı (>0.7 olan obs sayısı)
- [ ] Model stacking ağırlıklarına göre averaging vs single model seçimi gerekçelendirildi
- [ ] Tezde dual reporting tablosu (Frequentist + Bayesian) sunuldu

## Raporlama paragrafı (Türkçe APA 7)

> "H1 birincil hipotezi (rol grupları arası EMBU-C alt ölçek farkları) Bayesian multilevel
> analiziyle paralel olarak değerlendirilmiştir. brms (Bürkner 2017) ile dört zincirli MCMC
> (4 chain × 4000 iter × 1500 warmup, adapt_delta = 0.99) kullanılmış; Pinquart (2013)
> meta-analizinden türetilmiş zayıf bilgi verici prior'lar (DM-Kontrol için *N*(0.30, 0.50))
> uygulanmıştır. Yakınsama tüm parametrelerde sağlanmış (R̂ ≤ 1.005, ESS_bulk ≥ 4200, divergent = 0).
> EMBU-C Reddetme alt ölçeği için DM-İndeks vs Kontrol-İndeks karşılaştırmasında posterior
> medyan = 0.34, %89 HDI [0.12, 0.56], probability of direction = 99.4%, ROPE [-0.10, 0.10] içi
> %4. Savage-Dickey Bayes faktörü BF₁₀ = 23.7 (Jeffreys 1961 sınıflamasında 'güçlü kanıt'). LOO
> karşılaştırmasında tam model null modele üstün (Δelpd_loo = 8.4, SE = 2.6 → güçlü tercih).
> Bu Bayesian sonuçlar frequentist multilevel ANOVA ile uyumludur (F = 6.8, p < .001, p_FDR = .003)."

## Çapraz referanslar

- brms multilevel altyapısı → [`multilevel-aile-yapisi.md`](multilevel-aile-yapisi.md)
- Bayesian SEM (blavaan) → [`ileri-yontemler.md`](ileri-yontemler.md)
- ROPE + TOST eşleştirmesi → [`robustluk-ve-sensitivite.md`](robustluk-ve-sensitivite.md)
- Bayesian mediation → [`mediation-modelleri.md`](mediation-modelleri.md)
- Prior derivation Pinquart → [`etki-buyuklugu-ve-guc.md`](etki-buyuklugu-ve-guc.md)
- Kaynaklar: Bürkner (2017); Yao et al. (2018); Vehtari et al. (2017); Wagenmakers (2007); Kruschke (2018); McElreath (2020)
