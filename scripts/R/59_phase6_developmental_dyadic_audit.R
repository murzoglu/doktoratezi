# [KESIFSEL - POST-HOC] Faz VI SAP KISIM LI (§142-151) audit runner
#
# Gelisimsel-Diadik Olcum Yuzeyi (Developmental-Dyadic Surface) — OSF Layer 7.
# I/O YALNIZ bu runner'da; ciktilar YALNIZ outputs/tables/ altina yazilir.
# Kanonik CSV'lere yazma yoktur; yukleme R/01_io.R uzerinden dogrulanir.
# Konsola yalniz agregat/kosum durumu yazilir; satir-duzeyi veri DOKULMEZ.

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/65_phase6_developmental_dyadic.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data

result <- run_phase6_developmental_pipeline(
  df_family_ses = df_family_ses,
  sesoi_r = 0.10,
  sesoi_d = 0.20,
  seed = 20260714L
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

write_audit_csv <- function(df, path) {
  if (is.null(df) || nrow(df) == 0L) {
    stub <- data.frame(note = "empty result", statu = "[KESIFSEL - POST-HOC]",
      stringsAsFactors = FALSE)
    utils::write.csv(stub, path, row.names = FALSE, fileEncoding = "UTF-8")
  } else {
    utils::write.csv(df, path, row.names = FALSE, fileEncoding = "UTF-8")
  }
}

write_audit_csv(result$age_concordance,       "outputs/tables/phase6_age_concordance.csv")
write_audit_csv(result$age_transmission,      "outputs/tables/phase6_age_transmission.csv")
write_audit_csv(result$glass_severity,        "outputs/tables/phase6_glass_severity.csv")
write_audit_csv(result$glass_generalization,  "outputs/tables/phase6_glass_generalization.csv")
write_audit_csv(result$distress_timeline_status, "outputs/tables/phase6_distress_timeline_status.csv")
write_audit_csv(result$distress_timeline_shape,  "outputs/tables/phase6_distress_timeline_shape.csv")
write_audit_csv(result$sibling_warmth,        "outputs/tables/phase6_sibling_warmth.csv")
write_audit_csv(result$triadic_status,        "outputs/tables/phase6_triadic_status.csv")
write_audit_csv(result$triadic_fit,           "outputs/tables/phase6_triadic_fit.csv")
write_audit_csv(result$triadic_profiles,      "outputs/tables/phase6_triadic_profiles.csv")
write_audit_csv(result$triadic_group_distribution, "outputs/tables/phase6_triadic_group_distribution.csv")
write_audit_csv(result$discordance_direction, "outputs/tables/phase6_discordance_direction.csv")
write_audit_csv(result$fdr,                    "outputs/tables/phase6_fdr.csv")
write_audit_csv(result$target_summary,        "outputs/tables/phase6_target_summary.csv")

# --- Konsol ozeti (yalniz agregat) ---
cat("=== Faz VI KISIM LI — Gelisimsel-Diadik Olcum Yuzeyi (§142-151) ===\n")

con <- result$age_concordance; con_ok <- con[con$statu_kosum == "ok", , drop = FALSE]
if (nrow(con_ok) > 0L) {
  cat("[§142a yas->|anne-cocuk farki|] (negatif r = yasla uyum artar):\n")
  for (i in seq_len(nrow(con_ok))) {
    cat(sprintf("  %-13s r=%.3f [%.3f, %.3f] p=%.3f | <10 fark=%.3f (n=%d) vs >=10 fark=%.3f (n=%d)\n",
      con_ok$boyut[i], con_ok$r_yas_fark[i], con_ok$ci_alt[i], con_ok$ci_ust[i], con_ok$p[i],
      con_ok$fark_kucuk[i], con_ok$n_kucuk[i], con_ok$fark_buyuk[i], con_ok$n_buyuk[i]))
  }
}
tr <- result$age_transmission; tr_ok <- tr[tr$statu_kosum == "ok", , drop = FALSE]
if (nrow(tr_ok) > 0L) {
  cat("[§142b transmisyon b-yolu x yas] (etkilesim; pozitif=buyuk cocukta guclu):\n")
  for (i in seq_len(nrow(tr_ok))) {
    cat(sprintf("  %-13s b_ana=%.3f(p=%.3f) b:yas=%.3f [%.3f, %.3f] p=%.3f\n",
      tr_ok$boyut[i], tr_ok$b_ana[i], tr_ok$b_ana_p[i], tr_ok$b_x_yas[i],
      tr_ok$ci_alt[i], tr_ok$ci_ust[i], tr_ok$etkilesim_p[i]))
  }
}
sev <- result$glass_severity; sev_ok <- sev[sev$statu_kosum %in% c("ok", "betimsel_dusuk_guc"), , drop = FALSE]
if (nrow(sev_ok) > 0L) {
  cat("[§143a indeks hastalik-yuku -> kardes algisi] (DM-only; betimsel):\n")
  for (i in seq_len(nrow(sev_ok))) {
    cat(sprintf("  %-8s -> kardes_%-13s r=%.3f [%.3f, %.3f] p=%.3f (n=%d)\n",
      sev_ok$yordayici[i], sev_ok$boyut[i], sev_ok$r[i], sev_ok$ci_alt[i], sev_ok$ci_ust[i],
      sev_ok$p[i], sev_ok$n[i]))
  }
}
gen <- result$glass_generalization; gen_ok <- gen[gen$statu_kosum == "ok", , drop = FALSE]
if (nrow(gen_ok) > 0L) {
  cat("[§143b kardes EMBU-C: DM_Hasta_Kardes vs Kontrol_Kardes] (d=DM-Kontrol):\n")
  for (i in seq_len(nrow(gen_ok))) {
    cat(sprintf("  %-13s Kontrol=%.2f DM=%.2f d=%.3f p=%.3f | TOST(d=.20) %s\n",
      gen_ok$boyut[i], gen_ok$ort_kontrol[i], gen_ok$ort_dm[i], gen_ok$cohen_d[i],
      gen_ok$t_p[i], gen_ok$tost_karar[i]))
  }
}
tl <- result$distress_timeline_status
if (tl$statu_kosum == "ok") {
  cat(sprintf("[§144 Beck ~ ns(dm_yili,3)] lineer egim=%.3f(p=%.3f) spline-LRT F=%.2f p=%.3f (n=%d)\n",
    tl$lin_slope, tl$lin_p, tl$lrt_F, tl$lrt_p, tl$n))
  sh <- result$distress_timeline_shape
  if (nrow(sh) > 0L) cat(sprintf("  Beck tahmin (dm_yili %s): %s\n",
    paste(sh$dm_yili, collapse = "/"), paste(sprintf("%.1f", sh$beck_tahmin), collapse = "/")))
}
wm <- result$sibling_warmth; wm_ok <- wm[wm$statu_kosum == "ok", , drop = FALSE]
if (nrow(wm_ok) > 0L) {
  cat("[§145 kardes sicakligi x transmisyon] (M:W etkilesim):\n")
  cat(sprintf("  %s\n", paste(sprintf("%s=%.3f(p=%.3f)", wm_ok$boyut, wm_ok$trans_x_warmth,
    wm_ok$trans_p), collapse = ", ")))
}
ts <- result$triadic_status
if (ts$statu_kosum == "ok") {
  cat(sprintf("[§146 triadik LPA] en iyi: G=%d (model %d) BIC=%.1f entropy=%.3f (n=%d)\n",
    ts$en_iyi_G, ts$en_iyi_model, ts$bic, ts$entropy, ts$n))
  gd <- result$triadic_group_distribution
  if (nrow(gd) > 0L) { cat("  sinif x grup dagilimi:\n"); print(gd[, setdiff(names(gd), "statu")], row.names = FALSE) }
}
dd <- result$discordance_direction; dd_ok <- dd[dd$statu_kosum == "ok", , drop = FALSE]
if (nrow(dd_ok) > 0L) {
  cat("[§147 isaretli bias (anne-indeks) x grup] (+ = anne oz-yuceltme):\n")
  for (i in seq_len(nrow(dd_ok))) {
    cat(sprintf("  %-13s Kontrol=%.3f(p=%.3f) DM=%.3f(p=%.3f) grup_d=%.3f p=%.3f\n",
      dd_ok$boyut[i], dd_ok$bias_kontrol[i], dd_ok$bias_kontrol_p[i], dd_ok$bias_dm[i],
      dd_ok$bias_dm_p[i], dd_ok$grup_d[i], dd_ok$grup_p[i]))
  }
}
fdr <- result$fdr
if (nrow(fdr) > 0L) {
  cat(sprintf("[FDR/BH] %d test; FDR-dayanikli (p_bh<.05)=%d\n",
    nrow(fdr), sum(fdr$p_bh < 0.05, na.rm = TRUE)))
  surv <- fdr[!is.na(fdr$p_bh) & fdr$p_bh < 0.05, , drop = FALSE]
  if (nrow(surv) > 0L) for (i in seq_len(nrow(surv)))
    cat(sprintf("   * %s %s: p_ham=%.3f p_bh=%.3f\n", surv$paragraf[i], surv$test_adi[i],
      surv$p_ham[i], surv$p_bh[i]))
}
cat(sprintf("Durum: TAMAM (n_aile=%d). Tum tablolar outputs/tables/phase6_*.csv\n",
  result$target_summary$n_aile))

invisible(result)
