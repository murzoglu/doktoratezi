# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXIII/61-64
# H5 Diadik Tutarlilik Genisletmesi
#
# 61 — MTMM (Eid 2008 CT-C(M-1)): 4 trait (sicaklik/AK/reddetme/karsilastirma)
#      x 2 method (anne reference + indeks). Trait-method varyans dekompozisyonu.
#
# 62 — Beck x Grup diadic moderation: anne-cocuk fark skoru uzerinde
#      group_dm * beck_total_z etkilesimi (lm + bootstrap CI). Brms opsiyonel.
#
# 63 — Sibling-pair concordance ICC: aile icinde indeks <-> kardes EMBU-C
#      alt olcek skorlari, group stratifiye.
#
# 64 — H5 strateji Bayesian pooling: 5 H5 strateji estimate'lerini brms
#      random-effects meta-analitik pooling ile birlestir; tau heterogeneity
#      ve pooled mean credible interval. brms yoksa metafor fallback;
#      ikisi de yoksa basit weighted average + tau IQR.

h5ext_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

h5ext_anne_columns <- function(items) {
  paste0("embu_p_q", sprintf("%02d", items))
}

h5ext_cocuk_columns <- function(items) {
  paste0("embu_c_q", sprintf("%02d", items))
}

h5ext_subscale_map <- function() {
  if (exists("embu_subscale_map", mode = "function")) {
    return(embu_subscale_map())
  }
  list(
    sicaklik = c(1, 3, 6, 7, 13, 17, 20, 24, 26),
    asiri_koruma = c(4, 8, 14, 15, 19, 23, 25),
    reddetme = c(5, 9, 10, 12, 16, 21, 22, 28),
    karsilastirma = c(2, 11, 18, 27, 29)
  )
}

h5ext_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

h5ext_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(sprintf("%s missing column(s): %s",
      context, paste(missing_columns, collapse = ", ")), call. = FALSE)
  }
  invisible(TRUE)
}

h5ext_scale <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

# ============================================================================
# 61 — MTMM CT-C(M-1)
# ============================================================================

h5ext_mtmm_syntax <- function(subscale_map = h5ext_subscale_map()) {
  trait_lines <- character(0)
  method_lines <- character(0)
  ortho_lines <- character(0)

  trait_labels <- character(0)
  for (sl in names(subscale_map)) {
    items <- subscale_map[[sl]]
    anne_cols <- h5ext_anne_columns(items)
    cocuk_cols <- h5ext_cocuk_columns(items)
    indicator_str <- paste(c(anne_cols, cocuk_cols), collapse = " + ")
    tlabel <- sprintf("T_%s", sl)
    trait_lines <- c(trait_lines, sprintf("%s =~ %s", tlabel, indicator_str))
    trait_labels <- c(trait_labels, tlabel)
  }

  # Method factor: indeks (anne reference)
  cocuk_all <- unlist(lapply(subscale_map, function(it) h5ext_cocuk_columns(it)),
    use.names = FALSE)
  method_lines <- sprintf("M_indeks =~ %s", paste(cocuk_all, collapse = " + "))

  # Method orthogonal to all traits (CT-C(M-1) standardi)
  for (tl in trait_labels) {
    ortho_lines <- c(ortho_lines, sprintf("M_indeks ~~ 0 * %s", tl))
  }

  paste(c(trait_lines, method_lines, ortho_lines), collapse = "\n")
}

h5ext_mtmm_prepare_data <- function(df_family_scored, df_long_scored,
                                    subscale_map = h5ext_subscale_map()) {
  all_items <- unique(unlist(subscale_map))
  anne_cols <- h5ext_anne_columns(all_items)
  cocuk_cols <- h5ext_cocuk_columns(all_items)

  h5ext_require_columns(df_family_scored, c("aile_no", anne_cols), "MTMM family data")
  h5ext_require_columns(df_long_scored, c("aile_no", "family_role_f", cocuk_cols),
    "MTMM long data")

  family_side <- df_family_scored[, c("aile_no", anne_cols), drop = FALSE]
  long <- df_long_scored
  long$role_token <- h5ext_normalize_role(long$family_role_f)
  indeks <- long[!is.na(long$role_token) & long$role_token == "indeks", , drop = FALSE]
  if (anyDuplicated(indeks$aile_no) > 0L) {
    stop("MTMM long data has duplicated indeks rows", call. = FALSE)
  }
  indeks_side <- indeks[, c("aile_no", cocuk_cols), drop = FALSE]
  paired <- merge(family_side, indeks_side, by = "aile_no",
    all.x = FALSE, all.y = FALSE)
  for (col in c(anne_cols, cocuk_cols)) {
    paired[[col]] <- suppressWarnings(as.integer(as.character(paired[[col]])))
  }
  paired
}

h5ext_mtmm_fit <- function(paired_data, subscale_map = h5ext_subscale_map(),
                           estimator = "MLR") {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = "lavaan_unavailable"))
  }
  syntax <- h5ext_mtmm_syntax(subscale_map)
  ordered_cols <- c(
    h5ext_anne_columns(unlist(subscale_map)),
    h5ext_cocuk_columns(unlist(subscale_map))
  )
  fit <- tryCatch(
    suppressWarnings(lavaan::cfa(
      syntax,
      data = paired_data,
      estimator = estimator,
      missing = if (estimator == "WLSMV") "pairwise" else "fiml",
      check.gradient = FALSE
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", error_message = conditionMessage(fit)))
  }
  list(
    status = if (isTRUE(lavaan::lavInspect(fit, "converged"))) "ok" else "no_convergence",
    fit = fit,
    estimator_used = estimator
  )
}

h5ext_mtmm_variance_decomposition <- function(fit) {
  est <- lavaan::standardizedSolution(fit, type = "std.all")
  loadings <- est[est$op == "=~", , drop = FALSE]
  loadings$lambda_sq <- loadings$est.std^2

  loadings$factor_type <- ifelse(grepl("^T_", loadings$lhs), "trait",
    ifelse(grepl("^M_", loadings$lhs), "method", "other"))

  trait_per_item <- stats::aggregate(
    lambda_sq ~ rhs,
    data = loadings[loadings$factor_type == "trait", , drop = FALSE],
    FUN = sum, na.rm = TRUE
  )
  names(trait_per_item) <- c("item", "trait_var")

  method_per_item <- stats::aggregate(
    lambda_sq ~ rhs,
    data = loadings[loadings$factor_type == "method", , drop = FALSE],
    FUN = sum, na.rm = TRUE
  )
  names(method_per_item) <- c("item", "method_var")

  out <- merge(trait_per_item, method_per_item, by = "item", all = TRUE)
  out$trait_var[is.na(out$trait_var)] <- 0
  out$method_var[is.na(out$method_var)] <- 0
  out$communality <- out$trait_var + out$method_var
  out$trait_share <- ifelse(out$communality > 0, out$trait_var / out$communality, NA_real_)
  out$method_share <- ifelse(out$communality > 0, out$method_var / out$communality, NA_real_)
  out$informant <- ifelse(grepl("^embu_p_", out$item), "anne",
    ifelse(grepl("^embu_c_", out$item), "indeks", NA_character_))
  out
}

h5ext_mtmm_pipeline <- function(df_family_scored, df_long_scored,
                                estimator = "MLR") {
  paired <- h5ext_mtmm_prepare_data(df_family_scored, df_long_scored)
  result <- h5ext_mtmm_fit(paired, estimator = estimator)
  if (!identical(result$status, "ok")) {
    return(list(
      status = data.frame(
        analysis = "mtmm_ct_c_m1",
        status = result$status,
        n_pairs = nrow(paired),
        error_message = result$error_message %||% NA_character_,
        stringsAsFactors = FALSE
      ),
      variance = NULL,
      fit_indices = NULL
    ))
  }
  m <- lavaan::fitMeasures(result$fit, c("chisq", "df", "pvalue", "cfi", "tli",
    "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
  fit_indices <- data.frame(
    chi_sq = unname(m["chisq"]),
    df = unname(m["df"]),
    p_value = unname(m["pvalue"]),
    cfi = unname(m["cfi"]),
    tli = unname(m["tli"]),
    rmsea = unname(m["rmsea"]),
    rmsea_ci_lower = unname(m["rmsea.ci.lower"]),
    rmsea_ci_upper = unname(m["rmsea.ci.upper"]),
    srmr = unname(m["srmr"]),
    estimator_used = result$estimator_used,
    stringsAsFactors = FALSE
  )
  variance <- h5ext_mtmm_variance_decomposition(result$fit)
  list(
    status = data.frame(
      analysis = "mtmm_ct_c_m1",
      status = "ok",
      n_pairs = nrow(paired),
      error_message = NA_character_,
      stringsAsFactors = FALSE
    ),
    variance = variance,
    fit_indices = fit_indices
  )
}

# ============================================================================
# 62 — Beck x Grup Moderasyonu (Diadik Fark Skoru)
# ============================================================================

h5ext_beck_moderation_one <- function(family_frame, outcome_subscale,
                                      bootstrap_n = 2000L) {
  p_col <- paste0("embu_p_", outcome_subscale, "_mean")
  c_col <- paste0("embu_c_", outcome_subscale, "_mean")
  needed <- c(p_col, c_col, "group_dm", "beck_total_z", "ses_latent_z", "anne_yas_z")
  if (any(!needed %in% names(family_frame))) {
    return(list(status = "missing_columns",
      missing = setdiff(needed, names(family_frame))))
  }
  df <- family_frame
  df$disc_score <- df[[p_col]] - df[[c_col]]
  df$disc_abs <- abs(df$disc_score)

  formula <- stats::as.formula(
    "disc_score ~ group_dm * beck_total_z + ses_latent_z + anne_yas_z"
  )
  fit <- tryCatch(stats::lm(formula, data = df), error = function(e) e)
  if (inherits(fit, "error")) {
    return(list(status = "fit_error",
      outcome_subscale = outcome_subscale,
      error_message = conditionMessage(fit)))
  }
  sm <- summary(fit)
  coef_df <- as.data.frame(sm$coefficients)
  coef_df$term <- rownames(coef_df)
  rownames(coef_df) <- NULL
  names(coef_df) <- gsub("[ ,()<>]+", "_", names(coef_df))
  coef_df$outcome_subscale <- outcome_subscale

  # Bootstrap CI for group:beck interaction
  boot_int <- replicate(bootstrap_n, {
    idx <- sample(seq_len(nrow(df)), nrow(df), replace = TRUE)
    tryCatch(
      stats::coef(stats::lm(formula, data = df[idx, , drop = FALSE]))[
        "group_dm:beck_total_z"
      ],
      error = function(e) NA_real_
    )
  })
  boot_ci <- stats::quantile(boot_int, c(0.025, 0.5, 0.975), na.rm = TRUE)

  list(
    status = "ok",
    outcome_subscale = outcome_subscale,
    coefficients = coef_df,
    bootstrap_interaction_ci = data.frame(
      outcome_subscale = outcome_subscale,
      term = "group_dm:beck_total_z",
      estimate = unname(stats::coef(fit)["group_dm:beck_total_z"]),
      boot_lower = unname(boot_ci[1L]),
      boot_median = unname(boot_ci[2L]),
      boot_upper = unname(boot_ci[3L]),
      bootstrap_n = bootstrap_n,
      stringsAsFactors = FALSE
    ),
    n_used = stats::nobs(fit),
    r_squared = sm$r.squared
  )
}

h5ext_beck_moderation_pipeline <- function(family_frame,
                                           outcomes = h5ext_subscale_outcomes(),
                                           bootstrap_n = 2000L) {
  status_rows <- list()
  coef_rows <- list()
  ci_rows <- list()
  for (sub in outcomes) {
    r <- h5ext_beck_moderation_one(family_frame, sub, bootstrap_n = bootstrap_n)
    status_rows[[sub]] <- data.frame(
      outcome_subscale = sub,
      status = r$status,
      n_used = r$n_used %||% NA_integer_,
      r_squared = r$r_squared %||% NA_real_,
      bootstrap_n = bootstrap_n,
      error_message = r$error_message %||% NA_character_,
      stringsAsFactors = FALSE
    )
    if (identical(r$status, "ok")) {
      coef_rows[[sub]] <- r$coefficients
      ci_rows[[sub]] <- r$bootstrap_interaction_ci
    }
  }
  bind <- function(rows) if (length(rows) > 0L) do.call(rbind, rows) else NULL
  list(
    status = bind(status_rows),
    coefficients = bind(coef_rows),
    bootstrap_interaction_ci = bind(ci_rows)
  )
}

# ============================================================================
# 63 — Sibling-Pair Concordance ICC
# ============================================================================

h5ext_sibling_pair_data <- function(df_long_scored,
                                    outcome_subscale) {
  c_col <- paste0("embu_c_", outcome_subscale, "_mean")
  needed <- c("aile_no", "family_role_f", c_col)
  h5ext_require_columns(df_long_scored, needed, "sibling pair data")
  long <- df_long_scored[, needed, drop = FALSE]
  long$role_token <- h5ext_normalize_role(long$family_role_f)
  indeks <- long[!is.na(long$role_token) & long$role_token == "indeks",
    c("aile_no", c_col), drop = FALSE]
  kardes <- long[!is.na(long$role_token) & long$role_token == "kardes",
    c("aile_no", c_col), drop = FALSE]
  names(indeks)[2L] <- "indeks_value"
  names(kardes)[2L] <- "kardes_value"
  paired <- merge(indeks, kardes, by = "aile_no", all = FALSE)
  paired
}

h5ext_compute_icc_2_1 <- function(values_a, values_b) {
  ok <- !is.na(values_a) & !is.na(values_b)
  values_a <- values_a[ok]
  values_b <- values_b[ok]
  n <- length(values_a)
  if (n < 5L) {
    return(data.frame(
      icc = NA_real_, ci_lower = NA_real_, ci_upper = NA_real_,
      n = n, stringsAsFactors = FALSE
    ))
  }
  # ICC(2,1) two-way random absolute agreement: psych::ICC veya manuel
  if (requireNamespace("psych", quietly = TRUE)) {
    icc_obj <- tryCatch(
      psych::ICC(cbind(values_a, values_b), missing = FALSE)$results,
      error = function(e) NULL
    )
    if (!is.null(icc_obj)) {
      row <- icc_obj[icc_obj$type == "ICC2", , drop = FALSE]
      if (nrow(row) >= 1L) {
        return(data.frame(
          icc = row$ICC[1L],
          ci_lower = row$`lower bound`[1L],
          ci_upper = row$`upper bound`[1L],
          n = n,
          stringsAsFactors = FALSE
        ))
      }
    }
  }
  # Fallback: Pearson r
  r <- stats::cor(values_a, values_b)
  data.frame(icc = r, ci_lower = NA_real_, ci_upper = NA_real_, n = n,
    stringsAsFactors = FALSE)
}

h5ext_sibling_pair_pipeline <- function(df_family_scored, df_long_scored,
                                        outcomes = h5ext_subscale_outcomes()) {
  if (!"aile_no" %in% names(df_family_scored)) {
    stop("df_family_scored must contain aile_no", call. = FALSE)
  }
  group_col <- if ("group_dm" %in% names(df_family_scored)) {
    "group_dm"
  } else if ("group_f" %in% names(df_family_scored)) {
    "group_f"
  } else {
    NA_character_
  }
  group_lookup <- if (!is.na(group_col)) {
    setNames(df_family_scored[[group_col]], df_family_scored$aile_no)
  } else {
    NULL
  }

  rows <- list()
  for (sub in outcomes) {
    paired <- h5ext_sibling_pair_data(df_long_scored, sub)
    if (!is.null(group_lookup)) {
      paired$group <- group_lookup[as.character(paired$aile_no)]
      if (is.factor(paired$group)) {
        paired$group_label <- as.character(paired$group)
      } else {
        paired$group_label <- ifelse(paired$group == 1L, "DM", "Kontrol")
      }
    } else {
      paired$group_label <- "all"
    }

    # Pooled
    pooled <- h5ext_compute_icc_2_1(paired$indeks_value, paired$kardes_value)
    pooled$group_label <- "all"
    pooled$outcome_subscale <- sub
    rows[[paste(sub, "all", sep = "_")]] <- pooled

    # Stratified
    for (g in unique(stats::na.omit(paired$group_label))) {
      sub_paired <- paired[paired$group_label == g, , drop = FALSE]
      icc <- h5ext_compute_icc_2_1(sub_paired$indeks_value, sub_paired$kardes_value)
      icc$group_label <- g
      icc$outcome_subscale <- sub
      rows[[paste(sub, g, sep = "_")]] <- icc
    }
  }
  list(
    icc_table = do.call(rbind, rows)
  )
}

# ============================================================================
# 64 — H5 Strateji Bayesian Pooling
# ============================================================================

h5ext_strategy_estimates_default <- function() {
  # CSR §11.5 raporlanan H5 strateji estimate'leri (DM grubu odak)
  data.frame(
    strategy = c("ICC", "RSA", "CFM", "OlsenKenny", "k_coef"),
    estimate_dm = c(0.06, 0.18, 0.22, 0.29, 0.15),
    estimate_kontrol = c(0.10, 0.12, 0.18, 0.17, 0.09),
    se = c(0.05, 0.06, 0.07, 0.05, 0.06),
    source = "CSR §11.5 raporlanan degerler",
    stringsAsFactors = FALSE
  )
}

h5ext_strategy_pooling <- function(strategy_estimates = h5ext_strategy_estimates_default(),
                                   group_focus = c("dm", "kontrol", "diff"),
                                   chains = 2L, iter = 2000L) {
  group_focus <- match.arg(group_focus)
  if (group_focus == "diff") {
    yi <- strategy_estimates$estimate_dm - strategy_estimates$estimate_kontrol
    se <- sqrt(2) * strategy_estimates$se
  } else if (group_focus == "dm") {
    yi <- strategy_estimates$estimate_dm
    se <- strategy_estimates$se
  } else {
    yi <- strategy_estimates$estimate_kontrol
    se <- strategy_estimates$se
  }

  # brms varsa Bayesian random-effects pool
  if (requireNamespace("brms", quietly = TRUE)) {
    pool_data <- data.frame(
      strategy = strategy_estimates$strategy,
      yi = yi,
      se = se,
      stringsAsFactors = FALSE
    )
    fit <- tryCatch(
      suppressWarnings(brms::brm(
        formula = brms::bf(yi | brms::se(se) ~ 1 + (1 | strategy)),
        data = pool_data,
        prior = c(
          brms::prior(normal(0, 0.5), class = "Intercept"),
          brms::prior(student_t(3, 0, 0.3), class = "sd")
        ),
        chains = chains,
        iter = iter,
        warmup = floor(iter / 2),
        refresh = 0,
        silent = 2,
        seed = 20260508
      )),
      error = function(e) e
    )
    if (!inherits(fit, "error")) {
      post <- as.matrix(fit, variable = c("b_Intercept", "sd_strategy__Intercept"))
      summary_row <- data.frame(
        group_focus = group_focus,
        method = "brms_random_effects",
        n_strategies = nrow(pool_data),
        pooled_mean = unname(stats::median(post[, "b_Intercept"])),
        pooled_lower = unname(stats::quantile(post[, "b_Intercept"], 0.025)),
        pooled_upper = unname(stats::quantile(post[, "b_Intercept"], 0.975)),
        tau = unname(stats::median(post[, "sd_strategy__Intercept"])),
        tau_lower = unname(stats::quantile(post[, "sd_strategy__Intercept"], 0.025)),
        tau_upper = unname(stats::quantile(post[, "sd_strategy__Intercept"], 0.975)),
        stringsAsFactors = FALSE
      )
      return(summary_row)
    }
  }
  # Fallback: metafor or weighted average
  if (requireNamespace("metafor", quietly = TRUE)) {
    fit <- tryCatch(
      metafor::rma(yi = yi, sei = se, method = "REML"),
      error = function(e) e
    )
    if (!inherits(fit, "error")) {
      return(data.frame(
        group_focus = group_focus,
        method = "metafor_REML",
        n_strategies = length(yi),
        pooled_mean = as.numeric(fit$beta),
        pooled_lower = fit$ci.lb,
        pooled_upper = fit$ci.ub,
        tau = sqrt(fit$tau2),
        tau_lower = NA_real_,
        tau_upper = NA_real_,
        stringsAsFactors = FALSE
      ))
    }
  }
  # Last resort: inverse-variance weighted mean
  w <- 1 / se^2
  pooled <- sum(w * yi) / sum(w)
  pooled_se <- sqrt(1 / sum(w))
  data.frame(
    group_focus = group_focus,
    method = "inverse_variance_weighted",
    n_strategies = length(yi),
    pooled_mean = pooled,
    pooled_lower = pooled - 1.96 * pooled_se,
    pooled_upper = pooled + 1.96 * pooled_se,
    tau = stats::sd(yi),
    tau_lower = NA_real_,
    tau_upper = NA_real_,
    stringsAsFactors = FALSE
  )
}

h5ext_strategy_pooling_pipeline <- function(strategy_estimates =
                                              h5ext_strategy_estimates_default(),
                                            chains = 2L, iter = 2000L) {
  out <- list()
  for (gf in c("dm", "kontrol", "diff")) {
    out[[gf]] <- h5ext_strategy_pooling(strategy_estimates, group_focus = gf,
      chains = chains, iter = iter)
  }
  list(
    strategy_estimates = strategy_estimates,
    pooled_summary = do.call(rbind, out)
  )
}

# ============================================================================
# Pipeline
# ============================================================================

run_h5_extensions_pipeline <- function(df_family_ses, df_long_scored,
                                       df_family_scored = NULL,
                                       bootstrap_n = 2000L,
                                       brms_chains = 2L,
                                       brms_iter = 2000L,
                                       run_mtmm = TRUE,
                                       run_pooling = TRUE) {
  if (is.null(df_family_scored)) df_family_scored <- df_family_ses

  # 61 — MTMM
  mtmm_result <- if (run_mtmm) {
    h5ext_mtmm_pipeline(df_family_scored, df_long_scored)
  } else {
    list(status = NULL, variance = NULL, fit_indices = NULL)
  }

  # 62 — Beck x Grup moderation
  needed_family <- c("aile_no", "group_dm", "beck_total", "ses_latent", "anne_yas",
    paste0("embu_p_", h5ext_subscale_outcomes(), "_mean"))
  family_frame <- df_family_ses
  if (!"beck_total_z" %in% names(family_frame)) {
    family_frame$beck_total_z <- h5ext_scale(family_frame$beck_total)
  }
  if (!"ses_latent_z" %in% names(family_frame)) {
    family_frame$ses_latent_z <- h5ext_scale(family_frame$ses_latent)
  }
  if (!"anne_yas_z" %in% names(family_frame)) {
    family_frame$anne_yas_z <- h5ext_scale(family_frame$anne_yas)
  }
  c_means <- paste0("embu_c_", h5ext_subscale_outcomes(), "_mean")
  long_indeks <- df_long_scored
  long_indeks$role_token <- h5ext_normalize_role(long_indeks$family_role_f)
  long_indeks <- long_indeks[!is.na(long_indeks$role_token) &
    long_indeks$role_token == "indeks", c("aile_no", c_means), drop = FALSE]
  family_frame <- merge(family_frame, long_indeks, by = "aile_no",
    all.x = TRUE, all.y = FALSE)

  beck_mod <- h5ext_beck_moderation_pipeline(family_frame,
    bootstrap_n = bootstrap_n)

  # 63 — Sibling-pair ICC
  sibling_icc <- h5ext_sibling_pair_pipeline(df_family_scored, df_long_scored)

  # 64 — Strategy pooling
  pooling_result <- if (run_pooling) {
    h5ext_strategy_pooling_pipeline(chains = brms_chains, iter = brms_iter)
  } else {
    list(strategy_estimates = NULL, pooled_summary = NULL)
  }

  list(
    mtmm_status = mtmm_result$status,
    mtmm_fit_indices = mtmm_result$fit_indices,
    mtmm_variance = mtmm_result$variance,
    beck_moderation_status = beck_mod$status,
    beck_moderation_coefficients = beck_mod$coefficients,
    beck_moderation_bootstrap_ci = beck_mod$bootstrap_interaction_ci,
    sibling_icc = sibling_icc$icc_table,
    strategy_estimates = pooling_result$strategy_estimates,
    strategy_pooled_summary = pooling_result$pooled_summary,
    target_summary = data.frame(
      analysis = "h5_extensions_phase2",
      bootstrap_n = bootstrap_n,
      brms_chains = brms_chains,
      brms_iter = brms_iter,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXIII/61-64)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
