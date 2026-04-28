# scripts/R/27_network_audit.R

suppressPackageStartupMessages({ library(targets) })

source("R/00_paths.R")
source("R/26_network_analysis.R")

paths <- thesis_paths()
out_tables <- file.path(paths$outputs_dir, "tables")
dir.create(out_tables, showWarnings = FALSE, recursive = TRUE)

tar_load(c(df_family_ses, df_family_scored))

results <- run_network_pipeline(df_family_ses, df_family_scored)

write_csv <- function(df, name) {
  if (is.null(df) || (is.data.frame(df) && nrow(df) == 0L)) {
    cat(sprintf("  [skip] %s — empty\n", name))
    return(invisible(NULL))
  }
  utils::write.csv(df, file.path(out_tables, paste0(name, ".csv")), row.names = FALSE)
  cat(sprintf("  [ok]   %s.csv (%d rows)\n", name, nrow(df)))
}

cat("\n=== KISIM VIII Network Audit ===\n")
write_csv(results$status_table,           "network_status")
write_csv(results$edges_table,            "network_edges")
write_csv(results$centrality_table,       "network_centrality")
write_csv(results$nct_table,              "network_nct")
write_csv(results$beck_centrality_table,  "network_beck_centrality")

cat("\n=== Network status ===\n")
print(results$status_table)
cat("\n=== NCT (DM × Kontrol) ===\n")
print(results$nct_table)
cat("\n=== Top 5 centrality (strength) by group ===\n")
if (nrow(results$centrality_table) > 0L) {
  by_group <- split(results$centrality_table, results$centrality_table$group)
  for (g in names(by_group)) {
    cat(sprintf("\n--- %s ---\n", g))
    sub <- by_group[[g]][order(-by_group[[g]]$strength), ][1:5, ]
    print(sub[, c("variable", "strength", "expected_influence")])
  }
}
cat("\n[done] Network audit complete.\n")
