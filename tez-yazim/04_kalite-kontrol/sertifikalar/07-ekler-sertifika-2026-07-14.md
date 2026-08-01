# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 07 — EKLER |
| Dosya | `chapters/07_ekler.qmd` |
| Sertifika tarihi | 2026-07-14 |
| Strictness | `certification` |
| Uygulama onayı | Kullanıcı (repo sahibi) açık direktifi: `spec.md` eksikliklerini sırayla gider |

## Kapsam (bu tur)

`spec.md` R5 gereksinimi. İki `[YER TUTUCU]` işaretinin (Ek 2 etik kurul onayı,
Ek 3 ölçek izinleri/formları) belirsiz biçimden açıklayıcı, standart
"taranmış belge eklenecek" işaretine çevrilmesi. İçerik yazımı gerektirmeyen
fiziksel belge yerleri; yalnız işaretlemenin netliği hedeflendi.

## Uygulanan değişiklikler

- **Ek 2 (Etik Kurul Onayı):** `[YER TUTUCU — teslim öncesi eklenecek belge]` →
  `[TARANMIŞ BELGE EKLENECEK]` + belge künyesi (etik kurul tarih/sayı, kurum izni)
  korundu + "fiziksel belge teslim öncesi eklenecek; metin yazımı gerektirmez" notu.
- **Ek 3 (Ölçek İzinleri/Formlar):** `[YER TUTUCU — teslim öncesi eklenecek belgeler]` →
  `[TARANMIŞ BELGELER EKLENECEK]` + üç alt-ek (3a s-EMBU, 3b Beck, 3c KİA) net
  listelendi + aynı standart not.

Ek 1 (keşifsel genişletme) içeriği bu turda değiştirilmedi; yalnız yer-tutucu
işaretleri düzeltildi. Dosyada kalan `{...}` ifadeleri Quarto attribute söz-dizimidir
(başlık/şekil), doldurulmamış alan değildir.

## Kapı sonuçları (0-5) — tümü PASS

| Kapı | Kanıt | Sonuç |
|---|---|---|
| 0 | Kapsam/gizlilik: yalnız yer-tutucu işaret metni; ham veri/credential yok | ✅ PASS |
| 1 | Yeni bilimsel iddia yok; Ek 1 keşifsel bulgular değişmedi | ✅ PASS |
| 2 | Dış citation eklenmedi/değişmedi (`@pinquart2013`, `@lovejoy2000maternal`, `@kennyKashyCook2006` korundu); `bib_hygiene.py` HARD=0 | ✅ PASS |
| 3 | Marmara §3.5/§3.10 ek yapısı korundu; yer-tutucu artık açıklayıcı standart biçimde | ✅ PASS |
| 4 | Türkçe akış korundu | ✅ PASS |
| 5 | `quarto render thesis.qmd` **exit 0**; 0 çözümsüz crossref; Ek şekilleri (F2-*) etkilenmedi | ✅ PASS |

## Karar

Kapı 0–5 tümü PASS; belirsiz `[YER TUTUCU]` işaretleri açıklayıcı standart biçime
çevrildi; içerik iddiası değişmedi; render exit 0. Statü **`certified-final`**.
