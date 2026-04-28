# tests/test_h5_dyadic_concordance.R
# H5 (KISIM V/16) — Diadik tutarlılık 5 strateji assertion seti.

suppressPackageStartupMessages({ library(targets) })
source("R/00_paths.R")
source("R/20_h5_dyadic_concordance.R")

tar_load(c(df_family_ses, df_family_scored, df_long_scored))

results <- run_h5_dyadic_concordance_pipeline(
  df_family_ses    = df_family_ses,
  df_family_scored = df_family_scored,
  df_long_scored   = df_long_scored,
  run_rsa = TRUE, run_cfa = TRUE, run_k = TRUE, n_boot = 50L
)

# Strateji 1: ICC + Bland-Altman — 4 alt ölçek × 3 dyad × 3 grup = 36 satır
stopifnot(
  is.data.frame(results$icc_bland_altman_table),
  nrow(results$icc_bland_altman_table) == 36L,
  all(c("subscale", "dyad", "group", "icc", "loa_lo", "loa_hi") %in% names(results$icc_bland_altman_table))
)

# Strateji 2: RSA — sicaklik + reddetme × 3 grup = 6 satır status
stopifnot(
  is.data.frame(results$rsa_status_table),
  nrow(results$rsa_status_table) >= 6L,
  any(results$rsa_status_table$status == "fit_ok")
)

# Strateji 3: Common Fate Model — 4 alt ölçek
stopifnot(
  is.data.frame(results$common_fate_status_table),
  nrow(results$common_fate_status_table) == 4L,
  any(results$common_fate_status_table$status == "fit_ok")
)

# Strateji 4: Olsen-Kenny dyadic CFA — pooled + Kontrol + DM = 3 satır
stopifnot(
  is.data.frame(results$dyadic_cfa_status_table),
  nrow(results$dyadic_cfa_status_table) == 3L,
  all(results$dyadic_cfa_status_table$status == "fit_ok")
)

# Latent konkordans — 3 grup için sayısal değer
stopifnot(
  is.data.frame(results$dyadic_cfa_latent_corr_table),
  nrow(results$dyadic_cfa_latent_corr_table) == 3L,
  all(is.finite(results$dyadic_cfa_latent_corr_table$true_concordance))
)

# Strateji 5: k-coefficient — 4 alt ölçek
stopifnot(
  is.data.frame(results$k_coefficient_table),
  nrow(results$k_coefficient_table) == 4L,
  any(results$k_coefficient_table$status == "fit_ok")
)

# Inconsistency patterns — 3 örüntü × 2 grup = 6 satır
stopifnot(
  is.data.frame(results$inconsistency_patterns_table),
  nrow(results$inconsistency_patterns_table) == 6L,
  all(results$inconsistency_patterns_table$prop_flagged >= 0 &
        results$inconsistency_patterns_table$prop_flagged <= 1)
)

# Target summary
stopifnot(
  nrow(results$target_summary) == 6L,
  all(results$target_summary$n_rows >= 0)
)

cat("[PASS] H5 dyadic concordance (5 strategies + inconsistency patterns)\n")
