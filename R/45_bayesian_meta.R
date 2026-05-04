# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXVIII/80, 81, 82
# Meta-Analitik Birlestirme
#
# 80 — Bayesian meta-analytic pooling: Pinquart 2013 (chronic illness x parenting,
#      g = -0.16), Pinquart 2018 (parenting stress meta), Lovejoy 2000 (anne
#      depresyon x parenting), Vermaes 2012 (chronic illness siblings, d = 0.17)
#      ve bu calismanin H1 reddetme estimate'i ile brms random-effects pooling.
#
# 81 — Posterior predictive replication (Gelman 2013): brms H1 modelinden
#      posterior predictive draws cikar; simulated dataset uzerinde test
#      istatistigi dagilim; observed t-stat quantile pozisyonu.
#
# 82 — Empirical Bayes shrinkage: lme4::ranef cocuk-icin aile-duzeyi rastgele
#      kesisimleri shrunk estimate; outlier aile sayisi DM vs Kontrol.
#
# Skill referanslari: references/bayesci-paralel-hat.md,
#                     references/multilevel-aile-yapisi.md

meta_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

meta_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

meta_scale <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

meta_ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f) - 1L
    } else if ("grup" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$grup), ignore.case = TRUE))
    }
  }
  df
}

# ============================================================================
# 80 — Bayesian Meta-Analytic Pooling
# ============================================================================

meta_prior_studies <- function() {
  data.frame(
    study = c(
      "Pinquart_2013_chronic_illness_parenting",
      "Pinquart_2018_parenting_stress_chronic",
      "Lovejoy_2000_maternal_depression_parenting",
      "Vermaes_2012_chronic_illness_siblings"
    ),
    domain = c("chronic_illness_parenting", "parenting_stress",
      "depression_parenting", "siblings_internalizing"),
    yi = c(-0.16, 0.20, 0.40, 0.17),
    vi = c(0.0064, 0.0081, 0.0144, 0.0100),
    n_studies = c(325L, 56L, 46L, 56L),
    weight_label = c("meta_chronic", "meta_stress",
      "meta_depression", "meta_siblings"),
    stringsAsFactors = FALSE
  )
}

meta_estimate_this_study <- function(df_family_ses, df_long_scored,
                                       outcome_subscale = "reddetme") {
  outcome <- paste0("embu_c_", outcome_subscale, "_mean")
  needed_long <- c("aile_no", "family_role_f", "cocuk_yas", outcome)
  needed_fam <- c("aile_no", "ses_latent")
  fam <- meta_ensure_group_dm(df_family_ses)
  fam_keep <- intersect(c("aile_no", "group_dm", "ses_latent", "anne_yas"), names(fam))
  fam <- fam[, fam_keep, drop = FALSE]
  fam$ses_latent_z <- meta_scale(fam$ses_latent)

  long <- df_long_scored
  long$role_token <- meta_normalize_role(long$family_role_f)
  long <- long[!is.na(long$role_token), , drop = FALSE]
  long$cocuk_yas_z <- meta_scale(long$cocuk_yas)

  paired <- merge(long, fam, by = "aile_no", all.x = TRUE)

  if (!requireNamespace("lme4", quietly = TRUE)) {
    return(list(yi = NA_real_, se = NA_real_, n = NA_integer_,
      study_label = "T1DM_EBEVEYN_2026", domain = "this_study"))
  }
  formula <- stats::as.formula(sprintf(
    "%s ~ group_dm + cocuk_yas_z + ses_latent_z + (1 | aile_no)", outcome
  ))
  fit <- tryCatch(
    suppressWarnings(suppressMessages(lme4::lmer(formula, data = paired))),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(yi = NA_real_, se = NA_real_, n = NA_integer_,
      study_label = "T1DM_EBEVEYN_2026", domain = "this_study",
      error = conditionMessage(fit)))
  }
  cs <- summary(fit)$coefficients
  if (!"group_dm" %in% rownames(cs)) {
    return(list(yi = NA_real_, se = NA_real_, n = stats::nobs(fit),
      study_label = "T1DM_EBEVEYN_2026", domain = "this_study",
      error = "predictor_dropped"))
  }
  yi <- cs["group_dm", "Estimate"]
  se <- cs["group_dm", "Std. Error"]
  list(
    yi = yi,
    se = se,
    vi = se^2,
    n = stats::nobs(fit),
    study_label = sprintf("T1DM_EBEVEYN_2026_%s", outcome_subscale),
    domain = "this_study",
    weight_label = sprintf("this_%s", outcome_subscale)
  )
}

meta_bayesian_pooling <- function(combined_studies, chains = 2L, iter = 2000L,
                                  group_focus = "this_study") {
  if (!requireNamespace("brms", quietly = TRUE)) {
    return(list(status = "brms_unavailable"))
  }
  ok <- combined_studies[stats::complete.cases(combined_studies[,
    c("yi", "vi"), drop = FALSE]), , drop = FALSE]
  if (nrow(ok) < 2L) {
    return(list(status = "insufficient_studies"))
  }
  ok$se <- sqrt(ok$vi)
  ok$study_id <- factor(ok$study_label %||% ok$study, levels = unique(ok$study_label %||% ok$study))

  fit <- tryCatch(
    suppressWarnings(brms::brm(
      formula = brms::bf(yi | brms::se(se) ~ 1 + (1 | study_id)),
      data = ok,
      prior = c(
        brms::prior(normal(0, 0.5), class = "Intercept"),
        brms::prior(student_t(3, 0, 0.3), class = "sd")
      ),
      chains = chains,
      iter = iter,
      warmup = floor(iter / 2),
      refresh = 0,
      silent = 2,
      seed = 20260516
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    # Metafor REML fallback (h5ext deseni)
    if (requireNamespace("metafor", quietly = TRUE)) {
      meta_fit <- tryCatch(
        metafor::rma(yi = ok$yi, sei = ok$se, method = "REML"),
        error = function(e) e
      )
      if (!inherits(meta_fit, "error")) {
        return(list(
          status = "ok",
          summary = data.frame(
            group_focus = group_focus,
            n_studies = nrow(ok),
            pooled_mean = as.numeric(meta_fit$beta),
            pooled_lower = meta_fit$ci.lb,
            pooled_upper = meta_fit$ci.ub,
            tau = sqrt(meta_fit$tau2),
            tau_lower = NA_real_,
            tau_upper = NA_real_,
            rhat_max = NA_real_,
            method = "metafor_REML_fallback",
            stringsAsFactors = FALSE
          ),
          shrunk_estimates = data.frame(
            study_id = ok$study_label,
            shrunk_intercept = ok$yi - as.numeric(meta_fit$beta),
            shrunk_lower = NA_real_,
            shrunk_upper = NA_real_,
            shrunk_full = ok$yi,
            stringsAsFactors = FALSE
          )
        ))
      }
    }
    return(list(status = "fit_error", error_message = conditionMessage(fit)))
  }
  post_b <- as.matrix(fit, variable = "b_Intercept")
  post_sd <- as.matrix(fit, variable = "sd_study_id__Intercept")

  shrunk_estimates <- tryCatch(
    {
      ranef <- brms::ranef(fit)$study_id
      ranef_df <- data.frame(
        study_id = rownames(ranef[, , 1L]),
        shrunk_intercept = ranef[, "Estimate", 1L],
        shrunk_lower = ranef[, "Q2.5", 1L],
        shrunk_upper = ranef[, "Q97.5", 1L],
        stringsAsFactors = FALSE
      )
      pooled_b <- stats::median(post_b)
      ranef_df$shrunk_full <- ranef_df$shrunk_intercept + pooled_b
      ranef_df
    },
    error = function(e) NULL
  )

  list(
    status = "ok",
    summary = data.frame(
      group_focus = group_focus,
      n_studies = nrow(ok),
      pooled_mean = unname(stats::median(post_b)),
      pooled_lower = unname(stats::quantile(post_b, 0.025)),
      pooled_upper = unname(stats::quantile(post_b, 0.975)),
      tau = unname(stats::median(post_sd)),
      tau_lower = unname(stats::quantile(post_sd, 0.025)),
      tau_upper = unname(stats::quantile(post_sd, 0.975)),
      rhat_max = max(brms::rhat(fit), na.rm = TRUE),
      method = "brms_random_effects",
      stringsAsFactors = FALSE
    ),
    shrunk_estimates = shrunk_estimates
  )
}

# ============================================================================
# 81 — Posterior Predictive Replication (Gelman 2013)
# ============================================================================

meta_ppc_replication <- function(df_family_ses, df_long_scored,
                                  outcome_subscale = "reddetme",
                                  chains = 2L, iter = 2000L,
                                  n_replicates = 1000L) {
  if (!requireNamespace("brms", quietly = TRUE)) {
    return(list(status = "brms_unavailable"))
  }
  outcome <- paste0("embu_c_", outcome_subscale, "_mean")
  needed_long <- c("aile_no", "family_role_f", "cocuk_yas", outcome)

  fam <- meta_ensure_group_dm(df_family_ses)
  fam_keep <- intersect(c("aile_no", "group_dm", "ses_latent"), names(fam))
  fam <- fam[, fam_keep, drop = FALSE]
  fam$ses_latent_z <- meta_scale(fam$ses_latent)

  long <- df_long_scored
  long$role_token <- meta_normalize_role(long$family_role_f)
  long <- long[!is.na(long$role_token), , drop = FALSE]
  long$cocuk_yas_z <- meta_scale(long$cocuk_yas)

  paired <- merge(long, fam, by = "aile_no", all.x = TRUE)
  paired <- paired[stats::complete.cases(paired[, c(outcome, "group_dm", "cocuk_yas_z",
    "ses_latent_z", "aile_no"), drop = FALSE]), , drop = FALSE]

  formula <- brms::bf(stats::as.formula(sprintf(
    "%s ~ group_dm + cocuk_yas_z + ses_latent_z + (1 | aile_no)", outcome
  )))
  fit <- tryCatch(
    suppressWarnings(brms::brm(
      formula = formula,
      data = paired,
      family = gaussian(),
      chains = chains,
      iter = iter,
      warmup = floor(iter / 2),
      refresh = 0,
      silent = 2,
      seed = 20260517
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", error_message = conditionMessage(fit)))
  }

  observed_t <- {
    t_fit <- stats::lm(stats::as.formula(sprintf("%s ~ group_dm + cocuk_yas_z + ses_latent_z",
      outcome)), data = paired)
    cs <- summary(t_fit)$coefficients
    if ("group_dm" %in% rownames(cs)) cs["group_dm", "t value"] else NA_real_
  }

  pp <- brms::posterior_predict(fit, ndraws = n_replicates)
  rep_t_vals <- numeric(nrow(pp))
  for (k in seq_len(nrow(pp))) {
    rep_y <- pp[k, ]
    rep_data <- paired
    rep_data[[outcome]] <- rep_y
    fit_rep <- tryCatch(
      stats::lm(stats::as.formula(sprintf("%s ~ group_dm + cocuk_yas_z + ses_latent_z",
        outcome)), data = rep_data),
      error = function(e) NULL
    )
    if (is.null(fit_rep)) {
      rep_t_vals[k] <- NA_real_
      next
    }
    cs <- summary(fit_rep)$coefficients
    rep_t_vals[k] <- if ("group_dm" %in% rownames(cs)) cs["group_dm", "t value"] else NA_real_
  }
  rep_t_vals <- rep_t_vals[!is.na(rep_t_vals)]
  if (length(rep_t_vals) == 0L) {
    return(list(status = "no_valid_replicates"))
  }
  quantile_obs <- mean(rep_t_vals >= observed_t)

  list(
    status = "ok",
    outcome_subscale = outcome_subscale,
    summary = data.frame(
      outcome_subscale = outcome_subscale,
      observed_t = observed_t,
      n_replicates_used = length(rep_t_vals),
      replicate_t_mean = mean(rep_t_vals),
      replicate_t_sd = stats::sd(rep_t_vals),
      replicate_t_2_5 = stats::quantile(rep_t_vals, 0.025),
      replicate_t_97_5 = stats::quantile(rep_t_vals, 0.975),
      ppc_quantile = quantile_obs,
      ppc_decision = if (quantile_obs > 0.95 || quantile_obs < 0.05) {
        "ppc_violation_systematic_misfit"
      } else {
        "ppc_consistent"
      },
      n_used = stats::nobs(fit),
      rhat_max = max(brms::rhat(fit), na.rm = TRUE),
      stringsAsFactors = FALSE
    )
  )
}

# ============================================================================
# 82 — Empirical Bayes Shrinkage (Multilevel Random Intercepts)
# ============================================================================

meta_empirical_bayes_shrinkage <- function(df_family_ses, df_long_scored,
                                            outcome_subscale = "reddetme") {
  if (!requireNamespace("lme4", quietly = TRUE)) {
    return(list(status = "lme4_unavailable"))
  }
  outcome <- paste0("embu_c_", outcome_subscale, "_mean")

  fam <- meta_ensure_group_dm(df_family_ses)
  fam_keep <- intersect(c("aile_no", "group_dm", "ses_latent"), names(fam))
  fam <- fam[, fam_keep, drop = FALSE]
  fam$ses_latent_z <- meta_scale(fam$ses_latent)

  long <- df_long_scored
  long$role_token <- meta_normalize_role(long$family_role_f)
  long <- long[!is.na(long$role_token), , drop = FALSE]
  long$cocuk_yas_z <- meta_scale(long$cocuk_yas)

  paired <- merge(long, fam, by = "aile_no", all.x = TRUE)
  paired <- paired[stats::complete.cases(paired[, c(outcome, "group_dm",
    "cocuk_yas_z", "ses_latent_z", "aile_no"), drop = FALSE]), , drop = FALSE]

  formula <- stats::as.formula(sprintf(
    "%s ~ group_dm + cocuk_yas_z + ses_latent_z + (1 | aile_no)", outcome
  ))
  fit <- tryCatch(
    suppressWarnings(suppressMessages(lme4::lmer(formula, data = paired))),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", error_message = conditionMessage(fit)))
  }
  ranef_obj <- lme4::ranef(fit, condVar = TRUE)$aile_no
  shrunk <- data.frame(
    aile_no = as.integer(rownames(ranef_obj)),
    shrunk_intercept = ranef_obj[, 1L],
    stringsAsFactors = FALSE
  )
  postvar <- attr(ranef_obj, "postVar")
  shrunk$shrunk_se <- sqrt(as.vector(postvar))
  shrunk$ci_lower <- shrunk$shrunk_intercept - 1.96 * shrunk$shrunk_se
  shrunk$ci_upper <- shrunk$shrunk_intercept + 1.96 * shrunk$shrunk_se
  shrunk$is_outlier <- (shrunk$ci_lower > 0 | shrunk$ci_upper < 0)

  group_lookup <- setNames(fam$group_dm, fam$aile_no)
  shrunk$group_dm <- group_lookup[as.character(shrunk$aile_no)]
  shrunk$group_label <- ifelse(shrunk$group_dm == 1L, "DM",
    ifelse(shrunk$group_dm == 0L, "Kontrol", NA_character_))

  outlier_summary <- data.frame(
    outcome_subscale = outcome_subscale,
    n_total_families = nrow(shrunk),
    n_outliers_total = sum(shrunk$is_outlier, na.rm = TRUE),
    n_outliers_dm = sum(shrunk$is_outlier & shrunk$group_label == "DM", na.rm = TRUE),
    n_outliers_kontrol = sum(shrunk$is_outlier & shrunk$group_label == "Kontrol", na.rm = TRUE),
    expected_outliers_random = round(0.05 * nrow(shrunk)),
    decision = if (sum(shrunk$is_outlier, na.rm = TRUE) >
        2 * round(0.05 * nrow(shrunk))) {
      "elevated_heterogeneity"
    } else {
      "expected_random_outlier_rate"
    },
    stringsAsFactors = FALSE
  )

  shrunk$outcome_subscale <- outcome_subscale
  list(
    status = "ok",
    shrunk_estimates = shrunk,
    outlier_summary = outlier_summary,
    n_used = stats::nobs(fit)
  )
}

# ============================================================================
# Pipeline
# ============================================================================

run_bayesian_meta_pipeline <- function(df_family_ses, df_long_scored,
                                        outcomes = "reddetme",
                                        brms_chains = 2L,
                                        brms_iter = 2000L,
                                        ppc_replicates = 1000L) {
  # 80 — Meta-pooling
  prior_studies <- meta_prior_studies()
  meta_rows <- lapply(outcomes, function(s) {
    this_est <- meta_estimate_this_study(df_family_ses, df_long_scored,
      outcome_subscale = s)
    if (is.na(this_est$yi)) return(NULL)
    data.frame(
      study_label = this_est$study_label,
      domain = this_est$domain,
      yi = this_est$yi,
      vi = this_est$vi,
      n_studies = NA_integer_,
      weight_label = this_est$weight_label,
      stringsAsFactors = FALSE
    )
  })
  this_study_estimates <- if (length(meta_rows) > 0L) {
    do.call(rbind, Filter(Negate(is.null), meta_rows))
  } else NULL

  if (!is.null(this_study_estimates)) {
    combined <- rbind(
      data.frame(
        study_label = prior_studies$study,
        domain = prior_studies$domain,
        yi = prior_studies$yi,
        vi = prior_studies$vi,
        n_studies = prior_studies$n_studies,
        weight_label = prior_studies$weight_label,
        stringsAsFactors = FALSE
      ),
      this_study_estimates
    )
  } else {
    combined <- data.frame(
      study_label = prior_studies$study,
      domain = prior_studies$domain,
      yi = prior_studies$yi,
      vi = prior_studies$vi,
      n_studies = prior_studies$n_studies,
      weight_label = prior_studies$weight_label,
      stringsAsFactors = FALSE
    )
  }

  pooling <- meta_bayesian_pooling(combined, chains = brms_chains,
    iter = brms_iter)

  # 81 — PPC replication (focus = first outcome)
  ppc_results <- list()
  for (s in outcomes) {
    ppc_results[[s]] <- meta_ppc_replication(df_family_ses, df_long_scored,
      outcome_subscale = s, chains = brms_chains, iter = brms_iter,
      n_replicates = ppc_replicates)
  }
  ppc_summary <- do.call(rbind, Filter(Negate(is.null),
    lapply(ppc_results, function(x) x$summary)))

  # 82 — EB shrinkage
  eb_results <- list()
  outlier_summary_rows <- list()
  for (s in outcomes) {
    eb <- meta_empirical_bayes_shrinkage(df_family_ses, df_long_scored,
      outcome_subscale = s)
    if (identical(eb$status, "ok")) {
      eb_results[[s]] <- eb$shrunk_estimates
      outlier_summary_rows[[s]] <- eb$outlier_summary
    }
  }
  eb_shrunk_table <- if (length(eb_results) > 0L) do.call(rbind, eb_results) else NULL
  eb_outlier_summary <- if (length(outlier_summary_rows) > 0L) {
    do.call(rbind, outlier_summary_rows)
  } else NULL

  list(
    combined_studies = combined,
    pooling_status = data.frame(
      status = pooling$status,
      stringsAsFactors = FALSE
    ),
    pooling_summary = pooling$summary,
    pooling_shrunk_estimates = pooling$shrunk_estimates,
    ppc_summary = ppc_summary,
    eb_shrunk_estimates = eb_shrunk_table,
    eb_outlier_summary = eb_outlier_summary,
    target_summary = data.frame(
      analysis = "bayesian_meta_phase2",
      n_outcomes = length(outcomes),
      brms_chains = brms_chains,
      brms_iter = brms_iter,
      ppc_replicates = ppc_replicates,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXVIII/80, 81, 82)",
      reference_doc = "04-sap-faz2-posthoc.md",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
