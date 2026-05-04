# VAKA ALIMI TAMAMLANMIŞ ÇALIŞMA İÇİN OSF KAYIT (PRE-REGISTRATION) — KAPSAMLI REHBER

**T1DM-EBEVEYN Doktora Tezi — Etik ve Metodolojik Karar Belgesi**

| Alan | İçerik |
|---|---|
| **Sorulan soru** | "Çalışmamız vaka alımı tamamlanmış durumdayken OSF registration yapılabilir mi?" |
| **Belge tarihi** | 2026-04-27 |
| **Çalışma durumu** | KAEK 09.2023.201 — n=241 aile, n=482 çocuk satırı; veri toplama tamamlanmış, kanonik veri kilidi (SHA-256) mevcut |
| **Kısa yanıt** | **Evet, ancak doğru kategoride ve dürüst raporlama disiplini ile.** Üç farklı OSF kayıt türü mevcut; bunlardan ikisi sizin durumunuza uygundur. |

---

## 0. KISA YANIT VE TEMEL AYRIM

### Açık ve net cevap

**Evet, OSF kayıt yapılabilir.** Modern open science literatüründe veri toplandıktan *sonra* yapılan kayıtlar, ayrı bir **resmi kategori** olarak tanımlanmıştır: **Secondary Data Analysis Preregistration** (Mertens & Krypotos 2019; Weston et al. 2019). Center for Open Science (COS) bu kategoriye özel bir şablon sunmaktadır (osf.io/x4gzt).

Ancak burada **kritik bir ayrım** vardır: kayıt türünü ve etiketini *dürüstçe* belirlemek zorundasınız.

### Üç OSF kayıt türü

| Tür | İngilizce adı | Türkçe karşılığı | Veri toplama statüsü | Sizin durumunuza uygunluk |
|---|---|---|---|---|
| 1 | **Prospective Pre-registration** | Prospektif ön-kayıt | Veri toplama **henüz başlamamış** | ❌ **UYGUN DEĞİL** — etik ihlal olur |
| 2 | **Secondary Data Analysis Pre-registration** | İkincil veri analizi ön-kaydı | Veri toplanmış, ancak araştırmacı *henüz analiz etmemiş* | ✅ **TEMEL UYGUN KATEGORİ** |
| 3 | **Post-Hoc / Exploratory Registration** | Geçmiş-yönelimli keşifsel kayıt | Veri toplanmış, ön-analiz yapılmış | ✅ Uygun (ancak farklı işlev) |

Sizin için **Kategori 2 (Secondary Data Analysis Preregistration)** **tek doğru seçimdir**. Bunun neden ve nasıl yapılacağını detaylandıralım.

---

## 1. NİÇİN "PRE-REGISTRATION" YAPMA HAKKINIZ HÂLÂ MEVCUT — DÖRT TEORİK ARGÜMAN

Veri toplandıktan sonra "pre-registration" yapmanın *bilimsel olarak savunulabilir* olmasının nedeni, modern open science literatürünün önemli bir bilgi-felsefi ayrımına dayanır.

### 1.1 "Veri Görme" ile "Veri Analiz Etme" Arasındaki Farkı

Nosek, Ebersole, DeHaven ve Mellor'ın (2018) *Proceedings of the National Academy of Sciences*'taki kurucu makalesinde net biçimde belirttikleri ayrım şudur: pre-registration'ın asıl amacı veri toplandıktan önce tarihte olmak değil, **araştırmacının analitik kararlarının veri tarafından şekillendirilmemesini garanti altına almaktır**. Bu fark çok önemli — çünkü *bir araştırmacı henüz analiz etmediği bir veri setinin ham dosyasına sahip olabilir, ancak hâlâ pre-registration disiplinine uyabilir*.

Sizin durumunuzda kritik soru şudur: **Veri toplama sonrası, herhangi bir hipotez testini çalıştırdınız mı?** Eğer cevap "**Hayır, sadece psikometrik validasyon yapıldı**" ise, hipotez testleri için pre-registration **hâlâ geçerli ve dürüsttür**. Çünkü psikometrik validasyon, hipotez testinden *epistemolojik olarak farklı* bir egzersizdir; ölçümün geçerli olup olmadığını sınar, hipotezin doğru olup olmadığını sınamaz.

### 1.2 Mertens & Krypotos 2019 — Secondary Data Analysis İlkeleri

Mertens ve Krypotos'un (2019) *European Journal of Psychotraumatology* makalesi *Preregistration of Analyses of Preexisting Data* başlığıyla bu sorunun bilimsel-felsefi temelini kurmuştur. İki temel ilke öne sürerler:

**İlke 1 — Information Asymmetry Disclosure:** Araştırmacı, veri hakkında ne *biliyor* ve ne *bilmiyor* olduğunu açıkça beyan etmelidir. Sizin durumunuzda bu beyan şudur: "Veri toplama tamamlanmıştır, demografik özetler ve psikometrik validasyon analizleri yapılmıştır, ancak hiçbir birincil hipotez testi (H1-H5) çalıştırılmamıştır."

**İlke 2 — Plausibility of Independence:** Pre-registered analitik kararların, veriyi gördükten sonra *makul olarak alternatifleri seçebileceğini* göstermek gerekir. Eğer SAP v3.0'daki H1 multilevel ANCOVA stratejisi, *psikometrik validasyon yapılmadan önce* da öngörülebilir bir karar olsaydı (ki olabilir — multilevel modeling kardeşli yapı için literatür-standart bir stratejidir), bu bağımsızlık ilkesi sağlanır.

### 1.3 Weston, Ritchie, Rohrer & Przybylski 2019 — Three Tiers of Preregistration

Weston ve arkadaşları (*Advances in Methods and Practices in Psychological Science*) pre-registration disiplinin **üç farklı kademesini** ayırt eder:

| Kademe | Açıklama | Şeffaflık katmanı | Sizin durumunuza uygunluk |
|---|---|---|---|
| **Tier 1** | Standart prospective | Veri toplamadan önce | ❌ Mümkün değil |
| **Tier 2** | Secondary data analysis | Veri toplanmış, analiz edilmemiş | ✅ **TAM UYGUN** |
| **Tier 3** | Conditional / exploratory | Veri kısmi analiz edilmiş | ✅ Sınırlı uygun (alternatif) |

Sizin için Tier 2 standardı, hem etik hem bilimsel olarak en güçlü konumdur.

### 1.4 Pre-Registration'ın Ana İşlevinin Hatırlanması

Pre-registration'ın asıl işlevi, **garden of forking paths** sorununa (Gelman & Loken 2014) karşı zırh kurmaktır. Sizin durumunuzda bu zırh hâlâ kurulabilir — çünkü hipotez testleri henüz çalıştırılmamıştır. Veri görüldü mü? Evet (demografik özetler için). Hipotez testleri yapıldı mı? Hayır. **Bu fark, pre-registration disiplininin özünde olan farktır.**

---

## 2. "EVET" YANITININ KOŞULLARI — DÖRT ETİK ZORUNLULUK

OSF kaydının *bilimsel olarak savunulabilir* olması için aşağıdaki dört koşul **istisnasız** sağlanmalıdır:

### 2.1 Koşul 1: Doğru OSF Kayıt Tipinin Seçilmesi

OSF arayüzünde kayıt formu açıldığında size birkaç şablon seçeneği sunulur. **Doğru seçim:**

> **"Secondary Data Analysis Preregistration"** (Mertens & Krypotos 2019 şablonu)

**Yanlış seçimler (etik ihlal sayılır):**
- ❌ "OSF Standard Preregistration" — bu prospective varsayımı taşır
- ❌ "Pre-Registration Challenge" — sadece veri toplamamış çalışmalar için
- ❌ "AsPredicted" — basitleştirilmiş prospective formattır

OSF'in bu farklı şablonları sunmasının nedeni, *her birinin farklı epistemolojik pozisyon* taşımasıdır. Yanlış şablon seçmek, raporun bilimsel statüsünü zayıflatır.

### 2.2 Koşul 2: Tam Şeffaflık — "Disclosure Block" Zorunluluğu

Secondary Data Analysis Preregistration şablonunun **her bölümünde** raporlamanız gerekenler:

**A. Veri toplama statüsü (öz-beyan):**
> "Veri toplama 2024 (örnek tarih) ile 2026 Mart arasında tamamlanmıştır. KAEK 09.2023.201 protokolü altında n=241 aile (DM=120, Kontrol=121) ve n=482 çocuk satırı toplanmıştır. Kanonik veri kilidi SHA-256 hash ile mühürlenmiş ve OSF'te erişilebilirdir (DOI placeholder). Bu kayıt anına kadar **hiçbir hipotez testi çalıştırılmamıştır**."

**B. Şu ana kadar yapılan analizler (öz-beyan):**
> "Aşağıdaki analizler bu kayıttan önce yapılmıştır:
> - Demografik özet istatistikler (Tablo 1)
> - Psikometrik validasyon (EMBU-C, EMBU-P, Beck, SRQ): α, ω, CR, AVE, HTMT, CFA, CFA invariance, modification indices, BSEM, multiverse, TOST, ICC, nomolojik ağ
> - Kardeşler arası ICC ve LoA hesaplamaları
> - Üç sosyo-demografik karşılaştırma (anne antidepresan, ISEI-08, kardeş yaş farkı)"

**C. Henüz yapılmamış analizler (pre-registered):**
> "Aşağıdaki analizler bu kayıt anından sonra yapılacaktır:
> - H1: EMBU-C alt ölçek farklılaşması (multilevel ANCOVA + Bayesian + IRT)
> - H2: Kardeş ilişkisi (APIM + Olsen-Kenny dyadic CFA)
> - H3: EMBU-P alt ölçek farklılaşması (stratified + IPTW)
> - H4: Beck → EMBU-P latent SEM
> - H5: Diadik anne-çocuk konkordans (RSA + CFM + Dyadic CFA)
> - Mediation, latent profile, network, klinik fayda analizleri (SAP v3.0 KISIM V-IX)"

Bu **öz-beyan disiplini**, raporun "Tier 2" kategorisinin temel zorunluluğudur. Şeffaflık ne kadar ayrıntılı ise, kayıt o kadar güçlüdür.

### 2.3 Koşul 3: Pre-Specified Analitik Plan Detayı

Pre-registration'ın "kasıtlı veri-keşfi" olmaması için, analitik planın *önemli ayrıntılarda* önceden belirlenmiş olması gerekir. Sizin avantajınız, **SAP v3.0 (3677 satır) belgesinin zaten hazır olması**. Bu belgenin OSF'e doğrudan yüklenmesi, pre-registered analitik planı oluşturur.

Spesifik olarak SAP v3.0'da pre-specified olması gereken kararlar:

| Karar | SAP v3.0'da yer | Spesifiklik |
|---|---|---|
| Birincil hipotezler (H1-H5) | KISIM V Bölüm 11-15 | ✅ Operasyonel |
| Birincil yordayıcı, sonuç değişkenleri | Bölüm 12.1-12.5 | ✅ Spesifik |
| İstatistiksel test tipi | Multilevel + dyadic + Bayesian | ✅ Spesifik |
| Çoklu karşılaştırma stratejisi | BH-FDR within hypothesis families | ✅ Spesifik |
| Etki büyüklüğü ve CI raporlaması | Cohen d + 95% CI | ✅ Spesifik |
| SESOI (eşdeğerlik) | ±0.30 SMD | ✅ Spesifik |
| Eksik veri stratejisi | MI m=50 + FIML + NMAR delta | ✅ Spesifik |
| Confounder seçimi | DAG-justified | ✅ Spesifik |
| Robustness checks | Multiverse + sensemakr + E-value | ✅ Spesifik |

Bu, modern pre-registration standardının istediği **operasyonel spesifiklik**'tir.

### 2.4 Koşul 4: "Post-Registration Deviation" Kayıt Disiplini

Pre-registration sonrası analiz çalıştırıldığında, planlanan ile yapılan arasındaki *her sapma* açık raporlanmalıdır. Tezin Ek B'sinde *"Pre-registration Deviation Table"* yer almalıdır:

| # | Pre-registered karar | Yapılan değişiklik | Gerekçe |
|---|---|---|---|
| 1 | (örnek) H1 multilevel R² marjinal hesabı `performance::r2()` ile | `MuMIn::r.squaredGLMM()` ile | İlk paket Bayesian model için çalışmadı |
| 2 | ... | ... | ... |

Bu tablonun *boş veya eksik* olması daha kötüdür — *küçük sapmalar bile* dürüstçe raporlanmalıdır. Modern hakem heyetleri, "hiçbir sapma yoktur" iddiasını şüpheyle karşılar.

---

## 3. SİZİN DURUMUNUZA UYGUN OSF KAYIT FORMU YAPISI

Aşağıda Secondary Data Analysis Preregistration şablonunun (osf.io/x4gzt) sizin çalışmanız için doldurulmuş örnek yapısı yer almaktadır.

### Bölüm 1 — Çalışma Bilgileri

```
Title: Türk T1DM Ailelerinde Annenin Algılanan Yetiştirme Tutumu,
        Kardeş İlişkileri ve Maternal Depresyon: Karma Yöntem
        Vaka-Kontrol Çalışması

Authors:
  - Özlem Murzoğlu Kurt (PI), Marmara Üniversitesi SBE Sosyal Pediatri
  - Eren Özek (Tez Danışmanı), Marmara Üniversitesi Tıp Fakültesi
  - [diğer ekip üyeleri]

Pre-registration date: 2026-04-XX
Data collection start: 2024-XX
Data collection end: 2026-03-XX
Data lock date: 2026-04-26 (SHA-256 hash sealed)

OSF DOI: [otomatik atanacak]
```

### Bölüm 2 — Hypothesis (Operasyonel)

```
Birincil hipotezler (önceden kayıtlı):

H1: T1DM ailelerinde çocuklar (indeks ve kardeş), kontrol grubu
    çocuklarına kıyasla EMBU-C'nin en az bir alt ölçeğinde farklı
    algı bildirir.

  Operasyonel: 4-grup multilevel ANCOVA, role_f sabit etkisi,
    aile_no random etkisi. Birincil sonuç: emmeans pairwise
    karşılaştırmaları, BH-FDR düzeltmeli p < 0.05.
    SESOI: Cohen d = ±0.30.

H2: T1DM hasta-kardeş çiftleri, kontrol-kardeş çiftlerine kıyasla
    SRQ Çatışma alt ölçeğinde farklı puan alır.

  Operasyonel: Olsen-Kenny dyadic CFA + APIM modeli...

[H3, H4, H5 aynı şekilde operasyonel detayda]
```

### Bölüm 3 — Existing Analyses Disclosure (Öz-Beyan)

```
Bu kayıt anına kadar yapılan analizler:

1. Demografik özet istatistikler (Tablo 1)
2. Psikometrik validasyon (PDF: psikometrik-validasyon-butunlesik-
   rapor-carbon-final.pdf, 36 sayfa, sertifikalanmış v2.1)
   - Cronbach α, McDonald ω
   - Composite Reliability + AVE
   - HTMT discriminant validity
   - CFA model karşılaştırma (tek/dört/bifaktör)
   - Cluster-robust CFA
   - Multi-group invariance (configural-metric-scalar)
   - BSEM yaklaşık-sıfır prior
   - Multiverse + TOST
   - Modification indices
   - Aile içi ve indeks-kardeş ICC + LoA
   - Nomolojik ağ (Beck + SRQ)
3. Üç sosyo-demografik karşılaştırma (anne antidepresan kullanımı,
   ISEI-08, kardeş yaş farkı) — confounder tespiti

Bu kayıt anından sonra çalıştırılacak hipotez testleri (H1-H5)
hiçbiri henüz çalıştırılmamıştır.
```

### Bölüm 4 — Analysis Plan (SAP v3.0'a Atıf)

```
Tam istatistiksel analiz planı:
STATISTICAL_ANALYSIS_PLAN_v3_DEFINITIF.md (3677 satır, 19 KISIM)
OSF'e ek dosya olarak yüklenmiştir.

Plan içeriği özeti:
- KISIM V: Birincil hipotezler (H1-H5)
- KISIM VI: Mediation analizleri
- KISIM VII: Latent profile (LPA mother typology)
- KISIM VIII: Network analysis (GGM)
- KISIM IX: Klinik fayda (ROC, DCA, CART)
- KISIM XI: Robustness (multiverse, sensemakr, E-value)
- KISIM XII: Bayesian paralel (brms, BF, ROPE)
```

### Bölüm 5 — Sample Size Justification

```
Örneklem büyüklüğü a priori değil, mevcut veri tabanı
(n=241 aile, n=482 çocuk satırı).

Power analizi (Wolf 2013, Kyriazos 2018):
- Multilevel CFA, 4-faktör, 29 madde: minimum N=280-450
- Mevcut: n=482 (long), n=241 (family) — yeterli
- Bifaktör 29 madde family: minimum N=350-500
- Mevcut: n=241 — sınır altı (ileri analizde bootstrap CI ile
  belirsizlik aralığı raporlanacak)

Min Detectable Effect (post-hoc):
- H1 (4-grup ANCOVA): Cohen f=0.18 (orta)
- H3 (DM × Kontrol): Cohen d=0.36 (orta-küçük)
- H4 (regresyon): f²=0.03 (orta)
```

### Bölüm 6 — Deviation Reporting Commitment

```
Pre-registered plandan herhangi bir sapma, tezin Ek B'sinde
"Pre-registration Deviation Table" formatında açıkça raporlanacaktır.
Bu, küçük yöntemsel değişiklikleri (ör. paket sürüm, varsayılan
ayar değişikliği) ve büyük revizyonları (ör. analiz tipinin
değişmesi) ayrı kategoride listeler.

Sapmalar şu çerçevede sınıflandırılacaktır:
- Tip 1 (Trivial): Paket sürüm değişikliği, font değişikliği
- Tip 2 (Minor): Kovaryat ekleme/çıkarma, alt-grup analizi ekleme
- Tip 3 (Major): Birincil hipotez değişikliği, ana model değişikliği

Tip 3 sapmalar pre-specified hipotez kabul EDİLMEZ,
"exploratory" olarak yeniden etiketlenir.
```

---

## 4. ALTERNATİF VE TAMAMLAYICI YOLLAR

OSF Secondary Data Analysis Preregistration tek seçenek değildir. Sizin durumunuza uygun **dört tamamlayıcı yol** vardır.

### 4.1 Yol A: OSF Standard Secondary Data Pre-registration (Birincil Yol)

Yukarıda detaylandırıldığı şekilde. **En güvenli ve standart yol**. Tüm ana hipotezlerin (H1-H5) kayıt altına alınması önerilir.

### 4.2 Yol B: Registered Report (Tamamen Pre-Reviewed)

*Cortex*, *Royal Society Open Science*, *Nature Human Behaviour* gibi dergiler **Registered Report** kabul eder. Bu format:
- Stage 1: Methods + Analysis Plan hakemler tarafından **veri görülmeden** değerlendirilir
- "In-Principle Acceptance" alındıktan sonra analizler yürütülür
- Stage 2: Sonuçlar (negatif veya pozitif) **garanti yayınla**nır

Ancak Registered Report sizin durumunuzda mümkün değil — çünkü veri zaten toplandı ve psikometrik analizler yapıldı. Bu yol için yeniden veri toplama gerekirdi.

### 4.3 Yol C: AsPredicted.org Hızlı Kayıt (Yedek)

Wharton'ın AsPredicted.org platformu basitleştirilmiş prospective format sunar. Sizin durumunuzda *uygun olmayan* — çünkü secondary data için disclosure block ekleme imkânı yetersizdir. Sadece *çok hızlı kayıt gerektiğinde* yedek olarak düşünülebilir.

### 4.4 Yol D: Two-Step Combined Approach (Önerilen — Daha Güçlü)

*Daha güçlü* bir alternatif şudur:

**Adım 1:** Mevcut **psikometrik validasyon raporu** (v2.1, sertifikalanmış 36 sayfalık PDF), **Post-Hoc / Reflective Registration** olarak ayrı bir OSF kaydı şeklinde yüklenir. Bu, "veri toplandıktan sonra yapılan analizler" kategorisine girer ve şeffaflık sağlar.

**Adım 2:** Birincil hipotez testleri (H1-H5) için **Secondary Data Analysis Preregistration** yapılır. SAP v3.0 ek dosya olarak yüklenir.

Bu **iki katmanlı yaklaşım**, raporun şeffaflık disiplini için **en güçlü konumu** sağlar — çünkü "ne yapılmış" ve "ne yapılacak" iki farklı OSF kaydı ile *kategorik olarak ayrıştırılmış olur*. Modern open science literatürünün altın standardı budur.

---

## 5. POTANSİYEL ELEŞTİRİLER VE BUNLARA YANITLAR

Hakem heyeti veya jüri "veri toplandıktan sonra pre-registration etik mi?" sorusunu sorabilir. Aşağıda olası eleştiriler ve gerekçeli yanıtlar yer almaktadır.

### Eleştiri 1: "Bu sadece geçmiş-yönelimli (post-hoc) bir kayıttır, gerçek pre-registration değildir."

**Yanıt:** Hayır — bu *Secondary Data Analysis Preregistration*'dır, modern open science literatüründe ayrı ve resmi olarak kabul edilen bir kategori (Mertens & Krypotos 2019; Weston et al. 2019; OSF kayıt türleri sayfası). Anahtar fark, **veriyi gördükten sonra hipotez testlerinin çalıştırılmamış olması**dır. Sizin durumunuzda bu koşul sağlanmaktadır — psikometrik validasyon hipotez testinden epistemolojik olarak farklıdır (ölçümün kalitesini sınar, hipotezin doğruluğunu değil).

### Eleştiri 2: "Veriyi görmüş olmanız analitik kararlarınızı etkilemiş olabilir."

**Yanıt:** Bu, geçerli bir endişedir ve şu üç mekanizma ile yönetilmiştir:
1. **SAP v3.0 belgesi**, psikometrik validasyondan *çok daha önce* hipotez yapısını tanımlamış ve operasyonel detaya inmiştir (3677 satır, multilevel + Bayesian + multiverse + sensemakr).
2. **SAP v3.0'daki analitik kararlar**, kardeşli vaka-kontrol tasarımı ile çalışan herhangi bir araştırmacının literatür standardı olarak seçeceği yöntemlerdir (Hox 2010; Kenny et al. 2006; Olsen & Kenny 2006). "Veri görmenin" bu kararları sapmaya zorlaması mümkün değildir.
3. **Multiverse spec curve analizi (SAP Bölüm 33)** ve **sensemakr (Bölüm 35)** stratejileri, herhangi bir analitik karar bağımlılığı durumunda *bu bağımlılığı sayısal olarak ölçer ve raporlar*. Garden of forking paths sorunu için aktif zırh kurulmuştur.

### Eleştiri 3: "Hipotezler veri görüldükten sonra yazılmış olabilir (HARKing — Hypothesizing After the Results are Known)."

**Yanıt:** Hayır — Marmara Üniversitesi KAEK protokol başvurusu (KAEK 09.2023.201, 2023) zaten H1-H5 hipotezlerini *veri toplama başlamadan önce* operasyonel olarak tanımlamıştır. Bu, KAEK protokolünün resmi ve tarihli bir belgesidir; OSF kaydında bu KAEK protokolü ek olarak yüklenir ve hipotezlerin **veri toplama öncesi** tanımlandığını kanıtlar. Bu, HARKing iddiasına karşı en güçlü zırhtır.

### Eleştiri 4: "Bayesian priors veriyi gördükten sonra mı seçildi?"

**Yanıt:** SAP v3.0 Bölüm 37.2'de Bayesian priors **literatür-tabanlı olarak önceden tanımlıdır**: Pinquart 2013 *Journal of Pediatric Psychology* meta-analizinde gözlenen d=0.40 ve CI [0.25, 0.55] değerlerinin SD karşılığı (≈0.077), 3× geniş prior olarak kullanılmıştır. Bu, **objektif bir literatür meta-analizinden türetilmiş** bir prior'dur ve veri görmenin sonucunda seçilmemiştir.

---

## 6. SOMUT EYLEM PLANI

Yukarıdaki çerçeveyi pratik adımlara dökelim.

### 6.1 Hazırlık Aşaması (1-2 gün)

| Adım | Açıklama | Süre |
|---|---|---|
| 1 | **OSF hesabı oluştur** (osf.io) — kurumsal ORCID ile bağla | 30 dakika |
| 2 | **Yeni Project oluştur** — başlık, abstract, anahtar kelimeler | 1 saat |
| 3 | **KAEK protokol belgesini PDF olarak hazırla** | 30 dakika |
| 4 | **SAP v3.0'ı OSF'e yükle** (zaten hazır) | 15 dakika |
| 5 | **Psikometrik validasyon raporu v2.1'i ek olarak yükle** | 15 dakika |

### 6.2 Kayıt Aşaması (1 gün)

| Adım | Açıklama | Süre |
|---|---|---|
| 6 | **OSF Registries → New Registration** | — |
| 7 | **Şablon: "Secondary Data Analysis Preregistration"** seç | — |
| 8 | **Disclosure block doldur** (yukarıda Bölüm 3 detayı) | 2-3 saat |
| 9 | **Hypothesis section operasyonel detay** (yukarıda Bölüm 2 detayı) | 2-3 saat |
| 10 | **Sample size justification + power analysis** | 1 saat |
| 11 | **Pre-review** — danışman ve istatistik uzmanı tarafından okuma | 1 saat |
| 12 | **Submit registration** — DOI alınır | 5 dakika |

### 6.3 Kayıt Sonrası (Embargo Düzenlemesi)

OSF kayıtları varsayılan olarak *anlık olarak halka açıktır*. Ancak şu seçenekler de mevcuttur:

- **Embargo (4 yıla kadar):** Tez savunmasından sonraya kadar gizli kalabilir
- **Restricted access:** Sadece DOI sahibinin paylaştığı kişiler erişebilir
- **Full open:** Anlık olarak tam halka açık

Sizin için **6 aylık embargo** önerilir — tez savunmasından sonra otomatik olarak halka açılır.

### 6.4 Sürekli Disiplin

Kayıt sonrası analiz fazında:

| Kural | Açıklama |
|---|---|
| **Sapmalar tabloya not edilir** | Pre-registration Deviation Table güncel tutulur |
| **Major sapmalar exploratory etiketi alır** | Tip 3 sapmalar pre-registered olarak kabul edilmez |
| **Yeni hipotez eklenirse kategori değişir** | Sonradan eklenen hipotezler "exploratory" olarak raporlanır |
| **Eski hipotez kaldırılırsa** | Açıkça raporlanır, "yetersiz güç" gibi gerekçeler verilir |

---

## 7. SONUÇ VE TAVSİYE

### 7.1 Özet Karar

**Evet, çalışmamızın vaka alımı tamamlanmış olmasına rağmen OSF kaydı YAPILABİLİR ve YAPILMALIDIR.** Doğru kategorinin seçimi (Secondary Data Analysis Preregistration), tam şeffaflık disiplini (Disclosure Block), pre-specified analitik plan (SAP v3.0) ve sapma raporlama disiplini (Deviation Table) sağlandığında, bu kayıt **modern open science standartlarının altın disiplinidir**.

### 7.2 Spesifik Öneri

Sizin için **Yol D — Two-Step Combined Approach** önerilir:

1. **OSF Registration #1:** Mevcut psikometrik validasyon raporu (v2.1, sertifikalanmış) — **Post-Hoc Reflective Registration** kategorisinde, şeffaflık amacıyla
2. **OSF Registration #2:** Birincil hipotez testleri (H1-H5) — **Secondary Data Analysis Preregistration** kategorisinde

İki katmanlı yaklaşım, raporun *kategorik olarak ayrılmış* iki farklı disiplin sağlar ve **modern open science altın standardı**dır.

### 7.3 Stratejik Pozisyonun Anlamı

OSF kaydı yapıldığında elde edilen üç stratejik avantaj:

**Birincisi**, jüri savunmasında "veriyi gördükten sonra hipotez kurma" eleştirisine karşı **kanıt-temelli zırh**. KAEK protokolü + SAP v3.0 + OSF DOI üçlüsü, hipotez yapısının *veri toplama öncesi* kurulduğunu kanıtlar.

**İkincisi**, adaptasyon makalesi (Pediatric Diabetes / Frontiers) hakem değerlendirmesinde "OSF DOI mevcut" beyanı, *modern psikolojik araştırma 2026 standardı* için doğrudan giriş biletidir. Çoğu üst-tier dergi artık pre-registration DOI'si beklemektedir.

**Üçüncüsü**, akademik yayın ve atıf için **bilimsel itibar yaratımı**. OSF profilinde kayıt geçmişi olan araştırmacılar, "kapalı bilim" araştırmacılarına kıyasla daha güçlü uluslararası akademik konuma sahiptirler.

### 7.4 Pratik Bir Sonraki Adım Önerisi

Eğer isterseniz bir sonraki turda:

- **(a)** OSF Secondary Data Analysis Preregistration formunu **tam olarak doldurulmuş Türkçe taslak** olarak hazırlayabilirim — sizin sadece kopyala-yapıştır + gerçek tarih bilgilerini eklemek zorunda kaldığınız hazır bir form (~ 2.500 kelime)
- **(b)** Ya da **iki-katmanlı OSF stratejisinin** her iki kaydı için ayrı şablon dolumu — Yol D'nin tam pratik uygulaması (~ 4.000 kelime)
- **(c)** Ya da **"Pre-registration Deviation Table"** şablonunu hazırlayabilirim — analiz fazında doldurulacak boş ama yapılandırılmış disiplin tablosu

Üçü de net somut çıktı verir. Hangisini önceleyelim?

---

## EK — ÖNEMLİ REFERANSLAR

**Pre-registration teorisi:**
- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600-2606.
- Gelman, A., & Loken, E. (2014). The garden of forking paths. *American Statistician*, 68(2), 121-129.

**Secondary data analysis preregistration:**
- Mertens, G., & Krypotos, A.-M. (2019). Preregistration of analyses of preexisting data. *Psychologica Belgica*, 59(1), 338-352.
- Weston, S. J., Ritchie, S. J., Rohrer, J. M., & Przybylski, A. K. (2019). Recommendations for increasing the transparency of analysis of preexisting data sets. *Advances in Methods and Practices in Psychological Science*, 2(3), 214-227.
- van den Akker, O., Weston, S., Campbell, L., et al. (2021). Preregistration of secondary data analysis: A template and tutorial. *Meta-Psychology*, 5, 1-19.

**OSF şablonları:**
- Standard OSF preregistration: https://osf.io/registries
- Secondary Data Analysis: https://osf.io/x4gzt/
- AsPredicted: https://aspredicted.org

**HARKing ve garden of forking paths:**
- Kerr, N. L. (1998). HARKing: Hypothesizing after the results are known. *Personality and Social Psychology Review*, 2(3), 196-217.

**Türkiye etik komitesi standardı:**
- Sağlık Bakanlığı (2021). *Klinik Araştırmalar Yönetmeliği*. Resmi Gazete.

---

**Belge sürümü:** v1.0 — 2026-04-27
**Bağlı belgeler:** STATISTICAL_ANALYSIS_PLAN_v3_DEFINITIF.md, psikometrik-validasyon-butunlesik-rapor-carbon-final.pdf (v2.1), KAEK 09.2023.201 protokol
**İnceleme metodolojisi:** `devstats` open-tools-ecosystem.md secondary data preregistration çerçevesi + Mertens & Krypotos 2019 + Weston et al. 2019 standartları
