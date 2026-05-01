# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXI/54 audit runner
#
# Standard GRM (Gaussian) ve floor-aware GRM (empiricalhist) modellerini
# kanonik veri uzerinde EMBU reddetme alt olcegi icin (anne + indeks) fit eder.
# Cikti: outputs/tables/phase2_floor_irt_*.csv
#
# Calistirma: Rscript scripts/R/36_floor_aware_irt_audit.R

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/35_floor_aware_irt.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)

# group_dm turetimi (eksikse)
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
df_family_scored <- ensure_group_dm(df_family_scored)
df_long_scored <- ensure_group_dm(df_long_scored)

# Faz II odagi: reddetme + (asiri_koruma ek) — floor effect en yuksek alt olcekler
result <- run_floor_aware_irt_pipeline(
  df_family_scored = df_family_scored,
  df_long_scored = df_long_scored,
  subscales = c("reddetme", "asiri_koruma"),
  informants = c("anne", "indeks")
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

write_audit_csv(result$floor_summary, "outputs/tables/phase2_floor_irt_floor_summary.csv")
write_audit_csv(result$status, "outputs/tables/phase2_floor_irt_status.csv")
write_audit_csv(result$item_parameters, "outputs/tables/phase2_floor_irt_item_parameters.csv")
write_audit_csv(result$theta_comparison, "outputs/tables/phase2_floor_irt_theta_comparison.csv")
write_audit_csv(result$group_delta, "outputs/tables/phase2_floor_irt_group_delta.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_floor_irt_target_summary.csv")

if (!is.null(result$status) && nrow(result$status) > 0L) {
  cat(sprintf(
    "[Faz II/KISIM XXI/54] Floor-aware IRT audit: %d/%d model yakinsadi\n",
    sum(result$status$status == "ok", na.rm = TRUE),
    nrow(result$status)
  ))
}

invisible(result)
