from __future__ import annotations

from pathlib import Path

from .common import PROTECTED_RAW_DIRS, is_protected_path


def assert_not_protected_write(path: Path) -> None:
    if is_protected_path(path):
        protected = ", ".join(sorted(PROTECTED_RAW_DIRS))
        raise ValueError(
            f"Bu yol ham veri koruma listesinde: {path}. Yazma/dönüştürme hedefi "
            f"şu klasörlerden biri olamaz: {protected}."
        )
