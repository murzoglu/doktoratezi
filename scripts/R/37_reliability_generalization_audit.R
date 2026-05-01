# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXI/55-56 audit runner
#
# Bifactor S-1 (Eid 2017) modeli ile EMBU-P, EMBU-C ve Beck (cognitive vs
# somatic) icin omega_h, omega_h_s, ECV ve PUC metrikleri.
# Cikti: outputs/tables/phase2_omegah_*.csv
#
# Calistirma: Rscript scripts/R/37_reliability_generalization_audit.R

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/36_reliability_generalization.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)

result <- run_reliability_generalization_pipeline(
  df_family_scored = df_family_scored,
  df_long_scored = df_long_scored,
  reference_subscale = "asiri_koruma"
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

write_audit_csv(result$status, "outputs/tables/phase2_omegah_status.csv")
write_audit_csv(result$fit_indices, "outputs/tables/phase2_omegah_fit_indices.csv")
write_audit_csv(result$loadings, "outputs/tables/phase2_omegah_loadings.csv")
write_audit_csv(result$metrics_summary, "outputs/tables/phase2_omegah_metrics_summary.csv")
write_audit_csv(result$omega_hs, "outputs/tables/phase2_omegah_subscale_metrics.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_omegah_target_summary.csv")

if (!is.null(result$status) && nrow(result$status) > 0L) {
  cat(sprintf(
    "[Faz II/KISIM XXI/55-56] Reliability generalization audit: %d/%d domain yakinsadi\n",
    sum(result$status$status == "ok", na.rm = TRUE),
    nrow(result$status)
  ))
}

invisible(result)
