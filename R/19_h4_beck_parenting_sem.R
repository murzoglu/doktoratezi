h4_embu_subscale_map <- function() {
  if (exists("embu_subscale_map", mode = "function")) {
    return(embu_subscale_map())
  }
  list(
    sicaklik = c(1, 3, 6, 7, 13, 17, 20, 24, 26),
    asiri_koruma = c(4, 8, 14, 15, 19, 23, 25),
    reddetme = c(5, 9, 10, 12, 16, 21, 22, 28),
    karsilastirma = c(2, 11, 18, 27, 29)
  )
}

h4_embu_item_columns <- function(items = 1:29) {
  paste0("embu_p_q", sprintf("%02d", items))
}

h4_beck_item_columns <- function(items = 1:21) {
  paste0("beck_", items)
}

h4_ordered_items <- function() {
  c(h4_embu_item_columns(), h4_beck_item_columns())
}

h4_ordered_items_from_map <- function(item_map, beck_items = 1:21) {
  c(
    unlist(lapply(item_map, h4_embu_item_columns), use.names = FALSE),
    h4_beck_item_columns(beck_items)
  )
}

h4_multigroup_embu_subscale_map <- function() {
  list(
    sicaklik = c(1, 3, 24),
    asiri_koruma = c(4, 8, 14),
    reddetme = c(5, 9, 10, 28),
    karsilastirma = c(2, 18, 27)
  )
}

h4_multigroup_ordered_items <- function() {
  h4_ordered_items_from_map(h4_multigroup_embu_subscale_map(), beck_items = 1:6)
}

h4_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

h4_scale_vector <- function(x) {
  x <- suppressWarnings(as.numeric(x))
  center <- mean(x, na.rm = TRUE)
  scale <- stats::sd(x, na.rm = TRUE)
  if (is.na(scale) || scale == 0) {
    stop("Cannot z-scale a constant or fully missing vector", call. = FALSE)
  }
  list(value = (x - center) / scale, center = center, scale = scale)
}

h4_prepare_analysis_frame <- function(df_family_ses) {
  h4_require_columns(
    df_family_ses,
    c("aile_no", "group_f", "anne_yas", "ses_latent", h4_ordered_items()),
    "H4 family SES data"
  )
  if (anyDuplicated(df_family_ses$aile_no) > 0L) {
    stop("H4 family SES data must have one row per family", call. = FALSE)
  }

  out <- df_family_ses
  out$group_f <- factor(as.character(out$group_f), levels = c("Kontrol", "DM"))
  for (column in h4_ordered_items()) {
    out[[column]] <- suppressWarnings(as.integer(as.character(out[[column]])))
  }

  scaling_rows <- lapply(c("anne_yas", "ses_latent"), function(column) {
    scaled <- h4_scale_vector(out[[column]])
    out[[paste0(column, "_z")]] <<- scaled$value
    data.frame(
      variable = column,
      center = scaled$center,
      scale = scaled$scale,
      stringsAsFactors = FALSE
    )
  })
  attr(out, "h4_scaling") <- do.call(rbind, scaling_rows)
  out
}

h4_item_diagnostics <- function(df, ordered_items = h4_ordered_items(), sparse_threshold = 2L) {
  rows <- lapply(ordered_items, function(column) {
    x <- df[[column]]
    observed <- x[!is.na(x)]
    tab <- table(observed, useNA = "no")
    data.frame(
      item = column,
      n = length(observed),
      missing_n = sum(is.na(x)),
      n_categories = length(tab),
      min_observed = if (length(observed) > 0L) min(observed) else NA_integer_,
      max_observed = if (length(observed) > 0L) max(observed) else NA_integer_,
      min_category_n = if (length(tab) > 0L) min(as.integer(tab)) else NA_integer_,
      sparse_category_n = sum(as.integer(tab) <= sparse_threshold),
      sparse_categories = if (length(tab) > 0L && any(as.integer(tab) <= sparse_threshold)) {
        paste(names(tab)[as.integer(tab) <= sparse_threshold], as.integer(tab)[as.integer(tab) <= sparse_threshold], sep = ":", collapse = ";")
      } else {
        NA_character_
      },
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

h4_collapse_one_item_for_groups <- function(x, group) {
  original <- suppressWarnings(as.integer(as.character(x)))
  collapsed <- original

  repeat {
    levels_now <- sort(unique(collapsed[!is.na(collapsed)]))
    if (length(levels_now) < 2L) {
      break
    }
    tab <- table(group, factor(collapsed, levels = levels_now), useNA = "no")
    zero_cells <- which(tab == 0L, arr.ind = TRUE)
    if (nrow(zero_cells) == 0L) {
      break
    }
    zero_columns <- unique(zero_cells[, 2L])
    totals <- colSums(tab)
    collapse_pos <- zero_columns[which.min(totals[zero_columns])]
    if (collapse_pos <= 1L) {
      target_level <- levels_now[[2L]]
    } else if (collapse_pos >= length(levels_now)) {
      target_level <- levels_now[[length(levels_now) - 1L]]
    } else {
      left_total <- totals[[collapse_pos - 1L]]
      right_total <- totals[[collapse_pos + 1L]]
      target_level <- if (left_total >= right_total) levels_now[[collapse_pos - 1L]] else levels_now[[collapse_pos + 1L]]
    }
    collapsed[collapsed == levels_now[[collapse_pos]]] <- target_level
  }

  data.frame(
    original_value = sort(unique(original[!is.na(original)])),
    stringsAsFactors = FALSE
  ) |>
    within({
      collapsed_value <- vapply(original_value, function(value) {
        final <- unique(collapsed[original == value & !is.na(original)])
        if (length(final) == 0L) {
          NA_integer_
        } else {
          final[[1L]]
        }
      }, integer(1))
      changed <- original_value != collapsed_value
      original_n <- vapply(original_value, function(value) sum(original == value, na.rm = TRUE), integer(1))
    })
}

h4_sparse_group_collapse_plan <- function(df, ordered_items = h4_ordered_items(), group_column = "group_f") {
  h4_require_columns(df, c(group_column, ordered_items), "H4 multigroup sparse-category plan")
  rows <- list()
  index <- 0L
  for (item in ordered_items) {
    mapping <- h4_collapse_one_item_for_groups(df[[item]], df[[group_column]])
    mapping <- mapping[mapping$changed, , drop = FALSE]
    if (nrow(mapping) == 0L) {
      next
    }
    mapping$item <- item
    mapping$reason <- "group_specific_empty_ordered_category"
    index <- index + 1L
    rows[[index]] <- mapping[, c("item", "original_value", "collapsed_value", "original_n", "reason"), drop = FALSE]
  }
  if (length(rows) == 0L) {
    return(data.frame(
      item = character(),
      original_value = integer(),
      collapsed_value = integer(),
      original_n = integer(),
      reason = character(),
      stringsAsFactors = FALSE
    ))
  }
  out <- do.call(rbind, rows)
  rownames(out) <- NULL
  out
}

h4_apply_sparse_collapse_plan <- function(df, collapse_plan) {
  if (nrow(collapse_plan) == 0L) {
    return(df)
  }
  out <- df
  for (item in unique(collapse_plan$item)) {
    item_plan <- collapse_plan[collapse_plan$item == item, , drop = FALSE]
    values <- suppressWarnings(as.integer(as.character(out[[item]])))
    for (i in seq_len(nrow(item_plan))) {
      values[values == item_plan$original_value[[i]]] <- item_plan$collapsed_value[[i]]
    }
    out[[item]] <- values
  }
  out
}

h4_latent_factor_terms <- function(prefix, items) {
  paste0(prefix, "_q", sprintf("%02d", items), collapse = " + ")
}

h4_measurement_model_syntax <- function(beck_items = 1:21, item_map = h4_embu_subscale_map()) {
  paste(
    paste0("sicaklik =~ ", h4_latent_factor_terms("embu_p", item_map$sicaklik)),
    paste0("asiri_koruma =~ ", h4_latent_factor_terms("embu_p", item_map$asiri_koruma)),
    paste0("reddetme =~ ", h4_latent_factor_terms("embu_p", item_map$reddetme)),
    paste0("karsilastirma =~ ", h4_latent_factor_terms("embu_p", item_map$karsilastirma)),
    paste0("beck_dep =~ ", paste(h4_beck_item_columns(beck_items), collapse = " + ")),
    sep = "\n"
  )
}

h4_structural_model_syntax <- function(label_paths = TRUE) {
  labels <- if (label_paths) {
    c("b_sicaklik*", "b_asiri_koruma*", "b_reddetme*", "b_karsilastirma*")
  } else {
    rep("", 4L)
  }
  paste(
    paste0("sicaklik ~ ", labels[[1L]], "beck_dep + anne_yas_z + ses_latent_z"),
    paste0("asiri_koruma ~ ", labels[[2L]], "beck_dep + anne_yas_z + ses_latent_z"),
    paste0("reddetme ~ ", labels[[3L]], "beck_dep + anne_yas_z + ses_latent_z"),
    paste0("karsilastirma ~ ", labels[[4L]], "beck_dep + anne_yas_z + ses_latent_z"),
    sep = "\n"
  )
}

h4_latent_sem_model_syntax <- function(label_paths = TRUE, beck_items = 1:21,
                                       item_map = h4_embu_subscale_map()) {
  paste(
    h4_measurement_model_syntax(beck_items, item_map = item_map),
    h4_structural_model_syntax(label_paths),
    sep = "\n\n"
  )
}

h4_bayesian_sem_model_syntax <- function() {
  paste(
    h4_measurement_model_syntax(beck_items = 1:6, item_map = h4_multigroup_embu_subscale_map()),
    "sicaklik ~ b_warm*beck_dep",
    "reddetme ~ b_rej*beck_dep",
    sep = "\n"
  )
}

h4_capture <- function(expr) {
  warnings <- character()
  result <- tryCatch(
    withCallingHandlers(
      expr,
      warning = function(warning) {
        warnings <<- c(warnings, conditionMessage(warning))
        invokeRestart("muffleWarning")
      }
    ),
    error = function(error) error
  )
  list(result = result, warnings = unique(warnings))
}

h4_bind_rows_fill <- function(rows) {
  rows <- rows[!vapply(rows, is.null, logical(1))]
  if (length(rows) == 0L) {
    return(data.frame())
  }
  all_names <- unique(unlist(lapply(rows, names), use.names = FALSE))
  if (length(all_names) == 0L) {
    return(data.frame())
  }
  filled <- lapply(rows, function(row) {
    missing_names <- setdiff(all_names, names(row))
    for (name in missing_names) {
      row[[name]] <- NA
    }
    row[, all_names, drop = FALSE]
  })
  out <- do.call(rbind, filled)
  rownames(out) <- NULL
  out
}

h4_empty_status <- function(model_type, status, message, n_rows, n_ordered_items,
                            group_equal = NA_character_, warnings = character()) {
  data.frame(
    model_type = model_type,
    status = status,
    message = message,
    n_rows = n_rows,
    n_ordered_items = n_ordered_items,
    group_equal = group_equal,
    warning_n = length(warnings),
    warnings = if (length(warnings) > 0L) paste(warnings, collapse = " | ") else NA_character_,
    stringsAsFactors = FALSE
  )
}

h4_lavaan_status <- function(fit, model_type, n_rows, n_ordered_items,
                             group_equal = NA_character_, warnings = character()) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(h4_empty_status(model_type, "skipped", "lavaan package is not installed", n_rows, n_ordered_items, group_equal, warnings))
  }
  if (inherits(fit, "error")) {
    return(h4_empty_status(model_type, "failed", conditionMessage(fit), n_rows, n_ordered_items, group_equal, warnings))
  }
  converged <- isTRUE(lavaan::lavInspect(fit, "converged"))
  h4_empty_status(
    model_type,
    if (converged) "success" else "not_converged",
    if (converged) "lavaan model fitted" else "lavaan model did not converge",
    n_rows,
    n_ordered_items,
    group_equal,
    warnings
  )
}

h4_fit_measure_names <- function() {
  c(
    "chisq.scaled",
    "df.scaled",
    "pvalue.scaled",
    "cfi.scaled",
    "tli.scaled",
    "rmsea.scaled",
    "srmr",
    "aic",
    "bic"
  )
}

h4_fit_measures_table <- function(fit, model_type) {
  if (inherits(fit, "error")) {
    return(data.frame())
  }
  values <- tryCatch(
    lavaan::fitMeasures(fit, h4_fit_measure_names()),
    error = function(error) numeric()
  )
  if (length(values) == 0L) {
    return(data.frame())
  }
  data.frame(
    model_type = model_type,
    measure = names(values),
    value = as.numeric(values),
    stringsAsFactors = FALSE
  )
}

h4_structural_paths_table <- function(fit, model_type) {
  if (inherits(fit, "error")) {
    return(data.frame())
  }
  parameters <- tryCatch(
    lavaan::parameterEstimates(fit, standardized = TRUE, ci = TRUE),
    error = function(error) data.frame()
  )
  if (nrow(parameters) == 0L) {
    return(data.frame())
  }
  rows <- parameters[parameters$op == "~" & parameters$rhs == "beck_dep", , drop = FALSE]
  if (nrow(rows) == 0L) {
    return(data.frame())
  }
  rows$model_type <- model_type
  if (!"group" %in% names(rows)) {
    rows$group <- NA_integer_
  }
  keep <- intersect(
    c("model_type", "lhs", "op", "rhs", "label", "group", "est", "se", "z", "pvalue", "ci.lower", "ci.upper", "std.all"),
    names(rows)
  )
  out <- rows[, keep, drop = FALSE]
  out$p_fdr_across_h4 <- stats::p.adjust(out$pvalue, method = "BH")
  rownames(out) <- NULL
  out
}

h4_lavaan_group_labels <- function(fit) {
  labels <- tryCatch(lavaan::lavInspect(fit, "group.label"), error = function(error) NULL)
  if (is.null(labels)) {
    return(NULL)
  }
  labels
}

h4_add_group_label <- function(table, fit) {
  if (nrow(table) == 0L || !"group" %in% names(table)) {
    return(table)
  }
  labels <- h4_lavaan_group_labels(fit)
  if (is.null(labels)) {
    table$group_label <- NA_character_
    return(table)
  }
  group_index <- suppressWarnings(as.integer(table$group))
  table$group_label <- ifelse(!is.na(group_index) & group_index >= 1L & group_index <= length(labels), labels[group_index], NA_character_)
  table[, c("model_type", "group_label", setdiff(names(table), c("model_type", "group_label"))), drop = FALSE]
}

run_h4_latent_sem <- function(df) {
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(
      status = h4_empty_status("latent_sem_wlsmv", "skipped", "lavaan package is not installed", nrow(df), length(h4_ordered_items())),
      fit_measures = data.frame(),
      structural_paths = data.frame()
    ))
  }

  ordered <- h4_ordered_items()
  model <- h4_latent_sem_model_syntax(label_paths = TRUE)
  captured <- h4_capture(lavaan::sem(
    model,
    data = df,
    estimator = "WLSMV",
    ordered = ordered,
    missing = "pairwise",
    std.lv = TRUE,
    parameterization = "theta"
  ))
  status <- h4_lavaan_status(captured$result, "latent_sem_wlsmv", nrow(df), length(ordered), warnings = captured$warnings)
  list(
    status = status,
    fit_measures = h4_fit_measures_table(captured$result, "latent_sem_wlsmv"),
    structural_paths = h4_structural_paths_table(captured$result, "latent_sem_wlsmv")
  )
}

h4_invariance_steps <- function(max_step = "structural_regressions") {
  steps <- list(
    configural = character(),
    metric_loadings = "loadings",
    scalar_thresholds = c("loadings", "thresholds"),
    structural_regressions = c("loadings", "thresholds", "regressions")
  )
  if (!max_step %in% names(steps)) {
    stop(sprintf("Unknown H4 invariance max_step: %s", max_step), call. = FALSE)
  }
  steps[seq_len(match(max_step, names(steps)))]
}

h4_group_equal_label <- function(group_equal) {
  if (length(group_equal) == 0L) {
    return("none")
  }
  paste(group_equal, collapse = "+")
}

run_h4_multigroup_invariance_core <- function(df, model_prefix = "multigroup",
                                              max_step = "metric_loadings",
                                              item_map = h4_multigroup_embu_subscale_map(),
                                              beck_items = 1:6) {
  ordered <- h4_ordered_items_from_map(item_map, beck_items = beck_items)
  if (!requireNamespace("lavaan", quietly = TRUE)) {
    return(list(
      status = h4_empty_status(paste0(model_prefix, "_configural"), "skipped", "lavaan package is not installed", nrow(df), length(ordered)),
      fit_measures = data.frame(),
      comparison = data.frame(),
      structural_paths = data.frame()
    ))
  }

  model <- h4_latent_sem_model_syntax(label_paths = FALSE, beck_items = beck_items, item_map = item_map)
  steps <- h4_invariance_steps(max_step = max_step)
  fits <- list()
  status <- list()
  measures <- list()
  paths <- list()

  for (step_name in names(steps)) {
    group_equal <- steps[[step_name]]
    model_type <- paste0(model_prefix, "_", step_name)
    captured <- h4_capture(lavaan::sem(
      model,
      data = df,
      group = "group_f",
      estimator = "WLSMV",
      ordered = ordered,
      missing = "pairwise",
      std.lv = TRUE,
      parameterization = "theta",
      group.equal = group_equal
    ))
    fits[[step_name]] <- captured$result
    status[[step_name]] <- h4_lavaan_status(
      captured$result,
      model_type,
      nrow(df),
      length(ordered),
      group_equal = h4_group_equal_label(group_equal),
      warnings = captured$warnings
    )
    measures[[step_name]] <- h4_fit_measures_table(captured$result, model_type)
    paths[[step_name]] <- h4_add_group_label(h4_structural_paths_table(captured$result, model_type), captured$result)
  }

  fit_measures <- h4_bind_rows_fill(measures)
  comparison <- h4_invariance_comparison(fit_measures, model_prefix = model_prefix, max_step = max_step)
  list(
    status = h4_bind_rows_fill(status),
    fit_measures = fit_measures,
    comparison = comparison,
    structural_paths = h4_bind_rows_fill(paths)
  )
}

run_h4_multigroup_invariance <- function(df, max_step = "metric_loadings",
                                         item_map = h4_multigroup_embu_subscale_map(),
                                         beck_items = 1:6) {
  ordered <- h4_ordered_items_from_map(item_map, beck_items = beck_items)
  collapse_plan <- h4_sparse_group_collapse_plan(df, ordered_items = ordered)
  analysis_df <- if (nrow(collapse_plan) > 0L) {
    h4_apply_sparse_collapse_plan(df, collapse_plan)
  } else {
    df
  }
  results <- run_h4_multigroup_invariance_core(
    analysis_df,
    model_prefix = "multigroup",
    max_step = max_step,
    item_map = item_map,
    beck_items = beck_items
  )
  if (nrow(collapse_plan) > 0L && nrow(results$status) > 0L) {
    results$status$message <- paste(results$status$message, "Sparse ordered categories were collapsed for multigroup invariance sensitivity.")
  }
  results$collapse_plan <- collapse_plan
  results$ordered_items <- ordered
  results
}

h4_measure_value <- function(table, model_type, measure) {
  row <- table[table$model_type == model_type & table$measure == measure, , drop = FALSE]
  if (nrow(row) == 0L) {
    return(NA_real_)
  }
  row$value[[1L]]
}

h4_invariance_comparison <- function(fit_measures, model_prefix = "multigroup",
                                      max_step = "structural_regressions") {
  if (nrow(fit_measures) == 0L) {
    return(data.frame())
  }
  step_order <- paste0(model_prefix, "_", names(h4_invariance_steps(max_step = max_step)))
  step_order <- step_order[step_order %in% unique(fit_measures$model_type)]
  if (length(step_order) == 0L) {
    return(data.frame())
  }
  rows <- list()
  previous <- NA_character_
  for (model_type in step_order) {
    cfi <- h4_measure_value(fit_measures, model_type, "cfi.scaled")
    rmsea <- h4_measure_value(fit_measures, model_type, "rmsea.scaled")
    srmr <- h4_measure_value(fit_measures, model_type, "srmr")
    prev_cfi <- if (is.na(previous)) NA_real_ else h4_measure_value(fit_measures, previous, "cfi.scaled")
    prev_rmsea <- if (is.na(previous)) NA_real_ else h4_measure_value(fit_measures, previous, "rmsea.scaled")
    rows[[model_type]] <- data.frame(
      model_type = model_type,
      previous_model = previous,
      cfi_scaled = cfi,
      rmsea_scaled = rmsea,
      srmr = srmr,
      delta_cfi_scaled = if (is.na(prev_cfi) || is.na(cfi)) NA_real_ else cfi - prev_cfi,
      delta_rmsea_scaled = if (is.na(prev_rmsea) || is.na(rmsea)) NA_real_ else rmsea - prev_rmsea,
      invariance_rule = "flag_if_delta_cfi_le_-0.010_or_delta_rmsea_ge_0.015",
      sparse_category_handling = if (model_prefix == "multigroup") "group_empty_categories_collapsed_if_needed" else "none",
      invariance_flag = if (is.na(prev_cfi) || is.na(cfi) || is.na(prev_rmsea) || is.na(rmsea)) {
        NA_character_
      } else if ((cfi - prev_cfi) <= -0.010 || (rmsea - prev_rmsea) >= 0.015) {
        "possible_noninvariance"
      } else {
        "acceptable_change"
      },
      stringsAsFactors = FALSE
    )
    previous <- model_type
  }
  do.call(rbind, rows)
}

h4_bayesian_sem_plan <- function(seed = 20260428L) {
  data.frame(
    model = "bayesian_sem_blavaan_preflight",
    syntax = h4_bayesian_sem_model_syntax(),
    ordered_items = paste(h4_multigroup_ordered_items(), collapse = ";"),
    priors = "lambda~normal(0.5,0.5); beta~normal(0,1)",
    target = "stan",
    chains = 4L,
    burnin = 2000L,
    sample = 5000L,
    seed = seed,
    blavaan_available = requireNamespace("blavaan", quietly = TRUE),
    posterior_available = requireNamespace("posterior", quietly = TRUE),
    default_execution = "manual_not_in_targets_or_audit",
    status = "planned_preflight_only",
    stringsAsFactors = FALSE
  )
}

fit_h4_bayesian_sem <- function(df, seed = 20260428L, n.chains = 4L, burnin = 2000L, sample = 5000L) {
  if (!requireNamespace("blavaan", quietly = TRUE)) {
    stop("Required package is not installed: blavaan", call. = FALSE)
  }
  blavaan::bsem(
    h4_bayesian_sem_model_syntax(),
    data = df,
    ordered = h4_multigroup_ordered_items(),
    n.chains = n.chains,
    burnin = burnin,
    sample = sample,
    target = "stan",
    seed = seed,
    dp = blavaan::dpriors(
      lambda = "normal(0.5, 0.5)",
      beta = "normal(0, 1)"
    )
  )
}

summarize_h4_targets <- function(analysis_frame, item_diagnostics, latent_sem, multigroup, bayesian_plan) {
  data.frame(
    family_rows = nrow(analysis_frame),
    complete_item_rows = sum(stats::complete.cases(analysis_frame[h4_ordered_items()])),
    groups = paste(levels(analysis_frame$group_f), collapse = ";"),
    ordered_items = length(h4_ordered_items()),
    sparse_item_n = sum(item_diagnostics$sparse_category_n > 0L, na.rm = TRUE),
    max_sparse_category_n = max(item_diagnostics$sparse_category_n, na.rm = TRUE),
    latent_sem_status = latent_sem$status$status[[1L]],
    latent_sem_structural_paths = nrow(latent_sem$structural_paths),
    latent_sem_paths_fdr_lt_05 = if (nrow(latent_sem$structural_paths) > 0L) {
      sum(latent_sem$structural_paths$p_fdr_across_h4 < 0.05, na.rm = TRUE)
    } else {
      0L
    },
    multigroup_sparse_collapse_rows = if (!is.null(multigroup$collapse_plan)) nrow(multigroup$collapse_plan) else 0L,
    multigroup_ordered_items = if (!is.null(multigroup$ordered_items)) length(multigroup$ordered_items) else NA_integer_,
    multigroup_steps = nrow(multigroup$status),
    multigroup_success_n = sum(multigroup$status$status == "success", na.rm = TRUE),
    bayesian_plan_rows = nrow(bayesian_plan),
    bayesian_sampling_in_default_pipeline = FALSE,
    stringsAsFactors = FALSE
  )
}

run_h4_beck_parenting_sem_pipeline <- function(df_family_ses, run_sem = TRUE,
                                               run_multigroup = TRUE,
                                               multigroup_max_step = "metric_loadings") {
  analysis_frame <- h4_prepare_analysis_frame(df_family_ses)
  item_diagnostics <- h4_item_diagnostics(analysis_frame)
  latent_sem <- if (run_sem) {
    run_h4_latent_sem(analysis_frame)
  } else {
    list(
      status = h4_empty_status("latent_sem_wlsmv", "skipped", "run_sem is FALSE", nrow(analysis_frame), length(h4_ordered_items())),
      fit_measures = data.frame(),
      structural_paths = data.frame()
    )
  }
  multigroup <- if (run_multigroup) {
    run_h4_multigroup_invariance(analysis_frame, max_step = multigroup_max_step)
  } else {
    list(
      status = h4_empty_status("multigroup_configural", "skipped", "run_multigroup is FALSE", nrow(analysis_frame), length(h4_ordered_items())),
      fit_measures = data.frame(),
      comparison = data.frame(),
      structural_paths = data.frame(),
      collapse_plan = data.frame(),
      ordered_items = character()
    )
  }
  bayes <- h4_bayesian_sem_plan()

  list(
    scaling_summary = attr(analysis_frame, "h4_scaling"),
    ordered_item_diagnostics = item_diagnostics,
    latent_sem_status = latent_sem$status,
    latent_sem_fit_measures = latent_sem$fit_measures,
    latent_sem_structural_paths = latent_sem$structural_paths,
    multigroup_status = multigroup$status,
    multigroup_fit_measures = multigroup$fit_measures,
    multigroup_comparison = multigroup$comparison,
    multigroup_structural_paths = multigroup$structural_paths,
    multigroup_sparse_collapse_map = multigroup$collapse_plan,
    bayesian_sem_plan = bayes,
    target_summary = summarize_h4_targets(analysis_frame, item_diagnostics, latent_sem, multigroup, bayes)
  )
}
