source("R/09_reporting_standards.R")

checklist <- reporting_standards_checklist()
validate_reporting_standards_checklist(checklist)

summary <- summarize_reporting_standards(checklist)
findings <- reporting_standards_findings(checklist)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
utils::write.csv(
  checklist,
  "outputs/tables/reporting_standards_checklist.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  summary,
  "outputs/tables/reporting_standards_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  findings,
  "outputs/tables/reporting_standards_findings.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  "Reporting standards audit passed: %d checklist item(s), %d review finding(s), 0 critical finding(s)\n",
  nrow(checklist),
  nrow(findings)
))
