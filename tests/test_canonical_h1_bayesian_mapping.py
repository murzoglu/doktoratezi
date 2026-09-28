#!/usr/bin/env python3
"""Kanonik H1 Bayesçi özetinin tez yüzeylerine aktarımını kilitler.

Amaç: Üretilmiş H1 aggregate tablosundaki reddetme/aşırı koruma BF10
değerlerinin aktif tez özeti, bulgular ve tartışmada kaynak-okumalı kalmasını
sağlamak. Bağımsız klinik raporun kendi figür girdileri ayrı test edilir.
Tarihsel kalite-kontrol belgeleri kasıtlı olarak kapsam dışıdır. Yalnız
türetilmiş/özet CSV okunur; katılımcı verisi okunmaz.

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_canonical_h1_bayesian_mapping.py
"""
from __future__ import annotations

import csv
import pathlib
import re
import unittest


_ROOT = pathlib.Path(__file__).resolve().parents[1]
_TABLES = _ROOT / "outputs" / "tables"
_CANONICAL_SOURCES = {
    "ozet": _ROOT / "chapters" / "00c_ozet_summary.qmd",
    "bulgular": _ROOT / "chapters" / "04_bulgular.qmd",
    "tartisma": _ROOT / "chapters" / "05_tartisma_ve_sonuc.qmd",
}
_CLINICAL_REPORT = _ROOT / "docs" / "CLINICAL-STUDY-REPORT-FINAL.qmd"


def _load_csv(name: str) -> list[dict[str, str]]:
    with (_TABLES / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _num(value: str) -> float:
    return float(value.replace(",", "."))


class TestCanonicalH1BayesianMapping(unittest.TestCase):
    """Aktif yayın yüzeyleri, üretilmiş H1 Bayesçi tablosundan sapmaz."""

    CSV = "apa_t07_h1_bayesian.csv"

    def setUp(self):
        if not (_TABLES / self.CSV).exists():
            self.skipTest(f"{self.CSV} yok (gitignored artefakt)")
        self.rows = _load_csv(self.CSV)
        self.texts = {
            name: path.read_text(encoding="utf-8")
            for name, path in _CANONICAL_SOURCES.items()
        }

    def _bf10(self, outcome: str) -> float:
        for row in self.rows:
            if row.get("Sonuc") == outcome:
                return _num(row["BF10"])
        self.fail(f"kaynak satır bulunamadı: {outcome}")

    def test_source_values_support_h1_for_rejection_and_protection(self):
        self.assertGreater(self._bf10("EMBU-C Reddetme"), 1)
        self.assertGreater(self._bf10("EMBU-C Aşırı koruma"), 1)

    def test_all_active_thesis_surfaces_read_h1_bfs_from_source(self):
        summary = self.texts["ozet"]
        self.assertIn('summary_h1_bf10("embu_c_reddetme_mean")', summary)
        self.assertIn('summary_h1_bf10("embu_c_asiri_koruma_mean")', summary)
        for name in ("bulgular", "tartisma"):
            with self.subTest(source=name):
                self.assertIn('apa_h1_bf10("embu_c_reddetme_mean")', self.texts[name])
                self.assertIn('apa_h1_bf10("embu_c_asiri_koruma_mean")', self.texts[name])

    def test_stale_h1_bfs_are_absent_from_active_sources(self):
        stale = re.compile(r"BF₁₀\s*=\s*(?:10[,.]55|6[,.]93)")
        for name, text in self.texts.items():
            with self.subTest(source=name):
                self.assertIsNone(stale.search(text))

    def test_h1_figure_inputs_are_loaded_from_generated_csvs(self):
        report = _CLINICAL_REPORT.read_text(encoding="utf-8")
        self.assertIn('h1_bayes <- utils::read.csv(', report)
        self.assertIn('bayes_h1_posterior <- utils::read.csv(', report)

    def test_findings_do_not_reverse_rejection_direction(self):
        findings = self.texts["bulgular"]
        for stale in (
            "daha az reddedilmiş",
            "daha az reddedilme",
            "daha az reddedildiği",
            "daha az reddedilme hissediyor",
        ):
            self.assertNotIn(stale, findings)
        self.assertTrue(
            any(
                expression in findings
                for expression in ("daha fazla reddedilme", "daha reddedici")
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
