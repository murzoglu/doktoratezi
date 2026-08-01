# Niteliksel Raporlama Standartları — COREQ / SRQR / JARS-Qual

> **Amaç:** Niteliksel bulguların raporlanmasında standart-uyumu. Hangi madde nerede kapanır,
> refleksivite nasıl raporlanır, alıntı bütünlüğü nasıl korunur. Kaynak zemin: kanonik rapor §11 +
> `03_analysis/methodology/coreq_32_completed.md`.

## 0. Hangi Standart Ne Zaman?

| Standart | Kapsam | Bu koldaki rol |
|---|---|---|
| **COREQ** (Tong 2007) | Görüşme/odak grup çalışmaları, 32 madde, 3 domain | **Birincil** — tam kapatılır |
| **SRQR** (O'Brien 2014) | Tüm niteliksel tasarımlar, 21 madde | Ek denetim (COREQ'i tamamlar) |
| **JARS-Qual** (Levitt 2018, APA) | APA dergileri niteliksel raporlama | Karma tez/yayın için ek denetim |
| **GRAMMS** (O'Cathain 2008) | Karma yöntem raporlama | `karma-yontem.md`'de (nicel skill) |

Denetim komutu: `/sci-audit:guideline-check --type coreq` (ve karma bölüm için `--type jars`).

## 1. COREQ 32-Madde Durumu (kanonik)

| Domain | Tam | Kısmi | Eksik | Toplam |
|---|---:|---:|---:|---:|
| 1. Araştırma ekibi ve refleksivite | 7 | 0 | 0 | 7 |
| 2. Çalışma tasarımı | 14 | 1 | 0 | 15 |
| 3. Analiz ve bulgular | 9 | 1 | 0 | 10 |
| **Toplam** | **30** | **2** | **0** | **32** |

### Domain 1 — Araştırma ekibi ve refleksivite (Madde 1-8)
Kimlik/kimlik bilgisi, deneyim/eğitim, cinsiyet, araştırmacı-katılımcı ilişkisi. Bu kolda OM
(birinci araştırmacı/kodlayıcı) + BA (non-participant observer/critical friend). Detay:
`gorusme-etik-kvkk.md` (positionality).

### Domain 2 — Çalışma tasarımı (Madde 9-23)
Kuramsal çerçeve, katılımcı seçimi, ortam, veri toplama. **Kısmi: Madde 16 (pilot görüşme).**

### Domain 3 — Analiz ve bulgular (Madde 24-32)
Kodlama, tema türetme, yazılım, katılımcı geri-bildirimi, alıntı sunumu. **Kısmi: Madde 31
(negatif vaka).**

## 2. İki Kısmi Maddenin Kapatılması

**Madde 16 (pilot görüşme):** görüşme rehberi pilotlandıysa rapora eklenir; pilotlanmadıysa yöntem
ve sınırlılıklarda **açıkça** belirtilir. Açık bırakılmaz — bir yönde net karar yazılır.

**Madde 31 (negatif vaka):** her makro tema için en az bir **farklı tezahür / sınırlayıcı örnek**
paragrafı eklenir (bkz. `rta-ve-analiz.md §5`). Ön-tarama Tema 4 için yapılmıştır; **tüm temalara
yayılmalıdır.** Bu, COREQ 31'i kısmiden tama çevirir.

## 3. Refleksivite / Positionality Raporlama

COREQ Domain 1 + JARS-Qual "researcher description" için: araştırmacının mesleki konumu, veriyle
ilişkisi, potansiyel önyargı kaynakları ve yönetim stratejileri **bulgular bölümünde** raporlanır
(dipnotta gizlenmez). Refleksif riskler ve yönetim tablosu için kanonik rapor §3.4.

## 4. Alıntı Bütünlüğü (quote integrity)

Tez metnine konacak her doğrudan alıntı, kaynak (temizlenmiş tez) metniyle **bire bir** eşleşmeli;
role + aile kodu eklenmeli. Bu skill/`.qmd` **verbatim alıntı üretmez** — yalnız `quote_id` verir.

**İzin verilen müdahaleler:** kimlik maskeleme (`[isim]`, `[okul adı]`, `[şehir]`); kısaltma
(`[...]`); köşeli parantezde sınırlı bağlam açıklaması.

**Yasak:** alıntının akademikleştirilmesi; "dilbilgisi düzeltme" adıyla yeniden yazma; özet metni
alıntı gibi sunma; alıntıdan tema üretimini kesin hüküm gibi sunma.

## 5. Bulgular Bölümü Yapısı (kanonik `.qmd` için)

```
## Niteliksel Kol Bulguları
### Niteliksel Örneklem ve Analitik Çerçeve
### Tema 1. Sağlıklı Kardeşin Görünmeyen Yükü
### Tema 2. Annenin Tıbbi Bakıcı Rolüne Kayması
### Tema 3. T1DM Tanılı Çocuğun İçeriden Deneyimi
### Tema 4. Aynı Evde Üç Farklı Deneyim
### Karma Bulgulara Köprü
```

Her tema: ana sonuç → alt tema sonuçları (tablo) → bilimsel yorum → kod + `quote_id` ankraj →
negatif vaka/farklı tezahür paragrafı.

## 6. Raporlama Dil Disiplini
- Türkçe edilgen 3. tekil; ondalık virgül + baştan sıfır (Türkçe metin).
- Genelleme/nedensellik dili yok ("gösterir/düşündürür/bağlamsallaştırır" evet; "kanıtlar/neden
  olur" hayır).
- `[@key]` metin-içi atıf → tek `references.bib`; CSL (`marmara-ama11.csl`) render eder.

## Çapraz referanslar
- Analiz/yorum → `rta-ve-analiz.md` · Değerlendirme → `gecerlik-ve-degerlendirme.md`
- Etik/refleksivite → `gorusme-etik-kvkk.md` · Denetim → `manuskript-denetimi-sciaudit.md`
- Kaynaklar: Tong, Sainsbury & Craig (2007); O'Brien et al. (2014); Levitt et al. (2018)
