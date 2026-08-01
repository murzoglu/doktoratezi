#!/usr/bin/env python3
"""csr_numeric_trace_audit.py için saf-mantık regresyon testleri.

Ağ çağrısı YAPMAZ. İki kritik davranışı kilitler:
  1. Kanonik kilit sabitleri (family_rows/long_rows) izlenebilir kaynak sayılır
     → tasarım girdisi olan n=241/n=482 'kaynaksız yüksek-risk' işaretlenmez.
  2. Atıflı metodolojik eşik sabitleri (ör. R̂ 1,05 eşiği + atıf) yüksek-risk
     sayılmaz; ne fazla ne eksik — atıfsız ya da eşik-kelimesiz sayılar
     etkilenmez.

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_csr_numeric_trace_audit.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

_MOD = (
    pathlib.Path(__file__).resolve().parents[1]
    / "scripts" / "util" / "csr_numeric_trace_audit.py"
)
spec = importlib.util.spec_from_file_location("csr_numeric_trace_audit", _MOD)
nt = importlib.util.module_from_spec(spec)
sys.modules["csr_numeric_trace_audit"] = nt
spec.loader.exec_module(nt)


def _num(token: str) -> "nt.ClaimNumber":
    """Test için basit ClaimNumber üret (extract_claim_numbers ile aynı normalizasyon)."""
    nums = nt.extract_claim_numbers(token)
    # tek sayı bekleniyor; ilk denetlenebilir olanı döndür
    for n in nums:
        if not n.excluded_reason:
            return n
    return nums[0]


class TestCitedThresholdExemption(unittest.TestCase):
    def test_cited_threshold_is_exempt(self):
        """Eşik kelimesi + atıf + sayı yakınlığı → muaf."""
        line = ("H1 tanıları yaygın 1,05 eşiğinin (Vehtari ve diğerleri, 2021) "
                "altında kalmıştır.")
        num = _num("1,05")
        self.assertTrue(nt.is_cited_threshold_constant(num, line))

    def test_threshold_without_citation_not_exempt(self):
        """Eşik kelimesi var ama atıf yok → muaf değil."""
        line = "H1 tanıları yaygın 1,05 eşiğinin altında kalmıştır."
        num = _num("1,05")
        self.assertFalse(nt.is_cited_threshold_constant(num, line))

    def test_citation_without_threshold_word_not_exempt(self):
        """Atıf var ama eşik kelimesi yok → muaf değil (etki büyüklüğü vb.)."""
        line = "Lovejoy ve diğerleri (2000) d = 0,40 bildirmiştir."
        num = _num("0,40")
        self.assertFalse(nt.is_cited_threshold_constant(num, line))

    def test_far_token_not_exempt(self):
        """Sayı eşik kelimesinden uzaksa (>25 karakter) muaf değil."""
        line = ("0,40 değeri raporlanmış; ayrıca çok daha ilerideki bir cümlede "
                "yaygın eşik tartışılmıştır (Vehtari ve diğerleri, 2021).")
        num = _num("0,40")
        self.assertFalse(nt.is_cited_threshold_constant(num, line))


class TestCodeFenceSkipping(unittest.TestCase):
    def _write(self, text: str) -> pathlib.Path:
        import tempfile
        p = pathlib.Path(tempfile.mkstemp(suffix=".md")[1])
        p.write_text(text, encoding="utf-8")
        return p

    def test_code_fence_lines_are_skipped(self):
        """Fenced kod bloğu içindeki sayılar (figür koordinatı, tribble verisi)
        görünür satır listesine girmez; düzyazı sayıları girer."""
        md = (
            "Düzyazı satırı: örneklem n = 482.\n"
            "```{r}\n"
            'coords <- c(1.35, 3.75, 6.25, 8.65)  # figür konumları\n'
            "```\n"
            "Sonuç: Beck toplam ortalaması 8,97 idi.\n"
        )
        p = self._write(md)
        try:
            visible = nt.iter_visible_csr_lines(p)
            joined = " ".join(t for _, t in visible)
            self.assertIn("482", joined)        # düzyazı korunur
            self.assertIn("8,97", joined)       # düzyazı korunur
            self.assertNotIn("1.35", joined)    # kod-literal atlanır
            self.assertNotIn("6.25", joined)    # kod-literal atlanır
        finally:
            p.unlink()

    def test_nested_fences_toggle_correctly(self):
        """Ard arda iki kod bloğu arasındaki düzyazı görünür kalır."""
        md = (
            "```{r}\nx <- 111\n```\n"
            "Arada düzyazı: 222 katılımcı.\n"
            "```python\ny = 333\n```\n"
            "Kapanış düzyazı: 444 aile.\n"
        )
        p = self._write(md)
        try:
            joined = " ".join(t for _, t in nt.iter_visible_csr_lines(p))
            self.assertIn("222", joined)
            self.assertIn("444", joined)
            self.assertNotIn("111", joined)
            self.assertNotIn("333", joined)
        finally:
            p.unlink()


class TestCitedExternalLiterature(unittest.TestCase):
    """Atıflı dış-literatür yeniden-ifadesi ayrımı (ch04→ch05/CSR sürüklenme kapısı).

    Kilitlenen davranış: Tartışma paragraflarında literatürden aktarılan sayılar
    (Pinquart g, PedsQL 75,1, dış çalışma n=... vb.) hiçbir outputs/tables hücresine
    düşmez; bunlar 'yüksek-risk eşsiz' sayılmamalı. Buna karşılık kendi sonucumuzun
    (atıfsız ya da 'çalışmamız/bulgumuz' yakınında) sürüklenmesi flag'lenmeye devam eder.
    """

    def _num(self, token):
        return _num(token)

    def test_bracket_cite_external_sample_is_excluded(self):
        """[@key] atıflı paragrafta dış-çalışma örneklem sayısı → dış-literatür."""
        para = ("Devins ve arkadaşlarının 19 hasta-eş çiftinde yürüttüğü çalışmada "
                "hastalar daha yüksek müdahalecilik bildirmiştir [@devins1997].")
        self.assertTrue(nt.is_cited_external_literature(self._num("19"), para))

    def test_bare_at_cite_external_sample_is_excluded(self):
        """Bare `@key` (pandoc, köşesiz) atıf da paragraf ölçeğinde tanınır."""
        para = ("Kronik hastalık örnekleminde @sattoe2012proxy 584 çocuk-ebeveyn "
                "çiftinde öz-bildirim ile ebeveyn-vekili karşılaştırılmıştır.")
        self.assertTrue(nt.is_cited_external_literature(self._num("584"), para))

    def test_author_date_prose_external_is_excluded(self):
        """Yazar-tarih düzyazısı (parantezli) atıf da tanınır."""
        para = ("Pinquart ve diğerleri (2013) meta-analizinde 75,1 puanlık bir "
                "yaşam kalitesi örneklemi bildirmiştir.")
        self.assertTrue(nt.is_cited_external_literature(self._num("75,1"), para))

    def test_own_result_without_citation_not_excluded(self):
        """Kendi sonucumuz + atıf yok → dış-literatür değil (flag'lenir)."""
        para = "Çalışmamızda indeks çocuklarda reddetme puanı 44,00 bulunmuştur."
        self.assertFalse(nt.is_cited_external_literature(self._num("44,00"), para))

    def test_own_result_near_token_not_excluded_even_with_citation(self):
        """Sayının HEMEN yanında 'çalışmamız/bulgumuz' varsa, paragrafta atıf olsa
        bile dış-literatür sayılmaz (kendi sonucumuz literatürle kıyaslanıyor)."""
        para = ("Bulgumuzda ICC 0,11 çıkmıştır ve bu düşük uyum önceki çok-bilgi-"
                "verici yazınıyla tutarlıdır [@deLosReyes2015].")
        self.assertFalse(nt.is_cited_external_literature(self._num("0,11"), para))

    def test_no_citation_paragraph_not_excluded(self):
        """Paragrafta hiç atıf yoksa dış-literatür ayrımı devreye girmez."""
        para = ("Örneklemde 108 çocuk-anne çifti değerlendirilmiş ve reddetme "
                "puanı 44,82 hesaplanmıştır.")
        self.assertFalse(nt.is_cited_external_literature(self._num("44,82"), para))

    def test_own_marker_far_from_token_still_excluded(self):
        """'tezimiz' gibi kendi-sonucumuz işaretçisi sayıdan uzaktaysa (±70 dışı)
        yerel pencere dışı kalır; sayı hâlâ dış-literatür sayılır."""
        para = ("@liskola2021 evlat edinilmiş çocuk örnekleminde (n=222) annelerin "
                "daha az belirti bildirdiğini göstermiştir; bu örüntü, tezimizdeki "
                "maternal Beck bulgusuyla kavramsal olarak örtüşür.")
        self.assertTrue(nt.is_cited_external_literature(self._num("222"), para))


class TestParagraphMap(unittest.TestCase):
    def _write(self, text):
        import tempfile
        p = pathlib.Path(tempfile.mkstemp(suffix=".md")[1])
        p.write_text(text, encoding="utf-8")
        return p

    def test_wrapped_paragraph_lines_share_full_text(self):
        """Sarılı (hard-wrapped) paragrafın her fiziksel satırı, atıf komşu satırda
        olsa bile tam paragraf metnine eşlenir."""
        md = (
            "Devins ve arkadaşlarının 19 hasta-eş çiftinde yürüttüğü çalışmada\n"
            "hastalar daha yüksek müdahalecilik bildirmiştir [@devins1997].\n"
        )
        p = self._write(md)
        try:
            pm = nt.build_paragraph_map(p)
            self.assertIn("[@devins1997]", pm[1])  # 1. satır atıfı görür (komşu satır)
            self.assertIn("19", pm[2])
        finally:
            p.unlink()

    def test_code_fence_excluded_from_paragraph_map(self):
        """Kod çiti içindeki satırlar paragraf haritasına girmez."""
        md = (
            "Düzyazı satırı bir.\n"
            "```{r}\n"
            "x <- 123\n"
            "```\n"
            "Düzyazı satırı iki.\n"
        )
        p = self._write(md)
        try:
            pm = nt.build_paragraph_map(p)
            self.assertNotIn(3, pm)  # kod-literal satırı haritada yok
            self.assertIn(1, pm)
            self.assertIn(5, pm)
        finally:
            p.unlink()


class TestLockConstants(unittest.TestCase):
    def test_lock_constants_loaded_when_present(self):
        """Gerçek kilit dosyası varsa family_rows/long_rows sabitleri okunur."""
        root = pathlib.Path(__file__).resolve().parents[1]
        lock = root / "data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock"
        entries = nt.read_lock_constants(root)
        if not lock.exists():
            self.skipTest("kilit dosyası yok (gitignored ortam)")
        values = {int(e.value) for e in entries}
        # kanonik tasarım sabitleri
        self.assertIn(241, values)
        self.assertIn(482, values)

    def test_lock_missing_returns_empty(self):
        """Kilit dosyası olmayan kökte boş liste döner (çökmeden)."""
        entries = nt.read_lock_constants(pathlib.Path("/nonexistent_root_xyz"))
        self.assertEqual(entries, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
