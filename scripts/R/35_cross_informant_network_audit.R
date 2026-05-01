# [KESIFSEL - POST-HOC] Faz II SAP KISIM XX/53 audit runner
#
# Cross-informant GGM kanonik veri uzerinde 12 dugum (anne EMBU-P + Beck +
# indeks cocuk EMBU-C + SRQ) icin EBIC-LASSO regulariazasyon ile fit eder;
# pooled + DM/Kontrol stratifiye ag yapilarini outputs/tables/phase2_xinfo_*.csv
# olarak yazar.
#
# Calistirma: Rscript scripts/R/35_cross_informant_network_audit.R

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/34_cross_informant_network.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data

result <- run_cross_informant_network_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  gamma = 0.5,
  correlation = "spearman",
  group_split = TRUE
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

write_audit_csv(result$nodes, "outputs/tables/phase2_xinfo_nodes.csv")
write_audit_csv(result$coverage, "outputs/tables/phase2_xinfo_coverage.csv")
write_audit_csv(result$status, "outputs/tables/phase2_xinfo_status.csv")
write_audit_csv(result$edges, "outputs/tables/phase2_xinfo_edges.csv")
write_audit_csv(result$centrality, "outputs/tables/phase2_xinfo_centrality.csv")
write_audit_csv(result$cross_informant_summary, "outputs/tables/phase2_xinfo_summary.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_xinfo_target_summary.csv")

if (!is.null(result$status) && nrow(result$status) > 0L) {
  cat(sprintf(
    "[Faz II/KISIM XX/53] Cross-informant GGM audit: %d/%d ag tahmin edildi\n",
    sum(result$status$status == "ok", na.rm = TRUE),
    nrow(result$status)
  ))
} else {
  cat("[Faz II/KISIM XX/53] Cross-informant GGM audit: status yok\n")
}

invisible(result)
