source("R/49_phase2_thesis_mapping.R")

# 1) Chapter mapping
chap <- phase2_thesis_chapter06_mapping()
stopifnot(nrow(chap) == 13L)
stopifnot(all(c("chapter_section", "primary_audit_csv", "primary_figure",
  "headline_finding") %in% names(chap)))

# 2) Publication plan
pubs <- phase2_publication_plan()
stopifnot(nrow(pubs) == 3L)
stopifnot(all(c("Makale_4", "Makale_5", "Makale_6") %in% pubs$paper_id))
stopifnot(all(c("title", "primary_findings", "target_journal_primary",
  "submission_target") %in% names(pubs)))

# 3) Paragraph seeds
seeds <- phase2_quarto_chapter_paragraph_seeds()
stopifnot(length(seeds) == 13L)
stopifnot(all(vapply(seeds, nchar, integer(1L), USE.NAMES = FALSE) > 100L))
stopifnot(all(grepl("\\[KEŞİFSEL|KESIFSEL|Faz II", paste(seeds, collapse = " "))))

# 4) Pipeline
result <- run_phase2_thesis_mapping_pipeline()
stopifnot(grepl("KESIFSEL", result$target_summary$kanit_kategorisi, fixed = TRUE))
stopifnot(!is.null(result$chapter_mapping))
stopifnot(!is.null(result$publication_plan))
stopifnot(!is.null(result$paragraph_seeds_summary))

cat("PASS: tests/test_phase2_thesis_mapping.R\n")
