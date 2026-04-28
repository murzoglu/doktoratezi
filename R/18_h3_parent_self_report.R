h3_outcome_spec <- function() {
  data.frame(
    outcome = c(
      "embu_p_sicaklik_mean",
      "embu_p_asiri_koruma_mean",
      "embu_p_reddetme_mean",
      "embu_p_karsilastirma_mean"
    ),
    subscale = c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma"),
    label = c(
      "EMBU-P emotional warmth",
      "EMBU-P overprotection",
      "EMBU-P rejection",
      "EMBU-P comparison"
    ),
    family = "EMBU-P",
    stringsAsFactors = FALSE
  )
}

h3_primary_covariates <- function() {
  c("anne_yas", "ses_latent", "age_gap", "cocuk_sayisi")
}

h3_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

h3_scale_vector <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  center <- mean(x, na.rm = TRUE)
  scale <- stats::sd(x, na.rm = TRUE)
  if (is.na(scale) || scale == 0) {
    stop("Cannot z-scale a constant or fully missing vector", call. = FALSE)
  }
  list(value = (x - center) / scale, center = center, scale = scale)
}

h3_normalize_antidepressant <- function(x) {
  if (is.logical(x)) {
    return(ifelse(is.na(x), NA_integer_, as.integer(x)))
  }
  numeric_x <- suppressWarnings(as.numeric(as.character(x)))
  if (!all(is.na(numeric_x))) {
    out <- rep(NA_integer_, length(x))
    out[numeric_x == 0] <- 0L
    out[numeric_x == 1] <- 1L
    return(out)
  }

  value <- tolower(trimws(as.character(x)))
  out <- rep(NA_integer_, length(x))
  out[value %in% c("0", "hayir", "hayır", "yok", "no", "false", "kullanmiyor", "kullanmıyor")] <- 0L
  out[value %in% c("1", "evet", "var", "yes", "true", "kullaniyor", "kullanıyor")] <- 1L
  out
}

h3_propensity_columns <- function() {
  c(
    "ps_value",
    "ps_logit",
    "iptw_stabilized",
    "iptw_trimmed",
    "iptw_trimmed_flag",
    "group_dm",
    "propensity_analysis_row"
  )
}

h3_attach_propensity <- function(df, propensity_data = NULL) {
  if (is.null(propensity_data)) {
    if (all(c("iptw_trimmed", "group_dm") %in% names(df))) {
      return(df)
    }
    if (!exists("derive_propensity_score_pipeline", mode = "function")) {
      stop("H3 IPTW requires propensity data or derive_propensity_score_pipeline()", call. = FALSE)
    }
    propensity_data <- derive_propensity_score_pipeline(df)$data
  }

  h3_require_columns(propensity_data, c("aile_no", "iptw_trimmed", "group_dm"), "H3 propensity data")
  if (anyDuplicated(propensity_data$aile_no) > 0L) {
    stop("H3 propensity data must have one row per family", call. = FALSE)
  }

  keep_columns <- intersect(h3_propensity_columns(), names(propensity_data))
  matched <- match(df$aile_no, propensity_data$aile_no)
  out <- df
  for (column in keep_columns) {
    out[[column]] <- propensity_data[[column]][matched]
  }
  out
}

h3_prepare_analysis_frame <- function(df_family_ses, propensity_data = NULL,
                                      outcomes = h3_outcome_spec()$outcome) {
  h3_require_columns(
    df_family_ses,
    c("aile_no", "group_f", "anne_antidepresan", outcomes, h3_primary_covariates()),
    "H3 family SES data"
  )

  if (anyDuplicated(df_family_ses$aile_no) > 0L) {
    stop("H3 family SES data must have one row per family", call. = FALSE)
  }

  out <- h3_attach_propensity(df_family_ses, propensity_data)
  out$group_f <- factor(as.character(out$group_f), levels = c("Kontrol", "DM"))
  out$anne_antidepresan_bin <- h3_normalize_antidepressant(out$anne_antidepresan)
  out$anne_antidepresan_f <- factor(
    out$anne_antidepresan_bin,
    levels = c(0L, 1L),
    labels = c("Yok", "Var")
  )

  scaling_rows <- lapply(c("anne_yas", "ses_latent", "age_gap"), function(column) {
    scaled <- h3_scale_vector(out[[column]])
    out[[paste0(column, "_z")]] <<- scaled$value
    data.frame(
      variable = column,
      center = scaled$center,
      scale = scaled$scale,
      stringsAsFactors = FALSE
    )
  })
  attr(out, "h3_scaling") <- do.call(rbind, scaling_rows)
  out
}

h3_numeric_descriptives <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  observed <- x[!is.na(x)]
  n <- length(observed)
  data.frame(
    n = n,
    missing_n = sum(is.na(x)),
    mean = if (n > 0L) mean(observed) else NA_real_,
    sd = if (n > 1L) stats::sd(observed) else NA_real_,
    median = if (n > 0L) stats::median(observed) else NA_real_,
    q1 = if (n > 0L) as.numeric(stats::quantile(observed, 0.25, names = FALSE)) else NA_real_,
    q3 = if (n > 0L) as.numeric(stats::quantile(observed, 0.75, names = FALSE)) else NA_real_,
    min = if (n > 0L) min(observed) else NA_real_,
    max = if (n > 0L) max(observed) else NA_real_,
    floor_pct = if (n > 0L) mean(observed <= 1) * 100 else NA_real_,
    ceiling_pct = if (n > 0L) mean(observed >= 4) * 100 else NA_real_,
    stringsAsFactors = FALSE
  )
}

h3_outcome_descriptives <- function(df, outcomes = h3_outcome_spec()$outcome) {
  rows <- list()
  index <- 0L
  for (outcome in outcomes) {
    for (group in levels(df$group_f)) {
      keep <- df$group_f == group
      index <- index + 1L
      rows[[index]] <- data.frame(
        outcome = outcome,
        group = group,
        h3_numeric_descriptives(df[[outcome]][keep]),
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

h3_antidepressant_counts <- function(df) {
  groups <- levels(df$group_f)
  strata <- levels(df$anne_antidepresan_f)
  rows <- list()
  index <- 0L
  for (group in groups) {
    group_keep <- df$group_f == group & !is.na(df$group_f)
    group_n <- sum(group_keep, na.rm = TRUE)
    for (stratum in strata) {
      keep <- group_keep & df$anne_antidepresan_f == stratum
      index <- index + 1L
      rows[[index]] <- data.frame(
        group = group,
        anne_antidepresan = stratum,
        n = sum(keep, na.rm = TRUE),
        group_n = group_n,
        pct_within_group = if (group_n > 0L) sum(keep, na.rm = TRUE) / group_n * 100 else NA_real_,
        stringsAsFactors = FALSE
      )
    }
  }

  dm <- df$group_f == "DM"
  control <- df$group_f == "Kontrol"
  p_dm <- mean(df$anne_antidepresan_bin[dm] == 1L, na.rm = TRUE)
  p_control <- mean(df$anne_antidepresan_bin[control] == 1L, na.rm = TRUE)
  pooled <- sqrt((p_dm * (1 - p_dm) + p_control * (1 - p_control)) / 2)
  smd <- if (is.na(pooled) || pooled == 0) NA_real_ else (p_dm - p_control) / pooled

  out <- do.call(rbind, rows)
  out$dm_minus_control_smd_for_ad_use <- smd
  out
}

h3_primary_formula <- function(outcome) {
  stats::as.formula(paste(outcome, "~ group_f + anne_yas_z + ses_latent_z + age_gap_z + cocuk_sayisi"))
}

h3_stratified_all_formula <- function(outcome) {
  stats::as.formula(paste(outcome, "~ group_f + anne_antidepresan_f + anne_yas_z + ses_latent_z"))
}

h3_stratified_formula <- function(outcome) {
  stats::as.formula(paste(outcome, "~ group_f + anne_yas_z + ses_latent_z"))
}

h3_iptw_formula <- function(outcome) {
  stats::as.formula(paste(outcome, "~ group_f + anne_yas_z + ses_latent_z"))
}

h3_model_columns <- function(formula, weights_column = NULL) {
  unique(c(all.vars(formula), weights_column))
}

h3_model_frame <- function(df, formula, weights_column = NULL) {
  columns <- h3_model_columns(formula, weights_column)
  h3_require_columns(df, columns, "H3 model frame")
  keep <- stats::complete.cases(df[columns])
  if (!is.null(weights_column)) {
    weights <- suppressWarnings(as.numeric(df[[weights_column]]))
    keep <- keep & !is.na(weights) & weights > 0
  }
  model_df <- df[keep, , drop = FALSE]
  if (nrow(model_df) == 0L) {
    stop("H3 model has no complete-case rows", call. = FALSE)
  }
  model_df
}

h3_group_counts <- function(df) {
  c(
    n_dm = sum(df$group_f == "DM", na.rm = TRUE),
    n_control = sum(df$group_f == "Kontrol", na.rm = TRUE)
  )
}

h3_can_fit_group_model <- function(df, min_per_group = 2L) {
  counts <- h3_group_counts(df)
  all(counts >= min_per_group) && nrow(df) > length(counts)
}

h3_fit_lm <- function(df, formula, weights_column = NULL) {
  model_df <- h3_model_frame(df, formula, weights_column)
  if (!h3_can_fit_group_model(model_df, min_per_group = 2L)) {
    stop("H3 model requires both DM and control rows", call. = FALSE)
  }
  if (is.null(weights_column)) {
    return(stats::lm(formula, data = model_df))
  }
  model_df$.h3_weights <- model_df[[weights_column]]
  stats::lm(formula, data = model_df, weights = .h3_weights)
}

h3_vcov_hc3 <- function(model) {
  if (requireNamespace("sandwich", quietly = TRUE)) {
    return(sandwich::vcovHC(model, type = "HC3"))
  }
  stats::vcov(model)
}

h3_covariance_label <- function(robust = FALSE) {
  if (!robust) {
    return("model_based")
  }
  if (requireNamespace("sandwich", quietly = TRUE)) {
    return("HC3_sandwich")
  }
  "model_based_sandwich_unavailable"
}

h3_lm_fixed_effects <- function(model, outcome, model_type, robust = FALSE) {
  estimates <- stats::coef(model)
  vcov_matrix <- if (robust) h3_vcov_hc3(model) else stats::vcov(model)
  std_error <- sqrt(diag(vcov_matrix))
  statistic <- estimates / std_error
  df <- stats::df.residual(model)
  p_value <- 2 * stats::pt(abs(statistic), df = df, lower.tail = FALSE)
  multiplier <- stats::qt(0.975, df = df)
  data.frame(
    model_type = model_type,
    outcome = outcome,
    term = names(estimates),
    estimate = as.numeric(estimates),
    std_error = as.numeric(std_error),
    df = df,
    statistic = as.numeric(statistic),
    p_value = as.numeric(p_value),
    ci_low = as.numeric(estimates - multiplier * std_error),
    ci_high = as.numeric(estimates + multiplier * std_error),
    covariance = h3_covariance_label(robust),
    stringsAsFactors = FALSE
  )
}

h3_lm_diagnostics <- function(model, outcome, model_type, weights_column = NA_character_, robust = FALSE) {
  summary_model <- summary(model)
  model_df <- stats::model.frame(model)
  weights <- stats::weights(model)
  counts <- h3_group_counts(model_df)
  data.frame(
    model_type = model_type,
    outcome = outcome,
    n = stats::nobs(model),
    n_dm = unname(counts[["n_dm"]]),
    n_control = unname(counts[["n_control"]]),
    df_residual = stats::df.residual(model),
    sigma = summary_model$sigma,
    r_squared = summary_model$r.squared,
    adj_r_squared = summary_model$adj.r.squared,
    aic = stats::AIC(model),
    bic = stats::BIC(model),
    weight_column = weights_column,
    weight_mean = if (is.null(weights)) NA_real_ else mean(weights, na.rm = TRUE),
    weight_sd = if (is.null(weights)) NA_real_ else stats::sd(weights, na.rm = TRUE),
    weight_max = if (is.null(weights)) NA_real_ else max(weights, na.rm = TRUE),
    covariance = h3_covariance_label(robust),
    stringsAsFactors = FALSE
  )
}

h3_standardized_group_effect <- function(df, formula, weights_column = NULL, robust = FALSE) {
  model_df <- h3_model_frame(df, formula, weights_column)
  response <- all.vars(formula)[[1L]]
  scaled <- h3_scale_vector(model_df[[response]])
  model_df[[response]] <- scaled$value
  if (is.null(weights_column)) {
    model <- stats::lm(formula, data = model_df)
  } else {
    model_df$.h3_weights <- model_df[[weights_column]]
    model <- stats::lm(formula, data = model_df, weights = .h3_weights)
  }
  table <- h3_lm_fixed_effects(model, response, "standardized_group_effect", robust = robust)
  row <- table[table$term == "group_fDM", , drop = FALSE]
  if (nrow(row) == 0L) {
    return(data.frame(
      std_beta = NA_real_,
      std_beta_ci_low = NA_real_,
      std_beta_ci_high = NA_real_,
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    std_beta = row$estimate[[1L]],
    std_beta_ci_low = row$ci_low[[1L]],
    std_beta_ci_high = row$ci_high[[1L]],
    stringsAsFactors = FALSE
  )
}

h3_group_effect_row <- function(model, df, formula, outcome, model_type, weights_column = NULL,
                                robust = FALSE, status = "fitted", skip_reason = NA_character_) {
  fixed <- h3_lm_fixed_effects(model, outcome, model_type, robust = robust)
  row <- fixed[fixed$term == "group_fDM", , drop = FALSE]
  model_df <- h3_model_frame(df, formula, weights_column)
  counts <- h3_group_counts(model_df)
  std <- h3_standardized_group_effect(df, formula, weights_column, robust = robust)
  data.frame(
    model_type = model_type,
    outcome = outcome,
    term = "group_fDM",
    n = stats::nobs(model),
    n_dm = unname(counts[["n_dm"]]),
    n_control = unname(counts[["n_control"]]),
    estimate = row$estimate[[1L]],
    std_error = row$std_error[[1L]],
    df = row$df[[1L]],
    statistic = row$statistic[[1L]],
    p_value = row$p_value[[1L]],
    ci_low = row$ci_low[[1L]],
    ci_high = row$ci_high[[1L]],
    std_beta = std$std_beta[[1L]],
    std_beta_ci_low = std$std_beta_ci_low[[1L]],
    std_beta_ci_high = std$std_beta_ci_high[[1L]],
    covariance = h3_covariance_label(robust),
    weight_column = if (is.null(weights_column)) NA_character_ else weights_column,
    status = status,
    skip_reason = skip_reason,
    stringsAsFactors = FALSE
  )
}

h3_p_adjust <- function(p_value) {
  out <- rep(NA_real_, length(p_value))
  keep <- !is.na(p_value)
  out[keep] <- stats::p.adjust(p_value[keep], method = "BH")
  out
}

run_h3_primary <- function(df, outcomes = h3_outcome_spec()$outcome) {
  fixed <- list()
  group_effects <- list()
  diagnostics <- list()

  for (outcome in outcomes) {
    formula <- h3_primary_formula(outcome)
    model <- h3_fit_lm(df, formula)
    fixed[[outcome]] <- h3_lm_fixed_effects(model, outcome, "primary_parent_self_report_ancova")
    group_effects[[outcome]] <- h3_group_effect_row(
      model,
      df,
      formula,
      outcome,
      "primary_parent_self_report_ancova"
    )
    diagnostics[[outcome]] <- h3_lm_diagnostics(model, outcome, "primary_parent_self_report_ancova")
  }

  fixed_table <- do.call(rbind, fixed)
  group_table <- do.call(rbind, group_effects)
  group_table$p_fdr_across_h3_primary <- h3_p_adjust(group_table$p_value)

  list(
    fixed_effects = fixed_table,
    group_effects = group_table,
    diagnostics = do.call(rbind, diagnostics)
  )
}

h3_skip_group_effect_row <- function(df, formula, outcome, model_type, stratum, reason,
                                     weights_column = NULL, robust = FALSE) {
  model_df <- tryCatch(h3_model_frame(df, formula, weights_column), error = function(error) df[FALSE, , drop = FALSE])
  counts <- if (nrow(model_df) > 0L && "group_f" %in% names(model_df)) h3_group_counts(model_df) else c(n_dm = 0L, n_control = 0L)
  data.frame(
    model_type = model_type,
    stratum = stratum,
    outcome = outcome,
    term = "group_fDM",
    n = nrow(model_df),
    n_dm = unname(counts[["n_dm"]]),
    n_control = unname(counts[["n_control"]]),
    estimate = NA_real_,
    std_error = NA_real_,
    df = NA_real_,
    statistic = NA_real_,
    p_value = NA_real_,
    ci_low = NA_real_,
    ci_high = NA_real_,
    std_beta = NA_real_,
    std_beta_ci_low = NA_real_,
    std_beta_ci_high = NA_real_,
    covariance = h3_covariance_label(robust),
    weight_column = if (is.null(weights_column)) NA_character_ else weights_column,
    status = "skipped",
    skip_reason = reason,
    stringsAsFactors = FALSE
  )
}

h3_fit_stratum_group_effect <- function(df, formula, outcome, model_type, stratum,
                                        min_per_group = 5L) {
  model_df <- tryCatch(
    h3_model_frame(df, formula),
    error = function(error) error
  )
  if (inherits(model_df, "error")) {
    return(h3_skip_group_effect_row(
      df,
      formula,
      outcome,
      model_type,
      stratum,
      conditionMessage(model_df)
    ))
  }
  if (!h3_can_fit_group_model(model_df, min_per_group = min_per_group)) {
    return(h3_skip_group_effect_row(
      df,
      formula,
      outcome,
      model_type,
      stratum,
      sprintf("fewer_than_%d_per_group", min_per_group)
    ))
  }
  model <- stats::lm(formula, data = model_df)
  row <- h3_group_effect_row(model, df, formula, outcome, model_type)
  row$stratum <- stratum
  row[, c("model_type", "stratum", setdiff(names(row), c("model_type", "stratum"))), drop = FALSE]
}

run_h3_antidepressant_stratified <- function(df, outcomes = h3_outcome_spec()$outcome,
                                             min_per_group = 5L) {
  rows <- list()
  index <- 0L
  no_ad_rows <- !is.na(df$anne_antidepresan_bin) & df$anne_antidepresan_bin == 0L
  ad_rows <- !is.na(df$anne_antidepresan_bin) & df$anne_antidepresan_bin == 1L
  for (outcome in outcomes) {
    all_formula <- h3_stratified_all_formula(outcome)
    no_ad_formula <- h3_stratified_formula(outcome)

    index <- index + 1L
    rows[[index]] <- h3_fit_stratum_group_effect(
      df,
      all_formula,
      outcome,
      "antidepressant_adjusted_sensitivity",
      "all_adjusted_for_antidepressant",
      min_per_group = min_per_group
    )

    index <- index + 1L
    rows[[index]] <- h3_fit_stratum_group_effect(
      df[no_ad_rows, , drop = FALSE],
      no_ad_formula,
      outcome,
      "antidepressant_stratified_sensitivity",
      "no_antidepressant",
      min_per_group = min_per_group
    )

    index <- index + 1L
    rows[[index]] <- h3_fit_stratum_group_effect(
      df[ad_rows, , drop = FALSE],
      no_ad_formula,
      outcome,
      "antidepressant_stratified_sensitivity",
      "antidepressant_only",
      min_per_group = min_per_group
    )
  }

  out <- do.call(rbind, rows)
  out$p_fdr_across_h3_stratified <- h3_p_adjust(out$p_value)
  out
}

run_h3_iptw <- function(df, outcomes = h3_outcome_spec()$outcome,
                        weights_column = "iptw_trimmed") {
  h3_require_columns(df, c(weights_column), "H3 IPTW data")
  fixed <- list()
  group_effects <- list()
  diagnostics <- list()

  for (outcome in outcomes) {
    formula <- h3_iptw_formula(outcome)
    model <- h3_fit_lm(df, formula, weights_column = weights_column)
    fixed[[outcome]] <- h3_lm_fixed_effects(model, outcome, "iptw_parent_self_report_ancova", robust = TRUE)
    group_effects[[outcome]] <- h3_group_effect_row(
      model,
      df,
      formula,
      outcome,
      "iptw_parent_self_report_ancova",
      weights_column = weights_column,
      robust = TRUE
    )
    diagnostics[[outcome]] <- h3_lm_diagnostics(
      model,
      outcome,
      "iptw_parent_self_report_ancova",
      weights_column = weights_column,
      robust = TRUE
    )
  }

  fixed_table <- do.call(rbind, fixed)
  group_table <- do.call(rbind, group_effects)
  group_table$p_fdr_across_h3_iptw <- h3_p_adjust(group_table$p_value)

  list(
    fixed_effects = fixed_table,
    group_effects = group_table,
    diagnostics = do.call(rbind, diagnostics)
  )
}

summarize_h3_targets <- function(analysis_frame, primary, stratified, iptw) {
  data.frame(
    family_rows = nrow(analysis_frame),
    propensity_rows = sum(!is.na(analysis_frame$iptw_trimmed)),
    outcomes = length(h3_outcome_spec()$outcome),
    antidepressant_known_n = sum(!is.na(analysis_frame$anne_antidepresan_bin)),
    antidepressant_yes_n = sum(analysis_frame$anne_antidepresan_bin == 1L, na.rm = TRUE),
    antidepressant_yes_dm_n = sum(analysis_frame$anne_antidepresan_bin == 1L & analysis_frame$group_f == "DM", na.rm = TRUE),
    antidepressant_yes_control_n = sum(analysis_frame$anne_antidepresan_bin == 1L & analysis_frame$group_f == "Kontrol", na.rm = TRUE),
    primary_models = length(unique(primary$diagnostics$outcome)),
    primary_group_fdr_lt_05 = sum(primary$group_effects$p_fdr_across_h3_primary < 0.05, na.rm = TRUE),
    stratified_rows = nrow(stratified),
    stratified_fitted_rows = sum(stratified$status == "fitted", na.rm = TRUE),
    iptw_models = length(unique(iptw$diagnostics$outcome)),
    iptw_group_fdr_lt_05 = sum(iptw$group_effects$p_fdr_across_h3_iptw < 0.05, na.rm = TRUE),
    min_primary_model_n = min(primary$diagnostics$n, na.rm = TRUE),
    max_iptw_weight = max(analysis_frame$iptw_trimmed, na.rm = TRUE),
    stringsAsFactors = FALSE
  )
}

run_h3_parent_self_report_pipeline <- function(df_family_ses, propensity_data = NULL) {
  analysis_frame <- h3_prepare_analysis_frame(df_family_ses, propensity_data)
  primary <- run_h3_primary(analysis_frame)
  stratified <- run_h3_antidepressant_stratified(analysis_frame)
  iptw <- run_h3_iptw(analysis_frame)

  list(
    scaling_summary = attr(analysis_frame, "h3_scaling"),
    outcome_descriptives = h3_outcome_descriptives(analysis_frame),
    antidepressant_counts = h3_antidepressant_counts(analysis_frame),
    primary_fixed_effects = primary$fixed_effects,
    primary_group_effects = primary$group_effects,
    primary_diagnostics = primary$diagnostics,
    antidepressant_stratified_group_effects = stratified,
    iptw_fixed_effects = iptw$fixed_effects,
    iptw_group_effects = iptw$group_effects,
    iptw_diagnostics = iptw$diagnostics,
    target_summary = summarize_h3_targets(analysis_frame, primary, stratified, iptw)
  )
}
