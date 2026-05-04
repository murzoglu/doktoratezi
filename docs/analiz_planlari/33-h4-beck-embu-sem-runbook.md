# H4 Beck -> EMBU-P Latent SEM Runbook

**Kapsam:** KISIM V / 15  
**Uygulama:** `R/19_h4_beck_parenting_sem.R`, `scripts/R/20_h4_beck_parenting_sem_audit.R`  
**Son güncelleme:** 2026-04-28

## 1. Analiz Çerçevesi

H4, anne Beck depresyon belirti düzeyinin anne öz-rapor ebeveynlik tutumu latent boyutlarıyla ilişkisini test eder.

Primary latent SEM:

- EMBU-P dört latent faktör: `sicaklik`, `asiri_koruma`, `reddetme`, `karsilastirma`
- Beck latent faktör: `beck_dep`, `beck_1`-`beck_21`
- Kovaryatlar: `anne_yas_z`, `ses_latent_z`
- Estimator: `lavaan::sem(..., estimator = "WLSMV", ordered = 50 item, missing = "pairwise")`

Yapısal yollar:

```r
sicaklik ~ beck_dep + anne_yas_z + ses_latent_z
asiri_koruma ~ beck_dep + anne_yas_z + ses_latent_z
reddetme ~ beck_dep + anne_yas_z + ses_latent_z
karsilastirma ~ beck_dep + anne_yas_z + ses_latent_z
```

`scale(...)` terimleri analiz öncesi deterministik z-skor kolonlarına çevrilir.

## 2. Multi-Group Stratejisi

Tam 50-item ordinal multi-group SEM, gerçek veride grup-spesifik boş ordinal kategoriler ve yüksek hesap yükü nedeniyle default targets hattına alınmaz. Bunun yerine targets/audit içinde reduced ordinal measurement screen çalışır:

| Faktör | Reduced item set |
|---|---|
| `sicaklik` | `embu_p_q01`, `embu_p_q03`, `embu_p_q24` |
| `asiri_koruma` | `embu_p_q04`, `embu_p_q08`, `embu_p_q14` |
| `reddetme` | `embu_p_q05`, `embu_p_q09`, `embu_p_q10`, `embu_p_q28` |
| `karsilastirma` | `embu_p_q02`, `embu_p_q18`, `embu_p_q27` |
| `beck_dep` | `beck_1`-`beck_6` |

Default multi-group adımları `configural` ve `metric_loadings` ile sınırlıdır. `scalar_thresholds` ve `structural_regressions` için fonksiyonel opsiyon korunur:

```r
run_h4_multigroup_invariance(df, max_step = "structural_regressions")
```

Grup-spesifik boş ordinal kategoriler varsa yalnız multi-group sensitivity frame'inde bitişik kategoriye collapse edilir; mapping `h4_multigroup_sparse_collapse_map.csv` içinde raporlanır. Primary 50-item SEM raw itemlar üzerinde kalır.

## 3. Bayesian Katman

Bayesian SEM default audit/targets içinde MCMC çalıştırmaz. `blavaan` ve `posterior` uygunluğu, reduced model syntax'ı, prior ve sampler ayarları `h4_bayesian_sem_plan.csv` içinde preflight olarak tutulur.

Manuel çalıştırma fonksiyonu:

```r
fit_h4_bayesian_sem(df, seed = 20260428L, n.chains = 4L, burnin = 2000L, sample = 5000L)
```

Bu fonksiyon posterior örneklemi üretebilir; default pipeline satır-düzeyi veya posterior çıktısı yazmaz.

## 4. Komutlar

```bash
Rscript tests/test_h4_beck_parenting_sem.R
Rscript scripts/R/20_h4_beck_parenting_sem_audit.R
Rscript -e 'targets::tar_make()'
```

## 5. Outputs

| Output | İçerik |
|---|---|
| `outputs/tables/h4_scaling_summary.csv` | `anne_yas` ve `ses_latent` z-skor parametreleri |
| `outputs/tables/h4_ordered_item_diagnostics.csv` | 50 ordinal item kategori/missing/sparse diagnostic'i |
| `outputs/tables/h4_latent_sem_status.csv` | Full 50-item WLSMV SEM status |
| `outputs/tables/h4_latent_sem_fit_measures.csv` | Full SEM fit ölçüleri |
| `outputs/tables/h4_latent_sem_structural_paths.csv` | `beck_dep -> EMBU-P latent` yolları, standardized estimate ve FDR |
| `outputs/tables/h4_multigroup_status.csv` | Reduced multi-group configural/metric status |
| `outputs/tables/h4_multigroup_fit_measures.csv` | Reduced multi-group fit ölçüleri |
| `outputs/tables/h4_multigroup_comparison.csv` | Delta CFI/RMSEA invariance screen |
| `outputs/tables/h4_multigroup_structural_paths.csv` | Reduced multi-group path tahminleri |
| `outputs/tables/h4_multigroup_sparse_collapse_map.csv` | Multi-group için yapılan sparse kategori collapse haritası |
| `outputs/tables/h4_bayesian_sem_plan.csv` | Bayesian SEM preflight |
| `outputs/tables/h4_target_summary.csv` | Pipeline kapsam özeti |

## 6. Gerçek Veri Audit Özeti

| Metrik | Değer |
|---|---:|
| Aile sayısı | 241 |
| Full ordered item | 50 |
| Complete item row | 237 |
| Sparse item sayısı | 9 |
| Full latent SEM status | success |
| Full SEM structural path | 4 |
| Full SEM FDR < .05 path | 3 |
| Reduced multi-group ordered item | 19 |
| Reduced multi-group success | 2 / 2 |
| Sparse collapse mapping | 2 satır |
| Bayesian sampling default | FALSE |

Full SEM'de `beck_dep` daha düşük sıcaklık (`std.all = -0.285`), daha yüksek reddetme (`std.all = 0.329`) ve daha yüksek karşılaştırma (`std.all = 0.285`) ile FDR-düzeltmeli ilişkili bulundu; aşırı koruma yolu FDR < .05 değildir. Bu bulgular kesitsel latent ilişki olarak raporlanır, nedensel/aracılık iddiası değildir.
