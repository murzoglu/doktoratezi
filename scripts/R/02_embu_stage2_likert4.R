#!/usr/bin/env Rscript

source("R/03_embu_stage2_likert4.R")

result <- run_embu_likert4()

cat("EMBU stage 2 Likert 4pt conversion complete\n")
print(result$summary)
