---
description: "Use when editing R pipeline, targets, runner scripts, or stopifnot tests in this Quarto thesis repository. Covers R/ pure functions, scripts/R side effects, tests, renv, targets, and generated output boundaries."
name: "R Pipeline Conventions"
applyTo:
  - "R/**/*.R"
  - "scripts/R/**/*.R"
  - "tests/**/*.R"
  - "_targets.R"
---
# R Pipeline Conventions

Before changing pipeline code, read [AGENTS.md](../../AGENTS.md) and [CLAUDE.md](../../CLAUDE.md) for the current analysis status.

- Keep [R/](../../R/) as a library layer: pure functions only, no file writes, no implicit working-directory changes, no package installation.
- Put file I/O and artifact creation in [scripts/R/](../../scripts/R/) runners. Runner scripts should call library functions and write to `data/processed/` or `outputs/`.
- Keep tests in [tests/](../../tests/) focused on pure functions and invariants. Existing tests use `stopifnot()`; quiet output means PASS.
- Preserve the current `targets` boundary: [_targets.R](../../_targets.R) currently computes project paths and raw-data manifest only.
- Use `renv` for package reproducibility. Do not add ad hoc installation code to analysis scripts.
- Treat `data/raw/`, `data/processed/*`, `outputs/*`, `_targets/`, credentials, and `.env*` as non-committed data/artifact boundaries.
- Treat EMBU data architecture v2.0 as active. For EMBU edits, read [docs/veri-duzenleme/EMBU-STANDARTLASTIRMA.md](../../docs/veri-duzenleme/EMBU-STANDARTLASTIRMA.md) and the EMBU-P/EMBU-C mapping matrices first; do not carry forward obsolete inactive-status assumptions.

## Verification

Run the narrowest relevant command after edits:

```bash
Rscript tests/test_embu_stage1.R
Rscript tests/test_embu_stage2_likert4.R
Rscript tests/test_embu_stage3_family.R
Rscript -e 'targets::tar_make()'
quarto render thesis.qmd
```
