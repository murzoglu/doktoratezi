#!/usr/bin/env python3
"""csr_causal_label_audit.py için saf-mantık regresyon testleri.

Ağ çağrısı YAPMAZ. Bu oturumda eklenen kod-fence farkındalığını kilitler:
fenced kod bloğu (```{r}, ```python, ```) içindeki metin analiz düzyazısı
değil kod-literalidir (ör. ggplot etiketi label = "Net fayda") ve nedensel/
aksiyon dil taramasında yanlış pozitif üretmemelidir. HTML yorum atlama ve
düzyazı korunumu davranışları da doğrulanır.

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_csr_causal_label_audit.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import tempfile
import unittest

_MOD = (
    pathlib.Path(__file__).resolve().parents[1]
    / "scripts" / "util" / "csr_causal_label_audit.py"
)
spec = importlib.util.spec_from_file_location("csr_causal_label_audit", _MOD)
cl = importlib.util.module_from_spec(spec)
sys.modules["csr_causal_label_audit"] = cl
spec.loader.exec_module(cl)


class TestCodeFenceAwareness(unittest.TestCase):
    def _write(self, text: str) -> pathlib.Path:
        f = tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        )
        f.write(text)
        f.close()
        return pathlib.Path(f.name)

    def test_code_fence_lines_are_skipped(self):
        """Fenced R bloğu içindeki nedensel/aksiyon dili görünür satır
        listesine girmez; düzyazı satırları girer."""
        md = (
            "Düzyazı: gözlemsel tasarım nedensel yön kurmaz.\n"
            "```{r}\n"
            'ggplot2::labs(y = "Net fayda", subtitle = "Herkesi tedavi et")\n'
            "```\n"
            "Kapanış düzyazı: bulgu keşifsel düzeyde yorumlanmıştır.\n"
        )
        p = self._write(md)
        try:
            visible = cl.iter_visible_lines(p)
            joined = " ".join(x.text for x in visible)
            self.assertIn("gözlemsel", joined)       # düzyazı korunur
            self.assertIn("keşifsel", joined)        # düzyazı korunur
            self.assertNotIn("Net fayda", joined)    # kod-literal atlanır
            self.assertNotIn("tedavi et", joined)    # kod-literal atlanır
        finally:
            p.unlink()

    def test_nested_fences_toggle_correctly(self):
        """Ard arda iki kod bloğu arasındaki düzyazı görünür kalır."""
        md = (
            '```{r}\nlabs(y = "neden ol")\n```\n'
            "Arada düzyazı: aracılık analizi yön kanıtı sağlamaz.\n"
            '```python\ntitle = "yol açar"\n```\n'
            "Kapanış: sonuç betimseldir.\n"
        )
        p = self._write(md)
        try:
            joined = " ".join(x.text for x in cl.iter_visible_lines(p))
            self.assertIn("aracılık", joined)
            self.assertIn("betimsel", joined)
            self.assertNotIn("neden ol", joined)
            self.assertNotIn("yol açar", joined)
        finally:
            p.unlink()

    def test_html_comment_still_skipped(self):
        """Kod-fence eklemesi HTML yorum atlamasını bozmaz."""
        md = (
            "Görünür düzyazı bir.\n"
            "<!-- gizli neden ol yorumu -->\n"
            "Görünür düzyazı iki.\n"
        )
        p = self._write(md)
        try:
            joined = " ".join(x.text for x in cl.iter_visible_lines(p))
            self.assertIn("düzyazı bir", joined)
            self.assertIn("düzyazı iki", joined)
            self.assertNotIn("gizli", joined)
        finally:
            p.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
