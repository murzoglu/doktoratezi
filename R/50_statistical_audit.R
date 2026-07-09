# KISIM XXXIII — deterministik istatistik dogruluk/tutarlilik denetimi

stat_audit_empty_findings <- function() {
  data.frame(
    domain = character(),
    table_id = character(),
    check_id = character(),
    severity = character(),
    row_index = integer(),
    column = character(),
    observed = character(),
    expected = character(),
    message = character(),
    stringsAsFactors = FALSE
  )
}

stat_audit_scalar <- function(x) {
  if (length(x) == 0L || is.null(x)) {
    return(NA_character_)
  }
  if (is.numeric(x)) {
    return(paste(format(signif(x, 8L), scientific = FALSE, trim = TRUE), collapse = ";"))
  }
  paste(as.character(x), collapse = ";")
}

stat_audit_finding <- function(domain, check_id, severity, message,
                               table_id = "data_contract", row_index = NA_integer_,
                               column = NA_character_, observed = NA, expected = NA) {
  data.frame(
    domain = domain,
    table_id = table_id,
    check_id = check_id,
    severity = severity,
    row_index = as.integer(row_index)[1L],
    column = as.character(column)[1L],
    observed = stat_audit_scalar(observed),
    expected = stat_audit_scalar(expected),
    message = message,
    stringsAsFactors = FALSE
  )
}

stat_audit_bind_findings <- function(...) {
  dfs <- list(...)
  if (length(dfs) == 1L && is.list(dfs[[1L]]) && !is.data.frame(dfs[[1L]])) {
    dfs <- dfs[[1L]]
  }
  dfs <- dfs[vapply(dfs, is.data.frame, logical(1))]
  dfs <- dfs[vapply(dfs, nrow, integer(1)) > 0L]
  if (length(dfs) == 0L) {
    return(stat_audit_empty_findings())
  }

  cols <- names(stat_audit_empty_findings())
  aligned <- lapply(dfs, function(df) {
    missing <- setdiff(cols, names(df))
    for (col in missing) {
      df[[col]] <- NA
    }
    df[, cols, drop = FALSE]
  })
  do.call(rbind, aligned)
}

stat_audit_numeric <- function(x) {
  suppressWarnings(as.numeric(x))
}

stat_audit_first_col <- function(df, candidates) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0L) {
    return(NA_character_)
  }
  hit[[1L]]
}

stat_audit_relative_mismatch <- function(observed, expected, tolerance) {
  ok <- is.finite(observed) & is.finite(expected)
  mismatch <- rep(FALSE, length(observed))
  mismatch[ok] <- abs(observed[ok] - expected[ok]) >
    pmax(tolerance, abs(expected[ok]) * tolerance)
  mismatch
}

stat_audit_missing_column_findings <- function(df, required, table_id, domain) {
  missing <- setdiff(required, names(df))
  if (length(missing) == 0L) {
    return(stat_audit_empty_findings())
  }
  stat_audit_finding(
    domain = domain,
    table_id = table_id,
    check_id = "required_columns",
    severity = "critical",
    column = paste(missing, collapse = ","),
    observed = paste(names(df), collapse = ","),
    expected = paste(required, collapse = ","),
    message = "Required audit column(s) are missing."
  )
}

audit_data_contract <- function(df_family, df_long) {
  findings <- list()
  findings[[length(findings) + 1L]] <- stat_audit_missing_column_findings(
    df_family,
    c("aile_no", "group"),
    "family",
    "data_contract"
  )
  findings[[length(findings) + 1L]] <- stat_audit_missing_column_findings(
    df_long,
    c("aile_no", "group"),
    "long",
    "data_contract"
  )

  if (all(c("aile_no", "group") %in% names(df_family))) {
    family_key <- as.character(df_family$aile_no)
    duplicated_family <- family_key[duplicated(family_key) | duplicated(family_key, fromLast = TRUE)]
    if (length(duplicated_family) > 0L) {
      findings[[length(findings) + 1L]] <- stat_audit_finding(
        domain = "data_contract",
        table_id = "family",
        check_id = "family_key_unique",
        severity = "critical",
        observed = paste(sort(unique(duplicated_family)), collapse = ","),
        expected = "unique aile_no",
        message = "Family analysis base must have one row per aile_no."
      )
    }

    if ("hba1c" %in% names(df_family)) {
      hba1c <- stat_audit_numeric(df_family$hba1c)
      control_with_hba1c <- !is.na(hba1c) & as.character(df_family$group) != "DM"
      if (any(control_with_hba1c, na.rm = TRUE)) {
        findings[[length(findings) + 1L]] <- stat_audit_finding(
          domain = "data_contract",
          table_id = "family",
          check_id = "hba1c_structural_missingness",
          severity = "critical",
          row_index = which(control_with_hba1c)[1L],
          column = "hba1c",
          observed = paste(unique(as.character(df_family$group[control_with_hba1c])), collapse = ","),
          expected = "hba1c only populated for DM index families",
          message = "HbA1c is structurally missing outside the DM index stratum."
        )
      }
      hba1c_min <- 4.5
      hba1c_max <- 18.0
      out_of_range_hba1c <- !is.na(hba1c) & (hba1c < hba1c_min | hba1c > hba1c_max)
      if (any(out_of_range_hba1c, na.rm = TRUE)) {
        findings[[length(findings) + 1L]] <- stat_audit_finding(
          domain = "data_contract",
          table_id = "family",
          check_id = "hba1c_plausibility_range",
          severity = "review",
          row_index = which(out_of_range_hba1c)[1L],
          column = "hba1c",
          observed = hba1c[out_of_range_hba1c],
          expected = sprintf("%.1f <= hba1c <= %.1f", hba1c_min, hba1c_max),
          message = "HbA1c value is outside the canonical clinical plausibility range."
        )
      }
    }
  }

  if (all(c("aile_no", "group") %in% names(df_long))) {
    long_key <- as.character(df_long$aile_no)
    pair_counts <- table(long_key)
    bad_pairs <- pair_counts[pair_counts != 2L]
    if (length(bad_pairs) > 0L) {
      findings[[length(findings) + 1L]] <- stat_audit_finding(
        domain = "data_contract",
        table_id = "long",
        check_id = "long_family_pair_count",
        severity = "critical",
        observed = paste(names(bad_pairs), as.integer(bad_pairs), sep = ":", collapse = ","),
        expected = "2 rows per aile_no",
        message = "Long analysis base must keep the index-sibling dyad structure."
      )
    }

    group_counts <- tapply(as.character(df_long$group), long_key, function(x) length(unique(x[!is.na(x)])))
    inconsistent_group <- names(group_counts)[group_counts > 1L]
    if (length(inconsistent_group) > 0L) {
      findings[[length(findings) + 1L]] <- stat_audit_finding(
        domain = "data_contract",
        table_id = "long",
        check_id = "long_group_consistency",
        severity = "critical",
        observed = paste(inconsistent_group, collapse = ","),
        expected = "one group level per aile_no",
        message = "A family cannot contain mixed group labels in the long analysis base."
      )
    }
  }

  if (all(c("aile_no", "group") %in% names(df_family)) &&
      all(c("aile_no", "group") %in% names(df_long))) {
    family_ids <- unique(as.character(df_family$aile_no))
    long_ids <- unique(as.character(df_long$aile_no))
    missing_long <- setdiff(family_ids, long_ids)
    missing_family <- setdiff(long_ids, family_ids)
    if (length(missing_long) > 0L || length(missing_family) > 0L) {
      findings[[length(findings) + 1L]] <- stat_audit_finding(
        domain = "data_contract",
        table_id = "family_long",
        check_id = "family_long_key_match",
        severity = "critical",
        observed = paste(c(paste0("family_only:", missing_long), paste0("long_only:", missing_family)), collapse = ","),
        expected = "same aile_no set",
        message = "Family and long analysis bases must use the same family key set."
      )
    }
  }

  stat_audit_bind_findings(findings)
}

audit_result_table_consistency <- function(table, table_id = "result_table",
                                           stat_tolerance = 1e-6,
                                           p_tolerance = 1e-6) {
  if (is.null(table) || !is.data.frame(table) || nrow(table) == 0L) {
    return(stat_audit_empty_findings())
  }

  findings <- list()
  estimate_col <- stat_audit_first_col(table, c("estimate", "est", "tahmin", "std_beta", "std.all"))
  se_col <- stat_audit_first_col(table, c("std_error", "se", "SE", "Std..Error", "Std. Error"))
  stat_col <- stat_audit_first_col(table, c("statistic", "t", "z", "t.value", "t_value", "z_value"))
  p_col <- stat_audit_first_col(table, c("p_value", "pvalue", "p.value", "p"))
  df_col <- stat_audit_first_col(table, c("df_residual", "df", "df_error", "DF", "Df"))
  ci_low_col <- stat_audit_first_col(table, c("ci_low", "ci_alt", "alt_ga", "ci.lower", "std_beta_ci_low", "lower.CL", "asymp.LCL"))
  ci_high_col <- stat_audit_first_col(table, c("ci_high", "ci_ust", "ust_ga", "ci.upper", "std_beta_ci_high", "upper.CL", "asymp.UCL"))
  has_adjusted_p <- "adjust" %in% names(table) &&
    any(nzchar(as.character(table$adjust)) &
      !tolower(as.character(table$adjust)) %in% c("none", "raw", "unadjusted"), na.rm = TRUE)

  if (!is.na(estimate_col) && !is.na(se_col) && !is.na(stat_col)) {
    estimate <- stat_audit_numeric(table[[estimate_col]])
    se <- stat_audit_numeric(table[[se_col]])
    observed <- stat_audit_numeric(table[[stat_col]])
    keep <- is.finite(estimate) & is.finite(se) & se != 0 & is.finite(observed)
    expected <- estimate / se
    bad <- which(keep & stat_audit_relative_mismatch(observed, expected, stat_tolerance))
    if (length(bad) > 0L) {
      findings[[length(findings) + 1L]] <- stat_audit_finding(
        domain = "numeric_consistency",
        table_id = table_id,
        check_id = "statistic_recalculation",
        severity = "critical",
        row_index = bad[1L],
        column = stat_col,
        observed = observed[bad[1L]],
        expected = expected[bad[1L]],
        message = "Reported test statistic is inconsistent with estimate / standard error."
      )
    }
  }

  if (!is.na(p_col)) {
    p <- stat_audit_numeric(table[[p_col]])
    bad_range <- which(!is.na(p) & (p < 0 | p > 1))
    if (length(bad_range) > 0L) {
      findings[[length(findings) + 1L]] <- stat_audit_finding(
        domain = "numeric_consistency",
        table_id = table_id,
        check_id = "p_value_range",
        severity = "critical",
        row_index = bad_range[1L],
        column = p_col,
        observed = p[bad_range[1L]],
        expected = "0 <= p <= 1",
        message = "Reported p-value is outside [0, 1]."
      )
    }

    stat_can_be_t <- !has_adjusted_p && !is.na(stat_col) && !is.na(df_col) &&
      (stat_col %in% c("t", "t.value", "t_value") || (!is.na(estimate_col) && !is.na(se_col)))

    if (stat_can_be_t) {
      observed_stat <- stat_audit_numeric(table[[stat_col]])
      df <- stat_audit_numeric(table[[df_col]])
      expected_p <- 2 * stats::pt(abs(observed_stat), df = df, lower.tail = FALSE)
      keep <- is.finite(p) & is.finite(expected_p)
      bad <- which(keep & abs(p - expected_p) > p_tolerance)
      if (length(bad) > 0L) {
        findings[[length(findings) + 1L]] <- stat_audit_finding(
          domain = "numeric_consistency",
          table_id = table_id,
          check_id = "p_value_recalculation",
          severity = "critical",
          row_index = bad[1L],
          column = p_col,
          observed = p[bad[1L]],
          expected = expected_p[bad[1L]],
          message = "Reported two-sided t p-value is inconsistent with statistic and df."
        )
      }
    } else if (!has_adjusted_p && !is.na(stat_col) && identical(stat_col, "z")) {
      observed_stat <- stat_audit_numeric(table[[stat_col]])
      expected_p <- 2 * stats::pnorm(abs(observed_stat), lower.tail = FALSE)
      keep <- is.finite(p) & is.finite(expected_p)
      bad <- which(keep & abs(p - expected_p) > p_tolerance)
      if (length(bad) > 0L) {
        findings[[length(findings) + 1L]] <- stat_audit_finding(
          domain = "numeric_consistency",
          table_id = table_id,
          check_id = "p_value_recalculation",
          severity = "critical",
          row_index = bad[1L],
          column = p_col,
          observed = p[bad[1L]],
          expected = expected_p[bad[1L]],
          message = "Reported two-sided z p-value is inconsistent with statistic."
        )
      }
    }
  }

  if (!is.na(estimate_col) && !is.na(ci_low_col) && !is.na(ci_high_col)) {
    estimate <- stat_audit_numeric(table[[estimate_col]])
    ci_low <- stat_audit_numeric(table[[ci_low_col]])
    ci_high <- stat_audit_numeric(table[[ci_high_col]])
    keep <- is.finite(estimate) & is.finite(ci_low) & is.finite(ci_high)
    bad <- which(keep & (estimate < pmin(ci_low, ci_high) | estimate > pmax(ci_low, ci_high)))
    if (length(bad) > 0L) {
      findings[[length(findings) + 1L]] <- stat_audit_finding(
        domain = "numeric_consistency",
        table_id = table_id,
        check_id = "ci_contains_estimate",
        severity = "critical",
        row_index = bad[1L],
        column = paste(ci_low_col, ci_high_col, sep = ","),
        observed = estimate[bad[1L]],
        expected = sprintf("[%s, %s]", ci_low[bad[1L]], ci_high[bad[1L]]),
        message = "Point estimate is outside the reported confidence interval."
      )
    }
  }

  if (!is.na(p_col)) {
    p <- stat_audit_numeric(table[[p_col]])
    fdr_cols <- grep("^(p_fdr|q_value|p_adj|p_adjust)", names(table), value = TRUE)
    fdr_cols <- fdr_cols[!grepl("_fmt$", fdr_cols)]
    for (fdr_col in fdr_cols) {
      q <- stat_audit_numeric(table[[fdr_col]])
      expected_q <- rep(NA_real_, length(p))
      group_col <- if (grepl("h4", fdr_col) && "model_type" %in% names(table)) {
        "model_type"
      } else {
        NA_character_
      }
      groups <- if (is.na(group_col)) {
        list(seq_along(p))
      } else {
        split(seq_along(p), as.character(table[[group_col]]), drop = TRUE)
      }
      for (group_index in groups) {
        keep_p <- group_index[!is.na(p[group_index])]
        if (length(keep_p) > 0L) {
          expected_q[keep_p] <- stats::p.adjust(p[keep_p], method = "BH")
        }
      }
      keep <- is.finite(q) & is.finite(expected_q)
      bad <- which(keep & abs(q - expected_q) > p_tolerance)
      if (length(bad) > 0L) {
        findings[[length(findings) + 1L]] <- stat_audit_finding(
          domain = "numeric_consistency",
          table_id = table_id,
          check_id = "fdr_bh_recalculation",
          severity = "critical",
          row_index = bad[1L],
          column = fdr_col,
          observed = q[bad[1L]],
          expected = expected_q[bad[1L]],
          message = "Reported BH/FDR value is inconsistent with the table p-values."
        )
      }
    }
  }

  stat_audit_bind_findings(findings)
}

audit_result_tables <- function(result_tables) {
  if (is.null(result_tables) || length(result_tables) == 0L) {
    return(stat_audit_empty_findings())
  }
  if (is.null(names(result_tables))) {
    names(result_tables) <- paste0("table_", seq_along(result_tables))
  }
  findings <- lapply(names(result_tables), function(table_id) {
    audit_result_table_consistency(result_tables[[table_id]], table_id = table_id)
  })
  stat_audit_bind_findings(findings)
}

statistical_audit_tool_registry <- function() {
  tools <- data.frame(
    layer = c(
      "data_contract",
      "data_contract",
      "model_assumptions",
      "model_assumptions",
      "numeric_consistency",
      "numeric_consistency",
      "static_analysis",
      "reproducibility",
      "reproducibility"
    ),
    tool = c(
      "pointblank",
      "validate",
      "performance",
      "DHARMa",
      "statcheck",
      "scrutiny",
      "lintr",
      "targets",
      "renv"
    ),
    integration_status = c(
      "optional_package",
      "optional_package",
      "optional_package",
      "optional_package",
      "optional_package",
      "optional_package",
      "optional_package",
      "active_project_layer",
      "active_project_layer"
    ),
    stringsAsFactors = FALSE
  )
  tools$available <- vapply(tools$tool, requireNamespace, logical(1), quietly = TRUE)
  tools
}

summarize_statistical_audit <- function(findings) {
  if (is.null(findings) || !is.data.frame(findings)) {
    findings <- stat_audit_empty_findings()
  }
  critical <- sum(findings$severity == "critical", na.rm = TRUE)
  review <- sum(findings$severity == "review", na.rm = TRUE)
  data.frame(
    total_findings = nrow(findings),
    critical_findings = critical,
    review_findings = review,
    status = if (critical > 0L) "fail" else if (review > 0L) "review" else "pass",
    stringsAsFactors = FALSE
  )
}

assert_statistical_audit_ok <- function(findings, allow_review = TRUE) {
  if (is.null(findings) || !is.data.frame(findings)) {
    return(TRUE)
  }
  critical <- findings[findings$severity == "critical", , drop = FALSE]
  if (nrow(critical) > 0L) {
    stop(
      sprintf(
        "Statistical audit failed: %d critical finding(s); first=%s/%s/%s",
        nrow(critical),
        critical$table_id[[1L]],
        critical$check_id[[1L]],
        critical$message[[1L]]
      ),
      call. = FALSE
    )
  }
  if (!allow_review) {
    review <- findings[findings$severity == "review", , drop = FALSE]
    if (nrow(review) > 0L) {
      stop(sprintf("Statistical audit has %d review finding(s)", nrow(review)), call. = FALSE)
    }
  }
  TRUE
}

run_statistical_audit <- function(df_family, df_long, result_tables = list()) {
  findings <- stat_audit_bind_findings(
    audit_data_contract(df_family, df_long),
    attr(result_tables, "findings", exact = TRUE),
    audit_result_tables(result_tables)
  )
  list(
    findings = findings,
    summary = summarize_statistical_audit(findings),
    tool_registry = statistical_audit_tool_registry()
  )
}

collect_statistical_audit_csv_tables <- function(directory = "outputs/tables",
                                                 pattern = "\\.csv$",
                                                 max_files = Inf) {
  if (!dir.exists(directory)) {
    tables <- list()
    attr(tables, "findings") <- stat_audit_empty_findings()
    return(tables)
  }
  files <- list.files(directory, pattern = pattern, full.names = TRUE)
  files <- sort(files)
  if (is.finite(max_files)) {
    files <- files[seq_len(min(length(files), max_files))]
  }
  tables <- list()
  findings <- list()
  for (path in files) {
    table_id <- tools::file_path_sans_ext(basename(path))
    table <- try(
      utils::read.csv(path, check.names = FALSE, stringsAsFactors = FALSE),
      silent = TRUE
    )
    if (inherits(table, "try-error")) {
      findings[[length(findings) + 1L]] <- stat_audit_finding(
        domain = "csv_io",
        table_id = table_id,
        check_id = "csv_readable",
        severity = "review",
        observed = as.character(table),
        expected = "readable CSV",
        message = "CSV output could not be parsed and was skipped."
      )
      next
    }
    tables[[table_id]] <- table
  }
  attr(tables, "findings") <- stat_audit_bind_findings(findings)
  tables
}
