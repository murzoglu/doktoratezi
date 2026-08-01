from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from .anonymization import assert_not_protected_write


QUAL_REPO = Path(__file__).resolve().parents[1]
QUANT_REPO = Path("/workspaces/T1DM-Tez")
THESIS_WRITING_ROOT = QUANT_REPO / "tez-yazim"


@dataclass(frozen=True)
class RequiredFile:
    arm: str
    path: str
    purpose: str
    read_mode: str = "read metadata or cited sections only"

    def absolute_path(self) -> Path:
        repo = QUAL_REPO if self.arm == "qualitative" else QUANT_REPO
        return repo / self.path

    def as_dict(self) -> dict[str, Any]:
        absolute = self.absolute_path()
        return {
            "arm": self.arm,
            "path": self.path,
            "absolute_path": str(absolute),
            "purpose": self.purpose,
            "read_mode": self.read_mode,
            "exists": absolute.exists(),
        }


QUAL_REQUIRED_FILES = [
    RequiredFile("qualitative", "CLAUDE.md", "qualitative-arm identity, privacy boundary, active files"),
    RequiredFile("qualitative", "AGENTS.md", "repo-local agent priority and tool policy"),
    RequiredFile("qualitative", "00_context/TRACKER.md", "live phase state and completed qualitative work"),
    RequiredFile("qualitative", "00_context/REPO_CONTEXT.md", "qualitative repo architecture and canonical files"),
    RequiredFile("qualitative", "00_context/CODEX_PLAYBOOK.md", "primary Codex operating playbook"),
    RequiredFile("qualitative", "03_analysis/codebook/codebook_v2.md", "current code/theme mapping"),
    RequiredFile("qualitative", "03_analysis/methodology/coreq_32_completed.md", "COREQ evidence pack"),
    RequiredFile("qualitative", "03_analysis/methodology/audit_trail.md", "methodological decisions and audit trail"),
    RequiredFile("qualitative", "03_analysis/methodology/llm_use_statement.md", "LLM use statement"),
    RequiredFile(
        "qualitative",
        "02_processed/cleaned_text/thesis_qualitative_cleaned_current.md",
        "active cleaned qualitative writing source",
        "targeted section reads only; never dump long excerpts",
    ),
]

QUANT_REQUIRED_FILES = [
    RequiredFile("quantitative", "CLAUDE.md", "quantitative-arm identity and active analysis status"),
    RequiredFile("quantitative", "AGENTS.md", "repo-local R/Quarto agent policy"),
    RequiredFile("quantitative", "CONVENTIONS.md", "session-injected AI/tool operating policy"),
    RequiredFile("quantitative", "tez-yazim/README.md", "official guide-centered thesis writing entrypoint"),
    RequiredFile(
        "quantitative",
        "tez-yazim/00_kaynak-kurallari/format-kontrati.md",
        "Marmara guide-derived thesis format contract",
    ),
    RequiredFile(
        "quantitative",
        "tez-yazim/01_mimari/yetkinlik-ve-arac-mimarisi.md",
        "tool, plugin, MCP, and validation architecture for thesis writing",
    ),
    RequiredFile(
        "quantitative",
        "docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf",
        "official Marmara thesis writing guide",
        "read metadata and extracted rule sections only; do not modify",
    ),
    RequiredFile(
        "quantitative",
        "docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx",
        "official Marmara thesis templates",
        "read template structure only; do not modify",
    ),
    RequiredFile("quantitative", "_targets.R", "targets pipeline map"),
    RequiredFile("quantitative", "thesis.qmd", "Quarto root document"),
    RequiredFile("quantitative", "chapters/01_giris_ve_amac.qmd", "introduction and aims chapter source"),
    RequiredFile("quantitative", "chapters/02_genel_bilgiler.qmd", "background chapter source"),
    RequiredFile("quantitative", "chapters/03_gerec_ve_yontem.qmd", "methods chapter source"),
    RequiredFile("quantitative", "chapters/04_bulgular.qmd", "results chapter source"),
    RequiredFile("quantitative", "chapters/05_tartisma_ve_sonuc.qmd", "discussion and conclusion chapter source"),
    RequiredFile("quantitative", "docs/CLINICAL-STUDY-REPORT-FINAL.md", "clinical study report summary"),
    RequiredFile("quantitative", "docs/analiz_planlari/03-sap-ana-plan.md", "primary SAP"),
    RequiredFile("quantitative", "docs/analiz_planlari/04-sap-faz2-posthoc.md", "Phase II/post-hoc SAP"),
    RequiredFile(
        "quantitative",
        "docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md",
        "canonical variable map",
    ),
    RequiredFile(
        "quantitative",
        "data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock",
        "canonical analysis-base lock",
        "existence/hash-contract check only; do not print data rows",
    ),
]

PROTECTED_BOUNDARIES = [
    {
        "repo": str(QUAL_REPO),
        "paths": [
            "01_raw_data/",
            "02_processed/transcripts/",
            "01_deidentified/",
            "00_raw_locked/",
            ".remember/",
        ],
    },
    {
        "repo": str(QUANT_REPO),
        "paths": [
            "data/raw/",
            "data/identified/",
            "data/cleaned/",
            "data/backup/",
            "data/processed/*",
            "outputs/*",
            "_targets/",
        ],
    },
]

THESIS_LANES = [
    {
        "chapter": "GİRİŞ ve AMAÇ + GENEL BİLGİLER",
        "qualitative_sources": [
            "03_analysis/methodology/A9_triadic_methodology_literature.md",
            "03_analysis/methodology/A1_information_power.md",
            "03_analysis/codebook/codebook_v2.md",
        ],
        "quantitative_sources": [
            "tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md",
            "tez-yazim/03_bolum-hazirlik/02_genel-bilgiler.md",
            "docs/CLINICAL-STUDY-REPORT-FINAL.md",
            "docs/analiz_planlari/03-sap-ana-plan.md",
        ],
        "external_gate": "Anamnesis context + Evidentia D0-D6 + Anna's full-text + Zotero + dual AI-reliability",
    },
    {
        "chapter": "GEREÇ ve YÖNTEM",
        "qualitative_sources": [
            "03_analysis/methodology/coreq_32_completed.md",
            "03_analysis/methodology/audit_trail.md",
            "03_analysis/methodology/positionality_OM.md",
            "03_analysis/methodology/positionality_BA.md",
        ],
        "quantitative_sources": [
            "tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md",
            "_targets.R",
            "docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md",
            "docs/analiz_planlari/18-raporlama-standartlari-checklist.md",
        ],
        "external_gate": "Anamnesis context + COREQ/SRQR/JARS-Qual + statistical reporting standards as needed",
    },
    {
        "chapter": "BULGULAR",
        "qualitative_sources": [
            "03_analysis/codebook/codebook_v2.md",
            "04_triadic_matrices/triadic_matrix_from_cleaned_thesis.csv",
            "07_reports/quote_integrity_report.md",
        ],
        "quantitative_sources": [
            "tez-yazim/03_bolum-hazirlik/04_bulgular.md",
            "chapters/04_bulgular.qmd",
            "outputs/tables/",
            "outputs/figures/",
        ],
        "external_gate": "Repo artifacts by default; if any external citation appears, Anna's full-text + Zotero + dual AI-reliability",
    },
    {
        "chapter": "TARTIŞMA ve SONUÇ",
        "qualitative_sources": [
            "03_analysis/methodology/defense_arguments.md",
            "03_analysis/methodology/audit_trail.md",
            "07_reports/negative_case_review_plan.md",
        ],
        "quantitative_sources": [
            "tez-yazim/03_bolum-hazirlik/05_tartisma-ve-sonuc.md",
            "chapters/05_tartisma_ve_sonuc.qmd",
            "docs/analiz_planlari/04-sap-faz2-posthoc.md",
        ],
        "external_gate": "Anamnesis context + Evidentia + Anna's full-text + Zotero + dual AI-reliability; keep causality separated from qualitative themes",
    },
    {
        "chapter": "KAYNAKLAR ve EKLER",
        "qualitative_sources": [
            "03_analysis/methodology/llm_use_statement.md",
            "03_analysis/methodology/coreq_32_completed.md",
            "03_analysis/reflexive/journal_excerpts.md",
        ],
        "quantitative_sources": [
            "tez-yazim/03_bolum-hazirlik/06_kaynaklar-ekler.md",
            "references/references.bib",
            "references/apa.csl",
        ],
        "external_gate": "Anna's full-text ledger first; Zotero reference-library reconciliation second; dual AI-reliability final",
    },
]

VALIDATION_COMMANDS = [
    {
        "scope": "qualitative local toolkit",
        "command": "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests",
    },
    {
        "scope": "qualitative AI reliability plugin",
        "command": "PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py",
    },
    {
        "scope": "qualitative offline promptfoo gate",
        "command": "npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml",
    },
    {
        "scope": "quantitative AI reliability plugin",
        "command": "PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py",
        "cwd": str(QUANT_REPO),
    },
    {
        "scope": "reference full-text ledger unresolved-state check",
        "command": "rg -n 'full-text-pending|zotero-pending|reliability-pending|citation-without-full-text' tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md",
        "cwd": str(QUANT_REPO),
        "expected": "exit 1 after the ledger file exists; unresolved reference states must be absent",
    },
    {
        "scope": "quantitative canonical lock",
        "command": "Rscript tests/test_reproducibility_lock.R",
        "cwd": str(QUANT_REPO),
    },
    {
        "scope": "quantitative canonical loading",
        "command": "Rscript tests/test_final_reference_loading.R",
        "cwd": str(QUANT_REPO),
    },
    {
        "scope": "quantitative data governance",
        "command": "Rscript tests/test_data_governance.R",
        "cwd": str(QUANT_REPO),
    },
]


def build_cross_repo_status(output_format: str = "markdown") -> str:
    data = {
        "generated_on": date.today().isoformat(),
        "qualitative_repo": str(QUAL_REPO),
        "quantitative_repo": str(QUANT_REPO),
        "required_files": [item.as_dict() for item in QUAL_REQUIRED_FILES + QUANT_REQUIRED_FILES],
        "protected_boundaries": PROTECTED_BOUNDARIES,
        "thesis_writing_system": {
            "root": str(THESIS_WRITING_ROOT),
            "entrypoint": "tez-yazim/README.md",
            "official_sources": [
                "docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf",
                "docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx",
            ],
            "format_contract": "tez-yazim/00_kaynak-kurallari/format-kontrati.md",
            "tool_architecture": "tez-yazim/01_mimari/yetkinlik-ve-arac-mimarisi.md",
            "integration_plan": "tez-yazim/01_mimari/iki-repo-entegrasyon-plani.md",
        },
        "thesis_lanes": THESIS_LANES,
        "validation_commands": VALIDATION_COMMANDS,
        "routing_commands": [
            "cd /workspaces/T1DM-Tez && test -f tez-yazim/README.md",
            "./dmnitel ai-context",
            './dmnitel route-tool --query "<soru>"',
            "./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md",
            "python3 .codex/tools/codex_mcp_roster_redacted.py",
        ],
    }
    if output_format == "json":
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if output_format != "markdown":
        raise ValueError("format markdown veya json olmalıdır.")
    return _render_markdown(data)


def write_cross_repo_status(content: str, output: str | None) -> None:
    if output:
        path = Path(output)
        assert_not_protected_write(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Rapor yazıldı: {path}")
        return
    print(content, end="")


def _render_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# T1DM Karma Tez Cross-Repo Status",
        "",
        f"Generated: `{data['generated_on']}`",
        f"Qualitative repo: `{data['qualitative_repo']}`",
        f"Quantitative repo: `{data['quantitative_repo']}`",
        "",
        "## Thesis Writing System",
        f"Root: `{data['thesis_writing_system']['root']}`",
        f"Entrypoint: `{data['thesis_writing_system']['entrypoint']}`",
        "Official sources: "
        + ", ".join(f"`{path}`" for path in data["thesis_writing_system"]["official_sources"]),
        f"Format contract: `{data['thesis_writing_system']['format_contract']}`",
        f"Tool architecture: `{data['thesis_writing_system']['tool_architecture']}`",
        f"Integration plan: `{data['thesis_writing_system']['integration_plan']}`",
        "",
        "## Required Source Files",
        "| Arm | Exists | Path | Purpose | Read mode |",
        "|---|---:|---|---|---|",
    ]
    for item in data["required_files"]:
        exists = "yes" if item["exists"] else "no"
        lines.append(
            f"| {item['arm']} | {exists} | `{item['path']}` | {item['purpose']} | {item['read_mode']} |"
        )

    lines.extend(["", "## Protected Boundaries"])
    for boundary in data["protected_boundaries"]:
        lines.append(f"- `{boundary['repo']}`: " + ", ".join(f"`{path}`" for path in boundary["paths"]))

    lines.extend(["", "## Thesis Writing Lanes"])
    for lane in data["thesis_lanes"]:
        lines.append(f"### {lane['chapter']}")
        lines.append("Qualitative sources: " + ", ".join(f"`{path}`" for path in lane["qualitative_sources"]))
        lines.append("Quantitative sources: " + ", ".join(f"`{path}`" for path in lane["quantitative_sources"]))
        lines.append(f"External/tool gate: {lane['external_gate']}")
        lines.append("")

    lines.extend(["## Routing Commands"])
    lines.extend(f"- `{command}`" for command in data["routing_commands"])

    lines.extend(["", "## Validation Commands"])
    for item in data["validation_commands"]:
        cwd = f" (cwd `{item['cwd']}`)" if item.get("cwd") else ""
        lines.append(f"- {item['scope']}: `{item['command']}`{cwd}")

    lines.extend(
        [
            "",
            "## Operating Rule",
            "Use this status as an orientation artifact only. It does not authorize raw-data reads,",
            "row-level summaries, Zotero writes/imports, production deploys, or broad git staging.",
        ]
    )
    return "\n".join(lines) + "\n"
