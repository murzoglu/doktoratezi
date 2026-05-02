# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXXII/94, 95 audit runner

source("R/49_phase2_thesis_mapping.R")

result <- run_phase2_thesis_mapping_pipeline()

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

utils::write.csv(result$chapter_mapping,
  "outputs/tables/phase2_thesis_chapter06_mapping.csv",
  row.names = FALSE, fileEncoding = "UTF-8")
utils::write.csv(result$publication_plan,
  "outputs/tables/phase2_thesis_publication_plan.csv",
  row.names = FALSE, fileEncoding = "UTF-8")
utils::write.csv(result$paragraph_seeds_summary,
  "outputs/tables/phase2_thesis_paragraph_seeds_summary.csv",
  row.names = FALSE, fileEncoding = "UTF-8")
utils::write.csv(result$target_summary,
  "outputs/tables/phase2_thesis_target_summary.csv",
  row.names = FALSE, fileEncoding = "UTF-8")

cat(sprintf("[Faz II/KISIM XXXII/94] Bolum 6 chapter mapping: %d alt-bolum\n",
  nrow(result$chapter_mapping)))
cat(sprintf("[Faz II/KISIM XXXII/95] Yayin plan: %d makale\n",
  nrow(result$publication_plan)))
for (i in seq_len(nrow(result$publication_plan))) {
  cat(sprintf("  %s: %s\n",
    result$publication_plan$paper_id[i],
    result$publication_plan$title[i]))
}

invisible(result)
