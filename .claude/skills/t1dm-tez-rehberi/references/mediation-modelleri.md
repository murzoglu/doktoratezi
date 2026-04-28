# KISIM VI — Mediation Modelleri

> SAP v3.0 §17–20. Kişisel mekanizmaların testi: T1DM_status → Beck → ParentingStyle → ChildPerception
> → SiblingRelations zinciri. **[KEŞİFSEL]** statüsü — KISIM V H1–H4 confirmatory hipotezler tamamlanana
> kadar yorumlama secondary.

## Mediation çerçevesi — VanderWeele 4 etki

| Etki | Tanım | Yorumlama |
|---|---|---|
| **Total Effect (TE)** | T → Y toplam (mediator-blind) | DM-Kontrol farkının ham ölçüsü |
| **Direct Effect (DE / NDE)** | T → Y, M tutuldu | DM'nin parenting'i Beck'siz etkilemesi |
| **Indirect Effect (IE / NIE)** | T → M → Y | Beck üzerinden geçen yolun büyüklüğü |
| **Proportion Mediated** | IE / TE | Ne kadarı Beck ile açıklanıyor? |

> **Kural:** Mediator (Beck) ana modelden dışlanır (KISIM IV nedensellik); mediation analizi *ek*
> bir katmandır, ana hipotezi geriye doğru re-yorumlamak için kullanılmaz.

## 1. Tek-Mediator Modeli (lavaan + bootstrap)

```r
run_simple_mediation <- function(df_family, df_long) {
  # Aile-düzeyi özet (kardeş ortalaması)
  df_long_summary <- df_long |>
    group_by(aile_no, group_f) |>
    summarise(
      embu_c_redd_avg  = mean(embu_c_reddetme_mean, na.rm = TRUE),
      srq_conflict_avg = mean(srq_ho_conflict_mean, na.rm = TRUE),
      .groups = "drop"
    )

  df_med <- df_family |>
    select(aile_no, group_f, anne_yas, ses_latent,
            beck_total, embu_p_reddetme_mean) |>
    left_join(df_long_summary, by = c("aile_no", "group_f"))

  med_model <- '
    embu_p_reddetme_mean ~ a*beck_total + scale(anne_yas) + scale(ses_latent)
    embu_c_redd_avg      ~ b*embu_p_reddetme_mean + group_f + scale(ses_latent)
    srq_conflict_avg     ~ c*embu_c_redd_avg + group_f

    # Endirek etkiler (multi-step mediation)
    indirect_beck_to_child  := a * b
    indirect_beck_to_srq    := a * b * c
    total_beck              := a * b
  '

  fit_med <- lavaan::sem(med_model, data = df_med,
                           estimator = "MLR", missing = "fiml",
                           se = "bootstrap", bootstrap = 5000)

  list(fit = fit_med,
        indirect = lavaan::parameterEstimates(fit_med, boot.ci.type = "bca.simple") |>
                     filter(grepl("indirect|total", label)),
        fit_meas = fitMeasures(fit_med, c("cfi","rmsea","srmr")))
}
```

**Kritik karar — bootstrap BCa CI:** Preacher & Hayes (2008) → indirect effect dağılımı normalden
uzak olduğu için **percentile** veya **BCa** bootstrap CI standarttır; Sobel testi modası geçmiş.

## 2. Multilevel Mediation (1-1-1)

T1DM tezinde aile-içi nesting ihlal edilemez:

```r
run_multilevel_mediation <- function(df_long, df_family) {
  # 1-1-1 mediation:
  # Beck (Level-2 aile) → EMBU-P (Level-2 aile) → EMBU-C (Level-1 çocuk)

  msem_model <- '
    level: 1
      embu_c_reddetme_mean ~ scale(cocuk_yas) + cinsiyet_f

    level: 2
      embu_p_reddetme_mean ~ a*beck_total + scale(ses_latent)
      embu_c_reddetme_mean ~ b*embu_p_reddetme_mean + group_f +
                              scale(ses_latent)

      indirect := a * b
  '

  df_long_with_family <- df_long |>
    left_join(df_family |> select(aile_no, beck_total,
                                     embu_p_reddetme_mean, ses_latent),
                by = "aile_no")

  fit_msem <- lavaan::sem(msem_model, data = df_long_with_family,
                            cluster = "aile_no",
                            estimator = "MLR")

  list(fit = fit_msem,
        indirect = parameterEstimates(fit_msem) |> filter(label == "indirect"))
}
```

> **Uyarı:** lavaan two-level SEM, Bauer, Preacher & Gil (2006) ayrımına dikkat etmeli — within-level
> (level-1) ve between-level (level-2) mediasyon ayrı yorumlanır. Tezde indirect effect **Level-2**
> üzerinden raporlanır (anne özellikleri aile değişkeni).

## 3. Conditional Process Analysis (Hayes 2018)

Moderated mediation — DM grubu mediasyon yolunu *moderate* ediyor mu?

```r
run_moderated_mediation <- function(df_family, df_long) {
  library(lavaan)

  # Hayes Model 14: a-yolu W tarafından moderated
  # X = beck_total, M = embu_p_reddetme, Y = embu_c_redd, W = group_f

  df_med <- df_family |>
    left_join(df_long |>
                group_by(aile_no) |>
                summarise(embu_c_redd = mean(embu_c_reddetme_mean, na.rm=T)),
                by = "aile_no")

  mod_med_model <- '
    # a-path: beck → embu_p, moderated by group
    embu_p_reddetme_mean ~ a1*beck_total + a2*group_f +
                            a3*group_f:beck_total + scale(ses_latent)

    # b-path: embu_p → embu_c
    embu_c_redd ~ b*embu_p_reddetme_mean + scale(ses_latent)

    # Conditional indirect effects (Hayes 2015)
    cond_indirect_kontrol := (a1 + a3*0) * b   # Kontrol (group_dm=0)
    cond_indirect_dm      := (a1 + a3*1) * b   # DM (group_dm=1)

    # Index of moderated mediation (Hayes 2015)
    imm := a3 * b
  '

  fit_mod_med <- lavaan::sem(mod_med_model, data = df_med,
                                estimator = "MLR", missing = "fiml",
                                se = "bootstrap", bootstrap = 5000)

  parameterEstimates(fit_mod_med, boot.ci.type = "bca.simple") |>
    filter(grepl("cond_indirect|imm", label))
}
```

### Hayes model numaraları (Tezde kullanılan)

| Model | Yapı | T1DM tezinde anlamı |
|---|---|---|
| **4** | Basit mediation (X → M → Y) | H4 Beck → EMBU-P → EMBU-C |
| **7** | Moderated a-path (W → a) | DM grubunun Beck → EMBU-P yolunu moderate etmesi |
| **14** | Moderated b-path (W → b) | DM grubunun EMBU-P → EMBU-C yolunu moderate etmesi |

> **IMM (Index of Moderated Mediation):** Hayes (2015) — moderated mediation'ın **doğrudan testi**.
> Sıfır 95% bootstrap CI'ında değilse anlamlı.

## 4. Bayesian Mediation + ROPE

Frequentist'in karşılayamadığı: "Indirect effect 0'a *yakın* mı?" sorusu.

```r
run_bayesian_mediation <- function(df_family, df_long) {
  library(brms); library(bayestestR)

  df_med <- df_family |>
    left_join(df_long |>
                group_by(aile_no) |>
                summarise(embu_c_redd = mean(embu_c_reddetme_mean, na.rm=T)),
                by = "aile_no")

  # Path a: beck → embu_p
  m_a <- brm(embu_p_reddetme_mean ~ beck_total + scale(ses_latent),
              data = df_med, chains = 4, iter = 4000,
              seed = 20260427, cores = 4)

  # Path b: embu_p → embu_c
  m_b <- brm(embu_c_redd ~ embu_p_reddetme_mean + beck_total + scale(ses_latent),
              data = df_med, chains = 4, iter = 4000,
              seed = 20260427, cores = 4)

  # Posterior samples
  post_a <- as_draws_df(m_a)$b_beck_total
  post_b <- as_draws_df(m_b)$b_embu_p_reddetme_mean

  # Indirect effect distribution (Yuan & MacKinnon 2009)
  indirect_post <- post_a * post_b

  # ROPE (Region of Practical Equivalence)
  # SESOI ±0.05 (Pinquart küçük etki temelli)
  rope_indirect <- bayestestR::rope(indirect_post,
                                      range = c(-0.05, 0.05),
                                      ci = 0.95)

  list(model_a = m_a, model_b = m_b,
        indirect_summary = bayestestR::describe_posterior(indirect_post),
        rope = rope_indirect)
}
```

### Bayesian indirect raporlama

```
Indirect effect (Beck → EMBU-P → EMBU-C):
  Median posterior: 0.038
  89% HDI: [0.012, 0.071]
  ROPE [-0.05, 0.05] içindeki posterior oranı: 67%
  Probability of direction: 99.4%

→ Yön net olarak pozitif (pd > .99) ama büyüklük pratik anlamsız sınırına yakın
   (ROPE içi %67). Mediation "varolduğu kesin ama klinik etkisi sınırlı" şeklinde yorumlanır.
```

## Tedbir denetimi (mediation'a özgü)

- [ ] **Mediator → outcome rölatif zaman:** Beck (anne) → EMBU-P (anne) → EMBU-C (çocuk) zaman
      sırası kesin değil; cross-sectional veride mediator doğrultusu DAG-temelli **varsayım**.
- [ ] Mediator ↔ outcome confounding: Beck'i etkileyen ama EMBU-P üzerinde de etkisi olan başka
      faktör (ör. SES, antidepresan) modelde tutulmalı (VanderWeele 2015).
- [ ] **No exposure-induced confounder:** DM, hem mediator (Beck) hem de mediator-outcome
      confounder'ları etkiliyorsa basit mediation hatalı; G-formula veya MSM gerekir.
- [ ] Bootstrap n ≥ 5000 (BCa CI istikrar için).
- [ ] Indirect effect dağılımı simetrik mi? Eğri ise BCa zorunlu.
- [ ] Multilevel'da level-1 vs level-2 indirect ayrımı yapıldı mı?
- [ ] [KEŞİFSEL] etiketi eklendi mi? (KISIM VI tezde keşifsel statüde)

## Sensitivity (KISIM XI ile entegrasyon)

```r
# sensemakr ile mediator-outcome confounder duyarlılığı
library(sensemakr)

m_outcome <- lm(embu_c_redd ~ embu_p_reddetme_mean + group_f + beck_total +
                 scale(ses_latent) + scale(anne_yas), data = df_med)

sens_med <- sensemakr(model = m_outcome,
                        treatment = "embu_p_reddetme_mean",
                        benchmark_covariates = "scale(ses_latent)",
                        kd = c(1, 2, 3))

# Mediator'a karşı b-yolu Robustness Value
print(sens_med)
```

> Mediation duyarlılığı: VanderWeele (2015) Bölüm 3.4 — *unmeasured mediator-outcome confounder*
> tahminin ne kadarını silebilir?

## Raporlama paragrafı (Türkçe APA 7)

> "Tek-mediator modelinde anne depresyon belirtilerinin (Beck total) çocuk algılanan ebeveynlik
> reddetmesi üzerindeki indirek etkisi anne öz-rapor reddetme tutumu üzerinden anlamlı bulunmuştur:
> ab = 0.042, %95 BCa GA [0.012, 0.078]; bootstrap n = 5000. Endirek etkinin toplam etkiye oranı
> (proportion mediated) yaklaşık %38'dir. Multilevel uzantıda (Bauer ve ark. 2006) Level-2
> mediasyon yapısı korunmuş, Level-1 within-family varyans için yön anlamsızdır. Bayesian paralel
> testte (brms varsayılan zayıf prior) indirect posterior median = 0.038 (89% HDI [0.012, 0.071]),
> ROPE [-0.05, 0.05] içinde kalan posterior oranı %67 olduğundan etki *istatistiksel olarak* yön
> net ama *pratik olarak* sınırlı şeklinde yorumlanır. Bu paragraf KEŞİFSEL statüsündedir; OSF
> kaydında (`pytfe`) ana hipotezler arasında değildir."

## Çapraz referanslar

- Multilevel mediation altyapısı → [`multilevel-aile-yapisi.md`](multilevel-aile-yapisi.md)
- Lavaan SEM detayı → [`ileri-yontemler.md`](ileri-yontemler.md)
- Bayesian brms ROPE/BF → [`bayesci-paralel-hat.md`](bayesci-paralel-hat.md)
- Mediator-outcome confounder duyarlılığı → [`robustluk-ve-sensitivite.md`](robustluk-ve-sensitivite.md)
- Kaynak kitaplar: Hayes (2018) Bölüm 3-7; VanderWeele (2015) Bölüm 2-4; MacKinnon (2008) Bölüm 4
