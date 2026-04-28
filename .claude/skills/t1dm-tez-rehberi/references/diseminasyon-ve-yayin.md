# KISIM XIV — Raporlama, Diseminasyon ve Yayın

> SAP v3.0 §42–45. papaja Quarto template + APA otomatik paragraf üretimi + Tez bölüm eşlemesi
> + 3-makale yayın stratejisi + FAIR/Zenodo açık veri planı.

## 1. papaja + apaquarto Tablo Üretimi

```r
library(papaja)

apa_table_h1 <- papaja::apa_table(
  h1_results_summary,
  caption = "Çocuk Algılanan Ebeveynlik Tutumu: Multilevel ANCOVA Sonuçları",
  note = "DM_Hasta_Indeks (n=120), DM_Hasta_Kardes (n=120), Kontrol_Indeks (n=121), Kontrol_Kardes (n=121). Multilevel: random = (1|aile_no). Kovaryatlar: yaş, cinsiyet, SES latent, age gap. p_FDR: Benjamini-Hochberg düzeltmesi (q=.05).",
  align = c("l", rep("c", 8)),
  font_size = "footnotesize",
  escape = TRUE
)
```

> **papaja vs apaquarto vs gtsummary:** Tezde Quarto + apaquarto kullanılır (PDF/DOCX/HTML triple-format).
> papaja R Markdown odaklı; apaquarto Quarto için modern alternatif.

## 2. Şekil Üretim Kataloğu (22 şekil)

| # | Şekil | Paket | Format |
|---|---|---|---|
| 1 | CONSORT-Mixed flow | consort | PNG + SVG |
| 2 | DAG (causal structure) | ggdag | PNG + SVG |
| 3 | SMD plot (denge görsel) | tableone | PNG |
| 4 | Propensity score overlap | ggplot2 | PNG + PDF |
| 5 | SES kompozit korelasyon matrisi | corrplot | PNG |
| 6 | H1 forest plot (etki büyüklükleri) | see::plot_estimate | PNG + PDF |
| 7 | H1 ext.: 3-way interaction simple slopes | emmeans + ggplot2 | PNG |
| 8 | H2: APIM path diagram | semPlot | PDF (vektör) |
| 9 | H3: stratified forest (3 strata) | metafor::forest | PNG |
| 10 | H4 SEM: tam path diagram | semPlot | PDF (vektör) |
| 11 | H5: Bland-Altman | BlandAltmanLeh | PNG |
| 12 | H5: RSA yüzey | RSA::plotRSA | PDF (3D) |
| 13 | Mediation: indirect effects bootstrap dist | ggplot2 | PNG |
| 14 | LPA: 4-profile spider plot | ggplot2 | PNG + PDF |
| 15 | Network: spring layout + edge widths | qgraph | PDF |
| 16 | Network comparison test | NCT plot | PNG |
| 17 | Decision tree visualization | rpart.plot | PDF |
| 18 | Specification curve | specr::plot_specs | PDF (geniş) |
| 19 | Sensemakr contour | sensemakr | PNG |
| 20 | Calibration plot + ROC + DCA | rmda + pROC | PNG |
| 21 | Posterior predictive check | bayesplot::pp_check | PNG |
| 22 | Bayesian forest (probabilities) | tidybayes | PNG |

## 3. Quarto Final Rapor Şablonu

```yaml
# reports/00_main_analysis.qmd
---
title: "T1DM Aileleri Ebeveyn Tutumu Çalışması — Final Analiz Raporu"
subtitle: "Marmara Üniversitesi SBE Sosyal Pediatri Doktora Tezi"
author:
  - name: "Özlem Murzoğlu Kurt"
    affiliation: "Marmara Üniversitesi SBE Sosyal Pediatri"
    email: "ozlem.murzoglu@gmail.com"
  - name: "Eren Özek"
    affiliation: "Marmara Üniversitesi Tıp Fakültesi, Neonatoloji"
date: today
abstract: |
  **Amaç:** ...
  **Yöntem:** ...
  **Bulgular:** ...
  **Sonuç:** ...
keywords: [Tip 1 Diyabet, Ebeveynlik Tutumu, Kardeş İlişkileri, EMBU, SRQ,
           Beck Depresyon, Multilevel Analysis, Mixed Methods]
format:
  apaquarto-html:
    toc: true
    toc-depth: 4
    number-sections: true
    fig-format: svg
  apaquarto-docx:
    toc: true
    fig-format: png
  apaquarto-pdf:
    keep-tex: true
    fig-format: pdf
bibliography: references.bib
csl: apa-7th-edition.csl
lang: tr
execute:
  echo: false
  message: false
  warning: false
  cache: true
---
```

## 4. Otomatik APA Paragraf Üretimi

```r
library(report)

# H1 için
h1_para <- function(result, subscale) {
  anova_role <- result$anova["role_f", ]

  sprintf(
    paste0("Çocukların algıladıkları ebeveynlik tutumu %s alt ölçeğinde, ",
           "rol grupları (Kontrol-Indeks, Kontrol-Kardeş, DM-Indeks, DM-Kardeş) ",
           "arasında istatistiksel olarak %s grup farkı gözlenmiştir, ",
           "F(%.0f, %.1f) = %.2f, p %s, p_FDR = %.3f, ",
           "ICC_aile = %.3f, R²_marjinal = %.3f, R²_koşullu = %.3f. ",
           "Tukey-düzeltmeli ikili karşılaştırmalarda en güçlü fark ",
           "DM-Indeks ile Kontrol-Indeks arasında bulunmuştur (Cohen's d = %.2f, 95%% CI [%.2f, %.2f])."),
    subscale,
    ifelse(anova_role$`Pr(>F)` < 0.05, "anlamlı", "anlamsız"),
    anova_role$NumDF, anova_role$DenDF, anova_role$`F value`,
    ifelse(anova_role$`Pr(>F)` < .001, "< .001",
            sprintf("= %.3f", anova_role$`Pr(>F)`)),
    result$p_fdr,
    result$icc$ICC_adjusted,
    result$r2$R2_marginal, result$r2$R2_conditional,
    result$cohens_d_dm_idx_vs_kontrol_idx$d,
    result$cohens_d_dm_idx_vs_kontrol_idx$ci_lo,
    result$cohens_d_dm_idx_vs_kontrol_idx$ci_hi
  )
}
```

> **Otomatik paragraf uyarısı:** `report::report()` İngilizce çıktı verir; tezde Türkçe APA için
> elden çevrilir veya bu projede yazılmış özel `t1dm_report_*` fonksiyonları kullanılır.

## 5. Tez Bölüm Eşlemesi (Master Mapping)

| Tez Bölümü (öneri) | Kaynak | Tablo/Şekil |
|---|---|---|
| **3. BULGULAR** | | |
| 3.1 Sosyodemografik | `R/13_table1_smd.R` | Tablo 1a, 1b, 1c |
| 3.2 Aile-içi nesting | `R/multilevel_icc.R` | Tablo 2 |
| 3.3 Denge testi + propensity | `R/13` + `R/15` | Tablo 3, Şekil 4 |
| 3.4 SES kompozit | `R/11_ses_composites.R` | Tablo 4, Şekil 5 |
| 3.5 Ölçek psikometrisi | (validasyon raporu) | Ek A |
| 3.6 H1 — Çocuk algı | `R/16` + ext + irt + bayes | Tablo 5, Şekil 6, 7, 22 |
| 3.7 H2 — Kardeş ilişkisi | `R/17` + apim + dyadic | Tablo 6, Şekil 8 |
| 3.8 H3 — Anne öz-rapor | `R/18` + strat + iptw | Tablo 7, Şekil 9 |
| 3.9 H4 — Beck → EMBU-P | `R/19` + invariance + bayes | Tablo 8, Şekil 10 |
| 3.10 H5 — Diadik tutarlılık | `R/h5_*` | Tablo 9, Şekil 11, 12 |
| 3.11 Mediation | `R/mediation_*` | Tablo 10, Şekil 13 |
| 3.12 LPA — anne tipoloji | `R/latent_*` | Tablo 11, Şekil 14 |
| 3.13 Network | `R/network_*` | Tablo 12, Şekil 15, 16 |
| 3.14 Klinik fayda | `R/clinical_utility_*` | Tablo 13, Şekil 17, 20 |
| 3.15 DM klinik alt-analiz | `R/dm_clinical_*` | Tablo 14, 15 |
| 3.16 Robustness | `R/robustness_*` | Tablo 16, Şekil 18, 19 |
| 3.17 Bayesian doğrulama | `R/bayes_*` | Tablo 17, Şekil 21, 22 |
| 3.18 Niteliksel + joint display | `R/qualitative_*` | Tablo 18 |
| **4. TARTIŞMA** | (yorum) | (matrix raporu) |
| **5. SONUÇ** | (yorum) | — |
| **EKLER** | | |
| Ek A. Psikometrik validasyon | (ayrı doküman) | — |
| Ek B. Pre-registration | OSF GUID/DOI | — |
| Ek C. R session info | session_info.txt | — |
| Ek D. _targets.R orkestrasyonu | _targets.R | — |
| Ek E. Niteliksel kodlama kitabı | codebook.csv | — |

## 6. Yayın Stratejisi (3-Makale Planı)

### Makale 1 — Birincil Bulgu (En Yüksek Etki)

**Hedef dergi:** *Pediatric Diabetes* (IF ≈ 4.5) veya *Journal of Pediatric Psychology* (IF ≈ 3.5)

**Başlık önerisi:** "Differential Parental Treatment Perceptions in Type 1 Diabetes Families:
A Case-Control Mixed-Methods Study from Turkey"

**Odak:** H1 + H5 (çocuk algısı + anne-çocuk diadik tutarsızlık)

**Anahtar bulgular:**
- T1DM ailelerinde anne-çocuk Reddetme algı tutarsızlığı
- Differential Parental Treatment (PDT) ampirik kanıtı (kardeş ICC ≈ .16-.30)
- Joint display: nicel + niteliksel convergence

### Makale 2 — Maternal Ruh Sağlığı

**Hedef dergi:** *Diabetic Medicine* (IF ≈ 3.7) veya *Journal of Family Psychology* (IF ≈ 4.0)

**Başlık önerisi:** "Maternal Mental Health Burden in Pediatric Type 1 Diabetes: Antidepressant
Use, Depressive Symptoms, and Parenting Style Impact"

**Odak:** H3 + H4 + Mediation
- Anne antidepresan kullanımı 3.21x yüksek (DM 29% vs Kontrol 9%)
- Beck → EMBU-P → çocuk algısı mediation yolu
- LPA: "Tükenmiş anne" profili DM-yoğunluk

### Makale 3 — Metodolojik Katkı

**Hedef dergi:** *Methods in Psychology* (IF ≈ 2.5) veya *Frontiers in Psychology — Quantitative*

**Başlık önerisi:** "Polychoric BSEM Validation of the Turkish s-EMBU Parent Form: Addressing
Floor Effects and Skewed Items in Family Research"

**Odak:** Psikometrik validasyon raporu
- Floor effect karşı BSEM yaklaşık-sıfır prior çözümü
- Multiverse + TOST eşdeğerlik testi metodolojik gösterim
- Türk normu için EMBU-P yenilenmiş psikometrik model

## 7. FAIR İlkeleri

| FAIR İlkesi | Uygulama |
|---|---|
| **Findable** | OSF GUID/DOI + Zenodo arşivi + ORCID linkleri |
| **Accessible** | Kod açık (Apache 2.0); ham veri controlled access (KVKK) |
| **Interoperable** | CSV (UTF-8) + R/Quarto + Standard ölçek formatları |
| **Reusable** | Detaylı README + DataDictionary + License (CC-BY 4.0 metadata) |

## 8. OSF Proje Yapısı

```
OSF Project: T1DM-EBEVEYN_v1.0 (https://osf.io/vqrt5/)
├── Pre-registration/
│   ├── 01_psychometric_reflective_registration.pdf
│   └── 02_secondary_data_analysis_preregistration_form.pdf
├── Materials/
│   ├── FINAL_REFERENCE_VERI_HARITASI.md
│   ├── KANONIK_DEMOGRAFIK_VE_TIBBI_BILGILER.md
│   ├── KANONIK_KISALTILMIS_EMBU_EBEVEYN.md
│   ├── KANONIK_KISALTILMIS_EMBU_COCUK.md
│   ├── KANONIK_BECK_DEPRESYON_ENVANTERI.md
│   ├── KANONIK_KARDES_ILISKILERI_ANKETI.md
│   └── KLINIK_CALISMA_PROTOKOLU.md
├── Code/
│   ├── _targets.R, R/, scripts/R/, tests/, chapters/
│   ├── renv.lock, _quarto.yml, thesis.qmd
├── Data/                              ← KVKK kontrollü
│   ├── README_controlled_access.md
│   └── FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock
├── Outputs/
├── Reports/
│   ├── STATISTICAL-ANALYSIS-PLAN.md
│   ├── OSF-KAYIT-REHBERI.md
│   └── pre_registration_deviation_table_template.md
├── README.md
├── manifest_sha256.txt
└── T1DM-EBEVEYN_v1.0_OSF_package.zip
```

## 9. Zenodo Arşivleme

```bash
# Tezin kabulü sonrası
zenodo-cli upload \
  --title "T1DM-EBEVEYN: Analiz kodu ve metodoloji v3.0" \
  --description "..." \
  --keywords "t1dm,parenting,sibling,multilevel,bayesian" \
  --license "Apache-2.0" \
  --community "open-science-framework" \
  Code/

# DOI atanır → Tez Ek D'ye eklenir
```

## 10. GitHub Repository

```
github.com/ozlemmurzoglu/t1dm-ebeveyn-analysis
├── README.md (badges: OSF, Zenodo DOI, build status)
├── CITATION.cff
├── LICENSE (Apache 2.0)
├── docs/
│   ├── methodology.md
│   ├── reproducibility.md
│   └── changelog.md
└── (tüm analiz kodu)
```

## Tedbir denetimi

- [ ] Quarto YAML `lang: tr` (Türkçe sıralama, hyphenation)
- [ ] apaquarto + bibliography + apa-7th-edition.csl yapılandırıldı
- [ ] Şekil formatı double-output (PNG + PDF/SVG)
- [ ] Tablo notları kovaryat listesi + p düzeltme yöntemi içeriyor
- [ ] Ham veri CSV'leri OSF'ye **yüklenmiyor**; sadece kod + processed lock
- [ ] CITATION.cff güncel (DOI/ORCID)
- [ ] Renv.lock commit'lendi (reprodüksiyon için)
- [ ] Thesis bölüm eşlemesi 18 alt-bölüm tam mapping
- [ ] 3-makale planı tezde Bölüm 6 olarak listelendi
- [ ] Otomatik APA paragraflar elden Türkçeye uyarlandı

## Çapraz referanslar

- Tezin Quarto YAML detayı → [`tez-yazim-rehberi.md`](tez-yazim-rehberi.md)
- Türkçe APA paragraf şablonları → [`raporlama-sablonlari.md`](raporlama-sablonlari.md)
- OSF kayıt akışı → [`pipeline-mimarisi.md`](pipeline-mimarisi.md)
- Kaynaklar: APA (2020); Wilkinson et al. (2016); Marwick et al. (2018); Nosek et al. (2018)
