"""Versioned Git-ignore contract for protected qualitative research data."""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ROOT_IGNORE = REPO / ".gitignore"
QUAL_IGNORE = REPO / "niteliksel" / ".gitignore"

PROTECTED_PATHS = (
    "niteliksel/00_raw_locked/v3_incoming/source.docx",
    "niteliksel/01_raw_data/v3_incoming/source.docx",
    "niteliksel/01_deidentified/v3/segments.csv",
    "niteliksel/02_processed/transcripts/v3/transcript.md",
    "niteliksel/03_analysis/spreadsheets/v3.xlsx",
    "niteliksel/03_analysis/thematic_memos/v3.md",
    "niteliksel/03_analysis/triadic_matrices/v3.csv",
    "niteliksel/04_triadic_matrices/v3/matrix.csv",
    "niteliksel/new/v3.docx",
    "niteliksel/00_context/file_manifest_v3.tsv",
    "niteliksel/00_context/reorg_move_log.tsv",
)


class GitignoreProtectedPathsTests(unittest.TestCase):
    def test_root_and_qualitative_ignore_files_define_the_boundary(self):
        root_text = ROOT_IGNORE.read_text(encoding="utf-8")
        qual_text = QUAL_IGNORE.read_text(encoding="utf-8")
        for root_pattern, qual_pattern in (
            ("niteliksel/01_raw_data/", "01_raw_data/"),
            ("niteliksel/02_processed/", "02_processed/"),
            ("niteliksel/04_triadic_matrices/", "04_triadic_matrices/"),
            ("niteliksel/00_context/file_manifest_*.tsv", "00_context/file_manifest_*.tsv"),
        ):
            with self.subTest(root_pattern=root_pattern):
                self.assertIn(root_pattern, root_text)
                self.assertIn(qual_pattern, qual_text)

    def test_every_protected_path_is_ignored_by_a_versioned_rule(self):
        for path in PROTECTED_PATHS:
            with self.subTest(path=path):
                proc = subprocess.run(
                    ["git", "check-ignore", "-v", "--no-index", path],
                    cwd=REPO,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, proc.returncode, proc.stderr)
                source = proc.stdout.split("\t", 1)[0].split(":", 1)[0]
                self.assertIn(source, {".gitignore", "niteliksel/.gitignore"})

    def test_public_canonical_manifest_remains_trackable(self):
        proc = subprocess.run(
            [
                "git",
                "check-ignore",
                "--quiet",
                "--no-index",
                "niteliksel/03_analysis/public_canonical_manifest.json",
            ],
            cwd=REPO,
            check=False,
        )
        self.assertEqual(1, proc.returncode)


if __name__ == "__main__":
    unittest.main()
