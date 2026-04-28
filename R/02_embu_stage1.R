required_package <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    stop(sprintf("Required package is not installed: %s", package), call. = FALSE)
  }
}

clean_column_names <- function(x) {
  required_package("janitor")
  janitor::make_clean_names(x)
}

extract_first_integer <- function(x, pattern) {
  match <- regexpr(pattern, x, perl = TRUE)
  value <- regmatches(x, match)
  suppressWarnings(as.integer(gsub("\\D+", "", value)))
}

as_numeric_response <- function(x) {
  if (is.numeric(x)) {
    return(x)
  }

  x <- trimws(as.character(x))
  x[x == ""] <- NA_character_
  suppressWarnings(as.numeric(gsub(",", ".", x, fixed = TRUE)))
}

find_embu_columns <- function(names_raw) {
  p_cols <- grep("^EMBU-P", names_raw)
  c_cols <- grep("^\\(EMBU-C\\)", names_raw)

  if (length(p_cols) != 29) {
    stop(sprintf("Expected 29 EMBU-P columns, found %d", length(p_cols)),
         call. = FALSE)
  }
  if (length(c_cols) != 29) {
    stop(sprintf("Expected 29 EMBU-C columns, found %d", length(c_cols)),
         call. = FALSE)
  }

  p_q <- extract_first_integer(names_raw[p_cols], "Soru\\s*\\d+")
  c_q <- extract_first_integer(names_raw[c_cols], "\\(EMBU-C\\)\\s*\\d+")

  if (!identical(sort(p_q), 1:29)) {
    stop("EMBU-P question numbers must be unique and cover 1:29",
         call. = FALSE)
  }
  if (!identical(sort(c_q), 1:29)) {
    stop("EMBU-C question numbers must be unique and cover 1:29",
         call. = FALSE)
  }

  list(
    p_cols = p_cols,
    c_cols = c_cols,
    p_q = p_q,
    c_q = c_q
  )
}

align_embu_c_question_numbers <- function(q_numbers) {
  aligned <- as.integer(q_numbers)
  aligned[q_numbers == 8] <- 7L
  aligned[q_numbers == 9] <- 8L
  aligned[q_numbers == 10] <- 9L
  aligned[q_numbers == 7] <- 10L

  if (!identical(sort(as.integer(aligned)), 1:29)) {
    stop("Aligned EMBU-C question numbers must be unique and cover 1:29",
         call. = FALSE)
  }

  aligned
}

standardize_embu_matrix <- function(raw, cols, q_numbers, prefix) {
  out <- setNames(
    vector("list", 29),
    paste0(prefix, "_q", sprintf("%02d", 1:29))
  )
  outlier_frames <- list()

  for (q in 1:29) {
    source_col <- cols[which(q_numbers == q)]
    item_name <- paste0(prefix, "_q", sprintf("%02d", q))
    values <- as_numeric_response(raw[[source_col]])
    invalid <- !is.na(values) & !(values %in% 1:6)

    out[[item_name]] <- replace(values, invalid, NA_real_)

    if (any(invalid)) {
      outlier_frames[[length(outlier_frames) + 1]] <- data.frame(
        source_row_number = which(invalid),
        form = if (identical(prefix, "embu_p")) "EMBU-P" else "EMBU-C",
        item = item_name,
        raw_value = values[invalid],
        clean_action = "set_to_na_stage1_range_validation",
        stringsAsFactors = FALSE
      )
    }
  }

  list(
    data = as.data.frame(out, check.names = FALSE),
    outliers = do.call(rbind, outlier_frames)
  )
}

classify_embu_c_likert <- function(embu_c) {
  apply(embu_c, 1, function(row) {
    row <- row[!is.na(row)]
    if (length(row) == 0) {
      return(NA_character_)
    }
    if (max(row) <= 4) {
      return("4pt")
    }
    "6pt"
  })
}

mark_mixed_likert_families <- function(aile_no, likert_version) {
  if (is.null(aile_no)) {
    return(rep(FALSE, length(likert_version)))
  }

  family_keys <- as.character(aile_no)
  mixed <- tapply(likert_version, family_keys, function(x) {
    length(unique(x[!is.na(x)])) > 1
  })
  as.logical(mixed[family_keys])
}

standardize_embu_stage1 <- function(raw) {
  raw <- as.data.frame(raw, check.names = FALSE)
  names_raw <- names(raw)
  embu_cols <- find_embu_columns(names_raw)

  source_row_number <- seq_len(nrow(raw))

  non_embu_cols <- setdiff(seq_along(raw), c(embu_cols$p_cols, embu_cols$c_cols))
  non_embu <- raw[non_embu_cols]
  names(non_embu) <- clean_column_names(names(non_embu))
  pii_cols <- grepl("ad.*soyad", names(non_embu), perl = TRUE)
  non_embu <- non_embu[!pii_cols]

  embu_p <- standardize_embu_matrix(
    raw = raw,
    cols = embu_cols$p_cols,
    q_numbers = embu_cols$p_q,
    prefix = "embu_p"
  )
  embu_c_q <- align_embu_c_question_numbers(embu_cols$c_q)
  embu_c <- standardize_embu_matrix(
    raw = raw,
    cols = embu_cols$c_cols,
    q_numbers = embu_c_q,
    prefix = "embu_c"
  )

  outlier_report <- rbind(embu_p$outliers, embu_c$outliers)

  aile_no <- if ("aile_no" %in% names(non_embu)) non_embu$aile_no else NULL
  cocuk_no <- if ("cocuk_no" %in% names(non_embu)) non_embu$cocuk_no else NULL

  if (!is.null(outlier_report) && nrow(outlier_report) > 0) {
    outlier_report$aile_no <- if (is.null(aile_no)) NA else aile_no[outlier_report$source_row_number]
    outlier_report$cocuk_no <- if (is.null(cocuk_no)) NA else cocuk_no[outlier_report$source_row_number]
    outlier_report <- outlier_report[
      c("source_row_number", "aile_no", "cocuk_no", "form", "item",
        "raw_value", "clean_action")
    ]
  } else {
    outlier_report <- data.frame(
      source_row_number = integer(),
      aile_no = character(),
      cocuk_no = character(),
      form = character(),
      item = character(),
      raw_value = numeric(),
      clean_action = character(),
      stringsAsFactors = FALSE
    )
  }

  embu_c_likert_version <- classify_embu_c_likert(embu_c$data)
  embu_c_family_mixed_likert <- mark_mixed_likert_families(
    aile_no = aile_no,
    likert_version = embu_c_likert_version
  )

  embu_p_outlier_n <- rowSums(is.na(embu_p$data) &
                                !is.na(as.data.frame(lapply(
                                  raw[embu_cols$p_cols[order(embu_cols$p_q)]],
                                  as_numeric_response
                                ))))
  embu_c_outlier_n <- rowSums(is.na(embu_c$data) &
                                !is.na(as.data.frame(lapply(
                                  raw[embu_cols$c_cols[order(embu_c_q)]],
                                  as_numeric_response
                                ))))

  clean <- data.frame(
    source_row_number = source_row_number,
    non_embu,
    embu_p$data,
    embu_c$data,
    embu_p_likert_version = rep("6pt", nrow(raw)),
    embu_c_likert_version = embu_c_likert_version,
    embu_p_outlier_n = embu_p_outlier_n,
    embu_c_outlier_n = embu_c_outlier_n,
    embu_outlier_n = embu_p_outlier_n + embu_c_outlier_n,
    embu_c_family_mixed_likert = embu_c_family_mixed_likert,
    check.names = FALSE
  )

  likert_counts <- table(clean$embu_c_likert_version, useNA = "ifany")
  mixed_family_count <- length(unique(as.character(aile_no[embu_c_family_mixed_likert])))

  summary <- data.frame(
    metric = c(
      "rows",
      "families",
      "embu_p_columns",
      "embu_c_columns",
      "embu_p_outlier_cells",
      "embu_c_outlier_cells",
      "embu_c_4pt_rows",
      "embu_c_6pt_rows",
      "embu_c_mixed_likert_families"
    ),
    value = c(
      nrow(clean),
      if (is.null(aile_no)) NA_integer_ else length(unique(aile_no)),
      29,
      29,
      sum(embu_p_outlier_n),
      sum(embu_c_outlier_n),
      unname(likert_counts["4pt"] %||% 0),
      unname(likert_counts["6pt"] %||% 0),
      mixed_family_count
    ),
    stringsAsFactors = FALSE
  )

  mixed_families <- data.frame(
    aile_no = if (is.null(aile_no)) character() else
      sort(unique(as.character(aile_no[embu_c_family_mixed_likert]))),
    stringsAsFactors = FALSE
  )

  list(
    data = clean,
    outliers = outlier_report,
    summary = summary,
    mixed_families = mixed_families
  )
}

`%||%` <- function(x, y) {
  if (is.na(x)) y else x
}

run_embu_stage1 <- function(
  input_path = "data/raw/Raw Data - Final.csv",
  output_path = "data/processed/embu_stage1_standardized.csv",
  outlier_path = "outputs/tables/embu_stage1_outliers.csv",
  summary_path = "outputs/tables/embu_stage1_summary.csv",
  mixed_family_path = "outputs/tables/embu_stage1_mixed_likert_families.csv"
) {
  required_package("readr")

  raw <- readr::read_csv(
    input_path,
    locale = readr::locale(encoding = "UTF-8"),
    name_repair = "minimal",
    show_col_types = FALSE
  )

  result <- standardize_embu_stage1(raw)

  dir.create(dirname(output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(outlier_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(summary_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(mixed_family_path), recursive = TRUE, showWarnings = FALSE)

  readr::write_csv(result$data, output_path, na = "")
  readr::write_csv(result$outliers, outlier_path, na = "")
  readr::write_csv(result$summary, summary_path, na = "")
  readr::write_csv(result$mixed_families, mixed_family_path, na = "")

  invisible(result)
}
