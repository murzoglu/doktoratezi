# 02_sablonlar — Şablon (İskelet) Katmanı

Bu klasör tez yazımının **şablon katmanı**dır: `chapters/*.qmd` üretimine ve ön
bölüm hazırlığına girmeden önce doldurulacak **iskeletler**. Tek-otorite ilkesi
geçerlidir (bkz. `00_kaynak-kurallari/README.md`).

> **Temel kural:** Şablonlar **biçim kuralı tanımlamaz**. Her biçim/kural kararının
> tek kanonik yeri `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md`'dir.
> Bu klasördeki dosyalar yalnız **yapı (fill-in) + operasyonel kontrol
> hatırlatıcısı** taşır; bir kural çakışırsa kanonik talimatname esastır.

## Tek-Otorite Haritası

| Dosya | Ne için iskelet | Yöneten kanonik kural |
|---|---|---|
| `bolum-sablonu.md` | `chapters/*.qmd` bölüm hazırlığı (kimlik, kanıt haritası, gövde, kontrol). | marmara §5 (bölüm sırası), §3 (bölüm içerik), §1.3 (başlık), §1.4 (sayısal), §12 (checklist). |
| `on-bolumler-sablonu.md` | Kapak, beyan, teşekkür, içindekiler, listeler. | marmara §2 (§2.1–2.7) + resmi `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx`. |
| `ozet-summary-sablonu.md` | ÖZET + SUMMARY doldurulabilir alanları. | marmara §3.2 (özet/summary), §12 (checklist). |
| `tablo-sekil-sablonlari.md` | Tablo/şekil başlık ve dipnot iskeleti. | marmara §1.7 (tablolar), §1.6 (şekiller), §8 + §1.4 (istatistik/sayısal). |

## Şablon çıktısının gittiği yer (bağlı omurga)

| İskelet bölümü | Doldurulmuş hâlinin kanonik yeri | Katman |
|---|---|---|
| `bolum-sablonu.md` → "Kanıt Haritası" | `02_kanit-haritalari/<bölüm>-kanit-haritasi.md` | 02 |
| `bolum-sablonu.md` → bölüm planı | `03_bolum-hazirlik/<bölüm>.md` briefi | 03 |
| Tüm şablonlar → nihai metin | `chapters/*.qmd` + `thesis.qmd` | üretim |
| Tüm "Kontrol" listeleri | marmara §12 (kanonik format checklist) + `04_kalite-kontrol/format-kontrol-listesi.md` | 00/04 |

## Öncelik zinciri

Çakışmada: (1) kullanıcı/danışman açık talimatı → (2) resmi `docs/tez-kilavuz/`
(PDF + DOCX) → (3) `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md`
kanonik kural → (4) bu klasördeki iskelet. Bir şablonun kontrol maddesi kanonik
kuraldan sapıyorsa kanonik kural esastır ve şablon güncellenir.

## Duplikasyon önleme kuralı

Şablonlara **kural metni** eklenmez; yalnız doldurulacak alan + kanonik §'ye
işaret eden kontrol hatırlatıcısı eklenir. Yeni bir biçim kuralı önce
`marmara-tez-formati-talimatnamesi.md`'ye yazılır; şablon en fazla ona pointer
verir (bkz. 2026-07-06 rafinasyonu: dört şablona "Kanonik kural otoritesi"
başlığı eklendi, kural tanımı tek otoriteye — marmara talimatnamesi — bırakıldı).
