# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXVI/73, 74, 75
# Distribusyonel ve Kuantil Yaklasimlar
#
# 73 — Quantile regression (Koenker & Bassett 1978): tau = 0.50, 0.75, 0.90.
#      Ust kuyrukta DM x Kontrol farkinin nasil farkliliklastigini gosterir.
#
# 74 — Distributional regression: brms ile mean + sigma icin ayri yapisal
#      yollar; DM grubunda varyans heterojenligi sorgulanir.
#
# 75 — Beta regression: EMBU mean skorlari [1, 4] aralikta -> [0, 1]'e
#      olceklendirme + beta family. betareg yoksa gamlss::BE family fallback.
#
# Skill referanslari: references/etki-buyuklugu-ve-guc.md,
#                     references/raporlama-sablonlari.md
# Veri: df_long_scored (multilevel cocuk algi, EMBU-C alt olcek mean)

dist_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

dist_cocuk_outcome <- function(s) paste0("embu_c_", s, "_mean")

dist_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

dist_scale <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

dist_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(sprintf("%s missing column(s): %s",
      context, paste(missing_columns, collapse = ", ")), call. = FALSE)
  }
  invisible(TRUE)
}

dist_ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f) - 1L
    } else if ("grup" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$grup), ignore.case = TRUE))
    }
  }
  df
}

dist_prepare_long <- function(df_long_scored, df_family_ses,
                              outcomes = dist_subscale_outcomes()) {
  required_long <- c("aile_no", "family_role_f", "cocuk_yas", "cinsiyet_f",
    paste0("embu_c_", outcomes, "_mean"))
  dist_require_columns(df_long_scored, required_long, "distributional long data")
  required_family <- c("aile_no", "ses_latent", "anne_yas")
  dist_require_columns(df_family_ses, required_family, "distributional family data")

  long <- df_long_scored[, required_long, drop = FALSE]
  long$role_token <- dist_normalize_role(long$family_role_f)
  long <- long[!is.na(long$role_token), , drop = FALSE]

  fam <- dist_ensure_group_dm(df_family_ses)
  fam <- fam[, c("aile_no", "group_dm", "ses_latent", "anne_yas"), drop = FALSE]

  paired <- merge(long, fam, by = "aile_no", all.x = TRUE)
  paired$cocuk_yas_z <- dist_scale(paired$cocuk_yas)
  paired$ses_latent_z <- dist_scale(paired$ses_latent)
  paired$anne_yas_z <- dist_scale(paired$anne_yas)
  paired
}

# ============================================================================
# 73 — Quantile Regression
# ============================================================================

dist_quantile_regression_one <- function(long_data, outcome_subscale,
                                          taus = c(0.50, 0.75, 0.90),
                                          bootstrap_R = 5000L) {
  if (!requireNamespace("quantreg", quietly = TRUE)) {
    return(list(status = "quantreg_unavailable"))
  }
  outcome <- dist_cocuk_outcome(outcome_subscale)
  needed <- c(outcome, "group_dm", "cocuk_yas_z", "cinsiyet_f", "ses_latent_z")
  if (any(!needed %in% names(long_data))) {
    return(list(status = "missing_columns",
      missing = setdiff(needed, names(long_data))))
  }
  dat <- long_data[stats::complete.cases(long_data[, needed]), , drop = FALSE]
  if (nrow(dat) < 50L) {
    return(list(status = "insufficient_n", n = nrow(dat)))
  }
  formula_obj <- stats::as.formula(sprintf(
    "%s ~ group_dm + cocuk_yas_z + cinsiyet_f + ses_latent_z", outcome
  ))

  rows <- list()
  for (tau in taus) {
    fit <- tryCatch(
      quantreg::rq(formula_obj, tau = tau, data = dat),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      rows[[paste0("tau_", tau)]] <- data.frame(
        outcome_subscale = outcome_subscale,
        tau = tau,
        status = "fit_error",
        estimate = NA_real_, se = NA_real_,
        ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
        n_used = nrow(dat),
        error_message = conditionMessage(fit),
        stringsAsFactors = FALSE
      )
      next
    }
    sm <- tryCatch(
      summary(fit, se = "boot", R = bootstrap_R),
      error = function(e) NULL
    )
    if (is.null(sm)) {
      rows[[paste0("tau_", tau)]] <- data.frame(
        outcome_subscale = outcome_subscale,
        tau = tau,
        status = "se_bootstrap_failed",
        estimate = unname(stats::coef(fit)["group_dm"]),
        se = NA_real_,
        ci_lower = NA_real_,
        ci_upper = NA_real_,
        p_value = NA_real_,
        n_used = nrow(dat),
        error_message = NA_character_,
        stringsAsFactors = FALSE
      )
      next
    }
    cs <- sm$coefficients
    grp_idx <- which(rownames(cs) == "group_dm")
    if (length(grp_idx) == 0L) {
      rows[[paste0("tau_", tau)]] <- data.frame(
        outcome_subscale = outcome_subscale,
        tau = tau,
        status = "predictor_not_in_model",
        estimate = NA_real_, se = NA_real_,
        ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
        n_used = nrow(dat),
        error_message = NA_character_,
        stringsAsFactors = FALSE
      )
      next
    }
    est <- cs[grp_idx, 1L]
    se <- cs[grp_idx, 2L]
    rows[[paste0("tau_", tau)]] <- data.frame(
      outcome_subscale = outcome_subscale,
      tau = tau,
      status = "ok",
      estimate = est,
      se = se,
      ci_lower = est - 1.96 * se,
      ci_upper = est + 1.96 * se,
      p_value = 2 * (1 - stats::pnorm(abs(est / se))),
      n_used = nrow(dat),
      error_message = NA_character_,
      stringsAsFactors = FALSE
    )
  }
  list(
    status = "ok",
    outcome_subscale = outcome_subscale,
    quantile_table = do.call(rbind, rows)
  )
}

dist_quantile_regression_pipeline <- function(long_data,
                                               outcomes = dist_subscale_outcomes(),
                                               taus = c(0.50, 0.75, 0.90),
                                               bootstrap_R = 5000L) {
  rows <- list()
  for (sub in outcomes) {
    r <- dist_quantile_regression_one(long_data, sub, taus = taus,
      bootstrap_R = bootstrap_R)
    if (identical(r$status, "ok")) {
      rows[[sub]] <- r$quantile_table
    } else {
      rows[[sub]] <- data.frame(
        outcome_subscale = sub,
        tau = NA_real_,
        status = r$status,
        estimate = NA_real_, se = NA_real_,
        ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
        n_used = NA_integer_,
        error_message = r$missing %||% NA_character_,
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

# ============================================================================
# 74 — Distributional Regression (brms mean + sigma)
# ============================================================================

dist_distributional_one <- function(long_data, outcome_subscale,
                                     chains = 2L, iter = 2000L) {
  if (!requireNamespace("brms", quietly = TRUE)) {
    return(list(status = "brms_unavailable"))
  }
  outcome <- dist_cocuk_outcome(outcome_subscale)
  needed <- c(outcome, "group_dm", "cocuk_yas_z", "ses_latent_z", "aile_no")
  if (any(!needed %in% names(long_data))) {
    return(list(status = "missing_columns",
      missing = setdiff(needed, names(long_data))))
  }
  dat <- long_data[stats::complete.cases(long_data[, needed]), , drop = FALSE]
  if (nrow(dat) < 50L) {
    return(list(status = "insufficient_n", n = nrow(dat)))
  }

  formula_obj <- brms::bf(
    stats::as.formula(sprintf("%s ~ group_dm + cocuk_yas_z + ses_latent_z + (1 | aile_no)",
      outcome)),
    sigma ~ group_dm
  )

  fit <- tryCatch(
    suppressWarnings(brms::brm(
      formula = formula_obj,
      data = dat,
      family = gaussian(),
      chains = chains,
      iter = iter,
      warmup = floor(iter / 2),
      refresh = 0,
      silent = 2,
      seed = 20260512
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", error_message = conditionMessage(fit)))
  }

  post <- as.matrix(fit, variable = c("b_group_dm", "b_sigma_group_dm"))
  mean_post <- post[, "b_group_dm"]
  sigma_post <- post[, "b_sigma_group_dm"]

  data.frame(
    outcome_subscale = outcome_subscale,
    parameter = c("mean", "sigma"),
    posterior_median = c(stats::median(mean_post), stats::median(sigma_post)),
    ci_lower = c(stats::quantile(mean_post, 0.025), stats::quantile(sigma_post, 0.025)),
    ci_upper = c(stats::quantile(mean_post, 0.975), stats::quantile(sigma_post, 0.975)),
    pd = c(mean(mean_post * sign(stats::median(mean_post)) > 0),
      mean(sigma_post * sign(stats::median(sigma_post)) > 0)),
    n_used = stats::nobs(fit),
    rhat_max = max(brms::rhat(fit), na.rm = TRUE),
    chains = chains,
    iter = iter,
    stringsAsFactors = FALSE
  )
}

dist_distributional_pipeline <- function(long_data,
                                          outcomes = dist_subscale_outcomes(),
                                          chains = 2L, iter = 2000L) {
  rows <- list()
  status_rows <- list()
  for (sub in outcomes) {
    r <- dist_distributional_one(long_data, sub, chains = chains, iter = iter)
    if (is.data.frame(r)) {
      rows[[sub]] <- r
      status_rows[[sub]] <- data.frame(
        outcome_subscale = sub,
        status = "ok",
        n_used = r$n_used[1L],
        rhat_max = r$rhat_max[1L],
        stringsAsFactors = FALSE
      )
    } else {
      status_rows[[sub]] <- data.frame(
        outcome_subscale = sub,
        status = r$status,
        n_used = NA_integer_,
        rhat_max = NA_real_,
        stringsAsFactors = FALSE
      )
    }
  }
  list(
    status = if (length(status_rows) > 0L) do.call(rbind, status_rows) else NULL,
    posterior = if (length(rows) > 0L) do.call(rbind, rows) else NULL
  )
}

# ============================================================================
# 75 — Beta Regression (gamlss::BE fallback)
# ============================================================================

dist_normalize_to_unit <- function(x, min_val = 1, max_val = 4) {
  # EMBU mean [1, 4] -> [eps, 1-eps]
  eps <- 1e-3
  out <- (x - min_val) / (max_val - min_val)
  out <- pmin(pmax(out, eps), 1 - eps)
  out
}

dist_beta_regression_one <- function(long_data, outcome_subscale) {
  outcome <- dist_cocuk_outcome(outcome_subscale)
  needed <- c(outcome, "group_dm", "cocuk_yas_z", "ses_latent_z")
  if (any(!needed %in% names(long_data))) {
    return(data.frame(
      outcome_subscale = outcome_subscale,
      status = "missing_columns",
      estimate = NA_real_, se = NA_real_,
      ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
      n_used = NA_integer_,
      stringsAsFactors = FALSE
    ))
  }
  dat <- long_data[stats::complete.cases(long_data[, needed]), , drop = FALSE]
  if (nrow(dat) < 30L) {
    return(data.frame(
      outcome_subscale = outcome_subscale,
      status = "insufficient_n",
      estimate = NA_real_, se = NA_real_,
      ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
      n_used = nrow(dat),
      stringsAsFactors = FALSE
    ))
  }
  dat$y_unit <- dist_normalize_to_unit(dat[[outcome]], min_val = 1, max_val = 4)

  if (requireNamespace("betareg", quietly = TRUE)) {
    fit <- tryCatch(
      betareg::betareg(y_unit ~ group_dm + cocuk_yas_z + ses_latent_z, data = dat),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      return(data.frame(
        outcome_subscale = outcome_subscale,
        status = "fit_error",
        estimate = NA_real_, se = NA_real_,
        ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
        n_used = nrow(dat),
        engine = "betareg",
        stringsAsFactors = FALSE
      ))
    }
    cs <- summary(fit)$coefficients$mean
    grp_idx <- which(rownames(cs) == "group_dm")
    est <- cs[grp_idx, 1L]
    se <- cs[grp_idx, 2L]
    p <- cs[grp_idx, 4L]
    engine <- "betareg"
  } else if (requireNamespace("gamlss", quietly = TRUE) &&
      requireNamespace("gamlss.dist", quietly = TRUE)) {
    fit <- tryCatch(
      suppressWarnings(gamlss::gamlss(
        y_unit ~ group_dm + cocuk_yas_z + ses_latent_z,
        family = gamlss.dist::BE(),
        data = dat,
        trace = FALSE
      )),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      return(data.frame(
        outcome_subscale = outcome_subscale,
        status = "fit_error",
        estimate = NA_real_, se = NA_real_,
        ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
        n_used = nrow(dat),
        engine = "gamlss::BE",
        stringsAsFactors = FALSE
      ))
    }
    sm <- summary(fit)
    grp_row <- sm[grep("group_dm", rownames(sm)), , drop = FALSE]
    if (nrow(grp_row) == 0L) {
      return(data.frame(
        outcome_subscale = outcome_subscale,
        status = "predictor_not_in_model",
        estimate = NA_real_, se = NA_real_,
        ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
        n_used = nrow(dat),
        engine = "gamlss::BE",
        stringsAsFactors = FALSE
      ))
    }
    est <- grp_row[1L, "Estimate"]
    se <- grp_row[1L, "Std. Error"]
    p <- grp_row[1L, "Pr(>|t|)"]
    engine <- "gamlss::BE"
  } else {
    return(data.frame(
      outcome_subscale = outcome_subscale,
      status = "no_beta_engine",
      estimate = NA_real_, se = NA_real_,
      ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
      n_used = nrow(dat),
      engine = "none",
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    outcome_subscale = outcome_subscale,
    status = "ok",
    estimate = est,
    se = se,
    ci_lower = est - 1.96 * se,
    ci_upper = est + 1.96 * se,
    p_value = p,
    n_used = nrow(dat),
    engine = engine,
    stringsAsFactors = FALSE
  )
}

dist_beta_regression_pipeline <- function(long_data,
                                           outcomes = dist_subscale_outcomes()) {
  rows <- list()
  for (sub in outcomes) {
    rows[[sub]] <- dist_beta_regression_one(long_data, sub)
  }
  bind_safe <- function(rows) {
    all_cols <- unique(unlist(lapply(rows, names)))
    rows_padded <- lapply(rows, function(r) {
      missing_cols <- setdiff(all_cols, names(r))
      for (mc in missing_cols) r[[mc]] <- NA
      r[, all_cols, drop = FALSE]
    })
    do.call(rbind, rows_padded)
  }
  bind_safe(rows)
}

# ============================================================================
# Pipeline
# ============================================================================

run_distributional_pipeline <- function(df_family_ses, df_long_scored,
                                        outcomes = dist_subscale_outcomes(),
                                        taus = c(0.50, 0.75, 0.90),
                                        bootstrap_R = 5000L,
                                        run_distributional = TRUE,
                                        brms_chains = 2L,
                                        brms_iter = 2000L) {
  long <- dist_prepare_long(df_long_scored, df_family_ses, outcomes = outcomes)

  quantile_table <- dist_quantile_regression_pipeline(long,
    outcomes = outcomes, taus = taus, bootstrap_R = bootstrap_R)

  distributional <- if (run_distributional) {
    dist_distributional_pipeline(long, outcomes = outcomes,
      chains = brms_chains, iter = brms_iter)
  } else {
    list(status = NULL, posterior = NULL)
  }

  beta_table <- dist_beta_regression_pipeline(long, outcomes = outcomes)

  list(
    n_long = nrow(long),
    quantile_table = quantile_table,
    distributional_status = distributional$status,
    distributional_posterior = distributional$posterior,
    beta_table = beta_table,
    target_summary = data.frame(
      analysis = "distributional_phase2",
      n_long = nrow(long),
      taus = paste(taus, collapse = ","),
      bootstrap_R = bootstrap_R,
      brms_chains = brms_chains,
      brms_iter = brms_iter,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXVI/73, 74, 75)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      betareg_used = requireNamespace("betareg", quietly = TRUE),
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
