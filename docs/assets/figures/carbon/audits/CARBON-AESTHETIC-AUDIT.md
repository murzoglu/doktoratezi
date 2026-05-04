# Carbon Charts Estetik Audit

Üretim zamanı: `2026-05-01 15:48:49 UTC`

Bu audit, `docs/assets/figures/carbon/` altındaki 52 SVG'nin IBM Carbon Charts estetik ilkelerine göre yeniden taranmış durumunu verir. Referans zinciri: Carbon Charts repo `packages/core/scss` uygulama stilleri, yerel Figma source-of-truth Carbon Charts Library envanteri ve Carbon HTML Report chart palette referansı.

Kaynaklar: resmi Carbon Charts repo (`carbon-design-system/carbon-charts`, `packages/core/scss/_type.scss`, `_color-palette.scss`, `components/_axis.scss`, `components/_grid.scss`, `components/_legend.scss`, `components/_title.scss`), Carbon data visualization chart anatomy, axes/labels ve legends rehberleri.

## Kullanılan Estetik Kriterler

| Kriter | Uygulanan karar | Kaynak rolü |
|---|---|---|
| Typography | IBM Plex Sans; chart metinleri 12px eşdeğeri, başlık 16px eşdeğeri semibold | Carbon Charts `_type.scss`, `_title.scss`; Figma Carbon Type Sets |
| Başlık | Dekoratif mavi yerine `text-primary` siyah/semibold | Carbon Charts title component |
| Eksenler | Axis title semibold `text-primary`; tick labels `text-secondary`; tick çizgileri kapalı | Carbon Charts `_axis.scss` |
| Grid | Major grid `layer-accent-01` / `#e0e0e0`; minor grid yok | Carbon Charts `_grid.scss` |
| Legend | Varsayılan bottom; 12px label; tek seri/uygun boşlukta doğrudan etiket tercih edilir | Carbon data visualization legend guidance |
| Palet | Resmi `@carbon/charts` white-theme 14 seri paleti; sequential/semantic istisnalar korunur | Carbon Charts `_color-palette.scss` |
| SVG provenance | Her SVG `data-carbon-style`, `data-carbon-charts-source`, `data-font`, `data-chart-palette` metadata taşır | Repro/audit gereği |

## Toplu Sonuç

- SVG sayısı: **52**
- Carbon Charts estetik PASS: **52**
- Raster/gradient istisnası notlanan: **4**
- Review gereken: **0**
- Maksimum non-Carbon hex sayısı: **0**

## Figür Bazlı Audit Matrisi

| ID | SVG | Estetik durum | Chart palette hit | Text primary / secondary hit | Grid hit | Non-Carbon hex / rgb | Not |
|---|---|---|---:|---:|---:|---:|---|
| strobe_flow | [fig-01-strobe-flow.svg](primary/fig-01-strobe-flow.svg) | PASS: Carbon Charts | 0 | 0 / 0 | 0 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| causal_dag | [fig-02-causal-dag.svg](primary/fig-02-causal-dag.svg) | PASS: Carbon Charts | 0 | 0 / 0 | 0 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| smd_love_plot | [fig-03-smd-love-plot.svg](primary/fig-03-smd-love-plot.svg) | PASS: Carbon Charts | 8 | 2 / 13 | 9 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| propensity_overlap | [fig-04-propensity-overlap.svg](primary/fig-04-propensity-overlap.svg) | PASS: Carbon Charts | 123 | 4 / 135 | 8 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| ses_correlation_heatmap | [fig-05-ses-correlation-heatmap.svg](primary/fig-05-ses-correlation-heatmap.svg) | PASS: Carbon Charts; raster/gradient istisnası notlandı | 0 | 38 / 18 | 12 | 0 / 14 | Gradient/raster veya interpolasyon rengi içerir; SVG native kalır. |
| missing_pattern_primary | [fig-06-missing-pattern-primary.svg](primary/fig-06-missing-pattern-primary.svg) | PASS: Carbon Charts; raster/gradient istisnası notlandı | 0 | 2 / 47 | 43 | 0 / 1 | Gradient/raster veya interpolasyon rengi içerir; SVG native kalır. |
| h1_forest | [fig-07-h1-forest.svg](primary/fig-07-h1-forest.svg) | PASS: Carbon Charts | 23 | 3 / 11 | 7 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| h1_three_way_emm | [fig-08-h1-three-way-emm.svg](primary/fig-08-h1-three-way-emm.svg) | PASS: Carbon Charts | 67 | 10 / 27 | 70 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| h2_apim_path | [fig-09-h2-apim-path.svg](primary/fig-09-h2-apim-path.svg) | PASS: Carbon Charts | 0 | 0 / 0 | 0 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| h3_stratified_forest | [fig-10-h3-stratified-forest.svg](primary/fig-10-h3-stratified-forest.svg) | PASS: Carbon Charts | 46 | 6 / 15 | 8 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| h4_sem_path | [fig-11-h4-sem-path.svg](primary/fig-11-h4-sem-path.svg) | PASS: Carbon Charts | 0 | 0 / 0 | 0 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| h5_ba_grid | [fig-12-h5-ba-grid.svg](primary/fig-12-h5-ba-grid.svg) | PASS: Carbon Charts | 0 | 11 / 27 | 91 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| h5_rsa_surface | [fig-13-h5-rsa-surface.svg](primary/fig-13-h5-rsa-surface.svg) | PASS: Carbon Charts; raster/gradient istisnası notlandı | 0 | 16 / 26 | 53 | 0 / 481 | Gradient/raster veya interpolasyon rengi içerir; SVG native kalır. |
| mediation_effects | [fig-14-mediation-effects.svg](primary/fig-14-mediation-effects.svg) | PASS: Carbon Charts | 0 | 5 / 22 | 34 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| lpa_fit_indices | [fig-15-lpa-fit-indices.svg](primary/fig-15-lpa-fit-indices.svg) | PASS: Carbon Charts | 0 | 5 / 22 | 31 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| network_graph | [fig-16-network-graph.svg](primary/fig-16-network-graph.svg) | PASS: Carbon Charts | 0 | 0 / 0 | 0 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| network_nct | [fig-17-network-nct.svg](primary/fig-17-network-nct.svg) | PASS: Carbon Charts | 0 | 2 / 8 | 7 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| clinical_roc | [fig-18-clinical-roc.svg](primary/fig-18-clinical-roc.svg) | PASS: Carbon Charts | 0 | 4 / 13 | 10 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| clinical_dca | [fig-19-clinical-dca.svg](primary/fig-19-clinical-dca.svg) | PASS: Carbon Charts | 0 | 3 / 12 | 8 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| clinical_calibration | [fig-20-clinical-calibration.svg](primary/fig-20-clinical-calibration.svg) | PASS: Carbon Charts | 0 | 4 / 16 | 10 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| clinical_cart_rf | [fig-21-clinical-cart-rf.svg](primary/fig-21-clinical-cart-rf.svg) | PASS: Carbon Charts | 0 | 21 / 23 | 24 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| specification_curve | [fig-22-specification-curve.svg](primary/fig-22-specification-curve.svg) | PASS: Carbon Charts | 0 | 8 / 26 | 36 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| sensemakr_contour | [fig-23-sensemakr-contour.svg](primary/fig-23-sensemakr-contour.svg) | PASS: Carbon Charts; raster/gradient istisnası notlandı | 0 | 7 / 21 | 8 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| bayesian_forest | [fig-24-bayesian-forest.svg](primary/fig-24-bayesian-forest.svg) | PASS: Carbon Charts | 0 | 5 / 13 | 18 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| bayesian_diagnostics | [fig-25-bayesian-diagnostics.svg](primary/fig-25-bayesian-diagnostics.svg) | PASS: Carbon Charts | 15 | 3 / 12 | 9 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| reliability | [psychval-01-reliability.svg](psychometric/psychval-01-reliability.svg) | PASS: Carbon Charts | 20 | 2 / 14 | 10 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| floor | [psychval-02-floor.svg](psychometric/psychval-02-floor.svg) | PASS: Carbon Charts | 136 | 2 / 25 | 40 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| cfa | [psychval-03-cfa.svg](psychometric/psychval-03-cfa.svg) | PASS: Carbon Charts | 48 | 3 / 18 | 24 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| invariance | [psychval-04-invariance.svg](psychometric/psychval-04-invariance.svg) | PASS: Carbon Charts | 9 | 0 / 11 | 10 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| icc | [psychval-05-icc.svg](psychometric/psychval-05-icc.svg) | PASS: Carbon Charts | 10 | 0 / 8 | 4 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| validity | [psychval-06-validity.svg](psychometric/psychval-06-validity.svg) | PASS: Carbon Charts | 18 | 0 / 17 | 17 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| multiverse | [psychval-07-multiverse.svg](psychometric/psychval-07-multiverse.svg) | PASS: Carbon Charts | 20 | 0 / 8 | 4 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| grup-dagilim | [demo-01-grup-dagilim.svg](demographic/demo-01-grup-dagilim.svg) | PASS: Carbon Charts | 2 | 0 / 5 | 5 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| cocuk-yas-dagilim | [demo-02-cocuk-yas-dagilim.svg](demographic/demo-02-cocuk-yas-dagilim.svg) | PASS: Carbon Charts | 8 | 0 / 16 | 16 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| cinsiyet-grup | [demo-03-cinsiyet-grup.svg](demographic/demo-03-cinsiyet-grup.svg) | PASS: Carbon Charts | 10 | 2 / 9 | 14 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| same-sex | [demo-04-same-sex.svg](demographic/demo-04-same-sex.svg) | PASS: Carbon Charts | 6 | 0 / 7 | 7 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| aile-buyuklugu | [demo-05-aile-buyuklugu.svg](demographic/demo-05-aile-buyuklugu.svg) | PASS: Carbon Charts | 14 | 0 / 13 | 13 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| anne-yas | [demo-06-anne-yas.svg](demographic/demo-06-anne-yas.svg) | PASS: Carbon Charts | 2 | 0 / 7 | 7 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| beck-grup | [demo-07-beck-grup.svg](demographic/demo-07-beck-grup.svg) | PASS: Carbon Charts | 36 | 0 / 15 | 9 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| beck-severity | [demo-08-beck-severity.svg](demographic/demo-08-beck-severity.svg) | PASS: Carbon Charts | 12 | 0 / 10 | 10 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| antidep | [demo-09-antidep.svg](demographic/demo-09-antidep.svg) | PASS: Carbon Charts | 3 | 0 / 7 | 7 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| ses-density | [demo-10-ses-density.svg](demographic/demo-10-ses-density.svg) | PASS: Carbon Charts | 4 | 0 / 11 | 11 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| egitim | [demo-11-egitim.svg](demographic/demo-11-egitim.svg) | PASS: Carbon Charts | 25 | 2 / 14 | 20 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| dm-eksik | [demo-12-dm-eksik.svg](demographic/demo-12-dm-eksik.svg) | PASS: Carbon Charts | 5 | 0 / 10 | 5 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| hba1c | [demo-13-hba1c.svg](demographic/demo-13-hba1c.svg) | PASS: Carbon Charts | 15 | 0 / 9 | 9 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| hba1c-target | [demo-14-hba1c-target.svg](demographic/demo-14-hba1c-target.svg) | PASS: Carbon Charts | 3 | 0 / 8 | 8 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| dm-suresi | [demo-15-dm-suresi.svg](demographic/demo-15-dm-suresi.svg) | PASS: Carbon Charts | 31 | 0 / 16 | 16 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| tani-strata | [demo-16-tani-strata.svg](demographic/demo-16-tani-strata.svg) | PASS: Carbon Charts | 3 | 0 / 8 | 8 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| smd-love | [demo-17-smd-love.svg](demographic/demo-17-smd-love.svg) | PASS: Carbon Charts | 66 | 0 / 21 | 21 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| ps-density | [demo-18-ps-density.svg](demographic/demo-18-ps-density.svg) | PASS: Carbon Charts | 4 | 0 / 8 | 8 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| iptw-balance | [demo-19-iptw-balance.svg](demographic/demo-19-iptw-balance.svg) | PASS: Carbon Charts | 16 | 0 / 9 | 9 | 0 / 0 | Token/palette uyumlu vektör renkleri. |
| eksik-degisken | [demo-20-eksik-degisken.svg](demographic/demo-20-eksik-degisken.svg) | PASS: Carbon Charts | 8 | 0 / 10 | 10 | 0 / 0 | Token/palette uyumlu vektör renkleri. |

## Yorum

- `non_carbon_rgb_count`, SVG içinde raster/interpolasyon üreten heatmap, density, contour veya antialias geçişlerinde sıfırdan büyük olabilir. Bu durum, kaynak grafiğin continuous scale veya raster-like geom kullanmasından gelir; SVG wrapper'a düşürülmüş PNG değildir.
- Chart palette hit sayısı, resmi Carbon Charts kategorik paletinin veri işaretleri içinde ne kadar kullanıldığını gösterir. Tek seri veya semantic status grafikleri doğal olarak daha düşük hit sayısına sahip olabilir.
- `text_primary`, `text_secondary` ve `grid` hitleri, Carbon Charts'ın başlık/axis/grid rollerinin SVG içinde gerçekten üretildiğini gösteren mekanik sinyallerdir.
