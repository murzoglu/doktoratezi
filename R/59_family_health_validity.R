# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLV / §123-124
# AILE SAGLIK PROFILI VE VERI-GECERLIK
#
#   §123 — 14-kategori komorbidite betimsel prevalans paneli (anne + es × grup).
#     R/53 yalniz otoimmun+endokrin+kategori_sayisi kullandi; 12+ sistem-ozgu
#     kategori hic sunulmadi. YALNIZ betimsel prevalans; hicbir kategori tek
#     basina cikarimsal test EDILMEZ (cogu seyrek). Grup farki yalniz
#     kategori_sayisi ikili duzeyinde (Faz III §104 ile ic-tutarli) not edilir.
#   §124 — Komorbidite KODLAMA-SADAKATI denetimi (ANALIZ DEGIL, veri-audit).
#     ⚠️ Bagimsiz gecerlik calismasi DEGILDIR. kronik_hastalik_durumu (oz-bildirim
#     ikili) ile kategori_sayisi>0 (kodlanmis) arasinda κ — kodlanmis 14-kategori
#     matris ZATEN oz-bildirimden turetildigi icin bagimsiz olcum degildir.
#     Kriegsman-tipi "oz-bildirim↔tibbi kayit" capasi UYGULANAMAZ (bagimsiz kayit
#     yok). Yalniz KODLAMA-SADAKATINI teyit eder (κ=1 → kodlama hatasiz).
#
# ⚠️ Betimsel; cikarimsal iddia yok. Tum ciktilar [KESIFSEL - POST-HOC].

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}

fhv_status_label <- function() "[KESIFSEL - POST-HOC]"
fhv_numeric <- function(x) suppressWarnings(as.numeric(x))

fhv_require_columns <- function(df, columns, context) {
  missing <- setdiff(columns, names(df))
  if (length(missing) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

fhv_comorbidity_systems <- function() {
  c("kardiyovaskuler", "solunum", "gastrointestinal", "renal", "kas_iskelet",
    "mental", "sinir", "duyu", "hematolojik", "dermatolojik", "neoplazm",
    "diger", "otoimmun", "endokrin")
}

fhv_binary <- function(x) {
  if (is.factor(x)) {
    lv <- tolower(as.character(x))
    return(as.integer(lv %in% c("1", "evet", "var", "yes", "true")))
  }
  xn <- fhv_numeric(x); as.integer(!is.na(xn) & xn > 0)
}

# =========================================================================
# §123 — 14-kategori betimsel prevalans (anne + es × grup)
# =========================================================================

fhv_prevalence_panel <- function(df) {
  systems <- fhv_comorbidity_systems()
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  rows <- list()
  for (who in c("anne", "es")) {
    for (sys in systems) {
      col <- paste0(who, "_hastalik_", sys)
      if (!col %in% names(df)) next
      b <- fhv_binary(df[[col]])
      for (g in c("Kontrol", "DM", "Tumu")) {
        idx <- if (g == "Tumu") seq_len(nrow(df)) else which(df$group_f == g)
        bg <- b[idx]; nvalid <- sum(!is.na(bg))
        rows[[paste(who, sys, g, sep = "__")]] <- data.frame(
          bilgi_kaynagi = who, kategori = sys, group = g,
          n = nvalid, n_var = sum(bg == 1L, na.rm = TRUE),
          prevalans = if (nvalid > 0L) sum(bg == 1L, na.rm = TRUE) / nvalid else NA_real_,
          statu = fhv_status_label(), stringsAsFactors = FALSE)
      }
    }
  }
  do.call(rbind, rows)
}

# Grup farki yalniz kategori_sayisi ikili duzeyinde (Faz III §104 ic-tutarli)
fhv_category_count_group <- function(df) {
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  rows <- list()
  for (who in c("anne", "es")) {
    col <- paste0(who, "_hastalik_kategori_sayisi")
    if (!col %in% names(df)) next
    ikili <- as.integer(fhv_numeric(df[[col]]) > 0)
    tab <- table(factor(ikili, levels = c(0, 1)), df$group_f)
    ft <- tryCatch(stats::fisher.test(tab), error = function(e) NULL)
    rows[[who]] <- data.frame(
      bilgi_kaynagi = who,
      n_kontrol_var = tab[2, "Kontrol"], n_dm_var = tab[2, "DM"],
      prevalans_kontrol = tab[2, "Kontrol"] / sum(tab[, "Kontrol"]),
      prevalans_dm = tab[2, "DM"] / sum(tab[, "DM"]),
      odds_ratio = if (!is.null(ft)) unname(ft$estimate) else NA_real_,
      or_ci_lower = if (!is.null(ft)) ft$conf.int[1L] else NA_real_,
      or_ci_upper = if (!is.null(ft)) ft$conf.int[2L] else NA_real_,
      p_value = if (!is.null(ft)) ft$p.value else NA_real_,
      not = "Yalniz ikili kategori_sayisi>0 duzeyinde (Faz III §104 ic-tutarli); sistem-ozgu betimsel",
      statu = fhv_status_label(), stringsAsFactors = FALSE)
  }
  do.call(rbind, rows)
}

# =========================================================================
# §124 — Kodlama-sadakati denetimi (veri-audit; bagimsiz gecerlik DEGIL)
# =========================================================================

fhv_kappa_2x2 <- function(a, b) {
  ok <- !is.na(a) & !is.na(b)
  a <- a[ok]; b <- b[ok]; n <- length(a)
  if (n < 4L) return(list(kappa = NA_real_, po = NA_real_, n = n, tab = NULL))
  tab <- table(factor(a, levels = c(0, 1)), factor(b, levels = c(0, 1)))
  po <- sum(diag(tab)) / n
  pe <- sum(rowSums(tab) * colSums(tab)) / n^2
  kappa <- if ((1 - pe) == 0) NA_real_ else (po - pe) / (1 - pe)
  list(kappa = kappa, po = po, n = n, tab = tab)
}

fhv_coding_fidelity <- function(df) {
  rows <- list()
  pairs <- list(
    anne = c("kronik_hastalik_durumu", "anne_hastalik_kategori_sayisi"),
    es = c("esiniz_kronik_hastalik_durumu", "es_hastalik_kategori_sayisi"))
  for (who in names(pairs)) {
    sr_col <- pairs[[who]][1L]; coded_col <- pairs[[who]][2L]
    if (!all(c(sr_col, coded_col) %in% names(df))) next
    sr <- fhv_binary(df[[sr_col]])
    coded <- as.integer(fhv_numeric(df[[coded_col]]) > 0)
    kap <- fhv_kappa_2x2(sr, coded)
    # marjinal sayimlar KAPPA ile AYNI tam-vaka altkumesinde (ic-tutarlilik)
    ok <- !is.na(sr) & !is.na(coded)
    rows[[who]] <- data.frame(
      bilgi_kaynagi = who, n = kap$n,
      n_oz_bildirim_var = sum(sr[ok] == 1L),
      n_kodlanmis_var = sum(coded[ok] == 1L),
      gozlenen_uyum = kap$po, kappa = kap$kappa,
      yorum = paste0("KODLAMA-SADAKATI (bagimsiz gecerlik DEGIL): kodlanmis matris ",
        "oz-bildirimden turetilmis → κ=1 kodlama hatasizligini teyit eder, ",
        "olcum gecerligini DEGIL. Kriegsman capasi uygulanamaz (bagimsiz kayit yok)."),
      statu = fhv_status_label(), stringsAsFactors = FALSE)
  }
  do.call(rbind, rows)
}

# =========================================================================
# Pipeline sarici
# =========================================================================

run_phase4_family_health_pipeline <- function(df_family_ses) {
  fhv_require_columns(df_family_ses, "group_f", "§123-124")
  df <- df_family_ses[!duplicated(df_family_ses$aile_no), , drop = FALSE]

  prevalence <- fhv_prevalence_panel(df)
  category_group <- fhv_category_count_group(df)
  coding_fidelity <- fhv_coding_fidelity(df)

  target_summary <- data.frame(
    analysis = "phase4_family_health_validity",
    kisim = "KISIM XLV (§123-124)",
    n_family = nrow(df),
    n_sistem = length(fhv_comorbidity_systems()),
    kodlama_sadakati_min_kappa = if (!is.null(coding_fidelity)) min(coding_fidelity$kappa, na.rm = TRUE) else NA_real_,
    statu_123 = "betimsel (sistem-ozgu prevalans; cikarimsal test YOK)",
    statu_124 = "veri-audit (kodlama-sadakati; bagimsiz gecerlik DEGIL)",
    imputation = "YOK (Kural 19)",
    kanit_kategorisi = fhv_status_label(),
    sapma_tipi = "Tip 3 (Faz IV post-hoc, SAP KISIM XLV/123-124)",
    reference_doc = "07-sap-faz4-ek-plan.md",
    stringsAsFactors = FALSE
  )

  list(
    comorbidity_prevalence_123 = prevalence,
    category_count_group_123 = category_group,
    coding_fidelity_124 = coding_fidelity,
    target_summary = target_summary
  )
}
