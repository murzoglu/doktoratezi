import csv
import tempfile
import unittest
from pathlib import Path

from dm_niteliksel_toolkit.reporting import find_negative_cases
from dm_niteliksel_toolkit.triadic_matrix import CODED_DATA_FIELDS


class NegativeCaseRoleAliasTests(unittest.TestCase):
    def test_turkish_role_aliases_count_toward_triadic_completeness(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            coded = Path(tmpdir) / "coded_segments.csv"
            output = Path(tmpdir) / "report.md"
            self._write_rows(
                coded,
                [
                    self._row("anne"),
                    self._row("t1dm_çocuk"),
                    self._row("kardeş"),
                ],
            )

            find_negative_cases(coded, "Kardeş yükü", output)

            report = output.read_text(encoding="utf-8")
            self.assertNotIn("eksik rol alanı olabilir", report)

    def test_missing_role_is_reported_with_turkish_aliases_present(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            coded = Path(tmpdir) / "coded_segments.csv"
            output = Path(tmpdir) / "report.md"
            self._write_rows(coded, [self._row("anne"), self._row("kardeş")])

            find_negative_cases(coded, "Kardeş yükü", output)

            report = output.read_text(encoding="utf-8")
            self.assertIn("t1dm_child", report)
            self.assertIn("eksik rol alanı olabilir", report)

    def _row(self, role):
        return {
            "family_id": "011",
            "participant_role": role,
            "participant_id": "p1",
            "theme": "Kardeş yükü",
            "subtheme": "Görünmeyen yük",
            "code_name": "Rutin yük",
            "quote_id": "q1",
            "quote_text": "Örnek alıntı.",
            "field_note": "",
            "memo": "",
        }

    def _write_rows(self, path, rows):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CODED_DATA_FIELDS)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)


if __name__ == "__main__":
    unittest.main()
