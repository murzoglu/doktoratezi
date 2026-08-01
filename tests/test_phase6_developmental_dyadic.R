# [KESIFSEL - POST-HOC] Faz VI KISIM LI (§142-151) sentetik-veri sekil/aralik testi
source("R/65_phase6_developmental_dyadic.R")

set.seed(20260714L)

# ---- 1) Yardimci fonksiyonlar ----
stopifnot(identical(f6_embu_subscales(),
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")))
stopifnot(identical(f6_triadic_subscales(), c("sicaklik", "reddetme", "asiri_koruma")))
stopifnot(grepl("KESIFSEL", f6_status_label(), fixed = TRUE))

z <- f6_scale(c(1, 2, 3, 4, 5))
stopifnot(abs(mean(z)) < 1e-8, abs(stats::sd(z) - 1) < 1e-8)
stopifnot(all(is.na(f6_scale(rep(3, 5)))))

t_null <- f6_tost_r(r = 0.00, n = 1000L, sesoi = 0.10)
stopifnot(t_null$p >= 0, t_null$p <= 1, identical(t_null$decision, "esdeger(|r|<SESOI)"))
stopifnot(is.na(f6_tost_r(r = 0.1, n = 3L)$p))
td <- f6_tost_d(rnorm(500, 0, 1), rnorm(500, 0, 1), sesoi = 0.20)
stopifnot(td$p >= 0, td$p <= 1)
stopifnot(is.finite(f6_cohen_d(rnorm(100), rnorm(100, 0.5))))

# ---- 2) Sentetik veri fixture (aile duzeyi) ----
n <- 200L
embu_subs <- f6_embu_subscales()
grp <- factor(rep(c("DM", "Kontrol"), length.out = n), levels = c("Kontrol", "DM"))
is_dm <- grp == "DM"

df <- data.frame(
  aile_no = seq_len(n),
  group_f = grp,
  cocuk_yas = round(stats::runif(n, 7, 17), 1),
  anne_yas = round(stats::runif(n, 28, 55)),
  ses_latent = stats::rnorm(n),
  beck_total = pmax(0, round(stats::rnorm(n, 12, 8))),
  srq_ho_warmth_mean = pmin(5, pmax(1, 3 + 0.4 * stats::rnorm(n))),
  srq_sib_ho_warmth_mean = pmin(5, pmax(1, 3 + 0.4 * stats::rnorm(n))),
  same_sex = factor(sample(c("Ayni", "Farkli"), n, replace = TRUE)),
  stringsAsFactors = FALSE
)
# dm_yili yalniz DM'de (yapisal NA kontrol'de)
df$dm_yili <- NA_real_; df$dm_yili[is_dm] <- round(stats::runif(sum(is_dm), 0.5, 12), 1)

for (sub in embu_subs) {
  base <- stats::rnorm(n)
  df[[paste0("embu_p_", sub, "_mean")]] <- pmin(4, pmax(1, 2.5 + 0.3 * base + stats::rnorm(n, 0, 0.4)))
  # yasla artan transmisyon (etkilesim sinyali test icin)
  df[[paste0("embu_c_idx_", sub, "_mean")]] <- pmin(4, pmax(1,
    2.5 + 0.2 * base + 0.15 * base * f6_scale(df$cocuk_yas) + stats::rnorm(n, 0, 0.5)))
  df[[paste0("embu_c_sib_", sub, "_mean")]] <- pmin(4, pmax(1, 2.5 + 0.2 * base + stats::rnorm(n, 0, 0.5)))
}

# ---- 3) §142 yas x uyum ----
con <- f6_age_concordance(df)
stopifnot(all(c("boyut", "n", "r_yas_fark", "ci_alt", "ci_ust", "p", "std_beta_yas",
  "tost_p", "tost_karar", "n_kucuk", "n_buyuk", "fark_kucuk", "fark_buyuk", "statu") %in% names(con)))
con_ok <- con[con$statu_kosum == "ok", ]
stopifnot(nrow(con_ok) == length(embu_subs))
stopifnot(all(con_ok$r_yas_fark >= -1 & con_ok$r_yas_fark <= 1))
stopifnot(all(con_ok$ci_alt <= con_ok$ci_ust, na.rm = TRUE))
stopifnot(all(con_ok$n_kucuk + con_ok$n_buyuk == con_ok$n))

# ---- 4) §142 yas x transmisyon ----
tr <- f6_age_transmission(df)
stopifnot(all(c("boyut", "n", "b_ana", "b_ana_p", "b_x_yas", "ci_alt", "ci_ust",
  "etkilesim_p", "statu") %in% names(tr)))
tr_ok <- tr[tr$statu_kosum == "ok", ]
stopifnot(nrow(tr_ok) == length(embu_subs))
stopifnot(all(tr_ok$etkilesim_p >= 0 & tr_ok$etkilesim_p <= 1, na.rm = TRUE))
stopifnot(all(tr_ok$ci_alt <= tr_ok$ci_ust, na.rm = TRUE))

# ---- 5) §143 cam kardes ----
glass <- f6_glass_sibling(df)
stopifnot(all(c("severity", "generalization") %in% names(glass)))
sev <- glass$severity
stopifnot(all(c("yordayici", "boyut", "n", "r", "p", "statu") %in% names(sev)))
stopifnot(any(sev$yordayici == "dm_yili"))
gen <- glass$generalization
stopifnot(all(c("boyut", "n_kontrol", "n_dm", "cohen_d", "t_p", "tost_karar", "yorum") %in% names(gen)))
gen_ok <- gen[gen$statu_kosum == "ok", ]
stopifnot(nrow(gen_ok) == length(embu_subs))
stopifnot(all(gen_ok$t_p >= 0 & gen_ok$t_p <= 1, na.rm = TRUE))

# ---- 6) §144 distres zaman-cizgisi ----
tl <- f6_maternal_distress_timeline(df)
stopifnot(all(c("status", "shape") %in% names(tl)))
stopifnot(all(c("analiz", "n", "df_spline", "lin_slope", "lrt_F", "lrt_p", "statu") %in% names(tl$status)))
stopifnot(tl$status$statu_kosum == "ok")           # DM n=100 sentetikte
stopifnot(nrow(tl$shape) == 5L)                    # min/q1/med/q3/max
stopifnot(all(is.finite(tl$shape$beck_tahmin)))

# ---- 7) §145 kardes sicakligi moderator ----
wm <- f6_sibling_warmth_moderation(df)
stopifnot(all(c("boyut", "n", "trans_x_warmth", "trans_p", "uyum_x_warmth", "uyum_p", "statu") %in% names(wm)))
wm_ok <- wm[wm$statu_kosum == "ok", ]
stopifnot(nrow(wm_ok) == length(embu_subs))
stopifnot(all(wm_ok$trans_p >= 0 & wm_ok$trans_p <= 1, na.rm = TRUE))

# ---- 8) §146 triadik tipoloji ----
tp <- f6_triadic_typology(df, seed = 20260714L)
stopifnot(all(c("status", "fit", "profiles", "group_distribution") %in% names(tp)))
stopifnot(all(c("analiz", "n", "en_iyi_G", "bic", "entropy", "statu") %in% names(tp$status)))
stopifnot(tp$status$statu_kosum == "ok")
stopifnot(tp$status$en_iyi_G >= 1L)
stopifnot(nrow(tp$profiles) == tp$status$en_iyi_G)
stopifnot(sum(tp$profiles$n_sinif) == tp$status$n)

# ---- 9) §147 uyum yonu ----
dd <- f6_discordance_direction(df)
stopifnot(all(c("boyut", "n_kontrol", "n_dm", "bias_kontrol", "bias_dm", "grup_d",
  "grup_p", "tost_p", "tost_karar", "statu") %in% names(dd)))
dd_ok <- dd[dd$statu_kosum == "ok", ]
stopifnot(nrow(dd_ok) == length(embu_subs))
stopifnot(all(dd_ok$grup_p >= 0 & dd_ok$grup_p <= 1, na.rm = TRUE))

# ---- 10) FDR tablosu ----
fdr <- f6_fdr_table(con, tr, gen, dd, wm)
stopifnot(all(c("paragraf", "test_adi", "p_ham", "p_bh", "yontem", "statu") %in% names(fdr)))
if (nrow(fdr) > 0L) {
  stopifnot(all(fdr$p_ham >= 0 & fdr$p_ham <= 1))
  stopifnot(all(fdr$p_bh >= fdr$p_ham - 1e-9, na.rm = TRUE))
}

# ---- 11) Pipeline sarici + [KESIFSEL] statusu ----
pipe <- run_phase6_developmental_pipeline(df, seed = 20260714L)
expected <- c("age_concordance", "age_transmission", "glass_severity", "glass_generalization",
  "distress_timeline_status", "distress_timeline_shape", "sibling_warmth", "triadic_status",
  "triadic_fit", "triadic_profiles", "triadic_group_distribution", "discordance_direction",
  "fdr", "target_summary")
stopifnot(all(expected %in% names(pipe)))
stopifnot(grepl("KESIFSEL", pipe$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(grepl("DEGISMEZ", pipe$target_summary$dil_notu))
stopifnot(pipe$target_summary$n_aile == n)

# ---- 12) Determinizm: ayni seed -> ayni triadik BIC ----
p1 <- run_phase6_developmental_pipeline(df, seed = 20260714L)
p2 <- run_phase6_developmental_pipeline(df, seed = 20260714L)
stopifnot(identical(p1$triadic_status$bic, p2$triadic_status$bic))
stopifnot(identical(p1$age_transmission$b_x_yas, p2$age_transmission$b_x_yas))

cat("PASS: tests/test_phase6_developmental_dyadic.R\n")
