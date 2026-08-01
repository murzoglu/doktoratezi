#!/usr/bin/env python3
"""graphrag_query.py için saf-mantık regresyon testleri.

Canlı MCP/ağ çağrısı YAPMAZ: kavram-tetikleyici eşlemeyi (_candidate_concepts)
ve markdown render'ını sahte bir bağlam paketiyle doğrular. Füzyon/çapraz-
doğrulama mantığı graphrag_context içinde canlı client gerektirdiği için burada
test edilmez; onun kanıtı healthcheck ANAMNESIS katmanı + canlı çalıştırmadır.

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_graphrag_query.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

_MOD = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "mcp" / "graphrag_query.py"
spec = importlib.util.spec_from_file_location("graphrag_query", _MOD)
gq = importlib.util.module_from_spec(spec)
sys.modules["graphrag_query"] = gq
spec.loader.exec_module(gq)


class TestCandidateConcepts(unittest.TestCase):
    def test_turkish_triggers(self):
        c = gq._candidate_concepts("aşırı koruma ve ebeveyn tutumu")
        self.assertIn("Aşırı koruma", c)
        self.assertIn("Ebeveynlik tutumu", c)

    def test_english_triggers(self):
        c = gq._candidate_concepts("parental overprotection and glycemic control")
        self.assertIn("Aşırı koruma", c)
        self.assertIn("HbA1c / metabolik kontrol", c)

    def test_diabetes_and_sibling(self):
        c = gq._candidate_concepts("type 1 diabetes sibling adjustment")
        self.assertIn("Tip 1 diyabet", c)
        self.assertIn("Kardeş uyumu", c)

    def test_no_match_returns_empty(self):
        self.assertEqual(gq._candidate_concepts("tamamen alakasız metin xyz"), [])


class TestRenderMarkdown(unittest.TestCase):
    def _pkg(self):
        return {
            "query": "aşırı koruma",
            "sub_queries": ["overprotection"],
            "retrieval": {"pipeline": "vector∥bm25→rrf→rerank", "k": 2,
                          "chunks": 2, "graph_edges": 0},
            "chunks": [
                {"doc_id": "compas2012coping", "score": 0.001, "text": "chronic illness coping",
                 "galileo_score": 0.72, "fused_score": 0.63, "anamnesis_rank": 2},
                {"doc_id": "doctrine", "score": 0.03, "text": "protocol text",
                 "galileo_score": 0.51, "fused_score": 0.71, "anamnesis_rank": 1},
            ],
            "graph_expansion": {"Aşırı koruma": ["pinquart2013", "rosland2012family"]},
            "cross_validation": {
                "enabled": True, "scored": 2,
                "fused_order": ["doctrine", "compas2012coping"],
                "flags": [{"doc_id": "compas2012coping", "type": "gömülü-ilgili",
                           "anamnesis_rank": 2, "galileo": 0.72,
                           "note": "alt-sırada ama gemini yüksek"}],
            },
            "provenance_note": "test-note",
        }

    def test_render_sections_present(self):
        md = gq._render_markdown(self._pkg())
        self.assertIn("GraphRAG Bağlam Paketi", md)
        self.assertIn("Füzyon Yeniden-Sıralaması", md)
        self.assertIn("Bilgi Grafiği Genişletmesi", md)
        self.assertIn("Çapraz-Doğrulama Uyuşmazlıkları", md)

    def test_render_shows_fused_and_galileo(self):
        md = gq._render_markdown(self._pkg())
        self.assertIn("füzyon=", md)
        self.assertIn("galileo=", md)
        self.assertIn("gömülü-ilgili", md)


if __name__ == "__main__":
    unittest.main()
