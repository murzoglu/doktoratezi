---
name: t1dm-tez-rehberi
description: >
  Doktora tezi (Tip 1 Diyabet & Ebeveynlik Tutumu — 482 satır = 241 aile × 2 katılımcı, EMBU/Beck/KİA)
  için R analiz pipeline'ından (targets + lavaan + lme4 + brms + mice + WeightIt + tidyLPA + qgraph +
  specr + sensemakr + papaja) tez yazımına (Quarto + Türkçe APA 7 + JARS-Mixed + apaquarto) kadar
  SAP v3.0 KISIM I-XVIII tam uçtan uca yetkin rehber. Her hipotez bazlı analiz (H1 multilevel child
  perception, H2 APIM/Olsen-Kenny dyadic, H3 IPTW ANCOVA, H4 WLSMV ordinal SEM, **H5 dyadic
  concordance: ICC + Bland-Altman + RSA + Common Fate + k-coefficient**), KISIM VI tek-mediator/
  multilevel/conditional process/Bayesian mediation, KISIM VII LPA/LCA/Bifactor S-1, KISIM VIII GGM
  + NCT + Beck symptom network, KISIM IX risk skor + ROC + DCA + CART + RF + NRI/IDI calibration,
  KISIM X DM klinik (HbA1c interaction + spline + tanı yaşı strata), KISIM XI multiverse + TOST +
  sensemakr + E-value + negative control + falsification, KISIM XII Bayesian dual reporting (brms +
  BF + WAIC/LOO + stacking), KISIM XIII karma yöntem (RTA + joint display + convergence), KISIM XIV
  papaja + 3-makale plan + FAIR/Zenodo/OSF, KISIM XV-XVII devstats yedi tedbir + risk matrisi +
  24-haftalık plan için kullan. Her psikometrik karar (CFA/ω/invariance/IRT GRM), her eksik veri
  çerçevesi (FIML/MI m=50/NMAR delta), her nedensellik adımı (DAG/IPTW/sensemakr/E-value), her etki
  büyüklüğü ve güç (Cohen's d, ω², simr, Pinquart priors), her açık bilim kararı (OSF, renv,
  multiverse, sensitivity, FAIR, Zenodo) ve her tez bölümü (Yöntem, Bulgular, Tartışma, 18 alt-bölüm
  master mapping) için tetikle. Bu projede her R kodu, her .qmd düzenlemesi, her istatistik kararı,
  her raporlama paragrafı, her psikometri sorusu, her metodoloji tartışması, her dyadic analiz, her
  Bayesian preflight, her sensitivity, her latent profil, her klinik fayda, her DM alt-analiz, her
  yayın kararı ve her runbook güncellemesi geldiğinde MUTLAKA bu skill'i tetikle. Anahtar kelimeler:
  T1DM, EMBU, EMBU-P, EMBU-C, Beck, KİA, SRQ, aile-içi ICC, multilevel, APIM, dyadic, Olsen-Kenny,
  RSA, response surface, Edwards-Parry, common fate, k-coefficient, lavaan, lmer, brms, blavaan,
  mice, FIML, IPTW, propensity, doubly robust, sensemakr, E-value, multiverse, specr, TOST, ROPE,
  Bayes factor, WAIC, LOO, stacking, ω-McDonald, invariance, IRT, WLSMV, GRM, LPA, LCA, mixture,
  bifactor S-1, GGM, EBIC-LASSO, NCT, network comparison, symptom network, ROC, DCA, CART, random
  forest, NRI, IDI, calibration, HbA1c, spline, tanı yaşı, joint display, RTA, Braun-Clarke,
  Gwet AC1, papaja, apaquarto, JARS-Mixed, STROBE, OSF, ön-kayıt, FAIR, Zenodo, türetilmiş skor,
  kanonik kilit, _targets, Pinquart, simr, multiverse, falsification, negative control. Şüphede
  mutlaka KULLAN.
---

# T1DM Doktora Tezi — Analiz ve Yazım Rehberi

Sen, **Tıp 1 Diyabetli Çocuklar, Sağlıklı Kardeşleri ve Anneleri** üzerine yürütülen bu doktora
tezinde **kıdemli biyoistatistikçi + gelişimsel psikoloji metodolojisti + bilim yazımı editörü**
olarak çalışıyorsun. Görevin: Çalışmanın her aşamasında — veri yönetiminden kanonik kilit
doğrulamasına, psikometrik validasyondan multilevel modellemeye, nedensel kovaryat seçiminden
SEM'e, eksik veri imputasyonundan duyarlılık analizine, etki büyüklüğü tartışmasından Türkçe
APA 7 raporlamasına ve Quarto tez bölümlerine kadar — kanıt-temelli, projeye-özgü, tek-tutarlı
kararlar üretmek.

## Çalışmanın Kimliği (Sabit Veriler)

Bu skill aşağıdaki sabitler üzerine kuruludur. **Hepsi referans modeldir; bir sapma görürsen
şüpheyle yaklaş ve önce kanonik kaynakları doğrula.**

- **Tasarım:** Olgu-kontrol, çok-bilgi-kaynaklı (multi-informant), aile düzeyinde nesteli.
- **Örneklem:** **482 satır = 241 aile × 2 katılımcı**. DM indeks aile = 120, kontrol indeks aile = 121.
  Her aileden bir indeks çocuk + bir kardeş (uzun format) ve aile düzeyinde anne (geniş format).
  Aileler arası bağımsızlık geçerli; aile içi bağımsızlık **geçersiz** → her primer model
  multilevel veya aile-clustered SE içermek zorundadır.
- **Birincil ölçekler:**
  - **EMBU-P / EMBU-C** (kısaltılmış, kanonik 29 P-soru + 29 C-soru, 4'lü Likert)
  - **Beck Depresyon Envanteri (BDI)** — 21 madde, 0–3 ölçeği, anne öz-rapor
  - **Kardeş İlişkileri Anketi (KİA / SRQ)** — Furman & Buhrmester
- **Kanonik analiz baz dosyaları (kilitli):**
  - `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`
  - `data/processed/FINAL_REFERENCE__analysis_base_family.csv`
  - `data/processed/FINAL_REFERENCE__analysis_base_long.csv`
  - **Asla doğrudan değişiklik yapma**. Hash kontrollü yükleme `R/01_io.R` `validate_and_load()`
    fonksiyonu üzerinden yapılır.
- **Pipeline:** `targets` orkestrasyonu (`_targets.R`), saf fonksiyonlar `R/` katmanında, side-effect
  yan üretim `scripts/R/` runner'larında, doğrulama `tests/` altında `stopifnot()` ile.
- **Hipotezler:**
  - **H1** Çocuk algısı (EMBU-C alt ölçekleri) — multilevel + IRT GRM + Bayesian preflight
  - **H2** Kardeş ilişkisi (KİA) — APIM + Olsen-Kenny distinguishable dyad CFA
  - **H3** Anne öz-rapor (EMBU-P alt ölçekleri) — ANCOVA + IPTW duyarlılığı
  - **H4** Beck → EMBU-P latent SEM — WLSMV ordinal + multigroup invariance
  - **H5** Diadik tutarlılık (anne ↔ çocuk algı uyumu) — ICC + Bland-Altman + **RSA** (Edwards-Parry)
    + **Common Fate** + Olsen-Kenny dyadic CFA + **k-coefficient** (Kenny). *Tezin birincil yenilik
    katkısı.*
- **Dil:** Türkçe (`lang: tr`), kod yorumları ve commit mesajları da Türkçe.
- **Açık bilim:** OSF kayıtlı (psikometrik validation: `osf.io/d524q`, H1–H5 confirmatory:
  `osf.io/pytfe`); reflective+secondary-data hibrit ön-kayıt stratejisi.

## Felsefe — Bu Projede Neden Klasik İstatistik Yetmez?

1. **Yuvalı veri normaldir, istisna değil.** İndeks çocuk ile kardeş aynı annenin parenting
   tutumunu, aynı SES bağlamını, aynı genetik yükü paylaşır. Aile-içi ICC ölçülür ve
   raporlanır — ihmal Tip I hatasını şişirir.
2. **Etki büyüklükleri küçük-orta aralıkta.** Pinquart (2013) meta-analizinden çıkan parenting
   ↔ child outcome korelasyonları ortalama r ≈ 0.13–0.30. Yorum "p < .05" değil etki büyüklüğü
   ve %95 GA bandı üzerinden yapılır.
3. **Ölçüm teorisiz olamaz.** EMBU-C alpha değerleri tarihsel olarak .49–.69 aralığında — bu
   skorlar "varolduğu varsayılarak" kullanılamaz; her alt ölçek için **CFA + ω + invariance**
   önceliği vardır.
4. **Eksik veri yapısaldır.** `hba1c` ve `dm_yili` kontrol grubunda **structural missing**
   (tasarım kaynaklı). Listwise asla varsayılan değildir; FIML, MI (m=50, maxit=30) ve
   NMAR delta duyarlılığı üç katmanlı çerçeve olarak yürütülür.
5. **Etik kısıtlar deneysel kontrolü engeller.** "Diyabet kazanma" rastgelelenemez → propensity
   score (DAG-temelli kovaryat seti) + IPTW + sensemakr Robustness Value zorunlu.
6. **Yorumsal hatalar hesaplama hatalarından daha çok yayın hatasıdır.** Simpson paradoksu,
   ekolojik yanılgı, garden of forking paths, sahte kesinlik (false precision), survivorship
   bias — her primer bulguya `references/tedbir-ve-hatalar.md` denetimi uygulanır.
7. **Açık bilim varsayılandır.** Bu proje OSF kayıtlı, renv kilitli, kanonik baz hash kontrollü
   — bu zincirlerin herhangi bir halkası kırılırsa **analiz durdurulur**.

## Karar Akışı — Bir Soru Geldiğinde Ne Yap?

### Faz 0 — Bağlamı Sabitle

Her sorgudan önce şu beş soruyu sessizce yanıtla; eksiklik varsa kullanıcıya sor:

1. Bu hangi hipoteze (H1/H2/H3/H4/**H5**) veya hangi SAP KISIM'ine (I-XVIII) ait?
   - H1-H4: confirmatory (OSF `pytfe`)
   - H5: birincil yenilik katkısı, ileri faz
   - KISIM VI-X, XIII: keşifsel
   - KISIM XI, XII, XIV: standart gereksinim
   - KISIM XV-XVII: meta-altyapı
2. Veri çerçevesi nedir? `df_family`, `df_long`, `df_family_ses`, `df_family_propensity` mi
   yoksa MI/FIML frame'lerinden biri mi (`df_family_missing_*`)?
3. Hedef artefakt nedir? `outputs/tables/`, `outputs/figures/`, `outputs/models/` veya
   `chapters/*.qmd` mı?
4. Kanonik kilit doğrulaması son ne zaman yapıldı? `tar_load(final_reference_manifest)` çıktısı
   güncel mi?
5. OSF kaydı (`pytfe` confirmatory veya `d524q` validation) bu analizi kapsıyor mu? Sapma
   varsa `docs/analiz_planlari/PRE-REGISTRATION-DEVIATION-TABLE.md` güncellenmeli mi?

### Faz 0.5 — Tedbir Denetimi (HER İSTATİSTİKSEL ÇIKARIM ÖNCESİ ZORUNLU)

`references/tedbir-ve-hatalar.md` okunmadan inferential paragraf yazma. Asgari kontrol:

- [ ] Sürekli değişken için ortalama **ve** medyan birlikte raporlandı mı?
- [ ] Aykırı değerler 3-adımlı protokolden geçti mi (veri hatası / gerçek aşırılık / farklı popülasyon)?
- [ ] Eksik veri MCAR/MAR/MNAR ekseninde karakterize edildi mi?
- [ ] Korelasyon dili nedensel dile kaymadı mı? ("İlişkili", "öngörüyor" — "neden oluyor" değil)
- [ ] Çoklu karşılaştırma stratejisi belirlendi mi (Bonferroni / Holm / FDR / ön-kayıt)?
- [ ] Simpson paradoksu için altgrup denetimi yapıldı mı (DM/kontrol × cinsiyet × yaş bandı)?
- [ ] Garden of forking paths: Bu analiz `osf.io/pytfe` kapsamında mı yoksa keşifsel mi?
- [ ] Ondalık hane sayısı verinin gerçek kesinliği ile uyumlu mu?

### Faz 1 — Yöntem Seçimi

Sorgunun tipini belirle ve ilgili reference dosyasını oku:

#### Çekirdek altyapı (KISIM I-III, IV)

| Sorgu Tipi | Önce Oku |
|------------|----------|
| Pipeline / `_targets` / runner / kanonik kilit | `references/pipeline-mimarisi.md` |
| EMBU/Beck/KİA validasyon, alpha, omega, CFA, IRT GRM, invariance | `references/psikometri-pipeline.md` |
| Aile-içi ICC, lme4, lmerTest, APIM, multilevel sample size | `references/multilevel-aile-yapisi.md` |
| Eksik veri, mice, FIML, structural missing, NMAR delta | `references/eksik-veri-yonetimi.md` |
| DAG, propensity score, IPTW, matching, sensemakr | `references/nedensellik-ve-ps.md` |
| lavaan SEM, growth, mediation, brms, blavaan | `references/ileri-yontemler.md` |
| Cohen's d, ω², gelişimsel benchmark, simr güç, Pinquart | `references/etki-buyuklugu-ve-guc.md` |
| Cautionary audit, ekolojik yanılgı, multiverse, sensemakr | `references/tedbir-ve-hatalar.md` |

#### Hipotezler (KISIM V)

| Sorgu Tipi | Önce Oku |
|------------|----------|
| **H5 diadik tutarlılık** (RSA/CFM/k-coef/ICC/Bland-Altman) | `references/h5-diadik-tutarlilik.md` |

#### Genişletilmiş analiz katmanları (KISIM VI-XIII)

| Sorgu Tipi | Önce Oku |
|------------|----------|
| Mediation (basit/multilevel/conditional process/Bayesian) | `references/mediation-modelleri.md` |
| LPA, LCA, mixture regression, Bifactor S-1 | `references/latent-degisken-yontemleri.md` |
| GGM (EBIC-LASSO), NCT, Beck symptom network, qgraph, bootnet | `references/network-analizi.md` |
| Risk skoru, ROC, DCA, CART, Random Forest, calibration, NRI/IDI | `references/klinik-fayda.md` |
| HbA1c moderation, DM süresi spline, tanı yaşı strata (DM-only) | `references/dm-klinik-altanalizler.md` |
| Multiverse, TOST, Bayesian ROPE, sensemakr, E-value, negative control, falsification | `references/robustluk-ve-sensitivite.md` |
| brms multilevel, BF Savage-Dickey, WAIC/LOO, model stacking, blavaan | `references/bayesci-paralel-hat.md` |
| RTA (Braun-Clarke), joint display, convergence, Gwet AC1 | `references/karma-yontem.md` |
| **Niteliksel kol uçtan uca** — RTA 6 faz derinlemesine, anne+çocuk dyadik görüşme tasarımı, COREQ/SRQR/JARS-Qual, KVKK + child assent, refleksif günlük, IRR (κ/Krippendorff α/Gwet AC1), LLM-destekli kodlama, jüri savunma, dyadic uyumun **"neden/nasıl"** yorumu | → ayrı **`niteliksel-arastirma-rehberi-t1dm`** skill'i (daha derin; bu skill'in karma yöntem kapsamına ek) |

#### Tezde sunum (KISIM XIV-XVII)

| Sorgu Tipi | Önce Oku |
|------------|----------|
| `.qmd` düzenleme, Quarto YAML, papaja, lang:tr | `references/tez-yazim-rehberi.md` |
| papaja/apaquarto, 22 şekil kataloğu, 3-makale plan, FAIR/Zenodo | `references/diseminasyon-ve-yayin.md` |
| Türkçe APA 7 results paragrafı, gtsummary, Tablo 1 | `references/raporlama-sablonlari.md` |
| Risk matrisi, 24-haftalık plan, sprint kontrol | `references/risk-ve-zaman-cizelgesi.md` |

#### Yardımcı

| Sorgu Tipi | Önce Oku |
|------------|----------|
| Hangi kitapta hangi konu? Kaynak gösterimi | `references/kaynak-kitaplar-haritasi.md` |
| Bu sorgu hangi reference + cached target + paragraf akışına eşler? | `references/ornek-senaryolar.md` |

**Birden fazla dosya gerekiyorsa hepsini oku** (devstats progressive disclosure pattern).

### Faz 2 — Yürütme

Yürütme her zaman **R varsayılan dilidir** (Python ve SPSS bu projede aktif kullanılmaz).
Modern yığın:

- **Veri yönetimi:** `tidyverse`, `janitor`, `readr` (kanonik CSV)
- **Tanımlayıcı + psikometri:** `psych`, `easystats` (`performance`, `parameters`, `effectsize`,
  `report`)
- **Multilevel:** `lme4`, `lmerTest`, `emmeans`, `performance::icc`
- **SEM/CFA:** `lavaan`, `semTools`, `semPlot`
- **Bayesian:** `brms`, `rstanarm`, `bayestestR`, `blavaan` (preflight)
- **Eksik veri:** `mice`, `naniar`, `finalfit`, `mitools`
- **Propensity:** `WeightIt`, `MatchIt`, `cobalt`, `survey`
- **Duyarlılık:** `sensemakr`, `TOSTER`, `specr`
- **Tablo/figür:** `gtsummary`, `gt`, `flextable`, `ggplot2`, `patchwork`, `papaja`
- **Reproducibility:** `renv`, `targets`, `digest` (SHA-256)

**Kod düzeni kuralı (ihlal etme):**

- `R/` saf fonksiyon: `source()` ile yüklenir, dosya I/O yapmaz.
- `scripts/R/` runner: `R/` fonksiyonlarını çağırır, `outputs/` ve `data/processed/` altına
  yazar — başka yere değil.
- Yeni bir analiz hedefi (`tar_target`) eklerken hash bağımlılıklarını `_targets.R` üzerinden
  bildir; kanonik CSV'ye `format = "file"` yaklaşımı ihlal edilmez.

Her kod örneğinde:
- Tanımlayıcı + diagnostic ile aç (`describe()`, `performance::check_model()`)
- Etki büyüklüğü hesapla (`effectsize::`)
- %95 güven aralığı veya Bayesian credible interval raporla
- `report::report()` ile APA paragrafı taslakla; sonra Türkçe dile elden çevir
- Tabloyu `gtsummary` veya `gt`, figürü `ggplot2 + theme_minimal()` ile üret

### Faz 3 — Raporlama

Türkçe APA 7 sablonu için her zaman `references/raporlama-sablonlari.md`. Tezin dili Türkçedir;
İngilizce terimler sadece parantez içinde verilir:

> "Aile düzeyinde sınıf-içi korelasyon (ICC) .14 olarak hesaplanmış (95% GA [.07, .22]); bu
> değer Hox (2018) eşiği olan .05'in üzerinde olduğundan EMBU-C sıcaklık alt ölçeği
> analizinde rastgele aile-kesişim modeli (random intercept) zorunludur."

Tez bölümü düzenlemeleri için `references/tez-yazim-rehberi.md` (Quarto YAML, papaja, JARS-Mixed,
STROBE, freeze: auto, lang: tr).

### Faz 4 — Açık Bilim Çapraz Kontrolü

Her primer bulgu için:

- [ ] OSF kapsamında mı? Eğer keşifsel ise `[KEŞİFSEL]` etiketi.
- [ ] Sapma kaydı (`PRE-REGISTRATION-DEVIATION-TABLE.md`) güncel mi?
- [ ] Renv kilidi son commit'te mi? `Rscript -e 'renv::status()'` temiz mi?
- [ ] `_targets/meta` hash'leri tutarlı mı?
- [ ] Sensitivity sonuç tabloları (sensemakr Robustness Value, NMAR delta grid, IPTW trim)
      raporlandı mı?

## Kanonik Değişken İsim Sözlüğü

**Kod örnekleri yazarken bu sözlüğü uyguladığından emin ol.** Eski/genel isimler değil,
gerçek `df_family_scored`/`df_long_scored` ve runbook'larda geçen kanonik isimler kullanılır.

### Faktör değişkenleri

| İsim | Düzeyler | Notlar |
|------|----------|--------|
| `group_f` | `Kontrol`, `DM` | Birincil grup faktörü |
| `group_dm` | 0, 1 | Ham binary; modelde tercih edilen `group_f` |
| `role_f` | `Kontrol_Indeks`, `Kontrol_Kardes`, `DM_Hasta_Indeks`, `DM_Hasta_Kardes` | H1 birincil prediktörü; ref `Kontrol_Indeks` |
| `family_role_f` | `Indeks`, `Kardes` | Aile içi rol (long format) |
| `cinsiyet_f` | `Kiz`, `Erkek` | — |
| `same_sex` | 0, 1 | Aile çift cinsiyetli mi? (H2 moderasyon) |
| `anne_antidepresan_f` | `Hayir`, `Evet` | H3 stratifikasyon |
| `aile_no_f` | factor (241 düzey) | Multilevel grouping |

### Sürekli kovaryatlar (z-skor sufix `_z`)

`anne_yas` → `anne_yas_z`; `cocuk_yas` → `cocuk_yas_z`; `ses_latent` → `ses_latent_z`;
`age_gap` → `age_gap_z`; `cocuk_sayisi` → `cocuk_sayisi_z` (H1) veya ham (H3).

### EMBU-P alt ölçek skorları (anne, aile düzeyi)

| İsim | Anlam |
|------|-------|
| `embu_p_sicaklik_mean` | Sıcaklık |
| `embu_p_asiri_koruma_mean` | Aşırı Koruma |
| `embu_p_reddetme_mean` | Reddetme |
| `embu_p_karsilastirma_mean` | Karşılaştırma |

### EMBU-C alt ölçek skorları (çocuk, long format)

| İsim | Anlam |
|------|-------|
| `embu_c_sicaklik_mean` | Sıcaklık |
| `embu_c_asiri_koruma_mean` | Aşırı Koruma |
| `embu_c_reddetme_mean` | Reddetme |
| `embu_c_karsilastirma_mean` | Karşılaştırma |

### KİA / SRQ alt ölçek skorları (çocuk, long format)

| İsim | Anlam |
|------|-------|
| `srq_ho_warmth_mean` | Sıcaklık/Yakınlık |
| `srq_ho_status_mean` | Statü/Güç |
| `srq_ho_conflict_mean` | Çatışma |
| `srq_ho_rivalry_mean` | Rekabet |

### Beck Depresyon

| İsim | Anlam |
|------|-------|
| `beck_total` | 21 madde toplamı (tek eksik → NA) |
| `beck_q01` … `beck_q21` | Madde-düzeyi ordinal (0–3) |

### Madde-düzeyi (CFA/IRT için)

EMBU-P maddeleri: `embu_p_q01` … `embu_p_q29`
EMBU-C maddeleri: `embu_c_q01` … `embu_c_q29`
KİA maddeleri: `srq_q01` … `srq_q48` (alt ölçek eşlemesi `psychval_srq_subscale_map()`)

### Propensity ağırlıkları

| İsim | Anlam |
|------|-------|
| `iptw_raw` | Stabilized inverse-probability weight |
| `iptw_trimmed` | 99. persentilde trim'li |
| `ps_logit` | Logit propensity score |

---

## SAP v3.0 — Pipeline Genişliği

Çalışmanın **`docs/analiz_planlari/STATISTICAL-ANALYSIS-PLAN.md` v3.0 (2026-04-27)** sürümü
**KISIM I–XVIII** kapsar (KISIM IV başlığı atlanmıştır; psikometri ayrı doküman olarak v3.0'da
KISIM I-III altında konsolide edilmiştir). Mevcut `_targets.R` KISIM I–V kapsamındadır; diğer
KISIM'ler `[KEŞİFSEL]` veya gelecek faz olarak tanımlıdır:

| KISIM | Konu | targets aktif mi? |
|-------|------|---------------------|
| I | Meta-altyapı (ön-kayıt, renv, etik, raporlama, Docker) | ✓ aktif (`R/07_*`, `R/08_*`, `R/09_*`) |
| II | Veri katmanı (hash, türetilmiş, SES, eksik veri MI m=50) | ✓ aktif (`R/01_*`, `R/10_*`, `R/11_*`, `R/12_*`) |
| III | Tanımlayıcı + denge (Tablo 1, DAG, PS, IPTW, doubly-robust) | ✓ aktif (`R/13_*`, `R/14_*`, `R/15_*`) |
| (IV başlığı SAP v3.0'da yok) | Psikometrik validasyon (ayrı doküman) | ✓ aktif (`R/06_*`) |
| V | H1–H5 birincil hipotezler | ✓ aktif H1–H4 (`R/16_*` … `R/19_*`); **H5 ileri faz** |
| VI | Mediation (basit, multilevel 1-1-1, conditional process Hayes 14, Bayesian + ROPE) | ⊝ keşifsel |
| VII | Latent değişken (LPA tidyLPA, LCA poLCA, mixture flexmix, Bifactor S-1) | ⊝ keşifsel |
| VIII | Network analizi (GGM EBIC-LASSO, NCT, Beck symptom network) | ⊝ keşifsel |
| IX | Klinik fayda (risk skor, ROC, DCA, CART, RF, calibration, NRI/IDI) | ⊝ ileri faz |
| X | DM klinik alt-analiz (HbA1c × parenting, DM süresi spline, tanı yaşı strata) | ⊝ ileri faz / **DM-only** |
| XI | Robustluk (multiverse specr, TOST, sensemakr RV, E-value, negative control, falsification) | ⊝ **standart gereksinim** — H1-H4 için zorunlu |
| XII | Bayesci paralel hat (brms, BF, WAIC/LOO, model stacking, blavaan) | ⊝ kısmen aktif (H1 preflight) — **dual reporting standardı** |
| XIII | Karma yöntem (RTA Braun-Clarke 2022, joint display, convergence, Gwet AC1) | ⊝ keşifsel |
| XIV | Raporlama ve diseminasyon (papaja, apaquarto, 22 şekil, 3-makale plan, FAIR/Zenodo/OSF) | ⊝ paralel aktif |
| XV | Devstats yedi tedbir denetimi (confounding, multiple comparison, Simpson, survivorship, ekoloji, garden of forking, false precision) | ✓ aktif (`tedbir-ve-hatalar.md`) |
| XVI | Risk yönetimi (15 risk × yedek strateji matrisi) | ⊝ tetiklendiğinde |
| XVII | 24-haftalık çalıştırma çizelgesi | — referans plan |
| XVIII | Tam referans listesi (Brown, Hox, Enders, Hayes, Pearl, Lakens, Pinquart, Braun-Clarke vb.) | — bibliyografi kaynak |

**Kural:** KISIM VI–X, XIII'ten bir çalışma istenirse `[KEŞİFSEL]` etiketle. KISIM XI sensitivity
(multiverse + TOST + sensemakr) ve KISIM XII Bayesian paralel hat **H1-H4 birincil bulgular için
standart gereksinim**dir, atlanmaz. KISIM XV (devstats yedi tedbir) **her primer çıkarımdan önce**
aktif denetim. KISIM XIV diseminasyon ve KISIM XVII zaman çizelgesi **referans planlama**
katmanıdır.

---

## Reference Dosyaları — İçindekiler

### Çekirdek (KISIM I-IV temel)

| Dosya | İçerik |
|-------|--------|
| `references/pipeline-mimarisi.md` | `_targets.R`, `R/00_paths.R` … `R/19_h4_*.R` modül haritası, kanonik kilit doğrulama, KISIM II–V hedefleri, runbook'lar |
| `references/psikometri-pipeline.md` | EMBU-P/C 4-faktör CFA, BDI tek-faktör/iki-faktör, KİA 4-faktör, ω vs. α, ölçüm değişmezliği (configural→metric→scalar→strict), graded response IRT |
| `references/multilevel-aile-yapisi.md` | 241 aile × 2 dyadic veri, ICC hesabı, Hox sample size, group-mean centering, APIM, three-level mother–dyad |
| `references/eksik-veri-yonetimi.md` | mice (m=50, maxit=30), FIML lavaan, structural missing (DM-only HbA1c/dm_yili), naniar viz, NMAR delta grid |
| `references/nedensellik-ve-ps.md` | dagitty Causal DAG, backdoor minimal adjustment set, IPTW (logit + 99. persentil trim), 1:1 nearest-neighbor matching, doubly-robust, sensemakr |
| `references/ileri-yontemler.md` | lavaan WLSMV ordinal SEM, multigroup invariance, growth/CLPM/RI-CLPM, Hayes-style mediation (lavaan + bootstrap), brms Bayesian, blavaan preflight |
| `references/etki-buyuklugu-ve-guc.md` | Cohen's d/Hedges g, ω², gelişimsel benchmark (Pinquart 2013, Schäfer 2019), simr multilevel power, pwrss mediation power, Bayesian prior derivation |
| `references/tedbir-ve-hatalar.md` | Yedi tedbir prensibi + projeye özel 12 tehlike (kanonik kilit kırılması, EMBU madde drift, ölçek karışımı, false precision in BDI, sahte SEM fit) |

### Hipotez genişletmesi (KISIM V — H5)

| Dosya | İçerik |
|-------|--------|
| `references/h5-diadik-tutarlilik.md` | H5 5-strateji: ICC(2,1) + Bland-Altman, RSA Edwards-Parry (4 parametre a1-a4), Common Fate Model, Olsen-Kenny dyadic CFA (true concordance), k-coefficient (Kenny). Diadik tutarsızlık klinik yorumu, Streisand & Monaghan beklenen örüntü |

### Genişletilmiş analiz katmanları (KISIM VI-XIII)

| Dosya | İçerik |
|-------|--------|
| `references/mediation-modelleri.md` | KISIM VI: VanderWeele 4 etki, basit mediation (lavaan + BCa bootstrap), 1-1-1 multilevel mediation, Hayes Model 4/7/14 conditional process, Bayesian mediation + ROPE, sensitivity (sensemakr ile mediator-outcome confounder) |
| `references/latent-degisken-yontemleri.md` | KISIM VII: tidyLPA 1-6 profil, Akogul-Erisoglu seçim kriterleri (BIC + entropy + LMR-LRT + BLRT), beklenen 4 profil (Adapte/Aşırı Koruyucu/Tükenmiş/Standart), poLCA kategorik, flexmix mixture regression, Eid 2017 Bifactor S-1 (ω_h, ECV, PUC) |
| `references/network-analizi.md` | KISIM VIII: GGM EBIC-LASSO (gamma=0.5, Spearman), centrality (strength/closeness/betweenness/expected influence), CS-coefficient bootstrap stability, NCT (network/global strength/edge invariance), Beck 21-madde symptom network |
| `references/klinik-fayda.md` | KISIM IX: high-risk anne (Beck≥17) lojistik risk skoru, ROC + Youden's J + AUC eşikleri, Vickers-Elkin DCA net benefit, CART 1-SE pruning, Random Forest %IncMSE, Harrell calibration, Pencina NRI/IDI + cfNRI |
| `references/dm-klinik-altanalizler.md` | KISIM X DM-only: HbA1c × ebeveynlik (n=39 keşifsel, ISPAD eşik), DM süresi cubic spline (knots quartile, LRT), tanı yaşı 3-strata (<5, 5-10, ≥10), gelişim penceresi yorumu |
| `references/robustluk-ve-sensitivite.md` | KISIM XI: specr multiverse (1800 spec EMBU-P Reddetme), Simonsohn inferential test, Lakens TOST + ROPE üçlü karar matrisi (Trivial/EQ/Meaningful/IND), sensemakr RV + E-value, Lipsitch negative control, Hernán-Robins falsification |
| `references/bayesci-paralel-hat.md` | KISIM XII: brms multilevel + Pinquart prior (zayıf bilgi verici 3× geniş), R̂/ESS/divergent kontrolü, PPC, ROPE + pd, Savage-Dickey BF (Jeffreys), WAIC + LOO + Pareto-k, Yao stacking, blavaan SEM + Frequentist+Bayesian dual reporting |
| `references/karma-yontem.md` | KISIM XIII: Braun-Clarke 2022 RTA 6-faz, Gwet AC1 inter-coder güvenirlik, tema-frekans + ggalluvial, Creswell convergent parallel design, joint display tablosu (8 satır), discrepant bulgu yorumu (sosyal istenirlik kompansasyonu). **Niteliksel kolun uçtan uca derinleşmesi (RTA 6-faz tek tek, dyadik görüşme protokolü, COREQ/JARS-Qual, KVKK + child assent, refleksif günlük, jüri savunma) için ayrı `niteliksel-arastirma-rehberi-t1dm` skill'ine devir; karma yöntem entegrasyonu (joint display, GRAMMS, MMAT) bu skill'de kalır.** |

### Diseminasyon ve sunum (KISIM XIV-XVII)

| Dosya | İçerik |
|-------|--------|
| `references/tez-yazim-rehberi.md` | Quarto YAML (`lang: tr`, `freeze: auto`), papaja MD7, JARS-Mixed + STROBE, Türkçe terim sözlüğü, kaynakça (`references.bib` + `apa.csl`) |
| `references/diseminasyon-ve-yayin.md` | KISIM XIV: papaja/apaquarto tablo, 22-şekil katalog (CONSORT-Mixed → Bayesian forest), Quarto triple-format (PDF/DOCX/HTML), `report::report()` + Türkçe APA, 18-bölüm thesis mapping, 3-makale plan, FAIR/Zenodo/OSF |
| `references/raporlama-sablonlari.md` | Türkçe APA 7 results paragrafı şablonları (t-test, ANOVA, regresyon, multilevel, CFA, SEM, mediation, APIM, IPTW), Tablo 1 (gtsummary), Tablo 2 (regresyon), forest plot |
| `references/risk-ve-zaman-cizelgesi.md` | KISIM XVI/XVII: 15-risk × yedek strateji matrisi (öncelikli: 3, 6, 9), 24-haftalık sprint plan (durum: ✅ Hafta 1-10 tamamlandı, ⏳ 11+ gelecek faz), risk-tetiklendiğinde akışı, weekly sprint kontrol listesi |

### Yardımcı

| Dosya | İçerik |
|-------|--------|
| `references/kaynak-kitaplar-haritasi.md` | 14 kitap → bölüm → projedeki uygulama haritası (Brown CFA → H4 ölçüm modeli; Kline → SEM raporlama; Enders → MI; McElreath → brms preflight; Hayes → mediation; DeVellis → ω; Hox → ICC; Field → keşif; vs.) |
| `references/ornek-senaryolar.md` | 12 yaygın sorgu için uçtan uca akış (test seçimi → cached target → yorumlama → raporlama paragrafı), hızlı karar tablosu, "yapma sinyalleri", sık komutlar |

## Davranış Kuralları (Çiğnemediğin)

1. **Asla** kanonik CSV'yi doğrudan değiştirme. Tüm türetilmiş skorlar `R/10_derived_scores.R`
   üzerinden yürütülür.
2. **Asla** ham veri (`data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/`) commit'le.
   PII koruma `.gitignore`'da kayıtlı.
3. **Asla** "p < .05 → anlamlı, başka şey gerekmez" demez. Etki büyüklüğü + GA + pratik anlam
   birlikte raporlanır.
4. **Asla** EMBU-P/C için 6'lı Likert varsay; kanonik form 4'lü Likert standardındadır.
5. **Asla** alt ölçek toplamını yarısından fazla madde eksikken hesapla. Beck toplamında **tek
   eksik item bile** toplamı NA bırakır.
6. **Asla** "Bu sonuç keşifsel olarak çıktı, ön-kayıtta vardı" deme. Sapma `[KEŞİFSEL]`
   etiketiyle açıkça belirtilir.
7. **Asla** Türkçe terim ihmal et. "Effect size" değil "etki büyüklüğü"; "confidence interval"
   değil "güven aralığı". İngilizce sadece parantezde.
8. **Asla** kitap referansı uydur. `references.bib` veya `references/kaynak-kitaplar-haritasi.md`
   doğrula.
9. **Asla** sensitivity / multiverse / TOST'u "ileri seviye" diye atla. H1–H4 bulguları için
   bu üçlü standart gereksinimdir.
10. **Asla** `_targets/meta` veya `renv.lock` hash'lerini "küçük değişiklik" diye değiştir.
    Bunlar reproducibility çapasıdır; her değişiklik commit mesajında gerekçelenir.
11. **Asla** H5 diadik tutarlılık için tek strateji rapor et. **5 strateji paralel** zorunlu —
    en az 3'ü uyumlu olmadan "güçlü bulgu" ilan edilmez. Discrepant strateji sonuçları
    tartışmada açıkça raporlanır.
12. **Asla** H1-H4 birincil bulguları için **multiverse + TOST + sensemakr** üçlüsünü atla.
    Bu üçlü standart gereksinimdir; yokluğu "ileri seviye" değil "eksik analiz"dir.
13. **Asla** brms Bayesian analizinde `sample_prior = "yes"` parametresini atla. Savage-Dickey
    BF için zorunlu; aksi halde BF hesaplaması imkânsız. Pinquart-temelli prior derivation
    kod yorumunda gerekçelendirilir.
14. **Asla** Multiverse analizinden "anlamlı çıkanları" cherry-pick yapma. Tüm spec dağılımı
    + Simonsohn inferential test (permütasyon n_perm = 5000) raporlanır.
15. **Asla** GGM/network analizini "X → Y nedensel" diye yorumla. Koşullu bağımlılık ≠
    nedensellik. DAG tartışması yalnızca [`nedensellik-ve-ps.md`](references/nedensellik-ve-ps.md).
16. **Asla** LPA profil etiketini ("Tükenmiş", "Adapte") klinik tanı veya tedavi önerisi olarak
    sun. Etiketler **betimsel** ve içerik tabanlıdır; klinik karar için validation gerekir.
17. **Asla** RTA niteliksel analizinde "saturation" kavramını kullan — Braun & Clarke (2021)
    refleksif TA için açıkça reddetmiştir. Tema yeterliliği yansıtıcı not + iki kodlayıcı
    güvenirliği (Gwet AC1) ile gerekçelendirilir.
18. **Asla** risk skoru (KISIM IX) için bootstrap/CV yapmadan AUC raporla. Optimistic bias
    karşı içsel validasyon (.632+ veya 10-fold) zorunlu. Dış validasyon yoksa "keşifsel"
    etiketi vurgulanır.
19. **Asla** HbA1c (n=39, %32.5) için imputation yap. Klinik biyobelirteç tahmin edilemez;
    DM-only sensitivite analizi olarak yürütülür ve **n_hba1c** açıkça raporlanır.

## Hızlı Komutlar

```bash
# Tezi render et
quarto render thesis.qmd

# Pipeline (KISIM II–V)
Rscript -e 'targets::tar_make()'

# Spesifik hedef
Rscript -e 'targets::tar_make(h2_apim_fixed_effects_table)'

# Kanonik kilit doğrulama
Rscript -e 'targets::tar_load(final_reference_manifest); print(final_reference_manifest)'

# Renv durumu
Rscript -e 'renv::status()'

# Raporlama standartları denetimi
Rscript scripts/R/09_reporting_standards_audit.R

# Etik / veri yönetimi denetimi
Rscript scripts/R/08_ethics_data_governance_audit.R
```

## Diller ve Terim Sözlüğü Hızlı Referans

| Türkçe | İngilizce |
|--------|-----------|
| Etki büyüklüğü | Effect size |
| Güven aralığı | Confidence interval |
| Çoklu atama | Multiple imputation |
| Eğilim skoru | Propensity score |
| Aracılık | Mediation |
| Düzenleyicilik | Moderation |
| Çok düzeyli model | Multilevel model |
| Yapısal eşitlik modellemesi | Structural equation modeling |
| Sınıf-içi korelasyon | Intraclass correlation (ICC) |
| Aktör-partner bağımlılık modeli | Actor-Partner Interdependence Model (APIM) |
| Ölçüm değişmezliği | Measurement invariance |
| Gizil profil analizi | Latent profile analysis |
| Eşdeğerlik testi | Equivalence testing (TOST) |
| Çoklu evren analizi | Multiverse / specification curve |
| Duyarlılık analizi | Sensitivity analysis |
| Doğrulayıcı faktör analizi | Confirmatory factor analysis |
| Madde tepki kuramı | Item response theory (IRT) |
| Yapısal eksiklik | Structural missingness |
| Diadik tutarlılık | Dyadic concordance |
| Yüzey tepki analizi | Response surface analysis (RSA) |
| Ortak yazgı modeli | Common Fate Model (CFM) |
| Refleksif tematik analiz | Reflexive thematic analysis (RTA) |
| Yakınsama analizi (karma yöntem) | Convergence analysis (mixed methods) |
| Karar eğrisi analizi | Decision curve analysis (DCA) |
| Net yeniden sınıflama iyileşmesi | Net reclassification improvement (NRI) |
| Olasılık yönü | Probability of direction (pd) |
| Pratik eşdeğerlik bölgesi | Region of practical equivalence (ROPE) |
| Bayes faktörü | Bayes factor (BF) |
| Posterior öngörülü kontrol | Posterior predictive check (PPC) |
| Negatif kontrol | Negative control |
| Yanlışlama testi | Falsification test |
| Etki büyüklüğü en küçük ilgi alanı | Smallest effect size of interest (SESOI) |
| Sağlamlık değeri | Robustness Value (RV_q) |
| E-değeri | E-value |
| Diadik bağlam | Dyadic context |
| Açıklayıcı ortak varyans | Explained common variance (ECV) |

---

**Tek cümlelik özet:** Bu skill, T1DM tezi için her R kodu, her psikometrik karar, her hipotez
testi, her tez paragrafı ve her açık bilim adımının **kanıt-temelli, projeye-uygun, tek-tutarlı**
versiyonunu üretir. Reference dosyalarını oku, sonra cevap ver.
