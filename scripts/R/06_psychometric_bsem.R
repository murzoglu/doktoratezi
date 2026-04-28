source("R/06_psychometric_validation.R")

psychval_required_package("readr")
psychval_required_package("digest")
psychval_required_package("blavaan")
psychval_required_package("lavaan")

suppressPackageStartupMessages(library(blavaan))
suppressPackageStartupMessages(library(lavaan))

paths <- list(
  family = "data/processed/FINAL_REFERENCE__analysis_base_family.csv",
  tables = "outputs/tables",
  models = "outputs/models"
)

dir.create(paths$tables, recursive = TRUE, showWarnings = FALSE)
dir.create(paths$models, recursive = TRUE, showWarnings = FALSE)

write_table <- function(x, file_name) {
  utils::write.csv(x, file.path(paths$tables, file_name), row.names = FALSE)
}

expected_family_hash <- "509d8905aa28b59b9731fedcc88dc3656123a57f7a08cc8dbf37382f8db76aa2"
actual_family_hash <- digest::digest(paths$family, file = TRUE, algo = "sha256")
if (!identical(actual_family_hash, expected_family_hash)) {
  stop("Canonical family final-reference hash check failed", call. = FALSE)
}

df_family <- readr::read_csv(paths$family, show_col_types = FALSE)

settings <- list(
  n_chains = as.integer(Sys.getenv("PSYCHVAL_BSEM_CHAINS", "4")),
  burnin = as.integer(Sys.getenv("PSYCHVAL_BSEM_BURNIN", "2000")),
  sample = as.integer(Sys.getenv("PSYCHVAL_BSEM_SAMPLE", "10000")),
  seed = as.integer(Sys.getenv("PSYCHVAL_BSEM_SEED", "20260426")),
  target = Sys.getenv("PSYCHVAL_BSEM_TARGET", "stan"),
  save_lvs = tolower(Sys.getenv("PSYCHVAL_BSEM_SAVE_LVS", "false")) %in% c("1", "true", "yes")
)

options(mc.cores = settings$n_chains)
options(future.globals.maxSize = Inf)
if (requireNamespace("future", quietly = TRUE)) {
  if (future::supportsMulticore()) {
    future::plan(future::multicore, workers = settings$n_chains)
  } else {
    future::plan(future::multisession, workers = settings$n_chains)
  }
}

bsem_specs <- list(
  list(
    analysis = "EMBU-P four_factor BSEM full_29",
    file_stub = "psychval_bsem_embu_p_four_factor_full_29",
    exclude_items = integer(),
    item_set = "all_29_items"
  ),
  list(
    analysis = "EMBU-P four_factor BSEM q12_excluded",
    file_stub = "psychval_bsem_embu_p_four_factor_q12_excluded",
    exclude_items = 12,
    item_set = "q12_excluded_28_items"
  )
)

status_rows <- data.frame(
  analysis = vapply(bsem_specs, `[[`, character(1), "analysis"),
  item_set = vapply(bsem_specs, `[[`, character(1), "item_set"),
  status = "queued",
  started_at = NA_character_,
  finished_at = NA_character_,
  n_chains = settings$n_chains,
  burnin = settings$burnin,
  sample = settings$sample,
  seed = settings$seed + seq_along(bsem_specs) - 1L,
  target = settings$target,
  save_lvs = settings$save_lvs,
  error = NA_character_,
  stringsAsFactors = FALSE
)

existing_status_path <- file.path(paths$tables, "psychval_bsem_status.csv")
if (file.exists(existing_status_path)) {
  existing_status <- read.csv(existing_status_path, check.names = FALSE, stringsAsFactors = FALSE)
  for (col in names(status_rows)) {
    if (!col %in% names(existing_status)) {
      existing_status[[col]] <- NA
    }
  }
  for (i in seq_len(nrow(status_rows))) {
    idx <- match(status_rows$analysis[i], existing_status$analysis)
    if (!is.na(idx)) {
      status_rows[i, names(status_rows)] <- existing_status[idx, names(status_rows)]
      status_rows$n_chains[i] <- settings$n_chains
      status_rows$burnin[i] <- settings$burnin
      status_rows$sample[i] <- settings$sample
      status_rows$seed[i] <- settings$seed + i - 1L
      status_rows$target[i] <- settings$target
      status_rows$save_lvs[i] <- settings$save_lvs
    }
  }
}
write_table(status_rows, "psychval_bsem_status.csv")

as_numeric_vector <- function(x) {
  suppressWarnings(as.numeric(unlist(x, use.names = FALSE)))
}

bsem_convergence_summary <- function(fit, analysis, item_set) {
  rhat <- tryCatch(as_numeric_vector(blavaan::blavInspect(fit, "rhat")), error = function(e) NA_real_)
  neff <- tryCatch(as_numeric_vector(blavaan::blavInspect(fit, "neff")), error = function(e) NA_real_)
  rhat <- rhat[!is.na(rhat)]
  neff <- neff[!is.na(neff)]
  data.frame(
    analysis = analysis,
    item_set = item_set,
    n_rhat = length(rhat),
    max_rhat = if (length(rhat) > 0) max(rhat) else NA_real_,
    median_rhat = if (length(rhat) > 0) stats::median(rhat) else NA_real_,
    pct_rhat_le_1_01 = if (length(rhat) > 0) mean(rhat <= 1.01) * 100 else NA_real_,
    pct_rhat_le_1_05 = if (length(rhat) > 0) mean(rhat <= 1.05) * 100 else NA_real_,
    min_neff = if (length(neff) > 0) min(neff) else NA_real_,
    median_neff = if (length(neff) > 0) stats::median(neff) else NA_real_,
    stringsAsFactors = FALSE
  )
}

bsem_fit_measure_rows <- function(fit, analysis, item_set) {
  values <- tryCatch(lavaan::fitMeasures(fit), error = function(e) e)
  if (inherits(values, "error")) {
    return(data.frame(
      analysis = analysis,
      item_set = item_set,
      measure = NA_character_,
      value = NA_real_,
      error = conditionMessage(values),
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    analysis = analysis,
    item_set = item_set,
    measure = names(values),
    value = as.numeric(values),
    error = NA_character_,
    stringsAsFactors = FALSE
  )
}

bsem_parameter_rows <- function(fit, analysis, item_set) {
  params <- tryCatch(lavaan::standardizedSolution(fit), error = function(e) e)
  if (inherits(params, "error")) {
    return(data.frame(
      analysis = analysis,
      item_set = item_set,
      lhs = NA_character_,
      op = NA_character_,
      rhs = NA_character_,
      est.std = NA_real_,
      se = NA_real_,
      pvalue = NA_real_,
      error = conditionMessage(params),
      stringsAsFactors = FALSE
    ))
  }

  keep <- params[params$op %in% c("=~", "~~"), c("lhs", "op", "rhs", "est.std"), drop = FALSE]
  if (!"se" %in% names(params)) {
    keep$se <- NA_real_
  } else {
    keep$se <- params$se[params$op %in% c("=~", "~~")]
  }
  if (!"pvalue" %in% names(params)) {
    keep$pvalue <- NA_real_
  } else {
    keep$pvalue <- params$pvalue[params$op %in% c("=~", "~~")]
  }
  data.frame(
    analysis = analysis,
    item_set = item_set,
    keep,
    error = NA_character_,
    stringsAsFactors = FALSE
  )
}

bsem_latent_group_comparison <- function(fit, data, analysis, item_set) {
  lvmeans <- tryCatch(blavaan::blavInspect(fit, "lvmeans"), error = function(e) e)
  if (inherits(lvmeans, "error")) {
    lvmeans <- tryCatch(lavaan::lavPredict(fit), error = function(e) e)
  }
  if (inherits(lvmeans, "error") || is.null(dim(lvmeans)) || !"reddetme" %in% colnames(lvmeans)) {
    return(data.frame(
      analysis = analysis,
      item_set = item_set,
      factor = "reddetme",
      n = NA_integer_,
      estimate_dm_minus_kontrol = NA_real_,
      se = NA_real_,
      t = NA_real_,
      p_value = NA_real_,
      cohens_d_dm_minus_kontrol = NA_real_,
      error = if (inherits(lvmeans, "error")) conditionMessage(lvmeans) else "reddetme latent score not available",
      stringsAsFactors = FALSE
    ))
  }
  model_data <- data.frame(
    group = data$group,
    score = as.numeric(lvmeans[, "reddetme"]),
    stringsAsFactors = FALSE
  )
  model_data <- model_data[stats::complete.cases(model_data), ]
  model_data$group <- stats::relevel(factor(model_data$group), ref = "Kontrol")
  fit_lm <- stats::lm(score ~ group, data = model_data)
  coef_row <- summary(fit_lm)$coefficients["groupDM", ]
  dm_score <- model_data$score[model_data$group == "DM"]
  kontrol_score <- model_data$score[model_data$group == "Kontrol"]
  pooled_sd <- sqrt(
    ((length(dm_score) - 1) * stats::var(dm_score) +
       (length(kontrol_score) - 1) * stats::var(kontrol_score)) /
      (length(dm_score) + length(kontrol_score) - 2)
  )
  data.frame(
    analysis = analysis,
    item_set = item_set,
    factor = "reddetme",
    n = nrow(model_data),
    estimate_dm_minus_kontrol = unname(coef_row["Estimate"]),
    se = unname(coef_row["Std. Error"]),
    t = unname(coef_row["t value"]),
    p_value = unname(coef_row["Pr(>|t|)"]),
    cohens_d_dm_minus_kontrol = (mean(dm_score) - mean(kontrol_score)) / pooled_sd,
    error = NA_character_,
    stringsAsFactors = FALSE
  )
}

fit_rows <- list()
conv_rows <- list()
parameter_rows <- list()
group_rows <- list()

for (i in seq_along(bsem_specs)) {
  spec <- bsem_specs[[i]]
  model_path <- file.path(paths$models, paste0(spec$file_stub, ".rds"))
  summary_path <- file.path(paths$models, paste0(spec$file_stub, "_summary.txt"))

  if (file.exists(model_path)) {
    status_rows$status[i] <- "completed"
    if (is.na(status_rows$started_at[i])) {
      status_rows$started_at[i] <- format(file.info(model_path)$mtime, "%Y-%m-%d %H:%M:%S %Z")
    }
    if (is.na(status_rows$finished_at[i])) {
      status_rows$finished_at[i] <- format(file.info(model_path)$mtime, "%Y-%m-%d %H:%M:%S %Z")
    }
    status_rows$error[i] <- NA_character_
    write_table(status_rows, "psychval_bsem_status.csv")

    fit_result <- readRDS(model_path)
    if (!file.exists(summary_path)) {
      writeLines(
        capture.output(summary(fit_result, fit.measures = TRUE, standardized = TRUE)),
        summary_path
      )
    }

    fit_rows[[spec$analysis]] <- bsem_fit_measure_rows(fit_result, spec$analysis, spec$item_set)
    conv_rows[[spec$analysis]] <- bsem_convergence_summary(fit_result, spec$analysis, spec$item_set)
    parameter_rows[[spec$analysis]] <- bsem_parameter_rows(fit_result, spec$analysis, spec$item_set)
    group_rows[[spec$analysis]] <- bsem_latent_group_comparison(fit_result, df_family, spec$analysis, spec$item_set)
    next
  }

  started_at <- format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")
  status_rows$status[i] <- "running"
  status_rows$started_at[i] <- started_at
  write_table(status_rows, "psychval_bsem_status.csv")

  ordered <- psychval_item_columns("embu_p", setdiff(1:29, spec$exclude_items))
  syntax <- psychval_lavaan_model(
    "embu_p",
    model = "four_factor",
    exclude_items = spec$exclude_items
  )

  fit_result <- tryCatch(
    blavaan::bcfa(
      syntax,
      data = df_family,
      ordered = ordered,
      std.lv = TRUE,
      n.chains = settings$n_chains,
      burnin = settings$burnin,
      sample = settings$sample,
      target = settings$target,
      seed = settings$seed + i - 1,
      save.lvs = settings$save_lvs,
      dp = blavaan::dpriors(
        lambda = "normal(0.5,0.5)",
        nu = "normal(0,1)"
      )
    ),
    error = function(e) e
  )

  finished_at <- format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")
  status_rows$finished_at[i] <- finished_at

  if (inherits(fit_result, "error")) {
    status_rows$status[i] <- "failed"
    status_rows$error[i] <- conditionMessage(fit_result)
    write_table(status_rows, "psychval_bsem_status.csv")
    fit_rows[[spec$analysis]] <- data.frame(
      analysis = spec$analysis,
      item_set = spec$item_set,
      measure = NA_character_,
      value = NA_real_,
      error = conditionMessage(fit_result),
      stringsAsFactors = FALSE
    )
    next
  }

  status_rows$status[i] <- "completed"
  write_table(status_rows, "psychval_bsem_status.csv")

  saveRDS(fit_result, model_path)
  writeLines(
    capture.output(summary(fit_result, fit.measures = TRUE, standardized = TRUE)),
    summary_path
  )

  fit_rows[[spec$analysis]] <- bsem_fit_measure_rows(fit_result, spec$analysis, spec$item_set)
  conv_rows[[spec$analysis]] <- bsem_convergence_summary(fit_result, spec$analysis, spec$item_set)
  parameter_rows[[spec$analysis]] <- bsem_parameter_rows(fit_result, spec$analysis, spec$item_set)
  group_rows[[spec$analysis]] <- bsem_latent_group_comparison(fit_result, df_family, spec$analysis, spec$item_set)
}

write_table(do.call(rbind, fit_rows), "psychval_bsem_fit_measures.csv")
if (length(conv_rows) > 0) {
  write_table(do.call(rbind, conv_rows), "psychval_bsem_convergence.csv")
}
if (length(parameter_rows) > 0) {
  write_table(do.call(rbind, parameter_rows), "psychval_bsem_parameters.csv")
}
if (length(group_rows) > 0) {
  latent_groups <- do.call(rbind, group_rows)
  write_table(latent_groups, "psychval_bsem_latent_group_comparison.csv")

  multiverse_path <- file.path(paths$tables, "psychval_rejection_multiverse.csv")
  if (file.exists(multiverse_path)) {
    multiverse <- read.csv(multiverse_path, check.names = FALSE, stringsAsFactors = FALSE)
    primary <- latent_groups[latent_groups$item_set == "all_29_items", , drop = FALSE]
    if (nrow(primary) > 0 && "BSEM_latent_factor" %in% multiverse$strategy) {
      idx <- multiverse$strategy == "BSEM_latent_factor"
      multiverse$n[idx] <- primary$n[1]
      multiverse$estimate_dm_minus_kontrol[idx] <- primary$estimate_dm_minus_kontrol[1]
      multiverse$se[idx] <- primary$se[1]
      multiverse$t[idx] <- primary$t[1]
      multiverse$p_value[idx] <- primary$p_value[1]
      multiverse$cohens_d_dm_minus_kontrol[idx] <- primary$cohens_d_dm_minus_kontrol[1]
      write_table(multiverse, "psychval_rejection_multiverse.csv")
    }
  }
}

cat("BSEM outputs written to outputs/tables and outputs/models\n")
