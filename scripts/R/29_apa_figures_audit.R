source("R/25_clinical_utility.R")
source("R/28_apa_figures.R")

if (!requireNamespace("targets", quietly = TRUE)) {
  stop("Required package is not installed: targets", call. = FALSE)
}

targets::tar_load(c(
  table1_group_counts_table,
  causal_dag_nodes_table,
  causal_dag_edges_table,
  propensity_balance_before_after_table,
  df_family_propensity,
  propensity_overlap_summary_table,
  ses_correlation_summary_table,
  h1_primary_fixed_effects_table,
  h1_three_way_emmeans_grid_table,
  h2_apim_fixed_effects_table,
  h3_antidepressant_stratified_group_effects_table,
  h4_latent_sem_structural_paths_table,
  h5_rsa_parameters_table,
  robust_multiverse_spec_table,
  robust_sensemakr_evalue_table,
  clinical_base_performance,
  clinical_full_performance,
  clinical_decision_curve_table,
  clinical_calibration_table,
  clinical_cart_cp_table,
  clinical_rf_importance_table,
  mediation_simple_effect_table,
  mediation_multilevel_effect_table,
  mediation_conditional_effect_table,
  lpa_fit_table,
  network_edges_table,
  network_centrality_table,
  network_nct_table,
  df_family_ses
))

bayes_h1_posterior_table <- utils::read.csv("outputs/tables/bayes_h1_posterior.csv", fileEncoding = "UTF-8")
bayes_h3_posterior_table <- utils::read.csv("outputs/tables/bayes_h3_posterior.csv", fileEncoding = "UTF-8")
bayes_h1_diagnostics_table <- utils::read.csv("outputs/tables/bayes_h1_diagnostics.csv", fileEncoding = "UTF-8")
bayes_h3_diagnostics_table <- utils::read.csv("outputs/tables/bayes_h3_diagnostics.csv", fileEncoding = "UTF-8")

figures <- list(
  strobe_flow = save_apa_plot(
    apa_plot_study_flow(df_family_ses, table1_group_counts_table),
    "outputs/figures/strobe_flow.png",
    width = 7.2,
    height = 5.4
  ),
  causal_dag = save_apa_plot(
    apa_plot_causal_dag(causal_dag_nodes_table, causal_dag_edges_table),
    "outputs/figures/causal_dag.png",
    width = 9.6,
    height = 4.8
  ),
  smd_love_plot = save_apa_plot(
    apa_plot_smd_love(propensity_balance_before_after_table),
    "outputs/figures/smd_love_plot.png",
    width = 7.2,
    height = 4.6
  ),
  propensity_overlap = save_apa_plot(
    apa_plot_propensity_overlap(df_family_propensity, propensity_overlap_summary_table),
    "outputs/figures/propensity_overlap.png",
    width = 7.2,
    height = 4.8
  ),
  ses_correlation_heatmap = save_apa_plot(
    apa_plot_ses_correlation(ses_correlation_summary_table),
    "outputs/figures/ses_correlation_heatmap.png",
    width = 6.8,
    height = 5.8
  ),
  h1_forest = save_apa_plot(
    apa_plot_h1_forest(h1_primary_fixed_effects_table),
    "outputs/figures/h1_forest.png",
    width = 8.2,
    height = 5.1
  ),
  h1_three_way_emm = save_apa_plot(
    apa_plot_h1_three_way_emm(h1_three_way_emmeans_grid_table),
    "outputs/figures/h1_three_way_emm.png",
    width = 10.2,
    height = 8.2
  ),
  h4_sem_path = save_apa_plot(
    apa_plot_h4_sem_path(h4_latent_sem_structural_paths_table),
    "outputs/figures/h4_sem_path.png",
    width = 8.2,
    height = 5.1
  ),
  h5_ba_grid = save_apa_plot(
    apa_plot_h5_bland_altman(df_family_ses),
    "outputs/figures/h5_ba_grid.png",
    width = 10.5,
    height = 8.2
  ),
  h5_rsa_surface = save_apa_plot(
    apa_plot_h5_rsa_surface(h5_rsa_parameters_table, df_family_ses),
    "outputs/figures/h5_rsa_surface.png",
    width = 10.5,
    height = 6.4
  ),
  h2_apim_path = save_apa_plot(
    apa_plot_h2_apim_path(h2_apim_fixed_effects_table),
    "outputs/figures/h2_apim_path.png",
    width = 8.2,
    height = 5.1
  ),
  h3_stratified_forest = save_apa_plot(
    apa_plot_h3_stratified_forest(h3_antidepressant_stratified_group_effects_table),
    "outputs/figures/h3_stratified_forest.png",
    width = 8.2,
    height = 5.1
  ),
  specification_curve = save_apa_plot(
    apa_plot_specification_curve(robust_multiverse_spec_table),
    "outputs/figures/specification_curve.png",
    width = 8.2,
    height = 5.4
  ),
  sensemakr_contour = save_apa_plot(
    apa_plot_sensemakr_contour(robust_sensemakr_evalue_table),
    "outputs/figures/sensemakr_contour.png",
    width = 7.2,
    height = 5.4
  ),
  clinical_roc = save_apa_plot(
    apa_plot_clinical_roc(df_family_ses, clinical_base_performance, clinical_full_performance),
    "outputs/figures/clinical_roc.png",
    width = 6.4,
    height = 5.4
  ),
  clinical_dca = save_apa_plot(
    apa_plot_clinical_dca(clinical_decision_curve_table, clinical_full_performance),
    "outputs/figures/clinical_dca.png",
    width = 7.2,
    height = 5.2
  ),
  clinical_calibration = save_apa_plot(
    apa_plot_clinical_calibration(clinical_calibration_table),
    "outputs/figures/clinical_calibration.png",
    width = 6.4,
    height = 5.4
  ),
  mediation_effects = save_apa_plot(
    apa_plot_mediation_effects(mediation_simple_effect_table, mediation_multilevel_effect_table, mediation_conditional_effect_table),
    "outputs/figures/mediation_effects.png",
    width = 8.2,
    height = 6.6
  ),
  lpa_fit_indices = save_apa_plot(
    apa_plot_lpa_fit(lpa_fit_table),
    "outputs/figures/lpa_fit_indices.png",
    width = 7.2,
    height = 6.2
  ),
  network_graph = save_apa_plot(
    apa_plot_network_graph(network_edges_table, network_centrality_table),
    "outputs/figures/network_graph.png",
    width = 7.4,
    height = 6.2
  ),
  network_nct = save_apa_plot(
    apa_plot_network_nct(network_nct_table),
    "outputs/figures/network_nct.png",
    width = 6.8,
    height = 4.4
  ),
  clinical_cart_rf = save_apa_plot(
    apa_plot_clinical_cart_rf(clinical_cart_cp_table, clinical_rf_importance_table),
    "outputs/figures/clinical_cart_rf.png",
    width = 7.2,
    height = 6.2
  ),
  bayesian_forest = save_apa_plot(
    apa_plot_bayesian_forest(bayes_h1_posterior_table, bayes_h3_posterior_table),
    "outputs/figures/bayesian_forest.png",
    width = 8.2,
    height = 5.8
  ),
  bayesian_diagnostics = save_apa_plot(
    apa_plot_bayesian_diagnostics(bayes_h1_diagnostics_table, bayes_h3_diagnostics_table),
    "outputs/figures/bayesian_diagnostics.png",
    width = 7.2,
    height = 5.2
  )
)

manifest <- apa_figure_manifest(figures)
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
utils::write.csv(
  manifest,
  "outputs/tables/apa_sprint_a_figure_manifest.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  "APA Sprint A figure audit passed: figures=%d, bytes=%s\n",
  nrow(manifest),
  paste(manifest$bytes, collapse = ";")
))
