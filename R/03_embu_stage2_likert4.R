required_package <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    stop(sprintf("Required package is not installed: %s", package), call. = FALSE)
  }
}

embu_item_columns <- function(df, prefix) {
  cols <- paste0(prefix, "_q", sprintf("%02d", 1:29))
  missing <- setdiff(cols, names(df))
  if (length(missing) > 0) {
    stop(sprintf("Missing EMBU columns: %s", paste(missing, collapse = ", ")),
         call. = FALSE)
  }
  cols
}

as_numeric_vector <- function(x) {
  suppressWarnings(as.numeric(x))
}

build_empirical_equip_lookup <- function(
  ref_values,
  measured_values,
  reference_percentile = c("upper_boundary", "midpoint")
) {
  reference_percentile <- match.arg(reference_percentile)
  ref_values <- as_numeric_vector(ref_values)
  measured_values <- as_numeric_vector(measured_values)
  ref_values <- ref_values[!is.na(ref_values) & ref_values %in% 1:4]
  measured_values <- measured_values[!is.na(measured_values) & measured_values %in% 1:6]

  if (length(ref_values) == 0) {
    stop("Reference 4pt values are empty", call. = FALSE)
  }
  if (length(measured_values) == 0) {
    stop("Measured 6pt values are empty", call. = FALSE)
  }

  ref_counts <- tabulate(ref_values, nbins = 4)
  measured_counts <- tabulate(measured_values, nbins = 6)

  ref_cdf <- cumsum(ref_counts) / sum(ref_counts)
  ref_cdf_previous <- c(0, head(ref_cdf, -1))
  ref_mid_percentile <- ref_cdf_previous + (ref_counts / sum(ref_counts)) / 2
  ref_percentile <- switch(
    reference_percentile,
    upper_boundary = ref_cdf,
    midpoint = ref_mid_percentile
  )
  measured_cdf_previous <- c(0, head(cumsum(measured_counts) / sum(measured_counts), -1))
  measured_mid_percentile <- measured_cdf_previous +
    (measured_counts / sum(measured_counts)) / 2

  value_4pt_eq <- stats::approx(
    x = ref_percentile,
    y = 1:4,
    xout = measured_mid_percentile,
    method = "linear",
    rule = 2,
    ties = "ordered"
  )$y
  value_4pt_eq <- pmin(4, pmax(1, value_4pt_eq))

  value_4pt_rounded <- as.integer(pmin(4, pmax(1, round(value_4pt_eq))))

  data.frame(
    value_6pt = 1:6,
    measured_n = measured_counts,
    measured_mid_percentile = measured_mid_percentile,
    reference_percentile = reference_percentile,
    value_4pt_eq = value_4pt_eq,
    value_4pt_rounded = value_4pt_rounded,
    stringsAsFactors = FALSE
  )
}

build_embu_c_item_tables <- function(df) {
  c_cols <- embu_item_columns(df, "embu_c")
  tables <- vector("list", length(c_cols))

  for (i in seq_along(c_cols)) {
    col <- c_cols[i]
    ref <- df[df$embu_c_likert_version == "4pt", col, drop = TRUE]
    measured <- df[df$embu_c_likert_version == "6pt", col, drop = TRUE]
    tab <- build_empirical_equip_lookup(ref, measured)
    tab$form <- "EMBU-C"
    tab$item <- col
    tab$method <- "item_empirical_equip_percentile"
    tables[[i]] <- tab[
      c("form", "item", "value_6pt", "measured_n", "measured_mid_percentile",
        "reference_percentile", "value_4pt_eq", "value_4pt_rounded", "method")
    ]
  }

  do.call(rbind, tables)
}

build_embu_p_pooled_table <- function(
  df,
  reference_percentile = c("upper_boundary", "midpoint")
) {
  reference_percentile <- match.arg(reference_percentile)
  c_cols <- embu_item_columns(df, "embu_c")
  ref <- unlist(df[df$embu_c_likert_version == "4pt", c_cols], use.names = FALSE)
  measured <- unlist(df[df$embu_c_likert_version == "6pt", c_cols], use.names = FALSE)
  tab <- build_empirical_equip_lookup(
    ref,
    measured,
    reference_percentile = reference_percentile
  )
  tab$form <- "EMBU-P"
  tab$item <- "pooled_from_embu_c"
  tab$method <- switch(
    reference_percentile,
    upper_boundary = "pooled_embu_c_empirical_equip_percentile",
    midpoint = "pooled_embu_c_midpoint_empirical_equip_percentile"
  )
  tab[
    c("form", "item", "value_6pt", "measured_n", "measured_mid_percentile",
      "reference_percentile", "value_4pt_eq", "value_4pt_rounded", "method")
  ]
}

apply_lookup <- function(values, lookup) {
  values <- as_numeric_vector(values)
  mapped <- rep(NA_integer_, length(values))
  valid <- !is.na(values)
  mapped[valid] <- lookup$value_4pt_rounded[match(values[valid], lookup$value_6pt)]
  mapped
}

convert_embu_likert4 <- function(df) {
  df <- as.data.frame(df, check.names = FALSE)
  p_cols <- embu_item_columns(df, "embu_p")
  c_cols <- embu_item_columns(df, "embu_c")

  if (!"embu_p_likert_version" %in% names(df)) {
    stop("Missing embu_p_likert_version column", call. = FALSE)
  }
  if (!"embu_c_likert_version" %in% names(df)) {
    stop("Missing embu_c_likert_version column", call. = FALSE)
  }

  item_tables <- build_embu_c_item_tables(df)
  pooled_table <- build_embu_p_pooled_table(df, reference_percentile = "upper_boundary")
  pooled_sensitivity_table <- build_embu_p_pooled_table(
    df,
    reference_percentile = "midpoint"
  )

  converted <- df
  converted$embu_p_likert_version_original <- df$embu_p_likert_version
  converted$embu_c_likert_version_original <- df$embu_c_likert_version

  for (col in p_cols) {
    converted[[col]] <- apply_lookup(df[[col]], pooled_table)
  }

  six_pt_rows <- df$embu_c_likert_version == "6pt"
  for (col in c_cols) {
    converted[[col]] <- as_numeric_vector(df[[col]])
    lookup <- item_tables[item_tables$item == col, ]
    converted[[col]][six_pt_rows] <- apply_lookup(df[[col]][six_pt_rows], lookup)
  }

  converted$embu_p_likert_version <- "4pt"
  converted$embu_c_likert_version <- "4pt"
  converted$embu_p_conversion_method <- "pooled_embu_c_equip_percentile_rounded"
  converted$embu_c_conversion_method <- ifelse(
    converted$embu_c_likert_version_original == "4pt",
    "none_original_4pt",
    "item_embu_c_equip_percentile_rounded"
  )
  converted$embu_likert_standardized <- "4pt"

  sensitivity <- converted
  for (col in p_cols) {
    sensitivity[[col]] <- apply_lookup(df[[col]], pooled_sensitivity_table)
  }
  sensitivity$embu_p_conversion_method <-
    "pooled_embu_c_midpoint_equip_percentile_rounded"

  summary <- data.frame(
    metric = c(
      "rows",
      "embu_p_columns_converted",
      "embu_c_columns_standardized",
      "embu_c_original_4pt_rows",
      "embu_c_converted_6pt_rows",
      "max_embu_value_after_conversion",
      "min_embu_value_after_conversion"
    ),
    value = c(
      nrow(converted),
      length(p_cols),
      length(c_cols),
      sum(df$embu_c_likert_version == "4pt", na.rm = TRUE),
      sum(df$embu_c_likert_version == "6pt", na.rm = TRUE),
      max(unlist(converted[c(p_cols, c_cols)]), na.rm = TRUE),
      min(unlist(converted[c(p_cols, c_cols)]), na.rm = TRUE)
    ),
    stringsAsFactors = FALSE
  )

  sensitivity_summary <- data.frame(
    metric = c(
      "rows",
      "embu_p_columns_converted",
      "embu_c_columns_standardized",
      "embu_p_reference_percentile",
      "max_embu_value_after_conversion",
      "min_embu_value_after_conversion"
    ),
    value = c(
      nrow(sensitivity),
      length(p_cols),
      length(c_cols),
      "midpoint",
      max(unlist(sensitivity[c(p_cols, c_cols)]), na.rm = TRUE),
      min(unlist(sensitivity[c(p_cols, c_cols)]), na.rm = TRUE)
    ),
    stringsAsFactors = FALSE
  )

  list(
    data = converted,
    sensitivity_data = sensitivity,
    tables = list(
      item = item_tables,
      pooled = pooled_table,
      pooled_sensitivity = pooled_sensitivity_table
    ),
    summary = summary,
    sensitivity_summary = sensitivity_summary
  )
}

run_embu_likert4 <- function(
  input_path = "data/processed/embu_stage1_standardized.csv",
  output_path = "data/processed/embu_stage2_likert4.csv",
  sensitivity_output_path = "data/processed/embu_stage2_likert4_midpoint_sensitivity.csv",
  item_table_path = "outputs/tables/embu_stage2_embu_c_item_equipercentile.csv",
  pooled_table_path = "outputs/tables/embu_stage2_embu_p_pooled_equipercentile.csv",
  pooled_sensitivity_table_path = "outputs/tables/embu_stage2_embu_p_pooled_midpoint_sensitivity.csv",
  summary_path = "outputs/tables/embu_stage2_likert4_summary.csv",
  sensitivity_summary_path = "outputs/tables/embu_stage2_likert4_midpoint_sensitivity_summary.csv"
) {
  required_package("readr")

  df <- readr::read_csv(input_path, show_col_types = FALSE)
  result <- convert_embu_likert4(df)

  dir.create(dirname(output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(sensitivity_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(item_table_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(pooled_table_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(pooled_sensitivity_table_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(summary_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(sensitivity_summary_path), recursive = TRUE, showWarnings = FALSE)

  readr::write_csv(result$data, output_path, na = "")
  readr::write_csv(result$sensitivity_data, sensitivity_output_path, na = "")
  readr::write_csv(result$tables$item, item_table_path, na = "")
  readr::write_csv(result$tables$pooled, pooled_table_path, na = "")
  readr::write_csv(result$tables$pooled_sensitivity,
                   pooled_sensitivity_table_path, na = "")
  readr::write_csv(result$summary, summary_path, na = "")
  readr::write_csv(result$sensitivity_summary, sensitivity_summary_path, na = "")

  invisible(result)
}
