ethics_column_patterns <- function() {
  data.frame(
    category = c(
      "direct_name",
      "direct_contact",
      "direct_identity",
      "direct_address",
      "indirect_date",
      "indirect_geo"
    ),
    severity = c("critical", "critical", "critical", "critical", "review", "review"),
    pattern = c(
      "(^|_)(ad|adi|isim|soyad)($|_)|ad.*soyad|soyad.*ad",
      "telefon|tel_no|gsm|e[-_]?mail|eposta|mail",
      "tc(_)?(no|kimlik)|kimlik|hasta(_)?no|protokol|dosya(_)?no|mrn",
      "adres|mahalle|sokak|cadde|apartman|posta(_)?kodu",
      "dogum_tarihi|tani_tarihi|anket_tarihi|(^|_)tarih($|_)",
      "(^|_)(il|ilce|sehir|semt)($|_)"
    ),
    stringsAsFactors = FALSE
  )
}

flag_sensitive_column_names <- function(column_names, patterns = ethics_column_patterns()) {
  if (length(column_names) == 0L) {
    return(empty_column_audit())
  }

  hits <- lapply(seq_along(column_names), function(index) {
    column <- column_names[[index]]
    is_match <- vapply(
      patterns$pattern,
      function(pattern) grepl(pattern, column, ignore.case = TRUE, perl = TRUE),
      logical(1)
    )
    matched <- patterns[is_match, , drop = FALSE]
    if (nrow(matched) == 0L) {
      return(NULL)
    }

    data.frame(
      column = column,
      category = matched$category,
      severity = matched$severity,
      pattern = matched$pattern,
      stringsAsFactors = FALSE
    )
  })

  hits <- Filter(Negate(is.null), hits)
  if (length(hits) == 0L) {
    empty_column_audit()
  } else {
    do.call(rbind, hits)
  }
}

empty_column_audit <- function() {
  data.frame(
    column = character(),
    category = character(),
    severity = character(),
    pattern = character(),
    stringsAsFactors = FALSE
  )
}

ethics_path_patterns <- function() {
  data.frame(
    category = c(
      "raw_or_identified_data",
      "processed_row_level_data",
      "environment_secret",
      "credential_file",
      "targets_cache",
      "analysis_output"
    ),
    severity = c("critical", "critical", "critical", "critical", "review", "review"),
    pattern = c(
      "^data/(raw|cleaned|identified|backup)(/|$)",
      "^data/processed/.*\\.(csv|tsv|xlsx|xls|rds|RDS|qs|qs2)$",
      "(^|/)\\.env($|\\.)",
      "(^|/)credentials/|^[^/]+\\.json$|client_secret|service[-_]?account|credential|secret|firebase|vertexAI|dr-murzoglu",
      "^_targets(/|$)|^_targets\\.RDS$",
      "^outputs(/|$)"
    ),
    stringsAsFactors = FALSE
  )
}

flag_sensitive_paths <- function(paths, patterns = ethics_path_patterns()) {
  if (length(paths) == 0L) {
    return(empty_path_audit())
  }

  normalized <- normalize_audit_paths(paths)
  hits <- lapply(seq_along(normalized), function(index) {
    path <- normalized[[index]]
    is_match <- vapply(
      patterns$pattern,
      function(pattern) grepl(pattern, path, ignore.case = TRUE, perl = TRUE),
      logical(1)
    )
    matched <- patterns[is_match, , drop = FALSE]
    if (nrow(matched) == 0L) {
      return(NULL)
    }

    data.frame(
      path = path,
      category = matched$category,
      severity = matched$severity,
      pattern = matched$pattern,
      stringsAsFactors = FALSE
    )
  })

  hits <- Filter(Negate(is.null), hits)
  if (length(hits) == 0L) {
    empty_path_audit()
  } else {
    do.call(rbind, hits)
  }
}

empty_path_audit <- function() {
  data.frame(
    path = character(),
    category = character(),
    severity = character(),
    pattern = character(),
    stringsAsFactors = FALSE
  )
}

normalize_audit_paths <- function(paths) {
  paths <- gsub("\\\\", "/", paths)
  sub("^\\./", "", paths)
}

assert_no_critical_ethics_findings <- function(column_findings, path_findings) {
  critical_columns <- column_findings[column_findings$severity == "critical", , drop = FALSE]
  critical_paths <- path_findings[path_findings$severity == "critical", , drop = FALSE]

  if (nrow(critical_columns) == 0L && nrow(critical_paths) == 0L) {
    return(invisible(TRUE))
  }

  column_text <- if (nrow(critical_columns) == 0L) {
    "none"
  } else {
    paste(sprintf("%s [%s]", critical_columns$column, critical_columns$category), collapse = "; ")
  }

  path_text <- if (nrow(critical_paths) == 0L) {
    "none"
  } else {
    paste(sprintf("%s [%s]", critical_paths$path, critical_paths$category), collapse = "; ")
  }

  stop(
    sprintf(
      "Critical ethics/data-governance finding(s): columns=%s; paths=%s",
      column_text,
      path_text
    ),
    call. = FALSE
  )
}
