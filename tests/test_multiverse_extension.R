source("R/44_multiverse_extension.R")

set.seed(20260513L)

# 1) Spec grid yapisi
g1 <- multi_h1_spec_grid(n_random_subset = 30L)
stopifnot(nrow(g1) == 30L)
stopifnot(all(c("outcome_subscale", "covariate_set", "missing_strategy",
  "random_structure", "cluster_se", "outlier_handling", "spec_id") %in% names(g1)))

g4 <- multi_h4_spec_grid(n_random_subset = 8L)
stopifnot(nrow(g4) == 8L)
stopifnot(all(c("estimator", "beck_struct", "missing_strategy", "cluster") %in% names(g4)))

# 2) Covariate set switcher
stopifnot(length(multi_h1_covariate_set("minimal")) == 2L)
stopifnot(length(multi_h1_covariate_set("dag_justified")) == 5L)
stopifnot(length(multi_h1_covariate_set("extended")) == 7L)

# 3) Synthetic family + long fixture
n <- 150L
family <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), each = n / 2L),
  ses_latent = stats::rnorm(n),
  anne_yas = stats::rnorm(n, 38, 5),
  beck_total = stats::rnorm(n, 8, 5),
  age_gap = stats::runif(n, 1, 6),
  cocuk_sayisi = sample(2:4, n, replace = TRUE),
  stringsAsFactors = FALSE
)
for (i in 1:21) family[[paste0("beck_", i)]] <- as.integer(sample(0:3, n, replace = TRUE))
for (i in c(5, 9, 10, 12, 16, 21, 22, 28)) {
  family[[paste0("embu_p_q", sprintf("%02d", i))]] <- as.integer(sample(1:4, n, replace = TRUE))
}
long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  cocuk_yas = stats::runif(2 * n, 8, 17),
  cinsiyet_f = factor(sample(c("Kiz", "Erkek"), 2 * n, replace = TRUE),
    levels = c("Kiz", "Erkek")),
  stringsAsFactors = FALSE
)
for (sl in multi_subscale_outcomes()) {
  base <- 2 + 0.3 * rep(family$group_dm, each = 2L)
  long[[paste0("embu_c_", sl, "_mean")]] <- pmin(pmax(base + stats::rnorm(2 * n, 0, 0.6), 1), 4)
}

# 4) Outlier helper
trimmed <- multi_h1_apply_outlier(data.frame(x = c(1, 2, 3, 100)), "x", method = "trim_3sd")
stopifnot(nrow(trimmed) >= 3L)

# 5) H1 single-spec fit
prepared <- multi_h1_prepare_long(long, family)
spec_one <- g1[1L, , drop = FALSE]
result_one <- multi_h1_fit_one_spec(spec_one, prepared)
stopifnot(!is.null(result_one))
stopifnot(result_one$status %in% c("ok", "missing_columns", "fit_error",
  "lme4_unavailable", "predictor_dropped", "insufficient_n"))

# 6) Pipeline (H1 limited subset for speed)
result <- multi_h1_pipeline(family, long, n_random_subset = 12L)
stopifnot(!is.null(result$spec_results))
stopifnot(nrow(result$spec_grid) == 12L)
stopifnot("rank" %in% names(result$spec_results))
stopifnot(!is.null(result$curve_summary))

# 7) BMA
bma <- multi_bma_estimate(result$spec_results, "group_dm_estimate", "group_dm_se")
stopifnot(nrow(bma) == 1L)
stopifnot(all(c("bma_pooled", "bma_lower", "bma_upper", "tau") %in% names(bma)))

# 8) H4 multi (compact subset; lavaan ordinal might fail on synthetic)
if (requireNamespace("lavaan", quietly = TRUE)) {
  h4 <- multi_h4_pipeline(family, n_random_subset = 4L)
  stopifnot(!is.null(h4$summary))
}

# 9) SCA inferential (small n_perm for speed)
sca <- multi_sca_inferential(prepared, result$curve_summary, n_perm = 100L)
stopifnot(!is.null(sca))
stopifnot("perm_p_value" %in% names(sca))

# 10) Pipeline run
pipeline <- run_multiverse_pipeline(family, long, family,
  h1_n_spec = 8L, h4_n_spec = 4L, n_perm = 50L)
stopifnot(grepl("KESIFSEL", pipeline$target_summary$kanit_kategorisi, fixed = TRUE))

cat("PASS: tests/test_multiverse_extension.R\n")
