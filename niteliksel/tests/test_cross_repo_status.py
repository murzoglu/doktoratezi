import json
import unittest
from pathlib import Path

from dm_niteliksel_toolkit.cross_repo import build_cross_repo_status
from dm_niteliksel_toolkit.tool_bridge import route_query


QUAL_ROOT = Path(__file__).resolve().parents[1]
QUANT_ROOT = QUAL_ROOT.parent


class CrossRepoStatusTests(unittest.TestCase):
    def test_status_maps_both_thesis_repos(self):
        payload = json.loads(build_cross_repo_status("json"))

        self.assertEqual(payload["qualitative_repo"], str(QUAL_ROOT))
        self.assertEqual(payload["quantitative_repo"], str(QUANT_ROOT))
        paths = {item["path"] for item in payload["required_files"]}
        self.assertIn("00_context/CODEX_PLAYBOOK.md", paths)
        self.assertIn("tez-yazim/README.md", paths)
        self.assertIn("docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf", paths)
        self.assertIn("_targets.R", paths)
        self.assertIn("docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md", paths)
        self.assertEqual(payload["thesis_writing_system"]["entrypoint"], "tez-yazim/README.md")

    def test_status_keeps_raw_data_as_protected_boundary(self):
        payload = json.loads(build_cross_repo_status("json"))
        flattened = {
            path
            for boundary in payload["protected_boundaries"]
            for path in boundary["paths"]
        }

        self.assertIn("01_raw_data/", flattened)
        self.assertIn("02_processed/transcripts/", flattened)
        self.assertIn("data/raw/", flattened)
        self.assertIn("data/processed/*", flattened)

    def test_joint_display_route_includes_cross_repo_status(self):
        route = route_query("H5 joint display için iki repo karma tez yazım planı")

        self.assertTrue(any("cross-repo-status" in command for command in route.dmnitel_commands))
        self.assertEqual(route.paired_repo, str(QUANT_ROOT))


if __name__ == "__main__":
    unittest.main()
