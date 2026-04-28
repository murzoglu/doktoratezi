source("R/07_reproducibility.R")

sample_lock <- c(
  "FINAL_REFERENCE CANONICAL ANALYSIS BASE LOCK",
  "============================================",
  "",
  "status=LOCKED_CANONICAL_ANALYSIS_BASE",
  "lock_date=2026-04-26",
  "project=doktoratezi",
  "",
  "Canonical CSV files:",
  "- `data/processed/FINAL_REFERENCE__analysis_base_family.csv`: rows=241; columns=288; sha256=509d8905aa28b59b9731fedcc88dc3656123a57f7a08cc8dbf37382f8db76aa2",
  "- `data/processed/FINAL_REFERENCE__analysis_base_long.csv`: rows=482; columns=203; sha256=764d345eda31453992790e83a1ba20f6fe5dc8ab77d541a3879e13a62359dc97"
)

parsed <- parse_final_reference_lock(sample_lock)

stopifnot(identical(parsed$status, "LOCKED_CANONICAL_ANALYSIS_BASE"))
stopifnot(identical(parsed$lock_date, "2026-04-26"))
stopifnot(identical(parsed$project, "doktoratezi"))
stopifnot(nrow(parsed$files) == 2L)
stopifnot(identical(parsed$files$rows, c(241L, 482L)))
stopifnot(identical(parsed$files$columns, c(288L, 203L)))

actual <- parsed$files
valid <- compare_final_reference_facts(parsed$files, actual)
stopifnot(all(valid$ok))
stop_if_final_reference_invalid(valid)

actual_bad <- actual
actual_bad$sha256[2] <- paste(rep("0", 64), collapse = "")
invalid <- compare_final_reference_facts(parsed$files, actual_bad)
stopifnot(!all(invalid$ok))
stopifnot(inherits(try(stop_if_final_reference_invalid(invalid), silent = TRUE), "try-error"))
