source("R/19_h4_beck_parenting_sem.R")

set.seed(20260428)

n_families <- 96L
family <- data.frame(
  aile_no = seq_len(n_families),
  group_f = factor(rep(c("Kontrol", "DM"), each = n_families / 2L), levels = c("Kontrol", "DM")),
  anne_yas = stats::rnorm(n_families, 38, 5),
  ses_latent = stats::rnorm(n_families),
  stringsAsFactors = FALSE
)

latent <- data.frame(
  sicaklik = stats::rnorm(n_families),
  asiri_koruma = stats::rnorm(n_families),
  reddetme = stats::rnorm(n_families),
  karsilastirma = stats::rnorm(n_families),
  beck_dep = stats::rnorm(n_families),
  stringsAsFactors = FALSE
)

make_ordinal <- function(theta, min_value, max_value) {
  raw <- theta + stats::rnorm(length(theta), 0, 0.75)
  as.integer(cut(raw, breaks = stats::quantile(raw, probs = seq(0, 1, length.out = max_value - min_value + 2), na.rm = TRUE), include.lowest = TRUE, labels = min_value:max_value))
}

item_map <- h4_embu_subscale_map()
for (subscale in names(item_map)) {
  for (item in item_map[[subscale]]) {
    family[[paste0("embu_p_q", sprintf("%02d", item))]] <- make_ordinal(latent[[subscale]], 1L, 4L)
  }
}
for (item in 1:21) {
  family[[paste0("beck_", item)]] <- make_ordinal(latent$beck_dep, 0L, 3L)
}

frame <- h4_prepare_analysis_frame(family)
stopifnot(nrow(frame) == n_families)
stopifnot(all(c("anne_yas_z", "ses_latent_z") %in% names(frame)))
stopifnot(nrow(attr(frame, "h4_scaling")) == 2L)
stopifnot(identical(levels(frame$group_f), c("Kontrol", "DM")))

diagnostics <- h4_item_diagnostics(frame)
stopifnot(nrow(diagnostics) == 50L)
stopifnot(all(c("item", "n_categories", "sparse_category_n") %in% names(diagnostics)))

collapse_fixture <- frame
collapse_fixture$embu_p_q12[collapse_fixture$group_f == "Kontrol"] <- ifelse(
  collapse_fixture$embu_p_q12[collapse_fixture$group_f == "Kontrol"] == 4L,
  3L,
  collapse_fixture$embu_p_q12[collapse_fixture$group_f == "Kontrol"]
)
collapse_plan <- h4_sparse_group_collapse_plan(collapse_fixture, ordered_items = "embu_p_q12")
stopifnot(nrow(collapse_plan) >= 1L)
collapsed_fixture <- h4_apply_sparse_collapse_plan(collapse_fixture, collapse_plan)
tab <- table(collapsed_fixture$group_f, collapsed_fixture$embu_p_q12)
stopifnot(!any(tab == 0L))

syntax <- h4_latent_sem_model_syntax()
stopifnot(grepl("beck_dep =~ beck_1", syntax, fixed = TRUE))
stopifnot(grepl("sicaklik ~ b_sicaklik*beck_dep", syntax, fixed = TRUE))
stopifnot(grepl("karsilastirma ~ b_karsilastirma*beck_dep", syntax, fixed = TRUE))

unlabeled <- h4_latent_sem_model_syntax(label_paths = FALSE)
stopifnot(!grepl("b_sicaklik*", unlabeled, fixed = TRUE))
stopifnot(grepl("sicaklik ~ beck_dep", unlabeled, fixed = TRUE))

plan <- h4_bayesian_sem_plan()
stopifnot(nrow(plan) == 1L)
stopifnot(identical(plan$default_execution, "manual_not_in_targets_or_audit"))
stopifnot(grepl("beck_6", plan$ordered_items, fixed = TRUE))

pipeline <- run_h4_beck_parenting_sem_pipeline(family, run_sem = FALSE, run_multigroup = FALSE)
stopifnot(pipeline$target_summary$family_rows == n_families)
stopifnot(pipeline$target_summary$ordered_items == 50L)
stopifnot(identical(pipeline$target_summary$latent_sem_status, "skipped"))
stopifnot(pipeline$target_summary$bayesian_sampling_in_default_pipeline == FALSE)
stopifnot("multigroup_sparse_collapse_map" %in% names(pipeline))

bad_family <- family[, setdiff(names(family), "beck_21")]
stopifnot(inherits(
  try(h4_prepare_analysis_frame(bad_family), silent = TRUE),
  "try-error"
))
