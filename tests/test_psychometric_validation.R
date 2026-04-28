source("R/06_psychometric_validation.R")

map <- psychval_embu_subscale_map()
stopifnot(identical(
  names(map),
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
))
stopifnot(identical(lengths(map), c(
  sicaklik = 9L,
  asiri_koruma = 7L,
  reddetme = 8L,
  karsilastirma = 5L
)))
stopifnot(identical(
  psychval_item_columns("embu_p", map$reddetme),
  c(
    "embu_p_q05", "embu_p_q09", "embu_p_q10", "embu_p_q12",
    "embu_p_q16", "embu_p_q21", "embu_p_q22", "embu_p_q28"
  )
))

make_psychval_fixture <- function() {
  items <- as.data.frame(matrix(rep(1:4, length.out = 8 * 29), nrow = 8))
  names(items) <- paste0("embu_p_q", sprintf("%02d", 1:29))
  items$embu_p_q01 <- c(1, 2, 3, 4, 1, 2, 3, NA)
  items$embu_p_q03 <- c(1, 2, 3, 4, 1, 2, 3, 4)
  items$embu_p_q05 <- c(1, 1, 1, 2, 2, 3, 4, NA)

  data.frame(
    aile_no = seq_len(8),
    group = rep(c("DM", "Kontrol"), each = 4),
    items,
    check.names = FALSE
  )
}

fixture <- make_psychval_fixture()

desc <- psychval_item_descriptives(
  fixture,
  c("embu_p_q01", "embu_p_q05"),
  item_min = 1,
  item_max = 4,
  form = "EMBU-P"
)
stopifnot(nrow(desc) == 2)
stopifnot(all(c(
  "form", "item", "n", "mean", "sd", "median", "iqr",
  "skew", "kurtosis", "floor_pct", "ceiling_pct", "missing_pct"
) %in% names(desc)))
stopifnot(desc$floor_pct[desc$item == "embu_p_q05"] > 40)
stopifnot(desc$missing_pct[desc$item == "embu_p_q01"] == 12.5)

scores <- psychval_score_subscales(
  fixture,
  prefix = "embu_p",
  id_cols = c("aile_no", "group"),
  min_valid_ratio = 0.80
)
stopifnot(all(c(
  "sicaklik_mean", "asiri_koruma_mean", "reddetme_mean",
  "karsilastirma_mean", "sicaklik_valid_n", "sicaklik_sum_complete"
) %in% names(scores)))
stopifnot(nrow(scores) == nrow(fixture))
stopifnot(!is.na(scores$sicaklik_mean[8]))
stopifnot(is.na(scores$sicaklik_sum_complete[8]))

reliability <- psychval_reliability_table(
  fixture,
  prefix = "embu_p",
  form = "EMBU-P"
)
stopifnot(nrow(reliability) == 4)
stopifnot(all(c(
  "form", "subscale", "n_items", "n_complete",
  "alpha_raw", "alpha_std", "alpha_ci_lower", "alpha_ci_upper",
  "omega_total", "omega_h", "mean_interitem_r"
) %in% names(reliability)))
stopifnot(identical(
  reliability$n_items[match("reddetme", reliability$subscale)],
  8L
))

srq_map <- psychval_srq_subscale_map()
stopifnot(identical(
  names(srq_map),
  c("sicaklik_yakinlik", "statu_guc", "catisma", "rekabet")
))
stopifnot(identical(lengths(srq_map), c(
  sicaklik_yakinlik = 21L,
  statu_guc = 12L,
  catisma = 6L,
  rekabet = 9L
)))

srq_fixture <- as.data.frame(matrix(rep(1:5, length.out = 8 * 48), nrow = 8))
names(srq_fixture) <- paste0("srq_", 1:48)
srq_scores <- psychval_score_srq_subscales(
  cbind(aile_no = seq_len(8), srq_fixture),
  prefix = "srq",
  id_cols = "aile_no"
)
stopifnot(all(paste0(names(srq_map), "_mean") %in% names(srq_scores)))
stopifnot(nrow(srq_scores) == 8)

collapsed_binary <- psychval_collapse_likert_frame(
  fixture,
  c("embu_p_q01", "embu_p_q05"),
  scheme = "binary_floor"
)
stopifnot(identical(sort(unique(stats::na.omit(unlist(collapsed_binary)))), c(1, 2)))
stopifnot(collapsed_binary$embu_p_q01[1] == 1)
stopifnot(collapsed_binary$embu_p_q01[2] == 2)

collapsed_3cat <- psychval_collapse_likert_frame(
  fixture,
  c("embu_p_q01", "embu_p_q05"),
  scheme = "upper_3cat"
)
stopifnot(max(collapsed_3cat$embu_p_q01, na.rm = TRUE) == 3)
stopifnot(collapsed_3cat$embu_p_q01[4] == 3)

model_without_q12 <- psychval_lavaan_model(
  "embu_p",
  model = "four_factor",
  exclude_items = 12
)
stopifnot(!grepl("embu_p_q12", model_without_q12, fixed = TRUE))
stopifnot(grepl("reddetme =~", model_without_q12, fixed = TRUE))

bifactor_model <- psychval_lavaan_model("embu_p", model = "bifactor")
stopifnot(grepl("general =~", bifactor_model, fixed = TRUE))
stopifnot(grepl("general ~~ 0*sicaklik", bifactor_model, fixed = TRUE))

cat("Psychometric validation helper tests passed\n")
