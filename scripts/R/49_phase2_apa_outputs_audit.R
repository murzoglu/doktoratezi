# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXXII/93 audit runner
#
# Faz II audit CSV'lerinden APA tablo + figur paketi uretir.

source("R/48_phase2_apa_outputs.R")

read_if_exists <- function(path) {
  if (file.exists(path)) {
    df <- utils::read.csv(path, stringsAsFactors = FALSE)
    if (nrow(df) > 0L && !"note" %in% names(df)) return(df)
  }
  NULL
}

trifactor_loadings <- read_if_exists("outputs/tables/phase2_trifactor_loadings.csv")
trifactor_fit <- read_if_exists("outputs/tables/phase2_trifactor_fit_indices.csv")
disc_latent <- read_if_exists("outputs/tables/phase2_disc_latent_correlation.csv")
xinfo_summary <- read_if_exists("outputs/tables/phase2_xinfo_summary.csv")
xinfo_edges <- read_if_exists("outputs/tables/phase2_xinfo_edges.csv")
xinfo_centrality <- read_if_exists("outputs/tables/phase2_xinfo_centrality.csv")
floor_irt_delta <- read_if_exists("outputs/tables/phase2_floor_irt_group_delta.csv")
omegah_metrics <- read_if_exists("outputs/tables/phase2_omegah_metrics_summary.csv")
h5ext_pooled <- read_if_exists("outputs/tables/phase2_h5ext_strategy_pooled.csv")
ad_h5_strat <- read_if_exists("outputs/tables/phase2_ad_moderation_h5_stratified_correlations.csv")
hba1c_bayes <- read_if_exists("outputs/tables/phase2_hba1c_bayesian_posterior.csv")
hba1c_spline <- read_if_exists("outputs/tables/phase2_hba1c_spline.csv")
imai_grid <- read_if_exists("outputs/tables/phase2_imai_sensitivity_grid.csv")
imai_summary <- read_if_exists("outputs/tables/phase2_imai_summary.csv")
dag_ci <- read_if_exists("outputs/tables/phase2_dag_ci_tests.csv")
dag_three_level <- read_if_exists("outputs/tables/phase2_dag_three_level.csv")
multi_h1_spec <- read_if_exists("outputs/tables/phase2_multi_h1_spec_results.csv")
multi_h1_curve <- read_if_exists("outputs/tables/phase2_multi_h1_curve_summary.csv")
multi_sca <- read_if_exists("outputs/tables/phase2_multi_sca_inferential.csv")
meta_combined <- read_if_exists("outputs/tables/phase2_meta_combined_studies.csv")
meta_pooling <- read_if_exists("outputs/tables/phase2_meta_pooling_summary.csv")
meta_ppc <- read_if_exists("outputs/tables/phase2_meta_ppc_summary.csv")
clinical_fit <- read_if_exists("outputs/tables/phase2_clinical_fit_summary.csv")
clinical_dca_heatmap <- read_if_exists("outputs/tables/phase2_clinical_dca_heatmap.csv")

result <- run_phase2_apa_outputs_pipeline(
  trifactor_loadings_table = trifactor_loadings,
  trifactor_fit_indices_table = trifactor_fit,
  disc_latent_correlation_table = disc_latent,
  xinfo_summary_table = xinfo_summary,
  xinfo_edges_table = xinfo_edges,
  xinfo_centrality_table = xinfo_centrality,
  floor_irt_group_delta_table = floor_irt_delta,
  omegah_metrics_summary_table = omegah_metrics,
  h5ext_strategy_pooled_table = h5ext_pooled,
  ad_h5_stratified_table = ad_h5_strat,
  hba1c_bayesian_posterior_table = hba1c_bayes,
  hba1c_spline_table = hba1c_spline,
  imai_sensitivity_grid_table = imai_grid,
  imai_summary_table = imai_summary,
  dag_ci_tests_table = dag_ci,
  dag_three_level_table = dag_three_level,
  multi_h1_spec_results_table = multi_h1_spec,
  multi_h1_curve_summary_table = multi_h1_curve,
  multi_sca_inferential_table = multi_sca,
  meta_combined_studies_table = meta_combined,
  meta_pooling_summary_table = meta_pooling,
  meta_ppc_summary_table = meta_ppc,
  clinical_fit_summary_table = clinical_fit,
  clinical_dca_heatmap_table = clinical_dca_heatmap,
  output_dir = "outputs/figures"
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

if (!is.null(result$summary_table)) {
  utils::write.csv(result$summary_table,
    "outputs/tables/phase2_apa_summary_table.csv",
    row.names = FALSE, fileEncoding = "UTF-8")
}
utils::write.csv(result$target_summary,
  "outputs/tables/phase2_apa_target_summary.csv",
  row.names = FALSE, fileEncoding = "UTF-8")

cat(sprintf("[Faz II/KISIM XXXII/93] APA outputs: %d figur + %d ozet satir\n",
  length(result$figure_paths),
  if (!is.null(result$summary_table)) nrow(result$summary_table) else 0L))
cat("Figure paths:\n")
for (p in result$figure_paths) cat("  ", p, "\n", sep = "")

invisible(result)
