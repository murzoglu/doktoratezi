# tests/test_clinical_utility.R
# KISIM IX — Klinik fayda: risk skor + ROC + DCA + CART + RF + NRI/IDI.

suppressPackageStartupMessages({ library(targets) })
source("R/00_paths.R")
source("R/25_clinical_utility.R")

tar_load(df_family_ses)

# Frame preparation — high_risk_mom outcome
prep <- clinical_prepare_frame(df_family_ses)
stopifnot(
  is.data.frame(prep),
  nrow(prep) == 241L,
  "high_risk_mom" %in% names(prep),
  all(prep$high_risk_mom %in% c(0L, 1L, NA))
)

# Base logistic + ROC
base <- clinical_logistic_risk(prep, clinical_predictors_base(),
                                n_boot = 50L, seed = 42L)
stopifnot(
  base$status == "ok",
  is.data.frame(base$performance_table),
  base$performance_table$auc >= 0.5,
  base$performance_table$auc <= 1.0,
  is.finite(base$performance_table$auc_corrected),
  nrow(base$coef_table) == 5L
)

# Full logistic
full <- clinical_logistic_risk(prep, clinical_predictors_extended(),
                                n_boot = 50L, seed = 42L)
stopifnot(
  full$status == "ok",
  full$performance_table$auc >= base$performance_table$auc - 0.01
)

# CART + Random Forest
cart_rf <- clinical_cart_rf(prep, clinical_predictors_extended(), seed = 42L)
stopifnot(
  cart_rf$status == "ok",
  is.data.frame(cart_rf$cart_cp_table),
  is.data.frame(cart_rf$rf_importance_table),
  nrow(cart_rf$rf_importance_table) == length(clinical_predictors_extended()),
  is.finite(cart_rf$rf_oob_error)
)

# Pipeline orchestrator
results <- run_clinical_utility_pipeline(df_family_ses, seed = 42L)
stopifnot(
  is.data.frame(results$status_table),
  nrow(results$status_table) == 2L,
  all(results$status_table$status == "ok"),
  is.data.frame(results$nri_idi_table),
  nrow(results$nri_idi_table) == 6L
)

cat("[PASS] KISIM IX Clinical utility (logistic + ROC + DCA + CART + RF + NRI/IDI)\n")
