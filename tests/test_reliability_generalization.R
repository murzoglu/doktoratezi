source("R/36_reliability_generalization.R")

set.seed(20260505L)

# 1) Subscale map / column helpers
map <- omegah_subscale_map()
stopifnot(all(c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma") %in% names(map)))
stopifnot(identical(omegah_anne_columns(c(5, 9)), c("embu_p_q05", "embu_p_q09")))

# 2) Bifactor S-1 syntax — EMBU-P
syntax_p <- omegah_bifactor_s1_syntax("embu_p", map, "asiri_koruma")
stopifnot(grepl("G =~ embu_p_q01", syntax_p, fixed = TRUE))
stopifnot(grepl("F_sicaklik =~", syntax_p, fixed = TRUE))
stopifnot(grepl("F_reddetme =~", syntax_p, fixed = TRUE))
stopifnot(grepl("F_karsilastirma =~", syntax_p, fixed = TRUE))
# asiri_koruma reference, F_asiri_koruma factor olmamali
stopifnot(!grepl("F_asiri_koruma", syntax_p, fixed = TRUE))
stopifnot(grepl("G ~~ 0 \\* F_sicaklik", syntax_p))

# Beck bifactor syntax
syntax_b <- omegah_beck_bifactor_syntax()
stopifnot(grepl("G_beck =~ beck_1 \\+", syntax_b))
stopifnot(grepl("F_cognitive =~ beck_1 \\+", syntax_b))
stopifnot(grepl("F_somatic =~ beck_14 \\+", syntax_b))
stopifnot(grepl("G_beck ~~ 0 \\* F_cognitive", syntax_b))
stopifnot(grepl("F_cognitive ~~ 0 \\* F_somatic", syntax_b))

# 3) Synthetic family data — EMBU-P + Beck
n <- 300L
mk_ord <- function(theta, max_value = 4L, min_value = 1L) {
  raw <- theta + stats::rnorm(length(theta), 0, 0.6)
  q <- stats::quantile(raw, probs = seq(0, 1, length.out = max_value - min_value + 2L), na.rm = TRUE)
  as.integer(cut(raw, breaks = q, include.lowest = TRUE, labels = seq(min_value, max_value)))
}
g_factor <- stats::rnorm(n)
df_family <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), each = n / 2L),
  stringsAsFactors = FALSE
)
for (sl in names(map)) {
  trait_s <- 0.6 * g_factor + 0.4 * stats::rnorm(n)
  for (it in map[[sl]]) {
    df_family[[paste0("embu_p_q", sprintf("%02d", it))]] <- mk_ord(trait_s)
  }
}
# Beck: cognitive (1-13), somatic (14-21)
beck_g <- stats::rnorm(n)
beck_cog <- 0.5 * beck_g + 0.5 * stats::rnorm(n)
beck_som <- 0.5 * beck_g + 0.5 * stats::rnorm(n)
for (it in 1:13) {
  df_family[[paste0("beck_", it)]] <- mk_ord(beck_cog, max_value = 3L, min_value = 0L)
}
for (it in 14:21) {
  df_family[[paste0("beck_", it)]] <- mk_ord(beck_som, max_value = 3L, min_value = 0L)
}

# Long for indeks
df_long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  stringsAsFactors = FALSE
)
ix_indeks <- which(df_long$family_role_f == "Indeks")
ix_kardes <- which(df_long$family_role_f == "Kardes")
g_c <- stats::rnorm(n)
for (sl in names(map)) {
  trait_c <- 0.6 * g_c + 0.4 * stats::rnorm(n)
  for (it in map[[sl]]) {
    col <- paste0("embu_c_q", sprintf("%02d", it))
    values <- numeric(nrow(df_long))
    values[ix_indeks] <- mk_ord(trait_c)
    values[ix_kardes] <- mk_ord(stats::rnorm(n))
    df_long[[col]] <- as.integer(values)
  }
}

# 4) Reliability metrics on a stub loadings frame
stub_loadings <- data.frame(
  factor_type = c(rep("general", 4), rep("specific", 4)),
  factor_label = c(rep("G", 4), rep("F_x", 4)),
  item = rep(c("i1", "i2", "i3", "i4"), 2L),
  std_loading = c(0.6, 0.65, 0.55, 0.7,  # general
    0.4, 0.45, 0.35, 0.5),                # specific
  se = NA_real_, z = NA_real_, pvalue = NA_real_,
  stringsAsFactors = FALSE
)
metrics <- omegah_compute_metrics(stub_loadings)
stopifnot(!is.null(metrics))
stopifnot(metrics$summary$omega_h > 0 & metrics$summary$omega_h < 1)
stopifnot(metrics$summary$ecv > 0 & metrics$summary$ecv < 1)
stopifnot(metrics$summary$puc >= 0 & metrics$summary$puc <= 1)
stopifnot(nrow(metrics$omega_hs) == 1L)

# 5) Pipeline (lavaan available)
if (requireNamespace("lavaan", quietly = TRUE)) {
  result <- run_reliability_generalization_pipeline(
    df_family_scored = df_family,
    df_long_scored = df_long,
    reference_subscale = "asiri_koruma"
  )
  stopifnot(!is.null(result$status))
  stopifnot(nrow(result$status) == 3L)
  stopifnot(all(c("EMBU-P", "EMBU-C", "Beck") %in% result$status$domain))
  if (any(result$status$status == "ok")) {
    stopifnot(!is.null(result$loadings))
    stopifnot(all(c("general", "specific") %in% result$loadings$factor_type))
    stopifnot(!is.null(result$metrics_summary))
    stopifnot(all(c("omega_h", "ecv", "puc") %in% names(result$metrics_summary)))
    stopifnot(!is.null(result$omega_hs))
  }
}

cat("PASS: tests/test_reliability_generalization.R\n")
