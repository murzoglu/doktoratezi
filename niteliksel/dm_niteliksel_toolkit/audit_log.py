from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from .common import ensure_parent, safe_write_csv


AI_LOG_FIELDS = [
    "date",
    "tool",
    "model",
    "purpose",
    "data_type",
    "contains_raw_data",
    "contains_identifiable_data",
    "external_api_used",
    "output_summary",
    "researcher_decision",
]


def write_ai_log_template(path: Path) -> bool:
    return safe_write_csv(path, AI_LOG_FIELDS, [])


def append_ai_use(
    path: Path,
    tool: str,
    model: str,
    purpose: str,
    data_type: str,
    output_summary: str,
    researcher_decision: str = "",
    contains_raw_data: str = "no",
    contains_identifiable_data: str = "no",
    external_api_used: str = "no",
) -> None:
    # KVKK (CONVENTIONS kural 18): ham/kimliklenebilir veri hiçbir harici araca
    # gönderilemez; dolayısıyla bu bayraklar 'no' dışında kaydedilemez. Reddet ve
    # hiçbir satır yazma.
    for field, value in (
        ("contains_raw_data", contains_raw_data),
        ("contains_identifiable_data", contains_identifiable_data),
    ):
        if value != "no":
            raise ValueError(
                f"KVKK: {field}={value!r} kaydedilemez. Ham/kimliklenebilir veri "
                f"harici araca gönderilmez; bu bayrak 'no' olmalıdır."
            )
    ensure_parent(path)
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=AI_LOG_FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "date": date.today().isoformat(),
                "tool": tool,
                "model": model,
                "purpose": purpose,
                "data_type": data_type,
                "contains_raw_data": contains_raw_data,
                "contains_identifiable_data": contains_identifiable_data,
                "external_api_used": external_api_used,
                "output_summary": output_summary,
                "researcher_decision": researcher_decision,
            }
        )
