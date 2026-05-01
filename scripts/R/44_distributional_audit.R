# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXVI/73, 74, 75 audit runner

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/43_distributional.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data
df_family_ses <- dist_ensure_group_dm(df_family_ses)

result <- run_distributional_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  taus = c(0.50, 0.75, 0.90),
  bootstrap_R = 5000L,
  run_distributional = TRUE,
  brms_chains = 2L,
  brms_iter = 2000L
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

write_audit_csv(result$quantile_table, "outputs/tables/phase2_dist_quantile.csv")
write_audit_csv(result$distributional_status, "outputs/tables/phase2_dist_distributional_status.csv")
write_audit_csv(result$distributional_posterior, "outputs/tables/phase2_dist_distributional_posterior.csv")
write_audit_csv(result$beta_table, "outputs/tables/phase2_dist_beta.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_dist_target_summary.csv")

if (!is.null(result$quantile_table)) {
  cat(sprintf(
    "[Faz II/KISIM XXVI/73] Quantile regression: %d/%d satir (n_long=%d)\n",
    sum(result$quantile_table$status == "ok", na.rm = TRUE),
    nrow(result$quantile_table),
    result$n_long
  ))
}
if (!is.null(result$distributional_status)) {
  cat(sprintf(
    "[Faz II/KISIM XXVI/74] Distributional regression: %d/%d outcome\n",
    sum(result$distributional_status$status == "ok", na.rm = TRUE),
    nrow(result$distributional_status)
  ))
}
if (!is.null(result$beta_table)) {
  cat(sprintf(
    "[Faz II/KISIM XXVI/75] Beta regression: %d/%d outcome (engine=%s)\n",
    sum(result$beta_table$status == "ok", na.rm = TRUE),
    nrow(result$beta_table),
    paste(unique(result$beta_table$engine), collapse = ",")
  ))
}

invisible(result)
