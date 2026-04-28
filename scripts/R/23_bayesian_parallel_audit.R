# scripts/R/23_bayesian_parallel_audit.R
# KISIM XII Bayesian paralel hat audit.
# brms ile H3 (4 EMBU-P alt ölçek) + H1 (2 EMBU-C alt ölçek) modelleri.

suppressPackageStartupMessages({ library(targets); library(brms) })

source("R/00_paths.R")
source("R/22_bayesian_parallel.R")

paths <- thesis_paths()
out_tables <- file.path(paths$outputs_dir, "tables")
out_models <- file.path(paths$outputs_dir, "models")
dir.create(out_tables, showWarnings = FALSE, recursive = TRUE)
dir.create(out_models, showWarnings = FALSE, recursive = TRUE)

tar_load(c(df_family_ses, df_long_scored))

# Pratik MCMC ayarları (auto mod, makul süre):
# chains=2, iter=2000, warmup=1000 → ~1-2 dk per model × 6 model = 10-15 dk
results <- run_bayesian_parallel_pipeline(
  df_family_ses, df_long_scored,
  run_h1 = TRUE, run_h3 = TRUE,
  iter = 2000L, warmup = 1000L, chains = 2L, seed = 20260428L
)

write_csv <- function(df, name) {
  if (is.null(df) || (is.data.frame(df) && nrow(df) == 0L)) {
    cat(sprintf("  [skip] %s — empty\n", name))
    return(invisible(NULL))
  }
  utils::write.csv(df, file.path(out_tables, paste0(name, ".csv")), row.names = FALSE)
  cat(sprintf("  [ok]   %s.csv (%d rows)\n", name, nrow(df)))
}

cat("\n=== KISIM XII Bayesian Audit ===\n")
write_csv(results$priors_table,         "bayes_priors")
write_csv(results$h1_posterior_table,   "bayes_h1_posterior")
write_csv(results$h1_diagnostics_table, "bayes_h1_diagnostics")
write_csv(results$h3_posterior_table,   "bayes_h3_posterior")
write_csv(results$h3_diagnostics_table, "bayes_h3_diagnostics")
write_csv(results$loo_waic_table,       "bayes_loo_waic")
write_csv(results$target_summary,       "bayes_target_summary")

# Persist a representative fit for downstream use
if (length(results$fits$h3) > 0L) {
  saveRDS(results$fits$h3[["embu_p_reddetme_mean"]],
          file.path(out_models, "bayes_h3_reddetme.rds"))
  cat("  [ok]   models/bayes_h3_reddetme.rds saved\n")
}
if (length(results$fits$h1) > 0L) {
  saveRDS(results$fits$h1[["embu_c_reddetme_mean"]],
          file.path(out_models, "bayes_h1_reddetme_long.rds"))
  cat("  [ok]   models/bayes_h1_reddetme_long.rds saved\n")
}

cat("\n=== H3 Posterior özeti (Bayesian dual reporting) ===\n")
print(results$h3_posterior_table[, c("outcome", "estimate", "ci_lo", "ci_hi", "pd", "rope_pct", "bf10", "bf_class")])
cat("\n=== H3 MCMC diagnostics ===\n")
print(results$h3_diagnostics_table)
cat("\n=== H1 Posterior özeti ===\n")
print(results$h1_posterior_table[, c("outcome", "estimate", "ci_lo", "ci_hi", "pd", "rope_pct", "bf10", "bf_class")])
cat("\n=== LOO/WAIC ===\n")
print(results$loo_waic_table)
cat("\n[done] Bayesian audit complete.\n")
