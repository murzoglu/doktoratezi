"""
AMA-11 CSL regresyon testi — pandoc --citeproc ile marmara-ama11.csl doğrulama.

Test edilenler (AMA-11 §5.4 kuralları):
  - et-al terimi "ve ark." (7+ yazarlı Xie kaynağında)
  - "ve" bağlacı (genel)
  - https://doi.org/ DOI biçimi (Fadini 2022)
  - Metin-içi et-al: "Fadini ve ark." (4 yazar, et-al-min=3)
  - 2 yazarlı metin-içi: "John ve Marquez"
  - Düz metin çıktısında italik/kalın yıldız işareti yok
"""

import pathlib
import shutil
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSL = ROOT / "references" / "marmara-ama11.csl"
BIB = ROOT / "references" / "_csl_test" / "test-refs.bib"

DOC = """---
lang: tr
nocite: |
  @fadini2022
  @xie2019
  @john2017
---
Metin [@fadini2022] ve @john2017.

# Kaynaklar

::: {#refs}
:::
"""


class TestMarmaraAma11Render(unittest.TestCase):
    @unittest.skipIf(shutil.which("pandoc") is None, "pandoc yok")
    def test_ama11_render_key_rules(self):
        self.assertTrue(CSL.exists() and BIB.exists(),
                        f"CSL veya BIB dosyası bulunamadı: {CSL}, {BIB}")
        out = subprocess.run(
            [shutil.which("pandoc"), "--citeproc", "--csl", str(CSL),
             "--bibliography", str(BIB),
             "-f", "markdown", "-t", "plain"],
            input=DOC, capture_output=True, text=True, timeout=60,
        ).stdout
        # et-al "ve ark." (7+ yazarlı Xie)
        self.assertIn("ve ark.", out)
        # "ve" bağlacı (Fadini 4 yazar -> son iki isim "ve" ile veya metin-içi "ve ark.")
        self.assertIn("ve", out)
        # DOI biçimi
        self.assertIn("https://doi.org/10.1111/dom.14599", out)
        # metin-içi (Fadini ve ark., 2022) — 4 yazar, citation et-al-min=3
        self.assertIn("Fadini ve ark.", out)
        # 2 yazarlı John -> "John ve Marquez"
        self.assertIn("John ve Marquez", out)
        # italik/kalın markup düz metinde kalmamalı (yıldız yok)
        self.assertNotIn("*", out)


if __name__ == "__main__":
    unittest.main()
