#!/usr/bin/env python3
"""Test bib_hygiene parser + reconcile functions."""

import unittest
import importlib.util
import pathlib
import sys
import tempfile

# Load bib_hygiene module from scripts/util
_MOD = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "util" / "bib_hygiene.py"
spec = importlib.util.spec_from_file_location("bib_hygiene", _MOD)
bh = importlib.util.module_from_spec(spec)
sys.modules["bib_hygiene"] = bh
spec.loader.exec_module(bh)

BIB = """@article{smith2020,
  author = {Smith, Jane and Doe, John},
  title = {A Title},
  journal = {J Test},
  year = {2020},
  volume = {1},
  number = {2},
  pages = {3--4},
  doi = {10.1/x}
}

@book{jones2019,
  author = {Jones, Amy},
  title = {A Book},
  publisher = {Pub},
  address = {City},
  year = {2019}
}
"""


class TestBibHygiene(unittest.TestCase):
    """Test cases for bib_hygiene parser module."""

    def test_parse_bib_extracts_type_key_fields(self):
        """Verify parse_bib extracts entry type, key, and fields correctly."""
        entries = bh.parse_bib(BIB)
        self.assertEqual(len(entries), 2)

        by_key = {e["key"]: e for e in entries}

        self.assertEqual(by_key["smith2020"]["type"], "article")
        self.assertEqual(by_key["smith2020"]["fields"]["doi"], "10.1/x")
        self.assertEqual(by_key["jones2019"]["type"], "book")

    def test_cited_keys_from_qmd(self):
        """Verify cited_keys extracts citation keys from Quarto markdown."""
        qmd = "Metin [@smith2020] ve @jones2019 ile [-@smith2020; @ghost2021]."
        keys = bh.cited_keys(qmd)
        self.assertEqual(keys, {"smith2020", "jones2019", "ghost2021"})

    def test_cited_keys_excludes_quarto_crossrefs(self):
        """Quarto çapraz-referansları (@fig-, @tbl-, @sec- vb.) künye atfı sayılmaz."""
        qmd = (
            "Bkz. @fig-causal-dag ve @tbl-apa-h1 ile [-@sec-yontem]; "
            "denklem @eq-model ve @lst-kod. Gerçek atıf: [@smith2020]"
        )
        keys = bh.cited_keys(qmd)
        self.assertEqual(keys, {"smith2020"})

    def test_reconcile_ignores_crossrefs_no_false_undefined(self):
        """Crossref'ler .bib'de tanımlı olmasa da 'undefined' üretmemeli."""
        entries = bh.parse_bib(BIB)
        cited = bh.cited_keys("@smith2020 ve @fig-x ve @tbl-y ve @sec-z")
        rec = bh.reconcile(entries, cited)
        self.assertEqual(rec["undefined"], [])

    def test_reconcile_flags_undefined_and_orphan(self):
        """Verify reconcile flags undefined (cited but not defined) and orphan (defined but not cited)."""
        entries = bh.parse_bib(BIB)
        cited = {"smith2020", "ghost2021"}  # ghost undefined; jones orphan
        r = bh.reconcile(entries, cited)
        self.assertEqual(r["undefined"], ["ghost2021"])
        self.assertEqual(r["orphan"], ["jones2019"])

    def test_check_fields_flags_missing_ama11_fields(self):
        """Verify check_fields flags missing AMA-11 fields (volume, pages for article)."""
        bib = """@article{noVol2021,
  author = {A, B},
  title = {T},
  journal = {J},
  year = {2021},
  doi = {10.1/y}
}
"""
        entries = bh.parse_bib(bib)
        issues = {i["key"]: i for i in bh.check_fields(entries)}
        self.assertIn("noVol2021", issues)
        self.assertGreaterEqual(set(issues["noVol2021"]["missing"]), {"volume", "pages"})

    def test_check_fields_clean_article_has_no_issue(self):
        """Verify clean article (smith2020) has no missing fields."""
        entries = bh.parse_bib(BIB)
        keys_with_issues = {i["key"] for i in bh.check_fields(entries)}
        self.assertNotIn("smith2020", keys_with_issues)

    def test_check_fields_volume_exempt_when_issue_and_pages_present(self):
        """Cilt kullanmayan (sayı-esaslı) dergiler: number+pages varsa volume
        eksikliği SOFT tetiklememeli; volume+pages ikisi de yoksa tetiklemeli."""
        bib = """@article{issueBased2017,
  author = {AKTAS, E}, title = {T}, journal = {J}, year = {2017},
  number = {44}, pages = {499--515}, doi = {10.1/x}
}
@article{noVolNoIssue2018,
  author = {B, C}, title = {T2}, journal = {J2}, year = {2018},
  pages = {10--20}, doi = {10.1/z}
}
"""
        entries = bh.parse_bib(bib)
        issues = {i["key"]: i for i in bh.check_fields(entries)}
        # sayı + sayfa var → volume muaf, SOFT yok
        self.assertNotIn("issueBased2017", issues)
        # sayı yok, yalnız sayfa var → volume hâlâ eksik
        self.assertIn("noVolNoIssue2018", issues)
        self.assertIn("volume", issues["noVolNoIssue2018"]["missing"])

    def test_check_ids_detects_bad_missing_and_dup_doi(self):
        """Verify check_ids detects bad DOI format, missing DOI in articles, and duplicate DOIs."""
        bib = """@article{a1,
  author={A,B}, title={T1}, journal={J}, year={2020}, volume={1}, pages={1--2},
  doi={10.1/dup}
}
@article{a2,
  author={C,D}, title={T2}, journal={J}, year={2021}, volume={2}, pages={3--4},
  doi={10.1/dup}
}
@article{a3,
  author={E,F}, title={T3}, journal={J}, year={2022}, volume={3}, pages={5--6},
  doi={not-a-doi}
}
@article{a4,
  author={G,H}, title={T4}, journal={J}, year={2023}, volume={4}, pages={7--8}
}
"""
        entries = bh.parse_bib(bib)
        r = bh.check_ids(entries)
        assert {"key": "a3", "doi": "not-a-doi"} in r["bad_doi"]
        assert "a4" in r["missing_doi"]
        dup = {d["doi"]: set(d["keys"]) for d in r["dup_doi"]}
        assert dup.get("10.1/dup") == {"a1", "a2"}

    def test_check_ids_doiless_but_pmid_or_url_not_missing(self):
        """DOI'siz ama PMID/URL ile erişilebilir makale eksik sayılmaz.

        Eski/Türkçe dergiler DOI atamamış olabilir; bu kayıtlar
        `no_doi_accessible` olarak sınıflanır ve SOFT kapısını tetiklemez.
        """
        bib = """@article{pmid_only,
  author={A,B}, title={T}, journal={J}, year={2005}, volume={1}, pages={1--2},
  pmid={26111288}
}
@article{url_only,
  author={C,D}, title={T}, journal={J}, year={1989}, volume={2}, pages={3--4},
  url={https://example.org/x.pdf}
}
@article{truly_missing,
  author={E,F}, title={T}, journal={J}, year={2023}, volume={3}, pages={5--6}
}
"""
        entries = bh.parse_bib(bib)
        r = bh.check_ids(entries)
        assert "pmid_only" in r["no_doi_accessible"]
        assert "url_only" in r["no_doi_accessible"]
        assert "pmid_only" not in r["missing_doi"]
        assert "url_only" not in r["missing_doi"]
        assert "truly_missing" in r["missing_doi"]

    def test_check_dedup_flags_near_duplicate_titles(self):
        """Verify check_dedup flags near-duplicate titles by Jaccard similarity."""
        bib = """@article{x1,
  author={Smith, Jane and Doe, John}, title={Parenting and Type 1 Diabetes in Children},
  journal={J}, year={2020}, volume={1}, pages={1--2}, doi={10.1/a}
}
@article{x2,
  author={Smith, J and Doe, J}, title={Parenting and Type 1 Diabetes in Children},
  journal={K}, year={2020}, volume={2}, pages={3--4}, doi={10.1/b}
}
@article{x3,
  author={Zeta, Q}, title={Unrelated Cardiology Review}, journal={C}, year={2019},
  volume={9}, pages={9--9}, doi={10.1/c}
}
"""
        entries = bh.parse_bib(bib)
        pairs = bh.check_dedup(entries, threshold=0.7)
        flagged = {frozenset((p["a"], p["b"])) for p in pairs}
        self.assertIn(frozenset(("x1", "x2")), flagged)
        self.assertNotIn(frozenset(("x1", "x3")), flagged)


    def test_run_all_and_exit_code(self):
        """Verify run_all returns reconcile/fields/ids/dedup and main exits 1 on undefined key."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            bib = tmp / "r.bib"
            bib.write_text(BIB, encoding="utf-8")
            ch = tmp / "c.qmd"
            ch.write_text("Atıf [@smith2020] ve [@ghost2099].", encoding="utf-8")
            res = bh.run_all(str(bib), [str(ch)])
            assert res["reconcile"]["undefined"] == ["ghost2099"]
            # HARD undefined -> exit 1
            code = bh.main(["all", "--bib", str(bib), "--chapters", str(ch), "--json"])
            assert code == 1

    def test_desired_scheme_maps_key_tags(self):
        """Verify desired_scheme maps BibTeX keys to subcollection + tags."""
        bib_txt = """@article{eviz2026turkiyeCare,
  author={Eviz,E}, title={T1D care in Turkiye}, journal={J}, year={2026},
  volume={1}, pages={1--2}, doi={10.1/z}, keywords={t1dm, turkiye}
}
"""
        entries = bh.parse_bib(bib_txt)
        sch = bh.desired_scheme(entries)
        assert "eviz2026turkiyeCare" in sch
        assert "tags" in sch["eviz2026turkiyeCare"]


    def test_desired_scheme_scans_title_not_just_key(self):
        bib = (
            "@article{lummerAikey2021,\n"
            "  author={Lummer-Aikey, S and Goldstein, S}, title={Sibling Adjustment to Childhood Chronic Illness},\n"
            "  journal={J}, year={2021}, volume={27}, pages={136--153}, doi={10.1/s}\n}\n"
            "@article{someQol2024,\n"
            "  author={A, B}, title={Health-Related Quality of Life in Type 1 Diabetes},\n"
            "  journal={J}, year={2024}, volume={1}, pages={1--2}, doi={10.1/q}\n}\n"
        )
        entries = bh.parse_bib(bib)
        sch = bh.desired_scheme(entries)
        # başlıkta 'Sibling' -> Kardeş Uyumu (key'de 'sibling' token yok)
        self.assertEqual(sch["lummerAikey2021"]["subcollection"], "Kardeş Uyumu")
        self.assertIn("sibling", sch["lummerAikey2021"]["tags"])
        # 'Quality of Life' -> KİA (son-eşleşen: title 'quality of life' > 'type 1')
        self.assertEqual(sch["someQol2024"]["subcollection"], "KİA / Yaşam Kalitesi")


if __name__ == "__main__":
    unittest.main()
