#!/usr/bin/env python3
"""constrained_rewrite — kısıtlı-yeniden-yazım harness'i (klinisyen-diline-uyarlama).

Verbatim-koruma işini modelin elinden alıp deterministik koda taşır: immutable
span'lar (sayı / @tbl·@fig / [@cite] / çekince) göndermeden önce opak yer-tutucularla
(⟦KDUk⟧) maskelenir; model yalnız aralarındaki bağlaç nesrini yeniden yazar; sonra
orijinal span'lar birebir geri-yapıştırılır (splice) ve her yer-tutucunun tam bir kez
korunduğu deterministik olarak DOĞRULANIR (verify). Böylece sayı/token/atıf/çekince
düşmesi ya da mutasyonu MEKANİK olarak imkânsız olur — modelden bağımsız.

Bu modül SIR İÇERMEZ (saf mask/splice/verify mantığı); gateway çağrısını gitignored
`gemini_reformulate.py` köprüsüne subprocess ile devreder. Bu yüzden izlenebilir (tracked).

Sözleşme sınırı: maskeleme yalnız MASKELENENİ korur; maskeleme listesinin TAM olması
çağıranın (Claude Adım 0 envanteri) sorumluluğudur. Modelin YAZDIĞI bağlaç nesrindeki
abartı (F1) / eklenen iddia (F2) / üslup maskeyle çözülmez → Claude Adım 2 + galileo denetler.

CLI: stdin JSON {paragraphs:[{text, spans[], caveats[]}], glossary{}} →
     stdout JSON {paragraphs:[{original, masked, rewritten, status, attempts, verify}]}
"""
import json
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BRIDGE = os.path.join(_HERE, "gemini_reformulate.py")
_PH_RE = re.compile(r"⟦KDU\d+⟧")
_TOKEN_RE = re.compile(r"@(?:tbl|fig)-[A-Za-z0-9_-]+")
_CITE_RE = re.compile(r"\[@[^\]]+\]")


def segment_paragraphs(text):
    """Boş satır(lar)la böl; her paragrafı strip'le; boşları at. Paragraf sayısını
    korumak, yeniden birleştirmede yapı bütünlüğünü (4→4) garanti eder."""
    parts = re.split(r"\n\s*\n", text)
    return [p.strip() for p in parts if p.strip()]


def detect_auto_spans(paragraph):
    """Kesin regex'le tespit edilen immutable span'lar: @tbl/@fig token + [@cite].
    (Sayı ve çekince otomatik tespit edilmez — kırılgan; çağıran açıkça verir.)"""
    return _TOKEN_RE.findall(paragraph) + _CITE_RE.findall(paragraph)


def mask(paragraph, spans):
    """paragraph içindeki immutable span'ları ⟦KDUk⟧ yer-tutucularıyla değiştir.
    spans = çağıran-verdiği (sayı/çekince) + otomatik (token/cite). En-uzun-önce
    değişim, üst üste binen span'larda (uzun içinde kısa) bozulmayı önler.
    Döner: (masked_text, mapping{placeholder: original}). Kaynakta sentinel varsa hata."""
    if "⟦" in paragraph or "⟧" in paragraph:
        raise ValueError("kaynak metin ⟦/⟧ sentinel karakteri içeriyor; maskeleme güvensiz")
    all_spans = [s for s in (list(spans) + detect_auto_spans(paragraph)) if s]
    # benzersizle, en uzun önce (nesting güvenliği)
    uniq = sorted(dict.fromkeys(all_spans), key=len, reverse=True)
    mapping = {}
    masked = paragraph
    for i, s in enumerate(uniq):
        if s not in masked:      # daha uzun bir span tarafından tüketilmiş olabilir
            continue
        ph = "⟦KDU%d⟧" % i
        mapping[ph] = s
        masked = masked.replace(s, ph)
    return masked, mapping


def splice(text, mapping):
    """Yer-tutucuları orijinal span'larla doldur (birebir). Sentinel sınırlayıcıları
    (⟦…⟧) önek çakışmasını önler (⟦KDU1⟧ ≠ ⟦KDU10⟧'un öneki)."""
    for ph, orig in mapping.items():
        text = text.replace(ph, orig)
    return text


def verify(masked_text, model_output, mapping):
    """Her yer-tutucu model çıktısında MASKELİ GİRDİYLE aynı sayıda mı? Eksik/çift/
    tanınmayan yer-tutucu = FAIL. Bu geçerse splice sonrası orijinallerin varlığı
    garanti (yer-tutucu sayıları eşit)."""
    missing, extra = [], []
    for ph, orig in mapping.items():
        cin, cout = masked_text.count(ph), model_output.count(ph)
        if cout < cin:
            missing.append({"placeholder": ph, "original": orig, "expected": cin, "got": cout})
        elif cout > cin:
            extra.append({"placeholder": ph, "original": orig, "expected": cin, "got": cout})
    stray = sorted(set(_PH_RE.findall(model_output)) - set(mapping))
    ok = not missing and not extra and not stray
    return {"ok": ok, "missing": missing, "extra": extra, "stray": stray}


def filter_glossary(glossary, text):
    """Yalnız `text` içinde (büyük/küçük harf duyarsız) GEÇEN glossary terimlerini döndür.
    Böylece her paragrafa yalnız KENDİ terimlerinin klinik karşılığı gider; model,
    kullanmadığı tanımları paragraf sonuna boşaltamaz (glossary-dump kirlenmesi engellenir).
    Orijinal (maskelenmemiş) metne göre süzülür → maskeli kalın etiket içindeki terim de sayılır."""
    if not glossary:
        return {}
    low = text.casefold()
    return {k: v for k, v in glossary.items() if k.casefold() in low}


def verify_authored_spans(authored, required):
    """Claude-authored mod (üretici modeli değil, Claude yazdığında): `authored` metinde
    her DOKUNULMAZ span'ın (required = sayı/@token/[@cite]/çekince-verdikt VERBATIM listesi)
    en az bir kez bulunduğunu MEKANİK doğrular. Eksik/mutasyona uğramış span = FAIL.
    NOT: eklenen abartı/halüsinasyonu YAKALAMAZ (Adım-2 + galileo işi); yalnız düşme/mutasyon.
    Böylece Claude nesri sadeleştirirken sayı/çekince düşürmediği kanıtlanır."""
    missing = [s for s in required if s and s not in authored]
    return {"ok": not missing, "missing": missing, "checked": len([s for s in required if s])}


def default_system(glossary, note=None):
    """Maskeli-üretim sistem talimatı (KLİNİK HEKİM register'ı). Model yalnız bağlaç
    nesrini yeniden yazar; sonuç sayıları korunur, matematiksel formüller teknik eke havale."""
    gloss = ""
    if glossary:
        gloss = ("\n\nKLİNİK KARŞILIKLAR (yalnız BU paragrafta GEÇEN ve hekimin YABANCI olduğu "
                 "psikometrik model için; tanımı cümleye YEDİR, iç içe parantez yapma; listede "
                 "olmayan ya da paragrafta geçmeyen terim için tanım cümlesi EKLEME): " +
                 "; ".join("%s = %s" % (k, v) for k, v in glossary.items()))
    base = (
        "Sen bir doktora tezi editörüsün. Verilen Türkçe Bulgular paragrafını, KLİNİK HEKİM "
        "jürisine uygun biçimde yeniden yaz. Hekim profili: kanıta dayalı tıp altyapısı VAR "
        "(p-değeri, %95 GA, korelasyon rahat okunur); zamanı kısıtlı; psikometrik/matematiksel "
        "model arka planıyla ilgilenmez; sorusu 'bu bulgu aile dinamiği / klinik değerlendirme "
        "açısından ne söylüyor?'.\n"
        "MUTLAK (yer-tutucu): Metinde ⟦KDUk⟧ yer-tutucuları var. HER BİRİNİ, AYNI SAYIDA, AYNEN "
        "koru — değiştirme/çevirme/silme/ekleme yok. Yalnız aralarındaki bağlaç nesrini yaz.\n"
        "SAYILARI TUT: sonuç sayıları (p-değeri, %95 GA, r, katsayı, yüzde, ICC) metinde KALIR — "
        "hekim kanıtı kendi tartar; bunları tabloya kaçırma, yuvarlama, atma.\n"
        "İSTATİSTİK-META YASAK: p-değeri, %95 GA, korelasyon gibi hekimin BİLDİĞİ ölçütleri "
        "TANIMLAMA/AÇIKLAMA; 'sonuçlar/bulgular p ve %95 GA ile raporlanır/yorumlanır/"
        "değerlendirilir', 'p değeri anlamlılıktır', '%95 GA güven aralığıdır' türü GENEL "
        "meta-cümle EKLEME — bu değerler yalnız geldikleri yer-tutucularda kalır; paragrafta "
        "zaten yoksa hiç anma.\n"
        "YÖNTEM MEKANİĞİ → TEKNİK EK: matematiksel FORMÜL + katsayı türetimi + tahmin ayrıntısı "
        "(ör. merkezleme, ICC(A,1)/ICC(2,1) varyantı, yüzey eğriliği tanımı, varyans yapısı) metne "
        "YAZMA; '(formülizasyon/katsayı tanımları teknik ekte)' diye havale et. Metinde yöntemin "
        "tek-cümlelik klinik ADI + NE bulduğu kalır; ürettiği SONUÇ değerleri (p, katsayı, r, "
        "aralık) metinde kalır.\n"
        "KLİNİK ÖNCE (so-what): her stratejiyi/paragrafı, teknik yapıdan ÖNCE bulgunun KLİNİK "
        "anlamıyla (aile dinamiği / klinik değerlendirme karşılığı) tek sade DÜZ BİLDİRİM "
        "cümlesiyle başlat; önce 'klinik olarak ne', sonra 'nasıl'. 'poliklinikte' / 'poliklinik' "
        "gibi klinik-ortam ifadesi KULLANMA — 'klinik olarak', 'klinik açıdan', 'aile "
        "değerlendirmesinde' de.\n"
        "MARMARA RESMİ REGISTER (sade AMA akademik): pasif/nominal 3. tekil; RETORİK SORU YOK; "
        "eksiltili/cümle-parçası ('Çok az.', 'Peki?') YOK; konuşma dili/2. tekil YOK; her cümle "
        "tam ve düz bildirim. Sadelik = kısa DÜZ cümle + yalın sözcük, gayriresmîlik DEĞİL.\n"
        "KISA CÜMLE: tek-yargılı kısa düz cümleler; noktalı-virgülle uzun zincir kurma.\n"
        "MANŞET/GRID: sonucun MANŞETİNİ (kilit aralık/etki + p + yön) metinde bırak; çok-hücreli "
        "sayı GRİDİNİ (alt ölçek × grup katsayı dökümü) metne EKLEME/yeniden üretme — ayrıntı için "
        "verilen tablo işaretini (@tbl-…) koru. (Grid'i zaten çağıran metinden çıkardı; sen yeniden "
        "kurma.)\n"
        "GLOSS YEDİR: yalnız hekimin yabancı olduğu psikometrik modeli, tanımı cümleye "
        "yedirerek bir kez açıkla; iç içe parantez kurma; hekimin bildiğini (Bland-Altman, p, "
        "GA) glosslama.\n"
        "DİKİŞ: yer-tutucular tam dilbilgisel birimdir; çevresine bağlaç eklerken çift noktalama "
        "('.;', '. olarak'), sarkan yüklem veya kip uyumsuzluğu oluşturma; nokta ile biten "
        "yer-tutucudan sonra yeni yüklem ekleme, yeni cümleyle devam et; BÜYÜK harfle başlayan "
        "(tam cümle olan) yer-tutucudan ÖNCE aynı cümleye özne/parça ekleme — kendi cümleni "
        "tamamla, yer-tutucuyu ayrı cümle olarak bırak; küçük harfle başlayan yer-tutucu cümle "
        "ORTASINDA kalır, öncesine nokta koyup büyük harfle yeni cümle başlatma; bitişik iki "
        "yer-tutucu arasına 've' gibi bağlaç ekleme ve yer-tutucudan sonraki kaynak "
        "noktalamasını (nokta dâhil) düşürme.\n"
        "EK BİLGİ YASAK: yalnız BU paragrafın içeriğini yeniden yaz; paragrafta GEÇMEYEN başka "
        "strateji/model/yöntem adı ya da genel yöntem cümlesi (ör. 'Bulgular p ve %95 GA ile "
        "raporlanmıştır', 'Bland-Altman kullanılmıştır', başka stratejinin latent modeli) EKLEME. "
        "Paragrafa yeni bir özet/kapanış cümlesi iliştirme.\n"
        "META-NOT YASAK: kendi eylemini anlatan not/parantez (ör. '(… eklendi)') ASLA ekleme; "
        "'BU PARAGRAF İÇİN' sana verilen yönergeyi metne kopyalama/etiketleme (ör. "
        "'(klinik-kesme çekincesi)' gibi bir etiket YAZMA) — yönergeyi yalnız uygula.\n"
        "Pasif 3. tekil; ondalık ayırıcı virgül; kaynakta olmayan gerekçe/nedensellik/etki "
        "etiketi EKLEME; @tbl-/@fig- token'larını aynen bırak. Yalnız yeniden yazılmış paragrafı "
        "döndür."
    )
    if note:
        base += "\nBU PARAGRAF İÇİN: " + note
    return base + gloss


def bridge_generate(masked_text, glossary, system=None, max_tokens=6000):
    """Gerçek üretim: gitignored gemini_reformulate.py köprüsünü subprocess çağırır."""
    job = {"system": system or default_system(glossary), "user": masked_text,
           "max_tokens": max_tokens}
    p = subprocess.run([sys.executable, _BRIDGE], input=json.dumps(job),
                       capture_output=True, text=True)
    try:
        r = json.loads(p.stdout)
    except Exception:
        raise RuntimeError("köprü çıktısı ayrıştırılamadı: " + (p.stdout or p.stderr)[:200])
    if not r.get("ok"):
        raise RuntimeError("köprü hatası: " + str(r.get("error"))[:200])
    return r.get("text", "")


def rewrite_section(spec, generate=None, retries=2, max_tokens=6000):
    """spec = {paragraphs:[{text, spans[], caveats[]}], glossary{}}.
    Her paragrafı bağımsız işler (yapı korunur): mask → generate → verify (retry) → splice.
    generate(masked, glossary, system) enjekte edilebilir (test için); yoksa bridge_generate."""
    glossary = spec.get("glossary", {})
    if generate is None:
        def generate(m, g, s):
            return bridge_generate(m, g, s, max_tokens=max_tokens)
    out = []
    for par in spec.get("paragraphs", []):
        text = par["text"]
        spans = list(par.get("spans", [])) + list(par.get("caveats", []))
        masked, mapping = mask(text, spans)
        par_gloss = filter_glossary(glossary, text)  # yalnız bu paragrafta geçen terim → dump'ı önler
        system = default_system(par_gloss, note=par.get("note"))
        attempts, v, draft = 0, None, None
        for _ in range(retries + 1):
            attempts += 1
            try:
                draft = generate(masked, par_gloss, system)
            except Exception as e:  # köprü hatası tek paragrafı düşürür, batch'i çökertmez
                v = {"ok": False, "error": str(e)[:200], "missing": [], "extra": [], "stray": []}
                continue
            v = verify(masked, draft, mapping)
            if v["ok"]:
                break
        ok = bool(v and v["ok"])
        out.append({
            "original": text,
            "masked": masked,
            "rewritten": splice(draft, mapping) if ok else None,
            "status": "ok" if ok else "failed",
            "attempts": attempts,
            "verify": v,
            "n_masked": len(mapping),
        })
    return {"paragraphs": out}


def _main():
    try:
        spec = json.loads(sys.stdin.read() or "{}")
    except Exception as e:
        print(json.dumps({"error": "stdin JSON: " + str(e)[:120]}))
        return
    res = rewrite_section(spec, max_tokens=int(spec.get("max_tokens", 6000)))
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    _main()
