# KISIM VIII — Network Analizi

> SAP v3.0 §24–26. Üç katman: **Gaussian Graphical Model (GGM)** — koşullu bağımlılık ağı,
> **Network Comparison Test (NCT)** — DM × Kontrol ağ farkı, **Beck madde-düzeyi symptom network** —
> psikopatoloji ağ teorisi (Borsboom 2017). Tümü **[KEŞİFSEL]**.

## Niye Network Analizi?

Klasik regresyon "her değişken sıralıdır" varsayar; klinik psikolojide **karşılıklı etki** ağ
yapısı daha gerçekçidir (Epskamp, Borsboom & Fried 2018). T1DM tezinde:
- Hangi parenting boyutu **merkezi** (centrality)?
- DM ailelerinde ağ yapısı Kontrol'den nasıl farklı?
- Beck'in 21 maddesi içinde "köprü semptomlar" hangileri?

## 1. Gaussian Graphical Model (EBIC-LASSO)

### Mantık

GGM = partial correlation network. Her kenar, **diğer tüm değişkenler kontrol edildiğinde** kalan
ilişkiyi gösterir. EBIC-LASSO regularization ile spurious kenarlar otomatik elenir.

```r
run_network_analysis <- function(df_family) {
  library(qgraph); library(bootnet)

  net_data <- df_family |>
    select(beck_total,
           embu_p_sicaklik_mean, embu_p_asiri_koruma_mean,
           embu_p_reddetme_mean, embu_p_karsilastirma_mean,
           ses_latent, anne_yas) |>
    drop_na()

  net_labels <- c("Beck","Sıcaklık","AşırıKor","Redd","Karş","SES","Yaş")

  # GGM with EBIC-LASSO (Epskamp 2018 default)
  net_estimate <- bootnet::estimateNetwork(
    net_data,
    default = "EBICglasso",
    corMethod = "spearman",  # nonparametric
    tuning = 0.5             # gamma — büyük olursa daha sparse ağ
  )

  # Görselleştirme
  png(file.path(OUTPUT_DIR, "figures", "network_full.png"),
       width = 1200, height = 1000, res = 150)
  plot(net_estimate, layout = "spring", labels = net_labels,
        title = "T1DM Aileleri — Koşullu Bağımlılık Ağı")
  dev.off()

  # Centrality (Strength, Closeness, Betweenness)
  centrality_df <- centralityTable(net_estimate)

  # Bootstrap edge stability — case-drop
  boot_net <- bootnet::bootnet(net_estimate, nBoots = 1000, type = "case",
                                 statistics = c("strength","closeness","betweenness"))

  # CS-coefficient (Epskamp 2018: > 0.50 güçlü, > 0.25 kabul edilebilir)
  cs_coef <- corStability(boot_net)

  list(network = net_estimate, centrality = centrality_df,
        bootstrap = boot_net, cs_coef = cs_coef)
}
```

### Centrality metrik yorumları

| Metrik | Anlamı | T1DM tezinde yorumu |
|---|---|---|
| **Strength** | Toplam edge ağırlığı | "En çok bağlı" değişken — sistem omurgası |
| **Closeness** | Ortalama mesafe (kısa = merkezi) | Ağdaki "hub" değişken |
| **Betweenness** | Diğer node'lar arasındaki yol sayısı | "Köprü" değişken — kesilirse alt-ağlar ayrılır |
| **Expected Influence** | Negatif edge'leri de hesaplar | Klinik müdahale önceliği |

> **CS-coefficient eşiği:** Epskamp et al. (2018) — > .50 → "güçlü" centrality stability; .25–.50
> → "kabul edilebilir"; < .25 → centrality yorumlanamaz.

### Tuning gamma seçimi

| Gamma | Etki |
|---|---|
| 0 | EBIC = BIC (en az sparse) |
| 0.25 | Orta sparse (önerilen baseline) |
| 0.5 | Daha sparse (çok temiz ağlar — küçük örneklem) |
| 1.0 | Çok sparse (sadece güçlü kenarlar) |

T1DM tezinde **gamma = 0.5** (n = 241 aile alt-grup analiz için yeterince sparse).

## 2. Network Comparison Test (NCT)

DM ailelerinin ağı Kontrol'den **istatistiksel olarak** farklı mı?

```r
run_network_comparison <- function(df_family) {
  library(NetworkComparisonTest)

  vars <- c("beck_total", "embu_p_sicaklik_mean", "embu_p_asiri_koruma_mean",
            "embu_p_reddetme_mean", "embu_p_karsilastirma_mean",
            "ses_latent", "anne_yas")

  net_dm <- df_family |> filter(group_f == "DM") |>
    select(all_of(vars)) |> drop_na()
  net_kontrol <- df_family |> filter(group_f == "Kontrol") |>
    select(all_of(vars)) |> drop_na()

  nct_result <- NCT(net_dm, net_kontrol, it = 1000,
                     binary.data = FALSE, paired = FALSE,
                     test.edges = TRUE, edges = "all",
                     test.centrality = TRUE)

  print(nct_result)
  nct_result
}
```

### NCT üç anahtar test (van Borkulo et al. 2017)

| Test | H0 | Yorum |
|---|---|---|
| **Network Invariance** | İki ağ aynı edge yapısına sahip | Genel topolojik fark var mı? |
| **Global Strength Invariance** | İki ağ toplam edge ağırlığı aynı | "Daha kalabalık" ağ var mı? |
| **Edge-by-edge** | Her bir edge eşit (Holm düzeltmeli) | Spesifik kenar farklılıkları |

### Çoklu karşılaştırma uyarısı

NCT edge-by-edge testi yüksek FWER üretir; Holm-Bonferroni veya BH-FDR önerilir.

## 3. Beck Item-Level Symptom Network

Borsboom (2017) — psikopatoloji "ağ teorisi": semptomlar birbirini *neden olarak* uyarır;
"merkezi semptomlar" tedavi hedefi.

```r
run_beck_item_network <- function(df_family) {
  beck_data <- df_family |>
    select(starts_with("beck_q") & !contains("total") & !contains("severity")) |>
    drop_na()

  beck_net <- bootnet::estimateNetwork(beck_data,
                                          default = "EBICglasso",
                                          corMethod = "spearman_thr_chi")

  beck_labels <- c("Üzüntü","Karamsarlık","Başarısızlık","Doyum kaybı",
                    "Suçluluk","Cezalandırılma","Memnuniyet","Eleştiri",
                    "İntihar","Ağlama","Sinirlilik","İlgi","Karar",
                    "Görünüm","İşlevsellik","Uyku","Yorgunluk","İştah",
                    "Kilo","Sağlık","Cinsel")

  png(file.path(OUTPUT_DIR, "figures", "beck_item_network.png"),
       width = 1400, height = 1200, res = 150)
  plot(beck_net, layout = "spring", labels = beck_labels,
        title = "Beck Maddeleri — Anne Depresyon Semptom Ağı")
  dev.off()

  # Hangi semptom "merkezi"? (Strength)
  strength_centrality <- centrality(beck_net)$InDegree

  list(network = beck_net, strength = strength_centrality)
}
```

### Beck network içgörü örneği

Beklenen merkez maddeler (literatür temelli):
- **Düşük benlik (Item 8 — Eleştiri)** — sıkça köprü
- **İşlevsellik kaybı (Item 15)** — günlük etkilemenin kapısı
- **Yorgunluk (Item 17)** — somatic-affective köprü

> **Sınırlılık:** Beck madde-network için n ≈ 240 aile yeterli ama 21 madde × 21 = 210 olası kenar
> bootstrap stability'de zorlanabilir. CS-coefficient < .25 ise yorum keşifsel.

## Targets entegrasyonu

```r
# _targets.R'ye eklenecek (KISIM VIII gelecek faz)
tar_target(network_full,            run_network_analysis(df_family_scored)),
tar_target(network_comparison_test, run_network_comparison(df_family_scored)),
tar_target(beck_item_network,       run_beck_item_network(df_family_scored)),
tar_target(network_centrality_table,
            format_centrality_table(network_full),
            format = "file"),
tar_target(beck_network_figure,
            export_network_figure(beck_item_network, "outputs/figures/beck_item_network.png"),
            format = "file")
```

## Tedbir denetimi

- [ ] Spearman correlation kullanıldı (parametrik varsayımdan kaçın)
- [ ] EBIC-LASSO gamma seçimi gerekçelendirildi
- [ ] Bootstrap CS-coefficient ≥ .25 (centrality yorumu için)
- [ ] Edge-by-edge NCT için Holm/BH düzeltme uygulandı
- [ ] Centrality interpretation reasonable n (vars ≥ n/3 değil)
- [ ] Network ↔ DAG karışımı yok — GGM **partial correlation**, nedensel değil
- [ ] [KEŞİFSEL] etiketi (KISIM VIII keşifseldir)

## Raporlama paragrafı (Türkçe APA 7)

> "Anne ruh sağlığı ve ebeveynlik tutumu değişkenleri arasındaki koşullu bağımlılık yapısı
> Gaussian Graphical Model (Epskamp, Borsboom & Fried 2018) ile EBIC-LASSO regularization
> kullanılarak (gamma = 0.5, Spearman korelasyon) tahmin edilmiştir. Beck total, EMBU-P dört
> alt ölçeği, SES latent ve anne yaşı node olarak alınmıştır (toplam 7 node). En güçlü kenar Beck
> ↔ Reddetme arasında (β = 0.32) gözlenmiştir; merkezilik analizi Beck ve Reddetme'yi en güçlü
> 'hub' olarak tanımlamıştır (Strength CS-coefficient = .67, kabul edilebilir üstü). Network
> Comparison Test'te (van Borkulo et al. 2017) DM ve Kontrol grupları arasında global strength
> farkı anlamlıdır (M_DM = 4.21, M_Kontrol = 3.18, p = .024); ağın genel topolojisi farklı
> değildir (network invariance p = .41). Bu bulgular **keşifsel** olarak değerlendirilmektedir; OSF
> kayıtlı ana hipotezler arasında değildir."

## Çapraz referanslar

- Korelasyon vs partial correlation ayrımı → [`tedbir-ve-hatalar.md`](tedbir-ve-hatalar.md)
- Bootstrap stability → [`etki-buyuklugu-ve-guc.md`](etki-buyuklugu-ve-guc.md)
- LPA profil × network birleştirmesi → [`latent-degisken-yontemleri.md`](latent-degisken-yontemleri.md)
- Beck symptom network → klinik fayda risk skoru → [`klinik-fayda.md`](klinik-fayda.md)
- Kaynaklar: Borsboom (2017); Epskamp et al. (2018); van Borkulo et al. (2017); Fried et al. (2017)
