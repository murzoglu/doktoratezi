# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXX/87-90 audit runner

source("R/47_power_replication.R")

result <- run_power_replication_pipeline(
  n_aile_grid = c(100, 150, 200, 241, 300, 400, 500),
  apim_rs = c(0.10, 0.15, 0.20, 0.25, 0.30, 0.40),
  apim_powers = c(0.80, 0.90),
  bssd_n_grid = c(100, 150, 200, 241, 300, 400, 500),
  multilevel_n_sim = 200L,
  bssd_n_sim = 200L,
  d_target = 0.20,
  icc_aile = 0.20,
  d_assumed_bayesian = 0.16
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

write_audit_csv(result$multilevel_power, "outputs/tables/phase2_power_multilevel.csv")
write_audit_csv(result$apim_sample_size, "outputs/tables/phase2_power_apim.csv")
write_audit_csv(result$bayesian_ssd, "outputs/tables/phase2_power_bayesian_ssd.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase2_power_target_summary.csv")

if (!is.null(result$multilevel_power)) {
  cat(sprintf("[Faz II/KISIM XXX/87] Multilevel power: %d satir\n",
    nrow(result$multilevel_power)))
  for (i in seq_len(nrow(result$multilevel_power))) {
    cat(sprintf("  n_aile=%d, d=%.2f, power=%.3f\n",
      result$multilevel_power$n_aile[i],
      result$multilevel_power$d_target[i],
      result$multilevel_power$power[i]))
  }
}
if (!is.null(result$apim_sample_size)) {
  cat(sprintf("[Faz II/KISIM XXX/88] APIM sample size: %d satir\n",
    nrow(result$apim_sample_size)))
}
if (!is.null(result$bayesian_ssd)) {
  cat(sprintf("[Faz II/KISIM XXX/89] Bayesian SSD: %d satir\n",
    nrow(result$bayesian_ssd)))
}

invisible(result)
