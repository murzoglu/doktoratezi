demographic_free_text_columns <- function() {
  c("calistigi_is", "es_calistigi_is", "hastalik_engel", "es_hastalik_engel")
}

disease_category_basenames <- function() {
  c(
    "endokrin",
    "kardiyovaskuler",
    "solunum",
    "gastrointestinal",
    "renal",
    "kas_iskelet",
    "mental",
    "sinir",
    "otoimmun",
    "duyu",
    "hematolojik",
    "dermatolojik",
    "neoplazm",
    "diger"
  )
}

occupation_standard_columns <- function() {
  c(
    "es_emekli",
    "es_isco08_4digit",
    "es_isco08_major",
    "es_isei08",
    "es_siops08",
    "es_egp7",
    "es_meslek_kodlama_durumu",
    "es_meslek_kodlama_kaynagi",
    "aile_isei08",
    "aile_siops08",
    "aile_egp7"
  )
}

disease_category_names <- function(prefix) {
  paste0(
    prefix,
    c(paste0("_hastalik_", disease_category_basenames()),
      "_hastalik_kategori_sayisi",
      "_hastalik_kodlama_durumu")
  )
}

demographic_standard_columns <- function() {
  c(
    occupation_standard_columns(),
    disease_category_names("anne"),
    disease_category_names("es")
  )
}

normalize_demographic_text <- function(x) {
  x <- as.character(x)
  x[is.na(x)] <- NA_character_
  x <- trimws(x)
  x[x == ""] <- NA_character_

  replacements <- c(
    "\u00e7" = "c", "\u00c7" = "c",
    "\u011f" = "g", "\u011e" = "g",
    "\u0131" = "i", "\u0130" = "i",
    "\u00f6" = "o", "\u00d6" = "o",
    "\u015f" = "s", "\u015e" = "s",
    "\u00fc" = "u", "\u00dc" = "u"
  )
  for (pattern in names(replacements)) {
    x <- gsub(pattern, replacements[[pattern]], x, fixed = TRUE)
  }

  x <- tolower(x)
  x <- gsub("[^a-z0-9]+", " ", x)
  x <- gsub("\\s+", " ", x)
  trimws(x)
}

has_pattern <- function(text, pattern) {
  !is.na(text) && grepl(pattern, text, perl = TRUE)
}

occupation_result <- function(
  isco08_4digit = NA_character_,
  isco08_major = NA_integer_,
  isei08 = NA_real_,
  siops08 = NA_real_,
  egp7 = NA_integer_,
  status = "needs_manual_review",
  source = "investigator_final_2026_04_26",
  es_emekli = 0L
) {
  data.frame(
    es_emekli = as.integer(es_emekli),
    es_isco08_4digit = isco08_4digit,
    es_isco08_major = as.integer(isco08_major),
    es_isei08 = as.numeric(isei08),
    es_siops08 = as.numeric(siops08),
    es_egp7 = as.integer(egp7),
    es_meslek_kodlama_durumu = status,
    es_meslek_kodlama_kaynagi = source,
    stringsAsFactors = FALSE
  )
}

retired_occupation_result <- function() {
  occupation_result(
    isco08_4digit = NA_character_,
    isco08_major = NA_integer_,
    isei08 = NA_real_,
    siops08 = NA_real_,
    egp7 = NA_integer_,
    es_emekli = 1L,
    status = "retired_not_working",
    source = "investigator_decision_2026_04_26"
  )
}

draft_code_spouse_occupation <- function(raw_text, work_flag) {
  text <- normalize_demographic_text(raw_text)
  flag <- suppressWarnings(as.integer(work_flag))

  if (is.na(text) || text == "") {
    if (!is.na(flag) && flag == 1L) {
      return(occupation_result(status = "missing_text"))
    }
    return(occupation_result(es_emekli = NA_integer_, status = "not_working_no_text"))
  }

  retired <- has_pattern(text, "\\bemekli\\b")
  if (retired) {
    return(retired_occupation_result())
  }

  if (has_pattern(text, "avukat")) {
    return(occupation_result("2611", 2L, 85, 73, 1L, "final_rule"))
  }
  if (has_pattern(text, "ogretmen")) {
    return(occupation_result("2341", 2L, 66, 64, 2L, "final_rule"))
  }
  if (has_pattern(text, "muhendis|mimar")) {
    return(occupation_result("2142", 2L, 70, 67, 1L, "final_rule"))
  }
  if (has_pattern(text, "mali musavir|muhasebeci")) {
    return(occupation_result("2411", 2L, 65, 60, 2L, "final_rule"))
  }
  if (has_pattern(text, "yeminli tercuman")) {
    return(occupation_result("2643", 2L, 60, 58, 2L, "final_rule"))
  }
  if (has_pattern(text, "din gorevlisi|imam")) {
    return(occupation_result("2636", 2L, 55, 55, 2L, "final_rule"))
  }
  if (has_pattern(text, "antrenor")) {
    return(occupation_result("3422", 3L, 49, 47, 2L, "final_rule"))
  }
  if (has_pattern(text, "eczane")) {
    return(occupation_result("3213", 3L, 43, 44, 3L, "final_rule"))
  }
  if (has_pattern(text, "teknisyen|teknik servis|teknikeri")) {
    return(occupation_result("3113", 3L, 45, 44, 3L, "final_rule"))
  }
  if (has_pattern(text, "plasiyer|satin alma|proje sorumlusu")) {
    return(occupation_result("3322", 3L, 45, 44, 3L, "final_rule"))
  }
  if (has_pattern(text, "banka")) {
    return(occupation_result("4211", 4L, 45, 45, 3L, "final_rule"))
  }
  if (has_pattern(text, "memur|belediye|ptt|ibb|idari|buro|bakirkoy elektrik|kav")) {
    return(occupation_result("4110", 4L, 45, 45, 3L, "final_rule"))
  }
  if (has_pattern(text, "depo muduru")) {
    return(occupation_result("1324", 1L, 60, 55, 1L, "final_rule"))
  }
  if (has_pattern(text, "depo")) {
    return(occupation_result("4321", 4L, 36, 36, 3L, "final_rule"))
  }
  if (has_pattern(text, "asker")) {
    return(occupation_result("0310", 0L, 50, 50, 2L, "final_rule"))
  }
  if (has_pattern(text, "guvenlik")) {
    return(occupation_result("5414", 5L, 32, 35, 5L, "final_rule"))
  }
  if (has_pattern(text, "garson|cafe|bufe")) {
    return(occupation_result("5131", 5L, 28, 30, 5L, "final_rule"))
  }
  if (has_pattern(text, "asci|doner|firinci|kasap")) {
    return(occupation_result("5120", 5L, 30, 34, 5L, "final_rule"))
  }
  if (has_pattern(text, "market|manav|pazar|ticaret|esnaf|serbest|kendi isi")) {
    return(occupation_result("5221", 5L, 35, 37, 4L, "final_broad_category"))
  }
  if (has_pattern(text, "kapici|apartman gorevli|gorevli apartman")) {
    return(occupation_result("5153", 5L, 25, 28, 5L, "final_rule"))
  }
  if (has_pattern(text, "sofor|soforluk|servis|taksi|nakliye")) {
    status <- if (retired) "retired_not_working" else "final_rule"
    return(occupation_result("8332", 8L, 32, 35, 5L, status))
  }
  if (has_pattern(text, "forklift|kepce|vinc|operator|operat|makine opr")) {
    status <- if (retired) "retired_not_working" else "final_rule"
    return(occupation_result("8344", 8L, 34, 35, 5L, status))
  }
  if (has_pattern(text, "dokum|fabrika|imalat|tekstil|hazir giyim|makinaci")) {
    return(occupation_result("8189", 8L, 32, 34, 6L, "final_rule"))
  }
  if (has_pattern(text, "insaat isci|insaatci|insaat|halde isci")) {
    return(occupation_result("9313", 9L, 16, 20, 7L, "final_rule"))
  }
  if (has_pattern(text, "temizlik|oto yikama")) {
    return(occupation_result("9112", 9L, 16, 20, 7L, "final_rule"))
  }
  if (has_pattern(text, "isci|eleman|ozel sektor|ozelde isci|celik iscisi")) {
    return(occupation_result("9329", 9L, 20, 25, 7L, "final_broad_category"))
  }
  if (has_pattern(text, "tesisat|elektrik|kaynak|kaporta|tamir|tornaci|boyaci|badana|mobilya|mermer|terzi|ayakkabici|tabelaci|dekorasyon|oto cam|oto kaporta|\\boto\\b|gemi yat|celik dolap|usta|berber|dalgic|matbaa")) {
    return(occupation_result("7126", 7L, 31, 35, 6L, "final_broad_category"))
  }

  occupation_result(status = "needs_manual_review")
}

disease_result <- function(values, count, status) {
  data.frame(
    hastalik_endokrin = values[["endokrin"]],
    hastalik_kardiyovaskuler = values[["kardiyovaskuler"]],
    hastalik_solunum = values[["solunum"]],
    hastalik_gastrointestinal = values[["gastrointestinal"]],
    hastalik_renal = values[["renal"]],
    hastalik_kas_iskelet = values[["kas_iskelet"]],
    hastalik_mental = values[["mental"]],
    hastalik_sinir = values[["sinir"]],
    hastalik_otoimmun = values[["otoimmun"]],
    hastalik_duyu = values[["duyu"]],
    hastalik_hematolojik = values[["hematolojik"]],
    hastalik_dermatolojik = values[["dermatolojik"]],
    hastalik_neoplazm = values[["neoplazm"]],
    hastalik_diger = values[["diger"]],
    hastalik_kategori_sayisi = count,
    hastalik_kodlama_durumu = status,
    stringsAsFactors = FALSE
  )
}

empty_disease_values <- function(value) {
  stats::setNames(
    rep(value, length(disease_category_basenames())),
    disease_category_basenames()
  )
}

draft_code_chronic_condition <- function(raw_text, condition_flag) {
  text <- normalize_demographic_text(raw_text)
  flag <- suppressWarnings(as.integer(condition_flag))

  if (is.na(text) || text == "") {
    if (!is.na(flag) && flag == 1L) {
      return(disease_result(empty_disease_values(NA_integer_), NA_integer_, "missing_text"))
    }
    return(disease_result(empty_disease_values(0L), 0L, "no_condition"))
  }

  values <- empty_disease_values(0L)
  values[["endokrin"]] <- as.integer(has_pattern(text, "dm|diyabet|seker|tip ?1|tip ?2|tiroid|tiroit|guatr|hashi|kolesterol|biotinidaz"))
  values[["kardiyovaskuler"]] <- as.integer(has_pattern(text, "hipertansiyon|tansiyon|\\bht\\b|kalp|aort|koroner"))
  values[["solunum"]] <- as.integer(has_pattern(text, "astim|koah|alerji|uyku apnesi"))
  values[["gastrointestinal"]] <- as.integer(
    has_pattern(text, "colyak|crohn|chron|gastrit|ulser|bagirsak|barsak") ||
      (has_pattern(text, "mide") && !has_pattern(text, "mide ca|mide kanser"))
  )
  values[["renal"]] <- as.integer(has_pattern(text, "bobrek|diyaliz|renal|nefro"))
  values[["kas_iskelet"]] <- as.integer(has_pattern(text, "bel fit|romatizma|romatoid|ankiloz|spondilit|fibromiyalji|eklem|behcet|aksama"))
  values[["mental"]] <- as.integer(has_pattern(text, "depresyon|anksiyete|panik|bipolar"))
  values[["sinir"]] <- as.integer(has_pattern(text, "epilepsi|migren|vertigo|myasthenia|myastenia|mystania|romberg|parkinson|\\bms\\b"))
  values[["otoimmun"]] <- as.integer(has_pattern(text, "fmf|ailevi akdeniz"))
  values[["duyu"]] <- as.integer(has_pattern(text, "isitme|goz"))
  values[["hematolojik"]] <- as.integer(has_pattern(text, "kanama"))
  values[["dermatolojik"]] <- as.integer(has_pattern(text, "vitiligo"))
  values[["neoplazm"]] <- as.integer(has_pattern(text, "kanser|\\bca\\b|tumor|meme|rahim|prostat"))

  known_count <- sum(unlist(values[names(values) != "diger"]), na.rm = TRUE)
  values[["diger"]] <- as.integer(
    known_count == 0L ||
      has_pattern(text, "mide ca")
  )
  count <- sum(unlist(values), na.rm = TRUE)
  status <- if (!is.na(flag) && flag == 0L && count > 0L) {
    "final_flag_corrected"
  } else if (count == 0L) {
    "final_other"
  } else {
    "final_rule"
  }

  disease_result(values, count, status)
}

prefix_disease_columns <- function(df, prefix) {
  names(df) <- paste0(prefix, "_", names(df))
  df
}

standardize_demographic_final_family <- function(df) {
  required <- c(
    "aile_no",
    "es_calisma_durumu",
    "es_calistigi_is",
    "kronik_hastalik_durumu",
    "hastalik_engel",
    "esiniz_kronik_hastalik_durumu",
    "es_hastalik_engel"
  )
  missing <- setdiff(required, names(df))
  if (length(missing) > 0) {
    stop(sprintf("Missing demographic columns: %s", paste(missing, collapse = ", ")),
         call. = FALSE)
  }

  out <- as.data.frame(df, check.names = FALSE)
  original <- out

  occupation <- do.call(rbind, Map(
    draft_code_spouse_occupation,
    out$es_calistigi_is,
    out$es_calisma_durumu
  ))

  occupation_text <- normalize_demographic_text(out$es_calistigi_is)
  spouse_has_job_text <- !is.na(occupation_text) & occupation_text != ""
  out$es_calisma_durumu[out$aile_no == 42 & spouse_has_job_text] <- 1L
  out$es_calisma_durumu[occupation$es_emekli == 1L] <- 0L

  occupation$aile_isei08 <- occupation$es_isei08
  occupation$aile_siops08 <- occupation$es_siops08
  occupation$aile_egp7 <- occupation$es_egp7

  mother_disease <- do.call(rbind, Map(
    draft_code_chronic_condition,
    out$hastalik_engel,
    out$kronik_hastalik_durumu
  ))
  spouse_disease <- do.call(rbind, Map(
    draft_code_chronic_condition,
    out$es_hastalik_engel,
    out$esiniz_kronik_hastalik_durumu
  ))

  out$kronik_hastalik_durumu[
    mother_disease$hastalik_kodlama_durumu == "final_flag_corrected"
  ] <- 1L
  out$esiniz_kronik_hastalik_durumu[
    spouse_disease$hastalik_kodlama_durumu == "final_flag_corrected"
  ] <- 1L

  mother_disease <- prefix_disease_columns(mother_disease, "anne")
  spouse_disease <- prefix_disease_columns(spouse_disease, "es")

  out <- out[setdiff(names(out), demographic_free_text_columns())]
  out <- cbind(out, occupation, mother_disease, spouse_disease)

  audit <- build_demographic_text_standardization_audit(
    original,
    out,
    occupation,
    mother_disease,
    spouse_disease
  )

  list(family = out, audit = audit)
}

build_demographic_text_standardization_audit <- function(
  original,
  standardized,
  occupation,
  mother_disease,
  spouse_disease
) {
  occupation_audit <- data.frame(
    aile_no = original$aile_no,
    field = "es_calistigi_is",
    raw_text = original$es_calistigi_is,
    original_flag = original$es_calisma_durumu,
    final_flag = standardized$es_calisma_durumu,
    coding_source = occupation$es_meslek_kodlama_kaynagi,
    coding_status = occupation$es_meslek_kodlama_durumu,
    standardized_code = occupation$es_isco08_4digit,
    standardized_label = ifelse(
      occupation$es_emekli == 1L,
      "retired_not_active_occupation",
      paste0("ISCO-08 major ", occupation$es_isco08_major)
    ),
    decision_note = "spouse occupation coded by final investigator rule; original free text removed from final CSV",
    stringsAsFactors = FALSE
  )

  mother_audit <- data.frame(
    aile_no = original$aile_no,
    field = "hastalik_engel",
    raw_text = original$hastalik_engel,
    original_flag = original$kronik_hastalik_durumu,
    final_flag = standardized$kronik_hastalik_durumu,
    coding_source = "investigator_final_2026_04_26",
    coding_status = mother_disease$anne_hastalik_kodlama_durumu,
    standardized_code = disease_code_summary(mother_disease, "anne"),
    standardized_label = "ICD-10 major-category dummy set",
    decision_note = "mother chronic condition coded by final investigator rule; original free text removed from final CSV",
    stringsAsFactors = FALSE
  )

  spouse_audit <- data.frame(
    aile_no = original$aile_no,
    field = "es_hastalik_engel",
    raw_text = original$es_hastalik_engel,
    original_flag = original$esiniz_kronik_hastalik_durumu,
    final_flag = standardized$esiniz_kronik_hastalik_durumu,
    coding_source = "investigator_final_2026_04_26",
    coding_status = spouse_disease$es_hastalik_kodlama_durumu,
    standardized_code = disease_code_summary(spouse_disease, "es"),
    standardized_label = "ICD-10 major-category dummy set",
    decision_note = "spouse chronic condition coded by final investigator rule; original free text removed from final CSV",
    stringsAsFactors = FALSE
  )

  rbind(occupation_audit, mother_audit, spouse_audit)
}

disease_code_summary <- function(df, prefix) {
  categories <- disease_category_basenames()
  cols <- paste0(prefix, "_hastalik_", categories)
  apply(df[cols], 1, function(row) {
    if (all(is.na(row))) {
      return(NA_character_)
    }
    selected <- categories[which(row == 1L)]
    if (length(selected) == 0) {
      return("none")
    }
    paste(selected, collapse = ";")
  })
}

merge_demographic_standardization_into_long <- function(long_df, standardized_family) {
  out <- as.data.frame(long_df, check.names = FALSE)
  out <- out[setdiff(names(out), c(demographic_free_text_columns(), demographic_standard_columns()))]

  lookup_cols <- c(
    "aile_no",
    "es_calisma_durumu",
    "kronik_hastalik_durumu",
    "esiniz_kronik_hastalik_durumu",
    demographic_standard_columns()
  )
  lookup_cols <- intersect(lookup_cols, names(standardized_family))
  lookup <- standardized_family[lookup_cols]
  idx <- match(out$aile_no, lookup$aile_no)

  for (col in setdiff(lookup_cols, "aile_no")) {
    out[[col]] <- lookup[[col]][idx]
  }

  out
}

validate_demographic_standardized_final <- function(family_df, long_df) {
  free_text <- demographic_free_text_columns()
  if (any(free_text %in% names(family_df)) || any(free_text %in% names(long_df))) {
    stop("Free-text demographic columns remain in final CSV schema", call. = FALSE)
  }

  required <- demographic_standard_columns()
  missing_family <- setdiff(required, names(family_df))
  missing_long <- setdiff(required, names(long_df))
  if (length(missing_family) > 0 || length(missing_long) > 0) {
    stop("Standardized demographic columns are missing", call. = FALSE)
  }

  allowed_occupation_status <- c(
    "final_rule",
    "final_broad_category",
    "missing_text",
    "not_working_no_text",
    "retired_not_working"
  )
  invalid_occupation_status <- setdiff(
    na.omit(unique(family_df$es_meslek_kodlama_durumu)),
    allowed_occupation_status
  )
  if (length(invalid_occupation_status) > 0) {
    stop("Occupation status has invalid values", call. = FALSE)
  }

  for (prefix in c("anne", "es")) {
    category_cols <- paste0(
      prefix,
      "_hastalik_",
      disease_category_basenames()
    )
    count_col <- paste0(prefix, "_hastalik_kategori_sayisi")
    status_col <- paste0(prefix, "_hastalik_kodlama_durumu")
    complete_rows <- !is.na(family_df[[count_col]])
    expected <- rowSums(family_df[complete_rows, category_cols, drop = FALSE], na.rm = TRUE)
    if (!identical(as.integer(expected), as.integer(family_df[[count_col]][complete_rows]))) {
      stop(sprintf("%s disease category count mismatch", prefix), call. = FALSE)
    }
    allowed_status <- c("no_condition", "missing_text", "final_rule", "final_flag_corrected", "final_other")
    invalid_status <- setdiff(na.omit(unique(family_df[[status_col]])), allowed_status)
    if (length(invalid_status) > 0) {
      stop(sprintf("%s disease status has invalid values", prefix), call. = FALSE)
    }
  }

  family_level_cols <- c(
    "es_calisma_durumu",
    "kronik_hastalik_durumu",
    "esiniz_kronik_hastalik_durumu",
    demographic_standard_columns()
  )
  family_level_cols <- intersect(family_level_cols, names(long_df))
  inconsistent <- stats::aggregate(
    long_df[family_level_cols],
    by = list(aile_no = long_df$aile_no),
    FUN = function(x) length(unique(x[!is.na(x)]))
  )
  if (any(inconsistent[setdiff(names(inconsistent), "aile_no")] > 1, na.rm = TRUE)) {
    stop("Long final file has family-level demographic inconsistencies", call. = FALSE)
  }

  invisible(TRUE)
}
