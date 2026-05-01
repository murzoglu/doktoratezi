source("R/42_dag_pc_fci.R")

set.seed(20260511L)

# 1) Subscale helpers
stopifnot(length(dag_subscale_outcomes()) == 4L)
stopifnot(identical(dag_anne_outcome("reddetme"), "embu_p_reddetme_mean"))

# 2) Date parsing
yrs <- dag_extract_year(c("25.10.2023", "01.03.2024", NA, "bad", "14.03.2025"))
stopifnot(yrs[1L] == 2023L)
stopifnot(yrs[2L] == 2024L)
stopifnot(is.na(yrs[3L]))
stopifnot(yrs[5L] == 2025L)

# 3) Dagitty syntax
if (requireNamespace("dagitty", quietly = TRUE)) {
  dag <- dag_canonical_specification()
  stopifnot(!is.null(dag))
  cis <- dag_implied_conditional_independencies(dag)
  stopifnot(is.data.frame(cis))
}

# 4) Synthetic family fixture
n <- 200L
family <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), each = n / 2L),
  ses_latent = stats::rnorm(n),
  anne_yas = stats::rnorm(n, 38, 5),
  age_gap = stats::runif(n, 1, 6),
  cocuk_sayisi = sample(2:4, n, replace = TRUE),
  anket_tarihi = sample(c("25.10.2023", "14.03.2024", "02.09.2025"), n, replace = TRUE),
  stringsAsFactors = FALSE
)
for (sl in dag_subscale_outcomes()) {
  family[[paste0("embu_p_", sl, "_mean")]] <- 0.3 * family$ses_latent +
    0.2 * as.numeric(family$group_dm == 1L) + stats::rnorm(n)
}

ci_table <- dag_validate_implications(family, outcomes = "reddetme")
stopifnot(!is.null(ci_table))
stopifnot(all(c("partial_r", "n", "p_value", "ci_implication") %in% names(ci_table)))
stopifnot(any(ci_table$ci_implication %in% c("rejected", "consistent", "indeterminate",
  "missing_columns", "insufficient_n")))

# 5) 3-level model fixture
long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  stringsAsFactors = FALSE
)
for (sl in dag_subscale_outcomes()) {
  long[[paste0("embu_c_", sl, "_mean")]] <- stats::rnorm(nrow(long))
}

if (requireNamespace("lme4", quietly = TRUE)) {
  result <- run_dag_pc_fci_pipeline(family, long, outcomes = "reddetme")
  stopifnot(!is.null(result$three_level_table))
  stopifnot(!is.null(result$ci_test_results))
  stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))
  stopifnot(result$n_year_levels >= 2L)
}

cat("PASS: tests/test_dag_pc_fci.R\n")
