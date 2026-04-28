# scripts/R/24_mediation_audit.R
# KISIM VI Mediation audit (Beck → EMBU-P_reddetme → EMBU-C_reddetme).

suppressPackageStartupMessages({ library(targets) })

source("R/00_paths.R")
source("R/23_mediation.R")

paths <- thesis_paths()
out_tables <- file.path(paths$outputs_dir, "tables")
dir.create(out_tables, showWarnings = FALSE, recursive = TRUE)

tar_load(c(df_family_ses, df_long_scored))

# Bayesian preflight skip; ana focus frequentist 3-katman + lavaan multilevel.
# Ayrı bir Bayesian run (KISIM XII içinde) yapılır.
results <- run_mediation_pipeline(
  df_family_ses, df_long_scored,
  subscale = "reddetme",
  run_bayes = FALSE,
  n_boot = 1000L
)

write_csv <- function(df, name) {
  if (is.null(df) || (is.data.frame(df) && nrow(df) == 0L)) {
    cat(sprintf("  [skip] %s — empty\n", name))
    return(invisible(NULL))
  }
  utils::write.csv(df, file.path(out_tables, paste0(name, ".csv")), row.names = FALSE)
  cat(sprintf("  [ok]   %s.csv (%d rows)\n", name, nrow(df)))
}

cat("\n=== KISIM VI Mediation Audit ===\n")
write_csv(results$status_table,             "mediation_status")
write_csv(results$simple_effect_table,      "mediation_simple_effects")
write_csv(results$simple_fit_table,         "mediation_simple_fit")
write_csv(results$multilevel_effect_table,  "mediation_multilevel_effects")
write_csv(results$multilevel_fit_table,     "mediation_multilevel_fit")
write_csv(results$conditional_effect_table, "mediation_conditional_effects")
write_csv(results$conditional_fit_table,    "mediation_conditional_fit")
write_csv(results$bayes_indirect_table,     "mediation_bayes_indirect")
write_csv(results$target_summary,           "mediation_target_summary")

cat("\n=== Status ===\n")
print(results$status_table)
cat("\n=== Simple mediation indirect/direct ===\n")
print(results$simple_effect_table)
cat("\n=== Multilevel mediation ===\n")
print(results$multilevel_effect_table)
cat("\n=== Conditional process (Hayes 14) ===\n")
print(results$conditional_effect_table)
cat("\n[done] Mediation audit complete.\n")
