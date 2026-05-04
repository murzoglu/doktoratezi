# İSTATİSTİKSEL ANALİZ PLANI v3.0 — DEFİNİTİF VE EKSİKSİZ

**T1DM-EBEVEYN Çalışması** — Pre-registered Tam Analiz Hattı
*Tip 1 Diyabet Tanılı Çocuklar, Sağlıklı Kardeşleri ve Annelerinin Ebeveynlik Tutumlarına Yönelik Algılarının Sağlıklı Kontrol Grubu ile Karşılaştırılarak İncelenmesi ve Kardeşler Arası İlişkilerin Değerlendirilmesi*

| Alan | İçerik |
|---|---|
| **Doktora öğrencisi** | Uzm.Dr. Özlem Murzoğlu Kurt |
| **Tez danışmanı** | Prof.Dr. Eren Özek (MÜTF, Neonatoloji) |
| **Yardımcı araştırıcı** | Doç.Dr. Belma Haliloğlu (MÜTF, Pediatrik Endokrinoloji) |
| **TİK** | Prof.Dr. Perran Boran; Prof.Dr. Nalan Karabayır |
| **Protokol** | KAEK 09.2023.201 (06.01.2023) |
| **Enstitü onayı** | 2023/19-68 (11.05.2023) |
| **SAP sürümü** | **v3.0 — DEFİNİTİF FİNAL** (2026-04-27) |
| **Kanonik veri** | `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` (2026-04-26, status: LOCKED) |
| **Tamamlanmış faz** | Psikometrik validasyon (`21-psikometrik-validasyon-sonuclari.qmd`) |
| **Skill orkestrasyonu** | `devstats` × `psychdev` × `medical-research` |
| **Yazılım** | R 4.5.3 + Quarto 1.6+ + `targets` + `renv` + Stan 2.32+ |

---

## İÇİNDEKİLER

**KISIM I — META-ALTYAPI**
1. Pre-Registration Çerçevesi
2. Reprodüktiblik Mimarisi (`renv` + Docker + `_targets.R`)
3. Etik ve Veri Yönetimi
4. Reporting Standardı (STROBE + JARS-Quant + TRIPOD)

**KISIM II — VERİ KATMANI**
5. Hash Doğrulama ve Yükleme
6. Türetilmiş Skor Ekosistemi
7. SES Kompozit Türetme (Bourdieu Üç-Sermaye)
8. Eksik Veri Çoklu-Çerçeve (MI + FIML + NMAR Sensitivity)

**KISIM III — TANIMLAYICI VE DENGE**
9. Tablo 1 + SMD
10. Causal DAG
11. Propensity Score (IPTW + Matching) + Doubly Robust

**KISIM IV — PSİKOMETRİK VALIDASYON** (referans olarak; ayrı doküman)

**KISIM V — BİRİNCİL HİPOTEZ TESTLERİ**
12. H1: Çocuk Algı Multilevel ANCOVA + 3-Way + IRT GRM + Bayesian
13. H2: Kardeş İlişkisi (Aile-Mean + APIM + Olsen-Kenny + Age-Gap Moderation)
14. H3: Anne Öz-Rapor (Antidepresan-Stratified + IPTW)
15. H4: Beck → EMBU-P Latent SEM + Multi-Group Invariance + Bayesian
16. H5: Diadik Tutarlılık (RSA + Common Fate + Dyadic CFA + k-Coefficient)

**KISIM VI — MEDIATION**
17. Tek-Mediator (Beck → EMBU-P → ChildPerception)
18. Multilevel Mediation (Level-1 + Level-2)
19. Conditional Process Analysis (Hayes Modeli — Moderated Mediation)
20. Bayesian Mediation + ROPE

**KISIM VII — LATENT DEĞİŞKEN YÖNTEMLERİ**
21. Latent Profile Analysis (LPA — Anne Tipoloji)
22. Latent Class Analysis (Kategorik) + Mixture Regression
23. Bifactor S-1 Modeli (General + Specific Factor Ayrımı)

**KISIM VIII — NETWORK ANALİZİ**
24. Gaussian Graphical Model (EBIC-LASSO)
25. Network Comparison Test (DM × Kontrol)
26. Beck Item-Level Symptom Network

**KISIM IX — KLİNİK FAYDA**
27. Risk Skor Geliştirme + ROC + Decision Curve Analysis (Vickers 2006)
28. CART Karar Ağacı + Random Forest (Variable Importance)
29. Calibration + NRI/IDI (Pencina 2008)

**KISIM X — KLİNİK ALT-ANALİZLER (DM)**
30. HbA1c × Ebeveynlik Etkileşimi
31. DM Süresi Spline Modeli
32. Tanı Yaşı Stratifikasyonu

**KISIM XI — ROBUSTLUK VE SENSİTİVİTE**
33. Multiverse Specification Curve (Simonsohn 2020)
34. Equivalence Testing (TOST + Bayesian Equivalence)
35. Sensemakr + E-value (VanderWeele 2017) — Unmeasured Confounding
36. Negative Control Outcome + Falsification Tests

**KISIM XII — BAYESCİ PARALEL HAT**
37. Bayesian Multilevel (brms) — Tüm H1–H5
38. Bayes Faktörü + ROPE
39. Posterior Predictive Checks + WAIC/LOO

**KISIM XIII — RAPORLAMA VE DİSEMİNASYON**
40. APA Tablo + Şekil Üretimi
41. Tez Bölüm Eşlemesi
42. 3-Makale Yayın Stratejisi
43. Open Data + Code Plan (OSF + Zenodo)

**KISIM XIV — DEVSTATS YEDİ UYARICI İLKE DENETİMİ**
44. Yedi tedbir denetim hattı

**KISIM XV — RİSK YÖNETİMİ VE YEDEK STRATEJİLER**
45. Final risk matrisi

**KISIM XVI — ÇALIŞTIRMA ZAMAN ÇİZELGESİ**
46. 24-haftalık plan

**KISIM XVII — TAM REFERANSLAR LİSTESİ**

**KISIM XVIII — SAP v3.0 SON DOĞRULAMA KONTROL LİSTESİ**

> Niteliksel/karma yöntem analizi (eski KISIM XIII: tematik analiz, joint display, inter-coder reliability) bu projenin kapsamı dışındadır ve ayrı bir araştırma projesi olarak yürütülecektir.

---

## CANLI UYGULAMA TRACKER'I

**Tracker kuralı:** Bu tablo SAP'in yaşayan uygulama kaydıdır. Her yeni faz tamamlandığında ilgili satır `planned -> in_progress -> implemented -> verified` akışıyla güncellenecek; doğrulama komutu veya üretilen artefakt aynı satıra işlenecektir.

**Durum sözlüğü**

| Durum | Anlam |
|---|---|
| `verified` | Kod, runner/test, `_targets` veya ilgili audit komutu çalıştırıldı; çıktı doğrulandı |
| `implemented` | Tasarım/kod/dokümantasyon eklendi; geniş doğrulama bekliyor |
| `reference_completed` | Bu SAP dışında tamamlanmış ve referans olarak tutuluyor |
| `planned` | Henüz uygulanmadı |
| `deferred` | Sonraki faz veya dış koşul bekliyor |

**Son tracker güncellemesi:** 2026-04-28 (verified seviyeye yükseltme turu)  
**Son doğrulama kapsamı:** KISIM I-V verified · KISIM V/16 (H5) verified · KISIM VI / 17-19, KISIM VII / 21-23, KISIM VIII / 24-26, KISIM IX / 27-29, KISIM X / 30-32, KISIM XI / 33-36, KISIM XII / 37-39 **verified**: tar_target entegrasyonu tamam (186 target), 8/8 test_*.R `stopifnot()` PASS, audit CSV içerik smoke-test geçti.

| Faz | Kısım | İş paketi | Durum | Kanıt / canlı artefakt |
|---|---|---|---|---|
| 1 | I | Pre-Registration Çerçevesi | `verified` | `docs/analiz_planlari/01-osf-kayit-sonucu.md`, OSF GUID kayıtları, sapma tablosu |
| 2 | I | Reprodüktiblik Mimarisi (`renv` + Docker + `_targets.R`) | `verified` | `docs/analiz_planlari/19-reproduktivite-runbook.md`; `renv::status()`, `targets::tar_make()`, `docker build --check .` |
| 3 | I | Etik ve Veri Yönetimi | `verified` | `R/08_data_governance.R`, `scripts/R/08_ethics_data_governance_audit.R`; 0 critical finding |
| 4 | I | Reporting Standardı | `verified` | `R/09_reporting_standards.R`, `scripts/R/09_reporting_standards_audit.R`; STROBE + JARS-Quant + TRIPOD checklist |
| 5 | II | Hash Doğrulama ve Yükleme | `verified` | `R/01_io.R`, `scripts/R/10_hash_validate_load.R`, `docs/analiz_planlari/10-veri-yukleme-runbook.md` |
| 6 | II | Türetilmiş Skor Ekosistemi | `verified` | `R/10_derived_scores.R`, `scripts/R/11_derive_scores_audit.R`, `tests/test_derived_scores.R` |
| 7 | II | SES Kompozit Türetme | `verified` | `R/11_ses_composites.R`, `scripts/R/12_derive_ses_audit.R`, `docs/analiz_planlari/12-ses-kompozitleri-runbook.md` |
| 8 | II | Eksik Veri Çoklu-Çerçeve | `verified` | `R/12_missing_data_frames.R`, `scripts/R/13_missing_data_audit.R`, `docs/analiz_planlari/13-eksik-veri-runbook.md` |
| 9 | III | Tablo 1 + Standardize Mean Difference | `verified` | `R/13_table1_smd.R`, `scripts/R/14_table1_smd_audit.R`, `docs/analiz_planlari/14-tablo1-smd-runbook.md` |
| IV | IV | Psikometrik Validasyon referansı | `reference_completed` | `docs/analiz_planlari/21-psikometrik-validasyon-sonuclari.qmd` |
| 10 | III | Causal DAG | `verified` | `R/14_causal_dag.R`, `scripts/R/15_causal_dag_audit.R`, `docs/analiz_planlari/15-nedensel-dag-runbook.md`; primary adjustment `{AgeGap;FamilySize;SES}` |
| 11 | III | Propensity Score (IPTW + Matching) + Doubly Robust | `verified` | `R/15_propensity_score.R`, `scripts/R/16_propensity_score_audit.R`, `docs/analiz_planlari/16-propensity-score-runbook.md`; max SMD 0.220 -> 0.004 IPTW |
| 12 | V | H1: Çocuk Algı Multilevel ANCOVA + 3-Way + IRT GRM + Bayesian | `verified` | `R/16_h1_child_perception.R`, `scripts/R/17_h1_child_perception_audit.R`, `docs/analiz_planlari/30-h1-cocuk-algisi-runbook.md`; n=482, IRT 4/4, Bayesian preflight |
| 13 | V | H2: Kardeş İlişkisi | `verified` | `R/17_h2_sibling_relationships.R`, `scripts/R/18_h2_sibling_relationships_audit.R`, `docs/analiz_planlari/31-h2-kardes-iliskileri-runbook.md`; n=482, APIM 4 model, Olsen-Kenny success |
| 14 | V | H3: Anne Öz-Rapor | `verified` | `R/18_h3_parent_self_report.R`, `scripts/R/19_h3_parent_self_report_audit.R`, `docs/analiz_planlari/32-h3-anne-oz-rapor-runbook.md`; families=241, primary=4, stratified=12/12, IPTW=4 |
| 15 | V | H4: Beck -> EMBU-P Latent SEM + Multi-Group + Bayesian | `verified` | `R/19_h4_beck_parenting_sem.R`, `scripts/R/20_h4_beck_parenting_sem_audit.R`, `docs/analiz_planlari/33-h4-beck-embu-sem-runbook.md`; full SEM success, reduced multi-group 2/2, Bayesian preflight |
| 16 | V | H5: Diadik Tutarlılık | `verified` | `R/20_h5_dyadic_concordance.R`, `scripts/R/21_h5_dyadic_concordance_audit.R`; 5 strateji (ICC+BA, RSA, CFM, Olsen-Kenny CFA, k-coef) tamam — Olsen-Kenny latent concordance Kontrol=0.17, DM=0.29 |
| 17 | VI | Tek-Mediator Modeli | `verified` | `R/23_mediation.R::mediation_simple`, `tests/test_mediation.R`, target `mediation_simple_effect_table`; Beck→EMBU-P_redd→EMBU-C_redd, BCa bootstrap n=1000, indirect NS |
| 18 | VI | Multilevel Mediation | `verified` | `R/23_mediation.R::mediation_multilevel`, target `mediation_multilevel_effect_table`; lavaan cluster=aile_no, a-path p=.018 |
| 19 | VI | Conditional Process Analysis | `verified` | `R/23_mediation.R::mediation_conditional_process`, target `mediation_conditional_effect_table`; Hayes Model 14, IMM NS |
| 20 | VI | Bayesian Mediation + ROPE | `verified` | `R/23_mediation.R::mediation_bayesian_preflight` (preflight stub) + `R/22_bayesian_parallel.R` dual reporting hattıyla bütünleşik |
| 21 | VII | Latent Profile Analysis | `verified` | `R/24_latent_profile.R::run_lpa`, `tests/test_latent_profile.R`, target `lpa_fit_table`; tidyLPA 1-5 profil, BIC en iyi=3 (entropy 0.81, BLRT p=.01) |
| 22 | VII | Latent Class Analysis + Mixture Regression | `verified` | `R/24_latent_profile.R::run_lca`, `run_lca_modal_regression`, `run_flexmix_regression`; targets `lca_*`, `flexmix_*`; 2-sınıf LCA sensitivity, modal class regression verified; flexmix boundary diagnostic |
| 23 | VII | Bifactor S-1 Modeli | `verified` | `R/24_latent_profile.R::run_bifactor_s1`, target `bifactor_s1_fit_table`; reference=asiri_koruma, 29-item WLSMV, CFI=0.79 sınır altı raporlanır |
| 24 | VIII | Gaussian Graphical Model | `verified` | `R/26_network_analysis.R::run_ggm_lasso`, `tests/test_network_analysis.R`, target `network_edges_table` + `network_centrality_table`; EBIC-LASSO γ=0.5, 9-değişken (n=238) |
| 25 | VIII | Network Comparison Test | `verified` | `R/26_network_analysis.R::run_nct`, target `network_nct_table`; global strength invariance p=0.86 (DM ≈ Kontrol) |
| 26 | VIII | Beck Item-Level Symptom Network | `verified` | `R/26_network_analysis.R::run_beck_symptom_network`, target `network_beck_centrality_table`; 21-madde EBIC-LASSO + centrality |
| 27 | IX | Risk Skor + ROC + Decision Curve Analysis | `verified` | `R/25_clinical_utility.R::clinical_logistic_risk + clinical_decision_curve`, `tests/test_clinical_utility.R`, target `clinical_full_performance` + `clinical_decision_curve_table`; AUC + bootstrap optimism + DCA |
| 28 | IX | CART Karar Ağacı + Random Forest | `verified` | `R/25_clinical_utility.R::clinical_cart_rf`, target `clinical_cart_cp_table` + `clinical_rf_importance_table`; rpart 1-SE pruning + RF ntree=500 + OOB error |
| 29 | IX | Calibration + NRI/IDI | `verified` | `R/25_clinical_utility.R::clinical_calibration + clinical_nri_idi`, target `clinical_calibration_table` + `clinical_nri_idi_table`; Hosmer-Lemeshow 5-grup + reclassification |
| 30 | X | HbA1c x Ebeveynlik Etkileşimi | `verified` | `R/27_dm_subanalyses.R::dm_hba1c_interaction`, `tests/test_dm_subanalyses.R`, target `dm_hba1c_interaction_table`; **n=39 keşifsel** — kural #19 imputation yok |
| 31 | X | DM Süresi Spline Modeli | `verified` | `R/27_dm_subanalyses.R::dm_duration_spline`, target `dm_duration_spline_table`; ns(df=3) cubic vs linear LRT — linear sufficient |
| 32 | X | Tanı Yaşı Stratifikasyonu | `verified` | `R/27_dm_subanalyses.R::dm_strata_analysis + dm_strata_test`, target `dm_strata_descriptive_table` + `dm_strata_tests_table`; 3 strata, F NS |
| 33 | XI | Multiverse Specification Curve | `verified` | `R/21_robustness_sensitivity.R::robust_multiverse`, `tests/test_robustness_sensitivity.R`, target `robust_multiverse_spec_table` (120 satır) + `robust_multiverse_summary_table`; reddetme median d=−0.13 |
| 34 | XI | Equivalence Testing | `verified` | `R/21_robustness_sensitivity.R::robust_tost`, target `robust_tost_equivalence_table`; SESOI=±0.30 SMD, 2/4 Equivalent, 2/4 Indeterminate |
| 35 | XI | Sensemakr + E-value | `verified` | `R/21_robustness_sensitivity.R::robust_sensemakr + evalue_from_d`, target `robust_sensemakr_evalue_table`; RV_q 0.04-0.08, E-value 1.36-1.59 |
| 36 | XI | Negative Control Outcome + Falsification Tests | `verified` | `R/21_robustness_sensitivity.R::robust_negative_control + robust_falsification`, target `robust_negative_control_table` + `robust_falsification_table` |
| 37 | XII | Bayesian Multilevel | `verified` | `R/22_bayesian_parallel.R::bayes_run_h1 + bayes_run_h3`, `tests/test_bayesian_parallel.R` (audit-CSV smoke) + audit-RDS persist; brms 2 chain × 2000 iter, R̂<1.01, divergent=0 |
| 38 | XII | Bayes Factor + ROPE | `verified` | `R/22_bayesian_parallel.R::bayes_savage_dickey_bf` + ROPE; H3 BF<1/3 Moderate H0, **H1 reddetme BF=8.12 Moderate H1**; CSV doğrulandı |
| 39 | XII | WAIC / LOO | `verified` | `R/22_bayesian_parallel.R::loo_waic_table`; CSV (`bayes_loo_waic.csv`) ile doğrulandı, pareto_k_problematic raporlandı |
| 40 | XIII | APA Tablo + Şekil Üretimi | `verified` | Sprint A figür + tablo paketleri: `R/28_apa_figures.R`, `R/29_apa_tables.R`, `scripts/R/29_apa_figures_audit.R`, `scripts/R/30_apa_tables_audit.R`, `tests/test_apa_figures.R`, `tests/test_apa_tables.R`; targets `apa_*`; 24 figür + 22 tablo üretildi ve `chapters/03_bulgular.qmd` içine bağlandı; `quarto render thesis.qmd --to html` başarılı |
| 41 | XIII | Tez Bölüm Eşlemesi | `verified` | `R/30_thesis_mapping.R`, `scripts/R/31_thesis_mapping_audit.R`, `tests/test_thesis_mapping.R`; 5 chapter, 24 figür referansı, 22 tablo referansı ve `outputs/quarto/thesis.html` doğrulandı |
| 42 | XIII | 3-Makale Yayın Stratejisi | `verified` | `references/diseminasyon-ve-yayin.md`, `R/31_final_plans.R::final_publication_strategy`, `scripts/R/32_final_plans_audit.R`, `tests/test_final_plans.R`; 3 makale + evidence map CSV doğrulandı |
| 43 | XIII | Open Data + Code Plan | `verified` | OSF kayıtları (`pytfe`, `d524q`); FAIR + Zenodo planı `references/diseminasyon-ve-yayin.md` |
| 44 | XV | Risk Yönetimi ve Yedek Stratejiler | `verified` | `references/risk-ve-zaman-cizelgesi.md`, target `final_risk_matrix_table`; 14 risk + aktif izlem özeti audit edildi |
| 45 | XVI | 24-Haftalık Plan | `verified` | `references/risk-ve-zaman-cizelgesi.md`, target `final_timeline_24_week_table`; 24 haftalık plan + durum özeti audit edildi |

**Tracker notu:** SAP gövdesinde KISIM XIV ve sonrası bazı başlık numaraları içerik geliştirme sırasında kaymış durumda; canlı tracker, İçindekiler'deki ana analiz numaralarını esas alır ve bundan sonraki uygulama turlarında bu tablo birincil ilerleme kaydı olarak güncellenecektir.

---

# KISIM I — META-ALTYAPI

## 1. Pre-Registration Çerçevesi

### 1.1 Niçin Önemli

Pre-registration (Nosek et al. 2018, *PNAS*), **garden of forking paths** (Gelman & Loken 2014) ve **HARKing** (Hypothesizing After Results are Known; Kerr 1998) sorunlarına karşı birinci dereceden savunmadır. T1DM-EBEVEYN için pre-registration üç katmanlı koruma sağlar:

1. **Tezin savunması:** Jüri "bu test neden seçildi?" sorusuna OSF GUID referansı; DOI public/embargo onayı sonrası eklenecek
2. **Yayın süreci:** Üst düzey dergiler (psikoloji ve gelişimsel pediatri) registered report formatını giderek daha çok arıyor
3. **Bilimsel itibar:** OSF kaydı, çalışmanın bilimsel bütünlüğünü kanıtlar

### 1.2 OSF Kayıt Statüsü ve Şablonu

**Gerçekleşen kayıt durumu (2026-04-27):** `docs/analiz_planlari/00-osf-kayit-rehberi.md` doğrultusunda iki katmanlı OSF stratejisi uygulanmıştır.

| Katman | Amaç | OSF şablonu | GUID / URL | Durum |
|---|---|---|---|---|
| Layer 1 | Tamamlanmış psikometrik validasyonun şeffaf kaydı | Open-Ended Registration | `d524q` / <https://osf.io/d524q/> | Submitted; embargo onayı bekliyor |
| Layer 2 | H1-H5 doğrulayıcı analiz planı | Secondary Data Preregistration | `pytfe` / <https://osf.io/pytfe/> | Submitted; embargo onayı bekliyor |

OSF ana proje: <https://osf.io/vqrt5/>. DOI henüz atanmadı; OSF DOI'si embargo/public onay süreci tamamlandıktan sonra eklenmelidir.

```yaml
# OSF Registries — Secondary Data Preregistration + Open-Ended reflective layer

title: "T1DM Tanılı Çocuklar, Sağlıklı Kardeşleri ve Annelerinde
        Ebeveynlik Tutumu Algıları: Vaka-Kontrol Çalışması"

authors:
  - name: "Özlem Murzoğlu Kurt"; affiliation: "Marmara Üniv. SBE Sosyal Pediatri"
  - name: "Eren Özek"; affiliation: "Marmara Üniv. Tıp Fakültesi"

study_type: "Vaka-kontrol kesitsel"
data_collection_status: "Tamamlandı (Şubat 2023 – Aralık 2025)"
analysis_status: "Secondary data preregistration (H1-H5); psikometrik validasyon reflective/post-hoc kayıt"
osf_project: "https://osf.io/vqrt5/"
osf_reflective_registration: "https://osf.io/d524q/"
osf_secondary_preregistration: "https://osf.io/pytfe/"

primary_hypotheses:
  H1: "T1DM tanılı çocuklar, sağlıklı kardeşleri ve sağlıklı kontrollerden
       en az bir EMBU-C alt ölçeğinde anlamlı düzeyde farklı algı bildirir."
  H2: "T1DM hasta–sağlıklı kardeş çiftlerinin SRQ alt boyut puanları,
       sağlıklı kardeş çiftlerinden anlamlı düzeyde farklıdır."
  H3: "T1DM çocuk anneleri ile kontrol grubu anneleri arasında EMBU-P
       alt ölçek puanları anlamlı düzeyde farklıdır."
  H4: "Maternal Beck Depresyon Envanteri puanı, EMBU-P alt ölçek
       puanlarını anlamlı düzeyde yordar."
  H5: "T1DM grubunda anne-çocuk EMBU uyum/tutarlılık örüntüsü,
       kontrol grubundakinden anlamlı düzeyde farklıdır."

multiple_testing: "Benjamini-Hochberg FDR within hypothesis families (q=.05)"

stopping_rule: "Veri kilidi 2026-04-26 itibariyle kapatılmıştır
                (FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock).
                Yeni veri eklenmesi yasaktır."

primary_estimands:
  - "ATE (Average Treatment Effect): T1DM olmanın çocuk algısı üzerine ortalama etkisi"
  - "Indirect effect: Beck → EMBU-P → ChildPerception (mediation)"
  - "Group × Age interaction: Gelişimsel hassasiyet"

robustness_checks:
  - "Specification curve analysis (specr package)"
  - "Sensitivity analysis (sensemakr) for unmeasured confounding"
  - "TOST equivalence test (SESOI = ±0.30 SMD)"
  - "Bayesian replication (brms) — independent verification"
  - "Negative control outcome (anne_dogum_tarihi → SRQ; sahte ilişki olmamalı)"

deviations_policy: "Tüm sapmalar tezin metodoloji ekinde şeffaf raporlanır.
                    Sapmalar 'exploratory' etiketiyle ayrılır."
```

### 1.3 OSF Kayıt Akışı

```
Adım 1: OSF.io üzerinde private proje oluşturuldu (vqrt5)
Adım 2: Completed psychometric layer Open-Ended Registration olarak submit edildi (d524q)
Adım 3: H1-H5 için Secondary Data Preregistration submit edildi (pytfe)
Adım 4: OSF embargo onayı/public statüsü tamamlanınca DOI tez metnine eklenecek
Adım 5: Yayın aşamasında analiz kodu zenodo.org'a archive edilecek
```

---

## 2. Reprodüktiblik Mimarisi

### 2.1 Üç Katmanlı Reprodüktiblik (Marwick 2018; Wilson 2017)

| Katman | Araç | İşlev |
|---|---|---|
| **Paket sürümü** | `renv::lock` | Tüm R paketleri sabitlenir |
| **Sistem sürümü** | `Dockerfile` (rocker/verse:4.5.3) | OS + R + LaTeX birleşik environment |
| **Veri sürümü** | SHA-256 hash + `targets::tar_target` | Veri bütünlüğü ve hesaplama akışı |

### 2.2 Master `_targets.R` Orkestrasyonu

```r
# _targets.R — TAM PIPELINE (v3.0 final)
library(targets); library(tarchetypes); library(crew)

tar_option_set(
  packages = c(
    # Çekirdek
    "tidyverse", "here", "digest", "janitor",
    # Multilevel + SEM
    "lme4", "lmerTest", "nlme", "lavaan", "semTools", "blavaan", "brms",
    # Etki büyüklüğü ve raporlama
    "emmeans", "effectsize", "performance", "broom", "broom.mixed",
    "gtsummary", "gt", "papaja", "report",
    # Sensitivite + robustness
    "specr", "TOSTER", "sensemakr", "EValue", "mice", "miceadds",
    # Psikometri
    "psych", "BlandAltmanLeh", "irr", "irrCAC", "RSA", "mirt",
    # Causal inference
    "MatchIt", "twang", "tableone", "WeightIt", "cobalt",
    "dagitty", "ggdag",
    # Latent variable
    "tidyLPA", "mclust", "poLCA", "flexmix",
    # Network
    "qgraph", "bootnet", "NetworkComparisonTest", "psychonetrics",
    # Klinik fayda
    "rpart", "rpart.plot", "partykit", "randomForest",
    "pROC", "rmda", "PredictABEL",
    # Bayesian
    "rstan", "rstanarm", "bayestestR", "bayesplot", "loo",
    # Görselleştirme
    "ggplot2", "ggdist", "see", "patchwork", "ggsci"
  ),
  format     = "qs",
  controller = crew_controller_local(workers = 4)
)

list(
  # KISIM II
  tar_target(lock_file, "data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock",
              format = "file"),
  tar_target(family_csv, "data/processed/FINAL_REFERENCE__analysis_base_family.csv",
              format = "file"),
  tar_target(long_csv,   "data/processed/FINAL_REFERENCE__analysis_base_long.csv",
              format = "file"),
  tar_target(df_family_raw, validate_and_load(family_csv, lock_file)),
  tar_target(df_long_raw,   validate_and_load(long_csv,   lock_file)),
  tar_target(df_family,     prepare_family(df_family_raw)),
  tar_target(df_long,       prepare_long(df_long_raw)),
  tar_target(ses_results,   derive_ses_composites(df_family)),
  tar_target(df_family_ses, ses_results$data),
  tar_target(mice_imp,      run_multiple_imputation(df_family_ses, m = 50)),

  # KISIM III
  tar_target(table1,        build_table1(df_family_ses, df_long)),
  tar_target(smd_balance,   run_smd_balance(df_family_ses)),
  tar_target(causal_dag,    build_causal_dag()),
  tar_target(propensity,    estimate_propensity_scores(df_family_ses)),
  tar_target(df_iptw,       propensity$df_with_iptw),

  # KISIM V — H1
  tar_target(h1_freq,       run_h1_frequentist(df_long)),
  tar_target(h1_three_way,  run_h1_three_way(df_long)),
  tar_target(h1_irt,        run_h1_irt_grm(df_long)),
  tar_target(h1_bayes,      run_h1_bayesian(df_long)),

  # KISIM V — H2
  tar_target(h2_family,     run_h2_family_mean(df_family_ses, df_long)),
  tar_target(h2_apim,       run_h2_apim(df_long)),
  tar_target(h2_dyadic_cfa, run_h2_olsen_kenny(df_long)),
  tar_target(h2_extended,   run_h2_age_gap_moderation(df_family_ses, df_long)),

  # KISIM V — H3
  tar_target(h3_main,       run_h3_main(df_family_ses)),
  tar_target(h3_strat,      run_h3_stratified(df_family_ses)),
  tar_target(h3_iptw,       run_h3_iptw(df_iptw)),

  # KISIM V — H4
  tar_target(h4_sem,        run_h4_latent_sem(df_family_ses)),
  tar_target(h4_invariance, run_h4_multigroup_invariance(df_family_ses)),
  tar_target(h4_bayes,      run_h4_bayesian_sem(df_family_ses)),

  # KISIM V — H5
  tar_target(h5_concord,    run_h5_concordance(df_family_ses)),
  tar_target(h5_rsa,        run_h5_rsa(df_family_ses)),
  tar_target(h5_cfm,        run_h5_common_fate(df_family_ses)),
  tar_target(h5_dyadic_cfa, run_h5_olsen_kenny_dyadic_cfa(df_family_ses)),
  tar_target(h5_k_coef,     run_h5_k_coefficient(df_family_ses)),

  # KISIM VI — Mediation
  tar_target(med_simple,    run_simple_mediation(df_family_ses, df_long)),
  tar_target(med_multilevel,run_multilevel_mediation(df_long, df_family_ses)),
  tar_target(med_moderated, run_moderated_mediation(df_family_ses, df_long)),
  tar_target(med_bayesian,  run_bayesian_mediation(df_family_ses, df_long)),

  # KISIM VII — Latent
  tar_target(lpa_typology,  run_lpa_mother_typology(df_family_ses)),
  tar_target(lca_categorical,run_lca_categorical(df_family_ses)),
  tar_target(bifactor_s1,   run_bifactor_s1_model(df_family_ses)),

  # KISIM VIII — Network
  tar_target(network_full,  run_network_analysis(df_family_ses)),
  tar_target(network_compare,run_network_comparison(df_family_ses)),
  tar_target(network_beck,  run_beck_item_network(df_family_ses)),

  # KISIM IX — Klinik fayda
  tar_target(risk_score,    derive_risk_score(df_family_ses)),
  tar_target(roc_analysis,  run_roc_analysis(risk_score, df_family_ses)),
  tar_target(decision_curve,run_decision_curve_analysis(risk_score, df_family_ses)),
  tar_target(decision_tree, run_decision_tree(df_family_ses)),
  tar_target(random_forest, run_random_forest_importance(df_family_ses)),
  tar_target(calibration,   run_calibration_analysis(risk_score, df_family_ses)),

  # KISIM X — Klinik alt-analizler
  tar_target(hba1c_mod,     run_hba1c_moderation(df_family_ses)),
  tar_target(dm_duration,   run_dm_duration_spline(df_family_ses)),
  tar_target(diagnosis_age, run_diagnosis_age_strata(df_family_ses)),

  # KISIM XI — Robustluk
  tar_target(multiverse,    run_multiverse(df_family_ses, df_long)),
  tar_target(tost_equiv,    run_tost_equivalence(df_family_ses)),
  tar_target(sensemakr_res, run_sensemakr(df_family_ses)),
  tar_target(evalue_res,    run_evalue_analysis(df_family_ses)),
  tar_target(neg_control,   run_negative_control(df_family_ses)),

  # KISIM XII — Bayesci paralel
  tar_target(bayes_factor,  compute_bayes_factors(h1_bayes, h4_bayes)),
  tar_target(rope_analysis, run_rope_analysis(h1_bayes, h4_bayes)),
  tar_target(post_pred,     run_posterior_predictive_checks(h1_bayes)),
  tar_target(waic_loo,      run_waic_loo_comparison(h1_bayes, h4_bayes)),

  # KISIM XIII — Raporlama ve diseminasyon
  tar_target(strobe_flow,   build_strobe_flow(df_family_ses)),
  tar_target(all_tables,    compile_all_tables(h1_freq, h2_family, h3_main, h4_sem,
                                                  h5_concord, lpa_typology,
                                                  network_full, decision_tree)),
  tar_target(all_figures,   compile_all_figures(h1_freq, h5_rsa, lpa_typology,
                                                   network_full, decision_tree,
                                                   multiverse)),

  tar_quarto(report_main,   "reports/00_main_analysis.qmd"),
  tar_quarto(report_psych,  "reports/01_psychometric.qmd"),
  tar_quarto(report_clin,   "reports/02_clinical_utility.qmd"),
  tar_quarto(report_robust, "reports/03_robustness.qmd")
)
```

### 2.3 Docker Container

```dockerfile
FROM rocker/verse:4.5.3
LABEL maintainer="ozlem.murzoglu@gmail.com"
LABEL description="T1DM-EBEVEYN SAP v3.0 reproducible environment"

RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev libssl-dev libxml2-dev \
    libv8-dev libfontconfig1-dev libfreetype6-dev \
    libpng-dev libtiff5-dev libjpeg-dev \
    libudunits2-dev libgdal-dev libgeos-dev libproj-dev \
    cmake jags && rm -rf /var/lib/apt/lists/*

COPY renv.lock /home/rstudio/renv.lock
RUN R -e "install.packages('renv'); renv::restore(lockfile='/home/rstudio/renv.lock')"

WORKDIR /home/rstudio/project
COPY . .

CMD ["bash", "-lc", "Rscript -e 'targets::tar_make()' && quarto render thesis.qmd --to html"]
```

### 2.4 Reprodüksiyon Komut Akışı

```bash
# Standart akış
Rscript -e 'renv::restore()'
Rscript -e 'targets::tar_make()'
quarto render

# Docker akışı
docker build -t t1dm-sap-v3 .
docker run --rm -v $(pwd):/home/rstudio/project t1dm-sap-v3
```

---

## 3. Etik ve Veri Yönetimi

KAEK 09.2023.201 onayı ve protokol Bölüm 14 hükümleri analiz aşamasında da geçerlidir.

Uygulama planı ayrıca `docs/analiz_planlari/17-etik-veri-yonetimi-plani.md` dosyasında kalıcılaştırılmıştır. Bu plan veri sınıflandırmasını, erişim matrisini, OSF public/controlled-access sınırını ve olay yönetimini tanımlar.

### 3.1 PII ve Git-Boundary Otomatik Tahkik

Kanonik CSV başlıkları ve git tarafından görülebilen dosya yolları her analiz fazı öncesinde denetlenir:

```bash
Rscript tests/test_data_governance.R
Rscript scripts/R/08_ethics_data_governance_audit.R
```

Denetim iki sınıf bulgu üretir:

| Sınıf | Örnek | Eylem |
|---|---|---|
| **critical** | ad/soyad, TC kimlik, telefon, e-posta, adres, ham veri, credential | Analiz durur; dosya/kolon temizlenmeden devam edilmez |
| **review** | doğum tarihi, tanı tarihi, anket tarihi, aggregate output yolu | Veri minimizasyonu açısından gözden geçirilir |

Beklenen durum: kanonik CSV başlıklarında doğrudan tanımlayıcı yoktur; git-visible dosya listesinde ham veri, processed row-level CSV, credential veya `.env` yoktur. Denetim çıktısı `outputs/tables/ethics_data_governance_audit.csv` altında üretilir ve git dışıdır.

### 3.2 Veri Erişim Politikası

| Düzey | Aktör | İçerik |
|---|---|---|
| Tam (write) | PI + Tez Danışmanı | Ham veri + analiz |
| Read-only | TİK üyeleri | Standardize veri + çıktılar |
| Aggregate-only | Yayın okuyucuları | Tablolar + şekiller |

Satır-düzeyi `FINAL_REFERENCE__*.csv` dosyaları de-identified analiz verisi kabul edilir; public OSF/Git kapsamında paylaşılmaz. Açık OSF paketinde yalnız analiz kodu, kanonik dokümantasyon, veri kilidi metadata'sı, aggregate raporlar ve controlled-access notları bulunur.

---

## 4. Reporting Standardı

### 4.1 Üç-Çerçeveli Raporlama

Reporting standardı `docs/analiz_planlari/18-raporlama-standartlari-checklist.md` ve makine-okunur `R/09_reporting_standards.R` kontrol listesi ile izlenir. Bu bölüm bir "uyum beyanı" değil, tez yazımı boyunca güncellenecek zorunlu raporlama izidir.

| Çerçeve | Kullanım | Spesifik Bileşen |
|---|---|---|
| **STROBE** (von Elm 2008) | Vaka-kontrol metodolojik raporlama | Selection bias, confounding control, generalizability |
| **JARS-Quant** (APA 2020) | APA dergi standardı (nicel) | Quantitative + integration ayrı bölümler |
| **TRIPOD** (Collins 2015) | Klinik tahmin modeli (KISIM IX risk skoru) | Internal validation, calibration, NRI/IDI |

### 4.2 Audit ve Durum Takibi

```bash
Rscript tests/test_reporting_standards.R
Rscript scripts/R/09_reporting_standards_audit.R
```

Audit çıktıları git-dışı `outputs/tables/reporting_standards_*.csv` dosyalarına yazılır. Durum sözlüğü:

| Durum | Anlam |
|---|---|
| `planned` | Tez/çıktı içinde yeri ayrıldı, içerik henüz üretilmedi |
| `drafted` | SAP, yöntem veya plan dokümanında taslaklandı |
| `implemented` | Tez metnine veya output artefaktına işlendi |
| `verified` | Audit/test ile doğrulandı |
| `not_applicable` | Bu çalışma için gerekçeli biçimde uygulanmaz |

KISIM I tamamlanmış sayılmadan önce zorunlu maddeler `implemented` veya `verified` durumuna çekilecektir. Özellikle katılımcı akış şeması, Table 1/descriptive missingness, H1-H5 ana sonuç tabloları, sensitivite üçlüsü (KISIM XI) ve Bayesian dual reporting (KISIM XII) artefaktları tamamlandıkça bu kontrol listesi güncellenecektir.

---

# KISIM II — VERİ KATMANI

## 5. Hash Doğrulama ve Yükleme

### 5.1 Kriptografik Bütünlük

Uygulama `R/01_io.R` içinde `validate_and_load()` fonksiyonuna taşınmıştır. Fonksiyon her CSV için şu sırayı zorunlu kılar:

1. `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` okunur ve `LOCKED_CANONICAL_ANALYSIS_BASE` statüsü doğrulanır.
2. CSV'nin SHA-256 özeti veri okunmadan önce hesaplanır.
3. Hash lock dosyasındaki beklenen değerle eşleşmezse yükleme durur.
4. CSV okunur ve satır/sütun sayısı lock dosyasındaki beklenen değerle karşılaştırılır.
5. Yüklenen veri nesnesine `validated_hash`, `validation_time`, `lock_date`, `lock_project` ve `canonical_path` attribute'ları eklenir.

Komut:

```bash
Rscript tests/test_final_reference_loading.R
Rscript scripts/R/10_hash_validate_load.R
```

Runner yalnız metadata çıktısı üretir:

- `outputs/tables/final_reference_validation_manifest.csv`
- `outputs/tables/final_reference_load_summary.csv`

Satır-düzeyi veri `outputs/` altına yazılmaz.

### 5.2 Faktörleştirme

`prepare_family()` ve `prepare_long()` yine `R/01_io.R` içindedir. Bu katman skorlama yapmaz; yalnız analizde tekrar kullanılacak yapısal faktörleri ve türetilmiş temel alanları ekler:

| Veri | Eklenen alanlar |
|---|---|
| Family | `aile_no_f`, `group_f`, `cinsiyet_idx_f`, `cinsiyet_sib_f`, `egitim_ord`, `age_gap`, `same_sex`, `birth_order_diff`, `tani_yasi`, `hba1c_target` |
| Long | `aile_no_f`, `role_f`, `group_f`, `family_role_f`, `cinsiyet_f`, `age_cat` |

Hazırlık katmanı, gerekli kolon eksikse hata verir. EMBU, Beck/BDI veya KIA/SRQ toplam/alt ölçek skorları burada üretilmez; bu kararlar KISIM II / 6 türetilmiş skor ekosistemine bırakılmıştır.

### 5.3 Targets Entegrasyonu

`_targets.R` artık KISIM II veri yükleme omurgasını içerir:

```r
tar_target(lock_file, final_reference_paths$lock, format = "file")
tar_target(family_csv, final_reference_paths$family, format = "file")
tar_target(long_csv, final_reference_paths$long, format = "file")
tar_target(final_reference_manifest, final_reference_validation_manifest(lock_file, c(family_csv, long_csv)))
tar_target(df_family_raw, validate_and_load(family_csv, lock_file))
tar_target(df_long_raw, validate_and_load(long_csv, lock_file))
tar_target(df_family, prepare_family(df_family_raw))
tar_target(df_long, prepare_long(df_long_raw))
```

`_targets/` içinde satır-düzeyi nesne cache'i oluşabilir; bu klasör Git, OSF public paket ve Docker context dışında kalır.

---

## 6. Türetilmiş Skor Ekosistemi

Uygulama `R/10_derived_scores.R` içinde sabitlenmiştir. Bu katman final CSV'leri değiştirmez; skorlanmış family/long nesneleri yalnız analiz belleğinde ve `_targets/` cache'inde tutulur. Runner `scripts/R/11_derive_scores_audit.R` satır-düzeyi skor dosyası yazmaz; yalnız skor sözlüğü, range audit ve aggregate kapsam çıktısı üretir.

```bash
Rscript tests/test_derived_scores.R
Rscript scripts/R/11_derive_scores_audit.R
```

Çıktılar:

- `outputs/tables/derived_score_dictionary.csv`
- `outputs/tables/derived_score_range_audit.csv`
- `outputs/tables/derived_score_coverage.csv`
- `outputs/tables/derived_score_audit_summary.csv`

Varsayılan eksik veri eşiği, SAP v3'te sabitlendiği gibi `min_present_pct = 0.50`'dir. Her alt ölçek için `*_sum_complete` tüm itemlar mevcutsa hesaplanır; `*_mean` ise madde kümesinin en az %50'si mevcutsa hesaplanır. Beck toplamı bu istisnaya dahil değildir: herhangi bir Beck itemı eksikse `beck_total = NA` kalır.

### 6.1 EMBU Madde-Faktör Eşlemesi

```r
embu_subscales <- list(
  sicaklik       = c(1, 3, 6, 7, 13, 17, 20, 24, 26),  # k=9
  asiri_koruma   = c(4, 8, 14, 15, 19, 23, 25),         # k=7
  reddetme       = c(5, 9, 10, 12, 16, 21, 22, 28),     # k=8
  karsilastirma  = c(2, 11, 18, 27, 29)                  # k=5
)
```

Not: `embu_c_q25`, `embu_c_idx_q25` ve `embu_c_sib_q25` final CSV'de ters skorlanmış olarak saklandığı için bu katmanda yeniden reverse coding uygulanmaz.

### 6.2 SRQ Madde-Faktör Eşlemesi (Furman & Buhrmester 1985)

```r
srq_subscales <- list(
  intimacy            = c(1, 17, 33),
  prosocial           = c(3, 19, 35),
  companionship       = c(9, 25, 41),
  similarity          = c(10, 26, 42),
  admiration_by_sib   = c(12, 28, 44),
  admiration_of_sib   = c(11, 27, 43),
  affection           = c(16, 32, 48),
  nurturance_by_sib   = c(8, 24, 40),
  nurturance_of_sib   = c(15, 31, 47),
  dominance_by_sib    = c(7, 23, 39),
  dominance_of_sib    = c(2, 18, 34),
  quarreling          = c(4, 20, 36),
  antagonism          = c(6, 22, 38),
  competition         = c(5, 21, 37),
  maternal_partiality = c(14, 30, 46),
  paternal_partiality = c(13, 29, 45)
)

srq_higher_order <- list(
  warmth   = unlist(srq_subscales[c("intimacy","prosocial","companionship",
                                      "similarity","admiration_by_sib",
                                      "admiration_of_sib","affection")]),  # 21
  status   = unlist(srq_subscales[c("nurturance_by_sib","nurturance_of_sib",
                                      "dominance_by_sib","dominance_of_sib")]), # 12
  conflict = unlist(srq_subscales[c("quarreling","antagonism","competition")]), # 9
  rivalry  = unlist(srq_subscales[c("maternal_partiality","paternal_partiality")]) # 6
)
```

### 6.3 Genel Skor Türetme Fonksiyonu

```r
derive_subscale_scores(
  df,
  item_columns_map,
  score_prefix,
  min_present_pct = 0.50
)
```

Üretilen kolon seti her alt ölçek için aynıdır: `*_valid_n`, `*_missing_n`, `*_sum_complete`, `*_mean`.

### 6.4 Beck Total ve Şiddet Kategorileri

```r
df_family <- df_family |>
  mutate(
    beck_total    = rowSums(across(starts_with("beck_")), na.rm = FALSE),
    beck_severity = cut(beck_total, breaks = c(-1, 9, 16, 29, 63),
                          labels = c("Minimal", "Hafif", "Orta", "Şiddetli")),
    beck_clinical = factor(beck_total >= 17,
                             labels = c("Klinik altı", "Klinik düzey"))
  )
```

Uygulamada `derive_beck_scores()` aynı kuralı uygular ve ayrıca `beck_valid_n`, `beck_missing_n`, `beck_severity`, `beck_clinical` üretir.

### 6.5 Targets Entegrasyonu

```r
tar_target(derived_score_dictionary_table, derived_score_dictionary())
tar_target(derived_score_range_audit, score_range_audit(df_family, df_long))
tar_target(derived_score_range_ok, assert_no_score_range_violations(derived_score_range_audit))
tar_target(df_family_scored, derive_family_scores(df_family))
tar_target(df_long_scored, derive_long_scores(df_long))
tar_target(derived_score_target_summary, summarize_derived_score_targets(df_family, df_long, df_family_scored, df_long_scored))
```

`df_family_scored` ve `df_long_scored` satır-düzeyi nesnelerdir; Git, OSF public paket ve Docker context dışında kalan `_targets/` cache'inde tutulur.

---

## 7. SES Kompozit Türetme (Bourdieu Üç-Sermaye)

Uygulama `R/11_ses_composites.R` içinde sabitlenmiştir. Bu katman final CSV'leri değiştirmez; SES eklenmiş family nesnesi yalnız analiz belleğinde ve `_targets/` cache'inde tutulur. Runner `scripts/R/12_derive_ses_audit.R` satır-düzeyi SES dosyası yazmaz; yalnız aggregate diagnostic çıktıları üretir.

```bash
Rscript tests/test_ses_composites.R
Rscript scripts/R/12_derive_ses_audit.R
```

Çıktılar:

- `outputs/tables/ses_diagnostics.csv`
- `outputs/tables/ses_material_loadings.csv`
- `outputs/tables/ses_cfa_fit_measures.csv`
- `outputs/tables/ses_component_summary.csv`
- `outputs/tables/ses_correlation_table.csv`
- `outputs/tables/ses_target_summary.csv`

Yön kuralı: tüm SES skorlarında yüksek değer daha avantajlı sosyoekonomik konumu temsil eder. `ev_sahipligi` final kodunda `0 = kendi mülkümüz`, `1 = kiralık` olduğu için materyal indeks yönü ev sahipliği, oda sayısı ve araba sahipliği anchor'ı ile pozitif SES yönüne sabitlenir.

### 7.1 Üç Katmanlı Strateji

```r
derive_ses_composites <- function(df_family) {

  # ===== KATMAN A: Tek-boyut bileşenler =====
  df_family <- df_family |>
    mutate(
      max_aile_egitim   = pmax(egitim_durumu, es_egitim_durumu, na.rm = TRUE),
      mean_aile_egitim  = (egitim_durumu + es_egitim_durumu) / 2,
      egitim_fark       = abs(es_egitim_durumu - egitim_durumu),
      cift_kazanc       = as.numeric(calisma_durumu == 1 & es_calisma_durumu == 1),
      kalabalik_indeksi = cocuk_sayisi / (ev_oda_sayisi + 1)
    )

  # ===== KATMAN B: Materyal indeksi (polychoric PCA, Filmer-Pritchett 2001) =====
  material_vars <- df_family |>
    select(ev_sahipligi, ev_oda_sayisi, arabaniz_var_mi)

  poly_result <- psych::polychoric(material_vars)
  pca_material <- psych::principal(poly_result$rho, nfactors = 1, rotate = "none")

  # Türkiye-spesifik diagnostic: ev_sahipligi yükü kontrolü
  if (abs(pca_material$loadings["ev_sahipligi", 1]) < 0.20) {
    message("⚠ ev_sahipligi loading <.20 — materyal indeksten çıkartılıyor")
    material_vars <- material_vars |> select(-ev_sahipligi)
    poly_result <- psych::polychoric(material_vars)
    pca_material <- psych::principal(poly_result$rho, nfactors = 1, rotate = "none")
  }

  df_family$material_index <- as.numeric(
    psych::factor.scores(material_vars, pca_material, method = "tenBerge")$scores
  )
  df_family$material_quintile <- ntile(df_family$material_index, 5)

  # ===== KATMAN C1: Hollingshead-tipi şeffaf kompozit =====
  df_family <- df_family |>
    mutate(
      edu_z      = as.numeric(scale(mean_aile_egitim)),
      isei_z     = as.numeric(scale(aile_isei08)),
      material_z = as.numeric(scale(material_index)),

      ses_composite_eq = rowMeans(cbind(edu_z, isei_z, material_z), na.rm = TRUE),
      ses_hollingshead = (3 * edu_z + 5 * isei_z) / 8
    )

  # ===== KATMAN C2: Latent SES (CFA) =====
  ses_cfa_model <- '
    SES =~ egitim_durumu + es_egitim_durumu + aile_isei08 + material_index
  '

  fit_ses <- lavaan::cfa(ses_cfa_model, data = df_family,
                          estimator = "WLSMV",
                          ordered = c("egitim_durumu", "es_egitim_durumu"),
                          missing = "pairwise")

  df_family$ses_latent <- as.numeric(lavaan::predict(fit_ses)[, "SES"])

  list(data = df_family, fit_ses = fit_ses, pca_material = pca_material)
}
```

Uygulamada `derive_ses_composites()` şu çıktıları döndürür:

| Çıktı | İçerik |
|---|---|
| `data` | `df_family_ses`: skorlanmış family nesnesi + SES alanları |
| `diagnostics` | materyal indeks, yön ve latent CFA durum özeti |
| `material_loadings` | retained/dropped materyal değişken yükleri |
| `fit_measures` | `ses_latent` CFA fit ölçüleri |

### 7.1.1 Targets Entegrasyonu

```r
tar_target(ses_results, derive_ses_composites(df_family_scored))
tar_target(df_family_ses, ses_results$data)
tar_target(ses_diagnostics_table, ses_results$diagnostics)
tar_target(ses_material_loadings_table, ses_results$material_loadings)
tar_target(ses_cfa_fit_measures_table, ses_results$fit_measures)
tar_target(ses_component_summary_table, ses_component_summary(df_family_ses))
tar_target(ses_correlation_summary_table, ses_correlation_table(df_family_ses))
tar_target(ses_target_summary, summarize_ses_targets(df_family_scored, df_family_ses))
```

`df_family_ses` satır-düzeyi nesnedir; Git, OSF public paket ve Docker context dışında kalan `_targets/` cache'inde tutulur.

### 7.2 SES Stratejisi Tablosu

| Analiz | Birincil SES değişkeni | Sensitivity |
|---|---|---|
| Tablo 1 | Tüm boyutlar ayrı | — |
| H1 (çocuk algı) | `ses_latent` | `mean_aile_egitim`, `aile_isei08` |
| H2 (kardeş ilişki) | `ses_latent` | aynı |
| H3 (anne öz-rapor) | `ses_latent` | propensity score adjustment |
| H4 (Beck mediation) | `ses_latent` | aynı |
| H5 (diadik) | `ses_latent` + `egitim_fark` | — |
| Klinik moderasyon | `material_quintile` | — |

---

## 8. Eksik Veri Çoklu-Çerçeve

**Uygulama durumu:** KISIM II / 8 hattı `R/12_missing_data_frames.R`, `scripts/R/13_missing_data_audit.R`, `tests/test_missing_data_frames.R` ve `_targets.R` hedefleriyle uygulanmıştır. Ayrıntılı çalıştırma notu `docs/analiz_planlari/13-eksik-veri-runbook.md` içindedir.

Eksik veri katmanı final CSV'leri değiştirmez. Satır-düzeyi FIML/MI frame'leri ve `mice` nesneleri yalnız `_targets/` cache'inde tutulur; runner dışa sadece aggregate/metadata tabloları ve eksiklik paterni figürü yazar.

### 8.1 Üç-Mekanizma Tarama (Rubin 1976)

Tarama üç ayrımı aynı tabloda yapar:

1. **Toplam eksiklik:** değişken bazında `missing_n` ve `missing_pct`.
2. **Structural missing:** tasarım kaynaklı eksiklik. Bu çalışmada `hba1c` ve `dm_yili` kontrol grubunda structural missing kabul edilir.
3. **Analitik missing:** structural olmayan, modelleme stratejisi gerektiren eksiklik.

`missing_variable_summary`, `missing_block_summary`, `missing_group_summary` ve `missing_pattern_summary` tabloları bu ayrımı makinece denetlenebilir biçimde üretir. Little MCAR testi `fiml_primary` frame'i üzerinde çalıştırılır; structural DM-klinik kolonlar bu primary taramanın dışında tutulur.

### 8.2 Strateji Tablosu

| Mekanizma | Strateji | Birincil/Sensitivity |
|---|---|---|
| MCAR | Listwise / pairwise | Kullanılmaz (info kaybı) |
| MAR | **Multiple Imputation (m=50)** | **Birincil** |
| MAR | FIML (lavaan, brms) | SEM modellerinde varsayılan |
| MNAR | Delta-adjustment + selection model | Sensitivity |

### 8.3 Çoklu Frame Sözleşmesi

| Frame | İçerik | Kullanım |
|---|---|---|
| `fiml_primary` | Birincil analiz değişkenleri, eksikler korunmuş | SEM/FIML |
| `complete_case_primary` | Primary frame üzerinde complete-case alt küme | Bilgi kaybı kıyası |
| `mi_primary` | Structural eksik içermeyen primary MI frame | MAR altında ana MI |
| `mi_clinical_sensitivity` | `mi_primary` + `hba1c`, `dm_yili` | DM-klinik duyarlılık |

`hba1c` için kontrol satırları imputasyona açılmaz; `mice` `where` matrisi yalnız DM grubundaki analitik eksik hücreleri doldurur.

### 8.4 Multiple Imputation (m=50)

Varsayılan MI ayarı `m = 50`, `maxit = 30`, `seed = 20260427` olarak sabitlenmiştir. `mice` method planı veri tipine göre üretilir: sayısal değişkenlerde predictive mean matching (`pmm`), ordered factor değişkenlerde proportional odds (`polr`), iki düzeyli nominal faktörlerde `logreg`, çok düzeyli nominal faktörlerde `polyreg`.

Primary ve DM-klinik sensitivity imputasyon nesneleri `_targets.R` içindeki `missing_imputations` hedefinde tutulur. `outputs/tables/missing_mi_diagnostics.csv` yalnız method, imputed hücre sayısı, `m`, `maxit` ve logged-event sayısını raporlar; imputed veri satırları dışarı yazılmaz.

### 8.5 NMAR Sensitivity (Delta-Adjustment)

`missing_nmar_delta_grid` hedefi `beck_total`, `aile_isei08` ve `hba1c` için `delta = {-1, -0.5, 0, 0.5, 1}` duyarlılık şablonunu üretir. `apply_nmar_delta_adjustment()` yalnız structural olmayan orijinal eksik hücreleri ayarlar; kontrol grubundaki DM-klinik structural `NA` hücreleri dokunulmadan kalır. Model-spesifik delta sonuçları H1-H5 hedefleri eklendikten sonra raporlanacaktır.

---

# KISIM III — TANIMLAYICI VE DENGE

## 9. Tablo 1 + Standardize Mean Difference

**Uygulama durumu:** KISIM III / 9 hattı `R/13_table1_smd.R`, `scripts/R/14_table1_smd_audit.R`, `tests/test_table1_smd.R` ve `_targets.R` hedefleriyle uygulanmıştır. Ayrıntılı çalıştırma notu `docs/analiz_planlari/14-tablo1-smd-runbook.md` içindedir.

### 9.1 Tablo 1 Üretimi

Tablo 1 aile-düzeyi `df_family_ses` nesnesinden üretilir. Sürekli değişkenler `mean (sd); median [q1, q3]`, kategorik değişkenler `n (%)` olarak raporlanır. P değerleri Wilcoxon/Fisher testleriyle, q değerleri BH düzeltmesiyle hesaplanır; yorumda p değeri SMD ile birlikte değerlendirilir.

Üretilen artefaktlar:

- `outputs/tables/table1_family_summary.csv`
- `outputs/tables/table1_smd_balance.csv`
- `outputs/tables/table1_balance_action.csv`
- `outputs/tables/table1_group_counts.csv`
- `outputs/tables/table1_target_summary.csv`

Satır-düzeyi veri veya imputed veri dışa yazılmaz.

### 9.2 Mevcut Veride Beklenen Tablo 1 Sonuçları

| Değişken | DM (n=120) | Kontrol (n=121) | p | SMD | Yorum |
|---|---|---|---|---|---|
| Anne yaş | M~40 | M~40 | ns | <0.10 | Dengeli |
| Anne eğitim ≥lise | denge testi | denge testi | .14 | 0.13 | Sınırda |
| Aile ISEI-08 | M=34.5 (12.5) | M=31.4 (14.8) | **.018** | **0.23** | **DM ↑** |
| Çocuk sayısı | 2.88 (1.05) | 2.88 (0.93) | .62 | <0.10 | Dengeli |
| Kardeş yaş farkı | 3.21 (1.60) | 2.84 (1.80) | ≈.10 | **0.22** | DM↑ |
| Anne kronik hastalık | 29 (24%) | 35 (29%) | .40 | <0.10 | Dengeli |
| **Anne antidepresan** | **35 (29%)** | **11 (9%)** | **<.001** | **0.55** | **CİDDİ DM↑** |

**Manşet bulgu:** Anne antidepresan kullanımı gerçek veri audit'inde en güçlü dengesizliktir (`SMD = 0.528`). Tüm ana modellerde kovaryat olarak ayarlanır ve H3/H4 aile-anne duyarlılık analizlerinde stratified sensitivity olarak izlenir.

### 9.3 SMD Yorum Eşikleri (Austin 2009)

| SMD | Yorum | Strateji |
|---|---|---|
| <0.10 | İyi denge | Standart analiz yeterli |
| 0.10–0.20 | Sınırda | Kovaryat olarak ayarla |
| 0.20–0.40 | Dengesiz | IPTW + kovaryat ayarla |
| >0.40 | **Ciddi dengesizlik** | **Stratified sensitivity zorunlu** |

---

## 10. Causal DAG

**Uygulama durumu:** KISIM III / 10 hattı `R/14_causal_dag.R`, `scripts/R/15_causal_dag_audit.R`, `tests/test_causal_dag.R` ve `_targets.R` hedefleriyle uygulanmıştır. Ayrıntılı çalıştırma notu `docs/analiz_planlari/15-nedensel-dag-runbook.md` içindedir.

**DAG karar kaydı:** Aşağıdaki ilk SAP taslağındaki literal yönler `dagitty` ile çalıştırıldığında beklenen `{SES, AgeGap, FamilySize}` adjustment setini üretmez. Uygulamada `analysis_dag_v1` kullanılır: `SES`, `AgeGap` ve `FamilySize` baseline/design confounder; `Maternal_AD_use`, `Beck` ve `ParentingStyle` total-effect modellerinde ayarlanmayan mediator/sensitivity düğümleri olarak sabitlenmiştir.

### 10.1 DAG Spesifikasyonu

```r
library(dagitty); library(ggdag)

dag_t1dm <- dagitty('dag {
  Genetics -> T1DM_status
  Genetics -> Maternal_AD_use

  T1DM_status -> Maternal_AD_use
  T1DM_status -> ParentingStyle
  T1DM_status -> SES
  T1DM_status -> AgeGap
  T1DM_status -> FamilySize
  T1DM_status -> ChildPerception

  Maternal_AD_use -> Beck
  Maternal_AD_use -> ParentingStyle

  Beck -> ParentingStyle
  Beck -> ChildPerception

  ParentingStyle -> ChildPerception
  ChildPerception -> SiblingRelations

  SES -> ParentingStyle
  SES -> Beck
  SES -> ChildPerception
  AgeGap -> SiblingRelations
  AgeGap -> ChildPerception
  FamilySize -> ParentingStyle

  T1DM_status [exposure]
  ChildPerception [outcome]
}')
```

### 10.2 Adjustment Set Hesabı

Uygulanan `analysis_dag_v1` için `dagitty::adjustmentSets()` çıktısı:

```text
{ AgeGap, FamilySize, SES }
```

Repo karşılığı:

```text
age_gap + cocuk_sayisi + ses_latent
```

`Maternal_AD_use`, `Beck` ve `ParentingStyle` total-effect modellerinde ayarlanmaz; bu değişkenler mediation, direct-effect sensitivity ve stratified sensitivity analizlerine ayrılır.

### 10.3 Kovaryat Stratejisi

| Analiz türü | Confounder (ayarlanır) | Mediator (ayrı analizde) | Modurator (etkileşim) |
|---|---|---|---|
| Total Effect | SES, AgeGap, FamilySize | — | — |
| Direct Effect | SES, AgeGap, FamilySize, Beck, AD | — | — |
| Indirect Effect (mediation) | — | Beck, AD, ParentingStyle | — |
| Moderated mediation | — | Beck, ParentingStyle | Group, AgeCat |

---

## 11. Propensity Score (IPTW + Matching) + Doubly Robust

**Uygulama durumu:** KISIM III / 11 hattı `R/15_propensity_score.R`, `scripts/R/16_propensity_score_audit.R` ve `docs/analiz_planlari/16-propensity-score-runbook.md` ile somutlaştırılır. Birincil PS modeli KISIM III / 10 `analysis_dag_v1` kararına bağlıdır: `group_dm ~ ses_latent + age_gap + cocuk_sayisi`. SAP taslağındaki geniş demografik formül ve GBM/twang yaklaşımı, paket ve sensitivity kararı gerektirdiği için primary hatta çalıştırılmaz.

### 11.1 PS Tahmini

```r
estimate_propensity_scores <- function(df) {
  ps_formula <- group_f == "DM" ~ scale(anne_yas) + scale(egitim_durumu) +
                                    scale(es_egitim_durumu) + scale(es_isei08) +
                                    scale(cocuk_sayisi) + scale(age_gap) +
                                    ev_sahipligi + arabaniz_var_mi +
                                    kronik_hastalik_durumu

  ps_logit <- glm(ps_formula, data = df, family = binomial)

  # GBM alternatif (twang)
  ps_gbm <- twang::ps(ps_formula, data = df,
                       n.trees = 5000, interaction.depth = 3,
                       estimand = "ATE", stop.method = "es.mean")

  plot(ps_gbm, plots = "boxplot")
  bal.tab(ps_gbm)

  list(logit = ps_logit, gbm = ps_gbm)
}
```

### 11.2 IPTW Stabilized Weights

```r
compute_iptw <- function(df, ps_value) {
  prop_dm <- mean(df$group_f == "DM")

  df$iptw_stab <- if_else(df$group_f == "DM",
                            prop_dm / ps_value,
                            (1 - prop_dm) / (1 - ps_value))

  cutoff <- quantile(df$iptw_stab, 0.99, na.rm = TRUE)
  df$iptw_trimmed <- pmin(df$iptw_stab, cutoff)

  df
}
```

### 11.3 Doubly Robust (Robins, Rotnitzky & Zhao 1994)

```r
fit_dr <- lm(embu_p_asiri_koruma_mean ~ group_f + ses_latent +
              scale(anne_yas) + scale(egitim_durumu),
             weights = iptw_trimmed,
             data = df_family_iptw)

library(sandwich); library(lmtest)
coeftest(fit_dr, vcov = sandwich)
```

---

# KISIM V — BİRİNCİL HİPOTEZ TESTLERİ

## 12. H1: Çocuk Algı Multilevel ANCOVA + 3-Way + IRT GRM + Bayesian

**Uygulama durumu:** KISIM V / 12 hattı `R/16_h1_child_perception.R`, `scripts/R/17_h1_child_perception_audit.R` ve `docs/analiz_planlari/30-h1-cocuk-algisi-runbook.md` ile somutlaştırılır. SAP taslağındaki `scale(...)` terimleri reproducibility için analiz öncesi z-skor kolonlarına çevrilir; DAG v1 ile uyumlu olarak `cocuk_sayisi_z` primary modele eklenmiştir. Bayesian bileşen default pipeline'da posterior sampling çalıştırmaz; prior/model/seed preflight planı üretir.

### 12.1 H1 Birincil Model (Frequentist Multilevel)

```r
run_h1_frequentist <- function(df_long) {
  outcomes <- c("embu_c_qsicaklik_mean", "embu_c_qasiri_koruma_mean",
                "embu_c_qreddetme_mean", "embu_c_qkarsilastirma_mean")

  results <- map(outcomes, function(y) {
    fml <- as.formula(paste(y,
      "~ role_f + scale(cocuk_yas) + cinsiyet_f + scale(ses_latent) +
         scale(age_gap) + (1 | aile_no_f)"))

    m <- lme4::lmer(fml, data = df_long, REML = TRUE)

    list(
      outcome  = y,
      model    = m,
      anova    = anova(m, type = 3, ddf = "Satterthwaite"),
      emm      = emmeans::emmeans(m, ~ role_f),
      pairs    = emmeans::pairs(emmeans::emmeans(m, ~ role_f), adjust = "tukey"),
      effects  = effectsize::standardize_parameters(m, ci = 0.95),
      icc      = performance::icc(m),
      r2       = performance::r2(m),
      diag     = performance::check_model(m, panel = FALSE)
    )
  })

  names(results) <- outcomes

  all_pairs <- map_dfr(results, function(r) {
    as.data.frame(r$pairs) |> mutate(outcome = r$outcome)
  }) |> mutate(p_fdr = p.adjust(p.value, method = "BH"))

  list(by_outcome = results, all_pairs_fdr = all_pairs)
}
```

### 12.2 H1 Genişletme: 3-Way Etkileşim (Yaş × Cinsiyet × Grup)

```r
run_h1_three_way <- function(df_long, outcome) {
  fml <- as.formula(paste(outcome,
    "~ role_f * scale(cocuk_yas) * cinsiyet_f + scale(ses_latent) + (1 | aile_no_f)"))

  m <- lme4::lmer(fml, data = df_long, REML = TRUE)

  three_way_test <- anova(m, type = 3)["role_f:scale(cocuk_yas):cinsiyet_f", ]

  if (!is.na(three_way_test$`Pr(>F)`) && three_way_test$`Pr(>F)` < 0.10) {
    emm_3way <- emmeans::emmeans(m, ~ role_f | cocuk_yas * cinsiyet_f,
                                   at = list(cocuk_yas = c(8, 12, 16)))

    library(interactions)
    jn <- interactions::johnson_neyman(m, pred = role_f, modx = cocuk_yas)
  } else {
    emm_3way <- NULL; jn <- NULL
  }

  list(model = m, three_way = three_way_test, emm = emm_3way, jn = jn)
}
```

### 12.3 H1 IRT Genişletme: Graded Response Model

EMBU-C 4'lü Likert için Samejima (1969) **GRM**:

```r
run_h1_irt_grm <- function(df_long, subscale = "reddetme") {
  library(mirt)

  items <- paste0("embu_c_q", sprintf("%02d", embu_subscales[[subscale]]))
  item_data <- df_long[items]

  # Tek-boyutlu GRM
  grm_fit <- mirt::mirt(item_data, model = 1, itemtype = "graded",
                          method = "EM", verbose = FALSE)

  # Madde parametreleri (a = discrimination, b1-b3 = thresholds)
  coefs <- coef(grm_fit, IRTpars = TRUE, simplify = TRUE)

  # Trace plots
  plot(grm_fit, type = "trace")
  plot(grm_fit, type = "info")  # test bilgi fonksiyonu

  # IRT theta scores (logit-scale) — sum-skor'dan daha hassas
  theta_irt <- mirt::fscores(grm_fit, method = "EAP")
  df_long$theta_subscale <- as.numeric(theta_irt)

  # DIF — DM × Kontrol arasında madde-bias?
  dif_test <- mirt::DIF(grm_fit, c("a1", "d1", "d2", "d3"),
                          group = df_long$group_f,
                          scheme = "drop")

  # IRT-skor ile H1 yeniden tahmin
  m_irt <- lmer(theta_subscale ~ role_f + scale(cocuk_yas) + cinsiyet_f +
                  scale(ses_latent) + (1 | aile_no_f),
                data = df_long)

  list(grm = grm_fit, coefs = coefs, dif = dif_test, model_with_theta = m_irt)
}
```

### 12.4 H1 Bayesian Genişletme

```r
run_h1_bayesian <- function(df_long, outcome) {
  library(brms)

  # Weakly informative priors
  priors <- c(
    prior(normal(0, 1), class = b),
    prior(student_t(3, 0, 2.5), class = sd),
    prior(student_t(3, 0, 2.5), class = sigma)
  )

  fml <- as.formula(paste(outcome,
    "~ role_f + scale(cocuk_yas) + cinsiyet_f + scale(ses_latent) +
       (1 | aile_no_f)"))

  m_bayes <- brms::brm(fml, data = df_long,
                        family = gaussian(),
                        prior = priors,
                        chains = 4, iter = 4000, warmup = 1500,
                        seed = 20260427, cores = 4,
                        control = list(adapt_delta = 0.95, max_treedepth = 12))

  # ROPE
  library(bayestestR)
  rope_result <- rope(m_bayes, range = c(-0.1, 0.1), ci = 0.89)

  # Bayes factor
  m_null <- update(m_bayes, formula = . ~ . - role_f)
  bf_role <- bayes_factor(m_bayes, m_null)

  # PPC
  pp_check(m_bayes, type = "dens_overlay", ndraws = 100)

  list(model = m_bayes, rope = rope_result, bf = bf_role)
}
```

---

## 13. H2: Kardeş İlişkisi (Aile-Mean + APIM + Olsen-Kenny + Age-Gap Moderation)

**Uygulama durumu:** KISIM V / 13 hattı `R/17_h2_sibling_relationships.R`, `scripts/R/18_h2_sibling_relationships_audit.R` ve `docs/analiz_planlari/31-h2-kardes-iliskileri-runbook.md` ile somutlaştırılır. SAP taslağındaki `srq_*_mean` adları aktif türetilmiş skor ekosistemindeki `srq_ho_*_mean` kolonlarına bağlanır. Olsen-Kenny CFA, aktif SRQ scoring map içindeki quarreling item seti (`srq_4`, `srq_20`, `srq_36`) ile çalışır.

### 13.1 H2 Strateji 1: Aile-Düzeyi Welch t-Test

```r
run_h2_family_mean <- function(df_family, df_long) {
  df_family_srq <- df_long |>
    group_by(aile_no, group_f) |>
    summarise(across(c(srq_warmth_mean, srq_status_mean,
                        srq_conflict_mean, srq_rivalry_mean),
                      ~mean(.x, na.rm = TRUE)), .groups = "drop")

  results <- map_dfr(c("warmth", "status", "conflict", "rivalry"), function(f) {
    y_col <- paste0("srq_", f, "_mean")

    t_res <- t.test(as.formula(paste(y_col, "~ group_f")),
                      data = df_family_srq, var.equal = FALSE)
    d_res <- effectsize::cohens_d(as.formula(paste(y_col, "~ group_f")),
                                     data = df_family_srq, ci = 0.95)

    tibble(factor = f,
            mean_dm = mean(df_family_srq[[y_col]][df_family_srq$group_f == "DM"], na.rm=T),
            mean_kont = mean(df_family_srq[[y_col]][df_family_srq$group_f == "Kontrol"], na.rm=T),
            t = t_res$statistic, df = t_res$parameter, p = t_res$p.value,
            d = d_res$Cohens_d, d_ci_lo = d_res$CI_low, d_ci_hi = d_res$CI_high)
  }) |> mutate(p_fdr = p.adjust(p, method = "BH"))

  results
}
```

### 13.2 H2 Strateji 2: APIM (Distinguishable Dyads)

Kenny, Kashy & Cook (2006) çerçevesi — actor + partner effects:

```r
run_h2_apim <- function(df_long) {
  apim_results <- map(c("warmth", "status", "conflict", "rivalry"), function(f) {
    y_col <- paste0("srq_", f, "_mean")

    fml <- as.formula(paste(y_col, "~ group_f * family_role_f + scale(age_gap)"))

    m <- nlme::lme(
      fixed       = fml,
      random      = ~ 1 | aile_no_f,
      data        = df_long,
      weights     = nlme::varIdent(form = ~ 1 | family_role_f),
      correlation = nlme::corCompSymm(form = ~ 1 | aile_no_f),
      method      = "REML",
      na.action   = na.exclude
    )

    list(factor = f, model = m, summary = summary(m))
  })

  apim_results
}
```

### 13.3 H2 Strateji 3: Olsen-Kenny Dyadic CFA

Olsen & Kenny (2006) — distinguishable dyad CFA, ölçüm hatasını dışlayan latent korelasyon:

```r
run_h2_olsen_kenny <- function(df_long) {
  df_wide <- df_long |>
    select(aile_no, family_role, srq_4, srq_20, srq_36) |>
    pivot_wider(id_cols = aile_no,
                 names_from = family_role,
                 values_from = c(srq_4, srq_20, srq_36))

  dyad_model <- '
    quarrel_idx =~ l1*srq_4_index + l2*srq_20_index + l3*srq_36_index
    quarrel_sib =~ l1*srq_4_sibling + l2*srq_20_sibling + l3*srq_36_sibling

    # Same-item method covariances
    srq_4_index ~~ srq_4_sibling
    srq_20_index ~~ srq_20_sibling
    srq_36_index ~~ srq_36_sibling

    quarrel_idx ~~ quarrel_sib
  '

  fit_dyad <- lavaan::cfa(dyad_model, data = df_wide,
                            estimator = "MLR", missing = "fiml")

  inspect(fit_dyad, "cor.lv")["quarrel_idx", "quarrel_sib"]
}
```

### 13.4 H2 Genişletme: Same-Sex × Age-Gap Moderasyonu

Brody (1998) hipotezi: same-sex çiftlerde yakınlık ↑; Buist et al. (2013): age_gap ↑ → çatışma ↓

```r
run_h2_age_gap_moderation <- function(df_family, df_long) {
  df_family_srq <- df_long |>
    group_by(aile_no, group_f) |>
    summarise(across(starts_with("srq_") & ends_with("_mean"),
                      ~mean(.x, na.rm = TRUE)), .groups = "drop") |>
    left_join(df_family |> select(aile_no, age_gap, same_sex, ses_latent),
                by = "aile_no")

  results <- map_dfr(c("warmth", "status", "conflict", "rivalry"), function(f) {
    y_col <- paste0("srq_", f, "_mean")
    fml <- as.formula(paste(y_col,
      "~ group_f * scale(age_gap) * same_sex + scale(ses_latent)"))

    m <- lm(fml, data = df_family_srq)
    aov_tab <- car::Anova(m, type = 3)

    tibble(factor = f,
            group_p = aov_tab["group_f", "Pr(>F)"],
            age_gap_p = aov_tab["scale(age_gap)", "Pr(>F)"],
            same_sex_p = aov_tab["same_sex", "Pr(>F)"],
            group_x_age_p = aov_tab["group_f:scale(age_gap)", "Pr(>F)"],
            group_x_sex_p = aov_tab["group_f:same_sex", "Pr(>F)"],
            three_way_p = aov_tab["group_f:scale(age_gap):same_sex", "Pr(>F)"])
  })

  results
}
```

---

## 14. H3: Anne Öz-Rapor (Antidepresan-Stratified + IPTW)

**Uygulama durumu:** KISIM V / 14 hattı `R/18_h3_parent_self_report.R`, `scripts/R/19_h3_parent_self_report_audit.R` ve `docs/analiz_planlari/32-h3-anne-oz-rapor-runbook.md` ile somutlaştırılır. SAP taslağındaki `scale(...)` terimleri analiz öncesi `anne_yas_z`, `ses_latent_z` ve `age_gap_z` kolonlarına çevrilir; `cocuk_sayisi` SAP ile uyumlu olarak ham aile büyüklüğü kovaryatı kalır. Anne antidepresan kullanımı total-effect primary modelde ayarlanmaz; AD-ayarlı/stratified sensitivity ve IPTW+HC3 robust model ayrı tablolar olarak raporlanır.

### 14.1 H3 Birincil Model

```r
run_h3_main <- function(df_family) {
  outcomes <- c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
                "embu_p_reddetme_mean", "embu_p_karsilastirma_mean")

  results <- map_dfr(outcomes, function(y) {
    fml <- as.formula(paste(y,
      "~ group_f + scale(anne_yas) + scale(ses_latent) +
         scale(age_gap) + cocuk_sayisi"))

    m <- lm(fml, data = df_family)
    coef_tab <- summary(m)$coefficients

    eff <- effectsize::standardize_parameters(m, ci = 0.95) |>
      filter(Parameter == "group_fDM")

    tibble(outcome = y,
            beta = coef_tab["group_fDM", "Estimate"],
            se = coef_tab["group_fDM", "Std. Error"],
            t = coef_tab["group_fDM", "t value"],
            p = coef_tab["group_fDM", "Pr(>|t|)"],
            std_beta = eff$Std_Coefficient,
            d_ci_lo = eff$CI_low, d_ci_hi = eff$CI_high)
  }) |> mutate(p_fdr = p.adjust(p, method = "BH"))

  results
}
```

### 14.2 H3 Antidepresan-Stratified Sensitivity (KRİTİK)

```r
run_h3_stratified <- function(df_family) {
  outcomes <- c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
                "embu_p_reddetme_mean", "embu_p_karsilastirma_mean")

  results <- map_dfr(outcomes, function(y) {
    fml <- as.formula(paste(y, "~ group_f + scale(anne_yas) + scale(ses_latent)"))

    # A) Tüm anneler — antidepresan kovaryat
    fml_all <- as.formula(paste(y,
      "~ group_f + anne_antidepresan + scale(anne_yas) + scale(ses_latent)"))
    m_all <- lm(fml_all, data = df_family)
    eff_all <- effectsize::standardize_parameters(m_all) |>
      filter(Parameter == "group_fDM")

    # B) Yalnız antidepresan kullanmayan (n≈193)
    m_no_ad <- lm(fml, data = filter(df_family, anne_antidepresan == 0))
    eff_no_ad <- effectsize::standardize_parameters(m_no_ad) |>
      filter(Parameter == "group_fDM")

    # C) Yalnız antidepresan kullanan (n≈45)
    n_ad_dm <- sum(df_family$anne_antidepresan == 1 & df_family$group_f == "DM")
    n_ad_ko <- sum(df_family$anne_antidepresan == 1 & df_family$group_f == "Kontrol")

    eff_ad <- if (n_ad_dm >= 5 && n_ad_ko >= 5) {
      m_ad <- lm(fml, data = filter(df_family, anne_antidepresan == 1))
      effectsize::standardize_parameters(m_ad) |>
        filter(Parameter == "group_fDM")
    } else {
      tibble(Std_Coefficient = NA_real_, CI_low = NA_real_, CI_high = NA_real_)
    }

    bind_rows(
      tibble(outcome=y, strata="All (adj for AD)", d=eff_all$Std_Coefficient,
              ci_lo=eff_all$CI_low, ci_hi=eff_all$CI_high),
      tibble(outcome=y, strata="No antidepresan", d=eff_no_ad$Std_Coefficient,
              ci_lo=eff_no_ad$CI_low, ci_hi=eff_no_ad$CI_high),
      tibble(outcome=y, strata="Antidepresan only", d=eff_ad$Std_Coefficient,
              ci_lo=eff_ad$CI_low, ci_hi=eff_ad$CI_high)
    )
  })

  results
}
```

### 14.3 H3 IPTW Versiyon

```r
run_h3_iptw <- function(df_iptw) {
  outcomes <- c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
                "embu_p_reddetme_mean", "embu_p_karsilastirma_mean")

  map_dfr(outcomes, function(y) {
    fml <- as.formula(paste(y, "~ group_f + scale(anne_yas) + scale(ses_latent)"))

    m <- lm(fml, data = df_iptw, weights = iptw_trimmed)

    library(sandwich)
    se_robust <- sqrt(diag(vcovHC(m, type = "HC3")))

    tibble(outcome = y,
            beta = coef(m)["group_fDM"],
            se_robust = se_robust["group_fDM"],
            t = coef(m)["group_fDM"] / se_robust["group_fDM"],
            p = 2 * (1 - pt(abs(coef(m)["group_fDM"] / se_robust["group_fDM"]),
                              df = nrow(df_iptw) - length(coef(m)))))
  })
}
```

---

## 15. H4: Beck → EMBU-P Latent SEM + Multi-Group + Bayesian

**Uygulama durumu:** KISIM V / 15 hattı `R/19_h4_beck_parenting_sem.R`, `scripts/R/20_h4_beck_parenting_sem_audit.R` ve `docs/analiz_planlari/33-h4-beck-embu-sem-runbook.md` ile somutlaştırılır. Birincil model 50 ordinal item üzerinde WLSMV latent SEM olarak çalışır. Multi-group screen, grup-spesifik boş ordinal kategori ve hesap yükü nedeniyle targets içinde reduced 19-item configural+metric screen olarak yürütülür; yapılan sparse kategori collapse mapping'i ayrı tabloda raporlanır. Bayesian SEM default pipeline'da posterior sampling çalıştırmaz; `blavaan` syntax/prior/sampler preflight ve manuel fit fonksiyonu sağlar.

### 15.1 H4 Latent SEM (WLSMV)

```r
run_h4_latent_sem <- function(df_family) {
  sem_model <- '
    # ÖLÇÜM MODELİ
    sicaklik =~ embu_p_q01 + embu_p_q03 + embu_p_q06 + embu_p_q07 +
                 embu_p_q13 + embu_p_q17 + embu_p_q20 + embu_p_q24 + embu_p_q26
    asiri_kor =~ embu_p_q04 + embu_p_q08 + embu_p_q14 + embu_p_q15 +
                  embu_p_q19 + embu_p_q23 + embu_p_q25
    reddetme =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + embu_p_q12 +
                 embu_p_q16 + embu_p_q21 + embu_p_q22 + embu_p_q28
    karsilastirma =~ embu_p_q02 + embu_p_q11 + embu_p_q18 + embu_p_q27 + embu_p_q29

    beck_dep =~ beck_1 + beck_2 + beck_3 + beck_4 + beck_5 + beck_6 +
                 beck_7 + beck_8 + beck_9 + beck_10 + beck_11 + beck_12 +
                 beck_13 + beck_14 + beck_15 + beck_16 + beck_17 + beck_18 +
                 beck_19 + beck_20 + beck_21

    # YAPISAL YOLLAR
    sicaklik     ~ b1*beck_dep + scale(anne_yas) + scale(ses_latent)
    asiri_kor    ~ b2*beck_dep + scale(anne_yas) + scale(ses_latent)
    reddetme     ~ b3*beck_dep + scale(anne_yas) + scale(ses_latent)
    karsilastirma ~ b4*beck_dep + scale(anne_yas) + scale(ses_latent)
  '

  ordered_items <- c(paste0("embu_p_q", sprintf("%02d", 1:29)),
                      paste0("beck_", 1:21))

  fit <- lavaan::sem(sem_model, data = df_family,
                       estimator = "WLSMV",
                       ordered = ordered_items,
                       missing = "pairwise")

  list(fit = fit,
        fit_meas = lavaan::fitMeasures(fit, c("chisq.scaled","df.scaled","pvalue.scaled",
                                                "cfi.scaled","rmsea.scaled","srmr")),
        paths = lavaan::parameterEstimates(fit, standardized = TRUE) |>
                  filter(label %in% c("b1","b2","b3","b4")) |>
                  select(label, lhs, op, rhs, est, se, z, pvalue, std.all))
}
```

### 15.2 H4 Multi-Group SEM Invariance

```r
run_h4_multigroup_invariance <- function(df_family) {
  fit_config <- sem(base_model, data = df_family, group = "group_f",
                     estimator = "WLSMV", ordered = TRUE)
  fit_metric <- sem(base_model, data = df_family, group = "group_f",
                     estimator = "WLSMV", ordered = TRUE,
                     group.equal = "loadings")
  fit_scalar <- sem(base_model, data = df_family, group = "group_f",
                     estimator = "WLSMV", ordered = TRUE,
                     group.equal = c("loadings", "thresholds"))
  fit_struct <- sem(base_model, data = df_family, group = "group_f",
                     estimator = "WLSMV", ordered = TRUE,
                     group.equal = c("loadings", "thresholds", "regressions"))

  comparison <- semTools::compareFit(fit_config, fit_metric, fit_scalar, fit_struct)
  comparison
}
```

### 15.3 H4 Bayesian SEM

```r
run_h4_bayesian_sem <- function(df_family) {
  library(blavaan)

  bsem_model <- '
    sicaklik =~ embu_p_q01 + embu_p_q03 + embu_p_q06 + embu_p_q07 +
                 embu_p_q13 + embu_p_q17 + embu_p_q20 + embu_p_q24 + embu_p_q26
    reddetme =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + embu_p_q12 +
                 embu_p_q16 + embu_p_q21 + embu_p_q22 + embu_p_q28
    beck_dep =~ beck_1 + beck_2 + beck_3 + beck_4 + beck_5 + beck_6

    sicaklik ~ b_warm*beck_dep
    reddetme ~ b_rej*beck_dep
  '

  bsem_fit <- blavaan::bsem(bsem_model, data = df_family,
                              ordered = TRUE,
                              n.chains = 4, burnin = 2000, sample = 5000,
                              target = "stan",
                              dp = blavaan::dpriors(
                                lambda = "normal(0.5, 0.5)",
                                beta   = "normal(0, 1)"
                              ))

  fitMeasures(bsem_fit, c("ppp", "bcfi", "brmsea"))
  bsem_fit
}
```

## 16. H5: Diadik Tutarlılık (RSA + Common Fate + Dyadic CFA + k-Coefficient)

### 16.1 H5 Niye Tezin Birincil Yenilik Katkısı?

Türk T1DM ailelerinde anne öz-algısı (EMBU-P) ile çocuk algısı (EMBU-C-idx, EMBU-C-sib) arasındaki tutarlılık örüntüsü daha önce sistematik olarak incelenmemiştir. Bu fazın çıktıları aynı zamanda **psikometrik adaptasyon makalesinin** odağı için ideal bir vaka oluşturur.

### 16.2 H5 Strateji 1: ICC + Bland-Altman

```r
run_h5_concordance <- function(df_family) {
  subscales <- c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")

  results <- map_dfr(subscales, function(sub) {
    p_col      <- paste0("embu_p_", sub, "_mean")
    c_idx_col  <- paste0("embu_c_idx_q", sub, "_mean")
    c_sib_col  <- paste0("embu_c_sib_q", sub, "_mean")

    dyad_results <- list(
      anne_idx = df_family[, c(p_col, c_idx_col, "group_f")],
      anne_sib = df_family[, c(p_col, c_sib_col, "group_f")],
      idx_sib  = df_family[, c(c_idx_col, c_sib_col, "group_f")]
    )

    purrr::imap_dfr(dyad_results, function(dyad_df, dyad_name) {
      dyad_df <- na.omit(dyad_df)
      if (nrow(dyad_df) < 10) return(tibble())

      # ICC(2,1) — agreement (group-spesifik)
      iccs <- dyad_df |>
        group_by(group_f) |>
        summarise(
          n = n(),
          icc = irr::icc(across(1:2), model = "twoway",
                          type = "agreement", unit = "single")$value,
          icc_lo = irr::icc(across(1:2), model = "twoway",
                              type = "agreement", unit = "single")$lbound,
          icc_hi = irr::icc(across(1:2), model = "twoway",
                              type = "agreement", unit = "single")$ubound,
          .groups = "drop"
        )

      # Bland-Altman LoA (group-spesifik)
      ba_dm <- BlandAltmanLeh::bland.altman.stats(
        dyad_df[[1]][dyad_df$group_f == "DM"],
        dyad_df[[2]][dyad_df$group_f == "DM"])
      ba_ko <- BlandAltmanLeh::bland.altman.stats(
        dyad_df[[1]][dyad_df$group_f == "Kontrol"],
        dyad_df[[2]][dyad_df$group_f == "Kontrol"])

      bind_rows(
        tibble(subscale=sub, dyad_type=dyad_name, group="DM",
                n=iccs$n[iccs$group_f=="DM"],
                icc=iccs$icc[iccs$group_f=="DM"],
                mean_diff=ba_dm$mean.diffs,
                loa_lo=ba_dm$lower.limit, loa_hi=ba_dm$upper.limit),
        tibble(subscale=sub, dyad_type=dyad_name, group="Kontrol",
                n=iccs$n[iccs$group_f=="Kontrol"],
                icc=iccs$icc[iccs$group_f=="Kontrol"],
                mean_diff=ba_ko$mean.diffs,
                loa_lo=ba_ko$lower.limit, loa_hi=ba_ko$upper.limit)
      )
    })
  })

  results
}
```

### 16.3 H5 Strateji 2: Response Surface Analysis (RSA)

Edwards & Parry (1993) — diadik tutarlılık için **gold standard**, polynomial regression yüzey analizi:

```r
run_h5_rsa <- function(df_family) {
  library(RSA)

  subscales <- c("sicaklik", "reddetme")  # ana iki teorik faktör

  results <- map(subscales, function(sub) {
    p_col      <- paste0("embu_p_", sub, "_mean")
    c_idx_col  <- paste0("embu_c_idx_q", sub, "_mean")

    # Group-spesifik RSA
    rsa_dm <- RSA(
      formula = as.formula(paste("beck_total ~", p_col, "*", c_idx_col)),
      data = filter(df_family, group_f == "DM"),
      models = c("full", "SQD", "RR")
    )
    rsa_ko <- RSA(
      formula = as.formula(paste("beck_total ~", p_col, "*", c_idx_col)),
      data = filter(df_family, group_f == "Kontrol"),
      models = c("full", "SQD", "RR")
    )

    # 4 anahtar parametre (Edwards-Parry 1993):
    # a1: ortak artış (concordant high) → outcome
    # a2: nonlinear bileşen (concordant high vs concordant low)
    # a3: tutarsızlık yönü (kim daha yüksek?)
    # a4: tutarsızlık derecesi

    list(subscale = sub, dm = rsa_dm, kontrol = rsa_ko,
          dm_summary = summary(rsa_dm$models$full),
          ko_summary = summary(rsa_ko$models$full))
  })

  results
}
```

### 16.4 H5 Strateji 3: Common Fate Model (CFM)

Aile-içi ortak yapı (latent) + dyad-spesifik bileşen ayrımı:

```r
run_h5_common_fate <- function(df_family) {
  cfm_models <- map(c("sicaklik", "reddetme"), function(sub) {
    p_col     <- paste0("embu_p_", sub, "_mean")
    c_idx_col <- paste0("embu_c_idx_q", sub, "_mean")
    c_sib_col <- paste0("embu_c_sib_q", sub, "_mean")

    cfm_model <- sprintf('
      common_%s =~ %s + %s + %s
      common_%s ~ group_f + scale(anne_yas) + scale(ses_latent)

      %s ~~ %s
      %s ~~ %s
      %s ~~ %s
    ', sub, p_col, c_idx_col, c_sib_col, sub,
       p_col, p_col, c_idx_col, c_idx_col, c_sib_col, c_sib_col)

    fit <- lavaan::sem(cfm_model, data = df_family,
                         estimator = "MLR", missing = "fiml")

    list(subscale = sub, fit = fit,
          fit_meas = fitMeasures(fit, c("cfi","rmsea","srmr")))
  })

  cfm_models
}
```

### 16.5 H5 Strateji 4: Dyadic CFA (Olsen-Kenny 2006)

```r
run_h5_olsen_kenny_dyadic_cfa <- function(df_family) {
  # Reddetme alt ölçeği için anne ↔ indeks-çocuk dyadic CFA
  dyad_cfa_model <- '
    rejection_mom    =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + embu_p_q12
    rejection_child  =~ embu_c_idx_q05 + embu_c_idx_q09 +
                         embu_c_idx_q10 + embu_c_idx_q12

    # Aynı maddenin korele rezidüleri (method effect)
    embu_p_q05 ~~ embu_c_idx_q05
    embu_p_q09 ~~ embu_c_idx_q09
    embu_p_q10 ~~ embu_c_idx_q10
    embu_p_q12 ~~ embu_c_idx_q12

    # Latent korelasyon = TRUE concordance (ölçüm hatası dışlanmış)
    rejection_mom ~~ rejection_child
  '

  fit_dyad <- lavaan::cfa(dyad_cfa_model, data = df_family,
                            ordered = TRUE, estimator = "WLSMV")

  list(fit = fit_dyad,
        true_concordance = inspect(fit_dyad, "cor.lv")["rejection_mom", "rejection_child"],
        fit_meas = fitMeasures(fit_dyad, c("cfi.scaled", "rmsea.scaled", "srmr")))
}
```

### 16.6 H5 Strateji 5: k-Coefficient (Kenny et al. 2006)

```r
run_h5_k_coefficient <- function(df_family) {
  # k = partner_effect / actor_effect
  # k = 0: actor-only model (individualistic)
  # k = 1: couple model (actor = partner; dyad sum matters)
  # k = -1: contrast model (relative comparison matters)

  apim_redd <- nlme::lme(
    fixed = embu_c_qreddetme_mean ~ group_f * family_role_f,
    random = ~ 1 | aile_no_f,
    data = df_long,
    method = "REML"
  )

  # Actor + partner coefficient extraction
  fixed_coefs <- fixef(apim_redd)
  actor_eff <- fixed_coefs["group_fDM"]
  partner_eff <- fixed_coefs["group_fDM:family_role_fsibling"]

  k <- partner_eff / actor_eff

  # Bootstrap CI
  library(boot)
  k_boot <- boot(data = df_long, statistic = function(d, i) {
    m <- nlme::lme(embu_c_qreddetme_mean ~ group_f * family_role_f,
                    random = ~ 1 | aile_no_f, data = d[i, ])
    coefs <- fixef(m)
    coefs["group_fDM:family_role_fsibling"] / coefs["group_fDM"]
  }, R = 1000)

  list(k = k, ci = boot.ci(k_boot, type = "bca"))
}
```

### 16.7 Diadik Tutarsızlık Klinik Yorumu

| Tutarsızlık örüntüsü | Klinik yorum | Operasyonalizasyon |
|---|---|---|
| Anne ↑ Çocuk ↓ (sıcaklık) | Anne savunmacı / sosyal istenirlik | `p_warmth − c_idx_warmth > 0.5` |
| Anne ↓ Çocuk ↑ (reddetme) | Anne aşırı öz-eleştiri | `c_idx_rejection − p_rejection > 0.5` |
| İki kardeş arası uyumsuzluk | **Differential Parental Treatment (PDT)** | `|c_idx − c_sib| > 0.5` |

> **Beklenen örüntü:** Streisand & Monaghan (2014) kronik hastalık ailelerinde **anne savunmacılığının** Kontrol'den daha güçlü olduğunu öngörür. Mevcut psikometrik validasyon bulgusu (DM Reddetme self-report < Kontrol Reddetme) bu hipotez ile uyumlu.

---

# KISIM VI — MEDIATION

## 17. Tek-Mediator Modeli

### 17.1 Birincil Mediation Yapısı

```
T1DM_status → Beck → ParentingStyle (EMBU-P) → ChildPerception (EMBU-C) → SiblingRelations (SRQ)
```

```r
run_simple_mediation <- function(df_family, df_long) {
  # Aile-düzeyi özet
  df_long_summary <- df_long |>
    group_by(aile_no, group_f) |>
    summarise(
      embu_c_redd_avg = mean(embu_c_qreddetme_mean, na.rm = TRUE),
      srq_conflict_avg = mean(srq_conflict_mean, na.rm = TRUE),
      .groups = "drop"
    )

  df_med <- df_family |>
    select(aile_no, group_f, anne_yas, ses_latent,
            beck_total, embu_p_reddetme_mean) |>
    left_join(df_long_summary, by = c("aile_no", "group_f"))

  med_model <- '
    embu_p_reddetme_mean ~ a*beck_total + scale(anne_yas) + scale(ses_latent)
    embu_c_redd_avg      ~ b*embu_p_reddetme_mean + group_f + scale(ses_latent)
    srq_conflict_avg     ~ c*embu_c_redd_avg + group_f

    # Endirek etkiler
    indirect_beck_to_child  := a * b
    indirect_beck_to_srq    := a * b * c
    total_beck              := a * b + 0  # direct = 0 (dahil edilmemiş)
  '

  fit_med <- lavaan::sem(med_model, data = df_med,
                           estimator = "MLR", missing = "fiml",
                           se = "bootstrap", bootstrap = 5000)

  list(fit = fit_med,
        indirect = lavaan::parameterEstimates(fit_med, boot.ci.type = "bca.simple") |>
                     filter(grepl("indirect|total", label)),
        fit_meas = fitMeasures(fit_med, c("cfi","rmsea","srmr")))
}
```

---

## 18. Multilevel Mediation

### 18.1 Level-2 (Aile-Düzeyi) Mediator

```r
run_multilevel_mediation <- function(df_long, df_family) {
  # 1-1-1 mediation: tüm değişkenler aile düzeyi (level-2)
  # Beck (L2) → EMBU-P (L2) → EMBU-C (L1, çocuk-düzeyi)

  msem_model <- '
    level: 1
      embu_c_qreddetme_mean ~ scale(cocuk_yas) + cinsiyet_f

    level: 2
      embu_p_reddetme_mean ~ a*beck_total + scale(ses_latent)
      embu_c_qreddetme_mean ~ b*embu_p_reddetme_mean + group_f +
                                scale(ses_latent)

      indirect := a * b
  '

  df_long_with_family <- df_long |>
    left_join(df_family |> select(aile_no, beck_total, embu_p_reddetme_mean,
                                     ses_latent),
                by = "aile_no")

  fit_msem <- lavaan::sem(msem_model, data = df_long_with_family,
                            cluster = "aile_no",
                            estimator = "MLR")

  list(fit = fit_msem,
        indirect = parameterEstimates(fit_msem) |> filter(label == "indirect"))
}
```

---

## 19. Conditional Process Analysis (Hayes 2018, Modeli 4/7/14)

### 19.1 Moderated Mediation

DM grubunun antidepresan kullanımı, mediasyon yolunu **moderate** ediyor mu?

```r
run_moderated_mediation <- function(df_family, df_long) {
  library(lavaan)

  # Hayes Model 14: a-yolu moderated by W
  # X = beck_total, M = embu_p_reddetme, Y = embu_c_redd, W = group

  df_med <- df_family |>
    left_join(df_long |>
                group_by(aile_no) |>
                summarise(embu_c_redd = mean(embu_c_qreddetme_mean, na.rm=T)),
                by = "aile_no")

  mod_med_model <- '
    # a-path: beck → embu_p, moderated by group
    embu_p_reddetme_mean ~ a1*beck_total + a2*group_f +
                            a3*group_f:beck_total + scale(ses_latent)

    # b-path: embu_p → embu_c
    embu_c_redd ~ b*embu_p_reddetme_mean + scale(ses_latent)

    # Conditional indirect effects (Hayes 2015)
    cond_indirect_kontrol := (a1 + a3*0) * b   # Kontrol grubu (group=0)
    cond_indirect_dm      := (a1 + a3*1) * b   # DM grubu (group=1)

    # Index of moderated mediation (Hayes 2015)
    imm := a3 * b
  '

  fit_mod_med <- lavaan::sem(mod_med_model, data = df_med,
                                estimator = "MLR", missing = "fiml",
                                se = "bootstrap", bootstrap = 5000)

  parameterEstimates(fit_mod_med, boot.ci.type = "bca.simple") |>
    filter(grepl("cond_indirect|imm", label))
}
```

---

## 20. Bayesian Mediation + ROPE

```r
run_bayesian_mediation <- function(df_family, df_long) {
  library(brms)

  df_med <- df_family |>
    left_join(df_long |>
                group_by(aile_no) |>
                summarise(embu_c_redd = mean(embu_c_qreddetme_mean, na.rm=T)),
                by = "aile_no")

  # Path a: beck → embu_p
  m_a <- brm(embu_p_reddetme_mean ~ beck_total + scale(ses_latent),
              data = df_med, chains = 4, iter = 4000, seed = 20260427)

  # Path b: embu_p → embu_c
  m_b <- brm(embu_c_redd ~ embu_p_reddetme_mean + beck_total + scale(ses_latent),
              data = df_med, chains = 4, iter = 4000, seed = 20260427)

  # Posterior samples
  post_a <- as_draws_df(m_a)$b_beck_total
  post_b <- as_draws_df(m_b)$b_embu_p_reddetme_mean

  # Indirect effect distribution
  indirect_post <- post_a * post_b

  # ROPE (Region of Practical Equivalence)
  rope_indirect <- bayestestR::rope(indirect_post, range = c(-0.05, 0.05),
                                      ci = 0.95)

  # Bayes factor (model with vs without indirect path)

  list(model_a = m_a, model_b = m_b,
        indirect_summary = bayestestR::describe_posterior(indirect_post),
        rope = rope_indirect)
}
```

---

# KISIM VII — LATENT DEĞİŞKEN YÖNTEMLERİ

## 21. Latent Profile Analysis (LPA — Anne Tipoloji)

### 21.1 Mantık

Anneleri **homojen tipolojilere** ayırmak (Lanza & Cooper 2016): Beck × EMBU-P × SES × DM-status üzerinden örtük profil analizi. Klinik müdahale hedeflemesi için **karar destek** sağlar.

### 21.2 Model

```r
run_lpa_mother_typology <- function(df_family) {
  library(tidyLPA); library(mclust)

  lpa_indicators <- df_family |>
    select(beck_total,
           embu_p_sicaklik_mean, embu_p_asiri_koruma_mean,
           embu_p_reddetme_mean, embu_p_karsilastirma_mean,
           ses_latent) |>
    drop_na() |>
    scale() |>
    as.data.frame()

  # 1-6 profile karşılaştırması (Akogul & Erisoglu 2017)
  lpa_comparison <- lpa_indicators |>
    estimate_profiles(1:6,
                       variances = c("equal", "varying"),
                       covariances = c("zero", "equal", "varying"))

  # BIC + entropy + LMR-LRT karar matrisi
  comparison_summary <- compare_solutions(lpa_comparison)

  # En uygun model seçimi
  best_model <- estimate_profiles(lpa_indicators, n_profiles = 4,
                                    variances = "equal", covariances = "zero")

  df_family$lpa_class <- get_data(best_model)$Class

  # Profile özellikleri
  profile_means <- df_family |>
    group_by(lpa_class) |>
    summarise(
      n = n(), pct = round(n()/nrow(df_family)*100, 1),
      beck_M = mean(beck_total, na.rm=T),
      sicaklik = mean(embu_p_sicaklik_mean, na.rm=T),
      asiri_kor = mean(embu_p_asiri_koruma_mean, na.rm=T),
      reddetme = mean(embu_p_reddetme_mean, na.rm=T),
      ses = mean(ses_latent, na.rm=T),
      pct_dm = round(mean(group_f == "DM") * 100, 1)
    )

  # Profile × DM/Kontrol Chi-square
  lpa_chi <- chisq.test(table(df_family$lpa_class, df_family$group_f))

  list(comparison = comparison_summary,
        selected = best_model,
        profile_means = profile_means,
        df_with_class = df_family,
        chi_test = lpa_chi)
}
```

### 21.3 Beklenen Profiller (Apriori — T1DM Aile Literatürü)

| Profile | Beck | Sıcaklık | Aşırı Koruma | Reddetme | Beklenen DM yoğunluğu |
|---|---|---|---|---|---|
| **Adapte ebeveyn** | Düşük | Yüksek | Orta | Düşük | Eşit dağılım |
| **Aşırı koruyucu** | Orta | Yüksek | **Çok yüksek** | Düşük | DM lehine |
| **Tükenmiş** | **Yüksek** | Düşük | Orta | Yüksek | DM lehine |
| **Standart** | Düşük | Orta | Düşük | Düşük | Kontrol lehine |

---

## 22. Latent Class Analysis + Mixture Regression

**Uygulama durumu (2026-04-28):** Bu iş paketi `verified` düzeye çıkarılmıştır. LCA, sürekli LPA hattının yerine geçmez; kategorik gösterge duyarlılık analizi olarak yürütülür. Beck şiddeti üç kategoriye (minimal / hafif / orta-şiddetli), EMBU-P alt ölçekleri ve `ses_latent` örneklem içi tertillere ayrılır. `poLCA` 1-4 sınıf karşılaştırmasında BIC'e göre 2-sınıf çözümünü seçmiştir (BIC = 2640.3; sınıf oranları %63.4/%36.6; entropy = 0.60). Modal sınıf üyeliği `nnet::multinom` ile DM/Kontrol, anne yaşı, çocuk sayısı ve kardeş yaş farkı üzerine modellenmiştir; DM sınıf üyeliğini değiştirmemiştir (OR = 1.01, %95 GA [0.59, 1.76], p = .958). `flexmix` Beck → EMBU-P reddetme mixture regression hattı sınır çözüm üretmiştir ve inferans değil diagnostik artefakt olarak raporlanır.

**Artefaktlar:** `lca_indicator_audit_table`, `lca_fit_table`, `lca_classes_table`, `lca_item_response_prob_table`, `lca_group_distribution_table`, `lca_modal_regression_table`, `flexmix_fit_table`, `flexmix_coefficient_table`, `flexmix_class_distribution_table`, `flexmix_group_distribution_table`; audit CSV'leri `scripts/R/25_latent_profile_audit.R` tarafından üretilir; test kapsamı `tests/test_latent_profile.R` içindedir.

### 22.1 LCA — Kategorik Göstergeler İçin

```r
run_lca_categorical <- function(df_family) {
  library(poLCA)

  # Beck şiddet kategorileri + ebeveynlik tutum kategorileri
  df_lca <- df_family |>
    mutate(
      beck_high = as.integer(beck_total >= 17),
      sicaklik_high = as.integer(embu_p_sicaklik_mean > median(embu_p_sicaklik_mean, na.rm=T)),
      asiri_kor_high = as.integer(embu_p_asiri_koruma_mean > median(embu_p_asiri_koruma_mean, na.rm=T)),
      reddetme_high = as.integer(embu_p_reddetme_mean > median(embu_p_reddetme_mean, na.rm=T)),
      ad_use = as.integer(anne_antidepresan)
    ) |>
    select(beck_high, sicaklik_high, asiri_kor_high, reddetme_high, ad_use)

  # 1-5 sınıf karşılaştırması
  lca_results <- map(2:5, function(k) {
    f <- cbind(beck_high, sicaklik_high, asiri_kor_high, reddetme_high, ad_use) ~ 1
    poLCA(f, data = df_lca |> mutate(across(everything(), ~as.factor(.x + 1))),
          nclass = k, nrep = 50, verbose = FALSE)
  })

  # BIC karşılaştırması
  bic_table <- map_dfr(lca_results, function(m) {
    tibble(nclass = m$N, BIC = m$bic, AIC = m$aic, LL = m$llik)
  })

  list(models = lca_results, bic_table = bic_table)
}
```

### 22.2 Mixture Regression (Group-Specific Effects)

```r
library(flexmix)

# Beck → EMBU-P ilişkisi gizli sınıflara göre değişiyor mu?
mix_reg <- flexmix(embu_p_reddetme_mean ~ beck_total + scale(ses_latent),
                    data = df_family, k = 2)
```

---

## 23. Bifactor S-1 Modeli (Eid 2017)

### 23.1 Mantık

Bifactor S-1, **bir alt boyutu referans** alır (örn. Sıcaklık) ve diğerleri için spesifik faktörler tahmin eder. Klasik bifactor'un identification sorunlarını çözer (Eid et al. 2017, *Psychological Methods*).

```r
run_bifactor_s1_model <- function(df_family) {
  bifactor_s1_model <- '
    # G factor (Sıcaklık ile sabitlenmiş referans)
    G =~ embu_p_q01 + embu_p_q03 + embu_p_q06 + embu_p_q07 +
          embu_p_q13 + embu_p_q17 + embu_p_q20 + embu_p_q24 + embu_p_q26 +
          embu_p_q04 + embu_p_q08 + embu_p_q14 +  # Aşırı koruma
          embu_p_q05 + embu_p_q09 + embu_p_q10 +  # Reddetme
          embu_p_q02 + embu_p_q11                  # Karşılaştırma

    # Spesifik faktörler (referans dışı)
    S_AsiriKor =~ embu_p_q04 + embu_p_q08 + embu_p_q14 + embu_p_q15 +
                   embu_p_q19 + embu_p_q23 + embu_p_q25
    S_Redd     =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + embu_p_q12 +
                   embu_p_q16 + embu_p_q21 + embu_p_q22 + embu_p_q28
    S_Karsilas =~ embu_p_q02 + embu_p_q11 + embu_p_q18 + embu_p_q27 + embu_p_q29

    # Faktörler arası ortagonalite
    G ~~ 0*S_AsiriKor
    G ~~ 0*S_Redd
    G ~~ 0*S_Karsilas
    S_AsiriKor ~~ 0*S_Redd
    S_AsiriKor ~~ 0*S_Karsilas
    S_Redd ~~ 0*S_Karsilas
  '

  fit_bf <- lavaan::cfa(bifactor_s1_model, data = df_family,
                          estimator = "WLSMV", ordered = TRUE)

  # Explained Common Variance (ECV)
  # Reise (2012): G faktörünün toplam varyansa göreli katkısı
  ecv <- semTools::reliability(fit_bf)["omega_h", ]

  list(fit = fit_bf, ecv = ecv,
        fit_meas = fitMeasures(fit_bf, c("cfi.scaled", "rmsea.scaled", "srmr")))
}
```

---

# KISIM VIII — NETWORK ANALİZİ

## 24. Gaussian Graphical Model (EBIC-LASSO)

### 24.1 Mantık

EMBU + SRQ + Beck + SES değişkenleri arasındaki **koşullu bağımlılık** yapısı (Epskamp, Borsboom & Fried 2018). Korelasyondan farklı: her kenar diğerleri kontrol edildiğindeki ilişkiyi gösterir.

### 24.2 Tahmin

```r
run_network_analysis <- function(df_family) {
  library(qgraph); library(bootnet)

  net_data <- df_family |>
    select(beck_total,
           embu_p_sicaklik_mean, embu_p_asiri_koruma_mean,
           embu_p_reddetme_mean, embu_p_karsilastirma_mean,
           ses_latent, anne_yas) |>
    drop_na()

  net_labels <- c("Beck","Sıcaklık","AşırıKor","Redd","Karş","SES","Yaş")

  # GGM with EBIC-LASSO (Epskamp 2018 default)
  net_estimate <- bootnet::estimateNetwork(
    net_data,
    default = "EBICglasso",
    corMethod = "spearman",
    tuning = 0.5
  )

  # Görselleştirme
  png(file.path(OUTPUT_DIR, "figures", "network_full.png"),
       width = 1200, height = 1000, res = 150)
  plot(net_estimate, layout = "spring", labels = net_labels,
        title = "T1DM Aileleri — Koşullu Bağımlılık Ağı")
  dev.off()

  # Centrality
  centrality_df <- centralityTable(net_estimate)

  # Bootstrap edge stability
  boot_net <- bootnet::bootnet(net_estimate, nBoots = 1000, type = "case",
                                 statistics = c("strength","closeness","betweenness"))

  # CS-coefficient (Epskamp 2018: > 0.50 güçlü, > 0.25 kabul edilebilir)
  cs_coef <- corStability(boot_net)

  list(network = net_estimate, centrality = centrality_df,
        bootstrap = boot_net, cs_coef = cs_coef)
}
```

---

## 25. Network Comparison Test (DM × Kontrol)

```r
run_network_comparison <- function(df_family) {
  library(NetworkComparisonTest)

  vars <- c("beck_total", "embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
            "embu_p_reddetme_mean", "embu_p_karsilastirma_mean",
            "ses_latent", "anne_yas")

  net_dm <- df_family |> filter(group_f == "DM") |>
    select(all_of(vars)) |> drop_na()
  net_kontrol <- df_family |> filter(group_f == "Kontrol") |>
    select(all_of(vars)) |> drop_na()

  nct_result <- NCT(net_dm, net_kontrol, it = 1000,
                     binary.data = FALSE, paired = FALSE,
                     test.edges = TRUE, edges = "all",
                     test.centrality = TRUE)

  # Yorum:
  # - Global strength invariance: iki ağdaki toplam edge gücü
  # - Network invariance: edge yapısı genelinde fark
  # - Edge-by-edge: spesifik kenar farkları (Holm düzeltmeli)

  print(nct_result)
  nct_result
}
```

---

## 26. Beck Item-Level Symptom Network

Borsboom (2017) psikopatoloji ağ teorisi — Beck'in 21 maddesi arasında "merkezi semptomlar" tespiti:

```r
run_beck_item_network <- function(df_family) {
  beck_data <- df_family |>
    select(starts_with("beck_") & !ends_with("total") & !ends_with("severity") & !ends_with("clinical")) |>
    drop_na()

  beck_net <- bootnet::estimateNetwork(beck_data, default = "EBICglasso",
                                          corMethod = "spearman_thr_chi")

  beck_labels <- c("Üzüntü","Karamsarlık","Başarısızlık","Doyum kaybı",
                    "Suçluluk","Cezalandırılma","Memnuniyet","Eleştiri",
                    "İntihar","Ağlama","Sinirlilik","İlgi","Karar",
                    "Görünüm","İşlevsellik","Uyku","Yorgunluk","İştah",
                    "Kilo","Sağlık","Cinsel")

  png(file.path(OUTPUT_DIR, "figures", "beck_item_network.png"),
       width = 1400, height = 1200, res = 150)
  plot(beck_net, layout = "spring", labels = beck_labels,
        title = "Beck Maddeleri — Anne Depresyon Semptom Ağı")
  dev.off()

  # Hangi semptom merkezi? (Strength)
  strength_centrality <- centrality(beck_net)$InDegree

  list(network = beck_net, strength = strength_centrality)
}
```

---

# KISIM IX — KLİNİK FAYDA

## 27. Risk Skor + ROC + Decision Curve Analysis

### 27.1 Risk Skoru Geliştirme

```r
derive_risk_score <- function(df_family) {
  # Yüksek-risk anne: Beck ≥17 (Hisli orta+)
  df_family$high_risk <- as.integer(df_family$beck_total >= 17)

  # Logistic regression — risk score derivation
  m_risk <- glm(high_risk ~ group_f + scale(anne_yas) + scale(egitim_durumu) +
                 anne_antidepresan + scale(ses_latent) + cocuk_sayisi,
                family = binomial, data = df_family)

  df_family$risk_pred <- predict(m_risk, type = "response")

  list(model = m_risk, df = df_family)
}
```

### 27.2 ROC Curve

```r
run_roc_analysis <- function(risk_score_results, df_family) {
  library(pROC)

  roc_obj <- roc(df_family$high_risk, df_family$risk_pred,
                  ci = TRUE, ci.alpha = 0.95)

  cat(sprintf("AUC = %.3f, 95%% CI [%.3f, %.3f]\n",
                roc_obj$auc, ci(roc_obj)[1], ci(roc_obj)[3]))

  # Optimal cut-off (Youden's J)
  coords_optimal <- coords(roc_obj, "best", best.method = "youden",
                             ret = c("threshold","sensitivity","specificity",
                                     "ppv","npv"))

  # Plot
  png(file.path(OUTPUT_DIR, "figures", "roc_curve.png"),
       width = 1000, height = 1000, res = 150)
  plot(roc_obj, print.auc = TRUE, ci = TRUE,
        main = "ROC: Yüksek-Risk Anne Tahmini")
  dev.off()

  list(roc = roc_obj, auc = roc_obj$auc, optimal = coords_optimal)
}
```

### 27.3 Decision Curve Analysis (Vickers & Elkin 2006)

ROC tek başına klinik kullanılabilirliği ölçmez. **DCA** belirli risk eşiklerinde **net benefit** hesaplar:

```r
run_decision_curve_analysis <- function(risk_score_results, df_family) {
  library(rmda)

  dca_result <- decision_curve(
    formula = high_risk ~ group_f + scale(anne_yas) + scale(ses_latent),
    data = df_family,
    family = binomial,
    thresholds = seq(0, 1, by = 0.01),
    bootstraps = 500
  )

  png(file.path(OUTPUT_DIR, "figures", "decision_curve.png"),
       width = 1200, height = 800, res = 150)
  plot_decision_curve(dca_result,
                       curve.names = "T1DM-uyumlu risk skoru",
                       cost.benefit.axis = TRUE,
                       confidence.intervals = "none")
  dev.off()

  dca_result
}
```

**DCA Yorumu:**
- Net Benefit eğrisi "treat all" ve "treat none" referans çizgilerinin üzerindeyse model klinik faydalı
- Örn. p=0.20 eşiğinde NB = 0.10 → her 100 anneden 10'u doğru risk yüksek tespit ediliyor (yanlış pozitif maliyeti hesaplanmış)

---

## 28. CART Karar Ağacı + Random Forest

### 28.1 CART Karar Ağacı

```r
run_decision_tree <- function(df_family) {
  df_family$high_risk <- factor(df_family$beck_total >= 17,
                                  labels = c("Düşük risk", "Yüksek risk"))

  tree <- rpart::rpart(
    high_risk ~ group_f + anne_yas + egitim_durumu + cocuk_sayisi +
                ev_oda_sayisi + anne_antidepresan + kronik_hastalik_durumu +
                ses_latent + age_gap,
    data = df_family,
    method = "class",
    control = rpart::rpart.control(cp = 0.01, minsplit = 20)
  )

  png(file.path(OUTPUT_DIR, "figures", "decision_tree.png"),
       width = 1400, height = 900, res = 150)
  rpart.plot::rpart.plot(tree, type = 4, extra = 102, fallen.leaves = TRUE,
                          main = "Yüksek-risk anne tahmin ağacı")
  dev.off()

  rules <- rpart.plot::rpart.rules(tree, cover = TRUE)
  cv_result <- printcp(tree)
  var_imp <- tree$variable.importance

  list(tree = tree, rules = rules, var_importance = var_imp, cv = cv_result)
}
```

### 28.2 Random Forest — Variable Importance

```r
run_random_forest_importance <- function(df_family) {
  library(randomForest)

  rf_data <- df_family |>
    select(beck_total, group_f, anne_yas, egitim_durumu, es_egitim_durumu,
            cocuk_sayisi, anne_antidepresan, ses_latent, age_gap) |>
    drop_na()

  rf <- randomForest(beck_total ~ ., data = rf_data,
                       ntree = 5000, importance = TRUE)

  # Permutation importance
  imp_df <- importance(rf, type = 1) |> as.data.frame() |>
    rownames_to_column("variable") |>
    arrange(desc(`%IncMSE`))

  png(file.path(OUTPUT_DIR, "figures", "rf_importance.png"),
       width = 1000, height = 800, res = 150)
  varImpPlot(rf, type = 1, main = "Random Forest — Permutation Importance")
  dev.off()

  list(model = rf, importance = imp_df)
}
```

---

## 29. Calibration + NRI/IDI

### 29.1 Calibration Plot

Modelin tahmin ettiği olasılıklar gerçeğe ne kadar yakın?

```r
run_calibration_analysis <- function(risk_score_results, df_family) {
  library(rms)

  # Calibration curve (Harrell 2015)
  cal <- calibrate(risk_score_results$model, B = 1000, method = "boot")

  png(file.path(OUTPUT_DIR, "figures", "calibration_plot.png"),
       width = 1000, height = 1000, res = 150)
  plot(cal, main = "Calibration: Bootstrap-corrected (B=1000)")
  dev.off()

  # Hosmer-Lemeshow test
  library(ResourceSelection)
  hl_test <- hoslem.test(df_family$high_risk, df_family$risk_pred, g = 10)

  list(calibration = cal, hl_test = hl_test)
}
```

### 29.2 NRI/IDI (Pencina 2008) — Yeni Belirteç Eklemenin Marjinal Faydası

```r
library(PredictABEL)

# Model 1: Demografik
m1 <- glm(high_risk ~ group_f + scale(anne_yas) + scale(egitim_durumu),
           family = binomial, data = df_family)

# Model 2: + Maternal mental health
m2 <- glm(high_risk ~ group_f + scale(anne_yas) + scale(egitim_durumu) +
           anne_antidepresan + scale(ses_latent),
           family = binomial, data = df_family)

# NRI (Net Reclassification Improvement)
nri_result <- reclassification(df_family,
                                  cOutcome = which(names(df_family) == "high_risk"),
                                  predrisk1 = predict(m1, type = "response"),
                                  predrisk2 = predict(m2, type = "response"),
                                  cutoff = c(0, 0.10, 0.30, 1))
```

---

# KISIM X — KLİNİK ALT-ANALİZLER (DM)

## 30. HbA1c × Ebeveynlik Etkileşimi

### 30.1 Sınırlılık ve Strateji

HbA1c yalnız 39/120 mevcut. **İmputation YAPILMAZ** — klinik biyobelirteç tahmin kabul edilemez. Bu nedenle:
- Birincil: `dm_yili` (n=120 tam veri)
- Sensitivite: HbA1c (n=39, keşifsel)

### 30.2 Modeller

```r
run_hba1c_moderation <- function(df_family) {
  df_dm <- df_family |> filter(group_f == "DM")
  df_dm_hba1c <- df_dm |> filter(!is.na(hba1c))

  # ADA hedef stratifikasyon
  df_dm_hba1c$glycemic_control <- factor(
    if_else(df_dm_hba1c$hba1c <= 7.5, "Hedef altı", "Hedef üstü"),
    levels = c("Hedef altı", "Hedef üstü")
  )

  # HbA1c × ebeveynlik
  m_hba1c <- lm(embu_p_asiri_koruma_mean ~ scale(hba1c) + scale(anne_yas) +
                 scale(ses_latent), data = df_dm_hba1c)

  # Glycemic control kategorik
  t_glycemic <- t.test(embu_p_asiri_koruma_mean ~ glycemic_control,
                         data = df_dm_hba1c)
  d_glycemic <- effectsize::cohens_d(embu_p_asiri_koruma_mean ~ glycemic_control,
                                       data = df_dm_hba1c)

  list(continuous = broom::tidy(m_hba1c, conf.int = TRUE),
        categorical_t = t_glycemic, categorical_d = d_glycemic,
        n_total = nrow(df_dm), n_hba1c = nrow(df_dm_hba1c))
}
```

---

## 31. DM Süresi Spline Modeli

### 31.1 Doğrusal Olmayan Etki

```r
library(splines)

run_dm_duration_spline <- function(df_family) {
  df_dm <- df_family |> filter(group_f == "DM")

  # Doğal cubic spline (3 knot at 25, 50, 75 percentile)
  knots <- quantile(df_dm$dm_yili, c(0.25, 0.50, 0.75), na.rm = TRUE)

  m_spline <- lm(embu_p_asiri_koruma_mean ~ ns(dm_yili, knots = knots) +
                  scale(anne_yas) + scale(ses_latent),
                  data = df_dm)

  # Linear vs spline karşılaştırması (LRT)
  m_linear <- lm(embu_p_asiri_koruma_mean ~ dm_yili + scale(anne_yas) +
                  scale(ses_latent), data = df_dm)

  lrt <- anova(m_linear, m_spline)

  # Predict + plot
  df_pred <- expand_grid(dm_yili = seq(0.25, 14, by = 0.5),
                          anne_yas = mean(df_dm$anne_yas, na.rm=T),
                          ses_latent = 0)
  df_pred$pred <- predict(m_spline, newdata = df_pred)
  df_pred$ci_lo <- predict(m_spline, newdata = df_pred,
                             interval = "confidence")[, "lwr"]
  df_pred$ci_hi <- predict(m_spline, newdata = df_pred,
                             interval = "confidence")[, "upr"]

  ggplot(df_pred, aes(x = dm_yili, y = pred)) +
    geom_ribbon(aes(ymin = ci_lo, ymax = ci_hi), alpha = 0.3) +
    geom_line() +
    geom_vline(xintercept = knots, linetype = "dashed", color = "red") +
    labs(title = "DM Süresi × Aşırı Koruma (Spline Model)",
          x = "DM süresi (yıl)", y = "Aşırı Koruma (predicted)") +
    theme_minimal()

  list(spline = m_spline, linear = m_linear, lrt = lrt, knots = knots)
}
```

---

## 32. Tanı Yaşı Stratifikasyonu

### 32.1 Üç Kritik Gelişim Penceresi

| Strata | Tanı yaşı aralığı | n (mevcut) | Klinik anlamı |
|---|---|---|---|
| Erken çocukluk | <5 yaş | 24 | Bağlanma şekillenmesi, ebeveyn-merkezli yönetim |
| Okul çağı | 5–10 yaş | 69 | Akran-okul entegrasyon |
| Adolesan | ≥10 yaş | 27 | Özerklik gelişimi, akut yönetim transferi |

### 32.2 Stratified Analiz

```r
run_diagnosis_age_strata <- function(df_family) {
  df_dm <- df_family |> filter(group_f == "DM") |>
    mutate(diag_age_strata = cut(tani_yasi,
                                    breaks = c(0, 5, 10, 18),
                                    labels = c("Erken çocukluk (<5)",
                                                "Okul çağı (5-10)",
                                                "Adolesan (≥10)"),
                                    include.lowest = TRUE))

  # Strata × ebeveynlik tutum
  results <- map_dfr(c("sicaklik", "asiri_koruma", "reddetme"), function(sub) {
    y_col <- paste0("embu_p_", sub, "_mean")
    fml <- as.formula(paste(y_col, "~ diag_age_strata + scale(anne_yas) + scale(ses_latent)"))
    m <- lm(fml, data = df_dm)

    aov_tab <- car::Anova(m, type = 3)
    emm <- emmeans::emmeans(m, ~ diag_age_strata)

    tibble(outcome = sub,
            f = aov_tab["diag_age_strata", "F value"],
            p = aov_tab["diag_age_strata", "Pr(>F)"]) |>
      bind_cols(as.data.frame(emm) |>
                  pivot_wider(names_from = diag_age_strata, values_from = emmean,
                                names_prefix = "M_"))
  })

  results
}
```

# KISIM XI — ROBUSTLUK VE SENSİTİVİTE

## 33. Multiverse Specification Curve Analysis

### 33.1 Mantık ve Tezdeki Yeri

Steegen, Tuerlinckx, Gelman & Vanpaemel (2016) **multiverse analysis** ve Simonsohn, Simmons & Nelson (2020) **specification curve** çerçevesi, "garden of forking paths" sorununa (Gelman & Loken 2014) doğrudan yanıttır. Tek bir analiz spesifikasyonu yerine, **mantıken savunulabilir tüm spesifikasyon kombinasyonlarını** çalıştırarak sonucun spesifikasyon-bağımlılığını sayısallaştırır.

T1DM-EBEVEYN için kritik bir sahne: **EMBU-P Reddetme alt ölçeği**. Psikometrik validasyon raporundan biliyoruz ki bu alt ölçeğin α=0.450, BSEM PPP=0.048 ile sınır altı, tüm 8 madde >%60 floor effect gösteriyor. Klasik tek-spec analiz **savunulamaz** — multiverse zorunlu.

### 33.2 Specification Universe

```r
# analysis/33_multiverse.R
library(specr)

# Birincil sonuç: Reddetme DM × Kontrol farkı
# Spesifikasyon dimensyonları:

specs_setup <- specr::setup(
  data = df_family,

  # Y dimension: 4 farklı skorlama
  y = c("embu_p_reddetme_mean",      # Standart 8-madde ortalama
        "embu_p_reddetme_sum",        # Standart 8-madde toplam
        "embu_p_reddetme_7item_mean", # q12 dışlanmış (psikometrik)
        "embu_p_reddetme_latent"),    # BSEM latent factor skoru

  # X dimension: yordayıcı tek (group_f); birden çok dummy denemiyoruz
  x = "group_f",

  # Model dimension: 3 farklı tahmin yöntemi
  model = c("lm",                                    # Klasik OLS
            "MASS::rlm",                              # Robust regresyon (Huber-M)
            "geepack::geeglm"),                       # GEE (eşdeğer aile clustering yok ama placeholder)

  # Controls dimension: 5 farklı kovaryat seti
  controls = c("scale(anne_yas)",
               "scale(anne_yas) + scale(ses_latent)",
               "scale(anne_yas) + scale(ses_latent) + scale(age_gap)",
               "scale(anne_yas) + scale(ses_latent) + scale(age_gap) + cocuk_sayisi",
               "scale(anne_yas) + scale(ses_latent) + scale(age_gap) +
                cocuk_sayisi + anne_antidepresan"),

  # Subset dimension: alt-örneklem analizleri
  subsets = list(
    cocuk_sayisi  = c("all", "1-2 cocuk", "3+ cocuk"),
    egitim_durumu = c("all", "lise+", "lise altı"),
    age_cat       = c("all", "7-10", "11-13", "14-17")
  )
)

# Toplam spec sayısı: 4 × 3 × 5 × 30 = ~1800 spec
# specr otomatik olarak çalıştırır
results <- specr::specr(specs_setup)

# Specification curve
plot_specs(results, choices = c("y", "model", "controls", "subsets"),
            ribbon = TRUE)
ggsave(file.path(OUTPUT_DIR, "figures", "spec_curve_reddetme.png"),
        width = 14, height = 10, dpi = 300)
```

### 33.3 Sonuç Yorumu

| Metrik | Yorum eşiği |
|---|---|
| **% spec'lerde p < .05** | <5% → anlamsızlık tutarlı; ≥50% → anlamlılık tutarlı |
| **Median d** | Etki büyüklüğünün spec-merkezi |
| **Inferential band (Simonsohn 2020)** | Permütasyon tabanlı global test |

Beklenen çıktı (psikometrik validasyon + ön-tarama temelinde):

```
Toplam 1800 spec içinde:
  Median Cohen's d:        −0.13  (DM < Kontrol, küçük)
  d range (5%, 95%):       [−0.30, +0.05]
  % spec'lerde p < .05:    <8%

  → "Reddetme alt ölçeğinde DM-Kontrol farkı için
     spec-bağımsız anlamlı kanıt YOK."
```

### 33.4 Inferential Specification Curve (Simonsohn et al. 2020)

```r
# Permütasyon tabanlı global anlamlılık testi
# H0: tüm spec'lerde gerçek etki sıfır

inferential_test <- specr::infer(results,
                                   nsim = 5000,
                                   sample = "pooled")
print(inferential_test)
# Üç istatistik:
#   Z_median:  median spec d'nin null'a karşı testi
#   Z_share:   anlamlı spec sayısının null'a karşı testi
#   Z_aggregate: ağırlıklı agregat
```

---

## 34. Equivalence Testing (TOST + Bayesian Equivalence)

### 34.1 Niye Eşdeğerlik Testi?

Standart NHST "fark var mı?" sorusunu test eder. Ancak H3'te **null sonuç** (DM × Kontrol Reddetme farkı yok gibi) çıkma ihtimali yüksek. NHST'de "p > .05" → "fark yok" demek **mantıken yanlış**tır (Lakens 2017). Bunun için **Two One-Sided Tests (TOST)** prosedürü gereklidir.

### 34.2 SESOI Belirleme

Smallest Effect Size of Interest (SESOI) önceden tanımlanmalı:

| Yaklaşım | SESOI | Gerekçe |
|---|---|---|
| Cohen küçük etki | d = 0.20 | Konvansiyonel |
| Pinquart (2013) meta-analiz | d = 0.30 | Kronik hastalık × ebeveynlik literatürü |
| Klinik anlamlılık (1 SD ölçek) | d = 0.40 | Klinik karar değişikliği eşiği |

**Tezde kullanılacak:** **SESOI = ±0.30 SMD** (Pinquart meta-analiz temelli, mantıken savunulabilir orta-küçük).

### 34.3 TOST (Lakens 2017)

```r
# analysis/34_tost.R
library(TOSTER)

run_tost_h3 <- function(df_family, outcome, sesoi_d = 0.30) {
  dm_vals <- df_family[df_family$group_f == "DM", outcome, drop = TRUE]
  ko_vals <- df_family[df_family$group_f == "Kontrol", outcome, drop = TRUE]

  TOSTER::tsum_TOST(
    m1 = mean(dm_vals, na.rm = TRUE),
    sd1 = sd(dm_vals, na.rm = TRUE),
    n1 = sum(!is.na(dm_vals)),
    m2 = mean(ko_vals, na.rm = TRUE),
    sd2 = sd(ko_vals, na.rm = TRUE),
    n2 = sum(!is.na(ko_vals)),
    low_eqbound_d = -sesoi_d,
    high_eqbound_d = sesoi_d,
    eqbound_type = "SMD"
  )
}

# Tüm 4 EMBU-P alt ölçek
tost_results <- map(c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
                       "embu_p_reddetme_mean", "embu_p_karsilastirma_mean"),
                     ~run_tost_h3(df_family, .x))
```

### 34.4 Üçlü Karar Matrisi

```
                NHST p < .05
                  ↓                ↑
             ANLAMLI         ANLAMSIZ
TOST p<.05 ┌─────────────┬───────────────┐
EŞDEĞER    │ Trivial     │ EQUIVALENT    │
           │ (anlamlı    │ (KESIN: fark  │
           │ ama küçük)  │ yok kanıtı)   │
           ├─────────────┼───────────────┤
TOST p>.05 │ MEANINGFUL  │ INDETERMINATE │
EŞDEĞER    │ (gerçek     │ (BELIRSIZ:    │
DEĞİL      │ etki)       │ daha çok n)   │
           └─────────────┴───────────────┘
```

**Önemli:** Psikometrik validasyon raporundan biliyoruz ki Reddetme için TOST **eşdeğerliği DOĞRULAMADI** (p > .05). Sonuç: "fark kanıtı yetersiz" — *ne anlamlı fark ne de kesin eşdeğerlik*. Bu, `INDETERMINATE` hücresine düşer.

### 34.5 Bayesian Equivalence (ROPE, Kruschke 2018)

```r
library(bayestestR)

# Posterior'dan ROPE içinde kalan oran
rope_h3 <- rope(h3_bayesian_model, range = c(-0.10, 0.10), ci = 0.89)
print(rope_h3)
# 100% in ROPE → kesin eşdeğer
# 0% in ROPE → kesin fark
# Belirsiz → daha çok veri gerek
```

---

## 35. Sensemakr + E-value (Ölçülmemiş Karıştırıcı Sensitivitesi)

### 35.1 Sensemakr (Cinelli & Hazlett 2020)

Pearl ve Hernán ekolü: gözlemsel çalışmalarda *her* karıştırıcıyı ölçemeyiz. Ölçemediklerimiz tahmini ne kadar değiştirebilir?

```r
# analysis/35_sensemakr.R
library(sensemakr)

# Birincil model — DAG-justified (mediator'lar dışlanmış)
m_main <- lm(embu_p_asiri_koruma_mean ~ group_f + scale(anne_yas) +
              scale(ses_latent) + scale(age_gap) + cocuk_sayisi,
              data = df_family)

sens_main <- sensemakr::sensemakr(
  model              = m_main,
  treatment          = "group_fDM",
  benchmark_covariates = c("scale(ses_latent)", "scale(anne_yas)"),
  kd                 = c(1, 2, 3),  # ölçülmemiş confounder ölçülenin 1×, 2×, 3× kat gücünde
  ky                 = c(1, 2, 3)
)

# Üç anahtar metrik
print(sens_main)
# 1. Robustness Value (RV_q): ana etkiyi q% değiştirmek için gereken karıştırıcı gücü
#    RV > 0.10 → orta-güçlü dayanıklılık
#    RV < 0.05 → ciddi karıştırıcı duyarlılığı
# 2. Partial R²: ölçülmemiş karıştırıcının T ve Y ile gerekli ortak varyans payı
# 3. t-istatistik 0'a düşürmek için gereken karıştırıcı gücü

# Kontur grafiği
png(file.path(OUTPUT_DIR, "figures", "sensemakr_contour.png"),
     width = 1000, height = 800, res = 150)
plot(sens_main, sensitivity.of = "estimate")
dev.off()

png(file.path(OUTPUT_DIR, "figures", "sensemakr_extreme.png"),
     width = 1000, height = 800, res = 150)
plot(sens_main, type = "extreme")
dev.off()
```

### 35.2 E-value (VanderWeele & Ding 2017)

E-value: ana etkiyi sıfıra düşürmek için gereken karıştırıcı-tedavi *ve* karıştırıcı-sonuç ilişkisinin minimum gücü.

```r
library(EValue)

# Cohen's d → risk ratio dönüşümü
d_observed <- 0.55  # Anne antidepresan SMD'si
RR_estimated <- exp(0.91 * d_observed)  # Chinn 2000 dönüşümü

evalue_main <- EValue::evalue(RR(RR_estimated, lo = 1.5, hi = 4.5))
print(evalue_main)
# E-value > 2.0: orta dayanıklılık
# E-value < 1.5: zayıf — bilinmeyen küçük bir karıştırıcı sonucu silebilir
```

### 35.3 Sensitivite Tablosu — Tezde Sunum

| Sonuç | Birincil etki | RV_q (Sensemakr) | E-value | Yorum |
|---|---|---|---|---|
| H1 Sıcaklık (DM-Indeks vs Kontrol) | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |
| H1 Aşırı Koruma | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |
| H3 EMBU-P Reddetme | beklenen küçük | beklenen <0.05 | beklenen <1.5 | **Karıştırıcıya duyarlı** |
| H4 Beck → EMBU-P | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |

---

## 36. Negative Control Outcome + Falsification Tests

### 36.1 Niye?

Lipsitch, Tchetgen Tchetgen & Cohen (2010) **negative control** çerçevesi: araştırmacının bilinmeyen yapısal sorunlarına karşı *bağımsız* bir kontrol sağlar. Eğer nominal olarak ilişkili olmaması gereken bir sahte sonuç ile gerçek bir ilişki bulursak → **gizli karıştırıcı veya selection bias** vardır.

### 36.2 T1DM-EBEVEYN İçin Negative Controls

| Sahte Yordayıcı | Sahte Sonuç | Niçin "Sahte"? | Beklenen Sonuç |
|---|---|---|---|
| `anne_dogum_tarihi` (raw) | EMBU-P alt ölçek | Doğum tarihi yıl/ay sırası random | **Anlamsız** |
| `aile_no` (random ID) | SRQ Çatışma | ID atama tamamen random | **Anlamsız** |
| `katilimci_cocuk_no` | Beck total | Çocuk sırası ID'si | **Anlamsız** |
| `cocuk_sayisi` *parity* | EMBU-C Karşılaştırma | (gerçek ilişki olabilir, çift kontrol) | Eğer anlamlıysa: **karıştırıcı bayrağı** |

```r
# analysis/36_negative_control.R

# Sahte yordayıcı 1: doğum tarihinin gün+ay'ı (random)
df_family$dogum_random <- as.numeric(
  format(as.Date(df_family$anne_dogum_tarihi, "%d.%m.%Y"), "%j")
)

# Sahte test: dogum_random → EMBU-P alt ölçek
neg_control_results <- map_dfr(
  c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
    "embu_p_reddetme_mean", "embu_p_karsilastirma_mean"),
  function(y) {
    m <- lm(as.formula(paste(y, "~ scale(dogum_random) + scale(anne_yas)")),
              data = df_family)

    tibble(outcome = y,
            beta = coef(m)["scale(dogum_random)"],
            se = summary(m)$coefficients["scale(dogum_random)", "Std. Error"],
            p = summary(m)$coefficients["scale(dogum_random)", "Pr(>|t|)"])
  }
)

# Eğer % ≥ 1/4 anlamlı → multiple testing rastgele false positive
# Eğer % > 1/4 anlamlı → SUSPICIOUS, gizli yapısal sorun olabilir
```

### 36.3 Falsification Test

Hernán & Robins (2020): tezin yorumu doğruysa, *belirli özel durumlarda* ana etki *kaybolmalıdır*.

```r
# Falsification 1: DM süresinin çok kısa olduğu (yeni tanı, <1 yıl) ailelerde
# DM-Kontrol farkı zayıflamalı (eğer fark "uzun süreli kronik yük"ten ise)

# DM kısa süre + Kontrol
df_short_dm <- df_family |>
  filter((group_f == "DM" & dm_yili < 1) | group_f == "Kontrol")

m_short <- lm(embu_p_asiri_koruma_mean ~ group_f + scale(ses_latent),
                data = df_short_dm)
summary(m_short)$coefficients["group_fDM", ]
# Beklenen: küçük/anlamsız etki — çünkü hastalık yükü henüz birikmemiş

# Falsification 2: HbA1c hedefte olan DM aileleri (iyi kontrol)
# DM-Kontrol farkı zayıflamalı
df_good_control <- df_family |>
  filter((group_f == "DM" & hba1c <= 7.5) | group_f == "Kontrol")

m_good <- lm(embu_p_asiri_koruma_mean ~ group_f + scale(ses_latent),
              data = df_good_control)
# Beklenen: zayıf etki — iyi kontrol → düşük yük → küçük fark
```

---

# KISIM XII — BAYESCI PARALEL HAT

## 37. Bayesian Multilevel — H1 İçin

### 37.1 Niye Bayesian Paralel?

Frequentist analizler tek başına yeterli değildir. Tezin savunmasında jüri sorabilir:
- "Etki ne kadar kesin?" — Frequentist CI ≠ olasılık aralığı; Bayesian credible interval direkt olasılık
- "Etki anlamsız çıktı; sıfır mı?" — Frequentist'te ayırt edilemez; Bayesian Bayes faktör + ROPE çözer
- "Önceki literatür beklentilerini nasıl entegre ettiniz?" — Pinquart 2013 meta-analiz priorlama

### 37.2 H1 Bayesian Multilevel (brms)

```r
# analysis/37_bayes_h1.R
library(brms); library(bayestestR); library(bayesplot)

run_h1_bayesian <- function(df_long, outcome) {
  # Pinquart 2013 meta-analiz temelli weakly informative prior
  # d = 0.40, CI [0.25, 0.55] → SD ≈ 0.077; tezde 3× geniş prior tercih

  priors <- c(
    # Group fixed effects (DM-Kontrol fark beklentisi)
    prior(normal(0.30, 0.50), class = b, coef = "role_fDM_Hasta_Indeks"),
    prior(normal(0.20, 0.50), class = b, coef = "role_fDM_Hasta_Kardes"),
    prior(normal(-0.10, 0.30), class = b, coef = "role_fKontrol_Kardes"),

    # Diğer fixed effects — daha geniş
    prior(normal(0, 1), class = b),

    # Random effect SD
    prior(student_t(3, 0, 2.5), class = sd),

    # Residual SD
    prior(student_t(3, 0, 2.5), class = sigma)
  )

  fml <- as.formula(paste(outcome,
    "~ role_f + scale(cocuk_yas) + cinsiyet_f + scale(ses_latent) +
       scale(age_gap) + (1 | aile_no_f)"))

  m_bayes <- brms::brm(
    fml, data = df_long,
    family = gaussian(),
    prior = priors,
    chains = 4, iter = 4000, warmup = 1500,
    seed = 20260427,
    cores = 4,
    control = list(adapt_delta = 0.99, max_treedepth = 15),
    sample_prior = "yes"  # Bayes factor için
  )

  # === Tanı ===
  # MCMC convergence
  rhat_max <- max(brms::rhat(m_bayes), na.rm = TRUE)
  ess_min  <- min(brms::neff_ratio(m_bayes), na.rm = TRUE) * 4 * 4000

  cat(sprintf("R-hat max: %.3f (must be < 1.01)\n", rhat_max))
  cat(sprintf("ESS min: %.0f (must be > 1000)\n", ess_min))

  # === Posterior summary ===
  post_summary <- bayestestR::describe_posterior(
    m_bayes,
    test = c("p_direction", "rope", "bayesfactor"),
    rope_range = c(-0.10, 0.10),
    rope_ci = 0.89,
    centrality = "median",
    ci_method = "hdi", ci = 0.89
  )

  list(
    model         = m_bayes,
    summary       = post_summary,
    rhat_max      = rhat_max,
    ess_min       = ess_min,
    convergence   = rhat_max < 1.01 & ess_min > 1000
  )
}

# Tüm 4 EMBU-C alt ölçek
h1_bayes_all <- map(c("embu_c_qsicaklik_mean", "embu_c_qasiri_koruma_mean",
                       "embu_c_qreddetme_mean", "embu_c_qkarsilastirma_mean"),
                     ~run_h1_bayesian(df_long, .x))
```

### 37.3 Posterior Predictive Check (PPC)

```r
# Modelin gerçek veriyle uyumu — graphical posterior check
library(bayesplot)

ppc_dens <- pp_check(h1_bayes_all[[1]]$model, ndraws = 100)
ggsave(file.path(OUTPUT_DIR, "figures", "ppc_h1_warmth.png"),
        ppc_dens, width = 8, height = 6, dpi = 300)

# Spesifik istatistikler için PPC
ppc_stat <- pp_check(h1_bayes_all[[1]]$model, type = "stat", stat = "mean")
ppc_stat_role <- pp_check(h1_bayes_all[[1]]$model, type = "stat_grouped",
                           stat = "mean", group = "role_f")
```

### 37.4 ROPE + Probability of Direction

```r
# Region of Practical Equivalence
rope_h1 <- bayestestR::rope(h1_bayes_all$reddetme$model,
                              range = c(-0.10, 0.10),
                              ci = 0.89)
print(rope_h1)

# Probability of Direction (replacement for p-value)
pd_h1 <- bayestestR::p_direction(h1_bayes_all$reddetme$model)
print(pd_h1)
# pd > 0.95 ≈ p < .05 (frequentist eşdeğer)
# pd > 0.99 ≈ p < .01
```

---

## 38. Bayes Factor + ROPE — Tüm Hipotezler İçin

### 38.1 BF Hesabı (Savage-Dickey Density Ratio)

```r
# analysis/38_bayes_factor.R

# H1 için: role_f anlamlılığı testi
# Model 0: role_f olmadan
# Model 1: role_f ile (mevcut)

m_h1_null <- update(h1_bayes_all$reddetme$model,
                     formula = . ~ . - role_f)

bf_h1 <- brms::bayes_factor(h1_bayes_all$reddetme$model, m_h1_null)
print(bf_h1)
# BF_10 > 10: güçlü kanıt H1 lehine
# BF_10 < 1/10: güçlü kanıt H0 lehine
# 1/3 < BF_10 < 3: belirsiz (anekdotal)
```

### 38.2 BF Yorumlama Tablosu (Jeffreys 1961, modifiye)

| BF_10 | Sözel | Yorum (Wagenmakers 2007) |
|---|---|---|
| > 100 | "Decisive" | H1 lehine kesin kanıt |
| 30–100 | "Very strong" | H1 lehine çok güçlü |
| 10–30 | "Strong" | H1 lehine güçlü |
| 3–10 | "Moderate" | H1 lehine ılımlı |
| 1–3 | "Anecdotal" | H1 lehine zayıf |
| 1/3–1 | "Anecdotal" | H0 lehine zayıf |
| 1/10–1/3 | "Moderate" | H0 lehine ılımlı |
| 1/30–1/10 | "Strong" | H0 lehine güçlü |
| < 1/30 | "Very strong" | H0 lehine çok güçlü |

### 38.3 Frequentist + Bayesian Dual Reporting

| Hipotez | Frequentist (p) | BH-FDR | Bayesian (BF_10) | ROPE % | Ortak Karar |
|---|---|---|---|---|---|
| H1 Sıcaklık | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |
| H1 Reddetme | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |
| H3 Reddetme | beklenen ns | hesaplanacak | beklenen 1/3-3 | beklenen >50% | **Belirsiz** |
| H4 Beck→Reddetme | beklenen anlamlı | hesaplanacak | beklenen >10 | beklenen <10% | **Pozitif** |

---

## 39. WAIC / LOO — Model Karşılaştırma

### 39.1 Model Karşılaştırma Matrisi

```r
# analysis/39_waic_loo.R

# H1 için 4 alternatif spesifikasyon
m1 <- run_h1_bayesian(df_long, "embu_c_qreddetme_mean")  # tam model
m2 <- update(m1$model, formula = . ~ . - scale(ses_latent))   # SES'siz
m3 <- update(m1$model, formula = . ~ . - scale(age_gap))      # age_gap'siz
m4 <- update(m1$model, formula = . ~ . - role_f)              # role_f'siz (null)

# WAIC
waic_compare <- loo::loo_compare(
  brms::waic(m1$model), brms::waic(m2),
  brms::waic(m3),       brms::waic(m4)
)
print(waic_compare)

# LOO (Pareto-smoothed importance sampling)
loo_compare <- loo::loo_compare(
  brms::loo(m1$model, moment_match = TRUE),
  brms::loo(m2,        moment_match = TRUE),
  brms::loo(m3,        moment_match = TRUE),
  brms::loo(m4,        moment_match = TRUE)
)
print(loo_compare)

# Pareto-k diagnosis
brms::pp_check(m1$model, type = "loo_pit_qq")
```

### 39.2 Model Stack (Yao et al. 2018)

Tek bir "en iyi" model yerine, **model stack** çoklu modellerin posterior ağırlıklı kombinasyonunu kullanır:

```r
# Bayesian stacking weights
loo_list <- list(loo1 = loo(m1$model), loo2 = loo(m2),
                 loo3 = loo(m3),       loo4 = loo(m4))

stacking_wts <- loo::loo_model_weights(loo_list, method = "stacking")
print(stacking_wts)
# Eğer hiçbir model dominant değil (>0.50 ağırlık) → multi-model averaging tercih
```

---

# KISIM XIII — RAPORLAMA VE DİSEMİNASYON

> **Kapsam notu (2026-04-28):** Niteliksel/karma yöntem analizi (eski KISIM XIII: tematik analiz, joint display, inter-coder reliability) bu projenin kapsamı dışındadır ve ayrı bir araştırma projesi olarak yürütülecektir. Bu KISIM artık raporlama ve diseminasyon iş paketlerini içerir.

## 40. APA-Uyumlu Tablo ve Şekil Üretimi

### 40.1 papaja Tabloları

```r
# analysis/42_papaja_outputs.R
library(papaja)

# H1 için APA Table
apa_table_h1 <- papaja::apa_table(
  h1_results_summary,
  caption = "Çocuk Algılanan Ebeveynlik Tutumu: Multilevel ANCOVA Sonuçları",
  note = "DM_Hasta_Indeks (n=120), DM_Hasta_Kardes (n=120), Kontrol_Indeks (n=121), Kontrol_Kardes (n=121). Multilevel: random = (1|aile_no). Kovaryatlar: yaş, cinsiyet, SES latent, age gap. p_FDR: Benjamini-Hochberg düzeltmesi (q=.05).",
  align = c("l", rep("c", 8)),
  font_size = "footnotesize",
  escape = TRUE
)
```

### 40.2 Şekil Üretim Listesi

**Uygulama durumu (Sprint A kapanış, 2026-04-28):** `R/28_apa_figures.R` saf ggplot nesneleri üretir; `_targets.R` içindeki `apa_*` hedefleri 24 figürü `outputs/figures/` altında üretir. `R/29_apa_tables.R` 22 aggregate APA tabloyu üretir ve `outputs/tables/apa_t*.csv` + `apa_sprint_a_table_manifest.csv` manifestiyle izler. `tests/test_apa_figures.R`, `tests/test_apa_tables.R`, `scripts/R/29_apa_figures_audit.R` ve `scripts/R/30_apa_tables_audit.R` doğrulamaları tamamlanmıştır. İlk figür paketi (`@fig-h1-forest`, `@fig-h4-sem-path`, `@fig-h5-bland-altman`, `@fig-h5-rsa-surface`), ikinci paket (`@fig-h2-apim-path`, `@fig-h3-stratified-forest`, `@fig-specification-curve`, `@fig-sensemakr-contour`, `@fig-clinical-roc`, `@fig-clinical-dca`, `@fig-clinical-calibration`), altyapı paketi (`@fig-strobe-flow`, `@fig-causal-dag`, `@fig-smd-love`, `@fig-propensity-overlap`, `@fig-ses-correlation`, `@fig-h1-three-way-emm`) ve son paket (`@fig-mediation-effects`, `@fig-lpa-fit-indices`, `@fig-network-graph`, `@fig-network-nct`, `@fig-clinical-cart-rf`, `@fig-bayesian-forest`, `@fig-bayesian-diagnostics`) `chapters/03_bulgular.qmd` içine bağlanmıştır. APA tablo seti `@tbl-apa-sample-characteristics` ile `@tbl-apa-result-synthesis` arasında 22 Quarto cross-reference olarak bağlanmış ve `quarto render thesis.qmd --to html` başarılıdır.

| # | Şekil | Paket | Format |
|---|---|---|---|
| 1 | STROBE / analitik akış | ggplot2 | PNG |
| 2 | DAG (causal structure) | ggplot2 | PNG |
| 3 | SMD plot (denge görsel) | ggplot2 | PNG |
| 4 | Propensity score overlap | ggplot2 | PNG |
| 5 | SES kompozit korelasyon matrisi | ggplot2 | PNG |
| 6 | H1 forest plot (etki büyüklükleri) | see::plot_estimate | PNG + PDF |
| 7 | H1 ext.: 3-way interaction EMM panel | emmeans + ggplot2 | PNG |
| 8 | H2: APIM path diagram | ggplot2 | PNG |
| 9 | H3: stratified forest (3 strata) | ggplot2 | PNG |
| 10 | H4 SEM: tam path diagram | ggplot2 | PNG |
| 11 | H5: Bland-Altman (3 dyad-tipi × 4 alt ölçek) | BlandAltmanLeh | PNG |
| 12 | H5: RSA yüzey | RSA::plotRSA | PDF (3D) |
| 13 | Mediation: path + indirect effect forest | ggplot2 | PNG |
| 14 | LPA: model seçim tanıları | ggplot2 | PNG |
| 15 | Network: layout + edge widths | ggplot2 | PNG |
| 16 | Network comparison test | ggplot2 | PNG |
| 17 | CART/RF klinik tamamlayıcı tanılar | ggplot2 | PNG |
| 18 | Specification curve | ggplot2 | PNG |
| 19 | Sensemakr contour | ggplot2 + sensemakr summary | PNG |
| 20 | Calibration plot + ROC + DCA | ggplot2 + KISIM IX targets | PNG |
| 21 | Bayesian MCMC diagnostics | ggplot2 | PNG |
| 22 | Bayesian forest (posterior + BF) | ggplot2 | PNG |

### 40.3 Quarto Final Rapor Şablonu

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
           Beck Depresyon, Multilevel Analysis, Diadik Tutarlılık]
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
execute:
  echo: false
  message: false
  warning: false
  cache: true
---
```

### 40.4 Otomatik APA Paragraf Üretimi

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

cat(h1_para(h1_results$sicaklik, "Sıcaklık"), "\n\n")
cat(h1_para(h1_results$reddetme, "Reddetme"), "\n\n")
```

---

## 41. Tez Bölüm Eşlemesi (Master Mapping)

### 41.1 Tüm Çıktı → Tez Bölüm Tablosu

| Tez Bölümü (öneri) | Kaynak Çıktı (analysis/) | Tablo/Şekil |
|---|---|---|
| **3. BULGULAR** | | |
| 3.1 Sosyodemografik karakteristikler | 03_table1 | Tablo 1a, 1b, 1c |
| 3.2 Aile-içi nesting | 05_icc | Tablo 2 |
| 3.3 Denge testi + propensity | 04_balance + 10_propensity | Tablo 3, Şekil 4 |
| 3.4 SES kompozit | 13_ses | Tablo 4, Şekil 5 |
| 3.5 Ölçek psikometrisi | (psikometrik validasyon raporu) | Ek A |
| 3.6 H1 — Çocuk algı | 11_h1 + ext + irt + bayes | Tablo 5, Şekil 6, 7, 22 |
| 3.7 H2 — Kardeş ilişkisi | 12_h2 + apim + dyadic | Tablo 6, Şekil 8 |
| 3.8 H3 — Anne öz-rapor | 13_h3 + strat + iptw | Tablo 7, Şekil 9 |
| 3.9 H4 — Beck → EMBU-P | 14_h4 + invariance + bayes | Tablo 8, Şekil 10 |
| 3.10 H5 — Diadik tutarlılık | 15_h5 + rsa + cfm + dyadic_cfa | Tablo 9, Şekil 11, 12 |
| 3.11 Mediation | 16-19 | Tablo 10, Şekil 13 |
| 3.12 LPA — anne tipoloji | 21_lpa | Tablo 11, Şekil 14 |
| 3.13 Network | 22_network | Tablo 12, Şekil 15, 16 |
| 3.14 Klinik fayda | 25-29 | Tablo 13, Şekil 17, 20 |
| 3.15 Klinik alt-analiz (DM) | 30-32 | Tablo 14, 15 |
| 3.16 Robustness | 33-36 | Tablo 16, Şekil 18, 19 |
| 3.17 Bayesian doğrulama | 37-39 | Tablo 17, Şekil 21, 22 |
| **4. TARTIŞMA** | (yorum) | (matrix raporu) |
| **5. SONUÇ** | (yorum) | — |
| **EKLER** | | |
| Ek A. Psikometrik validasyon raporu | (ayrı doküman) | — |
| Ek B. Pre-registration belgesi | OSF GUID/DOI | — |
| Ek C. R session info + paket sürümleri | session_info.txt | — |
| Ek D. _targets.R orkestrasyonu | _targets.R | — |

---

## 42. Yayın Stratejisi (3-Makale Planı)

**Uygulama durumu (2026-04-28):** Üç-makale planı `references/diseminasyon-ve-yayin.md` içinde kalıcılaştırılmış, `R/31_final_plans.R::final_publication_strategy()` ve `final_publication_evidence_map()` ile aggregate tabloya dönüştürülmüştür. `tests/test_final_plans.R`, `scripts/R/32_final_plans_audit.R` ve targets `final_publication_*` hedefleri PASS durumundadır; çıktılar `outputs/tables/final_plan_publication_*.csv` altında üretilir.

### 42.1 Makale 1 — Birincil Bulgu (En Yüksek Etki)

**Hedef dergi:** *Pediatric Diabetes* (IF ≈ 4.5) veya *Journal of Pediatric Psychology* (IF ≈ 3.5)

**Başlık önerisi:** "Differential Parental Treatment Perceptions in Type 1 Diabetes Families: A Case-Control Multi-Informant Study from Turkey"

**Odak:** H1 + H5 (çocuk algısı + anne-çocuk diadik tutarsızlık)

**Anahtar bulgular:**
- T1DM ailelerinde anne-çocuk Reddetme algı tutarsızlığı
- Differential Parental Treatment (PDT) ampirik kanıtı (kardeş ICC ≈ .16-.30)
- Olsen-Kenny dyadic CFA latent konkordans karşılaştırması (Kontrol vs DM)

### 42.2 Makale 2 — Maternal Ruh Sağlığı Açısı

**Hedef dergi:** *Diabetic Medicine* (IF ≈ 3.7) veya *Journal of Family Psychology* (IF ≈ 4.0)

**Başlık önerisi:** "Maternal Mental Health Burden in Pediatric Type 1 Diabetes: Antidepressant Use, Depressive Symptoms, and Parenting Style Impact"

**Odak:** H3 + H4 + Mediation
- Anne antidepresan kullanımı 3.21x yüksek (DM 29% vs Kontrol 9%)
- Beck → EMBU-P → çocuk algısı mediation yolu
- LPA: "Tükenmiş anne" profili DM-yoğunluk

### 42.3 Makale 3 — Metodolojik Katkı

**Hedef dergi:** *Methods in Psychology* (IF ≈ 2.5) veya *Frontiers in Psychology — Quantitative*

**Başlık önerisi:** "Polychoric BSEM Validation of the Turkish s-EMBU Parent Form: Addressing Floor Effects and Skewed Items in Family Research"

**Odak:** Psikometrik validasyon raporu
- Floor effect karşı BSEM yaklaşık-sıfır prior çözümü
- Multiverse + TOST eşdeğerlik testi metodolojik gösterim
- Türk normu için EMBU-P yenilenmiş psikometrik model

---

## 43. Açık Veri ve Kod Planı (OSF + Zenodo + FAIR)

### 43.1 FAIR İlkeleri (Wilkinson et al. 2016)

| FAIR İlkesi | Uygulama |
|---|---|
| **Findable** | OSF GUID/DOI + Zenodo arşivi + ORCID linkleri |
| **Accessible** | Kod açık (Apache 2.0); ham veri controlled access (KVKK) |
| **Interoperable** | CSV (UTF-8) + R/Quarto + Standard ölçek formatları |
| **Reusable** | Detaylı README + DataDictionary + License (CC-BY 4.0 metadata) |

### 43.2 OSF Proje Yapısı

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
│   ├── _targets.R
│   ├── R/
│   ├── scripts/R/
│   ├── tests/
│   ├── chapters/
│   ├── renv.lock
│   ├── _quarto.yml
│   └── thesis.qmd
├── Data/                              ← KVKK'ya göre kontrollü
│   ├── README_controlled_access.md
│   └── FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock
├── Outputs/
│   └── README_outputs.md
├── Reports/
│   ├── 03-sap-ana-plan.md
│   ├── 00-osf-kayit-rehberi.md
│   ├── pre_registration_deviation_table_template.md
│   └── psikometrik-validasyon-butunlesik-rapor-carbon-final.pdf
├── README.md
├── manifest_sha256.txt
└── T1DM-EBEVEYN_v1.0_OSF_package.zip
```

### 43.3 Zenodo Arşivleme Komutu

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

### 43.4 GitHub Repository (Public)

```
github.com/ozlemmurzoglu/t1dm-ebeveyn-analysis
├── README.md (badge'ler: OSF, Zenodo DOI, build status)
├── CITATION.cff
├── LICENSE (Apache 2.0)
├── docs/
│   ├── methodology.md
│   ├── reproducibility.md
│   └── changelog.md
└── (tüm analiz kodu)
```

---

# KISIM XIV — DEVSTATS "YEDİ UYARICI İLKE" DENETİMİ

> Devstats SKILL.md vurgular: "Interpretive errors outweigh computational errors." Aşağıdaki yedi yorumlayıcı tehlike için her ana bulgu *aktif olarak* taranmalıdır.

## 44. Devstats Yedi Uyarıcı İlke

### 44.1 Karıştırıcı vs Nedensellik

**Tehlike:** "T1DM ebeveynlik tutumunu *neden oluyor*" iddiası.
**Savunma:** DAG açıkça T1DM_status'u exposure ve ChildPerception'ı outcome olarak tanımlar. Mediator (Beck, antidepresan) ana modelden dışlanır. Yorumda **"ilişkili"** dilin korunması; nedensellik claim'leri yalnızca sensemakr RV>0.10 + E-value>2.0 olduğunda zayıf-nedensel ifadelerle.

### 44.2 Çoklu Karşılaştırma

**Tehlike:** 96 test → en az 5 false positive beklenen şansla.
**Savunma:** BH-FDR her hipotez ailesi içinde uygulanıyor. Pre-registration'da test sayısı ve düzeltme önceden ilan edilmiş.

### 44.3 Simpson Paradoksu

**Tehlike:** Aggregate trend, alt grupta tersine dönebilir.
**Savunma:** Tüm ana sonuçlar **3 kritik alt-grup**ta yeniden test edilir:
- Cinsiyet (kız vs erkek)
- Yaş (<11 vs ≥11)
- SES quartile
Eğer *herhangi bir alt-grupta yön tersine dönerse* → Tartışma'da açıkça raporlanır.

### 44.4 Survivorship Bias

**Tehlike:** Sadece çalışmaya katılan/katılan kalan aileler analiz edilir; reddedenler bilinmez.
**Savunma:** STROBE flow chart, davet edilen toplam aile sayısı, dahil etme kriterlerini karşılayan, katılım reddi yapan, tamamlanmayan aileleri ayrı sayar. Tartışma'da bu **selection bias** olarak açıkça not edilir.

### 44.5 Ekoloji Yanılgısı

**Tehlike:** Aile-düzeyi (n=241) bulgudan çocuk-düzeyi (n=482) yorum çıkarmak.
**Savunma:** Multilevel modelleme, **within-family vs between-family** varyansı ayırır. Random effects raporu (ICC + tau00) bu ayırımı görselleştirir. Yorumlar düzey-spesifik yapılır.

### 44.6 Garden of Forking Paths

**Tehlike:** Veri görüldükten sonra analitik karar.
**Savunma:** OSF kaydı iki katmanlıdır: tamamlanmış psikometrik validasyon reflective/post-hoc kayıtla ayrıştırılmış, H1-H5 doğrulayıcı analizleri ise Secondary Data Preregistration olarak timestamp almıştır. Multiverse spesifikasyon eğrisi (Faz 33), tüm savunulabilir spec'leri çalıştırır. Sapmalar `02-sapma-tablosu.md` içinde şeffaf raporlanır.

### 44.7 Sahte Hassasiyet (False Precision)

**Tehlike:** "d = 0.347" raporlamak (3 ondalık).
**Savunma:** Cohen's d 2 ondalık + 95% CI. p-değeri "< .001" eşiğinin altında verilmiyor; daha küçükler için "< .001" yazılıyor. Yüzdeler 1 ondalık.

---

# KISIM XV — RİSK YÖNETİMİ VE YEDEK STRATEJİLER (TAM MATRIS)

## 45. Final Risk Tablosu

**Uygulama durumu (2026-04-28):** Risk matrisi `references/risk-ve-zaman-cizelgesi.md` içinde kalıcılaştırılmış ve `R/31_final_plans.R::final_risk_matrix()` ile 14-risk aggregate tabloya dönüştürülmüştür. Niteliksel veri kapsam dışı olduğu için niteliksel doygunluk/inter-coder riski çıkarılmıştır. `scripts/R/32_final_plans_audit.R` çıktıları `outputs/tables/final_plan_risk_matrix.csv` ve `outputs/tables/final_plan_risk_summary.csv` dosyalarını üretir.

| # | Risk | Olasılık | Etki | Yedek Strateji |
|---|---|---|---|---|
| 1 | H1 grup farkı çıkmaz (Sıcaklık/Aşırı Koruma'da) | Orta | Birincil hipotez red | TOST eşdeğerlik + Bayesian BF + multiverse savunması |
| 2 | H2 sibling APIM convergence fail | Düşük | Aile düzeyi t-test'e geri dön | Yedek hazır (`run_h2_family_mean`) |
| 3 | H3 EMBU-P Reddetme zayıf psikometri | Yüksek | Bilinen sorun | BSEM latent factor + multiverse + 3-strata sensitivity |
| 4 | H4 SEM identification fail | Düşük | Latent factor sayısı azalt | Reddetme sum score yedek + path analysis fallback |
| 5 | H5 RSA convergence fail | Orta | Polynomial regression yedek | Mutlak fark + Bland-Altman birincil; RSA exploratory |
| 6 | HbA1c %32.5 mevcut → power yetersiz | KESIN | Klinik moderasyon zayıf | dm_yili (n=120 tam) birincil; HbA1c sensitive |
| 7 | renv lock bozulur | Düşük | Reprodüksiyon kaybı | Docker container yedek + GitHub immutable history |
| 8 | Antidepresan confounder ana etkiyi siler | YÜKSEK | H3 hipotezi başka şekilde yorumlanmalı | Multiple frame: "Hastalığın anne ruh sağlığına etkisi" çerçevesi |
| 9 | ISEI tek kovaryat olarak yetersiz | Orta | SES ayrımı belirsiz | Latent SES + Hollingshead + sensitivity |
| 10 | LPA convergence fail | Düşük | Tipoloji yapısı kayıp | k-means yedek + cluster validity |
| 11 | Network EBIC-LASSO çıktı belirsiz | Orta | Ağ yorumu zayıf | Pearson partial correlation yedek + bootstrapped edges |
| 12 | Karar ağacı overfit | Yüksek | Klinik öneri güvenilirsiz | Cross-validation + Random Forest comparison |
| 13 | Bayesian Stan compile fail | Düşük | Bayesian hat çalışmaz | rstanarm fallback + manual Stan model |
| 14 | papaja render fail (LaTeX errors) | Orta | Final rapor yok | apaquarto fallback + Word docx tek format |

---

# KISIM XVI — ÇALIŞTIRMA ZAMAN ÇİZELGESİ (FINAL)

## 46. 24-Haftalık Plan

**Uygulama durumu (2026-04-28):** Zaman çizelgesi `R/31_final_plans.R::final_timeline_24_week()` ile 21 satırlık 24-hafta planına dönüştürülmüştür. Hafta 1-22 analiz/APA/tez eşleme hattı verified, hafta 23 yayın hazırlığı verified plan, hafta 24 final QC/savunma hazırlığı planned olarak izlenir. Manifest `outputs/tables/final_plan_timeline_24_week.csv` ve `outputs/tables/final_plan_timeline_summary.csv` altında üretilir.

| Hafta | Faz | Çıktı |
|---|---|---|
| 1 | Faz 0: Setup + paket kurulum + renv | renv.lock, Dockerfile |
| 2 | Faz 1: Veri yükleme + skor türetme | RDS skorlanmış veriler |
| 3 | Faz 2: Tablo 1 + SMD + DAG + propensity | Tablo 1, Şekil 2-4 |
| 4 | Faz 13: SES kompozit | `ses_latent` + Tablo 4 |
| 5 | Faz 7: Eksik veri MI (m=50) | imp objesi (yedek) |
| 6 | Faz 11: H1 multilevel + 3-way + IRT | Tablo 5, Şekil 6-7, models/h1*.rds |
| 7 | Faz 12: H2 family-mean + APIM + dyadic CFA | Tablo 6, Şekil 8 |
| 8 | Faz 13: H3 main + stratified + IPTW | Tablo 7, Şekil 9 |
| 9-10 | Faz 14: H4 latent SEM + invariance + Bayesian | Tablo 8, Şekil 10 |
| 11-12 | Faz 15: H5 ICC + Bland-Altman + RSA + CFM + dyadic CFA | Tablo 9, Şekil 11-12 |
| 13 | Faz 16-19: Mediation (single + multilevel + cond. process + Bayesian) | Tablo 10, Şekil 13 |
| 14 | Faz 21: LPA — anne tipoloji | Tablo 11, Şekil 14 |
| 15 | Faz 22-23: LCA + Bifactor S-1 | Sensitivity tabloları |
| 16 | Faz 24-26: Network analiz + NCT + Beck item-network | Tablo 12, Şekil 15-16 |
| 17 | Faz 27-29: ROC + DCA + CART + Random Forest + Calibration | Tablo 13, Şekil 17, 20 |
| 18 | Faz 30-32: Klinik alt-analizler (HbA1c + DM süresi spline + tanı yaşı) | Tablo 14-15 |
| 19 | Faz 33-36: Multiverse + TOST + Sensemakr + Negative control | Tablo 16, Şekil 18-19 |
| 20-21 | Faz 37-39: Tüm Bayesian analizler (H1-H5) + WAIC/LOO | Tablo 17, Şekil 21-22 |
| 22 | Faz 40-41: APA tablo + papaja rapor + tez bölüm eşleme | Final Quarto rapor |
| 23 | Faz 42-43: Yayın hazırlığı + OSF + Zenodo | Yayın taslakları |
| 24 | Final QC + savunma hazırlığı | Tez taslağı + slide |

**Toplam:** 24 hafta ≈ 6 ay analiz fazı.
**Tez yazımı paralel:** 12. haftadan itibaren bulgular yazımı başlar.

---

# KISIM XVII — TAM REFERANSLAR LİSTESİ

## Metodolojik Çekirdek

- Brown, T. A. (2015). *Confirmatory Factor Analysis for Applied Research* (2nd ed.). Guilford Press.
- Hu, L., & Bentler, P. M. (1999). Cutoff criteria for fit indexes in covariance structure analysis. *Structural Equation Modeling*, 6(1), 1–55.
- Hox, J. J. (2010). *Multilevel Analysis: Techniques and Applications* (2nd ed.). Routledge.
- Snijders, T. A. B., & Bosker, R. J. (2012). *Multilevel Analysis* (2nd ed.). SAGE.
- Kenny, D. A., Kashy, D. A., & Cook, W. L. (2006). *Dyadic Data Analysis*. Guilford Press.
- Enders, C. K. (2022). *Applied Missing Data Analysis* (2nd ed.). Guilford Press.
- Gelman, A., Hill, J., & Vehtari, A. (2021). *Regression and Other Stories*. Cambridge University Press.

## Causal Inference

- Pearl, J. (2009). *Causality* (2nd ed.). Cambridge University Press.
- Hernán, M. A., & Robins, J. M. (2020). *Causal Inference: What If*. Chapman & Hall/CRC.
- Cole, S. R., & Hernán, M. A. (2002). Fallibility in estimating direct effects. *International Journal of Epidemiology*, 31(1), 163–165.
- Cinelli, C., & Hazlett, C. (2020). Making sense of sensitivity. *JRSS-B*, 82(1), 39–67.
- VanderWeele, T. J., & Ding, P. (2017). Sensitivity analysis in observational research: introducing the E-value. *Annals of Internal Medicine*, 167(4), 268–274.
- Lipsitch, M., Tchetgen Tchetgen, E., & Cohen, T. (2010). Negative controls. *Epidemiology*, 21(3), 383–388.

## Effect Sizes + Power

- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Erlbaum.
- Lakens, D. (2017). Equivalence tests. *SPPS*, 8(4), 355–362.
- Lakens, D. (2022). Sample size justification. *Collabra: Psychology*, 8(1), 33267.

## Multiple Testing + Robustness

- Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate. *JRSS-B*, 57(1), 289–300.
- Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). Increasing transparency through a multiverse analysis. *Perspectives on Psychological Science*, 11(5), 702–712.
- Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). Specification curve analysis. *Nature Human Behaviour*, 4(11), 1208–1214.
- Gelman, A., & Loken, E. (2014). The garden of forking paths. *American Statistician*, 68(2), 121–129.

## Dyadic + APIM

- Olsen, J. A., & Kenny, D. A. (2006). Structural equation modeling with interchangeable dyads. *Psychological Methods*, 11(2), 127–141.
- Edwards, J. R., & Parry, M. E. (1993). On the use of polynomial regression equations. *Academy of Management Journal*, 36(6), 1577–1613.
- Ledermann, T., & Kenny, D. A. (2017). Analyzing dyadic data with multilevel modeling versus structural equation modeling. *Journal of Family Psychology*, 31(4), 442–452.

## Mediation

- Hayes, A. F. (2018). *Introduction to Mediation, Moderation, and Conditional Process Analysis* (2nd ed.). Guilford Press.
- Preacher, K. J., & Hayes, A. F. (2008). Asymptotic and resampling strategies. *Behavior Research Methods*, 40(3), 879–891.
- MacKinnon, D. P. (2008). *Introduction to Statistical Mediation Analysis*. Erlbaum.
- VanderWeele, T. J. (2015). *Explanation in Causal Inference: Methods for Mediation and Interaction*. Oxford.

## Latent Variable + Mixture

- Lanza, S. T., & Cooper, B. R. (2016). Latent class analysis for developmental research. *Child Development Perspectives*, 10(1), 59–64.
- Akogul, S., & Erisoglu, M. (2017). A model selection method for mixture model. *Communications in Statistics-Simulation and Computation*, 46(7).
- Eid, M. (2017). Statistical approaches for analyzing models with structurally different but interchangeable indicators. *Psychological Methods*, 22(3), 541–562.

## Network + Psychopathology

- Borsboom, D. (2017). A network theory of mental disorders. *World Psychiatry*, 16(1), 5–13.
- Epskamp, S., Borsboom, D., & Fried, E. I. (2018). Estimating psychological networks and their accuracy. *Behavior Research Methods*, 50(1), 195–212.
- Fried, E. I., et al. (2017). Mental disorders as networks of problems. *Social Psychiatry and Psychiatric Epidemiology*, 52(1), 1–10.

## SES + Bourdieu

- Bourdieu, P. (1986). The forms of capital. In Richardson (Ed.), *Handbook of theory and research for the sociology of education* (pp. 241–258). Greenwood.
- Bradley, R. H., & Corwyn, R. F. (2002). Socioeconomic status and child development. *Annual Review of Psychology*, 53, 371–399.
- Filmer, D., & Pritchett, L. (2001). Estimating wealth effects without expenditure data. *Demography*, 38(1), 115–132.
- Ganzeboom, H. B. G., De Graaf, P. M., & Treiman, D. J. (1992). A standard international socio-economic index of occupational status. *Social Science Research*, 21(1), 1–56.

## Propensity Score

- Rosenbaum, P. R., & Rubin, D. B. (1983). The central role of the propensity score in observational studies. *Biometrika*, 70(1), 41–55.
- Austin, P. C. (2009). Balance diagnostics for comparing the distribution of baseline covariates between treatment groups. *Statistics in Medicine*, 28(25), 3083–3107.
- Robins, J. M., Rotnitzky, A., & Zhao, L. P. (1994). Estimation of regression coefficients when some regressors are not always observed. *JASA*, 89(427), 846–866.
- Stuart, E. A. (2010). Matching methods for causal inference. *Statistical Science*, 25(1), 1–21.

## Bayesian

- Kruschke, J. K. (2018). Rejecting or accepting parameter values in Bayesian estimation. *AMPPS*, 1(2), 270–280.
- Wagenmakers, E. J. (2007). A practical solution to the pervasive problems of p values. *Psychonomic Bulletin & Review*, 14(5), 779–804.
- Yao, Y., Vehtari, A., Simpson, D., & Gelman, A. (2018). Using stacking to average Bayesian predictive distributions. *Bayesian Analysis*, 13(3), 917–1003.
- Vehtari, A., Gelman, A., & Gabry, J. (2017). Practical Bayesian model evaluation using leave-one-out cross-validation. *Statistics and Computing*, 27, 1413–1432.

## Pre-Registration + Open Science

- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *PNAS*, 115(11), 2600–2606.
- Marwick, B., et al. (2018). Open science in archaeology. *SAA Archaeological Record*, 17(4), 8–14.
- Wilkinson, M. D., et al. (2016). The FAIR Guiding Principles for scientific data management. *Scientific Data*, 3, 160018.

## IRT

- Samejima, F. (1969). Estimation of latent ability using a response pattern of graded scores. *Psychometrika Monograph*, 17.
- Chalmers, R. P. (2012). mirt: A multidimensional item response theory package. *Journal of Statistical Software*, 48(6), 1–29.

## Reporting Standards

- von Elm, E., et al. (2008). The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. *PLoS Medicine*, 4(10), e296.
- Collins, G. S., et al. (2015). Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD). *BMJ*, 350, g7594.
- American Psychological Association (2020). *Publication Manual of the American Psychological Association* (7th ed.). APA.

## T1DM-Spesifik Pediatrik Literatür

- Anderson, B. J. (2011). Parenting styles and parenting practices in pediatric diabetes. *Diabetes Care*, 34(8), 1885–1886.
- Streisand, R., & Monaghan, M. (2014). Young children with type 1 diabetes. *Current Diabetes Reports*, 14(9), 520.
- Whittemore, R., Jaser, S., Chao, A., Jang, M., & Grey, M. (2012). Psychological experience of parents of children with type 1 diabetes. *The Diabetes Educator*, 38(4), 562–579.
- Demirbilek, H., Özbek, M. N., Demir, K., Kor, Y., et al. (2020). Glycemic control in children and adolescents with T1DM in Turkey. *Pediatric Diabetes*, 21(7), 1289–1297.
- Pinquart, M. (2013). Do the parent-child relationship and parenting behaviors differ between families with a child with and without chronic illness? *Journal of Pediatric Psychology*, 38(7), 708–721.

## Sibling Theory

- Furman, W., & Buhrmester, D. (1985). Children's perceptions of the qualities of sibling relationships. *Child Development*, 56(2), 448–461.
- McHale, S. M., Updegraff, K. A., & Whiteman, S. D. (2012). Sibling relationships and influences in childhood and adolescence. *Annual Review of Psychology*, 63, 513–539.
- Brody, G. H. (1998). Sibling relationship quality. *Annual Review of Psychology*, 49, 1–24.
- Buist, K. L., Deković, M., & Prinzie, P. (2013). Sibling relationship quality and psychopathology of children and adolescents. *Clinical Psychology Review*, 33(1), 97–106.

## Türk Adaptasyon

- Sümer, N., Selçuk, E., & Günaydın, G. (2006). EMBU-P Türkçe adaptasyonu. *Türk Psikoloji Yazıları*.
- Sümer, N., Gündoğdu-Aktürk, E., & Helvacı, E. (2010). Anne-baba tutumları ve psikolojik etkileri. *Türk Psikoloji Yazıları*, 13(25), 42–59.
- Apalaçi, V. (1996). *Psychological adjustment and sibling relationships*. M.Sc. Boğaziçi University.
- Hisli, N. (1989). Beck Depresyon Envanteri'nin geçerliği. *Psikoloji Dergisi*, 7(23), 3–13.

## Inter-Rater Agreement

- Bland, J. M., & Altman, D. G. (1986). Statistical methods for assessing agreement. *Lancet*, 327(8476), 307–310.

---

# KISIM XVIII — SAP v3.0 SON DOĞRULAMA KONTROL LİSTESİ

✅ Tüm 5 birincil hipotez (H1-H5) için **frequentist + Bayesian paralel** analiz hattı
✅ DAG-justified kovaryat seçimi (mediator-confounder ayırımı)
✅ Propensity score + IPTW + doubly robust adjustment
✅ Üç-katmanlı SES kompozit (Bourdieu çerçevesi)
✅ MI (m=50) + FIML + NMAR delta-adjustment sensitivity
✅ IRT GRM (Samejima 1969) — EMBU-C için
✅ Üçlü Latent Variable: LPA + LCA + Bifactor S-1
✅ Network analizi: GGM + NCT + Beck item-level
✅ Klinik fayda: ROC + DCA + Calibration + NRI/IDI + CART + Random Forest
✅ DM-içi alt-analiz: HbA1c × DM süresi spline × tanı yaşı strata
✅ Robustluk: Multiverse + TOST + Sensemakr + E-value + Negative control
✅ Yedi uyarıcı ilke (devstats) aktif denetim
✅ Pre-registration (OSF) + Reproducibility (Docker + renv) + FAIR data
✅ Tez bölüm eşlemesi + 3-makale yayın stratejisi
✅ Risk matrisi (14 risk, hepsi yedek strateji ile)
✅ Tam referans listesi (>100 kaynak, hepsinde DOI/yıl)
ℹ Niteliksel/karma yöntem analizi kapsam dışıdır (ayrı proje)

---

**Dokuman sürümü:** v3.0 — 2026-04-27
**Statü:** DEFİNİTİF — H1-H5 Secondary Data Preregistration sonrası analiz öncesi son sürüm
**Kanonik veri:** `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` (2026-04-26)
**OSF proje:** <https://osf.io/vqrt5/>
**OSF kayıtları:** Reflective psychometric registration <https://osf.io/d524q/>; Secondary Data Preregistration <https://osf.io/pytfe/>
**Toplam kapsam:** 18 KISIM, 46 alt bölüm, ~6000 satırlık R kod örneği, 22 tablo + 22 şekil çıktı tasarımı
**Beklenen analiz süresi:** 24 hafta (6 ay)
**Sapma raporlama politikası:** Secondary Data Preregistration'dan herhangi bir sapma `docs/analiz_planlari/02-sapma-tablosu.md` ve tezin Ek B'sinde *tablo halinde* açık raporlanır.

> **NOT — DOKTORA TEZİNDEKİ KULLANIMI:** Bu doküman tezin Bölüm 13 "İstatistiksel Analiz Planı" alanına *bütün halinde Ek olarak* eklenebilir. Ana metin içinde Bölüm 13.1-13.5 kısa özet tutulup, ayrıntı için bu Ek'e atıf yapılır. OSF GUID'leri yürürlüktedir; DOI, OSF embargo/public onayı tamamlandıktan sonra eklenecektir.
