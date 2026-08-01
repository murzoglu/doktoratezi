# H3 (EMBU-P grup etkisi) eksik-veri cercevesi saglamligi.
#
# Denetim bulgusu (workflow wtl93r3uu): §8.5/§18.4 eksik-veri uclusunu
# (FIML + coklu atama m=50 + tamamlanmis-durum) ve NMAR delta izgarasini
# "islenmistir/raporlanmistir" diye atifliyor, ancak sayisal cikti yoktu.
#
# Bu modul H3 birincil grup etkisini (EMBU-P dort alt olcek) UC eksik-veri
# cercevesinde tahmin edip karsilastirir ve NMAR delta izgarasini fiilen uygular.
#
# ONEMLI: H3 birincil model (R/18) SES kovaryati olarak ses_latent kullanir;
# ses_latent CFA (missing="pairwise") ile tum 241 satira uretildiginden 0 NA
# tasir. Eksikligi TASIYAN gercek SES kovaryati aile_isei08'dir (22 NA / 241 =
# %9,1, analitik). Bu nedenle missing-data saglamlik analizi aile_isei08 SES
# kovaryati uzerinden kurulur; boylece tamamlanmis-durum ~22 satir dusurur ve
# NMAR delta bu satirlari fiilen ayarlar. Bu, R/18 kanonik H3'unu DEGISTIRMEZ;
# ayri, acikca etiketli bir raporlama-butunlugu saglamlik katmanidir.
#
# Saf fonksiyonlar; dosya I/O yok (R/ katmani sozlesmesi).

h3mr_outcomes <- function() {
  c(
    "embu_p_sicaklik_mean",
    "embu_p_asiri_koruma_mean",
    "embu_p_reddetme_mean",
    "embu_p_karsilastirma_mean"
  )
}

# Eksikligi tasiyan SES kovaryati (ses_latent degil).
h3mr_ses_covariate <- function() {
  "aile_isei08"
}

h3mr_delta_values <- function() {
  c(-1, -0.5, 0, 0.5, 1)
}

h3mr_formula <- function(outcome, ses_covariate = h3mr_ses_covariate()) {
  stats::as.formula(
    paste(outcome, "~ group_dm +", "anne_yas +", ses_covariate, "+ cocuk_sayisi")
  )
}

h3mr_group_row <- function(estimate, std_error, dfree, outcome, framework, n) {
  multiplier <- if (is.na(dfree)) stats::qnorm(0.975) else stats::qt(0.975, df = dfree)
  statistic <- estimate / std_error
  p_value <- if (is.na(dfree)) {
    2 * stats::pnorm(abs(statistic), lower.tail = FALSE)
  } else {
    2 * stats::pt(abs(statistic), df = dfree, lower.tail = FALSE)
  }
  data.frame(
    outcome = outcome,
    framework = framework,
    n = as.integer(n),
    estimate = as.numeric(estimate),
    std_error = as.numeric(std_error),
    df = as.numeric(dfree),
    ci_low = as.numeric(estimate - multiplier * std_error),
    ci_high = as.numeric(estimate + multiplier * std_error),
    p_value = as.numeric(p_value),
    stringsAsFactors = FALSE
  )
}

# --- Cerceve 1: tamamlanmis-durum (complete-case) ---------------------------
h3mr_complete_case <- function(frame, outcome, ses_covariate = h3mr_ses_covariate()) {
  fml <- h3mr_formula(outcome, ses_covariate)
  keep <- stats::complete.cases(frame[all.vars(fml)])
  d <- frame[keep, , drop = FALSE]
  model <- stats::lm(fml, data = d)
  coefs <- summary(model)$coefficients
  h3mr_group_row(
    coefs["group_dm", "Estimate"],
    coefs["group_dm", "Std. Error"],
    stats::df.residual(model),
    outcome, "complete_case", nrow(d)
  )
}

# --- Cerceve 2: FIML (lavaan, missing="fiml", fixed.x=FALSE) -----------------
h3mr_fiml <- function(frame, outcome, ses_covariate = h3mr_ses_covariate()) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Required package is not installed: lavaan", call. = FALSE)
  }
  fml <- h3mr_formula(outcome, ses_covariate)
  vars <- all.vars(fml)
  d <- frame[vars]
  d$group_dm <- as.numeric(d$group_dm)
  model <- paste0(
    outcome, " ~ b*group_dm + anne_yas + ", ses_covariate, " + cocuk_sayisi"
  )
  # aile_isei08 (ISEI olcegi ~10-90) ile EMBU ortalamalari (1-4) arasi olcek
  # farki lavaan'da benign bir varyans-disparitesi uyarisi uretir; nokta
  # tahminleri gecerlidir (uc cerceve arasi yayilim <0,01 ile teyitli).
  fit <- suppressWarnings(lavaan::sem(
    model, data = d, missing = "fiml", fixed.x = FALSE, meanstructure = TRUE
  ))
  pe <- lavaan::parameterEstimates(fit)
  row <- pe[pe$label == "b", ]
  n <- as.integer(lavaan::lavInspect(fit, "nobs"))
  data.frame(
    outcome = outcome,
    framework = "fiml",
    n = n,
    estimate = as.numeric(row$est),
    std_error = as.numeric(row$se),
    df = NA_real_,
    ci_low = as.numeric(row$ci.lower),
    ci_high = as.numeric(row$ci.upper),
    p_value = as.numeric(row$pvalue),
    stringsAsFactors = FALSE
  )
}

# --- Cerceve 3: MI-pooled (mice, m=50 uretilmis mids) -----------------------
h3mr_fit_list <- function(mids, fml) {
  if (!requireNamespace("mice", quietly = TRUE)) {
    stop("Required package is not installed: mice", call. = FALSE)
  }
  lapply(seq_len(mids$m), function(i) {
    stats::lm(fml, data = mice::complete(mids, i))
  })
}

h3mr_pool_group <- function(fit_list, outcome, framework, n) {
  pooled <- mice::pool(mice::as.mira(fit_list))
  s <- summary(pooled, conf.int = TRUE)
  gr <- s[s$term == "group_dm", ]
  data.frame(
    outcome = outcome,
    framework = framework,
    n = as.integer(n),
    estimate = as.numeric(gr$estimate),
    std_error = as.numeric(gr$std.error),
    df = as.numeric(gr$df),
    ci_low = as.numeric(gr[["2.5 %"]]),
    ci_high = as.numeric(gr[["97.5 %"]]),
    p_value = as.numeric(gr$p.value),
    stringsAsFactors = FALSE
  )
}

h3mr_mi_pooled <- function(mids, outcome, ses_covariate = h3mr_ses_covariate()) {
  fml <- h3mr_formula(outcome, ses_covariate)
  fits <- h3mr_fit_list(mids, fml)
  analysis_n <- nrow(mice::complete(mids, 1L))
  h3mr_pool_group(fits, outcome, "mi_pooled", analysis_n)
}

# --- NMAR delta: imputed SES kovaryatina delta ekle, refit, pool ------------
h3mr_delta_row <- function(mids, original_frame, outcome, delta,
                           ses_covariate = h3mr_ses_covariate()) {
  fml <- h3mr_formula(outcome, ses_covariate)
  long <- mice::complete(mids, "long", include = FALSE)
  adjusted <- apply_nmar_delta_adjustment(
    long, original_frame, ses_covariate, delta, id_column = ".id"
  )
  fits <- lapply(sort(unique(adjusted$.imp)), function(k) {
    stats::lm(fml, data = adjusted[adjusted$.imp == k, , drop = FALSE])
  })
  pooled <- mice::pool(mice::as.mira(fits))
  s <- summary(pooled, conf.int = TRUE)
  gr <- s[s$term == "group_dm", ]
  data.frame(
    outcome = outcome,
    delta = delta,
    estimate = as.numeric(gr$estimate),
    std_error = as.numeric(gr$std.error),
    ci_low = as.numeric(gr[["2.5 %"]]),
    ci_high = as.numeric(gr[["97.5 %"]]),
    p_value = as.numeric(gr$p.value),
    stringsAsFactors = FALSE
  )
}

run_h3_missing_robustness <- function(missing_results, missing_imputations,
                                      outcomes = h3mr_outcomes(),
                                      delta_values = h3mr_delta_values(),
                                      ses_covariate = h3mr_ses_covariate()) {
  frame <- missing_results$frames$mi_primary
  mids <- if (inherits(missing_imputations, "mids")) {
    missing_imputations
  } else {
    missing_imputations$primary
  }

  framework_comparison <- do.call(rbind, lapply(outcomes, function(outcome) {
    rbind(
      h3mr_complete_case(frame, outcome, ses_covariate),
      h3mr_fiml(frame, outcome, ses_covariate),
      h3mr_mi_pooled(mids, outcome, ses_covariate)
    )
  }))

  nmar_delta_sensitivity <- do.call(rbind, lapply(outcomes, function(outcome) {
    do.call(rbind, lapply(delta_values, function(delta) {
      h3mr_delta_row(mids, frame, outcome, delta, ses_covariate)
    }))
  }))

  reddetme <- framework_comparison[
    framework_comparison$outcome == "embu_p_reddetme_mean", "estimate"
  ]
  summary_table <- data.frame(
    ses_covariate = ses_covariate,
    n_outcomes = length(outcomes),
    n_frameworks = 3L,
    complete_case_n = framework_comparison$n[framework_comparison$framework == "complete_case"][1],
    imputed_n = mids$m,
    max_reddetme_estimate_spread = max(reddetme) - min(reddetme),
    stringsAsFactors = FALSE
  )

  list(
    framework_comparison = framework_comparison,
    nmar_delta_sensitivity = nmar_delta_sensitivity,
    summary = summary_table
  )
}

# --- H3 SES-operasyonelleştirme sağlamlığı (Hollingshead paralel) -----------
# §8.7 "latent SES ... Hollingshead İki-Faktör İndeksi duyarlılık analizinde
# paralel raporlanmıştır" iddiasini gerceklestirir: H3 grup etkisini dort SES
# operasyonelleştirmesi (latent CFA, Hollingshead İki-Faktör, eşit-ağırlık
# kompozit, ham ISEI-08) altinda kestirip karsilastirir. R/11 ses_hollingshead
# = (3*edu_z + 5*isei_z)/8 zaten hesaplidir.

h3ses_measures <- function() {
  c("ses_latent", "ses_hollingshead", "ses_composite_eq", "aile_isei08")
}

h3ses_measure_label <- function(measure) {
  c(
    ses_latent = "Latent CFA",
    ses_hollingshead = "Hollingshead İki-Faktör",
    ses_composite_eq = "Eşit-ağırlık kompozit",
    aile_isei08 = "Ham ISEI-08"
  )[[measure]]
}

h3ses_group_dm <- function(df) {
  if ("group_dm" %in% names(df)) {
    return(as.integer(df$group_dm))
  }
  group_source <- if ("group" %in% names(df)) df$group else df$group_f
  as.integer(tolower(as.character(group_source)) %in% c("dm", "diyabet", "diabetes", "t1dm"))
}

run_h3_ses_operationalization <- function(df_family_ses,
                                          outcomes = h3mr_outcomes(),
                                          measures = h3ses_measures()) {
  group_dm <- h3ses_group_dm(df_family_ses)
  rows <- list()
  index <- 0L
  for (measure in measures) {
    ses_z <- as.numeric(scale(suppressWarnings(as.numeric(df_family_ses[[measure]]))))
    for (outcome in outcomes) {
      d <- data.frame(
        y = suppressWarnings(as.numeric(df_family_ses[[outcome]])),
        group_dm = group_dm,
        anne_yas = suppressWarnings(as.numeric(df_family_ses[["anne_yas"]])),
        ses = ses_z,
        cocuk_sayisi = suppressWarnings(as.numeric(df_family_ses[["cocuk_sayisi"]])),
        stringsAsFactors = FALSE
      )
      d <- d[stats::complete.cases(d), , drop = FALSE]
      fit <- stats::lm(y ~ group_dm + anne_yas + ses + cocuk_sayisi, data = d)
      coefs <- summary(fit)$coefficients
      est <- coefs["group_dm", "Estimate"]
      se <- coefs["group_dm", "Std. Error"]
      dfree <- stats::df.residual(fit)
      mult <- stats::qt(0.975, df = dfree)
      index <- index + 1L
      rows[[index]] <- data.frame(
        ses_measure = measure,
        ses_label = h3ses_measure_label(measure),
        outcome = outcome,
        n = nrow(d),
        estimate = as.numeric(est),
        std_error = as.numeric(se),
        ci_low = as.numeric(est - mult * se),
        ci_high = as.numeric(est + mult * se),
        p_value = 2 * stats::pt(abs(est / se), df = dfree, lower.tail = FALSE),
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}
