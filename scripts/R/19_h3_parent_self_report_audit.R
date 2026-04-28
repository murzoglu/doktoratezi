source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/15_propensity_score.R")
source("R/18_h3_parent_self_report.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data
df_family_propensity <- derive_propensity_score_pipeline(df_family_ses)$data

h3_results <- run_h3_parent_self_report_pipeline(df_family_ses, df_family_propensity)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

utils::write.csv(
  h3_results$scaling_summary,
  "outputs/tables/h3_scaling_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$outcome_descriptives,
  "outputs/tables/h3_outcome_descriptives.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$antidepressant_counts,
  "outputs/tables/h3_antidepressant_counts.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$primary_fixed_effects,
  "outputs/tables/h3_primary_fixed_effects.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$primary_group_effects,
  "outputs/tables/h3_primary_group_effects.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$primary_diagnostics,
  "outputs/tables/h3_primary_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$antidepressant_stratified_group_effects,
  "outputs/tables/h3_antidepressant_stratified_group_effects.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$iptw_fixed_effects,
  "outputs/tables/h3_iptw_fixed_effects.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$iptw_group_effects,
  "outputs/tables/h3_iptw_group_effects.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$iptw_diagnostics,
  "outputs/tables/h3_iptw_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h3_results$target_summary,
  "outputs/tables/h3_target_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  paste0(
    "H3 parent self-report audit passed: families=%d, primary models=%d, ",
    "stratified rows=%d/%d fitted, IPTW models=%d, AD yes=%d (DM=%d, control=%d)\n"
  ),
  h3_results$target_summary$family_rows,
  h3_results$target_summary$primary_models,
  h3_results$target_summary$stratified_fitted_rows,
  h3_results$target_summary$stratified_rows,
  h3_results$target_summary$iptw_models,
  h3_results$target_summary$antidepressant_yes_n,
  h3_results$target_summary$antidepressant_yes_dm_n,
  h3_results$target_summary$antidepressant_yes_control_n
))
