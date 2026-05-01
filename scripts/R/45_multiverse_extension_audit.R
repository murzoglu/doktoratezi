# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXVII/76, 77, 78, 79 audit runner
#
# H1 multiverse: 120 random spec; H4 SEM multiverse: 16 spec; BMA;
# SCA inferential: n_perm = 5000.

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/44_multiverse_extension.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data
df_family_ses <- multi_ensure_group_dm(df_family_ses)
df_family_scored <- multi_ensure_group_dm(df_family_scored)

# Family scored datada beck_total da olmali (df_family_ses'tan tasi)
if (!"beck_total" %in% names(df_family_scored) && "beck_total" %in% names(df_family_ses)) {
  df_family_scored$beck_total <- df_family_ses$beck_total[
    match(df_family_scored$aile_no, df_family_ses$aile_no)
  ]
}

result <- run_multiverse_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  df_family_scored = df_family_scored,
  h1_n_spec = 120L,
  h4_n_spec = 16L,
  n_perm = 5000L
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write_audit_csv <- function(df, path) {
  if (is.null(df) || nrow(df) == 0L) {
    stub <- data.frame(note = "empty result", stringsAsFactors = FALSE)
    utils::write.csv(stub, path, row.names = FALSE, fileEncoding = "UTF-8")
  } else {
    utils::write.csv(df, path, row.names = FALSE, fileEncoding = "UTF-8")
  }
}

write_audit_csv(result$h1_spec_grid, "outputs/tables/phase2_multi_h1_spec_grid.csv")
write_audit_csv(result$h1_spec_results, "outputs/tables/phase2_multi_h1_spec_results.csv")
write_audit_csv(result$h1_curve_summary, "outputs/tables/phase2_multi_h1_curve_summary.csv")
write_audit_csv(result$h4_spec_results, "outputs/tables/phase2_multi_h4_spec_results.csv")
write_audit_csv(result$h4_summary, "outputs/tables/phase2_multi_h4_summary.csv")
write_audit_csv(result$bma, "outputs/tables/phase2_multi_bma.csv")
write_audit_csv(result$sca_inferential, "outputs/tables/phase2_multi_sca_inferential.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_multi_target_summary.csv")

if (!is.null(result$h1_curve_summary)) {
  cat(sprintf("[Faz II/KISIM XXVII/76] H1 multiverse: %d/%d ok spec, median=%.3f, share_p<.05=%.2f\n",
    result$h1_curve_summary$n_ok_spec,
    result$h1_curve_summary$n_total_spec,
    result$h1_curve_summary$median_estimate,
    result$h1_curve_summary$share_p_under_05))
}
if (!is.null(result$h4_summary)) {
  cat(sprintf("[Faz II/KISIM XXVII/77] H4 SEM multiverse: %d/%d ok spec, median_a=%.3f\n",
    result$h4_summary$n_ok_spec,
    result$h4_summary$n_total_spec,
    result$h4_summary$median_a))
}
if (!is.null(result$bma)) {
  cat(sprintf("[Faz II/KISIM XXVII/78] BMA: H1 pooled=%.3f, H4 pooled=%.3f\n",
    result$bma$bma_pooled[result$bma$family == "H1"],
    result$bma$bma_pooled[result$bma$family == "H4"]))
}
if (!is.null(result$sca_inferential)) {
  cat(sprintf("[Faz II/KISIM XXVII/79] SCA inferential perm p = %.4f (observed t = %.3f, n_perm=%d)\n",
    result$sca_inferential$perm_p_value,
    result$sca_inferential$observed_test_stat,
    result$sca_inferential$n_perm))
}

invisible(result)
