# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXVI (§96-99) audit runner
# Diferansiyel Ebeveynlik Etki Modellemesi (PDT). Yalniz outputs/ altina yazar;
# kanonik CSV'ye dokunmaz. Satir-duzeyi veri konsola/ciktiya dokulmez.

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/51_pdt_effect.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data

result <- run_phase3_pdt_effect_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  n_boot = 1000L,
  sesoi_r = 0.10,
  seed = 20260708L
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

write_audit_csv(result$rho_dd, "outputs/tables/phase3_pdt_rho_dd.csv")
write_audit_csv(result$rsa_surface, "outputs/tables/phase3_pdt_rsa_surface.csv")
write_audit_csv(result$magnitude_model, "outputs/tables/phase3_pdt_magnitude_model.csv")
write_audit_csv(result$direction_test, "outputs/tables/phase3_pdt_direction_test.csv")
write_audit_csv(result$path_model, "outputs/tables/phase3_pdt_path_model.csv")
write_audit_csv(result$favoritism_channels, "outputs/tables/phase3_pdt_favoritism_channels.csv")
write_audit_csv(result$favoritism_group_test, "outputs/tables/phase3_pdt_favoritism_group_test.csv")
write_audit_csv(result$favoritism_icc, "outputs/tables/phase3_pdt_favoritism_icc.csv")
write_audit_csv(result$mtmm_convergence, "outputs/tables/phase3_pdt_mtmm_convergence.csv")
write_audit_csv(result$moderation, "outputs/tables/phase3_pdt_moderation.csv")
write_audit_csv(result$moderation_slopes, "outputs/tables/phase3_pdt_moderation_slopes.csv")
write_audit_csv(result$tost, "outputs/tables/phase3_pdt_tost.csv")
write_audit_csv(result$holm, "outputs/tables/phase3_pdt_holm.csv")
write_audit_csv(result$target_summary, "outputs/tables/phase3_pdt_target_summary.csv")

# --- Konsol ozeti (yalniz agregat; satir-duzeyi veri yok) ---
ts <- result$target_summary
cat(sprintf("[Faz III/KISIM XXXVI] PDT-etki: n_aile=%d (DM=%d, Kontrol=%d), n_long=%d, n_boot=%d\n",
  ts$n_aile, ts$n_dm, ts$n_kontrol, ts$n_long, ts$n_boot))

if (!is.null(result$rho_dd) && nrow(result$rho_dd) > 0L) {
  for (i in seq_len(nrow(result$rho_dd))) {
    cat(sprintf("  [§96 rho_DD] %-14s rho_XY=%.3f rho_DD=%.3f (n=%d)\n",
      result$rho_dd$alt_olcek[i], result$rho_dd$rho_xy[i],
      result$rho_dd$rho_dd[i], result$rho_dd$n_cift[i]))
  }
}
if (!is.null(result$direction_test) && nrow(result$direction_test) > 0L) {
  for (i in seq_len(nrow(result$direction_test))) {
    cat(sprintf("  [§96 yon]   %-14s d=%.3f [%.3f, %.3f] isaret_p=%.3f holm=%.3f\n",
      result$direction_test$alt_olcek[i], result$direction_test$cohens_d[i],
      result$direction_test$d_alt_ga[i], result$direction_test$d_ust_ga[i],
      result$direction_test$isaret_testi_p[i], result$direction_test$p_holm_isaret[i]))
  }
}
if (!is.null(result$magnitude_model) && nrow(result$magnitude_model) > 0L) {
  gm <- result$magnitude_model[result$magnitude_model$terim == "group_fDM", , drop = FALSE]
  for (i in seq_len(nrow(gm))) {
    cat(sprintf("  [§96 buyukluk] %-14s group_fDM b=%.3f (robSE=%.3f) p=%.3f holm=%.3f\n",
      gm$alt_olcek[i], gm$tahmin[i], gm$robust_se[i], gm$p[i], gm$p_holm_grup[i]))
  }
}
if (!is.null(result$path_model) && nrow(result$path_model) > 0L && "std_beta" %in% names(result$path_model)) {
  ok_path <- result$path_model[!is.na(result$path_model$std_beta), , drop = FALSE]
  cat(sprintf("  [§97 yol]   %d/%d model ok; ICC araligi=[%.3f, %.3f]\n",
    sum(result$path_model$durum == "ok", na.rm = TRUE), nrow(result$path_model),
    suppressWarnings(min(ok_path$icc, na.rm = TRUE)),
    suppressWarnings(max(ok_path$icc, na.rm = TRUE))))
}
if (!is.null(result$favoritism_icc) && nrow(result$favoritism_icc) > 0L) {
  cat(sprintf("  [§98 kayirma] favoritism_icc %d satir; kanallar: %s\n",
    nrow(result$favoritism_icc), paste(unique(result$favoritism_icc$kanal), collapse = ",")))
}
if (!is.null(result$moderation) && nrow(result$moderation) > 0L && "durum" %in% names(result$moderation)) {
  cat(sprintf("  [§99 moderasyon] %d/%d etkilesim ok\n",
    sum(result$moderation$durum == "ok", na.rm = TRUE), nrow(result$moderation)))
}
if (!is.null(result$tost) && nrow(result$tost) > 0L && "karar" %in% names(result$tost)) {
  tab <- table(result$tost$karar)
  cat(sprintf("  [TOST] kararlar: %s\n",
    paste(sprintf("%s=%d", names(tab), as.integer(tab)), collapse = ", ")))
}
if (!is.null(result$holm) && nrow(result$holm) > 0L) {
  cat(sprintf("  [Holm] %d/%d karsilastirma Holm-anlamli (8 test: 4 alt olcek x 2 estimand)\n",
    sum(result$holm$anlamli_holm, na.rm = TRUE), nrow(result$holm)))
}

invisible(result)
