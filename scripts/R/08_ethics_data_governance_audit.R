source("R/08_data_governance.R")

required_file <- function(path) {
  if (!file.exists(path)) {
    stop(sprintf("Required file is missing: %s", path), call. = FALSE)
  }
}

read_csv_header <- function(path) {
  names(utils::read.csv(path, nrows = 0, check.names = FALSE))
}

git_visible_existing_paths <- function() {
  result <- tryCatch(
    system2(
      "git",
      c("ls-files", "--cached", "--others", "--exclude-standard"),
      stdout = TRUE,
      stderr = FALSE
    ),
    warning = function(condition) character(),
    error = function(condition) character()
  )
  result <- normalize_audit_paths(result)
  result[file.exists(result)]
}

as_audit_rows <- function(findings, scope, source) {
  if (nrow(findings) == 0L) {
    return(data.frame(
      scope = character(),
      source = character(),
      item = character(),
      category = character(),
      severity = character(),
      stringsAsFactors = FALSE
    ))
  }

  item <- if ("column" %in% names(findings)) findings$column else findings$path
  data.frame(
    scope = scope,
    source = source,
    item = item,
    category = findings$category,
    severity = findings$severity,
    stringsAsFactors = FALSE
  )
}

canonical_paths <- c(
  family = "data/processed/FINAL_REFERENCE__analysis_base_family.csv",
  long = "data/processed/FINAL_REFERENCE__analysis_base_long.csv"
)

invisible(lapply(canonical_paths, required_file))

column_audits <- lapply(names(canonical_paths), function(name) {
  findings <- flag_sensitive_column_names(read_csv_header(canonical_paths[[name]]))
  as_audit_rows(findings, "canonical_columns", canonical_paths[[name]])
})

visible_path_findings <- flag_sensitive_paths(git_visible_existing_paths())
path_audit <- as_audit_rows(visible_path_findings, "git_visible_paths", "git ls-files")

audit <- do.call(rbind, c(column_audits, list(path_audit)))

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
utils::write.csv(
  audit,
  "outputs/tables/ethics_data_governance_audit.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

critical_column_findings <- do.call(rbind, lapply(column_audits, function(rows) {
  if (nrow(rows) == 0L) {
    return(empty_column_audit())
  }
  data.frame(
    column = rows$item,
    category = rows$category,
    severity = rows$severity,
    pattern = NA_character_,
    stringsAsFactors = FALSE
  )
}))

assert_no_critical_ethics_findings(critical_column_findings, visible_path_findings)

cat(sprintf(
  "Ethics/data-governance audit passed: %d review finding(s), 0 critical finding(s)\n",
  sum(audit$severity == "review")
))
