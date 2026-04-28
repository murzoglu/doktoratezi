h1_outcome_spec <- function() {
  data.frame(
    outcome = c(
      "embu_c_sicaklik_mean",
      "embu_c_asiri_koruma_mean",
      "embu_c_reddetme_mean",
      "embu_c_karsilastirma_mean"
    ),
    subscale = c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma"),
    label = c(
      "EMBU-C emotional warmth",
      "EMBU-C overprotection",
      "EMBU-C rejection",
      "EMBU-C comparison"
    ),
    family = "EMBU-C",
    stringsAsFactors = FALSE
  )
}

h1_primary_covariates <- function() {
  c("cocuk_yas_z", "cinsiyet_f", "ses_latent_z", "age_gap_z", "cocuk_sayisi_z")
}

h1_family_covariates <- function() {
  c("ses_latent", "age_gap", "cocuk_sayisi")
}

h1_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

h1_subscale_items <- function(subscale) {
  item_map <- if (exists("embu_subscale_map", mode = "function")) {
    embu_subscale_map()
  } else {
    list(
      sicaklik = c(1, 3, 6, 7, 13, 17, 20, 24, 26),
      asiri_koruma = c(4, 8, 14, 15, 19, 23, 25),
      reddetme = c(5, 9, 10, 12, 16, 21, 22, 28),
      karsilastirma = c(2, 11, 18, 27, 29)
    )
  }
  if (!subscale %in% names(item_map)) {
    stop(sprintf("Unknown H1 EMBU-C subscale: %s", subscale), call. = FALSE)
  }
  paste0("embu_c_q", sprintf("%02d", item_map[[subscale]]))
}

h1_scale_vector <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  center <- mean(x, na.rm = TRUE)
  scale <- stats::sd(x, na.rm = TRUE)
  if (is.na(scale) || scale == 0) {
    stop("Cannot z-scale a constant or fully missing vector", call. = FALSE)
  }
  list(value = (x - center) / scale, center = center, scale = scale)
}

h1_prepare_analysis_frame <- function(df_long_scored, df_family_ses,
                                      outcomes = h1_outcome_spec()$outcome) {
  h1_require_columns(
    df_long_scored,
    c(
      "aile_no", "role_f", "group_f", "family_role_f", "cinsiyet_f",
      "cocuk_yas", outcomes, paste0("embu_c_q", sprintf("%02d", 1:29))
    ),
    "H1 long scored data"
  )
  h1_require_columns(df_family_ses, c("aile_no", h1_family_covariates()), "H1 family SES data")

  family_cov <- df_family_ses[, c("aile_no", h1_family_covariates()), drop = FALSE]
  family_cov <- family_cov[!duplicated(family_cov$aile_no), , drop = FALSE]
  if (nrow(family_cov) != length(unique(df_family_ses$aile_no))) {
    stop("H1 family SES data must have one row per family", call. = FALSE)
  }

  matched <- match(df_long_scored$aile_no, family_cov$aile_no)
  if (any(is.na(matched))) {
    stop("H1 long data contains family IDs absent from family SES data", call. = FALSE)
  }

  out <- df_long_scored
  for (column in h1_family_covariates()) {
    out[[column]] <- family_cov[[column]][matched]
  }

  z_specs <- c("cocuk_yas", h1_family_covariates())
  scaling_rows <- lapply(z_specs, function(column) {
    scaled <- h1_scale_vector(out[[column]])
    out[[paste0(column, "_z")]] <<- scaled$value
    data.frame(
      variable = column,
      center = scaled$center,
      scale = scaled$scale,
      stringsAsFactors = FALSE
    )
  })
  scaling <- do.call(rbind, scaling_rows)
  attr(out, "h1_scaling") <- scaling
  out
}

h1_primary_formula <- function(outcome) {
  stats::as.formula(paste(
    outcome,
    "~ role_f + cocuk_yas_z + cinsiyet_f + ses_latent_z + age_gap_z + cocuk_sayisi_z + (1 | aile_no_f)"
  ))
}

h1_three_way_formula <- function(outcome) {
  stats::as.formula(paste(
    outcome,
    "~ role_f * cocuk_yas_z * cinsiyet_f + ses_latent_z + age_gap_z + cocuk_sayisi_z + (1 | aile_no_f)"
  ))
}

h1_model_columns <- function(formula) {
  unique(all.vars(formula))
}

h1_model_frame <- function(df, formula) {
  columns <- h1_model_columns(formula)
  h1_require_columns(df, columns, "H1 model frame")
  df[stats::complete.cases(df[columns]), , drop = FALSE]
}

h1_fit_lmer <- function(df, formula) {
  if (!requireNamespace("lmerTest", quietly = TRUE)) {
    stop("Required package is not installed: lmerTest", call. = FALSE)
  }
  if (!requireNamespace("lme4", quietly = TRUE)) {
    stop("Required package is not installed: lme4", call. = FALSE)
  }
  model_df <- h1_model_frame(df, formula)
  suppressMessages(lmerTest::lmer(
    formula,
    data = model_df,
    REML = TRUE,
    control = lme4::lmerControl(optimizer = "bobyqa"),
    na.action = stats::na.exclude
  ))
}

h1_first_existing_col <- function(df, candidates) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0L) {
    return(NA_character_)
  }
  hit[[1L]]
}

h1_fixed_effects_table <- function(model, outcome, model_type) {
  coef_table <- as.data.frame(stats::coef(summary(model)))
  coef_table$term <- rownames(coef_table)
  rownames(coef_table) <- NULL

  estimate_col <- h1_first_existing_col(coef_table, c("Estimate"))
  se_col <- h1_first_existing_col(coef_table, c("Std. Error"))
  df_col <- h1_first_existing_col(coef_table, c("df"))
  statistic_col <- h1_first_existing_col(coef_table, c("t value", "z value"))
  p_col <- h1_first_existing_col(coef_table, c("Pr(>|t|)", "Pr(>|z|)"))

  estimate <- coef_table[[estimate_col]]
  std_error <- coef_table[[se_col]]
  df_value <- if (!is.na(df_col)) coef_table[[df_col]] else stats::df.residual(model)
  ci_multiplier <- stats::qt(0.975, df = df_value)

  data.frame(
    model_type = model_type,
    outcome = outcome,
    term = coef_table$term,
    estimate = estimate,
    std_error = std_error,
    df = df_value,
    statistic = coef_table[[statistic_col]],
    p_value = if (!is.na(p_col)) coef_table[[p_col]] else NA_real_,
    ci_low = estimate - ci_multiplier * std_error,
    ci_high = estimate + ci_multiplier * std_error,
    stringsAsFactors = FALSE
  )
}

h1_anova_table <- function(model, outcome, model_type) {
  anova_table <- as.data.frame(stats::anova(model, type = 3, ddf = "Satterthwaite"))
  anova_table$effect = rownames(anova_table)
  rownames(anova_table) <- NULL
  names(anova_table) <- gsub(" ", "_", names(anova_table), fixed = TRUE)
  names(anova_table) <- gsub("Pr\\(>F\\)", "p_value", names(anova_table))
  names(anova_table) <- gsub("F_value", "f_value", names(anova_table), fixed = TRUE)
  anova_table$model_type <- model_type
  anova_table$outcome <- outcome
  anova_table[, c("model_type", "outcome", setdiff(names(anova_table), c("model_type", "outcome"))), drop = FALSE]
}

h1_role_pairwise_table <- function(model, outcome) {
  if (!requireNamespace("emmeans", quietly = TRUE)) {
    stop("Required package is not installed: emmeans", call. = FALSE)
  }
  emm <- emmeans::emmeans(model, specs = stats::as.formula("~ role_f"))
  pairs <- as.data.frame(emmeans::contrast(emm, method = "pairwise", adjust = "holm"))
  p_col <- h1_first_existing_col(pairs, c("p.value", "p_value"))
  data.frame(
    outcome = outcome,
    contrast = pairs$contrast,
    estimate = pairs$estimate,
    std_error = pairs$SE,
    df = pairs$df,
    statistic = pairs$t.ratio,
    p_value = pairs[[p_col]],
    adjust = "holm_within_outcome",
    stringsAsFactors = FALSE
  )
}

h1_extract_r2 <- function(model) {
  if (!requireNamespace("performance", quietly = TRUE)) {
    return(c(r2_marginal = NA_real_, r2_conditional = NA_real_))
  }
  r2 <- tryCatch(
    suppressMessages(suppressWarnings(as.data.frame(performance::r2_nakagawa(model)))),
    error = function(error) NULL
  )
  if (is.null(r2)) {
    return(c(r2_marginal = NA_real_, r2_conditional = NA_real_))
  }
  c(
    r2_marginal = if ("R2_marginal" %in% names(r2)) r2$R2_marginal[[1L]] else NA_real_,
    r2_conditional = if ("R2_conditional" %in% names(r2)) r2$R2_conditional[[1L]] else NA_real_
  )
}

h1_extract_icc <- function(model) {
  if (!requireNamespace("performance", quietly = TRUE)) {
    return(NA_real_)
  }
  icc <- tryCatch(
    suppressMessages(suppressWarnings(as.data.frame(performance::icc(model)))),
    error = function(error) NULL
  )
  if (is.null(icc)) {
    return(NA_real_)
  }
  if ("ICC_adjusted" %in% names(icc)) {
    return(icc$ICC_adjusted[[1L]])
  }
  if ("ICC" %in% names(icc)) {
    return(icc$ICC[[1L]])
  }
  NA_real_
}

h1_model_diagnostics <- function(model, outcome, model_type) {
  singular <- lme4::isSingular(model, tol = 1e-4)
  r2 <- if (singular) c(r2_marginal = NA_real_, r2_conditional = NA_real_) else h1_extract_r2(model)
  icc <- if (singular) NA_real_ else h1_extract_icc(model)
  data.frame(
    model_type = model_type,
    outcome = outcome,
    n = stats::nobs(model),
    n_families = length(unique(stats::model.frame(model)$aile_no_f)),
    sigma = stats::sigma(model),
    icc = icc,
    r2_marginal = unname(r2[["r2_marginal"]]),
    r2_conditional = unname(r2[["r2_conditional"]]),
    singular = singular,
    aic = stats::AIC(model),
    bic = stats::BIC(model),
    stringsAsFactors = FALSE
  )
}

h1_outcome_descriptives <- function(df, outcomes = h1_outcome_spec()$outcome) {
  rows <- list()
  index <- 0L
  for (outcome in outcomes) {
    for (role in levels(df$role_f)) {
      x <- suppressWarnings(as.numeric(df[[outcome]][df$role_f == role]))
      observed <- x[!is.na(x)]
      index <- index + 1L
      rows[[index]] <- data.frame(
        outcome = outcome,
        role = role,
        n = length(observed),
        missing_n = sum(is.na(x)),
        mean = if (length(observed) > 0L) mean(observed) else NA_real_,
        sd = if (length(observed) > 1L) stats::sd(observed) else NA_real_,
        median = if (length(observed) > 0L) stats::median(observed) else NA_real_,
        q1 = if (length(observed) > 0L) as.numeric(stats::quantile(observed, 0.25, names = FALSE)) else NA_real_,
        q3 = if (length(observed) > 0L) as.numeric(stats::quantile(observed, 0.75, names = FALSE)) else NA_real_,
        min = if (length(observed) > 0L) min(observed) else NA_real_,
        max = if (length(observed) > 0L) max(observed) else NA_real_,
        floor_pct = if (length(observed) > 0L) mean(observed <= 1) * 100 else NA_real_,
        ceiling_pct = if (length(observed) > 0L) mean(observed >= 4) * 100 else NA_real_,
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

h1_sample_summary <- function(df, outcomes = h1_outcome_spec()$outcome) {
  role_counts <- as.data.frame(table(role = df$role_f, group = df$group_f), stringsAsFactors = FALSE)
  role_counts$role <- as.character(role_counts$role)
  role_counts$group <- as.character(role_counts$group)
  names(role_counts)[names(role_counts) == "Freq"] <- "n"
  outcome_rows <- lapply(outcomes, function(outcome) {
    data.frame(
      role = "ALL",
      group = "ALL",
      n = sum(!is.na(df[[outcome]])),
      outcome = outcome,
      complete_families = length(unique(df$aile_no[!is.na(df[[outcome]])])),
      stringsAsFactors = FALSE
    )
  })
  role_counts$outcome <- "role_count"
  role_counts$complete_families <- NA_integer_
  rbind(role_counts, do.call(rbind, outcome_rows))
}

run_h1_frequentist <- function(df, outcomes = h1_outcome_spec()$outcome) {
  models <- list()
  fixed <- list()
  anova <- list()
  pairs <- list()
  diagnostics <- list()

  for (outcome in outcomes) {
    model <- h1_fit_lmer(df, h1_primary_formula(outcome))
    models[[outcome]] <- model
    fixed[[outcome]] <- h1_fixed_effects_table(model, outcome, "primary_multilevel_ancova")
    anova[[outcome]] <- h1_anova_table(model, outcome, "primary_multilevel_ancova")
    pairs[[outcome]] <- h1_role_pairwise_table(model, outcome)
    diagnostics[[outcome]] <- h1_model_diagnostics(model, outcome, "primary_multilevel_ancova")
  }

  pairwise <- do.call(rbind, pairs)
  pairwise$p_fdr_across_h1 <- stats::p.adjust(pairwise$p_value, method = "BH")

  list(
    models = models,
    fixed_effects = do.call(rbind, fixed),
    anova = do.call(rbind, anova),
    role_pairwise = pairwise,
    diagnostics = do.call(rbind, diagnostics)
  )
}

h1_three_way_test_row <- function(anova_table) {
  effect <- "role_f:cocuk_yas_z:cinsiyet_f"
  row <- anova_table[anova_table$effect == effect, , drop = FALSE]
  if (nrow(row) == 0L) {
    row <- anova_table[grepl("role_f.*cocuk_yas_z.*cinsiyet_f", anova_table$effect), , drop = FALSE]
  }
  row
}

h1_age_z_values <- function(df, ages = c(8, 12, 16)) {
  scaling <- attr(df, "h1_scaling")
  center <- scaling$center[scaling$variable == "cocuk_yas"][[1L]]
  scale <- scaling$scale[scaling$variable == "cocuk_yas"][[1L]]
  (ages - center) / scale
}

h1_three_way_grid <- function(model, outcome, df, ages = c(8, 12, 16)) {
  if (!requireNamespace("emmeans", quietly = TRUE)) {
    return(data.frame())
  }
  age_z <- h1_age_z_values(df, ages)
  emm <- emmeans::emmeans(
    model,
    specs = stats::as.formula("~ role_f | cinsiyet_f * cocuk_yas_z"),
    at = list(cocuk_yas_z = age_z)
  )
  out <- as.data.frame(emm)
  age_lookup <- data.frame(cocuk_yas_z = age_z, age_year = ages)
  out <- merge(out, age_lookup, by = "cocuk_yas_z", all.x = TRUE, sort = FALSE)
  out$outcome <- outcome
  out[, c("outcome", "age_year", "cocuk_yas_z", setdiff(names(out), c("outcome", "age_year", "cocuk_yas_z"))), drop = FALSE]
}

run_h1_three_way <- function(df, outcomes = h1_outcome_spec()$outcome) {
  models <- list()
  tests <- list()
  grids <- list()
  diagnostics <- list()

  for (outcome in outcomes) {
    model <- h1_fit_lmer(df, h1_three_way_formula(outcome))
    models[[outcome]] <- model
    anova <- h1_anova_table(model, outcome, "three_way_role_age_sex")
    tests[[outcome]] <- h1_three_way_test_row(anova)
    grids[[outcome]] <- h1_three_way_grid(model, outcome, df)
    diagnostics[[outcome]] <- h1_model_diagnostics(model, outcome, "three_way_role_age_sex")
  }

  test_table <- do.call(rbind, tests)
  if (nrow(test_table) > 0L && "p_value" %in% names(test_table)) {
    test_table$p_fdr_across_h1 <- stats::p.adjust(test_table$p_value, method = "BH")
  }

  list(
    models = models,
    tests = test_table,
    emmeans_grid = do.call(rbind, grids),
    diagnostics = do.call(rbind, diagnostics)
  )
}

h1_irt_status_row <- function(subscale, status, message, n_rows = NA_integer_, n_items = NA_integer_) {
  data.frame(
    subscale = subscale,
    status = status,
    message = message,
    n_rows = n_rows,
    n_items = n_items,
    stringsAsFactors = FALSE
  )
}

h1_irt_item_data <- function(df, subscale) {
  columns <- h1_subscale_items(subscale)
  h1_require_columns(df, columns, sprintf("H1 IRT %s", subscale))
  item_data <- df[, columns, drop = FALSE]
  for (column in columns) {
    item_data[[column]] <- suppressWarnings(as.integer(item_data[[column]]))
  }
  complete <- stats::complete.cases(item_data)
  list(data = item_data[complete, , drop = FALSE], complete = complete, columns = columns)
}

h1_irt_grm_for_subscale <- function(df, subscale) {
  if (!requireNamespace("mirt", quietly = TRUE)) {
    return(list(
      status = h1_irt_status_row(subscale, "skipped", "mirt package is not installed"),
      item_parameters = data.frame(),
      theta_fixed_effects = data.frame(),
      theta_anova = data.frame(),
      theta_diagnostics = data.frame()
    ))
  }

  items <- h1_irt_item_data(df, subscale)
  if (nrow(items$data) < 50L) {
    return(list(
      status = h1_irt_status_row(subscale, "skipped", "fewer than 50 complete item rows", nrow(items$data), ncol(items$data)),
      item_parameters = data.frame(),
      theta_fixed_effects = data.frame(),
      theta_anova = data.frame(),
      theta_diagnostics = data.frame()
    ))
  }

  fit <- tryCatch(
    mirt::mirt(items$data, model = 1, itemtype = "graded", method = "EM", verbose = FALSE),
    error = function(error) error
  )
  if (inherits(fit, "error")) {
    return(list(
      status = h1_irt_status_row(subscale, "failed", conditionMessage(fit), nrow(items$data), ncol(items$data)),
      item_parameters = data.frame(),
      theta_fixed_effects = data.frame(),
      theta_anova = data.frame(),
      theta_diagnostics = data.frame()
    ))
  }

  coefs <- as.data.frame(mirt::coef(fit, IRTpars = TRUE, simplify = TRUE)$items)
  coefs$item <- rownames(coefs)
  rownames(coefs) <- NULL
  coefs$subscale <- subscale
  coefs <- coefs[, c("subscale", "item", setdiff(names(coefs), c("subscale", "item"))), drop = FALSE]

  theta <- as.numeric(mirt::fscores(fit, method = "EAP"))
  theta_df <- df[items$complete, , drop = FALSE]
  theta_outcome <- paste0("h1_irt_theta_", subscale)
  theta_df[[theta_outcome]] <- theta
  theta_model <- h1_fit_lmer(theta_df, h1_primary_formula(theta_outcome))

  list(
    status = h1_irt_status_row(subscale, "success", "GRM fitted and theta model estimated", nrow(items$data), ncol(items$data)),
    item_parameters = coefs,
    theta_fixed_effects = h1_fixed_effects_table(theta_model, theta_outcome, "irt_theta_multilevel_ancova"),
    theta_anova = h1_anova_table(theta_model, theta_outcome, "irt_theta_multilevel_ancova"),
    theta_diagnostics = h1_model_diagnostics(theta_model, theta_outcome, "irt_theta_multilevel_ancova")
  )
}

run_h1_irt_grm <- function(df, subscales = h1_outcome_spec()$subscale) {
  results <- lapply(subscales, function(subscale) h1_irt_grm_for_subscale(df, subscale))
  list(
    status = do.call(rbind, lapply(results, `[[`, "status")),
    item_parameters = do.call(rbind, lapply(results, `[[`, "item_parameters")),
    theta_fixed_effects = do.call(rbind, lapply(results, `[[`, "theta_fixed_effects")),
    theta_anova = do.call(rbind, lapply(results, `[[`, "theta_anova")),
    theta_diagnostics = do.call(rbind, lapply(results, `[[`, "theta_diagnostics"))
  )
}

h1_bayesian_plan <- function(outcomes = h1_outcome_spec()$outcome, seed = 20260427L) {
  data.frame(
    outcome = outcomes,
    formula = vapply(outcomes, function(outcome) deparse(h1_primary_formula(outcome), width.cutoff = 500L), character(1L)),
    family = "gaussian",
    priors = "b~normal(0,1);sd~student_t(3,0,2.5);sigma~student_t(3,0,2.5)",
    chains = 4L,
    iter = 4000L,
    warmup = 1500L,
    seed = seed,
    adapt_delta = 0.95,
    max_treedepth = 12L,
    package_available = requireNamespace("brms", quietly = TRUE) && requireNamespace("bayestestR", quietly = TRUE),
    default_execution = "manual_not_in_targets_or_audit",
    status = "planned_preflight_only",
    stringsAsFactors = FALSE
  )
}

fit_h1_bayesian_model <- function(df, outcome, seed = 20260427L, chains = 4L,
                                  iter = 4000L, warmup = 1500L, cores = 4L) {
  if (!requireNamespace("brms", quietly = TRUE)) {
    stop("Required package is not installed: brms", call. = FALSE)
  }
  priors <- c(
    brms::prior(normal(0, 1), class = b),
    brms::prior(student_t(3, 0, 2.5), class = sd),
    brms::prior(student_t(3, 0, 2.5), class = sigma)
  )
  brms::brm(
    h1_primary_formula(outcome),
    data = h1_model_frame(df, h1_primary_formula(outcome)),
    family = brms::gaussian(),
    prior = priors,
    chains = chains,
    iter = iter,
    warmup = warmup,
    seed = seed,
    cores = cores,
    control = list(adapt_delta = 0.95, max_treedepth = 12)
  )
}

summarize_h1_targets <- function(input_long, analysis_frame, frequentist, three_way, irt, bayesian_plan) {
  data.frame(
    input_rows = nrow(input_long),
    analysis_rows = nrow(analysis_frame),
    families = length(unique(analysis_frame$aile_no)),
    outcomes = length(h1_outcome_spec()$outcome),
    primary_models = length(frequentist$models),
    three_way_models = length(three_way$models),
    irt_subscales = nrow(irt$status),
    irt_success_n = sum(irt$status$status == "success"),
    bayesian_plan_rows = nrow(bayesian_plan),
    bayesian_sampling_in_default_pipeline = FALSE,
    min_primary_model_n = min(frequentist$diagnostics$n, na.rm = TRUE),
    max_primary_icc = max(frequentist$diagnostics$icc, na.rm = TRUE),
    role_pairwise_tests = nrow(frequentist$role_pairwise),
    role_pairwise_fdr_lt_05 = sum(frequentist$role_pairwise$p_fdr_across_h1 < 0.05, na.rm = TRUE),
    stringsAsFactors = FALSE
  )
}

run_h1_child_perception_pipeline <- function(df_long_scored, df_family_ses, run_irt = TRUE) {
  analysis_frame <- h1_prepare_analysis_frame(df_long_scored, df_family_ses)
  frequentist <- run_h1_frequentist(analysis_frame)
  three_way <- run_h1_three_way(analysis_frame)
  irt <- if (run_irt) {
    run_h1_irt_grm(analysis_frame)
  } else {
    list(
      status = data.frame(subscale = h1_outcome_spec()$subscale, status = "skipped", message = "run_irt is FALSE", n_rows = NA_integer_, n_items = NA_integer_),
      item_parameters = data.frame(),
      theta_fixed_effects = data.frame(),
      theta_anova = data.frame(),
      theta_diagnostics = data.frame()
    )
  }
  bayes <- h1_bayesian_plan()

  list(
    analysis_frame_summary = h1_sample_summary(analysis_frame),
    scaling_summary = attr(analysis_frame, "h1_scaling"),
    outcome_descriptives = h1_outcome_descriptives(analysis_frame),
    primary_fixed_effects = frequentist$fixed_effects,
    primary_anova = frequentist$anova,
    primary_role_pairwise = frequentist$role_pairwise,
    primary_diagnostics = frequentist$diagnostics,
    three_way_tests = three_way$tests,
    three_way_emmeans_grid = three_way$emmeans_grid,
    three_way_diagnostics = three_way$diagnostics,
    irt_status = irt$status,
    irt_item_parameters = irt$item_parameters,
    irt_theta_fixed_effects = irt$theta_fixed_effects,
    irt_theta_anova = irt$theta_anova,
    irt_theta_diagnostics = irt$theta_diagnostics,
    bayesian_plan = bayes,
    target_summary = summarize_h1_targets(df_long_scored, analysis_frame, frequentist, three_way, irt, bayes)
  )
}
