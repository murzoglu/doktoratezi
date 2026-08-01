source("R/10_derived_scores.R")
source("R/16_h1_child_perception.R")

set.seed(20260428)

n_families <- 48L
family <- data.frame(
  aile_no = seq_len(n_families),
  group = rep(c("Kontrol", "DM"), each = n_families / 2L),
  ses_latent = stats::rnorm(n_families),
  age_gap = stats::runif(n_families, 1, 6),
  cocuk_sayisi = sample(2:4, n_families, replace = TRUE),
  stringsAsFactors = FALSE
)

long <- do.call(rbind, lapply(seq_len(n_families), function(i) {
  roles <- if (family$group[[i]] == "DM") {
    c("DM_Hasta_Indeks", "DM_Hasta_Kardes")
  } else {
    c("Kontrol_Indeks", "Kontrol_Kardes")
  }
  data.frame(
    aile_no = family$aile_no[[i]],
    role_f = factor(
      roles,
      levels = c("Kontrol_Indeks", "Kontrol_Kardes", "DM_Hasta_Indeks", "DM_Hasta_Kardes")
    ),
    group_f = factor(family$group[[i]], levels = c("Kontrol", "DM")),
    family_role_f = factor(c("index", "sibling"), levels = c("index", "sibling")),
    cinsiyet_f = factor(sample(c("Kiz", "Erkek"), 2, replace = TRUE), levels = c("Kiz", "Erkek")),
    cocuk_yas = c(10, 13) + stats::rnorm(2, 0, 0.4),
    stringsAsFactors = FALSE
  )
}))
long$aile_no_f <- factor(long$aile_no)

role_effect <- as.numeric(long$role_f) * 0.05
long$embu_c_sicaklik_mean <- 2.7 + role_effect + stats::rnorm(nrow(long), 0, 0.15)
long$embu_c_asiri_koruma_mean <- 2.4 + role_effect + stats::rnorm(nrow(long), 0, 0.15)
long$embu_c_reddetme_mean <- 1.4 + role_effect + stats::rnorm(nrow(long), 0, 0.12)
long$embu_c_karsilastirma_mean <- 1.6 + role_effect + stats::rnorm(nrow(long), 0, 0.12)

for (item in sprintf("embu_c_q%02d", 1:29)) {
  long[[item]] <- sample(1:4, nrow(long), replace = TRUE)
}

frame <- h1_prepare_analysis_frame(long, family)
stopifnot(nrow(frame) == nrow(long))
stopifnot(all(c("ses_latent", "age_gap", "cocuk_sayisi", "cocuk_yas_z", "ses_latent_z") %in% names(frame)))
stopifnot(nrow(attr(frame, "h1_scaling")) == 4L)

descriptives <- h1_outcome_descriptives(frame)
stopifnot(all(c("outcome", "role", "n", "mean", "median", "floor_pct", "ceiling_pct") %in% names(descriptives)))
stopifnot(nrow(descriptives) == 16L)

frequentist <- run_h1_frequentist(frame)
stopifnot(length(frequentist$models) == 4L)
stopifnot(all(c("outcome", "term", "estimate", "std_error", "p_value", "ci_low", "ci_high") %in% names(frequentist$fixed_effects)))
stopifnot(any(frequentist$fixed_effects$term == "role_fDM_Hasta_Indeks"))
stopifnot(nrow(frequentist$role_pairwise) == 24L)

# --- Grup-ici (within-group) rol kontrasti: yapi + yon-mantigi ---
wgc <- frequentist$within_group_role_contrast
# 2 kontrast (DM / Kontrol indeks-eksi-kardes) x 4 alt olcek = 8 satir
stopifnot(nrow(wgc) == 8L)
stopifnot(all(c("outcome", "contrast", "estimate", "std_error", "ci_low",
                "ci_high", "p_value", "p_fdr_within_family") %in% names(wgc)))
stopifnot(all(sort(unique(wgc$contrast)) ==
              sort(c("DM_indeks_eksi_kardes", "Kontrol_indeks_eksi_kardes"))))
# Her kontrast icin tam 4 alt olcek
stopifnot(sum(wgc$contrast == "DM_indeks_eksi_kardes") == 4L)
stopifnot(sum(wgc$contrast == "Kontrol_indeks_eksi_kardes") == 4L)
# GA nokta tahminini icermeli (tutarlilik)
stopifnot(all(wgc$ci_low <= wgc$estimate & wgc$estimate <= wgc$ci_high))
# BH-FDR ham p'den kucuk olamaz (monotonluk)
stopifnot(all(wgc$p_fdr_within_family >= wgc$p_value - 1e-9))

# --- Yon-mantigi: DM indeks cocuguna kasitli +etki, kontrol kolu bozulmadan ---
long_dir <- long
dm_idx <- long_dir$role_f == "DM_Hasta_Indeks"
long_dir$embu_c_reddetme_mean <- 1.4 + 0.6 * dm_idx +
  stats::rnorm(nrow(long_dir), 0, 0.10)
frame_dir <- h1_prepare_analysis_frame(long_dir, family)
wgc_dir <- run_h1_frequentist(frame_dir)$within_group_role_contrast
red_dm <- wgc_dir[wgc_dir$outcome == "embu_c_reddetme_mean" &
                    wgc_dir$contrast == "DM_indeks_eksi_kardes", ]
red_kontrol <- wgc_dir[wgc_dir$outcome == "embu_c_reddetme_mean" &
                         wgc_dir$contrast == "Kontrol_indeks_eksi_kardes", ]
# DM indeks-kardes farki pozitif ve anlamli (kasitli etki yakalanmali)
stopifnot(red_dm$estimate > 0.3)
stopifnot(red_dm$p_fdr_within_family < 0.05)
# Kontrol kolunda ayni boyutta fark null kalmali (etki yalniz DM indeks'e verildi)
stopifnot(abs(red_kontrol$estimate) < 0.2)
stopifnot(red_kontrol$p_value > 0.05)
stopifnot(all(c("icc", "r2_marginal", "r2_conditional", "singular") %in% names(frequentist$diagnostics)))

three_way <- run_h1_three_way(frame)
stopifnot(length(three_way$models) == 4L)
stopifnot(nrow(three_way$tests) == 4L)
stopifnot(all(grepl("role_f:cocuk_yas_z:cinsiyet_f", three_way$tests$effect)))
stopifnot(nrow(three_way$emmeans_grid) > 0L)

bayes_plan <- h1_bayesian_plan()
stopifnot(nrow(bayes_plan) == 4L)
stopifnot(all(bayes_plan$default_execution == "manual_not_in_targets_or_audit"))

pipeline <- run_h1_child_perception_pipeline(long, family, run_irt = FALSE)
stopifnot(pipeline$target_summary$analysis_rows == nrow(long))
stopifnot(pipeline$target_summary$primary_models == 4L)
stopifnot(pipeline$target_summary$within_group_contrast_tests == 8L)
stopifnot(!is.null(pipeline$primary_within_group_role_contrast))
stopifnot(nrow(pipeline$primary_within_group_role_contrast) == 8L)
stopifnot(pipeline$target_summary$three_way_models == 4L)
stopifnot(pipeline$target_summary$irt_success_n == 0L)

bad_long <- long[, setdiff(names(long), "role_f")]
stopifnot(inherits(
  try(h1_prepare_analysis_frame(bad_long, family), silent = TRUE),
  "try-error"
))
