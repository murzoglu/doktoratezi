# Doktoratezi AI Audit Policy

## Scope

This policy adapts the upstream `ai-audit.zip` reliability scaffold to the doktoratezi T1DM thesis repo. It is for AI-agent reliability, not for replacing statistical review, clinical interpretation, or thesis-supervisor approval.

## Hard Boundaries

- Do not print, summarize row-level content, or add memory from `data/raw/`, `data/identified/`, `data/cleaned/`, `data/backup/`, `data/processed/*`, `outputs/*`, or `_targets/`.
- Do not install the scaffold globally from this repo. The repo-safe installer intentionally has no `--global` mode.
- Do not start observability services or add CI workflows unless the user explicitly asks.
- Do not stage with `git add .`; stage plugin files by name if a commit is requested.

## Primary Repo Sources

- Project rules: `AGENTS.md`, `CLAUDE.md`
- Official thesis writing center: `tez-yazim/README.md`
- Official Marmara guide/templates: `docs/tez-kilavuz/`
- Pipeline map: `_targets.R`
- Canonical data contract: `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`
- Canonical lock: `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`
- Active analysis code: `R/*.R`, runner layer under `scripts/R/`, tests under `tests/`

## Reliability Gate Expectations

- Source grounding: factual repo claims should cite a checked file path and line when practical.
- Claim verification: numeric/clinical claims need either a dated repo artifact or primary external source.
- Thesis-format verification: final formatting, section order, decimal comma, summary structure, table/figure rules, and reference-list format need `tez-yazim/` or `docs/tez-kilavuz/` grounding.
- Deterministic gates: hooks may block obvious secrets, destructive commands, direct shell dumps of sensitive data dirs, and broad staging.
- Regression checks: promptfoo cases should test behavior around canonical lock, raw-data refusal, Turkish thesis language, and source separation.
- Synthetic hook tests: run `scripts/test_repo_ai_reliability.py` after editing hooks, verifier files, installer behavior, or plugin assets.

## Recommended Validation

Use the smallest relevant test first:

```bash
Rscript tests/test_reproducibility_lock.R
Rscript tests/test_final_reference_loading.R
Rscript tests/test_data_governance.R
```

For analysis-module edits, run the matching `tests/test_*.R` file. Run `Rscript -e 'renv::status()'` when dependency or reproducibility assumptions are touched. Run `quarto check` or `quarto render thesis.qmd` only when Quarto structure or thesis text rendering is affected.
