# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXIV/65, 66, 68 audit runner

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/40_hba1c_joint.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data
df_family_ses <- hba1c_ensure_group_dm(df_family_ses)

result <- run_hba1c_joint_pipeline(
  df_family_ses = df_family_ses,
  brms_chains = 2L,
  brms_iter = 2000L,
  run_bayesian = TRUE,
  df_spline = 3L
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

write_audit_csv(result$dm_summary, "outputs/tables/phase2_hba1c_dm_summary.csv")
write_audit_csv(result$bayesian_status, "outputs/tables/phase2_hba1c_bayesian_status.csv")
write_audit_csv(result$bayesian_posterior, "outputs/tables/phase2_hba1c_bayesian_posterior.csv")
write_audit_csv(result$spline_table, "outputs/tables/phase2_hba1c_spline.csv")
write_audit_csv(result$ispad_table, "outputs/tables/phase2_hba1c_ispad_logistic.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_hba1c_target_summary.csv")

if (!is.null(result$dm_summary)) {
  cat(sprintf("[Faz II/KISIM XXIV] DM-only HbA1c: n=%d (median=%.2f%%, n_under_7=%d)\n",
    result$dm_summary$n_with_hba1c,
    result$dm_summary$median_hba1c,
    result$dm_summary$n_under_7))
}
if (!is.null(result$bayesian_status)) {
  cat(sprintf("[Faz II/KISIM XXIV/65] Bayesian joint: %d/%d outcome\n",
    sum(result$bayesian_status$status == "ok", na.rm = TRUE),
    nrow(result$bayesian_status)))
}
if (!is.null(result$spline_table)) {
  cat(sprintf("[Faz II/KISIM XXIV/66] Tani yasi spline: %d/%d outcome\n",
    sum(result$spline_table$status == "ok", na.rm = TRUE),
    nrow(result$spline_table)))
}
if (!is.null(result$ispad_table)) {
  cat(sprintf("[Faz II/KISIM XXIV/68] ISPAD logistic: %d/%d outcome\n",
    sum(result$ispad_table$status == "ok", na.rm = TRUE),
    nrow(result$ispad_table)))
}

invisible(result)
