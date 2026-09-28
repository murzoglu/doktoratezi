#!/usr/bin/env python3
"""ch05 nihai tartışma kaynağı sözleşmesi.

Tartışma bölümü kullanıcı tarafından sağlanan başlık hiyerarşili Word metnine
dayanır. Sayısal sonuçların kaynak-artefakt eşlemesi sonuç bölümü ve
istatistik/audit kapılarında sınanır; burada eski taslağa ait literal ICC ve
Bayes faktörü sözleşmeleri zorlanmaz.

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_ch05_source_mapping.py
"""
from __future__ import annotations

import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters" / "05_tartisma_ve_sonuc.qmd"
BIB = ROOT / "references" / "references.bib"


class TestCh05DiscussionContract(unittest.TestCase):
    def setUp(self):
        self.text = CHAPTER.read_text(encoding="utf-8")
        self.bib = BIB.read_text(encoding="utf-8")

    def test_placeholder_is_replaced(self):
        self.assertNotIn("Yer tutucu:", self.text)
        self.assertIn("# TARTIŞMA ve SONUÇ", self.text)

    def test_word_heading_hierarchy_is_preserved(self):
        headings = [
            "## Bulguların Genel Değerlendirilmesi",
            "## Hipotez Temelli Bulguların Tartışılması",
            "### H1 — Çocukların algıladığı ebeveynlik",
            "### H2 — Kardeş ilişkileri",
            "### H3 — Annelerin ebeveynlik öz-bildirimi",
            "### H4 — Anne depresyonu ve ebeveynlik",
            "### H5 — Anne–çocuk değerlendirmeleri arasındaki tutarlılık",
            "## Hipotez Dışı ve Keşifsel Bulguların Tartışılması",
            "## Nitel Bulguların Tartışılması",
            "## Nicel ve Nitel Bulguların Bütünleştirilmesi",
            "## Sınırlılıklar",
            "## Çalışmanın Güçlü Yönleri",
            "## Sonuç ve Öneriler",
        ]
        positions = [self.text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))

    def test_citations_resolve_in_bibliography(self):
        keys = set(re.findall(r"@(?!sec-)([A-Za-z0-9_]+)", self.text))
        self.assertGreaterEqual(len(keys), 50)
        missing = [
            key
            for key in keys
            if not re.search(rf"^@[A-Za-z]+\{{{re.escape(key)},", self.bib, re.M)
        ]
        self.assertEqual(missing, [])

    def test_latent_terminology_is_consistent(self):
        self.assertIn("Latent profil analizi", self.text)
        self.assertIn("latent sosyoekonomik düzey", self.text)
        self.assertNotRegex(self.text, r"(?i)\bgizli\b|\bgizil\b")


if __name__ == "__main__":
    unittest.main(verbosity=2)
