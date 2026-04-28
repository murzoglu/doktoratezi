# H5 — Diadik Tutarlılık (KISIM V genişletmesi)

> SAP v3.0 §16. **Tezin birincil yenilik katkısı.** Anne (EMBU-P) ↔ indeks-çocuk (EMBU-C-idx) ↔ kardeş
> (EMBU-C-sib) algıları arasındaki **uyum/uyumsuzluk yapısı**. 5 stratejinin **paralel** çalıştırılması
> zorunlu — herhangi biri yedek değildir, hepsi farklı bir bilgi katmanı verir.

## Niye 5 strateji paralel?

| Strateji | Soruyu yanıtlar | Sınırlılığı | Birincil/Yedek |
|---|---|---|---|
| **ICC + Bland-Altman** | Mutlak uyum nedir? | Latent yapıyı görmez | Birincil görsel + numeric |
| **RSA (Edwards-Parry)** | Tutarsızlık örüntüsü → outcome ilişkisi | n=120/121 alt-örnek için sınırlı güç | Keşifsel |
| **Common Fate Model** | Aile-içi ortak yapı vs idiyosenkrazi | Identification küçük örnekte zor | Doğrulayıcı |
| **Olsen-Kenny Dyadic CFA** | Ölçüm hatasından arındırılmış "true concordance" | WLSMV küçük n'de unstable | Birincil latent |
| **k-coefficient (Kenny)** | Aktör vs partner yapısı (individualistic/couple/contrast) | Yorumlama zor | Tamamlayıcı |

> **Kural:** En az 3'ü uyumlu sonuç verirse triangulasyon güçlü. Discrepant sonuç → tartışmada
> şeffaf raporlanır, tek bir strateji "gerçek" ilan edilmez.

## Strateji 1 — ICC(2,1) + Bland-Altman

**Amaç:** Mutlak uyum (agreement) — sadece korelasyon (consistency) değil, **aynı skor** mu?

```r
run_h5_concordance <- function(df_family) {
  subscales <- c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")

  results <- map_dfr(subscales, function(sub) {
    p_col      <- paste0("embu_p_", sub, "_mean")
    c_idx_col  <- paste0("embu_c_idx_q", sub, "_mean")
    c_sib_col  <- paste0("embu_c_sib_q", sub, "_mean")

    dyad_results <- list(
      anne_idx = df_family[, c(p_col, c_idx_col, "group_f")],
      anne_sib = df_family[, c(p_col, c_sib_col, "group_f")],
      idx_sib  = df_family[, c(c_idx_col, c_sib_col, "group_f")]
    )

    purrr::imap_dfr(dyad_results, function(dyad_df, dyad_name) {
      dyad_df <- na.omit(dyad_df)
      if (nrow(dyad_df) < 10) return(tibble())

      # ICC(2,1) twoway agreement single-rater (Shrout & Fleiss 1979)
      iccs <- dyad_df |>
        group_by(group_f) |>
        summarise(
          n = n(),
          icc = irr::icc(across(1:2), model = "twoway",
                          type = "agreement", unit = "single")$value,
          icc_lo = irr::icc(across(1:2), model = "twoway",
                              type = "agreement", unit = "single")$lbound,
          icc_hi = irr::icc(across(1:2), model = "twoway",
                              type = "agreement", unit = "single")$ubound,
          .groups = "drop"
        )

      # Bland-Altman LoA — group-spesifik
      ba_dm <- BlandAltmanLeh::bland.altman.stats(
        dyad_df[[1]][dyad_df$group_f == "DM"],
        dyad_df[[2]][dyad_df$group_f == "DM"])
      ba_ko <- BlandAltmanLeh::bland.altman.stats(
        dyad_df[[1]][dyad_df$group_f == "Kontrol"],
        dyad_df[[2]][dyad_df$group_f == "Kontrol"])

      bind_rows(
        tibble(subscale=sub, dyad_type=dyad_name, group="DM",
                n=iccs$n[iccs$group_f=="DM"],
                icc=iccs$icc[iccs$group_f=="DM"],
                mean_diff=ba_dm$mean.diffs,
                loa_lo=ba_dm$lower.limit, loa_hi=ba_dm$upper.limit),
        tibble(subscale=sub, dyad_type=dyad_name, group="Kontrol",
                n=iccs$n[iccs$group_f=="Kontrol"],
                icc=iccs$icc[iccs$group_f=="Kontrol"],
                mean_diff=ba_ko$mean.diffs,
                loa_lo=ba_ko$lower.limit, loa_hi=ba_ko$upper.limit)
      )
    })
  })

  results
}
```

### ICC yorum eşikleri (Koo & Li 2016, *J Chiropr Med*)

| ICC | Yorum | Klinik anlamı |
|---|---|---|
| < .50 | Düşük | Anne ↔ çocuk algıları büyük ölçüde bağımsız |
| .50–.75 | Orta | Kısmi uyum |
| .75–.90 | İyi | Güçlü uyum |
| > .90 | Mükemmel | Hemen hemen aynı algı |

**T1DM beklentisi:** Reddetme alt ölçeğinde ICC ≈ .16–.30 (düşük) → algı disconnect'i ana bulgu.

### Bland-Altman raporlama

```
DM Sıcaklık (anne ↔ indeks-çocuk):
  Ortalama fark: −0.42 (anne daha düşük)
  %95 LoA: [−1.85, +1.01]
  → Bireysel ailelerde 1.85 puana kadar farklılaşma görülüyor;
    sistematik bias yok ama dispersiyon yüksek.
```

## Strateji 2 — Response Surface Analysis (RSA)

**Amaç:** Edwards & Parry (1993) — tutarsızlık örüntüsünün **outcome ile ilişkisini** polinom yüzey
analiziyle gösterir. Klasik fark skoru (P − C) bilgi kaybeder; RSA korur.

```r
run_h5_rsa <- function(df_family) {
  library(RSA)

  subscales <- c("sicaklik", "reddetme")  # Ana iki teorik faktör

  results <- map(subscales, function(sub) {
    p_col      <- paste0("embu_p_", sub, "_mean")
    c_idx_col  <- paste0("embu_c_idx_q", sub, "_mean")

    # Group-spesifik RSA (DM ve Kontrol ayrı)
    rsa_dm <- RSA(
      formula = as.formula(paste("beck_total ~", p_col, "*", c_idx_col)),
      data = filter(df_family, group_f == "DM"),
      models = c("full", "SQD", "RR")
    )
    rsa_ko <- RSA(
      formula = as.formula(paste("beck_total ~", p_col, "*", c_idx_col)),
      data = filter(df_family, group_f == "Kontrol"),
      models = c("full", "SQD", "RR")
    )

    list(subscale = sub, dm = rsa_dm, kontrol = rsa_ko,
          dm_summary = summary(rsa_dm$models$full),
          ko_summary = summary(rsa_ko$models$full))
  })

  results
}
```

### Edwards-Parry 4 anahtar parametre

| Parametre | Anlamı | Tezde nasıl yorumlanır? |
|---|---|---|
| **a1** = b1 + b2 | Concordant artışın ana etkisi | Anne ve çocuk birlikte yüksek → outcome ne olur? |
| **a2** = b3 + b4 + b5 | Yüzeyin nonlinear kürvatürü (concordant high vs concordant low) | U-şekilli mi, ters-U mu? |
| **a3** = b1 − b2 | Tutarsızlık yönü (kim daha yüksek?) | Anne ↑ Çocuk ↓ vs tersi outcome'u nasıl etkiler? |
| **a4** = b3 − b4 + b5 | Tutarsızlık derecesinin etkisi | "Daha tutarsız → daha yüksek Beck" mi? |

### Yorum şablonu (Türkçe APA)

> "DM grubunda anne ve indeks-çocuk Reddetme algılarının uyumsuzluk derecesi (a4) Beck total ile
> pozitif ilişkili görünmüştür (a4 = 0.42, %95 GA [0.10, 0.74]); yani anne ve çocuk algısı ne kadar
> ayrışıyorsa anne depresyon belirtileri o kadar yüksek olmaktadır. Bu örüntü Kontrol grubunda
> görülmemiştir (a4 = 0.08, %95 GA [−0.18, 0.34]). Bulgu, Edwards & Parry (1993) çerçevesinde
> incongruence-as-stressor hipotezi ile uyumludur."

> **Sınırlılık:** RSA n=120 alt-grupta unstable olabilir. CI bandı genişse `[KEŞİFSEL]` etiketi.

## Strateji 3 — Common Fate Model (CFM)

**Amaç:** Aile-içi **ortak parenting yapısı** (latent) ile her bilgi-kaynağına özgü idiyosenkrazi
arasındaki ayrım (Ledermann & Macho 2009). Üç informant'ın (anne + 2 çocuk) ortak işaretiyle
maskelenen aile-düzeyi gerçeği yakalar.

```r
run_h5_common_fate <- function(df_family) {
  cfm_models <- map(c("sicaklik", "reddetme"), function(sub) {
    p_col     <- paste0("embu_p_", sub, "_mean")
    c_idx_col <- paste0("embu_c_idx_q", sub, "_mean")
    c_sib_col <- paste0("embu_c_sib_q", sub, "_mean")

    cfm_model <- sprintf('
      common_%s =~ %s + %s + %s
      common_%s ~ group_f + scale(anne_yas) + scale(ses_latent)

      %s ~~ %s
      %s ~~ %s
      %s ~~ %s
    ', sub, p_col, c_idx_col, c_sib_col, sub,
       p_col, p_col, c_idx_col, c_idx_col, c_sib_col, c_sib_col)

    fit <- lavaan::sem(cfm_model, data = df_family,
                         estimator = "MLR", missing = "fiml")

    list(subscale = sub, fit = fit,
          fit_meas = fitMeasures(fit, c("cfi","rmsea","srmr")))
  })

  cfm_models
}
```

**Yorum:** Common factor üzerinde DM etkisi anlamlıysa → "aile-düzeyi parenting iklimi" gerçekten
DM'den etkileniyor; her bir informant'ın bireysel raporundan çıkarmak yetersiz olabilir.

## Strateji 4 — Olsen-Kenny Dyadic CFA

**Amaç:** Ölçüm hatasından arındırılmış **true latent concordance** (Olsen & Kenny 2006). Anne ↔
çocuk arasındaki **gerçek** uyum, ölçek yetersizliği ile karıştırılmaz.

```r
run_h5_olsen_kenny_dyadic_cfa <- function(df_family) {
  # Reddetme alt ölçeği için anne ↔ indeks-çocuk dyadic CFA
  dyad_cfa_model <- '
    rejection_mom    =~ embu_p_q05 + embu_p_q09 + embu_p_q10 + embu_p_q12
    rejection_child  =~ embu_c_idx_q05 + embu_c_idx_q09 +
                         embu_c_idx_q10 + embu_c_idx_q12

    # Aynı maddenin korele rezidüleri (method effect)
    embu_p_q05 ~~ embu_c_idx_q05
    embu_p_q09 ~~ embu_c_idx_q09
    embu_p_q10 ~~ embu_c_idx_q10
    embu_p_q12 ~~ embu_c_idx_q12

    # Latent korelasyon = TRUE concordance (ölçüm hatası dışlanmış)
    rejection_mom ~~ rejection_child
  '

  fit_dyad <- lavaan::cfa(dyad_cfa_model, data = df_family,
                            ordered = TRUE, estimator = "WLSMV")

  list(fit = fit_dyad,
        true_concordance = inspect(fit_dyad, "cor.lv")["rejection_mom", "rejection_child"],
        fit_meas = fitMeasures(fit_dyad, c("cfi.scaled", "rmsea.scaled", "srmr")))
}
```

**Method effect etkisi:** Aynı maddenin anne ve çocuk yanıtları **korele residual** olarak modellenir;
böylece "aynı item üzerinden yanıt verme" kaynaklı sahte korelasyon dışlanır. Latent korelasyon
**genuine concordance**'tır.

### CFI/RMSEA eşikleri (WLSMV)

| Metrik | İyi | Kabul edilebilir |
|---|---|---|
| CFI.scaled | ≥ .95 | ≥ .90 |
| RMSEA.scaled | ≤ .06 | ≤ .08 |
| SRMR | ≤ .08 | ≤ .10 |

## Strateji 5 — k-Coefficient (Kenny et al. 2006)

**Amaç:** Aktör (kendi etkisi) vs partner (diğerinin etkisi) ilişki yapısının **doğasını** anlama.

```r
run_h5_k_coefficient <- function(df_long) {
  # k = partner_effect / actor_effect
  # k =  0: actor-only model (individualistic)
  # k =  1: couple model (actor = partner; dyad sum matters)
  # k = -1: contrast model (relative comparison matters)

  apim_redd <- nlme::lme(
    fixed = embu_c_qreddetme_mean ~ group_f * family_role_f,
    random = ~ 1 | aile_no_f,
    data = df_long,
    method = "REML"
  )

  fixed_coefs <- fixef(apim_redd)
  actor_eff <- fixed_coefs["group_fDM"]
  partner_eff <- fixed_coefs["group_fDM:family_role_fsibling"]

  k <- partner_eff / actor_eff

  # Bootstrap CI (BCa)
  k_boot <- boot::boot(data = df_long, statistic = function(d, i) {
    m <- nlme::lme(embu_c_qreddetme_mean ~ group_f * family_role_f,
                    random = ~ 1 | aile_no_f, data = d[i, ])
    coefs <- fixef(m)
    coefs["group_fDM:family_role_fsibling"] / coefs["group_fDM"]
  }, R = 1000)

  list(k = k, ci = boot::boot.ci(k_boot, type = "bca"))
}
```

### k yorumu

| k değeri | Model | Anlamı |
|---|---|---|
| ≈ 0 | **Actor-only** | Her çocuk yalnız kendi DM-statüsünden etkileniyor |
| ≈ 1 | **Couple** | İki kardeş ortak bir aile sistemi gibi tepki veriyor |
| ≈ −1 | **Contrast** | Bir kardeşin yüksekliği diğerini düşürür (rivalry pattern) |

## Diadik Tutarsızlık Klinik Yorumu

| Tutarsızlık örüntüsü | Klinik yorum | Operasyonalizasyon |
|---|---|---|
| Anne ↑ Çocuk ↓ (sıcaklık) | Anne savunmacı / sosyal istenirlik | `embu_p_sicaklik − embu_c_sicaklik > 0.5` |
| Anne ↓ Çocuk ↑ (reddetme) | Anne aşırı öz-eleştiri | `embu_c_reddetme − embu_p_reddetme > 0.5` |
| İki kardeş arası uyumsuzluk | **Differential Parental Treatment (PDT)** | `\|c_idx − c_sib\| > 0.5` |

> **Beklenen örüntü:** Streisand & Monaghan (2014) kronik hastalık ailelerinde **anne savunmacılığının**
> Kontrol'den daha güçlü olduğunu öngörür. Mevcut psikometrik validasyon bulgusu (DM Reddetme
> self-report < Kontrol Reddetme) bu hipotezle uyumlu.

## Targets entegrasyonu (gelecek faz)

```r
# _targets.R'ye eklenecek (KISIM V H5 ileri faz)
tar_target(h5_concordance,         run_h5_concordance(df_family_scored)),
tar_target(h5_rsa,                 run_h5_rsa(df_family_scored)),
tar_target(h5_common_fate,         run_h5_common_fate(df_family_scored)),
tar_target(h5_olsen_kenny_cfa,     run_h5_olsen_kenny_dyadic_cfa(df_family_scored)),
tar_target(h5_k_coefficient,       run_h5_k_coefficient(df_long_scored)),
tar_target(h5_concordance_table,   format_h5_concordance(h5_concordance),
            format = "file")
```

## Raporlama paragrafı (Türkçe APA 7)

> "Anne ve indeks-çocuk Reddetme alt ölçeği algıları arasındaki uyum DM grubunda ICC(2,1) = .19
> (95% GA [.06, .32]); Kontrol grubunda ICC(2,1) = .31 (95% GA [.18, .43]) olarak hesaplanmıştır;
> her iki değer de Koo ve Li (2016) düşük uyum eşiğindedir. Olsen-Kenny diadik CFA'da ölçüm
> hatasından arındırılmış latent korelasyon DM = .24, Kontrol = .38 olarak elde edilmiş, bu da ham
> ICC'lerin gerçek yapıyı az aşağı tahmin ettiğini göstermiştir. Edwards & Parry (1993) RSA çerçevesinde,
> tutarsızlık derecesi (a4) DM grubunda Beck total ile pozitif ilişkili bulunmuş (a4 = 0.42, %95 GA
> [0.10, 0.74]); Kontrol grubunda anlamlı bir ilişki gözlenmemiştir. Üç stratejinin ortak gösterdiği
> örüntü, T1DM ailelerinde **anne–çocuk algı uyuşmazlığının** anne ruh sağlığı yüküyle bağlantılı
> olabileceğine işaret etmektedir."

## Tedbir denetimi

- [ ] ICC(2,1) **agreement** seçildi (consistency değil) — mutlak uyum sorgulanıyor
- [ ] Bland-Altman LoA güveni n ≥ 30 (her grup için ayrı) sağlandı
- [ ] RSA için n ≥ 100 alt-grup temelinde sonuçlar `[KEŞİFSEL]` etiketli
- [ ] CFM model identification'ı (df > 0) doğrulandı
- [ ] Olsen-Kenny WLSMV küçük örnekte unstable → bootstrap CI tercih edildi
- [ ] k-coefficient bootstrap CI BCa kullanıldı (asimptotik değil)
- [ ] Discrepant strateji sonucu varsa ön-kayıt sapma tablosuna eklendi

## Çapraz referanslar

- Multilevel APIM zemin için → [`multilevel-aile-yapisi.md`](multilevel-aile-yapisi.md) (k = partner/actor formülü)
- Lavaan SEM/CFA detayları → [`ileri-yontemler.md`](ileri-yontemler.md)
- WLSMV ordinal parametreler → [`psikometri-pipeline.md`](psikometri-pipeline.md)
- Bayesian H5 → [`bayesci-paralel-hat.md`](bayesci-paralel-hat.md) (RSA için brms preflight)
- Joint display ile niteliksel verilerle entegrasyon → [`karma-yontem.md`](karma-yontem.md)
