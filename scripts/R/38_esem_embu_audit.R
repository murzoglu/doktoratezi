# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXI/57 audit runner
#
# ESEM (geomin rotation) + CFA baseline karsilastirmasi
# EMBU-P (anne) ve EMBU-C (indeks cocuk) icin
# Cikti: outputs/tables/phase2_esem_*.csv

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/37_esem_embu.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)

result <- run_esem_embu_pipeline(
  df_family_scored = df_family_scored,
  df_long_scored = df_long_scored,
  n_factors = 4L,
  rotation = "geomin"
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

write_audit_csv(result$status, "outputs/tables/phase2_esem_status.csv")
write_audit_csv(result$fit_indices, "outputs/tables/phase2_esem_fit_indices.csv")
write_audit_csv(result$loadings, "outputs/tables/phase2_esem_loadings.csv")
write_audit_csv(result$cross_loading_summary, "outputs/tables/phase2_esem_cross_loading_summary.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_esem_target_summary.csv")

if (!is.null(result$status) && nrow(result$status) > 0L) {
  cat(sprintf(
    "[Faz II/KISIM XXI/57] ESEM audit: %d/%d model yakinsadi\n",
    sum(result$status$status == "ok", na.rm = TRUE),
    nrow(result$status)
  ))
}

invisible(result)
