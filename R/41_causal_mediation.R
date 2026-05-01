# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXV/69, 71
# Nedensel Aracilik Sensitivitesi
#
# 69 — Imai-Keele-Tingley (2010) sequential ignorability sensitivity:
#      rho_critical = mediator-outcome residual correlation; ACME yon
#      degisikligi icin minimum confounder gucu. mediation paketi yoksa
#      manuel formul + grid search ile implement edilir.
#
# 71 — c' direct effect triangulation: uc paralel mediation modelinden
#      (basit lavaan, multilevel, conditional process Hayes 14) c' direct
#      effect estimate'lerini birlestiren forest-plot tarzi tablo.
#      CSR §12.1.5 c' direct triangulation'unu resmilestirir.
#
# Skill referanslari: references/mediation-modelleri.md,
#                     references/nedensellik-ve-ps.md

cmed_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

cmed_anne_outcome <- function(s) paste0("embu_p_", s, "_mean")
cmed_cocuk_outcome <- function(s) paste0("embu_c_", s, "_mean")

cmed_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

cmed_scale <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

cmed_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(sprintf("%s missing column(s): %s",
      context, paste(missing_columns, collapse = ", ")), call. = FALSE)
  }
  invisible(TRUE)
}

cmed_ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f) - 1L
    } else if ("grup" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$grup), ignore.case = TRUE))
    }
  }
  df
}

cmed_prepare_paired <- function(df_family_ses, df_long_scored) {
  family_needed <- c("aile_no", paste0("embu_p_", cmed_subscale_outcomes(), "_mean"),
    "ses_latent", "anne_yas")
  long_needed <- c("aile_no", "family_role_f",
    paste0("embu_c_", cmed_subscale_outcomes(), "_mean"))
  cmed_require_columns(df_family_ses, family_needed, "causal mediation family")
  cmed_require_columns(df_long_scored, long_needed, "causal mediation long")

  fam <- cmed_ensure_group_dm(df_family_ses)
  fam <- fam[, c("aile_no", "group_dm", paste0("embu_p_", cmed_subscale_outcomes(), "_mean"),
    "ses_latent", "anne_yas"), drop = FALSE]

  long <- df_long_scored
  long$role_token <- cmed_normalize_role(long$family_role_f)
  indeks <- long[!is.na(long$role_token) & long$role_token == "indeks",
    c("aile_no", paste0("embu_c_", cmed_subscale_outcomes(), "_mean"),
      if ("cocuk_yas" %in% names(long)) "cocuk_yas" else NULL),
    drop = FALSE]
  paired <- merge(fam, indeks, by = "aile_no", all = FALSE)

  paired$ses_latent_z <- cmed_scale(paired$ses_latent)
  paired$anne_yas_z <- cmed_scale(paired$anne_yas)
  if ("cocuk_yas" %in% names(paired)) {
    paired$cocuk_yas_z <- cmed_scale(paired$cocuk_yas)
  }
  paired
}

# ============================================================================
# 69 — Imai-Keele-Tingley Manual Sensitivity
# ============================================================================

# Imai, Keele & Tingley (2010, Psych Methods) sequential ignorability sensitivity:
#   rho = corr(epsilon_M, epsilon_Y | T, X)  (gozlemlenmemis confounder pay)
#   ACME(rho) approx ACME * sqrt(1 - rho^2/(R^2_M * R^2_Y))
#   rho_critical: ACME(rho_critical) = 0 oldugu rho degeri
# Manuel formul (Imai 2010 Lemma 3):
#   rho_critical_approx = a*b / sqrt(var(M_resid) * var(Y_resid))

cmed_imai_keele_one <- function(paired_data, mediator_subscale) {
  # T -> M -> Y (Y = cocuk algisi; M = anne raporu)
  treatment <- "group_dm"
  M_col <- cmed_anne_outcome(mediator_subscale)     # anne EMBU-P
  Y_col <- cmed_cocuk_outcome(mediator_subscale)    # cocuk EMBU-C
  covariates <- c("ses_latent_z", "anne_yas_z")
  if ("cocuk_yas_z" %in% names(paired_data)) {
    covariates <- c(covariates, "cocuk_yas_z")
  }

  needed <- c(treatment, M_col, Y_col, covariates)
  if (any(!needed %in% names(paired_data))) {
    return(list(status = "missing_columns",
      mediator_subscale = mediator_subscale))
  }
  dat <- paired_data[stats::complete.cases(paired_data[, needed]), , drop = FALSE]
  if (nrow(dat) < 30L) {
    return(list(status = "insufficient_n", n = nrow(dat)))
  }

  # Yol a: T -> M
  fa <- stats::lm(stats::as.formula(sprintf("%s ~ %s + %s", M_col, treatment,
    paste(covariates, collapse = " + "))), data = dat)
  a_est <- stats::coef(fa)[[treatment]]
  e_M <- stats::residuals(fa)
  sigma_M <- stats::sd(e_M)

  # Yol b ve c': T + M -> Y
  fb <- stats::lm(stats::as.formula(sprintf("%s ~ %s + %s + %s", Y_col, treatment, M_col,
    paste(covariates, collapse = " + "))), data = dat)
  b_est <- stats::coef(fb)[[M_col]]
  cprime_est <- stats::coef(fb)[[treatment]]
  e_Y <- stats::residuals(fb)
  sigma_Y <- stats::sd(e_Y)

  acme <- a_est * b_est
  total <- cprime_est + acme

  # Manuel rho_critical (Imai 2010 Lemma 3 simplifikasyonu)
  rho_critical <- if (abs(acme) < 1e-10) {
    NA_real_
  } else {
    acme / (sigma_M * sigma_Y)
  }
  rho_critical <- max(-1, min(1, rho_critical))

  # Bootstrap ACME CI ile pseudo-grid sensitivity
  set.seed(20260510L)
  B <- 1000L
  acme_grid_rho <- seq(-0.5, 0.5, by = 0.05)
  # Adjusted ACME(rho): acme - rho * sigma_M * sigma_Y
  adjusted_acme_grid <- acme - acme_grid_rho * sigma_M * sigma_Y

  # Bootstrap orijinal ACME
  boot_acme <- replicate(B, {
    idx <- sample(seq_len(nrow(dat)), nrow(dat), replace = TRUE)
    sub <- dat[idx, , drop = FALSE]
    fa_b <- tryCatch(stats::lm(stats::as.formula(sprintf("%s ~ %s + %s", M_col, treatment,
      paste(covariates, collapse = " + "))), data = sub), error = function(e) NULL)
    fb_b <- tryCatch(stats::lm(stats::as.formula(sprintf("%s ~ %s + %s + %s", Y_col,
      treatment, M_col, paste(covariates, collapse = " + "))), data = sub),
      error = function(e) NULL)
    if (is.null(fa_b) || is.null(fb_b)) return(NA_real_)
    stats::coef(fa_b)[[treatment]] * stats::coef(fb_b)[[M_col]]
  })

  acme_lower <- stats::quantile(boot_acme, 0.025, na.rm = TRUE)
  acme_upper <- stats::quantile(boot_acme, 0.975, na.rm = TRUE)

  list(
    status = "ok",
    mediator_subscale = mediator_subscale,
    n_used = nrow(dat),
    a_path = a_est,
    b_path = b_est,
    cprime_direct = cprime_est,
    total_effect = total,
    acme = acme,
    acme_boot_lower = unname(acme_lower),
    acme_boot_upper = unname(acme_upper),
    sigma_M_resid = sigma_M,
    sigma_Y_resid = sigma_Y,
    rho_critical = rho_critical,
    interpretation = if (is.na(rho_critical)) {
      "indeterminate"
    } else if (abs(rho_critical) < 0.05) {
      "very_fragile_to_unmeasured_confounding"
    } else if (abs(rho_critical) < 0.10) {
      "fragile_to_small_confounders"
    } else if (abs(rho_critical) < 0.20) {
      "moderate_robustness"
    } else {
      "robust_to_large_confounders"
    },
    sensitivity_grid = data.frame(
      mediator_subscale = mediator_subscale,
      rho = acme_grid_rho,
      adjusted_acme = adjusted_acme_grid,
      stringsAsFactors = FALSE
    )
  )
}

cmed_imai_keele_pipeline <- function(paired_data,
                                     outcomes = cmed_subscale_outcomes()) {
  status_rows <- list()
  summary_rows <- list()
  grid_rows <- list()
  for (sub in outcomes) {
    r <- cmed_imai_keele_one(paired_data, sub)
    status_rows[[sub]] <- data.frame(
      mediator_subscale = sub,
      status = r$status,
      n_used = r$n_used %||% NA_integer_,
      stringsAsFactors = FALSE
    )
    if (identical(r$status, "ok")) {
      summary_rows[[sub]] <- data.frame(
        mediator_subscale = sub,
        n_used = r$n_used,
        a_path = r$a_path,
        b_path = r$b_path,
        cprime_direct = r$cprime_direct,
        total_effect = r$total_effect,
        acme = r$acme,
        acme_boot_lower = r$acme_boot_lower,
        acme_boot_upper = r$acme_boot_upper,
        sigma_M_resid = r$sigma_M_resid,
        sigma_Y_resid = r$sigma_Y_resid,
        rho_critical = r$rho_critical,
        interpretation = r$interpretation,
        stringsAsFactors = FALSE
      )
      grid_rows[[sub]] <- r$sensitivity_grid
    }
  }
  list(
    status = if (length(status_rows) > 0L) do.call(rbind, status_rows) else NULL,
    summary = if (length(summary_rows) > 0L) do.call(rbind, summary_rows) else NULL,
    sensitivity_grid = if (length(grid_rows) > 0L) do.call(rbind, grid_rows) else NULL
  )
}

# ============================================================================
# 71 — c' Direct Effect Triangulation (3 model)
# ============================================================================

cmed_cprime_simple <- function(paired_data, mediator_subscale) {
  T_col <- "group_dm"
  M_col <- cmed_anne_outcome(mediator_subscale)
  Y_col <- cmed_cocuk_outcome(mediator_subscale)
  needed <- c(T_col, M_col, Y_col, "ses_latent_z", "anne_yas_z")
  if (any(!needed %in% names(paired_data))) {
    return(NULL)
  }
  dat <- paired_data[stats::complete.cases(paired_data[, needed]), , drop = FALSE]
  fb <- stats::lm(stats::as.formula(sprintf("%s ~ %s + %s + ses_latent_z + anne_yas_z",
    Y_col, T_col, M_col)), data = dat)
  cs <- summary(fb)$coefficients
  data.frame(
    mediator_subscale = mediator_subscale,
    model = "simple_lm",
    cprime_estimate = cs[T_col, "Estimate"],
    cprime_se = cs[T_col, "Std. Error"],
    cprime_ci_lower = cs[T_col, "Estimate"] - 1.96 * cs[T_col, "Std. Error"],
    cprime_ci_upper = cs[T_col, "Estimate"] + 1.96 * cs[T_col, "Std. Error"],
    cprime_p = cs[T_col, "Pr(>|t|)"],
    n_used = stats::nobs(fb),
    stringsAsFactors = FALSE
  )
}

cmed_cprime_multilevel <- function(paired_data_long, mediator_subscale) {
  T_col <- "group_dm"
  M_col <- cmed_anne_outcome(mediator_subscale)
  Y_col <- cmed_cocuk_outcome(mediator_subscale)
  needed <- c(T_col, M_col, Y_col, "ses_latent_z", "anne_yas_z", "aile_no")
  if (any(!needed %in% names(paired_data_long))) {
    return(NULL)
  }
  if (!requireNamespace("lme4", quietly = TRUE)) {
    return(NULL)
  }
  dat <- paired_data_long[stats::complete.cases(paired_data_long[, needed]), , drop = FALSE]
  formula <- stats::as.formula(sprintf(
    "%s ~ %s + %s + ses_latent_z + anne_yas_z + (1 | aile_no)",
    Y_col, T_col, M_col
  ))
  fit <- tryCatch(lme4::lmer(formula, data = dat), error = function(e) e)
  if (inherits(fit, "error")) return(NULL)
  cs <- summary(fit)$coefficients
  cprime_idx <- which(rownames(cs) == T_col)
  if (length(cprime_idx) == 0L) return(NULL)
  est <- cs[cprime_idx, 1L]
  se <- cs[cprime_idx, 2L]
  data.frame(
    mediator_subscale = mediator_subscale,
    model = "multilevel_lmer",
    cprime_estimate = est,
    cprime_se = se,
    cprime_ci_lower = est - 1.96 * se,
    cprime_ci_upper = est + 1.96 * se,
    cprime_p = 2 * (1 - stats::pnorm(abs(est / se))),
    n_used = stats::nobs(fit),
    stringsAsFactors = FALSE
  )
}

cmed_cprime_hayes14 <- function(paired_data, mediator_subscale,
                                moderator_col = "ses_latent_z") {
  # Hayes Model 14: Y = c'*T + b1*M + b2*W + b3*M*W + covariates
  T_col <- "group_dm"
  M_col <- cmed_anne_outcome(mediator_subscale)
  Y_col <- cmed_cocuk_outcome(mediator_subscale)
  needed <- c(T_col, M_col, Y_col, moderator_col, "anne_yas_z")
  if (any(!needed %in% names(paired_data))) {
    return(NULL)
  }
  dat <- paired_data[stats::complete.cases(paired_data[, needed]), , drop = FALSE]
  formula <- stats::as.formula(sprintf(
    "%s ~ %s + %s * %s + anne_yas_z",
    Y_col, T_col, M_col, moderator_col
  ))
  fit <- stats::lm(formula, data = dat)
  cs <- summary(fit)$coefficients
  cprime_idx <- which(rownames(cs) == T_col)
  if (length(cprime_idx) == 0L) return(NULL)
  data.frame(
    mediator_subscale = mediator_subscale,
    model = "hayes14_conditional",
    cprime_estimate = cs[cprime_idx, "Estimate"],
    cprime_se = cs[cprime_idx, "Std. Error"],
    cprime_ci_lower = cs[cprime_idx, "Estimate"] - 1.96 * cs[cprime_idx, "Std. Error"],
    cprime_ci_upper = cs[cprime_idx, "Estimate"] + 1.96 * cs[cprime_idx, "Std. Error"],
    cprime_p = cs[cprime_idx, "Pr(>|t|)"],
    n_used = stats::nobs(fit),
    stringsAsFactors = FALSE
  )
}

cmed_cprime_triangulation <- function(paired_data, paired_long_data,
                                      outcomes = cmed_subscale_outcomes()) {
  rows <- list()
  for (sub in outcomes) {
    s_simple <- cmed_cprime_simple(paired_data, sub)
    if (!is.null(s_simple)) rows[[paste(sub, "simple", sep = "_")]] <- s_simple
    s_ml <- cmed_cprime_multilevel(paired_long_data, sub)
    if (!is.null(s_ml)) rows[[paste(sub, "ml", sep = "_")]] <- s_ml
    s_h14 <- cmed_cprime_hayes14(paired_data, sub)
    if (!is.null(s_h14)) rows[[paste(sub, "h14", sep = "_")]] <- s_h14
  }
  if (length(rows) == 0L) return(NULL)
  do.call(rbind, rows)
}

# ============================================================================
# Pipeline
# ============================================================================

run_causal_mediation_pipeline <- function(df_family_ses, df_long_scored,
                                          outcomes = cmed_subscale_outcomes()) {
  paired <- cmed_prepare_paired(df_family_ses, df_long_scored)

  # Multilevel icin long format (indeks + kardes)
  long_full <- df_long_scored
  long_full$role_token <- cmed_normalize_role(long_full$family_role_f)
  long_full <- long_full[!is.na(long_full$role_token), , drop = FALSE]
  fam_join <- cmed_ensure_group_dm(df_family_ses)
  fam_join <- fam_join[, c("aile_no", "group_dm",
    paste0("embu_p_", outcomes, "_mean"), "ses_latent", "anne_yas"), drop = FALSE]
  fam_join$ses_latent_z <- cmed_scale(fam_join$ses_latent)
  fam_join$anne_yas_z <- cmed_scale(fam_join$anne_yas)
  paired_long <- merge(long_full, fam_join, by = "aile_no", all = FALSE)

  imai_result <- cmed_imai_keele_pipeline(paired, outcomes = outcomes)
  cprime_table <- cmed_cprime_triangulation(paired, paired_long, outcomes = outcomes)

  list(
    n_paired = nrow(paired),
    n_paired_long = nrow(paired_long),
    imai_status = imai_result$status,
    imai_summary = imai_result$summary,
    imai_sensitivity_grid = imai_result$sensitivity_grid,
    cprime_triangulation = cprime_table,
    target_summary = data.frame(
      analysis = "causal_mediation_phase2",
      n_paired = nrow(paired),
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXV/69, 71)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      mediation_paketi_kullanildi = "FALSE — manuel Imai-Keele formul fallback",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
