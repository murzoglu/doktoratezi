# KISIM VII — Latent Değişken Yöntemleri

> SAP v3.0 §21–23. Üç katman: **LPA** (sürekli göstergeler, anne tipoloji), **LCA + Mixture Regression**
> (kategorik göstergeler), **Bifactor S-1** (genel + spesifik faktör ayrımı). Tümü **[KEŞİFSEL]** —
> H1–H4 confirmatory bittikten sonra yorumlanır.

## Niye Latent Değişken Yaklaşımı?

Klasik regresyon "ortalama" anneyi modeller. Ama T1DM aileleri **homojen değil**: bazıları
"tükenmiş", bazıları "aşırı koruyucu", bazıları "adapte". Tipoloji çıkarmak → klinik müdahale
hedeflemesi.

> **Kural:** LPA/LCA "data-driven" yöntemlerdir; ön-kayıt OSF (`pytfe`) kapsamında *değildir*.
> Bulgular `[KEŞİFSEL]` etiketiyle raporlanır. Replikasyonu önerilir.

## 1. Latent Profile Analysis (LPA) — Anne Tipoloji

### Mantık

Lanza & Cooper (2016) — sürekli göstergelerden örtük profil çıkarımı. T1DM tezinde anneleri
**Beck × EMBU-P × SES × DM-status** üzerinden gruplamak.

```r
run_lpa_mother_typology <- function(df_family) {
  library(tidyLPA); library(mclust)

  lpa_indicators <- df_family |>
    select(beck_total,
           embu_p_sicaklik_mean, embu_p_asiri_koruma_mean,
           embu_p_reddetme_mean, embu_p_karsilastirma_mean,
           ses_latent) |>
    drop_na() |>
    scale() |>
    as.data.frame()

  # 1-6 profil karşılaştırması — Akogul & Erisoglu (2017)
  lpa_comparison <- lpa_indicators |>
    estimate_profiles(1:6,
                       variances = c("equal", "varying"),
                       covariances = c("zero", "equal", "varying"))

  comparison_summary <- compare_solutions(lpa_comparison)

  # En uygun model (BIC minimum + entropy > .80 + LMR-LRT p < .05)
  best_model <- estimate_profiles(lpa_indicators, n_profiles = 4,
                                    variances = "equal", covariances = "zero")

  df_family$lpa_class <- get_data(best_model)$Class

  # Profil özetleri
  profile_means <- df_family |>
    group_by(lpa_class) |>
    summarise(
      n = n(), pct = round(n()/nrow(df_family)*100, 1),
      beck_M    = mean(beck_total, na.rm=T),
      sicaklik  = mean(embu_p_sicaklik_mean, na.rm=T),
      asiri_kor = mean(embu_p_asiri_koruma_mean, na.rm=T),
      reddetme  = mean(embu_p_reddetme_mean, na.rm=T),
      ses       = mean(ses_latent, na.rm=T),
      pct_dm    = round(mean(group_f == "DM") * 100, 1)
    )

  # Profile × DM/Kontrol
  lpa_chi <- chisq.test(table(df_family$lpa_class, df_family$group_f))

  list(comparison = comparison_summary,
        selected = best_model,
        profile_means = profile_means,
        df_with_class = df_family,
        chi_test = lpa_chi)
}
```

### Profil seçim kriterleri

| Metrik | İdeal | Alt sınır |
|---|---|---|
| **BIC** | Lokal minimum | — |
| **Entropy** | > .80 | > .60 |
| **LMR-LRT p** | < .05 (k vs k−1) | — |
| **Smallest class** | > 5% | > 1% (klinik anlam ister) |
| **BLRT** | < .05 | — |

### Beklenen profiller (apriori — T1DM aile literatürü)

| Profile | Beck | Sıcaklık | Aşırı Koruma | Reddetme | DM yoğunluğu |
|---|---|---|---|---|---|
| **Adapte ebeveyn** | Düşük | Yüksek | Orta | Düşük | Eşit dağılım |
| **Aşırı koruyucu** | Orta | Yüksek | **Çok yüksek** | Düşük | DM lehine |
| **Tükenmiş** | **Yüksek** | Düşük | Orta | Yüksek | DM lehine |
| **Standart** | Düşük | Orta | Düşük | Düşük | Kontrol lehine |

### Yorum şablonu

> "Anne tipolojisi LPA çözümünde 4 profil çıkmıştır (BIC = 3148, entropy = .82, LMR-LRT p = .003).
> Profil 1 'Adapte' (n = 78, %32), Profil 2 'Aşırı Koruyucu' (n = 64, %27), Profil 3 'Tükenmiş'
> (n = 49, %20), Profil 4 'Standart' (n = 50, %21) olarak adlandırılmıştır. Tükenmiş profilde
> DM-Kontrol oranı %71 vs %29 (χ²(3) = 18.4, p < .001), Cramér's V = .28 — orta etki büyüklüğü."

## 2. Latent Class Analysis (LCA)

Kategorik göstergeler için (Beck şiddet kategorileri, ebeveynlik tutum medyan-bölünmüş):

```r
run_lca_categorical <- function(df_family) {
  library(poLCA)

  df_lca <- df_family |>
    mutate(
      beck_high      = as.integer(beck_total >= 17),
      sicaklik_high  = as.integer(embu_p_sicaklik_mean > median(embu_p_sicaklik_mean, na.rm=T)),
      asiri_kor_high = as.integer(embu_p_asiri_koruma_mean > median(embu_p_asiri_koruma_mean, na.rm=T)),
      reddetme_high  = as.integer(embu_p_reddetme_mean > median(embu_p_reddetme_mean, na.rm=T)),
      ad_use         = as.integer(anne_antidepresan)
    ) |>
    select(beck_high, sicaklik_high, asiri_kor_high, reddetme_high, ad_use)

  lca_results <- map(2:5, function(k) {
    f <- cbind(beck_high, sicaklik_high, asiri_kor_high, reddetme_high, ad_use) ~ 1
    poLCA(f,
           data = df_lca |> mutate(across(everything(), ~as.factor(.x + 1))),
           nclass = k, nrep = 50, verbose = FALSE)
  })

  bic_table <- map_dfr(lca_results, function(m) {
    tibble(nclass = m$N, BIC = m$bic, AIC = m$aic, LL = m$llik)
  })

  list(models = lca_results, bic_table = bic_table)
}
```

> **Median split eleştirisi:** Klasik istatistikte sürekli değişkeni median ile ikiye bölmek bilgi
> kaybeder (MacCallum et al. 2002). Burada *sadece* LCA için yapılır; primer analiz hep sürekli
> halde tutulur. Median split alternatifi: önceden tanımlanmış klinik eşikler (Beck ≥17, EMBU-P
> üst-quartile vs alt-quartile).

## 3. Mixture Regression — Group-Specific Effects

Beck → EMBU-P ilişkisi gizli sınıflara göre değişiyor mu?

```r
library(flexmix)

mix_reg <- flexmix(embu_p_reddetme_mean ~ beck_total + scale(ses_latent),
                    data = df_family, k = 2)

summary(mix_reg)  # 2-component karışımın bileşen başına regresyon parametreleri
```

**Yorum:** Bir komponentte Beck → EMBU-P **güçlü pozitif** (β = 0.48), diğerinde **sıfıra yakın**
(β = 0.08) çıkarsa → "depresyon-driven parenting" alt-grubu vs "depresyon-bağımsız parenting"
alt-grubu mevcut.

## 4. Bifactor S-1 Modeli (Eid 2017)

### Mantık

Klasik bifactor identification sorunlarını çözer. **Bir spesifik faktörü referans olarak sabitler**
(örn. Sıcaklık) ve diğerleri için spesifik faktörler tahmin eder.

```r
run_bifactor_s1_model <- function(df_family) {
  bifactor_s1_model <- '
    # G factor (Sıcaklık ile sabitlenmiş referans)
    G =~ embu_p_q01 + embu_p_q03 + embu_p_q06 + embu_p_q07 +
          embu_p_q13 + embu_p_q17 + embu_p_q20 + embu_p_q24 + embu_p_q26 +
          embu_p_q04 + embu_p_q08 + embu_p_q14 +  # Aşırı koruma
          embu_p_q05 + embu_p_q09 + embu_p_q10 +  # Reddetme
          embu_p_q02 + embu_p_q11                  # Karşılaştırma

    # Spesifik faktörler (referans dışı)
    S_AsiriKor =~ embu_p_q04 + embu_p_q08 + embu_p_q14 + embu_p_q15 +
                   embu_p_q19 + embu_p_q23 + embu_p_q25
    S_Redd     =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + embu_p_q12 +
                   embu_p_q16 + embu_p_q21 + embu_p_q22 + embu_p_q28
    S_Karsilas =~ embu_p_q02 + embu_p_q11 + embu_p_q18 + embu_p_q27 + embu_p_q29

    # Faktörler arası ortagonalite
    G ~~ 0*S_AsiriKor
    G ~~ 0*S_Redd
    G ~~ 0*S_Karsilas
    S_AsiriKor ~~ 0*S_Redd
    S_AsiriKor ~~ 0*S_Karsilas
    S_Redd ~~ 0*S_Karsilas
  '

  fit_bf <- lavaan::cfa(bifactor_s1_model, data = df_family,
                          estimator = "WLSMV", ordered = TRUE)

  # Explained Common Variance (ECV) — Reise (2012)
  ecv <- semTools::reliability(fit_bf)["omega_h", ]

  list(fit = fit_bf, ecv = ecv,
        fit_meas = fitMeasures(fit_bf, c("cfi.scaled", "rmsea.scaled", "srmr")))
}
```

### Bifactor metrik yorumlama (Reise 2012)

| Metrik | Anlamı | Eşik |
|---|---|---|
| **ω_h (omega hierarchical)** | G faktörünün toplam varyanstaki payı | > .50 |
| **ω_hs (omega hierarchical specific)** | Spesifik faktörün arta kalan varyanstaki payı | > .50 |
| **ECV (Explained Common Variance)** | G ortak varyansın oranı | > .60 → unidim eğilim |
| **PUC (Percent of Uncontaminated Correlations)** | G saf korelasyon oranı | > .80 → unidim güvenli |

**Yorum:** ω_h > .50 ise EMBU-P aslında "tek genel parenting" boyutu olarak yorumlanmalı, alt-ölçek
skorları kısıtlı bilgi taşır. ω_hs spesifik faktör için < .30 ise alt-ölçek skoru *kullanılmamalıdır*.

## Targets entegrasyonu

```r
# _targets.R'ye eklenecek (KISIM VII gelecek faz)
tar_target(lpa_mother_typology,    run_lpa_mother_typology(df_family_scored)),
tar_target(lca_categorical,        run_lca_categorical(df_family_scored)),
tar_target(mixture_regression,     mix_reg),  # üstteki kısa kod
tar_target(bifactor_s1_model,      run_bifactor_s1_model(df_family_scored)),
tar_target(latent_classes_table,   format_latent_table(lpa_mother_typology, lca_categorical),
            format = "file")
```

## Tedbir denetimi

- [ ] LPA için n > 200 (her profilin minimum 30 vakası önerilir; 482 yeterli)
- [ ] BIC + entropy + LMR-LRT + BLRT **birlikte** kullanıldı (tek metrik yetersiz)
- [ ] Profil etiketleri *betimsel* (içerik tabanlı), klinik tanı değil
- [ ] LCA'da median split alternatifi olarak klinik eşikler kullanıldı
- [ ] Mixture regression için BIC ile k seçildi
- [ ] Bifactor için ECV/PUC hesaplandı; unidim güvenli mi raporlandı
- [ ] Class membership'ı predictor olarak ikincil analizde kullanırken classification
      uncertainty (modal vs probabilistic) belirtildi
- [ ] [KEŞİFSEL] etiketi eklendi (KISIM VII tezde keşifsel)

## Raporlama paragrafı (Türkçe APA 7)

> "Anne tipolojisi gizil profil analiziyle (LPA) belirlenmiştir. Beck total skoru, EMBU-P dört alt
> ölçek puanı ve SES kompozit göstergeleri standardize edilerek 1–6 profil çözümü karşılaştırılmıştır.
> En uygun çözüm 4 profil olarak bulunmuş (BIC = 3148, entropy = .82, LMR-LRT p = .003); profiller
> içerik temelinde 'Adapte', 'Aşırı Koruyucu', 'Tükenmiş' ve 'Standart' olarak adlandırılmıştır.
> Profil dağılımı DM ve Kontrol grupları arasında anlamlı farklılaşmıştır (χ²(3) = 18.4, p < .001,
> Cramér's V = .28); özellikle 'Tükenmiş' profilde DM oranı %71 olarak bulunmuştur. Bifactor S-1
> modelinde EMBU-P için ω_h = .52, ω_hs(Reddetme) = .18 hesaplanmış; bu, alt-ölçek skorlarının
> spesifik bilgisinin sınırlı olduğuna ve genel 'parenting' boyutunun ana bilgi taşıyıcısı olduğuna
> işaret etmektedir. Bu bulgular **keşifsel** statüdedir; OSF kaydı kapsamında confirmatory
> hipotezler arasında değildir."

## Çapraz referanslar

- Bifactor için CFA detayları → [`psikometri-pipeline.md`](psikometri-pipeline.md) (omega vs alpha)
- LPA çıktısının clinical utility'ye taşınması → [`klinik-fayda.md`](klinik-fayda.md) (risk score)
- Joint display ile niteliksel kategorilerle karşılaştırma → [`karma-yontem.md`](karma-yontem.md)
- Mixture model identification için Bayesian alternatif → [`bayesci-paralel-hat.md`](bayesci-paralel-hat.md)
- Kaynaklar: Lanza & Cooper (2016); Eid et al. (2017); Akogul & Erisoglu (2017); Reise (2012)
