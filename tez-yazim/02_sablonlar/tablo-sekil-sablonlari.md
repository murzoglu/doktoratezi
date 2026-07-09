# Tablo ve Şekil Sablonları

> **Kanonik kural otoritesi:** Tablo/şekil biçim kuralı →
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §1.7 (tablolar) +
> §1.6 (şekiller); istatistik yazımı (`p`, ondalık virgül) → §8 + §1.4; kapanış
> checklist'i → §12. Bu dosya yalnız iskelet + kontrol hatırlatıcısıdır. Klasör
> haritası: `02_sablonlar/README.md`.

## Tablo Sablonu

Tablo başlığı tablonun üstünde yer alır.

```text
Tablo X. Kısa, açıklayıcı tablo başlığı.

| Değişken | Grup/ölçüt | İstatistik | p değeri |
|---|---:|---:|---:|
| ... | ... | ... | ... |

Not. Kısaltmalar, test adı, payda, eksik veri ve gerekli kaynak açıklaması.
```

Kontrol:

- [ ] Tablo metinde ilk anıldığı yerde veya takip eden sayfada.
- [ ] Aynı veri ayrıca şekil olarak tekrarlanmadı.
- [ ] Kısaltmalar dipnotta açıklandı.
- [ ] `p` değerleri ondalık virgülle yazıldı.
- [ ] Tablo tek başına anlaşılabilir.

## Şekil Sablonu

Şekil başlığı şeklin altında yer alır.

```text
Şekil X. Kısa, açıklayıcı şekil başlığı. Kısaltma: açıklama.
```

Kontrol:

- [ ] Şekil metinde anıldı.
- [ ] Şekil başlığı altında.
- [ ] Kaynak veya uyarlama notu varsa başlıkta/dipnotta belirtildi.
- [ ] Renk/etiketler siyah-beyaz çıktı için anlaşılır.
