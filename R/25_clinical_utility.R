# KISIM IX — Klinik Fayda
# 27. Risk skoru geliştirme + ROC + DCA
# 28. CART + Random Forest (variable importance)
# 29. Calibration + NRI/IDI
#
# Hedef: yüksek-riskli anne (Beck >= 17 ~ moderate depression) için lojistik risk skoru.

clinical_outcome <- function() "high_risk_mom"

clinical_predictors_base <- function() {
  c("group_dm", "anne_yas_z", "ses_latent_z", "cocuk_sayisi_z")
}

clinical_predictors_extended <- function() {
  c(clinical_predictors_base(),
    "embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
    "embu_p_reddetme_mean", "embu_p_karsilastirma_mean")
}

clinical_prepare_frame <- function(df_family_ses) {
  df <- df_family_ses
  df$group_f <- factor(as.character(df$group_f), levels = c("Kontrol", "DM"))
  df$group_dm <- as.integer(df$group_f == "DM")
  df$anne_yas_z      <- as.numeric(scale(df$anne_yas))
  df$ses_latent_z    <- as.numeric(scale(df$ses_latent))
  df$cocuk_sayisi_z  <- if ("cocuk_sayisi" %in% names(df)) as.numeric(scale(df$cocuk_sayisi)) else 0
  df$high_risk_mom   <- as.integer(!is.na(df$beck_total) & df$beck_total >= 17)
  df
}

# === 27. Logistic risk score + ROC =====================================

clinical_logistic_risk <- function(df, predictors,
                                    n_boot = 1000L, seed = 20260428L) {
  cols <- c(clinical_outcome(), predictors)
  sub_df <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
  formula_str <- sprintf("%s ~ %s", clinical_outcome(),
                          paste(predictors, collapse = " + "))
  fit <- tryCatch(
    suppressWarnings(stats::glm(stats::as.formula(formula_str),
                                 data = sub_df, family = "binomial")),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = paste0("error:", conditionMessage(fit))))
  }
  pred_prob <- stats::predict(fit, type = "response")
  if (!requireNamespace("pROC", quietly = TRUE)) {
    return(list(status = "pROC_unavailable"))
  }
  roc <- suppressMessages(pROC::roc(sub_df[[clinical_outcome()]], pred_prob))
  auc_val <- as.numeric(pROC::auc(roc))
  ci_auc <- pROC::ci.auc(roc, method = "delong")
  set.seed(seed)
  optimal <- pROC::coords(roc, "best", best.method = "youden",
                           ret = c("threshold", "specificity", "sensitivity",
                                   "ppv", "npv", "youden"))
  if (is.matrix(optimal) || is.data.frame(optimal)) optimal <- optimal[1, , drop = TRUE]
  boot_aucs <- numeric(n_boot)
  for (b in seq_len(n_boot)) {
    idx <- sample(seq_len(nrow(sub_df)), replace = TRUE)
    fit_b <- tryCatch(
      suppressWarnings(stats::glm(stats::as.formula(formula_str),
                                   data = sub_df[idx, , drop = FALSE],
                                   family = "binomial")),
      error = function(e) NULL
    )
    if (is.null(fit_b)) { boot_aucs[b] <- NA_real_; next }
    pred_b <- stats::predict(fit_b, newdata = sub_df, type = "response")
    boot_aucs[b] <- tryCatch(
      as.numeric(pROC::auc(suppressMessages(pROC::roc(sub_df[[clinical_outcome()]], pred_b)))),
      error = function(e) NA_real_
    )
  }
  optimism <- mean(boot_aucs, na.rm = TRUE) - auc_val
  auc_corrected <- auc_val - optimism
  coefs <- summary(fit)$coefficients
  coef_table <- data.frame(
    term     = rownames(coefs),
    estimate = coefs[, 1],
    se       = coefs[, 2],
    z_value  = coefs[, 3],
    p_value  = coefs[, 4],
    or       = exp(coefs[, 1]),
    or_lo    = exp(coefs[, 1] - 1.96 * coefs[, 2]),
    or_hi    = exp(coefs[, 1] + 1.96 * coefs[, 2]),
    stringsAsFactors = FALSE
  )
  performance_table <- data.frame(
    n              = nrow(sub_df),
    n_events       = sum(sub_df[[clinical_outcome()]]),
    auc            = auc_val,
    auc_ci_lo      = ci_auc[1],
    auc_ci_hi      = ci_auc[3],
    auc_corrected  = auc_corrected,
    youden_threshold = unname(optimal["threshold"]),
    sensitivity    = unname(optimal["sensitivity"]),
    specificity    = unname(optimal["specificity"]),
    ppv            = unname(optimal["ppv"]),
    npv            = unname(optimal["npv"]),
    stringsAsFactors = FALSE
  )
  list(status = "ok", fit = fit, predicted = pred_prob,
       coef_table = coef_table, performance_table = performance_table)
}

# === Decision Curve Analysis ==========================================

clinical_decision_curve <- function(df, predicted, outcome_col) {
  if (!requireNamespace("rmda", quietly = TRUE)) {
    return(list(status = "rmda_unavailable"))
  }
  d <- df
  d$predicted <- predicted
  dca <- tryCatch(
    suppressWarnings(rmda::decision_curve(
      stats::as.formula(sprintf("%s ~ predicted", outcome_col)),
      data = d,
      thresholds = seq(0.05, 0.5, by = 0.05),
      bootstraps = 200L
    )),
    error = function(e) e
  )
  if (inherits(dca, "error")) {
    return(list(status = paste0("error:", conditionMessage(dca))))
  }
  dca_df <- dca$derived.data
  thr_col <- if ("thresholds" %in% names(dca_df)) "thresholds" else "threshold"
  model_rows <- if ("model" %in% names(dca_df)) {
    dca_df[grepl("predicted", dca_df$model), , drop = FALSE]
  } else dca_df
  list(
    status = "ok",
    summary_table = data.frame(
      threshold       = model_rows[[thr_col]],
      net_benefit     = model_rows$NB,
      sNB             = model_rows$sNB,
      cost_benefit    = model_rows$cost.benefit.ratio,
      prob_high_risk  = model_rows$prob.high.risk,
      stringsAsFactors = FALSE
    )
  )
}

# === 28. CART + Random Forest =========================================

clinical_cart_rf <- function(df, predictors, seed = 20260428L) {
  if (!requireNamespace("rpart", quietly = TRUE) ||
      !requireNamespace("randomForest", quietly = TRUE)) {
    return(list(status = "packages_unavailable"))
  }
  cols <- c(clinical_outcome(), predictors)
  sub_df <- df[stats::complete.cases(df[, cols, drop = FALSE]), , drop = FALSE]
  sub_df$outcome_factor <- factor(sub_df[[clinical_outcome()]], levels = c(0, 1),
                                   labels = c("Low", "High"))
  formula_str <- sprintf("outcome_factor ~ %s", paste(predictors, collapse = " + "))

  set.seed(seed)
  cart <- tryCatch(
    rpart::rpart(stats::as.formula(formula_str), data = sub_df,
                  method = "class",
                  control = rpart::rpart.control(cp = 0.005, minsplit = 10)),
    error = function(e) e
  )
  cart_table <- if (inherits(cart, "rpart")) {
    cp <- cart$cptable
    data.frame(
      n_splits  = cp[, "nsplit"],
      cp        = cp[, "CP"],
      rel_error = cp[, "rel error"],
      xerror    = cp[, "xerror"],
      xstd      = cp[, "xstd"],
      stringsAsFactors = FALSE
    )
  } else data.frame()

  set.seed(seed)
  rf <- tryCatch(
    randomForest::randomForest(stats::as.formula(formula_str), data = sub_df,
                                ntree = 500L, importance = TRUE),
    error = function(e) e
  )
  rf_imp <- if (inherits(rf, "randomForest")) {
    imp <- randomForest::importance(rf)
    data.frame(
      variable        = rownames(imp),
      mean_decrease_accuracy = imp[, "MeanDecreaseAccuracy"],
      mean_decrease_gini     = imp[, "MeanDecreaseGini"],
      stringsAsFactors = FALSE
    )
  } else data.frame()

  rf_oob <- if (inherits(rf, "randomForest")) {
    rf$err.rate[nrow(rf$err.rate), "OOB"]
  } else NA_real_

  list(
    status            = if (inherits(cart, "rpart") && inherits(rf, "randomForest")) "ok" else "partial",
    cart_cp_table     = cart_table,
    rf_importance_table = rf_imp,
    rf_oob_error      = rf_oob
  )
}

# === 29. Calibration + NRI/IDI =========================================

clinical_calibration <- function(observed, predicted, n_groups = 5L) {
  d <- data.frame(observed = observed, predicted = predicted)
  d <- d[stats::complete.cases(d), , drop = FALSE]
  d <- d[order(d$predicted), , drop = FALSE]
  d$group <- cut(seq_len(nrow(d)), breaks = n_groups, labels = FALSE)
  rows <- list()
  for (g in unique(d$group)) {
    sub <- d[d$group == g, , drop = FALSE]
    rows[[length(rows) + 1L]] <- data.frame(
      decile        = g,
      n             = nrow(sub),
      mean_predicted = mean(sub$predicted),
      mean_observed  = mean(sub$observed),
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

clinical_nri_idi <- function(observed, predicted_base, predicted_full,
                              risk_threshold = 0.20) {
  d <- data.frame(obs = observed, p_base = predicted_base, p_full = predicted_full)
  d <- d[stats::complete.cases(d), , drop = FALSE]
  d$cat_base <- as.integer(d$p_base >= risk_threshold)
  d$cat_full <- as.integer(d$p_full >= risk_threshold)
  events    <- d[d$obs == 1L, , drop = FALSE]
  nonevents <- d[d$obs == 0L, , drop = FALSE]
  up_event   <- mean(events$cat_full > events$cat_base)
  down_event <- mean(events$cat_full < events$cat_base)
  up_ne      <- mean(nonevents$cat_full > nonevents$cat_base)
  down_ne    <- mean(nonevents$cat_full < nonevents$cat_base)
  nri_event  <- up_event - down_event
  nri_ne     <- down_ne - up_ne
  nri_total  <- nri_event + nri_ne
  idi_event  <- mean(events$p_full - events$p_base)
  idi_ne     <- mean(nonevents$p_base - nonevents$p_full)
  idi_total  <- idi_event + idi_ne
  data.frame(
    metric = c("NRI_event", "NRI_nonevent", "NRI_total",
               "IDI_event", "IDI_nonevent", "IDI_total"),
    value  = c(nri_event, nri_ne, nri_total, idi_event, idi_ne, idi_total),
    stringsAsFactors = FALSE
  )
}

# === Pipeline orchestrator =============================================

run_clinical_utility_pipeline <- function(df_family_ses,
                                           seed = 20260428L) {
  prepared <- clinical_prepare_frame(df_family_ses)
  base_predictors     <- clinical_predictors_base()
  extended_predictors <- clinical_predictors_extended()

  base_model <- clinical_logistic_risk(prepared, base_predictors, n_boot = 200L, seed = seed)
  full_model <- clinical_logistic_risk(prepared, extended_predictors, n_boot = 200L, seed = seed)

  status_table <- data.frame(
    component = c("base_logistic", "full_logistic"),
    status = c(base_model$status, full_model$status),
    stringsAsFactors = FALSE
  )
  if (base_model$status != "ok" || full_model$status != "ok") {
    return(list(status_table = status_table))
  }

  dca <- clinical_decision_curve(
    prepared[stats::complete.cases(prepared[, c(clinical_outcome(), extended_predictors), drop = FALSE]), , drop = FALSE],
    full_model$predicted,
    clinical_outcome()
  )
  cart_rf <- clinical_cart_rf(prepared, extended_predictors, seed = seed)

  calibration <- clinical_calibration(
    observed  = prepared[[clinical_outcome()]][stats::complete.cases(prepared[, c(clinical_outcome(), extended_predictors), drop = FALSE])],
    predicted = full_model$predicted
  )
  nri_idi <- clinical_nri_idi(
    observed         = prepared[[clinical_outcome()]][stats::complete.cases(prepared[, c(clinical_outcome(), extended_predictors), drop = FALSE])],
    predicted_base   = base_model$predicted,
    predicted_full   = full_model$predicted,
    risk_threshold   = 0.20
  )

  list(
    status_table         = status_table,
    base_coef_table      = base_model$coef_table,
    base_performance     = base_model$performance_table,
    full_coef_table      = full_model$coef_table,
    full_performance     = full_model$performance_table,
    decision_curve_table = if (!is.null(dca$summary_table)) dca$summary_table else data.frame(),
    cart_cp_table        = if (!is.null(cart_rf$cart_cp_table)) cart_rf$cart_cp_table else data.frame(),
    rf_importance_table  = if (!is.null(cart_rf$rf_importance_table)) cart_rf$rf_importance_table else data.frame(),
    rf_oob_error         = if (!is.null(cart_rf$rf_oob_error)) cart_rf$rf_oob_error else NA_real_,
    calibration_table    = calibration,
    nri_idi_table        = nri_idi
  )
}
