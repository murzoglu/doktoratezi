source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/29_apa_tables.R")
source("R/50_statistical_audit.R")

paths <- canonical_final_reference_paths()
data <- load_final_reference_data(paths, reader = "utils")

df_family <- prepare_family(data$family)
df_long <- prepare_long(data$long)
result_tables <- collect_statistical_audit_csv_tables("outputs/tables")

audit <- run_statistical_audit(
  df_family = df_family,
  df_long = df_long,
  result_tables = result_tables
)

findings_path <- save_apa_table_csv(audit$findings, "outputs/tables/statistical_audit_findings.csv")
summary_path <- save_apa_table_csv(audit$summary, "outputs/tables/statistical_audit_summary.csv")
registry_path <- save_apa_table_csv(audit$tool_registry, "outputs/tables/statistical_audit_tool_registry.csv")

invisible(assert_statistical_audit_ok(audit$findings))

cat(sprintf(
  "Statistical audit passed: status=%s, findings=%d, critical=%d, files=%d\nfindings=%s\nsummary=%s\nregistry=%s\n",
  audit$summary$status[[1L]],
  audit$summary$total_findings[[1L]],
  audit$summary$critical_findings[[1L]],
  length(result_tables),
  findings_path,
  summary_path,
  registry_path
))
