# Faz II Carbon/Figma Şekil-Tablo Haritası

Üretim tarihi: `2026-05-02`

Kaynaklar:

- Faz II aktif tez bölümü: `chapters/06_post_hoc_genisleme.qmd`
- Faz II SAP: `docs/analiz_planlari/04-sap-faz2-posthoc.md`
- Faz II figür üretimi: `R/48_phase2_apa_outputs.R`
- Tez Bölüm 6 eşlemesi: `R/49_phase2_thesis_mapping.R`
- Rapor/tezde kullanılan tracked figürler: `docs/assets/figures/carbon/phase2/phase2_f*.svg`
- Generated kaynak figürler: `outputs/figures/phase2_f*.{png,svg}` (git-dışı, yeniden üretilebilir)
- Gerçekleşen tablolar: `outputs/tables/phase2_*.csv`

Bu harita, Faz II görsellerini Phase 1'deki Carbon SVG dizin yaklaşımıyla aynı disipline çeker: her çıktı kaynak tabloya, SAP kimliğine, tez bölümüne, Carbon/Figma revizyon durumuna ve raporlama kararına bağlanır.

## 1. Carbon/Figma Kaynak Doğrulaması

| Yüzey | Figma kaynağı | Canlı doğrulama | Kullanım kararı |
|---|---|---|---|
| Renk tokenları | IBM Color Library, `Uu7QTLz6ERkFJPD7cVEWel#2228:805` | `Default/Blue/60 = #0f62fe`, `Default/Gray/100 = #161616`, `Default/Purple/70 = #6929c4` döndü | Faz II grafik paleti ve SVG metadata kaynağı |
| Grafik tokenları | Carbon Charts Library, `503EVkMrbdCfkqBbfjLqA3#3984:105703` | `General/Text 01`, `General/Layer 01`, `General/Text accent` döndü | Çok serili grafiklerde Carbon Charts white 14 sırası |
| Tipografi | Carbon Type Sets v11, FSOT + npm snapshot | `figma-sync.py --check type --strict` drift bulmadı | Carbon HTML/rapor gövdesi için Productive/Expressive kararı korunur |
| Teknik diyagram | IBM Technical Diagram Library, `RtZDc7pMQt8HcgYTiitspr#345:5092` | Kök node için MCP "active selection" istedi; SVG metadata'ya kaynak kimliği eklendi | DAG doğrulama paneli Carbon teknik diyagram kimliğiyle izlenebilir hale getirildi |

Ek doğrulama:

- `figma-sync.py --check charts --strict`: FAIL 0, WARN 0.
- `figma-sync.py --check type --strict`: FAIL 0, WARN 0.
- `R/48_phase2_apa_outputs.R` revize edildi: SVG kökleri artık `data-carbon-style`, `data-figma-color-library`, `data-figma-carbon-charts-library`, `data-font` ve `data-chart-palette` metadata alanlarını taşır.

## 2. Gerçekleşen Faz II Figür Paketi

SAP Bölüm 93.2 başlangıçta sekiz figür planladı; Carbon revizyonu sonrası gerçekleşen APA/tez paketi 12 generated PNG/SVG ve 12 tracked SVG kopyaya genişletildi. Daha önce tablo/özet düzeyinde kalan tanı yaşı spline, Imai-Keele duyarlılık, DAG doğrulama, posterior predictive replication ve DCA heatmap çıktıları artık figürleşmiştir.

| Gerçekleşen ID | SAP/Tracker karşılığı | Kaynak tablo | Çıktı | Carbon/Figma revizyonu | Tez/rapor yeri | Ana mesaj |
|---|---|---|---|---|---|---|
| F2-F01 | SAP F2-F01, tracker F2-02 | `phase2_trifactor_loadings.csv`, `phase2_trifactor_fit_indices.csv` | `docs/assets/figures/carbon/phase2/phase2_f01_trifactor.svg` (`outputs/figures/phase2_f01_trifactor.{png,svg}` generated) | Carbon Charts 1-3; SVG metadata eklendi | `chapters/06_post_hoc_genisleme.qmd` 6.2 | Trait, indeks-method ve kardeş-method yükleri aynı madde yüzeyinde ayrışıyor |
| F2-F02 | SAP F2-F02, tracker F2-05 | `phase2_xinfo_summary.csv`, `phase2_xinfo_edges.csv`, `phase2_xinfo_nodes.csv` | `docs/assets/figures/carbon/phase2/phase2_f02_xinfo.svg` (`outputs/figures/phase2_f02_xinfo.{png,svg}` generated) | Carbon categorical + redundant stack labels; SVG metadata eklendi | 25.1; Bölüm 6.2 | Pooled ağda cross-informant kenar oranı düşük, yapı bilgi-veren içinde kapanıyor |
| F2-F03 | SAP F2-F03, tracker F2-06 | `phase2_floor_irt_group_delta.csv`, `phase2_floor_irt_theta_comparison.csv` | `docs/assets/figures/carbon/phase2/phase2_f03_floor_irt.svg` (`outputs/figures/phase2_f03_floor_irt.{png,svg}` generated) | Diverging yön kodu; gri eşik çizgileri; SVG metadata eklendi | 25.2; Bölüm 6.3 | Floor-aware theta H1 reddetme/aşırı koruma farkını büyütüyor |
| F2-F04 | SAP F2-F04, tracker F2-14/XXIII | `phase2_ad_moderation_h5_stratified_correlations.csv` | `docs/assets/figures/carbon/phase2/phase2_f04_h5_strat.svg` (`outputs/figures/phase2_f04_h5_strat.{png,svg}` generated) | Renk + şekil ile redundant encoding; SVG metadata eklendi | 25.3 ve 25.4; Bölüm 6.4-6.5 | H5 diadik korelasyonları grup ve AD strata düzeyinde ayrışıyor; grup farkı kesin değil |
| F2-F05 | SAP F2-F07, tracker F2-28/31 | `phase2_multi_h1_spec_results.csv`, `phase2_multi_h1_curve_summary.csv`, `phase2_multi_sca_inferential.csv` | `docs/assets/figures/carbon/phase2/phase2_f05_h1_spec_curve.svg` (`outputs/figures/phase2_f05_h1_spec_curve.{png,svg}` generated) | Specification curve tarifi; median çizgisi; SVG metadata eklendi | 25.8; Bölüm 6.9 | 120/120 başarılı specification içinde H1 yönü pozitif kalıyor |
| F2-F06 | SAP F2-F08, tracker F2-32 | `phase2_meta_combined_studies.csv`, `phase2_meta_pooling_summary.csv` | `docs/assets/figures/carbon/phase2/phase2_f06_meta_forest.svg` (`outputs/figures/phase2_f06_meta_forest.{png,svg}` generated) | Forest plot istisnası: nötr CI + mavi pooled işaret; SVG metadata eklendi | 25.9; Bölüm 6.10 | Pooled etki `0.139 [0.049, 0.230]`, çalışma etkileri literatür merkezine yakın |
| F2-F07 | Tracker F2-05 ayrıntı | `phase2_xinfo_edges.csv`, `phase2_xinfo_centrality.csv` | `docs/assets/figures/carbon/phase2/phase2_f07_xinfo_network.svg` (`outputs/figures/phase2_f07_xinfo_network.{png,svg}` generated) | Carbon Charts categorical + cross-informant shape encoding; SVG metadata eklendi | 25.1; Bölüm 6.2 | Cross-informant ağ, edge ağırlığı ve bilgi-veren kapanmasını ayrıntılı gösteriyor |
| F2-F08 | SAP F2-F05, tracker F2-18 | `phase2_hba1c_spline.csv` | `docs/assets/figures/carbon/phase2/phase2_f08_dx_age_spline.svg` (`outputs/figures/phase2_f08_dx_age_spline.{png,svg}` generated) | Paired R² bar paneli; LRT p etiketi; SVG metadata eklendi | 25.5; Bölüm 6.6 | Tanı yaşı spline 4/4 alt ölçekte lineer modele anlamlı üstünlük sağlamıyor |
| F2-F09 | SAP F2-F06, tracker F2-21 | `phase2_imai_sensitivity_grid.csv`, `phase2_imai_summary.csv` | `docs/assets/figures/carbon/phase2/phase2_f09_imai_sensitivity.svg` (`outputs/figures/phase2_f09_imai_sensitivity.{png,svg}` generated) | Rho x adjusted ACME küçük çoklu panel; critical rho kesikli çizgi; SVG metadata eklendi | 25.6; Bölüm 6.7 | Dolaylı etkiler ölçülmemiş karıştırıcıya karşı çok kırılgan |
| F2-F10 | Tracker F2-22/F2-24 | `phase2_dag_ci_tests.csv`, `phase2_dag_three_level.csv` | `docs/assets/figures/carbon/phase2/phase2_f10_dag_validation.svg` (`outputs/figures/phase2_f10_dag_validation.{png,svg}` generated) | Carbon tile/technical validation paneli; Technical Diagram metadata eklendi | 25.6; Bölüm 6.7 | DAG implied CI 12/12 tutarlı; yıl kümelenmesi alt ölçeğe göre değişiyor |
| F2-F11 | Tracker F2-33 | `phase2_meta_ppc_summary.csv` | `docs/assets/figures/carbon/phase2/phase2_f11_ppc_replication.svg` (`outputs/figures/phase2_f11_ppc_replication.{png,svg}` generated) | PPC interval + observed marker; SVG metadata eklendi | 25.9; Bölüm 6.10 | 4/4 outcome posterior predictive replication ile uyumlu |
| F2-F12 | Tracker F2-37 | `phase2_clinical_dca_heatmap.csv` | `docs/assets/figures/carbon/phase2/phase2_f12_dca_heatmap.svg` (`outputs/figures/phase2_f12_dca_heatmap.{png,svg}` generated) | Diverging heatmap; sampled value labels; SVG metadata eklendi | 25.10; Bölüm 6.11 | Net benefit threshold ve cost-ratio arttıkça hızlı azalıyor |

## 3. Daha Önce Eksik Olan ve Bu Revizyonda Üretilen Görseller

| SAP/Tracker ID | Önceki durum | Üretilen çıktı | Kaynak veri | Carbon/Figma biçimi |
|---|---|---|---|---|
| F2-05 ayrıntı | Sadece edge-summary figürü vardı | `phase2_f07_xinfo_network.{png,svg}` | `phase2_xinfo_edges.csv`, `phase2_xinfo_centrality.csv` | Edge map; renk=işaret, şekil=cross-informant, boyut=|weight| |
| F2-F05 / F2-18 | Tablo/karar düzeyinde kalmıştı | `phase2_f08_dx_age_spline.{png,svg}` | `phase2_hba1c_spline.csv` | Lineer vs spline R² paneli + LRT p etiketi |
| F2-F06 / F2-21 | Rapor metninde kırılganlık tablosu vardı | `phase2_f09_imai_sensitivity.{png,svg}` | `phase2_imai_sensitivity_grid.csv`, `phase2_imai_summary.csv` | Rho x adjusted ACME curve; critical rho çizgisi |
| F2-22/F2-24 | `pcalg` fallback nedeniyle figür yoktu | `phase2_f10_dag_validation.{png,svg}` | `phase2_dag_ci_tests.csv`, `phase2_dag_three_level.csv` | Tile-based DAG validation panel; Technical Diagram metadata |
| F2-33 | PPC kararı tablo düzeyindeydi | `phase2_f11_ppc_replication.{png,svg}` | `phase2_meta_ppc_summary.csv` | Replike %95 aralık + gözlenen t marker |
| F2-37 | Heatmap CSV vardı, figür yoktu | `phase2_f12_dca_heatmap.{png,svg}` | `phase2_clinical_dca_heatmap.csv` | Diverging net-benefit heatmap |

## 4. SAP Tablo Listesi ve Gerçekleşen CSV Aileleri

| SAP tablo ID | SAP başlığı | Gerçekleşen çıktı ailesi | Raporlama kararı |
|---|---|---|---|
| F2-T01 | Trifactor T-CFA fit ve loadings | `phase2_trifactor_fit_indices.csv`, `phase2_trifactor_loadings.csv`, `phase2_trifactor_method_correlation.csv`, `phase2_trifactor_variance.csv`, `phase2_trifactor_coverage.csv`, `phase2_trifactor_status.csv`, `phase2_trifactor_syntax.csv`, `phase2_trifactor_target_summary.csv` | Figür F2-F01 ile birlikte ana sonuç |
| F2-T02 | Latent informant discrepancy SEM | `phase2_disc_fit_indices.csv`, `phase2_disc_latent_correlation.csv`, `phase2_disc_variance.csv`, `phase2_disc_predictor_paths.csv`, `phase2_disc_coverage.csv`, `phase2_disc_scaling.csv`, `phase2_disc_status.csv`, `phase2_disc_target_summary.csv` | H1-H3 ayrışmasının yapısal kanıtı |
| F2-T03 | Tobit IRT / floor-aware IRT | `phase2_floor_irt_item_parameters.csv`, `phase2_floor_irt_floor_summary.csv`, `phase2_floor_irt_theta_comparison.csv`, `phase2_floor_irt_group_delta.csv`, `phase2_floor_irt_status.csv`, `phase2_floor_irt_target_summary.csv` | Figür F2-F03 ile ana psikometrik robustleştirme |
| F2-T04 | Reliability generalization | `phase2_omegah_fit_indices.csv`, `phase2_omegah_loadings.csv`, `phase2_omegah_metrics_summary.csv`, `phase2_omegah_subscale_metrics.csv`, `phase2_omegah_status.csv`, `phase2_omegah_target_summary.csv`; ESEM için `phase2_esem_*` | Reddetme alt skorunun sınırlılığını taşır |
| F2-T05 | AD mediator indirect + sensitivity | `phase2_ad_mediator_estimates.csv`, `phase2_ad_mediator_sensitivity.csv`, `phase2_ad_mediator_status.csv`, `phase2_ad_family_summary.csv` | AD aracı kanıtı yok |
| F2-T06 | AD x group moderation | `phase2_ad_moderation_h1_*`, `phase2_ad_moderation_h4_*`, `phase2_ad_moderation_h5_stratified_correlations.csv`, `phase2_ad_beck_interaction_*` | Figür F2-F04 ile strata anlatımı |
| F2-T07 | MTMM trait/method varyans payları | `phase2_h5ext_mtmm_fit_indices.csv`, `phase2_h5ext_mtmm_variance.csv`, `phase2_h5ext_mtmm_status.csv` | H5 method ayrışması |
| F2-T08 | Sibling-pair concordance ICC | `phase2_h5ext_sibling_icc.csv`, `phase2_h5ext_strategy_estimates.csv`, `phase2_h5ext_strategy_pooled.csv`, `phase2_h5ext_beck_moderation_*`, `phase2_h5ext_target_summary.csv` | H5 pooled yorum ve PDT hipotezi |
| F2-T09 | HbA1c x parenting Bayesian posterior | `phase2_hba1c_bayesian_posterior.csv`, `phase2_hba1c_bayesian_status.csv`, `phase2_hba1c_dm_summary.csv`, `phase2_hba1c_spline.csv`, `phase2_hba1c_ispad_logistic.csv`, `phase2_hba1c_target_summary.csv` | Complete-case hipotez üretici; F2-F08 spline karar figürü |
| F2-T10 | Imai-Keele rho-critical sensitivity | `phase2_imai_summary.csv`, `phase2_imai_sensitivity_grid.csv`, `phase2_imai_status.csv`, `phase2_imai_target_summary.csv`, `phase2_cprime_triangulation.csv`, `phase2_dag_*` | Aracılık yorumunu sınırlayan ana tablo |
| F2-T11 | H1 multiverse özeti | `phase2_multi_h1_spec_grid.csv`, `phase2_multi_h1_spec_results.csv`, `phase2_multi_h1_curve_summary.csv`, `phase2_multi_h4_spec_results.csv`, `phase2_multi_h4_summary.csv`, `phase2_multi_bma.csv`, `phase2_multi_sca_inferential.csv`, `phase2_multi_target_summary.csv` | SAP 240 hedefi yerine gerçekleşen 120 spec açık belirtilmeli |
| F2-T12 | Bayesian meta-analytic pooling | `phase2_meta_combined_studies.csv`, `phase2_meta_pooling_summary.csv`, `phase2_meta_pooling_status.csv`, `phase2_meta_pooling_shrunk.csv`, `phase2_meta_ppc_summary.csv`, `phase2_meta_eb_shrunk.csv`, `phase2_meta_eb_outlier_summary.csv`, `phase2_meta_target_summary.csv` | Figür F2-F06 ile meta-analitik konum |

## 5. Ek Gerçekleşen Tablo Aileleri

| Aile | Dosya sayısı | Kapsam | Haritadaki yer |
|---|---:|---|---|
| `phase2_ad_*` | 12 | Antidepresan mediator/moderasyon/strata | F2-T05, F2-T06, F2-F04 |
| `phase2_h5ext_*` | 10 | MTMM, ICC, strategy pooling, Beck moderation | F2-T07, F2-T08, F2-F04 |
| `phase2_trifactor_*` | 8 | Trifactor yapı | F2-T01, F2-F01 |
| `phase2_multi_*` | 8 | H1/H4 multiverse, BMA, SCA | F2-T11, F2-F05 |
| `phase2_meta_*` | 8 | Meta-pooling, PPC, EB shrinkage | F2-T12, F2-F06 |
| `phase2_disc_*` | 8 | Latent discrepancy SEM | F2-T02 |
| `phase2_xinfo_*` | 7 | Cross-informant ağ | F2-F02 |
| `phase2_floor_irt_*` | 6 | Floor-aware IRT | F2-T03, F2-F03 |
| `phase2_omegah_*` | 6 | Reliability generalization | F2-T04 |
| `phase2_hba1c_*` | 6 | Klinik stratifikasyon | F2-T09 |
| `phase2_esem_*` | 5 | ESEM fallback/sınırlılık | F2-T04 ek sınırlılık |
| `phase2_dist_*` | 5 | Quantile, distributional, beta/bounded model | Faz II dağılımsal bölüm |
| `phase2_clinical_*` | 5 | AUC, sNB, DCA heatmap data | Klinik karar modeli |
| `phase2_power_*` | 4 | Multilevel power, APIM, Bayesian SSD | Replikasyon gücü |
| `phase2_dag_*` | 4 | DAG implied CI ve üç düzeyli model | F2-T10 |
| `phase2_imai_*` | 4 | Imai-Keele duyarlılık | F2-T10 |
| `phase2_thesis_*` | 4 | Bölüm 6 mapping, yayın planı, paragraf seed | Tez entegrasyonu |
| `phase2_apa_*` | 2 | Çekirdek APA özet ve target summary | Faz II yönetici özeti |
| `phase2_cprime_triangulation.csv` | 1 | c' direct-effect triangulation | F2-T10 ek kanıt |

Toplam gerçekleşen Phase 2 tablo artefaktı: `113` CSV.

## 6. Tez ve CSR İçin Kullanım Sırası

| Bölüm | Birincil tablo | Birincil figür | Not |
|---|---|---|---|
| Faz II sinopsis | `phase2_apa_summary_table.csv` | yok | Carbon HTML raporda KPI/stat-grid için ana kaynak |
| Multi-informant yapı | `phase2_trifactor_*`, `phase2_disc_*`, `phase2_xinfo_*` | F2-F01, F2-F02 | Çocuk/anne/kardeş ayrışması |
| Psikometrik robustleştirme | `phase2_floor_irt_*`, `phase2_omegah_*`, `phase2_esem_*` | F2-F03 | Ölçüm sınırlılığı + H1 yönünün korunması |
| Antidepresan | `phase2_ad_*` | F2-F04 | AD klinik yük göstergesi, mekanizma değil |
| H5 genişletmesi | `phase2_h5ext_*` | F2-F04 | Aynı figür paylaşımlı kullanılabilir |
| Klinik stratifikasyon | `phase2_hba1c_*` | F2-F08 | Complete-case; tanı yaşı spline karar paneli |
| Nedensel aracılık/DAG | `phase2_imai_*`, `phase2_dag_*`, `phase2_cprime_triangulation.csv` | F2-F09, F2-F10 | Duyarlılık ve DAG doğrulama görselleştirildi |
| Distribüsyonel modeller | `phase2_dist_*` | yok | İleride raincloud/quantile panel üretilebilir |
| Multiverse/SCA | `phase2_multi_*` | F2-F05 | 120 spec gerçekleşen sayı olarak korunmalı |
| Meta-pooling | `phase2_meta_*` | F2-F06, F2-F11 | Forest plot + PPC replication paneli |
| Klinik karar/power | `phase2_clinical_*`, `phase2_power_*` | F2-F12 | DCA heatmap figürleşti; power tabloda kaldı |

## 7. Revizyon Kontrol Listesi

| Kontrol | Durum |
|---|---|
| Phase 2 gerçek figürleri tespit edildi | PASS: 12 PNG + 12 SVG |
| SAP'teki figür planı ile gerçekleşen 12 figür paketi karşılaştırıldı | PASS |
| SVG'lere Carbon/Figma metadata eklendi | PASS |
| Carbon Charts paleti drift kontrolü | PASS |
| Carbon type/Figma uyumu | PASS |
| Teknik diyagram gereksinimi | PASS: DAG validation SVG'lerinde Technical Diagram Library metadata mevcut |
| Tüm `phase2_*.csv` tablo aileleri kapsandı | PASS: 113 CSV, 19 aile |

## 8. Kanonik Karar

Faz II raporu ve tez Bölüm 6 için kanonik görsel paket artık `F2-F01` ile `F2-F12` arasındaki 12 Carbon figürdür. Yeni eklenen `F2-F07`-`F2-F12` çıktıları ana sonuç iddiasını değiştirmez; daha önce tablo/özet düzeyinde kalan ağ ayrıntısı, tanı yaşı spline, Imai-Keele duyarlılık, DAG doğrulama, PPC ve DCA yüzeylerini tez/CSR içinde görsel olarak izlenebilir hale getirir.
