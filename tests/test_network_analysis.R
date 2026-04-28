# tests/test_network_analysis.R
# KISIM VIII — Network analizi: GGM + NCT + Beck symptom network.

suppressPackageStartupMessages({ library(targets) })
source("R/00_paths.R")
source("R/26_network_analysis.R")

tar_load(c(df_family_ses, df_family_scored))

# Variable list
vars <- network_parenting_outcomes()
stopifnot(length(vars) >= 8L)

# GGM EBIC-LASSO — pooled
df_prep <- df_family_ses
df_prep$group_f <- factor(as.character(df_prep$group_f), levels = c("Kontrol", "DM"))
ggm_all <- run_ggm_lasso(df_prep, vars, group_label = "all")
stopifnot(
  ggm_all$status == "ok",
  ggm_all$n >= 200L,
  is.data.frame(ggm_all$edges_table),
  nrow(ggm_all$edges_table) >= 1L,
  is.data.frame(ggm_all$centrality_table),
  nrow(ggm_all$centrality_table) == length(vars),
  all(c("strength", "closeness", "betweenness", "expected_influence") %in%
        names(ggm_all$centrality_table))
)

# NCT — DM × Kontrol
nct <- run_nct(df_prep, vars, group_col = "group_f", n_perm = 100L, seed = 42L)
stopifnot(
  nct$status == "ok",
  nct$n_dm >= 100L,
  nct$n_ko >= 100L,
  is.finite(nct$M_glstrinv),
  is.finite(nct$M_glstrinv_pvalue)
)

# Beck symptom network
beck <- run_beck_symptom_network(df_family_scored, group_label = "all")
stopifnot(
  beck$status == "ok",
  beck$n >= 200L,
  is.data.frame(beck$centrality_table),
  nrow(beck$centrality_table) == 21L
)

# Pipeline orchestrator
results <- run_network_pipeline(df_family_ses, df_family_scored, seed = 42L)
stopifnot(
  is.data.frame(results$status_table),
  nrow(results$status_table) == 5L,
  all(results$status_table$status %in% c("ok", "insufficient_n", "package_unavailable"))
)

cat("[PASS] KISIM VIII Network analysis (GGM + NCT + Beck symptom)\n")
