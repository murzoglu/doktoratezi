source("R/18_h3_parent_self_report.R")

set.seed(20260428)

n_families <- 80L
group <- factor(rep(c("Kontrol", "DM"), each = n_families / 2L), levels = c("Kontrol", "DM"))
group_dm <- as.integer(group == "DM")
anne_antidepresan <- rep(0L, n_families)
anne_antidepresan[c(6:15, 47:60)] <- 1L

family <- data.frame(
  aile_no = seq_len(n_families),
  group_f = group,
  anne_yas = stats::rnorm(n_families, 38, 4.5),
  ses_latent = stats::rnorm(n_families, 0, 1),
  age_gap = stats::runif(n_families, 0.5, 7),
  cocuk_sayisi = sample(2:4, n_families, replace = TRUE),
  anne_antidepresan = anne_antidepresan,
  stringsAsFactors = FALSE
)

family$embu_p_sicaklik_mean <- 3.20 + 0.10 * group_dm - 0.08 * family$anne_antidepresan + stats::rnorm(n_families, 0, 0.22)
family$embu_p_asiri_koruma_mean <- 2.60 + 0.16 * group_dm + 0.10 * family$anne_antidepresan + stats::rnorm(n_families, 0, 0.24)
family$embu_p_reddetme_mean <- 1.45 + 0.12 * group_dm + 0.15 * family$anne_antidepresan + stats::rnorm(n_families, 0, 0.18)
family$embu_p_karsilastirma_mean <- 1.80 + 0.09 * group_dm + 0.05 * family$anne_antidepresan + stats::rnorm(n_families, 0, 0.20)

propensity <- data.frame(
  aile_no = family$aile_no,
  group_dm = group_dm,
  ps_value = stats::plogis(-0.2 + 0.25 * family$ses_latent + 0.05 * family$age_gap),
  ps_logit = NA_real_,
  iptw_stabilized = stats::runif(n_families, 0.80, 1.25),
  stringsAsFactors = FALSE
)
propensity$ps_logit <- stats::qlogis(propensity$ps_value)
propensity$iptw_trimmed <- pmin(propensity$iptw_stabilized, 1.20)
propensity$iptw_trimmed_flag <- propensity$iptw_stabilized > 1.20
propensity$propensity_analysis_row <- seq_len(n_families)

frame <- h3_prepare_analysis_frame(family, propensity)
stopifnot(nrow(frame) == n_families)
stopifnot(all(c("anne_yas_z", "ses_latent_z", "age_gap_z", "iptw_trimmed") %in% names(frame)))
stopifnot(nrow(attr(frame, "h3_scaling")) == 3L)
stopifnot(identical(levels(frame$group_f), c("Kontrol", "DM")))
stopifnot(identical(levels(frame$anne_antidepresan_f), c("Yok", "Var")))

desc <- h3_outcome_descriptives(frame)
ad_counts <- h3_antidepressant_counts(frame)
stopifnot(nrow(desc) == 8L)
stopifnot(all(c("mean", "median", "floor_pct", "ceiling_pct") %in% names(desc)))
stopifnot(nrow(ad_counts) == 4L)
stopifnot("dm_minus_control_smd_for_ad_use" %in% names(ad_counts))

primary <- run_h3_primary(frame)
stopifnot(nrow(primary$group_effects) == 4L)
stopifnot(nrow(primary$diagnostics) == 4L)
stopifnot(all(primary$group_effects$term == "group_fDM"))
stopifnot(all(c("estimate", "std_beta", "p_fdr_across_h3_primary") %in% names(primary$group_effects)))

stratified <- run_h3_antidepressant_stratified(frame)
stopifnot(nrow(stratified) == 12L)
stopifnot(all(stratified$status == "fitted"))
stopifnot(all(c("stratum", "std_beta", "p_fdr_across_h3_stratified") %in% names(stratified)))

iptw <- run_h3_iptw(frame)
stopifnot(nrow(iptw$group_effects) == 4L)
stopifnot(nrow(iptw$diagnostics) == 4L)
stopifnot(all(iptw$group_effects$weight_column == "iptw_trimmed"))
stopifnot(all(c("estimate", "std_error", "p_fdr_across_h3_iptw") %in% names(iptw$group_effects)))

pipeline <- run_h3_parent_self_report_pipeline(family, propensity)
stopifnot(pipeline$target_summary$family_rows == n_families)
stopifnot(pipeline$target_summary$primary_models == 4L)
stopifnot(pipeline$target_summary$stratified_rows == 12L)
stopifnot(pipeline$target_summary$iptw_models == 4L)
stopifnot(pipeline$target_summary$antidepressant_yes_dm_n >= 5L)
stopifnot(pipeline$target_summary$antidepressant_yes_control_n >= 5L)

tiny_ad <- frame
tiny_ad$anne_antidepresan_bin[tiny_ad$group_f == "Kontrol"] <- 0L
tiny_ad$anne_antidepresan_f <- factor(tiny_ad$anne_antidepresan_bin, levels = c(0L, 1L), labels = c("Yok", "Var"))
tiny_stratified <- run_h3_antidepressant_stratified(tiny_ad)
ad_only <- tiny_stratified[tiny_stratified$stratum == "antidepressant_only", , drop = FALSE]
stopifnot(all(ad_only$status == "skipped"))

bad_family <- family[, setdiff(names(family), "anne_antidepresan")]
stopifnot(inherits(
  try(h3_prepare_analysis_frame(bad_family, propensity), silent = TRUE),
  "try-error"
))
