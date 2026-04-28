# Nedensellik, Causal DAG ve Propensity Score

**Ne zaman oku:** Kovaryat seçimi yapılırken, "şu değişken kontrol edilmeli mi?" sorusu
sorulduğunda, IPTW kurulurken, 1:1 matching uygulanırken, sensemakr ile sensitivity
yapılırken, "neden olur" mu yoksa "ilişkili" mi sorusunda, ön-kayıttaki nedensel
dilbilgisi sorgulanırken.

**Kaynaklar:** Pearl, Glymour & Jewell (2016) *Causal Inference in Statistics: A Primer*;
Hernán & Robins (2020) *Causal Inference: What If*; Gelman, Hill & Vehtari (2021) Ch. 18–21;
Kline (2023) *SEM* Ch. 6 (DAGs); Cinelli & Hazlett (2020) — sensemakr; VanderWeele (2015)
*Explanation in Causal Inference*; Stuart (2010) — propensity score.

---

## Temel İlke

**Bu çalışma OLGULU-KONTROL gözlemsel çalışmadır.** RCT değil. "Diyabet kazanma" rastgele
atanamaz → etki tahmini için **DAG-temelli kovaryat seçimi + propensity score (PS)
ayarlaması + duyarlılık analizi** üçlüsü zorunlu.

Gelman 2021 mantra: **regresyon katsayısı bir karşılaştırmadır, bir etki değildir.**
"DM grubunda EMBU-P Reddetme'nin 0.20 SD daha yüksek olması," sadece "DM grubunda
karşılaştırmalı olarak öyle gözlemlendiği"ni söyler — DM'nin reddetmeyi *yarattığını* değil.

---

## Causal DAG Yapımı (`R/14_causal_dag.R`)

### Düğümler

```
group_dm  → ses_latent → maternal_education
              ↓
maternal_age              → child_age
                                 ↓
ses_latent → embu_p_sicaklik_mean ← parental_strain
                  ↓                 ↑
            embu_c_sicaklik_mean         beck_total
                  ↓
            child_outcome (e.g., adjustment, sibling rivalry)
```

`build_causal_dag()` fonksiyonu bu yapıyı `dagitty` formatında üretir.

### Kenar Kategorileri

| Tip | Tanım | DAG'da | Aksiyon |
|-----|-------|--------|---------|
| **Confounder** | Hem X'i hem Y'yi etkiler (ortak ata) | `C → X`, `C → Y` | Kontrol et |
| **Mediator** | X → M → Y zincirinde | `X → M`, `M → Y` | KONTROL ETME (total effect istiyorsan) |
| **Collider** | X ve Y'nin ortak çocuğu | `X → C`, `Y → C` | KONTROL ETME |
| **Backdoor** | X'in dışından Y'ye giden yol | `X ← Z → Y` | Kapat (kontrol et) |
| **Mediating Confounder** | Pre-X confounder + post-X mediator | `Z → X → M → Y` | Front-door veya G-methods |

### Bu Projedeki Kararlar

`docs/analiz_planlari/CAUSAL-DAG-RUNBOOK.md` üzerinden:

- **Baseline confounders (kontrol edilir):** SES (latent), kardeş yaş farkı, aile büyüklüğü,
  anne yaşı, çocuk yaşı, çocuk cinsiyeti.
- **Mediator (kontrol edilmez total effect modelinde):** EMBU-P (anne öz-rapor) → EMBU-C
  (çocuk algısı) zincirinde EMBU-P, EMBU-C → outcome modelinde mediator. Mediation
  analizinde ayrı kullanılır.
- **Antidepresan kullanımı (potansiyel post-treatment):** total-effect modelde
  ayarlanmaz; AD-stratifiye duyarlılık ile incelenir (`h3_antidepressant_stratified_*`).
- **Beck depresyon (mediator hattında):** group_dm → maternal stress → beck_total →
  parenting → child outcome. Total effect modelde kovaryat YAPILMAZ; H4 SEM modeli içinde
  doğrudan latent yapı olarak ele alınır.

### Backdoor Adjustment Set

```r
library(dagitty)
g <- dagitty('
dag {
  group_dm -> embu_p_sicaklik_mean
  ses_latent -> group_dm
  ses_latent -> embu_p_sicaklik_mean
  maternal_age -> group_dm
  maternal_age -> embu_p_sicaklik_mean
  age_gap -> embu_p_sicaklik_mean
  cocuk_sayisi -> embu_p_sicaklik_mean
}')

adjustmentSets(g, exposure = "group_dm", outcome = "embu_p_sicaklik_mean", type = "minimal")
```

Çıktı: `{ses_latent, maternal_age, age_gap, cocuk_sayisi}` minimum yeterli set.

`causal_dag_adjustment_sets_table` her hipotez (H1–H4) için bu seti kayda alır.

### Conditional Independencies

```r
impliedConditionalIndependencies(g)
```

Bu, DAG'ın test edilebilir kısıtlarını verir. `causal_dag_conditional_independencies_table`
karşılığını veriden test eder; ihlal varsa DAG yanlış spec edilmiştir.

---

## Propensity Score Pipeline (`R/15_propensity_score.R`)

### Adım 1: PS Modeli (Logit)

```r
library(WeightIt)

ps_model <- WeightIt::weightit(
  group_dm ~ ses_latent + age_gap + cocuk_sayisi + maternal_age + cinsiyet,
  data = df_family_ses,
  method = "ps",
  estimand = "ATT"     # Average Treatment Effect on the Treated (DM grubu için)
)
summary(ps_model)
```

`estimand` seçimi:
- **ATT** (treated): DM hastalarında parenting etkisini istiyorsan
- **ATE** (whole population): tüm popülasyonda olsa
- **ATC** (control): kontrolde olsa

Bu projede **ATT** kanonik karar (DM hasta-spesifik etkiyi vurgular).

### Adım 2: Stabilized IPTW + 99. Persentil Trim

```r
# Stabilized weights (Robins, Hernan, Brumback 2000)
w_stab <- ps_model$weights * mean(df_family_ses$group_dm) / 
          (df_family_ses$group_dm * ps_model$ps + 
           (1 - df_family_ses$group_dm) * (1 - ps_model$ps))

# Trim
w_99 <- quantile(w_stab, 0.99)
df_family_ses$iptw_trimmed <- pmin(w_stab, w_99)

# Effective sample size
sum(df_family_ses$iptw_trimmed)^2 / sum(df_family_ses$iptw_trimmed^2)
```

`propensity_weight_summary_table` ağırlık dağılımını raporlar (median, IQR, max, ESS).

### Adım 3: Balance Diagnostics (`cobalt`)

```r
library(cobalt)

bal.tab(ps_model, m.threshold = 0.10, abs = TRUE)
# SMD < 0.10 → kabul; 0.10–0.25 → marginal; > 0.25 → fail

love.plot(ps_model, threshold = 0.10, abs = TRUE)
# Her kovaryat için before/after SMD
```

`propensity_balance_before_after_table` bunu kayda alır. SMD eşiği bu projede **.10**.

### Adım 4: 1:1 Nearest-Neighbor Matching (Alternatif)

```r
library(MatchIt)

m_match <- matchit(
  group_dm ~ ses_latent + age_gap + cocuk_sayisi + maternal_age,
  data    = df_family_ses,
  method  = "nearest",
  caliper = 0.20,           # 0.20 × SD(logit PS) — Austin (2011) kuralı
  distance = "logit"
)

summary(m_match)
df_matched <- match.data(m_match)
```

Caliper'ın 0.20 × SD ihlali halinde eşleşme dropped olur — bu projede DM = 120 + 121 kontrol
nicelik açısından genelde hepsini eşleştirebilir; eşleşmeyen vakalar `propensity_overlap_summary_table`
içinde belgelenir.

### Adım 5: Doubly Robust Estimation

```r
# Hem PS ağırlığı hem outcome regression
library(survey)
des_iptw <- svydesign(ids = ~aile_no, weights = ~iptw_trimmed, data = df_family_ses)

m_dr <- svyglm(
  embu_p_sicaklik_mean_z ~ group_dm + ses_latent + age_gap + cocuk_sayisi + maternal_age,
  design = des_iptw,
  family = gaussian()
)
summary(m_dr)
```

Doubly robust: PS modeli ya da outcome modeli birinden biri doğruysa, tahmin tutarlıdır
(Robins, Rotnitzky, Zhao 1994). `propensity_doubly_robust_plan_table` bu kombinasyonu
hipotez bazlı planlar.

---

## Duyarlılık Analizi — `sensemakr`

Cinelli & Hazlett (2020) Robustness Value:

```r
library(sensemakr)

m_h3 <- lm(embu_p_sicaklik_mean_z ~ group_dm + ses_latent_z + age_gap_z + cocuk_sayisi,
           data = df_family_ses)

s <- sensemakr(
  model = m_h3,
  treatment = "group_dm",
  benchmark_covariates = "ses_latent_z",
  kd = 1:3                # 1×, 2×, 3× SES gücünde unmeasured confounder
)

summary(s)
plot(s)
```

**Robustness Value (RV):** Tahmini sıfıra getirmek için unmeasured confounder'ın hem
treatment hem outcome ile ne kadar ilişki kurması gerektiği. RV ≥ %20 → bulgu
"unmeasured confounding"e çok dayanıklı.

**Yorum:** "DM grup etkisi (β_std = −0.21) için Robustness Value = 0.18; tahmini sıfıra
düşürmek için ölçülmeyen bir confounder'ın hem grup atanmasını hem de Reddetme alt ölçeğini
%18'in üzerinde açıklaması gerekirdi."

---

## Multiverse / Specification Curve — `specr`

Steegen ve diğerleri (2016) + Simonsohn ve diğerleri (2020):

```r
library(specr)

specs <- setup(
  data = df_family_ses,
  y    = c("embu_p_sicaklik_mean_z", "embu_p_asiri_koruma_mean", "embu_p_reddetme_mean"),
  x    = "group_dm",
  controls = c("ses_latent_z", "age_gap_z", "cocuk_sayisi"),
  model = "lm"
)

results <- specr(specs)
plot(results)
```

Tüm makul spesifikasyon kombinasyonlarında tahmin dağılımını gösterir. **Bu projede
sensitivity raporunun parçası.**

---

## TOST Eşdeğerlik Testi — `TOSTER`

Anlamlı olmayan bir t-test "etki yoktur" demek değildir. TOST ile eşdeğerlik test edilir:

```r
library(TOSTER)

# DM ile kontrol arasında EMBU-C Sıcaklık'ta %20 SD'lik fark "yok hükmündedir" mi?
TOSTtwo(
  m1 = mean(df_long_scored$embu_c_sicaklik_mean_ort[df_long_scored$group_dm == 1], na.rm = TRUE),
  m2 = mean(df_long_scored$embu_c_sicaklik_mean_ort[df_long_scored$group_dm == 0], na.rm = TRUE),
  sd1 = sd(df_long_scored$embu_c_sicaklik_mean_ort[df_long_scored$group_dm == 1], na.rm = TRUE),
  sd2 = sd(df_long_scored$embu_c_sicaklik_mean_ort[df_long_scored$group_dm == 0], na.rm = TRUE),
  n1 = sum(df_long_scored$group_dm == 1),
  n2 = sum(df_long_scored$group_dm == 0),
  low_eqbound_d = -0.20,
  high_eqbound_d = 0.20,
  alpha = 0.05
)
```

Eğer "anlamlı fark yok" sonucuna ulaşıyorsan **TOST'u da raporla** — yoksa "fail to reject"
"eşittir" hatasına düşersin.

---

## H1–H4 Hipotezlerine Eşleme

| Hipotez | Tahmin Yaklaşımı | Birincil Spec | Duyarlılık |
|---------|------------------|---------------|------------|
| **H1** Çocuk algısı | Multilevel + DAG-adjusted | `role_f + cocuk_yas_z + cinsiyet_f + ses_latent_z + age_gap_z + cocuk_sayisi_z + (1\|aile_no_f)` | IRT theta replikasyonu, three-way interaction, Bayesian preflight |
| **H2** Kardeş ilişkisi | Aile-mean Welch + APIM | APIM lme4 + Olsen-Kenny CFA | Yaş farkı moderasyonu |
| **H3** Anne öz-rapor | ANCOVA + IPTW + AD strata | DAG-adjusted ANCOVA | IPTW + AD-stratifiye + sensemakr |
| **H4** Beck → Parenting | WLSMV ordinal SEM | Beck (latent) → EMBU-P (4 latent) | Multigroup invariance + blavaan plan |

---

## Türkçe APA Sablonu

> "Diyabet grup etkisinin ölçülmemiş karıştırıcılara duyarlılığı sensemakr çerçevesi
> (Cinelli & Hazlett, 2020) ile değerlendirilmiştir. SES bağıl gücünde 1×, 2× ve 3× kuvvete
> sahip ölçülmemiş bir karıştırıcının tahmini etkiyi sıfıra çekme olasılığı düşük
> bulunmuş; Robustness Value %18.4 (95% GA: 13.2–24.1) olarak hesaplanmıştır. Bu, ölçülmeyen
> bir karıştırıcının hem grup atamasını hem de EMBU-P Reddetme alt ölçeğini ortak SES'in
> ötesinde %18'in üzerinde açıklaması durumunda bulgunun değişebileceğini göstermektedir.
> Ön-kayıttaki birincil yorum (`osf.io/pytfe`) bu duyarlılık eşiği üzerinden teyit
> edilmiştir."

---

## Sık Yapılan Hatalar (Bu Projede)

1. **Mediator'ı confounder gibi kontrol etme** — beck_total'i total-effect modelde
   kovaryat yapma; H4'te latent yapı olarak ele al.
2. **Antidepresan kullanımını kontrol etme** — post-treatment olabilir; total-effect modelde
   AD ayarlanmaz, ayrıca strata.
3. **Yaş farkını DAG dışında "kontrol etmek mantıklı" diyerek eklemek** — DAG'ta varsa
   ekle, yoksa ekleme. Karar runbook'ta gerekçeli.
4. **PS modelinde outcome'u predictor yapmak** — yasak; sadece pre-treatment kovaryatlar.
5. **IPTW'yi trim'siz uygulamak** — uçtaki ağırlıklar varyansı patlatır; 99. persentil trim
   bu projenin standardı.
6. **SMD < 0.25 ile yetinmek** — bu proje **0.10** eşiği uygular (klinik tezler için
   yaygın daha sıkı standart).
7. **Sensemakr'ı atlamak** — gözlemsel çıkarımda RV raporu standart.
8. **TOST'u atlamak** — "anlamlı fark yok"u "yok" olarak yorumlamak.
9. **Multiverse'ü "çok karmaşık" diye ihmal etmek** — `specr` çalıştırılır; sonuç tek
   bir grafik.
10. **DAG'ı tek seferde donduruyorum sanmak** — runbook'ta yeni bilgi gelirse DAG
    güncellenir, ama her güncelleme `PRE-REGISTRATION-DEVIATION-TABLE.md`'ye yazılır.
