# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLIX / §134-135
# SECILIM VE BATCH GECERLIK DENETIMLERI
#
# Bu modul YENI bir iliski kesfetmez; MEVCUT/planli analizlerin gecerligini
# denetler. Iki somut, kanonik CSV uzerinde birebir dogrulanmis tehdide yanittir:
#
#   §134 — HbA1c erisilebilirlik/eksiklik SECILIM denetimi (MNAR):
#     DM'de HbA1c yalniz 39/120 ailede var ve varligi anne_antidepresan ile
#     guclu iliskili (Fisher OR ~ 4.5). HbA1c ham dosyada yok; sonradan klinik-
#     kayit entegrasyonuyla eklendi → varlik klinik-izlem/temas gostergesi.
#     hba1c_available ~ AD + beck_total + ses + dm_yili + cocuk_yas (DM-only
#     lojistik). SONUC KURALI: hicbir HbA1c x ebeveynlik bulgusu (§122, CSR §12.5)
#     bu secilim yuzeyi raporlanmadan yorumlanamaz.
#     ⚠️ IPW/Heckman yalniz FIZIBILITE-DUYARLILIGI (DUZELTME DEGIL): amac secilimi
#     GOSTERMEK. n=39'da IPW gurultuyu buyutur → ESS + maks-agirlik + budama
#     (truncation) esigi/sayisi ZORUNLU raporlanir.
#
#   §135 — Alim-yili / batch duyarliligi:
#     Anket yili grupla neredeyse kollinear (group ~ yil logistic p cok kucuk).
#     DM agirlikla 2023'te, Kontrol 2024-25'te alinmis → recruitment/batch
#     temporal confound. Yil KOR KOVARYAT OLARAK EKLENMEZ (grup etkisini emer).
#     Bunun yerine: (i) 2023-only alt-orneklem replikasyonu (her iki grup
#     mevcut); (ii) yil-tabakali betimsel; (iii) kollinearite tanisi (yalniz).
#     SONUC KURALI: 2023-only'de ana etkiler yonce korunuyorsa guclenir;
#     kayboluyorsa "grup farki kismen batch/donem etkisiyle karisik" yazilir.
#
# ⚠️ Imputation YAPILMAZ (Kural 19). NA'lar acik. Korelasyonel dil; nedensel yok.
# ⚠️ Tum ciktilar [KESIFSEL - POST-HOC]; H1-H5'i YORUMLAR, DEGISTIRMEZ.

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}

selb_status_label <- function() "[KESIFSEL - POST-HOC]"

selb_numeric <- function(x) suppressWarnings(as.numeric(x))

selb_scale <- function(x) {
  x <- selb_numeric(x)
  ok <- !is.na(x)
  out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) return(out)
  s <- stats::sd(x[ok])
  if (is.na(s) || s == 0) return(out)
  out[ok] <- (x[ok] - mean(x[ok])) / s
  out
}

selb_require_columns <- function(df, columns, context) {
  missing <- setdiff(columns, names(df))
  if (length(missing) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

# anne_antidepresan kanonik bazda 0/1; guvenli 0/1 vektore cevir
selb_ad_binary <- function(x) {
  if (is.factor(x)) {
    lv <- tolower(as.character(x))
    return(as.integer(lv %in% c("1", "evet", "var", "yes", "true")))
  }
  xn <- selb_numeric(x)
  as.integer(!is.na(xn) & xn > 0)
}

# dd.mm.yyyy / yyyy-mm-dd / serbest metinden 4-haneli yil cikar
selb_extract_year <- function(x) {
  xc <- as.character(x)
  yr <- rep(NA_integer_, length(xc))
  # once dd.mm.yyyy sonu
  m1 <- regmatches(xc, regexpr("(19|20)[0-9]{2}$", xc))
  hit1 <- grepl("(19|20)[0-9]{2}$", xc)
  yr[hit1] <- as.integer(m1)
  # kalanlar icin metindeki ilk 4-haneli yil
  rest <- which(is.na(yr) & !is.na(xc) & nzchar(xc))
  if (length(rest) > 0L) {
    m2 <- regmatches(xc[rest], regexpr("(19|20)[0-9]{2}", xc[rest]))
    got <- grepl("(19|20)[0-9]{2}", xc[rest])
    yr[rest[got]] <- as.integer(m2)
  }
  yr
}

# Cohen's d (grup: iki-duzey faktor) + %95 GA. effectsize varsa onu kullan.
selb_group_d <- function(y, g, ref = "Kontrol", foc = "DM", conf = 0.95) {
  y <- selb_numeric(y)
  g <- as.character(g)
  keep <- !is.na(y) & g %in% c(ref, foc)
  y <- y[keep]; g <- g[keep]
  n_ref <- sum(g == ref); n_foc <- sum(g == foc)
  out0 <- data.frame(
    n_ref = n_ref, n_foc = n_foc, mean_ref = NA_real_, mean_foc = NA_real_,
    median_ref = NA_real_, median_foc = NA_real_,
    d = NA_real_, d_ci_lower = NA_real_, d_ci_upper = NA_real_,
    welch_t = NA_real_, welch_df = NA_real_, p_value = NA_real_,
    stringsAsFactors = FALSE
  )
  if (n_ref < 3L || n_foc < 3L) return(out0)
  m_ref <- mean(y[g == ref]); m_foc <- mean(y[g == foc])
  md_ref <- stats::median(y[g == ref]); md_foc <- stats::median(y[g == foc])
  tt <- tryCatch(stats::t.test(y[g == foc], y[g == ref]), error = function(e) NULL)
  d_est <- NA_real_; d_lo <- NA_real_; d_hi <- NA_real_
  if (requireNamespace("effectsize", quietly = TRUE)) {
    dd <- tryCatch(
      as.data.frame(effectsize::cohens_d(y[g == foc], y[g == ref], ci = conf)),
      error = function(e) NULL
    )
    if (!is.null(dd) && "Cohens_d" %in% names(dd)) {
      d_est <- dd$Cohens_d[1L]
      if (all(c("CI_low", "CI_high") %in% names(dd))) {
        d_lo <- dd$CI_low[1L]; d_hi <- dd$CI_high[1L]
      }
    }
  }
  if (is.na(d_est)) {
    sp <- sqrt(((n_foc - 1) * stats::var(y[g == foc]) +
      (n_ref - 1) * stats::var(y[g == ref])) / (n_foc + n_ref - 2))
    d_est <- if (sp > 0) (m_foc - m_ref) / sp else NA_real_
  }
  data.frame(
    n_ref = n_ref, n_foc = n_foc, mean_ref = m_ref, mean_foc = m_foc,
    median_ref = md_ref, median_foc = md_foc,
    d = d_est, d_ci_lower = d_lo, d_ci_upper = d_hi,
    welch_t = if (!is.null(tt)) unname(tt$statistic) else NA_real_,
    welch_df = if (!is.null(tt)) unname(tt$parameter) else NA_real_,
    p_value = if (!is.null(tt)) unname(tt$p.value) else NA_real_,
    stringsAsFactors = FALSE
  )
}

# =========================================================================
# §134 — HbA1c erisilebilirlik SECILIM denetimi (MNAR), DM-only
# =========================================================================

selb_dm_frame <- function(df_family_ses) {
  selb_require_columns(df_family_ses,
    c("group_f", "hba1c", "anne_antidepresan", "beck_total"),
    "§134 DM frame")
  df <- df_family_ses[as.character(df_family_ses$group_f) == "DM", , drop = FALSE]
  df$hba1c_available <- as.integer(!is.na(selb_numeric(df$hba1c)))
  df$ad_bin <- selb_ad_binary(df$anne_antidepresan)
  df$beck_total_num <- selb_numeric(df$beck_total)
  df$ses_latent_z <- if ("ses_latent" %in% names(df)) selb_scale(df$ses_latent) else rep(NA_real_, nrow(df))
  df$dm_yili_z <- if ("dm_yili" %in% names(df)) selb_scale(df$dm_yili) else rep(NA_real_, nrow(df))
  df$cocuk_yas_z <- if ("cocuk_yas" %in% names(df)) selb_scale(df$cocuk_yas) else rep(NA_real_, nrow(df))
  df
}

# AD x hba1c_available Fisher exact (OR + %95 GA + p)
selb_hba1c_ad_fisher <- function(df) {
  tab <- table(factor(df$ad_bin, levels = c(0, 1)),
    factor(df$hba1c_available, levels = c(0, 1)))
  ft <- tryCatch(stats::fisher.test(tab), error = function(e) NULL)
  data.frame(
    test = "Fisher exact: AD x HbA1c-availability (DM-only)",
    n_dm = nrow(df),
    ad0_avail0 = tab[1, 1], ad0_avail1 = tab[1, 2],
    ad1_avail0 = tab[2, 1], ad1_avail1 = tab[2, 2],
    avail_rate_ad0 = if (sum(tab[1, ]) > 0) tab[1, 2] / sum(tab[1, ]) else NA_real_,
    avail_rate_ad1 = if (sum(tab[2, ]) > 0) tab[2, 2] / sum(tab[2, ]) else NA_real_,
    odds_ratio = if (!is.null(ft)) unname(ft$estimate) else NA_real_,
    or_ci_lower = if (!is.null(ft)) ft$conf.int[1L] else NA_real_,
    or_ci_upper = if (!is.null(ft)) ft$conf.int[2L] else NA_real_,
    p_value = if (!is.null(ft)) ft$p.value else NA_real_,
    statu = selb_status_label(), stringsAsFactors = FALSE
  )
}

# Secilim yuzeyi: hba1c_available ~ AD + beck_total + ses + dm_yili + cocuk_yas
selb_hba1c_selection_model <- function(df) {
  needed <- c("hba1c_available", "ad_bin", "beck_total_num", "ses_latent_z",
    "dm_yili_z", "cocuk_yas_z")
  keep <- stats::complete.cases(df[, needed, drop = FALSE])
  sub <- df[keep, , drop = FALSE]
  if (nrow(sub) < 20L || length(unique(sub$hba1c_available)) < 2L) {
    return(data.frame(
      term = NA_character_, estimate_logodds = NA_real_, odds_ratio = NA_real_,
      or_ci_lower = NA_real_, or_ci_upper = NA_real_, se = NA_real_,
      z_value = NA_real_, p_value = NA_real_, n = nrow(sub),
      status = "yetersiz_n_veya_varyans", statu = selb_status_label(),
      stringsAsFactors = FALSE
    ))
  }
  fit <- stats::glm(
    hba1c_available ~ ad_bin + beck_total_num + ses_latent_z + dm_yili_z + cocuk_yas_z,
    data = sub, family = stats::binomial()
  )
  sm <- summary(fit)$coefficients
  ci <- tryCatch(suppressMessages(stats::confint(fit)), error = function(e) NULL)
  terms <- rownames(sm)
  data.frame(
    term = terms,
    estimate_logodds = sm[, "Estimate"],
    odds_ratio = exp(sm[, "Estimate"]),
    or_ci_lower = if (!is.null(ci)) exp(ci[terms, 1L]) else NA_real_,
    or_ci_upper = if (!is.null(ci)) exp(ci[terms, 2L]) else NA_real_,
    se = sm[, "Std. Error"],
    z_value = sm[, "z value"],
    p_value = sm[, "Pr(>|z|)"],
    n = stats::nobs(fit),
    status = "ok", statu = selb_status_label(),
    row.names = NULL, stringsAsFactors = FALSE
  )
}

# HbA1c-var vs HbA1c-yok DM alt-orneklemleri: Tablo-1 tarzi karsilastirma + SMD
selb_hba1c_availability_table1 <- function(df,
    vars = c("beck_total_num", "ses_latent_z", "dm_yili_z", "cocuk_yas_z", "ad_bin")) {
  vars <- intersect(vars, names(df))
  rows <- list()
  for (v in vars) {
    x <- selb_numeric(df[[v]])
    a <- x[df$hba1c_available == 1L]
    b <- x[df$hba1c_available == 0L]
    a <- a[!is.na(a)]; b <- b[!is.na(b)]
    smd <- NA_real_
    if (length(a) > 1L && length(b) > 1L) {
      sp <- sqrt(((length(a) - 1) * stats::var(a) + (length(b) - 1) * stats::var(b)) /
        (length(a) + length(b) - 2))
      smd <- if (!is.na(sp) && sp > 0) (mean(a) - mean(b)) / sp else NA_real_
    }
    rows[[v]] <- data.frame(
      degisken = v,
      n_hba1c_var = length(a), n_hba1c_yok = length(b),
      ort_var = if (length(a) > 0L) mean(a) else NA_real_,
      ort_yok = if (length(b) > 0L) mean(b) else NA_real_,
      medyan_var = if (length(a) > 0L) stats::median(a) else NA_real_,
      medyan_yok = if (length(b) > 0L) stats::median(b) else NA_real_,
      smd = smd, statu = selb_status_label(), stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# IPW FIZIBILITE-DUYARLILIGI (DUZELTME DEGIL). ESS + maks-agirlik + budama raporu.
selb_hba1c_ipw_feasibility <- function(df, trunc_q = 0.95) {
  needed <- c("hba1c_available", "ad_bin", "beck_total_num", "ses_latent_z",
    "dm_yili_z", "cocuk_yas_z")
  keep <- stats::complete.cases(df[, needed, drop = FALSE])
  sub <- df[keep, , drop = FALSE]
  base <- data.frame(
    amac = "SECILIM GOSTERIMI (feasibility) — TELAFI/DUZELTME DEGIL",
    n_model = nrow(sub),
    n_available = sum(sub$hba1c_available == 1L),
    ess = NA_real_, ess_orani = NA_real_,
    max_weight = NA_real_, min_weight = NA_real_,
    trunc_q = trunc_q, trunc_esik = NA_real_, n_truncated = NA_integer_,
    ess_truncated = NA_real_, max_weight_truncated = NA_real_,
    uyari = paste0("n cok kucuk; IPW gurultuyu buyutur. Agirliklar tani/gosterge ",
      "amacli; hicbir HbA1c-ebeveynlik tahmini IPW ile 'duzeltilmis' sayilmaz."),
    statu = selb_status_label(), stringsAsFactors = FALSE
  )
  if (nrow(sub) < 20L || length(unique(sub$hba1c_available)) < 2L) {
    base$uyari <- "yetersiz_n_veya_varyans; IPW hesaplanmadi"
    return(base)
  }
  fit <- stats::glm(
    hba1c_available ~ ad_bin + beck_total_num + ses_latent_z + dm_yili_z + cocuk_yas_z,
    data = sub, family = stats::binomial()
  )
  p_avail <- stats::fitted(fit)
  avail <- sub$hba1c_available == 1L
  # available gozlemler icin stabilize edilmemis IPW = 1/P(available)
  w <- rep(NA_real_, nrow(sub))
  w[avail] <- 1 / p_avail[avail]
  wa <- w[avail & is.finite(w)]
  ess_fun <- function(v) if (length(v) == 0L) NA_real_ else (sum(v)^2) / sum(v^2)
  base$ess <- ess_fun(wa)
  base$ess_orani <- base$ess / length(wa)
  base$max_weight <- max(wa)
  base$min_weight <- min(wa)
  esik <- unname(stats::quantile(wa, probs = trunc_q, na.rm = TRUE))
  wt <- pmin(wa, esik)
  base$trunc_esik <- esik
  base$n_truncated <- sum(wa > esik)
  base$ess_truncated <- ess_fun(wt)
  base$max_weight_truncated <- max(wt)
  base
}

# =========================================================================
# §135 — Alim-yili / batch duyarliligi
# =========================================================================

selb_year_frame <- function(df_family_ses, year_col = "anket_tarihi") {
  selb_require_columns(df_family_ses, c("group_f", year_col), "§135 yil frame")
  df <- df_family_ses
  df$anket_yil <- selb_extract_year(df[[year_col]])
  df
}

selb_year_group_table <- function(df) {
  yr <- df$anket_yil
  g <- as.character(df$group_f)
  keep <- !is.na(yr) & g %in% c("Kontrol", "DM")
  tab <- table(yr[keep], g[keep])
  years <- rownames(tab)
  data.frame(
    anket_yil = as.integer(years),
    n_kontrol = if ("Kontrol" %in% colnames(tab)) tab[, "Kontrol"] else 0L,
    n_dm = if ("DM" %in% colnames(tab)) tab[, "DM"] else 0L,
    toplam = rowSums(tab),
    statu = selb_status_label(), row.names = NULL, stringsAsFactors = FALSE
  )
}

# Kollinearite tanisi: group_dm ~ factor(yil) lojistik omnibus (yalniz TANI).
selb_year_collinearity <- function(df) {
  yr <- df$anket_yil
  g <- as.character(df$group_f)
  keep <- !is.na(yr) & g %in% c("Kontrol", "DM")
  sub <- data.frame(group_dm = as.integer(g[keep] == "DM"), yil = factor(yr[keep]))
  if (nlevels(sub$yil) < 2L || length(unique(sub$group_dm)) < 2L) {
    return(data.frame(
      test = "group_dm ~ factor(anket_yil) [SADECE KOLLINEARITE TANISI]",
      n = nrow(sub), n_yil = nlevels(sub$yil),
      lr_chisq = NA_real_, lr_df = NA_real_, p_value = NA_real_,
      cramers_v = NA_real_,
      not = "yetersiz varyans", statu = selb_status_label(), stringsAsFactors = FALSE
    ))
  }
  fit <- stats::glm(group_dm ~ yil, data = sub, family = stats::binomial())
  null <- stats::glm(group_dm ~ 1, data = sub, family = stats::binomial())
  lr <- stats::anova(null, fit, test = "LRT")
  chi <- suppressWarnings(stats::chisq.test(table(sub$group_dm, sub$yil)))
  n <- nrow(sub); k <- min(nlevels(sub$yil), 2L)
  cv <- sqrt(unname(chi$statistic) / (n * (k - 1)))
  data.frame(
    test = "group_dm ~ factor(anket_yil) [SADECE KOLLINEARITE TANISI — yil kovaryat degil]",
    n = n, n_yil = nlevels(sub$yil),
    lr_chisq = lr$Deviance[2L], lr_df = lr$Df[2L], p_value = lr$`Pr(>Chi)`[2L],
    cramers_v = cv,
    not = paste0("Yil grupla kollinear → grup etkisini emer; MODELE KOVARYAT ",
      "OLARAK EKLENMEZ. Bunun yerine 2023-only replikasyon + yil-tabakali betimsel."),
    statu = selb_status_label(), stringsAsFactors = FALSE
  )
}

# §135(i) — Anahtar grup kontrastlarinin 2023-only vs tam-orneklem replikasyonu.
selb_batch_replication <- function(df, replication_year = 2023L,
    outcomes = c("embu_c_idx_reddetme_mean", "embu_c_idx_asiri_koruma_mean",
      "embu_p_reddetme_mean", "embu_p_asiri_koruma_mean", "beck_total")) {
  outcomes <- intersect(outcomes, names(df))
  rows <- list()
  full <- df
  sub <- df[!is.na(df$anket_yil) & df$anket_yil == replication_year, , drop = FALSE]
  for (oc in outcomes) {
    df_full <- selb_group_d(full[[oc]], full$group_f)
    df_sub  <- selb_group_d(sub[[oc]], sub$group_f)
    dir_full <- sign(df_full$d)
    dir_sub <- sign(df_sub$d)
    dir_preserved <- !is.na(dir_full) & !is.na(dir_sub) & dir_full == dir_sub
    rows[[oc]] <- data.frame(
      outcome = oc,
      d_full = df_full$d, d_full_ci_lower = df_full$d_ci_lower,
      d_full_ci_upper = df_full$d_ci_upper, p_full = df_full$p_value,
      n_full_kontrol = df_full$n_ref, n_full_dm = df_full$n_foc,
      d_2023 = df_sub$d, d_2023_ci_lower = df_sub$d_ci_lower,
      d_2023_ci_upper = df_sub$d_ci_upper, p_2023 = df_sub$p_value,
      n_2023_kontrol = df_sub$n_ref, n_2023_dm = df_sub$n_foc,
      yon_korundu = dir_preserved,
      statu = selb_status_label(), stringsAsFactors = FALSE
    )
  }
  out <- do.call(rbind, rows)
  attr(out, "replication_year") <- replication_year
  out
}

# §135(ii) — Yil-tabakali betimsel (anahtar cocuk-algi + Beck; test yok).
selb_year_stratified_descriptive <- function(df,
    outcomes = c("embu_c_idx_reddetme_mean", "beck_total")) {
  outcomes <- intersect(outcomes, names(df))
  yr <- df$anket_yil
  g <- as.character(df$group_f)
  rows <- list()
  for (y in sort(unique(yr[!is.na(yr)]))) {
    for (grp in c("Kontrol", "DM")) {
      idx <- which(yr == y & g == grp)
      for (oc in outcomes) {
        vals <- selb_numeric(df[[oc]][idx]); vals <- vals[!is.na(vals)]
        rows[[paste(y, grp, oc, sep = "__")]] <- data.frame(
          anket_yil = y, group = grp, degisken = oc,
          n = length(vals),
          ortalama = if (length(vals) > 0L) mean(vals) else NA_real_,
          medyan = if (length(vals) > 0L) stats::median(vals) else NA_real_,
          sd = if (length(vals) > 1L) stats::sd(vals) else NA_real_,
          not = "betimsel; cikarimsal test YOK (yil-tabaka)",
          statu = selb_status_label(), stringsAsFactors = FALSE
        )
      }
    }
  }
  if (length(rows) == 0L) return(NULL)
  do.call(rbind, rows)
}

# =========================================================================
# Pipeline sarici
# =========================================================================

run_phase4_selection_batch_pipeline <- function(df_family_ses,
    year_col = "anket_tarihi", replication_year = 2023L, ipw_trunc_q = 0.95) {

  dm <- selb_dm_frame(df_family_ses)
  hba1c_fisher <- selb_hba1c_ad_fisher(dm)
  hba1c_selection <- selb_hba1c_selection_model(dm)
  hba1c_table1 <- selb_hba1c_availability_table1(dm)
  hba1c_ipw <- selb_hba1c_ipw_feasibility(dm, trunc_q = ipw_trunc_q)

  yf <- selb_year_frame(df_family_ses, year_col = year_col)
  year_group <- selb_year_group_table(yf)
  year_collinearity <- selb_year_collinearity(yf)
  batch_replication <- selb_batch_replication(yf, replication_year = replication_year)
  year_descriptive <- selb_year_stratified_descriptive(yf)

  target_summary <- data.frame(
    analysis = "phase4_selection_batch_validity",
    kisim = "KISIM XLIX (§134-135)",
    n_dm = nrow(dm),
    n_hba1c_var = sum(dm$hba1c_available == 1L),
    n_hba1c_yok = sum(dm$hba1c_available == 0L),
    hba1c_ad_or = hba1c_fisher$odds_ratio[1L],
    hba1c_ad_p = hba1c_fisher$p_value[1L],
    yil_grup_p = year_collinearity$p_value[1L],
    replication_year = replication_year,
    n_2023 = sum(!is.na(yf$anket_yil) & yf$anket_yil == replication_year),
    ipw_statu = "FIZIBILITE-DUYARLILIGI (duzeltme DEGIL)",
    imputation = "YOK (Kural 19)",
    kanit_kategorisi = selb_status_label(),
    sapma_tipi = "Tip 3 (Faz IV post-hoc, SAP KISIM XLIX/134-135; gecerlik-denetimi)",
    reference_doc = "07-sap-faz4-ek-plan.md",
    stringsAsFactors = FALSE
  )

  list(
    hba1c_ad_fisher = hba1c_fisher,
    hba1c_selection_model = hba1c_selection,
    hba1c_availability_table1 = hba1c_table1,
    hba1c_ipw_feasibility = hba1c_ipw,
    year_group_table = year_group,
    year_collinearity = year_collinearity,
    batch_replication = batch_replication,
    year_stratified_descriptive = year_descriptive,
    target_summary = target_summary
  )
}
