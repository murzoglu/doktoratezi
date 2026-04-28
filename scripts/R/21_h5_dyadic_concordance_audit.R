# scripts/R/21_h5_dyadic_concordance_audit.R
# H5 diadik tutarlılık denetim runner'ı.
# Tüm H5 hedeflerini hesaplar, outputs/tables/ altına yazar, kısa özet basar.

suppressPackageStartupMessages({
  library(targets)
})

source("R/00_paths.R")
source("R/20_h5_dyadic_concordance.R")

paths <- thesis_paths()
out_tables <- file.path(paths$outputs_dir, "tables")
dir.create(out_tables, showWarnings = FALSE, recursive = TRUE)

tar_load(c(df_family_ses, df_family_scored, df_long_scored))

results <- run_h5_dyadic_concordance_pipeline(
  df_family_ses = df_family_ses,
  df_family_scored = df_family_scored,
  df_long_scored = df_long_scored,
  run_rsa = TRUE,
  run_cfa = TRUE,
  run_k = TRUE,
  n_boot = 200L
)

write_csv <- function(df, name) {
  if (is.null(df) || (is.data.frame(df) && nrow(df) == 0L)) {
    cat(sprintf("  [skip] %s — empty\n", name))
    return(invisible(NULL))
  }
  utils::write.csv(df, file.path(out_tables, paste0(name, ".csv")), row.names = FALSE)
  cat(sprintf("  [ok]   %s.csv (%d rows)\n", name, nrow(df)))
}

cat("\n=== H5 Diadik Tutarlılık Audit ===\n")
write_csv(results$icc_bland_altman_table,         "h5_icc_bland_altman")
write_csv(results$rsa_status_table,               "h5_rsa_status")
write_csv(results$rsa_parameters_table,           "h5_rsa_parameters")
write_csv(results$common_fate_status_table,       "h5_common_fate_status")
write_csv(results$common_fate_fit_measures_table, "h5_common_fate_fit_measures")
write_csv(results$common_fate_loadings_table,     "h5_common_fate_loadings")
write_csv(results$common_fate_regressions_table,  "h5_common_fate_regressions")
write_csv(results$dyadic_cfa_status_table,        "h5_dyadic_cfa_status")
write_csv(results$dyadic_cfa_fit_measures_table,  "h5_dyadic_cfa_fit_measures")
write_csv(results$dyadic_cfa_latent_corr_table,   "h5_dyadic_cfa_latent_corr")
write_csv(results$k_coefficient_table,            "h5_k_coefficient")
write_csv(results$inconsistency_patterns_table,   "h5_inconsistency_patterns")
write_csv(results$target_summary,                 "h5_target_summary")

cat("\n=== Strateji yansımaları ===\n")
icc_summary <- aggregate(
  icc ~ subscale + group,
  data = results$icc_bland_altman_table[results$icc_bland_altman_table$dyad == "anne_idx", ],
  FUN  = function(x) round(mean(x, na.rm = TRUE), 3)
)
print(icc_summary)
cat("\nDiyadik CFA latent concordance:\n")
print(results$dyadic_cfa_latent_corr_table)
cat("\nk-coefficient (alt ölçek bazlı):\n")
print(results$k_coefficient_table[, c("subscale", "actor", "partner", "k", "k_ci_lo", "k_ci_hi")])
cat("\nTutarsızlık örüntüsü oranları:\n")
print(results$inconsistency_patterns_table)
cat("\n[done] H5 audit complete.\n")
