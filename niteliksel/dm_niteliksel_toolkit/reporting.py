from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .common import AI_SAFETY_STATEMENT, normalize_key, read_csv, slugify
from .triadic_matrix import ALLOWED_ROLES, normalize_role


NEGATIVE_CASE_TERMS = [
    "ama",
    "fakat",
    "ancak",
    "tersine",
    "etkilemedi",
    "fark etmedi",
    "yük yok",
    "korku yok",
    "sorun olmadı",
    "normal",
    "dışlanma",
]


def find_negative_cases(coded_data: Path, theme: str, output: Path | None = None) -> Path:
    rows = read_csv(coded_data)
    theme_key = normalize_key(theme)
    matched = [row for row in rows if normalize_key(row.get("theme", "")) == theme_key]
    candidates = []
    family_roles: dict[str, set[str]] = defaultdict(set)

    for row in matched:
        family_id = row.get("family_id", "")
        role = normalize_role(row.get("participant_role", ""))
        if role in ALLOWED_ROLES:
            family_roles[family_id].add(role)
        haystack = normalize_key(" ".join([row.get("code_name", ""), row.get("quote_text", ""), row.get("field_note", ""), row.get("memo", "")]))
        terms = [term for term in NEGATIVE_CASE_TERMS if term in haystack]
        if terms:
            candidates.append((row, terms))

    if output is None:
        output = Path("07_reports") / f"negative_case_report_{slugify(theme)}.md"

    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Negatif Vaka Tarama Desteği: {theme}",
        "",
        AI_SAFETY_STATEMENT,
        "",
        "Bu rapor negatif vaka keşfi için ön-denetim sağlar; nihai yorum üretmez.",
        "",
        "## Tema Kapsamı",
        "",
        f"- İncelenen kodlu segment sayısı: {len(matched)}",
        "",
        "## Olası Negatif / Sınırlayıcı Örnekler",
        "",
    ]
    if candidates:
        for row, terms in candidates:
            lines.append(
                "- "
                f"family_id=`{row.get('family_id', '')}`, role=`{row.get('participant_role', '')}`, "
                f"quote_id=`{row.get('quote_id', '')}`: kontrol terimleri `{', '.join(terms)}`. "
                "Araştırmacı kararı gerektirir."
            )
    else:
        lines.append("- Ön-denetimde belirgin aday saptanmadı; bu negatif vaka olmadığı anlamına gelmez.")

    lines.extend(["", "## Triadik Eksiklik / Gerilim Kontrolü", ""])
    for family_id, roles in sorted(family_roles.items()):
        missing = sorted(ALLOWED_ROLES - roles)
        if missing:
            lines.append(f"- `{family_id}` ailesinde bu tema altında eksik rol alanı olabilir: {', '.join(missing)}.")
    if not family_roles:
        lines.append("- Tema için aile-rol eşleşmesi bulunamadı.")

    lines.extend(
        [
            "",
            "## Araştırmacı Kararı İçin Notlar",
            "",
            "Aynı aile içinde anne, T1DM tanılı çocuk ve sağlıklı kardeş anlatıları birlikte okunmalıdır.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
