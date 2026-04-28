psychval_required_package <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    stop(sprintf("Required package is not installed: %s", package), call. = FALSE)
  }
}

psychval_embu_subscale_map <- function() {
  list(
    sicaklik = c(1, 3, 6, 7, 13, 17, 20, 24, 26),
    asiri_koruma = c(4, 8, 14, 15, 19, 23, 25),
    reddetme = c(5, 9, 10, 12, 16, 21, 22, 28),
    karsilastirma = c(2, 11, 18, 27, 29)
  )
}

psychval_subscale_labels <- function() {
  c(
    sicaklik = "Duygusal Sicaklik",
    asiri_koruma = "Asiri Koruma",
    reddetme = "Reddetme",
    karsilastirma = "Karsilastirma"
  )
}

psychval_item_columns <- function(prefix, items = 1:29) {
  paste0(prefix, "_q", sprintf("%02d", items))
}

psychval_srq_subscale_map <- function() {
  list(
    sicaklik_yakinlik = c(1, 8, 9, 11, 12, 14, 15, 17, 19, 20, 24, 25, 27, 28, 30, 31, 33, 40, 41, 46, 47),
    statu_guc = c(3, 4, 5, 6, 21, 22, 35, 36, 37, 38, 43, 44),
    catisma = c(10, 16, 26, 32, 42, 48),
    rekabet = c(2, 7, 13, 18, 23, 29, 34, 39, 45)
  )
}

psychval_srq_subscale_labels <- function() {
  c(
    sicaklik_yakinlik = "Sicaklik/Yakinlik",
    statu_guc = "Statu/Guc",
    catisma = "Catisma",
    rekabet = "Rekabet"
  )
}

psychval_srq_item_columns <- function(prefix, items = 1:48) {
  paste0(prefix, "_", items)
}

psychval_numeric_frame <- function(data, columns) {
  missing <- setdiff(columns, names(data))
  if (length(missing) > 0) {
    stop(sprintf("Missing required columns: %s", paste(missing, collapse = ", ")),
         call. = FALSE)
  }

  out <- data[columns]
  for (col in columns) {
    out[[col]] <- suppressWarnings(as.numeric(out[[col]]))
  }
  out
}

psychval_collapse_likert_frame <- function(data, columns,
                                           scheme = c("binary_floor", "upper_3cat")) {
  scheme <- match.arg(scheme)
  out <- psychval_numeric_frame(data, columns)

  for (col in columns) {
    values <- out[[col]]
    out[[col]] <- switch(
      scheme,
      binary_floor = ifelse(is.na(values), NA_real_, ifelse(values == 1, 1, 2)),
      upper_3cat = ifelse(is.na(values), NA_real_, pmin(values, 3))
    )
  }

  out
}

psychval_add_collapsed_likert <- function(data, columns,
                                          scheme = c("binary_floor", "upper_3cat")) {
  out <- data
  out[columns] <- psychval_collapse_likert_frame(data, columns, scheme = scheme)
  out
}

psychval_moment_skew <- function(x) {
  x <- x[!is.na(x)]
  if (length(x) < 3 || is.na(stats::sd(x)) || stats::sd(x) == 0) {
    return(NA_real_)
  }
  mean(((x - mean(x)) / stats::sd(x))^3)
}

psychval_moment_kurtosis <- function(x) {
  x <- x[!is.na(x)]
  if (length(x) < 4 || is.na(stats::sd(x)) || stats::sd(x) == 0) {
    return(NA_real_)
  }
  mean(((x - mean(x)) / stats::sd(x))^4) - 3
}

psychval_item_to_subscale <- function(columns, prefix) {
  map <- psychval_embu_subscale_map()
  item_lookup <- rep(names(map), lengths(map))
  names(item_lookup) <- psychval_item_columns(prefix, unlist(map, use.names = FALSE))
  unname(item_lookup[columns])
}

psychval_item_descriptives <- function(data, columns, item_min, item_max,
                                       form, prefix = NULL) {
  numeric_data <- psychval_numeric_frame(data, columns)
  rows <- lapply(columns, function(col) {
    values <- numeric_data[[col]]
    non_missing <- values[!is.na(values)]
    n <- length(non_missing)
    data.frame(
      form = form,
      subscale = if (is.null(prefix)) NA_character_ else psychval_item_to_subscale(col, prefix),
      item = col,
      n = n,
      missing_n = sum(is.na(values)),
      missing_pct = mean(is.na(values)) * 100,
      mean = if (n > 0) mean(non_missing) else NA_real_,
      sd = if (n > 1) stats::sd(non_missing) else NA_real_,
      median = if (n > 0) stats::median(non_missing) else NA_real_,
      iqr = if (n > 0) stats::IQR(non_missing) else NA_real_,
      min = if (n > 0) min(non_missing) else NA_real_,
      max = if (n > 0) max(non_missing) else NA_real_,
      skew = psychval_moment_skew(values),
      kurtosis = psychval_moment_kurtosis(values),
      floor_pct = mean(values == item_min, na.rm = TRUE) * 100,
      ceiling_pct = mean(values == item_max, na.rm = TRUE) * 100,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

psychval_score_subscales <- function(data, prefix, id_cols = character(),
                                     min_valid_ratio = 0.80) {
  map <- psychval_embu_subscale_map()
  keep_cols <- intersect(id_cols, names(data))
  out <- if (length(keep_cols) > 0) data[keep_cols] else data.frame(row_id = seq_len(nrow(data)))

  for (subscale in names(map)) {
    cols <- psychval_item_columns(prefix, map[[subscale]])
    numeric_items <- psychval_numeric_frame(data, cols)
    valid_n <- rowSums(!is.na(numeric_items))
    required_n <- ceiling(length(cols) * min_valid_ratio)
    means <- rowMeans(numeric_items, na.rm = TRUE)
    means[valid_n < required_n] <- NA_real_

    complete_sum <- rowSums(numeric_items)
    complete_sum[valid_n < length(cols)] <- NA_real_

    out[[paste0(subscale, "_valid_n")]] <- valid_n
    out[[paste0(subscale, "_mean")]] <- means
    out[[paste0(subscale, "_sum_complete")]] <- complete_sum
  }

  out
}

psychval_score_srq_subscales <- function(data, prefix = "srq", id_cols = character(),
                                         min_valid_ratio = 0.80) {
  map <- psychval_srq_subscale_map()
  keep_cols <- intersect(id_cols, names(data))
  out <- if (length(keep_cols) > 0) data[keep_cols] else data.frame(row_id = seq_len(nrow(data)))

  for (subscale in names(map)) {
    cols <- psychval_srq_item_columns(prefix, map[[subscale]])
    numeric_items <- psychval_numeric_frame(data, cols)
    valid_n <- rowSums(!is.na(numeric_items))
    required_n <- ceiling(length(cols) * min_valid_ratio)
    means <- rowMeans(numeric_items, na.rm = TRUE)
    means[valid_n < required_n] <- NA_real_

    complete_sum <- rowSums(numeric_items)
    complete_sum[valid_n < length(cols)] <- NA_real_

    out[[paste0(subscale, "_valid_n")]] <- valid_n
    out[[paste0(subscale, "_mean")]] <- means
    out[[paste0(subscale, "_sum_complete")]] <- complete_sum
  }

  out
}

psychval_safe_alpha <- function(items) {
  psychval_required_package("psych")
  result <- NULL
  suppressMessages(suppressWarnings(utils::capture.output(
    result <- tryCatch(
      psych::alpha(items, check.keys = FALSE, warnings = FALSE),
      error = function(e) e
    )
  )))
  result
}

psychval_alpha_ci <- function(alpha_raw, n_complete, n_items) {
  psychval_required_package("psych")
  if (is.na(alpha_raw) || is.na(n_complete) || n_complete < 4 || n_items < 2) {
    return(c(lower = NA_real_, upper = NA_real_))
  }

  ci <- tryCatch(
    psych::alpha.ci(alpha_raw, n.obs = n_complete, n.var = n_items, digits = 10),
    error = function(e) e
  )
  if (inherits(ci, "error")) {
    return(c(lower = NA_real_, upper = NA_real_))
  }

  c(lower = unname(ci$lower.ci), upper = unname(ci$upper.ci))
}

psychval_safe_omega <- function(items) {
  psychval_required_package("psych")
  complete_items <- items[stats::complete.cases(items), , drop = FALSE]
  if (ncol(complete_items) < 3 || nrow(complete_items) < ncol(complete_items) + 3) {
    return(list(omega_total = NA_real_, omega_h = NA_real_, omega_error = NA_character_))
  }

  result <- NULL
  suppressMessages(suppressWarnings(utils::capture.output(
    result <- tryCatch(
      psych::omega(complete_items, nfactors = 1, plot = FALSE),
      error = function(e) e
    )
  )))

  if (inherits(result, "error")) {
    return(list(
      omega_total = NA_real_,
      omega_h = NA_real_,
      omega_error = conditionMessage(result)
    ))
  }

  list(
    omega_total = unname(result[["omega.tot"]]),
    omega_h = unname(result[["omega_h"]]),
    omega_error = NA_character_
  )
}

psychval_reliability_table <- function(data, prefix, form) {
  map <- psychval_embu_subscale_map()
  rows <- lapply(names(map), function(subscale) {
    cols <- psychval_item_columns(prefix, map[[subscale]])
    items <- psychval_numeric_frame(data, cols)
    alpha <- psychval_safe_alpha(items)
    omega <- psychval_safe_omega(items)
    n_complete <- sum(stats::complete.cases(items))

    if (inherits(alpha, "error")) {
      alpha_raw <- NA_real_
      alpha_std <- NA_real_
      mean_interitem_r <- NA_real_
      alpha_error <- conditionMessage(alpha)
    } else {
      alpha_raw <- unname(alpha$total[["raw_alpha"]])
      alpha_std <- unname(alpha$total[["std.alpha"]])
      mean_interitem_r <- unname(alpha$total[["average_r"]])
      alpha_error <- NA_character_
    }

    alpha_ci <- psychval_alpha_ci(alpha_raw, n_complete, length(cols))

    data.frame(
      form = form,
      subscale = subscale,
      subscale_label = unname(psychval_subscale_labels()[subscale]),
      n_items = length(cols),
      n_complete = n_complete,
      alpha_raw = alpha_raw,
      alpha_std = alpha_std,
      alpha_ci_lower = unname(alpha_ci["lower"]),
      alpha_ci_upper = unname(alpha_ci["upper"]),
      omega_total = omega$omega_total,
      omega_h = omega$omega_h,
      mean_interitem_r = mean_interitem_r,
      alpha_error = alpha_error,
      omega_error = omega$omega_error,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

psychval_item_total_table <- function(data, prefix, form) {
  map <- psychval_embu_subscale_map()
  rows <- lapply(names(map), function(subscale) {
    cols <- psychval_item_columns(prefix, map[[subscale]])
    items <- psychval_numeric_frame(data, cols)
    alpha <- psychval_safe_alpha(items)

    if (inherits(alpha, "error")) {
      return(data.frame(
        form = form,
        subscale = subscale,
        item = cols,
        r_drop = NA_real_,
        r_cor = NA_real_,
        alpha_if_deleted = NA_real_,
        stringsAsFactors = FALSE
      ))
    }

    stats <- alpha$item.stats
    drops <- alpha$alpha.drop
    data.frame(
      form = form,
      subscale = subscale,
      item = rownames(stats),
      r_drop = unname(stats[, "r.drop"]),
      r_cor = unname(stats[, "r.cor"]),
      alpha_if_deleted = unname(drops[, "raw_alpha"]),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

psychval_beck_total <- function(data, prefix = "beck") {
  cols <- paste0(prefix, "_", 1:21)
  items <- psychval_numeric_frame(data, cols)
  totals <- rowSums(items)
  totals[rowSums(is.na(items)) > 0] <- NA_real_
  totals
}

psychval_srq_total_mean <- function(data, prefix = "srq", min_valid_ratio = 0.80) {
  cols <- paste0(prefix, "_", 1:48)
  items <- psychval_numeric_frame(data, cols)
  valid_n <- rowSums(!is.na(items))
  means <- rowMeans(items, na.rm = TRUE)
  means[valid_n < ceiling(length(cols) * min_valid_ratio)] <- NA_real_
  means
}

psychval_lavaan_model <- function(prefix,
                                  model = c("four_factor", "one_factor", "second_order", "bifactor"),
                                  exclude_items = integer()) {
  model <- match.arg(model)
  exclude_items <- as.integer(exclude_items)
  map <- lapply(psychval_embu_subscale_map(), function(items) {
    setdiff(items, exclude_items)
  })
  term <- function(items) paste(psychval_item_columns(prefix, items), collapse = " + ")
  all_items <- setdiff(1:29, exclude_items)

  four_factor <- paste(
    sprintf("sicaklik =~ %s", term(map$sicaklik)),
    sprintf("asiri_koruma =~ %s", term(map$asiri_koruma)),
    sprintf("reddetme =~ %s", term(map$reddetme)),
    sprintf("karsilastirma =~ %s", term(map$karsilastirma)),
    sep = "\n"
  )

  if (model == "four_factor") {
    return(four_factor)
  }

  if (model == "one_factor") {
    return(sprintf(
      "parenting =~ %s",
      paste(psychval_item_columns(prefix, all_items), collapse = " + ")
    ))
  }

  if (model == "second_order") {
    return(paste(
      four_factor,
      "parenting =~ sicaklik + asiri_koruma + reddetme + karsilastirma",
      sep = "\n"
    ))
  }

  factor_names <- names(map)
  zero_covs <- c(
    paste(sprintf("general ~~ 0*%s", factor_names), collapse = "\n"),
    "sicaklik ~~ 0*asiri_koruma",
    "sicaklik ~~ 0*reddetme",
    "sicaklik ~~ 0*karsilastirma",
    "asiri_koruma ~~ 0*reddetme",
    "asiri_koruma ~~ 0*karsilastirma",
    "reddetme ~~ 0*karsilastirma"
  )
  paste(
    sprintf("general =~ %s", paste(psychval_item_columns(prefix, all_items), collapse = " + ")),
    four_factor,
    paste(zero_covs, collapse = "\n"),
    sep = "\n"
  )
}

psychval_fit_indices <- function(fit, form, model_name) {
  measures <- c(
    "chisq.scaled", "df.scaled", "pvalue.scaled",
    "cfi.scaled", "tli.scaled", "rmsea.scaled",
    "rmsea.ci.lower.scaled", "rmsea.ci.upper.scaled",
    "srmr"
  )
  values <- tryCatch(
    lavaan::fitMeasures(fit, measures),
    error = function(e) stats::setNames(rep(NA_real_, length(measures)), measures)
  )

  data.frame(
    form = form,
    model = model_name,
    converged = isTRUE(lavaan::lavInspect(fit, "converged")),
    chisq_scaled = unname(values["chisq.scaled"]),
    df_scaled = unname(values["df.scaled"]),
    pvalue_scaled = unname(values["pvalue.scaled"]),
    cfi_scaled = unname(values["cfi.scaled"]),
    tli_scaled = unname(values["tli.scaled"]),
    rmsea_scaled = unname(values["rmsea.scaled"]),
    rmsea_ci_lower = unname(values["rmsea.ci.lower.scaled"]),
    rmsea_ci_upper = unname(values["rmsea.ci.upper.scaled"]),
    srmr = unname(values["srmr"]),
    error = NA_character_,
    stringsAsFactors = FALSE
  )
}

psychval_safe_cfa <- function(data, prefix, form, model_name,
                              group = NULL, cluster = NULL,
                              exclude_items = integer()) {
  psychval_required_package("lavaan")
  ordered <- psychval_item_columns(prefix, setdiff(1:29, as.integer(exclude_items)))
  syntax <- psychval_lavaan_model(prefix, model_name, exclude_items = exclude_items)

  fit <- tryCatch(
    lavaan::cfa(
      syntax,
      data = data,
      ordered = ordered,
      estimator = "WLSMV",
      group = group,
      cluster = cluster,
      std.lv = TRUE
    ),
    error = function(e) e
  )

  if (inherits(fit, "error")) {
    return(list(
      fit = NULL,
      indices = data.frame(
        form = form,
        model = model_name,
        converged = FALSE,
        chisq_scaled = NA_real_,
        df_scaled = NA_real_,
        pvalue_scaled = NA_real_,
        cfi_scaled = NA_real_,
        tli_scaled = NA_real_,
        rmsea_scaled = NA_real_,
        rmsea_ci_lower = NA_real_,
        rmsea_ci_upper = NA_real_,
        srmr = NA_real_,
        error = conditionMessage(fit),
        stringsAsFactors = FALSE
      )
    ))
  }

  list(fit = fit, indices = psychval_fit_indices(fit, form, model_name))
}

psychval_standardized_loadings <- function(fit, form, model_name) {
  if (is.null(fit)) {
    return(data.frame())
  }
  params <- lavaan::standardizedSolution(fit)
  loadings <- params[params$op == "=~", c("lhs", "rhs", "est.std", "se", "pvalue")]
  names(loadings) <- c("factor", "item", "std_loading", "se", "pvalue")
  loadings$form <- form
  loadings$model <- model_name
  loadings[, c("form", "model", "factor", "item", "std_loading", "se", "pvalue")]
}

psychval_correlation_rows <- function(data, x_vars, y_var, label) {
  rows <- lapply(x_vars, function(x_var) {
    keep <- stats::complete.cases(data[, c(x_var, y_var)])
    test <- if (sum(keep) >= 4) {
      suppressWarnings(stats::cor.test(data[[x_var]][keep], data[[y_var]][keep],
                                       method = "spearman", exact = FALSE))
    } else {
      NULL
    }
    data.frame(
      analysis = label,
      x = x_var,
      y = y_var,
      n = sum(keep),
      spearman_rho = if (is.null(test)) NA_real_ else unname(test$estimate),
      p_value = if (is.null(test)) NA_real_ else test$p.value,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

psychval_icc_rows <- function(scores, cluster_col, score_cols) {
  psychval_required_package("lme4")
  psychval_required_package("performance")
  rows <- lapply(score_cols, function(score_col) {
    model_data <- scores[, c(cluster_col, score_col)]
    model_data <- model_data[stats::complete.cases(model_data), ]
    names(model_data) <- c("cluster", "score")
    fit <- tryCatch(lme4::lmer(score ~ 1 + (1 | cluster), data = model_data), error = function(e) e)
    if (inherits(fit, "error")) {
      return(data.frame(score = score_col, n = nrow(model_data), icc_adjusted = NA_real_,
                        icc_unadjusted = NA_real_, error = conditionMessage(fit)))
    }
    icc <- performance::icc(fit)
    data.frame(
      score = score_col,
      n = nrow(model_data),
      icc_adjusted = unname(icc$ICC_adjusted),
      icc_unadjusted = unname(icc$ICC_unadjusted),
      error = NA_character_,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}
