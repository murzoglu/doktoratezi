# [KESIFSEL - POST-HOC] Faz VI SAP KISIM LI (§142-151)
# Gelisimsel-Diadik Olcum Yuzeyi (Developmental-Dyadic Surface) — OSF Layer 7
#
# Bu modul YALNIZ saf fonksiyon icerir (dosya I/O YOK). Kanonik CSV'lere yazma
# yoktur; yukleme runner uzerinden R/01_io.R ile yapilir. Tum ciktilar agregat
# istatistiktir; satir-duzeyi katilimci verisi hicbir tabloya dokulmez.
#
# KAPSAM: Faz I-V sonrasi kanonik bazda MEVCUT ama focal girmemis iki eksen:
# (i) gelisimsel olcum ekseni (cocuk yasi -> anne-cocuk uyumu / transmisyon),
# (ii) kronik-hastalik diadik yuku (indeks dm_yili -> kardes algisi;
# maternal distres zaman-cizgisi). YENI VERI YOK; kanonik kilit DEGISMEZ;
# H1-H5 confirmatory cekirdek DEGISMEZ. Tum ciktilar korelasyoneldir; nedensel
# dil yasak. Cok-karsilastirma BH-FDR paragraf-ici. HARKing yasagi: hicbir
# bulgu H1-H4 prior'ini guclendirmez.
#
# §142 [Tier A/B]: Cocuk yasi x anne-cocuk uyumu + Faz V §137 b-yolu x yas.
#   Uyum: |embu_p - embu_c_idx| (aile) ~ cocuk_yas; kucuk fark = yuksek uyum.
#   Transmisyon: embu_c_idx ~ embu_p * cocuk_yas -> b-yolunun yas-egimi.
#   Klinik: kucuk cocugun perspektif-alma kisitli -> uyum/transmisyon yasla artar mi?
# §143 [Tier C/D betimsel + B]: "Cam kardes". (a) indeks dm_yili -> kardes
#   EMBU-C (DM-only, betimsel). (b) kardes EMBU-C grup farki
#   (koruma-genelleşme vs tukenme cercevesi; DM_Hasta_Kardes vs Kontrol_Kardes).
# §144 [Tier C DM-only]: beck_total ~ ns(dm_yili,3) — maternal distres adaptasyon
#   egrisi (kesitsel psodo-trajektuvar; egri sekli ciktidir, onceden varsayilmaz).
# §145 [Tier C]: Kardes iliski sicakligi (SRQ warmth) uyum/transmisyon moderatoru.
# §146 [Tier B/C]: Triadik konfigurasyonel aile-iklimi tipolojisi (mclust LPA;
#   9 gosterge = anne/indeks/kardes x sicaklik/reddetme/asiri_koruma).
# §147 [Tier B]: Uyum yonu — isaretli bias (anne - indeks) x grup (sosyal
#   istenirlik/suculuk yorumu spekulatif; ayrik adil-madde yok).

# ---------------------------------------------------------------------------
# Sabitler ve yardimcilar (f6_ — modul kendi-kendine yeter, f5'ten bagimsiz)
# ---------------------------------------------------------------------------

f6_status_label <- function() "[KESIFSEL - POST-HOC]"

f6_embu_subscales <- function() c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")

f6_triadic_subscales <- function() c("sicaklik", "reddetme", "asiri_koruma")

f6_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

f6_num <- function(x) suppressWarnings(as.numeric(as.character(x)))

f6_scale <- function(x) {
  x <- f6_num(x)
  ok <- !is.na(x)
  out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) return(out)
  s <- stats::sd(x[ok])
  if (is.na(s) || s == 0) return(out)
  out[ok] <- (x[ok] - mean(x[ok])) / s
  out
}

f6_group_factor <- function(df) {
  g <- if ("group_f" %in% names(df)) as.character(df$group_f)
       else if ("group" %in% names(df)) as.character(df$group)
       else rep(NA_character_, nrow(df))
  factor(g, levels = c("Kontrol", "DM"))
}

# TOST — korelasyon esdegerligi (Fisher-z; SESOI |r|)
f6_tost_r <- function(r, n, sesoi = 0.10, alpha = 0.05) {
  if (is.na(r) || is.na(n) || n < 5L || abs(r) >= 1) {
    return(list(p = NA_real_, decision = NA_character_))
  }
  z <- atanh(r); se <- 1 / sqrt(n - 3)
  p_lower <- stats::pnorm((z - atanh(-sesoi)) / se, lower.tail = FALSE)
  p_upper <- stats::pnorm((z - atanh(sesoi)) / se, lower.tail = TRUE)
  p_tost <- max(p_lower, p_upper)
  list(p = p_tost, decision = if (p_tost < alpha) "esdeger(|r|<SESOI)" else "esdeger_degil")
}

# TOST — ortalama farki esdegerligi (Cohen d; SESOI d)
f6_tost_d <- function(x0, x1, sesoi = 0.20, alpha = 0.05) {
  x0 <- x0[!is.na(x0)]; x1 <- x1[!is.na(x1)]
  n0 <- length(x0); n1 <- length(x1)
  if (n0 < 3L || n1 < 3L) return(list(p = NA_real_, decision = NA_character_))
  sp <- sqrt(((n0 - 1) * stats::var(x0) + (n1 - 1) * stats::var(x1)) / (n0 + n1 - 2))
  if (is.na(sp) || sp == 0) return(list(p = NA_real_, decision = NA_character_))
  se <- sp * sqrt(1 / n0 + 1 / n1); diff <- mean(x1) - mean(x0)
  p_low <- stats::pt((diff - (-sesoi * sp)) / se, df = n0 + n1 - 2, lower.tail = FALSE)
  p_up <- stats::pt((diff - (sesoi * sp)) / se, df = n0 + n1 - 2, lower.tail = TRUE)
  p_tost <- max(p_low, p_up)
  list(p = p_tost, decision = if (p_tost < alpha) "esdeger(|d|<SESOI)" else "esdeger_degil")
}

f6_cohen_d <- function(x0, x1) {
  x0 <- x0[!is.na(x0)]; x1 <- x1[!is.na(x1)]
  n0 <- length(x0); n1 <- length(x1)
  if (n0 < 2L || n1 < 2L) return(NA_real_)
  sp <- sqrt(((n0 - 1) * stats::var(x0) + (n1 - 1) * stats::var(x1)) / (n0 + n1 - 2))
  if (is.na(sp) || sp == 0) return(NA_real_)
  (mean(x1) - mean(x0)) / sp
}

# ---------------------------------------------------------------------------
# §142 — Cocuk yasi x anne-cocuk uyumu (concordance)
# ---------------------------------------------------------------------------
# Uyum olcutu: mutlak diad-farki |embu_p - embu_c_idx| (dusuk = yuksek uyum).
# Yordanan: mutlak fark; moderator: cocuk_yas. Negatif r => yasla uyum ARTAR.
# Ek betimsel: <10 vs >=10 yas ortalama mutlak fark (klinik cerceve).

f6_age_concordance <- function(df, subs = f6_embu_subscales(), sesoi_r = 0.10) {
  f6_require_columns(df, c("cocuk_yas", "ses_latent",
    paste0("embu_p_", subs, "_mean"), paste0("embu_c_idx_", subs, "_mean")),
    "§142 yas x uyum")
  grp <- f6_group_factor(df)
  cy <- f6_num(df$cocuk_yas)

  rows <- list()
  for (sub in subs) {
    p <- f6_num(df[[paste0("embu_p_", sub, "_mean")]])
    c <- f6_num(df[[paste0("embu_c_idx_", sub, "_mean")]])
    absdiff <- abs(p - c)
    ok <- stats::complete.cases(absdiff, cy)
    ad <- absdiff[ok]; ag <- cy[ok]; n <- length(ad)
    if (n < 10L || stats::sd(ad) == 0 || stats::sd(ag) == 0) {
      rows[[length(rows) + 1L]] <- data.frame(
        boyut = sub, n = n, r_yas_fark = NA_real_, ci_alt = NA_real_, ci_ust = NA_real_,
        p = NA_real_, std_beta_yas = NA_real_, tost_p = NA_real_, tost_karar = NA_character_,
        n_kucuk = NA_integer_, n_buyuk = NA_integer_, fark_kucuk = NA_real_, fark_buyuk = NA_real_,
        sesoi_r = sesoi_r, statu_kosum = "yetersiz_n",
        aciklama = "cocuk_yas -> |anne-cocuk farki|; negatif r=yasla uyum artar; korelasyonel",
        statu = f6_status_label(), stringsAsFactors = FALSE)
      next
    }
    ct <- stats::cor.test(ag, ad)
    dd <- data.frame(y = f6_scale(absdiff), age = f6_scale(cy), grp = grp, ses = f6_scale(df$ses_latent))
    dd <- dd[stats::complete.cases(dd), , drop = FALSE]
    m <- tryCatch(stats::lm(y ~ age + grp + ses, data = dd), error = function(e) NULL)
    std_beta <- if (!is.null(m)) unname(stats::coef(m)["age"]) else NA_real_
    tost <- f6_tost_r(unname(ct$estimate), n, sesoi = sesoi_r)
    young <- ad[ag < 10]; old <- ad[ag >= 10]
    rows[[length(rows) + 1L]] <- data.frame(
      boyut = sub, n = n, r_yas_fark = unname(ct$estimate), ci_alt = ct$conf.int[1],
      ci_ust = ct$conf.int[2], p = ct$p.value, std_beta_yas = std_beta,
      tost_p = tost$p, tost_karar = tost$decision,
      n_kucuk = length(young), n_buyuk = length(old),
      fark_kucuk = if (length(young) > 0L) mean(young) else NA_real_,
      fark_buyuk = if (length(old) > 0L) mean(old) else NA_real_,
      sesoi_r = sesoi_r, statu_kosum = "ok",
      aciklama = "cocuk_yas -> |anne-cocuk farki|; std_beta group+ses kontrollu; <10 vs >=10 betimsel",
      statu = f6_status_label(), stringsAsFactors = FALSE)
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §142 — Cocuk yasi x transmisyon (Faz V §137 b-yolu genisletmesi)
# ---------------------------------------------------------------------------
# embu_c_idx ~ embu_p * cocuk_yas + anne_yas + ses (aile, standardize).
# Odak: embu_p:cocuk_yas etkilesimi (b-yolunun yas-egimi).

f6_age_transmission <- function(df, subs = f6_embu_subscales()) {
  f6_require_columns(df, c("cocuk_yas", "anne_yas", "ses_latent",
    paste0("embu_p_", subs, "_mean"), paste0("embu_c_idx_", subs, "_mean")),
    "§142 yas x transmisyon")
  rows <- list()
  for (sub in subs) {
    dd <- data.frame(
      Y = f6_scale(df[[paste0("embu_c_idx_", sub, "_mean")]]),
      M = f6_scale(df[[paste0("embu_p_", sub, "_mean")]]),
      age = f6_scale(df$cocuk_yas),
      c1 = f6_scale(df$anne_yas),
      c2 = f6_scale(df$ses_latent))
    dd <- dd[stats::complete.cases(dd), , drop = FALSE]
    n <- nrow(dd)
    if (n < 20L) {
      rows[[length(rows) + 1L]] <- data.frame(
        boyut = sub, n = n, b_ana = NA_real_, b_ana_p = NA_real_,
        b_x_yas = NA_real_, ci_alt = NA_real_, ci_ust = NA_real_, etkilesim_p = NA_real_,
        statu_kosum = "yetersiz_n",
        aciklama = "embu_c_idx ~ embu_p*cocuk_yas; b-yolu yas-egimi; korelasyonel",
        statu = f6_status_label(), stringsAsFactors = FALSE)
      next
    }
    m <- stats::lm(Y ~ M * age + c1 + c2, data = dd)
    sm <- summary(m)$coefficients
    ci <- stats::confint(m)
    rows[[length(rows) + 1L]] <- data.frame(
      boyut = sub, n = n,
      b_ana = unname(stats::coef(m)["M"]), b_ana_p = sm["M", 4],
      b_x_yas = unname(stats::coef(m)["M:age"]), ci_alt = ci["M:age", 1],
      ci_ust = ci["M:age", 2], etkilesim_p = sm["M:age", 4],
      statu_kosum = "ok",
      aciklama = "b-yolu (P->C_idx) yas-egimi; pozitif=buyuk cocukta transmisyon guclu; korelasyonel",
      statu = f6_status_label(), stringsAsFactors = FALSE)
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §143 — "Cam kardes": indeks hastalik-yuku -> kardes algisi
# ---------------------------------------------------------------------------
# (a) dm_yili -> kardes EMBU-C (DM-only; betimsel).
# (b) kardes EMBU-C grup farki (koruma-genelleşme vs tukenme).

f6_glass_sibling <- function(df, subs = f6_embu_subscales(), sesoi_d = 0.20) {
  f6_require_columns(df, c("dm_yili", paste0("embu_c_sib_", subs, "_mean")),
    "§143 cam kardes")
  grp <- f6_group_factor(df)
  dy <- f6_num(df$dm_yili)

  sev_rows <- list()  # (a) siddet/sure -> kardes algisi (DM-only)
  for (sub in subs) {
    sib <- f6_num(df[[paste0("embu_c_sib_", sub, "_mean")]])
    for (pred_name in c("dm_yili")) {
      x <- dy
      ok <- stats::complete.cases(x, sib)
      n <- sum(ok)
      if (n < 10L || stats::sd(x[ok]) == 0 || stats::sd(sib[ok]) == 0) {
        sev_rows[[length(sev_rows) + 1L]] <- data.frame(
          yordayici = pred_name, boyut = sub, n = n, r = NA_real_, ci_alt = NA_real_,
          ci_ust = NA_real_, p = NA_real_, statu_kosum = "yetersiz_n",
          aciklama = "DM-only; indeks hastalik-yuku -> kardes algisi; betimsel (dusuk guc)",
          statu = f6_status_label(), stringsAsFactors = FALSE)
        next
      }
      ct <- stats::cor.test(x[ok], sib[ok])
      sev_rows[[length(sev_rows) + 1L]] <- data.frame(
        yordayici = pred_name, boyut = sub, n = n, r = unname(ct$estimate),
        ci_alt = ct$conf.int[1], ci_ust = ct$conf.int[2], p = ct$p.value,
        statu_kosum = "ok",
        aciklama = "DM-only; indeks hastalik-yuku -> kardes algisi; korelasyonel",
        statu = f6_status_label(), stringsAsFactors = FALSE)
    }
  }
  severity <- do.call(rbind, sev_rows)

  # (b) genelleşme vs tukenme: kardes EMBU-C, DM vs Kontrol (d = DM - Kontrol)
  gen_rows <- list()
  for (sub in subs) {
    sib <- f6_num(df[[paste0("embu_c_sib_", sub, "_mean")]])
    y0 <- sib[grp == "Kontrol" & !is.na(sib)]  # Kontrol_Kardes
    y1 <- sib[grp == "DM" & !is.na(sib)]        # DM_Hasta_Kardes
    if (length(y0) < 3L || length(y1) < 3L) {
      gen_rows[[length(gen_rows) + 1L]] <- data.frame(
        boyut = sub, n_kontrol = length(y0), n_dm = length(y1), ort_kontrol = NA_real_,
        ort_dm = NA_real_, cohen_d = NA_real_, t_p = NA_real_, tost_p = NA_real_,
        tost_karar = NA_character_, yorum = NA_character_, sesoi_d = sesoi_d,
        statu_kosum = "yetersiz_n", statu = f6_status_label(), stringsAsFactors = FALSE)
      next
    }
    d <- f6_cohen_d(y0, y1); tt <- stats::t.test(y1, y0); tost <- f6_tost_d(y0, y1, sesoi = sesoi_d)
    yorum <- if (sub == "asiri_koruma") "asiri_koruma yuksek=koruma-genelleşme sinyali"
             else if (sub == "sicaklik") "sicaklik dusuk=tukenme sinyali"
             else "reddetme/karsilastirma yuksek=kardes dezavantaji"
    gen_rows[[length(gen_rows) + 1L]] <- data.frame(
      boyut = sub, n_kontrol = length(y0), n_dm = length(y1), ort_kontrol = mean(y0),
      ort_dm = mean(y1), cohen_d = d, t_p = tt$p.value, tost_p = tost$p,
      tost_karar = tost$decision, yorum = yorum, sesoi_d = sesoi_d,
      statu_kosum = "ok", statu = f6_status_label(), stringsAsFactors = FALSE)
  }
  generalization <- do.call(rbind, gen_rows)

  list(severity = severity, generalization = generalization)
}

# ---------------------------------------------------------------------------
# §144 — Maternal distres zaman-cizgisi: beck ~ ns(dm_yili, 3) [DM-only]
# ---------------------------------------------------------------------------

f6_maternal_distress_timeline <- function(df, df_spline = 3L) {
  f6_require_columns(df, c("beck_total", "dm_yili", "anne_yas", "ses_latent"),
    "§144 distres zaman-cizgisi")
  dd <- data.frame(
    beck = f6_num(df$beck_total), dy = f6_num(df$dm_yili),
    age = f6_scale(df$anne_yas), ses = f6_scale(df$ses_latent))
  dd <- dd[stats::complete.cases(dd), , drop = FALSE]
  n <- nrow(dd)
  status <- data.frame(analiz = "beck~ns(dm_yili,3)", n = n, df_spline = df_spline,
    lin_slope = NA_real_, lin_p = NA_real_, lrt_F = NA_real_, lrt_p = NA_real_,
    statu_kosum = if (n >= 20L) "ok" else "yetersiz_n",
    aciklama = "DM-only; kesitsel psodo-trajektuvar; egri sekli ciktidir; nedensel dil yok",
    statu = f6_status_label(), stringsAsFactors = FALSE)
  shape <- data.frame(dm_yili = numeric(), beck_tahmin = numeric(),
    statu = character(), stringsAsFactors = FALSE)
  if (n >= 20L && stats::sd(dd$dy) > 0) {
    m_lin <- stats::lm(beck ~ dy + age + ses, data = dd)
    m_spl <- stats::lm(beck ~ splines::ns(dy, df = df_spline) + age + ses, data = dd)
    an <- stats::anova(m_lin, m_spl)
    status$lin_slope <- unname(stats::coef(m_lin)["dy"])
    status$lin_p <- summary(m_lin)$coefficients["dy", 4]
    status$lrt_F <- an$F[2]
    status$lrt_p <- an$`Pr(>F)`[2]
    grid_dy <- as.numeric(stats::quantile(dd$dy, c(0, 0.25, 0.5, 0.75, 1.0)))
    pred_df <- data.frame(dy = grid_dy, age = 0, ses = 0)
    pr <- stats::predict(m_spl, newdata = pred_df)
    shape <- data.frame(dm_yili = round(grid_dy, 2), beck_tahmin = round(unname(pr), 2),
      statu = f6_status_label(), stringsAsFactors = FALSE)
  }
  list(status = status, shape = shape)
}

# ---------------------------------------------------------------------------
# §145 — Kardes sicakligi (SRQ warmth) uyum/transmisyon moderatoru
# ---------------------------------------------------------------------------
# Aile-sicakligi = mean(srq_ho_warmth, srq_sib_ho_warmth). Moderator:
# (i) transmisyon (embu_c_idx ~ embu_p * warmth), (ii) uyum (|fark| ~ warmth).

f6_sibling_warmth_moderation <- function(df, subs = f6_embu_subscales()) {
  need <- c("srq_ho_warmth_mean", paste0("embu_p_", subs, "_mean"),
    paste0("embu_c_idx_", subs, "_mean"))
  f6_require_columns(df, need, "§145 kardes sicakligi moderator")
  w_idx <- f6_num(df$srq_ho_warmth_mean)
  w_sib <- if ("srq_sib_ho_warmth_mean" %in% names(df)) f6_num(df$srq_sib_ho_warmth_mean) else NA_real_
  warmth <- if (length(w_sib) == length(w_idx)) rowMeans(cbind(w_idx, w_sib), na.rm = TRUE) else w_idx
  warmth[is.nan(warmth)] <- NA_real_

  rows <- list()
  for (sub in subs) {
    p <- f6_num(df[[paste0("embu_p_", sub, "_mean")]])
    c <- f6_num(df[[paste0("embu_c_idx_", sub, "_mean")]])
    dd <- data.frame(Y = f6_scale(c), M = f6_scale(p), W = f6_scale(warmth),
      absdiff = f6_scale(abs(p - c)))
    dd <- dd[stats::complete.cases(dd$Y, dd$M, dd$W), , drop = FALSE]
    n <- nrow(dd)
    if (n < 20L) {
      rows[[length(rows) + 1L]] <- data.frame(boyut = sub, n = n,
        trans_x_warmth = NA_real_, trans_p = NA_real_, uyum_x_warmth = NA_real_,
        uyum_p = NA_real_, statu_kosum = "yetersiz_n",
        aciklama = "kardes sicakligi moderatoru; dusuk guc; korelasyonel",
        statu = f6_status_label(), stringsAsFactors = FALSE)
      next
    }
    mt <- stats::lm(Y ~ M * W, data = dd)
    smt <- summary(mt)$coefficients
    md <- tryCatch(stats::lm(absdiff ~ W, data = dd[stats::complete.cases(dd$absdiff, dd$W), ]),
      error = function(e) NULL)
    rows[[length(rows) + 1L]] <- data.frame(boyut = sub, n = n,
      trans_x_warmth = unname(stats::coef(mt)["M:W"]), trans_p = smt["M:W", 4],
      uyum_x_warmth = if (!is.null(md)) unname(stats::coef(md)["W"]) else NA_real_,
      uyum_p = if (!is.null(md)) summary(md)$coefficients["W", 4] else NA_real_,
      statu_kosum = "ok",
      aciklama = "warmth x transmisyon (M:W) + warmth -> |fark|; korelasyonel; dusuk guc",
      statu = f6_status_label(), stringsAsFactors = FALSE)
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §146 — Triadik konfigurasyonel aile-iklimi tipolojisi (mclust LPA)
# ---------------------------------------------------------------------------
# 9 gosterge: anne(embu_p) + indeks(embu_c_idx) + kardes(embu_c_sib) x
# sicaklik/reddetme/asiri_koruma. BIC ile sinif secimi; entropy + grup dagilimi.

f6_triadic_typology <- function(df, subs = f6_triadic_subscales(), g_range = 1:5,
                                seed = 20260714L) {
  cols <- c(paste0("embu_p_", subs, "_mean"), paste0("embu_c_idx_", subs, "_mean"),
    paste0("embu_c_sib_", subs, "_mean"))
  f6_require_columns(df, cols, "§146 triadik tipoloji")
  X <- as.data.frame(lapply(cols, function(cc) f6_scale(df[[cc]])))
  names(X) <- cols
  ok <- stats::complete.cases(X)
  Xc <- X[ok, , drop = FALSE]
  grp <- f6_group_factor(df)[ok]
  n <- nrow(Xc)

  status <- data.frame(analiz = "triadik_LPA(tidyLPA,diagonal)", n = n, gosterge_sayisi = length(cols),
    en_iyi_G = NA_integer_, en_iyi_model = NA_integer_, bic = NA_real_, entropy = NA_real_,
    statu_kosum = if (n < 50L) "yetersiz_n" else if (!requireNamespace("tidyLPA", quietly = TRUE)) "paket_yok" else "beklemede",
    aciklama = "9 gosterge triadik profil; diyagonal (yerel bagimsizlik) LPA model 1-2; etiketler betimsel (tani degil); dusuk-BIC secimi",
    statu = f6_status_label(), stringsAsFactors = FALSE)
  fit_tbl <- data.frame(); prof_tbl <- data.frame(); grp_tbl <- data.frame()

  if (n >= 50L && requireNamespace("tidyLPA", quietly = TRUE)) {
    set.seed(seed)
    suppressWarnings(suppressMessages(requireNamespace("tidyLPA")))
    res <- tryCatch(
      suppressWarnings(suppressMessages(
        tidyLPA::estimate_profiles(Xc, n_profiles = g_range, models = c(1L, 2L)))),
      error = function(e) NULL)
    # get_fit/get_data/get_estimates sarmalayicilari fonksiyon-ici NSE ile
    # kirilir -> her res elemaninin $fit/$estimates/$dff'ine DOGRUDAN erisilir.
    # Gercek veride bazi model/sinif kombinasyonlari kestirilemez -> $fit atomik
    # NA doner; bunlar filtrelenir.
    fit_rows <- if (is.null(res)) list() else lapply(res, function(el) {
      f <- el$fit
      if (is.null(f) || !is.data.frame(f) || !("BIC" %in% names(f)) ||
          length(f$BIC) < 1L || !is.finite(f$BIC[1])) return(NULL)
      data.frame(model = as.integer(f$Model), G = as.integer(f$Classes),
        bic = as.numeric(f$BIC), entropy = as.numeric(f$Entropy),
        statu = f6_status_label(), stringsAsFactors = FALSE)
    })
    fit_rows <- Filter(Negate(is.null), fit_rows)
    status$statu_kosum <- if (length(fit_rows) == 0L) "lpa_basarisiz" else "ok"
    if (length(fit_rows) > 0L) {
      fit_tbl <- do.call(rbind, fit_rows); rownames(fit_tbl) <- NULL
      best_i <- which.min(fit_tbl$bic)
      bestM <- fit_tbl$model[best_i]; bestK <- fit_tbl$G[best_i]
      best_el <- res[[paste0("model_", bestM, "_class_", bestK)]]
      status$en_iyi_G <- bestK; status$en_iyi_model <- bestM
      status$bic <- fit_tbl$bic[best_i]; status$entropy <- fit_tbl$entropy[best_i]

      est <- best_el$estimates
      est <- est[est$Category == "Means", , drop = FALSE]
      cls <- as.integer(best_el$dff$Class)  # Xc satir sirasinda
      n_by_class <- as.integer(table(factor(cls, levels = seq_len(bestK))))

      prof_tbl <- data.frame(sinif = seq_len(bestK), stringsAsFactors = FALSE)
      for (cc in cols) {
        vals <- vapply(seq_len(bestK), function(k) {
          v <- est$Estimate[est$Class == k & est$Parameter == cc]
          if (length(v) == 1L) round(v, 3) else NA_real_
        }, numeric(1))
        prof_tbl[[cc]] <- vals
      }
      prof_tbl$n_sinif <- n_by_class
      prof_tbl$oran <- round(n_by_class / sum(n_by_class), 3)
      prof_tbl$statu <- f6_status_label()

      ct <- table(sinif = cls, grup = grp)  # grp Xc sirasinda
      grp_tbl <- as.data.frame.matrix(ct)
      grp_tbl$sinif <- as.integer(rownames(grp_tbl))
      grp_tbl$statu <- f6_status_label()
      rownames(grp_tbl) <- NULL
    }
  }
  list(status = status, fit = fit_tbl, profiles = prof_tbl, group_distribution = grp_tbl)
}

# ---------------------------------------------------------------------------
# §147 — Uyum yonu: isaretli bias (anne - indeks) x grup
# ---------------------------------------------------------------------------

f6_discordance_direction <- function(df, subs = f6_embu_subscales(), sesoi_d = 0.20) {
  f6_require_columns(df, c(paste0("embu_p_", subs, "_mean"),
    paste0("embu_c_idx_", subs, "_mean")), "§147 uyum yonu")
  grp <- f6_group_factor(df)
  rows <- list()
  for (sub in subs) {
    p <- f6_num(df[[paste0("embu_p_", sub, "_mean")]])
    c <- f6_num(df[[paste0("embu_c_idx_", sub, "_mean")]])
    bias <- p - c  # + => anne cocuktan yuksek bildiriyor
    b0 <- bias[grp == "Kontrol" & !is.na(bias)]
    b1 <- bias[grp == "DM" & !is.na(bias)]
    if (length(b0) < 3L || length(b1) < 3L) {
      rows[[length(rows) + 1L]] <- data.frame(boyut = sub, n_kontrol = length(b0),
        n_dm = length(b1), bias_kontrol = NA_real_, bias_dm = NA_real_,
        bias_kontrol_p = NA_real_, bias_dm_p = NA_real_, grup_d = NA_real_,
        grup_p = NA_real_, tost_p = NA_real_, tost_karar = NA_character_, sesoi_d = sesoi_d,
        statu_kosum = "yetersiz_n",
        aciklama = "isaretli bias (anne-indeks) x grup; + = anne yuksek; korelasyonel",
        statu = f6_status_label(), stringsAsFactors = FALSE)
      next
    }
    tt0 <- stats::t.test(b0); tt1 <- stats::t.test(b1)
    d <- f6_cohen_d(b0, b1); tt <- stats::t.test(b1, b0); tost <- f6_tost_d(b0, b1, sesoi = sesoi_d)
    rows[[length(rows) + 1L]] <- data.frame(boyut = sub, n_kontrol = length(b0),
      n_dm = length(b1), bias_kontrol = mean(b0), bias_dm = mean(b1),
      bias_kontrol_p = tt0$p.value, bias_dm_p = tt1$p.value, grup_d = d, grup_p = tt$p.value,
      tost_p = tost$p, tost_karar = tost$decision, sesoi_d = sesoi_d, statu_kosum = "ok",
      aciklama = "isaretli bias (anne-indeks); +=anne oz-yuceltme; grup farki d; korelasyonel",
      statu = f6_status_label(), stringsAsFactors = FALSE)
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# FDR (BH) — her paragraf kendi ailesi
# ---------------------------------------------------------------------------

f6_fdr_table <- function(concordance, transmission, glass_gen, discordance, warmth) {
  collect <- function(par, nm, p) {
    keep <- !is.na(p)
    if (!any(keep)) return(NULL)
    data.frame(paragraf = par, test_adi = nm[keep], p_ham = p[keep], stringsAsFactors = FALSE)
  }
  fam <- list()
  # §142a (uyum) ve §142b (transmisyon) FARKLI estimand aileleridir -> ayri BH.
  ok142a <- concordance[concordance$statu_kosum == "ok", , drop = FALSE]
  ok142b <- transmission[transmission$statu_kosum == "ok", , drop = FALSE]
  if (nrow(ok142a)) fam[["142a"]] <- collect("§142a", paste0("uyum:", ok142a$boyut), ok142a$p)
  if (nrow(ok142b)) fam[["142b"]] <- collect("§142b", paste0("transmisyon:", ok142b$boyut), ok142b$etkilesim_p)
  okgen <- glass_gen[glass_gen$statu_kosum == "ok", , drop = FALSE]
  if (nrow(okgen)) fam[["143"]] <- collect("§143b", paste0("kardes:", okgen$boyut), okgen$t_p)
  okw <- warmth[warmth$statu_kosum == "ok", , drop = FALSE]
  if (nrow(okw)) fam[["145"]] <- collect("§145", paste0("warmth:", okw$boyut), okw$trans_p)
  okd <- discordance[discordance$statu_kosum == "ok", , drop = FALSE]
  if (nrow(okd)) fam[["147"]] <- collect("§147", paste0("bias:", okd$boyut), okd$grup_p)

  base <- do.call(rbind, fam)
  if (is.null(base) || nrow(base) == 0L) {
    return(data.frame(paragraf = character(), test_adi = character(), p_ham = numeric(),
      p_bh = numeric(), yontem = character(), statu = character(), stringsAsFactors = FALSE))
  }
  base$p_bh <- NA_real_
  for (par in unique(base$paragraf)) {
    idx <- base$paragraf == par
    base$p_bh[idx] <- stats::p.adjust(base$p_ham[idx], method = "BH")
  }
  base$yontem <- "BH(paragraf-ici)"; base$statu <- f6_status_label()
  rownames(base) <- NULL
  base
}

# ---------------------------------------------------------------------------
# Pipeline sarici (Faz III/IV/V deseni)
# ---------------------------------------------------------------------------

run_phase6_developmental_pipeline <- function(df_family_ses,
                                              subscales = f6_embu_subscales(),
                                              triadic_subs = f6_triadic_subscales(),
                                              sesoi_r = 0.10, sesoi_d = 0.20,
                                              seed = 20260714L) {
  concordance <- f6_age_concordance(df_family_ses, subs = subscales, sesoi_r = sesoi_r)
  transmission <- f6_age_transmission(df_family_ses, subs = subscales)
  glass <- f6_glass_sibling(df_family_ses, subs = subscales, sesoi_d = sesoi_d)
  timeline <- f6_maternal_distress_timeline(df_family_ses)
  warmth <- f6_sibling_warmth_moderation(df_family_ses, subs = subscales)
  typology <- f6_triadic_typology(df_family_ses, subs = triadic_subs, seed = seed)
  discordance <- f6_discordance_direction(df_family_ses, subs = subscales, sesoi_d = sesoi_d)
  fdr <- f6_fdr_table(concordance, transmission, glass$generalization, discordance, warmth)

  target_summary <- data.frame(
    analiz = "phase6_developmental_dyadic",
    kisim = "KISIM LI (§142-151) — Faz VI",
    n_aile = nrow(df_family_ses),
    sesoi_r = sesoi_r, sesoi_d = sesoi_d, seed = seed,
    kanit_kategorisi = f6_status_label(),
    sapma_tipi = "Tip 3 (Faz VI post-hoc genisletme; OSF Layer 7)",
    reference_doc = "docs/analiz_planlari/09-sap-faz6-ek-plan.md v0.1",
    dil_notu = "Korelasyonel dil; nedensel dil yasak; H1-H5 confirmatory DEGISMEZ",
    stringsAsFactors = FALSE)

  list(
    age_concordance = concordance,
    age_transmission = transmission,
    glass_severity = glass$severity,
    glass_generalization = glass$generalization,
    distress_timeline_status = timeline$status,
    distress_timeline_shape = timeline$shape,
    sibling_warmth = warmth,
    triadic_status = typology$status,
    triadic_fit = typology$fit,
    triadic_profiles = typology$profiles,
    triadic_group_distribution = typology$group_distribution,
    discordance_direction = discordance,
    fdr = fdr,
    target_summary = target_summary)
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
