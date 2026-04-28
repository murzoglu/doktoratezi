# Final Reference Veri Haritası

Güncelleme tarihi: 26.04.2026  
Kapsam: `data/processed/FINAL_REFERENCE__analysis_base_long.csv` ve `data/processed/FINAL_REFERENCE__analysis_base_family.csv`

Bu harita, nihai analizlerde kullanılacak temiz referans CSV dosyalarını tanımlar. Belge yalnızca final CSV'lerde bulunan veri alanlarını, değer aralıklarını ve yapısal `NA` kurallarını açıklar. EMBU itemları final kanonik sırada ve 4'lü Likert standardındadır; Beck/BDI, SRQ/KIA, tarih-yaş, demografi ve klinik alanlar analiz girdisi olarak korunur.

## 1. Final Dosyalar

| Dosya | Düzey | Satır | Sütun | İçerik |
|---|---:|---:|---:|---|
| `FINAL_REFERENCE__analysis_base_long.csv` | Çocuk-satırı / long | 482 | 203 | Her katılımcı çocuk satırı; index ve kardeş satırları birlikte |
| `FINAL_REFERENCE__analysis_base_family.csv` | Aile-satırı / wide | 241 | 288 | Aile başına tek satır; index, kardeş ve anne/ebeveyn blokları yan yana |

Kalıcı final referans kuralı:

- Nihai dosya adları `FINAL_REFERENCE__` prefixini korur.
- `data/processed/` altında kalıcı analiz referansı olarak yalnız `FINAL_REFERENCE__` dosyaları tutulur.
- `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` dosyası geçerli final CSV sürümünün satır/sütun sayılarını ve SHA-256 özetlerini kaydeder.
- Boş CSV hücresi `NA` anlamına gelir; literal `#N/A` veya `?` final CSV'lerde saklanmaz.
- Bu stage gerçek veya yapısal eksikliği impute etmez.

## 2. Ortak Veri Standartları

| Alan tipi | Kolonlar / örüntü | Standart |
|---|---|---|
| Aile anahtarı | `aile_no` | Tam sayı aile ID'si; family dosyada tekil |
| Çocuk anahtarı | `cocuk_no`, `kardes_cocuk_no` | Aile içi çocuk ID'si |
| Rol | `katilimci_cocuk`, `is_index`, `family_role`, `role`, `group`, `kardes_role` | Çocuk rolü ve DM/Kontrol grup ayrımı |
| Tarih | `*_tarihi`, `anket_tarihi`, `kardes_anket_tarihi` | `gg.aa.yyyy` metin formatı |
| Yaş/süre | `cocuk_yas`, `kardes_yas`, `anne_yas`, `dm_yili` | Yıl cinsinden ondalık sayı; tarih farkı / 365.25 |
| EMBU item | `embu_*_qXX` | Final 4'lü Likert; geçerli değerler `1`, `2`, `3`, `4` |
| BDI item | `beck_1`-`beck_21` | 0-3 aralığında Beck Depresyon Envanteri madde skoru |
| KIA/SRQ item | `srq_1`-`srq_48`, `srq_sib_1`-`srq_sib_48` | 1-5 aralığında kardeş ilişkileri yanıtı |
| Klinik | `hba1c` | Son ölçülmüş klinik HbA1c yüzde değeri; yalnız `DM_Hasta_Indeks` satırında dolu olabilir; plauzibilite aralığı `4.5 – 18.0`% |
| Demografi/klinik | aile, anne, eş, çocuk ve DM tanı alanları | Kod değerleri mevcut veri standardına göre saklanır |

`katilimci_cocuk` rol kodları:

| Kod | `role` | `group` | `is_index` | `family_role` |
|---:|---|---|---|---|
| 1 | `DM_Hasta_Indeks` | `DM` | `TRUE` | `index` |
| 2 | `DM_Hasta_Kardes` | `DM` | `FALSE` | `sibling` |
| 3 | `Kontrol_Indeks` | `Kontrol` | `TRUE` | `index` |
| 4 | `Kontrol_Kardes` | `Kontrol` | `FALSE` | `sibling` |

Beck/BDI final standardı:

- Beck bloğu her iki final CSV'de `beck_1`-`beck_21` sırasıyla tutulur.
- Item değerleri yalnız `0`, `1`, `2`, `3` veya `NA` olabilir.
- `beck_total` final CSV'lerde saklanmaz; R analizinde `beck_1`-`beck_21` toplamı olarak üretilir.
- Herhangi bir Beck itemı `NA` ise analizde üretilecek `beck_total` da `NA` kalır.
- Long dosyada Beck bloğu yalnız index satırlarında doldurulur; kardeş satırlarında yapısal `NA`dır.
- Beck item alanları ve skorlama kuralı [KANONIK_BECK_DEPRESYON_ENVANTERI.md](KANONIK_BECK_DEPRESYON_ENVANTERI.md) belgesinde tanımlıdır.

KIA/SRQ final standardı:

- KIA/SRQ bloğu final CSV'lerde `srq_` prefixiyle tutulur; `kia_` prefixi final referans standardında kullanılmaz.
- Long dosyada her çocuk satırı için `srq_1`-`srq_48` bulunur.
- Family dosyada index çocuk için `srq_1`-`srq_48`, kardeş çocuk için `srq_sib_1`-`srq_sib_48` bulunur.
- Item değerleri yalnız `1`, `2`, `3`, `4`, `5` veya `NA` olabilir.
- KIA/SRQ toplam, ortalama, alt boyut veya kategori skorları final CSV'lerde saklanmaz; analizde üretilecek skorlar [KANONIK_KARDES_ILISKILERI_ANKETI.md](KANONIK_KARDES_ILISKILERI_ANKETI.md) belgesindeki item standardına göre R katmanında hesaplanır.

Demografik ve tıbbi final standardı:

- DM ve kontrol grubu demografik-tıbbi formları tek final standart altında temsil edilir.
- Long dosyada aile düzeyi demografi/klinik alanları aynı `aile_no` içindeki index ve kardeş satırlarında aynıdır.
- Family dosyada aile düzeyi alanlar index satırından temsil edilir; kardeşe özgü alanlar `kardes_*` prefixiyle tutulur.
- Tarih alanları `gg.aa.yyyy` formatındadır; yaş ve süre alanları tarih farkı / 365.25 ile uyumludur.
- `dm_tani_tarihi`, `dm_yili` ve `hba1c` yalnız `role == "DM_Hasta_Indeks"` için doludur.
- `hba1c` final analiz veri setinde saklanan son ölçülmüş klinik HbA1c yüzdesidir; ondalık sayı; eksikse `NA`. Final veride 120 DM indeks çocuğun 39'unda doludur; DM indeks dışındaki satırlarda dolu değer yoktur. HbA1c eşleştirmesi hasta/aile kimliği üzerinden kesinleştirilmiştir; HbA1c dışındaki ara eşleştirme alanları final veri standardına dahil değildir. Glisemik kontrolün ebeveynlik tutumu ile ilişkisinde birincil klinik kovaryat olarak kullanılır.
- Kronik hastalık/engel ve antidepresan gibi ikili tıbbi alanlarda standart kodlama `0 = Hayır/yok`, `1 = Evet/var` şeklindedir.
- Emekli eş/baba aktif çalışıyor sayılmaz: `es_calisma_durumu = 0`, `es_emekli = 1`; aktif meslek/ISEI/SIOPS/EGP alanları yapısal `NA` kalır.
- Eski serbest metin alanları final CSV'lerden kaldırılmıştır; meslek ve kronik hastalık açıklamaları standardize alanlara dönüştürülmüş, raw metinler yalnız audit dosyasında saklanmıştır.
- Hastalık kategori seti `endokrin`, `kardiyovaskuler`, `solunum`, `gastrointestinal`, `renal`, `kas_iskelet`, `mental`, `sinir`, `otoimmun`, `duyu`, `hematolojik`, `dermatolojik`, `neoplazm`, `diger` alanlarından oluşur.
- Demografik ve tıbbi kod haritası [KANONIK_DEMOGRAFIK_VE_TIBBI_BILGILER.md](KANONIK_DEMOGRAFIK_VE_TIBBI_BILGILER.md) belgesinde tanımlıdır.

## 3. Long Dosya Şeması

Dosya: `data/processed/FINAL_REFERENCE__analysis_base_long.csv`

| Sütun grubu | Kolonlar | Açıklama |
|---|---|---|
| Kimlik ve rol | `aile_no`, `cocuk_no`, `katilimci_cocuk`, `is_index`, `family_role`, `role`, `group` | Çocuk satırı kimliği ve grup/rol ayrımı |
| Tarih ve yaş | `anket_tarihi`, `anne_dogum_tarihi`, `katilimci_cocuk_dogum_tarihi`, `dm_tani_tarihi`, `kardes_dogum_tarihi`, `cocuk_yas`, `anne_yas`, `dm_yili` | Tarih ve türetilmiş yaş/süre alanları |
| Çocuk/aile demografi | `cocuk_sayisi`, `katilimci_cocuk_sirasi`, `katilimci_cocuk_cinsiyet`, `kardes_cinsiyet`, `medeni_durum`, `es_sag` | Çocuk ve aile yapısı alanları |
| Anne/eş sosyoekonomik | `egitim_durumu`, `es_egitim_durumu`, `calisma_durumu`, `es_calisma_durumu`, `es_emekli`, `ev_sahipligi`, `ev_oda_sayisi`, `arabaniz_var_mi`, `es_isco08_*`, `es_isei08`, `es_siops08`, `es_egp7`, `aile_isei08`, `aile_siops08`, `aile_egp7` | Kod değerleri ve araştırmacı kararıyla nihai meslek/SES standardizasyonu |
| Klinik/durum | `anne_antidepresan`, `kronik_hastalik_durumu`, `esiniz_kronik_hastalik_durumu`, `anne_hastalik_*`, `es_hastalik_*`, `hba1c` | Klinik durum bayrakları, nihai hastalık kategori kodları ve T1DM glisemik kontrol değeri |
| Beck/BDI | `beck_1`-`beck_21` | Sibling satırlarında yapısal `NA`; index satırlarında anne bildirimi |
| KIA/SRQ | `srq_1`-`srq_48` | Her çocuk satırında çocuk düzeyi kardeş ilişkileri item bloğu |
| EMBU-P | `embu_p_q01`-`embu_p_q29` | Sibling satırlarında yapısal `NA`; index satırlarında anne/ebeveyn bildirimi |
| EMBU-C | `embu_c_q01`-`embu_c_q29` | Her çocuk satırında çocuk bildirimi; `q25` ters skorlanmış final değerdir |

Yapısal eksiklik kuralları:

- `is_index == FALSE` satırlarında `embu_p_q01`-`embu_p_q29` ve `beck_1`-`beck_21` yapısal `NA`dır.
- `dm_yili` ve `hba1c` yalnız `role == "DM_Hasta_Indeks"` için hesaplanır; kontrol ve kardeş satırlarında yapısal `NA`dır.
- Long dosyada `hba1c` 39/120 DM indeks satırında doludur; 362 DM kardeş/kontrol satırında yapısal `NA`dır.

## 4. Family Dosya Şeması

Dosya: `data/processed/FINAL_REFERENCE__analysis_base_family.csv`

| Sütun grubu | Kolonlar | Açıklama |
|---|---|---|
| Aile ve index kimliği | `aile_no`, `cocuk_no`, `katilimci_cocuk`, `is_index`, `role`, `family_role`, `group` | Family satırındaki ana kişi index çocuktur |
| Index tarih/yaş | `anket_tarihi`, `katilimci_cocuk_dogum_tarihi`, `dm_tani_tarihi`, `cocuk_yas`, `anne_yas`, `dm_yili` | Index çocuk ve anne yaş/süre alanları |
| T1DM klinik | `hba1c` | Yalnız `DM_Hasta_Indeks` aile satırında dolu olabilir; 39/120 DM indeks ailede dolu; ondalık yüzde |
| Anne/aile demografi-klinik | `anne_dogum_tarihi`, `anne_antidepresan`, `cocuk_sayisi`, `medeni_durum`, `es_sag`, `es_dogum_tarihi`, `egitim_durumu`, `es_egitim_durumu`, `calisma_durumu`, `es_calisma_durumu`, `es_emekli`, `ev_sahipligi`, `ev_oda_sayisi`, `arabaniz_var_mi`, `kronik_hastalik_durumu`, `esiniz_kronik_hastalik_durumu`, `es_isco08_*`, `aile_isei08`, `anne_hastalik_*`, `es_hastalik_*` | Aile/anne düzeyi kovaryatlar ve standardize meslek/hastalık alanları |
| Index çocuk demografi | `katilimci_cocuk_sirasi`, `katilimci_cocuk_cinsiyet` | Index çocuk bilgisi |
| Kardeş kimlik/demografi | `kardes_cocuk_no`, `kardes_katilimci_cocuk`, `kardes_is_index`, `kardes_family_role`, `kardes_role`, `kardes_anket_tarihi`, `kardes_dogum_tarihi`, `kardes_sirasi`, `kardes_cinsiyet`, `kardes_yas` | Kardeş satırından wide forma taşınan alanlar |
| Beck/BDI | `beck_1`-`beck_21` | Anne/index düzeyi BDI item bloğu |
| EMBU-P | `embu_p_q01`-`embu_p_q29` | Anne/ebeveyn bildirimi |
| EMBU-C index | `embu_c_idx_q01`-`embu_c_idx_q29` | Index çocuğun çocuk bildirimi |
| EMBU-C kardeş | `embu_c_sib_q01`-`embu_c_sib_q29` | Kardeş çocuğun çocuk bildirimi |
| KIA/SRQ index | `srq_1`-`srq_48` | Index çocuk KIA/SRQ bloğu |
| KIA/SRQ kardeş | `srq_sib_1`-`srq_sib_48` | Kardeş çocuk KIA/SRQ bloğu |

Family dosyada her `aile_no` tek satırdır. Kardeş alanları `kardes_*`, `srq_sib_*` ve `embu_c_sib_*` prefixleriyle ayrılır. Index çocuk EMBU-C alanları `embu_c_idx_*` prefixiyle tutulur; family dosyada çıplak `embu_c_qXX` kolonu bulunmaz.

## 5. Likert ve Ölçek Standartları

Final CSV'lerde tüm EMBU item skorları 4'lü Likert standardındadır.

| Skor | Çocuk formu yorumu | Ebeveyn formu yorumu |
|---:|---|---|
| 1 | Hayır / hiçbir zaman | Hiçbir zaman veya en düşük sıklık standardı |
| 2 | Evet, bazen | Düşük-orta sıklık standardı |
| 3 | Evet, çoğu zaman | Orta-yüksek sıklık standardı |
| 4 | Evet, her zaman | Her zaman veya en yüksek sıklık standardı |

Notlar:

- EMBU-P ve EMBU-C final item kolonları analiz için doğrudan kullanılacak nihai 4'lü ordinal değerlerdir.
- Çocuk formu `q25` final CSV'lerde ters skorlanmış olarak saklanır.

## 6. EMBU-P Alt Ölçek Haritası

Bu harita `embu_p_qXX` kolon adlarına göre tanımlıdır.

| Alt ölçek | Madde kolonları | Madde sayısı |
|---|---|---:|
| Duygusal Sıcaklık | `q01`, `q03`, `q06`, `q07`, `q13`, `q17`, `q20`, `q24`, `q26` | 9 |
| Aşırı Koruma | `q04`, `q08`, `q14`, `q15`, `q19`, `q23`, `q25` | 7 |
| Reddetme | `q05`, `q09`, `q10`, `q12`, `q16`, `q21`, `q22`, `q28` | 8 |
| Karşılaştırma | `q02`, `q11`, `q18`, `q27`, `q29` | 5 |

EMBU-P madde 25 final kanonda ters skorlanmaz; item değeri doğrudan kaydedilir.

## 7. EMBU-C Kolon Haritası

Bu harita final veri kolonlarını açıklar. Çocuk formunda `qXX` kolonları ebeveyn formuyla aynı semantik sıraya getirilmiştir; yani `embu_p_qXX`, `embu_c_qXX`, `embu_c_idx_qXX` ve `embu_c_sib_qXX` aynı ebeveynlik davranışının farklı bildirim/düzey karşılıklarıdır.

| Alt ölçek | Final EMBU-C kolonları | Madde sayısı | Not |
|---|---|---:|---|
| Duygusal Sıcaklık | `q01`, `q03`, `q06`, `q07`, `q13`, `q17`, `q20`, `q24`, `q26` | 9 | P ile aynı sıra |
| Aşırı Koruma | `q04`, `q08`, `q14`, `q15`, `q19`, `q23`, `q25` | 7 | `q25` finalde ters skorlanmıştır |
| Reddetme | `q05`, `q09`, `q10`, `q12`, `q16`, `q21`, `q22`, `q28` | 8 | P ile aynı sıra |
| Karşılaştırma | `q02`, `q11`, `q18`, `q27`, `q29` | 5 | P ile aynı sıra |

## 8. Skorlama Çerçevesi

Final CSV'ler EMBU, Beck/BDI veya KIA/SRQ toplam/alt ölçek skorlarını saklamaz. Saklanan ölçek alanları item düzeyi analiz girdileridir; toplam ve alt ölçek skorları R analiz katmanında üretilir.

Raporlama veya analiz için EMBU alt ölçek skoru üretilecekse:

- Her madde `1`-`4` aralığında yorumlanır; yüksek değer ilgili madde içeriğinin daha güçlü bildirildiğini gösterir.
- Alt ölçek toplamı, ilgili itemların toplamıdır.
- Alt ölçek ortalaması, ilgili itemların ortalamasıdır ve `1`-`4` ölçeğinde kalır.
- Çocuk formu `q25` final CSV'de ters skorlanmış olduğu için aşırı koruma alt ölçeğine doğrudan dahil edilebilir.
- Eksik veri eşiği analiz fazında ayrıca dokümante edilmelidir.

Teorik toplam aralıkları:

| Form/blok | Sıcaklık | Aşırı Koruma | Reddetme | Karşılaştırma |
|---|---:|---:|---:|---:|
| 29 maddelik EMBU-P | 9-36 | 7-28 | 8-32 | 5-20 |
| 29 maddelik EMBU-C final kolon seti | 9-36 | 7-28 | 8-32 | 5-20 |

## 9. İlişkili Dokümanlar

| Doküman | İşlev |
|---|---|
| `docs/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md` | Final EMBU-P anket maddeleri, Likert ve puanlama notları |
| `docs/KANONIK_KISALTILMIS_EMBU_COCUK.md` | Final EMBU-C anket maddeleri, Likert ve puanlama notları |
| `docs/KANONIK_BECK_DEPRESYON_ENVANTERI.md` | Final Beck item alanları, analizde üretilecek toplam puan ve yapısal `NA` standardı |
| `docs/KANONIK_KARDES_ILISKILERI_ANKETI.md` | Final KIA/SRQ item alanları, Likert ve analizde üretilecek skor standardı |
| `docs/KANONIK_DEMOGRAFIK_VE_TIBBI_BILGILER.md` | Final demografik ve tıbbi alanlar, kodlar, tarih/yaş ve yapısal `NA` standardı |
