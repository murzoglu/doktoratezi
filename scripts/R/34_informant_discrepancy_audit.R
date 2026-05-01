# [KESIFSEL - POST-HOC] Faz II SAP KISIM XX/51-52 audit runner
#
# Two-factor latent corr + LDS modelleri kanonik veri uzerinde
# 4 EMBU alt olcegi icin fit eder ve outputs/tables/phase2_disc_*.csv
# olarak yazar.
#
# Calistirma: Rscript scripts/R/34_informant_discrepancy_audit.R

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/33_informant_discrepancy.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data

# group_dm ve beck_total iceriyor mu? Eksikse turet
if (!"group_dm" %in% names(df_family_ses)) {
  if ("group_f" %in% names(df_family_ses)) {
    df_family_ses$group_dm <- as.integer(df_family_ses$group_f) - 1L
  } else if ("grup" %in% names(df_family_ses)) {
    df_family_ses$group_dm <- as.integer(grepl("DM", as.character(df_family_ses$grup), ignore.case = TRUE))
  } else {
    stop("group_dm/group_f/grup yok; df_family_ses kontrol edin")
  }
}

result <- run_informant_discrepancy_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  include_predictors = TRUE,
  fit_lds = TRUE
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

write_audit_csv <- function(df, path) {
  if (is.null(df) || nrow(df) == 0L) {
    stub <- data.frame(
      note = "empty result; see status table",
      stringsAsFactors = FALSE
    )
    utils::write.csv(stub, path, row.names = FALSE, fileEncoding = "UTF-8")
  } else {
    utils::write.csv(df, path, row.names = FALSE, fileEncoding = "UTF-8")
  }
}

write_audit_csv(result$coverage, "outputs/tables/phase2_disc_coverage.csv")
write_audit_csv(result$scaling, "outputs/tables/phase2_disc_scaling.csv")
write_audit_csv(result$status, "outputs/tables/phase2_disc_status.csv")
write_audit_csv(result$fit_indices, "outputs/tables/phase2_disc_fit_indices.csv")
write_audit_csv(result$latent_correlation, "outputs/tables/phase2_disc_latent_correlation.csv")
write_audit_csv(result$variance, "outputs/tables/phase2_disc_variance.csv")
write_audit_csv(result$predictor_paths, "outputs/tables/phase2_disc_predictor_paths.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_disc_target_summary.csv")

if (!is.null(result$status) && nrow(result$status) > 0L) {
  cat(sprintf(
    "[Faz II/KISIM XX/51-52] Discrepancy audit: %d/%d model yakinsadi (4 alt olcek x 2 model)\n",
    sum(result$status$converged, na.rm = TRUE),
    nrow(result$status)
  ))
} else {
  cat("[Faz II/KISIM XX/51-52] Discrepancy audit: status yok\n")
}

invisible(result)
