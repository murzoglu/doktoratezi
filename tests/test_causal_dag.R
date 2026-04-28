source("R/14_causal_dag.R")

dag_results <- build_causal_dag()

stopifnot(inherits(dag_results$dag, "dagitty"))
stopifnot(nrow(dag_results$nodes) >= 10L)
stopifnot(nrow(dag_results$edges) >= 20L)

edge_keys <- paste(dag_results$edges$from, dag_results$edges$to, sep = "->")
stopifnot("SES->T1DM_status" %in% edge_keys)
stopifnot("T1DM_status->ChildPerception" %in% edge_keys)
stopifnot("Beck->ParentingStyle" %in% edge_keys)

adjustment_sets <- dag_results$adjustment_sets
stopifnot(nrow(adjustment_sets) >= 1L)
primary_set <- adjustment_sets$covariates[[1L]]
stopifnot(identical(primary_set, "AgeGap;FamilySize;SES"))
stopifnot(!grepl("Beck|Maternal_AD_use|ParentingStyle", primary_set))

strategy <- dag_results$covariate_strategy
total_effect <- strategy[strategy$estimand == "total_effect_primary", , drop = FALSE]
stopifnot(identical(total_effect$adjust_for, "SES;AgeGap;FamilySize"))
stopifnot(grepl("Maternal_AD_use", total_effect$do_not_adjust_for))

fixture <- data.frame(
  group = c("DM", "Kontrol"),
  ses_latent = c(0.2, -0.3),
  age_gap = c(2.5, 3.0),
  cocuk_sayisi = c(2, 3),
  anne_antidepresan = c(1, 0),
  beck_total = c(12, 5),
  embu_p_reddetme_mean = c(1.2, 1.0),
  embu_c_idx_reddetme_mean = c(1.1, 1.3),
  srq_ho_warmth_mean = c(4.2, 4.0)
)

validation <- validate_causal_dag_data_proxies(fixture)
stopifnot(all(validation$present[validation$observed]))

bad_fixture <- fixture[, setdiff(names(fixture), "ses_latent")]
bad_validation <- validate_causal_dag_data_proxies(bad_fixture)
stopifnot(!bad_validation$present[bad_validation$node == "SES"])

summary <- summarize_causal_dag_targets(dag_results, validation)
stopifnot(identical(summary$n_adjustment_sets, nrow(adjustment_sets)))
stopifnot(summary$observed_proxy_missing_n == 0L)

plot <- plot_causal_dag(dag_results)
stopifnot(inherits(plot, "ggplot"))
