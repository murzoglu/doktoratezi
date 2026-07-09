from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .common import read_csv, safe_write_csv, write_csv


ALLOWED_ROLES = {"mother", "t1dm_child", "healthy_sibling"}

# Türkçe rol adları (aksanlı/aksansız) kanonik İngilizce rollere eşlenir.
ROLE_ALIASES = {
    "anne": "mother",
    "t1dm_cocuk": "t1dm_child",
    "t1dm_çocuk": "t1dm_child",
    "diyabetli_cocuk": "t1dm_child",
    "diyabetli_çocuk": "t1dm_child",
    "hasta_cocuk": "t1dm_child",
    "hasta_çocuk": "t1dm_child",
    "kardes": "healthy_sibling",
    "kardeş": "healthy_sibling",
    "saglikli_kardes": "healthy_sibling",
    "sağlıklı_kardeş": "healthy_sibling",
}


def normalize_role(raw: str) -> str | None:
    role = (raw or "").strip().lower().replace(" ", "_")
    # Türkçe büyük İ/I küçültmesi locale'e bağlı sapabilir; alias anahtarları
    # zaten küçük harfli tutulur, ek olarak noktalı büyük İ'yi güvene al.
    role = role.replace("i̇", "i")
    if role in ALLOWED_ROLES:
        return role
    return ROLE_ALIASES.get(role)

CODED_DATA_FIELDS = [
    "family_id",
    "participant_role",
    "participant_id",
    "theme",
    "subtheme",
    "code_name",
    "quote_id",
    "quote_text",
    "field_note",
    "memo",
]

TRIADIC_FIELDS = [
    "family_id",
    "theme",
    "subtheme",
    "mother_summary",
    "t1dm_child_summary",
    "healthy_sibling_summary",
    "mother_quote_ids",
    "t1dm_child_quote_ids",
    "healthy_sibling_quote_ids",
    "convergence",
    "divergence",
    "negative_case_flag",
    "analytic_memo",
]


def write_triadic_template(path: Path) -> bool:
    return safe_write_csv(path, TRIADIC_FIELDS, [])


def build_triadic_matrix(coded_data: Path, output: Path) -> list[dict[str, str]]:
    rows = read_csv(coded_data)
    grouped: dict[tuple[str, str, str], dict[str, list[str]]] = defaultdict(lambda: {role: [] for role in ALLOWED_ROLES})
    for index, row in enumerate(rows, start=2):
        raw_role = (row.get("participant_role") or "").strip()
        role = normalize_role(raw_role)
        if role is None:
            raise ValueError(f"Geçersiz participant_role satır {index}: {raw_role!r}")
        key = (
            (row.get("family_id") or "").strip(),
            (row.get("theme") or "").strip(),
            (row.get("subtheme") or "").strip(),
        )
        quote_id = (row.get("quote_id") or "").strip()
        if quote_id:
            grouped[key][role].append(quote_id)

    output_rows: list[dict[str, str]] = []
    for family_id, theme, subtheme in sorted(grouped):
        role_quotes = grouped[(family_id, theme, subtheme)]
        output_rows.append(
            {
                "family_id": family_id,
                "theme": theme,
                "subtheme": subtheme,
                "mother_summary": "",
                "t1dm_child_summary": "",
                "healthy_sibling_summary": "",
                "mother_quote_ids": ";".join(role_quotes["mother"]),
                "t1dm_child_quote_ids": ";".join(role_quotes["t1dm_child"]),
                "healthy_sibling_quote_ids": ";".join(role_quotes["healthy_sibling"]),
                "convergence": "",
                "divergence": "",
                "negative_case_flag": "",
                "analytic_memo": "",
            }
        )

    write_csv(output, TRIADIC_FIELDS, output_rows)
    return output_rows
