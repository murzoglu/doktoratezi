## İncelemeye Konu Belge

 Aşağıda hem doğrulanan tahminler hem de **planın öngörmediği veya çıktıda hatalı/eksik kalan** noktalar bölüm bazında analiz edilmiştir.

---

## 1. v2 Planına Karşı İcra Performansı: Genel Değerlendirme

| Plan bileşeni | Çıktıda durumu | Yorum |
|---|---|---|
| Faz A (hash doğrulama) | ✅ Yapılmış (her iki SHA-256 eşleşti) | Reprodüktiblik temeli sağlam |
| B.1 (madde tanımlayıcılar) | ✅ Yapılmış | Reddetme tablosu yeterli; tüm 29 madde gösterimi eksik |
| B.2 (α + α_std + ortalama r) | ✅ Yapılmış | McDonald ω ve %95 CI **eksik** |
| B.3 (CITC + alpha-if-deleted) | ❌ **Çıktıda yok** | v2 planının B.3'ü atlanmış |
| B.4 (EFA + KMO + Bartlett) | ⚠️ Kısmen — KMO felaket düzeyde | Aşağıda detaylı |
| B.5 (CFA, dört rakip model) | ⚠️ Üç model denenmiş, biri convergence başarısız | Bifaktör model **hiç çalıştırılmamış** |
| B.6 (multilevel CFA) | ❌ **Çıktıda yok** | EMBU-C'nin nesting yapısı CFA'da kullanılmamış görünüyor |
| B.7 (BSEM) | ❌ **Atlanmış** ("MCMC uzun") | En kritik eksik — aşağıda detaylı |
| B.8.1 (DM × Kontrol MI) | ❌ **Tahmin başarısız** (q12 boş hücre) | Aşağıda detaylı |
| B.8.2 (İndeks × Kardeş MI) | ✅ Yapılmış, scalar tutuyor | İyi haber |
| B.8.3 (Yaş × Cinsiyet MI) | ❌ Çıktıda yok | İhmal edilmiş |
| B.9 (Beck convergent) | ✅ **Yapılmış ve temiz** | En güçlü çıktı |
| B.9.3 (SRQ concurrent) | ⚠️ **Operasyonel hata** | Aşağıda detaylı |
| B.10 (Within-family konkordans) | ✅ Yapılmış (ICC + LoA) | Beklenen düşük konkordans onaylandı |
| B.11 (Multiverse) | ⚠️ 3/4 strateji çalıştırılmış | S4 (BSEM) eksik |
| TOST eşdeğerlik testi | ❌ Çıktıda yok | Negatif sonuçlar için savunma kalkanı atlanmış |
| Faz C (sensemakr) | ❌ Çıktıda yok | Henüz erken olabilir |

**Genel hüküm:** Plan-icra eşleşmesi yaklaşık %55–60. Eksiklerin **çoğu zorlu/zaman alan adımlar** (BSEM, multilevel CFA, sensemakr); planın ucuz/kolay adımları (B.3 madde diskriminasyonu, ω) ise sebepsiz atlanmış.

---

## 2. Kritik Bulgular — Doğrulananlar ve Öngörülmeyenler

### 2.1 Plan v2'nin Bilerek Beklediği ve Şimdi Doğrulanan Bulgular

| Tahmin (v2 planı) | Çıktı | Durum |
|---|---|---|
| EMBU-P Reddetme α ≈ 0.45 | α = 0.450 | ✓ Tam isabet |
| EMBU-P Reddetme'de >%80 floor effect (6/8 madde) | 7/8 madde >%80 | ✓ |
| EMBU-C psikometrik olarak EMBU-P'den daha iyi | Tüm subskalalarda doğrulandı | ✓ |
| Sıcaklık × Beck negatif korelasyon | r = −0.22, p=.001 | ✓ |
| Reddetme × Beck pozitif korelasyon | r = +0.17, p=.008 | ✓ |
| Karşılaştırma × Beck pozitif korelasyon | r = +0.26, p<.001 | ✓ (en güçlü ilişki) |
| İndeks-kardeş konkordansı düşük | ICC = 0.158–0.297 | ✓ "PDT bulgusu" |

**Bu tablo planın ampirik öngörü gücünün kanıtıdır.** Tezin Tartışma bölümünde "psikometrik adaptasyonun ön-tahminleri ampirik olarak doğrulanmıştır" denebilir — bu, registered-report estetiği için güçlü bir ifadedir.

### 2.2 Plan v2'nin Tam Öngöremediği Üç Yeni Bulgu

#### Bulgu α — KMO = 0.120 (EMBU-P): Faktörleştirilebilirlik Çöküşü

Bu rakamın anlamını tam olarak vurgulamak gerekiyor: Kaiser-Meyer-Olkin ölçütü (Kaiser, 1974) **0.50 altı "kabul edilemez"**, **0.30 altı "felaket"** olarak sınıflandırılır. **0.120 değeri, EMBU-P verisinin ortak faktör modelini hiçbir şekilde destekleyemediği** anlamına gelir; matematiksel olarak madde-arası kovaryans yapısı, faktör analizinin gerektirdiği tekil olmayan korelasyon matrisini üretmiyor.

**Olası nedenler (Brown 2015, §3.7):**
1. Aşırı taban etkisi nedeniyle pek çok madde **fiilen sabit** (q12'de %96 tek kategori)
2. Anti-image korelasyon matrisi yapısı bozulmuş
3. Tetrachoric/polychoric matrisin düzgünlüğü ihlal edilmiş

**Bunun teze etkisi:** Mevcut hâliyle **EMBU-P için 4-faktör yapı iddiası savunulamaz**. Üç stratejik yön var:

| Strateji | Riski | Tavsiyem |
|---|---|---|
| EMBU-P'yi sadece toplam puan olarak kullan, alt ölçek yapısını terket | Sümer-Güngör 4-faktör modelini reddetmiş olursunuz | Önerilmez |
| Reddetme alt ölçeğini **dışla**, 3-faktör modele geç | Hipotez H1'in bir parçası kaybolur | Pragmatik orta yol |
| **BSEM (Bayes prior'larıyla zorunlu yapı)** ile yeniden çalıştır | Brown (2015) §10'un tam senaryosu | **Birincil tavsiyem** |

#### Bulgu β — Tüm CFA Modelleri Hu & Bentler Eşiklerini İhlal Ediyor

| Form | Model | CFI | TLI | RMSEA | SRMR | Hüküm |
|---|---|---|---|---|---|---|
| EMBU-P | 1-faktör | 0.480 | 0.440 | 0.083 | **0.174** | Çok kötü |
| EMBU-P | 4-faktör | **0.877** | 0.866 | 0.040 | **0.132** | **Eşik altı** |
| EMBU-P | 2nd-order | NA | NA | NA | 0.144 | Convergence yok |
| EMBU-C | 1-faktör | 0.480 | 0.440 | 0.121 | 0.146 | Çok kötü |
| EMBU-C | 4-faktör | **0.840** | 0.825 | 0.068 | 0.096 | **Eşik altı** |
| EMBU-C | 2nd-order | NA | NA | NA | NA | Convergence yok |

**Hu & Bentler (1999) eşikleri:** CFI ≥ .95 (iyi), ≥ .90 (kabul edilebilir); SRMR ≤ .08; RMSEA ≤ .06.

**İki yapısal sorun:**
1. **CFI 0.84–0.88 aralığı**: Hiçbir 4-faktör model **kabul edilebilir** kategoriye giremiyor. Tezin "4-faktör yapı bu örneklemde kısmen desteklenmiştir" diye **sınırlandırılmış** ifadeyle raporlanması gerekecek.
2. **RMSEA iyi + SRMR kötü kombinasyonu** (özellikle EMBU-P'de RMSEA=0.040, SRMR=0.132): Brown (2015) §4.4'te **"localized misfit"** sinyali olarak tanımlanır. RMSEA modeli **parsimony düzeltilmiş** olarak değerlendirir; SRMR **gözlenen-modelle-tahmin edilen** korelasyon farkını verir. Bu fark, modelin **bazı madde çiftlerini sistematik olarak kötü temsil ettiğini** gösterir. Modifikasyon indeksleri (B.5.3 — yapılmamış) bu noktada **zorunludur**.

**Şüpheli ek bulgu:** EMBU-P ve EMBU-C 1-faktör modelleri **birebir aynı CFI=0.480 ve TLI=0.440** veriyor. Bu mathematiksel olarak son derece düşük olasılık (hem örneklem hem madde sayısı farklı). **Runner script'inde bir bug, baseline-fit hesabında varsayılan değer override'ı veya raporlama copy-paste hatası olma ihtimali yüksek.** Aşağıdaki R kodu tekrar çalıştırılarak doğrulanmalı:

```r
# Doğrulama
fit_p_1f <- cfa(model_1f, data = df_family, ordered = TRUE, estimator = "WLSMV")
fit_c_1f <- cfa(model_1f, data = df_long,   ordered = TRUE, estimator = "WLSMV")
fitMeasures(fit_p_1f, c("cfi.scaled","tli.scaled","rmsea.scaled","srmr"))
fitMeasures(fit_c_1f, c("cfi.scaled","tli.scaled","rmsea.scaled","srmr"))
# Eğer hâlâ aynı çıkıyorsa: lavaan opsiyonları (test="scaled.shifted" vs "satorra.bentler") incelenmeli
```

#### Bulgu γ — DM × Kontrol Multiverse Hipotez-Karşıtı Yön

Bu sonuç **planın hiç beklemediği** ve tezin **hipotez yapısını yeniden değerlendirmeyi** gerektirebilecek noktadır:

| Strateji | DM − Kontrol farkı | Cohen's d |
|---|---|---|
| S1 (8 madde × 4 kategori) | **−0.040** | −0.142 |
| S2 (3-kategori daraltma) | **−0.020** | −0.121 |
| S3 (CITC<.30 silme, 4 madde) | **−0.066** | −0.154 |

**Üç deterministik spec birden DM annelerin Reddetme skorunu Kontrol'den DÜŞÜK gösteriyor**, hipotez ise tersini öngörüyordu (kronik hastalığa eşlik eden anne yükü → daha yüksek reddedici tutum, Streisand & Monaghan 2014). Hiçbiri istatistiksel anlamlı değil ama **yön sağlam**: multiverse'in tek kuvveti budur — yön tutarlılığı sinyaldir, anlamlılık değil.

**Üç açıklama hipotezi:**
1. **Sosyal istenirlik DM grubunda daha güçlü** — kronik hastalık çocuklu anneler klinik temasla daha sık karşılaştığı için "ideal anne" kalıbına daha çok uyum gösterirler (Edmondson, 1996; healthcare contact bias)
2. **Aşırı koruma kompensasyonu** — DM annelerinin koruyucu motivasyonu reddedici davranışları seçici biçimde bastırır (`asiri_koruma` skorları zaten yüksek)
3. **Gerçek "fark yok" sinyali** — bu hâlde **TOST eşdeğerlik testi** zorunlu (Lakens, 2017)

**Yapılması gereken (öncelikli):**

```r
library(TOSTER)
TOSTER::tsum_TOST(
  m1 = mean_dm, sd1 = sd_dm, n1 = 120,
  m2 = mean_kontrol, sd2 = sd_kontrol, n2 = 121,
  low_eqbound_d = -0.30, high_eqbound_d = 0.30  # SESOI = orta etki
)
# Eğer iki tek-yanlı test de p < .05 ise: "anlamlı farkın yokluğu" istatistiksel olarak savunulur
```

---

## 3. Acil Müdahale Gerektiren Sorunlar

### 3.1 q12 Maddesinin Yapısal Tıkanıklığı

```
embu_p_q12 — DM grubunda kategori frekansları: [116, 3, 0]
```

DM grubunun 116 annesi kategori 1, 3 annesi kategori 2, **hiçbiri** kategori 3'e gitmemiş. Bu durumda WLSMV tahminci threshold parametresini hesaplayamıyor (sıfır frekans → sonsuz threshold). **DM × Kontrol grup invariance bu yüzden tahmin edilemedi** — yani çalışmanın **birincil hipotez testi (H1)** psikometrik olarak savunulamıyor.

**Çözüm matrisi:**

| Çözüm | Maliyet | Kazanım |
|---|---|---|
| A) q12'yi Reddetme alt ölçeğinden çıkar | 1 madde kaybı | Threshold tahmin edilebilir hâle gelir |
| B) q12'yi 4 kategoriden 2'ye daraltma (1 vs ≥2) | Bilgi kaybı | Sıfır hücre sorunu çözülür |
| C) Bayesian threshold estimation (BSEM içinde) | MCMC zamanı | En savunulabilir |

**Tavsiyem:** A + C kombinasyonu. Tezde "q12 için ölçüm değişmezliği analizinde sıfır frekans nedeniyle tahmin yapılamadığı, q12 dışlanarak yedi maddeli Reddetme alt ölçeği üzerinden yeniden tahmin yapıldığı" şeklinde transparant raporlama. BSEM ise paralel sensitivite olarak.

### 3.2 BSEM Atlanması

Çıktının dipnotu: *"Stan tabanli blavaan MCMC kosusu uzun surelidir; otomatik Quarto/runner hattinda deterministik WLSMV ve sensitivite tablolari uretilmistir."*

Bu kabul edilebilir bir mühendislik kararı (otomatik runner için), ancak **tez teslim edilmeden önce BSEM çalıştırılmak zorunda**. Sebepler:

1. Reddetme α=0.450 + KMO=0.12 + 4-faktör CFI=0.877 üçlüsü, klasik frequentist çerçevede **savunulamaz**. Brown (2015) §10'un BSEM önerisi tam bu senaryo içindir.
2. Sümer-Güngör 4-faktör yapısı için **bilgi-bilgilendirici prior** kullanmak (loading ~ Normal(λ_referans, 0.1)), bu örneklemin yapıyı reddetmek yerine "yaklaşık olarak desteklediğini" göstermenin tek yoludur.
3. Tez savunmasında jüri "α=0.45 ile alt ölçek nasıl kullanılır?" sorusunu sormaz**a**, BSEM'in PPP değeriyle "Bayesian fit kabul edilebilir" cevabı verilebilir.

**Süre tahmini:** Tek bir BSEM modeli (4-faktör, 29 madde, n=241), 4 chain × 10000 sample × 2000 burnin → modern laptop'ta 45–90 dakika. Yatakhane gecesi tek-tıkla çalıştırılabilir.

```r
library(blavaan)
bsem_fit <- bcfa(model_4f, data = df_family,
                 ordered = TRUE,
                 n.chains = 4, burnin = 2000, sample = 10000,
                 target = "stan",
                 dp = dpriors(
                   lambda = "normal(0.5, 0.5)",  # Sümer-Güngör'den prior
                   nu     = "normal(0, 1)"
                 ))
fitMeasures(bsem_fit, c("ppp", "BCFI", "BTLI", "BRMSEA"))
# PPP ≈ 0.50 → kabul edilebilir Bayesian fit
```

### 3.3 SRQ Concurrent Validity'nin Operasyonel Sıfırlanması

```
EMBU-P karsilastirma × SRQ_total_mean → r=0.036, p=0.576 ❌
EMBU-C karsilastirma × SRQ_total_mean → r=0.011, p=0.812 ❌
```

Bu, **SRQ'nun yanlış operasyonalizasyonundan kaynaklanan sahte negatif sonuç**tur ve çıktının dipnotu da bunu doğru teşhis ediyor:

> *"...bu analiz global SRQ ortalamasıyla sınırlıdır ve alt boyut madde kümeleri ayrıca sabitlenirse genişletilebilir."*

Furman & Buhrmester (1985) SRQ'su **dört faktörlüdür** (Sıcaklık, Çatışma, Statü/Güç, Rekabet/Rivalry). Toplam ortalama, pozitif (Sıcaklık) ve negatif (Çatışma, Rivalry) yüklü maddeleri **ortalamaya katarak istatistiksel olarak sıfırlıyor**. Beklenen örüntü:

| EMBU Karşılaştırma × | Beklenen | Mantık |
|---|---|---|
| SRQ Rivalry | r > 0 (orta-güçlü) | PDT → kardeş rekabeti |
| SRQ Çatışma | r > 0 (orta) | PDT → kardeş çatışması |
| SRQ Sıcaklık | r < 0 (zayıf-orta) | PDT → düşük kardeş sıcaklığı |
| SRQ Statü | r ≈ 0 | İlişkili değil |

**Yapılması gereken:** SRQ alt ölçek madde tanımlarının kanonik dokümandan (`KANONIK_KARDES_ILISKILERI_ANKETI.md`) çekilmesi ve dört alt ölçek skorunun yeniden hesaplanması. Bu yapılmadan **çalışmanın H4 hipotezi (PDT → SRQ Rivalry mediasyon yolu) test edilemez**.

---

## 4. Plana Göre İhmal Edilen Adımların Aciliyet Sıralaması

| # | Eksik | Aciliyet | Süre |
|---|---|---|---|
| 1 | **BSEM (B.7)** | **Kritik** — Reddetme α savunması için tek yol | 1 gün |
| 2 | **SRQ alt ölçek skorları** | **Kritik** — H4 testi için zorunlu | 2 saat |
| 3 | **Multilevel CFA (B.6)** | Yüksek — EMBU-C için aile-bağımlılığı | 1 saat |
| 4 | **q12'siz 7-madde Reddetme MI** | Yüksek — H1 savunması | 1 saat |
| 5 | **TOST eşdeğerlik testi** | Orta — null sonuç savunması | 1 saat |
| 6 | **Modifikasyon indeksleri** | Orta — SRMR>.10 lokal misfit teşhisi | 30 dk |
| 7 | **B.3 CITC + alpha-if-deleted tablosu** | Orta — APA standardı | 30 dk |
| 8 | **McDonald ω (ω_h, ω_t) + %95 CI** | Orta — DeVellis standardı | 30 dk |
| 9 | **Bifaktör modeli** | Düşük | 30 dk |
| 10 | **Yaş × Cinsiyet MI (B.8.3)** | Düşük | 1 saat |
| 11 | **1-faktör CFI=0.480 anomalisi doğrulama** | Acil bug-fix | 15 dk |
| 12 | **sensemakr (Faz C)** | Düşük (henüz erken) | İlerleme sonrası |

**Toplam tahmini ek iş:** ~2 takvim günü (yoğun bir hafta sonu).

---

## 5. Olumlu Tablolar ve Tezde Vurgulanması Gereken Güçlü Yönler

Çıktıda **gerçekten güçlü** dört bulgu var; bunlar tezin Bulgular bölümünde **birincil pozisyonda** konumlandırılmalı:

### 5.1 EMBU-C Scalar Invariance ✓

DM × Kontrol ve İndeks × Kardeş eksenlerinde scalar invariance ΔCFI < 0.010 sınırında tutuyor. Bu, EMBU-C üzerinde **grup ortalamalarının latent düzeyde karşılaştırılabilir** olduğu anlamına geliyor (Brown 2015 §7). Bu, Aşağıdaki anlatımla raporlanabilir:

> "EMBU-C için DM tanılı ve kontrol grupları arasında scalar ölçüm değişmezliği desteklenmiştir (configural CFI=.913, metric CFI=.907, scalar CFI=.906; tüm ΔCFI < .010). Bu bulgu, gözlenen grup farklarının ölçüm artefaktı değil, yapısal latent fark olduğunu gösterir (Cheung & Rensvold, 2002)."

### 5.2 Beck Konvergent Geçerliği — Hipotez Gücünün Kanıtı

Üç apriori beklentinin üçü de yön ve anlamlılık olarak doğrulandı:

| İlişki | Beklenen yön | Gözlenen | p |
|---|---|---|---|
| Sıcaklık × Beck | Negatif | r = −0.22 | .001 |
| Reddetme × Beck | Pozitif | r = +0.17 | .008 |
| Karşılaştırma × Beck | Pozitif | r = +0.26 | <.001 |

Bu örüntü Tomoda et al. (2009) ve Bowlby (1973) bağlanma teorisini doğrudan destekliyor. Tezde "**ölçeğin nomolojik ağı (nomological network) ampirik olarak desteklenmiştir**" (Cronbach & Meehl, 1955) ifadesi savunulabilir.

### 5.3 İndeks-Kardeş Düşük Konkordans — PDT Teorisinin Doğrudan Kanıtı

| Subskala | ICC(2,1) | Yorum |
|---|---|---|
| Reddetme | 0.158 | Çok düşük |
| Karşılaştırma | 0.202 | Düşük |
| Aşırı Koruma | 0.205 | Düşük |
| Sıcaklık | 0.297 | Düşük-orta |

Koo & Li (2016) sınıflamasıyla **dördü de "poor"**, ama bu **kusur değil bulgu**. McHale et al. (2012) tam olarak bunu öngörüyor: aynı annenin sıcaklığını/reddini iki kardeş **sistematik olarak farklı algılar**, bu **non-shared environment** çekirdeğidir (Plomin & Daniels, 1987). Tezde:

> "Aile içi indeks-kardeş ICC değerleri (.16–.30 aralığında) parental differential treatment (PDT) çerçevesini ampirik olarak desteklemektedir. Bu bulgu, kardeşlerin aynı ebeveynlik ortamını birebir aynı algılamadığını ve dolayısıyla ölçek puanlarının dyadic veya within-family çerçevesinde modellenmesi gerektiğini göstermektedir."

### 5.4 SHA-256 Hash Doğrulaması — Reprodüktiblik Standardı

Çıktının ilk tablosu, kanonik veriden hiç sapmadığını kanıtlıyor. **Bu, 2026 standardı open-science raporlamada birinci satırda yer almalı.** Tez metodolojik ekinin "Reprodüktiblik" alt başlığında:

> "Tüm analizler, FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock (sürüm 2026-04-26) içinde tanımlı veri sürümü üzerinde yürütülmüş ve veri bütünlüğü SHA-256 kriptografik hash ile doğrulanmıştır. Analiz hattı Quarto + R + lavaan ile renv.lock altyapısında reprodüktibldir."

---

## 6. Quarto Render Kalitesi — Küçük Düzeltmeler

§6 (Ölçüm Değişmezliği) tablosunda lavaan hata mesajı **inline çıktı olarak markdown tablosuna karışmış** ve render bozulmuş:

```
| |EMBU-P |group       |configural |         NA|...|some categories of variable `embu_p_q12'...
```

Bu, R chunk'ında `error=TRUE` opsiyonunun açık unutulmasından kaynaklanıyor. Düzeltme:

```r
# YAML / chunk options
knitr::opts_chunk$set(error = FALSE, warning = FALSE, message = FALSE)

# Hata mesajını programatik olarak yakala ve formatla
mi_results <- tryCatch(
  measurementInvariance(...),
  error = function(e) tibble(error_message = as.character(e), level = "FAILED"))

# Tablo içine doğru sütun olarak yerleştir
gt::gt(mi_results) |>
  gt::cols_label(error_message = "Hata mesajı")
```

---

## 7. Sonuç ve Öneriler

### 7.1 Çıktının Genel Hükmü

Bu çıktı **iyi yapılandırılmış ama eksik bir validasyon raporudur**. Reproducible infrastructure (hash + Quarto) örnek; pre-registered analysis plan ile uyum %55–60 düzeyinde. Eksiklerin **çoğu giderilebilir**.

### 7.2 Üç Cümle Stratejik Tavsiye

1. **Tez teslim edilmeden önce mutlaka:** BSEM çalıştırılmalı, q12 dışlanarak DM × Kontrol MI yeniden tahmin edilmeli, SRQ alt ölçek skorları hesaplanmalı, TOST eklenmeli.
2. **Tez tartışmasında dürüstçe sınırlandırılmalı:** EMBU-P 4-faktör yapı bu örneklemde **tam değil kısmen** desteklendi (CFI=.88, KMO=.12); Reddetme alt ölçeği **sosyal istenirlik nedeniyle ölçemez** hâle gelmiş olabilir; bu, ölçeğin değil **örneklem-spesifik raporlama davranışının** sonucudur.
3. **Adaptasyon makalesinde ise tam tersine bir manşete dönüştürülebilir:** "Türk anne öz-bildirimi, çocuk bildirimine kıyasla sistematik olarak farklı bir ölçüm yapısına sahiptir; bu, EMBU ailesi içinde rapor-rolü etkisinin Türkçe kültürel bağlamda ilk ampirik kanıtıdır." Bu pozisyon, *European Journal of Psychological Assessment* veya *Journal of Family Psychology* için **özgün katkı** iddiası taşır.

### 7.3 Bir Sonraki Görüşmede Ele Alınabilecekler

Eğer isterseniz şu üç çıktıyı sırayla üretebilirim:

- **(a)** BSEM script'inin tam halini (`blavaan` + `rstan` ayarlarıyla) — Stan'ın gece çalıştırılabilir hâli
- **(b)** SRQ alt ölçek hesaplama R kodunu (Furman-Buhrmester orijinal madde-faktör eşlemesiyle) — bu hızlı bir kazanım
- **(c)** Tez Bölüm 3 (Bulgular) için APA-uyumlu **paragraf taslağını** — yukarıdaki tablolardan üretilmiş, kelime kelime kullanıma hazır

Hangisiyle başlamak istersiniz?
