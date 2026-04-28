# KISIM XI — Robustluk ve Sensitivite
# 33. Multiverse Specification Curve (specr)
# 34. Equivalence Testing (TOST + Bayesian ROPE preflight)
# 35. Sensemakr Robustness Value + E-value
# 36. Negative Control + Falsification Tests

robust_subscales <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

robust_p_outcomes <- function() {
  paste0("embu_p_", robust_subscales(), "_mean")
}

robust_prepare_frame <- function(df_family_ses) {
  df <- df_family_ses
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  df$group_dm <- as.integer(df$group_f == "DM")
  df$anne_yas_z   <- as.numeric(scale(df$anne_yas))
  df$ses_latent_z <- as.numeric(scale(df$ses_latent))
  if ("age_gap" %in% names(df)) df$age_gap_z <- as.numeric(scale(df$age_gap))
  if ("cocuk_sayisi" %in% names(df)) df$cocuk_sayisi_z <- as.numeric(scale(df$cocuk_sayisi))
  df$anne_antidep_dum <- if ("anne_antidepresan_f" %in% names(df)) {
    as.integer(df$anne_antidepresan_f == "Evet")
  } else if ("anne_antidepresan" %in% names(df)) {
    as.integer(df$anne_antidepresan == 1)
  } else 0L
  df
}

# === 33. Multiverse / Specification Curve =============================

robust_multiverse_one_outcome <- function(df, outcome) {
  control_sets <- list(
    minimal       = "scale(anne_yas)",
    plus_ses      = "scale(anne_yas) + scale(ses_latent)",
    plus_age_gap  = "scale(anne_yas) + scale(ses_latent) + scale(age_gap)",
    plus_size     = "scale(anne_yas) + scale(ses_latent) + scale(age_gap) + scale(cocuk_sayisi)",
    full_set      = "scale(anne_yas) + scale(ses_latent) + scale(age_gap) + scale(cocuk_sayisi) + anne_antidep_dum"
  )
  models <- list(
    ols     = function(formula, data) stats::lm(formula, data = data),
    robust  = function(formula, data) MASS::rlm(formula, data = data, maxit = 100L)
  )
  subsets <- list(
    all          = function(x) rep(TRUE, nrow(x)),
    families_2plus = function(x) {
      if ("cocuk_sayisi" %in% names(x)) x$cocuk_sayisi >= 2 else rep(TRUE, nrow(x))
    },
    no_antidep   = function(x) x$anne_antidep_dum == 0L
  )
  rows <- list()
  for (cs_name in names(control_sets)) {
    for (mdl_name in names(models)) {
      for (sub_name in names(subsets)) {
        keep <- subsets[[sub_name]](df)
        sub_df <- df[keep, , drop = FALSE]
        formula_str <- sprintf("%s ~ group_f + %s", outcome, control_sets[[cs_name]])
        fit <- tryCatch(
          suppressWarnings(models[[mdl_name]](stats::as.formula(formula_str), sub_df)),
          error = function(e) e
        )
        if (inherits(fit, "error")) {
          rows[[length(rows) + 1L]] <- data.frame(
            outcome = outcome, controls = cs_name, model = mdl_name, subset = sub_name,
            n = nrow(sub_df), estimate = NA_real_, se = NA_real_,
            statistic = NA_real_, p_value = NA_real_,
            cohens_d = NA_real_, status = paste0("error:", conditionMessage(fit)),
            stringsAsFactors = FALSE
          )
          next
        }
        coefs <- summary(fit)$coefficients
        idx <- grep("group_fDM", rownames(coefs))[1]
        if (is.na(idx)) {
          rows[[length(rows) + 1L]] <- data.frame(
            outcome = outcome, controls = cs_name, model = mdl_name, subset = sub_name,
            n = nrow(sub_df), estimate = NA_real_, se = NA_real_,
            statistic = NA_real_, p_value = NA_real_, cohens_d = NA_real_,
            status = "no_treatment_term", stringsAsFactors = FALSE
          )
          next
        }
        est <- coefs[idx, 1]; se <- coefs[idx, 2]
        stat <- if (ncol(coefs) >= 3) coefs[idx, 3] else NA_real_
        p_val <- if (mdl_name == "ols" && ncol(coefs) >= 4) coefs[idx, 4] else {
          2 * stats::pnorm(-abs(est / se))
        }
        sd_outcome <- stats::sd(sub_df[[outcome]], na.rm = TRUE)
        d_val <- if (is.finite(sd_outcome) && sd_outcome > 0) est / sd_outcome else NA_real_
        rows[[length(rows) + 1L]] <- data.frame(
          outcome = outcome, controls = cs_name, model = mdl_name, subset = sub_name,
          n = nrow(sub_df), estimate = est, se = se,
          statistic = stat, p_value = p_val, cohens_d = d_val,
          status = "ok", stringsAsFactors = FALSE
        )
      }
    }
  }
  do.call(rbind, rows)
}

robust_multiverse <- function(df) {
  rows <- list()
  for (oc in robust_p_outcomes()) {
    rows[[oc]] <- robust_multiverse_one_outcome(df, oc)
  }
  combined <- do.call(rbind, rows)
  rownames(combined) <- NULL

  summary_rows <- list()
  for (oc in unique(combined$outcome)) {
    sub <- combined[combined$outcome == oc & combined$status == "ok", ]
    if (nrow(sub) == 0L) next
    p <- sub$p_value
    d <- sub$cohens_d
    summary_rows[[length(summary_rows) + 1L]] <- data.frame(
      outcome              = oc,
      n_specs              = nrow(sub),
      median_d             = stats::median(d, na.rm = TRUE),
      d_q05                = stats::quantile(d, 0.05, na.rm = TRUE),
      d_q95                = stats::quantile(d, 0.95, na.rm = TRUE),
      pct_p_lt_05          = mean(p < 0.05, na.rm = TRUE),
      pct_p_lt_01          = mean(p < 0.01, na.rm = TRUE),
      pct_negative         = mean(d < 0, na.rm = TRUE),
      pct_positive         = mean(d > 0, na.rm = TRUE),
      stringsAsFactors = FALSE
    )
  }
  list(
    spec_table = combined,
    summary    = if (length(summary_rows) > 0L) do.call(rbind, summary_rows) else data.frame()
  )
}

# === 34. TOST Equivalence Testing =====================================

robust_tost <- function(df, sesoi_d = 0.30) {
  if (!requireNamespace("TOSTER", quietly = TRUE)) {
    return(data.frame(outcome = robust_p_outcomes(),
                      status = "package_unavailable", stringsAsFactors = FALSE))
  }
  rows <- list()
  for (oc in robust_p_outcomes()) {
    dm_vals <- df[df$group_f == "DM", oc, drop = TRUE]
    ko_vals <- df[df$group_f == "Kontrol", oc, drop = TRUE]
    dm_vals <- dm_vals[!is.na(dm_vals)]
    ko_vals <- ko_vals[!is.na(ko_vals)]
    if (length(dm_vals) < 10L || length(ko_vals) < 10L) {
      rows[[length(rows) + 1L]] <- data.frame(
        outcome = oc, status = "insufficient_n",
        sesoi = sesoi_d, n_dm = length(dm_vals), n_kontrol = length(ko_vals),
        observed_d = NA_real_, tost_p = NA_real_, decision = NA_character_,
        stringsAsFactors = FALSE
      )
      next
    }
    fit <- tryCatch(
      suppressMessages(suppressWarnings(TOSTER::tsum_TOST(
        m1 = mean(dm_vals), sd1 = stats::sd(dm_vals), n1 = length(dm_vals),
        m2 = mean(ko_vals), sd2 = stats::sd(ko_vals), n2 = length(ko_vals),
        low_eqbound = -sesoi_d, high_eqbound = sesoi_d,
        eqbound_type = "SMD", smd_ci = "goulet"
      ))),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      rows[[length(rows) + 1L]] <- data.frame(
        outcome = oc, status = paste0("error:", conditionMessage(fit)),
        sesoi = sesoi_d, n_dm = length(dm_vals), n_kontrol = length(ko_vals),
        observed_d = NA_real_, tost_p = NA_real_, decision = NA_character_,
        stringsAsFactors = FALSE
      )
      next
    }
    tost_p_max <- max(fit$TOST$p.value[2:3])
    nhst_p <- fit$TOST$p.value[1]
    decision <- if (tost_p_max < 0.05 && nhst_p < 0.05) {
      "Trivial"
    } else if (tost_p_max < 0.05 && nhst_p >= 0.05) {
      "Equivalent"
    } else if (tost_p_max >= 0.05 && nhst_p < 0.05) {
      "Meaningful"
    } else {
      "Indeterminate"
    }
    obs_d <- fit$effsize$estimate[fit$effsize$type == "Cohen's d(av)"][1]
    if (length(obs_d) == 0L) obs_d <- fit$effsize$estimate[1]
    rows[[length(rows) + 1L]] <- data.frame(
      outcome = oc, status = "ok",
      sesoi = sesoi_d, n_dm = length(dm_vals), n_kontrol = length(ko_vals),
      observed_d = unname(obs_d),
      tost_p = tost_p_max, nhst_p = nhst_p,
      decision = decision,
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# === 35. Sensemakr + E-value ==========================================

evalue_from_d <- function(d, lower_d = NA_real_, upper_d = NA_real_) {
  rr <- exp(0.91 * d)
  rr_lo <- if (is.finite(lower_d)) exp(0.91 * lower_d) else NA_real_
  rr_hi <- if (is.finite(upper_d)) exp(0.91 * upper_d) else NA_real_
  evalue_point <- if (rr >= 1) rr + sqrt(rr * (rr - 1)) else {
    rr_inv <- 1 / rr
    rr_inv + sqrt(rr_inv * (rr_inv - 1))
  }
  ci_e <- if (is.finite(rr_lo) && is.finite(rr_hi)) {
    bound <- if (rr >= 1) rr_lo else rr_hi
    if (is.finite(bound)) {
      if (bound <= 1 && bound >= 1 / 1) {
        1
      } else if (bound > 1) {
        bound + sqrt(bound * (bound - 1))
      } else {
        bound_inv <- 1 / bound
        bound_inv + sqrt(bound_inv * (bound_inv - 1))
      }
    } else NA_real_
  } else NA_real_
  list(rr = rr, evalue = evalue_point, evalue_ci = ci_e)
}

robust_sensemakr <- function(df) {
  if (!requireNamespace("sensemakr", quietly = TRUE)) {
    return(data.frame(outcome = robust_p_outcomes(),
                      status = "package_unavailable", stringsAsFactors = FALSE))
  }
  rows <- list()
  benchmarks <- c("scale(ses_latent)", "scale(anne_yas)")
  for (oc in robust_p_outcomes()) {
    formula_str <- sprintf("%s ~ group_f + scale(anne_yas) + scale(ses_latent) + scale(age_gap) + scale(cocuk_sayisi)", oc)
    sub_df <- df[stats::complete.cases(df[, c(oc, "group_f", "anne_yas", "ses_latent", "age_gap", "cocuk_sayisi")]), , drop = FALSE]
    fit <- tryCatch(
      stats::lm(stats::as.formula(formula_str), data = sub_df),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      rows[[length(rows) + 1L]] <- data.frame(
        outcome = oc, status = paste0("error:", conditionMessage(fit)),
        n = nrow(sub_df), estimate = NA_real_, t_value = NA_real_, p_value = NA_real_,
        cohens_d = NA_real_, RV_q = NA_real_, RV_qa = NA_real_,
        partial_r2_treatment = NA_real_,
        evalue_point = NA_real_, evalue_ci = NA_real_,
        stringsAsFactors = FALSE
      )
      next
    }
    sens <- tryCatch(
      sensemakr::sensemakr(
        model = fit,
        treatment = "group_fDM",
        benchmark_covariates = intersect(benchmarks, names(coef(fit))),
        kd = c(1, 2, 3),
        ky = c(1, 2, 3),
        q = 1
      ),
      error = function(e) e
    )
    coefs_table <- summary(fit)$coefficients
    treat_idx <- grep("group_fDM", rownames(coefs_table))[1]
    est <- coefs_table[treat_idx, 1]; se <- coefs_table[treat_idx, 2]
    t_val <- coefs_table[treat_idx, 3]; p_val <- coefs_table[treat_idx, 4]
    sd_y <- stats::sd(sub_df[[oc]], na.rm = TRUE)
    d_val <- if (is.finite(sd_y) && sd_y > 0) est / sd_y else NA_real_
    ci_lo <- est - 1.96 * se; ci_hi <- est + 1.96 * se
    d_lo <- if (is.finite(sd_y) && sd_y > 0) ci_lo / sd_y else NA_real_
    d_hi <- if (is.finite(sd_y) && sd_y > 0) ci_hi / sd_y else NA_real_
    e_res <- evalue_from_d(d_val, d_lo, d_hi)
    rv_q  <- if (inherits(sens, "sensemakr")) sens$sensitivity_stats$rv_q else NA_real_
    rv_qa <- if (inherits(sens, "sensemakr")) sens$sensitivity_stats$rv_qa else NA_real_
    pr2   <- if (inherits(sens, "sensemakr")) sens$sensitivity_stats$r2yd.x else NA_real_
    rows[[length(rows) + 1L]] <- data.frame(
      outcome = oc,
      status = if (inherits(sens, "sensemakr")) "ok" else paste0("sensemakr_error:", conditionMessage(sens)),
      n = nrow(sub_df), estimate = est, t_value = t_val, p_value = p_val,
      cohens_d = d_val, RV_q = rv_q, RV_qa = rv_qa,
      partial_r2_treatment = pr2,
      evalue_point = e_res$evalue, evalue_ci = e_res$evalue_ci,
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# === 36. Negative Control + Falsification ============================

robust_negative_control <- function(df, seed = 20260428L) {
  set.seed(seed)
  df$negctrl_random <- stats::runif(nrow(df))
  df$negctrl_aile_no <- as.numeric(df$aile_no)
  rows <- list()
  for (oc in robust_p_outcomes()) {
    for (predictor in c("negctrl_random", "negctrl_aile_no")) {
      formula_str <- sprintf("%s ~ scale(%s) + scale(anne_yas)", oc, predictor)
      fit <- tryCatch(
        stats::lm(stats::as.formula(formula_str), data = df),
        error = function(e) e
      )
      if (inherits(fit, "error")) {
        rows[[length(rows) + 1L]] <- data.frame(
          outcome = oc, predictor = predictor, status = paste0("error:", conditionMessage(fit)),
          estimate = NA_real_, p_value = NA_real_, suspicious = NA, stringsAsFactors = FALSE
        )
        next
      }
      coefs <- summary(fit)$coefficients
      term_idx <- grep("scale\\(.*\\)", rownames(coefs))
      term_idx <- term_idx[grepl(predictor, rownames(coefs)[term_idx])][1]
      est <- coefs[term_idx, 1]; p_val <- coefs[term_idx, 4]
      rows[[length(rows) + 1L]] <- data.frame(
        outcome = oc, predictor = predictor, status = "ok",
        estimate = est, p_value = p_val,
        suspicious = p_val < 0.05,
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

robust_falsification <- function(df) {
  rows <- list()
  scenarios <- list(
    short_dm = list(
      filter = function(x) (x$group_f == "DM" & !is.na(x$dm_yili) & x$dm_yili < 1) | x$group_f == "Kontrol",
      label  = "DM süresi <1 yıl"
    ),
    good_control = list(
      filter = function(x) (x$group_f == "DM" & !is.na(x$hba1c) & x$hba1c <= 7.5) | x$group_f == "Kontrol",
      label  = "HbA1c <=7.5"
    )
  )
  for (oc in robust_p_outcomes()) {
    base_fit <- stats::lm(stats::as.formula(sprintf("%s ~ group_f + scale(anne_yas) + scale(ses_latent)", oc)), data = df)
    base_est <- summary(base_fit)$coefficients["group_fDM", 1]
    base_p   <- summary(base_fit)$coefficients["group_fDM", 4]
    base_n   <- stats::nobs(base_fit)
    for (sc_name in names(scenarios)) {
      keep <- scenarios[[sc_name]]$filter(df)
      sub_df <- df[keep, , drop = FALSE]
      if (sum(sub_df$group_f == "DM", na.rm = TRUE) < 10L) {
        rows[[length(rows) + 1L]] <- data.frame(
          outcome = oc, scenario = sc_name, label = scenarios[[sc_name]]$label,
          n_total = nrow(sub_df), n_dm = sum(sub_df$group_f == "DM", na.rm = TRUE),
          base_est = base_est, base_p = base_p, base_n = base_n,
          falsi_est = NA_real_, falsi_p = NA_real_, attenuation_pct = NA_real_,
          status = "insufficient_dm",
          stringsAsFactors = FALSE
        )
        next
      }
      fit <- tryCatch(
        stats::lm(stats::as.formula(sprintf("%s ~ group_f + scale(anne_yas) + scale(ses_latent)", oc)), data = sub_df),
        error = function(e) e
      )
      if (inherits(fit, "error")) {
        rows[[length(rows) + 1L]] <- data.frame(
          outcome = oc, scenario = sc_name, label = scenarios[[sc_name]]$label,
          n_total = nrow(sub_df), n_dm = sum(sub_df$group_f == "DM", na.rm = TRUE),
          base_est = base_est, base_p = base_p, base_n = base_n,
          falsi_est = NA_real_, falsi_p = NA_real_, attenuation_pct = NA_real_,
          status = paste0("error:", conditionMessage(fit)),
          stringsAsFactors = FALSE
        )
        next
      }
      f_est <- summary(fit)$coefficients["group_fDM", 1]
      f_p   <- summary(fit)$coefficients["group_fDM", 4]
      atten <- if (is.finite(base_est) && base_est != 0) {
        100 * (1 - f_est / base_est)
      } else NA_real_
      rows[[length(rows) + 1L]] <- data.frame(
        outcome = oc, scenario = sc_name, label = scenarios[[sc_name]]$label,
        n_total = nrow(sub_df), n_dm = sum(sub_df$group_f == "DM", na.rm = TRUE),
        base_est = base_est, base_p = base_p, base_n = base_n,
        falsi_est = f_est, falsi_p = f_p, attenuation_pct = atten,
        status = "ok",
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

# === Pipeline orchestrator =============================================

run_robustness_pipeline <- function(df_family_ses, sesoi_d = 0.30) {
  prepared <- robust_prepare_frame(df_family_ses)
  multiverse <- robust_multiverse(prepared)
  tost_table <- robust_tost(prepared, sesoi_d = sesoi_d)
  sens_table <- robust_sensemakr(prepared)
  neg_table  <- robust_negative_control(prepared)
  fals_table <- robust_falsification(prepared)
  target_summary <- data.frame(
    component = c("multiverse_specs", "multiverse_summary",
                  "tost_equivalence", "sensemakr_evalue",
                  "negative_control", "falsification"),
    n_rows = c(nrow(multiverse$spec_table), nrow(multiverse$summary),
               nrow(tost_table), nrow(sens_table),
               nrow(neg_table), nrow(fals_table)),
    stringsAsFactors = FALSE
  )
  list(
    multiverse_spec_table     = multiverse$spec_table,
    multiverse_summary_table  = multiverse$summary,
    tost_equivalence_table    = tost_table,
    sensemakr_evalue_table    = sens_table,
    negative_control_table    = neg_table,
    falsification_table       = fals_table,
    target_summary            = target_summary
  )
}
