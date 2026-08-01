# tests/test_phase4_modules.R
# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLII-XLIX (§116-135) — R/56-62.
# Sentetik veriyle sekil/aralik/parametre-sinir + statu-damgasi + coklu-
# karsilastirma monotonluk + imputasyon-yasagi kontrolu. Kanonik veri kullanilmaz.

suppressMessages({
  source("R/10_derived_scores.R")
  source("R/24_latent_profile.R")
  source("R/56_directional_sibship.R")
  source("R/57_child_level_moderators.R")
  source("R/58_onset_metabolic_context.R")
  source("R/59_family_health_validity.R")
  source("R/60_derived_structural.R")
  source("R/61_maternal_mh_child_plane.R")
  source("R/62_selection_batch_validity.R")
})

set.seed(20260708L)
STATU <- "[KESIFSEL - POST-HOC]"

# ---------------------------------------------------------------------------
# Sentetik veri uretimi (tum modul kolon-gereksinimlerini karsilar)
# ---------------------------------------------------------------------------
N <- 240L
gid <- rep(c("DM", "Kontrol"), each = N / 2L)
fam <- data.frame(
  aile_no = seq_len(N),
  group_f = factor(gid, levels = c("Kontrol", "DM")),
  katilimci_cocuk_cinsiyet = sample(0:1, N, replace = TRUE),
  anne_yas = round(rnorm(N, 40, 6), 1),
  cocuk_yas = round(runif(N, 8, 17), 1),
  kardes_yas = round(runif(N, 6, 18), 1),
  dm_yili = round(runif(N, 0.5, 10), 1),
  ses_latent = rnorm(N),
  anne_antidepresan = rbinom(N, 1, 0.2),
  cocuk_sayisi = sample(2:4, N, replace = TRUE),
  age_gap = round(runif(N, 0.5, 6), 1),
  medeni_durum = sample(c("Evli", "Bosanmis"), N, replace = TRUE, prob = c(.9, .1)),
  anket_tarihi = sample(c("15.03.2023", "20.06.2024", "10.01.2025"), N, replace = TRUE),
  kronik_hastalik_durumu = rbinom(N, 1, 0.25),
  esiniz_kronik_hastalik_durumu = rbinom(N, 1, 0.2),
  stringsAsFactors = FALSE
)
fam$tani_yasi <- fam$cocuk_yas - fam$dm_yili
fam$beck_total <- pmax(0, round(rnorm(N, 12, 8)))
fam$beck_clinical <- factor(ifelse(fam$beck_total >= 17, "Klinik_duzey", "Klinik_alti"),
  levels = c("Klinik_alti", "Klinik_duzey"))
fam$beck_severity <- cut(fam$beck_total, c(-1, 9, 16, 29, 63),
  labels = c("Minimal", "Hafif", "Orta", "Siddetli"))
for (s in c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")) {
  fam[[paste0("embu_p_", s, "_mean")]] <- round(runif(N, 1, 4), 2)
  fam[[paste0("embu_c_idx_", s, "_mean")]] <- round(runif(N, 1, 4), 2)
}
for (d in c("nurturance", "dominance", "admiration")) for (dir in c("of", "by")) {
  fam[[sprintf("srq_fo_%s_%s_sib_mean", d, dir)]] <- round(runif(N, 1, 5), 2)
}
for (h in c("conflict", "rivalry", "warmth")) fam[[paste0("srq_ho_", h, "_mean")]] <- round(runif(N, 1, 5), 2)
sys14 <- fhv_comorbidity_systems()
for (w in c("anne", "es")) {
  cs <- integer(N)
  for (s in sys14) { v <- rbinom(N, 1, 0.03); fam[[paste0(w, "_hastalik_", s)]] <- v; cs <- cs + v }
  fam[[paste0(w, "_hastalik_kategori_sayisi")]] <- cs
}
# kodlama-sadakati: oz-bildirim = (kategori_sayisi>0) [κ=1 sentetik]
fam$kronik_hastalik_durumu <- as.integer(fam$anne_hastalik_kategori_sayisi > 0)
fam$esiniz_kronik_hastalik_durumu <- as.integer(fam$es_hastalik_kategori_sayisi > 0)

# Long: iki satir/aile (index + sibling)
long <- do.call(rbind, lapply(seq_len(N), function(i) {
  data.frame(
    aile_no = fam$aile_no[i], group_f = fam$group_f[i],
    family_role_f = c("index", "sibling"),
    cinsiyet_f = sample(c("Kiz", "Erkek"), 2, replace = TRUE),
    cocuk_yas = c(fam$cocuk_yas[i], fam$kardes_yas[i]),
    stringsAsFactors = FALSE)
}))
long$role_f <- factor(paste(ifelse(long$group_f == "DM", "DM_Hasta", "Kontrol"),
  ifelse(long$family_role_f == "index", "Indeks", "Kardes"), sep = "_"))
NL <- nrow(long)
for (s in c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")) {
  long[[paste0("embu_c_", s, "_mean")]] <- round(runif(NL, 1, 4), 2)
}
facet_map <- dsib_facet_item_map()
for (fc in names(facet_map)) long[[paste0("srq_fo_", fc, "_mean")]] <- round(runif(NL, 1, 5), 2)
for (it in 1:48) long[[paste0("srq_", it)]] <- sample(1:5, NL, replace = TRUE)
for (h in c("conflict", "rivalry", "warmth")) long[[paste0("srq_ho_", h, "_mean")]] <- round(runif(NL, 1, 5), 2)

supp <- data.frame(aile_no = fam$aile_no, es_yas = round(fam$anne_yas + rnorm(N, 3, 4), 1),
  es_yas_valid = TRUE, stringsAsFactors = FALSE)
supp$ebeveyn_yas_farki <- fam$anne_yas - supp$es_yas

# helper: coklu-karsilastirma monotonluk
adj_ge_raw <- function(adj, raw) all(adj >= raw - 1e-8, na.rm = TRUE)

# ===========================================================================
# R/62 — §135 secilim/batch
# ===========================================================================
r62 <- run_phase4_selection_batch_pipeline(fam)
stopifnot(all(c("year_group_table", "year_collinearity", "batch_replication",
  "year_stratified_descriptive", "target_summary") %in% names(r62)))
stopifnot(identical(r62$target_summary$kisim, "KISIM XLIX (§135)"))
stopifnot(r62$target_summary$imputation == "YOK (Kural 19)")
stopifnot(nrow(r62$year_group_table) >= 2L)
stopifnot(all(c("d_full", "d_2023", "yon_korundu") %in% names(r62$batch_replication)))

# ===========================================================================
# R/61 — §130-133 maternal MH → cocuk duzlemi
# ===========================================================================
r61 <- run_phase4_maternal_mh_pipeline(long, fam, seed = 20260708L)
stopifnot(all(c("embu_c_2x2_fixed", "embu_c_cell_means", "discrepancy_focal_131",
  "discrepancy_srq_132", "target_summary") %in% names(r61)))
stopifnot(grepl("tedavi/temas", r61$target_summary$ad_yorumu))
stopifnot(r61$target_summary$imputation == "YOK (Kural 19)")
# 2x2 cell means: 4 hucre / outcome
cm <- r61$embu_c_cell_means
stopifnot(nrow(cm[cm$outcome == "embu_c_reddetme_mean", ]) == 4L)
# §132 Holm >= raw
if (!is.null(r61$discrepancy_srq_132)) stopifnot(adj_ge_raw(r61$discrepancy_srq_132$p_holm, r61$discrepancy_srq_132$p_value))
# §133 LCA sozlesme (poLCA varsa)
if (requireNamespace("poLCA", quietly = TRUE) && !is.null(r61$lca_contract_meta)) {
  ct <- r61$lca_contract_table
  stopifnot(all(c("aile_no", "predclass", "risk_label", "max_posterior", "entropy_overall") %in% names(ct)))
  stopifnot(all(ct$max_posterior >= 0 & ct$max_posterior <= 1))
  stopifnot(all(levels(ct$risk_label) == c("adaptif", "riskli")))
  if (!is.null(r61$lca_external_validation_133))
    stopifnot(adj_ge_raw(r61$lca_external_validation_133$p_holm, r61$lca_external_validation_133$p_value))
}

# ===========================================================================
# R/56 — §116-118 yonlu kardes-iliski
# ===========================================================================
r56 <- run_phase4_directional_sibship_pipeline(long, fam)
stopifnot(all(c("asym_fixed_116", "facet_reliability_116", "facet_forest_117",
  "age_direction_descriptive_118", "target_summary") %in% names(r56)))
ff <- r56$facet_forest_117
stopifnot(nrow(ff) == 14L)                                 # 14 non-partiality faset
stopifnot(!any(c("maternal_partiality", "paternal_partiality") %in% ff$facet))
stopifnot(adj_ge_raw(ff$p_fdr, ff$p_value))                # BH-FDR >= raw
stopifnot(all(ff$std_fark >= -3 & ff$std_fark <= 3, na.rm = TRUE))
rel <- r56$facet_reliability_116
stopifnot(all(rel$alpha[!is.na(rel$alpha)] >= -1 & rel$alpha[!is.na(rel$alpha)] <= 1))
stopifnot(grepl("OF - BY", r56$target_summary$yon_konvansiyonu))

# ===========================================================================
# R/57 — §119-120 cocuk-duzeyi moderatorler
# ===========================================================================
r57 <- run_phase4_child_moderators_pipeline(long, fam)
stopifnot(all(c("interaction_119", "cell_means_119", "nonlinearity_120", "target_summary") %in% names(r57)))
inter <- r57$interaction_119
stopifnot(all(inter$term == "cinsiyet_fErkek:group_fDM"))  # yalniz etkilesim odak
stopifnot(all(inter$p_value >= 0 & inter$p_value <= 1, na.rm = TRUE))
nl <- r57$nonlinearity_120
stopifnot(all(c("nonlin_F", "nonlin_p", "nonlineer_var") %in% names(nl)))

# ===========================================================================
# R/58 — §121 onset (DM-only)
# ===========================================================================
r58 <- run_phase4_onset_metabolic_pipeline(fam)
stopifnot(r58$target_summary$n_dm == 120L)
stopifnot(identical(r58$target_summary$kisim, "KISIM XLIV (§121)"))
stopifnot(all(c("onset_band_descriptive_121", "onset_omnibus_121",
  "post_diagnosis_sibling_sensitivity_121", "target_summary") %in% names(r58)))
stopifnot(all(r58$onset_omnibus_121$p_value >= 0 & r58$onset_omnibus_121$p_value <= 1, na.rm = TRUE))

# ===========================================================================
# R/59 — §123-124 aile saglik profili/gecerlik
# ===========================================================================
r59 <- run_phase4_family_health_pipeline(fam)
stopifnot(all(c("comorbidity_prevalence_123", "coding_fidelity_124", "target_summary") %in% names(r59)))
pv <- r59$comorbidity_prevalence_123
stopifnot(all(pv$prevalans >= 0 & pv$prevalans <= 1, na.rm = TRUE))
cf <- r59$coding_fidelity_124
# sentetik: oz-bildirim == kodlanmis → κ=1 ve gozlenen uyum=1
stopifnot(all(abs(cf$kappa - 1) < 1e-8, na.rm = TRUE))
stopifnot(all(abs(cf$gozlenen_uyum - 1) < 1e-8, na.rm = TRUE))
stopifnot(all(cf$n_oz_bildirim_var == cf$n_kodlanmis_var))  # ic-tutarlilik (kappa=1)
stopifnot(grepl("bagimsiz gecerlik DEGIL", cf$yorum[1L]))

# ===========================================================================
# R/60 — §125 ebeveyn yas farki
# ===========================================================================
r60 <- run_phase4_derived_structural_pipeline(fam, supp)
stopifnot(all(c("age_gap_descriptive", "age_gap_models", "target_summary") %in% names(r60)))
d125 <- r60$age_gap_descriptive
stopifnot(d125$n_gecerli <= nrow(fam))
if (!is.null(r60$age_gap_models)) stopifnot(adj_ge_raw(r60$age_gap_models$p_holm, r60$age_gap_models$p_value))
# B7 maskesi: imkansiz es_yas dislanmali
supp_bad <- supp; supp_bad$es_yas[1:3] <- c(13, 12, 90)
r60b <- run_phase4_derived_structural_pipeline(fam, supp_bad)
stopifnot(r60b$target_summary$n_maskeli_B7 >= 3L)

cat("[PASS] tests/test_phase4_modules.R (KISIM XLII-XLIX §116-135 Faz IV — 7 modul)\n")
