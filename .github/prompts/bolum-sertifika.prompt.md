---
description: 'Bölüm finalizasyon sertifikasyonu — Kapı 0-5 denetimi; certified-final yalnız açık kullanıcı onayıyla'
mode: agent
---

**${input:bolum:bölüm adı, ör. 01_giris}** bölümü için finalizasyon sertifikasyon sürecini işlet.
Zorunlu playbook: `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
(önce onu oku ve kapı tanımlarını oradan uygula). Kapılar sırayla, atlanamaz:

1. **Kapı 0 — Kapsam/gizlilik**: bölümün kaynak seti `06_kritik-kaynaklar`
   manifestiyle eşleşiyor mu; korumalı veri sınırı ihlali var mı.
2. **Kapı 1 — Derin literatür**: bölümün iddia haritası; eksik/zayıf kanıtlı
   iddialar listesi.
3. **Kapı 2 — Full-text/Zotero/bağlam**: bölümdeki HER referans
   `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` içinde
   `cite-ok` (veya gerekçeli `full-text-exception`) mi.
4. **Kapı 3 — Metin/kılavuz uyumu**: resmi kılavuz + `format-kontrati.md`
   (başlık düzeni, ondalık virgül, tablo/şekil, AMA-11 kaynakça, edilgen dil).
5. **Kapı 4 — Türkçe imla/akış**: imla, terim tutarlılığı, paragraf akışı.
6. **Kapı 5 — AI-reliability/render**: `/tez-dogrulama` PASS + `quarto render`
   exit 0 + nitel kolda `t1dm-qual-ai-audit` (referanslı bölümde çift kapı).

Karar kuralı:
- Tüm kapılar PASS **ve kullanıcı açık onay verdiyse** →
  `tez-yazim/04_kalite-kontrol/sertifikalar/<bölüm>-sertifika-<tarih>.md`
  dosyasına `Durum: certified-final` sertifikası yaz (mevcut GİRİŞ sertifikası
  formatını şablon al).
- Teknik kapılar geçse bile açık onay yoksa en fazla `provisional-pass` yazılır.
- Herhangi bir kapı FAIL ise `blocked` + Bloklayıcı Hata Sözlüğü'ne göre
  gerekçe ve düzeltme planı yazılır; Gap Register
  (`tez-yazim/01_mimari/tez-yazim-ana-plani.md`) güncellenir.
