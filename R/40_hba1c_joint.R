# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXIV/65, 66, 68
# Klinik Stratifikasyon Genisletmesi (DM-only altgrup)
#
# 65 — HbA1c x parenting Bayesian joint model: brms ile Anderson 2002
#      ve Pinquart 2018 metalardan turetilmis bilgi-verici prior
#      (Normal(0.16, 0.10) — anne reddetme/asiri koruma -> HbA1c kanali
#      kucuk-orta etki beklenir).
#
# 66 — Tani yasi spline x parenting (DM-only): splines::ns(tani_yasi, df=3)
#      ile cubic spline + lineer model LRT karsilastirmasi.
#
# 68 — ISPAD esigi (HbA1c < 7.0%) ikili sonuc lojistik regresyon: anne
#      EMBU-P alt olcekleri yordayicilari, DM-only altgrup.
#
# Kural #19: HbA1c yapisal MNAR olarak etiketlenmistir, IMPUTASYON YAPILMAZ.
#            Yalnizca complete-case DM-only altgrupta calisilir; n_hba1c
#            acikca raporlanir.
#
# Skill referanslari: references/dm-klinik-altanalizler.md,
#                     references/bayesci-paralel-hat.md,
#                     references/eksik-veri-yonetimi.md

hba1c_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

hba1c_anne_outcome_columns <- function() {
  paste0("embu_p_", hba1c_subscale_outcomes(), "_mean")
}

hba1c_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(sprintf("%s missing column(s): %s",
      context, paste(missing_columns, collapse = ", ")), call. = FALSE)
  }
  invisible(TRUE)
}

hba1c_scale <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

hba1c_ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f) - 1L
    } else if ("grup" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$grup), ignore.case = TRUE))
    } else {
      stop("group_dm/group_f/grup yok; df_family_ses kontrol edin", call. = FALSE)
    }
  }
  df
}

hba1c_prepare_dm_only <- function(df_family_ses,
                                  require_hba1c = TRUE) {
  needed <- c("aile_no", "anne_yas", "ses_latent",
    "hba1c", "tani_yasi", "dm_yili",
    hba1c_anne_outcome_columns())
  hba1c_require_columns(df_family_ses, needed, "HbA1c DM-only frame")

  df <- hba1c_ensure_group_dm(df_family_ses)
  dm_idx <- !is.na(df$group_dm) & df$group_dm == 1L
  dm <- df[dm_idx, , drop = FALSE]

  out <- dm[, c("aile_no", "anne_yas", "ses_latent",
    "hba1c", "tani_yasi", "dm_yili",
    hba1c_anne_outcome_columns()), drop = FALSE]

  out$anne_yas_z <- hba1c_scale(out$anne_yas)
  out$ses_latent_z <- hba1c_scale(out$ses_latent)
  out$hba1c_z <- hba1c_scale(out$hba1c)
  out$tani_yasi_z <- hba1c_scale(out$tani_yasi)
  out$dm_yili_z <- hba1c_scale(out$dm_yili)
  for (col in hba1c_anne_outcome_columns()) {
    out[[paste0(col, "_z")]] <- hba1c_scale(out[[col]])
  }
  out$hba1c_under_7 <- as.integer(out$hba1c < 7.0)

  attr(out, "hba1c_summary") <- data.frame(
    n_dm_total = nrow(out),
    n_with_hba1c = sum(!is.na(out$hba1c)),
    n_with_tani_yasi = sum(!is.na(out$tani_yasi)),
    n_with_dm_yili = sum(!is.na(out$dm_yili)),
    median_hba1c = stats::median(out$hba1c, na.rm = TRUE),
    median_tani_yasi = stats::median(out$tani_yasi, na.rm = TRUE),
    median_dm_yili = stats::median(out$dm_yili, na.rm = TRUE),
    n_under_7 = sum(out$hba1c_under_7, na.rm = TRUE),
    stringsAsFactors = FALSE
  )

  if (require_hba1c) {
    out <- out[!is.na(out$hba1c), , drop = FALSE]
  }
  out
}

# ============================================================================
# 65 — HbA1c x Parenting Bayesian Joint
# ============================================================================

hba1c_bayesian_priors <- function() {
  # Anderson 2002 (parenting conflict <-> HbA1c r ~ 0.18)
  # Pinquart 2018 (parenting stress <-> glycemic control r ~ 0.15)
  # Pooled: weakly informative Normal(0.16, 0.10) for parenting predictors
  # Wide Normal(0, 0.5) for covariates
  list(
    parenting = list(mean = 0.16, sd = 0.10),
    covariate = list(mean = 0, sd = 0.5)
  )
}

hba1c_bayesian_one <- function(dm_data, predictor_subscale,
                               chains = 2L, iter = 2000L,
                               adapt_delta = 0.95) {
  if (!requireNamespace("brms", quietly = TRUE)) {
    return(list(status = "brms_unavailable"))
  }
  pred_z <- paste0("embu_p_", predictor_subscale, "_mean_z")
  if (!pred_z %in% names(dm_data)) {
    return(list(status = "missing_predictor", missing = pred_z))
  }
  formula_obj <- stats::as.formula(sprintf(
    "hba1c_z ~ %s + dm_yili_z + tani_yasi_z + anne_yas_z + ses_latent_z",
    pred_z
  ))

  priors <- hba1c_bayesian_priors()
  prior_set <- c(
    brms::set_prior(sprintf("normal(%.2f, %.2f)", priors$parenting$mean,
      priors$parenting$sd), class = "b", coef = pred_z),
    brms::set_prior("normal(0, 0.5)", class = "b"),
    brms::set_prior("student_t(3, 0, 1)", class = "sigma")
  )
  fit <- tryCatch(
    suppressWarnings(brms::brm(
      formula = formula_obj,
      data = dm_data,
      family = gaussian(),
      prior = prior_set,
      chains = chains,
      iter = iter,
      warmup = floor(iter / 2),
      control = list(adapt_delta = adapt_delta),
      refresh = 0,
      silent = 2,
      seed = 20260509
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", outcome_subscale = predictor_subscale,
      error_message = conditionMessage(fit)))
  }

  post <- as.matrix(fit, variable = paste0("b_", pred_z))
  median_est <- stats::median(post)
  hdi_low <- stats::quantile(post, 0.025)
  hdi_high <- stats::quantile(post, 0.975)
  pd <- mean(post * sign(median_est) > 0)
  in_rope <- mean(abs(post) < 0.10)

  list(
    status = "ok",
    predictor_subscale = predictor_subscale,
    posterior_summary = data.frame(
      predictor_subscale = predictor_subscale,
      posterior_median = median_est,
      ci_lower = unname(hdi_low),
      ci_upper = unname(hdi_high),
      pd = pd,
      rope_share = in_rope,
      rope = "[-0.10, +0.10]",
      n_used = stats::nobs(fit),
      stringsAsFactors = FALSE
    ),
    rhat_max = max(brms::rhat(fit), na.rm = TRUE),
    divergent_count = sum(brms::nuts_params(fit)$Value[
      brms::nuts_params(fit)$Parameter == "divergent__"
    ], na.rm = TRUE)
  )
}

hba1c_bayesian_pipeline <- function(dm_data,
                                    outcomes = hba1c_subscale_outcomes(),
                                    chains = 2L, iter = 2000L) {
  status_rows <- list()
  posterior_rows <- list()
  for (sub in outcomes) {
    r <- hba1c_bayesian_one(dm_data, sub, chains = chains, iter = iter)
    status_rows[[sub]] <- data.frame(
      predictor_subscale = sub,
      status = r$status,
      n_used = r$posterior_summary$n_used %||% NA_integer_,
      rhat_max = r$rhat_max %||% NA_real_,
      divergent_count = r$divergent_count %||% NA_integer_,
      chains = chains,
      iter = iter,
      error_message = r$error_message %||% NA_character_,
      stringsAsFactors = FALSE
    )
    if (identical(r$status, "ok")) {
      posterior_rows[[sub]] <- r$posterior_summary
    }
  }
  list(
    status = if (length(status_rows) > 0L) do.call(rbind, status_rows) else NULL,
    posterior = if (length(posterior_rows) > 0L) do.call(rbind, posterior_rows) else NULL
  )
}

# ============================================================================
# 66 — Tani Yasi Spline x Parenting (DM-only)
# ============================================================================

hba1c_tani_yasi_spline_one <- function(dm_data, outcome_subscale,
                                       df_spline = 3L) {
  if (!requireNamespace("splines", quietly = TRUE)) {
    return(list(status = "splines_unavailable"))
  }
  outcome <- paste0("embu_p_", outcome_subscale, "_mean")
  needed <- c(outcome, "tani_yasi", "dm_yili_z", "ses_latent_z", "anne_yas_z")
  if (any(!needed %in% names(dm_data))) {
    return(list(status = "missing_columns",
      missing = setdiff(needed, names(dm_data))))
  }
  dat <- dm_data[stats::complete.cases(dm_data[, needed]), , drop = FALSE]
  if (nrow(dat) < df_spline + 5L) {
    return(list(status = "insufficient_n", n = nrow(dat)))
  }

  # Spline (cubic ns)
  spline_formula <- stats::as.formula(sprintf(
    "%s ~ splines::ns(tani_yasi, df = %d) + dm_yili_z + ses_latent_z + anne_yas_z",
    outcome, df_spline
  ))
  linear_formula <- stats::as.formula(sprintf(
    "%s ~ tani_yasi + dm_yili_z + ses_latent_z + anne_yas_z", outcome
  ))
  fit_spline <- tryCatch(stats::lm(spline_formula, data = dat),
    error = function(e) e)
  fit_linear <- tryCatch(stats::lm(linear_formula, data = dat),
    error = function(e) e)
  if (inherits(fit_spline, "error") || inherits(fit_linear, "error")) {
    return(list(status = "fit_error",
      error_message = conditionMessage(if (inherits(fit_spline, "error")) fit_spline else fit_linear)))
  }
  lrt <- stats::anova(fit_linear, fit_spline)
  list(
    status = "ok",
    outcome_subscale = outcome_subscale,
    n_used = nrow(dat),
    spline_r_squared = summary(fit_spline)$r.squared,
    linear_r_squared = summary(fit_linear)$r.squared,
    lrt_f = lrt$F[2L],
    lrt_p = lrt$`Pr(>F)`[2L],
    aic_linear = stats::AIC(fit_linear),
    aic_spline = stats::AIC(fit_spline),
    decision = if (!is.na(lrt$`Pr(>F)`[2L]) && lrt$`Pr(>F)`[2L] < 0.05) {
      "spline_preferred"
    } else {
      "linear_sufficient"
    }
  )
}

hba1c_tani_yasi_spline_pipeline <- function(dm_data,
                                            outcomes = hba1c_subscale_outcomes(),
                                            df_spline = 3L) {
  rows <- list()
  for (sub in outcomes) {
    r <- hba1c_tani_yasi_spline_one(dm_data, sub, df_spline = df_spline)
    rows[[sub]] <- data.frame(
      outcome_subscale = sub,
      status = r$status,
      n_used = r$n_used %||% NA_integer_,
      df_spline = df_spline,
      spline_r_squared = r$spline_r_squared %||% NA_real_,
      linear_r_squared = r$linear_r_squared %||% NA_real_,
      lrt_f = r$lrt_f %||% NA_real_,
      lrt_p = r$lrt_p %||% NA_real_,
      aic_linear = r$aic_linear %||% NA_real_,
      aic_spline = r$aic_spline %||% NA_real_,
      decision = r$decision %||% NA_character_,
      error_message = r$error_message %||% NA_character_,
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ============================================================================
# 68 — ISPAD <%7 Logistic
# ============================================================================

hba1c_ispad_logistic_one <- function(dm_data, predictor_subscale) {
  pred <- paste0("embu_p_", predictor_subscale, "_mean_z")
  needed <- c("hba1c_under_7", pred, "dm_yili_z", "ses_latent_z", "anne_yas_z")
  if (any(!needed %in% names(dm_data))) {
    return(list(status = "missing_columns"))
  }
  dat <- dm_data[stats::complete.cases(dm_data[, needed]), , drop = FALSE]
  if (nrow(dat) < 15L || sum(dat$hba1c_under_7) < 3L) {
    return(list(status = "insufficient_outcome_events",
      n = nrow(dat),
      n_events = sum(dat$hba1c_under_7)))
  }

  formula_obj <- stats::as.formula(sprintf(
    "hba1c_under_7 ~ %s + dm_yili_z + ses_latent_z + anne_yas_z", pred
  ))
  fit <- tryCatch(
    stats::glm(formula_obj, data = dat, family = binomial()),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", error_message = conditionMessage(fit)))
  }
  sm <- summary(fit)
  coef_df <- as.data.frame(sm$coefficients)
  coef_df$term <- rownames(coef_df)
  rownames(coef_df) <- NULL
  names(coef_df) <- gsub("[ ,()<>]+", "_", names(coef_df))
  pred_row <- coef_df[coef_df$term == pred, , drop = FALSE]
  if (nrow(pred_row) == 0L) {
    return(list(status = "predictor_not_in_model"))
  }
  estimate <- pred_row[["Estimate"]]
  se <- pred_row[["Std._Error"]]
  list(
    status = "ok",
    predictor_subscale = predictor_subscale,
    n_used = stats::nobs(fit),
    n_events = sum(dat$hba1c_under_7),
    log_odds = estimate,
    odds_ratio = exp(estimate),
    or_lower = exp(estimate - 1.96 * se),
    or_upper = exp(estimate + 1.96 * se),
    p_value = pred_row[["Pr_|z|_"]],
    aic = stats::AIC(fit)
  )
}

hba1c_ispad_logistic_pipeline <- function(dm_data,
                                          outcomes = hba1c_subscale_outcomes()) {
  rows <- list()
  for (sub in outcomes) {
    r <- hba1c_ispad_logistic_one(dm_data, sub)
    rows[[sub]] <- data.frame(
      predictor_subscale = sub,
      status = r$status,
      n_used = r$n_used %||% NA_integer_,
      n_events = r$n_events %||% NA_integer_,
      log_odds = r$log_odds %||% NA_real_,
      odds_ratio = r$odds_ratio %||% NA_real_,
      or_lower = r$or_lower %||% NA_real_,
      or_upper = r$or_upper %||% NA_real_,
      p_value = r$p_value %||% NA_real_,
      aic = r$aic %||% NA_real_,
      error_message = r$error_message %||% NA_character_,
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ============================================================================
# Pipeline
# ============================================================================

run_hba1c_joint_pipeline <- function(df_family_ses,
                                     bootstrap_n = NULL,
                                     brms_chains = 2L,
                                     brms_iter = 2000L,
                                     run_bayesian = TRUE,
                                     df_spline = 3L) {
  dm_data <- hba1c_prepare_dm_only(df_family_ses, require_hba1c = TRUE)
  dm_summary <- attr(dm_data, "hba1c_summary")

  bayesian <- if (run_bayesian) {
    hba1c_bayesian_pipeline(dm_data, chains = brms_chains, iter = brms_iter)
  } else {
    list(status = NULL, posterior = NULL)
  }
  spline_table <- hba1c_tani_yasi_spline_pipeline(dm_data, df_spline = df_spline)
  ispad_table <- hba1c_ispad_logistic_pipeline(dm_data)

  list(
    dm_summary = dm_summary,
    bayesian_status = bayesian$status,
    bayesian_posterior = bayesian$posterior,
    spline_table = spline_table,
    ispad_table = ispad_table,
    target_summary = data.frame(
      analysis = "hba1c_joint_phase2",
      n_hba1c = dm_summary$n_with_hba1c,
      brms_chains = brms_chains,
      brms_iter = brms_iter,
      df_spline = df_spline,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXIV/65, 66, 68)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      kural_19 = "HbA1c imputasyon yok; complete-case DM-only",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
