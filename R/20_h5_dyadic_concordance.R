# H5 — Diadik Tutarlılık (Dyadic Concordance)
# 5 paralel strateji: ICC + Bland-Altman, RSA, Common Fate, Olsen-Kenny CFA, k-coefficient.
# Tezin birincil yenilik katkısı (KISIM V/16, SAP §16).

h5_subscales <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

h5_dyad_specs <- function() {
  list(
    anne_idx = list(a = "embu_p_%s_mean",       b = "embu_c_idx_%s_mean", label = "Anne x Indeks"),
    anne_sib = list(a = "embu_p_%s_mean",       b = "embu_c_sib_%s_mean", label = "Anne x Kardes"),
    idx_sib  = list(a = "embu_c_idx_%s_mean",   b = "embu_c_sib_%s_mean", label = "Indeks x Kardes")
  )
}

h5_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s missing column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

h5_prepare_frame <- function(df_family_ses) {
  required <- c("aile_no", "group_f", "anne_yas", "ses_latent", "beck_total",
                paste0("embu_p_", h5_subscales(), "_mean"),
                paste0("embu_c_idx_", h5_subscales(), "_mean"),
                paste0("embu_c_sib_", h5_subscales(), "_mean"))
  h5_require_columns(df_family_ses, required, "H5 family frame")
  df <- df_family_ses
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  df$anne_yas_z   <- as.numeric(scale(df$anne_yas))
  df$ses_latent_z <- as.numeric(scale(df$ses_latent))
  df
}

# === Strateji 1: ICC(2,1) + Bland-Altman LoA ===========================

h5_icc_one_dyad <- function(df, col_a, col_b) {
  pair <- df[, c(col_a, col_b), drop = FALSE]
  pair <- pair[stats::complete.cases(pair), , drop = FALSE]
  if (nrow(pair) < 10L) {
    return(list(n = nrow(pair), icc = NA_real_, lower = NA_real_, upper = NA_real_,
                p_value = NA_real_, mean_diff = NA_real_, sd_diff = NA_real_,
                loa_lo = NA_real_, loa_hi = NA_real_))
  }
  ic <- irr::icc(pair, model = "twoway", type = "agreement", unit = "single")
  diffs <- pair[[col_a]] - pair[[col_b]]
  mean_diff <- mean(diffs)
  sd_diff <- stats::sd(diffs)
  list(
    n         = nrow(pair),
    icc       = ic$value,
    lower     = ic$lbound,
    upper     = ic$ubound,
    p_value   = ic$p.value,
    mean_diff = mean_diff,
    sd_diff   = sd_diff,
    loa_lo    = mean_diff - 1.96 * sd_diff,
    loa_hi    = mean_diff + 1.96 * sd_diff
  )
}

h5_strategy1_icc_bland_altman <- function(df) {
  dyads <- h5_dyad_specs()
  rows <- list()
  for (sub in h5_subscales()) {
    for (dyad_name in names(dyads)) {
      spec <- dyads[[dyad_name]]
      col_a <- sprintf(spec$a, sub)
      col_b <- sprintf(spec$b, sub)
      for (grp in c("Pooled", "Kontrol", "DM")) {
        sub_df <- if (grp == "Pooled") df else df[df$group_f == grp, , drop = FALSE]
        res <- h5_icc_one_dyad(sub_df, col_a, col_b)
        rows[[length(rows) + 1L]] <- data.frame(
          subscale  = sub,
          dyad      = dyad_name,
          dyad_label = spec$label,
          group     = grp,
          n         = res$n,
          icc       = res$icc,
          icc_ci_lo = res$lower,
          icc_ci_hi = res$upper,
          icc_pvalue = res$p_value,
          mean_diff = res$mean_diff,
          sd_diff   = res$sd_diff,
          loa_lo    = res$loa_lo,
          loa_hi    = res$loa_hi,
          stringsAsFactors = FALSE
        )
      }
    }
  }
  do.call(rbind, rows)
}

# === Strateji 2: Response Surface Analysis (Edwards-Parry) =============

h5_strategy2_rsa <- function(df, subscales = c("sicaklik", "reddetme")) {
  if (!requireNamespace("RSA", quietly = TRUE)) {
    return(list(
      status = data.frame(subscale = subscales, group = NA_character_,
                          status = "package_unavailable", n = NA_integer_,
                          stringsAsFactors = FALSE),
      parameters = data.frame(),
      fits = list()
    ))
  }
  status_rows <- list()
  param_rows <- list()
  fits <- list()
  for (sub in subscales) {
    p_col   <- sprintf("embu_p_%s_mean", sub)
    c_col   <- sprintf("embu_c_idx_%s_mean", sub)
    for (grp in c("Pooled", "Kontrol", "DM")) {
      grp_df <- if (grp == "Pooled") df else df[df$group_f == grp, , drop = FALSE]
      data_df <- grp_df[, c(p_col, c_col, "beck_total"), drop = FALSE]
      data_df <- data_df[stats::complete.cases(data_df), , drop = FALSE]
      colnames(data_df) <- c("X", "Y", "Z")
      n_eff <- nrow(data_df)
      if (n_eff < 50L) {
        status_rows[[length(status_rows) + 1L]] <- data.frame(
          subscale = sub, group = grp, status = "insufficient_n",
          n = n_eff, stringsAsFactors = FALSE
        )
        next
      }
      fit <- tryCatch(
        suppressWarnings(RSA::RSA(formula = Z ~ X * Y, data = data_df,
                                  models = c("full"), verbose = FALSE)),
        error = function(e) e
      )
      if (inherits(fit, "error")) {
        status_rows[[length(status_rows) + 1L]] <- data.frame(
          subscale = sub, group = grp, status = paste0("error:", conditionMessage(fit)),
          n = n_eff, stringsAsFactors = FALSE
        )
        next
      }
      fits[[paste(sub, grp, sep = "_")]] <- fit
      pars <- tryCatch(
        RSA::getPar(fit, "coef", model = "full"),
        error = function(e) NULL
      )
      if (!is.null(pars)) {
        pars_df <- as.data.frame(pars)
        pars_df$subscale <- sub
        pars_df$group <- grp
        pars_df$param <- rownames(pars_df)
        rownames(pars_df) <- NULL
        param_rows[[length(param_rows) + 1L]] <- pars_df
      }
      status_rows[[length(status_rows) + 1L]] <- data.frame(
        subscale = sub, group = grp, status = "fit_ok",
        n = n_eff, stringsAsFactors = FALSE
      )
    }
  }
  list(
    status     = do.call(rbind, status_rows),
    parameters = if (length(param_rows) > 0L) do.call(rbind, param_rows) else data.frame(),
    fits       = fits
  )
}

# === Strateji 3: Common Fate Model (latent shared parenting) ===========

h5_common_fate_model <- function(sub) {
  p_col <- sprintf("embu_p_%s_mean", sub)
  i_col <- sprintf("embu_c_idx_%s_mean", sub)
  s_col <- sprintf("embu_c_sib_%s_mean", sub)
  sprintf(
    "common =~ %s + %s + %s\ncommon ~ group_dm + anne_yas_z + ses_latent_z\n",
    p_col, i_col, s_col
  )
}

h5_strategy3_common_fate <- function(df) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = data.frame(subscale = h5_subscales(),
                                    status = "package_unavailable",
                                    stringsAsFactors = FALSE),
                fits = list(), fit_measures = data.frame()))
  }
  df$group_dm <- as.integer(df$group_f == "DM")
  status_rows <- list()
  fit_rows <- list()
  loadings_rows <- list()
  reg_rows <- list()
  fits <- list()
  for (sub in h5_subscales()) {
    p_col <- sprintf("embu_p_%s_mean", sub)
    i_col <- sprintf("embu_c_idx_%s_mean", sub)
    s_col <- sprintf("embu_c_sib_%s_mean", sub)
    cols <- c(p_col, i_col, s_col, "group_dm", "anne_yas_z", "ses_latent_z")
    sub_df <- df[, cols, drop = FALSE]
    n_complete <- sum(stats::complete.cases(sub_df))
    fit <- tryCatch(
      suppressWarnings(lavaan::sem(
        h5_common_fate_model(sub),
        data = sub_df,
        estimator = "MLR",
        missing = "fiml"
      )),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      status_rows[[length(status_rows) + 1L]] <- data.frame(
        subscale = sub, status = paste0("error:", conditionMessage(fit)),
        n_complete = n_complete, stringsAsFactors = FALSE
      )
      next
    }
    fits[[sub]] <- fit
    fm <- tryCatch(
      lavaan::fitMeasures(fit, c("cfi.robust", "tli.robust", "rmsea.robust", "srmr",
                                  "chisq", "df", "pvalue")),
      error = function(e) rep(NA_real_, 7)
    )
    fit_rows[[length(fit_rows) + 1L]] <- data.frame(
      subscale = sub,
      cfi      = unname(fm[1]),
      tli      = unname(fm[2]),
      rmsea    = unname(fm[3]),
      srmr     = unname(fm[4]),
      chisq    = unname(fm[5]),
      df       = unname(fm[6]),
      pvalue   = unname(fm[7]),
      n_used   = lavaan::lavInspect(fit, "ntotal"),
      stringsAsFactors = FALSE
    )
    pe <- lavaan::parameterEstimates(fit, standardized = TRUE)
    loadings <- pe[pe$op == "=~" & pe$lhs == "common", ]
    if (nrow(loadings) > 0L) {
      loadings$subscale <- sub
      loadings_rows[[length(loadings_rows) + 1L]] <- loadings[, c("subscale", "rhs", "est", "se", "pvalue", "std.all")]
    }
    regs <- pe[pe$op == "~" & pe$lhs == "common", ]
    if (nrow(regs) > 0L) {
      regs$subscale <- sub
      reg_rows[[length(reg_rows) + 1L]] <- regs[, c("subscale", "rhs", "est", "se", "pvalue", "std.all")]
    }
    status_rows[[length(status_rows) + 1L]] <- data.frame(
      subscale = sub, status = "fit_ok",
      n_complete = n_complete, stringsAsFactors = FALSE
    )
  }
  list(
    status       = do.call(rbind, status_rows),
    fit_measures = if (length(fit_rows) > 0L) do.call(rbind, fit_rows) else data.frame(),
    loadings     = if (length(loadings_rows) > 0L) do.call(rbind, loadings_rows) else data.frame(),
    regressions  = if (length(reg_rows) > 0L) do.call(rbind, reg_rows) else data.frame(),
    fits         = fits
  )
}

# === Strateji 4: Olsen-Kenny dyadic CFA (true latent concordance) ======

h5_dyadic_cfa_model <- function() {
  redd_p <- c("embu_p_q05", "embu_p_q09", "embu_p_q10", "embu_p_q12")
  redd_c <- c("embu_c_idx_q05", "embu_c_idx_q09", "embu_c_idx_q10", "embu_c_idx_q12")
  paste0(
    "rejection_mom   =~ ", paste(redd_p, collapse = " + "), "\n",
    "rejection_child =~ ", paste(redd_c, collapse = " + "), "\n",
    paste0(redd_p, " ~~ ", redd_c, collapse = "\n"), "\n",
    "rejection_mom ~~ rejection_child\n"
  )
}

h5_strategy4_dyadic_cfa <- function(df_family_scored, df_family_ses_groups) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = data.frame(group = NA_character_, status = "package_unavailable",
                                    stringsAsFactors = FALSE)))
  }
  redd_p <- c("embu_p_q05", "embu_p_q09", "embu_p_q10", "embu_p_q12")
  redd_c <- c("embu_c_idx_q05", "embu_c_idx_q09", "embu_c_idx_q10", "embu_c_idx_q12")
  needed <- c("aile_no", redd_p, redd_c)
  if (!all(needed %in% names(df_family_scored))) {
    return(list(status = data.frame(group = NA_character_, status = "missing_items",
                                    stringsAsFactors = FALSE)))
  }
  scored <- df_family_scored[, needed, drop = FALSE]
  group_lookup <- df_family_ses_groups[, c("aile_no", "group_f")]
  joined <- merge(scored, group_lookup, by = "aile_no", all.x = FALSE)
  joined$group_f <- factor(as.character(joined$group_f), levels = c("Kontrol", "DM"))
  status_rows <- list()
  fit_rows <- list()
  cor_rows <- list()
  fits <- list()
  for (grp in c("Pooled", "Kontrol", "DM")) {
    grp_df <- if (grp == "Pooled") joined else joined[joined$group_f == grp, , drop = FALSE]
    n_eff <- nrow(grp_df)
    fit <- tryCatch(
      suppressWarnings(lavaan::cfa(
        h5_dyadic_cfa_model(),
        data = grp_df,
        ordered = c(redd_p, redd_c),
        estimator = "WLSMV",
        std.lv = TRUE
      )),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      status_rows[[length(status_rows) + 1L]] <- data.frame(
        group = grp, status = paste0("error:", conditionMessage(fit)),
        n = n_eff, stringsAsFactors = FALSE
      )
      next
    }
    fits[[grp]] <- fit
    fm <- tryCatch(
      lavaan::fitMeasures(fit, c("cfi.scaled", "tli.scaled", "rmsea.scaled", "srmr",
                                  "chisq.scaled", "df.scaled", "pvalue.scaled")),
      error = function(e) rep(NA_real_, 7)
    )
    cor_lv <- tryCatch(
      lavaan::lavInspect(fit, "cor.lv"),
      error = function(e) NULL
    )
    true_concordance <- if (!is.null(cor_lv) && all(c("rejection_mom", "rejection_child") %in% rownames(cor_lv))) {
      cor_lv["rejection_mom", "rejection_child"]
    } else {
      NA_real_
    }
    fit_rows[[length(fit_rows) + 1L]] <- data.frame(
      group = grp,
      n     = n_eff,
      cfi   = unname(fm[1]),
      tli   = unname(fm[2]),
      rmsea = unname(fm[3]),
      srmr  = unname(fm[4]),
      chisq = unname(fm[5]),
      df    = unname(fm[6]),
      pvalue = unname(fm[7]),
      true_concordance = true_concordance,
      stringsAsFactors = FALSE
    )
    cor_rows[[length(cor_rows) + 1L]] <- data.frame(
      group = grp, true_concordance = true_concordance,
      stringsAsFactors = FALSE
    )
    status_rows[[length(status_rows) + 1L]] <- data.frame(
      group = grp, status = "fit_ok", n = n_eff,
      stringsAsFactors = FALSE
    )
  }
  list(
    status              = do.call(rbind, status_rows),
    fit_measures        = if (length(fit_rows) > 0L) do.call(rbind, fit_rows) else data.frame(),
    latent_correlations = if (length(cor_rows) > 0L) do.call(rbind, cor_rows) else data.frame(),
    fits                = fits
  )
}

# === Strateji 5: k-coefficient (Kenny et al. 2006) =====================

h5_strategy5_k_coefficient <- function(df_long_scored, n_boot = 500L, seed = 20260428L) {
  if (!requireNamespace("lme4", quietly = TRUE)) {
    return(list(status = data.frame(subscale = NA_character_, status = "package_unavailable",
                                    stringsAsFactors = FALSE)))
  }
  long <- df_long_scored
  long$group_f <- factor(as.character(long$group_f), levels = c("Kontrol", "DM"))
  role_levels <- if ("index" %in% as.character(long$family_role_f)) {
    c("index", "sibling")
  } else {
    c("Indeks", "Kardes")
  }
  long$family_role_f <- factor(as.character(long$family_role_f), levels = role_levels)
  long$aile_no_f <- factor(as.character(long$aile_no_f))
  partner_term <- sprintf("group_fDM:family_role_f%s", role_levels[2])
  rows <- list()
  for (sub in h5_subscales()) {
    outcome <- sprintf("embu_c_%s_mean", sub)
    if (!outcome %in% names(long)) next
    formula_str <- sprintf("%s ~ group_f * family_role_f + (1 | aile_no_f)", outcome)
    fit <- tryCatch(
      suppressMessages(suppressWarnings(
        lme4::lmer(stats::as.formula(formula_str), data = long, REML = TRUE)
      )),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      rows[[length(rows) + 1L]] <- data.frame(
        subscale = sub, status = paste0("error:", conditionMessage(fit)),
        actor = NA_real_, partner = NA_real_, k = NA_real_,
        k_ci_lo = NA_real_, k_ci_hi = NA_real_, n_obs = NA_integer_,
        stringsAsFactors = FALSE
      )
      next
    }
    fixed <- lme4::fixef(fit)
    actor   <- unname(fixed["group_fDM"])
    partner <- unname(fixed[partner_term])
    k_point <- if (is.finite(actor) && actor != 0) partner / actor else NA_real_
    set.seed(seed)
    boot_k <- tryCatch(
      {
        valid <- numeric(0)
        families <- levels(long$aile_no_f)
        for (b in seq_len(n_boot)) {
          fams <- sample(families, replace = TRUE)
          idx <- unlist(lapply(fams, function(f) which(long$aile_no_f == f)))
          d <- long[idx, , drop = FALSE]
          d$aile_no_f <- factor(paste0(d$aile_no_f, "_", rep(seq_along(fams), lengths(lapply(fams, function(f) which(long$aile_no_f == f))))))
          fit_b <- suppressMessages(suppressWarnings(tryCatch(
            lme4::lmer(stats::as.formula(formula_str), data = d, REML = TRUE,
                       control = lme4::lmerControl(check.conv.singular = "ignore")),
            error = function(e) NULL
          )))
          if (is.null(fit_b)) next
          fb <- lme4::fixef(fit_b)
          if (!"group_fDM" %in% names(fb) || !partner_term %in% names(fb)) next
          a <- unname(fb["group_fDM"]); p <- unname(fb[partner_term])
          if (is.finite(a) && a != 0) valid <- c(valid, p / a)
        }
        valid
      },
      error = function(e) numeric(0)
    )
    ci <- if (length(boot_k) >= 50L) stats::quantile(boot_k, c(0.025, 0.975), na.rm = TRUE) else c(NA_real_, NA_real_)
    rows[[length(rows) + 1L]] <- data.frame(
      subscale = sub, status = "fit_ok",
      actor = actor, partner = partner,
      k = k_point,
      k_ci_lo = unname(ci[1]),
      k_ci_hi = unname(ci[2]),
      n_obs = stats::nobs(fit),
      n_boot_valid = length(boot_k),
      stringsAsFactors = FALSE
    )
  }
  list(table = do.call(rbind, rows))
}

# === Klinik tutarsızlık örüntüleri (SAP §16.7) =========================

h5_inconsistency_patterns <- function(df) {
  rows <- list()
  pattern_specs <- list(
    list(name = "anne_high_child_low_warmth",
         desc = "Anne sıcak Çocuk düşük (savunmacılık)",
         a = "embu_p_sicaklik_mean", b = "embu_c_idx_sicaklik_mean", direction = "a_minus_b", threshold = 0.5),
    list(name = "anne_low_child_high_rejection",
         desc = "Anne reddetme düşük Çocuk yüksek (öz-eleştiri yokluğu)",
         a = "embu_c_idx_reddetme_mean", b = "embu_p_reddetme_mean", direction = "a_minus_b", threshold = 0.5),
    list(name = "differential_parental_treatment",
         desc = "İndeks-Kardeş arası fark (DPT)",
         a = "embu_c_idx_sicaklik_mean", b = "embu_c_sib_sicaklik_mean", direction = "abs_diff", threshold = 0.5)
  )
  for (sp in pattern_specs) {
    for (grp in c("Kontrol", "DM")) {
      d <- df[df$group_f == grp, c(sp$a, sp$b), drop = FALSE]
      d <- d[stats::complete.cases(d), , drop = FALSE]
      n <- nrow(d)
      if (n == 0L) next
      diffs <- if (sp$direction == "a_minus_b") d[[sp$a]] - d[[sp$b]] else abs(d[[sp$a]] - d[[sp$b]])
      flag <- diffs > sp$threshold
      rows[[length(rows) + 1L]] <- data.frame(
        pattern    = sp$name,
        description = sp$desc,
        group      = grp,
        n          = n,
        n_flagged  = sum(flag, na.rm = TRUE),
        prop_flagged = mean(flag, na.rm = TRUE),
        median_diff  = stats::median(diffs, na.rm = TRUE),
        threshold  = sp$threshold,
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

# === Pipeline orchestrator =============================================

run_h5_dyadic_concordance_pipeline <- function(df_family_ses, df_family_scored, df_long_scored,
                                                run_rsa = TRUE, run_cfa = TRUE,
                                                run_k = TRUE, n_boot = 500L) {
  prepared <- h5_prepare_frame(df_family_ses)
  s1 <- h5_strategy1_icc_bland_altman(prepared)
  s2 <- if (run_rsa) h5_strategy2_rsa(prepared) else list(status = data.frame(status = "skipped"), parameters = data.frame())
  s3 <- h5_strategy3_common_fate(prepared)
  s4 <- if (run_cfa) {
    h5_strategy4_dyadic_cfa(df_family_scored, prepared[, c("aile_no", "group_f")])
  } else {
    list(status = data.frame(group = NA_character_, status = "skipped", stringsAsFactors = FALSE))
  }
  s5 <- if (run_k) h5_strategy5_k_coefficient(df_long_scored, n_boot = n_boot) else list(table = data.frame(status = "skipped"))
  patterns <- h5_inconsistency_patterns(prepared)

  target_summary <- data.frame(
    component = c("Strateji_1_ICC_BA", "Strateji_2_RSA", "Strateji_3_CFM",
                  "Strateji_4_DyadicCFA", "Strateji_5_kCoefficient",
                  "Inconsistency_Patterns"),
    n_rows = c(nrow(s1),
               if (is.data.frame(s2$status)) nrow(s2$status) else 0L,
               nrow(s3$status),
               if (is.data.frame(s4$status)) nrow(s4$status) else 0L,
               if (!is.null(s5$table) && is.data.frame(s5$table)) nrow(s5$table) else 0L,
               nrow(patterns)),
    stringsAsFactors = FALSE
  )

  list(
    icc_bland_altman_table          = s1,
    rsa_status_table                = s2$status,
    rsa_parameters_table            = s2$parameters,
    common_fate_status_table        = s3$status,
    common_fate_fit_measures_table  = s3$fit_measures,
    common_fate_loadings_table      = s3$loadings,
    common_fate_regressions_table   = s3$regressions,
    dyadic_cfa_status_table         = s4$status,
    dyadic_cfa_fit_measures_table   = if (!is.null(s4$fit_measures)) s4$fit_measures else data.frame(),
    dyadic_cfa_latent_corr_table    = if (!is.null(s4$latent_correlations)) s4$latent_correlations else data.frame(),
    k_coefficient_table             = s5$table,
    inconsistency_patterns_table    = patterns,
    target_summary                  = target_summary
  )
}
