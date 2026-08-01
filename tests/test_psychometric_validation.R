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

# --- KIA/SRQ + Beck guvenirlik tablolari (Ek 7 kaynak-tekilligi) ---
srq_reliability <- psychval_srq_reliability_table(
  srq_fixture,
  prefix = "srq",
  scale = "KIA/SRQ test"
)
stopifnot(nrow(srq_reliability) == 5L)
stopifnot(all(c(
  "scale", "subscale", "subscale_label", "n_items", "n_complete",
  "alpha_raw", "alpha_std", "alpha_ci_lower", "alpha_ci_upper",
  "omega_total", "omega_h", "mean_interitem_r"
) %in% names(srq_reliability)))
stopifnot(identical(
  srq_reliability$subscale,
  c("sicaklik_yakinlik", "statu_guc", "catisma", "rekabet", "toplam")
))
stopifnot(identical(
  srq_reliability$n_items,
  c(21L, 12L, 6L, 9L, 48L)
))

beck_map <- psychval_beck_block_map()
stopifnot(identical(names(beck_map), c("toplam", "bilissel_afektif", "somatik")))
stopifnot(identical(lengths(beck_map), c(toplam = 21L, bilissel_afektif = 13L, somatik = 8L)))
# Bilissel-afektif (q01-q13) ve somatik (q14-q21) bloklari ortusmez ve toplami kapsar
stopifnot(length(intersect(beck_map$bilissel_afektif, beck_map$somatik)) == 0L)
stopifnot(identical(
  sort(c(beck_map$bilissel_afektif, beck_map$somatik)),
  beck_map$toplam
))

beck_fixture <- as.data.frame(matrix(rep(0:3, length.out = 10 * 21), nrow = 10))
names(beck_fixture) <- paste0("beck_", 1:21)
beck_reliability <- psychval_beck_reliability_table(
  beck_fixture,
  prefix = "beck",
  scale = "BDI test"
)
stopifnot(nrow(beck_reliability) == 3L)
stopifnot(identical(beck_reliability$n_items, c(21L, 13L, 8L)))
stopifnot(all(beck_reliability$scale == "BDI test"))

# --- Skor duzeyi dagilim tablosu: taban/tavan yon-savi ---
dist_fixture <- data.frame(
  sicaklik_mean = c(1, 1, 2.5, 4, NA),
  reddetme_mean = c(1, 2, 3, 4, 4)
)
dist_tbl <- psychval_score_distribution_table(
  dist_fixture,
  c("sicaklik_mean", "reddetme_mean"),
  scale = "EMBU test",
  score_min = 1,
  score_max = 4,
  labels = c("Sicaklik", "Reddetme")
)
stopifnot(nrow(dist_tbl) == 2L)
stopifnot(all(c(
  "scale", "score", "score_label", "n", "missing_n", "mean", "sd", "median",
  "iqr", "min", "max", "skew", "kurtosis", "floor_pct", "ceiling_pct"
) %in% names(dist_tbl)))
stopifnot(dist_tbl$n[dist_tbl$score == "sicaklik_mean"] == 4L)
stopifnot(dist_tbl$missing_n[dist_tbl$score == "sicaklik_mean"] == 1L)
# 4 gecerli degerin 2'si tabanda (1), 1'i tavanda (4)
stopifnot(abs(dist_tbl$floor_pct[dist_tbl$score == "sicaklik_mean"] - 50) < 1e-8)
stopifnot(abs(dist_tbl$ceiling_pct[dist_tbl$score == "sicaklik_mean"] - 25) < 1e-8)
stopifnot(abs(dist_tbl$ceiling_pct[dist_tbl$score == "reddetme_mean"] - 40) < 1e-8)
# Taban ve tavan oranlari 0-100 bandinda kalir
stopifnot(all(dist_tbl$floor_pct >= 0 & dist_tbl$floor_pct <= 100))
stopifnot(all(dist_tbl$ceiling_pct >= 0 & dist_tbl$ceiling_pct <= 100))

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

# --- Kriter gecerligi FDR yon-savlari (Sayisal Butunluk kaidesi) ---
# Uretici artefakt varsa: (a) BH-FDR duzeltilmis p ham p'den kucuk olamaz
# (monotonluk), (b) 14 korelasyon ailesinde FDR sonrasi anlamlilik oruntusu
# metin/tablo ile ayni sayida sonucu anlamli birakmalidir.
validity_csv <- file.path("outputs", "tables", "psychval_validity_correlations.csv")
if (file.exists(validity_csv)) {
  vd <- utils::read.csv(validity_csv, check.names = FALSE, stringsAsFactors = FALSE)
  stopifnot("p_adjusted" %in% names(vd))
  stopifnot(nrow(vd) == 14L)
  finite_rows <- is.finite(vd$p_value) & is.finite(vd$p_adjusted)
  # (a) BH monotonlugu: duzeltilmis p >= ham p (kucuk numerik tolerans)
  stopifnot(all(vd$p_adjusted[finite_rows] >= vd$p_value[finite_rows] - 1e-9))
  # (b) 4.2 metninde raporlanan 6 anlamli korelasyon FDR sonrasi da anlamli;
  #     6 anlamli / 8 anlamsiz oruntusu metin ile birebir tutarli olmalidir.
  stopifnot(sum(vd$p_adjusted < 0.05, na.rm = TRUE) == 6L)
}

# --- KIA/SRQ + Beck guvenirlik artefakti yon-savlari ---
# Ek 7 bu artefakti dogrudan render eder; alfa nokta kestirimi kendi %95 guven
# araliginin icinde kalmali ve katsayilar teorik ust sinira uymalidir.
scale_rel_csv <- file.path("outputs", "tables", "psychval_reliability_srq_beck.csv")
if (file.exists(scale_rel_csv)) {
  sr <- utils::read.csv(scale_rel_csv, check.names = FALSE, stringsAsFactors = FALSE)
  stopifnot(all(c(
    "scale", "subscale", "n_items", "n_complete", "alpha_raw",
    "alpha_ci_lower", "alpha_ci_upper", "omega_total", "mean_interitem_r"
  ) %in% names(sr)))
  stopifnot(nrow(sr) == 8L)
  stopifnot(all(sr$n_items > 1L))
  ci_rows <- is.finite(sr$alpha_raw) & is.finite(sr$alpha_ci_lower) & is.finite(sr$alpha_ci_upper)
  stopifnot(all(sr$alpha_ci_lower[ci_rows] <= sr$alpha_raw[ci_rows] + 1e-9))
  stopifnot(all(sr$alpha_raw[ci_rows] <= sr$alpha_ci_upper[ci_rows] + 1e-9))
  stopifnot(all(sr$alpha_raw[is.finite(sr$alpha_raw)] <= 1 + 1e-9))
  omega_rows <- is.finite(sr$omega_total)
  stopifnot(all(sr$omega_total[omega_rows] <= 1 + 1e-9))
}

# --- Skor dagilimi artefakti yon-savlari ---
score_dist_csv <- file.path("outputs", "tables", "psychval_score_distributions.csv")
if (file.exists(score_dist_csv)) {
  sd_tbl <- utils::read.csv(score_dist_csv, check.names = FALSE, stringsAsFactors = FALSE)
  stopifnot(all(c(
    "scale", "score", "n", "mean", "sd", "min", "max", "floor_pct", "ceiling_pct"
  ) %in% names(sd_tbl)))
  stopifnot(all(sd_tbl$n > 0L))
  ok <- is.finite(sd_tbl$mean) & is.finite(sd_tbl$min) & is.finite(sd_tbl$max)
  stopifnot(all(sd_tbl$min[ok] <= sd_tbl$mean[ok] + 1e-9))
  stopifnot(all(sd_tbl$mean[ok] <= sd_tbl$max[ok] + 1e-9))
  pct_ok <- is.finite(sd_tbl$floor_pct) & is.finite(sd_tbl$ceiling_pct)
  stopifnot(all(sd_tbl$floor_pct[pct_ok] + sd_tbl$ceiling_pct[pct_ok] <= 100 + 1e-9))
}

cat("Psychometric validation helper tests passed\n")
