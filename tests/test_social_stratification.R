# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXVII (§100-102b) test
# R/52_social_stratification.R saf fonksiyon sekil/aralik/parametre-sinir kontrolu.

source("R/52_social_stratification.R")

set.seed(20260708L)

# ---------------------------------------------------------------------------
# 1) Recode fonksiyonlari
# ---------------------------------------------------------------------------
egp3 <- strat_egp3_recode(c(1, 2, 3, 4, 5, 6, 7, NA))
stopifnot(identical(as.character(egp3),
  c("hizmet", "hizmet", "ara", "ara", "ara", "isci_rutin", "isci_rutin", NA)))
stopifnot(identical(levels(egp3), c("hizmet", "ara", "isci_rutin")))

edu3 <- strat_edu3_recode(c(0, 1, 2, 3, 4, 5, NA))
stopifnot(identical(as.character(edu3),
  c("dusuk", "dusuk", "orta", "orta", "yuksek", "yuksek", NA)))
stopifnot(identical(levels(edu3), c("dusuk", "orta", "yuksek")))

# ---------------------------------------------------------------------------
# 2) z-skor ve yardimcilar
# ---------------------------------------------------------------------------
z <- strat_scale(c(1, 2, 3, 4, 5))
stopifnot(abs(mean(z)) < 1e-8)
stopifnot(abs(stats::sd(z) - 1) < 1e-8)
stopifnot(all(is.na(strat_scale(rep(2, 5)))))       # sabit -> NA
stopifnot(all(is.na(strat_scale(c(NA, NA)))))

# t -> r sinir kontrolu (|r| <= 1)
r_vals <- vapply(c(-50, -2, 0, 2, 50), function(t) strat_t_to_r(t, df = 100), numeric(1))
stopifnot(all(r_vals >= -1 & r_vals <= 1))
stopifnot(is.na(strat_t_to_r(2, df = 0)))

# Holm: NA guvenli, duzeltilmis >= ham
p_raw <- c(0.01, 0.04, NA, 0.20)
p_h <- strat_holm(p_raw)
stopifnot(is.na(p_h[3]))
stopifnot(all(p_h[c(1, 2, 4)] >= p_raw[c(1, 2, 4)] - 1e-12))
stopifnot(all(p_h[c(1, 2, 4)] <= 1))

# ---------------------------------------------------------------------------
# 3) Sentetik aile + long veri
# ---------------------------------------------------------------------------
n <- 180L
edu_anne <- sample(0:5, n, TRUE, prob = c(.06, .24, .2, .28, .15, .07))
edu_baba <- pmin(5L, pmax(0L, as.integer(edu_anne + sample(c(-1L, 0L, 1L), n, TRUE))))
egp7 <- sample(1:7, n, TRUE, prob = c(.05, .05, .10, .11, .15, .18, .36))
egp7[sample(seq_len(n), round(0.12 * n))] <- NA          # yapisal NA
isei <- 30 + 6 * edu_baba + stats::rnorm(n, 0, 8)
siops <- 28 + 5 * edu_baba + stats::rnorm(n, 0, 7)
material_raw <- stats::rnorm(n) + 0.3 * edu_baba
material_z <- as.numeric(scale(material_raw))
beck_total <- 8 + 2 * (-material_z) + stats::rnorm(n, 0, 5)
beck_total[beck_total < 0] <- 0
group_f <- factor(rep(c("Kontrol", "DM"), length.out = n), levels = c("Kontrol", "DM"))
calisma <- stats::rbinom(n, 1, 0.6)

family <- data.frame(
  aile_no = seq_len(n),
  group_f = group_f,
  katilimci_cocuk_cinsiyet = stats::rbinom(n, 1, 0.5),
  cocuk_yas = round(stats::runif(n, 7, 17)),
  anne_yas = round(stats::rnorm(n, 38, 5)),
  aile_egp7 = egp7,
  es_siops08 = siops,
  aile_isei08 = isei,
  egitim_durumu = edu_anne,
  es_egitim_durumu = edu_baba,
  calisma_durumu = calisma,
  edu_z = as.numeric(scale(edu_anne + edu_baba)),
  isei_z = as.numeric(scale(isei)),
  material_z = material_z,
  ses_latent = as.numeric(scale(0.5 * scale(isei) + 0.3 * scale(edu_baba) + 0.2 * material_z)),
  beck_total = beck_total,
  stringsAsFactors = FALSE
)
# EMBU-P (anne): FSM sinyali (beck -> sicaklik dusus / reddetme artis)
family$embu_p_sicaklik_mean <- 3.2 - 0.015 * beck_total + stats::rnorm(n, 0, 0.4)
family$embu_p_asiri_koruma_mean <- 2.1 + 0.10 * (2 - as.integer(strat_egp3_recode(egp7))) +
  stats::rnorm(n, 0, 0.5)
family$embu_p_reddetme_mean <- 1.6 + 0.010 * beck_total + stats::rnorm(n, 0, 0.3)
family$embu_p_karsilastirma_mean <- 1.8 + stats::rnorm(n, 0, 0.4)
# EMBU-C (indeks, aile) + SRQ: DRM icin anne/baba egitim karisimi
family$embu_c_idx_sicaklik_mean <- 3.0 + 0.10 * edu_anne + 0.05 * edu_baba + stats::rnorm(n, 0, 0.5)
family$embu_c_idx_reddetme_mean <- 1.8 - 0.05 * edu_anne - 0.05 * edu_baba + stats::rnorm(n, 0, 0.4)
family$srq_ho_conflict_mean <- 2.5 + 0.06 * edu_anne + 0.04 * edu_baba + stats::rnorm(n, 0, 0.5)

# Long: her aileden 2 cocuk (indeks + kardes)
long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  group = rep(as.character(group_f), each = 2L),
  family_role = rep(c("index", "sibling"), times = n),
  katilimci_cocuk_cinsiyet = stats::rbinom(2L * n, 1, 0.5),
  cocuk_yas = round(stats::runif(2L * n, 7, 17)),
  stringsAsFactors = FALSE
)
long$group_f <- factor(long$group, levels = c("Kontrol", "DM"))
cal_rep <- rep(calisma, each = 2L)
grp_rep <- rep(as.integer(group_f == "DM"), each = 2L)
for (sub in strat_embu_p_outcomes()) {
  base <- if (sub == "sicaklik") 3.0 else 2.0
  # sicaklik: calisma × grup etkilesim sinyali (long)
  inter <- if (sub == "sicaklik") 0.35 * cal_rep * grp_rep else 0
  long[[strat_embu_c_long_col(sub)]] <- base + inter + stats::rnorm(2L * n, 0, 0.5)
}

# ---------------------------------------------------------------------------
# 4) Veri hazirlama fonksiyonlari
# ---------------------------------------------------------------------------
fam <- strat_prepare_family(family)
stopifnot(all(c("egp3_f", "edu3_anne_f", "edu3_baba_f", "siops_z", "cocuk_yas_z",
  "anne_yas_z", "ses_latent_z", "deprivation_z", "calisma_f", "group_dm",
  "cinsiyet_idx_f") %in% names(fam)))
stopifnot(identical(levels(fam$egp3_f), c("hizmet", "ara", "isci_rutin")))
stopifnot(identical(levels(fam$edu3_anne_f), levels(fam$edu3_baba_f)))    # DRM: ayni durum uzayi
# deprivation = -material_z (isaret kontrolu)
stopifnot(all(abs(fam$deprivation_z + fam$material_z) < 1e-8, na.rm = TRUE))

lng <- strat_prepare_long(long, fam)
stopifnot(all(c("egp3_f", "calisma_f", "group_f", "ses_latent_z", "anne_yas_z",
  "cocuk_yas_z", "aile_no_f") %in% names(lng)))
stopifnot(nrow(lng) == nrow(long))

# ---------------------------------------------------------------------------
# 5) §100 EGP gradyan + Simpson
# ---------------------------------------------------------------------------
grad <- strat_egp_gradient(fam, lng)
stopifnot(!is.null(grad$cells), !is.null(grad$omnibus))
stopifnot(all(c("olcum", "kapsam", "egp3", "n_hucre", "ham_ort", "ham_medyan",
  "marj_ort", "ga_alt", "ga_ust", "statu") %in% names(grad$cells)))
stopifnot(all(grepl("KESIFSEL", grad$cells$statu)))
# omnibus: kismi_eta2 [0,1], p [0,1], p_holm >= p
om <- grad$omnibus
fam_om <- om[om$duzey == "aile" & !is.na(om$kismi_eta2), ]
stopifnot(all(fam_om$kismi_eta2 >= -1e-8 & fam_om$kismi_eta2 <= 1))
stopifnot(all(om$p_deger[!is.na(om$p_deger)] >= 0 & om$p_deger[!is.na(om$p_deger)] <= 1))
ok_h <- !is.na(om$p_holm) & !is.na(om$p_deger)
stopifnot(all(om$p_holm[ok_h] >= om$p_deger[ok_h] - 1e-12))

simp <- strat_egp_simpson(fam)
stopifnot(all(c("havuzlanmis", "DM", "Kontrol") %in% unique(simp$kapsam)))   # Simpson zorunlu
stopifnot("beck" %in% unique(simp$olcum))                                     # surekli: ort+medyan
stopifnot(all(!is.na(simp$ham_medyan[simp$n_hucre > 0])))
stopifnot(all(simp$n_hucre >= 0))

# ---------------------------------------------------------------------------
# 6) §100/1.6-C olcum-yarisi: commonality yeniden-insa
# ---------------------------------------------------------------------------
mr <- strat_measurement_race(fam)
stopifnot(all(c("olcum", "yordayici", "model_r2", "artimsal_r2", "essiz_r2",
  "aic", "p_holm", "statu") %in% names(mr)))
mr_r2 <- mr$model_r2[!is.na(mr$model_r2)]
stopifnot(all(mr_r2 >= -1e-8 & mr_r2 <= 1))
for (oc in unique(mr$olcum)) {
  sub <- mr[mr$olcum == oc, ]
  if (any(sub$yordayici == "yetersiz_n")) next
  total <- sub$artimsal_r2[sub$yordayici == "tam_model"]
  uniq <- sub$essiz_r2[sub$yordayici %in% c("isei_z", "siops_z", "egp3")]
  shared <- sub$essiz_r2[sub$yordayici == "ortak(shared)"]
  stopifnot(abs(total - (sum(uniq) + shared)) < 1e-8)   # commonality kimligi
  inc <- sub$artimsal_r2[sub$yordayici %in% c("isei_z", "siops_z", "egp3")]
  stopifnot(all(inc >= -1e-8))                          # artimsal R2 >= 0
}

# ---------------------------------------------------------------------------
# 7) §101 Egitim-DRM: parametre sinirlari (w_anne + w_baba = 1)
# ---------------------------------------------------------------------------
drm <- strat_drm_education(fam)
stopifnot(nrow(drm) == 3L)
stopifnot(all(grepl("KESIFSEL", drm$statu)))
conv <- drm[startsWith(drm$durum, "yakinsadi") & !is.na(drm$w_anne), ]
if (nrow(conv) > 0L) {
  stopifnot(all(abs((conv$w_anne + conv$w_baba) - 1) < 1e-6))   # Dref kisit
}
# Tekrarlanabilirlik: gnm rastgele start kullanir -> sabit seed ayni sonucu vermeli
drm2 <- strat_drm_education(fam)
stopifnot(identical(drm$w_anne, drm2$w_anne))
stopifnot(identical(drm$durum, drm2$durum))

# ---------------------------------------------------------------------------
# 8) §102 hiyerarsik regresyon + VIF
# ---------------------------------------------------------------------------
mh <- strat_material_hierarchical(fam)
stopifnot(nrow(mh) == 5L)                                # 4 EMBU-P + beck_total
ok_mh <- mh$durum == "ok"
stopifnot(all(mh$delta_r2[ok_mh] >= -1e-8))              # material eklenince R2 artar
stopifnot(all(mh$r2_blok2[ok_mh] >= mh$r2_blok1[ok_mh] - 1e-8))
stopifnot(all(mh$vif_material[ok_mh] >= 1 - 1e-8))       # VIF >= 1
stopifnot(all(mh$p_degisim[ok_mh] >= 0 & mh$p_degisim[ok_mh] <= 1))

# ---------------------------------------------------------------------------
# 9) §102 Beck-araci FSM (dusuk boot; sekil kontrolu)
# ---------------------------------------------------------------------------
if (requireNamespace("lavaan", quietly = TRUE)) {
  fsm <- strat_fsm_mediation(fam, subscales = c("sicaklik", "reddetme"), boot_n = 200L)
  stopifnot(all(c("olcum", "parametre", "tahmin", "ci_alt", "ci_ust", "p_holm",
    "statu") %in% names(fsm)))
  ind <- fsm[fsm$parametre == "dolayli" & fsm$durum == "ok", ]
  stopifnot(nrow(ind) >= 1L)
  stopifnot(all(ind$ci_alt <= ind$ci_ust))              # GA siralama
  stopifnot(all(ind$n > 0L))
}

# ---------------------------------------------------------------------------
# 10) §102b istihdam moderasyonu + TOST
# ---------------------------------------------------------------------------
emp <- strat_employment_moderation(fam, lng)
stopifnot(!is.null(emp$coefficients))
coefs <- emp$coefficients
stopifnot(all(c("aile", "long") %in% unique(coefs$duzey)))
er <- coefs$etki_r[!is.na(coefs$etki_r)]
stopifnot(all(er >= -1 & er <= 1))                       # etki r sinirlari
# Kumelenme duzeltmesi: long duzeyde n_etkin = aile sayisi (gozlem sayisi degil)
stopifnot("n_etkin" %in% names(coefs))
long_ok <- coefs$duzey == "long" & coefs$durum == "ok"
if (any(long_ok)) {
  stopifnot(all(coefs$n_etkin[long_ok] <= n))            # kume sayisi <= aile n
  stopifnot(all(coefs$n_etkin[long_ok] < coefs$n[long_ok]))  # 2 cocuk/aile -> etkin < ham
}
if (!is.null(emp$tost)) {
  tost <- emp$tost
  stopifnot(all(c("baglam", "r", "n", "sesoi", "tost_p", "karar", "statu") %in% names(tost)))
  stopifnot(all(tost$sesoi == 0.10))                     # SESOI |r|=.10
  tp <- tost$tost_p[!is.na(tost$tost_p)]
  stopifnot(all(tp >= 0 & tp <= 1))
  stopifnot(all(!is.na(tost$karar)))
  # Long TOST satirlari kume-duzeltmeli n kullanmali (<= aile sayisi)
  tost_long <- tost[startsWith(tost$baglam, "long|"), , drop = FALSE]
  if (nrow(tost_long) > 0L) {
    stopifnot(all(tost_long$n <= n))
  }
}

# ---------------------------------------------------------------------------
# 11) Pipeline sarici
# ---------------------------------------------------------------------------
res <- run_phase3_social_stratification_pipeline(
  df_family_ses = family, df_long_scored = long, boot_n = 200L, seed = 20260708L
)
expected <- c("egp_gradient", "egp_gradient_omnibus", "egp_simpson", "measurement_race",
  "drm_education", "material_hierarchical", "fsm_mediation", "employment_moderation",
  "tost", "status_summary")
stopifnot(all(expected %in% names(res)))
stopifnot(grepl("KESIFSEL", res$status_summary$kanit_kategorisi))
stopifnot(res$status_summary$n_aile == n)
stopifnot(res$status_summary$egp3_yapisal_na == sum(is.na(egp7)))

cat("PASS: tests/test_social_stratification.R\n")
