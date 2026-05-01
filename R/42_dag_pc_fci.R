# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXV/70, 72
# DAG Validation + 3-Level Varyans
#
# 70 — DAG Validation: pcalg paketi yoksa dagitty conditional independence
#      implications + manuel partial correlation testleri ile teorik DAG'in
#      veri ile uyumu degerlendirilir. CSR §8.8 DAG-justified ayarlama
#      seti {AgeGap, FamilySize, SES_latent} icin.
#
# 72 — 3-Level Varyans Yapisi: anket_tarihi'nden yil cikarilir; lme4 ile
#      yil x aile x satir random intercept modeli H3 ana etkilerini yeniden
#      tahmin eder. CSR §13.5 negative control flag yanit hatti.
#
# Skill referanslari: references/nedensellik-ve-ps.md,
#                     references/multilevel-aile-yapisi.md

dag_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

dag_anne_outcome <- function(s) paste0("embu_p_", s, "_mean")

dag_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

dag_scale <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

dag_ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f) - 1L
    } else if ("grup" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$grup), ignore.case = TRUE))
    }
  }
  df
}

# ============================================================================
# 70 — DAG Conditional Independence Implications (dagitty + manual)
# ============================================================================

dag_canonical_specification <- function() {
  if (!requireNamespace("dagitty", quietly = TRUE)) {
    return(NULL)
  }
  # CSR §8.8 + CAUSAL-DAG-RUNBOOK.md based DAG
  dag_str <- 'dag {
    Group [exposure]
    AnneRed [outcome]
    SES -> AnneRed
    SES -> Group
    AnneYas -> AnneRed
    AnneYas -> SES
    AgeGap -> AnneRed
    AgeGap -> Group
    FamilySize -> AnneRed
    FamilySize -> Group
    Group -> AnneRed
  }'
  dagitty::dagitty(dag_str)
}

dag_implied_conditional_independencies <- function(dag = NULL) {
  if (is.null(dag)) dag <- dag_canonical_specification()
  if (is.null(dag)) {
    return(data.frame(
      X = character(0), Y = character(0), conditioning_set = character(0),
      stringsAsFactors = FALSE
    ))
  }
  cis <- dagitty::impliedConditionalIndependencies(dag)
  if (length(cis) == 0L) {
    return(data.frame(
      X = character(0), Y = character(0), conditioning_set = character(0),
      stringsAsFactors = FALSE
    ))
  }
  rows <- lapply(cis, function(ci) {
    data.frame(
      X = ci$X,
      Y = ci$Y,
      conditioning_set = paste(ci$Z, collapse = "+"),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

dag_manual_partial_correlation_test <- function(df, x, y, conditioning,
                                                 subscale_label = NA_character_) {
  needed <- c(x, y, conditioning)
  if (any(!needed %in% names(df))) {
    return(data.frame(
      subscale = subscale_label,
      X = x, Y = y,
      conditioning_set = paste(conditioning, collapse = "+"),
      partial_r = NA_real_, n = 0L, p_value = NA_real_,
      ci_implication = "missing_columns",
      stringsAsFactors = FALSE
    ))
  }
  dat <- df[stats::complete.cases(df[, needed]), , drop = FALSE]
  n <- nrow(dat)
  if (n < length(conditioning) + 5L) {
    return(data.frame(
      subscale = subscale_label,
      X = x, Y = y,
      conditioning_set = paste(conditioning, collapse = "+"),
      partial_r = NA_real_, n = n, p_value = NA_real_,
      ci_implication = "insufficient_n",
      stringsAsFactors = FALSE
    ))
  }
  if (length(conditioning) == 0L) {
    pr <- stats::cor.test(dat[[x]], dat[[y]])
    partial_r <- unname(pr$estimate)
    p_val <- unname(pr$p.value)
  } else {
    # Partial correlation: residuals(x|Z) ~ residuals(y|Z)
    fx <- stats::lm(stats::as.formula(sprintf("%s ~ %s", x,
      paste(conditioning, collapse = " + "))), data = dat)
    fy <- stats::lm(stats::as.formula(sprintf("%s ~ %s", y,
      paste(conditioning, collapse = " + "))), data = dat)
    rx <- stats::residuals(fx)
    ry <- stats::residuals(fy)
    pr <- stats::cor.test(rx, ry)
    partial_r <- unname(pr$estimate)
    p_val <- unname(pr$p.value)
  }
  data.frame(
    subscale = subscale_label,
    X = x, Y = y,
    conditioning_set = paste(conditioning, collapse = "+"),
    partial_r = partial_r,
    n = n,
    p_value = p_val,
    ci_implication = if (is.na(p_val)) "indeterminate"
      else if (p_val < 0.05) "rejected"
      else "consistent",
    stringsAsFactors = FALSE
  )
}

dag_validate_implications <- function(df_family_ses,
                                      outcomes = dag_subscale_outcomes()) {
  # Standardize covariate names per DAG specification
  df <- df_family_ses
  rename_map <- c(
    SES = "ses_latent",
    AnneYas = "anne_yas",
    AgeGap = "age_gap",
    FamilySize = "cocuk_sayisi",
    Group = "group_dm"
  )
  for (nm in names(rename_map)) {
    src <- rename_map[[nm]]
    if (src %in% names(df)) df[[nm]] <- df[[src]]
  }

  rows <- list()
  for (sub in outcomes) {
    df$AnneRed <- df[[dag_anne_outcome(sub)]]
    if (!"AnneRed" %in% names(df)) next
    # Test 1: AnneYas _||_ Group | SES
    rows[[paste(sub, "AnneYas_Group_given_SES", sep = "_")]] <-
      dag_manual_partial_correlation_test(df, "AnneYas", "Group", "SES",
        subscale_label = sub)
    # Test 2: AgeGap _||_ AnneYas | (no conditioning, two roots)
    rows[[paste(sub, "AgeGap_AnneYas_marginal", sep = "_")]] <-
      dag_manual_partial_correlation_test(df, "AgeGap", "AnneYas", character(0),
        subscale_label = sub)
    # Test 3: FamilySize _||_ AnneYas | (no conditioning)
    rows[[paste(sub, "FamilySize_AnneYas_marginal", sep = "_")]] <-
      dag_manual_partial_correlation_test(df, "FamilySize", "AnneYas",
        character(0), subscale_label = sub)
  }
  if (length(rows) == 0L) return(NULL)
  do.call(rbind, rows)
}

# ============================================================================
# 72 — 3-Level Varyans Yapisi (Yil x Aile x Satir)
# ============================================================================

dag_extract_year <- function(date_str) {
  if (is.null(date_str) || all(is.na(date_str))) return(rep(NA_integer_, length(date_str)))
  parts <- strsplit(as.character(date_str), "[./-]")
  yr <- vapply(parts, function(p) {
    if (length(p) >= 3L) {
      candidates <- suppressWarnings(as.integer(p))
      candidates <- candidates[!is.na(candidates) & candidates >= 1900 & candidates <= 2100]
      if (length(candidates) > 0L) candidates[1L] else NA_integer_
    } else NA_integer_
  }, integer(1L))
  yr
}

dag_three_level_one <- function(long_data, outcome_subscale) {
  outcome <- paste0("embu_c_", outcome_subscale, "_mean")
  needed <- c(outcome, "group_dm", "ses_latent_z", "anne_yas_z",
    "aile_no", "kayit_yili")
  if (any(!needed %in% names(long_data))) {
    return(data.frame(
      outcome_subscale = outcome_subscale,
      status = "missing_columns",
      missing = paste(setdiff(needed, names(long_data)), collapse = ", "),
      stringsAsFactors = FALSE
    ))
  }
  if (!requireNamespace("lme4", quietly = TRUE)) {
    return(data.frame(
      outcome_subscale = outcome_subscale,
      status = "lme4_unavailable",
      stringsAsFactors = FALSE
    ))
  }
  dat <- long_data[stats::complete.cases(long_data[, needed]), , drop = FALSE]
  if (length(unique(dat$kayit_yili)) < 2L) {
    return(data.frame(
      outcome_subscale = outcome_subscale,
      status = "insufficient_year_levels",
      n_year_levels = length(unique(dat$kayit_yili)),
      stringsAsFactors = FALSE
    ))
  }

  # 2-level baseline: (1 | aile_no)
  formula_2l <- stats::as.formula(sprintf(
    "%s ~ group_dm + ses_latent_z + anne_yas_z + (1 | aile_no)", outcome
  ))
  fit_2l <- tryCatch(lme4::lmer(formula_2l, data = dat), error = function(e) e)

  # 3-level: (1 | kayit_yili) + (1 | aile_no)
  formula_3l <- stats::as.formula(sprintf(
    "%s ~ group_dm + ses_latent_z + anne_yas_z + (1 | kayit_yili) + (1 | aile_no)",
    outcome
  ))
  fit_3l <- tryCatch(lme4::lmer(formula_3l, data = dat), error = function(e) e)

  if (inherits(fit_2l, "error") || inherits(fit_3l, "error")) {
    return(data.frame(
      outcome_subscale = outcome_subscale,
      status = "fit_error",
      error_message = conditionMessage(if (inherits(fit_2l, "error")) fit_2l else fit_3l),
      stringsAsFactors = FALSE
    ))
  }

  vcov_2l <- as.data.frame(lme4::VarCorr(fit_2l))
  vcov_3l <- as.data.frame(lme4::VarCorr(fit_3l))

  icc_aile_2l <- vcov_2l$vcov[vcov_2l$grp == "aile_no"] /
    sum(vcov_2l$vcov)
  icc_aile_3l <- vcov_3l$vcov[vcov_3l$grp == "aile_no"] /
    sum(vcov_3l$vcov)
  icc_yil_3l <- vcov_3l$vcov[vcov_3l$grp == "kayit_yili"] /
    sum(vcov_3l$vcov)

  cs_2l <- summary(fit_2l)$coefficients
  cs_3l <- summary(fit_3l)$coefficients
  group_2l <- cs_2l["group_dm", , drop = FALSE]
  group_3l <- cs_3l["group_dm", , drop = FALSE]

  lrt <- stats::anova(fit_2l, fit_3l)

  data.frame(
    outcome_subscale = outcome_subscale,
    status = "ok",
    n_used = stats::nobs(fit_3l),
    n_year_levels = length(unique(dat$kayit_yili)),
    icc_family_2level = icc_aile_2l,
    icc_family_3level = icc_aile_3l,
    icc_year_3level = icc_yil_3l,
    group_dm_2level = group_2l[1L, "Estimate"],
    group_dm_se_2level = group_2l[1L, "Std. Error"],
    group_dm_3level = group_3l[1L, "Estimate"],
    group_dm_se_3level = group_3l[1L, "Std. Error"],
    se_inflation_pct = 100 * (group_3l[1L, "Std. Error"] / group_2l[1L, "Std. Error"] - 1),
    lrt_chisq = lrt$Chisq[2L],
    lrt_p = lrt$`Pr(>Chisq)`[2L],
    decision = if (!is.na(lrt$`Pr(>Chisq)`[2L]) && lrt$`Pr(>Chisq)`[2L] < 0.05) {
      "year_clustering_relevant"
    } else {
      "year_clustering_negligible"
    },
    stringsAsFactors = FALSE
  )
}

dag_three_level_pipeline <- function(long_data,
                                     outcomes = dag_subscale_outcomes()) {
  rows <- list()
  for (sub in outcomes) {
    rows[[sub]] <- dag_three_level_one(long_data, sub)
  }
  # Combine with consistent columns
  bind_safe <- function(rows) {
    all_cols <- unique(unlist(lapply(rows, names)))
    rows_padded <- lapply(rows, function(r) {
      missing_cols <- setdiff(all_cols, names(r))
      for (mc in missing_cols) r[[mc]] <- NA
      r[, all_cols, drop = FALSE]
    })
    do.call(rbind, rows_padded)
  }
  bind_safe(rows)
}

# ============================================================================
# Pipeline
# ============================================================================

run_dag_pc_fci_pipeline <- function(df_family_ses, df_long_scored,
                                    outcomes = dag_subscale_outcomes()) {
  # 70 — DAG implications + partial correlation tests
  fam <- dag_ensure_group_dm(df_family_ses)
  ci_table <- dag_validate_implications(fam, outcomes = outcomes)

  # Implied CIs from dagitty (for catalogue)
  implied_cis <- dag_implied_conditional_independencies()

  # 72 — 3-level model (yil x aile x satir)
  long <- df_long_scored
  long$role_token <- dag_normalize_role(long$family_role_f)
  long <- long[!is.na(long$role_token), , drop = FALSE]
  if ("anket_tarihi" %in% names(long)) {
    long$kayit_yili <- dag_extract_year(long$anket_tarihi)
  } else if ("anket_tarihi" %in% names(fam)) {
    long$kayit_yili <- dag_extract_year(fam$anket_tarihi)[
      match(long$aile_no, fam$aile_no)
    ]
  } else {
    long$kayit_yili <- NA_integer_
  }
  fam_join <- fam[, c("aile_no", "group_dm", "ses_latent", "anne_yas",
    if ("anket_tarihi" %in% names(fam)) "anket_tarihi" else NULL), drop = FALSE]
  fam_join$ses_latent_z <- dag_scale(fam_join$ses_latent)
  fam_join$anne_yas_z <- dag_scale(fam_join$anne_yas)
  long_full <- merge(long, fam_join, by = "aile_no", all.x = TRUE,
    suffixes = c("", ".fam"))
  if (all(is.na(long_full$kayit_yili)) && "anket_tarihi.fam" %in% names(long_full)) {
    long_full$kayit_yili <- dag_extract_year(long_full$anket_tarihi.fam)
  }

  three_level_table <- dag_three_level_pipeline(long_full, outcomes = outcomes)

  list(
    implied_conditional_independencies = implied_cis,
    ci_test_results = ci_table,
    three_level_table = three_level_table,
    n_long = nrow(long_full),
    n_year_levels = length(unique(stats::na.omit(long_full$kayit_yili))),
    target_summary = data.frame(
      analysis = "dag_pc_fci_phase2",
      pcalg_used = FALSE,
      dagitty_used = requireNamespace("dagitty", quietly = TRUE),
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXV/70, 72)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      pc_algoritma_notu = "pcalg yoksa dagitty implications + manuel partial correlation",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
