source("R/37_esem_embu.R")

set.seed(20260506L)

# 1) Subscale map / column helpers
map <- esem_subscale_map()
stopifnot(length(map) == 4L)
stopifnot(identical(esem_anne_columns(c(5, 9)), c("embu_p_q05", "embu_p_q09")))

# 2) CFA syntax
syntax_p <- esem_cfa_syntax("embu_p", map)
stopifnot(grepl("sicaklik =~ embu_p_q01", syntax_p, fixed = TRUE))
stopifnot(grepl("reddetme =~ embu_p_q05", syntax_p, fixed = TRUE))

# 3) Target matrix
target_p <- esem_target_matrix("embu_p", map)
stopifnot(nrow(target_p) == 29L)
stopifnot(ncol(target_p) == 4L)

# 4) Synthetic data — kismi-iyi 4-faktor yapisi
n <- 300L
mk_ord <- function(theta, max_value = 4L, min_value = 1L) {
  raw <- theta + stats::rnorm(length(theta), 0, 0.6)
  q <- stats::quantile(raw, probs = seq(0, 1, length.out = max_value - min_value + 2L), na.rm = TRUE)
  as.integer(cut(raw, breaks = q, include.lowest = TRUE, labels = seq(min_value, max_value)))
}
df_family <- data.frame(aile_no = seq_len(n), stringsAsFactors = FALSE)
for (sl in names(map)) {
  trait <- stats::rnorm(n)
  for (it in map[[sl]]) {
    df_family[[paste0("embu_p_q", sprintf("%02d", it))]] <- mk_ord(trait)
  }
}

df_long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  stringsAsFactors = FALSE
)
ix_indeks <- which(df_long$family_role_f == "Indeks")
ix_kardes <- which(df_long$family_role_f == "Kardes")
for (sl in names(map)) {
  trait_c <- stats::rnorm(n)
  for (it in map[[sl]]) {
    col <- paste0("embu_c_q", sprintf("%02d", it))
    values <- numeric(nrow(df_long))
    values[ix_indeks] <- mk_ord(trait_c)
    values[ix_kardes] <- mk_ord(stats::rnorm(n))
    df_long[[col]] <- as.integer(values)
  }
}

# 5) Cross-loading summary on stub
stub_loadings <- data.frame(
  domain = "X", item = rep(c("i1", "i2", "i3", "i4", "i5"), each = 4L),
  target_subscale = rep("a", 20L),
  factor_index = rep(1:4, 5L),
  factor_label = rep(sprintf("F%d", 1:4), 5L),
  loading = c(0.7, 0.05, -0.02, 0.03,
              0.6, 0.1, -0.05, 0.04,
              0.5, 0.15, 0.05, -0.05,
              0.4, 0.2, 0.1, 0.05,
              0.7, 0.05, 0.02, -0.03),
  rotation = "geomin",
  stringsAsFactors = FALSE
)
sum_x <- esem_cross_loading_summary(stub_loadings)
stopifnot(!is.null(sum_x))
stopifnot(sum_x$share_abs_below_small > 0)
stopifnot(sum_x$share_abs_above_moderate > 0)

# 6) Pipeline
if (requireNamespace("lavaan", quietly = TRUE)) {
  result <- run_esem_embu_pipeline(
    df_family_scored = df_family,
    df_long_scored = df_long,
    n_factors = 4L,
    rotation = "geomin"
  )
  stopifnot(!is.null(result$status))
  stopifnot(all(c("EMBU-P", "EMBU-C") %in% result$status$domain))
  stopifnot(all(c("cfa_baseline", "esem_geomin") %in% result$status$model))
  if (any(result$status$status == "ok")) {
    stopifnot(!is.null(result$fit_indices))
  }
}

cat("PASS: tests/test_esem_embu.R\n")
