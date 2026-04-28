# scripts/R/28_dm_subanalyses_audit.R

suppressPackageStartupMessages({ library(targets) })

source("R/00_paths.R")
source("R/27_dm_subanalyses.R")

paths <- thesis_paths()
out_tables <- file.path(paths$outputs_dir, "tables")
dir.create(out_tables, showWarnings = FALSE, recursive = TRUE)

tar_load(df_family_ses)

results <- run_dm_subanalyses_pipeline(df_family_ses)

write_csv <- function(df, name) {
  if (is.null(df) || (is.data.frame(df) && nrow(df) == 0L)) {
    cat(sprintf("  [skip] %s — empty\n", name))
    return(invisible(NULL))
  }
  utils::write.csv(df, file.path(out_tables, paste0(name, ".csv")), row.names = FALSE)
  cat(sprintf("  [ok]   %s.csv (%d rows)\n", name, nrow(df)))
}

cat("\n=== KISIM X DM Alt-Analizler Audit ===\n")
write_csv(results$n_summary_table,         "dm_n_summary")
write_csv(results$hba1c_interaction_table, "dm_hba1c_interaction")
write_csv(results$spline_duration_table,   "dm_duration_spline")
write_csv(results$strata_descriptive_table,"dm_strata_descriptive")
write_csv(results$strata_tests_table,      "dm_strata_tests")

cat("\n=== DM-only n özeti ===\n")
print(results$n_summary_table)
cat("\n=== HbA1c × parenting (n_hba1c=39 keşifsel) ===\n")
print(results$hba1c_interaction_table[, c("outcome", "n", "estimate", "p_value", "r_squared")])
cat("\n=== DM süresi spline (linear vs cubic) ===\n")
print(results$spline_duration_table[, c("outcome", "n", "linear_r2", "spline_r2", "lrt_p", "interpretation")])
cat("\n=== Tanı yaşı strata testleri ===\n")
print(results$strata_tests_table)
cat("\n[done] DM sub-analyses complete.\n")
