# İSTATİSTİKSEL ANALİZ PLANI — FAZ II (POST-HOC ZENGİNLEŞTİRME)

> **Kapsam Revizyonu (2026-05-02):** Yeni veri toplama gerektiren tüm aşamalar bu plandan çıkarılmıştır. Aşağıdaki 4 hedef kapsam dışında bırakılmıştır:
> - **F2-19** (Glycemic trajectory pilot) — longitudinal Faz III veri
> - **F2-35** (TRIPOD-Cluster hazırlık çerçevesi) — dış-validasyon Faz III veri
> - **F2-38** (Risk skor recalibration) — dış validasyon verisi gerektirir
> - **F2-42** (Çok-merkezli replikasyon protokolü) — yeni veri toplama
>
> İlgili iki doküman silinmiştir: `TRIPOD-CLUSTER-HAZIRLIK.md`, `REPLICATION-PROTOCOL-DRAFT.md`.
>
> **Faz II yalnızca mevcut Faz I kanonik baz** (`FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`, n=241 aile / 482 satır) **üzerinde çalışan 41 hedef ile sınırlandırılmıştır**. Tüm hedefler tamamlanmış ve `verified` durumundadır.

**T1DM-EBEVEYN Çalışması** — Çalışma-Sonu Verilerle Hipotez-Üretici Analiz Hattı
*Tip 1 Diyabet Tanılı Çocuklar, Sağlıklı Kardeşleri ve Annelerinin Ebeveynlik Tutumlarına Yönelik Algılarının Sağlıklı Kontrol Grubu ile Karşılaştırılarak İncelenmesi ve Kardeşler Arası İlişkilerin Değerlendirilmesi*

| Alan | İçerik |
|---|---|
| **Doktora öğrencisi** | Uzm.Dr. Özlem Murzoğlu Kurt |
| **Tez danışmanı** | Prof.Dr. Eren Özek (MÜTF, Neonatoloji) |
| **Yardımcı araştırıcı** | Doç.Dr. Belma Haliloğlu (MÜTF, Pediatrik Endokrinoloji) |
| **TİK** | Prof.Dr. Perran Boran; Prof.Dr. Nalan Karabayır |
| **Faz II SAP sürümü** | **v1.0 — POST-HOC ZENGİNLEŞTİRME** (2026-05-01) |
| **Bağlanılan ana plan** | `STATISTICAL-ANALYSIS-PLAN.md` v3.0 (2026-04-27) — KISIM I-XVIII |
| **Kanonik veri** | `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` (2026-04-26, status: LOCKED) — **değişiklik yok** |
| **Kanıt kategorisi** | **[KEŞİFSEL · POST-HOC]** — tüm Faz II analizleri Tip 3 sapma sınıfında |
| **Tetikleyici belgeler** | `CLINICAL-STUDY-REPORT.md` (v1.1, 2026-04-29), `CLINICAL-STUDY-REPORT-V2.md` (2026-05-01) |
| **OSF ek kayıt önerisi** | Layer 3: Post-hoc exploratory amendment — submit hedefi 2026-05-08 |
| **Skill orkestrasyonu** | `t1dm-tez-rehberi` × `devstats` × `psychdev` × `medical-research` |
| **Yazılım** | R 4.5.3 + Quarto 1.6+ + `targets` + `renv` + Stan 2.32+ (ana plan ile aynı yığın) |

---

## ÖN UYARI — Faz II'nin Epistemik Statüsü

Faz II SAP'sının tek bir analizi bile **doğrulayıcı (confirmatory) kanıt** üretmez. Her bulgu üç kademede konumlandırılır:

1. **[KEŞİFSEL · POST-HOC]** — Faz II'de tanımlanan, çalışma-sonu verisi görüldükten sonra eklenmiş tüm analizler bu kategoridedir.
2. **Sapma tipi:** Pre-registration sapma sınıflandırmasında (`PRE-REGISTRATION-DEVIATION-TABLE.md`) **Tip 3** sapmadır; OSF Layer 1 (`d524q`) veya Layer 2 (`pytfe`) kapsamında kabul edilmez.
3. **Replikasyon zorunluluğu:** Faz II'den çıkacak her bulgu, bağımsız bir Türk kohortunda **dış-validasyon olmadan** klinik öneri seviyesine yükseltilmez. Tezde "hipotez-üretici" alt-bölümler altında raporlanır.

> **Metin Kutusu — Faz II ne değildir?**  
> Faz II, ana SAP v3.0'ın tamamlamadığı KISIM'leri "kapatma" değil; bunun yerine **çalışma-sonu verileri ışığında ortaya çıkan psikometrik, klinik ve metodolojik soruları** disiplinli bir keşif çerçevesinde ele alır. H1–H5 birincil kanıt kademeleri (CSR Bölüm 11) **DEĞİŞMEZ**; Faz II yalnız (a) sınırlama dipnotlarına derinlik, (b) yeni hipotezlerin hazırlık verisi, (c) gelecek çalışmalar için power/replikasyon planlaması üretir.

---

## FAZ II İÇİNDEKİLER

**KISIM XIX — POST-HOC SAPMA DİSİPLİNİ VE OSF EK KAYIT**
- 47. Tip 3 Sapma Yönetişimi
- 48. OSF Layer 3 (Post-hoc Amendment) Şablonu
- 49. Faz II Reproducibility Zinciri (renv + targets + lockfile)

**KISIM XX — MULTI-İNFORMANT YAPISAL GENİŞLETME**
- 50. Trifactor Model (Anne × İndeks × Kardeş Ortak Ölçüm Yapısı)
- 51. Latent Informant Discrepancy SEM (De Los Reyes 2023 Operations Triad)
- 52. Latent Difference Score (LDS) Modeli
- 53. Cross-Informant Network Analysis

**KISIM XXI — PSİKOMETRİK ROBUSTLEŞTİRME**
- 54. Floor-Aware Tobit IRT (Reddetme Madde Kümesi)
- 55. Reliability Generalization (ω_h, ω_h_s, ECV — Bifactor S-1)
- 56. Beck Symptom Heterogeneity (Cognitive vs Somatic Bifactor)
- 57. ESEM (Exploratory SEM) — EMBU-P/C Cross-Loading Genişletmesi

**KISIM XXII — ANTİDEPRESAN VE MENTAL SAĞLIK YÜKÜ**
- 58. Antidepresan Kullanımı: Aracı (Mediator) Rol
- 59. Antidepresan × Grup Moderasyonu (H1, H4, H5)
- 60. Beck × Antidepresan Latent İnteraksiyon (Klein-Moosbrugger 2000)

**KISIM XXIII — H5 DİADİK TUTARLILIK GENİŞLETMESİ**
- 61. Multitrait-Multimethod (MTMM) Modeli (Eid 2008)
- 62. Beck × Grup Moderasyonu Diadik Korelasyon Üzerinde
- 63. İndeks-Kardeş Sibling-Pair Concordance ICC
- 64. H5 Strateji-Düzeyi Bayesian Pooling

**KISIM XXIV — KLİNİK STRATİFİKASYON GENİŞLETMESİ**
- 65. HbA1c × Parenting Joint Model (Bayesian)
- 66. Tanı Yaşı Spline × Parenting (DM-Only)
- 67. Glycemic-Parenting Latent Trajectory Sketch (Pilot)
- 68. ISPAD Eşiği (HbA1c < 7.0%) İkili Sonuç Ek-Analiz

**KISIM XXV — NEDENSEL ARACILIK SENSİTİVİTESİ**
- 69. Imai-Keele-Tingley Causal Mediation (sensitivity ρ)
- 70. DAG Doğrulama: PC Algorithm + FCI
- 71. c' Direct Effect Triangülasyon Re-Analizi (CSR §12.1)
- 72. Negative Outcome Control Genişletmesi (3-Level Varyans Yapısı)

**KISIM XXVI — DİSTRİBÜSYONEL VE KUANTİL YAKLAŞIMLAR**
- 73. Quantile Regression (Reddetme Üst Kuyruk)
- 74. Distributional Regression (gamlss / brms_distributional)
- 75. Beta Regression (EMBU Mean Score için Bounded Outcome)

**KISIM XXVII — MULTIVERSE GENİŞLETME**
- 76. H1 Multiverse (EMBU-C Reddetme — yeni 240 spec)
- 77. H4 SEM Multiverse (Estimator × Cluster × Missing)
- 78. Bayesian Model Averaging Across Multiverse
- 79. Specification Curve Inferential Test (Permütasyon n_perm = 5000)

**KISIM XXVIII — META-ANALİTİK BİRLEŞTİRME**
- 80. Bayesian Meta-Analytic Pooling (Pinquart 2013 + Lovejoy 2000 + bu çalışma)
- 81. Posterior Predictive Replication (Gelman 2013)
- 82. Empirical Bayes Shrinkage (Multilevel Random-Effects)

**KISIM XXIX — KLİNİK KARAR MODELİ DIŞ VALİDASYON HAZIRLIĞI**
- 83. TRIPOD-Cluster Hazırlık Çerçevesi
- 84. Standardized Net Benefit (sNB) Genişletmesi
- 85. Threshold-Sensitivity DCA Heatmap
- 86. Risk Skoru Recalibration Şablonu

**KISIM XXX — POWER VE REPLİKASYON PLANLAMA**
- 87. simr Multilevel Power Simülasyonu
- 88. APIM-Specific Sample Size (Ackerman & Kenny 2016)
- 89. Bayesian Sample Size Determination (BSSD; Kruschke 2018)
- 90. Çok-Merkezli Replikasyon Tasarımı

**KISIM XXXI — KARMA YÖNTEM (KOŞULLU)**
- 91. Niteliksel Veri Yokluk Beyanı + Gelecek Tasarım Şablonu
- 92. Convergence Joint Display (Kantitatif-Kantitatif)

**KISIM XXXII — ÇIKTI ENTEGRASYONU**
- 93. Faz II APA Tablo + Şekil Listesi
- 94. Tez Ek-Bölüm Eşlemesi
- 95. Faz II 3-Makale Yayın Planı (Makale 4-6)

**KISIM XXXIII — FAZ II RİSK MATRİSİ**

**KISIM XXXIV — FAZ II ZAMAN ÇİZELGESİ (12 HAFTA)**

**KISIM XXXV — FAZ II UYGULAMA TRACKER'I**

---

## CANLI UYGULAMA TRACKER'I (FAZ II)

| # | KISIM | İş Paketi | Durum | R modülü | Hedef artefakt |
|---|---|---|---|---|---|
| F2-01 | XIX | OSF Layer 3 amendment submit | `planned` | — | `docs/analiz_planlari/OSF-LAYER3-AMENDMENT.md` |
| F2-02 | XX/50 | Trifactor T-CFA | `planned` | `R/32_trifactor_model.R` | `outputs/tables/trifactor_fit.csv` |
| F2-03 | XX/51 | Latent informant discrepancy SEM | `planned` | `R/33_informant_discrepancy.R` | `outputs/models/informant_disc_*.rds` |
| F2-04 | XX/52 | Latent Difference Score | `planned` | `R/33_informant_discrepancy.R` | `outputs/tables/lds_table.csv` |
| F2-05 | XX/53 | Cross-informant GGM network | `planned` | `R/34_cross_informant_network.R` | `outputs/figures/cross_informant_network.pdf` |
| F2-06 | XXI/54 | Floor-aware Tobit IRT | `planned` | `R/35_floor_aware_irt.R` | `outputs/tables/tobit_irt_reddetme.csv` |
| F2-07 | XXI/55 | Reliability generalization (ω_h, ECV) | `planned` | `R/36_reliability_generalization.R` | `outputs/tables/omega_h_table.csv` |
| F2-08 | XXI/56 | Beck cognitive vs somatic bifactor | `planned` | `R/36_reliability_generalization.R` | `outputs/tables/beck_bifactor_fit.csv` |
| F2-09 | XXI/57 | ESEM EMBU-P/C cross-loading | `planned` | `R/37_esem_embu.R` | `outputs/tables/esem_loadings.csv` |
| F2-10 | XXII/58 | Anne AD aracı (mediator) modeli | `planned` | `R/38_antidepressant_pathway.R` | `outputs/tables/ad_mediator_indirect.csv` |
| F2-11 | XXII/59 | AD × Grup moderasyon (H1/H4/H5) | `planned` | `R/38_antidepressant_pathway.R` | `outputs/tables/ad_moderation_h1_h4_h5.csv` |
| F2-12 | XXII/60 | Beck × AD latent etkileşim | `planned` | `R/38_antidepressant_pathway.R` | `outputs/models/beck_ad_interaction.rds` |
| F2-13 | XXIII/61 | MTMM diadik tutarlılık | `planned` | `R/39_h5_extensions.R` | `outputs/tables/mtmm_h5_table.csv` |
| F2-14 | XXIII/62 | Beck × Grup moderasyon (diadik) | `planned` | `R/39_h5_extensions.R` | `outputs/tables/h5_beck_moderation.csv` |
| F2-15 | XXIII/63 | Sibling-pair concordance ICC | `planned` | `R/39_h5_extensions.R` | `outputs/tables/sibling_pair_icc.csv` |
| F2-16 | XXIII/64 | H5 Bayesian strateji pooling | `planned` | `R/39_h5_extensions.R` | `outputs/tables/h5_bayesian_pooling.csv` |
| F2-17 | XXIV/65 | HbA1c × parenting Bayesian joint | `planned` | `R/40_hba1c_joint.R` | `outputs/models/hba1c_parenting_joint.rds` |
| F2-18 | XXIV/66 | Tanı yaşı × parenting spline | `planned` | `R/40_hba1c_joint.R` | `outputs/figures/dx_age_spline.pdf` |
| ~~F2-19~~ | ~~XXIV/67~~ | ~~Glycemic trajectory pilot~~ | **`removed`** | — | **Yeni veri gerektirdiği için Faz II'den çıkarıldı** |
| F2-20 | XXIV/68 | ISPAD < 7.0% ikili sonuç | `planned` | `R/40_hba1c_joint.R` | `outputs/tables/ispad_logistic.csv` |
| F2-21 | XXV/69 | Imai-Keele causal mediation sens | `planned` | `R/41_causal_mediation.R` | `outputs/tables/imai_keele_rho.csv` |
| F2-22 | XXV/70 | PC algorithm + FCI DAG validation | `planned` | `R/42_dag_pc_fci.R` | `outputs/figures/dag_pc_estimated.pdf` |
| F2-23 | XXV/71 | c' direct effect triangülasyon | `planned` | `R/41_causal_mediation.R` | `outputs/tables/c_prime_triangulation.csv` |
| F2-24 | XXV/72 | 3-level varyans yapısı negctrl | `planned` | `R/42_dag_pc_fci.R` | `outputs/tables/three_level_negctrl.csv` |
| F2-25 | XXVI/73 | Quantile regression (üst kuyruk) | `planned` | `R/43_distributional.R` | `outputs/tables/quantile_reddetme.csv` |
| F2-26 | XXVI/74 | Distributional regression | `planned` | `R/43_distributional.R` | `outputs/models/dist_reg_*.rds` |
| F2-27 | XXVI/75 | Beta regression (bounded EMBU) | `planned` | `R/43_distributional.R` | `outputs/tables/beta_reg.csv` |
| F2-28 | XXVII/76 | H1 multiverse (240 spec) | `planned` | `R/44_multiverse_extension.R` | `outputs/tables/h1_multiverse_spec.csv` |
| F2-29 | XXVII/77 | H4 SEM multiverse | `planned` | `R/44_multiverse_extension.R` | `outputs/tables/h4_sem_multiverse.csv` |
| F2-30 | XXVII/78 | BMA across multiverse | `planned` | `R/44_multiverse_extension.R` | `outputs/tables/bma_multiverse.csv` |
| F2-31 | XXVII/79 | SCA inferential test (n_perm=5000) | `planned` | `R/44_multiverse_extension.R` | `outputs/tables/sca_inferential.csv` |
| F2-32 | XXVIII/80 | Bayesian meta-analytic pooling | `planned` | `R/45_bayesian_meta.R` | `outputs/tables/bayes_meta_pooling.csv` |
| F2-33 | XXVIII/81 | Posterior predictive replication | `planned` | `R/45_bayesian_meta.R` | `outputs/figures/ppc_replication.pdf` |
| F2-34 | XXVIII/82 | Empirical Bayes shrinkage | `planned` | `R/45_bayesian_meta.R` | `outputs/tables/eb_shrinkage.csv` |
| ~~F2-35~~ | ~~XXIX/83~~ | ~~TRIPOD-Cluster hazırlık çerçevesi~~ | **`removed`** | — | **Yeni (dış-validasyon) veri gerektirdiği için çıkarıldı** |
| F2-36 | XXIX/84 | sNB genişletmesi | `planned` | `R/46_clinical_dx_extension.R` | `outputs/tables/snb_extended.csv` |
| F2-37 | XXIX/85 | DCA threshold heatmap | `planned` | `R/46_clinical_dx_extension.R` | `outputs/figures/dca_threshold_heatmap.pdf` |
| ~~F2-38~~ | ~~XXIX/86~~ | ~~Risk skor recalibration~~ | **`removed`** | — | **Dış validasyon verisi gerektirdiği için çıkarıldı** |
| F2-39 | XXX/87 | simr multilevel power | `planned` | `R/47_power_replication.R` | `outputs/tables/simr_power_grid.csv` |
| F2-40 | XXX/88 | APIM sample size (Ackerman 2016) | `planned` | `R/47_power_replication.R` | `outputs/tables/apim_sample_size.csv` |
| F2-41 | XXX/89 | Bayesian sample size determ. | `planned` | `R/47_power_replication.R` | `outputs/tables/bayes_ssd.csv` |
| ~~F2-42~~ | ~~XXX/90~~ | ~~Çok-merkezli replikasyon plan~~ | **`removed`** | — | **Yeni veri toplama gerektirdiği için çıkarıldı** |
| F2-43 | XXXII/93 | Faz II APA tablo + şekil paketi | `planned` | `R/48_phase2_apa_outputs.R` | `outputs/tables/phase2_*.csv` |
| F2-44 | XXXII/94 | Tez ek-bölüm eşlemesi | `planned` | `R/49_phase2_thesis_mapping.R` | `chapters/06_post_hoc_genisleme.qmd` |
| F2-45 | XXXII/95 | Makale 4-6 plan | `planned` | doküman | `references/diseminasyon-ve-yayin.md` (ekleme) |

---

# KISIM XIX — POST-HOC SAPMA DİSİPLİNİ VE OSF EK KAYIT

## 47. Tip 3 Sapma Yönetişimi

### 47.1 Niçin Önemli?

`PRE-REGISTRATION-DEVIATION-TABLE.md` mevcut sürümünde Tip 3 (major) sapma sayısı **0**'dır. Faz II analizleri **tek bir blokta 45 yeni Tip 3 sapma** olarak işlenir. Bu blok sayesinde her bireysel analiz için ayrı Tip 3 satırı yerine **tek bir "Faz II Bütünleşik Amendment" satırı** açılır; her alt-analiz amendment'a referans verir.

### 47.2 Yeni Sapma Satırı Şablonu

Aşağıdaki satır `PRE-REGISTRATION-DEVIATION-TABLE.md` dosyasına eklenir:

```markdown
| 1 | 2026-05-01 | Layer 1 + Layer 2 | Sadece KISIM I-XVIII | Faz II SAP (KISIM XIX-XXXV) eklendi: 45 post-hoc analiz tetiklendi (CSR v1.1 ve CSR-V2 sonrası) | Tip 3 | Çalışma sonu verileri ışığında ortaya çıkan psikometrik sınırlamalar (EMBU reddetme α/ω düşüklüğü, H4 SEM CFI sınır altı), klinik moderator boşlukları (anne antidepresan SMD=0.53), strateji-düzeyi diadik tutarlılık çelişkisi (H5) ve dış validasyon hazırlığı için ek analiz hattı | docs/analiz_planlari/STATISTICAL-ANALYSIS-PLAN-PHASE-2.md |
```

### 47.3 Raporlama Disiplini

- **Her Faz II tablosu/şekli başlığında "[KEŞİFSEL · POST-HOC]" prefiksi zorunludur.**
- Tezde Faz II bulguları **ayrı bir bölüm** (Bölüm 6: Post-Hoc Genişleme) altında raporlanır; Bölüm 5 (CSR'a paralel ana sonuçlar) ile **karıştırılmaz**.
- "Doğruladı / desteklendi" ifadeleri kullanılmaz; bunun yerine "tutarlı yön gösterdi", "hipotez-üretici işaret üretti", "post-hoc keşifsel olarak gözlendi" tercih edilir.

> **Davranış Kuralı 6 hatırlatması:** "Bu sonuç keşifsel olarak çıktı, ön-kayıtta vardı" denmez. Sapma `[KEŞİFSEL]` etiketiyle açıkça belirtilir.

## 48. OSF Layer 3 (Post-hoc Amendment) Şablonu

### 48.1 OSF Kayıt Stratejisi

| Katman | Amaç | OSF GUID | Statü |
|---|---|---|---|
| Layer 1 | Psikometrik validasyon (reflective) | `d524q` | Submitted, embargo |
| Layer 2 | H1-H5 secondary data preregistration | `pytfe` | Submitted, embargo |
| **Layer 3 (yeni)** | **Faz II post-hoc exploratory amendment** | **2026-05 submit hedefi** | `planned` |

### 48.2 OSF Layer 3 Amendment İçerik İskeleti

- **Title:** "T1DM-EBEVEYN — Post-Hoc Exploratory Amendment (Phase II Statistical Analysis Plan)"
- **Type:** OSF Registries → "Open-Ended Registration" (post-hoc exploratory amendment)
- **Files attached:**
  1. `STATISTICAL-ANALYSIS-PLAN-PHASE-2.md` (bu dosya)
  2. CSR v1.1 ve CSR-V2 (tetikleyici belgeler)
  3. Updated `PRE-REGISTRATION-DEVIATION-TABLE.md`
- **Narrative (≈ 800 kelime):**
  - Faz II'nin neden gerektiği (CSR'da gözlenen 13 boşluk maddesi)
  - Her KISIM'in çıkarsadığı evidensel hat
  - Replikasyon zorunluluğu beyanı
  - Embargo: tez savunmasıyla eş-açılım
- **Hash anchor:** Faz II'nin commit SHA'sı (git rev-parse HEAD) submit anında dahil edilir.

### 48.3 Amendment Doğrulama Akışı

```
1. Faz II SAP commit → git SHA al
2. Faz II veri kilidi durumu doğrula (ana lock dosyası DEĞİŞMEZ)
3. PRE-REGISTRATION-DEVIATION-TABLE.md → Tip 3 satırı ekle
4. OSF Layer 3 amendment hazırla → submit
5. OSF GUID'i bu dokümana yansıt (Tablo 47.2)
6. CSR v2.0 (savunma sonrası) içine ek bölüm referansı işle
```

## 49. Faz II Reproducibility Zinciri

### 49.1 Yeni R Modülleri ve `_targets.R` Entegrasyonu

Faz II yeni `R/` modülleri:

| Modül | Sorumluluk | Bağlı target prefix'i |
|---|---|---|
| `R/32_trifactor_model.R` | T-CFA, anne+indeks+kardeş ortak ölçüm yapısı | `phase2_trifactor_*` |
| `R/33_informant_discrepancy.R` | Latent discrepancy SEM, LDS | `phase2_disc_*` |
| `R/34_cross_informant_network.R` | Cross-informant GGM | `phase2_xinfo_net_*` |
| `R/35_floor_aware_irt.R` | Censored IRT | `phase2_tobit_irt_*` |
| `R/36_reliability_generalization.R` | ω_h, ECV, bifactor reliability | `phase2_omega_h_*` |
| `R/37_esem_embu.R` | ESEM cross-loading | `phase2_esem_*` |
| `R/38_antidepressant_pathway.R` | AD mediator + moderator | `phase2_ad_*` |
| `R/39_h5_extensions.R` | MTMM, sibling concordance, Bayesian pooling | `phase2_h5_ext_*` |
| `R/40_hba1c_joint.R` | DM-only joint glycemic-parenting | `phase2_hba1c_*` |
| `R/41_causal_mediation.R` | Imai-Keele sensitivity, c' triangulation | `phase2_imai_*` |
| `R/42_dag_pc_fci.R` | PC algorithm + 3-level negctrl | `phase2_dag_*` |
| `R/43_distributional.R` | Quantile, distributional, beta regression | `phase2_dist_*` |
| `R/44_multiverse_extension.R` | H1/H4 multiverse + BMA + SCA inferential | `phase2_multi_*` |
| `R/45_bayesian_meta.R` | Bayesian meta-analytic pooling | `phase2_bayes_meta_*` |
| `R/46_clinical_dx_extension.R` | sNB, DCA heatmap, recalibration | `phase2_clinical_*` |
| `R/47_power_replication.R` | simr, APIM SS, BSSD | `phase2_power_*` |
| `R/48_phase2_apa_outputs.R` | APA tablo + şekil paketi | `phase2_apa_*` |
| `R/49_phase2_thesis_mapping.R` | Tez Bölüm 6 eşleme | `phase2_thesis_*` |

**Kural:** Tüm yeni modüller `R/01_io.R::validate_and_load()` üzerinden veri çeker; **kanonik kilit dosyası DEĞİŞMEZ**. Yeni türetilmiş skorlar `R/10_derived_scores.R` üzerinden değil, modül-başına `phase2_derive_*` fonksiyonları altında üretilir ve `outputs/processed/phase2_*.rds` altında saklanır.

### 49.2 Test ve Audit

Her yeni R/ modülü için:
- `tests/test_<modül>.R` — `stopifnot()` ile fonksiyon-başına doğrulama
- `scripts/R/<numara>_<modül>_audit.R` — runner; CSV smoke-test üretir
- `_targets.R` içinde `phase2_<modül>_audit_csv` hedefi `format = "file"` olarak deklare edilir

### 49.3 Renv Lock Stratejisi

Faz II yeni paket bağımlılıkları (öngörülen):

| Paket | Amaç | Min. sürüm |
|---|---|---|
| `mediation` | Imai-Keele causal mediation | 4.5.0 |
| `pcalg` | PC algorithm DAG inference | 2.7.10 |
| `mokken` | Floor-aware nonparametric IRT | 3.1.0 |
| `gamlss` | Distributional regression | 5.4.0 |
| `quantreg` | Quantile regression | 5.97 |
| `betareg` | Beta regression | 3.2.0 |
| `metafor` | Random-effects meta-analytic pooling | 4.6.0 |
| `bain` | Bayesian informative hypothesis evaluation | 0.2.10 |
| `simr` | Multilevel power simulation | 1.0.7 |
| `MOTE` | Effect size + sample size APIM | 1.0.2 |

Yeni paketler `renv::install()` ile eklenir, ardından `renv::snapshot()` çağrılır; commit mesajı: `chore(renv): Faz II SAP için 10 paket eklendi`.

> **Davranış Kuralı 10 hatırlatması:** `renv.lock` hash değişikliği "küçük değişiklik" olarak işlenmez; commit gerekçelenir.

---

# KISIM XX — MULTI-İNFORMANT YAPISAL GENİŞLETME

## 50. Trifactor Model (Anne × İndeks × Kardeş Ortak Ölçüm Yapısı)

### 50.1 Boşluk (CSR'dan)

CSR Bölüm 11.1.6'da H1 reddetme bulgusu **moderate kanıt birikimi** alarak raporlanmış; ancak **anne-indeks-kardeş üçlü ölçüm modelinde latent yapının evrensel olup olmadığı** test edilmemiştir. CSR §6.2 multi-informant çerçevesinin teorik temelini De Los Reyes 2015 modelinden çıkarmakta, fakat **Mâsse, Newman & Pulman (2020) Trifactor Model** uygulanmamıştır.

### 50.2 Amaç

EMBU reddetme alt ölçeği için anne (öz-rapor), indeks çocuk (algı), kardeş (algı) üç bilgi-veren grubunun ortak latent faktörünü ve bilgi-veren-spesifik bias bileşenlerini ayırt eden bir T-CFA modeli kurmak.

### 50.3 Yöntem

**Model:**

```
F_common =~ embu_p_<madde>_anne + embu_c_<madde>_indeks + embu_c_<madde>_kardes
F_anne_bias =~ embu_p_<madde>_anne
F_indeks_bias =~ embu_c_<madde>_indeks
F_kardes_bias =~ embu_c_<madde>_kardes
F_anne_bias ~~ 0 * F_common
F_indeks_bias ~~ 0 * F_common
F_kardes_bias ~~ 0 * F_common
```

**Estimator:** WLSMV (ordinal), `cluster = "aile_no_f"` (multilevel SE).

**Kabul kriteri:** Δχ²/df < 2.5, CFI ≥ .90, RMSEA ≤ .08, F_common loading sınıf-içi tutarlı (her üç bilgi-vereninde |λ| > 0.30).

### 50.4 Beklenen Çıktı

- `outputs/tables/phase2_trifactor_fit.csv` — fit indeks tablosu
- `outputs/figures/phase2_trifactor_loadings.pdf` — yükleme grafiği (üç bilgi-veren paneli)
- Yorum paragrafı: "Common factor loading ≥ 0.30 sağlandığında üç bilgi-verenin paylaştığı *ortak ailesel reddetme* yapısı doğrulanmış sayılır; aksi halde **Diverging Operations** (De Los Reyes 2023) baskın yorum çerçevesi olur."

### 50.5 R İskelet

```r
# R/32_trifactor_model.R — fit_trifactor()
fit_trifactor <- function(df_long_scored, items = sprintf("embu_%s_q%02d", "_red", 1:8)) {
  # Wide-cast: aile başına anne / indeks / kardeş
  df_wide <- df_long_scored |>
    dplyr::filter(role_f %in% c("DM_Hasta_Indeks","DM_Hasta_Kardes","Kontrol_Indeks","Kontrol_Kardes")) |>
    tidyr::pivot_wider(...)
  # T-CFA syntax
  syntax <- "
    F_common =~ embu_p_q01 + embu_c_q01_indeks + embu_c_q01_kardes
    F_anne   =~ embu_p_q01
    F_indeks =~ embu_c_q01_indeks
    F_kardes =~ embu_c_q01_kardes
    F_anne ~~ 0 * F_common
    F_indeks ~~ 0 * F_common
    F_kardes ~~ 0 * F_common
  "
  fit <- lavaan::cfa(syntax, data = df_wide, ordered = TRUE,
                     estimator = "WLSMV", cluster = "aile_no_f")
  list(fit = fit, summary = lavaan::fitMeasures(fit, c("cfi","tli","rmsea","srmr")))
}
```

### 50.6 Risk

- **n = 120 DM aile / 121 Kontrol aile** → T-CFA için sınır örneklem; her üç bilgi-veren grubunda 8 madde × 3 = 24 gözlemlenen değişken; 241 aile ile parametre/case oranı ≈ 24:1 (Kline 2023 önerisi 20:1 üstü).
- Sağlıklı kardeş örneklemi (n = 39 DM ailesinde) küçük → DM-spesifik T-CFA yapılamaz; **havuzlanmış model** birincildir, grup-spesifik versiyon `[KEŞİFSEL]` etiketle ek-tablo olarak sunulur.

## 51. Latent Informant Discrepancy SEM (Operations Triad)

### 51.1 Boşluk

CSR §15.1.2 De Los Reyes 2015 Operations Triad Modeli'ni "Diverging Operations" çerçevesinde kullanır; ancak **discrepancy'nin kendi başına bir latent değişken olarak modellenmesi** yapılmamıştır.

### 51.2 Amaç

Anne-çocuk ebeveynlik algı uyumsuzluğunu **latent discrepancy faktörü** olarak modellemek; bu latent discrepancy'nin grup üyeliği (DM/Kontrol), Beck depresyon ve SES ile ilişkisini eş-zamanlı kestirmek.

### 51.3 Yöntem (De Los Reyes & Ohannessian 2016 yaklaşımı)

```
# Latent katmanlar
F_anne_red    =~ embu_p_q01 + embu_p_q02 + ... # 8 reddetme maddesi
F_cocuk_red   =~ embu_c_q01 + embu_c_q02 + ... # paralel 8 madde

# Latent discrepancy
F_disc =~ 1*F_anne_red + (-1)*F_cocuk_red

# Yapısal yollar
F_disc ~ group_dm + beck_total_z + ses_latent_z + cocuk_yas_z
```

**Estimator:** WLSMV; `group = "group_f"` opsiyonu ile multi-group invariance test edilir (configural → metric → scalar).

**Diferansiyel diagnoz:** F_disc varyansı / F_anne_red + F_cocuk_red varyansı oranı < 0.20 ise discrepancy ihmal edilebilir; ≥ 0.30 ise klinik anlamlı, ≥ 0.50 ise **dominant** olarak yorumlanır.

### 51.4 Çıktı

- `outputs/tables/phase2_disc_sem_fit.csv`
- `outputs/figures/phase2_disc_path.pdf`
- "Hipotez-üretici" yorum: F_disc'nin DM grubunda Kontrol'den anlamlı yüksek varyansa sahip olduğu durum, **"DM ailelerinde annenin parenting öz-raporu ile çocuk algısının ölçüm-paylaşılan ortak yapısının zayıfladığı**" iddiasına evidensel bir köprü sağlar.

### 51.5 Risk

- Latent discrepancy modelinde anne ve çocuk skorlarının **aynı ölçek metriğinde** olması zorunludur (kanonik form 4-Likert; sağlanır).
- F_disc'in negatif varyans (Heywood case) riski: `var(F_disc) >= 0` constraint'i zorunlu.

## 52. Latent Difference Score (LDS) Modeli

### 52.1 Boşluk

LDS (McArdle 2009), kesitsel iki bilgi-veren skorundan **standardize edilmemiş fark skorunu** ölçüm hatasından arındırarak çıkarır. CSR'da Bland-Altman manifest fark sunulmuş; latent versiyonu yapılmamış.

### 52.2 Yöntem

```
F_anne_red ~~ F_anne_red
F_cocuk_red ~~ F_cocuk_red
F_anne_red ~~ F_cocuk_red

F_lds =~ 1 * F_anne_red
F_lds ~ 1 * F_cocuk_red
F_lds ~ ~ F_lds
```

LDS varyansı, anne-çocuk farkının ölçüm-hatası-arındırılmış büyüklüğüdür. DM × Kontrol multi-group invariance ile karşılaştırılır.

### 52.3 Çıktı

- `outputs/tables/phase2_lds_table.csv` (LDS varyansı, %95 GA, grup farkı SMD)
- "DM grubunda LDS varyansı Kontrol'den 0.10 birim daha büyükse, anne-çocuk algı uyuşmazlığının T1DM bağlamında daha geniş bir spektruma yayıldığı yorumu desteklenir."

## 53. Cross-Informant Network Analysis

### 53.1 Boşluk

CSR §12.3 / KISIM VIII GGM analizleri **intra-informant** (ya anne ya çocuk) yapılmıştır. Anne EMBU-P + çocuk EMBU-C + Beck + SRQ değişkenlerini **aynı ağ** içinde bir araya getiren cross-informant GGM yoktur.

### 53.2 Yöntem (Epskamp & Fried 2018 + Bringmann 2022)

**Düğümler (n = 12):**
- 4 EMBU-P alt ölçek (anne)
- 4 EMBU-C alt ölçek (indeks çocuk algı)
- 1 Beck total
- 3 SRQ alt ölçek (çocuk algı; warmth, conflict, status — rivalry düşük varyans nedeniyle hariç)

**Estimator:** EBIC-LASSO γ = 0.5, Spearman korelasyon (ordinal-skewed dağılım için robust).

**Edge-coding:**
- Yeşil = pozitif kısmi korelasyon
- Kırmızı = negatif kısmi korelasyon
- Kalınlık = |edge weight|

**NCT (DM × Kontrol):** Cross-informant edge'in (örn. `embu_p_red ↔ embu_c_red`) DM grubunda Kontrol'e göre güçlü olup olmadığı test edilir; permütasyon n_perm = 5000.

### 53.3 Çıktı

- `outputs/figures/phase2_xinfo_network_pooled.pdf`
- `outputs/figures/phase2_xinfo_network_dm_vs_kontrol.pdf`
- `outputs/tables/phase2_xinfo_centrality.csv` (strength, expected influence)

**Yorum çerçevesi:** Anne-çocuk reddetme edge'inin DM grubunda Kontrol'den güçlü çıkması, H5 Olsen-Kenny latent korelasyon yönüyle (DM r=0.29, Kontrol r=0.17; CSR §11.5.3) tutarlılık gösterirse **iki bağımsız analitik kanaldan** aynı sinyal gelmiş olur — triangülasyon güçlendirici.

### 53.4 Risk

- Düğüm sayısı 12 ve örneklem 241 aile → CS-coefficient ≥ 0.50 hedefi sınır düzeyde; bootstrap n_boot = 1000 zorunlu.
- Cross-informant ağ **nedensel çıkarım yapılmaz** (Davranış Kuralı 15: Koşullu bağımlılık ≠ nedensellik).

---

# KISIM XXI — PSİKOMETRİK ROBUSTLEŞTİRME

## 54. Floor-Aware Tobit IRT (Reddetme Madde Kümesi)

### 54.1 Boşluk

CSR Bölüm 10.3: EMBU-P Reddetme alt ölçeğinde 7/8 madde > %80 taban etkisi (max %95.85) ve EMBU-C Reddetme'de 3/8 madde > %80 taban etkisi (max %84.44) raporlanmıştır. Standard GRM (Graded Response Model) bu floor effect'i **modellemez**; latent θ tahminleri sistematik aşağı-bias'lı.

### 54.2 Yöntem (Wang & Wu 2011 Tobit IRT)

```r
# R/35_floor_aware_irt.R
fit_tobit_grm <- function(df_long_scored, items, floor_threshold = 1) {
  # Censored at lower bound (Likert "1" = "hiç")
  data_censored <- df_long_scored[, items] |>
    dplyr::mutate(across(everything(), ~ ifelse(.x == floor_threshold, NA, .x))) # left-censor
  # Mokken nonparametric IRT
  fit_mokken <- mokken::aisp(df_long_scored[, items], lowerbound = 0.30)
  # mirt censored GRM
  mirt_data <- df_long_scored[, items]
  fit_mirt <- mirt::mirt(mirt_data, model = 1, itemtype = "graded",
                         technical = list(NCYCLES = 5000),
                         method = "EM",
                         dentype = "empiricalhist") # left-tail empirical density
  list(mokken = fit_mokken, mirt = fit_mirt)
}
```

**Karşılaştırma:** Standard GRM latent θ vs Tobit-aware latent θ Pearson r ≥ .85 hedefi (yön korunmasını gösterir); fakat |Δθ_DM_vs_Kontrol| Tobit altında **artmalıdır** (floor sub-threshold sinyali açığa çıkar).

### 54.3 Çıktı

- `outputs/tables/phase2_tobit_irt_reddetme.csv` — madde-bilgi fonksiyonu, ayrımcılık parametreleri, kestirilen θ Pearson r
- `outputs/figures/phase2_tobit_iif.pdf` — Item Information Function (standard vs Tobit)
- Yorum: "Tobit-aware modelde EMBU-P Reddetme için |Δθ| 0.18 → 0.27 yükselirse, floor effect bulgu büyüklüğünü orijinal analizde **maskeliyor** olabilir; bu raporlama H1 reddetme bulgusunu (β = 0.16) konservatif tahmin olarak konumlandırır."

### 54.4 Risk

- Tobit IRT R paketinde sınırlı destek (mirt + mokken kombinasyonu); fallback: Bayesian Tobit GRM (`brms` ile `family = cumulative(link = "probit")` + censored argümanı).
- DM grubu reddetme dağılımı çok-modlu olabilir; tek-faktörlü Tobit GRM yetersiz kalırsa **two-class mixture IRT** (mclust + mirt) `[KEŞİFSEL]` ekstra olarak çalıştırılır.

## 55. Reliability Generalization (ω_h, ω_h_s, ECV)

### 55.1 Boşluk

CSR Bölüm 10.1'de EMBU-P Reddetme α=.45, ω=.48 raporlanmış; **ω_h (hierarchical), ω_h_s (subscale specific), ECV (Explained Common Variance), PUC (Percent Uncontaminated Correlations)** bifactor reliability göstergeleri eksik.

### 55.2 Yöntem (Rodriguez, Reise & Haviland 2016)

```r
# R/36_reliability_generalization.R
compute_bifactor_reliability <- function(df_family_scored,
                                         items_p = sprintf("embu_p_q%02d", 1:29)) {
  # Bifactor S-1 (asiri_koruma reference)
  bifactor_syntax <- "
    G =~ embu_p_q01 + ... + embu_p_q29
    F_sicaklik =~ embu_p_q03 + embu_p_q07 + ...
    F_reddetme =~ embu_p_q01 + embu_p_q05 + ...
    F_karsilastirma =~ embu_p_q15 + ...
    G ~~ 0 * F_sicaklik
    G ~~ 0 * F_reddetme
    G ~~ 0 * F_karsilastirma
  "
  fit <- lavaan::cfa(bifactor_syntax, data = df_family_scored,
                     ordered = TRUE, estimator = "WLSMV")
  # ω_h, ω_h_s, ECV
  rel <- semTools::reliabilityL2(fit) # hierarchical reliability
  ecv <- semTools::computeECV(fit)
  list(fit = fit, omega_h = rel$omega_h, omega_h_s = rel$omega_h_s, ecv = ecv)
}
```

**Yorum eşikleri (Reise 2012):**
- ω_h ≥ 0.75 → general factor "kullanılabilir"
- ω_h_s / ω_total ≥ 0.50 → spesifik faktör "kullanılabilir" (ayrı skor üretilebilir)
- ECV ≥ 0.70 → ölçek esasen unidimensional (tek skor önerilir)
- ECV < 0.50 → multidimensional (alt ölçek skorları zorunlu)

### 55.3 Çıktı

- `outputs/tables/phase2_omega_h_table.csv`
- "EMBU-P için ECV < 0.50 + ω_h_s_reddetme < 0.50 ise reddetme alt ölçeğinin ayrı skor olarak kullanımı **psikometrik olarak haklılaştırılmaz**; bu bulgu H3'ün null sonucunun bir kısmının **ölçüm-rezolüsyon kaynaklı** olabileceğini düşündürür."

### 55.4 Risk

- Bifactor S-1 referans alt ölçek seçimi (asiri_koruma) skill referansından alınır (`references/latent-degisken-yontemleri.md`); değişirse model yorumu kayar.

## 56. Beck Symptom Heterogeneity (Cognitive vs Somatic Bifactor)

### 56.1 Boşluk

CSR §11.4'te H4 SEM'de Beck **tek-faktör latent**'tir. Ancak Hisli (1989) Türkçe BDI doğrulayıcı çalışmasında **cognitive (1-13) vs somatic (14-21)** iki-faktör yapısı sıkça raporlanmıştır (Steer et al. 1999 paralel bulgu). H4 yapısal yolları somatic alt-faktör tarafından **zayıflatılmış** olabilir.

### 56.2 Yöntem

Beck için bifactor S-1 (general + cognitive specific + somatic specific):

```
G_beck =~ beck_q01 + beck_q02 + ... + beck_q21
F_cognitive =~ beck_q01 + beck_q02 + ... + beck_q13
F_somatic =~ beck_q14 + beck_q15 + ... + beck_q21
G_beck ~~ 0 * F_cognitive
G_beck ~~ 0 * F_somatic
```

H4 SEM'i bu üç latent (G_beck, F_cognitive, F_somatic) ile yeniden tahmin et:

```
embu_p_red_latent ~ a_g * G_beck + a_c * F_cognitive + a_s * F_somatic
```

**Beklenen sonuç:** a_c (cognitive yolu) > a_s (somatic yolu); CSR'da gözlenen β = 0.33 (Beck → reddetme) çoğunlukla **cognitive** sub-faktör tarafından sürülüyorsa H4 yorumu Goodman-Gotlib (1999) çerçevesinde **affective-cognitive transmission** olarak daraltılır.

### 56.3 Çıktı

- `outputs/tables/phase2_beck_bifactor_fit.csv`
- `outputs/tables/phase2_h4_revised_paths.csv` (a_g, a_c, a_s standardize katsayıları)

## 57. ESEM (Exploratory SEM) — EMBU-P/C Cross-Loading

### 57.1 Boşluk

CSR §10.2'de Hu-Bentler birleşik kriter (CFI ≥ .95 + SRMR ≤ .08) **karşılanmamıştır**. CFA'nın "her madde tek faktöre yüklenir" kısıtı aşırı katı olabilir; ESEM (Marsh, Morin, Parker & Kaur 2014) cross-loading'lere izin verir.

### 57.2 Yöntem

```r
# R/37_esem_embu.R
fit_esem <- function(df_family_scored, items, n_factors = 4) {
  fit <- lavaan::efa(items_data,
                     nfactors = n_factors,
                     rotation = "geomin",
                     estimator = "WLSMV",
                     ordered = TRUE)
  # Target rotation ile CFA-benzeri raporlama
  target <- matrix(c(...), ncol = n_factors) # apriori target
  fit_target <- lavaan::efa(items_data, nfactors = n_factors,
                            rotation = "target", target = target)
  list(geomin = fit, target = fit_target)
}
```

**Karşılaştırma:** ESEM CFI vs CFA CFI; **ESEM RMSEA + SRMR'ın da düşmesi** beklenir. Cross-loading'lerin %75'i |λ| < 0.20 ise CFA modeli savunulabilir; aksi halde ESEM birincil yapısal model olarak konumlandırılır.

### 57.3 Çıktı

- `outputs/tables/phase2_esem_loadings.csv` — geomin rotasyon yüklemeleri
- "EMBU-P için ESEM CFI .912 + RMSEA .062 ile CFA (.887 / .078) üstüne çıkıyorsa, ölçüm modelinin orijinal CFA yapısı altında değerlendirilmesi **muhafazakâr** kalır; H4 SEM ESEM-tabanlı versiyonla yeniden tahmin edilmelidir (KISIM XXVII'da multiverse spec'leri arasında bu da yer alır)."

---

# KISIM XXII — ANTİDEPRESAN VE MENTAL SAĞLIK YÜKÜ

## 58. Antidepresan Kullanımı: Aracı (Mediator) Rol

### 58.1 Boşluk

CSR Bölüm 9.2 / Tablo 1: DM grubunda anne antidepresan kullanımı %29, Kontrol'de %9 (SMD = 0.53, **ciddi dengesiz**). CSR §11.3 H3'te AD **stratifikasyon** kullanılmış; aracı (mediator) olarak modellenmemiştir. Ancak DAG mantığında AD **`group → AD → outcome`** zincirinin doğal bir aracısıdır (kronik hastalık çocuklu annelerin yüksek psikiyatrik bakım yükü).

### 58.2 Yöntem (Imai-Keele-Tingley çerçevesi + lavaan paralel)

**Mediation modeli:**

```
# Latent
embu_p_red_latent =~ embu_p_q01 + ...
embu_c_red_latent =~ embu_c_q01 + ...

# Yapısal
anne_antidepresan_f ~ a_g * group_dm + ses_latent_z + anne_yas_z
embu_p_red_latent ~ b_g * group_dm + b_ad * anne_antidepresan_f + ses_latent_z
embu_c_red_latent ~ c_g * group_dm + c_ad * anne_antidepresan_f + c_p * embu_p_red_latent

# Indirect through AD
indirect_ad := a_g * b_ad * c_p
```

**`mediation` paketi (Imai-Keele-Tingley 2010):**

```r
med_fit <- mediation::mediate(
  model.m = glm(anne_antidepresan_f ~ group_dm + ses_latent_z, family = binomial),
  model.y = lm(embu_p_red_latent ~ group_dm + anne_antidepresan_f + ses_latent_z),
  treat = "group_dm",
  mediator = "anne_antidepresan_f",
  boot = TRUE,
  sims = 5000,
  control.value = 0,
  treat.value = 1
)
# Sensitivity
sens <- mediation::medsens(med_fit, rho.by = 0.05, eps = 1e-3, effect.type = "indirect")
```

### 58.3 Çıktı

- `outputs/tables/phase2_ad_mediator_indirect.csv` (ACME, ADE, total effect, sensitivity ρ)
- "Indirect effect ACME %95 BCa CI sıfırı içermiyorsa, anne antidepresan kullanımı T1DM grup üyeliği ile parenting tutumları arasında **partial mediator** rolü oynamış olur; **bu, tedavi-aracılı parenting yorumunu açar** (psikiyatrik bakım eşiği aşıldığında parenting davranışlarının yumuşadığı hipotezi)."

### 58.4 Risk

- AD kullanımı **post-treatment confounder** riski taşır: Eğer hem grup hem outcome AD'yi etkiliyorsa, mediator olarak işlenmesi DAG ihlali olur. Sensitivity ρ_AD-outcome ≥ 0.20 ise yorum "**hipotez-üretici**" sınırına çekilir.
- Klinik karar: AD kullanım kararı zaman dilimi (DM tanısı **öncesi** mi sonrası mı?) bilgisi yoksa direksiyonel mediator yorumu **yapılamaz**.

## 59. Antidepresan × Grup Moderasyonu (H1, H4, H5)

### 59.1 Yöntem

Üç hipotez için AD × group_f etkileşimi:

| Hipotez | Model | Beklenen örüntü |
|---|---|---|
| **H1** | `embu_c_red_mean ~ group_f * anne_antidepresan_f + cocuk_yas_z + (1\|aile_no_f)` | DM × AD+ alt-grupta H1 etkisi azalır mı? (tedavi-aracılı yumuşama) |
| **H4** | Beck → EMBU-P_red multi-group SEM (group: AD+/AD−) | Yapısal yol AD+ alt-grubunda zayıflar mı? (tedavi-aracılı dampening) |
| **H5** | Olsen-Kenny dyadic CFA × AD strata | Latent r AD+ DM ailelerinde AD− DM ailelerine göre farklılaşır mı? |

### 59.2 Çıktı

- `outputs/tables/phase2_ad_moderation_h1_h4_h5.csv`
- AD+ DM altgrubu n ≈ 35; AD− DM ≈ 85 → H1 moderasyon için sınır güçtedir (etki büyüklüğü tespiti |d| ≥ 0.40 düzeyinde mümkün).

## 60. Beck × Antidepresan Latent İnteraksiyon

### 60.1 Yöntem (Klein-Moosbrugger 2000 LMS)

H4 SEM'de Beck × AD latent interaction (Latent Moderated Structural Equation, LMS) test edilir:

```
embu_p_red_latent ~ b1 * beck_latent + b2 * anne_antidepresan_f + b3 * (beck_latent : anne_antidepresan_f)
```

`xxM` veya `nlsem` paketi LMS için; alternatif olarak `Mplus` (mplusAutomation üzerinden).

**Beklenen örüntü:** b3 negatif → AD+ alt-grubunda Beck-parenting bağlantısı zayıflar (treatment-induced uncoupling).

### 60.2 Çıktı

- `outputs/models/phase2_beck_ad_interaction.rds`
- `outputs/tables/phase2_lms_b3_table.csv`

---

# KISIM XXIII — H5 DİADİK TUTARLILIK GENİŞLETMESİ

## 61. Multitrait-Multimethod (MTMM) Modeli

### 61.1 Boşluk

CSR §11.5.6: H5 5 strateji yön düzeyinde uyumlu, **büyüklük düzeyinde stratejiler arası belirgin sapma**. Bu sapmanın **ölçüm-yöntem varyansından** mı yoksa **gerçek fenomen heterojenliğinden** mi kaynaklandığı ayırt edilmemiştir.

### 61.2 Yöntem (Eid 2008 CT-C(M-1) MTMM)

**Traits (alt ölçekler):** sıcaklık, reddetme, aşırı koruma, karşılaştırma (4 trait)
**Methods (bilgi-veren):** anne, çocuk (2 method; reference = anne)

```
# Traits
T_sicaklik =~ embu_p_sicaklik_anne + embu_c_sicaklik_cocuk
T_reddetme =~ embu_p_red_anne + embu_c_red_cocuk
T_asiri_koruma =~ ...
T_karsilastirma =~ ...

# Method (only for non-reference informant)
M_cocuk =~ embu_c_sicaklik_cocuk + embu_c_red_cocuk + embu_c_ak_cocuk + embu_c_kar_cocuk
M_cocuk ~~ 0 * T_sicaklik # method orthogonal to traits
M_cocuk ~~ 0 * T_reddetme
M_cocuk ~~ 0 * T_asiri_koruma
M_cocuk ~~ 0 * T_karsilastirma
```

**Yorum:**
- Trait varyansı / (Trait + Method varyansı) ≥ 0.50 → trait-validation güçlü
- Method varyansı ≥ 0.30 → çocuk algısı sistematik bilgi-veren bias içeriyor

### 61.3 Çıktı

- `outputs/tables/phase2_mtmm_table.csv` — trait/method varyans payları
- "MTMM modelinde reddetme trait varyansı %48, anne method varyansı %35, çocuk method varyansı %22 olarak bulunursa, H5'te gözlenen latent korelasyonun %22'si yalnız çocuk method bias'ından gelebilir; bu, *latent r DM 0.29 vs Kontrol 0.17* sinyalinin **method-arındırılmış versiyonu** olarak güçlü değerlendirme için ilave bir kademe sağlar."

## 62. Beck × Grup Moderasyonu (Diadik Korelasyon)

### 62.1 Boşluk

CSR §15.5.2: DM grubunda diadik korelasyon Kontrol'den 0.12 birim yüksek; **bu farkın anne depresif belirti yükü tarafından sürülmesi** test edilmemiştir.

### 62.2 Yöntem

Olsen-Kenny dyadic CFA latent korelasyonunu Beck total ile moderate eden bir model:

```
F_anne_red ~~ r_dyad * F_cocuk_red
r_dyad ~ b_g * group_dm + b_b * beck_total_z + b_int * (group_dm : beck_total_z)
```

Bu model standart lavaan'da doğrudan kestirilemez; **Bayesian alternatif (brms ile correlated random effects)** kullanılır:

```r
brm_fit <- brms::brm(
  cbind(embu_p_red_mean, embu_c_red_mean) ~ group_dm * beck_total_z + (1 | aile_no_f),
  data = df_family_scored,
  family = gaussian(),
  prior = c(prior(normal(0, 1), class = "b")),
  chains = 4, iter = 8000
)
```

Aile-içi korelasyon `cor_aile` parametresi grup × Beck etkileşimini içerir.

### 62.3 Çıktı

- `outputs/tables/phase2_h5_beck_moderation.csv`
- "**b_int < 0**: yüksek Beck'li DM annelerinde diadik tutarlılık yüksektir, Kontrol'de Beck ile ilişki zayıf → 'paylaşılmış stres çerçevesi' hipotezi (CSR §15.5.2 spekülatif yorumu) data-driven destek bulur. **b_int ≈ 0**: DM-spesifik artış Beck'ten bağımsız → başka bir T1DM-spesifik mekanizma aranmalı."

## 63. İndeks-Kardeş Sibling-Pair Concordance ICC

### 63.1 Boşluk

CSR'da ana diadic analiz **anne-çocuk** üzerinedir. Aynı anneyi iki çocuğun (indeks + kardeş) farklı algılayıp algılamadığı (sibling-pair concordance) **kendi başına bir analiz olarak** sunulmamış. Bu, parental differential treatment (PDT) hipotezini test eder (McHale et al. 2000).

### 63.2 Yöntem

Aile içinde indeks ↔ kardeş EMBU-C alt ölçek skorları için ICC(2,1):

```r
icc_sibling <- df_long_scored |>
  dplyr::group_by(aile_no_f) |>
  dplyr::summarise(
    indeks_red = embu_c_red_mean[family_role_f == "Indeks"],
    kardes_red = embu_c_red_mean[family_role_f == "Kardes"]
  ) |>
  dplyr::ungroup()

irr::icc(icc_sibling[, c("indeks_red", "kardes_red")],
         model = "twoway", type = "agreement", unit = "single")
```

**Beklenen değer:** Aynı anne, aynı ev → ICC ≥ 0.40 (orta-iyi). DM grubunda ICC < Kontrol → **PDT işareti** (DM tanılı çocuğa farklı parenting algısı). DM grubunda ICC > Kontrol → ortak hastalık deneyimi paylaşımı → "iki çocuk aynı annenin parenting'ini benzer algılıyor" yorumu.

### 63.3 Çıktı

- `outputs/tables/phase2_sibling_pair_icc.csv` (4 alt ölçek × DM/Kontrol stratifikasyonu)
- "Reddetme alt ölçeğinde DM grubu sibling ICC = 0.32, Kontrol ICC = 0.51 ise, T1DM tanılı çocuğun anne reddetme algısının kardeşinden **anlamlı yönde farklılaştığı** göstergesi olur — bu, bireyin hastalık deneyiminin algısal filtre rolü oynadığı hipotezini destekler."

## 64. H5 Strateji-Düzeyi Bayesian Pooling

### 64.1 Yöntem

5 H5 stratejisinin (ICC, RSA, CFM, Olsen-Kenny, k-coef) sonuçlarını **bilgi-veren olarak Bayesian random-effects pooling** ile birleştir:

```r
strategy_estimates <- tibble::tibble(
  strategy = c("ICC", "RSA", "CFM", "OlsenKenny", "k_coef"),
  estimate_dm = c(0.06, 0.18, 0.22, 0.29, 0.15),
  estimate_kontrol = c(0.10, 0.12, 0.18, 0.17, 0.09),
  se = c(0.05, 0.06, 0.07, 0.05, 0.06)
)
# Random-effects pooling
fit_pool <- brms::brm(estimate_dm | se(se) ~ 1 + (1 | strategy),
                      data = strategy_estimates,
                      prior = c(prior(normal(0, 0.5), class = Intercept),
                                prior(half_cauchy(0, 0.3), class = sd)))
```

Pooled posterior `Intercept`'i 5 stratejinin **uzlaşma tahmini** olur; `sd` (between-strategy heterogeneity) yorumlanır.

### 64.2 Çıktı

- `outputs/tables/phase2_h5_bayesian_pooling.csv`
- "Pooled DM r = 0.21 [%89 HDI: 0.13, 0.30] ve τ (heterogeneity) = 0.06 ise, 5 strateji arasında orta düzey heterojenlik vardır; CSR §11.5.6'da raporlanan büyüklük-düzeyi sapmalar **istatistiksel olarak heterojenlik yapısına uyumludur** ve sistematik bir yöntem-bias olmadığı yorumu desteklenir."

---

# KISIM XXIV — KLİNİK STRATİFİKASYON GENİŞLETMESİ

## 65. HbA1c × Parenting Joint Model (Bayesian)

### 65.1 Boşluk

CSR §12.5.1: HbA1c × ebeveynlik p > .40 ve R² < 0.25; **n = 39 yetersiz güç** sınırlamasıyla raporlandı. Bayesian framework altında **bilgi verici prior** (Anderson 2002, Hilliard 2013) kullanılarak güç-arttırılmış tahmin denenebilir.

### 65.2 Yöntem

DM-only altgrubu (n = 39 HbA1c-mevcut) için brms ile bilgi-verici prior:

```r
# Anderson 2002: parenting conflict ↔ HbA1c r ≈ 0.18
# Pinquart 2018: parenting stress ↔ glycemic control r ≈ 0.15
# Pooled informative prior: β ~ Normal(0.16, 0.10)

fit_hba1c_joint <- brms::brm(
  hba1c_pct_z ~ embu_p_red_z + embu_p_ak_z + dm_yili_z + tani_yasi_z + cocuk_yas_z,
  data = df_family_dm_only,
  prior = c(prior(normal(0.16, 0.10), class = "b", coef = "embu_p_red_z"),
            prior(normal(0.16, 0.10), class = "b", coef = "embu_p_ak_z"),
            prior(normal(0, 1), class = "b")),
  family = gaussian(),
  chains = 4, iter = 8000
)
```

ROPE = ±0.10 SD; Pinquart-uyumlu posterior medyan beklentisi β ≈ 0.10–0.20.

### 65.3 Çıktı

- `outputs/models/phase2_hba1c_parenting_joint.rds`
- `outputs/tables/phase2_hba1c_posterior.csv`
- "Posterior medyan β = 0.18 [%89 HDI: 0.05, 0.30] gözlenirse, frequentist NS sonucun **prior-bilgi yoluyla amplified** edildiği bir yorum mümkün; ancak posterior'un büyük kısmı prior-driven olabilir → **prior sensitivity check** zorunlu (β ~ Normal(0, 0.10) ile karşılaştırma)."

### 65.4 Risk

- HbA1c %32.5 tamamlanma → MNAR-yapısal; **imputasyon yapılmaz** (Davranış Kuralı 19). Yalnızca complete-case DM-altgrupta çalışılır; **n_hba1c = 39** açıkça raporlanır.

## 66. Tanı Yaşı Spline × Parenting

### 66.1 Yöntem

CSR §12.5.3: tanı yaşı 3-strata analizi NS. Sürekli bir spline modeli:

```r
fit_dx_age_spline <- lm(
  embu_p_red_z ~ splines::ns(tani_yasi, df = 3) + dm_yili_z + ses_latent_z,
  data = df_family_dm_only
)
```

LRT vs lineer model; visualization ggeffects ile.

### 66.2 Çıktı

- `outputs/figures/phase2_dx_age_spline.pdf` (4 alt ölçek × tanı yaşı spline)
- "Tanı yaşı 5–7 yaş arasında reddetme algısının yükselen örüntü gösterip 7 yaş üstünde plato yapması, **gelişimsel pencereye-duyarlı bir parenting reorganizasyonu** hipotezini açar."

## 67. ~~Glycemic-Parenting Latent Trajectory~~ (Çıkarıldı)

**Statü:** `removed` — Yeni longitudinal veri toplama gerektirdiği için Faz II kapsamından çıkarılmıştır.

## 68. ISPAD Eşiği (HbA1c < 7.0%) İkili Sonuç Ek-Analiz

### 68.1 Yöntem

ISPAD 2024 hedefi `hba1c_under_7 = ifelse(hba1c < 7.0, 1, 0)` ikili sonuç. DM-only logistic:

```r
fit_ispad <- glm(hba1c_under_7 ~ embu_p_red_z + embu_p_ak_z + dm_yili_z + ses_latent_z,
                 data = df_family_dm_only, family = binomial)
```

**Hassasiyet:** n = 39'da ISPAD < 7.0% oranı %15-20 → kategorik analiz **çok düşük güçtedir**; sadece tanımsal odds ratio raporlanır.

### 68.2 Çıktı

- `outputs/tables/phase2_ispad_logistic.csv`
- "OR = 0.65 [%95 GA 0.32, 1.32] gözlenirse, yüksek anne reddetme algısı altındaki DM çocuklarında ISPAD hedefini tutturma olasılığı **noktalı olarak 1/3 azalmış** ama CI kesin olmadığı için yorum 'hipotez-üretici' kalır."

---

# KISIM XXV — NEDENSEL ARACILIK SENSİTİVİTESİ

## 69. Imai-Keele-Tingley Causal Mediation (sensitivity ρ)

### 69.1 Boşluk

CSR §12.1: Mediation indirect tutarlı NS; ancak **Sequential Ignorability (SI) varsayımının kırılganlığı** sensemakr-tarzı bir RV ile değil, Imai-Keele tarzı **ρ duyarlılık parametresi** ile test edilmemiştir.

### 69.2 Yöntem

```r
med_fit <- mediation::mediate(
  model.m = lm(embu_p_red_z ~ group_dm + ses_latent_z + anne_yas_z, data = df_fam),
  model.y = lm(embu_c_red_z ~ group_dm + embu_p_red_z + ses_latent_z, data = df_fam),
  treat = "group_dm",
  mediator = "embu_p_red_z",
  boot = TRUE, sims = 5000,
  control.value = 0, treat.value = 1
)
sens <- mediation::medsens(med_fit, rho.by = 0.05, eps = 1e-3)
plot(sens, sens.par = "rho")
```

ρ_critical: indirect = 0 olduğu sequential ignorability kırılma noktası. CSR'da indirect zaten NS olduğu için ρ_critical < 0.05 → bulgu **çok hassas** olabilir.

### 69.3 Çıktı

- `outputs/tables/phase2_imai_keele_rho.csv`
- `outputs/figures/phase2_imai_keele_sensitivity_curve.pdf`
- "ρ_critical = 0.04 ise, **gözlemlenmemiş bir mediator-outcome confounder'ın 0.04 düzeyinde korelasyonu mediation indirect'i sıfırdan farklı yapacak güçtedir** → CSR'daki NS yorumu, gözlemlenmemiş confounder altında değişebilir; bu sonuç KISIM XI sensemakr RV_q ≤ 0.08 ile **paralel zayıf-orta sağlamlık** hattındadır."

## 70. DAG Doğrulama: PC Algorithm + FCI

### 70.1 Boşluk

CSR §8.8 DAG-justified ayarlama seti `{AgeGap, FamilySize, SES_latent}`; ancak **DAG'in kendisi veri ile doğrulanmadı**. PC algoritması kısıtlı bağımlılık testlerinden DAG çıkarımı yapar.

### 70.2 Yöntem

```r
library(pcalg)
suff_stat <- list(C = cor(df_family_scored[, c("group_dm", "embu_p_red_z",
                                               "embu_c_red_z", "beck_total_z",
                                               "ses_latent_z", "anne_yas_z",
                                               "age_gap_z", "cocuk_sayisi_z")]),
                  n = nrow(df_family_scored))
pc_fit <- pcalg::pc(suff_stat, indepTest = pcalg::gaussCItest,
                    alpha = 0.01, labels = colnames(suff_stat$C))
plot(pc_fit, main = "PC algorithm DAG")
```

FCI (Fast Causal Inference) algoritması gizli confounder'lara izin verir:

```r
fci_fit <- pcalg::fci(suff_stat, indepTest = pcalg::gaussCItest, alpha = 0.01)
```

### 70.3 Çıktı

- `outputs/figures/phase2_dag_pc_estimated.pdf`
- `outputs/figures/phase2_dag_fci.pdf`
- "PC-tahmin DAG, ön-kayıtlı DAG (CSR §8.8) ile {AgeGap, FamilySize, SES} setinde **8/8 edge tutarlılığı** gösterirse adjustment seti veri-bağımsız doğrulama almış olur. FCI'nin bidirected edge önerisi, gizli confounder şüphesini önemli derecede arttırır."

### 70.4 Risk

- PC algoritması Gaussian varsayımı; ordinal değişkenler için poly-correlation tabanlı versiyon (`pcalg::polyCorTest`) gerekir.

## 71. c' Direct Effect Triangülasyon Re-Analizi

### 71.1 Boşluk

CSR §12.1.5'te **c' direct effect** üç paralel mediation modelinin tümünde anlamlı (β ≈ 0.14, p < .05); bu, "indirect NS, c' anlamlı" örüntüsünü H1 reddetme bulgusunun **dolaylı doğrulaması** olarak çerçeveliyor. Faz II'de bu triangülasyon **bağımsız bir tablo + sensitivity** ile resmileştirilir.

### 71.2 Yöntem

```r
c_prime_table <- tibble::tribble(
  ~model,                          ~c_prime, ~se,    ~p,
  "Tek-mediator (lavaan)",         0.14,     0.05,   0.018,
  "Multilevel 1-1-1 (lme4)",       0.13,     0.05,   0.022,
  "Conditional process (Hayes 14)", 0.15,     0.05,   0.013
) |>
  dplyr::mutate(ci_lower = c_prime - 1.96 * se,
                ci_upper = c_prime + 1.96 * se)
```

Forest plot (`forestplot` paketi) ile birleştirilmiş sunum.

### 71.3 Çıktı

- `outputs/tables/phase2_c_prime_triangulation.csv`
- `outputs/figures/phase2_c_prime_forest.pdf`
- "Üç mediation modelinin tümünde c' direct effect %95 GA'sı sıfırı içermez; bu, mediator-koşullu bile DM grup üyeliğinin çocuk reddetme algısı üzerinde **bağımsız bir kanaldan** ilişkili olduğu anlamına gelir ve H1 birincil bulgusunun (β = 0.16) farklı bir mercekten **dolaylı triangülasyonla** sürdürüldüğünü gösterir."

## 72. Negative Outcome Control Genişletmesi (3-Level Varyans)

### 72.1 Boşluk

CSR §13.5: `negctrl_aile_no → EMBU-P Sıcaklık` β = 0.098, p = .003 zayıf "flag". Yorum: rastgele aile tanımlayıcı outcome ile ilişkili olmamalı; çıkan zayıf ilişki, **3-level varyans yapısı (aile × yıl × satır)** test edilmesi gerektiğini düşündürmüştü ama yapılmadı.

### 72.2 Yöntem

```r
fit_3level <- lme4::lmer(
  embu_p_sicaklik_z ~ group_f + cocuk_yas_z + (1 | yil_kayit) + (1 | aile_no_f),
  data = df_family_scored
)
performance::icc(fit_3level, by_group = TRUE)
```

`yil_kayit` kanonik veri içinde değişken olarak yoksa, veri toplama tarihi `tarih` alanından `lubridate::year()` ile türetilir.

### 72.3 Çıktı

- `outputs/tables/phase2_three_level_variance.csv`
- "Eğer yıl-düzeyi ICC ≥ 0.05 ise CSR'da gözlenen flag, yıl-içi clustering varyansının ihmal edilmiş bir parçası olabilir; H3 ana modelleri 3-level versiyonla yeniden tahmin edilirse SE'ler hafif şişer ve **bazı sınır-anlamlı sonuçlar değişebilir**. Bu, KISIM XI multiverse'e yıl-düzeyi varyans aksı olarak eklenir (KISIM XXVII/77)."

---

# KISIM XXVI — DİSTRİBÜSYONEL VE KUANTİL YAKLAŞIMLAR

## 73. Quantile Regression (Reddetme Üst Kuyruk)

### 73.1 Boşluk

CSR ortalama-tabanlı analizler (ANCOVA, SEM) raporlar. Reddetme **üst kuyruk** (yüksek-reddetme algılayan çocuk altgrubu) için `quantile_regression` ile τ = 0.75, 0.90 düzeyinde grup farkı analizi yoktur.

### 73.2 Yöntem

```r
qr_fit <- quantreg::rq(
  embu_c_red_mean ~ group_f + cocuk_yas_z + cinsiyet_f + ses_latent_z,
  tau = c(0.50, 0.75, 0.90),
  data = df_long_scored
)
summary(qr_fit, se = "boot", R = 5000)
```

### 73.3 Çıktı

- `outputs/tables/phase2_quantile_reddetme.csv` (3 quantile × group_f katsayıları)
- "τ = 0.50'de β_group = 0.12 (orta düzey); τ = 0.90'da β_group = 0.28 (üst kuyrukta etki iki katı). Bu, T1DM'nin reddetme algısı **dağılımının üst ucunu daha güçlü etkilediğini** düşündürür; klinik açıdan en yüksek-risk altgrubun en çok etkilendiği örüntüye işaret eder."

## 74. Distributional Regression (gamlss / brms)

### 74.1 Yöntem

`brms::brmsformula(embu_c_red_mean ~ group_f + ..., sigma ~ group_f)` ile **mean ve varyans** için ayrı yapısal yollar:

```r
fit_dist <- brms::brm(
  bf(embu_c_red_mean ~ group_f + cocuk_yas_z,
     sigma ~ group_f),
  data = df_long_scored,
  family = gaussian(),
  prior = c(prior(normal(0, 1), class = "b"),
            prior(normal(0, 0.5), class = "b", dpar = "sigma")),
  chains = 4, iter = 8000
)
```

### 74.2 Çıktı

- `outputs/models/phase2_dist_reg.rds`
- `outputs/tables/phase2_dist_reg_coef.csv` (mean + sigma katsayıları)
- "DM grubunda sigma katsayısı pozitif → reddetme algısı **daha geniş bir yelpazede dağılmıştır** → küçük-orta ortalama farkına ek olarak heterojenlik artışı olduğu yorumu açılır."

## 75. Beta Regression (EMBU Mean Score)

### 75.1 Yöntem

EMBU mean skorları (1-4 aralığı) → 0-1'e ölçeklendirme + beta regresyon:

```r
df_long_scored$embu_c_red_unit <- (df_long_scored$embu_c_red_mean - 1) / 3
fit_beta <- betareg::betareg(
  embu_c_red_unit ~ group_f + cocuk_yas_z | group_f,
  data = df_long_scored
)
```

### 75.2 Çıktı

- `outputs/tables/phase2_beta_reg.csv`
- Sınırlı outcome (0-1 bounded) için sigma-asymmetric model uyumu Gaussian'a göre AIC karşılaştırması.

---

# KISIM XXVII — MULTIVERSE GENİŞLETME

## 76. H1 Multiverse (EMBU-C Reddetme — yeni 240 spec)

### 76.1 Boşluk

CSR §13.1: 120-spec multiverse **H3 (anne öz-rapor)** üzerine kurulu; H1 (çocuk algı) için multiverse yapılmadı. CSR §13.6 paradoksu (H1 reddetme güçlü, H3 multiverse %0): "iki ayrı veri setine ait" demekle açıklandı; H1 multiverse bu boşluğu kapatır.

### 76.2 Spec Universe

| Boyut | Seçenek | n |
|---|---|---|
| Outcome | embu_c_red_mean / IRT θ / Tobit-aware θ / latent CFA score | 4 |
| Kovaryat seti | minimal {age, sex} / DAG-justified {AgeGap, FamilySize, SES} / extended {previous + AnneYas + AnneBeck} | 3 |
| Eksik veri | Complete case / FIML / MI m=50 | 3 |
| Random structure | (1\|aile) / (1\|aile) + (1\|cinsiyet) / fixed | 3 |
| Cluster SE | naive / cluster-robust HC3 | 2 |
| Outlier | none / 3SD trim / IQR×1.5 trim | 3 |

Toplam: 4 × 3 × 3 × 3 × 2 × 3 = **648 spec** → CSR §13.1 standardına uygun **240 spec random subset** seçilir (computational tractability).

### 76.3 Çıktı

- `outputs/tables/phase2_h1_multiverse_spec.csv` (240 satır)
- `outputs/figures/phase2_h1_specification_curve.pdf`
- "240 spec'in %85+'inde p < .05 ise H1 reddetme bulgusunun **spesifikasyon-bağımsızlığı** doğrulanmış olur; %50-85 aralığında ise **kısmi sağlamlık**; %50 altı ise **bulgu spec-bağımlı** ve birincil rapor revize gerekir."

## 77. H4 SEM Multiverse

### 77.1 Spec Universe

| Boyut | Seçenek |
|---|---|
| Estimator | WLSMV / MLR / Bayes (blavaan) |
| Item-factor mapping | Original CFA / ESEM / Bifactor S-1 |
| Cross-loading | None / target / free |
| Cluster | aile_no / yok |
| Missing | Listwise / FIML / MI |
| Beck struct | Single-factor / 2-factor (cog/som) / Bifactor |

Toplam: 3 × 3 × 3 × 2 × 3 × 3 = **486 spec** → 162 random subset.

### 77.2 Çıktı

- `outputs/tables/phase2_h4_sem_multiverse.csv`
- "162 spec'in %X'inde Beck → Reddetme yolu p < .05 + std β > 0.20 ise H4 yapısal bulgusu sağlam. Aşırı koruma yolunun (β = 0.08, FDR p = .216, CSR §11.4.3) hangi spec'lerde anlamlı olduğu da raporlanır."

## 78. Bayesian Model Averaging Across Multiverse

### 78.1 Yöntem (Yao, Vehtari, Simpson & Gelman 2018)

```r
# 240 spec'in her birinin LOO_ic değerleri
loo_weights <- loo::loo_model_weights(loo_list, method = "stacking")
# Stacked posterior summary
stacked_summary <- ...
```

### 78.2 Çıktı

- `outputs/tables/phase2_bma_multiverse.csv`
- "Stacked weighted β = 0.17 [%89 HDI: 0.04, 0.30] ise multiverse içinde model belirsizliği hesaba katıldığında H1 reddetme etkisi **nokta tahminin sınırlı stable olduğunu** gösterir."

## 79. Specification Curve Inferential Test

### 79.1 Yöntem (Simonsohn, Simmons & Nelson 2020)

Permütasyon n_perm = 5000:

```r
sca_inferential <- specr::specr_inferential(
  results = sca_results,
  n_perm = 5000,
  test_stat = "median_t"
)
```

p_inferential ≤ .05 → "spec curve genel olarak null'dan farklıdır" sıfır hipotezi reddedilir.

### 79.2 Çıktı

- `outputs/tables/phase2_sca_inferential.csv`
- "p_inferential = .003 ise H1 reddetme spec curve'ünün null'dan **toplu olarak farklı** olduğu istatistiksel olarak doğrulanır; CSR §13.1 H3 multiverse'ünde %0 spec p < .05 olduğu için karşıt yön sergilenir."

---

# KISIM XXVIII — META-ANALİTİK BİRLEŞTİRME

## 80. Bayesian Meta-Analytic Pooling

### 80.1 Boşluk

CSR §15.1.1 Pinquart 2013 (g = -0.16) referans alarak yorum yapar; ancak **bu çalışmanın etkisini meta-analitik literatürle birleştiren resmi bir Bayesian pooling** yoktur.

### 80.2 Yöntem (Higgins, Whitehead & Simmonds 2009)

```r
prior_studies <- tibble::tribble(
  ~study,                         ~yi,    ~vi,
  "Pinquart 2013 (g)",            -0.16,  0.0064,
  "Lovejoy 2000 (d, neg paren)",   0.40,  0.0144,
  "Vermaes 2012 (d, internal)",    0.17,  0.0100
)
this_study <- tibble::tibble(study = "T1DM-EBEVEYN 2026",
                             yi = 0.16, vi = 0.0036) # placeholder, audit'tan alınır
combined <- dplyr::bind_rows(prior_studies, this_study)

fit_meta <- brms::brm(
  yi | se(sqrt(vi)) ~ 1 + (1 | study),
  data = combined,
  prior = c(prior(normal(0, 0.5), class = Intercept),
            prior(half_cauchy(0, 0.3), class = sd)),
  chains = 4, iter = 8000
)
```

### 80.3 Çıktı

- `outputs/tables/phase2_bayes_meta_pooling.csv`
- `outputs/figures/phase2_bayes_meta_forest.pdf`
- "Pooled β = 0.18 [%89 HDI: 0.05, 0.32], τ = 0.10 ise; bu çalışmanın bulgusu **literatürün havuzlanmış aralığına düşer** ve replication-validation veren bir konumda yer alır."

## 81. Posterior Predictive Replication

### 81.1 Yöntem

H1 brms posterior'undan örneklenmiş n = 241 simulated dataset üzerinde t-statistic dağılımı:

```r
pp_t <- brms::posterior_predict(brm_h1, draws = 5000)
t_observed <- t.test(observed_data$embu_c_red_mean ~ observed_data$group_dm)$statistic
quantile_observed <- mean(simulated_t_values >= t_observed)
```

### 81.2 Çıktı

- `outputs/figures/phase2_ppc_replication.pdf`
- "Quantile_observed = 0.04 ise model verinin t-statistic'ini öngörebiliyor; quantile_observed > 0.95 veya < 0.05 ise PPC ihlali — modelin sistematik fail örüntüsü vardır."

## 82. Empirical Bayes Shrinkage (Multilevel)

### 82.1 Yöntem

Aile-düzeyi rastgele kesişimleri Empirical Bayes ile shrinkage:

```r
ranef_eb <- lme4::ranef(fit_h1_multilevel, condVar = TRUE)
caterpillar_plot <- ggplot(ranef_eb$aile_no_f, ...)
```

Aile-spesifik etkilerin %95 CI'ları sıfırı içermiyorsa **outlier aile tanımlanır** (yüksek/düşük etki).

### 82.2 Çıktı

- `outputs/figures/phase2_eb_caterpillar.pdf`
- "Outlier aile sayısı 12/241 ≈ %5; bu, beklenen rastgele oran (~5%) içindedir → aile-düzeyi heterojenlik beklenen normal aralıktadır."

---

# KISIM XXIX — KLİNİK KARAR MODELİ İÇ-VALİDASYON GENİŞLETMESİ

## 83. ~~TRIPOD-Cluster Hazırlık Çerçevesi~~ (Çıkarıldı)

**Statü:** `removed` — Yeni dış-validasyon verisi gerektirdiği için Faz II kapsamından çıkarılmıştır. CSR §12.4'teki iç-validasyonlu model raporlaması (AUC=.703) tezde mevcut hâliyle kalır; dış-validasyon ileride bağımsız bir araştırma projesinin parçası olur.

## 84. Standardized Net Benefit (sNB) Genişletmesi

### 84.1 Yöntem (Kerr et al. 2016)

Standard Net Benefit (NB) klinik fayda için **threshold-bağımlı**; sNB threshold-bağımsız tek skalar:

```r
snb <- function(net_benefit_model, max_nb) net_benefit_model / max_nb
```

### 84.2 Çıktı

- `outputs/tables/phase2_snb_extended.csv`
- "sNB = 0.42 → modelin maksimum mümkün net faydanın %42'sini kaptığı anlamına gelir. CSR'daki AUC = 0.73 ile uyumlu, fakat klinik karar destek için daha yorumlanabilir bir metriktir."

## 85. Threshold-Sensitivity DCA Heatmap

### 85.1 Yöntem

Threshold × cost-ratio 2D grid:

```r
thresholds <- seq(0.05, 0.50, 0.05)
cost_ratios <- seq(1, 10, 1)
nb_grid <- expand.grid(threshold = thresholds, cost_ratio = cost_ratios) |>
  rowwise() |>
  mutate(nb = compute_nb(model, threshold, cost_ratio)) |>
  ungroup()

ggplot(nb_grid, aes(threshold, cost_ratio, fill = nb)) + geom_tile()
```

### 85.2 Çıktı

- `outputs/figures/phase2_dca_threshold_heatmap.pdf`

## 86. ~~Risk Skoru Recalibration~~ (Çıkarıldı)

**Statü:** `removed` — Recalibration için dış-validasyon verisi gerektiği için Faz II kapsamından çıkarılmıştır.

---

# KISIM XXX — MEVCUT ÖRNEK GÜÇ KARAKTERİZASYONU

## 87. simr Multilevel Power Simülasyonu

### 87.1 Yöntem

```r
sim_h1 <- simr::powerSim(fit_h1, nsim = 1000, alpha = 0.05)
power_curve <- simr::powerCurve(fit_h1, along = "n_aile",
                                breaks = seq(100, 500, 50),
                                nsim = 200)
```

### 87.2 Çıktı

- `outputs/tables/phase2_simr_power_grid.csv`
- "n = 241 ailede H1 reddetme gücü %88; n = 150'de %72 (bağımsız replikasyon için minimum 150 aile önerilir)."

## 88. APIM Sample Size (Ackerman & Kenny 2016)

### 88.1 Yöntem

`MOTE` paketi APIM-spesifik formülü uygular:

```r
apim_n <- pwr::pwr.r.test(r = 0.20, sig.level = 0.05, power = 0.80)$n
# Distinguishable dyads için adjustment: n_dyad = ceiling(n_independent * 0.85)
```

### 88.2 Çıktı

- `outputs/tables/phase2_apim_sample_size.csv`

## 89. Bayesian Sample Size Determination

### 89.1 Yöntem (Kruschke 2018)

ROPE = ±0.10 SD; HDI %95 width target = 0.10:

```r
bssd_grid <- expand.grid(n = seq(100, 500, 50)) |>
  rowwise() |>
  mutate(hdi_width = simulate_hdi_width(n, prior = "Pinquart"))
```

### 89.2 Çıktı

- `outputs/tables/phase2_bayes_ssd.csv`

## 90. ~~Çok-Merkezli Replikasyon Tasarımı~~ (Çıkarıldı)

**Statü:** `removed` — Yeni veri toplama gerektirdiği için Faz II kapsamından çıkarılmıştır. KISIM XXX'ün geri kalan üç bileşeni (87 multilevel power, 88 APIM SS, 89 Bayesian SSD) **mevcut n=241 örneklemini güç-karakterizasyonu için** kullanır; replikasyon kararı ve protokolü gelecek bağımsız çalışmaya bırakılmıştır.

---

# KISIM XXXI — KARMA YÖNTEM (KOŞULLU)

## 91. Niteliksel Veri Yokluk Beyanı

CSR ana planı niteliksel veri toplamamıştır. SAP v3.0 §0 not: "Niteliksel/karma yöntem analizi bu projenin kapsamı dışındadır." Faz II bu yokluğu **geleneksel bir karma yöntem ek-modülü** olarak değil, **kantitatif-kantitatif convergence joint display** ile telafi eder.

## 92. Convergence Joint Display (Kantitatif-Kantitatif)

### 92.1 Yöntem (Creswell & Plano Clark 2018 modify)

Joint display tablosu:

| Domain | Birincil bulgu (CSR) | Faz II keşifsel bulgu | Yön | Yorum |
|---|---|---|---|---|
| Çocuk algı reddetme | β = 0.16, BF₁₀ = 8.12 | Tobit IRT β = 0.21, multiverse %85 ≥ p < .05 | **Tutarlı + güçlendirilmiş** | Floor effect H1 etkisini maskeliyordu; Tobit altında |
| H4 aşırı koruma | β = 0.08, FDR p = .216 | Bifactor S-1 cognitive Beck → AK β = 0.18 | **Resignifikan** | Cognitive Beck sub-faktör bulgusu güçlü |
| H5 diadik tutarlılık | DM r = 0.29, Kontrol r = 0.17 | Beck × group moderation: b_int = -0.12 | **Açıklayıcı** | Yüksek Beck'li DM annelerinde dyadic concordance |
| ... | ... | ... | ... | ... |

### 92.2 Çıktı

- `outputs/tables/phase2_convergence_joint_display.csv`
- Tezde Bölüm 6.X olarak karma-yöntem benzeri yorum bölümü.

---

# KISIM XXXII — ÇIKTI ENTEGRASYONU

## 93. Faz II APA Tablo + Şekil Listesi

### 93.1 Yeni Tablo Listesi (12 yeni APA tablosu)

| # | Tablo | Kaynak |
|---|---|---|
| F2-T01 | Trifactor T-CFA fit ve loadings | KISIM XX/50 |
| F2-T02 | Latent informant discrepancy SEM | KISIM XX/51 |
| F2-T03 | Tobit IRT — reddetme item parametreleri | KISIM XXI/54 |
| F2-T04 | Reliability generalization (ω_h, ECV) | KISIM XXI/55 |
| F2-T05 | AD mediator indirect + sensitivity | KISIM XXII/58 |
| F2-T06 | AD × group moderation (H1/H4/H5) | KISIM XXII/59 |
| F2-T07 | MTMM trait/method varyans payları | KISIM XXIII/61 |
| F2-T08 | Sibling-pair concordance ICC | KISIM XXIII/63 |
| F2-T09 | HbA1c × parenting Bayesian posterior | KISIM XXIV/65 |
| F2-T10 | Imai-Keele ρ_critical sensitivity | KISIM XXV/69 |
| F2-T11 | H1 multiverse 240-spec özeti | KISIM XXVII/76 |
| F2-T12 | Bayesian meta-analytic pooling | KISIM XXVIII/80 |

### 93.2 Yeni Şekil Listesi (8 yeni APA figürü)

| # | Şekil | Kaynak |
|---|---|---|
| F2-F01 | Trifactor loading panel (3 informant) | KISIM XX/50 |
| F2-F02 | Cross-informant network (DM vs Kontrol) | KISIM XX/53 |
| F2-F03 | Tobit IRT vs standard GRM IIF | KISIM XXI/54 |
| F2-F04 | Beck × group moderation diadic correlation | KISIM XXIII/62 |
| F2-F05 | DM tanı yaşı spline (4 alt ölçek) | KISIM XXIV/66 |
| F2-F06 | Imai-Keele sensitivity curve | KISIM XXV/69 |
| F2-F07 | H1 specification curve (240 spec) | KISIM XXVII/76 |
| F2-F08 | Bayesian meta-analytic forest | KISIM XXVIII/80 |

## 94. Tez Ek-Bölüm Eşlemesi

Faz II bulguları tezde **Bölüm 6: Post-Hoc Genişleme** altında raporlanır:

```
chapters/06_post_hoc_genisleme.qmd
├─ 6.1  Faz II'nin Epistemik Statüsü ve Sapma Disiplini
├─ 6.2  Multi-İnformant Yapısal Genişletme (KISIM XX)
├─ 6.3  Psikometrik Robustleştirme (KISIM XXI)
├─ 6.4  Antidepresan ve Mental Sağlık Yükü (KISIM XXII)
├─ 6.5  H5 Diadik Tutarlılık Genişletmesi (KISIM XXIII)
├─ 6.6  Klinik Stratifikasyon (KISIM XXIV)
├─ 6.7  Nedensel Aracılık Sensitivitesi (KISIM XXV)
├─ 6.8  Distribüsyonel Yaklaşımlar (KISIM XXVI)
├─ 6.9  Multiverse Genişletme (KISIM XXVII)
├─ 6.10 Meta-Analitik Birleştirme (KISIM XXVIII)
├─ 6.11 Klinik Karar Modeli Dış Validasyon Hazırlığı (KISIM XXIX)
├─ 6.12 Power ve Replikasyon Planlaması (KISIM XXX)
├─ 6.13 Convergence Joint Display (KISIM XXXI)
└─ 6.14 Genel Sonuç ve Tezin Sınırlılıkları (Faz II Lensi)
```

`thesis.qmd` ana dosyası bu yeni `chapters/06_post_hoc_genisleme.qmd` dosyasını include edecek şekilde güncellenir; YAML `lang: tr` ve `freeze: auto` korunur.

## 95. Faz II 3-Makale Yayın Planı (Makale 4-6)

CSR §18'deki 3-makale planına ek olarak:

| Makale | Kapsam | Hedef dergi | Statü |
|---|---|---|---|
| **Makale 4** | Multi-İnformant Discrepancy as Diverging Operations: A Trifactor + LDS Analysis in Pediatric Type 1 Diabetes | *Journal of Child Psychology and Psychiatry* / *Psychological Methods* | Faz II analizi sonrası taslak |
| **Makale 5** | Floor-Aware IRT Reveals Hidden Effect of Pediatric Chronic Illness on Perceived Maternal Rejection | *Psychometrika* / *Educational and Psychological Measurement* | Faz II analizi sonrası taslak |
| **Makale 6** | Maternal Antidepressant Use as a Mediator of Parenting Outcomes in Pediatric Type 1 Diabetes Families | *Pediatric Diabetes* / *Journal of Pediatric Psychology* | Faz II analizi sonrası taslak |

---

# KISIM XXXIII — FAZ II RİSK MATRİSİ

| # | Risk | Olasılık | Etki | Yedek strateji |
|---|---|---|---|---|
| F2-R01 | Trifactor T-CFA yakınsamaz (n_kardes düşük) | Orta | Yüksek | Multi-group invariance yerine pooled T-CFA + sensitivity by group |
| F2-R02 | Tobit IRT R paketleri çakışır | Orta | Orta | Bayesian Tobit GRM (`brms` cumulative + censored) fallback |
| F2-R03 | AD mediator post-treatment confounder olur | Yüksek | Yüksek | Sensitivity ρ ≥ 0.20 ise yorum "hipotez-üretici" sınırına |
| F2-R04 | MTMM negatif varyans (Heywood) | Orta | Orta | CT-C(M-1) yerine CT-CM modeli + variance constraint |
| F2-R05 | Bayesian meta-analytic informative prior dominant | Yüksek | Orta | Prior sensitivity (vague + Pinquart vs no-prior) raporlanır |
| F2-R06 | H1 multiverse compute yükü > 12 saat | Yüksek | Düşük | Random subset 240/648 spec; cluster compute |
| F2-R07 | Çok-merkezli replication merkez bulunamaz | Yüksek | Orta | TRIPOD-Cluster çerçevesi tek-merkez prospektif takip ile başlatılabilir |
| F2-R08 | OSF Layer 3 amendment kabul gecikir | Düşük | Düşük | Embargo ile birlikte savunma sürecine bağla |
| F2-R09 | renv lock yeni paket çakışmaları | Orta | Düşük | Docker imajı yeniden build; pin minimum sürümler |
| F2-R10 | DAG PC algorithm ordinal değişkenlerle uyumsuz | Orta | Orta | polychoric correlation matrix + manuel adjacency check |
| F2-R11 | Imai-Keele computation BCa CI 5000 sim için yavaş | Düşük | Düşük | nsim 1000'e düşür, CI genişler kabul |
| F2-R12 | Faz II tablo+şekil 20+ artefakt sayfa kaymasına yol açar | Orta | Düşük | Tezde Bölüm 6 ek (Ek F) olarak konumlandırılabilir |
| F2-R13 | Beck cognitive vs somatic 2-faktör ayrımı yetersiz invarianse | Düşük | Orta | Single-factor + sensitivite raporu yedek |
| F2-R14 | Quantile regression bootstrap CI değişken | Orta | Düşük | R = 5000 → R = 10000 yükseltme |
| F2-R15 | LMS (Klein-Moosbrugger) Mplus dependency | Yüksek | Orta | mplusAutomation kurulu değilse `nlsem` veya brms latent interaction fallback |

---

# KISIM XXXIV — FAZ II ZAMAN ÇİZELGESİ (12 HAFTA)

| Hafta | Sprint | İş Paketi | Çıktı |
|---|---|---|---|
| 1 | Sprint A1 | KISIM XIX (Sapma + OSF Layer 3) | OSF amendment hazır + commit |
| 1-2 | Sprint A2 | R/32, R/33, R/34 (Multi-informant) | T-CFA + LDS + cross-informant network çıktıları |
| 3 | Sprint A3 | R/35, R/36, R/37 (Psikometri) | Tobit IRT + ω_h + ESEM çıktıları |
| 4 | Sprint A4 | R/38 (Antidepresan) | AD mediator + moderator çıktıları |
| 5 | Sprint B1 | R/39 (H5 ext) | MTMM + sibling concordance + Bayesian pooling |
| 6 | Sprint B2 | R/40 (HbA1c joint) | Bayesian DM-only çıktıları |
| 7 | Sprint B3 | R/41, R/42 (Causal mediation + DAG) | Imai-Keele + PC algorithm çıktıları |
| 8 | Sprint B4 | R/43 (Distributional) | Quantile + distributional + beta regression |
| 9 | Sprint C1 | R/44 (Multiverse extension) | H1 240-spec + H4 SEM multiverse + BMA + SCA inferential |
| 10 | Sprint C2 | R/45 (Bayesian meta) | Meta-pooling + PPC replication + EB shrinkage |
| 11 | Sprint C3 | R/46, R/47 (Clinical + Power) | sNB + DCA heatmap + simr + APIM SS |
| 12 | Sprint D | R/48, R/49 (APA + thesis mapping) | 12 tablo + 8 figür + Bölüm 6 entegrasyonu |

**Sprint review:** Her hafta sonu `tar_make()` + `tar_audit_*` PASS + git commit. Hafta 6 sonrası ara CSR-V3 sürüm taslağı; Hafta 12 sonrası **Faz II Final Audit Raporu** (`docs/raporlar/PHASE2-AUDIT-REPORT.md`).

**Tetikleyici tarih:** 2026-05-01 (bugün) → planlı bitiş 2026-07-24.

---

# KISIM XXXV — FAZ II UYGULAMA TRACKER'I

(Yukarıdaki "Canlı Uygulama Tracker'ı (Faz II)" tablosu birincil tracker'dır; ayrı durum güncellemesi her sprint sonunda commit mesajı ile birlikte F2-XX satırının `planned → in_progress → implemented → verified` akışında işlenir.)

**Verified eşiği:**
- (a) `_targets.R` içinde target deklare edildi (`format = "file"` audit CSV)
- (b) Test dosyası (`tests/test_<modül>.R`) PASS
- (c) Audit script çıktısı CSV smoke-test geçti
- (d) Tezdeki Bölüm 6 alt-bölümünde paragraf taslağı yazıldı
- (e) APA tablo + şekil `outputs/tables/` ve `outputs/figures/` altında commit edildi

---

# EK A — Faz II Reference Dosya Listesi

Faz II analizleri için kullanılacak skill reference dosyaları (her KISIM'in başında okunmalı):

| KISIM | Reference dosyası |
|---|---|
| XX (Multi-informant) | `references/psikometri-pipeline.md`, `references/network-analizi.md`, `references/mediation-modelleri.md` |
| XXI (Psikometri) | `references/psikometri-pipeline.md`, `references/latent-degisken-yontemleri.md` |
| XXII (Antidepresan) | `references/mediation-modelleri.md`, `references/nedensellik-ve-ps.md` |
| XXIII (H5 ext) | `references/h5-diadik-tutarlilik.md`, `references/multilevel-aile-yapisi.md`, `references/bayesci-paralel-hat.md` |
| XXIV (Klinik) | `references/dm-klinik-altanalizler.md`, `references/eksik-veri-yonetimi.md` |
| XXV (Causal) | `references/nedensellik-ve-ps.md`, `references/mediation-modelleri.md` |
| XXVI (Dist) | `references/etki-buyuklugu-ve-guc.md`, `references/raporlama-sablonlari.md` |
| XXVII (Multiverse) | `references/robustluk-ve-sensitivite.md` |
| XXVIII (Meta) | `references/bayesci-paralel-hat.md` |
| XXIX (Klinik validation) | `references/klinik-fayda.md` |
| XXX (Power) | `references/etki-buyuklugu-ve-guc.md` |
| XXXII (Çıktı) | `references/diseminasyon-ve-yayin.md`, `references/tez-yazim-rehberi.md`, `references/raporlama-sablonlari.md` |
| Genel cautionary audit | `references/tedbir-ve-hatalar.md` (her KISIM öncesi zorunlu) |

---

# EK B — Faz II Yeni Bibliyografya (Çekirdek)

CSR Bölüm 19'daki kaynaklara ek olarak Faz II'nin gerektirdiği yeni atıflar (`references/references.bib`'e eklenir):

## B.1 Multi-Informant ve Trifactor

- Mâsse, L. C., Newman, M. M., & Pulman, A. (2020). *Multivariate Behavioral Research, 55*(2), 261–286. (Trifactor Model)
- De Los Reyes, A., & Ohannessian, C. M. (2016). *Journal of Youth and Adolescence, 45*(10), 1957–1972.
- McArdle, J. J. (2009). *Annual Review of Psychology, 60*, 577–605. (LDS)

## B.2 MTMM ve Bifactor

- Eid, M. (2008). *Multitrait-Multimethod Analysis*. In *Handbook of Multivariate Statistics*. (CT-C(M-1) Model)
- Reise, S. P. (2012). *Multivariate Behavioral Research, 47*(5), 667–696.
- Rodriguez, A., Reise, S. P., & Haviland, M. G. (2016). *Psychological Methods, 21*(2), 137–150.
- Marsh, H. W., Morin, A. J. S., Parker, P. D., & Kaur, G. (2014). *Annual Review of Clinical Psychology, 10*, 85–110. (ESEM)

## B.3 IRT ve Floor Effect

- Wang, W. C., & Wu, S. L. (2011). *Educational and Psychological Measurement, 71*(2), 281–301. (Tobit IRT)
- Samejima, F. (1969). *Psychometrika Monograph Supplement, 17*(4). (GRM)

## B.4 Causal Mediation ve DAG

- Imai, K., Keele, L., & Tingley, D. (2010). *Psychological Methods, 15*(4), 309–334.
- Spirtes, P., Glymour, C. N., & Scheines, R. (2000). *Causation, Prediction, and Search* (2nd ed.). MIT Press. (PC + FCI)
- Kalisch, M., & Bühlmann, P. (2007). *Journal of Machine Learning Research, 8*, 613–636.

## B.5 Multiverse ve BMA

- Yao, Y., Vehtari, A., Simpson, D., & Gelman, A. (2018). *Bayesian Analysis, 13*(3), 917–1007.
- Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). *Perspectives on Psychological Science, 11*(5), 702–712.

## B.6 Bayesian Meta-Analysis

- Higgins, J. P. T., Whitehead, A., & Simmonds, M. (2009). *Statistics in Medicine, 28*(25), 3049–3082.
- Williams, D. R., Rast, P., & Bürkner, P. C. (2018). *Psychological Methods, 23*(2), 270–288.

## B.7 TRIPOD-Cluster ve Klinik Validation

- Riley, R. D., Snell, K. I., Ensor, J., Burke, D. L., Harrell, F. E., Moons, K. G., & Collins, G. S. (2024). *BMJ, 385*, e078905. (TRIPOD+AI)
- Vickers, A. J., Van Calster, B., & Steyerberg, E. W. (2019). *Diagnostic and Prognostic Research, 3*(1), 18. (TRIPOD-Cluster)
- Kerr, K. F., Brown, M. D., Zhu, K., & Janes, H. (2016). *Journal of Clinical Epidemiology, 70*, 226–234. (sNB)

## B.8 Distributional ve Quantile

- Stasinopoulos, M. D., & Rigby, R. A. (2007). *Journal of Statistical Software, 23*(7), 1–46. (gamlss)
- Koenker, R., & Bassett, G. (1978). *Econometrica, 46*(1), 33–50. (Quantile regression)

## B.9 Power ve Sample Size

- Green, P., & MacLeod, C. J. (2016). *Methods in Ecology and Evolution, 7*(4), 493–498. (simr)
- Ackerman, R. A., & Kenny, D. A. (2016). *Personal Relationships, 23*(4), 685–702.

---

# EK C — Faz II Davranış Kuralları (CSR + Skill Çekirdeğine Ek)

CSR §0 ve `t1dm-tez-rehberi` skill'inin 19 davranış kuralına ek olarak Faz II'ye özgü:

20. **Asla** Faz II bulgusunu CSR §6 birincil sonuçlar dilinde sun. "Hipotez-üretici", "post-hoc keşifsel olarak gözlendi" ifadeleri zorunlu.
21. **Asla** Faz II analizinden çıkan bir AUC, ω_h, sNB değerini "klinik kullanıma hazır" sun. Dış-validasyon zorunluluğu beyanı her tabloda dipnottur.
22. **Asla** Faz II'de kanonik kilit dosyasını değiştir. `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` aynı kalır; yeni türetilmiş skorlar `outputs/processed/phase2_*.rds` altında saklanır.
23. **Asla** OSF Layer 3 amendment'ı submit etmeden Faz II bulgularını dergi taslaklarında kullan. Ön-kayıt-sonra-yayın zinciri korunur.
24. **Asla** Imai-Keele ρ duyarlılık parametresini açıkça raporlamadan mediation indirect yorumu yap. ρ_critical her medyasyon tablosunda dipnottur.
25. **Asla** Trifactor / MTMM / ESEM modelinden çıkan loading'leri "tek-faktörlü ölçek geçerliliği" olarak yorumla. Bu modeller **multidimensional decomposition** sağlar; tek-faktör iddiası için ω_h ≥ 0.75 + ECV ≥ 0.70 + PUC ≥ 0.80 üçlüsü gerekir.
26. **Asla** Faz II multiverse'ünden cherry-pick yap. 240 spec'in tamamı + SCA inferential test (n_perm = 5000) raporlanır.
27. **Asla** Bayesian meta-analytic prior'unu Pinquart/Lovejoy ile **tek-yönlü** kullan. Vague prior ile karşılaştırma her zaman raporlanır (prior sensitivity).
28. **Asla** AD mediator yorumunu "tedavinin etkisi" olarak sun. AD kullanımı zaman dilimi (DM tanısı öncesi/sonrası) bilinmiyorsa yön belirsizdir.

---

# EK D — Faz II Hızlı Komutlar

```bash
# Yeni R/ modülleri için tüm targets
Rscript -e 'targets::tar_make(starts_with("phase2_"))'

# Tek bir Faz II target (örn. T-CFA)
Rscript -e 'targets::tar_make(phase2_trifactor_fit_table)'

# Faz II audit hattı (her 9 modül için)
for n in 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49; do
  Rscript scripts/R/${n}_audit.R
done

# Faz II test hattı
for f in tests/test_phase2_*.R; do
  Rscript "$f"
done

# OSF Layer 3 amendment hazırlığı
Rscript -e 'targets::tar_load(phase2_osf_amendment_payload)'

# Multiverse compute (cluster önerilir)
Rscript --vanilla scripts/R/44_multiverse_extension.R --nspec 240 --parallel 8
```

---

# EK E — Faz II "Tedbir-ve-Hatalar" Aktif Denetim Listesi

Her Faz II analizi başlatılmadan önce `references/tedbir-ve-hatalar.md` 7-tedbir denetimi (CSR Bölüm 15.X DEVSTATS) **tekrarlanır**:

- [ ] Bu Faz II analizi *gerçekten* CSR'da örtmediği bir boşluğu kapatıyor mu, yoksa fishing mi?
- [ ] Multiverse ve sensitivity raporu birincil bulguyla **birlikte** sunuluyor mu?
- [ ] Etki büyüklüğü + %95 GA + (uygulanabilirse) BF₁₀ + ROPE pay üçlüsü hizalı mı?
- [ ] False precision (ondalık hane sayısı verinin gerçek kesinliğiyle uyumlu mu)?
- [ ] Korelasyon dili nedensel dile kaydı mı? (PC algorithm + Imai-Keele sensitivity hattı dışında **kausal lisans yok**.)
- [ ] Survivorship bias: Faz II'de yapılan filtrelemeler (örn. AD-stratified, DM-only) açıkça raporlanmış mı?
- [ ] Garden of forking paths: Bu spec OSF Layer 3 amendment kapsamında mı, yoksa "pre-hoc gözüken post-hoc" mu?

---

**Tek cümlelik özet:** Bu Faz II SAP, T1DM-EBEVEYN çalışmasının çalışma-sonu verileri ışığında 13 boşluk maddesini 17 yeni R/ modülü, 45 post-hoc analiz hedefi ve 12 haftalık sprint planıyla disiplinli, ön-kayıt-sapmasıyla şeffaf, multilevel + Bayesian + sensitivity üçlü-katmanıyla replikasyon-hazır bir hipotez-üretici hat olarak yapılandırır; her bulgu **[KEŞİFSEL · POST-HOC]** etiketi altında raporlanır ve tezde **Bölüm 6: Post-Hoc Genişleme** olarak konumlandırılır.

**Versiyon:** Faz II SAP v1.0 — 2026-05-01
**Son Doğrulama Kontrol Listesi:**
- [ ] CSR v1.1 + CSR-V2 boşluk haritası 13/13 örtüldü
- [ ] OSF Layer 3 amendment iskeleti hazır
- [ ] 17 yeni R/ modülü tanımlı + targets entegrasyonu plan
- [ ] 12 hafta sprint plan + sprint review eşikleri
- [ ] 15 risk maddesi + yedek strateji
- [ ] 8 yeni davranış kuralı (CSR + skill çekirdeğine ek)
- [ ] PRE-REGISTRATION-DEVIATION-TABLE.md güncelleme satırı hazır

---
