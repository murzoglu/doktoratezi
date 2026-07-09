# [KESIFSEL - POST-HOC] Faz III SAP KISIM XL / §110-111
# DM-Spesifik Maruziyet Yogunlugu (DM-only, agir kisitli)
#
# Kapsam (yalniz DM alt-orneklemi, indeks aile n=120):
#   §110 [duyarlilik katmani] — Yasam-orani maruziyet x asiri koruma:
#     illness_life_ratio = dm_yili / cocuk_yas. Uc maruziyet parametrizasyonu
#     YAN YANA (AIC ile karsilastirilarak):
#       (i)   illness_life_ratio  (oran; DOGRULANMAMIS metrik → duyarlilik)
#       (ii)  dm_yili + cocuk_yas_z kovaryat  (Mullins gelisimsel moderasyon)
#       (iii) tani_yasi (cocuk_yas - dm_yili) x cocuk_yas etkilesimi (Malik & Koot)
#     Ciktilar: embu_c_idx_asiri_koruma_mean (family) + embu_p_asiri_koruma_mean
#     + srq_ho_conflict_mean. Her parametrizasyon icin katsayi + %95 GA + AIC.
#     Yan-analiz: psikolojik-kontrol proxy (embu_c_idx reddetme + karsilastirma)
#     — Prikken et al. (2019) duzeltmesi: T1DM'de operatif mediyator asiri koruma
#     DEGIL psikolojik kontroldur.
#   §111 [yalniz betimsel eskiz] — Kardes tani-ani yasi (kardes_yas - dm_yili);
#     gelisim penceresi bandlari (<0, 0-5, 5-10, >=10) betimsel n + kardes
#     SRQ/EMBU-C ortalamalari. CIKARIMSAL TEST YOK.
#
# ⚠️ Imputation YAPILMAZ (Skill Kurali 19). NA'lar acik raporlanir.
# ⚠️ illness_life_ratio DOGRULANMAMIS metrik → duyarlilik, kanonik alternatiflerle yan yana.
# ⚠️ Korelasyonel dil; nedensel dil yok. Tum ciktilar [KESIFSEL - POST-HOC].

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}

dmexp_status_label <- function() "[KESIFSEL - POST-HOC]"

# Analiz sabitleri --------------------------------------------------------

dmexp_overprotection_outcomes <- function() {
  c("embu_c_idx_asiri_koruma_mean", "embu_p_asiri_koruma_mean", "srq_ho_conflict_mean")
}

dmexp_psychcontrol_components <- function() {
  c("embu_c_idx_reddetme_mean", "embu_c_idx_karsilastirma_mean")
}

dmexp_sibling_outcomes <- function() {
  c(
    "embu_c_sib_asiri_koruma_mean", "embu_c_sib_reddetme_mean",
    "embu_c_sib_sicaklik_mean", "srq_sib_ho_warmth_mean",
    "srq_sib_ho_conflict_mean", "srq_sib_ho_rivalry_mean"
  )
}

dmexp_parametrizations <- function() {
  c("i_illness_life_ratio", "ii_dm_yili_yas_kovaryat", "iii_taniyasi_x_yas")
}

dmexp_focal_term <- function(param) {
  switch(param,
    i_illness_life_ratio = "illness_life_ratio",
    ii_dm_yili_yas_kovaryat = "dm_yili",
    iii_taniyasi_x_yas = "tani_yasi_c:cocuk_yas_c",
    stop(sprintf("Bilinmeyen parametrizasyon: %s", param), call. = FALSE)
  )
}

dmexp_formula <- function(param, outcome_col) {
  rhs <- switch(param,
    i_illness_life_ratio = "illness_life_ratio + anne_yas_z + ses_latent_z",
    ii_dm_yili_yas_kovaryat = "dm_yili + cocuk_yas_z + anne_yas_z + ses_latent_z",
    iii_taniyasi_x_yas = "tani_yasi_c * cocuk_yas_c + anne_yas_z + ses_latent_z",
    stop(sprintf("Bilinmeyen parametrizasyon: %s", param), call. = FALSE)
  )
  stats::as.formula(sprintf("%s ~ %s", outcome_col, rhs))
}

# Yardimcilar -------------------------------------------------------------

dmexp_numeric <- function(x) suppressWarnings(as.numeric(x))

dmexp_scale <- function(x) {
  x <- dmexp_numeric(x)
  ok <- !is.na(x)
  out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) return(out)
  s <- stats::sd(x[ok])
  if (is.na(s) || s == 0) return(out)
  out[ok] <- (x[ok] - mean(x[ok])) / s
  out
}

dmexp_center <- function(x) {
  x <- dmexp_numeric(x)
  ok <- !is.na(x)
  out <- rep(NA_real_, length(x))
  if (!any(ok)) return(out)
  out[ok] <- x[ok] - mean(x[ok])
  out
}

# Mantiksal tutarlilik maskesi: dm_yili > cocuk_yas (oran>1) veya oran<=0 olan
# satirlar MANTIKSAL IMKANSIZ kayittir (§110.1 gecerlilik denetimi). Bu satirlar
# §110 modellerinden DISLANIR; ayni kural yan-analiz (§110 psikolojik-kontrol)
# ve §111 betimsel eskiz icin de uygulanir (dm_yili turevleri kirlenmis olur).
dmexp_consistent_rows <- function(df) {
  !(!is.na(df$illness_life_ratio) &
    (df$illness_life_ratio <= 0 | df$illness_life_ratio > 1))
}

dmexp_require_columns <- function(df, columns, context) {
  missing <- setdiff(columns, names(df))
  if (length(missing) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

# Fisher-z tabanli korelasyon %95 GA (cor.test fallback icin)
dmexp_cor_ci <- function(r, n, conf = 0.95) {
  if (is.na(r) || is.na(n) || n < 4L) {
    return(c(lower = NA_real_, upper = NA_real_))
  }
  z <- atanh(r)
  se <- 1 / sqrt(n - 3)
  crit <- stats::qnorm(1 - (1 - conf) / 2)
  c(lower = tanh(z - crit * se), upper = tanh(z + crit * se))
}

# t-degeri → kismi r + %95 GA (effectsize varsa; yoksa manuel Fisher-z)
dmexp_t_to_r <- function(t_value, df_error, conf = 0.95) {
  if (is.na(t_value) || is.na(df_error) || df_error < 1L) {
    return(data.frame(r = NA_real_, ci_lower = NA_real_, ci_upper = NA_real_,
      stringsAsFactors = FALSE))
  }
  if (requireNamespace("effectsize", quietly = TRUE)) {
    tr <- tryCatch(
      as.data.frame(effectsize::t_to_r(t = t_value, df_error = df_error, ci = conf)),
      error = function(e) NULL
    )
    if (!is.null(tr) && all(c("r", "CI_low", "CI_high") %in% names(tr))) {
      return(data.frame(r = tr$r[1L], ci_lower = tr$CI_low[1L], ci_upper = tr$CI_high[1L],
        stringsAsFactors = FALSE))
    }
  }
  r <- t_value / sqrt(t_value^2 + df_error)
  z <- atanh(r)
  se <- 1 / sqrt(df_error - 1)
  crit <- stats::qnorm(1 - (1 - conf) / 2)
  data.frame(r = r, ci_lower = tanh(z - crit * se), ci_upper = tanh(z + crit * se),
    stringsAsFactors = FALSE)
}

# =========================================================================
# Frame hazirlama — DM-only
# =========================================================================

dmexp_prepare_frame <- function(df_family_scored) {
  dmexp_require_columns(df_family_scored,
    c("group_f", "dm_yili", "cocuk_yas", "kardes_yas"),
    "DM maruziyet frame")

  df <- df_family_scored[df_family_scored$group_f == "DM", , drop = FALSE]

  df$dm_yili_num  <- dmexp_numeric(df$dm_yili)
  df$cocuk_yas_num <- dmexp_numeric(df$cocuk_yas)
  df$kardes_yas_num <- dmexp_numeric(df$kardes_yas)

  # §110 — yasam-orani maruziyet (DOGRULANMAMIS metrik)
  df$illness_life_ratio <- ifelse(
    is.na(df$dm_yili_num) | is.na(df$cocuk_yas_num) | df$cocuk_yas_num == 0,
    NA_real_,
    df$dm_yili_num / df$cocuk_yas_num
  )

  # tani yasi = guncel yas - dm suresi (prepare_family verirse onu koru)
  if ("tani_yasi" %in% names(df)) {
    df$tani_yasi <- dmexp_numeric(df$tani_yasi)
  } else {
    df$tani_yasi <- df$cocuk_yas_num - df$dm_yili_num
  }

  # §111 — kardes tani-ani yasi = kardes_yas - dm_yili
  df$kardes_tani_ani_yas <- df$kardes_yas_num - df$dm_yili_num

  # Kovaryatlar / merkezlemeler
  df$cocuk_yas_z <- dmexp_scale(df$cocuk_yas_num)
  df$cocuk_yas_c <- dmexp_center(df$cocuk_yas_num)
  df$tani_yasi_c <- dmexp_center(df$tani_yasi)
  df$anne_yas_z <- if ("anne_yas" %in% names(df)) dmexp_scale(df$anne_yas) else rep(NA_real_, nrow(df))
  df$ses_latent_z <- if ("ses_latent" %in% names(df)) dmexp_scale(df$ses_latent) else rep(NA_real_, nrow(df))

  # Psikolojik-kontrol proxy (Prikken): reddetme + karsilastirma (z-ortalama)
  pc_cols <- dmexp_psychcontrol_components()
  if (all(pc_cols %in% names(df))) {
    z1 <- dmexp_scale(df[[pc_cols[1L]]])
    z2 <- dmexp_scale(df[[pc_cols[2L]]])
    pc <- rowMeans(cbind(z1, z2), na.rm = TRUE)
    pc[is.nan(pc)] <- NA_real_
    df$psychcontrol_proxy_z <- pc
  } else {
    df$psychcontrol_proxy_z <- rep(NA_real_, nrow(df))
  }

  df
}

# =========================================================================
# §110.1 — illness_life_ratio gecerlilik/aralik denetimi
# =========================================================================

dmexp_describe_one <- function(x, degisken, lower = NA_real_, upper = NA_real_,
                               uyari = NA_character_) {
  x <- dmexp_numeric(x)
  obs <- x[!is.na(x)]
  n_below <- if (!is.na(lower)) sum(obs < lower) else 0L
  n_above <- if (!is.na(upper)) sum(obs > upper) else 0L
  data.frame(
    degisken = degisken,
    n = length(x),
    n_gecerli = length(obs),
    n_eksik = sum(is.na(x)),
    ortalama = if (length(obs) > 0L) mean(obs) else NA_real_,
    medyan = if (length(obs) > 0L) stats::median(obs) else NA_real_,
    sd = if (length(obs) > 1L) stats::sd(obs) else NA_real_,
    min = if (length(obs) > 0L) min(obs) else NA_real_,
    max = if (length(obs) > 0L) max(obs) else NA_real_,
    gecerli_alt = lower,
    gecerli_ust = upper,
    n_alt_disi = n_below,
    n_ust_disi = n_above,
    n_aralik_disi = n_below + n_above,
    uyari = uyari,
    statu = dmexp_status_label(),
    stringsAsFactors = FALSE
  )
}

dmexp_life_ratio_validity <- function(df) {
  ratio_uyari <- paste0(
    "DOGRULANMAMIS metrik (proportion-of-life; literaturde valide edilmis ",
    "pediatrik karsiligi yok) → duyarlilik analizi, kanonik alternatiflerle yan yana. ",
    "Oran>1 mantiksal olarak imkansiz (dm_yili>cocuk_yas)."
  )
  do.call(rbind, list(
    dmexp_describe_one(df$illness_life_ratio, "illness_life_ratio", 0, 1, ratio_uyari),
    dmexp_describe_one(df$dm_yili_num, "dm_yili", 0, NA_real_,
      "DM suresi (yil); >=0 beklenir."),
    dmexp_describe_one(df$cocuk_yas_num, "cocuk_yas", 0, NA_real_, NA_character_),
    dmexp_describe_one(df$tani_yasi, "tani_yasi (cocuk_yas - dm_yili)", 0, NA_real_,
      "Negatif deger tutarsizlik isaretidir."),
    dmexp_describe_one(df$kardes_tani_ani_yas, "kardes_tani_ani_yas (kardes_yas - dm_yili)",
      NA_real_, NA_real_, "Negatif = tanidan sonra dogan kardes (§111 ayri kategori).")
  ))
}

# =========================================================================
# §110 — Uc parametrizasyon (ortak analitik ornekleme AIC-karsilastirilabilir)
# =========================================================================

# AIC karsilastirmasinin gecerli olmasi icin uc model AYNI satirlarda fit edilir.
# Analitik ornek = DM satirlari; outcome + tum model degiskenleri non-NA;
# illness_life_ratio gecerli aralikta (0 < ratio <= 1).
dmexp_analytic_subset <- function(df, outcome_col) {
  needed <- c(outcome_col, "illness_life_ratio", "dm_yili_num", "cocuk_yas_z",
    "cocuk_yas_c", "tani_yasi_c", "anne_yas_z", "ses_latent_z")
  dmexp_require_columns(df, needed, "analitik ornek")
  keep <- stats::complete.cases(df[, needed, drop = FALSE])
  valid_ratio <- !is.na(df$illness_life_ratio) &
    df$illness_life_ratio > 0 & df$illness_life_ratio <= 1
  df[keep & valid_ratio, , drop = FALSE]
}

dmexp_focal_row <- function(fit, param, outcome_col, sub_df) {
  focal <- dmexp_focal_term(param)
  sm <- summary(fit)
  cs <- sm$coefficients
  if (!focal %in% rownames(cs)) {
    return(data.frame(
      outcome = outcome_col, parametrizasyon = param, focal_term = focal,
      estimate = NA_real_, se = NA_real_, ci_lower = NA_real_, ci_upper = NA_real_,
      t_value = NA_real_, p_value = NA_real_,
      r_partial = NA_real_, r_ci_lower = NA_real_, r_ci_upper = NA_real_,
      aic = stats::AIC(fit), n = stats::nobs(fit),
      outcome_ort = mean(sub_df[[outcome_col]], na.rm = TRUE),
      outcome_medyan = stats::median(sub_df[[outcome_col]], na.rm = TRUE),
      status = "focal_term_yok", statu = dmexp_status_label(),
      stringsAsFactors = FALSE
    ))
  }
  est <- cs[focal, "Estimate"]
  se <- cs[focal, "Std. Error"]
  tval <- cs[focal, "t value"]
  pval <- cs[focal, "Pr(>|t|)"]
  ci <- tryCatch(stats::confint(fit, parm = focal, level = 0.95),
    error = function(e) matrix(c(NA_real_, NA_real_), nrow = 1L))
  rp <- dmexp_t_to_r(tval, df_error = fit$df.residual)
  data.frame(
    outcome = outcome_col, parametrizasyon = param, focal_term = focal,
    estimate = unname(est), se = unname(se),
    ci_lower = unname(ci[1L, 1L]), ci_upper = unname(ci[1L, 2L]),
    t_value = unname(tval), p_value = unname(pval),
    r_partial = rp$r[1L], r_ci_lower = rp$ci_lower[1L], r_ci_upper = rp$ci_upper[1L],
    aic = stats::AIC(fit), n = stats::nobs(fit),
    outcome_ort = mean(sub_df[[outcome_col]], na.rm = TRUE),
    outcome_medyan = stats::median(sub_df[[outcome_col]], na.rm = TRUE),
    status = "ok", statu = dmexp_status_label(),
    stringsAsFactors = FALSE
  )
}

dmexp_full_coef_rows <- function(fit, param, outcome_col) {
  sm <- summary(fit)
  cs <- as.data.frame(sm$coefficients)
  cs$term <- rownames(cs)
  rownames(cs) <- NULL
  names(cs) <- c("estimate", "se", "t_value", "p_value", "term")
  ci <- tryCatch(as.data.frame(stats::confint(fit, level = 0.95)),
    error = function(e) NULL)
  if (!is.null(ci)) {
    ci$term <- rownames(ci)
    rownames(ci) <- NULL
    names(ci) <- c("ci_lower", "ci_upper", "term")
    cs <- merge(cs, ci, by = "term", all.x = TRUE, sort = FALSE)
  } else {
    cs$ci_lower <- NA_real_
    cs$ci_upper <- NA_real_
  }
  cs$outcome <- outcome_col
  cs$parametrizasyon <- param
  cs$n <- stats::nobs(fit)
  cs$r_squared <- sm$r.squared
  cs$aic <- stats::AIC(fit)
  cs$statu <- dmexp_status_label()
  cs[, c("outcome", "parametrizasyon", "term", "estimate", "se",
    "ci_lower", "ci_upper", "t_value", "p_value", "n", "r_squared", "aic", "statu")]
}

dmexp_overprotection_models <- function(df, outcomes = dmexp_overprotection_outcomes()) {
  focal_rows <- list()
  coef_rows <- list()
  for (oc in outcomes) {
    if (!oc %in% names(df)) {
      focal_rows[[oc]] <- data.frame(
        outcome = oc, parametrizasyon = NA_character_, focal_term = NA_character_,
        estimate = NA_real_, se = NA_real_, ci_lower = NA_real_, ci_upper = NA_real_,
        t_value = NA_real_, p_value = NA_real_,
        r_partial = NA_real_, r_ci_lower = NA_real_, r_ci_upper = NA_real_,
        aic = NA_real_, n = 0L, outcome_ort = NA_real_, outcome_medyan = NA_real_,
        status = "outcome_kolonu_yok", statu = dmexp_status_label(),
        stringsAsFactors = FALSE
      )
      next
    }
    sub_df <- dmexp_analytic_subset(df, oc)
    if (nrow(sub_df) < 20L) {
      focal_rows[[oc]] <- data.frame(
        outcome = oc, parametrizasyon = NA_character_, focal_term = NA_character_,
        estimate = NA_real_, se = NA_real_, ci_lower = NA_real_, ci_upper = NA_real_,
        t_value = NA_real_, p_value = NA_real_,
        r_partial = NA_real_, r_ci_lower = NA_real_, r_ci_upper = NA_real_,
        aic = NA_real_, n = nrow(sub_df),
        outcome_ort = mean(sub_df[[oc]], na.rm = TRUE),
        outcome_medyan = stats::median(sub_df[[oc]], na.rm = TRUE),
        status = "yetersiz_n", statu = dmexp_status_label(),
        stringsAsFactors = FALSE
      )
      next
    }
    aic_by_param <- setNames(rep(NA_real_, length(dmexp_parametrizations())),
      dmexp_parametrizations())
    per_outcome_focal <- list()
    for (param in dmexp_parametrizations()) {
      fit <- tryCatch(stats::lm(dmexp_formula(param, oc), data = sub_df),
        error = function(e) e)
      if (inherits(fit, "error")) {
        per_outcome_focal[[param]] <- data.frame(
          outcome = oc, parametrizasyon = param, focal_term = dmexp_focal_term(param),
          estimate = NA_real_, se = NA_real_, ci_lower = NA_real_, ci_upper = NA_real_,
          t_value = NA_real_, p_value = NA_real_,
          r_partial = NA_real_, r_ci_lower = NA_real_, r_ci_upper = NA_real_,
          aic = NA_real_, n = nrow(sub_df),
          outcome_ort = mean(sub_df[[oc]], na.rm = TRUE),
          outcome_medyan = stats::median(sub_df[[oc]], na.rm = TRUE),
          status = paste0("fit_error:", conditionMessage(fit)),
          statu = dmexp_status_label(),
          stringsAsFactors = FALSE
        )
        next
      }
      fr <- dmexp_focal_row(fit, param, oc, sub_df)
      aic_by_param[param] <- fr$aic[1L]
      per_outcome_focal[[param]] <- fr
      coef_rows[[paste(oc, param, sep = "__")]] <- dmexp_full_coef_rows(fit, param, oc)
    }
    of <- do.call(rbind, per_outcome_focal)
    min_aic <- suppressWarnings(min(of$aic, na.rm = TRUE))
    of$delta_aic <- if (is.finite(min_aic)) of$aic - min_aic else NA_real_
    focal_rows[[oc]] <- of
  }
  focal <- do.call(rbind, focal_rows)
  if (!"delta_aic" %in% names(focal)) focal$delta_aic <- NA_real_

  # Holm — KISIM XL ici focal maruziyet testleri ailesi
  focal$p_holm <- NA_real_
  ok_idx <- which(!is.na(focal$p_value))
  if (length(ok_idx) > 0L) {
    focal$p_holm[ok_idx] <- stats::p.adjust(focal$p_value[ok_idx], method = "holm")
  }

  coef_table <- if (length(coef_rows) > 0L) do.call(rbind, coef_rows) else NULL
  list(
    exposure_parametrizations = focal,
    overprotection_models = coef_table
  )
}

# =========================================================================
# §110 yan-analiz — Psikolojik-kontrol proxy (Prikken duzeltmesi)
# =========================================================================

dmexp_cor_tost_row <- function(x, y, exposure_label, sesoi_r = 0.10) {
  ok <- !is.na(x) & !is.na(y)
  x <- x[ok]; y <- y[ok]; n <- length(x)
  if (n < 10L) {
    return(data.frame(
      exposure = exposure_label, n = n, r = NA_real_,
      ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
      sesoi_r = sesoi_r, tost_p = NA_real_, tost_karar = "yetersiz_n",
      statu = dmexp_status_label(), stringsAsFactors = FALSE
    ))
  }
  ct <- suppressWarnings(stats::cor.test(x, y))
  r <- unname(ct$estimate)
  ci <- ct$conf.int
  ci_lo <- if (!is.null(ci)) ci[1L] else dmexp_cor_ci(r, n)["lower"]
  ci_hi <- if (!is.null(ci)) ci[2L] else dmexp_cor_ci(r, n)["upper"]

  tost_p <- NA_real_
  if (requireNamespace("TOSTER", quietly = TRUE)) {
    tt <- tryCatch(
      suppressWarnings(suppressMessages(
        TOSTER::z_cor_test(x, y, alternative = "equivalence", null = sesoi_r)
      )),
      error = function(e) NULL
    )
    if (!is.null(tt)) tost_p <- unname(tt$p.value)
  }
  if (is.na(tost_p)) {
    # Fisher-z manuel TOST fallback
    z <- atanh(r); se <- 1 / sqrt(n - 3)
    zl <- atanh(-sesoi_r); zu <- atanh(sesoi_r)
    p1 <- stats::pnorm((z - zl) / se, lower.tail = FALSE)
    p2 <- stats::pnorm((z - zu) / se, lower.tail = TRUE)
    tost_p <- max(p1, p2)
  }
  nhst_p <- unname(ct$p.value)
  karar <- if (!is.na(tost_p) && tost_p < 0.05 && !is.na(nhst_p) && nhst_p < 0.05) {
    "Onemsiz (trivial)"
  } else if (!is.na(tost_p) && tost_p < 0.05) {
    "Esdeger (|r|<.10)"
  } else if (!is.na(nhst_p) && nhst_p < 0.05) {
    "Anlamli (esdeger degil)"
  } else {
    "Belirsiz"
  }
  data.frame(
    exposure = exposure_label, n = n, r = r,
    ci_lower = unname(ci_lo), ci_upper = unname(ci_hi), p_value = nhst_p,
    sesoi_r = sesoi_r, tost_p = tost_p, tost_karar = karar,
    statu = dmexp_status_label(), stringsAsFactors = FALSE
  )
}

dmexp_psychcontrol_sideanalysis <- function(df, sesoi_r = 0.10) {
  consistent <- dmexp_consistent_rows(df)
  n_dislanan <- sum(!consistent)
  df <- df[consistent, , drop = FALSE]
  note <- paste0(
    "Prikken et al. (2019): T1DM'de operatif mediyator PSIKOLOJIK KONTROL ",
    "(asiri koruma degil). Proxy = z(embu_c_idx_reddetme_mean) + ",
    "z(embu_c_idx_karsilastirma_mean) ortalamasi. Null iddia icin TOST/SESOI |r|=.10. ",
    sprintf(paste0("Mantiksal-imkansiz kayitlar (dm_yili>cocuk_yas; §110.1) ",
      "§110 modelleriyle ayni kuralla DISLANDI: n_dislanan=%d."), n_dislanan)
  )
  proxy <- df$psychcontrol_proxy_z
  if (all(is.na(proxy))) {
    out <- data.frame(
      exposure = "psychcontrol_proxy_yok", n = 0L, r = NA_real_,
      ci_lower = NA_real_, ci_upper = NA_real_, p_value = NA_real_,
      sesoi_r = sesoi_r, tost_p = NA_real_, tost_karar = "proxy_yok",
      statu = dmexp_status_label(), stringsAsFactors = FALSE
    )
    out$n_dislanan_tutarsiz <- n_dislanan
    out$not <- note
    out$p_holm <- NA_real_
    return(out)
  }
  rows <- list(
    dmexp_cor_tost_row(df$illness_life_ratio, proxy, "illness_life_ratio", sesoi_r),
    dmexp_cor_tost_row(df$dm_yili_num, proxy, "dm_yili", sesoi_r),
    dmexp_cor_tost_row(df$tani_yasi, proxy, "tani_yasi", sesoi_r)
  )
  out <- do.call(rbind, rows)
  out$p_holm <- NA_real_
  ok_idx <- which(!is.na(out$p_value))
  if (length(ok_idx) > 0L) {
    out$p_holm[ok_idx] <- stats::p.adjust(out$p_value[ok_idx], method = "holm")
  }
  out$n_dislanan_tutarsiz <- n_dislanan
  out$not <- note
  out
}

# =========================================================================
# §111 — Kardes tani-penceresi betimsel eskiz (CIKARIMSAL TEST YOK)
# =========================================================================

dmexp_window_band <- function(x) {
  factor(
    cut(dmexp_numeric(x),
      breaks = c(-Inf, 0, 5, 10, Inf),
      labels = c("<0 (tani sonrasi dogdu)", "0-5", "5-10", ">=10"),
      right = FALSE),
    levels = c("<0 (tani sonrasi dogdu)", "0-5", "5-10", ">=10")
  )
}

dmexp_sibling_window_descriptive <- function(df, outcomes = dmexp_sibling_outcomes()) {
  consistent <- dmexp_consistent_rows(df)
  n_dislanan <- sum(!consistent)
  df <- df[consistent, , drop = FALSE]
  note <- paste0(
    "GELECEK-TASARIM SINYALI: yalniz betimsel eskiz; n ve karisiklik nedeniyle ",
    "cikarimsal test ONERILMEZ (§111, Tier C). Kardes gelisim penceresi = ",
    "kardes_yas - dm_yili. ",
    sprintf(paste0("Mantiksal-imkansiz dm_yili kayitlari (dm_yili>cocuk_yas; §110.1) ",
      "kardes_tani_ani_yas'i kirlettiginden DISLANDI: n_dislanan=%d."), n_dislanan)
  )
  band <- dmexp_window_band(df$kardes_tani_ani_yas)
  present_outcomes <- intersect(outcomes, names(df))
  rows <- list()
  if (n_dislanan > 0L) {
    rows[["dislanan"]] <- data.frame(
      band = "DISLANDI (dm_yili>cocuk_yas tutarsiz)", n_band = n_dislanan,
      degisken = NA_character_, n_gecerli = NA_integer_,
      ortalama = NA_real_, medyan = NA_real_, sd = NA_real_,
      not = note, statu = dmexp_status_label(),
      stringsAsFactors = FALSE
    )
  }
  for (lv in levels(band)) {
    idx <- which(band == lv)
    n_band <- length(idx)
    if (length(present_outcomes) == 0L) {
      rows[[lv]] <- data.frame(
        band = lv, n_band = n_band, degisken = NA_character_,
        n_gecerli = NA_integer_, ortalama = NA_real_, medyan = NA_real_,
        sd = NA_real_, not = note, statu = dmexp_status_label(),
        stringsAsFactors = FALSE
      )
      next
    }
    for (oc in present_outcomes) {
      vals <- dmexp_numeric(df[[oc]][idx])
      obs <- vals[!is.na(vals)]
      rows[[paste(lv, oc, sep = "__")]] <- data.frame(
        band = lv, n_band = n_band, degisken = oc,
        n_gecerli = length(obs),
        ortalama = if (length(obs) > 0L) mean(obs) else NA_real_,
        medyan = if (length(obs) > 0L) stats::median(obs) else NA_real_,
        sd = if (length(obs) > 1L) stats::sd(obs) else NA_real_,
        not = note, statu = dmexp_status_label(),
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

# =========================================================================
# Pipeline sarici (Faz II deseni)
# =========================================================================

run_phase3_dm_exposure_pipeline <- function(df_family_scored,
                                            outcomes = dmexp_overprotection_outcomes(),
                                            sibling_outcomes = dmexp_sibling_outcomes(),
                                            sesoi_r = 0.10) {
  df <- dmexp_prepare_frame(df_family_scored)

  validity <- dmexp_life_ratio_validity(df)
  models <- dmexp_overprotection_models(df, outcomes = outcomes)
  psychcontrol <- dmexp_psychcontrol_sideanalysis(df, sesoi_r = sesoi_r)
  sibling <- dmexp_sibling_window_descriptive(df, outcomes = sibling_outcomes)

  target_summary <- data.frame(
    analysis = "phase3_dm_exposure_intensity",
    kisim = "KISIM XL (§110-111)",
    n_dm = nrow(df),
    n_ratio_gecerli = sum(!is.na(df$illness_life_ratio) &
      df$illness_life_ratio > 0 & df$illness_life_ratio <= 1),
    n_ratio_aralik_disi = sum(!is.na(df$illness_life_ratio) &
      (df$illness_life_ratio <= 0 | df$illness_life_ratio > 1)),
    sesoi_r = sesoi_r,
    coklu_karsilastirma = "Holm (KISIM ici)",
    imputation = "YOK (Kural 19)",
    kanit_kategorisi = dmexp_status_label(),
    sapma_tipi = "Tip 3 (Faz III post-hoc, SAP KISIM XL/110-111)",
    metrik_uyari = "illness_life_ratio DOGRULANMAMIS → duyarlilik",
    reference_doc = "06-sap-faz3-ek-plan.md",
    stringsAsFactors = FALSE
  )

  list(
    life_ratio_validity = validity,
    exposure_parametrizations = models$exposure_parametrizations,
    overprotection_models = models$overprotection_models,
    psychcontrol_sideanalysis = psychcontrol,
    sibling_window_descriptive = sibling,
    target_summary = target_summary
  )
}
