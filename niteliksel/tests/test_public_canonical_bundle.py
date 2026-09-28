import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "util" / "verify_public_canonical_bundle.py"
MANIFEST = ROOT / "03_analysis" / "public_canonical_manifest.json"


class PublicCanonicalBundleTests(unittest.TestCase):
    def run_verifier(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )

    def test_public_bundle_integrity_passes_without_protected_inputs(self):
        completed = self.run_verifier("--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["source_rederivation"], "not_available_in_public_clone")
        self.assertEqual(len(payload["checked_artifacts"]), 7)
        self.assertNotIn("new/", completed.stdout)

    def test_manifest_lists_only_public_relative_artifacts(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

        for artifact in manifest["artifacts"]:
            path = Path(artifact["path"])
            self.assertFalse(path.is_absolute())
            self.assertNotIn("..", path.parts)
            self.assertNotIn("01_raw_data", path.parts)
            self.assertNotIn("02_processed", path.parts)

    def test_hash_mismatch_fails(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest["artifacts"][0]["sha256"] = "0" * 64

        with tempfile.TemporaryDirectory() as tmpdir:
            tampered_manifest = Path(tmpdir) / "manifest.json"
            tampered_manifest.write_text(json.dumps(manifest), encoding="utf-8")
            completed = self.run_verifier("--manifest", str(tampered_manifest), "--json")

        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stdout)
        self.assertFalse(payload["ok"])
        self.assertIn("SHA-256 mismatch: 03_analysis/codebook/codebook_v3.csv", payload["errors"])


if __name__ == "__main__":
    unittest.main()
