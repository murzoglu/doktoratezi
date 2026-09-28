from __future__ import annotations

import json
import stat
import tempfile
import unittest
from pathlib import Path

from scripts.util.ingest_v3_protected_intake import MANIFEST_NAME, ingest_sources


class V3ProtectedIntakeTests(unittest.TestCase):
    def test_import_is_content_opaque_idempotent_and_restricted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.docx"
            second_source = root / "second.csv"
            source.write_bytes(b"protected test fixture")
            second_source.write_bytes(b"second protected test fixture")
            intake = root / "01_raw_data" / "v3_incoming"

            first = ingest_sources([source], intake)
            second = ingest_sources([source], intake)
            third = ingest_sources([second_source], intake)

            self.assertEqual("copied", first[0]["action"])
            self.assertEqual("existing", second[0]["action"])
            self.assertEqual("copied", third[0]["action"])
            self.assertEqual(0o700, stat.S_IMODE(intake.stat().st_mode))
            self.assertEqual(0o600, stat.S_IMODE((intake / source.name).stat().st_mode))
            self.assertEqual(0o600, stat.S_IMODE((intake / MANIFEST_NAME).stat().st_mode))

            manifest = json.loads((intake / MANIFEST_NAME).read_text(encoding="utf-8"))
            self.assertEqual("v3", manifest["intake_label"])
            manifest_names = {record["filename"] for record in manifest["artifacts"]}
            self.assertEqual({source.name, second_source.name}, manifest_names)
            self.assertTrue(all("source_path" not in record for record in manifest["artifacts"]))

    def test_rejects_nonmatching_filename_collision(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intake = root / "01_raw_data" / "v3_incoming"
            first_parent = root / "first"
            second_parent = root / "second"
            first_parent.mkdir()
            second_parent.mkdir()
            first = first_parent / "artifact.csv"
            second = second_parent / "artifact.csv"
            first.write_bytes(b"first")
            second.write_bytes(b"second")

            ingest_sources([first], intake)
            with self.assertRaises(FileExistsError):
                ingest_sources([second], intake)


if __name__ == "__main__":
    unittest.main()
