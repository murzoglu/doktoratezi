# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXVIII/80, 81, 82 audit runner

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/45_bayesian_meta.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data
df_family_ses <- meta_ensure_group_dm(df_family_ses)

result <- run_bayesian_meta_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  outcomes = c("reddetme", "asiri_koruma", "sicaklik", "karsilastirma"),
  brms_chains = 2L,
  brms_iter = 2000L,
  ppc_replicates = 1000L
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

write_audit_csv(result$combined_studies, "outputs/tables/phase2_meta_combined_studies.csv")
write_audit_csv(result$pooling_status, "outputs/tables/phase2_meta_pooling_status.csv")
write_audit_csv(result$pooling_summary, "outputs/tables/phase2_meta_pooling_summary.csv")
write_audit_csv(result$pooling_shrunk_estimates,
  "outputs/tables/phase2_meta_pooling_shrunk.csv")
write_audit_csv(result$ppc_summary, "outputs/tables/phase2_meta_ppc_summary.csv")
write_audit_csv(result$eb_shrunk_estimates,
  "outputs/tables/phase2_meta_eb_shrunk.csv")
write_audit_csv(result$eb_outlier_summary,
  "outputs/tables/phase2_meta_eb_outlier_summary.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_meta_target_summary.csv")

if (!is.null(result$pooling_summary)) {
  cat(sprintf("[Faz II/KISIM XXVIII/80] Bayesian meta-pooling: pooled=%.3f [%.3f, %.3f], tau=%.3f, n_studies=%d\n",
    result$pooling_summary$pooled_mean,
    result$pooling_summary$pooled_lower,
    result$pooling_summary$pooled_upper,
    result$pooling_summary$tau,
    result$pooling_summary$n_studies))
}
if (!is.null(result$ppc_summary)) {
  cat(sprintf("[Faz II/KISIM XXVIII/81] PPC replication: %d outcome (consistent / violation)\n",
    nrow(result$ppc_summary)))
  for (i in seq_len(nrow(result$ppc_summary))) {
    cat(sprintf("  %s: observed_t=%.3f, ppc_quantile=%.3f, decision=%s\n",
      result$ppc_summary$outcome_subscale[i],
      result$ppc_summary$observed_t[i],
      result$ppc_summary$ppc_quantile[i],
      result$ppc_summary$ppc_decision[i]))
  }
}
if (!is.null(result$eb_outlier_summary)) {
  cat(sprintf("[Faz II/KISIM XXVIII/82] EB shrinkage: %d outcome\n",
    nrow(result$eb_outlier_summary)))
  for (i in seq_len(nrow(result$eb_outlier_summary))) {
    cat(sprintf("  %s: outliers=%d/%d (DM=%d, Kontrol=%d), decision=%s\n",
      result$eb_outlier_summary$outcome_subscale[i],
      result$eb_outlier_summary$n_outliers_total[i],
      result$eb_outlier_summary$n_total_families[i],
      result$eb_outlier_summary$n_outliers_dm[i],
      result$eb_outlier_summary$n_outliers_kontrol[i],
      result$eb_outlier_summary$decision[i]))
  }
}

invisible(result)
