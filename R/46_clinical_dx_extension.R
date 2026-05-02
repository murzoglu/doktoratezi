# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXIX/83-86
# Klinik Karar Modeli Dis Validasyon Hazirligi
#
# 84 — Standardized Net Benefit (sNB; Kerr et al. 2016): NB / NB_max,
#      threshold-bagimsiz tek skalar.
#
# 85 — DCA threshold-sensitivity heatmap: threshold x cost-ratio gridi.
#
# (Not: TRIPOD-Cluster hazirlik dokumani ve recalibration template
#  yeni-veri gerektirdigi icin Faz II'den cikarildi; mevcut veriyle
#  sNB + DCA heatmap ic-validasyon raporlamasi tezde kullanilir.)
#
# Skill referanslari: references/klinik-fayda.md
# Veri: df_family_ses (Beck >= 17 yuksek-risk anne sinifi + EMBU-P alt olcek prediktor)

cdx_high_risk_threshold <- 17L

cdx_subscale_predictors <- function() {
  paste0("embu_p_", c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma"), "_mean")
}

cdx_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(sprintf("%s missing column(s): %s",
      context, paste(missing_columns, collapse = ", ")), call. = FALSE)
  }
  invisible(TRUE)
}

cdx_scale <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

cdx_ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f) - 1L
    } else if ("grup" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$grup), ignore.case = TRUE))
    }
  }
  df
}

cdx_prepare_data <- function(df_family_ses, threshold = cdx_high_risk_threshold) {
  needed <- c("aile_no", "beck_total", "anne_yas", "ses_latent",
    cdx_subscale_predictors())
  cdx_require_columns(df_family_ses, needed, "clinical extension family data")
  df <- cdx_ensure_group_dm(df_family_ses)
  out <- df[stats::complete.cases(df[, needed, drop = FALSE]), , drop = FALSE]
  out$high_risk_anne <- as.integer(out$beck_total >= threshold)
  out$anne_yas_z <- cdx_scale(out$anne_yas)
  out$ses_latent_z <- cdx_scale(out$ses_latent)
  for (col in cdx_subscale_predictors()) {
    out[[paste0(col, "_z")]] <- cdx_scale(out[[col]])
  }
  out
}

# ============================================================================
# Risk Skor Modeli (CSR §12.4 paterni)
# ============================================================================

cdx_fit_risk_model <- function(prepared_data,
                                model_type = c("baseline", "extended")) {
  model_type <- match.arg(model_type)
  if (model_type == "baseline") {
    formula <- stats::as.formula(
      "high_risk_anne ~ group_dm + anne_yas_z + ses_latent_z"
    )
  } else {
    z_preds <- paste0(cdx_subscale_predictors(), "_z")
    formula <- stats::as.formula(sprintf(
      "high_risk_anne ~ group_dm + anne_yas_z + ses_latent_z + %s",
      paste(z_preds, collapse = " + ")
    ))
  }
  fit <- tryCatch(
    stats::glm(formula, data = prepared_data, family = binomial()),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", error_message = conditionMessage(fit)))
  }
  list(
    status = "ok",
    fit = fit,
    model_type = model_type,
    n = stats::nobs(fit),
    auc = cdx_compute_auc(stats::predict(fit, type = "response"),
      prepared_data$high_risk_anne)
  )
}

cdx_compute_auc <- function(predicted, observed) {
  ok <- !is.na(predicted) & !is.na(observed)
  pred <- predicted[ok]
  obs <- observed[ok]
  pos <- pred[obs == 1L]
  neg <- pred[obs == 0L]
  if (length(pos) == 0L || length(neg) == 0L) return(NA_real_)
  combinations <- length(pos) * length(neg)
  wins <- 0
  for (p in pos) {
    wins <- wins + sum(p > neg) + 0.5 * sum(p == neg)
  }
  wins / combinations
}

# ============================================================================
# 84 — Standardized Net Benefit (sNB; Kerr et al. 2016)
# ============================================================================

cdx_net_benefit <- function(predicted, observed, threshold) {
  ok <- !is.na(predicted) & !is.na(observed)
  pred <- predicted[ok]
  obs <- observed[ok]
  n <- length(obs)
  if (n == 0L) return(NA_real_)
  positive <- pred >= threshold
  TP <- sum(positive & obs == 1L)
  FP <- sum(positive & obs == 0L)
  if (threshold >= 1) return(NA_real_)
  (TP / n) - (FP / n) * (threshold / (1 - threshold))
}

cdx_max_net_benefit <- function(observed) {
  ok <- !is.na(observed)
  obs <- observed[ok]
  sum(obs) / length(obs)  # Treat-all en yuksek prevalansa esit
}

cdx_snb_pipeline <- function(prepared_data,
                              thresholds = seq(0.05, 0.50, by = 0.05)) {
  baseline <- cdx_fit_risk_model(prepared_data, model_type = "baseline")
  extended <- cdx_fit_risk_model(prepared_data, model_type = "extended")

  rows <- list()
  for (mt in c("baseline", "extended")) {
    fit_obj <- if (mt == "baseline") baseline else extended
    if (!identical(fit_obj$status, "ok")) next
    pred <- stats::predict(fit_obj$fit, type = "response")
    nb_max <- cdx_max_net_benefit(prepared_data$high_risk_anne)
    for (th in thresholds) {
      nb <- cdx_net_benefit(pred, prepared_data$high_risk_anne, th)
      treat_all_nb <- mean(prepared_data$high_risk_anne, na.rm = TRUE) -
        (1 - mean(prepared_data$high_risk_anne, na.rm = TRUE)) * (th / (1 - th))
      treat_none_nb <- 0
      rows[[length(rows) + 1L]] <- data.frame(
        model_type = mt,
        threshold = th,
        net_benefit_model = nb,
        net_benefit_treat_all = treat_all_nb,
        net_benefit_treat_none = treat_none_nb,
        snb_model = if (!is.na(nb_max) && nb_max > 0) nb / nb_max else NA_real_,
        n_used = length(pred),
        stringsAsFactors = FALSE
      )
    }
  }
  if (length(rows) == 0L) return(NULL)
  do.call(rbind, rows)
}

# ============================================================================
# 85 — DCA Threshold-Sensitivity Heatmap
# ============================================================================

cdx_dca_threshold_heatmap_data <- function(prepared_data,
                                            thresholds = seq(0.05, 0.50, by = 0.05),
                                            cost_ratios = seq(1, 10, by = 1)) {
  extended <- cdx_fit_risk_model(prepared_data, model_type = "extended")
  if (!identical(extended$status, "ok")) return(NULL)
  pred <- stats::predict(extended$fit, type = "response")
  obs <- prepared_data$high_risk_anne
  prev <- mean(obs, na.rm = TRUE)

  rows <- list()
  for (th in thresholds) {
    positive <- pred >= th
    TP <- sum(positive & obs == 1L)
    FP <- sum(positive & obs == 0L)
    n <- length(obs)
    for (cr in cost_ratios) {
      # NB = TP/n - (FP/n) * cr * (th/(1-th))
      nb <- (TP / n) - (FP / n) * cr * (th / (1 - th))
      rows[[length(rows) + 1L]] <- data.frame(
        threshold = th,
        cost_ratio = cr,
        TP = TP, FP = FP,
        n = n, prevalence = prev,
        net_benefit = nb,
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

# ============================================================================
# Pipeline
# ============================================================================

run_clinical_dx_extension_pipeline <- function(df_family_ses,
                                                 thresholds = seq(0.05, 0.50, by = 0.05),
                                                 cost_ratios = seq(1, 10, by = 1),
                                                 high_risk_threshold = cdx_high_risk_threshold) {
  prepared <- cdx_prepare_data(df_family_ses, threshold = high_risk_threshold)

  baseline <- cdx_fit_risk_model(prepared, model_type = "baseline")
  extended <- cdx_fit_risk_model(prepared, model_type = "extended")

  fit_summary <- data.frame(
    model_type = c("baseline", "extended"),
    status = c(baseline$status, extended$status),
    n_used = c(baseline$n %||% NA_integer_, extended$n %||% NA_integer_),
    auc = c(baseline$auc %||% NA_real_, extended$auc %||% NA_real_),
    stringsAsFactors = FALSE
  )

  snb_table <- cdx_snb_pipeline(prepared, thresholds = thresholds)
  dca_heatmap <- cdx_dca_threshold_heatmap_data(prepared,
    thresholds = thresholds, cost_ratios = cost_ratios)

  prepared_summary <- data.frame(
    n_total = nrow(prepared),
    n_high_risk = sum(prepared$high_risk_anne == 1L),
    high_risk_prevalence = mean(prepared$high_risk_anne == 1L),
    high_risk_threshold = high_risk_threshold,
    stringsAsFactors = FALSE
  )

  list(
    prepared_summary = prepared_summary,
    fit_summary = fit_summary,
    snb_table = snb_table,
    dca_heatmap = dca_heatmap,
    target_summary = data.frame(
      analysis = "clinical_dx_extension_phase2",
      n_thresholds = length(thresholds),
      n_cost_ratios = length(cost_ratios),
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXIX/84-85)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
