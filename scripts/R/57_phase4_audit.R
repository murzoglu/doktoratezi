# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLII-XLIX (§116-135) audit runner
# Saf fonksiyonlar R/56-62; bu runner I/O yapar ve YALNIZ outputs/tables/ altina
# yazar. Kanonik CSV'ler yalniz R/01_io.R uzerinden hash-dogrulamali yuklenir.
# Yeni veri toplanmaz; kanonik kilit DEGISMEZ; H1-H5 confirmatory cekirdek DEGISMEZ.

suppressMessages({
  source("R/07_reproducibility.R")
  source("R/01_io.R")
  source("R/10_derived_scores.R")
  source("R/11_ses_composites.R")
  source("R/24_latent_profile.R")
  source("R/56_directional_sibship.R")
  source("R/57_child_level_moderators.R")
  source("R/58_onset_metabolic_context.R")
  source("R/59_family_health_validity.R")
  source("R/60_derived_structural.R")
  source("R/61_maternal_mh_child_plane.R")
  source("R/62_selection_batch_validity.R")
})

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_long_scored <- derive_long_scores(df_long)
df_family_ses <- tryCatch(
  derive_ses_composites(df_family_scored)$data,
  error = function(e) {
    message(sprintf("[UYARI] SES kompozit turetilemedi (%s); ses_latent NA.", conditionMessage(e)))
    df_family_scored$ses_latent <- NA_real_
    df_family_scored
  }
)
supplement <- utils::read.csv("data/processed/SUPPLEMENT__es_yas_recovered.csv",
  stringsAsFactors = FALSE)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

# Sonuc listesindeki her data.frame'i outputs/tables/phase4_<prefix>_<ad>.csv yazar.
write_result_list <- function(res, prefix) {
  written <- character(0)
  for (nm in names(res)) {
    obj <- res[[nm]]
    path <- sprintf("outputs/tables/phase4_%s_%s.csv", prefix, nm)
    if (is.null(obj) || (is.data.frame(obj) && nrow(obj) == 0L)) {
      stub <- data.frame(note = "bos sonuc (stub)", statu = "[KESIFSEL - POST-HOC]",
        stringsAsFactors = FALSE)
      utils::write.csv(stub, path, row.names = FALSE, fileEncoding = "UTF-8")
    } else if (is.data.frame(obj)) {
      utils::write.csv(obj, path, row.names = FALSE, fileEncoding = "UTF-8")
    } else {
      next
    }
    written <- c(written, path)
  }
  written
}

cat("=== Faz IV audit runner — KISIM XLII-XLIX ===\n")

# --- §134-135 (yurutme onceligi #1: gecerlik denetimleri) ---
res_selb <- run_phase4_selection_batch_pipeline(df_family_ses)
write_result_list(res_selb, "selb")
f <- res_selb$hba1c_ad_fisher; cc <- res_selb$year_collinearity
cat(sprintf("[§134] HbA1c-avail x AD: OR=%.2f [%.2f,%.2f] p=%.6f (n_dm=%d, var=%d)\n",
  f$odds_ratio, f$or_ci_lower, f$or_ci_upper, f$p_value, f$n_dm, res_selb$target_summary$n_hba1c_var))
cat(sprintf("[§135] yil x grup kollinearite: LR chisq=%.1f df=%d p=%.2e V=%.3f\n",
  cc$lr_chisq, cc$lr_df, cc$p_value, cc$cramers_v))

# --- §130-133 (maternal MH → cocuk duzlemi) ---
res_mmcp <- run_phase4_maternal_mh_pipeline(df_long_scored, df_family_ses, seed = 20260708L)
write_result_list(res_mmcp, "mmcp")
mm <- res_mmcp$lca_contract_meta
cat(sprintf("[§130-133] LCA best_n=%s entropy=%.3f (adaptif=%s/riskli=%s)\n",
  mm$best_n, mm$entropy_overall, mm$n_adaptif, mm$n_riskli))

# --- §116-118 (yonlu kardes-iliski) ---
res_dsib <- run_phase4_directional_sibship_pipeline(df_long_scored, df_family_scored)
write_result_list(res_dsib, "dsib")
ff <- res_dsib$facet_forest_117
cat(sprintf("[§117] 14-faset forest: FDR-hayatta=%d/%d (dusuk-guvenilir=%d)\n",
  sum(ff$fdr_hayatta, na.rm = TRUE), nrow(ff), sum(!ff$guvenilir, na.rm = TRUE)))

# --- §119-120 (cocuk-duzeyi moderatorler) ---
res_clmod <- run_phase4_child_moderators_pipeline(df_long_scored, df_family_ses)
write_result_list(res_clmod, "clmod")

# --- §121-122 (onset/metabolik, DM-only) ---
res_onmet <- run_phase4_onset_metabolic_pipeline(df_family_ses)
write_result_list(res_onmet, "onmet")

# --- §123-124 (aile saglik profili/gecerlik) ---
res_fhv <- run_phase4_family_health_pipeline(df_family_ses)
write_result_list(res_fhv, "fhv")
cf <- res_fhv$coding_fidelity_124
cat(sprintf("[§124] kodlama-sadakati κ: anne=%.2f es=%.2f (veri-audit; bagimsiz gecerlik DEGIL)\n",
  cf$kappa[cf$bilgi_kaynagi == "anne"], cf$kappa[cf$bilgi_kaynagi == "es"]))

# --- §125 (turetilebilir yapisal) ---
res_dstr <- run_phase4_derived_structural_pipeline(df_family_ses, supplement)
write_result_list(res_dstr, "dstr")

n_csv <- length(list.files("outputs/tables", pattern = "^phase4_.*\\.csv$"))
cat(sprintf("\n[TAMAM] Faz IV: %d adet phase4_*.csv yazildi.\n", n_csv))
invisible(TRUE)
