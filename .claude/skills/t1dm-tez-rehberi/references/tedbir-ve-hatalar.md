# Tedbir Prensipleri ve Sık Yapılan Hatalar

**Ne zaman oku:** HER inferential analiz öncesi, HER tez paragrafı yazılmadan, HER karşılık
yorum (causal language, segment kıyası, "fark yok" iddiası). Bu dosya zorunlu denetim
listesidir; bypass etme.

**Kaynaklar:** Gelman & Loken (2014) — garden of forking paths; Simpson (1951);
Berkson (1946); Robinson (1950) — ekolojik yanılgı; Lakens (2017) — TOST; Cinelli & Hazlett
(2020) — sensemakr; Steegen ve diğerleri (2016) — multiverse; De Los Reyes ve diğerleri
(2015) — multi-informant.

---

## Yedi Genel Tedbir Prensibi

### 1. Korelasyon Nedensellik Değildir

Aşağıdaki dilbilgisi **sıkı uygulanır**:

| Söylenebilir | Söylenemez |
|--------------|------------|
| "X ile Y ilişkilidir" | "X, Y'ye neden olur" |
| "X, Y'yi yordamaktadır" | "X, Y'ye yol açmaktadır" |
| "X arttıkça Y artar" | "X, Y'yi artırır" |
| "Bağımsız değişken Y ile ilişkili bulunmuştur" | "Bağımsız değişkenin Y üzerindeki etkisi" |

**İstisna:** Sadece RCT veya quasi-experimental + sensitivity destekli + DAG-justified
durumlarda nedensel dile geçilebilir; o zaman da **etki büyüklüğü + GA + sensemakr RV**
zorunlu.

### 2. Çoklu Karşılaştırma Sorunu

20 hipotez α = .05 ile test edilirse ~1 false positive beklenir.

Bu projede:
- **Birincil hipotezler (H1–H4):** Ön-kayıtta sabit; aile-bazında düzeltme yok (her
  hipotez bağımsız confirmatory).
- **Hipotez-içi alt ölçek karşılaştırmaları (örn. EMBU-P 4 alt ölçek):** Holm düzeltmesi
  uygulanır.
- **Keşifsel analizler:** **`[KEŞİFSEL]`** etiketi ile raporlanır; FDR (Benjamini-Hochberg)
  düzeltmesi tercih edilir.

```r
p.adjust(c(0.012, 0.024, 0.034, 0.156), method = "holm")
```

### 3. Simpson Paradoksu

Toplam grup ortalaması bir yönü, alt grup ortalamaları tersini gösterebilir.

**Bu projede zorunlu kontrol:**

```r
# Toplam etki
df_long_scored |>
  group_by(group_dm) |>
  summarise(mean_warmth = mean(embu_c_sicaklik_mean, na.rm = TRUE))

# Alt grup denetimi
df_long_scored |>
  group_by(group_dm, cinsiyet_f) |>
  summarise(mean_warmth = mean(embu_c_sicaklik_mean, na.rm = TRUE))

df_long_scored |>
  group_by(group_dm, cocuk_yas_band_f) |>   # 5–11 vs 12–17
  summarise(mean_warmth = mean(embu_c_sicaklik_mean, na.rm = TRUE))

df_long_scored |>
  group_by(group_dm, ses_tertile_f) |>
  summarise(mean_warmth = mean(embu_c_sicaklik_mean, na.rm = TRUE))
```

Eğer toplamla alt grup yönü farklıysa **runbook'ta açıkla, primer yorumu sınırlandır**.

### 4. Survivorship Bias

Bu projede:
- DM grubu = tedavi alabilen, takipte olan, çalışmaya katılmaya gönüllü olan aileler
  (klinik takipte). Tedaviyi terk eden veya akut komplikasyon yaşayan aileler örnekleme
  girmedi.
- Kontrol grubu = sağlık kurumlarına başvurabilen, anketleri yanıtlayabilen aileler.

**"Bu örneklemde DM ile kontrol arasında EMBU-P Reddetme farkı yok bulunmuştur"** →
ekstreme stres altındaki DM ailelerini temsil etmiyor olabilir. Tartışma bölümünde bu
sınırlama açıkça yer alır.

### 5. Ekolojik Yanılgı

Aile-düzeyi (toplu) bulgular bireysel düzeye taşınmaz.

```r
# Yanlış: Aile ortalaması yüksek → bu ailedeki her çocuk yüksek
# Doğru: Aile ortalaması yüksek → ailenin tüm çocukları için ortalama
```

**Within-between decomposition** (`references/multilevel-aile-yapisi.md`) bu hatayı
otomatik çözer:
- Aile-mean kovaryatı = aileler arası fark (between-family)
- Aile-deviation kovaryatı = aile içinde sapma (within-family)

### 6. Garden of Forking Paths (Gelman & Loken 2014)

Veriyi gördükten sonra spec değiştirmek = p-hacking'in sessiz hali.

**Bu projedeki çözüm:**
1. **Ön-kayıt** (`osf.io/pytfe`) — H1–H4 spec donmuş.
2. **Multiverse analiz** (`specr` `references/nedensellik-ve-ps.md`) — tüm makul
   spec'lerde tahmin dağılımı.
3. **`[KEŞİFSEL]`** etiketi — ön-kayıttan sapan her analiz açıkça etiketli.

**Sapma dökümü** (`PRE-REGISTRATION-DEVIATION-TABLE.md`) zorunludur; tez ekinde tablo
olarak yer alır.

### 7. Sahte Kesinlik (False Precision)

```r
# YANLIŞ
"d = 0.347, p = 0.0233"

# DOĞRU
"d = 0.35 [0.18, 0.52], p = .023"
```

Ondalık hane sayısı verinin gerçek kesinliğini yansıtmalı. Üç haneli p-değeri (.001 hariç)
nadiren gerekli.

---

## Bu Projeye Özel 12 Tehlike

### A. Veri Yönetimi

#### 1. Kanonik Kilit Bypass

Asla `validate_and_load()` çıktısını `tryCatch()` ile yutma. Hash uyuşmazlığı varsa
PIPELINE DURDURULUR. Eğer "küçük bir typo düzeltmek için" CSV'ye dokunmak istersen:

1. Kanonik kilit yeniden oluşturulmalı (`scripts/R/07_verify_reproducibility.R` ile).
2. Tüm downstream invalidate olur.
3. Tezde sapma kaydı.

#### 2. EMBU Madde Drift

Kanonik form öncesinde EMBU-C bazı maddelerinde 4'lü ↔ 6'lı Likert karışımı vardı. Bu
final CSV'de temizlenmiştir; ama `data/cleaned/` veya `data/identified/` altında eski
versiyonlar bulunabilir — bunları analiz girdisi olarak KULLANMA.

#### 3. PII Sızıntısı

`ad.*soyad` regex'iyle eşleşen kolonlar Stage 1'de düşürüldü. Yeni veri eklenirse
`R/05_demographic_text_standardization.R` aynı temizliği yeniden uygulamalı; commit öncesi
`scripts/R/08_ethics_data_governance_audit.R` zorunlu.

`data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/` `.gitignore`'da. **Asla
bu dizinlerden bir dosyayı stage'leme.**

### B. Psikometri

#### 4. Alpha Tek Başına ile Yetinmek

s-EMBU-C tarihsel alpha .49–.69. Bu skor "var" diye kabul edilemez. **CFA + ω + invariance
sırası ihlal edilemez.**

#### 5. Beck'te Madde-Eksiklik Hatası

Beck total = tüm 21 madde tam → toplam. Tek eksik → NA. **%50 kuralı UYGULANMAZ Beck'e.**

#### 6. Modifikasyon İndeksleriyle Modeli "Kurtarmak"

MI > 10 değişikliklerini bir bir uygulayarak fit'i şişirmek = aşırı uyum (overfitting).
Brown 2015 + Kline 2023: sadece teorik gerekçeli + MI > 20 + duyarlılık raporu birlikte.

### C. İstatistik

#### 7. Aile-İçi Bağımsızlık Varsayımı

482 satır = 241 aile × 2. Tek-düzey t-test yapma. Bu projenin en kritik tehlikesi.

#### 8. Antidepresan Kullanımını "Confounder" Sanmak

AD kullanımı:
- DM grubunda farklı oranda olabilir (post-treatment).
- Beck'i etkiler (etki yönüne göre).
- Bir mediator olabilir.

→ Total-effect modelde KOVARYAT YAPILMAZ. AD-stratifiye duyarlılık zorunlu.

#### 9. HbA1c'yi Kontrole Imput Etmek

Yapısal eksiklik. İmput etme = hastalığı imput etmek. Sadece DM altkümede sensitivity.

#### 10. IPTW'yi Trim Etmemek

Uçtaki 99th percentile ağırlıkları varyansı patlatır. Bu projede sabit kural: trim at
99th percentile, raporla effective sample size.

### D. Yorum

#### 11. "İstatistiksel Anlamsız" → "Yok"

```
NEVER: "p = .234 → fark yoktur"
ALWAYS:
"İki grup arasında EMBU-P Sıcaklık ortalamaları arasında anlamlı fark
saptanmamıştır (t(238.4) = 1.19, p = .234, d = 0.15 [-0.10, 0.41]).
TOST eşdeğerlik testi ±0.20 SD bound'unda eşdeğerlik teyit edilememiştir
(t = -0.79, p = .215; t = 3.18, p < .001), bu nedenle bulgu 'fark yok'
olarak değil 'mevcut örneklem büyüklüğüyle 0.20 SD'lik fark kesin olarak
dışlanamamıştır' biçiminde yorumlanır."
```

#### 12. Multi-Informant Konkordanı Yüksek Beklemek

De Los Reyes (2015): Anne-çocuk konkordansı r ≈ 0.20–0.40 normal. Düşüklüğü "ölçüm
hatası" değil, **gelişimsel olgu**. ICC raporla, Bland-Altman çiz; düşük konkordans
"anneler ile çocuklar farklı bilgi kaynaklarıdır" diye yorumlanır — defansif ya da
saldırgan değil.

---

## Faz 0.5 Cautionary Audit Checklist (Her İnferansiyel Çıkarımdan Önce)

Aşağıdaki liste her sorgunun başında uygulanır:

- [ ] **Ortalama + medyan** birlikte var mı?
- [ ] **Aykırı değerler** investigate edildi mi (data error / genuine / different
      population)?
- [ ] **Eksik veri mekanizması** belirtildi mi (MCAR test)?
- [ ] **Bound** bilgisi var mı (floor/ceiling, structural zeros)?
- [ ] **Korelasyon dilbilgisi** doğru mu?
- [ ] **Çoklu karşılaştırma** stratejisi (Holm/FDR/preregistration)?
- [ ] **Simpson paradoksu** taraması (alt grup yön kontrolü)?
- [ ] **Survivorship bias**: Kim örnekleme girmedi?
- [ ] **Ekolojik yanılgı**: Aile-düzeyi vs çocuk-düzeyi yorum tutarlı mı?
- [ ] **Garden of forking paths**: Confirmatory (`osf.io/pytfe`) mı keşifsel mi?
- [ ] **Decimal precision**: Veri kesinliği ile uyumlu mu?
- [ ] **`[KEŞİFSEL]`** etiketi gerekli mi?

---

## Tedbir Tablosu — Hangi Tehlike Hangi Sonuca Yol Açar?

| Tehlike | Yol Açtığı Hata | Bu Projede Çözüm |
|---------|------------------|-------------------|
| Korelasyon → nedensellik | Yanıltıcı politik öneri | DAG + sensemakr RV |
| Çoklu karşılaştırma | Tip I enflasyonu | Ön-kayıt + Holm/FDR |
| Simpson paradoksu | Yön hatası | Alt grup taraması |
| Survivorship | Genelleme hatası | Tartışmada açık sınırlama |
| Ekolojik yanılgı | Bireysel öneri yanılır | Within/between decomposition |
| Forking paths | False positive | Ön-kayıt + multiverse |
| False precision | Sahte kesinlik | 2 haneli ondalık + GA |
| Madde drift | Yanlış skor | Kanonik kilit |
| Modification madness | Aşırı uyum | MI > 20 + teori |
| Aile-içi bağımsızlık varsayımı | SE düşük | Multilevel zorunlu |
| AD kontrol | Mediator-confounder karışım | AD strata |
| Yapısal imputation | Hastalığı imput | DM-only sensitivity |
| IPTW trim yok | Varyans patlaması | 99th percentile trim |
| "Yok" yanlış yorum | Eşdeğerlik iddiası | TOST |
| Konkordans şişirme | Anne–çocuk uyumsuzluğu | ICC + Bland-Altman normal |

---

## Türkçe APA Sablonu (Sınırlamaları Belgeleme)

> "Bu çalışmanın bulguları yorumlanırken üç temel sınırlama göz önünde bulundurulmalıdır.
> İlk olarak, çalışma kesitsel desende olduğundan ebeveyn depresyonu ile çocuk
> ebeveynlik algısı arasındaki ilişkinin zamansal yönü tespit edilemez; nedensel iddia
> bidireksiyonelliği ayrıştırabilen RI-CLPM (Hamaker ve diğerleri, 2015) gerektirir. İkinci
> olarak, DM grubuna katılan aileler aktif klinik takipte olan ve anket tamamlamayı kabul
> eden ailelerdir; daha ağır metabolik kontrolsüzlüğe veya tedavi terkine sahip aileler
> örnekleme girmemiş olabilir (survivorship bias). Üçüncü olarak, ölçülmemiş karıştırıcılara
> duyarlılık sensemakr (Cinelli & Hazlett, 2020) çerçevesi ile %18 Robustness Value
> düzeyinde değerlendirilmiş olsa da bu, ölçülmeyen tüm faktörleri tüketmemektedir; özellikle
> aile içi iletişim örüntüleri ve baba ebeveynlik tutumu gibi bu çalışmada toplanmamış
> değişkenler bulguları değiştirebilir."

---

## SAP v3.0 Genişletilmiş KISIM-Spesifik Tehlikeler

KISIM VI–XVII'den gelen yeni risk kategorileri:

### 13. Multiverse cherry-picking (KISIM XI)

**Tehlike:** 1800 spesifikasyon arasından "anlamlı" çıkanları öne çıkarma.
**Kontrol:**
- **Tüm** spec dağılımı raporlanır (median + %5-%95 aralık)
- Inferential test (Simonsohn 2020 permütasyon) zorunlu — descriptive değil
- "Spec'lerde anlamlı" oranı + `[KEŞİFSEL]` etiketi
**Saptama:** "x koşulda fark çıktı" cümlesi → multiverse'in tek bir slice'ı seçildi mi?

### 14. RSA küçük-örneklem aşırı yorumu (KISIM V H5)

**Tehlike:** RSA n=120 alt-grupta unstable; a4 (tutarsızlık) parametresinin CI bandı geniş.
**Kontrol:**
- n_min ≥ 100 alt-grup için
- Bootstrap CI (BCa) zorunlu, asimptotik değil
- Polynomial bileşenler (b3, b4, b5) collinearity kontrol
- `[KEŞİFSEL]` etiketi RSA için varsayılan
**Saptama:** "DM grubunda a4 = 0.42 anlamlı" → CI [0.10, 0.74] mu yoksa [-0.18, 1.02] mu?

### 15. Bayesian prior allegiance (KISIM XII)

**Tehlike:** "Pinquart-temelli prior kullandık" diyerek aslında sonuç-yönlü prior seçmek.
**Kontrol:**
- Prior derivation gerekçesi **kod yorumunda** belge (`prior(normal(0.30, 0.50), ...)` neden bu SD?)
- Sensitivity: 3 prior width (default / yarı / iki kat) ile BF/posterior nasıl değişiyor?
- `sample_prior = "yes"` zorunlu (Savage-Dickey için)
**Saptama:** Prior SD < 0.10 kullanılmış → çok dar; literatür güveni 1 SD'den dar olamaz

### 16. Network causal claim hatası (KISIM VIII)

**Tehlike:** GGM partial correlation görselleştirmeyi "X → Y nedensel" diye yorumlamak.
**Kontrol:**
- "Beck → Reddetme" değil "Beck ile Reddetme arasında koşullu bağımlılık var" dilbilgisi
- DAG yorumu sadece KISIM III nedensellik dosyasında
- Network "merkezilik" → klinik müdahale önceliği değil; istatistiksel nokta
**Saptama:** Network yorumu içinde "neden olur", "tetikler", "kötüleştirir" kelimeleri

### 17. LPA "label-driven" yorumu (KISIM VII)

**Tehlike:** "Tükenmiş profil" etiketinin profilin gerçek özelliklerinden bağımsız klinik karar
ürünü olarak kullanılması.
**Kontrol:**
- Profil etiketleri **betimsel** (içerik tabanlı), klinik tanı değil
- Profil membership uncertainty (modal vs probabilistic) raporlandı
- Profil × outcome regresyonlarında `lpa_class` factor değil; classification error eklenmiş
**Saptama:** "'Tükenmiş' profilin tedavisi..." cümleleri → klinik öneri için validation eksik

### 18. Mediation: bidirectional confusion (KISIM VI)

**Tehlike:** Cross-sectional veride "Beck → EMBU-P → EMBU-C" sırasını veri ile *test* edilmiş gibi
sunmak.
**Kontrol:**
- Mediator sırası **DAG-temelli varsayım**, veri test etmez
- "Anne EMBU-P çocuk EMBU-C'yi etkiliyor olabilir" değil "DAG'da bu yön postulate edildi"
- RI-CLPM tarihsel veri yoksa bu sınırlılık tartışmada
**Saptama:** "Mediation analizi göstermiştir ki..." → veri test etmedi, model varsaydı

### 19. DCA: gerçekçi olmayan threshold (KISIM IX)

**Tehlike:** DCA'da p > .50 eşiklerinde "net benefit" göstermek (klinik anlamsız).
**Kontrol:**
- Threshold range klinik anlamlı (0.05–0.50)
- Müdahale maliyeti ↔ tedavi vermeme zararı oranı belirtilir
- "Treat all" alternatifi hep gösterilir
**Saptama:** DCA grafiğinde threshold = 0.80'de "fayda var" yorumu → klinik anlamsız

### 20. Falsification cherry-pick (KISIM XI)

**Tehlike:** Üç falsification testten birinde "negatif" sonuç çıkınca "tezi destekliyor" demek.
**Kontrol:**
- **Önceden tanımlanmış** falsification senaryoları
- Tüm sonuçlar (pozitif + negatif + null) raporlanır
- Negatif kontrol *anlamsız* çıkma şartı → öyle olduysa "tehdit yok" denir, ama anlamlı çıkarsa
  yapısal sorun bayrağı
**Saptama:** "DM kısa süre alt-grupta etki kayboldu, hipotez doğrulandı" → diğer iki test ne çıktı?

### 21. KEŞİFSEL etiketinin kötüye kullanımı (KISIM XV)

**Tehlike:** OSF kayıtlı analizden sapınca "[KEŞİFSEL] etiketleyince güvenlide" düşüncesi.
**Kontrol:**
- `[KEŞİFSEL]` ≠ "yorum gevşekleşir"; aynı tedbir denetimleri
- Sapma `PRE-REGISTRATION-DEVIATION-TABLE.md`'ye işlenir
- Tezde ek bölümünde tablo halinde belge
- Yayın aşamasında "exploratory" ayrı section
**Saptama:** Bir paragrafta `[KEŞİFSEL]` etiketi var ama "anlamlı bulundu" iddiası net

### 22. papaja/apaquarto fit kontrolü atlamak (KISIM XIV)

**Tehlike:** Otomatik üretilen `report::report()` çıktısının manuel kontrol olmadan tezde
kullanılması (p-değer formatı, ondalık kuralı, terminoloji).
**Kontrol:**
- `report()` çıktısı **taslak**, son hâl değil
- Türkçe APA terim sözlüğü kontrolü ([`tez-yazim-rehberi.md`](tez-yazim-rehberi.md))
- p < .001, d = 0.34 [0.12, 0.56], 2 ondalık kuralları
- Türk tirelemesi (`lang: tr`) doğru mu?
**Saptama:** Tezde "p = 0.000" → APA 7'ye aykırı; "< .001" yazılmalı

### 23. Risk skoru içsel validation eksik (KISIM IX)

**Tehlike:** AUC = .78 hesaplandı ama bootstrap/CV yok → optimistic bias.
**Kontrol:**
- Bootstrap (.632+) veya 10-fold CV
- Calibration **bootstrap-corrected** (B = 1000)
- Eğitim AUC ile düzeltilmiş AUC farkı raporlanır
- Dış validation yok = "keşifsel risk skoru" etiketi
**Saptama:** "AUC = .82" tek değer + CI yok + CV yok

### 24. H5 strateji-shopping (KISIM V)

**Tehlike:** 5 dyadic stratejiden 3'ü null çıkınca "RSA anlamlı" diye öne çıkarmak.
**Kontrol:**
- 5 strateji **paralel** raporlanır (hepsi aynı tabloda)
- Triangulation: en az 3 uyumlu → güçlü; aksi halde discrepant tartışmada açık
- Tek-strateji "gerçek" ilan edilmez
**Saptama:** Tezde sadece RSA sonucu raporlanmış → ICC + CFM + k-coef nerede?

---

## Hızlı Bayrak Tablosu — Yeni KISIM Tehlikeleri

| Sinyal | Tehlike # | Düzeltme |
|---|---|---|
| Multiverse'den tek slice | 13 | Tüm dağılım + inferential |
| RSA n_alt < 100 + dar yorum | 14 | BCa + KEŞİFSEL |
| Prior SD < 0.10 | 15 | Sensitivity prior |
| GGM "neden olur" dili | 16 | Koşullu bağımlılık dilbilgisi |
| LPA profil → klinik tedavi | 17 | Validation gerekli |
| "Mediation göstermiştir" | 18 | DAG varsayımı |
| DCA threshold > 0.50 | 19 | 0.05–0.50 range |
| Tek falsification "destekledi" | 20 | Üç senaryo birlikte |
| KEŞİFSEL + "anlamlı bulduk" | 21 | Sapma tablosu |
| `report()` doğrudan tezde | 22 | Türkçe APA elden kontrol |
| AUC tek nokta + CV yok | 23 | Bootstrap optimistic correction |
| H5 sadece 1 strateji | 24 | 5 paralel zorunlu |
