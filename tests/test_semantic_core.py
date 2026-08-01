#!/usr/bin/env python3
"""semantic_core.py saf-mantık regresyon testleri (stdlib unittest).

Ağ/gateway çağrısı YAPMAZ: cosine matematiğini, KVKK tripwire'ını ve
dedup/redundancy/match mantığını `embed` monkeypatch'iyle offline doğrular.
Canlı embed yalnız opsiyonel smoke'ta (erişilemezse atlanır).

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_semantic_core.py
"""
from __future__ import annotations

import importlib.util
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_MOD = os.path.join(os.path.dirname(_HERE), "scripts", "eval", "semantic_core.py")
_spec = importlib.util.spec_from_file_location("semantic_core", _MOD)
sc = importlib.util.module_from_spec(_spec)
sys.modules["semantic_core"] = sc
_spec.loader.exec_module(sc)


class TestCosine(unittest.TestCase):
    def test_identical(self):
        self.assertAlmostEqual(sc.cosine([1, 0], [1, 0]), 1.0)

    def test_orthogonal(self):
        self.assertAlmostEqual(sc.cosine([1, 0], [0, 1]), 0.0)

    def test_opposite(self):
        self.assertAlmostEqual(sc.cosine([1, 0], [-1, 0]), -1.0)

    def test_zero_vector_safe(self):
        self.assertEqual(sc.cosine([0, 0], [1, 1]), 0.0)


class TestKvkkTripwire(unittest.TestCase):
    def test_tc_kimlik_rejected(self):
        with self.assertRaises(sc.KvkkViolation):
            sc._kvkk_tripwire(["katılımcı 12345678901 numaralı"])

    def test_ad_soyad_column_rejected(self):
        with self.assertRaises(sc.KvkkViolation):
            sc._kvkk_tripwire(["Adı Soyadı: gizli"])
        with self.assertRaises(sc.KvkkViolation):
            sc._kvkk_tripwire(["ad_soyad kolonu"])

    def test_manuscript_text_passes(self):
        # Yayımlanmış manuskript/literatür metni engellenmemeli (yanlış-pozitif yok).
        sc._kvkk_tripwire([
            "Aşırı korumada etki büyüklüğü g=0,39 bildirilmiştir (Pinquart, 2013).",
            "Tip 1 diyabette ebeveyn tutumu ve glisemik kontrol ilişkisi.",
            "DOI 10.1016/S0272-7358(98)00100-7 numaralı meta-analiz",  # 13+ hane değil
        ])

    def test_embed_guards_before_network(self):
        # embed() önce tripwire koşar; PII girişi ağ denemeden reddedilir.
        with self.assertRaises(sc.KvkkViolation):
            sc.embed(["Adı Soyadı: X", "normal metin"])


# --- dedup/redundancy/match: embed monkeypatch ile deterministik (offline) ---
_VECS = {
    "over1": [1.0, 0.0, 0.0],
    "over2": [0.98, 0.20, 0.0],   # over1'e çok yakın (near-dup)
    "hba1c": [0.0, 0.0, 1.0],     # dik (farklı konu)
}


def _fake_embed(texts):
    out = []
    for t in texts:
        key = next((k for k in _VECS if k in t), None)
        out.append(_VECS[key] if key else [0.0, 0.0, 0.0])
    return out


class TestDedupRedundancyMatch(unittest.TestCase):
    def setUp(self):
        self._orig = sc.embed
        sc.embed = _fake_embed

    def tearDown(self):
        sc.embed = self._orig

    def test_dedup_matrix_finds_near_dup_only(self):
        items = [
            {"key": "A", "title": "over1 parenting"},
            {"key": "B", "title": "over2 overprotection"},
            {"key": "C", "title": "hba1c glycemic"},
        ]
        dups = sc.dedup_matrix(items, threshold=0.9)
        self.assertEqual(len(dups), 1)
        self.assertEqual({dups[0]["a"], dups[0]["b"]}, {"A", "B"})
        self.assertGreaterEqual(dups[0]["sim"], 0.9)

    def test_dedup_threshold_respected(self):
        items = [{"key": "A", "title": "over1"}, {"key": "C", "title": "hba1c"}]
        self.assertEqual(sc.dedup_matrix(items, threshold=0.5), [])

    def test_redundancy_pairs(self):
        paras = ["over1 paragraf", "over2 paragraf", "hba1c paragraf"]
        red = sc.redundancy_pairs(paras, threshold=0.9)
        self.assertEqual(len(red), 1)
        self.assertEqual({red[0]["a"], red[0]["b"]}, {0, 1})

    def test_match_matrix_best(self):
        a = ["over1 tema", "hba1c tema"]
        b = ["over2 yapı", "hba1c yapı"]
        res = sc.match_matrix(a, b)
        self.assertEqual(res["best"][0]["b"], 0)   # over1 -> over2
        self.assertEqual(res["best"][1]["b"], 1)   # hba1c -> hba1c

    def test_embedding_unavailable_propagates(self):
        def _boom(_texts):
            raise sc.EmbeddingUnavailable("down")
        sc.embed = _boom
        with self.assertRaises(sc.EmbeddingUnavailable):
            sc.dedup_matrix([{"key": "A", "title": "x"}, {"key": "B", "title": "y"}])


if __name__ == "__main__":
    unittest.main()
