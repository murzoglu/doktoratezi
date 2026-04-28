table1_default_spec <- function() {
  data.frame(
    variable = c(
      "anne_yas",
      "egitim_durumu",
      "es_egitim_durumu",
      "calisma_durumu",
      "es_calisma_durumu",
      "es_isei08",
      "aile_isei08",
      "ses_latent",
      "cocuk_sayisi",
      "age_gap",
      "same_sex",
      "ev_sahipligi",
      "ev_oda_sayisi",
      "arabaniz_var_mi",
      "kronik_hastalik_durumu",
      "anne_antidepresan",
      "beck_total",
      "beck_severity"
    ),
    label = c(
      "Anne yas",
      "Anne egitim durumu",
      "Es egitim durumu",
      "Anne calisma durumu",
      "Es calisma durumu",
      "Es ISEI-08",
      "Aile ISEI-08",
      "Latent SES",
      "Cocuk sayisi",
      "Kardes yas farki",
      "Ayni cinsiyet kardes cifti",
      "Ev sahipligi",
      "Ev oda sayisi",
      "Araba sahipligi",
      "Anne kronik hastalik",
      "Anne antidepresan kullanimi",
      "Beck toplam",
      "Beck siddet kategorisi"
    ),
    type = c(
      "continuous",
      "categorical",
      "categorical",
      "binary",
      "binary",
      "continuous",
      "continuous",
      "continuous",
      "continuous",
      "continuous",
      "binary",
      "binary",
      "continuous",
      "binary",
      "binary",
      "binary",
      "continuous",
      "categorical"
    ),
    block = c(
      "Demografi",
      "SES",
      "SES",
      "Demografi",
      "Demografi",
      "SES",
      "SES",
      "SES",
      "Aile yapisi",
      "Aile yapisi",
      "Aile yapisi",
      "Materyal",
      "Materyal",
      "Materyal",
      "Klinik",
      "Klinik",
      "Klinik",
      "Klinik"
    ),
    stringsAsFactors = FALSE
  )
}

table1_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("%s is missing required column(s): %s", context, paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

table1_group_levels <- function(group) {
  observed <- unique(as.character(group[!is.na(group)]))
  preferred <- c("DM", "Kontrol")
  if (all(preferred %in% observed)) {
    return(preferred)
  }
  observed <- sort(observed)
  if (length(observed) != 2L) {
    stop("Table 1 requires exactly two non-missing group levels", call. = FALSE)
  }
  observed
}

table1_numeric <- function(x) {
  suppressWarnings(as.numeric(x))
}

table1_format_number <- function(x, digits = 2L) {
  if (is.na(x) || !is.finite(x)) {
    return("")
  }
  formatC(x, format = "f", digits = digits)
}

table1_format_p <- function(p) {
  if (is.na(p) || !is.finite(p)) {
    return("")
  }
  if (p < 0.001) {
    return("<0.001")
  }
  sub("^0", "", formatC(p, format = "f", digits = 3L))
}

table1_continuous_stats <- function(x) {
  x <- table1_numeric(x)
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
    stringsAsFactors = FALSE
  )
}

table1_format_continuous <- function(x) {
  stats <- table1_continuous_stats(x)
  sprintf(
    "%s (%s); %s [%s, %s]",
    table1_format_number(stats$mean),
    table1_format_number(stats$sd),
    table1_format_number(stats$median),
    table1_format_number(stats$q1),
    table1_format_number(stats$q3)
  )
}

table1_values_by_group <- function(x, group, group_levels) {
  list(
    overall = x,
    group_1 = x[as.character(group) == group_levels[[1L]]],
    group_2 = x[as.character(group) == group_levels[[2L]]]
  )
}

table1_pooled_sd <- function(x1, x2) {
  x1 <- x1[!is.na(x1)]
  x2 <- x2[!is.na(x2)]
  if (length(x1) < 2L || length(x2) < 2L) {
    return(NA_real_)
  }
  pooled <- sqrt((stats::var(x1) + stats::var(x2)) / 2)
  if (is.na(pooled) || pooled == 0) {
    return(NA_real_)
  }
  pooled
}

table1_smd_continuous <- function(x, group, group_levels = table1_group_levels(group)) {
  x <- table1_numeric(x)
  x1 <- x[as.character(group) == group_levels[[1L]]]
  x2 <- x[as.character(group) == group_levels[[2L]]]
  pooled <- table1_pooled_sd(x1, x2)
  smd <- if (is.na(pooled)) NA_real_ else (mean(x1, na.rm = TRUE) - mean(x2, na.rm = TRUE)) / pooled
  data.frame(
    smd = smd,
    abs_smd = abs(smd),
    method = "mean_difference_pooled_sd",
    smd_level = NA_character_,
    stringsAsFactors = FALSE
  )
}

table1_binary_target_level <- function(x) {
  values <- sort(unique(as.character(x[!is.na(x)])))
  if ("1" %in% values) {
    return("1")
  }
  if ("Evet" %in% values) {
    return("Evet")
  }
  values[[length(values)]]
}

table1_smd_binary <- function(x, group, group_levels = table1_group_levels(group),
                              target_level = table1_binary_target_level(x)) {
  x <- as.character(x)
  g <- as.character(group)
  p1 <- mean(x[g == group_levels[[1L]]] == target_level, na.rm = TRUE)
  p2 <- mean(x[g == group_levels[[2L]]] == target_level, na.rm = TRUE)
  pooled <- sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
  smd <- if (is.na(pooled) || pooled == 0) NA_real_ else (p1 - p2) / pooled
  data.frame(
    smd = smd,
    abs_smd = abs(smd),
    method = "binary_proportion_pooled_sd",
    smd_level = target_level,
    stringsAsFactors = FALSE
  )
}

table1_smd_categorical <- function(x, group, group_levels = table1_group_levels(group)) {
  levels_observed <- sort(unique(as.character(x[!is.na(x)])))
  if (length(levels_observed) == 0L) {
    return(data.frame(
      smd = NA_real_,
      abs_smd = NA_real_,
      method = "max_abs_level_smd",
      smd_level = NA_character_,
      stringsAsFactors = FALSE
    ))
  }
  level_smds <- lapply(levels_observed, function(level) {
    table1_smd_binary(x, group, group_levels = group_levels, target_level = level)
  })
  out <- do.call(rbind, level_smds)
  idx <- which.max(out$abs_smd)
  data.frame(
    smd = out$smd[[idx]],
    abs_smd = out$abs_smd[[idx]],
    method = "max_abs_level_smd",
    smd_level = out$smd_level[[idx]],
    stringsAsFactors = FALSE
  )
}

table1_smd_for_variable <- function(x, group, type, group_levels = table1_group_levels(group)) {
  if (type == "continuous") {
    return(table1_smd_continuous(x, group, group_levels))
  }
  if (type == "binary") {
    return(table1_smd_binary(x, group, group_levels))
  }
  table1_smd_categorical(x, group, group_levels)
}

table1_p_value <- function(x, group, type, group_levels = table1_group_levels(group)) {
  keep <- !is.na(x) & !is.na(group)
  x <- x[keep]
  group <- factor(as.character(group[keep]), levels = group_levels)
  if (length(unique(group[!is.na(group)])) != 2L) {
    return(NA_real_)
  }

  result <- tryCatch({
    if (type == "continuous") {
      stats::wilcox.test(table1_numeric(x) ~ group, exact = FALSE)$p.value
    } else {
      tab <- table(group, x)
      if (all(dim(tab) >= 2L)) {
        stats::fisher.test(tab)$p.value
      } else {
        NA_real_
      }
    }
  }, error = function(error) NA_real_)
  as.numeric(result)
}

table1_balance_flag <- function(abs_smd) {
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

table1_balance_action <- function(flag) {
  switch(
    flag,
    iyi_denge = "standart_analiz_yeterli",
    sinirda = "kovaryat_olarak_ayarla",
    dengesiz = "iptw_ve_kovaryat_ayari",
    ciddi_dengesizlik = "stratified_sensitivity_zorunlu",
    "incele"
  )
}

table1_categorical_levels <- function(x) {
  if (is.factor(x)) {
    levels <- levels(x)
    return(levels[levels %in% as.character(x[!is.na(x)])])
  }
  sort(unique(as.character(x[!is.na(x)])))
}

table1_format_level <- function(x, level) {
  x <- as.character(x)
  denom <- sum(!is.na(x))
  n <- sum(x == level, na.rm = TRUE)
  pct <- if (denom > 0L) n / denom * 100 else NA_real_
  sprintf("%d (%s%%)", n, table1_format_number(pct, digits = 1L))
}

table1_continuous_row <- function(df, variable, label, block, group_column, group_levels, smd, p_value) {
  values <- table1_values_by_group(df[[variable]], df[[group_column]], group_levels)
  stats <- table1_continuous_stats(values$overall)
  data.frame(
    variable = variable,
    label = label,
    block = block,
    row_type = "continuous",
    level = "",
    overall = table1_format_continuous(values$overall),
    n_overall = stats$n,
    missing_n = stats$missing_n,
    missing_pct = stats$missing_n / length(values$overall) * 100,
    setNames(
      data.frame(
        table1_format_continuous(values$group_1),
        table1_format_continuous(values$group_2),
        check.names = FALSE,
        stringsAsFactors = FALSE
      ),
      group_levels
    ),
    smd = smd$smd,
    abs_smd = smd$abs_smd,
    smd_method = smd$method,
    smd_level = smd$smd_level,
    balance_flag = table1_balance_flag(smd$abs_smd),
    p_value = p_value,
    p_value_fmt = table1_format_p(p_value),
    stringsAsFactors = FALSE
  )
}

table1_categorical_rows <- function(df, variable, label, block, group_column, group_levels, smd, p_value) {
  x <- df[[variable]]
  values <- table1_values_by_group(x, df[[group_column]], group_levels)
  levels <- table1_categorical_levels(x)
  rows <- lapply(seq_along(levels), function(i) {
    level <- levels[[i]]
    data.frame(
      variable = variable,
      label = label,
      block = block,
      row_type = "level",
      level = level,
      overall = table1_format_level(values$overall, level),
      n_overall = sum(!is.na(values$overall)),
      missing_n = sum(is.na(values$overall)),
      missing_pct = mean(is.na(values$overall)) * 100,
      setNames(
        data.frame(
          table1_format_level(values$group_1, level),
          table1_format_level(values$group_2, level),
          check.names = FALSE,
          stringsAsFactors = FALSE
        ),
        group_levels
      ),
      smd = if (i == 1L) smd$smd else NA_real_,
      abs_smd = if (i == 1L) smd$abs_smd else NA_real_,
      smd_method = if (i == 1L) smd$method else NA_character_,
      smd_level = if (i == 1L) smd$smd_level else NA_character_,
      balance_flag = if (i == 1L) table1_balance_flag(smd$abs_smd) else NA_character_,
      p_value = if (i == 1L) p_value else NA_real_,
      p_value_fmt = if (i == 1L) table1_format_p(p_value) else "",
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)

  if (any(is.na(x))) {
    missing_row <- data.frame(
      variable = variable,
      label = label,
      block = block,
      row_type = "missing",
      level = "Eksik",
      overall = sprintf("%d (%s%%)", sum(is.na(values$overall)), table1_format_number(mean(is.na(values$overall)) * 100, 1L)),
      n_overall = sum(!is.na(values$overall)),
      missing_n = sum(is.na(values$overall)),
      missing_pct = mean(is.na(values$overall)) * 100,
      setNames(
        data.frame(
          sprintf("%d (%s%%)", sum(is.na(values$group_1)), table1_format_number(mean(is.na(values$group_1)) * 100, 1L)),
          sprintf("%d (%s%%)", sum(is.na(values$group_2)), table1_format_number(mean(is.na(values$group_2)) * 100, 1L)),
          check.names = FALSE,
          stringsAsFactors = FALSE
        ),
        group_levels
      ),
      smd = NA_real_,
      abs_smd = NA_real_,
      smd_method = NA_character_,
      smd_level = NA_character_,
      balance_flag = NA_character_,
      p_value = NA_real_,
      p_value_fmt = "",
      stringsAsFactors = FALSE
    )
    out <- rbind(out, missing_row)
  }

  out
}

table1_variable_row <- function(df, spec_row, group_column, group_levels) {
  variable <- spec_row$variable
  type <- spec_row$type
  smd <- table1_smd_for_variable(df[[variable]], df[[group_column]], type, group_levels)
  p_value <- table1_p_value(df[[variable]], df[[group_column]], type, group_levels)
  if (type == "continuous") {
    return(table1_continuous_row(
      df,
      variable,
      spec_row$label,
      spec_row$block,
      group_column,
      group_levels,
      smd,
      p_value
    ))
  }
  table1_categorical_rows(
    df,
    variable,
    spec_row$label,
    spec_row$block,
    group_column,
    group_levels,
    smd,
    p_value
  )
}

table1_smd_balance <- function(table_rows) {
  rows <- table_rows[!is.na(table_rows$abs_smd), , drop = FALSE]
  out <- rows[, c(
    "variable", "label", "block", "smd", "abs_smd", "smd_method",
    "smd_level", "balance_flag", "p_value", "p_value_fmt"
  ), drop = FALSE]
  out$recommended_action <- vapply(out$balance_flag, table1_balance_action, character(1L))
  out <- out[order(-out$abs_smd, out$variable), , drop = FALSE]
  rownames(out) <- NULL
  out
}

table1_add_q_values <- function(table_rows) {
  variable_rows <- !is.na(table_rows$p_value)
  q_values <- rep(NA_real_, nrow(table_rows))
  q_values[variable_rows] <- stats::p.adjust(table_rows$p_value[variable_rows], method = "BH")
  table_rows$q_value <- q_values
  table_rows$q_value_fmt <- vapply(q_values, table1_format_p, character(1L))
  table_rows
}

build_table1_family <- function(df, spec = table1_default_spec(), group_column = "group") {
  table1_require_columns(df, group_column, "Table 1")
  spec <- spec[spec$variable %in% names(df), , drop = FALSE]
  table1_require_columns(df, spec$variable, "Table 1")
  if (nrow(spec) == 0L) {
    stop("Table 1 variable spec has no variables present in data", call. = FALSE)
  }
  group_levels <- table1_group_levels(df[[group_column]])

  rows <- lapply(seq_len(nrow(spec)), function(i) {
    table1_variable_row(df, spec[i, , drop = FALSE], group_column, group_levels)
  })
  table_rows <- do.call(rbind, rows)
  table_rows <- table1_add_q_values(table_rows)
  balance <- table1_smd_balance(table_rows)

  list(
    table = table_rows,
    smd_balance = balance,
    balance_action = balance[balance$abs_smd >= 0.10 | is.na(balance$abs_smd), , drop = FALSE],
    group_counts = data.frame(
      group = group_levels,
      n = as.integer(table(factor(as.character(df[[group_column]]), levels = group_levels))),
      stringsAsFactors = FALSE
    )
  )
}

summarize_table1_targets <- function(df, table1_results) {
  data.frame(
    dataset = "family",
    input_rows = nrow(df),
    input_columns = ncol(df),
    table_rows = nrow(table1_results$table),
    smd_variables = nrow(table1_results$smd_balance),
    action_variables = nrow(table1_results$balance_action),
    group_1 = table1_results$group_counts$group[[1L]],
    group_1_n = table1_results$group_counts$n[[1L]],
    group_2 = table1_results$group_counts$group[[2L]],
    group_2_n = table1_results$group_counts$n[[2L]],
    stringsAsFactors = FALSE
  )
}
