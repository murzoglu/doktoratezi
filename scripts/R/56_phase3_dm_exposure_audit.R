# [KESIFSEL - POST-HOC] Faz III SAP KISIM XL/110-111 audit runner
# DM-Spesifik Maruziyet Yogunlugu (DM-only, n=120).
# Saf fonksiyonlar R/55_dm_exposure_intensity.R; bu runner I/O yapar ve YALNIZ
# outputs/tables/ altina yazar. Kanonik CSV'ler yalniz R/01_io.R uzerinden yuklenir.

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/55_dm_exposure_intensity.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)

# SES kompozitleri (ses_latent kovaryati icin); basarisiz olursa NA ile devam
df_family_ses <- tryCatch(
  derive_ses_composites(df_family_scored)$data,
  error = function(e) {
    message(sprintf("[UYARI] SES kompozit turetilemedi (%s); ses_latent NA olarak devam.",
      conditionMessage(e)))
    df_family_scored$ses_latent <- NA_real_
    df_family_scored
  }
)

result <- run_phase3_dm_exposure_pipeline(
  df_family_scored = df_family_ses,
  sesoi_r = 0.10
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

write_audit_csv(result$life_ratio_validity,
  "outputs/tables/phase3_dmexp_life_ratio_validity.csv")
write_audit_csv(result$exposure_parametrizations,
  "outputs/tables/phase3_dmexp_exposure_parametrizations.csv")
write_audit_csv(result$overprotection_models,
  "outputs/tables/phase3_dmexp_overprotection_models.csv")
write_audit_csv(result$psychcontrol_sideanalysis,
  "outputs/tables/phase3_dmexp_psychcontrol_sideanalysis.csv")
write_audit_csv(result$sibling_window_descriptive,
  "outputs/tables/phase3_dmexp_sibling_window_descriptive.csv")
write_audit_csv(result$target_summary,
  "outputs/tables/phase3_dmexp_target_summary.csv")

# --- Konsol ozeti (yalniz agregat; satir-duzeyi veri dokulmez) ---
ts <- result$target_summary
cat(sprintf(
  "[Faz III/KISIM XL] DM maruziyet: n_dm=%d | oran gecerli=%d, aralik-disi=%d\n",
  ts$n_dm, ts$n_ratio_gecerli, ts$n_ratio_aralik_disi))

vr <- result$life_ratio_validity
ratio_row <- vr[vr$degisken == "illness_life_ratio", , drop = FALSE]
if (nrow(ratio_row) == 1L) {
  cat(sprintf(
    "[§110.1] illness_life_ratio: ort=%.3f medyan=%.3f aralik=[%.3f, %.3f] n_aralik_disi=%d\n",
    ratio_row$ortalama, ratio_row$medyan, ratio_row$min, ratio_row$max,
    ratio_row$n_aralik_disi))
}

ep <- result$exposure_parametrizations
if (!is.null(ep)) {
  ok <- ep[!is.na(ep$status) & ep$status == "ok", , drop = FALSE]
  cat(sprintf("[§110] Parametrizasyon focal katsayi: %d/%d ok satir\n",
    nrow(ok), nrow(ep)))
  for (i in seq_len(nrow(ok))) {
    cat(sprintf("   %-30s [%-24s] b=%.3f 95%%GA[%.3f, %.3f] r=%.3f p=%.3f p_holm=%.3f dAIC=%.2f (n=%d)\n",
      ok$outcome[i], ok$parametrizasyon[i], ok$estimate[i], ok$ci_lower[i], ok$ci_upper[i],
      ok$r_partial[i], ok$p_value[i], ok$p_holm[i], ok$delta_aic[i], ok$n[i]))
  }
}

pc <- result$psychcontrol_sideanalysis
if (!is.null(pc) && "r" %in% names(pc)) {
  cat("[§110 yan] Psikolojik-kontrol proxy korelasyonlari (TOST |r|=.10):\n")
  for (i in seq_len(nrow(pc))) {
    cat(sprintf("   %-20s n=%s r=%s 95%%GA[%s, %s] tost_p=%s karar=%s\n",
      pc$exposure[i], format(pc$n[i]),
      formatC(pc$r[i], format = "f", digits = 3),
      formatC(pc$ci_lower[i], format = "f", digits = 3),
      formatC(pc$ci_upper[i], format = "f", digits = 3),
      formatC(pc$tost_p[i], format = "f", digits = 3),
      pc$tost_karar[i]))
  }
}

sw <- result$sibling_window_descriptive
if (!is.null(sw)) {
  bands <- unique(sw[, c("band", "n_band")])
  cat("[§111] Kardes gelisim penceresi bandlari (betimsel; test yok):\n")
  for (i in seq_len(nrow(bands))) {
    cat(sprintf("   %-24s n=%d\n", bands$band[i], bands$n_band[i]))
  }
}

invisible(result)
