# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXVI (§96-99) test paketi
# Sentetik veriyle sekil/aralik/parametre-sinir kontrolu.

source("R/10_derived_scores.R")   # embu_subscale_map / srq_first_order_map
source("R/51_pdt_effect.R")

set.seed(20260708L)

# ---- 1) Yardimci fonksiyon birim testleri --------------------------------

# Cronbach alfa: paylasilan trait -> pozitif, <= 1
mk_items <- function(trait, k, min_v = 1L, max_v = 4L) {
  m <- sapply(seq_len(k), function(j) {
    raw <- 2.5 + trait + stats::rnorm(length(trait), 0, 0.6)
    as.integer(pmin(max_v, pmax(min_v, round(raw))))
  })
  as.data.frame(m)
}
trait0 <- stats::rnorm(200)
items0 <- mk_items(trait0, 4L)
alpha0 <- pdt_cronbach_alpha(items0)
stopifnot(is.finite(alpha0), alpha0 <= 1 + 1e-9, alpha0 > 0)

# omega: NA veya (0,1] araliginda
om0 <- pdt_omega_total(items0)
stopifnot(is.na(om0) || (om0 > 0 && om0 <= 1 + 1e-9))

# RSA polinom a-parametre eslemesi: bilinen dogrusal yuzey Z = 2Xc + 3Yc
xc <- stats::rnorm(300); yc <- stats::rnorm(300)
zlin <- 2 * xc + 3 * yc + stats::rnorm(300, 0, 0.01)
a_lin <- pdt_rsa_poly_a(xc, yc, zlin)
stopifnot(abs(a_lin[["a1"]] - 5) < 0.05)   # b1 + b2 = 2 + 3
stopifnot(abs(a_lin[["a3"]] + 1) < 0.05)   # b1 - b2 = 2 - 3
stopifnot(abs(a_lin[["a2"]]) < 0.05)       # egrilik ~ 0
stopifnot(abs(a_lin[["a4"]]) < 0.05)

# TOST: buyuk n + sifira yakin r -> esdeger/onemsiz, karar gecerli kumede
tt <- pdt_tost_r(stats::rnorm(400), stats::rnorm(400), sesoi_r = 0.10)
stopifnot(tt$karar %in% c("esdeger", "onemsiz", "anlamli", "belirsiz", "yetersiz_n"))
stopifnot(is.finite(tt$r), abs(tt$r) <= 1 + 1e-9)

# Holm: 8 satir, p_holm >= p_ham
gp <- stats::setNames(c(0.01, 0.20, 0.50, 0.80), pdt_subscales())
sp <- stats::setNames(c(0.04, 0.30, 0.60, 0.90), pdt_subscales())
holm0 <- pdt_holm_table(gp, sp)
stopifnot(nrow(holm0) == 8L)
stopifnot(all(holm0$p_holm >= holm0$p_ham - 1e-9, na.rm = TRUE))

# ---- 2) Sentetik aile + long fixture --------------------------------------

n <- 120L
subs <- pdt_subscales()

fam <- data.frame(
  aile_no = seq_len(n),
  group_f = factor(rep(c("Kontrol", "DM"), each = n / 2L), levels = c("Kontrol", "DM")),
  ses_latent = stats::rnorm(n),
  age_gap = sample(1:6, n, replace = TRUE),
  cocuk_sayisi = sample(2:4, n, replace = TRUE),
  same_sex = factor(sample(c("Farkli", "Ayni"), n, replace = TRUE), levels = c("Farkli", "Ayni")),
  srq_ho_conflict_mean = stats::rnorm(n, 2.5, 0.6),
  srq_ho_rivalry_mean = stats::rnorm(n, 3.0, 0.7),
  stringsAsFactors = FALSE
)

# EMBU-C indeks + kardes maddeleri ve alt olcek ortalamalari
for (sub in subs) {
  items <- pdt_subscale_items(sub)
  trait_fam <- stats::rnorm(n)
  idx_mat <- mk_items(trait_fam, length(items))
  sib_mat <- mk_items(0.5 * trait_fam + 0.5 * stats::rnorm(n), length(items))
  for (j in seq_along(items)) {
    fam[[pdt_embu_item_columns("embu_c_idx", items[j])]] <- idx_mat[[j]]
    fam[[pdt_embu_item_columns("embu_c_sib", items[j])]] <- sib_mat[[j]]
  }
  fam[[paste0("embu_c_idx_", sub, "_mean")]] <- rowMeans(idx_mat)
  fam[[paste0("embu_c_sib_", sub, "_mean")]] <- rowMeans(sib_mat)
}

# SRQ kayirma maddeleri (indeks + kardes), 1-5 olcek
fav <- pdt_favoritism_map()
for (informant in c("srq", "srq_sib")) {
  for (ch in names(fav)) {
    trait_ch <- stats::rnorm(n)
    for (it in fav[[ch]]) {
      raw <- 3 + trait_ch + stats::rnorm(n, 0, 0.7)
      fam[[pdt_srq_item_columns(informant, it)]] <- as.integer(pmin(5L, pmax(1L, round(raw))))
    }
  }
}

# Long: aile basina 2 cocuk
long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("index", "sibling"), n), levels = c("index", "sibling")),
  group_f = factor(rep(as.character(fam$group_f), each = 2L), levels = c("Kontrol", "DM")),
  srq_ho_conflict_mean = stats::rnorm(2L * n, 2.5, 0.6),
  srq_ho_rivalry_mean = stats::rnorm(2L * n, 3.0, 0.7),
  stringsAsFactors = FALSE
)
long$aile_no_f <- factor(long$aile_no)

# ---- 3) §96 fonksiyonlari -------------------------------------------------

fam2 <- pdt_add_signed_abs(fam)
for (sub in subs) {
  s_col <- paste0("pdt_signed_", sub); a_col <- paste0("pdt_abs_", sub)
  stopifnot(all(c(s_col, a_col) %in% names(fam2)))
  ok <- !is.na(fam2[[s_col]])
  stopifnot(all(abs(fam2[[a_col]][ok] - abs(fam2[[s_col]][ok])) < 1e-9))
}

rho_tab <- pdt_rho_dd_table(fam2)
stopifnot(nrow(rho_tab) == length(subs))
# Mantiksal sinir: rho_DD ve rho'lar [-1, 1] icinde
stopifnot(all(rho_tab$rho_dd >= -1 - 1e-9 & rho_tab$rho_dd <= 1 + 1e-9, na.rm = TRUE))
stopifnot(all(rho_tab$rho_xy >= -1 - 1e-9 & rho_tab$rho_xy <= 1 + 1e-9, na.rm = TRUE))
stopifnot(all(rho_tab$rho_xx_alfa_idx <= 1 + 1e-9, na.rm = TRUE))
# ort + medyan kolonlari mevcut
stopifnot(all(c("pdt_signed_ort", "pdt_signed_medyan", "pdt_abs_ort", "pdt_abs_medyan") %in% names(rho_tab)))

# rho_DD formul dogrulamasi (bir alt olcek elle hesap)
sub1 <- "sicaklik"
items1 <- pdt_subscale_items(sub1)
idx_items1 <- pdt_embu_item_columns("embu_c_idx", items1)
sib_items1 <- pdt_embu_item_columns("embu_c_sib", items1)
axx <- pdt_cronbach_alpha(as.data.frame(lapply(fam2[idx_items1], as.numeric)))
ayy <- pdt_cronbach_alpha(as.data.frame(lapply(fam2[sib_items1], as.numeric)))
xv <- fam2[[paste0("embu_c_idx_", sub1, "_mean")]]
yv <- fam2[[paste0("embu_c_sib_", sub1, "_mean")]]
sx <- stats::sd(xv); sy <- stats::sd(yv); rxy <- stats::cor(xv, yv)
num <- sx^2 * axx + sy^2 * ayy - 2 * rxy * sx * sy
den <- sx^2 + sy^2 - 2 * rxy * sx * sy
expected_rho_dd <- num / den
got_rho_dd <- rho_tab$rho_dd[rho_tab$alt_olcek == sub1]
stopifnot(abs(got_rho_dd - expected_rho_dd) < 1e-8)

# RSA yuzey tablosu (kucuk boot)
rsa_tab <- pdt_rsa_surface_table(fam2, n_boot = 50L)
stopifnot(all(c("alt_olcek", "outcome", "parametre", "tahmin", "alt_ga", "ust_ga", "blok_p") %in% names(rsa_tab)))
stopifnot(all(c("a1", "a2", "a3", "a4") %in% unique(rsa_tab$parametre)))
ok_rsa <- rsa_tab$durum == "ok"
stopifnot(all(rsa_tab$alt_ga[ok_rsa] <= rsa_tab$ust_ga[ok_rsa] + 1e-9, na.rm = TRUE))

# Buyukluk modeli
mag <- pdt_magnitude_model(fam2)
stopifnot("group_fDM" %in% mag$terim)
gp_attr <- attr(mag, "group_p")
stopifnot(length(gp_attr) == length(subs))
mag_ok <- mag[mag$durum == "ok", , drop = FALSE]
stopifnot(all(mag_ok$alt_ga <= mag_ok$ust_ga + 1e-9, na.rm = TRUE))

# Yon testi
dir_tab <- pdt_direction_test(fam2)
stopifnot(nrow(dir_tab) == length(subs))
stopifnot(all(c("cohens_d", "d_alt_ga", "d_ust_ga", "isaret_testi_p") %in% names(dir_tab)))
sp_attr <- attr(dir_tab, "sign_p")
stopifnot(length(sp_attr) == length(subs))
ok_p <- !is.na(dir_tab$isaret_testi_p)
stopifnot(all(dir_tab$isaret_testi_p[ok_p] >= 0 & dir_tab$isaret_testi_p[ok_p] <= 1))

# ---- 4) §98 kayirma fonksiyonlari ----------------------------------------

fam3 <- pdt_add_favoritism(fam2)
stopifnot(all(c("mat_partiality_idx", "mat_partiality_sib",
                "pat_partiality_idx", "pat_partiality_sib") %in% names(fam3)))
ch_tab <- pdt_favoritism_channels(fam3)
stopifnot(all(c("kanal", "informant", "grup", "n", "ort", "medyan", "alfa_3madde", "omega_3madde") %in% names(ch_tab)))
ok_a <- !is.na(ch_tab$alfa_3madde)
stopifnot(all(ch_tab$alfa_3madde[ok_a] <= 1 + 1e-9))

icc_tab <- pdt_favoritism_icc(fam3)
stopifnot(all(c("kanal", "grup", "icc_2_1", "ba_loa_alt", "ba_loa_ust") %in% names(icc_tab)))
ok_icc <- !is.na(icc_tab$icc_2_1)
stopifnot(all(icc_tab$icc_2_1[ok_icc] >= -1 - 1e-9 & icc_tab$icc_2_1[ok_icc] <= 1 + 1e-9))
stopifnot(all(icc_tab$ba_loa_alt[!is.na(icc_tab$ba_loa_alt)] <=
              icc_tab$ba_loa_ust[!is.na(icc_tab$ba_loa_ust)] + 1e-9))

mtmm_tab <- pdt_mtmm_convergence(fam3)
stopifnot(all(c("srq_kanal", "embu_alt_olcek", "embu_metrik", "r") %in% names(mtmm_tab)))
ok_r <- !is.na(mtmm_tab$r)
stopifnot(all(mtmm_tab$r[ok_r] >= -1 - 1e-9 & mtmm_tab$r[ok_r] <= 1 + 1e-9))

# ---- 5) Tam pipeline ------------------------------------------------------

fam_pipe <- fam  # add_signed_abs/favoritism icerde yapiliyor
result <- run_phase3_pdt_effect_pipeline(
  df_family_ses = fam_pipe,
  df_long_scored = long,
  n_boot = 50L,
  sesoi_r = 0.10,
  seed = 20260708L
)

expected_tables <- c("rho_dd", "rsa_surface", "magnitude_model", "direction_test",
  "path_model", "favoritism_channels", "favoritism_group_test", "favoritism_icc",
  "mtmm_convergence", "moderation", "moderation_slopes", "tost", "holm", "target_summary")
for (nm in expected_tables) {
  stopifnot(nm %in% names(result))
  stopifnot(!is.null(result[[nm]]))
  stopifnot(nrow(result[[nm]]) >= 1L)
}

# statu kolonu ve KESIFSEL etiketi
for (nm in setdiff(expected_tables, "target_summary")) {
  stopifnot("statu" %in% names(result[[nm]]))
  stopifnot(all(grepl("KESIFSEL", result[[nm]]$statu, fixed = TRUE)))
}
stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))

# rho_DD mantiksal sinir (pipeline ciktisi)
stopifnot(all(result$rho_dd$rho_dd >= -1 - 1e-9 & result$rho_dd$rho_dd <= 1 + 1e-9, na.rm = TRUE))

# Holm 8 test
stopifnot(nrow(result$holm) == 8L)

# path_model std_beta (ok satirlar) sonlu ve GA tutarli
pm <- result$path_model
if ("std_beta" %in% names(pm)) {
  pm_ok <- pm[pm$durum == "ok" & !is.na(pm$std_beta), , drop = FALSE]
  if (nrow(pm_ok) > 0L) {
    stopifnot(all(is.finite(pm_ok$std_beta)))
    stopifnot(all(pm_ok$alt_ga <= pm_ok$ust_ga + 1e-9))
    stopifnot(all(pm_ok$icc >= -1e-9 & pm_ok$icc <= 1 + 1e-9))
  }
}

# tost karar kolonu gecerli kumede
stopifnot(all(result$tost$karar %in%
  c("esdeger", "onemsiz", "anlamli", "belirsiz", "yetersiz_n")))

cat("PASS: tests/test_pdt_effect.R\n")
