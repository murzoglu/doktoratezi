"""QC kapsam genişletme kontrat testleri — doktoratezi.

`tez_checklist_verify.py`'a eklenen yeni maddeler (K5-NUM-03, K5-CAU-02,
K5-TRK-01, R-SVG-01, K0-PII-03), `--closing` modu ve yeni salt-okuma
denetçileri (targets_file_tracking_audit, pii_value_scan) için davranış
testleri. Plan: docs/superpowers/plans/2026-07-22-qc-otomatik-zorlama.md

Run: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_qc_coverage.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VERIFY = REPO / "scripts" / "util" / "tez_checklist_verify.py"
UTIL = REPO / "scripts" / "util"


def run_verify(args):
    return subprocess.run(
        [sys.executable, str(VERIFY), *args],
        capture_output=True, text=True, cwd=str(REPO),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=120,
    )


class ClosingModeTests(unittest.TestCase):
    def test_closing_refuses_fast(self):
        p = run_verify(["--closing", "--fast"])
        self.assertEqual(2, p.returncode, p.stdout + p.stderr)
        self.assertIn("closing", (p.stdout + p.stderr).lower())


class RegistryTests(unittest.TestCase):
    NEW_IDS = ["K5-NUM-03", "K5-CAU-02", "K5-TRK-01", "R-SVG-01", "K0-PII-03"]

    def test_new_ids_registered(self):
        out = run_verify(["--list"]).stdout
        for cid in self.NEW_IDS:
            self.assertIn(cid, out, cid)

    def test_audit_doc_zero_orphan(self):
        p = run_verify(["--audit-doc"])
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)


class NewToolExistenceTests(unittest.TestCase):
    def test_targets_file_tracking_tool_exists(self):
        self.assertTrue((UTIL / "targets_file_tracking_audit.py").exists())

    def test_pii_value_scan_tool_exists(self):
        self.assertTrue((UTIL / "pii_value_scan.py").exists())


class PiiValueScanTests(unittest.TestCase):
    def _scan(self, text):
        with tempfile.NamedTemporaryFile("w", suffix=".qmd", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(text)
            path = fh.name
        self.addCleanup(os.unlink, path)
        return subprocess.run(
            [sys.executable, str(UTIL / "pii_value_scan.py"), "--paths", path],
            capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=60,
        )

    def test_flags_tckn(self):
        p = self._scan("Katılımcı TC 12345678901 kaydı.")
        self.assertEqual(1, p.returncode, p.stdout + p.stderr)

    def test_flags_birthdate(self):
        p = self._scan("Doğum tarihi 03.05.2011 olan çocuk.")
        self.assertEqual(1, p.returncode, p.stdout + p.stderr)

    def test_ignores_plain_year_and_n(self):
        p = self._scan("2024 yılında 241 aile ve 482 satır analiz edildi.")
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)

    def test_ignores_bare_study_date(self):
        # Etik onayı/veri toplama gibi çalışma tarihleri PII DEĞİLDİR — yalnız
        # doğum-bağlamlı tam tarih işaretlenir (yanlış-pozitif koruması).
        p = self._scan("Etik kurul onayı 11.05.2023 tarihinde alınmıştır.")
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)

    def test_ignores_high_precision_decimal(self):
        # Yüksek-hassasiyet ondalık (R model çıktısı) T.C. no DEĞİLDİR:
        # 3951.12345678901 gibi bir kesir 11-hane olarak işaretlenmemeli.
        p = self._scan("Katsayı 3951.12345678901 ve 0.12345678901 bulundu.")
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)


class PiiExemptionScopeTests(unittest.TestCase):
    """Kılavuz-zorunlu alan muafiyeti DAR mı? (K0-PII-03 istisna sözleşmesi)

    Marmara SBE şablonu §9 ÖZGEÇMİŞ, Doğum Tarihi ve Tel alanlarını zorunlu
    kılar; muafiyet yalnız o dosyada + o sınıfta + etiketli satırda geçerlidir.
    Bu testler muafiyetin genel bir PII kapısı gevşetmesine dönüşmesini önler.
    """

    @staticmethod
    def _mod():
        sys.path.insert(0, str(UTIL))
        try:
            import pii_value_scan  # type: ignore
        finally:
            sys.path.pop(0)
        return pii_value_scan

    CV = "chapters/06_ozgecmis_faaliyetler.qmd"

    def _exempt(self, key, line, dosya=None):
        m = self._mod()
        return m._exemption_for(dosya or self.CV, key, line) is not None

    def test_cv_labeled_phone_is_exempt(self):
        self.assertTrue(self._exempt(
            "telefon", "| **Uyruğu** | T.C. | **Tel** | 0555 111 22 20 |"))

    def test_cv_labeled_birthdate_is_exempt(self):
        self.assertTrue(self._exempt(
            "dogum-tarihi", "| **Doğum Tarihi** | 21.12.1982 |"))

    def test_unlabeled_phone_same_file_still_flagged(self):
        # Aynı dosyada CV etiketi olmayan bir telefon muaf DEĞİLDİR.
        self.assertFalse(self._exempt(
            "telefon", "Katılımcı ile iletişim: 0532 999 88 77"))

    def test_tckn_never_exemptible(self):
        # Kimlik numarası, CV etiketi taşısa bile muaf edilemez.
        self.assertFalse(self._exempt("tckn", "| **Tel** | 12345678901 |"))

    def test_patient_no_never_exemptible(self):
        self.assertFalse(self._exempt("hasta-no", "| **Tel** | Hasta No: 4471 |"))

    def test_non_exemptible_set_contract(self):
        self.assertEqual({"tckn", "hasta-no"}, set(self._mod().NON_EXEMPTIBLE))

    def test_other_file_not_exempt(self):
        # CV etiketi başka bir bölümde muafiyet üretmez.
        self.assertFalse(self._exempt(
            "telefon", "| **Tel** | 0555 111 22 20 |",
            dosya="chapters/04_bulgular.qmd"))

    def test_strict_mode_reports_exemptions_as_findings(self):
        p = subprocess.run(
            [sys.executable, str(UTIL / "pii_value_scan.py"), "--strict"],
            capture_output=True, text=True, cwd=str(REPO),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=60)
        self.assertEqual(1, p.returncode, p.stdout + p.stderr)

    def test_default_mode_clean_but_logs_exemption(self):
        p = subprocess.run(
            [sys.executable, str(UTIL / "pii_value_scan.py")],
            capture_output=True, text=True, cwd=str(REPO),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=60)
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)
        # Muafiyet sessizce yutulmaz: denetim izi çıktıda görünür.
        self.assertIn("MUAF", p.stdout)


class CrossArmRhetoricTests(unittest.TestCase):
    TOOL = UTIL / "cross_arm_rhetoric_audit.py"

    def _scan(self, text):
        with tempfile.NamedTemporaryFile("w", suffix=".qmd", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(text)
            path = fh.name
        self.addCleanup(os.unlink, path)
        return subprocess.run(
            [sys.executable, str(self.TOOL), "--paths", path],
            capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=60)

    def test_tool_exists(self):
        self.assertTrue(self.TOOL.exists())

    def test_flags_cross_arm_confirmation(self):
        p = self._scan("Nitel bulgular nicel regresyon sonuçlarını doğrulamaktadır.")
        self.assertEqual(1, p.returncode, p.stdout + p.stderr)

    def test_ignores_single_arm_verification(self):
        p = self._scan("Nicel analizde regresyon katsayısı doğrulandı.")
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)

    def test_ignores_convergence_language(self):
        p = self._scan("Nitel temalar nicel bulgularla yakınsamaktadır.")
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)

    def test_ignores_negated_positioning(self):
        # 'doğrulayan ... olarak DEĞİL' = doğru disiplin beyanı → işaretlenmez.
        p = self._scan("Nitel bulgular nicel sonuçları doğrulayan ikincil kanıt "
                       "olarak değil, tamamlayıcı bir kanıt türüdür.")
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)

    def test_ignores_negative_verb_form(self):
        # 'doğrulamaz' = olumsuz fiil → cross-arm iddiası DEĞİL.
        p = self._scan("Nitel bulgular nicel sonuçları doğrulamaz.")
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)

    def test_ignores_noun_kanit_homograph(self):
        # 'kanıtların/kanıtlar' = İSİM (kanıt+lar), fiil 'kanıtla-' DEĞİL.
        p = self._scan("Nicel ve nitel kanıtların aynı yönde olması beklenir.")
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)

    def test_ignores_verification_noun(self):
        # 'doğrulama aracı' = İSİM (verification), fiil DEĞİL.
        p = self._scan("Nicel ve nitel için bir doğrulama aracı kullanılır.")
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)


class NewCheckRegistryTests(unittest.TestCase):
    def test_p2p3_ids_registered(self):
        out = run_verify(["--list"]).stdout
        for cid in ["K4-TRG-01", "K1-KAR-01", "T-CERT-01",
                    "K1-DOI-01", "K5-GAL-01"]:
            self.assertIn(cid, out, cid)

    def test_doi_skips_off_closing(self):
        # K1-DOI-01 ağ-bağımlı → --closing dışında SKIP (asla FAIL).
        p = run_verify(["--section", "K1-DOI-01"])
        self.assertEqual(0, p.returncode, p.stdout)  # FAIL yok → exit 0
        self.assertIn("[SKIP", p.stdout)


class RGeneratorChapterScanTests(unittest.TestCase):
    TOOL = UTIL / "r_generator_literal_audit.py"

    def _scan_qmd(self, text):
        with tempfile.NamedTemporaryFile("w", suffix=".qmd", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(text)
            path = fh.name
        self.addCleanup(os.unlink, path)
        return subprocess.run(
            [sys.executable, str(self.TOOL), "--paths", path, "--fail-on-find"],
            capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=60)

    def test_include_chapters_flag_exists(self):
        p = subprocess.run([sys.executable, str(self.TOOL), "--help"],
                           capture_output=True, text=True, timeout=30)
        self.assertIn("--include-chapters", p.stdout)

    def test_flags_hardcoded_stat_in_inline_chunk(self):
        text = '```{r}\ntbl <- data.frame(\n  sonuc = "BF10=8.12"\n)\n```\n'
        p = self._scan_qmd(text)
        self.assertEqual(1, p.returncode, p.stdout)

    def test_ignores_prose_stat_outside_chunk(self):
        # R chunk DIŞI düzyazıdaki sayı taranmaz (yalnız {r} chunk içi).
        text = "Metinde BF10=8.12 geçiyor ama bu düzyazı, kod değil.\n"
        p = self._scan_qmd(text)
        self.assertEqual(0, p.returncode, p.stdout)


class GitHooksInstallerTests(unittest.TestCase):
    INSTALLER = UTIL / "install_git_hooks.sh"

    def _temp_git(self):
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        return d

    def test_installer_exists(self):
        self.assertTrue(self.INSTALLER.exists())

    def test_installs_executable_precommit(self):
        d = self._temp_git()
        r = subprocess.run(["bash", str(self.INSTALLER)], cwd=d,
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        hook = Path(d) / ".git" / "hooks" / "pre-commit"
        self.assertTrue(hook.exists())
        self.assertTrue(os.access(hook, os.X_OK))
        self.assertIn("tez_checklist_verify", hook.read_text(encoding="utf-8"))

    def test_uninstall_removes(self):
        d = self._temp_git()
        subprocess.run(["bash", str(self.INSTALLER)], cwd=d, check=True,
                       capture_output=True, timeout=60)
        subprocess.run(["bash", str(self.INSTALLER), "--uninstall"], cwd=d,
                       check=True, capture_output=True, timeout=60)
        self.assertFalse((Path(d) / ".git" / "hooks" / "pre-commit").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
