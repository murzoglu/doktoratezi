ses_required_columns <- function() {
  c(
    "egitim_durumu",
    "es_egitim_durumu",
    "calisma_durumu",
    "es_calisma_durumu",
    "cocuk_sayisi",
    "ev_oda_sayisi",
    "ev_sahipligi",
    "arabaniz_var_mi",
    "aile_isei08"
  )
}

ses_material_columns <- function() {
  c("ev_sahipligi", "ev_oda_sayisi", "arabaniz_var_mi")
}

ses_primary_columns <- function() {
  c(
    "max_aile_egitim",
    "mean_aile_egitim",
    "egitim_fark",
    "cift_kazanc",
    "kalabalik_indeksi",
    "material_index",
    "material_quintile",
    "edu_z",
    "isei_z",
    "material_z",
    "ses_composite_eq",
    "ses_hollingshead",
    "ses_latent"
  )
}

ses_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

ses_numeric <- function(x) {
  suppressWarnings(as.numeric(x))
}

ses_standardize <- function(x) {
  x <- ses_numeric(x)
  ok <- !is.na(x)
  out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) {
    return(out)
  }
  sx <- stats::sd(x[ok])
  if (is.na(sx) || sx == 0) {
    return(out)
  }
  out[ok] <- (x[ok] - mean(x[ok])) / sx
  out
}

ses_row_mean <- function(...) {
  values <- cbind(...)
  out <- rowMeans(values, na.rm = TRUE)
  out[is.nan(out)] <- NA_real_
  out
}

ses_pmax_na <- function(...) {
  values <- cbind(...)
  out <- apply(values, 1L, function(row) {
    if (all(is.na(row))) {
      NA_real_
    } else {
      max(row, na.rm = TRUE)
    }
  })
  as.numeric(out)
}

ses_ntile <- function(x, n = 5L) {
  x <- ses_numeric(x)
  out <- rep(NA_integer_, length(x))
  ok <- !is.na(x)
  if (!any(ok)) {
    return(out)
  }
  ranks <- rank(x[ok], ties.method = "average")
  out[ok] <- pmin(n, pmax(1L, ceiling(ranks / sum(ok) * n)))
  as.integer(out)
}

derive_ses_layer_a <- function(df_family) {
  ses_require_columns(
    df_family,
    c(
      "egitim_durumu",
      "es_egitim_durumu",
      "calisma_durumu",
      "es_calisma_durumu",
      "cocuk_sayisi",
      "ev_oda_sayisi"
    ),
    "SES layer A"
  )

  out <- df_family
  egitim <- ses_numeric(out$egitim_durumu)
  es_egitim <- ses_numeric(out$es_egitim_durumu)
  calisma <- ses_numeric(out$calisma_durumu)
  es_calisma <- ses_numeric(out$es_calisma_durumu)
  cocuk_sayisi <- ses_numeric(out$cocuk_sayisi)
  ev_oda_sayisi <- ses_numeric(out$ev_oda_sayisi)

  out$max_aile_egitim <- ses_pmax_na(egitim, es_egitim)
  out$mean_aile_egitim <- ses_row_mean(egitim, es_egitim)
  out$egitim_fark <- abs(egitim - es_egitim)
  out$cift_kazanc <- ifelse(
    is.na(calisma) | is.na(es_calisma),
    NA_real_,
    as.numeric(calisma == 1 & es_calisma == 1)
  )
  out$kalabalik_indeksi <- cocuk_sayisi / (ev_oda_sayisi + 1)
  out
}

ses_complete_correlation <- function(data) {
  stats::cor(data, use = "pairwise.complete.obs")
}

ses_polychoric_correlation <- function(data) {
  if (!requireNamespace("psych", quietly = TRUE)) {
    stop("Required package is not installed: psych", call. = FALSE)
  }

  result <- suppressWarnings(tryCatch(
    psych::polychoric(data)$rho,
    error = function(error) error
  ))
  if (inherits(result, "error")) {
    return(NULL)
  }
  result
}

ses_correlation_matrix_for_material <- function(data, use_polychoric = TRUE) {
  if (use_polychoric) {
    rho <- ses_polychoric_correlation(data)
    if (!is.null(rho) && all(is.finite(rho))) {
      return(list(rho = rho, method = "polychoric"))
    }
  }

  rho <- ses_complete_correlation(data)
  if (!all(is.finite(rho))) {
    stop("Material SES correlation matrix contains non-finite value(s)", call. = FALSE)
  }
  list(rho = rho, method = "pearson_pairwise")
}

ses_one_component_pca <- function(rho) {
  eigen_result <- eigen(rho, symmetric = TRUE)
  vector <- eigen_result$vectors[, 1L]
  loadings <- vector * sqrt(eigen_result$values[[1L]])
  names(vector) <- colnames(rho)
  names(loadings) <- colnames(rho)
  list(
    weights = vector,
    loadings = loadings,
    eigenvalue = eigen_result$values[[1L]],
    variance_explained = eigen_result$values[[1L]] / sum(eigen_result$values)
  )
}

ses_material_anchor <- function(df, columns) {
  pieces <- list()
  if ("ev_sahipligi" %in% columns) {
    pieces$own_home <- 1 - ses_numeric(df$ev_sahipligi)
  }
  if ("ev_oda_sayisi" %in% columns) {
    pieces$rooms <- ses_numeric(df$ev_oda_sayisi)
  }
  if ("arabaniz_var_mi" %in% columns) {
    pieces$car <- ses_numeric(df$arabaniz_var_mi)
  }
  do.call(ses_row_mean, lapply(pieces, ses_standardize))
}

ses_score_pca_component <- function(df, columns, weights) {
  values <- df[columns]
  for (column in columns) {
    values[[column]] <- ses_standardize(values[[column]])
  }
  matrix_values <- as.matrix(values)
  out <- rep(NA_real_, nrow(values))
  complete <- stats::complete.cases(matrix_values)
  out[complete] <- as.numeric(matrix_values[complete, , drop = FALSE] %*% weights[columns])
  out
}

derive_material_index <- function(df_family, loading_threshold = 0.20, use_polychoric = TRUE) {
  ses_require_columns(df_family, ses_material_columns(), "SES material index")

  columns <- ses_material_columns()
  data <- df_family[columns]
  for (column in columns) {
    data[[column]] <- ses_numeric(data[[column]])
  }

  correlation <- ses_correlation_matrix_for_material(data, use_polychoric = use_polychoric)
  pca <- ses_one_component_pca(correlation$rho)
  dropped <- character()

  if ("ev_sahipligi" %in% columns &&
      !is.na(pca$loadings[["ev_sahipligi"]]) &&
      abs(pca$loadings[["ev_sahipligi"]]) < loading_threshold) {
    dropped <- "ev_sahipligi"
    columns <- setdiff(columns, dropped)
    data <- data[columns]
    correlation <- ses_correlation_matrix_for_material(data, use_polychoric = use_polychoric)
    pca <- ses_one_component_pca(correlation$rho)
  }

  score <- ses_score_pca_component(data, columns, pca$weights)
  anchor <- ses_material_anchor(df_family, columns)
  orientation_correlation <- suppressWarnings(stats::cor(score, anchor, use = "complete.obs"))
  orientation <- 1
  if (!is.na(orientation_correlation) && orientation_correlation < 0) {
    orientation <- -1
    score <- -score
    pca$weights <- -pca$weights
    pca$loadings <- -pca$loadings
    orientation_correlation <- -orientation_correlation
  }

  loadings <- data.frame(
    variable = names(pca$loadings),
    loading = unname(pca$loadings),
    retained = TRUE,
    stringsAsFactors = FALSE
  )
  if (length(dropped) > 0L) {
    loadings <- rbind(
      data.frame(
        variable = dropped,
        loading = NA_real_,
        retained = FALSE,
        stringsAsFactors = FALSE
      ),
      loadings
    )
  }

  list(
    score = score,
    quintile = ses_ntile(score, 5L),
    loadings = loadings,
    diagnostics = data.frame(
      material_variables = paste(columns, collapse = ";"),
      dropped_variables = paste(dropped, collapse = ";"),
      correlation_method = correlation$method,
      eigenvalue = pca$eigenvalue,
      variance_explained = pca$variance_explained,
      orientation = orientation,
      orientation_correlation = orientation_correlation,
      stringsAsFactors = FALSE
    )
  )
}

add_ses_composite_scores <- function(df_family) {
  ses_require_columns(df_family, c("mean_aile_egitim", "aile_isei08", "material_index"), "SES composites")
  out <- df_family
  out$edu_z <- ses_standardize(out$mean_aile_egitim)
  out$isei_z <- ses_standardize(out$aile_isei08)
  out$material_z <- ses_standardize(out$material_index)
  out$ses_composite_eq <- ses_row_mean(out$edu_z, out$isei_z, out$material_z)
  out$ses_hollingshead <- (3 * out$edu_z + 5 * out$isei_z) / 8
  out
}

fit_ses_latent_cfa <- function(df_family) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    stop("Required package is not installed: lavaan", call. = FALSE)
  }

  ses_require_columns(
    df_family,
    c("egitim_durumu", "es_egitim_durumu", "aile_isei08", "material_index", "ses_composite_eq"),
    "SES latent CFA"
  )

  model <- "
    SES =~ egitim_durumu + es_egitim_durumu + aile_isei08 + material_index
  "
  fit <- lavaan::cfa(
    model,
    data = df_family,
    estimator = "WLSMV",
    ordered = c("egitim_durumu", "es_egitim_durumu"),
    missing = "pairwise",
    std.lv = TRUE
  )

  scores <- as.numeric(lavaan::lavPredict(fit, type = "lv")[, "SES"])
  if (length(scores) != nrow(df_family)) {
    stop("SES latent CFA scores do not match input row count", call. = FALSE)
  }

  orientation_correlation <- suppressWarnings(stats::cor(scores, df_family$ses_composite_eq, use = "complete.obs"))
  orientation <- 1
  if (!is.na(orientation_correlation) && orientation_correlation < 0) {
    orientation <- -1
    scores <- -scores
    orientation_correlation <- -orientation_correlation
  }

  list(
    fit = fit,
    scores = scores,
    diagnostics = data.frame(
      latent_status = "ok",
      latent_n = sum(!is.na(scores)),
      latent_orientation = orientation,
      latent_orientation_correlation = orientation_correlation,
      stringsAsFactors = FALSE
    )
  )
}

ses_cfa_fit_measures <- function(fit) {
  measures <- c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "srmr")
  values <- tryCatch(
    lavaan::fitMeasures(fit, measures),
    error = function(error) stats::setNames(rep(NA_real_, length(measures)), measures)
  )
  data.frame(
    measure = names(values),
    value = as.numeric(values),
    stringsAsFactors = FALSE
  )
}

derive_ses_composites <- function(df_family, include_latent = TRUE,
                                  loading_threshold = 0.20,
                                  use_polychoric = TRUE) {
  ses_require_columns(df_family, ses_required_columns(), "SES composite derivation")

  out <- derive_ses_layer_a(df_family)
  material <- derive_material_index(
    out,
    loading_threshold = loading_threshold,
    use_polychoric = use_polychoric
  )
  out$material_index <- material$score
  out$material_quintile <- factor(material$quintile, levels = 1:5, ordered = TRUE)
  out <- add_ses_composite_scores(out)

  latent <- NULL
  cfa_fit <- NULL
  cfa_fit_measures <- data.frame(measure = character(), value = numeric(), stringsAsFactors = FALSE)
  latent_diagnostics <- data.frame(
    latent_status = "not_run",
    latent_n = NA_integer_,
    latent_orientation = NA_real_,
    latent_orientation_correlation = NA_real_,
    stringsAsFactors = FALSE
  )

  if (include_latent) {
    latent <- fit_ses_latent_cfa(out)
    out$ses_latent <- latent$scores
    cfa_fit <- latent$fit
    cfa_fit_measures <- ses_cfa_fit_measures(cfa_fit)
    latent_diagnostics <- latent$diagnostics
  } else {
    out$ses_latent <- NA_real_
  }

  diagnostics <- cbind(
    data.frame(
      n_rows = nrow(out),
      loading_threshold = loading_threshold,
      use_polychoric = use_polychoric,
      stringsAsFactors = FALSE
    ),
    material$diagnostics,
    latent_diagnostics
  )

  list(
    data = out,
    diagnostics = diagnostics,
    material_loadings = material$loadings,
    fit_ses = cfa_fit,
    fit_measures = cfa_fit_measures
  )
}

ses_component_summary <- function(df_family_ses) {
  columns <- intersect(ses_primary_columns(), names(df_family_ses))
  rows <- lapply(columns, function(column) {
    values <- df_family_ses[[column]]
    numeric_values <- if (is.factor(values)) {
      ses_numeric(as.character(values))
    } else {
      ses_numeric(values)
    }
    observed <- numeric_values[!is.na(numeric_values)]
    data.frame(
      component = column,
      class = paste(class(values), collapse = ";"),
      n = length(values),
      non_missing_n = length(observed),
      missing_n = sum(is.na(numeric_values)),
      mean = if (length(observed) > 0L) mean(observed) else NA_real_,
      sd = if (length(observed) > 1L) stats::sd(observed) else NA_real_,
      min = if (length(observed) > 0L) min(observed) else NA_real_,
      max = if (length(observed) > 0L) max(observed) else NA_real_,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

ses_correlation_table <- function(df_family_ses) {
  columns <- intersect(
    c("mean_aile_egitim", "aile_isei08", "material_index", "ses_composite_eq", "ses_hollingshead", "ses_latent"),
    names(df_family_ses)
  )
  values <- df_family_ses[columns]
  for (column in columns) {
    values[[column]] <- ses_numeric(values[[column]])
  }
  rho <- stats::cor(values, use = "pairwise.complete.obs")
  rows <- expand.grid(
    variable_1 = rownames(rho),
    variable_2 = colnames(rho),
    stringsAsFactors = FALSE
  )
  rows$r <- as.numeric(rho[cbind(rows$variable_1, rows$variable_2)])
  rows
}

summarize_ses_targets <- function(df_family, df_family_ses) {
  data.frame(
    dataset = "family",
    input_rows = nrow(df_family),
    input_columns = ncol(df_family),
    ses_rows = nrow(df_family_ses),
    ses_columns = ncol(df_family_ses),
    added_columns = ncol(df_family_ses) - ncol(df_family),
    ses_latent_non_missing = if ("ses_latent" %in% names(df_family_ses)) sum(!is.na(df_family_ses$ses_latent)) else NA_integer_,
    stringsAsFactors = FALSE
  )
}
