# Sosyoekonomik Statü (SES) Tariflemesi — Nihai Strateji

Final form yapınız bu soruya cevap vermek için gerçekten zengin bir altyapı sunuyor. Elinizdeki SES-ilişkili değişkenleri sistematik olarak değerlendirip **çalışmanız için defendable bir SES kompozit yapısı** öneriyorum.

---

## 1. Elinizdeki SES-İlişkili Değişkenler — Envanter

Final formunuzdan SES bilgisi taşıyan 9 alanı üç eksende sınıflandırıyorum (Bourdieu'nün üç sermaye türü çerçevesi + materyal koşullar):

| Alan | SES Boyutu | Boyut Ailesi | Veri Tipi | Kayıp |
|---|---|---|---|---|
| `egitim_durumu` (anne) | Beşeri/kültürel sermaye | **Eğitim** | Sıralı (0–5) | Beklenen düşük |
| `es_egitim_durumu` (baba) | Beşeri/kültürel sermaye | **Eğitim** | Sıralı (0–5) | Beklenen düşük |
| `calisma_durumu` (anne) | İşgücü statüsü | **Meslek** | İkili | Düşük |
| `es_calisma_durumu` (baba) | İşgücü statüsü | **Meslek** | İkili | Düşük |
| `es_isei08` | Mesleki konum (sürekli) | **Meslek** | Sürekli (16–90) | ~%5 |
| `es_egp7` | Mesleki sınıf (kategorik) | **Meslek** | Kategorik (7) | ~%5 |
| `es_siops08` | Mesleki prestij | **Meslek** | Sürekli (~13–78) | ~%5 |
| `ev_sahipligi` | Servet/varlık | **Materyal** | İkili | Düşük |
| `ev_oda_sayisi` | Konut kalitesi/kalabalık | **Materyal** | Sıralı (0–3) | Düşük |
| `arabaniz_var_mi` | Servet/varlık | **Materyal** | İkili | Düşük |

**Eksik olan ama olsaydı yararlı olacak değişkenler** (limitasyon bölümünde belirtilmesi gereken):
- Hane geliri (Türkiye saha çalışmalarında genellikle red oranı yüksek olduğu için doğrudan toplanmaması savunulabilir)
- Sağlık sigortası tipi (SGK / özel / yeşil kart) — sosyal güvenlik gradient'i
- Mahalle/semt SES'i (komşuluk etkisi için)

---

## 2. SES Tariflemesi — Üç Katmanlı Strateji

Tek bir "SES değişkeni" yapmaya çalışmak yerine, **üç katmanlı yaklaşım** tezinizde hem metodolojik olarak modern hem de istatistiksel olarak güçlüdür.

### Katman A — Tek Boyutlu SES Bileşenleri (boyut-spesifik analiz)

Her boyutu **ayrı kovaryat** olarak modele alın. Ne zaman: araştırma sorularınız spesifik bir kanaldan etki bekliyorsa (örn. "anne eğitimi ebeveynlik tutumlarını öngörüyor mu?").

| Boyut | Önerilen değişken | Gerekçe |
|---|---|---|
| Eğitim | `egitim_durumu` + `es_egitim_durumu` (her ikisi ayrı) ya da **`max_aile_egitim`** (ikisinin maksimumu) | Ebeveyn eğitimi çocuk gelişimi araştırmalarında en güçlü ve en az kayıplı SES proxy'sidir |
| Meslek | `aile_isei08` (sürekli) | Sosyoekonomik hiyerarşi için optimal sürekli ölçü |
| Materyal | `material_index` (aşağıda — Katman B) | 3 alanın kompoziti |

### Katman B — Materyal Varlık İndeksi (Asset Index)

DHS-Filmer-Pritchett geleneğinde, üç materyal değişkeniniz (`ev_sahipligi`, `ev_oda_sayisi`, `arabaniz_var_mi`) için **ana bileşenler analiziyle (PCA) tek bir indeks** türetilebilir. Bu, gelir verisi olmadığında SES için en yaygın kabul gören çözümdür (Filmer & Pritchett 2001; UNICEF MICS protokolü; DHS Wealth Index metodu).

```r
library(psych)

# Üç materyal değişken
material_vars <- family_data %>%
  select(ev_sahipligi, ev_oda_sayisi, arabaniz_var_mi)

# Polikorik korelasyon (karışık kategorik/sıralı için)
poly_cor <- polychoric(material_vars)$rho

# PCA (ya da uygunsa polikorik üzerinden)
pca_material <- principal(poly_cor, nfactors = 1, rotate = "none")

# Faktör skorlarını orijinal veriye uygula
material_scores <- factor.scores(material_vars, pca_material)$scores
family_data$material_index <- as.numeric(material_scores)

# Yüzdelik dilimlere böl (klasik DHS yaklaşımı):
family_data$material_quintile <- ntile(family_data$material_index, 5)
```

**Dikkat edilmesi gereken nokta — `ev_sahipligi` Türkiye bağlamında karmaşık:** Türkiye'de düşük SES haneleri çoğunlukla *kendi mülklerinde* otururken, yüksek SES profesyonel haneleri büyükşehirlerde *kiracı* konumdadır. Yani `ev_sahipligi=0 (Kendi mülkümüz)` her zaman yüksek SES anlamına gelmez. Bunu PCA loading'lerini gözden geçirerek doğrulayın; eğer ev sahipliğinin yükü ters yönde çıkıyorsa indeksten çıkarın veya bağımsız değişken olarak ayrı tutun. Bu **mutlaka denenmesi ve tezde raporlanması gereken** bir sensitivity analysis'tir.

### Katman C — Bütünleşik SES Kompoziti (genel SES gradient)

Üç boyutu (eğitim + meslek + materyal) tek bir kompozit skora indirgemek için iki yöntem var; her ikisini de denemeniz ve tutarlılığı raporlamanız önerilir:

#### Seçenek C1 — Hollingshead-tipi ağırlıklı kompozit (basit, şeffaf)

```
ses_hollingshead = w_edu * mean(egitim_durumu, es_egitim_durumu)
                 + w_occ * (aile_isei08 / 10)
                 + w_mat * material_index_z
```

Hollingshead'ın klasik ağırlıkları (1975) eğitime 3, mesleğe 5 verir; ancak modern çocuk gelişimi araştırmalarında **eşit ağırlık (z-skorların ortalaması)** daha sık tercih edilir çünkü Hollingshead orjinal ağırlıkları 1970'ler ABD verisine kalibreedir.

#### Seçenek C2 — Latent SES değişkeni (CFA temelli — yöntemsel olarak en güçlü)

```r
library(lavaan)

ses_model <- '
  SES =~ egitim_durumu + es_egitim_durumu + aile_isei08 + material_index
'

fit <- cfa(ses_model, data = family_data, estimator = "WLSMV",
           ordered = c("egitim_durumu", "es_egitim_durumu"))

# Faktör skorlarını çıkar
family_data$ses_latent <- predict(fit)
```

Bu yaklaşım Mahir, sizin örnekleminizde **241 aile için** marjinal yeterlilikle çalışır (CFA için minimum N≈200 önerilir; 4 göstergeli basit model için yeterlidir). `devstats` skill'inin kapsama alanına girer ve doktoral tez için yöntemsel sofistikasyon sağlar.

---

## 3. Hangi Yaklaşımı Önceliklendirmelisiniz?

Doktoral tezinizin yapısı (s-EMBU-C/s-EMBU-P + SRQ + Beck temelli case-control aile dizaynı) için **karma strateji** öneriyorum:

| Analiz amacı | Önerilen SES değişkeni |
|---|---|
| Tanımlayıcı istatistikler (Tablo 1 — örneklem karakterizasyonu) | Tüm bireysel boyutlar ayrı ayrı (eğitim her iki ebeveyn, çalışma durumu her iki ebeveyn, EGP-7 sınıfı, materyal indeksi quintile) |
| DM vs. Kontrol grup karşılaştırması | Ana boyutlar ayrı + bütünleşik kompozit (her ikisi raporlanır) |
| Ana ana hipotez modelleri (s-EMBU, SRQ, Beck → SES kovaryatı) | **`ses_latent` (CFA temelli)** primer; **`aile_isei08`** ve **`max_aile_egitim`** sensitivity analizinde |
| Aile-içi farklılaşma analizi (PDT/SIDE) | SES kompoziti kovaryat; ayrıca anne–baba eğitim farkı (asortatif eşleşme proxy'si) |
| Yayında (Ek Tablolar) | Bireysel boyutların korelasyon matrisi + kompozit yapı doğrulaması |

---

## 4. Pratik Öneri — Türetilecek Değişkenler

Final veri sözlüğünüze aşağıdaki türetilmiş değişkenleri eklemenizi tavsiye ederim:

| Yeni Değişken | Tip | Türetme |
|---|---|---|
| `max_aile_egitim` | Sıralı 0–5 | `pmax(egitim_durumu, es_egitim_durumu, na.rm=TRUE)` |
| `mean_aile_egitim` | Sürekli | `(egitim_durumu + es_egitim_durumu) / 2` |
| `egitim_fark` | Sürekli | `abs(es_egitim_durumu - egitim_durumu)` — asortatif eşleşme |
| `cift_kazanc` | İkili | `(calisma_durumu == 1 & es_calisma_durumu == 1)` |
| `es_emekli` | İkili | Eş/babanın emekli olduğunu gösterir; aktif çalışma ve mesleki prestijden ayrı değerlendirilir |
| `material_index` | Sürekli | PCA / polikorik PCA (Katman B) |
| `material_quintile` | Sıralı 1–5 | `material_index` quintile'ları |
| `ses_composite_z` | Sürekli | Eğitim z + ISEI z + materyal z ortalaması |
| `ses_latent` | Sürekli | CFA faktör skoru (lavaan) |
| `kalabalik_indeksi` | Sürekli | `cocuk_sayisi / (ev_oda_sayisi + 1)` — kişi başına oda |

---

## 5. Tez Metodoloji Bölümü — Savunulabilir Paragraf Taslağı

> "Sosyoekonomik statü (SES), tek boyutlu bir yapı olarak değil, üç teorik kanal (eğitim sermayesi, mesleki konum, materyal varlık) üzerinden işletildi. Eğitim sermayesi için anne ve baba eğitim durumları altı kategorili sıralı ölçekte (0=okuma bilmiyor, 5=lisansüstü) ayrı ayrı kayıt altına alındı; aile düzeyi gösterge olarak ebeveyn eğitiminin maksimumu (`max_aile_egitim`) ve ortalaması (`mean_aile_egitim`) hesaplandı. Mesleki konum için baba/eş meslek serbest metni ISCO-08 birim grubu (4-haneli) düzeyinde Codex destekli ilk kodlama ve araştırmacı karar revizyonu ile standardize edildi; ISCO-08 kodlarından ISEI-08 (sürekli sosyoekonomik indeks), SIOPS-08 (prestij) ve EGP-7 (sınıf kategorisi) türetildi. Emekli eş/baba aktif çalışan olarak değerlendirilmedi; `es_emekli` ayrı bir gelir güvencesi bayrağı olarak tutuldu ve emekli satırlarında mesleki prestij/ISEI puanı türetilmedi. Anne mesleği yüksek item-nonresponse oranı nedeniyle SES gradient değişkenine dahil edilmedi; bu durum Türkiye'deki düşük kadın işgücüne katılımı bağlamında beklenen bir sınırlılıktır. Materyal varlık için ev sahipliği, oda sayısı ve araç sahipliği değişkenleri polikorik korelasyon matrisi üzerinden temel bileşenler analizi (PCA) ile tek bir materyal indeksine indirgendi (Filmer & Pritchett 2001 metodolojisine uygun olarak). Bütünleşik SES değişkeni olarak hem (a) eğitim, ISEI-08 ve materyal indeksinin standardize edilip ortalanmasıyla elde edilen Hollingshead-tipi şeffaf kompozit, hem de (b) WLSMV tahmincisi kullanılan doğrulayıcı faktör analiziyle (CFA) elde edilen latent SES skoru hesaplandı. Ana hipotez analizlerinde latent SES skoru kullanıldı; sensitivity analizleri her iki kompozitin sonuçlarının tutarlılığını doğruladı."

---

## 6. Limitasyon Cümlesi (savunma açısından kritik)

> "Bu çalışma hane gelir bilgisini doğrudan toplamamıştır; Türkiye saha çalışmalarında gelir sorularının yüksek red ve yanılgı oranları nedeniyle güvenilirliği düşüktür. Bunun yerine meslek-temelli ISEI-08 ve materyal varlık indeksi kullanılmıştır. Emekli eş/baba için aktif meslek prestiji türetilmemiş, emeklilik ayrı bir sabit gelir/güvence bayrağı olarak korunmuştur. Anne meslek bilgisi yüksek nonresponse nedeniyle SES kompozitine dahil edilememiş; bu durum, Türkiye'de kadın işgücüne katılımının düşüklüğü ve veri toplama protokolünün ev hanımı statüsündeki kadınlara yönelik standardize edilmemiş olmasından kaynaklanmaktadır."

---

## 7. Bir Tavsiye — DM Grubunun Özel Durumu

Mahir, gözden kaçırmamanız gereken bir nokta: Çalışmanız case-control (DM-Kontrol) tasarımında, **SES'in bir kovaryat değil, potansiyel bir confounder** olduğunu hatırlayın. Tip 1 DM Türkiye'de SES gradient göstermezken (otoimmün etiyoloji, sosyal sınıfa görece nötr), Tip 2 DM ve sağlık hizmetlerine erişim SES ile sıkı ilişkilidir. DM tanı yaşı / `dm_yili` ile SES değişkenlerinin korelasyonunu Tablo 1'de raporlamanız ve eğer anlamlıysa SES için propensity score adjustment (case-control matching kalitesini doğrulamak için) düşünmeniz savunulabilir bir adımdır.
