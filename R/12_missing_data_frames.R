missing_default_seed <- function() {
  20260427L
}

missing_required_columns <- function() {
  c("aile_no", "group")
}

missing_dm_only_columns <- function() {
  c("hba1c", "dm_yili", "dm_tani_tarihi")
}

missing_primary_core_columns <- function() {
  c(
    "aile_no",
    "group",
    "cocuk_yas",
    "kardes_yas",
    "katilimci_cocuk_cinsiyet",
    "kardes_cinsiyet",
    "anne_yas",
    "anne_antidepresan",
    "cocuk_sayisi",
    "egitim_durumu",
    "es_egitim_durumu",
    "aile_isei08",
    "material_index",
    "ses_composite_eq",
    "ses_latent"
  )
}

missing_score_columns <- function(df) {
  patterns <- c(
    "^embu_p_.*_mean$",
    "^embu_c_idx_.*_mean$",
    "^embu_c_sib_.*_mean$",
    "^srq_ho_.*_mean$",
    "^srq_sib_ho_.*_mean$",
    "^beck_total$"
  )
  grep(paste(patterns, collapse = "|"), names(df), value = TRUE)
}

missing_clinical_sensitivity_columns <- function(df) {
  intersect(c("hba1c", "dm_yili"), names(df))
}

missing_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

missing_is_dm_group <- function(group) {
  tolower(as.character(group)) %in% c("dm", "diyabet", "diabetes", "t1dm")
}

missing_structural_mask <- function(df, variable) {
  if (!variable %in% names(df)) {
    stop(sprintf("Missing variable is not present: %s", variable), call. = FALSE)
  }
  mask <- rep(FALSE, nrow(df))
  if (variable %in% missing_dm_only_columns() && "group" %in% names(df)) {
    mask <- !missing_is_dm_group(df$group)
  }
  mask
}

missing_structural_matrix <- function(df, columns = names(df)) {
  columns <- intersect(columns, names(df))
  matrix_values <- lapply(columns, function(column) missing_structural_mask(df, column))
  out <- do.call(cbind, matrix_values)
  colnames(out) <- columns
  out
}

missing_variable_block <- function(variable) {
  if (variable %in% c("aile_no", "cocuk_no")) {
    return("identifier")
  }
  if (variable %in% c("group", "group_dm", "role", "family_role", "is_index")) {
    return("design")
  }
  if (variable %in% c(
    "cocuk_yas", "kardes_yas", "katilimci_cocuk_cinsiyet", "kardes_cinsiyet",
    "anne_yas", "anne_antidepresan", "cocuk_sayisi", "egitim_durumu", "es_egitim_durumu"
  )) {
    return("demographic")
  }
  if (variable %in% missing_dm_only_columns()) {
    return("clinical_dm_only")
  }
  if (grepl("^(aile_isei08|material_|ses_|mean_aile_egitim|max_aile_egitim|egitim_fark|cift_kazanc|kalabalik_indeksi)", variable)) {
    return("ses")
  }
  if (grepl("^embu_p_", variable)) {
    return("embu_parent")
  }
  if (grepl("^embu_c_", variable)) {
    return("embu_child")
  }
  if (grepl("^srq", variable)) {
    return("srq")
  }
  if (grepl("^beck", variable)) {
    return("beck")
  }
  "other"
}

missing_analysis_columns <- function(df) {
  unique(intersect(
    c(
      missing_primary_core_columns(),
      missing_score_columns(df),
      missing_clinical_sensitivity_columns(df)
    ),
    names(df)
  ))
}

missing_primary_columns <- function(df) {
  setdiff(missing_analysis_columns(df), missing_clinical_sensitivity_columns(df))
}

missing_clinical_columns <- function(df) {
  unique(c(missing_primary_columns(df), missing_clinical_sensitivity_columns(df)))
}

missing_strategy_label <- function(variable, structural_missing_n, analytic_missing_pct,
                                   high_missing_threshold = 0.60) {
  if (missing_variable_block(variable) == "identifier") {
    return("identifier_no_imputation")
  }
  if (variable == "group") {
    return("design_predictor_no_imputation")
  }
  if (structural_missing_n > 0L) {
    if (is.na(analytic_missing_pct) || analytic_missing_pct <= high_missing_threshold * 100) {
      return("dm_only_sensitivity_where_matrix")
    }
    return("dm_only_high_missing_sensitivity")
  }
  if (is.na(analytic_missing_pct) || analytic_missing_pct == 0) {
    return("observed_predictor_or_outcome")
  }
  if (analytic_missing_pct <= high_missing_threshold * 100) {
    return("primary_mi_or_fiml")
  }
  "high_missing_sensitivity_only"
}

missing_variable_summary <- function(df, columns = missing_analysis_columns(df),
                                     high_missing_threshold = 0.60) {
  missing_require_columns(df, missing_required_columns(), "missing variable summary")
  columns <- intersect(columns, names(df))
  rows <- lapply(columns, function(column) {
    values <- df[[column]]
    structural <- missing_structural_mask(df, column)
    missing_values <- is.na(values)
    analytic_denominator <- sum(!structural)
    analytic_missing_n <- sum(missing_values & !structural)
    structural_missing_n <- sum(missing_values & structural)
    analytic_missing_pct <- if (analytic_denominator > 0L) {
      analytic_missing_n / analytic_denominator * 100
    } else {
      NA_real_
    }

    data.frame(
      variable = column,
      block = missing_variable_block(column),
      class = paste(class(values), collapse = ";"),
      n = length(values),
      missing_n = sum(missing_values),
      missing_pct = mean(missing_values) * 100,
      structural_missing_n = structural_missing_n,
      analytic_denominator = analytic_denominator,
      analytic_missing_n = analytic_missing_n,
      analytic_missing_pct = analytic_missing_pct,
      strategy = missing_strategy_label(
        column,
        structural_missing_n,
        analytic_missing_pct,
        high_missing_threshold
      ),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

missing_block_summary <- function(variable_summary) {
  blocks <- split(variable_summary, variable_summary$block)
  rows <- lapply(names(blocks), function(block) {
    values <- blocks[[block]]
    analytic_denominator <- sum(values$analytic_denominator)
    analytic_missing_n <- sum(values$analytic_missing_n)
    data.frame(
      block = block,
      n_variables = nrow(values),
      n_cells = sum(values$n),
      missing_cells = sum(values$missing_n),
      missing_pct = sum(values$missing_n) / sum(values$n) * 100,
      structural_missing_cells = sum(values$structural_missing_n),
      analytic_denominator = analytic_denominator,
      analytic_missing_cells = analytic_missing_n,
      analytic_missing_pct = if (analytic_denominator > 0L) analytic_missing_n / analytic_denominator * 100 else NA_real_,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

missing_group_summary <- function(df, columns = missing_analysis_columns(df), group_column = "group") {
  missing_require_columns(df, c(group_column), "missing group summary")
  columns <- intersect(columns, names(df))
  groups <- unique(as.character(df[[group_column]]))
  rows <- list()
  k <- 1L
  for (column in columns) {
    structural <- missing_structural_mask(df, column)
    missing_values <- is.na(df[[column]])
    for (group_value in groups) {
      in_group <- as.character(df[[group_column]]) == group_value
      analytic_denominator <- sum(in_group & !structural)
      analytic_missing_n <- sum(in_group & missing_values & !structural)
      rows[[k]] <- data.frame(
        variable = column,
        block = missing_variable_block(column),
        group = group_value,
        n = sum(in_group),
        missing_n = sum(in_group & missing_values),
        missing_pct = if (sum(in_group) > 0L) sum(in_group & missing_values) / sum(in_group) * 100 else NA_real_,
        structural_missing_n = sum(in_group & missing_values & structural),
        analytic_denominator = analytic_denominator,
        analytic_missing_n = analytic_missing_n,
        analytic_missing_pct = if (analytic_denominator > 0L) analytic_missing_n / analytic_denominator * 100 else NA_real_,
        stringsAsFactors = FALSE
      )
      k <- k + 1L
    }
  }
  do.call(rbind, rows)
}

missing_pattern_summary <- function(df, columns = missing_primary_columns(df), max_patterns = 20L) {
  columns <- setdiff(intersect(columns, names(df)), "aile_no")
  if (length(columns) == 0L) {
    return(data.frame(
      pattern = character(),
      n = integer(),
      pct = numeric(),
      n_missing_variables = integer(),
      missing_variables = character(),
      stringsAsFactors = FALSE
    ))
  }

  analytic_missing <- do.call(cbind, lapply(columns, function(column) {
    is.na(df[[column]]) & !missing_structural_mask(df, column)
  }))
  colnames(analytic_missing) <- columns
  pattern <- apply(analytic_missing, 1L, function(row) paste(ifelse(row, "1", "0"), collapse = ""))
  indices <- split(seq_len(nrow(analytic_missing)), pattern)
  rows <- lapply(names(indices), function(pattern_id) {
    idx <- indices[[pattern_id]]
    first <- idx[[1L]]
    missing_variables <- columns[analytic_missing[first, ]]
    data.frame(
      pattern = pattern_id,
      n = length(idx),
      pct = length(idx) / nrow(df) * 100,
      n_missing_variables = length(missing_variables),
      missing_variables = paste(missing_variables, collapse = ";"),
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)
  out <- out[order(-out$n, out$n_missing_variables, out$pattern), , drop = FALSE]
  utils::head(out, max_patterns)
}

missing_prepare_analysis_frame <- function(df, columns) {
  columns <- intersect(columns, names(df))
  out <- df[columns]
  for (column in names(out)) {
    if (is.character(out[[column]])) {
      out[[column]] <- factor(out[[column]])
    }
  }
  if ("group" %in% names(out) && !"group_dm" %in% names(out)) {
    out$group_dm <- as.integer(missing_is_dm_group(out$group))
  }
  out
}

missing_complete_case_frame <- function(frame, id_columns = "aile_no") {
  analysis_columns <- setdiff(names(frame), id_columns)
  if (length(analysis_columns) == 0L) {
    return(frame)
  }
  frame[stats::complete.cases(frame[analysis_columns]), , drop = FALSE]
}

missing_method_for_column <- function(values, should_impute) {
  if (!should_impute) {
    return("")
  }
  if (is.factor(values)) {
    n_levels <- length(levels(values))
    if (is.ordered(values)) {
      return("polr")
    }
    if (n_levels <= 2L) {
      return("logreg")
    }
    return("polyreg")
  }
  if (is.numeric(values) || is.integer(values)) {
    return("pmm")
  }
  ""
}

missing_predictor_candidates <- function(target) {
  candidates <- c(
    "cocuk_yas",
    "kardes_yas",
    "katilimci_cocuk_cinsiyet",
    "kardes_cinsiyet",
    "anne_yas",
    "anne_antidepresan",
    "cocuk_sayisi",
    "egitim_durumu",
    "es_egitim_durumu",
    "aile_isei08",
    "material_index",
    "ses_latent",
    "beck_total",
    "embu_p_sicaklik_mean",
    "embu_p_reddetme_mean",
    "embu_c_idx_sicaklik_mean",
    "embu_c_sib_sicaklik_mean",
    "srq_ho_warmth_mean",
    "srq_sib_ho_warmth_mean",
    "dm_yili"
  )
  candidates
}

missing_build_mice_spec <- function(frame, id_columns = "aile_no") {
  if (!requireNamespace("mice", quietly = TRUE)) {
    stop("Required package is not installed: mice", call. = FALSE)
  }

  method <- mice::make.method(frame)
  where <- is.na(frame)
  structural <- missing_structural_matrix(frame, names(frame))
  where[structural] <- FALSE

  for (column in names(frame)) {
    method[[column]] <- missing_method_for_column(frame[[column]], any(where[, column]))
  }
  method[intersect(id_columns, names(method))] <- ""

  predictor_matrix <- mice::make.predictorMatrix(frame)
  predictor_matrix[,] <- 0
  for (column in names(method)[method != ""]) {
    predictors <- intersect(missing_predictor_candidates(column), names(frame))
    predictors <- setdiff(predictors, c(column, id_columns))
    predictor_matrix[column, predictors] <- 1
  }
  id_present <- intersect(id_columns, colnames(predictor_matrix))
  if (length(id_present) > 0L) {
    predictor_matrix[, id_present] <- 0
    predictor_matrix[id_present, ] <- 0
  }
  predictor_matrix[method == "", ] <- 0

  list(
    method = method,
    predictor_matrix = predictor_matrix,
    where = where,
    structural = structural
  )
}

missing_mice_method_plan <- function(spec, frame_name) {
  data.frame(
    frame = frame_name,
    variable = names(spec$method),
    method = unname(spec$method),
    imputed_n = as.integer(colSums(spec$where)),
    structural_n = as.integer(colSums(spec$structural)),
    used_predictor_n = as.integer(colSums(spec$predictor_matrix != 0)),
    stringsAsFactors = FALSE
  )
}

run_missing_mice <- function(frame, spec, m = 50L, maxit = 30L,
                             seed = missing_default_seed(), print_flag = FALSE) {
  if (!requireNamespace("mice", quietly = TRUE)) {
    stop("Required package is not installed: mice", call. = FALSE)
  }
  mice::mice(
    frame,
    m = m,
    maxit = maxit,
    method = spec$method,
    predictorMatrix = spec$predictor_matrix,
    where = spec$where,
    seed = seed,
    printFlag = print_flag
  )
}

run_missing_imputation_set <- function(missing_results, m = 50L, maxit = 30L,
                                       seed = missing_default_seed(), print_flag = FALSE) {
  list(
    primary = run_missing_mice(
      missing_results$frames$mi_primary,
      missing_results$mice_specs$primary,
      m = m,
      maxit = maxit,
      seed = seed,
      print_flag = print_flag
    ),
    clinical_sensitivity = run_missing_mice(
      missing_results$frames$mi_clinical_sensitivity,
      missing_results$mice_specs$clinical_sensitivity,
      m = m,
      maxit = maxit,
      seed = seed + 1L,
      print_flag = print_flag
    )
  )
}

summarize_missing_mice <- function(imputations) {
  if (inherits(imputations, "mids")) {
    imputations <- list(primary = imputations)
  }
  rows <- lapply(names(imputations), function(frame_name) {
    imp <- imputations[[frame_name]]
    logged_events_n <- if (!is.null(imp$loggedEvents)) nrow(imp$loggedEvents) else 0L
    data.frame(
      frame = frame_name,
      variable = names(imp$method),
      method = unname(imp$method),
      imputed_n = as.integer(colSums(imp$where)),
      m = imp$m,
      maxit = imp$iteration,
      logged_events_n = logged_events_n,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

missing_mcar_numeric_frame <- function(frame) {
  out <- data.frame(row.names = seq_len(nrow(frame)))
  for (column in names(frame)) {
    values <- frame[[column]]
    if (is.factor(values)) {
      out[[column]] <- as.numeric(values)
    } else if (is.numeric(values) || is.integer(values)) {
      out[[column]] <- as.numeric(values)
    }
  }
  out
}

run_missing_mcar_test <- function(frame, columns = names(frame)) {
  if (!requireNamespace("naniar", quietly = TRUE)) {
    return(data.frame(
      status = "not_run_package_missing",
      n_variables = length(columns),
      statistic = NA_real_,
      df = NA_real_,
      p_value = NA_real_,
      missing_patterns = NA_real_,
      message = "naniar is not installed",
      stringsAsFactors = FALSE
    ))
  }

  columns <- setdiff(intersect(columns, names(frame)), c("aile_no", "group"))
  test_frame <- missing_mcar_numeric_frame(frame[columns])
  test_frame <- test_frame[, colSums(is.na(test_frame)) < nrow(test_frame), drop = FALSE]
  if (ncol(test_frame) < 2L || sum(is.na(test_frame)) == 0L) {
    return(data.frame(
      status = "not_run_insufficient_missingness",
      n_variables = ncol(test_frame),
      statistic = NA_real_,
      df = NA_real_,
      p_value = NA_real_,
      missing_patterns = NA_real_,
      message = "Little MCAR requires at least two usable variables and at least one missing cell",
      stringsAsFactors = FALSE
    ))
  }

  result <- tryCatch(
    suppressWarnings(as.data.frame(naniar::mcar_test(test_frame))),
    error = function(error) error
  )
  if (inherits(result, "error")) {
    return(data.frame(
      status = "error",
      n_variables = ncol(test_frame),
      statistic = NA_real_,
      df = NA_real_,
      p_value = NA_real_,
      missing_patterns = NA_real_,
      message = conditionMessage(result),
      stringsAsFactors = FALSE
    ))
  }

  get_value <- function(candidates) {
    column <- intersect(candidates, names(result))
    if (length(column) == 0L) {
      return(NA_real_)
    }
    as.numeric(result[[column[[1L]]]][[1L]])
  }

  data.frame(
    status = "ok",
    n_variables = ncol(test_frame),
    statistic = get_value(c("statistic", "chi.square", "chi_square")),
    df = get_value(c("df", "d_f")),
    p_value = get_value(c("p.value", "p_value", "p")),
    missing_patterns = get_value(c("missing.patterns", "missing_patterns")),
    message = "",
    stringsAsFactors = FALSE
  )
}

missing_frame_manifest <- function(frames) {
  rows <- lapply(names(frames), function(frame_name) {
    frame <- frames[[frame_name]]
    structural <- missing_structural_matrix(frame, names(frame))
    analytic_missing <- is.na(frame)
    analytic_missing[structural] <- FALSE
    data.frame(
      frame = frame_name,
      n_rows = nrow(frame),
      n_columns = ncol(frame),
      complete_rows = if (ncol(frame) > 0L) sum(stats::complete.cases(frame)) else nrow(frame),
      missing_cells = sum(is.na(frame)),
      structural_missing_cells = sum(is.na(frame) & structural),
      analytic_missing_cells = sum(analytic_missing),
      variables = paste(names(frame), collapse = ";"),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

nmar_delta_grid <- function(variables, delta_values = c(-1, -0.5, 0, 0.5, 1)) {
  variables <- unique(variables)
  rows <- expand.grid(
    variable = variables,
    delta = delta_values,
    stringsAsFactors = FALSE
  )
  rows$target_missing_type <- ifelse(rows$variable %in% missing_dm_only_columns(), "dm_analytic_missing_only", "analytic_missing_only")
  rows$analysis_status <- "sensitivity_template_pending_model"
  rows
}

apply_nmar_delta_adjustment <- function(completed_long, original_frame, variable, delta,
                                        id_column = ".id") {
  if (!variable %in% names(completed_long)) {
    stop(sprintf("completed_long is missing variable: %s", variable), call. = FALSE)
  }
  if (!variable %in% names(original_frame)) {
    stop(sprintf("original_frame is missing variable: %s", variable), call. = FALSE)
  }
  if (!id_column %in% names(completed_long)) {
    stop(sprintf("completed_long is missing id column: %s", id_column), call. = FALSE)
  }

  out <- completed_long
  original_ids <- as.character(seq_len(nrow(original_frame)))
  structural <- missing_structural_mask(original_frame, variable)
  analytic_missing_ids <- original_ids[is.na(original_frame[[variable]]) & !structural]
  adjust <- as.character(out[[id_column]]) %in% analytic_missing_ids
  out[[variable]][adjust] <- out[[variable]][adjust] + delta
  out
}

derive_missing_data_frames <- function(df_family_ses, high_missing_threshold = 0.60,
                                       run_mcar = TRUE, max_patterns = 20L) {
  missing_require_columns(df_family_ses, missing_required_columns(), "missing data frames")

  primary_columns <- missing_primary_columns(df_family_ses)
  clinical_columns <- missing_clinical_columns(df_family_ses)

  fiml_primary <- missing_prepare_analysis_frame(df_family_ses, primary_columns)
  mi_primary <- fiml_primary
  mi_clinical_sensitivity <- missing_prepare_analysis_frame(df_family_ses, clinical_columns)
  complete_case_primary <- missing_complete_case_frame(mi_primary)

  frames <- list(
    fiml_primary = fiml_primary,
    complete_case_primary = complete_case_primary,
    mi_primary = mi_primary,
    mi_clinical_sensitivity = mi_clinical_sensitivity
  )

  primary_spec <- missing_build_mice_spec(mi_primary)
  clinical_spec <- missing_build_mice_spec(mi_clinical_sensitivity)
  mice_specs <- list(
    primary = primary_spec,
    clinical_sensitivity = clinical_spec
  )

  variable_summary <- missing_variable_summary(
    df_family_ses,
    columns = missing_analysis_columns(df_family_ses),
    high_missing_threshold = high_missing_threshold
  )
  block_summary <- missing_block_summary(variable_summary)
  group_summary <- missing_group_summary(df_family_ses, columns = missing_analysis_columns(df_family_ses))
  pattern_summary <- missing_pattern_summary(
    df_family_ses,
    columns = primary_columns,
    max_patterns = max_patterns
  )
  frame_manifest <- missing_frame_manifest(frames)
  method_plan <- rbind(
    missing_mice_method_plan(primary_spec, "mi_primary"),
    missing_mice_method_plan(clinical_spec, "mi_clinical_sensitivity")
  )
  mcar_test <- if (isTRUE(run_mcar)) {
    run_missing_mcar_test(fiml_primary, columns = names(fiml_primary))
  } else {
    data.frame(
      status = "not_run",
      n_variables = ncol(fiml_primary) - 2L,
      statistic = NA_real_,
      df = NA_real_,
      p_value = NA_real_,
      missing_patterns = NA_real_,
      message = "run_mcar = FALSE",
      stringsAsFactors = FALSE
    )
  }

  nmar_variables <- intersect(c("beck_total", "aile_isei08", "hba1c"), clinical_columns)
  list(
    frames = frames,
    mice_specs = mice_specs,
    variable_summary = variable_summary,
    block_summary = block_summary,
    group_summary = group_summary,
    pattern_summary = pattern_summary,
    frame_manifest = frame_manifest,
    mice_method_plan = method_plan,
    mcar_test = mcar_test,
    nmar_delta_grid = nmar_delta_grid(nmar_variables)
  )
}

summarize_missing_targets <- function(df_family_ses, missing_results) {
  manifest <- missing_results$frame_manifest
  data.frame(
    dataset = "family",
    input_rows = nrow(df_family_ses),
    input_columns = ncol(df_family_ses),
    fiml_rows = manifest$n_rows[manifest$frame == "fiml_primary"],
    fiml_columns = manifest$n_columns[manifest$frame == "fiml_primary"],
    primary_complete_rows = manifest$n_rows[manifest$frame == "complete_case_primary"],
    mi_primary_columns = manifest$n_columns[manifest$frame == "mi_primary"],
    mi_clinical_columns = manifest$n_columns[manifest$frame == "mi_clinical_sensitivity"],
    stringsAsFactors = FALSE
  )
}
