# tests/test_bayesian_parallel.R
# KISIM XII — Bayesian paralel hat (lite mode: priors_table + classify
# fonksiyonları; tam brms run audit script üzerinden çalıştırılır).

suppressPackageStartupMessages({ library(targets) })
source("R/00_paths.R")
source("R/22_bayesian_parallel.R")

tar_load(c(df_family_ses, df_long_scored))

# Priors — Pinquart 2013 temelli
priors <- bayes_pinquart_priors_h3()
stopifnot(
  is.data.frame(priors),
  nrow(priors) == 4L,
  all(priors$prior_sd > 0),
  all(grepl("Pinquart|DM|Reddetme|Aşırı koruma|Karşılaştırma", priors$rationale))
)

# Frame preparation
prep_family <- bayes_prepare_family(df_family_ses)
stopifnot(
  is.data.frame(prep_family),
  nrow(prep_family) == 241L,
  all(c("group_dm", "anne_yas_z", "ses_latent_z") %in% names(prep_family))
)

prep_long <- bayes_prepare_long(df_long_scored, df_family_ses)
stopifnot(
  is.data.frame(prep_long),
  nrow(prep_long) == 482L,
  "ses_latent_z" %in% names(prep_long)
)

# BF classifier — Jeffreys eşikleri
stopifnot(
  bayes_bf_classify(150) == "Extreme H1",
  bayes_bf_classify(50)  == "Very strong H1",
  bayes_bf_classify(15)  == "Strong H1",
  bayes_bf_classify(5)   == "Moderate H1",
  bayes_bf_classify(2)   == "Anecdotal H1",
  bayes_bf_classify(0.5) == "Anecdotal H0",
  bayes_bf_classify(0.2) == "Moderate H0",
  bayes_bf_classify(0.05) == "Strong H0",
  is.na(bayes_bf_classify(NA)) || bayes_bf_classify(NA) == "Indeterminate"
)

# Önceki audit run çıktıları olmalı (outputs/tables)
expected_csvs <- c("bayes_priors.csv", "bayes_h1_posterior.csv", "bayes_h3_posterior.csv",
                   "bayes_h1_diagnostics.csv", "bayes_h3_diagnostics.csv",
                   "bayes_loo_waic.csv", "bayes_target_summary.csv")
out_dir <- file.path(thesis_paths()$outputs_dir, "tables")
missing_csvs <- setdiff(expected_csvs, list.files(out_dir))
stopifnot(length(missing_csvs) == 0L)

# Posterior tablosu içerik smoke-test
post_h3 <- read.csv(file.path(out_dir, "bayes_h3_posterior.csv"))
stopifnot(
  nrow(post_h3) == 4L,
  all(c("estimate", "ci_lo", "ci_hi", "pd", "rope_pct", "bf10", "bf_class") %in% names(post_h3)),
  all(post_h3$pd >= 0.5 & post_h3$pd <= 1.0),
  all(post_h3$rope_pct >= 0 & post_h3$rope_pct <= 1)
)

post_h1 <- read.csv(file.path(out_dir, "bayes_h1_posterior.csv"))
stopifnot(
  nrow(post_h1) == 2L,
  all(post_h1$status == "ok")
)

# Diagnostics — R̂ < 1.01 eşiği
diag_h3 <- read.csv(file.path(out_dir, "bayes_h3_diagnostics.csv"))
stopifnot(
  nrow(diag_h3) == 4L,
  all(diag_h3$max_rhat < 1.05),
  all(diag_h3$n_divergent == 0L)
)

cat("[PASS] KISIM XII Bayesian parallel (priors + frame prep + BF classifier + audit CSV smoke)\n")
