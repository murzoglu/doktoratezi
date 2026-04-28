source("R/29_apa_tables.R")

if (!requireNamespace("targets", quietly = TRUE)) {
  stop("Required package is not installed: targets", call. = FALSE)
}

targets::tar_load(c(
  table1_family_summary_table,
  propensity_balance_before_after_table,
  missing_variable_summary_table,
  propensity_model_summary_table,
  propensity_weight_summary_table,
  propensity_overlap_summary_table,
  ses_component_summary_table,
  ses_cfa_fit_measures_table,
  h1_primary_fixed_effects_table,
  h1_primary_anova_table,
  h2_family_mean_welch_tests_table,
  h2_apim_fixed_effects_table,
  h3_primary_group_effects_table,
  h3_iptw_group_effects_table,
  h3_antidepressant_stratified_group_effects_table,
  robust_tost_equivalence_table,
  h4_latent_sem_fit_measures_table,
  h4_latent_sem_structural_paths_table,
  h5_icc_bland_altman_table,
  h5_dyadic_cfa_latent_corr_table,
  h5_k_coefficient_table,
  h5_inconsistency_patterns_table,
  mediation_simple_effect_table,
  mediation_multilevel_effect_table,
  mediation_conditional_effect_table,
  lpa_fit_table,
  lca_fit_table,
  lca_modal_regression_table,
  flexmix_fit_table,
  bifactor_s1_fit_table,
  network_centrality_table,
  network_nct_table,
  clinical_base_performance,
  clinical_full_performance,
  clinical_nri_idi_table,
  dm_n_summary_table,
  dm_hba1c_interaction_table,
  dm_duration_spline_table,
  dm_strata_tests_table,
  robust_multiverse_summary_table,
  robust_sensemakr_evalue_table,
  robust_negative_control_table,
  robust_falsification_table
))

bayes_h1_posterior_table <- utils::read.csv("outputs/tables/bayes_h1_posterior.csv", fileEncoding = "UTF-8")
bayes_h3_posterior_table <- utils::read.csv("outputs/tables/bayes_h3_posterior.csv", fileEncoding = "UTF-8")
bayes_h1_diagnostics_table <- utils::read.csv("outputs/tables/bayes_h1_diagnostics.csv", fileEncoding = "UTF-8")
bayes_h3_diagnostics_table <- utils::read.csv("outputs/tables/bayes_h3_diagnostics.csv", fileEncoding = "UTF-8")
bayes_loo_waic_table <- utils::read.csv("outputs/tables/bayes_loo_waic.csv", fileEncoding = "UTF-8")

bundle <- apa_build_table_bundle(
  table1_family_summary_table = table1_family_summary_table,
  propensity_balance_before_after_table = propensity_balance_before_after_table,
  missing_variable_summary_table = missing_variable_summary_table,
  propensity_model_summary_table = propensity_model_summary_table,
  propensity_weight_summary_table = propensity_weight_summary_table,
  propensity_overlap_summary_table = propensity_overlap_summary_table,
  ses_component_summary_table = ses_component_summary_table,
  ses_cfa_fit_measures_table = ses_cfa_fit_measures_table,
  h1_primary_fixed_effects_table = h1_primary_fixed_effects_table,
  h1_primary_anova_table = h1_primary_anova_table,
  bayes_h1_posterior_table = bayes_h1_posterior_table,
  bayes_h1_diagnostics_table = bayes_h1_diagnostics_table,
  h2_family_mean_welch_tests_table = h2_family_mean_welch_tests_table,
  h2_apim_fixed_effects_table = h2_apim_fixed_effects_table,
  h3_primary_group_effects_table = h3_primary_group_effects_table,
  h3_iptw_group_effects_table = h3_iptw_group_effects_table,
  h3_antidepressant_stratified_group_effects_table = h3_antidepressant_stratified_group_effects_table,
  bayes_h3_posterior_table = bayes_h3_posterior_table,
  bayes_h3_diagnostics_table = bayes_h3_diagnostics_table,
  robust_tost_equivalence_table = robust_tost_equivalence_table,
  h4_latent_sem_fit_measures_table = h4_latent_sem_fit_measures_table,
  h4_latent_sem_structural_paths_table = h4_latent_sem_structural_paths_table,
  h5_icc_bland_altman_table = h5_icc_bland_altman_table,
  h5_dyadic_cfa_latent_corr_table = h5_dyadic_cfa_latent_corr_table,
  h5_k_coefficient_table = h5_k_coefficient_table,
  h5_inconsistency_patterns_table = h5_inconsistency_patterns_table,
  mediation_simple_effect_table = mediation_simple_effect_table,
  mediation_multilevel_effect_table = mediation_multilevel_effect_table,
  mediation_conditional_effect_table = mediation_conditional_effect_table,
  lpa_fit_table = lpa_fit_table,
  lca_fit_table = lca_fit_table,
  lca_modal_regression_table = lca_modal_regression_table,
  flexmix_fit_table = flexmix_fit_table,
  bifactor_s1_fit_table = bifactor_s1_fit_table,
  network_centrality_table = network_centrality_table,
  network_nct_table = network_nct_table,
  clinical_base_performance = clinical_base_performance,
  clinical_full_performance = clinical_full_performance,
  clinical_nri_idi_table = clinical_nri_idi_table,
  dm_n_summary_table = dm_n_summary_table,
  dm_hba1c_interaction_table = dm_hba1c_interaction_table,
  dm_duration_spline_table = dm_duration_spline_table,
  dm_strata_tests_table = dm_strata_tests_table,
  robust_multiverse_summary_table = robust_multiverse_summary_table,
  robust_sensemakr_evalue_table = robust_sensemakr_evalue_table,
  robust_negative_control_table = robust_negative_control_table,
  robust_falsification_table = robust_falsification_table,
  bayes_loo_waic_table = bayes_loo_waic_table
)

stopifnot(length(bundle) == 22L)
stopifnot(!anyDuplicated(names(bundle)))
stopifnot(all(vapply(bundle, is.data.frame, logical(1))))
stopifnot(all(vapply(bundle, nrow, integer(1)) > 0L))
stopifnot(all(nzchar(vapply(bundle, attr, character(1), which = "title", exact = TRUE))))

tmp_dir <- tempfile("apa_tables_")
paths <- save_apa_table_bundle(bundle, tmp_dir)
manifest <- apa_table_manifest(paths, bundle)
stopifnot(nrow(manifest) == 22L)
stopifnot(all(manifest$exists))
stopifnot(all(manifest$bytes > 0))
stopifnot(all(file.exists(paths)))

cat("[PASS] APA tables Sprint A bundle\n")
