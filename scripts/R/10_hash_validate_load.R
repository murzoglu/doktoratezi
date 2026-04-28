source("R/07_reproducibility.R")
source("R/01_io.R")

paths <- canonical_final_reference_paths()

manifest <- final_reference_validation_manifest(
  paths$lock,
  c(paths$family, paths$long)
)
stop_if_final_reference_invalid(manifest)

loaded <- load_final_reference_data(paths)
df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)

summary <- summarize_loaded_final_reference(
  loaded$family,
  loaded$long,
  df_family,
  df_long
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
utils::write.csv(
  manifest,
  "outputs/tables/final_reference_validation_manifest.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  summary,
  "outputs/tables/final_reference_load_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  "Final reference hash/load validated: family=%dx%d -> %dx%d; long=%dx%d -> %dx%d; 0 critical finding(s)\n",
  summary$raw_rows[summary$dataset == "family"],
  summary$raw_columns[summary$dataset == "family"],
  summary$prepared_rows[summary$dataset == "family"],
  summary$prepared_columns[summary$dataset == "family"],
  summary$raw_rows[summary$dataset == "long"],
  summary$raw_columns[summary$dataset == "long"],
  summary$prepared_rows[summary$dataset == "long"],
  summary$prepared_columns[summary$dataset == "long"]
))
