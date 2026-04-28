#!/usr/bin/env Rscript

source("R/02_embu_stage1.R")

result <- run_embu_stage1()

cat("EMBU stage 1 standardization complete\n")
print(result$summary)
