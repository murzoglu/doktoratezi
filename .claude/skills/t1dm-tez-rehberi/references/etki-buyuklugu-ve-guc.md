# Etki Büyüklüğü ve İstatistiksel Güç

**Ne zaman oku:** Cohen's d / ω² / r raporlarken, "küçük/orta/büyük" değerlendirmesi
yaparken, simr veya pwrss ile güç hesabı yaparken, Pinquart 2013 prior'ı türetirken, SESOI
(Smallest Effect Size of Interest) belirlerken.

**Kaynaklar:** Cohen (1988); Schäfer & Schwarz (2019); Funder & Ozer (2019); Lakens (2017);
Green & MacLeod (2016) — simr; Pinquart (2013) meta-analizi (parenting → child outcome);
Gelman, Hill & Vehtari (2021) Ch. 4 (design analysis, winner's curse).

---

## Temel İlke

> "p < .05" yerine **etki büyüklüğü + güven aralığı + pratik anlam**. APA 7 zorunlu kıldığı
> minimum standart. Funder & Ozer 2019: r = .05 düzeyinde sürdürülmüş etki, gelişimsel
> trajektoriyi şekillendirebilir.

Bu projede **her** primer karşılaştırma için:
1. Nokta tahmini (β, d, r, OR)
2. %95 güven aralığı (veya Bayesian credible interval)
3. Domain-specific benchmark karşılaştırması
4. Pratik anlam yorumu (Türkçe paragraf)

---

## Cohen Klasik Eşikleri (Karşılaştırma İçin)

| Metrik | Küçük | Orta | Büyük |
|--------|-------|------|-------|
| Cohen's d | 0.20 | 0.50 | 0.80 |
| Pearson r | 0.10 | 0.30 | 0.50 |
| η² (eta-squared) | 0.01 | 0.06 | 0.14 |
| ω² (omega-squared) | 0.01 | 0.06 | 0.14 |
| f² | 0.02 | 0.15 | 0.35 |
| Cramér's V | 0.10 | 0.30 | 0.50 |
| OR | 1.5 | 2.5 | 4.0 |

**Uyarı:** Cohen kendisi "aşırı kullanılmasın" demiştir. Domain'e özgü beklenti bilinmediğinde
fallback olarak kullan; bilindiğinde bypass.

---

## Gelişimsel ve Davranış Bilimleri Domain-Calibrated Beklenti

(Schäfer & Schwarz 2019 + Funder & Ozer 2019 meta-meta-analiz):

| Alan | Tipik d | Tipik r | Not |
|------|---------|---------|-----|
| Parenting müdahaleleri | 0.25–0.50 | .12–.25 | Hedefli > evrensel |
| Parent-child ↔ child outcome | 0.30–0.60 | .15–.30 | Shared method variance ile zayıflar |
| Akran etkisi → davranış | 0.20–0.40 | .10–.20 | Adolesanda güçlenir |
| Ekran süresi → iyilik hali | 0.05–0.15 | .03–.08 | Çok küçük; yüksek N gerekir |
| Yürütücü işlevler → akademik | 0.40–0.70 | .20–.35 | Orta-büyük |
| Bağlanma → uyum | 0.30–0.50 | .15–.25 | Insecure/disorganized güçlü |
| SES → çocuk gelişimi | 0.40–0.80 | .20–.40 | Doz-yanıt |
| Kardeş ilişki kalitesi | 0.20–0.40 | .10–.20 | İkili rapor uyumuna bağlı |
| Mizaç → davranış sorunu | 0.30–0.60 | .15–.30 | Negative emotionality güçlü |
| CBT → çocuk anksiyete | 0.50–0.90 | .25–.40 | Kontrollü denemelerde büyük |

### Bu Projeye Uyarlama (Pinquart 2013)

Pinquart (2013) meta-analizi parenting → child outcome ilişkilerinde:
- r ≈ 0.13 (Reddetme → externalizing)
- r ≈ 0.18 (Sıcaklık → ↓ internalizing)
- r ≈ 0.20 (Sıcaklık → social competence)

**SESOI (Smallest Effect Size of Interest):** Bu projede:
- d ≥ 0.30 (clinically meaningful, Pinquart alt sınırı)
- r ≥ 0.15 (literatürün alt limiti)
- TOST eşdeğerlik bound: ±0.20 SD

---

## Cohen's d Hesabı

### Bağımsız Gruplar

```r
library(effectsize)

# Welch t-test sonrası
cohens_d(embu_p_sicaklik_mean ~ group_dm, data = df_family_ses,
          pooled_sd = FALSE)

# Hedges g düzeltmesi (küçük örneklem için)
hedges_g(embu_p_sicaklik_mean ~ group_dm, data = df_family_ses)
```

Hedges g = d × (1 − 3 / (4(n1+n2) − 9)). N ≤ 20 gruplarda fark anlamlı.

### Eşleştirilmiş

```r
# Within-subjects (paired)
cohens_d(x = anne_pre, y = anne_post, paired = TRUE)
# d_z = M_diff / SD_diff (Lakens 2013)

# Average method (preferred for meta-analysis)
# d_av = M_diff / ((SD1 + SD2)/2)
```

### Multilevel Modelden

```r
library(parameters)
m1 <- lmer(outcome ~ group_dm + (1 | aile_no_f), data = df_long_scored)
standardize_parameters(m1, method = "refit")
# β_std = etki büyüklüğü eşdeğeri
```

---

## ANOVA Etki Büyüklükleri

```r
m_anova <- aov(outcome ~ role_f, data = df_long_scored)
effectsize::eta_squared(m_anova, partial = TRUE)
effectsize::omega_squared(m_anova, partial = TRUE)
effectsize::epsilon_squared(m_anova)
```

**ω² preferred** — η² küçük örneklemde upward biased.

---

## Regresyon Etki Büyüklüğü

```r
m_reg <- lm(outcome ~ predictor + covariate, data = df_family_ses)
summary(m_reg)$r.squared
summary(m_reg)$adj.r.squared

# Cohen's f² (added predictor için)
m_reduced <- lm(outcome ~ covariate, data = df_family_ses)
f2_change <- (summary(m_reg)$r.squared - summary(m_reduced)$r.squared) /
             (1 - summary(m_reg)$r.squared)
```

---

## Bayesian Etki Büyüklüğü

```r
library(bayestestR)

m_brms <- brm(outcome ~ group_dm + (1 | aile_no_f), data = df_long_scored)

# Standardize
parameters::standardize_parameters(m_brms)

# 95% credible interval
describe_posterior(m_brms, ci = 0.95)

# Probability of direction
p_direction(m_brms)
```

---

## Power Analysis — `simr` Multilevel

H1 multilevel modeli için:

```r
library(simr)

# Pilot model (mevcut data)
m_pilot <- lmer(
  embu_c_sicaklik_mean ~ group_dm + (1 | aile_no_f),
  data = df_long_scored
)

# Etki büyüklüğünü Pinquart'a göre fix et
fixef(m_pilot)["group_dm"] <- 0.30   # SESOI

# Güç hesabı
power_h1 <- powerSim(m_pilot, nsim = 1000, test = fixed("group_dm"))
print(power_h1)
# Çıktı: Power = X% (95% CI: ...)

# Mevcut N yetersiz ise extend et
extend_h1 <- extend(m_pilot, along = "aile_no_f", n = 300)
powerCurve(extend_h1, along = "aile_no_f",
            breaks = seq(150, 300, by = 25), nsim = 200)
```

**Bu projedeki kanonik durum:** N = 241 aile sabit (post-hoc güç). simr ile mevcut güç
raporlanır; "güç düşük" çıkarsa Bayesian sensitivity ile karar.

### Mediation Power — `pwrss`

```r
library(pwrss)

# Sobel-tarzı mediation power
pwrss.f.mediation(
  a = 0.30,         # X → M standardized
  b = 0.30,         # M → Y standardized
  cprime = 0.10,    # Direct
  alpha = 0.05,
  power = 0.80
)
# Returns required N
```

---

## Gelman'ın Design Analysis ve Winner's Curse

Gelman, Hill & Vehtari (2021) Ch. 16:

> Düşük güçlü çalışmalarda yalnız "anlamlı" sonuçlar yayınlanır; bu **etki büyüklüğünün
> sistematik olarak şişirilmesi** demektir (Type M error / magnitude error).

Bu projede:

```r
library(retrodesign)

# Pinquart prior etki: d = 0.30
# Bu çalışma SE'si ≈ 0.13 (n_DM = 120 + n_kontrol = 121)
retrodesign(A = 0.30, s = 0.13, alpha = 0.05)
# Type M error rate: gözlenen etki gerçek etkiden ~%X şişebilir
# Type S error rate: işaret hatası %X
```

`retrodesign(A = 0.30, s = 0.13)` çıktısı:
- Power ≈ 60% (orta düzey)
- Exaggeration (Type M) ≈ 1.3× (gözlenen büyüklük gerçeğin %30 üzerinde)
- Type S < %1

Bu, "güç orta — etki tahmini orta düzeyde şişmiş olabilir, ihtiyatla yorumla" diye okunur.

---

## ROPE Testi (Region of Practical Equivalence)

```r
library(bayestestR)

# H0: |β_std| < 0.10 (SESOI)
rope(
  m_h1_brms,
  ci = 0.95,
  range = c(-0.10, 0.10)
)
# Çıktı: 95% credible interval'ın % kaçı ROPE içinde?
# %95'in tamamı ROPE'da → eşdeğerlik (TOST eşdeğeri)
# %0'ı ROPE'da → açık fark
```

---

## Bayesian Prior — Pinquart'tan Türetim

Pinquart 2013'te:
- Reddetme ↔ externalizing: r = 0.13 → Cohen's d ≈ 0.26 → β_std ≈ 0.13
- 95% CI: ~[.10, .16]

Standardized regresyon prior'ı:

```r
# Normal(mean = 0.13, sd = 0.05) — Pinquart point estimate ± uncertainty band
prior(normal(0.13, 0.05), class = "b", coef = "rejection_to_outcome")
```

Bu prior, mevcut çalışmanın Pinquart'ın etrafında olabileceğini ama %95 prior interval'ın
[0.03, 0.23] aralığını kapsadığını söyler. Veri bu aralıkta toplandığında posterior daraltır.

`references/ileri-yontemler.md` "Pinquart 2013 Meta-Analizinden Prior Türetimi" bölümünde
detay var.

---

## Equivalence Testing (TOST)

```r
library(TOSTER)

# Anlamlı olmayan t-test sonrası eşdeğerlik testi
TOSTtwo(
  m1 = M_DM, m2 = M_Kontrol,
  sd1 = SD_DM, sd2 = SD_Kontrol,
  n1 = N_DM, n2 = N_Kontrol,
  low_eqbound_d  = -0.20,        # SESOI
  high_eqbound_d =  0.20,
  alpha = 0.05
)
```

Çıktı:
- "Statistically equivalent" (ikisi de p < .05) → fark yok demek mantıklı.
- "Not statistically equivalent" → fark olabilir ama power yetmedi; "yok" deme.
- "Statistically different and equivalent" → küçük ama gerçek bir fark.

---

## Türkçe APA Sablonu

> "DM grubunun EMBU-P Reddetme alt ölçek puanı kontrol grubuna göre Cohen's d = 0.34
> (Hedges g = 0.33, 95% GA [0.08, 0.59]) düzeyinde anlamlı yüksek bulunmuştur. Bu etki,
> Pinquart'ın (2013) meta-analizinde rapor edilen ortalama parenting–child outcome ilişkisi
> büyüklüğüyle (d ≈ 0.26) tutarlı, ancak güven aralığının alt sınırı SESOI eşiği olan d =
> 0.20'nin altındadır; bu nedenle pratik anlam belirsizdir. Gelman ve diğerlerinin (2021)
> Type M error çerçevesinde, mevcut örneklem büyüklüğünde post-hoc güç ≈ %62; gözlenen
> etki büyüklüğü gerçek etkiden yaklaşık 1.3× şişmiş olabilir. Bu nedenle bulgu, Bayesian
> Pinquart-bilgilendirilmiş prior altında posterior aralık β_std = 0.18 (95% CrI [0.05,
> 0.30]) ile teyit edilmiştir."

---

## Effect Size Tablosu — gtsummary ile

```r
library(gtsummary)

m_h1 <- lmer(embu_c_sicaklik_mean ~ role_f + (1 | aile_no_f), data = df_long_scored)

tbl_regression(m_h1,
               estimate_fun = function(x) style_number(x, digits = 2),
               pvalue_fun  = function(x) style_pvalue(x, digits = 2)) |>
  add_glance_source_note(include = c(nobs)) |>
  modify_caption("**Tablo X.** H1 birincil model regresyon çıktısı")
```

`effectsize::standardize_parameters()` ek sütun olarak eklenir; sonuç tablo APA formatına
yakın.

---

## Sık Yapılan Hatalar

1. **"Anlamlı" → "büyük etki" atlama** — d = 0.10 anlamlı ama önemsiz olabilir (büyük N'da).
2. **Cohen eşiklerine sıkı bağlanmak** — domain'e bak. Parenting'te d = 0.30 = "büyük".
3. **Multilevel'da klasik d kullanmak** — clustering varyansı düzelttiğinde standardize
   değişir; `standardize_parameters()` kullan.
4. **TOST'u ihmal** — "anlamlı yok" ≠ "yok"; eşdeğerliği iddia ediyorsan TOST.
5. **simr'ı atlamak** — analytic power formülleri multilevel için yetmez.
6. **Pinquart prior'ı yarı-uydurma** — meta-analiz pointi + uncertainty band birlikte;
   point alone bias.
7. **Type M error'ı yok varsayma** — düşük güçlü çalışmada effect inflation gerçek; runbook'ta
   gerekirse retrodesign.
8. **Hedges g'yi atlamak** — küçük örneklemde Cohen d biased; g raporla.
9. **CI raporlamadan d/r vermek** — APA 7 zorunlu kılar.
10. **Posterior'dan tek nokta tahmini almak** — full posterior summary (ci, pd, ROPE).

---

## SAP v3.0 Genişletilmiş Etki Büyüklüğü ve Güç Bölümleri

### 11. SESOI Standardı (KISIM XI tezde zorunlu)

| Yaklaşım | SESOI | Gerekçe |
|---|---|---|
| Cohen küçük etki | d = 0.20 | Konvansiyonel ama çok düşük |
| **Pinquart (2013) meta-analiz** | **d = 0.30** | Kronik hastalık × ebeveynlik literatürü medyanı; **tezde standart** |
| Klinik anlamlılık | d = 0.40 | Klinik karar değişikliği eşiği |
| Bayesian ROPE eşiği | ±0.10 | Standardize ölçek için pratik eşdeğerlik bandı |

**Tezde kullanılan:** **SESOI = ±0.30 SMD** (Pinquart-temelli, *önceden tanımlı*, post-hoc değil).

> **Kural:** SESOI veri görmeden tanımlanır. TOST bandının `low_eqbound_d = -0.30, high_eqbound_d = 0.30`
> olduğu kod yorumunda gerekçelendirilir.

### 12. Bayesian Prior Derivation Standardı (KISIM XII)

Pinquart meta-analizinden Bayesian prior türetimi:

```
Pinquart 2013: d ≈ 0.40, %95 CI [0.25, 0.55]
SD ≈ (0.55 - 0.25) / (2 × 1.96) ≈ 0.077

Tezde 3× geniş prior (skeptical / weakly informative):
  prior(normal(0.30, 0.50), class = b, coef = "role_fDM_Hasta_Indeks")

Niye 3×?
- Türk örneklemi farklı olabilir
- Meta-analizdeki heterogenlik kovaryata göre
- Bayesian güven dar prior'a fazla yapışmamak için geniş tutulur
```

### Prior sensitivity protokolü

| Test | Prior SD | BF₁₀ değişimi |
|---|---|---|
| Default | 0.50 | hesaplanır |
| Yarı | 0.25 | hesaplanır (daha bilgi verici) |
| İki kat | 1.00 | hesaplanır (daha skeptical) |

Üç sonuç **birlikte raporlanır** ([`bayesci-paralel-hat.md`](bayesci-paralel-hat.md) §sensitivity).

### 13. Network Sample Size + Stability (KISIM VIII)

| Metrik | Eşik | Kaynak |
|---|---|---|
| n / vars | ≥ 3 (her node başına) | Epskamp et al. (2018) |
| **CS-coefficient (centrality)** | > .50 güçlü, > .25 kabul | Epskamp et al. (2018) |
| Bootstrap edge stability | %95 CI sıfırı içermez | bootnet pakage |
| EBIC tuning gamma | 0.5 (T1DM tezi) | Foygel & Drton (2010) |

**T1DM tezi için:** n = 241 aile, 7 node → n/vars ≈ 34. Yeterli ama Beck 21-madde network için
yetersiz (n/vars = 11.5; CS-coefficient < .25 olabilir → keşifsel etiket).

### 14. Bayesian Power ≠ Frequentist Power

| Frequentist | Bayesian eşdeğeri |
|---|---|
| Tip I error (α) | False positive rate (FPR) — prior tarafından modüle edilir |
| Güç (1 − β) | Probability of conclusive evidence (BF > 10 veya ROPE %5) |
| Sample size for d = 0.30, α = 0.05, power = .80 → n ≈ 175 | Sample size for BF₁₀ > 10 with d = 0.30 → n ≈ 200 (genelde 1.1-1.2× frequentist) |

> **Uyarı:** Bayesian "güç" frequentist çerçeveden farklı kavramsal bir şey değil; aynı veri farklı
> raporlanmış. Stopping rule (BF > 10 olunca dur) ile sample size minimum belirsizdir; **a priori
> sabit n** kullan.

### 15. Multilevel Sample Size — Hox + simr Sentezi

T1DM tezi 241 aile × 2 katılımcı yapısı için:

```r
library(simr)

# Mevcut model
m_h1 <- lmer(embu_c_reddetme_mean ~ role_f + (1 | aile_no_f),
              data = df_long_scored)

# Pinquart-tabanlı small effect (d = 0.20) için güç
m_h1_small <- m_h1
fixef(m_h1_small)["role_fDM_Hasta_Indeks"] <- 0.20

power_h1 <- simr::powerSim(m_h1_small,
                            test = fixed("role_fDM_Hasta_Indeks", "z"),
                            nsim = 1000)
print(power_h1)
# Beklenen: %95+ güç (n = 482, 4 grup, ICC ≈ 0.20)
```

| Etki | n_required (ICC = 0.15) | n_required (ICC = 0.30) |
|---|---|---|
| d = 0.20 | ~ 320 | ~ 540 |
| d = 0.30 | ~ 145 | ~ 240 |
| d = 0.40 | ~ 84 | ~ 140 |

> **Mevcut n = 482, beklenen ICC ≈ 0.15-0.20** → d = 0.20 için %92 güç, d = 0.30 için %99 güç.

### 16. SEM Sample Size — H4 ve H5

| Yaklaşım | Eşik | n_T1DM | Yeterli mi? |
|---|---|---|---|
| **N:p ≥ 5** (Bentler & Chou 1987) | minimum | 482 / 30 par = 16 | ✓ |
| **N:p ≥ 10** (Kline 2023) | tercih | 482 / 30 par = 16 | ✓ |
| **WLSMV küçük örneklem stability** | n ≥ 200 | 482 (full); 120 (DM-only) | ✓ full / ✗ DM-only |
| **Olsen-Kenny dyadic CFA** | n_dyad ≥ 100 | 241 dyad | ✓ |
| **RSA polynomial regresyon** | n ≥ 100 alt-grup | 120 (DM), 121 (Kontrol) | sınır → BCa CI zorunlu |

### 17. Type S ve Type M Hatalar (Gelman & Carlin 2014)

Düşük güçlü çalışmalar için **iki yeni hata tipi**:

- **Type S (sign):** Anlamlı bulgunun ters yöne çıkma olasılığı
- **Type M (magnitude):** Anlamlı bulgunun gerçek etkiyi büyütme oranı (exaggeration ratio)

```r
# T1DM tezi için retrodesign
library(retrodesign)

# Beklenen küçük etki + mevcut güç
retro <- retrodesign(A = 0.30, s = 0.10, df = 230)
print(retro)
# power, type_s, exaggeration
```

| Beklenen | Yorum |
|---|---|
| power > .80 | Type S < %1, exaggeration ≈ 1.0× |
| power = .50 | Type S ≈ %3, exaggeration ≈ 1.5× |
| power < .25 | Type S ≈ %20, exaggeration > 2× → **bulgu güvenilmez** |

> **Tezde uygulama:** H1-H4 için power > .90, Type S < %0.1, exaggeration < 1.05× (post-hoc retrodesign)
> raporlanır. KEŞİFSEL analizler için (KISIM VI-X) düşük güç riski vurgulanır.

### 18. Dyadic Power (H5 için Olsen-Kenny ICC)

Donner & Eliasziw (1992) ICC için minimum sample size:

| ICC | α | power | n_dyad |
|---|---|---|---|
| 0.20 | 0.05 | 0.80 | 195 |
| 0.30 | 0.05 | 0.80 | 87 |
| 0.50 | 0.05 | 0.80 | 33 |

T1DM tezi: **n_dyad = 241** (anne + indeks-çocuk) → ICC ≥ 0.20 için %85+ güç.

### 19. Hızlı Etki Büyüklüğü Çeviri Tablosu

Tezde sıkça lazım olan dönüşümler:

| Cohen's d | r | OR (yaklaşık) | %varyans (η²) |
|---|---|---|---|
| 0.10 | .05 | 1.20 | 0.5% |
| 0.20 | .10 | 1.44 | 1.0% |
| 0.30 | .15 | 1.72 | 2.2% |
| 0.50 | .24 | 2.48 | 5.9% |
| 0.80 | .37 | 4.50 | 13.8% |

```r
# d → r
r <- d / sqrt(d^2 + 4)

# d → OR (Chinn 2000)
OR <- exp(0.91 * d)

# r → d
d <- 2 * r / sqrt(1 - r^2)
```

> **Kural:** Tezin "Bulgular" kısmında etki büyüklüğü hep **orijinal birim** + **Cohen's d** (veya
> ω²) + **%95 GA** üçlüsü; çeviri tablosu yalnız *yorum* için, raporlama için değil.
