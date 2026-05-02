# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXIX/83-86 audit runner

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/46_clinical_dx_extension.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data
df_family_ses <- cdx_ensure_group_dm(df_family_ses)

result <- run_clinical_dx_extension_pipeline(
  df_family_ses = df_family_ses,
  thresholds = seq(0.05, 0.50, by = 0.05),
  cost_ratios = seq(1, 10, by = 1),
  high_risk_threshold = cdx_high_risk_threshold
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

write_audit_csv(result$prepared_summary, "outputs/tables/phase2_clinical_prepared_summary.csv")
write_audit_csv(result$fit_summary, "outputs/tables/phase2_clinical_fit_summary.csv")
write_audit_csv(result$snb_table, "outputs/tables/phase2_clinical_snb.csv")
write_audit_csv(result$dca_heatmap, "outputs/tables/phase2_clinical_dca_heatmap.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_clinical_target_summary.csv")

if (!is.null(result$prepared_summary)) {
  cat(sprintf("[Faz II/KISIM XXIX] DM-Kontrol prepared: n=%d, high_risk=%d (%.1f%%)\n",
    result$prepared_summary$n_total,
    result$prepared_summary$n_high_risk,
    100 * result$prepared_summary$high_risk_prevalence))
}
if (!is.null(result$fit_summary)) {
  cat(sprintf("[Faz II/KISIM XXIX] Risk model fit: baseline AUC=%.3f, extended AUC=%.3f\n",
    result$fit_summary$auc[1L], result$fit_summary$auc[2L]))
}
if (!is.null(result$snb_table)) {
  cat(sprintf("[Faz II/KISIM XXIX/84] sNB: %d satir (2 model x %d threshold)\n",
    nrow(result$snb_table),
    nrow(result$snb_table) / 2L))
}
if (!is.null(result$dca_heatmap)) {
  cat(sprintf("[Faz II/KISIM XXIX/85] DCA heatmap: %d satir\n",
    nrow(result$dca_heatmap)))
}

invisible(result)
