# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXV/69, 71 audit runner

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/41_causal_mediation.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data
df_family_ses <- cmed_ensure_group_dm(df_family_ses)

result <- run_causal_mediation_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored
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

write_audit_csv(result$imai_status, "outputs/tables/phase2_imai_status.csv")
write_audit_csv(result$imai_summary, "outputs/tables/phase2_imai_summary.csv")
write_audit_csv(result$imai_sensitivity_grid, "outputs/tables/phase2_imai_sensitivity_grid.csv")
write_audit_csv(result$cprime_triangulation, "outputs/tables/phase2_cprime_triangulation.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_imai_target_summary.csv")

if (!is.null(result$imai_status)) {
  cat(sprintf("[Faz II/KISIM XXV/69] Imai-Keele sensitivity: %d/%d outcome (n_paired=%d)\n",
    sum(result$imai_status$status == "ok", na.rm = TRUE),
    nrow(result$imai_status), result$n_paired))
}
if (!is.null(result$cprime_triangulation)) {
  cat(sprintf("[Faz II/KISIM XXV/71] c' direct triangulation: %d satir (3 model x 4 outcome)\n",
    nrow(result$cprime_triangulation)))
}

invisible(result)
