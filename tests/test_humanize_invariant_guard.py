#!/usr/bin/env python3
"""Test humanize_invariant_guard — insansılaştırma DOKUNULMAZLIK bekçisi.

Sınanan sözleşme: üslup değişse bile ÖZ değişmez. Bir sayının/atıfın/çapraz
referansın/çekincenin düşmesi, bir sayının mutasyona uğraması, uydurma sayı-kaynak
eklenmesi ve kesinlik enflasyonu HARD; salt yeniden ifade SOFT/temizdir. Ayrıca
ritim (burstiness) ve klişe ölçümünün yönü doğrulanır.

Run: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_humanize_invariant_guard.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

_MOD = (
    pathlib.Path(__file__).resolve().parents[1]
    / "scripts" / "eval" / "humanize_invariant_guard.py"
)
spec = importlib.util.spec_from_file_location("humanize_invariant_guard", _MOD)
hig = importlib.util.module_from_spec(spec)
sys.modules["humanize_invariant_guard"] = hig
spec.loader.exec_module(hig)


KAYNAK = """\
Bu bağlamda, ebeveyn reddi ile çocuk depresyon düzeyi kapsamlı bir şekilde incelenmiştir.
Ebeveyn reddi ile depresyon puanı arasında orta düzeyde pozitif bir ilişki saptanmıştır (r = 0,38; p < 0,001).
Bu ilişki, yaş ve cinsiyet kontrol edildikten sonra da korunmuştur (β = 0,29; %95 GA [0,12; 0,45]).
Kontrol grubunda aynı ilişki anlamlı bulunmamıştır (r = 0,08; p = 0,412).
Bulgular @tbl-apa-h1 ve @fig-h1-forest içinde sunulmuştur [@rohner2005; @dirik2014].
Çalışma kesitsel olduğundan nedensellik çıkarılamaz ve bulgular dikkatle yorumlanmalıdır [KEŞİFSEL].
"""

ADAY_TEMIZ = """\
Reddedilme, çocuğun ruhsal yükünü değiştirir.
Ebeveyn reddi ile depresyon puanı arasında orta düzeyde pozitif bir ilişki saptanmıştır (r = 0,38; p < 0,001); bu büyüklük, klinik gözlemin uzun süredir işaret ettiği örüntüyü bu örneklemde sayısallaştırmaktadır.
Yaş ve cinsiyet kontrol edildiğinde ilişki ayakta kalmıştır (β = 0,29; %95 GA [0,12; 0,45]).
Kontrol grubunda tablo farklıdır: aynı ilişki anlamlı bulunmamıştır (r = 0,08; p = 0,412).
Ayrıntılar @tbl-apa-h1 ve @fig-h1-forest içinde sunulmuş olup örüntü, kuramın öngörüsüyle örtüşmektedir [@rohner2005; @dirik2014].
Yine de tasarım kesitseldir. Nedensellik çıkarılamaz; bulgular dikkatle yorumlanmalıdır [KEŞİFSEL].
"""


def _kinds(findings):
    return {(kind, cls, val) for kind, cls, val, _ in findings}


def _classes(findings):
    return {cls for _, cls, _, _ in findings}


class TestOzKorumasi(unittest.TestCase):
    def test_temiz_yeniden_yazim_hard_uretmez(self):
        res = hig.compare(KAYNAK, ADAY_TEMIZ)
        self.assertEqual(res["hard"], [], f"beklenmeyen HARD: {res['hard']}")

    def test_dusen_sayi_hard(self):
        aday = ADAY_TEMIZ.replace("(r = 0,38; p < 0,001)", "(anlamlı bir ilişki)")
        res = hig.compare(KAYNAK, aday)
        self.assertIn("sayi", _classes(res["hard"]))
        self.assertIn("istatistik", _classes(res["hard"]))

    def test_mutasyona_ugrayan_sayi_hard(self):
        aday = ADAY_TEMIZ.replace("r = 0,38", "r = 0,42")
        res = hig.compare(KAYNAK, aday)
        self.assertIn(("DÜŞTÜ", "istatistik", "r=0,38"), _kinds(res["hard"]))
        self.assertIn(("UYDURULDU", "istatistik", "r=0,42"), _kinds(res["hard"]))

    def test_ondalik_nokta_kaymasi_hard(self):
        """0,38 → 0.38 bir biçim değil ÖZ ihlalidir (Marmara ondalık virgül)."""
        aday = ADAY_TEMIZ.replace("r = 0,38", "r = 0.38")
        res = hig.compare(KAYNAK, aday)
        self.assertIn("istatistik", _classes(res["hard"]))

    def test_dusen_atif_ve_capraz_ref_hard(self):
        aday = ADAY_TEMIZ.replace("[@rohner2005; @dirik2014]", "[@rohner2005]")
        aday = aday.replace(" ve @fig-h1-forest", "")
        res = hig.compare(KAYNAK, aday)
        self.assertIn(("DÜŞTÜ", "atif", "@dirik2014"), _kinds(res["hard"]))
        self.assertIn(("DÜŞTÜ", "capraz_ref", "@fig-h1-forest"), _kinds(res["hard"]))

    def test_uydurulan_atif_hard(self):
        aday = ADAY_TEMIZ.replace("[@rohner2005; @dirik2014]", "[@rohner2005; @dirik2014; @uydurma2099]")
        res = hig.compare(KAYNAK, aday)
        self.assertIn(("UYDURULDU", "atif", "@uydurma2099"), _kinds(res["hard"]))

    def test_dusen_cekince_hard(self):
        aday = ADAY_TEMIZ.replace(
            "Yine de tasarım kesitseldir. Nedensellik çıkarılamaz; bulgular dikkatle yorumlanmalıdır [KEŞİFSEL].",
            "Bulgular güçlü bir örüntü ortaya koymaktadır [KEŞİFSEL].",
        )
        res = hig.compare(KAYNAK, aday)
        self.assertIn("cekince", _classes(res["hard"]))

    def test_dusen_etiket_hard(self):
        aday = ADAY_TEMIZ.replace(" [KEŞİFSEL]", "")
        res = hig.compare(KAYNAK, aday)
        self.assertIn("etiket", _classes(res["hard"]))

    def test_olumsuzlama_kaybi_hard(self):
        """'anlamlı bulunmamıştır' → 'anlamlı bulunmuştur' yön ters çevirmedir."""
        aday = ADAY_TEMIZ.replace("anlamlı bulunmamıştır", "anlamlı bulunmuştur")
        res = hig.compare(KAYNAK, aday)
        self.assertIn("olumsuzluk", _classes(res["hard"]))

    def test_kesinlik_enflasyonu_hard(self):
        aday = ADAY_TEMIZ + "Bu bulgu, reddedilmenin depresyona neden olduğunu kesinlikle kanıtlamaktadır.\n"
        res = hig.compare(KAYNAK, aday)
        kinds = {k for k, _, _, _ in res["hard"]}
        self.assertIn("KESİNLİK ENFLASYONU", kinds)

    def test_yz_beyani_silinmesi_hard(self):
        kaynak = KAYNAK + "Metnin dil düzenlemesinde büyük dil modeli desteği alınmıştır.\n"
        res = hig.compare(kaynak, ADAY_TEMIZ)
        self.assertIn("yz_beyani", _classes(res["hard"]))

    def test_yon_degisimi_soft(self):
        aday = ADAY_TEMIZ.replace("orta düzeyde pozitif", "pozitif")
        res = hig.compare(KAYNAK, aday)
        self.assertEqual(res["hard"], [])
        self.assertIn("yon", {cls for _, cls, _, _ in res["soft"]})


class TestRitimOlcumu(unittest.TestCase):
    def test_insansilastirma_burstiness_artirir(self):
        m_src = hig.compute_metrics(KAYNAK)
        m_cnd = hig.compute_metrics(ADAY_TEMIZ)
        self.assertGreater(m_cnd["cv"], m_src["cv"])
        self.assertGreater(m_cnd["ttr"], m_src["ttr"])

    def test_klise_tespiti(self):
        m_src = hig.compute_metrics(KAYNAK)
        m_cnd = hig.compute_metrics(ADAY_TEMIZ)
        self.assertGreaterEqual(m_src["cliche_hits"], 2)  # "bu bağlamda", "kapsamlı bir şekilde"
        self.assertEqual(m_cnd["cliche_hits"], 0)

    def test_tekduze_metin_bulgu_uretir(self):
        tekduze = "\n".join(
            f"Bu bağlamda ele alınan {i}. değişken için ilgili analiz sonucu ayrıntılı biçimde raporlanmıştır."
            for i in range(1, 9)
        )
        find = hig.metric_findings(hig.compute_metrics(tekduze))
        self.assertTrue(any("burstiness" in f for f in find), find)
        self.assertTrue(any("klişe" in f or "LLM imza" in f for f in find), find)

    def test_cumle_bolme_ondalik_ve_kisaltma_korur(self):
        s = hig.split_sentences("Ortalama 0,38 idi (bkz. Tablo 1). İkinci cümle burada yer alır.")
        self.assertEqual(len(s), 2, s)

    def test_mattr_metin_uzunlugundan_bagimsizdir(self):
        """Ham TTR uzun metinde mekanik çöker; MATTR sabit pencerede kararlı kalır."""
        import random

        rnd = random.Random(7)
        vocab = [f"sozcuk{i}" for i in range(120)]

        def uret(n_cumle):
            return "\n".join(
                " ".join(rnd.choice(vocab) for _ in range(11)) + "."
                for _ in range(n_cumle)
            )

        m_orta, m_uzun = hig.compute_metrics(uret(30)), hig.compute_metrics(uret(300))
        self.assertLess(m_uzun["ttr"], m_orta["ttr"] / 2)  # ham TTR uzunlukla çöker
        self.assertAlmostEqual(m_uzun["mattr"], m_orta["mattr"], delta=0.08)

    def test_tekduze_seri_esigi_uzunlukla_buyur(self):
        self.assertEqual(hig._uniform_run_limit(6), 4)
        self.assertGreater(hig._uniform_run_limit(575), hig._uniform_run_limit(46))


class TestGuvenlik(unittest.TestCase):
    def test_korumali_yol_reddedilir(self):
        with self.assertRaises(SystemExit):
            hig.assert_safe_path("data/raw/Raw Data - Final.csv")
        with self.assertRaises(SystemExit):
            hig.assert_safe_path("_targets/objects/x")

    def test_manuskript_yolu_kabul_edilir(self):
        hig.assert_safe_path("chapters/04_bulgular.qmd")  # istisna atmamalı

    def test_kod_citi_envanterden_duser(self):
        metin = "Değer 0,38'dir.\n\n```{r}\nx <- 0.99\n```\n"
        bag = hig.extract_inventory(metin)
        self.assertIn(("sayi", "0,38"), bag)
        self.assertNotIn(("sayi", "0.99"), bag)


if __name__ == "__main__":
    unittest.main(verbosity=2)
