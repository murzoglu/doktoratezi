# T1DM Karma Tez Cross-Repo Status

Generated: `2026-07-09`
Qualitative repo: `niteliksel/`
Quantitative repo: repository root

## Thesis Writing System
Root: `tez-yazim/`
Entrypoint: `tez-yazim/README.md`
Official sources: `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf`, `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx`
Format contract: `tez-yazim/00_kaynak-kurallari/format-kontrati.md`
Tool architecture: `tez-yazim/01_mimari/yetkinlik-ve-arac-mimarisi.md`
Integration plan: `tez-yazim/01_mimari/iki-repo-entegrasyon-plani.md`

## Required Source Files
| Arm | Exists | Path | Purpose | Read mode |
|---|---:|---|---|---|
| qualitative | yes | `CLAUDE.md` | qualitative-arm identity, privacy boundary, active files | read metadata or cited sections only |
| qualitative | yes | `AGENTS.md` | repo-local agent priority and tool policy | read metadata or cited sections only |
| qualitative | yes | `00_context/TRACKER.md` | live phase state and completed qualitative work | read metadata or cited sections only |
| qualitative | yes | `00_context/REPO_CONTEXT.md` | qualitative repo architecture and canonical files | read metadata or cited sections only |
| qualitative | yes | `00_context/CODEX_PLAYBOOK.md` | primary Codex operating playbook | read metadata or cited sections only |
| qualitative | yes | `03_analysis/codebook/codebook_v3.md` | current code/theme mapping | read metadata or cited sections only |
| qualitative | yes | `03_analysis/methodology/coreq_32_completed.md` | COREQ evidence pack | read metadata or cited sections only |
| qualitative | yes | `03_analysis/methodology/audit_trail.md` | methodological decisions and audit trail | read metadata or cited sections only |
| qualitative | yes | `03_analysis/methodology/llm_use_statement.md` | LLM use statement | read metadata or cited sections only |
| qualitative | yes | `02_processed/cleaned_text/thesis_qualitative_cleaned_current.md` | active cleaned qualitative writing source | targeted section reads only; never dump long excerpts |
| quantitative | yes | `CLAUDE.md` | quantitative-arm identity and active analysis status | read metadata or cited sections only |
| quantitative | yes | `AGENTS.md` | repo-local R/Quarto agent policy | read metadata or cited sections only |
| quantitative | yes | `CONVENTIONS.md` | session-injected AI/tool operating policy | read metadata or cited sections only |
| quantitative | yes | `tez-yazim/README.md` | official guide-centered thesis writing entrypoint | read metadata or cited sections only |
| quantitative | yes | `tez-yazim/00_kaynak-kurallari/format-kontrati.md` | Marmara guide-derived thesis format contract | read metadata or cited sections only |
| quantitative | yes | `tez-yazim/01_mimari/yetkinlik-ve-arac-mimarisi.md` | tool, plugin, MCP, and validation architecture for thesis writing | read metadata or cited sections only |
| quantitative | yes | `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf` | official Marmara thesis writing guide | read metadata and extracted rule sections only; do not modify |
| quantitative | yes | `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx` | official Marmara thesis templates | read template structure only; do not modify |
| quantitative | yes | `_targets.R` | targets pipeline map | read metadata or cited sections only |
| quantitative | yes | `thesis.qmd` | Quarto root document | read metadata or cited sections only |
| quantitative | yes | `chapters/01_giris_ve_amac.qmd` | introduction and aims chapter source | read metadata or cited sections only |
| quantitative | yes | `chapters/02_genel_bilgiler.qmd` | background chapter source | read metadata or cited sections only |
| quantitative | yes | `chapters/03_gerec_ve_yontem.qmd` | methods chapter source | read metadata or cited sections only |
| quantitative | yes | `chapters/04_bulgular.qmd` | results chapter source | read metadata or cited sections only |
| quantitative | yes | `chapters/05_tartisma_ve_sonuc.qmd` | discussion and conclusion chapter source | read metadata or cited sections only |
| quantitative | yes | `docs/CLINICAL-STUDY-REPORT-FINAL.md` | clinical study report summary | read metadata or cited sections only |
| quantitative | yes | `docs/analiz_planlari/03-sap-ana-plan.md` | primary SAP | read metadata or cited sections only |
| quantitative | yes | `docs/analiz_planlari/04-sap-faz2-posthoc.md` | Phase II/post-hoc SAP | read metadata or cited sections only |
| quantitative | yes | `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md` | canonical variable map | read metadata or cited sections only |
| quantitative | yes | `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` | canonical analysis-base lock | existence/hash-contract check only; do not print data rows |

## Protected Boundaries
- `niteliksel/`: `01_raw_data/`, `02_processed/transcripts/`, `01_deidentified/`, `00_raw_locked/`, `.remember/`
- repository root: `data/raw/`, `data/identified/`, `data/cleaned/`, `data/backup/`, `data/processed/*`, `outputs/*`, `_targets/`

## Thesis Writing Lanes
### GİRİŞ ve AMAÇ + GENEL BİLGİLER
Qualitative sources: `03_analysis/methodology/A9_triadic_methodology_literature.md`, `03_analysis/methodology/A1_information_power.md`, `03_analysis/codebook/codebook_v3.md`
Quantitative sources: `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md`, `tez-yazim/03_bolum-hazirlik/02_genel-bilgiler.md`, `docs/CLINICAL-STUDY-REPORT-FINAL.md`, `docs/analiz_planlari/03-sap-ana-plan.md`
External/tool gate: Anamnesis context + Evidentia D0-D6 + Anna's full-text + Zotero + dual AI-reliability

### GEREÇ ve YÖNTEM
Qualitative sources: `03_analysis/methodology/coreq_32_completed.md`, `03_analysis/methodology/audit_trail.md`, `03_analysis/methodology/positionality_OM.md`, `03_analysis/methodology/positionality_BA.md`
Quantitative sources: `tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md`, `_targets.R`, `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`, `docs/analiz_planlari/18-raporlama-standartlari-checklist.md`
External/tool gate: Anamnesis context + COREQ/SRQR/JARS-Qual + statistical reporting standards as needed

### BULGULAR
Qualitative sources: `03_analysis/codebook/codebook_v3.md`, `04_triadic_matrices/triadic_matrix_from_cleaned_thesis.csv`, `07_reports/quote_integrity_report.md`
Quantitative sources: `tez-yazim/03_bolum-hazirlik/04_bulgular.md`, `chapters/04_bulgular.qmd`, `outputs/tables/`, `outputs/figures/`
External/tool gate: Repo artifacts by default; if any external citation appears, Anna's full-text + Zotero + dual AI-reliability

### TARTIŞMA ve SONUÇ
Qualitative sources: `03_analysis/methodology/defense_arguments.md`, `03_analysis/methodology/audit_trail.md`, `07_reports/negative_case_review_plan.md`
Quantitative sources: `tez-yazim/03_bolum-hazirlik/05_tartisma-ve-sonuc.md`, `chapters/05_tartisma_ve_sonuc.qmd`, `docs/analiz_planlari/04-sap-faz2-posthoc.md`
External/tool gate: Anamnesis context + Evidentia + Anna's full-text + Zotero + dual AI-reliability; keep causality separated from qualitative themes

### KAYNAKLAR ve EKLER
Qualitative sources: `03_analysis/methodology/llm_use_statement.md`, `03_analysis/methodology/coreq_32_completed.md`, `03_analysis/reflexive/journal_excerpts.md`
Quantitative sources: `tez-yazim/03_bolum-hazirlik/06_kaynaklar-ekler.md`, `references/references.bib`, `references/apa.csl`
External/tool gate: Anna's full-text ledger first; Zotero reference-library reconciliation second; dual AI-reliability final

## Routing Commands
- `cd "$(git rev-parse --show-toplevel)" && test -f tez-yazim/README.md`
- `./dmnitel ai-context`
- `./dmnitel route-tool --query "<soru>"`
- `./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md`
- `python3 .codex/tools/codex_mcp_roster_redacted.py`

## Validation Commands
- qualitative local toolkit: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`
- qualitative AI reliability plugin: `PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py`
- qualitative offline promptfoo gate: `npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml`
- quantitative AI reliability plugin: `PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py` (cwd: repository root)
- reference full-text ledger unresolved-state check: `rg -n 'full-text-pending|zotero-pending|reliability-pending|citation-without-full-text' tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` (cwd: repository root)
- quantitative canonical lock: `Rscript tests/test_reproducibility_lock.R` (cwd: repository root)
- quantitative canonical loading: `Rscript tests/test_final_reference_loading.R` (cwd: repository root)
- quantitative data governance: `Rscript tests/test_data_governance.R` (cwd: repository root)

## Operating Rule
Use this status as an orientation artifact only. It does not authorize raw-data reads,
row-level summaries, Zotero writes/imports, production deploys, or broad git staging.
