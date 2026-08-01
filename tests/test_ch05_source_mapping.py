#!/usr/bin/env python3
"""ch05 Tartışma → ch04 Bulgular kaynak-hücre eşleme testi (Öneri C).

Amaç: ch05'te YENİDEN İFADE edilen KENDİ sayısal sonuçlarımızın (β/ICC/p ...),
ch04'ün okuduğu kanonik `outputs/tables/*.csv` üretilmiş artefaktındaki DOĞRU
hücreyle birebir örtüştüğünü kilitlemek. csr_numeric_trace_audit.py (K5-NUM-02)
"herhangi bir CSV hücresine düşüyor mu?" sorusunu genel olarak sorar; bu test ise
her bağlayıcı iddiayı BELİRLİ bir kaynak dosya+değere sabitler. Böylece ch05'te
sayı sürüklenirse (ör. 0,32 → 0,51) ya da ch04 kaynağı değişip ch05 güncellenmezse
kapı FAIL verir. AGENTS.md "Sayısal Bütünlük Kaideleri" (kaynak-tekilliği) altında.

Gizlilik: yalnız türetilmiş/özet CSV hücreleri okunur; satır-düzeyi katılımcı
verisi ne okunur ne raporlanır. Artefaktlar gitignored olduğundan yoklukta SKIP.

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_ch05_source_mapping.py
"""
from __future__ import annotations

import csv
import pathlib
import re
import unittest

_ROOT = pathlib.Path(__file__).resolve().parents[1]
_CH05 = _ROOT / "chapters" / "05_tartisma_ve_sonuc.qmd"
_TABLES = _ROOT / "outputs" / "tables"


def _read_ch05_text() -> str:
    return _CH05.read_text(encoding="utf-8")


def _load_csv(name: str) -> list[dict[str, str]]:
    path = _TABLES / name
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _num(cell: str) -> float:
    """Hücre/token → float (Türkçe virgül ve ICC=/r=/k= önekleri temizlenir)."""
    s = str(cell).strip()
    s = re.sub(r"(?i)^(icc|r|k|b|β|d)\s*=\s*", "", s)
    s = s.replace("−", "-").replace(",", ".")
    m = re.search(r"[-+]?\d*\.?\d+", s)
    if not m:
        raise ValueError(f"sayı ayrıştırılamadı: {cell!r}")
    return float(m.group(0))


def _round_eq(a: float, b: float, decimals: int) -> bool:
    """İki değer, verilen ondalıkta yuvarlandığında eşit mi (yeniden-ifade toleransı)."""
    q = 10 ** (-decimals)
    return abs(round(a, decimals) - round(b, decimals)) <= (0.5 * q + 1e-9)


# ---------------------------------------------------------------------------
# Bağlayıcı eşleme kayıtları: (ch05'te görünmesi gereken metin literali,
#   kaynak CSV, satır seçici (col→value), kaynak sütun, ondalık).
# ch05'teki literal ile kaynak hücre AYNI yuvarlamada eşleşmezse test FAIL.
# ---------------------------------------------------------------------------

class TestCh05IccReddetmeConcordance(unittest.TestCase):
    """Kardeş-arası reddetme algı uyumu (H5 forest/havuzlama): kontrol ICC=0,32; DM ICC=0,00.

    Kanonik kaynak, ch05'te "havuzlama (forest) çözümlemesi" olarak anılan
    `phase2_h5ext_sibling_icc.csv` grup-katmanlı ICC tablosudur (ham Bland-Altman
    değil). ch05 ile ch04 aynı forest kaynağını yeniden ifade eder.
    """

    CSV = "phase2_h5ext_sibling_icc.csv"

    def setUp(self):
        if not (_TABLES / self.CSV).exists():
            self.skipTest(f"{self.CSV} yok (gitignored artefakt)")
        self.rows = _load_csv(self.CSV)
        self.text = _read_ch05_text()

    def _cell(self, subscale: str, group_label: str, col: str) -> float:
        for r in self.rows:
            if (r.get("outcome_subscale") == subscale
                    and r.get("group_label") == group_label):
                return _num(r[col])
        self.fail(f"kaynak satır bulunamadı: {subscale}/{group_label}")

    def test_control_icc_matches_source(self):
        """ch05 'ICC = 0,32' (kontrol, kardeş-arası reddetme) kaynak hücreyle örtüşür."""
        self.assertIn("ICC = 0,32", self.text,
                      "ch05'te 'ICC = 0,32' kontrol kardeş-uyum literali bulunmadı")
        src = self._cell("reddetme", "Kontrol", "icc")  # 0.321954...
        self.assertTrue(_round_eq(src, 0.32, 2),
                        f"kaynak ICC {src:.4f} ≠ 0,32 (ch05 sürüklenme/kaynak değişimi)")

    def test_control_icc_ci_matches_source(self):
        """ch05 GA [0,15; 0,47] kaynak GA ile örtüşür."""
        self.assertIn("[0,15; 0,47]", self.text)
        lo = self._cell("reddetme", "Kontrol", "ci_lower")  # 0.153165...
        hi = self._cell("reddetme", "Kontrol", "ci_upper")  # 0.472568...
        self.assertTrue(_round_eq(lo, 0.15, 2), f"GA alt {lo:.4f} ≠ 0,15")
        self.assertTrue(_round_eq(hi, 0.47, 2), f"GA üst {hi:.4f} ≠ 0,47")

    def test_dm_icc_matches_source(self):
        """ch05 'ICC = 0,00' (DM, kardeş-arası reddetme) kaynak hücreyle örtüşür."""
        self.assertIn("ICC = 0,00", self.text)
        src = self._cell("reddetme", "DM", "icc")  # 0.000
        self.assertTrue(_round_eq(src, 0.00, 2),
                        f"kaynak ICC {src:.4f} 2 ondalıkta 0,00 değil")

    def test_dm_icc_ci_matches_source(self):
        """ch05 DM GA [−0,18; 0,18] kaynak GA ile örtüşür (simetrik ±0,1786)."""
        self.assertTrue(
            "[−0,18; 0,18]" in self.text or "[-0,18; 0,18]" in self.text,
            "ch05'te DM reddetme GA [−0,18; 0,18] literali bulunamadı")
        lo = self._cell("reddetme", "DM", "ci_lower")  # -0.178597...
        hi = self._cell("reddetme", "DM", "ci_upper")  # 0.178597...
        self.assertTrue(_round_eq(lo, -0.18, 2), f"GA alt {lo:.4f} ≠ −0,18")
        self.assertTrue(_round_eq(hi, 0.18, 2), f"GA üst {hi:.4f} ≠ 0,18")


class TestCh05NoDriftAgainstCsvValues(unittest.TestCase):
    """Regresyon güvencesi: yukarıdaki bağlayıcı literaller ch05'te tekildir
    (yanlışlıkla iki farklı yerde çelişik yazılmamıştır)."""

    def setUp(self):
        self.text = _read_ch05_text()

    def test_control_icc_literal_unique_or_consistent(self):
        """'ICC = 0,32' farklı bir değere sürüklenmiş bir ikizle çakışmaz."""
        # kontrol kardeş-reddetme ICC bağlamında tek kanonik literal 0,32'dir;
        # aynı cümlede 0,3x varyasyonu (0,31/0,33...) belirmemelidir.
        near = re.findall(r"ICC = 0,3\d", self.text)
        for lit in near:
            self.assertEqual(lit, "ICC = 0,32",
                             f"beklenmeyen ICC yeniden-ifade varyantı: {lit}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
