source("R/11_ses_composites.R")

fixture <- data.frame(
  egitim_durumu = c(1, 2, 4, 5),
  es_egitim_durumu = c(2, 2, 3, 5),
  calisma_durumu = c(0, 1, 1, 1),
  es_calisma_durumu = c(1, 1, 0, 1),
  cocuk_sayisi = c(2, 3, 1, 4),
  ev_oda_sayisi = c(0, 1, 2, 3),
  ev_sahipligi = c(1, 1, 0, 0),
  arabaniz_var_mi = c(0, 0, 1, 1),
  aile_isei08 = c(20, 35, 60, 85)
)

layer_a <- derive_ses_layer_a(fixture)
stopifnot(identical(layer_a$max_aile_egitim, c(2, 2, 4, 5)))
stopifnot(identical(layer_a$mean_aile_egitim, c(1.5, 2, 3.5, 5)))
stopifnot(identical(layer_a$egitim_fark, c(1, 0, 1, 0)))
stopifnot(identical(layer_a$cift_kazanc, c(0, 1, 0, 1)))
stopifnot(identical(layer_a$kalabalik_indeksi, c(2, 1.5, 1 / 3, 1)))

material <- derive_material_index(layer_a, use_polychoric = FALSE)
stopifnot(length(material$score) == nrow(fixture))
stopifnot(all(!is.na(material$score)))
stopifnot(all(material$quintile %in% 1:5))
stopifnot(material$diagnostics$orientation_correlation >= 0)
stopifnot(all(c("variable", "loading", "retained") %in% names(material$loadings)))

composite_input <- layer_a
composite_input$material_index <- material$score
composite_input <- add_ses_composite_scores(composite_input)
stopifnot(all(c("edu_z", "isei_z", "material_z", "ses_composite_eq", "ses_hollingshead") %in% names(composite_input)))
stopifnot(isTRUE(abs(mean(composite_input$edu_z, na.rm = TRUE)) < 1e-12))
stopifnot(isTRUE(stats::cor(composite_input$ses_composite_eq, composite_input$aile_isei08, use = "complete.obs") > 0))

ses <- derive_ses_composites(fixture, include_latent = FALSE, use_polychoric = FALSE)
stopifnot("data" %in% names(ses))
stopifnot("diagnostics" %in% names(ses))
stopifnot("material_loadings" %in% names(ses))
stopifnot(all(c("material_index", "material_quintile", "ses_composite_eq", "ses_hollingshead", "ses_latent") %in% names(ses$data)))
stopifnot(all(is.na(ses$data$ses_latent)))
stopifnot(identical(ses$diagnostics$latent_status, "not_run"))

summary <- ses_component_summary(ses$data)
stopifnot(any(summary$component == "material_index"))
stopifnot(any(summary$component == "ses_hollingshead"))

correlations <- ses_correlation_table(ses$data)
stopifnot(all(c("variable_1", "variable_2", "r") %in% names(correlations)))
stopifnot(any(correlations$variable_1 == "ses_composite_eq" & correlations$variable_2 == "material_index"))

target_summary <- summarize_ses_targets(fixture, ses$data)
stopifnot(identical(target_summary$input_rows, 4L))
stopifnot(target_summary$added_columns > 0)

bad_fixture <- fixture[, setdiff(names(fixture), "aile_isei08")]
stopifnot(inherits(
  try(derive_ses_composites(bad_fixture, include_latent = FALSE), silent = TRUE),
  "try-error"
))
