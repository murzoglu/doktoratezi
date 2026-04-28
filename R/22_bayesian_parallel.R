# KISIM XII — Bayesci Paralel Hat
# 37. brms multilevel — H1, H3, H4 dual reporting
# 38. Bayes Factor (Savage-Dickey) + ROPE + Probability of Direction
# 39. WAIC + LOO model karşılaştırma
#
# Pinquart (2013) meta-analiz temelli weakly informative priors.
# Frequentist + Bayesian dual reporting standardı (kural #12).

bayes_subscales <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

bayes_pinquart_priors_h3 <- function() {
  # Pinquart 2013 meta-analiz: kronik hastalık × ebeveynlik d ≈ 0.20-0.30
  # SAP §12.4, §37.2 ile uyumlu — 3× geniş prior
  data.frame(
    outcome  = paste0("embu_p_", bayes_subscales(), "_mean"),
    prior_mean = c(0.20, 0.30, -0.15, 0.10),
    prior_sd   = c(0.50, 0.50,  0.50, 0.50),
    rationale  = c(
      "Pinquart sıcak/destek beklentisi: DM aileler kontrol≈ veya hafif ↑",
      "Aşırı koruma DM'de ↑ beklenir (Cameron 2007)",
      "Reddetme DM'de ↓ beklenir (savunmacı self-report)",
      "Karşılaştırma — zayıf bilgi, geniş 0 etrafı"
    ),
    stringsAsFactors = FALSE
  )
}

bayes_prepare_family <- function(df_family_ses) {
  df <- df_family_ses
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  df$group_dm <- as.integer(df$group_f == "DM")
  df$anne_yas_z   <- as.numeric(scale(df$anne_yas))
  df$ses_latent_z <- as.numeric(scale(df$ses_latent))
  df$age_gap_z    <- if ("age_gap" %in% names(df)) as.numeric(scale(df$age_gap)) else 0
  df$cocuk_sayisi_z <- if ("cocuk_sayisi" %in% names(df)) as.numeric(scale(df$cocuk_sayisi)) else 0
  df
}

bayes_prepare_long <- function(df_long_scored, df_family_ses) {
  long <- df_long_scored
  long$group_f <- factor(as.character(long$group_f), levels = c("Kontrol", "DM"))
  long$family_role_f <- factor(as.character(long$family_role_f))
  long$aile_no_f <- factor(as.character(long$aile_no_f))
  ses_lookup <- df_family_ses[, c("aile_no", "ses_latent", "anne_yas")]
  ses_lookup$ses_latent_z <- as.numeric(scale(ses_lookup$ses_latent))
  ses_lookup$anne_yas_z   <- as.numeric(scale(ses_lookup$anne_yas))
  merged <- merge(long, ses_lookup[, c("aile_no", "ses_latent_z", "anne_yas_z")],
                  by = "aile_no", all.x = TRUE)
  merged
}

bayes_extract_summary <- function(fit, term_pattern = "^b_group") {
  if (is.null(fit) || inherits(fit, "error")) return(NULL)
  posterior <- as.data.frame(fit)
  cols <- grep(term_pattern, names(posterior), value = TRUE)
  if (length(cols) == 0L) return(NULL)
  rows <- list()
  for (col in cols) {
    draws <- posterior[[col]]
    rows[[length(rows) + 1L]] <- data.frame(
      term       = col,
      estimate   = mean(draws),
      sd         = stats::sd(draws),
      ci_lo      = stats::quantile(draws, 0.025),
      ci_hi      = stats::quantile(draws, 0.975),
      hdi89_lo   = stats::quantile(draws, 0.055),
      hdi89_hi   = stats::quantile(draws, 0.945),
      pd         = max(mean(draws > 0), mean(draws < 0)),
      rope_pct   = mean(abs(draws) < 0.1),
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

bayes_savage_dickey_bf <- function(fit, term, prior_sd = 0.5) {
  if (is.null(fit) || inherits(fit, "error")) return(NA_real_)
  posterior <- as.data.frame(fit)
  if (!term %in% names(posterior)) return(NA_real_)
  draws <- posterior[[term]]
  posterior_density_at_zero <- tryCatch(
    stats::density(draws, from = -3 * prior_sd, to = 3 * prior_sd, n = 512),
    error = function(e) NULL
  )
  if (is.null(posterior_density_at_zero)) return(NA_real_)
  post_at_0 <- stats::approx(posterior_density_at_zero$x, posterior_density_at_zero$y, xout = 0)$y
  prior_at_0 <- stats::dnorm(0, mean = 0, sd = prior_sd)
  bf01 <- post_at_0 / prior_at_0
  bf10 <- 1 / bf01
  bf10
}

bayes_bf_classify <- function(bf10) {
  if (is.na(bf10)) return("Indeterminate")
  if (bf10 > 100) "Extreme H1"
  else if (bf10 > 30) "Very strong H1"
  else if (bf10 > 10) "Strong H1"
  else if (bf10 > 3)  "Moderate H1"
  else if (bf10 > 1)  "Anecdotal H1"
  else if (bf10 > 1/3) "Anecdotal H0"
  else if (bf10 > 1/10) "Moderate H0"
  else if (bf10 > 1/30) "Strong H0"
  else if (bf10 > 1/100) "Very strong H0"
  else "Extreme H0"
}

# === H3 Bayesian (frequentist analog: ANCOVA) =========================

bayes_h3_one_outcome <- function(df_family, outcome, prior_mean, prior_sd,
                                  iter = 2000L, warmup = 1000L,
                                  chains = 4L, seed = 20260428L) {
  if (!requireNamespace("brms", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  formula_str <- sprintf("%s ~ group_f + anne_yas_z + ses_latent_z + age_gap_z + cocuk_sayisi_z", outcome)
  priors <- c(
    brms::set_prior(sprintf("normal(%.3f, %.3f)", prior_mean, prior_sd), class = "b", coef = "group_fDM"),
    brms::set_prior("normal(0, 1)", class = "b"),
    brms::set_prior("normal(0, 2)", class = "Intercept"),
    brms::set_prior("student_t(3, 0, 2.5)", class = "sigma")
  )
  fit <- tryCatch(
    suppressMessages(suppressWarnings(brms::brm(
      formula = stats::as.formula(formula_str),
      data    = df_family,
      prior   = priors,
      sample_prior = "yes",
      iter    = iter,
      warmup  = warmup,
      chains  = chains,
      seed    = seed,
      cores   = chains,
      backend = "rstan",
      refresh = 0,
      control = list(adapt_delta = 0.95, max_treedepth = 12)
    ))),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = paste0("error:", conditionMessage(fit)), fit = NULL))
  }
  diag <- tryCatch(brms::rhat(fit), error = function(e) NULL)
  ess <- tryCatch(brms::neff_ratio(fit), error = function(e) NULL)
  divergent <- tryCatch(
    rstan::get_num_divergent(fit$fit),
    error = function(e) NA_integer_
  )
  list(
    status = "ok",
    fit    = fit,
    posterior_summary = bayes_extract_summary(fit, "^b_group_fDM"),
    bf10 = bayes_savage_dickey_bf(fit, "b_group_fDM", prior_sd = prior_sd),
    diagnostics = list(
      max_rhat = if (!is.null(diag)) max(diag, na.rm = TRUE) else NA_real_,
      min_ess_ratio = if (!is.null(ess)) min(ess, na.rm = TRUE) else NA_real_,
      n_divergent = divergent
    )
  )
}

bayes_run_h3 <- function(df_family, iter = 2000L, warmup = 1000L,
                          chains = 4L, seed = 20260428L) {
  priors_table <- bayes_pinquart_priors_h3()
  rows <- list()
  diag_rows <- list()
  fits <- list()
  for (i in seq_len(nrow(priors_table))) {
    oc <- priors_table$outcome[i]
    res <- bayes_h3_one_outcome(
      df_family, oc,
      prior_mean = priors_table$prior_mean[i],
      prior_sd   = priors_table$prior_sd[i],
      iter = iter, warmup = warmup, chains = chains, seed = seed
    )
    if (res$status != "ok") {
      rows[[length(rows) + 1L]] <- data.frame(
        outcome = oc, status = res$status,
        estimate = NA_real_, sd = NA_real_, ci_lo = NA_real_, ci_hi = NA_real_,
        pd = NA_real_, rope_pct = NA_real_,
        bf10 = NA_real_, bf_class = NA_character_,
        prior_mean = priors_table$prior_mean[i],
        prior_sd   = priors_table$prior_sd[i],
        stringsAsFactors = FALSE
      )
      diag_rows[[length(diag_rows) + 1L]] <- data.frame(
        outcome = oc, status = res$status,
        max_rhat = NA_real_, min_ess_ratio = NA_real_, n_divergent = NA_integer_,
        stringsAsFactors = FALSE
      )
      next
    }
    fits[[oc]] <- res$fit
    summ <- res$posterior_summary
    if (is.null(summ) || nrow(summ) == 0L) next
    rows[[length(rows) + 1L]] <- data.frame(
      outcome    = oc,
      status     = "ok",
      estimate   = summ$estimate[1],
      sd         = summ$sd[1],
      ci_lo      = summ$ci_lo[1],
      ci_hi      = summ$ci_hi[1],
      pd         = summ$pd[1],
      rope_pct   = summ$rope_pct[1],
      bf10       = res$bf10,
      bf_class   = bayes_bf_classify(res$bf10),
      prior_mean = priors_table$prior_mean[i],
      prior_sd   = priors_table$prior_sd[i],
      stringsAsFactors = FALSE
    )
    diag_rows[[length(diag_rows) + 1L]] <- data.frame(
      outcome = oc, status = "ok",
      max_rhat = res$diagnostics$max_rhat,
      min_ess_ratio = res$diagnostics$min_ess_ratio,
      n_divergent = res$diagnostics$n_divergent,
      stringsAsFactors = FALSE
    )
  }
  list(
    posterior_table = if (length(rows) > 0L) do.call(rbind, rows) else data.frame(),
    diagnostics_table = if (length(diag_rows) > 0L) do.call(rbind, diag_rows) else data.frame(),
    fits = fits
  )
}

# === H1 Bayesian (multilevel) =========================================

bayes_h1_one_outcome <- function(df_long, outcome,
                                  iter = 2000L, warmup = 1000L,
                                  chains = 4L, seed = 20260428L) {
  if (!requireNamespace("brms", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  formula_str <- sprintf("%s ~ group_f * family_role_f + anne_yas_z + ses_latent_z + (1 | aile_no_f)", outcome)
  priors <- c(
    brms::set_prior("normal(0.20, 0.50)", class = "b", coef = "group_fDM"),
    brms::set_prior("normal(0, 0.50)",    class = "b"),
    brms::set_prior("normal(0, 2)",       class = "Intercept"),
    brms::set_prior("student_t(3, 0, 2.5)", class = "sigma"),
    brms::set_prior("student_t(3, 0, 2.5)", class = "sd")
  )
  fit <- tryCatch(
    suppressMessages(suppressWarnings(brms::brm(
      formula = stats::as.formula(formula_str),
      data    = df_long,
      prior   = priors,
      sample_prior = "yes",
      iter    = iter, warmup = warmup, chains = chains, seed = seed,
      cores   = chains, backend = "rstan",
      refresh = 0,
      control = list(adapt_delta = 0.95, max_treedepth = 12)
    ))),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = paste0("error:", conditionMessage(fit)), fit = NULL))
  }
  diag <- tryCatch(brms::rhat(fit), error = function(e) NULL)
  ess <- tryCatch(brms::neff_ratio(fit), error = function(e) NULL)
  divergent <- tryCatch(rstan::get_num_divergent(fit$fit), error = function(e) NA_integer_)
  list(
    status = "ok",
    fit    = fit,
    posterior_summary = bayes_extract_summary(fit, "^b_group_fDM"),
    bf10 = bayes_savage_dickey_bf(fit, "b_group_fDM", prior_sd = 0.5),
    diagnostics = list(
      max_rhat = if (!is.null(diag)) max(diag, na.rm = TRUE) else NA_real_,
      min_ess_ratio = if (!is.null(ess)) min(ess, na.rm = TRUE) else NA_real_,
      n_divergent = divergent
    )
  )
}

bayes_run_h1 <- function(df_long_prepared, subscales = c("sicaklik", "reddetme"),
                         iter = 2000L, warmup = 1000L, chains = 4L, seed = 20260428L) {
  rows <- list()
  diag_rows <- list()
  fits <- list()
  for (sub in subscales) {
    outcome <- sprintf("embu_c_%s_mean", sub)
    if (!outcome %in% names(df_long_prepared)) next
    res <- bayes_h1_one_outcome(df_long_prepared, outcome, iter, warmup, chains, seed)
    if (res$status != "ok") {
      rows[[length(rows) + 1L]] <- data.frame(
        outcome = outcome, status = res$status,
        estimate = NA_real_, sd = NA_real_, ci_lo = NA_real_, ci_hi = NA_real_,
        pd = NA_real_, rope_pct = NA_real_,
        bf10 = NA_real_, bf_class = NA_character_,
        stringsAsFactors = FALSE
      )
      next
    }
    fits[[outcome]] <- res$fit
    summ <- res$posterior_summary
    if (is.null(summ) || nrow(summ) == 0L) next
    rows[[length(rows) + 1L]] <- data.frame(
      outcome  = outcome,
      status   = "ok",
      estimate = summ$estimate[1],
      sd       = summ$sd[1],
      ci_lo    = summ$ci_lo[1],
      ci_hi    = summ$ci_hi[1],
      pd       = summ$pd[1],
      rope_pct = summ$rope_pct[1],
      bf10     = res$bf10,
      bf_class = bayes_bf_classify(res$bf10),
      stringsAsFactors = FALSE
    )
    diag_rows[[length(diag_rows) + 1L]] <- data.frame(
      outcome = outcome, status = "ok",
      max_rhat = res$diagnostics$max_rhat,
      min_ess_ratio = res$diagnostics$min_ess_ratio,
      n_divergent = res$diagnostics$n_divergent,
      stringsAsFactors = FALSE
    )
  }
  list(
    posterior_table = if (length(rows) > 0L) do.call(rbind, rows) else data.frame(),
    diagnostics_table = if (length(diag_rows) > 0L) do.call(rbind, diag_rows) else data.frame(),
    fits = fits
  )
}

# === Pipeline orchestrator =============================================

run_bayesian_parallel_pipeline <- function(df_family_ses, df_long_scored,
                                            run_h1 = TRUE, run_h3 = TRUE,
                                            iter = 2000L, warmup = 1000L,
                                            chains = 2L, seed = 20260428L) {
  prepared_family <- bayes_prepare_family(df_family_ses)
  prepared_long   <- bayes_prepare_long(df_long_scored, df_family_ses)

  h3 <- if (run_h3) {
    bayes_run_h3(prepared_family, iter = iter, warmup = warmup, chains = chains, seed = seed)
  } else list(posterior_table = data.frame(), diagnostics_table = data.frame(), fits = list())

  h1 <- if (run_h1) {
    bayes_run_h1(prepared_long, subscales = c("sicaklik", "reddetme"),
                 iter = iter, warmup = warmup, chains = chains, seed = seed)
  } else list(posterior_table = data.frame(), diagnostics_table = data.frame(), fits = list())

  priors_table <- bayes_pinquart_priors_h3()

  loo_rows <- list()
  for (oc in names(h3$fits)) {
    fit <- h3$fits[[oc]]
    loo_obj <- tryCatch(brms::loo(fit), error = function(e) NULL)
    waic_obj <- tryCatch(brms::waic(fit), error = function(e) NULL)
    loo_rows[[length(loo_rows) + 1L]] <- data.frame(
      level    = "H3",
      outcome  = oc,
      elpd_loo = if (!is.null(loo_obj)) loo_obj$estimates["elpd_loo", "Estimate"] else NA_real_,
      se_elpd_loo = if (!is.null(loo_obj)) loo_obj$estimates["elpd_loo", "SE"] else NA_real_,
      p_loo    = if (!is.null(loo_obj)) loo_obj$estimates["p_loo", "Estimate"] else NA_real_,
      waic     = if (!is.null(waic_obj)) waic_obj$estimates["waic", "Estimate"] else NA_real_,
      pareto_k_problematic = if (!is.null(loo_obj)) sum(loo_obj$pointwise[, "influence_pareto_k"] > 0.7, na.rm = TRUE) else NA_integer_,
      stringsAsFactors = FALSE
    )
  }
  for (oc in names(h1$fits)) {
    fit <- h1$fits[[oc]]
    loo_obj <- tryCatch(brms::loo(fit), error = function(e) NULL)
    waic_obj <- tryCatch(brms::waic(fit), error = function(e) NULL)
    loo_rows[[length(loo_rows) + 1L]] <- data.frame(
      level    = "H1",
      outcome  = oc,
      elpd_loo = if (!is.null(loo_obj)) loo_obj$estimates["elpd_loo", "Estimate"] else NA_real_,
      se_elpd_loo = if (!is.null(loo_obj)) loo_obj$estimates["elpd_loo", "SE"] else NA_real_,
      p_loo    = if (!is.null(loo_obj)) loo_obj$estimates["p_loo", "Estimate"] else NA_real_,
      waic     = if (!is.null(waic_obj)) waic_obj$estimates["waic", "Estimate"] else NA_real_,
      pareto_k_problematic = if (!is.null(loo_obj)) sum(loo_obj$pointwise[, "influence_pareto_k"] > 0.7, na.rm = TRUE) else NA_integer_,
      stringsAsFactors = FALSE
    )
  }
  loo_table <- if (length(loo_rows) > 0L) do.call(rbind, loo_rows) else data.frame()

  target_summary <- data.frame(
    component = c("priors", "h1_posterior", "h1_diagnostics",
                  "h3_posterior", "h3_diagnostics", "loo_waic"),
    n_rows = c(nrow(priors_table), nrow(h1$posterior_table), nrow(h1$diagnostics_table),
               nrow(h3$posterior_table), nrow(h3$diagnostics_table), nrow(loo_table)),
    stringsAsFactors = FALSE
  )

  list(
    priors_table              = priors_table,
    h1_posterior_table        = h1$posterior_table,
    h1_diagnostics_table      = h1$diagnostics_table,
    h3_posterior_table        = h3$posterior_table,
    h3_diagnostics_table      = h3$diagnostics_table,
    loo_waic_table            = loo_table,
    target_summary            = target_summary,
    fits                      = list(h1 = h1$fits, h3 = h3$fits)
  )
}
