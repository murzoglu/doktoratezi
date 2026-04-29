---
title: "Tip 1 Diyabetli Çocuklar, Sağlıklı Kardeşleri ve Annelerinde Ebeveynlik Tutumlarının Vaka-Kontrol Çalışması"
subtitle: "Klinik Çalışma Raporu (ICH E3 Uyumlu Bütünleşik Sürüm)"
author:
  - Uzm.Dr. Özlem Murzoğlu Kurt
  - Prof.Dr. Eren Özek (Tez Danışmanı)
  - Doç.Dr. Belma Haliloğlu (Yardımcı Araştırıcı)
date: "2026-04-29"
study-protocol: "MÜTF-KAEK 09.2023.201"
csr-version: "v1.1 — Tezsel CSR (Doktora Savunması Sürümü, sistematik denetim sonrası revize)"
sap-version: "v3.0 — DEFİNİTİF FİNAL (2026-04-27)"
data-lock: "FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock (2026-04-26)"
osf-registrations: "d524q (psikometrik) · pytfe (secondary data preregistration) · vqrt5 (proje)"
language: tr
abstract-title: "Sinopsis"
---

\newpage

# 1 · KAPAK BİLGİLERİ VE ÇALIŞMA TANIMI

| Alan | İçerik |
|---|---|
| **Çalışma başlığı** | Tip 1 Diyabet Tanılı Çocuklar, Sağlıklı Kardeşleri ve Annelerinin Ebeveynlik Tutumlarına Yönelik Algılarının Sağlıklı Kontrol Grubu ile Karşılaştırılarak İncelenmesi ve Kardeşler Arası İlişkilerin Değerlendirilmesi |
| **Kısa başlık** | T1DM-EBEVEYN Vaka-Kontrol Çalışması |
| **Çalışma protokolü** | KAEK Protokol Kodu **09.2023.201** (06.01.2023) |
| **Enstitü onayı** | 2023/19-68 (11.05.2023) |
| **Çalışma tipi** | Tek-merkezli, gözlemsel, vaka-kontrol, kesitsel, çok-bilgi-veren (multi-informant), aile-içi düad tasarımlı psikososyal araştırma |
| **Yürütücü kurum** | Marmara Üniversitesi Sağlık Bilimleri Enstitüsü, Sosyal Pediatri Doktora Programı |
| **PI / Doktora öğrencisi** | Uzm.Dr. Özlem Murzoğlu Kurt |
| **Tez danışmanı** | Prof.Dr. Eren Özek (MÜTF Neonatoloji) |
| **Yardımcı araştırıcı** | Doç.Dr. Belma Haliloğlu (MÜTF Pediatrik Endokrinoloji) |
| **TİK üyeleri** | Prof.Dr. Perran Boran; Prof.Dr. Nalan Karabayır |
| **Veri toplama dönemi** | Ocak 2023 – Eylül 2025 |
| **Embargo durumu** | 6 aylık embargo onayı bekleniyor; tez savunmasından sonra otomatik açılım |
| **Raporlama standardı** | STROBE (gözlemsel) + JARS-Quant (APA) + TRIPOD (klinik tahmin modeli) |
| **CSR sürümü** | v1.1 (Doktora savunması sürümü, 29 Nisan 2026) |

> **Reproducibility ve ön-kayıt teknik referansı:** Veri kilidi (26 Nisan 2026), `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` SHA-256 mührü, SAP v3.0, OSF kayıtları (`d524q` psikometrik validasyon · `pytfe` H1–H5 secondary data preregistration · `vqrt5` proje) ve yazılım yığını (R 4.5.3 + Quarto 1.6 + `targets` + `renv` + Stan 2.32) Bölüm 4.4 Pre-Registration Disiplini ve Bölüm 8.4 Veri Yönetimi ve Kanonik Kilit altında ayrıntılı belgelenmiştir.

---

# 2 · SİNOPSİS

## 2.1 Çalışmanın Amacı

Bu vaka-kontrol çalışması, Tip 1 Diyabet (T1DM) tanılı pediatrik hastaların ailelerinde ebeveynlik tutumlarının, anne mental sağlık göstergelerinin ve kardeş ilişkisi mimarisinin sağlıklı kontrol aileleriyle karşılaştırmalı olarak incelenmesini amaçlamıştır. Çalışma, beş ön-kayıtlı birincil hipotez (H1–H5) ile yedi keşifsel analiz katmanını (KISIM VI–XII) birleştirerek; ebeveyn-çocuk algı uyumsuzluğunun, anne depresif belirtilerinin ebeveynlik aracılı yansımalarının ve klinik göstergelerin (HbA1c, hastalık süresi) aile psikososyal ortamı ile ilişkisini test etmeyi hedeflemiştir.

## 2.2 Çalışma Tasarımı

Tek-merkezli, kesitsel, vaka-kontrol tasarımı; her ailede üç katılımcı (anne + indeks çocuk + sağlıklı kardeş) ile multi-informant ve aile-içi düad yapısı. Birincil maruziyet *grup üyeliği* (DM vs Kontrol); birincil sonuçlar EMBU-C alt ölçekleri (çocuk algı), EMBU-P alt ölçekleri (anne öz-rapor), Beck Depresyon Envanteri toplam puanı (anne) ve SRQ alt ölçekleri (kardeş ilişkisi).

## 2.3 Örneklem

Toplam **241 aile** kanonik analiz tabanına dahil edilmiştir: **120 DM ailesi** (her birinde 1 anne + 1 T1DM tanılı indeks çocuk + 1 sağlıklı biyolojik kardeş) ve **121 Kontrol ailesi** (her birinde 1 anne + 2 sağlıklı çocuk). Uzun-format çocuk düzeyi veri seti **482 satır** içermektedir.

## 2.4 Birincil Hipotez Bulguları (Yönetici Özeti)

| Hipotez | Bulgu | Etki Büyüklüğü | Bayesyen Kanıt | TOST Eşdeğerlik |
|---|---|---|---|---|
| **H1 Çocuk algısı (EMBU-C)** | Çocuk algısında dört anlamlı bulgu: DM indeks aşırı koruma (β = 0.20, p = .010) ve reddetme (β = 0.15, p = .003); DM kardeş sıcaklık (β = 0.16, p = .029) ve reddetme (β = 0.14, p = .009). En tutarlı bulgu reddetme algısının hem indekste hem kardeşte yükselmesidir. | Reddetme için β = 0.16 SD, %95 GA [0.05, 0.26], pd = 0.999 | **BF₁₀ = 8.12** (moderate H1 lehine) | — |
| **H2 Kardeş ilişkisi (SRQ)** | Dört SRQ alt ölçeğinin tümünde DM × Kontrol fark kanıtı yetersiz | \|d\| < 0.20, FDR p > .35 | — | — |
| **H3 Anne öz-rapor (EMBU-P)** | Dört EMBU-P alt ölçeğinde grup farkı yok | \|d\| < 0.17, FDR p > .50, max SMD 0.220 → 0.004 (IPTW) | BF₁₀ = 0.17–0.25 (moderate H0 lehine); ROPE içi pay reddetmede %92 | Aşırı koruma + karşılaştırma "Equivalent"; sıcaklık + reddetme "Indeterminate" |
| **H4 Beck → EMBU-P latent SEM** | Anne depresyonunun ebeveynlik tutumlarıyla ilişkisi orta-büyük; 4 yapısal yoldan 3'ü FDR-düzeltmeli anlamlı | Anlamlı yollar için \|std. β\| = 0.28–0.33; aşırı koruma std. β = 0.08, FDR p = .216 | Bayesyen dual reporting planlandı / paralel hatla yorumlandı | — |
| **H5 Diadik tutarlılık** | Anne öz-rapor ↔ çocuk algısı zayıf-orta düzeyde eşleşiyor; DM grubunda marjinal yüksek | Olsen-Kenny latent r: Kontrol = 0.17, DM = 0.29 | 5/5 strateji çalıştı | — |

## 2.5 Sensitivite ve Robustluk Özeti

- **Multiverse (KISIM XI/33):** 120 spesifikasyondan **%0** spec'te p < .05 (sağlam null); araştırmacı serbestliğine karşı tam dayanıklılık.
- **Sensemakr Robustness Value (Cinelli & Hazlett, 2020):** RV_q = 0.04–0.08 (zayıf gözlemlenmemiş karıştırıcı dayanıklılığı).
- **E-değeri (VanderWeele & Ding, 2017):** 1.36–1.59 (zayıf-orta düzey).
- **Bayesyen yakınsama (KISIM XII):** H3 modellerinde R̂ < 1.01; H1 modellerinde R̂ = 1.012–1.013 ile sıkı 1.01 eşiğinin hafif üzerindedir ancak yaygın 1.05 eşiğinin altındadır. Divergent transition = 0; sonuçlar bu tanı notuyla birlikte raporlanmıştır.

## 2.6 Sonuç

Bulgular, T1DM aile sisteminde **anne öz-rapor ile çocuk algısı arasında sistematik bir asimetri** sergilemektedir: anne tarafından bildirilen ebeveynlik davranışlarında DM × Kontrol farkı yokken, çocuk algı düzeyinde reddetme alt ölçeğinde DM lehine küçük-fakat-tutarlı bir yükseliş gözlenmiştir. Anne depresyonunun ebeveynlik tutumları üzerindeki latent etkisi her iki grupta da büyüklük olarak önemlidir. Bu örüntü, De Los Reyes ve diğerlerinin (2015) Operations Triad Modeli çerçevesinde "Diverging Operations" olarak okunabilir ve Türk pediatrik T1DM popülasyonunda *aile-merkezli, çift-perspektifli psikososyal değerlendirme* gerekliliğini ampirik olarak desteklemektedir.

---

\newpage

# 3 · KISALTMALAR VE TANIMLAR

| Kısaltma | Açılım |
|---|---|
| **ADA** | American Diabetes Association |
| **AUC** | Area Under the Curve (eğri altındaki alan) |
| **APIM** | Actor-Partner Interdependence Model (oyuncu-partner karşılıklı bağımlılık modeli) |
| **AVE** | Average Variance Extracted (ortalama açıklanan varyans) |
| **BCa** | Bias-corrected and accelerated bootstrap |
| **BDI** | Beck Depression Inventory (Beck Depresyon Envanteri) |
| **BF₁₀** | Bayes Factor (alternatif hipotez lehine kanıt oranı) |
| **BSEM** | Bayesian Structural Equation Model |
| **CART** | Classification and Regression Trees |
| **CFA** | Confirmatory Factor Analysis (doğrulayıcı faktör analizi) |
| **CFI** | Comparative Fit Index |
| **CFM** | Common Fate Model (ortak yazgı modeli) |
| **CR** | Composite Reliability |
| **CSR** | Clinical Study Report (klinik çalışma raporu) |
| **DAG** | Directed Acyclic Graph (yönlü asiklik graf) |
| **DCA** | Decision Curve Analysis |
| **DM** | Diabetes Mellitus (Tip 1, çalışma kapsamında) |
| **EMBU-C** | s-EMBU çocuk formu (algılanan ebeveynlik) |
| **EMBU-P** | s-EMBU ebeveyn formu (anne öz-rapor) |
| **FDR** | False Discovery Rate (yanlış keşif oranı, Benjamini-Hochberg) |
| **FIML** | Full Information Maximum Likelihood |
| **GA** | Güven Aralığı |
| **GGM** | Gaussian Graphical Model |
| **HbA1c** | Glikolize hemoglobin (glisemik kontrol göstergesi) |
| **HC3** | Heteroscedasticity-consistent SE (sürüm 3) |
| **HTMT** | Heterotrait-Monotrait Ratio |
| **ICC** | Intra-class Correlation Coefficient |
| **ICH E3** | International Council for Harmonisation, Clinical Study Report standart kılavuzu |
| **IPTW** | Inverse Probability of Treatment Weighting |
| **IRT** | Item Response Theory |
| **ISEI-08** | International Socio-Economic Index of Occupational Status, 2008 sürümü |
| **ISPAD** | International Society for Pediatric and Adolescent Diabetes |
| **JARS-Quant** | APA Journal Article Reporting Standards, Quantitative |
| **KAEK** | Klinik Araştırmalar Etik Kurulu |
| **KİA** | Kardeş İlişkileri Anketi (= SRQ Türkçe varyantı) |
| **LPA** | Latent Profile Analysis |
| **LRT** | Likelihood Ratio Test |
| **MAR** | Missing at Random (rastgele eksik) |
| **MI** | Multiple Imputation (çoklu atama) |
| **NCT** | Network Comparison Test |
| **NICE** | National Institute for Health and Care Excellence |
| **NMAR** | Not Missing at Random (rastgele olmayan eksik) |
| **NRI/IDI** | Net Reclassification / Integrated Discrimination Improvement |
| **OSF** | Open Science Framework |
| **PII** | Personally Identifiable Information (kişisel tanımlayıcı bilgi) |
| **PD** | Probability of Direction |
| **PDT** | Parental Differential Treatment (ebeveyn diferansiyel davranışı) |
| **RMSEA** | Root Mean Square Error of Approximation |
| **ROPE** | Region of Practical Equivalence (pratik eşdeğerlik bölgesi) |
| **RSA** | Response Surface Analysis (yanıt yüzeyi analizi) |
| **RV_q** | Robustness Value at q% (Cinelli-Hazlett duyarlılık göstergesi) |
| **SAP** | Statistical Analysis Plan |
| **SES** | Socioeconomic Status (sosyoekonomik durum) |
| **SESOI** | Smallest Effect Size of Interest (ilgilenilen en küçük etki büyüklüğü) |
| **SEM** | Structural Equation Model |
| **SHA-256** | Secure Hash Algorithm 256-bit (kriptografik dosya imzası) |
| **SMD** | Standardized Mean Difference |
| **SRMR** | Standardized Root Mean Square Residual |
| **SRQ** | Sibling Relationship Questionnaire |
| **STROBE** | Strengthening the Reporting of Observational Studies in Epidemiology |
| **T1DM** | Type 1 Diabetes Mellitus |
| **TOST** | Two One-Sided Tests (iki tek-yanlı eşdeğerlik testi) |
| **TRIPOD** | Transparent Reporting of a multivariable prediction model for Individual Prognosis or Diagnosis |
| **WLSMV** | Weighted Least Squares with Mean and Variance adjustment (ordinal estimator) |
| **ω** | McDonald's Omega (güvenirlik katsayısı) |

---

\newpage

# 4 · ETİK KURUL VE DÜZENLEYİCİ ÇERÇEVE

## 4.1 Etik Onay

Çalışma protokolü, Marmara Üniversitesi Tıp Fakültesi Klinik Araştırmalar Etik Kurulu (KAEK) tarafından **6 Ocak 2023** tarihinde **09.2023.201** protokol numarasıyla onaylanmıştır. Marmara Üniversitesi Sağlık Bilimleri Enstitüsü doktora tez izni **2023/19-68** numarasıyla 11 Mayıs 2023 tarihinde verilmiştir.

## 4.2 Bilgilendirilmiş Onam

Tüm anneler, çalışmaya katılım öncesinde yazılı bilgilendirilmiş onam vermiştir; pediatrik katılımcılar (7–17 yaş) için ayrı yaşa-uygun onam formları kullanılmıştır. Onam süreci, 18 yaş altı çocukların sözel onayını (assent) ve velilerin yazılı izinini birlikte içermektedir.

## 4.3 Veri Yönetimi ve Mahremiyet

Çalışma, KVKK ve genel veri minimizasyonu ilkelerine uygun olarak yürütülmüştür. Veri sınıflandırma matrisi:

- **L0 (Açık metadata):** SAP, protokol özeti, kanonik form dokümantasyonu, analiz kodu, aggregate raporlar — commit edilebilir / OSF'e yüklenebilir.
- **L1 (De-identified analiz verisi):** `FINAL_REFERENCE__analysis_base_*.csv` — controlled access; public yüklenmez.
- **L2 (Kaynak/ara veri):** `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/` — commit edilmez.
- **L3 (Kimlik/credential):** `.env`, servis hesabı dosyaları, kimlik bilgileri — yalnız PI erişimi.

Tüm doğrudan tanımlayıcı kolonlar (ad, soyad, TC kimlik, telefon, e-posta, dosya/protokol/MRN, açık adres) Stage 1 standardizasyonunda kalıcı olarak düşürülmüş; yeniden tanımlama riskini sıfıra yaklaştırmak için kontrol-akışı veri minimizasyonu prensibi çerçevesinde sürdürülmüştür.

## 4.4 Pre-Registration Disiplini

Çalışma iki katmanlı OSF preregistration ile kayıtlanmıştır: (i) **Layer 1 (`d524q`)** psikometrik validasyon için reflective registration, (ii) **Layer 2 (`pytfe`)** H1–H5 birincil hipotezleri için secondary data preregistration. Proje deposu `vqrt5` numarasıyla OSF'te yer almaktadır. Embargo süresi 6 aydır; tez savunmasından sonra DOI atanır ve veri/kod paketi açılır. Pre-registered plandan yapılan tüm sapmalar `PRE-REGISTRATION-DEVIATION-TABLE.md` dosyasında Tip 1 (trivial), Tip 2 (minor) veya Tip 3 (major) olarak sınıflandırılmaktadır.

## 4.5 Çıkar Çatışması ve Finansman

Doktora tez çalışmasının yürütücüsü tarafından beyan edilen finansal veya ticari çıkar çatışması bulunmamaktadır. Çalışma, Marmara Üniversitesi SBE doktora programı kurumsal kaynaklarıyla yürütülmüştür.

---

\newpage

# 5 · ARAŞTIRMACILAR VE ÇALIŞMA YÖNETİMİ

| Rol | Kişi | Kurum / Bölüm |
|---|---|---|
| Birincil araştırmacı / Doktora öğrencisi | Uzm.Dr. Özlem Murzoğlu Kurt | Marmara Üniversitesi SBE Sosyal Pediatri |
| Tez danışmanı | Prof.Dr. Eren Özek | Marmara Üniversitesi Tıp Fakültesi Neonatoloji |
| Yardımcı araştırıcı (klinik) | Doç.Dr. Belma Haliloğlu | MÜTF Pediatrik Endokrinoloji |
| Tez İzleme Komitesi (TİK) | Prof.Dr. Perran Boran | MÜTF Sosyal Pediatri |
| Tez İzleme Komitesi (TİK) | Prof.Dr. Nalan Karabayır | MÜTF Sosyal Pediatri |

İstatistik desteği R 4.5.3 + Quarto 1.6+ + `targets` + `renv` + Stan 2.32+ teknoloji yığını üzerinden yürütülmüştür.

---

\newpage

# 6 · GİRİŞ VE ARKA PLAN

## 6.1 Bilimsel Gerekçe

Tip 1 Diyabet, çocukluk çağının en yaygın endokrin kronik hastalıklarından biridir; günlük insülin yönetimi, glisemik takip ve diyet uyumu gerektirmesi nedeniyle aile sistemini sürekli ve özgün bir biçimde etkilemektedir. Türkiye'de pediatrik T1DM ulusal prevalansı 0.75/1000 olarak raporlanmıştır (Yeşilkaya ve diğerleri, 2017); bölgesel insidans son dönemde 13.1/100.000 düzeyine yükselme eğilimi göstermektedir (Vuralli ve diğerleri, 2024). Bu epidemiyolojik tablo, T1DM ailelerinde aile-merkezli psikososyal destek gereksinimini her geçen yıl artırmaktadır.

Pinquart'ın (2013) 325 çalışmayı içeren meta-analizi, kronik hastalığı olan çocukların ailelerinde ebeveyn-çocuk ilişkisinde küçük negatif (g = −0.16) ve aşırı korumada görece büyük (g = 0.39) etki büyüklükleri bildirmiştir. Ne var ki bu havuzlanmış bulguların *Türk T1DM örnekleminde* sistematik olarak tekrarlanıp tekrarlanmadığı; ebeveyn ve çocuk perspektiflerinin uyum / uyumsuzluğunun anne mental sağlığıyla nasıl etkileştiği; ve kardeş ilişkisi mimarisinin hastalık deneyiminden ne ölçüde etkilendiği ampirik olarak yetersiz incelenmiştir.

ISPAD 2024 Klinik Pratik Konsensüs Kılavuzları'nın PsychoSocial Care bölümü ve ADA Standards of Care 2025/2026 (Madde 14.9–14.11) T1DM tanılı çocukların **tanı anında ve rutin takipte** çoklu informant tabanlı, valide araçlarla psikososyal taramaya tabi tutulmasını şart koşmaktadır. NICE Guideline NG18 aynı doğrultuda aile-merkezli bakım, ergen-bağımsızlık geçişi ve davranış sağlığı uzmanlarının pediatrik takıma entegrasyonunu vurgulamaktadır. Bu çalışma, söz konusu klinik kılavuzların *çift-perspektifli aile değerlendirmesi* önerilerini Türk popülasyonunda operasyonelleştiren ampirik bir prototip olarak konumlandırılmaktadır.

## 6.2 Multi-İnformant Çerçevenin Kuramsal Konumu

De Los Reyes ve diğerleri (2015) tarafından *Psychological Bulletin* dergisinde 341 çalışmayı havuzlayan meta-analizde, anne-çocuk algı korelasyonlarının ortalaması içselleştirme alanında r = 0.25, dışsallaştırma alanında r = 0.30 ve toplam alanda r = 0.29 olarak rapor edilmiştir. De Los Reyes ve diğerlerinin (2023) Operations Triad Modeli, bilgi-veren uyumsuzluğunu üç desende ele almaktadır: Converging Operations (uyum), Diverging Operations (anlamlı, bağlam-spesifik gerçek farklılık) ve Compensating Operations (yöntemsel sapma). Multi-informant çerçeve, uyumsuzluğun *ölçüm hatası* değil **alana ilişkin bilgi** olarak okunmasını öngörmekte; bu, klinik müdahale planlamasında *kim, ne, nerede* sorularına farklılaşmış yanıtlar üretebilmektedir.

## 6.3 Çalışmanın Boşluğu Doldurduğu Alan

Mevcut literatürde T1DM Türk popülasyonunda; (i) anne öz-rapor ile çocuk algısının paralel ölçüldüğü, (ii) sağlıklı kardeşin de aynı ölçek setiyle değerlendirildiği, (iii) propensity score yöntemleriyle gözlenebilir karıştırıcıların kontrol edildiği, (iv) Bayesyen dual reporting ile null bulguların yorumlandığı ve (v) çoklu sensitivite katmanıyla araştırmacı serbestliğinin denetlendiği kapsamlı bir vaka-kontrol çalışması bulunmamaktadır. Bu çalışma, bu beş eksiği eşzamanlı kapatma iddiasıyla yürütülmüştür.

---

\newpage

# 7 · AMAÇLAR VE HİPOTEZLER

## 7.1 Birincil Amaçlar

1. T1DM ailelerinde çocuk perspektifinden algılanan ebeveynlik tutumlarının (EMBU-C alt ölçekleri) Kontrol ailelerinden farklılaşıp farklılaşmadığını belirlemek (**H1**).
2. T1DM kardeş çiftlerinde kardeş ilişkisi mimarisinin (SRQ alt ölçekleri) Kontrol kardeş çiftlerinden farklılaşıp farklılaşmadığını test etmek (**H2**).
3. T1DM annelerinin öz-rapor ettikleri ebeveynlik davranışlarının (EMBU-P alt ölçekleri) Kontrol annelerinden farklılaşıp farklılaşmadığını incelemek (**H3**).
4. Anne depresif belirti yükünün (BDI) ebeveynlik tutumları (EMBU-P) üzerindeki latent etkisini yapısal eşitlik modeliyle tahmin etmek (**H4**).
5. Anne öz-rapor ile çocuk algısı arasındaki diadik tutarlılığı (Olsen-Kenny dyadic CFA dahil beş paralel strateji ile) DM ve Kontrol grupları arasında karşılaştırmak (**H5**).

## 7.2 Birincil Hipotezler (Ön-Kayıtlı, OSF `pytfe`)

| Kod | Hipotez | İstatistiksel test |
|---|---|---|
| **H1** | T1DM tanılı çocuklar, EMBU-C reddetme alt ölçeğinde Kontrol gruplarından daha yüksek puan alacaktır. | 4-grup multilevel ANCOVA + IRT GRM + Bayesyen brms |
| **H2** | T1DM kardeş çiftleri, SRQ çatışma alt ölçeğinde Kontrol kardeş çiftlerinden daha yüksek puan alacaktır. | Aile-mean Welch + APIM + Olsen-Kenny dyadic CFA |
| **H3** | T1DM anneleri, EMBU-P aşırı koruma alt ölçeğinde Kontrol annelerinden daha yüksek puan alacaktır. | ANCOVA + antidepresan-stratified + IPTW + HC3 |
| **H4** | Anne depresif belirti yükü (BDI total), EMBU-P alt ölçek latent yapısını anlamlı düzeyde yordayacaktır. | WLSMV ordinal latent SEM + multi-group invariance + Bayesyen blavaan |
| **H5** | Anne öz-rapor ile çocuk algısı arasındaki diadik tutarlılık DM grubunda Kontrol grubundan farklı olacaktır. | 5 paralel strateji: ICC + Bland-Altman; RSA Edwards-Parry; CFM lavaan; Olsen-Kenny dyadic CFA; k-coefficient APIM |

## 7.3 İkincil Amaçlar (Keşifsel)

KISIM VI–XII başlıkları altında düzenlenmiştir: mediation modelleri (KISIM VI), latent profil analizi (KISIM VII), ağ analizi (KISIM VIII), klinik fayda analizi (KISIM IX), DM klinik alt-analizler (KISIM X), robustluk-sensitivite (KISIM XI) ve Bayesyen paralel hat (KISIM XII).

## 7.4 SESOI ve İstatistiksel Eşik Kararları

- **SESOI:** Cohen d = ±0.30 SMD (TOST eşdeğerlik testleri için)
- **FDR:** Benjamini-Hochberg, q = .05, hipotez ailesi içinde uygulanır
- **Pinquart prior:** d = 0.40, %95 GA [0.25, 0.55] → Bayesyen modellerde 3× geniş bilgilendirici prior
- **ROPE konvansiyonu (Kruschke, 2018):** ±0.10 d standardize parametre için negligible bölgesi

---

\newpage

# 8 · ARAŞTIRMA PLANI VE METODOLOJİ

## 8.1 Tasarım

Tek-merkezli, gözlemsel, vaka-kontrol, kesitsel tasarım. Aile başına üç katılımcı (anne, indeks çocuk, kardeş) ve aile-içi düad yapısı. Veri, kâğıt anket formları ile yüz yüze toplanmış; daha sonra elektronik forma dönüştürülerek dijital veri tabanına aktarılmıştır.

## 8.2 Katılımcı Seçimi

### 8.2.1 Dahil Etme Kriterleri

- **DM grubu:** ISPAD 2018 kriterlerine göre Tip 1 DM tanısı almış, en az 6 ay önce tanı konmuş, 7–17 yaş arası indeks çocuklar; aynı haneyi paylaşan en az bir sağlıklı biyolojik kardeşe sahip olmak.
- **Kontrol grubu:** Bilinen kronik hastalığı olmayan, 7–17 yaş arası indeks çocuklar; aynı haneyi paylaşan en az bir sağlıklı biyolojik kardeşe sahip olmak.

### 8.2.2 Dışlama Kriterleri

- Pediatrik nörogelişimsel tanı (otizm spektrumu, Down sendromu vb.)
- Aktif onkolojik veya psikiyatrik komorbidite
- Anneye ait psikotik bozukluk tanısı
- Türkçe okuma-yazma yetersizliği (ölçek doldurmayı engelleyen düzeyde)
- Eksik onam imzası

## 8.3 Ölçek Bataryası

| Ölçek | Madde sayısı | Likert | Bilgi-veren | Türkçe uyarlama |
|---|---|---|---|---|
| **EMBU-P** (anne formu) | 29 | 4'lü | Anne öz-rapor | Castro ve diğerleri (1997) temelli; Türk yetişkin verisinde α = 0.64–0.79 (Dirik ve diğerleri, 2015) |
| **EMBU-C** (çocuk formu) | 29 | 4'lü | Çocuk algı (her ailede iki rapor: indeks + kardeş) | s-EMBU-Children Türkçe form, q25 ters skorlanmış olarak saklanır |
| **BDI** (Beck Depresyon Envanteri) | 21 | 0–3 | Anne öz-rapor | Hisli (1989) Türkçe uyarlama; α = 0.80 |
| **SRQ / KİA** (Kardeş İlişkileri Anketi) | 48 | 5'li | Çocuk algı (her ailede iki rapor) | Furman & Buhrmester (1985) temelli; Türkçe uyarlama (Yurdabakan ve diğerleri, 2016) |

## 8.4 Veri Yönetimi ve Kanonik Kilit

Final analiz veri seti **`FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`** dosyasıyla kriptografik olarak mühürlenmiştir (SHA-256 hash imzası). Kilit dosyası iki kanonik CSV'yi indeksler:

- **Family dosyası:** 241 satır × 288 sütun (her satır bir aile)
- **Long dosyası:** 482 satır × 203 sütun (her satır bir çocuk × aile düzeyi alanlar)

`R/01_io.R::validate_and_load()` fonksiyonu altı-adımlı doğrulama zinciri uygular: (1) lock objesi parse, (2) status doğrulama, (3) CSV path eşleşmesi, (4) SHA-256 hash karşılaştırma, (5) satır/sütun sayısı manifestesi, (6) targets DAG imzası. Zincirin herhangi bir adımı kırılırsa pipeline `stop()` ile sonlanır; bypass mümkün değildir.

## 8.5 Yapısal Eksiklik Kuralları

| Kolon | Yapısal NA koşulu |
|---|---|
| `embu_p_q01..q29` | `is_index == FALSE` (kardeş satırlarında) |
| `beck_1..beck_21` | `is_index == FALSE` (kardeş satırlarında) |
| `dm_yili`, `hba1c`, `dm_tani_tarihi` | `role != "DM_Hasta_Indeks"` |
| `es_isco08_*`, `es_isei08`, `es_siops08`, `es_egp7` | `es_calisma_durumu == 0` ve `es_emekli == 1` |
| `beck_total` | 21 maddeden herhangi biri eksikse beck_total NA olarak işlenir; eksik-tolerans uygulanmaz |

**Kritik kural:** HbA1c yapısal eksiklik (kontrol/kardeş satırlarında tanım gereği yok) nedeniyle imputasyona alınmaz; klinik biyobelirteç tahmin edilemez. DM grubunda %32.5 (39/120) tamamlanma oranıyla yalnız `[KEŞİFSEL]` etiketli alt-analizlerde kullanılır.

## 8.6 İstatistiksel Analiz Planı (SAP v3.0) Özeti

SAP, beş ana katmandan oluşmaktadır:

1. **KISIM I–II Meta-altyapı + Veri katmanı:** Pre-registration, reprodüktiblik (renv + Docker + targets), etik/veri yönetimi, hash doğrulama, türetilmiş skor ekosistemi, SES kompoziti, çoklu-çerçeve eksik veri (MI m=50 + FIML + NMAR delta).
2. **KISIM III Tanımlayıcı + Denge:** Tablo 1 + SMD; nedensel DAG; propensity score (IPTW + matching) + doubly robust ANCOVA.
3. **KISIM IV Psikometrik Validasyon:** CFA + IRT + ω + AVE/CR + HTMT + DIF + invariance (ayrı doküman; özetleri Bölüm 10'da).
4. **KISIM V Birincil Hipotezler (H1–H5):** ANCOVA + multilevel + APIM + WLSMV SEM + dyadic CFA.
5. **KISIM VI–XII İkincil + Robustluk + Bayesyen:** Mediation, LPA, network, klinik fayda, DM alt-analizler, multiverse + TOST + sensemakr + brms dual reporting.

## 8.7 Çoklu Karşılaştırma Disiplini

Birincil analizler (H1–H5) Benjamini-Hochberg FDR ailesi içinde düzeltilmiştir (q = .05). Aileler:

- **H1 ailesi:** 4 EMBU-C alt ölçeği × group_f testi
- **H2 ailesi:** 4 SRQ alt ölçeği × DM-Kontrol testi
- **H3 ailesi:** 4 EMBU-P alt ölçeği × DM-Kontrol testi
- **H4 ailesi:** 4 yapısal yol (Beck → EMBU-P alt ölçek)
- **H5 ailesi:** 3 dyad-tipi × 4 alt ölçek

Aileler arası FDR uygulanmamış; her aile bağımsız düzeltilmiştir.

## 8.8 Kovaryat Seti ve Nedensel DAG

**Birincil ayarlama seti (DAG-justified):** {AgeGap (kardeş yaş farkı); FamilySize (aile çocuk sayısı); SES_latent (Bourdieu üç-sermaye kompozit z-skoru)}. Anne yaşı, anne eğitim seviyesi, eş eğitim seviyesi, ISEI-08 mesleki indeksi gibi gözlemlenebilir karıştırıcılar IPTW ağırlıklamasıyla kontrol edilmiştir. Antidepresan kullanımı, H3 analizinde stratifiye duyarlılık değişkeni olarak işlenmiştir.

---

\newpage

# 9 · ÇALIŞMA POPÜLASYONU

## 9.1 Aile Yapısı ve Örneklem Akışı

Toplam 241 aile kanonik analiz tabanına dahil edilmiştir: 120 DM ailesi ve 121 Kontrol ailesi. Her aileden 1 anne, 1 indeks çocuk ve 1 kardeş katılımıyla **482 çocuk satırı** uzun-format kanonik tabana yazılmıştır.

DM grubunda indeks çocuk T1DM tanısı taşımakta; kardeş ise sağlıklı biyolojik kardeştir. Kontrol grubunda hem indeks hem kardeş sağlıklıdır. Üç-veya-daha-fazla çocuklu ailelerde anne-çocuk-kardeş üçlüsü için indeks ile en yakın yaşlı kardeş seçilmiştir.

## 9.2 Demografik Profil — Tablo 1 Özeti

| Değişken | Kontrol (n=121) | DM (n=120) | SMD | Yorum |
|---|---|---|---|---|
| Anne yaşı (yıl, medyan) | 37.3 | 38.5 | **0.21** | Dengesiz eşiği |
| Çocuk yaşı (yıl, medyan) | 11.2 | 12.0 | 0.07 | Dengeli |
| İndeks çocuk Kız oranı | %48 | %52 | < 0.10 | Dengeli |
| Kardeş Kız oranı | %50 | %48 | < 0.10 | Dengeli |
| Aynı cinsiyet kardeş çifti | %42 | %44 | 0.03 | Dengeli |
| Kardeş yaş farkı (yıl, medyan) | 3.0 | 3.0 | < 0.10 | Dengeli |
| Aile çocuk sayısı (medyan) | 2.4 | 2.4 | < 0.10 | Dengeli |
| Anne antidepresan kullanımı | %9 | %29 | **0.53** | **Ciddi dengesiz** |
| Anne eğitim seviyesi (ordinal) | — | — | **0.29** | Dengesiz |
| Eş eğitim seviyesi (ordinal) | — | — | **0.32** | Dengesiz |
| Aile ISEI-08 mesleki indeks | — | — | **0.23** | Dengesiz |
| Eş ISEI-08 mesleki indeks | — | — | **0.23** | Dengesiz |
| Beck şiddet kategorisi | — | — | 0.11 | Sınırda |
| Beck total ortalama | ~ 6.8 | ~ 6.8 | < 0.10 | Dengeli |
| Latent SES kompozit (z) | 0.0 | 0.0 | **0.03** | İyi denge |

**Yorum:** Ham gözlemde dört değişkende dengesizlik tespit edilmiştir. En güçlü dengesizlik anne antidepresan kullanımındadır (DM grubunda %29 vs Kontrol %9; SMD = 0.53, ciddi eşik üzeri); bu, T1DM annelerinin yaklaşık 3.2 katı yüksek antidepresan kullanım oranına işaret etmektedir. Bu bulgu, kronik hastalık çocuklu annelerin yüksek psikiyatrik bakım yüküne dair literatür ile tutarlıdır (Cousino & Hazen, 2013; Bassi ve diğerleri, 2020).

Eğitim ve mesleki indeks dengesizlikleri (SMD 0.23–0.32), latent SES kompoziti (Bourdieu üç-sermaye, polikorik PCA + CFA) düzeyinde silinmiştir (SMD = 0.03). Latent SES, H3 birincil analizinde DAG-justified ayarlama setinin bir bileşeni olarak kullanılmıştır.

## 9.3 DM Klinik Profili

| Klinik gösterge | Değer |
|---|---|
| DM grubunda HbA1c veri tamamlanması | 39/120 (%32.5) |
| HbA1c medyan | 9.0 % |
| HbA1c ortalama | 8.97 % |
| HbA1c minimum / maksimum | 5.8 / 15.1 |
| HbA1c plauzibilite aralığı dışı | 0 |
| Tanı yaşı medyan | 7.8 yıl |
| DM süresi medyan | 3.9 yıl |

**Yorum:** Medyan HbA1c değeri 9.0%, ISPAD 2024 kılavuzunun pediatrik glisemik hedef eşiği (< 7.0%) üzerindedir; bu, çalışma popülasyonunun glisemik kontrol açısından Türk pediatrik T1DM kohortlarının ortalama profili ile tutarlı olduğunu (Vuralli ve diğerleri, 2024) ve klinik müdahale gereksiniminin yüksek bir alt grupta yoğunlaştığını göstermektedir. Tanı yaşı medyanı 7.8 yıl olup okul çağında tanı almış çocukların baskın olduğunu işaret eder. DM süresi medyanı 3.9 yıl, orta süreli kronik bakım deneyimini gösterir.

## 9.4 Propensity Score Dengeleme Sonucu

Birincil propensity modeli (logistic regression: anne yaşı + anne eğitim seviyesi + eş eğitim seviyesi + ISEI-08 + ses_latent + cocuk_sayisi + age_gap + ev_sahipligi + arabaniz_var_mi → group_dm) ile stabilize trimlenmiş ağırlıklar (99. persentil cap) hesaplanmıştır.

**Denge sonucu:**
- Ham gözlemde maksimum |SMD| = **0.220** (anne antidepresan haricinde; antidepresan kovaryat yapılmamış stratifiye değişkendir)
- IPTW sonrası maksimum |SMD| = **0.004**
- **Geliştirme:** −0.216 birim SMD redüksiyonu

Doubly robust ANCOVA + HC3 robust standart hata kullanımı, model misspecification'a karşı çift koruma sağlamıştır.

## 9.5 Eksik Veri Profili

`R/12_missing_data_frames.R` üç-katmanlı çerçeve uygular: (i) FIML birincil hat, (ii) MI (mice, m=50, maxit=30) doğrulama hattı, (iii) NMAR delta-adjustment grid sensitivite hattı.

| Değişken bloğu | Eksik veri oranı | Mekanizma | Çerçeve |
|---|---|---|---|
| Aile-düzeyi sosyodemografi | < %5 | MAR | MI + FIML birincil |
| EMBU-P (anne) | yapısal NA kardeş satırlarda | MNAR-yapısal | İmputasyona alınmaz |
| Beck (anne) | yapısal NA kardeş satırlarda | MNAR-yapısal | İmputasyona alınmaz |
| HbA1c | %67.5 DM grubunda | MNAR-yapısal | **İmputasyona alınmaz** (klinik biyobelirteç) |

Eksik veri çerçevesinin sayısal kilidi `missing_frame_manifest.csv` ile doğrulanmıştır: FIML birincil çerçeve **241 aile × 37 değişken** içerir; bu çerçevede **215 tam satır**, **26 analitik eksik hücre**, **0 yapısal eksik hücre** vardır. Complete-case birincil çerçeve **215 aile × 37 değişken** ile aynı değişken setinde eksiksiz analiz alt kümesini oluşturur. MI birincil çerçeve yine **241 aile × 37 değişken** üzerinden yürür ve 26 analitik eksik hücreyi MAR varsayımı altında ele alır. Klinik duyarlılık çerçevesi **241 aile × 39 değişken** içerir; HbA1c yalnız DM ailesinde mevcut olduğundan **30 tam satır**, **349 toplam eksik hücre**, **242 yapısal eksik hücre** ve **107 analitik eksik hücre** ile ayrı, imputasyonsuz duyarlılık alanı olarak tutulmuştur.

---

\newpage

# 10 · PSİKOMETRİK VALIDASYON BULGULARI (KISIM IV)

Bu bölüm, COSMIN/ITC/JARS-Quant uyumlu 35 sayfalık `psikometrik-validasyon-butunlesik-rapor-carbon-final.pdf` dokümanının özetini sunmaktadır. Tam sürüm `docs/analiz_planlari/PSIKOMETRIK-VALIDASYON-BUTUNLESIK-RAPOR.qmd` çıktısında mevcuttur.

## 10.1 İç Tutarlılık (Cronbach α + McDonald ω)

EMBU-P ve EMBU-C alt ölçeklerinde toplam puan ile alt ölçek puanlarının iç tutarlılık katsayıları hesaplanmıştır. **EMBU-P Reddetme** alt ölçeğinde α ve ω değerleri her iki katsayıda da düşük seviyede tespit edilmiştir; bu paralellik (alpha ve omega birlikte düşük) sorunun yalnız α'nın varsayım kısıtlarından (eşit faktör yükleri) değil, **madde havuzunun bu örneklemde ürettiği zayıf ortak sinyal** ve faktör homojenliğinden kaynaklandığını işaret etmektedir. EMBU-C reddetme alt ölçeğinde bu sorun daha az belirgin olup, reddedici ebeveynlik içeriğinin çocuk bildiriminde anne öz-bildirimine kıyasla daha tutarlı yakalandığını düşündürmektedir.

Reddetme alt ölçeği için tam sayısal güvenilirlik profili şöyledir: EMBU-P Reddetme **8 madde**, **n = 241**, Cronbach α_raw = **.45**, α_std = **.47**, α %95 GA \[.34, .55\], McDonald ω_total = **.48**, ω_h = **.46**, ortalama madde-arası korelasyon = **.10**. EMBU-C Reddetme **8 madde**, **n = 479**, Cronbach α_raw = **.72**, α_std = **.74**, α %95 GA \[.68, .75\], McDonald ω_total = **.75**, ω_h = **.74**, ortalama madde-arası korelasyon = **.27**. Bu nedenle anne formunda reddetme boyutu güçlü doğrulayıcı ölçüm kanıtı olarak değil, sınırlılık ve duyarlılık odağı olarak; çocuk formunda ise daha tutarlı fakat yine taban etkisinden etkilenmiş bir algı göstergesi olarak kullanılmıştır.

## 10.2 Faktör Yapısı (CFA Karşılaştırması)

| Form | Tek faktör | Dört faktör | Bifaktör |
|---|---|---|---|
| EMBU-P | CFI düşük | CFI orta, SRMR yüksek | Karşılaştırma fonksiyonu |
| EMBU-C | CFI düşük | CFI sınırda, SRMR uygun | Karşılaştırma fonksiyonu |

Hu-Bentler (1999) birleşik kriter (CFI ≥ .95 + SRMR ≤ .08) **karşılanmamıştır**; dört-faktör çözümü tek-faktör alternatife göre göreli iyileşme göstermekle birlikte yapısal model olarak mutlak doğrulanmış değildir. Bu durum, "kullanılabilir ancak sınırlı faktör kanıtı" olarak raporlanmaktadır. Aile-kümelenmesine duyarlı sürekli-MLR cluster CFA, ordinal CFA'nın yerini almak yerine aile içi bağımlılığın model uyumuna etkisinin tamamlayıcı bir kontrolü olarak eklenmiştir.

## 10.3 Madde Düzeyi Taban Etkisi

EMBU-P ve EMBU-C ölçeklerinin reddetme alt ölçeğindeki birden fazla madde ≥ %80 taban etkisi sergilemiştir; bu dağılım kısıtı, korelasyon, CFA yükü ve grup farkı tahminlerini sistematik olarak aşağı çekme eğilimindedir. EMBU-P Reddetme alt ölçeğinde **8/8 madde > %60 taban etkisi**, **7/8 madde > %80 taban etkisi** göstermiştir; madde düzeyi floor aralığı **%62.2406639004149–%95.850622406639** düzeyindedir. EMBU-C Reddetme alt ölçeğinde **6/8 madde > %60 taban etkisi**, **3/8 madde > %80 taban etkisi** göstermiştir; madde düzeyi floor aralığı **%39.7916666666667–%84.4398340248963** düzeyindedir. Reddetme sonuçlarının yalnız toplam puan düzeyinde değil, **madde dağılımı düzeyinde de temkinli okunması** gerektiği vurgulanmıştır.

## 10.4 Ölçüm Değişmezliği (Multi-Group Invariance)

Configural, metric ve scalar düzeyler grup (DM × Kontrol), yaş ve cinsiyet kategorileri için sırayla test edilmiştir. Scalar düzey grup ortalaması karşılaştırmaları için kritik öneme sahiptir; bu çalışmada konfigural ve metric invariance büyük ölçüde sağlanmış, scalar invariance sınır düzeyde kabul edilmiştir. Δ CFI < 0.010 + ΔRMSEA < 0.015 kriterleri Cheung & Rensvold (2002) standardıyla raporlanmaktadır.

## 10.5 Kriter ve Eşzamanlı Geçerlik (Nomolojik Ağ)

EMBU-P/C alt ölçekleri, Beck total ve SRQ alt ölçekleri arasında 14 paralel korelasyon testi uygulanmış; tüm korelasyon p-değerleri Benjamini-Hochberg FDR ailesi içinde düzeltilmiştir. Anne reddetmesi ile anne depresif belirtileri arasında orta-büyük ilişki, çocuk algısında karşılaştırma alt ölçeği ile SRQ çatışma alt ölçeği arasında güçlü ilişki gözlenmiştir.

## 10.6 Genel Psikometrik Karar

EMBU-P/C ve BDI ölçeklerinin Türk T1DM örnekleminde **kullanılabilir ancak sınırlı geçerlik kanıtı** sergilediği sonucuna varılmıştır. Reddetme alt ölçeğinin görece zayıf psikometrik profili, bu boyutta gözlenen birincil hipotez bulgularının (özellikle H1) latent SEM ve Bayesyen yaklaşımlarla desteklenmesini gerektirmiştir; bu yaklaşımlar Bölüm 11.1'de detaylıdır.

---

\newpage

# 11 · BİRİNCİL HİPOTEZ BULGULARI (KISIM V)

## 11.1 H1 — Çocuk Algısı (EMBU-C × 4 grup, multilevel ANCOVA + IRT GRM + Bayesyen)

### 11.1.1 Birincil Model

`R/16_h1_child_perception.R::run_h1_primary()` fonksiyonu, dört EMBU-C alt ölçeği için aşağıdaki modeli uygulamıştır:

```
embu_c_<alt_olcek>_mean ~ role_f + cocuk_yas_z + cinsiyet_f +
                          ses_latent_z + age_gap_z + cocuk_sayisi_z +
                          (1 | aile_no_f)
```

Burada `role_f` 4-düzeyli faktördür: Kontrol_İndeks (referans), Kontrol_Kardeş, DM_Hasta_İndeks, DM_Hasta_Kardeş.

### 11.1.2 Sonuçlar

- **EMBU-C Reddetme:** DM çocukları (DM_Hasta_İndeks + DM_Hasta_Kardeş) Kontrol grubuna göre **β = 0.16 SD** [%95 GA: 0.05, 0.26], pd = 0.999 düzeyinde yüksek puan vermiştir. FDR-düzeltilmiş p < .01.
- **EMBU-C Sıcaklık, Aşırı Koruma, Karşılaştırma:** Üç alt ölçekte DM × Kontrol farkı kanıtı yetersiz; FDR-düzeltilmiş p > .15.

### 11.1.3 Bayesyen Replikasyon (KISIM XII)

Pinquart 2013 meta-analizinden türetilen bilgilendirici prior (β ~ Normal(0.30, 0.15)) altında brms multilevel model (4 zincir × 4000 yineleme; R̂ ≤ 1.01, divergent transition = 0):

| EMBU-C alt ölçek | Posterior medyan β | %95 Cr.I | BF₁₀ | Yorum |
|---|---|---|---|---|
| **Reddetme** | 0.18 | [0.05, 0.30] | **8.12** | Moderate H1 lehine |
| Sıcaklık | -0.04 | [-0.16, 0.08] | 0.29 | Moderate H0 lehine |
| Aşırı Koruma | 0.06 | [-0.06, 0.18] | 0.41 | Anectodal H0 lehine |
| Karşılaştırma | 0.09 | [-0.04, 0.21] | 0.55 | Anectodal H0 lehine |

### 11.1.4 IRT GRM Replikasyonu

Reddetme alt ölçeği için Graded Response Model (GRM, mirt paketi) latent θ skorları hesaplanmıştır. DM × Kontrol latent θ farkı multilevel ANCOVA'nın puanlanmış sonucuyla aynı yön ve büyüklükte (β = 0.14 SD, %95 GA [0.04, 0.25]), bu da reddetme bulgusunun ölçek düzeyinden bağımsız sağlam olduğunu göstermektedir.

### 11.1.5 Üçlü Etkileşim (Tanı Modeli)

Üçlü etkileşim modeli (`role_f * cocuk_yas_z * cinsiyet_f`) FDR-düzeltilmiş p > .20 düzeyinde anlamlı bulunmamıştır; reddetme bulgusu yaş × cinsiyet alt gruplarında homojendir.

### 11.1.6 Karar

H1 reddetme alt ölçeği için **moderate kanıt birikimi** (frequentist + Bayesyen + IRT) DM lehine küçük-orta (d ≈ 0.16–0.18) etki büyüklüğünde bir farkı desteklemektedir.

---

## 11.2 H2 — Kardeş İlişkisi (SRQ × 4 alt ölçek)

### 11.2.1 Üç Paralel Strateji

`R/17_h2_sibling_relationships.R` fonksiyonu üç paralel strateji yürütmüştür:

1. **Aile-mean Welch t-testi:** Her ailedeki iki çocuğun SRQ alt ölçek ortalaması alınarak DM × Kontrol Welch testleri uygulanmış.
2. **Long-format APIM:** `outcome ~ group_f * family_role_f + age_gap_z + (1|aile_no_f)` karma modeli.
3. **Olsen-Kenny Distinguishable Dyad CFA:** SRQ çatışma maddeleri için dyadic CFA.

### 11.2.2 Sonuçlar

| SRQ alt ölçek | Welch d | APIM grup × rol p | FDR p |
|---|---|---|---|
| Sıcaklık/Yakınlık | < 0.20 | > .30 | > .35 |
| Çatışma | < 0.20 | > .30 | > .35 |
| Statü | < 0.20 | > .30 | > .35 |
| Rekabet | < 0.20 | > .30 | > .35 |

Dört SRQ alt ölçeğinde DM × Kontrol fark kanıtı **yetersiz** olarak değerlendirilmiştir. APIM 4 modelin tümü yakınsamış; Olsen-Kenny çatışma item dyadic CFA uyum sağlamış ve indeks-kardeş latent korelasyonu **r = .27** olarak raporlanmıştır. Bu değer kardeş ilişkisi alanında zayıf-orta ortak varyans olduğunu, ancak DM × Kontrol farkı için doğrulayıcı kanıt üretmediğini gösterir. **Not:** H2 için TOST eşdeğerlik testi *bu ön-kayıt sürümünde uygulanmamıştır*; bu nedenle "fark yoktur" yerine "fark kanıtı yetersizdir" ifadesi raporlanmıştır (kanıt yetersizliği aktif eşdeğerlikten farklıdır).

### 11.2.3 Yaş Farkı × Aynı Cinsiyet Moderasyonu

Aile-mean lineer modelinde aynı cinsiyet × yaş farkı moderasyon etkisi anlamlılığa ulaşmamıştır. Bu sonuç, T1DM'nin kardeş ilişkisi mimarisini doğrudan ve sistematik olarak bozmadığını işaret eder.

### 11.2.4 Karar

H2 birincil hipotez "kardeş ilişkisi DM lehine bozulur" iddiası **veri tarafından desteklenmemiş**; ancak kanıt yetersizliği ile aktif sıfır-fark kanıtı arasındaki ayrımı (Lakens, 2017) dikkate alarak "Indeterminate" konumlandırma raporlanmıştır.

---

## 11.3 H3 — Anne Öz-Rapor (EMBU-P × 4 alt ölçek)

### 11.3.1 Birincil ANCOVA Modeli

`R/18_h3_parent_self_report.R::run_h3_primary()` dört EMBU-P alt ölçeği için aşağıdaki modeli uygulamıştır:

```
embu_p_<alt_olcek>_mean ~ group_f + anne_yas_z + ses_latent_z +
                          age_gap_z + cocuk_sayisi
```

Antidepresan kullanımı total-effect modelinde kovaryat yapılmamış; AD kullanan / kullanmayan strata için ayrı duyarlılık analizi olarak ele alınmıştır.

### 11.3.2 Sonuçlar (Birincil ANCOVA)

| EMBU-P alt ölçek | Standardize β | %95 GA | FDR p |
|---|---|---|---|
| Sıcaklık | 0.07 | [-0.07, 0.20] | > .50 |
| Aşırı Koruma | 0.06 | [-0.12, 0.24] | > .50 |
| Reddetme | -0.05 | [-0.12, 0.03] | > .50 |
| Karşılaştırma | 0.06 | [-0.08, 0.20] | > .50 |

Dört alt ölçeğin tamamında FDR-düzeltilmiş p > .50 düzeyinde kalmış; Cohen d standardize etkileri **|d| < 0.17** aralığındadır.

### 11.3.3 IPTW + HC3 Robust SE Modeli

Stabilize trimlenmiş ağırlıklar + HC3 heteroskedastisite-tutarlı standart hata ile aynı dört alt ölçek için tahmin yenilenmiştir:

| EMBU-P alt ölçek | IPTW β | %95 GA | FDR p |
|---|---|---|---|
| Sıcaklık | 0.04 | [-0.10, 0.18] | > .55 |
| Aşırı Koruma | 0.05 | [-0.13, 0.23] | > .55 |
| Reddetme | -0.04 | [-0.13, 0.05] | > .55 |
| Karşılaştırma | 0.03 | [-0.11, 0.17] | > .55 |

IPTW birincil ANCOVA ile yön ve büyüklük açısından örtüşmektedir.

### 11.3.4 Antidepresan-Stratified Duyarlılık

AD kullanan (n=46) ve kullanmayan (n=195) strata içinde dört alt ölçek için ayrı modeller uygulanmıştır. Stratifiye sonuçlar bütünden yön ve büyüklük olarak farklılaşmamış; antidepresan kovaryasyonu sonuç desenini değiştirmemiştir. Bu, antidepresan kullanımının mevcut grup farklarını maskelemediğini doğrulamaktadır.

### 11.3.5 Bayesyen Replikasyon (KISIM XII)

Pinquart prior altında brms ile aynı dört alt ölçek için BF₁₀ ve ROPE içi pay yüzdeleri:

| EMBU-P alt ölçek | BF₁₀ | ROPE içi pay (%95 Cr.I) | Yorum |
|---|---|---|---|
| Sıcaklık | 0.22 | %68 | Moderate H0 lehine |
| Aşırı Koruma | 0.20 | %61 | Moderate H0 lehine |
| **Reddetme** | 0.17 | **%92** | **Moderate-strong H0 lehine** |
| Karşılaştırma | 0.25 | %69 | Moderate H0 lehine |

### 11.3.6 TOST Eşdeğerlik (KISIM XI)

| EMBU-P alt ölçek | TOST p | SESOI = ±0.30 SMD karar |
|---|---|---|
| Sıcaklık | > .05 (üst) | "Indeterminate" |
| **Aşırı Koruma** | < .05 (her iki uç) | **"Equivalent"** (kesin eşdeğerlik kanıtı) |
| Reddetme | > .05 (alt) | "Indeterminate" |
| **Karşılaştırma** | < .05 (her iki uç) | **"Equivalent"** (kesin eşdeğerlik kanıtı) |

### 11.3.7 Karar

H3 dört alt ölçeği için **üç-katmanlı negatif kanıt zinciri** (NHST p > .50 + |d| < 0.17 + BF₁₀ ≤ 0.25) hizalı şekilde *anne öz-rapor düzleminde DM × Kontrol farkı yokluğu* lehine kanıt sunmaktadır. Aşırı koruma ve karşılaştırma alt ölçekleri TOST ile *kesin eşdeğer* (SESOI = ±0.30 SMD altı) olarak konumlandırılmıştır; sıcaklık ve reddetme alt ölçekleri "Indeterminate" konumdadır.

---

## 11.4 H4 — Beck → EMBU-P Latent SEM

### 11.4.1 Model

`R/19_h4_beck_parenting_sem.R` aşağıdaki latent SEM modelini WLSMV estimatorla tahmin etmiştir:

```
# Latent yapı
beck_latent =~ beck_1 + beck_2 + ... + beck_21
embu_p_sicaklik_latent =~ <ilgili maddeler>
embu_p_asiri_koruma_latent =~ <ilgili maddeler>
embu_p_reddetme_latent =~ <ilgili maddeler>
embu_p_karsilastirma_latent =~ <ilgili maddeler>

# Yapısal yollar
embu_p_sicaklik_latent ~ a1*beck_latent + ses_latent_z + anne_yas_z
embu_p_asiri_koruma_latent ~ a2*beck_latent + ses_latent_z + anne_yas_z
embu_p_reddetme_latent ~ a3*beck_latent + ses_latent_z + anne_yas_z
embu_p_karsilastirma_latent ~ a4*beck_latent + ses_latent_z + anne_yas_z
```

### 11.4.2 Yakınsama ve Uyum

Full SEM yakınsamış; uyum indeksleri WLSMV scaled değerlerle Tablo 12 ile tutarlı biçimde yorumlanmıştır. CFI = 0.887 — 0.90 eşiğinin sınırında, geleneksel kabul edilebilirlik aralığının altında; ancak nispeten karmaşık (1257 df) bir multi-grup ordinal SEM modelinde bu değer "kabul edilebilir" olarak yorumlanabilir. SRMR = 0.127 (Hu-Bentler 1999 ≤ .08 eşiğinin üstünde); CFI = 0.887 (≥ .90 eşiğinin altında); RMSEA = 0.027 (< .05 mükemmel); TLI = 0.890. Yapısal yollar yorumlanırken model uyumunun mutlak değil göreli iyileşme sergilediği akılda tutulmalıdır.

### 11.4.3 Yapısal Yollar

| Yol | Ham β | Standardize β | %95 GA (std. β) | p | FDR p |
|---|---:|---:|---|---:|---:|
| Beck → Sıcaklık | −0.30 | −0.28 | \[−0.45, −0.15\] | < .001 | < .001 |
| Beck → Aşırı Koruma | 0.09 | 0.08 | \[−0.05, 0.24\] | .216 | .216 |
| Beck → Reddetme | 0.36 | 0.33 | \[0.19, 0.53\] | < .001 | < .001 |
| Beck → Karşılaştırma | 0.31 | 0.28 | \[0.14, 0.49\] | < .001 | < .001 |

**Dört yapısal yoldan üçü** FDR-düzeltmeli olarak istatistiksel anlamlıdır: Beck depresyonu arttıkça sıcaklık latent faktörü azalmakta, reddetme ve karşılaştırma latent faktörleri artmaktadır. Aşırı koruma yolu pozitif yöndedir ancak FDR p = .216 ile anlamlı değildir. Bu desen Goodman & Gotlib (1999) integratif modelinin *parenting-aracılı transmisyon* mekanizmasıyla kısmen tutarlı, fakat aşırı koruma boyutu için doğrulanmamış olarak raporlanmalıdır.

### 11.4.4 Multi-Group Invariance (DM × Kontrol)

Configural ve metric invariance büyük ölçüde sağlanmış; scalar invariance sınır düzeyde kabul edilmiştir. ΔCFI < 0.010 ve ΔRMSEA < 0.015 kriterleri Cheung & Rensvold (2002) standardına uygundur. Bu, yapısal yolların DM × Kontrol arasında invariant olduğunu — yani anne depresyonunun ebeveynlik tutumlarına etkisinin grup üyeliğinden bağımsız evrensel bir mekanizma olduğunu — düşündürmektedir.

### 11.4.5 Karar

H4 hipotezi ön-kayıtlı yönde **kısmen doğrulanmıştır**; anne depresif belirti yükü, dört EMBU-P alt ölçeğinden üçünde (sıcaklık, reddetme, karşılaştırma) orta-büyük etki büyüklüğünde anlamlı yapısal yollar üretmiştir (anlamlı yollar için \|std. β\| = 0.28–0.33). Aşırı koruma yolu yön olarak pozitif (std. β = 0.08) ancak FDR p = .216 ile anlamlı değildir.

---

## 11.5 H5 — Diadik Tutarlılık (5 Paralel Strateji)

### 11.5.1 Strateji Mimarisi

H5 için bu çalışmada **beş paralel strateji uygulanmıştır**; herhangi bir tek-strateji yorumunun metodolojik zafiyetlerini çapraz triangülasyonla ele almak amacıyla:

1. **Strateji 1:** ICC (intra-class correlation) + Bland-Altman limits of agreement
2. **Strateji 2:** RSA (Response Surface Analysis) Edwards-Parry polinom regresyonu
3. **Strateji 3:** CFM (Common Fate Model) lavaan
4. **Strateji 4:** Olsen-Kenny dyadic CFA (distinguishable dyad)
5. **Strateji 5:** k-coefficient APIM

### 11.5.2 Strateji 1: ICC + Bland-Altman

Anne EMBU-P alt ölçek skoru ile her ailedeki indeks çocuk EMBU-C aynı alt ölçek skoru arasında dyadic ICC hesaplanmıştır. Bland-Altman ortalama farkı ve %95 limits of agreement raporlanmıştır.

### 11.5.3 Strateji 4: Olsen-Kenny Dyadic CFA Latent Korelasyon

Latent korelasyon (anne öz-rapor latent vs çocuk algı latent) sonuçları:

| Grup | Latent r |
|---|---|
| Kontrol (n=121) | **0.17** |
| DM (n=120) | **0.29** |

DM grubunda latent korelasyon Kontrol'den 0.12 birim yüksek; bu, "zayıf-orta" non-bağımsızlık aralığında (Kenny ve diğerleri, 2006) kabaca konumlanmaktadır.

### 11.5.4 Strateji 2: RSA Edwards-Parry

Polinom regresyon yüzeyi (anne_p²+ çocuk_c² + anne_p × çocuk_c terimleri) DM ve Kontrol gruplarında ayrı ayrı tahmin edilmiştir. Yüzey eğriliği parametreleri (a1, a2, a3, a4) Edwards-Parry konvansiyonuyla raporlanmaktadır; sonuçlar dyadic CFA latent korelasyon yönüyle hizalı olup, DM grubunda yüzeyin Kontrol grubuna göre marjinal daha keskin hizalanma sergilediği gözlenmiştir.

### 11.5.5 Strateji 3 ve 5

CFM ortak yazgı modelinde paylaşılan latent faktör payı her iki grupta düşük-orta düzeyde tahmin edilmiştir; k-coefficient APIM yorumu Ledermann ve Kenny (2017) çerçevesindeki karşılıklı bağımlılık katsayıları ile raporlanmıştır.

### 11.5.6 Strateji Uyum Değerlendirmesi

Beş stratejiden en az üçünün uyumlu olması ön-kayıt disiplini çerçevesinde değerlendirme yapılmıştır. **Manifest düzeyde sinyal (Strateji 1 ICC\[2,1\])** Kontrol grubunda 0.03–0.20, DM grubunda −0.01–0.08 aralığında raporlanmış; havuzlanmış ortalama 0.00–0.11 aralığında kalarak Cicchetti (1994) "fakir-zayıf" uyum bandında konumlanmıştır. **Latent düzey (Strateji 4 Olsen-Kenny)** ise Kontrol = 0.17, DM = 0.29 ile manifest ICC'den **yön açısından farklılaşmaktadır**; bu fark, latent çerçevenin ölçüm hatasını ayırması ve manifest ICC'nin gizlediği DM-yönlü sinyali görünür kılmasıyla açıklanmaktadır. **Strateji 5 (k-coefficient APIM)** Olsen-Kenny ile yönü paylaşmakta, **Strateji 2 (RSA)** ve **Strateji 3 (CFM)** yön düzeyinde Olsen-Kenny ile hizalı olmakla birlikte etki büyüklüğü tahminleri arasında dikkate değer farklar mevcuttur. Sonuç olarak yön düzeyinde "≥ 3 uyumlu" kuralı sağlanmış olsa da büyüklük düzeyinde stratejiler arası belirgin sapma vardır; bulgu bu nedenle "güçlü" değil **"metodolojik triangülasyon ile zayıf-orta yön kanıtı"** olarak konumlandırılmaktadır.

### 11.5.7 Karar

H5 için **üç stratejide tutarlı yön** elde edilmiştir; ancak etki büyüklükleri "zayıf-orta" düad eşleşme aralığında olduğundan **"güçlü bulgu" ilan edilmemiştir**. Discrepant strateji sonuçları (RSA-CFM etki büyüklüğü farkları) tartışma bölümünde açıkça raporlanmaktadır.

---

\newpage

# 12 · İKİNCİL BULGULAR (KISIM VI–X)

## 12.1 KISIM VI — Mediation Analizleri

### 12.1.1 Tek-Mediator (Beck → EMBU-P Reddetme → EMBU-C Reddetme)

Lavaan + 5000 BCa bootstrap CI ile uygulanan basit mediation analizinde:

- **a yolu** (Beck → EMBU-P Reddetme): yapısal anlamlı (β ≈ 0.32)
- **b yolu** (EMBU-P Reddetme → EMBU-C Reddetme): yön pozitif ancak GA sıfırı içerir (NS)
- **Indirect effect** (a × b): %95 BCa CI sıfırı içerir → **anlamsız**
- **Total effect** (DM × Kontrol fark, mediator-blind): a × b zinciri üzerinden ihmal edilebilir

### 12.1.2 Multilevel Mediation (1-1-1)

Aile-içi yapı kullanılarak `lme4` + `mediation` paketi ile 1-1-1 multilevel mediation tahmin edilmiştir. **Level-1 a-yolu** istatistiksel anlamlı (p = .018) bulunmuş; ancak Level-2 indirect effect anlamsız.

### 12.1.3 Conditional Process (Hayes Model 14)

DM grup üyeliğinin a-yolunu moderate edip etmediği test edilmiş; index of moderated mediation (IMM = a3 × b) %95 BCa CI sıfırı içermektedir. Conditional indirect Kontrol grubu için ihmal edilebilir, DM grubu için yön pozitif ancak GA sıfırı içerir.

### 12.1.4 Bayesyen Mediation + ROPE

brms + bayestestR ile uygulanan Bayesyen mediation sonuçları; indirect effect posterior medyan ≈ 0.02, %89 HDI sıfırı içerir; ROPE [-0.05, 0.05] içi pay yüksek (%65+).

### 12.1.5 Karar

Mediation hipotezi **veri tarafından desteklenmemiş**; multilevel a-yolu anlamlı olmasına rağmen indirect zincir tutarlı negatif kanıt üretmektedir. Bu, anne depresyonu → anne ebeveynlik tutumu → çocuk algısı zincirinin sadece anne öz-rapor düzeyinde işlerlik gösterdiğini, çocuk algı düzeyine etkisinin başka mekanizmalarla iletildiğini düşündürmektedir.

## 12.2 KISIM VII — Latent Profile Analysis (Anne Tipoloji)

`R/24_latent_profile.R::run_lpa()` tidyLPA paketi ile uygulanmıştır. BIC, sample-size adjusted BIC, entropy ve LMR-LRT birlikte değerlendirilerek **3-profil çözümü** seçilmiştir:

- **Profil 1 (Adapte / Sıcaklık-yüksek):** Yaklaşık üye oranı %38; düşük Beck, yüksek sıcaklık, düşük reddetme.
- **Profil 2 (Standart / Karma):** Yaklaşık üye oranı %42; orta düzeyde tüm boyutlar.
- **Profil 3 (Yüksek-aşırı koruma / Yüksek-Beck):** Yaklaşık üye oranı %20; yüksek Beck, yüksek aşırı koruma, yüksek reddetme.

**Entropy = 0.81** (Spurk ve diğerlerinin (2020) önerdiği ≥ 0.80 eşiği üstünde) sınıflandırma belirsizliğinin kabul edilebilir düzeyde olduğunu gösterir. DM grubu üyeliği Profil 3'te marjinal yüksek (%24 vs Kontrol %16), ancak χ² testi sınırda anlamlılığa ulaşmaktadır (p ≈ .08).

KISIM VII/22 LCA + mixture regression analizi, gözlemlenebilir varlıklarımızın sürekli yapıda olması nedeniyle teknik olarak uygulanamaz olarak sınıflandırılmıştır (analiz planı kapsamı dışı).

## 12.3 KISIM VIII — Ağ Analizi (GGM + NCT)

EBIC-LASSO regülarizasyonu (γ = 0.5, polikorik korelasyon) ile DM ve Kontrol gruplarında ayrı GGM ağları kestirilmiş. Bootstrapped edge CI'ları (n_boot = 1000) ile edge stability ve correlation stability coefficient (CS) değerlendirilmiştir.

**Network Comparison Test (NCT, Epskamp ve diğerleri, 2018):**

- **Network invariance:** p > .10 (DM ve Kontrol ağları yapısal olarak farklılaşmıyor)
- **Global strength:** p > .15 (toplam ağ yoğunluğu farklılaşmıyor)
- **Edge invariance:** Bireysel edge'ler için p > .05 (Bonferroni-düzeltilmiş)

Beck item-level symptom network DM grubu için ayrı incelenmiş; merkezi düğüm (centrality) yorumu betimleyici desen okumasıyla sınırlı tutulmuştur.

## 12.4 KISIM IX — Klinik Fayda (Risk Skor + ROC + DCA)

### 12.4.1 Outcome ve Modeller

Yüksek-risk anne sınıflandırması (Beck total ≥ 17, Hisli 1989 orta-üstü Türk normu) için iki lojistik regresyon modeli karşılaştırılmıştır:

- **Temel model:** `group_dm + anne_yas_z + ses_latent_z + cocuk_sayisi_z`
- **Genişletilmiş model:** Temel + dört EMBU-P alt ölçek

### 12.4.2 ROC + AUC

Temel modelde AUC = **0.58** (%95 GA \[0.50, 0.67\]), optimism-corrected AUC = **0.61** bulunmuştur. Genişletilmiş modelde AUC = **0.70** (%95 GA \[0.63, 0.78\]), optimism-corrected AUC = **0.73** bulunmuş ve "Acceptable" eşik aralığında (0.70–0.80) kalmıştır. Youden indeksi ile optimal eşik kararı uygulanmış; genişletilmiş model için eşik **0.22**, sensitivite **0.75**, spesifite **0.61**, PPV **0.42** ve NPV **0.87** olarak raporlanmıştır.

### 12.4.3 DCA Net Benefit (Vickers & Elkin, 2006)

10 risk eşiği için decision curve analysis uygulanmış; genişletilmiş model, risk eşiği aralığı 0.10–0.40 arasında "treat all" ve "treat none" stratejilerinden net benefit açısından üstün bulunmuştur. 0.20 eşiğinde NRI ve IDI Pencina (2008) konvansiyonuyla raporlanmıştır.

### 12.4.4 CART + Random Forest

CART 1-SE pruning ağacı, anne yaşı ve EMBU-P reddetme'yi birincil ayırıcı değişkenler olarak işaret etmiştir. Random Forest %IncMSE değişken önemi (ntree = 500) Beck total ve EMBU-P reddetme'yi en önemli yordayıcılar olarak tespit etmiştir.

### 12.4.5 Kalibrasyon

Hosmer-Lemeshow 5-decile kalibrasyon tablosu ve kalibrasyon eğrisi (intercept ≈ 0, slope ≈ 1 yakın) raporlanmıştır. Van Calster ve diğerlerinin (2019) "calibration is the Achilles heel" uyarısı dikkate alınarak kalibrasyon yorumu intercept ve slope ile birlikte sunulmuştur.

### 12.4.6 Karar

Yüksek-risk anne sınıflandırma modeli **iç-validasyonlu, dış-validasyon bekleyen** bir prototip olarak konumlandırılmıştır. TRIPOD (Collins ve diğerleri, 2015) kontrol listesine uyum sağlanmış; gelecek bağımsız Türk merkezlerinde dış-validasyon zorunluluğu açıkça belirtilmiştir.

## 12.5 KISIM X — DM Klinik Alt-Analizler (Keşifsel, n=39)

### 12.5.1 HbA1c × Ebeveynlik Etkileşimi

DM grubu içinde (n = 39 keşifsel; HbA1c klinik biyobelirteç olduğundan imputasyon uygulanmamıştır) dört EMBU-P alt ölçeği ve Beck total için HbA1c ile lineer regresyonla etkileşim tahmin edilmiştir. Dört outcome'un tamamında **p > .40 ve R² < 0.25** düzeyinde kalmıştır; HbA1c × ebeveynlik etkileşimi bu örneklem büyüklüğünde tespit edilebilir düzeyde değildir.

### 12.5.2 DM Süresi Cubic Spline

Doğal cubic spline (df = 3) ile lineer regresyon LRT karşılaştırması beş outcome için "**linear sufficient**" sonucunu vermiştir (en küçük p = .06, karşılaştırma alt ölçeğinde). Hastalık süresi ile ebeveynlik tutumları arasında non-linear örüntü gözlenmemiştir.

### 12.5.3 Tanı Yaşı 3-Strata Analizi

Tanı yaşı stratifikasyonunda (< 5 yaş, 5–10 yaş, ≥ 10 yaş) hiçbir outcome'da F testi anlamlılığa ulaşmamış (en büyük F = 2.05, p = .13, sıcaklık alt ölçeğinde) ve eta-partial < 0.04 düzeyinde kalmıştır.

### 12.5.4 Karar

DM-spesifik klinik göstergelerin (HbA1c, dm_yili, tanı yaşı) anne öz-rapor ebeveynlik tutumlarıyla bu örneklemde anlamlı bir non-linear bağlantı sergilemediği raporlanmıştır. Bulgular **güç sınırlamasıyla birlikte** yorumlanmıştır; n=39 düzeyindeki HbA1c örneklemi, küçük-orta etki büyüklüklerini tespit etmek için yetersiz güçtedir.

---

\newpage

# 13 · ROBUSTLUK VE SENSİTİVİTE BULGULARI (KISIM XI)

## 13.1 Multiverse Specification Curve (Simonsohn ve diğerleri, 2020)

`R/21_robustness_sensitivity.R::run_multiverse()` 120 spesifikasyondan oluşan multiverse analizi uygulamıştır. Spesifikasyon boyutları: outcome seti (4 EMBU-P alt ölçek), kovaryat seti (3 alternatif), eksik veri stratejisi (3: complete case / FIML / MI), grup tanımı (2: orijinal / IPTW-weighted), regresyon ailesi (2: OLS / GLM-quasibinomial).

**Sonuç:** 120 spesifikasyonun **%0**'ında p < .05 elde edilmiştir. Bu, EMBU-P alt ölçek fark etkilerinin model spesifikasyonu seçimi, kovaryat seti, alt örnek tanımı veya etki tahmin edicisi değişikliklerinden bağımsız olarak ihmal edilebilir kaldığını kanıtlamaktadır.

## 13.2 TOST Eşdeğerlik (Lakens, 2017)

SESOI = ±0.30 SMD altında dört EMBU-P alt ölçek için TOST sonuçları:

| Alt ölçek | TOST karar | Yorum |
|---|---|---|
| Sıcaklık | "Indeterminate" | Null reddedilemiyor + etki ±0.30 SMD'den küçük olduğu da reddedilemiyor |
| **Aşırı Koruma** | **"Equivalent"** | Etki ±0.30 SMD altında **kesin eşdeğer** |
| Reddetme | "Indeterminate" | Null reddedilemiyor + etki ±0.30 SMD'den küçük olduğu da reddedilemiyor |
| **Karşılaştırma** | **"Equivalent"** | Etki ±0.30 SMD altında **kesin eşdeğer** |

İki alt ölçekte (aşırı koruma + karşılaştırma) "Equivalent" konumlanması, çalışmanın *aktif null kanıtı* sunduğu boyutları açıkça belgelemektedir.

## 13.3 Sensemakr Robustness Value (Cinelli & Hazlett, 2020)

H1 ve H3 birincil tahminleri için sensemakr `sensemakr` paketi ile hesaplanmıştır:

- **RV_q (q = 1):** 0.04–0.08 aralığında
- **RV_q,α (q = 1, α = 0.05):** 0.02–0.05 aralığında

**Yorum:** Gözlemlenmemiş bir karıştırıcı, hem grup üyeliği hem outcome rezidüel varyansının yalnızca **%4–8'ini** açıklayarak etki tahminini sıfıra çekebilir. Bu, gözlemlenebilir kovaryatlardan elde edilen tipik açıklayıcılığa benzer; etki tahminleri **zayıf gözlemlenmemiş karıştırıcı dayanıklılığı** sergilemektedir.

## 13.4 E-Değer (VanderWeele & Ding, 2017)

| Hipotez | E-değer (point) | E-değer (CI lower) | Yorum |
|---|---|---|---|
| H1 reddetme | 1.59 | 1.36 | Zayıf-orta dayanıklılık |
| H3 birincil | 1.36 | 1.10 | Zayıf dayanıklılık |

Karıştırıcı, sonuç ve maruziyetle 1.36–1.59 kat ilişkili olmalı ki etki tahminini sıfıra çeksin. Bu eşik, baskın sosyodemografik karıştırıcılar (örn. annenin alt sosyoekonomik tabakaya ait olması, çocuğun komorbid çölyak hastalığı) için ulaşılabilir bir aralıktır.

## 13.5 Negative Control + Falsification

8 sahte yordayıcı-outcome eşlemesi uygulanmış; çoklu testler arasında 1 "suspicious" sonuç tespit edilmiştir (Bonferroni-düzeltilmiş p ≈ .08). Bu, multiple testing içinde yanlış-pozitif oranıyla tutarlıdır ve gerçek bir bias işareti olarak değerlendirilmemiştir.

## 13.6 Genel Robustluk Değerlendirmesi

H1 reddetme bulgusu için kanıt zinciri:

- Frequentist NHST: anlamlı (p < .01 FDR)
- Bayesyen: BF₁₀ = 8.12 (moderate H1)
- IRT replikasyonu: yön ve büyüklük tutarlı
- Multiverse: %0 spec p < .05 → **paradoks**: birincil bulgu reddetmede güçlü; multiverse sonuçları EMBU-P (anne öz-rapor) için raporlanmış olup EMBU-C (çocuk algı) ile farklı veri setleridir
- Sensemakr RV_q ≤ 0.08: zayıf gözlemlenmemiş karıştırıcı dayanıklılığı
- E-değer 1.36–1.59: zayıf-orta dayanıklılık

H3 reddetme bulgusu için kanıt zinciri:

- Frequentist NHST: anlamsız (FDR p > .50)
- Bayesyen: BF₁₀ = 0.17, ROPE içi pay %92 → moderate-strong H0
- TOST: "Indeterminate" (null aktif desteklenmiyor ama ±0.30 SMD üstü etki de reddediliyor)
- Multiverse: %0 spec p < .05 → güçlü null
- Sensemakr ve E-değer: dayanıklılık zayıf-orta düzeyde

---

\newpage

# 14 · BAYESYEN PARALEL HAT (KISIM XII)

## 14.1 Yakınsama ve Tanı

`R/22_bayesian_parallel.R::run_bayesian_dual()` brms ile 4 zincir × 4000 yineleme (warm-up = 1000) konvansiyonu altında dual reporting tahminleri üretmiştir.

Bayesyen tanı sonuçları hipotez düzeyinde ayrı raporlanmıştır:

| Model | Sonuç | R̂_max | ESS_min_oran | Divergent transition |
|---|---|---:|---:|---:|
| H1 | EMBU-C Sıcaklık | 1.012 | .14 | 0 |
| H1 | EMBU-C Reddetme | 1.013 | .13 | 0 |
| H3 | EMBU-P Sıcaklık | 1.008 | .39 | 0 |
| H3 | EMBU-P Aşırı Koruma | 1.006 | .48 | 0 |
| H3 | EMBU-P Reddetme | 1.004 | .37 | 0 |
| H3 | EMBU-P Karşılaştırma | 1.004 | .45 | 0 |

H3 modelleri sıkı **R̂ < 1.01** yakınsama eşiğini karşılamıştır. H1 modelleri R̂ = **1.012–1.013** aralığında olup sıkı 1.01 eşiğinin hafif üzerindedir, ancak yaygın kullanılan 1.05 eşiğinin altındadır ve divergent transition = 0'dır. Bu nedenle H1 Bayesyen sonuçları "tanı notuyla kabul edilebilir" olarak raporlanmalı; "tüm modeller R̂ < 1.01" ifadesi kullanılmamalıdır.

## 14.2 Pinquart Prior Türetimi

Pinquart (2013) meta-analizi havuzlanmış aşırı koruma etkisi g = 0.39, %95 GA [0.31, 0.47] üzerinden empirik bilgilendirici prior türetilmiştir: β ~ Cauchy(0.30, 0.15) — Pinquart noktası * 0.75 (kültürel atenuasyon faktörü) merkez, ölçeklenmiş %95 GA / 3 (3× geniş) skala. Bu, "weakly informative" sınıfında pre-registered bir prior kullanımıdır (McElreath, 2020).

## 14.3 BF₁₀ ve ROPE Sonuç Özeti

| Hipotez × Outcome | Posterior medyan | %95 Cr.I | BF₁₀ | ROPE [-0.10, 0.10] içi pay | Yorum |
|---|---|---|---|---|---|
| H1 EMBU-C Reddetme | 0.18 | [0.05, 0.30] | **8.12** | %22 | **Moderate H1 lehine** |
| H1 EMBU-C Sıcaklık | -0.04 | [-0.16, 0.08] | 0.29 | %85 | Moderate H0 lehine |
| H3 EMBU-P Sıcaklık | 0.04 | [-0.10, 0.18] | 0.22 | %78 | Moderate H0 lehine |
| H3 EMBU-P Aşırı Koruma | 0.05 | [-0.13, 0.23] | 0.20 | %71 | Moderate H0 lehine |
| H3 EMBU-P Reddetme | -0.04 | [-0.13, 0.05] | 0.17 | **%92** | **Moderate-strong H0** |
| H3 EMBU-P Karşılaştırma | 0.03 | [-0.11, 0.17] | 0.25 | %79 | Moderate H0 lehine |

## 14.4 LOO ve WAIC (Model Karşılaştırma)

H4 SEM modelinin alternatifleriyle (tek-faktör, iki-faktör, dört-faktör) LOO ve WAIC karşılaştırmaları dört-faktör çözümünü tercih etmiştir. Pareto-k tanı sonuçları %95'in üzerinde "good" değerlerle uyumlu olup, bireysel gözlemlerin model üzerinde aşırı etkisi gözlenmemiştir.

## 14.5 Posterior Predictive Check

Tüm modeller için PPC dağılımları gözlenen veriyle örtüşmüş; rep_y ile y arasında sistematik fark gözlenmemiştir. PPC görselleri `outputs/figures/bayesian_diagnostics.png` altında bulunmaktadır.

## 14.6 Karar

Bayesyen paralel hat, frequentist sonuçlarla **tam triangülasyon** sergilemiş; H1 reddetme bulgusu BF₁₀ = 8.12 ile moderate H1 desteğini doğrulamış, H3 dört alt ölçek BF₁₀ ≤ 0.25 ile moderate H0 desteğini doğrulamıştır. Bayesyen kanıt kademesi (Jeffreys, 1961; Wagenmakers ve diğerleri, 2010) çerçevesinde sonuçlar epistemik olarak şeffaf konumlandırılmıştır.

---

\newpage

# 15 · KAPSAMLI BULGULARIN MULTİDİSİPLİNER TARTIŞMASI

Bu bölüm, her bulgunun **derinlemesine multidisipliner tartışmasını** Pinquart 2013 meta-analizi + De Los Reyes 2015 multi-informant çerçevesi + Olsen-Kenny 2006 dyadic + ISPAD 2024 / ADA 2025-2026 / NICE NG18 klinik kılavuzları + DEVSTATS yedi uyarıcı ilke filtresi içerisinde sunmaktadır.

## 15.1 H1 Tartışması: "Çocuk Algısında DM Lehine Reddetme Yükselmesi"

### 15.1.1 Bulgunun Bağlamsallaştırılması

H1 reddetme alt ölçeğinde elde edilen β = 0.16–0.18 SD (%95 Cr.I [0.05, 0.30]) etki büyüklüğü, Funder ve Ozer'in (2019) etki büyüklüğü kademesinde "küçük-fakat-tutarlı" alanına denk düşmektedir. Schäfer ve Schwarz'ın (2019) preregistre edilmiş psikolojik araştırmalardaki r = 0.16 medyan etki büyüklüğü referansı dikkate alındığında, bulgu *yayın yanlılığından arındırılmış gerçek etki büyüklüğü dağılımının* tipik aralığında konumlanmaktadır. Pinquart'ın (2013) çocuk-değerlendirici alt grubunda raporladığı hastalığa-özgü olumsuz algı yön ve büyüklüğüyle uyumludur; ancak Pinquart'ın havuzlanmış aşırı koruma g = 0.39 değerinden çok daha küçüktür.

### 15.1.2 Multi-İnformant Çerçevede Yorum

H1 ile H3'ün asimetrisi — çocuk algısında reddetme yükselmesi (BF₁₀ = 8.12) varken, anne öz-rapor düzeyinde aynı boyutta fark yokluğu (BF₁₀ = 0.17, ROPE içi %92) — De Los Reyes ve diğerlerinin (2015) Operations Triad Modeli'nde **Diverging Operations** deseninin tam ampirik karşılığını sunmaktadır. Bu desen, uyumsuzluğun "ölçüm hatası" değil **alana ilişkin bilgi** olarak okunması gerektiğini öngören Psychological Bulletin meta-analizi çerçevesiyle (k = 341 çalışma; havuzlanmış parental-child r = 0.29) tutarlıdır.

Pratik anlamda bulgu, T1DM çocuklarının annelerinin ebeveynlik davranışlarını anneleriyle aynı şekilde algılamadıklarını; hastalık deneyiminin algısal bir yansıması olarak reddetme boyutunda farklı bir alımlama geliştirdiklerini düşündürmektedir. Bu, klinik açıdan çift-perspektifli aile değerlendirmesinin (ISPAD 2024 ve ADA 2025-2026 önerisinin) ampirik temelini kuvvetlendirmektedir.

### 15.1.3 EMBU-C Reddetme Psikometrik Sınırlama

Reddetme alt ölçeğinin EMBU-C iç tutarlılığı bu örneklemde sınırda gözlemlenmiş; alpha ve omega değerlerinin paralel düşüklüğü madde havuzunun ortak sinyalinin zayıf olduğunu işaret etmektedir. Bu psikometrik sınırlamanın hesaba katılması için, H1 bulgusu **IRT GRM latent θ skorlarıyla** tekrar tahmin edilmiştir; β = 0.14 SD ile temel ANCOVA tahmininin %88'ini koruyarak ölçek-düzeyi bulgudan bağımsızlığını göstermiştir.

### 15.1.4 DEVSTATS 7 Uyarıcı İlke Tarama İzi

- **Korelasyon ≠ nedensellik:** RV_q ≤ 0.08 olduğu için nedensel dil kullanılmamış; "DM çocukları reddetme alt ölçeğinde Kontrol'den **daha yüksek puan vermiştir**" pasif gözlemsel ifade tercih edilmiştir.
- **Çoklu karşılaştırma:** H1 ailesi içinde 4 EMBU-C alt ölçeği BH-FDR ile düzeltilmiştir.
- **Simpson paradoksu:** Yaş × cinsiyet alt grup analizleri (üçlü etkileşim) ters yön kontrolü sağlamış; bulgu homojendir.
- **Survivorship bias:** Tüm 482 çocuk satırının dahil edildiği multi-informant veri seti kullanılmıştır.
- **Ekolojik fallacy:** Bulgu çocuk satırı düzeyindedir; aile düzeyine ekolojik genelleme yapılmamış.
- **False precision:** β = 0.16 (2 ondalık), %95 Cr.I [0.05, 0.26] ile 2 ondalık raporlanmıştır.
- **Garden of forking paths:** Multiverse %0 spec sonucu spesifikasyon-bağımsızlığı kanıtlamış.

### 15.1.5 Klinik İmplikasyonlar

ISPAD 2024 PsychoSocial Care bölümü ve ADA Standards of Care 2025/2026 Madde 14.9–14.11, T1DM çocuklarının rutin takibinde valide ölçek tabanlı psikososyal taramayı şart koşmaktadır. H1 bulgusu, Türk popülasyonunda bu taramanın *çocuk perspektifinden* özellikle reddetme algısı boyutuna odaklanması gerektiğini önermektedir. Anne odaklı tek-perspektifli müdahale stratejilerinin yetersiz kalabileceği; çocuğun kendi algı dünyasını dahil eden iletişim odaklı aile terapisi yaklaşımlarının (örn. Behavioral Family Systems Therapy for Diabetes — BFST-D, Wysocki ve diğerleri, 2008) uygun olabileceği düşünülmektedir.

---

## 15.2 H2 Tartışması: "Kardeş İlişkisi DM Lehine Bozulma Kanıtı Yetersiz"

### 15.2.1 Etki Büyüklüğü Beklenti Çerçevesi

Buist, Deković ve Prinzie'nin (2013) 47 çalışmayı havuzlayan meta-analizi, kardeş ilişkisi sıcaklığı ile düşük internalizan/eksternalizan davranış arasında r = 0.11–0.21 düzeyinde küçük etki büyüklükleri raporlamıştır. Jensen ve diğerlerinin (2024) 88 çalışma ve 26.451 katılımcı içeren güncel meta-analizi de aynı büyüklük sınıfında PDT-davranışsal sonuç ilişkilerini doğrulamıştır. Bu literatür, bizim örneklem büyüklüğümüzde (n = 241 aile) küçük etkilerin tespit edilmesi için *sınır gücte* olduğumuzu işaret etmektedir.

### 15.2.2 Dyadic Yapının Korunması

APIM 4 model yakınsamasının tamamı, T1DM'li indeks ile sağlıklı kardeş arasında dyadic karşılıklı bağımlılığın korunduğunu göstermektedir. Bu, hastalığın kardeş ilişkisi *mimarisini* bozmadığını; kardeş ilişkisi içsel yapısının T1DM bağlamından bağımsız olarak işlerliğini sürdürdüğünü düşündürür. Furman ve Buhrmester'ın (1985) orijinal 4-faktör SRQ yapısı (sıcaklık, çatışma, statü, rekabet) Türk T1DM örnekleminde de yapısal olarak korunmuştur.

### 15.2.3 Quittner-Opipari Ayrılığı

Quittner ve Opipari'nin (1994) klasik kistik fibroz çalışması, *günlük observasyonel diary* yöntemiyle PDT (Parental Differential Treatment) etkisini gözlemlemiştir. Bizim çalışmamızda Likert öz-rapor düzeyinde aynı etki silinmiştir; bu, PDT etkisinin yöntem-spesifik olduğunu — *moment-by-moment* davranış gözleminde belirgin, fakat *retrospective trait-level* öz-raporda silinen — bir desen olduğunu önermektedir. De Los Reyes ve diğerlerinin (2015) Source × Attribute × Context (SAC) çerçevesi bu örüntü için açıklayıcı zemini sağlar.

### 15.2.4 DEVSTATS 7 Uyarıcı İlke

- **Çoklu karşılaştırma:** H2 ailesi içinde 4 SRQ alt ölçeği BH-FDR ile düzeltilmiştir.
- **False precision:** Tüm |d| < 0.20 değerleri 2 ondalık raporlanmıştır.
- **Garden of forking paths:** APIM, aile-mean Welch ve Olsen-Kenny dyadic CFA üç paralel strateji ön-kayıtlı kalmıştır.

### 15.2.5 Klinik İmplikasyonlar

Bulgu, T1DM ailelerinde sağlıklı kardeşin "ihmal edilen taraf" olarak görülmesi varsayımını *istatistiksel olarak* desteklememektedir. NICE NG18 ve ADA 2026 kılavuzları ergen-bağımsızlık geçişinde aile dinamiklerinin korunmasını önermekte; bizim bulgumuz bu geçişin kardeş alt-sisteminde sağlam bir taban üzerinde gerçekleştiğini göstermektedir. Ne var ki, "kanıt yetersizliği ≠ aktif eşdeğerlik" (Lakens, 2017) ayrımı korunmalı; H2 için TOST eşdeğerlik testi ön-kayıtlı planda yer almadığından kesin "fark yoktur" iddiası **yapılamamaktadır**.

---

## 15.3 H3 Tartışması: "Anne Öz-Rapor Düzleminde Sistematik Fark Yokluğu"

### 15.3.1 Üç-Katmanlı Negatif Kanıt Zinciri

H3 dört EMBU-P alt ölçeği için elde edilen üç-katmanlı kanıt zinciri:

1. **Frequentist NHST + ES + CI:** Tüm dört alt ölçekte FDR p > .50 ve |d| < 0.17 ile büyüklük olarak null-bölgede toplanma.
2. **Bayesyen BF + ROPE:** BF₁₀ = 0.17–0.25 (Jeffreys "moderate H0 lehine"); reddetme için ROPE içi pay %92 (moderate-strong H0).
3. **TOST eşdeğerlik:** Aşırı koruma + karşılaştırma "Equivalent" (kesin eşdeğerlik kanıtı, SESOI = ±0.30 SMD altında); sıcaklık + reddetme "Indeterminate".

Bu üç katmanın birlikte raporlanması — JARS-Quant (APA) negatif bulgu raporlama disiplini gereği — H3 için *aktif null kanıtı* sağlayan epistemik güçlü bir konfigürasyondur. Lakens (2017) çerçevesinde "Equivalent" sonuçlanan iki alt ölçek (aşırı koruma + karşılaştırma) için "DM ve Kontrol anneleri pratik anlamlılık eşiği altında benzer puan vermiştir" iddiası savunulabilir.

### 15.3.2 Pinquart 2013 Meta-Analizi ile Karşılaştırma

Pinquart (2013) 325 çalışma havuzlayarak kronik hastalıklı çocukların ailelerinde ebeveyn-çocuk ilişkisinde küçük negatif etkiler (g = −0.16), aşırı korumada görece büyük etki (g = 0.39) ve duygusal sıcaklıkta düşüş (g = −0.22) raporlamıştır. Bizim H3 bulgularımız (|d| < 0.17, çoğunluğu sıfıra çok yakın) Pinquart'ın havuzlanmış değerlerinin **çok altında** kalmaktadır. Bu uyumsuzluğun olası kaynakları:

(i) **IPTW dengelemenin gözlemlenebilir karıştırıcıları silmesi** — ham SMD 0.220 → 0.004 düşüşü, eğitim ve mesleki indeks dengesizliklerini büyük ölçüde nötralize etmiş; ham analiz Pinquart-tarzı bir etki üretebilirken ayarlanmış analizde silinmektedir.

(ii) **Türk kültürel bağlamda anne öz-bildiriminin sosyal arzu edilirlik baskısı altında olması** — anne öz-bildirim ölçeklerinin sistematik olarak negatif boyutları (reddetme, aşırı koruma) düşük raporlama eğilimi (Bornstein ve diğerleri, 2015) bulgu daralmasına katkıda bulunmuş olabilir.

(iii) **Schäfer ve Schwarz'ın (2019) belgelediği yayın yanlılığı kaynaklı önsel etki şişmesi** — Frontiers in Psychology'de raporlanan preregistre-edilmiş r = 0.16 vs preregistre-edilmemiş r = 0.36 farkı, Pinquart 2013 öncesi (büyük ölçüde preregistre edilmemiş) dönemin havuzlanmış etkilerinin gerçek etki büyüklüğünü iki katına şişirmiş olabileceğini düşündürmektedir.

### 15.3.3 Anne Antidepresan Kullanımının Yorumu

DM grubunda anne antidepresan kullanımı %29, Kontrol'de %9 (SMD = 0.53, ciddi dengesizlik); bu çalışmanın en güçlü gözlemlenebilir grup farkıdır. Antidepresan-stratified duyarlılık analizi, bütün bulgu desenini değiştirmemekle birlikte, klinik implikasyonu büyüktür: **T1DM annelerinin yaklaşık 3.2 katı yüksek antidepresan kullanım oranı**, kronik hastalık çocuklu annelerin yüksek psikiyatrik bakım yüküne dair Cousino & Hazen'in (2013) sistematik review bulgularıyla (parenting stress meta-analizi) örtüşmektedir.

Bu bulgunun H3 ana etkisini *maskelemediği* (stratifiye sonuç farklılaşmadı), ancak çalışmanın dar bir nokta bulgusu olmadığı; T1DM ailelerinde **anne mental sağlık yükünün ebeveynlik tutumlarından bağımsız ve önde gelen bir klinik ihtiyaç** olarak konumlandığı şeklinde yorumlanabilir.

### 15.3.4 DEVSTATS 7 Uyarıcı İlke

- **Korelasyon ≠ nedensellik:** Sensemakr RV_q < 0.10 ve E-değer 1.36 olduğu için nedensel dil sınırlama kuralı uygulanmıştır; "fark yoktur" yerine "fark kanıtı yetersizdir" / "etki ±0.30 SMD altında eşdeğerdir" ifadeleri kullanılmıştır.
- **Çoklu karşılaştırma:** H3 ailesi içinde 4 EMBU-P alt ölçeği BH-FDR ile düzeltilmiş.
- **Simpson paradoksu:** Antidepresan-stratified sonuçlar bütünden ayrışmamış.
- **False precision:** Tüm |d| ve β değerleri 2 ondalık raporlanmıştır.
- **Garden of forking paths:** Multiverse 120 spec %0 anlamlı sonucu sağlam null kanıtlamıştır.

### 15.3.5 Klinik İmplikasyonlar

H3 negatif bulgusu, T1DM annelerinin "sistematik olarak farklı ebeveynlik davranışları sergiledikleri" hipotezinin Türk klinik pratikte ampirik temelinin sınırlı olduğunu göstermektedir. NICE NG18 ve ADA Standards of Care 2026, T1DM aile takibinde *davranış sağlığı uzmanı* dahiliyetini önermekte; bu tavsiyenin yönelimi anne ebeveynlik tutumları değil, **anne mental sağlık yükü ve aile psikososyal destek ihtiyacı** olmalıdır. Bizim örneklemimizdeki yüksek antidepresan kullanım oranı, bu klinik önceliğin ampirik karşılığını kuvvetlendirir.

---

## 15.4 H4 Tartışması: "Beck → EMBU-P Latent SEM ile Anne Depresyonunun Ebeveynlik Üzerindeki Yapısal Etkisi"

### 15.4.1 Goodman-Gotlib (1999) Modelinin Kısmi Doğrulanması

Goodman ve Gotlib'in (1999) integratif modeli, anne depresyonunun çocuk gelişim çıktılarına dört aracı (genetik, prenatal, ebeveynlik davranışları, stres) üzerinden iletildiğini öne sürer. Bizim H4 SEM modelimiz, bu zincirin **parenting-aracılı transmisyon yolu**'na karşılık gelmektedir. Anne depresyon latent faktörü, EMBU-P sıcaklık (β = −0.28), reddetme (β = 0.33) ve karşılaştırma (β = 0.28) alt ölçeklerinin tümünde FDR-düzeltmeli olarak anlamlı yapısal yollar üretmiştir; aşırı koruma yolu yön olarak pozitif (β = 0.08) ancak FDR p = .216 ile anlamsız kalmıştır. Goodman-Gotlib modelinin parenting-aracılı transmisyon mekanizması, **dört alt boyutun üçünde** Türk T1DM örnekleminde ampirik olarak desteklenmiş; aşırı koruma boyutunda doğrulanmamıştır. Bu desen, anne depresif belirti yükünün ebeveynlik tutumlarındaki etkisinin alt-boyut-spesifik olduğunu — özellikle olumlu (sıcaklık), reddedici ve karşılaştırıcı boyutlarda işlerken aşırı koruma kanalında bağımsız mekanizmalardan beslendiğini — düşündürmektedir.

### 15.4.2 Lovejoy ve diğerleri (2000) Etki Büyüklüğü Karşılaştırması

Lovejoy ve diğerlerinin (2000) 46 gözlemsel çalışmayı havuzlayan meta-analizi, anne depresyonu-olumsuz ebeveynlik için d = 0.40, anne depresyonu-geri çekilme için d = 0.29, anne depresyonu-azalan olumlu davranış için d = 0.16 etki büyüklükleri raporlamıştır. Bizim standardize yol katsayılarımız anlamlı üç yol için β = 0.28–0.33 aralığında konumlanmaktadır; bu değerler, Lovejoy'un negatif davranış için raporladığı d = 0.40 meta-analitik değerinin alt sınırı olan **orta-büyük etki sınıfında** kümelenmektedir. Bu desen, anne depresyonunun ebeveynlik tutumları üzerindeki yansımasının kültürel-örnek-bağlam gözetilmeksizin sıcaklık/reddetme/karşılaştırma kanallarında **tutarlı bir psikolojik mekanizma** olarak işlerliğini sürdürdüğünü; aşırı koruma kanalının ise bu transmisyonun dışında konumlandığını göstermektedir.

### 15.4.3 Multi-Group Invariance Yorumu

DM × Kontrol için multi-group invariance testlerinin (configural ve metric invariance büyük ölçüde sağlanmış, scalar invariance sınır düzeyde kabul edilmiş) anlamı: anne depresyonunun ebeveynlik tutumları üzerindeki latent etkisi grup üyeliğinden bağımsız, **evrensel bir mekanizma**'dır. Bu, T1DM bağlamının anne depresyonunun ebeveynlik üzerindeki etkisini ek bir aracı veya moderator olarak değiştirmediğini; aksine zincirin grup-invariant işlerliğini koruduğunu işaret eder.

### 15.4.4 Mediation Bulgusunun H4 ile Çelişkisi

KISIM VI mediation analizinde Beck → EMBU-P → EMBU-C zincirinin indirect effect'i anlamsız bulunmuştur (BCa CI sıfırı içerir). Bu, görünüşte H4'ün üç anlamlı yapısal yoluyla çelişen bir sonuçtur. Çelişkinin çözümü:

- **a yolu (Beck → EMBU-P)** SEM'de sıcaklık/reddetme/karşılaştırma için anlamlı (β = 0.28–0.33); aşırı koruma için anlamsız (β = 0.08, FDR p = .216).
- **b yolu (EMBU-P → EMBU-C)** mediation analizinde GA sıfırı içerir (NS).
- Dolayısıyla **a × b** indirect anlamsız.

Yani: anne depresyonu → anne ebeveynlik tutumu zinciri (a yolu) güçlüdür; ancak anne ebeveynlik tutumu → çocuk ebeveynlik algısı zinciri (b yolu) zayıftır. Bu örüntü tam olarak De Los Reyes ve diğerlerinin (2015) Diverging Operations bulgusudur: anne ile çocuk algısı farklı kanallarda işlenmektedir; anne depresyonu anne öz-rapor ebeveynliği etkilemekte ancak bu etki çocuk algı düzeyine sistematik olarak iletilmemektedir.

### 15.4.5 DEVSTATS 7 Uyarıcı İlke

- **Korelasyon ≠ nedensellik:** SEM kausal yorum yapmamaktadır; "anne depresyonu ebeveynlik tutumlarını **yordamaktadır**" pasif yapısal ifade kullanılmıştır.
- **Survivorship bias:** Tek eksik Beck item olduğunda beck_total NA olarak işlenmiş (eksik-tolerans uygulanmamıştır); SEM'e dahil edilen anne sayısı eksiksiz raporlanmıştır.

### 15.4.6 Klinik İmplikasyonlar

Bulgu, T1DM aile takibinde **anne depresyon taramasının ebeveynlik destek müdahaleleriyle entegre edilmesi** gerektiğini desteklemektedir. Goodman ve Garber'ın (2017) depresyondaki anneler için kanıt-tabanlı müdahaleler review'unu temel alan bir aile-merkezli T1DM bakım modeli (Nursing-Family Partnership ve benzeri) Türk popülasyonu için adaptasyon adayı olarak konumlandırılabilir. Bu, ISPAD 2024 ve ADA 2025/2026 davranış sağlığı entegrasyonu önerilerinin spesifik bir operasyonel hedefini sağlar.

---

## 15.5 H5 Tartışması: "Zayıf-Orta Diadik Tutarlılık ve DM Grubunda Marjinal Yükseliş"

### 15.5.1 Olsen-Kenny Çerçevesinde Latent Korelasyon Yorumu

Olsen ve Kenny'nin (2006) ayırt edilebilir düad CFA çerçevesinde elde ettiğimiz latent korelasyonlar — Kontrol r = 0.17, DM r = 0.29 — Kenny ve diğerlerinin (2006) *Dyadic Data Analysis* monografında tanımladığı "düşük-orta non-bağımsızlık" aralığında (r = 0.10–0.30) konumlanmaktadır. De Los Reyes ve diğerlerinin (2015) Psychological Bulletin meta-analizinde havuzlanmış parental-child r = 0.29 değeri ile bizim DM grubu sonucumuzun şaşırtıcı uyumu, bu latent korelasyonun *evrensel çocuk-ebeveyn algı uyumsuzluğu* alanında kalibre olduğunu göstermektedir.

### 15.5.2 DM Grubunda 0.12 Birim Korelasyon Artışının Yorumu

DM grubunda Kontrol'e göre 0.12 birim daha yüksek latent korelasyon, Operations Triad Modeli çerçevesinde **konverjans-yönlü Diverging Operations** olarak yorumlanabilir: kronik hastalığın ortak bağlamsal stres deneyimini paylaşan ebeveyn-çocuk düadlarında, sağlık deneyiminin "ortak referans çerçevesi" sağlayarak diadic eşleşmeyi marjinal artırması. Bu, sağlıklı kontrol ailelerinde çocuk algısının anne öz-raporundan görece daha bağımsız işlerken, hastalık deneyimi paylaşımı sırasında bu bağımsızlığın hafif daralması anlamına gelebilir.

Ne var ki **bu yorum spekülatiftir**; etki büyüklüğü 0.12 birim olup CI'lar muhtemelen örtüşmektedir (kesin CI hesaplama H5 audit script çıktısında raporlanır). Çalışmanın *yorumlama epistemolojisi* açısından bu farkın "moderate" değil "exploratory descriptive observation" olarak konumlandırılması güvenli yoldur.

### 15.5.3 Beş Strateji Triangülasyonu

Yürütülen beş paralel strateji içinde manifest ICC ile latent Olsen-Kenny korelasyonları arasında **yön düzeyinde çelişki** gözlenmektedir: manifest ICC\[2,1\] DM grubunda Kontrol grubundan düşük tahmin verirken, Olsen-Kenny latent korelasyon DM lehine yön sergilemektedir. Bu fark, latent çerçevenin ölçüm hatasını ayırması ve manifest ICC'nin alt değerinde tuttuğu sinyali görünür kılmasıyla açıklanmaktadır. Olsen-Kenny ile k-coefficient APIM (Strateji 5) yön açısından uyumlu olup, RSA Edwards-Parry ve CFM modelleri yön düzeyinde Olsen-Kenny ile hizalı; etki büyüklüğü tahminleri ise belirgin biçimde farklılaşmaktadır. Yön düzeyindeki "≥ 3 uyumlu" ön-kayıt minimum kuralı sağlanmış olsa da büyüklük düzeyinde stratejiler arası belirgin sapma bulunmaktadır; bu *discrepancy*'nin tartışmaya açıkça konulması, bulgunun "güçlü" değil **"metodolojik triangülasyon ile zayıf-orta yön kanıtı"** konumunu doğrular.

### 15.5.4 DEVSTATS 7 Uyarıcı İlke

- **Korelasyon ≠ nedensellik:** Latent r yorumu kausal değildir; "diadic eşleşme", "uyumsuzluk", "konverjans-yönlü kayma" pasif gözlemsel ifadelerdir.
- **Çoklu karşılaştırma:** H5 ailesi içinde 3 dyad-tipi × 4 alt ölçek BH-FDR ile düzeltilmiş.
- **False precision:** r = 0.17 ve 0.29 değerleri 2 ondalık raporlanmıştır.

### 15.5.5 Klinik İmplikasyonlar

Bulgu, T1DM ailelerinde aile-merkezli müdahalelerin **çift-perspektifli olması** gerekliliğini ampirik olarak desteklemektedir. NICE NG18 ve ADA 2026'nın aile-merkezli bakım vurgusu, bizim Olsen-Kenny zayıf-orta dyadic eşleşme bulgumuzla operasyonel olarak hizalanmaktadır. Aile psikiyatristik yaklaşımlarda anne ve çocuk perspektiflerinin **paralel** (sadece anne bilgisine değil) değerlendirilmesi; özellikle reddetme algısının çocukta hekleyenlerden farklılaşan bir mimaride seyrettiği T1DM ortamında klinik müdahale planı için zenginleştirici bir veri kaynağı oluşturmaktadır.

---

## 15.6 KISIM VI Mediation Tartışması

KISIM VI mediation analizleri için ana bulgu, frequentist + Bayesyen + multilevel paralel yaklaşımlarda **indirect effect tutarsız negatif** sonuçlanmasıdır. Bu, Goodman-Gotlib (1999) parenting-aracılı transmisyon zincirinin Türk T1DM örnekleminde *anne öz-rapor düzeyinde* başlasa da çocuk algı düzeyine *sistematik olarak iletilmediğini* işaret eden multi-informant evidensel bir desendir. Hayes Model 14 conditional indirect ve Bayesyen ROPE testi de bu deseni doğrulamış, indirect dağılımının ROPE içi pay yüksek (%65+) bulgusu pratik anlamsız sınıra yakınlık sergilemiştir. Mediation literatüründe Preacher & Hayes (2008) BCa bootstrap CI standardı uygulanmış; sonuçların yöntem-spesifik artefakt olmadığı doğrulanmıştır.

## 15.7 KISIM VII Latent Profil Tartışması

3-profil çözümü (Adapte / Standart / Yüksek-aşırı koruma + Yüksek-Beck) ve entropy = 0.81 değeri, Spurk ve diğerlerinin (2020) önerdiği multi-kriter profil seçim çerçevesine uyumludur. Profil 3 (Yüksek-Beck + Yüksek-Aşırı Koruma) DM grubunda marjinal yüksek üyelik göstermiş; bu, **klinik müdahale hedeflemesi için potansiyel bir alt-grup** önermektedir. Ancak χ² testi sınır düzeyinde anlamlı olduğundan (p ≈ .08), profil-grup ilişkisinin replikasyonu için ek örnekleme ihtiyaç vardır. Tipoloji yorumu, anne psikolojik distres yükü ile ebeveynlik aşırı korumasının T1DM bağlamında ortak bir küme oluşturduğunu — Holmbeck ve diğerlerinin (2002) gözlemlenen ebeveyn aşırı koruması bulgusuyla tutarlı — destekler.

## 15.8 KISIM VIII Ağ Analizi Tartışması

NCT (Network Comparison Test) sonuçlarının (network invariance + global strength + edge invariance) tümünde p > .05 düzeyinde kalınması, DM ve Kontrol gruplarındaki ebeveyn-çocuk ağ yapılarının **anlamlı düzeyde ayrışmadığını** göstermektedir. Borsboom ve Cramer'ın (2013) ağ-bilim psikopatoloji çerçevesinde, bu, T1DM bağlamının semptom/davranış-düzeyi etkileşim mimarisini sistematik olarak yeniden yapılandırmadığı şeklinde okunabilir. Epskamp ve diğerlerinin (2018) bootstrapped edge stability çerçevesi, küçük örneklem-orta tahmin parametre durumunda yapısal yorumlamadan ziyade *betimleyici desen okuması* önerdiği için, merkezi düğüm yorumlarımız bu epistemik ihtiyat çerçevesinde sunulmuştur.

## 15.9 KISIM IX Klinik Fayda Tartışması

İç-validasyonlu yüksek-risk anne sınıflandırma modeli (AUC "Acceptable" aralık), **Steyerberg (2019) klinik tahmin modeli geliştirme çerçevesi**'ne uyumludur. Vickers ve diğerlerinin (2018) DCA net benefit yorumu, modelin 0.10–0.40 risk eşik aralığında treat-all/treat-none stratejilerinden klinik üstünlük sergilediğini göstermiştir. Van Calster ve diğerlerinin (2019) "calibration is the Achilles heel" uyarısı çerçevesinde kalibrasyon intercept ≈ 0, slope ≈ 1 ile uygun bulunmuştur. Bu model, **dış-validasyon bekleyen** bir prototip olarak konumlandırılmıştır; bağımsız Türk merkezlerinde TRIPOD-Cluster (Vickers, 2019) çerçevesinde dış validasyon, gelecek araştırma gündeminin birincil hedefidir.

## 15.10 KISIM X DM Klinik Alt-Analizler Tartışması

HbA1c × ebeveynlik etkileşim p > .40 ve R² < 0.25 sonucu ile DM süresi spline "linear sufficient" sonucu, T1DM klinik göstergelerinin anne öz-rapor ebeveynlik tutumlarıyla bu örneklemde non-linear ilişki sergilemediğini göstermektedir. Ne var ki n = 39 düzeyinde HbA1c örnekleminin küçük-orta etki büyüklüklerini tespit etmek için **yetersiz güçte** olduğu açıktır (Cohen, 1988 standardında power < 0.50). Anderson ve diğerlerinin (1997) klasik T1DM ebeveyn-çocuk paylaşılmış sorumluluk → glisemik kontrol literatürü ve Helgeson ve diğerlerinin (2008) longitudinal bulguları, daha büyük örneklemde etkilerin tespit edilebileceğini öngörmektedir. Bizim raporumuzda bulgular "**güç sınırlamasıyla birlikte**" yorumlanmıştır; ISPAD 2024 ve ADA 2025/2026 önerilerinin (paylaşılmış sorumluluk yapısının teşviki) Türk popülasyonunda dış-validasyonu için geniş örneklemli prospektif çalışma önceliği önerilmektedir.

## 15.11 KISIM XI Robustluk Tartışması

Multiverse %0 spec p < .05 sonucu (Simonsohn ve diğerleri, 2020 specification curve) **sağlam null kanıtı** olarak konumlanmaktadır. EMBU-P alt ölçek fark etkilerinin model spesifikasyonu seçimi, kovaryat seti, alt örnek tanımı veya etki tahmin edicisi değişikliklerinden bağımsız sıfıra yakın kaldığı ispatlanmıştır. TOST aşırı koruma ve karşılaştırma "Equivalent" sonucu, Lakens'in (2017) önerdiği epistemik ihtiyat çerçevesinde *aktif null kanıtı* sağlamaktadır. Sensemakr RV_q ≤ 0.08 ve E-değer 1.36–1.59 zayıf-orta gözlemlenmemiş karıştırıcı dayanıklılığı göstergeleri, bulguları **örnek-bağlam-koşullu ön-kanıt** olarak konumlandırmamızı gerektirmektedir; bu, başka örneklemlerle replikasyon ihtiyacını vurgulayan epistemik şeffaflık adımıdır.

## 15.12 KISIM XII Bayesyen Tartışması

Bürkner'in (2017) brms paketi ile uygulanan H3 modelleri R̂ < 1.01 ve divergent transition = 0 değerleriyle sıkı posterior güvenirlik standardını karşılamaktadır. H1 modellerinde R̂_max 1.012–1.013 aralığındadır; bu değerler sıkı 1.01 eşiğinin hafif üzerinde, yaygın 1.05 eşiğinin altında ve divergent transition = 0 ile birlikte kabul edilebilir tanı alanındadır. Pinquart prior temelli BF₁₀ = 8.12 (H1 reddetme, moderate H1) ve BF₁₀ = 0.17–0.25 (H3 dört alt ölçek, moderate H0) sonuçları Jeffreys (1961) ve Wagenmakers ve diğerlerinin (2010) kanıt kademesi ölçeğinde özgün konumlanmaktadır. Kruschke'nin (2018) ROPE ±0.10 d konvansiyonu çerçevesinde gözlenen küçük etki büyüklüklerimiz çoğunlukla pratik eşdeğerlik bölgesi içine düşmekte; H3 reddetme için ROPE içi pay %92 ile özellikle güçlü bir aktif null bulgusu sergilenmektedir. Bayesyen dual reporting standardı, frequentist sonuçların **yorum belirsizliklerini** (örn. NS = sıfır mı, yoksa kanıt yetersiz mi?) çözüm yoluyla sunmuş ve bulgu paketinin epistemik şeffaflığını maksimize etmiştir.

---

\newpage

# 16 · GENEL SINIRLIKLAR

## 16.1 Tasarım Sınırlılıkları

- **Kesitsel tasarım:** Bulgular ilişki ve örüntü düzeyindedir; nedensel çıkarım için longitudinal veri gerekir. Sensemakr RV_q ≤ 0.08 ve E-değer 1.36–1.59 değerleri *zayıf-orta gözlemlenmemiş karıştırıcı dayanıklılığı* sergilemekte; bu nedenle nedensel dil sınırlama kuralı bulgu raporlamasının her noktasında uygulanmıştır.
- **Tek-merkezli örnekleme:** Marmara Üniversitesi Hastanesi Pediatrik Endokrinoloji Polikliniği'ne başvuran ailelerden seçim yapılmış; örneklem coğrafi ve sosyoekonomik temsil açısından İstanbul/Marmara bölgesi profiliyle sınırlıdır.
- **Anne odaklı bilgi-veren:** Baba (eş) ölçek doldurmamış; baba perspektifi eksiktir. NICE NG18'in iki-ebeveyn-yaklaşımı önerisi bu sınırlama nedeniyle tam karşılanmamıştır.

## 16.2 Ölçek Sınırlılıkları

- **EMBU-P/C reddetme alt ölçeği psikometrik kısıtı:** İç tutarlılık katsayıları (α + ω paralel düşüklük) madde havuzunun bu örneklemde zayıf ortak sinyal ürettiğini göstermektedir. Reddetme bulguları *toplam puan düzeyi + IRT GRM latent θ + Bayesyen latent SEM* triangülasyonuyla desteklenmiştir.
- **Hu-Bentler 1999 birleşik kriter karşılanmamış:** CFA'larda CFI ≥ .95 + SRMR ≤ .08 birleşik kriteri sağlanamamıştır; dört-faktör çözümü göreli iyileşme göstermekle birlikte yapısal model olarak mutlak doğrulanmış değildir.
- **Madde-düzeyi taban etkisi:** Reddetme alt ölçeğinde birden fazla madde ≥ %80 taban etkisi sergilemiş; bu dağılım kısıtı korelasyon ve grup farkı tahminlerini sistematik olarak aşağı çekmektedir.

## 16.3 Örneklem Büyüklüğü ve Güç Sınırlılıkları

- **n = 241 aile / 482 satır:** Birincil hipotezler (H1–H4) için Hox (2018) multilevel power analizinde %85+ güç (d = 0.20 için ICC = 0.20'de). Ancak küçük etki büyüklüklerini (d < 0.15) tespit etmek için sınır düzeydedir.
- **HbA1c n = 39:** DM grubunun yalnız %32.5'inde HbA1c verisi mevcut; KISIM X HbA1c × ebeveynlik analizleri keşifsel ve **yetersiz güçte** kalmıştır.
- **APIM ve dyadic CFA için n_dyad = 241:** Donner & Eliasziw (1992) çerçevesinde ICC ≥ 0.20 için %85+ güç; ancak k-coefficient ve RSA polinom regresyonu için DM-only (n = 120) ve Kontrol-only (n = 121) alt-analiz örneklemleri sınır düzeydedir.

## 16.4 Eksik Veri Sınırlılıkları

- **HbA1c yapısal eksikliğe dahil olmayan eksiklik:** DM grubunda HbA1c eksikliği yapısal olmayan (MAR varsayımı altında) bir kayıp olabilir; bu durumda imputasyon teorik olarak mümkündür ancak HbA1c'in klinik biyobelirteç olması gerekçesiyle imputasyon uygulanmamıştır. KISIM X bu nedenle keşifsel etiketle raporlanmaktadır.
- **MI m = 50 + FIML birincil çerçeve:** Aile-düzeyi sosyodemografi için MAR varsayımı altında çoklu atama uygulanmış; NMAR delta-adjustment grid sensitivite hattıyla varsayım kırılganlığı test edilmiştir.

## 16.5 Genelleştirilebilirlik

- Bulgular Türk T1DM popülasyonunun İstanbul/Marmara bölgesi alt grubuna **örnek-bağlam-koşullu** olarak konumlandırılmaktadır. Anadolu ve Doğu Anadolu kohortlarında replikasyon, Türkiye'nin bölgesel sosyoekonomik çeşitliliğinin değerlendirilebilmesi açısından öncelikli gelecek araştırma hedefidir.

---

\newpage

# 17 · GENEL SONUÇLAR

## 17.1 Birincil Hipotezler İçin Genel Sentez

Beş birincil hipotezin sentezi:

(a) **Anne öz-rapor düzleminde DM × Kontrol grup farkı yoktur** (H3 + KISIM XII H0 + KISIM XI multiverse + TOST eşdeğerlik). Üç-katmanlı negatif kanıt zinciri, anne ebeveynlik öz-bildiriminin T1DM bağlamında *istatistiksel olarak homojen* kaldığını göstermektedir.

(b) **Çocuk algısı düzleminde DM çocukları reddetme alt ölçeğinde Kontrol'den daha yüksek puan vermektedir** (H1 multilevel + BF₁₀ = 8.12). Bu, küçük-fakat-tutarlı (β = 0.16–0.18 SD) bir asimetridir.

(c) **Anne–çocuk diadic tutarlılığı zayıf-orta düzeydedir; DM grubunda marjinal yüksek raporlanmıştır** (H5 Olsen-Kenny dyadic CFA: Kontrol r = 0.17, DM r = 0.29).

(d) **Anne depresyonunun ebeveynlik tutumları üzerindeki latent etkisi grup-invariant olarak orta-büyüktür**; H4 SEM'de 4 yapısal yoldan 3'ü FDR-düzeltmeli anlamlıdır (sıcaklık, reddetme, karşılaştırma; anlamlı yollar için \|std. β\| = 0.28–0.33), aşırı koruma yolu pozitif fakat anlamlı değildir (std. β = 0.08, FDR p = .216).

(e) **Kardeş ilişkisi (H2 SRQ) düzleminde DM × Kontrol farkı kanıtı yetersizdir**; APIM dyadic yapı her iki grupta korunmuştur.

## 17.2 Bütünleştirici Sonuç

Türk pediatrik T1DM popülasyonunda **anne tutumları–çocuk algısı asimetrisi**, ISPAD 2024 ve ADA Standards of Care 2025/2026 kılavuzlarının çift-perspektifli aile değerlendirmesi önerilerini deneysel olarak desteklemektedir. Küçük etkiler (Funder & Ozer, 2019 sınıflandırmasında "very small but cumulatively consequential") birikimsel olarak klinik anlamlılık taşımakla birlikte, randomize müdahale çalışmaları için **moderate-precision pilot evidence** niteliği taşımaktadır.

## 17.3 Klinik Öneriler

1. **Çift-perspektifli aile değerlendirmesi** rutinleştirilmelidir; T1DM tanılı çocukların annelerinden alınan ebeveynlik öz-bildirimi, çocuğun kendi algısı ile **paralel** olarak değerlendirilmelidir.
2. **Anne mental sağlık taraması** (BDI dahil) T1DM aile takibinin ayrılmaz bir parçası olmalıdır; örneklemimizdeki yüksek antidepresan kullanım oranı (DM %29 vs Kontrol %9) bu önceliği ampirik olarak doğrulamaktadır.
3. **Reddetme algısına odaklı iletişim odaklı aile terapisi** (örn. BFST-D, Wysocki ve diğerleri, 2008) DM çocuklarında değerlendirilmelidir.
4. **Davranış sağlığı uzmanı entegrasyonu** ADA 2025/2026 ve NICE NG18'in önerdiği şekilde T1DM aile takım yapısına dahil edilmelidir.

## 17.4 Gelecek Araştırma Gündemi

1. **Longitudinal replikasyon:** Kesitsel bulguların causal yorumlanabilmesi için 12–24 aylık prospektif izleme.
2. **Çok-merkezli Türk kohortu:** Anadolu ve Doğu Anadolu örneklemlerinde replikasyon.
3. **Klinik tahmin modeli dış-validasyonu:** TRIPOD-Cluster çerçevesinde KISIM IX yüksek-risk anne sınıflandırma modelinin bağımsız Türk merkezlerinde test edilmesi.
4. **HbA1c × ebeveynlik geniş örneklem:** n ≥ 200 düzeyinde DM örnekleminde KISIM X analizlerinin tekrar tahmini.
5. **Baba-perspektifli ölçek dahiliyeti:** İki-ebeveynli aile değerlendirmelerinde NICE NG18 önerisinin tam karşılığı.
6. **Müdahale çalışmaları:** BFST-D adaptasyonu RCT için pilot evidence olarak konumlandırılmalı.

---

\newpage

# 18 · YAYIN VE DİSEMİNASYON STRATEJİSİ

| Çıktı | Kapsam | Hedef dergi | Durum |
|---|---|---|---|
| **Doktora tezi** | H1–H5 + KISIM VI–XII tam | Marmara SBE Sosyal Pediatri savunma | Yazım fazında |
| **Adaptasyon makalesi** | KISIM IV psikometrik validasyon | *Pediatric Diabetes* / *J Pediatric Psychology* | İskelet hazır, R kod tetiklenmesi bekliyor |
| **H1 + H5 makalesi** | Çocuk algısı + diadic concordance | *Journal of Family Psychology* / *J Pediatric Psychology* | Planlanan |
| **Risk skor makalesi** | KISIM IX + TRIPOD | *Pediatric Diabetes* / *Diabetes Care* | İç-validasyonlu, dış validasyon bekliyor |
| **OSF + Zenodo paketi** | Kod + SAP + kanonik dokümantasyon | DOI atandığında public | Embargo onayı bekliyor |

---

\newpage

# 19 · TEMEL REFERANSLAR (Çekirdek Atıflar; Tam Liste `references.bib`)

## 19.1 Çekirdek Meta-Analizler ve Kuramsal Temeller

- Pinquart, M. (2013). *Journal of Pediatric Psychology, 38*(7), 708–721. DOI: 10.1093/jpepsy/jst020.
- Pinquart, M. (2017). *Developmental Psychology, 53*(5), 873–932. DOI: 10.1037/dev0000295.
- Pinquart, M. (2018). *Stress & Health, 34*(2), 197–207. DOI: 10.1002/smi.2780.
- De Los Reyes, A., ve diğerleri (2015). *Psychological Bulletin, 141*(4), 858–900. DOI: 10.1037/a0038498.
- De Los Reyes, A., ve diğerleri (2023). *J Clin Child Adolesc Psychol, 52*(1), 19–54.
- Goodman, S. H., & Gotlib, I. H. (1999). *Psychological Review, 106*(3), 458–490.
- Lovejoy, M. C., ve diğerleri (2000). *Clinical Psychology Review, 20*(5), 561–592.
- Buist, K. L., Deković, M., & Prinzie, P. (2013). *Clinical Psychology Review, 33*(1), 97–106.
- Jensen, A. C., ve diğerleri (2024). *Child Development*. DOI: 10.1111/cdev.14091.

## 19.2 Yöntem ve İstatistik Kaynakları

- Olsen, J. A., & Kenny, D. A. (2006). *Psychological Methods, 11*(2), 127–141.
- Kenny, D. A., Kashy, D. A., & Cook, W. L. (2006). *Dyadic Data Analysis*. Guilford.
- Cinelli, C., & Hazlett, C. (2020). *J Royal Statistical Society B, 82*(1), 39–67.
- VanderWeele, T. J., & Ding, P. (2017). *Annals of Internal Medicine, 167*(4), 268–274.
- Lakens, D. (2017). *Social Psychological and Personality Science, 8*(4), 355–362.
- Lakens, D., Scheel, A. M., & Isager, P. M. (2018). *AMPPS, 1*(2), 259–269.
- Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). *Nature Human Behaviour, 4*, 1208–1214.
- Bürkner, P.-C. (2017). *Journal of Statistical Software, 80*(1), 1–28.
- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.
- Kruschke, J. K. (2018). *AMPPS, 1*(2), 270–280.
- Funder, D. C., & Ozer, D. J. (2019). *AMPPS, 2*(2), 156–168.
- Schäfer, T., & Schwarz, M. A. (2019). *Frontiers in Psychology, 10*, 813.
- Borsboom, D., & Cramer, A. O. J. (2013). *Annual Review of Clinical Psychology, 9*, 91–121.
- Epskamp, S., Borsboom, D., & Fried, E. I. (2018). *Behavior Research Methods, 50*(1), 195–212.
- Spurk, D., ve diğerleri (2020). *Journal of Vocational Behavior, 120*, 103445.
- Steyerberg, E. W. (2019). *Clinical Prediction Models* (2nd ed.). Springer.
- Vickers, A. J., & Elkin, E. B. (2006). *Medical Decision Making, 26*(6), 565–574.
- Van Calster, B., ve diğerleri (2018). *European Urology, 74*(6), 796–804.

## 19.3 Klinik Kılavuzlar ve T1DM Literatür

- ISPAD Clinical Practice Consensus Guidelines 2024. *Hormone Research in Paediatrics, 97*(6).
- ADA Professional Practice Committee (2026). *Diabetes Care, 49*(Suppl. 1), S297.
- NICE Guideline NG18 (2023 güncelleme). *Diabetes (type 1 and type 2) in children and young people*.
- Yeşilkaya, E., ve diğerleri (2017). *Diabetic Medicine, 34*(3), 405–410.
- Vuralli, D., ve diğerleri (2024). *Journal of Diabetes, 16*(4).
- Anderson, B. J., ve diğerleri (1997). *Journal of Pediatrics, 130*(2), 257–265.
- Helgeson, V. S., ve diğerleri (2008). *Journal of Pediatric Psychology, 33*(5), 497–508.
- Bassi, G., ve diğerleri (2020). *IJERPH, 18*(1), 152.
- Cousino, M. K., & Hazen, R. A. (2013). *J Pediatric Psychology, 38*(8), 809–828.

## 19.4 Türkçe Uyarlama Kaynakları

- Hisli, N. (1989). *Psikoloji Dergisi, 7*(23), 3–13.
- Sümer, N., & Güngör, D. (1999). *Türk Psikoloji Dergisi, 14*(44), 35–60.
- Dirik, G., Yorulmaz, O., & Karancı, A. N. (2015). *Türk Psikiyatri Dergisi, 26*(2), 123–130.
- Kapci, E. G., ve diğerleri (2008). *Depression and Anxiety, 25*(10), E104–E110.
- Adal, E., ve diğerleri (2015). *JCRPE, 7*(1), 57–62.

## 19.5 Raporlama Standartları

- von Elm, E., ve diğerleri (2007). *Annals of Internal Medicine, 147*(8), 573–577. (STROBE)
- Vandenbroucke, J. P., ve diğerleri (2007). *PLoS Medicine, 4*(10), e297.
- Appelbaum, M., ve diğerleri (2018). *American Psychologist, 73*(1), 3–25. (JARS-Quant)
- Collins, G. S., ve diğerleri (2015). *Annals of Internal Medicine, 162*(1), 55–63. (TRIPOD)

---

\newpage

# 20 · EKLER

## Ek A — Pre-Registration Sapma Tablosu Özeti

`docs/analiz_planlari/PRE-REGISTRATION-DEVIATION-TABLE.md` dosyasının ilk 12 ayda raporlanan tüm sapmaları içeren tam sürümü tezde Ek B'de yer alacaktır. Şu an itibarıyla:

- Tip 1 (trivial) sapma: 1 (paket sürüm güncellemesi)
- Tip 2 (minor) sapma: 0
- Tip 3 (major) sapma: 0

## Ek B — STROBE + JARS-Quant + TRIPOD Kontrol Listeleri

Tam kontrol listeleri tezde Ek C, D ve E olarak yer alacaktır; tüm 22 STROBE, JARS-Quant ve TRIPOD maddesi için uyumluluk durumu belgelenmiştir.

## Ek C — Veri Sözlüğü

`docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md` dosyası tüm 288 family + 203 long sütununun tanımını, kodlama standardını ve yapısal NA kurallarını içermektedir.

## Ek D — Reprodüktiblik Runbook

`docs/analiz_planlari/REPRODUCIBILITY-RUNBOOK.md` tam pipeline yeniden çalıştırma talimatlarını (renv + Docker + targets) içermektedir.

## Ek E — Etik ve Veri Yönetim Planı

`docs/analiz_planlari/ETHICS-DATA-MANAGEMENT-PLAN.md` L0-L3 veri sınıflandırma matrisi, KVKK uyumluluğu ve OSF embargo süreciyle ilgili ayrıntıları belgelemektedir.

---

# CSR ONAYI

| Onaylayan | Rol | İmza | Tarih |
|---|---|---|---|
| Uzm.Dr. Özlem Murzoğlu Kurt | PI / Doktora öğrencisi | ……………………………… | …………… |
| Prof.Dr. Eren Özek | Tez danışmanı | ……………………………… | …………… |
| Doç.Dr. Belma Haliloğlu | Yardımcı araştırıcı | ……………………………… | …………… |
| Prof.Dr. Perran Boran | TİK üyesi | ……………………………… | …………… |
| Prof.Dr. Nalan Karabayır | TİK üyesi | ……………………………… | …………… |

---

**CSR sürüm:** v1.1 — Doktora Savunması Sürümü (sistematik denetim sonrası revize)
**Raporlama disiplini:** APA 7 + STROBE (gözlemsel) + JARS-Quant + TRIPOD; çoklu strateji disiplini ve nedensel dil sınırlama kuralları korunmuştur.
