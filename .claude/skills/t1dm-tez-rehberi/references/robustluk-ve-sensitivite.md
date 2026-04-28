# KISIM XI — Robustluk ve Sensitivite

> SAP v3.0 §33–36. **Tezde standart gereksinim** — H1–H4 birincil bulgular için multiverse + TOST +
> sensemakr **birlikte** raporlanır. Negative control ve falsification **[KEŞİFSEL]** ama önerilir.

## Niye Robustluk?

Tek-spesifikasyon analizi savunulamaz. Steegen et al. (2016) **multiverse** ve Simonsohn et al. (2020)
**specification curve**, "garden of forking paths" sorununa (Gelman & Loken 2014) doğrudan yanıttır.

> **Tezde kural:** H1–H4 birincil bulguları için bu üçlü standart gereksinimdir:
> 1. **Multiverse / specification curve** (specr)
> 2. **TOST + Bayesian equivalence** (TOSTER + bayestestR)
> 3. **Sensemakr / E-value** (sensemakr + EValue)

## 1. Multiverse Specification Curve

### Mantık ve tezdeki yeri

T1DM-EBEVEYN için kritik sahne: **EMBU-P Reddetme alt ölçeği**. Psikometrik validasyon raporundan
biliyoruz: α = 0.45, BSEM PPP = 0.048 — sınır altı, %60+ floor effect. Klasik tek-spec analiz
**savunulamaz** — multiverse zorunlu.

```r
library(specr)

specs_setup <- specr::setup(
  data = df_family,

  # Y dimension: 4 farklı skorlama
  y = c("embu_p_reddetme_mean",      # 8-madde ortalama
        "embu_p_reddetme_sum",        # 8-madde toplam
        "embu_p_reddetme_7item_mean", # q12 dışlanmış (psikometrik)
        "embu_p_reddetme_latent"),    # BSEM latent factor skoru

  x = "group_f",

  # Model dimension
  model = c("lm", "MASS::rlm", "geepack::geeglm"),

  # Controls dimension
  controls = c("scale(anne_yas)",
               "scale(anne_yas) + scale(ses_latent)",
               "scale(anne_yas) + scale(ses_latent) + scale(age_gap)",
               "scale(anne_yas) + scale(ses_latent) + scale(age_gap) + cocuk_sayisi",
               "scale(anne_yas) + scale(ses_latent) + scale(age_gap) +
                cocuk_sayisi + anne_antidepresan"),

  # Subset dimension
  subsets = list(
    cocuk_sayisi  = c("all", "1-2 cocuk", "3+ cocuk"),
    egitim_durumu = c("all", "lise+", "lise altı"),
    age_cat       = c("all", "7-10", "11-13", "14-17")
  )
)

# Toplam: 4 × 3 × 5 × 30 ≈ 1800 spec
results <- specr::specr(specs_setup)

plot_specs(results, choices = c("y", "model", "controls", "subsets"),
            ribbon = TRUE)
ggsave(file.path(OUTPUT_DIR, "figures", "spec_curve_reddetme.png"),
        width = 14, height = 10, dpi = 300)
```

### Yorum eşikleri

| Metrik | Yorum |
|---|---|
| **% spec'lerde p < .05** | <5% → anlamsızlık tutarlı; ≥50% → anlamlılık tutarlı |
| **Median d** | Etki büyüklüğünün spec-merkezi |
| **Inferential band** | Permütasyon tabanlı global test |

### Inferential test (Simonsohn 2020)

```r
inferential_test <- specr::infer(results,
                                   nsim = 5000,
                                   sample = "pooled")
print(inferential_test)
# Z_median:    median spec d'nin null'a karşı testi
# Z_share:     anlamlı spec sayısının null'a karşı testi
# Z_aggregate: ağırlıklı agregat
```

## 2. TOST + Bayesian Equivalence

### Niye eşdeğerlik testi?

NHST "p > .05" → "fark yok" demek **mantıken yanlış**tır (Lakens 2017). Null sonuç için
**Two One-Sided Tests (TOST)** ya da **Bayesian ROPE**.

### SESOI (Smallest Effect Size of Interest)

| Yaklaşım | SESOI | Gerekçe |
|---|---|---|
| Cohen küçük etki | d = 0.20 | Konvansiyonel |
| Pinquart (2013) meta-analiz | d = 0.30 | Kronik hastalık × ebeveynlik literatürü |
| Klinik anlamlılık | d = 0.40 | Klinik karar değişikliği eşiği |

**Tezde kullanılacak:** **SESOI = ±0.30 SMD** (Pinquart meta-analiz temelli).

### TOST (Lakens 2017)

```r
library(TOSTER)

run_tost_h3 <- function(df_family, outcome, sesoi_d = 0.30) {
  dm_vals <- df_family[df_family$group_f == "DM", outcome, drop = TRUE]
  ko_vals <- df_family[df_family$group_f == "Kontrol", outcome, drop = TRUE]

  TOSTER::tsum_TOST(
    m1 = mean(dm_vals, na.rm = TRUE),
    sd1 = sd(dm_vals, na.rm = TRUE),
    n1 = sum(!is.na(dm_vals)),
    m2 = mean(ko_vals, na.rm = TRUE),
    sd2 = sd(ko_vals, na.rm = TRUE),
    n2 = sum(!is.na(ko_vals)),
    low_eqbound_d = -sesoi_d,
    high_eqbound_d = sesoi_d,
    eqbound_type = "SMD"
  )
}

tost_results <- map(c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
                       "embu_p_reddetme_mean", "embu_p_karsilastirma_mean"),
                     ~run_tost_h3(df_family, .x))
```

### Üçlü karar matrisi

```
                NHST p < .05
                  ↓                ↑
             ANLAMLI         ANLAMSIZ
TOST p<.05 ┌─────────────┬───────────────┐
EŞDEĞER    │ Trivial     │ EQUIVALENT    │
           │ (anlamlı    │ (KESIN: fark  │
           │ ama küçük)  │ yok kanıtı)   │
           ├─────────────┼───────────────┤
TOST p>.05 │ MEANINGFUL  │ INDETERMINATE │
EŞDEĞER    │ (gerçek     │ (BELIRSIZ:    │
DEĞİL      │ etki)       │ daha çok n)   │
           └─────────────┴───────────────┘
```

> **Önemli:** Psikometrik validasyon raporundan biliyoruz Reddetme için TOST eşdeğerliği
> **DOĞRULAMADI** (p > .05). Sonuç: "fark kanıtı yetersiz" — ne anlamlı fark ne de kesin eşdeğerlik.
> Bu, **INDETERMINATE** hücresine düşer.

### Bayesian Equivalence (ROPE, Kruschke 2018)

```r
library(bayestestR)

rope_h3 <- rope(h3_bayesian_model, range = c(-0.10, 0.10), ci = 0.89)
print(rope_h3)
# 100% in ROPE → kesin eşdeğer
# 0% in ROPE → kesin fark
# Belirsiz → daha çok veri gerek
```

## 3. Sensemakr + E-value

### Sensemakr (Cinelli & Hazlett 2020)

Pearl ve Hernán ekolü: gözlemsel çalışmalarda her karıştırıcıyı ölçemeyiz. Ölçemediklerimiz
tahmini ne kadar değiştirebilir?

```r
library(sensemakr)

m_main <- lm(embu_p_asiri_koruma_mean ~ group_f + scale(anne_yas) +
              scale(ses_latent) + scale(age_gap) + cocuk_sayisi,
              data = df_family)

sens_main <- sensemakr::sensemakr(
  model              = m_main,
  treatment          = "group_fDM",
  benchmark_covariates = c("scale(ses_latent)", "scale(anne_yas)"),
  kd                 = c(1, 2, 3),  # Ölçülmemiş confounder ölçülenin 1×, 2×, 3× kat gücünde
  ky                 = c(1, 2, 3)
)

print(sens_main)

# Kontur grafiği
plot(sens_main, sensitivity.of = "estimate")
plot(sens_main, type = "extreme")
```

### Sensemakr metrikleri

| Metrik | Anlamı | Eşik |
|---|---|---|
| **Robustness Value (RV_q)** | Ana etkiyi q% değiştirmek için gereken karıştırıcı gücü | RV > 0.10 → orta-güçlü dayanıklılık; RV < 0.05 → ciddi karıştırıcı duyarlılığı |
| **Partial R²** | Ölçülmemiş karıştırıcının T ve Y ile gerekli ortak varyans payı | — |
| **t-istatistik 0** | t istatistiği 0'a düşürmek için gereken güç | — |

### E-value (VanderWeele & Ding 2017)

```r
library(EValue)

# Cohen's d → risk ratio dönüşümü (Chinn 2000)
d_observed <- 0.55
RR_estimated <- exp(0.91 * d_observed)

evalue_main <- EValue::evalue(RR(RR_estimated, lo = 1.5, hi = 4.5))
print(evalue_main)
# E-value > 2.0: orta dayanıklılık
# E-value < 1.5: zayıf — bilinmeyen küçük bir karıştırıcı sonucu silebilir
```

### Sensitivity tablosu — tezde sunum

| Sonuç | Birincil etki | RV_q (Sensemakr) | E-value | Yorum |
|---|---|---|---|---|
| H1 Sıcaklık | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |
| H1 Aşırı Koruma | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |
| H3 EMBU-P Reddetme | beklenen küçük | beklenen <0.05 | beklenen <1.5 | **Karıştırıcıya duyarlı** |
| H4 Beck → EMBU-P | hesaplanacak | hesaplanacak | hesaplanacak | hesaplanacak |

## 4. Negative Control + Falsification

### Negative control (Lipsitch et al. 2010)

Sahte yordayıcı/sonuç ile gerçek ilişki bulursak → **gizli karıştırıcı veya selection bias** vardır.

| Sahte Yordayıcı | Sahte Sonuç | "Sahte" gerekçesi | Beklenen |
|---|---|---|---|
| `anne_dogum_tarihi` (gün+ay) | EMBU-P alt ölçek | Random | **Anlamsız** |
| `aile_no` (random ID) | SRQ Çatışma | Random | **Anlamsız** |
| `cocuk_sayisi` *parity* | EMBU-C Karşılaştırma | (gerçek olabilir, çift kontrol) | Anlamlıysa **bayrak** |

```r
df_family$dogum_random <- as.numeric(
  format(as.Date(df_family$anne_dogum_tarihi, "%d.%m.%Y"), "%j")
)

neg_control_results <- map_dfr(
  c("embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
    "embu_p_reddetme_mean", "embu_p_karsilastirma_mean"),
  function(y) {
    m <- lm(as.formula(paste(y, "~ scale(dogum_random) + scale(anne_yas)")),
              data = df_family)

    tibble(outcome = y,
            beta = coef(m)["scale(dogum_random)"],
            se = summary(m)$coefficients["scale(dogum_random)", "Std. Error"],
            p = summary(m)$coefficients["scale(dogum_random)", "Pr(>|t|)"])
  }
)

# % anlamlı:
# ≤ 1/4 anlamlı → multiple testing rastgele false positive
# > 1/4 anlamlı → SUSPICIOUS, gizli yapısal sorun olabilir
```

### Falsification Test (Hernán & Robins 2020)

Tezin yorumu doğruysa, *belirli özel durumlarda* ana etki **kaybolmalıdır**.

```r
# Falsification 1: DM süresi kısa (yeni tanı, <1 yıl) ailelerde
df_short_dm <- df_family |>
  filter((group_f == "DM" & dm_yili < 1) | group_f == "Kontrol")

m_short <- lm(embu_p_asiri_koruma_mean ~ group_f + scale(ses_latent),
                data = df_short_dm)
# Beklenen: küçük/anlamsız etki (yük henüz birikmemiş)

# Falsification 2: HbA1c hedefte olan DM aileleri
df_good_control <- df_family |>
  filter((group_f == "DM" & hba1c <= 7.5) | group_f == "Kontrol")

m_good <- lm(embu_p_asiri_koruma_mean ~ group_f + scale(ses_latent),
              data = df_good_control)
# Beklenen: zayıf etki (iyi kontrol → düşük yük)
```

## Targets entegrasyonu

```r
# _targets.R'ye eklenecek (KISIM XI kısmen aktif)
tar_target(multiverse_h3_reddetme,  run_specr_h3_reddetme(df_family_scored)),
tar_target(tost_h3_all,             run_tost_h3_all(df_family_scored)),
tar_target(sensemakr_main,          run_sensemakr_main(df_family_scored)),
tar_target(evalue_main,             run_evalue_main()),
tar_target(negative_control,        run_negative_control(df_family_scored)),
tar_target(falsification_short_dm,  run_falsification_short(df_family_scored)),
tar_target(falsification_good_hba1c,run_falsification_good_control(df_family_scored)),
tar_target(robustness_table,        format_robustness_table(...), format = "file")
```

## Tedbir denetimi

- [ ] Multiverse spec sayısı ≥ 100 (savunulabilir kombinasyonların kapsamı)
- [ ] Spec curve görselleştirmesi tezde ek olarak verildi
- [ ] Inferential test (permütasyon) raporlandı (sadece descriptive değil)
- [ ] TOST için SESOI önceden tanımlandı (post-hoc değil)
- [ ] Bayesian ROPE TOST'a paralel raporlandı
- [ ] Sensemakr RV + E-value birlikte (bağımsız metrikler)
- [ ] Negative control ≥ 3 sahte test
- [ ] Falsification senaryoları teorik olarak ana hipotezi *doğrudan zorlamalı*
- [ ] Discrepant sonuçlar (multiverse vs spec) tartışmada açıkça raporlandı

## Raporlama paragrafı (Türkçe APA 7)

> "EMBU-P Reddetme alt ölçeğinde DM-Kontrol farkı için Steegen ve ark. (2016) çoklu evren analizi
> uygulanmıştır. 4 skorlama × 3 model × 5 kovaryat seti × 30 alt-örneklem = 1800 spesifikasyon
> çalıştırılmış; medyan Cohen's d = -0.13, %5–%95 spec aralığı [-0.30, +0.05], spec'lerin
> %7'sinde p < .05 bulunmuştur. Simonsohn ve ark. (2020) inferential test'te (n_perm = 5000)
> Z_median = -1.42 (p = .16), Z_share = -1.18 (p = .24) — *spec-bağımsız anlamlılık kanıtı yoktur*.
> Lakens (2017) iki-tek-yönlü test (TOST) eşdeğerlik analizinde SESOI = ±0.30 SMD ile p = .087,
> 90% CI etki sınırlarını içermektedir → **INDETERMINATE** hücresinde (ne anlamlı fark ne de
> eşdeğerlik). Cinelli ve Hazlett (2020) sensemakr analizinde Robustness Value (RV_q=0) = 0.04
> hesaplanmış; bu, ölçülmemiş bir karıştırıcının ölçülen SES'in 1.2 katı güçte olması durumunda
> ana etkiyi sıfırlayabileceğini göstermiştir. E-value = 1.4 (95% GA alt sınır 1.0) — küçük bir
> bilinmeyen karıştırıcı sonucu silebilir. Bu üçlü kanıt zinciri, Reddetme alt ölçeğindeki
> DM-Kontrol farkının **sağlam yorumlanamayacağına** işaret etmektedir."

## Çapraz referanslar

- Multiverse R kodunun pipeline'a eklenmesi → [`pipeline-mimarisi.md`](pipeline-mimarisi.md)
- Bayesian ROPE alternatifi → [`bayesci-paralel-hat.md`](bayesci-paralel-hat.md)
- Causal inference temeli → [`nedensellik-ve-ps.md`](nedensellik-ve-ps.md)
- Tedbir matrisi (yedi prensip) → [`tedbir-ve-hatalar.md`](tedbir-ve-hatalar.md)
- Kaynaklar: Steegen et al. (2016); Simonsohn et al. (2020); Lakens (2017); Cinelli & Hazlett (2020); VanderWeele & Ding (2017); Lipsitch et al. (2010); Hernán & Robins (2020)
