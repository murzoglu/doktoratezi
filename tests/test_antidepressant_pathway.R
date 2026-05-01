source("R/38_antidepressant_pathway.R")

set.seed(20260507L)

# 1) Helpers
stopifnot(identical(ad_normalize(c(0, 1, NA, 2)), c(0L, 1L, NA_integer_, 1L)))
stopifnot(identical(levels(ad_factor_from_bin(c(0L, 1L))), c("Yok", "Var")))
stopifnot(identical(ad_normalize_role("Indeks"), "indeks"))

# 2) Synthetic family fixture
n <- 200L
family <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), each = n / 2L),
  anne_antidepresan = rbinom(n, 1, prob = c(rep(0.10, n / 2L), rep(0.30, n / 2L))),
  beck_total = stats::rnorm(n, 8, 5),
  ses_latent = stats::rnorm(n),
  anne_yas = stats::rnorm(n, 38, 5),
  stringsAsFactors = FALSE
)
for (s in ad_subscale_outcomes()) {
  family[[paste0("embu_p_", s, "_mean")]] <- stats::rnorm(n, 2, 0.5)
}

frame <- ad_prepare_family_frame(family)
stopifnot(all(c("ad_bin", "ad_f", "beck_total_z", "ses_latent_z", "anne_yas_z") %in% names(frame)))
stopifnot(all(frame$ad_bin %in% c(0L, 1L, NA_integer_)))
stopifnot(identical(levels(frame$ad_f), c("Yok", "Var")))

# 3) Long fixture
long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  cocuk_yas = stats::runif(2 * n, 8, 17),
  stringsAsFactors = FALSE
)
for (s in ad_subscale_outcomes()) {
  long[[paste0("embu_c_", s, "_mean")]] <- stats::rnorm(nrow(long), 2, 0.5)
}

long_frame <- ad_prepare_long_frame(long, frame)
stopifnot(all(c("group_dm", "ad_bin", "beck_total_z", "cocuk_yas_z") %in% names(long_frame)))
stopifnot(all(long_frame$role_token %in% c("indeks", "kardes")))
stopifnot(nrow(long_frame) == 2L * n) # iki rol per aile

# 4) Mediator pipeline (bootstrap_n dusuk)
if (requireNamespace("lavaan", quietly = TRUE)) {
  med <- ad_mediator_pipeline(frame, bootstrap_n = 100L, outcomes = "reddetme")
  stopifnot(!is.null(med$status))
  stopifnot(med$status$outcome_subscale == "reddetme")
  if (identical(med$status$status, "ok")) {
    stopifnot(any(med$estimates$op == ":="))   # indirect/total/prop_mediated
    stopifnot(any(med$estimates$label %in% c("a", "b", "cprime", "indirect", "total", "prop_mediated")))
    stopifnot(!is.null(med$sensitivity))
    stopifnot("rho_observed_residual_corr" %in% names(med$sensitivity))
  }
}

# 5) H1 moderation
if (requireNamespace("lme4", quietly = TRUE) && requireNamespace("lmerTest", quietly = TRUE)) {
  h1 <- ad_moderation_pipeline_h1(long_frame, outcomes = "reddetme")
  stopifnot(!is.null(h1$status))
  if (identical(h1$status$status[1L], "ok")) {
    stopifnot(!is.null(h1$fixed_effects))
    stopifnot("term" %in% names(h1$fixed_effects))
    stopifnot(any(grepl("group_dm:ad_bin", h1$fixed_effects$term)))
  }
}

# 6) H4 moderation
h4 <- ad_moderation_pipeline_h4(frame, outcomes = "reddetme")
stopifnot(!is.null(h4$status))
stopifnot(h4$status$status == "ok")
stopifnot(any(grepl("beck_total_z:ad_bin", h4$fixed_effects$term)))

# 7) H5 stratified
h5 <- ad_moderation_pipeline_h5(frame, long_frame, outcomes = "reddetme")
stopifnot(!is.null(h5$stratified_correlations))
stopifnot(nrow(h5$stratified_correlations) == 4L) # 2 group x 2 ad

# 8) Beck x AD interaction
beck_int <- ad_beck_interaction_pipeline(frame, outcomes = "reddetme")
stopifnot(!is.null(beck_int$status))
stopifnot(beck_int$status$status == "ok")
stopifnot("hc3_se" %in% names(beck_int$fixed_effects))

# 9) Pipeline target_summary
if (requireNamespace("lavaan", quietly = TRUE)) {
  pipeline_result <- run_ad_pathway_pipeline(family, long, bootstrap_n = 100L)
  stopifnot(!is.null(pipeline_result$family_summary))
  stopifnot(pipeline_result$family_summary$n_total == n)
  stopifnot(pipeline_result$family_summary$n_ad_var > 0L)
  stopifnot(grepl("KESIFSEL", pipeline_result$target_summary$kanit_kategorisi, fixed = TRUE))
}

cat("PASS: tests/test_antidepressant_pathway.R\n")
