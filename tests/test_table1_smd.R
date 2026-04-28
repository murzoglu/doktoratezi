source("R/13_table1_smd.R")

fixture <- data.frame(
  group = c("DM", "DM", "DM", "Kontrol", "Kontrol", "Kontrol"),
  anne_yas = c(40, 42, NA, 38, 39, 40),
  egitim_durumu = c(4, 5, 4, 3, 4, 3),
  anne_antidepresan = c(1, 1, 0, 0, 0, 0),
  beck_severity = factor(
    c("Minimal", "Hafif", "Orta", "Minimal", "Minimal", NA),
    levels = c("Minimal", "Hafif", "Orta", "Siddetli")
  ),
  ses_latent = c(0.5, 0.6, 0.7, -0.1, 0.0, 0.1)
)

spec <- data.frame(
  variable = c("anne_yas", "egitim_durumu", "anne_antidepresan", "beck_severity", "ses_latent"),
  label = c("Anne yaş", "Anne eğitim", "Anne antidepresan", "BDI şiddet", "Latent SES"),
  type = c("continuous", "categorical", "binary", "categorical", "continuous"),
  block = c("Demografi", "SES", "Klinik", "Klinik", "SES"),
  stringsAsFactors = FALSE
)

results <- build_table1_family(fixture, spec = spec)

summary <- results$table
stopifnot(all(c(
  "variable", "label", "row_type", "level", "overall", "DM", "Kontrol",
  "missing_n", "missing_pct", "smd", "abs_smd", "balance_flag", "p_value", "q_value"
) %in% names(summary)))
stopifnot(any(summary$variable == "anne_yas" & summary$row_type == "continuous"))
stopifnot(any(summary$variable == "beck_severity" & summary$row_type == "missing"))

continuous_smd <- table1_smd_continuous(fixture$anne_yas, fixture$group)
expected_pooled <- sqrt((stats::var(c(40, 42)) + stats::var(c(38, 39, 40))) / 2)
expected_smd <- (mean(c(40, 42)) - mean(c(38, 39, 40))) / expected_pooled
stopifnot(isTRUE(all.equal(continuous_smd$smd, expected_smd)))

binary_smd <- table1_smd_binary(fixture$anne_antidepresan, fixture$group)
stopifnot(binary_smd$smd > 0)
stopifnot(binary_smd$abs_smd > 0.40)

categorical_smd <- table1_smd_categorical(fixture$beck_severity, fixture$group)
stopifnot(categorical_smd$abs_smd > 0)
stopifnot(identical(categorical_smd$method, "max_abs_level_smd"))

balance <- results$smd_balance
stopifnot(all(c("variable", "smd", "abs_smd", "balance_flag", "recommended_action") %in% names(balance)))
stopifnot(balance$balance_flag[balance$variable == "anne_antidepresan"] == "ciddi_dengesizlik")

target_summary <- summarize_table1_targets(fixture, results)
stopifnot(identical(target_summary$input_rows, 6L))
stopifnot(target_summary$table_rows >= length(spec$variable))

bad_fixture <- fixture
bad_fixture$group <- "DM"
stopifnot(inherits(
  try(build_table1_family(bad_fixture, spec = spec), silent = TRUE),
  "try-error"
))
