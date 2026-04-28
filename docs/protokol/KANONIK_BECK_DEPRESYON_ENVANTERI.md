# Beck Depresyon Envanteri - Kanonik Final Form

Güncelleme tarihi: 26.04.2026  
Final veri dosyaları: `data/processed/FINAL_REFERENCE__analysis_base_long.csv`, `data/processed/FINAL_REFERENCE__analysis_base_family.csv`

Bu belge final analizlerde kullanılan Beck Depresyon Envanteri alanlarını tanımlar. Final CSV'lerde Beck bloğu yalnız 21 item skorundan oluşur; toplam puan R analiz katmanında yeniden üretilir.

## 1. Uygulama Standardı

| Alan | Final standart |
|---|---|
| Ölçek adı | Beck Depresyon Envanteri |
| Yanıtlayıcı | Anne/ebeveyn |
| Zaman çerçevesi | Bugün dahil geçen hafta |
| Veri düzeyi | Aile/index düzeyi |
| Final item aralığı | `0`, `1`, `2`, `3` |
| Analizde üretilecek toplam aralığı | `0`-`63` |

## 2. Final Veri Alanları

| Dosya | Beck alanları | Yapısal kural |
|---|---|---|
| `FINAL_REFERENCE__analysis_base_long.csv` | `beck_1`-`beck_21` | Index satırlarında doldurulur; kardeş satırlarında yapısal `NA` |
| `FINAL_REFERENCE__analysis_base_family.csv` | `beck_1`-`beck_21` | Aile/index düzeyinde tek Beck item bloğu |

Final kolon sırası her iki dosyada da `beck_1`, `beck_2`, ..., `beck_21` şeklindedir.

## 3. Madde Alanları

Her madde dört şiddet seçeneğinden birine karşılık gelen tek bir skorla saklanır. Skor yükseldikçe ilgili depresif belirti alanının şiddeti artar.

| Kolon | Belirti alanı |
|---|---|
| `beck_1` | Üzüntü / sıkıntı |
| `beck_2` | Geleceğe yönelik karamsarlık |
| `beck_3` | Başarısızlık algısı |
| `beck_4` | Zevk alma / doyum kaybı |
| `beck_5` | Suçluluk |
| `beck_6` | Cezalandırılma algısı veya beklentisi |
| `beck_7` | Kendinden memnuniyet |
| `beck_8` | Kendini eleştirme veya suçlama |
| `beck_9` | Yaşamı sonlandırma düşüncesi |
| `beck_10` | Ağlama |
| `beck_11` | Sinirlilik |
| `beck_12` | Sosyal ilgi / insanlarla görüşme isteği |
| `beck_13` | Karar verme güçlüğü |
| `beck_14` | Beden görünümü algısı |
| `beck_15` | Çalışma ve günlük işlevsellik |
| `beck_16` | Uyku |
| `beck_17` | Yorgunluk |
| `beck_18` | İştah |
| `beck_19` | Kilo kaybı |
| `beck_20` | Sağlıkla ilgili kaygı |
| `beck_21` | Cinsel ilgi |

## 4. Skorlama

| Hesap | Final kural |
|---|---|
| Item skoru | Her madde `0`-`3` aralığında tek skor olarak saklanır. |
| Çoklu işaretleme | Aynı maddede birden fazla seçenek işaretlendiyse final skor en yüksek şiddet seçeneğidir. |
| Ters madde | Yoktur. |
| Toplam puan | R analizinde `beck_total = beck_1 + beck_2 + ... + beck_21` olarak üretilir. |
| Eksik item | Herhangi bir Beck itemı `NA` ise analizde üretilecek `beck_total` da `NA` kalır. |
| Yorum yönü | Daha yüksek toplam puan daha yüksek depresif belirti düzeyini gösterir. |

Bu final doküman klinik kesme puanı tanımlamaz. Kesme puanı veya kategori üretilecekse ilgili analiz planında ayrıca sabitlenmelidir.

## 5. Veri Kalitesi Kuralları

- `beck_1`-`beck_21` dışında Beck item kolonu bulunmaz.
- Item değerleri yalnız `0`, `1`, `2`, `3` veya `NA` olabilir.
- Final CSV'lerde `beck_total` veya başka türetilmiş Beck toplam/alt skor kolonu bulunmaz.
- Long dosyada `is_index == FALSE` olan kardeş satırlarında `beck_1`-`beck_21` yapısal `NA`dır.
- Family dosyada Beck bloğu long dosyadaki aynı `aile_no` index satırıyla bire bir aynı olmalıdır.
