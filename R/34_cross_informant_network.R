# [KESIFSEL - POST-HOC] Faz II SAP KISIM XX/53
# Cross-Informant Gaussian Graphical Model (GGM)
#
# Anne (EMBU-P 4 alt olcek + Beck) + Indeks cocuk (EMBU-C 4 alt olcek + SRQ 3 alt
# olcek) duzeyinde tek bir ag uzerinden bilgi-veren-arasi kosullu bagimliliklari
# gorsellestirir. EBIC-LASSO regulariazasyonu (gamma=0.5), Spearman korelasyon.
#
# Skill referanslari: references/network-analizi.md
# Veri: df_family_ses + df_long_scored[Indeks]

xinfo_node_specs <- function() {
  data.frame(
    variable = c(
      "embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
      "embu_p_reddetme_mean", "embu_p_karsilastirma_mean",
      "embu_c_sicaklik_mean", "embu_c_asiri_koruma_mean",
      "embu_c_reddetme_mean", "embu_c_karsilastirma_mean",
      "beck_total",
      "srq_ho_warmth_mean", "srq_ho_status_mean", "srq_ho_conflict_mean"
    ),
    label = c(
      "P-Sicaklik", "P-AK", "P-Reddetme", "P-Karsilastirma",
      "C-Sicaklik", "C-AK", "C-Reddetme", "C-Karsilastirma",
      "Beck",
      "SRQ-Sicaklik", "SRQ-Status", "SRQ-Catisma"
    ),
    informant = c(
      rep("anne", 4),
      rep("cocuk_indeks", 4),
      "anne",
      rep("cocuk_indeks", 3)
    ),
    domain = c(
      rep("EMBU-P", 4), rep("EMBU-C", 4),
      "Beck",
      rep("SRQ", 3)
    ),
    stringsAsFactors = FALSE
  )
}

xinfo_require_columns <- function(df, columns, context) {
  missing_columns <- setdiff(columns, names(df))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf(
        "%s is missing required column(s): %s",
        context, paste(missing_columns, collapse = ", ")
      ),
      call. = FALSE
    )
  }
  invisible(TRUE)
}

xinfo_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

xinfo_prepare_data <- function(df_family_ses, df_long_scored) {
  specs <- xinfo_node_specs()
  family_vars <- specs$variable[specs$informant == "anne"]
  cocuk_vars <- specs$variable[specs$informant == "cocuk_indeks"]

  xinfo_require_columns(df_family_ses, c("aile_no", family_vars), "xinfo family data")
  xinfo_require_columns(df_long_scored, c("aile_no", "family_role_f", cocuk_vars), "xinfo long data")

  if (anyDuplicated(df_family_ses$aile_no) > 0L) {
    stop("xinfo family data must have one row per family", call. = FALSE)
  }

  long_side <- df_long_scored[, c("aile_no", "family_role_f", cocuk_vars), drop = FALSE]
  long_side$role_token <- xinfo_normalize_role(long_side$family_role_f)
  indeks_side <- long_side[!is.na(long_side$role_token) & long_side$role_token == "indeks", , drop = FALSE]
  if (anyDuplicated(indeks_side$aile_no) > 0L) {
    stop("xinfo long data has duplicated indeks rows per family", call. = FALSE)
  }

  paired <- merge(
    df_family_ses[, c("aile_no", family_vars), drop = FALSE],
    indeks_side[, c("aile_no", cocuk_vars), drop = FALSE],
    by = "aile_no",
    all.x = FALSE,
    all.y = FALSE
  )

  if ("group_f" %in% names(df_family_ses)) {
    paired$group_f <- df_family_ses$group_f[match(paired$aile_no, df_family_ses$aile_no)]
  } else if ("group_dm" %in% names(df_family_ses)) {
    paired$group_f <- factor(
      ifelse(df_family_ses$group_dm[match(paired$aile_no, df_family_ses$aile_no)] == 1L, "DM", "Kontrol"),
      levels = c("Kontrol", "DM")
    )
  }

  paired
}

xinfo_complete_subset <- function(paired_data, variables) {
  ok_rows <- stats::complete.cases(paired_data[, variables, drop = FALSE])
  paired_data[ok_rows, , drop = FALSE]
}

xinfo_coverage <- function(paired_data, variables, group_label = "all") {
  data.frame(
    group_label = group_label,
    n_rows = nrow(paired_data),
    n_complete = sum(stats::complete.cases(paired_data[, variables, drop = FALSE])),
    n_variables = length(variables),
    stringsAsFactors = FALSE
  )
}

xinfo_estimate_ggm <- function(data, variables, gamma = 0.5,
                               correlation = "spearman",
                               group_label = "all") {
  if (!requireNamespace("qgraph", quietly = TRUE)) {
    return(list(status = "qgraph_unavailable", group_label = group_label))
  }
  sub <- xinfo_complete_subset(data, variables)
  if (nrow(sub) < length(variables) + 5L) {
    return(list(status = "insufficient_n", n = nrow(sub), group_label = group_label))
  }
  cor_mat <- stats::cor(sub[, variables, drop = FALSE], method = correlation, use = "pairwise.complete.obs")
  if (any(!is.finite(cor_mat))) {
    return(list(status = "non_finite_correlation", group_label = group_label))
  }
  net <- suppressMessages(
    qgraph::EBICglasso(cor_mat, n = nrow(sub), gamma = gamma)
  )
  list(
    status = "ok",
    group_label = group_label,
    n = nrow(sub),
    correlation = cor_mat,
    network = net,
    gamma = gamma,
    correlation_method = correlation
  )
}

xinfo_edges_table <- function(ggm_result, node_specs = xinfo_node_specs()) {
  if (!is.list(ggm_result) || !identical(ggm_result$status, "ok")) {
    return(data.frame(
      from = character(0), to = character(0),
      from_informant = character(0), to_informant = character(0),
      cross_informant = logical(0),
      weight = numeric(0),
      sign = character(0),
      stringsAsFactors = FALSE
    ))
  }
  net <- ggm_result$network
  variables <- rownames(net)
  rows <- list()
  inf_lookup <- setNames(node_specs$informant, node_specs$variable)
  for (i in seq_len(nrow(net) - 1L)) {
    for (j in seq(i + 1L, nrow(net))) {
      w <- net[i, j]
      if (!is.na(w) && abs(w) > 1e-8) {
        from_inf <- inf_lookup[[variables[i]]]
        to_inf <- inf_lookup[[variables[j]]]
        rows[[length(rows) + 1L]] <- data.frame(
          group_label = ggm_result$group_label,
          from = variables[i],
          to = variables[j],
          from_informant = from_inf,
          to_informant = to_inf,
          cross_informant = !identical(from_inf, to_inf),
          weight = w,
          sign = if (w > 0) "positive" else "negative",
          stringsAsFactors = FALSE
        )
      }
    }
  }
  if (length(rows) == 0L) {
    return(data.frame(
      group_label = character(0),
      from = character(0), to = character(0),
      from_informant = character(0), to_informant = character(0),
      cross_informant = logical(0),
      weight = numeric(0), sign = character(0),
      stringsAsFactors = FALSE
    ))
  }
  do.call(rbind, rows)
}

xinfo_centrality_table <- function(ggm_result) {
  if (!is.list(ggm_result) || !identical(ggm_result$status, "ok")) {
    return(data.frame(
      group_label = character(0),
      variable = character(0),
      strength = numeric(0),
      expected_influence = numeric(0),
      betweenness = numeric(0),
      closeness = numeric(0),
      stringsAsFactors = FALSE
    ))
  }
  if (!requireNamespace("qgraph", quietly = TRUE)) {
    return(NULL)
  }
  cent <- qgraph::centrality(ggm_result$network)
  data.frame(
    group_label = ggm_result$group_label,
    variable = rownames(ggm_result$network),
    strength = unname(cent$InDegree),
    expected_influence = unname(cent$InExpectedInfluence),
    betweenness = unname(cent$Betweenness),
    closeness = unname(cent$Closeness),
    stringsAsFactors = FALSE
  )
}

xinfo_cross_informant_summary <- function(edges_table) {
  if (nrow(edges_table) == 0L) {
    return(data.frame(
      group_label = character(0),
      n_edges_total = integer(0),
      n_edges_cross_informant = integer(0),
      cross_informant_share = numeric(0),
      mean_weight_cross = numeric(0),
      mean_weight_within = numeric(0),
      stringsAsFactors = FALSE
    ))
  }
  groups <- unique(edges_table$group_label)
  rows <- lapply(groups, function(g) {
    sub <- edges_table[edges_table$group_label == g, , drop = FALSE]
    cross <- sub[sub$cross_informant, , drop = FALSE]
    within <- sub[!sub$cross_informant, , drop = FALSE]
    data.frame(
      group_label = g,
      n_edges_total = nrow(sub),
      n_edges_cross_informant = nrow(cross),
      cross_informant_share = if (nrow(sub) > 0L) nrow(cross) / nrow(sub) else NA_real_,
      mean_weight_cross = if (nrow(cross) > 0L) mean(abs(cross$weight)) else NA_real_,
      mean_weight_within = if (nrow(within) > 0L) mean(abs(within$weight)) else NA_real_,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

run_cross_informant_network_pipeline <- function(df_family_ses, df_long_scored,
                                                 gamma = 0.5,
                                                 correlation = "spearman",
                                                 group_split = TRUE) {
  specs <- xinfo_node_specs()
  paired <- xinfo_prepare_data(df_family_ses, df_long_scored)
  variables <- specs$variable

  group_results <- list()
  group_labels <- "all"
  if (group_split && "group_f" %in% names(paired)) {
    group_labels <- c("all", "Kontrol", "DM")
  }

  for (gl in group_labels) {
    if (gl == "all") {
      sub <- paired
    } else {
      sub <- paired[!is.na(paired$group_f) & paired$group_f == gl, , drop = FALSE]
    }
    group_results[[gl]] <- list(
      coverage = xinfo_coverage(sub, variables, group_label = gl),
      ggm = xinfo_estimate_ggm(sub, variables, gamma = gamma,
        correlation = correlation, group_label = gl
      )
    )
  }

  coverage_rows <- do.call(rbind, lapply(group_results, function(g) g$coverage))

  status_rows <- do.call(rbind, lapply(group_results, function(g) {
    data.frame(
      group_label = g$ggm$group_label %||% NA_character_,
      status = g$ggm$status,
      n = g$ggm$n %||% NA_integer_,
      gamma = g$ggm$gamma %||% NA_real_,
      correlation_method = g$ggm$correlation_method %||% NA_character_,
      stringsAsFactors = FALSE
    )
  }))

  edges_rows <- do.call(rbind, lapply(group_results, function(g) {
    if (identical(g$ggm$status, "ok")) xinfo_edges_table(g$ggm) else NULL
  }))

  centrality_rows <- do.call(rbind, lapply(group_results, function(g) {
    if (identical(g$ggm$status, "ok")) xinfo_centrality_table(g$ggm) else NULL
  }))

  summary_rows <- if (!is.null(edges_rows) && nrow(edges_rows) > 0L) {
    xinfo_cross_informant_summary(edges_rows)
  } else {
    NULL
  }

  list(
    nodes = specs,
    coverage = coverage_rows,
    status = status_rows,
    edges = edges_rows,
    centrality = centrality_rows,
    cross_informant_summary = summary_rows,
    target_summary = data.frame(
      analysis = "cross_informant_network_phase2",
      n_nodes = nrow(specs),
      gamma = gamma,
      correlation_method = correlation,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XX/53)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      stringsAsFactors = FALSE
    )
  )
}

# Yardimci: NULL coalesce (R 4.x'te varsayilan yok)
`%||%` <- function(a, b) if (is.null(a)) b else a
