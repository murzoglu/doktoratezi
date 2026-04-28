required_package <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    stop(sprintf("Required package is not installed: %s", package), call. = FALSE)
  }
}

stage3_embu_p_columns <- function(df) {
  grep("^embu_p_q\\d{2}$", names(df), value = TRUE)
}

stage3_embu_c_columns <- function(df) {
  grep("^embu_c_q\\d{2}$", names(df), value = TRUE)
}

stage3_beck_columns <- function(df) {
  grep("^beck_\\d+$", names(df), value = TRUE)
}

stage3_kia_columns <- function(df) {
  grep("^kia_\\d+$", names(df), value = TRUE)
}

stage3_srq_columns <- function(df) {
  grep("^srq_\\d+$", names(df), value = TRUE)
}

stage3_embu_p_meta_columns <- function(df) {
  grep("^embu_p_(likert|conversion|outlier)", names(df), value = TRUE)
}

stage3_embu_c_meta_columns <- function(df) {
  grep("^embu_c_(likert|conversion|outlier|family_mixed)", names(df),
       value = TRUE)
}

stage3_embu_common_meta_columns <- function(df) {
  intersect(c("embu_outlier_n", "embu_likert_standardized"), names(df))
}

stage3_default_index_authority_family_ids <- function() {
  c(5, 15, 78, 2005, 2009, 2316)
}

stage3_default_dm_diagnosis_corrections <- function() {
  data.frame(
    aile_no = c(5, 11, 14),
    dm_tani_tarihi = c("05.09.2018", "30.03.2017", "03.02.2012"),
    correction_source = rep("raw_data_lookup", 3),
    stringsAsFactors = FALSE
  )
}

stage3_default_survey_date_corrections <- function() {
  data.frame(
    aile_no = c(
      3, 12, 22, 33, 83, 303, 400, 901, 1001, 1007, 1101,
      1105, 1110, 1200, 1218, 1219, 2027, 2030, 2034,
      2304, 2306
    ),
    anket_tarihi = c(
      "02.09.2023", "14.03.2023", "02.10.2023", "03.08.2023",
      "08.07.2025", "14.08.2024", "14.11.2024", "02.05.2025",
      "15.06.2023", "24.07.2025", "06.09.2024", "10.06.2025",
      "11.07.2025", "23.09.2025", "25.12.2025", "13.10.2025",
      "07.08.2024", "08.08.2025", "10.08.2025", "22.03.2023",
      "03.09.2025"
    ),
    correction_source = rep("raw_data_lookup", 21),
    stringsAsFactors = FALSE
  )
}

stage3_default_child_birth_date_corrections <- function() {
  data.frame(
    cocuk_no = c(
      "607-4", "1007-1", "1200-3", "1202-3", "1219-4",
      "1242-2", "2027-2", "2030-2", "2034-2", "2306-2"
    ),
    katilimci_cocuk_dogum_tarihi = c(
      "09.07.2015", "20.04.2018", "17.09.2018", "30.10.2008",
      "13.09.2018", "22.11.2008", "07.10.2016", "08.11.2009",
      "06.10.2016", "03.09.2012"
    ),
    correction_source = rep("raw_data_lookup", 10),
    stringsAsFactors = FALSE
  )
}

stage3_final_reference_paths <- function() {
  c(
    long = "data/processed/FINAL_REFERENCE__analysis_base_long.csv",
    family = "data/processed/FINAL_REFERENCE__analysis_base_family.csv"
  )
}

stage3_anne_demography_columns <- function(df) {
  candidates <- c(
    "anne_dogum_tarihi",
    "anne_antidepresan",
    "cocuk_sayisi",
    "medeni_durum",
    "es_sag",
    "es_dogum_tarihi",
    "egitim_durumu",
    "es_egitim_durumu",
    "calisma_durumu",
    "calistigi_is",
    "es_calisma_durumu",
    "es_calistigi_is",
    "ev_sahipligi",
    "ev_oda_sayisi",
    "arabaniz_var_mi",
    "kronik_hastalik_durumu",
    "hastalik_engel",
    "esiniz_kronik_hastalik_durumu",
    "es_hastalik_engel"
  )
  intersect(candidates, names(df))
}

stage3_family_level_columns <- function(df) {
  candidates <- c(
    "anket_tarihi",
    stage3_anne_demography_columns(df)
  )
  intersect(candidates, names(df))
}

normalize_stage3_literal_missing_values <- function(df) {
  for (col in names(df)) {
    if (is.character(df[[col]]) || is.factor(df[[col]])) {
      values <- as.character(df[[col]])
      values[trimws(values) %in% c("#N/A", "?")] <- NA_character_
      df[[col]] <- values
    }
  }
  df
}

reverse_stage3_binary_01 <- function(x) {
  values <- suppressWarnings(as.integer(as.character(x)))
  valid <- !is.na(values) & values %in% c(0L, 1L)
  values[valid] <- 1L - values[valid]
  values
}

standardize_stage3_chronic_binary_codes <- function(df) {
  chronic_cols <- intersect(
    c("kronik_hastalik_durumu", "esiniz_kronik_hastalik_durumu"),
    names(df)
  )
  for (col in chronic_cols) {
    df[[col]] <- reverse_stage3_binary_01(df[[col]])
  }
  df
}

stage3_validate_columns <- function(df) {
  required <- c("aile_no", "katilimci_cocuk")
  missing <- setdiff(required, names(df))
  if (length(missing) > 0) {
    stop(sprintf("Missing required columns: %s", paste(missing, collapse = ", ")),
         call. = FALSE)
  }

  p_cols <- stage3_embu_p_columns(df)
  c_cols <- stage3_embu_c_columns(df)
  beck_cols <- stage3_beck_columns(df)

  if (length(p_cols) != 29) {
    stop(sprintf("Expected 29 EMBU-P item columns, found %d", length(p_cols)),
         call. = FALSE)
  }
  if (length(c_cols) != 29) {
    stop(sprintf("Expected 29 EMBU-C item columns, found %d", length(c_cols)),
         call. = FALSE)
  }
  if (length(beck_cols) == 0) {
    stop("No Beck columns found", call. = FALSE)
  }
}

add_stage3_roles <- function(df) {
  participant <- suppressWarnings(as.integer(df$katilimci_cocuk))
  if (any(!participant %in% 1:4, na.rm = TRUE)) {
    stop("katilimci_cocuk must use codes 1, 2, 3, 4", call. = FALSE)
  }

  df$is_index <- participant %in% c(1, 3)
  df$family_role <- ifelse(df$is_index, "index", "sibling")
  df$role <- ifelse(
    participant == 1, "DM_Hasta_Indeks",
    ifelse(
      participant == 2, "DM_Hasta_Kardes",
      ifelse(participant == 3, "Kontrol_Indeks", "Kontrol_Kardes")
    )
  )
  df$group <- ifelse(participant %in% c(1, 2), "DM", "Kontrol")
  df
}

harmonize_stage3_family_level_fields <- function(df) {
  if (!all(c("aile_no", "is_index") %in% names(df))) {
    return(df)
  }

  family_cols <- stage3_family_level_columns(df)
  if (length(family_cols) == 0) {
    return(df)
  }

  for (family_id in unique(df$aile_no)) {
    rows <- which(df$aile_no == family_id)
    index_row <- rows[df$is_index[rows]]
    if (length(index_row) != 1) {
      next
    }
    for (col in family_cols) {
      df[rows, col] <- df[index_row, col]
    }
  }

  df
}

parse_stage3_date <- function(x) {
  if (inherits(x, "Date")) {
    return(x)
  }

  x <- trimws(as.character(x))
  x[x == ""] <- NA_character_

  parsed <- as.Date(x, format = "%d.%m.%Y")
  missing <- is.na(parsed)
  parsed[missing] <- as.Date(x[missing], format = "%Y-%m-%d")
  parsed
}

add_stage3_derived_dates <- function(df) {
  survey_date <- parse_stage3_date(df$anket_tarihi)
  child_birth_date <- parse_stage3_date(df$katilimci_cocuk_dogum_tarihi)
  mother_birth_date <- parse_stage3_date(df$anne_dogum_tarihi)
  dm_diagnosis_date <- parse_stage3_date(df$dm_tani_tarihi)

  df$cocuk_yas <- as.numeric(survey_date - child_birth_date) / 365.25
  df$anne_yas <- as.numeric(survey_date - mother_birth_date) / 365.25
  df$dm_yili <- ifelse(
    df$role == "DM_Hasta_Indeks",
    as.numeric(survey_date - dm_diagnosis_date) / 365.25,
    NA_real_
  )
  df
}

empty_stage3_outlier_report <- function() {
  data.frame(
    source_row_number = numeric(),
    aile_no = numeric(),
    katilimci_cocuk = numeric(),
    role = character(),
    instrument = character(),
    item = character(),
    raw_value = numeric(),
    cleaned_value = numeric(),
    stringsAsFactors = FALSE
  )
}

build_stage3_outlier_report <- function(df) {
  reports <- list()
  beck_cols <- stage3_beck_columns(df)
  kia_cols <- stage3_kia_columns(df)

  if (length(beck_cols) > 0) {
    beck_values <- as.matrix(df[beck_cols])
    beck_outliers <- which(!is.na(beck_values) &
                             (beck_values < 0 | beck_values > 3),
                           arr.ind = TRUE)
    if (nrow(beck_outliers) > 0) {
      reports[[length(reports) + 1]] <- data.frame(
        source_row_number = df$source_row_number[beck_outliers[, "row"]],
        aile_no = df$aile_no[beck_outliers[, "row"]],
        katilimci_cocuk = df$katilimci_cocuk[beck_outliers[, "row"]],
        role = df$role[beck_outliers[, "row"]],
        instrument = "BDI",
        item = beck_cols[beck_outliers[, "col"]],
        raw_value = beck_values[beck_outliers],
        cleaned_value = NA_real_,
        stringsAsFactors = FALSE
      )
    }
  }

  if (length(kia_cols) > 0) {
    kia_values <- as.matrix(df[kia_cols])
    kia_outliers <- which(!is.na(kia_values) &
                            (kia_values < 1 | kia_values > 5),
                          arr.ind = TRUE)
    if (nrow(kia_outliers) > 0) {
      reports[[length(reports) + 1]] <- data.frame(
        source_row_number = df$source_row_number[kia_outliers[, "row"]],
        aile_no = df$aile_no[kia_outliers[, "row"]],
        katilimci_cocuk = df$katilimci_cocuk[kia_outliers[, "row"]],
        role = df$role[kia_outliers[, "row"]],
        instrument = "SRQ",
        item = sub("^kia_", "srq_", kia_cols[kia_outliers[, "col"]]),
        raw_value = kia_values[kia_outliers],
        cleaned_value = NA_real_,
        stringsAsFactors = FALSE
      )
    }
  }

  if (length(reports) == 0) {
    return(empty_stage3_outlier_report())
  }

  do.call(rbind, reports)
}

clean_stage3_bdi_and_srq <- function(df) {
  beck_cols <- stage3_beck_columns(df)
  kia_cols <- stage3_kia_columns(df)

  for (col in beck_cols) {
    values <- suppressWarnings(as.numeric(df[[col]]))
    values[!is.na(values) & !(values %in% 0:3)] <- NA_real_
    df[[col]] <- values
  }

  if (length(kia_cols) > 0) {
    for (col in kia_cols) {
      values <- suppressWarnings(as.numeric(df[[col]]))
      values[!is.na(values) & !(values %in% 1:5)] <- NA_real_
      df[[col]] <- values
    }

    names(df)[match(kia_cols, names(df))] <- sub("^kia_", "srq_", kia_cols)
  }

  df
}

empty_dm_diagnosis_correction_report <- function() {
  data.frame(
    aile_no = numeric(),
    index_source_row_number = numeric(),
    old_dm_tani_tarihi = character(),
    new_dm_tani_tarihi = character(),
    correction_source = character(),
    applied_rule = character(),
    stringsAsFactors = FALSE
  )
}

empty_survey_date_correction_report <- function() {
  data.frame(
    aile_no = numeric(),
    old_anket_tarihi = character(),
    new_anket_tarihi = character(),
    rows_corrected = integer(),
    correction_source = character(),
    applied_rule = character(),
    stringsAsFactors = FALSE
  )
}

empty_child_birth_date_correction_report <- function() {
  data.frame(
    cocuk_no = character(),
    aile_no = numeric(),
    target_source_row_number = numeric(),
    old_katilimci_cocuk_dogum_tarihi = character(),
    new_katilimci_cocuk_dogum_tarihi = character(),
    paired_kardes_rows_corrected = integer(),
    correction_source = character(),
    applied_rule = character(),
    stringsAsFactors = FALSE
  )
}

apply_child_birth_date_corrections <- function(df, child_birth_date_corrections) {
  if (is.null(child_birth_date_corrections) ||
      nrow(child_birth_date_corrections) == 0) {
    return(list(data = df, report = empty_child_birth_date_correction_report()))
  }
  required <- c("cocuk_no", "katilimci_cocuk_dogum_tarihi")
  missing <- setdiff(required, names(child_birth_date_corrections))
  if (length(missing) > 0) {
    stop(sprintf("Missing child birth correction columns: %s",
                 paste(missing, collapse = ", ")), call. = FALSE)
  }
  if (!"correction_source" %in% names(child_birth_date_corrections)) {
    child_birth_date_corrections$correction_source <- "manual_raw_lookup"
  }

  report_rows <- vector("list", nrow(child_birth_date_corrections))

  for (i in seq_len(nrow(child_birth_date_corrections))) {
    child_id <- as.character(child_birth_date_corrections$cocuk_no[i])
    new_date <- as.character(
      child_birth_date_corrections$katilimci_cocuk_dogum_tarihi[i]
    )
    target <- df$cocuk_no == child_id

    if (sum(target, na.rm = TRUE) != 1) {
      next
    }

    family_id <- df$aile_no[target]
    old_date <- as.character(df$katilimci_cocuk_dogum_tarihi[target])
    old_date[is.na(old_date)] <- NA_character_
    df$katilimci_cocuk_dogum_tarihi[target] <- new_date

    paired <- df$aile_no == family_id & df$cocuk_no != child_id
    if ("kardes_dogum_tarihi" %in% names(df)) {
      df$kardes_dogum_tarihi[paired] <- new_date
    }

    report_rows[[i]] <- data.frame(
      cocuk_no = child_id,
      aile_no = family_id,
      target_source_row_number = if ("source_row_number" %in% names(df)) {
        df$source_row_number[target]
      } else {
        NA_integer_
      },
      old_katilimci_cocuk_dogum_tarihi = old_date,
      new_katilimci_cocuk_dogum_tarihi = new_date,
      paired_kardes_rows_corrected = as.integer(sum(paired, na.rm = TRUE)),
      correction_source = child_birth_date_corrections$correction_source[i],
      applied_rule = "participant_child_birth_date_filled_from_raw_data",
      stringsAsFactors = FALSE
    )
  }

  report_rows <- report_rows[!vapply(report_rows, is.null, logical(1))]
  report <- if (length(report_rows) == 0) {
    empty_child_birth_date_correction_report()
  } else {
    do.call(rbind, report_rows)
  }

  list(data = df, report = report)
}

harmonize_stage3_sibling_reference_fields <- function(df) {
  if (!all(c("aile_no", "katilimci_cocuk_dogum_tarihi") %in% names(df))) {
    return(df)
  }

  for (family_id in unique(df$aile_no)) {
    rows <- which(df$aile_no == family_id)
    if (length(rows) != 2) {
      next
    }

    if ("kardes_dogum_tarihi" %in% names(df)) {
      df$kardes_dogum_tarihi[rows] <- rev(df$katilimci_cocuk_dogum_tarihi[rows])
    }

    if (all(c("katilimci_cocuk_cinsiyet", "kardes_cinsiyet") %in% names(df))) {
      df$kardes_cinsiyet[rows] <- rev(df$katilimci_cocuk_cinsiyet[rows])
    }
  }

  df
}

apply_survey_date_corrections <- function(df, survey_date_corrections) {
  if (is.null(survey_date_corrections) || nrow(survey_date_corrections) == 0) {
    return(list(data = df, report = empty_survey_date_correction_report()))
  }
  required <- c("aile_no", "anket_tarihi")
  missing <- setdiff(required, names(survey_date_corrections))
  if (length(missing) > 0) {
    stop(sprintf("Missing survey correction columns: %s",
                 paste(missing, collapse = ", ")), call. = FALSE)
  }
  if (!"correction_source" %in% names(survey_date_corrections)) {
    survey_date_corrections$correction_source <- "manual_raw_lookup"
  }

  report_rows <- vector("list", nrow(survey_date_corrections))

  for (i in seq_len(nrow(survey_date_corrections))) {
    family_id <- survey_date_corrections$aile_no[i]
    new_date <- as.character(survey_date_corrections$anket_tarihi[i])
    target <- df$aile_no == family_id

    if (!any(target, na.rm = TRUE)) {
      next
    }

    old_dates <- unique(as.character(df$anket_tarihi[target]))
    old_dates[is.na(old_dates)] <- NA_character_
    df$anket_tarihi[target] <- new_date

    report_rows[[i]] <- data.frame(
      aile_no = family_id,
      old_anket_tarihi = paste(old_dates, collapse = ";"),
      new_anket_tarihi = new_date,
      rows_corrected = as.integer(sum(target, na.rm = TRUE)),
      correction_source = survey_date_corrections$correction_source[i],
      applied_rule = "family_survey_date_filled_from_raw_data",
      stringsAsFactors = FALSE
    )
  }

  report_rows <- report_rows[!vapply(report_rows, is.null, logical(1))]
  report <- if (length(report_rows) == 0) {
    empty_survey_date_correction_report()
  } else {
    do.call(rbind, report_rows)
  }

  list(data = df, report = report)
}

apply_dm_diagnosis_corrections <- function(df, dm_diagnosis_corrections) {
  if (is.null(dm_diagnosis_corrections) || nrow(dm_diagnosis_corrections) == 0) {
    return(list(data = df, report = empty_dm_diagnosis_correction_report()))
  }
  required <- c("aile_no", "dm_tani_tarihi")
  missing <- setdiff(required, names(dm_diagnosis_corrections))
  if (length(missing) > 0) {
    stop(sprintf("Missing correction columns: %s", paste(missing, collapse = ", ")),
         call. = FALSE)
  }
  if (!"correction_source" %in% names(dm_diagnosis_corrections)) {
    dm_diagnosis_corrections$correction_source <- "manual_raw_lookup"
  }

  report_rows <- vector("list", nrow(dm_diagnosis_corrections))

  for (i in seq_len(nrow(dm_diagnosis_corrections))) {
    family_id <- dm_diagnosis_corrections$aile_no[i]
    new_date <- as.character(dm_diagnosis_corrections$dm_tani_tarihi[i])
    target <- df$aile_no == family_id & df$role == "DM_Hasta_Indeks"

    if (sum(target, na.rm = TRUE) != 1) {
      next
    }

    old_date <- as.character(df$dm_tani_tarihi[target])
    old_date[is.na(old_date)] <- NA_character_
    df$dm_tani_tarihi[target] <- new_date

    report_rows[[i]] <- data.frame(
      aile_no = family_id,
      index_source_row_number = if ("source_row_number" %in% names(df)) {
        df$source_row_number[target]
      } else {
        NA_integer_
      },
      old_dm_tani_tarihi = old_date,
      new_dm_tani_tarihi = new_date,
      correction_source = dm_diagnosis_corrections$correction_source[i],
      applied_rule = "dm_index_diagnosis_date_filled_from_raw_data",
      stringsAsFactors = FALSE
    )
  }

  report_rows <- report_rows[!vapply(report_rows, is.null, logical(1))]
  report <- if (length(report_rows) == 0) {
    empty_dm_diagnosis_correction_report()
  } else {
    do.call(rbind, report_rows)
  }

  list(data = df, report = report)
}

na_parent_report_on_sibling_rows <- function(df) {
  p_cols <- stage3_embu_p_columns(df)
  beck_cols <- stage3_beck_columns(df)
  sibling_rows <- !df$is_index

  df[sibling_rows, c(p_cols, beck_cols)] <- NA
  df
}

add_beck_total <- function(df) {
  beck_cols <- stage3_beck_columns(df)
  if (length(beck_cols) == 0) {
    return(df)
  }

  beck_values <- as.data.frame(lapply(df[beck_cols], as.numeric))
  missing_any <- rowSums(is.na(beck_values)) > 0
  total <- rowSums(beck_values, na.rm = FALSE)
  total[missing_any] <- NA_real_
  df$beck_total <- total
  df
}

add_dm_missing_diagnosis_flag <- function(df) {
  family_ids <- unique(df$aile_no)
  flag <- setNames(rep(FALSE, length(family_ids)), as.character(family_ids))

  for (family_id in family_ids) {
    rows <- df[df$aile_no == family_id, , drop = FALSE]
    dm_family <- all(rows$group == "DM")
    diagnosis <- trimws(as.character(rows$dm_tani_tarihi))
    diagnosis[diagnosis == ""] <- NA_character_
    flag[as.character(family_id)] <- dm_family && all(is.na(diagnosis))
  }

  df$family_dm_inconsistent <- unname(flag[as.character(df$aile_no)])
  df
}

build_dm_missing_diagnosis_report <- function(df) {
  index_rows <- df[df$is_index & df$group == "DM" &
                     df$family_dm_inconsistent, , drop = FALSE]

  if (nrow(index_rows) == 0) {
    return(data.frame(
      aile_no = numeric(),
      index_source_row_number = numeric(),
      index_role = character(),
      hastalik_engel = character(),
      stringsAsFactors = FALSE
    ))
  }

  data.frame(
    aile_no = index_rows$aile_no,
    index_source_row_number = if ("source_row_number" %in% names(index_rows)) {
      index_rows$source_row_number
    } else {
      NA_integer_
    },
    index_role = index_rows$role,
    hastalik_engel = if ("hastalik_engel" %in% names(index_rows)) {
      index_rows$hastalik_engel
    } else {
      NA_character_
    },
    stringsAsFactors = FALSE
  )
}

build_stage3_integrity_by_role <- function(df_stage3) {
  p_cols <- stage3_embu_p_columns(df_stage3)
  c_cols <- stage3_embu_c_columns(df_stage3)
  beck_cols <- stage3_beck_columns(df_stage3)
  srq_cols <- stage3_srq_columns(df_stage3)
  roles <- c("DM_Hasta_Indeks", "DM_Hasta_Kardes",
             "Kontrol_Indeks", "Kontrol_Kardes")

  rows <- lapply(roles, function(role_name) {
    rows_for_role <- df_stage3$role == role_name
    data.frame(
      role = role_name,
      n = sum(rows_for_role),
      embu_p_dolu = sum(rowSums(!is.na(df_stage3[rows_for_role, p_cols, drop = FALSE])) > 0),
      embu_c_dolu = sum(rowSums(!is.na(df_stage3[rows_for_role, c_cols, drop = FALSE])) > 0),
      bdi_dolu = sum(rowSums(!is.na(df_stage3[rows_for_role, beck_cols, drop = FALSE])) > 0),
      srq_dolu = sum(rowSums(!is.na(df_stage3[rows_for_role, srq_cols, drop = FALSE])) > 0),
      stringsAsFactors = FALSE
    )
  })

  do.call(rbind, rows)
}

rename_prefix <- function(names_in, pattern, replacement) {
  sub(pattern, replacement, names_in)
}

rename_embu_c_role_columns <- function(names_in, role_prefix) {
  out <- names_in
  item_cols <- grepl("^embu_c_q", out)
  out[item_cols] <- sub(
    "^embu_c_q",
    paste0("embu_c_", role_prefix, "_q"),
    out[item_cols]
  )
  out[!item_cols] <- sub(
    "^embu_c_",
    paste0("embu_c_", role_prefix, "_"),
    out[!item_cols]
  )
  out
}

different_cell_count <- function(index_values, sibling_values) {
  different <- !(is.na(index_values) & is.na(sibling_values)) &
    (is.na(index_values) != is.na(sibling_values) |
       (!is.na(index_values) & !is.na(sibling_values) &
          index_values != sibling_values))
  sum(different)
}

build_index_authority_report <- function(df_stage3, index_authority_family_ids) {
  p_cols <- stage3_embu_p_columns(df_stage3)
  beck_cols <- stage3_beck_columns(df_stage3)
  parent_cols <- c(p_cols, beck_cols)

  index_rows <- df_stage3[df_stage3$is_index, , drop = FALSE]
  sibling_rows <- df_stage3[!df_stage3$is_index, , drop = FALSE]

  report_rows <- vector("list", length(index_authority_family_ids))
  for (i in seq_along(index_authority_family_ids)) {
    family_id <- index_authority_family_ids[i]
    index_row <- index_rows[index_rows$aile_no == family_id, , drop = FALSE]
    sibling_row <- sibling_rows[sibling_rows$aile_no == family_id, , drop = FALSE]

    if (nrow(index_row) != 1 || nrow(sibling_row) != 1) {
      next
    }

    report_rows[[i]] <- data.frame(
      aile_no = family_id,
      index_source_row_number = if ("source_row_number" %in% names(index_row)) {
        index_row$source_row_number
      } else {
        NA_integer_
      },
      sibling_source_row_number = if ("source_row_number" %in% names(sibling_row)) {
        sibling_row$source_row_number
      } else {
        NA_integer_
      },
      differing_parent_report_cells = different_cell_count(
        unlist(index_row[parent_cols], use.names = FALSE),
        unlist(sibling_row[parent_cols], use.names = FALSE)
      ),
      applied_rule = "index_parent_report_retained_sibling_parent_report_set_na",
      stringsAsFactors = FALSE
    )
  }

  report_rows <- report_rows[!vapply(report_rows, is.null, logical(1))]
  if (length(report_rows) == 0) {
    return(data.frame(
      aile_no = numeric(),
      index_source_row_number = numeric(),
      sibling_source_row_number = numeric(),
      differing_parent_report_cells = integer(),
      applied_rule = character(),
      stringsAsFactors = FALSE
    ))
  }

  do.call(rbind, report_rows)
}

build_stage3_family_wide <- function(df_stage3) {
  p_cols <- stage3_embu_p_columns(df_stage3)
  c_cols <- stage3_embu_c_columns(df_stage3)
  beck_cols <- stage3_beck_columns(df_stage3)
  srq_cols <- stage3_srq_columns(df_stage3)
  anne_cols <- stage3_anne_demography_columns(df_stage3)
  embu_p_meta_cols <- stage3_embu_p_meta_columns(df_stage3)
  embu_c_meta_cols <- stage3_embu_c_meta_columns(df_stage3)
  embu_common_meta_cols <- stage3_embu_common_meta_columns(df_stage3)
  index_identity_cols <- intersect(c(
    "source_row_number",
    "sira_no",
    "aile_no",
    "cocuk_no",
    "katilimci_cocuk",
    "is_index",
    "role",
    "family_role",
    "group"
  ), names(df_stage3))
  index_date_child_cols <- intersect(c(
    "anket_tarihi",
    "katilimci_cocuk_dogum_tarihi",
    "katilimci_cocuk_sirasi",
    "katilimci_cocuk_cinsiyet",
    "dm_tani_tarihi"
  ), names(df_stage3))
  index_derived_cols <- intersect(c(
    "beck_total",
    "cocuk_yas",
    "anne_yas",
    "dm_yili",
    "family_dm_inconsistent"
  ), names(df_stage3))
  base_cols <- unique(c(
    index_identity_cols,
    index_date_child_cols,
    anne_cols,
    index_derived_cols,
    p_cols,
    embu_p_meta_cols,
    beck_cols,
    "beck_total",
    embu_common_meta_cols
  ))

  index_rows <- df_stage3[df_stage3$is_index, , drop = FALSE]
  sibling_rows <- df_stage3[!df_stage3$is_index, , drop = FALSE]

  if (anyDuplicated(index_rows$aile_no)) {
    stop("Index rows must be unique per family", call. = FALSE)
  }
  if (anyDuplicated(sibling_rows$aile_no)) {
    stop("Sibling rows must be unique per family", call. = FALSE)
  }

  family <- index_rows[base_cols]

  index_c_cols <- c(c_cols, embu_c_meta_cols)
  index_c <- index_rows[c("aile_no", index_c_cols)]
  names(index_c) <- c(
    "aile_no",
    rename_embu_c_role_columns(index_c_cols, "idx")
  )

  index_srq <- index_rows[c("aile_no", srq_cols)]

  sibling_extra_cols <- intersect(c(
    "source_row_number",
    "sira_no",
    "cocuk_no",
    "katilimci_cocuk",
    "is_index",
    "family_role",
    "role",
    "anket_tarihi",
    "cocuk_yas",
    "katilimci_cocuk_dogum_tarihi",
    "katilimci_cocuk_sirasi",
    "katilimci_cocuk_cinsiyet"
  ), names(df_stage3))
  sibling_common_meta_cols <- embu_common_meta_cols
  sibling_c_cols <- c(c_cols, embu_c_meta_cols)
  sibling_cols <- c(
    "aile_no",
    sibling_c_cols,
    srq_cols,
    sibling_extra_cols,
    sibling_common_meta_cols
  )
  sibling <- sibling_rows[sibling_cols]
  sibling_extra_names <- c(
    source_row_number = "kardes_source_row_number",
    sira_no = "kardes_sira_no",
    cocuk_no = "kardes_cocuk_no",
    katilimci_cocuk = "kardes_katilimci_cocuk",
    is_index = "kardes_is_index",
    family_role = "kardes_family_role",
    role = "kardes_role",
    anket_tarihi = "kardes_anket_tarihi",
    cocuk_yas = "kardes_yas",
    katilimci_cocuk_dogum_tarihi = "kardes_dogum_tarihi",
    katilimci_cocuk_sirasi = "kardes_sirasi",
    katilimci_cocuk_cinsiyet = "kardes_cinsiyet"
  )
  sibling_common_meta_names <- c(
    embu_outlier_n = "kardes_embu_outlier_n",
    embu_likert_standardized = "kardes_embu_likert_standardized"
  )
  names(sibling) <- c(
    "aile_no",
    rename_embu_c_role_columns(sibling_c_cols, "sib"),
    rename_prefix(srq_cols, "^srq_", "srq_sib_"),
    sibling_extra_names[sibling_extra_cols],
    sibling_common_meta_names[sibling_common_meta_cols]
  )

  family <- merge(family, index_c, by = "aile_no", all.x = TRUE, sort = FALSE)
  family <- merge(family, index_srq, by = "aile_no", all.x = TRUE, sort = FALSE)
  family <- merge(family, sibling, by = "aile_no", all.x = TRUE, sort = FALSE)

  family[order(match(family$aile_no, index_rows$aile_no)), , drop = FALSE]
}

require_stage3_columns <- function(df, cols, context) {
  missing <- setdiff(cols, names(df))
  if (length(missing) > 0) {
    stop(sprintf(
      "%s missing required columns: %s",
      context,
      paste(missing, collapse = ", ")
    ), call. = FALSE)
  }
}

stage3_final_reference_excluded_columns <- function(df) {
  exact_cols <- c(
    "source_row_number",
    "sira_no",
    "kardes_source_row_number",
    "kardes_sira_no",
    "family_dm_inconsistent",
    "beck_total"
  )
  process_pattern <- paste(
    c(
      "likert",
      "conversion",
      "outlier",
      "family_mixed_likert"
    ),
    collapse = "|"
  )
  unique(c(
    intersect(exact_cols, names(df)),
    grep(process_pattern, names(df), value = TRUE)
  ))
}

drop_stage3_final_reference_excluded_columns <- function(df) {
  excluded_cols <- stage3_final_reference_excluded_columns(df)
  df[setdiff(names(df), excluded_cols)]
}

reverse_stage3_likert4 <- function(x) {
  values <- suppressWarnings(as.numeric(x))
  valid <- !is.na(values) & values %in% 1:4
  values[valid] <- 5 - values[valid]
  values
}

build_stage3_final_reference_long <- function(df_stage3) {
  require_stage3_columns(df_stage3, "embu_c_q25", "Final long reference")
  final <- drop_stage3_final_reference_excluded_columns(df_stage3)
  final$embu_c_q25 <- reverse_stage3_likert4(final$embu_c_q25)
  final
}

build_stage3_final_reference_family <- function(df_family) {
  require_stage3_columns(
    df_family,
    c("embu_c_idx_q25", "embu_c_sib_q25"),
    "Final family reference"
  )
  final <- drop_stage3_final_reference_excluded_columns(df_family)
  final$embu_c_idx_q25 <- reverse_stage3_likert4(final$embu_c_idx_q25)
  final$embu_c_sib_q25 <- reverse_stage3_likert4(final$embu_c_sib_q25)
  final
}

prepare_embu_stage3_family <- function(
  df,
  index_authority_family_ids = stage3_default_index_authority_family_ids(),
  dm_diagnosis_corrections = stage3_default_dm_diagnosis_corrections(),
  survey_date_corrections = stage3_default_survey_date_corrections(),
  child_birth_date_corrections = stage3_default_child_birth_date_corrections()
) {
  df <- as.data.frame(df, check.names = FALSE)
  df <- normalize_stage3_literal_missing_values(df)
  df <- standardize_stage3_chronic_binary_codes(df)
  stage3_validate_columns(df)

  df_stage3 <- add_stage3_roles(df)
  survey_correction_result <- apply_survey_date_corrections(
    df_stage3,
    survey_date_corrections
  )
  df_stage3 <- survey_correction_result$data
  survey_date_correction_report <- survey_correction_result$report
  child_birth_correction_result <- apply_child_birth_date_corrections(
    df_stage3,
    child_birth_date_corrections
  )
  df_stage3 <- child_birth_correction_result$data
  child_birth_date_correction_report <- child_birth_correction_result$report
  df_stage3 <- harmonize_stage3_sibling_reference_fields(df_stage3)
  index_authority_report <- build_index_authority_report(
    df_stage3,
    index_authority_family_ids
  )
  dm_correction_result <- apply_dm_diagnosis_corrections(
    df_stage3,
    dm_diagnosis_corrections
  )
  df_stage3 <- dm_correction_result$data
  dm_diagnosis_correction_report <- dm_correction_result$report
  df_stage3 <- harmonize_stage3_family_level_fields(df_stage3)
  df_stage3 <- na_parent_report_on_sibling_rows(df_stage3)
  df_stage3 <- clean_stage3_bdi_and_srq(df_stage3)
  df_stage3 <- add_beck_total(df_stage3)
  df_stage3 <- add_stage3_derived_dates(df_stage3)
  df_stage3 <- add_dm_missing_diagnosis_flag(df_stage3)
  df_family <- build_stage3_family_wide(df_stage3)
  outlier_report <- build_stage3_outlier_report(add_stage3_roles(df))
  integrity <- build_stage3_integrity_by_role(df_stage3)
  dm_missing_diagnosis <- build_dm_missing_diagnosis_report(df_stage3)

  p_cols <- stage3_embu_p_columns(df_stage3)
  beck_cols <- stage3_beck_columns(df_stage3)
  sibling_rows <- !df_stage3$is_index
  parent_cols <- c(p_cols, beck_cols)
  family_rows_per_family <- table(df_stage3$aile_no)
  srq_outlier_n <- sum(outlier_report$instrument == "SRQ")
  beck_outlier_n <- sum(outlier_report$instrument == "BDI")

  summary <- data.frame(
    metric = c(
      "long_rows",
      "family_rows",
      "families",
      "index_rows",
      "sibling_rows_parent_report_na",
      "embu_p_columns_set_na_on_siblings",
      "beck_columns_set_na_on_siblings",
      "families_with_two_rows",
      "index_authority_families",
      "index_authority_differing_parent_report_cells",
      "srq_outlier_cells_set_na",
      "beck_outlier_cells_set_na",
      "survey_date_corrected_families",
      "child_birth_date_corrected_children",
      "dm_diagnosis_corrected_families",
      "dm_missing_diagnosis_families"
    ),
    value = c(
      nrow(df_stage3),
      nrow(df_family),
      length(unique(df_stage3$aile_no)),
      sum(df_stage3$is_index),
      sum(sibling_rows),
      length(p_cols),
      length(beck_cols),
      sum(family_rows_per_family == 2),
      nrow(index_authority_report),
      sum(index_authority_report$differing_parent_report_cells),
      srq_outlier_n,
      beck_outlier_n,
      nrow(survey_date_correction_report),
      nrow(child_birth_date_correction_report),
      nrow(dm_diagnosis_correction_report),
      nrow(dm_missing_diagnosis)
    ),
    stringsAsFactors = FALSE
  )

  list(
    long = df_stage3,
    family = df_family,
    index_authority = index_authority_report,
    integrity = integrity,
    outliers = outlier_report,
    survey_date_corrections = survey_date_correction_report,
    child_birth_date_corrections = child_birth_date_correction_report,
    dm_diagnosis_corrections = dm_diagnosis_correction_report,
    dm_missing_diagnosis = dm_missing_diagnosis,
    summary = summary
  )
}

run_embu_stage3_family <- function(
  input_path = "data/processed/embu_stage2_likert4.csv",
  final_reference_long_output_path = stage3_final_reference_paths()[["long"]],
  final_reference_family_output_path = stage3_final_reference_paths()[["family"]],
  index_authority_output_path = "outputs/tables/embu_stage3_index_authority_families.csv",
  integrity_output_path = "outputs/tables/embu_stage3_integrity_by_role.csv",
  outlier_output_path = "outputs/tables/embu_stage3_outlier_cleaning_report.csv",
  survey_correction_output_path = "outputs/tables/embu_stage3_survey_date_corrections.csv",
  child_birth_correction_output_path = "outputs/tables/embu_stage3_child_birth_date_corrections.csv",
  dm_correction_output_path = "outputs/tables/embu_stage3_dm_diagnosis_corrections.csv",
  dm_missing_output_path = "outputs/tables/embu_stage3_dm_missing_diagnosis_families.csv",
  demographic_text_audit_output_path = "outputs/tables/demographic_text_standardization_audit.csv",
  summary_path = "outputs/tables/embu_stage3_family_summary.csv"
) {
  required_package("readr")

  df <- readr::read_csv(input_path, show_col_types = FALSE)
  result <- prepare_embu_stage3_family(df)
  result$final_reference_long <- build_stage3_final_reference_long(result$long)
  result$final_reference_family <- build_stage3_final_reference_family(result$family)
  if (file.exists("R/05_demographic_text_standardization.R")) {
    source("R/05_demographic_text_standardization.R")
    demographic_standardized <- standardize_demographic_final_family(
      result$final_reference_family
    )
    result$final_reference_family <- demographic_standardized$family
    result$final_reference_long <- merge_demographic_standardization_into_long(
      result$final_reference_long,
      result$final_reference_family
    )
    result$demographic_text_standardization_audit <- demographic_standardized$audit
    validate_demographic_standardized_final(
      result$final_reference_family,
      result$final_reference_long
    )
  } else {
    result$demographic_text_standardization_audit <- data.frame()
  }
  result$summary <- rbind(
    result$summary,
    data.frame(
      metric = c(
        "final_reference_long_columns",
        "final_reference_family_columns",
        "demographic_text_standardization_audit_rows"
      ),
      value = c(
        ncol(result$final_reference_long),
        ncol(result$final_reference_family),
        nrow(result$demographic_text_standardization_audit)
      ),
      stringsAsFactors = FALSE
    )
  )

  dir.create(dirname(final_reference_long_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(final_reference_family_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(index_authority_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(integrity_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(outlier_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(survey_correction_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(child_birth_correction_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(dm_correction_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(dm_missing_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(demographic_text_audit_output_path), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(summary_path), recursive = TRUE, showWarnings = FALSE)

  readr::write_csv(result$final_reference_long, final_reference_long_output_path, na = "")
  readr::write_csv(result$final_reference_family, final_reference_family_output_path, na = "")
  readr::write_csv(result$index_authority, index_authority_output_path, na = "")
  readr::write_csv(result$integrity, integrity_output_path, na = "")
  readr::write_csv(result$outliers, outlier_output_path, na = "")
  readr::write_csv(result$survey_date_corrections,
                   survey_correction_output_path, na = "")
  readr::write_csv(result$child_birth_date_corrections,
                   child_birth_correction_output_path, na = "")
  readr::write_csv(result$dm_diagnosis_corrections,
                   dm_correction_output_path, na = "")
  readr::write_csv(result$dm_missing_diagnosis, dm_missing_output_path, na = "")
  readr::write_csv(result$demographic_text_standardization_audit,
                   demographic_text_audit_output_path, na = "")
  readr::write_csv(result$summary, summary_path, na = "")

  invisible(result)
}
