# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXVIII/103-106 test
# Sentetik veriyle sekil/aralik/parametre-sinir kontrolu (satir-duzeyi veri yok).

source("R/53_maternal_comorbidity.R")

set.seed(20260708L)

# --- 1) Yardimci fonksiyonlar ---------------------------------------------
stopifnot(identical(mc_evidence_status(), "[KESIFSEL - POST-HOC]"))
stopifnot(identical(mc_embu_p_outcomes(),
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")))
stopifnot(identical(mc_binary_from_count(c(0, 1, 2, NA)), c(0L, 1L, 1L, NA)))
stopifnot(is.na(mc_scale(rep(3, 5)))[1])  # sabit vektor -> NA

# Cohen's d yon: grup1 ortalamasi grup0'dan buyukse d > 0
dtest <- mc_cohens_d_ci(c(rnorm(40, 1), rnorm(40, 0)),
  rep(c(1L, 0L), each = 40))
stopifnot(is.finite(dtest$d), dtest$d > 0)
stopifnot(dtest$ci_low <= dtest$d, dtest$d <= dtest$ci_high)
stopifnot(dtest$n1 == 40L, dtest$n0 == 40L)

# --- 2) Sentetik family + long fikstur ------------------------------------
n <- 160L
family <- data.frame(
  aile_no = seq_len(n),
  group_f = factor(rep(c("Kontrol", "DM"), each = n / 2L),
    levels = c("Kontrol", "DM")),
  anne_hastalik_otoimmun = c(rep(0L, n - 2L), 1L, 0L),
  anne_hastalik_endokrin = rbinom(n, 1L, 0.08),
  anne_hastalik_mental = c(rep(0L, n - 2L), 1L, 1L),
  anne_hastalik_kategori_sayisi = sample(c(0L, 0L, 0L, 1L, 2L), n, replace = TRUE),
  es_hastalik_kategori_sayisi = sample(c(0L, 0L, 0L, 0L, 1L, 2L), n, replace = TRUE),
  anne_antidepresan = rbinom(n, 1L, 0.2),
  anne_yas = rnorm(n, 38, 5),
  beck_total = pmax(0, round(rnorm(n, 9, 6))),
  ses_latent = rnorm(n),
  stringsAsFactors = FALSE
)
family$beck_total[family$anne_antidepresan == 1L] <-
  family$beck_total[family$anne_antidepresan == 1L] + 5
for (sub in mc_embu_p_outcomes()) {
  family[[paste0("embu_p_", sub, "_mean")]] <- rnorm(n, 2.4, 0.5)
}

long <- data.frame(
  aile_no = rep(seq_len(n), each = 2L),
  family_role_f = factor(rep(c("index", "sibling"), n),
    levels = c("index", "sibling")),
  stringsAsFactors = FALSE
)
for (sub in mc_embu_p_outcomes()) {
  long[[paste0("embu_c_", sub, "_mean")]] <- rnorm(nrow(long), 2.5, 0.5)
}

# --- 3) 103 otoimmun prevalans (Tier D) -----------------------------------
ap <- mc_autoimmune_prevalence(family)
stopifnot(all(c("gosterge", "dm_prevalans_pct", "kontrol_prevalans_pct",
  "fisher_p", "test_edilebilir", "statu") %in% names(ap)))
stopifnot(all(ap$test_edilebilir == "HAYIR"))
stopifnot(all(ap$statu == "[KESIFSEL - POST-HOC]"))
stopifnot(all(ap$tier == "D"))
# Fisher p mantiksal sinir [0, 1]
fp <- ap$fisher_p[!is.na(ap$fisher_p)]
stopifnot(all(fp >= 0 & fp <= 1))
# prevalans yuzdeleri [0, 100]
pv <- c(ap$dm_prevalans_pct, ap$kontrol_prevalans_pct)
pv <- pv[!is.na(pv)]
stopifnot(all(pv >= 0 & pv <= 100))

# --- 4) 104 ikili komorbidite etkileri (Tier C) ---------------------------
be <- mc_binary_comorbid_effects(family)
stopifnot(nrow(be) == 5L)  # beck_total + 4 EMBU-P
stopifnot(all(c("outcome", "cohen_d", "d_ci_low", "d_ci_high", "welch_p",
  "welch_p_holm", "ols_comorbid_beta", "statu") %in% names(be)))
# Cohen's d GA sirasi tutarli
okd <- !is.na(be$cohen_d) & !is.na(be$d_ci_low) & !is.na(be$d_ci_high)
stopifnot(all(be$d_ci_low[okd] <= be$cohen_d[okd]),
  all(be$cohen_d[okd] <= be$d_ci_high[okd]))
# Welch p ve Holm mantiksal sinir [0, 1]; Holm >= ham p
wp <- be$welch_p[!is.na(be$welch_p)]
stopifnot(all(wp >= 0 & wp <= 1))
okp <- !is.na(be$welch_p) & !is.na(be$welch_p_holm)
stopifnot(all(be$welch_p_holm[okp] >= be$welch_p[okp] - 1e-9))
# alt-grup n toplami <= n
stopifnot(all(be$n_komorbid_var + be$n_komorbid_yok <= n))

# --- 5) 104 aracilik (lavaan varsa) ---------------------------------------
med <- mc_comorbid_mediation(family, n_boot = 200L)
stopifnot(all(c("outcome_subscale", "status", "statu") %in% names(med)))
stopifnot(all(med$statu == "[KESIFSEL - POST-HOC]"))
if (any(med$status == "ok")) {
  pm <- med[med$effect == "prop_mediated" & med$status == "ok", , drop = FALSE]
  # BCa CI alt <= ust mantiksal sinir
  ok_ci <- med$status == "ok" & !is.na(med$ci_low) & !is.na(med$ci_high)
  stopifnot(all(med$ci_low[ok_ci] <= med$ci_high[ok_ci]))
}

# --- 6) 105 antidepresan x grup + yakinsama (Tier B-) ---------------------
ag <- mc_antidep_group(family)
stopifnot(all(c("dm_pct", "kontrol_pct", "chisq_p", "cramers_v", "statu")
  %in% names(ag)))
stopifnot(ag$chisq_p >= 0 & ag$chisq_p <= 1)
stopifnot(ag$dm_pct >= 0 & ag$dm_pct <= 100)
# Cramer's V mantiksal sinir [0, 1] (NA olabilir)
if (!is.na(ag$cramers_v)) stopifnot(ag$cramers_v >= 0 & ag$cramers_v <= 1)

dc <- mc_distress_convergence(family)
stopifnot(all(c("metrik", "deger", "ci_low", "ci_high", "n", "statu") %in% names(dc)))
# korelasyon/kappa/phi hepsi [-1, 1] mantiksal sinirinda
val <- dc$deger[!is.na(dc$deger)]
stopifnot(all(val >= -1 & val <= 1))
rpb <- dc[dc$metrik == "nokta_biserial_r", , drop = FALSE]
if (!is.na(rpb$ci_low[1]) && !is.na(rpb$ci_high[1])) {
  stopifnot(rpb$ci_low[1] <= rpb$deger[1], rpb$deger[1] <= rpb$ci_high[1])
}

# --- 7) 106 negatif kontrol lme4 + TOST (Tier C) --------------------------
nc <- mc_negative_control_lme(family, long)
stopifnot(all(c("outcome_subscale", "model", "status", "beta", "ci_low",
  "ci_high", "p", "p_holm", "statu") %in% names(nc)))
stopifnot(any(nc$model == "temel"), any(nc$model == "duyarlilik_toplam_yuk"))
ok_nc <- nc$status == "ok" & !is.na(nc$ci_low) & !is.na(nc$ci_high)
stopifnot(all(nc$ci_low[ok_nc] <= nc$beta[ok_nc]),
  all(nc$beta[ok_nc] <= nc$ci_high[ok_nc]))
pnc <- nc$p[nc$status == "ok" & !is.na(nc$p)]
stopifnot(all(pnc >= 0 & pnc <= 1))

tost <- mc_negative_control_tost(family, long, sesoi_r = 0.10)
stopifnot(all(c("outcome_subscale", "r", "tost_p", "sesoi_r", "tost_karar",
  "statu") %in% names(tost)))
stopifnot(all(tost$sesoi_r == 0.10))
# r mantiksal sinir [-1, 1]; tost_p [0, 1]
rr <- tost$r[!is.na(tost$r)]
stopifnot(all(rr >= -1 & rr <= 1))
tp <- tost$tost_p[!is.na(tost$tost_p)]
stopifnot(all(tp >= 0 & tp <= 1))

# --- 8) Pipeline sarici ---------------------------------------------------
res <- run_phase3_maternal_comorbidity_pipeline(family, long,
  mediation_boot = 200L, sesoi_r = 0.10)
stopifnot(all(c("autoimmune_prevalence", "comorbid_binary_effects",
  "comorbid_mediation", "antidep_group", "distress_convergence",
  "negative_control", "negative_control_tost", "target_summary") %in% names(res)))
stopifnot(grepl("KESIFSEL", res$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(res$target_summary$sesoi_r == 0.10)
stopifnot(res$target_summary$mediation_boot == 200L)

cat("PASS: tests/test_maternal_comorbidity.R\n")
