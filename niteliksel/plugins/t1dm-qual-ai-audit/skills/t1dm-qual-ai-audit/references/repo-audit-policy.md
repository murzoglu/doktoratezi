# T1DM Niteliksel AI Audit Policy

## Scope

This policy adapts the AI reliability scaffold to the T1DM qualitative thesis repo. It protects qualitative research ethics, source grounding, tool routing, and evidence boundaries; it does not replace researcher judgement, thesis-supervisor approval, or reflexive thematic analysis.

## Hard Boundaries

- Do not print, summarize broadly, export, send to MCP/RAG, or add to memory content from `01_raw_data/`, `02_processed/transcripts/`, `.remember/`, `00_raw_locked/`, or `01_deidentified/`.
- Do not expose family-level demographic rows, pseudonym maps, consent/protocol personal content, or raw participant quotes.
- Use only researcher-selected anonymized quote IDs / family-role labels when quote work is explicitly requested.
- Do not run raw `codex mcp list`; use `python3 .codex/tools/codex_mcp_roster_redacted.py`.
- Do not stage with `git add .`; stage files by name.

## Primary Repo Sources

- Project rules: `CLAUDE.md`, `AGENTS.md`
- Live process: `00_context/TRACKER.md`, `00_context/ROADMAP_v1.md`
- Codex operations: `00_context/CODEX_PLAYBOOK.md`
- Cross-repo thesis writing source: `/mnt/thunderbolt/workspaces/doktoratezi/tez-yazim/README.md`
- Official thesis guide/templates: `/mnt/thunderbolt/workspaces/doktoratezi/docs/tez-kilavuz/`
- Architecture: `00_context/REPO_CONTEXT.md`
- Current analysis: `03_analysis/codebook/codebook_v2.md`, `03_analysis/methodology/*`, `03_analysis/reflexive/*`
- Active thesis writing source: `02_processed/cleaned_text/thesis_qualitative_cleaned_current.md`
- Toolkit and tests: `dm_niteliksel_toolkit/`, `tests/`, `./dmnitel`

## Reliability Gate Expectations

- Qualitative-arm numeric claims such as family count, interview count, code count, theme count, COREQ/SRQR/JARS-Qual item count, and phase/package count need a checked repo source marker.
- RTA language must distinguish information power, reflexivity, and interpretive depth from positivist saturation or inter-coder reliability language.
- Tool routing should prefer local `./dmnitel` for repo checks, Evidentia MCP for external evidence, and the paired quantitative repo only for H1-H5/EMBU/Beck/KIA/R-pipeline claims.
- Thesis writing and formatting should prefer the paired repo `tez-yazim` contract and official Marmara guide/templates before older style notes.
- External MCP use should be followed by `./dmnitel log-ai-use` when it materially informs thesis work.

## Recommended Validation

Use the smallest relevant checks first:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
./dmnitel ai-context
./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md
./dmnitel route-tool --query "COREQ ve alıntı bütünlüğü denetimi"
python3 .codex/tools/codex_mcp_roster_redacted.py
```
