# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXII/58-60
# Anne Antidepresan Kullanim Hatti
#
# 58 — Antidepresan aracilik (mediator) modeli: group_dm -> AD -> EMBU-P_red
#      lavaan SEM + BCa bootstrap CI; mediation paketi yoksa lavaan-tabanli
#      indirect effect raporlanir, sensitivity rho icin manuel uyari notu eklenir.
#
# 59 — AD x Grup moderasyonu: H1 (cocuk algi), H4 (Beck->parenting), H5
#      (diadik konkordans) uzerinde anne_antidepresan_bin moderator etkisi.
#      Cikti: alt-grup etki buyuklukleri (AD+ vs AD-) DM altgrubunda.
#
# 60 — Beck x AD manifest etkilesim: Beck total z-score, AD bin ve etkilesim
#      terimi parenting outcomes uzerinde (lm + HC3 robust SE). Latent LMS
#      bir sonraki iterasyonda (xxM/nlsem fallback) derinlestirilecektir.
#
# Skill referanslari: references/mediation-modelleri.md,
#                     references/nedensellik-ve-ps.md
# Veri: df_family_ses (anne EMBU-P + Beck + SES + AD), df_long_scored[Indeks]

ad_normalize <- function(x) {
  vals <- suppressWarnings(as.numeric(x))
  bin <- ifelse(is.na(vals), NA_integer_, ifelse(vals > 0, 1L, 0L))
  bin
}

ad_factor_from_bin <- function(bin) {
  factor(bin, levels = c(0L, 1L), labels = c("Yok", "Var"))
}

ad_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s",
        context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

ad_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

ad_scale_vector <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

ad_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

ad_prepare_family_frame <- function(df_family_ses) {
  required <- c("aile_no", "group_dm", "anne_antidepresan", "beck_total",
    "ses_latent", "anne_yas",
    paste0("embu_p_", ad_subscale_outcomes(), "_mean"))
  ad_require_columns(df_family_ses, required, "AD family frame")

  out <- df_family_ses[, required, drop = FALSE]
  out$ad_bin <- ad_normalize(out$anne_antidepresan)
  out$ad_f <- ad_factor_from_bin(out$ad_bin)
  out$beck_total_z <- ad_scale_vector(out$beck_total)
  out$ses_latent_z <- ad_scale_vector(out$ses_latent)
  out$anne_yas_z <- ad_scale_vector(out$anne_yas)
  out$group_dm <- as.integer(out$group_dm)
  out
}

ad_prepare_long_frame <- function(df_long_scored, family_frame) {
  required_long <- c("aile_no", "family_role_f", "cocuk_yas",
    paste0("embu_c_", ad_subscale_outcomes(), "_mean"))
  ad_require_columns(df_long_scored, required_long, "AD long frame")

  long <- df_long_scored[, required_long, drop = FALSE]
  long$role_token <- ad_normalize_role(long$family_role_f)
  # Indeks + Kardes her ikisini de tut (multilevel ICC icin aile basina ≥ 2 satir)
  long <- long[!is.na(long$role_token), , drop = FALSE]
  long$cocuk_yas_z <- ad_scale_vector(long$cocuk_yas)

  family_join <- family_frame[, c("aile_no", "group_dm", "ad_bin", "ad_f",
    "beck_total_z", "ses_latent_z", "anne_yas_z",
    paste0("embu_p_", ad_subscale_outcomes(), "_mean")), drop = FALSE]
  paired <- merge(long, family_join, by = "aile_no", all.x = FALSE, all.y = FALSE)
  paired
}

# ============================================================================
# 58 — Antidepresan Aracilik (Mediator) Modeli
# ============================================================================

ad_mediator_lavaan_syntax <- function(outcome_col_p,
                                      treatment = "group_dm",
                                      mediator = "ad_bin",
                                      covariates = c("ses_latent_z", "anne_yas_z")) {
  cov_str <- if (length(covariates) > 0L) paste("+", paste(covariates, collapse = " + ")) else ""
  paste(
    sprintf("# Mediator yolu (a)"),
    sprintf("%s ~ a * %s %s", mediator, treatment, cov_str),
    sprintf("# Outcome yolu (b, c')"),
    sprintf("%s ~ b * %s + cprime * %s %s", outcome_col_p, mediator, treatment, cov_str),
    sprintf("# Indirect ve total effects"),
    sprintf("indirect := a * b"),
    sprintf("total := cprime + a * b"),
    sprintf("prop_mediated := (a * b) / (cprime + a * b)"),
    sep = "\n"
  )
}

ad_mediator_fit_one <- function(family_frame, outcome_subscale,
                                bootstrap_n = 1000L,
                                seed = 20260507L) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = "lavaan_unavailable"))
  }
  outcome <- paste0("embu_p_", outcome_subscale, "_mean")
  syntax <- ad_mediator_lavaan_syntax(outcome)
  set.seed(seed)
  # Bootstrap SE icin lavaan ML estimator (MLR + bootstrap desteklenmez)
  fit <- tryCatch(
    suppressWarnings(lavaan::sem(
      syntax,
      data = family_frame,
      se = "bootstrap",
      bootstrap = bootstrap_n,
      estimator = "ML"
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(
      status = "fit_error",
      outcome_subscale = outcome_subscale,
      error_message = conditionMessage(fit)
    ))
  }

  est <- lavaan::parameterEstimates(fit, ci = TRUE, boot.ci.type = "bca.simple")
  rows <- est[est$op %in% c("~", ":="), , drop = FALSE]
  rows$outcome_subscale <- outcome_subscale

  # Sensitivity rho — mediator-outcome confounder strength tahmini
  # Imai-Keele 2010 yaklasimi: rho_critical = corr(residual_mediator, residual_outcome)
  med_resid <- stats::residuals(stats::lm(
    stats::as.formula(sprintf("ad_bin ~ group_dm + ses_latent_z + anne_yas_z")),
    data = family_frame, na.action = stats::na.exclude
  ))
  out_resid <- stats::residuals(stats::lm(
    stats::as.formula(sprintf("%s ~ ad_bin + group_dm + ses_latent_z + anne_yas_z", outcome)),
    data = family_frame, na.action = stats::na.exclude
  ))
  ok <- !is.na(med_resid) & !is.na(out_resid)
  rho_obs <- stats::cor(med_resid[ok], out_resid[ok])

  list(
    status = "ok",
    outcome_subscale = outcome_subscale,
    estimates = rows,
    rho_observed_residual_corr = rho_obs,
    n_used = sum(stats::complete.cases(family_frame[, c(outcome, "ad_bin", "group_dm",
      "ses_latent_z", "anne_yas_z"), drop = FALSE]))
  )
}

ad_mediator_pipeline <- function(family_frame, bootstrap_n = 1000L,
                                 outcomes = ad_subscale_outcomes()) {
  status_rows <- list()
  estimates_rows <- list()
  sensitivity_rows <- list()
  for (sub in outcomes) {
    res <- ad_mediator_fit_one(family_frame, sub, bootstrap_n = bootstrap_n)
    status_rows[[sub]] <- data.frame(
      outcome_subscale = sub,
      status = res$status,
      n_used = if (identical(res$status, "ok")) res$n_used else NA_integer_,
      bootstrap_n = bootstrap_n,
      error_message = res$error_message %||% NA_character_,
      stringsAsFactors = FALSE
    )
    if (identical(res$status, "ok")) {
      df_e <- res$estimates
      est_clean <- data.frame(
        outcome_subscale = sub,
        op = df_e$op,
        lhs = df_e$lhs,
        rhs = df_e$rhs,
        label = df_e$label,
        est = df_e$est,
        se = df_e$se,
        ci_lower = df_e$ci.lower,
        ci_upper = df_e$ci.upper,
        p_value = df_e$pvalue,
        stringsAsFactors = FALSE
      )
      estimates_rows[[sub]] <- est_clean
      sensitivity_rows[[sub]] <- data.frame(
        outcome_subscale = sub,
        rho_observed_residual_corr = res$rho_observed_residual_corr,
        rho_critical_threshold = 0.10,
        interpretation = if (abs(res$rho_observed_residual_corr) < 0.10) {
          "small_residual_corr_low_concern"
        } else {
          "moderate_residual_corr_check_unmeasured_confounders"
        },
        stringsAsFactors = FALSE
      )
    }
  }
  bind <- function(rows) if (length(rows) > 0L) do.call(rbind, rows) else NULL
  list(
    status = bind(status_rows),
    estimates = bind(estimates_rows),
    sensitivity = bind(sensitivity_rows)
  )
}

# ============================================================================
# 59 — AD x Grup Moderasyonu (H1 / H4 / H5 paralel)
# ============================================================================

ad_moderation_h1_one <- function(long_frame, outcome_subscale) {
  outcome <- paste0("embu_c_", outcome_subscale, "_mean")
  formula <- stats::as.formula(sprintf(
    "%s ~ group_dm * ad_bin + cocuk_yas_z + ses_latent_z + (1 | aile_no)",
    outcome
  ))
  if (!requireNamespace("lme4", quietly = TRUE) ||
        !requireNamespace("lmerTest", quietly = TRUE)) {
    return(list(status = "lme4_unavailable", outcome_subscale = outcome_subscale))
  }
  fit <- tryCatch(
    lmerTest::lmer(formula, data = long_frame),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error",
      outcome_subscale = outcome_subscale,
      error_message = conditionMessage(fit)))
  }
  coefs <- summary(fit)$coefficients
  fixed <- as.data.frame(coefs)
  fixed$term <- rownames(coefs)
  rownames(fixed) <- NULL
  names(fixed) <- gsub("[ ,()<>]+", "_", names(fixed))
  list(
    status = "ok",
    outcome_subscale = outcome_subscale,
    fixed_effects = fixed,
    aic = stats::AIC(fit),
    n_used = stats::nobs(fit)
  )
}

ad_moderation_pipeline_h1 <- function(long_frame, outcomes = ad_subscale_outcomes()) {
  status_rows <- list()
  fe_rows <- list()
  for (sub in outcomes) {
    r <- ad_moderation_h1_one(long_frame, sub)
    status_rows[[sub]] <- data.frame(
      hypothesis = "H1",
      outcome_subscale = sub,
      status = r$status,
      n_used = r$n_used %||% NA_integer_,
      aic = r$aic %||% NA_real_,
      error_message = r$error_message %||% NA_character_,
      stringsAsFactors = FALSE
    )
    if (identical(r$status, "ok")) {
      df_fe <- r$fixed_effects
      df_fe$hypothesis <- "H1"
      df_fe$outcome_subscale <- sub
      fe_rows[[sub]] <- df_fe
    }
  }
  list(
    status = if (length(status_rows) > 0L) do.call(rbind, status_rows) else NULL,
    fixed_effects = if (length(fe_rows) > 0L) do.call(rbind, fe_rows) else NULL
  )
}

ad_moderation_pipeline_h4 <- function(family_frame, outcomes = ad_subscale_outcomes()) {
  status_rows <- list()
  estimates_rows <- list()
  for (sub in outcomes) {
    outcome <- paste0("embu_p_", sub, "_mean")
    formula <- stats::as.formula(sprintf(
      "%s ~ beck_total_z * ad_bin + group_dm + ses_latent_z + anne_yas_z",
      outcome
    ))
    fit <- tryCatch(stats::lm(formula, data = family_frame), error = function(e) e)
    if (inherits(fit, "error")) {
      status_rows[[sub]] <- data.frame(
        hypothesis = "H4",
        outcome_subscale = sub,
        status = "fit_error",
        n_used = NA_integer_,
        r_squared = NA_real_,
        error_message = conditionMessage(fit),
        stringsAsFactors = FALSE
      )
      next
    }
    sm <- summary(fit)
    coef_df <- as.data.frame(sm$coefficients)
    coef_df$term <- rownames(coef_df)
    rownames(coef_df) <- NULL
    names(coef_df) <- gsub("[ ,()<>]+", "_", names(coef_df))
    coef_df$hypothesis <- "H4"
    coef_df$outcome_subscale <- sub
    estimates_rows[[sub]] <- coef_df
    status_rows[[sub]] <- data.frame(
      hypothesis = "H4",
      outcome_subscale = sub,
      status = "ok",
      n_used = stats::nobs(fit),
      r_squared = sm$r.squared,
      error_message = NA_character_,
      stringsAsFactors = FALSE
    )
  }
  list(
    status = if (length(status_rows) > 0L) do.call(rbind, status_rows) else NULL,
    fixed_effects = if (length(estimates_rows) > 0L) do.call(rbind, estimates_rows) else NULL
  )
}

ad_moderation_pipeline_h5 <- function(family_frame, long_frame,
                                      outcomes = ad_subscale_outcomes()) {
  rows <- list()
  for (sub in outcomes) {
    p_col <- paste0("embu_p_", sub, "_mean")
    c_col <- paste0("embu_c_", sub, "_mean")
    paired <- merge(
      family_frame[, c("aile_no", "ad_bin", "group_dm", p_col), drop = FALSE],
      long_frame[long_frame$role_token == "indeks", c("aile_no", c_col), drop = FALSE],
      by = "aile_no", all = FALSE
    )
    paired$ad_bin <- as.integer(paired$ad_bin)
    paired$group_dm <- as.integer(paired$group_dm)
    for (g in c(0L, 1L)) {
      for (a in c(0L, 1L)) {
        sub_data <- paired[paired$group_dm == g & paired$ad_bin == a, , drop = FALSE]
        if (nrow(sub_data) >= 5L) {
          r <- stats::cor.test(sub_data[[p_col]], sub_data[[c_col]],
            method = "pearson", use = "pairwise.complete.obs"
          )
          rows[[length(rows) + 1L]] <- data.frame(
            hypothesis = "H5",
            outcome_subscale = sub,
            group_dm = g,
            ad_bin = a,
            n = nrow(sub_data),
            pearson_r = unname(r$estimate),
            ci_lower = unname(r$conf.int[1L]),
            ci_upper = unname(r$conf.int[2L]),
            p_value = unname(r$p.value),
            stringsAsFactors = FALSE
          )
        } else {
          rows[[length(rows) + 1L]] <- data.frame(
            hypothesis = "H5",
            outcome_subscale = sub,
            group_dm = g,
            ad_bin = a,
            n = nrow(sub_data),
            pearson_r = NA_real_,
            ci_lower = NA_real_,
            ci_upper = NA_real_,
            p_value = NA_real_,
            stringsAsFactors = FALSE
          )
        }
      }
    }
  }
  list(stratified_correlations = if (length(rows) > 0L) do.call(rbind, rows) else NULL)
}

# ============================================================================
# 60 — Beck x AD Manifest Etkilesim
# ============================================================================

ad_beck_interaction_one <- function(family_frame, outcome_subscale) {
  outcome <- paste0("embu_p_", outcome_subscale, "_mean")
  formula <- stats::as.formula(sprintf(
    "%s ~ beck_total_z * ad_f + group_dm + ses_latent_z + anne_yas_z",
    outcome
  ))
  fit <- tryCatch(stats::lm(formula, data = family_frame), error = function(e) e)
  if (inherits(fit, "error")) {
    return(list(status = "fit_error",
      outcome_subscale = outcome_subscale,
      error_message = conditionMessage(fit)))
  }

  hc3_se <- if (requireNamespace("sandwich", quietly = TRUE) &&
      requireNamespace("lmtest", quietly = TRUE)) {
    suppressWarnings(lmtest::coeftest(fit, vcov. = sandwich::vcovHC(fit, type = "HC3")))
  } else {
    NULL
  }

  sm <- summary(fit)
  coef_df <- as.data.frame(sm$coefficients)
  coef_df$term <- rownames(coef_df)
  rownames(coef_df) <- NULL
  names(coef_df) <- gsub("[ ,()<>]+", "_", names(coef_df))

  if (!is.null(hc3_se)) {
    coef_df$hc3_se <- hc3_se[, "Std. Error"]
    coef_df$hc3_t <- hc3_se[, "t value"]
    coef_df$hc3_p <- hc3_se[, "Pr(>|t|)"]
  } else {
    coef_df$hc3_se <- NA_real_
    coef_df$hc3_t <- NA_real_
    coef_df$hc3_p <- NA_real_
  }

  coef_df$outcome_subscale <- outcome_subscale
  list(
    status = "ok",
    outcome_subscale = outcome_subscale,
    fixed_effects = coef_df,
    n_used = stats::nobs(fit),
    r_squared = sm$r.squared
  )
}

ad_beck_interaction_pipeline <- function(family_frame, outcomes = ad_subscale_outcomes()) {
  status_rows <- list()
  fe_rows <- list()
  for (sub in outcomes) {
    r <- ad_beck_interaction_one(family_frame, sub)
    status_rows[[sub]] <- data.frame(
      analysis = "beck_x_ad_interaction",
      outcome_subscale = sub,
      status = r$status,
      n_used = r$n_used %||% NA_integer_,
      r_squared = r$r_squared %||% NA_real_,
      error_message = r$error_message %||% NA_character_,
      stringsAsFactors = FALSE
    )
    if (identical(r$status, "ok")) {
      fe_rows[[sub]] <- r$fixed_effects
    }
  }
  list(
    status = if (length(status_rows) > 0L) do.call(rbind, status_rows) else NULL,
    fixed_effects = if (length(fe_rows) > 0L) do.call(rbind, fe_rows) else NULL
  )
}

# ============================================================================
# Pipeline
# ============================================================================

run_ad_pathway_pipeline <- function(df_family_ses, df_long_scored,
                                    bootstrap_n = 1000L) {
  family_frame <- ad_prepare_family_frame(df_family_ses)
  long_frame <- ad_prepare_long_frame(df_long_scored, family_frame)

  mediator <- ad_mediator_pipeline(family_frame, bootstrap_n = bootstrap_n)
  mod_h1 <- ad_moderation_pipeline_h1(long_frame)
  mod_h4 <- ad_moderation_pipeline_h4(family_frame)
  mod_h5 <- ad_moderation_pipeline_h5(family_frame, long_frame)
  beck_int <- ad_beck_interaction_pipeline(family_frame)

  list(
    family_summary = data.frame(
      n_total = nrow(family_frame),
      n_ad_yok = sum(family_frame$ad_bin == 0L, na.rm = TRUE),
      n_ad_var = sum(family_frame$ad_bin == 1L, na.rm = TRUE),
      n_ad_var_dm = sum(family_frame$ad_bin == 1L & family_frame$group_dm == 1L, na.rm = TRUE),
      n_ad_var_kontrol = sum(family_frame$ad_bin == 1L & family_frame$group_dm == 0L, na.rm = TRUE),
      stringsAsFactors = FALSE
    ),
    mediator_status = mediator$status,
    mediator_estimates = mediator$estimates,
    mediator_sensitivity = mediator$sensitivity,
    moderation_h1_status = mod_h1$status,
    moderation_h1_fixed_effects = mod_h1$fixed_effects,
    moderation_h4_status = mod_h4$status,
    moderation_h4_fixed_effects = mod_h4$fixed_effects,
    moderation_h5_stratified_correlations = mod_h5$stratified_correlations,
    beck_interaction_status = beck_int$status,
    beck_interaction_fixed_effects = beck_int$fixed_effects,
    target_summary = data.frame(
      analysis = "antidepressant_pathway_phase2",
      bootstrap_n = bootstrap_n,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXII/58-60)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      mediation_paketi_kullanildi = "FALSE — lavaan tabanli BCa bootstrap fallback",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
