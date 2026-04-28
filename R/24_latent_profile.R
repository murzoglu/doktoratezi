# KISIM VII — Latent Değişken Yöntemleri
# 21. Latent Profile Analysis (LPA) — anne tipolojisi
# 22. Bifactor S-1 modeli (referans plan; uygulama tidyLPA + EFAtools)
# Akogul-Erisoglu (2017) seçim kriterleri: BIC + entropy + LMR-LRT + BLRT.

lpa_indicators <- function() {
  c("beck_total",
    "embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
    "embu_p_reddetme_mean", "embu_p_karsilastirma_mean",
    "ses_latent")
}

lpa_prepare_frame <- function(df_family_ses) {
  cols <- c("aile_no", "group_f", lpa_indicators())
  missing_cols <- setdiff(cols, names(df_family_ses))
  if (length(missing_cols) > 0L) {
    stop(sprintf("LPA frame missing: %s", paste(missing_cols, collapse = ", ")))
  }
  df <- df_family_ses[, cols, drop = FALSE]
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  df_complete <- df[stats::complete.cases(df), , drop = FALSE]
  list(
    full = df,
    complete = df_complete,
    n_full = nrow(df),
    n_complete = nrow(df_complete)
  )
}

run_lpa <- function(df_family_ses, profile_range = 1:6,
                    seed = 20260428L) {
  if (!requireNamespace("tidyLPA", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  prep <- lpa_prepare_frame(df_family_ses)
  scaled <- as.data.frame(scale(prep$complete[, lpa_indicators()]))
  set.seed(seed)
  ep <- tryCatch(
    suppressMessages(suppressWarnings(
      tidyLPA::estimate_profiles(scaled, n_profiles = profile_range,
                                  variances = "equal",
                                  covariances = "zero")
    )),
    error = function(e) e
  )
  if (inherits(ep, "error")) {
    return(list(status = paste0("error:", conditionMessage(ep))))
  }
  fits_summary <- tryCatch(
    tidyLPA::get_fit(ep),
    error = function(e) NULL
  )
  if (is.null(fits_summary)) {
    return(list(status = "no_fit_summary"))
  }
  fits_df <- as.data.frame(fits_summary)
  best_idx <- which.min(fits_df$BIC)
  best_n <- fits_df$Classes[best_idx]
  best_model <- ep[[paste0("model_1_class_", best_n)]]
  if (is.null(best_model)) best_model <- ep[[best_idx]]
  data_with_class <- tryCatch(
    tidyLPA::get_data(ep),
    error = function(e) NULL
  )
  classes_table <- if (!is.null(data_with_class)) {
    if ("classes_number" %in% names(data_with_class)) {
      data_with_class <- data_with_class[data_with_class$classes_number == best_n, ]
    }
    counts <- table(data_with_class$Class, useNA = "ifany")
    data.frame(
      class_id = names(counts),
      n = as.integer(counts),
      pct = as.numeric(counts) / sum(counts),
      stringsAsFactors = FALSE
    )
  } else data.frame()

  profile_means <- if (!is.null(data_with_class)) {
    by_class <- split(data_with_class, data_with_class$Class)
    rows <- list()
    for (cl in names(by_class)) {
      d <- by_class[[cl]]
      for (ind in lpa_indicators()) {
        if (!ind %in% names(d)) next
        rows[[length(rows) + 1L]] <- data.frame(
          class_id  = cl,
          indicator = ind,
          mean      = mean(d[[ind]], na.rm = TRUE),
          sd        = stats::sd(d[[ind]], na.rm = TRUE),
          stringsAsFactors = FALSE
        )
      }
    }
    if (length(rows) > 0L) do.call(rbind, rows) else data.frame()
  } else data.frame()

  group_distribution <- if (!is.null(data_with_class) &&
                            "Class" %in% names(data_with_class)) {
    full_with_group <- prep$complete
    full_with_group$Class <- data_with_class$Class[match(rownames(prep$complete),
                                                          rownames(data_with_class))]
    counts <- table(full_with_group$group_f, full_with_group$Class, useNA = "ifany")
    df_counts <- as.data.frame(counts)
    names(df_counts) <- c("group", "class_id", "n")
    df_counts
  } else data.frame()

  list(
    status     = "ok",
    fit_table  = fits_df,
    best_n     = best_n,
    classes_table = classes_table,
    profile_means_table = profile_means,
    group_distribution_table = group_distribution,
    estimates = ep
  )
}

# === Bifactor S-1 preflight =============================================

run_bifactor_s1 <- function(df_family_scored, target_subscale = "asiri_koruma") {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  embu_subscale <- list(
    sicaklik = c(1, 3, 6, 7, 13, 17, 20, 24, 26),
    asiri_koruma = c(4, 8, 14, 15, 19, 23, 25),
    reddetme = c(5, 9, 10, 12, 16, 21, 22, 28),
    karsilastirma = c(2, 11, 18, 27, 29)
  )
  all_items <- unlist(embu_subscale)
  item_cols <- sprintf("embu_p_q%02d", all_items)
  if (!all(item_cols %in% names(df_family_scored))) {
    return(list(status = "items_missing"))
  }
  ref_factor <- target_subscale
  spec_factors <- setdiff(names(embu_subscale), ref_factor)
  general_loadings <- paste("g =~", paste(item_cols, collapse = " + "))
  spec_lines <- vapply(spec_factors, function(f) {
    items <- sprintf("embu_p_q%02d", embu_subscale[[f]])
    sprintf("%s =~ %s", f, paste(items, collapse = " + "))
  }, character(1))
  ortho_lines <- paste0("g ~~ 0*", spec_factors)
  pairs <- utils::combn(spec_factors, 2, simplify = FALSE)
  spec_ortho <- vapply(pairs, function(pr) sprintf("%s ~~ 0*%s", pr[1], pr[2]), character(1))
  model_str <- paste(c(general_loadings, spec_lines, ortho_lines, spec_ortho), collapse = "\n")
  fit <- tryCatch(
    suppressWarnings(lavaan::cfa(model_str, data = df_family_scored,
                                  ordered = item_cols, estimator = "WLSMV",
                                  std.lv = TRUE)),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = paste0("error:", conditionMessage(fit)), model_str = model_str))
  }
  fit_meas <- lavaan::fitMeasures(fit, c("cfi.scaled", "tli.scaled",
                                          "rmsea.scaled", "srmr",
                                          "chisq.scaled", "df.scaled",
                                          "pvalue.scaled"))
  pe <- lavaan::parameterEstimates(fit, standardized = TRUE)
  loadings <- pe[pe$op == "=~", ]
  fit_table <- data.frame(
    reference_factor = ref_factor,
    cfi   = unname(fit_meas[1]),
    tli   = unname(fit_meas[2]),
    rmsea = unname(fit_meas[3]),
    srmr  = unname(fit_meas[4]),
    chisq = unname(fit_meas[5]),
    df    = unname(fit_meas[6]),
    pvalue = unname(fit_meas[7]),
    stringsAsFactors = FALSE
  )
  general_loadings_df <- loadings[loadings$lhs == "g", c("rhs", "est", "se", "pvalue", "std.all")]
  list(
    status = "ok",
    fit_table = fit_table,
    general_loadings_table = general_loadings_df,
    full_loadings_table = loadings[, c("lhs", "rhs", "est", "se", "pvalue", "std.all")],
    model_str = model_str
  )
}

# === Pipeline orchestrator =============================================

run_latent_profile_pipeline <- function(df_family_ses, df_family_scored,
                                         profile_range = 1:5,
                                         run_bifactor = TRUE,
                                         seed = 20260428L) {
  lpa_res <- run_lpa(df_family_ses, profile_range = profile_range, seed = seed)
  bifactor_res <- if (run_bifactor) {
    run_bifactor_s1(df_family_scored, target_subscale = "asiri_koruma")
  } else list(status = "skipped")
  status_table <- data.frame(
    component = c("LPA", "Bifactor_S1"),
    status    = c(lpa_res$status, bifactor_res$status),
    stringsAsFactors = FALSE
  )
  list(
    status_table             = status_table,
    lpa_fit_table            = if (!is.null(lpa_res$fit_table)) lpa_res$fit_table else data.frame(),
    lpa_classes_table        = if (!is.null(lpa_res$classes_table)) lpa_res$classes_table else data.frame(),
    lpa_profile_means_table  = if (!is.null(lpa_res$profile_means_table)) lpa_res$profile_means_table else data.frame(),
    lpa_group_distribution   = if (!is.null(lpa_res$group_distribution_table)) lpa_res$group_distribution_table else data.frame(),
    lpa_best_n               = if (!is.null(lpa_res$best_n)) lpa_res$best_n else NA_integer_,
    bifactor_fit_table       = if (!is.null(bifactor_res$fit_table)) bifactor_res$fit_table else data.frame(),
    bifactor_loadings_table  = if (!is.null(bifactor_res$general_loadings_table)) bifactor_res$general_loadings_table else data.frame()
  )
}
