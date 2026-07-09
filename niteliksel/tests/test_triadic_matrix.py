import csv
import tempfile
import unittest
from pathlib import Path

from dm_niteliksel_toolkit.triadic_matrix import CODED_DATA_FIELDS, build_triadic_matrix, normalize_role


class RoleAliasTests(unittest.TestCase):
    def test_turkish_aliases_map_to_canonical_roles(self):
        self.assertEqual(normalize_role("anne"), "mother")
        self.assertEqual(normalize_role("t1dm_cocuk"), "t1dm_child")
        self.assertEqual(normalize_role("t1dm_çocuk"), "t1dm_child")
        self.assertEqual(normalize_role("diyabetli_cocuk"), "t1dm_child")
        self.assertEqual(normalize_role("kardes"), "healthy_sibling")
        self.assertEqual(normalize_role("kardeş"), "healthy_sibling")
        self.assertEqual(normalize_role("sağlıklı_kardeş"), "healthy_sibling")

    def test_canonical_roles_pass_through(self):
        self.assertEqual(normalize_role("mother"), "mother")
        self.assertEqual(normalize_role("t1dm_child"), "t1dm_child")
        self.assertEqual(normalize_role("healthy_sibling"), "healthy_sibling")

    def test_case_and_whitespace_are_normalized(self):
        self.assertEqual(normalize_role("  Anne "), "mother")
        self.assertEqual(normalize_role("KARDEŞ"), "healthy_sibling")

    def test_unknown_role_returns_none(self):
        self.assertIsNone(normalize_role("father"))
        self.assertIsNone(normalize_role(""))


class TriadicMatrixTests(unittest.TestCase):
    def test_turkish_role_aliases_are_grouped_like_canonical_roles(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            coded = Path(tmpdir) / "coded_segments.csv"
            output = Path(tmpdir) / "triadic_matrix.csv"
            self._write_rows(
                coded,
                [
                    self._row("anne", "q_m"),
                    self._row("t1dm_çocuk", "q_t"),
                    self._row("kardeş", "q_s"),
                ],
            )

            rows = build_triadic_matrix(coded, output)

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["mother_quote_ids"], "q_m")
            self.assertEqual(rows[0]["t1dm_child_quote_ids"], "q_t")
            self.assertEqual(rows[0]["healthy_sibling_quote_ids"], "q_s")

    def test_groups_three_roles_under_same_family_and_theme(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            coded = Path(tmpdir) / "coded_segments.csv"
            output = Path(tmpdir) / "triadic_matrix.csv"
            self._write_rows(
                coded,
                [
                    self._row("mother", "q_m"),
                    self._row("t1dm_child", "q_t"),
                    self._row("healthy_sibling", "q_s"),
                ],
            )

            rows = build_triadic_matrix(coded, output)

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["mother_quote_ids"], "q_m")
            self.assertEqual(rows[0]["t1dm_child_quote_ids"], "q_t")
            self.assertEqual(rows[0]["healthy_sibling_quote_ids"], "q_s")

    def test_missing_role_leaves_empty_field(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            coded = Path(tmpdir) / "coded_segments.csv"
            output = Path(tmpdir) / "triadic_matrix.csv"
            self._write_rows(coded, [self._row("mother", "q_m")])

            rows = build_triadic_matrix(coded, output)

            self.assertEqual(rows[0]["t1dm_child_quote_ids"], "")
            self.assertEqual(rows[0]["healthy_sibling_quote_ids"], "")

    def test_invalid_role_raises_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            coded = Path(tmpdir) / "coded_segments.csv"
            output = Path(tmpdir) / "triadic_matrix.csv"
            self._write_rows(coded, [self._row("father", "q_f")])

            with self.assertRaises(ValueError):
                build_triadic_matrix(coded, output)

    def test_quote_ids_are_preserved_by_role(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            coded = Path(tmpdir) / "coded_segments.csv"
            output = Path(tmpdir) / "triadic_matrix.csv"
            self._write_rows(coded, [self._row("mother", "q1"), self._row("mother", "q2")])

            rows = build_triadic_matrix(coded, output)

            self.assertEqual(rows[0]["mother_quote_ids"], "q1;q2")

    def _row(self, role, quote_id):
        return {
            "family_id": "011",
            "participant_role": role,
            "participant_id": "p1",
            "theme": "Kardeş yükü",
            "subtheme": "Görünmeyen yük",
            "code_name": "Rutin yük",
            "quote_id": quote_id,
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
