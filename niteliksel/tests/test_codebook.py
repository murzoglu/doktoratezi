import csv
import tempfile
import unittest
from pathlib import Path

from dm_niteliksel_toolkit.codebook import CODEBOOK_FIELDS, lint_codebook, write_codebook_template


class CodebookTests(unittest.TestCase):
    def test_missing_code_name_is_critical(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "codebook.csv"
            self._write_rows(
                path,
                [
                    {
                        "code_id": "C1",
                        "code_name": "",
                        "definition": "Bir cümlelik tanım.",
                        "include_criteria": "Dahil.",
                        "exclude_criteria": "Hariç.",
                        "example_quote_id": "011_mother_q1",
                        "theme": "Tema",
                    }
                ],
            )

            issues = lint_codebook(path)

            self.assertTrue(any(issue.severity == "critical" and issue.field == "code_name" for issue in issues))

    def test_duplicate_code_name_with_different_definitions_warns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "codebook.csv"
            self._write_rows(
                path,
                [
                    self._base_row("C1", "Rutin yük", "Tanım bir."),
                    self._base_row("C2", "Rutin yük", "Tanım iki."),
                ],
            )

            issues = lint_codebook(path)

            self.assertTrue(any("farklı tanımlarla" in issue.message for issue in issues))

    def test_missing_include_or_exclude_warns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "codebook.csv"
            row = self._base_row("C1", "Rutin yük", "Tanım.")
            row["include_criteria"] = ""
            row["exclude_criteria"] = ""
            self._write_rows(path, [row])

            issues = lint_codebook(path)

            self.assertTrue(any(issue.field == "include_criteria" for issue in issues))
            self.assertTrue(any(issue.field == "exclude_criteria" for issue in issues))

    def test_codebook_template_is_valid_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "codebook_template.csv"

            created = write_codebook_template(path)

            self.assertTrue(created)
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, CODEBOOK_FIELDS)

    def test_placeholder_example_quote_id_warns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "codebook.csv"
            row = self._base_row("C1", "Rutin yük", "Tanım.")
            row["example_quote_id"] = "RESEARCHER_TO_ASSIGN_C1"
            self._write_rows(path, [row])

            issues = lint_codebook(path)

            self.assertTrue(any(issue.field == "example_quote_id" and "placeholder" in issue.message for issue in issues))

    def _base_row(self, code_id, code_name, definition):
        return {
            "code_id": code_id,
            "code_name": code_name,
            "definition": definition,
            "include_criteria": "Bu deneyimi anlatan ifadeler.",
            "exclude_criteria": "İlgisiz bağlam.",
            "example_quote_id": "011_mother_q1",
            "theme": "Aile rutini",
            "subtheme": "",
            "memo": "",
            "version": "v1",
            "date": "2026-06-30",
        }

    def _write_rows(self, path, rows):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CODEBOOK_FIELDS)
            writer.writeheader()
            for row in rows:
                writer.writerow({field: row.get(field, "") for field in CODEBOOK_FIELDS})


if __name__ == "__main__":
    unittest.main()
