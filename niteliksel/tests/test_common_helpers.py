"""common.py yardımcıları — slugify, normalize_key/space, no-overwrite yazımı, BOM okuma."""
import csv
import tempfile
import unittest
from pathlib import Path

from dm_niteliksel_toolkit.common import (
    normalize_key,
    normalize_space,
    read_csv,
    safe_write_csv,
    safe_write_text,
    slugify,
)


class SlugifyTests(unittest.TestCase):
    def test_strips_turkish_diacritics_and_lowercases(self):
        self.assertEqual(slugify("TEMA 4: Görünmeyen İş"), "tema_4_gorunmeyen_is")

    def test_collapses_non_alnum_runs_to_single_underscore(self):
        self.assertEqual(slugify("a — b / c"), "a_b_c")

    def test_empty_falls_back_to_tema(self):
        self.assertEqual(slugify(""), "tema")
        self.assertEqual(slugify("—/—"), "tema")


class NormalizeTests(unittest.TestCase):
    def test_normalize_space_collapses_whitespace(self):
        self.assertEqual(normalize_space("  a\t b\n c "), "a b c")

    def test_normalize_key_casefolds_and_trims(self):
        self.assertEqual(normalize_key("  TEMA  4 "), "tema 4")

    def test_normalize_key_handles_none(self):
        self.assertEqual(normalize_key(None), "")


class NoOverwriteTests(unittest.TestCase):
    def test_safe_write_text_refuses_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.md"
            self.assertTrue(safe_write_text(p, "first"))
            self.assertFalse(safe_write_text(p, "second"))
            self.assertEqual(p.read_text(encoding="utf-8"), "first")

    def test_safe_write_csv_refuses_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.csv"
            self.assertTrue(safe_write_csv(p, ["a"], [{"a": "1"}]))
            self.assertFalse(safe_write_csv(p, ["a"], [{"a": "2"}]))


class ReadCsvTests(unittest.TestCase):
    def test_reads_utf8_bom_without_polluting_first_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "b.csv"
            # utf-8-sig ile yazıp BOM'un başlık adına sızmadığını doğrula
            with p.open("w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.DictWriter(handle, fieldnames=["family_id", "theme"])
                writer.writeheader()
                writer.writerow({"family_id": "011", "theme": "T4"})
            rows = read_csv(p)
            self.assertEqual(rows[0]["family_id"], "011")
            self.assertIn("family_id", rows[0])


if __name__ == "__main__":
    unittest.main()
