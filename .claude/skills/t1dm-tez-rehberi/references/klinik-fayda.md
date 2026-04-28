# KISIM IX — Klinik Fayda Analizleri

> SAP v3.0 §27–29. Risk skor + ROC + Decision Curve Analysis (DCA) + CART + Random Forest +
> Calibration + NRI/IDI. **[KEŞİFSEL/İLERİ FAZ]** — H1–H4 confirmatory bittikten sonra.

## Niye Klinik Fayda Analizi?

İstatistiksel anlamlılık ≠ klinik kullanılabilirlik. Bu KISIM "DM ailesinde **yüksek-risk anne**
nasıl tespit edilir?" sorusunu üç katmanda yanıtlar:
1. **Risk skoru türetme** (logistic regression)
2. **Diskriminasyon** (ROC AUC) — kim yüksek-risk?
3. **Klinik karar değeri** (DCA, NRI/IDI) — klinik müdahale eşiklerinde net fayda

> **Yüksek-risk tanımı:** Beck total ≥ 17 (Hisli orta-üstü Türk normu).

## 1. Risk Skoru Geliştirme

```r
derive_risk_score <- function(df_family) {
  df_family$high_risk <- as.integer(df_family$beck_total >= 17)

  m_risk <- glm(high_risk ~ group_f + scale(anne_yas) + scale(egitim_durumu) +
                 anne_antidepresan + scale(ses_latent) + cocuk_sayisi,
                family = binomial, data = df_family)

  df_family$risk_pred <- predict(m_risk, type = "response")

  list(model = m_risk, df = df_family)
}
```

> **Uyarı:** Outcome (Beck high_risk) bağımlı değişken; *aynı zamanda* model dışı kullanmak
> data leakage'a yol açar. Risk skoru yalnız *yüksek-risk öngörüsü* için kullanılır; mediation
> veya causal claim'lerde değil.

## 2. ROC Analizi

```r
run_roc_analysis <- function(risk_score_results, df_family) {
  library(pROC)

  roc_obj <- roc(df_family$high_risk, df_family$risk_pred,
                  ci = TRUE, ci.alpha = 0.95)

  cat(sprintf("AUC = %.3f, 95%% CI [%.3f, %.3f]\n",
                roc_obj$auc, ci(roc_obj)[1], ci(roc_obj)[3]))

  # Optimal cut-off (Youden's J = sensitivity + specificity − 1)
  coords_optimal <- coords(roc_obj, "best", best.method = "youden",
                             ret = c("threshold","sensitivity","specificity",
                                     "ppv","npv"))

  png(file.path(OUTPUT_DIR, "figures", "roc_curve.png"),
       width = 1000, height = 1000, res = 150)
  plot(roc_obj, print.auc = TRUE, ci = TRUE,
        main = "ROC: Yüksek-Risk Anne Tahmini")
  dev.off()

  list(roc = roc_obj, auc = roc_obj$auc, optimal = coords_optimal)
}
```

### AUC yorum eşikleri (Hosmer & Lemeshow)

| AUC | Yorum |
|---|---|
| < .60 | Pratik olarak kullanılmaz |
| .60–.70 | Zayıf |
| .70–.80 | Kabul edilebilir |
| .80–.90 | İyi |
| > .90 | Mükemmel (overfitting şüphesi!) |

## 3. Decision Curve Analysis (Vickers & Elkin 2006)

ROC tek başına klinik kullanılabilirliği ölçmez. **DCA**: belirli risk eşiklerinde **net benefit**.

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

### DCA yorumu

```
Net Benefit (NB) eğrisi 'treat all' ve 'treat none' referans çizgilerinin üzerindeyse model
klinik faydalı.

Örn. p=0.20 eşiğinde NB = 0.10 →
  Her 100 anneden 10'u doğru risk yüksek tespit ediliyor
  (yanlış pozitif maliyeti hesaplanmış).

Threshold karar matrisi:
  threshold < .10  → "tüm anneleri tara" stratejisi yeterli; modele gerek yok
  threshold .10-.30 → model belirgin avantaj
  threshold > .30  → eğri 'treat none'a yakın; klinik kullanım sınırlı
```

## 4. CART Karar Ağacı

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

> **Pruning kuralı:** `printcp()` çıktısında `xerror + xstd` minimumun bir SE içindeki en küçük
> ağacı seç (1-SE rule, Breiman et al. 1984).

## 5. Random Forest — Variable Importance

```r
run_random_forest_importance <- function(df_family) {
  library(randomForest)

  rf_data <- df_family |>
    select(beck_total, group_f, anne_yas, egitim_durumu, es_egitim_durumu,
            cocuk_sayisi, anne_antidepresan, ses_latent, age_gap) |>
    drop_na()

  rf <- randomForest(beck_total ~ ., data = rf_data,
                       ntree = 5000, importance = TRUE)

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

### Importance metrik seçimi

| `type` | Metrik | Yorum |
|---|---|---|
| 1 | **%IncMSE** (permutation) | Daha güvenilir; varsayım hafif |
| 2 | IncNodePurity | Bias var; bağımlı kategorik prediktörlerde sorun |

## 6. Calibration + NRI/IDI

### Calibration (Harrell 2015)

Model ne kadar iyi diskrimine ediyor (AUC) yetmez; **gerçek olasılıkları tahmin ediyor mu**?

```r
run_calibration_analysis <- function(risk_score_results, df_family) {
  library(rms)

  cal <- calibrate(risk_score_results$model, B = 1000, method = "boot")

  png(file.path(OUTPUT_DIR, "figures", "calibration_plot.png"),
       width = 1000, height = 1000, res = 150)
  plot(cal, main = "Calibration: Bootstrap-corrected (B=1000)")
  dev.off()

  library(ResourceSelection)
  hl_test <- hoslem.test(df_family$high_risk, df_family$risk_pred, g = 10)

  list(calibration = cal, hl_test = hl_test)
}
```

> **Hosmer-Lemeshow eleştirisi:** Test düşük güçlü ve grup-sayısına bağımlı. Calibration plot
> görsel doğrulama daha güvenilir; HL test sadece *destekleyici* metriktir.

### NRI/IDI (Pencina 2008)

Yeni bir belirteç eklemenin **marjinal** faydası:

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

### NRI/IDI yorum

| Metrik | Anlamı | Eşik |
|---|---|---|
| **NRI** | Net doğru-yeniden sınıflanma oranı (hasta + sağlıklı) | > 0.20 anlamlı klinik fayda |
| **IDI** | Diskriminasyon iyileşmesi (sürekli) | > 0.05 anlamlı |
| **cfNRI** (cont) | Kategorisiz NRI alternatifi | Daha kararlı |

> **Uyarı (Pepe et al. 2014):** NRI istatistiksel olarak yanıltıcı olabilir (CI hesabı standart
> hatadan etkilenir). Tezde NRI + cfNRI **birlikte** raporlanır.

## Targets entegrasyonu

```r
# _targets.R'ye eklenecek (KISIM IX gelecek faz)
tar_target(risk_score_model,       derive_risk_score(df_family_scored)),
tar_target(roc_analysis,           run_roc_analysis(risk_score_model, df_family_scored)),
tar_target(decision_curve,         run_decision_curve_analysis(risk_score_model, df_family_scored)),
tar_target(cart_tree,              run_decision_tree(df_family_scored)),
tar_target(rf_importance,          run_random_forest_importance(df_family_scored)),
tar_target(calibration_results,    run_calibration_analysis(risk_score_model, df_family_scored)),
tar_target(clinical_utility_table,
            format_clinical_utility(roc_analysis, decision_curve, calibration_results),
            format = "file")
```

## Tedbir denetimi

- [ ] **Out-of-sample validation:** Bootstrap (.632+) veya 10-fold CV ile AUC overfitting kontrol
- [ ] DCA threshold range klinik anlamlı (0.05–0.50)
- [ ] CART için 1-SE pruning rule uygulandı
- [ ] Random Forest %IncMSE (permutation), tip 2 değil
- [ ] Calibration plot + HL test birlikte
- [ ] NRI + cfNRI (sürekli alternatif) birlikte raporlandı
- [ ] Risk skoru *müdahale önerisi olarak değil* keşifsel filtre olarak yorumlandı
- [ ] Sample size: AUC için n_event ≥ 100 (487 × prevalans → kontrol et)
- [ ] [KEŞİFSEL] etiketi (KISIM IX ileri faz)

## Raporlama paragrafı (Türkçe APA 7)

> "Yüksek riskli anne (Beck total ≥ 17) tahmini için lojistik regresyon temelli risk skoru
> türetilmiştir. Demografik (yaş, eğitim) ve psikososyal (antidepresan kullanımı, SES latent)
> belirteçler içeren modelin AUC = .78 (%95 GA [.72, .84]) olarak hesaplanmıştır; bu Hosmer ve
> Lemeshow (2013) kabul edilebilir aralıkta yer alır. Vickers ve Elkin (2006) decision curve
> analizinde model 'treat all' ve 'treat none' stratejilerine göre 0.10–0.30 risk eşiğinde anlamlı
> net fayda göstermiştir. NRI = .24 (95% bootstrap CI [.12, .36]) anne ruh sağlığı belirteçlerinin
> demografik temele eklenmesinin marjinal sınıflandırma iyileştirmesi sağladığını göstermiştir.
> Calibration eğrisi (bootstrap-corrected, B = 1000) intercept = -0.04, slope = 1.06 ile
> kabul edilebilir kalibrasyon göstermektedir. Bu bulgular **keşifsel** statüdedir ve dış
> validasyon gerektirmektedir."

## Çapraz referanslar

- Logistic regression diagnostics → [`tedbir-ve-hatalar.md`](tedbir-ve-hatalar.md)
- LPA tipoloji + risk skoru entegrasyonu → [`latent-degisken-yontemleri.md`](latent-degisken-yontemleri.md)
- Calibration için Bayesian alternatifler → [`bayesci-paralel-hat.md`](bayesci-paralel-hat.md)
- Kaynaklar: Vickers & Elkin (2006); Pencina et al. (2008); Harrell (2015); Hosmer & Lemeshow (2013); Pepe et al. (2014)
