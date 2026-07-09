# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLIV / §121-122 (DM-only, kisitli)
# KLINIK ZAMANLAMA VE METABOLIK BAGLAM
#
#   §121 — Tani gelisim-penceresi × ebeveynlik/kardes. onset_band (erken<6 /
#     orta 6-10 / gec>10) tani_yasi'ndan. Duzeltilmis n=120'de bantlar ~34/59/27
#     → 3-bant birlestirmesiz. Cikti: embu_c_idx asiri koruma + kardes bakim
#     asimetrisi (indeks). DM-only, betimsel-oncelikli, genis CI.
#     ⚠️ "Tanidan sonra dogan kardes" duyarliligi: kardes_tani_ani_yas<0 (1 kayit)
#     HATA DEGIL — kardes indeksin tanisindan SONRA dogmus; ayri etiketli
#     kategori, betimsel/duyarlilik maskesi (cikarimsal banda sokulmaz).
#   §122 — Metabolik kontrolun sosyodemografik + psikososyal-olcek gradyani.
#     (i) hba1c ~ ses + komorbidite-ikili (+ tek_ebeveyn varsa); (ii) hba1c ↔
#     EMBU-C asiri koruma / EMBU-P / BDI / SRQ catisma betimsel korelasyon.
#     ⚠️ CSR §12.5.1: tam-veri n≈39 → DUSUK GUC; betimsel, genis CI, imputasyon
#     YOK. ⚠️⚠️ §134 SECILIM YUZEYI (HbA1c MNAR) raporlanmadan yorumlanamaz.
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

onmet_cor_ci <- function(r, n, conf = 0.95) {
  if (is.na(r) || is.na(n) || n < 4L) return(c(NA_real_, NA_real_))
  z <- atanh(r); se <- 1 / sqrt(n - 3); crit <- stats::qnorm(1 - (1 - conf) / 2)
  c(tanh(z - crit * se), tanh(z + crit * se))
}

onmet_dm_frame <- function(df_family_ses) {
  onmet_require_columns(df_family_ses, c("group_f", "cocuk_yas", "kardes_yas", "dm_yili"),
    "§121-122 DM frame")
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
# §122 — Metabolik kontrol gradyani (DM-only, betimsel, n≈39)
# =========================================================================

onmet_run_122 <- function(df) {
  if (!"hba1c" %in% names(df)) {
    return(list(hba1c_descriptive = NULL, hba1c_sociodemographic = NULL,
      hba1c_psychosocial_cor = NULL))
  }
  df$hba1c_num <- onmet_numeric(df$hba1c)
  hv <- df$hba1c_num[!is.na(df$hba1c_num)]
  hba1c_desc <- data.frame(
    degisken = "hba1c (DM-only)", n_dm = nrow(df), n_gecerli = length(hv),
    n_eksik = sum(is.na(df$hba1c_num)),
    ortalama = if (length(hv)) mean(hv) else NA_real_,
    medyan = if (length(hv)) stats::median(hv) else NA_real_,
    sd = if (length(hv) > 1L) stats::sd(hv) else NA_real_,
    min = if (length(hv)) min(hv) else NA_real_, max = if (length(hv)) max(hv) else NA_real_,
    uyari = paste0("STRUCTURAL + item eksik; tam-veri n≈39 (DUSUK GUC). §134 SECILIM ",
      "YUZEYI (MNAR) raporlanmadan yorumlanamaz. Betimsel; imputasyon YOK."),
    statu = onmet_status_label(), stringsAsFactors = FALSE)

  # (i) sosyodemografik (betimsel regresyon, dusuk guc)
  df$komorbidite_ikili <- if ("anne_hastalik_kategori_sayisi" %in% names(df)) {
    as.integer(onmet_numeric(df$anne_hastalik_kategori_sayisi) > 0)
  } else rep(NA_integer_, nrow(df))
  socio <- NULL
  cols <- c("hba1c_num", "ses_latent_z", "komorbidite_ikili")
  sub <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
  if (nrow(sub) >= 20L) {
    fit <- tryCatch(stats::lm(hba1c_num ~ ses_latent_z + komorbidite_ikili, data = sub),
      error = function(e) NULL)
    if (!is.null(fit)) {
      sm <- as.data.frame(summary(fit)$coefficients); sm$term <- rownames(sm); rownames(sm) <- NULL
      ci <- tryCatch(as.data.frame(stats::confint(fit)), error = function(e) NULL)
      socio <- data.frame(
        term = sm$term, estimate = sm[["Estimate"]], se = sm[["Std. Error"]],
        t_value = sm[["t value"]], p_value = sm[["Pr(>|t|)"]],
        ci_lower = if (!is.null(ci)) ci[sm$term, 1L] else NA_real_,
        ci_upper = if (!is.null(ci)) ci[sm$term, 2L] else NA_real_,
        n = stats::nobs(fit),
        not = "betimsel/dusuk-guc (n≈39); cikarimsal iddia YOK",
        statu = onmet_status_label(), row.names = NULL, stringsAsFactors = FALSE)
    }
  }

  # (ii) psikososyal-olcek korelasyonlari (betimsel)
  psy_targets <- c(
    embu_c_idx_asiri_koruma_mean = "embu_c_idx_asiri_koruma_mean",
    embu_p_asiri_koruma_mean = "embu_p_asiri_koruma_mean",
    embu_p_reddetme_mean = "embu_p_reddetme_mean",
    beck_total = "beck_total",
    srq_ho_conflict_mean = "srq_ho_conflict_mean")
  cor_rows <- list()
  for (nm in names(psy_targets)) {
    col <- psy_targets[[nm]]
    if (!col %in% names(df)) next
    x <- df$hba1c_num; y <- onmet_numeric(df[[col]])
    ok <- !is.na(x) & !is.na(y); n <- sum(ok)
    r <- if (n >= 4L) suppressWarnings(stats::cor(x[ok], y[ok])) else NA_real_
    ci <- onmet_cor_ci(r, n)
    p <- if (n >= 4L) tryCatch(stats::cor.test(x[ok], y[ok])$p.value, error = function(e) NA_real_) else NA_real_
    cor_rows[[nm]] <- data.frame(
      hedef = nm, n = n, r = r, ci_lower = ci[1L], ci_upper = ci[2L], p_value = p,
      not = "betimsel korelasyon (DM-only, n≈39); nedensel dil YOK; §134 secilim uyarisi",
      statu = onmet_status_label(), stringsAsFactors = FALSE)
  }
  list(
    hba1c_descriptive = hba1c_desc,
    hba1c_sociodemographic = socio,
    hba1c_psychosocial_cor = if (length(cor_rows)) do.call(rbind, cor_rows) else NULL
  )
}

# =========================================================================
# Pipeline sarici
# =========================================================================

run_phase4_onset_metabolic_pipeline <- function(df_family_ses) {
  df <- onmet_dm_frame(df_family_ses)
  res121 <- onmet_run_121(df)
  res122 <- onmet_run_122(df)

  onset_tab <- table(df$onset_band, useNA = "ifany")
  target_summary <- data.frame(
    analysis = "phase4_onset_metabolic_context",
    kisim = "KISIM XLIV (§121-122)",
    n_dm = nrow(df),
    onset_erken = as.integer(onset_tab[["erken(<6)"]] %||% 0L),
    onset_orta = as.integer(onset_tab[["orta(6-10)"]] %||% 0L),
    onset_gec = as.integer(onset_tab[["gec(>=10)"]] %||% 0L),
    n_hba1c = sum(!is.na(onmet_numeric(df$hba1c))),
    hba1c_uyari = "n≈39 DUSUK GUC + §134 MNAR SECILIM → betimsel",
    imputation = "YOK (Kural 19)",
    kanit_kategorisi = onmet_status_label(),
    sapma_tipi = "Tip 3 (Faz IV post-hoc, SAP KISIM XLIV/121-122)",
    reference_doc = "07-sap-faz4-ek-plan.md",
    stringsAsFactors = FALSE
  )

  list(
    onset_band_descriptive_121 = res121$onset_band_descriptive,
    onset_omnibus_121 = res121$onset_omnibus,
    post_diagnosis_sibling_sensitivity_121 = res121$post_diagnosis_sibling_sensitivity,
    hba1c_descriptive_122 = res122$hba1c_descriptive,
    hba1c_sociodemographic_122 = res122$hba1c_sociodemographic,
    hba1c_psychosocial_cor_122 = res122$hba1c_psychosocial_cor,
    target_summary = target_summary
  )
}
