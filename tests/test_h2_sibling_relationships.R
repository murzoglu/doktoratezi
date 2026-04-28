source("R/17_h2_sibling_relationships.R")

set.seed(20260428)

n_families <- 64L
family <- data.frame(
  aile_no = seq_len(n_families),
  group_f = factor(rep(c("Kontrol", "DM"), each = n_families / 2L), levels = c("Kontrol", "DM")),
  age_gap = stats::runif(n_families, 0.5, 6),
  same_sex = factor(sample(c("Farkli", "Ayni"), n_families, replace = TRUE), levels = c("Farkli", "Ayni")),
  ses_latent = stats::rnorm(n_families),
  stringsAsFactors = FALSE
)

long <- do.call(rbind, lapply(seq_len(n_families), function(i) {
  data.frame(
    aile_no = family$aile_no[[i]],
    aile_no_f = factor(family$aile_no[[i]]),
    group_f = family$group_f[[i]],
    family_role_f = factor(c("index", "sibling"), levels = c("index", "sibling")),
    stringsAsFactors = FALSE
  )
}))
long$aile_no_f <- factor(long$aile_no)
long$group_f <- factor(as.character(long$group_f), levels = c("Kontrol", "DM"))

group_effect <- ifelse(long$group_f == "DM", 0.18, 0)
role_effect <- ifelse(long$family_role_f == "sibling", -0.08, 0)
long$srq_ho_warmth_mean <- 3.1 + group_effect + role_effect + stats::rnorm(nrow(long), 0, 0.25)
long$srq_ho_status_mean <- 3.3 + group_effect + role_effect + stats::rnorm(nrow(long), 0, 0.25)
long$srq_ho_conflict_mean <- 2.7 + group_effect - role_effect + stats::rnorm(nrow(long), 0, 0.25)
long$srq_ho_rivalry_mean <- 3.0 + group_effect + stats::rnorm(nrow(long), 0, 0.25)

for (item in paste0("srq_", 1:48)) {
  long[[item]] <- sample(1:5, nrow(long), replace = TRUE)
}

long_frame <- h2_prepare_long_frame(long, family)
stopifnot(nrow(long_frame) == nrow(long))
stopifnot(all(c("age_gap", "same_sex", "ses_latent", "age_gap_z", "ses_latent_z") %in% names(long_frame)))
stopifnot(nrow(attr(long_frame, "h2_scaling")) == 2L)

family_frame <- h2_build_family_mean_frame(long_frame)
stopifnot(nrow(family_frame) == n_families)
stopifnot(all(h2_outcome_spec()$outcome %in% names(family_frame)))
stopifnot(all(family_frame$child_rows == 2L))

long_desc <- h2_long_descriptives(long_frame)
family_desc <- h2_family_mean_descriptives(family_frame)
stopifnot(nrow(long_desc) == 16L)
stopifnot(nrow(family_desc) == 8L)
stopifnot(all(c("mean", "median", "floor_pct", "ceiling_pct") %in% names(long_desc)))

family_mean <- run_h2_family_mean(family_frame)
stopifnot(nrow(family_mean) == 4L)
stopifnot(all(c("mean_difference_dm_minus_control", "p_value", "hedges_g", "p_fdr_across_h2") %in% names(family_mean)))

apim <- run_h2_apim(long_frame)
stopifnot(nrow(apim$diagnostics) == 4L)
stopifnot(all(c("outcome", "term", "estimate", "std_error", "p_value", "p_fdr_across_h2") %in% names(apim$fixed_effects)))
stopifnot(any(apim$fixed_effects$term == "group_fDM:family_role_fsibling"))

moderation <- run_h2_age_gap_moderation(family_frame)
stopifnot(nrow(moderation$diagnostics) == 4L)
stopifnot(any(moderation$anova$effect == "group_f:age_gap_z:same_sex"))
stopifnot(all(c("f_value", "p_value", "p_fdr_across_h2") %in% names(moderation$anova)))

wide <- h2_wide_items_by_family(long_frame)
stopifnot(nrow(wide) == n_families)
stopifnot(all(c("srq_4_index", "srq_4_sibling", "srq_20_index", "srq_36_sibling") %in% names(wide)))

pipeline <- run_h2_sibling_relationships_pipeline(long, family, run_cfa = FALSE)
stopifnot(pipeline$target_summary$long_rows == nrow(long))
stopifnot(pipeline$target_summary$family_rows == n_families)
stopifnot(pipeline$target_summary$apim_models == 4L)
stopifnot(identical(pipeline$target_summary$olsen_kenny_status, "skipped"))

bad_long <- long[, setdiff(names(long), "family_role_f")]
stopifnot(inherits(
  try(h2_prepare_long_frame(bad_long, family), silent = TRUE),
  "try-error"
))
