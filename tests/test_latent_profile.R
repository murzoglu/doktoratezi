# tests/test_latent_profile.R
# KISIM VII — LPA (anne tipoloji) + Bifactor S-1.

suppressPackageStartupMessages({ library(targets) })
source("R/00_paths.R")
source("R/24_latent_profile.R")

tar_load(c(df_family_ses, df_family_scored))

# Frame preparation
prep <- lpa_prepare_frame(df_family_ses)
stopifnot(
  is.list(prep),
  prep$n_full == 241L,
  prep$n_complete >= 200L
)

# LPA estimate
lpa_res <- run_lpa(df_family_ses, profile_range = 1:4)
stopifnot(
  lpa_res$status == "ok",
  is.data.frame(lpa_res$fit_table),
  nrow(lpa_res$fit_table) == 4L,
  all(c("Classes", "BIC", "Entropy") %in% names(lpa_res$fit_table)),
  is.numeric(lpa_res$best_n),
  lpa_res$best_n >= 1 && lpa_res$best_n <= 4,
  is.data.frame(lpa_res$classes_table),
  nrow(lpa_res$classes_table) >= 1L,
  is.data.frame(lpa_res$profile_means_table),
  nrow(lpa_res$profile_means_table) >= length(lpa_indicators())
)

# LCA sensitivity and modal-class mixture regression
lca_prep <- lca_prepare_frame(df_family_ses)
stopifnot(
  is.list(lca_prep),
  lca_prep$n_full == 241L,
  lca_prep$n_complete_indicators >= 230L,
  all(lca_indicators() %in% names(lca_prep$full))
)

lca_res <- run_lca(df_family_ses, class_range = 1:4, nrep = 10L)
stopifnot(
  lca_res$status == "ok",
  is.data.frame(lca_res$indicator_audit_table),
  nrow(lca_res$indicator_audit_table) >= 14L,
  is.data.frame(lca_res$fit_table),
  nrow(lca_res$fit_table) == 4L,
  all(c("nclass", "bic", "entropy", "min_class_prop") %in% names(lca_res$fit_table)),
  is.numeric(lca_res$best_n),
  lca_res$best_n >= 1 && lca_res$best_n <= 4,
  is.data.frame(lca_res$item_response_prob_table),
  nrow(lca_res$item_response_prob_table) > 0L
)

lca_modal <- run_lca_modal_regression(lca_res)
stopifnot(
  lca_modal$status == "ok",
  is.data.frame(lca_modal$regression_table),
  nrow(lca_modal$regression_table) >= 5L,
  all(c("class_contrast", "term", "odds_ratio", "p_value") %in% names(lca_modal$regression_table))
)

flexmix_res <- run_flexmix_regression(df_family_ses, k = 2L)
stopifnot(
  flexmix_res$status %in% c("ok", "boundary_solution"),
  is.data.frame(flexmix_res$fit_table),
  nrow(flexmix_res$fit_table) == 1L,
  is.data.frame(flexmix_res$coefficient_table),
  nrow(flexmix_res$coefficient_table) >= 4L
)

# Bifactor S-1
bifactor <- run_bifactor_s1(df_family_scored, target_subscale = "asiri_koruma")
stopifnot(
  bifactor$status == "ok",
  is.data.frame(bifactor$fit_table),
  nrow(bifactor$fit_table) == 1L,
  is.finite(bifactor$fit_table$cfi),
  is.finite(bifactor$fit_table$rmsea),
  is.data.frame(bifactor$general_loadings_table),
  nrow(bifactor$general_loadings_table) == 29L
)

# Pipeline orchestrator
results <- run_latent_profile_pipeline(df_family_ses, df_family_scored,
                                        profile_range = 1:4, run_bifactor = TRUE)
stopifnot(
  is.data.frame(results$status_table),
  nrow(results$status_table) == 5L,
  all(results$status_table$status %in% c("ok", "boundary_solution")),
  is.data.frame(results$lca_fit_table),
  is.data.frame(results$lca_modal_regression_table),
  is.data.frame(results$flexmix_fit_table)
)

cat("[PASS] KISIM VII LPA + LCA + Mixture Regression + Bifactor S-1\n")
