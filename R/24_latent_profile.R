# KISIM VII — Latent Değişken Yöntemleri
# 21. Latent Profile Analysis (LPA) — anne tipolojisi
# 22. Latent Class Analysis + Mixture Regression
# 23. Bifactor S-1 modeli (referans plan; uygulama tidyLPA + lavaan)
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

# === LCA + Mixture Regression sensitivity ===============================

lca_indicators <- function() {
  c("lca_beck_cat",
    "lca_sicaklik_cat", "lca_asiri_koruma_cat",
    "lca_reddetme_cat", "lca_karsilastirma_cat",
    "lca_ses_cat")
}

lca_indicator_label_map <- function() {
  list(
    lca_beck_cat          = c("minimal", "hafif", "orta_siddetli"),
    lca_sicaklik_cat      = c("dusuk", "orta", "yuksek"),
    lca_asiri_koruma_cat  = c("dusuk", "orta", "yuksek"),
    lca_reddetme_cat      = c("dusuk", "orta", "yuksek"),
    lca_karsilastirma_cat = c("dusuk", "orta", "yuksek"),
    lca_ses_cat           = c("dusuk", "orta", "yuksek")
  )
}

lca_indicator_sources <- function() {
  data.frame(
    indicator = lca_indicators(),
    source = c("beck_severity",
               "embu_p_sicaklik_mean",
               "embu_p_asiri_koruma_mean",
               "embu_p_reddetme_mean",
               "embu_p_karsilastirma_mean",
               "ses_latent"),
    method = c("BDI severity collapsed: minimal / mild / moderate-severe",
               rep("sample tertiles; sensitivity categorization", 5)),
    stringsAsFactors = FALSE
  )
}

lca_tertile_code <- function(x) {
  out <- rep(NA_integer_, length(x))
  ok <- is.finite(x)
  if (sum(ok) == 0L) return(out)
  q <- stats::quantile(x[ok], probs = c(0, 1 / 3, 2 / 3, 1),
                       na.rm = TRUE, names = FALSE, type = 7)
  if (length(unique(q)) < 4L) {
    ranked <- rank(x[ok], ties.method = "average", na.last = "keep")
    q <- stats::quantile(ranked, probs = c(0, 1 / 3, 2 / 3, 1),
                         na.rm = TRUE, names = FALSE, type = 7)
    out[ok] <- as.integer(cut(ranked, breaks = unique(q),
                              include.lowest = TRUE, labels = FALSE))
  } else {
    out[ok] <- as.integer(cut(x[ok], breaks = q, include.lowest = TRUE,
                              labels = FALSE))
  }
  out
}

lca_beck_code <- function(x) {
  y <- as.character(x)
  out <- rep(NA_integer_, length(y))
  out[y == "Minimal"] <- 1L
  out[y == "Hafif"] <- 2L
  out[y %in% c("Orta", "Siddetli")] <- 3L
  out
}

lca_z <- function(x) {
  as.numeric(scale(x))
}

lca_prepare_frame <- function(df_family_ses) {
  source_cols <- unique(c(
    "aile_no", "group_f", "beck_severity",
    "embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
    "embu_p_reddetme_mean", "embu_p_karsilastirma_mean",
    "ses_latent", "anne_yas", "cocuk_sayisi", "age_gap"
  ))
  missing_cols <- setdiff(source_cols, names(df_family_ses))
  if (length(missing_cols) > 0L) {
    stop(sprintf("LCA frame missing: %s", paste(missing_cols, collapse = ", ")))
  }
  df <- df_family_ses[, source_cols, drop = FALSE]
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  df$group_dm <- as.integer(df$group_f == "DM")
  df$lca_beck_cat <- lca_beck_code(df$beck_severity)
  df$lca_sicaklik_cat <- lca_tertile_code(df$embu_p_sicaklik_mean)
  df$lca_asiri_koruma_cat <- lca_tertile_code(df$embu_p_asiri_koruma_mean)
  df$lca_reddetme_cat <- lca_tertile_code(df$embu_p_reddetme_mean)
  df$lca_karsilastirma_cat <- lca_tertile_code(df$embu_p_karsilastirma_mean)
  df$lca_ses_cat <- lca_tertile_code(df$ses_latent)
  df$anne_yas_z <- lca_z(df$anne_yas)
  df$cocuk_sayisi_z <- lca_z(df$cocuk_sayisi)
  df$age_gap_z <- lca_z(df$age_gap)

  indicator_cols <- lca_indicators()
  mixture_cols <- c(indicator_cols, "group_f", "anne_yas_z",
                    "cocuk_sayisi_z", "age_gap_z")
  list(
    full = df,
    complete_indicators = df[stats::complete.cases(df[, indicator_cols, drop = FALSE]), , drop = FALSE],
    complete_mixture = df[stats::complete.cases(df[, mixture_cols, drop = FALSE]), , drop = FALSE],
    n_full = nrow(df),
    n_complete_indicators = sum(stats::complete.cases(df[, indicator_cols, drop = FALSE])),
    n_complete_mixture = sum(stats::complete.cases(df[, mixture_cols, drop = FALSE]))
  )
}

lca_indicator_audit <- function(lca_frame) {
  sources <- lca_indicator_sources()
  labels <- lca_indicator_label_map()
  rows <- list()
  for (ind in lca_indicators()) {
    tab <- table(lca_frame[[ind]], useNA = "ifany")
    for (i in seq_along(tab)) {
      nm <- names(tab)[i]
      level_num <- suppressWarnings(as.integer(nm))
      level_label <- if (is.na(level_num)) NA_character_ else labels[[ind]][level_num]
      rows[[length(rows) + 1L]] <- data.frame(
        indicator = ind,
        source = sources$source[match(ind, sources$indicator)],
        method = sources$method[match(ind, sources$indicator)],
        level = nm,
        level_label = level_label,
        n = as.integer(tab[i]),
        pct = as.integer(tab[i]) / nrow(lca_frame),
        missing_n = sum(is.na(lca_frame[[ind]])),
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

lca_entropy <- function(posterior) {
  if (is.null(posterior) || ncol(posterior) <= 1L) return(NA_real_)
  p <- as.matrix(posterior)
  p[p <= 0] <- NA_real_
  entropy_raw <- -sum(p * log(p), na.rm = TRUE)
  1 - entropy_raw / (nrow(p) * log(ncol(p)))
}

run_lca <- function(df_family_ses, class_range = 1:4,
                    seed = 20260428L, nrep = 30L, maxiter = 3000L) {
  if (!requireNamespace("poLCA", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  prep <- lca_prepare_frame(df_family_ses)
  lca_df <- prep$complete_indicators
  indicator_cols <- lca_indicators()
  if (nrow(lca_df) < 100L) {
    return(list(status = "insufficient_complete_cases",
                indicator_audit_table = lca_indicator_audit(prep$full)))
  }
  form <- stats::as.formula(
    paste0("cbind(", paste(indicator_cols, collapse = ", "), ") ~ 1")
  )
  fits <- list()
  fit_rows <- list()
  for (k in class_range) {
    set.seed(seed + as.integer(k))
    fit <- tryCatch(
      suppressWarnings(poLCA::poLCA(
        form, data = lca_df, nclass = k, nrep = nrep,
        maxiter = maxiter, verbose = FALSE, calc.se = FALSE,
        graphs = FALSE, na.rm = TRUE
      )),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      fit_rows[[length(fit_rows) + 1L]] <- data.frame(
        nclass = k, status = paste0("error:", conditionMessage(fit)),
        logLik = NA_real_, aic = NA_real_, bic = NA_real_,
        g_sq = NA_real_, chisq = NA_real_, npar = NA_real_,
        nobs = nrow(lca_df), min_class_prop = NA_real_, entropy = NA_real_,
        stringsAsFactors = FALSE
      )
      next
    }
    fits[[as.character(k)]] <- fit
    fit_rows[[length(fit_rows) + 1L]] <- data.frame(
      nclass = k,
      status = "ok",
      logLik = fit$llik,
      aic = fit$aic,
      bic = fit$bic,
      g_sq = fit$Gsq,
      chisq = fit$Chisq,
      npar = fit$npar,
      nobs = fit$N,
      min_class_prop = min(fit$P),
      entropy = lca_entropy(fit$posterior),
      stringsAsFactors = FALSE
    )
  }
  fit_table <- do.call(rbind, fit_rows)
  ok_rows <- fit_table[fit_table$status == "ok" & is.finite(fit_table$bic), , drop = FALSE]
  if (nrow(ok_rows) == 0L) {
    return(list(status = "all_models_failed",
                indicator_audit_table = lca_indicator_audit(prep$full),
                fit_table = fit_table))
  }
  best_n <- ok_rows$nclass[which.min(ok_rows$bic)]
  best_fit <- fits[[as.character(best_n)]]

  classes <- table(best_fit$predclass, useNA = "ifany")
  classes_table <- data.frame(
    class_id = names(classes),
    n = as.integer(classes),
    pct = as.numeric(classes) / sum(classes),
    stringsAsFactors = FALSE
  )

  label_map <- lca_indicator_label_map()
  prob_rows <- list()
  for (ind in names(best_fit$probs)) {
    mat <- best_fit$probs[[ind]]
    for (level_idx in seq_len(nrow(mat))) {
      for (class_idx in seq_len(ncol(mat))) {
        prob_rows[[length(prob_rows) + 1L]] <- data.frame(
          class_id = as.character(class_idx),
          indicator = ind,
          level = as.character(level_idx),
          level_label = label_map[[ind]][level_idx],
          probability = as.numeric(mat[level_idx, class_idx]),
          stringsAsFactors = FALSE
        )
      }
    }
  }
  item_response_prob_table <- if (length(prob_rows) > 0L) {
    do.call(rbind, prob_rows)
  } else data.frame()

  lca_df$class_id <- factor(best_fit$predclass, levels = seq_len(best_n))
  group_counts <- as.data.frame(table(lca_df$group_f, lca_df$class_id))
  names(group_counts) <- c("group", "class_id", "n")
  group_counts$pct_within_group <- ave(group_counts$n, group_counts$group,
                                       FUN = function(x) x / sum(x))

  list(
    status = "ok",
    frame = prep,
    fit_table = fit_table,
    best_n = best_n,
    best_model = best_fit,
    classes_table = classes_table,
    item_response_prob_table = item_response_prob_table,
    group_distribution_table = group_counts,
    indicator_audit_table = lca_indicator_audit(prep$full)
  )
}

run_lca_modal_regression <- function(lca_res) {
  if (!requireNamespace("nnet", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  if (is.null(lca_res$status) || lca_res$status != "ok" ||
      is.null(lca_res$best_model) || is.null(lca_res$frame)) {
    return(list(status = "lca_not_available"))
  }
  reg_df <- lca_res$frame$complete_indicators
  reg_df$lca_class <- factor(lca_res$best_model$predclass)
  reg_df <- reg_df[stats::complete.cases(reg_df[, c("lca_class", "group_f",
                                                    "anne_yas_z", "cocuk_sayisi_z",
                                                    "age_gap_z"), drop = FALSE]), , drop = FALSE]
  if (nlevels(reg_df$lca_class) < 2L || nrow(reg_df) < 100L) {
    return(list(status = "insufficient_class_variation"))
  }
  fit <- tryCatch(
    suppressWarnings(nnet::multinom(
      lca_class ~ group_f + anne_yas_z + cocuk_sayisi_z + age_gap_z,
      data = reg_df, trace = FALSE, maxit = 1000
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = paste0("error:", conditionMessage(fit))))
  }
  co <- coef(fit)
  se <- summary(fit)$standard.errors
  if (is.null(dim(co))) {
    co <- matrix(co, nrow = 1L, dimnames = list(levels(reg_df$lca_class)[2], names(co)))
    se <- matrix(se, nrow = 1L, dimnames = dimnames(co))
  }
  rows <- list()
  for (contrast in rownames(co)) {
    for (term in colnames(co)) {
      estimate <- co[contrast, term]
      stderr <- se[contrast, term]
      z <- estimate / stderr
      p <- 2 * stats::pnorm(abs(z), lower.tail = FALSE)
      rows[[length(rows) + 1L]] <- data.frame(
        model = "modal_class_multinomial",
        class_contrast = paste0(contrast, "_vs_reference"),
        term = term,
        estimate = estimate,
        se = stderr,
        z = z,
        p_value = p,
        odds_ratio = exp(estimate),
        or_low = exp(estimate - 1.96 * stderr),
        or_high = exp(estimate + 1.96 * stderr),
        n = nrow(reg_df),
        stringsAsFactors = FALSE
      )
    }
  }
  list(status = "ok", regression_table = do.call(rbind, rows), model = fit)
}

run_flexmix_regression <- function(df_family_ses, k = 2L, seed = 20260428L) {
  if (!requireNamespace("flexmix", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  cols <- c("group_f", "beck_total", "ses_latent", "embu_p_reddetme_mean")
  missing_cols <- setdiff(cols, names(df_family_ses))
  if (length(missing_cols) > 0L) {
    return(list(status = paste0("missing:", paste(missing_cols, collapse = ","))))
  }
  df <- df_family_ses[, cols, drop = FALSE]
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  df$beck_total_z <- lca_z(df$beck_total)
  df$ses_latent_z <- lca_z(df$ses_latent)
  df <- df[stats::complete.cases(df[, c("group_f", "beck_total_z",
                                        "ses_latent_z", "embu_p_reddetme_mean")]), , drop = FALSE]
  if (nrow(df) < 100L) return(list(status = "insufficient_complete_cases"))
  set.seed(seed)
  fit <- tryCatch(
    suppressWarnings(flexmix::flexmix(
      embu_p_reddetme_mean ~ beck_total_z + ses_latent_z,
      data = df,
      k = k,
      model = flexmix::FLXMRglm(family = "gaussian"),
      concomitant = flexmix::FLXPmultinom(~ group_f),
      control = list(verbose = 0, iter.max = 500)
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = paste0("error:", conditionMessage(fit))))
  }
  param <- tryCatch(flexmix::parameters(fit), error = function(e) NULL)
  coef_table <- data.frame()
  if (!is.null(param)) {
    pmat <- as.matrix(param)
    coef_table <- data.frame(
      term = rep(rownames(pmat), times = ncol(pmat)),
      component = rep(colnames(pmat), each = nrow(pmat)),
      estimate = as.vector(pmat),
      stringsAsFactors = FALSE
    )
  }
  clusters <- flexmix::clusters(fit)
  class_distribution <- as.data.frame(table(clusters))
  names(class_distribution) <- c("component", "n")
  class_distribution$pct <- class_distribution$n / sum(class_distribution$n)
  group_distribution <- as.data.frame(table(df$group_f, clusters))
  names(group_distribution) <- c("group", "component", "n")
  group_distribution$pct_within_group <- ave(group_distribution$n, group_distribution$group,
                                             FUN = function(x) x / sum(x))
  loglik <- tryCatch(as.numeric(stats::logLik(fit)), error = function(e) as.numeric(slot(fit, "logLik")))
  df_model <- tryCatch(as.numeric(slot(fit, "df")), error = function(e) NA_real_)
  aic <- tryCatch(stats::AIC(fit), error = function(e) if (is.finite(df_model)) -2 * loglik + 2 * df_model else NA_real_)
  bic <- tryCatch(stats::BIC(fit), error = function(e) if (is.finite(df_model)) -2 * loglik + log(nrow(df)) * df_model else NA_real_)
  fit_table <- data.frame(
    model = "flexmix_gaussian_rejection_on_beck_ses",
    k = k,
    n = nrow(df),
    logLik = loglik,
    aic = aic,
    bic = bic,
    converged = fit@converged,
    status = if (isTRUE(fit@converged)) "ok" else "boundary_solution",
    stringsAsFactors = FALSE
  )
  list(
    status = fit_table$status[1],
    fit_table = fit_table,
    coefficient_table = coef_table,
    class_distribution_table = class_distribution,
    group_distribution_table = group_distribution,
    model = fit
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
    tidyLPA::get_data(best_model),
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
                                         lca_class_range = 1:4,
                                         run_bifactor = TRUE,
                                         run_lca_sensitivity = TRUE,
                                         run_flexmix_sensitivity = TRUE,
                                         seed = 20260428L) {
  lpa_res <- run_lpa(df_family_ses, profile_range = profile_range, seed = seed)
  lca_res <- if (run_lca_sensitivity) {
    run_lca(df_family_ses, class_range = lca_class_range, seed = seed)
  } else list(status = "skipped")
  lca_modal_res <- if (isTRUE(run_lca_sensitivity)) {
    run_lca_modal_regression(lca_res)
  } else list(status = "skipped")
  flexmix_res <- if (run_flexmix_sensitivity) {
    run_flexmix_regression(df_family_ses, k = 2L, seed = seed)
  } else list(status = "skipped")
  bifactor_res <- if (run_bifactor) {
    run_bifactor_s1(df_family_scored, target_subscale = "asiri_koruma")
  } else list(status = "skipped")
  status_table <- data.frame(
    component = c("LPA", "LCA", "LCA_Modal_Regression",
                  "Flexmix_Mixture_Regression", "Bifactor_S1"),
    status    = c(lpa_res$status, lca_res$status, lca_modal_res$status,
                  flexmix_res$status, bifactor_res$status),
    stringsAsFactors = FALSE
  )
  list(
    status_table             = status_table,
    lpa_fit_table            = if (!is.null(lpa_res$fit_table)) lpa_res$fit_table else data.frame(),
    lpa_classes_table        = if (!is.null(lpa_res$classes_table)) lpa_res$classes_table else data.frame(),
    lpa_profile_means_table  = if (!is.null(lpa_res$profile_means_table)) lpa_res$profile_means_table else data.frame(),
    lpa_group_distribution   = if (!is.null(lpa_res$group_distribution_table)) lpa_res$group_distribution_table else data.frame(),
    lpa_best_n               = if (!is.null(lpa_res$best_n)) lpa_res$best_n else NA_integer_,
    lca_indicator_audit_table = if (!is.null(lca_res$indicator_audit_table)) lca_res$indicator_audit_table else data.frame(),
    lca_fit_table             = if (!is.null(lca_res$fit_table)) lca_res$fit_table else data.frame(),
    lca_classes_table         = if (!is.null(lca_res$classes_table)) lca_res$classes_table else data.frame(),
    lca_item_response_prob_table = if (!is.null(lca_res$item_response_prob_table)) lca_res$item_response_prob_table else data.frame(),
    lca_group_distribution    = if (!is.null(lca_res$group_distribution_table)) lca_res$group_distribution_table else data.frame(),
    lca_best_n                = if (!is.null(lca_res$best_n)) lca_res$best_n else NA_integer_,
    lca_modal_regression_table = if (!is.null(lca_modal_res$regression_table)) lca_modal_res$regression_table else data.frame(),
    flexmix_fit_table         = if (!is.null(flexmix_res$fit_table)) flexmix_res$fit_table else data.frame(),
    flexmix_coefficient_table = if (!is.null(flexmix_res$coefficient_table)) flexmix_res$coefficient_table else data.frame(),
    flexmix_class_distribution = if (!is.null(flexmix_res$class_distribution_table)) flexmix_res$class_distribution_table else data.frame(),
    flexmix_group_distribution = if (!is.null(flexmix_res$group_distribution_table)) flexmix_res$group_distribution_table else data.frame(),
    bifactor_fit_table       = if (!is.null(bifactor_res$fit_table)) bifactor_res$fit_table else data.frame(),
    bifactor_loadings_table  = if (!is.null(bifactor_res$general_loadings_table)) bifactor_res$general_loadings_table else data.frame()
  )
}
