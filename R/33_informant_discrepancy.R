# [KESIFSEL - POST-HOC] Faz II SAP KISIM XX/51-52
# Latent Informant Discrepancy SEM + Latent Difference Score (LDS)
#
# Anne (EMBU-P) ile indeks cocuk (EMBU-C) algilari arasindaki uyumsuzlugu
# latent duzeyde modeller. Iki katman:
#   (1) Two-factor latent corr modeli: F_anne_red ~~ F_cocuk_red
#   (2) LDS modeli (McArdle 2009): F_diff = F_anne - F_cocuk; F_diff uzerinde
#       grup, Beck, SES, cocuk yasi yapisal etkileri
#
# Skill referanslari: references/psikometri-pipeline.md,
#                     references/mediation-modelleri.md,
#                     references/raporlama-sablonlari.md
# Veri: df_family_ses (anne EMBU-P + Beck + SES) + df_long_scored[Indeks] (cocuk EMBU-C + cocuk_yas)

disc_subscale_map <- function() {
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

disc_anne_item_columns <- function(items) {
  paste0("embu_p_q", sprintf("%02d", items))
}

disc_cocuk_item_columns <- function(items) {
  paste0("embu_c_q", sprintf("%02d", items))
}

disc_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf(
        "%s is missing required column(s): %s",
        context, paste(missing_columns, collapse = ", ")
      ),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

disc_scale_vector <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  center <- mean(x, na.rm = TRUE)
  scale <- stats::sd(x, na.rm = TRUE)
  if (is.na(scale) || scale == 0) {
    stop("Cannot z-scale a constant or fully missing vector", call. = FALSE)
  }
  list(value = (x - center) / scale, center = center, scale = scale)
}

disc_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

disc_ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    group_source <- NULL
    if ("group_f" %in% names(df)) {
      group_source <- df$group_f
    } else if ("grup" %in% names(df)) {
      group_source <- df$grup
    } else if ("group" %in% names(df)) {
      group_source <- df$group
    }

    if (!is.null(group_source)) {
      group_text <- as.character(group_source)
      df$group_dm <- as.integer(grepl("DM", group_text, ignore.case = TRUE))
    }
  }
  df
}

disc_predictor_columns <- function() {
  c(
    "group_dm" = "group_dm",
    "beck_total_z" = "beck_total_z",
    "ses_latent_z" = "ses_latent_z",
    "cocuk_yas_z" = "cocuk_yas_z"
  )
}

disc_prepare_paired_data <- function(df_family_ses, df_long_scored, items,
                                     include_predictors = TRUE) {
  df_family_ses <- disc_ensure_group_dm(df_family_ses)
  anne_cols <- disc_anne_item_columns(items)
  cocuk_cols <- disc_cocuk_item_columns(items)

  required_family <- c("aile_no", anne_cols)
  required_long <- c("aile_no", "family_role_f", cocuk_cols, "cocuk_yas")
  if (include_predictors) {
    required_family <- c(required_family, "group_dm", "beck_total", "ses_latent")
  }

  disc_require_columns(df_family_ses, required_family, "discrepancy family data")
  disc_require_columns(df_long_scored, required_long, "discrepancy long data")

  if (anyDuplicated(df_family_ses$aile_no) > 0L) {
    stop("discrepancy family data must have one row per family", call. = FALSE)
  }

  family_side <- df_family_ses[, required_family, drop = FALSE]

  long_side <- df_long_scored[, required_long, drop = FALSE]
  long_side$role_token <- disc_normalize_role(long_side$family_role_f)
  indeks_side <- long_side[!is.na(long_side$role_token) & long_side$role_token == "indeks", , drop = FALSE]
  if (anyDuplicated(indeks_side$aile_no) > 0L) {
    stop("discrepancy long data has duplicated indeks rows per family", call. = FALSE)
  }

  paired <- merge(
    family_side,
    indeks_side[, c("aile_no", cocuk_cols, "cocuk_yas"), drop = FALSE],
    by = "aile_no",
    all.x = FALSE,
    all.y = FALSE
  )

  for (col in c(anne_cols, cocuk_cols)) {
    paired[[col]] <- suppressWarnings(as.integer(as.character(paired[[col]])))
  }

  scaling <- list()
  if (include_predictors) {
    z_targets <- c("beck_total", "ses_latent", "cocuk_yas")
    for (column in z_targets) {
      scaled <- disc_scale_vector(paired[[column]])
      paired[[paste0(column, "_z")]] <- scaled$value
      scaling[[column]] <- data.frame(
        variable = column,
        center = scaled$center,
        scale = scaled$scale,
        stringsAsFactors = FALSE
      )
    }
    if (is.numeric(paired$group_dm)) {
      paired$group_dm <- as.integer(paired$group_dm)
    } else if (is.factor(paired$group_dm)) {
      paired$group_dm <- as.integer(paired$group_dm) - 1L
    }
  }

  attr(paired, "disc_items") <- items
  attr(paired, "disc_anne_columns") <- anne_cols
  attr(paired, "disc_cocuk_columns") <- cocuk_cols
  attr(paired, "disc_scaling") <- if (length(scaling) > 0L) do.call(rbind, scaling) else NULL
  paired
}

disc_two_factor_syntax <- function(items, subscale_label, ordinal = TRUE) {
  anne_cols <- disc_anne_item_columns(items)
  cocuk_cols <- disc_cocuk_item_columns(items)
  sl <- subscale_label
  syntax <- c(
    sprintf("F_anne_%s =~ %s", sl, paste(anne_cols, collapse = " + ")),
    sprintf("F_cocuk_%s =~ %s", sl, paste(cocuk_cols, collapse = " + ")),
    sprintf("F_anne_%s ~~ F_cocuk_%s", sl, sl)
  )
  paste(syntax, collapse = "\n")
}

disc_lds_syntax <- function(items, subscale_label, predictors = NULL) {
  anne_cols <- disc_anne_item_columns(items)
  cocuk_cols <- disc_cocuk_item_columns(items)
  sl <- subscale_label

  body <- c(
    sprintf("F_anne_%s =~ %s", sl, paste(anne_cols, collapse = " + ")),
    sprintf("F_cocuk_%s =~ %s", sl, paste(cocuk_cols, collapse = " + ")),
    # LDS: F_anne_<sl> = F_cocuk_<sl> + F_diff_<sl>
    sprintf("F_diff_%s =~ 1 * F_anne_%s", sl, sl),
    sprintf("F_anne_%s ~ 1 * F_cocuk_%s", sl, sl),
    sprintf("F_anne_%s ~~ 0 * F_anne_%s", sl, sl),
    # Discrepancy variance estimated freely
    sprintf("F_diff_%s ~~ F_diff_%s", sl, sl),
    # Cocuk latent variance estimated; correlation with F_diff free
    sprintf("F_cocuk_%s ~~ F_cocuk_%s", sl, sl),
    sprintf("F_cocuk_%s ~~ F_diff_%s", sl, sl)
  )
  if (!is.null(predictors) && length(predictors) > 0L) {
    body <- c(
      body,
      sprintf("F_diff_%s ~ %s", sl, paste(predictors, collapse = " + ")),
      sprintf("F_cocuk_%s ~ %s", sl, paste(setdiff(predictors, "beck_total_z"), collapse = " + "))
    )
  }
  paste(body, collapse = "\n")
}

disc_fit_two_factor <- function(paired_data, items, subscale_label,
                                estimator = "WLSMV") {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required", call. = FALSE)
  }
  syntax <- disc_two_factor_syntax(items, subscale_label, ordinal = TRUE)
  ordered_cols <- c(
    disc_anne_item_columns(items),
    disc_cocuk_item_columns(items)
  )
  fit <- tryCatch(
    lavaan::cfa(
      syntax,
      data = paired_data,
      ordered = ordered_cols,
      estimator = estimator,
      missing = "pairwise"
    ),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(
      fit = NULL,
      converged = FALSE,
      error_message = conditionMessage(fit)
    ))
  }
  list(
    fit = fit,
    converged = isTRUE(lavaan::lavInspect(fit, "converged")),
    error_message = NA_character_
  )
}

disc_fit_lds <- function(paired_data, items, subscale_label,
                         predictors = NULL,
                         estimator = "WLSMV") {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required", call. = FALSE)
  }
  syntax <- disc_lds_syntax(items, subscale_label, predictors = predictors)
  ordered_cols <- c(
    disc_anne_item_columns(items),
    disc_cocuk_item_columns(items)
  )
  fit <- tryCatch(
    lavaan::sem(
      syntax,
      data = paired_data,
      ordered = ordered_cols,
      estimator = estimator,
      missing = "pairwise"
    ),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(
      fit = NULL,
      converged = FALSE,
      error_message = conditionMessage(fit)
    ))
  }
  list(
    fit = fit,
    converged = isTRUE(lavaan::lavInspect(fit, "converged")),
    error_message = NA_character_
  )
}

disc_fit_indices <- function(fit, subscale_label, model_label) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required", call. = FALSE)
  }
  m <- lavaan::fitMeasures(
    fit,
    c(
      "chisq.scaled", "df.scaled", "pvalue.scaled",
      "cfi.scaled", "tli.scaled", "rmsea.scaled",
      "rmsea.ci.lower.scaled", "rmsea.ci.upper.scaled",
      "srmr"
    )
  )
  data.frame(
    subscale = subscale_label,
    model = model_label,
    chi_sq = unname(m["chisq.scaled"]),
    df = unname(m["df.scaled"]),
    p_value = unname(m["pvalue.scaled"]),
    cfi = unname(m["cfi.scaled"]),
    tli = unname(m["tli.scaled"]),
    rmsea = unname(m["rmsea.scaled"]),
    rmsea_ci_lower = unname(m["rmsea.ci.lower.scaled"]),
    rmsea_ci_upper = unname(m["rmsea.ci.upper.scaled"]),
    srmr = unname(m["srmr"]),
    converged = lavaan::lavInspect(fit, "converged"),
    stringsAsFactors = FALSE
  )
}

disc_latent_correlation <- function(fit, subscale_label) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required", call. = FALSE)
  }
  est <- lavaan::standardizedSolution(fit, type = "std.all")
  rows <- est[
    est$op == "~~" &
      est$lhs != est$rhs &
      grepl(sprintf("^F_anne_%s$", subscale_label), est$lhs) &
      grepl(sprintf("^F_cocuk_%s$", subscale_label), est$rhs),
    ,
    drop = FALSE
  ]
  if (nrow(rows) == 0L) {
    return(data.frame(
      subscale = subscale_label,
      latent_r = NA_real_,
      ci_lower = NA_real_,
      ci_upper = NA_real_,
      p_value = NA_real_,
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    subscale = subscale_label,
    latent_r = rows$est.std[1L],
    ci_lower = rows$ci.lower[1L],
    ci_upper = rows$ci.upper[1L],
    p_value = rows$pvalue[1L],
    stringsAsFactors = FALSE
  )
}

disc_lds_variance_decomposition <- function(fit, subscale_label) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required", call. = FALSE)
  }
  est <- lavaan::parameterEstimates(fit, standardized = TRUE)
  variance_rows <- est[est$op == "~~" & est$lhs == est$rhs, , drop = FALSE]

  pull <- function(label) {
    sub <- variance_rows[variance_rows$lhs == label, , drop = FALSE]
    if (nrow(sub) == 0L) NA_real_ else sub$est[1L]
  }
  var_diff <- pull(sprintf("F_diff_%s", subscale_label))
  var_cocuk <- pull(sprintf("F_cocuk_%s", subscale_label))
  total <- sum(c(var_diff, var_cocuk), na.rm = TRUE)
  ratio <- if (!is.na(total) && total > 0) var_diff / total else NA_real_

  category <- if (is.na(ratio)) {
    NA_character_
  } else if (ratio < 0.20) {
    "ihmal_edilebilir"
  } else if (ratio < 0.30) {
    "kucuk"
  } else if (ratio < 0.50) {
    "klinik_anlamli"
  } else {
    "dominant"
  }
  data.frame(
    subscale = subscale_label,
    var_diff = var_diff,
    var_cocuk = var_cocuk,
    var_total = total,
    discrepancy_ratio = ratio,
    interpretation = category,
    stringsAsFactors = FALSE
  )
}

disc_lds_predictor_paths <- function(fit, subscale_label) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required", call. = FALSE)
  }
  est <- lavaan::standardizedSolution(fit, type = "std.all")
  rows <- est[
    est$op == "~" &
      grepl(sprintf("^F_diff_%s$|^F_cocuk_%s$", subscale_label, subscale_label), est$lhs),
    ,
    drop = FALSE
  ]
  if (nrow(rows) == 0L) {
    return(data.frame(
      subscale = character(0),
      outcome = character(0),
      predictor = character(0),
      std_estimate = numeric(0),
      se = numeric(0),
      ci_lower = numeric(0),
      ci_upper = numeric(0),
      p_value = numeric(0),
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    subscale = subscale_label,
    outcome = rows$lhs,
    predictor = rows$rhs,
    std_estimate = rows$est.std,
    se = rows$se,
    ci_lower = rows$ci.lower,
    ci_upper = rows$ci.upper,
    p_value = rows$pvalue,
    stringsAsFactors = FALSE
  )
}

disc_run_subscale <- function(paired_data, items, subscale_label,
                              predictors = NULL,
                              estimator = "WLSMV",
                              fit_lds = TRUE) {
  two_factor <- disc_fit_two_factor(paired_data, items, subscale_label, estimator = estimator)
  status_rows <- list(data.frame(
    subscale = subscale_label,
    model = "two_factor_corr",
    converged = two_factor$converged,
    error_message = two_factor$error_message,
    stringsAsFactors = FALSE
  ))
  fit_rows <- list()
  cor_rows <- list()
  if (two_factor$converged) {
    fit_rows[["two_factor"]] <- disc_fit_indices(two_factor$fit, subscale_label, "two_factor_corr")
    cor_rows[[subscale_label]] <- disc_latent_correlation(two_factor$fit, subscale_label)
  }

  variance_rows <- list()
  predictor_rows <- list()
  if (fit_lds) {
    lds <- disc_fit_lds(paired_data, items, subscale_label,
      predictors = predictors, estimator = estimator
    )
    status_rows[[length(status_rows) + 1L]] <- data.frame(
      subscale = subscale_label,
      model = if (length(predictors) > 0L) "lds_with_predictors" else "lds_basic",
      converged = lds$converged,
      error_message = lds$error_message,
      stringsAsFactors = FALSE
    )
    if (lds$converged) {
      fit_rows[["lds"]] <- disc_fit_indices(
        lds$fit, subscale_label,
        if (length(predictors) > 0L) "lds_with_predictors" else "lds_basic"
      )
      variance_rows[[subscale_label]] <- disc_lds_variance_decomposition(lds$fit, subscale_label)
      if (length(predictors) > 0L) {
        predictor_rows[[subscale_label]] <- disc_lds_predictor_paths(lds$fit, subscale_label)
      }
    }
  }

  bind_or_null <- function(rows) if (length(rows) > 0L) do.call(rbind, rows) else NULL
  list(
    status = bind_or_null(status_rows),
    fit_indices = bind_or_null(fit_rows),
    latent_correlation = bind_or_null(cor_rows),
    variance = bind_or_null(variance_rows),
    predictor_paths = bind_or_null(predictor_rows)
  )
}

run_informant_discrepancy_pipeline <- function(df_family_ses, df_long_scored,
                                               subscales = NULL,
                                               estimator = "WLSMV",
                                               include_predictors = TRUE,
                                               fit_lds = TRUE) {
  subscale_map <- disc_subscale_map()
  if (is.null(subscales)) {
    subscales <- names(subscale_map)
  }
  unknown <- setdiff(subscales, names(subscale_map))
  if (length(unknown) > 0L) {
    stop(sprintf("Unknown discrepancy subscale(s): %s", paste(unknown, collapse = ", ")), call. = FALSE)
  }

  status_all <- list()
  fit_all <- list()
  cor_all <- list()
  variance_all <- list()
  predictor_all <- list()
  coverage_rows <- list()
  scaling_rows <- list()

  predictors <- if (include_predictors) {
    c("group_dm", "beck_total_z", "ses_latent_z", "cocuk_yas_z")
  } else {
    NULL
  }

  for (sl in subscales) {
    items <- subscale_map[[sl]]
    paired <- disc_prepare_paired_data(
      df_family_ses, df_long_scored, items,
      include_predictors = include_predictors
    )
    coverage_rows[[sl]] <- data.frame(
      subscale = sl,
      n_families_total = nrow(df_family_ses),
      n_paired = nrow(paired),
      n_complete_anne = sum(stats::complete.cases(paired[, disc_anne_item_columns(items), drop = FALSE])),
      n_complete_cocuk = sum(stats::complete.cases(paired[, disc_cocuk_item_columns(items), drop = FALSE])),
      stringsAsFactors = FALSE
    )
    scaling_attr <- attr(paired, "disc_scaling")
    if (!is.null(scaling_attr)) {
      scaling_attr$subscale <- sl
      scaling_rows[[sl]] <- scaling_attr
    }
    sub_result <- disc_run_subscale(
      paired, items, sl,
      predictors = predictors,
      estimator = estimator,
      fit_lds = fit_lds
    )
    if (!is.null(sub_result$status)) status_all[[sl]] <- sub_result$status
    if (!is.null(sub_result$fit_indices)) fit_all[[sl]] <- sub_result$fit_indices
    if (!is.null(sub_result$latent_correlation)) cor_all[[sl]] <- sub_result$latent_correlation
    if (!is.null(sub_result$variance)) variance_all[[sl]] <- sub_result$variance
    if (!is.null(sub_result$predictor_paths)) predictor_all[[sl]] <- sub_result$predictor_paths
  }

  bind <- function(rows) if (length(rows) > 0L) do.call(rbind, rows) else NULL
  list(
    coverage = bind(coverage_rows),
    scaling = bind(scaling_rows),
    status = bind(status_all),
    fit_indices = bind(fit_all),
    latent_correlation = bind(cor_all),
    variance = bind(variance_all),
    predictor_paths = bind(predictor_all),
    target_summary = data.frame(
      analysis = "informant_discrepancy_phase2",
      n_subscales = length(subscales),
      include_predictors = include_predictors,
      fit_lds = fit_lds,
      estimator = estimator,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XX/51-52)",
      reference_doc = "04-sap-faz2-posthoc.md",
      stringsAsFactors = FALSE
    )
  )
}
