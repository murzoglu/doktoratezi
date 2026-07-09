# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXVII (§100-102b) audit runner
# Sosyal Tabakalasma Genisletmesi — R/52_social_stratification.R sarici kosumu.
# Cikti: outputs/tables/phase3_strat_*.csv (yalniz outputs/ altina yazilir).

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/52_social_stratification.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- derive_ses_composites(df_family_scored)$data

ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f) - 1L
    } else if ("group" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$group), ignore.case = TRUE))
    }
  }
  df
}
df_family_ses <- ensure_group_dm(df_family_ses)

result <- run_phase3_social_stratification_pipeline(
  df_family_ses = df_family_ses,
  df_long_scored = df_long_scored,
  df_family_scored = df_family_scored,
  boot_n = 1000L,
  seed = 20260708L
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write_audit_csv <- function(df, path) {
  if (is.null(df) || nrow(df) == 0L) {
    stub <- data.frame(
      note = "bos sonuc (stub)",
      statu = "[KESIFSEL - POST-HOC]",
      stringsAsFactors = FALSE
    )
    utils::write.csv(stub, path, row.names = FALSE, fileEncoding = "UTF-8")
  } else {
    utils::write.csv(df, path, row.names = FALSE, fileEncoding = "UTF-8")
  }
}

write_audit_csv(result$egp_gradient, "outputs/tables/phase3_strat_egp_gradient.csv")
write_audit_csv(result$egp_gradient_omnibus, "outputs/tables/phase3_strat_egp_gradient_omnibus.csv")
write_audit_csv(result$egp_simpson, "outputs/tables/phase3_strat_egp_simpson.csv")
write_audit_csv(result$measurement_race, "outputs/tables/phase3_strat_measurement_race.csv")
write_audit_csv(result$drm_education, "outputs/tables/phase3_strat_drm_education.csv")
write_audit_csv(result$material_hierarchical, "outputs/tables/phase3_strat_material_hierarchical.csv")
write_audit_csv(result$fsm_mediation, "outputs/tables/phase3_strat_fsm_mediation.csv")
write_audit_csv(result$employment_moderation, "outputs/tables/phase3_strat_employment_moderation.csv")
write_audit_csv(result$tost, "outputs/tables/phase3_strat_tost.csv")
write_audit_csv(result$status_summary, "outputs/tables/phase3_strat_status_summary.csv")

# --- Konsol ozeti (satir-duzeyi veri DOKULMEZ; yalniz agregat) ---
ss <- result$status_summary
cat(sprintf(
  "[Faz III/KISIM XXXVII] n_aile=%d n_long=%d | EGP-3: hizmet=%d ara=%d isci_rutin=%d (yapisal NA=%d)\n",
  ss$n_aile, ss$n_long, ss$egp3_hizmet, ss$egp3_ara, ss$egp3_isci_rutin, ss$egp3_yapisal_na
))

if (!is.null(result$egp_gradient_omnibus)) {
  om <- result$egp_gradient_omnibus
  n_sig <- sum(!is.na(om$p_holm) & om$p_holm < 0.05)
  cat(sprintf("[§100] EGP gradyan omnibus: %d satir (%d Holm<.05); duzeyler: %s\n",
    nrow(om), n_sig, paste(unique(om$duzey), collapse = "/")))
}
if (!is.null(result$measurement_race)) {
  mr <- result$measurement_race
  cat(sprintf("[§100/1.6-C] Olcum-yarisi: %d satir, %d alt olcek (ISEI/SIOPS/EGP + ortak)\n",
    nrow(mr), length(unique(mr$olcum))))
}
if (!is.null(result$drm_education)) {
  drm <- result$drm_education
  cat(sprintf("[§101] Egitim-DRM: %d cikti; durum(lar): %s\n",
    nrow(drm), paste(unique(drm$durum), collapse = ", ")))
  for (i in seq_len(nrow(drm))) {
    if (startsWith(drm$durum[i], "yakinsadi")) {
      cat(sprintf("   %s: w_anne=%.3f [%.3f, %.3f], w_baba=%.3f (n=%d)\n",
        drm$olcum[i], drm$w_anne[i], drm$w_anne_ga_alt[i], drm$w_anne_ga_ust[i],
        drm$w_baba[i], drm$n[i]))
    }
  }
}
if (!is.null(result$material_hierarchical)) {
  mh <- result$material_hierarchical
  cat(sprintf("[§102] Materyal hiyerarsik: %d cikti; ortalama deltaR2=%.4f\n",
    nrow(mh), mean(mh$delta_r2, na.rm = TRUE)))
}
if (!is.null(result$fsm_mediation)) {
  fsm <- result$fsm_mediation
  ind <- fsm[fsm$parametre == "dolayli" & fsm$durum == "ok", , drop = FALSE]
  cat(sprintf("[§102] Beck-araci FSM: %d parametre satiri; dolayli etki(ler):\n", nrow(fsm)))
  for (i in seq_len(nrow(ind))) {
    cat(sprintf("   %s dolayli=%.4f [%.4f, %.4f] p=%.3f\n",
      ind$olcum[i], ind$tahmin[i], ind$ci_alt[i], ind$ci_ust[i], ind$p_deger[i]))
  }
}
if (!is.null(result$employment_moderation)) {
  emp <- result$employment_moderation
  int_ok <- emp[grepl(":", emp$terim) & emp$durum == "ok", , drop = FALSE]
  cat(sprintf("[§102b] Anne istihdami × grup: %d katsayi satiri, %d etkilesim terimi\n",
    nrow(emp), nrow(int_ok)))
}
if (!is.null(result$tost)) {
  tost <- result$tost
  n_eq <- sum(tost$karar == "esdeger(SESOI ici)", na.rm = TRUE)
  cat(sprintf("[TOST |r|=.10] %d etkilesim testi, %d esdeger karari\n", nrow(tost), n_eq))
}

invisible(result)
