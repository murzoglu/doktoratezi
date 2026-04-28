h2_outcome_spec <- function() {
  data.frame(
    outcome = c(
      "srq_ho_warmth_mean",
      "srq_ho_status_mean",
      "srq_ho_conflict_mean",
      "srq_ho_rivalry_mean"
    ),
    domain = c("warmth", "status", "conflict", "rivalry"),
    label = c(
      "SRQ/KIA warmth",
      "SRQ/KIA status",
      "SRQ/KIA conflict",
      "SRQ/KIA rivalry"
    ),
    stringsAsFactors = FALSE
  )
}

h2_family_covariates <- function() {
  c("age_gap", "same_sex", "ses_latent")
}

h2_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

h2_scale_vector <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  center <- mean(x, na.rm = TRUE)
  scale <- stats::sd(x, na.rm = TRUE)
  if (is.na(scale) || scale == 0) {
    stop("Cannot z-scale a constant or fully missing vector", call. = FALSE)
  }
  list(value = (x - center) / scale, center = center, scale = scale)
}

h2_first_existing_col <- function(df, candidates) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0L) {
    return(NA_character_)
  }
  hit[[1L]]
}

h2_prepare_long_frame <- function(df_long_scored, df_family_ses,
                                  outcomes = h2_outcome_spec()$outcome) {
  h2_require_columns(
    df_long_scored,
    c("aile_no", "aile_no_f", "group_f", "family_role_f", outcomes, paste0("srq_", 1:48)),
    "H2 long scored data"
  )
  h2_require_columns(df_family_ses, c("aile_no", "group_f", h2_family_covariates()), "H2 family SES data")

  family_cov <- df_family_ses[, c("aile_no", "group_f", h2_family_covariates()), drop = FALSE]
  family_cov <- family_cov[!duplicated(family_cov$aile_no), , drop = FALSE]
  if (nrow(family_cov) != length(unique(df_family_ses$aile_no))) {
    stop("H2 family SES data must have one row per family", call. = FALSE)
  }

  matched <- match(df_long_scored$aile_no, family_cov$aile_no)
  if (any(is.na(matched))) {
    stop("H2 long data contains family IDs absent from family SES data", call. = FALSE)
  }

  out <- df_long_scored
  for (column in h2_family_covariates()) {
    out[[column]] <- family_cov[[column]][matched]
  }
  out$group_f <- factor(as.character(out$group_f), levels = c("Kontrol", "DM"))
  out$family_role_f <- factor(as.character(out$family_role_f), levels = c("index", "sibling"))
  out$same_sex <- factor(as.character(out$same_sex), levels = c("Farkli", "Ayni"))

  scaling_rows <- lapply(c("age_gap", "ses_latent"), function(column) {
    scaled <- h2_scale_vector(out[[column]])
    out[[paste0(column, "_z")]] <<- scaled$value
    data.frame(
      variable = column,
      center = scaled$center,
      scale = scaled$scale,
      stringsAsFactors = FALSE
    )
  })
  attr(out, "h2_scaling") <- do.call(rbind, scaling_rows)
  out
}

h2_mean_or_na <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  if (all(is.na(x))) {
    return(NA_real_)
  }
  mean(x, na.rm = TRUE)
}

h2_build_family_mean_frame <- function(long_frame, outcomes = h2_outcome_spec()$outcome) {
  h2_require_columns(
    long_frame,
    c("aile_no", "group_f", "age_gap", "same_sex", "ses_latent", "age_gap_z", "ses_latent_z", outcomes),
    "H2 family mean frame"
  )
  families <- sort(unique(long_frame$aile_no))
  rows <- lapply(families, function(family_id) {
    rows <- long_frame[long_frame$aile_no == family_id, , drop = FALSE]
    base <- data.frame(
      aile_no = family_id,
      group_f = factor(as.character(rows$group_f[[1L]]), levels = c("Kontrol", "DM")),
      age_gap = rows$age_gap[[1L]],
      age_gap_z = rows$age_gap_z[[1L]],
      same_sex = factor(as.character(rows$same_sex[[1L]]), levels = c("Farkli", "Ayni")),
      ses_latent = rows$ses_latent[[1L]],
      ses_latent_z = rows$ses_latent_z[[1L]],
      child_rows = nrow(rows),
      stringsAsFactors = FALSE
    )
    for (outcome in outcomes) {
      base[[outcome]] <- h2_mean_or_na(rows[[outcome]])
      base[[paste0(outcome, "_observed_children")]] <- sum(!is.na(rows[[outcome]]))
    }
    base
  })
  out <- do.call(rbind, rows)
  out$group_f <- factor(as.character(out$group_f), levels = c("Kontrol", "DM"))
  out$same_sex <- factor(as.character(out$same_sex), levels = c("Farkli", "Ayni"))
  out
}

h2_numeric_descriptives <- function(x) {
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
    ceiling_pct = if (n > 0L) mean(observed >= 5) * 100 else NA_real_,
    stringsAsFactors = FALSE
  )
}

h2_long_descriptives <- function(long_frame, outcomes = h2_outcome_spec()$outcome) {
  rows <- list()
  index <- 0L
  for (outcome in outcomes) {
    for (group in levels(long_frame$group_f)) {
      for (role in levels(long_frame$family_role_f)) {
        keep <- long_frame$group_f == group & long_frame$family_role_f == role
        stats <- h2_numeric_descriptives(long_frame[[outcome]][keep])
        index <- index + 1L
        rows[[index]] <- data.frame(
          dataset = "long_child",
          outcome = outcome,
          group = group,
          family_role = role,
          stats,
          stringsAsFactors = FALSE
        )
      }
    }
  }
  do.call(rbind, rows)
}

h2_family_mean_descriptives <- function(family_frame, outcomes = h2_outcome_spec()$outcome) {
  rows <- list()
  index <- 0L
  for (outcome in outcomes) {
    for (group in levels(family_frame$group_f)) {
      keep <- family_frame$group_f == group
      stats <- h2_numeric_descriptives(family_frame[[outcome]][keep])
      index <- index + 1L
      rows[[index]] <- data.frame(
        dataset = "family_mean",
        outcome = outcome,
        group = group,
        family_role = "family_mean",
        stats,
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

h2_hedges_g <- function(x_treat, x_control) {
  x_treat <- suppressWarnings(as.numeric(x_treat))
  x_control <- suppressWarnings(as.numeric(x_control))
  x_treat <- x_treat[!is.na(x_treat)]
  x_control <- x_control[!is.na(x_control)]
  n_treat <- length(x_treat)
  n_control <- length(x_control)
  if (n_treat < 2L || n_control < 2L) {
    return(c(g = NA_real_, ci_low = NA_real_, ci_high = NA_real_))
  }
  pooled <- sqrt(((n_treat - 1) * stats::var(x_treat) + (n_control - 1) * stats::var(x_control)) /
    (n_treat + n_control - 2))
  if (is.na(pooled) || pooled == 0) {
    return(c(g = NA_real_, ci_low = NA_real_, ci_high = NA_real_))
  }
  d <- (mean(x_treat) - mean(x_control)) / pooled
  correction <- 1 - 3 / (4 * (n_treat + n_control) - 9)
  g <- d * correction
  se_g <- sqrt((n_treat + n_control) / (n_treat * n_control) + g^2 / (2 * (n_treat + n_control - 2)))
  c(g = g, ci_low = g - stats::qnorm(0.975) * se_g, ci_high = g + stats::qnorm(0.975) * se_g)
}

run_h2_family_mean <- function(family_frame, outcomes = h2_outcome_spec()$outcome) {
  rows <- lapply(outcomes, function(outcome) {
    x_dm <- family_frame[[outcome]][family_frame$group_f == "DM"]
    x_control <- family_frame[[outcome]][family_frame$group_f == "Kontrol"]
    test <- stats::t.test(x_dm, x_control, var.equal = FALSE)
    g <- h2_hedges_g(x_dm, x_control)
    data.frame(
      outcome = outcome,
      n_dm = sum(!is.na(x_dm)),
      n_control = sum(!is.na(x_control)),
      mean_dm = mean(x_dm, na.rm = TRUE),
      mean_control = mean(x_control, na.rm = TRUE),
      mean_difference_dm_minus_control = mean(x_dm, na.rm = TRUE) - mean(x_control, na.rm = TRUE),
      mean_difference_ci_low = test$conf.int[[1L]],
      mean_difference_ci_high = test$conf.int[[2L]],
      t = unname(test$statistic),
      df = unname(test$parameter),
      p_value = test$p.value,
      hedges_g = unname(g[["g"]]),
      hedges_g_ci_low = unname(g[["ci_low"]]),
      hedges_g_ci_high = unname(g[["ci_high"]]),
      effect_size_ci_method = "normal_approximation",
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)
  out$p_fdr_across_h2 <- stats::p.adjust(out$p_value, method = "BH")
  out
}

h2_apim_formula <- function(outcome) {
  stats::as.formula(paste(outcome, "~ group_f * family_role_f + age_gap_z"))
}

h2_lme_frame <- function(df, formula) {
  columns <- unique(c(all.vars(formula), "aile_no_f", "family_role_f"))
  h2_require_columns(df, columns, "H2 APIM frame")
  df[stats::complete.cases(df[columns]), , drop = FALSE]
}

h2_fit_apim <- function(df, formula) {
  if (!requireNamespace("nlme", quietly = TRUE)) {
    stop("Required package is not installed: nlme", call. = FALSE)
  }
  model_df <- h2_lme_frame(df, formula)
  suppressMessages(nlme::lme(
    fixed = formula,
    random = ~ 1 | aile_no_f,
    data = model_df,
    weights = nlme::varIdent(form = ~ 1 | family_role_f),
    correlation = nlme::corCompSymm(form = ~ 1 | aile_no_f),
    method = "REML",
    na.action = stats::na.exclude,
    control = nlme::lmeControl(opt = "optim", maxIter = 100, msMaxIter = 100)
  ))
}

h2_apim_fixed_effects <- function(model, outcome) {
  table <- as.data.frame(summary(model)$tTable)
  table$term <- rownames(table)
  rownames(table) <- NULL
  estimate <- table$Value
  std_error <- table$Std.Error
  df <- table$DF
  multiplier <- stats::qt(0.975, df = df)
  data.frame(
    outcome = outcome,
    term = table$term,
    estimate = estimate,
    std_error = std_error,
    df = df,
    statistic = table$`t-value`,
    p_value = table$`p-value`,
    ci_low = estimate - multiplier * std_error,
    ci_high = estimate + multiplier * std_error,
    stringsAsFactors = FALSE
  )
}

h2_apim_diagnostics <- function(model, outcome) {
  data.frame(
    outcome = outcome,
    n = stats::nobs(model),
    n_families = length(unique(model$data$aile_no_f)),
    sigma = model$sigma,
    logLik = as.numeric(stats::logLik(model)),
    aic = stats::AIC(model),
    bic = stats::BIC(model),
    correlation_structure = "compound_symmetry",
    variance_structure = "role_specific_varIdent",
    stringsAsFactors = FALSE
  )
}

run_h2_apim <- function(long_frame, outcomes = h2_outcome_spec()$outcome) {
  fixed <- list()
  diagnostics <- list()
  for (outcome in outcomes) {
    model <- h2_fit_apim(long_frame, h2_apim_formula(outcome))
    fixed[[outcome]] <- h2_apim_fixed_effects(model, outcome)
    diagnostics[[outcome]] <- h2_apim_diagnostics(model, outcome)
  }
  fixed_table <- do.call(rbind, fixed)
  fixed_table$p_fdr_across_h2 <- stats::p.adjust(fixed_table$p_value, method = "BH")
  list(
    fixed_effects = fixed_table,
    diagnostics = do.call(rbind, diagnostics)
  )
}

h2_moderation_formula <- function(outcome) {
  stats::as.formula(paste(outcome, "~ group_f * age_gap_z * same_sex + ses_latent_z"))
}

h2_fit_moderation <- function(family_frame, formula) {
  columns <- unique(all.vars(formula))
  h2_require_columns(family_frame, columns, "H2 moderation frame")
  model_df <- family_frame[stats::complete.cases(family_frame[columns]), , drop = FALSE]
  old_options <- options(contrasts = c("contr.sum", "contr.poly"))
  on.exit(options(old_options), add = TRUE)
  stats::lm(formula, data = model_df)
}

h2_lm_fixed_effects <- function(model, outcome, model_type) {
  table <- as.data.frame(stats::coef(summary(model)))
  table$term <- rownames(table)
  rownames(table) <- NULL
  estimate <- table$Estimate
  std_error <- table$`Std. Error`
  df <- stats::df.residual(model)
  multiplier <- stats::qt(0.975, df = df)
  data.frame(
    model_type = model_type,
    outcome = outcome,
    term = table$term,
    estimate = estimate,
    std_error = std_error,
    df = df,
    statistic = table$`t value`,
    p_value = table$`Pr(>|t|)`,
    ci_low = estimate - multiplier * std_error,
    ci_high = estimate + multiplier * std_error,
    stringsAsFactors = FALSE
  )
}

h2_moderation_anova <- function(model, outcome) {
  if (!requireNamespace("car", quietly = TRUE)) {
    stop("Required package is not installed: car", call. = FALSE)
  }
  table <- as.data.frame(car::Anova(model, type = 3))
  table$effect <- rownames(table)
  rownames(table) <- NULL
  names(table) <- gsub("Pr\\(>F\\)", "p_value", names(table))
  names(table) <- gsub("F value", "f_value", names(table), fixed = TRUE)
  table$outcome <- outcome
  table[, c("outcome", "effect", setdiff(names(table), c("outcome", "effect"))), drop = FALSE]
}

h2_lm_diagnostics <- function(model, outcome, model_type) {
  summary_model <- summary(model)
  data.frame(
    model_type = model_type,
    outcome = outcome,
    n = stats::nobs(model),
    df_residual = stats::df.residual(model),
    sigma = summary_model$sigma,
    r_squared = summary_model$r.squared,
    adj_r_squared = summary_model$adj.r.squared,
    aic = stats::AIC(model),
    bic = stats::BIC(model),
    stringsAsFactors = FALSE
  )
}

run_h2_age_gap_moderation <- function(family_frame, outcomes = h2_outcome_spec()$outcome) {
  fixed <- list()
  anova <- list()
  diagnostics <- list()
  for (outcome in outcomes) {
    model <- h2_fit_moderation(family_frame, h2_moderation_formula(outcome))
    fixed[[outcome]] <- h2_lm_fixed_effects(model, outcome, "family_mean_age_gap_same_sex_moderation")
    anova[[outcome]] <- h2_moderation_anova(model, outcome)
    diagnostics[[outcome]] <- h2_lm_diagnostics(model, outcome, "family_mean_age_gap_same_sex_moderation")
  }
  anova_table <- do.call(rbind, anova)
  anova_table$p_fdr_across_h2 <- stats::p.adjust(anova_table$p_value, method = "BH")
  fixed_table <- do.call(rbind, fixed)
  fixed_table$p_fdr_across_h2 <- stats::p.adjust(fixed_table$p_value, method = "BH")
  list(
    fixed_effects = fixed_table,
    anova = anova_table,
    diagnostics = do.call(rbind, diagnostics)
  )
}

h2_olsen_kenny_item_set <- function() {
  data.frame(
    item = c(4L, 20L, 36L),
    item_role = "quarreling",
    long_column = paste0("srq_", c(4L, 20L, 36L)),
    stringsAsFactors = FALSE
  )
}

h2_wide_items_by_family <- function(long_frame, item_spec = h2_olsen_kenny_item_set()) {
  h2_require_columns(long_frame, c("aile_no", "family_role_f", item_spec$long_column), "H2 Olsen-Kenny wide data")
  families <- sort(unique(long_frame$aile_no))
  rows <- lapply(families, function(family_id) {
    rows <- long_frame[long_frame$aile_no == family_id, , drop = FALSE]
    index_row <- rows[rows$family_role_f == "index", , drop = FALSE]
    sibling_row <- rows[rows$family_role_f == "sibling", , drop = FALSE]
    if (nrow(index_row) != 1L || nrow(sibling_row) != 1L) {
      stop(sprintf("Family %s must have exactly one index and one sibling row", family_id), call. = FALSE)
    }
    out <- data.frame(aile_no = family_id, stringsAsFactors = FALSE)
    for (column in item_spec$long_column) {
      out[[paste0(column, "_index")]] <- suppressWarnings(as.numeric(index_row[[column]]))
      out[[paste0(column, "_sibling")]] <- suppressWarnings(as.numeric(sibling_row[[column]]))
    }
    out
  })
  do.call(rbind, rows)
}

h2_olsen_kenny_model_syntax <- function(item_spec = h2_olsen_kenny_item_set()) {
  index_terms <- paste0("l", seq_len(nrow(item_spec)), "*", item_spec$long_column, "_index", collapse = " + ")
  sibling_terms <- paste0("l", seq_len(nrow(item_spec)), "*", item_spec$long_column, "_sibling", collapse = " + ")
  residual_cov <- paste0(item_spec$long_column, "_index ~~ ", item_spec$long_column, "_sibling", collapse = "\n")
  paste(
    paste0("quarrel_index =~ ", index_terms),
    paste0("quarrel_sibling =~ ", sibling_terms),
    residual_cov,
    "quarrel_index ~~ quarrel_sibling",
    sep = "\n"
  )
}

h2_lavaan_status <- function(status, message, n_families, n_items) {
  data.frame(
    model = "olsen_kenny_quarreling_cfa",
    status = status,
    message = message,
    n_families = n_families,
    n_items_per_role = n_items,
    stringsAsFactors = FALSE
  )
}

run_h2_olsen_kenny <- function(long_frame) {
  item_spec <- h2_olsen_kenny_item_set()
  wide <- h2_wide_items_by_family(long_frame, item_spec)
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(
      status = h2_lavaan_status("skipped", "lavaan package is not installed", nrow(wide), nrow(item_spec)),
      fit_measures = data.frame(),
      latent_correlations = data.frame(),
      parameter_estimates = data.frame()
    ))
  }

  syntax <- h2_olsen_kenny_model_syntax(item_spec)
  fit <- tryCatch(
    lavaan::cfa(
      syntax,
      data = wide,
      estimator = "MLR",
      missing = "fiml",
      std.lv = TRUE,
      meanstructure = TRUE
    ),
    error = function(error) error
  )
  if (inherits(fit, "error")) {
    return(list(
      status = h2_lavaan_status("failed", conditionMessage(fit), nrow(wide), nrow(item_spec)),
      fit_measures = data.frame(),
      latent_correlations = data.frame(),
      parameter_estimates = data.frame()
    ))
  }

  fit_names <- c("chisq.scaled", "df.scaled", "pvalue.scaled", "cfi.scaled", "tli.scaled", "rmsea.scaled", "srmr", "aic", "bic")
  fit_values <- lavaan::fitMeasures(fit, fit_names)
  fit_measures <- data.frame(
    model = "olsen_kenny_quarreling_cfa",
    measure = names(fit_values),
    value = as.numeric(fit_values),
    stringsAsFactors = FALSE
  )

  cor_lv <- lavaan::lavInspect(fit, "cor.lv")
  latent_correlations <- data.frame(
    model = "olsen_kenny_quarreling_cfa",
    lhs = "quarrel_index",
    rhs = "quarrel_sibling",
    correlation = as.numeric(cor_lv["quarrel_index", "quarrel_sibling"]),
    stringsAsFactors = FALSE
  )

  parameters <- lavaan::parameterEstimates(fit, standardized = TRUE, ci = TRUE)
  parameters$model <- "olsen_kenny_quarreling_cfa"
  parameters <- parameters[, c("model", setdiff(names(parameters), "model")), drop = FALSE]

  list(
    status = h2_lavaan_status("success", "Dyadic CFA fitted", nrow(wide), nrow(item_spec)),
    fit_measures = fit_measures,
    latent_correlations = latent_correlations,
    parameter_estimates = parameters
  )
}

summarize_h2_targets <- function(long_frame, family_frame, family_mean, apim, moderation, olsen_kenny) {
  data.frame(
    long_rows = nrow(long_frame),
    family_rows = nrow(family_frame),
    outcomes = length(h2_outcome_spec()$outcome),
    family_mean_tests = nrow(family_mean),
    family_mean_fdr_lt_05 = sum(family_mean$p_fdr_across_h2 < 0.05, na.rm = TRUE),
    apim_models = length(unique(apim$diagnostics$outcome)),
    apim_fixed_effect_rows = nrow(apim$fixed_effects),
    moderation_models = length(unique(moderation$diagnostics$outcome)),
    moderation_three_way_fdr_lt_05 = sum(
      moderation$anova$effect == "group_f:age_gap_z:same_sex" &
        moderation$anova$p_fdr_across_h2 < 0.05,
      na.rm = TRUE
    ),
    olsen_kenny_status = olsen_kenny$status$status[[1L]],
    olsen_kenny_latent_correlation = if (nrow(olsen_kenny$latent_correlations) > 0L) {
      olsen_kenny$latent_correlations$correlation[[1L]]
    } else {
      NA_real_
    },
    stringsAsFactors = FALSE
  )
}

run_h2_sibling_relationships_pipeline <- function(df_long_scored, df_family_ses, run_cfa = TRUE) {
  long_frame <- h2_prepare_long_frame(df_long_scored, df_family_ses)
  family_frame <- h2_build_family_mean_frame(long_frame)
  family_mean <- run_h2_family_mean(family_frame)
  apim <- run_h2_apim(long_frame)
  moderation <- run_h2_age_gap_moderation(family_frame)
  olsen_kenny <- if (run_cfa) {
    run_h2_olsen_kenny(long_frame)
  } else {
    list(
      status = h2_lavaan_status("skipped", "run_cfa is FALSE", nrow(family_frame), nrow(h2_olsen_kenny_item_set())),
      fit_measures = data.frame(),
      latent_correlations = data.frame(),
      parameter_estimates = data.frame()
    )
  }

  list(
    scaling_summary = attr(long_frame, "h2_scaling"),
    long_descriptives = h2_long_descriptives(long_frame),
    family_mean_descriptives = h2_family_mean_descriptives(family_frame),
    family_mean_tests = family_mean,
    apim_fixed_effects = apim$fixed_effects,
    apim_diagnostics = apim$diagnostics,
    moderation_fixed_effects = moderation$fixed_effects,
    moderation_anova = moderation$anova,
    moderation_diagnostics = moderation$diagnostics,
    olsen_kenny_status = olsen_kenny$status,
    olsen_kenny_fit_measures = olsen_kenny$fit_measures,
    olsen_kenny_latent_correlations = olsen_kenny$latent_correlations,
    olsen_kenny_parameter_estimates = olsen_kenny$parameter_estimates,
    target_summary = summarize_h2_targets(long_frame, family_frame, family_mean, apim, moderation, olsen_kenny)
  )
}
