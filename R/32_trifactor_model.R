# [KESIFSEL - POST-HOC] Faz II SAP KISIM XX/50
# Trifactor Model (CT-C(M-1) varyanti, Eid 2008; Masse, Newman & Pulman 2020)
#
# Anne (referans informant) + Indeks cocuk + Kardes ucgenli olcum modeli.
# Her EMBU alt olcegi icin ayri T-CFA: tek ortak trait latent + 2 method-spesifik
# (indeks ve kardes; anne method faktoru reference olarak kaldirilir).
#
# Skill referansi: references/psikometri-pipeline.md, references/network-analizi.md
# Veri kaynagi: df_family_scored (anne EMBU-P), df_long_scored (cocuk EMBU-C)
# Cikti: outputs/tables/phase2_trifactor_*.csv

trifactor_subscale_map <- function() {
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

trifactor_anne_item_columns <- function(items) {
  paste0("embu_p_q", sprintf("%02d", items))
}

trifactor_cocuk_base_columns <- function(items) {
  paste0("embu_c_q", sprintf("%02d", items))
}

trifactor_cocuk_role_columns <- function(items, role) {
  if (!role %in% c("indeks", "kardes")) {
    stop("trifactor role must be 'indeks' or 'kardes'", call. = FALSE)
  }
  paste0(trifactor_cocuk_base_columns(items), "_", role)
}

trifactor_require_columns <- function(df, columns, context) {
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

trifactor_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

trifactor_prepare_wide_data <- function(df_family_scored, df_long_scored, items) {
  anne_cols <- trifactor_anne_item_columns(items)
  cocuk_cols <- trifactor_cocuk_base_columns(items)

  trifactor_require_columns(
    df_family_scored,
    c("aile_no", anne_cols),
    "trifactor anne data"
  )
  trifactor_require_columns(
    df_long_scored,
    c("aile_no", "family_role_f", cocuk_cols),
    "trifactor cocuk data"
  )

  if (anyDuplicated(df_family_scored$aile_no) > 0L) {
    stop("trifactor family data must have one row per family", call. = FALSE)
  }

  anne_side <- df_family_scored[, c("aile_no", anne_cols), drop = FALSE]

  long_side <- df_long_scored[, c("aile_no", "family_role_f", cocuk_cols), drop = FALSE]
  long_side$role_token <- trifactor_normalize_role(long_side$family_role_f)
  long_side <- long_side[!is.na(long_side$role_token), , drop = FALSE]

  collapse_role <- function(role) {
    sub <- long_side[long_side$role_token == role, , drop = FALSE]
    if (anyDuplicated(sub$aile_no) > 0L) {
      stop(
        sprintf("trifactor cocuk data has duplicated aile_no for role '%s'", role),
        call. = FALSE
      )
    }
    out <- sub[, c("aile_no", cocuk_cols), drop = FALSE]
    names(out)[-1L] <- trifactor_cocuk_role_columns(items, role)
    out
  }

  indeks_side <- collapse_role("indeks")
  kardes_side <- collapse_role("kardes")

  wide <- merge(anne_side, indeks_side, by = "aile_no", all.x = TRUE)
  wide <- merge(wide, kardes_side, by = "aile_no", all.x = TRUE)

  for (col in c(
    anne_cols,
    trifactor_cocuk_role_columns(items, "indeks"),
    trifactor_cocuk_role_columns(items, "kardes")
  )) {
    wide[[col]] <- suppressWarnings(as.integer(as.character(wide[[col]])))
  }

  attr(wide, "trifactor_items") <- items
  attr(wide, "trifactor_anne_columns") <- anne_cols
  attr(wide, "trifactor_indeks_columns") <- trifactor_cocuk_role_columns(items, "indeks")
  attr(wide, "trifactor_kardes_columns") <- trifactor_cocuk_role_columns(items, "kardes")
  wide
}

trifactor_coverage_summary <- function(wide_data, subscale_label) {
  anne_cols <- attr(wide_data, "trifactor_anne_columns")
  indeks_cols <- attr(wide_data, "trifactor_indeks_columns")
  kardes_cols <- attr(wide_data, "trifactor_kardes_columns")

  coverage <- function(cols) {
    rows_complete <- stats::complete.cases(wide_data[, cols, drop = FALSE])
    sum(rows_complete)
  }

  anne_n <- coverage(anne_cols)
  indeks_n <- coverage(indeks_cols)
  kardes_n <- coverage(kardes_cols)
  triple_n <- sum(stats::complete.cases(wide_data[, c(anne_cols, indeks_cols, kardes_cols), drop = FALSE]))

  data.frame(
    subscale = subscale_label,
    n_family_total = nrow(wide_data),
    n_complete_anne = anne_n,
    n_complete_indeks = indeks_n,
    n_complete_kardes = kardes_n,
    n_triple_complete = triple_n,
    triple_coverage_ratio = ifelse(nrow(wide_data) > 0L, triple_n / nrow(wide_data), NA_real_),
    stringsAsFactors = FALSE
  )
}

trifactor_model_syntax <- function(items, subscale_label) {
  anne_cols <- trifactor_anne_item_columns(items)
  indeks_cols <- trifactor_cocuk_role_columns(items, "indeks")
  kardes_cols <- trifactor_cocuk_role_columns(items, "kardes")

  trait_indicators <- paste(c(anne_cols, indeks_cols, kardes_cols), collapse = " + ")
  indeks_indicators <- paste(indeks_cols, collapse = " + ")
  kardes_indicators <- paste(kardes_cols, collapse = " + ")

  sl <- subscale_label
  paste(c(
    sprintf("F_trait_%s =~ %s", sl, trait_indicators),
    sprintf("F_indeks_%s =~ %s", sl, indeks_indicators),
    sprintf("F_kardes_%s =~ %s", sl, kardes_indicators),
    # CT-C(M-1) ortogonalite: method faktorleri trait'e ortogonal
    sprintf("F_trait_%s ~~ 0 * F_indeks_%s", sl, sl),
    sprintf("F_trait_%s ~~ 0 * F_kardes_%s", sl, sl),
    # Method faktorleri arasinda serbest korelasyon (Eid 2008)
    sprintf("F_indeks_%s ~~ F_kardes_%s", sl, sl)
  ), collapse = "\n")
}

trifactor_fit_indices <- function(fit, subscale_label) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required for trifactor models", call. = FALSE)
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

trifactor_loadings_table <- function(fit, subscale_label) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required for trifactor models", call. = FALSE)
  }
  est <- lavaan::standardizedSolution(fit, type = "std.all")
  est <- est[est$op == "=~", , drop = FALSE]
  factor_to_method <- function(lhs) {
    if (grepl("^F_trait_", lhs)) "trait"
    else if (grepl("^F_indeks_", lhs)) "indeks_method"
    else if (grepl("^F_kardes_", lhs)) "kardes_method"
    else NA_character_
  }
  data.frame(
    subscale = subscale_label,
    factor = est$lhs,
    method = vapply(est$lhs, factor_to_method, character(1L)),
    item = est$rhs,
    std_loading = est$est.std,
    se = est$se,
    z = est$z,
    p_value = est$pvalue,
    ci_lower = est$ci.lower,
    ci_upper = est$ci.upper,
    stringsAsFactors = FALSE
  )
}

trifactor_variance_decomposition <- function(loadings_table, subscale_label) {
  loadings_table <- loadings_table[loadings_table$subscale == subscale_label, , drop = FALSE]
  loadings_table$lambda_sq <- loadings_table$std_loading^2

  total_per_item <- stats::aggregate(
    lambda_sq ~ item,
    data = loadings_table,
    FUN = sum,
    na.rm = TRUE
  )
  names(total_per_item)[2L] <- "communality_sum_sq"

  trait_per_item <- stats::aggregate(
    lambda_sq ~ item,
    data = loadings_table[loadings_table$method == "trait", , drop = FALSE],
    FUN = sum,
    na.rm = TRUE
  )
  names(trait_per_item)[2L] <- "trait_sum_sq"

  method_per_item <- stats::aggregate(
    lambda_sq ~ item,
    data = loadings_table[loadings_table$method %in% c("indeks_method", "kardes_method"), , drop = FALSE],
    FUN = sum,
    na.rm = TRUE
  )
  names(method_per_item)[2L] <- "method_sum_sq"

  out <- merge(total_per_item, trait_per_item, by = "item", all.x = TRUE)
  out <- merge(out, method_per_item, by = "item", all.x = TRUE)
  out$trait_sum_sq[is.na(out$trait_sum_sq)] <- 0
  out$method_sum_sq[is.na(out$method_sum_sq)] <- 0
  out$trait_proportion <- ifelse(out$communality_sum_sq > 0, out$trait_sum_sq / out$communality_sum_sq, NA_real_)
  out$method_proportion <- ifelse(out$communality_sum_sq > 0, out$method_sum_sq / out$communality_sum_sq, NA_real_)

  out$subscale <- subscale_label
  informant_token <- function(item_name) {
    if (grepl("_indeks$", item_name)) "indeks"
    else if (grepl("_kardes$", item_name)) "kardes"
    else if (grepl("^embu_p_", item_name)) "anne"
    else NA_character_
  }
  out$informant <- vapply(out$item, informant_token, character(1L))
  out[, c(
    "subscale", "informant", "item",
    "trait_sum_sq", "method_sum_sq", "communality_sum_sq",
    "trait_proportion", "method_proportion"
  )]
}

trifactor_method_correlation <- function(fit, subscale_label) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required for trifactor models", call. = FALSE)
  }
  est <- lavaan::standardizedSolution(fit, type = "std.all")
  rows <- est[est$op == "~~" & est$lhs != est$rhs, , drop = FALSE]
  rows <- rows[
    grepl("^F_indeks_", rows$lhs) & grepl("^F_kardes_", rows$rhs) |
      grepl("^F_kardes_", rows$lhs) & grepl("^F_indeks_", rows$rhs),
    ,
    drop = FALSE
  ]
  if (nrow(rows) == 0L) {
    return(data.frame(
      subscale = subscale_label,
      pair = character(0),
      std_correlation = numeric(0),
      ci_lower = numeric(0),
      ci_upper = numeric(0),
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    subscale = subscale_label,
    pair = paste(rows$lhs, rows$rhs, sep = " <-> "),
    std_correlation = rows$est.std,
    ci_lower = rows$ci.lower,
    ci_upper = rows$ci.upper,
    p_value = rows$pvalue,
    stringsAsFactors = FALSE
  )
}

trifactor_fit_one <- function(wide_data, items, subscale_label,
                              estimator = "WLSMV") {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Package 'lavaan' is required for trifactor models", call. = FALSE)
  }
  syntax <- trifactor_model_syntax(items, subscale_label)
  ordered_cols <- c(
    trifactor_anne_item_columns(items),
    trifactor_cocuk_role_columns(items, "indeks"),
    trifactor_cocuk_role_columns(items, "kardes")
  )
  fit <- tryCatch(
    lavaan::cfa(
      syntax,
      data = wide_data,
      ordered = ordered_cols,
      estimator = estimator,
      missing = "pairwise"
    ),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(
      fit = NULL,
      status = data.frame(
        subscale = subscale_label,
        converged = FALSE,
        error_message = conditionMessage(fit),
        stringsAsFactors = FALSE
      ),
      fit_indices = NULL,
      loadings = NULL,
      variance = NULL,
      method_correlation = NULL
    ))
  }
  converged <- isTRUE(lavaan::lavInspect(fit, "converged"))
  if (!converged) {
    return(list(
      fit = fit,
      status = data.frame(
        subscale = subscale_label,
        converged = FALSE,
        error_message = "lavaan did not converge",
        stringsAsFactors = FALSE
      ),
      fit_indices = NULL,
      loadings = NULL,
      variance = NULL,
      method_correlation = NULL
    ))
  }
  fit_indices <- trifactor_fit_indices(fit, subscale_label)
  loadings <- trifactor_loadings_table(fit, subscale_label)
  variance <- trifactor_variance_decomposition(loadings, subscale_label)
  method_corr <- trifactor_method_correlation(fit, subscale_label)
  status <- data.frame(
    subscale = subscale_label,
    converged = TRUE,
    error_message = NA_character_,
    stringsAsFactors = FALSE
  )
  list(
    fit = fit,
    status = status,
    fit_indices = fit_indices,
    loadings = loadings,
    variance = variance,
    method_correlation = method_corr
  )
}

run_trifactor_pipeline <- function(df_family_scored, df_long_scored,
                                   subscales = NULL,
                                   estimator = "WLSMV",
                                   fit_models = TRUE) {
  subscale_map <- trifactor_subscale_map()
  if (is.null(subscales)) {
    subscales <- names(subscale_map)
  }
  unknown <- setdiff(subscales, names(subscale_map))
  if (length(unknown) > 0L) {
    stop(sprintf("Unknown trifactor subscale(s): %s", paste(unknown, collapse = ", ")), call. = FALSE)
  }

  coverage_rows <- list()
  status_rows <- list()
  fit_rows <- list()
  loadings_rows <- list()
  variance_rows <- list()
  method_rows <- list()
  syntax_rows <- list()

  for (sl in subscales) {
    items <- subscale_map[[sl]]
    wide <- trifactor_prepare_wide_data(df_family_scored, df_long_scored, items)
    coverage_rows[[sl]] <- trifactor_coverage_summary(wide, sl)
    syntax_rows[[sl]] <- data.frame(
      subscale = sl,
      n_items = length(items),
      syntax = trifactor_model_syntax(items, sl),
      stringsAsFactors = FALSE
    )
    if (!fit_models) {
      next
    }
    result <- trifactor_fit_one(wide, items, sl, estimator = estimator)
    status_rows[[sl]] <- result$status
    if (!is.null(result$fit_indices)) fit_rows[[sl]] <- result$fit_indices
    if (!is.null(result$loadings)) loadings_rows[[sl]] <- result$loadings
    if (!is.null(result$variance)) variance_rows[[sl]] <- result$variance
    if (!is.null(result$method_correlation)) method_rows[[sl]] <- result$method_correlation
  }

  bind <- function(rows) if (length(rows) > 0L) do.call(rbind, rows) else NULL
  out <- list(
    coverage = bind(coverage_rows),
    syntax = bind(syntax_rows),
    status = bind(status_rows),
    fit_indices = bind(fit_rows),
    loadings = bind(loadings_rows),
    variance = bind(variance_rows),
    method_correlation = bind(method_rows),
    target_summary = data.frame(
      analysis = "trifactor_phase2",
      n_subscales_requested = length(subscales),
      n_subscales_fit = if (fit_models) length(status_rows) else 0L,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XX/50)",
      reference_doc = "04-sap-faz2-posthoc.md",
      stringsAsFactors = FALSE
    )
  )
  out
}
