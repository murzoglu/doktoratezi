# tests/test_dm_exposure_intensity.R
# [KESIFSEL - POST-HOC] Faz III SAP KISIM XL/110-111 — DM maruziyet yogunlugu.
# Sentetik veriyle sekil/aralik/parametre-sinir kontrolu (r, illness_life_ratio,
# TOST karar, band seviyeleri, AIC sonlulugu). Kanonik veri kullanilmaz.

source("R/55_dm_exposure_intensity.R")

set.seed(20260708L)

# --- 1) Sabit haritalar / focal terimler ---
stopifnot(length(dmexp_overprotection_outcomes()) == 3L)
stopifnot(identical(dmexp_focal_term("i_illness_life_ratio"), "illness_life_ratio"))
stopifnot(identical(dmexp_focal_term("ii_dm_yili_yas_kovaryat"), "dm_yili"))
stopifnot(identical(dmexp_focal_term("iii_taniyasi_x_yas"), "tani_yasi_c:cocuk_yas_c"))

# --- 2) Sentetik DM-agirlikli aile karesi ---
n <- 140L
cocuk_yas <- round(runif(n, 7, 17), 1)
dm_yili <- pmin(cocuk_yas, round(runif(n, 0.5, 12), 1)) # cogunlukla gecerli oran
group_f <- factor(rep(c("DM", "Kontrol"), c(120L, n - 120L)), levels = c("Kontrol", "DM"))
# Birkac mantiksal-imkansiz oran ekle (dm_yili > cocuk_yas) — gecerlilik denetimi icin
dm_yili[1:4] <- cocuk_yas[1:4] + c(0.5, 1.0, 1.5, 2.0)

fam <- data.frame(
  aile_no = seq_len(n),
  group_f = group_f,
  cocuk_yas = cocuk_yas,
  dm_yili = dm_yili,
  kardes_yas = round(runif(n, 5, 19), 1),
  anne_yas = round(rnorm(n, 40, 5), 1),
  ses_latent = rnorm(n),
  stringsAsFactors = FALSE
)
map_out <- c(dmexp_overprotection_outcomes(),
  dmexp_psychcontrol_components(), dmexp_sibling_outcomes())
for (oc in unique(map_out)) {
  fam[[oc]] <- rnorm(n, 2.2, 0.5) + 0.15 * scale(dm_yili)[, 1]
}

# --- 3) Frame hazirlama: DM-only filtre + turetilmis alanlar ---
prep <- dmexp_prepare_frame(fam)
stopifnot(is.data.frame(prep))
stopifnot(nrow(prep) == 120L)              # yalniz DM
stopifnot(all(prep$group_f == "DM"))
stopifnot(all(c("illness_life_ratio", "tani_yasi", "kardes_tani_ani_yas",
  "cocuk_yas_z", "cocuk_yas_c", "tani_yasi_c", "psychcontrol_proxy_z") %in% names(prep)))
# tani_yasi = cocuk_yas - dm_yili tutarliligi
stopifnot(isTRUE(all.equal(prep$tani_yasi, prep$cocuk_yas_num - prep$dm_yili_num)))
# ratio mantiksal-imkansiz vakalar (>1) mevcut olmali (ilk 4 satir DM icinde)
stopifnot(sum(prep$illness_life_ratio > 1, na.rm = TRUE) >= 1L)

# --- 4) Gecerlilik tablosu: aralik-disi tespiti + mean/median ---
validity <- dmexp_life_ratio_validity(prep)
stopifnot(is.data.frame(validity))
stopifnot(all(c("degisken", "ortalama", "medyan", "n_aralik_disi", "uyari", "statu")
  %in% names(validity)))
ratio_v <- validity[validity$degisken == "illness_life_ratio", , drop = FALSE]
stopifnot(nrow(ratio_v) == 1L)
stopifnot(ratio_v$n_aralik_disi >= 1L)     # >1 vakalari yakalandi
stopifnot(grepl("DOGRULANMAMIS", ratio_v$uyari))
stopifnot(all(validity$statu == "[KESIFSEL - POST-HOC]"))

# --- 5) Analitik ornek: yalniz gecerli oran (0<ratio<=1) ---
sub <- dmexp_analytic_subset(prep, "embu_c_idx_asiri_koruma_mean")
stopifnot(all(sub$illness_life_ratio > 0 & sub$illness_life_ratio <= 1))
stopifnot(nrow(sub) <= nrow(prep))

# --- 6) Parametrizasyon modelleri: focal katsayi + AIC + Holm ---
models <- dmexp_overprotection_models(prep)
ep <- models$exposure_parametrizations
stopifnot(is.data.frame(ep))
stopifnot(all(c("outcome", "parametrizasyon", "focal_term", "estimate",
  "ci_lower", "ci_upper", "r_partial", "aic", "delta_aic", "p_value", "p_holm",
  "n", "statu") %in% names(ep)))
ok_ep <- ep[!is.na(ep$status) & ep$status == "ok", , drop = FALSE]
stopifnot(nrow(ok_ep) >= 1L)
# AIC sonlu; delta_aic >= 0; GA siralamasi; kismi r sinirlari [-1,1]
stopifnot(all(is.finite(ok_ep$aic)))
stopifnot(all(ok_ep$delta_aic >= -1e-8, na.rm = TRUE))
stopifnot(all(ok_ep$ci_lower <= ok_ep$estimate + 1e-8, na.rm = TRUE))
stopifnot(all(ok_ep$ci_upper >= ok_ep$estimate - 1e-8, na.rm = TRUE))
stopifnot(all(ok_ep$r_partial >= -1 & ok_ep$r_partial <= 1, na.rm = TRUE))
stopifnot(all(ok_ep$r_ci_lower >= -1 & ok_ep$r_ci_upper <= 1, na.rm = TRUE))
# Holm >= ham p
stopifnot(all(ok_ep$p_holm >= ok_ep$p_value - 1e-8, na.rm = TRUE))
# Her outcome icin en fazla 3 parametrizasyon; ayni analitik n (AIC-karsilastirilabilir)
for (oc in unique(ok_ep$outcome)) {
  block <- ok_ep[ok_ep$outcome == oc, , drop = FALSE]
  stopifnot(nrow(block) <= 3L)
  stopifnot(length(unique(block$n)) == 1L)  # ortak satirlar
}

# Full coef tablosu
stopifnot(!is.null(models$overprotection_models))
stopifnot(all(c("term", "estimate", "ci_lower", "ci_upper", "aic", "statu")
  %in% names(models$overprotection_models)))

# --- 7) Psikolojik-kontrol yan-analizi: r sinirlari + TOST karar kumesi ---
pc <- dmexp_psychcontrol_sideanalysis(prep, sesoi_r = 0.10)
stopifnot(is.data.frame(pc))
stopifnot(all(c("exposure", "r", "ci_lower", "ci_upper", "tost_p", "tost_karar",
  "p_holm") %in% names(pc)))
# Yan-analiz §110 modelleriyle AYNI mantiksal-tutarlilik kuralini uygular:
# dm_yili>cocuk_yas kayitlari dislanir (test verisinde 4). Boylece side-analysis
# ile ana model (n=115/116) tutarli; kirlenmis dm_yili turevleri korelasyonu
# sifira dogru zayiflatmaz.
stopifnot("n_dislanan_tutarsiz" %in% names(pc))
stopifnot(all(pc$n_dislanan_tutarsiz == 4L))                 # 4 mantiksal-imkansiz DM
stopifnot(all(pc$n <= 116L, na.rm = TRUE))                   # 120 - 4 dislanan
pc_ok <- pc[!is.na(pc$r), , drop = FALSE]
stopifnot(all(pc_ok$r >= -1 & pc_ok$r <= 1))                 # korelasyon siniri
stopifnot(all(pc_ok$tost_p >= 0 & pc_ok$tost_p <= 1))        # p siniri
valid_kararlar <- c("Onemsiz (trivial)", "Esdeger (|r|<.10)",
  "Anlamli (esdeger degil)", "Belirsiz", "yetersiz_n")
stopifnot(all(pc$tost_karar %in% valid_kararlar))

# --- 8) §111 kardes penceresi: band seviyeleri + betimsel (test yok) ---
sw <- dmexp_sibling_window_descriptive(prep)
stopifnot(is.data.frame(sw))
stopifnot(all(c("band", "n_band", "degisken", "ortalama", "medyan", "not", "statu")
  %in% names(sw)))
expected_bands <- c("<0 (tani sonrasi dogdu)", "0-5", "5-10", ">=10",
  "DISLANDI (dm_yili>cocuk_yas tutarsiz)")
stopifnot(all(unique(sw$band) %in% expected_bands))
stopifnot(grepl("GELECEK-TASARIM", sw$not[1L]))
# Mantiksal-imkansiz dm_yili kayitlari §110.1 kuraliyla dislanmali (test verisinde 4)
stopifnot("DISLANDI (dm_yili>cocuk_yas tutarsiz)" %in% sw$band)
# band n toplami DM n'ye esit (dislanan band + gecerli bandlar = tum DM)
band_n <- unique(sw[, c("band", "n_band")])
stopifnot(sum(band_n$n_band) == nrow(prep))

# --- 9) Pipeline sarici: 6 tablo + [KESIFSEL - POST-HOC] damgasi ---
res <- run_phase3_dm_exposure_pipeline(prep_input <- fam)
stopifnot(all(c("life_ratio_validity", "exposure_parametrizations",
  "overprotection_models", "psychcontrol_sideanalysis",
  "sibling_window_descriptive", "target_summary") %in% names(res)))
stopifnot(res$target_summary$n_dm == 120L)
stopifnot(grepl("KESIFSEL", res$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(identical(res$target_summary$imputation, "YOK (Kural 19)"))
stopifnot(grepl("Holm", res$target_summary$coklu_karsilastirma))

cat("[PASS] tests/test_dm_exposure_intensity.R (KISIM XL §110-111 DM maruziyet)\n")
