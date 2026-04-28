# Kaynak Kitaplar Haritası — `docs/books/` ile Tez Bölümleri

**Ne zaman oku:** Bir karar için "hangi kitap?" sorusu; bir tez paragrafına atıf eklerken;
bir yöntem seçimini gerekçelendirirken; metodolojik tartışmanın kökenine inerken.

**Lokasyon:** `/mnt/thunderbolt/workspaces/doktoratezi/docs/books/` — 16 PDF/EPUB temel
referans kitabı.

---

## Hızlı Eşleme: Konu → Kitap

| Sorgun bu konuda mı? | Önce şu kitabı aç |
|----------------------|-------------------|
| **Genel R + tidyverse veri yönetimi** | Wickham, Çetinkaya-Rundel & Grolemund (R for Data Science) |
| **Klasik istatistik temeli** | Field, Miles & Field (Discovering Statistics Using R) |
| **Makine öğrenmesi + classification** | James, Witten, Hastie & Tibshirani (ISL) |
| **Olasılık + temel teori** | Aggarwal (Probability and Statistics for ML) |
| **Genel istatistiksel akıl yürütme** | Michelucci (Statistics for Scientists) |
| **Regresyon + Bayesian foundations** | Gelman, Hill & Vehtari (Regression and Other Stories) |
| **Bayesian course + DAG + multilevel** | McElreath (Statistical Rethinking) |
| **Multilevel modeller (lme4 odaklı)** | Hox, Moerbeek & van de Schoot (Multilevel Analysis) |
| **CFA pratik uygulama** | Brown (Confirmatory Factor Analysis) |
| **SEM kanonu** | Kline (Principles and Practice of SEM) |
| **Dyadic veri (APIM)** | Kenny, Kashy & Cook (Dyadic Data Analysis) |
| **Mediation + Moderation (Hayes PROCESS) | Hayes (Introduction to Mediation, Moderation, Conditional Process Analysis) |
| **Eksik veri (MI, FIML, sensitivity)** | Enders (Applied Missing Data Analysis) |
| **Ölçek geliştirme + güvenilirlik teorisi** | DeVellis & Thorpe (Scale Development) |
| **R Markdown / Quarto reproducibility** | Xie, Dervieux & Riederer (R Markdown Cookbook) |

---

## Detaylı Harita — Her Kitap Hangi Tez Bölümünde Ne Yapıyor?

### 1. Field, Miles & Field — *Discovering Statistics Using R* (epub)

**Genel rol:** Klasik istatistik + R workflow temeli. Birinci yıl mezun seviyesi. Bu projede
**lojistik kararlar** için referans (test seçimi, varsayım kontrolü).

| Bu Tezde | Bölüm | Field Ch. |
|----------|-------|-----------|
| t-test & ANOVA temelleri | Bulgular §H1, §H2 | 9, 11 |
| Multiple regression diagnostics | Bulgular §H3 | 7 |
| Effect size hesabı | Bulgular tüm | 5, 9 |
| Assumption checking | Bulgular §H1, §H3 | 5 |
| Korelasyon yorumlama | Bulgular §psikometri | 6 |

Atıf örneği: `[@field2012, p. 312]`.

---

### 2. Wickham, Çetinkaya-Rundel & Grolemund — *R for Data Science* (epub)

**Genel rol:** tidyverse-merkezli veri yönetimi. `dplyr`, `tidyr`, `ggplot2`, `purrr`.
Pipeline kütüphane katmanı (`R/01_io.R` … `R/19_*.R`) tüm fonksiyonlarda bu stil aktif.

| Bu Tezde | Bölüm | R4DS Ch. |
|----------|-------|----------|
| Veri temizleme (clean_names, NA handling) | Yöntem §veri yönetimi | 5–7 |
| `pivot_longer/wider` (geniş↔uzun) | Yöntem §çerçeveler | 6 |
| `purrr::map_dfr` (çoklu test toplama) | Bulgular §multiverse | 26 |
| `ggplot2` figür üretimi | Bulgular tüm grafikler | 28 |
| `rowwise()` (alt ölçek skor türetme) | `R/10_derived_scores.R` | — |

---

### 3. James, Witten, Hastie & Tibshirani — *An Introduction to Statistical Learning with Applications in R (ISLR)* (epub)

**Genel rol:** ML temeli. Bu projede tezin merkezinde değil ama **regularization +
cross-validation** kavramı sensemakr ve specr için arka plan.

| Bu Tezde | Bölüm | ISL Ch. |
|----------|-------|---------|
| Cross-validation (model seçim) | Yöntem §mass-univariate (varsa) | 5 |
| Regularization (LASSO/ridge) | Yöntem §çoklu evren analizi | 6 |
| Bias-variance tradeoff | Tartışma §sınırlamalar | 2 |

---

### 4. Aggarwal — *Probability and Statistics for Machine Learning* (pdf)

**Genel rol:** Olasılık + Bayesçi temeller (conjugate prior, posterior). brms kullanımının
arkasındaki teori için. Bu projede **prior türetimi** (Pinquart 2013 → Normal prior)
gerekçelendirme.

| Bu Tezde | Bölüm | Aggarwal Ch. |
|----------|-------|--------------|
| Bayes kuralı + prior/posterior | Yöntem §H4 Bayesian preflight | 2 |
| Conjugate priors | references/ileri-yontemler.md | 3 |
| Hypothesis testing framework | Bulgular §H1 Bayesian | 6 |

---

### 5. Michelucci — *Statistics for Scientists* (book) → references/formulas-and-theory

**Genel rol:** Tüm temel istatistik formülleri (mean, variance, hypothesis testing,
correlation). devstats skill'inin formula-and-theory referansının temel kaynağı.

| Bu Tezde | Bölüm | Michelucci Ch. |
|----------|-------|----------------|
| Tanımlayıcı istatistik bölümü | Bulgular §Tablo 1 | 4–5 |
| Anscombe Quartet uyarısı | Yöntem §veri keşif | 5 |
| Hypothesis testing framework | Bulgular tüm | 12 |
| Correlation interpretation | Bulgular §korelasyon | 13 |

---

### 6. Gelman, Hill & Vehtari — *Regression and Other Stories* (pdf)

**Genel rol:** Modern regresyon felsefesi (regresyon = karşılaştırma, etki değil; design
analysis; Type M error; informative prior). Bu projedeki tüm regresyon yorumu Gelman
mantra'sı altında: "DM grubu için tahmin = karşılaştırma, neden değil."

| Bu Tezde | Bölüm | Gelman ROS Ch. |
|----------|-------|----------------|
| Regresyon = karşılaştırma | Yöntem §yorum dilbilgisi | 1, 9 |
| Prior specification (3 düzey) | references/ileri-yontemler.md | 9 |
| Design analysis & winner's curse | Tartışma §sınırlamalar | 16 |
| Fake-data simulation (model check) | Yöntem §H4 SEM doğrulama | 8 |
| Causal inference framework | references/nedensellik-ve-ps.md | 18–21 |
| Multilevel temelleri | references/multilevel-aile-yapisi.md | 11–12 |

**Atıf yoğunluğu yüksek** — temel yorumsal felsefenin %30+'ı buradan.

---

### 7. McElreath — *Statistical Rethinking* (epub)

**Genel rol:** Bayesçi + DAG + multilevel'i birlikte düşünmek. brms ile değiştirilebilir
örnekler. Generative model thinking. Bu projede **DAG yapımı**, **multilevel partial
pooling** ve **MCMC diagnostics** McElreath odaklı.

| Bu Tezde | Bölüm | McElreath Ch. |
|----------|-------|---------------|
| Generative model thinking | Yöntem §kuram → veri | 1–2 |
| DAG-based causal reasoning | references/nedensellik-ve-ps.md | 5–6 |
| Multilevel = adaptive regularization | references/multilevel-aile-yapisi.md | 13–14 |
| Ordered categorical (Beck items) | references/ileri-yontemler.md §H4 | 12 |
| MCMC diagnostics (Rhat, n_eff) | references/ileri-yontemler.md §brms | 9 |
| WAIC / PSIS-LOO model comparison | references/ileri-yontemler.md §brms | 7 |
| Regularizing priors | references/etki-buyuklugu-ve-guc.md | 4–6 |
| Prior predictive simulation | references/ileri-yontemler.md §brms | 4 |

---

### 8. Hox, Moerbeek & van de Schoot — *Multilevel Analysis* (pdf)

**Genel rol:** Multilevel modellemenin temel referansı. lme4-uyumlu (R odaklı). Bu
projedeki tüm multilevel kararlar (ICC, sample size, centering) Hox kuralları altında.

| Bu Tezde | Bölüm | Hox Ch. |
|----------|-------|---------|
| ICC + design effect | Yöntem §H1, references/multilevel-aile-yapisi.md | 1, 2 |
| Sample size kuralları | Tartışma §güç | 12 |
| Group-mean centering | references/multilevel-aile-yapisi.md | 4 |
| Within/between decomposition | Bulgular §H1 sensitivity | 4 |
| REML vs ML | references/multilevel-aile-yapisi.md | 3 |
| Kenward-Roger df | references/multilevel-aile-yapisi.md | 12 |

---

### 9. Brown — *Confirmatory Factor Analysis for Applied Research* (pdf)

**Genel rol:** CFA kanonu. lavaan-pratik. Bu projede H4 latent ölçüm modelinin tüm
kararları + EMBU/BDI/KİA validation.

| Bu Tezde | Bölüm | Brown Ch. |
|----------|-------|-----------|
| Model spec (latent → indicator) | references/psikometri-pipeline.md | 4 |
| Fit index ekosistemi | references/psikometri-pipeline.md | 5 |
| Modification indices (DİKKATLİ) | references/psikometri-pipeline.md | 4–5 |
| Measurement invariance | references/psikometri-pipeline.md | 7 |
| Non-normal data (WLSMV/MLR) | Yöntem §H4 | 9 |
| Bifactor models (alternatif H4 spec) | Tartışma §H4 model alternatifleri | 9 |

---

### 10. Kenny, Kashy & Cook — *Dyadic Data Analysis* (pdf)

**Genel rol:** APIM ve dyadic CFA referansı. Bu projede H2 (kardeş ilişkisi) tüm
kararları Kenny çerçevesinde.

| Bu Tezde | Bölüm | Kenny Ch. |
|----------|-------|-----------|
| APIM modeli | references/multilevel-aile-yapisi.md, ileri-yontemler.md | 5 |
| Distinguishable vs indistinguishable | Yöntem §H2 | 4 |
| Olsen-Kenny CFA (latent dyadic) | references/multilevel-aile-yapisi.md | 6 |
| Nonindependence in dyads | Yöntem §H2 | 1 |
| MLM for dyadic data | references/multilevel-aile-yapisi.md | 7 |

---

### 11. Hayes — *Introduction to Mediation, Moderation, and Conditional Process Analysis* (pdf)

**Genel rol:** Mediation + moderation kanonu (PROCESS makrosu kitap dili). Bu projede
**aracılık analizi** (Beck → EMBU-P → EMBU-C) ve **conditional process** (H1 üç-yönlü
etkileşim) referansı.

| Bu Tezde | Bölüm | Hayes Ch. |
|----------|-------|-----------|
| Mediation a/b/c'-yolları | references/ileri-yontemler.md, raporlama-sablonlari.md §13 | 3 |
| Bootstrap CI (BCa) | references/ileri-yontemler.md | 4 |
| Moderation çerçevesi | references/ileri-yontemler.md | 7 |
| Conditional indirect effect (Model 7) | references/ileri-yontemler.md | 12 |
| Index of moderated mediation | references/ileri-yontemler.md | 12 |

---

### 12. Enders — *Applied Missing Data Analysis* (pdf + md)

**Genel rol:** Eksik veri kanonu. mice, FIML, sensitivity. Bu projedeki üç çerçeveli
strateji Enders'tan.

| Bu Tezde | Bölüm | Enders Ch. |
|----------|-------|------------|
| MCAR/MAR/MNAR mekanizmaları | references/eksik-veri-yonetimi.md | 1 |
| FIML | references/eksik-veri-yonetimi.md | 4 |
| Multiple imputation (Rubin rules) | references/eksik-veri-yonetimi.md | 5 |
| Auxiliary variables | references/eksik-veri-yonetimi.md | 6 |
| Convergence diagnostics | references/eksik-veri-yonetimi.md | 5 |
| Sensitivity (NMAR delta) | references/eksik-veri-yonetimi.md | 9 |
| Pattern-mixture vs selection model | Tartışma §eksik veri sınırlamaları | 9 |

---

### 13. DeVellis & Thorpe — *Scale Development: Theory and Applications* (pdf)

**Genel rol:** Ölçek geliştirme + reliability teorisi (alpha vs omega). Bu projede
**psikometrik validasyon** kararlarının teorik kökü.

| Bu Tezde | Bölüm | DeVellis Ch. |
|----------|-------|--------------|
| Reliability teorisi (CTT) | references/psikometri-pipeline.md | 3 |
| Alpha sınırları (lower bound) | references/psikometri-pipeline.md | 3 |
| McDonald omega tercih | references/psikometri-pipeline.md | 3 |
| Scale vs Index distinction | references/psikometri-pipeline.md | 6 |
| EFA: PAF (NOT PCA) | references/psikometri-pipeline.md | 6 |
| Factor loading thresholds | references/psikometri-pipeline.md | 6 |
| Cultural adaptation (s-EMBU TR) | Yöntem §EMBU TR adaptasyonu | 7 |

---

### 14. Kline — *Principles and Practice of Structural Equation Modeling* (pdf)

**Genel rol:** SEM kanonu (5. baskı). lavaan örnekleri. Bu projede H4 SEM raporlama
standardı + DAG-based causal reasoning Kline'a göre.

| Bu Tezde | Bölüm | Kline Ch. |
|----------|-------|-----------|
| SEM prerequisites (N, identification) | Yöntem §H4 | 4 |
| Two-step approach (Anderson-Gerbing) | Yöntem §H4 | 9 |
| Fit index framework (4 indeks paketi) | references/psikometri-pipeline.md, ileri-yontemler.md | 8 |
| DAG ve nonparametric causal models | references/nedensellik-ve-ps.md | 6 |
| Equivalent models | Tartışma §H4 alternatif | 11 |
| Measurement invariance hierarchy | references/psikometri-pipeline.md | 9 |
| Small-sample SEM (SAM, parceling) | Tartışma §H4 sınırlamaları | 12 |

---

### 15. Xie, Dervieux & Riederer — *R Markdown Cookbook* (epub)

**Genel rol:** R Markdown / Quarto reproducibility kılavuzu. Bu projede tüm `.qmd`
düzenlemeleri + reproducible reporting.

| Bu Tezde | Bölüm | Xie Ch. |
|----------|-------|---------|
| Pipeline (Rmd → md → final) | references/tez-yazim-rehberi.md | 2 |
| Chunk options reference | references/tez-yazim-rehberi.md | 11 |
| Parameterized reports | Bulgular §grup-spesifik raporlar | 17 |
| Cross-references | references/tez-yazim-rehberi.md | 4 |
| Bibliography management | references/tez-yazim-rehberi.md | 4 |
| Child documents | thesis.qmd → chapters/* | 16 |

---

## Ek Kaynaklar (Kitap Dışı, references.bib'te)

Bu projenin yöntem felsefesi için kritik makaleler:

| Kaynak | Konu | Bu Projede |
|--------|------|------------|
| Pinquart (2013) | Parenting–child outcome meta-analizi | Bayesian prior + benchmark |
| De Los Reyes ve diğerleri (2015) | Multi-informant validity | Yöntem §multi-informant + Tartışma |
| Cinelli & Hazlett (2020) | sensemakr Robustness Value | Sensitivity raporu standardı |
| Lakens (2017) | TOST eşdeğerlik testi | "Anlamsız fark" yorumu |
| Simonsohn ve diğerleri (2020) | Specification curve | Multiverse raporu |
| Hu & Bentler (1999) | CFA fit cutoff (CFI ≥ .95, RMSEA ≤ .06) | Psikometri raporu |
| Cheung & Rensvold (2002) | Invariance ΔCFI eşik | Ölçüm değişmezliği |
| Robins, Hernan & Brumback (2000) | IPTW stabilized weights | Yöntem §propensity score |
| Schäfer & Schwarz (2019) | Etki büyüklüğü domain calibration | references/etki-buyuklugu-ve-guc.md |
| Funder & Ozer (2019) | Small effects'in önemi | Tartışma §pratik anlam |
| Hamaker, Kuiper & Grasman (2015) | RI-CLPM | Tartışma §gelecek araştırma |
| Olsen & Kenny (2006) | Distinguishable dyad CFA | H2 latent korelasyon |
| Furman & Buhrmester (1985) | KİA orijinal | Yöntem §ölçek |
| Apalaçi (1996) | KİA Türkçe adaptasyon | Yöntem §ölçek |
| Sümer ve diğerleri | s-EMBU Türkçe adaptasyon | Yöntem §ölçek |
| Hisli (1989) | Beck Türkçe adaptasyon | Yöntem §ölçek |
| Bürkner (2017) | brms paketi | Yöntem §Bayesian |
| Rosseel (2012) | lavaan paketi | Yöntem §SEM |

---

## Kullanım Stratejisi

1. **Sorgu geldiğinde:** Yukarıdaki "Hızlı Eşleme" tablosuyla kitabı seç.
2. **Kitabın TOC'una git:** Detaylı haritada listelenen bölümler.
3. **Notu çıkar:** Kavram + sayfa/bölüm + bu projedeki bağlam.
4. **`references.bib`'te BibTeX entry'sini doğrula:** Yoksa ekle (`@book{...}` formunda).
5. **Atıfı `[@key]` formatında yerleştir:** Quarto auto-render eder.

---

## Atıf Yoğunluğu Tahmini (Tezin Tüm Bölümlerinde)

Birinci yıl yazım için kaba tahmin (atıf adedi):

- **Gelman, Hill & Vehtari (2021):** ~25 atıf — yöntem felsefesi
- **McElreath (2020):** ~15 atıf — Bayesian + DAG
- **Hox ve diğerleri (2018):** ~12 atıf — multilevel
- **Brown (2015):** ~10 atıf — CFA
- **Kline (2023):** ~10 atıf — SEM
- **Enders (2022):** ~10 atıf — eksik veri
- **Kenny ve diğerleri (2006):** ~8 atıf — APIM
- **DeVellis & Thorpe (2022):** ~8 atıf — psikometri
- **Hayes (2022):** ~6 atıf — mediation
- **Field ve diğerleri (2012):** ~5 atıf — klasik
- **Wickham ve diğerleri (2023):** ~3 atıf — R workflow
- **Pinquart (2013):** ~12 atıf — meta-analiz benchmark
- **De Los Reyes ve diğerleri (2015):** ~5 atıf — multi-informant
- Diğerleri: ~30 atıf

**Tahmini toplam: 160–180 atıf** (doktora tezi normu).

---

## Bibliyografya Öncelik Listesi (`references.bib` Doldurma)

`references/references.bib` içinde MUTLAKA bulunması gerekenler:

```
@book{enders2022, ...}
@book{brown2015, ...}
@book{kline2023, ...}
@book{kenny2006, ...}
@book{hox2018, ...}
@book{devellis2022, ...}
@book{hayes2022, ...}
@book{gelman2021, ...}
@book{mcelreath2020, ...}
@book{field2012, ...}
@book{wickham2023, ...}
@book{aggarwal2025, ...}
@book{michelucci2025, ...}
@book{xie2021, ...}

@article{pinquart2013, ...}
@article{delosreyes2015, ...}
@article{cinelli2020, ...}
@article{lakens2017, ...}
@article{simonsohn2020, ...}
@article{huBentler1999, ...}
@article{cheungRensvold2002, ...}
@article{robins2000, ...}
@article{schaferSchwarz2019, ...}
@article{funderOzer2019, ...}
@article{hamaker2015, ...}
@article{olsenKenny2006, ...}
@article{furmanBuhrmester1985, ...}
@article{burkner2017, ...}
@article{rosseel2012, ...}

@manual{Rcore2024, ... title = {R: A Language and Environment for Statistical Computing}, ...}
@manual{lme4, ...}
@manual{lavaan, ...}
@manual{brms, ...}
@manual{mice, ...}
@manual{targets, ...}
```

Not: `citation("paketAdı")` R'de paket atıfını verir; bunu BibTeX'e dönüştür.

---

## "Hangi Kitap Hangi Karar?" Akış Diyagramı

```
SORGU TİPİ
│
├── Veri yönetimi/wrangling? → Wickham (R4DS) + Field (R workflow)
│
├── Tanımlayıcı istatistik? → Field + Michelucci
│
├── Test seçimi? → Field (Ch. 5–11) + devstats test-selection-guide
│
├── Regresyon yorumu? → Gelman ROS (regresyon = karşılaştırma!)
│
├── Multilevel?
│   ├── Pratik kod → Hox (Ch. 4–5)
│   └── Felsefe → McElreath (Ch. 13–14, partial pooling)
│
├── CFA?
│   ├── Pratik → Brown
│   └── Teori → DeVellis
│
├── SEM?
│   ├── Spec + fit → Kline + Brown
│   └── Causal yorum → Kline (Ch. 6) + McElreath (Ch. 5–6)
│
├── Mediation? → Hayes + lavaan dokümantasyon
│
├── Dyadic? → Kenny
│
├── Bayesian?
│   ├── Felsefe → McElreath
│   ├── Pratik → Gelman ROS + Bürkner brms
│   └── Prior türetimi → Pinquart (meta-analiz) + Aggarwal (conjugate)
│
├── Eksik veri? → Enders
│
├── Causal inference?
│   ├── DAG → McElreath + Kline + Pearl primer (eklenmeli)
│   └── PS/IPTW → Gelman ROS (Ch. 18–21) + Stuart 2010 (eklenmeli)
│
├── Sensitivity?
│   └── Cinelli & Hazlett (sensemakr)
│
├── Equivalence/TOST? → Lakens 2017
│
├── Multiverse? → Simonsohn 2020 + Steegen 2016
│
├── Etki büyüklüğü? → references/etki-buyuklugu-ve-guc.md (Schäfer + Funder)
│
└── Reproducible reporting? → Xie (R Markdown Cookbook)
```

---

## SAP v3.0 Genişletilmiş Kaynak Haritası (KISIM V-XVII)

SAP v3.0 §XVIII'deki >100 kaynaktan **projedeki uygulama eşlemesi**:

### Diadik analiz (H5)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Olsen & Kenny** *Psychological Methods* "SEM with interchangeable dyads" | 2006 | H5 dyadic CFA modeli — true latent concordance |
| **Edwards & Parry** *Academy Manag. J.* "Polynomial regression equations" | 1993 | H5 RSA 4 parametre (a1-a4) — tutarsızlık → outcome |
| **Kenny, Kashy & Cook** *Dyadic Data Analysis* (Guilford) | 2006 | k-coefficient çerçevesi (KISIM V H5) + APIM teorisi |
| **Ledermann & Kenny** *J. Family Psychol.* "Dyadic data: MLM vs SEM" | 2017 | H5 strateji seçimi gerekçe |
| **Bland & Altman** *Lancet* "Statistical methods for assessing agreement" | 1986 | H5 Bland-Altman LoA — mutlak fark dispersiyonu |
| **Koo & Li** *J. Chiropr. Med.* "ICC interpretation guidelines" | 2016 | ICC eşik yorumu (.50, .75, .90) |

### Mediation (KISIM VI)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Hayes** *Intro to Mediation, Moderation, and Conditional Process* (2nd) | 2018 | KISIM VI Model 4/7/14, IMM (index of moderated mediation) |
| **Preacher & Hayes** *Behav Res Methods* "Asymptotic and resampling strategies" | 2008 | BCa bootstrap CI standardı — Sobel modası geçmiş |
| **MacKinnon** *Statistical Mediation Analysis* (Erlbaum) | 2008 | Multilevel mediation (Bauer-Preacher 1-1-1) |
| **VanderWeele** *Explanation in Causal Inference* (Oxford) | 2015 | DAG-temelli mediation; mediator-outcome confounder |
| **Yuan & MacKinnon** *Psychological Methods* "Bayesian mediation" | 2009 | Bayesian indirect distribution + ROPE |
| **Bauer, Preacher & Gil** *Psychological Methods* "1-1-1 multilevel mediation" | 2006 | KISIM VI Level-1 vs Level-2 ayrımı |

### Latent değişken (KISIM VII)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Lanza & Cooper** *Child Dev. Perspectives* "LCA for developmental research" | 2016 | LPA mantığı + 4-profil seçimi |
| **Akogul & Erisoglu** *Comm. Stats — Sim. Comp.* "Mixture model selection" | 2017 | BIC + entropy + LMR-LRT karar matrisi |
| **Eid et al.** *Psychological Methods* "Bifactor S-1 indicators" | 2017 | EMBU-P Bifactor S-1 modeli, ECV/PUC/ω_h |
| **Reise** *Multivariate Behav Res* "Bifactor model invariance" | 2012 | Bifactor metrik yorumlama (ω_h > .50 unidim) |
| **Rosenberg et al.** *J. Open Source Software* "tidyLPA" | 2018 | tidyLPA paket implementasyonu |
| **Nylund-Gibson & Choi** *Translational Issues* "LPA best practices" | 2018 | Profil yorumlama, classification uncertainty |

### Network analizi (KISIM VIII)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Borsboom** *World Psychiatry* "Network theory of mental disorders" | 2017 | Beck symptom network teorik temel |
| **Epskamp, Borsboom & Fried** *Behav Res Methods* "Network estimation" | 2018 | EBIC-LASSO, gamma=0.5, CS-coefficient .25/.50 eşiği |
| **van Borkulo et al.** *Psychological Methods* "NCT" | 2017 | Network Comparison Test — 3 invariance |
| **Fried et al.** *Soc. Psych. Psychiatr. Epidemiol.* "Network as problems" | 2017 | Klinik ağ yorumu |
| **Costantini et al.** *J. Abnormal Psychol.* "Network analysis methodology" | 2019 | Centrality stability (CS-coefficient) |

### Klinik fayda (KISIM IX)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Vickers & Elkin** *Med Decis Making* "Decision curve analysis" | 2006 | DCA net benefit framework |
| **Pencina et al.** *Stat Med* "NRI/IDI" | 2008 | Marjinal sınıflandırma iyileştirmesi |
| **Pepe et al.** *Stat Med* "Limitations of NRI" | 2014 | NRI eleştirisi → cfNRI alternatif |
| **Harrell** *Regression Modeling Strategies* (2nd, Springer) | 2015 | Bootstrap-corrected calibration (B=1000) |
| **Hosmer, Lemeshow & Sturdivant** *Applied Logistic Regression* (3rd) | 2013 | AUC eşikleri (.70-.80 kabul edilebilir) |
| **Steyerberg** *Clinical Prediction Models* (2nd, Springer) | 2019 | Risk skoru türetme + iç validasyon |
| **Breiman et al.** *Classification and Regression Trees* (CRC) | 1984 | CART 1-SE pruning rule |

### Robustluk ve sensitivite (KISIM XI)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Steegen, Tuerlinckx, Gelman & Vanpaemel** *PPS* "Multiverse" | 2016 | Multiverse spec setup mantığı |
| **Simonsohn, Simmons & Nelson** *Nature Hum Behav* "Spec curve" | 2020 | Inferential spec curve (Z_median, Z_share, Z_aggregate) |
| **Lakens** *SPPS* "Equivalence tests" | 2017 | TOST üçlü karar matrisi (Trivial/EQ/Meaningful/IND) |
| **Lakens** *Collabra: Psychology* "Sample size justification" | 2022 | SESOI tanımı → ±0.30 SMD |
| **Cinelli & Hazlett** *JRSS-B* "Making sense of sensitivity" | 2020 | sensemakr Robustness Value (RV_q) |
| **VanderWeele & Ding** *Annals Internal Med* "E-value" | 2017 | E-value eşiği (>2.0 orta dayanıklılık) |
| **Lipsitch, Tchetgen Tchetgen & Cohen** *Epidemiology* "Negative controls" | 2010 | Negative outcome/exposure çerçevesi |
| **Hernán & Robins** *Causal Inference: What If* (Chapman/CRC) | 2020 | Falsification testi mantığı |
| **Gelman & Loken** *American Statistician* "Garden of forking paths" | 2014 | Spec curve mantığı arka planı |
| **Simonsohn et al.** *Adv Methods Pract Psychol Sci* "Specification curve" | 2020 | Permütasyon-tabanlı global anlamlılık |

### Bayesci metodoloji (KISIM XII)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Bürkner** *J Stat Software* "brms package" | 2017 | brms multilevel + prior specification |
| **Vehtari, Gelman & Gabry** *Stat Comput* "PSIS-LOO" | 2017 | LOO Pareto-k diagnostics |
| **Yao, Vehtari, Simpson & Gelman** *Bayesian Analysis* "Stacking" | 2018 | Model stacking ağırlıkları |
| **Kruschke** *AMPPS* "Rejecting/accepting parameters" | 2018 | ROPE çerçevesi (89% HDI + ROPE %) |
| **Wagenmakers** *Psychon Bull Rev* "Solution to p-values" | 2007 | BF Jeffreys sınıflama tablosu |
| **van den Bergh et al.** *Psychon Bull Rev* "BF prior sensitivity" | 2020 | BF için 3 prior width sensitivity |
| **Gelman, Hill & Vehtari** *Regression and Other Stories* (Cambridge) | 2021 | Bayesian regresyon felsefe + pratik |
| **McElreath** *Statistical Rethinking* (2nd, CRC) | 2020 | Bayesian preflight + DAG entegrasyonu |
| **Merkle & Rosseel** *J Stat Software* "blavaan" | 2018 | Bayesian SEM (H4 alternatif) |

### Karma yöntem (KISIM XIII)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Braun & Clarke** *Thematic Analysis: A Practical Guide* (SAGE) | 2022 | RTA 6-faz protokol — saturation kullanılmaz |
| **Creswell & Plano Clark** *Designing Mixed Methods Research* (3rd, SAGE) | 2018 | Convergent parallel design + joint display |
| **Gwet** *Handbook of Inter-Rater Reliability* (4th, AAL) | 2014 | Gwet AC1 — Cohen's κ alternatifi |
| **Wisdom & Creswell** *AHRQ Publication* "Mixed methods" | 2013 | Mixed methods reporting standards |
| **Edmondson** *Admin Sci Q.* "Healthcare contact bias" | 1996 | Anne sosyal istenirlik kompansasyonu yorumu |

### Açık bilim ve raporlama (KISIM XIV)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Wilkinson et al.** *Scientific Data* "FAIR principles" | 2016 | OSF + Zenodo + GitHub açık bilim mimarisi |
| **Nosek, Ebersole, DeHaven & Mellor** *PNAS* "Preregistration revolution" | 2018 | OSF reflective + secondary data hibrit |
| **Marwick et al.** *SAA Archaeological Record* "Open science" | 2018 | Üç katmanlı reprodüktiblik (renv + Docker) |
| **von Elm et al.** *PLoS Medicine* "STROBE statement" | 2008 | Gözlemsel çalışma raporlama |
| **APA** *Publication Manual* (7th ed.) | 2020 | APA 7 formatı zorunlu |
| **JARS-Mixed (APA)** *American Psychologist* "Mixed methods reporting" | 2018 | Karma yöntem paragraf yapısı |

### T1DM-spesifik pediatrik literatür

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Pinquart** *J Pediatr Psychol.* "Parenting in chronic illness families" | 2013 | Meta-analiz priorlama (d ≈ 0.40, %95 CI [0.25, 0.55]) → SESOI ±0.30 |
| **Streisand & Monaghan** *Curr Diabetes Rep* "Young children with T1DM" | 2014 | Anne savunmacılığı + sosyal istenirlik kompansasyonu hipotezi |
| **Anderson** *Diabetes Care* "Parenting practices in T1DM" | 2011 | Klinik yönetim ↔ parenting tutum |
| **Whittemore et al.** *Diabetes Educator* "Parents of T1DM children" | 2012 | Tükenmişlik + maternal mental health |
| **Demirbilek et al.** *Pediatric Diabetes* "Glycemic control in Turkey" | 2020 | Türk T1DM normu, HbA1c eşikleri |
| **ISPAD Clinical Practice Guidelines** | 2022 | HbA1c hedef ≤7.5 (pediatrik) |

### Sibling ve aile sistemleri

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Furman & Buhrmester** *Child Development* "Sibling Relationships Quest." | 1985 | KİA / SRQ orijinal ölçek |
| **McHale, Updegraff & Whiteman** *Annual Rev Psychol* "Sibling influences" | 2012 | Differential Parental Treatment teorik temel |
| **Brody** *Annual Rev Psychol* "Sibling relationship quality" | 1998 | Kardeş ilişkisi yapısı |
| **Buist, Deković & Prinzie** *Clinical Psychol Rev* "Sibling psychopathology" | 2013 | Sibling outcome ile psikopatoloji |

### Türk adaptasyon (kanonik)

| Kaynak | Yıl | Projede Kullanım |
|---|---|---|
| **Sümer, Selçuk & Günaydın** *Türk Psikoloji Yazıları* | 2006 | EMBU-P Türkçe adaptasyonu |
| **Sümer, Gündoğdu-Aktürk & Helvacı** *Türk Psikoloji Yazıları* | 2010 | Anne-baba tutumları Türk normu |
| **Apalaçi** M.Sc. Boğaziçi Üniv. | 1996 | KİA Türkçe adaptasyonu |
| **Hisli** *Psikoloji Dergisi* | 1989 | Beck Depresyon Türk geçerlik (≥17 orta) |

---

## Hızlı Eşleme — KISIM × Birincil Kaynak

| KISIM | Birincil kaynak (1) | Birincil kaynak (2) |
|---|---|---|
| V H1 | Hox (multilevel) | Bürkner (brms) |
| V H2 | Kenny (APIM) | Olsen-Kenny (dyadic CFA) |
| V H3 | Robins (IPTW) | Stuart (matching) |
| V H4 | Brown (CFA) | Kline (SEM) |
| **V H5** | **Olsen-Kenny + Edwards-Parry** | **Kenny (k-coef)** |
| VI | Hayes | VanderWeele |
| VII | Lanza-Cooper | Eid (Bifactor S-1) |
| VIII | Borsboom | Epskamp |
| IX | Vickers-Elkin | Pencina |
| X | ISPAD + Demirbilek | (klinik literatür) |
| XI | Steegen + Simonsohn | Cinelli-Hazlett + Lakens |
| XII | Bürkner | Yao (stacking) |
| XIII | Braun-Clarke 2022 | Creswell-Plano Clark |
| XIV | APA 7 | Wilkinson (FAIR) |
| XV (devstats) | Gelman-Loken | (her tehlike için ayrı) |
| XVI risk | (proje-içi tablo) | — |
| XVII timeline | (proje-içi tablo) | — |
