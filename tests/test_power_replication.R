source("R/47_power_replication.R")

set.seed(20260519L)

# 1) Subscale outcomes
stopifnot(length(power_subscale_outcomes()) == 4L)

# 2) Multilevel power simulation (small grid + small n_sim for speed)
if (requireNamespace("lme4", quietly = TRUE) && requireNamespace("lmerTest", quietly = TRUE)) {
  ml <- power_simulate_multilevel(
    n_aile_grid = c(100, 150),
    d_target = 0.30,
    icc_aile = 0.20,
    n_sim = 30L
  )
  stopifnot(nrow(ml) == 2L)
  stopifnot(all(c("n_aile", "power", "status") %in% names(ml)))
  stopifnot(all(ml$power >= 0 & ml$power <= 1, na.rm = TRUE))
}

# 3) APIM sample size
if (requireNamespace("pwr", quietly = TRUE)) {
  apim <- power_apim_sample_size(rs = c(0.20, 0.30), powers = c(0.80))
  stopifnot(nrow(apim) == 2L)
  stopifnot(all(c("n_independent", "n_dyad") %in% names(apim)))
  stopifnot(all(apim$n_dyad < apim$n_independent, na.rm = TRUE))
}

# 4) Bayesian SSD
bssd <- power_bayesian_ssd(
  n_grid = c(100, 200),
  d_assumed = 0.20,
  n_sim = 30L
)
stopifnot(nrow(bssd) == 2L)
stopifnot(all(c("n", "mean_hdi_width", "share_hdi_under_target",
  "share_outside_rope") %in% names(bssd)))

# 5) Pipeline (compact)
result <- run_power_replication_pipeline(
  n_aile_grid = c(100, 200),
  apim_rs = c(0.20),
  apim_powers = c(0.80),
  bssd_n_grid = c(100, 200),
  multilevel_n_sim = 20L,
  bssd_n_sim = 30L,
  d_target = 0.30
)
stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(!is.null(result$multilevel_power))
stopifnot(!is.null(result$apim_sample_size))
stopifnot(!is.null(result$bayesian_ssd))
stopifnot(is.null(result$replication_plan)) # cikarildi

cat("PASS: tests/test_power_replication.R\n")
