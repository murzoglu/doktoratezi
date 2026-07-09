from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path
from typing import Iterable


AI_SAFETY_STATEMENT = (
    "AI destekli çıktılar yalnızca yardımcı, ön-denetim veya tutarlılık kontrolü "
    "olarak değerlendirilir. Kodlama, tema geliştirme ve yorumlama kararları "
    "araştırmacı sorumluluğundadır."
)

PROTECTED_RAW_DIRS = {
    ".remember",
    "00_raw_locked",
    "01_raw_data",
    "01_deidentified",
    "ham_veri",
    "raw",
    "ses_kayitlari",
}

PROTECTED_RAW_PATHS = {
    ("02_processed", "transcripts"),
}


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def safe_write_text(path: Path, content: str) -> bool:
    """Write a file only if it does not already exist."""
    ensure_parent(path)
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def safe_write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> bool:
    ensure_parent(path)
    if path.exists():
        return False
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return True


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    ensure_parent(path)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_key(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    return normalize_space(value)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return value or "tema"


def is_protected_path(path: Path) -> bool:
    parts = path.parts
    if any(part in PROTECTED_RAW_DIRS for part in parts):
        return True
    return any(_contains_part_sequence(parts, protected) for protected in PROTECTED_RAW_PATHS)


def _contains_part_sequence(parts: tuple[str, ...], sequence: tuple[str, ...]) -> bool:
    if len(sequence) > len(parts):
        return False
    for start in range(0, len(parts) - len(sequence) + 1):
        if parts[start : start + len(sequence)] == sequence:
            return True
    return False
