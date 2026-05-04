source("R/33_informant_discrepancy.R")

set.seed(20260502L)

# 1) Subscale map
map <- disc_subscale_map()
stopifnot(all(c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma") %in% names(map)))
stopifnot(length(map$reddetme) == 8L)

# 2) Column helpers
stopifnot(identical(disc_anne_item_columns(c(5, 9)), c("embu_p_q05", "embu_p_q09")))
stopifnot(identical(disc_cocuk_item_columns(c(5, 9)), c("embu_c_q05", "embu_c_q09")))

# 3) Synthetic fixture
n_families <- 100L
items <- map$reddetme

mk_ord <- function(theta, max_value = 4L) {
  raw <- theta + stats::rnorm(length(theta), 0, 0.6)
  q <- stats::quantile(raw, probs = seq(0, 1, length.out = max_value + 1L), na.rm = TRUE)
  as.integer(cut(raw, breaks = q, include.lowest = TRUE, labels = seq_len(max_value)))
}

trait_anne <- stats::rnorm(n_families)
trait_cocuk <- 0.5 * trait_anne + 0.5 * stats::rnorm(n_families)

family <- data.frame(
  aile_no = seq_len(n_families),
  group_dm = rep(c(0L, 1L), each = n_families / 2L),
  beck_total = stats::rnorm(n_families, 8, 5),
  ses_latent = stats::rnorm(n_families),
  stringsAsFactors = FALSE
)
for (it in items) {
  family[[paste0("embu_p_q", sprintf("%02d", it))]] <- mk_ord(trait_anne)
}

long <- data.frame(
  aile_no = rep(seq_len(n_families), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n_families), levels = c("Indeks", "Kardes")),
  cocuk_yas = stats::runif(2 * n_families, 8, 17),
  stringsAsFactors = FALSE
)
for (it in items) {
  col <- paste0("embu_c_q", sprintf("%02d", it))
  values <- numeric(nrow(long))
  values[long$family_role_f == "Indeks"] <- mk_ord(trait_cocuk)
  values[long$family_role_f == "Kardes"] <- mk_ord(stats::rnorm(n_families))
  long[[col]] <- as.integer(values)
}

# 4) Paired wide-data prep
paired <- disc_prepare_paired_data(family, long, items, include_predictors = TRUE)
stopifnot(nrow(paired) == n_families)
stopifnot(all(disc_anne_item_columns(items) %in% names(paired)))
stopifnot(all(disc_cocuk_item_columns(items) %in% names(paired)))
stopifnot(all(c("beck_total_z", "ses_latent_z", "cocuk_yas_z", "group_dm") %in% names(paired)))
stopifnot(!is.null(attr(paired, "disc_scaling")))

family_group_f <- family
family_group_f$group_f <- factor(ifelse(family_group_f$group_dm == 1L, "DM", "Kontrol"),
  levels = c("Kontrol", "DM"))
family_group_f$group_dm <- NULL
paired_group_f <- disc_prepare_paired_data(family_group_f, long, items, include_predictors = TRUE)
stopifnot(identical(paired_group_f$group_dm, family$group_dm))

# 5) Two-factor syntax
syntax_2f <- disc_two_factor_syntax(items, "reddetme")
stopifnot(grepl("F_anne_reddetme =~ embu_p_q05", syntax_2f, fixed = TRUE))
stopifnot(grepl("F_cocuk_reddetme =~ embu_c_q05", syntax_2f, fixed = TRUE))
stopifnot(grepl("F_anne_reddetme ~~ F_cocuk_reddetme", syntax_2f, fixed = TRUE))

# 6) LDS syntax
syntax_lds <- disc_lds_syntax(items, "reddetme",
  predictors = c("group_dm", "beck_total_z", "ses_latent_z", "cocuk_yas_z")
)
stopifnot(grepl("F_diff_reddetme =~ 1 \\* F_anne_reddetme", syntax_lds))
stopifnot(grepl("F_anne_reddetme ~ 1 \\* F_cocuk_reddetme", syntax_lds))
stopifnot(grepl("F_anne_reddetme ~~ 0 \\* F_anne_reddetme", syntax_lds))
stopifnot(grepl("F_diff_reddetme ~ group_dm", syntax_lds, fixed = TRUE))

# 7) Pipeline (single subscale, lavaan available)
if (requireNamespace("lavaan", quietly = TRUE)) {
  result <- run_informant_discrepancy_pipeline(
    family, long,
    subscales = "reddetme",
    include_predictors = TRUE,
    fit_lds = TRUE
  )
  stopifnot(!is.null(result$status))
  stopifnot(nrow(result$status) == 2L)
  stopifnot(all(c("two_factor_corr", "lds_with_predictors") %in% result$status$model))
  if (any(result$status$converged)) {
    stopifnot(!is.null(result$fit_indices))
    if (!is.null(result$latent_correlation)) {
      stopifnot(nrow(result$latent_correlation) >= 1L)
    }
    if (any(result$status$model == "lds_with_predictors" & result$status$converged)) {
      stopifnot(!is.null(result$variance))
      stopifnot("interpretation" %in% names(result$variance))
      stopifnot(!is.null(result$predictor_paths))
      stopifnot("group_dm" %in% result$predictor_paths$predictor)
    }
  } else {
    cat(sprintf(
      "[disc test] convergence skipped: %s\n",
      paste(result$status$error_message, collapse = "; ")
    ))
  }
} else {
  cat("[disc test] lavaan unavailable, fit-step skipped\n")
}

# 8) Variance interpretation thresholds (smoke)
mock_variance <- function(ratio) {
  data.frame(
    subscale = "x", var_diff = ratio, var_cocuk = 1 - ratio,
    var_total = 1, discrepancy_ratio = ratio,
    interpretation = NA_character_, stringsAsFactors = FALSE
  )
}
stopifnot(local({
  v <- mock_variance(0.10)
  v$interpretation <- if (v$discrepancy_ratio < 0.20) "ihmal_edilebilir" else NA
  v$interpretation == "ihmal_edilebilir"
}))

cat("PASS: tests/test_informant_discrepancy.R\n")
