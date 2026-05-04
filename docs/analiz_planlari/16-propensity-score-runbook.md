# Propensity Score Runbook

**Kapsam:** KISIM III / 11  
**Uygulama:** `R/15_propensity_score.R`, `scripts/R/16_propensity_score_audit.R`  
**Son güncelleme:** 2026-04-27

## 1. Kapsam

Bu katman DM ve kontrol aileleri için propensity score, stabilized IPTW, 1:1 nearest-neighbor matching ve doubly robust model şablonunu üretir. Final CSV dosyalarını değiştirmez; runner yalnız aggregate tablo ve figür yazar.

## 2. DAG Bağlantısı

Primary total-effect propensity modeli KISIM III / 10 `analysis_dag_v1` kararına bağlıdır.

```text
group_dm ~ ses_latent + age_gap + cocuk_sayisi
```

`anne_antidepresan`, `beck_total` ve ebeveynlik tutumu değişkenleri primary PS modeline alınmaz; bunlar direct-effect sensitivity, mediation veya stratified sensitivity fazlarında ele alınır.

## 3. Uygulama Kararları

| Bileşen | Karar |
|---|---|
| PS tahmini | `glm(..., family = binomial)` |
| Estimand | ATE total-effect primary |
| Ağırlık | Stabilized IPTW |
| Trim | 99. persentil üst sınırı |
| Denge ölçütü | Unweighted, IPTW ve matched SMD |
| Matching | Logit PS üzerinde 1:1 greedy nearest neighbor, replacement yok |
| Caliper | `0.2 * sd(logit_ps)` |
| Doubly robust | H1-H5 fazı için `outcome ~ group_dm + ses_latent + age_gap + cocuk_sayisi`, `weights = iptw_trimmed` planı |

SAP taslağındaki GBM/twang alternatifi paket ekleme kararı gerektirdiği için bu fazda çalıştırılmaz; ileride sensitivity modeli olarak ayrı karar ile eklenebilir.

## 4. Çıktılar

| Çıktı | İçerik |
|---|---|
| `propensity_model_summary.csv` | Logit PS katsayıları, OR ve Wald CI |
| `propensity_weight_summary.csv` | PS ve IPTW dağılım özetleri |
| `propensity_balance_before_after.csv` | Kovaryat SMD değerleri: öncesi, IPTW sonrası, matching sonrası |
| `propensity_matching_summary.csv` | Eşleşen çift sayısı, caliper ve logit mesafe özeti |
| `propensity_overlap_summary.csv` | Common support aralığı ve dışarıda kalan gözlem sayısı |
| `propensity_doubly_robust_plan.csv` | H1-H5 için outcome-spesifik DR model planı |
| `propensity_target_summary.csv` | Targets/pipeline kapsama özeti |
| `propensity_overlap.png` | Grup bazlı propensity score overlap figürü |

`df_family_propensity` satır-düzeyi PS/weight kolonlarını yalnız `_targets/` cache içinde tutar. Bu nesne Git, OSF public paket ve Docker context dışında kalır.

## 5. Komutlar

```bash
Rscript tests/test_propensity_score.R
Rscript scripts/R/16_propensity_score_audit.R
Rscript -e 'targets::tar_make()'
```

## 6. Targets

| Target | İçerik |
|---|---|
| `propensity_results` | PS sonuç listesi |
| `df_family_propensity` | Satır-düzeyi PS/weight nesnesi, yalnız `_targets/` |
| `propensity_model_summary_table` | Logit model özeti |
| `propensity_weight_summary_table` | Weight ve PS dağılım tablosu |
| `propensity_balance_before_after_table` | Unweighted/IPTW/matched SMD tablosu |
| `propensity_matching_summary_table` | Matching özeti |
| `propensity_overlap_summary_table` | Common support özeti |
| `propensity_doubly_robust_plan_table` | H1-H5 doubly robust model planı |
| `propensity_target_summary` | Pipeline özeti |
