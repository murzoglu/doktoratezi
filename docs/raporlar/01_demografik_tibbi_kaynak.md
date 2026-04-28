# T1DM-EBEVEYN Çalışması — Demografik ve Tıbbi Bilgiler Bütünleşik Raporu

## Yönetici Özeti

Marmara Üniversitesi SBE Sosyal Pediatri doktora tezi kapsamında yürütülen
T1DM-EBEVEYN çalışması, Tip 1 diyabet (T1DM) tanılı çocuklar, sağlıklı
kardeşleri ve anneleri ile sağlıklı kontrol grubu arasında ebeveynlik tutum
örüntülerini incelemektedir. Bu rapor, çalışmanın demografik ve tıbbi bilgiler
katmanından elde edilen bulguları SAP v3.0 KISIM II-III ve KISIM X kapsamında
birleştirir.

Toplam 241 aile dahil edilmiştir: 120 DM ve 121 sağlıklı kontrol ailesi.
Her aileden 1 anne, 1 indeks çocuk ve 1 kardeş katılımı sağlanarak 482 çocuk
satırı uzun-format kanonik tabana yazılmıştır. Veri kilidi
FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock dosyasında SHA-256 hash kontrolü
ile sabitlenmiştir.

DM ve kontrol grupları çoğu sosyodemografik değişkende dengelidir. Ham
gözlemde 4 değişkende dengesizlik tespit edilmiştir: anne antidepresan
kullanımı SMD = 0.53 (ciddi dengesizlik), eş eğitim durumu SMD = 0.32, anne
eğitim durumu SMD = 0.29, aile ve eş ISEI mesleki indeksleri SMD = 0.23.
Bu dengesizlikler DAG temelli birincil ayarlama seti ve propensity-temelli
stabilize IPTW ağırlıklamasıyla kontrol edilmiştir; ham SMD maksimumu
0.220 düzeyinden 0.004 seviyesine düşürülmüştür.

DM grubunda HbA1c verisi yalnızca 39 aile (%32.5) için mevcuttur. Klinik
biyobelirteç imputasyona alınmaz; KISIM X HbA1c × ebeveynlik etkileşimi
keşifsel etiketle yürütülmüştür. Tanı yaşı medyanı 7.8 yıl, DM süresi
medyanı 3.9 yıldır. Bu profil, çoğunlukla okul çağında tanı almış ve orta
süreli kronik bakım deneyimi olan ailelerin örneklenmiştir.

## Bölüm 1 — Örneklem ve Aile Yapısı

Çalışmaya 241 aile dahil edilmiştir. Aile yapısı her grupta tutarlıdır:
DM grubunda 120 aile, kontrol grubunda 121 aile. DM grubu için indeks çocuk
T1DM tanısı taşıyan çocuktur; kardeş ise sağlıklı bir biyolojik kardeştir.
Kontrol grubunda hem indeks hem kardeş sağlıklıdır. Toplam 482 çocuk satırı
uzun-format kanonik tabana yazılmıştır.

Çocuk yaşı medyanı kontrol grubunda 11.2 yıl, DM grubunda 12.0 yıl
düzeyinde olup gruplar arasında fark anlamsızdır (SMD = 0.07).
Çalışma protokolü 7-17 yaş aralığını dahil etme kriteri olarak
sabitlemiştir. Kardeş yaş farkı medyanı 3.0 yıl olup pozitif ve negatif
yönde simetrik dağılım göstermiştir. Cinsiyet dağılımı dengelidir: indeks
çocuk Kız oranı kontrol %48, DM %52; kardeş Kız oranı kontrol %50, DM %48.
Aynı cinsiyet kardeş çifti oranı kontrol grubunda %42, DM grubunda %44
düzeyindedir, gruplar arası fark sınır altıdır (SMD = 0.03).

Aile büyüklüğü ortalaması 2.4 çocuk olup grup bazında değişmemektedir.
2 çocuklu aileler en sık raporlanan aile yapısıdır (oran %63). 3+ çocuklu
ailelerde anne-çocuk-kardeş üçlüsü için indeks ile en yakın yaşlı kardeş
seçilmiştir.

## Bölüm 2 — Anne Demografik ve Klinik Profili

DM grubunda anneler kontrol grubuna göre yaklaşık 1 yıl daha yaşlıdır.
Anne yaşı medyanı kontrol grubunda 37.3 yıl, DM grubunda 38.5 yıl
düzeyindedir (SMD = 0.21, dengesiz eşiği). Bu fark KISIM III propensity
ayarlamasında kovaryat olarak yer alır.

Anne Beck Depresyon Envanteri toplam puanı 5 kategoriye ayrılmıştır:
minimal (0-9), hafif (10-16), orta (17-20), şiddetli (21-30) ve çok
şiddetli (≥31). Beck şiddet kategorisi grup bazında dengelidir
(SMD = 0.11, sınırda). Toplam puan ortalama 6.8 olup minimal kategoride
yoğunlaşma göstermiştir.

Anne antidepresan kullanım oranı çalışmadaki en güçlü dengesizliktir.
DM grubunda anne antidepresan kullanım oranı %29 iken kontrol grubunda
%9 düzeyindedir. SMD = 0.53 ciddi dengesizlik eşiğinin üzerindedir; bu,
DM grubu kontrol grubundan yaklaşık 3.2 kat yüksek antidepresan kullanım
oranına işaret eder. H3 anne öz-rapor analizinde stratifiye duyarlılık
zorunluluğu burada doğrulanmaktadır (SAP v3.0 KISIM V/14.2). Bulgu,
kronik hastalık çocuklu annelerin yüksek psikiyatrik bakım yüküne
işaret etmekte, klinik perinatal psikiyatri tarama programlarının T1DM
bakım hizmetine entegre edilmesini önermektedir.

Anne kronik hastalık varlığı SMD = 0.11 sınırda; eş çalışma durumu
SMD = 0.14 sınırda; her iki değişken kovaryat olarak ayarlama setinde yer alır.

## Bölüm 3 — Sosyoekonomik Durum (SES) Kompoziti

Sosyoekonomik durum üç katmanlı kompozit hat ile türetilmiştir.
Birinci katman eğitim göstergesi (anne ve eş eğitim seviyesi 1-6 ordinal),
ikinci katman ISEI-08 mesleki indeksi (anne ve eş için ayrı), üçüncü
katman materyal varlık göstergesi (ev sahipliği, araba sahipliği, ev oda
sayısı, kalabalık indeksi). Üç katman polychoric PCA + CFA latent skor
formülasyonuyla `ses_latent` z-standardize değişkenine dönüştürülmüştür.

Eğitim göstergeleri ham gözlemde dengesizlik göstermiştir. Anne eğitim
durumu SMD = 0.29, eş eğitim durumu SMD = 0.32 düzeyindedir; her ikisi
de dengesiz eşiğindedir. ISEI-08 mesleki indeksi için aile ve eş
SMD = 0.23 düzeyindedir. Bu üç dengesizlik DAG-justified ayarlama
setinde latent SES kompoziti üzerinden kontrol edilmiştir.

Latent SES kompoziti grup bazında dengelidir (SMD = 0.03, iyi denge
eşiğinde). Bourdieu üç-sermaye çerçevesi (kültürel, ekonomik, sosyal
sermaye) latent kompoziti şekillendirmiştir; H3 anne öz-rapor analizinde
birincil kovaryat olarak kullanılır. Hollingshead alternatif kompoziti
duyarlılık analizi olarak raporlanır.

## Bölüm 4 — DM Klinik Profili

DM grubu için 120 aile için klinik veriler toplanmıştır. Klinik gösterge
veri tamamlanma profili dengesizdir: DM süresi (dm_yili) ve tanı yaşı
(tani_yasi) için %100 tamamlanma sağlanmışken, HbA1c yalnızca 39 aile
(%32.5) için mevcuttur. Bu, çalışmanın güç kısıtlamasıdır.

HbA1c medyanı 9.0% (IQR 7.3-9.6) düzeyindedir. ISPAD 2022 hedef eşiği
olan 7.0% değerinin oldukça üzerindedir. Hedefte (<7%) olan aile oranı
%18, hedef üstü (7-9%) %33, yüksek risk (>9%) %49 düzeyindedir. Bu
profil, çalışma örnekleminin glisemik kontrol açısından ortalama düzeyin
altında bir bakım kalitesine sahip olduğunu göstermektedir. Klinik
biyobelirteç imputasyona alınmaz (kural #19); KISIM X HbA1c × ebeveynlik
etkileşim analizi keşifsel etiketle yürütülmüş ve güç sınırlamasıyla
yorumlanmıştır.

DM süresi medyanı 3.9 yıl, çeyrekler arası aralık 2.0-6.2 yıl. DM süresi
spline modellemesinde cubic vs. lineer regresyon LRT karşılaştırması beş
outcome için linear sufficient sonucunu vermiştir; bu, DM süresinin
ebeveynlik tutum yordayıcısı olarak kalıcı doğrusal bir etki gösterdiğini
düşündürmektedir.

Tanı yaşı medyanı 7.8 yıl, çeyrekler arası aralık 5.7-9.3 yıl. Tanı yaşı
3 strataya ayrılmıştır: erken (<5 yaş), okul (5-10 yaş), ergen (≥10 yaş).
Erken strata 22 aile, okul strata 64 aile, ergen strata 34 aile içerir.
Strata analizi ANOVA F testi ile yürütülmüş; hiçbir outcome'da F testi
anlamlılığa ulaşmamıştır (en büyük F = 2.05, p = 0.13, sıcaklık alt
ölçeğinde). Eta-partial < 0.04 düzeyindedir. Bulgu, tanı yaşının
ebeveynlik tutum yordayıcısı olarak ayrımlaştırıcı olmadığını,
güç kısıtlamasıyla yorumlanması gerektiğini önermektedir.

## Bölüm 5 — Tablo 1 ve Kovaryat Dengesi

Tablo 1, 18 başlangıç sosyodemografik ve klinik değişkenini grup bazında
medyan/çeyrek ve sayı/yüzde formatında raporlar. Standardize edilmiş
ortalama farkı (SMD) Austin 2009 eşikleri ile yorumlanmıştır:
|SMD| < 0.10 iyi denge, 0.10-0.25 sınırda, 0.25-0.50 dengesiz,
≥ 0.50 ciddi dengesizlik.

Ham gözlemde 1 değişken ciddi dengesizlik (anne antidepresan), 5 değişken
dengesiz, 6 değişken sınırda, 6 değişken iyi denge kategorisindedir.
Eylem planı SMD eşiğine göre belirlenir: ciddi dengesizlik için stratifiye
duyarlılık zorunlu, dengesiz için IPTW ve kovaryat ayarı, sınırda için
kovaryat olarak ayarla, iyi denge için standart analiz yeterlidir.

Causal DAG temelli birincil ayarlama seti `{ses_latent, age_gap,
cocuk_sayisi}` olarak sabitlenmiştir. Mediator/duyarlılık kovaryatları
(Beck depresyon skoru, EMBU-P alt ölçekleri, anne antidepresan)
total-effect modellerinde ayarlanmaz; aracılık (KISIM VI) ve duyarlılık
(KISIM XI sensemakr) hatlarında ayrıca işlenir.

Propensity score (PS) hattı `group_dm ~ ses_latent + age_gap +
cocuk_sayisi` lojistik modeli ile tahmin edilmiştir. PS ortalama 0.498,
standart sapma 0.055 düzeyindedir; common support bandı 0.39-0.67 olup
4 aile bant dışında kalmıştır. Stabilize IPTW 99. persentilde trimlenmiş
ve dengeleme uygulanmıştır. IPTW sonrası maksimum |SMD| 0.004 düzeyine
düşmüştür; bu, DAG-justified ayarlama setinin başarılı dengeleme
sağladığını gösterir. Doubly-robust ANCOVA + IPTW H3 birincil hattında
raporlanır.

## Bölüm 6 — Eksik Veri Yönetimi

Aile düzeyi 241 satır üzerinde eksik veri profili karakterize edilmiştir.
HbA1c değişkeni DM grubunda %67.5 eksik (39/120 mevcut), kontrol grubunda
%100 eksik olup tasarım kaynaklı yapısal eksikliktir. Kontrol grubunda
HbA1c ölçülmediği için bu eksiklik MCAR/MAR/MNAR ekseninin dışındadır
ve imputasyona alınmaz (kural #19).

Diğer aile-düzeyi sosyodemografik değişkenlerde eksik oran düşüktür.
ISEI mesleki indeksi 22 aile (%9.1) için eksik, materyal varlık
göstergeleri 1 aile (%0.4) için eksiktir. Bu eksikler MAR varsayımı
altında üç katmanlı çerçevede işlenir: birincil FIML (lavaan WLSMV
estimator), birincil çoklu atama (mice m=50, maxit=30), ve tamamlanmış
durum analizi (sensitivity için).

NMAR delta-adjustment grid duyarlılığı her birincil hipotez için
hesaplanır. Delta parametresi -1, 0, +1 düzeylerinde değerlendirilerek
imputasyon sonuçlarının NMAR mekanizmaya karşı sağlamlığı raporlanır.
Ham complete-case analizleri bilgi kaybını göstermek için ek olarak
yürütülür; birincil yorum MI/FIML çıktısına dayanır.

## Bölüm 7 — Bulgu Sentezi ve Sonraki Adımlar

Çalışmanın demografik ve tıbbi bilgiler katmanı sekiz ana bulguyu
desteklemektedir. Aile yapısı 241 aile = 120 DM + 121 Kontrol olup aile
içi multilevel model zorunluluğu ortaya konmuştur. Yaş ve cinsiyet
bileşenleri grup bazında dengelidir; yalnız anne yaşı SMD = 0.21 ile
dengesiz eşiğindedir. Anne ruh sağlığı eksenınde anne antidepresan
SMD = 0.53 ciddi dengesizlik göstermiştir. SES bileşenleri ham gözlemde
dengesizlik gösterirken latent SES kompoziti dengelidir. DM klinik
profilinde HbA1c medyan 9.0% ile ISPAD hedefin üzerindedir, %32.5
tamamlanma ile keşifsel analiz sınırlamaları geçerlidir. DM süresi
ve tanı yaşı strata farkları ebeveynlik tutum yordayıcısı olarak
ayrımlaştırıcı bulunmamıştır. Kovaryat dengesi maksimum |SMD| 0.220
ham gözlemden 0.004 IPTW sonrasına düşmüştür. Eksik veri stratejisi
HbA1c yapısal eksiklik + sosyodemografi MAR/MI(m=50)/FIML üç katmanlı
çerçevede yürütülür.

Sonraki adımlar olarak psikometrik validasyon (KISIM IV) ayrı dokümanda
raporlanmıştır: EMBU-P/C 4-faktör WLSMV CFA, Beck tek-faktör/iki-faktör,
KİA 4-faktör, omega ve alfa güvenirlik, ölçüm değişmezliği. Birincil
hipotez testleri (KISIM V) H1 çocuk algısı multilevel ANCOVA, H2 kardeş
ilişkisi APIM + Olsen-Kenny dyadic CFA, H3 anne öz-rapor ANCOVA + IPTW +
antidepresan stratifikasyon, H4 Beck → EMBU-P latent SEM (WLSMV) ve
H5 anne ↔ çocuk diadik tutarlılık (5 paralel strateji — birincil yenilik)
olarak yürütülmektedir. Genişletilmiş analiz katmanları (KISIM VI-X)
mediation, latent profil analizi, network, klinik fayda, DM-only
alt-analizleri içerir. Sensitivite üçlüsü (KISIM XI) multiverse + TOST +
sensemakr + negative control + falsification çerçevesinde yürütülür.
Bayesian paralel hat (KISIM XII) brms + Pinquart prior + Savage-Dickey
BF dual reporting standardındadır.
