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
  tar_target(h5_target_summary,                 h5_dyadic_concordance_results$target_summary)
)
