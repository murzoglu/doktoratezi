source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/14_causal_dag.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data

dag_results <- build_causal_dag()
proxy_validation <- validate_causal_dag_data_proxies(df_family_ses)
target_summary <- summarize_causal_dag_targets(dag_results, proxy_validation)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)

utils::write.csv(
  dag_results$nodes,
  "outputs/tables/causal_dag_nodes.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  dag_results$edges,
  "outputs/tables/causal_dag_edges.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  dag_results$adjustment_sets,
  "outputs/tables/causal_dag_adjustment_sets.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  dag_results$conditional_independencies,
  "outputs/tables/causal_dag_conditional_independencies.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  dag_results$covariate_strategy,
  "outputs/tables/causal_dag_covariate_strategy.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  dag_results$variable_mapping,
  "outputs/tables/causal_dag_variable_mapping.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  proxy_validation,
  "outputs/tables/causal_dag_proxy_validation.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  target_summary,
  "outputs/tables/causal_dag_target_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

writeLines(
  dag_results$dag_string,
  "outputs/tables/causal_dag_model.txt",
  useBytes = TRUE
)

plot <- plot_causal_dag(dag_results)
ggplot2::ggsave(
  "outputs/figures/causal_dag.png",
  plot = plot,
  width = 12,
  height = 6,
  dpi = 300
)

cat(sprintf(
  "Causal DAG audit passed: %d node(s), %d edge(s), primary adjustment={%s}, missing proxy=%d\n",
  target_summary$n_nodes,
  target_summary$n_edges,
  target_summary$primary_adjustment_set,
  target_summary$observed_proxy_missing_n
))
