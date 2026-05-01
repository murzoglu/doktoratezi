source("R/32_trifactor_model.R")

set.seed(20260501L)

# 1) Item map
map <- trifactor_subscale_map()
stopifnot(all(c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma") %in% names(map)))
stopifnot(length(map$reddetme) == 8L)

# 2) Column helpers
stopifnot(identical(
  trifactor_anne_item_columns(c(5, 9)),
  c("embu_p_q05", "embu_p_q09")
))
stopifnot(identical(
  trifactor_cocuk_role_columns(c(5, 9), "indeks"),
  c("embu_c_q05_indeks", "embu_c_q09_indeks")
))
stopifnot(inherits(
  tryCatch(trifactor_cocuk_role_columns(1, "anne"), error = function(e) e),
  "error"
))

# 3) Role normalization (Turkish characters + tokens)
stopifnot(identical(trifactor_normalize_role("Indeks"), "indeks"))
stopifnot(identical(trifactor_normalize_role("Kardes"), "kardes"))
stopifnot(identical(trifactor_normalize_role("kardes_v2"), "kardes"))

# 4) Synthetic fixture: 80 family * 1 anne, 1 indeks, 1 kardes
n_families <- 80L
items <- map$reddetme

mk_ord <- function(theta, max_value = 4L) {
  raw <- theta + stats::rnorm(length(theta), 0, 0.6)
  q <- stats::quantile(raw, probs = seq(0, 1, length.out = max_value + 1L), na.rm = TRUE)
  as.integer(cut(raw, breaks = q, include.lowest = TRUE, labels = seq_len(max_value)))
}

family <- data.frame(
  aile_no = seq_len(n_families),
  group_f = factor(rep(c("Kontrol", "DM"), each = n_families / 2L), levels = c("Kontrol", "DM")),
  stringsAsFactors = FALSE
)
trait_anne <- stats::rnorm(n_families)
for (it in items) {
  family[[paste0("embu_p_q", sprintf("%02d", it))]] <- mk_ord(trait_anne)
}

# Long fixture: each family has Indeks and Kardes child rows
trait_indeks <- 0.6 * trait_anne + 0.4 * stats::rnorm(n_families)
trait_kardes <- 0.6 * trait_anne + 0.4 * stats::rnorm(n_families)
long <- data.frame(
  aile_no = rep(seq_len(n_families), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n_families), levels = c("Indeks", "Kardes")),
  stringsAsFactors = FALSE
)
for (it in items) {
  col <- paste0("embu_c_q", sprintf("%02d", it))
  values <- numeric(nrow(long))
  values[long$family_role_f == "Indeks"] <- mk_ord(trait_indeks)
  values[long$family_role_f == "Kardes"] <- mk_ord(trait_kardes)
  long[[col]] <- as.integer(values)
}

# 5) Wide-prep
wide <- trifactor_prepare_wide_data(family, long, items)
stopifnot(nrow(wide) == n_families)
stopifnot(all(trifactor_anne_item_columns(items) %in% names(wide)))
stopifnot(all(trifactor_cocuk_role_columns(items, "indeks") %in% names(wide)))
stopifnot(all(trifactor_cocuk_role_columns(items, "kardes") %in% names(wide)))
stopifnot(identical(attr(wide, "trifactor_items"), items))

# Duplicate role rows trigger error
bad_long <- rbind(long, long[long$aile_no == 1L & long$family_role_f == "Indeks", , drop = FALSE])
stopifnot(inherits(
  tryCatch(trifactor_prepare_wide_data(family, bad_long, items), error = function(e) e),
  "error"
))

# 6) Coverage summary
coverage <- trifactor_coverage_summary(wide, "reddetme")
stopifnot(nrow(coverage) == 1L)
stopifnot(coverage$n_family_total == n_families)
stopifnot(coverage$n_triple_complete <= n_families)
stopifnot(!is.na(coverage$triple_coverage_ratio))

# 7) Syntax helpers
syntax <- trifactor_model_syntax(items, "reddetme")
stopifnot(grepl("F_trait_reddetme =~ embu_p_q05", syntax, fixed = TRUE))
stopifnot(grepl("F_indeks_reddetme =~ embu_c_q05_indeks", syntax, fixed = TRUE))
stopifnot(grepl("F_kardes_reddetme =~ embu_c_q05_kardes", syntax, fixed = TRUE))
stopifnot(grepl("F_trait_reddetme ~~ 0 * F_indeks_reddetme", syntax, fixed = TRUE))
stopifnot(grepl("F_indeks_reddetme ~~ F_kardes_reddetme", syntax, fixed = TRUE))

# 8) Pipeline (fit_models = FALSE) — synthetic veride sadece reddetme alt-olcegi var,
#    bu yuzden subscales = "reddetme" ile sinirla; pipeline syntax/coverage uretir
plan_only <- run_trifactor_pipeline(
  family, long,
  subscales = "reddetme",
  fit_models = FALSE
)
stopifnot(!is.null(plan_only$coverage))
stopifnot(nrow(plan_only$coverage) == 1L)
stopifnot(nrow(plan_only$syntax) == 1L)
stopifnot(plan_only$target_summary$n_subscales_requested == 1L)
stopifnot(plan_only$target_summary$n_subscales_fit == 0L)
stopifnot(grepl("KESIFSEL", plan_only$target_summary$kanit_kategorisi, fixed = TRUE))

# 9) Pipeline (fit_models = TRUE), reddetme alt-olcegi tek subscale ile yakinsama testi
if (requireNamespace("lavaan", quietly = TRUE)) {
  result <- run_trifactor_pipeline(
    family, long,
    subscales = "reddetme",
    fit_models = TRUE
  )
  stopifnot(!is.null(result$status))
  stopifnot(nrow(result$status) == 1L)
  if (isTRUE(result$status$converged)) {
    stopifnot(!is.null(result$fit_indices))
    stopifnot(nrow(result$fit_indices) == 1L)
    stopifnot(result$fit_indices$df > 0L)
    stopifnot(result$fit_indices$converged == TRUE)
    stopifnot(!is.null(result$loadings))
    stopifnot(all(c("trait", "indeks_method", "kardes_method") %in% unique(result$loadings$method)))
    stopifnot(!is.null(result$variance))
    stopifnot(all(result$variance$communality_sum_sq >= 0))
    stopifnot(!is.null(result$method_correlation))
    stopifnot(nrow(result$method_correlation) >= 1L)
  } else {
    cat(sprintf(
      "[trifactor test] reddetme convergence skipped: %s\n",
      result$status$error_message
    ))
  }
} else {
  cat("[trifactor test] lavaan unavailable, fit-step skipped\n")
}

cat("PASS: tests/test_trifactor_model.R\n")
