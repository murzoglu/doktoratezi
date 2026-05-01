source("R/39_h5_extensions.R")

set.seed(20260508L)

# 1) Helpers
stopifnot(identical(h5ext_anne_columns(c(5, 9)), c("embu_p_q05", "embu_p_q09")))
stopifnot(identical(h5ext_cocuk_columns(c(5, 9)), c("embu_c_q05", "embu_c_q09")))
stopifnot(identical(h5ext_normalize_role("Indeks"), "indeks"))

# 2) MTMM syntax
syntax <- h5ext_mtmm_syntax()
stopifnot(grepl("T_sicaklik =~", syntax, fixed = TRUE))
stopifnot(grepl("T_reddetme =~", syntax, fixed = TRUE))
stopifnot(grepl("M_indeks =~", syntax, fixed = TRUE))
stopifnot(grepl("M_indeks ~~ 0 \\* T_sicaklik", syntax))

# 3) Synthetic family + long fixture
n <- 150L
mk_ord <- function(theta, max_value = 4L, min_value = 1L) {
  raw <- theta + stats::rnorm(length(theta), 0, 0.6)
  q <- stats::quantile(raw, probs = seq(0, 1, length.out = max_value - min_value + 2L), na.rm = TRUE)
  as.integer(cut(raw, breaks = q, include.lowest = TRUE, labels = seq(min_value, max_value)))
}

family <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), each = n / 2L),
  beck_total = stats::rnorm(n, 8, 5),
  ses_latent = stats::rnorm(n),
  anne_yas = stats::rnorm(n, 38, 5),
  stringsAsFactors = FALSE
)
map <- h5ext_subscale_map()
for (sl in names(map)) {
  trait_p <- stats::rnorm(n)
  for (it in map[[sl]]) {
    family[[paste0("embu_p_q", sprintf("%02d", it))]] <- mk_ord(trait_p)
  }
  family[[paste0("embu_p_", sl, "_mean")]] <- stats::rnorm(n, 2, 0.5)
}

long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  stringsAsFactors = FALSE
)
ix_indeks <- which(long$family_role_f == "Indeks")
ix_kardes <- which(long$family_role_f == "Kardes")
for (sl in names(map)) {
  trait_c <- stats::rnorm(n)
  for (it in map[[sl]]) {
    col <- paste0("embu_c_q", sprintf("%02d", it))
    values <- numeric(nrow(long))
    values[ix_indeks] <- mk_ord(trait_c)
    values[ix_kardes] <- mk_ord(stats::rnorm(n))
    long[[col]] <- as.integer(values)
  }
  trait_c_mean <- 0.4 * trait_c + 0.6 * stats::rnorm(n)
  values <- numeric(nrow(long))
  values[ix_indeks] <- trait_c_mean
  values[ix_kardes] <- stats::rnorm(n)
  long[[paste0("embu_c_", sl, "_mean")]] <- values
}

# 4) MTMM data prep + fit
paired <- h5ext_mtmm_prepare_data(family, long)
stopifnot(nrow(paired) == n)
stopifnot(all(h5ext_anne_columns(unlist(map)) %in% names(paired)))
stopifnot(all(h5ext_cocuk_columns(unlist(map)) %in% names(paired)))

if (requireNamespace("lavaan", quietly = TRUE)) {
  result <- h5ext_mtmm_pipeline(family, long, estimator = "MLR")
  stopifnot(!is.null(result$status))
  stopifnot(result$status$n_pairs == n)
  if (identical(result$status$status, "ok")) {
    stopifnot(!is.null(result$variance))
    stopifnot(all(c("trait_var", "method_var", "communality", "trait_share",
      "method_share") %in% names(result$variance)))
  } else {
    cat(sprintf("[MTMM test] convergence skipped: %s\n",
      result$status$error_message))
  }
}

# 5) Beck x Grup moderation
beck_data <- family
for (sl in names(map)) {
  beck_data[[paste0("embu_c_", sl, "_mean")]] <- stats::rnorm(n, 2, 0.5)
}
beck_data$beck_total_z <- h5ext_scale(beck_data$beck_total)
beck_data$ses_latent_z <- h5ext_scale(beck_data$ses_latent)
beck_data$anne_yas_z <- h5ext_scale(beck_data$anne_yas)

bm <- h5ext_beck_moderation_pipeline(beck_data, outcomes = "reddetme",
  bootstrap_n = 100L)
stopifnot(!is.null(bm$status))
stopifnot(bm$status$status == "ok")
stopifnot(any(grepl("group_dm:beck_total_z", bm$coefficients$term)))
stopifnot(!is.null(bm$bootstrap_interaction_ci))

# 6) Sibling-pair ICC
sibling <- h5ext_sibling_pair_pipeline(family, long, outcomes = "reddetme")
stopifnot(!is.null(sibling$icc_table))
stopifnot(any(sibling$icc_table$group_label == "all"))

# 7) Strategy pooling defaults + fallback
defaults <- h5ext_strategy_estimates_default()
stopifnot(nrow(defaults) == 5L)
stopifnot(all(c("ICC", "RSA", "CFM", "OlsenKenny", "k_coef") %in% defaults$strategy))

pool_iv <- h5ext_strategy_pooling(group_focus = "dm", chains = 2L, iter = 500L)
stopifnot(!is.null(pool_iv))
stopifnot("pooled_mean" %in% names(pool_iv))

# 8) Pipeline
if (requireNamespace("lavaan", quietly = TRUE)) {
  pipeline_result <- run_h5_extensions_pipeline(
    df_family_ses = beck_data,
    df_long_scored = long,
    df_family_scored = family,
    bootstrap_n = 100L,
    brms_chains = 2L,
    brms_iter = 500L,
    run_mtmm = TRUE,
    run_pooling = TRUE
  )
  stopifnot(grepl("KESIFSEL", pipeline_result$target_summary$kanit_kategorisi, fixed = TRUE))
  stopifnot(!is.null(pipeline_result$sibling_icc))
}

cat("PASS: tests/test_h5_extensions.R\n")
