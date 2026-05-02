source("R/48_phase2_apa_outputs.R")

set.seed(20260520L)

# 1) Format helpers
stopifnot(phase2_apa_format_pct(0.75) == "75.0%")
stopifnot(phase2_apa_format_num(0.146, 3L) == "0.146")
stopifnot(phase2_apa_format_p(.0002) == "<.001")
stopifnot(phase2_apa_format_p(.013) == "0.013")
stopifnot(phase2_apa_format_p(NA) == "—")

# 2) Stub tables
trifactor_loadings <- data.frame(
  subscale = rep("reddetme", 12L),
  factor = rep(c("F_trait_red", "F_indeks_red", "F_kardes_red"), each = 4L),
  method = rep(c("trait", "indeks_method", "kardes_method"), each = 4L),
  item = rep(c("embu_p_q05", "embu_c_q05_indeks", "embu_c_q05_kardes", "embu_p_q09"), 3L),
  std_loading = c(0.6, 0.5, 0.4, 0.65, 0.3, 0.25, 0.2, 0.35, 0.4, 0.35, 0.3, 0.45),
  se = NA_real_, z = NA_real_, p_value = NA_real_,
  ci_lower = NA_real_, ci_upper = NA_real_,
  stringsAsFactors = FALSE
)

trifactor_fit <- data.frame(
  subscale = c("reddetme", "sicaklik"),
  cfi = c(0.92, 0.88),
  rmsea = c(0.05, 0.06),
  stringsAsFactors = FALSE
)

xinfo_summary <- data.frame(
  group_label = c("all", "DM", "Kontrol"),
  n_edges_total = c(16L, 16L, 5L),
  n_edges_cross_informant = c(1L, 0L, 0L),
  cross_informant_share = c(0.0625, 0, 0),
  stringsAsFactors = FALSE
)

floor_irt_delta <- data.frame(
  subscale = rep(c("reddetme", "asiri_koruma"), each = 2L),
  informant = rep(c("anne", "indeks"), 2L),
  cohen_d = c(-0.20, 0.37, 0.06, 0.54),
  stringsAsFactors = FALSE
)

omegah_metrics <- data.frame(
  domain = c("EMBU-P", "EMBU-C", "Beck"),
  omega_h = c(0.66, 0.54, 0.89),
  ecv = c(0.41, 0.51, 0.78),
  stringsAsFactors = FALSE
)

h5ext_pooled <- data.frame(
  group_focus = c("dm", "kontrol", "diff"),
  pooled_mean = c(0.179, 0.130, 0.047),
  pooled_lower = c(0.097, 0.081, -0.023),
  pooled_upper = c(0.260, 0.180, 0.117),
  tau = c(0.073, 0, 0),
  stringsAsFactors = FALSE
)

ad_h5_strat <- data.frame(
  hypothesis = "H5",
  outcome_subscale = rep(c("reddetme", "sicaklik"), each = 4L),
  group_dm = rep(c(0L, 0L, 1L, 1L), 2L),
  ad_bin = rep(c(0L, 1L, 0L, 1L), 2L),
  n = rep(c(110, 11, 85, 35), 2L),
  pearson_r = c(0.04, 0.05, -0.09, 0.15, 0.14, 0.40, 0.04, 0.01),
  ci_lower = c(-0.15, -0.57, -0.30, -0.20, -0.05, -0.26, -0.17, -0.33),
  ci_upper = c(0.23, 0.63, 0.12, 0.46, 0.32, 0.81, 0.25, 0.34),
  p_value = NA_real_,
  stringsAsFactors = FALSE
)

hba1c_bayes <- data.frame(
  predictor_subscale = c("sicaklik", "reddetme"),
  posterior_median = c(0.123, 0.067),
  pd = c(0.944, 0.800),
  ci_lower = c(-0.031, -0.091),
  ci_upper = c(0.275, 0.232),
  rope_share = c(0.386, 0.652),
  stringsAsFactors = FALSE
)

multi_h1_spec <- data.frame(
  spec_id = 1:30,
  outcome_subscale = sample(c("sicaklik", "reddetme"), 30, replace = TRUE),
  status = rep("ok", 30L),
  group_dm_estimate = stats::rnorm(30, 0.13, 0.06),
  group_dm_se = stats::runif(30, 0.04, 0.08),
  group_dm_p = stats::runif(30, 0.001, 0.20),
  n_used = rep(482, 30L),
  stringsAsFactors = FALSE
)

multi_h1_curve <- data.frame(
  n_total_spec = 120L, n_ok_spec = 120L,
  median_estimate = 0.134, share_p_under_05 = 0.75,
  stringsAsFactors = FALSE
)

multi_sca <- data.frame(
  n_perm = 5000L, observed_test_stat = 4.084, perm_p_value = 0.0002,
  estimator = "median_t", stringsAsFactors = FALSE
)

meta_combined <- data.frame(
  study_label = c("Pinquart_2013", "Pinquart_2018", "Lovejoy_2000",
    "Vermaes_2012", "T1DM_EBEVEYN_red"),
  yi = c(-0.16, 0.20, 0.40, 0.17, 0.147),
  vi = c(0.0064, 0.0081, 0.0144, 0.0100, 0.0015),
  stringsAsFactors = FALSE
)

meta_pooling <- data.frame(
  pooled_mean = 0.139, pooled_lower = 0.049, pooled_upper = 0.230,
  tau = 0.106, stringsAsFactors = FALSE
)

clinical_fit <- data.frame(
  model_type = c("baseline", "extended"),
  auc = c(0.586, 0.703),
  stringsAsFactors = FALSE
)

# 3) APA summary table
summary_tbl <- phase2_apa_summary_table(
  trifactor_fit = trifactor_fit,
  disc_latent_correlation = data.frame(
    subscale = "reddetme", latent_r = 0.025, ci_lower = -0.13, ci_upper = 0.18,
    p_value = 0.76, stringsAsFactors = FALSE
  ),
  floor_irt_group_delta = floor_irt_delta,
  omegah_metrics = omegah_metrics,
  h5ext_strategy_pooled = h5ext_pooled,
  hba1c_bayesian = hba1c_bayes,
  multi_h1_curve = multi_h1_curve,
  meta_pooling = meta_pooling,
  multi_sca = multi_sca,
  clinical_fit = clinical_fit
)
stopifnot(!is.null(summary_tbl))
stopifnot(nrow(summary_tbl) >= 6L)
stopifnot(all(c("kisim", "analiz", "ana_metrik", "yorum") %in% names(summary_tbl)))

# 4) Pipeline (ggplot2 yoksa skip)
if (requireNamespace("ggplot2", quietly = TRUE)) {
  result <- run_phase2_apa_outputs_pipeline(
    trifactor_loadings_table = trifactor_loadings,
    trifactor_fit_indices_table = trifactor_fit,
    xinfo_summary_table = xinfo_summary,
    floor_irt_group_delta_table = floor_irt_delta,
    omegah_metrics_summary_table = omegah_metrics,
    h5ext_strategy_pooled_table = h5ext_pooled,
    ad_h5_stratified_table = ad_h5_strat,
    hba1c_bayesian_posterior_table = hba1c_bayes,
    multi_h1_spec_results_table = multi_h1_spec,
    multi_h1_curve_summary_table = multi_h1_curve,
    multi_sca_inferential_table = multi_sca,
    meta_combined_studies_table = meta_combined,
    meta_pooling_summary_table = meta_pooling,
    clinical_fit_summary_table = clinical_fit,
    output_dir = tempfile("phase2_figs_")
  )
  stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))
  stopifnot(length(result$figures) == 6L)
  stopifnot(length(result$figure_paths) == 6L)
}

cat("PASS: tests/test_phase2_apa_outputs.R\n")
