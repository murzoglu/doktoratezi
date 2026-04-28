source("R/06_psychometric_validation.R")

psychval_required_package("readr")
psychval_required_package("digest")
psychval_required_package("psych")
psychval_required_package("lavaan")
psychval_required_package("irr")
psychval_required_package("TOSTER")

paths <- list(
  family = "data/processed/FINAL_REFERENCE__analysis_base_family.csv",
  long = "data/processed/FINAL_REFERENCE__analysis_base_long.csv",
  tables = "outputs/tables",
  models = "outputs/models"
)

dir.create(paths$tables, recursive = TRUE, showWarnings = FALSE)
dir.create(paths$models, recursive = TRUE, showWarnings = FALSE)

write_table <- function(x, file_name) {
  utils::write.csv(x, file.path(paths$tables, file_name), row.names = FALSE)
}

expected_hash <- c(
  family = "509d8905aa28b59b9731fedcc88dc3656123a57f7a08cc8dbf37382f8db76aa2",
  long = "764d345eda31453992790e83a1ba20f6fe5dc8ab77d541a3879e13a62359dc97"
)

actual_hash <- c(
  family = digest::digest(paths$family, file = TRUE, algo = "sha256"),
  long = digest::digest(paths$long, file = TRUE, algo = "sha256")
)

if (!identical(unname(actual_hash), unname(expected_hash))) {
  stop("Canonical final-reference hash check failed", call. = FALSE)
}

df_family <- readr::read_csv(paths$family, show_col_types = FALSE)
df_long <- readr::read_csv(paths$long, show_col_types = FALSE)

data_audit <- data.frame(
  file = c(basename(paths$family), basename(paths$long)),
  rows = c(nrow(df_family), nrow(df_long)),
  columns = c(ncol(df_family), ncol(df_long)),
  sha256 = unname(actual_hash),
  expected_sha256 = unname(expected_hash),
  hash_ok = unname(actual_hash) == unname(expected_hash),
  stringsAsFactors = FALSE
)
write_table(data_audit, "psychval_data_audit.csv")

role_counts <- as.data.frame(table(df_long$role), stringsAsFactors = FALSE)
names(role_counts) <- c("role", "n")
write_table(role_counts, "psychval_role_counts.csv")

map <- psychval_embu_subscale_map()
p_cols <- psychval_item_columns("embu_p", 1:29)
c_cols <- psychval_item_columns("embu_c", 1:29)

item_desc_p <- psychval_item_descriptives(
  df_family, p_cols, item_min = 1, item_max = 4,
  form = "EMBU-P", prefix = "embu_p"
)
item_desc_c <- psychval_item_descriptives(
  df_long, c_cols, item_min = 1, item_max = 4,
  form = "EMBU-C", prefix = "embu_c"
)
write_table(item_desc_p, "psychval_item_descriptives_embu_p.csv")
write_table(item_desc_c, "psychval_item_descriptives_embu_c.csv")

reliability <- rbind(
  psychval_reliability_table(df_family, "embu_p", "EMBU-P"),
  psychval_reliability_table(df_long, "embu_c", "EMBU-C"),
  psychval_reliability_table(df_long[df_long$is_index %in% TRUE, ], "embu_c", "EMBU-C index"),
  psychval_reliability_table(df_long[df_long$is_index %in% FALSE, ], "embu_c", "EMBU-C sibling")
)
write_table(reliability, "psychval_reliability.csv")

item_total <- rbind(
  psychval_item_total_table(df_family, "embu_p", "EMBU-P"),
  psychval_item_total_table(df_long, "embu_c", "EMBU-C")
)
write_table(item_total, "psychval_item_total.csv")

family_p_scores <- psychval_score_subscales(
  df_family,
  prefix = "embu_p",
  id_cols = c("aile_no", "group", "role", "cocuk_yas", "anne_yas", "egitim_durumu")
)
family_idx_scores <- psychval_score_subscales(
  df_family,
  prefix = "embu_c_idx",
  id_cols = c("aile_no")
)
family_sib_scores <- psychval_score_subscales(
  df_family,
  prefix = "embu_c_sib",
  id_cols = c("aile_no")
)
names(family_idx_scores)[-1] <- paste0(names(family_idx_scores)[-1], "_idx")
names(family_sib_scores)[-1] <- paste0(names(family_sib_scores)[-1], "_sib")
family_scores <- merge(
  merge(family_p_scores, family_idx_scores, by = "aile_no", all.x = TRUE),
  family_sib_scores,
  by = "aile_no",
  all.x = TRUE
)
family_srq_scores <- psychval_score_srq_subscales(
  df_family,
  prefix = "srq",
  id_cols = c("aile_no")
)
family_srq_sib_scores <- psychval_score_srq_subscales(
  df_family,
  prefix = "srq_sib",
  id_cols = c("aile_no")
)
names(family_srq_sib_scores)[-1] <- paste0("srq_sib_", names(family_srq_sib_scores)[-1])
family_scores <- merge(family_scores, family_srq_scores, by = "aile_no", all.x = TRUE)
family_scores <- merge(family_scores, family_srq_sib_scores, by = "aile_no", all.x = TRUE)
family_scores$beck_total <- psychval_beck_total(df_family)
family_scores$srq_total_mean <- psychval_srq_total_mean(df_family, "srq")
write_table(family_scores, "psychval_scores_family.csv")
write_table(family_srq_scores, "psychval_srq_scores_family.csv")

long_scores <- psychval_score_subscales(
  df_long,
  prefix = "embu_c",
  id_cols = c("aile_no", "cocuk_no", "group", "role", "family_role", "is_index", "cocuk_yas")
)
long_srq_scores <- psychval_score_srq_subscales(
  df_long,
  prefix = "srq",
  id_cols = c("aile_no", "cocuk_no")
)
long_scores <- merge(long_scores, long_srq_scores, by = c("aile_no", "cocuk_no"), all.x = TRUE)
long_scores$srq_total_mean <- psychval_srq_total_mean(df_long, "srq")
write_table(long_scores, "psychval_scores_long.csv")
write_table(long_srq_scores, "psychval_srq_scores_long.csv")

run_efa <- function(data, prefix, form) {
  items <- psychval_numeric_frame(data, psychval_item_columns(prefix, 1:29))
  n_obs <- sum(stats::complete.cases(items))
  result <- tryCatch({
    poly <- psych::polychoric(items)$rho
    kmo <- psych::KMO(poly)
    bart <- psych::cortest.bartlett(poly, n = n_obs)
    fit <- psych::fa(poly, nfactors = 4, n.obs = n_obs, fm = "wls", rotate = "oblimin")
    loadings <- as.data.frame(unclass(fit$loadings), stringsAsFactors = FALSE)
    loadings$item <- rownames(loadings)
    list(
      summary = data.frame(
        form = form,
        n_complete = n_obs,
        kmo_msa = unname(kmo$MSA),
        bartlett_chisq = unname(bart$chisq),
        bartlett_df = unname(bart$df),
        bartlett_p = unname(bart$p.value),
        rmsea = unname(fit$RMSEA[1]),
        tli = unname(fit$TLI),
        error = NA_character_,
        stringsAsFactors = FALSE
      ),
      loadings = cbind(form = form, loadings[, c("item", names(loadings)[names(loadings) != "item"])])
    )
  }, error = function(e) {
    list(
      summary = data.frame(
        form = form,
        n_complete = n_obs,
        kmo_msa = NA_real_,
        bartlett_chisq = NA_real_,
        bartlett_df = NA_real_,
        bartlett_p = NA_real_,
        rmsea = NA_real_,
        tli = NA_real_,
        error = conditionMessage(e),
        stringsAsFactors = FALSE
      ),
      loadings = data.frame()
    )
  })
  result
}

efa_p <- run_efa(df_family, "embu_p", "EMBU-P")
efa_c <- run_efa(df_long, "embu_c", "EMBU-C")
write_table(rbind(efa_p$summary, efa_c$summary), "psychval_efa_summary.csv")
write_table(rbind(efa_p$loadings, efa_c$loadings), "psychval_efa_loadings.csv")

cfa_specs <- list(
  list(data = df_family, prefix = "embu_p", form = "EMBU-P"),
  list(data = df_long, prefix = "embu_c", form = "EMBU-C")
)

cfa_fits <- list()
cfa_indices <- list()
cfa_loadings <- list()
for (spec in cfa_specs) {
  for (model_name in c("one_factor", "four_factor", "second_order", "bifactor")) {
    fit_result <- psychval_safe_cfa(
      spec$data, spec$prefix, spec$form, model_name
    )
    key <- paste(spec$form, model_name, sep = "__")
    cfa_fits[[key]] <- fit_result$fit
    cfa_indices[[key]] <- fit_result$indices
    cfa_loadings[[key]] <- psychval_standardized_loadings(
      fit_result$fit, spec$form, model_name
    )
  }
}
write_table(do.call(rbind, cfa_indices), "psychval_cfa_fit.csv")
write_table(do.call(rbind, cfa_loadings), "psychval_cfa_loadings.csv")
saveRDS(cfa_fits, file.path(paths$models, "psychval_cfa_fits.rds"))

modification_index_rows <- function(fit, form, model_name, top_n = 30) {
  if (is.null(fit)) {
    return(data.frame())
  }
  mi <- tryCatch(
    lavaan::modindices(fit, sort. = TRUE),
    error = function(e) e
  )
  if (inherits(mi, "error") || nrow(mi) == 0) {
    return(data.frame(
      form = form,
      model = model_name,
      lhs = NA_character_,
      op = NA_character_,
      rhs = NA_character_,
      mi = NA_real_,
      epc = NA_real_,
      sepc.all = NA_real_,
      error = if (inherits(mi, "error")) conditionMessage(mi) else NA_character_,
      stringsAsFactors = FALSE
    ))
  }
  keep <- mi[mi$op %in% c("~~", "=~"), , drop = FALSE]
  keep <- utils::head(keep, top_n)
  data.frame(
    form = form,
    model = model_name,
    lhs = keep$lhs,
    op = keep$op,
    rhs = keep$rhs,
    mi = keep$mi,
    epc = keep$epc,
    sepc.all = keep$sepc.all,
    error = NA_character_,
    stringsAsFactors = FALSE
  )
}

modification_indices <- rbind(
  modification_index_rows(cfa_fits[["EMBU-P__four_factor"]], "EMBU-P", "four_factor"),
  modification_index_rows(cfa_fits[["EMBU-C__four_factor"]], "EMBU-C", "four_factor")
)
write_table(modification_indices, "psychval_modification_indices.csv")

multilevel_cfa <- psychval_safe_cfa(
  df_long,
  "embu_c",
  "EMBU-C clustered aile_no",
  "four_factor",
  cluster = "aile_no"
)
write_table(multilevel_cfa$indices, "psychval_multilevel_cfa_fit.csv")
saveRDS(multilevel_cfa$fit, file.path(paths$models, "psychval_multilevel_cfa_embu_c_four_factor.rds"))

run_continuous_cluster_cfa <- function(data, prefix, form, model_name, cluster_var) {
  syntax <- psychval_lavaan_model(prefix, model_name)
  fit <- tryCatch(
    lavaan::cfa(
      syntax,
      data = data,
      estimator = "MLR",
      cluster = cluster_var,
      missing = "fiml",
      std.lv = TRUE
    ),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(data.frame(
      form = form,
      model = model_name,
      method = "continuous_MLR_cluster_robust",
      cluster = cluster_var,
      n_obs = sum(stats::complete.cases(data[psychval_item_columns(prefix, 1:29)])),
      n_clusters = length(unique(data[[cluster_var]][!is.na(data[[cluster_var]])])),
      converged = FALSE,
      cfi_robust = NA_real_,
      tli_robust = NA_real_,
      rmsea_robust = NA_real_,
      srmr = NA_real_,
      chisq_scaled = NA_real_,
      df_scaled = NA_real_,
      pvalue_scaled = NA_real_,
      caveat = "Ordinal items treated as continuous; use only as family-cluster sensitivity.",
      error = conditionMessage(fit),
      stringsAsFactors = FALSE
    ))
  }
  fm <- lavaan::fitMeasures(
    fit,
    c("cfi.robust", "tli.robust", "rmsea.robust", "srmr", "chisq.scaled", "df.scaled", "pvalue.scaled")
  )
  data.frame(
    form = form,
    model = model_name,
    method = "continuous_MLR_cluster_robust",
    cluster = cluster_var,
    n_obs = sum(stats::complete.cases(data[psychval_item_columns(prefix, 1:29)])),
    n_clusters = length(unique(data[[cluster_var]][!is.na(data[[cluster_var]])])),
    converged = isTRUE(lavaan::lavInspect(fit, "converged")),
    cfi_robust = unname(fm["cfi.robust"]),
    tli_robust = unname(fm["tli.robust"]),
    rmsea_robust = unname(fm["rmsea.robust"]),
    srmr = unname(fm["srmr"]),
    chisq_scaled = unname(fm["chisq.scaled"]),
    df_scaled = unname(fm["df.scaled"]),
    pvalue_scaled = unname(fm["pvalue.scaled"]),
    caveat = "Ordinal items treated as continuous; use only as family-cluster sensitivity.",
    error = NA_character_,
    stringsAsFactors = FALSE
  )
}

cluster_cfa_sensitivity <- run_continuous_cluster_cfa(
  df_long,
  "embu_c",
  "EMBU-C clustered aile_no continuous sensitivity",
  "four_factor",
  "aile_no"
)
write_table(cluster_cfa_sensitivity, "psychval_cluster_cfa_sensitivity.csv")

one_factor_check <- do.call(rbind, cfa_indices)
one_factor_check <- one_factor_check[
  one_factor_check$model == "one_factor",
  c("form", "model", "cfi_scaled", "tli_scaled", "rmsea_scaled", "srmr")
]
if (nrow(one_factor_check) == 2) {
  one_factor_check$cfi_tli_exact_match_across_forms <- all(
    one_factor_check$cfi_scaled == one_factor_check$cfi_scaled[1],
    one_factor_check$tli_scaled == one_factor_check$tli_scaled[1],
    na.rm = TRUE
  )
}
write_table(one_factor_check, "psychval_one_factor_anomaly_check.csv")

run_invariance <- function(data, prefix, form, group_var,
                           exclude_items = integer(),
                           item_set = "all_29_items") {
  data <- data[!is.na(data[[group_var]]), , drop = FALSE]
  ordered <- psychval_item_columns(prefix, setdiff(1:29, as.integer(exclude_items)))
  syntax <- psychval_lavaan_model(prefix, "four_factor", exclude_items = exclude_items)
  if (length(unique(data[[group_var]])) < 2) {
    return(data.frame(
      form = form, group_var = group_var, item_set = item_set, level = c("configural", "metric", "scalar"),
      cfi_scaled = NA_real_, rmsea_scaled = NA_real_, srmr = NA_real_,
      delta_cfi = NA_real_, delta_rmsea = NA_real_,
      error = "group_var has fewer than two observed groups",
      stringsAsFactors = FALSE
    ))
  }
  fit_one <- function(level, equal = NULL) {
    tryCatch(
      lavaan::cfa(
        syntax,
        data = data,
        ordered = ordered,
        estimator = "WLSMV",
        group = group_var,
        group.equal = equal,
        std.lv = TRUE
      ),
      error = function(e) e
    )
  }
  fits <- list(
    configural = fit_one("configural"),
    metric = fit_one("metric", "loadings"),
    scalar = fit_one("scalar", c("loadings", "thresholds"))
  )
  rows <- lapply(names(fits), function(level) {
    fit <- fits[[level]]
    if (inherits(fit, "error")) {
      return(data.frame(
        form = form, group_var = group_var, item_set = item_set, level = level,
        cfi_scaled = NA_real_, rmsea_scaled = NA_real_, srmr = NA_real_,
        delta_cfi = NA_real_, delta_rmsea = NA_real_, error = conditionMessage(fit),
        stringsAsFactors = FALSE
      ))
    }
    fm <- lavaan::fitMeasures(fit, c("cfi.scaled", "rmsea.scaled", "srmr"))
    data.frame(
      form = form, group_var = group_var, item_set = item_set, level = level,
      cfi_scaled = unname(fm["cfi.scaled"]),
      rmsea_scaled = unname(fm["rmsea.scaled"]),
      srmr = unname(fm["srmr"]),
      delta_cfi = NA_real_,
      delta_rmsea = NA_real_,
      error = NA_character_,
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)
  for (i in seq_len(nrow(out))[-1]) {
    out$delta_cfi[i] <- out$cfi_scaled[i] - out$cfi_scaled[i - 1]
    out$delta_rmsea[i] <- out$rmsea_scaled[i] - out$rmsea_scaled[i - 1]
  }
  out
}

run_single_factor_invariance <- function(data, prefix, form, group_var,
                                         items, factor_name,
                                         item_set) {
  data <- data[!is.na(data[[group_var]]), , drop = FALSE]
  ordered <- psychval_item_columns(prefix, items)
  syntax <- sprintf("%s =~ %s", factor_name, paste(ordered, collapse = " + "))
  fit_one <- function(level, equal = NULL) {
    tryCatch(
      lavaan::cfa(
        syntax,
        data = data,
        ordered = ordered,
        estimator = "WLSMV",
        group = group_var,
        group.equal = equal,
        std.lv = TRUE
      ),
      error = function(e) e
    )
  }
  fits <- list(
    configural = fit_one("configural"),
    metric = fit_one("metric", "loadings"),
    scalar = fit_one("scalar", c("loadings", "thresholds"))
  )
  rows <- lapply(names(fits), function(level) {
    fit <- fits[[level]]
    if (inherits(fit, "error")) {
      return(data.frame(
        form = form, group_var = group_var, item_set = item_set, level = level,
        cfi_scaled = NA_real_, rmsea_scaled = NA_real_, srmr = NA_real_,
        delta_cfi = NA_real_, delta_rmsea = NA_real_, error = conditionMessage(fit),
        stringsAsFactors = FALSE
      ))
    }
    fm <- lavaan::fitMeasures(fit, c("cfi.scaled", "rmsea.scaled", "srmr"))
    data.frame(
      form = form, group_var = group_var, item_set = item_set, level = level,
      cfi_scaled = unname(fm["cfi.scaled"]),
      rmsea_scaled = unname(fm["rmsea.scaled"]),
      srmr = unname(fm["srmr"]),
      delta_cfi = NA_real_,
      delta_rmsea = NA_real_,
      error = NA_character_,
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)
  for (i in seq_len(nrow(out))[-1]) {
    out$delta_cfi[i] <- out$cfi_scaled[i] - out$cfi_scaled[i - 1]
    out$delta_rmsea[i] <- out$rmsea_scaled[i] - out$rmsea_scaled[i - 1]
  }
  out
}

df_long$age_cat <- cut(
  df_long$cocuk_yas,
  breaks = c(-Inf, 10, 13, Inf),
  labels = c("7-10", "11-13", "14+"),
  right = TRUE
)
df_long$sex_group <- factor(
  ifelse(df_long$katilimci_cocuk_cinsiyet == 0, "cinsiyet_0", "cinsiyet_1")
)

df_long_binary <- psychval_add_collapsed_likert(df_long, c_cols, scheme = "binary_floor")
df_long_binary$age_cat <- df_long$age_cat
df_long_binary$sex_group <- df_long$sex_group

category_sparsity_audit <- function(data, prefix, group_vars, item_set, scheme) {
  rows <- lapply(group_vars, function(group_var) {
    item_rows <- lapply(psychval_item_columns(prefix, 1:29), function(col) {
      tab <- table(data[[group_var]], data[[col]], useNA = "no")
      data.frame(
        group_var = group_var,
        item_set = item_set,
        scheme = scheme,
        item = col,
        n_groups = nrow(tab),
        n_categories = ncol(tab),
        min_cell = if (length(tab) > 0) min(tab) else NA_integer_,
        empty_cell_count = if (length(tab) > 0) sum(tab == 0) else NA_integer_,
        has_empty_cell = if (length(tab) > 0) any(tab == 0) else NA,
        stringsAsFactors = FALSE
      )
    })
    do.call(rbind, item_rows)
  })
  do.call(rbind, rows)
}

category_audit <- rbind(
  category_sparsity_audit(df_long, "embu_c", c("age_cat", "sex_group"), "all_29_items_original_4cat", "original_4cat"),
  category_sparsity_audit(df_long_binary, "embu_c", c("age_cat", "sex_group"), "all_29_items_binary_1_vs_gt1", "binary_1_vs_gt1")
)
write_table(category_audit, "psychval_invariance_category_audit.csv")

df_family_rejection_binary <- df_family
rejection_q12less_items <- setdiff(map$reddetme, 12)
for (col in psychval_item_columns("embu_p", rejection_q12less_items)) {
  df_family_rejection_binary[[col]] <- ifelse(
    is.na(df_family_rejection_binary[[col]]),
    NA_real_,
    ifelse(df_family_rejection_binary[[col]] == 1, 1, 2)
  )
}

invariance <- rbind(
  run_invariance(df_family, "embu_p", "EMBU-P", "group"),
  run_invariance(
    df_family,
    "embu_p",
    "EMBU-P q12siz",
    "group",
    exclude_items = 12,
    item_set = "q12_excluded_28_items"
  ),
  run_single_factor_invariance(
    df_family_rejection_binary,
    "embu_p",
    "EMBU-P q12siz Reddetme binary",
    "group",
    items = rejection_q12less_items,
    factor_name = "reddetme",
    item_set = "q12_excluded_7_rejection_items_binary_1_vs_gt1"
  ),
  run_invariance(df_long, "embu_c", "EMBU-C", "group"),
  run_invariance(df_long, "embu_c", "EMBU-C", "family_role"),
  run_invariance(df_long, "embu_c", "EMBU-C", "age_cat"),
  run_invariance(df_long, "embu_c", "EMBU-C", "sex_group"),
  run_invariance(
    df_long_binary,
    "embu_c",
    "EMBU-C binary",
    "age_cat",
    item_set = "all_29_items_binary_1_vs_gt1"
  ),
  run_invariance(
    df_long_binary,
    "embu_c",
    "EMBU-C binary",
    "sex_group",
    item_set = "all_29_items_binary_1_vs_gt1"
  )
)
write_table(invariance, "psychval_measurement_invariance.csv")

embu_c_mean_cols <- paste0(names(map), "_mean")
icc_scores <- long_scores[, c("aile_no", embu_c_mean_cols)]
icc <- psychval_icc_rows(icc_scores, "aile_no", embu_c_mean_cols)
write_table(icc, "psychval_icc_embu_c.csv")

concordance_rows <- lapply(names(map), function(subscale) {
  idx_col <- paste0(subscale, "_mean_idx")
  sib_col <- paste0(subscale, "_mean_sib")
  pair <- family_scores[, c(idx_col, sib_col)]
  pair <- pair[stats::complete.cases(pair), ]
  icc_value <- tryCatch(
    irr::icc(pair, model = "twoway", type = "agreement", unit = "single")$value,
    error = function(e) NA_real_
  )
  diff <- pair[[idx_col]] - pair[[sib_col]]
  data.frame(
    subscale = subscale,
    n_pairs = nrow(pair),
    icc_2_1_agreement = icc_value,
    mean_difference_idx_minus_sib = mean(diff),
    sd_difference = stats::sd(diff),
    loa_lower = mean(diff) - 1.96 * stats::sd(diff),
    loa_upper = mean(diff) + 1.96 * stats::sd(diff),
    stringsAsFactors = FALSE
  )
})
write_table(do.call(rbind, concordance_rows), "psychval_within_family_concordance.csv")

validity_family_data <- family_scores
family_x <- paste0(names(map), "_mean")
validity_beck <- psychval_correlation_rows(
  validity_family_data,
  family_x,
  "beck_total",
  "EMBU-P vs Beck total"
)
srq_subscale_means <- paste0(names(psychval_srq_subscale_map()), "_mean")
validity_srq_family <- do.call(rbind, lapply(c("srq_total_mean", srq_subscale_means), function(y_var) {
  psychval_correlation_rows(
    validity_family_data,
    "karsilastirma_mean",
    y_var,
    paste("EMBU-P comparison vs", y_var)
  )
}))
validity_srq_long <- do.call(rbind, lapply(c("srq_total_mean", srq_subscale_means), function(y_var) {
  psychval_correlation_rows(
    long_scores,
    "karsilastirma_mean",
    y_var,
    paste("EMBU-C comparison vs", y_var)
  )
}))
write_table(
  rbind(validity_beck, validity_srq_family, validity_srq_long),
  "psychval_validity_correlations.csv"
)

collapse_rejection_items <- function(data, prefix) {
  cols <- psychval_item_columns(prefix, map$reddetme)
  out <- psychval_numeric_frame(data, cols)
  for (col in names(out)) {
    out[[col]] <- ifelse(out[[col]] %in% c(1, 2), 1,
                         ifelse(out[[col]] == 3, 2,
                                ifelse(out[[col]] == 4, 3, NA_real_)))
  }
  rowMeans(out, na.rm = TRUE)
}

rejection_multiverse_data <- data.frame(
  group = df_family$group,
  full_8_item = family_scores$reddetme_mean,
  collapsed_3_category = collapse_rejection_items(df_family, "embu_p"),
  citc_4_item = rowMeans(
    psychval_numeric_frame(
      df_family,
      psychval_item_columns("embu_p", c(5, 9, 10, 16))
    ),
    na.rm = TRUE
  ),
  stringsAsFactors = FALSE
)

run_group_spec <- function(data, score_col, strategy) {
  model_data <- data[, c("group", score_col)]
  model_data <- model_data[stats::complete.cases(model_data), ]
  names(model_data) <- c("group", "score")
  model_data$group <- stats::relevel(factor(model_data$group), ref = "Kontrol")
  fit <- stats::lm(score ~ group, data = model_data)
  coef_row <- summary(fit)$coefficients["groupDM", ]
  dm_score <- model_data$score[model_data$group == "DM"]
  kontrol_score <- model_data$score[model_data$group == "Kontrol"]
  pooled_sd <- sqrt(
    ((length(dm_score) - 1) * stats::var(dm_score) +
       (length(kontrol_score) - 1) * stats::var(kontrol_score)) /
      (length(dm_score) + length(kontrol_score) - 2)
  )
  cohens_d <- (mean(dm_score) - mean(kontrol_score)) / pooled_sd
  data.frame(
    strategy = strategy,
    n = nrow(model_data),
    estimate_dm_minus_kontrol = unname(coef_row["Estimate"]),
    se = unname(coef_row["Std. Error"]),
    t = unname(coef_row["t value"]),
    p_value = unname(coef_row["Pr(>|t|)"]),
    cohens_d_dm_minus_kontrol = cohens_d,
    stringsAsFactors = FALSE
  )
}

multiverse <- rbind(
  run_group_spec(rejection_multiverse_data, "full_8_item", "S1_full_8_item_4_category"),
  run_group_spec(rejection_multiverse_data, "collapsed_3_category", "S2_collapsed_3_category"),
  run_group_spec(rejection_multiverse_data, "citc_4_item", "S3_low_citc_removed_4_item"),
  data.frame(
    strategy = "BSEM_latent_factor",
    n = NA_integer_,
    estimate_dm_minus_kontrol = NA_real_,
    se = NA_real_,
    t = NA_real_,
    p_value = NA_real_,
    cohens_d_dm_minus_kontrol = NA_real_,
    stringsAsFactors = FALSE
  )
)
bsem_group_path <- file.path(paths$tables, "psychval_bsem_latent_group_comparison.csv")
if (file.exists(bsem_group_path)) {
  bsem_group <- read.csv(bsem_group_path, check.names = FALSE, stringsAsFactors = FALSE)
  primary_bsem <- bsem_group[bsem_group$item_set == "all_29_items", , drop = FALSE]
  if (nrow(primary_bsem) > 0) {
    idx <- multiverse$strategy == "BSEM_latent_factor"
    multiverse$n[idx] <- primary_bsem$n[1]
    multiverse$estimate_dm_minus_kontrol[idx] <- primary_bsem$estimate_dm_minus_kontrol[1]
    multiverse$se[idx] <- primary_bsem$se[1]
    multiverse$t[idx] <- primary_bsem$t[1]
    multiverse$p_value[idx] <- primary_bsem$p_value[1]
    multiverse$cohens_d_dm_minus_kontrol[idx] <- primary_bsem$cohens_d_dm_minus_kontrol[1]
  }
}
write_table(multiverse, "psychval_rejection_multiverse.csv")

run_tost_spec <- function(data, score_col, strategy) {
  model_data <- data[, c("group", score_col)]
  model_data <- model_data[stats::complete.cases(model_data), ]
  names(model_data) <- c("group", "score")
  dm_score <- model_data$score[model_data$group == "DM"]
  kontrol_score <- model_data$score[model_data$group == "Kontrol"]
  tost <- tryCatch(
    suppressWarnings(TOSTER::tsum_TOST(
      m1 = mean(dm_score),
      sd1 = stats::sd(dm_score),
      n1 = length(dm_score),
      m2 = mean(kontrol_score),
      sd2 = stats::sd(kontrol_score),
      n2 = length(kontrol_score),
      low_eqbound = -0.30,
      high_eqbound = 0.30,
      eqbound_type = "SMD"
    )),
    error = function(e) e
  )
  if (inherits(tost, "error")) {
    return(data.frame(
      strategy = strategy,
      n_dm = length(dm_score),
      n_kontrol = length(kontrol_score),
      mean_dm = mean(dm_score),
      mean_kontrol = mean(kontrol_score),
      hedges_g = NA_real_,
      g_ci_lower_90 = NA_real_,
      g_ci_upper_90 = NA_real_,
      tost_lower_p = NA_real_,
      tost_upper_p = NA_real_,
      equivalent_at_smd_030 = NA,
      error = conditionMessage(tost),
      stringsAsFactors = FALSE
    ))
  }
  tost_rows <- rownames(tost$TOST)
  data.frame(
    strategy = strategy,
    n_dm = length(dm_score),
    n_kontrol = length(kontrol_score),
    mean_dm = mean(dm_score),
    mean_kontrol = mean(kontrol_score),
    hedges_g = tost$smd$d,
    g_ci_lower_90 = tost$smd$dlow,
    g_ci_upper_90 = tost$smd$dhigh,
    tost_lower_p = tost$TOST$p.value[tost_rows == "TOST Lower"],
    tost_upper_p = tost$TOST$p.value[tost_rows == "TOST Upper"],
    equivalent_at_smd_030 = all(tost$TOST$p.value[tost_rows != "t-test"] < 0.05),
    error = NA_character_,
    stringsAsFactors = FALSE
  )
}

tost <- rbind(
  run_tost_spec(rejection_multiverse_data, "full_8_item", "S1_full_8_item_4_category"),
  run_tost_spec(rejection_multiverse_data, "collapsed_3_category", "S2_collapsed_3_category"),
  run_tost_spec(rejection_multiverse_data, "citc_4_item", "S3_low_citc_removed_4_item")
)
write_table(tost, "psychval_rejection_tost.csv")

if (!file.exists(file.path(paths$tables, "psychval_bsem_status.csv"))) {
  bsem_status <- data.frame(
    analysis = "BSEM",
    status = "pending_dedicated_runner",
    reason = paste(
      "Stan tabanli blavaan MCMC kosusu ayri runner ile calistirilir;",
      "scripts/R/06_psychometric_bsem.R tamamlandiginda bu tablo guncellenir."
    ),
    stringsAsFactors = FALSE
  )
  write_table(bsem_status, "psychval_bsem_status.csv")
}

summary_metrics <- data.frame(
  metric = c(
    "family_rows",
    "long_rows",
    "embu_p_reddetme_alpha_raw",
    "embu_c_reddetme_alpha_raw",
    "embu_p_reddetme_items_floor_gt_60_pct",
    "embu_p_reddetme_items_floor_gt_80_pct",
    "embu_c_icc_reddetme_adjusted",
    "index_sibling_reddetme_icc_2_1"
  ),
  value = c(
    nrow(df_family),
    nrow(df_long),
    reliability$alpha_raw[reliability$form == "EMBU-P" & reliability$subscale == "reddetme"],
    reliability$alpha_raw[reliability$form == "EMBU-C" & reliability$subscale == "reddetme"],
    sum(item_desc_p$subscale == "reddetme" & item_desc_p$floor_pct > 60, na.rm = TRUE),
    sum(item_desc_p$subscale == "reddetme" & item_desc_p$floor_pct > 80, na.rm = TRUE),
    icc$icc_adjusted[icc$score == "reddetme_mean"],
    do.call(rbind, concordance_rows)$icc_2_1_agreement[
      do.call(rbind, concordance_rows)$subscale == "reddetme"
    ]
  ),
  stringsAsFactors = FALSE
)
write_table(summary_metrics, "psychval_summary_metrics.csv")

cat("Psychometric validation outputs written to outputs/tables\n")
