# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXII/58-60 audit runner
#
# Anne antidepresan kullanim hatti — mediator + moderator + Beck x AD
# Cikti: outputs/tables/phase2_ad_*.csv
#
# Calistirma: Rscript scripts/R/39_antidepressant_pathway_audit.R

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/38_antidepressant_pathway.R")

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
df_long_scored <- ensure_group_dm(df_long_scored)

result <- run_ad_pathway_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  bootstrap_n = 1000L
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

write_audit_csv(result$family_summary, "outputs/tables/phase2_ad_family_summary.csv")
write_audit_csv(result$mediator_status, "outputs/tables/phase2_ad_mediator_status.csv")
write_audit_csv(result$mediator_estimates, "outputs/tables/phase2_ad_mediator_estimates.csv")
write_audit_csv(result$mediator_sensitivity, "outputs/tables/phase2_ad_mediator_sensitivity.csv")
write_audit_csv(result$moderation_h1_status, "outputs/tables/phase2_ad_moderation_h1_status.csv")
write_audit_csv(result$moderation_h1_fixed_effects, "outputs/tables/phase2_ad_moderation_h1_fixed_effects.csv")
write_audit_csv(result$moderation_h4_status, "outputs/tables/phase2_ad_moderation_h4_status.csv")
write_audit_csv(result$moderation_h4_fixed_effects, "outputs/tables/phase2_ad_moderation_h4_fixed_effects.csv")
write_audit_csv(result$moderation_h5_stratified_correlations,
  "outputs/tables/phase2_ad_moderation_h5_stratified_correlations.csv")
write_audit_csv(result$beck_interaction_status, "outputs/tables/phase2_ad_beck_interaction_status.csv")
write_audit_csv(result$beck_interaction_fixed_effects, "outputs/tables/phase2_ad_beck_interaction_fixed_effects.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_ad_target_summary.csv")

if (!is.null(result$mediator_status)) {
  cat(sprintf(
    "[Faz II/KISIM XXII/58] AD mediator: %d/%d outcome yakinsadi\n",
    sum(result$mediator_status$status == "ok", na.rm = TRUE),
    nrow(result$mediator_status)
  ))
}
if (!is.null(result$moderation_h1_status)) {
  cat(sprintf(
    "[Faz II/KISIM XXII/59] AD x grup moderation H1: %d/%d, H4: %d/%d, H5: %d strat corr satiri\n",
    sum(result$moderation_h1_status$status == "ok", na.rm = TRUE),
    nrow(result$moderation_h1_status),
    sum(result$moderation_h4_status$status == "ok", na.rm = TRUE),
    nrow(result$moderation_h4_status),
    nrow(result$moderation_h5_stratified_correlations %||% data.frame())
  ))
}
if (!is.null(result$beck_interaction_status)) {
  cat(sprintf(
    "[Faz II/KISIM XXII/60] Beck x AD interaction: %d/%d outcome\n",
    sum(result$beck_interaction_status$status == "ok", na.rm = TRUE),
    nrow(result$beck_interaction_status)
  ))
}

invisible(result)
