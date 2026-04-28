source("R/05_demographic_text_standardization.R")

required_package <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    stop(sprintf("Required package is not installed: %s", package), call. = FALSE)
  }
}

required_package("readr")

family_path <- "data/processed/FINAL_REFERENCE__analysis_base_family.csv"
long_path <- "data/processed/FINAL_REFERENCE__analysis_base_long.csv"
archive_dir <- "archive/final_reference_pre_demographic_text_standardization_2026-04-26"
audit_path <- "outputs/tables/demographic_text_standardization_audit.csv"
archive_family_path <- file.path(archive_dir, basename(family_path))
archive_long_path <- file.path(archive_dir, basename(long_path))

if (!file.exists(family_path)) {
  stop(sprintf("Missing family final reference: %s", family_path), call. = FALSE)
}
if (!file.exists(long_path)) {
  stop(sprintf("Missing long final reference: %s", long_path), call. = FALSE)
}

dir.create(archive_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(audit_path), recursive = TRUE, showWarnings = FALSE)

family <- readr::read_csv(family_path, show_col_types = FALSE, progress = FALSE)
long <- readr::read_csv(long_path, show_col_types = FALSE, progress = FALSE)

if (!all(demographic_free_text_columns() %in% names(family))) {
  validation_error <- tryCatch({
    validate_demographic_standardized_final(family, long)
    NULL
  }, error = function(e) e)

  if (is.null(validation_error)) {
    cat("Demographic text standardization already applied\n")
    cat(sprintf("family_rows=%d family_cols=%d\n", nrow(family), ncol(family)))
    cat(sprintf("long_rows=%d long_cols=%d\n", nrow(long), ncol(long)))
    quit(save = "no", status = 0)
  }

  if (!file.exists(archive_family_path) || !file.exists(archive_long_path)) {
    stop(conditionMessage(validation_error), call. = FALSE)
  }

  family <- readr::read_csv(archive_family_path, show_col_types = FALSE, progress = FALSE)
  long <- readr::read_csv(archive_long_path, show_col_types = FALSE, progress = FALSE)
  if (!all(demographic_free_text_columns() %in% names(family))) {
    stop(conditionMessage(validation_error), call. = FALSE)
  }
  cat("Reapplying demographic text standardization from archived raw-text final reference\n")
}

invisible(file.copy(
  family_path,
  file.path(archive_dir, basename(family_path)),
  overwrite = FALSE
))
invisible(file.copy(
  long_path,
  file.path(archive_dir, basename(long_path)),
  overwrite = FALSE
))

standardized <- standardize_demographic_final_family(family)
standardized_family <- standardized$family
audit <- standardized$audit
standardized_long <- merge_demographic_standardization_into_long(
  long,
  standardized_family
)

validate_demographic_standardized_final(standardized_family, standardized_long)

readr::write_csv(standardized_family, family_path, na = "")
readr::write_csv(standardized_long, long_path, na = "")
readr::write_csv(audit, audit_path, na = "")

cat("Demographic text standardization completed\n")
cat(sprintf("family_rows=%d family_cols=%d\n", nrow(standardized_family), ncol(standardized_family)))
cat(sprintf("long_rows=%d long_cols=%d\n", nrow(standardized_long), ncol(standardized_long)))
cat(sprintf("audit_rows=%d audit_path=%s\n", nrow(audit), audit_path))
