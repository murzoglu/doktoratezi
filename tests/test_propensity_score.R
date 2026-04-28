source("R/15_propensity_score.R")

set.seed(42)

primary_covariates <- propensity_primary_covariates()
stopifnot(identical(primary_covariates, c("ses_latent", "age_gap", "cocuk_sayisi")))
stopifnot(!any(propensity_excluded_total_effect_covariates() %in% primary_covariates))

n_per_group <- 24L
fixture <- data.frame(
  aile_no = seq_len(n_per_group * 2L),
  group = c(rep("DM", n_per_group), rep("Kontrol", n_per_group)),
  ses_latent = c(
    stats::rnorm(n_per_group, mean = 0.35, sd = 0.85),
    stats::rnorm(n_per_group, mean = -0.25, sd = 0.85)
  ),
  age_gap = c(
    stats::rnorm(n_per_group, mean = 3.2, sd = 1.1),
    stats::rnorm(n_per_group, mean = 3.8, sd = 1.1)
  ),
  cocuk_sayisi = c(
    sample(2:4, n_per_group, replace = TRUE),
    sample(2:4, n_per_group, replace = TRUE)
  ),
  anne_antidepresan = c(rep(1, 6), rep(0, n_per_group - 6), rep(0, n_per_group)),
  beck_total = c(stats::rnorm(n_per_group, 12, 3), stats::rnorm(n_per_group, 8, 3)),
  embu_p_sicaklik_mean = c(
    stats::rnorm(n_per_group, 2.8, 0.25),
    stats::rnorm(n_per_group, 2.6, 0.25)
  ),
  embu_c_idx_sicaklik_mean = c(
    stats::rnorm(n_per_group, 2.7, 0.30),
    stats::rnorm(n_per_group, 2.5, 0.30)
  ),
  srq_ho_warmth_mean = c(
    stats::rnorm(n_per_group, 3.9, 0.35),
    stats::rnorm(n_per_group, 4.0, 0.35)
  ),
  stringsAsFactors = FALSE
)

ps_fit <- estimate_propensity_scores(fixture)
stopifnot(inherits(ps_fit$model, "glm"))
stopifnot(nrow(ps_fit$data) == nrow(fixture))
stopifnot(all(ps_fit$data$ps_value > 0 & ps_fit$data$ps_value < 1))
stopifnot(all(ps_fit$data$iptw_stabilized > 0))
stopifnot(all(ps_fit$data$iptw_trimmed <= ps_fit$data$iptw_stabilized + 1e-12))
stopifnot(identical(ps_fit$treatment_level, "DM"))
stopifnot(identical(ps_fit$control_level, "Kontrol"))

model_summary <- propensity_model_summary(ps_fit)
stopifnot(all(c("term", "estimate", "std_error", "odds_ratio", "or_ci_low", "or_ci_high") %in% names(model_summary)))
stopifnot(all(primary_covariates %in% model_summary$term))

weight_summary <- propensity_weight_summary(ps_fit)
stopifnot(all(c("overall", "DM", "Kontrol") %in% weight_summary$group))

pairs <- propensity_nearest_neighbor_pairs(ps_fit$data)
matched <- propensity_matched_data(ps_fit$data, pairs)
stopifnot(nrow(pairs) > 0L)
stopifnot(nrow(matched) == nrow(pairs) * 2L)

balance <- propensity_balance_before_after(ps_fit$data, primary_covariates, matched)
stopifnot(all(c(
  "variable", "abs_smd_before", "abs_smd_iptw", "abs_smd_matched",
  "balance_flag_iptw", "recommendation"
) %in% names(balance)))
stopifnot(all(primary_covariates %in% balance$variable))
stopifnot(all(is.finite(balance$abs_smd_before)))

pipeline <- derive_propensity_score_pipeline(fixture)
stopifnot(all(c(
  "data", "model_summary", "weight_summary", "balance", "matching_summary",
  "overlap_summary", "doubly_robust_plan", "target_summary"
) %in% names(pipeline)))
stopifnot(pipeline$target_summary$analysis_rows == nrow(fixture))
stopifnot(pipeline$target_summary$matched_pairs > 0L)
stopifnot(grepl("ses_latent;age_gap;cocuk_sayisi", pipeline$target_summary$covariates))

dr_plan <- propensity_doubly_robust_plan(pipeline$data)
stopifnot(nrow(dr_plan) >= 3L)
stopifnot(all(grepl("group_dm", dr_plan$model_formula)))
stopifnot(all(dr_plan$weight_column == "iptw_trimmed"))

dr_fit <- fit_propensity_doubly_robust_lm(pipeline$data, "embu_p_sicaklik_mean")
stopifnot(any(dr_fit$term == "group_dm"))
stopifnot(all(c("estimate", "std_error", "ci_low", "ci_high", "p_value") %in% names(dr_fit)))

bad_fixture <- fixture[, setdiff(names(fixture), "ses_latent")]
stopifnot(inherits(
  try(estimate_propensity_scores(bad_fixture), silent = TRUE),
  "try-error"
))

mediator_covariates <- c(primary_covariates, "beck_total")
stopifnot(inherits(
  try(derive_propensity_score_pipeline(fixture, covariates = mediator_covariates), silent = TRUE),
  "try-error"
))
