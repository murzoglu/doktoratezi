source("R/50_statistical_audit.R")

family_ok <- data.frame(
  aile_no = c(1, 2),
  group = c("Kontrol", "DM"),
  stringsAsFactors = FALSE
)

long_ok <- data.frame(
  aile_no = c(1, 1, 2, 2),
  group = c("Kontrol", "Kontrol", "DM", "DM"),
  family_role = c("index", "sibling", "index", "sibling"),
  role = c("Kontrol_Indeks", "Kontrol_Kardes", "DM_Hasta_Indeks", "DM_Hasta_Kardes"),
  stringsAsFactors = FALSE
)

result_ok <- data.frame(
  term = "group_fDM",
  estimate = 0.40,
  std_error = 0.20,
  statistic = 2.00,
  df_residual = 30,
  p_value = 2 * stats::pt(2.00, df = 30, lower.tail = FALSE),
  ci_low = 0.40 - stats::qt(0.975, df = 30) * 0.20,
  ci_high = 0.40 + stats::qt(0.975, df = 30) * 0.20,
  p_fdr_across_h1 = 2 * stats::pt(2.00, df = 30, lower.tail = FALSE),
  stringsAsFactors = FALSE
)

audit_ok <- run_statistical_audit(
  df_family = family_ok,
  df_long = long_ok,
  result_tables = list(h1_primary = result_ok)
)

stopifnot(is.data.frame(audit_ok$findings))
stopifnot(is.data.frame(audit_ok$summary))
stopifnot(is.data.frame(audit_ok$tool_registry))
stopifnot(!any(audit_ok$findings$severity == "critical"))
stopifnot(isTRUE(assert_statistical_audit_ok(audit_ok$findings)))
stopifnot(any(audit_ok$tool_registry$tool == "performance"))

family_bad <- data.frame(
  aile_no = c(1, 1, 3),
  group = c("Kontrol", "DM", "DM"),
  stringsAsFactors = FALSE
)

long_bad <- data.frame(
  aile_no = c(1, 1, 3),
  group = c("Kontrol", "DM", "DM"),
  family_role = c("index", "index", "index"),
  role = c("Kontrol_Indeks", "DM_Hasta_Indeks", "DM_Hasta_Indeks"),
  stringsAsFactors = FALSE
)

contract_findings <- audit_data_contract(family_bad, long_bad)
stopifnot(any(contract_findings$check_id == "family_key_unique" & contract_findings$severity == "critical"))
stopifnot(any(contract_findings$check_id == "long_family_pair_count" & contract_findings$severity == "critical"))
stopifnot(any(contract_findings$check_id == "long_group_consistency" & contract_findings$severity == "critical"))

result_bad <- result_ok
result_bad$statistic <- 1.25
result_bad$p_value <- 0.90
result_bad$ci_low <- 0.50
result_bad$p_fdr_across_h1 <- 0.01

table_findings <- audit_result_table_consistency(result_bad, table_id = "bad_h1")
stopifnot(any(table_findings$check_id == "statistic_recalculation" & table_findings$severity == "critical"))
stopifnot(any(table_findings$check_id == "p_value_recalculation" & table_findings$severity == "critical"))
stopifnot(any(table_findings$check_id == "ci_contains_estimate" & table_findings$severity == "critical"))
stopifnot(any(table_findings$check_id == "fdr_bh_recalculation" & table_findings$severity == "critical"))
stopifnot(inherits(
  try(assert_statistical_audit_ok(table_findings), silent = TRUE),
  "try-error"
))

tahmin_table <- data.frame(
  tahmin = -0.069370226,
  se = 0.07958393,
  std_beta = -0.10910828,
  t = -0.8716613,
  df = 237,
  p = 2 * stats::pt(abs(-0.8716613), df = 237, lower.tail = FALSE),
  ci_alt = -0.22615588,
  ci_ust = 0.087415428,
  stringsAsFactors = FALSE
)
tahmin_findings <- audit_result_table_consistency(tahmin_table, table_id = "tahmin_table")
stopifnot(!any(tahmin_findings$check_id == "statistic_recalculation"))

summary_bad <- summarize_statistical_audit(table_findings)
stopifnot(summary_bad$total_findings[[1L]] >= 4L)
stopifnot(summary_bad$critical_findings[[1L]] >= 4L)
stopifnot(identical(summary_bad$status[[1L]], "fail"))

csv_dir <- tempfile("stat-audit-csv-")
dir.create(csv_dir)
utils::write.csv(result_ok, file.path(csv_dir, "ok.csv"), row.names = FALSE)
writeLines(rep("", 5), file.path(csv_dir, "empty.csv"))

csv_tables <- collect_statistical_audit_csv_tables(csv_dir)
csv_findings <- attr(csv_tables, "findings", exact = TRUE)
stopifnot(identical(names(csv_tables), "ok"))
stopifnot(any(csv_findings$check_id == "csv_readable" & csv_findings$severity == "review"))

csv_audit <- run_statistical_audit(family_ok, long_ok, csv_tables)
stopifnot(any(csv_audit$findings$check_id == "csv_readable" & csv_audit$findings$severity == "review"))
stopifnot(identical(csv_audit$summary$status[[1L]], "review"))

adjusted_pairwise <- result_ok
adjusted_pairwise$adjust <- "holm_within_outcome"
adjusted_pairwise$p_value <- 0.99
stopifnot(!any(audit_result_table_consistency(adjusted_pairwise, "adjusted_pairwise")$check_id == "p_value_recalculation"))

mcar_like <- data.frame(
  status = "ok",
  statistic = 126.14,
  df = 102,
  p_value = stats::pchisq(126.14, df = 102, lower.tail = FALSE),
  stringsAsFactors = FALSE
)
stopifnot(!any(audit_result_table_consistency(mcar_like, "missing_mcar_test")$check_id == "p_value_recalculation"))

rounded_q <- data.frame(
  p_value = c(0.0749873872399339, 0.341736780799513),
  q_value = stats::p.adjust(c(0.0749873872399339, 0.341736780799513), method = "BH"),
  q_value_fmt = c(".150", ".342"),
  stringsAsFactors = FALSE
)
stopifnot(!any(audit_result_table_consistency(rounded_q, "rounded_q")$column == "q_value_fmt"))

grouped_fdr <- data.frame(
  model_type = c("a", "a", "b", "b"),
  pvalue = c(0.01, 0.20, 0.03, 0.40),
  p_fdr_across_h4 = c(stats::p.adjust(c(0.01, 0.20), method = "BH"),
    stats::p.adjust(c(0.03, 0.40), method = "BH")),
  stringsAsFactors = FALSE
)
stopifnot(!any(audit_result_table_consistency(grouped_fdr, "grouped_fdr")$check_id == "fdr_bh_recalculation"))

cat("[PASS] Statistical audit contract and numeric consistency checks\n")
