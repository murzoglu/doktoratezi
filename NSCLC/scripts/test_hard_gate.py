#!/usr/bin/env python3
"""NSCLC HARD-gate denetçileri için regresyon testleri (stdlib unittest).

Çalıştır:
  cd NSCLC && python3 scripts/test_hard_gate.py
Sessiz + exit 0 = PASS. Harici bağımlılık yok.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import context_source_guard as cg  # noqa: E402
import extraction_direction_check as ed  # noqa: E402
import prisma_flow_check as pf  # noqa: E402
import source_singularity_check as ss  # noqa: E402
import turkish_p_check as tp  # noqa: E402
from _common import to_float  # noqa: E402


def _tmp(content: str, suffix: str) -> str:
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


class TestToFloat(unittest.TestCase):
    def test_turkish_comma(self):
        self.assertEqual(to_float("0,72"), 0.72)

    def test_dot(self):
        self.assertEqual(to_float("0.72"), 0.72)

    def test_empty_and_unverified(self):
        self.assertIsNone(to_float(""))
        self.assertIsNone(to_float("unverified"))
        self.assertIsNone(to_float("NR"))

    def test_thousands(self):
        self.assertEqual(to_float("1.234,5"), 1234.5)


class TestPrismaFlow(unittest.TestCase):
    GOOD = ("asama;sayi;not\n"
            "tanimlanan_kayit_veritabani;120;\n"
            "tanimlanan_kayit_diger_yontem;5;\n"
            "tekillestirme_oncesi_toplam;125;\n"
            "cikarilan_duplikat;25;\n"
            "taranan_kayit;100;\n"
            "dislanan_kayit_tab;70;\n"
            "tam_metin_degerlendirilen;30;\n"
            "dislanan_tam_metin;22;\n"
            "dahil_edilen_calisma;8;\n"
            "dahil_edilen_rapor;10;\n")

    def test_good_passes(self):
        p = _tmp(self.GOOD, ".csv")
        self.assertTrue(pf.check(p).ok())
        os.remove(p)

    def test_arithmetic_blocker(self):
        bad = self.GOOD.replace("taranan_kayit;100", "taranan_kayit;99")
        p = _tmp(bad, ".csv")
        self.assertFalse(pf.check(p).ok())
        os.remove(p)

    def test_report_lt_studies_blocker(self):
        bad = self.GOOD.replace("dahil_edilen_rapor;10", "dahil_edilen_rapor;5")
        p = _tmp(bad, ".csv")
        self.assertFalse(pf.check(p).ok())
        os.remove(p)


class TestExtractionDirection(unittest.TestCase):
    HEAD = "study_id;pmid_doi;hr;ci95_lo;ci95_hi;p;orr;source_locator\n"

    def test_good_passes(self):
        good = self.HEAD + "A;10.1/x;0,72;0,58;0,90;0,001;45;Tablo 2\n"
        p = _tmp(good, ".csv")
        self.assertTrue(ed.check(p).ok())
        os.remove(p)

    def test_ci_inverted_blocker(self):
        bad = self.HEAD + "A;10.1/x;0,72;0,90;0,58;0,001;45;Tablo 2\n"
        p = _tmp(bad, ".csv")
        self.assertFalse(ed.check(p).ok())
        os.remove(p)

    def test_impossible_values(self):
        bad = self.HEAD + "A;;-0,5;0,1;0,9;1,5;150;\n"
        p = _tmp(bad, ".csv")
        self.assertFalse(ed.check(p).ok())
        os.remove(p)


class TestSourceSingularity(unittest.TestCase):
    SRC = ("study_id;hr;ci95_lo;ci95_hi;p;orr\n"
           "A;0,72;0,58;0,90;0,001;45\n")

    def test_grounded_passes(self):
        src = _tmp(self.SRC, ".csv")
        ms = _tmp("HR 0,72; %95 GA 0,58-0,90; p 0,001; ORR %45. Yıl 2023.\n", ".md")
        self.assertTrue(ss.check(ms, [src]).ok())
        os.remove(src)
        os.remove(ms)

    def test_fabricated_blocker(self):
        src = _tmp(self.SRC, ".csv")
        ms = _tmp("Havuzlanmış HR 0,63 idi.\n", ".md")
        self.assertFalse(ss.check(ms, [src]).ok())
        os.remove(src)
        os.remove(ms)


class TestTurkishP(unittest.TestCase):
    def test_comma_passes(self):
        ms = _tmp("HR 0,72; p = 0,001 anlamlı.\n", ".md")
        self.assertTrue(tp.check(ms).ok())
        os.remove(ms)

    def test_dot_p_blocker(self):
        ms = _tmp("p = 0.001 idi.\n", ".md")
        self.assertFalse(tp.check(ms).ok())
        os.remove(ms)

    def test_code_block_ignored(self):
        ms = _tmp("```\np = 0.05\n```\nMetinde p = 0,05.\n", ".md")
        self.assertTrue(tp.check(ms).ok())
        os.remove(ms)


class TestContextSourceGuard(unittest.TestCase):
    HEAD = "study_id;hr;ci95_lo;ci95_hi;orr;source_tier;source_locator\n"

    def test_evidence_effect_passes(self):
        good = self.HEAD + "A;0,72;0,58;0,90;45;evidence;PMID+T2\n"
        p = _tmp(good, ".csv")
        self.assertTrue(cg.check(p).ok())
        os.remove(p)

    def test_context_with_effect_blocker(self):
        bad = self.HEAD + "A;0,72;0,58;0,90;45;context;titck\n"
        p = _tmp(bad, ".csv")
        self.assertFalse(cg.check(p).ok())
        os.remove(p)

    def test_lead_with_effect_blocker(self):
        bad = self.HEAD + "A;0,49;0,38;0,64;48;lead;socius\n"
        p = _tmp(bad, ".csv")
        self.assertFalse(cg.check(p).ok())
        os.remove(p)

    def test_empty_tier_with_effect_blocker(self):
        bad = self.HEAD + "A;0,72;0,58;0,90;45;;PMID\n"
        p = _tmp(bad, ".csv")
        self.assertFalse(cg.check(p).ok())
        os.remove(p)

    def test_invalid_tier_blocker(self):
        bad = self.HEAD + "A;0,72;0,58;0,90;45;guess;PMID\n"
        p = _tmp(bad, ".csv")
        self.assertFalse(cg.check(p).ok())
        os.remove(p)

    def test_context_without_effect_passes(self):
        # bağlam satırı sayısız ise sorun yok (yalnız metodoloji notu)
        good = self.HEAD + "A;;;;;context;ich E9\n"
        p = _tmp(good, ".csv")
        self.assertTrue(cg.check(p).ok())
        os.remove(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
