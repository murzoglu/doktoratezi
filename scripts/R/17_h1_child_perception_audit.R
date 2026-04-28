source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/16_h1_child_perception.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data

h1_results <- run_h1_child_perception_pipeline(df_long_scored, df_family_ses, run_irt = TRUE)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

utils::write.csv(
  h1_results$analysis_frame_summary,
  "outputs/tables/h1_analysis_frame_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$scaling_summary,
  "outputs/tables/h1_scaling_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$outcome_descriptives,
  "outputs/tables/h1_outcome_descriptives.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$primary_fixed_effects,
  "outputs/tables/h1_primary_fixed_effects.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$primary_anova,
  "outputs/tables/h1_primary_anova.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$primary_role_pairwise,
  "outputs/tables/h1_primary_role_pairwise.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$primary_diagnostics,
  "outputs/tables/h1_primary_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$three_way_tests,
  "outputs/tables/h1_three_way_tests.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$three_way_emmeans_grid,
  "outputs/tables/h1_three_way_emmeans_grid.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$three_way_diagnostics,
  "outputs/tables/h1_three_way_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$irt_status,
  "outputs/tables/h1_irt_status.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$irt_item_parameters,
  "outputs/tables/h1_irt_item_parameters.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$irt_theta_fixed_effects,
  "outputs/tables/h1_irt_theta_fixed_effects.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$irt_theta_anova,
  "outputs/tables/h1_irt_theta_anova.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$irt_theta_diagnostics,
  "outputs/tables/h1_irt_theta_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$bayesian_plan,
  "outputs/tables/h1_bayesian_plan.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h1_results$target_summary,
  "outputs/tables/h1_target_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  "H1 child perception audit passed: n=%d, families=%d, primary models=%d, IRT success=%d/%d, Bayesian sampling default=%s\n",
  h1_results$target_summary$analysis_rows,
  h1_results$target_summary$families,
  h1_results$target_summary$primary_models,
  h1_results$target_summary$irt_success_n,
  h1_results$target_summary$irt_subscales,
  h1_results$target_summary$bayesian_sampling_in_default_pipeline
))
