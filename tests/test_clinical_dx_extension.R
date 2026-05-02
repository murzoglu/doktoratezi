source("R/46_clinical_dx_extension.R")

set.seed(20260518L)

# 1) Subscale predictors
stopifnot(length(cdx_subscale_predictors()) == 4L)
stopifnot(cdx_high_risk_threshold == 17L)

# 2) Synthetic family fixture (pseudo CSR pattern)
n <- 241L
fixture <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), times = c(121L, 120L)),
  beck_total = stats::rnorm(n, 8, 6),
  anne_yas = stats::rnorm(n, 38, 5),
  ses_latent = stats::rnorm(n),
  stringsAsFactors = FALSE
)
for (col in cdx_subscale_predictors()) {
  fixture[[col]] <- stats::rnorm(n, 2, 0.5)
}

# 3) Prepare data
prep <- cdx_prepare_data(fixture)
stopifnot(nrow(prep) <= n)
stopifnot(all(c("high_risk_anne", "anne_yas_z", "ses_latent_z",
  "embu_p_reddetme_mean_z") %in% names(prep)))
stopifnot(all(prep$high_risk_anne %in% c(0L, 1L)))

# 4) Risk model
base <- cdx_fit_risk_model(prep, model_type = "baseline")
stopifnot(identical(base$status, "ok"))
stopifnot(!is.na(base$auc))
ext <- cdx_fit_risk_model(prep, model_type = "extended")
stopifnot(identical(ext$status, "ok"))
stopifnot(!is.na(ext$auc))

# 5) Net benefit + sNB
nb <- cdx_net_benefit(stats::predict(ext$fit, type = "response"),
  prep$high_risk_anne, threshold = 0.20)
stopifnot(!is.na(nb))

# 6) SNB pipeline
snb <- cdx_snb_pipeline(prep, thresholds = c(0.10, 0.20, 0.30))
stopifnot(!is.null(snb))
stopifnot(all(c("threshold", "model_type", "net_benefit_model", "snb_model") %in% names(snb)))
stopifnot(nrow(snb) == 6L) # 2 model x 3 threshold

# 7) DCA heatmap
heatmap <- cdx_dca_threshold_heatmap_data(prep,
  thresholds = c(0.10, 0.20), cost_ratios = c(1, 2))
stopifnot(!is.null(heatmap))
stopifnot(nrow(heatmap) == 4L)

# 8) Pipeline (recalibration template cikarildi - dis veri gerektiriyordu)
result <- run_clinical_dx_extension_pipeline(fixture,
  thresholds = c(0.10, 0.20, 0.30), cost_ratios = c(1, 2, 3))
stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(!is.null(result$snb_table))
stopifnot(!is.null(result$dca_heatmap))
stopifnot(is.null(result$recalibration_template)) # cikarildi

cat("PASS: tests/test_clinical_dx_extension.R\n")
