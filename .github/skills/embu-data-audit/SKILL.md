---
name: embu-data-audit
description: "Audit active EMBU data pipeline decisions in the doktoratezi repository. Use when working on EMBU, EMBU-C, EMBU-P, Likert 4pt/6pt, Stage 1, Stage 2, Stage 3, family matching, outliers, ICC, CFA, mixed Likert families, find_embu_columns, PII removal, or EMBU v2.0 validation."
argument-hint: "EMBU audit focus, e.g. Stage 1 outliers, Likert conversion, family wide output, CFA/ICC checks, v2.0 decision status"
---
# EMBU Data Audit

Use this skill for EMBU pipeline review, verification, or narrow fixes. The current project status is important: EMBU data architecture v2.0 is active. Previous inactive-status language was an obsolete artifact; CSV headers are treated as mislabeled, PDF is canonical, and the separate field-validation phase is no longer required.

## Load First

Read these files before making claims or edits:

- [AGENTS.md](../../../AGENTS.md)
- [CLAUDE.md](../../../CLAUDE.md)
- [docs/veri-duzenleme/EMBU_C_VERI_MIMARISI.md](../../../docs/veri-duzenleme/EMBU_C_VERI_MIMARISI.md)
- [docs/veri-duzenleme/EMBU_P_VERI_MIMARISI.md](../../../docs/veri-duzenleme/EMBU_P_VERI_MIMARISI.md)
- [docs/method_archive/2026-04-25_EMBU_LIKERT_STANDARDIZATION_METHOD_NOTE.md](../../../docs/method_archive/2026-04-25_EMBU_LIKERT_STANDARDIZATION_METHOD_NOTE.md)
- [docs/veri-duzenleme/STAGE-4-MAP.md](../../../docs/veri-duzenleme/STAGE-4-MAP.md)

Then inspect the relevant implementation:

- [R/02_embu_stage1.R](../../../R/02_embu_stage1.R)
- [R/03_embu_stage2_likert4.R](../../../R/03_embu_stage2_likert4.R)
- [R/04_embu_stage3_family.R](../../../R/04_embu_stage3_family.R)
- [scripts/R/01_embu_stage1_standardize.R](../../../scripts/R/01_embu_stage1_standardize.R)
- [scripts/R/02_embu_stage2_likert4.R](../../../scripts/R/02_embu_stage2_likert4.R)
- [scripts/R/03_embu_stage3_family.R](../../../scripts/R/03_embu_stage3_family.R)
- [tests/test_embu_stage1.R](../../../tests/test_embu_stage1.R)
- [tests/test_embu_stage2_likert4.R](../../../tests/test_embu_stage2_likert4.R)
- [tests/test_embu_stage3_family.R](../../../tests/test_embu_stage3_family.R)

## Audit Procedure

1. State the audit scope: Stage 1 standardization, Stage 2 Likert conversion, Stage 3 family structure, or Stage 4 psychometrics.
2. Confirm the active v2.0 decision context before interpreting CFA, ICC, or EMBU scale results.
3. Check data-boundary safety: do not expose names, raw rows, credentials, or raw data contents.
4. Verify column discovery through `find_embu_columns()` instead of positional assumptions.
5. Verify Likert handling through `classify_embu_c_likert()` and `mark_mixed_likert_families()`.
6. Verify out-of-range values are converted to `NA` and logged to `outputs/tables/embu_stage1_outliers.csv`.
7. Verify family structure uses `aile_no` x `cocuk_no` and that index/sibling roles are handled in Stage 3.
8. Run the narrowest relevant tests, then broaden only if the changed surface requires it.

## Verification Commands

```bash
Rscript tests/test_embu_stage1.R
Rscript tests/test_embu_stage2_likert4.R
Rscript tests/test_embu_stage3_family.R
Rscript scripts/R/01_embu_stage1_standardize.R
Rscript scripts/R/02_embu_stage2_likert4.R
Rscript scripts/R/03_embu_stage3_family.R
```

Use runner scripts only when the user asks for regeneration or when verification genuinely requires regenerated artifacts.

## Response Shape

Return:

- Scope audited.
- Files inspected.
- Findings ordered by severity.
- Whether any active v2.0 decision caveats affect interpretation.
- Tests or commands run.
- Any residual uncertainty requiring additional documentation, code, or field-record review.
