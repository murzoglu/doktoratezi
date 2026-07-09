# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLVIII / §130-133
# MATERNAL MENTAL SAGLIK YUKU → COCUK/KARDES DUZLEMI
#
# Mantik: CSR'da H3 (anne oz-bildirimi) uc-katmanli NEGATIF iken cocuk algisi
# (H1) DM lehine reddetme sinyali verir. Anne mental-saglik yuku (antidepresan +
# BDI) CSR'da yalniz ANNE duzlemine baglandi; COCUK algi ve KARDES duzlemine
# hic tasinmadi. Bu modul o kopruyu kurar.
#
#   §130 — AD (tedavi/temas) x BDI (guncel siddet) 2x2 → EMBU-C cocuk algisi.
#     KRITIK (ampirik dogrulı): DM'de AD kullanan annede guncel Beck DAHA DUSUK
#     (tedaviyle kontrol) → anne_antidepresan GUNCEL SIDDET DEGIL tedavi/temas
#     gostergesidir. AD ve BDI AYNI YONDE TOPLANMAZ → 2x2 (ad_f x beck_clinical).
#     Model: embu_c_reddetme ~ ad_f * beck_clinical + group_f + cocuk_yas_z +
#       (1|aile_no). AD KOVARYAT DEGIL, tedavi-ekseni. beck_total surekli duyarlilik.
#   §131 — Maternal distres → anne-cocuk EMBU discrepancy (isaretli).
#     Gozlenen fark-skoru: disc = embu_p - embu_c_idx (isaretli; + = anne fazla).
#     ~ ad_f + beck_clinical + group_f (iki eksen ADDITIF; monotonik gradyan YOK).
#     Yon acik: anne-fazla vs cocuk-fazla discrepancy.
#   §132 — Informant discrepancy (|EMBU-P - EMBU-C idx|) → SRQ kardes iliskisi.
#     |disc| → srq_ho_conflict/rivalry/warmth (aile-duzeyi; indeks SRQ = 1/aile).
#     ⚠️ Baba davranisi dogrudan olculmuyor → "cocugun algi-uyusmazligi" etiketi.
#   §133 — Latent Beck-sinifi (R/24 LCA predclass) dissal dogrulamasi.
#     Girdi-sozlesmesi: aile_no + predclass + posterior + entropy + max_posterior
#     (modal atama; entropy raporlanir, siniflandirma-hatasi DUZELTILMEZ → ihtiyatli).
#     Sinif → (i) EMBU-C reddetme discrepancy; (ii) SRQ catisma; (iii) AD orani.
#
# ⚠️ Imputation YAPILMAZ (Kural 19). Korelasyonel dil; nedensel yok. HARKing yok:
# hicbir bulgu H1-H4 prior'ini guclendirmez. Tum ciktilar [KESIFSEL - POST-HOC].

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}

mmcp_status_label <- function() "[KESIFSEL - POST-HOC]"

mmcp_numeric <- function(x) suppressWarnings(as.numeric(x))

mmcp_scale <- function(x) {
  x <- mmcp_numeric(x)
  ok <- !is.na(x); out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) return(out)
  s <- stats::sd(x[ok]); if (is.na(s) || s == 0) return(out)
  out[ok] <- (x[ok] - mean(x[ok])) / s
  out
}

mmcp_require_columns <- function(df, columns, context) {
  missing <- setdiff(columns, names(df))
  if (length(missing) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

mmcp_ad_factor <- function(x) {
  if (is.factor(x)) {
    lv <- tolower(as.character(x))
    bin <- as.integer(lv %in% c("1", "evet", "var", "yes", "true"))
  } else {
    xn <- mmcp_numeric(x); bin <- as.integer(!is.na(xn) & xn > 0)
  }
  factor(ifelse(bin == 1L, "Evet", "Hayir"), levels = c("Hayir", "Evet"))
}

mmcp_embu_c_long_outcomes <- function() {
  c("embu_c_reddetme_mean", "embu_c_karsilastirma_mean")
}

# lmerTest sabit-etki tablosu (Satterthwaite df + %95 GA + kismi r)
mmcp_lmer_fixed <- function(model, label) {
  ct <- as.data.frame(stats::coef(summary(model)))
  ct$term <- rownames(ct); rownames(ct) <- NULL
  est <- ct[["Estimate"]]; se <- ct[["Std. Error"]]
  dfv <- if ("df" %in% names(ct)) ct[["df"]] else rep(stats::df.residual(model), nrow(ct))
  tval <- if ("t value" %in% names(ct)) ct[["t value"]] else ct[[grep("value", names(ct))[1L]]]
  pcol <- grep("^Pr", names(ct), value = TRUE)
  pval <- if (length(pcol)) ct[[pcol[1L]]] else rep(NA_real_, nrow(ct))
  crit <- stats::qt(0.975, df = dfv)
  data.frame(
    label = label, term = ct$term, estimate = est, se = se, df = dfv,
    t_value = tval, p_value = pval,
    ci_lower = est - crit * se, ci_upper = est + crit * se,
    n = stats::nobs(model), statu = mmcp_status_label(),
    row.names = NULL, stringsAsFactors = FALSE
  )
}

# =========================================================================
# §130 — AD x BDI 2x2 → EMBU-C (long, aile-clustered)
# =========================================================================

mmcp_prepare_long <- function(df_long_scored, df_family_ses) {
  mmcp_require_columns(df_long_scored,
    c("aile_no", "group_f", "cocuk_yas"), "§130 long")
  mmcp_require_columns(df_family_ses,
    c("aile_no", "anne_antidepresan", "beck_clinical", "beck_total"), "§130 family")

  fam <- df_family_ses[!duplicated(df_family_ses$aile_no),
    c("aile_no", "anne_antidepresan", "beck_clinical", "beck_total"), drop = FALSE]
  m <- match(df_long_scored$aile_no, fam$aile_no)
  out <- df_long_scored
  out$ad_f <- mmcp_ad_factor(fam$anne_antidepresan[m])
  bc <- fam$beck_clinical[m]
  out$beck_clinical <- factor(as.character(bc), levels = c("Klinik_alti", "Klinik_duzey"))
  out$beck_total_z <- mmcp_scale(fam$beck_total[m])
  out$cocuk_yas_z <- mmcp_scale(out$cocuk_yas)
  out$aile_no_f <- factor(out$aile_no)
  out$group_f <- factor(as.character(out$group_f), levels = c("Kontrol", "DM"))
  # 2x2 stratum etiketi (betimsel)
  out$risk_2x2 <- factor(
    paste0(ifelse(out$ad_f == "Evet", "AD+", "AD-"), "/",
      ifelse(out$beck_clinical == "Klinik_duzey", "BDI>=17", "BDI<17")),
    levels = c("AD-/BDI<17", "AD-/BDI>=17", "AD+/BDI<17", "AD+/BDI>=17")
  )
  out
}

mmcp_fit_embu_c <- function(df, outcome, use_continuous = FALSE) {
  rhs <- if (use_continuous) {
    "ad_f * beck_total_z + group_f + cocuk_yas_z + (1 | aile_no_f)"
  } else {
    "ad_f * beck_clinical + group_f + cocuk_yas_z + (1 | aile_no_f)"
  }
  fml <- stats::as.formula(paste(outcome, "~", rhs))
  cols <- unique(all.vars(fml))
  sub <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
  if (nrow(sub) < 30L || nlevels(droplevels(sub$ad_f)) < 2L ||
      (!use_continuous && nlevels(droplevels(sub$beck_clinical)) < 2L)) {
    return(list(fit = NULL, n = nrow(sub), status = "yetersiz_n_veya_hucre"))
  }
  fit <- tryCatch(suppressMessages(lmerTest::lmer(fml, data = sub, REML = TRUE,
    control = lme4::lmerControl(optimizer = "bobyqa"), na.action = stats::na.exclude)),
    error = function(e) e)
  if (inherits(fit, "error")) {
    return(list(fit = NULL, n = nrow(sub), status = paste0("fit_error:", conditionMessage(fit))))
  }
  list(fit = fit, n = nrow(sub), status = "ok")
}

mmcp_cell_means <- function(df, outcome) {
  cols <- c(outcome, "ad_f", "beck_clinical")
  sub <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
  rows <- list()
  for (a in levels(sub$ad_f)) {
    for (b in levels(sub$beck_clinical)) {
      idx <- which(sub$ad_f == a & sub$beck_clinical == b)
      vals <- mmcp_numeric(sub[[outcome]][idx]); vals <- vals[!is.na(vals)]
      rows[[paste(a, b, sep = "__")]] <- data.frame(
        outcome = outcome, ad = a, beck = b, n_gozlem = length(vals),
        n_aile = length(unique(sub$aile_no[idx])),
        ortalama = if (length(vals) > 0L) mean(vals) else NA_real_,
        medyan = if (length(vals) > 0L) stats::median(vals) else NA_real_,
        sd = if (length(vals) > 1L) stats::sd(vals) else NA_real_,
        statu = mmcp_status_label(), stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

mmcp_run_130 <- function(df, outcomes = mmcp_embu_c_long_outcomes()) {
  fixed_rows <- list(); cell_rows <- list(); sens_rows <- list(); status_rows <- list()
  for (oc in outcomes) {
    if (!oc %in% names(df)) {
      status_rows[[oc]] <- data.frame(outcome = oc, model = "2x2", n = 0L,
        status = "outcome_yok", statu = mmcp_status_label(), stringsAsFactors = FALSE)
      next
    }
    m2 <- mmcp_fit_embu_c(df, oc, use_continuous = FALSE)
    status_rows[[paste0(oc, "_2x2")]] <- data.frame(outcome = oc, model = "2x2",
      n = m2$n, status = m2$status, statu = mmcp_status_label(), stringsAsFactors = FALSE)
    if (!is.null(m2$fit)) {
      fixed_rows[[paste0(oc, "_2x2")]] <- mmcp_lmer_fixed(m2$fit, paste0(oc, "|2x2(ad*beck_clinical)"))
    }
    cell_rows[[oc]] <- mmcp_cell_means(df, oc)
    mc <- mmcp_fit_embu_c(df, oc, use_continuous = TRUE)
    status_rows[[paste0(oc, "_cont")]] <- data.frame(outcome = oc, model = "beck_surekli",
      n = mc$n, status = mc$status, statu = mmcp_status_label(), stringsAsFactors = FALSE)
    if (!is.null(mc$fit)) {
      sens_rows[[paste0(oc, "_cont")]] <- mmcp_lmer_fixed(mc$fit, paste0(oc, "|beck_total_z surekli"))
    }
  }
  list(
    fixed_2x2 = if (length(fixed_rows)) do.call(rbind, fixed_rows) else NULL,
    cell_means = if (length(cell_rows)) do.call(rbind, cell_rows) else NULL,
    beck_continuous_sensitivity = if (length(sens_rows)) do.call(rbind, sens_rows) else NULL,
    model_status = do.call(rbind, status_rows)
  )
}

# =========================================================================
# §131 — Maternal distres → anne-cocuk EMBU discrepancy (isaretli)
# =========================================================================

mmcp_discrepancy_subscales <- function() {
  c("reddetme", "asiri_koruma", "sicaklik", "karsilastirma")
}

mmcp_prepare_discrepancy <- function(df_family_ses) {
  sub <- mmcp_discrepancy_subscales()
  need <- c("aile_no", "group_f", "anne_antidepresan", "beck_clinical",
    paste0("embu_p_", sub, "_mean"), paste0("embu_c_idx_", sub, "_mean"))
  mmcp_require_columns(df_family_ses, need, "§131 discrepancy family")
  df <- df_family_ses[!duplicated(df_family_ses$aile_no), , drop = FALSE]
  for (s in sub) {
    p <- mmcp_numeric(df[[paste0("embu_p_", s, "_mean")]])
    c_ <- mmcp_numeric(df[[paste0("embu_c_idx_", s, "_mean")]])
    df[[paste0("disc_signed_", s)]] <- p - c_          # + = anne fazla bildiriyor
    df[[paste0("disc_abs_", s)]] <- abs(p - c_)
  }
  df$ad_f <- mmcp_ad_factor(df$anne_antidepresan)
  df$beck_clinical <- factor(as.character(df$beck_clinical),
    levels = c("Klinik_alti", "Klinik_duzey"))
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  df
}

mmcp_lm_focal <- function(fit, focal_terms, label, outcome) {
  sm <- summary(fit)$coefficients
  ci <- tryCatch(stats::confint(fit), error = function(e) NULL)
  rows <- list()
  for (ft in intersect(focal_terms, rownames(sm))) {
    rows[[ft]] <- data.frame(
      label = label, outcome = outcome, term = ft,
      estimate = sm[ft, "Estimate"], se = sm[ft, "Std. Error"],
      t_value = sm[ft, "t value"], p_value = sm[ft, "Pr(>|t|)"],
      ci_lower = if (!is.null(ci)) ci[ft, 1L] else NA_real_,
      ci_upper = if (!is.null(ci)) ci[ft, 2L] else NA_real_,
      n = stats::nobs(fit), r_squared = summary(fit)$r.squared,
      statu = mmcp_status_label(), stringsAsFactors = FALSE
    )
  }
  if (length(rows) == 0L) return(NULL)
  do.call(rbind, rows)
}

mmcp_run_131 <- function(df, subscales = mmcp_discrepancy_subscales()) {
  focal_rows <- list(); desc_rows <- list()
  for (s in subscales) {
    yv <- paste0("disc_signed_", s)
    cols <- c(yv, "ad_f", "beck_clinical", "group_f")
    sub <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
    # betimsel: ortalama isaretli discrepancy (anne-fazla mi cocuk-fazla mi)
    dd <- mmcp_numeric(sub[[yv]])
    desc_rows[[s]] <- data.frame(
      subscale = s, n = length(dd[!is.na(dd)]),
      disc_signed_ort = mean(dd, na.rm = TRUE),
      disc_signed_medyan = stats::median(dd, na.rm = TRUE),
      yon = if (mean(dd, na.rm = TRUE) > 0) "anne_fazla_bildiriyor" else "cocuk_fazla_bildiriyor",
      statu = mmcp_status_label(), stringsAsFactors = FALSE
    )
    if (nrow(sub) < 30L || nlevels(droplevels(sub$beck_clinical)) < 2L) next
    fit <- tryCatch(stats::lm(
      stats::as.formula(paste0(yv, " ~ ad_f + beck_clinical + group_f")), data = sub),
      error = function(e) NULL)
    if (is.null(fit)) next
    fr <- mmcp_lm_focal(fit, c("beck_clinicalKlinik_duzey", "ad_fEvet"),
      "distres→discrepancy (isaretli)", yv)
    if (!is.null(fr)) fr$subscale <- s
    focal_rows[[s]] <- fr
  }
  focal <- if (length(focal_rows)) do.call(rbind, focal_rows) else NULL
  if (!is.null(focal)) {
    # beck_clinical focal ailesi icin Holm
    bidx <- which(focal$term == "beck_clinicalKlinik_duzey")
    focal$p_holm <- NA_real_
    if (length(bidx) > 0L) focal$p_holm[bidx] <- stats::p.adjust(focal$p_value[bidx], method = "holm")
  }
  list(
    discrepancy_focal = focal,
    discrepancy_descriptive = do.call(rbind, desc_rows)
  )
}

# =========================================================================
# §132 — Informant discrepancy (|EMBU-P - EMBU-C idx|) → SRQ kardes iliskisi
# =========================================================================

mmcp_srq_outcomes <- function() {
  c("srq_ho_conflict_mean", "srq_ho_rivalry_mean", "srq_ho_warmth_mean")
}

mmcp_run_132 <- function(df, disc_subscale = "reddetme",
    srq_outcomes = mmcp_srq_outcomes()) {
  # df: §131 prepare ciktisi (disc_abs_* mevcut). Aile-duzeyi (indeks SRQ = 1/aile).
  disc_col <- paste0("disc_abs_", disc_subscale)
  mmcp_require_columns(df, c(disc_col, "group_f", srq_outcomes[1L]), "§132")
  df$disc_abs_z <- mmcp_scale(df[[disc_col]])
  df$ses_latent_z <- if ("ses_latent" %in% names(df)) mmcp_scale(df$ses_latent) else rep(NA_real_, nrow(df))
  focal_rows <- list()
  for (oc in srq_outcomes) {
    if (!oc %in% names(df)) next
    cols <- c(oc, "disc_abs_z", "group_f")
    sub <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
    if (nrow(sub) < 30L) next
    rhs <- if (all(!is.na(sub$ses_latent_z))) "disc_abs_z + group_f + ses_latent_z" else "disc_abs_z + group_f"
    fit <- tryCatch(stats::lm(stats::as.formula(paste(oc, "~", rhs)), data = sub),
      error = function(e) NULL)
    if (is.null(fit)) next
    fr <- mmcp_lm_focal(fit, "disc_abs_z", "discrepancy→SRQ (cocuk algi-uyusmazligi)", oc)
    if (!is.null(fr)) {
      fr$disc_subscale <- disc_subscale
      fr$label_uyari <- "Baba davranisi olculmedi; 'cocugun algi-uyusmazligi'. Nedensel dil yok."
      focal_rows[[oc]] <- fr
    }
  }
  focal <- if (length(focal_rows)) do.call(rbind, focal_rows) else NULL
  if (!is.null(focal)) {
    focal$p_holm <- stats::p.adjust(focal$p_value, method = "holm")
  }
  focal
}

# =========================================================================
# §133 — LCA girdi-sozlesmesi + dissal dogrulama
# =========================================================================

# Girdi-sozlesmesi: aile_no + predclass + posterior + entropy + max_posterior +
# risk-etiketi (profil-tabanli; poLCA sinif etiketleri keyfi).
mmcp_lca_contract <- function(df_family_ses, class_range = 1:4, seed = 20260708L) {
  if (!requireNamespace("poLCA", quietly = TRUE)) {
    return(list(status = "poLCA_yok", table = NULL, meta = NULL))
  }
  lca_res <- run_lca(df_family_ses, class_range = class_range, seed = seed)
  if (is.null(lca_res$status) || lca_res$status != "ok") {
    return(list(status = paste0("lca_", lca_res$status %||% "fail"), table = NULL, meta = NULL))
  }
  prep <- lca_res$frame
  lca_df <- prep$complete_indicators
  best <- lca_res$best_model
  post <- best$posterior
  predclass <- best$predclass
  entropy_overall <- lca_entropy(post)
  max_post <- apply(post, 1L, max)

  # Profil-tabanli etiket: yuksek beck + dusuk sicaklik = "riskli"
  class_ids <- sort(unique(predclass))
  beck_mean <- tapply(mmcp_numeric(lca_df$lca_beck_cat), predclass, mean, na.rm = TRUE)
  warm_mean <- tapply(mmcp_numeric(lca_df$lca_sicaklik_cat), predclass, mean, na.rm = TRUE)
  risk_score <- beck_mean - warm_mean
  riskli_class <- names(which.max(risk_score))
  risk_label <- ifelse(as.character(predclass) == riskli_class, "riskli", "adaptif")

  contract <- data.frame(
    aile_no = lca_df$aile_no,
    predclass = as.integer(predclass),
    risk_label = factor(risk_label, levels = c("adaptif", "riskli")),
    max_posterior = max_post,
    entropy_overall = entropy_overall,
    best_n = lca_res$best_n,
    statu = mmcp_status_label(), stringsAsFactors = FALSE
  )
  # posterior sutunlari (c1..ck)
  for (k in seq_len(ncol(post))) contract[[paste0("posterior_c", k)]] <- post[, k]

  meta <- data.frame(
    best_n = lca_res$best_n, n_contract = nrow(contract),
    entropy_overall = entropy_overall,
    mean_max_posterior = mean(max_post),
    riskli_class_id = as.integer(riskli_class),
    n_adaptif = sum(risk_label == "adaptif"), n_riskli = sum(risk_label == "riskli"),
    statu = mmcp_status_label(), stringsAsFactors = FALSE
  )
  list(status = "ok", table = contract, meta = meta)
}

# Dissal dogrulama: sinif (risk_label) → (i) EMBU-C reddetme discrepancy,
# (ii) SRQ catisma, (iii) AD orani. Modal atama; entropy ihtiyat notu.
mmcp_run_133 <- function(contract, df_family_ses) {
  if (is.null(contract) || is.null(contract$table)) {
    return(list(status = contract$status %||% "no_contract",
      external_validation = NULL, ad_by_class = NULL))
  }
  ct <- contract$table
  df <- df_family_ses[!duplicated(df_family_ses$aile_no), , drop = FALSE]
  m <- match(ct$aile_no, df$aile_no)
  # discrepancy reddetme (anne - cocuk idx) + SRQ + AD
  disc <- mmcp_numeric(df$embu_p_reddetme_mean[m]) - mmcp_numeric(df$embu_c_idx_reddetme_mean[m])
  work <- data.frame(
    aile_no = ct$aile_no, risk_label = ct$risk_label,
    group_f = factor(as.character(df$group_f[m]), levels = c("Kontrol", "DM")),
    disc_reddetme = disc,
    srq_conflict = mmcp_numeric(df$srq_ho_conflict_mean[m]),
    ad_bin = as.integer(mmcp_ad_factor(df$anne_antidepresan[m]) == "Evet"),
    stringsAsFactors = FALSE
  )
  ext_rows <- list()
  for (oc in c("disc_reddetme", "srq_conflict")) {
    cols <- c(oc, "risk_label", "group_f")
    sub <- work[stats::complete.cases(work[, cols, drop = FALSE]), , drop = FALSE]
    if (nrow(sub) < 30L || nlevels(droplevels(sub$risk_label)) < 2L) next
    fit <- stats::lm(stats::as.formula(paste(oc, "~ risk_label + group_f")), data = sub)
    sm <- summary(fit)$coefficients
    ci <- tryCatch(stats::confint(fit), error = function(e) NULL)
    ft <- "risk_labelriskli"
    if (ft %in% rownames(sm)) {
      ext_rows[[oc]] <- data.frame(
        outcome = oc, term = ft, estimate = sm[ft, "Estimate"], se = sm[ft, "Std. Error"],
        t_value = sm[ft, "t value"], p_value = sm[ft, "Pr(>|t|)"],
        ci_lower = if (!is.null(ci)) ci[ft, 1L] else NA_real_,
        ci_upper = if (!is.null(ci)) ci[ft, 2L] else NA_real_,
        n = stats::nobs(fit),
        mean_adaptif = mean(sub[[oc]][sub$risk_label == "adaptif"], na.rm = TRUE),
        mean_riskli = mean(sub[[oc]][sub$risk_label == "riskli"], na.rm = TRUE),
        statu = mmcp_status_label(), stringsAsFactors = FALSE
      )
    }
  }
  ext <- if (length(ext_rows)) do.call(rbind, ext_rows) else NULL
  if (!is.null(ext)) ext$p_holm <- stats::p.adjust(ext$p_value, method = "holm")

  # (iii) AD orani x sinif (Fisher)
  adtab <- table(factor(work$risk_label, levels = c("adaptif", "riskli")),
    factor(work$ad_bin, levels = c(0, 1)))
  ft2 <- tryCatch(stats::fisher.test(adtab), error = function(e) NULL)
  ad_by_class <- data.frame(
    test = "AD-kullanim orani x LCA risk-sinifi (Fisher)",
    n_adaptif = sum(adtab[1, ]), n_riskli = sum(adtab[2, ]),
    ad_rate_adaptif = if (sum(adtab[1, ]) > 0) adtab[1, 2] / sum(adtab[1, ]) else NA_real_,
    ad_rate_riskli = if (sum(adtab[2, ]) > 0) adtab[2, 2] / sum(adtab[2, ]) else NA_real_,
    odds_ratio = if (!is.null(ft2)) unname(ft2$estimate) else NA_real_,
    or_ci_lower = if (!is.null(ft2)) ft2$conf.int[1L] else NA_real_,
    or_ci_upper = if (!is.null(ft2)) ft2$conf.int[2L] else NA_real_,
    p_value = if (!is.null(ft2)) ft2$p.value else NA_real_,
    entropy_note = sprintf("Modal atama; genel entropy=%.3f, ort max-posterior=%.3f (siniflandirma-hatasi DUZELTILMEDI → ihtiyatli).",
      contract$meta$entropy_overall, contract$meta$mean_max_posterior),
    statu = mmcp_status_label(), stringsAsFactors = FALSE
  )
  list(status = "ok", external_validation = ext, ad_by_class = ad_by_class)
}

# =========================================================================
# Pipeline sarici
# =========================================================================

run_phase4_maternal_mh_pipeline <- function(df_long_scored, df_family_ses,
    lca_class_range = 1:4, seed = 20260708L) {

  long <- mmcp_prepare_long(df_long_scored, df_family_ses)
  res130 <- mmcp_run_130(long)

  disc_df <- mmcp_prepare_discrepancy(df_family_ses)
  res131 <- mmcp_run_131(disc_df)
  res132 <- mmcp_run_132(disc_df)

  contract <- mmcp_lca_contract(df_family_ses, class_range = lca_class_range, seed = seed)
  res133 <- mmcp_run_133(contract, df_family_ses)

  target_summary <- data.frame(
    analysis = "phase4_maternal_mh_child_plane",
    kisim = "KISIM XLVIII (§130-133)",
    n_long = nrow(long),
    ad_evet_n = sum(long$ad_f == "Evet" & !duplicated(long$aile_no), na.rm = TRUE),
    lca_best_n = if (!is.null(contract$meta)) contract$meta$best_n else NA_integer_,
    lca_entropy = if (!is.null(contract$meta)) contract$meta$entropy_overall else NA_real_,
    coklu_karsilastirma = "Holm (§131 beck focal / §132 SRQ / §133 dissal)",
    imputation = "YOK (Kural 19)",
    ad_yorumu = "AD = tedavi/temas ekseni (guncel siddet DEGIL); 2x2 ayri eksen",
    kanit_kategorisi = mmcp_status_label(),
    sapma_tipi = "Tip 3 (Faz IV post-hoc, SAP KISIM XLVIII/130-133)",
    reference_doc = "07-sap-faz4-ek-plan.md",
    stringsAsFactors = FALSE
  )

  list(
    embu_c_2x2_fixed = res130$fixed_2x2,
    embu_c_cell_means = res130$cell_means,
    embu_c_beck_continuous = res130$beck_continuous_sensitivity,
    model_status_130 = res130$model_status,
    discrepancy_focal_131 = res131$discrepancy_focal,
    discrepancy_descriptive_131 = res131$discrepancy_descriptive,
    discrepancy_srq_132 = res132,
    lca_contract_table = contract$table,
    lca_contract_meta = contract$meta,
    lca_external_validation_133 = res133$external_validation,
    lca_ad_by_class_133 = res133$ad_by_class,
    target_summary = target_summary
  )
}
