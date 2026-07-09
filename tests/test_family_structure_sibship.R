# [KESIFSEL - POST-HOC] Faz III KISIM XXXIX (§107-109) sentetik-veri sekil/aralik testi
source("R/54_family_structure_sibship.R")

set.seed(20260708L)

# ---- 1) Yardimci fonksiyonlar ----
stopifnot(identical(fam_struct_embu_subscales(),
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")))
stopifnot(identical(fam_struct_srq_dims(), c("warmth", "status", "conflict", "rivalry")))
stopifnot(grepl("KESIFSEL", fam_struct_status_label(), fixed = TRUE))

z <- fam_struct_scale(c(1, 2, 3, 4, 5))
stopifnot(abs(mean(z)) < 1e-8, abs(stats::sd(z) - 1) < 1e-8)
stopifnot(all(is.na(fam_struct_scale(rep(3, 5)))))  # sifir varyans -> NA

# TOST korelasyon esdegerlik: p in [0,1]; sifira yakin buyuk n -> esdeger
t_null <- fam_struct_tost_r(r = 0.00, n = 1000L, sesoi = 0.10)
stopifnot(t_null$p >= 0, t_null$p <= 1)
stopifnot(identical(t_null$decision, "esdeger(|r|<SESOI)"))
# n=200'de +-.10 sinirlari cok genis -> esdeverlik SONUCLANAMAZ (dogru davranis)
t_wide <- fam_struct_tost_r(r = 0.02, n = 200L, sesoi = 0.10)
stopifnot(identical(t_wide$decision, "esdeger_degil"))
t_big <- fam_struct_tost_r(r = 0.60, n = 200L, sesoi = 0.10)
stopifnot(identical(t_big$decision, "esdeger_degil"))
stopifnot(is.na(fam_struct_tost_r(r = 0.1, n = 3L)$p))  # yetersiz n

# ---- 2) Sentetik veri fixture ----
n <- 160L
srq_dims <- fam_struct_srq_dims()
embu_subs <- fam_struct_embu_subscales()

family <- data.frame(
  aile_no = seq_len(n),
  group = rep(c("DM", "Kontrol"), length.out = n),
  medeni_durum = c(rep(0L, n - 3L), 2L, 2L, 0L),
  es_sag = c(rep(1L, n - 1L), 0L),
  cocuk_sayisi = sample(2:5, n, replace = TRUE),
  katilimci_cocuk_sirasi = sample(1:3, n, replace = TRUE),
  kardes_sirasi = sample(1:3, n, replace = TRUE),
  cocuk_yas = round(stats::runif(n, 8, 17)),
  kardes_yas = round(stats::runif(n, 8, 17)),
  katilimci_cocuk_cinsiyet = sample(0:1, n, replace = TRUE),
  kardes_cinsiyet = sample(0:1, n, replace = TRUE),
  stringsAsFactors = FALSE
)
# EMBU-C idx/sib alt-olcek ortalamalari (1-4 araligi)
for (sub in embu_subs) {
  base <- stats::rnorm(n)
  family[[paste0("embu_c_idx_", sub, "_mean")]] <-
    pmin(4, pmax(1, 2.5 + 0.4 * base + stats::rnorm(n, 0, 0.4)))
  family[[paste0("embu_c_sib_", sub, "_mean")]] <-
    pmin(4, pmax(1, 2.5 + 0.4 * base + stats::rnorm(n, 0, 0.4)))
}
# SRQ ust-boyut idx/sib ortalamalari (1-5 araligi), pozitif intrapair kovaryans
for (dim in srq_dims) {
  shared <- stats::rnorm(n)
  family[[paste0("srq_ho_", dim, "_mean")]] <-
    pmin(5, pmax(1, 3 + 0.6 * shared + stats::rnorm(n, 0, 0.5)))
  family[[paste0("srq_sib_ho_", dim, "_mean")]] <-
    pmin(5, pmax(1, 3 + 0.6 * shared + stats::rnorm(n, 0, 0.5)))
}

# Long fixture (indeks + kardes)
long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  aile_no_f = factor(rep(seq_len(n), each = 2L)),
  family_role_f = factor(rep(c("index", "sibling"), n), levels = c("index", "sibling")),
  group = rep(family$group, each = 2L),
  cocuk_yas = round(stats::runif(2L * n, 8, 17)),
  stringsAsFactors = FALSE
)
for (sub in embu_subs) {
  long[[paste0("embu_c_", sub, "_mean")]] <- pmin(4, pmax(1, stats::rnorm(2L * n, 2.5, 0.5)))
}

# ---- 3) §107 tek-ebeveyn betimsel ----
sp <- fam_struct_single_parent_descriptive(family)
stopifnot(all(c("gosterge", "n", "n_dm", "n_kontrol", "aciklama", "statu") %in% names(sp)))
tek <- sp[sp$gosterge == "tek_ebeveyn (birlesik)", ]
stopifnot(nrow(tek) == 1L)
stopifnot(tek$n == 3L)  # 2 bosanmis + 1 dul
stopifnot(all(sp$n >= 0), all(sp$n <= n))
stopifnot(any(grepl("YAPILAMAZ", sp$aciklama)))

# ---- 4) §108a within-family kontrast ----
bw <- fam_struct_birth_order_within(family)
stopifnot(all(c("boyut", "terim", "rol", "n", "tahmin", "ci_alt", "ci_ust",
  "std_beta", "t", "p", "statu") %in% names(bw)))
stopifnot(all(bw$boyut %in% embu_subs))
bw_ok <- bw[bw$statu_kosum == "ok", ]
stopifnot(nrow(bw_ok) > 0L)
# yas kontrolu her alt-olcekte mevcut olmali
stopifnot(any(bw_ok$rol == "yas_kontrolu"))
stopifnot(any(bw_ok$rol == "yordayici"))
# p ve GA mantiksal sinirlar
stopifnot(all(bw_ok$p >= 0 & bw_ok$p <= 1, na.rm = TRUE))
stopifnot(all(bw_ok$ci_alt <= bw_ok$ci_ust, na.rm = TRUE))

# ---- 5) §108b sibship dilution ----
sd_tab <- fam_struct_sibship_dilution(long, family)
stopifnot(all(c("boyut", "yordayici", "n_gozlem", "n_aile", "tahmin", "ci_alt",
  "ci_ust", "std_beta", "p", "statu") %in% names(sd_tab)))
stopifnot(all(sd_tab$boyut %in% c("sicaklik", "asiri_koruma")))
sd_ok <- sd_tab[sd_tab$statu_kosum == "ok", ]
if (nrow(sd_ok) > 0L) {
  stopifnot(all(sd_ok$ci_alt <= sd_ok$ci_ust, na.rm = TRUE))
  stopifnot(all(sd_ok$p >= 0 & sd_ok$p <= 1, na.rm = TRUE))
  stopifnot(all(sd_ok$n_gozlem > 0), all(sd_ok$n_aile > 0))
}

# ---- 6) §109 reciprocity: intrapair r ve dz sinirlar ----
rc <- fam_struct_reciprocity(family)
stopifnot(all(c("boyut", "n", "intrapair_r", "r_ci_alt", "r_ci_ust", "cohen_dz",
  "tost_p", "tost_karar", "statu") %in% names(rc)))
rc_ok <- rc[rc$statu_kosum == "ok", ]
stopifnot(nrow(rc_ok) == length(srq_dims))
# r in [-1, 1]; GA in [-1, 1]; TOST p in [0,1]
stopifnot(all(rc_ok$intrapair_r >= -1 & rc_ok$intrapair_r <= 1))
stopifnot(all(rc_ok$r_ci_alt >= -1 & rc_ok$r_ci_ust <= 1, na.rm = TRUE))
stopifnot(all(rc_ok$tost_p >= 0 & rc_ok$tost_p <= 1, na.rm = TRUE))
stopifnot(all(rc_ok$tost_karar %in% c("esdeger(|r|<SESOI)", "esdeger_degil")))

# ---- 7) §109 varyans ayrisimi: oranlar ve sinirlar ----
vd <- fam_struct_variance_decomposition(family)
stopifnot(all(c("boyut", "var_duad_ort", "var_duad_fark", "oran_common_fate",
  "oran_duad_ici", "mutekabiliyet_orani", "statu") %in% names(vd)))
vd_ok <- vd[vd$statu_kosum == "ok", ]
stopifnot(nrow(vd_ok) == length(srq_dims))
# oran_common_fate + oran_duad_ici == 1
stopifnot(all(abs((vd_ok$oran_common_fate + vd_ok$oran_duad_ici) - 1) < 1e-8))
stopifnot(all(vd_ok$oran_common_fate >= 0 & vd_ok$oran_common_fate <= 1))
stopifnot(all(vd_ok$var_duad_ort >= 0), all(vd_ok$var_duad_fark >= 0))
# rho_DD analogu (mutekabiliyet_orani = cov/meanVar) in [-1, 1]
stopifnot(all(vd_ok$mutekabiliyet_orani >= -1 & vd_ok$mutekabiliyet_orani <= 1, na.rm = TRUE))

# ---- 8) §109 uzanti: same_sex + age_gap ----
ssa <- fam_struct_same_sex_age_gap(family)
stopifnot(all(c("boyut", "test", "terim", "n", "tahmin", "p", "statu") %in% names(ssa)))
stopifnot(any(ssa$test == "same_sex_fisher_z"))
stopifnot(any(ssa$test == "age_gap_poly"))
ssa_ok <- ssa[ssa$statu_kosum == "ok", ]
stopifnot(all(ssa_ok$p >= 0 & ssa_ok$p <= 1, na.rm = TRUE))

# ---- 9) FDR tablosu: p_bh >= p_ham (BH monotonluk gevsek kontrol) ----
fdr <- fam_struct_fdr_table(bw, sd_tab, ssa)
stopifnot(all(c("paragraf", "test_adi", "p_ham", "p_bh", "yontem", "statu") %in% names(fdr)))
if (nrow(fdr) > 0L) {
  stopifnot(all(fdr$p_ham >= 0 & fdr$p_ham <= 1))
  stopifnot(all(fdr$p_bh >= 0 & fdr$p_bh <= 1, na.rm = TRUE))
  stopifnot(all(fdr$p_bh >= fdr$p_ham - 1e-9, na.rm = TRUE))
}

# ---- 10) Pipeline sarici: tum tablolar + [KESIFSEL - POST-HOC] statusu ----
pipe <- run_phase3_family_structure_pipeline(
  df_family_scored = family,
  df_long_scored = long,
  sesoi_r = 0.10
)
expected_tables <- c("single_parent_descriptive", "birth_order_within",
  "sibship_dilution", "reciprocity_correlations", "variance_decomposition",
  "same_sex_age_gap", "fdr", "target_summary")
stopifnot(all(expected_tables %in% names(pipe)))
stopifnot(grepl("KESIFSEL", pipe$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(pipe$target_summary$n_single_parent == 3L)
stopifnot(grepl("SRM", pipe$target_summary$srm_notu))

cat("PASS: tests/test_family_structure_sibship.R\n")
