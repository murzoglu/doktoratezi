#!/usr/bin/env python3
"""Materialize the bundled AI reliability scaffold into the doktoratezi repo.

Default mode is dry-run. Use --apply after reviewing the planned file writes.
Existing files are backed up before replacement.
"""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD_ROOT = SKILL_ROOT / "assets" / "ai-reliability"
REQUIRED_REPO_FILES = ("AGENTS.md", "CLAUDE.md", "_targets.R", "thesis.qmd")


def git_root() -> Path:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception as exc:  # pragma: no cover - environment guard
        raise SystemExit(f"Not inside a git repo: {exc}") from exc
    return Path(out)


def assert_repo(root: Path) -> None:
    missing = [name for name in REQUIRED_REPO_FILES if not (root / name).exists()]
    if missing:
        raise SystemExit(
            "This installer is doktoratezi-specific. Missing repo markers: "
            + ", ".join(missing)
        )


def iter_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    )


def selected_sources(args: argparse.Namespace) -> list[tuple[Path, Path]]:
    selections = [
        (SCAFFOLD_ROOT / ".codex", Path(".codex")),
        (SCAFFOLD_ROOT / "CONVENTIONS.md", Path("CONVENTIONS.md")),
        (SCAFFOLD_ROOT / "governance", Path("governance")),
        (SCAFFOLD_ROOT / "requirements.txt", Path("reliability") / "requirements.txt"),
        (SCAFFOLD_ROOT / "reliability" / "evals", Path("reliability") / "evals"),
        (SCAFFOLD_ROOT / "reliability" / "redteam", Path("reliability") / "redteam"),
        (SCAFFOLD_ROOT / "reliability" / "verify", Path("reliability") / "verify"),
    ]
    if args.with_observability:
        selections.append(
            (
                SCAFFOLD_ROOT / "reliability" / "observability",
                Path("reliability") / "observability",
            )
        )
    if args.with_ci:
        selections.append((SCAFFOLD_ROOT / ".github" / "workflows", Path(".github") / "workflows"))
    return selections


def planned_copies(args: argparse.Namespace, repo: Path) -> list[tuple[Path, Path]]:
    planned: list[tuple[Path, Path]] = []
    for src, rel_dest in selected_sources(args):
        if src.is_file():
            planned.append((src, repo / rel_dest))
            continue
        for file_path in iter_files(src):
            planned.append((file_path, repo / rel_dest / file_path.relative_to(src)))
    return planned


def copy_file(src: Path, dest: Path, *, apply: bool, backup_suffix: str) -> str:
    existed = dest.exists()
    if dest.exists() and filecmp.cmp(src, dest, shallow=False):
        return "unchanged"
    if not apply:
        return "would_update" if dest.exists() else "would_create"

    dest.parent.mkdir(parents=True, exist_ok=True)
    if existed:
        backup = dest.with_name(dest.name + backup_suffix)
        shutil.copy2(dest, backup)
    shutil.copy2(src, dest)
    return "updated" if existed else "created"


def chmod_hooks(repo: Path, *, apply: bool) -> None:
    hooks_dir = repo / ".codex" / "hooks"
    if not hooks_dir.exists():
        return
    for path in hooks_dir.glob("*.py"):
        if apply:
            path.chmod(path.stat().st_mode | 0o111)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write files. Omit for dry-run.")
    parser.add_argument("--check", action="store_true", help="Fail if materialized files drift from assets.")
    parser.add_argument("--with-ci", action="store_true", help="Also copy the GitHub Actions gate.")
    parser.add_argument(
        "--with-observability",
        action="store_true",
        help="Also copy OTel/Langfuse observability files.",
    )
    args = parser.parse_args()
    if args.apply and args.check:
        raise SystemExit("--apply and --check cannot be used together.")

    if not SCAFFOLD_ROOT.exists():
        raise SystemExit(f"Missing scaffold asset: {SCAFFOLD_ROOT}")

    repo = git_root()
    assert_repo(repo)

    backup_suffix = f".bak.{int(time.time())}"
    actions: list[tuple[str, Path]] = []
    for src, dest in planned_copies(args, repo):
        status = copy_file(src, dest, apply=args.apply, backup_suffix=backup_suffix)
        actions.append((status, dest.relative_to(repo)))

    chmod_hooks(repo, apply=args.apply)

    mode = "CHECK" if args.check else "APPLY" if args.apply else "DRY-RUN"
    print(f"{mode}: {repo}")
    for status, rel_dest in actions:
        print(f"{status:>12}  {rel_dest}")

    drift = [status for status, _ in actions if status != "unchanged"]
    if args.check:
        if drift:
            print("\nDrift detected. Re-run with --apply after reviewing the changed files.")
            return 1
        print("\nMaterialized reliability files match bundled assets.")
    elif not args.apply:
        print("\nRe-run with --apply after reviewing this plan.")
    else:
        print("\nNext: run /hooks in Codex and trust the repo-local hooks if you want them active.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
