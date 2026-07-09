# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLIII / §119-120
# COCUK-DUZEYI MODERATORLER
#
#   §119 — Cocuk cinsiyeti odakli diferansiyel ebeveynlik. katilimci_cocuk_cinsiyet
#     H1/bazi modullerde yalniz kovaryat; sistematik cinsiyet × grup × ebeveynlik
#     ODAK analizi yok. EMBU-C (cocuk algi, long): y ~ cinsiyet_f * group_f +
#     cocuk_yas_z + (1|aile_no). EMBU-P (anne rapor, family): y ~ cinsiyet_f *
#     group_f + ses + anne_yas. Odak: cinsiyet×grup etkilesimi (on-belirtilmis).
#   §120 — Anne yasi substantif gradyani. anne_yas 27 modulde yalniz _z kovaryat;
#     yas→ebeveynlik ODAK gradyani yok. y ~ ns(anne_yas, 3) + ses + group_f
#     (non-lineer spline); asiri koruma / sicaklik / reddetme. Non-linearite
#     testi (spline vs lineer). Simpson denetimi (grup×yas-bandi).
#
# ⚠️ Imputation YAPILMAZ (Kural 19). Korelasyonel dil; nedensel yok.
# ⚠️ cinsiyet_f = katilimci_cocuk_cinsiyet (0=Kiz, 1=Erkek). [KESIFSEL - POST-HOC].

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}

clmod_status_label <- function() "[KESIFSEL - POST-HOC]"
clmod_numeric <- function(x) suppressWarnings(as.numeric(x))

clmod_scale <- function(x) {
  x <- clmod_numeric(x); ok <- !is.na(x); out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) return(out)
  s <- stats::sd(x[ok]); if (is.na(s) || s == 0) return(out)
  out[ok] <- (x[ok] - mean(x[ok])) / s; out
}

clmod_require_columns <- function(df, columns, context) {
  missing <- setdiff(columns, names(df))
  if (length(missing) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

# 0=Kiz, 1=Erkek (kanonik katilimci_cocuk_cinsiyet)
clmod_sex_factor <- function(x) {
  if (is.factor(x)) {
    lv <- tolower(as.character(x))
    return(factor(ifelse(lv %in% c("erkek", "1", "male", "m"), "Erkek", "Kiz"),
      levels = c("Kiz", "Erkek")))
  }
  xn <- clmod_numeric(x)
  factor(ifelse(!is.na(xn) & xn == 1, "Erkek", ifelse(!is.na(xn) & xn == 0, "Kiz", NA)),
    levels = c("Kiz", "Erkek"))
}

clmod_embu_subscales <- function() c("reddetme", "asiri_koruma", "sicaklik", "karsilastirma")

clmod_lmer_fixed <- function(model, label, source) {
  ct <- as.data.frame(stats::coef(summary(model)))
  ct$term <- rownames(ct); rownames(ct) <- NULL
  est <- ct[["Estimate"]]; se <- ct[["Std. Error"]]
  dfv <- if ("df" %in% names(ct)) ct[["df"]] else rep(stats::df.residual(model), nrow(ct))
  tcol <- grep("value$", names(ct), value = TRUE)[1L]
  pcol <- grep("^Pr", names(ct), value = TRUE)
  crit <- stats::qt(0.975, df = dfv)
  data.frame(
    source = source, label = label, term = ct$term, estimate = est, se = se, df = dfv,
    t_value = ct[[tcol]], p_value = if (length(pcol)) ct[[pcol[1L]]] else NA_real_,
    ci_lower = est - crit * se, ci_upper = est + crit * se,
    n = stats::nobs(model), statu = clmod_status_label(),
    row.names = NULL, stringsAsFactors = FALSE
  )
}

clmod_lm_fixed <- function(fit, label, source) {
  sm <- as.data.frame(summary(fit)$coefficients)
  sm$term <- rownames(sm); rownames(sm) <- NULL
  ci <- tryCatch(as.data.frame(stats::confint(fit)), error = function(e) NULL)
  est <- sm[["Estimate"]]; se <- sm[["Std. Error"]]
  data.frame(
    source = source, label = label, term = sm$term, estimate = est, se = se,
    df = stats::df.residual(fit), t_value = sm[["t value"]], p_value = sm[["Pr(>|t|)"]],
    ci_lower = if (!is.null(ci)) ci[sm$term, 1L] else NA_real_,
    ci_upper = if (!is.null(ci)) ci[sm$term, 2L] else NA_real_,
    n = stats::nobs(fit), statu = clmod_status_label(),
    row.names = NULL, stringsAsFactors = FALSE
  )
}

# =========================================================================
# §119 — Cinsiyet × grup × ebeveynlik
# =========================================================================

clmod_prepare_long <- function(df_long_scored) {
  clmod_require_columns(df_long_scored,
    c("aile_no", "group_f", "cinsiyet_f", "cocuk_yas"), "§119 long")
  out <- df_long_scored
  out$group_f <- factor(as.character(out$group_f), levels = c("Kontrol", "DM"))
  out$cinsiyet_f <- factor(as.character(out$cinsiyet_f), levels = c("Kiz", "Erkek"))
  out$aile_no_f <- factor(out$aile_no)
  out$cocuk_yas_z <- clmod_scale(out$cocuk_yas)
  out
}

clmod_prepare_family <- function(df_family_ses) {
  clmod_require_columns(df_family_ses,
    c("aile_no", "group_f", "katilimci_cocuk_cinsiyet", "anne_yas"), "§119/§120 family")
  out <- df_family_ses[!duplicated(df_family_ses$aile_no), , drop = FALSE]
  out$group_f <- factor(as.character(out$group_f), levels = c("Kontrol", "DM"))
  out$cinsiyet_f <- clmod_sex_factor(out$katilimci_cocuk_cinsiyet)
  out$anne_yas_num <- clmod_numeric(out$anne_yas)
  out$ses_latent_z <- if ("ses_latent" %in% names(out)) clmod_scale(out$ses_latent) else rep(NA_real_, nrow(out))
  out$cocuk_yas_z <- if ("cocuk_yas" %in% names(out)) clmod_scale(out$cocuk_yas) else rep(NA_real_, nrow(out))
  out
}

clmod_sex_cellmeans <- function(df, outcome) {
  cols <- c(outcome, "cinsiyet_f", "group_f")
  sub <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
  rows <- list()
  for (s in levels(sub$cinsiyet_f)) for (g in levels(sub$group_f)) {
    idx <- which(sub$cinsiyet_f == s & sub$group_f == g)
    v <- clmod_numeric(sub[[outcome]][idx]); v <- v[!is.na(v)]
    rows[[paste(s, g, sep = "__")]] <- data.frame(
      outcome = outcome, cinsiyet = s, group = g, n = length(v),
      ortalama = if (length(v)) mean(v) else NA_real_,
      sd = if (length(v) > 1L) stats::sd(v) else NA_real_,
      statu = clmod_status_label(), stringsAsFactors = FALSE)
  }
  do.call(rbind, rows)
}

clmod_run_119 <- function(long, fam, subscales = clmod_embu_subscales()) {
  inter_rows <- list(); cell_rows <- list()
  # EMBU-C (cocuk algisi, long)
  for (s in subscales) {
    yv <- paste0("embu_c_", s, "_mean")
    if (!yv %in% names(long)) next
    cols <- c(yv, "cinsiyet_f", "group_f", "cocuk_yas_z", "aile_no_f")
    sub <- long[stats::complete.cases(long[, cols, drop = FALSE]), , drop = FALSE]
    cell_rows[[paste0("C_", s)]] <- clmod_sex_cellmeans(sub, yv)
    if (nrow(sub) < 40L) next
    fit <- tryCatch(suppressMessages(lmerTest::lmer(
      stats::as.formula(paste0(yv, " ~ cinsiyet_f * group_f + cocuk_yas_z + (1 | aile_no_f)")),
      data = sub, REML = TRUE, control = lme4::lmerControl(optimizer = "bobyqa"),
      na.action = stats::na.exclude)), error = function(e) NULL)
    if (!is.null(fit)) {
      fx <- clmod_lmer_fixed(fit, paste0("embu_c_", s), "EMBU-C (cocuk)")
      inter_rows[[paste0("C_", s)]] <- fx[fx$term == "cinsiyet_fErkek:group_fDM", , drop = FALSE]
    }
  }
  # EMBU-P (anne raporu, family)
  for (s in subscales) {
    yv <- paste0("embu_p_", s, "_mean")
    if (!yv %in% names(fam)) next
    cols <- c(yv, "cinsiyet_f", "group_f")
    sub <- fam[stats::complete.cases(fam[, cols, drop = FALSE]), , drop = FALSE]
    cell_rows[[paste0("P_", s)]] <- clmod_sex_cellmeans(sub, yv)
    if (nrow(sub) < 40L) next
    rhs <- if (all(!is.na(sub$ses_latent_z))) "cinsiyet_f * group_f + ses_latent_z" else "cinsiyet_f * group_f"
    fit <- tryCatch(stats::lm(stats::as.formula(paste(yv, "~", rhs)), data = sub),
      error = function(e) NULL)
    if (!is.null(fit)) {
      fx <- clmod_lm_fixed(fit, paste0("embu_p_", s), "EMBU-P (anne)")
      inter_rows[[paste0("P_", s)]] <- fx[fx$term == "cinsiyet_fErkek:group_fDM", , drop = FALSE]
    }
  }
  inter <- if (length(inter_rows)) do.call(rbind, inter_rows) else NULL
  if (!is.null(inter)) {
    inter$p_holm <- NA_real_
    for (src in unique(inter$source)) {
      idx <- which(inter$source == src & !is.na(inter$p_value))
      if (length(idx)) inter$p_holm[idx] <- stats::p.adjust(inter$p_value[idx], method = "holm")
    }
  }
  list(
    interaction_119 = inter,
    cell_means_119 = if (length(cell_rows)) do.call(rbind, cell_rows) else NULL
  )
}

# =========================================================================
# §120 — Anne yasi non-lineer gradyani (spline)
# =========================================================================

clmod_run_120 <- function(fam, outcomes = c("asiri_koruma", "sicaklik", "reddetme")) {
  if (!requireNamespace("splines", quietly = TRUE)) {
    return(list(nonlinearity_120 = NULL, predicted_120 = NULL, simpson_120 = NULL))
  }
  nl_rows <- list(); pred_rows <- list(); simp_rows <- list()
  for (oc in outcomes) {
    yv <- paste0("embu_p_", oc, "_mean")
    if (!yv %in% names(fam)) next
    cols <- c(yv, "anne_yas_num", "group_f")
    sub <- fam[stats::complete.cases(fam[, cols, drop = FALSE]), , drop = FALSE]
    if (nrow(sub) < 40L) next
    has_ses <- "ses_latent_z" %in% names(sub) && all(!is.na(sub$ses_latent_z))
    cov_rhs <- if (has_ses) " + ses_latent_z + group_f" else " + group_f"
    lin <- tryCatch(stats::lm(
      stats::as.formula(paste0(yv, " ~ anne_yas_num", cov_rhs)), data = sub), error = function(e) NULL)
    spl <- tryCatch(stats::lm(
      stats::as.formula(paste0(yv, " ~ splines::ns(anne_yas_num, 3)", cov_rhs)), data = sub),
      error = function(e) NULL)
    if (is.null(lin) || is.null(spl)) next
    an <- tryCatch(stats::anova(lin, spl), error = function(e) NULL)
    lin_sm <- summary(lin)$coefficients
    nl_rows[[oc]] <- data.frame(
      outcome = oc, n = nrow(sub),
      lineer_beta_anne_yas = if ("anne_yas_num" %in% rownames(lin_sm)) lin_sm["anne_yas_num", "Estimate"] else NA_real_,
      lineer_p = if ("anne_yas_num" %in% rownames(lin_sm)) lin_sm["anne_yas_num", "Pr(>|t|)"] else NA_real_,
      nonlin_F = if (!is.null(an)) an$F[2L] else NA_real_,
      nonlin_df = if (!is.null(an)) an$Df[2L] else NA_real_,
      nonlin_p = if (!is.null(an)) an$`Pr(>F)`[2L] else NA_real_,
      nonlineer_var = !is.null(an) && !is.na(an$`Pr(>F)`[2L]) && an$`Pr(>F)`[2L] < 0.05,
      statu = clmod_status_label(), stringsAsFactors = FALSE)
    # Predicted (spline) anne_yas quantile'larinda (ceteris paribus ort SES + Kontrol)
    qs <- stats::quantile(sub$anne_yas_num, probs = c(.10, .25, .50, .75, .90), na.rm = TRUE)
    nd <- data.frame(anne_yas_num = as.numeric(qs))
    if (has_ses) nd$ses_latent_z <- 0
    nd$group_f <- factor("Kontrol", levels = levels(sub$group_f))
    pr <- tryCatch(stats::predict(spl, newdata = nd, interval = "confidence"),
      error = function(e) NULL)
    if (!is.null(pr)) {
      pred_rows[[oc]] <- data.frame(
        outcome = oc, anne_yas_persentil = names(qs), anne_yas = as.numeric(qs),
        tahmin = pr[, "fit"], ci_lower = pr[, "lwr"], ci_upper = pr[, "upr"],
        statu = clmod_status_label(), row.names = NULL, stringsAsFactors = FALSE)
    }
    # Simpson: grup × yas-bandi betimsel
    band <- cut(sub$anne_yas_num, breaks = stats::quantile(sub$anne_yas_num,
      probs = c(0, 1/3, 2/3, 1), na.rm = TRUE), include.lowest = TRUE,
      labels = c("genc", "orta", "yasli"))
    for (g in levels(sub$group_f)) for (b in levels(band)) {
      idx <- which(sub$group_f == g & band == b)
      v <- clmod_numeric(sub[[yv]][idx]); v <- v[!is.na(v)]
      simp_rows[[paste(oc, g, b, sep = "__")]] <- data.frame(
        outcome = oc, group = g, yas_bandi = b, n = length(v),
        ortalama = if (length(v)) mean(v) else NA_real_,
        not = "Simpson denetimi (grup×yas-bandi betimsel)",
        statu = clmod_status_label(), stringsAsFactors = FALSE)
    }
  }
  list(
    nonlinearity_120 = if (length(nl_rows)) do.call(rbind, nl_rows) else NULL,
    predicted_120 = if (length(pred_rows)) do.call(rbind, pred_rows) else NULL,
    simpson_120 = if (length(simp_rows)) do.call(rbind, simp_rows) else NULL
  )
}

# =========================================================================
# Betimsel: dogum sirasi × cinsiyet 2x2 (CIKARIMSAL TEST YOK)
# Faz V doygunluk-denetimi (workflow) bu adayi "gercekten kosulmamis + fizibl
# ama dusuk kuramsal deger" bulmustu → yalniz BETIMSEL satir; focal'e terfi
# HARKing/forking onlemi geregi YAPILMAZ.
# =========================================================================

clmod_birthorder_sex_descriptive <- function(fam,
    outcomes = c("embu_p_asiri_koruma_mean", "embu_p_reddetme_mean", "embu_c_idx_reddetme_mean")) {
  if (!all(c("katilimci_cocuk_sirasi", "cinsiyet_f") %in% names(fam))) return(NULL)
  bo <- clmod_numeric(fam$katilimci_cocuk_sirasi)
  bo_f <- factor(ifelse(is.na(bo), NA_character_, ifelse(bo <= 1, "ilk_cocuk", "sonra_dogan")),
    levels = c("ilk_cocuk", "sonra_dogan"))
  sex <- fam$cinsiyet_f
  rows <- list()
  for (b in levels(bo_f)) for (s in levels(sex)) {
    idx <- which(bo_f == b & sex == s)
    row <- data.frame(dogum_sirasi = b, cinsiyet = s, n = length(idx),
      not = "BETIMSEL 2x2 (ilk vs sonra-dogan × cinsiyet); cikarimsal test YOK (forking onlemi)",
      statu = clmod_status_label(), stringsAsFactors = FALSE)
    for (oc in intersect(outcomes, names(fam))) {
      v <- clmod_numeric(fam[[oc]][idx]); v <- v[!is.na(v)]
      row[[paste0(oc, "_ort")]] <- if (length(v)) mean(v) else NA_real_
      row[[paste0(oc, "_sd")]] <- if (length(v) > 1L) stats::sd(v) else NA_real_
    }
    rows[[paste(b, s, sep = "__")]] <- row
  }
  do.call(rbind, rows)
}

# =========================================================================
# Pipeline sarici
# =========================================================================

run_phase4_child_moderators_pipeline <- function(df_long_scored, df_family_ses) {
  long <- clmod_prepare_long(df_long_scored)
  fam <- clmod_prepare_family(df_family_ses)
  res119 <- clmod_run_119(long, fam)
  res120 <- clmod_run_120(fam)
  birthorder_sex <- clmod_birthorder_sex_descriptive(fam)

  target_summary <- data.frame(
    analysis = "phase4_child_level_moderators",
    kisim = "KISIM XLIII (§119-120)",
    n_long = nrow(long), n_family = nrow(fam),
    cinsiyet_kodlama = "0=Kiz, 1=Erkek (katilimci_cocuk_cinsiyet)",
    coklu_karsilastirma = "§119 etkilesim on-belirtilmis + Holm-icinde; §120 non-linearite F",
    imputation = "YOK (Kural 19)",
    kanit_kategorisi = clmod_status_label(),
    sapma_tipi = "Tip 3 (Faz IV post-hoc, SAP KISIM XLIII/119-120)",
    reference_doc = "07-sap-faz4-ek-plan.md",
    stringsAsFactors = FALSE
  )

  list(
    interaction_119 = res119$interaction_119,
    cell_means_119 = res119$cell_means_119,
    nonlinearity_120 = res120$nonlinearity_120,
    predicted_120 = res120$predicted_120,
    simpson_120 = res120$simpson_120,
    birthorder_sex_descriptive = birthorder_sex,
    target_summary = target_summary
  )
}
