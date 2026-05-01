# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXI/55-56
# Reliability Generalization (omega_h, omega_h_s, ECV, PUC) + Beck Bifactor
#
# Eid (2017) Bifactor S-1 modeli ile EMBU-P/C icin general factor + alt-olcek
# spesifik faktorler; reference alt olcek default = "asiri_koruma" (Faz II SAP).
# Beck Depresyon Envanteri icin cognitive (q01-q13) vs somatic (q14-q21)
# bifactor analizi (Steer 1999 paralel ayrim).
#
# Reliability metrikleri (Reise 2012; Rodriguez, Reise & Haviland 2016):
#   omega_h = (sum lambda_g)^2 / total_variance
#   omega_h_s = (sum lambda_s)^2 / total_variance  (alt-olcek bazinda)
#   ECV = sum(lambda_g^2) / (sum(lambda_g^2) + sum(lambda_s^2))
#   PUC = uncontaminated correlations / all correlations
#
# Skill referanslari: references/psikometri-pipeline.md,
#                     references/latent-degisken-yontemleri.md
# Veri: df_family_scored (anne EMBU-P + Beck), df_long_scored[Indeks] (cocuk EMBU-C)

omegah_subscale_map <- function() {
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

omegah_anne_columns <- function(items) {
  paste0("embu_p_q", sprintf("%02d", items))
}

omegah_cocuk_columns <- function(items) {
  paste0("embu_c_q", sprintf("%02d", items))
}

omegah_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

omegah_extract_indeks_long <- function(df_long_scored) {
  long <- df_long_scored
  long$role_token <- omegah_normalize_role(long$family_role_f)
  long[!is.na(long$role_token) & long$role_token == "indeks", , drop = FALSE]
}

omegah_bifactor_s1_syntax <- function(prefix, subscale_map, reference_subscale,
                                      label_g = "G") {
  if (!reference_subscale %in% names(subscale_map)) {
    stop(sprintf("Reference subscale '%s' not in map", reference_subscale), call. = FALSE)
  }
  all_items <- unlist(lapply(subscale_map, function(items) {
    paste0(prefix, "_q", sprintf("%02d", items))
  }), use.names = FALSE)

  body <- c(
    sprintf("%s =~ %s", label_g, paste(all_items, collapse = " + "))
  )

  specific_subscales <- setdiff(names(subscale_map), reference_subscale)
  for (sl in specific_subscales) {
    items <- subscale_map[[sl]]
    cols <- paste0(prefix, "_q", sprintf("%02d", items))
    body <- c(body, sprintf("F_%s =~ %s", sl, paste(cols, collapse = " + ")))
  }

  # Orthogonality: G ortogonal to all specific factors
  for (sl in specific_subscales) {
    body <- c(body, sprintf("%s ~~ 0 * F_%s", label_g, sl))
  }
  # Specific factors mutually orthogonal (Eid 2017 S-1 standard)
  if (length(specific_subscales) > 1L) {
    pairs <- utils::combn(specific_subscales, 2L)
    for (k in seq_len(ncol(pairs))) {
      body <- c(body, sprintf("F_%s ~~ 0 * F_%s", pairs[1L, k], pairs[2L, k]))
    }
  }
  paste(body, collapse = "\n")
}

omegah_beck_bifactor_syntax <- function(cognitive_items = 1:13,
                                        somatic_items = 14:21,
                                        prefix = "beck_") {
  cog_cols <- paste0(prefix, cognitive_items)
  som_cols <- paste0(prefix, somatic_items)
  all_cols <- c(cog_cols, som_cols)

  body <- c(
    sprintf("G_beck =~ %s", paste(all_cols, collapse = " + ")),
    sprintf("F_cognitive =~ %s", paste(cog_cols, collapse = " + ")),
    sprintf("F_somatic =~ %s", paste(som_cols, collapse = " + ")),
    "G_beck ~~ 0 * F_cognitive",
    "G_beck ~~ 0 * F_somatic",
    "F_cognitive ~~ 0 * F_somatic"
  )
  paste(body, collapse = "\n")
}

omegah_fit_bifactor <- function(syntax, data, ordered_columns,
                                estimator = "WLSMV",
                                check_gradient = TRUE) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = "lavaan_unavailable"))
  }
  cfa_args <- list(
    model = syntax,
    data = data,
    estimator = estimator,
    missing = if (estimator == "WLSMV") "pairwise" else "fiml",
    check.gradient = check_gradient
  )
  if (estimator %in% c("WLSMV", "DWLS", "ULSMV")) {
    cfa_args$ordered <- ordered_columns
  }
  fit <- tryCatch(do.call(lavaan::cfa, cfa_args), error = function(e) e)
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", error_message = conditionMessage(fit)))
  }
  list(
    status = if (isTRUE(lavaan::lavInspect(fit, "converged"))) "ok" else "no_convergence",
    fit = fit
  )
}

omegah_fit_indices <- function(fit, label_subscale, label_model) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(NULL)
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
    domain = label_subscale,
    model = label_model,
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

omegah_extract_loadings <- function(fit, label_general = "G") {
  est <- lavaan::standardizedSolution(fit, type = "std.all")
  loadings <- est[est$op == "=~", , drop = FALSE]
  loadings$factor_type <- ifelse(loadings$lhs == label_general, "general",
    ifelse(grepl("^F_", loadings$lhs), "specific",
      "other"
    )
  )
  loadings$factor_label <- loadings$lhs
  loadings$item <- loadings$rhs
  loadings$std_loading <- loadings$est.std
  loadings[, c("factor_type", "factor_label", "item", "std_loading", "se", "z", "pvalue")]
}

omegah_compute_metrics <- function(loadings, label_general = "G") {
  if (is.null(loadings) || nrow(loadings) == 0L) {
    return(NULL)
  }
  general <- loadings[loadings$factor_type == "general", , drop = FALSE]
  specific <- loadings[loadings$factor_type == "specific", , drop = FALSE]
  general$lambda_sq <- general$std_loading^2
  specific$lambda_sq <- specific$std_loading^2

  sum_lambda_g_sq <- sum(general$lambda_sq, na.rm = TRUE)
  sum_lambda_s_sq <- sum(specific$lambda_sq, na.rm = TRUE)
  total_common <- sum_lambda_g_sq + sum_lambda_s_sq
  ecv <- if (total_common > 0) sum_lambda_g_sq / total_common else NA_real_

  # Item-level uniqueness via 1 - communality (per item)
  per_item_lambda_sq <- stats::aggregate(
    lambda_sq ~ item,
    data = rbind(general[, c("item", "lambda_sq")], specific[, c("item", "lambda_sq")]),
    FUN = sum,
    na.rm = TRUE
  )
  uniqueness_per_item <- pmax(0, 1 - per_item_lambda_sq$lambda_sq)
  total_uniqueness <- sum(uniqueness_per_item, na.rm = TRUE)

  sum_lambda_g <- sum(general$std_loading, na.rm = TRUE)
  sum_lambda_g_full <- sum_lambda_g^2

  total_variance <- sum_lambda_g_full + sum_lambda_s_sq + total_uniqueness
  omega_h <- if (total_variance > 0) sum_lambda_g_full / total_variance else NA_real_

  # omega_h_s per specific subscale
  if (nrow(specific) > 0L) {
    omega_hs_rows <- lapply(unique(specific$factor_label), function(f) {
      sub_lambda <- specific$std_loading[specific$factor_label == f]
      sub_items <- specific$item[specific$factor_label == f]
      sum_sub <- sum(sub_lambda, na.rm = TRUE)^2
      gen_items <- general[general$item %in% sub_items, , drop = FALSE]
      gen_var <- sum(gen_items$std_loading, na.rm = TRUE)^2
      gen_lambda_sq_within <- sum(gen_items$lambda_sq, na.rm = TRUE)
      spec_lambda_sq_within <- sum(sub_lambda^2, na.rm = TRUE)
      uniq_within <- sum(pmax(0, 1 - (gen_items$lambda_sq + sub_lambda^2)), na.rm = TRUE)
      sub_total <- gen_var + sum_sub + uniq_within
      omega_hs_value <- if (sub_total > 0) sum_sub / sub_total else NA_real_
      data.frame(
        factor_label = f,
        n_items = length(sub_lambda),
        omega_hs = omega_hs_value,
        stringsAsFactors = FALSE
      )
    })
    omega_hs <- do.call(rbind, omega_hs_rows)
  } else {
    omega_hs <- data.frame(
      factor_label = character(0),
      n_items = integer(0),
      omega_hs = numeric(0),
      stringsAsFactors = FALSE
    )
  }

  # PUC: percent uncontaminated correlations
  all_items <- unique(c(general$item, specific$item))
  total_pairs <- choose(length(all_items), 2L)
  contaminated <- 0L
  for (f in unique(specific$factor_label)) {
    n_items_f <- sum(specific$factor_label == f)
    contaminated <- contaminated + choose(n_items_f, 2L)
  }
  puc <- if (total_pairs > 0L) (total_pairs - contaminated) / total_pairs else NA_real_

  list(
    summary = data.frame(
      omega_h = omega_h,
      ecv = ecv,
      puc = puc,
      n_items = length(all_items),
      sum_lambda_g_sq = sum_lambda_g_sq,
      sum_lambda_s_sq = sum_lambda_s_sq,
      total_uniqueness = total_uniqueness,
      stringsAsFactors = FALSE
    ),
    omega_hs = omega_hs
  )
}

omegah_run_embu <- function(prefix, data, subscale_map, reference_subscale,
                            label_domain,
                            estimator = "WLSMV",
                            check_gradient = TRUE,
                            fallback_estimator = "MLR") {
  ordered_cols <- unlist(lapply(subscale_map, function(items) {
    paste0(prefix, "_q", sprintf("%02d", items))
  }), use.names = FALSE)
  available <- ordered_cols[ordered_cols %in% names(data)]
  if (length(available) < length(ordered_cols)) {
    return(list(
      status = "missing_columns",
      missing = setdiff(ordered_cols, available)
    ))
  }
  syntax <- omegah_bifactor_s1_syntax(prefix, subscale_map, reference_subscale)
  result <- omegah_fit_bifactor(syntax, data, ordered_cols,
    estimator = estimator, check_gradient = check_gradient
  )
  if (!identical(result$status, "ok") && !is.null(fallback_estimator) &&
      fallback_estimator != estimator) {
    fallback <- omegah_fit_bifactor(syntax, data, ordered_cols,
      estimator = fallback_estimator, check_gradient = FALSE
    )
    if (identical(fallback$status, "ok")) {
      result <- fallback
      result$used_estimator <- fallback_estimator
    } else {
      return(list(
        status = result$status,
        error_message = result$error_message,
        fallback_status = fallback$status,
        fallback_error = fallback$error_message
      ))
    }
  } else {
    result$used_estimator <- estimator
  }
  if (!identical(result$status, "ok")) {
    return(list(status = result$status, error_message = result$error_message))
  }
  loadings <- omegah_extract_loadings(result$fit)
  metrics <- omegah_compute_metrics(loadings)
  fit_indices <- omegah_fit_indices(result$fit, label_domain, "bifactor_s1")
  list(
    status = "ok",
    fit_indices = fit_indices,
    loadings = transform(loadings, domain = label_domain, model = "bifactor_s1"),
    metrics_summary = transform(metrics$summary, domain = label_domain, model = "bifactor_s1"),
    omega_hs = transform(metrics$omega_hs,
      domain = label_domain,
      reference_subscale = reference_subscale,
      model = "bifactor_s1"
    )
  )
}

omegah_run_beck <- function(data, cognitive_items = 1:13, somatic_items = 14:21,
                            prefix = "beck_", label_domain = "Beck") {
  cog_cols <- paste0(prefix, cognitive_items)
  som_cols <- paste0(prefix, somatic_items)
  all_cols <- c(cog_cols, som_cols)
  available <- all_cols[all_cols %in% names(data)]
  if (length(available) < length(all_cols)) {
    return(list(
      status = "missing_columns",
      missing = setdiff(all_cols, available)
    ))
  }
  syntax <- omegah_beck_bifactor_syntax(cognitive_items, somatic_items, prefix)
  result <- omegah_fit_bifactor(syntax, data, all_cols)
  if (!identical(result$status, "ok")) {
    return(list(status = result$status, error_message = result$error_message))
  }
  loadings <- omegah_extract_loadings(result$fit, label_general = "G_beck")
  loadings$factor_type[loadings$factor_label == "G_beck"] <- "general"
  metrics <- omegah_compute_metrics(loadings, label_general = "G_beck")
  fit_indices <- omegah_fit_indices(result$fit, label_domain, "beck_bifactor")
  list(
    status = "ok",
    fit_indices = fit_indices,
    loadings = transform(loadings, domain = label_domain, model = "beck_bifactor"),
    metrics_summary = transform(metrics$summary, domain = label_domain, model = "beck_bifactor"),
    omega_hs = transform(metrics$omega_hs,
      domain = label_domain,
      reference_subscale = NA_character_,
      model = "beck_bifactor"
    )
  )
}

run_reliability_generalization_pipeline <- function(df_family_scored, df_long_scored,
                                                    reference_subscale = "asiri_koruma") {
  subscale_map <- omegah_subscale_map()

  status_rows <- list()
  fit_rows <- list()
  loading_rows <- list()
  summary_rows <- list()
  omega_hs_rows <- list()

  # EMBU-P (anne)
  embu_p_result <- omegah_run_embu(
    prefix = "embu_p", data = df_family_scored,
    subscale_map = subscale_map, reference_subscale = reference_subscale,
    label_domain = "EMBU-P"
  )
  status_rows[["EMBU-P"]] <- data.frame(
    domain = "EMBU-P",
    model = "bifactor_s1",
    reference_subscale = reference_subscale,
    status = embu_p_result$status,
    error_message = embu_p_result$error_message %||% NA_character_,
    stringsAsFactors = FALSE
  )
  if (identical(embu_p_result$status, "ok")) {
    fit_rows[["EMBU-P"]] <- embu_p_result$fit_indices
    loading_rows[["EMBU-P"]] <- embu_p_result$loadings
    summary_rows[["EMBU-P"]] <- embu_p_result$metrics_summary
    omega_hs_rows[["EMBU-P"]] <- embu_p_result$omega_hs
  }

  # EMBU-C (indeks cocuk)
  long_indeks <- omegah_extract_indeks_long(df_long_scored)
  embu_c_result <- omegah_run_embu(
    prefix = "embu_c", data = long_indeks,
    subscale_map = subscale_map, reference_subscale = reference_subscale,
    label_domain = "EMBU-C"
  )
  status_rows[["EMBU-C"]] <- data.frame(
    domain = "EMBU-C",
    model = "bifactor_s1",
    reference_subscale = reference_subscale,
    status = embu_c_result$status,
    error_message = embu_c_result$error_message %||% NA_character_,
    stringsAsFactors = FALSE
  )
  if (identical(embu_c_result$status, "ok")) {
    fit_rows[["EMBU-C"]] <- embu_c_result$fit_indices
    loading_rows[["EMBU-C"]] <- embu_c_result$loadings
    summary_rows[["EMBU-C"]] <- embu_c_result$metrics_summary
    omega_hs_rows[["EMBU-C"]] <- embu_c_result$omega_hs
  }

  # Beck (cognitive vs somatic)
  beck_result <- omegah_run_beck(df_family_scored)
  status_rows[["Beck"]] <- data.frame(
    domain = "Beck",
    model = "beck_bifactor",
    reference_subscale = NA_character_,
    status = beck_result$status,
    error_message = beck_result$error_message %||% NA_character_,
    stringsAsFactors = FALSE
  )
  if (identical(beck_result$status, "ok")) {
    fit_rows[["Beck"]] <- beck_result$fit_indices
    loading_rows[["Beck"]] <- beck_result$loadings
    summary_rows[["Beck"]] <- beck_result$metrics_summary
    omega_hs_rows[["Beck"]] <- beck_result$omega_hs
  }

  bind <- function(rows) if (length(rows) > 0L) do.call(rbind, rows) else NULL
  list(
    status = bind(status_rows),
    fit_indices = bind(fit_rows),
    loadings = bind(loading_rows),
    metrics_summary = bind(summary_rows),
    omega_hs = bind(omega_hs_rows),
    target_summary = data.frame(
      analysis = "reliability_generalization_phase2",
      reference_subscale = reference_subscale,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXI/55-56)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
