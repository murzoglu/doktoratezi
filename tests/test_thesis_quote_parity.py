"""
tests/test_thesis_quote_parity.py
Tez-düzeyi verbatim parity denetleyicisi için TDD testleri.

KVKK: Tüm fixture'lar sentetiktir; gerçek katılımcı verisi yok.
"""

import subprocess
import sys
import pathlib

SCRIPT = pathlib.Path(__file__).parents[1] / "scripts/util/thesis_quote_parity.py"


# ---------------------------------------------------------------------------
# Yardımcı fonksiyonlar
# ---------------------------------------------------------------------------

def run(qmd: str, csv_path: str):
    """Denetleyiciyi alt-süreç olarak çalıştırır."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--chapter", qmd, "--manifest", csv_path],
        capture_output=True,
        text=True,
    )


def write_manifest(tmp_path, rows=None):
    """Sentetik manifest CSV yazar."""
    m = tmp_path / "m.csv"
    header = "quote_id,aile_no,rol,tema,triadik_eksen,kaynak_dosya\n"
    if rows is None:
        m.write_text(header, encoding="utf-8")
    else:
        lines = header
        for r in rows:
            lines += (
                f"{r['quote_id']},{r['aile_no']},{r['rol']},"
                f"{r.get('tema', '')},{r.get('eksen', '')},{r.get('kaynak', '')}\n"
            )
        m.write_text(lines, encoding="utf-8")
    return str(m)


def write_qmd(tmp_path, text: str, name: str = "c.qmd"):
    """Sentetik QMD dosyası yazar."""
    q = tmp_path / name
    q.write_text(text, encoding="utf-8")
    return str(q)


# ---------------------------------------------------------------------------
# (b) Tarih deseni → returncode 1
# ---------------------------------------------------------------------------

class TestDateInLabel:
    """KVKK kapısı: etikette tarih deseni bulunursa FAIL."""

    def test_date_gg_aa_yyyy_noktalı(self, tmp_path):
        """GG.AA.YYYY formatı (brief örneği)."""
        q = write_qmd(tmp_path, "«...» (Aile 11, anne, 12.05.2011)\n")
        m = write_manifest(tmp_path)
        assert run(q, m).returncode == 1

    def test_date_slash_formatı(self, tmp_path):
        """GG/AA/YYYY formatı."""
        q = write_qmd(tmp_path, "«Bir şey söyleyeyim.» (Aile 14, sağlıklı kardeş, 22/03/2015)\n")
        m = write_manifest(tmp_path)
        assert run(q, m).returncode == 1

    def test_date_guillemet_alıntı(self, tmp_path):
        """Guillemet alıntı + tarih etiketi."""
        q = write_qmd(tmp_path, "«Kardeşim hasta.» (Aile 19, anne, 01.01.2010)\n")
        m = write_manifest(tmp_path)
        assert run(q, m).returncode == 1

    def test_date_kıvrık_tırnak_alıntı(self, tmp_path):
        """Kıvrık tırnak alıntı + tarih etiketi."""
        q = write_qmd(tmp_path, "“Bir şey söyleyeyim.” (Aile 26, anne, 15.07.2012)\n")
        m = write_manifest(tmp_path)
        assert run(q, m).returncode == 1

    def test_date_iki_haneli_yıl(self, tmp_path):
        """GG.AA.YY kısa yıl formatı da yakalanmalı."""
        q = write_qmd(tmp_path, "«Test.» (Aile 11, anne, 12.05.11)\n")
        m = write_manifest(tmp_path)
        assert run(q, m).returncode == 1


# ---------------------------------------------------------------------------
# (c) Tanınmayan rol → returncode 1
# ---------------------------------------------------------------------------

class TestUnknownRol:
    """Tanınmayan rol yüzeyi → FAIL."""

    def test_rol_baba(self, tmp_path):
        """'baba' tanımlı rol değil."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Test alıntı.» (Aile 11, baba, 9 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 1

    def test_rol_ogretmen(self, tmp_path):
        """'öğretmen' tanımlı rol değil."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 11, öğretmen, 10 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 1

    def test_rol_completely_unknown(self, tmp_path):
        """Tamamen bilinmeyen rol."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 11, xyz_rol, 8 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 1


# ---------------------------------------------------------------------------
# (a) Manifest eksik → returncode 1
# ---------------------------------------------------------------------------

class TestMissingFromManifest:
    """Manifest'te bulunmayan (aile_no, rol) → FAIL."""

    def test_aile_numarası_yok(self, tmp_path):
        """Manifest'te olmayan aile numarası."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Bir şey söyleyeyim.» (Aile 99, anne, 10 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 1

    def test_rol_bu_ailede_yok(self, tmp_path):
        """Aile var ama o rol (t1dm_child) manifest'te yok."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Bir şey söyleyeyim.» (Aile 11, hasta, 8 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 1

    def test_boş_manifest_alıntılı_bölüm(self, tmp_path):
        """Manifest boş ama bölümde alıntı var → FAIL."""
        q = write_qmd(tmp_path, "«Test alıntı.» (Aile 11, anne, 9 yaş)\n")
        m = write_manifest(tmp_path)  # yalnız başlık
        assert run(q, m).returncode == 1

    def test_sağlıklı_kardeş_rolü_yok_manifeste(self, tmp_path):
        """Aile 11 için healthy_sibling manifestte yok."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Kardeşim bazen üzülüyor.» (Aile 11, sağlıklı kardeş, 12 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 1


# ---------------------------------------------------------------------------
# Geçerli etiket + manifest eşleşmesi → returncode 0
# ---------------------------------------------------------------------------

class TestValidClean:
    """Temiz bölümler → returncode 0."""

    def test_anne_geçerli(self, tmp_path):
        """'anne' → mother; manifestte (011, mother) var → PASS."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Şeker hastalığı çok zor.» (Aile 11, anne, 35 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_sağlıklı_kardeş_geçerli(self, tmp_path):
        """'sağlıklı kardeş' → healthy_sibling → PASS."""
        rows = [{"quote_id": "011_healthy_sibling_q1", "aile_no": "011", "rol": "healthy_sibling"}]
        q = write_qmd(tmp_path, "«Kardeşim bazen üzülüyor.» (Aile 11, sağlıklı kardeş, 12 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_hasta_geçerli(self, tmp_path):
        """'hasta' → t1dm_child → PASS."""
        rows = [{"quote_id": "011_t1dm_child_q1", "aile_no": "011", "rol": "t1dm_child"}]
        q = write_qmd(tmp_path, "«İğne yapmak bazen acıtıyor.» (Aile 11, hasta, 9 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_yaş_ay_formatı(self, tmp_path):
        """'12 yaş 5 ay' formatı → PASS."""
        rows = [{"quote_id": "014_mother_q1", "aile_no": "014", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Çok şey değişti.» (Aile 14, anne, 12 yaş 5 ay)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_guillemet_alıntı_geçerli(self, tmp_path):
        """Guillemet alıntı + geçerli etiket → PASS."""
        rows = [{"quote_id": "019_mother_q1", "aile_no": "019", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Çocuğum çok güçlü.» (Aile 19, anne, 40 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_kıvrık_tırnak_alıntı_geçerli(self, tmp_path):
        """Kıvrık tırnak (U+201C/201D) + geçerli etiket → PASS."""
        rows = [{"quote_id": "019_mother_q1", "aile_no": "019", "rol": "mother"}]
        q = write_qmd(tmp_path, "“Çocuğum çok güçlü.” (Aile 19, anne, 40 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_alıntısız_bölüm_temiz(self, tmp_path):
        """Alıntı olmayan bölüm → PASS (etiket yok, denetim geçiyor)."""
        q = write_qmd(tmp_path, "Bu bölümde henüz alıntı yok.\n")
        m = write_manifest(tmp_path)  # boş manifest
        assert run(q, m).returncode == 0

    def test_çoklu_geçerli_alıntı(self, tmp_path):
        """Birden fazla geçerli alıntı → PASS."""
        rows = [
            {"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"},
            {"quote_id": "014_t1dm_child_q1", "aile_no": "014", "rol": "t1dm_child"},
        ]
        text = (
            "«İlk alıntı.» (Aile 11, anne, 35 yaş)\n"
            "Sonraki alıntı:\n"
            "«İkinci alıntı.» (Aile 14, hasta, 10 yaş)\n"
        )
        q = write_qmd(tmp_path, text)
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_önce_sıfırlı_aile_no(self, tmp_path):
        """Manifest'teki '011', etiketteki 'Aile 11' ile eşleşmeli (sıfır normalizasyonu)."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 11, anne, 35 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_büyük_aile_numarası(self, tmp_path):
        """201 gibi büyük aile numarası (ön-sıfırsız) → PASS."""
        rows = [{"quote_id": "201_t1dm_child_q1", "aile_no": "201", "rol": "t1dm_child"}]
        q = write_qmd(tmp_path, "«Kardeşim bana yardım eder.» (Aile 201, hasta, 13 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0


# ---------------------------------------------------------------------------
# Türkçe rol yüzey formları (kanonikleştirme testi)
# ---------------------------------------------------------------------------

class TestTurkishRolVariants:
    """Türkçe yüzey formlarının doğru kanonikleştirilmesi."""

    def test_t1dm_li_çocuk_unicode_apostrof(self, tmp_path):
        """T1DM’li çocuk (sağ tek tırnak U+2019) → t1dm_child → PASS."""
        rows = [{"quote_id": "020_t1dm_child_q1", "aile_no": "020", "rol": "t1dm_child"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 20, T1DM’li çocuk, 11 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_t1dm_li_çocuk_ascii_apostrof(self, tmp_path):
        """T1DM'li çocuk (ASCII apostrof) → t1dm_child → PASS."""
        rows = [{"quote_id": "020_t1dm_child_q1", "aile_no": "020", "rol": "t1dm_child"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 20, T1DM'li çocuk, 11 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_kardeş_kısa_form(self, tmp_path):
        """Sadece 'kardeş' → healthy_sibling → PASS."""
        rows = [{"quote_id": "020_healthy_sibling_q1", "aile_no": "020", "rol": "healthy_sibling"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 20, kardeş, 8 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_hasta_çocuk_formu(self, tmp_path):
        """'hasta çocuk' → t1dm_child → PASS."""
        rows = [{"quote_id": "026_t1dm_child_q1", "aile_no": "026", "rol": "t1dm_child"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 26, hasta çocuk, 9 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0


# ---------------------------------------------------------------------------
# Büyük-harfli rol yüzeyleri → NAME_RE false-positive tetiklememeli
# (Fix 1: NAME_RE yalnız yaş alanına uygulanır)
# ---------------------------------------------------------------------------

class TestCapitalizedRolFalsePositive:
    """
    Büyük-harfli rol yüzeyleri (Sağlıklı Kardeş, Hasta Çocuk, Anne)
    NAME_RE false-positive tetiklememeli; geçerli manifest eşleşmesinde PASS.
    """

    def test_sağlıklı_kardeş_büyük_harf(self, tmp_path):
        """'Sağlıklı Kardeş' (her iki sözcük büyük harf) KVKK-AD false-positive üretmemeli."""
        rows = [{"quote_id": "011_healthy_sibling_q1", "aile_no": "011", "rol": "healthy_sibling"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 11, Sağlıklı Kardeş, 12 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_hasta_çocuk_büyük_harf(self, tmp_path):
        """'Hasta Çocuk' (her iki sözcük büyük harf) KVKK-AD false-positive üretmemeli."""
        rows = [{"quote_id": "011_t1dm_child_q1", "aile_no": "011", "rol": "t1dm_child"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 11, Hasta Çocuk, 9 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_anne_büyük_harf(self, tmp_path):
        """'Anne' (tek büyük sözcük) zaten sorunsuzdur — hâlâ PASS olduğunu doğrula."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 11, Anne, 35 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_yaş_alanında_gerçek_ad_hâlâ_fail(self, tmp_path):
        """Yaş alanında gerçek ad deseni (Ayşe Kaya) → KVKK-AD FAIL hâlâ çalışmalı."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        # yaş alanı yerine "Ayşe Kaya" yazılmış → gerçek kişi adı
        q = write_qmd(tmp_path, "«Test.» (Aile 11, anne, Ayşe Kaya)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 1


class TestSatirSarmaRol:
    """Etiket nesir icinde satir sonuna sararsa rol yine taninmali (ic bosluk normalizasyonu)."""

    def test_saglikli_kardes_satir_sarmasi(self, tmp_path):
        """'(Aile 14, sağlıklı\\nkardeş, 10 yaş)' satir sarmasi -> healthy_sibling; manifestte varsa PASS."""
        rows = [{"quote_id": "014_healthy_sibling_q007", "aile_no": "014", "rol": "healthy_sibling"}]
        q = write_qmd(tmp_path, "«Bir şey söyleyeyim.» (Aile 14, sağlıklı\nkardeş, 10 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 0

    def test_tanimsiz_rol_satir_sarmasi_hala_fail(self, tmp_path):
        """Satir sarsa bile tanimsiz rol (baba) FAIL kalmali."""
        rows = [{"quote_id": "011_mother_q1", "aile_no": "011", "rol": "mother"}]
        q = write_qmd(tmp_path, "«Test.» (Aile 11, sağlıklı\nbaba, 40 yaş)\n")
        m = write_manifest(tmp_path, rows)
        assert run(q, m).returncode == 1
