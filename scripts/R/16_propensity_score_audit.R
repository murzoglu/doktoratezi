source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/15_propensity_score.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data

propensity_results <- derive_propensity_score_pipeline(df_family_ses)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)

utils::write.csv(
  propensity_results$model_summary,
  "outputs/tables/propensity_model_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  propensity_results$weight_summary,
  "outputs/tables/propensity_weight_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  propensity_results$balance,
  "outputs/tables/propensity_balance_before_after.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  propensity_results$matching_summary,
  "outputs/tables/propensity_matching_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  propensity_results$overlap_summary,
  "outputs/tables/propensity_overlap_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  propensity_results$doubly_robust_plan,
  "outputs/tables/propensity_doubly_robust_plan.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  propensity_results$target_summary,
  "outputs/tables/propensity_target_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

plot <- plot_propensity_overlap(propensity_results$data)
ggplot2::ggsave(
  "outputs/figures/propensity_overlap.png",
  plot = plot,
  width = 8,
  height = 5,
  dpi = 300
)

cat(sprintf(
  "Propensity score audit passed: n=%d/%d, covariates={%s}, max SMD %.3f -> %.3f IPTW, matched pairs=%d\n",
  propensity_results$target_summary$analysis_rows,
  propensity_results$target_summary$input_rows,
  propensity_results$target_summary$covariates,
  propensity_results$target_summary$max_abs_smd_before,
  propensity_results$target_summary$max_abs_smd_iptw,
  propensity_results$target_summary$matched_pairs
))
