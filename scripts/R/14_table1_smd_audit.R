source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/13_table1_smd.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data

table1_results <- build_table1_family(df_family_ses)
target_summary <- summarize_table1_targets(df_family_ses, table1_results)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
utils::write.csv(
  table1_results$table,
  "outputs/tables/table1_family_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  table1_results$smd_balance,
  "outputs/tables/table1_smd_balance.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  table1_results$balance_action,
  "outputs/tables/table1_balance_action.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  table1_results$group_counts,
  "outputs/tables/table1_group_counts.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  target_summary,
  "outputs/tables/table1_target_summary.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

cat(sprintf(
  "Table 1/SMD audit passed: %s n=%d, %s n=%d, %d variable(s), %d action flag(s)\n",
  target_summary$group_1,
  target_summary$group_1_n,
  target_summary$group_2,
  target_summary$group_2_n,
  target_summary$smd_variables,
  target_summary$action_variables
))
