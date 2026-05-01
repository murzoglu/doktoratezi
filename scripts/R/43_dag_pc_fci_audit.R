# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXV/70, 72 audit runner

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/42_dag_pc_fci.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data
df_family_ses <- dag_ensure_group_dm(df_family_ses)

# Tarih kolonlarini df_family_ses'e tasi (raw'dan)
if (!"anket_tarihi" %in% names(df_family_ses) && "anket_tarihi" %in% names(df_family)) {
  df_family_ses$anket_tarihi <- df_family$anket_tarihi[
    match(df_family_ses$aile_no, df_family$aile_no)
  ]
}

result <- run_dag_pc_fci_pipeline(
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

write_audit_csv(result$implied_conditional_independencies,
  "outputs/tables/phase2_dag_implied_ci.csv")
write_audit_csv(result$ci_test_results, "outputs/tables/phase2_dag_ci_tests.csv")
write_audit_csv(result$three_level_table, "outputs/tables/phase2_dag_three_level.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_dag_target_summary.csv")

if (!is.null(result$ci_test_results)) {
  cat(sprintf(
    "[Faz II/KISIM XXV/70] DAG CI tests: %d satir (rejected=%d / consistent=%d)\n",
    nrow(result$ci_test_results),
    sum(result$ci_test_results$ci_implication == "rejected", na.rm = TRUE),
    sum(result$ci_test_results$ci_implication == "consistent", na.rm = TRUE)
  ))
}
if (!is.null(result$three_level_table)) {
  cat(sprintf(
    "[Faz II/KISIM XXV/72] 3-level varyans: %d/%d outcome (n_year_levels=%d)\n",
    sum(result$three_level_table$status == "ok", na.rm = TRUE),
    nrow(result$three_level_table),
    result$n_year_levels
  ))
}

invisible(result)
