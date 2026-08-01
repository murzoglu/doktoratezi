#!/usr/bin/env python3
"""thesis_semantic.py saf-mantık regresyon testleri (stdlib unittest).

Ağ/gateway çağrısı YAPMAZ: semantic_core fonksiyonları monkeypatch'lenir.
Exit-code mantığını (HARD/advisory/strict), degrade yolunu ve paragraf
çıkarımını doğrular.

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_thesis_semantic.py
"""
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_MOD = os.path.join(os.path.dirname(_HERE), "scripts", "util", "thesis_semantic.py")
_spec = importlib.util.spec_from_file_location("thesis_semantic", _MOD)
ts = importlib.util.module_from_spec(_spec)
sys.modules["thesis_semantic"] = ts
_spec.loader.exec_module(ts)

_BIB = (
    "@article{A, title={Parental overprotection in type 1 diabetes},"
    " author={X}, year={2020}}\n"
    "@article{B, title={Overprotective parenting in T1DM children},"
    " author={Y}, year={2021}}\n"
)


class TestBibDup(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.bib = os.path.join(self.tmp, "r.bib")
        with open(self.bib, "w", encoding="utf-8") as f:
            f.write(_BIB)
        self._orig = ts.sc.dedup_matrix

    def tearDown(self):
        ts.sc.dedup_matrix = self._orig

    def test_hard_strict_exits_1(self):
        ts.sc.dedup_matrix = lambda items, threshold=None: [{"a": "A", "b": "B", "sim": 0.97}]
        res, code = ts.cmd_bib_dup(self.bib, 0.90, 0.96, strict=True)
        self.assertEqual(code, 1)
        self.assertEqual(len(res["hard"]), 1)

    def test_hard_without_strict_is_advisory(self):
        ts.sc.dedup_matrix = lambda items, threshold=None: [{"a": "A", "b": "B", "sim": 0.97}]
        res, code = ts.cmd_bib_dup(self.bib, 0.90, 0.96, strict=False)
        self.assertEqual(code, 2)

    def test_advisory_only(self):
        ts.sc.dedup_matrix = lambda items, threshold=None: [{"a": "A", "b": "B", "sim": 0.92}]
        res, code = ts.cmd_bib_dup(self.bib, 0.90, 0.96, strict=True)
        self.assertEqual(code, 2)
        self.assertEqual(len(res["advisory"]), 1)
        self.assertEqual(res["hard"], [])

    def test_clean(self):
        ts.sc.dedup_matrix = lambda items, threshold=None: []
        res, code = ts.cmd_bib_dup(self.bib, 0.90, 0.96, strict=True)
        self.assertEqual(code, 0)

    def test_degrade_to_lexical(self):
        def _boom(items, threshold=None):
            raise ts.sc.EmbeddingUnavailable("down")
        ts.sc.dedup_matrix = _boom
        _obh = ts.bh.check_dedup
        ts.bh.check_dedup = lambda entries, threshold=0.85: [{"a": "A", "b": "B", "sim": 0.9}]
        try:
            res, code = ts.cmd_bib_dup(self.bib, 0.90, 0.96, strict=True)
            self.assertEqual(res["mode"], "lexical-fallback")
            self.assertEqual(code, 2)          # strict olsa bile lexical HARD üretmez
        finally:
            ts.bh.check_dedup = _obh


class TestParagraphs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.f = os.path.join(self.tmp, "c.qmd")
        with open(self.f, "w", encoding="utf-8") as f:
            f.write(
                "# BAŞLIK atlanmalı çünkü başlık satırı ve yeterince uzun değil\n\n"
                "```{r}\nbu kod bloğu tamamen atlanmalı ve içindeki uzun uzun uzun "
                "cümleler paragraf sayılmamalı kesinlikle hayır asla olmaz\n```\n\n"
                "Bu gerçek bir manuskript paragrafıdır ve yirmi beş kelimeden fazla "
                "içerdiği için semantik tekrar taramasına dahil edilmelidir; tip 1 "
                "diyabet ve ebeveyn tutumu bağlamında yazılmış uzun bir cümledir.\n\n"
                "kısa satır\n"
            )

    def test_extraction_skips_fence_heading_short(self):
        paras = ts._paragraphs([self.f])
        self.assertEqual(len(paras), 1)
        self.assertIn("gerçek bir manuskript", paras[0][1])


class TestRedundancy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.f = os.path.join(self.tmp, "c.qmd")
        with open(self.f, "w", encoding="utf-8") as f:
            f.write(
                "birinci uzun manuskript paragrafı yirmi beş kelime sınırını rahatça "
                "aşacak kadar uzundur ve tip 1 diyabet ile ebeveyn tutumu üzerine "
                "yazılmış olup burada ayrıca birkaç ek kelime daha bulunmaktadır ki "
                "toplam sayı sınırı geçsin diye eklenmiştir.\n\n"
                "ikinci uzun manuskript paragrafı yine yirmi beş kelime sınırını "
                "rahatça aşacak kadar uzundur ve glisemik kontrol üzerine yazılmış "
                "olup burada da birkaç ek kelime daha bulunmaktadır ki toplam sayı "
                "sınırı geçsin diye özellikle eklenmiştir.\n"
            )
        self._orig = ts.sc.redundancy_pairs

    def tearDown(self):
        ts.sc.redundancy_pairs = self._orig

    def test_pairs_exit_2(self):
        ts.sc.redundancy_pairs = lambda paras, threshold=None: [{"a": 0, "b": 1, "sim": 0.91}]
        res, code = ts.cmd_redundancy([self.f], 0.88)
        self.assertEqual(code, 2)
        self.assertEqual(res["pairs"][0]["sim"], 0.91)
        self.assertIn("file", res["pairs"][0]["a"])

    def test_clean_exit_0(self):
        ts.sc.redundancy_pairs = lambda paras, threshold=None: []
        _res, code = ts.cmd_redundancy([self.f], 0.88)
        self.assertEqual(code, 0)

    def test_degrade_note(self):
        def _boom(paras, threshold=None):
            raise ts.sc.EmbeddingUnavailable("down")
        ts.sc.redundancy_pairs = _boom
        res, code = ts.cmd_redundancy([self.f], 0.88)
        self.assertEqual(res["mode"], "unavailable")
        self.assertEqual(code, 0)
        self.assertIn("tr_corpus_audit", res["note"])


if __name__ == "__main__":
    unittest.main()
