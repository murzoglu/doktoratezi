# tests/test_dm_subanalyses.R
# KISIM X — DM klinik alt-analizler: HbA1c × parenting + spline + tanı yaşı strata.

suppressPackageStartupMessages({ library(targets) })
source("R/00_paths.R")
source("R/27_dm_subanalyses.R")

tar_load(df_family_ses)

# Frame preparation — DM-only
prep <- dm_prepare_frame(df_family_ses)
stopifnot(
  is.data.frame(prep),
  nrow(prep) == 120L,
  all(prep$group_f == "DM"),
  "tani_yasi_strata" %in% names(prep),
  length(levels(prep$tani_yasi_strata)) == 3L
)

# n özet — kural #19 HbA1c %32.5
n_summary <- dm_n_summary(prep)
stopifnot(
  is.data.frame(n_summary),
  nrow(n_summary) == 7L,
  n_summary$value[n_summary$metric == "n_dm_total"] == 120L,
  n_summary$value[n_summary$metric == "n_with_hba1c"] >= 30L,
  n_summary$value[n_summary$metric == "n_with_hba1c"] <= 50L
)

# HbA1c × parenting — keşifsel
hba1c <- dm_hba1c_interaction(prep, "embu_p_asiri_koruma_mean")
stopifnot(
  is.data.frame(hba1c),
  hba1c$status == "ok",
  hba1c$n <= 45L,
  is.finite(hba1c$estimate),
  is.finite(hba1c$p_value)
)

# DM süresi spline — cubic vs lineer LRT
spline <- dm_duration_spline(prep, "embu_p_asiri_koruma_mean")
stopifnot(
  is.data.frame(spline),
  spline$status == "ok",
  spline$n >= 100L,
  is.finite(spline$linear_r2),
  is.finite(spline$spline_r2),
  is.finite(spline$lrt_p),
  spline$interpretation %in% c("linear_sufficient", "nonlinear_effect")
)

# Tanı yaşı strata
strata_desc <- dm_strata_analysis(prep, "embu_p_asiri_koruma_mean")
stopifnot(
  is.data.frame(strata_desc),
  nrow(strata_desc) == 3L,
  all(strata_desc$status == "ok")
)

strata_test <- dm_strata_test(prep, "embu_p_asiri_koruma_mean")
stopifnot(
  is.data.frame(strata_test),
  strata_test$status == "ok",
  is.finite(strata_test$F_value),
  is.finite(strata_test$p_value)
)

# Pipeline orchestrator
results <- run_dm_subanalyses_pipeline(df_family_ses)
stopifnot(
  nrow(results$n_summary_table) == 7L,
  nrow(results$hba1c_interaction_table) == 5L,
  nrow(results$spline_duration_table) == 5L,
  nrow(results$strata_descriptive_table) == 15L,
  nrow(results$strata_tests_table) == 5L
)

cat("[PASS] KISIM X DM sub-analyses (HbA1c + spline + diagnosis-age strata)\n")
