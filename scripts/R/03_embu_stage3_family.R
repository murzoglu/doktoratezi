#!/usr/bin/env Rscript

source("R/04_embu_stage3_family.R")

result <- run_embu_stage3_family()

cat("EMBU stage 3 family cleaning complete\n")
print(result$summary)
