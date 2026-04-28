# scripts/R/25_latent_profile_audit.R

suppressPackageStartupMessages({ library(targets) })

source("R/00_paths.R")
source("R/24_latent_profile.R")

paths <- thesis_paths()
out_tables <- file.path(paths$outputs_dir, "tables")
dir.create(out_tables, showWarnings = FALSE, recursive = TRUE)

tar_load(c(df_family_ses, df_family_scored))

results <- run_latent_profile_pipeline(
  df_family_ses = df_family_ses,
  df_family_scored = df_family_scored,
  profile_range = 1:5,
  run_bifactor = TRUE
)

write_csv <- function(df, name) {
  if (is.null(df) || (is.data.frame(df) && nrow(df) == 0L)) {
    cat(sprintf("  [skip] %s — empty\n", name))
    return(invisible(NULL))
  }
  utils::write.csv(df, file.path(out_tables, paste0(name, ".csv")), row.names = FALSE)
  cat(sprintf("  [ok]   %s.csv (%d rows)\n", name, nrow(df)))
}

cat("\n=== KISIM VII Latent Variable Audit ===\n")
write_csv(results$status_table,            "lpa_status")
write_csv(results$lpa_fit_table,           "lpa_fit_indices")
write_csv(results$lpa_classes_table,       "lpa_classes_distribution")
write_csv(results$lpa_profile_means_table, "lpa_profile_means")
write_csv(results$lpa_group_distribution,  "lpa_group_distribution")
write_csv(results$lca_indicator_audit_table, "lca_indicator_audit")
write_csv(results$lca_fit_table,             "lca_fit_indices")
write_csv(results$lca_classes_table,         "lca_classes_distribution")
write_csv(results$lca_item_response_prob_table, "lca_item_response_probabilities")
write_csv(results$lca_group_distribution,    "lca_group_distribution")
write_csv(results$lca_modal_regression_table, "lca_modal_class_regression")
write_csv(results$flexmix_fit_table,          "mixture_regression_flexmix_fit")
write_csv(results$flexmix_coefficient_table,  "mixture_regression_flexmix_coefficients")
write_csv(results$flexmix_class_distribution, "mixture_regression_class_distribution")
write_csv(results$flexmix_group_distribution, "mixture_regression_group_distribution")
write_csv(results$bifactor_fit_table,      "bifactor_s1_fit")
write_csv(results$bifactor_loadings_table, "bifactor_s1_general_loadings")

cat("\n=== Status ===\n")
print(results$status_table)
cat("\n=== LPA fit indices ===\n")
print(results$lpa_fit_table)
cat(sprintf("\n[best n profiles by BIC] = %s\n", results$lpa_best_n))
cat("\n=== LPA class distribution ===\n")
print(results$lpa_classes_table)
cat("\n=== LPA group × class ===\n")
print(results$lpa_group_distribution)
cat(sprintf("\n[best n LCA classes by BIC] = %s\n", results$lca_best_n))
cat("\n=== LCA fit indices ===\n")
print(results$lca_fit_table)
cat("\n=== LCA class distribution ===\n")
print(results$lca_classes_table)
cat("\n=== LCA modal-class regression ===\n")
print(results$lca_modal_regression_table)
cat("\n=== Flexmix mixture regression fit ===\n")
print(results$flexmix_fit_table)
cat("\n=== Bifactor S-1 fit ===\n")
print(results$bifactor_fit_table)
cat("\n[done] Latent variable audit complete.\n")
