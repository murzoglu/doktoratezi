# [KESIFSEL - POST-HOC] Faz IV SAP KISIM XLII / §116-118
# YONLU KARDES-ILISKI MIMARISI (SRQ birinci-derece faset)
#
#   §116 — Yonlu bakim/guc/hayranlik asimetrisi. srq_higher_order_map() `status`
#     ustunu nurturance_by + nurturance_of + dominance_by + dominance_of olarak
#     TOPLAR → yon simetriklesir. Kronik-hastalik diadinda kimin kime bakim
#     verdigi/baskin oldugu asimetriktir. Yon skoru = OF - BY (+ = raporlayan
#     cocuk kardese VERIYOR/baskin). Model: asym ~ group_f * family_role_f +
#     cocuk_yas_z + (1|aile_no) (long, aile-clustered). Her faset icin ω/α.
#   §117 — 14 non-partiality faset granuler profil × grup. maternal/paternal
#     partiality (mad 14,30,46 / 13,29,45) Faz III §98 kayirma-kanalidir → HARIC
#     (cift-analiz onlemi). Standardize ortalama fark forest'i (long, aile-
#     clustered) + Benjamini-Hochberg FDR (14 test). α<.50 → betimsel isaret.
#   §118 — Isaretli kardes yas-yonu × bakim asimetrisi. dm_older (DM'li indeks >
#     kardes) ikili moderator × nurturance_asym; age_gap isaretli + kuadratik.
#     YALNIZ DM ailelerinde; betimsel-oncelikli (Tier C, hucre denetimi).
#
# ⚠️ Imputation YAPILMAZ (Kural 19). Korelasyonel dil; nedensel yok.
# ⚠️ Yon konvansiyonu: asym = OF - BY (acik). Tum ciktilar [KESIFSEL - POST-HOC].

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}

dsib_status_label <- function() "[KESIFSEL - POST-HOC]"

dsib_numeric <- function(x) suppressWarnings(as.numeric(x))

dsib_scale <- function(x) {
  x <- dsib_numeric(x); ok <- !is.na(x); out <- rep(NA_real_, length(x))
  if (sum(ok) < 2L) return(out)
  s <- stats::sd(x[ok]); if (is.na(s) || s == 0) return(out)
  out[ok] <- (x[ok] - mean(x[ok])) / s; out
}

dsib_require_columns <- function(df, columns, context) {
  missing <- setdiff(columns, names(df))
  if (length(missing) > 0L) {
    stop(sprintf("%s eksik kolon(lar): %s", context, paste(missing, collapse = ", ")),
      call. = FALSE)
  }
  invisible(TRUE)
}

# 14 non-partiality faset (maternal/paternal partiality HARIC)
dsib_nonpartiality_facets <- function() {
  c("intimacy", "prosocial", "companionship", "similarity",
    "admiration_by_sib", "admiration_of_sib", "affection",
    "nurturance_by_sib", "nurturance_of_sib",
    "dominance_by_sib", "dominance_of_sib",
    "quarreling", "antagonism", "competition")
}

# Faset → SRQ madde no (α icin; srq_first_order_map ile tutarli, self-contained)
dsib_facet_item_map <- function() {
  list(
    intimacy = c(1, 17, 33), prosocial = c(3, 19, 35),
    companionship = c(9, 25, 41), similarity = c(10, 26, 42),
    admiration_by_sib = c(12, 28, 44), admiration_of_sib = c(11, 27, 43),
    affection = c(16, 32, 48),
    nurturance_by_sib = c(8, 24, 40), nurturance_of_sib = c(15, 31, 47),
    dominance_by_sib = c(7, 23, 39), dominance_of_sib = c(2, 18, 34),
    quarreling = c(4, 20, 36), antagonism = c(6, 22, 38), competition = c(5, 21, 37)
  )
}

# Yon-asimetri ciftleri: of_sib - by_sib (+ = raporlayan kardese veriyor/baskin)
dsib_asym_pairs <- function() {
  list(
    nurturance = c("srq_fo_nurturance_of_sib_mean", "srq_fo_nurturance_by_sib_mean"),
    dominance  = c("srq_fo_dominance_of_sib_mean",  "srq_fo_dominance_by_sib_mean"),
    admiration = c("srq_fo_admiration_of_sib_mean", "srq_fo_admiration_by_sib_mean")
  )
}

# 3-maddelik faset α (psych varsa; yoksa standardize-madde Cronbach elle)
dsib_facet_alpha <- function(df, items, item_prefix = "srq") {
  cols <- paste0(item_prefix, "_", items)
  if (!all(cols %in% names(df))) return(NA_real_)
  M <- as.data.frame(lapply(df[cols], dsib_numeric))
  M <- M[stats::complete.cases(M), , drop = FALSE]
  if (nrow(M) < 10L || ncol(M) < 2L) return(NA_real_)
  if (requireNamespace("psych", quietly = TRUE)) {
    a <- tryCatch(suppressWarnings(psych::alpha(M, warnings = FALSE, check.keys = FALSE)),
      error = function(e) NULL)
    if (!is.null(a) && !is.null(a$total$raw_alpha)) return(unname(a$total$raw_alpha))
  }
  k <- ncol(M); v <- stats::var(M)
  (k / (k - 1)) * (1 - sum(diag(v)) / sum(v))
}

# =========================================================================
# Frame hazirlama — long + aile-duzeyi dm_older/age_gap_signed merge
# =========================================================================

dsib_prepare_long <- function(df_long_scored, df_family_scored = NULL) {
  dsib_require_columns(df_long_scored,
    c("aile_no", "group_f", "family_role_f", "cocuk_yas"), "§116 long")
  out <- df_long_scored
  out$group_f <- factor(as.character(out$group_f), levels = c("Kontrol", "DM"))
  out$family_role_f <- factor(as.character(out$family_role_f), levels = c("index", "sibling"))
  out$aile_no_f <- factor(out$aile_no)
  out$cocuk_yas_z <- dsib_scale(out$cocuk_yas)

  # Yon-asimetri skorlari
  for (nm in names(dsib_asym_pairs())) {
    pr <- dsib_asym_pairs()[[nm]]
    if (all(pr %in% names(out))) {
      out[[paste0(nm, "_asym")]] <- dsib_numeric(out[[pr[1L]]]) - dsib_numeric(out[[pr[2L]]])
    } else {
      out[[paste0(nm, "_asym")]] <- rep(NA_real_, nrow(out))
    }
  }

  # Aile-duzeyi isaretli yas farki + dm_older (§118)
  if (!is.null(df_family_scored) &&
      all(c("aile_no", "cocuk_yas", "kardes_yas") %in% names(df_family_scored))) {
    fam <- df_family_scored[!duplicated(df_family_scored$aile_no), , drop = FALSE]
    age_signed <- dsib_numeric(fam$cocuk_yas) - dsib_numeric(fam$kardes_yas)
    dm_older <- ifelse(is.na(age_signed), NA, age_signed > 0)
    m <- match(out$aile_no, fam$aile_no)
    out$age_gap_signed <- age_signed[m]      # indeks - kardes (isaretli)
    out$dm_older <- factor(ifelse(dm_older[m], "DM_buyuk", "DM_kucuk"),
      levels = c("DM_kucuk", "DM_buyuk"))
  } else {
    out$age_gap_signed <- rep(NA_real_, nrow(out))
    out$dm_older <- factor(rep(NA_character_, nrow(out)), levels = c("DM_kucuk", "DM_buyuk"))
  }
  out
}

dsib_lmer_fixed <- function(model, label) {
  ct <- as.data.frame(stats::coef(summary(model)))
  ct$term <- rownames(ct); rownames(ct) <- NULL
  est <- ct[["Estimate"]]; se <- ct[["Std. Error"]]
  dfv <- if ("df" %in% names(ct)) ct[["df"]] else rep(stats::df.residual(model), nrow(ct))
  tcol <- grep("value$", names(ct), value = TRUE)[1L]
  pcol <- grep("^Pr", names(ct), value = TRUE)
  crit <- stats::qt(0.975, df = dfv)
  data.frame(
    label = label, term = ct$term, estimate = est, se = se, df = dfv,
    t_value = ct[[tcol]], p_value = if (length(pcol)) ct[[pcol[1L]]] else NA_real_,
    ci_lower = est - crit * se, ci_upper = est + crit * se,
    n = stats::nobs(model), statu = dsib_status_label(),
    row.names = NULL, stringsAsFactors = FALSE
  )
}

# =========================================================================
# §116 — Yonlu asimetri modelleri + faset guvenilirlik
# =========================================================================

dsib_run_116 <- function(df) {
  fixed_rows <- list(); desc_rows <- list(); rel_rows <- list()
  # Faset α (of/by ayri ayri) — asimetri bilesenleri
  for (nm in names(dsib_asym_pairs())) {
    for (dir in c("of", "by")) {
      facet_key <- paste0(nm, "_", dir, "_sib")
      items <- dsib_facet_item_map()[[facet_key]]
      if (is.null(items)) next
      a <- dsib_facet_alpha(df, items, "srq")
      rel_rows[[facet_key]] <- data.frame(
        asimetri = nm, yon = dir, facet = facet_key, alpha = a,
        guvenilir = !is.na(a) && a >= 0.50, statu = dsib_status_label(),
        stringsAsFactors = FALSE)
    }
  }
  for (nm in names(dsib_asym_pairs())) {
    yv <- paste0(nm, "_asym")
    if (!yv %in% names(df)) next
    d <- dsib_numeric(df[[yv]])
    # betimsel (grup×rol)
    for (g in c("Kontrol", "DM")) {
      for (r in c("index", "sibling")) {
        idx <- which(df$group_f == g & df$family_role_f == r)
        v <- d[idx]; v <- v[!is.na(v)]
        desc_rows[[paste(nm, g, r, sep = "__")]] <- data.frame(
          asimetri = nm, group = g, rol = r, n = length(v),
          asym_ort = if (length(v)) mean(v) else NA_real_,
          asym_medyan = if (length(v)) stats::median(v) else NA_real_,
          asym_sd = if (length(v) > 1L) stats::sd(v) else NA_real_,
          statu = dsib_status_label(), stringsAsFactors = FALSE)
      }
    }
    cols <- c(yv, "group_f", "family_role_f", "cocuk_yas_z", "aile_no_f")
    sub <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
    if (nrow(sub) < 40L) next
    fml <- stats::as.formula(paste0(yv, " ~ group_f * family_role_f + cocuk_yas_z + (1 | aile_no_f)"))
    fit <- tryCatch(suppressMessages(lmerTest::lmer(fml, data = sub, REML = TRUE,
      control = lme4::lmerControl(optimizer = "bobyqa"), na.action = stats::na.exclude)),
      error = function(e) NULL)
    if (!is.null(fit)) fixed_rows[[nm]] <- dsib_lmer_fixed(fit, paste0(nm, "_asym"))
  }
  list(
    asym_fixed = if (length(fixed_rows)) do.call(rbind, fixed_rows) else NULL,
    asym_descriptive = do.call(rbind, desc_rows),
    facet_reliability = do.call(rbind, rel_rows)
  )
}

# =========================================================================
# §117 — 14-faset granuler profil × grup (aile-clustered) + BH-FDR
# =========================================================================

dsib_run_117 <- function(df) {
  facets <- dsib_nonpartiality_facets()
  rows <- list()
  for (fc in facets) {
    yv <- paste0("srq_fo_", fc, "_mean")
    items <- dsib_facet_item_map()[[fc]]
    a <- if (!is.null(items)) dsib_facet_alpha(df, items, "srq") else NA_real_
    if (!yv %in% names(df)) next
    # standardize outcome → std ortalama fark
    dd <- df
    dd$y_z <- dsib_scale(dd[[yv]])
    cols <- c("y_z", "group_f", "cocuk_yas_z", "aile_no_f")
    sub <- dd[stats::complete.cases(dd[, cols, drop = FALSE]), , drop = FALSE]
    if (nrow(sub) < 40L || nlevels(droplevels(sub$group_f)) < 2L) {
      rows[[fc]] <- data.frame(facet = fc, alpha = a, guvenilir = !is.na(a) && a >= .50,
        std_fark = NA_real_, ci_lower = NA_real_, ci_upper = NA_real_,
        p_value = NA_real_, n = nrow(sub), status = "yetersiz",
        statu = dsib_status_label(), stringsAsFactors = FALSE)
      next
    }
    fit <- tryCatch(suppressMessages(lmerTest::lmer(
      y_z ~ group_f + cocuk_yas_z + (1 | aile_no_f), data = sub, REML = TRUE,
      control = lme4::lmerControl(optimizer = "bobyqa"), na.action = stats::na.exclude)),
      error = function(e) NULL)
    if (is.null(fit)) {
      rows[[fc]] <- data.frame(facet = fc, alpha = a, guvenilir = !is.na(a) && a >= .50,
        std_fark = NA_real_, ci_lower = NA_real_, ci_upper = NA_real_,
        p_value = NA_real_, n = nrow(sub), status = "fit_error",
        statu = dsib_status_label(), stringsAsFactors = FALSE)
      next
    }
    fx <- dsib_lmer_fixed(fit, fc)
    g <- fx[fx$term == "group_fDM", , drop = FALSE]
    rows[[fc]] <- data.frame(
      facet = fc, alpha = a, guvenilir = !is.na(a) && a >= .50,
      std_fark = g$estimate, ci_lower = g$ci_lower, ci_upper = g$ci_upper,
      p_value = g$p_value, n = fx$n[1L], status = "ok",
      statu = dsib_status_label(), stringsAsFactors = FALSE)
  }
  out <- do.call(rbind, rows)
  out$p_fdr <- NA_real_
  ok <- which(!is.na(out$p_value))
  if (length(ok) > 0L) out$p_fdr[ok] <- stats::p.adjust(out$p_value[ok], method = "BH")
  out$fdr_hayatta <- !is.na(out$p_fdr) & out$p_fdr < 0.05
  out
}

# =========================================================================
# §118 — Isaretli kardes yas-yonu × bakim asimetrisi (DM-only)
# =========================================================================

dsib_run_118 <- function(df) {
  dm <- df[df$group_f == "DM", , drop = FALSE]
  yv <- "nurturance_asym"
  desc <- NULL; fixed <- NULL
  if (yv %in% names(dm) && "dm_older" %in% names(dm)) {
    # betimsel: dm_older × rol
    drows <- list()
    for (lev in levels(dm$dm_older)) {
      idx <- which(dm$dm_older == lev)
      v <- dsib_numeric(dm[[yv]][idx]); v <- v[!is.na(v)]
      drows[[lev]] <- data.frame(
        dm_older = lev, n = length(v),
        nurturance_asym_ort = if (length(v)) mean(v) else NA_real_,
        nurturance_asym_medyan = if (length(v)) stats::median(v) else NA_real_,
        not = "DM-only; Tier C betimsel-oncelikli (kucuk hucreler, genis CI)",
        statu = dsib_status_label(), stringsAsFactors = FALSE)
    }
    desc <- do.call(rbind, drows)
    cols <- c(yv, "dm_older", "age_gap_signed", "family_role_f", "aile_no_f")
    sub <- dm[stats::complete.cases(dm[, cols, drop = FALSE]), , drop = FALSE]
    if (nrow(sub) >= 40L && nlevels(droplevels(sub$dm_older)) == 2L) {
      sub$age_gap_signed_z <- dsib_scale(sub$age_gap_signed)
      fit <- tryCatch(suppressMessages(lmerTest::lmer(
        stats::as.formula(paste0(yv,
          " ~ dm_older + age_gap_signed_z + I(age_gap_signed_z^2) + family_role_f + (1 | aile_no_f)")),
        data = sub, REML = TRUE, control = lme4::lmerControl(optimizer = "bobyqa"),
        na.action = stats::na.exclude)), error = function(e) NULL)
      if (!is.null(fit)) fixed <- dsib_lmer_fixed(fit, "nurturance_asym|DM-only")
    }
  }
  list(age_direction_descriptive = desc, age_direction_fixed = fixed)
}

# =========================================================================
# Pipeline sarici
# =========================================================================

run_phase4_directional_sibship_pipeline <- function(df_long_scored, df_family_scored = NULL) {
  df <- dsib_prepare_long(df_long_scored, df_family_scored)
  res116 <- dsib_run_116(df)
  res117 <- dsib_run_117(df)
  res118 <- dsib_run_118(df)

  target_summary <- data.frame(
    analysis = "phase4_directional_sibship",
    kisim = "KISIM XLII (§116-118)",
    n_long = nrow(df),
    n_facet_nonpartiality = length(dsib_nonpartiality_facets()),
    yon_konvansiyonu = "asym = OF - BY (+ raporlayan kardese veriyor/baskin)",
    coklu_karsilastirma = "BH-FDR (§117: 14 faset)",
    partiality_harici = "maternal/paternal partiality HARIC (Faz III §98 cift-analiz onlemi)",
    imputation = "YOK (Kural 19)",
    kanit_kategorisi = dsib_status_label(),
    sapma_tipi = "Tip 3 (Faz IV post-hoc, SAP KISIM XLII/116-118)",
    reference_doc = "07-sap-faz4-ek-plan.md",
    stringsAsFactors = FALSE
  )

  list(
    asym_fixed_116 = res116$asym_fixed,
    asym_descriptive_116 = res116$asym_descriptive,
    facet_reliability_116 = res116$facet_reliability,
    facet_forest_117 = res117,
    age_direction_descriptive_118 = res118$age_direction_descriptive,
    age_direction_fixed_118 = res118$age_direction_fixed,
    target_summary = target_summary
  )
}
