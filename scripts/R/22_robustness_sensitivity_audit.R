# scripts/R/22_robustness_sensitivity_audit.R
# KISIM XI Robustluk + Sensitivite denetimi.

suppressPackageStartupMessages({ library(targets) })

source("R/00_paths.R")
source("R/21_robustness_sensitivity.R")

paths <- thesis_paths()
out_tables <- file.path(paths$outputs_dir, "tables")
dir.create(out_tables, showWarnings = FALSE, recursive = TRUE)

tar_load(df_family_ses)

results <- run_robustness_pipeline(df_family_ses, sesoi_d = 0.30)

write_csv <- function(df, name) {
  if (is.null(df) || (is.data.frame(df) && nrow(df) == 0L)) {
    cat(sprintf("  [skip] %s — empty\n", name))
    return(invisible(NULL))
  }
  utils::write.csv(df, file.path(out_tables, paste0(name, ".csv")), row.names = FALSE)
  cat(sprintf("  [ok]   %s.csv (%d rows)\n", name, nrow(df)))
}

cat("\n=== KISIM XI Robustluk Audit ===\n")
write_csv(results$multiverse_spec_table,    "robust_multiverse_specs")
write_csv(results$multiverse_summary_table, "robust_multiverse_summary")
write_csv(results$tost_equivalence_table,   "robust_tost_equivalence")
write_csv(results$sensemakr_evalue_table,   "robust_sensemakr_evalue")
write_csv(results$negative_control_table,   "robust_negative_control")
write_csv(results$falsification_table,      "robust_falsification")
write_csv(results$target_summary,           "robust_target_summary")

cat("\n=== Multiverse özet (alt ölçek bazlı) ===\n")
print(results$multiverse_summary_table)
cat("\n=== TOST kararları ===\n")
print(results$tost_equivalence_table[, c("outcome", "observed_d", "tost_p", "decision")])
cat("\n=== Sensemakr Robustness Value + E-value ===\n")
print(results$sensemakr_evalue_table[, c("outcome", "estimate", "p_value", "RV_q", "evalue_point")])
cat("\n=== Negative control (sahte yordayıcı) ===\n")
print(results$negative_control_table[, c("outcome", "predictor", "p_value", "suspicious")])
cat("\n=== Falsification (DM kısa süre + iyi kontrol) ===\n")
print(results$falsification_table[, c("outcome", "scenario", "base_est", "falsi_est", "attenuation_pct")])
cat("\n[done] Robustness audit complete.\n")
