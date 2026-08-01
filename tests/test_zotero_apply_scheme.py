"""Unit tests for zotero_apply_scheme.build_plan (pure, no network)."""

import importlib.util
import pathlib
import sys
import unittest

_MOD = (
    pathlib.Path(__file__).resolve().parents[1]
    / "scripts"
    / "util"
    / "zotero_apply_scheme.py"
)
spec = importlib.util.spec_from_file_location("zotero_apply_scheme", _MOD)
zas = importlib.util.module_from_spec(spec)
sys.modules["zotero_apply_scheme"] = zas
spec.loader.exec_module(zas)


class TestBuildPlan(unittest.TestCase):
    def test_matches_by_doi_and_falls_back_to_genel(self):
        desired = {"10.1/a": {"subcollection": "Kardeş Uyumu", "tags": ["sibling"]}}
        items = [
            # case-insensitive DOI match -> Kardeş Uyumu + sibling tag
            {
                "data": {
                    "key": "IT1",
                    "DOI": "10.1/A",
                    "title": "x",
                    "collections": [],
                    "tags": [],
                }
            },
            # no DOI -> Genel; t1dm already present, so add_tags == []
            {
                "data": {
                    "key": "IT2",
                    "DOI": "",
                    "title": "y",
                    "collections": [],
                    "tags": [{"tag": "t1dm"}],
                }
            },
        ]
        plan = zas.build_plan(desired, items)
        a = {x["item_key"]: x for x in plan["assignments"]}

        self.assertEqual(a["IT1"]["subcollection"], "Kardeş Uyumu")
        self.assertIn("sibling", a["IT1"]["add_tags"])

        self.assertEqual(a["IT2"]["subcollection"], "Genel")
        self.assertEqual(a["IT2"]["add_tags"], [])  # t1dm already present

        self.assertIn("Kardeş Uyumu", plan["subcollections"])
        self.assertEqual(plan["unmatched_by_doi"], 1)

    def test_matched_count(self):
        desired = {
            "10.1/x": {"subcollection": "EMBU / Ebeveynlik Tutumu", "tags": ["embu"]},
            "10.1/y": {"subcollection": "KİA / Yaşam Kalitesi", "tags": ["t1dm"]},
        }
        items = [
            {"data": {"key": "A", "DOI": "10.1/X", "title": "", "collections": [], "tags": []}},
            {"data": {"key": "B", "DOI": "10.1/Y", "title": "", "collections": [], "tags": []}},
            {"data": {"key": "C", "DOI": "", "title": "", "collections": [], "tags": []}},
        ]
        plan = zas.build_plan(desired, items)
        self.assertEqual(plan["matched"], 2)
        self.assertEqual(plan["unmatched_by_doi"], 1)
        self.assertEqual(len(plan["assignments"]), 3)

    def test_no_duplicate_tags_added(self):
        """If tag is already present, add_tags must not include it."""
        desired = {"10.1/a": {"subcollection": "T1DM Psikososyal", "tags": ["t1dm", "embu"]}}
        items = [
            {
                "data": {
                    "key": "Z",
                    "DOI": "10.1/A",
                    "title": "z",
                    "collections": [],
                    "tags": [{"tag": "t1dm"}],  # t1dm already present
                }
            }
        ]
        plan = zas.build_plan(desired, items)
        a = plan["assignments"][0]
        self.assertNotIn("t1dm", a["add_tags"])
        self.assertIn("embu", a["add_tags"])

    def test_subcollections_sorted(self):
        desired = {
            "10.1/a": {"subcollection": "Z-col", "tags": []},
            "10.1/b": {"subcollection": "A-col", "tags": []},
        }
        items = [
            {"data": {"key": "K1", "DOI": "10.1/A", "title": "", "collections": [], "tags": []}},
            {"data": {"key": "K2", "DOI": "10.1/B", "title": "", "collections": [], "tags": []}},
        ]
        plan = zas.build_plan(desired, items)
        self.assertEqual(plan["subcollections"], sorted(plan["subcollections"]))


if __name__ == "__main__":
    unittest.main()
