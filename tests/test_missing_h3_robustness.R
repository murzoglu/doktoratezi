# test_missing_h3_robustness.R
# H3 eksik-veri cercevesi saglamligi (R/63) — stopifnot; sessizse PASS.
# Kanonik targets store'undan df_family_ses/missing_results yuklenir; hiz icin
# kucuk m ile MI uretilir (uretim hedefi m=50).

suppressMessages(library(targets))
source("R/12_missing_data_frames.R")
source("R/63_missing_h3_robustness.R")

tar_load(c("missing_results", "df_family_ses"))

imp <- run_missing_imputation_set(missing_results, m = 5L, maxit = 5L)
res <- run_h3_missing_robustness(missing_results, imp)

fc <- res$framework_comparison
stopifnot(all(c("outcome", "framework", "n", "estimate", "std_error",
                "df", "ci_low", "ci_high", "p_value") %in% names(fc)))
stopifnot(setequal(unique(fc$framework), c("complete_case", "fiml", "mi_pooled")))
stopifnot(nrow(fc) == length(h3mr_outcomes()) * 3L)
stopifnot(all(is.finite(fc$estimate)))
stopifnot(all(is.finite(fc$std_error)))

# Tamamlanmis-durum aile_isei08 eksikligini dusurur (~219); FIML/MI tum 241
cc_n <- unique(fc$n[fc$framework == "complete_case"])
mi_n <- unique(fc$n[fc$framework == "mi_pooled"])
stopifnot(length(cc_n) == 1L, length(mi_n) == 1L)
fiml_n <- unique(fc$n[fc$framework == "fiml"])
stopifnot(cc_n < mi_n)                        # complete-case daha kucuk N
stopifnot(mi_n == fiml_n)                     # MI ve FIML tum orneklem (241)

# Reddetme grup etkisi uc cercevede yakin (SES-eksikligi null'i bozmaz)
red <- fc[fc$outcome == "embu_p_reddetme_mean", ]
stopifnot(max(red$estimate) - min(red$estimate) < 0.10)

# NMAR delta izgarasi
ds <- res$nmar_delta_sensitivity
stopifnot(all(c("outcome", "delta", "estimate", "ci_low", "ci_high", "p_value") %in% names(ds)))
stopifnot(setequal(unique(ds$delta), c(-1, -0.5, 0, 0.5, 1)))
stopifnot(nrow(ds) == length(h3mr_outcomes()) * 5L)
stopifnot(all(is.finite(ds$estimate)))

# delta = 0, mi_pooled ile tutarli (ayni imputasyon, ayarlama yok)
z0 <- ds$estimate[ds$delta == 0 & ds$outcome == "embu_p_reddetme_mean"]
mip <- fc$estimate[fc$framework == "mi_pooled" & fc$outcome == "embu_p_reddetme_mean"]
stopifnot(abs(z0 - mip) < 1e-6)

# delta uygulamasi gercekten satir ayarliyor (delta uclari farkli tahmin verir)
spread_delta <- {
  r <- ds$estimate[ds$outcome == "embu_p_reddetme_mean"]
  max(r) - min(r)
}
stopifnot(spread_delta > 0)                  # no-op degil (aile_isei08 22 NA ayarlandi)

# --- SES operasyonellestirme saglamligi (Hollingshead paralel) ---
ses_op <- run_h3_ses_operationalization(df_family_ses)
stopifnot(all(c("ses_measure", "ses_label", "outcome", "n",
                "estimate", "ci_low", "ci_high", "p_value") %in% names(ses_op)))
stopifnot(nrow(ses_op) == length(h3mr_outcomes()) * length(h3ses_measures()))  # 4x4 = 16
stopifnot("ses_hollingshead" %in% ses_op$ses_measure)
stopifnot(all(is.finite(ses_op$estimate)))
red_ses <- ses_op$estimate[ses_op$outcome == "embu_p_reddetme_mean"]
stopifnot(max(red_ses) - min(red_ses) < 0.05)   # SES olcusune dayanikli null

cat("test_missing_h3_robustness PASS (cc_n=", cc_n, " mi_n=", mi_n,
    " reddetme_spread=", round(max(red$estimate) - min(red$estimate), 4),
    " delta_spread=", round(spread_delta, 4), ")\n", sep = "")
