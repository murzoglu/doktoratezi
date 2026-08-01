---
name: doktoratezi-ai-audit
description: Repo-aware AI reliability audit workflow for the /workspaces/T1DM-Tez Quarto/R/targets thesis repository. Use when Codex needs to install, review, tune, or run the ai-audit.zip reliability scaffold; audit LLM-generated claims, citations, hooks, promptfoo evals, or raw-data boundaries; or add source-grounding and verification gates for this T1DM thesis repo.
---

# Doktoratezi AI Audit

## Overview

Use this skill to apply the bundled AI reliability scaffold to the doktoratezi thesis repository without weakening the repo's data-governance boundary. Treat the scaffold as a defense-in-depth aid: it improves consistency, traceability, and catchability, but does not certify statistical or clinical correctness by itself.

## Workflow

1. Read repo grounding first: `AGENTS.md`, `CLAUDE.md`, `CONVENTIONS.md`, `tez-yazim/README.md`,
   `_targets.R`, and the specific `R/`, `scripts/R/`, `tests/`, `docs/tez-kilavuz/`, or
   `docs/protokol/` files involved in the task.
2. Preserve sensitive boundaries: never print, summarize row-level contents from, or add to memory any files under `data/raw/`, `data/identified/`, `data/cleaned/`, `data/backup/`, `data/processed/*`, `outputs/*`, or `_targets/`.
3. For thesis writing and format, use `tez-yazim/README.md` plus the official Marmara sources in
   `docs/tez-kilavuz/`; these override older APA/decimal-dot style notes for final thesis formatting.
4. Use `references/repo-audit-policy.md` when deciding whether a reliability gate is safe for this repo.
5. Do not run `assets/ai-reliability/setup.sh` directly. It is the upstream scaffold and still exposes broad flags such as `--global`. Use `scripts/install_repo_ai_reliability.py` instead.
6. Start materialization with a dry run:

```bash
python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/install_repo_ai_reliability.py
```

7. Apply only after the dry-run output is reviewed:

```bash
python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/install_repo_ai_reliability.py --apply
```

8. Add `--with-ci` only when the user explicitly wants the GitHub Actions reliability gate copied into `.github/workflows/`. Add `--with-observability` only when the user explicitly wants the Langfuse/OTel files materialized.

## Audit Rules

- Prefer primary repo sources for internal facts: `CLAUDE.md`, `AGENTS.md`, `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`, the canonical lock file, `_targets.R`, and the tested `R/` module.
- For clinical/statistical claims, separate repo-derived facts from external medical literature; cite each source tier explicitly when it affects interpretation.
- For code changes, validate with the narrowest relevant test first, then broaden when shared analysis contracts are touched.
- For thesis-output claims, require traceability from source document to R function/test to produced table/figure when possible.
- For thesis-format claims, require traceability to `tez-yazim/00_kaynak-kurallari/` or the official
  `docs/tez-kilavuz` source; do not rely on stale APA/Quarto defaults.
- For AI outputs, treat numeric claims, citations, and "latest" statements as untrusted until checked against a primary source or a dated repo artifact.
- For MCP checks, never use raw `codex mcp list` in this repo. Use `python3 .codex/tools/codex_mcp_roster_redacted.py` so plaintext stdio arguments are redacted before entering the transcript.

## Resources

- `assets/ai-reliability/`: upstream ai-audit scaffold adapted for this repo.
- `scripts/install_repo_ai_reliability.py`: repo-safe materializer with dry-run default and backups on overwrite.
- `scripts/test_repo_ai_reliability.py`: synthetic-event regression test suite for hooks, config, installer drift, and claim checking.
- `references/repo-audit-policy.md`: local policy for data boundaries, verification gates, and recommended validation commands.

## Validation Commands

Run only the commands relevant to the touched surface:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit
python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/install_repo_ai_reliability.py
python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/install_repo_ai_reliability.py --check
python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
python3 .codex/tools/codex_mcp_roster_redacted.py
python3 -m py_compile .codex/hooks/*.py .codex/tools/codex_mcp_roster_redacted.py plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/.codex/hooks/*.py plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/.codex/tools/codex_mcp_roster_redacted.py plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/install_repo_ai_reliability.py
```

After materializing runtime files, run the relevant repo tests such as `Rscript tests/test_reproducibility_lock.R` or the exact `tests/test_*.R` file matching the changed analysis module.
