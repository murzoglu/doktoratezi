import csv
import tempfile
import unittest
from pathlib import Path

from dm_niteliksel_toolkit.quote_integrity import QUOTE_FIELDS, check_quotes


class QuoteIntegrityTests(unittest.TestCase):
    def test_exact_quote_match_has_no_issue(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, quotes = self._fixture(tmpdir, "Evde herkes saatlere göre hareket ediyor.")

            issues = check_quotes(source, quotes)

            self.assertEqual(issues, [])

    def test_changed_quote_warns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = self._source(tmpdir)
            quotes = Path(tmpdir) / "quotes.csv"
            self._write_quotes(quotes, "011_mother_q1", "Evde herkes plana göre hareket ediyor.")

            issues = check_quotes(source, quotes)

            self.assertTrue(any(issue.severity == "warning" for issue in issues))

    def test_shortened_quote_with_ellipsis_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = self._source(tmpdir)
            quotes = Path(tmpdir) / "quotes.csv"
            self._write_quotes(quotes, "011_mother_q1", "Evde herkes […] hareket ediyor.")

            issues = check_quotes(source, quotes)

            self.assertFalse(any(issue.quote_id == "011_mother_q1" and issue.severity == "warning" for issue in issues))

    def test_same_quote_id_with_different_text_warns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = self._source(tmpdir)
            quotes = Path(tmpdir) / "quotes.csv"
            with quotes.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=QUOTE_FIELDS)
                writer.writeheader()
                writer.writerow(self._quote_row("011_mother_q1", "Evde herkes saatlere göre hareket ediyor."))
                writer.writerow(self._quote_row("011_mother_q1", "Evde herkes plana göre hareket ediyor."))

            issues = check_quotes(source, quotes)

            self.assertTrue(any("farklı yazılmış" in issue.message for issue in issues))

    def _fixture(self, tmpdir, quote_text):
        source = self._source(tmpdir)
        quotes = Path(tmpdir) / "quotes.csv"
        self._write_quotes(quotes, "011_mother_q1", quote_text)
        return source, quotes

    def _source(self, tmpdir):
        source = Path(tmpdir) / "transcripts"
        source.mkdir()
        (source / "family_011_mother.md").write_text(
            "Evde herkes saatlere göre hareket ediyor. Sonra okul hazırlığı başlıyor.",
            encoding="utf-8",
        )
        return source

    def _write_quotes(self, path, quote_id, quote_text):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=QUOTE_FIELDS)
            writer.writeheader()
            writer.writerow(self._quote_row(quote_id, quote_text))

    def _quote_row(self, quote_id, quote_text):
        return {
            "quote_id": quote_id,
            "family_id": "011",
            "participant_role": "mother",
            "quote_text_used": quote_text,
            "manuscript_section": "results",
            "theme": "Aile rutini",
        }


if __name__ == "__main__":
    unittest.main()
