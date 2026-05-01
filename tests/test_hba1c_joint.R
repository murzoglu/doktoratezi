source("R/40_hba1c_joint.R")

set.seed(20260509L)

# 1) Subscale helpers
stopifnot(length(hba1c_subscale_outcomes()) == 4L)
stopifnot(length(hba1c_anne_outcome_columns()) == 4L)

# 2) Bayesian priors
priors <- hba1c_bayesian_priors()
stopifnot(priors$parenting$mean == 0.16)
stopifnot(priors$parenting$sd == 0.10)

# 3) Synthetic fixture: ilk 60 DM (25'i HbA1c'li), sonraki 60 Kontrol
n <- 120L
n_hba1c_target <- 25L
fixture <- data.frame(
  aile_no = seq_len(n),
  group_f = factor(c(rep("DM", n / 2L), rep("Kontrol", n / 2L)),
    levels = c("Kontrol", "DM")),
  anne_yas = stats::rnorm(n, 38, 5),
  ses_latent = stats::rnorm(n),
  hba1c = NA_real_,
  tani_yasi = NA_real_,
  dm_yili = NA_real_,
  stringsAsFactors = FALSE
)
# DM-only HbA1c: ilk 25 DM
fixture$hba1c[seq_len(n_hba1c_target)] <- stats::rnorm(n_hba1c_target, 8.5, 1.5)
# DM-only tani_yasi/dm_yili (ilk 60)
fixture$tani_yasi[seq_len(n / 2L)] <- stats::runif(n / 2L, 4, 14)
fixture$dm_yili[seq_len(n / 2L)] <- stats::runif(n / 2L, 1, 8)
for (col in hba1c_anne_outcome_columns()) {
  fixture[[col]] <- stats::rnorm(n, 2, 0.5)
}

# 4) DM-only prep
dm_only <- hba1c_prepare_dm_only(fixture, require_hba1c = TRUE)
summary_attr <- attr(dm_only, "hba1c_summary")
stopifnot(!is.null(summary_attr))
stopifnot(summary_attr$n_with_hba1c == n_hba1c_target)
stopifnot(nrow(dm_only) == n_hba1c_target)
stopifnot(all(c("hba1c_z", "tani_yasi_z", "dm_yili_z", "anne_yas_z",
  "ses_latent_z", "hba1c_under_7") %in% names(dm_only)))
stopifnot(all(c("embu_p_reddetme_mean_z", "embu_p_sicaklik_mean_z") %in% names(dm_only)))

# 5) Tani yasi spline pipeline
spline <- hba1c_tani_yasi_spline_pipeline(dm_only, df_spline = 3L)
stopifnot(nrow(spline) == 4L)
stopifnot(all(spline$status %in% c("ok", "insufficient_n")))
if (any(spline$status == "ok")) {
  stopifnot(all(c("decision", "lrt_f", "lrt_p", "aic_linear", "aic_spline") %in%
    names(spline)))
}

# 6) ISPAD logistic
ispad <- hba1c_ispad_logistic_pipeline(dm_only)
stopifnot(nrow(ispad) == 4L)
stopifnot(all(ispad$status %in% c("ok", "insufficient_outcome_events", "fit_error",
  "missing_columns", "predictor_not_in_model")))

# 7) Bayesian (skip in test if brms slow — minimum chain for smoke)
if (requireNamespace("brms", quietly = TRUE) && nrow(dm_only) >= 15L) {
  bayes <- hba1c_bayesian_pipeline(dm_only,
    outcomes = "reddetme",
    chains = 2L, iter = 500L)
  stopifnot(!is.null(bayes$status))
  stopifnot(nrow(bayes$status) == 1L)
  if (identical(bayes$status$status, "ok")) {
    stopifnot(!is.null(bayes$posterior))
    stopifnot(all(c("posterior_median", "ci_lower", "ci_upper", "pd",
      "rope_share") %in% names(bayes$posterior)))
  }
}

# 8) Pipeline
pipeline_result <- run_hba1c_joint_pipeline(
  fixture,
  brms_chains = 2L,
  brms_iter = 500L,
  run_bayesian = FALSE,  # test'te brms kapali
  df_spline = 3L
)
stopifnot(grepl("KESIFSEL", pipeline_result$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(pipeline_result$target_summary$n_hba1c == n_hba1c_target)
stopifnot(!is.null(pipeline_result$spline_table))
stopifnot(!is.null(pipeline_result$ispad_table))

cat("PASS: tests/test_hba1c_joint.R\n")
