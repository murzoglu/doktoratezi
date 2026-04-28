score_min_present_pct <- function() {
  0.50
}

score_required_columns_present <- function(df, required_columns, context) {
  missing_columns <- setdiff(required_columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

embu_subscale_map <- function() {
  list(
    sicaklik = c(1, 3, 6, 7, 13, 17, 20, 24, 26),
    asiri_koruma = c(4, 8, 14, 15, 19, 23, 25),
    reddetme = c(5, 9, 10, 12, 16, 21, 22, 28),
    karsilastirma = c(2, 11, 18, 27, 29)
  )
}

srq_first_order_map <- function() {
  list(
    intimacy = c(1, 17, 33),
    prosocial = c(3, 19, 35),
    companionship = c(9, 25, 41),
    similarity = c(10, 26, 42),
    admiration_by_sib = c(12, 28, 44),
    admiration_of_sib = c(11, 27, 43),
    affection = c(16, 32, 48),
    nurturance_by_sib = c(8, 24, 40),
    nurturance_of_sib = c(15, 31, 47),
    dominance_by_sib = c(7, 23, 39),
    dominance_of_sib = c(2, 18, 34),
    quarreling = c(4, 20, 36),
    antagonism = c(6, 22, 38),
    competition = c(5, 21, 37),
    maternal_partiality = c(14, 30, 46),
    paternal_partiality = c(13, 29, 45)
  )
}

srq_higher_order_map <- function(first_order = srq_first_order_map()) {
  list(
    warmth = unlist(first_order[c(
      "intimacy",
      "prosocial",
      "companionship",
      "similarity",
      "admiration_by_sib",
      "admiration_of_sib",
      "affection"
    )], use.names = FALSE),
    status = unlist(first_order[c(
      "nurturance_by_sib",
      "nurturance_of_sib",
      "dominance_by_sib",
      "dominance_of_sib"
    )], use.names = FALSE),
    conflict = unlist(first_order[c("quarreling", "antagonism", "competition")], use.names = FALSE),
    rivalry = unlist(first_order[c("maternal_partiality", "paternal_partiality")], use.names = FALSE)
  )
}

embu_score_item_columns <- function(prefix, items = 1:29) {
  paste0(prefix, "_q", sprintf("%02d", items))
}

srq_score_item_columns <- function(prefix = "srq", items = 1:48) {
  paste0(prefix, "_", items)
}

beck_score_item_columns <- function(prefix = "beck", items = 1:21) {
  paste0(prefix, "_", items)
}

score_numeric_frame <- function(df, columns, context) {
  score_required_columns_present(df, columns, context)
  out <- df[columns]
  for (column in columns) {
    out[[column]] <- suppressWarnings(as.numeric(out[[column]]))
  }
  out
}

derive_subscale_scores <- function(df, item_columns_map, score_prefix,
                                   min_present_pct = score_min_present_pct()) {
  if (!is.list(item_columns_map) || length(item_columns_map) == 0L) {
    stop("item_columns_map must be a non-empty named list", call. = FALSE)
  }
  if (any(!nzchar(names(item_columns_map)))) {
    stop("item_columns_map must be named", call. = FALSE)
  }
  if (!is.numeric(min_present_pct) || length(min_present_pct) != 1L ||
      is.na(min_present_pct) || min_present_pct <= 0 || min_present_pct > 1) {
    stop("min_present_pct must be in (0, 1]", call. = FALSE)
  }

  out <- df
  for (subscale in names(item_columns_map)) {
    columns <- item_columns_map[[subscale]]
    numeric_items <- score_numeric_frame(
      out,
      columns,
      sprintf("%s/%s", score_prefix, subscale)
    )
    valid_n <- rowSums(!is.na(numeric_items))
    required_n <- ceiling(length(columns) * min_present_pct)
    means <- rowMeans(numeric_items, na.rm = TRUE)
    means[valid_n < required_n | is.nan(means)] <- NA_real_

    complete_sum <- rowSums(numeric_items)
    complete_sum[valid_n < length(columns)] <- NA_real_

    out[[paste0(score_prefix, "_", subscale, "_valid_n")]] <- valid_n
    out[[paste0(score_prefix, "_", subscale, "_missing_n")]] <- length(columns) - valid_n
    out[[paste0(score_prefix, "_", subscale, "_sum_complete")]] <- complete_sum
    out[[paste0(score_prefix, "_", subscale, "_mean")]] <- means
  }
  out
}

derive_embu_scores <- function(df, item_prefix, score_prefix = item_prefix,
                               min_present_pct = score_min_present_pct()) {
  item_columns_map <- lapply(embu_subscale_map(), function(items) {
    embu_score_item_columns(item_prefix, items)
  })
  derive_subscale_scores(df, item_columns_map, score_prefix, min_present_pct)
}

derive_srq_first_order_scores <- function(df, item_prefix = "srq", score_prefix = paste0(item_prefix, "_fo"),
                                          min_present_pct = score_min_present_pct()) {
  item_columns_map <- lapply(srq_first_order_map(), function(items) {
    srq_score_item_columns(item_prefix, items)
  })
  derive_subscale_scores(df, item_columns_map, score_prefix, min_present_pct)
}

derive_srq_higher_order_scores <- function(df, item_prefix = "srq", score_prefix = paste0(item_prefix, "_ho"),
                                           min_present_pct = score_min_present_pct()) {
  item_columns_map <- lapply(srq_higher_order_map(), function(items) {
    srq_score_item_columns(item_prefix, items)
  })
  derive_subscale_scores(df, item_columns_map, score_prefix, min_present_pct)
}

derive_srq_scores <- function(df, item_prefix = "srq", score_prefix = item_prefix,
                              min_present_pct = score_min_present_pct()) {
  out <- derive_srq_first_order_scores(
    df,
    item_prefix = item_prefix,
    score_prefix = paste0(score_prefix, "_fo"),
    min_present_pct = min_present_pct
  )
  derive_srq_higher_order_scores(
    out,
    item_prefix = item_prefix,
    score_prefix = paste0(score_prefix, "_ho"),
    min_present_pct = min_present_pct
  )
}

derive_beck_scores <- function(df, item_prefix = "beck", score_prefix = "beck") {
  columns <- beck_score_item_columns(item_prefix)
  numeric_items <- score_numeric_frame(df, columns, score_prefix)
  valid_n <- rowSums(!is.na(numeric_items))
  total <- rowSums(numeric_items)
  total[valid_n < length(columns)] <- NA_real_

  out <- df
  out[[paste0(score_prefix, "_valid_n")]] <- valid_n
  out[[paste0(score_prefix, "_missing_n")]] <- length(columns) - valid_n
  out[[paste0(score_prefix, "_total")]] <- total
  out[[paste0(score_prefix, "_severity")]] <- cut(
    total,
    breaks = c(-1, 9, 16, 29, 63),
    labels = c("Minimal", "Hafif", "Orta", "Siddetli"),
    include.lowest = TRUE,
    right = TRUE
  )

  clinical <- rep(NA_character_, length(total))
  clinical[!is.na(total)] <- ifelse(total[!is.na(total)] >= 17, "Klinik_duzey", "Klinik_alti")
  out[[paste0(score_prefix, "_clinical")]] <- factor(
    clinical,
    levels = c("Klinik_alti", "Klinik_duzey")
  )
  out
}

derive_family_scores <- function(df_family, min_present_pct = score_min_present_pct()) {
  out <- df_family
  out <- derive_embu_scores(out, "embu_p", "embu_p", min_present_pct)
  out <- derive_embu_scores(out, "embu_c_idx", "embu_c_idx", min_present_pct)
  out <- derive_embu_scores(out, "embu_c_sib", "embu_c_sib", min_present_pct)
  out <- derive_srq_scores(out, "srq", "srq", min_present_pct)
  out <- derive_srq_scores(out, "srq_sib", "srq_sib", min_present_pct)
  out <- derive_beck_scores(out, "beck", "beck")
  out
}

derive_long_scores <- function(df_long, min_present_pct = score_min_present_pct()) {
  out <- df_long
  out <- derive_embu_scores(out, "embu_c", "embu_c", min_present_pct)
  out <- derive_srq_scores(out, "srq", "srq", min_present_pct)
  out <- derive_beck_scores(out, "beck", "beck")
  out
}

score_range_block <- function(df, columns, item_min, item_max, dataset, instrument, block) {
  numeric_items <- score_numeric_frame(df, columns, sprintf("%s/%s", dataset, block))
  values <- unlist(numeric_items, use.names = FALSE)
  observed <- values[!is.na(values)]
  out_of_range <- observed[observed < item_min | observed > item_max]
  data.frame(
    dataset = dataset,
    instrument = instrument,
    block = block,
    n_items = length(columns),
    n_values = length(observed),
    n_out_of_range = length(out_of_range),
    min_observed = if (length(observed) > 0L) min(observed) else NA_real_,
    max_observed = if (length(observed) > 0L) max(observed) else NA_real_,
    expected_min = item_min,
    expected_max = item_max,
    stringsAsFactors = FALSE
  )
}

score_range_audit <- function(df_family, df_long) {
  do.call(rbind, list(
    score_range_block(df_family, embu_score_item_columns("embu_p"), 1, 4, "family", "EMBU-P", "embu_p"),
    score_range_block(df_family, embu_score_item_columns("embu_c_idx"), 1, 4, "family", "EMBU-C", "embu_c_idx"),
    score_range_block(df_family, embu_score_item_columns("embu_c_sib"), 1, 4, "family", "EMBU-C", "embu_c_sib"),
    score_range_block(df_family, srq_score_item_columns("srq"), 1, 5, "family", "SRQ", "srq"),
    score_range_block(df_family, srq_score_item_columns("srq_sib"), 1, 5, "family", "SRQ", "srq_sib"),
    score_range_block(df_family, beck_score_item_columns("beck"), 0, 3, "family", "BDI", "beck"),
    score_range_block(df_long, embu_score_item_columns("embu_c"), 1, 4, "long", "EMBU-C", "embu_c"),
    score_range_block(df_long, srq_score_item_columns("srq"), 1, 5, "long", "SRQ", "srq"),
    score_range_block(df_long, beck_score_item_columns("beck"), 0, 3, "long", "BDI", "beck")
  ))
}

assert_no_score_range_violations <- function(range_audit) {
  violations <- range_audit[range_audit$n_out_of_range > 0L, , drop = FALSE]
  if (nrow(violations) == 0L) {
    return(invisible(TRUE))
  }

  details <- paste(
    sprintf(
      "%s/%s/%s: n_out_of_range=%d expected=[%s,%s] observed=[%s,%s]",
      violations$dataset,
      violations$instrument,
      violations$block,
      violations$n_out_of_range,
      violations$expected_min,
      violations$expected_max,
      violations$min_observed,
      violations$max_observed
    ),
    collapse = "\n"
  )
  stop(sprintf("Score item range violation(s):\n%s", details), call. = FALSE)
}

score_definition_rows <- function(dataset, instrument, level, item_prefix, score_prefix,
                                  map, item_column_fn, min_present_pct) {
  rows <- lapply(names(map), function(subscale) {
    columns <- item_column_fn(item_prefix, map[[subscale]])
    data.frame(
      dataset = dataset,
      instrument = instrument,
      level = level,
      item_prefix = item_prefix,
      score_prefix = score_prefix,
      subscale = subscale,
      n_items = length(columns),
      item_columns = paste(columns, collapse = ";"),
      valid_n_column = paste0(score_prefix, "_", subscale, "_valid_n"),
      missing_n_column = paste0(score_prefix, "_", subscale, "_missing_n"),
      sum_column = paste0(score_prefix, "_", subscale, "_sum_complete"),
      mean_column = paste0(score_prefix, "_", subscale, "_mean"),
      min_present_pct = min_present_pct,
      sum_rule = "complete_items_only",
      mean_rule = "available_items_if_threshold_met",
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

beck_definition_row <- function(dataset) {
  data.frame(
    dataset = dataset,
    instrument = "BDI",
    level = "total",
    item_prefix = "beck",
    score_prefix = "beck",
    subscale = "total",
    n_items = 21L,
    item_columns = paste(beck_score_item_columns("beck"), collapse = ";"),
    valid_n_column = "beck_valid_n",
    missing_n_column = "beck_missing_n",
    sum_column = "beck_total",
    mean_column = NA_character_,
    min_present_pct = 1,
    sum_rule = "complete_items_only",
    mean_rule = "not_applicable",
    stringsAsFactors = FALSE
  )
}

derived_score_dictionary <- function(min_present_pct = score_min_present_pct()) {
  embu <- embu_subscale_map()
  srq_fo <- srq_first_order_map()
  srq_ho <- srq_higher_order_map(srq_fo)

  do.call(rbind, list(
    score_definition_rows("family", "EMBU-P", "subscale", "embu_p", "embu_p", embu, embu_score_item_columns, min_present_pct),
    score_definition_rows("family", "EMBU-C", "subscale", "embu_c_idx", "embu_c_idx", embu, embu_score_item_columns, min_present_pct),
    score_definition_rows("family", "EMBU-C", "subscale", "embu_c_sib", "embu_c_sib", embu, embu_score_item_columns, min_present_pct),
    score_definition_rows("family", "SRQ", "first_order", "srq", "srq_fo", srq_fo, srq_score_item_columns, min_present_pct),
    score_definition_rows("family", "SRQ", "higher_order", "srq", "srq_ho", srq_ho, srq_score_item_columns, min_present_pct),
    score_definition_rows("family", "SRQ", "first_order", "srq_sib", "srq_sib_fo", srq_fo, srq_score_item_columns, min_present_pct),
    score_definition_rows("family", "SRQ", "higher_order", "srq_sib", "srq_sib_ho", srq_ho, srq_score_item_columns, min_present_pct),
    beck_definition_row("family"),
    score_definition_rows("long", "EMBU-C", "subscale", "embu_c", "embu_c", embu, embu_score_item_columns, min_present_pct),
    score_definition_rows("long", "SRQ", "first_order", "srq", "srq_fo", srq_fo, srq_score_item_columns, min_present_pct),
    score_definition_rows("long", "SRQ", "higher_order", "srq", "srq_ho", srq_ho, srq_score_item_columns, min_present_pct),
    beck_definition_row("long")
  ))
}

score_columns_from_dictionary <- function(dictionary) {
  unique(na.omit(c(
    dictionary$valid_n_column,
    dictionary$missing_n_column,
    dictionary$sum_column,
    dictionary$mean_column
  )))
}

score_coverage <- function(scored_df, score_columns, dataset) {
  columns <- intersect(score_columns, names(scored_df))
  rows <- lapply(columns, function(column) {
    values <- scored_df[[column]]
    numeric_values <- if (is.numeric(values) || is.integer(values)) values else rep(NA_real_, length(values))
    data.frame(
      dataset = dataset,
      score_column = column,
      class = paste(class(values), collapse = ";"),
      n_rows = length(values),
      non_missing_n = sum(!is.na(values)),
      missing_n = sum(is.na(values)),
      mean = if (is.numeric(values) || is.integer(values)) mean(numeric_values, na.rm = TRUE) else NA_real_,
      sd = if ((is.numeric(values) || is.integer(values)) && sum(!is.na(numeric_values)) > 1L) stats::sd(numeric_values, na.rm = TRUE) else NA_real_,
      min = if (is.numeric(values) || is.integer(values)) suppressWarnings(min(numeric_values, na.rm = TRUE)) else NA_real_,
      max = if (is.numeric(values) || is.integer(values)) suppressWarnings(max(numeric_values, na.rm = TRUE)) else NA_real_,
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)
  numeric_empty <- is.infinite(out$min) | is.infinite(out$max)
  out$min[numeric_empty] <- NA_real_
  out$max[numeric_empty] <- NA_real_
  out
}

summarize_derived_score_targets <- function(df_family, df_long, df_family_scored, df_long_scored) {
  data.frame(
    dataset = c("family", "long"),
    input_rows = c(nrow(df_family), nrow(df_long)),
    input_columns = c(ncol(df_family), ncol(df_long)),
    scored_rows = c(nrow(df_family_scored), nrow(df_long_scored)),
    scored_columns = c(ncol(df_family_scored), ncol(df_long_scored)),
    added_columns = c(
      ncol(df_family_scored) - ncol(df_family),
      ncol(df_long_scored) - ncol(df_long)
    ),
    stringsAsFactors = FALSE
  )
}
