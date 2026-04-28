# Tez Yazım Rehberi — Quarto, Türkçe APA 7, JARS-Mixed, papaja

**Ne zaman oku:** `chapters/*.qmd` düzenleme, `_quarto.yml` ayarı, `references.bib`/`apa.csl`,
papaja kullanımı, JARS-Mixed/STROBE checklist denetimi, Türkçe terim sözlüğü, kaynak
gösterimi, bölüm yapısı (Yöntem, Bulgular, Tartışma, Sonuç).

**Kaynaklar:** APA Publication Manual (7th ed., 2020); JARS-Quant + JARS-Mixed; STROBE
ve CONSORT-Mixed; Xie, Dervieux & Riederer (2021) *R Markdown Cookbook*; Aust & Barth (2024)
papaja paketi; Türk Psikologlar Derneği yazım kılavuzu (TPD).

---

## Quarto Proje Yapısı

```
doktoratezi/
├── thesis.qmd               # Kök belge — chapters/*.qmd include eder
├── _quarto.yml              # Proje ayarları (lang, format, freeze)
├── chapters/
│   ├── 01_giris.qmd
│   ├── 02_yontem.qmd
│   ├── 03_bulgular.qmd
│   ├── 04_tartisma.qmd
│   └── 05_sonuc.qmd
├── references/
│   ├── references.bib       # BibTeX
│   └── apa.csl              # APA 7 stil
├── outputs/                 # Tablo + figür artefaktları
└── _freeze/                 # Quarto cache
```

### `_quarto.yml` Standardı

```yaml
project:
  type: book
  output-dir: outputs/quarto

book:
  title: "Tip 1 Diyabetli Çocuklar, Sağlıklı Kardeşleri ve Annelerinde Ebeveynlik
          Tutumu, Beck Depresyonu ve Kardeş İlişkilerinin İncelenmesi"
  author: "Mahir Kurt"
  date: today
  language: tr
  chapters:
    - index.qmd
    - chapters/01_giris.qmd
    - chapters/02_yontem.qmd
    - chapters/03_bulgular.qmd
    - chapters/04_tartisma.qmd
    - chapters/05_sonuc.qmd

bibliography: references/references.bib
csl: references/apa.csl
lang: tr

format:
  pdf:
    documentclass: scrreprt
    papersize: a4
    fontsize: 12pt
    linestretch: 1.5
    geometry:
      - top=3cm
      - bottom=2.5cm
      - left=3.5cm
      - right=2.5cm
    keep-tex: true
    pdf-engine: xelatex
    mainfont: "Times New Roman"
    sansfont: "Arial"
    monofont: "JetBrains Mono"
  html:
    theme: cosmo
    toc: true

execute:
  echo: false
  warning: false
  message: false
  freeze: auto
```

**`freeze: auto`** kritik: sadece chunk değiştiğinde yeniden çalışır; reproducibility için
zaman tasarrufu.

### `thesis.qmd` (Kök)

```qmd
---
title: "Tip 1 Diyabet & Ebeveynlik Tezi"
---

{{< include chapters/01_giris.qmd >}}

{{< include chapters/02_yontem.qmd >}}

{{< include chapters/03_bulgular.qmd >}}

{{< include chapters/04_tartisma.qmd >}}

{{< include chapters/05_sonuc.qmd >}}

# Kaynaklar
::: {#refs}
:::
```

---

## Türkçe APA 7 Yazım Kuralları

### 1. Temel İlke

**Türkçe ana metin** + **parantezde İngilizce** (sadece teknik terim ve özel adlar için).
Kaynakça APA 7 standardı.

### 2. Kaynaklar İçi Atıf

```
Pinquart (2013) tarafından yapılan meta-analiz...
... olduğu bildirilmiştir (Pinquart, 2013).
... (Furman & Buhrmester, 1985).
... (DeVellis & Thorpe, 2022; Hox ve diğerleri, 2018).
```

**"Ve diğerleri" Türkçede.** İngilizcede "et al." yerine TR'de "ve diğerleri" (üçüncü
kişiden itibaren).

### 3. Sayılar

- 10'dan büyük → rakam ("23 katılımcı")
- 10'dan küçük → kelime ("üç anne") — istisna: ölçü, p-değeri, etki büyüklüğü
- Cümle başında her zaman kelime ("Yetmiş bir aile...")
- p-değeri için her zaman "p" italik, < işareti ("p < .001")
- Ondalık ayraç **virgül** (Türkçe norm) → ama tezde **nokta** (uluslararası bilim norm)
  tercih edilir; **tek bir konvansiyon seç ve tut**.

**Bu projedeki karar:** Ondalık ayraç **nokta** (uluslararası bilim norm).

### 4. İstatistik Rakam Formatı

```
M = 23.45, SD = 4.12
t(238) = 2.89, p = .005, d = 0.34 [0.10, 0.58]
χ²(3) = 12.45, p = .006, V = .18
F(2, 478) = 5.62, p = .004, ω² = .020
β = 0.18, SE = 0.07, p = .010, 95% GA [0.04, 0.32]
ICC = .19 [.10, .29]
α = .87, ω = .89
χ²(35) = 48.2, p = .071, CFI = .978, RMSEA = .045 [.000, .072]
```

**Kurallar:**
- p-değeri: 3 ondalık, p < .001 (sıfır kullanma)
- d, r, β: 2 ondalık
- α, ω, ICC: noktalı kısa form (.87, ne 0.87)
- df: parantez içinde
- 95% GA: köşeli parantez

### 5. Kısaltmalar

| Kısaltma | İngilizce | Türkçe |
|----------|-----------|--------|
| GA | CI | Güven Aralığı |
| GH | SE | Standart Hata |
| OS | SD | Standart Sapma |
| Ort | M | Ortalama |
| Med | Mdn | Medyan |
| ÇA | IQR | Çeyrekler Arası |
| n | n | Örneklem büyüklüğü |
| df / sd | df | Serbestlik derecesi |
| p | p | Anlamlılık değeri |
| α / β / γ | — | Yunan harf orijinal |
| Tablo / Şekil | Table / Figure | Tablo / Şekil |

**Tek tutarlı kalın:** Tezde "GA" mı "%95 CI" mı seçtikten sonra DEĞİŞTİRMEME.

### 6. Tablo / Şekil Etiketleme

```
Tablo 3.1
Tip 1 Diyabet ve Kontrol Aileleri Demografik Özellikleri (N = 241)

Şekil 4.2
Aile Düzeyinde EMBU-P Reddetme Alt Ölçek Ortalamaları (95% GA)
```

Quarto cross-ref:

```qmd
... Tablo @tbl-tablo1 ile sunulmuştur.

::: {#tbl-tablo1 tbl-cap="Tip 1 Diyabet ve Kontrol Aileleri Demografik Özellikleri"}
{{< include outputs/tables/tablo1.md >}}
:::
```

---

## Tez Bölümü Yapısı (JARS-Mixed Uyarımlı)

### Giriş (`01_giris.qmd`)

- **Problemin önemi:** T1DM ve aile (epidemiyoloji + Türkiye verisi)
- **Kuramsal çerçeve:** Aile sistemleri, ebeveynlik tutumu, kardeş ilişkisi
- **Literatür özeti:** Pinquart 2013, Sümer (s-EMBU TR), Apalaçi (KİA TR), Hisli (BDI TR)
- **Hipotezler:** H1–H4 — açık, ölçülebilir, ön-kayıtlı
- **Çalışmanın katkısı**

**Uzunluk:** ~25–30 sayfa (tez normu).

### Yöntem (`02_yontem.qmd`) — Mevcut

JARS-Mixed başlıkları:
- Açık bilim, kayıtlılık, veri yönetimi
- Tasarım (case-control, multi-informant)
- Katılımcılar (n, dahil/dışlama, etik)
- Ölçekler (EMBU-P, EMBU-C, BDI, KİA — kanonik form referansı)
- Veri toplama prosedürü
- Veri analizi (FIML/MI, multilevel, SEM, IPTW, sensitivity)
- Etik onay + bilgilendirilmiş onam

Mevcut `chapters/02_yontem.qmd` bu yapıdadır.

### Bulgular (`03_bulgular.qmd`)

JARS-Mixed sırası:
1. **Tablo 1:** Demografi + grup denge (`gtsummary::tbl_summary` + SMD)
2. **Eksik veri raporu:** %, mekanizma, çerçeve
3. **Psikometrik validasyon:** CFA, ω, invariance (alt ölçek bazında)
4. **H1 sonuçları:** Multilevel + IRT theta replikasyonu + (preflight) Bayesian plan
5. **H2 sonuçları:** Aile-mean Welch + APIM + Olsen-Kenny
6. **H3 sonuçları:** ANCOVA + IPTW + AD strata
7. **H4 sonuçları:** WLSMV SEM + multigroup invariance
8. **Sensitivity:** sensemakr, multiverse, NMAR delta

Her bulgu için:
- Tablo + figür atıfı
- Test istatistikleri (yukarıdaki APA format)
- Etki büyüklüğü + GA
- Pratik anlam yorumu (kısa)

### Tartışma (`04_tartisma.qmd`)

JARS-Mixed başlıkları:
1. **Bulgu özeti** (her hipoteze 1 paragraf)
2. **Literatürle karşılaştırma** (Pinquart 2013, De Los Reyes 2015 vs)
3. **Türkiye bağlamı** (kültürel, eğitim, sağlık sistemi)
4. **Kuramsal çıkarımlar** (aile sistemleri, multi-informant)
5. **Klinik/eğitsel çıkarımlar** (DM aile destek programları)
6. **Sınırlılıklar** (kesitsel, survivorship, multi-informant düşük konkordans)
7. **Gelecek araştırma**

### Sonuç (`05_sonuc.qmd`)

Kısa (~5 sayfa). Hipotez bazlı ana çıkarımlar + uygulama önerileri.

---

## R Code Chunk Standardları (Quarto)

### Default Chunk Options

```r
#| echo: false
#| warning: false
#| message: false
#| fig-width: 7
#| fig-height: 5
#| fig-align: center
#| fig-cap: "Şekil X başlığı"
```

### Tablo Üretimi

```{r}
#| label: tbl-h1-primary
#| tbl-cap: "H1 birincil model çıktısı"

tar_load(h1_primary_fixed_effects_table)

h1_primary_fixed_effects_table |>
  gt::gt() |>
  gt::fmt_number(decimals = 2) |>
  gt::cols_label(
    term     = "Parametre",
    estimate = "β",
    std.error = "GH",
    p.value  = "p"
  )
```

### Figür Üretimi

```{r}
#| label: fig-h1-emmeans
#| fig-cap: "H1 EMBU-C alt ölçeklerinde rol etkisi (EMM ± 95% GA)"

tar_load(h1_three_way_emmeans_grid_table)

h1_three_way_emmeans_grid_table |>
  ggplot(aes(role_f, estimate, ymin = conf.low, ymax = conf.high)) +
  geom_pointrange() +
  facet_wrap(~ subscale) +
  labs(x = "Rol", y = "EMM (z-skor)") +
  theme_minimal(base_family = "Times New Roman")
```

### `tar_load()` Pattern

```r
# Bulgular bölümünde target'ları yükle
library(targets)
tar_load(c(
  table1_family_summary_table,
  h1_primary_fixed_effects_table,
  h2_apim_fixed_effects_table,
  h3_iptw_group_effects_table,
  h4_latent_sem_structural_paths_table
))
```

---

## papaja Kullanımı (APA Manuscript)

papaja kanonik APA stilinde dergi makalesi/MS Word şablonu üretir. Tez için Quarto + papaja
kombinasyonu tercih edilir; ya da papaja alone:

```yaml
output:
  papaja::apa6_pdf:
    citation_package: biblatex
    keep_tex: true
```

Quarto + papaja birlikte: papaja şablonunu Quarto LaTeX template olarak adapte etmek mümkün
ama proje şu anda saf Quarto. **Papaja sadece yan yayın (dergi makalesi) için.**

---

## Bibliyografya — `references/references.bib`

### Format

BibTeX standardı:

```bibtex
@book{enders2022,
  author    = {Enders, Craig K.},
  title     = {Applied Missing Data Analysis},
  edition   = {2},
  publisher = {Guilford Press},
  year      = {2022},
  address   = {New York}
}

@article{pinquart2013,
  author  = {Pinquart, Martin},
  title   = {Do the Parent--Child Relationship and Parenting Behaviors Differ
             between Families with a Child with and without Chronic Illness?
             A Meta-Analysis},
  journal = {Journal of Pediatric Psychology},
  volume  = {38},
  number  = {7},
  pages   = {708--721},
  year    = {2013},
  doi     = {10.1093/jpepsy/jst020}
}
```

### CSL — Türkçe APA

`apa.csl` standart APA 7 stilidir; Türkçe varyantlar için:
- "ve diğerleri" → CSL düzenlenmesi
- "(Yıl)" formatı → varsayılan

Genelde standart APA 7 yeter; Türkçe makale ise `bibliography:` içinde Türkçe metin
verilir, CSL stil sadece formatlamayı yapar.

### Atıf Komutları (Quarto)

```qmd
... bildirilmiştir [@pinquart2013].
... [@enders2022, p. 145] tarafından önerilen yöntem...
... Pinquart [-@pinquart2013] tarafından...
... çoklu kaynak [@pinquart2013; @devellis2022; @hox2018].
```

---

## JARS-Mixed Checklist Denetimi

`R/09_reporting_standards.R::audit_reporting_standards()` ve
`scripts/R/09_reporting_standards_audit.R` runner'ı her audit'te aşağıdaki maddeleri
denetler:

- [ ] Açık bilim ön-kayıt referansı
- [ ] Veri yönetimi planı atıfı
- [ ] Etik onay numarası
- [ ] Örneklem büyüklüğü justifikasyonu
- [ ] Veri toplama prosedürü detayı
- [ ] Ölçek psikometrik özet
- [ ] Eksik veri patterni + işlem
- [ ] Etki büyüklüğü + GA
- [ ] Sensitivity analiz raporu
- [ ] Sınırlamalar bölümü
- [ ] Bulgu paylaşma + kod açık erişim

`docs/analiz_planlari/REPORTING-STANDARDS-CHECKLIST.md` insan-okur formundadır; runner
machine-readable status'u üretir.

---

## STROBE (Observational) Checklist

Bu çalışma case-control gözlemsel → STROBE da uygulanır:

- [ ] Title: "case-control study"
- [ ] Abstract: arka plan, amaç, yöntem, bulgu, çıkarım
- [ ] Introduction: bilimsel arka plan + spesifik amaç
- [ ] Methods: tasarım, ortam, katılımcılar, değişkenler, veri kaynakları, bias, örneklem,
      kantitatif değişken, istatistiksel yöntem
- [ ] Results: katılımcı (eligibility, dahil/dışlama akış diyagramı), tanımlayıcı veri,
      ana sonuçlar
- [ ] Discussion: anahtar sonuçlar, sınırlamalar, yorum, genelleme
- [ ] Other: finansman

`STROBE 2007` denetim listesi ile karşılaştırılır; runner çıktısı tezde Ek olarak yer alır.

---

## Türkçe Terim Sözlüğü (Kapsamlı)

| Türkçe | İngilizce | Notlar |
|--------|-----------|--------|
| Etki büyüklüğü | Effect size | Cohen's d için "Cohen d" değil "d" yeter |
| Güven aralığı (GA) | Confidence interval (CI) | %95 GA |
| Çoklu atama | Multiple imputation | "MI" parantezde |
| Eğilim skoru | Propensity score | "PS" parantezde |
| Aracılık (analizi) | Mediation | "Mediasyon" da kabul ama "aracılık" daha Türkçe |
| Düzenleyicilik | Moderation | "Moderasyon" yerine |
| Çok düzeyli model | Multilevel model | "Hiyerarşik lineer model" eş anlamlı |
| Yapısal eşitlik modellemesi | Structural equation modeling (SEM) | "SEM" parantezde |
| Sınıf-içi korelasyon | Intraclass correlation | "ICC" parantezde |
| Aktör-partner bağımlılık modeli | Actor-Partner Interdependence Model (APIM) | "APIM" parantezde |
| Ölçüm değişmezliği | Measurement invariance | configural/metric/scalar düzeyleri |
| Gizil profil analizi | Latent profile analysis (LPA) | — |
| Eşdeğerlik testi | Equivalence testing | "TOST" parantezde |
| Çoklu evren analizi | Multiverse analysis | "specification curve" eş anlamlı |
| Duyarlılık analizi | Sensitivity analysis | — |
| Doğrulayıcı faktör analizi | Confirmatory factor analysis (CFA) | — |
| Açımlayıcı faktör analizi | Exploratory factor analysis (EFA) | — |
| Madde tepki kuramı | Item response theory (IRT) | — |
| Yapısal eksiklik | Structural missingness | — |
| Aşırı koruma | Overprotection | EMBU alt ölçek |
| Reddetme | Rejection | EMBU alt ölçek |
| Karşılaştırma | Comparison | EMBU alt ölçek (TR-spesifik) |
| Sıcaklık | Warmth | EMBU/KİA alt ölçek |
| Çatışma | Conflict | KİA alt ölçek |
| Statü/Güç | Status/Power | KİA alt ölçek |
| Rekabet | Rivalry | KİA alt ölçek |
| Dyad | Dyad / İkili | "İkili" mümkün ama dyad sıkça kalır |
| Latent değişken | Latent variable / Gizil değişken | — |
| Yapısal yol | Structural path | — |
| Robustness Value | Robustness Value (RV) | TR yakın eşdeğer yok; "sağlamlık değeri" çoğu zaman olmaz |

---

## Yazım Stil İlkeleri (Bu Tezde)

1. **Türkçe edilgen ses** — bilimsel norm. "Yapılmıştır", "incelenmiştir", "saptanmıştır."
2. **Etken ses sınırlı** — sadece kişisel pozisyon (Tartışma sonu) ve hipotez ifadelerinde.
3. **Kısa cümleler** — uzun zincirler okuruyu kaybeder. ≤ 25 kelime tercih.
4. **Listeleme** — JARS-Mixed başlık + paragraf; mümkün olduğunda alt bullet'lar.
5. **"Çalışma" veya "araştırma"** — "tez" yerine; "tez" sadece formaliteyle gerektiğinde.
6. **Çapraz referans** — Quarto cross-ref ile (`@tbl-`, `@fig-`, `@sec-`).
7. **Aktif sayım** — Tüm bulgu cümlesi tablo/figür referansıyla başlamayı tercih.

---

## Sık Yapılan Hatalar (Yazım)

1. **"Çalışma sonucunda X'in Y'ye neden olduğu görülmüştür"** — kesinlikle nedensel dile
   geçmedi.
2. **Türkçe + İngilizce terim çift kullanım kafa karışıklığı** — "etki büyüklüğü (effect
   size, ES)" gerekli; sürekli birini seç.
3. **Atama / atık (typo)** — multiple imputation = "çoklu atama" değil "çoklu atama"
   tutarlı.
4. **Ölçek alt ölçek isimleri çevirisinde tutarsızlık** — "Reddetme" mi "Ret" mi? Kanonik
   formdaki ad sabit.
5. **p < .05 kalıbı** — kullan ama her zaman etki büyüklüğü + GA ile.
6. **APA 7 numara kuralı ihlali** — 10'dan büyük rakam, başında kelime.
7. **Quarto chunk içinde `library()` tekrarlama** — bir kere `setup` chunk'ında.
8. **`echo: true` ile kod tezde göstermek** — istisna; chunk-bazlı override yap.
9. **Forgot freeze: auto** — render her seferinde herhangi tüm pipeline tetikler; cache
   kullan.
10. **Kaynakçada `@manual{}` kullanmadan paket atfı** — R paketi atıfı `citation("paket")`
    çıktısı + manuel BibTeX entry.

---

## Hızlı Komutlar

```bash
quarto check                                    # Yapı kontrolü
quarto render thesis.qmd                        # Tüm tez render
quarto preview thesis.qmd                       # Canlı preview

# Sadece bir bölüm
quarto render chapters/03_bulgular.qmd

# Word çıktısı (jüri için)
quarto render thesis.qmd --to docx

# PDF cache temizle
rm -rf _freeze/ .quarto/
quarto render thesis.qmd
```
