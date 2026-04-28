parse_final_reference_lock <- function(lock_text) {
  lines <- if (length(lock_text) == 1L) {
    unlist(strsplit(lock_text, "\n", fixed = TRUE), use.names = FALSE)
  } else {
    as.character(lock_text)
  }

  status <- parse_lock_scalar(lines, "status")
  lock_date <- parse_lock_scalar(lines, "lock_date")
  project <- parse_lock_scalar(lines, "project")

  pattern <- "^- `([^`]+)`: rows=([0-9]+); columns=([0-9]+); sha256=([a-f0-9]{64})$"
  matches <- regexec(pattern, lines)
  parsed <- regmatches(lines, matches)
  parsed <- parsed[lengths(parsed) == 5L]

  files <- data.frame(
    path = vapply(parsed, `[[`, character(1), 2),
    rows = as.integer(vapply(parsed, `[[`, character(1), 3)),
    columns = as.integer(vapply(parsed, `[[`, character(1), 4)),
    sha256 = vapply(parsed, `[[`, character(1), 5),
    stringsAsFactors = FALSE
  )

  list(
    status = status,
    lock_date = lock_date,
    project = project,
    files = files
  )
}

parse_lock_scalar <- function(lines, key) {
  prefix <- paste0(key, "=")
  value <- lines[startsWith(lines, prefix)]
  if (length(value) == 0L) {
    return(NA_character_)
  }
  sub(prefix, "", value[[1]], fixed = TRUE)
}

compare_final_reference_facts <- function(expected, actual) {
  required <- c("path", "rows", "columns", "sha256")
  if (!all(required %in% names(expected))) {
    stop("expected must include path, rows, columns, sha256")
  }
  if (!all(required %in% names(actual))) {
    stop("actual must include path, rows, columns, sha256")
  }

  merged <- merge(
    expected[required],
    actual[required],
    by = "path",
    all.x = TRUE,
    suffixes = c("_expected", "_actual")
  )

  merged$exists <- !is.na(merged$sha256_actual)
  merged$rows_ok <- merged$exists & merged$rows_expected == merged$rows_actual
  merged$columns_ok <- merged$exists & merged$columns_expected == merged$columns_actual
  merged$sha256_ok <- merged$exists & merged$sha256_expected == merged$sha256_actual
  merged$ok <- merged$exists & merged$rows_ok & merged$columns_ok & merged$sha256_ok
  merged
}

stop_if_final_reference_invalid <- function(results) {
  if (all(results$ok)) {
    return(invisible(TRUE))
  }

  failed <- results[!results$ok, , drop = FALSE]
  details <- paste(
    sprintf(
      "%s: exists=%s rows_ok=%s columns_ok=%s sha256_ok=%s",
      failed$path,
      failed$exists,
      failed$rows_ok,
      failed$columns_ok,
      failed$sha256_ok
    ),
    collapse = "\n"
  )
  stop(sprintf("Final reference verification failed:\n%s", details), call. = FALSE)
}
