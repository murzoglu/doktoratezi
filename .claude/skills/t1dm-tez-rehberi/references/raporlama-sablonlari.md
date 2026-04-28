# Türkçe APA 7 Raporlama Şablonları

**Ne zaman oku:** Bulgular bölümünde paragraf yazılırken, gtsummary tablosu hazırlanırken,
forest plot çizilirken, tek bir test sonucunu metne çevirirken.

Her şablon **Türkçe ana metin + İngilizce parantez** standardındadır.

---

## 1. Tanımlayıcı İstatistik

> "DM grubundaki çocukların yaş ortalaması M = 11.34 (SD = 2.78, Mdn = 11.5, ÇA [9.0,
> 13.5]) iken kontrol grubunda M = 11.18 (SD = 2.65) olmuştur. İki grup arasında yaş
> bakımından anlamlı fark bulunmamıştır (t(478.2) = 0.62, p = .538, d = 0.06 [-0.13,
> 0.24])."

---

## 2. Bağımsız t-Test

> "Anne yaşı ortalaması DM grubunda M = 38.45 (SD = 5.21) ve kontrol grubunda M = 37.82
> (SD = 4.98) olarak bulunmuştur. Welch düzeltmeli iki örneklemli t testi (Welch
> two-sample t-test) anlamlı bir fark göstermemiştir (t(238.4) = 1.02, p = .311, d = 0.13
> [-0.12, 0.38]). TOST eşdeğerlik testi ±0.20 SD bound'unda istatistiksel eşdeğerliği
> teyit etmiştir (t = -0.81, p = .209; t = 2.83, p = .003)."

---

## 3. Eşleştirilmiş t-Test

> "İndeks çocuklarda EMBU-C Sıcaklık ortalaması (M = 2.95, SD = 0.62), kardeşlerinin
> ortalamasından (M = 3.12, SD = 0.58) anlamlı düzeyde düşük bulunmuştur (t(240) = -3.45,
> p = .001, d_z = -0.22 [-0.35, -0.09])."

---

## 4. Tek Yönlü ANOVA

> "EMBU-C Sıcaklık alt ölçeği ortalamaları rol gruplarına (DM-indeks, DM-kardeş,
> kontrol-indeks, kontrol-kardeş) göre tek yönlü varyans analizi (one-way ANOVA) ile
> karşılaştırılmıştır. Roller arasında anlamlı fark saptanmıştır (F(3, 478) = 4.82,
> p = .003, ω² = .024). Holm düzeltmeli ardıl karşılaştırmalar DM-indeks grubunun
> kontrol-indeks grubundan anlamlı düzeyde düşük olduğunu göstermiştir (Δ = −0.21,
> SE = 0.07, p_adj = .008, d = −0.34)."

---

## 5. Korelasyon

> "EMBU-P Reddetme alt ölçeği ile Beck Depresyon toplam puanı arasında orta düzeyde
> pozitif korelasyon bulunmuştur (r(239) = .34, p < .001, 95% GA [.22, .45]). Bu büyüklük,
> Pinquart'ın (2013) meta-analizinde rapor edilen tipik parenting–maternal mental health
> ilişkisi büyüklüğüyle (r ≈ 0.30) tutarlıdır."

---

## 6. Çoklu Regresyon

> "EMBU-P Sıcaklık alt ölçeğini yordamak üzere hiyerarşik regresyon yürütülmüştür.
> Birinci adımda demografi (anne yaşı, çocuk sayısı, kardeş yaş farkı, SES) modelin %12'sini
> açıklamıştır (R² = .12, F(4, 236) = 8.04, p < .001). İkinci adımda DM grup değişkeni
> ve Beck Depresyon eklenince ek %8 açıklama elde edilmiştir (ΔR² = .08, F-change(2, 234)
> = 11.64, p < .001, f² = 0.10). Tam modelde Beck Depresyon Sıcaklık'ı negatif yönde
> anlamlı yordamıştır (β = -.27, SE = .07, p < .001, β_std = -.31 [-.45, -.17]; sr² = .06)."

---

## 7. Multilevel Model (lme4 + lmerTest)

> "EMBU-C Sıcaklık alt ölçek ortalamasının aile-içi sınıf-içi korelasyonu ICC = .19
> (95% GA [.10, .29]) hesaplanmış ve Hox (2018) eşiği olan .05'in üzerinde olduğundan
> rastgele aile-kesişim modeli (random intercept model) gerekli görülmüştür. Birincil
> model `embu_c_sicaklik_mean ~ role_f + cocuk_yas_z + cinsiyet_f + ses_latent_z + age_gap_z +
> cocuk_sayisi_z + (1 | aile_no_f)` REML tahmin edicisi ve Kenward-Roger serbestlik
> derecesi ile uygulanmıştır. DM-indeks rolü kontrol-indeksten Δ = -0.18 (SE = 0.07,
> t(232.4) = -2.55, p = .011, β_std = -0.21 [-0.37, -0.05]) düzeyinde anlamlı düşük
> bulunmuştur. Aile düzeyi varyans bileşeni τ² = 0.058 (SE = 0.014); rezidüel σ² = 0.247.
> Modelin koşullu R² = .247, marjinal R² = .078 olmuştur."

---

## 8. APIM (lavaan)

> "Kardeş çatışmasının sıcaklığa aktör ve partner etkileri APIM çerçevesinde lavaan ile
> tahmin edilmiştir (Kenny ve diğerleri, 2006). DM-indeks aktör etkisi a_index = -0.42
> (SE = 0.09, p < .001, β_std = -0.39 [-0.55, -0.23]); kardeş aktör etkisi a_sib = -0.38
> (SE = 0.10, p < .001, β_std = -0.36 [-0.52, -0.20]) olmuştur. Partner etkileri DM-indeks
> için p_index = -0.18 (SE = 0.08, p = .021, β_std = -0.17 [-0.30, -0.04]); kardeş için
> p_sib = -0.21 (SE = 0.08, p = .010, β_std = -0.19 [-0.32, -0.06]) bulunmuştur. Aktör ve
> partner etkilerinin distinguishability testi anlamlı fark göstermemiştir (actor_diff =
> -0.04, p = .812; partner_diff = 0.03, p = .824), bu nedenle exchangeable APIM
> spesifikasyonu da raporlanmıştır."

---

## 9. Olsen-Kenny Distinguishable Dyad CFA

> "Quarrel item seti üzerinde indeks–kardeş latent korelasyonu Olsen-Kenny distinguishable
> dyad CFA çerçevesinde (Olsen & Kenny, 2006) tahmin edilmiştir. Modelin uyumu iyi
> düzeydedir (χ²(8) = 12.4, p = .135, CFI = .982, TLI = .967, RMSEA = .039 [%95 GA: .000–
> .076], SRMR = .031). Latent korelasyon r_latent = .34 (SE = .08, p < .001), gözlenen
> korelasyon r_obs = .22'den belirgin olarak yüksek bulunmuş ve ölçüm hatasının ham
> korelasyonu zayıflattığı doğrulanmıştır. Yük eşitliği (λ_index = λ_sib) kabul edilebilir
> uyum dağılımı sağlamıştır (Δχ²(3) = 4.18, p = .243), bu nedenle indeks ve kardeş yapı
> psikometrik olarak ayırt edilemez (indistinguishable) sonucu raporlanmıştır."

---

## 10. CFA + ω

> "EMBU-C Sıcaklık alt ölçeği için tek faktörlü WLSMV CFA modeli iyi uyum göstermiştir
> (χ²(35) = 48.2, p = .071, CFI = .978, TLI = .965, RMSEA = .045 [%95 GA: .000–.072],
> SRMR = .038). Standardize yükler .52 ile .81 arasında (Mdn = .68) yer almıştır.
> McDonald ω = .87 (95% GA [.84, .90]) güvenilirlik düzeyini desteklemiş; Cronbach α = .85
> ek kanıt sağlamıştır."

---

## 11. Ölçüm Değişmezliği

> "DM ve kontrol grupları arasında EMBU-C Sıcaklık alt ölçeğinin ölçüm değişmezliği
> dört aşamalı multigroup CFA hiyerarşisi (configural → metric → scalar → strict) ile
> test edilmiştir. Configural değişmezlik kabul edilmiş (CFI = .976, RMSEA = .047), metric
> değişmezlik korunmuştur (ΔCFI = .003, ΔRMSEA = .002 — eşik altı). Scalar düzeyde
> ΔCFI = .013 (eşik > .010) saptanmış ve q14 ve q22 maddelerinin intercept'leri serbest
> bırakılmıştır; bu kısmi-scalar (partial scalar) çözümle iyileşme elde edilmiş (ΔCFI =
> .007). Bu nedenle alt ölçek ortalama karşılaştırmaları kısmi-scalar düzeyde yorumlanmıştır
> (Cheung & Rensvold, 2002)."

---

## 12. SEM (Yapısal Yollar)

> "H4 yapısal eşitlik modeli `lavaan` paketinde WLSMV tahmin edicisi ile uygulanmıştır
> (Rosseel, 2012). Modelin uyumu kabul edilebilir düzeyde olmuştur (χ²(1175, N = 241) =
> 1542.3, p < .001, χ²/df = 1.31, CFI = .914, TLI = .906, RMSEA = .043 [%95 GA: .038–
> .048], SRMR = .067). Anne yaşı ve SES için ayarlandığında, Beck depresyon latent
> faktörü Reddetme alt ölçeğini β_std = .29 (SE = .07, p < .001), Sıcaklık alt ölçeğini
> ise β_std = -.18 (SE = .08, p = .024) düzeyinde anlamlı yordamıştır. Aşırı Koruma
> (β_std = .12, p = .142) ve Karşılaştırma (β_std = .09, p = .231) üzerindeki etkiler
> anlamlı bulunmamıştır."

---

## 13. Aracılık (Mediation)

> "Beck depresyon → EMBU-P Sıcaklık → EMBU-C Sıcaklık aracılık modeli `lavaan` ile bias-
> corrected bootstrap (5,000 yineleme) güven aralıkları ile test edilmiştir (Hayes, 2022).
> a-yolu (Beck → EMBU-P) â = -0.31 (95% GA [-0.46, -0.16], p < .001); b-yolu (EMBU-P →
> EMBU-C) b̂ = 0.42 (95% GA [0.28, 0.56], p < .001); doğrudan etki c'̂ = -0.08 (95% GA
> [-0.21, 0.05], p = .228); dolaylı etki ab̂ = -0.13 (95% GA [-0.21, -0.06], p = .002);
> toplam etki ĉ = -0.21 (95% GA [-0.34, -0.08], p = .002) olmuştur. Aracılık oranı
> ab/c = .619, yani toplam etkinin yaklaşık %62'si aracılık tarafından açıklanmaktadır."

---

## 14. IPTW + ANCOVA

> "Eğilim skoru ters olasılık ağırlıklandırması (IPTW; Robins ve diğerleri, 2000) `WeightIt`
> paketi ile logit PS modeli (group_dm ~ ses_latent + age_gap + cocuk_sayisi + maternal_age
> + cinsiyet) üzerinde tahmin edilmiş; stabilized ağırlıklar 99. persentilde trimlenmiştir.
> Ağırlıklandırma sonrası tüm kovaryatlarda standardized mean difference (SMD) eşiği
> < .10 sağlanmıştır (önceki SMD ortalaması .23, sonra .04). Etkin örneklem büyüklüğü
> ESS = 198 olmuştur. Ağırlıklı ANCOVA modelinde DM grup etkisi β = -0.19 (HC3 SE = 0.08,
> p = .022, β_std = -0.22 [-0.40, -0.04]); ham ANCOVA tahminiyle (β_std = -0.21) yakın
> tutarlık göstermiştir."

---

## 15. Sensemakr Robustness Value

> "DM grup etkisinin ölçülmemiş karıştırıcılara duyarlılığı sensemakr çerçevesi (Cinelli &
> Hazlett, 2020) ile değerlendirilmiştir. Tahmini sıfıra çekmek için ölçülmeyen bir
> karıştırıcının hem grup atamasını hem de EMBU-P Reddetme alt ölçeğini SES'in ötesinde
> %18.4'ün üzerinde açıklaması gerekirdi (Robustness Value = .184). 1×, 2× ve 3× SES
> gücüne sahip karıştırıcı senaryolarında tahmin yönü değişmemiş; üç katlı SES gücünde
> %95 GA üst sınırı sıfırı geçmemiştir. Bu, bulgunun ortalama düzey ölçülmemiş
> karıştırıcılara dayanıklı olduğunu göstermektedir."

---

## 16. Multiverse / Specification Curve

> "DM grup etkisinin analitik spesifikasyon seçimlerine duyarlılığı `specr` paketi ile
> 36 makul kombinasyonda (3 outcome × 4 kovaryat seti × 3 sample subset) test edilmiştir
> (Simonsohn ve diğerleri, 2020). Spesifikasyonların %92'sinde (33/36) etki yönü negatif
> (DM < kontrol) ve istatistiksel olarak anlamlı (p < .05) bulunmuş; medyan etki büyüklüğü
> β_std = -.20 (IQR [-0.27, -0.13]) olmuştur. Üç ihlal eden spesifikasyon kontrol grubunda
> kardeş alt-örnekleminde anlamlılığı kaybetmiş; bu, mevcut güç düşüklüğüne atfedilebilir
> (n_kardeş = 121)."

---

## 17. Bayesian Posterior

> "Pinquart'ın (2013) meta-analizinden türetilen informative prior (β ~ Normal(-0.20, 0.10))
> altında uygulanan brms multilevel model (4 zincir × 4000 yineleme; R̂ ≤ 1.01, n_eff ≥
> 1200) DM grup etkisi için posterior medyan β = -0.21, 95% credible interval [-0.36,
> -0.06] vermiştir. Posterior'un tamamı negatif olduğundan etki yönü %100 olasılıkla
> negatiftir (Probability of Direction = 1.00). Bayesian eşdeğerlik testi (ROPE
> [-0.10, 0.10]) credible interval'ın yalnız %4.2'sinin ROPE içinde olduğunu göstermiş;
> bu pratik anlamlı bir farkı destekler."

---

## 18. Tablo 1 (Demografik) — gtsummary

```r
library(gtsummary); library(targets)

tar_load(df_family_ses)

t1 <- df_family_ses |>
  select(group_dm, anne_yas, ses_latent, age_gap, cocuk_sayisi,
         beck_total, antidepressant) |>
  tbl_summary(
    by = group_dm,
    statistic = list(
      all_continuous() ~ "{mean} ({sd})",
      all_categorical() ~ "{n} ({p}%)"
    ),
    digits = list(
      all_continuous() ~ 2,
      all_categorical() ~ 0
    ),
    label = list(
      anne_yas        ~ "Anne Yaşı (yıl)",
      ses_latent      ~ "SES Latent Skor (z)",
      age_gap         ~ "Kardeş Yaş Farkı (yıl)",
      cocuk_sayisi    ~ "Aile Çocuk Sayısı",
      beck_total      ~ "Beck Depresyon Toplam",
      antidepressant  ~ "Antidepresan Kullanan"
    ),
    missing = "ifany",
    missing_text = "Eksik"
  ) |>
  add_overall(col_label = "**Toplam (N = 241)**") |>
  add_difference(test = list(all_continuous() ~ "smd",
                              all_categorical() ~ "smd")) |>
  modify_caption("**Tablo 1.** Tip 1 Diyabet ve Kontrol Aileleri Demografik
                  ve Klinik Özellikleri (N = 241)") |>
  bold_labels()

t1
```

---

## 19. Forest Plot (Çoklu Etki Büyüklüğü)

```r
library(ggplot2)

forest_data <- tibble::tribble(
  ~outcome,                ~est,    ~lower,   ~upper,
  "EMBU-P Sıcaklık",       -0.18,   -0.34,    -0.02,
  "EMBU-P Aşırı Koruma",    0.12,   -0.04,     0.28,
  "EMBU-P Reddetme",        0.29,    0.13,     0.45,
  "EMBU-P Karşılaştırma",   0.09,   -0.07,     0.25
)

ggplot(forest_data, aes(x = est, y = outcome,
                        xmin = lower, xmax = upper)) +
  geom_pointrange(size = 0.6) +
  geom_vline(xintercept = 0, linetype = "dashed", colour = "gray50") +
  geom_vline(xintercept = c(-0.20, 0.20), linetype = "dotted",
             colour = "gray70") +
  scale_x_continuous(limits = c(-0.5, 0.6),
                     breaks = seq(-0.4, 0.6, by = 0.2)) +
  labs(
    x = expression(beta[std]~"(95% GA)"),
    y = NULL,
    title = "DM Grup Etkisi — EMBU-P Alt Ölçekleri",
    subtitle = "ROPE: [-0.20, 0.20] gri kesik çizgi"
  ) +
  theme_minimal(base_family = "Times New Roman") +
  theme(panel.grid.major.y = element_blank())
```

---

## 20. Eksik Veri Tablosu

> "Toplam 241 ailede gözlemlenen analiz değişkenleri için eksiklik düzeyleri Tablo X'te
> sunulmuştur. Anne öz-rapor değişkenlerinde eksiklik %1.2 ile %3.7 arasında (Beck
> Depresyon: %2.5; EMBU-P alt ölçekleri ortalama %1.8) bulunmuş, klinik DM değişkenleri
> tasarım kaynaklı yapısal eksiklik (kontrol grubunda HbA1c ve dm_yili %100) sergilemiştir.
> Little MCAR testi DM-spesifik değişkenler hariç tutulduğunda anlamlılık göstermemiş
> (χ²(48) = 56.3, p = .195), MAR varsayımı altında çoklu atama uygulanması desteklenmiştir."

---

## 21. Sınırlama Paragrafı (Tartışma Sonu)

> "Bu çalışmanın bulguları yorumlanırken üç temel sınırlama göz önünde bulundurulmalıdır.
> İlk olarak, kesitsel desen Beck depresyonu ile EMBU-P alt ölçekleri arasındaki ilişkinin
> zamansal yönünü tespit etmeye olanak vermez; bidireksiyonel ilişkiyi ayrıştırabilen RI-CLPM
> (Hamaker ve diğerleri, 2015) en az üç ölçüm noktası gerektirir. İkinci olarak, DM
> grubuna katılan aileler aktif klinik takipte olan ve anket tamamlamayı kabul eden
> ailelerdir; daha ağır metabolik kontrolsüzlük yaşayan veya tedaviyi terk etmiş aileler
> örnekleme dahil edilmemiş olabilir (survivorship bias). Üçüncü olarak, sensemakr
> Robustness Value %18 ile orta düzey ölçülmemiş karıştırıcılara dayanıklılık göstermiş
> olsa da bu, baba ebeveynlik tutumu, aile içi iletişim örüntüleri ve geniş aile destek
> ağı gibi bu çalışmada toplanmamış değişkenleri kapsamamaktadır. Gelecek araştırmalarda
> baba katılımı sağlanmalı, aile sistemleri perspektifi ile dyadic ve triadic ölçümler
> birlikte yürütülmelidir."

---

## Hızlı Bakış: Test → Şablon Eşleme

| Test/Analiz | Şablon | Kaynak |
|-------------|--------|--------|
| Bağımsız t | §2 | — |
| Eşleştirilmiş t | §3 | — |
| Welch t / TOST | §2 | Lakens 2017 |
| Tek yönlü ANOVA | §4 | — |
| Korelasyon | §5 | — |
| Hiyerarşik regresyon | §6 | Field 2012 |
| Multilevel (lme4) | §7 | Hox 2018 |
| APIM | §8 | Kenny 2006 |
| Olsen-Kenny CFA | §9 | Olsen & Kenny 2006 |
| CFA + ω | §10 | Brown 2015 + DeVellis 2022 |
| Ölçüm değişmezliği | §11 | Cheung & Rensvold 2002 |
| SEM | §12 | Kline 2023 |
| Aracılık (lavaan) | §13 | Hayes 2022 |
| IPTW + ANCOVA | §14 | Robins ve diğerleri 2000 |
| Sensemakr | §15 | Cinelli & Hazlett 2020 |
| Multiverse | §16 | Simonsohn ve diğerleri 2020 |
| Bayesian (brms) | §17 | Bürkner 2017 + Gelman ve diğerleri 2021 |
| Tablo 1 | §18 | gtsummary |
| Forest plot | §19 | ggplot2 |
| Eksik veri raporu | §20 | Enders 2022 |
| Sınırlama paragrafı | §21 | Bu projenin geneli |
| H5 diadik tutarlılık (5-strateji) | §22 | bu doküman |
| Mediation (BCa bootstrap) | §23 | Hayes 2018; VanderWeele 2015 |
| LPA — anne tipoloji | §24 | Lanza & Cooper 2016 |
| GGM + NCT | §25 | Epskamp ve diğerleri 2018 |
| Risk skoru + DCA + Calibration | §26 | Vickers & Elkin 2006; Harrell 2015 |
| Multiverse + TOST + Sensemakr (üçlü robustluk) | §27 | bu doküman §H1-H4 zorunlu |
| Bayesian dual reporting (Frequentist + Bayesian) | §28 | bu doküman |
| Joint display (karma yöntem) | §29 | Creswell & Plano Clark 2018 |

---

## §22. H5 Diadik Tutarlılık Şablonu

> "Anne (EMBU-P) ve indeks-çocuk (EMBU-C) Reddetme alt ölçeği algıları arasındaki uyum, beş paralel
> stratejiyle değerlendirilmiştir. (1) İki-yönlü mutlak uyum sınıf-içi korelasyon DM grubunda
> ICC(2,1) = .19 (95% GA [.06, .32]); Kontrol grubunda ICC(2,1) = .31 (95% GA [.18, .43]) olarak
> hesaplanmış; her iki değer de Koo ve Li (2016) düşük uyum eşiğinde kalmıştır. (2) Bland-Altman
> sınırlarında (LoA) DM grubunda ortalama fark = -0.42, %95 LoA = [-1.85, +1.01]; sistematik bias
> bulunmamış ancak bireysel ailelerde dispersiyon yüksektir. (3) Olsen-Kenny diadik CFA'da
> (estimator = WLSMV) ölçüm hatasından arındırılmış latent korelasyon DM = .24, Kontrol = .38
> olarak elde edilmiştir; method effect (aynı maddenin korele rezidüleri) modele dahildir;
> CFI.scaled = .96, RMSEA.scaled = .05, SRMR = .07. (4) Edwards ve Parry (1993) yüzey tepki
> analizinde tutarsızlık derecesi (a4) DM grubunda Beck total ile pozitif ilişkilidir, a4 = 0.42,
> %95 GA [0.10, 0.74]; Kontrol grubunda anlamsız (a4 = 0.08, %95 GA [-0.18, 0.34]). (5) Aile-içi
> rastgele etki APIM'inde k-coefficient = 0.32 (BCa %95 GA [0.08, 0.56]) — actor-only modele
> yakın ancak partner etkisi de mevcuttur. Beş stratejinin ortak gösterdiği örüntü, T1DM
> ailelerinde anne–çocuk algı uyuşmazlığının anne ruh sağlığı yüküyle bağlantılı olabileceğine
> işaret etmektedir."

## §23. Mediation Şablonu (Tek-Mediator + BCa Bootstrap)

> "Anne depresyon belirtilerinin (Beck total) çocuk algılanan ebeveynlik reddetmesine etkisinin
> anne öz-rapor reddetme tutumu üzerinden geçen indirek yolu lavaan paketi ile (estimator = MLR,
> missing = FIML) test edilmiştir. Bootstrap güven aralıkları BCa yöntemi ile 5000 yeniden
> örnekleme üzerinden hesaplanmıştır. Yol a (Beck → EMBU-P) β = 0.31 (SE = 0.06), yol b
> (EMBU-P → EMBU-C) β = 0.14 (SE = 0.05). İndirek etki ab = 0.043 (95% BCa GA [0.012, 0.078]),
> sıfırı içermediğinden anlamlıdır; toplam etkiye oranı (proportion mediated) %38'dir. Bayesian
> paralel testte (brms, weakly informative prior) indirek posterior medyan = 0.038 (89% HDI
> [0.012, 0.071]); ROPE [-0.05, 0.05] içinde kalan posterior oranı %67 olduğundan etki *yön
> olarak* net (pd = 99.4%) ancak *pratik olarak* sınırlıdır. Sensemakr (Cinelli & Hazlett, 2020)
> ile mediator-outcome confounder duyarlılığında Robustness Value (RV_q=0) = 0.07 hesaplanmış;
> ölçülmemiş bir karıştırıcının ses_latent değişkeninin 1.5 katı güçte olması durumunda
> indirek etki sıfırlanabilir. Bu paragraf KEŞİFSEL statüsündedir; OSF kaydında (`pytfe`) ana
> hipotezler arasında değildir."

## §24. LPA — Anne Tipoloji Şablonu

> "Anne tipolojisi gizil profil analiziyle (LPA) belirlenmiştir. Beck total skoru, EMBU-P dört
> alt ölçek puanı ve SES kompozit göstergeleri standardize edilerek tidyLPA (Rosenberg ve
> diğerleri, 2018) ile 1-6 profil çözümü karşılaştırılmıştır. En uygun çözüm dört profil olarak
> bulunmuş (BIC = 3148, entropy = .82, LMR-LRT p = .003, BLRT p < .001); profiller içerik
> temelinde 'Adapte ebeveyn' (n = 78, %32), 'Aşırı koruyucu' (n = 64, %27), 'Tükenmiş' (n = 49,
> %20) ve 'Standart' (n = 50, %21) olarak adlandırılmıştır. Profil dağılımı DM ve Kontrol grupları
> arasında anlamlı farklılaşmıştır χ²(3) = 18.4, p < .001, Cramér's V = .28; özellikle 'Tükenmiş'
> profilde DM oranı %71 olarak bulunmuştur. Bu bulgular keşifsel statüdedir."

## §25. GGM + NCT Şablonu

> "Anne ruh sağlığı ve ebeveynlik tutumu değişkenleri arasındaki koşullu bağımlılık yapısı
> Gaussian Graphical Model (Epskamp, Borsboom & Fried, 2018) ile EBIC-LASSO regularization
> kullanılarak tahmin edilmiştir (gamma = 0.5, Spearman korelasyon, n = 241 aile). Beck total,
> EMBU-P dört alt ölçeği, SES latent ve anne yaşı node olarak alınmıştır. En güçlü kenar Beck
> ↔ Reddetme arasında (β = 0.32) gözlenmiştir; merkezilik analizi Beck ve Reddetme'yi en güçlü
> 'hub' olarak tanımlamıştır (Strength CS-coefficient = .67, kabul edilebilir üstü; Epskamp ve
> diğerleri, 2018 eşiği). Network Comparison Test'te (van Borkulo ve diğerleri, 2017; nperm =
> 1000) DM ve Kontrol grupları arasında global strength farkı anlamlıdır (M_DM = 4.21,
> M_Kontrol = 3.18, p = .024); ağın genel topolojisi farklı değildir (network invariance
> p = .41). Edge-by-edge testlerde Holm düzeltmesi sonrası Beck ↔ Reddetme kenarı DM lehine
> güçlenmiştir (Δβ = 0.18, p_Holm = .031). Bu bulgular keşifsel olarak değerlendirilmektedir."

## §26. Risk Skoru + ROC + DCA + Calibration Şablonu

> "Yüksek riskli anne (Beck total ≥ 17, Hisli 1989 Türk normu orta-üstü) tahmini için lojistik
> regresyon temelli risk skoru türetilmiştir (n = 241 aile). Demografik (yaş, eğitim) ve
> psikososyal (antidepresan kullanımı, SES latent, çocuk sayısı) belirteçler içeren modelin AUC =
> .78 (95% GA [.72, .84]) olarak hesaplanmış; Hosmer ve Lemeshow (2013) sınıflamasında 'kabul
> edilebilir' aralıkta yer almaktadır. Vickers ve Elkin (2006) decision curve analizinde model
> 'treat all' ve 'treat none' stratejilerine göre 0.10–0.30 risk eşiğinde anlamlı net fayda
> göstermiştir; örn. p = .20 eşiğinde NB = 0.10. Pencina ve diğerleri (2008) NRI = .24
> (95% bootstrap GA [.12, .36]) anne ruh sağlığı belirteçlerinin demografik temele eklenmesinin
> marjinal sınıflandırma iyileştirmesi sağladığını göstermiştir; cfNRI = .19 (sürekli alternatif).
> Calibration eğrisi (bootstrap-corrected, B = 1000) intercept = -0.04, slope = 1.06 ile kabul
> edilebilir kalibrasyon göstermektedir; Hosmer-Lemeshow χ²(8) = 9.4, p = .31. Bu bulgular
> keşifsel statüdedir ve dış validasyon gerektirmektedir."

## §27. Multiverse + TOST + Sensemakr Üçlü Robustluk Şablonu

> "EMBU-P Reddetme alt ölçeğinde DM-Kontrol farkı için Steegen ve diğerleri (2016) çoklu evren
> analizi uygulanmıştır. Dört skorlama (mean / sum / 7-item / BSEM latent) × üç model (lm /
> Huber-M / GEE) × beş kovaryat seti × otuz alt-örneklem = 1800 spesifikasyon çalıştırılmıştır;
> medyan Cohen's d = -0.13, %5–%95 spec aralığı [-0.30, +0.05], spec'lerin %7'sinde p < .05
> bulunmuştur. Simonsohn ve diğerleri (2020) inferential test'te (n_perm = 5000) Z_median = -1.42
> (p = .16), Z_share = -1.18 (p = .24); spec-bağımsız anlamlılık kanıtı yoktur. Lakens (2017)
> iki-tek-yönlü test (TOST) eşdeğerlik analizinde SESOI = ±0.30 SMD (Pinquart 2013 meta-analiz
> temelli) ile p = .087, 90% CI etki sınırlarını içermektedir; sonuç INDETERMINATE (ne anlamlı
> fark ne de eşdeğerlik). Cinelli ve Hazlett (2020) sensemakr analizinde Robustness Value
> (RV_q=0) = 0.04 hesaplanmış; bu, ölçülmemiş bir karıştırıcının SES'in 1.2 katı güçte olması
> durumunda ana etkiyi sıfırlayabileceğini göstermiştir. VanderWeele ve Ding (2017) E-value =
> 1.4 (95% GA alt sınır 1.0) — küçük bir bilinmeyen karıştırıcı sonucu silebilir. Bu üçlü kanıt
> zinciri, Reddetme alt ölçeğindeki DM-Kontrol farkının sağlam yorumlanamayacağına işaret
> etmektedir."

## §28. Bayesian Dual Reporting Şablonu

> "H1 birincil hipotezi (rol grupları arası EMBU-C alt ölçek farkları) frequentist multilevel
> ANCOVA'ya paralel olarak Bayesian multilevel modelleme ile değerlendirilmiştir. brms paketi
> (Bürkner, 2017) ile dört zincirli MCMC (4 chain × 4000 iter × 1500 warmup, adapt_delta = 0.99)
> kullanılmış; Pinquart (2013) meta-analizinden türetilmiş zayıf bilgi verici prior'lar
> (DM-Kontrol için *N*(0.30, 0.50)) uygulanmıştır. Yakınsama tüm parametrelerde sağlanmıştır
> (R̂ ≤ 1.005, ESS_bulk ≥ 4200, divergent transitions = 0). EMBU-C Reddetme alt ölçeği için
> DM-İndeks vs Kontrol-İndeks karşılaştırmasında posterior medyan = 0.34, %89 HDI [0.12, 0.56],
> probability of direction = 99.4%, ROPE [-0.10, 0.10] içi posterior oranı %4. Savage-Dickey
> Bayes faktörü BF₁₀ = 23.7 (Jeffreys 1961, Wagenmakers 2007 sınıflamasında 'güçlü kanıt'). LOO
> karşılaştırmasında tam model null modele üstün (Δelpd_loo = 8.4, SE = 2.6 → güçlü tercih). Bu
> Bayesian sonuçlar frequentist multilevel ANCOVA ile uyumludur (F = 6.8, p < .001, p_FDR =
> .003)."

## §29. Joint Display Şablonu (Karma Yöntem)

> "Çalışmanın karma yöntem boyutunda Creswell ve Plano Clark (2018) eşzamanlı paralel tasarımı
> uygulanmıştır. Altı T1DM annesi ile yarı-yapılandırılmış görüşme yapılmış; transkriptler Braun
> ve Clarke (2022) reflexive thematic analysis çerçevesinde altı fazda kodlanmıştır. İki bağımsız
> kodlayıcı (PI ve harici klinik psikolog) tarafından yapılan kodlamada Gwet AC1 = .76 (Gwet,
> 2014; kabul edilebilir uyum) bulunmuştur. Beş tema ortaya çıkmıştır: 'Sürekli denetim yükü',
> 'Suçluluk ve fedakarlık dili', 'Eşit muamele kaygısı', 'Tükenmişlik ve terapi arayışı' ve
> 'İdeal anne normuna yapışma'. Joint display tablosunda sekiz nicel bulgudan yedi convergent,
> bir discrepant sonuç saptanmıştır. Discrepant bulgu (DM Reddetme self-report düşük + niteliksel
> 'sertlik' teması) sosyal istenirlik kompansasyonu hipoteziyle yorumlanmış (Streisand & Monaghan,
> 2014) ve ileri çalışma için kardeş-spesifik analiz önerisi getirilmiştir. Bu karma yöntem
> entegrasyonu tezin keşifsel katmanını oluşturmaktadır."
