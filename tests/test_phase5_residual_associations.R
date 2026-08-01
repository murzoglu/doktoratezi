# [KESIFSEL - POST-HOC] Faz V KISIM L (§136-141) sentetik-veri sekil/aralik testi
source("R/64_phase5_residual_associations.R")

set.seed(20260714L)

# ---- 1) Yardimci fonksiyonlar ----
stopifnot(identical(f5_embu_subscales(),
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")))
stopifnot(identical(f5_srq_dims(), c("warmth", "status", "conflict", "rivalry")))
stopifnot(grepl("KESIFSEL", f5_status_label(), fixed = TRUE))

z <- f5_scale(c(1, 2, 3, 4, 5))
stopifnot(abs(mean(z)) < 1e-8, abs(stats::sd(z) - 1) < 1e-8)
stopifnot(all(is.na(f5_scale(rep(3, 5)))))

t_null <- f5_tost_r(r = 0.00, n = 1000L, sesoi = 0.10)
stopifnot(t_null$p >= 0, t_null$p <= 1, identical(t_null$decision, "esdeger(|r|<SESOI)"))
stopifnot(is.na(f5_tost_r(r = 0.1, n = 3L)$p))
td <- f5_tost_d(rnorm(500, 0, 1), rnorm(500, 0, 1), sesoi = 0.20)
stopifnot(td$p >= 0, td$p <= 1)

# ---- 2) Sentetik veri fixture (aile duzeyi) ----
n <- 200L
embu_subs <- f5_embu_subscales()
srq_dims <- f5_srq_dims()

df <- data.frame(
  aile_no = seq_len(n),
  group_f = factor(rep(c("DM", "Kontrol"), length.out = n), levels = c("Kontrol", "DM")),
  beck_total = pmax(0, round(stats::rnorm(n, 12, 8))),
  anne_yas = round(stats::runif(n, 28, 55)),
  ses_latent = stats::rnorm(n),
  kalabalik_indeksi = stats::runif(n, 0.3, 2.0),
  egitim_fark = sample(0:4, n, replace = TRUE),
  cift_kazanc = sample(0:1, n, replace = TRUE),
  same_sex = factor(sample(c("Ayni", "Farkli"), n, replace = TRUE)),
  aile_isei08 = round(stats::runif(n, 16, 90)),
  aile_siops08 = round(stats::runif(n, 13, 78)),
  aile_egp7 = sample(1:7, n, replace = TRUE),
  stringsAsFactors = FALSE
)
for (sub in embu_subs) {
  base <- stats::rnorm(n)
  df[[paste0("embu_p_", sub, "_mean")]] <- pmin(4, pmax(1, 2.5 + 0.3 * base + stats::rnorm(n, 0, 0.4)))
  df[[paste0("embu_c_idx_", sub, "_mean")]] <- pmin(4, pmax(1, 2.5 + 0.2 * base + stats::rnorm(n, 0, 0.5)))
}
for (dim in srq_dims) {
  df[[paste0("srq_ho_", dim, "_mean")]] <- pmin(5, pmax(1, 3 + 0.3 * stats::rnorm(n) + stats::rnorm(n, 0, 0.5)))
}

# ---- 3) §136 Beck -> SRQ ----
bs <- f5_maternal_depression_sibling(df)
stopifnot(all(c("boyut", "n", "ham_r", "ham_ci_alt", "ham_ci_ust", "ham_p",
  "std_beta", "ci_alt", "ci_ust", "p", "tost_p", "tost_karar", "statu") %in% names(bs)))
bs_ok <- bs[bs$statu_kosum == "ok", ]
stopifnot(nrow(bs_ok) == length(srq_dims))
stopifnot(all(bs_ok$ham_r >= -1 & bs_ok$ham_r <= 1))
stopifnot(all(bs_ok$ham_p >= 0 & bs_ok$ham_p <= 1, na.rm = TRUE))
stopifnot(all(bs_ok$ci_alt <= bs_ok$ci_ust, na.rm = TRUE))

# ---- 4) §137 informant transmisyon / mediasyon ----
tr <- f5_informant_transmission(df, n_boot = 100L)
stopifnot(all(c("boyut", "n", "a_yolu", "a_p", "b_yolu", "b_p", "cprime",
  "cprime_p", "dolayli", "dolayli_ci_alt", "dolayli_ci_ust", "statu") %in% names(tr)))
tr_ok <- tr[tr$statu_kosum == "ok", ]
stopifnot(nrow(tr_ok) == length(embu_subs))
stopifnot(all(tr_ok$dolayli_ci_alt <= tr_ok$dolayli_ci_ust, na.rm = TRUE))
stopifnot(all(tr_ok$a_p >= 0 & tr_ok$a_p <= 1, na.rm = TRUE))

# ---- 5) §138 asiri koruma gradyani ----
og <- f5_overprotection_gradient(df)
stopifnot(all(c("analiz", "terim", "n", "std_beta", "ci_alt", "ci_ust", "p",
  "method", "statu") %in% names(og)))
og_joint <- og[og$analiz == "birlesik_model" & og$statu_kosum == "ok", ]
stopifnot(nrow(og_joint) == 3L)  # age, ses, crowd
stopifnot(all(og_joint$terim %in% c("age", "ses", "crowd")))
stopifnot(all(og_joint$ci_alt <= og_joint$ci_ust, na.rm = TRUE))
og_biv <- og[og$analiz == "bivariate_dogrulama", ]
stopifnot(nrow(og_biv) >= 1L)

# ---- 6) §139 egitim farki ----
eg <- f5_education_gap(df)
stopifnot(all(c("yordayici", "boyut", "n", "r", "ci_alt", "ci_ust", "p", "statu") %in% names(eg)))
eg_ok <- eg[eg$statu_kosum == "ok", ]
stopifnot(nrow(eg_ok) > 0L)
stopifnot(all(eg_ok$r >= -1 & eg_ok$r <= 1, na.rm = TRUE))

# ---- 7) §140 same_sex -> SRQ ----
ss <- f5_same_sex_sibling(df)
stopifnot(all(c("boyut", "grup0", "grup1", "n0", "n1", "ort0", "ort1", "cohen_d",
  "t_p", "tost_p", "tost_karar", "statu") %in% names(ss)))
ss_ok <- ss[ss$statu_kosum == "ok", ]
stopifnot(nrow(ss_ok) == length(srq_dims))
stopifnot(all(ss_ok$t_p >= 0 & ss_ok$t_p <= 1, na.rm = TRUE))

# ---- 8) FDR tablosu ----
fdr <- f5_fdr_table(bs, eg, ss)
stopifnot(all(c("paragraf", "test_adi", "p_ham", "p_bh", "yontem", "statu") %in% names(fdr)))
if (nrow(fdr) > 0L) {
  stopifnot(all(fdr$p_ham >= 0 & fdr$p_ham <= 1))
  stopifnot(all(fdr$p_bh >= fdr$p_ham - 1e-9, na.rm = TRUE))
}

# ---- 9) Pipeline sarici: tum tablolar + [KESIFSEL - POST-HOC] statusu ----
pipe <- run_phase5_residual_associations_pipeline(df, n_boot = 100L, seed = 20260714L)
expected_tables <- c("beck_sibling", "informant_transmission", "overprotection_gradient",
  "education_gap", "same_sex_sibling", "fdr", "target_summary")
stopifnot(all(expected_tables %in% names(pipe)))
stopifnot(grepl("KESIFSEL", pipe$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(grepl("DEGISMEZ", pipe$target_summary$dil_notu))
stopifnot(pipe$target_summary$n_aile == n)

# ---- 10) Determinizm: ayni seed -> ayni dolayli etki GA ----
p1 <- run_phase5_residual_associations_pipeline(df, n_boot = 100L, seed = 20260714L)
p2 <- run_phase5_residual_associations_pipeline(df, n_boot = 100L, seed = 20260714L)
stopifnot(identical(p1$informant_transmission$dolayli_ci_alt,
  p2$informant_transmission$dolayli_ci_alt))

cat("PASS: tests/test_phase5_residual_associations.R\n")
