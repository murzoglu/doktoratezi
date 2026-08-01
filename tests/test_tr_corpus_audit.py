#!/usr/bin/env python3
"""Test tr_corpus_audit — axis H (başlık + tutarlılık + referans-anlatım)."""

import unittest
import importlib.util
import pathlib
import sys
import tempfile

_MOD = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "util" / "tr_corpus_audit.py"
spec = importlib.util.spec_from_file_location("tr_corpus_audit", _MOD)
tca = importlib.util.module_from_spec(spec)
sys.modules["tr_corpus_audit"] = tca
spec.loader.exec_module(tca)

_REPO = pathlib.Path(__file__).resolve().parents[1]


def _codes(findings):
    return {f.code for f in findings}


class TestTurkishCase(unittest.TestCase):
    def test_tr_upper_lower_dotted_i(self):
        self.assertEqual(tca.tr_upper("giriş"), "GİRİŞ")
        self.assertEqual(tca.tr_lower("GİRİŞ"), "giriş")
        self.assertEqual(tca.tr_upper("ılık"), "ILIK")
        self.assertEqual(tca.tr_lower("IŞIK"), "ışık")


class TestFence(unittest.TestCase):
    def test_r_comment_inside_fence_is_not_a_heading(self):
        text = (
            "# GİRİŞ ve AMAÇ\n\n"
            "```{r}\n"
            "#| label: setup\n"
            "# bu bir R yorumu, başlık değil\n"
            "## ikinci R yorumu\n"
            "```\n\n"
            "# BULGULAR\n"
        )
        heads = tca.extract_headings(text)
        titles = [h["title"] for h in heads]
        self.assertEqual(titles, ["GİRİŞ ve AMAÇ", "BULGULAR"])

    def test_html_comment_hash_ignored(self):
        text = "<!--\n# yorum içinde başlık değil\n-->\n\n# KISALTMALAR\n"
        heads = tca.extract_headings(text)
        self.assertEqual([h["title"] for h in heads], ["KISALTMALAR"])

    def test_attrs_stripped(self):
        heads = tca.extract_headings("# EKLER {.unnumbered}\n## Ek 1. X {#sec-ek}\n")
        self.assertEqual(heads[0]["title"], "EKLER")
        self.assertIn(".unnumbered", heads[0]["attrs"])
        self.assertEqual(heads[1]["title"], "Ek 1. X")


class TestHeadings(unittest.TestCase):
    def _mkfile(self, tmp, name, text):
        p = pathlib.Path(tmp) / name
        p.write_text(text, encoding="utf-8")
        return str(p)

    def test_level_skip_H1_to_H3(self):
        with tempfile.TemporaryDirectory() as tmp:
            fp = self._mkfile(tmp, "x.qmd", "# A BÖLÜM\n\n### C ALT\n")
            out = tca.check_cascade(tca.extract_headings(pathlib.Path(fp).read_text()), fp)
            self.assertIn("H-HC1", _codes(out))

    def test_no_level_skip_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            fp = self._mkfile(tmp, "x.qmd", "# A BÖLÜM\n\n## B ALT\n\n### C ALT\n")
            out = tca.check_cascade(tca.extract_headings(pathlib.Path(fp).read_text()), fp)
            self.assertNotIn("H-HC1", _codes(out))

    def test_depth_over_3(self):
        with tempfile.TemporaryDirectory() as tmp:
            fp = self._mkfile(tmp, "x.qmd", "# A\n## B\n### C\n#### D\n")
            out = tca.check_cascade(tca.extract_headings(pathlib.Path(fp).read_text()), fp)
            self.assertIn("H-HC2", _codes(out))

    def test_main_heading_conjunction_uppercase_is_HARD(self):
        heads = tca.extract_headings("# GİRİŞ VE AMAÇ\n")
        out = tca.check_case(heads, "01_giris_ve_amac.qmd")
        codes = _codes(out)
        self.assertIn("H-HC6a", codes)
        self.assertEqual(tca.CODE_SEVERITY["H-HC6a"], "blocker")

    def test_main_heading_correct_conjunction_clean(self):
        heads = tca.extract_headings("# GİRİŞ ve AMAÇ\n")
        out = tca.check_case(heads, "01_giris_ve_amac.qmd")
        self.assertNotIn("H-HC6a", _codes(out))

    def test_main_heading_titlecase_is_HARD(self):
        heads = tca.extract_headings("# Giriş ve Amaç\n")
        out = tca.check_case(heads, "01_giris_ve_amac.qmd")
        self.assertIn("H-HC6a", _codes(out))

    def test_L1_titlecase_lowercase_word_flagged(self):
        heads = tca.extract_headings("# BÖLÜM\n## örneklem ve tanımlayıcı\n")
        out = tca.check_case(heads, "x.qmd")
        self.assertIn("H-HC6b", _codes(out))

    def test_L1_titlecase_clean(self):
        heads = tca.extract_headings("# BÖLÜM\n## Örneklem ve Tanımlayıcı Bulgular\n")
        out = tca.check_case(heads, "x.qmd")
        self.assertNotIn("H-HC6b", _codes(out))

    def test_abbrev_in_L2_heading_not_flagged(self):
        # '### H1 — Çocuk Algısı (EMBU-C)' abbreviation/digit tokens skip
        heads = tca.extract_headings("# BÖLÜM\n## Üst\n### H1 — Çocuk Algısı (EMBU-C)\n")
        out = tca.check_case(heads, "x.qmd")
        self.assertNotIn("H-HC6c", _codes(out))

    def test_body_unnumbered_flagged(self):
        heads = tca.extract_headings("# BULGULAR\n## Örneklem {.unnumbered}\n")
        out = tca.check_cascade(heads, "04_bulgular.qmd")
        self.assertIn("H-HC5", _codes(out))

    def test_frontmatter_unnumbered_allowed(self):
        heads = tca.extract_headings("# KISALTMALAR {.unnumbered}\n")
        out = tca.check_cascade(heads, "00b_kisaltmalar.qmd")
        self.assertNotIn("H-HC5", _codes(out))

    def test_body_first_h1_mismatch(self):
        heads = tca.extract_headings("# YANLIŞ BAŞLIK\n")
        out = tca.check_cascade(heads, "01_giris_ve_amac.qmd")
        self.assertIn("H-HC3", _codes(out))

    def test_trailing_punctuation(self):
        heads = tca.extract_headings("# BÖLÜM:\n")
        out = tca.check_cascade(heads, "x.qmd")
        self.assertIn("H-HC7", _codes(out))


class TestSectionOrder(unittest.TestCase):
    def _mk_thesis(self, tmp, order):
        tmp = pathlib.Path(tmp)
        titles = {
            "01_giris_ve_amac": "# GİRİŞ ve AMAÇ\n",
            "02_genel_bilgiler": "# GENEL BİLGİLER\n",
            "03_gerec_ve_yontem": "# GEREÇ ve YÖNTEM\n",
            "04_bulgular": "# BULGULAR\n",
            "05_tartisma_ve_sonuc": "# TARTIŞMA ve SONUÇ\n",
        }
        for stem, txt in titles.items():
            (tmp / f"{stem}.qmd").write_text(txt, encoding="utf-8")
        inc = "\n".join(f"{{{{< include {s}.qmd >}}}}" for s in order)
        th = tmp / "thesis.qmd"
        th.write_text(inc + "\n", encoding="utf-8")
        return str(th)

    def test_wrong_order_flags_H_ORD(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Bulgular, Gereç'ten ÖNCE → ihlal
            th = self._mk_thesis(tmp, [
                "01_giris_ve_amac", "02_genel_bilgiler",
                "04_bulgular", "03_gerec_ve_yontem", "05_tartisma_ve_sonuc",
            ])
            seq = tca.build_assembled_h1_sequence(th)
            out = tca.check_section_order(seq)
            self.assertIn("H-ORD", _codes(out))

    def test_correct_order_no_inversion(self):
        with tempfile.TemporaryDirectory() as tmp:
            th = self._mk_thesis(tmp, [
                "01_giris_ve_amac", "02_genel_bilgiler", "03_gerec_ve_yontem",
                "04_bulgular", "05_tartisma_ve_sonuc",
            ])
            seq = tca.build_assembled_h1_sequence(th)
            inversions = [f for f in tca.check_section_order(seq)
                          if "sırası ihlali" in f.message]
            self.assertEqual(inversions, [])


class TestCoherence(unittest.TestCase):
    def _para(self, extra=""):
        return (
            "Kronik hastalık bağlamında ailelerin yaşadığı psikososyal yük "
            "çeşitli araştırmalarda incelenmiş ve ebeveynlerin duygusal "
            "tepkilerinin çocuğun uyumu üzerinde belirleyici olduğu ortaya "
            "konmuştur; bu bulgular klinik uygulama için önem taşımaktadır. " + extra
        )

    def test_cross_chapter_duplicate_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            (tmp / "01_giris_ve_amac.qmd").write_text("# GİRİŞ ve AMAÇ\n\n" + self._para(), encoding="utf-8")
            (tmp / "02_genel_bilgiler.qmd").write_text("# GENEL BİLGİLER\n\n" + self._para(), encoding="utf-8")
            tb = tca.load_termbase(None, "diyabet")
            files = [str(tmp / "01_giris_ve_amac.qmd"), str(tmp / "02_genel_bilgiler.qmd")]
            out = tca.run_coherence(files, tb)
            self.assertIn("H-DUP", _codes(out))

    def test_suppressed_pair_method_results_echo(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            (tmp / "03_gerec_ve_yontem.qmd").write_text("# GEREÇ ve YÖNTEM\n\n" + self._para(), encoding="utf-8")
            (tmp / "04_bulgular.qmd").write_text("# BULGULAR\n\n" + self._para(), encoding="utf-8")
            tb = tca.load_termbase(None, "diyabet")
            files = [str(tmp / "03_gerec_ve_yontem.qmd"), str(tmp / "04_bulgular.qmd")]
            out = tca.run_coherence(files, tb)
            # ch03↔ch04 meşru eko → bastırılır
            self.assertNotIn("H-DUP", _codes(out))

    def test_abbrev_undeclared_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            abbrev = tmp / "00b_kisaltmalar.qmd"
            abbrev.write_text("# KISALTMALAR\n\n| Kısaltma | Açıklama |\n|---|---|\n| EMBU | X |\n", encoding="utf-8")
            ch = tmp / "01_giris_ve_amac.qmd"
            ch.write_text("# GİRİŞ ve AMAÇ\n\nZZTQ ölçeği kullanıldı. ZZTQ tekrar edildi.\n", encoding="utf-8")
            tb = tca.load_termbase(str(abbrev), None)
            out = tca.abbrev_crosscheck({str(ch): ch.read_text()}, tb)
            codes = _codes(out)
            self.assertIn("H-ABBR", codes)  # ZZTQ tanımsız

    def test_abbrev_unused_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            abbrev = tmp / "00b_kisaltmalar.qmd"
            abbrev.write_text("# KISALTMALAR\n\n| Kısaltma | Açıklama |\n|---|---|\n| WLSMV | X |\n", encoding="utf-8")
            ch = tmp / "01_giris_ve_amac.qmd"
            ch.write_text("# GİRİŞ ve AMAÇ\n\nMetinde hiç geçmiyor.\n", encoding="utf-8")
            tb = tca.load_termbase(str(abbrev), None)
            out = tca.abbrev_crosscheck({str(ch): ch.read_text()}, tb)
            self.assertIn("H-ABBR-UNUSED", _codes(out))


class TestReferenceProse(unittest.TestCase):
    def test_reporting_verb_monotony(self):
        text = "# GENEL BİLGİLER\n\n" + " ".join(
            f"Araştırma bunu göstermiştir [@kaynak{i}]." for i in range(14)
        )
        out = tca.reporting_verb_monotony(text, "02_genel_bilgiler.qmd")
        self.assertIn("H-VERB", _codes(out))

    def test_bracket_monotony(self):
        text = "# GENEL BİLGİLER\n\n" + " ".join(
            f"Bir bulgu vardır [@k{i}]." for i in range(16)
        )
        out = tca.bracket_monotony(text, "02_genel_bilgiler.qmd")
        self.assertIn("H-BRAK", _codes(out))

    def test_discussion_zero_citation_soft(self):
        text = "# TARTIŞMA ve SONUÇ\n\nBulgular yorumlandı ama hiç atıf yok.\n"
        out = tca.citation_density(text, "05_tartisma_ve_sonuc.qmd")
        codes = _codes(out)
        self.assertIn("H-DISCZERO", codes)
        self.assertEqual(tca.CODE_SEVERITY["H-DISCZERO"], "major")

    def test_bulgular_zero_citation_is_info(self):
        text = "# BULGULAR\n\nSonuçlar sunuldu.\n"
        out = tca.citation_density(text, "04_bulgular.qmd")
        self.assertNotIn("H-DISCZERO", _codes(out))


class TestCanonicalDriftGuard(unittest.TestCase):
    def test_encoded_order_matches_talimatname(self):
        tal = _REPO / "tez-yazim" / "00_kaynak-kurallari" / "marmara-tez-formati-talimatnamesi.md"
        if not tal.exists():
            self.skipTest("talimatname yok")
        text = tal.read_text(encoding="utf-8")
        # §5 numaralı listesini parse et
        m = __import__("re").search(r"## 5\..*?RESMİ BÖLÜM SIRASI.*?\n(.*?)\n---",
                                    text, __import__("re").S)
        self.assertIsNotNone(m, "§5 bölümü bulunamadı")
        items = __import__("re").findall(r"^\d+\.\s+(.*?)\s*$", m.group(1),
                                         __import__("re").M)
        self.assertEqual(items, tca.CANONICAL_ORDER)


class TestExitCodes(unittest.TestCase):
    def test_severity_hard_soft_clean(self):
        self.assertEqual(tca._severity_code({"blocker": 1, "major": 0}, "major"), 1)
        self.assertEqual(tca._severity_code({"blocker": 0, "major": 2}, "major"), 2)
        self.assertEqual(tca._severity_code({"blocker": 0, "major": 0}, "major"), 0)
        self.assertEqual(tca._severity_code({"blocker": 1}, "none"), 0)
        self.assertEqual(tca._severity_code({"major": 3}, "blocker"), 0)

    def test_main_exit_on_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            fp = pathlib.Path(tmp) / "01_giris_ve_amac.qmd"
            fp.write_text("# GİRİŞ VE AMAÇ\n\n## örnek\n", encoding="utf-8")  # HARD case
            code = tca.main(["headings", "--chapters", str(fp), "--json"])
            self.assertEqual(code, 1)


class TestStdlibPurity(unittest.TestCase):
    def test_no_third_party_imports(self):
        src = _MOD.read_text(encoding="utf-8")
        for bad in ("import numpy", "import pandas", "import requests", "import yaml"):
            self.assertNotIn(bad, src)

    def test_module_compiles(self):
        import py_compile
        py_compile.compile(str(_MOD), doraise=True)


if __name__ == "__main__":
    unittest.main()
