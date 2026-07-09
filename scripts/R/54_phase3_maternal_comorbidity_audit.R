# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXVIII/103-106 audit runner
# Anne somatik komorbidite ve aile saglik yuku. I/O yalniz burada;
# kanonik CSV'ye yazma yok; ciktilar yalniz outputs/tables/ altina.

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/53_maternal_comorbidity.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data

# group_dm garanti (Kontrol=0 / DM=1)
df_family_ses <- mc_ensure_group_dm(df_family_ses)

result <- run_phase3_maternal_comorbidity_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  mediation_boot = 1000L,
  sesoi_r = 0.10,
  seed = 20260708L
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write_audit_csv <- function(df, path) {
  if (is.null(df) || nrow(df) == 0L) {
    stub <- data.frame(
      note = "bos sonuc",
      statu = "[KESIFSEL - POST-HOC]",
      stringsAsFactors = FALSE
    )
    utils::write.csv(stub, path, row.names = FALSE, fileEncoding = "UTF-8")
  } else {
    utils::write.csv(df, path, row.names = FALSE, fileEncoding = "UTF-8")
  }
}

write_audit_csv(result$autoimmune_prevalence,
  "outputs/tables/phase3_comorbid_autoimmune_prevalence.csv")
write_audit_csv(result$comorbid_binary_effects,
  "outputs/tables/phase3_comorbid_binary_effects.csv")
write_audit_csv(result$comorbid_mediation,
  "outputs/tables/phase3_comorbid_mediation.csv")
write_audit_csv(result$distress_convergence,
  "outputs/tables/phase3_comorbid_distress_convergence.csv")
write_audit_csv(result$antidep_group,
  "outputs/tables/phase3_comorbid_antidep_group.csv")
write_audit_csv(result$negative_control,
  "outputs/tables/phase3_comorbid_negative_control.csv")
write_audit_csv(result$negative_control_tost,
  "outputs/tables/phase3_comorbid_tost.csv")
write_audit_csv(result$target_summary,
  "outputs/tables/phase3_comorbid_target_summary.csv")

# --- Konsol ozeti (yalniz agregat; satir-duzeyi veri DOKULMEZ) --------------
cat("=== Faz III / KISIM XXXVIII — Anne Komorbidite Audit ===\n")

ap <- result$autoimmune_prevalence
if (!is.null(ap) && "gosterge" %in% names(ap)) {
  for (i in seq_len(nrow(ap))) {
    cat(sprintf("[103 Tier D] %s: DM %d/%d (%.1f%%) vs Kontrol %d/%d (%.1f%%); Fisher p=%.3f [TEST EDILEMEZ=%s]\n",
      ap$gosterge[i], ap$dm_pozitif[i], ap$dm_toplam[i], ap$dm_prevalans_pct[i],
      ap$kontrol_pozitif[i], ap$kontrol_toplam[i], ap$kontrol_prevalans_pct[i],
      ap$fisher_p[i], ap$test_edilebilir[i]))
  }
}

be <- result$comorbid_binary_effects
if (!is.null(be) && "outcome" %in% names(be)) {
  cat(sprintf("[104 Tier C] ikili komorbidite (n_var=%d / n_yok=%d):\n",
    be$n_komorbid_var[1], be$n_komorbid_yok[1]))
  for (i in seq_len(nrow(be))) {
    cat(sprintf("   %-24s d=%.3f [%.3f, %.3f] Welch p=%.3f (Holm=%.3f)\n",
      be$outcome[i], be$cohen_d[i], be$d_ci_low[i], be$d_ci_high[i],
      be$welch_p[i], be$welch_p_holm[i]))
  }
}

med <- result$comorbid_mediation
if (!is.null(med) && "effect" %in% names(med)) {
  ind <- med[med$effect == "indirect", , drop = FALSE]
  for (i in seq_len(nrow(ind))) {
    cat(sprintf("[104 aracilik] %s indirect=%.3f BCa[%.3f, %.3f] (n=%d, boot=%d)\n",
      ind$outcome_subscale[i], ind$estimate[i], ind$ci_low[i], ind$ci_high[i],
      ind$n[i], ind$n_boot[i]))
  }
}

ag <- result$antidep_group
if (!is.null(ag) && "chisq" %in% names(ag)) {
  cat(sprintf("[105 Tier B-] antidepresan x grup: DM %d/%d (%.1f%%) vs Kontrol %d/%d (%.1f%%); chi2=%.2f p=%.3f; V=%.3f\n",
    ag$dm_var, ag$dm_toplam, ag$dm_pct, ag$kontrol_var, ag$kontrol_toplam,
    ag$kontrol_pct, ag$chisq, ag$chisq_p, ag$cramers_v))
}

dc <- result$distress_convergence
if (!is.null(dc) && "metrik" %in% names(dc)) {
  rpb <- dc[dc$metrik == "nokta_biserial_r", , drop = FALSE]
  if (nrow(rpb) > 0L) {
    cat(sprintf("[105 yakinsama] antidepresan<->beck r=%.3f [%.3f, %.3f] (n=%d)\n",
      rpb$deger[1], rpb$ci_low[1], rpb$ci_high[1], rpb$n[1]))
  }
}

nc <- result$negative_control
if (!is.null(nc) && "outcome_subscale" %in% names(nc)) {
  base <- nc[nc$model == "temel", , drop = FALSE]
  for (i in seq_len(nrow(base))) {
    cat(sprintf("[106 negatif kontrol] EMBU-C %-14s beta=%.3f [%.3f, %.3f] p=%.3f (Holm=%.3f) [%s n_obs=%s]\n",
      base$outcome_subscale[i], base$beta[i], base$ci_low[i], base$ci_high[i],
      base$p[i], base$p_holm[i], base$status[i], as.character(base$n_obs[i])))
  }
}

tost <- result$negative_control_tost
if (!is.null(tost) && "outcome_subscale" %in% names(tost)) {
  for (i in seq_len(nrow(tost))) {
    cat(sprintf("[106 TOST |r|=%.2f] EMBU-C %-14s r=%.3f tost_p=%.3f -> %s (n=%s)\n",
      tost$sesoi_r[i], tost$outcome_subscale[i], tost$r[i], tost$tost_p[i],
      as.character(tost$tost_karar[i]), as.character(tost$n[i])))
  }
}

cat("=== Ciktilar: outputs/tables/phase3_comorbid_*.csv (UTF-8) ===\n")
invisible(result)
