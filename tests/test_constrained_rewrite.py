#!/usr/bin/env python3
"""constrained_rewrite harness birim testleri (deterministik; gateway GEREKMEZ).

Garanti sözleşmesi: maskele → (model) → splice → verify zinciri, maskelenen her
immutable span'ın (sayı/@token/[@cite]/çekince) birebir hayatta kalmasını MEKANİK
olarak sağlar. Bu testler mask/splice/verify/segment sözleşmesini ve rewrite_section
retry mantığını (enjekte edilen sahte 'generate' ile) kilitler.

Çalıştır: python3 tests/test_constrained_rewrite.py   (sessiz çıkış = PASS)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "eval"))
import constrained_rewrite as cr  # noqa: E402


def test_segment_paragraphs():
    txt = "Birinci paragraf.\n\nİkinci paragraf.\n\nÜçüncü."
    paras = cr.segment_paragraphs(txt)
    assert paras == ["Birinci paragraf.", "İkinci paragraf.", "Üçüncü."], paras
    # tek paragraf
    assert cr.segment_paragraphs("Tek.") == ["Tek."]
    # çoklu boş satır tek ayraç sayılır
    assert cr.segment_paragraphs("A.\n\n\n\nB.") == ["A.", "B."]


def test_detect_auto_spans():
    p = "Sonuç @tbl-apa-sample-characteristics ve @fig-smd-love [@austin2009balanceDiagnostics]."
    spans = cr.detect_auto_spans(p)
    assert "@tbl-apa-sample-characteristics" in spans
    assert "@fig-smd-love" in spans
    assert "[@austin2009balanceDiagnostics]" in spans


def test_mask_splice_roundtrip_identity():
    """Model yer-tutucuları AYNEN korursa (mükemmel model) → splice orijinali verir."""
    p = "SMD = 0,53 iken denge @fig-smd-love içinde; medyan 38,5 yıl [@austin2009balanceDiagnostics]."
    masked, mapping = cr.mask(p, ["SMD = 0,53", "medyan 38,5 yıl"])
    # maskeli metinde ham değerler kalmamalı
    assert "0,53" not in masked
    assert "38,5" not in masked
    assert "@fig-smd-love" not in masked
    assert "[@austin2009balanceDiagnostics]" not in masked
    # splice = orijinal
    assert cr.splice(masked, mapping) == p


def test_mask_longest_first_no_corruption():
    """Üst üste binen span'lar (uzun içinde kısa) → uzun maskelenir, kısa bozulmaz."""
    p = "Fark SMD = 0,53 düzeyindedir."
    masked, mapping = cr.mask(p, ["0,53", "SMD = 0,53"])
    # uzun span tek yer-tutucuya inmeli; splice birebir dönmeli
    assert cr.splice(masked, mapping) == p
    # maskeli metinde ne '0,53' ne 'SMD = 0,53' ham kalmalı
    assert "0,53" not in masked


def test_mask_repeated_span_both_masked():
    p = "@tbl-x ilk; sonra yine @tbl-x."
    masked, mapping = cr.mask(p, [])
    # @tbl-x iki kez → aynı yer-tutucu iki kez
    ph = [k for k, v in mapping.items() if v == "@tbl-x"][0]
    assert masked.count(ph) == 2
    assert cr.splice(masked, mapping) == p


def test_verify_pass_when_placeholders_intact():
    p = "Değer SMD = 0,004 latent SES."
    masked, mapping = cr.mask(p, ["SMD = 0,004"])
    v = cr.verify(masked, masked, mapping)  # model çıktısı = maskeli girdi (aynen korudu)
    assert v["ok"], v


def test_verify_detects_missing_placeholder():
    p = "İki değer: SMD = 0,220 ve SMD = 0,004."
    masked, mapping = cr.mask(p, ["SMD = 0,220", "SMD = 0,004"])
    # model bir yer-tutucuyu düşürsün
    ph_drop = [k for k, v in mapping.items() if v == "SMD = 0,004"][0]
    broken = masked.replace(ph_drop, "")
    v = cr.verify(masked, broken, mapping)
    assert not v["ok"]
    assert any(m.get("placeholder") == ph_drop for m in v["missing"]), v


def test_verify_detects_extra_placeholder():
    p = "Tek değer @fig-smd-love."
    masked, mapping = cr.mask(p, [])
    ph = list(mapping)[0]
    broken = masked + " " + ph  # model çift kullandı
    v = cr.verify(masked, broken, mapping)
    assert not v["ok"]
    assert v["extra"], v


def test_mask_rejects_sentinel_in_source():
    try:
        cr.mask("İçinde ⟦ sentinel var.", [])
    except ValueError:
        return
    raise AssertionError("⟦ içeren kaynakta ValueError bekleniyordu")


def test_rewrite_section_retries_then_flags():
    """Sahte generate ilk turda placeholder düşürür, ikinci turda korur → status ok, attempts=2."""
    spec = {"paragraphs": [{"text": "Değer SMD = 0,53 ve @fig-x.", "spans": ["SMD = 0,53"]}],
            "glossary": {}}
    calls = {"n": 0}

    def flaky_generate(masked, glossary, system):
        calls["n"] += 1
        if calls["n"] == 1:
            # ilk tur: bir yer-tutucuyu düşür (ilk ⟦KDU...⟧'yu sil)
            import re
            return re.sub(r"⟦KDU\d+⟧", "", masked, count=1)
        return masked  # ikinci tur: aynen koru

    out = cr.rewrite_section(spec, generate=flaky_generate, retries=2)
    par = out["paragraphs"][0]
    assert par["status"] == "ok", par
    assert par["attempts"] == 2, par
    assert par["rewritten"] == "Değer SMD = 0,53 ve @fig-x."  # splice orijinali geri verdi


def test_rewrite_section_fails_after_retries():
    spec = {"paragraphs": [{"text": "Değer SMD = 0,53.", "spans": ["SMD = 0,53"]}]}

    def always_drop(masked, glossary, system):
        import re
        return re.sub(r"⟦KDU\d+⟧", "", masked)

    out = cr.rewrite_section(spec, generate=always_drop, retries=2)
    par = out["paragraphs"][0]
    assert par["status"] == "failed", par
    assert par["rewritten"] is None
    assert par["attempts"] == 3  # 1 + 2 retry


def test_filter_glossary_keeps_only_present_terms():
    """Guardrail 1: yalnız paragrafta GEÇEN terim döner (glossary-dump'ı kökten keser)."""
    g = {"yanıt yüzeyi analizi": "üç boyutlu yüzey",
         "Olsen-Kenny latent düad": "gizli düzey uyum",
         "konkordans": "uyum"}
    text = "Bu paragrafta yanıt yüzeyi analizi ve konkordans geçmektedir."
    kept = cr.filter_glossary(g, text)
    assert set(kept) == {"yanıt yüzeyi analizi", "konkordans"}, kept
    # büyük/küçük harf duyarsız (casefold; Türkçe İ/ı locale-casing garanti edilmez)
    assert set(cr.filter_glossary(g, "Konkordans klinik önemdedir.")) == {"konkordans"}
    # hiç terim yoksa / boş glossary → boş
    assert cr.filter_glossary(g, "Alakasız bir cümle.") == {}
    assert cr.filter_glossary({}, text) == {}


def test_rewrite_section_filters_glossary_per_paragraph():
    """Guardrail 1 uçtan uca: her paragraf generate'e yalnız kendi terimlerini alır."""
    spec = {"paragraphs": [
        {"text": "yanıt yüzeyi analizi ile @fig-x incelendi.", "spans": []},
        {"text": "Basit bir @fig-y sonucu.", "spans": []}],
        "glossary": {"yanıt yüzeyi analizi": "üç boyutlu yüzey",
                     "Olsen-Kenny latent düad": "gizli düzey"}}
    seen = []

    def capture(masked, glossary, system):
        seen.append(dict(glossary))
        return masked

    cr.rewrite_section(spec, generate=capture, retries=0)
    assert set(seen[0]) == {"yanıt yüzeyi analizi"}, seen[0]  # sadece geçen terim
    assert seen[1] == {}, seen[1]  # ikinci paragrafta terim yok → gloss verilmez


def test_default_system_has_dump_and_note_guards():
    """Guardrail 2 regresyon kilidi: no-dump + note-echo + büyük-harf-dikiş kuralları var."""
    s = cr.default_system({}, note="klinik-kesme çekincesini listeden önce belirt")
    assert "EK BİLGİ YASAK" in s              # paragraf-dışı model/istatistik ekleme yasağı
    assert "İSTATİSTİK-META YASAK" in s       # p/%95 GA meta-filler yasağı (Guardrail 3)
    assert "yönergeyi yalnız uygula" in s     # note metne kopyalanmaz
    assert "BÜYÜK harfle başlayan" in s       # tam-cümle yer-tutucu önüne özne eklenmez
    assert "MARMARA RESMİ REGISTER" in s      # sade AMA resmi: retorik soru/eksiltili yok
    assert "MANŞET/GRID" in s                 # grid tabloya, manşet metinde
    assert "YÖNTEM MEKANİĞİ" in s             # mekanik/formül → teknik ek


def test_verify_authored_spans():
    """Claude-authored mod: eksik span FAIL, hepsi varsa PASS."""
    authored = ("Uyum düşüktür (ICC 0,03–0,20). Ayrıntı @tbl-x'da; şart karşılanmamıştır.")
    req = ["0,03–0,20", "@tbl-x", "şart karşılanmamıştır"]
    assert cr.verify_authored_spans(authored, req)["ok"], "hepsi varken PASS bekleniyordu"
    # bir sayı düşerse FAIL
    v = cr.verify_authored_spans("Uyum düşüktür. Ayrıntı @tbl-x'da.", req)
    assert not v["ok"] and "0,03–0,20" in v["missing"], v
    # mutasyon (0,03→0,3) yakalanır
    v2 = cr.verify_authored_spans("ICC 0,3–0,20 @tbl-x şart karşılanmamıştır", req)
    assert not v2["ok"] and "0,03–0,20" in v2["missing"], v2


def test_paragraph_count_preserved():
    spec = {"paragraphs": [{"text": "P1 @fig-a.", "spans": []},
                           {"text": "P2 @fig-b.", "spans": []}]}
    out = cr.rewrite_section(spec, generate=lambda m, g, s: m, retries=1)
    assert len(out["paragraphs"]) == 2
    assert all(p["status"] == "ok" for p in out["paragraphs"])


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
    print("PASS: %d test" % len(fns))


if __name__ == "__main__":
    _run()
