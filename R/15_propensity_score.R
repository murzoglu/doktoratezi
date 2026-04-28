propensity_primary_covariates <- function() {
  c("ses_latent", "age_gap", "cocuk_sayisi")
}

propensity_sensitivity_covariates <- function(df = NULL) {
  candidates <- c(
    propensity_primary_covariates(),
    "anne_yas",
    "egitim_durumu",
    "es_egitim_durumu",
    "aile_isei08",
    "ev_sahipligi",
    "ev_oda_sayisi",
    "arabaniz_var_mi",
    "kronik_hastalik_durumu"
  )
  if (is.null(df)) {
    return(candidates)
  }
  candidates[candidates %in% names(df)]
}

propensity_excluded_total_effect_covariates <- function() {
  c("anne_antidepresan", "beck_total", "beck_clinical", "embu_p_sicaklik_mean", "embu_p_reddetme_mean")
}

propensity_default_outcome_plan <- function() {
  data.frame(
    outcome = c(
      "embu_p_sicaklik_mean",
      "embu_p_asiri_koruma_mean",
      "embu_p_reddetme_mean",
      "embu_p_karsilastirma_mean",
      "embu_c_idx_sicaklik_mean",
      "embu_c_idx_asiri_koruma_mean",
      "embu_c_idx_reddetme_mean",
      "embu_c_idx_karsilastirma_mean",
      "srq_ho_warmth_mean",
      "srq_ho_status_mean",
      "srq_ho_conflict_mean",
      "srq_ho_rivalry_mean"
    ),
    outcome_family = c(
      rep("EMBU-P", 4L),
      rep("EMBU-C index", 4L),
      rep("SRQ/KIA", 4L)
    ),
    analysis_phase = c(
      rep("H3_family_parenting", 4L),
      rep("H1_child_perception", 4L),
      rep("H2_sibling_relations", 4L)
    ),
    stringsAsFactors = FALSE
  )
}

propensity_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

propensity_group_levels <- function(group, treatment_level = "DM", control_level = "Kontrol") {
  observed <- unique(as.character(group[!is.na(group)]))
  preferred <- c(treatment_level, control_level)
  if (all(preferred %in% observed)) {
    return(preferred)
  }
  observed <- sort(observed)
  if (length(observed) != 2L) {
    stop("Propensity score requires exactly two non-missing group levels", call. = FALSE)
  }
  observed
}

propensity_variable_type <- function(x) {
  if (is.logical(x)) {
    return("binary")
  }
  observed <- unique(x[!is.na(x)])
  if (is.numeric(x) || is.integer(x)) {
    if (length(observed) <= 2L) {
      return("binary")
    }
    return("continuous")
  }
  if (length(unique(as.character(observed))) <= 2L) {
    return("binary")
  }
  "categorical"
}

propensity_target_level <- function(x) {
  values <- sort(unique(as.character(x[!is.na(x)])))
  if ("1" %in% values) {
    return("1")
  }
  if ("Evet" %in% values) {
    return("Evet")
  }
  values[[length(values)]]
}

propensity_weighted_mean <- function(x, weights = NULL) {
  x <- suppressWarnings(as.numeric(x))
  if (is.null(weights)) {
    observed <- x[!is.na(x)]
    if (length(observed) == 0L) {
      return(NA_real_)
    }
    return(mean(observed))
  }
  weights <- suppressWarnings(as.numeric(weights))
  keep <- !is.na(x) & !is.na(weights) & weights > 0
  if (!any(keep)) {
    return(NA_real_)
  }
  sum(weights[keep] * x[keep]) / sum(weights[keep])
}

propensity_weighted_variance <- function(x, weights = NULL) {
  x <- suppressWarnings(as.numeric(x))
  if (is.null(weights)) {
    observed <- x[!is.na(x)]
    if (length(observed) < 2L) {
      return(NA_real_)
    }
    return(stats::var(observed))
  }
  weights <- suppressWarnings(as.numeric(weights))
  keep <- !is.na(x) & !is.na(weights) & weights > 0
  if (sum(keep) < 2L) {
    return(NA_real_)
  }
  mu <- sum(weights[keep] * x[keep]) / sum(weights[keep])
  sum(weights[keep] * (x[keep] - mu)^2) / sum(weights[keep])
}

propensity_weighted_proportion <- function(x, level, weights = NULL) {
  indicator <- as.numeric(as.character(x) == level)
  indicator[is.na(x)] <- NA_real_
  propensity_weighted_mean(indicator, weights)
}

propensity_smd_continuous <- function(x, treatment, weights = NULL) {
  treatment <- as.integer(treatment)
  x1 <- x[treatment == 1L]
  x0 <- x[treatment == 0L]
  w1 <- if (is.null(weights)) NULL else weights[treatment == 1L]
  w0 <- if (is.null(weights)) NULL else weights[treatment == 0L]
  m1 <- propensity_weighted_mean(x1, w1)
  m0 <- propensity_weighted_mean(x0, w0)
  v1 <- propensity_weighted_variance(x1, w1)
  v0 <- propensity_weighted_variance(x0, w0)
  pooled <- sqrt((v1 + v0) / 2)
  smd <- if (is.na(pooled) || pooled == 0) NA_real_ else (m1 - m0) / pooled
  data.frame(
    smd = smd,
    abs_smd = abs(smd),
    smd_method = if (is.null(weights)) "mean_difference_pooled_sd" else "weighted_mean_difference_pooled_sd",
    smd_level = NA_character_,
    stringsAsFactors = FALSE
  )
}

propensity_smd_binary <- function(x, treatment, weights = NULL, target_level = propensity_target_level(x)) {
  treatment <- as.integer(treatment)
  p1 <- propensity_weighted_proportion(x[treatment == 1L], target_level, if (is.null(weights)) NULL else weights[treatment == 1L])
  p0 <- propensity_weighted_proportion(x[treatment == 0L], target_level, if (is.null(weights)) NULL else weights[treatment == 0L])
  pooled <- sqrt((p1 * (1 - p1) + p0 * (1 - p0)) / 2)
  smd <- if (is.na(pooled) || pooled == 0) NA_real_ else (p1 - p0) / pooled
  data.frame(
    smd = smd,
    abs_smd = abs(smd),
    smd_method = if (is.null(weights)) "binary_proportion_pooled_sd" else "weighted_binary_proportion_pooled_sd",
    smd_level = target_level,
    stringsAsFactors = FALSE
  )
}

propensity_smd_categorical <- function(x, treatment, weights = NULL) {
  levels_observed <- sort(unique(as.character(x[!is.na(x)])))
  if (length(levels_observed) == 0L) {
    return(data.frame(
      smd = NA_real_,
      abs_smd = NA_real_,
      smd_method = "max_abs_level_smd",
      smd_level = NA_character_,
      stringsAsFactors = FALSE
    ))
  }
  rows <- lapply(levels_observed, function(level) {
    propensity_smd_binary(x, treatment, weights = weights, target_level = level)
  })
  out <- do.call(rbind, rows)
  idx <- which.max(out$abs_smd)
  data.frame(
    smd = out$smd[[idx]],
    abs_smd = out$abs_smd[[idx]],
    smd_method = if (is.null(weights)) "max_abs_level_smd" else "weighted_max_abs_level_smd",
    smd_level = out$smd_level[[idx]],
    stringsAsFactors = FALSE
  )
}

propensity_smd_for_variable <- function(x, treatment, weights = NULL, type = propensity_variable_type(x)) {
  if (type == "continuous") {
    return(propensity_smd_continuous(x, treatment, weights))
  }
  if (type == "binary") {
    return(propensity_smd_binary(x, treatment, weights))
  }
  propensity_smd_categorical(x, treatment, weights)
}

propensity_balance_flag <- function(abs_smd) {
  if (is.na(abs_smd)) {
    return("degerlendirilemedi")
  }
  if (abs_smd < 0.10) {
    return("iyi_denge")
  }
  if (abs_smd < 0.20) {
    return("sinirda")
  }
  if (abs_smd < 0.40) {
    return("dengesiz")
  }
  "ciddi_dengesizlik"
}

propensity_balance_recommendation <- function(abs_smd) {
  flag <- propensity_balance_flag(abs_smd)
  switch(
    flag,
    iyi_denge = "primary_adjustment_ok",
    sinirda = "report_and_monitor",
    dengesiz = "sensitivity_required",
    ciddi_dengesizlik = "strong_sensitivity_required",
    "inspect"
  )
}

propensity_prepare_analysis_frame <- function(df, covariates = propensity_primary_covariates(),
                                              group_column = "group", treatment_level = "DM",
                                              control_level = "Kontrol") {
  propensity_require_columns(df, c(group_column, covariates), "Propensity score")
  group_levels <- propensity_group_levels(df[[group_column]], treatment_level, control_level)
  keep <- !is.na(df[[group_column]]) & as.character(df[[group_column]]) %in% group_levels
  for (covariate in covariates) {
    keep <- keep & !is.na(df[[covariate]])
  }
  analysis <- df[keep, , drop = FALSE]
  if (nrow(analysis) == 0L) {
    stop("Propensity score has no complete-case rows for selected covariates", call. = FALSE)
  }
  analysis$group_dm <- as.integer(as.character(analysis[[group_column]]) == group_levels[[1L]])
  if (length(unique(analysis$group_dm)) != 2L) {
    stop("Propensity score complete-case frame must contain both treatment groups", call. = FALSE)
  }
  analysis$propensity_analysis_row <- seq_len(nrow(analysis))
  attr(analysis, "excluded_rows") <- nrow(df) - nrow(analysis)
  attr(analysis, "group_levels") <- group_levels
  analysis
}

propensity_formula <- function(covariates = propensity_primary_covariates(), response = "group_dm") {
  stats::reformulate(covariates, response = response)
}

estimate_propensity_scores <- function(df, covariates = propensity_primary_covariates(),
                                       group_column = "group", treatment_level = "DM",
                                       control_level = "Kontrol", trim_quantile = 0.99,
                                       eps = 1e-6) {
  analysis <- propensity_prepare_analysis_frame(
    df,
    covariates = covariates,
    group_column = group_column,
    treatment_level = treatment_level,
    control_level = control_level
  )
  model <- stats::glm(
    propensity_formula(covariates),
    data = analysis,
    family = stats::binomial()
  )
  ps_value <- as.numeric(stats::predict(model, type = "response"))
  ps_value <- pmin(pmax(ps_value, eps), 1 - eps)
  analysis$ps_value <- ps_value
  analysis$ps_logit <- stats::qlogis(ps_value)

  prop_treated <- mean(analysis$group_dm == 1L)
  analysis$iptw_stabilized <- ifelse(
    analysis$group_dm == 1L,
    prop_treated / analysis$ps_value,
    (1 - prop_treated) / (1 - analysis$ps_value)
  )
  cutoff <- as.numeric(stats::quantile(analysis$iptw_stabilized, trim_quantile, na.rm = TRUE, names = FALSE))
  analysis$iptw_trimmed <- pmin(analysis$iptw_stabilized, cutoff)
  analysis$iptw_trimmed_flag <- analysis$iptw_stabilized > cutoff

  list(
    data = analysis,
    model = model,
    formula = deparse(propensity_formula(covariates), width.cutoff = 500L),
    covariates = covariates,
    treatment_level = attr(analysis, "group_levels")[[1L]],
    control_level = attr(analysis, "group_levels")[[2L]],
    excluded_rows = attr(analysis, "excluded_rows"),
    trim_quantile = trim_quantile,
    trim_cutoff = cutoff
  )
}

propensity_model_summary <- function(ps_fit) {
  coefficients <- as.data.frame(stats::coef(summary(ps_fit$model)))
  coefficients$term <- rownames(coefficients)
  rownames(coefficients) <- NULL
  names(coefficients) <- sub("^Estimate$", "estimate", names(coefficients))
  names(coefficients) <- sub("^Std\\. Error$", "std_error", names(coefficients))
  names(coefficients) <- sub("^z value$", "z_value", names(coefficients))
  names(coefficients) <- sub("^Pr\\(>\\|z\\|\\)$", "p_value", names(coefficients))
  coefficients$odds_ratio <- exp(coefficients$estimate)
  coefficients$or_ci_low <- exp(coefficients$estimate - stats::qnorm(0.975) * coefficients$std_error)
  coefficients$or_ci_high <- exp(coefficients$estimate + stats::qnorm(0.975) * coefficients$std_error)
  coefficients$model <- "logit_primary"
  coefficients$formula <- ps_fit$formula[[1L]]
  coefficients[, c(
    "model", "formula", "term", "estimate", "std_error", "z_value",
    "p_value", "odds_ratio", "or_ci_low", "or_ci_high"
  )]
}

propensity_distribution_row <- function(df, group_label, rows, trim_cutoff) {
  ps <- df$ps_value[rows]
  weight <- df$iptw_stabilized[rows]
  trimmed_weight <- df$iptw_trimmed[rows]
  data.frame(
    group = group_label,
    n = sum(rows),
    ps_mean = mean(ps, na.rm = TRUE),
    ps_sd = stats::sd(ps, na.rm = TRUE),
    ps_min = min(ps, na.rm = TRUE),
    ps_p25 = as.numeric(stats::quantile(ps, 0.25, na.rm = TRUE, names = FALSE)),
    ps_median = stats::median(ps, na.rm = TRUE),
    ps_p75 = as.numeric(stats::quantile(ps, 0.75, na.rm = TRUE, names = FALSE)),
    ps_max = max(ps, na.rm = TRUE),
    iptw_mean = mean(weight, na.rm = TRUE),
    iptw_sd = stats::sd(weight, na.rm = TRUE),
    iptw_max = max(weight, na.rm = TRUE),
    iptw_trimmed_mean = mean(trimmed_weight, na.rm = TRUE),
    iptw_trimmed_max = max(trimmed_weight, na.rm = TRUE),
    trim_cutoff = trim_cutoff,
    trimmed_n = sum(df$iptw_trimmed_flag[rows], na.rm = TRUE),
    stringsAsFactors = FALSE
  )
}

propensity_weight_summary <- function(ps_fit) {
  df <- ps_fit$data
  rows <- list(
    propensity_distribution_row(df, "overall", rep(TRUE, nrow(df)), ps_fit$trim_cutoff),
    propensity_distribution_row(df, ps_fit$treatment_level, df$group_dm == 1L, ps_fit$trim_cutoff),
    propensity_distribution_row(df, ps_fit$control_level, df$group_dm == 0L, ps_fit$trim_cutoff)
  )
  do.call(rbind, rows)
}

propensity_balance_one <- function(df, covariates, weight_column = NULL, label = "unweighted") {
  weights <- if (is.null(weight_column)) NULL else df[[weight_column]]
  rows <- lapply(covariates, function(covariate) {
    type <- propensity_variable_type(df[[covariate]])
    smd <- propensity_smd_for_variable(df[[covariate]], df$group_dm, weights = weights, type = type)
    data.frame(
      variable = covariate,
      variable_type = type,
      balance_stage = label,
      weight_column = if (is.null(weight_column)) NA_character_ else weight_column,
      smd = smd$smd,
      abs_smd = smd$abs_smd,
      smd_method = smd$smd_method,
      smd_level = smd$smd_level,
      balance_flag = propensity_balance_flag(smd$abs_smd),
      recommendation = propensity_balance_recommendation(smd$abs_smd),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

propensity_balance_before_after <- function(df, covariates, matched_df = NULL) {
  unweighted <- propensity_balance_one(df, covariates, label = "before_unweighted")
  weighted <- propensity_balance_one(df, covariates, weight_column = "iptw_trimmed", label = "after_iptw_trimmed")
  matched <- if (!is.null(matched_df) && nrow(matched_df) > 0L) {
    propensity_balance_one(matched_df, covariates, label = "after_nearest_neighbor_matching")
  } else {
    empty <- unweighted
    empty$balance_stage <- "after_nearest_neighbor_matching"
    empty$smd <- NA_real_
    empty$abs_smd <- NA_real_
    empty$balance_flag <- "degerlendirilemedi"
    empty$recommendation <- "inspect"
    empty
  }

  merged <- merge(
    unweighted[, c("variable", "variable_type", "smd", "abs_smd", "balance_flag")],
    weighted[, c("variable", "smd", "abs_smd", "balance_flag", "recommendation")],
    by = "variable",
    suffixes = c("_before", "_iptw"),
    all = TRUE
  )
  merged <- merge(
    merged,
    matched[, c("variable", "smd", "abs_smd", "balance_flag")],
    by = "variable",
    all = TRUE
  )
  names(merged)[names(merged) == "smd"] <- "smd_matched"
  names(merged)[names(merged) == "abs_smd"] <- "abs_smd_matched"
  names(merged)[names(merged) == "balance_flag"] <- "balance_flag_matched"
  merged$abs_smd_change_iptw <- merged$abs_smd_before - merged$abs_smd_iptw
  merged$abs_smd_change_matched <- merged$abs_smd_before - merged$abs_smd_matched
  merged <- merged[order(-merged$abs_smd_before, merged$variable), , drop = FALSE]
  rownames(merged) <- NULL
  merged
}

propensity_nearest_neighbor_pairs <- function(df, caliper = NULL) {
  propensity_require_columns(df, c("group_dm", "ps_logit"), "Propensity matching")
  treated <- which(df$group_dm == 1L)
  controls <- which(df$group_dm == 0L)
  if (length(treated) == 0L || length(controls) == 0L) {
    stop("Propensity matching requires treated and control rows", call. = FALSE)
  }
  if (is.null(caliper)) {
    caliper <- 0.2 * stats::sd(df$ps_logit, na.rm = TRUE)
  }
  available_controls <- controls
  treated <- treated[order(df$ps_logit[treated])]
  pairs <- vector("list", length(treated))
  pair_count <- 0L
  for (treated_row in treated) {
    if (length(available_controls) == 0L) {
      break
    }
    distances <- abs(df$ps_logit[available_controls] - df$ps_logit[treated_row])
    best_pos <- which.min(distances)
    if (length(best_pos) == 0L || is.na(distances[[best_pos]]) || distances[[best_pos]] > caliper) {
      next
    }
    control_row <- available_controls[[best_pos]]
    pair_count <- pair_count + 1L
    pairs[[pair_count]] <- data.frame(
      pair_id = pair_count,
      treated_row = treated_row,
      control_row = control_row,
      abs_logit_distance = distances[[best_pos]],
      stringsAsFactors = FALSE
    )
    available_controls <- setdiff(available_controls, control_row)
  }
  if (pair_count == 0L) {
    return(data.frame(
      pair_id = integer(),
      treated_row = integer(),
      control_row = integer(),
      abs_logit_distance = numeric(),
      stringsAsFactors = FALSE
    ))
  }
  do.call(rbind, pairs[seq_len(pair_count)])
}

propensity_matched_data <- function(df, pairs) {
  if (nrow(pairs) == 0L) {
    return(df[FALSE, , drop = FALSE])
  }
  treated <- df[pairs$treated_row, , drop = FALSE]
  control <- df[pairs$control_row, , drop = FALSE]
  treated$matched_pair_id <- pairs$pair_id
  control$matched_pair_id <- pairs$pair_id
  rbind(treated, control)
}

propensity_matching_summary <- function(df, pairs, caliper) {
  data.frame(
    method = "greedy_nearest_neighbor_1to1_without_replacement",
    distance = "logit_propensity_score",
    caliper = caliper,
    treated_n = sum(df$group_dm == 1L),
    control_n = sum(df$group_dm == 0L),
    matched_pairs = nrow(pairs),
    matched_treated_n = nrow(pairs),
    matched_control_n = nrow(pairs),
    unmatched_treated_n = sum(df$group_dm == 1L) - nrow(pairs),
    unmatched_control_n = sum(df$group_dm == 0L) - nrow(pairs),
    mean_abs_logit_distance = if (nrow(pairs) > 0L) mean(pairs$abs_logit_distance) else NA_real_,
    max_abs_logit_distance = if (nrow(pairs) > 0L) max(pairs$abs_logit_distance) else NA_real_,
    stringsAsFactors = FALSE
  )
}

propensity_doubly_robust_plan <- function(df, covariates = propensity_primary_covariates(),
                                          outcomes = propensity_default_outcome_plan()) {
  outcomes <- outcomes[outcomes$outcome %in% names(df), , drop = FALSE]
  if (nrow(outcomes) == 0L) {
    return(data.frame(
      outcome = character(),
      outcome_family = character(),
      analysis_phase = character(),
      estimand = character(),
      model_formula = character(),
      weight_column = character(),
      covariance = character(),
      status = character(),
      stringsAsFactors = FALSE
    ))
  }
  outcomes$estimand <- "ATE_total_effect_primary"
  outcomes$model_formula <- paste0(outcomes$outcome, " ~ group_dm + ", paste(covariates, collapse = " + "))
  outcomes$weight_column <- "iptw_trimmed"
  outcomes$covariance <- "HC3_if_sandwich_available_else_model_based"
  outcomes$status <- "planned_for_H1_H5_phase_no_inference_reported_here"
  outcomes
}

propensity_model_vcov <- function(fit) {
  if (requireNamespace("sandwich", quietly = TRUE)) {
    return(sandwich::vcovHC(fit, type = "HC3"))
  }
  stats::vcov(fit)
}

fit_propensity_doubly_robust_lm <- function(df, outcome, covariates = propensity_primary_covariates(),
                                            treatment_column = "group_dm",
                                            weight_column = "iptw_trimmed") {
  propensity_require_columns(df, c(outcome, covariates, treatment_column, weight_column), "Doubly robust model")
  model_columns <- c(outcome, covariates, treatment_column, weight_column)
  analysis <- df[stats::complete.cases(df[model_columns]), model_columns, drop = FALSE]
  if (nrow(analysis) == 0L) {
    stop("Doubly robust model has no complete-case rows", call. = FALSE)
  }
  formula <- stats::reformulate(c(treatment_column, covariates), response = outcome)
  fit <- stats::lm(formula, data = analysis, weights = analysis[[weight_column]])
  vcov_matrix <- propensity_model_vcov(fit)
  estimates <- stats::coef(fit)
  std_error <- sqrt(diag(vcov_matrix))
  statistic <- estimates / std_error
  df_residual <- stats::df.residual(fit)
  p_value <- 2 * stats::pt(abs(statistic), df = df_residual, lower.tail = FALSE)
  ci_multiplier <- stats::qt(0.975, df = df_residual)
  data.frame(
    outcome = outcome,
    term = names(estimates),
    estimate = as.numeric(estimates),
    std_error = as.numeric(std_error),
    statistic = as.numeric(statistic),
    df_residual = df_residual,
    p_value = as.numeric(p_value),
    ci_low = as.numeric(estimates - ci_multiplier * std_error),
    ci_high = as.numeric(estimates + ci_multiplier * std_error),
    n = nrow(analysis),
    weight_column = weight_column,
    covariance = if (requireNamespace("sandwich", quietly = TRUE)) "HC3_sandwich" else "model_based",
    formula = deparse(formula, width.cutoff = 500L),
    stringsAsFactors = FALSE
  )
}

propensity_overlap_summary <- function(df) {
  treated <- df$ps_value[df$group_dm == 1L]
  control <- df$ps_value[df$group_dm == 0L]
  data.frame(
    treated_min = min(treated, na.rm = TRUE),
    treated_max = max(treated, na.rm = TRUE),
    control_min = min(control, na.rm = TRUE),
    control_max = max(control, na.rm = TRUE),
    common_support_low = max(min(treated, na.rm = TRUE), min(control, na.rm = TRUE)),
    common_support_high = min(max(treated, na.rm = TRUE), max(control, na.rm = TRUE)),
    outside_common_support_n = sum(
      df$ps_value < max(min(treated, na.rm = TRUE), min(control, na.rm = TRUE)) |
        df$ps_value > min(max(treated, na.rm = TRUE), max(control, na.rm = TRUE)),
      na.rm = TRUE
    ),
    stringsAsFactors = FALSE
  )
}

plot_propensity_overlap <- function(df) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("Required package is not installed: ggplot2", call. = FALSE)
  }
  ggplot2::ggplot(df, ggplot2::aes(x = ps_value, fill = group, color = group)) +
    ggplot2::geom_density(alpha = 0.18, linewidth = 0.7) +
    ggplot2::scale_x_continuous(limits = c(0, 1)) +
    ggplot2::labs(
      title = "Propensity score overlap",
      subtitle = "Primary adjustment: ses_latent + age_gap + cocuk_sayisi",
      x = "Propensity score",
      y = "Density",
      fill = "Group",
      color = "Group"
    ) +
    ggplot2::theme_minimal(base_size = 11) +
    ggplot2::theme(legend.position = "bottom")
}

propensity_max_abs_smd <- function(x) {
  if (all(is.na(x))) {
    return(NA_real_)
  }
  max(x, na.rm = TRUE)
}

summarize_propensity_targets <- function(input_df, ps_fit, balance_table, matching_summary, overlap_summary) {
  data.frame(
    input_rows = nrow(input_df),
    analysis_rows = nrow(ps_fit$data),
    excluded_rows = ps_fit$excluded_rows,
    treatment_level = ps_fit$treatment_level,
    treatment_n = sum(ps_fit$data$group_dm == 1L),
    control_level = ps_fit$control_level,
    control_n = sum(ps_fit$data$group_dm == 0L),
    covariates = paste(ps_fit$covariates, collapse = ";"),
    trim_quantile = ps_fit$trim_quantile,
    trim_cutoff = ps_fit$trim_cutoff,
    trimmed_weight_n = sum(ps_fit$data$iptw_trimmed_flag, na.rm = TRUE),
    max_abs_smd_before = propensity_max_abs_smd(balance_table$abs_smd_before),
    max_abs_smd_iptw = propensity_max_abs_smd(balance_table$abs_smd_iptw),
    max_abs_smd_matched = propensity_max_abs_smd(balance_table$abs_smd_matched),
    matched_pairs = matching_summary$matched_pairs[[1L]],
    common_support_low = overlap_summary$common_support_low[[1L]],
    common_support_high = overlap_summary$common_support_high[[1L]],
    outside_common_support_n = overlap_summary$outside_common_support_n[[1L]],
    stringsAsFactors = FALSE
  )
}

derive_propensity_score_pipeline <- function(df, covariates = propensity_primary_covariates(),
                                             group_column = "group", treatment_level = "DM",
                                             control_level = "Kontrol", trim_quantile = 0.99) {
  stopifnot(!any(propensity_excluded_total_effect_covariates() %in% covariates))
  ps_fit <- estimate_propensity_scores(
    df,
    covariates = covariates,
    group_column = group_column,
    treatment_level = treatment_level,
    control_level = control_level,
    trim_quantile = trim_quantile
  )
  caliper <- 0.2 * stats::sd(ps_fit$data$ps_logit, na.rm = TRUE)
  matching_pairs <- propensity_nearest_neighbor_pairs(ps_fit$data, caliper = caliper)
  matched_df <- propensity_matched_data(ps_fit$data, matching_pairs)
  balance <- propensity_balance_before_after(ps_fit$data, covariates, matched_df)
  matching <- propensity_matching_summary(ps_fit$data, matching_pairs, caliper)
  overlap <- propensity_overlap_summary(ps_fit$data)
  target_summary <- summarize_propensity_targets(df, ps_fit, balance, matching, overlap)

  list(
    data = ps_fit$data,
    model = ps_fit$model,
    model_summary = propensity_model_summary(ps_fit),
    weight_summary = propensity_weight_summary(ps_fit),
    balance = balance,
    matching_pairs = matching_pairs,
    matching_summary = matching,
    overlap_summary = overlap,
    doubly_robust_plan = propensity_doubly_robust_plan(ps_fit$data, covariates),
    target_summary = target_summary
  )
}
