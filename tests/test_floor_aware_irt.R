source("R/35_floor_aware_irt.R")

set.seed(20260504L)

# 1) Subscale map / column helpers
map <- floor_irt_subscale_map()
stopifnot(length(map$reddetme) == 8L)
stopifnot(identical(floor_irt_anne_columns(c(5, 9)), c("embu_p_q05", "embu_p_q09")))
stopifnot(identical(floor_irt_cocuk_columns(c(5, 9)), c("embu_c_q05", "embu_c_q09")))

# 2) Floor summary on synthetic data
n <- 200L
items <- map$reddetme
mk_floor_heavy <- function(theta, max_value = 4L, floor_pull = 0.7) {
  raw <- theta + stats::rnorm(length(theta), 0, 0.6) - floor_pull
  q <- stats::quantile(raw, probs = seq(0, 1, length.out = max_value + 1L), na.rm = TRUE)
  as.integer(cut(raw, breaks = q, include.lowest = TRUE, labels = seq_len(max_value)))
}
trait <- stats::rnorm(n)
df_anne <- data.frame(
  aile_no = seq_len(n),
  group_dm = rep(c(0L, 1L), each = n / 2L),
  stringsAsFactors = FALSE
)
for (it in items) {
  df_anne[[paste0("embu_p_q", sprintf("%02d", it))]] <- mk_floor_heavy(trait)
}

cols_anne <- floor_irt_anne_columns(items)
items_data <- floor_irt_extract_items(df_anne, cols_anne)
floor_summary <- floor_irt_floor_summary(items_data)
stopifnot(nrow(floor_summary) == length(items))
stopifnot(all(floor_summary$n_floor >= 0L))
stopifnot(all(floor_summary$floor_share >= 0 & floor_summary$floor_share <= 1))

# 3) GRM fit (mirt available)
if (requireNamespace("mirt", quietly = TRUE)) {
  std <- floor_irt_fit_grm(items_data, dentype = "Gaussian")
  stopifnot(identical(std$status, "ok"))
  flr <- floor_irt_fit_grm(items_data, dentype = "empiricalhist")
  stopifnot(identical(flr$status, "ok"))
  std_params <- floor_irt_item_parameters(std, "reddetme", "anne")
  stopifnot(!is.null(std_params))
  stopifnot(nrow(std_params) == length(items))
  stopifnot(all(c("subscale", "informant", "dentype", "item") %in% names(std_params)))
  th_std <- floor_irt_score_thetas(std)
  th_flr <- floor_irt_score_thetas(flr)
  stopifnot(length(th_std) == n)
  comp <- floor_irt_compare_thetas(th_std, th_flr, "reddetme", "anne")
  stopifnot(comp$n == n)
  stopifnot(!is.na(comp$pearson_r))
  delta <- floor_irt_group_delta(th_flr, df_anne$group_dm, "reddetme", "anne")
  stopifnot(delta$n_kontrol == n / 2L)
  stopifnot(delta$n_dm == n / 2L)
} else {
  cat("[floor_irt test] mirt unavailable, skipping fit-step\n")
}

# 4) Pipeline (subscale='reddetme', informant='anne' tek path)
df_long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n), levels = c("Indeks", "Kardes")),
  group_dm = rep(rep(c(0L, 1L), each = n / 2L), each = 2L),
  stringsAsFactors = FALSE
)
for (it in items) {
  df_long[[paste0("embu_c_q", sprintf("%02d", it))]] <- mk_floor_heavy(stats::rnorm(nrow(df_long)))
}

if (requireNamespace("mirt", quietly = TRUE)) {
  result <- run_floor_aware_irt_pipeline(
    df_family_scored = df_anne,
    df_long_scored = df_long,
    subscales = "reddetme",
    informants = c("anne", "indeks")
  )
  stopifnot(!is.null(result$status))
  stopifnot(nrow(result$status) == 4L)  # 1 alt olcek x 2 informant x 2 model
  stopifnot(all(c("standard_grm", "floor_aware_grm") %in% result$status$model))
  stopifnot(all(c("anne", "indeks") %in% result$status$informant))
  stopifnot(!is.null(result$theta_comparison))
  stopifnot(nrow(result$theta_comparison) == 2L)
  stopifnot(!is.null(result$group_delta))
  stopifnot(nrow(result$group_delta) == 2L)
  stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))
}

cat("PASS: tests/test_floor_aware_irt.R\n")
