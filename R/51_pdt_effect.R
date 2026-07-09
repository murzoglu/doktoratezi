# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXVI (§96-99)
# Diferansiyel Ebeveynlik Etki Modellemesi (Parental Differential Treatment, PDT)
#
# Saf fonksiyon modulu (dosya I/O yok). Runner: scripts/R/52_phase3_pdt_effect_audit.R
#
# §96 — PDT buyuklugu & yonu: aile-duzeyi EMBU-C alt olcek algi-farki
#        (pdt_signed / pdt_abs); fark-skoru guvenilirligi rho_DD;
#        birincil model RSA/polinom (LDS DEGIL); buyukluk yordayici OLS +
#        robust SE; yon isaret testi + Cohen's d.
# §97 — PDT -> kardes iliskisi (SRQ catisma/rekabet) yol modeli, lme4
#        random intercept (1|aile_no_f); ICC; standartlastirilmis katsayi.
# §98 — Dogrudan kayirma (favoritism): anne (14,30,46) vs baba (13,29,45)
#        kanallari; iki-informant ICC(2,1) + Bland-Altman; 3-madde omega/alfa;
#        MTMM yakinsama (SRQ-kayirma <-> EMBU-C PDT).
# §99 — Mesruiyet/baglam moderasyonu: pdt_abs x group_f; emmeans basit egim;
#        etkilesim null ise TOST (SESOI |r|=.10); "adalet maddesi yok" siniri.
#
# Tum ciktilar korelasyonel dildedir; nedensel yorum yasaktir. Her tabloya
# "[KESIFSEL - POST-HOC]" statu kolonu eklenir. Kanonik CSV'ye yazilmaz.

# ============================================================================
# Yardimci fonksiyonlar
# ============================================================================

pdt_status_label <- function() {
  "[KESIFSEL - POST-HOC]"
}

pdt_subscales <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

pdt_favoritism_map <- function() {
  # SRQ kayirma maddeleri (R/10 srq_first_order_map ile birebir)
  list(
    mat = c(14, 30, 46),  # anne kayirma (maternal partiality)
    pat = c(13, 29, 45)   # baba kayirma (paternal partiality)
  )
}

pdt_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context,
      paste(missing_columns, collapse = ", ")), call. = FALSE)
  }
  invisible(TRUE)
}

pdt_scale <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) {
    return(rep(NA_real_, length(x)))
  }
  (x - m) / s
}

pdt_embu_item_columns <- function(prefix, items) {
  paste0(prefix, "_q", sprintf("%02d", items))
}

pdt_srq_item_columns <- function(prefix, items) {
  paste0(prefix, "_", items)
}

pdt_subscale_items <- function(subscale) {
  # EMBU alt olcek madde eslemesi (R/10 embu_subscale_map)
  if (exists("embu_subscale_map", mode = "function")) {
    return(embu_subscale_map()[[subscale]])
  }
  map <- list(
    sicaklik = c(1, 3, 6, 7, 13, 17, 20, 24, 26),
    asiri_koruma = c(4, 8, 14, 15, 19, 23, 25),
    reddetme = c(5, 9, 10, 12, 16, 21, 22, 28),
    karsilastirma = c(2, 11, 18, 27, 29)
  )
  map[[subscale]]
}

# Cronbach alfa (madde-duzeyinden, elle -- deterministik)
pdt_cronbach_alpha <- function(item_matrix) {
  m <- item_matrix[stats::complete.cases(item_matrix), , drop = FALSE]
  k <- ncol(m)
  if (k < 2L || nrow(m) < 3L) {
    return(NA_real_)
  }
  item_var <- apply(m, 2L, stats::var)
  total_var <- stats::var(rowSums(m))
  if (is.na(total_var) || total_var <= 0) {
    return(NA_real_)
  }
  (k / (k - 1)) * (1 - sum(item_var) / total_var)
}

# McDonald omega_total (tek-faktor loadinglerinden, elle -- 3 madde icin saglam)
pdt_omega_total <- function(item_matrix) {
  m <- item_matrix[stats::complete.cases(item_matrix), , drop = FALSE]
  if (ncol(m) < 3L || nrow(m) < 10L) {
    return(NA_real_)
  }
  if (!requireNamespace("psych", quietly = TRUE)) {
    return(NA_real_)
  }
  fa1 <- tryCatch(
    suppressWarnings(suppressMessages(psych::fa(m, nfactors = 1L, fm = "minres"))),
    error = function(e) NULL
  )
  if (is.null(fa1)) {
    return(NA_real_)
  }
  lambda <- as.numeric(fa1$loadings[, 1L])
  if (any(!is.finite(lambda))) {
    return(NA_real_)
  }
  num <- sum(lambda)^2
  den <- num + sum(1 - lambda^2)
  if (den <= 0) {
    return(NA_real_)
  }
  num / den
}

pdt_tag <- function(df) {
  if (is.null(df) || nrow(df) == 0L) {
    return(df)
  }
  df$statu <- pdt_status_label()
  df
}

`%|NA|%` <- function(a, b) if (is.null(a) || length(a) == 0L) b else a

# ============================================================================
# §96 — PDT buyuklugu, yonu, guvenilirligi
# ============================================================================

# Aile duzeyinde her EMBU-C alt olcegi icin pdt_signed = idx - sib, pdt_abs = |.|
pdt_add_signed_abs <- function(df_family, subscales = pdt_subscales()) {
  out <- df_family
  for (sub in subscales) {
    idx_col <- paste0("embu_c_idx_", sub, "_mean")
    sib_col <- paste0("embu_c_sib_", sub, "_mean")
    pdt_require_columns(out, c(idx_col, sib_col),
      sprintf("PDT signed/abs (%s)", sub))
    signed <- suppressWarnings(as.numeric(out[[idx_col]]) - as.numeric(out[[sib_col]]))
    out[[paste0("pdt_signed_", sub)]] <- signed
    out[[paste0("pdt_abs_", sub)]] <- abs(signed)
  }
  out
}

# Fark-skoru guvenilirligi rho_DD (Rogosa-Willett 1983; Overall-Woodward 1975)
pdt_rho_dd_table <- function(df_family, subscales = pdt_subscales()) {
  rows <- list()
  for (sub in subscales) {
    items <- pdt_subscale_items(sub)
    idx_items <- pdt_embu_item_columns("embu_c_idx", items)
    sib_items <- pdt_embu_item_columns("embu_c_sib", items)
    idx_mean_col <- paste0("embu_c_idx_", sub, "_mean")
    sib_mean_col <- paste0("embu_c_sib_", sub, "_mean")
    signed_col <- paste0("pdt_signed_", sub)
    abs_col <- paste0("pdt_abs_", sub)

    have_items <- all(c(idx_items, sib_items) %in% names(df_family))
    rho_xx <- if (have_items) {
      pdt_cronbach_alpha(as.data.frame(lapply(df_family[idx_items], as.numeric)))
    } else {
      NA_real_
    }
    rho_yy <- if (have_items) {
      pdt_cronbach_alpha(as.data.frame(lapply(df_family[sib_items], as.numeric)))
    } else {
      NA_real_
    }

    x <- suppressWarnings(as.numeric(df_family[[idx_mean_col]]))
    y <- suppressWarnings(as.numeric(df_family[[sib_mean_col]]))
    ok <- !is.na(x) & !is.na(y)
    n_pair <- sum(ok)
    sigma_x <- stats::sd(x[ok])
    sigma_y <- stats::sd(y[ok])
    rho_xy <- if (n_pair >= 3L) suppressWarnings(stats::cor(x[ok], y[ok])) else NA_real_

    num <- sigma_x^2 * rho_xx + sigma_y^2 * rho_yy - 2 * rho_xy * sigma_x * sigma_y
    den <- sigma_x^2 + sigma_y^2 - 2 * rho_xy * sigma_x * sigma_y
    rho_dd <- if (!is.na(den) && den > 0) num / den else NA_real_

    signed <- if (signed_col %in% names(df_family)) {
      suppressWarnings(as.numeric(df_family[[signed_col]]))
    } else {
      x - y
    }
    absv <- if (abs_col %in% names(df_family)) {
      suppressWarnings(as.numeric(df_family[[abs_col]]))
    } else {
      abs(x - y)
    }

    rows[[sub]] <- data.frame(
      alt_olcek = sub,
      n_cift = n_pair,
      sigma_x = sigma_x,
      sigma_y = sigma_y,
      rho_xx_alfa_idx = rho_xx,
      rho_yy_alfa_sib = rho_yy,
      rho_xy = rho_xy,
      rho_dd = rho_dd,
      pdt_signed_ort = mean(signed, na.rm = TRUE),
      pdt_signed_medyan = stats::median(signed, na.rm = TRUE),
      pdt_abs_ort = mean(absv, na.rm = TRUE),
      pdt_abs_medyan = stats::median(absv, na.rm = TRUE),
      rho_dd_not = "dusuk rho_dd -> ham fark yalniz betimsel (Trafimow 2015 nuansi)",
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# RSA/polinom yuzey parametreleri a1-a4 + bootstrap %95 GA (elle lm + boot)
pdt_rsa_poly_a <- function(xc, yc, z) {
  fit <- stats::lm(z ~ xc + yc + I(xc^2) + I(xc * yc) + I(yc^2))
  b <- stats::coef(fit)
  # sira: (Intercept), xc, yc, xc^2, xc*yc, yc^2
  b1 <- b[[2L]]; b2 <- b[[3L]]; b3 <- b[[4L]]; b4 <- b[[5L]]; b5 <- b[[6L]]
  c(
    a1 = b1 + b2,          # X=Y hatti egimi
    a2 = b3 + b4 + b5,     # X=Y hatti egriligi
    a3 = b1 - b2,          # X=-Y hatti egimi (yanlilik/fark)
    a4 = b3 - b4 + b5      # X=-Y hatti egriligi
  )
}

pdt_rsa_one <- function(df, xcol, ycol, zcol, n_boot = 1000L) {
  d <- df[, c(xcol, ycol, zcol)]
  d <- d[stats::complete.cases(d), , drop = FALSE]
  n <- nrow(d)
  param_names <- c("a1", "a2", "a3", "a4")
  if (n < 20L) {
    return(data.frame(
      outcome = zcol, parametre = param_names, tahmin = NA_real_,
      alt_ga = NA_real_, ust_ga = NA_real_, n = n,
      blok_F = NA_real_, blok_p = NA_real_, durum = "yetersiz_n",
      stringsAsFactors = FALSE
    ))
  }
  grand <- mean(c(d[[xcol]], d[[ycol]]))
  xc <- d[[xcol]] - grand
  yc <- d[[ycol]] - grand
  z <- d[[zcol]]

  a_hat <- pdt_rsa_poly_a(xc, yc, z)

  full <- stats::lm(z ~ xc + yc + I(xc^2) + I(xc * yc) + I(yc^2))
  lin <- stats::lm(z ~ xc + yc)
  an <- stats::anova(lin, full)
  blok_F <- an$F[2L]
  blok_p <- an$`Pr(>F)`[2L]

  boot_mat <- matrix(NA_real_, nrow = n_boot, ncol = 4L)
  for (bi in seq_len(n_boot)) {
    ii <- sample.int(n, n, replace = TRUE)
    boot_mat[bi, ] <- tryCatch(
      pdt_rsa_poly_a(xc[ii], yc[ii], z[ii]),
      error = function(e) rep(NA_real_, 4L)
    )
  }
  ci <- apply(boot_mat, 2L, stats::quantile, probs = c(0.025, 0.975), na.rm = TRUE)

  data.frame(
    outcome = zcol,
    parametre = param_names,
    tahmin = as.numeric(a_hat),
    alt_ga = as.numeric(ci[1L, ]),
    ust_ga = as.numeric(ci[2L, ]),
    n = n,
    blok_F = blok_F,
    blok_p = blok_p,
    durum = "ok",
    stringsAsFactors = FALSE
  )
}

pdt_rsa_surface_table <- function(df_family, subscales = pdt_subscales(),
                                  outcomes = c("srq_ho_conflict_mean", "srq_ho_rivalry_mean"),
                                  n_boot = 1000L) {
  rows <- list()
  for (sub in subscales) {
    xcol <- paste0("embu_c_idx_", sub, "_mean")
    ycol <- paste0("embu_c_sib_", sub, "_mean")
    if (!all(c(xcol, ycol) %in% names(df_family))) next
    for (oc in outcomes) {
      if (!oc %in% names(df_family)) next
      res <- pdt_rsa_one(df_family, xcol, ycol, oc, n_boot = n_boot)
      res$alt_olcek <- sub
      rows[[paste(sub, oc, sep = "_")]] <- res
    }
  }
  if (length(rows) == 0L) {
    return(data.frame(
      alt_olcek = character(), outcome = character(), parametre = character(),
      tahmin = numeric(), alt_ga = numeric(), ust_ga = numeric(),
      n = integer(), blok_F = numeric(), blok_p = numeric(), durum = character(),
      stringsAsFactors = FALSE
    ))
  }
  out <- do.call(rbind, rows)
  out[, c("alt_olcek", "outcome", "parametre", "tahmin", "alt_ga", "ust_ga",
          "n", "blok_F", "blok_p", "durum")]
}

# Buyukluk yordayici modeli: pdt_abs ~ group + ses + age_gap + same_sex + cocuk_sayisi
pdt_magnitude_model <- function(df_family, subscales = pdt_subscales()) {
  covars <- c("group_f", "ses_latent_z", "age_gap_z", "same_sex", "cocuk_sayisi_z")
  d0 <- df_family
  if (!"ses_latent_z" %in% names(d0)) d0$ses_latent_z <- pdt_scale(d0$ses_latent)
  if (!"age_gap_z" %in% names(d0)) d0$age_gap_z <- pdt_scale(d0$age_gap)
  if (!"cocuk_sayisi_z" %in% names(d0)) d0$cocuk_sayisi_z <- pdt_scale(d0$cocuk_sayisi)

  rows <- list()
  group_p <- stats::setNames(rep(NA_real_, length(subscales)), subscales)
  for (sub in subscales) {
    abs_col <- paste0("pdt_abs_", sub)
    if (!abs_col %in% names(d0)) next
    d0$.y <- suppressWarnings(as.numeric(d0[[abs_col]]))
    fmla <- stats::as.formula(
      ".y ~ group_f + ses_latent_z + age_gap_z + same_sex + cocuk_sayisi_z"
    )
    fit <- tryCatch(stats::lm(fmla, data = d0), error = function(e) e)
    if (inherits(fit, "error")) {
      rows[[sub]] <- data.frame(
        alt_olcek = sub, terim = NA_character_, tahmin = NA_real_,
        robust_se = NA_real_, t = NA_real_, p = NA_real_,
        alt_ga = NA_real_, ust_ga = NA_real_, n = NA_integer_,
        durum = paste0("hata:", conditionMessage(fit)),
        stringsAsFactors = FALSE
      )
      next
    }
    V <- tryCatch(sandwich::vcovHC(fit, type = "HC3"), error = function(e) NULL)
    ct <- if (!is.null(V)) {
      lmtest::coeftest(fit, vcov. = V)
    } else {
      stats::coef(summary(fit))
    }
    ct <- as.matrix(ct)
    dfres <- stats::df.residual(fit)
    tcrit <- stats::qt(0.975, dfres)
    est <- ct[, 1L]; se <- ct[, 2L]; tval <- ct[, 3L]; pval <- ct[, 4L]
    terms <- rownames(ct)
    rows[[sub]] <- data.frame(
      alt_olcek = sub,
      terim = terms,
      tahmin = as.numeric(est),
      robust_se = as.numeric(se),
      t = as.numeric(tval),
      p = as.numeric(pval),
      alt_ga = as.numeric(est - tcrit * se),
      ust_ga = as.numeric(est + tcrit * se),
      n = stats::nobs(fit),
      durum = "ok",
      stringsAsFactors = FALSE
    )
    if ("group_fDM" %in% terms) {
      group_p[[sub]] <- as.numeric(pval[["group_fDM"]])
    }
  }
  out <- if (length(rows) > 0L) do.call(rbind, rows) else data.frame()
  attr(out, "group_p") <- group_p
  out
}

# Yon analizi: DM grubunda isaretli Delta isaret testi + Cohen's d + %95 GA
pdt_direction_test <- function(df_family, subscales = pdt_subscales(),
                               group_col = "group_f", group_value = "DM") {
  rows <- list()
  sign_p <- stats::setNames(rep(NA_real_, length(subscales)), subscales)
  grp <- as.character(df_family[[group_col]])
  in_group <- grp == group_value
  for (sub in subscales) {
    signed_col <- paste0("pdt_signed_", sub)
    if (!signed_col %in% names(df_family)) next
    v <- suppressWarnings(as.numeric(df_family[[signed_col]]))[in_group]
    v <- v[!is.na(v)]
    n <- length(v)
    n_pos <- sum(v > 0)
    n_neg <- sum(v < 0)
    n_nonzero <- n_pos + n_neg

    sp <- if (n_nonzero >= 1L) {
      tryCatch(stats::binom.test(n_pos, n_nonzero, p = 0.5)$p.value,
        error = function(e) NA_real_)
    } else {
      NA_real_
    }
    sign_p[[sub]] <- sp

    d_est <- NA_real_; d_lo <- NA_real_; d_hi <- NA_real_
    if (n >= 3L && stats::sd(v) > 0) {
      dd <- tryCatch(
        suppressWarnings(effectsize::cohens_d(v, mu = 0, ci = 0.95)),
        error = function(e) NULL
      )
      if (!is.null(dd)) {
        d_est <- as.numeric(dd$Cohens_d[1L])
        d_lo <- as.numeric(dd$CI_low[1L])
        d_hi <- as.numeric(dd$CI_high[1L])
      } else {
        d_est <- mean(v) / stats::sd(v)
        se_d <- sqrt(1 / n + d_est^2 / (2 * n))
        d_lo <- d_est - 1.96 * se_d
        d_hi <- d_est + 1.96 * se_d
      }
    }

    rows[[sub]] <- data.frame(
      alt_olcek = sub,
      grup = group_value,
      n = n,
      n_pozitif = n_pos,
      n_negatif = n_neg,
      pdt_signed_ort = mean(v, na.rm = TRUE),
      pdt_signed_medyan = stats::median(v, na.rm = TRUE),
      isaret_testi_p = sp,
      cohens_d = d_est,
      d_alt_ga = d_lo,
      d_ust_ga = d_hi,
      yon = ifelse(is.na(mean(v)), NA_character_,
        ifelse(mean(v) > 0, "indeks_daha_yuksek", "kardes_daha_yuksek")),
      stringsAsFactors = FALSE
    )
  }
  out <- if (length(rows) > 0L) do.call(rbind, rows) else data.frame()
  attr(out, "sign_p") <- sign_p
  out
}

# ============================================================================
# §97 — PDT -> kardes iliskisi yol modeli (lme4 random intercept)
# ============================================================================

pdt_build_long_frame <- function(df_family, df_long, subscales = pdt_subscales()) {
  d0 <- df_family
  if (!"ses_latent_z" %in% names(d0)) d0$ses_latent_z <- pdt_scale(d0$ses_latent)
  if (!"age_gap_z" %in% names(d0)) d0$age_gap_z <- pdt_scale(d0$age_gap)

  keep <- c("aile_no", "ses_latent_z", "age_gap_z", "same_sex")
  for (sub in subscales) {
    abs_col <- paste0("pdt_abs_", sub)
    z_col <- paste0("pdt_abs_", sub, "_z")
    d0[[z_col]] <- pdt_scale(d0[[abs_col]])
    keep <- c(keep, z_col)
  }
  fam_side <- d0[, keep, drop = FALSE]
  merged <- merge(df_long, fam_side, by = "aile_no", all.x = TRUE, all.y = FALSE)
  merged
}

pdt_path_model <- function(df_family, df_long, subscales = pdt_subscales(),
                           outcomes = c("srq_ho_conflict_mean", "srq_ho_rivalry_mean")) {
  if (!requireNamespace("lme4", quietly = TRUE)) {
    return(data.frame(durum = "lme4_yok", stringsAsFactors = FALSE))
  }
  merged <- pdt_build_long_frame(df_family, df_long, subscales)
  if (!"aile_no_f" %in% names(merged)) merged$aile_no_f <- factor(merged$aile_no)

  rows <- list()
  for (sub in subscales) {
    pred <- paste0("pdt_abs_", sub, "_z")
    if (!pred %in% names(merged)) next
    for (oc in outcomes) {
      if (!oc %in% names(merged)) next
      d <- merged
      d$.y <- pdt_scale(suppressWarnings(as.numeric(d[[oc]])))  # std sonuc
      d$.pred <- suppressWarnings(as.numeric(d[[pred]]))
      d <- d[stats::complete.cases(
        d[, c(".y", ".pred", "ses_latent_z", "age_gap_z", "same_sex",
              "group_f", "aile_no_f")]), , drop = FALSE]
      if (nrow(d) < 20L || length(unique(d$aile_no_f)) < 5L) {
        rows[[paste(sub, oc, sep = "_")]] <- data.frame(
          alt_olcek = sub, outcome = oc, terim = "pdt_abs_z",
          std_beta = NA_real_, se = NA_real_, alt_ga = NA_real_, ust_ga = NA_real_,
          p = NA_real_, icc = NA_real_, n = nrow(d), n_aile = length(unique(d$aile_no_f)),
          durum = "yetersiz_n", stringsAsFactors = FALSE
        )
        next
      }
      fit <- tryCatch(
        suppressWarnings(suppressMessages(lmerTest::lmer(
          .y ~ .pred + ses_latent_z + age_gap_z + same_sex + group_f + (1 | aile_no_f),
          data = d
        ))),
        error = function(e) e
      )
      if (inherits(fit, "error")) {
        rows[[paste(sub, oc, sep = "_")]] <- data.frame(
          alt_olcek = sub, outcome = oc, terim = "pdt_abs_z",
          std_beta = NA_real_, se = NA_real_, alt_ga = NA_real_, ust_ga = NA_real_,
          p = NA_real_, icc = NA_real_, n = nrow(d),
          n_aile = length(unique(d$aile_no_f)),
          durum = paste0("hata:", conditionMessage(fit)), stringsAsFactors = FALSE
        )
        next
      }
      cf <- summary(fit)$coefficients
      est <- cf[".pred", "Estimate"]
      se <- cf[".pred", "Std. Error"]
      pv <- cf[".pred", "Pr(>|t|)"]
      vc <- as.data.frame(lme4::VarCorr(fit))
      tau <- vc$vcov[vc$grp == "aile_no_f"]
      sig <- vc$vcov[vc$grp == "Residual"]
      icc <- if (length(tau) == 1L && length(sig) == 1L) tau / (tau + sig) else NA_real_
      rows[[paste(sub, oc, sep = "_")]] <- data.frame(
        alt_olcek = sub, outcome = oc, terim = "pdt_abs_z",
        std_beta = as.numeric(est), se = as.numeric(se),
        alt_ga = as.numeric(est - 1.96 * se), ust_ga = as.numeric(est + 1.96 * se),
        p = as.numeric(pv), icc = as.numeric(icc), n = nrow(d),
        n_aile = length(unique(d$aile_no_f)), durum = "ok",
        stringsAsFactors = FALSE
      )
    }
  }
  if (length(rows) == 0L) {
    return(data.frame(durum = "sonuc_yok", stringsAsFactors = FALSE))
  }
  do.call(rbind, rows)
}

# ============================================================================
# §98 — Dogrudan kayirma (favoritism): anne/baba kanal + iki-informant
# ============================================================================

pdt_add_favoritism <- function(df_family) {
  out <- df_family
  fav <- pdt_favoritism_map()
  for (informant in c("srq", "srq_sib")) {
    for (ch in names(fav)) {
      cols <- pdt_srq_item_columns(informant, fav[[ch]])
      if (!all(cols %in% names(out))) next
      mat <- as.data.frame(lapply(out[cols], as.numeric))
      valid_n <- rowSums(!is.na(mat))
      means <- rowMeans(mat, na.rm = TRUE)
      means[valid_n < 2L | is.nan(means)] <- NA_real_
      inf_tag <- if (informant == "srq") "idx" else "sib"
      out[[paste0(ch, "_partiality_", inf_tag)]] <- means
    }
  }
  out
}

pdt_favoritism_channels <- function(df_family) {
  fav <- pdt_favoritism_map()
  rows <- list()
  for (ch in names(fav)) {
    for (inf_tag in c("idx", "sib")) {
      col <- paste0(ch, "_partiality_", inf_tag)
      if (!col %in% names(df_family)) next
      informant <- if (inf_tag == "idx") "srq" else "srq_sib"
      item_cols <- pdt_srq_item_columns(informant, fav[[ch]])
      alfa <- if (all(item_cols %in% names(df_family))) {
        pdt_cronbach_alpha(as.data.frame(lapply(df_family[item_cols], as.numeric)))
      } else {
        NA_real_
      }
      omega <- if (all(item_cols %in% names(df_family))) {
        pdt_omega_total(as.data.frame(lapply(df_family[item_cols], as.numeric)))
      } else {
        NA_real_
      }
      for (grp in c("Pooled", "Kontrol", "DM")) {
        v <- if (grp == "Pooled") {
          suppressWarnings(as.numeric(df_family[[col]]))
        } else {
          suppressWarnings(as.numeric(df_family[[col]][as.character(df_family$group_f) == grp]))
        }
        v <- v[!is.na(v)]
        rows[[paste(ch, inf_tag, grp, sep = "_")]] <- data.frame(
          kanal = ch,
          kanal_etiket = if (ch == "mat") "anne_kayirma" else "baba_kayirma",
          informant = inf_tag,
          grup = grp,
          n = length(v),
          ort = if (length(v) > 0L) mean(v) else NA_real_,
          medyan = if (length(v) > 0L) stats::median(v) else NA_real_,
          sd = if (length(v) > 1L) stats::sd(v) else NA_real_,
          alfa_3madde = alfa,
          omega_3madde = omega,
          stringsAsFactors = FALSE
        )
      }
    }
  }
  if (length(rows) == 0L) return(data.frame())
  do.call(rbind, rows)
}

# Grup karsilastirmasi (DM vs Kontrol) her kanal x informant
pdt_favoritism_group_test <- function(df_family) {
  fav <- pdt_favoritism_map()
  rows <- list()
  for (ch in names(fav)) {
    for (inf_tag in c("idx", "sib")) {
      col <- paste0(ch, "_partiality_", inf_tag)
      if (!col %in% names(df_family)) next
      v <- suppressWarnings(as.numeric(df_family[[col]]))
      g <- as.character(df_family$group_f)
      dmv <- v[g == "DM"]; dmv <- dmv[!is.na(dmv)]
      kov <- v[g == "Kontrol"]; kov <- kov[!is.na(kov)]
      d_est <- NA_real_; d_lo <- NA_real_; d_hi <- NA_real_
      p_val <- NA_real_
      if (length(dmv) >= 3L && length(kov) >= 3L) {
        dd <- tryCatch(
          suppressWarnings(effectsize::cohens_d(dmv, kov, ci = 0.95)),
          error = function(e) NULL
        )
        if (!is.null(dd)) {
          d_est <- as.numeric(dd$Cohens_d[1L])
          d_lo <- as.numeric(dd$CI_low[1L])
          d_hi <- as.numeric(dd$CI_high[1L])
        }
        p_val <- tryCatch(stats::t.test(dmv, kov)$p.value, error = function(e) NA_real_)
      }
      rows[[paste(ch, inf_tag, sep = "_")]] <- data.frame(
        kanal = ch,
        informant = inf_tag,
        n_dm = length(dmv),
        n_kontrol = length(kov),
        ort_dm = if (length(dmv) > 0L) mean(dmv) else NA_real_,
        ort_kontrol = if (length(kov) > 0L) mean(kov) else NA_real_,
        medyan_dm = if (length(dmv) > 0L) stats::median(dmv) else NA_real_,
        medyan_kontrol = if (length(kov) > 0L) stats::median(kov) else NA_real_,
        cohens_d = d_est,
        d_alt_ga = d_lo,
        d_ust_ga = d_hi,
        p = p_val,
        stringsAsFactors = FALSE
      )
    }
  }
  if (length(rows) == 0L) return(data.frame())
  do.call(rbind, rows)
}

# Iki-informant uyum: ICC(2,1) + Bland-Altman (idx vs sib), grup stratifiye
pdt_favoritism_icc <- function(df_family) {
  fav <- pdt_favoritism_map()
  rows <- list()
  for (ch in names(fav)) {
    idx_col <- paste0(ch, "_partiality_idx")
    sib_col <- paste0(ch, "_partiality_sib")
    if (!all(c(idx_col, sib_col) %in% names(df_family))) next
    for (grp in c("Pooled", "Kontrol", "DM")) {
      sub_df <- if (grp == "Pooled") df_family else df_family[as.character(df_family$group_f) == grp, , drop = FALSE]
      a <- suppressWarnings(as.numeric(sub_df[[idx_col]]))
      b <- suppressWarnings(as.numeric(sub_df[[sib_col]]))
      ok <- !is.na(a) & !is.na(b)
      a <- a[ok]; b <- b[ok]
      n <- length(a)
      icc <- NA_real_; lo <- NA_real_; hi <- NA_real_
      md <- NA_real_; sdd <- NA_real_; loa_lo <- NA_real_; loa_hi <- NA_real_
      if (n >= 10L && requireNamespace("irr", quietly = TRUE)) {
        ic <- tryCatch(
          irr::icc(cbind(a, b), model = "twoway", type = "agreement", unit = "single"),
          error = function(e) NULL
        )
        if (!is.null(ic)) {
          icc <- ic$value; lo <- ic$lbound; hi <- ic$ubound
        }
        diffs <- a - b
        md <- mean(diffs); sdd <- stats::sd(diffs)
        loa_lo <- md - 1.96 * sdd; loa_hi <- md + 1.96 * sdd
      } else if (n >= 3L) {
        icc <- suppressWarnings(stats::cor(a, b))
        diffs <- a - b
        md <- mean(diffs); sdd <- stats::sd(diffs)
        loa_lo <- md - 1.96 * sdd; loa_hi <- md + 1.96 * sdd
      }
      rows[[paste(ch, grp, sep = "_")]] <- data.frame(
        kanal = ch,
        grup = grp,
        n = n,
        icc_2_1 = icc,
        icc_alt_ga = lo,
        icc_ust_ga = hi,
        ba_ort_fark = md,
        ba_sd_fark = sdd,
        ba_loa_alt = loa_lo,
        ba_loa_ust = loa_hi,
        stringsAsFactors = FALSE
      )
    }
  }
  if (length(rows) == 0L) return(data.frame())
  do.call(rbind, rows)
}

# MTMM yakinsama: SRQ-kayirma <-> EMBU-C PDT (§96 skorlari) korelasyon + yon uyumu
pdt_mtmm_convergence <- function(df_family, subscales = pdt_subscales()) {
  fav <- pdt_favoritism_map()
  rows <- list()
  for (ch in names(fav)) {
    for (inf_tag in c("idx", "sib")) {
      fav_col <- paste0(ch, "_partiality_", inf_tag)
      if (!fav_col %in% names(df_family)) next
      fav_v <- suppressWarnings(as.numeric(df_family[[fav_col]]))
      for (sub in subscales) {
        for (metric in c("signed", "abs")) {
          pdt_col <- paste0("pdt_", metric, "_", sub)
          if (!pdt_col %in% names(df_family)) next
          pv <- suppressWarnings(as.numeric(df_family[[pdt_col]]))
          ok <- !is.na(fav_v) & !is.na(pv)
          n <- sum(ok)
          r <- if (n >= 3L && stats::sd(fav_v[ok]) > 0 && stats::sd(pv[ok]) > 0) {
            suppressWarnings(stats::cor(fav_v[ok], pv[ok]))
          } else {
            NA_real_
          }
          rows[[paste(ch, inf_tag, sub, metric, sep = "_")]] <- data.frame(
            srq_kanal = ch,
            srq_informant = inf_tag,
            embu_alt_olcek = sub,
            embu_metrik = metric,
            n = n,
            r = r,
            yon = ifelse(is.na(r), NA_character_, ifelse(r >= 0, "pozitif", "negatif")),
            yorum = "yakinsama: converging(r>0; ayni yon) vs diverging(gecerli vantaj farki; olcum hatasi DEGIL)",
            stringsAsFactors = FALSE
          )
        }
      }
    }
  }
  if (length(rows) == 0L) return(data.frame())
  do.call(rbind, rows)
}

# ============================================================================
# §99 — Mesruiyet/baglam moderasyonu (pdt_abs x group_f) + TOST
# ============================================================================

pdt_moderation <- function(df_family, df_long, subscales = pdt_subscales(),
                           outcomes = c("srq_ho_conflict_mean", "srq_ho_rivalry_mean")) {
  if (!requireNamespace("lme4", quietly = TRUE)) {
    return(list(
      moderation = data.frame(durum = "lme4_yok", stringsAsFactors = FALSE),
      slopes = data.frame(durum = "lme4_yok", stringsAsFactors = FALSE)
    ))
  }
  merged <- pdt_build_long_frame(df_family, df_long, subscales)
  if (!"aile_no_f" %in% names(merged)) merged$aile_no_f <- factor(merged$aile_no)

  mod_rows <- list()
  slope_rows <- list()
  for (sub in subscales) {
    pred <- paste0("pdt_abs_", sub, "_z")
    if (!pred %in% names(merged)) next
    for (oc in outcomes) {
      if (!oc %in% names(merged)) next
      d <- merged
      d$.y <- pdt_scale(suppressWarnings(as.numeric(d[[oc]])))
      d$.pred <- suppressWarnings(as.numeric(d[[pred]]))
      d <- d[stats::complete.cases(
        d[, c(".y", ".pred", "ses_latent_z", "age_gap_z", "same_sex",
              "group_f", "aile_no_f")]), , drop = FALSE]
      key <- paste(sub, oc, sep = "_")
      if (nrow(d) < 20L || length(unique(d$group_f)) < 2L ||
          length(unique(d$aile_no_f)) < 5L) {
        mod_rows[[key]] <- data.frame(
          alt_olcek = sub, outcome = oc, terim = "pdt_abs_z:group_fDM",
          tahmin = NA_real_, se = NA_real_, alt_ga = NA_real_, ust_ga = NA_real_,
          p = NA_real_, n = nrow(d), durum = "yetersiz_n",
          adalet_maddesi_siniri = "kanonik formda ayrik 'adil mi?' maddesi YOK; mesruiyet yalniz hastalik-baglami proxy'si",
          stringsAsFactors = FALSE
        )
        next
      }
      fit <- tryCatch(
        suppressWarnings(suppressMessages(lmerTest::lmer(
          .y ~ .pred * group_f + ses_latent_z + age_gap_z + same_sex + (1 | aile_no_f),
          data = d
        ))),
        error = function(e) e
      )
      if (inherits(fit, "error")) {
        mod_rows[[key]] <- data.frame(
          alt_olcek = sub, outcome = oc, terim = "pdt_abs_z:group_fDM",
          tahmin = NA_real_, se = NA_real_, alt_ga = NA_real_, ust_ga = NA_real_,
          p = NA_real_, n = nrow(d), durum = paste0("hata:", conditionMessage(fit)),
          adalet_maddesi_siniri = "kanonik formda ayrik 'adil mi?' maddesi YOK",
          stringsAsFactors = FALSE
        )
        next
      }
      cf <- summary(fit)$coefficients
      int_term <- grep(":group_f", rownames(cf), value = TRUE)[1L]
      if (is.na(int_term)) int_term <- ".pred:group_fDM"
      est <- if (int_term %in% rownames(cf)) cf[int_term, "Estimate"] else NA_real_
      se <- if (int_term %in% rownames(cf)) cf[int_term, "Std. Error"] else NA_real_
      pv <- if (int_term %in% rownames(cf)) cf[int_term, "Pr(>|t|)"] else NA_real_
      mod_rows[[key]] <- data.frame(
        alt_olcek = sub, outcome = oc, terim = "pdt_abs_z:group_fDM",
        tahmin = as.numeric(est), se = as.numeric(se),
        alt_ga = as.numeric(est - 1.96 * se), ust_ga = as.numeric(est + 1.96 * se),
        p = as.numeric(pv), n = nrow(d), durum = "ok",
        adalet_maddesi_siniri = "kanonik formda ayrik 'adil mi?' maddesi YOK; mesruiyet yalniz hastalik-baglami proxy'si",
        stringsAsFactors = FALSE
      )
      # emmeans basit egimler
      if (requireNamespace("emmeans", quietly = TRUE)) {
        et <- tryCatch(
          suppressWarnings(suppressMessages(
            emmeans::emtrends(fit, ~ group_f, var = ".pred")
          )),
          error = function(e) NULL
        )
        if (!is.null(et)) {
          es <- as.data.frame(summary(et, infer = c(TRUE, TRUE)))
          trend_col <- grep("trend", names(es), value = TRUE)[1L]
          lcl <- grep("lower.CL|asymp.LCL|lower", names(es), value = TRUE)[1L]
          ucl <- grep("upper.CL|asymp.UCL|upper", names(es), value = TRUE)[1L]
          slope_rows[[key]] <- data.frame(
            alt_olcek = sub, outcome = oc,
            grup = as.character(es$group_f),
            basit_egim = as.numeric(es[[trend_col]]),
            se = as.numeric(es$SE),
            alt_ga = as.numeric(es[[lcl]]),
            ust_ga = as.numeric(es[[ucl]]),
            stringsAsFactors = FALSE
          )
        }
      }
    }
  }
  list(
    moderation = if (length(mod_rows) > 0L) do.call(rbind, mod_rows) else data.frame(),
    slopes = if (length(slope_rows) > 0L) do.call(rbind, slope_rows) else data.frame()
  )
}

# TOST esdegerlik (SESOI |r|=.10) -- null iddialar icin (TOSTER z_cor_test)
pdt_tost_r <- function(x, y, sesoi_r = 0.10, alpha = 0.05) {
  ok <- !is.na(x) & !is.na(y)
  x <- x[ok]; y <- y[ok]
  n <- length(x)
  if (n < 10L || stats::sd(x) == 0 || stats::sd(y) == 0) {
    return(data.frame(
      n = n, r = NA_real_, sesoi_r = sesoi_r, tost_p = NA_real_,
      nhst_p = NA_real_, karar = "yetersiz_n", stringsAsFactors = FALSE
    ))
  }
  r_obs <- suppressWarnings(stats::cor(x, y))
  if (requireNamespace("TOSTER", quietly = TRUE)) {
    eq <- tryCatch(
      suppressWarnings(suppressMessages(
        TOSTER::z_cor_test(x, y, alternative = "equivalence", null = sesoi_r, alpha = alpha)
      )),
      error = function(e) NULL
    )
    ns <- tryCatch(
      suppressWarnings(suppressMessages(
        TOSTER::z_cor_test(x, y, alternative = "two.sided", null = 0, alpha = alpha)
      )),
      error = function(e) NULL
    )
    tost_p <- if (!is.null(eq)) as.numeric(eq$p.value) else NA_real_
    nhst_p <- if (!is.null(ns)) as.numeric(ns$p.value) else NA_real_
  } else {
    # elle Fisher-z TOST
    z <- atanh(r_obs); se <- 1 / sqrt(n - 3); zb <- atanh(sesoi_r)
    p_a <- stats::pnorm((z + zb) / se, lower.tail = FALSE)
    p_b <- stats::pnorm((z - zb) / se, lower.tail = TRUE)
    tost_p <- max(p_a, p_b)
    nhst_p <- 2 * stats::pnorm(abs(z) / se, lower.tail = FALSE)
  }
  karar <- if (is.na(tost_p) || is.na(nhst_p)) {
    "belirsiz"
  } else if (tost_p < alpha && nhst_p < alpha) {
    "onemsiz"
  } else if (tost_p < alpha && nhst_p >= alpha) {
    "esdeger"
  } else if (tost_p >= alpha && nhst_p < alpha) {
    "anlamli"
  } else {
    "belirsiz"
  }
  data.frame(
    n = n, r = r_obs, sesoi_r = sesoi_r, tost_p = tost_p,
    nhst_p = nhst_p, karar = karar, stringsAsFactors = FALSE
  )
}

pdt_tost_table <- function(df_family, subscales = pdt_subscales(),
                           outcomes = c("srq_ho_conflict_mean", "srq_ho_rivalry_mean"),
                           sesoi_r = 0.10) {
  rows <- list()
  g_dm <- as.integer(as.character(df_family$group_f) == "DM")
  # (a) buyukluk-grup esdegerligi: group -> pdt_abs
  for (sub in subscales) {
    abs_col <- paste0("pdt_abs_", sub)
    if (!abs_col %in% names(df_family)) next
    res <- pdt_tost_r(g_dm, suppressWarnings(as.numeric(df_family[[abs_col]])), sesoi_r)
    res$estimand <- "buyukluk_grup_farki"
    res$alt_olcek <- sub
    res$outcome <- NA_character_
    res$grup <- "pooled"
    rows[[paste("mag", sub, sep = "_")]] <- res
  }
  # (b) buffering / PDT -> SRQ esdegerligi: pooled + DM + Kontrol
  for (sub in subscales) {
    abs_col <- paste0("pdt_abs_", sub)
    if (!abs_col %in% names(df_family)) next
    for (oc in outcomes) {
      if (!oc %in% names(df_family)) next
      for (grp in c("pooled", "DM", "Kontrol")) {
        sel <- if (grp == "pooled") rep(TRUE, nrow(df_family)) else as.character(df_family$group_f) == grp
        res <- pdt_tost_r(
          suppressWarnings(as.numeric(df_family[[abs_col]][sel])),
          suppressWarnings(as.numeric(df_family[[oc]][sel])),
          sesoi_r
        )
        res$estimand <- "pdt_srq_esdegerlik"
        res$alt_olcek <- sub
        res$outcome <- oc
        res$grup <- grp
        rows[[paste("buf", sub, oc, grp, sep = "_")]] <- res
      }
    }
  }
  if (length(rows) == 0L) return(data.frame())
  out <- do.call(rbind, rows)
  out[, c("estimand", "alt_olcek", "outcome", "grup", "n", "r",
          "sesoi_r", "tost_p", "nhst_p", "karar")]
}

# ============================================================================
# Holm duzeltmesi (4 alt olcek x 2 estimand = 8 karsilastirma)
# ============================================================================

pdt_holm_table <- function(magnitude_group_p, direction_sign_p) {
  subs <- names(magnitude_group_p)
  df <- data.frame(
    alt_olcek = c(subs, subs),
    estimand = c(rep("buyukluk_grup", length(subs)),
                 rep("yon_isaret_testi", length(subs))),
    p_ham = c(as.numeric(magnitude_group_p), as.numeric(direction_sign_p)),
    stringsAsFactors = FALSE
  )
  valid <- !is.na(df$p_ham)
  df$p_holm <- NA_real_
  if (any(valid)) {
    df$p_holm[valid] <- stats::p.adjust(df$p_ham[valid], method = "holm")
  }
  df$anlamli_holm <- !is.na(df$p_holm) & df$p_holm < 0.05
  df
}

# ============================================================================
# Sarici pipeline (Faz II deseni)
# ============================================================================

run_phase3_pdt_effect_pipeline <- function(df_family_ses, df_long_scored,
                                           subscales = pdt_subscales(),
                                           outcomes = c("srq_ho_conflict_mean", "srq_ho_rivalry_mean"),
                                           n_boot = 1000L,
                                           sesoi_r = 0.10,
                                           seed = 20260708L) {
  set.seed(seed)

  # Ortak turetmeler
  fam <- pdt_add_signed_abs(df_family_ses, subscales)
  fam <- pdt_add_favoritism(fam)
  if (!"ses_latent_z" %in% names(fam)) fam$ses_latent_z <- pdt_scale(fam$ses_latent)
  if (!"age_gap_z" %in% names(fam)) fam$age_gap_z <- pdt_scale(fam$age_gap)
  if (!"cocuk_sayisi_z" %in% names(fam)) fam$cocuk_sayisi_z <- pdt_scale(fam$cocuk_sayisi)

  # §96
  rho_dd <- pdt_rho_dd_table(fam, subscales)
  rsa_surface <- pdt_rsa_surface_table(fam, subscales, outcomes, n_boot = n_boot)
  magnitude <- pdt_magnitude_model(fam, subscales)
  direction <- pdt_direction_test(fam, subscales)

  group_p <- attr(magnitude, "group_p") %|NA|% stats::setNames(rep(NA_real_, length(subscales)), subscales)
  sign_p <- attr(direction, "sign_p") %|NA|% stats::setNames(rep(NA_real_, length(subscales)), subscales)
  holm <- pdt_holm_table(group_p, sign_p)

  # magnitude/direction tablolarina Holm p ekle
  if (nrow(magnitude) > 0L) {
    magnitude$p_holm_grup <- NA_real_
    for (sub in subscales) {
      ph <- holm$p_holm[holm$alt_olcek == sub & holm$estimand == "buyukluk_grup"]
      is_grp <- magnitude$alt_olcek == sub & magnitude$terim == "group_fDM"
      if (length(ph) == 1L) magnitude$p_holm_grup[is_grp] <- ph
    }
  }
  if (nrow(direction) > 0L) {
    direction$p_holm_isaret <- NA_real_
    for (sub in subscales) {
      ph <- holm$p_holm[holm$alt_olcek == sub & holm$estimand == "yon_isaret_testi"]
      if (length(ph) == 1L) direction$p_holm_isaret[direction$alt_olcek == sub] <- ph
    }
  }

  # §97
  path_model <- pdt_path_model(fam, df_long_scored, subscales, outcomes)

  # §98
  favoritism_channels <- pdt_favoritism_channels(fam)
  favoritism_group_test <- pdt_favoritism_group_test(fam)
  favoritism_icc <- pdt_favoritism_icc(fam)
  mtmm_convergence <- pdt_mtmm_convergence(fam, subscales)

  # §99
  mod <- pdt_moderation(fam, df_long_scored, subscales, outcomes)
  moderation <- mod$moderation
  moderation_slopes <- mod$slopes

  # TOST
  tost <- pdt_tost_table(fam, subscales, outcomes, sesoi_r = sesoi_r)

  n_dm <- sum(as.character(fam$group_f) == "DM", na.rm = TRUE)
  n_kontrol <- sum(as.character(fam$group_f) == "Kontrol", na.rm = TRUE)
  target_summary <- data.frame(
    analiz = "phase3_pdt_effect",
    kisim = "KISIM XXXVI (§96-99)",
    n_aile = nrow(fam),
    n_dm = n_dm,
    n_kontrol = n_kontrol,
    n_long = nrow(df_long_scored),
    n_boot = n_boot,
    sesoi_r = sesoi_r,
    kanit_kategorisi = pdt_status_label(),
    sapma_tipi = "Tip 3 (Faz III SAP KISIM XXXVI, keşifsel post-hoc)",
    reference_doc = "docs/analiz_planlari/06-sap-faz3-ek-plan.md",
    dil = "korelasyonel (nedensel yorum yasak)",
    stringsAsFactors = FALSE
  )

  list(
    rho_dd = pdt_tag(rho_dd),
    rsa_surface = pdt_tag(rsa_surface),
    magnitude_model = pdt_tag(magnitude),
    direction_test = pdt_tag(direction),
    path_model = pdt_tag(path_model),
    favoritism_channels = pdt_tag(favoritism_channels),
    favoritism_group_test = pdt_tag(favoritism_group_test),
    favoritism_icc = pdt_tag(favoritism_icc),
    mtmm_convergence = pdt_tag(mtmm_convergence),
    moderation = pdt_tag(moderation),
    moderation_slopes = pdt_tag(moderation_slopes),
    tost = pdt_tag(tost),
    holm = pdt_tag(holm),
    target_summary = target_summary
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
