source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/17_h2_sibling_relationships.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data

h2_results <- run_h2_sibling_relationships_pipeline(df_long_scored, df_family_ses, run_cfa = TRUE)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

utils::write.csv(
  h2_results$scaling_summary,
  "outputs/tables/h2_scaling_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$long_descriptives,
  "outputs/tables/h2_long_descriptives.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$family_mean_descriptives,
  "outputs/tables/h2_family_mean_descriptives.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$family_mean_tests,
  "outputs/tables/h2_family_mean_welch_tests.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$apim_fixed_effects,
  "outputs/tables/h2_apim_fixed_effects.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$apim_diagnostics,
  "outputs/tables/h2_apim_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$moderation_fixed_effects,
  "outputs/tables/h2_age_gap_moderation_fixed_effects.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$moderation_anova,
  "outputs/tables/h2_age_gap_moderation_anova.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$moderation_diagnostics,
  "outputs/tables/h2_age_gap_moderation_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$olsen_kenny_status,
  "outputs/tables/h2_olsen_kenny_status.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$olsen_kenny_fit_measures,
  "outputs/tables/h2_olsen_kenny_fit_measures.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$olsen_kenny_latent_correlations,
  "outputs/tables/h2_olsen_kenny_latent_correlations.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$olsen_kenny_parameter_estimates,
  "outputs/tables/h2_olsen_kenny_parameter_estimates.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h2_results$target_summary,
  "outputs/tables/h2_target_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  "H2 sibling relationships audit passed: long n=%d, families=%d, APIM models=%d, Olsen-Kenny=%s, latent r=%.3f\n",
  h2_results$target_summary$long_rows,
  h2_results$target_summary$family_rows,
  h2_results$target_summary$apim_models,
  h2_results$target_summary$olsen_kenny_status,
  h2_results$target_summary$olsen_kenny_latent_correlation
))
