source("R/29_apa_tables.R")
source("R/30_thesis_mapping.R")

figure_manifest <- utils::read.csv("outputs/tables/apa_sprint_a_figure_manifest.csv", fileEncoding = "UTF-8")
table_manifest <- utils::read.csv("outputs/tables/apa_sprint_a_table_manifest.csv", fileEncoding = "UTF-8")

chapters <- thesis_chapter_mapping()
checks <- thesis_mapping_checks(chapters, figure_manifest, table_manifest, "outputs/quarto/thesis.html")
manifest <- thesis_mapping_manifest(chapters, checks)

chapter_path <- save_apa_table_csv(chapters, "outputs/tables/thesis_chapter_mapping.csv")
checks_path <- save_apa_table_csv(checks, "outputs/tables/thesis_mapping_checks.csv")
manifest_path <- save_apa_table_csv(manifest, "outputs/tables/thesis_mapping_manifest.csv")

if (any(checks$status != "verified")) {
  stop("Thesis mapping audit failed: at least one mapping check is not verified", call. = FALSE)
}

cat(sprintf(
  "Thesis mapping audit passed: chapters=%d, checks=%d verified\n",
  nrow(chapters),
  nrow(checks)
))
