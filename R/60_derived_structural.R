# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLVI / §125
# TURETILEBILIR YAPISAL DEGISKENLER — Ebeveyn yas farki (assortatif eslesme)
#
# es_dogum_tarihi kanonik final CSV'de %100 bostu (turetme kaybi, B5); ham
# kaynakta 480/482 doluydu → kurtarildi: SUPPLEMENT__es_yas_recovered.csv
# (aile_no, es_yas, ebeveyn_yas_farki, es_yas_valid; es_yas 240/241).
#
#   §125 — ebeveyn_yas_farki (= anne_yas - es_yas) kovaryat/moderator → EMBU-P +
#     Beck. ⚠️ Plausibilite-maskesi (B7): es_yas 13 = imkansiz baba yasi →
#     es_yas<16 | >70 DISLA (es_yas_valid). Asiri deger 3-adim protokolu.
#     Moderator zayif beklenir (Tier B kovaryat).
#
# ⚠️ Imputation YAPILMAZ (Kural 19). Korelasyonel dil; nedensel yok.
# Tum ciktilar [KESIFSEL - POST-HOC].

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}

dstr_status_label <- function() "[KESIFSEL - POST-HOC]"
dstr_numeric <- function(x) suppressWarnings(as.numeric(x))

dstr_scale <- function(x) {
  x <- dstr_numeric(x); ok <- !is.na(x); out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) return(out)
  s <- stats::sd(x[ok]); if (is.na(s) || s == 0) return(out)
  out[ok] <- (x[ok] - mean(x[ok])) / s; out
}

dstr_require_columns <- function(df, columns, context) {
  missing <- setdiff(columns, names(df))
  if (length(missing) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

# B7 plausibilite-maskesi + aile bazina birlestirme
dstr_prepare_frame <- function(df_family_ses, supplement,
    es_yas_min = 16, es_yas_max = 70) {
  dstr_require_columns(df_family_ses, c("aile_no", "group_f", "anne_yas"), "§125 family")
  dstr_require_columns(supplement, c("aile_no", "es_yas"), "§125 supplement")
  df <- df_family_ses[!duplicated(df_family_ses$aile_no), , drop = FALSE]
  m <- match(df$aile_no, supplement$aile_no)
  es_yas_raw <- dstr_numeric(supplement$es_yas[m])
  # B7 maskesi
  es_yas <- ifelse(!is.na(es_yas_raw) & (es_yas_raw < es_yas_min | es_yas_raw > es_yas_max),
    NA_real_, es_yas_raw)
  df$es_yas <- es_yas
  df$anne_yas_num <- dstr_numeric(df$anne_yas)
  df$ebeveyn_yas_farki <- df$anne_yas_num - df$es_yas    # + = anne buyuk
  df$ebeveyn_yas_farki_z <- dstr_scale(df$ebeveyn_yas_farki)
  df$anne_yas_z <- dstr_scale(df$anne_yas_num)
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  attr(df, "n_masked") <- sum(!is.na(es_yas_raw) &
    (es_yas_raw < es_yas_min | es_yas_raw > es_yas_max))
  df
}

dstr_describe <- function(df) {
  x <- df$ebeveyn_yas_farki
  obs <- x[!is.na(x)]
  q <- if (length(obs)) stats::quantile(obs, probs = c(.25, .5, .75)) else c(NA, NA, NA)
  iqr <- if (length(obs)) stats::IQR(obs) else NA_real_
  # 3-adim asiri-deger: |z|>3.29 (p<.001) isaretle (SILME, sadece rapor)
  z <- if (length(obs) > 1L) (obs - mean(obs)) / stats::sd(obs) else rep(NA_real_, length(obs))
  data.frame(
    degisken = "ebeveyn_yas_farki (anne_yas - es_yas)",
    n_family = nrow(df), n_gecerli = length(obs),
    n_maskeli_B7 = attr(df, "n_masked") %||% NA_integer_,
    ortalama = if (length(obs)) mean(obs) else NA_real_,
    medyan = q[2L], q1 = q[1L], q3 = q[3L], iqr = iqr,
    min = if (length(obs)) min(obs) else NA_real_,
    max = if (length(obs)) max(obs) else NA_real_,
    n_asiri_z329 = sum(abs(z) > 3.29, na.rm = TRUE),
    yorum = paste0("+ = anne buyuk; - = baba buyuk. B7 maskesi es_yas<16|>70 → NA. ",
      "Asiri-deger 3-adim: |z|>3.29 isaretli (silinmedi)."),
    statu = dstr_status_label(), stringsAsFactors = FALSE)
}

dstr_lm_focal <- function(fit, focal, label, outcome) {
  sm <- summary(fit)$coefficients
  ci <- tryCatch(stats::confint(fit), error = function(e) NULL)
  if (!focal %in% rownames(sm)) return(NULL)
  data.frame(
    label = label, outcome = outcome, term = focal,
    estimate = sm[focal, "Estimate"], se = sm[focal, "Std. Error"],
    t_value = sm[focal, "t value"], p_value = sm[focal, "Pr(>|t|)"],
    ci_lower = if (!is.null(ci)) ci[focal, 1L] else NA_real_,
    ci_upper = if (!is.null(ci)) ci[focal, 2L] else NA_real_,
    n = stats::nobs(fit), statu = dstr_status_label(),
    row.names = NULL, stringsAsFactors = FALSE)
}

dstr_run_models <- function(df,
    embu_outcomes = c("reddetme", "asiri_koruma", "sicaklik", "karsilastirma")) {
  rows <- list()
  # EMBU-P (anne raporu)
  for (s in embu_outcomes) {
    yv <- paste0("embu_p_", s, "_mean")
    if (!yv %in% names(df)) next
    cols <- c(yv, "ebeveyn_yas_farki_z", "group_f", "anne_yas_z")
    sub <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
    if (nrow(sub) < 40L) next
    fit <- tryCatch(stats::lm(
      stats::as.formula(paste0(yv, " ~ ebeveyn_yas_farki_z + group_f + anne_yas_z")),
      data = sub), error = function(e) NULL)
    if (!is.null(fit)) rows[[paste0("P_", s)]] <- dstr_lm_focal(fit, "ebeveyn_yas_farki_z",
      "yas_farki→EMBU-P", yv)
  }
  # Beck
  if ("beck_total" %in% names(df)) {
    cols <- c("beck_total", "ebeveyn_yas_farki_z", "group_f")
    sub <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
    if (nrow(sub) >= 40L) {
      fit <- tryCatch(stats::lm(beck_total ~ ebeveyn_yas_farki_z + group_f, data = sub),
        error = function(e) NULL)
      if (!is.null(fit)) rows[["beck"]] <- dstr_lm_focal(fit, "ebeveyn_yas_farki_z",
        "yas_farki→Beck", "beck_total")
    }
  }
  out <- if (length(rows)) do.call(rbind, rows) else NULL
  if (!is.null(out)) out$p_holm <- stats::p.adjust(out$p_value, method = "holm")
  out
}

run_phase4_derived_structural_pipeline <- function(df_family_ses, supplement) {
  df <- dstr_prepare_frame(df_family_ses, supplement)
  describe <- dstr_describe(df)
  models <- dstr_run_models(df)

  target_summary <- data.frame(
    analysis = "phase4_derived_structural",
    kisim = "KISIM XLVI (§125)",
    n_family = nrow(df),
    n_yas_farki_gecerli = sum(!is.na(df$ebeveyn_yas_farki)),
    n_maskeli_B7 = attr(df, "n_masked") %||% NA_integer_,
    medyan_yas_farki = stats::median(df$ebeveyn_yas_farki, na.rm = TRUE),
    kaynak = "SUPPLEMENT__es_yas_recovered.csv (es_dogum turetme-kaybi kurtarma, B5)",
    imputation = "YOK (Kural 19)",
    coklu_karsilastirma = "Holm (§125 EMBU-P + Beck ailesi)",
    kanit_kategorisi = dstr_status_label(),
    sapma_tipi = "Tip 3 (Faz IV post-hoc, SAP KISIM XLVI/125)",
    reference_doc = "07-sap-faz4-ek-plan.md",
    stringsAsFactors = FALSE
  )

  list(
    age_gap_descriptive = describe,
    age_gap_models = models,
    target_summary = target_summary
  )
}
