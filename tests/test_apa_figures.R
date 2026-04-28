source("R/25_clinical_utility.R")
source("R/28_apa_figures.R")

set.seed(20260428)

outcomes <- c(
  "embu_c_sicaklik_mean",
  "embu_c_asiri_koruma_mean",
  "embu_c_reddetme_mean",
  "embu_c_karsilastirma_mean"
)
terms <- c("role_fKontrol_Kardes", "role_fDM_Hasta_Indeks", "role_fDM_Hasta_Kardes")

h1_rows <- expand.grid(outcome = outcomes, term = terms, stringsAsFactors = FALSE)
h1_rows$model_type <- "primary_multilevel_ancova"
h1_rows$estimate <- stats::rnorm(nrow(h1_rows), 0, 0.15)
h1_rows$std_error <- 0.05
h1_rows$df <- 220
h1_rows$statistic <- h1_rows$estimate / h1_rows$std_error
h1_rows$p_value <- 0.2
h1_rows$ci_low <- h1_rows$estimate - 1.96 * h1_rows$std_error
h1_rows$ci_high <- h1_rows$estimate + 1.96 * h1_rows$std_error

h4 <- data.frame(
  model_type = "latent_sem_wlsmv",
  lhs = c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma"),
  op = "~",
  rhs = "beck_dep",
  label = c("b_sicaklik", "b_asiri_koruma", "b_reddetme", "b_karsilastirma"),
  group = NA_integer_,
  est = c(-0.30, 0.09, 0.36, 0.31),
  se = c(0.07, 0.07, 0.08, 0.09),
  z = c(-4, 1.2, 4.2, 3.5),
  pvalue = c(0.001, 0.2, 0.001, 0.001),
  ci.lower = c(-0.45, -0.05, 0.19, 0.14),
  ci.upper = c(-0.15, 0.24, 0.53, 0.49),
  std.all = c(-0.28, 0.08, 0.33, 0.28),
  p_fdr_across_h4 = c(0.001, 0.2, 0.001, 0.001),
  stringsAsFactors = FALSE
)

n <- 60L
family <- data.frame(
  aile_no = seq_len(n),
  group_f = rep(c("Kontrol", "DM"), each = n / 2L),
  stringsAsFactors = FALSE
)
for (subscale in apa_h5_subscales()) {
  family[[paste0("embu_p_", subscale, "_mean")]] <- runif(n, 1, 4)
  family[[paste0("embu_c_idx_", subscale, "_mean")]] <- runif(n, 1, 4)
  family[[paste0("embu_c_sib_", subscale, "_mean")]] <- runif(n, 1, 4)
}

params <- expand.grid(
  subscale = c("sicaklik", "reddetme"),
  group = c("Pooled", "Kontrol", "DM"),
  param = c("Z~1", "Z~X", "Z~Y", "Z~X2", "Z~X_Y", "Z~Y2"),
  stringsAsFactors = FALSE
)
params$label <- c("b0", "b1", "b2", "b3", "b4", "b5")[match(params$param, c("Z~1", "Z~X", "Z~Y", "Z~X2", "Z~X_Y", "Z~Y2"))]
params$est <- c("Z~1" = 10, "Z~X" = 1, "Z~Y" = -0.5, "Z~X2" = 0.1, "Z~X_Y" = 0.05, "Z~Y2" = -0.1)[params$param]
params$se <- 0.1
params$z <- 1
params$pvalue <- 0.5
params$ci.lower <- params$est - 0.2
params$ci.upper <- params$est + 0.2

p1 <- apa_plot_h1_forest(h1_rows)
p2 <- apa_plot_h4_sem_path(h4)
p3 <- apa_plot_h5_bland_altman(family)
p4 <- apa_plot_h5_rsa_surface(params, family)

h2_outcomes <- c("srq_ho_warmth_mean", "srq_ho_status_mean", "srq_ho_conflict_mean", "srq_ho_rivalry_mean")
h2_terms <- c("group_fDM", "family_role_fsibling", "age_gap_z", "group_fDM:family_role_fsibling")
h2 <- expand.grid(outcome = h2_outcomes, term = h2_terms, stringsAsFactors = FALSE)
h2$estimate <- stats::rnorm(nrow(h2), 0, 0.08)
h2$std_error <- 0.04
h2$df <- 220
h2$statistic <- h2$estimate / h2$std_error
h2$p_value <- 0.2
h2$ci_low <- h2$estimate - 1.96 * h2$std_error
h2$ci_high <- h2$estimate + 1.96 * h2$std_error
h2$p_fdr_across_h2 <- 0.4

h3 <- expand.grid(
  outcome = c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean", "embu_p_reddetme_mean", "embu_p_karsilastirma_mean"),
  stratum = c("all_adjusted_for_antidepressant", "no_antidepressant", "antidepressant_only"),
  stringsAsFactors = FALSE
)
h3$model_type <- "antidepressant_stratified_sensitivity"
h3$term <- "group_fDM"
h3$n <- 120
h3$n_dm <- 60
h3$n_control <- 60
h3$estimate <- stats::rnorm(nrow(h3), 0, 0.12)
h3$std_error <- 0.08
h3$df <- 100
h3$statistic <- h3$estimate / h3$std_error
h3$p_value <- 0.3
h3$ci_low <- h3$estimate - 1.96 * h3$std_error
h3$ci_high <- h3$estimate + 1.96 * h3$std_error
h3$std_beta <- h3$estimate
h3$std_beta_ci_low <- h3$ci_low
h3$std_beta_ci_high <- h3$ci_high
h3$covariance <- "model_based"
h3$weight_column <- NA_character_
h3$status <- "fitted"
h3$skip_reason <- NA_character_
h3$p_fdr_across_h3_stratified <- 0.5

multiverse <- expand.grid(
  outcome = c("embu_p_sicaklik_mean", "embu_p_reddetme_mean"),
  controls = c("minimal", "plus_ses"),
  model = c("ols", "robust"),
  subset = c("all", "no_antidep"),
  stringsAsFactors = FALSE
)
multiverse$n <- 180
multiverse$estimate <- stats::rnorm(nrow(multiverse), 0, 0.08)
multiverse$se <- 0.05
multiverse$statistic <- multiverse$estimate / multiverse$se
multiverse$p_value <- 0.25
multiverse$cohens_d <- multiverse$estimate / 0.5
multiverse$status <- "ok"

sense <- data.frame(
  outcome = c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean", "embu_p_reddetme_mean", "embu_p_karsilastirma_mean"),
  status = "ok",
  n = 180,
  estimate = c(0.06, 0.04, -0.05, 0.03),
  t_value = c(1.0, 0.8, -1.1, 0.7),
  p_value = 0.3,
  cohens_d = c(0.12, 0.08, -0.14, 0.06),
  RV_q = c(0.06, 0.04, 0.08, 0.05),
  RV_qa = 0,
  partial_r2_treatment = c(0.004, 0.003, 0.006, 0.002),
  evalue_point = c(1.5, 1.4, 1.6, 1.35),
  evalue_ci = c(1.4, 1.3, 1.5, 1.25),
  stringsAsFactors = FALSE
)

clinical <- family
clinical$anne_yas <- stats::rnorm(n, 38, 5)
clinical$ses_latent <- stats::rnorm(n)
clinical$cocuk_sayisi <- sample(1:4, n, replace = TRUE)
clinical$beck_total <- rpois(n, lambda = 11) + ifelse(clinical$group_f == "DM", 4, 0)
clinical$embu_p_sicaklik_mean <- runif(n, 1, 4)
clinical$embu_p_asiri_koruma_mean <- runif(n, 1, 4)
clinical$embu_p_reddetme_mean <- runif(n, 1, 4)
clinical$embu_p_karsilastirma_mean <- runif(n, 1, 4)
clinical_base_perf <- data.frame(n = n, n_events = sum(clinical$beck_total >= 17), auc = 0.58, auc_ci_lo = 0.50, auc_ci_hi = 0.67, auc_corrected = 0.59)
clinical_full_perf <- data.frame(n = n, n_events = sum(clinical$beck_total >= 17), auc = 0.70, auc_ci_lo = 0.62, auc_ci_hi = 0.78, auc_corrected = 0.71)
clinical_dca <- data.frame(threshold = seq(0.05, 0.5, by = 0.05), net_benefit = seq(0.20, 0.02, length.out = 10), sNB = NA_real_, cost_benefit = NA_character_, prob_high_risk = NA_real_)
clinical_calibration <- data.frame(decile = 1:5, n = rep(12, 5), mean_predicted = seq(0.1, 0.5, length.out = 5), mean_observed = c(0.08, 0.20, 0.25, 0.42, 0.55))

table1_groups <- data.frame(group = c("DM", "Kontrol"), n = c(30, 30), stringsAsFactors = FALSE)
nodes <- data.frame(
  node = c("SES", "AgeGap", "FamilySize", "T1DM_status", "Beck", "ParentingStyle", "ChildPerception"),
  label = c("SES", "Yaş farkı", "Aile büyüklüğü", "T1DM", "Beck", "Ebeveynlik", "Çocuk algısı"),
  role = c("confounder", "confounder", "confounder", "exposure", "mediator", "mediator", "outcome"),
  observed = TRUE,
  primary_proxy = NA_character_,
  x = c(0, 0, 0, 2, 4, 5, 7),
  y = c(3, 2, 1, 2, 3, 2, 2),
  stringsAsFactors = FALSE
)
edges <- data.frame(
  from = c("SES", "AgeGap", "FamilySize", "T1DM_status", "Beck", "ParentingStyle"),
  to = c("T1DM_status", "T1DM_status", "T1DM_status", "Beck", "ParentingStyle", "ChildPerception"),
  edge_role = c("backdoor_or_selection", "backdoor_or_selection", "backdoor_or_selection", "total_effect_path", "total_effect_path", "downstream_path"),
  stringsAsFactors = FALSE
)
balance <- data.frame(
  variable = c("age_gap", "ses_latent", "cocuk_sayisi"),
  variable_type = "continuous",
  smd_before = c(0.22, -0.03, 0.00),
  abs_smd_before = c(0.22, 0.03, 0.00),
  balance_flag_before = c("dengesiz", "iyi_denge", "iyi_denge"),
  smd_iptw = c(0.003, -0.004, 0.001),
  abs_smd_iptw = c(0.003, 0.004, 0.001),
  balance_flag_iptw = "iyi_denge",
  recommendation = "primary_adjustment_ok",
  smd_matched = c(-0.08, 0.01, 0.01),
  abs_smd_matched = c(0.08, 0.01, 0.01),
  balance_flag_matched = "iyi_denge",
  abs_smd_change_iptw = c(0.21, 0.02, 0.00),
  abs_smd_change_matched = c(0.14, 0.02, 0.01),
  stringsAsFactors = FALSE
)
propensity <- clinical
propensity$ps_value <- ifelse(propensity$group_f == "DM", runif(n, 0.42, 0.68), runif(n, 0.36, 0.62))
propensity_overlap <- data.frame(
  treated_min = 0.42,
  treated_max = 0.68,
  control_min = 0.36,
  control_max = 0.62,
  common_support_low = 0.42,
  common_support_high = 0.62,
  outside_common_support_n = 4
)
ses_corr <- expand.grid(
  variable_1 = c("mean_aile_egitim", "aile_isei08", "material_index", "ses_composite_eq", "ses_hollingshead", "ses_latent"),
  variable_2 = c("mean_aile_egitim", "aile_isei08", "material_index", "ses_composite_eq", "ses_hollingshead", "ses_latent"),
  stringsAsFactors = FALSE
)
ses_corr$r <- ifelse(ses_corr$variable_1 == ses_corr$variable_2, 1, runif(nrow(ses_corr), 0.2, 0.9))
h1_emm <- expand.grid(
  outcome = outcomes,
  age_year = c(8, 12, 16),
  role_f = c("Kontrol_Indeks", "Kontrol_Kardes", "DM_Hasta_Indeks", "DM_Hasta_Kardes"),
  cinsiyet_f = c("Kiz", "Erkek"),
  stringsAsFactors = FALSE
)
h1_emm$cocuk_yas_z <- scale(h1_emm$age_year)[, 1]
h1_emm$emmean <- runif(nrow(h1_emm), 2.5, 3.4)
h1_emm$SE <- 0.08
h1_emm$df <- 420
h1_emm$lower.CL <- h1_emm$emmean - 0.16
h1_emm$upper.CL <- h1_emm$emmean + 0.16

med_simple <- data.frame(
  parameter = c("a", "b", "cprime", "indirect"),
  operator = c("~", "~", "~", ":="),
  estimate = c(0.006, 0.09, 0.14, 0.0005),
  se = c(0.002, 0.06, 0.04, 0.0004),
  z_value = c(2.3, 1.4, 3.5, 1.0),
  p_value = c(0.02, 0.16, 0.001, 0.30),
  ci_lo = c(0.001, -0.03, 0.06, -0.0001),
  ci_hi = c(0.010, 0.21, 0.22, 0.002),
  stringsAsFactors = FALSE
)
med_multi <- med_simple
med_cond <- data.frame(
  parameter = c("a1", "a3", "b", "cprime", "cond_indirect_kontrol", "cond_indirect_dm", "index_mod_mediation"),
  operator = c("~", "~", "~", "~", ":=", ":=", ":="),
  estimate = c(0.02, 0.04, 0.09, 0.14, 0.002, 0.006, 0.004),
  se = c(0.03, 0.04, 0.06, 0.04, 0.003, 0.005, 0.004),
  z_value = 1,
  p_value = c(0.49, 0.22, 0.16, 0.001, 0.64, 0.22, 0.37),
  ci_lo = c(-0.03, -0.03, -0.03, 0.06, -0.002, -0.002, -0.002),
  ci_hi = c(0.08, 0.12, 0.21, 0.22, 0.016, 0.019, 0.019),
  stringsAsFactors = FALSE
)
lpa_fit <- data.frame(
  Classes = 1:5,
  BIC = c(4112, 3975, 3951, 3976, 3972),
  Entropy = c(1, 0.93, 0.81, 0.73, 0.77),
  BLRT_p = c(NA, 0.01, 0.01, 0.25, 0.01)
)
net_edges <- data.frame(
  group = "all",
  from = c("embu_p_sicaklik_mean", "embu_p_reddetme_mean", "srq_ho_warmth_mean"),
  to = c("beck_total", "embu_p_karsilastirma_mean", "srq_ho_conflict_mean"),
  partial_cor = c(-0.08, 0.25, 0.24),
  stringsAsFactors = FALSE
)
net_cent <- data.frame(
  group = "all",
  variable = unique(c(net_edges$from, net_edges$to)),
  strength = runif(length(unique(c(net_edges$from, net_edges$to))), 0.1, 0.6),
  closeness = 0,
  betweenness = 0,
  expected_influence = runif(length(unique(c(net_edges$from, net_edges$to))), -0.2, 0.6),
  stringsAsFactors = FALSE
)
nct <- data.frame(n_dm = 60, n_ko = 60, M_invariance = 0.2, M_invariance_pvalue = 0.77, global_strength_invariance = 0.28, global_strength_pvalue = 0.86, permutations = 200)
cart_cp <- data.frame(n_splits = c(0, 2, 4), cp = c(0.04, 0.02, 0.005), rel_error = c(1, 0.8, 0.6), xerror = c(1.0, 1.2, 1.3), xstd = c(0.1, 0.11, 0.12))
rf_imp <- data.frame(variable = c("group_dm", "anne_yas_z", "embu_p_sicaklik_mean"), mean_decrease_accuracy = c(3, 1, 6), mean_decrease_gini = c(3, 16, 15))
bayes_h1 <- data.frame(outcome = c("embu_c_sicaklik_mean", "embu_c_reddetme_mean"), status = "ok", estimate = c(0.08, 0.16), sd = c(0.07, 0.05), ci_lo = c(-0.05, 0.05), ci_hi = c(0.22, 0.26), pd = c(0.90, 0.999), rope_pct = c(0.55, 0.13), bf10 = c(0.29, 8.12), bf_class = c("Moderate H0", "Moderate H1"))
bayes_h3 <- data.frame(outcome = c("embu_p_sicaklik_mean", "embu_p_reddetme_mean"), status = "ok", estimate = c(0.06, -0.05), sd = c(0.07, 0.04), ci_lo = c(-0.06, -0.12), ci_hi = c(0.19, 0.03), pd = c(0.83, 0.90), rope_pct = c(0.68, 0.92), bf10 = c(0.22, 0.17), bf_class = c("Moderate H0", "Moderate H0"))
bayes_d1 <- data.frame(outcome = bayes_h1$outcome, status = "ok", max_rhat = c(1.01, 1.012), min_ess_ratio = c(0.14, 0.13), n_divergent = 0)
bayes_d3 <- data.frame(outcome = bayes_h3$outcome, status = "ok", max_rhat = c(1.006, 1.004), min_ess_ratio = c(0.39, 0.37), n_divergent = 0)

p5 <- apa_plot_h2_apim_path(h2)
p6 <- apa_plot_h3_stratified_forest(h3)
p7 <- apa_plot_specification_curve(multiverse)
p8 <- apa_plot_sensemakr_contour(sense)
p9 <- apa_plot_clinical_roc(clinical, clinical_base_perf, clinical_full_perf)
p10 <- apa_plot_clinical_dca(clinical_dca, clinical_full_perf)
p11 <- apa_plot_clinical_calibration(clinical_calibration)
p12 <- apa_plot_study_flow(clinical, table1_groups)
p13 <- apa_plot_causal_dag(nodes, edges)
p14 <- apa_plot_smd_love(balance)
p15 <- apa_plot_propensity_overlap(propensity, propensity_overlap)
p16 <- apa_plot_ses_correlation(ses_corr)
p17 <- apa_plot_h1_three_way_emm(h1_emm)
p18 <- apa_plot_mediation_effects(med_simple, med_multi, med_cond)
p19 <- apa_plot_lpa_fit(lpa_fit)
p20 <- apa_plot_network_graph(net_edges, net_cent)
p21 <- apa_plot_network_nct(nct)
p22 <- apa_plot_clinical_cart_rf(cart_cp, rf_imp)
p23 <- apa_plot_bayesian_forest(bayes_h1, bayes_h3)
p24 <- apa_plot_bayesian_diagnostics(bayes_d1, bayes_d3)

stopifnot(inherits(p1, "ggplot"))
stopifnot(inherits(p2, "ggplot"))
stopifnot(inherits(p3, "ggplot"))
stopifnot(inherits(p4, "ggplot"))
stopifnot(inherits(p5, "ggplot"))
stopifnot(inherits(p6, "ggplot"))
stopifnot(inherits(p7, "ggplot"))
stopifnot(inherits(p8, "ggplot"))
stopifnot(inherits(p9, "ggplot"))
stopifnot(inherits(p10, "ggplot"))
stopifnot(inherits(p11, "ggplot"))
stopifnot(inherits(p12, "ggplot"))
stopifnot(inherits(p13, "ggplot"))
stopifnot(inherits(p14, "ggplot"))
stopifnot(inherits(p15, "ggplot"))
stopifnot(inherits(p16, "ggplot"))
stopifnot(inherits(p17, "ggplot"))
stopifnot(inherits(p18, "ggplot"))
stopifnot(inherits(p19, "ggplot"))
stopifnot(inherits(p20, "ggplot"))
stopifnot(inherits(p21, "ggplot"))
stopifnot(inherits(p22, "ggplot"))
stopifnot(inherits(p23, "ggplot"))
stopifnot(inherits(p24, "ggplot"))
stopifnot(nrow(apa_h1_forest_data(h1_rows)) == 12L)
stopifnot(nrow(apa_h4_path_data(h4)) == 4L)
stopifnot(nrow(apa_h5_bland_altman_data(family)) == n * 4L * 3L)
stopifnot(nrow(apa_h2_apim_path_data(h2)) == 16L)
stopifnot(nrow(apa_h3_stratified_forest_data(h3)) == 12L)
stopifnot(nrow(apa_specification_curve_data(multiverse)) == nrow(multiverse))
stopifnot(nrow(apa_sensemakr_contour_data(sense)$points) == 4L)
stopifnot(length(unique(apa_clinical_roc_data(clinical)$model)) == 2L)
stopifnot(nrow(apa_h1_three_way_emm_data(h1_emm)) == nrow(h1_emm))
stopifnot(nrow(apa_mediation_effects_data(med_simple, med_multi, med_cond)) > 0L)
stopifnot(nrow(apa_lpa_fit_data(lpa_fit)) == 14L)
stopifnot(nrow(apa_network_layout_data(net_edges, net_cent)$edges) == nrow(net_edges))
stopifnot(nrow(apa_bayesian_posterior_data(bayes_h1, bayes_h3)) == 4L)

tmp <- tempfile(fileext = ".png")
saved <- save_apa_plot(p1, tmp, width = 5, height = 4, dpi = 96)
manifest <- apa_figure_manifest(c(h1_forest = saved))
stopifnot(file.exists(saved))
stopifnot(manifest$exists[[1L]])
stopifnot(manifest$bytes[[1L]] > 0)

cat("[PASS] APA figures Sprint A plot builders\n")
