# [KESIFSEL - POST-HOC] Faz III SAP KISIM XXXVII (§100–102b)
# Sosyal Tabakalasma Genisletmesi (saf fonksiyon modulu — dosya I/O yok)
#
# Kapsam (SAP 06-sap-faz3-ek-plan.md satir 249–288):
#   §100  — EGP-3 sinif-gradyanli ebeveynlik (EMBU-P/C) + ISEI/SIOPS/EGP olcum-yarisi
#           (commonality + AIC) + ZORUNLU SIMPSON denetimi (havuzlanmis vs grup-ici).
#   §101  — Egitim-ekseni Diagonal Reference Model (Dref, gnm); meslek-DRM kimliklenemez
#           (§1.5-C2: aile_*08 = es_*08, 241/241). Egitim 3-duzeye daraltilir. Kesifsel.
#   §102  — Materyal yoksunluk faceti: hiyerarsik regresyon (blok-1 prestij edu_z+isei_z,
#           blok-2 material_z) + Beck-araci Aile-Stres-Modeli (deprivation=-material_z ->
#           beck_total -> EMBU-P; lavaan a·b, BCa bootstrap). ses_latent blok-1'de KULLANILMAZ.
#   §102b — Anne istihdami (calisma_durumu) × grup moderasyonu (aile OLS + long lme4);
#           null etkilesim icin TOST esdegerlik (SESOI |r|=.10, TOSTER).
#
# Yorumsal uyari (§1.5-C2): aile_egp7 = es_egp7 (baba sinifi) -> "baba-sinifi ->
#   anne-ebeveynlik" okumasi. Tum sonuc korelasyoneldir; nedensel dil kullanilmaz.
#   Holm coklu-karsilastirma duzeltmesi YALNIZ bu KISIM ici uygulanir.
#
# Yeniden-kullanilan altyapi: R/11 (edu_z, isei_z, material_z, ses_latent, egitim_fark,
#   cift_kazanc), R/10 (srq_ho_conflict_mean, embu_c_idx_*_mean), R/23 (mediation deseni).

# ============================================================================
# Sabitler ve yardimcilar
# ============================================================================

strat_evidence_status <- function() "[KESIFSEL - POST-HOC]"

strat_deviation_note <- function() "Tip 3 (Faz III SAP KISIM XXXVII/100-102b)"

strat_reference_doc <- function() "docs/analiz_planlari/06-sap-faz3-ek-plan.md"

strat_sesoi_r <- function() 0.10

strat_embu_p_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

strat_embu_p_col <- function(subscale) paste0("embu_p_", subscale, "_mean")
strat_embu_c_idx_col <- function(subscale) paste0("embu_c_idx_", subscale, "_mean")
strat_embu_c_long_col <- function(subscale) paste0("embu_c_", subscale, "_mean")

strat_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

# NA-duyarli z-skor (sonek _z); sabit ya da tek gozlem -> NA vektoru
strat_scale <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) {
    return(rep(NA_real_, length(x)))
  }
  (x - mean(x, na.rm = TRUE)) / s
}

# EGP-7 -> EGP-3: hizmet 1-2 / ara 3-5 / isci-rutin 6-7; yapisal NA korunur (22 aile)
strat_egp3_recode <- function(egp7) {
  v <- suppressWarnings(as.numeric(egp7))
  out <- cut(v, breaks = c(0, 2, 5, 7), labels = c("hizmet", "ara", "isci_rutin"))
  factor(as.character(out), levels = c("hizmet", "ara", "isci_rutin"))
}

# Egitim (0-5) -> 3-duzey: dusuk 0-1 / orta 2-3 / yuksek 4-5 (anne & baba ayni durum uzayi)
strat_edu3_recode <- function(edu) {
  v <- suppressWarnings(as.numeric(edu))
  out <- cut(v, breaks = c(-1, 1, 3, 5), labels = c("dusuk", "orta", "yuksek"))
  factor(as.character(out), levels = c("dusuk", "orta", "yuksek"))
}

# Holm — yalniz KISIM ici; NA guvenli
strat_holm <- function(p) {
  ok <- !is.na(p)
  out <- rep(NA_real_, length(p))
  if (any(ok)) {
    out[ok] <- stats::p.adjust(p[ok], method = "holm")
  }
  out
}

# t-degeri + df -> etki buyuklugu r (kismi korelasyon)
strat_t_to_r <- function(t_value, df) {
  if (is.na(t_value) || is.na(df) || df <= 0) {
    return(NA_real_)
  }
  sign(t_value) * sqrt(t_value^2 / (t_value^2 + df))
}

# ============================================================================
# Veri hazirlama
# ============================================================================

strat_prepare_family <- function(df_family_ses) {
  outcomes <- strat_embu_p_outcomes()
  strat_require_columns(
    df_family_ses,
    c(
      "aile_no", "aile_egp7", "es_siops08", "aile_isei08",
      "egitim_durumu", "es_egitim_durumu", "calisma_durumu",
      "cocuk_yas", "anne_yas", "katilimci_cocuk_cinsiyet",
      "edu_z", "isei_z", "material_z", "ses_latent",
      "beck_total", strat_embu_p_col(outcomes)
    ),
    "strat_prepare_family"
  )

  out <- df_family_ses
  out$aile_no_f <- factor(out$aile_no)

  out$egp3_f <- strat_egp3_recode(out$aile_egp7)
  out$edu3_anne_f <- strat_edu3_recode(out$egitim_durumu)
  out$edu3_baba_f <- strat_edu3_recode(out$es_egitim_durumu)

  # SIOPS prestij olcusu -> z (isei_z, edu_z, material_z R/11'den hazir)
  out$siops_z <- strat_scale(out$es_siops08)
  out$cocuk_yas_z <- strat_scale(out$cocuk_yas)
  out$anne_yas_z <- strat_scale(out$anne_yas)
  out$ses_latent_z <- strat_scale(out$ses_latent)
  # Yoksunluk = -material_z (Conger FSM: ekonomik baski yonunde)
  out$deprivation_z <- -suppressWarnings(as.numeric(out$material_z))

  calisma <- suppressWarnings(as.numeric(out$calisma_durumu))
  out$calisma_f <- factor(
    ifelse(is.na(calisma), NA_character_, ifelse(calisma == 1, "Calisiyor", "Calismiyor")),
    levels = c("Calismiyor", "Calisiyor")
  )

  if (!"group_f" %in% names(out)) {
    if ("group" %in% names(out)) {
      out$group_f <- factor(out$group, levels = c("Kontrol", "DM"))
    } else {
      stop("strat_prepare_family: group_f/group bulunamadi", call. = FALSE)
    }
  }
  if (!"group_dm" %in% names(out)) {
    out$group_dm <- as.integer(out$group_f == "DM")
  }
  if (!"cinsiyet_idx_f" %in% names(out)) {
    out$cinsiyet_idx_f <- factor(out$katilimci_cocuk_cinsiyet, levels = 0:1,
      labels = c("Kiz", "Erkek"))
  }
  out
}

strat_prepare_long <- function(df_long_scored, df_family_prepared) {
  strat_require_columns(df_long_scored, c("aile_no", "cocuk_yas"), "strat_prepare_long")

  out <- df_long_scored
  out$cocuk_yas_z <- strat_scale(out$cocuk_yas)
  if (!"cinsiyet_f" %in% names(out) && "katilimci_cocuk_cinsiyet" %in% names(out)) {
    out$cinsiyet_f <- factor(out$katilimci_cocuk_cinsiyet, levels = 0:1,
      labels = c("Kiz", "Erkek"))
  }

  cov_cols <- c("aile_no", "egp3_f", "calisma_f", "group_f", "ses_latent_z", "anne_yas_z")
  strat_require_columns(df_family_prepared, cov_cols, "strat_prepare_long (aile kovaryatlari)")
  fam_cov <- df_family_prepared[, cov_cols, drop = FALSE]
  names(fam_cov) <- c("aile_no", "egp3_f", "calisma_f", "group_f_fam", "ses_latent_z", "anne_yas_z")

  # Long tarafinda ayni adli kolonlari dusur (aile kovaryatlari otorite)
  drop_existing <- intersect(c("egp3_f", "calisma_f", "ses_latent_z", "anne_yas_z"), names(out))
  if (length(drop_existing) > 0L) {
    out <- out[, setdiff(names(out), drop_existing), drop = FALSE]
  }
  out <- merge(out, fam_cov, by = "aile_no", all.x = TRUE, all.y = FALSE)
  if (!"group_f" %in% names(out)) {
    out$group_f <- out$group_f_fam
  }
  out$aile_no_f <- factor(out$aile_no)
  out
}

# ============================================================================
# §100 — EGP-3 sinif-gradyanli ebeveynlik + Simpson denetimi
# ============================================================================

# Bir alt olcek icin kapsam-bazli (havuzlanmis/DM/Kontrol) hucre betimi + emmeans
strat_egp_cells <- function(df, outcome_sub, scope, with_model = TRUE) {
  ycol <- if (identical(outcome_sub, "beck")) "beck_total" else strat_embu_p_col(outcome_sub)
  if (!ycol %in% names(df)) {
    return(NULL)
  }
  d <- data.frame(
    y = suppressWarnings(as.numeric(df[[ycol]])),
    egp3_f = df$egp3_f,
    cocuk_yas_z = df$cocuk_yas_z,
    cinsiyet_idx_f = df$cinsiyet_idx_f,
    stringsAsFactors = FALSE
  )
  d <- d[!is.na(d$egp3_f) & !is.na(d$y), , drop = FALSE]
  d$egp3_f <- factor(as.character(d$egp3_f), levels = c("hizmet", "ara", "isci_rutin"))

  levels_present <- levels(droplevels(d$egp3_f))
  raw <- do.call(rbind, lapply(c("hizmet", "ara", "isci_rutin"), function(lv) {
    yy <- d$y[d$egp3_f == lv]
    yy <- yy[!is.na(yy)]
    data.frame(
      olcum = outcome_sub, kapsam = scope, egp3 = lv,
      n_hucre = length(yy),
      ham_ort = if (length(yy) > 0L) mean(yy) else NA_real_,
      ham_medyan = if (length(yy) > 0L) stats::median(yy) else NA_real_,
      ham_sd = if (length(yy) > 1L) stats::sd(yy) else NA_real_,
      marj_ort = NA_real_, marj_se = NA_real_, ga_alt = NA_real_, ga_ust = NA_real_,
      stringsAsFactors = FALSE
    )
  }))

  if (with_model && !identical(outcome_sub, "beck") &&
      length(levels_present) >= 2L && nrow(d) >= 12L &&
      requireNamespace("emmeans", quietly = TRUE)) {
    fit <- tryCatch(stats::lm(y ~ egp3_f + cocuk_yas_z + cinsiyet_idx_f, data = d),
      error = function(e) e)
    if (!inherits(fit, "error")) {
      emm <- tryCatch(
        as.data.frame(summary(emmeans::emmeans(fit, ~ egp3_f), infer = c(TRUE, FALSE))),
        error = function(e) NULL
      )
      if (!is.null(emm)) {
        for (i in seq_len(nrow(emm))) {
          lv <- as.character(emm$egp3_f[i])
          idx <- which(raw$egp3 == lv)
          if (length(idx) == 1L) {
            raw$marj_ort[idx] <- emm$emmean[i]
            raw$marj_se[idx] <- emm$SE[i]
            raw$ga_alt[idx] <- emm$lower.CL[i]
            raw$ga_ust[idx] <- emm$upper.CL[i]
          }
        }
      }
    }
  }
  raw$statu <- strat_evidence_status()
  raw
}

# Havuzlanmis gradyan + omnibus F/eta² (aile OLS) ve long lme4 gradyani
strat_egp_gradient <- function(df_family, df_long, outcomes = strat_embu_p_outcomes()) {
  cell_rows <- list()
  omnibus_rows <- list()

  # --- Aile OLS gradyan (havuzlanmis) ---
  for (sub in outcomes) {
    cells <- strat_egp_cells(df_family, sub, scope = "havuzlanmis", with_model = TRUE)
    cells$duzey <- "aile"
    cell_rows[[paste0("fam_", sub)]] <- cells

    ycol <- strat_embu_p_col(sub)
    d <- data.frame(
      y = suppressWarnings(as.numeric(df_family[[ycol]])),
      egp3_f = df_family$egp3_f,
      cocuk_yas_z = df_family$cocuk_yas_z,
      cinsiyet_idx_f = df_family$cinsiyet_idx_f
    )
    d <- d[!is.na(d$egp3_f) & !is.na(d$y) & !is.na(d$cocuk_yas_z), , drop = FALSE]
    d$egp3_f <- factor(as.character(d$egp3_f), levels = c("hizmet", "ara", "isci_rutin"))
    row <- data.frame(
      olcum = sub, duzey = "aile", n = nrow(d),
      test = "omnibus_F", istatistik = NA_real_, df1 = NA_real_, df2 = NA_real_,
      p_deger = NA_real_, kismi_eta2 = NA_real_, stringsAsFactors = FALSE
    )
    if (nlevels(droplevels(d$egp3_f)) >= 2L && nrow(d) >= 12L) {
      full <- stats::lm(y ~ egp3_f + cocuk_yas_z + cinsiyet_idx_f, data = d)
      red <- stats::lm(y ~ cocuk_yas_z + cinsiyet_idx_f, data = d)
      an <- stats::anova(red, full)
      ss_red <- sum(stats::residuals(red)^2)
      ss_full <- sum(stats::residuals(full)^2)
      row$istatistik <- an$F[2]
      row$df1 <- an$Df[2]
      row$df2 <- an$Res.Df[2]
      row$p_deger <- an$`Pr(>F)`[2]
      row$kismi_eta2 <- (ss_red - ss_full) / ss_red
    }
    omnibus_rows[[paste0("fam_", sub)]] <- row
  }

  # --- Long lme4 gradyan (embu_c_*_mean; family-level EGP-3 merge edilmis) ---
  # SAP §100.1: kovaryatlar yas + cinsiyet (long modelde de cinsiyet_f zorunlu;
  # cinsiyet kolonu tumden yoksa/bos ise yalniz yas ile dusulur ve bu not edilir).
  use_lmer <- requireNamespace("lme4", quietly = TRUE)
  for (sub in outcomes) {
    ycol <- strat_embu_c_long_col(sub)
    if (!ycol %in% names(df_long)) next
    d <- data.frame(
      y = suppressWarnings(as.numeric(df_long[[ycol]])),
      egp3_f = df_long$egp3_f,
      cocuk_yas_z = df_long$cocuk_yas_z,
      cinsiyet_f = if ("cinsiyet_f" %in% names(df_long)) df_long$cinsiyet_f else factor(NA),
      aile_no_f = df_long$aile_no_f
    )
    d <- d[!is.na(d$egp3_f) & !is.na(d$y) & !is.na(d$cocuk_yas_z), , drop = FALSE]
    use_gender <- any(!is.na(d$cinsiyet_f)) &&
      nlevels(droplevels(factor(d$cinsiyet_f[!is.na(d$cinsiyet_f)]))) >= 2L
    if (use_gender) {
      d <- d[!is.na(d$cinsiyet_f), , drop = FALSE]
      d$cinsiyet_f <- droplevels(factor(d$cinsiyet_f))
    }
    cov_rhs <- if (use_gender) "cocuk_yas_z + cinsiyet_f" else "cocuk_yas_z"
    d$egp3_f <- factor(as.character(d$egp3_f), levels = c("hizmet", "ara", "isci_rutin"))

    # Long hucre betimi (havuzlanmis)
    raw <- do.call(rbind, lapply(c("hizmet", "ara", "isci_rutin"), function(lv) {
      yy <- d$y[d$egp3_f == lv]; yy <- yy[!is.na(yy)]
      data.frame(olcum = sub, kapsam = "havuzlanmis", egp3 = lv, n_hucre = length(yy),
        ham_ort = if (length(yy) > 0L) mean(yy) else NA_real_,
        ham_medyan = if (length(yy) > 0L) stats::median(yy) else NA_real_,
        ham_sd = if (length(yy) > 1L) stats::sd(yy) else NA_real_,
        marj_ort = NA_real_, marj_se = NA_real_, ga_alt = NA_real_, ga_ust = NA_real_,
        statu = strat_evidence_status(), duzey = "long", stringsAsFactors = FALSE)
    }))

    row <- data.frame(
      olcum = sub, duzey = "long", n = nrow(d),
      test = "omnibus_LRT", istatistik = NA_real_, df1 = NA_real_, df2 = NA_real_,
      p_deger = NA_real_, kismi_eta2 = NA_real_, stringsAsFactors = FALSE
    )
    if (use_lmer && nlevels(droplevels(d$egp3_f)) >= 2L &&
        length(unique(d$aile_no_f)) >= 10L) {
      full <- tryCatch(suppressMessages(lme4::lmer(
        stats::as.formula(paste0("y ~ egp3_f + ", cov_rhs, " + (1 | aile_no_f)")),
        data = d, REML = FALSE)),
        error = function(e) e)
      red <- tryCatch(suppressMessages(lme4::lmer(
        stats::as.formula(paste0("y ~ ", cov_rhs, " + (1 | aile_no_f)")),
        data = d, REML = FALSE)),
        error = function(e) e)
      if (!inherits(full, "error") && !inherits(red, "error")) {
        an <- tryCatch(stats::anova(red, full), error = function(e) NULL)
        if (!is.null(an)) {
          row$istatistik <- an$Chisq[2]
          row$df1 <- an$Df[2]
          row$p_deger <- an$`Pr(>Chisq)`[2]
        }
        if (requireNamespace("emmeans", quietly = TRUE)) {
          emm <- tryCatch(
            as.data.frame(summary(emmeans::emmeans(full, ~ egp3_f), infer = c(TRUE, FALSE))),
            error = function(e) NULL
          )
          if (!is.null(emm)) {
            lc <- if ("lower.CL" %in% names(emm)) "lower.CL" else "asymp.LCL"
            uc <- if ("upper.CL" %in% names(emm)) "upper.CL" else "asymp.UCL"
            for (i in seq_len(nrow(emm))) {
              lv <- as.character(emm$egp3_f[i]); idx <- which(raw$egp3 == lv)
              if (length(idx) == 1L) {
                raw$marj_ort[idx] <- emm$emmean[i]
                raw$marj_se[idx] <- emm$SE[i]
                raw$ga_alt[idx] <- emm[[lc]][i]
                raw$ga_ust[idx] <- emm[[uc]][i]
              }
            }
          }
        }
      }
    }
    cell_rows[[paste0("long_", sub)]] <- raw
    omnibus_rows[[paste0("long_", sub)]] <- row
  }

  cells <- do.call(rbind, cell_rows)
  omnibus <- do.call(rbind, omnibus_rows)
  omnibus$p_holm <- strat_holm(omnibus$p_deger)
  omnibus$statu <- strat_evidence_status()
  rownames(cells) <- NULL
  rownames(omnibus) <- NULL
  list(cells = cells, omnibus = omnibus)
}

# ZORUNLU Simpson denetimi: havuzlanmis + grup-ici (DM/Kontrol) yan yana
strat_egp_simpson <- function(df_family, outcomes = strat_embu_p_outcomes()) {
  all_outcomes <- c(outcomes, "beck")
  rows <- list()
  scopes <- list(
    havuzlanmis = df_family,
    DM = df_family[df_family$group_f == "DM", , drop = FALSE],
    Kontrol = df_family[df_family$group_f == "Kontrol", , drop = FALSE]
  )
  for (sub in all_outcomes) {
    for (scope in names(scopes)) {
      cells <- strat_egp_cells(scopes[[scope]], sub, scope = scope,
        with_model = !identical(sub, "beck"))
      if (!is.null(cells)) {
        cells$duzey <- "aile"
        rows[[paste(sub, scope, sep = "_")]] <- cells
      }
    }
  }
  out <- do.call(rbind, rows)
  rownames(out) <- NULL
  out
}

# ============================================================================
# §100 / §1.6-C — ISEI vs SIOPS vs EGP-3 olcum-yarisi (commonality + AIC)
# ============================================================================

strat_measurement_race_one <- function(df, outcome_sub) {
  ycol <- strat_embu_p_col(outcome_sub)
  d <- data.frame(
    y = suppressWarnings(as.numeric(df[[ycol]])),
    isei_z = suppressWarnings(as.numeric(df$isei_z)),
    siops_z = df$siops_z,
    egp3_f = df$egp3_f,
    cocuk_yas_z = df$cocuk_yas_z,
    cinsiyet_idx_f = df$cinsiyet_idx_f
  )
  d <- d[stats::complete.cases(d), , drop = FALSE]
  d$egp3_f <- factor(as.character(d$egp3_f), levels = c("hizmet", "ara", "isci_rutin"))
  n <- nrow(d)
  if (n < 20L || nlevels(droplevels(d$egp3_f)) < 2L) {
    return(data.frame(
      olcum = outcome_sub, yordayici = "yetersiz_n", n = n,
      model_r2 = NA_real_, artimsal_r2 = NA_real_, essiz_r2 = NA_real_,
      aic = NA_real_, F_deger = NA_real_, p_deger = NA_real_,
      statu = strat_evidence_status(), stringsAsFactors = FALSE
    ))
  }

  r2 <- function(fit) summary(fit)$r.squared
  base <- stats::lm(y ~ cocuk_yas_z + cinsiyet_idx_f, data = d)
  m_isei <- stats::update(base, . ~ . + isei_z)
  m_siops <- stats::update(base, . ~ . + siops_z)
  m_egp <- stats::update(base, . ~ . + egp3_f)
  full <- stats::lm(y ~ cocuk_yas_z + cinsiyet_idx_f + isei_z + siops_z + egp3_f, data = d)
  no_isei <- stats::lm(y ~ cocuk_yas_z + cinsiyet_idx_f + siops_z + egp3_f, data = d)
  no_siops <- stats::lm(y ~ cocuk_yas_z + cinsiyet_idx_f + isei_z + egp3_f, data = d)
  no_egp <- stats::lm(y ~ cocuk_yas_z + cinsiyet_idx_f + isei_z + siops_z, data = d)

  r2_base <- r2(base); r2_full <- r2(full)
  total_ses <- r2_full - r2_base
  uniq_isei <- r2_full - r2(no_isei)
  uniq_siops <- r2_full - r2(no_siops)
  uniq_egp <- r2_full - r2(no_egp)
  ortak <- total_ses - (uniq_isei + uniq_siops + uniq_egp)

  ftest <- function(reduced, added) {
    an <- stats::anova(reduced, added)
    c(F = an$F[2], p = an$`Pr(>F)`[2])
  }
  f_isei <- ftest(base, m_isei); f_siops <- ftest(base, m_siops); f_egp <- ftest(base, m_egp)

  data.frame(
    olcum = outcome_sub,
    yordayici = c("base(kovaryat)", "isei_z", "siops_z", "egp3", "tam_model", "ortak(shared)"),
    n = n,
    model_r2 = c(r2_base, r2(m_isei), r2(m_siops), r2(m_egp), r2_full, NA_real_),
    artimsal_r2 = c(NA_real_, r2(m_isei) - r2_base, r2(m_siops) - r2_base,
      r2(m_egp) - r2_base, total_ses, NA_real_),
    essiz_r2 = c(NA_real_, uniq_isei, uniq_siops, uniq_egp, NA_real_, ortak),
    aic = c(stats::AIC(base), stats::AIC(m_isei), stats::AIC(m_siops),
      stats::AIC(m_egp), stats::AIC(full), NA_real_),
    F_deger = c(NA_real_, f_isei["F"], f_siops["F"], f_egp["F"], NA_real_, NA_real_),
    p_deger = c(NA_real_, f_isei["p"], f_siops["p"], f_egp["p"], NA_real_, NA_real_),
    statu = strat_evidence_status(),
    stringsAsFactors = FALSE
  )
}

strat_measurement_race <- function(df_family, outcomes = strat_embu_p_outcomes()) {
  rows <- lapply(outcomes, function(sub) strat_measurement_race_one(df_family, sub))
  out <- do.call(rbind, rows)
  out$p_holm <- strat_holm(out$p_deger)
  rownames(out) <- NULL
  out
}

# ============================================================================
# §101 — Egitim-ekseni Diagonal Reference Model (Dref, gnm)
# ============================================================================

strat_drm_outcomes <- function() {
  data.frame(
    etiket = c("embu_c_idx_sicaklik", "embu_c_idx_reddetme", "srq_ho_conflict"),
    kolon = c("embu_c_idx_sicaklik_mean", "embu_c_idx_reddetme_mean", "srq_ho_conflict_mean"),
    stringsAsFactors = FALSE
  )
}

strat_drm_one <- function(df, outcome_label, ycol, boot_n = 1000L,
                          seed = 20260708L) {
  base_row <- function(status, n, w_anne = NA_real_, se_anne = NA_real_,
                       w_baba = NA_real_, se_baba = NA_real_,
                       deviance = NA_real_, fallback_F = NA_real_, fallback_p = NA_real_) {
    data.frame(
      olcum = outcome_label, n = n, durum = status,
      w_anne = w_anne, w_anne_ga_alt = if (is.na(w_anne)) NA_real_ else w_anne - 1.96 * se_anne,
      w_anne_ga_ust = if (is.na(w_anne)) NA_real_ else w_anne + 1.96 * se_anne,
      w_baba = w_baba, w_baba_ga_alt = if (is.na(w_baba)) NA_real_ else w_baba - 1.96 * se_baba,
      w_baba_ga_ust = if (is.na(w_baba)) NA_real_ else w_baba + 1.96 * se_baba,
      deviance = deviance, fallback_F = fallback_F, fallback_p = fallback_p,
      statu = strat_evidence_status(), stringsAsFactors = FALSE
    )
  }

  if (!ycol %in% names(df)) {
    return(base_row("kolon_yok", 0L))
  }
  d <- data.frame(
    y = suppressWarnings(as.numeric(df[[ycol]])),
    edu3_anne_f = df$edu3_anne_f,
    edu3_baba_f = df$edu3_baba_f
  )
  d <- d[stats::complete.cases(d), , drop = FALSE]
  levs <- c("dusuk", "orta", "yuksek")
  d$edu3_anne_f <- factor(as.character(d$edu3_anne_f), levels = levs)
  d$edu3_baba_f <- factor(as.character(d$edu3_baba_f), levels = levs)
  n <- nrow(d)

  if (n < 30L) {
    return(base_row("yetersiz_n", n))
  }

  if (!requireNamespace("gnm", quietly = TRUE)) {
    return(base_row("gnm_yok", n))
  }

  Dref <- gnm::Dref  # formula ortaminda Dref gorunur olsun
  form <- stats::as.formula("y ~ Dref(edu3_anne_f, edu3_baba_f)")
  # gnm rastgele baslangic degerleri kullanir; sinir (boundary) cozumlerde
  # taraf run'dan run'a degisebilir -> tekrarlanabilirlik icin sabit seed.
  set.seed(seed)
  model <- tryCatch(
    suppressMessages(suppressWarnings(
      gnm::gnm(form, family = stats::gaussian(), data = d, verbose = FALSE, trace = FALSE)
    )),
    error = function(e) e
  )
  if (inherits(model, "error") || is.null(model) || !isTRUE(model$converged)) {
    # Fallback: kategorik anne × baba etkilesim
    fb <- tryCatch(stats::lm(y ~ edu3_anne_f * edu3_baba_f, data = d), error = function(e) e)
    if (inherits(fb, "error")) {
      return(base_row("yakinsamadi_fallback_hata", n))
    }
    fb_red <- stats::lm(y ~ edu3_anne_f + edu3_baba_f, data = d)
    an <- tryCatch(stats::anova(fb_red, fb), error = function(e) NULL)
    return(base_row(
      "yakinsamadi_kategorik_fallback", n,
      fallback_F = if (!is.null(an)) an$F[2] else NA_real_,
      fallback_p = if (!is.null(an)) an$`Pr(>F)`[2] else NA_real_
    ))
  }

  w <- tryCatch(
    suppressMessages(suppressWarnings({
      utils::capture.output(dw <- gnm::DrefWeights(model)); dw
    })),
    error = function(e) e
  )
  if (inherits(w, "error") || is.null(w)) {
    return(base_row("drefweights_hata", n, deviance = model$deviance))
  }
  anne_key <- if ("edu3_anne_f" %in% names(w)) "edu3_anne_f" else names(w)[1]
  baba_key <- if ("edu3_baba_f" %in% names(w)) "edu3_baba_f" else names(w)[2]
  w_anne_val <- unname(w[[anne_key]]["weight"]); se_anne_val <- unname(w[[anne_key]]["se"])
  w_baba_val <- unname(w[[baba_key]]["weight"]); se_baba_val <- unname(w[[baba_key]]["se"])

  # Sinir (boundary) cozumu denetimi: w ~ 0/1 ve se ~ 0 -> kimliklenemez/dejenere
  boundary <- (min(abs(w_anne_val), abs(w_anne_val - 1)) < 1e-4) ||
    is.na(se_anne_val) || se_anne_val < 1e-4
  status <- if (isTRUE(boundary)) "yakinsadi_sinir(kimliklenemez)" else "yakinsadi"

  base_row(
    status, n,
    w_anne = w_anne_val, se_anne = se_anne_val,
    w_baba = w_baba_val, se_baba = se_baba_val,
    deviance = model$deviance
  )
}

strat_drm_education <- function(df_family, boot_n = 1000L, seed = 20260708L) {
  spec <- strat_drm_outcomes()
  rows <- lapply(seq_len(nrow(spec)), function(i) {
    strat_drm_one(df_family, spec$etiket[i], spec$kolon[i], boot_n = boot_n,
      seed = seed)
  })
  out <- do.call(rbind, rows)
  rownames(out) <- NULL
  out
}

# ============================================================================
# §102 — Materyal facet: hiyerarsik regresyon (blok-1 prestij, blok-2 material)
# ============================================================================

strat_manual_vif <- function(d, predictors) {
  stats::setNames(vapply(predictors, function(p) {
    others <- setdiff(predictors, p)
    if (length(others) == 0L) return(1)
    f <- stats::as.formula(paste(p, "~", paste(others, collapse = " + ")))
    r2 <- summary(stats::lm(f, data = d))$r.squared
    if (r2 >= 1) return(Inf)
    1 / (1 - r2)
  }, numeric(1)), predictors)
}

strat_hierarchical_one <- function(df, outcome_label, ycol) {
  d <- data.frame(
    y = suppressWarnings(as.numeric(df[[ycol]])),
    edu_z = suppressWarnings(as.numeric(df$edu_z)),
    isei_z = suppressWarnings(as.numeric(df$isei_z)),
    material_z = suppressWarnings(as.numeric(df$material_z))
  )
  d <- d[stats::complete.cases(d), , drop = FALSE]
  n <- nrow(d)
  empty <- data.frame(
    olcum = outcome_label, n = n,
    r2_blok1 = NA_real_, r2_blok2 = NA_real_, delta_r2 = NA_real_,
    F_degisim = NA_real_, df1 = NA_real_, df2 = NA_real_, p_degisim = NA_real_,
    material_b = NA_real_, material_ga_alt = NA_real_, material_ga_ust = NA_real_,
    vif_edu = NA_real_, vif_isei = NA_real_, vif_material = NA_real_,
    statu = strat_evidence_status(), stringsAsFactors = FALSE
  )
  if (n < 20L) {
    empty$durum <- "yetersiz_n"
    return(empty)
  }
  b1 <- stats::lm(y ~ edu_z + isei_z, data = d)
  b2 <- stats::lm(y ~ edu_z + isei_z + material_z, data = d)
  an <- stats::anova(b1, b2)
  ci <- stats::confint(b2)["material_z", ]
  vif <- strat_manual_vif(d, c("edu_z", "isei_z", "material_z"))

  empty$r2_blok1 <- summary(b1)$r.squared
  empty$r2_blok2 <- summary(b2)$r.squared
  empty$delta_r2 <- summary(b2)$r.squared - summary(b1)$r.squared
  empty$F_degisim <- an$F[2]
  empty$df1 <- an$Df[2]
  empty$df2 <- an$Res.Df[2]
  empty$p_degisim <- an$`Pr(>F)`[2]
  empty$material_b <- unname(stats::coef(b2)["material_z"])
  empty$material_ga_alt <- ci[1]
  empty$material_ga_ust <- ci[2]
  empty$vif_edu <- unname(vif["edu_z"])
  empty$vif_isei <- unname(vif["isei_z"])
  empty$vif_material <- unname(vif["material_z"])
  empty$durum <- "ok"
  empty
}

strat_material_hierarchical <- function(df_family, outcomes = strat_embu_p_outcomes()) {
  specs <- c(
    stats::setNames(strat_embu_p_col(outcomes), outcomes),
    c(beck_total = "beck_total")
  )
  rows <- lapply(names(specs), function(lab) {
    strat_hierarchical_one(df_family, lab, specs[[lab]])
  })
  out <- do.call(rbind, rows)
  out$p_holm <- strat_holm(out$p_degisim)
  rownames(out) <- NULL
  out
}

# ============================================================================
# §102 — Beck-araci Aile-Stres-Modeli (FSM): deprivation -> beck -> EMBU-P
# ============================================================================

strat_fsm_mediation_one <- function(df, outcome_sub, boot_n = 1000L,
                                    seed = 20260708L) {
  ycol <- strat_embu_p_col(outcome_sub)
  status_row <- function(status, n = 0L) {
    data.frame(olcum = outcome_sub, parametre = NA_character_, tahmin = NA_real_,
      se = NA_real_, ci_alt = NA_real_, ci_ust = NA_real_, p_deger = NA_real_,
      n = n, durum = status, statu = strat_evidence_status(), stringsAsFactors = FALSE)
  }
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(status_row("lavaan_yok"))
  }
  d <- data.frame(
    y = suppressWarnings(as.numeric(df[[ycol]])),
    deprivation_z = suppressWarnings(as.numeric(df$deprivation_z)),
    beck_total = suppressWarnings(as.numeric(df$beck_total)),
    group_dm = suppressWarnings(as.numeric(df$group_dm)),
    anne_yas_z = suppressWarnings(as.numeric(df$anne_yas_z))
  )
  d <- d[stats::complete.cases(d), , drop = FALSE]
  n <- nrow(d)
  if (n < 30L) {
    return(status_row("yetersiz_n", n))
  }
  model <- '
    beck_total ~ a*deprivation_z + group_dm + anne_yas_z
    y ~ b*beck_total + cprime*deprivation_z + group_dm + anne_yas_z
    dolayli := a*b
    toplam := a*b + cprime
    oran_araci := (a*b) / (a*b + cprime)
  '
  set.seed(seed)
  fit <- tryCatch(
    suppressWarnings(lavaan::sem(model, data = d, estimator = "ML",
      missing = "listwise", se = "bootstrap", bootstrap = boot_n)),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(status_row(paste0("hata:", conditionMessage(fit)), n))
  }
  pe <- tryCatch(lavaan::parameterEstimates(fit, boot.ci.type = "bca.simple"),
    error = function(e) NULL)
  if (is.null(pe)) {
    return(status_row("parameterEstimates_hata", n))
  }
  keep <- pe$label %in% c("a", "b", "cprime") | pe$op == ":="
  eff <- pe[keep, , drop = FALSE]
  label <- ifelse(nzchar(eff$label), eff$label, eff$lhs)
  data.frame(
    olcum = outcome_sub,
    parametre = label,
    tahmin = eff$est,
    se = eff$se,
    ci_alt = eff$ci.lower,
    ci_ust = eff$ci.upper,
    p_deger = eff$pvalue,
    n = n,
    durum = "ok",
    statu = strat_evidence_status(),
    stringsAsFactors = FALSE
  )
}

strat_fsm_mediation <- function(df_family, subscales = c("sicaklik", "reddetme"),
                                boot_n = 1000L, seed = 20260708L) {
  rows <- lapply(subscales, function(sub) {
    strat_fsm_mediation_one(df_family, sub, boot_n = boot_n, seed = seed)
  })
  out <- do.call(rbind, rows)
  # Holm yalniz dolayli etki (a*b) p-degerleri uzerinde (alt olcekler arasi)
  is_ind <- out$parametre == "dolayli" & out$durum == "ok"
  out$p_holm <- NA_real_
  if (any(is_ind)) {
    out$p_holm[is_ind] <- strat_holm(out$p_deger[is_ind])
  }
  rownames(out) <- NULL
  out
}

# ============================================================================
# §102b — Anne istihdami × grup moderasyonu (aile OLS + long lme4) + TOST
# ============================================================================

strat_employment_family_one <- function(df, outcome_sub) {
  ycol <- strat_embu_p_col(outcome_sub)
  d <- data.frame(
    y = suppressWarnings(as.numeric(df[[ycol]])),
    calisma_f = df$calisma_f,
    group_f = df$group_f,
    ses_latent_z = suppressWarnings(as.numeric(df$ses_latent_z)),
    anne_yas_z = suppressWarnings(as.numeric(df$anne_yas_z))
  )
  d <- d[stats::complete.cases(d), , drop = FALSE]
  d$calisma_f <- droplevels(d$calisma_f)
  d$group_f <- droplevels(d$group_f)
  n <- nrow(d)
  empty <- function(status) data.frame(
    olcum = outcome_sub, duzey = "aile", terim = NA_character_,
    tahmin = NA_real_, se = NA_real_, ci_alt = NA_real_, ci_ust = NA_real_,
    t_deger = NA_real_, p_deger = NA_real_, etki_r = NA_real_, n = n,
    n_etkin = n,
    durum = status, statu = strat_evidence_status(), stringsAsFactors = FALSE
  )
  if (n < 20L || nlevels(d$calisma_f) < 2L || nlevels(d$group_f) < 2L) {
    return(empty("yetersiz_veri"))
  }
  fit <- stats::lm(y ~ calisma_f * group_f + ses_latent_z + anne_yas_z, data = d)
  sm <- summary(fit)
  co <- sm$coefficients
  ci <- stats::confint(fit)
  df_res <- fit$df.residual
  terms_of_interest <- rownames(co)
  rows <- lapply(terms_of_interest, function(tm) {
    tval <- co[tm, "t value"]
    data.frame(
      olcum = outcome_sub, duzey = "aile", terim = tm,
      tahmin = co[tm, "Estimate"], se = co[tm, "Std. Error"],
      ci_alt = ci[tm, 1], ci_ust = ci[tm, 2],
      t_deger = tval, p_deger = co[tm, "Pr(>|t|)"],
      etki_r = strat_t_to_r(tval, df_res), n = n,
      n_etkin = n,
      durum = "ok", statu = strat_evidence_status(), stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

strat_employment_long_one <- function(df_long, outcome_sub) {
  ycol <- strat_embu_c_long_col(outcome_sub)
  empty <- function(status, n = 0L) data.frame(
    olcum = outcome_sub, duzey = "long", terim = NA_character_,
    tahmin = NA_real_, se = NA_real_, ci_alt = NA_real_, ci_ust = NA_real_,
    t_deger = NA_real_, p_deger = NA_real_, etki_r = NA_real_, n = n,
    n_etkin = n,
    durum = status, statu = strat_evidence_status(), stringsAsFactors = FALSE
  )
  if (!ycol %in% names(df_long)) {
    return(empty("kolon_yok"))
  }
  if (!requireNamespace("lme4", quietly = TRUE) ||
      !requireNamespace("lmerTest", quietly = TRUE)) {
    return(empty("lme4_yok"))
  }
  d <- data.frame(
    y = suppressWarnings(as.numeric(df_long[[ycol]])),
    calisma_f = df_long$calisma_f,
    group_f = df_long$group_f,
    ses_latent_z = suppressWarnings(as.numeric(df_long$ses_latent_z)),
    anne_yas_z = suppressWarnings(as.numeric(df_long$anne_yas_z)),
    aile_no_f = df_long$aile_no_f
  )
  d <- d[stats::complete.cases(d), , drop = FALSE]
  d$calisma_f <- droplevels(d$calisma_f)
  d$group_f <- droplevels(d$group_f)
  n <- nrow(d)
  if (n < 30L || nlevels(d$calisma_f) < 2L || nlevels(d$group_f) < 2L ||
      length(unique(d$aile_no_f)) < 10L) {
    return(empty("yetersiz_veri", n))
  }
  fit <- tryCatch(
    suppressMessages(suppressWarnings(lmerTest::lmer(
      y ~ calisma_f * group_f + ses_latent_z + anne_yas_z + (1 | aile_no_f), data = d))),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(empty(paste0("hata:", conditionMessage(fit)), n))
  }
  co <- tryCatch(summary(fit)$coefficients, error = function(e) NULL)
  if (is.null(co)) {
    return(empty("summary_hata", n))
  }
  ci <- tryCatch(suppressMessages(stats::confint(fit, method = "Wald")),
    error = function(e) NULL)
  # Kumelenme duzeltmesi: TOST/esdegerlik icin etkin n = aile (kume) sayisi;
  # 482 long gozlemi bagimsiz saymak anti-konservatif olur (SAP §115 tedbiri).
  n_fam <- length(unique(d$aile_no_f))
  rows <- lapply(rownames(co), function(tm) {
    tval <- if ("t value" %in% colnames(co)) co[tm, "t value"] else NA_real_
    dfree <- if ("df" %in% colnames(co)) co[tm, "df"] else NA_real_
    pval <- if ("Pr(>|t|)" %in% colnames(co)) co[tm, "Pr(>|t|)"] else NA_real_
    ci_lo <- if (!is.null(ci) && tm %in% rownames(ci)) ci[tm, 1] else NA_real_
    ci_hi <- if (!is.null(ci) && tm %in% rownames(ci)) ci[tm, 2] else NA_real_
    data.frame(
      olcum = outcome_sub, duzey = "long", terim = tm,
      tahmin = co[tm, "Estimate"], se = co[tm, "Std. Error"],
      ci_alt = ci_lo, ci_ust = ci_hi,
      t_deger = tval, p_deger = pval,
      etki_r = strat_t_to_r(tval, dfree), n = n,
      n_etkin = n_fam,
      durum = "ok", statu = strat_evidence_status(), stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

# TOST esdegerlik (SESOI |r|=.10) — korelasyon uzerinden (TOSTER::corsum_test)
strat_tost_r <- function(r, n, context = "", sesoi = strat_sesoi_r(), alpha = 0.05) {
  out <- data.frame(
    baglam = context, r = r, n = n, sesoi = sesoi,
    tost_p = NA_real_, ga_alt = NA_real_, ga_ust = NA_real_,
    karar = NA_character_, yontem = NA_character_,
    statu = strat_evidence_status(), stringsAsFactors = FALSE
  )
  if (is.na(r) || is.na(n) || n < 5L || abs(r) >= 1) {
    out$karar <- "hesaplanamadi"
    return(out)
  }
  if (requireNamespace("TOSTER", quietly = TRUE)) {
    res <- tryCatch(
      TOSTER::corsum_test(r = r, n = as.integer(n), alternative = "equivalence",
        method = "pearson", null = sesoi, alpha = alpha),
      error = function(e) e
    )
    if (!inherits(res, "error")) {
      out$tost_p <- unname(res$p.value)
      if (!is.null(res$conf.int)) {
        out$ga_alt <- res$conf.int[1]
        out$ga_ust <- res$conf.int[2]
      }
      out$yontem <- "TOSTER::corsum_test"
      out$karar <- if (!is.na(out$tost_p) && out$tost_p < alpha) {
        "esdeger(SESOI ici)"
      } else {
        "esdeger_degil/belirsiz"
      }
      return(out)
    }
  }
  # Fallback: Fisher-z manuel TOST
  zr <- atanh(r); se <- 1 / sqrt(n - 3)
  zl <- atanh(-sesoi); zh <- atanh(sesoi)
  p_lower <- stats::pnorm((zr - zl) / se, lower.tail = FALSE)
  p_upper <- stats::pnorm((zr - zh) / se, lower.tail = TRUE)
  p_tost <- max(p_lower, p_upper)
  out$tost_p <- p_tost
  out$ga_alt <- tanh(zr - stats::qnorm(1 - alpha) * se)
  out$ga_ust <- tanh(zr + stats::qnorm(1 - alpha) * se)
  out$yontem <- "Fisher_z_manuel"
  out$karar <- if (p_tost < alpha) "esdeger(SESOI ici)" else "esdeger_degil/belirsiz"
  out
}

strat_employment_moderation <- function(df_family, df_long,
                                        outcomes = strat_embu_p_outcomes()) {
  fam_rows <- lapply(outcomes, function(sub) strat_employment_family_one(df_family, sub))
  long_rows <- lapply(outcomes, function(sub) strat_employment_long_one(df_long, sub))
  coefs <- do.call(rbind, c(fam_rows, long_rows))

  # Etkilesim terimini isaretle + Holm (aile ve long ayri aile-set)
  is_int <- grepl(":", coefs$terim) & coefs$durum == "ok"
  coefs$p_holm <- NA_real_
  for (lev in c("aile", "long")) {
    idx <- which(is_int & coefs$duzey == lev)
    if (length(idx) > 0L) {
      coefs$p_holm[idx] <- strat_holm(coefs$p_deger[idx])
    }
  }

  # TOST: etkilesim terimleri (null iddia hazirligi — SESOI |r|=.10)
  # Long duzeyde n = n_etkin (aile/kume sayisi): kumelenmis 482 gozlemi bagimsiz
  # saymak esdegerlik testini anti-konservatif yapar (SAP §115 cluster tedbiri).
  int_rows <- coefs[is_int, , drop = FALSE]
  tost_rows <- list()
  if (nrow(int_rows) > 0L) {
    for (i in seq_len(nrow(int_rows))) {
      ctx <- sprintf("%s|%s|%s", int_rows$duzey[i], int_rows$olcum[i], int_rows$terim[i])
      n_tost <- if (!is.na(int_rows$n_etkin[i])) int_rows$n_etkin[i] else int_rows$n[i]
      tost_rows[[i]] <- strat_tost_r(int_rows$etki_r[i], n_tost, context = ctx)
    }
  }
  tost <- if (length(tost_rows) > 0L) do.call(rbind, tost_rows) else NULL
  rownames(coefs) <- NULL
  list(coefficients = coefs, tost = tost)
}

# ============================================================================
# Pipeline sarici (Faz II deseni)
# ============================================================================

run_phase3_social_stratification_pipeline <- function(df_family_ses, df_long_scored,
                                                       df_family_scored = NULL,
                                                       boot_n = 1000L,
                                                       seed = 20260708L) {
  fam <- strat_prepare_family(df_family_ses)
  long <- strat_prepare_long(df_long_scored, fam)

  gradient <- tryCatch(strat_egp_gradient(fam, long), error = function(e) {
    list(cells = NULL, omnibus = NULL, hata = conditionMessage(e))
  })
  simpson <- tryCatch(strat_egp_simpson(fam), error = function(e) NULL)
  meas_race <- tryCatch(strat_measurement_race(fam), error = function(e) NULL)
  drm <- tryCatch(strat_drm_education(fam, boot_n = boot_n, seed = seed),
    error = function(e) NULL)
  hierarchical <- tryCatch(strat_material_hierarchical(fam), error = function(e) NULL)
  fsm <- tryCatch(strat_fsm_mediation(fam, boot_n = boot_n, seed = seed),
    error = function(e) NULL)
  employment <- tryCatch(strat_employment_moderation(fam, long),
    error = function(e) list(coefficients = NULL, tost = NULL))

  n_egp_na <- sum(is.na(fam$egp3_f))
  status_summary <- data.frame(
    analiz = "phase3_social_stratification",
    n_aile = nrow(fam),
    n_long = nrow(long),
    egp3_yapisal_na = n_egp_na,
    egp3_hizmet = sum(fam$egp3_f == "hizmet", na.rm = TRUE),
    egp3_ara = sum(fam$egp3_f == "ara", na.rm = TRUE),
    egp3_isci_rutin = sum(fam$egp3_f == "isci_rutin", na.rm = TRUE),
    boot_n = boot_n,
    kanit_kategorisi = strat_evidence_status(),
    sapma_tipi = strat_deviation_note(),
    reference_doc = strat_reference_doc(),
    stringsAsFactors = FALSE
  )

  list(
    egp_gradient = gradient$cells,
    egp_gradient_omnibus = gradient$omnibus,
    egp_simpson = simpson,
    measurement_race = meas_race,
    drm_education = drm,
    material_hierarchical = hierarchical,
    fsm_mediation = fsm,
    employment_moderation = employment$coefficients,
    tost = employment$tost,
    status_summary = status_summary
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
