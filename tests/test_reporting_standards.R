source("R/09_reporting_standards.R")

checklist <- reporting_standards_checklist()
registry <- reporting_framework_registry()

validation_result <- validate_reporting_standards_checklist(checklist)
stopifnot(isTRUE(validation_result))

stopifnot(setequal(unique(checklist$framework), registry$framework))
stopifnot(!anyDuplicated(paste(checklist$framework, checklist$item, sep = "::")))
stopifnot(all(checklist$status %in% reporting_status_levels()))
stopifnot(all(checklist$priority %in% reporting_priority_levels()))
stopifnot(all(table(checklist$framework) >= c("CONSORT-Mixed" = 7, "JARS-Mixed" = 8, "STROBE" = 12)[names(table(checklist$framework))]))

summary <- summarize_reporting_standards(checklist)
stopifnot(sum(summary$n) == nrow(checklist))
stopifnot(all(summary$status %in% reporting_status_levels()))

findings <- reporting_standards_findings(checklist)
stopifnot(all(findings$severity == "review"))
stopifnot(any(findings$framework == "STROBE"))
stopifnot(!any(findings$item == "STROBE-07"))

bad_checklist <- checklist
bad_checklist$status[1] <- "done"
stopifnot(inherits(
  try(validate_reporting_standards_checklist(bad_checklist), silent = TRUE),
  "try-error"
))
