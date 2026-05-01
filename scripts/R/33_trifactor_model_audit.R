# [KESIFSEL - POST-HOC] Faz II SAP KISIM XX/50 audit runner
#
# Trifactor T-CFA — kanonik veri uzerinde 4 EMBU alt olcegi icin Eid 2008
# CT-C(M-1) varyantli T-CFA fit eder; coverage, fit indices, loadings,
# variance decomposition ve method correlation tablolarini outputs/tables/
# altinda CSV olarak yazar.
#
# Calistirma: Rscript scripts/R/33_trifactor_model_audit.R

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/32_trifactor_model.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)

result <- run_trifactor_pipeline(
  df_family_scored = df_family_scored,
  df_long_scored = df_long_scored,
  fit_models = TRUE
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

write_audit_csv <- function(df, path) {
  if (is.null(df) || nrow(df) == 0L) {
    stub <- data.frame(
      note = "empty result; see status/coverage tables for diagnostic context",
      stringsAsFactors = FALSE
    )
    utils::write.csv(stub, path, row.names = FALSE, fileEncoding = "UTF-8")
  } else {
    utils::write.csv(df, path, row.names = FALSE, fileEncoding = "UTF-8")
  }
}

write_audit_csv(result$coverage, "outputs/tables/phase2_trifactor_coverage.csv")
write_audit_csv(result$syntax, "outputs/tables/phase2_trifactor_syntax.csv")
write_audit_csv(result$status, "outputs/tables/phase2_trifactor_status.csv")
write_audit_csv(result$fit_indices, "outputs/tables/phase2_trifactor_fit_indices.csv")
write_audit_csv(result$loadings, "outputs/tables/phase2_trifactor_loadings.csv")
write_audit_csv(result$variance, "outputs/tables/phase2_trifactor_variance.csv")
write_audit_csv(result$method_correlation, "outputs/tables/phase2_trifactor_method_correlation.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_trifactor_target_summary.csv")

if (!is.null(result$status) && nrow(result$status) > 0L) {
  cat(sprintf(
    "[Faz II/KISIM XX/50] Trifactor audit tamam: %d/%d alt olcek yakinsadi\n",
    sum(result$status$converged, na.rm = TRUE),
    nrow(result$status)
  ))
} else {
  cat("[Faz II/KISIM XX/50] Trifactor audit tamam: status yok (fit_models=FALSE)\n")
}

invisible(result)
