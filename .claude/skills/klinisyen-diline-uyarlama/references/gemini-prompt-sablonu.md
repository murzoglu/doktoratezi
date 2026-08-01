# Harness sözleşmesi: spec + default_system + verify/retry (OPSİYONEL üretici-taslak yolu)

> **Not (birincil akış değişti):** Artık **Claude YAZAR, harness `verify_authored_spans` ile
> mekanik DOĞRULAR** (bkz. SKILL.md Adım 1). Üretici modeli maksimum-sadeye zorlamak parafrazı
> artırıp çarpıtma/halüsinasyon üretir (H5 v6 ¶8 kanıtı). Aşağıdaki mask→generate→verify→splice
> yolu **opsiyonel taslak** üreticidir; çıktısı Adım 2'de ağır denetlenir. Register kuralları
> (Marmara-sade, manşet/grid→tablo, yöntem→ek, İSTATİSTİK-META/dump/note-echo yasağı) her iki
> yolda da geçerlidir.

Üretim artık ham "pasajı modele gönder" değil; **kısıtlı-yeniden-yazım harness'i**
(`scripts/eval/constrained_rewrite.py`, izlenebilir/tracked) üzerinden yürür. Claude
(orkestratör) bir **spec** kurar; harness her paragrafı maskeler (immutable span → `⟦KDUk⟧`)
→ üretici modele (portkey-galileo gateway; şu an GPT-5.5, köprü `gemini_reformulate.py`
gitignored) yollar → yer-tutucuyu **verify** eder (gerekirse retry) → orijinal span'ları birebir
**splice** eder. Kanıt bütünlüğü böylece **mekanik** garanti (sayı/atıf/token/çekince/etiket
düşmesi imkânsız); Claude Adım 2 yalnız modelin sahip olduğu **bağlaç nesrini** denetler.

## Spec şeması (Claude Adım 0.2 envanterinden kurar → harness stdin JSON)

```json
{
  "paragraphs": [
    {"text": "<paragraf metni>",
     "spans":   ["<atomik DOKUNULMAZ değer/etiket>", "..."],
     "caveats": ["<TAM CÜMLE çekince>", "..."],
     "note":    "<bu paragrafa özel yönerge — opsiyonel>"}
  ],
  "glossary": {"<yabancı psikometrik model>": "<klinik karşılık>"},
  "max_tokens": 12000
}
```

- `spans` + `caveats` maskelenir → verbatim korunur. `@tbl-*`/`@fig-*`/`[@key]` **otomatik**
  tespit + maskelenir (`detect_auto_spans`; elle eklemek gerekmez).
- `glossary` **paragraf-bazlı süzülür** (`filter_glossary`): yalnız o paragrafta GEÇEN terim
  modele gider → kullanılmayan tanımın paragraf sonuna boşaltılması (dump) engellenir.
- `note` metne kopyalanmaz, yalnız uygulanır (META-NOT yasağı).
- Spec üretici script span'ların kaynakta **birebir** bulunduğunu ön-kontrol etmeli (eşleşmeyen
  span = düzelt; yoksa maske sessizce atlar).

## Maskeleme granülerliği (kanıt bütünlüğü + dikişsizlik) — kalibrasyon dersleri

| Öğe | Maske biçimi | Neden |
|---|---|---|
| **Atomik değer** (sayı/oran/eşik/token/atıf) | cümle-içi minimal | tek parça; yeniden yazımda yer değiştirmez |
| **Çekince / kapsam sınırı** | **TAM CÜMLE** | model çekinceyi yeniden kurup zayıflatamaz/atamaz |
| **Tam-yüklemli kapsam öbeği** ("…yalnız X ve Y alt ölçeklerinde tahmin edilmiştir") | **TAM CÜMLE ya da yüklem-DAHİL öbek** | parça (yalnız "X ve Y'de") maskelenirse model özne/yüklemi yeniden kurunca **bağlaçsız dikiş/run-on** doğar — H5 ¶4 dersi |
| **Kalın yapısal etiket** (`**Strateji N (…).**`) | maskele | düşmesin / yeniden adlandırılmasın |

## default_system — klinik hekim register'ı (harness'te gömülü, `default_system(glossary, note)`)

Hepsi modelin **bağlaç nesrine** dairdir; kanıt zaten maskelidir:

- **SAYILARI TUT:** p/%95 GA/r/katsayı/yüzde/ICC metinde KALIR — hekim (KDT altyapılı) kanıtı
  kendi tartar; tabloya kaçırma/yuvarlama/atma.
- **İSTATİSTİK-META YASAK** *(Guardrail 3):* p/%95 GA/korelasyon gibi hekimin BİLDİĞİ ölçütü
  **tanımlama**; "sonuçlar/bulgular p ve %95 GA ile raporlanır/yorumlanır" türü genel meta-cümle
  **ekleme** — bu değerler yalnız geldikleri yer-tutucularda kalır; paragrafta yoksa hiç anma.
- **FORMÜL HARİÇ:** matematiksel formülü metne yazma → "(formülizasyon/katsayı tanımları teknik
  ekte)" havale; formülün ürettiği **sonuç** değerleri (p, katsayı) metinde kalır.
- **KLİNİK ÖNCE (so-what):** her paragrafı teknik yapıdan ÖNCE klinik anlamıyla (aile dinamiği /
  klinik değerlendirme karşılığı) tek sade cümleyle başlat. **'poliklinikte' / 'poliklinik' gibi
  klinik-ortam ifadesi KULLANMA** (yanlış register; "klinik olarak / klinik açıdan / aile
  değerlendirmesinde" de).
- **KISA CÜMLE** (tek-yargı; noktalı-virgül zinciri yok) · **GLOSS YEDİR** (yalnız paragrafta
  geçen yabancı psikometrik model, tanımı cümleye yedirerek bir kez; hekimin bildiğini —
  Bland-Altman/p/GA — glosslama).
- **EK BİLGİ YASAK** *(Guardrail 1):* paragrafta GEÇMEYEN model/istatistik/strateji hakkında
  cümle ekleme; yeni özet/kapanış cümlesi iliştirme.
- **META-NOT YASAK** *(Guardrail 2):* kendi eylemini anlatan not/parantez ('(… eklendi)') ya da
  `note` yönergesini metne kopyalama/etiketleme ('(klinik-kesme çekincesi)' gibi) YOK.
- **DİKİŞ:** çift noktalama ('.;', '. olarak')/sarkan yüklem/kip uyumsuzluğu yok; nokta ile biten
  maskeden sonra yeni yüklem ekleme; BÜYÜK harfle başlayan (tam cümle) maskeden ÖNCE aynı cümleye
  özne/parça ekleme; küçük harfle başlayan maske cümle ORTASINDA kalır; bitişik iki maske arasına
  bağlaç ekleme, kaynak noktalamasını düşürme.
- Pasif 3. tekil; ondalık virgül; kaynakta olmayan gerekçe/nedensellik/etki etiketi EKLEME.

## Çalıştırma (Adım 1)

```bash
python3 /tmp/kdu_<bölüm>_spec.py > /tmp/kdu_<bölüm>_spec.json   # spec üret + span ön-kontrolü
python3 scripts/eval/constrained_rewrite.py < /tmp/kdu_<bölüm>_spec.json > /tmp/kdu_<bölüm>_out.json
```

Harness her paragraf için döner:
`{original, masked, rewritten, status(ok|failed), attempts, verify{ok,missing,extra,stray}, n_masked}`.
`status:failed` = yer-tutucu düştü/çiftlendi (retry tükendi) → o paragraf splice EDİLMEZ
(`rewritten=null`); Claude o paragrafı yeniden kurar. Üretici modeli/config'i `.env`
`GALILEO_GEMINI_CONFIG` belirler (köprü `.env`'den okur, sır basmaz). gpt-5.x yalnız varsayılan
`temperature`(1) kabul eder → köprü gpt-5'te temperature'ı hiç göndermez. Gateway erişilemezse
köprü `ok:false` → **bildir; sessiz Claude-fallback YOK** (kullanıcı açık isterse fallback +
"Claude-fallback" işareti).

## Adım 2 — Claude modelin bağlaç nesrini denetler (harness'in göremediği)

`verify` **kanıtı** mekanik garanti eder; ama **üslup dikişi / eklenen cümle / F1–F5** modelin
yazdığı nesirdedir ve varyansla her koşuda farklı çıkabilir. Claude her paragrafı orijinalle
kıyaslar:

- **Dikiş:** run-on ("…tanımlanır yalnız…"), büyük-harf maske önüne kelime ("Triangülasyonda
  Bir…"), bağlaç/nokta düşmesi → 1–4 kelimelik elle onarım.
- **F1–F5** (abartı/kapsam · eklenen iddia · 1. şahıs · terim kayması) + **eklenen gloss/kavram**
  (kaynakta yok, ör. bir metriği "…ile karıştırılmamalıdır" diye tanımlama) → düşür ya da spec'i
  düzeltip yeniden koş.

Harness çıktısı bir **taslaktır**; nihai metin = harness çıktısı + Claude Adım-2 elle onarımı,
ardından denetim kapısı (SKILL.md). Israrlı ihlal (spec düzeltmesi + 2–3 koşuya rağmen) → o
paragrafı reddet, kullanıcıya bildir. Tur sayısı + F# bulguları + elle onarımlar journal'a yazılır.
