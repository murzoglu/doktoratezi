source("R/30_thesis_mapping.R")

chapters <- thesis_chapter_mapping()
stopifnot(nrow(chapters) == 5L)
stopifnot(all(file.exists(chapters$path)))
stopifnot(any(chapters$chapter == "03_bulgular"))

figure_manifest <- utils::read.csv("outputs/tables/apa_sprint_a_figure_manifest.csv", fileEncoding = "UTF-8")
table_manifest <- utils::read.csv("outputs/tables/apa_sprint_a_table_manifest.csv", fileEncoding = "UTF-8")

checks <- thesis_mapping_checks(chapters, figure_manifest, table_manifest, "outputs/quarto/thesis.html")
stopifnot(nrow(checks) == 6L)
stopifnot(all(checks$status == "verified"))

manifest <- thesis_mapping_manifest(chapters, checks)
stopifnot(manifest$value[manifest$metric == "review_checks"] == 0L)

cat("[PASS] Thesis chapter-artifact mapping\n")
