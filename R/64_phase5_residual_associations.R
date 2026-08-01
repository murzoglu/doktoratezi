# [KESIFSEL - POST-HOC] Faz V SAP KISIM L (§136-141)
# Artik Iliski Yuzeyi (Residual Association Surface) — OSF Layer 6
#
# Bu modul YALNIZ saf fonksiyon icerir (dosya I/O YOK). Kanonik CSV'lere yazma
# yoktur; yukleme runner uzerinden R/01_io.R ile yapilir. Tum ciktilar agregat
# istatistiktir; satir-duzeyi katilimci verisi hicbir tabloya dokulmez.
#
# KAPSAM: Faz I-IV cekirdek + genisletmeler sonrasi, kanonik bazda MEVCUT ama
# bir sonuc modeline focal girmemis birkac artik iliski yuzeyi. YENI VERI YOK;
# kanonik kilit DEGISMEZ; H1-H5 confirmatory cekirdek DEGISMEZ. Tum ciktilar
# korelasyoneldir; nedensel dil yasak. Cok-karsilastirma BH-FDR paragraf-ici.
#
# §136 [Tier B]: Maternal depresyon (Beck) -> kardes iliskisi (SRQ ust-boyut).
#   H2 grup->SRQ null bulmustu; bu paragraf FARKLI bir ekseni (anne depresyonu)
#   dener. group_f + ses_latent kismi kontrol; BH-FDR (4 boyut).
#
# §137 [Tier B]: Informant transmisyon / b-yolu darbogazi + reddetme-disi
#   mediasyon. Her EMBU alt olcegi icin a (Beck->EMBU-P), b (EMBU-P->EMBU-C_idx),
#   dolayli a*b (bootstrap yuzdelik GA), c' (dogrudan). R/23 yalniz reddetme'yi
#   test etmisti; burada 4 alt olcek. Bulgunun cekirdegi: b-yolu (anne oz-rapor
#   -> cocuk algisi) tum boyutlarda zayif -> depresyonun etkisi cocuk algisina
#   "transmisyon" gostermez.
#
# §138 [Tier B]: Asiri korumanin sosyo-demografik gradyani (birlesik model).
#   embu_p_asiri_koruma ~ anne_yas_z + ses_latent_z + kalabalik_indeksi_z + group.
#   Ek: kullanilmamis prestij/sinif eksenleri (aile_isei08 / aile_siops08 /
#   aile_egp7) ile bivariate dogrulama. NOT: anne_yas ve ISEI gradyanlari Faz III
#   (R/57 §120, R/52 §100) ile ORTUSUR -> burada DOGRULAMA + kalabalik_indeksi
#   birlesik focal katki.
#
# §139 [Tier C]: Esler-arasi egitim farki -> reddetme (ve cift_kazanc). Turetilmis
#   ama focal kullanilmamis SES yardimcilari.
#
# §140 [Tier C]: Ayni-cinsiyet duad -> kardes iliskisi. H2 APIM yalniz age_gap
#   moderatorunu almisti; same_sex duad kompozisyonu test edilmemisti. Cohen d +
#   TOST(SESOI d=0.20).

# ---------------------------------------------------------------------------
# Sabitler ve yardimcilar
# ---------------------------------------------------------------------------

f5_status_label <- function() "[KESIFSEL - POST-HOC]"

f5_embu_subscales <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

f5_srq_dims <- function() {
  c("warmth", "status", "conflict", "rivalry")
}

f5_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s eksik kolon(lar): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

f5_num <- function(x) {
  suppressWarnings(as.numeric(as.character(x)))
}

f5_scale <- function(x) {
  x <- f5_num(x)
  ok <- !is.na(x)
  out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) {
    return(out)
  }
  s <- stats::sd(x[ok])
  if (is.na(s) || s == 0) {
    return(out)
  }
  out[ok] <- (x[ok] - mean(x[ok])) / s
  out
}

f5_desc <- function(x) {
  x <- f5_num(x)
  obs <- x[!is.na(x)]
  list(
    n = length(obs),
    mean = if (length(obs) > 0L) mean(obs) else NA_real_,
    median = if (length(obs) > 0L) stats::median(obs) else NA_real_,
    sd = if (length(obs) > 1L) stats::sd(obs) else NA_real_
  )
}

# Grup faktoru: group_f varsa onu, yoksa group'u kullan (ref = Kontrol).
f5_group_factor <- function(df) {
  g <- if ("group_f" %in% names(df)) {
    as.character(df$group_f)
  } else if ("group" %in% names(df)) {
    as.character(df$group)
  } else {
    rep(NA_character_, nrow(df))
  }
  factor(g, levels = c("Kontrol", "DM"))
}

# Korelasyon esdegerlik testi (TOST, Fisher-z; SESOI |r|).
f5_tost_r <- function(r, n, sesoi = 0.10, alpha = 0.05) {
  if (is.na(r) || is.na(n) || n < 5L || abs(r) >= 1) {
    return(list(p = NA_real_, decision = NA_character_))
  }
  z <- atanh(r)
  se <- 1 / sqrt(n - 3)
  stat_lower <- (z - atanh(-sesoi)) / se
  p_lower <- stats::pnorm(stat_lower, lower.tail = FALSE)
  stat_upper <- (z - atanh(sesoi)) / se
  p_upper <- stats::pnorm(stat_upper, lower.tail = TRUE)
  p_tost <- max(p_lower, p_upper)
  list(
    p = p_tost,
    decision = if (p_tost < alpha) "esdeger(|r|<SESOI)" else "esdeger_degil"
  )
}

# Ortalama-farki esdegerlik testi (TOST, Cohen d; SESOI d). Iki bagimsiz grup.
f5_tost_d <- function(x0, x1, sesoi = 0.20, alpha = 0.05) {
  x0 <- x0[!is.na(x0)]; x1 <- x1[!is.na(x1)]
  n0 <- length(x0); n1 <- length(x1)
  if (n0 < 3L || n1 < 3L) {
    return(list(p = NA_real_, decision = NA_character_))
  }
  sp <- sqrt(((n0 - 1) * stats::var(x0) + (n1 - 1) * stats::var(x1)) / (n0 + n1 - 2))
  if (is.na(sp) || sp == 0) {
    return(list(p = NA_real_, decision = NA_character_))
  }
  se <- sp * sqrt(1 / n0 + 1 / n1)
  diff <- mean(x1) - mean(x0)
  low <- -sesoi * sp; up <- sesoi * sp
  t_low <- (diff - low) / se
  p_low <- stats::pt(t_low, df = n0 + n1 - 2, lower.tail = FALSE)
  t_up <- (diff - up) / se
  p_up <- stats::pt(t_up, df = n0 + n1 - 2, lower.tail = TRUE)
  p_tost <- max(p_low, p_up)
  list(
    p = p_tost,
    decision = if (p_tost < alpha) "esdeger(|d|<SESOI)" else "esdeger_degil"
  )
}

# ---------------------------------------------------------------------------
# §136 — Maternal depresyon -> kardes iliskisi (SRQ)
# ---------------------------------------------------------------------------

f5_maternal_depression_sibling <- function(df, dims = f5_srq_dims(), sesoi_r = 0.10) {
  f5_require_columns(df, c("beck_total", "ses_latent", paste0("srq_ho_", dims, "_mean")),
    "§136 Beck->SRQ")
  grp <- f5_group_factor(df)
  beck <- f5_num(df$beck_total)

  rows <- list()
  for (dim in dims) {
    y <- f5_num(df[[paste0("srq_ho_", dim, "_mean")]])
    ok <- stats::complete.cases(y, beck)
    yy <- y[ok]; bb <- beck[ok]; n <- length(yy)
    if (n < 10L || stats::sd(yy) == 0 || stats::sd(bb) == 0) {
      rows[[length(rows) + 1L]] <- data.frame(
        boyut = dim, n = n, ham_r = NA_real_, ham_ci_alt = NA_real_,
        ham_ci_ust = NA_real_, ham_p = NA_real_, std_beta = NA_real_,
        ci_alt = NA_real_, ci_ust = NA_real_, p = NA_real_,
        tost_p = NA_real_, tost_karar = NA_character_, sesoi_r = sesoi_r,
        statu_kosum = "yetersiz_n",
        aciklama = "Beck -> SRQ (anne depresyonu -> kardes iliskisi); korelasyonel",
        statu = f5_status_label(), stringsAsFactors = FALSE
      )
      next
    }
    ct <- stats::cor.test(bb, yy)
    dd <- data.frame(y = f5_scale(y), beck = f5_scale(beck), grp = grp, ses = f5_scale(df$ses_latent))
    dd <- dd[stats::complete.cases(dd), , drop = FALSE]
    m <- tryCatch(stats::lm(y ~ beck + grp + ses, data = dd), error = function(e) NULL)
    if (!is.null(m)) {
      co <- summary(m)$coefficients["beck", ]
      cf <- stats::confint(m)["beck", ]
      std_beta <- unname(co[1]); ci_lo <- cf[1]; ci_hi <- cf[2]; p_par <- co[4]
    } else {
      std_beta <- NA_real_; ci_lo <- NA_real_; ci_hi <- NA_real_; p_par <- NA_real_
    }
    tost <- f5_tost_r(unname(ct$estimate), n, sesoi = sesoi_r)
    rows[[length(rows) + 1L]] <- data.frame(
      boyut = dim, n = n,
      ham_r = unname(ct$estimate), ham_ci_alt = ct$conf.int[1], ham_ci_ust = ct$conf.int[2],
      ham_p = ct$p.value, std_beta = std_beta, ci_alt = ci_lo, ci_ust = ci_hi, p = p_par,
      tost_p = tost$p, tost_karar = tost$decision, sesoi_r = sesoi_r,
      statu_kosum = "ok",
      aciklama = "Beck -> SRQ; kismi std_beta group_f+ses_latent kontrollu; korelasyonel",
      statu = f5_status_label(), stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §137 — Informant transmisyon / b-yolu + reddetme-disi mediasyon
# ---------------------------------------------------------------------------
# X = beck_total, M = embu_p_<sub>_mean, Y = embu_c_idx_<sub>_mean
# a: M ~ X + C ; b, c': Y ~ X + M + C ; dolayli = a*b (bootstrap yuzdelik GA)
# C = anne_yas_z + ses_latent_z (aile duzeyi).

f5_informant_transmission <- function(df, subs = f5_embu_subscales(),
                                      n_boot = 1000L, seed = 20260714L) {
  f5_require_columns(df, c("beck_total", "anne_yas", "ses_latent",
    paste0("embu_p_", subs, "_mean"), paste0("embu_c_idx_", subs, "_mean")),
    "§137 informant transmisyon")

  rows <- list()
  for (sub in subs) {
    dd <- data.frame(
      X = f5_scale(df$beck_total),
      M = f5_scale(df[[paste0("embu_p_", sub, "_mean")]]),
      Y = f5_scale(df[[paste0("embu_c_idx_", sub, "_mean")]]),
      c1 = f5_scale(df$anne_yas),
      c2 = f5_scale(df$ses_latent)
    )
    dd <- dd[stats::complete.cases(dd), , drop = FALSE]
    n <- nrow(dd)
    if (n < 20L) {
      rows[[length(rows) + 1L]] <- data.frame(
        boyut = sub, n = n, a_yolu = NA_real_, a_p = NA_real_,
        b_yolu = NA_real_, b_p = NA_real_, cprime = NA_real_, cprime_p = NA_real_,
        dolayli = NA_real_, dolayli_ci_alt = NA_real_, dolayli_ci_ust = NA_real_,
        n_boot = n_boot, statu_kosum = "yetersiz_n",
        aciklama = "Beck->EMBU-P->EMBU-C_idx dolayli yol; korelasyonel",
        statu = f5_status_label(), stringsAsFactors = FALSE
      )
      next
    }
    ma <- stats::lm(M ~ X + c1 + c2, data = dd)
    mb <- stats::lm(Y ~ X + M + c1 + c2, data = dd)
    a <- unname(stats::coef(ma)["X"])
    a_p <- summary(ma)$coefficients["X", 4]
    b <- unname(stats::coef(mb)["M"])
    b_p <- summary(mb)$coefficients["M", 4]
    cprime <- unname(stats::coef(mb)["X"])
    cprime_p <- summary(mb)$coefficients["X", 4]

    # Bootstrap dolayli etki (a*b), yuzdelik GA
    set.seed(seed)
    ind <- rep(NA_real_, n_boot)
    for (bi in seq_len(n_boot)) {
      idx <- sample.int(n, n, replace = TRUE)
      db <- dd[idx, , drop = FALSE]
      aa <- tryCatch(unname(stats::coef(stats::lm(M ~ X + c1 + c2, data = db))["X"]),
        error = function(e) NA_real_)
      bb <- tryCatch(unname(stats::coef(stats::lm(Y ~ X + M + c1 + c2, data = db))["M"]),
        error = function(e) NA_real_)
      ind[bi] <- aa * bb
    }
    ci <- stats::quantile(ind, c(0.025, 0.975), na.rm = TRUE)

    rows[[length(rows) + 1L]] <- data.frame(
      boyut = sub, n = n, a_yolu = a, a_p = a_p, b_yolu = b, b_p = b_p,
      cprime = cprime, cprime_p = cprime_p, dolayli = a * b,
      dolayli_ci_alt = unname(ci[1]), dolayli_ci_ust = unname(ci[2]),
      n_boot = n_boot, statu_kosum = "ok",
      aciklama = "a(Beck->P) b(P->C_idx) dolayli a*b bootstrap; b-yolu darbogazi odagi",
      statu = f5_status_label(), stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §138 — Asiri korumanin sosyo-demografik gradyani (birlesik model + dogrulama)
# ---------------------------------------------------------------------------

f5_overprotection_gradient <- function(df) {
  f5_require_columns(df, c("embu_p_asiri_koruma_mean", "anne_yas", "ses_latent",
    "kalabalik_indeksi"), "§138 asiri koruma gradyani (birlesik)")

  dd <- data.frame(
    y = f5_scale(df$embu_p_asiri_koruma_mean),
    age = f5_scale(df$anne_yas),
    ses = f5_scale(df$ses_latent),
    crowd = f5_scale(df$kalabalik_indeksi),
    grp = f5_group_factor(df)
  )
  dd <- dd[stats::complete.cases(dd), , drop = FALSE]
  n <- nrow(dd)

  joint_rows <- list()
  if (n >= 20L) {
    m <- stats::lm(y ~ age + ses + crowd + grp, data = dd)
    sm <- summary(m)$coefficients
    ci <- stats::confint(m)
    for (term in c("age", "ses", "crowd")) {
      joint_rows[[length(joint_rows) + 1L]] <- data.frame(
        analiz = "birlesik_model", terim = term, n = n,
        std_beta = unname(stats::coef(m)[term]), ci_alt = ci[term, 1], ci_ust = ci[term, 2],
        p = sm[term, 4], method = "lm(std) ~ age+ses+crowd+group",
        statu_kosum = "ok", statu = f5_status_label(), stringsAsFactors = FALSE
      )
    }
  } else {
    joint_rows[[1L]] <- data.frame(
      analiz = "birlesik_model", terim = NA_character_, n = n,
      std_beta = NA_real_, ci_alt = NA_real_, ci_ust = NA_real_, p = NA_real_,
      method = "lm", statu_kosum = "yetersiz_n", statu = f5_status_label(),
      stringsAsFactors = FALSE
    )
  }

  # Bivariate dogrulama: prestij/sinif eksenleri (kullanilmamis) -> asiri koruma
  y_raw <- f5_num(df$embu_p_asiri_koruma_mean)
  biv <- list()
  add_biv <- function(vname, method) {
    if (!vname %in% names(df)) return(NULL)
    x <- f5_num(df[[vname]])
    ok <- stats::complete.cases(x, y_raw)
    if (sum(ok) < 10L) return(NULL)
    ct <- suppressWarnings(stats::cor.test(x[ok], y_raw[ok], method = method))
    data.frame(
      analiz = "bivariate_dogrulama", terim = vname, n = sum(ok),
      std_beta = unname(ct$estimate),
      ci_alt = if (!is.null(ct$conf.int)) ct$conf.int[1] else NA_real_,
      ci_ust = if (!is.null(ct$conf.int)) ct$conf.int[2] else NA_real_,
      p = ct$p.value, method = paste0(method, "_r"),
      statu_kosum = "ok", statu = f5_status_label(), stringsAsFactors = FALSE
    )
  }
  biv[[1]] <- add_biv("aile_isei08", "pearson")
  biv[[2]] <- add_biv("aile_siops08", "pearson")
  biv[[3]] <- add_biv("aile_egp7", "spearman")

  out <- do.call(rbind, c(joint_rows, Filter(Negate(is.null), biv)))
  out
}

# ---------------------------------------------------------------------------
# §139 — Esler-arasi egitim farki -> reddetme (+ cift_kazanc)
# ---------------------------------------------------------------------------

f5_education_gap <- function(df) {
  outcomes <- c("reddetme", "asiri_koruma")
  f5_require_columns(df, c("egitim_fark", paste0("embu_p_", outcomes, "_mean")),
    "§139 egitim farki")

  rows <- list()
  eg <- f5_num(df$egitim_fark)
  for (out in outcomes) {
    y <- f5_num(df[[paste0("embu_p_", out, "_mean")]])
    ok <- stats::complete.cases(eg, y)
    if (sum(ok) < 10L) next
    ct <- stats::cor.test(eg[ok], y[ok])
    rows[[length(rows) + 1L]] <- data.frame(
      yordayici = "egitim_fark", boyut = out, n = sum(ok),
      r = unname(ct$estimate), ci_alt = ct$conf.int[1], ci_ust = ct$conf.int[2],
      p = ct$p.value, statu_kosum = "ok",
      aciklama = "Esler-arasi egitim uyumsuzlugu -> ebeveynlik; korelasyonel",
      statu = f5_status_label(), stringsAsFactors = FALSE
    )
  }
  # cift_kazanc (ikili) -> reddetme, nokta-biserial (cor)
  if ("cift_kazanc" %in% names(df)) {
    ck <- f5_num(df$cift_kazanc)
    y <- f5_num(df$embu_p_reddetme_mean)
    ok <- stats::complete.cases(ck, y)
    if (sum(ok) >= 10L && stats::sd(ck[ok]) > 0) {
      ct <- stats::cor.test(ck[ok], y[ok])
      rows[[length(rows) + 1L]] <- data.frame(
        yordayici = "cift_kazanc", boyut = "reddetme", n = sum(ok),
        r = unname(ct$estimate), ci_alt = ct$conf.int[1], ci_ust = ct$conf.int[2],
        p = ct$p.value, statu_kosum = "ok",
        aciklama = "Cift kazanc (ikili) -> reddetme; nokta-biserial; korelasyonel",
        statu = f5_status_label(), stringsAsFactors = FALSE
      )
    }
  }
  if (length(rows) == 0L) {
    return(data.frame(
      yordayici = character(), boyut = character(), n = integer(), r = numeric(),
      ci_alt = numeric(), ci_ust = numeric(), p = numeric(), statu_kosum = character(),
      aciklama = character(), statu = character(), stringsAsFactors = FALSE
    ))
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §140 — Ayni-cinsiyet duad -> kardes iliskisi (SRQ)
# ---------------------------------------------------------------------------

f5_same_sex_sibling <- function(df, dims = f5_srq_dims(), sesoi_d = 0.20) {
  f5_require_columns(df, c("same_sex", paste0("srq_ho_", dims, "_mean")),
    "§140 same_sex -> SRQ")

  g <- df$same_sex
  # same_sex faktor ("Ayni"/"Farkli") veya 0/1 olabilir; ikili gruba cevir.
  gg <- suppressWarnings(as.integer(as.character(g)))
  if (all(is.na(gg))) {
    lev <- sort(unique(as.character(g[!is.na(g)])))
    gg <- match(as.character(g), lev) - 1L  # 0 = ilk duzey (alfabetik: Ayni), 1 = Farkli
    grp_label0 <- if (length(lev) >= 1L) lev[1] else "grup0"
    grp_label1 <- if (length(lev) >= 2L) lev[2] else "grup1"
  } else {
    grp_label0 <- "0"; grp_label1 <- "1"
  }

  rows <- list()
  for (dim in dims) {
    y <- f5_num(df[[paste0("srq_ho_", dim, "_mean")]])
    ok <- stats::complete.cases(y, gg)
    yy <- y[ok]; ga <- gg[ok]
    y0 <- yy[ga == 0]; y1 <- yy[ga == 1]
    if (length(y0) < 3L || length(y1) < 3L || stats::sd(yy) == 0) {
      rows[[length(rows) + 1L]] <- data.frame(
        boyut = dim, grup0 = grp_label0, grup1 = grp_label1,
        n0 = length(y0), n1 = length(y1), ort0 = NA_real_, ort1 = NA_real_,
        cohen_d = NA_real_, t_p = NA_real_, tost_p = NA_real_, tost_karar = NA_character_,
        sesoi_d = sesoi_d, statu_kosum = "yetersiz_n",
        aciklama = "same_sex duad -> SRQ; korelasyonel",
        statu = f5_status_label(), stringsAsFactors = FALSE
      )
      next
    }
    sp <- sqrt(((length(y0) - 1) * stats::var(y0) + (length(y1) - 1) * stats::var(y1)) /
      (length(y0) + length(y1) - 2))
    d <- (mean(y1) - mean(y0)) / sp
    tt <- stats::t.test(y1, y0)
    tost <- f5_tost_d(y0, y1, sesoi = sesoi_d)
    rows[[length(rows) + 1L]] <- data.frame(
      boyut = dim, grup0 = grp_label0, grup1 = grp_label1,
      n0 = length(y0), n1 = length(y1), ort0 = mean(y0), ort1 = mean(y1),
      cohen_d = d, t_p = tt$p.value, tost_p = tost$p, tost_karar = tost$decision,
      sesoi_d = sesoi_d, statu_kosum = "ok",
      aciklama = "same_sex duad -> SRQ (grup1 eksi grup0 d); korelasyonel",
      statu = f5_status_label(), stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# FDR (BH) — her paragraf kendi ailesi (paragraflar arasi birlestirme YOK)
# ---------------------------------------------------------------------------

f5_fdr_table <- function(beck_srq, education_gap, same_sex) {
  collect <- function(paragraf, test_adi, p) {
    keep <- !is.na(p)
    if (!any(keep)) return(NULL)
    data.frame(paragraf = paragraf, test_adi = test_adi[keep], p_ham = p[keep],
      stringsAsFactors = FALSE)
  }
  fam_list <- list()
  if (!is.null(beck_srq)) {
    ok <- beck_srq[beck_srq$statu_kosum == "ok", , drop = FALSE]
    if (nrow(ok) > 0L) fam_list[["136"]] <- collect("§136",
      paste0("beck_srq:", ok$boyut), ok$ham_p)
  }
  if (!is.null(education_gap)) {
    ok <- education_gap[education_gap$statu_kosum == "ok", , drop = FALSE]
    if (nrow(ok) > 0L) fam_list[["139"]] <- collect("§139",
      paste0("egitim:", ok$yordayici, "_", ok$boyut), ok$p)
  }
  if (!is.null(same_sex)) {
    ok <- same_sex[same_sex$statu_kosum == "ok", , drop = FALSE]
    if (nrow(ok) > 0L) fam_list[["140"]] <- collect("§140",
      paste0("same_sex:", ok$boyut), ok$t_p)
  }
  base <- do.call(rbind, fam_list)
  if (is.null(base) || nrow(base) == 0L) {
    return(data.frame(paragraf = character(), test_adi = character(), p_ham = numeric(),
      p_bh = numeric(), yontem = character(), statu = character(), stringsAsFactors = FALSE))
  }
  base$p_bh <- NA_real_
  for (par in unique(base$paragraf)) {
    idx <- base$paragraf == par
    base$p_bh[idx] <- stats::p.adjust(base$p_ham[idx], method = "BH")
  }
  base$yontem <- "BH(paragraf-ici)"
  base$statu <- f5_status_label()
  rownames(base) <- NULL
  base
}

# ---------------------------------------------------------------------------
# Pipeline sarici (Faz III/IV deseni)
# ---------------------------------------------------------------------------

run_phase5_residual_associations_pipeline <- function(df_family_ses,
                                                      subscales = f5_embu_subscales(),
                                                      srq_dims = f5_srq_dims(),
                                                      n_boot = 1000L,
                                                      sesoi_r = 0.10,
                                                      sesoi_d = 0.20,
                                                      seed = 20260714L) {
  beck_srq <- f5_maternal_depression_sibling(df_family_ses, dims = srq_dims, sesoi_r = sesoi_r)
  transmission <- f5_informant_transmission(df_family_ses, subs = subscales,
    n_boot = n_boot, seed = seed)
  overprotection <- f5_overprotection_gradient(df_family_ses)
  education_gap <- f5_education_gap(df_family_ses)
  same_sex <- f5_same_sex_sibling(df_family_ses, dims = srq_dims, sesoi_d = sesoi_d)
  fdr <- f5_fdr_table(beck_srq, education_gap, same_sex)

  target_summary <- data.frame(
    analiz = "phase5_residual_associations",
    kisim = "KISIM L (§136-141) — Faz V",
    n_aile = nrow(df_family_ses),
    n_boot = n_boot,
    sesoi_r = sesoi_r,
    sesoi_d = sesoi_d,
    seed = seed,
    kanit_kategorisi = f5_status_label(),
    sapma_tipi = "Tip 3 (Faz V post-hoc genisletme; OSF Layer 6)",
    reference_doc = "docs/analiz_planlari/08-sap-faz5-ek-plan.md v0.1",
    dil_notu = "Korelasyonel dil; nedensel dil yasak; H1-H5 confirmatory DEGISMEZ",
    stringsAsFactors = FALSE
  )

  list(
    beck_sibling = beck_srq,
    informant_transmission = transmission,
    overprotection_gradient = overprotection,
    education_gap = education_gap,
    same_sex_sibling = same_sex,
    fdr = fdr,
    target_summary = target_summary
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
