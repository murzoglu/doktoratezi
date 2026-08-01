# KISIM X — DM Klinik Alt-Analizleri

> SAP v3.0 §30–32. Yalnız DM grubu içinde (aile n = 120): **DM süresi doğal cubic spline**
> ve **tanı yaşı 3-strata** analizleri. **[KEŞİFSEL]** — DM-only klinik bağlam analizi;
> kontrol grubuyla doğrudan karşılaştırma değildir.

## Veri sınırı uyarısı

| Kovaryat | n_DM mevcut | Notlar |
|---|---:|---|
| `dm_yili` | 120 / 120 | Tam veri — birincil DM klinik kovaryat |
| `tani_yasi` | 120 / 120 | Tam veri — gelişim penceresi stratifikasyonu |
| `insulin_yontemi` | 120 / 120 | Pompa vs. çoklu doz enjeksiyon; yalnız destekleyici betimleme |

> **Kural:** Bu dosya yalnız DM-only klinik değişkenlerle çalışır. Kontrol grubunda tanı tarihi,
> hastalık süresi veya tedavi yöntemi tanımlı değildir; bu değişkenler tüm örnekleme imput edilmez
> ve DM–kontrol etkileşim kovaryatı gibi kullanılmaz.

## 1. DM Süresi Doğal Cubic Spline Modeli

### Niye spline?

DM süresi ile ebeveynlik tutumu ilişkisi **doğrusal olmayabilir**: ilk yıllarda bakım yükü ve
kaygı daha yüksek olabilir, orta dönemde aile uyumu gelişebilir, ergenliğe yaklaşırken özerklik
çatışmaları tekrar artabilir. Doğal cubic spline, bu olası bükülmeleri tek doğrusal katsayıya
zorlamadan sınar.

```r
library(splines)

run_dm_duration_spline <- function(df_family) {
  df_dm <- df_family |> filter(group_f == "DM")

  # Doğal cubic spline; knot'lar DM süresi dağılımının 25/50/75 persentilinde.
  knots <- quantile(df_dm$dm_yili, c(0.25, 0.50, 0.75), na.rm = TRUE)

  m_spline <- lm(
    embu_p_asiri_koruma_mean ~ ns(dm_yili, knots = knots) +
      scale(anne_yas) + scale(ses_latent),
    data = df_dm
  )

  m_linear <- lm(
    embu_p_asiri_koruma_mean ~ dm_yili + scale(anne_yas) + scale(ses_latent),
    data = df_dm
  )

  lrt <- anova(m_linear, m_spline)

  df_pred <- tidyr::expand_grid(
    dm_yili = seq(min(df_dm$dm_yili, na.rm = TRUE), max(df_dm$dm_yili, na.rm = TRUE), by = 0.5),
    anne_yas = mean(df_dm$anne_yas, na.rm = TRUE),
    ses_latent = mean(df_dm$ses_latent, na.rm = TRUE)
  )

  pred_mat <- predict(m_spline, newdata = df_pred, interval = "confidence")
  df_pred$pred  <- pred_mat[, "fit"]
  df_pred$ci_lo <- pred_mat[, "lwr"]
  df_pred$ci_hi <- pred_mat[, "upr"]

  plot <- ggplot(df_pred, aes(x = dm_yili, y = pred)) +
    geom_ribbon(aes(ymin = ci_lo, ymax = ci_hi), alpha = 0.30) +
    geom_line() +
    geom_vline(xintercept = knots, linetype = "dashed", color = "red") +
    labs(
      title = "DM Süresi × Aşırı Koruma (Doğal Cubic Spline)",
      x = "DM süresi (yıl)",
      y = "Aşırı Koruma (tahmin edilen ortalama)"
    ) +
    theme_minimal()

  list(spline = m_spline, linear = m_linear, lrt = lrt, knots = knots, plot = plot)
}
```

### Spline yorumu

- **LRT p < .05:** Spline modeli doğrusal modelden anlamlı biçimde daha iyi uyum sağlar →
  doğrusal olmayan ilişki olasılığı desteklenir.
- **Knot'lar:** Eğri büküm noktalarıdır; yalnız sayısal kesim olarak değil klinik dönemlerle
  (erken uyum, yerleşik rutin, ergenlik özerkliği) birlikte yorumlanır.
- **Uçlarda geniş güven bandı:** Veri yoğunluğu azaldığı için ekstrapolasyon yapılmaz; uç dönem
  bulguları temkinli raporlanır.
- **Sonuç dili:** “DM süresi ebeveynliği değiştirir” değil, “DM süresi ile ebeveynlik puanları
  arasında doğrusal olmayan örüntü gözlenmiştir” denir.

## 2. Tanı Yaşı Stratifikasyonu

### Üç kritik gelişim penceresi

| Strata | Tanı yaşı aralığı | Klinik/gelişimsel anlamı |
|---|---|---|
| Erken çocukluk | <5 yaş | Bağlanma ve bakım rutinleri ebeveyn-merkezli şekillenir |
| Okul çağı | 5–10 yaş | Akran-okul entegrasyonu ve aile dışı bakım paylaşımı belirginleşir |
| Adolesan | ≥10 yaş | Özerklik gelişimi ve sorumluluk devri öne çıkar |

```r
run_diagnosis_age_strata <- function(df_family) {
  df_dm <- df_family |>
    filter(group_f == "DM") |>
    mutate(
      diag_age_strata = cut(
        tani_yasi,
        breaks = c(0, 5, 10, 18),
        labels = c("Erken çocukluk (<5)", "Okul çağı (5-10)", "Adolesan (≥10)"),
        include.lowest = TRUE
      )
    )

  purrr::map_dfr(c("sicaklik", "asiri_koruma", "reddetme"), function(sub) {
    y_col <- paste0("embu_p_", sub, "_mean")
    fml <- as.formula(paste(y_col, "~ diag_age_strata + scale(anne_yas) + scale(ses_latent)"))
    m <- lm(fml, data = df_dm)

    aov_tab <- car::Anova(m, type = 3)
    emm <- emmeans::emmeans(m, ~ diag_age_strata)

    tibble::tibble(
      outcome = sub,
      f = aov_tab["diag_age_strata", "F value"],
      p = aov_tab["diag_age_strata", "Pr(>F)"]
    ) |>
      dplyr::bind_cols(
        as.data.frame(emm) |>
          tidyr::pivot_wider(
            names_from = diag_age_strata,
            values_from = emmean,
            names_prefix = "M_"
          )
      )
  })
}
```

### Gelişim penceresi yorumu

- **Erken çocukluk tanısı:** Bakım yönetimi daha uzun süre ebeveyn-merkezli kaldığı için aşırı
  koruma puanları daha yüksek görünebilir.
- **Okul çağı tanısı:** Akran, okul ve kardeş karşılaştırmaları daha görünür hâle gelebilir.
- **Adolesan tanısı:** Özerklik ve hastalık sorumluluğu devri nedeniyle çatışma veya reddetme
  algısı artabilir.

## Targets entegrasyonu

```r
# _targets.R KISIM X / DM-only klinik bağlam
# Mevcut karar: DM süresi spline + tanı yaşı strata; kaldırılmış klinik ölçüm hedefleri yoktur.
tar_target(dm_duration_spline,   run_dm_duration_spline(df_family_scored)),
tar_target(diagnosis_age_strata, run_diagnosis_age_strata(df_family_scored)),
tar_target(dm_clinical_table,
           format_dm_clinical(dm_duration_spline, diagnosis_age_strata),
           format = "file")
```

## Tedbir denetimi

- [ ] Analizin **DM-only** olduğu açıkça belirtildi; DM–kontrol karşılaştırması gibi yazılmadı.
- [ ] `[KEŞİFSEL]` etiketi eklendi; OSF kayıtlı doğrulayıcı hipotez gibi sunulmadı.
- [ ] Spline knot'ları dağılım-temelli ve raporlanabilir biçimde gerekçelendirildi.
- [ ] Doğrusal model ile spline modeli LRT ile karşılaştırıldı.
- [ ] Güven bandının uçlarda genişlemesi ekstrapolasyon uyarısıyla yorumlandı.
- [ ] Tanı yaşı strata hücre büyüklükleri raporlandı; küçük hücre varsa etki yönü temkinli yazıldı.
- [ ] Strata analizi, gerekirse sürekli `tani_yasi` modeliyle duyarlılık olarak karşılaştırıldı.
- [ ] DM-only klinik değişkenler tüm örnekleme imput edilmedi.

## Raporlama paragrafı (Türkçe APA 7)

> "DM grubu içinde (aile n = 120) hastalık süresi ve tanı yaşı bağlamı keşifsel olarak
> incelenmiştir. DM süresi için doğal cubic spline modeli, doğrusal modele göre ek uyum sağlayıp
> sağlamadığı LRT ile sınanmıştır (knot'lar 25/50/75 persentilde). Eğri örüntüsü, ilk yıllar,
> yerleşik rutin dönemi ve daha uzun süreli hastalık deneyimi için ayrı ayrı yorumlanmış; uç
> bölgelerde güven bandı genişlediği için ekstrapolasyondan kaçınılmıştır. Tanı yaşı
> stratifikasyonunda erken çocukluk (<5), okul çağı (5–10) ve adolesan (≥10) pencereleri
> karşılaştırılmıştır. Bu bulgular yalnız DM altkümesine ait keşifsel klinik bağlam analizleri
> olarak değerlendirilmiş, doğrulayıcı DM–kontrol grup etkisi yerine geçirilmemiştir."

## Çapraz referanslar

- DM-only DAG ve kovaryat mantığı → [`nedensellik-ve-ps.md`](nedensellik-ve-ps.md)
- Yapısal eksiklik ve DM-only değişkenlerin imputasyon sınırı → [`eksik-veri-yonetimi.md`](eksik-veri-yonetimi.md)
- Spline alternatifleri (GAM, fractional polynomial) → [`ileri-yontemler.md`](ileri-yontemler.md)
- Robustluk / yanlışlama senaryoları → [`robustluk-ve-sensitivite.md`](robustluk-ve-sensitivite.md)
