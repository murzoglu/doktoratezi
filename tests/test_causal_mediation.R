source("R/41_causal_mediation.R")

set.seed(20260510L)

# 1) Helpers
stopifnot(identical(cmed_anne_outcome("reddetme"), "embu_p_reddetme_mean"))
stopifnot(identical(cmed_cocuk_outcome("reddetme"), "embu_c_reddetme_mean"))

# 2) Synthetic family + long fixture
n <- 200L
family <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), each = n / 2L),
  ses_latent = stats::rnorm(n),
  anne_yas = stats::rnorm(n, 38, 5),
  stringsAsFactors = FALSE
)
shared <- stats::rnorm(n)
for (sl in cmed_subscale_outcomes()) {
  family[[paste0("embu_p_", sl, "_mean")]] <- 0.4 * shared +
    0.3 * as.numeric(family$group_dm == 1L) + stats::rnorm(n)
}

long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  cocuk_yas = stats::runif(2 * n, 8, 17),
  stringsAsFactors = FALSE
)
ix_indeks <- which(long$family_role_f == "Indeks")
ix_kardes <- which(long$family_role_f == "Kardes")
for (sl in cmed_subscale_outcomes()) {
  values <- numeric(nrow(long))
  values[ix_indeks] <- 0.5 * family[[paste0("embu_p_", sl, "_mean")]] +
    0.2 * as.numeric(family$group_dm == 1L) + stats::rnorm(n)
  values[ix_kardes] <- stats::rnorm(n)
  long[[paste0("embu_c_", sl, "_mean")]] <- values
}

# 3) Paired prep
paired <- cmed_prepare_paired(family, long)
stopifnot(nrow(paired) == n)
stopifnot(all(c("group_dm", "ses_latent_z", "anne_yas_z", "cocuk_yas_z") %in% names(paired)))

# 4) Imai-Keele single subscale
r <- cmed_imai_keele_one(paired, "reddetme")
stopifnot(identical(r$status, "ok"))
stopifnot(!is.na(r$rho_critical))
stopifnot(r$rho_critical >= -1 && r$rho_critical <= 1)
stopifnot(nchar(r$interpretation) > 0L)
stopifnot(nrow(r$sensitivity_grid) >= 21L) # rho seq -0.5..0.5 by 0.05

# 5) Pipeline
imai_pipe <- cmed_imai_keele_pipeline(paired, outcomes = "reddetme")
stopifnot(!is.null(imai_pipe$status))
stopifnot(nrow(imai_pipe$status) == 1L)

# 6) c' triangulation
long_full <- long
long_full$role_token <- cmed_normalize_role(long_full$family_role_f)
long_full <- long_full[!is.na(long_full$role_token), , drop = FALSE]
fam_join <- family
fam_join$ses_latent_z <- cmed_scale(fam_join$ses_latent)
fam_join$anne_yas_z <- cmed_scale(fam_join$anne_yas)
fam_join <- fam_join[, c("aile_no", "group_dm",
  paste0("embu_p_", cmed_subscale_outcomes(), "_mean"),
  "ses_latent_z", "anne_yas_z"), drop = FALSE]
paired_long <- merge(long_full, fam_join, by = "aile_no", all = FALSE)

triang <- cmed_cprime_triangulation(paired, paired_long, outcomes = "reddetme")
stopifnot(!is.null(triang))
stopifnot(all(c("simple_lm", "multilevel_lmer", "hayes14_conditional") %in% triang$model))

# 7) Pipeline run
result <- run_causal_mediation_pipeline(family, long, outcomes = "reddetme")
stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(!is.null(result$cprime_triangulation))

cat("PASS: tests/test_causal_mediation.R\n")
