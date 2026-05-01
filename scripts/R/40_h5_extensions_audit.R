# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXIII/61-64 audit runner

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/39_h5_extensions.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data

ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f) - 1L
    } else if ("grup" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$grup), ignore.case = TRUE))
    }
  }
  df
}
df_family_ses <- ensure_group_dm(df_family_ses)
df_family_scored <- ensure_group_dm(df_family_scored)
df_long_scored <- ensure_group_dm(df_long_scored)

result <- run_h5_extensions_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  df_family_scored = df_family_scored,
  bootstrap_n = 1000L,
  brms_chains = 2L,
  brms_iter = 2000L,
  run_mtmm = TRUE,
  run_pooling = TRUE
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

write_audit_csv(result$mtmm_status, "outputs/tables/phase2_h5ext_mtmm_status.csv")
write_audit_csv(result$mtmm_fit_indices, "outputs/tables/phase2_h5ext_mtmm_fit_indices.csv")
write_audit_csv(result$mtmm_variance, "outputs/tables/phase2_h5ext_mtmm_variance.csv")
write_audit_csv(result$beck_moderation_status, "outputs/tables/phase2_h5ext_beck_moderation_status.csv")
write_audit_csv(result$beck_moderation_coefficients,
  "outputs/tables/phase2_h5ext_beck_moderation_coefficients.csv")
write_audit_csv(result$beck_moderation_bootstrap_ci,
  "outputs/tables/phase2_h5ext_beck_moderation_bootstrap_ci.csv")
write_audit_csv(result$sibling_icc, "outputs/tables/phase2_h5ext_sibling_icc.csv")
write_audit_csv(result$strategy_estimates,
  "outputs/tables/phase2_h5ext_strategy_estimates.csv")
write_audit_csv(result$strategy_pooled_summary,
  "outputs/tables/phase2_h5ext_strategy_pooled.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_h5ext_target_summary.csv")

if (!is.null(result$mtmm_status)) {
  cat(sprintf("[Faz II/KISIM XXIII/61] MTMM CT-C(M-1): %s (n=%d pairs)\n",
    result$mtmm_status$status, result$mtmm_status$n_pairs))
}
if (!is.null(result$beck_moderation_status)) {
  cat(sprintf("[Faz II/KISIM XXIII/62] Beck x Grup moderation: %d/%d outcome\n",
    sum(result$beck_moderation_status$status == "ok", na.rm = TRUE),
    nrow(result$beck_moderation_status)))
}
if (!is.null(result$sibling_icc)) {
  cat(sprintf("[Faz II/KISIM XXIII/63] Sibling-pair ICC: %d satir\n",
    nrow(result$sibling_icc)))
}
if (!is.null(result$strategy_pooled_summary)) {
  cat(sprintf("[Faz II/KISIM XXIII/64] Strategy pooling: %d focus group\n",
    nrow(result$strategy_pooled_summary)))
}

invisible(result)
