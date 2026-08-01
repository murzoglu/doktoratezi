---
description: Seçili tez metninin ANLATIMINI + referans doğruluk/kapsam/tutarlılığını zenginleştirir (sayı/istatistik/bulgu ve yapıları DOKUNULMAZ, değiştirilmez); sci-audit + galileo kapısından geçirip onaya sunar (dosyaya doğrudan yazmaz)
argument-hint: "[seçili metin veya chapters/<bolum>.qmd konumu]"
---

# /anlatim-zenginligi — Anlatım Zenginleştirme Kapısı

Zenginleştirilecek metin: **$ARGUMENTS** — argüman boşsa editör seçimini (`ide_selection`) kullan.

Seçili tez pasajını, ilgili literatürün **tam metniyle temellendirilmiş**, okuyucu için
bağlamı genişletilmiş, teknik terimleri **izah eden**, Türkçe anlam akışı + imlaya uygun
bir revizyona dönüştürür. **Revizyonu chapter dosyasına DOĞRUDAN yazmaz; sci-audit +
galileo kapısından geçirip onaya sunar.**

**Kapsam — DOKUNULMAZ kanıt bölgesi vs. düzenlenebilir anlatım/referans bölgesi.** Bu araç
YALNIZ **etkili bilimsel anlatım** ile **referansların doğruluk / kapsam / tutarlılığı**
üzerinde çalışır; çalışmanın **bulgularını, sayısal sonuçlarını ve yapılarını DEĞİŞTİRMEZ.**
Sayı/istatistik (g, β, SE, p, %GA, ICC, AUC, N, yüzde …), bulgunun içeriği / yönü / anlamlılığı /
büyüklüğü, bulgu sırası ve `@tbl-*`/`@fig-*`/`[@key]` token'ları **aynen korunur** — yeniden
yorumlanmaz, yuvarlanmaz, güçlendirilmez; kaynakta olmayan özgüllük (informant "anneden",
"klinik açıdan anlamlı", "sağlam/dayanıklı", nedensellik) **eklenmez.** Zenginleştirme =
terim izahı + okuyucu bağlamı + **ayrı ve atıflı** literatür karşılaştırması; bu çalışmanın
yeni bir bulgusu gibi sunulmaz.

## Yürütme (sıra sabittir)

1. **Bağlamı sabitle — DOSYA ADI TAHMİN ETME.** Seçili ifadeyi chapter'larda ara
   (`grep -rn "<seçili parça>" chapters/`) ve pasajın **gerçek** dosya + satırını bul;
   dosya adını hatırdan yazma. Sayısal iddiaların kaynak-tekilliğini artefakttan doğrula
   (gömülü literal yok). t1dm-tez-rehberi **Faz 0** kapsam + **Faz 0.5** tedbir kapısı
   geçmezse dur.
2. **Literatür zenginleştirme (evidentia D-kaskad + Minerva).** Doktrin:
   `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` (D0–D6).
   `minerva_literature_search` (D2) + `minerva_*_fulltext`/`get_article` (D4, annas ÖNCESİ).
   **Türkçe sorgu = `mode:semantic` zorunlu; İngilizce sorgu = hybrid.** Tam metni
   `anamnesis.ingest_document → hybrid_query` ile **chunk-alıntıla; verbatim toplu kopya
   yok (telif)**. **Kaynak makaleyi BÜTÜN olarak kavra — parça değil:** bir referansı
   kullanmadan önce tam metnini ingest edip amaç / yöntem / örneklem / ana-iddia / koşul-kısıt /
   temkin ekseninde geniş bağlamıyla semantik olarak kavra; zenginleştirmeyi bu **bütün-makale**
   anlayışından türet, tek çekilmiş bir cümleden değil (cherry-pick = çarpıtma). Kaynağın somut
   bilimsel iddiasını **kapsam ve koşullarıyla** temsil et — düzleştirme / abartma / olduğundan
   daha uyumlu gösterme yok. **KVKK: gateway'e yalnız literatür terimi — katılımcı/ham/aile-düzeyi
   veri asla gönderilmez.** Ağır fan-out için `evidentia:evidence-synthesizer`.
3. **Türkçe revize et — YALNIZ anlatım/referans bölgesi (kanıt/bulgu bölgesine dokunma).**
   Marmara sözleşmesi (`tez-yazim/00_kaynak-kurallari/`): pasif 3. tekil; **ondalık virgül**
   (`0,38`, `p<0,001`); teknik terim ilk geçişte **tam ad + parantezde kısaltma/özgün karşılık**.
   **`[@key]` ve `@tbl-*`/`@fig-*` token'larını, tüm sayı/istatistiği ve bulgunun içeriğini/
   yönünü/anlamlılığını/sırasını AYNEN koru; yeniden yorumlama, güçlendirme, yuvarlama, kaynakta
   olmayan özgüllük ekleme; başlık ve bölüm yapısını değiştirme.** Zenginleştirme yalnız üç
   şeyi ekler: (a) mevcut terimlerin izahı, (b) okuyucu bağlamı, (c) **ayrı ve atıflı** literatür
   karşılaştırması (bu çalışmanın yeni bulgusu gibi sunulmaz). Nesir kalitesi:
   `tez-yazim/04_kalite-kontrol/insan-turkcesi-retorik-playbook.md`.
4. **Yeni atıf = ADAY (uydurma YASAK).** Zenginleştirme `references.bib`'de olmayan kaynak
   gerektiriyorsa: adayı ayrı bir "öneri" bloğunda listele; revizyon uygulanmadan ÖNCE
   `/referans-kapisi` (7-adım: DOI → tam-metin → Zotero → claim) ile `cite-ok` yap. Kapı
   kapanmadan hiçbir atıf metne girmez.
5. **Denetle — UYGULAMADAN ÖNCE, üç kademeli kapı (araç-rol tablosu aşağıda).** Aday
   revizyonu bir önizleme parçasına yazıp **sci-audit (HARD)** koştur; **galileo**'yu
   doğrudan aday metin üzerinde koştur. Denetimi render/onay sonrasına **ERTELEME** —
   kapı onaydan öncedir. Herhangi HARD bulgu = düzelt-ve-tekrar; onaya çıkma.
6. **Onaya sun.** Sun: (a) diff (eski → yeni), (b) kapı özeti (HARD / SOFT-block /
   advisory bulguları + galileo skorları), (c) aday atıflar + kapı durumu. **Açık kullanıcı
   onayı olmadan Edit/commit yok.** Onay sonrası: Edit uygula → kapanışta
   `/sci-audit:audit chapters/<bolum>.qmd --lang tr` + bölüm kapanıyorsa `/tez-dogrulama`.

## Denetim araç-rol tablosu (araçları KARIŞTIRMA)

| Kademe | Araç | Rol |
|---|---|---|
| **HARD** | `/sci-audit:check-turkish … --strictness certification` | Axis G: Türkçe imla + ondalık-virgül (nokta-`p` = blocker) |
| **HARD** | `/sci-audit:verify-citations` · `/sci-audit:check-stats` | Axis A referans bütünlüğü · Axis C istatistik tutarlılığı |
| **SOFT-block** | `galileo_judge` (`text`, `section_type`, `evidence`) | Revize **metnin** faithfulness / groundedness / citation_support / marmara / hallucination |
| **SOFT-block** | `galileo_claim_source_match` (`claim`, `source_text`) | Her güçlendirilen/yeni **iddia ↔ kaynağı** temellendirme skoru |
| **advisory** | `galileo_coherence` · `galileo_reference_prose` | Paragraf akışı/tekrar · atıf yoğunluğu + reporting-verb monotonluğu |

Kademe anlamı (eşikler `.claude/galileo.local.md`): **HARD** değişmez, override yok; **SOFT-block**
`certified-final`'ı durdurur, insan-override'lı (groundedness/faithfulness < 0,60; nicel iddia
`citation_support=unsupported`); **advisory** bloklamaz. Doktrin:
`.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md` §6.

## Devir (scope guard)
- Yeni referans yerleştirme → `/referans-kapisi` · Derin literatür sentezi → `/tez-literatur`
- Bölüm finalizasyonu → `/bolum-sertifika` · Sistematik derleme → `/evidentia:evidentia`

## Bağlayıcı (çiğnenmez)
- **Kanıt bölgesi DOKUNULMAZ:** sayı/istatistik ve bulgunun içeriği/yönü/anlamlılığı/büyüklüğü/
  sırası **aynen** kalır; yeniden-yorum, yuvarlama, güçlendirme yok; kaynakta olmayan özgüllük
  (informant, "klinik açıdan anlamlı", "sağlam/dayanıklı", nedensellik) **eklenmez.** Odak:
  anlatım etkinliği + referans doğruluk/kapsam/tutarlılığı — **çalışmanın bulguları değişmez.**
- **Kırmızı bayraklar (bulgu mutasyonu → çıkar):** kaynakta olmayan aktör ekleme (ör. "anneden");
  g/β'ye "klinik/ihmal edilemez/güçlü" atfetme; kaynakta olmayan etki-büyüklüğü etiketi
  ("küçük/orta/güçlü") ekleme (metrik TANIMI izah edilebilir, ama BU sonucun büyüklüğü kaynakta
  yoksa etiketlenmez); "anlamlı değildi" → "eğilim/kısmen" yumuşatma; korelasyonu "neden" yapma;
  bulgu cümlelerini birleştirme veya sırasını değiştirme.
- **Kaynak-iddia sadakati:** referans, makalenin **bütünsel/semantik** kavranışına dayanır
  (parça-alıntı çarpıtması yok); ne kaynağın ne tez metninin somut bilimsel iddiası
  düzleştirilir/abartılır/çarpıtılır — kaynak kendi **kapsam + koşuluyla** (ör. "diyabette daha
  zayıf", "çocuk-bildiriminde tutarsız") aktarılır; uyumsuz kanıt "uyumlu"ya çevrilmez.
  **(Konstitüsyonel: Referans Bütünlük Şiarı — `talimatname-claude-code.md` §4.1.)**
- **Dosyaya doğrudan yazmadan önce onaya sun; denetimi onaydan sonraya erteleme.**
- **Uydurma referans/sayı yok** — sayılar artefakttan, atıflar `/referans-kapisi`'ndan.
- **sci-audit (HARD) atlanamaz;** `tez_checklist_verify` onun YERİNE, `galileo` da sci-audit'in yerine geçmez — üçü ayrı kademedir.
- **`[@key]`/`@tbl-*` token, ondalık virgül ve başlık yapısı aynen korunur.**
- **KVKK:** dış gateway'e yalnız literatür terimi.
