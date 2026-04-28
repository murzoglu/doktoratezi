# KISIM XIII — Karma Yöntem Entegrasyonu

> SAP v3.0 §40–41. Reflexive Thematic Analysis (Braun & Clarke 2022) + Joint Display +
> Convergence Analysis (Creswell & Plano Clark 2018). **[KEŞİFSEL]** statüsünde — niteliksel
> görüşme verisi (~6 transkript) tezde *triangulation* katmanı.

## Niye Karma Yöntem?

Nicel analiz "ne kadar?" yanıtlar; niteliksel "neden ve nasıl?". T1DM aile bağlamında özellikle:
- Anneler **kendi sözleriyle** parenting deneyimini nasıl tanımlıyor?
- Nicel olarak görünmeyen **gizli yapısal sorunlar** (ör. healthcare contact bias) niteliksel
  görüşmelerde ortaya çıkıyor mu?
- Discrepant nicel-niteliksel bulgular yeni hipotez doğurabilir.

> **Convergent Parallel Design** (Creswell & Plano Clark 2018): nicel ve niteliksel veri **paralel**
> toplanır, **bağımsız** analiz edilir, sonra **eşit ağırlıkta** entegre edilir.

## 1. Reflexive Thematic Analysis (RTA)

### Niye RTA, Klasik TA değil?

Braun & Clarke 2022 *Thematic Analysis: A Practical Guide* — orijinal 2006 makalesinden farklı
olarak **reflexive** vurgu: tema "verinin içinde gizli" değildir; araştırmacı **anlam üretiminde
aktif faildir**. Bu yaklaşım:
- "İnter-coder reliability" zorunlu değildir (RTA epistemolojik olarak buna karşı)
- Saturation kavramı RTA için uygun değil (Braun & Clarke 2021)
- Researcher reflexivity raporlanır

### Altı Faz Protokolü (B&C 2022)

| Faz | Açıklama | Çıktı |
|---|---|---|
| **1. Aşinalık** | Transkriptlerin tam okuma + yansıtıcı not | Analitik notlar |
| **2. Kodlama** | Madde madde anlam birimleri | Kod hattı |
| **3. Tema oluşturma** | Kodları kavramsal kümelere dönüştürme | İlk tema haritası |
| **4. Tema gözden geçirme** | Veriye karşı temaları test | Düzeltilmiş tema haritası |
| **5. Tanımlama + isimlendirme** | Her temaya kavramsal kimlik | Final tema şeması |
| **6. Yazım** | Analitik anlatı + alıntı | Bulgular bölümü |

### Klasik TA için inter-coder reliability (gereksinim olarak)

Tezde RTA + klasik TA hibrit: tematik harita reflexive üretilir, ama **iki bağımsız kodlayıcı**
ile güvenirlik raporlanır (jüri için savunulabilir).

```r
library(irrCAC); library(tidytext)

# İki kodlayıcı: Murzoğlu Kurt (PI) + harici psikolog
# Aynı 6 transkriptin manuel kodlanması

# Cohen's kappa (kategorik)
kappa_result <- irrCAC::kappa2.table(coding_table_2x2)

# Gwet AC1 (kategori dengesizliği için tercih edilir)
gwet_result <- irrCAC::gwet.ac1.raw(coding_matrix)

cat("Cohen's κ:", round(kappa_result$est$coeff_val, 3), "\n")
cat("Gwet AC1:",  round(gwet_result$est$coeff_val, 3), "\n")
```

| Metrik | Eşik | Yorum |
|---|---|---|
| **AC1 > 0.80** | Çok iyi | Landis & Koch (1977) modifiye |
| **AC1 > 0.60** | Kabul edilebilir | — |
| **AC1 < 0.60** | Düşük | Kodlama protokolü revize |

> **Niye Gwet AC1, Cohen's κ değil?** Cohen's κ kategori dengesiz (skewed prevalence) olduğunda
> *paradoksal olarak* düşük çıkar (Gwet 2014). T1DM görüşmelerde belirli temalar baskın olacağı
> için AC1 daha güvenilir.

## 2. Tema-Frekans Analizi (Triangulasyon)

```r
library(tidytext); library(quanteda)

turkish_stopwords <- quanteda::stopwords("turkish")

theme_word_freq <- transcripts |>
  unnest_tokens(word, text) |>
  anti_join(tibble(word = turkish_stopwords)) |>
  filter(!str_detect(word, "^[0-9]+$"),     # Numerik dışla
          nchar(word) > 2) |>
  count(participant_role, theme, word) |>
  group_by(participant_role, theme) |>
  slice_max(order_by = n, n = 15)

# Sankey/alluvial: rol × tema akışı
library(ggalluvial)
ggplot(theme_word_freq, aes(axis1 = participant_role, axis2 = theme,
                              y = n)) +
  geom_alluvium(aes(fill = theme)) +
  geom_stratum() +
  geom_text(stat = "stratum", aes(label = after_stat(stratum))) +
  theme_void()
```

> **Uyarı:** Frekans analizi RTA'nın **destekleyici** katmanıdır, değiştirici değil. Bir tema sık
> görünmediği halde teorik açıdan kritik olabilir (Braun & Clarke 2021).

## 3. Joint Display ve Convergence Analysis

### Convergent Parallel Design tipleri

| Tip | Tanım | Yorumsal Ağırlık |
|---|---|---|
| **Convergent** | Nicel + niteliksel aynı sonucu söylüyor | Bulgu güçlendirilmiş |
| **Complementary** | Nicel + niteliksel tamamlayıcı (overlap yok) | Bulgu zenginleştirilmiş |
| **Discrepant** | Nicel + niteliksel zıt | Yeni hipotez gerekli |

### Joint Display Tablosu

```r
joint_display <- tribble(
  ~quant_finding,                                       ~qual_theme,                                                            ~convergence,
  "DM annelerinde Reddetme self-report DÜŞÜK (d=-0.14)", "Anneler suçluluk + fedakarlık dilini kullanıyor",                     "Convergent",
  "DM grubunda Aşırı Koruma yüksek (d=+0.30)",           "Sürekli denetim ve kaygı tanımı; 'ona her zaman göz kulak olmalıyım'", "Convergent",
  "EMBU-C Karşılaştırma × SRQ Çatışma r=.30",            "Kardeşler 'eşit muamele' eksikliğinden bahsediyor",                   "Convergent",
  "İndeks-kardeş ICC ≈ .16-.30",                         "Hasta çocuk dikkatten faydalanma; sağlıklı kardeş geri planda kalma", "Convergent (PDT teyit)",
  "DM Reddetme self-report DÜŞÜK (anlamsız)",            "Bazı kardeşler annenin 'sert' olduğundan bahsediyor",                 "**Discrepant**",
  "Maternal Beck × Karşılaştırma r=+.26",                "Annelerin tükenmişlik + öz-eleştiri hikayesi",                        "Convergent",
  "Anne antidepresan DM'de %29 (Kontrol %9)",            "Anneler 'dayanamadım, terapiye başladım' söylemi",                    "Convergent + yeni",
  "LPA Profil 3 (Tükenmiş) DM-yoğun",                    "'İçinden çıkamadım' tematik kümesi DM annelerinde belirgin",          "Convergent"
) |>
  gt() |>
  cols_label(
    quant_finding = "Nicel Bulgu",
    qual_theme    = "Niteliksel Tema",
    convergence   = "Yakınsama Düzeyi"
  ) |>
  tab_header(title = "**Tablo X. Karma Yöntem Joint Display**",
              subtitle = "Convergent Parallel Design (Creswell & Plano Clark 2018)") |>
  tab_style(
    style = cell_fill(color = "#FEE0E0"),
    locations = cells_body(rows = convergence == "**Discrepant**")
  )
```

## 4. Discrepant Bulgu Yorumu — Tezde Önemli

> **Discrepant örnek:** Nicel veriden DM annelerinin Reddetme öz-rapor puanı kontrolden DAHA DÜŞÜK
> çıkıyor (d = -0.14, anlamsız ama yön ters). Niteliksel görüşmelerde *bazı* kardeşler annenin
> "sert" olduğundan bahsediyor.

İki olası açıklama:

**(a) Sosyal istenirlik kompansasyonu:** Kronik hastalık çocuklu anneler healthcare contact bias ile
"ideal anne" kalıbına daha çok yapışıyor (Edmondson 1996; Streisand & Monaghan 2014). Çocuk algısı
bu kompensasyonu *yakalamıyor*.

**(b) Aşırı koruma kompensasyonu:** Koruyucu motivasyon reddedici davranışı seçici biçimde
bastırıyor ama sertlik başka bir kanaldan (örn. tıbbi yönetim çatışmasıyla) sızıyor.

Bu disconnect, **kardeş-spesifik analiz** (sağlıklı kardeş açısından "anne sertliği" puanı) ile
çözülebilir; ileri çalışma için hipotez doğurur.

## 5. Niteliksel Görüşme Protokolü (T1DM-EBEVEYN)

### Görüşme yapısı

| Aşama | Süre | İçerik |
|---|---|---|
| Açılış | 5 dk | Bilgilendirme, onam, pilot soru ("Bana çocuğunuzla bir gününüzden bahsedin") |
| Çekirdek | 30-40 dk | Yarı-yapılandırılmış soru rehberi |
| Kapanış | 5 dk | "Eklemek istediğiniz?" + post-interview reflection |

### Soru rehberi (örnek)

```
1. T1DM tanısı sonrası ailenizde neler değişti?
2. (Çocuğunuza nasıl yaklaşıyorsunuz?) Sağlıklı kardeşine nasıl yaklaşıyorsunuz?
3. Her iki çocuk için de "aynı muamele" yapabildiğinizi düşünüyor musunuz?
4. Hangi durumlarda kendinizi "tükenmiş" hissediyorsunuz?
5. Hastalık yönetimi ile ilgili çocuğunuzla anlaşmazlık yaşıyor musunuz?
6. Kendi annelik tarzınızı nasıl tanımlardınız?
```

### Etik

- Yazılı bilgilendirilmiş onam; TUBA İK referansı
- Ses kaydı yalnız onamla
- Transkripsiyon: tüm tanımlayıcı bilgi (ad, okul, hastane) anonimleştirilir (PII koruma —
  CLAUDE.md kuralı geçerli)
- Veri saklama: KVKK uyumlu, kontrollü erişim, OSF kontrollü erişim klasöründe

## Targets entegrasyonu (kısmi — çoğu manuel)

```r
# _targets.R'ye eklenecek (KISIM XIII keşifsel)
tar_target(qualitative_codebook,    "data/qualitative/codebook.csv", format = "file"),
tar_target(qualitative_kappa,       run_kappa_analysis(qualitative_codebook)),
tar_target(theme_freq_analysis,     run_theme_frequency(qualitative_codebook)),
tar_target(joint_display_table,     build_joint_display(quant_h1, quant_h2, theme_freq_analysis),
                                      format = "file"),
# Tematik analiz çoğu manuel; R sadece güvenirlik ve frekans için
```

## Tedbir denetimi

- [ ] RTA paradigması açıkça belirtildi (post-positivist değil, constructionist)
- [ ] Researcher reflexivity (PI'nin mesleki konumu, çocukluk deneyimi vb.) bulgular bölümünde raporlandı
- [ ] İki-kodlayıcı güvenirlik (Gwet AC1) > 0.60
- [ ] Saturation iddiası **kullanılmadı** (RTA ile uyumsuz)
- [ ] Tema sayısı çekirdek 4-6 arası (aşırı parçalı değil)
- [ ] Joint display'de discrepant bulgular *renklendirilmiş* ve tartışıldı
- [ ] Niteliksel veri OSF kontrollü erişim klasöründe; ham transkript paylaşılmıyor
- [ ] Anonimleştirme tam (özel ad, okul, hastane → "[anonim]")
- [ ] [KEŞİFSEL] etiketi mixedmethods bulgular için
- [ ] CONSORT-Mixed flow: nicel + niteliksel paralel akış raporlandı

## Raporlama paragrafı (Türkçe APA 7)

> "Çalışmanın karma yöntem boyutunda Creswell ve Plano Clark (2018) eşzamanlı paralel tasarımı
> uygulanmıştır. Altı T1DM annesi ile yarı-yapılandırılmış görüşme yapılmış; transkriptler Braun
> ve Clarke (2022) reflexive thematic analysis çerçevesinde altı fazda kodlanmıştır. İki bağımsız
> kodlayıcı (PI ve harici klinik psikolog) tarafından yapılan kodlamada Gwet AC1 = .76 (kabul
> edilebilir uyum) bulunmuştur. Beş tema ortaya çıkmıştır: 'Sürekli denetim yükü', 'Suçluluk ve
> fedakarlık dili', 'Eşit muamele kaygısı', 'Tükenmişlik ve terapi arayışı', 've 'İdeal anne
> normuna yapışma'. Joint display analizinde sekiz nicel bulgudan yedi convergent, bir discrepant
> sonuç saptanmıştır. Discrepant bulgu (DM Reddetme self-report düşük + niteliksel 'sertlik'
> teması) sosyal istenirlik kompansasyonu hipoteziyle yorumlanmış ve ileri çalışma için
> kardeş-spesifik analiz önerisi getirilmiştir. Bu karma yöntem entegrasyonu tezin **keşifsel**
> katmanını oluşturmaktadır."

## Çapraz referanslar

- Discrepant bulguların hipotez doğurması → [`tedbir-ve-hatalar.md`](tedbir-ve-hatalar.md)
- Joint display tablosunun papaja entegrasyonu → [`diseminasyon-ve-yayin.md`](diseminasyon-ve-yayin.md)
- Niteliksel + LPA tipoloji eşleştirmesi → [`latent-degisken-yontemleri.md`](latent-degisken-yontemleri.md)
- Kaynaklar: Creswell & Plano Clark (2018); Braun & Clarke (2022); Gwet (2014); Wisdom & Creswell (2013)
