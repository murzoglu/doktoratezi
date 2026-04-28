source("R/12_missing_data_frames.R")

fixture <- data.frame(
  aile_no = 1:6,
  group = c("DM", "DM", "DM", "Kontrol", "Kontrol", "Kontrol"),
  cocuk_yas = c(10, 11, 12, 10, 11, 12),
  kardes_yas = c(8, 9, 10, 8, 9, 10),
  katilimci_cocuk_cinsiyet = c(1, 0, 1, 0, 1, 0),
  kardes_cinsiyet = c(0, 1, 0, 1, 0, 1),
  anne_yas = c(35, 36, 37, 35, 36, 37),
  anne_antidepresan = c(0, 1, 0, 0, 0, 1),
  cocuk_sayisi = c(2, 2, 3, 2, 3, 3),
  egitim_durumu = c(3, 4, 5, 3, 4, 5),
  es_egitim_durumu = c(3, 4, 4, 3, 4, 5),
  aile_isei08 = c(30, NA, 50, 35, 45, 55),
  material_index = c(-1.1, -0.2, 0.4, -0.7, 0.1, 1.2),
  material_quintile = ordered(c(1, 2, 4, 1, 3, 5), levels = 1:5),
  ses_composite_eq = c(-0.9, -0.1, 0.5, -0.6, 0.2, 0.9),
  ses_latent = c(-0.8, -0.2, 0.6, -0.5, 0.1, 0.8),
  hba1c = c(8.1, NA, 7.4, NA, NA, NA),
  dm_yili = c(3, 4, 5, NA, NA, NA),
  embu_p_sicaklik_mean = c(3.0, 3.1, 3.2, 2.9, 3.0, 3.3),
  embu_p_reddetme_mean = c(1.2, 1.3, 1.1, 1.4, 1.2, 1.1),
  embu_c_idx_sicaklik_mean = c(3.2, 3.3, 3.0, 3.1, 3.2, 3.4),
  embu_c_sib_sicaklik_mean = c(3.0, 2.9, 3.1, 3.2, 3.1, 3.0),
  srq_ho_warmth_mean = c(4.0, 4.1, 4.2, 4.0, 3.9, 4.3),
  srq_sib_ho_warmth_mean = c(3.9, 4.0, 4.1, 3.8, 4.0, 4.2),
  beck_total = c(8, NA, 12, 6, 5, 7)
)

results <- derive_missing_data_frames(fixture, run_mcar = FALSE)

summary <- results$variable_summary
hba1c_summary <- summary[summary$variable == "hba1c", , drop = FALSE]
stopifnot(identical(hba1c_summary$structural_missing_n, 3L))
stopifnot(identical(hba1c_summary$analytic_missing_n, 1L))
stopifnot(isTRUE(all.equal(hba1c_summary$analytic_missing_pct, 100 / 3)))

stopifnot(!"hba1c" %in% names(results$frames$mi_primary))
stopifnot("hba1c" %in% names(results$frames$mi_clinical_sensitivity))

primary_spec <- results$mice_specs$primary
clinical_spec <- results$mice_specs$clinical_sensitivity
stopifnot(identical(unname(primary_spec$method["aile_no"]), ""))
stopifnot(identical(unname(primary_spec$method["group"]), ""))
stopifnot(identical(unname(clinical_spec$method["hba1c"]), "pmm"))

clinical_where <- clinical_spec$where
stopifnot(identical(unname(clinical_where[1:3, "hba1c"]), c(FALSE, TRUE, FALSE)))
stopifnot(identical(unname(clinical_where[4:6, "hba1c"]), c(FALSE, FALSE, FALSE)))

manifest <- results$frame_manifest
stopifnot(any(manifest$frame == "complete_case_primary"))
stopifnot(manifest$n_rows[manifest$frame == "complete_case_primary"] < nrow(fixture))

delta_grid <- results$nmar_delta_grid
stopifnot(any(delta_grid$variable == "beck_total"))
stopifnot(any(delta_grid$variable == "hba1c"))

completed_long <- data.frame(
  .imp = c(1, 1, 1, 1, 1, 1),
  .id = as.character(1:6),
  beck_total = c(8, 9, 12, 6, 5, 7)
)
adjusted <- apply_nmar_delta_adjustment(completed_long, results$frames$mi_primary, "beck_total", 2)
stopifnot(identical(adjusted$beck_total, c(8, 11, 12, 6, 5, 7)))

bad_fixture <- fixture[, setdiff(names(fixture), "group")]
stopifnot(inherits(
  try(derive_missing_data_frames(bad_fixture, run_mcar = FALSE), silent = TRUE),
  "try-error"
))
