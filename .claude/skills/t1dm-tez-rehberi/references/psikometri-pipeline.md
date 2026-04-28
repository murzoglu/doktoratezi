# Psikometri Pipeline — EMBU-P/C, Beck (BDI), KİA (SRQ)

**Ne zaman oku:** Bir alt ölçek skoru kullanılmadan önce, alpha/omega raporlanırken, CFA
yapılırken, ölçüm değişmezliği test edilirken, IRT preflight planlanırken, EMBU/Beck/KİA
ile ilgili her psikometrik karar.

**Kaynaklar:** Brown (2015) *Confirmatory Factor Analysis for Applied Research*; DeVellis &
Thorpe (2022) *Scale Development*; Kline (2023) *Principles and Practice of SEM*; Lord & Novick
(klasik); Sümer (s-EMBU TR adaptasyonu); Furman & Buhrmester (1985); Apalaçi (1996, KİA TR
adaptasyonu); Beck (BDI); Hisli (BDI TR adaptasyonu).

---

## Temel İlke (DeVellis 2022 + Brown 2015)

> **Alpha tek başına yeterli değildir.** Alpha tau-eşdeğerlik varsayar (eşit yükler) — bu
> varsayım gelişimsel psikolojide nadiren tutar. Çok-faktörlü bir ölçek için alpha düşük
> tahmindir; tek-faktörlü ama heterojen yüklü bir ölçek için bile alpha şişebilir.

Bu projede her alt ölçek için **birinci atak ω, alpha ikinci sırada**.

> **Skor öncesi yapı doğrulanır.** s-EMBU-C için tarihsel alpha .49–.69 → CFA / ω önce yapılır;
> ancak yapı kabul edilebilirse alt ölçek skoru analiz değişkeni olarak kullanılır.

---

## Kanonik Ölçek Profili

### 1. EMBU-P (Anne Öz-Rapor, 29 madde, 4'lü Likert)

- **Alt ölçekler (4):** Sıcaklık (Warmth), Aşırı Koruma (Overprotection),
  Reddetme/Aşırı Sertlik (Rejection), Karşılaştırma (Comparison).
- **Ölçek doğası:** Reflektif (reflective). Skor = madde ortalamaları.
- **Türkçe adaptasyon kaynağı:** Sümer ve diğerleri (Karşılaştırma alt ölçeği orijinal
  s-EMBU'ya eklenmiştir → tam psikometrik yeniden doğrulama gerektirir).
- **Bilinen sorunlar:** Türk örnekleminde bazı maddelerde alt-grup Likert kayması; kanonik
  formdan önce karışım vardı (`archive/2026-04-26_pre_canonical_embu/` referansı). Final
  CSV'de bu kayma temizlenmiştir.

### 2. EMBU-C (Çocuk Algısı, 29 madde, 4'lü Likert)

- **Alt ölçekler:** EMBU-P ile semantik olarak hizalı (q01–q29 paraleldir).
- **Bilgi kaynağı:** İndeks çocuk + sağlıklı kardeş (long format).
- **Anne–çocuk konkordansı düşük olabilir** — multi-informant literatür normu (De Los Reyes
  ve diğerleri, 2015).

### 3. Beck Depresyon Envanteri (BDI, 21 madde, 0–3)

- **Tek faktörlü** (klasik Beck) veya iki-faktörlü (somatik-affektif vs. bilişsel; Beck 2.
  versiyondan beri tartışmalı).
- **Türkçe adaptasyon:** Hisli (1989).
- **Skor kuralı:** **Toplam 21 maddenin tamamı tamsa hesaplanır; herhangi bir eksik item
  toplamı NA bırakır.** (`R/10_derived_scores.R` bu kuralı sıkı uygular.)
- **Klinik kesim:** ≥17 hafif depresyon, ≥21 orta, ≥30 ağır (Türkiye normu).
- **Antidepresan kullanan anneler:** Total-effect modelde kovaryat yapılmaz; AD-stratifiye
  duyarlılık analizi (`h3_antidepressant_stratified_group_effects_table`).

### 4. Kardeş İlişkileri Anketi (KİA / SRQ, 48 madde, 5'li Likert)

- **Alt ölçekler (4):** Sıcaklık/Yakınlık (Warmth/Closeness), Statü/Güç (Status/Power),
  Çatışma (Conflict), Rekabet (Rivalry — anne ve baba kayırması ortalama).
- **Türkçe adaptasyon:** Apalaçi (1996); alpha .73–.90 aralığı.
- **Dyadic non-bağımsızlık:** Aynı dyad'daki iki kardeş bağımsız doldurur → APIM zorunlu
  (`references/multilevel-aile-yapisi.md`).
- **Olsen-Kenny distinguishable dyad CFA**: H2 analizinde quarrel item seti üzerinden
  index-kardeş latent korelasyonu raporlanır.

---

## Pipeline (8 Adımlı, Her Ölçek İçin)

### Adım 1: Tanımlayıcı Madde İstatistikleri

```r
library(psych)
library(tidyverse)

# EMBU-C için örnek
embu_c_items <- df_long_scored |>
  select(starts_with("embu_c_q"))   # q01..q29

describe(embu_c_items) |>
  as_tibble(rownames = "item") |>
  mutate(
    floor_pct = colMeans(embu_c_items == min(embu_c_items, na.rm = TRUE), na.rm = TRUE) * 100,
    ceil_pct  = colMeans(embu_c_items == max(embu_c_items, na.rm = TRUE), na.rm = TRUE) * 100
  )
```

**Kararlar:**
- |skewness| > 2 veya |kurtosis| > 7 → 4'lü Likert için sınırlı endişe verici (ordinal
  yorumla); WLSMV CFA bu sorunu yumuşatır.
- Floor/ceiling > %15 → madde varyans bilgisi az; CFA'da düşük yük beklenir.
- Madde eksiklik > %5 → wording/atlama sorunu olabilir; runbook'a not düş.

### Adım 2: Madde-Toplam Korelasyonu (CITC)

```r
alpha_result <- psych::alpha(embu_c_items, check.keys = TRUE)

alpha_result$item.stats |>
  as_tibble(rownames = "item") |>
  arrange(r.drop) |>
  print()

alpha_result$alpha.drop  # alpha-if-deleted
```

| CITC | Yorum | Aksiyon |
|------|-------|---------|
| ≥ .50 | Mükemmel | Tut |
| .30–.49 | İyi | Tut |
| .20–.29 | Sınırda | Düşür raporu, runbook'a not |
| < .20 | Zayıf | Madde-CFA tartışmasında ele al |

### Adım 3: Cronbach Alpha (Bağlam Olarak — Birincil Değil)

```r
psych::alpha(embu_c_items)$total$raw_alpha
```

Eşikler (DeVellis 2022):
- .70 araştırma (grup düzeyi)
- .80 uygulamalı/bireysel
- .90 yüksek-bahisli karar
- .60–.70 kısa tarama

**Bu projede asıl referans ω.**

### Adım 4: McDonald ω (Birincil Güvenilirlik)

```r
library(psych)
omega_result <- omega(embu_c_items, nfactors = 4, plot = FALSE)
omega_result$omega.tot   # ω_total
omega_result$omega_h     # ω_hierarchical (genel faktör payı)
```

Eşikler:
- ω_t ≥ .80 sağlam
- ω_t ≥ .70 araştırma için kabul
- ω_h / ω_t ≥ .70 → genel faktör baskın (bifaktör destekli)

### Adım 5: CFA — `lavaan` (Birincil Yapı Doğrulama)

#### EMBU-C 4-Faktör Modeli (Türkiye s-EMBU-C 29 madde)

```r
library(lavaan)

embu_c_model <- '
  warmth      =~ embu_c_q01 + embu_c_q02 + ... 
  rejection   =~ embu_c_q07 + embu_c_q08 + ...
  overprot    =~ embu_c_q15 + ...
  comparison  =~ embu_c_q23 + ...
'

# 4'lü Likert + ordinal → WLSMV
fit_embu_c <- cfa(
  embu_c_model,
  data       = df_long_scored,
  ordered    = grep("^embu_c_q", names(df_long_scored), value = TRUE),
  estimator  = "WLSMV",
  cluster    = "aile_no"   # aile-içi clustering için robust SE
)

summary(fit_embu_c, fit.measures = TRUE, standardized = TRUE)
fitMeasures(fit_embu_c, c("chisq", "df", "pvalue", "cfi", "tli",
                          "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
```

**Fit indeks eşikleri (Hu & Bentler 1999 + Kline 2023):**

| İndeks | Yakın Fit | Kabul | Kötü |
|--------|-----------|-------|------|
| CFI | ≥ .95 | ≥ .90 | < .90 |
| TLI | ≥ .95 | ≥ .90 | < .90 |
| RMSEA | ≤ .06 | ≤ .08 | > .10 |
| RMSEA Üst CI | < .08 | < .10 | ≥ .10 |
| SRMR | ≤ .08 | ≤ .10 | > .10 |
| χ²/df | < 2 | < 3 | ≥ 5 |

**ASLA tek bir indekse dayanma. Dört indeksi birlikte raporla.**

#### Beck BDI Tek Faktör vs. İki Faktör

```r
beck_one <- '
  bdi =~ beck_q01 + beck_q02 + ... + beck_q21
'

beck_two <- '
  somatic_affective =~ beck_q11 + beck_q12 + beck_q13 + ...
  cognitive         =~ beck_q01 + beck_q02 + beck_q03 + ...
'

fit1 <- cfa(beck_one, data = df_family_ses, ordered = paste0("beck_q", sprintf("%02d", 1:21)),
             estimator = "WLSMV")
fit2 <- cfa(beck_two, data = df_family_ses, ordered = paste0("beck_q", sprintf("%02d", 1:21)),
             estimator = "WLSMV")

compareFit(fit1, fit2)
# ΔCFI < .010 → tek faktör tercih edilir (parsimony)
```

#### KİA (SRQ) 4-Faktör

```r
kia_model <- '
  # Item-eşleşmesi `psychval_srq_subscale_map()` üzerinden alınır;
  # alt ölçek karşılıkları: warmth → ho_warmth, status → ho_status,
  # conflict → ho_conflict, rivalry → ho_rivalry (mother + father average).
  warmth   =~ srq_q01 + srq_q02 + srq_q03 + srq_q04 + ...
  status   =~ srq_q12 + srq_q13 + srq_q14 + ...
  conflict =~ srq_q22 + srq_q23 + srq_q24 + ...
  rivalry  =~ srq_q33 + srq_q34 + ...
'

fit_kia <- cfa(
  kia_model,
  data      = df_long_scored,
  estimator = "MLR",          # 5'li Likert + sürekli yaklaşım kabul edilebilir
  cluster   = "aile_no"
)
```

### Adım 6: Modifikasyon İndeksleri (DİKKATLİ)

```r
modindices(fit_embu_c, sort = TRUE, minimum.value = 10)
```

Brown (2015): MI > 10 olan tek bir parametreyi serbest bırakmak istatistiksel ihlali çözmez —
**teori gerektirir**. Cross-loading veya residual covariance eklersen runbook'ta gerekçe yaz.

### Adım 7: Ölçüm Değişmezliği (Multigroup)

```r
library(semTools)

# DM vs Kontrol
fit_config <- cfa(embu_c_model, data = df_long_scored,
                   group = "group_dm", estimator = "WLSMV", ordered = ...)

fit_metric <- cfa(embu_c_model, data = df_long_scored,
                   group = "group_dm", estimator = "WLSMV", ordered = ...,
                   group.equal = "loadings")

fit_scalar <- cfa(embu_c_model, data = df_long_scored,
                   group = "group_dm", estimator = "WLSMV", ordered = ...,
                   group.equal = c("loadings", "intercepts"))

fit_strict <- cfa(embu_c_model, data = df_long_scored,
                   group = "group_dm", estimator = "WLSMV", ordered = ...,
                   group.equal = c("loadings", "intercepts", "residuals"))

compareFit(fit_config, fit_metric, fit_scalar, fit_strict)
# ΔCFI < .010 ve ΔRMSEA < .015 → invariance HOLDS
```

**Karar zinciri (Cheung & Rensvold 2002 + Kline 2023):**

1. Configural FAIL → grup yapı sorunu, ortalama karşılaştırma yapma.
2. Metric FAIL → yükler farklı, korelasyon karşılaştırması da risksizken yapılamaz.
3. Scalar FAIL → ortalama karşılaştırma yapma (intercept biased).
4. Scalar HOLD → grup ortalaması karşılaştırılabilir.
5. Strict HOLD → tam invariance (genelde gereksiz katılık).

H4 modelinde hedef en az **metric** seviyeye ulaşmak. Scalar seviyeye ulaşılırsa duyarlılık
analizinde partial scalar test edilir.

### Adım 8: IRT (Birinci Aşamada Tamamlayıcı; H1'de Birincil)

```r
library(mirt)

# 4'lü Likert ordinal → graded response model (GRM)
irt_warmth <- mirt(
  data = df_long_scored |> select(matches("embu_c_q[0-9]+_warmth")),
  model = 1,
  itemtype = "graded",
  technical = list(NCYCLES = 2000)
)

# Madde parametreleri (a = ayırıcılık, b = eşik)
coef(irt_warmth, IRTpars = TRUE, simplify = TRUE)$items

# Theta (gizil yetenek) skoru
theta_warmth <- fscores(irt_warmth, method = "EAP")
df_long_scored$theta_warmth <- theta_warmth[, 1]

# Madde bilgi fonksiyonu
plot(irt_warmth, type = "info")
```

H1 multilevel modelinde theta skoru kovaryat olarak kullanılır (bkz. `R/16_h1_child_perception.R`).

---

## Beck Özel Durumu — Multinomial Item, Ordinal Skor

BDI maddeleri 0–3 ordinal skala — ama madde içerikleri farklı (örnek: 0 = "üzgün değilim",
3 = "o kadar üzgünüm ve mutsuzum ki dayanamıyorum"). Polikorik korelasyon WLSMV altında
uygundur. **Ancak madde 19 (kilo kaybı)** kategoriler arasında tek-yönde sıralı değil
(geleneksel Beck bunu eski versiyondan miras alır) — bu maddeye runbook'ta dikkat çek.

---

## Türetilmiş Skor Kuralları (Kanonik)

`R/10_derived_scores.R` üzerinden:

- **Alt ölçek toplamı:** Tüm itemlar mevcutsa hesaplanır. Tek eksik item → toplam NA.
- **Alt ölçek ortalaması:** Madde mevcutluğu ≥ %50 ise hesaplanır. Aksi halde NA.
- **Beck toplamı:** **Tüm 21 madde tam olmalı.** %50 kuralı UYGULANMAZ.
- **KİA Rekabet:** anne kayırması + baba kayırması ortalaması olarak hesaplanır.
- **Skor aralığı denetimi:** `score_range_audit()` her alt ölçek için min/max sınırlarını
  tarar; ihlal → `assert_no_score_range_violations()` hata fırlatır.

**Sonuç:** Türetilmiş skorlar kanonik CSV'ye yazılmaz; her yüklemede yeniden üretilir
(tez Yöntem bölümü kararı, `chapters/02_yontem.qmd`).

---

## Raporlama Sablonu (APA 7 Türkçe)

> "EMBU-C Sıcaklık alt ölçeği için iki-faktörlü WLSMV CFA modeli iyi uyum göstermiştir
> (χ²[35] = 48.2, p = .071, CFI = .978, TLI = .965, RMSEA = .045 [%95 GA: .000–.072],
> SRMR = .038). McDonald ω = .87 (95% GA [.84, .90]) güvenilirlik düzeyini desteklemiştir.
> DM ve kontrol grupları arasında configural ve metric değişmezlik karşılanmış (ΔCFI = .003,
> ΔRMSEA = .002), scalar değişmezlik kısmen kabul edilmiştir (ΔCFI = .008; q14 ve q22
> intercept'leri serbest bırakılmıştır). Bu nedenle alt ölçek ortalama karşılaştırmaları
> kısmi-scalar düzeyde yorumlanmıştır."

---

## Sık Yapılan Hatalar (Bu Projede)

1. **6'lı Likert varsayımı** — kanonik form 4'lüdür. Eski analiz raporları arşivde.
2. **q14, q21 gibi "tipo" değerleri ham veride** — Stage 1 (legacy) bunları NA yaptı; final
   CSV'de problemli madde yok ama yeni veri eklenirse aynı kontrol gerekli.
3. **PCA = faktör analizi varsaymak** — KESİNLİKLE FARKLI. Scale dev için PAF (`fm = "pa"`)
   veya ML; PCA yalnız veri redüksiyonu içindir (DeVellis 2022 Ch. 6).
4. **Modifikasyon indeksleriyle modeli "kurtarmak"** — Brown (2015) uyarısı: teori
   gerektirir. Sadece MI > 20 ve teorik gerekçesi olan parametreyi serbest bırak.
5. **Ölçek arası karşılaştırmadan önce invariance test etmemek** — DM ile kontrolün
   "EMBU-C Reddetme" ortalamasını karşılaştırmak için en az scalar HOLD gerekir.
6. **Beck'te %50 kuralını uygulamak** — kuraldışı; tüm 21 madde tam olmalı.
7. **EMBU-C alpha = .55 görünce skoru kullanmak** — alpha tek başına yetmez; CFA + ω + 
   invariance pipeline'ı bypass etme.

---

## Validasyon Belgeleri

`docs/analiz_planlari/`:

- `PSIKOMETRIK-VALIDASYON.md` — ana çalışma raporu
- `PSIKOMETRIK-VALIDASYON-BUTUNLESIK-RAPOR.qmd` — Quarto bütünleşik
- `PSIKOMETRIK-VALIDASYON-FINAL-ONERI.md` — final öneri
- `VALIDASYON-V2.md`, `V3.md`, `V4.md` — versiyon geçmişi

OSF: <https://osf.io/d524q/> (psikometrik validation reflective registration).
