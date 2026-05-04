# Causal DAG Runbook

**Kapsam:** KISIM III / 10  
**Uygulama:** `R/14_causal_dag.R`, `scripts/R/15_causal_dag_audit.R`  
**Son güncelleme:** 2026-04-27

## 1. Kapsam

Bu katman T1DM durumunun çocuk algısı üzerindeki total-effect analizleri için DAG tabanlı kovaryat stratejisini sabitler. Final CSV dosyalarını değiştirmez ve satır-düzeyi veri yazmaz.

## 2. Analiz DAG Kararı

SAP taslağındaki literal örnek DAG `dagitty` ile çalıştırıldığında beklenen `{SES, AgeGap, FamilySize}` adjustment setini vermez. Bu nedenle uygulanan `analysis_dag_v1`, SAP'in yazılı kovaryat stratejisini esas alır:

- `SES`, `AgeGap` ve `FamilySize` gözlenen baseline/design confounder olarak ele alınır.
- `Maternal_AD_use`, `Beck` ve `ParentingStyle` total-effect modellerinde ayarlanmaz; mediation/direct-effect sensitivity modellerinde ayrı ele alınır.
- `GeneticLiability` gözlenmeyen exposure-background düğümü olarak kaydedilir; primary adjustment setine dahil edilemez.

## 3. Çıktılar

| Çıktı | İçerik |
|---|---|
| `causal_dag_nodes.csv` | DAG düğümleri, roller, gözlenme durumu ve proxy değişkenleri |
| `causal_dag_edges.csv` | Yönlü kenarlar ve edge rolleri |
| `causal_dag_adjustment_sets.csv` | `dagitty::adjustmentSets()` çıktısı |
| `causal_dag_covariate_strategy.csv` | Total/direct/mediation kovaryat stratejisi |
| `causal_dag_variable_mapping.csv` | DAG düğümü -> repo kolon eşlemesi |
| `causal_dag_proxy_validation.csv` | Gerçek veride proxy kolon varlığı |
| `causal_dag_conditional_independencies.csv` | DAG implied conditional independencies |
| `causal_dag_model.txt` | `dagitty` model metni |
| `causal_dag.png` | Deterministik DAG figürü |

## 4. Birincil Adjustment Set

Primary total-effect analizlerinde adjustment set:

```text
SES + AgeGap + FamilySize
```

Repo karşılığı:

```text
ses_latent + age_gap + cocuk_sayisi
```

## 5. Komutlar

```bash
Rscript tests/test_causal_dag.R
Rscript scripts/R/15_causal_dag_audit.R
Rscript -e 'targets::tar_make()'
```

## 6. Targets

| Target | İçerik |
|---|---|
| `causal_dag_results` | DAG sonuç listesi |
| `causal_dag_nodes_table` | Node tablosu |
| `causal_dag_edges_table` | Edge tablosu |
| `causal_dag_adjustment_sets_table` | Adjustment set tablosu |
| `causal_dag_covariate_strategy_table` | Kovaryat stratejisi |
| `causal_dag_variable_mapping_table` | Repo değişken eşlemesi |
| `causal_dag_proxy_validation_table` | Proxy kolon doğrulaması |
| `causal_dag_target_summary` | Target özeti |
