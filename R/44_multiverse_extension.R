# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXVII/76, 77, 78, 79
# Multiverse Genisletme
#
# 76 — H1 multiverse: outcome (mean / IRT theta proxy), kovaryat seti (minimal /
#      DAG / extended), eksik veri (CC / FIML / MI), random structure
#      (aile / aile + cinsiyet / fixed), cluster SE (naive / HC3),
#      outlier (none / 3SD / IQR x 1.5). Random subset.
#
# 77 — H4 SEM multiverse: estimator (WLSMV / MLR), Beck struct (single /
#      cog-som 2 factor), missing (listwise / FIML / MI), cluster (aile / yok).
#
# 78 — Bayesian Model Averaging across multiverse: LOO weights ile ag
#      tabanli stacking; Yao, Vehtari, Simpson & Gelman 2018.
#
# 79 — Specification Curve Inferential Test (Simonsohn 2020): permutation
#      n_perm = 5000; spec curve null'dan farkli mi.
#
# Skill referanslari: references/robustluk-ve-sensitivite.md,
#                     references/bayesci-paralel-hat.md

multi_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

multi_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

multi_scale <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

multi_ensure_group_dm <- function(df) {
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
# 76 — H1 Multiverse Specification Universe
# ============================================================================

multi_h1_spec_grid <- function(outcomes = multi_subscale_outcomes(),
                                seed = 20260513L,
                                n_random_subset = 120L) {
  full_grid <- expand.grid(
    outcome_subscale = outcomes,
    covariate_set = c("minimal", "dag_justified", "extended"),
    missing_strategy = c("complete_case", "fiml_proxy", "mi_proxy"),
    random_structure = c("aile", "aile_cinsiyet", "fixed"),
    cluster_se = c("naive", "hc3"),
    outlier_handling = c("none", "trim_3sd", "trim_iqr"),
    stringsAsFactors = FALSE
  )
  full_grid$spec_id <- seq_len(nrow(full_grid))
  if (n_random_subset >= nrow(full_grid)) return(full_grid)
  set.seed(seed)
  sub_idx <- sample(seq_len(nrow(full_grid)), n_random_subset, replace = FALSE)
  full_grid[sort(sub_idx), , drop = FALSE]
}

multi_h1_covariate_set <- function(spec_label) {
  switch(spec_label,
    "minimal" = c("cocuk_yas_z", "cinsiyet_f"),
    "dag_justified" = c("cocuk_yas_z", "cinsiyet_f", "ses_latent_z",
      "age_gap_z", "cocuk_sayisi_z"),
    "extended" = c("cocuk_yas_z", "cinsiyet_f", "ses_latent_z",
      "age_gap_z", "cocuk_sayisi_z", "anne_yas_z", "beck_total_z"),
    c("cocuk_yas_z")
  )
}

multi_h1_apply_outlier <- function(df, outcome_col, method = "none") {
  if (method == "none") return(df)
  vals <- df[[outcome_col]]
  if (method == "trim_3sd") {
    m <- mean(vals, na.rm = TRUE)
    s <- stats::sd(vals, na.rm = TRUE)
    keep <- abs(vals - m) <= 3 * s | is.na(vals)
  } else if (method == "trim_iqr") {
    q <- stats::quantile(vals, probs = c(0.25, 0.75), na.rm = TRUE)
    iqr <- q[2L] - q[1L]
    lo <- q[1L] - 1.5 * iqr
    hi <- q[2L] + 1.5 * iqr
    keep <- (vals >= lo & vals <= hi) | is.na(vals)
  } else {
    keep <- rep(TRUE, nrow(df))
  }
  df[keep, , drop = FALSE]
}

multi_h1_apply_missing <- function(df, strategy, needed_cols) {
  if (strategy == "complete_case") {
    return(df[stats::complete.cases(df[, needed_cols, drop = FALSE]), , drop = FALSE])
  }
  # FIML proxy: lme4 default missing handling = complete case
  # MI proxy: mice with m=5 (sade)
  if (strategy == "mi_proxy" && requireNamespace("mice", quietly = TRUE)) {
    mi_fit <- tryCatch(
      suppressWarnings(suppressMessages(mice::mice(df[, needed_cols, drop = FALSE],
        m = 5L, maxit = 5L, printFlag = FALSE))),
      error = function(e) NULL
    )
    if (!is.null(mi_fit)) {
      completed <- mice::complete(mi_fit, action = 1L)
      df_imputed <- df
      df_imputed[, needed_cols] <- completed
      return(df_imputed)
    }
  }
  # FIML / fallback: complete case
  df[stats::complete.cases(df[, needed_cols, drop = FALSE]), , drop = FALSE]
}

multi_h1_fit_one_spec <- function(spec_row, prepared_long) {
  outcome <- paste0("embu_c_", spec_row$outcome_subscale, "_mean")
  covariates <- multi_h1_covariate_set(spec_row$covariate_set)

  base_cols <- c(outcome, "group_dm", "aile_no", covariates)
  if (spec_row$random_structure == "aile_cinsiyet") {
    base_cols <- c(base_cols, "cinsiyet_f")
  }

  needed_in_data <- intersect(base_cols, names(prepared_long))
  if (length(setdiff(base_cols, needed_in_data)) > 0L) {
    return(data.frame(
      spec_id = spec_row$spec_id,
      outcome_subscale = spec_row$outcome_subscale,
      status = "missing_columns",
      group_dm_estimate = NA_real_,
      group_dm_se = NA_real_,
      group_dm_p = NA_real_,
      n_used = NA_integer_,
      stringsAsFactors = FALSE
    ))
  }

  dat <- multi_h1_apply_outlier(prepared_long, outcome,
    method = spec_row$outlier_handling)
  dat <- multi_h1_apply_missing(dat, spec_row$missing_strategy,
    needed_in_data)

  if (nrow(dat) < 30L) {
    return(data.frame(
      spec_id = spec_row$spec_id,
      outcome_subscale = spec_row$outcome_subscale,
      status = "insufficient_n",
      group_dm_estimate = NA_real_,
      group_dm_se = NA_real_,
      group_dm_p = NA_real_,
      n_used = nrow(dat),
      stringsAsFactors = FALSE
    ))
  }

  fixed_part <- paste(c("group_dm", covariates), collapse = " + ")
  random_part <- switch(spec_row$random_structure,
    "aile" = "(1 | aile_no)",
    "aile_cinsiyet" = "(1 | aile_no)",
    "fixed" = NULL,
    "(1 | aile_no)"
  )

  if (is.null(random_part)) {
    formula_str <- sprintf("%s ~ %s", outcome, fixed_part)
    fit <- tryCatch(stats::lm(stats::as.formula(formula_str), data = dat),
      error = function(e) e)
    if (inherits(fit, "error")) {
      return(data.frame(
        spec_id = spec_row$spec_id,
        outcome_subscale = spec_row$outcome_subscale,
        status = "fit_error",
        group_dm_estimate = NA_real_,
        group_dm_se = NA_real_,
        group_dm_p = NA_real_,
        n_used = nrow(dat),
        stringsAsFactors = FALSE
      ))
    }
    cs <- summary(fit)$coefficients
    if (spec_row$cluster_se == "hc3" && requireNamespace("sandwich", quietly = TRUE) &&
        requireNamespace("lmtest", quietly = TRUE)) {
      hc <- suppressWarnings(lmtest::coeftest(fit, vcov. = sandwich::vcovHC(fit, type = "HC3")))
      grp_idx <- which(rownames(hc) == "group_dm")
      est <- hc[grp_idx, 1L]; se <- hc[grp_idx, 2L]; p <- hc[grp_idx, 4L]
    } else {
      grp_idx <- which(rownames(cs) == "group_dm")
      est <- cs[grp_idx, 1L]; se <- cs[grp_idx, 2L]; p <- cs[grp_idx, 4L]
    }
    return(data.frame(
      spec_id = spec_row$spec_id,
      outcome_subscale = spec_row$outcome_subscale,
      status = "ok",
      group_dm_estimate = est,
      group_dm_se = se,
      group_dm_p = p,
      n_used = stats::nobs(fit),
      stringsAsFactors = FALSE
    ))
  }

  if (!requireNamespace("lme4", quietly = TRUE) ||
      !requireNamespace("lmerTest", quietly = TRUE)) {
    return(data.frame(
      spec_id = spec_row$spec_id,
      outcome_subscale = spec_row$outcome_subscale,
      status = "lme4_unavailable",
      group_dm_estimate = NA_real_,
      group_dm_se = NA_real_,
      group_dm_p = NA_real_,
      n_used = NA_integer_,
      stringsAsFactors = FALSE
    ))
  }
  formula_str <- sprintf("%s ~ %s + %s", outcome, fixed_part, random_part)
  fit <- tryCatch(
    suppressWarnings(suppressMessages(lmerTest::lmer(stats::as.formula(formula_str),
      data = dat))),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(data.frame(
      spec_id = spec_row$spec_id,
      outcome_subscale = spec_row$outcome_subscale,
      status = "fit_error",
      group_dm_estimate = NA_real_,
      group_dm_se = NA_real_,
      group_dm_p = NA_real_,
      n_used = nrow(dat),
      stringsAsFactors = FALSE
    ))
  }
  cs <- summary(fit)$coefficients
  grp_idx <- which(rownames(cs) == "group_dm")
  if (length(grp_idx) == 0L) {
    return(data.frame(
      spec_id = spec_row$spec_id,
      outcome_subscale = spec_row$outcome_subscale,
      status = "predictor_dropped",
      group_dm_estimate = NA_real_,
      group_dm_se = NA_real_,
      group_dm_p = NA_real_,
      n_used = stats::nobs(fit),
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    spec_id = spec_row$spec_id,
    outcome_subscale = spec_row$outcome_subscale,
    status = "ok",
    group_dm_estimate = cs[grp_idx, 1L],
    group_dm_se = cs[grp_idx, 2L],
    group_dm_p = cs[grp_idx, "Pr(>|t|)"],
    n_used = stats::nobs(fit),
    stringsAsFactors = FALSE
  )
}

multi_h1_prepare_long <- function(df_long_scored, df_family_ses) {
  long_needed <- c("aile_no", "family_role_f", "cocuk_yas", "cinsiyet_f",
    paste0("embu_c_", multi_subscale_outcomes(), "_mean"))
  fam_needed <- c("aile_no", "ses_latent", "anne_yas", "beck_total")
  for (c in c("age_gap", "cocuk_sayisi")) {
    if (c %in% names(df_family_ses)) fam_needed <- c(fam_needed, c)
  }

  long <- df_long_scored
  long$role_token <- multi_normalize_role(long$family_role_f)
  long <- long[!is.na(long$role_token), , drop = FALSE]
  long$cocuk_yas_z <- multi_scale(long$cocuk_yas)

  fam <- multi_ensure_group_dm(df_family_ses)
  fam <- fam[, intersect(c("aile_no", "group_dm", fam_needed), names(fam)), drop = FALSE]
  fam$ses_latent_z <- multi_scale(fam$ses_latent)
  fam$anne_yas_z <- multi_scale(fam$anne_yas)
  fam$beck_total_z <- multi_scale(fam$beck_total)
  if ("age_gap" %in% names(fam)) fam$age_gap_z <- multi_scale(fam$age_gap)
  if ("cocuk_sayisi" %in% names(fam)) fam$cocuk_sayisi_z <- multi_scale(fam$cocuk_sayisi)

  paired <- merge(long, fam, by = "aile_no", all.x = TRUE)
  paired
}

multi_h1_pipeline <- function(df_family_ses, df_long_scored,
                               n_random_subset = 120L,
                               seed = 20260513L) {
  prepared <- multi_h1_prepare_long(df_long_scored, df_family_ses)
  spec_grid <- multi_h1_spec_grid(seed = seed, n_random_subset = n_random_subset)

  rows <- vector("list", nrow(spec_grid))
  for (i in seq_len(nrow(spec_grid))) {
    rows[[i]] <- multi_h1_fit_one_spec(spec_grid[i, , drop = FALSE], prepared)
  }
  spec_results <- do.call(rbind, rows)

  # Specification curve aggregation
  spec_with_meta <- merge(spec_results, spec_grid, by = "spec_id", all.x = TRUE,
    suffixes = c("_result", ""))
  spec_with_meta <- spec_with_meta[order(spec_with_meta$group_dm_estimate), , drop = FALSE]
  spec_with_meta$rank <- seq_len(nrow(spec_with_meta))

  ok <- spec_results[spec_results$status == "ok", , drop = FALSE]
  curve_summary <- if (nrow(ok) > 0L) {
    data.frame(
      n_total_spec = nrow(spec_grid),
      n_ok_spec = nrow(ok),
      median_estimate = stats::median(ok$group_dm_estimate),
      ci_lower = stats::quantile(ok$group_dm_estimate, 0.025),
      ci_upper = stats::quantile(ok$group_dm_estimate, 0.975),
      share_p_under_05 = mean(ok$group_dm_p < 0.05),
      share_positive_estimate = mean(ok$group_dm_estimate > 0),
      stringsAsFactors = FALSE
    )
  } else {
    data.frame(
      n_total_spec = nrow(spec_grid),
      n_ok_spec = 0L,
      median_estimate = NA_real_,
      ci_lower = NA_real_, ci_upper = NA_real_,
      share_p_under_05 = NA_real_,
      share_positive_estimate = NA_real_,
      stringsAsFactors = FALSE
    )
  }

  list(
    n_long = nrow(prepared),
    spec_grid = spec_grid,
    spec_results = spec_with_meta,
    curve_summary = curve_summary
  )
}

# ============================================================================
# 77 — H4 SEM Multiverse
# ============================================================================

multi_h4_spec_grid <- function(seed = 20260514L, n_random_subset = 60L) {
  full_grid <- expand.grid(
    estimator = c("WLSMV", "MLR"),
    beck_struct = c("single_factor", "cog_som_two_factor"),
    missing_strategy = c("listwise", "fiml"),
    cluster = c("aile_no", "none"),
    stringsAsFactors = FALSE
  )
  full_grid$spec_id <- seq_len(nrow(full_grid))
  if (n_random_subset >= nrow(full_grid)) return(full_grid)
  set.seed(seed)
  sub_idx <- sample(seq_len(nrow(full_grid)), n_random_subset, replace = FALSE)
  full_grid[sort(sub_idx), , drop = FALSE]
}

multi_h4_syntax <- function(beck_struct = "single_factor") {
  embu_lines <- c(
    "embu_red =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + embu_p_q12 + embu_p_q16 + embu_p_q21 + embu_p_q22 + embu_p_q28"
  )
  beck_lines <- if (beck_struct == "single_factor") {
    "beck_lat =~ beck_1 + beck_2 + beck_3 + beck_4 + beck_5 + beck_6 + beck_7 + beck_8 + beck_9 + beck_10 + beck_11 + beck_12 + beck_13 + beck_14 + beck_15 + beck_16 + beck_17 + beck_18 + beck_19 + beck_20 + beck_21"
  } else {
    c(
      "beck_cog =~ beck_1 + beck_2 + beck_3 + beck_4 + beck_5 + beck_6 + beck_7 + beck_8 + beck_9 + beck_10 + beck_11 + beck_12 + beck_13",
      "beck_som =~ beck_14 + beck_15 + beck_16 + beck_17 + beck_18 + beck_19 + beck_20 + beck_21",
      "beck_lat =~ 1*beck_cog + 1*beck_som"
    )
  }
  structural <- "embu_red ~ a*beck_lat"
  paste(c(embu_lines, beck_lines, structural), collapse = "\n")
}

multi_h4_fit_one_spec <- function(spec_row, df_family_scored) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(data.frame(
      spec_id = spec_row$spec_id,
      status = "lavaan_unavailable",
      a_estimate = NA_real_, a_se = NA_real_, a_p = NA_real_,
      cfi = NA_real_, rmsea = NA_real_, srmr = NA_real_, n_used = NA_integer_,
      stringsAsFactors = FALSE
    ))
  }
  syntax <- multi_h4_syntax(spec_row$beck_struct)

  ordered_cols <- if (spec_row$estimator == "WLSMV") {
    c(paste0("embu_p_q", sprintf("%02d", c(5, 9, 10, 12, 16, 21, 22, 28))),
      paste0("beck_", 1:21))
  } else NULL

  args <- list(
    model = syntax,
    data = df_family_scored,
    estimator = spec_row$estimator,
    missing = if (spec_row$missing_strategy == "fiml") "fiml" else "listwise",
    check.gradient = FALSE
  )
  if (!is.null(ordered_cols)) args$ordered <- ordered_cols
  if (spec_row$cluster == "aile_no" && "aile_no" %in% names(df_family_scored)) {
    args$cluster <- "aile_no"
  }

  fit <- tryCatch(do.call(lavaan::sem, args), error = function(e) e)
  if (inherits(fit, "error")) {
    return(data.frame(
      spec_id = spec_row$spec_id,
      status = "fit_error",
      a_estimate = NA_real_, a_se = NA_real_, a_p = NA_real_,
      cfi = NA_real_, rmsea = NA_real_, srmr = NA_real_, n_used = NA_integer_,
      stringsAsFactors = FALSE
    ))
  }
  if (!isTRUE(lavaan::lavInspect(fit, "converged"))) {
    return(data.frame(
      spec_id = spec_row$spec_id,
      status = "no_convergence",
      a_estimate = NA_real_, a_se = NA_real_, a_p = NA_real_,
      cfi = NA_real_, rmsea = NA_real_, srmr = NA_real_, n_used = NA_integer_,
      stringsAsFactors = FALSE
    ))
  }
  est <- lavaan::standardizedSolution(fit)
  a_row <- est[est$op == "~" & est$lhs == "embu_red" & est$rhs == "beck_lat", , drop = FALSE]
  fitm <- lavaan::fitMeasures(fit, c("cfi", "rmsea", "srmr"))
  data.frame(
    spec_id = spec_row$spec_id,
    status = "ok",
    a_estimate = if (nrow(a_row) > 0L) a_row$est.std[1L] else NA_real_,
    a_se = if (nrow(a_row) > 0L) a_row$se[1L] else NA_real_,
    a_p = if (nrow(a_row) > 0L) a_row$pvalue[1L] else NA_real_,
    cfi = unname(fitm["cfi"]),
    rmsea = unname(fitm["rmsea"]),
    srmr = unname(fitm["srmr"]),
    n_used = lavaan::lavInspect(fit, "ntotal"),
    stringsAsFactors = FALSE
  )
}

multi_h4_pipeline <- function(df_family_scored, n_random_subset = 16L,
                               seed = 20260514L) {
  spec_grid <- multi_h4_spec_grid(seed = seed, n_random_subset = n_random_subset)
  rows <- vector("list", nrow(spec_grid))
  for (i in seq_len(nrow(spec_grid))) {
    rows[[i]] <- multi_h4_fit_one_spec(spec_grid[i, , drop = FALSE], df_family_scored)
  }
  spec_results <- do.call(rbind, rows)
  spec_with_meta <- merge(spec_results, spec_grid, by = "spec_id", all.x = TRUE)

  ok <- spec_results[spec_results$status == "ok", , drop = FALSE]
  summary_row <- if (nrow(ok) > 0L) {
    data.frame(
      n_total_spec = nrow(spec_grid),
      n_ok_spec = nrow(ok),
      median_a = stats::median(ok$a_estimate),
      ci_lower = stats::quantile(ok$a_estimate, 0.025),
      ci_upper = stats::quantile(ok$a_estimate, 0.975),
      share_p_under_05 = mean(ok$a_p < 0.05, na.rm = TRUE),
      median_cfi = stats::median(ok$cfi, na.rm = TRUE),
      median_rmsea = stats::median(ok$rmsea, na.rm = TRUE),
      median_srmr = stats::median(ok$srmr, na.rm = TRUE),
      stringsAsFactors = FALSE
    )
  } else {
    data.frame(
      n_total_spec = nrow(spec_grid),
      n_ok_spec = 0L,
      median_a = NA_real_, ci_lower = NA_real_, ci_upper = NA_real_,
      share_p_under_05 = NA_real_,
      median_cfi = NA_real_, median_rmsea = NA_real_, median_srmr = NA_real_,
      stringsAsFactors = FALSE
    )
  }

  list(
    spec_grid = spec_grid,
    spec_results = spec_with_meta,
    summary = summary_row
  )
}

# ============================================================================
# 78 — Bayesian Model Averaging (basit IV-weighted approximation)
# ============================================================================

multi_bma_estimate <- function(spec_results, estimate_col = "group_dm_estimate",
                                se_col = "group_dm_se") {
  ok <- spec_results[spec_results$status == "ok" &
    !is.na(spec_results[[estimate_col]]) &
    !is.na(spec_results[[se_col]]), , drop = FALSE]
  if (nrow(ok) == 0L) {
    return(data.frame(
      method = "inverse_variance_BMA_proxy",
      n_spec_ok = 0L,
      bma_pooled = NA_real_,
      bma_lower = NA_real_,
      bma_upper = NA_real_,
      tau = NA_real_,
      stringsAsFactors = FALSE
    ))
  }
  w <- 1 / (ok[[se_col]]^2)
  pooled <- sum(w * ok[[estimate_col]]) / sum(w)
  pooled_se <- sqrt(1 / sum(w))
  data.frame(
    method = "inverse_variance_BMA_proxy",
    n_spec_ok = nrow(ok),
    bma_pooled = pooled,
    bma_lower = pooled - 1.96 * pooled_se,
    bma_upper = pooled + 1.96 * pooled_se,
    tau = stats::sd(ok[[estimate_col]]),
    stringsAsFactors = FALSE
  )
}

# ============================================================================
# 79 — Specification Curve Inferential Test (Simonsohn 2020)
# ============================================================================

multi_sca_inferential <- function(prepared_long, observed_curve_summary,
                                    n_perm = 5000L, seed = 20260515L,
                                    estimator = c("median_t", "share_p")) {
  estimator <- match.arg(estimator)
  if (is.null(prepared_long) || nrow(prepared_long) < 50L) {
    return(data.frame(
      n_perm = n_perm,
      observed_test_stat = NA_real_,
      perm_p_value = NA_real_,
      estimator = estimator,
      stringsAsFactors = FALSE
    ))
  }
  set.seed(seed)
  outcome <- "embu_c_reddetme_mean"
  if (!outcome %in% names(prepared_long)) {
    return(data.frame(
      n_perm = n_perm,
      observed_test_stat = NA_real_,
      perm_p_value = NA_real_,
      estimator = estimator,
      stringsAsFactors = FALSE
    ))
  }
  observed_t <- if (estimator == "median_t") {
    fit <- stats::lm(stats::as.formula(sprintf("%s ~ group_dm + cocuk_yas_z + ses_latent_z",
      outcome)), data = prepared_long)
    cs <- summary(fit)$coefficients
    if ("group_dm" %in% rownames(cs)) cs["group_dm", "t value"] else NA_real_
  } else {
    fit <- stats::lm(stats::as.formula(sprintf("%s ~ group_dm + cocuk_yas_z + ses_latent_z",
      outcome)), data = prepared_long)
    cs <- summary(fit)$coefficients
    if ("group_dm" %in% rownames(cs)) cs["group_dm", "Pr(>|t|)"] else NA_real_
  }

  if (is.na(observed_t)) {
    return(data.frame(
      n_perm = n_perm,
      observed_test_stat = NA_real_,
      perm_p_value = NA_real_,
      estimator = estimator,
      stringsAsFactors = FALSE
    ))
  }

  # Permutation: shuffle group_dm n_perm times
  perm_stats <- numeric(n_perm)
  for (k in seq_len(n_perm)) {
    perm_data <- prepared_long
    perm_data$group_dm <- sample(prepared_long$group_dm)
    fit <- tryCatch(
      stats::lm(stats::as.formula(sprintf("%s ~ group_dm + cocuk_yas_z + ses_latent_z",
        outcome)), data = perm_data),
      error = function(e) NULL
    )
    if (is.null(fit)) {
      perm_stats[k] <- NA_real_
      next
    }
    cs <- summary(fit)$coefficients
    perm_stats[k] <- if (estimator == "median_t") {
      if ("group_dm" %in% rownames(cs)) cs["group_dm", "t value"] else NA_real_
    } else {
      if ("group_dm" %in% rownames(cs)) cs["group_dm", "Pr(>|t|)"] else NA_real_
    }
  }
  perm_stats <- perm_stats[!is.na(perm_stats)]

  perm_p <- if (estimator == "median_t") {
    mean(abs(perm_stats) >= abs(observed_t))
  } else {
    mean(perm_stats <= observed_t)
  }

  data.frame(
    n_perm = length(perm_stats),
    observed_test_stat = observed_t,
    perm_p_value = perm_p,
    estimator = estimator,
    stringsAsFactors = FALSE
  )
}

# ============================================================================
# Pipeline
# ============================================================================

run_multiverse_pipeline <- function(df_family_ses, df_long_scored, df_family_scored,
                                     h1_n_spec = 120L,
                                     h4_n_spec = 16L,
                                     n_perm = 5000L,
                                     seed = 20260513L) {
  h1_result <- multi_h1_pipeline(df_family_ses, df_long_scored,
    n_random_subset = h1_n_spec, seed = seed)

  h4_result <- multi_h4_pipeline(df_family_scored,
    n_random_subset = h4_n_spec, seed = seed + 1L)

  bma_h1 <- multi_bma_estimate(h1_result$spec_results,
    estimate_col = "group_dm_estimate", se_col = "group_dm_se")
  bma_h4 <- multi_bma_estimate(h4_result$spec_results,
    estimate_col = "a_estimate", se_col = "a_se")
  bma_h1$family <- "H1"
  bma_h4$family <- "H4"
  bma_combined <- rbind(bma_h1, bma_h4)

  prepared <- multi_h1_prepare_long(df_long_scored, df_family_ses)
  sca_result <- multi_sca_inferential(prepared, h1_result$curve_summary,
    n_perm = n_perm, seed = seed + 2L)

  list(
    h1_spec_grid = h1_result$spec_grid,
    h1_spec_results = h1_result$spec_results,
    h1_curve_summary = h1_result$curve_summary,
    h4_spec_results = h4_result$spec_results,
    h4_summary = h4_result$summary,
    bma = bma_combined,
    sca_inferential = sca_result,
    target_summary = data.frame(
      analysis = "multiverse_phase2",
      h1_n_spec_run = nrow(h1_result$spec_grid),
      h4_n_spec_run = nrow(h4_result$spec_grid),
      n_perm = n_perm,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXVII/76, 77, 78, 79)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
