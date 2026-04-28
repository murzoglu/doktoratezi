# tests/test_mediation.R
# KISIM VI — Mediation: simple + multilevel + Hayes Model 14.

suppressPackageStartupMessages({ library(targets) })
source("R/00_paths.R")
source("R/23_mediation.R")

tar_load(c(df_family_ses, df_long_scored))

# Frame preparation
prepared <- mediation_prepare_family(df_family_ses, df_long_scored, "reddetme")
stopifnot(
  is.data.frame(prepared),
  nrow(prepared) == 241L,
  all(c("aile_no", "group_f", "beck_total", "parent_mediator", "child_outcome",
        "anne_yas_z", "ses_latent_z") %in% names(prepared)),
  sum(is.na(prepared$beck_total)) <= 5L
)

# Simple mediation
simple <- mediation_simple(prepared, n_boot = 100L, seed = 42L)
stopifnot(
  simple$status == "ok",
  is.data.frame(simple$effect_table),
  nrow(simple$effect_table) >= 5L,
  all(c("a", "b", "cprime", "indirect", "direct") %in% simple$effect_table$parameter)
)

# Multilevel mediation
multilevel <- mediation_multilevel(df_long_scored, df_family_ses,
                                    subscale = "reddetme", n_boot = 100L)
stopifnot(
  multilevel$status == "ok",
  is.data.frame(multilevel$effect_table),
  nrow(multilevel$effect_table) >= 4L
)

# Conditional process — Hayes Model 14
conditional <- mediation_conditional_process(prepared, n_boot = 100L)
stopifnot(
  conditional$status == "ok",
  is.data.frame(conditional$effect_table),
  any(grepl("cond_indirect|index_mod_mediation", conditional$effect_table$parameter))
)

# Pipeline orchestrator
results <- run_mediation_pipeline(
  df_family_ses, df_long_scored,
  subscale = "reddetme", run_bayes = FALSE, n_boot = 100L
)
stopifnot(
  is.data.frame(results$status_table),
  nrow(results$status_table) == 4L,
  sum(results$status_table$status == "ok") >= 3L,
  is.data.frame(results$target_summary)
)

cat("[PASS] KISIM VI Mediation (simple + multilevel + conditional process)\n")
