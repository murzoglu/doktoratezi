# Negatif / Farklı Vaka İnceleme Planı

AI destekli çıktılar yalnızca yardımcı, ön-denetim veya tutarlılık kontrolü olarak değerlendirilir. Kodlama, tema geliştirme ve yorumlama kararları araştırmacı sorumluluğundadır.

## Durum

`dmnitel find-negative-cases` komutunun doğrudan çalışması için gerekli yapılandırılmış `coded_segments.csv` dosyası depoda henüz doldurulmuş halde bulunamadı. Bu turda güvenli başlık şablonu `01_deidentified/coded_segments_template.csv` olarak eklendi. Mevcut durumda negatif/farklı vaka incelemesi, `codebook_v3.csv`, `codebook_v3.md`, temizlenmiş tez bulguları ve triadik matris DOCX dosyaları üzerinden araştırmacı denetimli olarak yürütülmelidir.

Bu rapor nihai yorum üretmez; yalnızca Faz B bulgular yazımı sırasında kontrol edilecek gerilim alanlarını listeler.

## Tema Bazlı Kontrol Alanları

| Tez teması | Kontrol edilmesi gereken gerilim | Öncelikli kodlar | Araştırmacı kararı |
|---|---|---|---|
| T1 — Gölgedeki çocuklar | Sağlıklı kardeş yük/fedakarlık anlatırken anne veya hasta çocuk bunu bakım, yakınlaşma ya da normal aile desteği olarak çerçeveliyor mu? | `KARDES_GORUNMEZ_YUK`; `KARDES_ILISKISI`; `OFKE_ADALETSIZLIK`; `AILE_ICI_ADALET` | Her alt temada en az bir farklı tezahür veya sınırlayıcı örnek aranmalıdır. |
| T2 — Annelikte eksen kayması | Anne tıbbi bakıcı rolünü zorunlu ve koruyucu anlatırken, çocuk/kardeş bunu kontrol, kısıtlanma veya görünmeme olarak deneyimliyor mu? | `ANNE_HIPERVIJILANS`; `RUTIN_TAKIP`; `KAYGI_KIRILGANLIK`; `ILETISIM_CATISMA` | Koruyucu bakım ile aşırı kontrol ayrımı araştırmacı notuyla gerekçelendirilmelidir. |
| T3 — Hastalığın içinden | Hasta çocuk “normalleşme” veya etkilenmeme dili kurarken aynı ailede anne/kardeş yoğun kaygı, kısıtlılık veya yük anlatıyor mu? | `KABULLENME_NORMALLESME`; `COCUK_OZERKLIK_OZBAKIM`; `OKUL_SOSYAL_UYUM`; `KAYGI_KIRILGANLIK` | Normalleşme dili yükün yokluğu gibi sunulmamalı; olası duygu düzenleme stratejisi olarak dikkatle yazılmalıdır. |
| T4 — Triadik karşılaştırma | Aynı olay anne, hasta çocuk ve sağlıklı kardeş tarafından farklı anlamlandırılıyor mu; üç rolün biri görünmez kalıyor mu? | `BESLENME_KONTROL`; `AILE_ICI_ADALET`; `KARDES_ILISKISI`; `KARDES_GORUNMEZ_YUK` | Uyum, ayrışma ve kör alanlar ayrı ayrı işaretlenmelidir. |

## Özel Kontrol Noktaları

- Aile 201 düşük odak-aile temsili nedeniyle yalnızca sınırlılık olarak değil, farklı/yoğun vaka olasılığı açısından da kontrol edilmelidir.
- `J2.1`, `J2.2`, `J3.3`, `J5.4` için odak aile atamaları triadik matris DOCX başlıklarından doğrulanmıştır: `J2.1=Aile 14`, `J2.2=Aile 11`, `J3.3=Aile 11`, `J5.4=Aile 202`.
- `KARDES_KORUYUCU_ROLU` ayrı kod olarak açılacaksa, `KARDES_GORUNMEZ_YUK` ile sınırı netleştirilmelidir.
- `AILE_ICI_ADALET` yazımı v3 codebook içinde `AILE_ICI_ADALET` olarak düzeltilmiştir. DOCX/XLSX/ODS taramasında eski ID saptanmamıştır; kalan eski yazımlar v1/v2/audit gibi tarihsel metinlerde açıklayıcı kayıt niteliğindedir.

## Coded Segments CSV Gereksinimi

Otomatik ön-denetim için aşağıdaki alanlara sahip anonimleştirilmiş bir CSV gerekir:

| Alan | Açıklama |
|---|---|
| `family_id` | Aile kodu |
| `participant_role` | `mother`, `t1dm_child`, `healthy_sibling` |
| `participant_id` | Anonim katılımcı kodu |
| `theme` | Tez veya journal tema etiketi |
| `subtheme` | Alt tema etiketi |
| `code_name` | Codebook v3 kod adı |
| `quote_id` | Alıntı bütünlüğü için benzersiz ID |
| `quote_text` | Anonimleştirilmiş kaynak alıntı |
| `field_note` | Varsa saha notu |
| `memo` | Araştırmacı notu |

Bu CSV oluşturulduktan sonra örnek komut:

```bash
./dmnitel find-negative-cases --coded-data 01_deidentified/coded_segments.csv --theme "T4 — Triadik karşılaştırma"
```

Alıntı bütünlüğü denetimi için ayrıca `06_manuscript_outputs/quotes_used_template.csv` şablonu eklenmiştir.

## Araştırmacı Kararı İçin Not

Negatif veya farklı vaka, temayı yanlışlayan otomatik bir karar olarak değil; temanın sınırlarını, çeşitliliğini ve hangi aile/rol konumlarında farklılaştığını görünür kılan analitik denetim olarak kullanılmalıdır.
