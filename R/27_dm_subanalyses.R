# KISIM X — DM-only Klinik Alt-Analizler
# 30. HbA1c × ebeveynlik etkileşimi
# 31. DM süresi spline modeli
# 32. Tanı yaşı stratifikasyonu (3 strata)
#
# DM-only frame (n_dm=120, n_hba1c=39 keşifsel).
# Kural #19: HbA1c için imputation YAPILMAZ; eksiklik açıkça raporlanır.

dm_prepare_frame <- function(df_family_ses) {
  df <- df_family_ses[df_family_ses$group_f == "DM", , drop = FALSE]
  df$anne_yas_z   <- as.numeric(scale(df$anne_yas))
  df$ses_latent_z <- as.numeric(scale(df$ses_latent))
  df$cocuk_yas_z  <- as.numeric(scale(df$cocuk_yas))
  df$tani_yasi_strata <- factor(
    cut(df$tani_yasi, breaks = c(-Inf, 5, 10, Inf),
        labels = c("erken_<5y", "okul_5-10y", "ergen_>=10y"),
        right = FALSE),
    levels = c("erken_<5y", "okul_5-10y", "ergen_>=10y")
  )
  df
}

dm_n_summary <- function(df) {
  data.frame(
    metric = c("n_dm_total", "n_with_hba1c", "n_with_dm_yili", "n_with_tani_yasi",
               "median_dm_yili", "median_hba1c", "median_tani_yasi"),
    value  = c(
      nrow(df),
      sum(!is.na(df$hba1c)),
      sum(!is.na(df$dm_yili)),
      sum(!is.na(df$tani_yasi)),
      stats::median(df$dm_yili, na.rm = TRUE),
      stats::median(df$hba1c, na.rm = TRUE),
      stats::median(df$tani_yasi, na.rm = TRUE)
    ),
    stringsAsFactors = FALSE
  )
}

# === 30. HbA1c × parenting interaction =================================

dm_hba1c_interaction <- function(df, outcome_col = "embu_p_asiri_koruma_mean") {
  sub_df <- df[!is.na(df$hba1c) & !is.na(df[[outcome_col]]), , drop = FALSE]
  if (nrow(sub_df) < 20L) {
    return(data.frame(outcome = outcome_col, status = "insufficient_n",
                      n = nrow(sub_df), stringsAsFactors = FALSE))
  }
  formula_main <- stats::as.formula(sprintf("%s ~ hba1c + anne_yas_z + ses_latent_z + cocuk_yas_z", outcome_col))
  fit_main <- stats::lm(formula_main, data = sub_df)
  cs <- summary(fit_main)$coefficients
  hba1c_idx <- grep("hba1c", rownames(cs))[1]
  data.frame(
    outcome = outcome_col,
    status  = "ok",
    n       = nrow(sub_df),
    median_hba1c = stats::median(sub_df$hba1c),
    estimate = cs[hba1c_idx, 1],
    se       = cs[hba1c_idx, 2],
    t_value  = cs[hba1c_idx, 3],
    p_value  = cs[hba1c_idx, 4],
    r_squared = summary(fit_main)$r.squared,
    stringsAsFactors = FALSE
  )
}

# === 31. DM süresi spline =============================================

dm_duration_spline <- function(df, outcome_col = "embu_p_asiri_koruma_mean") {
  if (!requireNamespace("splines", quietly = TRUE)) {
    return(data.frame(outcome = outcome_col, status = "splines_unavailable",
                      stringsAsFactors = FALSE))
  }
  sub_df <- df[!is.na(df$dm_yili) & !is.na(df[[outcome_col]]), , drop = FALSE]
  if (nrow(sub_df) < 30L) {
    return(data.frame(outcome = outcome_col, status = "insufficient_n",
                      n = nrow(sub_df), stringsAsFactors = FALSE))
  }
  formula_lin <- stats::as.formula(sprintf("%s ~ dm_yili + anne_yas_z + ses_latent_z", outcome_col))
  formula_spl <- stats::as.formula(sprintf("%s ~ splines::ns(dm_yili, df = 3) + anne_yas_z + ses_latent_z", outcome_col))
  fit_lin <- stats::lm(formula_lin, data = sub_df)
  fit_spl <- stats::lm(formula_spl, data = sub_df)
  lrt <- stats::anova(fit_lin, fit_spl)
  data.frame(
    outcome = outcome_col,
    status  = "ok",
    n       = nrow(sub_df),
    median_dm_yili = stats::median(sub_df$dm_yili),
    linear_r2 = summary(fit_lin)$r.squared,
    spline_r2 = summary(fit_spl)$r.squared,
    lrt_F     = lrt[2, "F"],
    lrt_p     = lrt[2, "Pr(>F)"],
    interpretation = if (!is.na(lrt[2, "Pr(>F)"]) && lrt[2, "Pr(>F)"] < 0.05) {
      "nonlinear_effect"
    } else "linear_sufficient",
    stringsAsFactors = FALSE
  )
}

# === 32. Diagnostic age strata =========================================

dm_strata_analysis <- function(df, outcome_col = "embu_p_asiri_koruma_mean") {
  rows <- list()
  for (stratum in levels(df$tani_yasi_strata)) {
    sub <- df[df$tani_yasi_strata == stratum & !is.na(df[[outcome_col]]), , drop = FALSE]
    if (nrow(sub) < 5L) {
      rows[[length(rows) + 1L]] <- data.frame(
        stratum = stratum, outcome = outcome_col,
        n = nrow(sub), mean = NA_real_, sd = NA_real_,
        median = NA_real_, status = "insufficient_n",
        stringsAsFactors = FALSE
      )
      next
    }
    rows[[length(rows) + 1L]] <- data.frame(
      stratum = stratum, outcome = outcome_col,
      n = nrow(sub),
      mean   = mean(sub[[outcome_col]], na.rm = TRUE),
      sd     = stats::sd(sub[[outcome_col]], na.rm = TRUE),
      median = stats::median(sub[[outcome_col]], na.rm = TRUE),
      status = "ok",
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

dm_strata_test <- function(df, outcome_col) {
  sub_df <- df[!is.na(df[[outcome_col]]) & !is.na(df$tani_yasi_strata), , drop = FALSE]
  if (nrow(sub_df) < 15L) {
    return(data.frame(outcome = outcome_col, status = "insufficient_n",
                      n = nrow(sub_df), stringsAsFactors = FALSE))
  }
  formula_str <- stats::as.formula(sprintf("%s ~ tani_yasi_strata + anne_yas_z + ses_latent_z", outcome_col))
  fit <- stats::lm(formula_str, data = sub_df)
  ano <- stats::anova(fit)
  data.frame(
    outcome = outcome_col,
    status  = "ok",
    n       = nrow(sub_df),
    F_value = ano["tani_yasi_strata", "F value"],
    p_value = ano["tani_yasi_strata", "Pr(>F)"],
    eta_partial = ano["tani_yasi_strata", "Sum Sq"] / sum(ano[, "Sum Sq"]),
    stringsAsFactors = FALSE
  )
}

# === Pipeline orchestrator =============================================

run_dm_subanalyses_pipeline <- function(df_family_ses) {
  prepared <- dm_prepare_frame(df_family_ses)
  n_summary <- dm_n_summary(prepared)
  outcomes <- c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
                "embu_p_reddetme_mean", "embu_p_karsilastirma_mean",
                "beck_total")
  hba1c_table <- do.call(rbind, lapply(outcomes, function(o) dm_hba1c_interaction(prepared, o)))
  spline_table <- do.call(rbind, lapply(outcomes, function(o) dm_duration_spline(prepared, o)))
  strata_descriptive <- do.call(rbind, lapply(outcomes, function(o) dm_strata_analysis(prepared, o)))
  strata_tests <- do.call(rbind, lapply(outcomes, function(o) dm_strata_test(prepared, o)))
  list(
    n_summary_table        = n_summary,
    hba1c_interaction_table = hba1c_table,
    spline_duration_table   = spline_table,
    strata_descriptive_table = strata_descriptive,
    strata_tests_table      = strata_tests
  )
}
