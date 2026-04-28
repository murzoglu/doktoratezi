# Multilevel Modelleme ve Aile Yapısı — 241 Aile × 2 Katılımcı

**Ne zaman oku:** ICC hesabı, lme4/lmerTest seçimi, aile-clustered SE, APIM (aktör-partner)
modeli, Olsen-Kenny distinguishable dyad CFA, three-level model, group-mean centering, kardeş
yaş farkı moderasyonu.

**Kaynaklar:** Hox, Moerbeek & van de Schoot (2018) *Multilevel Analysis* (3rd ed.); Kenny,
Kashy & Cook (2006) *Dyadic Data Analysis*; Curran & Bauer (2011) — within/between
decomposition; Snijders & Bosker (2012) — power; Gelman, Hill & Vehtari (2021) Ch. 11–13;
McElreath (2020) Ch. 13–14 (partial pooling).

---

## Veri Yapısının Anatomisi

```
N = 482 satır = 241 aile × 2 katılımcı
                                     │
              ┌──────────────────────┼─────────────────────────┐
              │                      │                          │
       DM Aileleri              Kontrol Aileleri          Anne (aile düzeyi)
       n_aile = 120             n_aile = 121               n = 241
              │                      │
       (1 indeks + 1 kardeş)  (1 indeks + 1 kardeş)
              │                      │
       n_çocuk = 240          n_çocuk = 242
```

- **Geniş format** (`df_family`, `df_family_ses`): 1 satır/aile. Anne değişkenleri burada.
- **Uzun format** (`df_long`, `df_long_scored`): 2 satır/aile (indeks + kardeş). Çocuk
  değişkenleri burada.
- **Birincil aile anahtarı:** `aile_no`. Çocuk satırı için ek olarak `cocuk_no` (1 = indeks,
  2 = kardeş veya tam tersi — `R/01_io.R` ile fixed).
- **DM grup değişkeni:** `group_dm` (0 = kontrol aile, 1 = DM aile).
- **Çocuk rolü:** `role_f` factor — kanonik düzeyler: `Kontrol_Indeks`, `Kontrol_Kardes`,
  `DM_Hasta_Indeks`, `DM_Hasta_Kardes`. Referans seviye `Kontrol_Indeks`.
- **Grup faktörü:** `group_f` (`Kontrol`, `DM`); ham binary için `group_dm` (0/1) da
  bulunur, primer modellerde `group_f` tercih edilir.

---

## ICC: Multilevel Gerekli mi?

### Hesap

ICC = τ₀₀ / (τ₀₀ + σ²)

`lme4` ile:

```r
library(lme4)
library(performance)

# Çocuk DV için (uzun format)
m0 <- lmer(embu_c_sicaklik_mean ~ 1 + (1 | aile_no_f), data = df_long_scored,
            REML = TRUE)
performance::icc(m0)
# Tipik beklenen: .15–.40 (parenting algısı için yüksek paylaşım)
```

### Karar Eşiği

| ICC | Yorum | Aksiyon |
|-----|-------|---------|
| < .05 | Aile etkisi ihmal edilebilir | Tek-düzey OK; multilevel yine de çalış (test power için) |
| .05–.15 | Orta | Multilevel zorunlu |
| > .15 | Yüksek | Multilevel zorunlu + within/between decomposition düşün |

**Bu projede multilevel her durumda yapılır** çünkü ön-kayıtta sabittir; ICC raporlanır
ve karar mantığı runbook'ta gerekçelendirilir.

### Tasarım Etkisi (Hox 2018)

```
N_effective = N_total / (1 + (n_cluster - 1) × ICC)
```

Örnek: 482 satır, n_cluster = 2, ICC = .25 →
N_eff = 482 / (1 + 1 × .25) = 482 / 1.25 = 385.6.

Yani **bağımsız varsayımdan ~%20 daha az bilgi içerikli**. Tek-düzey t-test'i kullanırsan
Tip I hata enflasyonu ciddi.

---

## Hox Sample Size Kuralları (Bu Projeye Uygulamalı)

Bu projede:
- **Level-2 birim sayısı:** 241 aile → fixed effects için yeterli; random slopes için
  yeterli; cross-level interaction için MARGİNAL.
- **Level-1 birim/küme:** 2 (sabit) — minimum.

Hox uyarısı: küme-içi sayı az olduğunda REML + Kenward-Roger df kritik.

```r
library(lmerTest)
m1 <- lmer(embu_c_sicaklik_mean ~ group_dm + cocuk_yas_z + cinsiyet_f +
              (1 | aile_no_f), data = df_long_scored, REML = TRUE)
anova(m1, ddf = "Kenward-Roger")
```

---

## H1 — Çok Düzeyli Çocuk Algısı Modeli (Kanonik)

Birincil model (`R/16_h1_child_perception.R`):

```r
m_h1_primary <- lmer(
  embu_c_sicaklik_mean ~ role_f + cocuk_yas_z + cinsiyet_f +
                          ses_latent_z + age_gap_z + cocuk_sayisi_z +
                          (1 | aile_no_f),
  data = df_long_scored,
  REML = TRUE
)
```

Aynı formül üç EMBU-C alt ölçeği için de tekrar edilir (`embu_c_asiri_koruma_mean`,
`embu_c_reddetme_mean`, `embu_c_karsilastirma_mean`); H1 FDR (Benjamini-Hochberg) ailesi
dört outcome'ı kapsar.

`role_f` 4 düzeyli factor: `Kontrol_Indeks`, `Kontrol_Kardes`, `DM_Hasta_Indeks`,
`DM_Hasta_Kardes` (referans `Kontrol_Indeks`). Outcome seti H1 runbook'taki kanonik
isimlerle: `embu_c_sicaklik_mean`, `embu_c_asiri_koruma_mean`, `embu_c_reddetme_mean`,
`embu_c_karsilastirma_mean`.

Genişletme hattı:

```r
m_h1_three_way <- lmer(
  embu_c_sicaklik_mean ~ role_f * cocuk_yas_z * cinsiyet_f +
                       ses_latent_z + age_gap_z + cocuk_sayisi_z +
                       (1 | aile_no_f),
  data = df_long_scored,
  REML = TRUE
)

anova(m_h1_three_way, ddf = "Kenward-Roger")
```

**Karşılaştırmalar (`emmeans`):**

```r
library(emmeans)

emmeans(m_h1_primary, pairwise ~ role_f, adjust = "holm")
# Holm projektedeki çoklu karşılaştırma standardıdır (Bonferroni'ye göre güçlü).

# Cinsiyet × yaş etkileşim profili
emmip(m_h1_three_way, role_f ~ cocuk_yas_z | cinsiyet_f, CIs = TRUE)
```

**Etki büyüklüğü (multilevel için):**

```r
library(effectsize)
parameters::standardize_parameters(m_h1_primary)
# Etki büyüklüğü tablosunu raporla
```

---

## H2 — APIM (Actor-Partner Interdependence Model)

Kardeşler birbirini etkiler. Tipik APIM yapısı:

```
Predictor_self  → Outcome_self  (actor effect: a)
Predictor_partner → Outcome_self (partner effect: p)
```

### `lavaan` Distinguishable Dyad APIM

```r
library(lavaan)

# Geniş format gerekir (1 satır/aile, kolonlar index_ ve sibling_ ön ekli)
apim_model <- '
  # Actor effects
  index_srq_ho_warmth_mean   ~ a_index*index_srq_ho_conflict_mean
  sibling_srq_ho_warmth_mean ~ a_sib*sibling_srq_ho_conflict_mean

  # Partner effects
  index_srq_ho_warmth_mean   ~ p_index*sibling_srq_ho_conflict_mean
  sibling_srq_ho_warmth_mean ~ p_sib*index_srq_ho_conflict_mean

  # Residual covariance (paylaşılan aile bağlamı)
  index_srq_ho_warmth_mean ~~ sibling_srq_ho_warmth_mean

  # Predictor covariance
  index_srq_ho_conflict_mean ~~ sibling_srq_ho_conflict_mean

  # Eşitlik testleri (distinguishability)
  actor_diff   := a_index - a_sib
  partner_diff := p_index - p_sib
'

fit_apim <- sem(apim_model, data = df_dyad, missing = "FIML")
summary(fit_apim, standardized = TRUE, fit.measures = TRUE)
```

**Yorum:**
- `actor_diff` ≈ 0 → roller arasında actor etkisi ayırt edilemiyor (pooled aktör mümkün).
- `partner_diff` ≠ 0 → DM indeks çocuğun çatışma puanı kardeş çıktısını farklı düzeyde
  öngörür (rolspesifik partner etkisi).

### `lme4` ile APIM-benzeri Karma Model

```r
m_h2_apim <- lmer(
  srq_ho_warmth_mean ~ group_f * family_role_f +
                        srq_ho_conflict_mean_partner +
                        age_gap_z + same_sex +
                        (1 | aile_no_f),
  data = df_long_scored,
  REML = TRUE
)
```

`family_role_f` (indeks/kardeş) ile `group_f` (DM/kontrol) etkileşimi her dört rol için
ayrı ortalama tahmin verir.

---

## H2 Olsen-Kenny Distinguishable Dyad CFA

```r
library(lavaan)

# Quarrel item seti
ok_model <- '
  index_quarrel   =~ index_srq_q1   + index_srq_q2   + index_srq_q3
  sibling_quarrel =~ sibling_srq_q1 + sibling_srq_q2 + sibling_srq_q3

  # Yük eşitliği (distinguishability test)
  index_quarrel   =~ NA*index_srq_q1   + l1*index_srq_q1   + l2*index_srq_q2   + l3*index_srq_q3
  sibling_quarrel =~ NA*sibling_srq_q1 + l1*sibling_srq_q1 + l2*sibling_srq_q2 + l3*sibling_srq_q3

  # Latent korelasyon — ölçüm hatasından arındırılmış
  index_quarrel ~~ sibling_quarrel

  index_quarrel   ~~ 1*index_quarrel
  sibling_quarrel ~~ 1*sibling_quarrel
'

fit_ok <- cfa(ok_model, data = df_dyad, estimator = "MLR")
summary(fit_ok, standardized = TRUE, fit.measures = TRUE)
```

Bu raporlama H2 sonuçlarında index–sibling latent korelasyonunu ham korelasyondan ayırır;
ölçüm hatası nedeniyle ham korelasyon altında kalan gerçek ilişkiyi ortaya çıkarır.

---

## H3 — Aile Düzeyinde ANCOVA

Anne öz-rapor (EMBU-P) → 1 satır/aile → multilevel zorunlu değil ama IPTW ile twinned:

```r
m_h3 <- lm(
  embu_p_subscale_z ~ group_dm + anne_yas_z + ses_latent_z + age_gap_z + cocuk_sayisi,
  data = df_family_ses
)

# IPTW versiyonu
library(survey)
des <- svydesign(ids = ~aile_no, weights = ~iptw_trimmed, data = df_family_propensity)
m_h3_iptw <- svyglm(embu_p_subscale_z ~ group_dm + anne_yas_z + ses_latent_z, design = des)

# Robust SE (HC3)
library(sandwich); library(lmtest)
coeftest(m_h3_iptw, vcov = sandwich::vcovHC(m_h3_iptw, type = "HC3"))
```

---

## Centering Stratejisi (Hox 2018 + Curran & Bauer 2011)

### Grand-Mean Centering (GMC)

`X_gmc = X - mean(X)` — tüm örneklem ortalaması.

```r
df_long_scored <- df_long_scored |>
  mutate(cocuk_yas_z = scale(cocuk_yas)[, 1])  # GMC + scale
```

### Group-Mean Centering (CWC)

`X_cwc = X - aile_mean(X)` — aile içi sapma.

```r
df_long_scored <- df_long_scored |>
  group_by(aile_no_f) |>
  mutate(
    embu_c_aile_mean    = mean(embu_c_sicaklik_mean, na.rm = TRUE),
    embu_c_aile_kayma   = embu_c_sicaklik_mean - embu_c_aile_mean
  ) |>
  ungroup()

m_within_between <- lmer(
  outcome ~ embu_c_aile_kayma + embu_c_aile_mean + (1 | aile_no_f),
  data = df_long_scored
)
```

Bu, **within-family** ve **between-family** etkileri ayrıştırır — ekolojik yanılgıyı
önler. **H1 modelinde varsayılan strateji:** GMC (ön-kayıt). Within/between decomposition
duyarlılık analizi olarak yürütülür.

---

## Aile-Clustered Robust SE

Multilevel mümkün değilse (örn. tek-düzey OLS gerekiyorsa):

```r
library(sandwich)
library(lmtest)

m_ols <- lm(outcome ~ predictor, data = df_long_scored)
coeftest(m_ols, vcov = vcovCL(m_ols, cluster = ~aile_no_f, type = "HC3"))
```

`type = "HC3"` küçük örneklemde tercih edilir (Long & Ervin 2000).

---

## Üç-Düzey Yapı (Anne–Dyad)

Eğer anne ve çocuk aynı tabloya birleştirilirse:

```
Level 3: Aile (n=241)
  Level 2: Katılımcı tipi (anne / dyad)
    Level 1: Madde-tepki (uzun-uzun format)
```

Bu projede `df_family_ses` 1 satır/aile, `df_long_scored` 2 satır/aile — anne ve çocuk
ayrı dataset'lerdedir; üç-düzey nadiren gerekir. SEM'de anne ve çocuk değişkenlerini
geniş formatta tutmak daha pratik.

---

## Sample Size ve Güç (Hox + simr)

### Analitik Yaklaşım (Snijders & Bosker)

n_2 (Level-2 küme sayısı) = 241 ✓ (tipik kural ≥ 30, daha sağlam ≥ 100)
n_1 (küme başına) = 2 — minimum; bu küçük küme tasarımı yüksek güç için yüksek ICC ister.

### simr ile Simülasyon

```r
library(simr)

# Mevcut model
m_pilot <- lmer(outcome ~ group_dm + (1 | aile_no_f), data = df_long_scored, REML = FALSE)

# 1000 simülasyon ile güç
power_h1 <- powerSim(m_pilot, nsim = 1000, test = fixed("group_dm"))
print(power_h1)

# Eğer güç < .80, n_aile büyütme gerekiyor
extend_h1 <- extend(m_pilot, along = "aile_no_f", n = 300)
powerSim(extend_h1, nsim = 1000)
```

`pwrss` paketi mediation/APIM güç hesabı için ek seçenek.

---

## Aile-İçi Korelasyon Yapıları (Compound Symmetry vs Unstructured)

Random intercept = compound symmetry. Eğer indeks ve kardeş varyansı farklıysa unstructured:

```r
# Random intercept + slope (cocuk_no üzerinden)
m_cs <- lmer(outcome ~ predictor + (1 | aile_no_f), data = df_long_scored)
m_us <- lmer(outcome ~ predictor + (1 + cocuk_no_f | aile_no_f), data = df_long_scored)

anova(m_cs, m_us)
# Anlamlı iyileşme → varyans heterojenliği var
```

**Bu projede:** CS varsayım edilir, ancak H2 APIM içinde varyans heterojenliği zaten
distinguishable dyad çerçevesiyle yakalanır.

---

## Sık Yapılan Hatalar (Multilevel-Spesifik)

1. **Tek-düzey t-test ile DM vs kontrol kıyası** — aile-içi ICC ihlal eder; SE düşer,
   p-değeri sahte düşer.
2. **`(1 | aile_no)` yerine `(1 | aile_no_f)` ihmali** — `aile_no` numerik olabilir, factor
   olarak verirsin.
3. **REML = FALSE ile model karşılaştırma yapmak ama final raporlamada REML = TRUE
   kullanmamak** — fixed effect tahminleri için REML doğru, ML ise random effect
   karşılaştırması için.
4. **Kenward-Roger df'i ihmal etmek** — küçük örneklem (Level-2 < 50) durumunda
   Satterthwaite yetmez.
5. **Standardize edilmemiş sürekli kovaryatlar** — multilevel'de yorum güçleşir; tüm
   sürekli kovaryatları `_z` (standardize) ile yeniden adlandır.
6. **APIM'de partner etkisi unutmak** — Kenny (2006) uyarısı: tek aktör ile çalışmak,
   etkileşimi gizler.
7. **Distinguishability testini atlamak** — Olsen-Kenny çerçevesinde indeks ve kardeş
   "rol-bağımlı" mı yoksa exchangeable mi öncelikli karar.
8. **`emmeans` ortalamalarını ham veri ortalamalarıyla karıştırmak** — `emmeans`
   model-tabanlı (kovaryatlar sabitlenmiş); raw mean ≠ EMM, bu farkı raporda açıkla.

---

## Türkçe APA Sablonu

> "Aile düzeyinde sınıf-içi korelasyon ICC = .19 (95% GA [.10, .29]) hesaplanmış ve
> Hox (2018) eşiği olan .05'in üzerinde olduğundan rastgele aile-kesişim modeli zorunlu
> görülmüştür. Birincil model (intercept + grup + yaş + cinsiyet + SES + yaş farkı + kardeş
> sayısı + (1 | aile_no_f); REML, Kenward-Roger df) DM grubunun EMBU-C Sıcaklık alt ölçek
> ortalamasını kontrole göre β = −0.18 (SE = 0.07, t(232.4) = −2.55, p = .011, β_std =
> −0.21 [−0.37, −0.05]) düzeyinde düşük öngörmüştür."
