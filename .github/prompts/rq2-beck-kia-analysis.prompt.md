---
description: "Plan or draft the active RQ2 analysis for Beck Depression and KIA/SRQ in this thesis repository, using existing R/Quarto conventions while preserving active EMBU v2.0 decisions."
name: "RQ2 Beck KIA Analysis Checklist"
argument-hint: "Optional focus, e.g. descriptive table, missing data, regression model, Quarto results draft"
agent: "agent"
---
# RQ2 Beck KIA Analysis Checklist

Use this prompt to plan or draft work for the active RQ2 stream: Beck Depression and KIA/SRQ analyses.

First read:

- [AGENTS.md](../../AGENTS.md)
- [CLAUDE.md](../../CLAUDE.md)
- Relevant code in [R/](../../R/) and [scripts/R/](../../scripts/R/)
- Current thesis result text in [chapters/03_bulgular.qmd](../../chapters/03_bulgular.qmd), if the task touches reporting

User focus: `${input:focus:What RQ2 analysis or output should be planned/drafted?}`

Produce a concise, implementable checklist with:

1. Data sources and variables to inspect.
2. Required cleaning or validation steps, including out-of-range Beck or KIA/SRQ values.
3. Suggested descriptive tables and figures.
4. Candidate statistical models with assumptions and covariates.
5. Exact R/Quarto files likely to change.
6. Minimal verification commands.

Constraints:

- Treat EMBU as an active v2.0 data pipeline. Do not change EMBU artifacts from this RQ2 prompt unless the user explicitly asks for an EMBU-related change.
- Keep raw data and PII out of the response.
- Prefer repo-local conventions over new analysis architecture.
- If code changes are requested, preserve the [R/](../../R/) pure-function and [scripts/R/](../../scripts/R/) runner split.
