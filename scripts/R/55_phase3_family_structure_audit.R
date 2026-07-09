# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXIX (§107-109) audit runner
#
# Aile Yapisi ve Kardes Konstelasyonu.
# I/O YALNIZ bu runner'da; ciktilar YALNIZ outputs/tables/ altina yazilir.
# Kanonik CSV'lere yazma yoktur; yukleme R/01_io.R uzerinden dogrulanir.
# Konsola yalniz agregat/koşum durumu yazilir; satir-duzeyi veri DOKULMEZ.

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/54_family_structure_sibship.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)

result <- run_phase3_family_structure_pipeline(
  df_family_scored = df_family_scored,
  df_long_scored = df_long_scored,
  sesoi_r = 0.10
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

write_audit_csv <- function(df, path) {
  if (is.null(df) || nrow(df) == 0L) {
    stub <- data.frame(
      note = "empty result",
      statu = "[KESIFSEL - POST-HOC]",
      stringsAsFactors = FALSE
    )
    utils::write.csv(stub, path, row.names = FALSE, fileEncoding = "UTF-8")
  } else {
    utils::write.csv(df, path, row.names = FALSE, fileEncoding = "UTF-8")
  }
}

write_audit_csv(result$single_parent_descriptive,
  "outputs/tables/phase3_family_single_parent_descriptive.csv")
write_audit_csv(result$birth_order_within,
  "outputs/tables/phase3_family_birth_order_within.csv")
write_audit_csv(result$sibship_dilution,
  "outputs/tables/phase3_family_sibship_dilution.csv")
write_audit_csv(result$reciprocity_correlations,
  "outputs/tables/phase3_family_reciprocity_correlations.csv")
write_audit_csv(result$variance_decomposition,
  "outputs/tables/phase3_family_variance_decomposition.csv")
write_audit_csv(result$same_sex_age_gap,
  "outputs/tables/phase3_family_same_sex_age_gap.csv")
write_audit_csv(result$fdr,
  "outputs/tables/phase3_family_fdr.csv")
write_audit_csv(result$target_summary,
  "outputs/tables/phase3_family_target_summary.csv")

# --- Konsol ozeti (yalniz agregat) ---
cat("=== Faz III KISIM XXXIX — Aile Yapisi & Kardes Konstelasyonu ===\n")

sp <- result$single_parent_descriptive
sp_tek <- sp[sp$gosterge == "tek_ebeveyn (birlesik)", , drop = FALSE]
cat(sprintf("[§107 Tier D] Tek-ebeveyn n=%d (DM=%d, Kontrol=%d) -> moderasyon YAPILAMAZ (betimsel)\n",
  sp_tek$n[1], sp_tek$n_dm[1], sp_tek$n_kontrol[1]))

bw <- result$birth_order_within
bw_bo <- bw[bw$terim == "dogum_sirasi_farki" & bw$statu_kosum == "ok", , drop = FALSE]
cat(sprintf("[§108a within-family] %d/%d alt-olcek tahmin edildi; |std_beta| ortanca=%.3f\n",
  nrow(bw_bo), length(fam_struct_embu_subscales()),
  if (nrow(bw_bo) > 0L) stats::median(abs(bw_bo$std_beta), na.rm = TRUE) else NA_real_))

sd_tab <- result$sibship_dilution
sd_ok <- sd_tab[sd_tab$statu_kosum == "ok", , drop = FALSE]
cat(sprintf("[§108b dilution] %d/%d cikti (lme4); cocuk_sayisi std_beta: %s\n",
  nrow(sd_ok), nrow(sd_tab),
  if (nrow(sd_ok) > 0L) paste(sprintf("%s=%.3f", sd_ok$boyut, sd_ok$std_beta), collapse = ", ") else "NA"))

rc <- result$reciprocity_correlations
rc_ok <- rc[rc$statu_kosum == "ok", , drop = FALSE]
if (nrow(rc_ok) > 0L) {
  cat("[§109 intrapair r + TOST]\n")
  for (i in seq_len(nrow(rc_ok))) {
    cat(sprintf("  %-9s r=%.3f [%.3f, %.3f] n=%d | TOST(|r|=.10) p=%.3f -> %s\n",
      rc_ok$boyut[i], rc_ok$intrapair_r[i], rc_ok$r_ci_alt[i], rc_ok$r_ci_ust[i],
      rc_ok$n[i], rc_ok$tost_p[i], rc_ok$tost_karar[i]))
  }
}

vd <- result$variance_decomposition
vd_ok <- vd[vd$statu_kosum == "ok", , drop = FALSE]
if (nrow(vd_ok) > 0L) {
  cat("[§109 varyans ayrisimi] common-fate orani (duad-ort / toplam):\n")
  cat(sprintf("  %s\n", paste(sprintf("%s=%.2f", vd_ok$boyut, vd_ok$oran_common_fate), collapse = ", ")))
}

fdr <- result$fdr
if (nrow(fdr) > 0L) {
  cat(sprintf("[FDR/BH] %d test; anlamli (p_bh<.05)=%d\n",
    nrow(fdr), sum(fdr$p_bh < 0.05, na.rm = TRUE)))
}

cat(sprintf("Durum: TAMAM (n_aile=%d). Tum tablolar outputs/tables/phase3_family_*.csv\n",
  result$target_summary$n_aile))

invisible(result)
