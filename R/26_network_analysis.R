# KISIM VIII — Network Analizi
# 24. Gaussian Graphical Model (EBIC-LASSO)
# 25. Network Comparison Test (DM × Kontrol)
# 26. Beck symptom item-level network
#
# qgraph + bootnet + NetworkComparisonTest

network_parenting_outcomes <- function() {
  c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
    "embu_p_reddetme_mean", "embu_p_karsilastirma_mean",
    "srq_ho_warmth_mean",   "srq_ho_status_mean",
    "srq_ho_conflict_mean", "srq_ho_rivalry_mean",
    "beck_total")
}

run_ggm_lasso <- function(df, variables, gamma = 0.5, group_label = "all") {
  if (!requireNamespace("qgraph", quietly = TRUE)) {
    return(list(status = "qgraph_unavailable"))
  }
  sub <- df[, variables, drop = FALSE]
  sub <- sub[stats::complete.cases(sub), , drop = FALSE]
  if (nrow(sub) < 20L) {
    return(list(status = "insufficient_n", n = nrow(sub)))
  }
  cor_mat <- stats::cor(sub, method = "spearman", use = "pairwise.complete.obs")
  net <- tryCatch(
    suppressMessages(qgraph::EBICglasso(cor_mat, n = nrow(sub), gamma = gamma,
                                         returnAllResults = FALSE)),
    error = function(e) e
  )
  if (inherits(net, "error")) {
    return(list(status = paste0("error:", conditionMessage(net))))
  }
  edge_rows <- list()
  vnames <- variables
  for (i in seq_len(length(vnames) - 1L)) {
    for (j in (i + 1L):length(vnames)) {
      if (abs(net[i, j]) > 1e-6) {
        edge_rows[[length(edge_rows) + 1L]] <- data.frame(
          group = group_label,
          from = vnames[i], to = vnames[j],
          partial_cor = net[i, j], stringsAsFactors = FALSE
        )
      }
    }
  }
  edges_df <- if (length(edge_rows) > 0L) do.call(rbind, edge_rows) else data.frame()
  if (!requireNamespace("bootnet", quietly = TRUE) || nrow(edges_df) == 0L) {
    centrality_df <- data.frame()
  } else {
    centrality <- tryCatch(
      qgraph::centrality(net),
      error = function(e) NULL
    )
    centrality_df <- if (!is.null(centrality)) {
      data.frame(
        group = group_label,
        variable  = vnames,
        strength  = unname(centrality$InDegree),
        closeness = unname(centrality$Closeness),
        betweenness = unname(centrality$Betweenness),
        expected_influence = unname(centrality$InExpectedInfluence),
        stringsAsFactors = FALSE
      )
    } else data.frame()
  }
  list(
    status = "ok",
    n      = nrow(sub),
    edges_table = edges_df,
    centrality_table = centrality_df,
    adjacency = net
  )
}

run_nct <- function(df, variables, group_col = "group_f",
                     n_perm = 500L, seed = 20260428L) {
  if (!requireNamespace("NetworkComparisonTest", quietly = TRUE)) {
    return(list(status = "NCT_unavailable"))
  }
  sub_dm <- df[df[[group_col]] == "DM", variables, drop = FALSE]
  sub_ko <- df[df[[group_col]] == "Kontrol", variables, drop = FALSE]
  sub_dm <- sub_dm[stats::complete.cases(sub_dm), , drop = FALSE]
  sub_ko <- sub_ko[stats::complete.cases(sub_ko), , drop = FALSE]
  if (nrow(sub_dm) < 20L || nrow(sub_ko) < 20L) {
    return(list(status = "insufficient_n", n_dm = nrow(sub_dm), n_ko = nrow(sub_ko)))
  }
  set.seed(seed)
  nct <- tryCatch(
    suppressMessages(suppressWarnings(NetworkComparisonTest::NCT(
      data1 = as.matrix(sub_dm), data2 = as.matrix(sub_ko),
      it = n_perm, paired = FALSE, weighted = TRUE,
      test.edges = FALSE,
      test.centrality = TRUE,
      progressbar = FALSE
    ))),
    error = function(e) e
  )
  if (inherits(nct, "error")) {
    return(list(status = paste0("error:", conditionMessage(nct))))
  }
  list(
    status = "ok",
    n_dm   = nrow(sub_dm),
    n_ko   = nrow(sub_ko),
    M_glstrinv = nct$nwinv.real,
    M_glstrinv_pvalue = nct$nwinv.pval,
    glstrinv_real = nct$glstrinv.real,
    glstrinv_pvalue = nct$glstrinv.pval,
    permutations = n_perm
  )
}

run_beck_symptom_network <- function(df_family_scored, gamma = 0.5,
                                      group_label = "all") {
  beck_cols <- paste0("beck_", 1:21)
  if (!all(beck_cols %in% names(df_family_scored))) {
    return(list(status = "items_missing"))
  }
  sub <- df_family_scored[, beck_cols, drop = FALSE]
  sub <- sub[stats::complete.cases(sub), , drop = FALSE]
  if (nrow(sub) < 30L) return(list(status = "insufficient_n", n = nrow(sub)))
  cor_mat <- stats::cor(sub, method = "spearman", use = "pairwise.complete.obs")
  net <- tryCatch(
    suppressMessages(qgraph::EBICglasso(cor_mat, n = nrow(sub), gamma = gamma)),
    error = function(e) e
  )
  if (inherits(net, "error")) {
    return(list(status = paste0("error:", conditionMessage(net))))
  }
  centrality <- qgraph::centrality(net)
  centrality_df <- data.frame(
    group = group_label,
    item = beck_cols,
    strength = unname(centrality$InDegree),
    closeness = unname(centrality$Closeness),
    betweenness = unname(centrality$Betweenness),
    expected_influence = unname(centrality$InExpectedInfluence),
    stringsAsFactors = FALSE
  )
  list(
    status = "ok",
    n = nrow(sub),
    centrality_table = centrality_df
  )
}

run_network_pipeline <- function(df_family_ses, df_family_scored, seed = 20260428L) {
  prepared <- df_family_ses
  prepared$group_f <- factor(as.character(prepared$group_f), levels = c("Kontrol", "DM"))
  variables <- network_parenting_outcomes()
  available <- intersect(variables, names(prepared))

  ggm_all <- run_ggm_lasso(prepared, available, group_label = "all")
  ggm_dm  <- run_ggm_lasso(prepared[prepared$group_f == "DM", , drop = FALSE], available, group_label = "DM")
  ggm_ko  <- run_ggm_lasso(prepared[prepared$group_f == "Kontrol", , drop = FALSE], available, group_label = "Kontrol")
  nct     <- run_nct(prepared, available, n_perm = 200L, seed = seed)
  beck_net <- run_beck_symptom_network(df_family_scored, group_label = "all")

  edges <- do.call(rbind, list(
    if (!is.null(ggm_all$edges_table)) ggm_all$edges_table else data.frame(),
    if (!is.null(ggm_dm$edges_table)) ggm_dm$edges_table else data.frame(),
    if (!is.null(ggm_ko$edges_table)) ggm_ko$edges_table else data.frame()
  ))
  centrality <- do.call(rbind, list(
    if (!is.null(ggm_all$centrality_table)) ggm_all$centrality_table else data.frame(),
    if (!is.null(ggm_dm$centrality_table)) ggm_dm$centrality_table else data.frame(),
    if (!is.null(ggm_ko$centrality_table)) ggm_ko$centrality_table else data.frame()
  ))
  status_table <- data.frame(
    component = c("ggm_all", "ggm_dm", "ggm_ko", "nct", "beck_symptom"),
    status    = c(ggm_all$status, ggm_dm$status, ggm_ko$status, nct$status, beck_net$status),
    n         = c(if (!is.null(ggm_all$n)) ggm_all$n else NA_integer_,
                  if (!is.null(ggm_dm$n)) ggm_dm$n else NA_integer_,
                  if (!is.null(ggm_ko$n)) ggm_ko$n else NA_integer_,
                  if (!is.null(nct$n_dm)) nct$n_dm + nct$n_ko else NA_integer_,
                  if (!is.null(beck_net$n)) beck_net$n else NA_integer_),
    stringsAsFactors = FALSE
  )
  nct_table <- if (nct$status == "ok") {
    data.frame(
      n_dm = nct$n_dm, n_ko = nct$n_ko,
      M_invariance = nct$M_glstrinv,
      M_invariance_pvalue = nct$M_glstrinv_pvalue,
      global_strength_invariance = nct$glstrinv_real,
      global_strength_pvalue = nct$glstrinv_pvalue,
      permutations = nct$permutations,
      stringsAsFactors = FALSE
    )
  } else data.frame()
  list(
    status_table     = status_table,
    edges_table      = edges,
    centrality_table = centrality,
    nct_table        = nct_table,
    beck_centrality_table = if (!is.null(beck_net$centrality_table)) beck_net$centrality_table else data.frame()
  )
}
