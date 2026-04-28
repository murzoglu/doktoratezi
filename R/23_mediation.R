# KISIM VI — Mediation
# 17. Tek-mediator (Beck → EMBU-P_reddetme → EMBU-C_reddetme)
# 18. Multilevel mediation (level-2 mediator, level-1/2 outcome)
# 19. Conditional process (Hayes Model 14: a-path moderated by group)
# 20. Bayesian mediation preflight + ROPE

mediation_prepare_family <- function(df_family_ses, df_long_scored,
                                     subscale = "reddetme") {
  outcome_p <- sprintf("embu_p_%s_mean", subscale)
  outcome_c <- sprintf("embu_c_%s_mean", subscale)
  if (!outcome_p %in% names(df_family_ses)) stop(sprintf("%s not in family frame", outcome_p))
  if (!outcome_c %in% names(df_long_scored)) stop(sprintf("%s not in long frame", outcome_c))
  long_avg <- aggregate(df_long_scored[[outcome_c]],
                        by = list(aile_no = df_long_scored$aile_no),
                        FUN = mean, na.rm = TRUE)
  names(long_avg)[2] <- "child_outcome"
  family <- df_family_ses[, c("aile_no", "group_f", "anne_yas", "ses_latent",
                               "beck_total", outcome_p)]
  names(family)[names(family) == outcome_p] <- "parent_mediator"
  merged <- merge(family, long_avg, by = "aile_no", all.x = TRUE)
  merged$group_f <- factor(as.character(merged$group_f), levels = c("Kontrol", "DM"))
  merged$group_dm <- as.integer(merged$group_f == "DM")
  merged$anne_yas_z   <- as.numeric(scale(merged$anne_yas))
  merged$ses_latent_z <- as.numeric(scale(merged$ses_latent))
  merged
}

# === 17. Simple mediation =============================================

mediation_simple <- function(df, n_boot = 2000L, seed = 20260428L) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  model <- '
    parent_mediator  ~ a*beck_total + anne_yas_z + ses_latent_z
    child_outcome    ~ b*parent_mediator + cprime*group_dm + ses_latent_z
    indirect := a * b
    direct   := cprime
    total    := indirect + direct
    prop_mediated := indirect / (indirect + cprime)
  '
  fit <- tryCatch(
    suppressWarnings(lavaan::sem(model, data = df, estimator = "ML",
                                  missing = "fiml",
                                  se = "bootstrap", bootstrap = n_boot)),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = paste0("error:", conditionMessage(fit)), fit = NULL))
  }
  pe <- lavaan::parameterEstimates(fit, boot.ci.type = "bca.simple")
  effects <- pe[pe$op == ":=" | pe$label %in% c("a", "b", "cprime"), ]
  fit_meas <- tryCatch(
    lavaan::fitMeasures(fit, c("cfi", "tli", "rmsea", "srmr", "chisq", "df", "pvalue")),
    error = function(e) rep(NA_real_, 7)
  )
  fit_table <- data.frame(
    model = "simple_mediation",
    n     = lavaan::lavInspect(fit, "ntotal"),
    cfi   = unname(fit_meas[1]),
    tli   = unname(fit_meas[2]),
    rmsea = unname(fit_meas[3]),
    srmr  = unname(fit_meas[4]),
    chisq = unname(fit_meas[5]),
    df    = unname(fit_meas[6]),
    pvalue = unname(fit_meas[7]),
    stringsAsFactors = FALSE
  )
  effect_table <- data.frame(
    parameter = effects$label,
    operator  = effects$op,
    estimate  = effects$est,
    se        = effects$se,
    z_value   = effects$z,
    p_value   = effects$pvalue,
    ci_lo     = effects$ci.lower,
    ci_hi     = effects$ci.upper,
    stringsAsFactors = FALSE
  )
  list(status = "ok", fit = fit, effect_table = effect_table, fit_table = fit_table)
}

# === 18. Multilevel mediation (Level-2 mediator with long outcome) =====

mediation_multilevel <- function(df_long_scored, df_family_ses,
                                  subscale = "reddetme", n_boot = 1000L,
                                  seed = 20260428L) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  outcome_p <- sprintf("embu_p_%s_mean", subscale)
  outcome_c <- sprintf("embu_c_%s_mean", subscale)
  family_l2 <- df_family_ses[, c("aile_no", "anne_yas", "ses_latent",
                                  "beck_total", outcome_p)]
  names(family_l2)[names(family_l2) == outcome_p] <- "parent_mediator"
  long_subset <- df_long_scored[, !names(df_long_scored) %in%
                                  c("anne_yas", "ses_latent", "beck_total"), drop = FALSE]
  merged <- merge(long_subset, family_l2, by = "aile_no", all.x = TRUE)
  merged$group_f <- factor(as.character(merged$group_f), levels = c("Kontrol", "DM"))
  merged$group_dm <- as.integer(merged$group_f == "DM")
  merged$anne_yas_z   <- as.numeric(scale(merged$anne_yas))
  merged$ses_latent_z <- as.numeric(scale(merged$ses_latent))
  merged$cocuk_yas_z  <- as.numeric(scale(merged$cocuk_yas))
  merged$child_outcome <- merged[[outcome_c]]
  merged$cinsiyet_dum <- if ("cinsiyet_f" %in% names(merged)) {
    as.integer(as.character(merged$cinsiyet_f) %in% c("Erkek", "erkek", "Male", "M"))
  } else 0L
  model <- '
    level: 1
      child_outcome ~ cocuk_yas_z + cinsiyet_dum
    level: 2
      parent_mediator ~ a*beck_total + ses_latent_z
      child_outcome   ~ b*parent_mediator + cprime*group_dm + ses_latent_z
      indirect := a * b
      direct   := cprime
  '
  fit <- tryCatch(
    suppressWarnings(lavaan::sem(model, data = merged, cluster = "aile_no",
                                  estimator = "ML")),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = paste0("error:", conditionMessage(fit)), fit = NULL))
  }
  pe <- lavaan::parameterEstimates(fit)
  effects <- pe[pe$op == ":=" | pe$label %in% c("a", "b", "cprime"), ]
  effect_table <- data.frame(
    parameter = effects$label,
    operator  = effects$op,
    estimate  = effects$est,
    se        = effects$se,
    z_value   = if ("z" %in% names(effects)) effects$z else NA_real_,
    p_value   = if ("pvalue" %in% names(effects)) effects$pvalue else NA_real_,
    ci_lo     = if ("ci.lower" %in% names(effects)) effects$ci.lower else NA_real_,
    ci_hi     = if ("ci.upper" %in% names(effects)) effects$ci.upper else NA_real_,
    stringsAsFactors = FALSE
  )
  fit_meas <- tryCatch(
    lavaan::fitMeasures(fit, c("cfi", "tli", "rmsea", "srmr", "chisq", "df", "pvalue")),
    error = function(e) rep(NA_real_, 7)
  )
  fit_table <- data.frame(
    model = "multilevel_mediation",
    n_obs = nrow(merged),
    cfi   = unname(fit_meas[1]),
    tli   = unname(fit_meas[2]),
    rmsea = unname(fit_meas[3]),
    srmr  = unname(fit_meas[4]),
    chisq = unname(fit_meas[5]),
    df    = unname(fit_meas[6]),
    pvalue = unname(fit_meas[7]),
    stringsAsFactors = FALSE
  )
  list(status = "ok", fit = fit, effect_table = effect_table, fit_table = fit_table)
}

# === 19. Conditional process (Hayes Model 14: a-path moderated by group)

mediation_conditional_process <- function(df, n_boot = 2000L, seed = 20260428L) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  df$beck_total_z <- as.numeric(scale(df$beck_total))
  df$beck_x_group <- df$beck_total_z * df$group_dm
  model <- '
    parent_mediator ~ a1*beck_total_z + a2*group_dm + a3*beck_x_group +
                       anne_yas_z + ses_latent_z
    child_outcome   ~ b*parent_mediator + cprime*group_dm + ses_latent_z

    cond_indirect_kontrol := a1 * b
    cond_indirect_dm      := (a1 + a3) * b
    index_mod_mediation   := a3 * b
  '
  fit <- tryCatch(
    suppressWarnings(lavaan::sem(model, data = df, estimator = "ML",
                                  missing = "fiml",
                                  se = "bootstrap", bootstrap = n_boot)),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = paste0("error:", conditionMessage(fit)), fit = NULL))
  }
  pe <- lavaan::parameterEstimates(fit, boot.ci.type = "bca.simple")
  effects <- pe[pe$op == ":=" | pe$label %in% c("a1", "a2", "a3", "b", "cprime"), ]
  effect_table <- data.frame(
    parameter = effects$label,
    operator  = effects$op,
    estimate  = effects$est,
    se        = effects$se,
    z_value   = effects$z,
    p_value   = effects$pvalue,
    ci_lo     = effects$ci.lower,
    ci_hi     = effects$ci.upper,
    stringsAsFactors = FALSE
  )
  fit_meas <- tryCatch(
    lavaan::fitMeasures(fit, c("cfi", "tli", "rmsea", "srmr")),
    error = function(e) rep(NA_real_, 4)
  )
  fit_table <- data.frame(
    model = "conditional_process_hayes14",
    cfi = unname(fit_meas[1]),
    tli = unname(fit_meas[2]),
    rmsea = unname(fit_meas[3]),
    srmr = unname(fit_meas[4]),
    stringsAsFactors = FALSE
  )
  list(status = "ok", fit = fit, effect_table = effect_table, fit_table = fit_table)
}

# === 20. Bayesian mediation (preflight) ================================

mediation_bayesian_preflight <- function(df, iter = 1500L, warmup = 750L,
                                          chains = 2L, seed = 20260428L) {
  if (!requireNamespace("brms", quietly = TRUE)) {
    return(list(status = "package_unavailable"))
  }
  fit_a <- tryCatch(
    suppressMessages(suppressWarnings(brms::brm(
      parent_mediator ~ beck_total + anne_yas_z + ses_latent_z,
      data = df,
      prior = c(brms::set_prior("normal(0, 0.5)", class = "b"),
                brms::set_prior("student_t(3, 0, 2.5)", class = "sigma")),
      sample_prior = "yes",
      iter = iter, warmup = warmup, chains = chains, seed = seed,
      cores = chains, backend = "rstan", refresh = 0,
      control = list(adapt_delta = 0.95)
    ))),
    error = function(e) e
  )
  fit_b <- tryCatch(
    suppressMessages(suppressWarnings(brms::brm(
      child_outcome ~ parent_mediator + group_dm + ses_latent_z,
      data = df,
      prior = c(brms::set_prior("normal(0, 0.5)", class = "b"),
                brms::set_prior("student_t(3, 0, 2.5)", class = "sigma")),
      sample_prior = "yes",
      iter = iter, warmup = warmup, chains = chains, seed = seed,
      cores = chains, backend = "rstan", refresh = 0,
      control = list(adapt_delta = 0.95)
    ))),
    error = function(e) e
  )
  if (inherits(fit_a, "error") || inherits(fit_b, "error")) {
    err <- if (inherits(fit_a, "error")) conditionMessage(fit_a) else conditionMessage(fit_b)
    return(list(status = paste0("error:", err)))
  }
  post_a <- as.data.frame(fit_a)$b_beck_total
  post_b <- as.data.frame(fit_b)$b_parent_mediator
  indirect <- post_a * post_b
  direct_post <- as.data.frame(fit_b)$b_group_dm
  indirect_summary <- data.frame(
    parameter   = c("a", "b", "indirect", "direct_cprime"),
    posterior_mean = c(mean(post_a), mean(post_b), mean(indirect), mean(direct_post)),
    sd          = c(stats::sd(post_a), stats::sd(post_b), stats::sd(indirect), stats::sd(direct_post)),
    ci_lo       = c(stats::quantile(post_a, 0.025), stats::quantile(post_b, 0.025),
                     stats::quantile(indirect, 0.025), stats::quantile(direct_post, 0.025)),
    ci_hi       = c(stats::quantile(post_a, 0.975), stats::quantile(post_b, 0.975),
                     stats::quantile(indirect, 0.975), stats::quantile(direct_post, 0.975)),
    pd          = c(max(mean(post_a > 0), mean(post_a < 0)),
                     max(mean(post_b > 0), mean(post_b < 0)),
                     max(mean(indirect > 0), mean(indirect < 0)),
                     max(mean(direct_post > 0), mean(direct_post < 0))),
    rope_pct    = c(mean(abs(post_a) < 0.05), mean(abs(post_b) < 0.05),
                     mean(abs(indirect) < 0.025), mean(abs(direct_post) < 0.10)),
    stringsAsFactors = FALSE
  )
  list(
    status = "ok",
    fit_a  = fit_a,
    fit_b  = fit_b,
    indirect_summary = indirect_summary
  )
}

# === Pipeline orchestrator =============================================

run_mediation_pipeline <- function(df_family_ses, df_long_scored,
                                    subscale = "reddetme",
                                    run_bayes = TRUE, n_boot = 2000L,
                                    iter = 1500L, warmup = 750L, chains = 2L,
                                    seed = 20260428L) {
  prepared <- mediation_prepare_family(df_family_ses, df_long_scored, subscale)
  simple   <- mediation_simple(prepared, n_boot = n_boot, seed = seed)
  conditional <- mediation_conditional_process(prepared, n_boot = n_boot, seed = seed)
  multilevel  <- mediation_multilevel(df_long_scored, df_family_ses,
                                       subscale = subscale, n_boot = n_boot, seed = seed)
  bayes <- if (run_bayes) {
    mediation_bayesian_preflight(prepared, iter = iter, warmup = warmup,
                                 chains = chains, seed = seed)
  } else list(status = "skipped")

  status_table <- data.frame(
    component = c("simple", "multilevel", "conditional_process", "bayesian_preflight"),
    status = c(simple$status, multilevel$status, conditional$status,
               if (is.list(bayes)) bayes$status else "skipped"),
    stringsAsFactors = FALSE
  )

  list(
    status_table              = status_table,
    simple_effect_table       = if (!is.null(simple$effect_table)) simple$effect_table else data.frame(),
    simple_fit_table          = if (!is.null(simple$fit_table)) simple$fit_table else data.frame(),
    multilevel_effect_table   = if (!is.null(multilevel$effect_table)) multilevel$effect_table else data.frame(),
    multilevel_fit_table      = if (!is.null(multilevel$fit_table)) multilevel$fit_table else data.frame(),
    conditional_effect_table  = if (!is.null(conditional$effect_table)) conditional$effect_table else data.frame(),
    conditional_fit_table     = if (!is.null(conditional$fit_table)) conditional$fit_table else data.frame(),
    bayes_indirect_table      = if (!is.null(bayes$indirect_summary)) bayes$indirect_summary else data.frame(),
    target_summary            = data.frame(
      component = c("simple", "multilevel", "conditional", "bayesian"),
      n_rows = c(
        nrow(simple$effect_table %||% data.frame()),
        nrow(multilevel$effect_table %||% data.frame()),
        nrow(conditional$effect_table %||% data.frame()),
        nrow(bayes$indirect_summary %||% data.frame())
      ),
      stringsAsFactors = FALSE
    )
  )
}

`%||%` <- function(x, y) if (is.null(x)) y else x
