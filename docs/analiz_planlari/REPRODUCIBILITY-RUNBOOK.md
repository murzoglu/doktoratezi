# Reprodüktiblik Runbook

**Kapsam:** `renv`, Docker, `_targets.R`, Quarto ve kanonik veri kilidi.
**Kanonik veri:** `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` (2026-04-26)
**OSF proje:** <https://osf.io/vqrt5/>

## Yerel Doğrulama

```bash
Rscript -e 'renv::status()'
Rscript tests/test_reproducibility_lock.R
Rscript scripts/R/07_verify_reproducibility.R
Rscript tests/test_final_reference_loading.R
Rscript scripts/R/10_hash_validate_load.R
Rscript tests/test_derived_scores.R
Rscript scripts/R/11_derive_scores_audit.R
Rscript tests/test_ses_composites.R
Rscript scripts/R/12_derive_ses_audit.R
Rscript tests/test_missing_data_frames.R
Rscript scripts/R/13_missing_data_audit.R
Rscript tests/test_table1_smd.R
Rscript scripts/R/14_table1_smd_audit.R
Rscript tests/test_causal_dag.R
Rscript scripts/R/15_causal_dag_audit.R
Rscript tests/test_propensity_score.R
Rscript scripts/R/16_propensity_score_audit.R
Rscript tests/test_h1_child_perception.R
Rscript scripts/R/17_h1_child_perception_audit.R
Rscript tests/test_h2_sibling_relationships.R
Rscript scripts/R/18_h2_sibling_relationships_audit.R
Rscript tests/test_h3_parent_self_report.R
Rscript scripts/R/19_h3_parent_self_report_audit.R
Rscript tests/test_h4_beck_parenting_sem.R
Rscript scripts/R/20_h4_beck_parenting_sem_audit.R
Rscript tests/test_h5_dyadic_concordance.R
Rscript scripts/R/21_h5_dyadic_concordance_audit.R
Rscript tests/test_robustness_sensitivity.R
Rscript tests/test_bayesian_parallel.R
Rscript tests/test_mediation.R
Rscript tests/test_latent_profile.R
Rscript tests/test_clinical_utility.R
Rscript tests/test_network_analysis.R
Rscript tests/test_dm_subanalyses.R
Rscript tests/test_apa_figures.R
Rscript scripts/R/29_apa_figures_audit.R
Rscript tests/test_apa_tables.R
Rscript scripts/R/30_apa_tables_audit.R
Rscript tests/test_thesis_mapping.R
Rscript scripts/R/31_thesis_mapping_audit.R
Rscript tests/test_final_plans.R
Rscript scripts/R/32_final_plans_audit.R
Rscript tests/test_data_governance.R
Rscript scripts/R/08_ethics_data_governance_audit.R
Rscript tests/test_reporting_standards.R
Rscript scripts/R/09_reporting_standards_audit.R
Rscript -e 'targets::tar_make()'
quarto render thesis.qmd --to html
```

`scripts/R/07_verify_reproducibility.R`, kanonik lock dosyasında tanımlı CSV dosyalarının satır sayısı, sütun sayısı ve SHA-256 hash değerlerini doğrular. Satır-düzeyi veri çıktısı üretmez.

`scripts/R/10_hash_validate_load.R`, hash doğrulaması geçmeden `family` ve `long` CSV'lerini yüklemez. Hazırlık katmanı yalnız faktör ve temel yapısal değişkenleri ekler; satır-düzeyi veri çıktısı üretmez.

`scripts/R/11_derive_scores_audit.R`, EMBU, BDI ve KIA/SRQ türetilmiş skor sözlüğünü, item range audit'ini ve aggregate skor kapsamını üretir. Satır-düzeyi skorlanmış veri dosyası yazmaz.

`scripts/R/12_derive_ses_audit.R`, üç katmanlı SES kompozit hattını çalıştırır; materyal indeks diagnostic'leri, CFA fit ölçüleri ve aggregate SES kapsam tabloları üretir. Satır-düzeyi SES dosyası yazmaz.

`scripts/R/13_missing_data_audit.R`, FIML/MI/NMAR eksik veri çerçevelerini denetler; `mice` diagnostic'leri, MCAR taraması, frame manifest'i ve aggregate eksiklik tabloları üretir. Satır-düzeyi frame veya imputed veri dosyası yazmaz.

`scripts/R/14_table1_smd_audit.R`, aile-düzeyi Tablo 1 özetini ve DM-Kontrol SMD denge diagnostic'lerini üretir. Satır-düzeyi veri dosyası yazmaz.

`scripts/R/15_causal_dag_audit.R`, DAG node/edge tablolarını, `dagitty` adjustment setlerini, kovaryat stratejisini, proxy kolon doğrulamasını ve DAG figürünü üretir. Satır-düzeyi veri dosyası yazmaz.

`scripts/R/16_propensity_score_audit.R`, DAG v1 primary adjustment setiyle propensity score, stabilized IPTW, matching, common support ve doubly robust model planı çıktıları üretir. Satır-düzeyi PS/weight verisi yazmaz.

`scripts/R/17_h1_child_perception_audit.R`, H1 çocuk algısı için mixed ANCOVA, 3-way etkileşim, IRT GRM/theta modeli ve Bayesian preflight tablolarını üretir. Satır-düzeyi analiz verisi veya posterior örneklemi yazmaz.

`scripts/R/18_h2_sibling_relationships_audit.R`, H2 kardeş ilişkisi için family-mean Welch, APIM/dyadic mixed model, age-gap × same-sex moderation ve Olsen-Kenny dyadic CFA tablolarını üretir. Satır-düzeyi analiz verisi veya wide item verisi yazmaz.

`scripts/R/19_h3_parent_self_report_audit.R`, H3 anne öz-rapor için EMBU-P primary ANCOVA, antidepresan-ayarlı/stratified sensitivity ve IPTW+HC3 tablolarını üretir. Satır-düzeyi analiz frame'i veya PS/weight verisi yazmaz.

`scripts/R/20_h4_beck_parenting_sem_audit.R`, H4 Beck -> EMBU-P için full 50-item WLSMV latent SEM, reduced ordinal multi-group configural/metric screen ve Bayesian SEM preflight tablolarını üretir. Satır-düzeyi analiz frame'i, collapsed sensitivity frame'i veya posterior örneklemi yazmaz.

`scripts/R/21_h5_dyadic_concordance_audit.R`, H5 diadik tutarlılık için ICC+Bland-Altman, RSA, Common Fate, Olsen-Kenny CFA, k-coefficient ve klinik tutarsızlık aggregate tablolarını üretir. Satır-düzeyi dyad verisi yazmaz.

`scripts/R/29_apa_figures_audit.R`, KISIM XIII/40 Sprint A figür paketlerini (`strobe_flow`, `causal_dag`, `smd_love_plot`, `propensity_overlap`, `ses_correlation_heatmap`, `h1_forest`, `h1_three_way_emm`, `h2_apim_path`, `h3_stratified_forest`, `h4_sem_path`, `h5_ba_grid`, `h5_rsa_surface`, `specification_curve`, `sensemakr_contour`, `clinical_roc`, `clinical_dca`, `clinical_calibration`, `mediation_effects`, `lpa_fit_indices`, `network_graph`, `network_nct`, `clinical_cart_rf`, `bayesian_forest`, `bayesian_diagnostics`) üretir ve manifest tablosunu yazar. Figürler `outputs/figures/` altında git-dışı artefakt olarak kalır.

`scripts/R/30_apa_tables_audit.R`, KISIM XIII/40 APA tablo paketini (`apa_t01_sample_characteristics` ... `apa_t22_result_synthesis`) üretir ve `outputs/tables/apa_sprint_a_table_manifest.csv` manifestini yazar. Tablolar yalnız aggregate sonuç içerir; satır-düzeyi veri veya kimliklenebilir bilgi yazmaz.

`scripts/R/31_thesis_mapping_audit.R`, KISIM XIII/41 tez bölüm eşlemesini denetler; 5 chapter dosyası, 24 figür referansı, 22 tablo referansı ve `outputs/quarto/thesis.html` render çıktısının varlığını `outputs/tables/thesis_mapping_*.csv` altında aggregate olarak raporlar.

`scripts/R/32_final_plans_audit.R`, KISIM XIII/42, KISIM XV/44 ve KISIM XVI/45 için 3-makale yayın stratejisi, risk matrisi ve 24-haftalık plan aggregate tablolarını üretir. Çıktılar `outputs/tables/final_plan_*.csv` altında kalır.

`scripts/R/09_reporting_standards_audit.R`, STROBE + JARS-Quant + TRIPOD kontrol listesinin şemasını doğrular ve açık raporlama maddelerini `outputs/tables/reporting_standards_*.csv` altında izler.

## Docker Build

```bash
docker build -t t1dm-ebeveyn-repro .
```

Docker context bilinçli olarak ham veri, temizlenmiş veri, işlenmiş satır-düzeyi veri, credential dosyaları, `.env`, `_targets/`, `outputs/`, `tmp/` ve kitap PDF'lerini dışarıda bırakır.

## Docker İçinde Tez Render

```bash
docker run --rm t1dm-ebeveyn-repro
```

Bu komut imaj içinde kanonik veri bulunmuyorsa yalnız veri gerektirmeyen `_targets.R` hedeflerini ve HTML Quarto render'ını çalıştırır.

## Docker İçinde Kanonik Veri Doğrulama

Satır-düzeyi veriler imaja kopyalanmaz. Kanonik veri doğrulaması ve tam KISIM II targets hattı için `data/processed` klasörü salt-okunur mount edilir:

```bash
docker run --rm \
  -v "$PWD/data/processed:/home/rstudio/project/data/processed:ro" \
  t1dm-ebeveyn-repro \
  bash -lc "Rscript scripts/R/07_verify_reproducibility.R && Rscript scripts/R/10_hash_validate_load.R && Rscript -e 'targets::tar_make()'"
```

## `_targets.R` Sınırı

`_targets.R` KISIM XIII / 40 itibarıyla proje yolları, raw-data manifest, kanonik veri lock doğrulaması, hash kontrollü yükleme, hazırlık faktörleri, türetilmiş skor nesneleri, SES kompozitleri, eksik veri çoklu-çerçeve nesneleri, Tablo 1/SMD denge tabloları, Causal DAG strateji tabloları, Propensity Score/IPTW/Matching altyapısı, H1-H5 analizleri, KISIM VI-XII genişletilmiş analizleri ve KISIM XIII/40 APA figür + tablo Sprint A paketlerini hesaplar. Satır-düzeyi veri cache'i `_targets/` altında kalır ve public paketlere dahil edilmez.

## Hassas Veri Sınırı

Aşağıdakiler Docker imajına, OSF public dosyalarına veya Git commit'ine dahil edilmez:

- `data/raw/`
- `data/cleaned/`
- `data/identified/`
- `data/backup/`
- `data/processed/*.csv`
- `.env`
- credential JSON dosyaları
- `_targets/`
- `outputs/`
