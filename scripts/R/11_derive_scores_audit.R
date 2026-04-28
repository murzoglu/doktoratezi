source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)

range_audit <- score_range_audit(df_family, df_long)
assert_no_score_range_violations(range_audit)

df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)

dictionary <- derived_score_dictionary()
family_score_columns <- score_columns_from_dictionary(dictionary[dictionary$dataset == "family", , drop = FALSE])
long_score_columns <- score_columns_from_dictionary(dictionary[dictionary$dataset == "long", , drop = FALSE])

coverage <- rbind(
  score_coverage(df_family_scored, family_score_columns, "family"),
  score_coverage(df_long_scored, long_score_columns, "long")
)
summary <- summarize_derived_score_targets(df_family, df_long, df_family_scored, df_long_scored)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
utils::write.csv(
  dictionary,
  "outputs/tables/derived_score_dictionary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  range_audit,
  "outputs/tables/derived_score_range_audit.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  coverage,
  "outputs/tables/derived_score_coverage.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  summary,
  "outputs/tables/derived_score_audit_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  "Derived score audit passed: %d definition row(s), family +%d column(s), long +%d column(s), 0 range violation(s)\n",
  nrow(dictionary),
  summary$added_columns[summary$dataset == "family"],
  summary$added_columns[summary$dataset == "long"]
))
