library(targets)

source("R/00_paths.R")
source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/12_missing_data_frames.R")
source("R/13_table1_smd.R")
source("R/14_causal_dag.R")
source("R/15_propensity_score.R")
source("R/16_h1_child_perception.R")
source("R/17_h2_sibling_relationships.R")
source("R/18_h3_parent_self_report.R")
source("R/19_h4_beck_parenting_sem.R")
source("R/20_h5_dyadic_concordance.R")
source("R/21_robustness_sensitivity.R")
source("R/22_bayesian_parallel.R")
source("R/23_mediation.R")
source("R/24_latent_profile.R")
source("R/25_clinical_utility.R")
source("R/26_network_analysis.R")
source("R/27_dm_subanalyses.R")
source("R/28_apa_figures.R")
source("R/29_apa_tables.R")
source("R/30_thesis_mapping.R")
source("R/31_final_plans.R")
# Faz II SAP (KISIM XIX-XXXV) — [KESIFSEL · POST-HOC]
source("R/32_trifactor_model.R")
source("R/33_informant_discrepancy.R")
source("R/34_cross_informant_network.R")
source("R/35_floor_aware_irt.R")
source("R/36_reliability_generalization.R")
source("R/37_esem_embu.R")
source("R/38_antidepressant_pathway.R")
source("R/39_h5_extensions.R")
source("R/40_hba1c_joint.R")
source("R/41_causal_mediation.R")
source("R/42_dag_pc_fci.R")
source("R/43_distributional.R")
source("R/44_multiverse_extension.R")
source("R/45_bayesian_meta.R")

tar_option_set(
  packages = character()
)

list(
  tar_target(project_paths, thesis_paths()),
  tar_target(raw_data_manifest, list_raw_data(project_paths$raw_data_dir)),
  tar_target(final_reference_paths, canonical_final_reference_paths(project_paths$processed_data_dir)),
  tar_target(lock_file, final_reference_paths$lock, format = "file"),
  tar_target(family_csv, final_reference_paths$family, format = "file"),
  tar_target(long_csv, final_reference_paths$long, format = "file"),
  tar_target(
    final_reference_manifest,
    final_reference_validation_manifest(lock_file, c(family_csv, long_csv))
  ),
  tar_target(df_family_raw, validate_and_load(family_csv, lock_file)),
  tar_target(df_long_raw, validate_and_load(long_csv, lock_file)),
  tar_target(df_family, prepare_family(df_family_raw)),
  tar_target(df_long, prepare_long(df_long_raw)),
  tar_target(
    final_reference_loaded_summary,
    summarize_loaded_final_reference(df_family_raw, df_long_raw, df_family, df_long)
  ),
  tar_target(derived_score_dictionary_table, derived_score_dictionary()),
  tar_target(derived_score_range_audit, score_range_audit(df_family, df_long)),
  tar_target(derived_score_range_ok, assert_no_score_range_violations(derived_score_range_audit)),
  tar_target(df_family_scored, derive_family_scores(df_family)),
  tar_target(df_long_scored, derive_long_scores(df_long)),
  tar_target(
    derived_score_target_summary,
    summarize_derived_score_targets(df_family, df_long, df_family_scored, df_long_scored)
  ),
  tar_target(ses_results, derive_ses_composites(df_family_scored)),
  tar_target(df_family_ses, ses_results$data),
  tar_target(ses_diagnostics_table, ses_results$diagnostics),
  tar_target(ses_material_loadings_table, ses_results$material_loadings),
  tar_target(ses_cfa_fit_measures_table, ses_results$fit_measures),
  tar_target(ses_component_summary_table, ses_component_summary(df_family_ses)),
  tar_target(ses_correlation_summary_table, ses_correlation_table(df_family_ses)),
  tar_target(
    ses_target_summary,
    summarize_ses_targets(df_family_scored, df_family_ses)
  ),
  tar_target(missing_results, derive_missing_data_frames(df_family_ses)),
  tar_target(df_family_missing_fiml, missing_results$frames$fiml_primary),
  tar_target(df_family_missing_complete_case, missing_results$frames$complete_case_primary),
  tar_target(df_family_missing_mi_primary, missing_results$frames$mi_primary),
  tar_target(df_family_missing_mi_clinical_sensitivity, missing_results$frames$mi_clinical_sensitivity),
  tar_target(missing_variable_summary_table, missing_results$variable_summary),
  tar_target(missing_block_summary_table, missing_results$block_summary),
  tar_target(missing_group_summary_table, missing_results$group_summary),
  tar_target(missing_pattern_summary_table, missing_results$pattern_summary),
  tar_target(missing_frame_manifest_table, missing_results$frame_manifest),
  tar_target(missing_mice_method_plan_table, missing_results$mice_method_plan),
  tar_target(missing_mcar_test_table, missing_results$mcar_test),
  tar_target(missing_nmar_delta_grid_table, missing_results$nmar_delta_grid),
  tar_target(
    missing_imputations,
    run_missing_imputation_set(missing_results, m = 50L, maxit = 30L)
  ),
  tar_target(missing_mi_diagnostics_table, summarize_missing_mice(missing_imputations)),
  tar_target(
    missing_target_summary,
    summarize_missing_targets(df_family_ses, missing_results)
  ),
  tar_target(table1_results, build_table1_family(df_family_ses)),
  tar_target(table1_family_summary_table, table1_results$table),
  tar_target(table1_smd_balance_table, table1_results$smd_balance),
  tar_target(table1_balance_action_table, table1_results$balance_action),
  tar_target(table1_group_counts_table, table1_results$group_counts),
  tar_target(
    table1_target_summary,
    summarize_table1_targets(df_family_ses, table1_results)
  ),
  tar_target(causal_dag_results, build_causal_dag()),
  tar_target(causal_dag_nodes_table, causal_dag_results$nodes),
  tar_target(causal_dag_edges_table, causal_dag_results$edges),
  tar_target(causal_dag_adjustment_sets_table, causal_dag_results$adjustment_sets),
  tar_target(causal_dag_conditional_independencies_table, causal_dag_results$conditional_independencies),
  tar_target(causal_dag_covariate_strategy_table, causal_dag_results$covariate_strategy),
  tar_target(causal_dag_variable_mapping_table, causal_dag_results$variable_mapping),
  tar_target(causal_dag_proxy_validation_table, validate_causal_dag_data_proxies(df_family_ses)),
  tar_target(
    causal_dag_target_summary,
    summarize_causal_dag_targets(causal_dag_results, causal_dag_proxy_validation_table)
  ),
  tar_target(propensity_results, derive_propensity_score_pipeline(df_family_ses)),
  tar_target(df_family_propensity, propensity_results$data),
  tar_target(propensity_model_summary_table, propensity_results$model_summary),
  tar_target(propensity_weight_summary_table, propensity_results$weight_summary),
  tar_target(propensity_balance_before_after_table, propensity_results$balance),
  tar_target(propensity_matching_summary_table, propensity_results$matching_summary),
  tar_target(propensity_overlap_summary_table, propensity_results$overlap_summary),
  tar_target(propensity_doubly_robust_plan_table, propensity_results$doubly_robust_plan),
  tar_target(
    propensity_target_summary,
    propensity_results$target_summary
  ),
  tar_target(h1_child_perception_results, run_h1_child_perception_pipeline(df_long_scored, df_family_ses, run_irt = TRUE)),
  tar_target(h1_analysis_frame_summary_table, h1_child_perception_results$analysis_frame_summary),
  tar_target(h1_scaling_summary_table, h1_child_perception_results$scaling_summary),
  tar_target(h1_outcome_descriptives_table, h1_child_perception_results$outcome_descriptives),
  tar_target(h1_primary_fixed_effects_table, h1_child_perception_results$primary_fixed_effects),
  tar_target(h1_primary_anova_table, h1_child_perception_results$primary_anova),
  tar_target(h1_primary_role_pairwise_table, h1_child_perception_results$primary_role_pairwise),
  tar_target(h1_primary_diagnostics_table, h1_child_perception_results$primary_diagnostics),
  tar_target(h1_three_way_tests_table, h1_child_perception_results$three_way_tests),
  tar_target(h1_three_way_emmeans_grid_table, h1_child_perception_results$three_way_emmeans_grid),
  tar_target(h1_three_way_diagnostics_table, h1_child_perception_results$three_way_diagnostics),
  tar_target(h1_irt_status_table, h1_child_perception_results$irt_status),
  tar_target(h1_irt_item_parameters_table, h1_child_perception_results$irt_item_parameters),
  tar_target(h1_irt_theta_fixed_effects_table, h1_child_perception_results$irt_theta_fixed_effects),
  tar_target(h1_irt_theta_anova_table, h1_child_perception_results$irt_theta_anova),
  tar_target(h1_irt_theta_diagnostics_table, h1_child_perception_results$irt_theta_diagnostics),
  tar_target(h1_bayesian_plan_table, h1_child_perception_results$bayesian_plan),
  tar_target(
    h1_target_summary,
    h1_child_perception_results$target_summary
  ),
  tar_target(h2_sibling_relationships_results, run_h2_sibling_relationships_pipeline(df_long_scored, df_family_ses, run_cfa = TRUE)),
  tar_target(h2_scaling_summary_table, h2_sibling_relationships_results$scaling_summary),
  tar_target(h2_long_descriptives_table, h2_sibling_relationships_results$long_descriptives),
  tar_target(h2_family_mean_descriptives_table, h2_sibling_relationships_results$family_mean_descriptives),
  tar_target(h2_family_mean_welch_tests_table, h2_sibling_relationships_results$family_mean_tests),
  tar_target(h2_apim_fixed_effects_table, h2_sibling_relationships_results$apim_fixed_effects),
  tar_target(h2_apim_diagnostics_table, h2_sibling_relationships_results$apim_diagnostics),
  tar_target(h2_age_gap_moderation_fixed_effects_table, h2_sibling_relationships_results$moderation_fixed_effects),
  tar_target(h2_age_gap_moderation_anova_table, h2_sibling_relationships_results$moderation_anova),
  tar_target(h2_age_gap_moderation_diagnostics_table, h2_sibling_relationships_results$moderation_diagnostics),
  tar_target(h2_olsen_kenny_status_table, h2_sibling_relationships_results$olsen_kenny_status),
  tar_target(h2_olsen_kenny_fit_measures_table, h2_sibling_relationships_results$olsen_kenny_fit_measures),
  tar_target(h2_olsen_kenny_latent_correlations_table, h2_sibling_relationships_results$olsen_kenny_latent_correlations),
  tar_target(h2_olsen_kenny_parameter_estimates_table, h2_sibling_relationships_results$olsen_kenny_parameter_estimates),
  tar_target(
    h2_target_summary,
    h2_sibling_relationships_results$target_summary
  ),
  tar_target(h3_parent_self_report_results, run_h3_parent_self_report_pipeline(df_family_ses, df_family_propensity)),
  tar_target(h3_scaling_summary_table, h3_parent_self_report_results$scaling_summary),
  tar_target(h3_outcome_descriptives_table, h3_parent_self_report_results$outcome_descriptives),
  tar_target(h3_antidepressant_counts_table, h3_parent_self_report_results$antidepressant_counts),
  tar_target(h3_primary_fixed_effects_table, h3_parent_self_report_results$primary_fixed_effects),
  tar_target(h3_primary_group_effects_table, h3_parent_self_report_results$primary_group_effects),
  tar_target(h3_primary_diagnostics_table, h3_parent_self_report_results$primary_diagnostics),
  tar_target(
    h3_antidepressant_stratified_group_effects_table,
    h3_parent_self_report_results$antidepressant_stratified_group_effects
  ),
  tar_target(h3_iptw_fixed_effects_table, h3_parent_self_report_results$iptw_fixed_effects),
  tar_target(h3_iptw_group_effects_table, h3_parent_self_report_results$iptw_group_effects),
  tar_target(h3_iptw_diagnostics_table, h3_parent_self_report_results$iptw_diagnostics),
  tar_target(
    h3_target_summary,
    h3_parent_self_report_results$target_summary
  ),
  tar_target(
    h4_beck_parenting_sem_results,
    run_h4_beck_parenting_sem_pipeline(
      df_family_ses,
      run_sem = TRUE,
      run_multigroup = TRUE,
      multigroup_max_step = "metric_loadings"
    )
  ),
  tar_target(h4_scaling_summary_table, h4_beck_parenting_sem_results$scaling_summary),
  tar_target(h4_ordered_item_diagnostics_table, h4_beck_parenting_sem_results$ordered_item_diagnostics),
  tar_target(h4_latent_sem_status_table, h4_beck_parenting_sem_results$latent_sem_status),
  tar_target(h4_latent_sem_fit_measures_table, h4_beck_parenting_sem_results$latent_sem_fit_measures),
  tar_target(h4_latent_sem_structural_paths_table, h4_beck_parenting_sem_results$latent_sem_structural_paths),
  tar_target(h4_multigroup_status_table, h4_beck_parenting_sem_results$multigroup_status),
  tar_target(h4_multigroup_fit_measures_table, h4_beck_parenting_sem_results$multigroup_fit_measures),
  tar_target(h4_multigroup_comparison_table, h4_beck_parenting_sem_results$multigroup_comparison),
  tar_target(h4_multigroup_structural_paths_table, h4_beck_parenting_sem_results$multigroup_structural_paths),
  tar_target(h4_multigroup_sparse_collapse_map_table, h4_beck_parenting_sem_results$multigroup_sparse_collapse_map),
  tar_target(h4_bayesian_sem_plan_table, h4_beck_parenting_sem_results$bayesian_sem_plan),
  tar_target(
    h4_target_summary,
    h4_beck_parenting_sem_results$target_summary
  ),
  tar_target(
    h5_dyadic_concordance_results,
    run_h5_dyadic_concordance_pipeline(
      df_family_ses = df_family_ses,
      df_family_scored = df_family_scored,
      df_long_scored = df_long_scored,
      run_rsa = TRUE,
      run_cfa = TRUE,
      run_k = TRUE,
      n_boot = 200L
    )
  ),
  tar_target(h5_icc_bland_altman_table,         h5_dyadic_concordance_results$icc_bland_altman_table),
  tar_target(h5_rsa_status_table,               h5_dyadic_concordance_results$rsa_status_table),
  tar_target(h5_rsa_parameters_table,           h5_dyadic_concordance_results$rsa_parameters_table),
  tar_target(h5_common_fate_status_table,       h5_dyadic_concordance_results$common_fate_status_table),
  tar_target(h5_common_fate_fit_measures_table, h5_dyadic_concordance_results$common_fate_fit_measures_table),
  tar_target(h5_common_fate_loadings_table,     h5_dyadic_concordance_results$common_fate_loadings_table),
  tar_target(h5_common_fate_regressions_table,  h5_dyadic_concordance_results$common_fate_regressions_table),
  tar_target(h5_dyadic_cfa_status_table,        h5_dyadic_concordance_results$dyadic_cfa_status_table),
  tar_target(h5_dyadic_cfa_fit_measures_table,  h5_dyadic_concordance_results$dyadic_cfa_fit_measures_table),
  tar_target(h5_dyadic_cfa_latent_corr_table,   h5_dyadic_concordance_results$dyadic_cfa_latent_corr_table),
  tar_target(h5_k_coefficient_table,            h5_dyadic_concordance_results$k_coefficient_table),
  tar_target(h5_inconsistency_patterns_table,   h5_dyadic_concordance_results$inconsistency_patterns_table),
  tar_target(h5_target_summary,                 h5_dyadic_concordance_results$target_summary),

  # KISIM XI — Robustluk + Sensitivite (multiverse + TOST + sensemakr + neg ctrl + falsification)
  tar_target(
    robustness_results,
    run_robustness_pipeline(df_family_ses, sesoi_d = 0.30)
  ),
  tar_target(robust_multiverse_spec_table,    robustness_results$multiverse_spec_table),
  tar_target(robust_multiverse_summary_table, robustness_results$multiverse_summary_table),
  tar_target(robust_tost_equivalence_table,   robustness_results$tost_equivalence_table),
  tar_target(robust_sensemakr_evalue_table,   robustness_results$sensemakr_evalue_table),
  tar_target(robust_negative_control_table,   robustness_results$negative_control_table),
  tar_target(robust_falsification_table,      robustness_results$falsification_table),
  tar_target(robust_target_summary,           robustness_results$target_summary),

  # KISIM VI — Mediation (Beck → EMBU-P_redd → EMBU-C_redd)
  tar_target(
    mediation_results,
    run_mediation_pipeline(
      df_family_ses, df_long_scored,
      subscale = "reddetme",
      run_bayes = FALSE,
      n_boot = 1000L
    )
  ),
  tar_target(mediation_status_table,             mediation_results$status_table),
  tar_target(mediation_simple_effect_table,      mediation_results$simple_effect_table),
  tar_target(mediation_simple_fit_table,         mediation_results$simple_fit_table),
  tar_target(mediation_multilevel_effect_table,  mediation_results$multilevel_effect_table),
  tar_target(mediation_multilevel_fit_table,     mediation_results$multilevel_fit_table),
  tar_target(mediation_conditional_effect_table, mediation_results$conditional_effect_table),
  tar_target(mediation_conditional_fit_table,    mediation_results$conditional_fit_table),
  tar_target(mediation_target_summary,           mediation_results$target_summary),

  # KISIM VII — Latent değişken: LPA + LCA + Mixture Regression + Bifactor S-1
  tar_target(
    latent_profile_results,
    run_latent_profile_pipeline(
      df_family_ses, df_family_scored,
      profile_range = 1:5,
      lca_class_range = 1:4,
      run_bifactor = TRUE,
      run_lca_sensitivity = TRUE,
      run_flexmix_sensitivity = TRUE,
      seed = 20260428L
    )
  ),
  tar_target(lpa_status_table,                latent_profile_results$status_table),
  tar_target(lpa_fit_table,                   latent_profile_results$lpa_fit_table),
  tar_target(lpa_classes_table,               latent_profile_results$lpa_classes_table),
  tar_target(lpa_profile_means_table,         latent_profile_results$lpa_profile_means_table),
  tar_target(lpa_group_distribution_table,    latent_profile_results$lpa_group_distribution),
  tar_target(lca_indicator_audit_table,       latent_profile_results$lca_indicator_audit_table),
  tar_target(lca_fit_table,                   latent_profile_results$lca_fit_table),
  tar_target(lca_classes_table,               latent_profile_results$lca_classes_table),
  tar_target(lca_item_response_prob_table,    latent_profile_results$lca_item_response_prob_table),
  tar_target(lca_group_distribution_table,    latent_profile_results$lca_group_distribution),
  tar_target(lca_modal_regression_table,      latent_profile_results$lca_modal_regression_table),
  tar_target(flexmix_fit_table,               latent_profile_results$flexmix_fit_table),
  tar_target(flexmix_coefficient_table,       latent_profile_results$flexmix_coefficient_table),
  tar_target(flexmix_class_distribution_table, latent_profile_results$flexmix_class_distribution),
  tar_target(flexmix_group_distribution_table, latent_profile_results$flexmix_group_distribution),
  tar_target(bifactor_s1_fit_table,           latent_profile_results$bifactor_fit_table),
  tar_target(bifactor_s1_loadings_table,      latent_profile_results$bifactor_loadings_table),

  # KISIM VIII — Network analizi: GGM + NCT + Beck symptom
  tar_target(
    network_results,
    run_network_pipeline(df_family_ses, df_family_scored, seed = 20260428L)
  ),
  tar_target(network_status_table,           network_results$status_table),
  tar_target(network_edges_table,            network_results$edges_table),
  tar_target(network_centrality_table,       network_results$centrality_table),
  tar_target(network_nct_table,              network_results$nct_table),
  tar_target(network_beck_centrality_table,  network_results$beck_centrality_table),

  # KISIM IX — Klinik fayda: risk skor + ROC + DCA + CART + RF + NRI/IDI
  tar_target(
    clinical_utility_results,
    run_clinical_utility_pipeline(df_family_ses, seed = 20260428L)
  ),
  tar_target(clinical_status_table,        clinical_utility_results$status_table),
  tar_target(clinical_base_coef_table,     clinical_utility_results$base_coef_table),
  tar_target(clinical_base_performance,    clinical_utility_results$base_performance),
  tar_target(clinical_full_coef_table,     clinical_utility_results$full_coef_table),
  tar_target(clinical_full_performance,    clinical_utility_results$full_performance),
  tar_target(clinical_decision_curve_table, clinical_utility_results$decision_curve_table),
  tar_target(clinical_cart_cp_table,       clinical_utility_results$cart_cp_table),
  tar_target(clinical_rf_importance_table, clinical_utility_results$rf_importance_table),
  tar_target(clinical_calibration_table,   clinical_utility_results$calibration_table),
  tar_target(clinical_nri_idi_table,       clinical_utility_results$nri_idi_table),

  # KISIM X — DM klinik alt-analizler (HbA1c × parenting, dm_yili spline, tanı yaşı strata)
  tar_target(
    dm_subanalyses_results,
    run_dm_subanalyses_pipeline(df_family_ses)
  ),
  tar_target(dm_n_summary_table,           dm_subanalyses_results$n_summary_table),
  tar_target(dm_hba1c_interaction_table,   dm_subanalyses_results$hba1c_interaction_table),
  tar_target(dm_duration_spline_table,     dm_subanalyses_results$spline_duration_table),
  tar_target(dm_strata_descriptive_table,  dm_subanalyses_results$strata_descriptive_table),
  tar_target(dm_strata_tests_table,        dm_subanalyses_results$strata_tests_table),

  # KISIM XIII / 40 — APA tablo + sekil paketi, Sprint A paketleri
  tar_target(bayes_h1_posterior_table, utils::read.csv("outputs/tables/bayes_h1_posterior.csv", fileEncoding = "UTF-8")),
  tar_target(bayes_h3_posterior_table, utils::read.csv("outputs/tables/bayes_h3_posterior.csv", fileEncoding = "UTF-8")),
  tar_target(bayes_h1_diagnostics_table, utils::read.csv("outputs/tables/bayes_h1_diagnostics.csv", fileEncoding = "UTF-8")),
  tar_target(bayes_h3_diagnostics_table, utils::read.csv("outputs/tables/bayes_h3_diagnostics.csv", fileEncoding = "UTF-8")),
  tar_target(bayes_loo_waic_table, utils::read.csv("outputs/tables/bayes_loo_waic.csv", fileEncoding = "UTF-8")),
  tar_target(apa_h1_forest_plot, apa_plot_h1_forest(h1_primary_fixed_effects_table)),
  tar_target(apa_h4_sem_path_plot, apa_plot_h4_sem_path(h4_latent_sem_structural_paths_table)),
  tar_target(apa_h5_bland_altman_plot, apa_plot_h5_bland_altman(df_family_ses)),
  tar_target(apa_h5_rsa_surface_plot, apa_plot_h5_rsa_surface(h5_rsa_parameters_table, df_family_ses)),
  tar_target(apa_h2_apim_path_plot, apa_plot_h2_apim_path(h2_apim_fixed_effects_table)),
  tar_target(apa_h3_stratified_forest_plot, apa_plot_h3_stratified_forest(h3_antidepressant_stratified_group_effects_table)),
  tar_target(apa_specification_curve_plot, apa_plot_specification_curve(robust_multiverse_spec_table)),
  tar_target(apa_sensemakr_contour_plot, apa_plot_sensemakr_contour(robust_sensemakr_evalue_table)),
  tar_target(apa_clinical_roc_plot, apa_plot_clinical_roc(df_family_ses, clinical_base_performance, clinical_full_performance)),
  tar_target(apa_clinical_dca_plot, apa_plot_clinical_dca(clinical_decision_curve_table, clinical_full_performance)),
  tar_target(apa_clinical_calibration_plot, apa_plot_clinical_calibration(clinical_calibration_table)),
  tar_target(apa_strobe_flow_plot, apa_plot_study_flow(df_family_ses, table1_group_counts_table)),
  tar_target(apa_causal_dag_plot, apa_plot_causal_dag(causal_dag_nodes_table, causal_dag_edges_table)),
  tar_target(apa_smd_love_plot, apa_plot_smd_love(propensity_balance_before_after_table)),
  tar_target(apa_propensity_overlap_plot, apa_plot_propensity_overlap(df_family_propensity, propensity_overlap_summary_table)),
  tar_target(apa_ses_correlation_plot, apa_plot_ses_correlation(ses_correlation_summary_table)),
  tar_target(apa_h1_three_way_emm_plot, apa_plot_h1_three_way_emm(h1_three_way_emmeans_grid_table)),
  tar_target(apa_mediation_effects_plot, apa_plot_mediation_effects(mediation_simple_effect_table, mediation_multilevel_effect_table, mediation_conditional_effect_table)),
  tar_target(apa_lpa_fit_plot, apa_plot_lpa_fit(lpa_fit_table)),
  tar_target(apa_network_graph_plot, apa_plot_network_graph(network_edges_table, network_centrality_table)),
  tar_target(apa_network_nct_plot, apa_plot_network_nct(network_nct_table)),
  tar_target(apa_clinical_cart_rf_plot, apa_plot_clinical_cart_rf(clinical_cart_cp_table, clinical_rf_importance_table)),
  tar_target(apa_bayesian_forest_plot, apa_plot_bayesian_forest(bayes_h1_posterior_table, bayes_h3_posterior_table)),
  tar_target(apa_bayesian_diagnostics_plot, apa_plot_bayesian_diagnostics(bayes_h1_diagnostics_table, bayes_h3_diagnostics_table)),
  tar_target(
    apa_h1_forest_png,
    save_apa_plot(apa_h1_forest_plot, "outputs/figures/h1_forest.png", width = 8.2, height = 5.1),
    format = "file"
  ),
  tar_target(
    apa_h4_sem_path_png,
    save_apa_plot(apa_h4_sem_path_plot, "outputs/figures/h4_sem_path.png", width = 8.2, height = 5.1),
    format = "file"
  ),
  tar_target(
    apa_h5_ba_grid_png,
    save_apa_plot(apa_h5_bland_altman_plot, "outputs/figures/h5_ba_grid.png", width = 10.5, height = 8.2),
    format = "file"
  ),
  tar_target(
    apa_h5_rsa_surface_png,
    save_apa_plot(apa_h5_rsa_surface_plot, "outputs/figures/h5_rsa_surface.png", width = 10.5, height = 6.4),
    format = "file"
  ),
  tar_target(
    apa_h2_apim_path_png,
    save_apa_plot(apa_h2_apim_path_plot, "outputs/figures/h2_apim_path.png", width = 8.2, height = 5.1),
    format = "file"
  ),
  tar_target(
    apa_h3_stratified_forest_png,
    save_apa_plot(apa_h3_stratified_forest_plot, "outputs/figures/h3_stratified_forest.png", width = 8.2, height = 5.1),
    format = "file"
  ),
  tar_target(
    apa_specification_curve_png,
    save_apa_plot(apa_specification_curve_plot, "outputs/figures/specification_curve.png", width = 8.2, height = 5.4),
    format = "file"
  ),
  tar_target(
    apa_sensemakr_contour_png,
    save_apa_plot(apa_sensemakr_contour_plot, "outputs/figures/sensemakr_contour.png", width = 7.2, height = 5.4),
    format = "file"
  ),
  tar_target(
    apa_clinical_roc_png,
    save_apa_plot(apa_clinical_roc_plot, "outputs/figures/clinical_roc.png", width = 6.4, height = 5.4),
    format = "file"
  ),
  tar_target(
    apa_clinical_dca_png,
    save_apa_plot(apa_clinical_dca_plot, "outputs/figures/clinical_dca.png", width = 7.2, height = 5.2),
    format = "file"
  ),
  tar_target(
    apa_clinical_calibration_png,
    save_apa_plot(apa_clinical_calibration_plot, "outputs/figures/clinical_calibration.png", width = 6.4, height = 5.4),
    format = "file"
  ),
  tar_target(
    apa_strobe_flow_png,
    save_apa_plot(apa_strobe_flow_plot, "outputs/figures/strobe_flow.png", width = 7.2, height = 5.4),
    format = "file"
  ),
  tar_target(
    apa_causal_dag_png,
    save_apa_plot(apa_causal_dag_plot, "outputs/figures/causal_dag.png", width = 9.6, height = 4.8),
    format = "file"
  ),
  tar_target(
    apa_smd_love_png,
    save_apa_plot(apa_smd_love_plot, "outputs/figures/smd_love_plot.png", width = 7.2, height = 4.6),
    format = "file"
  ),
  tar_target(
    apa_propensity_overlap_png,
    save_apa_plot(apa_propensity_overlap_plot, "outputs/figures/propensity_overlap.png", width = 7.2, height = 4.8),
    format = "file"
  ),
  tar_target(
    apa_ses_correlation_png,
    save_apa_plot(apa_ses_correlation_plot, "outputs/figures/ses_correlation_heatmap.png", width = 6.8, height = 5.8),
    format = "file"
  ),
  tar_target(
    apa_h1_three_way_emm_png,
    save_apa_plot(apa_h1_three_way_emm_plot, "outputs/figures/h1_three_way_emm.png", width = 10.2, height = 8.2),
    format = "file"
  ),
  tar_target(
    apa_mediation_effects_png,
    save_apa_plot(apa_mediation_effects_plot, "outputs/figures/mediation_effects.png", width = 8.2, height = 6.6),
    format = "file"
  ),
  tar_target(
    apa_lpa_fit_png,
    save_apa_plot(apa_lpa_fit_plot, "outputs/figures/lpa_fit_indices.png", width = 7.2, height = 6.2),
    format = "file"
  ),
  tar_target(
    apa_network_graph_png,
    save_apa_plot(apa_network_graph_plot, "outputs/figures/network_graph.png", width = 7.4, height = 6.2),
    format = "file"
  ),
  tar_target(
    apa_network_nct_png,
    save_apa_plot(apa_network_nct_plot, "outputs/figures/network_nct.png", width = 6.8, height = 4.4),
    format = "file"
  ),
  tar_target(
    apa_clinical_cart_rf_png,
    save_apa_plot(apa_clinical_cart_rf_plot, "outputs/figures/clinical_cart_rf.png", width = 7.2, height = 6.2),
    format = "file"
  ),
  tar_target(
    apa_bayesian_forest_png,
    save_apa_plot(apa_bayesian_forest_plot, "outputs/figures/bayesian_forest.png", width = 8.2, height = 5.8),
    format = "file"
  ),
  tar_target(
    apa_bayesian_diagnostics_png,
    save_apa_plot(apa_bayesian_diagnostics_plot, "outputs/figures/bayesian_diagnostics.png", width = 7.2, height = 5.2),
    format = "file"
  ),
  tar_target(
    apa_sprint_a_figure_manifest_table,
    apa_figure_manifest(c(
      strobe_flow = apa_strobe_flow_png,
      causal_dag = apa_causal_dag_png,
      smd_love_plot = apa_smd_love_png,
      propensity_overlap = apa_propensity_overlap_png,
      ses_correlation_heatmap = apa_ses_correlation_png,
      h1_forest = apa_h1_forest_png,
      h1_three_way_emm = apa_h1_three_way_emm_png,
      h4_sem_path = apa_h4_sem_path_png,
      h5_ba_grid = apa_h5_ba_grid_png,
      h5_rsa_surface = apa_h5_rsa_surface_png,
      h2_apim_path = apa_h2_apim_path_png,
      h3_stratified_forest = apa_h3_stratified_forest_png,
      specification_curve = apa_specification_curve_png,
      sensemakr_contour = apa_sensemakr_contour_png,
      clinical_roc = apa_clinical_roc_png,
      clinical_dca = apa_clinical_dca_png,
      clinical_calibration = apa_clinical_calibration_png,
      mediation_effects = apa_mediation_effects_png,
      lpa_fit_indices = apa_lpa_fit_png,
      network_graph = apa_network_graph_png,
      network_nct = apa_network_nct_png,
      clinical_cart_rf = apa_clinical_cart_rf_png,
      bayesian_forest = apa_bayesian_forest_png,
      bayesian_diagnostics = apa_bayesian_diagnostics_png
    ))
  ),
  tar_target(
    apa_table_bundle,
    apa_build_table_bundle(
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
  ),
  tar_target(
    apa_sprint_a_table_files,
    save_apa_table_bundle(apa_table_bundle, "outputs/tables"),
    format = "file"
  ),
  tar_target(
    apa_sprint_a_table_manifest_table,
    apa_table_manifest(apa_sprint_a_table_files, apa_table_bundle)
  ),
  tar_target(
    apa_sprint_a_table_manifest_csv,
    save_apa_table_csv(apa_sprint_a_table_manifest_table, "outputs/tables/apa_sprint_a_table_manifest.csv"),
    format = "file"
  ),
  tar_target(thesis_chapter_mapping_table, thesis_chapter_mapping()),
  tar_target(thesis_html_file, "outputs/quarto/thesis.html", format = "file"),
  tar_target(
    thesis_mapping_checks_table,
    thesis_mapping_checks(thesis_chapter_mapping_table, apa_sprint_a_figure_manifest_table, apa_sprint_a_table_manifest_table, thesis_html_file)
  ),
  tar_target(
    thesis_mapping_manifest_table,
    thesis_mapping_manifest(thesis_chapter_mapping_table, thesis_mapping_checks_table)
  ),
  tar_target(
    thesis_mapping_checks_csv,
    save_apa_table_csv(thesis_mapping_checks_table, "outputs/tables/thesis_mapping_checks.csv"),
    format = "file"
  ),
  tar_target(
    thesis_mapping_manifest_csv,
    save_apa_table_csv(thesis_mapping_manifest_table, "outputs/tables/thesis_mapping_manifest.csv"),
    format = "file"
  ),
  tar_target(final_publication_strategy_table, final_publication_strategy()),
  tar_target(final_publication_evidence_map_table, final_publication_evidence_map()),
  tar_target(final_risk_matrix_table, final_risk_matrix()),
  tar_target(final_risk_summary_table, final_risk_summary(final_risk_matrix_table)),
  tar_target(final_timeline_24_week_table, final_timeline_24_week()),
  tar_target(final_timeline_summary_table, final_timeline_summary(final_timeline_24_week_table)),
  tar_target(
    final_planning_manifest_table,
    final_planning_manifest(list(
      publication_strategy = final_publication_strategy_table,
      publication_evidence_map = final_publication_evidence_map_table,
      risk_matrix = final_risk_matrix_table,
      risk_summary = final_risk_summary_table,
      timeline_24_week = final_timeline_24_week_table,
      timeline_summary = final_timeline_summary_table
    ))
  ),
  tar_target(
    final_publication_strategy_csv,
    save_apa_table_csv(final_publication_strategy_table, "outputs/tables/final_plan_publication_strategy.csv"),
    format = "file"
  ),
  tar_target(
    final_publication_evidence_map_csv,
    save_apa_table_csv(final_publication_evidence_map_table, "outputs/tables/final_plan_publication_evidence_map.csv"),
    format = "file"
  ),
  tar_target(
    final_risk_matrix_csv,
    save_apa_table_csv(final_risk_matrix_table, "outputs/tables/final_plan_risk_matrix.csv"),
    format = "file"
  ),
  tar_target(
    final_risk_summary_csv,
    save_apa_table_csv(final_risk_summary_table, "outputs/tables/final_plan_risk_summary.csv"),
    format = "file"
  ),
  tar_target(
    final_timeline_24_week_csv,
    save_apa_table_csv(final_timeline_24_week_table, "outputs/tables/final_plan_timeline_24_week.csv"),
    format = "file"
  ),
  tar_target(
    final_timeline_summary_csv,
    save_apa_table_csv(final_timeline_summary_table, "outputs/tables/final_plan_timeline_summary.csv"),
    format = "file"
  ),
  tar_target(
    final_planning_manifest_csv,
    save_apa_table_csv(final_planning_manifest_table, "outputs/tables/final_plan_manifest.csv"),
    format = "file"
  ),

  # ============================================================================
  # FAZ II POST-HOC ANALIZLERI — [KESIFSEL · POST-HOC]
  # docs/analiz_planlari/STATISTICAL-ANALYSIS-PLAN-PHASE-2.md v1.0
  # docs/analiz_planlari/OSF-LAYER3-AMENDMENT.md
  # PRE-REGISTRATION-DEVIATION-TABLE.md sapma satiri #1 (Tip 3)
  # ============================================================================

  # KISIM XX/50 — Trifactor T-CFA (CT-C(M-1) Eid 2008 / Masse 2020)
  tar_target(
    phase2_trifactor_results,
    run_trifactor_pipeline(
      df_family_scored = df_family_scored,
      df_long_scored = df_long_scored,
      fit_models = TRUE
    )
  ),
  tar_target(phase2_trifactor_coverage_table, phase2_trifactor_results$coverage),
  tar_target(phase2_trifactor_syntax_table, phase2_trifactor_results$syntax),
  tar_target(phase2_trifactor_status_table, phase2_trifactor_results$status),
  tar_target(phase2_trifactor_fit_indices_table, phase2_trifactor_results$fit_indices),
  tar_target(phase2_trifactor_loadings_table, phase2_trifactor_results$loadings),
  tar_target(phase2_trifactor_variance_table, phase2_trifactor_results$variance),
  tar_target(phase2_trifactor_method_correlation_table, phase2_trifactor_results$method_correlation),
  tar_target(phase2_trifactor_target_summary_table, phase2_trifactor_results$target_summary),
  tar_target(
    phase2_trifactor_coverage_csv,
    save_apa_table_csv(phase2_trifactor_coverage_table, "outputs/tables/phase2_trifactor_coverage.csv"),
    format = "file"
  ),
  tar_target(
    phase2_trifactor_status_csv,
    save_apa_table_csv(phase2_trifactor_status_table, "outputs/tables/phase2_trifactor_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_trifactor_fit_indices_csv,
    save_apa_table_csv(phase2_trifactor_fit_indices_table, "outputs/tables/phase2_trifactor_fit_indices.csv"),
    format = "file"
  ),
  tar_target(
    phase2_trifactor_loadings_csv,
    save_apa_table_csv(phase2_trifactor_loadings_table, "outputs/tables/phase2_trifactor_loadings.csv"),
    format = "file"
  ),
  tar_target(
    phase2_trifactor_variance_csv,
    save_apa_table_csv(phase2_trifactor_variance_table, "outputs/tables/phase2_trifactor_variance.csv"),
    format = "file"
  ),
  tar_target(
    phase2_trifactor_method_correlation_csv,
    save_apa_table_csv(phase2_trifactor_method_correlation_table, "outputs/tables/phase2_trifactor_method_correlation.csv"),
    format = "file"
  ),
  tar_target(
    phase2_trifactor_target_summary_csv,
    save_apa_table_csv(phase2_trifactor_target_summary_table, "outputs/tables/phase2_trifactor_target_summary.csv"),
    format = "file"
  ),

  # KISIM XX/51-52 — Latent Informant Discrepancy SEM + LDS
  tar_target(
    phase2_disc_results,
    run_informant_discrepancy_pipeline(
      df_family_ses = df_family_ses,
      df_long_scored = df_long_scored,
      include_predictors = TRUE,
      fit_lds = TRUE
    )
  ),
  tar_target(phase2_disc_coverage_table, phase2_disc_results$coverage),
  tar_target(phase2_disc_scaling_table, phase2_disc_results$scaling),
  tar_target(phase2_disc_status_table, phase2_disc_results$status),
  tar_target(phase2_disc_fit_indices_table, phase2_disc_results$fit_indices),
  tar_target(phase2_disc_latent_correlation_table, phase2_disc_results$latent_correlation),
  tar_target(phase2_disc_variance_table, phase2_disc_results$variance),
  tar_target(phase2_disc_predictor_paths_table, phase2_disc_results$predictor_paths),
  tar_target(phase2_disc_target_summary_table, phase2_disc_results$target_summary),
  tar_target(
    phase2_disc_coverage_csv,
    save_apa_table_csv(phase2_disc_coverage_table, "outputs/tables/phase2_disc_coverage.csv"),
    format = "file"
  ),
  tar_target(
    phase2_disc_status_csv,
    save_apa_table_csv(phase2_disc_status_table, "outputs/tables/phase2_disc_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_disc_fit_indices_csv,
    save_apa_table_csv(phase2_disc_fit_indices_table, "outputs/tables/phase2_disc_fit_indices.csv"),
    format = "file"
  ),
  tar_target(
    phase2_disc_latent_correlation_csv,
    save_apa_table_csv(phase2_disc_latent_correlation_table, "outputs/tables/phase2_disc_latent_correlation.csv"),
    format = "file"
  ),
  tar_target(
    phase2_disc_variance_csv,
    save_apa_table_csv(phase2_disc_variance_table, "outputs/tables/phase2_disc_variance.csv"),
    format = "file"
  ),
  tar_target(
    phase2_disc_predictor_paths_csv,
    save_apa_table_csv(phase2_disc_predictor_paths_table, "outputs/tables/phase2_disc_predictor_paths.csv"),
    format = "file"
  ),
  tar_target(
    phase2_disc_target_summary_csv,
    save_apa_table_csv(phase2_disc_target_summary_table, "outputs/tables/phase2_disc_target_summary.csv"),
    format = "file"
  ),

  # KISIM XX/53 — Cross-Informant GGM
  tar_target(
    phase2_xinfo_results,
    run_cross_informant_network_pipeline(
      df_family_ses = df_family_ses,
      df_long_scored = df_long_scored,
      gamma = 0.5,
      correlation = "spearman",
      group_split = TRUE
    )
  ),
  tar_target(phase2_xinfo_nodes_table, phase2_xinfo_results$nodes),
  tar_target(phase2_xinfo_coverage_table, phase2_xinfo_results$coverage),
  tar_target(phase2_xinfo_status_table, phase2_xinfo_results$status),
  tar_target(phase2_xinfo_edges_table, phase2_xinfo_results$edges),
  tar_target(phase2_xinfo_centrality_table, phase2_xinfo_results$centrality),
  tar_target(phase2_xinfo_summary_table, phase2_xinfo_results$cross_informant_summary),
  tar_target(phase2_xinfo_target_summary_table, phase2_xinfo_results$target_summary),
  tar_target(
    phase2_xinfo_nodes_csv,
    save_apa_table_csv(phase2_xinfo_nodes_table, "outputs/tables/phase2_xinfo_nodes.csv"),
    format = "file"
  ),
  tar_target(
    phase2_xinfo_status_csv,
    save_apa_table_csv(phase2_xinfo_status_table, "outputs/tables/phase2_xinfo_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_xinfo_edges_csv,
    save_apa_table_csv(phase2_xinfo_edges_table, "outputs/tables/phase2_xinfo_edges.csv"),
    format = "file"
  ),
  tar_target(
    phase2_xinfo_centrality_csv,
    save_apa_table_csv(phase2_xinfo_centrality_table, "outputs/tables/phase2_xinfo_centrality.csv"),
    format = "file"
  ),
  tar_target(
    phase2_xinfo_summary_csv,
    save_apa_table_csv(phase2_xinfo_summary_table, "outputs/tables/phase2_xinfo_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_xinfo_target_summary_csv,
    save_apa_table_csv(phase2_xinfo_target_summary_table, "outputs/tables/phase2_xinfo_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXI/54 — Floor-Aware IRT (Tobit motivasyonlu)
  tar_target(
    phase2_floor_irt_results,
    run_floor_aware_irt_pipeline(
      df_family_scored = df_family_scored,
      df_long_scored = df_long_scored,
      subscales = c("reddetme", "asiri_koruma"),
      informants = c("anne", "indeks")
    )
  ),
  tar_target(phase2_floor_irt_floor_summary_table, phase2_floor_irt_results$floor_summary),
  tar_target(phase2_floor_irt_status_table, phase2_floor_irt_results$status),
  tar_target(phase2_floor_irt_item_parameters_table, phase2_floor_irt_results$item_parameters),
  tar_target(phase2_floor_irt_theta_comparison_table, phase2_floor_irt_results$theta_comparison),
  tar_target(phase2_floor_irt_group_delta_table, phase2_floor_irt_results$group_delta),
  tar_target(phase2_floor_irt_target_summary_table, phase2_floor_irt_results$target_summary),
  tar_target(
    phase2_floor_irt_floor_summary_csv,
    save_apa_table_csv(phase2_floor_irt_floor_summary_table, "outputs/tables/phase2_floor_irt_floor_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_floor_irt_status_csv,
    save_apa_table_csv(phase2_floor_irt_status_table, "outputs/tables/phase2_floor_irt_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_floor_irt_item_parameters_csv,
    save_apa_table_csv(phase2_floor_irt_item_parameters_table, "outputs/tables/phase2_floor_irt_item_parameters.csv"),
    format = "file"
  ),
  tar_target(
    phase2_floor_irt_theta_comparison_csv,
    save_apa_table_csv(phase2_floor_irt_theta_comparison_table, "outputs/tables/phase2_floor_irt_theta_comparison.csv"),
    format = "file"
  ),
  tar_target(
    phase2_floor_irt_group_delta_csv,
    save_apa_table_csv(phase2_floor_irt_group_delta_table, "outputs/tables/phase2_floor_irt_group_delta.csv"),
    format = "file"
  ),
  tar_target(
    phase2_floor_irt_target_summary_csv,
    save_apa_table_csv(phase2_floor_irt_target_summary_table, "outputs/tables/phase2_floor_irt_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXI/55-56 — Reliability Generalization (omega_h, ECV) + Beck bifactor
  tar_target(
    phase2_omegah_results,
    run_reliability_generalization_pipeline(
      df_family_scored = df_family_scored,
      df_long_scored = df_long_scored,
      reference_subscale = "asiri_koruma"
    )
  ),
  tar_target(phase2_omegah_status_table, phase2_omegah_results$status),
  tar_target(phase2_omegah_fit_indices_table, phase2_omegah_results$fit_indices),
  tar_target(phase2_omegah_loadings_table, phase2_omegah_results$loadings),
  tar_target(phase2_omegah_metrics_summary_table, phase2_omegah_results$metrics_summary),
  tar_target(phase2_omegah_subscale_metrics_table, phase2_omegah_results$omega_hs),
  tar_target(phase2_omegah_target_summary_table, phase2_omegah_results$target_summary),
  tar_target(
    phase2_omegah_status_csv,
    save_apa_table_csv(phase2_omegah_status_table, "outputs/tables/phase2_omegah_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_omegah_fit_indices_csv,
    save_apa_table_csv(phase2_omegah_fit_indices_table, "outputs/tables/phase2_omegah_fit_indices.csv"),
    format = "file"
  ),
  tar_target(
    phase2_omegah_loadings_csv,
    save_apa_table_csv(phase2_omegah_loadings_table, "outputs/tables/phase2_omegah_loadings.csv"),
    format = "file"
  ),
  tar_target(
    phase2_omegah_metrics_summary_csv,
    save_apa_table_csv(phase2_omegah_metrics_summary_table, "outputs/tables/phase2_omegah_metrics_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_omegah_subscale_metrics_csv,
    save_apa_table_csv(phase2_omegah_subscale_metrics_table, "outputs/tables/phase2_omegah_subscale_metrics.csv"),
    format = "file"
  ),
  tar_target(
    phase2_omegah_target_summary_csv,
    save_apa_table_csv(phase2_omegah_target_summary_table, "outputs/tables/phase2_omegah_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXI/57 — ESEM (Exploratory SEM) EMBU-P/C
  tar_target(
    phase2_esem_results,
    run_esem_embu_pipeline(
      df_family_scored = df_family_scored,
      df_long_scored = df_long_scored,
      n_factors = 4L,
      rotation = "geomin"
    )
  ),
  tar_target(phase2_esem_status_table, phase2_esem_results$status),
  tar_target(phase2_esem_fit_indices_table, phase2_esem_results$fit_indices),
  tar_target(phase2_esem_loadings_table, phase2_esem_results$loadings),
  tar_target(phase2_esem_cross_loading_summary_table, phase2_esem_results$cross_loading_summary),
  tar_target(phase2_esem_target_summary_table, phase2_esem_results$target_summary),
  tar_target(
    phase2_esem_status_csv,
    save_apa_table_csv(phase2_esem_status_table, "outputs/tables/phase2_esem_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_esem_fit_indices_csv,
    save_apa_table_csv(phase2_esem_fit_indices_table, "outputs/tables/phase2_esem_fit_indices.csv"),
    format = "file"
  ),
  tar_target(
    phase2_esem_loadings_csv,
    save_apa_table_csv(phase2_esem_loadings_table, "outputs/tables/phase2_esem_loadings.csv"),
    format = "file"
  ),
  tar_target(
    phase2_esem_cross_loading_summary_csv,
    save_apa_table_csv(phase2_esem_cross_loading_summary_table, "outputs/tables/phase2_esem_cross_loading_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_esem_target_summary_csv,
    save_apa_table_csv(phase2_esem_target_summary_table, "outputs/tables/phase2_esem_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXII/58-60 — Antidepresan kullanim hatti (mediator + moderator + Beck x AD)
  tar_target(
    phase2_ad_results,
    run_ad_pathway_pipeline(
      df_family_ses = df_family_ses,
      df_long_scored = df_long_scored,
      bootstrap_n = 1000L
    )
  ),
  tar_target(phase2_ad_family_summary_table, phase2_ad_results$family_summary),
  tar_target(phase2_ad_mediator_status_table, phase2_ad_results$mediator_status),
  tar_target(phase2_ad_mediator_estimates_table, phase2_ad_results$mediator_estimates),
  tar_target(phase2_ad_mediator_sensitivity_table, phase2_ad_results$mediator_sensitivity),
  tar_target(phase2_ad_moderation_h1_status_table, phase2_ad_results$moderation_h1_status),
  tar_target(phase2_ad_moderation_h1_fixed_effects_table, phase2_ad_results$moderation_h1_fixed_effects),
  tar_target(phase2_ad_moderation_h4_status_table, phase2_ad_results$moderation_h4_status),
  tar_target(phase2_ad_moderation_h4_fixed_effects_table, phase2_ad_results$moderation_h4_fixed_effects),
  tar_target(phase2_ad_moderation_h5_stratified_table,
    phase2_ad_results$moderation_h5_stratified_correlations),
  tar_target(phase2_ad_beck_interaction_status_table, phase2_ad_results$beck_interaction_status),
  tar_target(phase2_ad_beck_interaction_fixed_effects_table,
    phase2_ad_results$beck_interaction_fixed_effects),
  tar_target(phase2_ad_target_summary_table, phase2_ad_results$target_summary),
  tar_target(
    phase2_ad_family_summary_csv,
    save_apa_table_csv(phase2_ad_family_summary_table, "outputs/tables/phase2_ad_family_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_mediator_status_csv,
    save_apa_table_csv(phase2_ad_mediator_status_table, "outputs/tables/phase2_ad_mediator_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_mediator_estimates_csv,
    save_apa_table_csv(phase2_ad_mediator_estimates_table, "outputs/tables/phase2_ad_mediator_estimates.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_mediator_sensitivity_csv,
    save_apa_table_csv(phase2_ad_mediator_sensitivity_table, "outputs/tables/phase2_ad_mediator_sensitivity.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_moderation_h1_status_csv,
    save_apa_table_csv(phase2_ad_moderation_h1_status_table, "outputs/tables/phase2_ad_moderation_h1_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_moderation_h1_fixed_effects_csv,
    save_apa_table_csv(phase2_ad_moderation_h1_fixed_effects_table,
      "outputs/tables/phase2_ad_moderation_h1_fixed_effects.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_moderation_h4_status_csv,
    save_apa_table_csv(phase2_ad_moderation_h4_status_table, "outputs/tables/phase2_ad_moderation_h4_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_moderation_h4_fixed_effects_csv,
    save_apa_table_csv(phase2_ad_moderation_h4_fixed_effects_table,
      "outputs/tables/phase2_ad_moderation_h4_fixed_effects.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_moderation_h5_stratified_csv,
    save_apa_table_csv(phase2_ad_moderation_h5_stratified_table,
      "outputs/tables/phase2_ad_moderation_h5_stratified.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_beck_interaction_status_csv,
    save_apa_table_csv(phase2_ad_beck_interaction_status_table,
      "outputs/tables/phase2_ad_beck_interaction_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_beck_interaction_fixed_effects_csv,
    save_apa_table_csv(phase2_ad_beck_interaction_fixed_effects_table,
      "outputs/tables/phase2_ad_beck_interaction_fixed_effects.csv"),
    format = "file"
  ),
  tar_target(
    phase2_ad_target_summary_csv,
    save_apa_table_csv(phase2_ad_target_summary_table, "outputs/tables/phase2_ad_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXIII/61-64 — H5 Diadik Tutarlilik Genisletmesi
  tar_target(
    phase2_h5ext_results,
    run_h5_extensions_pipeline(
      df_family_ses = df_family_ses,
      df_long_scored = df_long_scored,
      df_family_scored = df_family_scored,
      bootstrap_n = 1000L,
      brms_chains = 2L,
      brms_iter = 2000L,
      run_mtmm = TRUE,
      run_pooling = TRUE
    )
  ),
  tar_target(phase2_h5ext_mtmm_status_table, phase2_h5ext_results$mtmm_status),
  tar_target(phase2_h5ext_mtmm_fit_indices_table, phase2_h5ext_results$mtmm_fit_indices),
  tar_target(phase2_h5ext_mtmm_variance_table, phase2_h5ext_results$mtmm_variance),
  tar_target(phase2_h5ext_beck_moderation_status_table,
    phase2_h5ext_results$beck_moderation_status),
  tar_target(phase2_h5ext_beck_moderation_coefficients_table,
    phase2_h5ext_results$beck_moderation_coefficients),
  tar_target(phase2_h5ext_beck_moderation_bootstrap_ci_table,
    phase2_h5ext_results$beck_moderation_bootstrap_ci),
  tar_target(phase2_h5ext_sibling_icc_table, phase2_h5ext_results$sibling_icc),
  tar_target(phase2_h5ext_strategy_estimates_table, phase2_h5ext_results$strategy_estimates),
  tar_target(phase2_h5ext_strategy_pooled_table, phase2_h5ext_results$strategy_pooled_summary),
  tar_target(phase2_h5ext_target_summary_table, phase2_h5ext_results$target_summary),
  tar_target(
    phase2_h5ext_mtmm_status_csv,
    save_apa_table_csv(phase2_h5ext_mtmm_status_table,
      "outputs/tables/phase2_h5ext_mtmm_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_h5ext_mtmm_fit_indices_csv,
    save_apa_table_csv(phase2_h5ext_mtmm_fit_indices_table,
      "outputs/tables/phase2_h5ext_mtmm_fit_indices.csv"),
    format = "file"
  ),
  tar_target(
    phase2_h5ext_mtmm_variance_csv,
    save_apa_table_csv(phase2_h5ext_mtmm_variance_table,
      "outputs/tables/phase2_h5ext_mtmm_variance.csv"),
    format = "file"
  ),
  tar_target(
    phase2_h5ext_beck_moderation_status_csv,
    save_apa_table_csv(phase2_h5ext_beck_moderation_status_table,
      "outputs/tables/phase2_h5ext_beck_moderation_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_h5ext_beck_moderation_coefficients_csv,
    save_apa_table_csv(phase2_h5ext_beck_moderation_coefficients_table,
      "outputs/tables/phase2_h5ext_beck_moderation_coefficients.csv"),
    format = "file"
  ),
  tar_target(
    phase2_h5ext_beck_moderation_bootstrap_ci_csv,
    save_apa_table_csv(phase2_h5ext_beck_moderation_bootstrap_ci_table,
      "outputs/tables/phase2_h5ext_beck_moderation_bootstrap_ci.csv"),
    format = "file"
  ),
  tar_target(
    phase2_h5ext_sibling_icc_csv,
    save_apa_table_csv(phase2_h5ext_sibling_icc_table,
      "outputs/tables/phase2_h5ext_sibling_icc.csv"),
    format = "file"
  ),
  tar_target(
    phase2_h5ext_strategy_estimates_csv,
    save_apa_table_csv(phase2_h5ext_strategy_estimates_table,
      "outputs/tables/phase2_h5ext_strategy_estimates.csv"),
    format = "file"
  ),
  tar_target(
    phase2_h5ext_strategy_pooled_csv,
    save_apa_table_csv(phase2_h5ext_strategy_pooled_table,
      "outputs/tables/phase2_h5ext_strategy_pooled.csv"),
    format = "file"
  ),
  tar_target(
    phase2_h5ext_target_summary_csv,
    save_apa_table_csv(phase2_h5ext_target_summary_table,
      "outputs/tables/phase2_h5ext_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXIV/65, 66, 68 — HbA1c klinik stratifikasyon (DM-only)
  tar_target(
    phase2_hba1c_results,
    run_hba1c_joint_pipeline(
      df_family_ses = hba1c_ensure_group_dm(df_family_ses),
      brms_chains = 2L,
      brms_iter = 2000L,
      run_bayesian = TRUE,
      df_spline = 3L
    )
  ),
  tar_target(phase2_hba1c_dm_summary_table, phase2_hba1c_results$dm_summary),
  tar_target(phase2_hba1c_bayesian_status_table, phase2_hba1c_results$bayesian_status),
  tar_target(phase2_hba1c_bayesian_posterior_table, phase2_hba1c_results$bayesian_posterior),
  tar_target(phase2_hba1c_spline_table, phase2_hba1c_results$spline_table),
  tar_target(phase2_hba1c_ispad_table, phase2_hba1c_results$ispad_table),
  tar_target(phase2_hba1c_target_summary_table, phase2_hba1c_results$target_summary),
  tar_target(
    phase2_hba1c_dm_summary_csv,
    save_apa_table_csv(phase2_hba1c_dm_summary_table,
      "outputs/tables/phase2_hba1c_dm_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_hba1c_bayesian_status_csv,
    save_apa_table_csv(phase2_hba1c_bayesian_status_table,
      "outputs/tables/phase2_hba1c_bayesian_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_hba1c_bayesian_posterior_csv,
    save_apa_table_csv(phase2_hba1c_bayesian_posterior_table,
      "outputs/tables/phase2_hba1c_bayesian_posterior.csv"),
    format = "file"
  ),
  tar_target(
    phase2_hba1c_spline_csv,
    save_apa_table_csv(phase2_hba1c_spline_table,
      "outputs/tables/phase2_hba1c_spline.csv"),
    format = "file"
  ),
  tar_target(
    phase2_hba1c_ispad_csv,
    save_apa_table_csv(phase2_hba1c_ispad_table,
      "outputs/tables/phase2_hba1c_ispad_logistic.csv"),
    format = "file"
  ),
  tar_target(
    phase2_hba1c_target_summary_csv,
    save_apa_table_csv(phase2_hba1c_target_summary_table,
      "outputs/tables/phase2_hba1c_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXV/69, 71 — Imai-Keele sensitivity + c' triangulation
  tar_target(
    phase2_imai_results,
    run_causal_mediation_pipeline(
      df_family_ses = df_family_ses,
      df_long_scored = df_long_scored
    )
  ),
  tar_target(phase2_imai_status_table, phase2_imai_results$imai_status),
  tar_target(phase2_imai_summary_table, phase2_imai_results$imai_summary),
  tar_target(phase2_imai_sensitivity_grid_table,
    phase2_imai_results$imai_sensitivity_grid),
  tar_target(phase2_cprime_triangulation_table,
    phase2_imai_results$cprime_triangulation),
  tar_target(phase2_imai_target_summary_table,
    phase2_imai_results$target_summary),
  tar_target(
    phase2_imai_status_csv,
    save_apa_table_csv(phase2_imai_status_table,
      "outputs/tables/phase2_imai_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_imai_summary_csv,
    save_apa_table_csv(phase2_imai_summary_table,
      "outputs/tables/phase2_imai_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_imai_sensitivity_grid_csv,
    save_apa_table_csv(phase2_imai_sensitivity_grid_table,
      "outputs/tables/phase2_imai_sensitivity_grid.csv"),
    format = "file"
  ),
  tar_target(
    phase2_cprime_triangulation_csv,
    save_apa_table_csv(phase2_cprime_triangulation_table,
      "outputs/tables/phase2_cprime_triangulation.csv"),
    format = "file"
  ),
  tar_target(
    phase2_imai_target_summary_csv,
    save_apa_table_csv(phase2_imai_target_summary_table,
      "outputs/tables/phase2_imai_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXV/70, 72 — DAG CI tests + 3-level varyans
  tar_target(
    phase2_dag_results,
    run_dag_pc_fci_pipeline(
      df_family_ses = dag_ensure_group_dm(df_family_ses),
      df_long_scored = df_long_scored
    )
  ),
  tar_target(phase2_dag_implied_ci_table,
    phase2_dag_results$implied_conditional_independencies),
  tar_target(phase2_dag_ci_tests_table, phase2_dag_results$ci_test_results),
  tar_target(phase2_dag_three_level_table, phase2_dag_results$three_level_table),
  tar_target(phase2_dag_target_summary_table, phase2_dag_results$target_summary),
  tar_target(
    phase2_dag_implied_ci_csv,
    save_apa_table_csv(phase2_dag_implied_ci_table,
      "outputs/tables/phase2_dag_implied_ci.csv"),
    format = "file"
  ),
  tar_target(
    phase2_dag_ci_tests_csv,
    save_apa_table_csv(phase2_dag_ci_tests_table,
      "outputs/tables/phase2_dag_ci_tests.csv"),
    format = "file"
  ),
  tar_target(
    phase2_dag_three_level_csv,
    save_apa_table_csv(phase2_dag_three_level_table,
      "outputs/tables/phase2_dag_three_level.csv"),
    format = "file"
  ),
  tar_target(
    phase2_dag_target_summary_csv,
    save_apa_table_csv(phase2_dag_target_summary_table,
      "outputs/tables/phase2_dag_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXVI/73, 74, 75 — Distribusyonel + kuantil yaklasimlar
  tar_target(
    phase2_dist_results,
    run_distributional_pipeline(
      df_family_ses = dist_ensure_group_dm(df_family_ses),
      df_long_scored = df_long_scored,
      taus = c(0.50, 0.75, 0.90),
      bootstrap_R = 5000L,
      run_distributional = TRUE,
      brms_chains = 2L,
      brms_iter = 2000L
    )
  ),
  tar_target(phase2_dist_quantile_table, phase2_dist_results$quantile_table),
  tar_target(phase2_dist_distributional_status_table,
    phase2_dist_results$distributional_status),
  tar_target(phase2_dist_distributional_posterior_table,
    phase2_dist_results$distributional_posterior),
  tar_target(phase2_dist_beta_table, phase2_dist_results$beta_table),
  tar_target(phase2_dist_target_summary_table, phase2_dist_results$target_summary),
  tar_target(
    phase2_dist_quantile_csv,
    save_apa_table_csv(phase2_dist_quantile_table,
      "outputs/tables/phase2_dist_quantile.csv"),
    format = "file"
  ),
  tar_target(
    phase2_dist_distributional_status_csv,
    save_apa_table_csv(phase2_dist_distributional_status_table,
      "outputs/tables/phase2_dist_distributional_status.csv"),
    format = "file"
  ),
  tar_target(
    phase2_dist_distributional_posterior_csv,
    save_apa_table_csv(phase2_dist_distributional_posterior_table,
      "outputs/tables/phase2_dist_distributional_posterior.csv"),
    format = "file"
  ),
  tar_target(
    phase2_dist_beta_csv,
    save_apa_table_csv(phase2_dist_beta_table,
      "outputs/tables/phase2_dist_beta.csv"),
    format = "file"
  ),
  tar_target(
    phase2_dist_target_summary_csv,
    save_apa_table_csv(phase2_dist_target_summary_table,
      "outputs/tables/phase2_dist_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXVII/76, 77, 78, 79 — Multiverse genisletme
  tar_target(
    phase2_multi_results,
    run_multiverse_pipeline(
      df_family_ses = multi_ensure_group_dm(df_family_ses),
      df_long_scored = df_long_scored,
      df_family_scored = multi_ensure_group_dm(df_family_scored),
      h1_n_spec = 120L,
      h4_n_spec = 16L,
      n_perm = 5000L
    )
  ),
  tar_target(phase2_multi_h1_spec_grid_table, phase2_multi_results$h1_spec_grid),
  tar_target(phase2_multi_h1_spec_results_table, phase2_multi_results$h1_spec_results),
  tar_target(phase2_multi_h1_curve_summary_table, phase2_multi_results$h1_curve_summary),
  tar_target(phase2_multi_h4_spec_results_table, phase2_multi_results$h4_spec_results),
  tar_target(phase2_multi_h4_summary_table, phase2_multi_results$h4_summary),
  tar_target(phase2_multi_bma_table, phase2_multi_results$bma),
  tar_target(phase2_multi_sca_inferential_table, phase2_multi_results$sca_inferential),
  tar_target(phase2_multi_target_summary_table, phase2_multi_results$target_summary),
  tar_target(
    phase2_multi_h1_spec_grid_csv,
    save_apa_table_csv(phase2_multi_h1_spec_grid_table,
      "outputs/tables/phase2_multi_h1_spec_grid.csv"),
    format = "file"
  ),
  tar_target(
    phase2_multi_h1_spec_results_csv,
    save_apa_table_csv(phase2_multi_h1_spec_results_table,
      "outputs/tables/phase2_multi_h1_spec_results.csv"),
    format = "file"
  ),
  tar_target(
    phase2_multi_h1_curve_summary_csv,
    save_apa_table_csv(phase2_multi_h1_curve_summary_table,
      "outputs/tables/phase2_multi_h1_curve_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_multi_h4_spec_results_csv,
    save_apa_table_csv(phase2_multi_h4_spec_results_table,
      "outputs/tables/phase2_multi_h4_spec_results.csv"),
    format = "file"
  ),
  tar_target(
    phase2_multi_h4_summary_csv,
    save_apa_table_csv(phase2_multi_h4_summary_table,
      "outputs/tables/phase2_multi_h4_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_multi_bma_csv,
    save_apa_table_csv(phase2_multi_bma_table,
      "outputs/tables/phase2_multi_bma.csv"),
    format = "file"
  ),
  tar_target(
    phase2_multi_sca_inferential_csv,
    save_apa_table_csv(phase2_multi_sca_inferential_table,
      "outputs/tables/phase2_multi_sca_inferential.csv"),
    format = "file"
  ),
  tar_target(
    phase2_multi_target_summary_csv,
    save_apa_table_csv(phase2_multi_target_summary_table,
      "outputs/tables/phase2_multi_target_summary.csv"),
    format = "file"
  ),

  # KISIM XXVIII/80, 81, 82 — Bayesian meta-pooling + PPC + EB shrinkage
  tar_target(
    phase2_meta_results,
    run_bayesian_meta_pipeline(
      df_family_ses = meta_ensure_group_dm(df_family_ses),
      df_long_scored = df_long_scored,
      outcomes = c("reddetme", "asiri_koruma", "sicaklik", "karsilastirma"),
      brms_chains = 2L,
      brms_iter = 2000L,
      ppc_replicates = 1000L
    )
  ),
  tar_target(phase2_meta_combined_studies_table, phase2_meta_results$combined_studies),
  tar_target(phase2_meta_pooling_summary_table, phase2_meta_results$pooling_summary),
  tar_target(phase2_meta_pooling_shrunk_table, phase2_meta_results$pooling_shrunk_estimates),
  tar_target(phase2_meta_ppc_summary_table, phase2_meta_results$ppc_summary),
  tar_target(phase2_meta_eb_shrunk_table, phase2_meta_results$eb_shrunk_estimates),
  tar_target(phase2_meta_eb_outlier_summary_table, phase2_meta_results$eb_outlier_summary),
  tar_target(phase2_meta_target_summary_table, phase2_meta_results$target_summary),
  tar_target(
    phase2_meta_combined_studies_csv,
    save_apa_table_csv(phase2_meta_combined_studies_table,
      "outputs/tables/phase2_meta_combined_studies.csv"),
    format = "file"
  ),
  tar_target(
    phase2_meta_pooling_summary_csv,
    save_apa_table_csv(phase2_meta_pooling_summary_table,
      "outputs/tables/phase2_meta_pooling_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_meta_pooling_shrunk_csv,
    save_apa_table_csv(phase2_meta_pooling_shrunk_table,
      "outputs/tables/phase2_meta_pooling_shrunk.csv"),
    format = "file"
  ),
  tar_target(
    phase2_meta_ppc_summary_csv,
    save_apa_table_csv(phase2_meta_ppc_summary_table,
      "outputs/tables/phase2_meta_ppc_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_meta_eb_shrunk_csv,
    save_apa_table_csv(phase2_meta_eb_shrunk_table,
      "outputs/tables/phase2_meta_eb_shrunk.csv"),
    format = "file"
  ),
  tar_target(
    phase2_meta_eb_outlier_summary_csv,
    save_apa_table_csv(phase2_meta_eb_outlier_summary_table,
      "outputs/tables/phase2_meta_eb_outlier_summary.csv"),
    format = "file"
  ),
  tar_target(
    phase2_meta_target_summary_csv,
    save_apa_table_csv(phase2_meta_target_summary_table,
      "outputs/tables/phase2_meta_target_summary.csv"),
    format = "file"
  )
)
