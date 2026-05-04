# Carbon SVG Figure Dizin ve Cross-Reference Haritası

Üretim zamanı: `2026-05-01 15:48:49 UTC`

Bu dizin, tez analizleri kapsamında şu ana dek üretilmiş benzersiz görsel çıktıların Carbon uyumlu SVG karşılıklarını tek klasör ağacında toplar. Kaynak envanter dört yüzeyden derlenmiştir: aktif `_targets`/`outputs/figures` figür seti, psikometrik validasyon Quarto görselleri, demografik-tıbbi Quarto görselleri ve Faz II post-hoc Carbon figürleri.

## Kapsam ve Üretim Modu

- Toplam SVG: **64**
- Aktif bulgular / `_targets` SVG: **25**
- Psikometrik validasyon Quarto SVG: **7**
- Demografik-tıbbi Quarto SVG: **20**
- Faz II post-hoc Carbon SVG: **12**
- Dışlananlar: `.quarto/_freeze` altındaki birebir kopyalar, `tmp/pdfs/*` sayfa görüntüleri, form/book PDF'leri ve Carbon HTML/PDF rapor çıktıları. Bunlar analiz figürü değil, render kopyası ya da kaynak belgedir.

## Aslına Uygunluk Denetimi

- `targets-native-vector`: `_targets` store içindeki ggplot nesnesi doğrudan `grDevices::svg()` ile basıldı; kaynak PNG varlığı ve hash'i manifestte tutuldu.
- `missing-native-vector`: eksik veri haritası `missing_results$frames$fiml_primary` üzerinden `naniar::vis_miss()` ile yeniden çizildi.
- `quarto-native-vector`: ilgili Quarto belgesi geçici kopya üzerinden `dev = "svg"` ile render edildi; frozen PNG kaynaklarıyla eşlenen chunk/cross-ref kimlikleri korundu.
- IBM Plex Sans, SVG aygıtı açılmadan önce fontconfig'e tanıtıldı; R/Cairo aygıtının ürettiği metinler IBM Plex glyph outline'ları olarak SVG içinde taşınır.
- Eski tez paleti hex değerleri resmi `@carbon/charts` white-theme kategorik sırasına ve Carbon semantic tokenlarına normalize edildi: Purple 70, Cyan 50, Teal 70, Magenta 70, Red 50, Green 60, Blue 80, Orange 70 ve Carbon gri rampası.
- Carbon Charts repo estetik rolleri uygulanmıştır: başlık `text-primary`/semibold, axis title semibold, axis text `text-secondary`, graph-grid `layer-accent-01`, legend bottom ve IBM Plex Sans chart typography.
- Flow/diagram figürleri Figma IBM Technical Diagram Library (`RtZDc7pMQt8HcgYTiitspr`) rollerine göre özel SVG renderer ile yeniden çizildi: Large node, Small node, Connector, Connector line ending, Label text, Label pill, Flow number ve Legend. Bu figürlerde generic chart grid/axis/raster katmanı yoktur; connector stroke'ları Carbon border tokenlarına çekildi.
- Final SVG'ler raster-wrapper değildir. Ancak heatmap, missingness map, RSA surface, sensemakr contour ve bazı ağ/surface panelleri ggplot tarafından SVG içinde raster katman olarak temsil edilebilir; bu durum audit notu olarak işaretlenir.

Ayrıntılı makine-okunur kayıtlar: [manifest.csv](audits/manifest.csv), [fidelity-audit.csv](audits/fidelity-audit.csv), [carbon-aesthetic-audit.csv](audits/carbon-aesthetic-audit.csv) ve [technical-diagram-audit.csv](audits/technical-diagram-audit.csv).

## Aktif Bulgular / CSR ve Tez Bölümü Figürleri

| ID | SVG | Cross-ref | İlişkili analiz | Üretim modu | Denetim | Carbon stil | Estetik audit | Technical Diagram |
|---|---|---|---|---|---|---|---|---|
| strobe_flow | [fig-01-strobe-flow.svg](primary/fig-01-strobe-flow.svg) | `@fig-strobe-flow` | Analitik akış / STROBE | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | PASS: full Figma Technical Diagram Library SVG |
| causal_dag | [fig-02-causal-dag.svg](primary/fig-02-causal-dag.svg) | `@fig-causal-dag` | DAG ve ayarlama seti | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | PASS: full Figma Technical Diagram Library SVG |
| smd_love_plot | [fig-03-smd-love-plot.svg](primary/fig-03-smd-love-plot.svg) | `@fig-smd-love` | Propensity denge | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| propensity_overlap | [fig-04-propensity-overlap.svg](primary/fig-04-propensity-overlap.svg) | `@fig-propensity-overlap` | Propensity ortak destek | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| ses_correlation_heatmap | [fig-05-ses-correlation-heatmap.svg](primary/fig-05-ses-correlation-heatmap.svg) | `@fig-ses-correlation` | SES kompozit validasyonu | targets-native-vector | PASS: native SVG; heatmap/surface benzeri raster katman içeriyor | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts; raster/gradient istisnası notlandı | N/A |
| missing_pattern_primary | [fig-06-missing-pattern-primary.svg](primary/fig-06-missing-pattern-primary.svg) | `missing-data-audit` | Eksik veri yapısı | missing-native-vector | PASS: native SVG; heatmap/surface benzeri raster katman içeriyor | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts; raster/gradient istisnası notlandı | N/A |
| h1_forest | [fig-07-h1-forest.svg](primary/fig-07-h1-forest.svg) | `@fig-h1-forest` | H1 çocuk algısı | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| h1_three_way_emm | [fig-08-h1-three-way-emm.svg](primary/fig-08-h1-three-way-emm.svg) | `@fig-h1-three-way-emm` | H1 etkileşim tanısı | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| h2_apim_path | [fig-09-h2-apim-path.svg](primary/fig-09-h2-apim-path.svg) | `@fig-h2-apim-path` | H2 kardeş ilişkisi APIM | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | PASS: full Figma Technical Diagram Library SVG |
| h3_stratified_forest | [fig-10-h3-stratified-forest.svg](primary/fig-10-h3-stratified-forest.svg) | `@fig-h3-stratified-forest` | H3 anne öz-bildirimi | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| h4_sem_path | [fig-11-h4-sem-path.svg](primary/fig-11-h4-sem-path.svg) | `@fig-h4-sem-path` | H4 Beck -> EMBU-P SEM | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | PASS: full Figma Technical Diagram Library SVG |
| h5_ba_grid | [fig-12-h5-ba-grid.svg](primary/fig-12-h5-ba-grid.svg) | `@fig-h5-bland-altman` | H5 manifest uyum | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| h5_rsa_surface | [fig-13-h5-rsa-surface.svg](primary/fig-13-h5-rsa-surface.svg) | `@fig-h5-rsa-surface` | H5 RSA uyum yüzeyi | targets-native-vector | PASS: native SVG; heatmap/surface benzeri raster katman içeriyor | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts; raster/gradient istisnası notlandı | N/A |
| mediation_effects | [fig-14-mediation-effects.svg](primary/fig-14-mediation-effects.svg) | `@fig-mediation-effects` | KISIM VI mediation | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| lpa_fit_indices | [fig-15-lpa-fit-indices.svg](primary/fig-15-lpa-fit-indices.svg) | `@fig-lpa-fit-indices` | KISIM VII LPA | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| network_graph | [fig-16-network-graph.svg](primary/fig-16-network-graph.svg) | `@fig-network-graph` | KISIM VIII ağ modeli | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | PASS: full Figma Technical Diagram Library SVG |
| network_nct | [fig-17-network-nct.svg](primary/fig-17-network-nct.svg) | `@fig-network-nct` | KISIM VIII NCT | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| clinical_roc | [fig-18-clinical-roc.svg](primary/fig-18-clinical-roc.svg) | `@fig-clinical-roc` | KISIM IX ROC | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| clinical_dca | [fig-19-clinical-dca.svg](primary/fig-19-clinical-dca.svg) | `@fig-clinical-dca` | KISIM IX DCA | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| clinical_calibration | [fig-20-clinical-calibration.svg](primary/fig-20-clinical-calibration.svg) | `@fig-clinical-calibration` | KISIM IX kalibrasyon | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| clinical_cart_rf | [fig-21-clinical-cart-rf.svg](primary/fig-21-clinical-cart-rf.svg) | `@fig-clinical-cart-rf` | KISIM IX CART/RF | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| specification_curve | [fig-22-specification-curve.svg](primary/fig-22-specification-curve.svg) | `@fig-specification-curve` | KISIM XI multiverse | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| sensemakr_contour | [fig-23-sensemakr-contour.svg](primary/fig-23-sensemakr-contour.svg) | `@fig-sensemakr-contour` | KISIM XI sensemakr/E-value | targets-native-vector | PASS: native SVG; heatmap/surface benzeri raster katman içeriyor | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts; raster/gradient istisnası notlandı | N/A |
| bayesian_forest | [fig-24-bayesian-forest.svg](primary/fig-24-bayesian-forest.svg) | `@fig-bayesian-forest` | KISIM XII Bayesçi forest | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| bayesian_diagnostics | [fig-25-bayesian-diagnostics.svg](primary/fig-25-bayesian-diagnostics.svg) | `@fig-bayesian-diagnostics` | KISIM XII MCMC tanıları | targets-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |

## Psikometrik Validasyon Figürleri

| ID | SVG | Cross-ref | İlişkili analiz | Üretim modu | Denetim | Carbon stil | Estetik audit | Technical Diagram |
|---|---|---|---|---|---|---|---|---|
| reliability | [psychval-01-reliability.svg](psychometric/psychval-01-reliability.svg) | `@fig-reliability` | Psikometrik güvenirlik | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| floor | [psychval-02-floor.svg](psychometric/psychval-02-floor.svg) | `@fig-floor` | Madde taban etkisi | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| cfa | [psychval-03-cfa.svg](psychometric/psychval-03-cfa.svg) | `@fig-cfa` | CFA uyum göstergeleri | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| invariance | [psychval-04-invariance.svg](psychometric/psychval-04-invariance.svg) | `@fig-invariance` | Ölçüm değişmezliği | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| icc | [psychval-05-icc.svg](psychometric/psychval-05-icc.svg) | `@fig-icc` | Aile içi ICC | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| validity | [psychval-06-validity.svg](psychometric/psychval-06-validity.svg) | `@fig-validity` | Geçerlik korelasyonları | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| multiverse | [psychval-07-multiverse.svg](psychometric/psychval-07-multiverse.svg) | `@fig-multiverse` | Reddetme multiverse | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |

## Demografik ve Tıbbi Rapor Figürleri

| ID | SVG | Cross-ref | İlişkili analiz | Üretim modu | Denetim | Carbon stil | Estetik audit | Technical Diagram |
|---|---|---|---|---|---|---|---|---|
| grup-dagilim | [demo-01-grup-dagilim.svg](demographic/demo-01-grup-dagilim.svg) | `@fig-grup-dagilim` | Örneklem grup dağılımı | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| cocuk-yas-dagilim | [demo-02-cocuk-yas-dagilim.svg](demographic/demo-02-cocuk-yas-dagilim.svg) | `@fig-cocuk-yas-dagilim` | Çocuk yaşı ve kardeş yaş farkı | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| cinsiyet-grup | [demo-03-cinsiyet-grup.svg](demographic/demo-03-cinsiyet-grup.svg) | `@fig-cinsiyet-grup` | Cinsiyet oranları | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| same-sex | [demo-04-same-sex.svg](demographic/demo-04-same-sex.svg) | `@fig-same-sex` | Kardeş cinsiyet kompozisyonu | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| aile-buyuklugu | [demo-05-aile-buyuklugu.svg](demographic/demo-05-aile-buyuklugu.svg) | `@fig-aile-buyuklugu` | Aile büyüklüğü | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| anne-yas | [demo-06-anne-yas.svg](demographic/demo-06-anne-yas.svg) | `@fig-anne-yas` | Anne yaşı | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| beck-grup | [demo-07-beck-grup.svg](demographic/demo-07-beck-grup.svg) | `@fig-beck-grup` | Beck toplam puanı | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| beck-severity | [demo-08-beck-severity.svg](demographic/demo-08-beck-severity.svg) | `@fig-beck-severity` | Beck şiddet kategorisi | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| antidep | [demo-09-antidep.svg](demographic/demo-09-antidep.svg) | `@fig-antidep` | Antidepresan kullanımı | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| ses-density | [demo-10-ses-density.svg](demographic/demo-10-ses-density.svg) | `@fig-ses-density` | Latent SES dağılımı | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| egitim | [demo-11-egitim.svg](demographic/demo-11-egitim.svg) | `@fig-egitim` | Anne/eş eğitim düzeyi | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| dm-eksik | [demo-12-dm-eksik.svg](demographic/demo-12-dm-eksik.svg) | `@fig-dm-eksik` | DM klinik gösterge tamamlanması | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| hba1c | [demo-13-hba1c.svg](demographic/demo-13-hba1c.svg) | `@fig-hba1c` | HbA1c dağılımı | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| hba1c-target | [demo-14-hba1c-target.svg](demographic/demo-14-hba1c-target.svg) | `@fig-hba1c-target` | HbA1c hedef kategorileri | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| dm-suresi | [demo-15-dm-suresi.svg](demographic/demo-15-dm-suresi.svg) | `@fig-dm-suresi` | DM süresi ve tanı yaşı | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| tani-strata | [demo-16-tani-strata.svg](demographic/demo-16-tani-strata.svg) | `@fig-tani-strata` | Tanı yaşı üç strata | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| smd-love | [demo-17-smd-love.svg](demographic/demo-17-smd-love.svg) | `@fig-smd-love` | Ham kovaryat dengesi | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| ps-density | [demo-18-ps-density.svg](demographic/demo-18-ps-density.svg) | `@fig-ps-density` | Logit propensity yoğunluğu | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| iptw-balance | [demo-19-iptw-balance.svg](demographic/demo-19-iptw-balance.svg) | `@fig-iptw-balance` | IPTW dengeleme etkisi | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |
| eksik-degisken | [demo-20-eksik-degisken.svg](demographic/demo-20-eksik-degisken.svg) | `@fig-eksik-degisken` | Aile düzeyi eksik veri | quarto-native-vector | PASS: native SVG, kaynak PNG mevcut | PASS: IBM Plex + Carbon Charts metadata/palette | PASS: Carbon Charts | N/A |

## Faz II Post-Hoc Figürleri

| ID | SVG | CSR yeri | İlişkili analiz |
|---|---|---|---|
| F2-F01 | [phase2_f01_trifactor.svg](phase2/phase2_f01_trifactor.svg) | CSR 18.3 | Trifactor T-CFA |
| F2-F02 | [phase2_f02_xinfo.svg](phase2/phase2_f02_xinfo.svg) | CSR 18.3 | Cross-informant edge oranı |
| F2-F03 | [phase2_f03_floor_irt.svg](phase2/phase2_f03_floor_irt.svg) | CSR 18.4 | Floor-aware IRT |
| F2-F04 | [phase2_f04_h5_strat.svg](phase2/phase2_f04_h5_strat.svg) | CSR 18.5-18.6 | H5 antidepresan strata |
| F2-F05 | [phase2_f05_h1_spec_curve.svg](phase2/phase2_f05_h1_spec_curve.svg) | CSR 18.9 | H1 specification curve |
| F2-F06 | [phase2_f06_meta_forest.svg](phase2/phase2_f06_meta_forest.svg) | CSR 18.9 | Meta-analitik forest |
| F2-F07 | [phase2_f07_xinfo_network.svg](phase2/phase2_f07_xinfo_network.svg) | CSR 18.3 | Cross-informant GGM |
| F2-F08 | [phase2_f08_dx_age_spline.svg](phase2/phase2_f08_dx_age_spline.svg) | CSR 18.7 | Tanı yaşı spline |
| F2-F09 | [phase2_f09_imai_sensitivity.svg](phase2/phase2_f09_imai_sensitivity.svg) | CSR 18.8 | Imai duyarlılık |
| F2-F10 | [phase2_f10_dag_validation.svg](phase2/phase2_f10_dag_validation.svg) | CSR 18.8 | DAG validasyon |
| F2-F11 | [phase2_f11_ppc_replication.svg](phase2/phase2_f11_ppc_replication.svg) | CSR 18.9 | Posterior predictive replication |
| F2-F12 | [phase2_f12_dca_heatmap.svg](phase2/phase2_f12_dca_heatmap.svg) | CSR 18.10 | Klinik karar DCA heatmap |

## Analitik İlişki Haritası

- **Akış ve tasarım katmanı:** `fig-01-strobe-flow`, `fig-02-causal-dag`, `fig-03-smd-love-plot`, `fig-04-propensity-overlap`, `fig-05-ses-correlation-heatmap`, `fig-06-missing-pattern-primary` çalışma akışını, karıştırıcı stratejisini, dengeyi, ortak destek alanını, SES proxy doğrulamasını ve eksik veri çerçevesini belgeler.
- **H1-H5 hipotez katmanı:** `fig-07` ile `fig-13` çocuk algısı, kardeş ilişkisi, anne öz-bildirimi, Beck-ebeveynlik SEM ve diadik tutarlılık bulgularını doğrudan tez hipotezlerine bağlar.
- **Genişletilmiş analiz katmanı:** `fig-14` ile `fig-17` mediation, LPA ve ağ analizlerini; `fig-18` ile `fig-21` klinik fayda hattını; `fig-22` ile `fig-25` multiverse/sensemakr/Bayesçi sağlamlık katmanını taşır.
- **Psikometrik geçerlik katmanı:** `psychval-*` seti EMBU-P/EMBU-C/KİA/SRQ ölçeklerinin güvenirlik, taban etkisi, CFA, invaryans, ICC, yakınsak geçerlik ve reddetme multiverse kararlarını destekler.
- **Tanımlayıcı-demografik katman:** `demo-*` seti örneklem dağılımı, çocuk/anne yaşı, cinsiyet kompozisyonu, Beck ve antidepresan yükü, SES, DM klinik göstergeleri, ham denge, IPTW ve eksik veri görsellerini kapsar.
- **Faz II katmanı:** `phase2_f*` seti CSR Bölüm 18 ve Ek F içine gömülen keşifsel post-hoc figürleri kalıcı SVG asset olarak taşır.

## Yeniden Üretim

```bash
Rscript scripts/R/39_export_carbon_svg_figures.R
```

Bu komut `_targets` store'u ve mevcut `outputs/tables` özetlerini kullanır; ham/kimliklenebilir veri okumaz. Quarto kaynakları geçici kopyalarla render edilir ve final SVG'ler yalnız `docs/assets/figures/carbon/` altında toplanır.
