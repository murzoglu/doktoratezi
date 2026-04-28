# Pipeline Mimarisi — `_targets.R` ve Modül Haritası

**Ne zaman oku:** Bir analiz hedefi ekleneceği/değiştirileceği zaman, `tar_make()` hatası
geldiğinde, yeni bir runner yazmadan önce, kanonik kilit doğrulaması için,
`_targets/meta` hash tutarlılığı sorulduğunda.

---

## Üç Katmanlı Mimari

```
data/processed/FINAL_REFERENCE__*.csv
              │
              ▼
       R/01_io.R::validate_and_load()
              │
              ▼
            df_family_raw / df_long_raw
              │   prepare_family() / prepare_long()
              ▼
            df_family / df_long  (faktörler, key columns hazır)
              │   R/10_derived_scores.R
              ▼
            df_family_scored / df_long_scored
              │   R/11_ses_composites.R
              ▼
            df_family_ses
              │   R/12_missing_data_frames.R
              ▼
            df_family_missing_{fiml_primary, complete_case_primary, mi_primary, mi_clinical_sensitivity}
              │   R/13_table1_smd.R
              ▼
            table1_results
              │   R/14_causal_dag.R + R/15_propensity_score.R
              ▼
            df_family_propensity
              │   R/16..19_h{1,2,3,4}_*.R
              ▼
            h1_*, h2_*, h3_*, h4_* sonuç tabloları → outputs/tables/
```

**Üç katman, üç sorumluluk:**

| Katman | Yer | Rol | Yan etki | Test |
|--------|-----|-----|----------|------|
| **Kütüphane** | `R/*.R` | Saf fonksiyonlar | Yok — yalnız hesap | `tests/test_*.R` (`stopifnot`) |
| **Runner** | `scripts/R/*.R` | `R/` fonksiyonlarını çağır + `outputs/` ve `data/processed/` yaz | Dosya I/O | Manuel + audit runner |
| **Orkestrator** | `_targets.R` | Hedef grafiği (DAG), hash kontrol, paralel | Dosya hash takibi | `tar_visnetwork()` |

**Bu sınırı asla bulanıklaştırma.** `R/` içindeki bir fonksiyon `write_csv()` çağırırsa
mimari kırılır.

---

## `R/` Modül Haritası

| Dosya | Sorumluluk | Anahtar fonksiyonlar |
|-------|-----------|----------------------|
| `R/00_paths.R` | Proje yol kökleri | `thesis_paths()` |
| `R/01_io.R` | Kanonik veri yükleme + SHA-256 doğrulama | `canonical_final_reference_paths()`, `read_final_reference_lock()`, `match_final_reference_record()`, `final_reference_validation_manifest()`, `validate_and_load()`, `prepare_family()`, `prepare_long()`, `summarize_loaded_final_reference()` |
| `R/02_embu_stage1.R` (arşiv pipeline) | EMBU Stage 1 standardizasyonu (legacy; kanonik öncesi) | — |
| `R/03_embu_stage2_likert4.R` (arşiv) | EMBU 4'lü Likert standardizasyonu (legacy) | — |
| `R/04_embu_stage3_family.R` (arşiv) | EMBU aile eşleştirme (legacy; kanonik baz oluştuktan sonra dondurulmuş) | — |
| `R/05_demographic_text_standardization.R` | Demografik tekst standartlaştırma | `clean_column_names()`, `as_numeric_response()` |
| `R/06_psychometric_validation.R` | EMBU/Beck/KİA item-, alt ölçek-, CFA-, ω- bazlı validasyon | `psychval_embu_subscale_map()`, `psychval_srq_subscale_map()`, `psychval_item_descriptives()`, `psychval_score_subscales()`, `psychval_score_srq_subscales()`, `psychval_safe_alpha()`, `psychval_safe_omega()`, `psychval_reliability_table()`, `psychval_lavaan_model()`, `psychval_safe_cfa()`, `psychval_fit_indices()`, `psychval_standardized_loadings()`, `psychval_beck_total()`, `psychval_srq_total_mean()`, `psychval_icc_rows()` |
| `R/07_reproducibility.R` | Kilit dosyası ayrıştırma + hash hesabı | `parse_final_reference_lock()`, `sha256_file()` |
| `R/08_data_governance.R` | Etik/veri yönetimi denetimi | `audit_data_governance()` |
| `R/09_reporting_standards.R` | JARS-Mixed/STROBE checklist denetimi | `audit_reporting_standards()` |
| `R/10_derived_scores.R` | Türetilmiş skorlar (alt ölçek toplam/ortalama, %50 madde eşiği, Beck NA) | `derived_score_dictionary()`, `derive_family_scores()`, `derive_long_scores()`, `score_range_audit()`, `assert_no_score_range_violations()` |
| `R/11_ses_composites.R` | Üç katmanlı SES kompoziti (polychoric PCA + CFA latent) | `derive_ses_composites()`, `ses_component_summary()`, `ses_correlation_table()` |
| `R/12_missing_data_frames.R` | mice/MI + FIML + NMAR delta | `derive_missing_data_frames()`, `run_missing_imputation_set()`, `summarize_missing_mice()` |
| `R/13_table1_smd.R` | Tablo 1 + SMD denge | `build_table1_family()` |
| `R/14_causal_dag.R` | dagitty Causal DAG + minimal adjustment set | `causal_dag_nodes()`, `causal_dag_edges()`, `causal_dag_string()`, `make_causal_dag()`, `causal_dag_adjustment_sets()` (exposure = `T1DM_status`), `causal_dag_conditional_independencies()`, `causal_dag_covariate_strategy()`, `causal_dag_variable_mapping()`, `causal_dag_proxy_requirements()`, `validate_causal_dag_data_proxies()`, `plot_causal_dag()`, `build_causal_dag()`, `summarize_causal_dag_targets()` |
| `R/15_propensity_score.R` | Logit PS + IPTW (99. persentil trim) + 1:1 matching + doubly robust plan | `derive_propensity_score_pipeline()` |
| `R/16_h1_child_perception.R` | H1 multilevel (role × yaş × cinsiyet) + IRT + Bayesian preflight | `run_h1_child_perception_pipeline()` |
| `R/17_h2_sibling_relationships.R` | H2 aile-mean Welch + APIM + Olsen-Kenny CFA | `run_h2_sibling_relationships_pipeline()` |
| `R/18_h3_parent_self_report.R` | H3 ANCOVA + IPTW + AD-stratifiye duyarlılık | `run_h3_parent_self_report_pipeline()` |
| `R/19_h4_beck_parenting_sem.R` | H4 WLSMV ordinal SEM + multigroup (configural→metric) + blavaan plan | `run_h4_beck_parenting_sem_pipeline()` |

**Not:** `R/02-04` arşiv pipeline'ıdır. Kanonik baz kilitlendikten sonra (2026-04-26) bu
modüller yalnızca tarihsel doğrulama amacıyla kullanılır; aktif analizde dokunulmaz.

---

## `scripts/R/` Runner Haritası

Her runner ya **veri üretici** ya da **denetim (audit)** rolü oynar:

| Runner | Tip | Çağırdığı R/ |
|--------|-----|--------------|
| `00_preprocessing.R` | Üretici (legacy, arşiv) | — |
| `01_embu_stage1_standardize.R` | Üretici (arşiv) | `R/02_embu_stage1.R` |
| `02_embu_stage2_likert4.R` | Üretici (arşiv) | `R/03_embu_stage2_likert4.R` |
| `03_embu_stage3_family.R` | Üretici (arşiv) | `R/04_embu_stage3_family.R` |
| `04_demographic_text_standardize_final.R` | Üretici | `R/05_demographic_text_standardization.R` |
| `05_psychometric_validation.R` | Üretici | `R/06_psychometric_validation.R` |
| `06_psychometric_bsem.R` | Üretici (Bayesian SEM preflight) | `R/06_psychometric_validation.R` + `blavaan` |
| `07_verify_reproducibility.R` | Audit | `R/07_reproducibility.R` |
| `08_ethics_data_governance_audit.R` | Audit | `R/08_data_governance.R` |
| `09_reporting_standards_audit.R` | Audit | `R/09_reporting_standards.R` |
| `10_hash_validate_load.R` | Audit | `R/01_io.R::validate_and_load()` |
| `11_derive_scores_audit.R` | Audit | `R/10_derived_scores.R` |
| `12_derive_ses_audit.R` | Audit | `R/11_ses_composites.R` |
| `13_missing_data_audit.R` | Audit | `R/12_missing_data_frames.R` |
| `14_table1_smd_audit.R` | Audit | `R/13_table1_smd.R` |
| `15_causal_dag_audit.R` | Audit | `R/14_causal_dag.R` |
| `16_propensity_score_audit.R` | Audit | `R/15_propensity_score.R` |
| `17_h1_child_perception_audit.R` | Audit | `R/16_h1_child_perception.R` |
| `18_h2_sibling_relationships_audit.R` | Audit | `R/17_h2_sibling_relationships.R` |
| `19_h3_parent_self_report_audit.R` | Audit | `R/18_h3_parent_self_report.R` |
| `20_h4_beck_parenting_sem_audit.R` | Audit | `R/19_h4_beck_parenting_sem.R` |

---

## Kanonik Kilit Doğrulama Zinciri

```r
# Sıralı ve kırılamaz
1. parse_final_reference_lock(readLines("data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock"))
   → lock objesi (status: LOCKED_CANONICAL_ANALYSIS_BASE)

2. read_final_reference_lock(lock_path)
   → status doğrulaması (status != LOCKED_CANONICAL_ANALYSIS_BASE → STOP)

3. match_final_reference_record(lock, csv_path)
   → CSV path'inin lock'ta kayıtlı olup olmadığı (1 tek kayıt değilse → STOP)

4. sha256_file(csv_path)
   vs
   lock'taki sha256 hash → eşleşmezse STOP

5. final_reference_file_facts(csv_path)
   → satır/sütun sayısı + hash + N_unique key → manifest

6. final_reference_validation_manifest(lock_file, c(family_csv, long_csv))
   → tüm dosyalar için manifest → targets DAG için imza
```

**Bu zincirin herhangi bir adımı kırılırsa `validate_and_load()` `stop()` ile çağrı ağacını
keser. Bypass etme.**

`_targets.R` üzerinde:

```r
tar_target(lock_file, final_reference_paths$lock, format = "file"),
tar_target(family_csv, final_reference_paths$family, format = "file"),
tar_target(long_csv, final_reference_paths$long, format = "file"),
```

`format = "file"` → targets bu dosyaların hash'ini izler. Hash değişirse downstream
hedeflerin tümü invalidate olur.

---

## KISIM II–V Hedef Grupları (`_targets.R` blokları)

### KISIM II — Yükleme + Türetilmiş Skorlar
```
project_paths → raw_data_manifest → final_reference_paths → lock_file/family_csv/long_csv
→ final_reference_manifest → df_family_raw/df_long_raw → df_family/df_long
→ derived_score_dictionary_table → derived_score_range_audit → derived_score_range_ok
→ df_family_scored / df_long_scored → derived_score_target_summary
```
Anahtar prensip: `derived_score_range_ok` `TRUE` döndürmezse downstream çalıştırılmaz
(targets `cue` ile bu zincir kırılırsa hata alırsın).

### KISIM III — SES + Eksik Veri + Tablo 1
```
ses_results → df_family_ses → ses_diagnostics_table → ses_target_summary
→ missing_results → df_family_missing_{fiml_primary, complete_case_primary, mi_primary, mi_clinical_sensitivity}
→ missing_imputations → missing_mi_diagnostics_table
→ table1_results → table1_smd_balance_table → table1_balance_action_table
```

### KISIM IV — Causal DAG + Propensity Score
```
causal_dag_results → causal_dag_{nodes,edges,adjustment_sets,conditional_independencies,covariate_strategy,variable_mapping}_table
→ causal_dag_proxy_validation_table
→ propensity_results → df_family_propensity
→ propensity_{model_summary, weight_summary, balance_before_after, matching_summary, overlap_summary, doubly_robust_plan}_table
```

### KISIM V — Hipotez Testleri H1–H4
```
h1_child_perception_results → h1_{analysis_frame_summary, scaling_summary, outcome_descriptives,
  primary_fixed_effects, primary_anova, primary_role_pairwise, primary_diagnostics,
  three_way_tests, three_way_emmeans_grid, three_way_diagnostics,
  irt_status, irt_item_parameters, irt_theta_fixed_effects, irt_theta_anova, irt_theta_diagnostics,
  bayesian_plan}_table
→ h2_sibling_relationships_results → h2_{scaling, long_descriptives, family_mean_descriptives,
  family_mean_welch_tests, apim_fixed_effects, apim_diagnostics,
  age_gap_moderation_{fixed_effects, anova, diagnostics},
  olsen_kenny_{status, fit_measures, latent_correlations, parameter_estimates}}_table
→ h3_parent_self_report_results → h3_{scaling, outcome_descriptives, antidepressant_counts,
  primary_{fixed_effects, group_effects, diagnostics},
  antidepressant_stratified_group_effects,
  iptw_{fixed_effects, group_effects, diagnostics}}_table
→ h4_beck_parenting_sem_results → h4_{scaling, ordered_item_diagnostics,
  latent_sem_{status, fit_measures, structural_paths},
  multigroup_{status, fit_measures, comparison, structural_paths, sparse_collapse_map},
  bayesian_sem_plan}_table
```

---

## Yeni Hedef Eklerken Yapılacaklar

1. **`R/` katmanına saf fonksiyonu ekle** — eğer yeni bir hesap hattı ise.
2. **`tests/test_*.R`** dosyasına `stopifnot()` ile assertion yaz.
3. **`scripts/R/`** runner'ını ekle (sadece eğer `targets` dışında manuel çalıştırma
   gerekiyorsa).
4. **`_targets.R`** içine `tar_target(name, expr)` ekle. Bağımlılığı doğru bildir
   (girdi target'ları fonksiyon argümanı olarak verilmelidir, böylece DAG izlenir).
5. `tar_visnetwork()` ile DAG'ı görselleştirip döngü olmadığını doğrula.
6. `tar_make()` ile çalıştır; `tar_meta()` çıktısında yeni target'ın `seconds`,
   `bytes`, `error` sütunlarını incele.
7. Audit runner ekle (`scripts/R/##_*_audit.R`) — JARS-Mixed checklist'in bir maddesi
   ise `R/09_reporting_standards.R` audit'ine de bağla.

---

## Sık Yapılan Hatalar (Pipeline-Düzeyi)

1. **`R/` içinde `write_csv()`** — mimari ihlali, runner'a taşı.
2. **`tar_target` yerine `targets::tar_target`** — `library(targets)` zaten yüklü; namespace
   gereksiz.
3. **Path'i hardcode** — her zaman `thesis_paths()` veya `final_reference_paths` üzerinden
   referans ver.
4. **Kanonik CSV'yi runner içinden yaz** — KESİNLİKLE YASAK. Kanonik baz dondurulmuştur.
5. **Hash bypass** — `tryCatch()` ile `validate_and_load()` hatasını yutma. Kilitlilik
   ihlal edilmiş demektir.
6. **`_targets/meta/meta` git'le** — `.gitignore`'da `_targets/` var; bu durum bile
   reproducibility açısından sıkıntılı, hash değişirse herkes yeniden hesaplar.

---

## Runbook'lar (Modül-Bazında Detay)

`docs/analiz_planlari/` altında her ana KISIM/hipotez için runbook vardır:

- `DATA-LOADING-RUNBOOK.md` — kanonik yükleme adımları
- `DERIVED-SCORES-RUNBOOK.md` — alt ölçek hesaplama kuralları
- `SES-COMPOSITES-RUNBOOK.md` — üç katmanlı SES protokolü
- `MISSING-DATA-FRAMES-RUNBOOK.md` — FIML/MI/sensitivity çerçeveleri
- `TABLE1-SMD-RUNBOOK.md` — Tablo 1 oluşturma
- `CAUSAL-DAG-RUNBOOK.md` — DAG karar matrisi
- `PROPENSITY-SCORE-RUNBOOK.md` — IPTW/matching adımları
- `H1-CHILD-PERCEPTION-RUNBOOK.md`
- `H2-SIBLING-RELATIONSHIPS-RUNBOOK.md`
- `H3-PARENT-SELF-REPORT-RUNBOOK.md`
- `H4-BECK-PARENTING-SEM-RUNBOOK.md`
- `REPRODUCIBILITY-RUNBOOK.md`

**Pipeline değişikliği yaparken ilgili runbook'u eş zamanlı güncelle**; yoksa belge–kod
arasında drift oluşur.
