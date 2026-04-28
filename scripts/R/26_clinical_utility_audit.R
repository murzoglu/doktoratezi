# scripts/R/26_clinical_utility_audit.R

suppressPackageStartupMessages({ library(targets) })

source("R/00_paths.R")
source("R/25_clinical_utility.R")

paths <- thesis_paths()
out_tables <- file.path(paths$outputs_dir, "tables")
dir.create(out_tables, showWarnings = FALSE, recursive = TRUE)

tar_load(df_family_ses)

results <- run_clinical_utility_pipeline(df_family_ses)

write_csv <- function(df, name) {
  if (is.null(df) || (is.data.frame(df) && nrow(df) == 0L)) {
    cat(sprintf("  [skip] %s — empty\n", name))
    return(invisible(NULL))
  }
  utils::write.csv(df, file.path(out_tables, paste0(name, ".csv")), row.names = FALSE)
  cat(sprintf("  [ok]   %s.csv (%d rows)\n", name, nrow(df)))
}

cat("\n=== KISIM IX Klinik Fayda Audit ===\n")
write_csv(results$status_table,         "clinical_status")
write_csv(results$base_coef_table,      "clinical_base_logistic_coef")
write_csv(results$base_performance,     "clinical_base_performance")
write_csv(results$full_coef_table,      "clinical_full_logistic_coef")
write_csv(results$full_performance,     "clinical_full_performance")
write_csv(results$decision_curve_table, "clinical_decision_curve")
write_csv(results$cart_cp_table,        "clinical_cart_cp")
write_csv(results$rf_importance_table,  "clinical_rf_importance")
write_csv(results$calibration_table,    "clinical_calibration")
write_csv(results$nri_idi_table,        "clinical_nri_idi")

cat("\n=== Performance: base vs full ===\n")
print(rbind(
  cbind(model = "base", results$base_performance),
  cbind(model = "full", results$full_performance)
))
cat("\n=== Random Forest variable importance ===\n")
print(results$rf_importance_table)
cat("\n=== Calibration deciles ===\n")
print(results$calibration_table)
cat("\n=== NRI / IDI ===\n")
print(results$nri_idi_table)
cat("\n[done] Clinical utility audit complete.\n")
