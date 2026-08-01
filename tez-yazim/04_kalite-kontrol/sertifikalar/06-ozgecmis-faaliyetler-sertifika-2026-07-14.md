# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 06 — ÖZGEÇMİŞ ve BİLİMSEL FAALİYETLER |
| Dosya | `chapters/06_ozgecmis_faaliyetler.qmd` |
| Sertifika tarihi | 2026-07-14 |
| Strictness | `certification` |
| Uygulama onayı | Kullanıcı (repo sahibi) açık direktifi: `docs/superpowers/specs/2026-08-01-tez-kontrol-checklisti-tasarimi.md` eksikliklerini sırayla gider |

## Kapsam (bu tur)

`docs/superpowers/specs/2026-08-01-tez-kontrol-checklisti-tasarimi.md` R4 gereksinimi. Özgeçmiş ve bilimsel faaliyet alanlarının kullanıcı
tarafından sağlanan resmi özgeçmiş (CV) belgesindeki doğrulanabilir verilerle
doldurulması. CV'de bulunmayan kişisel alanlar (doğum yeri/tarihi) Marmara §3.8
biçiminde işaretli yer tutucu olarak korundu — sahte veri eklenmedi.

## Kaynak

Kullanıcı tarafından sağlanan: *Özlem Murzoğlu Kurt, MD — Curriculum Vitae* (2026, 5 sayfa).
Yalnız künye/biyografik alanlar aktarıldı; kişisel iletişim/adres bilgisi CV'deki
kurumsal e-posta ile sınırlı tutuldu.

## Uygulanan doldurmalar

- **Öğrenim durumu:** Doktora (Sosyal Pediatri, Marmara, 2019–), Lisans (Çocuk Gelişimi,
  İstanbul Üniv., 2019–2023), Tıpta Uzmanlık (Çocuk Sağlığı ve Hastalıkları, Marmara,
  2011–2017), Tıp (İstanbul Üniv. İstanbul Tıp Fak., 2001–2007).
- **Yabancı dil:** İngilizce (C1).
- **Çalıştığı kurumlar:** bağımsız muayenehane (2022–), Marmara Pendik EAH Çocuk Acil
  birim sorumluluğu (2017–2022), Iğdır Tuzluca DH devlet hizmeti (2017).
- **İletişim:** kurumsal e-posta (CV).
- **Makaleler:** İpar ve ark. 2025 (Gulhane Medical Journal) + Şenkal ve ark. 2023
  (Child: Care, Health and Development) eklendi; iki tez makalesi "hazırlanıyor"
  işaretiyle korundu.
- **Kitap bölümü:** Murzoğlu Kurt & Boran 2021 (Türkiye Klinikleri) eklendi.
- **Sertifikalar:** Triple P, Bayley III, Denver II, SOS Feeding, ETÇEP, İleri Emzirme
  Danışmanlığı, GİDR listelendi (CV §02.2).

## Kapı sonuçları (0-5) — tümü PASS

| Kapı | Kanıt | Sonuç |
|---|---|---|
| 0 | Kapsam/gizlilik: yalnız kullanıcının sağladığı CV künye verisi; ham veri/credential yok; KVKK sınırında kişisel adres/telefon aktarılmadı | ✅ PASS |
| 1 | Bilimsel iddia yok; yalnız yazarın kendi yayın künyeleri ve biyografik alan | ✅ PASS |
| 2 | Dış bibliyografik citation eklenmedi (`@cite` yok); yayın künyeleri düz metin AMA-benzeri biçimde | ✅ PASS |
| 3 | Marmara §3.8/§3.9 özgeçmiş+faaliyet yapısı korundu; CV'de olmayan alanlar işaretli yer tutucu | ✅ PASS |
| 4 | Türkçe akış/biçim korundu; künye biçimi tutarlı | ✅ PASS |
| 5 | `quarto render thesis.qmd` **exit 0**; CV içeriği HTML'de doğrulandı (İpar, Şenkal, Triple P, Pendik EAH, C1) | ✅ PASS |

## Karar

Kapı 0–5 tümü PASS; sahte/uydurma veri eklenmedi; CV'de olmayan kişisel alanlar
işaretli yer tutucu olarak korundu; render exit 0. Statü **`certified-final`**.
