# TUTARSIZLIK WORKLIST — Final'de DÜZELTİLMEMİŞ (Persist Eden) Kayıtlar

> ✅ **DURUM: UYGULANDI (2026-07-08).** Aşağıdaki 11 ailenin tamamı PI form-teyitli değerlerle
> düzeltildi; kanonik kilit rev 2 olarak yenilendi (38 hücre); düzeltme sonrası tutarsızlık **0**;
> tam pipeline yeniden koşuldu. Uygulanan değerler: B1 dm_tani → 2000=01.12.2012, 1007=01.08.2020,
> 1003=03.03.2014, 2004=02.02.2017, 2025=01.03.2017; B8 oda → 2001=2, 64=2; B2 cocuk_sayisi →
> 1003=2, 1219=2; F2 sıra → 403-3=1, 904-4=2, 1216-4=2; B7 es_dogum 1011=25.03.1980 (supplement,
> es_yas=42,98). İz: `CORRECTIONS__pi_verified_ledger.csv`, sapma tablosu #3, lock rev 2.

**Tarih:** 2026-07-08 · **Kapsam:** Yalnız **kilitli kanonik final'de HÂLÂ mevcut** tutarsızlıklar.
Kaynak `Birleşik Veri...NİHAİ.csv` ile final `cocuk_no` üzerinden karşılaştırıldı (persistence
cross-check, `persist.R`, bu tur).
**Kapsam-dışı (kasıtlı):** Kaynakta hatalı ama final derivation'da **zaten düzeltilmiş** 19 aile
(anne_yas kaynak≠final: 3, 12, 22, 33, 83, 303, 400, 901, 1001, 1007, 1101, 1105, 1110, 1218,
2027, 2030, 2034, 2304, 2306). Örn. 1001 kaynak çocuk_yaş −4,8/−12,1 → final 15,2/7,9; 12-2
1,5→11,5; 2306-2 3,0→13,0. **Final bunlarda temiz; yalnız `NİHAİ.csv` bayat.**
> ⚠️ **Provenans-boşluğu (ayrı sorun):** `NİHAİ.csv` kilitli final'in tam girdisi DEĞİL — 19 ailede
> belgelenmemiş tarih-düzeltmesi var. Bu kaynaktan yeniden türetme, düzeltmeleri KAYBEDER. Düzeltme
> günlüğü/düzeltilmiş kaynak PI'da ayrıca aranmalı (reprodüktivite).

---

## 1. PERSİST EDEN TUTARSIZLIKLAR (final'de mevcut)

| # | cocuk_no / aile | Alan | Final değeri (hatalı) | Doğru değer | Sınıf |
|---|---|---|---|---|---|
| **B1.1** | 2000-1 | dm_yili vs cocuk_yas | dm_yili=14,25 > yaş=10,93 (tanı doğumdan **1211 gün önce**) | bilinmiyor | kaynak tarih hatası |
Doğru Tarih 01.12.2012

| **B1.2** | 1007-1 | dm_yili vs cocuk_yas | dm_yili=7,98 > yaş=7,26 (627 gün) | bilinmiyor | kaynak tarih hatası |
Doğru Tarih 01.08.2020

| **B1.3** | 1003-1 | dm_yili vs cocuk_yas | dm_yili=13,25 > yaş=11,87 (501 gün) | bilinmiyor | kaynak tarih hatası |
Doğru Tarih 03.03.2014

| **B1.4** | 2004-1 | dm_yili vs cocuk_yas | dm_yili=8,11 > yaş=7,40 (260 gün) | bilinmiyor | kaynak tarih hatası |
Doğru Tarih 02.02.2017

| **B1.5** | 2025-1 | dm_yili vs cocuk_yas | dm_yili=8,44 > yaş=8,42 (6 gün) | bilinmiyor (sınır) | kaynak tarih hatası |
Doğru Tarih 01.03.2017

| **B8.1** | aile 2001 (2001-1,-2) | ev_oda_sayisi | **0** (imkansız: 0 odalı hane) | bilinmiyor (muhtemel: eksik) | geçersiz/eksik-kod |
Ev Oda Sayısı Kod 2

| **B8.2** | aile 64 (64-1,-2) | ev_oda_sayisi | **0** | bilinmiyor | geçersiz/eksik-kod |
Ev Oda Sayısı Kod 2

| **B2.1** | aile 1003 (1003-1,-2) | cocuk_sayisi | **1** ama 2 katılımcı çocuk | ≥2 (belirsiz) | eksik-kayıt |
2 çocuk var, doğum tarihlerine uygun biçimde sıraları düzenle

| **B2.2** | aile 1219 (1219-3,-4) | cocuk_sayisi | **1** ama 2 katılımcı çocuk | ≥2 (belirsiz) | eksik-kayıt |
2 çocuk var, doğum tarihlerine uygun biçimde sıraları düzenle

| **F2.1** | aile 403 (403-3,-4) | doğum sırası | iki kardeş de sıra=2 (farklı yaş) | biri yanlış | eksik-kayıt |
403-3 1 olacak

| **F2.2** | aile 904 (904-3,-4) | doğum sırası | iki kardeş de sıra=1 | biri yanlış | eksik-kayıt |
904-4 2 olacak

| **F2.3** | aile 1216 (1216-3,-4) | doğum sırası | iki kardeş de sıra=1 | biri yanlış | eksik-kayıt |
1216-4 2 olacak

| **B7** | aile 1011 (1011-1,-2) | es_yas (supplement) | **13** (imkansız baba yaşı) | bilinmiyor | kaynak Eş Doğum hatası |
eş doğum tarihi 25.03.1980

*F2 notu:* Kaynakta 7 aile aynı-sıra taşır; 4'ü ikiz/aynı-yaş (**meşru**: 1101, 2306, 2315, 405);
yalnız yukarıdaki **3'ü farklı-yaş (hata)**. B7 yalnız kurtarma supplement'ini etkiler (es_dogum
final'de yok).

---

## 2. ANALİTİK ETKİ — hangisi nereye ulaşıyor?

| Tutarsızlık | Etkilediği yüzey | Confirmatory'ye ulaşır mı? |
|---|---|---|
| **B8 oda=0** (2 aile) | `material_index`→`ses_latent` (R/11) → propensity + kovaryat | **EVET, dolaylı** (SES kompoziti H1–H5'e girer) — en geniş erişim |
| **B2 cocuk_sayisi=1** (2) | `cocuk_sayisi_z` kovaryat (H1/H3) + sibship (§108) | **EVET, kovaryat** (2/241, yön değiştirmez) |
| **B1 dm_yili** (5) | R/27 (§12.5), R/40 (§12.5.1 HbA1c) **maskesiz**; R/55 maskeli | Hayır (DM-klinik keşifsel) |
| **F2 sıra** (3) | Faz III §108 doğum sırası/sibship | Hayır (keşifsel) |
| **B7 es_yas=13** (1) | yalnız SUPPLEMENT / Faz IV §125 | Hayır (supplement) |

**Özet:** En "ulaşan" ikisi **B8 (oda=0→SES)** ve **B2 (cocuk_sayisi→kovaryat)** — confirmatory'ye
SES/kovaryat üzerinden dolaylı, 2'şer aile, yön-değiştirmez ama temizlenmeli. B1/F2/B7 keşifsel/
supplement kalır.

---

## 3. GİDERME — item bazında (kilit-farkında)

| # | Güvenle düzeltilebilir mi? | Önerilen aksiyon |
|---|---|---|
| **B8 oda=0** | ✅ **EVET** — 0 oda imkansız = eksik | `ev_oda_sayisi: 0 → NA` recode (savunulabilir); `material_index` yeniden türet (R/11). |
| **B7 es_yas=13** | ✅ **EVET** (supplement) | Supplement'te `es_yas<16 → NA` plausibilite-maskesi. |
| **B1 dm_yili** (5) | ❌ doğru tarih bilinmiyor | Maske (R/55 kuralını R/27+R/40'a genişlet) **veya** PI form-teyidi ile doğru tarih. |
| **B2 cocuk_sayisi** (2) | ⚠️ "1" yanlış, gerçek ≥2 belirsiz | `1 → NA` recode **veya** PI form-teyidi (gerçek toplam). |
| **F2 sıra** (3) | ❌ doğru sıra bilinmiyor | Maske (§108 dışla) **veya** PI form-teyidi (Çocuk No eki −3/−4 ipucu, teyitsiz). |

**Uydurma yasağı:** B1/B2/F2 için değer üretilmez; ya recode-to-NA (bilgi-koruyucu, savunulabilir)
ya PI form-teyidi. B8/B7 recode-to-NA güvenli (imkansız değer = eksik).

**Kilit etkisi:** B8 recode'u `material_index`→`ses_latent`'i değiştirir → SES kovaryatı kullanan
modeller (propensity dâhil) yeniden koşmalı. Bu, kanonik-değiştiren adımdır; C-hibrit gereği
maske-katmanı (kilit dokunmadan) veya kontrollü re-derive+re-lock kararı gerektirir.
