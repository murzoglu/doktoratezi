# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLIV / §121 (DM-only, kisitli)
# KLINIK ZAMANLAMA (TANI GELISIM-PENCERESI)
#
#   §121 — Tani gelisim-penceresi × ebeveynlik/kardes. onset_band (erken<6 /
#     orta 6-10 / gec>10) tani_yasi'ndan. Duzeltilmis n=120'de bantlar ~34/59/27
#     → 3-bant birlestirmesiz. Cikti: embu_c_idx asiri koruma + kardes bakim
#     asimetrisi (indeks). DM-only, betimsel-oncelikli, genis CI.
#     ⚠️ "Tanidan sonra dogan kardes" duyarliligi: kardes_tani_ani_yas<0 (1 kayit)
#     HATA DEGIL — kardes indeksin tanisindan SONRA dogmus; ayri etiketli
#     kategori, betimsel/duyarlilik maskesi (cikarimsal banda sokulmaz).
#
# ⚠️ Imputation YAPILMAZ (Kural 19). Korelasyonel dil; nedensel yok.
# Tum ciktilar [KESIFSEL - POST-HOC].

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}

onmet_status_label <- function() "[KESIFSEL - POST-HOC]"
onmet_numeric <- function(x) suppressWarnings(as.numeric(x))

onmet_scale <- function(x) {
  x <- onmet_numeric(x); ok <- !is.na(x); out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) return(out)
  s <- stats::sd(x[ok]); if (is.na(s) || s == 0) return(out)
  out[ok] <- (x[ok] - mean(x[ok])) / s; out
}

onmet_require_columns <- function(df, columns, context) {
  missing <- setdiff(columns, names(df))
  if (length(missing) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

onmet_dm_frame <- function(df_family_ses) {
  onmet_require_columns(df_family_ses, c("group_f", "cocuk_yas", "kardes_yas", "dm_yili"),
    "§121 DM frame")
  df <- df_family_ses[as.character(df_family_ses$group_f) == "DM", , drop = FALSE]
  df$cocuk_yas_num <- onmet_numeric(df$cocuk_yas)
  df$dm_yili_num <- onmet_numeric(df$dm_yili)
  df$kardes_yas_num <- onmet_numeric(df$kardes_yas)
  df$tani_yasi <- if ("tani_yasi" %in% names(df)) onmet_numeric(df$tani_yasi) else
    df$cocuk_yas_num - df$dm_yili_num
  df$kardes_tani_ani_yas <- df$kardes_yas_num - df$dm_yili_num
  df$onset_band <- cut(df$tani_yasi, breaks = c(-Inf, 6, 10, Inf), right = FALSE,
    labels = c("erken(<6)", "orta(6-10)", "gec(>=10)"))
  # indeks bakim-asimetrisi (of - by)
  if (all(c("srq_fo_nurturance_of_sib_mean", "srq_fo_nurturance_by_sib_mean") %in% names(df))) {
    df$nurturance_asym_idx <- onmet_numeric(df$srq_fo_nurturance_of_sib_mean) -
      onmet_numeric(df$srq_fo_nurturance_by_sib_mean)
  } else df$nurturance_asym_idx <- rep(NA_real_, nrow(df))
  df$cocuk_yas_z <- onmet_scale(df$cocuk_yas_num)
  df$ses_latent_z <- if ("ses_latent" %in% names(df)) onmet_scale(df$ses_latent) else rep(NA_real_, nrow(df))
  df
}

# =========================================================================
# §121 — Onset penceresi × ebeveynlik/kardes (DM-only)
# =========================================================================

onmet_run_121 <- function(df, outcomes = c("embu_c_idx_asiri_koruma_mean", "nurturance_asym_idx")) {
  # "Tanidan sonra dogan kardes" (kardes_tani_ani_yas<0) ayir
  post_dx <- which(!is.na(df$kardes_tani_ani_yas) & df$kardes_tani_ani_yas < 0)
  sensitivity <- data.frame(
    kategori = "kardes_tani_ani_yas<0 (tani sonrasi dogan kardes)",
    n = length(post_dx),
    not = paste0("HATA DEGIL; kardes indeksin tanisindan sonra dogmus (aileye hastalik ",
      "yerlesmisken). Betimsel/duyarlilik; cikarimsal banda sokulmaz."),
    statu = onmet_status_label(), stringsAsFactors = FALSE)
  main <- df[-post_dx, , drop = FALSE]
  if (length(post_dx) == 0L) main <- df

  band_desc <- list(); omnibus_rows <- list()
  for (oc in outcomes) {
    if (!oc %in% names(main)) next
    for (b in levels(main$onset_band)) {
      idx <- which(main$onset_band == b)
      v <- onmet_numeric(main[[oc]][idx]); v <- v[!is.na(v)]
      band_desc[[paste(oc, b, sep = "__")]] <- data.frame(
        outcome = oc, onset_band = b, n = length(v),
        ortalama = if (length(v)) mean(v) else NA_real_,
        medyan = if (length(v)) stats::median(v) else NA_real_,
        sd = if (length(v) > 1L) stats::sd(v) else NA_real_,
        statu = onmet_status_label(), stringsAsFactors = FALSE)
    }
    cols <- c(oc, "onset_band", "cocuk_yas_z")
    sub <- main[stats::complete.cases(main[, cols, drop = FALSE]), , drop = FALSE]
    if (nrow(sub) >= 30L && nlevels(droplevels(sub$onset_band)) >= 2L) {
      fit <- tryCatch(stats::lm(stats::as.formula(paste0(oc, " ~ onset_band + cocuk_yas_z")),
        data = sub), error = function(e) NULL)
      if (!is.null(fit)) {
        an <- tryCatch(stats::anova(fit), error = function(e) NULL)
        omnibus_rows[[oc]] <- data.frame(
          outcome = oc, n = nrow(sub),
          onset_F = if (!is.null(an)) an$`F value`[1L] else NA_real_,
          onset_df1 = if (!is.null(an)) an$Df[1L] else NA_real_,
          onset_df2 = if (!is.null(an)) an$Df[nrow(an)] else NA_real_,
          onset_p = if (!is.null(an)) an$`Pr(>F)`[1L] else NA_real_,
          eta_sq = if (!is.null(an)) an$`Sum Sq`[1L] / sum(an$`Sum Sq`) else NA_real_,
          not = "DM-only; Tier C betimsel-oncelikli (genis CI)",
          statu = onmet_status_label(), stringsAsFactors = FALSE)
      }
    }
  }
  list(
    onset_band_descriptive = if (length(band_desc)) do.call(rbind, band_desc) else NULL,
    onset_omnibus = if (length(omnibus_rows)) do.call(rbind, omnibus_rows) else NULL,
    post_diagnosis_sibling_sensitivity = sensitivity
  )
}

# =========================================================================
# Pipeline sarici
# =========================================================================

run_phase4_onset_metabolic_pipeline <- function(df_family_ses) {
  df <- onmet_dm_frame(df_family_ses)
  res121 <- onmet_run_121(df)

  onset_tab <- table(df$onset_band, useNA = "ifany")
  target_summary <- data.frame(
    analysis = "phase4_onset_metabolic_context",
    kisim = "KISIM XLIV (§121)",
    n_dm = nrow(df),
    onset_erken = as.integer(onset_tab[["erken(<6)"]] %||% 0L),
    onset_orta = as.integer(onset_tab[["orta(6-10)"]] %||% 0L),
    onset_gec = as.integer(onset_tab[["gec(>=10)"]] %||% 0L),
    imputation = "YOK (Kural 19)",
    kanit_kategorisi = onmet_status_label(),
    sapma_tipi = "Tip 3 (Faz IV post-hoc, SAP KISIM XLIV/121)",
    reference_doc = "07-sap-faz4-ek-plan.md",
    stringsAsFactors = FALSE
  )

  list(
    onset_band_descriptive_121 = res121$onset_band_descriptive,
    onset_omnibus_121 = res121$onset_omnibus,
    post_diagnosis_sibling_sensitivity_121 = res121$post_diagnosis_sibling_sensitivity,
    target_summary = target_summary
  )
}
