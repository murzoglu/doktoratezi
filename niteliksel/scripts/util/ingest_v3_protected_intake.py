#!/usr/bin/env python3
"""Import protected v3 qualitative source files without inspecting content."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DEFAULT_INTAKE_DIR = Path(__file__).resolve().parents[2] / "01_raw_data" / "v3_incoming"
MANIFEST_NAME = "intake_manifest.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_manifest(path: Path, payload: dict) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(payload, handle, ensure_ascii=True, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    os.chmod(temporary, 0o600)
    temporary.replace(path)


def _read_manifest(path: Path) -> dict:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError(f"Unsupported intake manifest schema: {path}")
    return payload


def ingest_sources(sources: Iterable[Path], intake_dir: Path = DEFAULT_INTAKE_DIR) -> list[dict]:
    """Copy sources atomically and return metadata-only import records."""
    intake_dir = intake_dir.resolve()
    intake_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(intake_dir, 0o700)

    manifest_path = intake_dir / MANIFEST_NAME
    previous_manifest = _read_manifest(manifest_path)
    all_records = {
        str(record["filename"]): record
        for record in previous_manifest.get("artifacts", [])
        if isinstance(record, dict) and record.get("filename")
    }
    records: list[dict] = []
    for source in sources:
        source = source.expanduser().resolve()
        if not source.is_file():
            raise FileNotFoundError(f"Source file not found: {source}")

        target = intake_dir / source.name
        source_hash = sha256_file(source)
        action = "copied"
        if target.exists():
            if sha256_file(target) != source_hash:
                raise FileExistsError(f"Refusing to overwrite nonmatching intake artifact: {target.name}")
            action = "existing"
        else:
            with tempfile.NamedTemporaryFile(dir=intake_dir, delete=False) as handle:
                temporary = Path(handle.name)
            try:
                shutil.copyfile(source, temporary)
                os.chmod(temporary, 0o600)
                temporary.replace(target)
            finally:
                temporary.unlink(missing_ok=True)

        os.chmod(target, 0o600)
        record = {
            "filename": target.name,
            "bytes": target.stat().st_size,
            "sha256": source_hash,
            "action": action,
        }
        records.append(record)
        all_records[target.name] = record

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    manifest = {
        "schema_version": 1,
        "intake_label": "v3",
        "created_at_utc": previous_manifest.get("created_at_utc") or now,
        "updated_at_utc": now,
        "artifacts": [all_records[name] for name in sorted(all_records)],
    }
    _write_manifest(manifest_path, manifest)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy v3 qualitative source files into the protected local intake."
    )
    parser.add_argument("--source", action="append", required=True, type=Path)
    args = parser.parse_args()

    records = ingest_sources(args.source)
    copied = sum(record["action"] == "copied" for record in records)
    existing = len(records) - copied
    print(json.dumps({"artifacts": len(records), "copied": copied, "existing": existing}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
