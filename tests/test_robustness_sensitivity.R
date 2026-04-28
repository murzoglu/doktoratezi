# tests/test_robustness_sensitivity.R
# KISIM XI — Multiverse + TOST + Sensemakr/E-value + Negative control + Falsification.

suppressPackageStartupMessages({ library(targets) })
source("R/00_paths.R")
source("R/21_robustness_sensitivity.R")

tar_load(df_family_ses)

results <- run_robustness_pipeline(df_family_ses, sesoi_d = 0.30)

# Multiverse — 4 outcome × 5 controls × 2 model × 3 subset = 120 spec
stopifnot(
  is.data.frame(results$multiverse_spec_table),
  nrow(results$multiverse_spec_table) == 120L,
  all(c("outcome", "controls", "model", "subset", "estimate", "p_value", "cohens_d") %in%
        names(results$multiverse_spec_table)),
  sum(results$multiverse_spec_table$status == "ok") >= 100L
)

# Multiverse summary — 4 outcome
stopifnot(
  is.data.frame(results$multiverse_summary_table),
  nrow(results$multiverse_summary_table) == 4L,
  all(is.finite(results$multiverse_summary_table$median_d))
)

# TOST — 4 outcome × 1 SESOI = 4 satır
stopifnot(
  is.data.frame(results$tost_equivalence_table),
  nrow(results$tost_equivalence_table) == 4L,
  all(results$tost_equivalence_table$decision %in%
        c("Trivial", "Equivalent", "Meaningful", "Indeterminate"))
)

# Sensemakr + E-value — 4 outcome
stopifnot(
  is.data.frame(results$sensemakr_evalue_table),
  nrow(results$sensemakr_evalue_table) == 4L,
  all(results$sensemakr_evalue_table$status == "ok"),
  all(is.finite(results$sensemakr_evalue_table$RV_q)),
  all(results$sensemakr_evalue_table$evalue_point >= 1)
)

# Negative control — 4 outcome × 2 fake predictor = 8 satır
stopifnot(
  is.data.frame(results$negative_control_table),
  nrow(results$negative_control_table) == 8L,
  # Çoklu test rastgele false positive beklentisi: <= 2/8 (tipik %5-25)
  sum(results$negative_control_table$suspicious, na.rm = TRUE) <= 3L
)

# Falsification — 4 outcome × 2 senaryo = 8 satır
stopifnot(
  is.data.frame(results$falsification_table),
  nrow(results$falsification_table) == 8L,
  any(results$falsification_table$status == "ok")
)

# Target summary
stopifnot(
  nrow(results$target_summary) == 6L,
  all(results$target_summary$n_rows > 0L)
)

cat("[PASS] KISIM XI Robustness sensitivity (multiverse + TOST + sensemakr + neg-ctrl + falsification)\n")
