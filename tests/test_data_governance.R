source("R/08_data_governance.R")

column_findings <- flag_sensitive_column_names(c(
  "aile_no",
  "cocuk_no",
  "anne_dogum_tarihi",
  "ad_soyad",
  "tc_kimlik_no",
  "telefon"
))

stopifnot(any(column_findings$column == "anne_dogum_tarihi" & column_findings$severity == "review"))
stopifnot(any(column_findings$column == "ad_soyad" & column_findings$severity == "critical"))
stopifnot(any(column_findings$column == "tc_kimlik_no" & column_findings$severity == "critical"))
stopifnot(!any(column_findings$column == "aile_no" & column_findings$severity == "critical"))

path_findings <- flag_sensitive_paths(c(
  "data/raw/source.csv",
  "data/processed/FINAL_REFERENCE__analysis_base_long.csv",
  ".env",
  "outputs/tables/example.csv",
  "docs/analiz_planlari/STATISTICAL-ANALYSIS-PLAN.md"
))

stopifnot(any(path_findings$path == "data/raw/source.csv" & path_findings$severity == "critical"))
stopifnot(any(path_findings$path == "data/processed/FINAL_REFERENCE__analysis_base_long.csv" & path_findings$severity == "critical"))
stopifnot(any(path_findings$path == ".env" & path_findings$severity == "critical"))
stopifnot(any(path_findings$path == "outputs/tables/example.csv" & path_findings$severity == "review"))
stopifnot(!any(path_findings$path == "docs/analiz_planlari/STATISTICAL-ANALYSIS-PLAN.md"))

safe_columns <- flag_sensitive_column_names(c("aile_no", "cocuk_no", "group", "role"))
safe_paths <- flag_sensitive_paths(c("R/08_data_governance.R", "docs/FINAL_REFERENCE_VERI_HARITASI.md"))
stop_if_not_safe <- assert_no_critical_ethics_findings(safe_columns, safe_paths)
stopifnot(isTRUE(stop_if_not_safe))

stopifnot(inherits(
  try(assert_no_critical_ethics_findings(column_findings, empty_path_audit()), silent = TRUE),
  "try-error"
))
