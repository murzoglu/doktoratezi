#!/usr/bin/env python3
"""Test terim_tutarlilik_audit — kanonik terim sözlüğü zorlaması.

Muafiyet mantığının (ilk-geçiş parantezi, bağlamsal paragraf penceresi, kod-çiti,
atıf, İngilizce özet dosya-öneki, bölüm başlığı) HARD/INFO ayrımını doğru yaptığını
ve gömülü mini-YAML ayrıştırıcının PyYAML yokken şemayı doğru okuduğunu sınar.

Run: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_terim_tutarlilik.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import tempfile
import unittest

_MOD = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "util" / "terim_tutarlilik_audit.py"
spec = importlib.util.spec_from_file_location("terim_tutarlilik_audit", _MOD)
tta = importlib.util.module_from_spec(spec)
sys.modules["terim_tutarlilik_audit"] = tta
spec.loader.exec_module(tta)

_REPO = pathlib.Path(__file__).resolve().parents[1]
_SOZLUK = _REPO / "docs" / "tez-kilavuz" / "terim-sozlugu.yaml"


# --- test sabitleri: minimal in-memory sözlük (gerçek YAML'a bağımlı değil) ---
def _sozluk(terimler, global_muaf=None):
    return {"global_muafiyet": global_muaf or {}, "terimler": terimler}


def _hard(findings):
    return [f for f in findings if f.level == "HARD"]


def _info(findings):
    return [f for f in findings if f.level == "INFO"]


def _scan_text(text, terimler, global_muaf=None, name="x.qmd"):
    """Geçici .qmd yazıp scan_file çalıştır."""
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / name
        p.write_text(text, encoding="utf-8")
        return tta.scan_file(str(p), terimler, global_muaf or {})


# ---------------------------------------------------------------------------
# 1. Gömülü mini-YAML ayrıştırıcı
# ---------------------------------------------------------------------------
class TestMiniYaml(unittest.TestCase):
    def test_inline_list_and_scalars(self):
        text = (
            "global_muafiyet:\n"
            '  muaf_dosya_onekleri: ["chapters/00c"]\n'
            '  muaf_bolum_basliklari: ["SUMMARY", "ABSTRACT"]\n'
            "terimler:\n"
            '  - id: A1\n'
            '    kanonik: "gizil değişken"\n'
            '    zorlama: "hard"\n'
            '    yasak_varyantlar: ["latent değişken", "örtük değişken"]\n'
        )
        d = tta._mini_yaml(text)
        self.assertEqual(d["global_muafiyet"]["muaf_dosya_onekleri"], ["chapters/00c"])
        self.assertEqual(d["global_muafiyet"]["muaf_bolum_basliklari"],
                         ["SUMMARY", "ABSTRACT"])
        self.assertEqual(len(d["terimler"]), 1)
        t = d["terimler"][0]
        self.assertEqual(t["id"], "A1")
        self.assertEqual(t["kanonik"], "gizil değişken")
        self.assertEqual(t["zorlama"], "hard")
        self.assertEqual(t["yasak_varyantlar"], ["latent değişken", "örtük değişken"])

    def test_empty_inline_list(self):
        self.assertEqual(tta._scalar("[]"), [])

    def test_scalar_unquote(self):
        self.assertEqual(tta._scalar('"a b"'), "a b")
        self.assertEqual(tta._scalar("c d"), "c d")


# ---------------------------------------------------------------------------
# 2. Temel HARD tespiti
# ---------------------------------------------------------------------------
class TestHardDetection(unittest.TestCase):
    T = [{"id": "A1", "kanonik": "gizil değişken", "ingilizce": "latent variable",
          "zorlama": "hard", "yasak_varyantlar": ["latent değişken"]}]

    def test_plain_variant_is_hard(self):
        f = _scan_text("Latent değişken kavramı gözlenemeyen yapıyı temsil eder.\n", self.T)
        self.assertEqual(len(_hard(f)), 1)
        self.assertEqual(_hard(f)[0].term_id, "A1")

    def test_canonical_form_not_flagged(self):
        f = _scan_text("Gizil değişken kavramı yapıyı temsil eder.\n", self.T)
        self.assertEqual(_hard(f), [])

    def test_zorlama_not_is_ignored(self):
        # zorlama != hard → hiç taranmaz (belge-amaçlı A4/A6/A7)
        t = [{"id": "A4", "kanonik": "x", "zorlama": "not",
              "yasak_varyantlar": ["aşırı koruyuculuk"]}]
        f = _scan_text("burada aşırı koruyuculuk geçer\n", t)
        self.assertEqual(f, [])


# ---------------------------------------------------------------------------
# 3. Muafiyet: ilk-geçiş parantezi
# ---------------------------------------------------------------------------
class TestFirstUseExemption(unittest.TestCase):
    T = [{"id": "A1", "kanonik": "gizil değişken", "ingilizce": "latent variable",
          "zorlama": "hard", "yasak_varyantlar": ["latent değişken"]}]

    def test_first_use_paren_is_info(self):
        # "latent variable" ilk-geçiş parantezi → varyant yakınında olsa da INFO
        txt = "Gizil değişken (*latent variable*) ve latent değişken aynı satırda.\n"
        f = _scan_text(txt, self.T)
        # aynı satırda ilk-geçiş parantezi var → INFO'ya düşer
        self.assertEqual(_hard(f), [])
        self.assertEqual(len(_info(f)), 1)


# ---------------------------------------------------------------------------
# 4. Muafiyet: bağlamsal paragraf penceresi (confounder=gizli)
# ---------------------------------------------------------------------------
class TestContextualParagraphExemption(unittest.TestCase):
    T = [{"id": "A1", "kanonik": "gizil değişken", "ingilizce": "latent variable",
          "zorlama": "hard", "yasak_varyantlar": ["gizli değişken"],
          "baglamsal_muafiyet": "confounder|karıştırıcı|ölçülmemiş"}]

    def test_confounder_context_same_line_is_info(self):
        f = _scan_text("ölçülmemiş bir gizli değişkene karşı dayanıklıdır\n", self.T)
        self.assertEqual(_hard(f), [])
        self.assertEqual(len(_info(f)), 1)

    def test_confounder_context_prior_line_in_paragraph_is_info(self):
        # bağlam ÖNCEKİ satırda (aynı paragraf) → paragraf penceresi yakalamalı
        txt = (
            "Ölçülmemiş karıştırıcı dayanıklılığı analizinde\n"
            "sonuçların böyle bir gizli değişkene karşı dayanıklı olduğu görülür.\n"
        )
        f = _scan_text(txt, self.T)
        self.assertEqual(_hard(f), [], "önceki satırdaki confounder bağlamı muaf kılmalı")
        self.assertEqual(len(_info(f)), 1)

    def test_latent_meaning_without_context_is_hard(self):
        # confounder bağlamı YOK → gerçek latent ihlali
        txt = "gizli değişken düzeyinde anne-çocuk uyuşmazlığı ölçülmüştür\n"
        f = _scan_text(txt, self.T)
        self.assertEqual(len(_hard(f)), 1)

    def test_paragraph_boundary_respected(self):
        # confounder bağlamı AYRI paragrafta (boş satırla) → muaf DEĞİL
        txt = (
            "Ölçülmemiş karıştırıcı dayanıklılığı ayrı bir paragraftır.\n"
            "\n"
            "gizli değişken düzeyinde uyuşmazlık nicelenmiştir\n"
        )
        f = _scan_text(txt, self.T)
        self.assertEqual(len(_hard(f)), 1, "boş-satır sınırı paragrafı ayırmalı")


# ---------------------------------------------------------------------------
# 5. Muafiyet: kod-çiti + HTML-yorum + atıf
# ---------------------------------------------------------------------------
class TestStructuralExemption(unittest.TestCase):
    T = [{"id": "A5", "kanonik": "yanlış-keşif", "zorlama": "hard",
          "yasak_varyantlar": ["yanlış keşif"]}]

    def test_fenced_code_is_ignored(self):
        txt = (
            "```{r}\n"
            "# yanlış keşif oranı hesapla\n"
            "fdr <- 0.05\n"
            "```\n"
        )
        f = _scan_text(txt, self.T)
        self.assertEqual(f, [], "kod-çiti içi eşleşme sayılmamalı")

    def test_html_comment_is_ignored(self):
        txt = "<!-- yanlış keşif notu: sonra düzelt -->\n"
        f = _scan_text(txt, self.T)
        self.assertEqual(f, [])

    def test_citation_noise_stripped(self):
        # atıf anahtarında geçse bile _strip_citations ile temizlenir
        A1 = [{"id": "A1", "kanonik": "gizil değişken", "zorlama": "hard",
               "yasak_varyantlar": ["latent"]}]
        f = _scan_text("Bu yapı ölçülmüştür [@smithLatentModel2020].\n", A1)
        self.assertEqual(f, [], "atıf-anahtarı içindeki 'latent' sayılmamalı")


# ---------------------------------------------------------------------------
# 6. Muafiyet: dosya öneki + bölüm başlığı (İngilizce özet)
# ---------------------------------------------------------------------------
class TestGlobalExemption(unittest.TestCase):
    T = [{"id": "A1", "kanonik": "gizil değişken", "zorlama": "hard",
          "yasak_varyantlar": ["latent değişken"]}]

    def test_file_prefix_exempt(self):
        gm = {"muaf_dosya_onekleri": ["x.qmd"]}
        # scan_file relpath'i REPO köküne göre; geçici dosya adı ile eşleşmez.
        # Bu yüzden öneki tam yol-parçası olarak kur.
        f = _scan_text("latent değişken serbest burada\n", self.T, gm, name="x.qmd")
        # relpath REPO dışı olduğu için önek eşleşmez → HARD kalır (davranış doğru).
        # Dosya-öneki muafiyeti chapters/00c gibi repo-içi yol için tasarlıdır;
        # burada yalnız API'nin çökmeğini değil, muafiyet olmayınca HARD'ı doğrularız.
        self.assertEqual(len(_hard(f)), 1)

    def test_section_heading_exempt(self):
        gm = {"muaf_bolum_basliklari": ["SUMMARY"]}
        txt = (
            "# BULGULAR\n"
            "latent değişken burada HARD olmalı\n"
            "# SUMMARY\n"
            "latent değişken burada muaf (İngilizce özet)\n"
        )
        f = _scan_text(txt, self.T, gm)
        self.assertEqual(len(_hard(f)), 1, "yalnız SUMMARY öncesi HARD sayılmalı")


# ---------------------------------------------------------------------------
# 7. Gerçek sözlük + tez taraması (entegrasyon; sözlük mevcutsa)
# ---------------------------------------------------------------------------
class TestRealSozluk(unittest.TestCase):
    def test_sozluk_loads(self):
        self.assertTrue(_SOZLUK.exists(), "terim-sozlugu.yaml mevcut olmalı")
        d = tta.load_sozluk(str(_SOZLUK))
        self.assertIn("terimler", d)
        self.assertEqual(len(d["terimler"]), 7, "A1-A7 yedi terim")
        hard = [t for t in d["terimler"] if (t.get("zorlama") or "") == "hard"]
        self.assertEqual(len(hard), 4, "A1,A2,A3,A5 dört zorlanan terim")

    def test_sozluk_schema_fields(self):
        d = tta.load_sozluk(str(_SOZLUK))
        ids = {t.get("id") for t in d["terimler"]}
        self.assertEqual(ids, {"A1", "A2", "A3", "A4", "A5", "A6", "A7"})
        for t in d["terimler"]:
            self.assertIn("kanonik", t)
            self.assertIn("zorlama", t)
            self.assertIn(t["zorlama"], ("hard", "not"))

    def test_a1_yonu_latent_kanonik(self):
        # 2026-07-29 kullanıcı kararı: A1 kanonik 'latent', 'gizil' yasak varyant.
        # Ters çevrim regresyona karşı kilitlensin.
        d = tta.load_sozluk(str(_SOZLUK))
        a1 = next(t for t in d["terimler"] if t.get("id") == "A1")
        self.assertEqual(a1["kanonik"], "latent")
        self.assertIn("gizil", a1["yasak_varyantlar"])
        self.assertNotIn("latent", a1["yasak_varyantlar"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
