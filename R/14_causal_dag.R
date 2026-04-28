causal_dag_nodes <- function() {
  data.frame(
    node = c(
      "GeneticLiability",
      "SES",
      "AgeGap",
      "FamilySize",
      "T1DM_status",
      "Maternal_AD_use",
      "Beck",
      "ParentingStyle",
      "ChildPerception",
      "SiblingRelations"
    ),
    label = c(
      "Genetik yatkinlik",
      "SES",
      "Kardes yas farki",
      "Aile buyuklugu",
      "T1DM durumu",
      "Anne antidepresan",
      "Beck depresyon",
      "Ebeveynlik tutumu",
      "Cocuk algisi",
      "Kardes iliskisi"
    ),
    role = c(
      "unobserved_exposure_cause",
      "confounder",
      "confounder",
      "confounder",
      "exposure",
      "mediator_or_sensitivity",
      "mediator",
      "mediator",
      "outcome",
      "downstream_outcome"
    ),
    observed = c(FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),
    primary_proxy = c(
      NA_character_,
      "ses_latent",
      "age_gap",
      "cocuk_sayisi",
      "group",
      "anne_antidepresan",
      "beck_total",
      "embu_p_*_mean",
      "embu_c_*_mean",
      "srq_ho_*_mean"
    ),
    x = c(0, 0, 0, 0, 2, 4, 5, 6, 8, 10),
    y = c(4, 3, 2, 1, 2.5, 4, 3, 2, 2.5, 2.5),
    stringsAsFactors = FALSE
  )
}

causal_dag_edges <- function() {
  data.frame(
    from = c(
      "GeneticLiability",
      "SES", "SES", "SES", "SES",
      "AgeGap", "AgeGap", "AgeGap",
      "FamilySize", "FamilySize", "FamilySize",
      "T1DM_status", "T1DM_status", "T1DM_status", "T1DM_status",
      "Maternal_AD_use", "Maternal_AD_use",
      "Beck", "Beck",
      "ParentingStyle",
      "ChildPerception"
    ),
    to = c(
      "T1DM_status",
      "T1DM_status", "Beck", "ParentingStyle", "ChildPerception",
      "T1DM_status", "ChildPerception", "SiblingRelations",
      "T1DM_status", "ParentingStyle", "ChildPerception",
      "Maternal_AD_use", "Beck", "ParentingStyle", "ChildPerception",
      "Beck", "ParentingStyle",
      "ParentingStyle", "ChildPerception",
      "ChildPerception",
      "SiblingRelations"
    ),
    edge_role = c(
      "exposure_background",
      rep("backdoor_or_selection", 10L),
      rep("exposure_to_mediator_or_outcome", 4L),
      rep("mediator_path", 5L),
      "downstream_path"
    ),
    stringsAsFactors = FALSE
  )
}

causal_dag_edge_statement <- function(edges) {
  paste(sprintf("  %s -> %s", edges$from, edges$to), collapse = "\n")
}

causal_dag_string <- function(nodes = causal_dag_nodes(), edges = causal_dag_edges()) {
  unobserved_nodes <- nodes$node[!nodes$observed]
  unobserved_lines <- if (length(unobserved_nodes) > 0L) {
    paste(sprintf("  %s [unobserved]", unobserved_nodes), collapse = "\n")
  } else {
    ""
  }

  paste0(
    "dag {\n",
    unobserved_lines,
    if (nzchar(unobserved_lines)) "\n" else "",
    causal_dag_edge_statement(edges),
    "\n  T1DM_status [exposure]\n",
    "  ChildPerception [outcome]\n",
    "}"
  )
}

make_causal_dag <- function(dag_string = causal_dag_string()) {
  if (!requireNamespace("dagitty", quietly = TRUE)) {
    stop("Required package is not installed: dagitty", call. = FALSE)
  }
  dagitty::dagitty(dag_string)
}

causal_dag_adjustment_sets <- function(dag, exposure = "T1DM_status",
                                       outcome = "ChildPerception") {
  sets <- dagitty::adjustmentSets(dag, exposure = exposure, outcome = outcome, type = "minimal")
  if (length(sets) == 0L) {
    return(data.frame(
      set_id = integer(),
      estimand = character(),
      covariates = character(),
      n_covariates = integer(),
      stringsAsFactors = FALSE
    ))
  }

  rows <- lapply(seq_along(sets), function(i) {
    covariates <- sort(as.character(sets[[i]]))
    data.frame(
      set_id = i,
      estimand = "total_effect_primary",
      covariates = paste(covariates, collapse = ";"),
      n_covariates = length(covariates),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

causal_dag_conditional_independencies <- function(dag) {
  statements <- capture.output(print(dagitty::impliedConditionalIndependencies(dag)))
  if (length(statements) == 0L) {
    statements <- character()
  }
  data.frame(
    statement_id = seq_along(statements),
    statement = statements,
    stringsAsFactors = FALSE
  )
}

causal_dag_covariate_strategy <- function() {
  data.frame(
    estimand = c(
      "total_effect_primary",
      "direct_effect_sensitivity",
      "mediation",
      "moderated_mediation"
    ),
    adjust_for = c(
      "SES;AgeGap;FamilySize",
      "SES;AgeGap;FamilySize;Maternal_AD_use;Beck",
      "SES;AgeGap;FamilySize",
      "SES;AgeGap;FamilySize"
    ),
    do_not_adjust_for = c(
      "Maternal_AD_use;Beck;ParentingStyle",
      "ParentingStyle",
      "ParentingStyle_on_path",
      "ParentingStyle_on_path"
    ),
    model_role = c(
      "Birincil total-effect modelleri",
      "Aracilik yollarini kapatan duyarlilik analizi",
      "Beck/AD/ParentingStyle aracilik modeli",
      "Group/AgeCat etkilesimli aracilik modeli"
    ),
    repo_proxy = c(
      "ses_latent + age_gap + cocuk_sayisi",
      "ses_latent + age_gap + cocuk_sayisi + anne_antidepresan + beck_total",
      "ses_latent + age_gap + cocuk_sayisi; mediator kolonlari model-spesifik",
      "ses_latent + age_gap + cocuk_sayisi; moderator kolonlari model-spesifik"
    ),
    stringsAsFactors = FALSE
  )
}

causal_dag_variable_mapping <- function() {
  data.frame(
    node = c(
      "T1DM_status",
      "SES",
      "AgeGap",
      "FamilySize",
      "Maternal_AD_use",
      "Beck",
      "ParentingStyle",
      "ChildPerception",
      "SiblingRelations"
    ),
    primary_columns = c(
      "group;group_f",
      "ses_latent",
      "age_gap",
      "cocuk_sayisi",
      "anne_antidepresan",
      "beck_total;beck_severity",
      "embu_p_sicaklik_mean;embu_p_asiri_koruma_mean;embu_p_reddetme_mean;embu_p_karsilastirma_mean",
      "embu_c_idx_*_mean;embu_c_sib_*_mean",
      "srq_ho_*_mean;srq_sib_ho_*_mean"
    ),
    sensitivity_columns = c(
      NA_character_,
      "aile_isei08;mean_aile_egitim;material_index",
      NA_character_,
      NA_character_,
      "stratified sensitivity",
      "beck_clinical",
      "role-specific EMBU-P/EMBU-C subscales",
      "child role and sibling role separated",
      "SRQ first-order scores"
    ),
    stringsAsFactors = FALSE
  )
}

causal_dag_proxy_requirements <- function() {
  list(
    T1DM_status = c("group"),
    SES = c("ses_latent"),
    AgeGap = c("age_gap"),
    FamilySize = c("cocuk_sayisi"),
    Maternal_AD_use = c("anne_antidepresan"),
    Beck = c("beck_total"),
    ParentingStyle = c("embu_p_reddetme_mean"),
    ChildPerception = c("embu_c_idx_reddetme_mean"),
    SiblingRelations = c("srq_ho_warmth_mean")
  )
}

validate_causal_dag_data_proxies <- function(df, requirements = causal_dag_proxy_requirements()) {
  nodes <- causal_dag_nodes()
  rows <- lapply(nodes$node, function(node) {
    required <- requirements[[node]]
    if (is.null(required)) {
      required <- character()
    }
    missing_columns <- setdiff(required, names(df))
    observed <- nodes$observed[nodes$node == node]
    data.frame(
      node = node,
      observed = observed,
      required_columns = paste(required, collapse = ";"),
      present = if (!observed) TRUE else length(missing_columns) == 0L,
      missing_columns = paste(missing_columns, collapse = ";"),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

plot_causal_dag <- function(dag_results = build_causal_dag()) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("Required package is not installed: ggplot2", call. = FALSE)
  }
  nodes <- dag_results$nodes
  edges <- dag_results$edges
  edge_plot <- merge(edges, nodes[, c("node", "x", "y")], by.x = "from", by.y = "node", all.x = TRUE)
  edge_plot <- merge(
    edge_plot,
    nodes[, c("node", "x", "y")],
    by.x = "to",
    by.y = "node",
    all.x = TRUE,
    suffixes = c("_from", "_to")
  )

  ggplot2::ggplot() +
    ggplot2::geom_segment(
      data = edge_plot,
      ggplot2::aes(x = x_from, y = y_from, xend = x_to, yend = y_to),
      arrow = ggplot2::arrow(length = grid::unit(0.16, "inches")),
      linewidth = 0.45,
      color = "#59616f"
    ) +
    ggplot2::geom_point(
      data = nodes,
      ggplot2::aes(x = x, y = y, fill = role, shape = observed),
      size = 5,
      color = "#263238"
    ) +
    ggplot2::geom_text(
      data = nodes,
      ggplot2::aes(x = x, y = y + 0.23, label = label),
      size = 3.2,
      color = "#111827"
    ) +
    ggplot2::scale_shape_manual(values = c(`TRUE` = 21, `FALSE` = 24)) +
    ggplot2::scale_fill_manual(values = c(
      confounder = "#80cbc4",
      downstream_outcome = "#b39ddb",
      exposure = "#ffcc80",
      mediator = "#90caf9",
      mediator_or_sensitivity = "#f48fb1",
      outcome = "#c5e1a5",
      unobserved_exposure_cause = "#e0e0e0"
    )) +
    ggplot2::coord_equal(xlim = c(-0.7, 10.8), ylim = c(0.5, 4.6), expand = FALSE) +
    ggplot2::labs(
      title = "T1DM-EBEVEYN Causal DAG",
      subtitle = "Primary total-effect adjustment: SES + AgeGap + FamilySize",
      x = NULL,
      y = NULL,
      fill = "Rol",
      shape = "Gozlenen"
    ) +
    ggplot2::theme_minimal(base_size = 11) +
    ggplot2::theme(
      panel.grid = ggplot2::element_blank(),
      axis.text = ggplot2::element_blank(),
      legend.position = "bottom"
    )
}

build_causal_dag <- function() {
  nodes <- causal_dag_nodes()
  edges <- causal_dag_edges()
  dag_string <- causal_dag_string(nodes, edges)
  dag <- make_causal_dag(dag_string)
  adjustment_sets <- causal_dag_adjustment_sets(dag)

  list(
    dag = dag,
    dag_string = dag_string,
    nodes = nodes,
    edges = edges,
    adjustment_sets = adjustment_sets,
    conditional_independencies = causal_dag_conditional_independencies(dag),
    covariate_strategy = causal_dag_covariate_strategy(),
    variable_mapping = causal_dag_variable_mapping()
  )
}

summarize_causal_dag_targets <- function(dag_results, validation) {
  data.frame(
    dag_version = "analysis_dag_v1",
    n_nodes = nrow(dag_results$nodes),
    n_edges = nrow(dag_results$edges),
    n_adjustment_sets = nrow(dag_results$adjustment_sets),
    primary_adjustment_set = if (nrow(dag_results$adjustment_sets) > 0L) dag_results$adjustment_sets$covariates[[1L]] else NA_character_,
    observed_proxy_missing_n = sum(!validation$present[validation$observed]),
    stringsAsFactors = FALSE
  )
}
