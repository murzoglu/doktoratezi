# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXIX (§107-109)
# Aile Yapisi ve Kardes Konstelasyonu
#
# Bu modul YALNIZ saf fonksiyon icerir (dosya I/O YOK). Kanonik CSV'lere yazma
# yoktur; yukleme runner uzerinden R/01_io.R ile yapilir. Tum ciktilar agregat
# istatistiktir; satir-duzeyi katilimci verisi hicbir tabloya dokulmez.
#
# §107 [Tier D — betimsel]: es_sag / medeni_durum tek-ebeveyn sayimlari.
#   Moderasyon TANIMSIZ (Amato-Keith kucuk etki x near-zero alt-grup). Yalniz
#   betimsel; hicbir modele kovaryat olarak girmez.
#
# §108 [Tier B]: Dogum sirasi & konstelasyon -> EMBU-C.
#   (a) BIRINCIL: within-family kontrast (aile-sabit-etki mantigi) — aile icinde
#       indeks-kardes EMBU-C farkinin dogum-sirasi farki ve yas farkiyla iliskisi.
#       Yas kontrolu ZORUNLU. Between-family karistiricilar (sibship, SES) fark
#       alma ile otomatik dusurulur (Rohrer/Damian yontem dersi).
#   (b) Ana etki: cocuk_sayisi (kaynak-seyrelme; Downey/Hertwig) -> EMBU-C
#       sicaklik/asiri-koruma (long lme4 + cocuk_yas_z).
#   Coklu-karsilastirma FDR (BH) bu paragrafta. Birth-order etkileri literaturde
#   minik (Rohrer 2015) -> kucuk etki + genis GA beklentisi.
#
# §109 [Tier B]: Kardes SRQ diadik KARSILIKLILIK (reciprocity/mutuality).
#   Her SRQ ust-boyutu (warmth, status, conflict, rivalry) icin:
#   - intrapair korelasyon (srq_ho_X vs srq_sib_ho_X) + %95 GA + TOST(|r|=.10);
#   - Kenny-Mohr-Levesque diadik varyans ayrisimi: duad-ortalamasi (common fate)
#     varyansi vs duad-ici fark varyansi oranlari;
#   - Ayirt-edilebilirlik: indeks-vs-kardes ortalama farki (eslesmis t + Cohen dz);
#   - Uzanti: same_sex moderasyonu (Fisher z korelasyon-farki) + age_gap
#     dogrusal-olmayan (poly(age_gap,2), lm).
#   ⚠️ "SRM" (Social Relations Model) TERIMI KULLANILMAZ — round-robin (kisi basi
#   >=3-4 partner) gerektirir; burada YALNIZ diadik mutekabiliyet (Kenny-Mohr-
#   Levesque 2001 varyans ayristirmasi).

# ---------------------------------------------------------------------------
# Sabitler ve yardimcilar
# ---------------------------------------------------------------------------

fam_struct_status_label <- function() "[KESIFSEL - POST-HOC]"

fam_struct_embu_subscales <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

fam_struct_srq_dims <- function() {
  c("warmth", "status", "conflict", "rivalry")
}

fam_struct_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s eksik kolon(lar): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

fam_struct_num <- function(x) {
  suppressWarnings(as.numeric(as.character(x)))
}

fam_struct_scale <- function(x) {
  x <- fam_struct_num(x)
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

# Bir surekli vektorun ortalama + medyan + n (rapor kurali: her ikisi de).
fam_struct_desc <- function(x) {
  x <- fam_struct_num(x)
  obs <- x[!is.na(x)]
  list(
    n = length(obs),
    mean = if (length(obs) > 0L) mean(obs) else NA_real_,
    median = if (length(obs) > 0L) stats::median(obs) else NA_real_,
    sd = if (length(obs) > 1L) stats::sd(obs) else NA_real_
  )
}

# Korelasyon esdegerlik testi (TOST) — Fisher-z tabanli, SESOI |r| = .10.
# Null iddialar (kardes-uyumu / buffering) icin: non-significant != "etki yok".
# TOSTER paketi mevcutsa dogrulama amacli kullanilabilir; buradaki uygulama
# TOSTER::TOSTr ile ozdes Fisher-z prosedurudur (versiyon-bagimsiz).
fam_struct_tost_r <- function(r, n, sesoi = 0.10, alpha = 0.05) {
  if (is.na(r) || is.na(n) || n < 5L || abs(r) >= 1) {
    return(list(p = NA_real_, decision = NA_character_, stat_lower = NA_real_, stat_upper = NA_real_))
  }
  z <- atanh(r)
  se <- 1 / sqrt(n - 3)
  z_lower <- atanh(-sesoi)
  z_upper <- atanh(sesoi)
  # Alt-sinir testi H0: rho <= -SESOI  (red = rho > -SESOI)
  stat_lower <- (z - z_lower) / se
  p_lower <- stats::pnorm(stat_lower, lower.tail = FALSE)
  # Ust-sinir testi H0: rho >= +SESOI  (red = rho < +SESOI)
  stat_upper <- (z - z_upper) / se
  p_upper <- stats::pnorm(stat_upper, lower.tail = TRUE)
  p_tost <- max(p_lower, p_upper)
  list(
    p = p_tost,
    decision = if (p_tost < alpha) "esdeger(|r|<SESOI)" else "esdeger_degil",
    stat_lower = stat_lower,
    stat_upper = stat_upper
  )
}

# ---------------------------------------------------------------------------
# §107 — Tek-ebeveyn / baba yokluğu betimsel (Tier D)
# ---------------------------------------------------------------------------

fam_struct_single_parent_descriptive <- function(df_family) {
  fam_struct_require_columns(df_family, c("medeni_durum", "es_sag", "group"),
    "§107 tek-ebeveyn betimsel")

  md <- fam_struct_num(df_family$medeni_durum)
  es <- fam_struct_num(df_family$es_sag)
  grp <- as.character(df_family$group)
  n_total <- nrow(df_family)

  # Tek-ebeveyn gostergesi: dul (es_sag == 0) VEYA bosanmis (medeni_durum == 2).
  single <- (!is.na(es) & es == 0) | (!is.na(md) & md == 2)

  count_row <- function(gosterge, mask, aciklama) {
    data.frame(
      gosterge = gosterge,
      n = sum(mask, na.rm = TRUE),
      n_dm = sum(mask & grp == "DM", na.rm = TRUE),
      n_kontrol = sum(mask & grp == "Kontrol", na.rm = TRUE),
      yuzde = round(100 * sum(mask, na.rm = TRUE) / n_total, 2),
      aciklama = aciklama,
      statu = fam_struct_status_label(),
      stringsAsFactors = FALSE
    )
  }

  rows <- list(
    count_row("medeni_durum=0 (evli)", !is.na(md) & md == 0, "Cift-ebeveyn referans"),
    count_row("medeni_durum=2 (bosanmis)", !is.na(md) & md == 2, "Tek-ebeveyn bileseni (bosanma)"),
    count_row("es_sag=0 (es vefat/dul)", !is.na(es) & es == 0, "Tek-ebeveyn bileseni (dul)"),
    count_row("tek_ebeveyn (birlesik)", single,
      paste0("Moderasyon YAPILAMAZ: tek-ebeveyn near-constant alt-grup; ",
        "Amato-Keith kucuk etki x near-zero alt-grup = tanimsiz etkilesim. ",
        "H1/H3 modellerine kovaryat olarak dahi girmez. Yalniz betimsel denge tablosu.")),
    count_row("cift_ebeveyn (birlesik)", !single,
      "Referans grup (dul/bosanma disi)")
  )

  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §108 (a) — Within-family kontrast (BIRINCIL, aile-sabit-etki mantigi)
# ---------------------------------------------------------------------------
# Aile icinde: d_X = embu_c_idx_X_mean - embu_c_sib_X_mean
# Yordayicilar: dogum_sirasi_farki = katilimci_cocuk_sirasi - kardes_sirasi
#               yas_farki = cocuk_yas - kardes_yas   (KONTROL — zorunlu)
# Model: lm(d_X ~ dogum_sirasi_farki + yas_farki). Fark alma between-family
# karistiricilarini (sibship, SES) dusurdugu icin ekstra kovaryat gerekmez.

fam_struct_birth_order_within <- function(df_family, subscales = fam_struct_embu_subscales()) {
  needed <- c(
    "katilimci_cocuk_sirasi", "kardes_sirasi", "cocuk_yas", "kardes_yas",
    paste0("embu_c_idx_", subscales, "_mean"),
    paste0("embu_c_sib_", subscales, "_mean")
  )
  fam_struct_require_columns(df_family, needed, "§108a within-family kontrast")

  bo_diff <- fam_struct_num(df_family$katilimci_cocuk_sirasi) - fam_struct_num(df_family$kardes_sirasi)
  age_diff <- fam_struct_num(df_family$cocuk_yas) - fam_struct_num(df_family$kardes_yas)

  term_labels <- c(bo = "dogum_sirasi_farki", age = "yas_farki")
  term_roles <- c(bo = "yordayici", age = "yas_kontrolu")

  rows <- list()
  for (sub in subscales) {
    idx <- fam_struct_num(df_family[[paste0("embu_c_idx_", sub, "_mean")]])
    sib <- fam_struct_num(df_family[[paste0("embu_c_sib_", sub, "_mean")]])
    dd <- data.frame(d = idx - sib, bo = bo_diff, age = age_diff)
    dd <- dd[stats::complete.cases(dd), , drop = FALSE]
    n <- nrow(dd)
    d_desc <- fam_struct_desc(dd$d)

    if (n < 10L) {
      rows[[length(rows) + 1L]] <- data.frame(
        boyut = sub, terim = "model", rol = NA_character_, n = n,
        ort_fark = d_desc$mean, medyan_fark = d_desc$median,
        tahmin = NA_real_, se = NA_real_, ci_alt = NA_real_, ci_ust = NA_real_,
        std_beta = NA_real_, std_ci_alt = NA_real_, std_ci_ust = NA_real_,
        t = NA_real_, p = NA_real_, statu_kosum = "yetersiz_n",
        aciklama = "n<10: within-family kontrast tahmini yapilmadi",
        statu = fam_struct_status_label(), stringsAsFactors = FALSE
      )
      next
    }

    fit <- stats::lm(d ~ bo + age, data = dd)
    sm <- summary(fit)$coefficients
    ci <- stats::confint(fit)

    # Standardize edilmis model -> std beta (etki buyuklugu)
    ddz <- data.frame(
      d = fam_struct_scale(dd$d),
      bo = fam_struct_scale(dd$bo),
      age = fam_struct_scale(dd$age)
    )
    std_ok <- all(vapply(ddz, function(v) sum(!is.na(v)) > 2L, logical(1)))
    fit_z <- if (std_ok) tryCatch(stats::lm(d ~ bo + age, data = ddz), error = function(e) NULL) else NULL
    ci_z <- if (!is.null(fit_z)) tryCatch(stats::confint(fit_z), error = function(e) NULL) else NULL

    for (term in c("bo", "age")) {
      std_beta <- if (!is.null(fit_z)) unname(stats::coef(fit_z)[term]) else NA_real_
      std_lo <- if (!is.null(ci_z)) ci_z[term, 1] else NA_real_
      std_hi <- if (!is.null(ci_z)) ci_z[term, 2] else NA_real_
      rows[[length(rows) + 1L]] <- data.frame(
        boyut = sub,
        terim = unname(term_labels[term]),
        rol = unname(term_roles[term]),
        n = n,
        ort_fark = d_desc$mean,
        medyan_fark = d_desc$median,
        tahmin = unname(stats::coef(fit)[term]),
        se = sm[term, "Std. Error"],
        ci_alt = ci[term, 1],
        ci_ust = ci[term, 2],
        std_beta = std_beta,
        std_ci_alt = std_lo,
        std_ci_ust = std_hi,
        t = sm[term, "t value"],
        p = sm[term, "Pr(>|t|)"],
        statu_kosum = "ok",
        aciklama = if (term == "bo") {
          "Birth-order within-family; Rohrer 2015: minik etki + genis GA beklentisi"
        } else {
          "Yas kontrolu (zorunlu); confound dogum-sirasi<->yas"
        },
        statu = fam_struct_status_label(),
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §108 (b) — Sibship kaynak-seyrelme (long lme4 + cocuk_yas_z)
# ---------------------------------------------------------------------------
# embu_c_X_mean ~ cocuk_sayisi_z + cocuk_yas_z + (1 | aile_no_f)
# X in {sicaklik (warmth), asiri_koruma (overprotection)}. Yas kontrolu zorunlu.

fam_struct_sibship_dilution <- function(df_long, df_family,
                                        outcomes = c("sicaklik", "asiri_koruma")) {
  fam_struct_require_columns(df_family, c("aile_no", "cocuk_sayisi"),
    "§108b dilution (family)")
  fam_struct_require_columns(df_long,
    c("aile_no", "aile_no_f", "cocuk_yas", paste0("embu_c_", outcomes, "_mean")),
    "§108b dilution (long)")

  # cocuk_sayisi'yi aile bazinda family'den lookup ile al (long'da ayni adli kolon
  # bulunabildigi icin merge yerine match kullaniyoruz — canonical family kaynak).
  fam_small <- unique(df_family[, c("aile_no", "cocuk_sayisi")])
  cs_lookup <- stats::setNames(fam_struct_num(fam_small$cocuk_sayisi), as.character(fam_small$aile_no))
  long <- df_long
  long$cocuk_sayisi_fam <- unname(cs_lookup[as.character(long$aile_no)])
  long$cocuk_sayisi_z <- fam_struct_scale(long$cocuk_sayisi_fam)
  long$cocuk_yas_z <- fam_struct_scale(long$cocuk_yas)

  have_lme4 <- requireNamespace("lme4", quietly = TRUE)
  have_lmerTest <- requireNamespace("lmerTest", quietly = TRUE)

  rows <- list()
  for (out in outcomes) {
    ycol <- paste0("embu_c_", out, "_mean")
    dd <- data.frame(
      y = fam_struct_num(long[[ycol]]),
      y_z = fam_struct_scale(long[[ycol]]),
      cs = long$cocuk_sayisi_z,
      cs_raw = long$cocuk_sayisi_fam,
      ya = long$cocuk_yas_z,
      aile = factor(as.character(long$aile_no_f))
    )
    dd <- dd[stats::complete.cases(dd[, c("y", "y_z", "cs", "ya", "aile")]), , drop = FALSE]
    dd$aile <- droplevels(dd$aile)
    n_obs <- nrow(dd)
    n_grp <- nlevels(dd$aile)
    y_desc <- fam_struct_desc(dd$y)
    cs_desc <- fam_struct_desc(dd$cs_raw)

    base_row <- function(status, est = NA_real_, se = NA_real_, ci_lo = NA_real_,
                         ci_hi = NA_real_, std_beta = NA_real_, tval = NA_real_,
                         dfree = NA_real_, p = NA_real_, method = NA_character_) {
      data.frame(
        boyut = out, yordayici = "cocuk_sayisi_z",
        n_gozlem = n_obs, n_aile = n_grp,
        ort_embu_c = y_desc$mean, medyan_embu_c = y_desc$median,
        ort_cocuk_sayisi = cs_desc$mean, medyan_cocuk_sayisi = cs_desc$median,
        tahmin = est, se = se, ci_alt = ci_lo, ci_ust = ci_hi,
        std_beta = std_beta, t = tval, df = dfree, p = p,
        p_yontemi = method, statu_kosum = status,
        aciklama = "Kaynak-seyrelme (Downey/Hertwig); yas kontrolu (cocuk_yas_z) zorunlu",
        statu = fam_struct_status_label(), stringsAsFactors = FALSE
      )
    }

    if (!have_lme4 || n_obs < 20L || n_grp < 10L) {
      rows[[length(rows) + 1L]] <- base_row(
        if (!have_lme4) "lme4_yok" else "yetersiz_n"
      )
      next
    }

    fit_fun <- function(formula, data) {
      if (have_lmerTest) {
        lmerTest::lmer(formula, data = data, REML = TRUE)
      } else {
        lme4::lmer(formula, data = data, REML = TRUE)
      }
    }
    fit <- tryCatch(
      suppressMessages(suppressWarnings(fit_fun(y ~ cs + ya + (1 | aile), data = dd))),
      error = function(e) e
    )
    if (inherits(fit, "error")) {
      rows[[length(rows) + 1L]] <- base_row(paste0("hata:", conditionMessage(fit)))
      next
    }
    fit_z <- tryCatch(
      suppressMessages(suppressWarnings(fit_fun(y_z ~ cs + ya + (1 | aile), data = dd))),
      error = function(e) NULL
    )

    coefs <- summary(fit)$coefficients
    est <- coefs["cs", "Estimate"]
    se <- coefs["cs", "Std. Error"]
    tval <- coefs["cs", grep("t value", colnames(coefs), fixed = TRUE)][1]
    if (have_lmerTest && "Pr(>|t|)" %in% colnames(coefs)) {
      p <- coefs["cs", "Pr(>|t|)"]
      dfree <- coefs["cs", "df"]
      method <- "Satterthwaite(lmerTest)"
    } else {
      p <- 2 * stats::pnorm(-abs(est / se))
      dfree <- NA_real_
      method <- "Wald-z(lme4)"
    }
    std_beta <- if (!is.null(fit_z)) summary(fit_z)$coefficients["cs", "Estimate"] else NA_real_

    rows[[length(rows) + 1L]] <- base_row(
      "ok", est = est, se = se,
      ci_lo = est - stats::qnorm(0.975) * se,
      ci_hi = est + stats::qnorm(0.975) * se,
      std_beta = std_beta, tval = tval, dfree = dfree, p = p, method = method
    )
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §109 — Diadik karsiliklilik: intrapair korelasyon + ayirt-edilebilirlik
# ---------------------------------------------------------------------------

fam_struct_reciprocity <- function(df_family, dims = fam_struct_srq_dims(), sesoi_r = 0.10) {
  needed <- c(paste0("srq_ho_", dims, "_mean"), paste0("srq_sib_ho_", dims, "_mean"))
  fam_struct_require_columns(df_family, needed, "§109 diadik karsiliklilik")

  rows <- list()
  for (dim in dims) {
    a <- fam_struct_num(df_family[[paste0("srq_ho_", dim, "_mean")]])       # indeks algisi
    b <- fam_struct_num(df_family[[paste0("srq_sib_ho_", dim, "_mean")]])   # kardes algisi
    ok <- !is.na(a) & !is.na(b)
    a <- a[ok]; b <- b[ok]; n <- length(a)
    a_desc <- fam_struct_desc(a); b_desc <- fam_struct_desc(b)
    diff <- a - b
    diff_desc <- fam_struct_desc(diff)

    if (n < 5L || stats::sd(a) == 0 || stats::sd(b) == 0) {
      rows[[length(rows) + 1L]] <- data.frame(
        boyut = dim, n = n,
        ort_indeks = a_desc$mean, medyan_indeks = a_desc$median,
        ort_kardes = b_desc$mean, medyan_kardes = b_desc$median,
        intrapair_r = NA_real_, r_ci_alt = NA_real_, r_ci_ust = NA_real_, r_p = NA_real_,
        ort_fark = diff_desc$mean, medyan_fark = diff_desc$median,
        t = NA_real_, t_df = NA_real_, t_p = NA_real_,
        cohen_dz = NA_real_, dz_ci_alt = NA_real_, dz_ci_ust = NA_real_,
        tost_p = NA_real_, tost_karar = NA_character_, sesoi_r = sesoi_r,
        statu_kosum = "yetersiz_n",
        aciklama = "Diadik mutekabiliyet (Kenny-Mohr-Levesque); SRM DEGIL",
        statu = fam_struct_status_label(), stringsAsFactors = FALSE
      )
      next
    }

    ct <- stats::cor.test(a, b)
    r <- unname(ct$estimate)
    r_ci <- ct$conf.int
    tt <- stats::t.test(a, b, paired = TRUE)
    dz <- mean(diff) / stats::sd(diff)
    se_dz <- sqrt(1 / n + dz^2 / (2 * n))
    tost <- fam_struct_tost_r(r, n, sesoi = sesoi_r)

    rows[[length(rows) + 1L]] <- data.frame(
      boyut = dim, n = n,
      ort_indeks = a_desc$mean, medyan_indeks = a_desc$median,
      ort_kardes = b_desc$mean, medyan_kardes = b_desc$median,
      intrapair_r = r, r_ci_alt = r_ci[1], r_ci_ust = r_ci[2], r_p = ct$p.value,
      ort_fark = diff_desc$mean, medyan_fark = diff_desc$median,
      t = unname(tt$statistic), t_df = unname(tt$parameter), t_p = tt$p.value,
      cohen_dz = dz, dz_ci_alt = dz - stats::qnorm(0.975) * se_dz,
      dz_ci_ust = dz + stats::qnorm(0.975) * se_dz,
      tost_p = tost$p, tost_karar = tost$decision, sesoi_r = sesoi_r,
      statu_kosum = "ok",
      aciklama = "Intrapair r + ayirt-edilebilirlik (eslesmis t + dz); diadik, SRM DEGIL",
      statu = fam_struct_status_label(), stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §109 — Kenny-Mohr-Levesque diadik varyans ayrisimi
# ---------------------------------------------------------------------------
# Duad-ortalamasi (common fate) varyansi vs duad-ici fark varyansi.
#   var_duad_ort  = Var((a + b) / 2)        [common fate / paylasilan]
#   var_duad_fark = Var((a - b) / 2)        [ayirt-edici / duad-ici]
#   oran_common_fate = var_duad_ort / (var_duad_ort + var_duad_fark)  in [0,1]
# Ayrica common/unique dekompozisyonu (a = C + U):
#   common_var = cov(a,b);  unique_var = mean(Var(a),Var(b)) - cov(a,b)
#   mutekabiliyet_orani = common_var / (common_var + unique_var)  in [-1,1]

fam_struct_variance_decomposition <- function(df_family, dims = fam_struct_srq_dims()) {
  needed <- c(paste0("srq_ho_", dims, "_mean"), paste0("srq_sib_ho_", dims, "_mean"))
  fam_struct_require_columns(df_family, needed, "§109 varyans ayrisimi")

  rows <- list()
  for (dim in dims) {
    a <- fam_struct_num(df_family[[paste0("srq_ho_", dim, "_mean")]])
    b <- fam_struct_num(df_family[[paste0("srq_sib_ho_", dim, "_mean")]])
    ok <- !is.na(a) & !is.na(b)
    a <- a[ok]; b <- b[ok]; n <- length(a)

    if (n < 5L) {
      rows[[length(rows) + 1L]] <- data.frame(
        boyut = dim, n = n,
        var_indeks = NA_real_, var_kardes = NA_real_, kovaryans = NA_real_,
        var_duad_ort = NA_real_, var_duad_fark = NA_real_,
        oran_common_fate = NA_real_, oran_duad_ici = NA_real_,
        common_var = NA_real_, unique_var = NA_real_, mutekabiliyet_orani = NA_real_,
        statu_kosum = "yetersiz_n",
        aciklama = "Kenny-Mohr-Levesque diadik varyans ayrisimi (SRM DEGIL)",
        statu = fam_struct_status_label(), stringsAsFactors = FALSE
      )
      next
    }

    var_a <- stats::var(a)
    var_b <- stats::var(b)
    cov_ab <- stats::cov(a, b)
    var_mean <- stats::var((a + b) / 2)
    var_hdiff <- stats::var((a - b) / 2)
    total <- var_mean + var_hdiff
    common_var <- cov_ab
    unique_var <- mean(c(var_a, var_b)) - cov_ab

    rows[[length(rows) + 1L]] <- data.frame(
      boyut = dim, n = n,
      var_indeks = var_a, var_kardes = var_b, kovaryans = cov_ab,
      var_duad_ort = var_mean, var_duad_fark = var_hdiff,
      oran_common_fate = if (total > 0) var_mean / total else NA_real_,
      oran_duad_ici = if (total > 0) var_hdiff / total else NA_real_,
      common_var = common_var, unique_var = unique_var,
      mutekabiliyet_orani = if ((common_var + unique_var) != 0) {
        common_var / (common_var + unique_var)
      } else {
        NA_real_
      },
      statu_kosum = "ok",
      aciklama = "Common fate (duad-ort) vs duad-ici fark varyansi; Kenny-Mohr-Levesque 2001",
      statu = fam_struct_status_label(), stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# §109 (uzanti) — same_sex moderasyonu (Fisher z) + age_gap dogrusal-olmayan
# ---------------------------------------------------------------------------

fam_struct_same_sex_age_gap <- function(df_family, dims = fam_struct_srq_dims()) {
  needed <- c(
    "katilimci_cocuk_cinsiyet", "kardes_cinsiyet", "cocuk_yas", "kardes_yas",
    paste0("srq_ho_", dims, "_mean"), paste0("srq_sib_ho_", dims, "_mean")
  )
  fam_struct_require_columns(df_family, needed, "§109 same_sex/age_gap uzanti")

  same_sex <- fam_struct_num(df_family$katilimci_cocuk_cinsiyet) ==
    fam_struct_num(df_family$kardes_cinsiyet)
  age_gap <- abs(fam_struct_num(df_family$cocuk_yas) - fam_struct_num(df_family$kardes_yas))

  make_row <- function(boyut, test, terim, n, tahmin, ci_alt, ci_ust,
                       istatistik, p, ek_bilgi, statu_kosum) {
    data.frame(
      boyut = boyut, test = test, terim = terim, n = n,
      tahmin = tahmin, ci_alt = ci_alt, ci_ust = ci_ust,
      istatistik = istatistik, p = p, ek_bilgi = ek_bilgi,
      statu_kosum = statu_kosum, statu = fam_struct_status_label(),
      stringsAsFactors = FALSE
    )
  }

  rows <- list()
  for (dim in dims) {
    a <- fam_struct_num(df_family[[paste0("srq_ho_", dim, "_mean")]])
    b <- fam_struct_num(df_family[[paste0("srq_sib_ho_", dim, "_mean")]])

    # --- same_sex: iki bagimsiz korelasyonun Fisher-z farki (Kim-McHale 2006) ---
    r_group <- function(mask) {
      m <- mask & !is.na(a) & !is.na(b)
      av <- a[m]; bv <- b[m]; ng <- length(av)
      if (ng < 5L || stats::sd(av) == 0 || stats::sd(bv) == 0) {
        return(list(r = NA_real_, n = ng))
      }
      list(r = stats::cor(av, bv), n = ng)
    }
    g_ayni <- r_group(same_sex %in% TRUE)
    g_farkli <- r_group(same_sex %in% FALSE)

    if (!is.na(g_ayni$r) && !is.na(g_farkli$r) && g_ayni$n > 3L && g_farkli$n > 3L) {
      z1 <- atanh(g_ayni$r); z2 <- atanh(g_farkli$r)
      se <- sqrt(1 / (g_ayni$n - 3) + 1 / (g_farkli$n - 3))
      zstat <- (z1 - z2) / se
      p <- 2 * stats::pnorm(-abs(zstat))
      rows[[length(rows) + 1L]] <- make_row(
        dim, "same_sex_fisher_z", "r_farki(Ayni_eksi_Farkli)",
        g_ayni$n + g_farkli$n, g_ayni$r - g_farkli$r, NA_real_, NA_real_,
        zstat, p,
        sprintf("r_ayni=%.3f (n=%d); r_farkli=%.3f (n=%d)",
          g_ayni$r, g_ayni$n, g_farkli$r, g_farkli$n),
        "ok"
      )
    } else {
      rows[[length(rows) + 1L]] <- make_row(
        dim, "same_sex_fisher_z", "r_farki(Ayni_eksi_Farkli)",
        g_ayni$n + g_farkli$n, NA_real_, NA_real_, NA_real_, NA_real_, NA_real_,
        sprintf("yetersiz_n: n_ayni=%d n_farkli=%d", g_ayni$n, g_farkli$n),
        "yetersiz_n"
      )
    }

    # --- age_gap dogrusal-olmayan: |a-b| ~ poly(age_gap, 2) ---
    dd <- data.frame(y = abs(a - b), ag = age_gap)
    dd <- dd[stats::complete.cases(dd), , drop = FALSE]
    n_ag <- nrow(dd)
    if (n_ag >= 15L && stats::sd(dd$ag) > 0 && length(unique(dd$ag)) >= 3L) {
      fit <- tryCatch(stats::lm(y ~ poly(ag, 2), data = dd), error = function(e) NULL)
      if (!is.null(fit)) {
        sm <- summary(fit)$coefficients
        ci <- tryCatch(stats::confint(fit), error = function(e) matrix(NA_real_, nrow(sm), 2))
        f <- summary(fit)$fstatistic
        model_p <- if (!is.null(f)) {
          stats::pf(f[1], f[2], f[3], lower.tail = FALSE)
        } else {
          NA_real_
        }
        for (k in c(2L, 3L)) {
          terim <- if (k == 2L) "lineer" else "kuadratik"
          rows[[length(rows) + 1L]] <- make_row(
            dim, "age_gap_poly", terim, n_ag,
            sm[k, "Estimate"], ci[k, 1], ci[k, 2],
            sm[k, "t value"], sm[k, "Pr(>|t|)"],
            "|indeks-kardes| ~ poly(age_gap,2)", "ok"
          )
        }
        rows[[length(rows) + 1L]] <- make_row(
          dim, "age_gap_poly", "model_overall", n_ag,
          summary(fit)$r.squared, NA_real_, NA_real_,
          if (!is.null(f)) unname(f[1]) else NA_real_, model_p,
          "R^2 + genel model F", "ok"
        )
      } else {
        rows[[length(rows) + 1L]] <- make_row(
          dim, "age_gap_poly", "model_overall", n_ag,
          NA_real_, NA_real_, NA_real_, NA_real_, NA_real_, "lm hata", "hata"
        )
      }
    } else {
      rows[[length(rows) + 1L]] <- make_row(
        dim, "age_gap_poly", "model_overall", n_ag,
        NA_real_, NA_real_, NA_real_, NA_real_, NA_real_,
        "yetersiz_n / yetersiz_varyans", "yetersiz_n"
      )
    }
  }
  do.call(rbind, rows)
}

# ---------------------------------------------------------------------------
# FDR (BH) — her paragraf kendi ailesi (KISIM'lar arasi birlestirme YOK)
# ---------------------------------------------------------------------------

fam_struct_fdr_table <- function(birth_within, sibship_dilution, same_sex_age_gap) {
  collect <- function(paragraf, test_adi, p) {
    keep <- !is.na(p)
    if (!any(keep)) {
      return(NULL)
    }
    data.frame(
      paragraf = paragraf,
      test_adi = test_adi[keep],
      p_ham = p[keep],
      stringsAsFactors = FALSE
    )
  }

  fam_list <- list()

  # §108 ailesi: within-family dogum_sirasi_farki katsayilari + dilution cocuk_sayisi
  if (!is.null(birth_within) && "terim" %in% names(birth_within)) {
    bw <- birth_within[birth_within$terim == "dogum_sirasi_farki" &
      birth_within$statu_kosum == "ok", , drop = FALSE]
    if (nrow(bw) > 0L) {
      fam_list[["108_bw"]] <- collect("§108",
        paste0("within_dogum_sirasi:", bw$boyut), bw$p)
    }
  }
  if (!is.null(sibship_dilution)) {
    sd_ok <- sibship_dilution[sibship_dilution$statu_kosum == "ok", , drop = FALSE]
    if (nrow(sd_ok) > 0L) {
      fam_list[["108_sd"]] <- collect("§108",
        paste0("dilution_cocuk_sayisi:", sd_ok$boyut), sd_ok$p)
    }
  }

  # §109 uzanti ailesi: same_sex Fisher z + age_gap kuadratik
  if (!is.null(same_sex_age_gap)) {
    ss <- same_sex_age_gap[same_sex_age_gap$test == "same_sex_fisher_z" &
      same_sex_age_gap$statu_kosum == "ok", , drop = FALSE]
    if (nrow(ss) > 0L) {
      fam_list[["109_ss"]] <- collect("§109_uzanti",
        paste0("same_sex_fisher_z:", ss$boyut), ss$p)
    }
    ag <- same_sex_age_gap[same_sex_age_gap$test == "age_gap_poly" &
      same_sex_age_gap$terim == "kuadratik" &
      same_sex_age_gap$statu_kosum == "ok", , drop = FALSE]
    if (nrow(ag) > 0L) {
      fam_list[["109_ag"]] <- collect("§109_uzanti",
        paste0("age_gap_kuadratik:", ag$boyut), ag$p)
    }
  }

  base <- do.call(rbind, fam_list)
  if (is.null(base) || nrow(base) == 0L) {
    return(data.frame(
      paragraf = character(), test_adi = character(), p_ham = numeric(),
      p_bh = numeric(), yontem = character(), statu = character(),
      stringsAsFactors = FALSE
    ))
  }

  # BH her paragraf-ailesi icinde ayri
  base$p_bh <- NA_real_
  for (par in unique(base$paragraf)) {
    idx <- base$paragraf == par
    base$p_bh[idx] <- stats::p.adjust(base$p_ham[idx], method = "BH")
  }
  base$yontem <- "BH(paragraf-ici)"
  base$statu <- fam_struct_status_label()
  rownames(base) <- NULL
  base
}

# ---------------------------------------------------------------------------
# Pipeline sarici (Faz II deseni)
# ---------------------------------------------------------------------------

run_phase3_family_structure_pipeline <- function(df_family_scored, df_long_scored,
                                                  subscales = fam_struct_embu_subscales(),
                                                  srq_dims = fam_struct_srq_dims(),
                                                  dilution_outcomes = c("sicaklik", "asiri_koruma"),
                                                  sesoi_r = 0.10) {
  single_parent <- fam_struct_single_parent_descriptive(df_family_scored)
  birth_within <- fam_struct_birth_order_within(df_family_scored, subscales = subscales)
  sibship_dilution <- fam_struct_sibship_dilution(df_long_scored, df_family_scored,
    outcomes = dilution_outcomes)
  reciprocity <- fam_struct_reciprocity(df_family_scored, dims = srq_dims, sesoi_r = sesoi_r)
  variance_decomp <- fam_struct_variance_decomposition(df_family_scored, dims = srq_dims)
  same_sex_age_gap <- fam_struct_same_sex_age_gap(df_family_scored, dims = srq_dims)
  fdr <- fam_struct_fdr_table(birth_within, sibship_dilution, same_sex_age_gap)

  target_summary <- data.frame(
    analiz = "phase3_family_structure_sibship",
    kisim = "KISIM XXXIX (§107-109)",
    n_aile = nrow(df_family_scored),
    n_single_parent = single_parent$n[single_parent$gosterge == "tek_ebeveyn (birlesik)"][1],
    sesoi_r = sesoi_r,
    kanit_kategorisi = fam_struct_status_label(),
    sapma_tipi = "Tip 3 (Faz III post-hoc genisletme)",
    reference_doc = "docs/analiz_planlari/06-sap-faz3-ek-plan.md v0.2/v0.3",
    srm_notu = "SRM adi KULLANILMAZ; yalniz diadik mutekabiliyet (Kenny-Mohr-Levesque 2001)",
    dil_notu = "Korelasyonel dil; nedensel dil yasak",
    stringsAsFactors = FALSE
  )

  list(
    single_parent_descriptive = single_parent,
    birth_order_within = birth_within,
    sibship_dilution = sibship_dilution,
    reciprocity_correlations = reciprocity,
    variance_decomposition = variance_decomp,
    same_sex_age_gap = same_sex_age_gap,
    fdr = fdr,
    target_summary = target_summary
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
