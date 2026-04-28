source("R/29_apa_tables.R")
source("R/31_final_plans.R")

bundle <- final_planning_bundle()

paths <- c(
  publication_strategy = "outputs/tables/final_plan_publication_strategy.csv",
  publication_evidence_map = "outputs/tables/final_plan_publication_evidence_map.csv",
  risk_matrix = "outputs/tables/final_plan_risk_matrix.csv",
  risk_summary = "outputs/tables/final_plan_risk_summary.csv",
  timeline_24_week = "outputs/tables/final_plan_timeline_24_week.csv",
  timeline_summary = "outputs/tables/final_plan_timeline_summary.csv"
)

for (id in names(paths)) {
  save_apa_table_csv(bundle[[id]], paths[[id]])
}

manifest <- final_planning_manifest(bundle)
manifest$path <- unname(paths[manifest$artifact])
manifest$exists <- file.exists(manifest$path)
manifest$bytes <- ifelse(manifest$exists, file.info(manifest$path)$size, NA_real_)
manifest_path <- save_apa_table_csv(manifest, "outputs/tables/final_plan_manifest.csv")

if (any(!manifest$exists) || any(is.na(manifest$bytes)) || any(manifest$bytes <= 0)) {
  stop("Final planning audit failed: at least one aggregate plan output is missing or empty", call. = FALSE)
}

cat(sprintf(
  "Final planning audit passed: artifacts=%d, publication=%d manuscripts, risks=%d, timeline_rows=%d\n",
  nrow(manifest),
  nrow(bundle$publication_strategy),
  nrow(bundle$risk_matrix),
  nrow(bundle$timeline_24_week)
))
