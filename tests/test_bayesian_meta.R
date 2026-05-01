source("R/45_bayesian_meta.R")

set.seed(20260516L)

# 1) Prior studies
ps <- meta_prior_studies()
stopifnot(nrow(ps) == 4L)
stopifnot(all(c("Pinquart_2013_chronic_illness_parenting",
  "Lovejoy_2000_maternal_depression_parenting") %in% ps$study))

# 2) Synthetic family + long fixture
n <- 150L
family <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), each = n / 2L),
  ses_latent = stats::rnorm(n),
  anne_yas = stats::rnorm(n, 38, 5),
  beck_total = stats::rnorm(n, 8, 5),
  stringsAsFactors = FALSE
)
long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  cocuk_yas = stats::runif(2 * n, 8, 17),
  stringsAsFactors = FALSE
)
for (sl in meta_subscale_outcomes()) {
  long[[paste0("embu_c_", sl, "_mean")]] <- 2 + 0.3 * rep(family$group_dm, each = 2L) +
    stats::rnorm(2 * n, 0, 0.6)
}

# 3) Estimate this study (lme4 path)
if (requireNamespace("lme4", quietly = TRUE)) {
  est <- meta_estimate_this_study(family, long, outcome_subscale = "reddetme")
  stopifnot(!is.na(est$yi))
  stopifnot(!is.na(est$se))
  stopifnot(grepl("T1DM_EBEVEYN", est$study_label))
}

# 4) EB shrinkage
if (requireNamespace("lme4", quietly = TRUE)) {
  eb <- meta_empirical_bayes_shrinkage(family, long, outcome_subscale = "reddetme")
  stopifnot(identical(eb$status, "ok"))
  stopifnot(!is.null(eb$shrunk_estimates))
  stopifnot(all(c("aile_no", "shrunk_intercept", "shrunk_se", "ci_lower",
    "ci_upper", "is_outlier", "group_label") %in% names(eb$shrunk_estimates)))
  stopifnot(!is.null(eb$outlier_summary))
}

# 5) Bayesian pooling (compact)
if (requireNamespace("brms", quietly = TRUE)) {
  combined <- data.frame(
    study_label = c("A", "B", "C", "D", "E"),
    yi = c(-0.16, 0.20, 0.40, 0.17, 0.14),
    vi = c(0.0064, 0.0081, 0.0144, 0.0100, 0.0036),
    stringsAsFactors = FALSE
  )
  pool <- meta_bayesian_pooling(combined, chains = 2L, iter = 500L)
  stopifnot(!is.null(pool))
  if (identical(pool$status, "ok")) {
    stopifnot(all(c("pooled_mean", "pooled_lower", "pooled_upper", "tau") %in%
      names(pool$summary)))
  }
}

# 6) Pipeline (compact, brms iter=500 for speed)
result <- run_bayesian_meta_pipeline(family, long, outcomes = "reddetme",
  brms_chains = 2L, brms_iter = 500L, ppc_replicates = 50L)
stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(!is.null(result$combined_studies))

cat("PASS: tests/test_bayesian_meta.R\n")
