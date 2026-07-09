# KAYNAKLAR ve EKLER — Kapsamlı Bölüm Talimatnamesi

> **Kanonik kural otoritesi:** Kaynakça biçimi (AMA-11 özel format, alfabetik,
> italik/kalın yok, 0,5 cm asılı, 6 nk, >6 yazar "et al./ve ark.", dergi
> kısaltması, künye örnekleri) → `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md`
> §4 (§4.1–4.3); **tez kaynak olamaz + web ≤%5 yalnız .gov/.int/.eu** → §4.2;
> Özgeçmiş → §3.8; Bilimsel Faaliyetler → §3.9; Ekler (Ek 1, Ek 2… ayrı
> sayfa, etik onayı) → §3.10. Bu talimatname kural tanımlamaz. Klasör haritası:
> `03_bolum-hazirlik/README.md`.

## 1. Bölüm İşlevi

Bu talimatname resmi sıradaki **KAYNAKLAR (15)**, **ÖZGEÇMİŞ (16)**, **BİLİMSEL
FAALİYETLER (17)** ve **EKLER (18)** bloklarının hazırlığını kapsar (marmara §5
sıra). Kaynakça, tez boyunca `referans-denetim-ledgeri.md` üzerinden kapısı
kapatılmış künyelerin **Enstitü AMA-11 çıktısı**dır; Ekler, metinde anılma
sırasına göre düzenlenmiş resmi belgelerdir.

## 2. Kaynaklar — üretim hattı

Kaynakça **yazılmaz, türetilir**: `references/references.bib` + Zotero `T1DM
Thesis` collection → Enstitü CSL/stil dosyası → AMA-11 çıktısı. Hiçbir künye
**referans kapısı kapanmadan** (`talimatname-claude-code.md` §4;
`02_kanit-haritalari/referans-denetim-ledgeri.md` durumu `cite-ok`) kaynakçaya
girmez.

Bağlayıcı kurallar (tam metin marmara §4.1–4.2, burada tekrar edilmez, kapı
olarak listelenir):

- Yazar soyadına göre **alfabetik**; italik/kalın yok; 0,5 cm asılı; kaynaklar
  arası 6 nk; **1 satır aralığı**.
- Künye düzeni: `Yazar. Başlık. Dergi. Cilt;(Sayı):Sayfa. doi` (tip istisnaları
  §4.3). >6 yazar → ilk 6 + `et al.`/`ve ark.`; dergi adı **kısaltılmış**.
- **Tez (lisans/YL/doktora) kaynak olarak KULLANILMAZ** (§4.2). YÖK tezleri
  yalnız hazırlık/ledger'da yerel literatür izi olarak tutulur; final kaynakçada
  hakemli dergi karşılığıyla değiştirilir (bkz. GİRİŞ §3.8.2 uyum notu).
- **Web:** yalnız `.gov/.int/.eu`; toplam **≤ %5**; `.com/.net` kaynak değildir.
- Bildiri: yalnız son 3 yıl + dergide genişletilmiş özet (Proceedings).

Kontrol:

- [ ] Alfabetik; italik/kalın yok; asılı girinti + 6 nk.
- [ ] >6 yazarda ilk 6 + `et al.`/`ve ark.`; dergi kısaltması.
- [ ] Web ≤ %5 ve yalnız `.gov/.int/.eu`.
- [ ] **Tez kaynağı yok** (§4.2).
- [ ] Her künye ledger `cite-ok` + Zotero item/BibTeX + `references.bib` mutabık.
- [ ] Metin içi atıf ile kaynakça bire bir örtüşüyor (eksik/fazla künye yok).

## 3. Özgeçmiş (madde 16, marmara §3.8)

Öğrencinin kısa özgeçmişi, şablon formatında, **tek sayfa**. PII/kişisel iletişim
detayı gizlilik sınırına dikkat edilerek yalnız şablonun istediği alanlarla
sınırlı tutulur.

## 4. Bilimsel Faaliyetler (madde 17, marmara §3.9)

Kayıt tarihinden itibaren proje/toplantı/patent/makale vb., **kaynak yazımı
formatında**. Mezuniyet koşulu sağlayan yayın/sunumların tam dokümanları **teze
eklenmez**, ayrı portfolyo olarak Enstitüye teslim edilir. Dergide basılmayan
bildiriler için şablon örnek biçimi kullanılır.

## 5. Ekler (madde 18, marmara §3.10)

Ekler metinde **anılma sırasına** göre `Ek 1`, `Ek 2`, `Ek 3`… biçiminde, her
biri **ayrı sayfada**. Metinden eke atıf yapılır.

Olası ekler (bu tez için):

| Ek | İçerik | Kaynak/sınır |
|---|---|---|
| Etik kurul onayı | Tarih/sayı GEREÇ ve YÖNTEM ile bire bir tutarlı belge. | `06_kritik-kaynaklar` etik kaynağı; imzalı metin PII taşımaz. |
| Veri toplama araçları | EMBU-P/C, Beck, KİA/SRQ, demografik-tıbbi form. | Ölçek telif sınırı; kullanım izni. |
| Ek tablo/şekiller | Metne sığmayan aggregate tablolar. | `outputs/tables`; satır verisi yok. |
| COREQ / SRQR / JARS-Qual özetleri | Nitel raporlama uyum tabloları. | Nitel repo türetilmiş çıktı. |
| LLM kullanım beyanı | AI/LLM kullanımının şeffaf beyanı (sci-audit axis F ile uyumlu). | `03_analysis/methodology/llm_use_statement` (nitel repo türevleri). |
| Codebook / audit trail özeti | De-identified kod-tema haritası, karar izi. | Ham veri yok. |
| Bilimsel faaliyet portfolyo yönlendirmesi | Teze eklenmeyen belgelerin nereye teslim edildiği notu. | — |

Kontrol:

- [ ] Ekler metinde anılma sırasında; her biri ayrı sayfa; `Ek N` biçimi.
- [ ] Etik onay Ekler'de; tarih/sayı yöntem bölümüyle tutarlı.
- [ ] Hiçbir ekte satır düzeyi veri, ham transcript, imzalı onam PII'si yok.
- [ ] Nitel ekler de-identified; anonim/quote-ID düzeyi.

## 6. Anti-pattern'ler (bu blokta yapma)

- Tez künyesini kaynakçada bırakmak (§4.2 ihlali).
- `.com/.net` web kaynağı veya %5'i aşan web atfı.
- Metin içi atıf ↔ kaynakça uyuşmazlığı (hayalet/eksik künye).
- Ekleri anılma sırası dışında dizmek; etik belgeyi metne gömüp Ekler'e koymamak.
- Mezuniyet yayın dokümanlarını teze eklemek (portfolyo olarak teslim edilir).
- Kaynakçaya ledger `cite-ok` olmayan künye sokmak.

## 7. Kapanış kapıları

- [ ] Kaynakça AMA-11 (§4) + tez-kaynak yok + web ≤%5; alfabetik/asılı/6 nk.
- [ ] Her künye ledger `cite-ok`; metin içi atıfla bire bir örtüşüyor.
- [ ] Özgeçmiş tek sayfa; Bilimsel Faaliyetler kaynak biçiminde; portfolyo teze
      eklenmedi.
- [ ] Ekler sırası/ayrı sayfa; etik onay Ekler'de; PII/ham veri yok.
- [ ] `sci-audit` axis A (referans bütünlüğü — DOI/PMID/retraction) + axis F
      (AI-şeffaflık/LLM beyanı) blocker'sız.
- [ ] Format §12 + Kapı 0–5 sertifikasyonu + açık onay.
