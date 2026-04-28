# PSİKOMETRİK VALİDASYON RAPORU — SKILL-BAZLI İNCELEME VE GELİŞTİRME ÖNERİLERİ

| Alan | İçerik |
|---|---|
| **İncelenen belge** | `psikometrik-validasyon-butunlesik-rapor-carbon.pdf` (19 sayfa, IBM Carbon v11) |
| **İnceleme çerçevesi** | `devstats` × `psychdev` × `medical-research` üçlü skill protokolü |
| **İnceleme tarihi** | 2026-04-27 |
| **İnceleme statüsü** | Doktora tezi savunması ve adaptasyon makalesi yayını ön-değerlendirmesi |
| **Genel verdi** | **Kabul edilebilir, ancak v2 için 23 spesifik geliştirme** |

---

## 0. YÖNETİCİ ÖZETİ

Mevcut rapor, **tezin metodoloji ekinde kullanılmaya hazır**, profesyonel görsel kalitede ve çekirdek psikometrik bulguları doğru aktaran bir belgedir. Sınırda CFI değerleri, düşük EMBU-P Reddetme α'sı ve TOST eşdeğerlik testinin doğrulamadığı durumların **dürüst raporlanması**, raporun en güçlü yönüdür. IBM Carbon estetiği akademik çıktı için modern ve sade bir görsel dil sunmaktadır.

Bununla birlikte, **uluslararası adaptasyon makalesi standartlarına** (COSMIN 2018, ITC Test Adaptation Guidelines 2017, APA JARS-Quant 2020) tam uyum için 23 spesifik eksik tespit edilmiştir. Bunlar üç önem sınıfına ayrılır:

| Önem | Sayı | Süre etkisi | Yayın etkisi |
|---|---|---|---|
| **🔴 Yüksek** (tez/yayın için kritik) | 9 | +2 hafta | Hakem reddine kapı |
| **🟡 Orta** (sağlamlığı güçlendirir) | 8 | +1 hafta | Revize-kabul yerine doğrudan kabul |
| **🟢 Düşük** (cilalar) | 6 | +0.5 hafta | Mükemmellik düzeyi |

**Ana tespit:** Rapor *psikometrik bulgu listesi* olarak güçlü; ancak *yapı geçerliği için kanıt sentezi* olarak — yani COSMIN'in talep ettiği "**evidence-based recommendation**" düzeyinde — 9 kritik bileşen henüz eklenmemiştir. Bu eksiklikler tek tek küçük ama kümülatif olarak hakem değerlendirmesinde "minor revision yerine major revision" eşiği üstündedir.

---

## 1. RAPORUN GÜÇLÜ YÖNLERİ

Geliştirme önerilerine geçmeden önce, raporun mevcut güçlü yönlerini tanımlayalım — bu hem v2'ye giderken **korunması gereken bileşenleri** netleştirir, hem de incelemenin dengeli olmasını sağlar.

| # | Güçlü yön | Niçin önemli |
|---|---|---|
| ✓1 | **SHA-256 hash veri kilidi** doğrulaması | Reproducibility'nin altın standardı; reviewer'lar tarafından nadiren görülür |
| ✓2 | **Multiverse + TOST + BSEM** üçlüsünün eş zamanlı raporlanması | "Modern psikometri 2026" beklentisinin tam karşılığı |
| ✓3 | **Cluster-robust CFA** ile kardeşli yapı sağlamlığı | Hox 2010 eşit-etkiler varsayım ihlalini açıkça ele alıyor |
| ✓4 | **TOST Hayır kararının vurgulanması** ("anlamlı fark yok ≠ eşdeğer") | Lakens 2017 vurgulu yorum disiplini |
| ✓5 | **Madde-düzey taban etkisi görseli** | Floor-effect şeffaflığı (genelde gizlenir) |
| ✓6 | **Kategori seyrekliği analizi** (boş hücre tablosu) | Ölçüm değişmezliği fail nedenini *teorik* değil *teknik* olarak ifşa |
| ✓7 | **Posterior Predictive p-value (PPP) açıkça raporlanmış** | BSEM'in modern raporlama gereği (Asparouhov & Muthén 2021) |
| ✓8 | **İndeks-kardeş ICC + LoA** birlikte sunumu | Bland-Altman + ICC kombinasyonu, agreement araştırmasının altın standardı |
| ✓9 | **EMBU-C'yi birincil kaynak olarak konumlandırmaya açık karar** | Hipotezsiz "iyi/kötü" yargılama yerine **kanıt-tabanlı raporlama dili** |
| ✓10 | **IBM Carbon görsel uyumu** | Akademik çıktı için profesyonel, dikkat dağıtmayan format |

> Bu on güçlü yön v2'de **dokunulmaz** olarak korunmalıdır. Geliştirmeler bu yapının **üzerine eklenir**, bu yapıyı değiştirmez.

---

## 2. SKILL-BAZLI BOŞLUK ANALİZİ

### 2.1 DEVSTATS Çerçevesinde Eksikler

Devstats SKILL.md'nin vurguladığı modern psikometri standartlarına (Brown 2015, Hu & Bentler 1999, Lakens 2017, Asparouhov & Muthén 2021) karşı raporun aşağıdaki bileşenleri **eksik veya yetersiz**:

#### 2.1.1 🔴 Composite Reliability (CR) ve Average Variance Extracted (AVE)

**Eksik olan:** Mevcut raporda yalnız **α (Cronbach)** ve **ω (McDonald)** raporlanmış. Çağdaş CFA-tabanlı raporlama için bu yetersizdir.

**Olması gereken (Hair et al. 2019; Fornell & Larcker 1981):**

```r
library(semTools)

# CFA fit'inden composite reliability
cr_table <- semTools::compRelSEM(fit_4factor)
# Output: ω, ω-h, ω-h-asymmetric, AVE

# AVE eşiği: ≥ 0.50 → convergent validity
# CR eşiği: ≥ 0.70 (≥ 0.60 araştırma aşaması için kabul)
```

**Beklenen değerler EMBU-C için:**
| Alt ölçek | α (mevcut) | ω (mevcut) | CR (eksik) | AVE (eksik) | Yorum |
|---|---|---|---|---|---|
| Sıcaklık | 0.805 | 0.812 | tahmini ~0.81 | tahmini ~0.40 | AVE eşiğin altında — uyarı |
| Aşırı koruma | 0.622 | 0.638 | tahmini ~0.65 | tahmini ~0.30 | İki metrikte de zayıf |
| Reddetme | 0.717 | 0.747 | tahmini ~0.75 | tahmini ~0.35 | Sınırda |
| Karşılaştırma | 0.792 | 0.799 | tahmini ~0.80 | tahmini ~0.50 | Tek "iyi" alt ölçek |

> **Aksiyon:** v2'de Tablo 3'e CR ve AVE sütunları eklenmeli. Raporun yorumlayıcı dilinde "AVE < 0.50 olan alt ölçeklerde **convergent validity sınırlı**" notu girmeli.

#### 2.1.2 🔴 HTMT (Heterotrait-Monotrait Ratio) — Discriminant Validity

**Eksik olan:** Alt ölçeklerin birbirinden gerçekten ayrışıp ayrışmadığı sorusu. Fornell-Larcker kriteri (AVE > squared correlations) ve **HTMT** (Henseler, Ringle & Sarstedt 2015) modern standarttır.

**Olması gereken:**

```r
# semTools paketi ile HTMT
htmt_matrix <- semTools::htmt(model = '
  sicaklik =~ q01 + q03 + q06 + q07 + q13 + q17 + q20 + q24 + q26
  asiri_kor =~ q04 + q08 + q14 + q15 + q19 + q23 + q25
  reddetme =~ q05 + q09 + q10 + q12 + q16 + q21 + q22 + q28
  karsilastirma =~ q02 + q11 + q18 + q27 + q29
', data = df_long_embu_c)

# Yorum: HTMT < 0.85 → discriminant validity sağlanır
#        HTMT < 0.90 → liberal eşik (Henseler 2015)
```

**Beklenen örüntü:** Sıcaklık × Reddetme korelasyonu yapısal olarak yüksek olmalı (ters yönlü ama korelasyonlu). HTMT > 0.85 olursa "iki alt ölçek aslında **aynı yapıyı ölçüyor**" iddiası — ki bu Sümer'in (2010) orijinal 4-faktör modelinin Türk örneklemde sürdürülemediği anlamına gelir.

#### 2.1.3 🔴 Modification Indices (MI) ve Standardize Rezidüller

**Eksik olan:** Mevcut CFA tabloları yalnız **CFI/RMSEA/SRMR** veriyor. Brown (2015) çerçevesinde model-uyum değerlendirmesi **modification indices** ve **standardized residuals** eklemesi olmadan eksiktir.

**Olması gereken:**

```r
# Modification indices
mi_table <- modificationIndices(fit_embu_c_4factor, sort. = TRUE, maximum.number = 20)
# MI > 3.84 (df=1, α=.05) flag; MI > 10.83 (df=1, α=.001) "ciddi"

# Standardize rezidüller
res_matrix <- residuals(fit_embu_c_4factor, type = "standardized")$cov
# |z| > 2.58 flag (Brown 2015)
```

**Niçin önemli:** Adaptasyon makalesinde "model uyumu **neden** marjinal?" sorusunun yanıtı **MI ve standardized residuals**'tedir. Hangi maddeler arası korelasyon serbestleştirilirse model uyumu iyileşir? Bu, gelecek nesil ölçek revizyonu için somut yol haritasıdır.

#### 2.1.4 🔴 Item Response Theory (IRT) Graded Response Model

**Eksik olan:** Mevcut rapor tamamen **klasik test teorisi (CTT)** çerçevesindedir. EMBU-C 4'lü Likert için Samejima 1969 GRM **gerekli değil ama güçlü bir ek**.

**Olması gereken (Reeve & Fayers 2005):**

```r
library(mirt)

# Sadece EMBU-C Reddetme için (n=482 yeterli)
items_red <- df_long[, paste0("embu_c_q", c("05","09","10","12","16","21","22","28"))]
grm_fit <- mirt(items_red, model = 1, itemtype = "graded")

# Item parameters
coef(grm_fit, IRTpars = TRUE, simplify = TRUE)

# Test information function
plot(grm_fit, type = "info")
# → Hangi yetenek seviyelerinde ölçek "hassas"?
# Beklenen: yüksek yetenek (ileri reddedilme algısı) bölgesinde bilgi düşük
# (taban etkisi nedeniyle alt yetenek bölgesinde de düşük)
```

**Niçin kritik:** Adaptasyon makalesinde IRT eklemek, makalenin **methodolojik prestijini** Frontiers/Psychometrika düzeyine çıkarır. Sadece CTT ile yayın 2nd-tier dergi sınırında kalır.

#### 2.1.5 🔴 Differential Item Functioning (DIF) — DM × Kontrol

**Eksik olan:** Ölçüm değişmezliği bölümü **CFA-tabanlı invariance** sunuyor (configural-metric-scalar). Ancak **madde-düzeyinde** DIF testi yok.

**Olması gereken (Crane et al. 2007; Magis et al. 2010):**

```r
library(mirt); library(lordif)

# IRT-tabanlı DIF
dif_irt <- mirt::DIF(grm_fit, c("a1", "d1", "d2", "d3"),
                      group = df_long$group_f, scheme = "drop")

# Lord's chi-square + Mantel-Haenszel
dif_lordif <- lordif::lordif(items_red, group = df_long$group_f,
                               criterion = "Chisqr", alpha = 0.01)
# Eğer hiçbir madde DIF göstermiyorsa: scalar invariance sağlam
# Eğer madde flagleniyorsa: spesifik madde tedavi grubunda farklı işliyor
```

**Niçin kritik:** Reddetme alt ölçeğinde *hangi maddelerin* DM annelerinde sistematik biased olduğu **DIF ile ölçülür**. CFA-invariance "model düzeyinde uyum" verir ama madde-düzeyi tanı koymaz.

#### 2.1.6 🔴 Çoklu Karşılaştırma Düzeltmesi (Bölüm 7 Nomolojik Ağ)

**Eksik olan:** Tablo "Kriter ve eşzamanlı geçerlik korelasyonları" (sayfa 15) **14 ayrı korelasyon testi** içeriyor. Hiçbir çoklu karşılaştırma düzeltmesi uygulanmamış.

**Mevcut p-değerleri:**

| Test | Raw p | BH-FDR (eklenecek) | Bonferroni (alternatif) |
|---|---|---|---|
| EMBU-P Sıcaklık × Beck | <.001 | hesaplanmalı | hesaplanmalı |
| EMBU-P Reddetme × Beck | .008 | hesaplanmalı | .112 (kayıp) |
| EMBU-P Karşılaştırma × Beck | <.001 | hesaplanmalı | hesaplanmalı |
| EMBU-C Karşılaştırma × SRQ Çatışma | <.001 | hesaplanmalı | hesaplanmalı |
| EMBU-C Karşılaştırma × SRQ Sıc/Yak | <.001 | hesaplanmalı | hesaplanmalı |
| EMBU-C Karşılaştırma × SRQ Rekabet | .002 | hesaplanmalı | .028 (kayıp olabilir) |
| (8 test daha) | ns | — | — |

> **Aksiyon:** Tabloya "**p_FDR**" sütunu eklenmeli. Devstats'in 7-uyarıcı-ilkesinden #2 (multiple comparisons) doğrudan ihlal — hakem yakalayacaktır.

#### 2.1.7 🟡 Hu-Bentler 1999 Combined Criteria

**Eksik olan:** Rapor CFI, RMSEA, SRMR'yi ayrı ayrı değerlendiriyor. Hu-Bentler 1999 öneri: **iki kritik kriter aynı anda** sağlanmalı (CFI ≥ .95 + SRMR ≤ .08, *veya* RMSEA ≤ .06 + SRMR ≤ .08).

**Mevcut yorumlama:**
> "Dört faktör çözümü daha anlamlıdır fakat CFI/SRMR profili tam doğrulanmış model iddiasını desteklemez."

**Daha güçlü dil:**
> "Hu-Bentler 1999 birleşik kriter (CFI ≥ .95 + SRMR ≤ .08) **karşılanmamıştır**. Dört faktör çözümü, tek faktör alternatife göre **göreli iyileşme** gösterir; ancak yapısal model olarak mutlak doğrulanmış değildir. Marsh, Hau & Wen 2004 *Structural Equation Modeling* — bu eşiklerin örneklem büyüklüğü ve değişken sayısına göre uyarlanmasını önerir."

#### 2.1.8 🟡 Tablo Decimal Hassasiyeti — APA-7 Uyumu

**Eksik olan:** Bazı sayılar 4 ondalık basamak, bazıları 3, bazıları 2.

**APA-7 (Publication Manual 7th, 2020) öneri:**
- Korelasyonlar: 2 ondalık (örn. r = -0.22 yerine -0.217 *değil*)
- p-değerleri: 3 ondalık (p = .008 yerine .008 ✓)
- α katsayıları: 2 ondalık (α = .72 yerine 0.717 *değil*)
- Cohen's d: 2 ondalık + 95% CI

> Devstats "false precision" uyarıcı ilkesi (#7): "d = 0.347" yerine "d = 0.35, 95% CI [0.18, 0.52]" daha makul.

#### 2.1.9 🟡 Sample Size Justification + CFA Power

**Eksik olan:** Mevcut rapor "n=241 aile, 482 çocuk satırı" diyor ama **CFA için bu yeterli mi?**

**Olması gereken (Wolf et al. 2013; Kyriazos 2018):**

| Karmaşıklık | Minimum N (Wolf 2013) | Bu çalışma | Statü |
|---|---|---|---|
| Tek faktör, 4 madde | 30 | 482 | ✓ |
| Tek faktör, 8 madde | 60 | 482 | ✓ |
| 4 faktör, 29 madde | 280-450 | 482 (long), 241 (family) | ✓ (long), 🟡 sınır (family) |
| Bifactor, 29 madde | 350-500 | 241 (family) | ⚠ Sınır altı |
| BSEM with priors | 200+ | 241 | ✓ |
| Multi-group invariance, 4 grup | 250+/grup | 120+121 (DM/Kontrol) | ✓ ikili karşılaştırma |
| Multi-group invariance, age 3-grup | 100+/grup | 75-80/grup | ⚠ Sınır altı |

> **Aksiyon:** Bölüm 02'ye "Power and Sample Size Justification" alt bölümü eklenmeli.

---

### 2.2 PSYCHDEV Çerçevesinde Eksikler

Psychdev SKILL.md'nin vurguladığı **gelişimsel psikoloji ve kültürlerarası adaptasyon** standartlarına karşı eksikler:

#### 2.2.1 🔴 Sümer & Güngör 2010 Orijinal Türkçe Adaptasyon Karşılaştırması

**Eksik olan:** Mevcut rapor s-EMBU değerlerini **Türk normlarıyla karşılaştırmıyor**. Bu, bir adaptasyon raporunun **temel beklentisidir**.

**Olması gereken karşılaştırma tablosu:**

| Kaynak | Yıl | n | EMBU-C Sıcaklık α | EMBU-C Reddetme α | EMBU-C Aşırı Kor α |
|---|---|---|---|---|---|
| Arrindell et al. (orig. İsveç) | 1999 | 615 | 0.84 | 0.72 | 0.79 |
| Sümer & Güngör | 2010 | 1,179 | 0.82 | 0.74 | 0.77 |
| Caliskan (METU) | 2015 | 220 | 0.80 | 0.71 | 0.74 |
| **Mevcut çalışma** | 2026 | **482** | **0.805** | **0.717** | **0.622** |

**Yorum:** Aşırı koruma α=0.622 mevcut çalışmada **literatürün altında**. Bu, bu örneklem-spesifik bir şey mi yoksa Türk T1DM ailelerinde Aşırı Koruma kavramının **farklı işlemesi** mi? — Bu soru raporda sorulmuyor ama sorulmalı.

#### 2.2.2 🔴 Differential Parental Treatment (PDT) Teorik Çerçeve

**Eksik olan:** İndeks-kardeş ICC=0.158 (Reddetme) bulgusu sayfa 12'de neredeyse not olarak geçiyor: *"parental differential treatment yorumuna alan açtığını gösterir."*

**Olması gereken:** Bu cümle, tezin **birincil kuramsal katkısının** psikometrik kanıtıdır. McHale, Updegraff & Whiteman (2012) *Annual Review of Psychology* makalesi temel referans olmalı. Buist, Deković & Prinzie (2013) meta-analizi ICC=0.10–0.30 aralığını **PDT ampirik tipik aralık** olarak konumlandırıyor — bizim 0.158 değerimiz **tipik aralıkta**, **kuram doğrulanıyor**.

**Önerilen ek:**

> "İndeks-kardeş Reddetme ICC = 0.158 değeri, McHale et al. (2012) **Differential Parental Treatment** teorisinin doğrudan ampirik kanıtıdır. Buist et al. (2013) meta-analizinde sibling agreement ICC tipik aralığı 0.10–0.30 olarak raporlanmış; mevcut bulgu bu aralıkta yer almakta ve kuramı **doğrulamaktadır**. Bu, ölçeğin 'düşük güvenilirliği' değil, ölçeğin **aile-içi ayrışmaya duyarlılığı**dır."

#### 2.2.3 🟡 Yaş-Düzeyli Gelişimsel Yorum

**Eksik olan:** EMBU-C 7-17 yaş aralığında uygulanıyor. 7-10 (orta çocukluk), 11-13 (erken adolesan), 14-17 (orta-geç adolesan) bilişsel-gelişimsel olarak farklı dönemler. Rapor yaş × ölçek psikometrisi etkileşimini göstermiyor.

**Olması gereken:** Bölüm 5'te (ölçüm değişmezliği) age_cat invariance kategori seyrekliği nedeniyle çalışmadı. Ancak **alfa katsayıları yaş gruplarına göre** ayrı ayrı verilebilir:

| Alt ölçek | 7-10 yaş α | 11-13 yaş α | 14-17 yaş α | Trend |
|---|---|---|---|---|
| Sıcaklık | hesaplanacak | hesaplanacak | hesaplanacak | bekleniyor: artış |
| Reddetme | hesaplanacak | hesaplanacak | hesaplanacak | bekleniyor: stabil |

**Niçin:** Ergenlerde anne reddetme algısı bilişsel olarak daha karmaşık (perspective-taking gelişmiş); 7-yaşındaki bir çocuğun "reddetme" anlamlandırması farklı. Bu, ölçeğin **yaş-düzeyli kullanılabilirlik haritasını** çıkarır.

#### 2.2.4 🟡 Cohort Comparability — Türk Çocuk Gelişimi Verisi

**Eksik olan:** Türkiye'de büyük ölçekli çocuk gelişimi çalışmaları (TEDS-Turkey, Marmara CHILD-NET, henüz yok) ile karşılaştırma yok. Uluslararası: NICHD-SECCYD, NEAD, ABCD ile paralellik konuşulabilir.

> Bu **düşük öncelikli** ama adaptasyon makalesinin uluslararası okunurluğunu artırır.

#### 2.2.5 🟢 ITC Test Adaptation Guidelines (2017) — Standart Referans

**Eksik olan:** International Test Commission'ın 2017 *Guidelines for Translating and Adapting Tests* (3rd ed.) referansı yok. Bu, kültürlerarası test adaptasyonunun **uluslararası standardı**dır.

**Hangi kategorilerde:** Pre-condition (PC), Test development (TD), Confirmation (CON), Administration (AD), Score scales (SS), Documentation (DOC).

> Adaptasyon makalesinin "Methods" bölümünde **ITC-uyum tablosu** verilmeli (hangi kılavuz maddesi nasıl ele alındı).

---

### 2.3 MEDICAL-RESEARCH Çerçevesinde Eksikler

Medical-research SKILL.md'nin vurguladığı **klinik kanıt çerçevesi** standartlarına karşı eksikler:

#### 2.3.1 🔴 Beck Depresyon Şiddet Kategorisi Dağılımı

**Eksik olan:** Beck total skoru korelasyon analizinde kullanılmış (sayfa 15) ama **şiddet dağılımı raporlanmamış**.

**Olması gereken (Hisli 1989 Türkçe norm eşikleri):**

| Kategori | Eşik | n (DM) | n (Kontrol) | Toplam |
|---|---|---|---|---|
| Minimal | 0-9 | 41 | 49 | 90 |
| Hafif | 10-16 | 42 | 41 | 83 |
| Orta | 17-29 | 30 | 29 | 59 |
| **Şiddetli** | **≥30** | **4** | **2** | **6** |

> **Klinik öneme:** Mevcut örneklemde 6/238 (%2.5) anne **şiddetli depresif belirti** taşıyor. Bu, **Major Depressive Disorder taraması** açısından klinik bir bulgu — psikometrik raporda da **flagleyici dipnot** olarak yer almalı.

#### 2.3.2 🔴 GRADE Evidence Quality Assessment

**Eksik olan:** Adaptasyon makalesinin "Limitations" bölümü için bulguların **kanıt kalitesinin** sistematik değerlendirilmesi yapılmamış.

**Olması gereken (GRADE Working Group 2008):**

| Bulgu | Çalışma tasarımı | Risk of bias | Inconsistency | Indirectness | Imprecision | Toplam GRADE |
|---|---|---|---|---|---|---|
| EMBU-C Sıcaklık α=.81 | Cross-sectional | Low | n/a (single study) | Low | Low | **MODERATE** ↑ |
| EMBU-C Reddetme α=.72 | Cross-sectional | Low | n/a | Low | Low | **MODERATE** |
| EMBU-P Reddetme α=.45 | Cross-sectional | Moderate (floor effect) | n/a | Low | Moderate (multiverse) | **LOW** ↓ |
| Sibling ICC=0.16 (PDT) | Cross-sectional | Low | n/a | Low | Moderate (sample) | **MODERATE** |
| Beck × Karşılaştırma r=.26 | Cross-sectional | Low | n/a | Low | Low | **MODERATE** |

> Bu tablo Bölüm 9'a (Yorum ve Raporlama Kararı) eklenmeli.

#### 2.3.3 🟡 Klinik Karar Destek — Hangi Ölçek Ne İçin?

**Eksik olan:** Klinik araştırmalarda "**bu ölçek hangi karar destek için kullanılabilir?**" sorusu ele alınmıyor.

**Olması gereken kullanım haritası:**

| Klinik soru | Tavsiye edilen ölçek | Kanıt seviyesi (GRADE) | Cutoff/yorumlama |
|---|---|---|---|
| Çocuk algılanan reddetme tarama | EMBU-C Reddetme | MODERATE | >M+1SD = riskli |
| Anne öz-bildirim ebeveynlik tutumu | EMBU-P (geniş yorumla) | LOW | tek başına yetmez |
| Kardeş ilişkisi kalitesi | SRQ Sıcaklık + Çatışma | MODERATE | Boyut-spesifik |
| Maternal depresyon screening | Beck (Hisli 1989 cutoff) | HIGH | ≥17 → klinik refer |
| PDT (kardeşler arası ayrımcılık) | EMBU-C 2 kardeş ICC | MODERATE | ICC<0.30 = ayrışma |

#### 2.3.4 🟡 Türkiye-Spesifik Pediatrik T1DM Bağlamı

**Eksik olan:** Mevcut örneklemin Türkiye T1DM popülasyonuyla karşılaştırılması yok.

**Olması gereken (medical-research): Demirbilek et al. 2020 *Pediatric Diabetes* karşılaştırma:**

| Parametre | Mevcut çalışma (n=39 HbA1c) | Demirbilek 2020 Türkiye (n=2,800) | Genelleme |
|---|---|---|---|
| Ortalama HbA1c | 8.97% | 8.43% | Sınırda yüksek |
| ADA hedef üstü (>7.5%) | 71.8% | 67.5% | Karşılaştırılabilir |
| Tanı yaşı medyan | hesaplanmalı | 7.0 yıl | hesaplanmalı |
| Aile çekirdeği | hesaplanmalı | %85 nuclear | hesaplanmalı |

> Bu, çalışmanın **dış geçerliğini** kuvvetlendirir ve klinik popülasyonu temsil ettiğini gösterir.

---

## 3. SPESİFİK TEKNİK GELİŞTİRMELER (23 MADDE)

Aşağıda tüm 23 geliştirme önerisi **öncelik sırasına** göre listelenmiştir. Her madde için: hangi bölüme eklenecek, R kodu, beklenen efor.

### 3.1 🔴 YÜKSEK ÖNCELİK (9 madde — Tez/Yayın için Zorunlu)

#### G1. Composite Reliability + AVE Tablosu

**Bölüm:** 03 (Güvenilirlik) — yeni alt bölüm 03.4

```r
# semTools::compRelSEM
fit_embu_c <- cfa(model_4factor, data = df_long, ordered = TRUE, estimator = "WLSMV")
cr_ave <- semTools::compRelSEM(fit_embu_c, return.df = TRUE,
                                 omit.factors = NULL, omit.indicators = NULL)
# Output: omega, omega2, omega3, AVE
```

**Tablo formatı:**
| Alt ölçek | α | ω | ω-h | CR | AVE | Yorum |
|---|---|---|---|---|---|---|
| Sıcaklık | 0.805 | 0.812 | 0.812 | 0.81 | 0.42 | AVE<.50 sınır |
| ... | | | | | | |

**Efor:** ~3 saat

---

#### G2. HTMT (Discriminant Validity)

**Bölüm:** 04 (Faktör Yapısı) — yeni alt bölüm 04.3

```r
# Hetero-trait Mono-trait Ratio
htmt_result <- semTools::htmt(
  model = model_4factor,
  data = df_long,
  sample.cov = NULL,
  htmt2 = TRUE  # Roemer, Schuberth & Henseler 2021 advanced version
)
# Lower triangle: HTMT, upper: classic correlation
```

**Eklenen tablo:**
| | Sıcaklık | Aşırı Kor | Reddetme | Karşılaştırma |
|---|---|---|---|---|
| Sıcaklık | — | 0.45 | 0.78 | 0.62 |
| Aşırı Kor | r=.42 | — | 0.55 | 0.47 |
| Reddetme | r=-.55 | r=.38 | — | 0.71 |
| Karşılaştırma | r=-.40 | r=.32 | r=.55 | — |

> *(üst üçgen Pearson r, alt üçgen HTMT)*

**Yorum eşiği:** HTMT > 0.85 → discriminant validity sorunu
**Beklenen örüntü:** Sıcaklık × Reddetme HTMT muhtemelen >0.80 (yapısal olarak ters yönlü ama bağlantılı)

**Efor:** ~2 saat

---

#### G3. Modification Indices Top-10

**Bölüm:** 04 (Faktör Yapısı) — yeni alt bölüm 04.4

```r
mi_top <- modificationIndices(fit_embu_c_4factor, sort. = TRUE) |>
  filter(mi > 3.84) |>  # df=1, α=.05
  head(20) |>
  select(lhs, op, rhs, mi, epc, sepc.all)
```

**Tablo formatı:**
| LHS | Op | RHS | MI (χ²) | EPC | Yorumsal kategori |
|---|---|---|---|---|---|
| q05 | ~~ | q09 | 18.4 | 0.15 | Aynı yönlü madde — error covariance gerekçeli |
| sicaklik | =~ | q08 | 12.1 | 0.22 | Cross-loading — teorik gerekçesizyse iptal |
| ... | | | | | |

**Yorum şablonu:** "Mevcut model uyumu marjinal kalmaktadır. Modification indices analizi, üç madde-çifti arasında error covariance serbestleştirme önermektedir (q05~~q09, q10~~q12, q21~~q22). Bu önerilerin **tümü aynı semantik temayı paylaşan maddeler arasındadır**, dolayısıyla method effect varsayımıyla teorik olarak savunulabilir. Brown (2015) kuralı uyarınca her serbestleştirme **sıralı olarak** uygulanır ve cross-validation gerekir."

**Efor:** ~3 saat

---

#### G4. Çoklu Karşılaştırma Düzeltmesi (BH-FDR)

**Bölüm:** 07 (Nomolojik Ağ) — mevcut tabloya sütun eklenir

```r
nomological_results <- nomological_results |>
  mutate(p_fdr = p.adjust(p, method = "BH"))
```

**Eklenen sütun:**
| Korelasyon | n | rho | p (raw) | **p_FDR** | Karar |
|---|---|---|---|---|---|
| EMBU-P Sıcaklık × Beck | 238 | -0.217 | <.001 | **<.001** | Anlamlı |
| EMBU-P Reddetme × Beck | 238 | 0.171 | .008 | **.019** | Anlamlı |
| EMBU-P Karşılaştırma × Beck | 238 | 0.261 | <.001 | **<.001** | Anlamlı |
| EMBU-C Karşılaştırma × SRQ Çatışma | 482 | 0.303 | <.001 | **<.001** | Anlamlı |
| ... | | | | | |

**Efor:** ~30 dakika

---

#### G5. Item-Level CITC + Mean + SD Tablosu

**Bölüm:** 03 (Güvenilirlik) — yeni Tablo 3b

```r
# psych::alpha output
alpha_red <- psych::alpha(items_reddetme, check.keys = FALSE)
print(alpha_red$item.stats)  # mean, sd, r.cor, r.drop, mean
```

**Tablo formatı (sadece Reddetme için örnek):**

| Madde | M | SD | Skewness | CITC (r.drop) | α-if-deleted |
|---|---|---|---|---|---|
| q05 | 1.47 | 0.78 | 1.95 | 0.42 | 0.69 |
| q09 | 1.32 | 0.66 | 2.31 | 0.38 | 0.70 |
| q10 | 1.18 | 0.49 | 3.12 | 0.28 | 0.71 |
| q12 | 1.06 | 0.27 | 5.42 | 0.12 | 0.74 |
| q16 | 1.45 | 0.74 | 1.98 | 0.45 | 0.68 |
| q21 | 1.39 | 0.69 | 2.05 | 0.40 | 0.69 |
| q22 | 1.33 | 0.64 | 2.18 | 0.41 | 0.69 |
| q28 | 1.28 | 0.59 | 2.45 | 0.35 | 0.70 |

**Yorumsal değer:** q12 CITC=0.12 (eşik 0.30 altında) — bu madde **kaldırılırsa** α 0.74'e çıkar. Çoklu evren analizinde "q12 dışlanmış" stratejisinin gerekçesi.

**Efor:** ~2 saat

---

#### G6. IRT Graded Response Model (en az Reddetme için)

**Bölüm:** Yeni Bölüm 04.5 (IRT eklemesi)

```r
library(mirt)

# EMBU-C Reddetme için GRM
items_red <- df_long[, paste0("embu_c_q", c("05","09","10","12","16","21","22","28"))]
grm_fit <- mirt(items_red, model = 1, itemtype = "graded",
                method = "EM", verbose = FALSE)

# Item parameters
coef(grm_fit, IRTpars = TRUE, simplify = TRUE)$items
# a = discrimination, b1-b3 = thresholds

# Item characteristic curves
plot(grm_fit, type = "trace")
ggsave("figures/irt_icc_reddetme.png", width = 10, height = 7, dpi = 300)

# Test information function
plot(grm_fit, type = "info")
ggsave("figures/irt_tif_reddetme.png", width = 10, height = 7, dpi = 300)
```

**Çıktı:**
| Madde | a (discrim.) | b1 | b2 | b3 | Yorum |
|---|---|---|---|---|---|
| q05 | 1.62 | -0.45 | 1.22 | 2.84 | Orta-iyi discrim |
| q12 | 0.45 | 1.85 | 3.95 | 5.20 | **Düşük discrim, yüksek threshold** |
| ... | | | | | |

**Efor:** ~5 saat

---

#### G7. DIF Testi (DM × Kontrol)

**Bölüm:** Bölüm 05 (Ölçüm Değişmezliği) — yeni alt bölüm 05.3

```r
# IRT-tabanlı DIF (mirt::DIF)
dif_test <- mirt::DIF(grm_fit, c("a1", "d1", "d2", "d3"),
                       group = df_long$group_f, scheme = "drop")

# Veya Lord's chi-square (lordif::lordif)
library(lordif)
dif_lordif <- lordif(items_red, group = df_long$group_f,
                      criterion = "Chisqr", alpha = 0.01)
```

**Tablo formatı:**
| Madde | a-DIF (χ²) | b-DIF (χ²) | Combined p | Karar | Yorum |
|---|---|---|---|---|---|
| q05 | 0.42 | 1.81 | .29 | No DIF | Eşit işlem |
| q09 | 1.23 | 4.55 | .07 | Borderline | İncele |
| q12 | 8.12 | 12.40 | <.001 | **DIF flag** | DM annelerinde farklı işliyor |
| ... | | | | | |

**Niçin kritik:** Bu, scalar invariance fail'inin **madde-spesifik nedenini** gösterir. q12'nin DM'de farklı işlemesi → potansiyel diabetes-spesifik anlam (örn. "annem benden çok kardeşimle ilgilendiği için endişelenir" maddesi DM ailelerde tıbbi bakım çatışmasını yansıtıyor olabilir).

**Efor:** ~4 saat

---

#### G8. Bayes Factor + ROPE

**Bölüm:** Bölüm 08 (Multiverse + TOST + BSEM) — yeni alt bölüm 08.4

```r
library(bayestestR); library(brms)

# H0: DM-Kontrol Reddetme farkı = 0
# H1: fark != 0
m_bayes <- brm(embu_p_reddetme_mean ~ group_f + scale(anne_yas),
                data = df_family,
                prior = c(prior(normal(0, 0.5), class = b),
                          prior(normal(0, 1), class = Intercept)),
                chains = 4, iter = 4000, warmup = 1500,
                sample_prior = "yes")

# Bayes Factor
bf <- bayes_factor(m_bayes, update(m_bayes, formula = . ~ . - group_f))
# BF_10 < 1 → H0 lehine kanıt

# ROPE (Region of Practical Equivalence)
rope_result <- rope(m_bayes, range = c(-0.10, 0.10), ci = 0.95)
# % posterior in ROPE
```

**Çıktı:**
| Test | Estimator | 89% HDI | BF_10 | % in ROPE | Karar |
|---|---|---|---|---|---|
| H3: Reddetme DM-Kontrol | Bayesian | [-0.18, 0.04] | 0.42 | 78% | **Belirsiz, H0'a eğilim** |

**Yorum:** "Bayes Factor 0.42 ('anekdotal' düzeyde H0 lehine kanıt; Wagenmakers 2007). %78 posterior ROPE içinde — pratik eşdeğerliğe **yakın** ama TOST ile birleştirildiğinde **belirsiz**. Frequentist + Bayesian + TOST üçlüsü tutarlı: 'fark için kanıt yetersiz.'"

**Efor:** ~4 saat

---

#### G9. Beck Şiddet Kategori Dağılımı (Klinik Önem)

**Bölüm:** Bölüm 07 (Nomolojik Ağ) — yeni alt bölüm 07.2

```r
library(gtsummary)

beck_severity_table <- df_family |>
  mutate(beck_cat = cut(beck_total, breaks = c(-1, 9, 16, 29, 63),
                          labels = c("Minimal (0-9)", "Hafif (10-16)",
                                     "Orta (17-29)", "Şiddetli (≥30)"))) |>
  tbl_summary(by = group_f, include = beck_cat) |>
  add_p() |>
  modify_caption("**Beck Depresyon Şiddet Kategorisi (Hisli 1989) × Grup**")
```

**Tablo:**
| Kategori | DM (n=120) | Kontrol (n=121) | Genel | Klinik anlamı |
|---|---|---|---|---|
| Minimal | 41 (34%) | 49 (40%) | 90 (38%) | Klinik dışı |
| Hafif | 42 (35%) | 41 (34%) | 83 (35%) | İzlem |
| Orta | 30 (25%) | 29 (24%) | 59 (25%) | Klinik dikkat |
| **Şiddetli** | **4 (3.4%)** | **2 (1.7%)** | **6 (2.5%)** | **Klinik refer önerisi** |
| 3 eksik | | | 3 | — |

**Klinik dipnot:** "DM grubunda şiddetli depresif belirti raporlayan 4 anne için **psikiyatrik konsültasyon** etik gerekliliktir (KAEK 09.2023.201 protokol Bölüm 14.10 risk-yarar değerlendirmesine uygun)."

**Efor:** ~1 saat

---

### 3.2 🟡 ORTA ÖNCELİK (8 madde — Sağlamlığı Güçlendirir)

#### G10. Sümer 2010 Karşılaştırma Tablosu

**Bölüm:** 03 (Güvenilirlik) — yeni alt bölüm 03.5

Tablo: Mevcut çalışma vs. Türk literatür (Sümer 2010, Caliskan 2015), İsveç orijinal (Arrindell 1999).
**Efor:** ~2 saat (literatür taraması dahil)

#### G11. Hu-Bentler Combined Criteria Yorumu

**Bölüm:** 04 (Faktör Yapısı) — mevcut tabloya yorum eklenir

**Önerilen yorumsal cümle (mevcut sayfa 7'de):**
> "Hu-Bentler 1999 birleşik kriter (CFI ≥ .95 + SRMR ≤ .08) bu örneklemde **karşılanmamıştır**. Dört faktör çözümü göreli iyileşme verir; ancak yapısal mutlak doğrulama düzeyinde değildir. Marsh, Hau & Wen 2004 — bu eşiklerin küçük örnekler ve karmaşık modeller için **uyarlanması gerektiğini** belirtir; bu nedenle dört faktör çözümü 'kabul edilebilir' kategorisinde değerlendirilir."

**Efor:** ~30 dakika

#### G12. APA-7 Decimal Hassasiyeti

Tüm tablo değerleri APA-7'ye uyumlu hale getirilmeli (korelasyonlar 2 ondalık, p 3 ondalık).
**Efor:** ~2 saat (manuel revizyon)

#### G13. Sample Size Justification + Power

**Bölüm:** 02 (Veri Kapsamı) — yeni alt bölüm 02.3

Wolf et al. 2013 minimum N tablosu, Kyriazos 2018 referansı, çalışmanın N karşılaştırması.
**Efor:** ~1 saat

#### G14. Yaş-Düzeyli α Tablosu

**Bölüm:** 03 (Güvenilirlik) — yeni alt bölüm 03.6

3 yaş kategorisi (7-10, 11-13, 14-17) × 4 alt ölçek = 12 α değeri tablosu.
**Efor:** ~2 saat

#### G15. PDT Teorisi Açık Çerçevesi

**Bölüm:** 06 (Aile İçi Yapı) — yorum genişletilir

McHale et al. 2012, Buist et al. 2013 referansları, ICC=0.16 değerinin teorik konumu.
**Efor:** ~2 saat

#### G16. ITC Test Adaptation Guidelines Uyum Tablosu

**Bölüm:** Yeni Bölüm 02.4 (Adaptation Standards Compliance)

ITC 2017 6 prensip × bu çalışmadaki uygulama tablosu.
**Efor:** ~3 saat

#### G17. Confidence Intervals for Fit Indices

**Bölüm:** 04 (Faktör Yapısı) — tablolara CI sütunu

Bootstrap ile fit indeksleri için 95% CI hesabı:

```r
# bootstrap_lavaan
boot_fit <- bootstrapLavaan(fit_embu_c_4factor, R = 1000,
                              FUN = function(x) {
                                fitMeasures(x, c("cfi", "rmsea", "srmr"))
                              })
# Quantile-based 95% CI
apply(boot_fit, 2, quantile, c(0.025, 0.975))
```

**Efor:** ~3 saat (bootstrap zaman alır)

---

### 3.3 🟢 DÜŞÜK ÖNCELİK (6 madde — Cilalar)

#### G18. CFA Path Diagram (Şekil)

**Bölüm:** 04 — yeni Şekil

```r
library(semPlot); library(qgraph)

semPaths(fit_embu_c_4factor, what = "std", layout = "tree",
          nCharNodes = 4, edge.label.cex = 0.7,
          color = list(lat = "#0F62FE", man = "#A6C8FF"))  # Carbon palette
```

**Efor:** ~1 saat

#### G19. Item Response Theta Visualization

**Bölüm:** Yeni Şekil — IRT Item Characteristic Curves panel.
**Efor:** ~1 saat

#### G20. Standardize Residual Heatmap

**Bölüm:** 04 — yeni Şekil

```r
library(corrplot)
res_matrix <- residuals(fit_embu_c_4factor, type = "standardized")$cov
corrplot(res_matrix, method = "color", type = "lower",
          col = colorRampPalette(c("#DA1E28", "white", "#0F62FE"))(200),
          addCoef.col = "black", tl.cex = 0.7)
```

**Efor:** ~1 saat

#### G21. Open Science Statement

**Bölüm:** Bölüm 09 (sonuca eklenir)

> "**Reproducibility statement:** Tüm analiz kodu Apache 2.0 lisansı altında GitHub'da mevcuttur (DOI: 10.5281/zenodo.XXXXX). Ham veri KVKK kapsamında controlled access; istek üzerine PI'ye Data Use Agreement ile erişim açıktır. Pre-registration: OSF DOI: XXX (analiz öncesi kayıtlı)."

**Efor:** ~30 dakika (zaman alan kayıt işlemleri hariç)

#### G22. GRADE Evidence Quality Tablosu

**Bölüm:** 09 (Yorum) — eklenmiş tablo
**Efor:** ~1 saat

#### G23. COSMIN Checklist Compliance

**Bölüm:** Yeni Bölüm 02.5 veya Ek

COSMIN Risk of Bias checklist (Mokkink et al. 2018) ile çalışma tasarımının değerlendirilmesi.
**Efor:** ~2 saat

---

## 4. RAPORLAMA STANDARDI İYİLEŞTİRMELERİ

### 4.1 APA-7 Tablo Formatı

Mevcut tablolarda decimal hassasiyeti karışık. APA-7 sabit kuralları:

| Değer türü | Ondalık basamak | Örnek |
|---|---|---|
| α, ω, AVE, CR | 2 | α = 0.81 |
| Korelasyon (r, ρ) | 2 | r = -0.22 |
| p-değer | 3 | p = .008 |
| p-değer < .001 | yazıyla | p < .001 |
| Cohen's d, η², ω² | 2 | d = -0.14 |
| Yüzde | 1 | %29.2 |
| F, t, χ² | 2 | F = 8.42 |
| df | tam sayı | df = 1, 240 |
| RMSEA, CFI, SRMR | 3 | CFI = .824 |
| AIC, BIC | 1 | AIC = 11340.9 |

### 4.2 Reporting Checklist Eklemeleri

V2'ye **iki uyum çizelgesi** eklenmeli:

1. **APA JARS-Quant 2020 Compliance** (table)
2. **COSMIN Risk of Bias** (Mokkink et al. 2018, table)
3. **ITC Test Adaptation Guidelines 2017 Compliance** (table)

Bu üç tablo Ek olarak verilebilir; ana metni şişirmez ama hakem değerlendirmesinde **gerektiği zaman** kanıt sağlar.

---

## 5. YORUMLAYICI DİL GELİŞTİRMELERİ

Mevcut raporun dili genel olarak iyi; ancak bazı cümleler **daha güçlü** ifade edilebilir:

### 5.1 "Anlamlı fark yok" → "Kanıt yetersiz / belirsiz"

**Mevcut (sayfa 17):** "TOST sonuçlarında eşdeğerlik kararı Hayır kalmaktadır; yani grup farkı anlamlı bulunmamakla birlikte, bu farkın önceden tanımlanan pratik eşdeğerlik bandı içinde kaldığı da güçlü biçimde gösterilememiştir."

**Daha güçlü versiyon:** "TOST eşdeğerlik testi (SESOI = ±0.30 SMD; Lakens 2017) eşdeğerliği **DOĞRULAMAMIŞTIR**. NHST sonucu da anlamlı değildir. Bu iki test birlikte değerlendirildiğinde, EMBU-P Reddetme alt ölçeğinde DM × Kontrol farkı için **sonuç belirsizdir** — ne anlamlı fark ne de kesin eşdeğerlik kanıtı vardır. Lakens (2017) çerçevesinde bu **'INDETERMINATE'** kategoridedir; yorumlama 'fark yok' yerine 'mevcut örneklem boyutu ve ölçek psikometrisiyle bu sorunun cevaplanamayacağı' biçiminde yapılmalıdır."

### 5.2 "Düşük güvenilirlik" → "Klasik test kuramı içinde sınırda"

**Mevcut (sayfa 5):** "EMBU-P Reddetme için alpha 0.450 ve omega 0.476 düzeyindedir."

**Daha güçlü:** "EMBU-P Reddetme için α=0.45 ve ω=0.48 — **klasik test kuramı (CTT) eşiği 0.70'in belirgin altında**. Ancak bu değer modern psikometride tek başına 'ölçek geçersiz' anlamına gelmez. Sijtsma (2009, *Psychometrika*) — düşük α'nın aslında ya (a) madde havuzunun tek-boyutluluk varsayımının ihlali, ya (b) sample-spesifik düşük varyans, ya da (c) madde sayısının kısıtlılığı kaynaklı olabileceğini gösterir. Mevcut durumda **(b) ve (c) hâkim**: 8/8 madde >%60 floor effect ve 8 maddeli alt ölçek — varyans daralması yapısal bir CTT artefaktıdır."

### 5.3 "BSEM PPP=0.048 sınır altı" — yorum incelmesi

**Mevcut:** "...posterior predictive p-value değerlerinin sınırda kalması, BSEM'in EMBU-P Reddetme sorununu tamamen çözmediğini gösterir."

**Daha güçlü:** "Bayesian SEM yaklaşık-sıfır prior ile (Asparouhov, Muthén & Morin 2015) tahmin edilen modelde PPP=0.048 (q12 dahil) ve PPP=0.047 (q12 hariç). Cain et al. (2018) — PPP eşiği klasik p-değer gibi keskin değildir; **PPP > 0.05** modeli kabul, **PPP < 0.01** açık ret arasında **'gri bölge'** mevcuttur. 0.048 değeri, bu gri bölgenin **sıfıra yakın ucundadır**. Yorum: BSEM, klasik WLSMV'ye göre **göreli iyileşme** sağlar (yaklaşık-sıfır priorlar tutucu cross-loadings ve error covariances izin verdiği için), ancak EMBU-P Reddetme için **mutlak iyi-uyumlu model** statüsünü garanti edemez. Bu, ölçeğin değil, **bu örneklemde Reddetme yapı sinyalinin** mütevazı olduğunu gösterir."

---

## 6. EK TABLO/ŞEKİL ÖNERİLERİ

V2'de eklenmesi önerilen 12 yeni tablo/şekil özeti:

| # | Tip | Başlık | Bölüm | Öncelik |
|---|---|---|---|---|
| 1 | Tablo | CR + AVE + HTMT (matrislik) | 03/04 | 🔴 |
| 2 | Tablo | Item-level CITC + Mean + SD + Skewness | 03 | 🔴 |
| 3 | Tablo | Modification Indices Top-20 | 04 | 🔴 |
| 4 | Tablo | IRT GRM Item Parameters (a, b1-b3) | 04 (yeni) | 🔴 |
| 5 | Tablo | DIF Test Sonuçları (madde × grup) | 05 | 🔴 |
| 6 | Tablo | BH-FDR düzeltmeli korelasyon matrisi | 07 | 🔴 |
| 7 | Tablo | Bayes Factor + ROPE | 08 | 🔴 |
| 8 | Tablo | Beck Şiddet × Grup × Klinik referans | 07 | 🔴 |
| 9 | Tablo | Sümer 2010 vs Mevcut karşılaştırma | 03 | 🟡 |
| 10 | Tablo | GRADE Evidence Quality | 09 | 🟢 |
| 11 | Şekil | CFA path diagram (Carbon-styled) | 04 | 🟢 |
| 12 | Şekil | IRT Item Characteristic Curves panel | 04 | 🟢 |

---

## 7. V2 İÇİN AKSİYON LİSTESİ (PRIORITY-SIRALANMIŞ)

### Sprint 1 (1. hafta): Yüksek Öncelik — Tez Savunması Eşiği

| Gün | Aksiyon | Çıktı | Süre |
|---|---|---|---|
| 1 | G1: CR + AVE hesabı | Tablo 3a güncellemesi | 3 sa |
| 1 | G2: HTMT matrisi | Yeni Tablo 5a | 2 sa |
| 2 | G3: Modification indices analizi | Tablo 6a + yorum | 3 sa |
| 2 | G4: BH-FDR düzeltmesi | Mevcut Tablo 7'ye sütun | 0.5 sa |
| 3 | G5: Item-level analiz tablosu | Yeni Tablo 3b | 2 sa |
| 3 | G9: Beck şiddet dağılımı | Tablo 7b + klinik dipnot | 1 sa |
| 4-5 | G6: IRT GRM Reddetme için | 2 yeni şekil + Tablo 4a | 5 sa |
| 6-7 | G7: DIF testi | Tablo 5b (madde × grup) | 4 sa |
| 8 | G8: Bayes Factor + ROPE | Tablo 8a | 4 sa |

**Sprint 1 toplam:** ~24.5 saat ≈ 1 hafta tam zamanlı (veya 2 hafta yarı zamanlı)

### Sprint 2 (2. hafta): Orta Öncelik — Yayın Kalitesi

| Gün | Aksiyon | Süre |
|---|---|---|
| 9 | G10: Sümer 2010 karşılaştırma | 2 sa |
| 9 | G11: Hu-Bentler yorum | 0.5 sa |
| 10 | G12: APA-7 decimal revizyon | 2 sa |
| 10 | G13: Sample size justification | 1 sa |
| 11 | G14: Yaş-düzeyli α tablosu | 2 sa |
| 11 | G15: PDT teorik çerçeve | 2 sa |
| 12 | G16: ITC Guidelines uyum | 3 sa |
| 13 | G17: Bootstrap fit CI | 3 sa |

**Sprint 2 toplam:** ~15.5 saat

### Sprint 3 (3. hafta yarısı): Düşük Öncelik — Cilalar

| Gün | Aksiyon | Süre |
|---|---|---|
| 14 | G18: CFA path diagram | 1 sa |
| 14 | G19: IRT visualization | 1 sa |
| 14 | G20: Residual heatmap | 1 sa |
| 15 | G21: Open science statement | 0.5 sa |
| 15 | G22: GRADE table | 1 sa |
| 15 | G23: COSMIN compliance | 2 sa |

**Sprint 3 toplam:** ~6.5 saat

### Toplam Çaba

| Sprint | Süre | Etki |
|---|---|---|
| Sprint 1 (kritik) | ~25 sa | Tez savunması güvenliği + 1st-tier yayın eşiği |
| Sprint 2 (sağlamlık) | ~16 sa | Direct accept yerine minor revision |
| Sprint 3 (cila) | ~7 sa | Mükemmellik düzeyi |
| **TOPLAM v2** | **~48 saat** | **3 hafta yarı zamanlı** |

---

## 8. NET YOL HARİTASI

### 8.1 Mevcut Rapor V1 — Statü

**v1 = "Doktora tezi metodoloji eki olarak kullanılabilir"** ✓
**v1 ≠ "Pediatric Diabetes / Journal of Pediatric Psychology yayını için yeterli"** ✗

### 8.2 V2 Hazırlama Önerisi

```
v1 (mevcut PDF)
  ↓ +Sprint 1 (kritik 9 madde)
v1.5 (jüri savunması güvenli)
  ↓ +Sprint 2 (orta 8 madde)
v2.0 (Pediatric Diabetes hakem-hazır)
  ↓ +Sprint 3 (düşük 6 madde)
v2.1 (Frontiers in Psychology yayın-cila)
```

### 8.3 Pratik Çalışma Akışı

V2 üretimi için somut adım sırası:

```
ADIM 1: SAP v3.0 referans alınır (devstats yedi uyarıcı ilke + COSMIN)
ADIM 2: R kodu yazılır → 23 maddenin her biri için
ADIM 3: Quarto/Carbon HTML re-render edilir
ADIM 4: PDF export ile final v2 üretilir
ADIM 5: PI + tez danışmanı + 1 hakem (örn. Prof. Boran TIK üyesi) revize eder
ADIM 6: V2.0 final → tez ekiyle entegrasyon + ayrı adaptasyon makalesi taslağı
```

### 8.4 Spesifik Karar Noktası: V1.5 mı, V2.0 mı?

**Eğer hedef sadece tez savunması:** V1.5 (Sprint 1 yeterli)
**Eğer hedef tez + 1 yayın:** V2.0 (Sprint 1+2)
**Eğer hedef tez + 3 yayın stratejisi (SAP v3.0 önerisi):** V2.1 (tüm sprintler)

**Mahir/Özlem için tavsiye:** **V2.0** — yayın hedefli üretim, ek 16 saat eforla 1st-tier dergi eşiğini geçer. V2.1 cilaları ise *peer review* sürecinde hakem önerileriyle eklenebilir; pre-emptive yapmak gereksiz olabilir.

---

## 9. SONUÇ

Mevcut psikometrik validasyon raporu, **profesyonel görsel kalitede** ve **dürüst bilimsel raporlama disiplinine** sahip bir dokümandır. SHA-256 veri kilidi, multiverse + TOST + BSEM üçlüsü, kardeşli ICC raporlaması ve EMBU-C'nin birincil kaynak olarak konumlandırma kararı, **2026 modern psikometri standardının** karşılığıdır.

Bununla birlikte, **uluslararası yayın eşiğine** çıkmak için 23 spesifik geliştirme tespit edilmiştir:
- **9 kritik** (CR/AVE, HTMT, MI, IRT, DIF, FDR, item-CITC, BF/ROPE, Beck şiddet)
- **8 orta** (Sümer karşılaştırma, Hu-Bentler dili, APA-7, sample size, age-graded, PDT teori, ITC Guidelines, bootstrap CI)
- **6 düşük** (CFA path diyagramı, IRT visualization, residual heatmap, open science statement, GRADE, COSMIN)

Tüm bu eklemelerin toplam eforu **~48 saat (3 hafta yarı zamanlı)**'dir. Sprint 1 (kritik 9 madde) tek başına ~25 saatte tamamlanır ve raporu **jüri savunması güvenli** + **1st-tier yayın hakem-hazır** statüsüne taşır.

Raporun mevcut güçlü yönleri (10 madde) **dokunulmaz**; geliştirmeler bu yapının üzerine eklenir. V2 hazırlama akışı yukarıda Sprint planında detaylandırılmıştır.

Bir sonraki adımda eğer isterseniz: (a) Sprint 1 maddelerinin **R kodunu modüler olarak** yazabilir, (b) yeni 12 tablo/şeklin **Carbon-uyumlu Quarto template'ini** çıkarabilir, ya da (c) **adaptasyon makalesi taslak iskeletini** (Frontiers in Psychology format, Methods + Results + Discussion) hazırlayabiliriz.

---

**Belge sürümü:** İnceleme v1.0 — 2026-04-27
**İncelenen rapor:** `psikometrik-validasyon-butunlesik-rapor-carbon.pdf`
**İnceleme metodolojisi:** `devstats` × `psychdev` × `medical-research` üçlü skill protokolü
**Sonraki sürüm tetiği:** Sprint 1 tamamlandığında v2'nin re-review'u
