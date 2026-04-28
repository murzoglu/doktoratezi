# Kardeş İlişkileri Anketi - Kanonik Final Form

Güncelleme tarihi: 26.04.2026  
Final veri dosyaları: `data/processed/FINAL_REFERENCE__analysis_base_long.csv`, `data/processed/FINAL_REFERENCE__analysis_base_family.csv`

Bu belge final analizlerde kullanılan Kardeş İlişkileri Anketi alanlarını tanımlar. Final CSV'lerde anket yalnız item düzeyi skorlarla saklanır; toplam, ortalama, alt boyut veya kategori skorları R analiz katmanında üretilir.

## 1. Uygulama Standardı

| Alan | Final standart |
|---|---|
| Ölçek adı | Kardeş İlişkileri Anketi |
| İngilizce adı | Sibling Relationship Questionnaire |
| Final kolon prefixi | `srq_` |
| Yanıtlayıcı | Katılımcı çocuk |
| Veri düzeyi | Çocuk-satırı / kardeş çifti algısı |
| Item sayısı | 48 |
| Final item aralığı | `1`, `2`, `3`, `4`, `5` |

## 2. Final Veri Alanları

| Dosya | KIA/SRQ alanları | Yapısal kural |
|---|---|---|
| `FINAL_REFERENCE__analysis_base_long.csv` | `srq_1`-`srq_48` | Her çocuk satırında çocuğun kardeş ilişkisi bildirimi |
| `FINAL_REFERENCE__analysis_base_family.csv` | `srq_1`-`srq_48` | Index çocuğun kardeş ilişkisi bildirimi |
| `FINAL_REFERENCE__analysis_base_family.csv` | `srq_sib_1`-`srq_sib_48` | Kardeş çocuğun kardeş ilişkisi bildirimi |

Final kolon sırası long dosyada `srq_1`, `srq_2`, ..., `srq_48`; family dosyada index bloğu için `srq_1`-`srq_48`, kardeş bloğu için `srq_sib_1`-`srq_sib_48` şeklindedir. Final CSV'lerde `kia_` prefixi kullanılmaz.

## 3. Likert ve Yanıt Standardı

Standart sıklık/yoğunluk maddelerinde final skorlar şöyledir:

| Skor | Yanıt |
|---:|---|
| 1 | Hemen hemen hiç |
| 2 | Oldukça az |
| 3 | Biraz |
| 4 | Oldukça fazla |
| 5 | Çok çok fazla |

Ebeveyn davranışının iki kardeş arasında göreli yönünü soran maddeler `srq_2`, `srq_7`, `srq_18`, `srq_23`, `srq_34` ve `srq_39` için final skor yine `1`-`5` aralığındadır. Bu maddelerde `1` kardeş lehine, orta değer eşitlik/tarafsızlık, `5` yanıtlayan çocuk lehine yönü temsil eder.

## 4. Madde Alanları

Madde metinleri final CSV'lerde saklanmaz; kolonlar aşağıdaki kısa içerik alanlarıyla temsil edilir.

| Kolon | İçerik alanı |
|---|---|
| `srq_1` | Karşılıklı iyi şeyler yapma |
| `srq_2` | Annenin daha iyi davranma yönü |
| `srq_3` | Kardeşe yapmayı bilmediği şeyleri gösterme |
| `srq_4` | Kardeş tarafından yapmayı bilmediği şeylerin gösterilmesi |
| `srq_5` | Kardeşe ne yapması gerektiğini söyleme |
| `srq_6` | Kardeşin ne yapılması gerektiğini söylemesi |
| `srq_7` | Babanın daha iyi davranma yönü |
| `srq_8` | Karşılıklı önemseme |
| `srq_9` | Birlikte etkinlik yapma |
| `srq_10` | Aşağılama veya isim takma |
| `srq_11` | Aynı şeylerden hoşlanma |
| `srq_12` | Birbirine her şeyi anlatma |
| `srq_13` | Birbirini geçme veya yenme çabası |
| `srq_14` | Kardeşe hayranlık ve saygı |
| `srq_15` | Kardeşin hayranlık ve saygısı |
| `srq_16` | Anlaşamama ve kavga etme |
| `srq_17` | İşbirliği yapma |
| `srq_18` | Anneden daha fazla ilgi görme yönü |
| `srq_19` | Kardeşe yardım etme |
| `srq_20` | Kardeşten yardım alma |
| `srq_21` | Kardeşe istenen şeyleri yaptırma |
| `srq_22` | Kardeşin istenen şeyleri yaptırması |
| `srq_23` | Babadan daha fazla ilgi görme yönü |
| `srq_24` | Karşılıklı sevgi |
| `srq_25` | Birlikte oynama ve eğlenme |
| `srq_26` | Birbirine kötü davranma |
| `srq_27` | Ortak yönler |
| `srq_28` | Sırları ve özel duyguları paylaşma |
| `srq_29` | Yarışma |
| `srq_30` | Kardeşe saygı duyma ve gururlanma |
| `srq_31` | Kardeşin saygı duyması ve gururlanması |
| `srq_32` | Kızma ve tartışmaya girme |
| `srq_33` | Bir şeyleri paylaşma |
| `srq_34` | Annenin kayırma yönü |
| `srq_35` | Kardeşe bilmediği şeyleri öğretme |
| `srq_36` | Kardeşten bilmediği şeyleri öğrenme |
| `srq_37` | Kardeşe emir verme |
| `srq_38` | Kardeşten emir alma |
| `srq_39` | Babanın kayırma yönü |
| `srq_40` | Güçlü sevgi duygusu |
| `srq_41` | Boş zamanı birlikte geçirme |
| `srq_42` | Birbirini kızdırma ve uğraşma |
| `srq_43` | Birbirine benzeme |
| `srq_44` | Başkalarının bilmesini istemediği şeyleri anlatma |
| `srq_45` | Bir şeyleri birbirinden daha iyi yapmaya çalışma |
| `srq_46` | Kardeşe değer verme |
| `srq_47` | Kardeşin değer vermesi |
| `srq_48` | Tartışma |

## 5. Skorlama

| Hesap | Final kural |
|---|---|
| Item skoru | Her madde `1`-`5` aralığında tek skor olarak saklanır. |
| Ters madde | Final referans CSV'de ters skorlanmış KIA/SRQ maddesi yoktur. |
| Global toplam | Final kanonda tanımlı değildir ve CSV'de saklanmaz. |
| Alt boyut skoru | Analiz planında madde kümesi sabitlenirse R analizinde toplam veya ortalama olarak üretilir. |
| Eksik item | Skor üretilecek madde kümesinde herhangi bir item `NA` ise varsayılan final kuralı skoru `NA` bırakmaktır; farklı eşik kullanılırsa analiz planında ayrıca belirtilir. |

KIA/SRQ için protokol düzeyinde dört genel boyut kullanılır: Sıcaklık/Yakınlık, Bağlantı Statü/Güç, Çatışma ve Rekabet. Bu belge item düzeyi final veri standardını kilitler; alt boyut madde kümeleri, ters/yön kararları ve eksik veri eşiği analiz fazında ayrıca sabitlenmeden final CSV'ye skor kolonu eklenmez.

## 6. Veri Kalitesi Kuralları

- `srq_1`-`srq_48` dışında long dosyada KIA/SRQ item kolonu bulunmaz.
- Family dosyada index bloğu `srq_1`-`srq_48`, kardeş bloğu `srq_sib_1`-`srq_sib_48` şeklindedir.
- Item değerleri yalnız `1`, `2`, `3`, `4`, `5` veya `NA` olabilir.
- Final CSV'lerde `kia_` prefixi, `srq_total` veya başka türetilmiş KIA/SRQ toplam/alt skor kolonu bulunmaz.
- Family dosyada `srq_1`-`srq_48` bloğu long dosyadaki aynı `aile_no` index satırıyla, `srq_sib_1`-`srq_sib_48` bloğu ise aynı `aile_no` kardeş satırıyla bire bir aynı olmalıdır.
