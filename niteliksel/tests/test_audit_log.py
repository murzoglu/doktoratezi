"""AI kullanım günlüğü — append_ai_use davranışı (log-ai-use'un çekirdeği)."""
import csv
import tempfile
import unittest
from datetime import date
from pathlib import Path

from dm_niteliksel_toolkit.audit_log import AI_LOG_FIELDS, append_ai_use


def _read_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class AppendAiUseTests(unittest.TestCase):
    def test_first_write_creates_header_and_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "ai_use_log.csv"
            append_ai_use(log, tool="evidentia", model="m", purpose="p",
                          data_type="anonim/türetilmiş", output_summary="s",
                          external_api_used="yes")
            rows = _read_rows(log)
            self.assertEqual(len(rows), 1)
            self.assertEqual(list(rows[0].keys()), AI_LOG_FIELDS)
            self.assertEqual(rows[0]["tool"], "evidentia")
            self.assertEqual(rows[0]["external_api_used"], "yes")
            self.assertEqual(rows[0]["date"], date.today().isoformat())

    def test_second_write_appends_without_duplicate_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "ai_use_log.csv"
            append_ai_use(log, tool="a", model="m", purpose="p",
                          data_type="anonim/türetilmiş", output_summary="s1")
            append_ai_use(log, tool="b", model="m", purpose="p",
                          data_type="anonim/türetilmiş", output_summary="s2")
            rows = _read_rows(log)
            self.assertEqual([r["tool"] for r in rows], ["a", "b"])
            # Ham satır sayısı: 1 başlık + 2 veri = 3
            self.assertEqual(len(log.read_text(encoding="utf-8").strip().splitlines()), 3)

    def test_defaults_are_no_for_privacy_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "ai_use_log.csv"
            append_ai_use(log, tool="a", model="m", purpose="p",
                          data_type="anonim/türetilmiş", output_summary="s")
            row = _read_rows(log)[0]
            self.assertEqual(row["contains_raw_data"], "no")
            self.assertEqual(row["contains_identifiable_data"], "no")
            self.assertEqual(row["external_api_used"], "no")

    def test_parent_directory_is_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "99_ai_use_log" / "ai_use_log.csv"
            append_ai_use(log, tool="a", model="m", purpose="p",
                          data_type="anonim/türetilmiş", output_summary="s")
            self.assertTrue(log.exists())


class KvkkFlagGuardTests(unittest.TestCase):
    """CONVENTIONS kural 18: contains_raw_data/identifiable bayrakları 'no' kalmalı;
    böyle veri hiçbir harici araca gönderilmez. Kod düzeyinde reddedilir."""

    def test_contains_raw_data_yes_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "ai_use_log.csv"
            with self.assertRaises(ValueError):
                append_ai_use(log, tool="a", model="m", purpose="p",
                              data_type="anonim/türetilmiş", output_summary="s",
                              contains_raw_data="yes")

    def test_contains_identifiable_data_yes_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "ai_use_log.csv"
            with self.assertRaises(ValueError):
                append_ai_use(log, tool="a", model="m", purpose="p",
                              data_type="anonim/türetilmiş", output_summary="s",
                              contains_identifiable_data="yes")

    def test_rejected_row_is_not_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "ai_use_log.csv"
            with self.assertRaises(ValueError):
                append_ai_use(log, tool="a", model="m", purpose="p",
                              data_type="anonim/türetilmiş", output_summary="s",
                              contains_raw_data="yes")
            # Reddedilen kayıt dosyaya sızmamalı.
            self.assertFalse(log.exists())


if __name__ == "__main__":
    unittest.main()
