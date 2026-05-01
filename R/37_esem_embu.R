# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXI/57
# Exploratory SEM (ESEM) — EMBU-P / EMBU-C cross-loading genisletmesi
#
# ESEM (Marsh, Morin, Parker & Kaur 2014), CFA'nin "her madde tek faktore yuklenir"
# kisitini esneterek geomin rotation ile cross-loading'lere izin verir. CFA fit'in
# Hu-Bentler birlesik kriterini karsilamadigi durumlarda alternatif yapisal model
# olarak konumlandirilir.
#
# Skill referanslari: references/psikometri-pipeline.md
# Veri: df_family_scored (anne EMBU-P) + df_long_scored[Indeks] (cocuk EMBU-C)

esem_subscale_map <- function() {
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

esem_anne_columns <- function(items) {
  paste0("embu_p_q", sprintf("%02d", items))
}

esem_cocuk_columns <- function(items) {
  paste0("embu_c_q", sprintf("%02d", items))
}

esem_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

esem_extract_indeks_long <- function(df_long_scored) {
  long <- df_long_scored
  long$role_token <- esem_normalize_role(long$family_role_f)
  long[!is.na(long$role_token) & long$role_token == "indeks", , drop = FALSE]
}

esem_target_matrix <- function(prefix, subscale_map) {
  all_items <- unlist(lapply(subscale_map, function(items) {
    paste0(prefix, "_q", sprintf("%02d", items))
  }), use.names = FALSE)
  factors <- names(subscale_map)
  m <- matrix(NA_real_, nrow = length(all_items), ncol = length(factors),
              dimnames = list(all_items, factors))
  for (sl in factors) {
    cols <- paste0(prefix, "_q", sprintf("%02d", subscale_map[[sl]]))
    m[, sl] <- 0
    m[cols, sl] <- NA_real_  # NA -> serbest (target loading)
    # Diger faktorlerde 0 hedefli (cross-loading minimize edilir)
  }
  m
}

esem_cfa_syntax <- function(prefix, subscale_map) {
  body <- character(0)
  for (sl in names(subscale_map)) {
    cols <- paste0(prefix, "_q", sprintf("%02d", subscale_map[[sl]]))
    body <- c(body, sprintf("%s =~ %s", sl, paste(cols, collapse = " + ")))
  }
  paste(body, collapse = "\n")
}

esem_fit_cfa <- function(syntax, data, ordered_columns, estimator = "WLSMV") {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = "lavaan_unavailable"))
  }
  fit <- tryCatch(
    lavaan::cfa(syntax, data = data, ordered = ordered_columns,
                estimator = estimator, missing = "pairwise"),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", error_message = conditionMessage(fit)))
  }
  list(
    status = if (isTRUE(lavaan::lavInspect(fit, "converged"))) "ok" else "no_convergence",
    fit = fit
  )
}

esem_fit_efa <- function(data, ordered_columns, n_factors,
                         rotation = "geomin", estimator = "WLSMV") {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = "lavaan_unavailable"))
  }
  fit <- tryCatch(
    suppressMessages(lavaan::efa(
      data = data[, ordered_columns, drop = FALSE],
      nfactors = n_factors,
      rotation = rotation,
      ordered = ordered_columns,
      estimator = estimator,
      missing = "pairwise"
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", rotation = rotation, error_message = conditionMessage(fit)))
  }
  list(status = "ok", rotation = rotation, fit = fit)
}

esem_fit_indices <- function(fit, label_domain, label_model) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(NULL)
  }
  tryCatch({
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
      domain = label_domain,
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
      stringsAsFactors = FALSE
    )
  }, error = function(e) NULL)
}

esem_efa_loadings_table <- function(efa_result, label_domain, subscale_map) {
  if (!is.list(efa_result) || !identical(efa_result$status, "ok")) {
    return(NULL)
  }
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(NULL)
  }
  load_mat <- tryCatch(
    {
      sol <- efa_result$fit
      # lavaan.efa S4 - first single-factor result has loadings via @loadings or via summary
      lambda <- tryCatch(lavaan::lavInspect(sol, "std")$lambda, error = function(e) NULL)
      if (is.null(lambda)) {
        sm <- summary(sol)
        sm$loadings
      } else {
        lambda
      }
    },
    error = function(e) NULL
  )
  if (is.null(load_mat) || !is.matrix(load_mat)) {
    return(NULL)
  }
  factor_labels <- colnames(load_mat) %||% sprintf("F%d", seq_len(ncol(load_mat)))
  item_subscale <- list()
  for (sl in names(subscale_map)) {
    for (it in subscale_map[[sl]]) {
      it_name <- paste0(esem_strip_prefix(rownames(load_mat)[1L]), "_q", sprintf("%02d", it))
      item_subscale[[it_name]] <- sl
    }
  }
  rows <- list()
  for (i in seq_len(nrow(load_mat))) {
    item <- rownames(load_mat)[i]
    target_sub <- item_subscale[[item]]
    for (j in seq_len(ncol(load_mat))) {
      rows[[length(rows) + 1L]] <- data.frame(
        domain = label_domain,
        item = item,
        target_subscale = target_sub %||% NA_character_,
        factor_index = j,
        factor_label = factor_labels[j],
        loading = load_mat[i, j],
        rotation = efa_result$rotation,
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

esem_strip_prefix <- function(item_name) {
  # "embu_p_q01" -> "embu_p"
  sub("_q[0-9]+$", "", item_name)
}

esem_cross_loading_summary <- function(loadings_table,
                                       small_threshold = 0.20,
                                       moderate_threshold = 0.30) {
  if (is.null(loadings_table) || nrow(loadings_table) == 0L) {
    return(NULL)
  }
  abs_lambda <- abs(loadings_table$loading)
  data.frame(
    domain = unique(loadings_table$domain),
    n_loadings = nrow(loadings_table),
    n_items = length(unique(loadings_table$item)),
    n_factors = length(unique(loadings_table$factor_label)),
    n_abs_below_small = sum(abs_lambda < small_threshold, na.rm = TRUE),
    share_abs_below_small = mean(abs_lambda < small_threshold, na.rm = TRUE),
    n_abs_above_moderate = sum(abs_lambda >= moderate_threshold, na.rm = TRUE),
    share_abs_above_moderate = mean(abs_lambda >= moderate_threshold, na.rm = TRUE),
    median_abs_loading = stats::median(abs_lambda, na.rm = TRUE),
    max_abs_loading = max(abs_lambda, na.rm = TRUE),
    rotation = unique(loadings_table$rotation),
    stringsAsFactors = FALSE
  )
}

esem_run_domain <- function(prefix, data, subscale_map, label_domain,
                            n_factors = 4L, rotation = "geomin") {
  ordered_cols <- unlist(lapply(subscale_map, function(items) {
    paste0(prefix, "_q", sprintf("%02d", items))
  }), use.names = FALSE)
  available <- ordered_cols[ordered_cols %in% names(data)]
  if (length(available) < length(ordered_cols)) {
    return(list(
      status = "missing_columns",
      missing = setdiff(ordered_cols, available),
      domain = label_domain
    ))
  }

  cfa_syntax <- esem_cfa_syntax(prefix, subscale_map)
  cfa_result <- esem_fit_cfa(cfa_syntax, data, ordered_cols)
  efa_result <- esem_fit_efa(data, ordered_cols, n_factors = n_factors, rotation = rotation)

  fit_rows <- list()
  if (identical(cfa_result$status, "ok")) {
    fit_rows[["cfa"]] <- esem_fit_indices(cfa_result$fit, label_domain, "cfa_baseline")
  }
  if (identical(efa_result$status, "ok")) {
    fit_rows[["efa"]] <- esem_fit_indices(efa_result$fit, label_domain,
                                           sprintf("esem_%s", rotation))
  }

  loadings_tbl <- esem_efa_loadings_table(efa_result, label_domain, subscale_map)
  cross_summary <- esem_cross_loading_summary(loadings_tbl)

  status_rows <- data.frame(
    domain = rep(label_domain, 2L),
    model = c("cfa_baseline", sprintf("esem_%s", rotation)),
    status = c(cfa_result$status, efa_result$status),
    error_message = c(cfa_result$error_message %||% NA_character_,
                      efa_result$error_message %||% NA_character_),
    stringsAsFactors = FALSE
  )

  list(
    status = status_rows,
    fit_indices = if (length(fit_rows) > 0L) do.call(rbind, fit_rows) else NULL,
    loadings = loadings_tbl,
    cross_loading_summary = cross_summary
  )
}

run_esem_embu_pipeline <- function(df_family_scored, df_long_scored,
                                   n_factors = 4L,
                                   rotation = "geomin") {
  subscale_map <- esem_subscale_map()
  status_all <- list()
  fit_all <- list()
  loadings_all <- list()
  summary_all <- list()

  # EMBU-P (anne)
  p_result <- esem_run_domain(
    prefix = "embu_p", data = df_family_scored,
    subscale_map = subscale_map, label_domain = "EMBU-P",
    n_factors = n_factors, rotation = rotation
  )
  if (!is.null(p_result$status)) status_all[["EMBU-P"]] <- p_result$status
  if (!is.null(p_result$fit_indices)) fit_all[["EMBU-P"]] <- p_result$fit_indices
  if (!is.null(p_result$loadings)) loadings_all[["EMBU-P"]] <- p_result$loadings
  if (!is.null(p_result$cross_loading_summary)) summary_all[["EMBU-P"]] <- p_result$cross_loading_summary

  # EMBU-C (indeks cocuk)
  long_indeks <- esem_extract_indeks_long(df_long_scored)
  c_result <- esem_run_domain(
    prefix = "embu_c", data = long_indeks,
    subscale_map = subscale_map, label_domain = "EMBU-C",
    n_factors = n_factors, rotation = rotation
  )
  if (!is.null(c_result$status)) status_all[["EMBU-C"]] <- c_result$status
  if (!is.null(c_result$fit_indices)) fit_all[["EMBU-C"]] <- c_result$fit_indices
  if (!is.null(c_result$loadings)) loadings_all[["EMBU-C"]] <- c_result$loadings
  if (!is.null(c_result$cross_loading_summary)) summary_all[["EMBU-C"]] <- c_result$cross_loading_summary

  bind <- function(rows) if (length(rows) > 0L) do.call(rbind, rows) else NULL
  list(
    status = bind(status_all),
    fit_indices = bind(fit_all),
    loadings = bind(loadings_all),
    cross_loading_summary = bind(summary_all),
    target_summary = data.frame(
      analysis = "esem_embu_phase2",
      n_factors = n_factors,
      rotation = rotation,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXI/57)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
