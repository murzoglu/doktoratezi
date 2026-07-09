"""KVKK koruma mantığı — is_protected_path + assert_not_protected_write.

Bu, deponun en kritik gizlilik yüzeyidir: hangi yolların ham/korumalı sayıldığını
kilitler. Regresyon burada sessizce KVKK ihlaline yol açabilir.
"""
import unittest
from pathlib import Path

from dm_niteliksel_toolkit.anonymization import assert_not_protected_write
from dm_niteliksel_toolkit.common import PROTECTED_RAW_DIRS, is_protected_path


class ProtectedPathTests(unittest.TestCase):
    def test_each_protected_dir_name_is_detected_anywhere_in_path(self):
        for name in PROTECTED_RAW_DIRS:
            with self.subTest(dir=name):
                self.assertTrue(is_protected_path(Path(name) / "x.csv"))
                self.assertTrue(is_protected_path(Path("a") / "b" / name / "x.csv"))

    def test_transcripts_sequence_under_02_processed_is_protected(self):
        self.assertTrue(
            is_protected_path(Path("02_processed") / "transcripts" / "aile_011.md")
        )

    def test_cleaned_text_under_02_processed_is_not_protected(self):
        # 02_processed/cleaned_text kanonik serbest çalışma alanıdır.
        self.assertFalse(
            is_protected_path(
                Path("02_processed") / "cleaned_text" / "thesis_qualitative_cleaned_current.md"
            )
        )

    def test_safe_working_dirs_are_not_protected(self):
        for safe in ["07_reports/x.md", "03_analysis/codebook/c.csv",
                     "04_triadic_matrices/m.csv", "06_manuscript_outputs/q.csv",
                     "00_context/TRACKER.md", "99_ai_use_log/ai_use_log.csv"]:
            with self.subTest(path=safe):
                self.assertFalse(is_protected_path(Path(safe)))

    def test_partial_name_match_does_not_false_trigger(self):
        # "raw" korumalı ama "raw_notes" adlı bir dizin parçası tam eşleşme değildir.
        self.assertFalse(is_protected_path(Path("raw_notes") / "x.md"))
        self.assertFalse(is_protected_path(Path("my01_raw_data") / "x.md"))


class AssertNotProtectedWriteTests(unittest.TestCase):
    def test_raises_on_protected_target(self):
        with self.assertRaises(ValueError):
            assert_not_protected_write(Path("01_deidentified") / "coded_segments.csv")
        with self.assertRaises(ValueError):
            assert_not_protected_write(Path("02_processed") / "transcripts" / "x.md")

    def test_allows_safe_target(self):
        # İstisna yükseltmemeli.
        assert_not_protected_write(Path("07_reports") / "out.md")


if __name__ == "__main__":
    unittest.main()
