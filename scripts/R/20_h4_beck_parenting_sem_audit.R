source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/19_h4_beck_parenting_sem.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data

h4_results <- run_h4_beck_parenting_sem_pipeline(
  df_family_ses,
  run_sem = TRUE,
  run_multigroup = TRUE,
  multigroup_max_step = "metric_loadings"
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

utils::write.csv(
  h4_results$scaling_summary,
  "outputs/tables/h4_scaling_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$ordered_item_diagnostics,
  "outputs/tables/h4_ordered_item_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$latent_sem_status,
  "outputs/tables/h4_latent_sem_status.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$latent_sem_fit_measures,
  "outputs/tables/h4_latent_sem_fit_measures.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$latent_sem_structural_paths,
  "outputs/tables/h4_latent_sem_structural_paths.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$multigroup_status,
  "outputs/tables/h4_multigroup_status.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$multigroup_fit_measures,
  "outputs/tables/h4_multigroup_fit_measures.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$multigroup_comparison,
  "outputs/tables/h4_multigroup_comparison.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$multigroup_structural_paths,
  "outputs/tables/h4_multigroup_structural_paths.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$multigroup_sparse_collapse_map,
  "outputs/tables/h4_multigroup_sparse_collapse_map.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$bayesian_sem_plan,
  "outputs/tables/h4_bayesian_sem_plan.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  h4_results$target_summary,
  "outputs/tables/h4_target_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  paste0(
    "H4 Beck -> EMBU-P SEM audit passed: families=%d, ordered items=%d, ",
    "latent SEM=%s, multigroup success=%d/%d, Bayesian=%s\n"
  ),
  h4_results$target_summary$family_rows,
  h4_results$target_summary$ordered_items,
  h4_results$target_summary$latent_sem_status,
  h4_results$target_summary$multigroup_success_n,
  h4_results$target_summary$multigroup_steps,
  h4_results$bayesian_sem_plan$status
))
