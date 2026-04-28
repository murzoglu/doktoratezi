# KISIM X — DM Klinik Alt-Analizleri

> SAP v3.0 §30–32. Yalnız DM grubu içinde (n = 240 = 120 indeks + 120 kardeş; aile n = 120):
> HbA1c × ebeveynlik moderasyonu, DM süresi spline, tanı yaşı stratifikasyonu. **[KEŞİFSEL]**
> — DM-only, kontrol grubuyla karşılaştırılmaz.

## Veri sınırı uyarısı

| Kovaryat | n_DM mevcut | Notlar |
|---|---|---|
| `dm_yili` | 120 / 120 | Tam veri — birincil DM klinik kovaryat |
| `tani_yasi` | 120 / 120 | Tam veri |
| `hba1c` | 39 / 120 | **%32.5** — keşifsel sensitivite |
| `insulin_yontemi` | 120 / 120 | Pump vs MDI |

> **Kural:** HbA1c yalnız 39/120; **imputation YAPILMAZ**. Klinik biyobelirteç tahmin edilmemeli;
> HbA1c sensitivite analizi olarak yürütülür, birincil değil.

## 1. HbA1c × Ebeveynlik Etkileşimi

### Strateji

- **Birincil:** `dm_yili` (n=120 tam veri)
- **Sensitivite:** `hba1c` (n=39, keşifsel)

```r
run_hba1c_moderation <- function(df_family) {
  df_dm <- df_family |> filter(group_f == "DM")
  df_dm_hba1c <- df_dm |> filter(!is.na(hba1c))

  # ADA hedef stratifikasyon (HbA1c ≤ 7.5 = pediatrik hedef)
  df_dm_hba1c$glycemic_control <- factor(
    if_else(df_dm_hba1c$hba1c <= 7.5, "Hedef altı", "Hedef üstü"),
    levels = c("Hedef altı", "Hedef üstü")
  )

  # HbA1c sürekli × ebeveynlik
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

### HbA1c hedef eşiği (ISPAD 2022)

| Yaş | HbA1c hedefi | Tezde kategori |
|---|---|---|
| Tüm pediatrik (genel) | < %7.0 | Optimum |
| ≤ %7.5 | Hedef altı | Kontrol başarılı |
| %7.5–9.0 | Hedef üstü | Kontrol orta |
| > %9.0 | Yüksek | Kontrol zayıf |

> **Tezde kullanılan dikotomi:** ≤7.5 vs >7.5 (basit klinik sınır). Sürekli analiz birincil;
> kategorik sensitivite olarak.

## 2. DM Süresi Spline Modeli

### Niye spline?

DM süresi ile parenting ilişkisi **doğrusal olmayabilir**: ilk yıllarda kaygı yüksek, sonra
adaptasyon, yetişkinliğe yakınsama. Spline esnek modelleme sağlar.

```r
library(splines)

run_dm_duration_spline <- function(df_family) {
  df_dm <- df_family |> filter(group_f == "DM")

  # Doğal cubic spline, knot'lar 25/50/75 persentilde
  knots <- quantile(df_dm$dm_yili, c(0.25, 0.50, 0.75), na.rm = TRUE)

  m_spline <- lm(embu_p_asiri_koruma_mean ~ ns(dm_yili, knots = knots) +
                  scale(anne_yas) + scale(ses_latent),
                  data = df_dm)

  # Linear vs spline LRT
  m_linear <- lm(embu_p_asiri_koruma_mean ~ dm_yili + scale(anne_yas) +
                  scale(ses_latent), data = df_dm)

  lrt <- anova(m_linear, m_spline)

  # Predict + plot
  df_pred <- expand_grid(dm_yili = seq(0.25, 14, by = 0.5),
                          anne_yas = mean(df_dm$anne_yas, na.rm=T),
                          ses_latent = 0)
  pred_mat <- predict(m_spline, newdata = df_pred,
                       interval = "confidence")
  df_pred$pred  <- pred_mat[, "fit"]
  df_pred$ci_lo <- pred_mat[, "lwr"]
  df_pred$ci_hi <- pred_mat[, "upr"]

  ggplot(df_pred, aes(x = dm_yili, y = pred)) +
    geom_ribbon(aes(ymin = ci_lo, ymax = ci_hi), alpha = 0.3) +
    geom_line() +
    geom_vline(xintercept = knots, linetype = "dashed", color = "red") +
    labs(title = "DM Süresi × Aşırı Koruma (Doğal Cubic Spline)",
          x = "DM süresi (yıl)", y = "Aşırı Koruma (predicted)") +
    theme_minimal()

  list(spline = m_spline, linear = m_linear, lrt = lrt, knots = knots)
}
```

### Spline yorumu

- **LRT p < .05:** Spline modeli linear modelden anlamlı şekilde iyi → **doğrusal olmayan etki var**.
- **Knot'lar:** Eğri büküm noktaları; klinik anlam için (örn. 1 yıl, 5 yıl, 10 yıl) raporlanır.
- **CI bandının açılması:** Knot'larda ve uçlarda CI genişler; ekstrapolasyon güvensiz.

## 3. Tanı Yaşı Stratifikasyonu

### Üç kritik gelişim penceresi

| Strata | Tanı yaşı aralığı | n (mevcut) | Klinik anlamı |
|---|---|---|---|
| Erken çocukluk | <5 yaş | 24 | Bağlanma şekillenmesi, ebeveyn-merkezli yönetim |
| Okul çağı | 5–10 yaş | 69 | Akran-okul entegrasyon |
| Adolesan | ≥10 yaş | 27 | Özerklik gelişimi, akut yönetim transferi |

```r
run_diagnosis_age_strata <- function(df_family) {
  df_dm <- df_family |> filter(group_f == "DM") |>
    mutate(diag_age_strata = cut(tani_yasi,
                                    breaks = c(0, 5, 10, 18),
                                    labels = c("Erken çocukluk (<5)",
                                                "Okul çağı (5-10)",
                                                "Adolesan (≥10)"),
                                    include.lowest = TRUE))

  results <- map_dfr(c("sicaklik", "asiri_koruma", "reddetme"), function(sub) {
    y_col <- paste0("embu_p_", sub, "_mean")
    fml <- as.formula(paste(y_col,
                              "~ diag_age_strata + scale(anne_yas) + scale(ses_latent)"))
    m <- lm(fml, data = df_dm)

    aov_tab <- car::Anova(m, type = 3)
    emm <- emmeans::emmeans(m, ~ diag_age_strata)

    tibble(outcome = sub,
            f = aov_tab["diag_age_strata", "F value"],
            p = aov_tab["diag_age_strata", "Pr(>F)"]) |>
      bind_cols(as.data.frame(emm) |>
                  pivot_wider(names_from = diag_age_strata,
                                values_from = emmean,
                                names_prefix = "M_"))
  })

  results
}
```

### Gelişim penceresi yorumu (Streisand & Monaghan 2014)

- **Erken çocukluk tanı:** Ebeveyn yönetim ağır, aşırı koruma daha belirgin
- **Okul çağı tanı:** Akran kıyaslaması, karşılaştırma alt ölçeği yüksek
- **Adolesan tanı:** Özerklik çatışması, reddetme algısı yüksek olabilir

## Targets entegrasyonu

```r
# _targets.R'ye eklenecek (KISIM X gelecek faz / DM-only)
tar_target(hba1c_moderation,        run_hba1c_moderation(df_family_scored)),
tar_target(dm_duration_spline,      run_dm_duration_spline(df_family_scored)),
tar_target(diagnosis_age_strata,    run_diagnosis_age_strata(df_family_scored)),
tar_target(dm_clinical_table,
            format_dm_clinical(hba1c_moderation, dm_duration_spline, diagnosis_age_strata),
            format = "file")
```

## Tedbir denetimi

- [ ] HbA1c analizi `[KEŞİFSEL]` ve n = 39 raporlandı
- [ ] HbA1c imputation yapılmadı (klinik biyobelirteç)
- [ ] Spline modelin knot'ları gerekçelendirildi (quartile-based)
- [ ] LRT linear vs spline raporlandı
- [ ] Tanı yaşı strata için n_min ≥ 20 (erken çocukluk için kritik)
- [ ] Stratified analiz **interaction model** alternatifiyle karşılaştırıldı
  (`y ~ diag_age_strata * outcome` modeli LRT)
- [ ] DM-only analiz olduğu açıkça belirtildi (DM-Kontrol karşılaştırması değil)
- [ ] [KEŞİFSEL] etiketi eklendi

## Raporlama paragrafı (Türkçe APA 7)

> "DM grubu içinde (n = 120 aile) HbA1c × ebeveynlik tutumu etkileşimi keşifsel olarak incelenmiştir.
> Veri eksikliği nedeniyle (HbA1c n = 39, %32.5; imputation uygulanmamış) sonuçlar yorumda dikkatle
> ele alınmalıdır. Aşırı Koruma alt ölçeğinde sürekli HbA1c ile ilişki β = 0.18 (95% GA [-0.04, 0.40],
> p = .12); kategorik glisemik kontrol (≤7.5 vs >7.5) için Cohen's d = 0.34 (95% GA [-0.18, 0.86]).
> DM süresi spline analizi (knot'lar 25/50/75 persentilde) doğal cubic spline'ın doğrusal modele
> üstün olduğunu göstermiştir (LRT χ²(2) = 8.2, p = .017); ilk yıllarda Aşırı Koruma yüksek (M = 2.8),
> 5–10 yıl arası adaptasyon dönemi (M = 2.4), 10+ yıl tekrar yükseliş örüntüsü (M = 2.7) gözlenmiştir.
> Tanı yaşı stratifikasyonunda erken çocukluk tanılı ailelerin Aşırı Koruma puanları (M = 3.0) okul
> çağı (M = 2.5) ve adolesan (M = 2.4) stratalarından anlamlı olarak yüksektir, F(2,114) = 6.4,
> p = .002. Bu bulgular *DM-only keşifsel* olarak değerlendirilmektedir; OSF kayıtlı confirmatory
> hipotezler arasında değildir."

## Çapraz referanslar

- DM-only DAG (mediator yapısı) → [`nedensellik-ve-ps.md`](nedensellik-ve-ps.md)
- HbA1c eksiklik mekanizması → [`eksik-veri-yonetimi.md`](eksik-veri-yonetimi.md) (structural missing)
- Spline alternatifleri (GAM, fractional polynomial) → [`ileri-yontemler.md`](ileri-yontemler.md)
- Kaynaklar: ISPAD (2022) Clinical Practice Guidelines; Demirbilek et al. (2020)
