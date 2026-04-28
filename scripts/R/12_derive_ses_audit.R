source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
ses_results <- derive_ses_composites(df_family_scored)
df_family_ses <- ses_results$data

component_summary <- ses_component_summary(df_family_ses)
correlations <- ses_correlation_table(df_family_ses)
target_summary <- summarize_ses_targets(df_family_scored, df_family_ses)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
utils::write.csv(
  ses_results$diagnostics,
  "outputs/tables/ses_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  ses_results$material_loadings,
  "outputs/tables/ses_material_loadings.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  ses_results$fit_measures,
  "outputs/tables/ses_cfa_fit_measures.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  component_summary,
  "outputs/tables/ses_component_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  correlations,
  "outputs/tables/ses_correlation_table.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  target_summary,
  "outputs/tables/ses_target_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  "SES composite audit passed: family +%d column(s), latent non-missing=%d/%d, material method=%s\n",
  target_summary$added_columns,
  target_summary$ses_latent_non_missing,
  target_summary$ses_rows,
  ses_results$diagnostics$correlation_method
))
