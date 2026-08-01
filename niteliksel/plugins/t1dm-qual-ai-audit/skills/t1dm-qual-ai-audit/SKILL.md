---
name: t1dm-qual-ai-audit
description: Repo-aware AI reliability audit workflow for the T1DM Niteliksel qualitative thesis repository. Use when Codex needs to review, tune, or run qualitative-arm AI safety, hooks, MCP routing, Evidentia integration, raw-data boundaries, COREQ/RTA/codebook traceability, or cross-repo coordination with the quantitative nicel kök.
---

# T1DM Qual AI Audit

Use this skill for the qualitative arm of the T1DM mixed-methods thesis. It does not replace
qualitative methodology judgement; it enforces source grounding, privacy boundaries, and tool routing.

## Workflow

1. Read `CLAUDE.md`, `00_context/TRACKER.md`, `00_context/REPO_CONTEXT.md`, and
   `00_context/CODEX_PLAYBOOK.md` first.
2. Preserve protected data boundaries: do not print or export raw interview DOCX, merged transcripts,
   demographic rows, consent/protocol personal content, `.remember/`, or family-level sensitive detail.
3. For thesis writing, format, official section order, summary/ozet, table/figure, or references work,
   use `/workspaces/T1DM-Tez/tez-yazim/README.md` and the official
   `/workspaces/T1DM-Tez/docs/tez-kilavuz` sources as the top writing gate.
4. Establish the tool surface with `./dmnitel ai-context`; for ambiguous requests run
   `./dmnitel route-tool --query "<soru>"` before selecting MCPs.
5. For local qualitative tooling, prefer `dm_niteliksel_toolkit` and `./dmnitel`; for tests use
   `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`.
6. For external literature, use `.claude/evidentia.local.md` routing and Evidentia MCP core.
7. For biomedical entity/data lanes (genetics, variants, proteins, pathways, pharmacology,
   clinical trials, omics datasets, mechanistic T1DM biology), add the conditional
   `life-science-research:research-router-skill` layer.
8. For reference-library, citation key, BibTeX/RIS, `references.bib`, or Zotero full-text
   index work, use `zotero:Zotero`. For headless search/export, check
   `python3 scripts/util/zotero_env_bridge.py status --json` first; it loads `ZOTERO_API_KEY`
   from `.env` and must never print the key. Use the Desktop helper only for local full-text,
   attachment, or connector workflows. Require confirmation for Zotero writes/imports.
9. For quantitative H1-H5/EMBU/Beck/KIA/R-pipeline questions, switch to the nicel kök
   `/workspaces/T1DM-Tez`, `tez-yazim`, and `t1dm-tez-rehberi`.
10. For MCP checks, use `python3 .codex/tools/codex_mcp_roster_redacted.py`; never raw
   `codex mcp list`.
11. After external Evidentia/Codex/MCP/plugin use, record the operation with `./dmnitel log-ai-use`.

## Audit Rules

- Qualitative claims need a checked repo artifact: codebook v2, COREQ checklist, audit trail,
  methodology pack, tracker, or cleaned thesis text.
- External claims need primary literature or official reporting standards.
- RTA language must not imply positivist saturation or inter-coder reliability unless explicitly
  framed as non-RTA supplementary analysis.
- Cross-repo synthesis must separate qualitative themes from quantitative estimates and preserve
  the mixed-methods interpretation layer.
- Official Marmara thesis guide/template rules override older repo notes for section order, decimal
  comma, table/figure placement, summary structure, and reference-list format.
- `dmnitel route-tool` recommendations are routing evidence, not a substitute for researcher judgement.
- Life Science Research mechanistic evidence must not be used to overstate causality for qualitative
  psychosocial themes.
- Zotero item keys and BibTeX citation keys are different; report which one is used when inserting
  or exporting citations.

## Validation Commands

```bash
./dmnitel ai-context
./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md
./dmnitel route-tool --query "Marmara tez yazım formatı ve joint display"
./dmnitel route-tool --query "RTA bilgi gücü için PubMed tam metin taraması"
./dmnitel route-tool --query "HLA genetik mekanizma ve references.bib Zotero eşitleme"
python3 scripts/util/zotero_env_bridge.py status --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
python3 .codex/tools/codex_mcp_roster_redacted.py
python3 -m py_compile .codex/hooks/*.py .codex/tools/codex_mcp_roster_redacted.py
```
