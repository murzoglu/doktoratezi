#!/usr/bin/env python3
"""claim_certification.py için saf-mantık regresyon testleri.

Ağ/denetçi çağrısı YAPMAZ: _parse_kv çok-token satır ayrıştırmasını, karar
mantığını (PASS/WARN/FAIL eşikleri) ve çıkış-kodu eşlemesini doğrular.
Katman fonksiyonları monkeypatch ile sahte değerlerle beslenir.

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_claim_certification.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

_MOD = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "util" / "claim_certification.py"
spec = importlib.util.spec_from_file_location("claim_certification", _MOD)
cc = importlib.util.module_from_spec(spec)
sys.modules["claim_certification"] = cc
spec.loader.exec_module(cc)


class TestParseKV(unittest.TestCase):
    def test_multi_token_single_line(self):
        """Tek satırda çok k=v token'ı ayrı ayrı ayrıştırılmalı."""
        out = cc._parse_kv("claims=394 traced_all=250 partial=117 untraced=27")
        self.assertEqual(out["claims"], 394)
        self.assertEqual(out["traced_all"], 250)
        self.assertEqual(out["untraced"], 27)

    def test_path_value_stays_string(self):
        """Yol içeren değer int'e zorlanmaz, string kalır."""
        out = cc._parse_kv("report=outputs/reports/x.md")
        self.assertEqual(out["report"], "outputs/reports/x.md")

    def test_ignores_non_kv_tokens(self):
        out = cc._parse_kv("=== başlık === n=5")
        self.assertEqual(out.get("n"), 5)
        self.assertNotIn("===", out)


class TestNumf(unittest.TestCase):
    def test_numf_valid_and_fallback(self):
        self.assertEqual(cc._numf("0.86", 0.0), 0.86)
        self.assertEqual(cc._numf(None, 1.0), 1.0)
        self.assertEqual(cc._numf("x", 0.5), 0.5)


class TestCertifyDecision(unittest.TestCase):
    """certify() karar mantığı — katmanlar monkeypatch ile sahtelenir."""

    def setUp(self):
        self._orig = (cc.layer_numeric, cc.layer_causal, cc.layer_bib)

    def tearDown(self):
        cc.layer_numeric, cc.layer_causal, cc.layer_bib = self._orig

    def _patch(self, numeric, causal, bib):
        cc.layer_numeric = lambda csr: numeric
        cc.layer_causal = lambda csr: causal
        cc.layer_bib = lambda: bib

    def _clean(self):
        return (
            {"ok": True, "high_risk_unmatched": 0, "numbers_unmatched": 0,
             "claims": 10, "traced_all": 10, "partial": 0, "untraced": 0},
            {"ok": True, "causal_revise": 0, "causal_review": 0,
             "label_errors": 0, "label_reviews": 0, "causal_rows": 5, "label_rows": 100},
            {"ok": True, "undefined": [], "orphan": 0, "soft_fields": 0,
             "missing_doi": 0, "bad_doi": 0, "dup_doi": 0, "dedup": 0},
        )

    def test_all_clean_is_pass(self):
        self._patch(*self._clean())
        r = cc.certify("x.md", with_judge=False, strict=False, th=dict(cc.DEFAULT_THRESHOLDS))
        self.assertEqual(r["verdict"], "PASS")
        self.assertEqual(r["fails"], [])

    def test_causal_revise_is_fail(self):
        n, c, b = self._clean()
        c["causal_revise"] = 2
        self._patch(n, c, b)
        r = cc.certify("x.md", False, False, dict(cc.DEFAULT_THRESHOLDS))
        self.assertEqual(r["verdict"], "FAIL")
        self.assertTrue(any("nedensel-revize" in f for f in r["fails"]))

    def test_undefined_citation_is_fail(self):
        n, c, b = self._clean()
        b["undefined"] = ["ghostKey2020"]
        self._patch(n, c, b)
        r = cc.certify("x.md", False, False, dict(cc.DEFAULT_THRESHOLDS))
        self.assertEqual(r["verdict"], "FAIL")
        self.assertTrue(any("tanımsız atıf" in f for f in r["fails"]))

    def test_high_risk_number_is_warn(self):
        n, c, b = self._clean()
        n["high_risk_unmatched"] = 5
        self._patch(n, c, b)
        r = cc.certify("x.md", False, False, dict(cc.DEFAULT_THRESHOLDS))
        self.assertEqual(r["verdict"], "WARN")

    def test_strict_promotes_warn_to_fail(self):
        n, c, b = self._clean()
        n["high_risk_unmatched"] = 5
        self._patch(n, c, b)
        r = cc.certify("x.md", False, strict=True, th=dict(cc.DEFAULT_THRESHOLDS))
        self.assertEqual(r["verdict"], "FAIL")

    def test_label_error_is_fail(self):
        n, c, b = self._clean()
        c["label_errors"] = 1
        self._patch(n, c, b)
        r = cc.certify("x.md", False, False, dict(cc.DEFAULT_THRESHOLDS))
        self.assertEqual(r["verdict"], "FAIL")


class TestRenderAndExit(unittest.TestCase):
    def test_render_contains_verdict_icon(self):
        pkg = {
            "verdict": "PASS", "csr": "x.md", "strict": False, "with_judge": False,
            "fails": [], "warns": [],
            "layers": {
                "numeric": {"claims": 1, "traced_all": 1, "partial": 0, "untraced": 0,
                            "high_risk_unmatched": 0, "numbers_unmatched": 0},
                "causal": {"causal_rows": 0, "causal_revise": 0, "causal_review": 0,
                           "label_rows": 0, "label_errors": 0, "label_reviews": 0},
                "bib": {"undefined": [], "orphan": 0, "soft_fields": 0,
                        "missing_doi": 0, "bad_doi": 0, "dup_doi": 0, "dedup": 0},
            },
        }
        md = cc._render(pkg)
        self.assertIn("✅", md)
        self.assertIn("Claim Sertifikasyon Raporu", md)


if __name__ == "__main__":
    unittest.main()
