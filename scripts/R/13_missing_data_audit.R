source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/12_missing_data_frames.R")

missing_env_int <- function(name, default) {
  value <- Sys.getenv(name, unset = "")
  if (!nzchar(value)) {
    return(default)
  }
  parsed <- suppressWarnings(as.integer(value))
  if (is.na(parsed) || parsed < 1L) {
    return(default)
  }
  parsed
}

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data

missing_results <- derive_missing_data_frames(df_family_ses)
mi_m <- missing_env_int("MISSING_MI_M", 50L)
mi_maxit <- missing_env_int("MISSING_MI_MAXIT", 30L)
imputations <- run_missing_imputation_set(missing_results, m = mi_m, maxit = mi_maxit)
mi_diagnostics <- summarize_missing_mice(imputations)
target_summary <- summarize_missing_targets(df_family_ses, missing_results)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)

utils::write.csv(
  missing_results$variable_summary,
  "outputs/tables/missing_variable_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  missing_results$block_summary,
  "outputs/tables/missing_block_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  missing_results$group_summary,
  "outputs/tables/missing_group_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  missing_results$pattern_summary,
  "outputs/tables/missing_pattern_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  missing_results$frame_manifest,
  "outputs/tables/missing_frame_manifest.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  missing_results$mice_method_plan,
  "outputs/tables/missing_mice_method_plan.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  missing_results$mcar_test,
  "outputs/tables/missing_mcar_test.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  missing_results$nmar_delta_grid,
  "outputs/tables/missing_nmar_delta_grid.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  mi_diagnostics,
  "outputs/tables/missing_mi_diagnostics.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  target_summary,
  "outputs/tables/missing_target_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

if (requireNamespace("naniar", quietly = TRUE) && requireNamespace("ggplot2", quietly = TRUE)) {
  plot <- naniar::vis_miss(missing_results$frames$fiml_primary) +
    ggplot2::labs(title = "Primary FIML/MI frame missingness")
  ggplot2::ggsave(
    "outputs/figures/missing_pattern_primary.png",
    plot = plot,
    width = 12,
    height = 8,
    dpi = 300
  )
}

cat(sprintf(
  "Missing-data audit passed: primary frame %d row(s) x %d column(s), complete-case n=%d, MI m=%d maxit=%d, MCAR status=%s\n",
  target_summary$fiml_rows,
  target_summary$fiml_columns,
  target_summary$primary_complete_rows,
  mi_m,
  mi_maxit,
  missing_results$mcar_test$status
))
