import csv
import tempfile
import unittest
from pathlib import Path

from dm_niteliksel_toolkit.coreq import (
    ALLOWED_COREQ_STATUSES,
    COREQ_ITEMS,
    audit_coreq,
    load_coreq_rows,
    write_coreq_template,
)


class CoreqTests(unittest.TestCase):
    def test_coreq_has_32_items(self):
        self.assertEqual(len(COREQ_ITEMS), 32)

    def test_template_status_values_are_allowed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "coreq_32_template.csv"
            write_coreq_template(path)

            rows = load_coreq_rows(path)

            self.assertEqual(len(rows), 32)
            self.assertTrue(all(row["status"] in ALLOWED_COREQ_STATUSES for row in rows))

    def test_invalid_status_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "coreq.csv"
            write_coreq_template(path)
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["status"] = "invented"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

            with self.assertRaises(ValueError):
                load_coreq_rows(path)

    def test_missing_evidence_stays_missing_and_not_invented(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            methods = root / "methods.md"
            results = root / "results.md"
            output = root / "coreq_report.md"
            methods.write_text("Bu metin COREQ kanıtı içermeyen kısa bir taslaktır.", encoding="utf-8")
            results.write_text("Bulgular bölümü henüz boş.", encoding="utf-8")

            rows = audit_coreq(methods, results, output)

            self.assertTrue(any(row.status == "missing" for row in rows))
            self.assertTrue(all("uydur" not in row.evidence_location.lower() for row in rows))
            self.assertTrue(output.exists())

    def test_short_researcher_initials_do_not_create_false_coder_evidence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            methods = root / "methods.md"
            results = root / "results.md"
            output = root / "coreq_report.md"
            methods.write_text(
                "Araştırma, aile olmanın ilişkisel deneyimini anlamayı amaçlamaktadır.",
                encoding="utf-8",
            )
            results.write_text("Bulgular henüz yazılmadı.", encoding="utf-8")

            rows = audit_coreq(methods, results, output)
            coder_row = next(row for row in rows if row.item_no == 24)

            self.assertEqual(coder_row.status, "missing")
            self.assertEqual(coder_row.evidence_location, "")


if __name__ == "__main__":
    unittest.main()
