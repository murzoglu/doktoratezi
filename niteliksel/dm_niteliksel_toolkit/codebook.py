from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .common import AI_SAFETY_STATEMENT, normalize_key, normalize_space, read_csv, safe_write_csv


CODEBOOK_FIELDS = [
    "code_id",
    "code_name",
    "definition",
    "include_criteria",
    "exclude_criteria",
    "example_quote_id",
    "theme",
    "subtheme",
    "memo",
    "version",
    "date",
]

VAGUE_CODE_NAMES = {
    "guzel ifade",
    "güzel ifade",
    "onemli",
    "önemli",
    "anne soyledi",
    "anne söyledi",
    "kardes problemi",
    "kardeş problemi",
    "diyabet etkisi",
}

OVERINTERPRETATION_TERMS = {
    "kesinlikle",
    "kanıtlar",
    "kanıtlıyor",
    "travma",
    "patoloji",
    "bilinçdışı",
    "inkar",
    "manipulasyon",
}

QUOTE_ID_PLACEHOLDER_TERMS = {
    "researcher_to_assign",
    "tbd",
    "todo",
    "belirlenecek",
    "atanacak",
    "placeholder",
}


@dataclass(frozen=True)
class Issue:
    severity: str
    row: int | None
    field: str
    message: str
    value: str = ""


def write_codebook_template(path: Path) -> bool:
    return safe_write_csv(path, CODEBOOK_FIELDS, [])


def lint_codebook(path: Path) -> list[Issue]:
    rows = read_csv(path)
    issues: list[Issue] = []

    for index, row in enumerate(rows, start=2):
        code_name = normalize_space(row.get("code_name", ""))
        definition = normalize_space(row.get("definition", ""))
        include_criteria = normalize_space(row.get("include_criteria", ""))
        exclude_criteria = normalize_space(row.get("exclude_criteria", ""))
        example_quote_id = normalize_space(row.get("example_quote_id", ""))
        theme = normalize_space(row.get("theme", ""))
        subtheme = normalize_space(row.get("subtheme", ""))

        if not code_name:
            issues.append(Issue("critical", index, "code_name", "Boş kod adı kontrol edilmelidir."))
        if not definition:
            issues.append(Issue("warning", index, "definition", "Kod tanımı eksik; araştırmacı kararı gerektirir."))
        if not include_criteria:
            issues.append(Issue("warning", index, "include_criteria", "Dahil etme ölçütü eksik olabilir."))
        if not exclude_criteria:
            issues.append(Issue("warning", index, "exclude_criteria", "Hariç tutma ölçütü eksik olabilir."))
        if not example_quote_id:
            issues.append(Issue("warning", index, "example_quote_id", "En az bir örnek alıntı ID'si eklenmelidir."))
        elif any(term in normalize_key(example_quote_id) for term in QUOTE_ID_PLACEHOLDER_TERMS):
            issues.append(
                Issue(
                    "warning",
                    index,
                    "example_quote_id",
                    "Örnek alıntı ID'si placeholder görünüyor; kaynak alıntı kaydıyla doğrulanmalıdır.",
                    example_quote_id,
                )
            )
        if not theme and not subtheme:
            issues.append(Issue("warning", index, "theme", "Kod bir tema veya alt tema ile ilişkilendirilmelidir."))

        if normalize_key(code_name) in VAGUE_CODE_NAMES:
            issues.append(
                Issue(
                    "warning",
                    index,
                    "code_name",
                    "Kod adı betimleyici ama analitik olarak belirsiz olabilir.",
                    code_name,
                )
            )

        if code_name and normalize_key(code_name) in {normalize_key(theme), normalize_key(subtheme)}:
            issues.append(
                Issue(
                    "warning",
                    index,
                    "code_name",
                    "Kod düzeyi tema/alt tema düzeyiyle karışıyor olabilir.",
                    code_name,
                )
            )

        definition_key = normalize_key(definition)
        matched_terms = [term for term in OVERINTERPRETATION_TERMS if term in definition_key]
        if matched_terms:
            issues.append(
                Issue(
                    "suggestion",
                    index,
                    "definition",
                    "Kod tanımı katılımcı verisinin ötesine aşırı yorum yüklüyor olabilir.",
                    ", ".join(sorted(matched_terms)),
                )
            )

    issues.extend(_duplicate_code_name_issues(rows))
    issues.extend(_quote_theme_overlap_issues(rows))
    return issues


def _duplicate_code_name_issues(rows: list[dict[str, str]]) -> list[Issue]:
    by_name: dict[str, dict[str, set[str] | list[int]]] = defaultdict(lambda: {"definitions": set(), "rows": []})
    for index, row in enumerate(rows, start=2):
        name = normalize_key(row.get("code_name", ""))
        if not name:
            continue
        by_name[name]["definitions"].add(normalize_key(row.get("definition", "")))  # type: ignore[index]
        by_name[name]["rows"].append(index)  # type: ignore[index]

    issues: list[Issue] = []
    for name, data in by_name.items():
        definitions = data["definitions"]
        rows_for_name = data["rows"]
        if len(rows_for_name) > 1 and len(definitions) > 1:  # type: ignore[arg-type]
            issues.append(
                Issue(
                    "warning",
                    None,
                    "code_name",
                    "Aynı kod adı farklı tanımlarla tekrar ediyor olabilir.",
                    f"{name} (satırlar: {', '.join(map(str, rows_for_name))})",
                )
            )
    return issues


def _quote_theme_overlap_issues(rows: list[dict[str, str]]) -> list[Issue]:
    by_quote: dict[str, list[tuple[int, str, str]]] = defaultdict(list)
    for index, row in enumerate(rows, start=2):
        quote_id = normalize_space(row.get("example_quote_id", ""))
        if not quote_id:
            continue
        theme = normalize_space(row.get("theme", ""))
        memo = normalize_key(row.get("memo", ""))
        by_quote[quote_id].append((index, theme, memo))

    issues: list[Issue] = []
    for quote_id, assignments in by_quote.items():
        themes = {normalize_key(theme) for _, theme, _ in assignments if theme}
        has_justification = any("gerek" in memo or "karar" in memo for _, _, memo in assignments)
        if len(themes) > 1 and not has_justification:
            rows_for_quote = ", ".join(str(index) for index, _, _ in assignments)
            issues.append(
                Issue(
                    "warning",
                    None,
                    "example_quote_id",
                    "Aynı alıntı birden fazla temaya gerekçesiz atanmış olabilir.",
                    f"{quote_id} (satırlar: {rows_for_quote})",
                )
            )
    return issues


def write_codebook_report(issues: list[Issue], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    grouped = {level: [issue for issue in issues if issue.severity == level] for level in ("critical", "warning", "suggestion")}
    lines = [
        "# Kod Kitabı Tutarlılık Raporu",
        "",
        AI_SAFETY_STATEMENT,
        "",
        "## Kritik Bulgular",
        "",
        _format_issue_list(grouped["critical"]),
        "",
        "## Uyarılar",
        "",
        _format_issue_list(grouped["warning"]),
        "",
        "## Öneriler",
        "",
        _format_issue_list(grouped["suggestion"]),
        "",
        "## Kontrol Edilmesi Gereken Kodlar",
        "",
        "Rapor, kesin bir analitik karar üretmez. Listelenen maddeler araştırmacı tarafından kontrol edilmelidir.",
        "",
        "## Araştırmacı Kararı İçin Notlar",
        "",
        "Tema geliştirme, kod revizyonu ve nihai yorumlama araştırmacı sorumluluğundadır.",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def _format_issue_list(issues: list[Issue]) -> str:
    if not issues:
        return "- Bu düzeyde bulgu saptanmadı."
    lines = []
    for issue in issues:
        location = f"satır {issue.row}, `{issue.field}`" if issue.row else f"`{issue.field}`"
        value = f" ({issue.value})" if issue.value else ""
        lines.append(f"- {location}: {issue.message}{value}")
    return "\n".join(lines)
