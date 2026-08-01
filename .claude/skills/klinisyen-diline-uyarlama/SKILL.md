---
name: klinisyen-diline-uyarlama
description: >
  Bir tez pasajını **Sosyal Pediatri klinisyen jürisine** (çocuk sağlığı öğretim üyeleri;
  psikometri/davranış bilimi/ileri istatistik altyapısı YOK) uygun; sade, çok iyi anlaşılır,
  akıcı, sebep-sonuç ilişkilerini net kuran bir dile **yeniden üsluplayan** kapı. Üretimi
  portkey-galileo gateway üzerinden yapılandırılmış üretici model (`.env`; şu an GPT-5.5) yapar,
  ajan çıktıyı değerlendirip onaya sunar. Tüm hesaplama, sayı, bulgu, yön, anlamlılık, atıf ve
  kanonik token birebir korunur. Zenginleştirme değil ERİŞİLEBİLİRLİK (vektör aşağı). Dosyaya
  doğrudan yazmaz; sci-audit + galileo kapısından geçirir, journal ritüeli tutar. Tetikleyiciler:
  "klinisyen diline uyarla", "jüriye sadeleştir", "çocuk hekimi jüri için sadeleştir", "bu pasaj
  jüriyi boğuyor", "jargon jüriye karmaşık". DEĞİL: ayrı açıklama (data-narrative), literatür
  zenginleştirme (anlatim-zenginligi), figür/tablo sunumu (veri-gosterimi-zenginligi).
---

# Klinisyen Diline Uyarlama — Claude yazar (sade+Marmara), harness kanıtı mekanik doğrular, kapı geçer, onaya sunar

Sunulan pasajı/bölümü, **Sosyal Pediatri klinisyen jürisinin** ilk okuyuşta anlayacağı
register ve kurguya uyarla: sade, akıcı, **açık sebep-sonuç**, az-altyapılı okura dahi geçen
mesaj — **karşılığında tüm kanonik içeriği (sayı, bulgu, yön, anlamlılık, atıf, token,
çekince) titizlikle koru.** Erişilebilirlik kapısı; **zenginleştirme değil** (literatür
eklemez), **açıklama değil** (ayrı çıktı üretmez) — tez metnini fiilen revize eder.

**Rol dağılımı (bu skill'in özü) — birincil akış: Claude YAZAR, harness DOĞRULAR:**
- **Claude (sen) YAZARSIN** — sade + Marmara-resmi + sadık nesri sen kurarsın: kısa düz bildirim
  cümlesi, klinik so-what önce, jargon glossu yedirilmiş, grid→tablo, yöntem mekaniği/formül →
  teknik ek. Sayı/çekince/**verdikt VERBATIM**. (Neden: üretici modeli maksimum-sadeye zorlamak
  parafrazı artırıp çarpıtma/halüsinasyon üretir — H5 v6 ¶8 kaynağa-aykırı verdikt kanıtı.)
- **Harness DOĞRULAR** (`scripts/eval/constrained_rewrite.py`) — `verify_authored_spans(authored,
  required)` yazdığın metinde her DOKUNULMAZ span'ın (sayı/@token/[@cite]/çekince-verdikt)
  korunduğunu **mekanik** onaylar; düşme/mutasyon = FAIL. Eklenen abartı/halüsinasyonu YAKALAMAZ.
- **Adım 2 + galileo** — eklenen abartı/overclaim/halüsinasyonu denetler (mekaniğin göremediği).
- **Üretici model OPSİYONEL** — portkey-galileo gateway (`.env`/`GALILEO_GEMINI_CONFIG`; köprü
  `gemini_reformulate.py`) taslak üretebilir (`rewrite_section` mask→generate→verify→splice); ama
  zorlanınca çarpıtır → birincil değil. Detay: `references/gemini-prompt-sablonu.md`.

**Değişmez temel:** Kanıtın letter'ını çiğnemek kanıtın spirit'ini çiğnemektir. Sadeleştirme
adına en küçük abartı, kapsam genişletme, eklenen gerekçe veya düşen çekince = **çalışmanın
bulgusunu değiştirmektir** ve reddedilir — Gemini'den gelse de.

## Adım 0 — Claude: önce doğrula, kitleyi tanı (Gemini'yi çağırmadan ÖNCE)

**Asla doğrulamadan Gemini'ye gönderme, asla Gemini çıktısını körlemesine sunma.** Sırayla:

1. **Kaynağı doğrula.** Pasajın **gerçek** dosya:satırını `grep` ile bul (dosya adı tahmin
   etme). **DOKUNULMAZ envanteri** çıkar: tüm sayılar, `@tbl-*`·`@fig-*`·`[@key]` token'ları,
   `[KEŞİFSEL]`/`[POST-HOC]` etiketleri, çekince/kapsam ifadeleri. Her sayının kanonik değerini
   üreten artefakttan teyit et. Komut kalıpları: **`references/kaynak-dogrulama.md`**.
   t1dm-tez-rehberi **Faz 0** + **Faz 0.5** kapısı geçmezse dur.
2. **Journal'ı oku (seans başı ritüeli).**
   `tez-yazim/04_kalite-kontrol/klinisyen-diline-uyarlama-journal.md` — durum panosu + backlog.
3. **Kitleyi kalibre et.** Pasajdaki metodolojik yükü tanı; klinisyenin *bildiği* ile
   *çevrilmesi gerekeni* ayır: **`references/hedef-kitle-personasi.md`**.

Bu envanter + kalibrasyon, hem Gemini'ye vereceğin talimatı hem değerlendirme ölçütünü belirler.

## Adım 1 — Claude yazar, harness mekanik doğrular (birincil akış)

Sade + Marmara-resmi + sadık paragrafı **sen yazarsın**. Kurallar:
- **Sade AMA Marmara:** kısa düz bildirim cümlesi; pasif/nominal 3. tekil; **retorik soru /
  eksiltili cümle / konuşma dili YOK**; klinik so-what ÖNCE ("klinik olarak / aile
  değerlendirmesinde"; **"poliklinikte" YOK**).
- **Kanıt VERBATIM:** sonuç sayıları (p/%95 GA/r/katsayı/%/ICC/aralık) + çekince + **verdikt**
  birebir korunur. **Verdikti/çekinceyi ASLA parafraz etme** — çarpıtma en çok orada olur
  (H5 v6 ¶8 kaynağa-aykırı "tutarlı ayrışma bulundu" halüsinasyonu).
- **Grid→tablo:** çok-hücreli sayı gridini (alt ölçek × grup dökümü) metne yazma →
  "(… @tbl-…'da sunulmuştur)"; değerin **tabloda VARLIĞINI doğrula** (yoksa taşıma = veri kaybı,
  yasak — R üretici/tabloyu kontrol et).
- **Yöntem mekaniği/formül → teknik ek:** "(formülizasyon/katsayı tanımları teknik ekte)";
  metinde yöntemin tek-cümlelik klinik adı + NE bulduğu kalır. (Uygulama turunda formül Ekler'e eklenir.)
- **Doğrulanmamış yön/etki iddiası EKLEME** ("X arttıkça Y artar" kaynakta/artefaktta yoksa).
- **Jargon glossu:** yalnız yabancı psikometrik modeli, cümleye yedirerek, bir kez
  (`docs/tez-kilavuz/klinik-karsilik-sozlugu.md`); hekimin bildiğini (p/GA/Bland-Altman) glosslama.

Sonra Adım 0 DOKUNULMAZ envanterini **mekanik doğrula**:

```python
import constrained_rewrite as cr
cr.verify_authored_spans(authored_text, required_spans)   # {ok, missing, checked}
```

`ok:False` → düşen/mutasyona uğrayan span'ı geri koy, tekrar doğrula. Bu, sadeleştirirken
sayı/çekince/verdikt düşürmediğini **mekanik** kanıtlar (eklenen abartıyı değil — o Adım 2/galileo).

**Opsiyonel üretici-taslak yolu** (zorlanınca çarpıtır, birincil değil): spec kur → `python3
scripts/eval/constrained_rewrite.py < spec.json` (mask→generate→verify→splice) → çıktıyı Adım 2'de
ağır denetle. Sözleşme + register + granülerlik: `references/gemini-prompt-sablonu.md`. Gateway
erişilemezse bildir. **KVKK:** gateway'e yalnız manuskript/literatür terimi (ham veri ASLA).

## Adım 2 — Claude: Gemini taslağını DEĞERLENDİR (kapıdan önceki asıl iş)

Harness çıktısı bir **taslaktır**. `verify` maskeleneni (sayı/atıf/token/çekince/etiket)
**mekanik** garanti eder — o eksende diff yapman gerekmez, `verify.ok`'a güven. Adım 2'nin işi
**modelin sahip olduğu bağlaç nesridir**: harness'in göremediği abartı/eklenen iddia/üslup/dikiş.

**Değerlendirme kontrol listesi (hepsi geçmeli):**
- **verify + status:** her paragraf `status:ok` + `verify.ok:true` mi? `failed` → paragrafı
  yeniden kur (spec'i düzelt, yeniden koş). (Sayı/token/atıf diff'i harness yapar.)
- **F1 — abartı/kapsam genişletme:** "eşitlendi/denk/tamamen/tüm özelliklerde", "neredeyse"→
  "tamamen"? Kaynağın kapsamı/temkini korunmuş mu?
- **F2 — eklenen gerekçe/iddia:** kaynakta olmayan neden/nedensellik/yorum cümlesi; bir metriği
  kaynakta olmayan bir gloss/uyarıyla ("…ile karıştırılmamalıdır") tanımlama.
- **F3 — tez sesi:** pasif 3. tekil mi (1. şahıs YOK)?
- **F4 — terim kayması:** mevcut terim korunmuş mu ("medyan→ortanca" yok; "partner→eş" gibi
  düad→evlilik kayması yok)?
- **İSTATİSTİK-META (Guardrail 3):** p/%95 GA/korelasyonu **tanımlayan** ya da "sonuçlar p/GA ile
  raporlanır" türü **genel meta-cümle** eklenmiş mi? (özellikle o paragrafta p/GA yoksa) = düşür.
- **Register:** klinik-lead "klinik olarak / klinik açıdan / aile değerlendirmesinde" mi —
  **"poliklinikte" gibi klinik-ortam ifadesi YOK**; ondalık virgül; jargon glossu yedirilmiş mi?
- **DİKİŞ:** yer-tutucu çevresinde run-on ("…tanımlanır yalnız…"), büyük-harf maske önüne kelime
  ("Triangülasyonda Bir…"), bağlaç/nokta düşmesi var mı? → 1–4 kelimelik elle onar.
- **EK BİLGİ / note-echo:** paragraf-dışı model/istatistik cümlesi ya da note etiketi
  ("(klinik-kesme çekincesi)") sızmış mı?
- **Amaç:** gerçekten klinisyen-anlaşılır + akıcı + sebep-sonuç açık; detay kaybı yok.
- **Yeniden sıralama:** varsa §Yeniden sıralama kapısına uygun mu (yerel + gerekçeli)?

**Karar:** (a) **kabul** → Adım 3; (b) **spec düzelt + yeniden koş** → dikiş için granülerliği
(tam-cümle maske) düzelt, F# için `note`/register kuralını sıkılaştır, yeniden üret (2–3 koşu);
(c) **küçük düzeltme** → Claude tek tük dikiş/ihlali elle onarır (1–4 kelime; ör. "poliklinikte"
sil, "Triangülasyonda " sil), **bulguyu asla mutasyona uğratmadan**; (d) **reddet** → ısrarlı
ihlalde paragrafı at, kullanıcıya bildir. Karar + F# bulguları + elle onarımlar journal'a girer.
Nihai metin = harness çıktısı + Claude Adım-2 elle onarımı.

## Yeniden üsluplama reçetesi (harness register'ında gömülü, Claude denetler)

Reçete `constrained_rewrite.default_system` klinik hekim register'ında kodlu; yeniden yazılmış
pasaj **şu bileşenlerden ve yalnız bunlardan** oluşur:
1. **Klinik çerçeve** (klinik "so-what" önce — "klinik olarak/aile değerlendirmesinde";
**"poliklinikte" DEME**). 2. **Açık sebep-sonuç** (kaynakta olmayan yeni gerekçe EKLEME, F2).
3. **Jargon çevirisi** (klinik karşılık + parantezde özgün ad; **hekimin bildiği p/%95 GA'yı
tanımlama**). 4. **Cümle bölme.** 5. **Yerel yeniden sıralama** (kapıya tabi).
**Sayı KALIR, formül teknik eke** (hekim = KDT altyapılı).
**Ölçek uyumu:** basit pasaj hafif dokunuş; ağır metodoloji pasajı tam yeniden kurma.
**Detay kaybı yok.** Yöntem + tam örnek: **`references/yeniden-uslup-yontemi.md`** +
**`references/ornek-yeniden-uslup.md`** (yeni işten önce üslup kalibrasyonu).

## Yeniden sıralama kapısı (yalnız yerel, gerekçeli, ayrı onaylı)

Pedagojik açıklık için blok içi sıra değişince: diff'te **↔ yeniden sıralama** işaretle;
**klinik-pedagojik gerekçe** yaz; onay özetinde **ayrı listele** (kullanıcı ayrıca onaylar).
**Güvence:** bulgu *kümesi* değişmez; sayı/yön/anlamlılık/atıf sabit; çapraz-referanslar
(`@tbl`/`@fig`, "yukarıda/aşağıda", ileri-geri atıf, özet/summary) yeniden doğrulanır;
**Bulgular'da** `csr_numeric_trace_audit.py` yeniden koşar (yüksek-risk eşsiz = 0). Yereldir;
argüman mantığını/atıf zincirini kıran sınırı aşamaz.

## Rasyonalizasyon tablosu — Gemini taslağında BUNLARI gördüğünde reddet/düzelt

| Rasyonalizasyon (Gemini'nin ya da senin) | Gerçek |
|---|---|
| "Daha akıcı: 'iki grup eşitlendi / tüm özelliklerde denk oldu'" | Kaynak yalnız **ayarlama-seti değişkenlerinde** "kayda değer fark kalmadı" diyor. Genişletme + abartı (F1). Kapsamı **birebir** koru. |
| "'neredeyse kayboldu' yerine 'tamamen/tümüyle kayboldu' daha temiz" | Her güçlendirme büyüklük mutasyonu (F1). Ton kaynaktakiyle aynı: "neredeyse" → "neredeyse". |
| "Okur anlasın diye 'bu farklar hastalığa mı bağlı belli değil' gerekçesi ekleyeyim" | Kaynakta olmayan nedensel-çıkarım iddiası (F2). Yeni gerekçe/iddia **ekleme**. |
| "Sıcak dursun: 'kullandık / uyguladığımız / topladığımızda'" | Marmara **pasif 3. tekil**. 1. şahıs tez sesini bozar (F3). |
| "'medyan' yerine 'ortanca' daha Türkçe" | Terim tez genelinde **tek karşılık**; keyfî geçiş tutarlılığı bozar (F4). |
| "Anlamı bozmuyorum, netleştiriyorum" | 'sınırda'→'önemli', korelasyon→'neden' yön/etiket mutasyonu. Etki-büyüklüğü/nedensellik etiketi eklenmez. |
| "Kısaltmak için şu çekinceyi atabilirim" | 'Sade **ama detay kaybı yok**' — çekince/kapsam/alt-ayrım/`[KEŞİFSEL]` düşmez. |
| "Gemini yazdı, herhalde doğrudur" | Gemini akıcı ama disiplinsiz olabilir; **her taslak Adım 2'den geçer.** Kaynak, Gemini değil. |

## Red flags — DUR, kaynağa hizala (Gemini çıktısında da)

- "eşitlendi / denk oldu / tamamen / tümüyle / tüm özelliklerde" (kaynakta yoksa)
- kaynakta olmayan yeni gerekçe/neden/iddia cümlesi
- "biz / kullandık / uyguladık" (1. şahıs)
- "medyan→ortanca" gibi terim değişimi
- "sınırda→önemli", "birlikte değişir→neden olur" (yön/etiket kayması)
- bir çekinceyi/kapsam sınırını/alt-ayrımı atma; bir sayı/token/atıf çıkarma-yuvarlama

**Hepsi: DUR. Gemini'yi yeniden yönlendir veya düzelt. Bulguyu değil yalnız üslubu değiştir.**

## Zorunlu davranışlar

- **Tez-geneli bağlam etkisi notu (zorunlu).** Her uyarlamada üret: terim tutarlılığı
  dalgalanması (→ backlog), çapraz-referanslar, özet/summary/kısaltmalar yansıması, pasajın
  başka yerde tekrarı. Not onay özeti + journal girdisine girer.
- **Dil/biçim:** Türkçe, **pasif 3. tekil**, **ondalık virgül**; terim ilk geçişte klinik
  karşılık + parantezde özgün ad. Marmara sözleşmesi (`tez-yazim/00_kaynak-kurallari/`) +
  `tez-yazim/04_kalite-kontrol/insan-turkcesi-retorik-playbook.md`.
- **Doğrudan yazmaz.** Öneri → kapı → **açık onay** → Edit. Denetimi onaydan sonraya erteleme.
- **Kaynak = Gemini değil.** Gemini taslağı bir **öneridir**; kanonik değer artefakttan,
  disiplin Claude'un değerlendirmesinden gelir.
- **Journal (seans sonu).** Günlüğe gir: pasaj (dosya:satır), Gemini modeli + kaç tur, çıkan
  F# bulguları + karar, yeniden sıralama+gerekçe, kapı sonucu, bağlam etkileri, açık takipler;
  pano + backlog güncelle.

## Denetim kapısı (uygulamadan ÖNCE — üç kademe, araçları KARIŞTIRMA)

| Kademe | Araç (Claude Code) | Ona-yerel ikame | Rol |
|---|---|---|---|
| **HARD** | `sci-audit:check-turkish … --strictness certification` | `python3 scripts/util/tr_corpus_audit.py all --fail-on blocker` + `tez_checklist_verify.py --fast` (ondalık-virgül) | Türkçe imla + ondalık virgül (nokta-`p` = blocker) |
| **HARD** | `sci-audit:verify-citations` · `check-stats` | `python3 scripts/util/bib_hygiene.py all` · `python3 scripts/util/claim_certification.py` (+ `csr_causal_label_audit.py`) | Atıf bütünlüğü · istatistik tutarlılığı |
| **HARD** | `csr_numeric_trace_audit.py` (yalnız Bulgular yeniden sıralaması) | *(aynı — repo-yerel)* | Yazılı bulgu ↔ CSV izi; yüksek-risk eşsiz = 0 |
| **SOFT-block** | `galileo_judge` (`text`, `section_type`, `evidence` = **orijinal pasaj + artefakt**) | galileo-audit MCP (`.ona/mcp-config.json`) · CLI fallback: `python3 scripts/eval/galileo_bridge.py` | **Ana kontrol:** Gemini sadeleştirmesi iddiayı çarpıttı mı — faithfulness/groundedness/overclaim/hallucination |
| **advisory** | `galileo_coherence` · `galileo_reference_prose` | galileo-audit MCP (aynı sunucu) | Akış/tekrar · atıf nesri |

**Ona (Gitpod) çalışma notu:** `sci-audit` bir Claude Code plugin'idir
(`sci-audit@cureonics-marketplace`) ve **Ona'da mevcut değildir**; yukarıdaki
"Ona-yerel ikame" sütunu aynı HARD güvenceyi repo-yerel araçlarla sağlar (blocker/FAIL =
düzelt-ve-tekrar; HARD anlamı korunur). `galileo_*` tool'ları Ona'da
`.ona/mcp-config.json`'daki **galileo-audit** MCP sunucusundan gelir (Ona `.ona/`
config'ini okur; `.mcp.json` Claude Code içindir); MCP bağlanmazsa `galileo_bridge.py`
stdio köprüsü CLI olarak çağrılır. Harness (`constrained_rewrite.py`) ve üretici
gateway (`gemini_reformulate.py --probe`) Ona'da değişmeden çalışır. Skill'in kendisi
Ona'da açıklama-eşleşmesiyle otomatik tetiklenir (repository skill; `/` invoke gerekmez).

`galileo_judge` (bağımsız GPT-5.4) burada Gemini çıktısının **ikinci-model denetimi** işlevini
de görür — üretici (Gemini) ≠ denetleyici (GPT-5.4 judge + Claude). Kademe eşikleri
`.claude/galileo.local.md`; doktrin `…/manuskript-denetimi-sciaudit.md` §6. **HARD** override
yok; **SOFT-block** `certified-final`'ı durdurur (insan-override'lı). sci-audit'in yerine
galileo veya checklist geçmez.

## Yürütme sırası (sabit)

1. Adım 0: bağlamı sabitle + DOKUNULMAZ envanter; journal oku; kitle kalibre et.
2. Adım 1: paragrafı sade+Marmara+sadık **YAZ** (kanıt/çekince/**verdikt verbatim**; grid→tablo;
   yöntem/formül→teknik ek; poliklinik yok; doğrulanmamış yön iddiası yok); `verify_authored_spans`
   ile DOKUNULMAZ mekanik doğrula (FAIL→düzelt). (Üretici-taslak yolu opsiyonel.)
3. Adım 2: yazdığın metni denetle — mekanik doğrulama düşmeyi yakalar; sen **eklenen** abartı/
   overclaim/halüsinasyon + F1–F5 + Marmara + register ararsın → düzelt.
4. Tez-geneli bağlam etkisi notu.
5. Denetle (üç kademe) — uygulamadan ÖNCE.
6. Onaya sun: diff (eski→yeni), Gemini modeli+tur sayısı + çıkan F# bulguları, yeniden-sıralama
   + gerekçe, kapı özeti, bağlam-etkisi notu, backlog güncellemesi.
7. Onay sonrası: Edit → (Bulgular reorder ise tam `tar_make` + numeric-trace) → journal güncelle
   → kapanışta `sci-audit:audit … --lang tr` (**Ona'da yerel ikame:**
   `python3 scripts/util/tr_corpus_audit.py all --fail-on blocker` +
   `python3 scripts/util/tez_checklist_verify.py --fast`) + bölüm kapanıyorsa `/tez-dogrulama`.

## Devir (scope guard)
- Ayrı açıklama (metni değiştirmeden) → `data-narrative`
- Literatürle zenginleştirme / yeni atıf → `anlatim-zenginligi` · `referans-kapisi`
- Figür/tablo sunum katmanı → `veri-gosterimi-zenginligi`
- Bölüm finalizasyonu → `bolum-sertifika` · Kapanış → `tez-dogrulama`
- **Aynı bölgede eşgüdüm:** önce zenginleştir (anlatim), **sonra** son okunabilirlik geçişi
  olarak klinisyen-diline-uyarla. Protokol:
  `tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md`.

## Yasaklar
- Doğrulamadan Gemini'ye gönderme; Gemini çıktısını Adım 2'den geçirmeden sunma.
- Sayı/token/atıf çıkarma-yuvarlama-uydurma; kaynak kapsamını genişletme/abartma.
- Kaynakta olmayan gerekçe/nedensellik/etki-büyüklüğü etiketi ekleme (Gemini eklese de).
- Çekince/kapsam/alt-ayrım düşürme; 1. şahıs; keyfî terim değişimi.
- Gemini erişilemeyince **sessizce** Claude'a düşme; dosyaya doğrudan yazma; denetimi erteleme.

## Referanslar
- **`references/kaynak-dogrulama.md`** — dosya:satır, DOKUNULMAZ envanter, numeric-trace, çapraz-ref.
- **`references/hedef-kitle-personasi.md`** — klinisyen jüri: ne bilir / ne çevrilmeli + klinik karşılık.
- **`references/yeniden-uslup-yontemi.md`** — reçete, yerel yeniden sıralama kuralları + gerekçe, ölçek uyumu.
- **`references/gemini-prompt-sablonu.md`** — harness sözleşmesi: spec şeması + maskeleme granülerliği + `default_system` klinik register + verify/retry + köprü.
- **`references/ornek-yeniden-uslup.md`** — tek referans-kalite öncesi/sonrası örnek (F1–F5 uyumlu).

---

## Ek: tam tetikleyici kapsamı (arşiv)

Bu skill'in `description` alanı Copilot skill kayıt bütçesine (~1 KB) sığması için
kısaltılmıştır. Kısaltmadan önceki tam tetikleyici/anahtar-kelime listesi kayıt dışı
kalmasın diye burada saklanır; kapsam **değişmemiştir**.

> Bir tez pasajını/bölümünü, **Sosyal Pediatri klinisyen jürisine** (çocuk sağlığı ve
> hastalıkları öğretim üyeleri; klinisyen kökenli; psikometri / davranış bilimi / ileri
> istatistik altyapısı YOK) uygun, sade, çok iyi anlaşılır, akıcı, sebep-sonuç ilişkilerini net
> kuran, az-altyapılı okura dahi mesaj veren bir dile **yeniden üsluplayan** kapı. Üretimi
> **portkey-galileo gateway üzerinden yapılandırılmış bir üretici model** (`.env`; şu an
> GPT-5.5) yapar; **Claude çıktıyı değerlendirir** ve amaca uygunsa onaya sunar. Tüm hesaplama,
> sayı, bulgu, yön, anlamlılık, atıf ve kanonik token birebir korunur. Zenginleştirme değil
> ERİŞİLEBİLİRLİK; vektör aşağı (sadeleştirme). Dosyaya doğrudan yazmaz — sci-audit + galileo
> kapısından geçirip onaya sunar; journal ritüeli tutar. ŞU DURUMLARDA KULLAN: kullanıcı
> "klinisyen diline uyarla", "jüriye sadeleştir", "çocuk hekimi jüri için sadeleştir", "bu pasaj
> jüriyi boğuyor", "metodoloji jargonu jüriye çok karmaşık", "bunu klinisyene anlaşılır yap",
> "klinisyen-diline-uyarlama" derse. ŞUNLAR İÇİN DEĞİL: ayrı açıklama üretme (data-narrative),
> literatürle zenginleştirme (anlatim-zenginligi), figür/tablo sunum katmanı
> (veri-gosterimi-zenginligi).
