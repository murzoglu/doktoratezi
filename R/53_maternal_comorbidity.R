# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXVIII/103-106
# Anne Somatik Komorbidite ve Aile Saglik Yuku
#
# 103 — [Tier D — TEST EDILEMEZ] Anne otoimmun (+ endokrin) betimsel prevalans
#       DM vs Kontrol, Fisher kesin test. otoimmun n=1 (Kontrol'de); Malcova
#       taban-orani ~%2 -> yapisal test imkansiz. Sadece betimsel + gerekce.
#
# 104 — [Tier C] anne_any_comorbid = anne_hastalik_kategori_sayisi >= 1 (ikili,
#       n~61). -> beck_total ve EMBU-P 4 alt olcek (Welch t + grup-kovaryat OLS;
#       Cohen's d + %95 GA). Basit aracilik: any_comorbid -> beck_total ->
#       embu_p_sicaklik/reddetme (lavaan BCa 1000).
#
# 105 — [Tier B-] Iki-gosterge maternal-distres yakinsamasi. anne_antidepresan
#       x group_f chi-kare (n=46; DM 35 / Kontrol 11); antidepresan <-> beck_total
#       nokta-biserial r + %95 GA; iki-gosterge (antidepresan vs beck klinik)
#       uyum tablosu; ortak-yontem uyarisi.
#
# 106 — [Tier C] es_any_comorbid = es_hastalik_kategori_sayisi >= 1; NEGATIF
#       KONTROL: es_any_comorbid -> EMBU-C (cocugun ANNE algisi, long lme4).
#       Beklenti sifira yakin; katsayi + %95 GA + TOST |r|=.10 (SESOI).
#       Aile toplam yuk kovaryat duyarliligi.
#
# Holm KISIM icindedir (bolumler arasi birlestirme yok).
# Skill Kurali: imputation yok (HbA1c/klinik); korelasyonel dil; satir-duzeyi
# veri dokulmez; her surekli degisken ortalama + medyan; alt-grup n acik.
# Veri: df_family_ses (anne EMBU-P + Beck + hastalik + antidepresan + SES),
#       df_long_scored (cocuk EMBU-C, Indeks + Kardes).

# ============================================================================
# Yardimci fonksiyonlar
# ============================================================================

mc_evidence_status <- function() {
  "[KESIFSEL - POST-HOC]"
}

mc_embu_p_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

mc_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s",
      context, paste(missing_columns, collapse = ", ")), call. = FALSE)
  }
  invisible(TRUE)
}

mc_binary_from_count <- function(x) {
  vals <- suppressWarnings(as.numeric(x))
  ifelse(is.na(vals), NA_integer_, as.integer(vals >= 1))
}

mc_ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f == "DM")
    } else if ("group" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$group), ignore.case = TRUE))
    }
  }
  df
}

mc_scale <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) {
    return(rep(NA_real_, length(x)))
  }
  (x - mean(x, na.rm = TRUE)) / s
}

# Cohen's d (grup1 - grup0) + %95 GA. effectsize varsa onu kullanir, yoksa
# havuzlanmis-SD + noncentral-yaklasik geri dusme.
mc_cohens_d_ci <- function(values, group_bin) {
  ok <- !is.na(values) & !is.na(group_bin)
  values <- values[ok]
  g <- group_bin[ok]
  n1 <- sum(g == 1L)
  n0 <- sum(g == 0L)
  if (n1 < 3L || n0 < 3L) {
    return(list(d = NA_real_, ci_low = NA_real_, ci_high = NA_real_,
      n1 = n1, n0 = n0))
  }
  if (requireNamespace("effectsize", quietly = TRUE)) {
    fr <- data.frame(y = values, grp = factor(g, levels = c(0L, 1L)))
    res <- tryCatch(
      suppressWarnings(effectsize::cohens_d(y ~ grp, data = fr, ci = 0.95)),
      error = function(e) NULL
    )
    if (!is.null(res)) {
      # effectsize: grup(0) - grup(1) siralamasi -> yon ters, isaret cevrilir
      return(list(
        d = -as.numeric(res$Cohens_d),
        ci_low = -as.numeric(res$CI_high),
        ci_high = -as.numeric(res$CI_low),
        n1 = n1, n0 = n0
      ))
    }
  }
  m1 <- mean(values[g == 1L]); m0 <- mean(values[g == 0L])
  s1 <- stats::sd(values[g == 1L]); s0 <- stats::sd(values[g == 0L])
  sp <- sqrt(((n1 - 1) * s1^2 + (n0 - 1) * s0^2) / (n1 + n0 - 2))
  d <- if (sp > 0) (m1 - m0) / sp else NA_real_
  se_d <- sqrt((n1 + n0) / (n1 * n0) + d^2 / (2 * (n1 + n0)))
  list(d = d, ci_low = d - 1.96 * se_d, ci_high = d + 1.96 * se_d,
    n1 = n1, n0 = n0)
}

# ============================================================================
# 103 — Anne otoimmun/endokrin betimsel prevalans (Tier D — TEST EDILEMEZ)
# ============================================================================

mc_group_prevalence <- function(indicator_bin, group_f, group_label) {
  in_grp <- as.character(group_f) == group_label
  ind <- indicator_bin[in_grp]
  n_toplam <- sum(!is.na(ind))
  n_pozitif <- sum(ind == 1L, na.rm = TRUE)
  data.frame(
    n_pozitif = n_pozitif,
    n_toplam = n_toplam,
    prevalans_pct = if (n_toplam > 0L) round(100 * n_pozitif / n_toplam, 2) else NA_real_,
    stringsAsFactors = FALSE
  )
}

mc_autoimmune_prevalence <- function(df_family) {
  mc_require_columns(
    df_family,
    c("group_f", "anne_hastalik_otoimmun", "anne_hastalik_endokrin"),
    "103 otoimmun prevalans"
  )
  otoimmun <- mc_binary_from_count(df_family$anne_hastalik_otoimmun)
  endokrin <- mc_binary_from_count(df_family$anne_hastalik_endokrin)
  birlesik <- ifelse(is.na(otoimmun) & is.na(endokrin), NA_integer_,
    as.integer((otoimmun %in% 1L) | (endokrin %in% 1L)))

  gostergeler <- list(
    otoimmun = otoimmun,
    endokrin = endokrin,
    otoimmun_veya_endokrin = birlesik
  )
  gerekceler <- list(
    otoimmun = paste0("otoimmun n=1 (Kontrol'de); Malcova 2004 taban-orani ~%2 ",
      "-> n=120 DM'de beklenen ~2-3, gozlenen 0 taban-oran sinirinda. ",
      "Oz-bildirim formu klinik otoimmun panel degil -> eksik-tespit. ",
      "'Confounder yok' DEGIL 'orneklemde olculemedi'."),
    endokrin = "endokrin oz-bildirim; klinik tiroid/celyak taramasi degil.",
    otoimmun_veya_endokrin = "birlesik betimsel; hucre kucuk -> Fisher kesin."
  )

  rows <- lapply(names(gostergeler), function(g) {
    ind <- gostergeler[[g]]
    dm <- mc_group_prevalence(ind, df_family$group_f, "DM")
    ko <- mc_group_prevalence(ind, df_family$group_f, "Kontrol")
    tab <- table(
      factor(ind, levels = c(0L, 1L)),
      factor(df_family$group_f, levels = c("Kontrol", "DM"))
    )
    ft <- tryCatch(stats::fisher.test(tab), error = function(e) NULL)
    data.frame(
      gosterge = g,
      dm_pozitif = dm$n_pozitif, dm_toplam = dm$n_toplam, dm_prevalans_pct = dm$prevalans_pct,
      kontrol_pozitif = ko$n_pozitif, kontrol_toplam = ko$n_toplam,
      kontrol_prevalans_pct = ko$prevalans_pct,
      fisher_p = if (!is.null(ft)) unname(ft$p.value) else NA_real_,
      fisher_or = if (!is.null(ft) && !is.null(ft$estimate)) unname(ft$estimate) else NA_real_,
      test_edilebilir = "HAYIR",
      gerekce = gerekceler[[g]],
      tier = "D",
      statu = mc_evidence_status(),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

# ============================================================================
# 104 — Ikili komorbidite -> Beck / EMBU-P (Tier C)
# ============================================================================

mc_subgroup_desc <- function(values, comorbid_bin, level) {
  v <- values[!is.na(values) & !is.na(comorbid_bin) & comorbid_bin == level]
  data.frame(
    n = length(v),
    ortalama = if (length(v) > 0L) mean(v) else NA_real_,
    medyan = if (length(v) > 0L) stats::median(v) else NA_real_,
    sd = if (length(v) > 1L) stats::sd(v) else NA_real_,
    stringsAsFactors = FALSE
  )
}

mc_binary_comorbid_effects <- function(df_family) {
  df_family <- mc_ensure_group_dm(df_family)
  outcome_cols <- c("beck_total",
    paste0("embu_p_", mc_embu_p_outcomes(), "_mean"))
  mc_require_columns(
    df_family,
    c("group_dm", "anne_hastalik_kategori_sayisi", outcome_cols),
    "104 ikili komorbidite"
  )
  comorbid <- mc_binary_from_count(df_family$anne_hastalik_kategori_sayisi)

  rows <- lapply(outcome_cols, function(oc) {
    y <- suppressWarnings(as.numeric(df_family[[oc]]))
    d1 <- mc_subgroup_desc(y, comorbid, 1L)
    d0 <- mc_subgroup_desc(y, comorbid, 0L)

    # Welch t-test (komorbidite var vs yok)
    y1 <- y[!is.na(y) & comorbid == 1L]
    y0 <- y[!is.na(y) & comorbid == 0L]
    tt <- tryCatch(stats::t.test(y1, y0), error = function(e) NULL)

    # OLS: outcome ~ comorbid + group_dm (grup-kovaryat)
    fr <- data.frame(y = y, comorbid = comorbid, group_dm = df_family$group_dm)
    fr <- fr[stats::complete.cases(fr), , drop = FALSE]
    ols <- tryCatch(stats::lm(y ~ comorbid + group_dm, data = fr), error = function(e) NULL)
    ols_beta <- NA_real_; ols_lo <- NA_real_; ols_hi <- NA_real_; ols_p <- NA_real_
    if (!is.null(ols)) {
      sm <- summary(ols)$coefficients
      if ("comorbid" %in% rownames(sm)) {
        ols_beta <- unname(sm["comorbid", "Estimate"])
        ols_p <- unname(sm["comorbid", "Pr(>|t|)"])
        ci <- tryCatch(stats::confint(ols, "comorbid"), error = function(e) NULL)
        if (!is.null(ci)) { ols_lo <- ci[1L]; ols_hi <- ci[2L] }
      }
    }

    dci <- mc_cohens_d_ci(y, comorbid)
    data.frame(
      outcome = oc,
      n_komorbid_var = d1$n, ort_komorbid_var = d1$ortalama,
      medyan_komorbid_var = d1$medyan, sd_komorbid_var = d1$sd,
      n_komorbid_yok = d0$n, ort_komorbid_yok = d0$ortalama,
      medyan_komorbid_yok = d0$medyan, sd_komorbid_yok = d0$sd,
      welch_t = if (!is.null(tt)) unname(tt$statistic) else NA_real_,
      welch_df = if (!is.null(tt)) unname(tt$parameter) else NA_real_,
      welch_p = if (!is.null(tt)) unname(tt$p.value) else NA_real_,
      cohen_d = dci$d, d_ci_low = dci$ci_low, d_ci_high = dci$ci_high,
      ols_comorbid_beta = ols_beta, ols_ci_low = ols_lo, ols_ci_high = ols_hi,
      ols_comorbid_p = ols_p,
      not = "kesitsel; ters-yon (depresyon->daha cok bildirilen hastalik) acik",
      tier = "C",
      statu = mc_evidence_status(),
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)
  # Holm KISIM icinde (Welch p uzerinde, 5 karsilastirma)
  out$welch_p_holm <- stats::p.adjust(out$welch_p, method = "holm")
  out
}

# 104 basit aracilik: any_comorbid -> beck_total -> embu_p_{sicaklik,reddetme}
mc_comorbid_mediation <- function(df_family, n_boot = 1000L, seed = 20260708L) {
  df_family <- mc_ensure_group_dm(df_family)
  status_stub <- function(outcome, status) {
    data.frame(
      outcome_subscale = outcome, status = status,
      effect = NA_character_, estimate = NA_real_,
      ci_low = NA_real_, ci_high = NA_real_, n = NA_integer_,
      ci_type = "bca.simple", n_boot = n_boot,
      not = "kesitsel aracilik = zayif nedensel iddia; korelasyonel dil",
      tier = "C", statu = mc_evidence_status(), stringsAsFactors = FALSE
    )
  }
  outcomes <- c("sicaklik", "reddetme")
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(do.call(rbind, lapply(outcomes, status_stub, status = "lavaan_unavailable")))
  }
  needed_base <- c("anne_hastalik_kategori_sayisi", "beck_total", "group_dm")
  mc_require_columns(df_family, needed_base, "104 aracilik")

  rows <- list()
  for (oc in outcomes) {
    y_col <- paste0("embu_p_", oc, "_mean")
    if (!y_col %in% names(df_family)) {
      rows[[oc]] <- status_stub(oc, "missing_outcome"); next
    }
    dat <- data.frame(
      comorbid = mc_binary_from_count(df_family$anne_hastalik_kategori_sayisi),
      beck_total = suppressWarnings(as.numeric(df_family$beck_total)),
      y = suppressWarnings(as.numeric(df_family[[y_col]])),
      group_dm = df_family$group_dm
    )
    dat <- dat[stats::complete.cases(dat), , drop = FALSE]
    if (nrow(dat) < 30L) { rows[[oc]] <- status_stub(oc, "insufficient_n"); next }

    model <- paste0(
      "beck_total ~ a*comorbid + group_dm\n",
      "y ~ b*beck_total + cprime*comorbid + group_dm\n",
      "indirect := a*b\n",
      "direct := cprime\n",
      "total := indirect + direct\n",
      "prop_mediated := indirect / (indirect + cprime)\n"
    )
    fit <- tryCatch(
      suppressWarnings(lavaan::sem(model, data = dat, estimator = "ML",
        se = "bootstrap", bootstrap = n_boot)),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      st <- status_stub(oc, paste0("error:", conditionMessage(fit))); rows[[oc]] <- st; next
    }
    pe <- tryCatch(
      lavaan::parameterEstimates(fit, boot.ci.type = "bca.simple"),
      error = function(e) NULL
    )
    if (is.null(pe)) { rows[[oc]] <- status_stub(oc, "pe_error"); next }
    keep <- pe[pe$label %in% c("a", "b", "cprime", "indirect", "direct",
      "total", "prop_mediated"), , drop = FALSE]
    rows[[oc]] <- data.frame(
      outcome_subscale = oc,
      status = "ok",
      effect = keep$label,
      estimate = keep$est,
      ci_low = keep$ci.lower,
      ci_high = keep$ci.upper,
      n = lavaan::lavInspect(fit, "ntotal"),
      ci_type = "bca.simple",
      n_boot = n_boot,
      not = "kesitsel aracilik = zayif nedensel iddia; korelasyonel dil",
      tier = "C",
      statu = mc_evidence_status(),
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ============================================================================
# 105 — Iki-gosterge maternal-distres yakinsamasi (Tier B-)
# ============================================================================

mc_antidep_group <- function(df_family) {
  mc_require_columns(df_family, c("group_f", "anne_antidepresan"),
    "105 antidepresan x grup")
  ad <- mc_binary_from_count(df_family$anne_antidepresan)
  g <- factor(as.character(df_family$group_f), levels = c("Kontrol", "DM"))
  tab <- table(antidepresan = factor(ad, levels = c(0L, 1L)), grup = g)

  chi <- tryCatch(stats::chisq.test(tab, correct = TRUE), error = function(e) NULL)
  ft <- tryCatch(stats::fisher.test(tab), error = function(e) NULL)
  cv <- NA_real_; cv_lo <- NA_real_; cv_hi <- NA_real_
  if (requireNamespace("effectsize", quietly = TRUE)) {
    cvr <- tryCatch(suppressWarnings(effectsize::cramers_v(tab, ci = 0.95)),
      error = function(e) NULL)
    if (!is.null(cvr)) {
      cv <- as.numeric(cvr$Cramers_v_adjusted %||% cvr$Cramers_v)
      cv_lo <- as.numeric(cvr$CI_low); cv_hi <- as.numeric(cvr$CI_high)
    }
  }
  n_dm_var <- sum(ad == 1L & g == "DM", na.rm = TRUE)
  n_dm_tot <- sum(!is.na(ad) & g == "DM")
  n_ko_var <- sum(ad == 1L & g == "Kontrol", na.rm = TRUE)
  n_ko_tot <- sum(!is.na(ad) & g == "Kontrol")
  data.frame(
    gosterge = "anne_antidepresan",
    dm_var = n_dm_var, dm_toplam = n_dm_tot,
    dm_pct = if (n_dm_tot > 0L) round(100 * n_dm_var / n_dm_tot, 2) else NA_real_,
    kontrol_var = n_ko_var, kontrol_toplam = n_ko_tot,
    kontrol_pct = if (n_ko_tot > 0L) round(100 * n_ko_var / n_ko_tot, 2) else NA_real_,
    n_toplam = n_dm_tot + n_ko_tot,
    chisq = if (!is.null(chi)) unname(chi$statistic) else NA_real_,
    chisq_df = if (!is.null(chi)) unname(chi$parameter) else NA_real_,
    chisq_p = if (!is.null(chi)) unname(chi$p.value) else NA_real_,
    fisher_p = if (!is.null(ft)) unname(ft$p.value) else NA_real_,
    cramers_v = cv, cramers_v_ci_low = cv_lo, cramers_v_ci_high = cv_hi,
    not = "maternal-distres yukunun grup-asimetrisi (Van Gampelaere ile tutarli)",
    tier = "B-",
    statu = mc_evidence_status(),
    stringsAsFactors = FALSE
  )
}

mc_distress_convergence <- function(df_family) {
  mc_require_columns(df_family, c("anne_antidepresan", "beck_total"),
    "105 distres yakinsama")
  ad <- mc_binary_from_count(df_family$anne_antidepresan)
  beck <- suppressWarnings(as.numeric(df_family$beck_total))

  # Nokta-biserial r (antidepresan <-> beck_total)
  ok <- !is.na(ad) & !is.na(beck)
  ct <- tryCatch(stats::cor.test(ad[ok], beck[ok]), error = function(e) NULL)
  r_pb <- if (!is.null(ct)) unname(ct$estimate) else NA_real_
  r_lo <- if (!is.null(ct) && !is.null(ct$conf.int)) ct$conf.int[1L] else NA_real_
  r_hi <- if (!is.null(ct) && !is.null(ct$conf.int)) ct$conf.int[2L] else NA_real_

  # Iki-gosterge uyum: antidepresan vs beck klinik esik (>=17)
  beck_clin <- ifelse(is.na(beck), NA_integer_, as.integer(beck >= 17))
  ok2 <- !is.na(ad) & !is.na(beck_clin)
  tab <- table(antidepresan = factor(ad[ok2], levels = c(0L, 1L)),
    beck_klinik = factor(beck_clin[ok2], levels = c(0L, 1L)))
  # Cohen's kappa
  kappa_val <- NA_real_
  if (requireNamespace("irr", quietly = TRUE) && sum(ok2) >= 5L) {
    kp <- tryCatch(irr::kappa2(cbind(ad[ok2], beck_clin[ok2])),
      error = function(e) NULL)
    if (!is.null(kp)) kappa_val <- unname(kp$value)
  }
  # Phi katsayisi (2x2)
  phi_val <- NA_real_
  if (all(dim(tab) == c(2L, 2L))) {
    a <- tab[1, 1]; b <- tab[1, 2]; c <- tab[2, 1]; d <- tab[2, 2]
    denom <- sqrt((a + b) * (c + d) * (a + c) * (b + d))
    if (denom > 0) phi_val <- (a * d - b * c) / denom
  }

  data.frame(
    metrik = c("nokta_biserial_r", "cohen_kappa", "phi"),
    deger = c(r_pb, kappa_val, phi_val),
    ci_low = c(r_lo, NA_real_, NA_real_),
    ci_high = c(r_hi, NA_real_, NA_real_),
    n = c(sum(ok), sum(ok2), sum(ok2)),
    not = c(
      "antidepresan <-> beck_total; her iki gosterge de anne oz-bildirimi -> ortak-yontem varyansi",
      "antidepresan vs beck klinik esik (>=17) uyum",
      "2x2 phi; formatif etiket (latent distres tek-gostergeye iner)"
    ),
    tier = "B-",
    statu = mc_evidence_status(),
    stringsAsFactors = FALSE
  )
}

# ============================================================================
# 106 — Es/baba & aile saglik yuku + negatif kontrol (Tier C)
# ============================================================================

mc_negative_control_prepare <- function(df_family, df_long_scored) {
  df_family <- mc_ensure_group_dm(df_family)
  mc_require_columns(df_family,
    c("aile_no", "es_hastalik_kategori_sayisi", "anne_hastalik_kategori_sayisi"),
    "106 negatif kontrol (family)")
  mc_require_columns(df_long_scored, c("aile_no"), "106 negatif kontrol (long)")

  fam <- data.frame(
    aile_no = df_family$aile_no,
    es_any_comorbid = mc_binary_from_count(df_family$es_hastalik_kategori_sayisi),
    aile_toplam_yuk = suppressWarnings(as.numeric(df_family$anne_hastalik_kategori_sayisi)) +
      suppressWarnings(as.numeric(df_family$es_hastalik_kategori_sayisi)),
    stringsAsFactors = FALSE
  )
  merged <- merge(df_long_scored, fam, by = "aile_no", all.x = TRUE, all.y = FALSE)
  merged
}

mc_negative_control_lme <- function(df_family, df_long_scored,
                                    outcomes = mc_embu_p_outcomes()) {
  merged <- mc_negative_control_prepare(df_family, df_long_scored)
  status_stub <- function(sub, model_type, status) {
    data.frame(
      outcome_subscale = sub, model = model_type, status = status,
      beta = NA_real_, ci_low = NA_real_, ci_high = NA_real_, p = NA_real_,
      n_obs = NA_integer_, n_aile = NA_integer_,
      not = "negatif kontrol: sifira yakin beklenti (Goodman-Gotlib baba-moderatoru)",
      tier = "C", statu = mc_evidence_status(), stringsAsFactors = FALSE
    )
  }
  have_lme <- requireNamespace("lme4", quietly = TRUE) &&
    requireNamespace("lmerTest", quietly = TRUE)

  fit_one <- function(sub, use_covariate) {
    model_type <- if (use_covariate) "duyarlilik_toplam_yuk" else "temel"
    y_col <- paste0("embu_c_", sub, "_mean")
    if (!y_col %in% names(merged)) return(status_stub(sub, model_type, "missing_outcome"))
    dat <- data.frame(
      y = suppressWarnings(as.numeric(merged[[y_col]])),
      es_any_comorbid = merged$es_any_comorbid,
      aile_toplam_yuk = merged$aile_toplam_yuk,
      aile_no = factor(merged$aile_no)
    )
    dat <- dat[stats::complete.cases(dat), , drop = FALSE]
    if (nrow(dat) < 20L || length(unique(dat$aile_no)) < 10L) {
      return(status_stub(sub, model_type, "insufficient_n"))
    }
    if (!have_lme) return(status_stub(sub, model_type, "lme4_unavailable"))
    form <- if (use_covariate) {
      y ~ es_any_comorbid + aile_toplam_yuk + (1 | aile_no)
    } else {
      y ~ es_any_comorbid + (1 | aile_no)
    }
    fit <- tryCatch(
      suppressWarnings(suppressMessages(
        lmerTest::lmer(form, data = dat, REML = TRUE,
          control = lme4::lmerControl(calc.derivs = FALSE)))),
      error = function(e) e
    )
    if (inherits(fit, "error")) return(status_stub(sub, model_type, "fit_error"))
    sm <- summary(fit)$coefficients
    if (!"es_any_comorbid" %in% rownames(sm)) {
      return(status_stub(sub, model_type, "no_term"))
    }
    beta <- unname(sm["es_any_comorbid", "Estimate"])
    se <- unname(sm["es_any_comorbid", "Std. Error"])
    pval <- unname(sm["es_any_comorbid", "Pr(>|t|)"])
    data.frame(
      outcome_subscale = sub, model = model_type, status = "ok",
      beta = beta, ci_low = beta - 1.96 * se, ci_high = beta + 1.96 * se,
      p = pval,
      n_obs = nrow(dat), n_aile = length(unique(dat$aile_no)),
      not = "negatif kontrol: sifira yakin beklenti (Goodman-Gotlib baba-moderatoru)",
      tier = "C", statu = mc_evidence_status(), stringsAsFactors = FALSE
    )
  }

  base_rows <- lapply(outcomes, fit_one, use_covariate = FALSE)
  sens_rows <- lapply(outcomes, fit_one, use_covariate = TRUE)
  out <- do.call(rbind, c(base_rows, sens_rows))
  # Holm KISIM icinde: yalniz temel modelin p-degerleri uzerinde
  out$p_holm <- NA_real_
  base_idx <- out$model == "temel" & out$status == "ok"
  if (any(base_idx)) {
    out$p_holm[base_idx] <- stats::p.adjust(out$p[base_idx], method = "holm")
  }
  out
}

# 106 TOST: es_any_comorbid <-> aile-ortalama EMBU-C nokta-biserial, SESOI |r|=.10
mc_negative_control_tost <- function(df_family, df_long_scored,
                                     outcomes = mc_embu_p_outcomes(),
                                     sesoi_r = 0.10) {
  df_family <- mc_ensure_group_dm(df_family)
  fam <- data.frame(
    aile_no = df_family$aile_no,
    es_any_comorbid = mc_binary_from_count(df_family$es_hastalik_kategori_sayisi),
    stringsAsFactors = FALSE
  )
  have_tost <- requireNamespace("TOSTER", quietly = TRUE)
  rows <- lapply(outcomes, function(sub) {
    y_col <- paste0("embu_c_", sub, "_mean")
    stub <- data.frame(
      outcome_subscale = sub, status = "insufficient",
      r = NA_real_, r_ci_low = NA_real_, r_ci_high = NA_real_,
      sesoi_r = sesoi_r, tost_p = NA_real_, tost_karar = NA_character_,
      n = NA_integer_, tier = "C", statu = mc_evidence_status(),
      stringsAsFactors = FALSE
    )
    if (!y_col %in% names(df_long_scored)) { stub$status <- "missing_outcome"; return(stub) }
    agg <- stats::aggregate(
      suppressWarnings(as.numeric(df_long_scored[[y_col]])),
      by = list(aile_no = df_long_scored$aile_no),
      FUN = function(v) mean(v, na.rm = TRUE)
    )
    names(agg)[2L] <- "child_mean"
    agg$child_mean[is.nan(agg$child_mean)] <- NA_real_
    m <- merge(fam, agg, by = "aile_no", all = FALSE)
    m <- m[!is.na(m$es_any_comorbid) & !is.na(m$child_mean), , drop = FALSE]
    if (nrow(m) < 20L) { stub$n <- nrow(m); return(stub) }
    if (!have_tost) {
      ct <- tryCatch(stats::cor.test(m$es_any_comorbid, m$child_mean), error = function(e) NULL)
      stub$status <- "tost_unavailable"
      if (!is.null(ct)) {
        stub$r <- unname(ct$estimate); stub$r_ci_low <- ct$conf.int[1L]
        stub$r_ci_high <- ct$conf.int[2L]
      }
      stub$n <- nrow(m); return(stub)
    }
    res <- tryCatch(
      suppressWarnings(suppressMessages(TOSTER::z_cor_test(
        m$es_any_comorbid, m$child_mean,
        alternative = "equivalence", null = sesoi_r))),
      error = function(e) e
    )
    if (inherits(res, "error")) { stub$status <- "tost_error"; stub$n <- nrow(m); return(stub) }
    tost_p <- unname(res$p.value)
    karar <- if (!is.na(tost_p) && tost_p < 0.05) "Esdeger (|r|<.10)" else "Belirsiz"
    data.frame(
      outcome_subscale = sub, status = "ok",
      r = unname(res$estimate),
      r_ci_low = if (!is.null(res$conf.int)) res$conf.int[1L] else NA_real_,
      r_ci_high = if (!is.null(res$conf.int)) res$conf.int[2L] else NA_real_,
      sesoi_r = sesoi_r, tost_p = tost_p, tost_karar = karar,
      n = nrow(m), tier = "C", statu = mc_evidence_status(),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

# ============================================================================
# Pipeline sarici
# ============================================================================

run_phase3_maternal_comorbidity_pipeline <- function(df_family_ses, df_long_scored,
                                                     mediation_boot = 1000L,
                                                     sesoi_r = 0.10,
                                                     seed = 20260708L) {
  set.seed(seed)
  df_family_ses <- mc_ensure_group_dm(df_family_ses)

  autoimmune_prevalence <- tryCatch(mc_autoimmune_prevalence(df_family_ses),
    error = function(e) data.frame(hata = conditionMessage(e), stringsAsFactors = FALSE))
  comorbid_binary_effects <- tryCatch(mc_binary_comorbid_effects(df_family_ses),
    error = function(e) data.frame(hata = conditionMessage(e), stringsAsFactors = FALSE))
  comorbid_mediation <- tryCatch(
    mc_comorbid_mediation(df_family_ses, n_boot = mediation_boot, seed = seed),
    error = function(e) data.frame(hata = conditionMessage(e), stringsAsFactors = FALSE))
  antidep_group <- tryCatch(mc_antidep_group(df_family_ses),
    error = function(e) data.frame(hata = conditionMessage(e), stringsAsFactors = FALSE))
  distress_convergence <- tryCatch(mc_distress_convergence(df_family_ses),
    error = function(e) data.frame(hata = conditionMessage(e), stringsAsFactors = FALSE))
  negative_control <- tryCatch(mc_negative_control_lme(df_family_ses, df_long_scored),
    error = function(e) data.frame(hata = conditionMessage(e), stringsAsFactors = FALSE))
  negative_control_tost <- tryCatch(
    mc_negative_control_tost(df_family_ses, df_long_scored, sesoi_r = sesoi_r),
    error = function(e) data.frame(hata = conditionMessage(e), stringsAsFactors = FALSE))

  target_summary <- data.frame(
    analysis = "phase3_maternal_comorbidity",
    kisim = "KISIM XXXVIII (103-106)",
    mediation_boot = mediation_boot,
    sesoi_r = sesoi_r,
    holm = "KISIM icinde (104 Welch x5; 106 temel lme4 x4)",
    kanit_kategorisi = mc_evidence_status(),
    sapma_tipi = "Tip 3 (Faz III SAP KISIM XXXVIII/103-106)",
    reference_doc = "06-sap-faz3-ek-plan.md v0.3",
    stringsAsFactors = FALSE
  )

  list(
    autoimmune_prevalence = autoimmune_prevalence,
    comorbid_binary_effects = comorbid_binary_effects,
    comorbid_mediation = comorbid_mediation,
    antidep_group = antidep_group,
    distress_convergence = distress_convergence,
    negative_control = negative_control,
    negative_control_tost = negative_control_tost,
    target_summary = target_summary
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
