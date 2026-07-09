from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .common import AI_SAFETY_STATEMENT, normalize_space, read_csv


QUOTE_FIELDS = [
    "quote_id",
    "family_id",
    "participant_role",
    "quote_text_used",
    "manuscript_section",
    "theme",
]

TEXT_SUFFIXES = {".txt", ".md", ".csv", ".tsv"}
ALLOWED_BRACKET_INSERTS = {"[isim]", "[okul adı]", "[şehir]", "[annesi]", "[ablası]", "[…]", "[...]"}


@dataclass(frozen=True)
class QuoteIssue:
    severity: str
    quote_id: str
    message: str


def check_quotes(source_dir: Path, quotes_csv: Path) -> list[QuoteIssue]:
    source_text = _read_source_text(source_dir)
    rows = read_csv(quotes_csv)
    issues: list[QuoteIssue] = []

    by_quote_id: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        quote_id = normalize_space(row.get("quote_id", ""))
        quote_text = normalize_space(row.get("quote_text_used", ""))
        family_id = normalize_space(row.get("family_id", ""))
        by_quote_id[quote_id].add(quote_text)

        if not quote_text:
            issues.append(QuoteIssue("critical", quote_id, "Alıntı metni boş; kontrol edilmelidir."))
            continue

        if quote_text in source_text:
            continue

        bracket_issue = _check_bracket_insertions(quote_text)
        if bracket_issue:
            issues.append(QuoteIssue("warning", quote_id, bracket_issue))

        if _is_allowed_shortening(quote_text, source_text) or _is_allowed_masked_quote(quote_text, source_text):
            continue

        normalized_source = normalize_space(source_text)
        if normalize_space(quote_text) in normalized_source:
            continue

        issues.append(
            QuoteIssue(
                "warning",
                quote_id,
                "Alıntı kaynak dökümde bire bir bulunamadı; köşeli parantez dışı editoryal müdahale olabilir.",
            )
        )

        if family_id and family_id not in quote_id:
            issues.append(
                QuoteIssue(
                    "suggestion",
                    quote_id,
                    "Alıntı ID'si aile bilgisiyle açıkça uyumlu görünmüyor; adlandırma konvansiyonu kontrol edilmelidir.",
                )
            )

    for quote_id, variants in by_quote_id.items():
        if quote_id and len(variants) > 1:
            issues.append(
                QuoteIssue(
                    "warning",
                    quote_id,
                    "Aynı quote_id farklı yerlerde farklı yazılmış olabilir.",
                )
            )

    return issues


def write_quote_report(issues: list[QuoteIssue], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Alıntı Bütünlüğü Raporu",
        "",
        AI_SAFETY_STATEMENT,
        "",
        "## Kritik Bulgular",
        "",
        _format_issues([issue for issue in issues if issue.severity == "critical"]),
        "",
        "## Uyarılar",
        "",
        _format_issues([issue for issue in issues if issue.severity == "warning"]),
        "",
        "## Öneriler",
        "",
        _format_issues([issue for issue in issues if issue.severity == "suggestion"]),
        "",
        "## Araştırmacı Kararı İçin Notlar",
        "",
        "Alıntılar yeniden yazılmamalı; yalnızca izin verilen maskeleme, kısaltma veya açıklayıcı ekler kullanılmalıdır.",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def _read_source_text(source_dir: Path) -> str:
    if source_dir.is_file():
        return source_dir.read_text(encoding="utf-8")
    chunks = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            chunks.append(path.read_text(encoding="utf-16"))
    return "\n".join(chunks)


def _check_bracket_insertions(quote_text: str) -> str:
    inserts = re.findall(r"\[[^\]]+\]", quote_text)
    unexpected = [insert for insert in inserts if insert not in ALLOWED_BRACKET_INSERTS]
    if unexpected:
        return "Beklenmeyen köşeli parantez ekleri araştırmacı tarafından kontrol edilmelidir: " + ", ".join(unexpected)
    return ""


def _is_allowed_shortening(quote_text: str, source_text: str) -> bool:
    if "[…]" not in quote_text and "[...]" not in quote_text:
        return False
    token_pattern = r"\[(?:…|\.\.\.)\]"
    parts = [part for part in re.split(token_pattern, quote_text) if part]
    if not parts:
        return False
    return _parts_appear_in_order(parts, source_text)


def _is_allowed_masked_quote(quote_text: str, source_text: str) -> bool:
    if "[" not in quote_text:
        return False
    parts = [part for part in re.split(r"\[[^\]]+\]", quote_text) if part]
    if not parts:
        return False
    return _parts_appear_in_order(parts, source_text)


def _parts_appear_in_order(parts: list[str], source_text: str) -> bool:
    position = 0
    for part in parts:
        clean = normalize_space(part)
        if not clean:
            continue
        found = source_text.find(clean, position)
        if found < 0:
            return False
        position = found + len(clean)
    return True


def _format_issues(issues: list[QuoteIssue]) -> str:
    if not issues:
        return "- Bu düzeyde bulgu saptanmadı."
    return "\n".join(f"- `{issue.quote_id}`: {issue.message}" for issue in issues)
