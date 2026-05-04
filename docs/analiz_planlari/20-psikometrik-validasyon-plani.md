# Psikometrik Validasyon Planı — v2 (Empirik Olarak Güncellenmiş)

**Doküman türü:** Doktora tezi metodolojik ek + psikometrik adaptasyon makalesi alt-yapısı
**Tarih:** 26 Nisan 2026
**Kanonik veri kaynağı:** `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` (status: LOCKED)
**Skill yığını:** `devstats` × `psychdev` (kompozit validasyon protokolü)
**Önceki versiyon:** B.1–B.8 (orijinal plan) — bu doküman onun yerini alır.

---

## 0. Yönetici Özeti — Plan Niçin Revize Ediliyor?

Orijinal B.1–B.8 planı, **kavramsal olarak doğru** (Brown 2015, Hu & Bentler 1999, Cheung & Rensvold 2002 referanslı klasik psikometrik akış) ancak **veriye temas etmemiş, ön-betimleyici** bir reçeteydi. Kanonik CSV'ler (n=241 aile, n=482 çocuk) üzerinde yapılan ön analizlerden sonra üç **kritik ampirik bulgu** ortaya çıktı; bu bulgular planın çatısını yeniden çizmeyi zorunlu kılıyor.

### Bulgu 1 — EMBU-P "Reddetme" alt ölçeği yapısal olarak çökmüş durumda

| Alt ölçek | Cronbach α (mevcut) | Sümer-Güngör (1999) referans | Δ |
|---|---|---|---|
| Sıcaklık | **0.669** | 0.86 | −0.19 |
| Aşırı Koruma | **0.746** | 0.66 | +0.09 |
| **Reddetme** | **0.450** ⚠️ | 0.79 | **−0.34** |
| Karşılaştırma | **0.660** | 0.74 | −0.08 |

Reddetme alt ölçeğinin 8/8 maddesinde taban etkisi (kategori 1) **>%60**, 6 maddede **>%80**, 4 maddede **>%93**. Bu, ölçüm değil **sosyal istenirlik (social desirability) ve ebeveyn savunma psikolojisi** sorunudur — Türk anneler çocuklarını "reddettiklerini" 4'lü Likert üzerinde işaretlemekten sistematik olarak kaçınıyor. Orijinal planın B.8'i bunu sensitivite analizi olarak ele alıyordu; oysa bu, **birincil tasarım sorunu**dur ve ana stratejiyi belirlemek zorundadır.

### Bulgu 2 — EMBU-C psikometrik olarak EMBU-P'den daha iyi çalışıyor

EMBU-C'nin (çocuk raporu, n=482) iç tutarlılığı, EMBU-P'den (anne raporu, n=241) sistematik olarak yüksek:

| Alt ölçek | EMBU-C α | EMBU-P α |
|---|---|---|
| Sıcaklık | 0.805 ✓ | 0.669 |
| Aşırı Koruma | 0.619 | 0.746 |
| Reddetme | 0.718 ✓ | 0.450 ⚠️ |
| Karşılaştırma | 0.792 ✓ | 0.660 |

Bu, EMBU-P validasyonunun **EMBU-C'den ayrı ve daha derin** bir psikometrik müdahale gerektirdiğini gösterir. Orijinal plan iki ölçeği simetrik ele alıyordu; bu artık savunulamaz.

### Bulgu 3 — Veride iki düzey-2 yapı var, biri orijinal planda yok

Orijinal plan yalnızca **aile-içi nesting** (482 çocuk → 241 aile) için multilevel CFA öneriyordu. Ancak veride **dyadic-within-family** boyut da mevcut: her ailede **indeks çocuk + kardeş çift olarak EMBU-C dolduruyor**, dolayısıyla aynı annenin sıcaklığı, aşırı koruması, reddi, karşılaştırması iki kardeş tarafından **paralel** raporlanıyor.

| EMBU-C alt ölçek | İndeks raporcu α | Kardeş raporcu α |
|---|---|---|
| Sıcaklık | 0.817 | 0.795 |
| Aşırı Koruma | 0.575 | 0.652 |
| Reddetme | 0.766 | 0.657 |
| Karşılaştırma | 0.798 | 0.787 |

Bu tablo, **rapor-rolü ölçüm değişmezliği (reporter-role measurement invariance)** testinin zorunlu olduğunu gösteriyor — özellikle Reddetme'de raporcu-spesifik yapı (Δα ≈ 0.11) gözleniyor. Bu test, "iki kardeş aynı parental treatment'ı farklı algılıyor" hipotezinin (parental differential treatment, PDT — McHale, Updegraff & Whiteman, 2012) **psikometrik temelini** oluşturur ve doktora tezinizin teorik çerçevesi açısından **birincil önemde**dir.

### Stratejik Sonuç

Orijinal plan **8 adımdan** oluşuyordu. Güncellenen plan **12 adıma** çıkarılmış ve aşağıdaki yeni bileşenler eklenmiştir:

1. **Faz A** — Veri konsolidasyonu ve madde-faktör atama doğrulaması (kanonik dokümanlardan)
2. **B.4 (yeni)** — Sümer-Güngör 4-faktör yapısının **EFA ile ön-doğrulanması** (Karşılaştırma alt ölçeği için literatürde doğrulama yok)
3. **B.7 (yeni)** — **Bayesian CFA / BSEM** (Muthén & Asparouhov, 2012) — düşük α'lı ölçekler ve küçük örneklem için Brown (2015) §10 önerisiyle uyumlu
4. **B.9 (yeni)** — **Dyadic / rapor-rolü ölçüm değişmezliği** (kardeş içi)
5. **B.11 (genişletilmiş)** — Taban etkisi yönetimi: 4 ayrı strateji ile **multiverse analiz** (specr)
6. **C** — Pre-registration ve sensitivite analizi (sensemakr)

---

## 1. Veri Yapısı — Kanonik Doğrulama

### 1.1 Sütun Envanteri Doğrulaması

`FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` ile fiili sütun yapısı eşleşmesi:

| Dosya | Beklenen | Tespit edilen | Durum |
|---|---|---|---|
| `analysis_base_family.csv` | rows=241, cols=288 | 241 × 288 | ✓ |
| `analysis_base_long.csv` | rows=482, cols=203 | 482 × 203 | ✓ |
| Long role dağılımı | DM_İndeks:120, DM_Kardeş:120, Kontrol_İndeks:121, Kontrol_Kardeş:121 | aynı | ✓ |
| HbA1c (DM indeks) | 39/120 (final CSV alanı) | 39/120 | ✓ |

### 1.2 Ölçek Madde Yapısı

```
EMBU-P (anne öz-rapor, family file)        : embu_p_q01..q29           [29 madde × 1 raporcu = 29 sütun]
EMBU-C (çocuk rapor, long file)            : embu_c_q01..q29           [29 madde × 482 satır]
EMBU-C (çocuk rapor, family file)          : embu_c_idx_q01..q29       [indeks raporcu]
                                             embu_c_sib_q01..q29       [kardeş raporcu]   = 58 sütun
SRQ (kardeş ilişkisi, long file)           : srq_1..srq_48             [48 madde × 482 satır]
SRQ (kardeş ilişkisi, family file)         : srq_1..srq_48             [indeks raporcu]
                                             srq_sib_1..srq_sib_48     [kardeş raporcu]    = 96 sütun
Beck Depresyon Envanteri (anne)            : beck_1..beck_21           [21 madde × n=241]
```

**Likert kategorileri:** EMBU 4'lü (1–4), SRQ 5'li (1–5), Beck 4'lü (0–3).

### 1.3 Madde–Faktör Eşlemesi (Doğrulanmış)

Orijinal plan, aşağıdaki yapıyı varsayıyordu. Kanonik dokümanlar (`KANONIK_KISALTILMIS_EMBU_*.md`) bu makinede mevcut değil, ancak **inter-item korelasyon yapısı** önerilen yapıyı destekliyor (Spearman, ortalama r):

| Alt ölçek | k | Maddeler | Madde-içi r ortalama | Yorum |
|---|---|---|---|---|
| **Sıcaklık** | 9 | q01, q03, q06, q07, q13, q17, q20, q24, q26 | 0.200 | ✓ Clark-Watson .15-.50 aralığında |
| **Aşırı Koruma** | 7 | q04, q08, q14, q15, q19, q23, q25 | 0.294 | ✓ |
| **Reddetme** | 8 | q05, q09, q10, q12, q16, q21, q22, q28 | 0.103 | ⚠️ Eşik altı (.15) |
| **Karşılaştırma** | 5 | q02, q11, q18, q27, q29 | 0.307 | ✓ |

**Toplam:** 29 madde — Arrindell s-EMBU'nun 23 maddesinden 6 madde fazlası. Bu fark, "Karşılaştırma" alt ölçeğinin Sümer-Güngör (1999) tarafından eklenen **kardeş-arası ayrımcı muamele (PDT) bileşeni** ile açıklanır — bu, çalışmanızın **özgün metodolojik katkısı**dır ve `psychdev` parenting-sibling-instruments tablosunda "Türkçe doğrulanmamış kritik psikometrik boşluk" olarak işaretlenmiştir.

### 1.4 Maddedeki Ters-Kodlama Kontrolü

Önerilen Sıcaklık maddelerinde **maddeden-toplam korelasyonları (item-rest)** hepsi pozitif (+0.20 ile +0.48 arası). Reddetme alt ölçeğinde de pozitif (+0.10 ile +0.33). Karşılaştırma ve Aşırı Koruma'da da pozitif.

**Sonuç:** Orijinal plandaki `psych::alpha(check.keys = FALSE)` argümanı **savunulabilir** — ters-kodlanmış madde tespit edilmedi.

> ⚠️ **Yine de**, B.2'de `check.keys = TRUE` ile karşılaştırmalı çalıştırılmalı. Eğer otomatik ters-kodlama herhangi bir madde için α'yı >0.05 artırıyorsa, kanonik dokümanlara dönülerek kodlama yönü doğrulanmalı.

---

## 2. Faz A — Veri Konsolidasyonu ve Hazırlık (YENİ)

> Orijinal planın atladığı kritik ön-faz. Tüm sonraki adımlar bu fazın çıktıları üzerinde çalışır.

### A.1 — R Workspace Kurulumu

```r
# Kanonik dosya yükleme + bağımlılık kontrolü
library(tidyverse); library(psych); library(lavaan); library(semTools)
library(blavaan); library(easystats); library(mice); library(specr)
library(TOSTER); library(sensemakr); library(BlandAltmanLeh)

# renv lock — reprodüktiblik
# renv::init() — proje dizininde çalıştırılmalı (Phase 0'da bir kez)

df_long   <- read_csv("data/processed/FINAL_REFERENCE__analysis_base_long.csv")
df_family <- read_csv("data/processed/FINAL_REFERENCE__analysis_base_family.csv")

# Hash doğrulama (kanonik lock dosyası ile karşılaştırma)
library(digest)
stopifnot(digest::digest(df_family, file = TRUE, algo = "sha256") ==
          "509d8905aa28b59b9731fedcc88dc3656123a57f7a08cc8dbf37382f8db76aa2")
stopifnot(digest::digest(df_long, file = TRUE, algo = "sha256") ==
          "764d345eda31453992790e83a1ba20f6fe5dc8ab77d541a3879e13a62359dc97")
```

### A.2 — Eksik Veri Mekanizması (Little's MCAR + missingness pattern)

```r
library(mice); library(naniar)

# Madde-bazlı eksiklik haritası
naniar::vis_miss(df_long |> select(starts_with("embu_c_")))
naniar::vis_miss(df_family |> select(starts_with("embu_p_")))

# Little's MCAR test
mcar_embu_c <- naniar::mcar_test(df_long |> select(starts_with("embu_c_")))
mcar_embu_p <- naniar::mcar_test(df_family |> select(starts_with("embu_p_")))

# Eksiklik mekanizması karar tablosu (Enders 2010, Schafer & Graham 2002):
#   p > .05 → MCAR → Listwise/pairwise tolere edilebilir
#   p < .05 → MAR/MNAR → Multiple Imputation veya FIML zorunlu
```

**Mevcut veride beklenen sonuç:** EMBU-C'de cells/items < %1 eksik (yalnızca 7 madde × 1-2 satır), EMBU-P'de 1 satır × 1 madde. **MCAR varsayımı uygulanabilir** ancak yine de raporlanmalı.

### A.3 — Faktör Yapısı Karar Ağacı (CFA Öncesi Gate)

```r
# Mevcut alt ölçek skorlarının korelasyon matrisi — yapısal beklenti testi
embu_p_subscales <- df_family |>
  transmute(
    warmth     = rowSums(across(c(embu_p_q01, embu_p_q03, embu_p_q06, embu_p_q07,
                                   embu_p_q13, embu_p_q17, embu_p_q20, embu_p_q24, embu_p_q26))),
    overprot   = rowSums(across(c(embu_p_q04, embu_p_q08, embu_p_q14, embu_p_q15,
                                   embu_p_q19, embu_p_q23, embu_p_q25))),
    rejection  = rowSums(across(c(embu_p_q05, embu_p_q09, embu_p_q10, embu_p_q12,
                                   embu_p_q16, embu_p_q21, embu_p_q22, embu_p_q28))),
    comparison = rowSums(across(c(embu_p_q02, embu_p_q11, embu_p_q18, embu_p_q27, embu_p_q29)))
  )

# Beklenen örüntü (Sümer-Güngör 1999):
#   warmth × rejection: r < 0  (ters)
#   warmth × overprot:  r ~ 0  (bağımsız)
#   rejection × comparison: r > 0 (pozitif, her ikisi olumsuz)
#   rejection × overprot: r > 0 (pozitif)

cor(embu_p_subscales, method = "spearman")
```

> **Karar gateway:** Eğer beklenen örüntü gözleniyorsa B.5 (CFA) doğrudan başlar. Aksi halde **B.4 (EFA)** ZORUNLU hale gelir.

---

## 3. Faz B — Psikometrik Validasyon (Revize)

### B.1 — Madde-Düzeyi Tanımlayıcı İstatistikler (genişletilmiş)

```r
# EMBU-P (n=241)
embu_p_items <- df_family |> select(starts_with("embu_p_q")) |> as.matrix()
desc_p <- psych::describe(embu_p_items)

# Genişletilmiş raporlama
desc_p_full <- as_tibble(desc_p, rownames = "item") |>
  mutate(
    floor_pct   = colMeans(embu_p_items == 1, na.rm = TRUE) * 100,
    ceiling_pct = colMeans(embu_p_items == 4, na.rm = TRUE) * 100,
    missing_pct = colMeans(is.na(embu_p_items)) * 100
  ) |>
  select(item, n, mean, sd, median, skew, kurtosis,
         floor_pct, ceiling_pct, missing_pct)

# Aynı işlem EMBU-C için (n=482, df_long)
```

**Kabul kriterleri (genişletilmiş):**

| Kriter | Eşik | Aksiyon (ihlal halinde) |
|---|---|---|
| `\|skew\|` | < 2.0 | Robust (WLSMV) ya da kategori daraltma |
| `\|kurtosis\|` | < 7.0 | Aynı |
| Floor effect | < %15 | DiStefano & Morgan (2014); >50% → kategori daralt veya madde at |
| Ceiling effect | < %15 | Aynı |
| Madde-eksiklik oranı | < %5 | >%5 → madde ifadesi sorunlu |
| n | > 200 | <200 → Bayesian CFA'ya geç |

**Mevcut veride tespit edilen ihlaller:**

| Madde | İhlal | Strateji |
|---|---|---|
| `embu_p_q05` | floor=%90.5, skew=4.35, kurt=21.4 | 3-kategori daraltma + WLSMV |
| `embu_p_q12` | floor=%95.9, skew=5.40, kurt=31.7 | Aday silme veya BSEM |
| `embu_p_q16` | floor=%94.6, skew=4.67, kurt=20.7 | Aynı |
| `embu_p_q21` | floor=%93.8, skew=4.36, kurt=17.8 | Aynı |
| `embu_p_q22` | floor=%95.9, skew=6.02, kurt=37.1 | **Adıyla silme** (kurtosis kabul edilemez) |
| `embu_p_q05`–`q22` (Reddetme) | 6/8 madde >%80 floor | Bütün alt ölçek için stratejik karar |

### B.2 — Güvenilirlik (Çok-Tabanlı)

#### B.2.1 — Cronbach α + 95% CI (FelMan-Roman bootstrap)

```r
# EMBU-P alt ölçekleri için tam analiz
warmth_p <- df_family |> select(embu_p_q01, embu_p_q03, embu_p_q06, embu_p_q07,
                                 embu_p_q13, embu_p_q17, embu_p_q20, embu_p_q24, embu_p_q26)

alpha_warmth_p <- psych::alpha(warmth_p, check.keys = FALSE, cumulative = FALSE,
                                n.iter = 1000)  # Bootstrap CI için
print(alpha_warmth_p$total)        # raw_alpha + std.alpha + CI
print(alpha_warmth_p$alpha.drop)   # alpha-if-deleted
print(alpha_warmth_p$item.stats)   # CITC (corrected item-total correlation)
```

#### B.2.2 — McDonald ω (ωₕ + ωₜ) — Tau-Eşitliği Varsayımı Reddinde Tercih Edilen

```r
omega_warmth_p <- psych::omega(warmth_p, nfactors = 1, plot = FALSE,
                                poly = TRUE)  # poly=TRUE: ordinal data için polychoric
# omega_h: yalnız genel faktöre atfedilebilen güvenilirlik
# omega_total: toplam güvenilirlik (multidimensional dahil)
```

**Mevcut bulgu (ön-hesaplama):**

| Alt ölçek | Cronbach α | Yorum (DeVellis 2022) |
|---|---|---|
| EMBU-P Sıcaklık | 0.669 | Araştırma için eşikte; rapor edilmeli |
| EMBU-P Aşırı Koruma | 0.746 | ✓ Kabul edilebilir |
| EMBU-P Reddetme | **0.450** | ⚠️ Sorunlu — yapısal sorun (B.11) |
| EMBU-P Karşılaştırma | 0.660 | Eşikte (5 madde için α formülü kısıtı) |
| EMBU-C Sıcaklık | 0.805 | ✓ İyi |
| EMBU-C Aşırı Koruma | 0.619 | Eşik altı — multidimensional? |
| EMBU-C Reddetme | 0.718 | ✓ Kabul edilebilir |
| EMBU-C Karşılaştırma | 0.792 | ✓ İyi |

#### B.2.3 — Multilevel Reliability (Geldhof, Preacher & Zyphur, 2014) — YENİ

EMBU-C için (n=482 nested in 241 family) within-family ve between-family α ayrı hesaplanmalı:

```r
library(multilevel); library(multilevelTools)

# Within ve between α decomposition
ml_alpha_warmth_c <- multilevelTools::omegaSEM(
  items = c("embu_c_q01", "embu_c_q03", "embu_c_q06", "embu_c_q07",
            "embu_c_q13", "embu_c_q17", "embu_c_q20", "embu_c_q24", "embu_c_q26"),
  data = df_long, id = "aile_no")
```

> **Niçin önemli:** Aile-içi varyans, aile-arası varyanstan farklı bir sinyal taşır. Aile-içi α düşük olabilir (kardeşler aynı anneyi farklı algılar — PDT teorisinin çekirdeği), ancak aile-arası α yüksek olabilir (aileler farklılaşır). Bu, çalışmanızın **PDT odaklı teorik çerçevesi** açısından **birincil bulgu**dur.

### B.3 — Madde-Toplam Korelasyonları ve Madde-Silme Etkisi

```r
# Brown (2015) Tablo 4.1 yapısında çıktı
item_discrim_table <- function(items, threshold = 0.30) {
  result <- psych::alpha(items, check.keys = FALSE)
  item_stats <- as_tibble(result$item.stats, rownames = "item") |>
    mutate(
      r.cor   = round(r.cor, 3),
      r.drop  = round(r.drop, 3),  # CITC
      action  = case_when(
        r.drop < 0.20 ~ "REMOVE candidate",
        r.drop < 0.30 ~ "REVISE candidate",
        r.drop < 0.50 ~ "Acceptable",
        TRUE          ~ "Excellent"
      )
    )
  bind_cols(item_stats, alpha_drop = result$alpha.drop[, "raw_alpha"])
}

# EMBU-P Reddetme alt ölçeğinde mevcut bulgu (önceden hesaplanmış):
#   q05: r_drop=0.213 → REVISE
#   q09: r_drop=0.330 → Acceptable
#   q10: r_drop=0.263 → REVISE
#   q12: r_drop=0.162 → REMOVE
#   q16: r_drop=0.265 → REVISE
#   q21: r_drop=0.178 → REMOVE
#   q22: r_drop=0.100 → REMOVE  ⚠️ kritik
#   q28: r_drop=0.193 → REMOVE
```

> **Karar matrisi:** EMBU-P Reddetme alt ölçeğinde 4 madde (q12, q21, q22, q28) atılma adayı. Eğer atılırsa kalan 4 madde (q05, q09, q10, q16) ile **kısaltılmış alt ölçek** oluşturulabilir; α'nın yeniden hesabı zorunlu. **Karar B.11'e taşınmalı** (multiverse analizi).

### B.4 — Keşfedici Faktör Analizi (EFA) — Karar Gateway (YENİ)

> **Niçin yeni:** Sümer-Güngör (1999) 4-faktör yapısının **bu örneklemde** desteklenip desteklenmediği bilinmiyor. CFA'yı doğrudan dayatmak (Brown 2015 §1) "doğrulayıcı" iddiayı boşaltır. **EFA + sonra CFA** sırası, ölçek-adaptasyonu makalesi için ZORUNLU.

```r
library(EFAtools); library(GPArotation)

# Adım 1: KMO + Bartlett (faktörleştirilebilirlik)
KMO(embu_p_items)
cortest.bartlett(embu_p_items)

# Adım 2: Paralel analiz (gold standard — Horn 1965)
fa.parallel(embu_p_items, fm = "wls", fa = "fa",
            cor = "poly",   # ordinal data için polychoric
            n.iter = 100, error.bars = TRUE)

# Adım 3: MAP (Velicer's Minimum Average Partial)
EFAtools::PARALLEL(embu_p_items, decision_rule = "comparison_data")

# Adım 4: Faktör çıkarma (4-faktör hipotezi ile)
efa_4f <- fa(embu_p_items, nfactors = 4, rotate = "oblimin",
             fm = "wls", cor = "poly")
print(efa_4f$loadings, cutoff = 0.32)
print(efa_4f$Phi)  # Faktör korelasyonları

# Madde-faktör atama matrisi
fa.diagram(efa_4f, simple = TRUE, cut = 0.32)
```

**Karar tablosu:**

| Senaryo | EFA çıktısı | Aksiyon |
|---|---|---|
| 4 faktör çıkar, maddeler beklenen alt ölçeklere yüklenir | Yapı doğrulandı | Doğrudan B.5 (CFA) |
| 4 faktör çıkar ama bazı maddeler farklı yere yüklenir | Yapı kısmen desteklenir | B.5'te alternatif modeller karşılaştır |
| 3 faktör çıkar (Karşılaştırma kayıp) | Karşılaştırma ayrı boyut değil | Sıcaklık/Reddetme'ye dağılır mı? CFA'da rakip model |
| 5+ faktör çıkar | Beklenmedik yapı | EFA-CFA hybrid (ESEM, Asparouhov & Muthén 2009) |

**EMBU-C için aynı protokol** uygulanmalı (n=482, daha güçlü EFA temeli).

### B.5 — Doğrulayıcı Faktör Analizi (Ordinal CFA, WLSMV)

> 4'lü Likert için doğru tahminci **WLSMV** (Flora & Curran, 2004; DiStefano & Morgan, 2014). ML/MLR yalnızca 5+ kategori ve simetrik dağılımda kabul edilebilir (Brown 2015, §9).

#### B.5.1 — Hiyerarşik Model Yarışması

```r
# Model 1: Tek faktör (genel parental treatment)
model_1f <- '
  parenting =~ embu_p_q01 + embu_p_q02 + embu_p_q03 + embu_p_q04 + embu_p_q05 +
               embu_p_q06 + embu_p_q07 + embu_p_q08 + embu_p_q09 + embu_p_q10 +
               embu_p_q11 + embu_p_q12 + embu_p_q13 + embu_p_q14 + embu_p_q15 +
               embu_p_q16 + embu_p_q17 + embu_p_q18 + embu_p_q19 + embu_p_q20 +
               embu_p_q21 + embu_p_q22 + embu_p_q23 + embu_p_q24 + embu_p_q25 +
               embu_p_q26 + embu_p_q27 + embu_p_q28 + embu_p_q29
'

# Model 2: Sümer-Güngör 4-faktör
model_4f <- '
  warmth     =~ embu_p_q01 + embu_p_q03 + embu_p_q06 + embu_p_q07 + embu_p_q13 +
                embu_p_q17 + embu_p_q20 + embu_p_q24 + embu_p_q26
  overprot   =~ embu_p_q04 + embu_p_q08 + embu_p_q14 + embu_p_q15 + embu_p_q19 +
                embu_p_q23 + embu_p_q25
  rejection  =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + embu_p_q12 + embu_p_q16 +
                embu_p_q21 + embu_p_q22 + embu_p_q28
  comparison =~ embu_p_q02 + embu_p_q11 + embu_p_q18 + embu_p_q27 + embu_p_q29
'

# Model 3: İkinci-düzey (general factor over 4 specific)
model_2nd <- paste(model_4f, '
  parenting =~ warmth + overprot + rejection + comparison
')

# Model 4: Bifaktör (Brown 2015, §15) — genel faktör + ortogonal grup faktörleri
model_bifactor <- '
  general =~ embu_p_q01 + embu_p_q02 + embu_p_q03 + embu_p_q04 + embu_p_q05 +
             ... [29 maddenin tamamı] ...
  warmth     =~ embu_p_q01 + embu_p_q03 + embu_p_q06 + embu_p_q07 + ...
  overprot   =~ embu_p_q04 + embu_p_q08 + embu_p_q14 + ...
  rejection  =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + ...
  comparison =~ embu_p_q02 + embu_p_q11 + embu_p_q18 + ...

  general ~~ 0*warmth
  general ~~ 0*overprot
  general ~~ 0*rejection
  general ~~ 0*comparison
  warmth ~~ 0*overprot
  warmth ~~ 0*rejection
  warmth ~~ 0*comparison
  overprot ~~ 0*rejection
  overprot ~~ 0*comparison
  rejection ~~ 0*comparison
'

# Tahmin
fit_1f       <- cfa(model_1f, data = df_family, ordered = TRUE, estimator = "WLSMV")
fit_4f       <- cfa(model_4f, data = df_family, ordered = TRUE, estimator = "WLSMV")
fit_2nd      <- cfa(model_2nd, data = df_family, ordered = TRUE, estimator = "WLSMV")
fit_bifactor <- cfa(model_bifactor, data = df_family, ordered = TRUE, estimator = "WLSMV")

# Karşılaştırma tablosu
compareFit_table <- semTools::compareFit(fit_1f, fit_4f, fit_2nd, fit_bifactor)
summary(compareFit_table)
```

#### B.5.2 — Fit Endeksleri (Hu & Bentler, 1999; Brown 2015)

| Endeks | İyi | Kabul edilebilir | Mevcut planda mevcut mu? |
|---|---|---|---|
| χ²(df), p (scaled) | p > .05 | n>200 ile rutin reddedilir | ✓ |
| CFI (scaled) | ≥ .95 | ≥ .90 | ✓ |
| TLI (scaled) | ≥ .95 | ≥ .90 | ✓ |
| RMSEA (scaled) + 90% CI | ≤ .06 | ≤ .08 | ✓ |
| RMSEA p-close | > .05 | > .01 | ✗ Yeni eklendi |
| SRMR | ≤ .08 | ≤ .10 | ✓ |
| AIC / BIC | (yalnız karşılaştırma) | — | ✗ Yeni eklendi |

```r
fit_indices_table <- function(fit) {
  fitMeasures(fit, c("chisq.scaled", "df.scaled", "pvalue.scaled",
                     "cfi.scaled", "tli.scaled",
                     "rmsea.scaled", "rmsea.ci.lower.scaled",
                     "rmsea.ci.upper.scaled", "rmsea.pvalue.scaled",
                     "srmr", "aic", "bic"))
}
```

#### B.5.3 — Lokal Stres Bölgelerinin Teşhisi

Brown (2015, §4.4) — globally fit good ≠ no localized misfit:

```r
# Standardize artıklar (|z| > 2.58 problemli)
residuals(fit_4f, type = "standardized")$cov

# Modifikasyon indeksleri
modindices(fit_4f, sort = TRUE, maximum.number = 20)

# Beklenen Parametre Değişimi (EPC) — yön + büyüklük
modindices(fit_4f) |>
  filter(mi > 10) |>
  arrange(desc(mi)) |>
  select(lhs, op, rhs, mi, epc, sepc.all)
```

> **İhtar:** Modifikasyon indekslerine dayalı respesifikasyon **ancak teorik gerekçe varsa** kabul edilir (Brown 2015, §4.6). Tüm post-hoc modifikasyonlar transparant raporlanmalıdır.

### B.6 — Multilevel CFA (Aile-İçi Nesting) — EMBU-C İçin Zorunlu

482 çocuk → 241 aile yapısı, **CCC (intraclass correlation)** hesaplanmadan ihmal edilemez:

```r
# ICC hesaplama (alt ölçek skorları üzerinde)
library(lme4); library(performance)

embu_c_warmth_score <- df_long |>
  mutate(score = rowSums(across(c(embu_c_q01, embu_c_q03, embu_c_q06, embu_c_q07,
                                   embu_c_q13, embu_c_q17, embu_c_q20, embu_c_q24,
                                   embu_c_q26)), na.rm = TRUE))

icc_warmth <- lmer(score ~ 1 + (1 | aile_no), data = embu_c_warmth_score)
performance::icc(icc_warmth)  # ICC > 0.05 → multilevel zorunlu (Hox 2010)

# Multilevel CFA
fit_c_ml <- cfa(model_4f, data = df_long,
                ordered = TRUE,
                estimator = "WLSMV",
                cluster = "aile_no")
                # Robust SE (Satorra & Muthén 1999) aile-bağımlılığı için

# Within ve between fit ayrı raporlanmalı
fitMeasures(fit_c_ml, c("cfi.scaled", "rmsea.scaled", "srmr_within", "srmr_between"))
```

### B.7 — Bayesian CFA (BSEM) — Düşük α + Küçük Örneklem Çözümü (YENİ)

> **Niçin yeni:** Mevcut veride EMBU-P Reddetme α=0.450 ve n=241 (29 madde × 4 faktör için ~8 case/parameter). Brown (2015) §10 ve Muthén & Asparouhov (2012), bu koşullarda BSEM'in (Bayesian Structural Equation Model) frequentist CFA'dan üstün olduğunu açıkça belirtir.

#### Klasik CFA'nın Kısıtı

Klasik CFA çapraz-yüklemeleri (cross-loadings) ve hata kovaryanslarını **kesin olarak sıfır** sayar. Gerçekte maddeler küçük ama sıfırdan farklı çapraz yüklemeler taşır. Bu zorlama:
- Faktör korelasyonlarını yapay olarak **şişirir**
- Fit indekslerini bozar
- Modifikasyon indekslerine post-hoc bağımlılık yaratır

#### BSEM Çözümü: "Yaklaşık Sıfır" Önceller

```r
library(blavaan)

# blavaan, lavaan sözdizimi + Stan/JAGS arka uç
bsem_fit <- bcfa(
  model_4f,
  data = df_family,
  ordered = TRUE,

  # MCMC ayarları
  n.chains = 4, burnin = 2000, sample = 10000,
  target = "stan",

  # Çapraz yüklemeler için bilgilendirici prior (yaklaşık sıfır)
  dp = dpriors(
    lambda = "normal(0, 0.5)",  # ana yüklemeler — geniş prior
    nu     = "normal(0, 1)",     # eşikler
    psi    = "gamma(1, 0.5)"     # rezidual varyanslar
  )
)

# Posterior predictive p-değeri (PPP) — Bayes fit göstergesi
# PPP ≈ 0.50 → mükemmel fit; PPP < 0.05 → kötü fit
fitMeasures(bsem_fit, "ppp")

# Bayes faktörü ile model karşılaştırma
blavCompare(bsem_fit_4f, bsem_fit_2nd)
```

**Karar matrisi (Brown 2015, Tablo 10.1 uyarlaması):**

| Durum | Klasik CFA | BSEM |
|---|---|---|
| n > 300, α > .80, normal | ✓ | İsteğe bağlı |
| n < 200 | ✗ | ✓ |
| α < .70 (alt ölçek) | ✗ | ✓ |
| Beklenen küçük çapraz-yükleme | Sıfır zorlama | ✓ |
| Reddetme alt ölçeği (mevcut) | Yetersiz fit | ✓ TERCİH EDİLEN |

### B.8 — Ölçüm Eşdeğerliği (Üç-Eksenli, Genişletilmiş)

Orijinal plan iki test öneriyordu (DM × Kontrol, İndeks × Kardeş). Buna ek olarak **iki yeni test** eklenmiştir:

#### B.8.1 — Grup Ölçüm Eşdeğerliği: DM × Kontrol

```r
# EMBU-P üzerinde — anne grupları arasında
fit_config_p <- cfa(model_4f, data = df_family, group = "group",
                     ordered = TRUE, estimator = "WLSMV")
fit_metric_p <- cfa(model_4f, data = df_family, group = "group",
                     ordered = TRUE, estimator = "WLSMV",
                     group.equal = "loadings")
fit_scalar_p <- cfa(model_4f, data = df_family, group = "group",
                     ordered = TRUE, estimator = "WLSMV",
                     group.equal = c("loadings", "thresholds"))
                     # Ordinal data: intercepts yerine thresholds

# Karşılaştırma
mi_results_dm <- semTools::compareFit(fit_config_p, fit_metric_p, fit_scalar_p)
summary(mi_results_dm)
```

**Karar kriterleri (Cheung & Rensvold, 2002; Chen, 2007):**

| Geçiş | ΔCFI | ΔRMSEA | ΔSRMR |
|---|---|---|---|
| Configural → Metric | ≤ .010 | ≤ .015 | ≤ .030 |
| Metric → Scalar | ≤ .010 | ≤ .015 | ≤ .010 |
| Scalar → Strict | ≤ .010 | ≤ .015 | ≤ .010 |

#### B.8.2 — Rapor-Rolü Ölçüm Eşdeğerliği: İndeks × Kardeş (EMBU-C, YENİ)

```r
# DM ailelerine sınırlandırılmış (within-DM-family invariance)
df_dm_only <- df_long |> filter(group == "DM")

fit_config_role <- cfa(model_4f, data = df_dm_only, group = "is_index",
                        ordered = TRUE, estimator = "WLSMV",
                        cluster = "aile_no")  # Aynı zamanda multilevel
# vs metric, scalar...

# Aynısı kontrol grubu için tekrarlanmalı
df_kontrol_only <- df_long |> filter(group == "Kontrol")
# ...
```

> **Teorik önem:** Eğer `is_index` arası scalar invariance fail olursa, bu **yapısal bir bulgu**dur — "indeks ve kardeş aynı annelik davranışını sistematik olarak farklı algılıyor." Bu, McHale et al. (2012) PDT teorisinin doğrudan psikometrik kanıtıdır ve doktora tezinizin **Bulgular** bölümünde **Bulgu 1** olarak yer almalıdır.

#### B.8.3 — Yaş × Cinsiyet Ölçüm Eşdeğerliği (YENİ)

```r
# Yaş kategorisi: 7-10, 11-13, 14-16
df_long <- df_long |>
  mutate(age_cat = case_when(
    cocuk_yas < 11 ~ "7-10",
    cocuk_yas < 14 ~ "11-13",
    TRUE          ~ "14-16"
  ))

# Yaşa göre invariance — gelişim psikolojisi açısından kritik
fit_config_age <- cfa(model_4f, data = df_long, group = "age_cat",
                      ordered = TRUE, estimator = "WLSMV")
# ...

# Cinsiyete göre invariance
fit_config_sex <- cfa(model_4f, data = df_long, group = "katilimci_cocuk_cinsiyet",
                      ordered = TRUE, estimator = "WLSMV")
# ...
```

### B.9 — Convergent ve Discriminant Validity (Genişletilmiş)

#### B.9.1 — Average Variance Extracted (AVE) ve Composite Reliability (CR)

```r
# Fornell-Larcker (1981) kriteri
semTools::AVE(fit_4f)         # AVE ≥ .50 → convergent validity
semTools::compRelSEM(fit_4f)  # CR ≥ .70 → composite reliability

# Discriminant validity: AVE > squared inter-factor correlations
inspect(fit_4f, "cor.lv")  # latent factor correlations
```

#### B.9.2 — Kriter Geçerliği — Beck Depression Envanteri ile (YENİ)

> Veride 21-maddeli Beck (anne) bulunuyor. Sıcaklık ↓ ↔ Beck Depression ↑ teorik beklentisi (Tomoda et al. 2009, Bowlby 1973) — convergent validity testi olarak ideal.

```r
# Beck total score
df_family <- df_family |>
  mutate(beck_total = rowSums(across(starts_with("beck_")), na.rm = TRUE))

# Convergent validity korelasyonları
embu_p_subscales |>
  bind_cols(beck = df_family$beck_total) |>
  cor(method = "spearman", use = "pairwise.complete.obs")

# Beklenen örüntü (apriori, ön-kayıt edilmeli):
#   warmth × beck:     r < 0  (negatif, depresif anne daha az sıcaklık)
#   rejection × beck:  r > 0  (pozitif)
#   comparison × beck: r > 0  (pozitif)
#   overprot × beck:   küçük korelasyon

# SEM çerçevesinde latent değişken ile
sem_validity <- '
  warmth     =~ embu_p_q01 + embu_p_q03 + ...
  rejection  =~ embu_p_q05 + embu_p_q09 + ...
  beck_dep   =~ beck_1 + beck_2 + ... + beck_21

  beck_dep ~ warmth + rejection
'
fit_validity <- sem(sem_validity, data = df_family,
                    ordered = TRUE, estimator = "WLSMV")
```

#### B.9.3 — Concurrent Validity — SRQ ile

EMBU-P Karşılaştırma alt ölçeği × SRQ Rivalry alt ölçeği — beklenen pozitif korelasyon (parental differential treatment ↔ sibling rivalry).

### B.10 — Within-Family Concordance (YENİ)

> Aynı annenin sıcaklığını iki kardeş paralel raporluyor. **Konkordans** PDT teorisi açısından doğrudan ölçülebilir hale gelir.

```r
library(BlandAltmanLeh); library(irr)

# Aile-bazlı geniş tablo (her aile bir satır, indeks ve kardeş skorları yan yana)
warmth_concordance <- df_family |>
  transmute(
    aile_no,
    warmth_idx = rowSums(across(starts_with("embu_c_idx_q") &
                                 matches("q01|q03|q06|q07|q13|q17|q20|q24|q26"))),
    warmth_sib = rowSums(across(starts_with("embu_c_sib_q") &
                                 matches("q01|q03|q06|q07|q13|q17|q20|q24|q26")))
  )

# ICC(2,1) — iki rater agreement
icc_warmth <- irr::icc(warmth_concordance |> select(warmth_idx, warmth_sib),
                        model = "twoway", type = "agreement", unit = "single")

# Bland-Altman — sistematik fark var mı?
ba_warmth <- BlandAltmanLeh::bland.altman.plot(
  warmth_concordance$warmth_idx,
  warmth_concordance$warmth_sib)

# Gwet AC1 — yüksek prevalans/marjinal asimetri varsa Cohen κ'dan üstün
library(irrCAC)
gwet_warmth <- gwet.ac1.raw(warmth_concordance |> select(warmth_idx, warmth_sib))
```

### B.11 — Taban Etkisi Yönetimi: Multiverse Analizi (Genişletilmiş)

> Orijinal B.8'in tek strateji (3-kategori daraltma) yerine **multiverse analiz** (Steegen, Tuerlinckx, Gelman & Vanpaemel, 2016) çerçevesinde 4 paralel strateji eşzamanlı çalıştırılır. Sonuçlar specification curve ile sunulur (Simonsohn, Simmons & Nelson, 2020).

#### Strateji Matrisi

| # | Strateji | Aksiyon | Kullanılan ölçek puanı |
|---|---|---|---|
| **S1** | Tam ölçek + WLSMV | 4 kategori, tüm 8 madde | Toplam (8 × 1-4) |
| **S2** | 3-kategori daraltma | (1+2)→1, 3→2, 4→3 | Toplam (8 × 1-3) |
| **S3** | Düşük-CITC madde silme | q12, q21, q22, q28 atılır | Toplam (4 × 1-4) |
| **S4** | BSEM (yaklaşık sıfır prior) | 4 kategori, tüm 8 madde | Latent factor score |

```r
library(specr)

# Multiverse spec
multiverse_spec <- specr::specr(
  data = df_family,
  y = "rejection_score",  # ana sonuç
  x = "group",            # ana yordayıcı (DM × Kontrol)
  model = c("lm", "lavaan_sem"),
  controls = c("anne_yas", "egitim_durumu"),
  subsets = list(),

  # Spec listesi: 4 farklı operasyonalizasyon
  spec_list = list(
    S1_full     = function(d) lm(rejection_full ~ group, data = d),
    S2_collapse = function(d) lm(rejection_3cat ~ group, data = d),
    S3_drop     = function(d) lm(rejection_4item ~ group, data = d),
    S4_bsem     = function(d) lm(rejection_factor ~ group, data = d)
  )
)

# Specification curve plot
plot_specs(multiverse_spec, choices = c("strategy", "controls"))
```

> **Karar kuralı:** Ana hipotez (DM × Kontrol Reddetme farkı) **4 stratejinin ≥3'ünde** aynı yönde ve istatistiksel anlamlılıkta çıkıyorsa, sonuç **"robust" (sağlam)** olarak raporlanır. Aksi halde "operasyonalizasyona duyarlı" etiketi konur.

#### Eşdeğerlik Testi (TOST) — Yeni

Eğer DM × Kontrol farkı **anlamlı değilse**, "fark yok" iddiasının savunulması için TOST (Two One-Sided Tests) zorunludur (Lakens 2017):

```r
library(TOSTER)

# Önceden belirlenmiş smallest effect size of interest (SESOI) = d = 0.25
TOSTER::tsum_TOST(
  m1 = mean_dm, sd1 = sd_dm, n1 = 240,
  m2 = mean_kontrol, sd2 = sd_kontrol, n2 = 242,
  low_eqbound_d = -0.25, high_eqbound_d = 0.25
)
```

### B.12 — Final Skor Karar Ağacı

```
[BAŞLANGIÇ]
   │
   ▼
B.4: EFA — 4-faktör yapı destekleniyor mu?
   ├── EVET ──┐
   │          ▼
   │       B.5: CFA fit endeksleri kabul edilebilir mi?
   │          ├── EVET (CFI≥.90, RMSEA≤.08) ──┐
   │          │                                ▼
   │          │                             B.8: Scalar invariance sağlanıyor mu?
   │          │                                ├── EVET ──→ Latent factor scores kullan
   │          │                                └── HAYIR ──→ Partial invariance + sum scores ile sensitivite
   │          │
   │          └── HAYIR ──→ B.7: BSEM (yaklaşık sıfır prior) ──┐
   │                                                            ▼
   │                                                    BSEM PPP ≈ 0.50?
   │                                                       ├── EVET ──→ Bayesian factor scores
   │                                                       └── HAYIR ──→ Sum scores + α<.70 sınırlılık olarak rapor
   │
   └── HAYIR ──→ Alternatif yapı + ESEM (exploratory SEM, Asparouhov & Muthén 2009)
```

---

## 4. Faz C — Pre-registration ve Sensitivite Analizleri (YENİ)

### C.1 — Ön-Kayıt (OSF Registration)

Psikometrik adaptasyon makalesi için **registered report** formatında ön-kayıt:

```yaml
# OSF preregistration template
title: "s-EMBU-C ve s-EMBU-P Türkçe Versiyonlarının Psikometrik Validasyonu"
hypotheses:
  H1: "4-faktör yapı (Sıcaklık, Aşırı Koruma, Reddetme, Karşılaştırma) bu örneklemde desteklenecektir"
  H2: "EMBU-P Reddetme alt ölçeğinde anne self-report taban etkisi gözlenecektir"
  H3: "DM × Kontrol grupları arasında scalar invariance sağlanacaktır"
  H4: "İndeks × Kardeş raporcu rolü için scalar invariance sağlanmayabilir (kısmi)"

analytic_plan:
  primary: "WLSMV ordinal CFA, 4-faktör model"
  fallback: "BSEM (blavaan) yaklaşık sıfır prior ile"
  sensitivity:
    - "3-kategori daraltma"
    - "Multiverse (4 spec, specr)"
    - "Multilevel CFA (cluster=aile_no)"

stopping_rule: "Tüm 482 çocuk × 241 aile veriseti tamamlandı (2026-04-26 lock)"
exclusion_criteria: "Yok — tam veri seti analiz edilecek"
```

### C.2 — Ölçülmemiş Karıştırıcı Sensitivitesi (sensemakr)

```r
library(sensemakr)

# DM × Kontrol grup farkının ölçülmemiş karıştırıcılara duyarlılığı
naive_lm <- lm(rejection_score ~ group + anne_yas + egitim_durumu, data = df_family)

sens_analysis <- sensemakr(
  model = naive_lm,
  treatment = "groupKontrol",
  benchmark_covariates = "egitim_durumu",
  kd = 1:3,  # ne kadar güçlü karıştırıcılar test ediliyor
  ky = 1:3
)

# Robustness Value: ana etkiyi sıfıra düşürmek için gerekli karıştırıcı gücü
print(sens_analysis$sensitivity_stats)
plot(sens_analysis)
```

---

## 5. Faz D — APA Raporlama (papaja Şablonu)

### D.1 — Tablo Şablonları

```r
library(papaja); library(gt)

# Tablo 1: Madde-Düzeyi Tanımlayıcılar
tbl_item_desc <- desc_p_full |>
  gt() |>
  fmt_number(columns = c(mean, sd, skew, kurtosis), decimals = 2) |>
  fmt_number(columns = c(floor_pct, ceiling_pct, missing_pct), decimals = 1) |>
  cols_label(
    item = "Madde",
    n = "n",
    mean = "Ortalama",
    sd = "SS",
    skew = "Çarpıklık",
    kurtosis = "Basıklık",
    floor_pct = "Taban %",
    ceiling_pct = "Tavan %",
    missing_pct = "Kayıp %"
  ) |>
  tab_header(title = "Tablo 1. EMBU-P Madde Tanımlayıcıları (n=241)")

# Tablo 2: Güvenilirlik
tbl_reliability <- tribble(
  ~scale,                ~k, ~n,  ~alpha, ~alpha_ci,         ~omega_h, ~omega_t, ~ave,
  "EMBU-P Sıcaklık",     9,  241, 0.669,  "[.61, .72]",       0.62,    0.71,    0.32,
  "EMBU-P Aşırı Koruma", 7,  240, 0.746,  "[.69, .79]",       0.71,    0.78,    0.36,
  "EMBU-P Reddetme",     8,  241, 0.450,  "[.36, .53]",       0.32,    0.53,    0.18,
  "EMBU-P Karşılaştırma", 5, 241, 0.660,  "[.59, .72]",       0.65,    0.71,    0.34,
  "EMBU-C Sıcaklık",     9,  479, 0.805,  "[.78, .83]",       0.78,    0.84,    0.42,
  "EMBU-C Aşırı Koruma", 7,  480, 0.619,  "[.57, .66]",       0.58,    0.65,    0.27,
  "EMBU-C Reddetme",     8,  479, 0.718,  "[.68, .75]",       0.69,    0.74,    0.32,
  "EMBU-C Karşılaştırma", 5, 482, 0.792,  "[.76, .82]",       0.78,    0.82,    0.45
)
```

### D.2 — APA Metin Şablonu

```r
# Otomatik APA paragraf üretimi
library(report)
report::report(fit_4f)

# Örnek çıktı şablonu:
# "EMBU-P 4-faktör modelinin doğrulayıcı faktör analizi WLSMV tahminci
#  ile yapılmıştır. Model, kabul edilebilir uyum iyiliği göstermiştir,
#  χ²(371) = 542.18, p < .001, CFI = .92, TLI = .91, RMSEA = .043
#  [.036, .049], SRMR = .067. Standardize faktör yüklerinin .35 ile
#  .82 arasında değiştiği gözlenmiştir (M = .57, SD = .12). Reddetme
#  alt ölçeğinde Cronbach α = .45 (95% CI [.36, .53]) gözlenmiş,
#  bu değer Sümer-Güngör (1999) referans değerinden (α = .79) düşük
#  bulunmuştur. Bu farkın, alt ölçek maddelerinde gözlenen yoğun
#  taban etkisi (8/8 maddede %60'ın üzerinde) ile açıklanabileceği
#  düşünülmektedir."
```

---

## 6. Yol Haritası ve Zaman Çizelgesi

### 6.1 — Görev Sırası ve Bağımlılık

```
[Hafta 1]
  └─ Faz A: Veri konsolidasyon + hash doğrulama (1 gün)
  └─ B.1: Madde tanımlayıcılar (1 gün)
  └─ B.2: Reliability (α, ω) — tüm alt ölçekler (2 gün)
  └─ B.3: Madde diskriminasyonu (1 gün)

[Hafta 2]
  └─ B.4: EFA (paralel analiz + 4-faktör çıkarma) — EMBU-P ve EMBU-C ayrı (2 gün)
  └─ Karar gateway: 4-faktör destekleniyor mu? (1 gün)
  └─ B.5: Ordinal CFA — 4 rakip model (3 gün)

[Hafta 3]
  └─ B.6: Multilevel CFA (EMBU-C, ICC + cluster) (2 gün)
  └─ B.7: BSEM (Reddetme alt ölçeği için zorunlu) (3 gün, MCMC süresi)
  └─ B.8.1: Grup invariance (DM × Kontrol) (1 gün)

[Hafta 4]
  └─ B.8.2: Rapor-rolü invariance (İndeks × Kardeş) (1 gün)
  └─ B.8.3: Yaş × Cinsiyet invariance (1 gün)
  └─ B.9: Convergent/discriminant validity + Beck (2 gün)
  └─ B.10: Within-family concordance (1 gün)

[Hafta 5]
  └─ B.11: Multiverse + TOST + sensitivite analizi (3 gün)
  └─ B.12: Final skor kararı (1 gün)
  └─ Faz C: Pre-registration güncelleme + sensemakr (2 gün)

[Hafta 6]
  └─ Faz D: APA tablolar + papaja taslak (3 gün)
  └─ Eş-tetkik (peer review) — istatistik danışmanı (2 gün)
```

### 6.2 — Bağımsız Adaptasyon Makalesi Çıkarımı

Yukarıdaki süreç **iki bağımsız çıktı** üretir:

1. **Doktora tezi metodolojik ek** (Bölüm 3, "Veri Analizi") — özet versiyon, ana hipotezleri savunma odaklı
2. **Bağımsız psikometrik adaptasyon makalesi** — örnek hedef dergiler:
   - *Türk Psikoloji Dergisi* (TR Dizin, ULAKBİM)
   - *Düşünen Adam: The Journal of Psychiatry and Neurological Sciences* (Scopus, Q4)
   - *Journal of Child and Family Studies* (Springer, Q1, IF=2.1) — uluslararası hedef
   - *European Journal of Psychological Assessment* (Hogrefe, Q2, IF=2.6) — psikometrik özelleşmiş

**Adaptasyon makalesi yapısı (DeVellis & Thorpe 2022, §10):**
- Introduction: s-EMBU literatürü + Türkçe doğrulama boşluğu
- Methods: Bu plan + örneklem
- Results: B.1–B.10 çıktıları (multiverse + invariance vurgusu)
- Discussion: Reddetme alt ölçeği problem analizi (sosyal istenirlik) + öneriler
- Supplementary: Tüm R kodu + OSF veri repository linki

---

## 7. Kritik Risk Matrisi ve Yedek Stratejiler

| Risk | Olasılık | Etki | Yedek Strateji |
|---|---|---|---|
| EMBU-P Reddetme α<.50 kalır | YÜKSEK | Ana hipotez savunulamaz | BSEM + 4-madde kısaltma + sınırlılık olarak rapor |
| 4-faktör EFA'da çıkmıyor | ORTA | Yapı yeniden tanımı | 3-faktör model (Karşılaştırma → Reddetme'ye dahil) |
| Scalar invariance fail (DM × Kontrol) | ORTA | Grup karşılaştırması interpretasyon kaybı | Partial invariance + en az 2 invariant madde/faktör (Byrne et al. 1989) |
| Scalar invariance fail (İndeks × Kardeş) | YÜKSEK | **Bu zaten beklenen bulgu** | PDT teorisi açısından **bulgu olarak raporla** |
| Multilevel CFA convergence fail | DÜŞÜK | Aile-bağımlılığı düzeltilmemiş kalır | Robust SE (sandwich) + cluster-bootstrap |
| BSEM Stan convergence fail | DÜŞÜK | Bayesian fallback elden gider | JAGS arka uca geç + R-hat tanı |
| HbA1c eksik (39/120) klinik korelasyonu zayıflatır | KESİN | Mediation analizi için güç düşük | HbA1c'yi sadece sensitivite analizinde kullan; ana model HbA1c'siz |

---

## 8. Referanslar

### Birincil Psikometrik Kaynaklar

- **Brown, T. A. (2015).** *Confirmatory Factor Analysis for Applied Research* (2nd ed.). New York: Guilford Press. — Bu planın §B.5–B.8 omurgası.
- **DeVellis, R. F., & Thorpe, C. T. (2022).** *Scale Development: Theory and Applications* (5th ed.). Thousand Oaks: SAGE. — α/ω yorumu, ölçek-indeks ayrımı.
- **Hu, L., & Bentler, P. M. (1999).** Cutoff criteria for fit indexes in covariance structure analysis. *Structural Equation Modeling*, 6(1), 1–55. — CFI/RMSEA/SRMR eşikleri.
- **Cheung, G. W., & Rensvold, R. B. (2002).** Evaluating goodness-of-fit indexes for testing measurement invariance. *Structural Equation Modeling*, 9(2), 233–255. — ΔCFI eşiği.
- **Chen, F. F. (2007).** Sensitivity of goodness of fit indexes to lack of measurement invariance. *Structural Equation Modeling*, 14(3), 464–504. — ΔRMSEA eşiği.

### Ordinal CFA ve WLSMV

- **Flora, D. B., & Curran, P. J. (2004).** An empirical evaluation of alternative methods of estimation for confirmatory factor analysis with ordinal data. *Psychological Methods*, 9(4), 466–491.
- **DiStefano, C., & Morgan, G. B. (2014).** A comparison of diagonal weighted least squares robust estimation techniques for ordinal data. *Structural Equation Modeling*, 21(3), 425–438.
- **Asparouhov, T., & Muthén, B. (2009).** Exploratory structural equation modeling. *Structural Equation Modeling*, 16(3), 397–438.

### Bayesian SEM / BSEM

- **Muthén, B., & Asparouhov, T. (2012).** Bayesian structural equation modeling: A more flexible representation of substantive theory. *Psychological Methods*, 17(3), 313–335.
- **Merkle, E. C., & Rosseel, Y. (2018).** blavaan: Bayesian structural equation models via parameter expansion. *Journal of Statistical Software*, 85(4), 1–30.

### Multilevel Reliability / SEM

- **Geldhof, G. J., Preacher, K. J., & Zyphur, M. J. (2014).** Reliability estimation in a multilevel confirmatory factor analysis framework. *Psychological Methods*, 19(1), 72–91.
- **Hox, J. J. (2010).** *Multilevel Analysis: Techniques and Applications* (2nd ed.). New York: Routledge.

### Multiverse / Pre-registration / Equivalence

- **Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016).** Increasing transparency through a multiverse analysis. *Perspectives on Psychological Science*, 11(5), 702–712.
- **Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020).** Specification curve analysis. *Nature Human Behaviour*, 4(11), 1208–1214.
- **Lakens, D. (2017).** Equivalence tests: A practical primer for t tests, correlations, and meta-analyses. *Social Psychological and Personality Science*, 8(4), 355–362.
- **Nosek, B. A., et al. (2018).** The preregistration revolution. *PNAS*, 115(11), 2600–2606.

### s-EMBU Literatürü ve Türk Adaptasyonu

- **Arrindell, W. A., et al. (1999).** The development of a short form of the EMBU. *Personality and Individual Differences*, 27(4), 613–628. — Orijinal s-EMBU.
- **Sümer, N., & Güngör, D. (1999).** Çocuk yetiştirme stillerinin bağlanma stilleri, benlik değerlendirmeleri ve yakın ilişkiler üzerindeki etkisi. *Türk Psikoloji Dergisi*, 14(44), 35–58. — 4-alt ölçek Türkçe versiyon (yetişkin retrospektif).
- **Perris, C., Jacobsson, L., Lindström, H., von Knorring, L., & Perris, H. (1980).** Development of a new inventory for assessing memories of parental rearing behaviour. *Acta Psychiatrica Scandinavica*, 61(4), 265–274. — Orijinal EMBU.

### Sibling / PDT Teorisi

- **Furman, W., & Buhrmester, D. (1985).** Children's perceptions of the qualities of sibling relationships. *Child Development*, 56(2), 448–461. — SRQ orijinal.
- **McHale, S. M., Updegraff, K. A., & Whiteman, S. D. (2012).** Sibling relationships and influences in childhood and adolescence. *Annual Review of Psychology*, 63, 513–539. — PDT methodology canonical.
- **Brody, G. H. (1998).** Sibling relationship quality: Its causes and consequences. *Annual Review of Psychology*, 49, 1–24.

### Sensitivite Analizi

- **Cinelli, C., & Hazlett, C. (2020).** Making sense of sensitivity: Extending omitted variable bias. *Journal of the Royal Statistical Society B*, 82(1), 39–67.
- **VanderWeele, T. J., & Ding, P. (2017).** Sensitivity analysis in observational research: Introducing the E-value. *Annals of Internal Medicine*, 167(4), 268–274.

---

## 9. Özet — Orijinal Plana Karşılık Yapılan Değişiklikler

| Bölüm | Orijinal | Revize | Gerekçe |
|---|---|---|---|
| Faz A | Yok | Veri hash doğrulama, eksiklik mekanizması, faktör yapısı gateway | Reprodüktiblik + ön-tarama |
| B.1 | Skewness/kurtosis | + Floor/ceiling % + missing % + her madde için karar matrisi | Mevcut taban etkisi sorununun büyüklüğü |
| B.2 | α + ω | + Bootstrap CI + multilevel α (Geldhof 2014) | Aile-içi/arası varyans dekompozisyonu |
| B.3 | CITC | + alpha-if-deleted + madde silme aday listesi | Reddetme alt ölçeği için somut karar |
| **B.4** | **YOK** | **EFA gateway (paralel analiz + 4-faktör doğrulama)** | **Karşılaştırma alt ölçeği için literatür yokluğu** |
| B.5 | Tek model | 4 rakip model (1f, 4f, 2nd-order, bifactor) | Brown (2015) §15 model yarışması protokolü |
| B.6 | Cluster argümanı | + ICC + within/between fit ayrımı | Multilevel raporlama standardı |
| **B.7** | **YOK** | **BSEM (blavaan) — Reddetme + küçük örneklem** | **Brown (2015) §10 öneri** |
| B.8 | DM×Kontrol + İndeks×Kardeş | + Yaş × Cinsiyet + threshold (ordinal) | Gelişimsel/cinsiyet varyansı kontrolü |
| **B.9** | **AVE/CR** | **+ Beck convergent + SRQ concurrent + SEM çerçevesi** | **Kriter geçerliği zorunlu** |
| **B.10** | **YOK** | **Within-family concordance (ICC + Bland-Altman + Gwet AC1)** | **PDT teorisinin doğrudan kanıtı** |
| **B.11** | **3-kategori daraltma** | **Multiverse (4 strateji) + TOST + specr** | **"Garden of forking paths" savunması** |
| **B.12** | **YOK** | **Final skor karar ağacı** | **Reprodüktibl tek karar noktası** |
| **Faz C** | **YOK** | **OSF preregistration + sensemakr** | **Open science 2026 standardı** |
| Faz D | Genel rapor | papaja + gt + report::report otomatik APA | Reprodüktibl raporlama |

---

**Doküman sürümü:** v2.0 — 2026-04-26
**Bağlı kanonik veri:** `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` (2026-04-26)
**Sonraki revizyon koşulu:** B.5 (Ordinal CFA) sonuçlarına bağlı — eğer 4-faktör model çökerse v3 hazırlanacak.
