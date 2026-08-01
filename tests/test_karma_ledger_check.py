"""karma_ledger_check drift-guard testleri (stdlib unittest)."""
import importlib.util
import os
import tempfile
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_MOD = os.path.join(os.path.dirname(_HERE), "scripts", "util", "karma_ledger_check.py")
_spec = importlib.util.spec_from_file_location("karma_ledger_check", _MOD)
klc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(klc)

HEADER = "\t".join(klc.COLUMNS)


def _row(**kw):
    d = {c: "x" for c in klc.COLUMNS}
    d.update(kw)
    return "\t".join(d[c] for c in klc.COLUMNS)


class TestKarmaLedgerCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        with open(os.path.join(self.tmp, "nicel.qmd"), "w", encoding="utf-8") as f:
            f.write("### H1 Karar Kutusu {#h1-karar}\n"
                    "DM lehine reddetme yükselmesi gözlenmiştir.\n")
        with open(os.path.join(self.tmp, "nitel.qmd"), "w", encoding="utf-8") as f:
            f.write("## Tema 3 {#tema-3}\n"
                    "hastalığı hem normalleştirme hem yük olarak taşıma\n")

    def _led(self, *rows):
        p = os.path.join(self.tmp, "led.tsv")
        with open(p, "w", encoding="utf-8") as f:
            f.write(HEADER + "\n" + "\n".join(rows) + "\n")
        return p

    def _ok_row(self, **over):
        base = dict(
            id="h1", iliski_turu="açıklayıcı-genişleme",
            nicel_ankraj="nicel.qmd#h1-karar",
            nicel_verdikt_ozet="DM lehine reddetme yükselmesi",
            nitel_ankraj="nitel.qmd#tema-3",
            nitel_oruntu_ozet="normalleştirme hem yük olarak taşıma",
        )
        base.update(over)
        return _row(**base)

    def test_clean(self):
        sev, f = klc.check(self._led(self._ok_row()), root=self.tmp)
        self.assertEqual(sev, 0, f)

    def test_hard_missing_anchor(self):
        sev, _ = klc.check(self._led(self._ok_row(nicel_ankraj="nicel.qmd#YOK")), root=self.tmp)
        self.assertEqual(sev, 1)

    def test_hard_missing_file(self):
        sev, _ = klc.check(self._led(self._ok_row(nicel_ankraj="yok.qmd#h1-karar")), root=self.tmp)
        self.assertEqual(sev, 1)

    def test_soft_snippet_drift(self):
        sev, _ = klc.check(self._led(self._ok_row(nicel_verdikt_ozet="BURADA OLMAYAN CÜMLE")), root=self.tmp)
        self.assertEqual(sev, 2)

    def test_soft_invalid_iliski(self):
        sev, _ = klc.check(self._led(self._ok_row(iliski_turu="GECERSIZ")), root=self.tmp)
        self.assertEqual(sev, 2)

    def test_hard_dominates_soft(self):
        sev, _ = klc.check(
            self._led(self._ok_row(iliski_turu="GECERSIZ", nicel_ankraj="nicel.qmd#YOK")),
            root=self.tmp)
        self.assertEqual(sev, 1)

    def test_bad_header(self):
        p = os.path.join(self.tmp, "bad.tsv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("wrong\theader\n")
        with self.assertRaises(ValueError):
            klc.check(p, root=self.tmp)

    def test_bad_column_count(self):
        p = os.path.join(self.tmp, "bad2.tsv")
        with open(p, "w", encoding="utf-8") as f:
            f.write(HEADER + "\n" + "a\tb\n")
        with self.assertRaises(ValueError):
            klc.check(p, root=self.tmp)


class _FakeSem:
    """semantic_core taklidi (offline). mode: rescue|nomatch|down."""
    class EmbeddingUnavailable(Exception):
        pass

    def __init__(self, mode):
        self.mode = mode

    def embed(self, texts):
        if self.mode == "down":
            raise self.EmbeddingUnavailable("down")
        if self.mode == "rescue":
            return [[1.0, 0.0] for _ in texts]           # hepsi aynı → cosine 1.0
        return [[1.0, 0.0]] + [[0.0, 1.0] for _ in texts[1:]]  # ozet dik → cosine 0

    @staticmethod
    def cosine(a, b):
        import math
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return 0.0 if na == 0 or nb == 0 else dot / (na * nb)


class TestSemanticRescue(unittest.TestCase):
    """Substring-drift'in semantik rescue katmanı (spec: karma tema↔yapı)."""
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        with open(os.path.join(self.tmp, "nicel.qmd"), "w", encoding="utf-8") as f:
            f.write("### H1 Karar Kutusu {#h1-karar}\n"
                    "DM lehine reddetme yükselmesi gözlenmiştir.\n")
        with open(os.path.join(self.tmp, "nitel.qmd"), "w", encoding="utf-8") as f:
            f.write("## Tema 3 {#tema-3}\n"
                    "hastalığı hem normalleştirme hem yük olarak taşıma\n")
        self._orig = klc._get_semantic

    def tearDown(self):
        klc._get_semantic = self._orig

    def _led(self, *rows):
        p = os.path.join(self.tmp, "led.tsv")
        with open(p, "w", encoding="utf-8") as f:
            f.write(HEADER + "\n" + "\n".join(rows) + "\n")
        return p

    def _drift_row(self):
        # nicel özet kaynakta substring DEĞİL (parafraz) → drift tetiklenir
        return _row(id="h1", iliski_turu="uyum",
                    nicel_ankraj="nicel.qmd#h1-karar",
                    nicel_verdikt_ozet="reddetme algısı DM grubunda belirgin artış",
                    nitel_ankraj="nitel.qmd#tema-3",
                    nitel_oruntu_ozet="hastalığı hem normalleştirme hem yük olarak taşıma")

    def test_default_off_is_soft(self):
        # semantic kapalı → mevcut davranış (SOFT), ağ yok
        sev, _ = klc.check(self._led(self._drift_row()), root=self.tmp)
        self.assertEqual(sev, 2)

    def test_semantic_rescue_paraphrase_to_info(self):
        klc._get_semantic = lambda: _FakeSem("rescue")
        sev, finds = klc.check(self._led(self._drift_row()), root=self.tmp, semantic=True)
        self.assertEqual(sev, 0)                       # INFO severity'yi yükseltmez
        self.assertTrue(any(s == "INFO" for s, _, _ in finds))

    def test_semantic_nomatch_stays_soft(self):
        klc._get_semantic = lambda: _FakeSem("nomatch")
        sev, finds = klc.check(self._led(self._drift_row()), root=self.tmp, semantic=True)
        self.assertEqual(sev, 2)
        self.assertTrue(any(s == "SOFT" for s, _, _ in finds))

    def test_embedding_down_falls_back_soft(self):
        klc._get_semantic = lambda: _FakeSem("down")
        sev, finds = klc.check(self._led(self._drift_row()), root=self.tmp, semantic=True)
        self.assertEqual(sev, 2)                       # çökme yok, SOFT'a düşer
        self.assertTrue(any("semantik yok" in m for _, _, m in finds))


if __name__ == "__main__":
    unittest.main()
