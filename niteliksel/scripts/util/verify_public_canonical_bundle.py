#!/usr/bin/env python3
"""Verify the public qualitative v3 canonical artifact bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "03_analysis" / "public_canonical_manifest.json"
EXPECTED_SOURCE_REDERIVATION = "not_available_in_public_clone"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_relative_path(value: Any) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("artifact path must be a non-empty string")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"artifact path must stay within the public bundle: {value}")
    return path


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read manifest: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data


def verify_manifest(manifest_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    checked: list[str] = []

    try:
        manifest = load_manifest(manifest_path)
    except ValueError as exc:
        return {
            "ok": False,
            "checked_artifacts": checked,
            "errors": [str(exc)],
            "source_rederivation": EXPECTED_SOURCE_REDERIVATION,
        }

    if manifest.get("schema_version") != 1:
        errors.append("unsupported or missing schema_version")
    if manifest.get("canonical_version") != "v3":
        errors.append("canonical_version must be v3")
    if manifest.get("source_rederivation") != EXPECTED_SOURCE_REDERIVATION:
        errors.append("source_rederivation contract is invalid")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must be a non-empty list")
        artifacts = []

    seen_paths: set[Path] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            errors.append("each artifact must be an object")
            continue
        try:
            relative_path = validate_relative_path(artifact.get("path"))
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if relative_path in seen_paths:
            errors.append(f"duplicate artifact path: {relative_path}")
            continue
        seen_paths.add(relative_path)

        expected_hash = artifact.get("sha256")
        if not isinstance(expected_hash, str) or len(expected_hash) != 64:
            errors.append(f"invalid SHA-256 value: {relative_path}")
            continue
        try:
            int(expected_hash, 16)
        except ValueError:
            errors.append(f"invalid SHA-256 value: {relative_path}")
            continue

        artifact_path = ROOT / relative_path
        if not artifact_path.is_file():
            errors.append(f"missing artifact: {relative_path}")
            continue

        checked.append(relative_path.as_posix())
        actual_hash = sha256_file(artifact_path)
        if actual_hash != expected_hash:
            errors.append(f"SHA-256 mismatch: {relative_path}")

    return {
        "ok": not errors,
        "canonical_version": manifest.get("canonical_version"),
        "checked_artifacts": checked,
        "errors": errors,
        "source_rederivation": manifest.get("source_rederivation"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    result = verify_manifest(args.manifest)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    elif result["ok"]:
        print(
            "PASS: public v3 canonical integrity: "
            f"{len(result['checked_artifacts'])} artifacts verified. "
            "Source re-derivation is intentionally unavailable in a public clone."
        )
    else:
        print("FAIL: public v3 canonical integrity", file=sys.stderr)
        for error in result["errors"]:
            print(f"- {error}", file=sys.stderr)

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
