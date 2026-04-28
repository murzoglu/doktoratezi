# Demografik ve Tıbbi Bilgiler - Kanonik Final Form

Güncelleme tarihi: 26.04.2026  
Final veri dosyaları: `data/processed/FINAL_REFERENCE__analysis_base_long.csv`, `data/processed/FINAL_REFERENCE__analysis_base_family.csv`

Bu belge DM ve kontrol grubu demografik-tıbbi bilgi formlarından gelen final veri alanlarını tanımlar. Final CSV'lerde demografik ve tıbbi bilgiler kimlik, rol, tarih, çocuk, anne/aile, eş, sosyoekonomik, tıbbi kategori, DM tanı ve HbA1c alanları olarak saklanır.

## 1. Form Kapsamı

| Form | Final veri karşılığı |
|---|---|
| DM grubu demografik-tıbbi formu | DM indeks çocuk, sağlıklı kardeş, anne/aile ve DM tanı bilgileri |
| Kontrol grubu demografik-tıbbi formu | Kontrol indeks çocuk, kardeş, anne/aile bilgileri |

İki formun ortak çekirdeği anne/aile bilgileri, index çocuk bilgileri ve kardeş bilgilerini içerir. DM formuna özgü alan `dm_tani_tarihi`dir.

## 2. Dosya Düzeyleri

| Dosya | Düzey | Satır | Sütun | Demografik-tıbbi temsil |
|---|---|---:|---:|---|
| `FINAL_REFERENCE__analysis_base_long.csv` | Çocuk-satırı | 482 | 203 | Her ailede index ve kardeş satırı; aile düzeyi alanlar iki satırda aynıdır |
| `FINAL_REFERENCE__analysis_base_family.csv` | Aile-satırı | 241 | 288 | Aile başına tek satır; index ve kardeş alanları ayrı bloklarda tutulur |

## 3. Kimlik ve Rol Alanları

| Kolon | Standart |
|---|---|
| `aile_no` | Tam sayı aile ID'si |
| `cocuk_no` | Aile içi çocuk ID'si; örn. `1200-3` |
| `katilimci_cocuk` | Formdaki katılımcı çocuk rol kodu |
| `is_index` | `TRUE` index çocuk, `FALSE` kardeş çocuk |
| `family_role` | `index` veya `sibling` |
| `role` | Dört kategorili final rol etiketi |
| `group` | `DM` veya `Kontrol` |

`katilimci_cocuk` rol kodları:

| Kod | `role` | `group` | `is_index` |
|---:|---|---|---|
| 1 | `DM_Hasta_Indeks` | `DM` | `TRUE` |
| 2 | `DM_Hasta_Kardes` | `DM` | `FALSE` |
| 3 | `Kontrol_Indeks` | `Kontrol` | `TRUE` |
| 4 | `Kontrol_Kardes` | `Kontrol` | `FALSE` |

## 4. Tarih ve Türetilmiş Süre Alanları

| Kolon | Düzey | Standart |
|---|---|---|
| `anket_tarihi` | Aile/çocuk | `gg.aa.yyyy` |
| `anne_dogum_tarihi` | Anne/aile | `gg.aa.yyyy` |
| `es_dogum_tarihi` | Eş/aile | `gg.aa.yyyy`; eş bilgisi yoksa `NA` |
| `katilimci_cocuk_dogum_tarihi` | Çocuk | Satırdaki çocuk doğum tarihi |
| `kardes_dogum_tarihi` | Long eşleşme alanı | Aynı ailedeki diğer çocuğun doğum tarihi; long dosyada karşı çocuk satırından türetilir |
| `kardes_anket_tarihi` | Family kardeş bloğu | Kardeş satırının anket tarihi |
| `dm_tani_tarihi` | DM indeks | Yalnız `role == "DM_Hasta_Indeks"` için doludur |
| `cocuk_yas` | Çocuk | `(anket_tarihi - katilimci_cocuk_dogum_tarihi) / 365.25` |
| `kardes_yas` | Family kardeş bloğu | Kardeş çocuğun anket tarihindeki yaşı |
| `anne_yas` | Anne/aile | `(anket_tarihi - anne_dogum_tarihi) / 365.25` |
| `dm_yili` | DM indeks | `(anket_tarihi - dm_tani_tarihi) / 365.25`; diğer rollerde `NA` |

Tarih alanlarının final standardı metin biçimli `gg.aa.yyyy` değeridir. Yaş ve süre alanları tarih alanlarından yeniden üretilebilir sayısal analiz değişkenleridir.

## 5. Çocuk ve Kardeş Alanları

| Kolon | Açıklama | Kod/standart |
|---|---|---|
| `cocuk_sayisi` | Annenin toplam çocuk sayısı | Pozitif tam sayı |
| `katilimci_cocuk_sirasi` | Satırdaki/index çocuğun doğum sırası | Pozitif tam sayı |
| `kardes_sirasi` | Family dosyada kardeş çocuğun doğum sırası | Pozitif tam sayı |
| `katilimci_cocuk_cinsiyet` | Satırdaki/index çocuk cinsiyeti | `0 = Kız`, `1 = Erkek` |
| `kardes_cinsiyet` | Kardeş çocuk cinsiyeti | `0 = Kız`, `1 = Erkek` |
| `kardes_cocuk_no` | Family dosyada kardeş çocuk ID'si | Aile içi çocuk ID'si |
| `kardes_katilimci_cocuk` | Family dosyada kardeş rol kodu | `2` veya `4` |
| `kardes_is_index` | Family dosyada kardeş index durumu | Her zaman `FALSE` |
| `kardes_family_role` | Family dosyada kardeş aile rolü | Her zaman `sibling` |
| `kardes_role` | Family dosyada kardeş rol etiketi | `DM_Hasta_Kardes` veya `Kontrol_Kardes` |

## 6. Anne, Eş ve Sosyoekonomik Alanlar

| Kolon | Form alanı | Final kod standardı |
|---|---|---|
| `medeni_durum` | Medeni durum | `0 = Evli`, `1 = Bekar`, `2 = Boşanmış` |
| `es_sag` | Eş hayatta mı | `0 = Hayır`, `1 = Evet` |
| `egitim_durumu` | Anne eğitim durumu | `0 = Okuma bilmiyor`, `1 = İlkokul`, `2 = Ortaokul`, `3 = Lise`, `4 = Üniversite`, `5 = Lisans üstü` |
| `es_egitim_durumu` | Eş eğitim durumu | `0 = Okuma bilmiyor`, `1 = İlkokul`, `2 = Ortaokul`, `3 = Lise`, `4 = Üniversite`, `5 = Lisans üstü` |
| `calisma_durumu` | Anne çalışıyor mu | `0 = Hayır`, `1 = Evet`; anne meslek serbest metni final CSV'de tutulmaz |
| `es_calisma_durumu` | Eş çalışıyor mu | `0 = Hayır`, `1 = Evet` |
| `es_emekli` | Eş emekli mi | `0 = Hayır`, `1 = Evet`, `NA = metin yokluğu nedeniyle bilinmiyor`; emekli eşlerde `es_calisma_durumu = 0` |
| `ev_sahipligi` | Ev sahipliği | `0 = Kendi mülkümüz`, `1 = Kiralık` |
| `ev_oda_sayisi` | Ev oda sayısı | `0 = 1+1`, `1 = 2+1`, `2 = 3+1`, `3 = 4+1 veya fazlası` |
| `arabaniz_var_mi` | Araba var mı | `0 = Hayır`, `1 = Evet` |

Eş/baba mesleği final CSV'de serbest metin olarak değil, araştırmacı kararıyla standardize edilmiş meslek/SES alanları olarak tutulur:

| Kolon | Final kod standardı |
|---|---|
| `es_emekli` | Emeklilik bayrağı; emekli metni olan eşler aktif çalışıyor sayılmaz |
| `es_isco08_4digit` | Nihai ISCO-08 4 haneli meslek kodu |
| `es_isco08_major` | ISCO-08 ana grup kodu |
| `es_isei08` | ISEI-08 sosyoekonomik indeks puanı |
| `es_siops08` | SIOPS-08 prestij puanı |
| `es_egp7` | EGP-7 sınıf kodu |
| `es_meslek_kodlama_durumu` | Kodlama durumu: `final_rule`, `final_broad_category`, `missing_text`, `not_working_no_text`, `retired_not_working` |
| `es_meslek_kodlama_kaynagi` | Kodlama kaynağı: `investigator_final_2026_04_26` |
| `aile_isei08` | Aile SES gradient için baba/eş ISEI-08 karşılığı |
| `aile_siops08` | Aile düzeyi SIOPS-08 karşılığı |
| `aile_egp7` | Aile düzeyi EGP-7 karşılığı |

Emekli eş/baba için metodolojik final karar: emeklilik güncel aktif meslek olarak kodlanmaz. Bu satırlarda `es_calisma_durumu = 0`, `es_emekli = 1`, `es_isco08_*`, `es_isei08`, `es_siops08`, `es_egp7`, `aile_isei08`, `aile_siops08` ve `aile_egp7` yapısal `NA` olarak kalır. Emeklilik sabit gelir/güvence bilgisini temsil eden ayrı bir bayrak olarak analizde değerlendirilebilir.

## 7. Tıbbi Alanlar

| Kolon | Form alanı | Final kod standardı |
|---|---|---|
| `kronik_hastalik_durumu` | Annede süregiden hastalık/engellilik var mı | `0 = Hayır/yok`, `1 = Evet/var` |
| `esiniz_kronik_hastalik_durumu` | Eşte süregiden hastalık/engellilik var mı | `0 = Hayır/yok`, `1 = Evet/var` |
| `anne_antidepresan` | Anne antidepresan kullanıyor mu | `0 = Hayır`, `1 = Evet` |
| `dm_tani_tarihi` | DM tanı tarihi | Yalnız DM indeks satırında dolu |
| `dm_yili` | DM süresi | Yalnız DM indeks satırında dolu |
| `hba1c` | Klinik HbA1c değeri (%) | Ondalık sayı; yalnız `DM_Hasta_Indeks` satırında dolu olabilir; klinik plauzibilite aralığı `4.5 – 18.0`%; eksikse `NA` |

`hba1c` alanı, T1DM tanılı çocuğun final analiz veri setinde saklanan son ölçülmüş klinik HbA1c yüzdesidir. Glisemik kontrolün ebeveynlik tutumu ile ilişkisinde birincil klinik kovaryat olarak kullanılır. Final veride 120 `DM_Hasta_Indeks` satırının 39'unda HbA1c değeri vardır; 81 DM indeks satırında eksiktir. HbA1c eşleştirmesi hasta/aile kimliği üzerinden kesinleştirilmiştir; HbA1c dışındaki ara eşleştirme alanları final veri standardına dahil değildir. `DM_Hasta_Indeks` dışındaki tüm satırlarda `hba1c` yapısal `NA`'dır.

Final HbA1c kalite özeti:

| Ölçüt | Değer |
|---|---:|
| DM indeks satırı | 120 |
| HbA1c dolu | 39 |
| HbA1c eksik | 81 |
| DM indeks dışı dolu HbA1c | 0 |
| Minimum | 5.8 |
| Medyan | 9.0 |
| Ortalama | 8.97 |
| Maksimum | 15.1 |
| Plauzibilite aralığı dışı (`<4.5` veya `>18.0`) | 0 |

Kronik hastalık alanları final veride standart ikili kodlama ile tutulur: `0` yokluğu, `1` varlığı gösterir. Hastalık/engel açıklama metinleri final CSV'de tutulmaz; aşağıdaki standardize ICD-10 ana kategori dummy alanlarına dönüştürülür.

Anne için `anne_`, eş/baba için `es_` prefixi kullanılır:

| Kolon örüntüsü | Final kod standardı |
|---|---|
| `*_hastalik_endokrin` | `0/1/NA`; endokrin/metabolik hastalık |
| `*_hastalik_kardiyovaskuler` | `0/1/NA`; kardiyovasküler hastalık |
| `*_hastalik_solunum` | `0/1/NA`; solunum sistemi hastalığı |
| `*_hastalik_gastrointestinal` | `0/1/NA`; gastrointestinal hastalık |
| `*_hastalik_renal` | `0/1/NA`; renal/böbrek hastalığı |
| `*_hastalik_kas_iskelet` | `0/1/NA`; kas-iskelet/romatolojik hastalık |
| `*_hastalik_mental` | `0/1/NA`; mental/davranışsal hastalık |
| `*_hastalik_sinir` | `0/1/NA`; sinir sistemi hastalığı |
| `*_hastalik_otoimmun` | `0/1/NA`; otoimmün/otoenflamatuvar hastalık |
| `*_hastalik_duyu` | `0/1/NA`; görme/işitme gibi duyu sistemi hastalığı |
| `*_hastalik_hematolojik` | `0/1/NA`; hematolojik/kanama bozukluğu |
| `*_hastalik_dermatolojik` | `0/1/NA`; dermatolojik hastalık |
| `*_hastalik_neoplazm` | `0/1/NA`; neoplazm/kanser |
| `*_hastalik_diger` | `0/1/NA`; diğer veya sınıflanamayan hastalık |
| `*_hastalik_kategori_sayisi` | Dummy kategorilerinin toplamı; hastalık yükü özeti |
| `*_hastalik_kodlama_durumu` | `no_condition`, `missing_text`, `final_rule`, `final_flag_corrected`, `final_other` |

## 8. Yapısal Kurallar

- Long dosyada aile düzeyi alanlar aynı `aile_no` içindeki index ve kardeş satırlarında aynı olmalıdır.
- Long dosyada `kardes_dogum_tarihi` ve `kardes_cinsiyet`, aynı ailedeki karşı çocuk satırının doğum tarihi ve cinsiyetinden türetilir.
- Family dosyada aile düzeyi alanlar index satırından temsil edilir.
- Family dosyada kardeşe özgü alanlar `kardes_*` prefixiyle tutulur.
- `dm_tani_tarihi`, `dm_yili` ve `hba1c` yalnız DM indeks çocuk için doludur.
- Kontrol ailelerinde, DM kardeş satırlarında ve kontrol kardeş satırlarında `dm_tani_tarihi`, `dm_yili` ve `hba1c` yapısal `NA`dır.
- Boş hücre `NA` anlamına gelir; final CSV'lerde literal `#N/A` veya `?` saklanmaz.
- Final CSV'lerde eski serbest metin alanları (`calistigi_is`, `es_calistigi_is`, `hastalik_engel`, `es_hastalik_engel`) bulunmaz.

## 9. Veri Kalitesi Kuralları

- Tarih alanları parse edilebilir `gg.aa.yyyy` formatında olmalıdır.
- `cocuk_yas`, `anne_yas`, `kardes_yas` ve `dm_yili` tarih alanlarıyla uyumlu olmalıdır.
- Cinsiyet, medeni durum, eğitim, çalışma, ev, araba, kronik hastalık ve antidepresan alanları bu belgede tanımlanan kod aralıkları dışında değer alamaz.
- `hba1c` ondalık sayı formatındadır; klinik plauzibilite aralığı `4.5 – 18.0`%; bu aralık dışı değerler veri kalitesi izlemesinde işaretlenir.
- Eski serbest metin alanları final CSV'lerde bulunmaz. Meslek ve hastalık alanları bu belgede tanımlanan nihai standardize kolonlarla temsil edilir; raw serbest metin yalnız arşiv/audit kaynaklarında izlenir.
