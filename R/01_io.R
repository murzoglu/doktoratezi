list_raw_data <- function(raw_data_dir) {
  if (!dir.exists(raw_data_dir)) {
    return(data.frame(
      file = character(),
      bytes = numeric(),
      stringsAsFactors = FALSE
    ))
  }

  files <- list.files(raw_data_dir, full.names = TRUE, recursive = FALSE)

  data.frame(
    file = basename(files),
    bytes = file.size(files),
    stringsAsFactors = FALSE
  )
}

canonical_final_reference_paths <- function(processed_data_dir = file.path("data", "processed")) {
  list(
    lock = file.path(processed_data_dir, "FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock"),
    family = file.path(processed_data_dir, "FINAL_REFERENCE__analysis_base_family.csv"),
    long = file.path(processed_data_dir, "FINAL_REFERENCE__analysis_base_long.csv")
  )
}

normalize_reference_path <- function(path) {
  sub("^\\./", "", gsub("\\\\", "/", path))
}

sha256_file <- function(path) {
  if (!requireNamespace("digest", quietly = TRUE)) {
    stop("Required package is not installed: digest", call. = FALSE)
  }
  if (!file.exists(path)) {
    stop(sprintf("File is missing: %s", path), call. = FALSE)
  }
  digest::digest(path, file = TRUE, algo = "sha256")
}

read_final_reference_lock <- function(lock_path) {
  if (!exists("parse_final_reference_lock", mode = "function")) {
    stop("parse_final_reference_lock() is unavailable; source R/07_reproducibility.R first", call. = FALSE)
  }
  if (!file.exists(lock_path)) {
    stop(sprintf("Canonical lock file is missing: %s", lock_path), call. = FALSE)
  }

  lock <- parse_final_reference_lock(readLines(lock_path, warn = FALSE))
  if (!identical(lock$status, "LOCKED_CANONICAL_ANALYSIS_BASE")) {
    stop(sprintf("Unexpected lock status: %s", lock$status), call. = FALSE)
  }
  lock
}

match_final_reference_record <- function(lock, csv_path) {
  if (!is.list(lock) || !"files" %in% names(lock)) {
    stop("lock must be a parsed final-reference lock object", call. = FALSE)
  }

  files <- lock$files
  files$normalized_path <- normalize_reference_path(files$path)
  csv_normalized <- normalize_reference_path(csv_path)

  exact <- files[files$normalized_path == csv_normalized, , drop = FALSE]
  if (nrow(exact) == 1L) {
    exact$normalized_path <- NULL
    return(exact)
  }

  basename_match <- files[basename(files$normalized_path) == basename(csv_normalized), , drop = FALSE]
  if (nrow(basename_match) == 1L) {
    basename_match$normalized_path <- NULL
    return(basename_match)
  }

  if (nrow(basename_match) > 1L) {
    stop(sprintf("Ambiguous final-reference record for: %s", csv_path), call. = FALSE)
  }
  stop(sprintf("No final-reference lock record for: %s", csv_path), call. = FALSE)
}

read_final_reference_csv <- function(csv_path, reader = c("readr", "utils")) {
  reader <- match.arg(reader)
  if (reader == "readr" && requireNamespace("readr", quietly = TRUE)) {
    return(readr::read_csv(csv_path, show_col_types = FALSE, progress = FALSE))
  }

  utils::read.csv(
    csv_path,
    check.names = FALSE,
    stringsAsFactors = FALSE,
    na.strings = c("", "NA")
  )
}

final_reference_file_facts <- function(csv_path, reader = c("readr", "utils")) {
  df <- read_final_reference_csv(csv_path, reader = reader)
  data.frame(
    path = normalize_reference_path(csv_path),
    rows = nrow(df),
    columns = ncol(df),
    sha256 = sha256_file(csv_path),
    stringsAsFactors = FALSE
  )
}

validate_and_load <- function(csv_path, lock_path, reader = c("readr", "utils")) {
  reader <- match.arg(reader)
  lock <- read_final_reference_lock(lock_path)
  expected <- match_final_reference_record(lock, csv_path)
  actual_hash <- sha256_file(csv_path)

  if (!identical(actual_hash, expected$sha256[[1]])) {
    stop(
      sprintf(
        "HASH MISMATCH for %s\n  expected: %s\n  actual: %s",
        csv_path,
        expected$sha256[[1]],
        actual_hash
      ),
      call. = FALSE
    )
  }

  df <- read_final_reference_csv(csv_path, reader = reader)
  actual <- data.frame(
    path = expected$path,
    rows = nrow(df),
    columns = ncol(df),
    sha256 = actual_hash,
    stringsAsFactors = FALSE
  )

  results <- compare_final_reference_facts(expected, actual)
  stop_if_final_reference_invalid(results)

  attr(df, "validated_hash") <- actual_hash
  attr(df, "validation_time") <- format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
  attr(df, "lock_date") <- lock$lock_date
  attr(df, "lock_project") <- lock$project
  attr(df, "canonical_path") <- expected$path[[1]]
  df
}

final_reference_validation_manifest <- function(lock_path, csv_paths = NULL, reader = c("readr", "utils")) {
  reader <- match.arg(reader)
  lock <- read_final_reference_lock(lock_path)

  expected <- if (is.null(csv_paths)) {
    lock$files
  } else {
    do.call(rbind, lapply(csv_paths, function(path) match_final_reference_record(lock, path)))
  }

  actual <- do.call(rbind, lapply(seq_len(nrow(expected)), function(index) {
    path <- expected$path[[index]]
    if (!file.exists(path)) {
      return(data.frame(
        path = path,
        rows = NA_integer_,
        columns = NA_integer_,
        sha256 = NA_character_,
        stringsAsFactors = FALSE
      ))
    }
    facts <- final_reference_file_facts(path, reader = reader)
    facts$path <- path
    facts
  }))

  compare_final_reference_facts(expected, actual)
}

load_final_reference_data <- function(paths = canonical_final_reference_paths(), reader = c("readr", "utils")) {
  reader <- match.arg(reader)
  list(
    family = validate_and_load(paths$family, paths$lock, reader = reader),
    long = validate_and_load(paths$long, paths$lock, reader = reader)
  )
}

required_columns_present <- function(df, required_columns, context) {
  missing_columns <- setdiff(required_columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

prepare_family <- function(df) {
  required_columns_present(
    df,
    c(
      "aile_no",
      "group",
      "katilimci_cocuk_cinsiyet",
      "kardes_cinsiyet",
      "egitim_durumu",
      "cocuk_yas",
      "kardes_yas",
      "katilimci_cocuk_sirasi",
      "kardes_sirasi",
      "dm_yili",
      "hba1c"
    ),
    "family analysis base"
  )

  df$aile_no_f <- factor(df$aile_no)
  df$group_f <- factor(df$group, levels = c("Kontrol", "DM"))
  df$cinsiyet_idx_f <- factor(df$katilimci_cocuk_cinsiyet, levels = 0:1, labels = c("Kiz", "Erkek"))
  df$cinsiyet_sib_f <- factor(df$kardes_cinsiyet, levels = 0:1, labels = c("Kiz", "Erkek"))
  df$egitim_ord <- factor(df$egitim_durumu, levels = 0:5, ordered = TRUE)
  df$age_gap <- abs(as.numeric(df$cocuk_yas) - as.numeric(df$kardes_yas))
  df$same_sex <- factor(
    df$katilimci_cocuk_cinsiyet == df$kardes_cinsiyet,
    levels = c(FALSE, TRUE),
    labels = c("Farkli", "Ayni")
  )
  df$birth_order_diff <- as.numeric(df$katilimci_cocuk_sirasi) - as.numeric(df$kardes_sirasi)
  df$tani_yasi <- ifelse(
    df$group == "DM",
    as.numeric(df$cocuk_yas) - as.numeric(df$dm_yili),
    NA_real_
  )

  hba1c_target <- rep(NA_character_, nrow(df))
  hba1c <- as.numeric(df$hba1c)
  hba1c_target[!is.na(hba1c)] <- ifelse(hba1c[!is.na(hba1c)] <= 7.5, "Hedef_alti", "Hedef_ustu")
  df$hba1c_target <- factor(hba1c_target, levels = c("Hedef_alti", "Hedef_ustu"))
  df
}

prepare_long <- function(df) {
  required_columns_present(
    df,
    c(
      "aile_no",
      "role",
      "group",
      "family_role",
      "katilimci_cocuk_cinsiyet",
      "cocuk_yas"
    ),
    "long analysis base"
  )

  df$aile_no_f <- factor(df$aile_no)
  df$role_f <- factor(
    df$role,
    levels = c("Kontrol_Indeks", "Kontrol_Kardes", "DM_Hasta_Indeks", "DM_Hasta_Kardes")
  )
  df$group_f <- factor(df$group, levels = c("Kontrol", "DM"))
  df$family_role_f <- factor(df$family_role, levels = c("index", "sibling"))
  df$cinsiyet_f <- factor(df$katilimci_cocuk_cinsiyet, levels = 0:1, labels = c("Kiz", "Erkek"))
  df$age_cat <- cut(
    as.numeric(df$cocuk_yas),
    breaks = c(7, 11, 14, 18),
    labels = c("7-10", "11-13", "14-17"),
    include.lowest = TRUE,
    right = FALSE
  )
  df
}

summarize_loaded_final_reference <- function(df_family_raw, df_long_raw, df_family, df_long) {
  data.frame(
    dataset = c("family", "long"),
    raw_rows = c(nrow(df_family_raw), nrow(df_long_raw)),
    raw_columns = c(ncol(df_family_raw), ncol(df_long_raw)),
    prepared_rows = c(nrow(df_family), nrow(df_long)),
    prepared_columns = c(ncol(df_family), ncol(df_long)),
    validated_hash = c(attr(df_family_raw, "validated_hash"), attr(df_long_raw, "validated_hash")),
    lock_date = c(attr(df_family_raw, "lock_date"), attr(df_long_raw, "lock_date")),
    canonical_path = c(attr(df_family_raw, "canonical_path"), attr(df_long_raw, "canonical_path")),
    stringsAsFactors = FALSE
  )
}
