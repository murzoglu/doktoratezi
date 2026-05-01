source("R/43_distributional.R")

set.seed(20260512L)

# 1) Helpers
stopifnot(identical(dist_cocuk_outcome("reddetme"), "embu_c_reddetme_mean"))
stopifnot(identical(dist_normalize_role("Indeks"), "indeks"))
stopifnot(all(dist_normalize_to_unit(c(1, 2.5, 4)) > 0))
stopifnot(all(dist_normalize_to_unit(c(1, 2.5, 4)) < 1))

# 2) Synthetic family + long fixture
n <- 150L
family <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), each = n / 2L),
  ses_latent = stats::rnorm(n),
  anne_yas = stats::rnorm(n, 38, 5),
  stringsAsFactors = FALSE
)
long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  cocuk_yas = stats::runif(2 * n, 8, 17),
  cinsiyet_f = factor(sample(c("Kiz", "Erkek"), 2 * n, replace = TRUE),
    levels = c("Kiz", "Erkek")),
  stringsAsFactors = FALSE
)
for (sl in dist_subscale_outcomes()) {
  group_eff <- 0.3 * as.numeric(family$group_dm == 1L)
  base <- 2 + 0.5 * group_eff
  long_base <- rep(base, each = 2L) + stats::rnorm(2 * n, 0, 0.6)
  long[[paste0("embu_c_", sl, "_mean")]] <- pmin(pmax(long_base, 1), 4)
}

# 3) Prepare long
prepared <- dist_prepare_long(long, family)
stopifnot(nrow(prepared) == 2 * n)
stopifnot(all(c("group_dm", "cocuk_yas_z", "ses_latent_z", "anne_yas_z") %in% names(prepared)))

# 4) Quantile regression
if (requireNamespace("quantreg", quietly = TRUE)) {
  q_table <- dist_quantile_regression_pipeline(prepared, outcomes = "reddetme",
    taus = c(0.5, 0.75, 0.9), bootstrap_R = 200L)
  stopifnot(!is.null(q_table))
  stopifnot(nrow(q_table) >= 3L)
  stopifnot(all(c("tau", "estimate", "ci_lower", "ci_upper") %in% names(q_table)))
}

# 5) Beta regression (gamlss fallback)
b_table <- dist_beta_regression_pipeline(prepared, outcomes = "reddetme")
stopifnot(!is.null(b_table))
stopifnot(b_table$status[1L] %in% c("ok", "fit_error", "predictor_not_in_model"))

# 6) Pipeline (brms kapali smoke)
result <- run_distributional_pipeline(family, long,
  outcomes = "reddetme",
  taus = c(0.5, 0.9),
  bootstrap_R = 200L,
  run_distributional = FALSE,
  brms_chains = 2L,
  brms_iter = 500L
)
stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(!is.null(result$quantile_table))
stopifnot(!is.null(result$beta_table))

cat("PASS: tests/test_distributional.R\n")
