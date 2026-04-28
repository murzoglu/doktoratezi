source("R/07_reproducibility.R")

required_package <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    stop(sprintf("Required package is not installed: %s", package), call. = FALSE)
  }
}

read_csv_facts <- function(path) {
  df <- utils::read.csv(
    path,
    check.names = FALSE,
    stringsAsFactors = FALSE,
    nrows = -1
  )

  data.frame(
    path = path,
    rows = nrow(df),
    columns = ncol(df),
    sha256 = digest::digest(path, file = TRUE, algo = "sha256"),
    stringsAsFactors = FALSE
  )
}

required_package("digest")

lock_path <- "data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock"
if (!file.exists(lock_path)) {
  stop(sprintf("Canonical lock file is missing: %s", lock_path), call. = FALSE)
}

lock <- parse_final_reference_lock(readLines(lock_path, warn = FALSE))
if (!identical(lock$status, "LOCKED_CANONICAL_ANALYSIS_BASE")) {
  stop(sprintf("Unexpected lock status: %s", lock$status), call. = FALSE)
}

actual <- do.call(
  rbind,
  lapply(lock$files$path, function(path) {
    if (!file.exists(path)) {
      return(data.frame(
        path = path,
        rows = NA_integer_,
        columns = NA_integer_,
        sha256 = NA_character_,
        stringsAsFactors = FALSE
      ))
    }
    read_csv_facts(path)
  })
)

results <- compare_final_reference_facts(lock$files, actual)
stop_if_final_reference_invalid(results)

cat(sprintf(
  "Final reference lock verified: %s (%s); %d files OK\n",
  lock$lock_date,
  lock$project,
  nrow(results)
))
