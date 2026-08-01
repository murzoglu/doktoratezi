# EK İSTATİSTİK PLANI — FAZ III (KULLANILMAYAN DEĞİŞKEN YÜZEYLERİ · POST-HOC)

**Sürüm:** v0.3 (tam-metin doğrulaması) · **Tarih:** 2026-07-08
**v0.2 → v0.3 farkı:** Literatür çapaları OpenAthens (Millet Kütüphanesi) + Anna's Reader + Europe PMC ile **tam-metinden doğrulandı** (20 künye × çekişmeli doğrulama; §1.5.5 defter): **14 CONFIRMED, 5 CORRECTED, 1 NOT_FOUND**. Sonuç düzeltmeleri: (i) **McHale & Pawletko (1992)** "buffering/zayıf-bağ" atfı DÜZELTİLDİ — makale bağın zayıfladığını değil bağlam-bağımlı (hatta ters) ilişki bulur; buffering çapası Kowal-Kramer/McHale2000'e taşındı; (ii) **Sharpe & Rossiter (2002)** "d≈0.28" DÜZELTİLDİ → alan-özgü içe-yönelim d≈0.41, dışa-yönelim d≈0.15 (0.28 bu ikisinin ortalaması; kaynak 2023 güncelleme PMID 35950954); (iii) **Prikken et al. (2019)** operatif mediyatör DÜZELTİLDİ → aşırı koruma değil **psikolojik kontrol** (aşırı-koruma→uyum yolları non-anlamlı); (iv) **Conger et al. (2010)** β≈.20-.40 atfı KALDIRILDI (narratif derleme, nokta-katsayı yok); (v) Buist/Eradus/Pinquart/Malcová/Van Gampelaere/Downey kesin değerleri tam-metinle teyit edildi.
**v0.1 → v0.2 farkı:** (a) kanonik şema + **hücre-sayısı fizibilite denetimi** (§1.5) eklendi → birkaç analiz gerçekçi güç/kimliklenebilirlik temelinde yeniden sınıflandırıldı; (b) **Evidentia ile varlık-doğrulı literatür çapaları** (gerçek DOI/PMID) her KISIM'e işlendi (EK'teki "aday" liste artık doğrulanmış); (c) fark-skoru güvenilirliği (**ρ_DD formülü**), **RSA/polinom vs LDS** kararı, **SESOI + TOST** ve **MTMM/Operations-Triad** üçgenlemesi ile metodolojik derinleştirme; (d) 4 yapısal düzeltme (SRQ kayırma-madde eşlemesi, DRM kimliklenebilirlik, SES altyapı yeniden-kullanımı, R modül numaralandırması); (e) planın atladığı **veride-hazır yeni yüzeyler** (§1.6: anne istihdamı, eğitim homogamisi, SIOPS/ISEI/EGP yarışı, Beck-aracı FSM).
**Kapsam:** Ana SAP v3.0 (KISIM I–XVIII) ve Faz II post-hoc planı (`04-sap-faz2-posthoc.md`, KISIM XIX–XXXV, §47–95) **dışında** kalan, kanonik analiz bazında **mevcut ama analitik olarak hiç kullanılmamış** değişken bloklarını disiplinli keşif çerçevesinde ele alır.
**Veri:** Mevcut `FINAL_REFERENCE__analysis_base_{family,long}.csv` (family: 241 satır × 288 kolon; long: 482 satır × 203 kolon; kilit SHA-256 doğrulandı, `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`). **Yeni veri toplanmaz. Kanonik kilit DEĞİŞMEZ.**
**Epistemik statü:** Tüm analizler **[KEŞİFSEL · POST-HOC]** — Tip 3 sapma, OSF **Layer 4** (yeni). H1–H4 doğrulayıcı kanıt kademeleri (CSR Bölüm 11) **DEĞİŞMEZ**; hiçbir Faz III analizi confirmatory prior'ı güçlendirmez (HARKing yasağı, Skill Davranış Kuralı 20).

---

## 0. ÖN UYARI — Faz III Ne DEĞİLDİR

- **Faz II'nin tekrarı değildir.** Faz II çalışma-sonu verisinin ortaya çıkardığı psikometrik/klinik/metodolojik boşlukları (trifactor, MTMM, floor-IRT, causal-mediation sensitivity, multiverse, meta-pooling) kapatır. **Faz III ise farklı bir soruyu sorar:** *"Sosyodemografik-klinik formda topladığımız ama hiçbir modele girmemiş değişkenler bize ne söyleyebilir?"*
- **H1–H4'ü yeniden açmaz.** Confirmatory estimand, outcome ve model aileleri sabittir.
- **Klinik öneri üretmez.** Her bulgu hipotez-üretici; bağımsız Türk kohortunda dış-validasyon olmadan yükseltilmez.
- **Yeni ölçek/ölçüm eklemez.** Yalnız `FINAL_REFERENCE__*` içindeki hâlihazırda kayıtlı alanları modeller.
- **Fizibilite tavanının ötesine geçmez (v0.2 vurgusu).** Bir analiz veride *var* olması onun *test edilebilir* olduğu anlamına gelmez. §1.5 hücre-sayısı denetimi, birkaç v0.1 analizini "moderasyon" iddiasından "betimsel/gelecek-tasarım sinyali"ne indirir; bu güç-dürüstlüğü Faz III'ün jüri savunmasının çekirdeğidir.

> **Neden gerekli?** CSR ve Faz II, üç birincil ölçeğin (EMBU-P/C, Beck, SRQ) latent yapısını derinlemesine işledi; ancak **sosyodemografik-klinik form** (meslek ISCO-08 → ISEI/SIOPS/EGP kodlaması, anne+eş 14-kategori kronik hastalık matrisi, hane koşulları, aile yapısı, doğum sırası) yalnız Tablo 1 betimlemesinde ve tek bir SES-latent kompozitinde kullanıldı. Bu form, **ebeveynlik literatürünün merkezî bağlamsal değişkenlerini** (sosyal sınıf, materyal yoksunluk, bakım-veren yükü, aile yapısı, kardeş konstelasyonu) içeriyor ve bunların hiçbiri bir hipotez modeline girmedi.

---

## 1. BOŞLUK PROVENANSI — Hangi Değişken Bloğu × Neden Kullanılmadı

İki plan (`03-sap-ana-plan.md`, `04-sap-faz2-posthoc.md`) + CSR-FINAL taramasıyla doğrulanmış kullanım durumu:

| Değişken bloğu (kanonik ad) | Ana SAP | Faz II | CSR | Faz III fırsatı |
|---|---|---|---|---|
| `anne_hastalik_*` (14 kategori) + `anne_hastalik_kategori_sayisi` | ✗ | ✗ | ✗ | **Anne somatik komorbidite & bakım-veren yükü** |
| `es_hastalik_*` (14 kategori) | ✗ | ✗ | ✗ | Aile sağlık yükü kovaryatı / negatif kontrol |
| `aile_egp7`, `es_egp7`, `es_siops08`, `aile_siops08` | ✗ | ✗ | ✗ | **EGP sosyal sınıf-gradyanlı ebeveynlik; DRM (eğitim ekseni)** |
| `aile_isei08`, `es_isei08` | SES-latent girdisi | ✗ (yalnız latent) | Tablo 1 | Ayrık prestij vs sınıf ayrıştırması |
| `ev_oda_sayisi`, `cocuk_sayisi`, `arabaniz_var_mi`, `ev_sahipligi` | SES-latent girdisi (`material_index`) | ✗ | Tablo 1 | **Materyal yoksunluk faceti (prestijden ayrık) — indeks HAZIR (§1.5-C3)** |
| `calisma_durumu`, `es_calisma_durumu`, `es_emekli` | `cift_kazanc` girdisi | ✗ | Tablo 1 | **Anne istihdamı × ebeveynlik (§1.6-A)** |
| `egitim_durumu`, `es_egitim_durumu` | `edu_z`/`egitim_fark` girdisi | ✗ | Tablo 1 | **Eğitim homogamisi & eğitim-ekseni DRM (§1.6-B)** |
| `es_sag`, `medeni_durum` | ✗ | ✗ | Tablo 1 | Aile yapısı — **fizibilite: near-constant (§1.5)** |
| `katilimci_cocuk_sirasi`, `kardes_sirasi`, `cocuk_sayisi` | ✗ | ✗ | ✗ | **Doğum sırası & kardeş konstelasyonu** |
| `srq`/`srq_sib` rekabet = **anne/baba kayırma maddeleri** | Rekabet üst-boyutu | §63 concordance | §11.5 | **Doğrudan self-report PDT (favoritism) ayrıştırması (§1.5-C1)** |
| `embu_c_idx_*` vs `embu_c_sib_*` fark | ✗ | §50 trifactor / §52 LDS (anne-çocuk) | ✗ | **PDT-etki modellemesi (concordance değil, etki)** |
| İki kardeşin SRQ raporu (`srq` + `srq_sib`) | H2 APIM | §63 ICC | §11.2 | **Diadik karşılıklılık (reciprocity/mutuality)** |
| `dm_yili`/`cocuk_yas` oranı | ✗ | §66 tanı-yaşı spline | §12.5 | **Yaşam-oranı maruziyet yoğunluğu (DM-only, duyarlılık)** |

**Not — PDT çakışma denetimi:** PDT ana SAP'ta yalnız `|c_idx − c_sib| > 0.5` **eşik/oran** olarak (§Tablo, Buist 2013) ve Faz II §63'te **concordance-ICC** olarak var; CSR'da hipotez-üretici sinyal olarak raporlandı (reddetme: DM ICC=0 vs Kontrol ICC=0,322). **Hiçbiri PDT'yi bir *etki* olarak modellemedi** — yani diferansiyel muamelenin *büyüklüğü* ve *yönü* ne öngörüyor, kardeş ilişkisine (SRQ çatışma/rekabet) etkisi ne? Faz III §96–99 bu boşluğu kapatır ve §63 ile **kasıtlı olarak** iç-tutarlı kalır (aynı yapı, farklı estimand).

---

## 1.5. İSTATİSTİKÇİ FİZİBİLİTE VE VERİ-GERÇEKLİK DENETİMİ *(v0.2 ÇEKİRDEK KATKI)*

> **İlke:** Bir değişkenin kanonik bazda *bulunması* onun *modellenebileceğini* garanti etmez. Aşağıdaki denetim, `FINAL_REFERENCE__analysis_base_family.csv` üzerinde **yalnız agregat frekans** (satır-düzeyi PII dökülmeden) çıkararak her Faz III analizinin gerçek güç/kimliklenebilirlik tavanını sabitler. Kaynak: kanonik CSV üzerinde salt-okunur agregat sorgu (2026-07-08).

### 1.5.1 Şema doğrulaması
v0.1'de adı geçen tüm değişken blokları kanonik bazda **doğrulandı** (family 288 kolon: EMBU-P q01–29, Beck 1–21, EMBU-C indeks q01–29 + kardeş q01–29, SRQ 1–48 + SRQ-kardeş 1–48, ISCO/ISEI/SIOPS/EGP, `anne_hastalik_*`/`es_hastalik_*` 14'er kategori + kategori-sayısı; long 203 kolon). Kilit hash tutarlı. **Uyarı:** 14 hastalık kategorisi vardır (`endokrin, kardiyovaskuler, solunum, gastrointestinal, renal, kas_iskelet, mental, sinir, otoimmun, duyu, hematolojik, dermatolojik, neoplazm, diger`), v0.1 metni "13 kategori" diyordu — düzeltildi.

### 1.5.2 Hücre-sayısı fizibilite tablosu

| Değişken (analiz) | Dağılım (× grup) | Fizibilite kararı |
|---|---|---|
| `anne_hastalik_otoimmun` (§103) | **=1 yalnız 1 aile** (üstelik Kontrol'de), 3 boş | **TEST EDİLEMEZ.** Malcová 2004 (PMID 15532904, tam-metin doğrulı): T1DM birinci-derece akrabalarda T1DM prevalansı anne %2.0 vs %0.5 / baba %4.4 vs %0.8; maternal otoimmün (tiroid vb.) eş-hastalık taban-oranı tek-haneli → n=120 DM'de beklenen birkaç vaka; gözlenen 0 bu düşük taban-oranla tutarlı. Öz-bildirim formu klinik tiroid/çölyak taraması değil → eksik-tespit. |
| `anne_hastalik_mental` (§105) | **=1 yalnız 2 aile** | **Dejenere gösterge.** Üçlü triangülasyondan çıkar; §105 antidepresan×Beck'e iner. |
| `es_sag=0` / `medeni_durum=2` (§107) | dul: **1**; boşanmış: **2** (hepsi DM) | **Moderasyon İMKÂNSIZ.** Tek-ebeveyn n≈3. Betimsel dipnot; moderasyon/kovaryat testi yok. Amato-Keith küçük etki × near-zero alt-grup = tanımsız etkileşim. |
| `anne_hastalik_kategori_sayisi` (§104) | 0:**177**, 1:53, 2:8 (maks 2, %73 sıfır) | "Sürekli yük" **yanıltıcı**; ikili "herhangi komorbidite" (n≈61) olarak modelle; tavan/eksik-tespit uyarısı. |
| `anne_antidepresan` (§105, §1.6) | **=1: 46** (DM 35 / Kontrol 11) | **TEMİZ + GÜÇLÜ SİNYAL.** DM'de %29 vs Kontrol %9 (χ² anlamlı beklenir). Kullanılabilir. |
| `calisma_durumu` (anne istihdamı, §1.6-A) | çalışıyor 152 / hayır 89 (DM 77/43, Kontrol 75/46) | **TEMİZ, DENGELİ, KULLANIMSIZ.** Gruplar arası dengeli → grupla karışmamış moderatör. |
| `es_calisma_durumu` / `es_emekli` | baba çalışıyor 227/14; emekli 4 | **Near-constant** → zayıf değişken; yalnız `cift_kazanc` girdisi. |
| `ev_sahipligi` / `arabaniz_var_mi` (§102) | mülk 131/kira 110; araba yok 125/var 116 (dengeli) | **İYİ VARYANS, DENGELİ.** Materyal facet sağlam (Tier A). |
| `aile_egp7` (§100) | 1:12,2:11,3:23,4:26,5:37,6:43,7:67 (+22 boş) | **FİZİBİL ama grup-karışık.** Sınıf 7: Kontrol 48/DM 19; sınıf 6: DM 31/Kontrol 12 → EGP grupla **ağır confounded** → Simpson riski gerçek. 22 boş (yapısal: emekli/işsiz baba). EGP-3'e daralt. |
| `egitim_durumu` (anne) / `es_egitim_durumu` (baba) | anne 0-5: 13/65/51/68/36/8; baba: 3/65/46/77/44/6 | **6-DÜZEY İYİ DAĞILIM.** Eğitim homogamisi + eğitim-ekseni DRM fizibil (§1.6-B). |
| Doğum sırası / sibship (§108) | `cocuk_sayisi` 2:96,3:88,4:44,…; `katilimci_cocuk_sirasi` 1:102,2:90,3:33,… | **İYİ VARYANS.** Within-family kontrast fizibil. |

### 1.5.3 Yapısal düzeltmeler (dört adet)

**(C1) SRQ kayırma-madde eşlemesi — v0.1 §98 yanlış fonksiyona referans veriyor.**
Kanonik `srq_ho_rivalry_mean` **`srq_higher_order_map()` (R/10)** üzerinden türetilir, `psychval_srq_subscale_map()` (R/06, 9-maddelik psikometri-doğrulama haritası) üzerinden **değil**. Doğru eşleme:
- **Anne kayırma (maternal partiality):** maddeler **14, 30, 46**
- **Baba kayırma (paternal partiality):** maddeler **13, 29, 45**
- **Rekabet (rivalry) üst-boyutu = bu 6 maddenin tamamı** — yani rivalry "içine kayırma gömülü" değil, rivalry **birebir kayırmadır**. Furman-Buhrmester "competition" birinci-düzey ölçeği (maddeler **5, 21, 37**) AYRIDIR ve `conflict` üst-boyutuna girer. §98 bu nedenle "ayrıştırma" değil **iki kanala (anne-vs-baba kayırma) bölme** olarak yeniden çerçevelenir; ayrıca `srq` (indeks çocuk) + `srq_sib` (kardeş) → her iki çocuğun anne-kayırma ve baba-kayırma algısı ayrı ayrı elde.

**(C2) DRM kimliklenebilirliği — v0.1 §101 meslek ekseninde kimliklenemez.**
`aile_egp7 == es_egp7`, `aile_isei08 == es_isei08`, `aile_siops08 == es_siops08` **241/241 birebir aynı** (aile-SES tümüyle baba/eş-türetimli; emekli/işsiz babada yapısal NA). **Ayrı anne mesleki-SES kolonu YOKTUR** (`anne_isei08`/`anne_egp7` mevcut değil; anne meslek serbest metni final CSV'de tutulmaz — bkz. kanonik demografi dokümanı). Sonuç: köken(anne)-vs-varış(baba) meslek-sınıfı DRM **kimliklenemez**. DRM yalnız **eğitim ekseninde** (anne `egitim_durumu` vs baba `es_egitim_durumu`, ikisi de ayrı 6-düzey) çalıştırılabilir. **Ek yorumsal sonuç:** tüm EGP/ISEI-tabanlı SES analizleri fiilen **baba/eş sınıfını** temsil eder; EMBU-P ise **anne** ebeveynliğidir → "baba-sınıfı → anne-ebeveynlik" okuması açıkça yazılır. Anneye-özgü SES = **eğitim (`egitim_durumu`) + istihdam (`calisma_durumu`)** ekseniyle sınırlıdır.

**(C3) SES altyapısı zaten mevcut — v0.1 §102/§101 sıfırdan kurma önerisi gereksiz.**
`R/11_ses_composites.R` hâlihazırda türetir: `material_index` (ev_sahipligi[ters]/ev_oda_sayisi/arabaniz tek-bileşen polychoric PCA), `material_z`, `material_quintile`, `kalabalik_indeksi` (= `cocuk_sayisi/(ev_oda_sayisi+1)`), `egitim_fark` (= `|anne_edu − baba_edu|`, eğitim heterogamisi), `cift_kazanc` (iki ebeveyn de çalışıyor), `max_aile_egitim`, `mean_aile_egitim`, `edu_z`, `isei_z`, `ses_latent`. **Bu nedenle §102 "yeni indeks" değil, `ses_latent`'i facet'lerine (edu_z, isei_z, material_z) ayrıştırıp materyal-z'yi prestij-bloğu üzerine artımsal test etmektir.** ⚠️ **Çift-sayım tuzağı:** `ses_latent` zaten `material_z`'yi içerir → materyal faceti `ses_latent + material_z` olarak DEĞİL, "prestij bloğu (`edu_z + isei_z`) → materyal-z artımı" hiyerarşik kurgusuyla test edilir.

**(C4) R modül numaralandırması — v0.1 §113 çakışıyor.**

### 1.5.4 Fizibiliteye göre yeniden-sınıflandırma (v0.1 Tier'larının revizyonu)

| § | v0.1 Tier | v0.2 revize | Gerekçe |
|---|---|---|---|
| §103 otoimmün diatez | C | **D — test edilemez** | otoimmün n=1; taban-oran ~%2 (Malcová) → yapısal güçsüz; betimsel prevalans + "gelecek çalışma: klinik otoimmün panel" |
| §107 tek-ebeveyn | C | **D — betimsel** | tek-ebeveyn n≈3; moderasyon tanımsız |
| §104 komorbidite yükü | B | **C — ikili yeniden-çerçeve** | %73 sıfır, maks 2 → ikili "herhangi komorbidite"; doz-yanıt zayıf |
| §105 üçlü triangülasyon | B | **B− — iki-gösterge** | mental-kayıt dejenere (n=2); antidepresan×Beck korunur |
| §101 DRM (meslek) | B/C | **D→ eğitim-eksenine taşındı** | meslek-DRM kimliklenemez; eğitim-DRM keşifsel |
| Diğerleri (§96,§97,§98,§100,§102,§108,§109,§110) | — | **korunur** | fizibil (aşağıdaki KISIM'lerde revize güçle) |

### 1.5.5 Tam-metin doğrulama defteri *(v0.3 — OpenAthens + Anna's Reader + EPMC)*

> **Yöntem:** 20 kritik sayısal/yönsel çapa, iki-aşamalı çekişmeli doğrulamayla tam-metinden kontrol edildi (aşama-1: tam-metin çek + değeri çıkar; aşama-2: bağımsız denetçi quote↔değer + plan-iddiası). Kanal önceliği: Anna's Reader (SciDB) → OpenAthens (Millet Kütüphanesi lisanslı) → Europe PMC/Unpaywall (OA). **Sonuç: 14 CONFIRMED · 5 CORRECTED · 1 NOT_FOUND · 0 UNVERIFIED.**

| Künye | Sonuç | Tam-metin bulgusu / düzeltme |
|---|---|---|
| Buist ve ark. 2013 | ✅ CONFIRMED | Diferansiyel muamele→içselleştirme r=.14/dışsallaştırma r=.18; çatışma .27/.28; sıcaklık −.12/−.14 (Table 2). Sıralama + N=12.257 + moderatörler doğrulandı |
| Pinquart 2013 | ✅ CONFIRMED | 7/7 g birebir: ilişki −.16, sıcaklık −.22, talep +.18, aşırı koruma +.39, otoriter +.24, ihmalkâr +.51, otoriter-demokratik −.13 |
| Lovejoy ve ark. 2000 | ✅ CONFIRMED | Magnitüd d=0.40 (negatif) / 0.29 (geri çekilme) / 0.16 (pozitif) — birincil tam-metin erişilemedi, NBK215128 + abstract yön teyidi; işaret konvansiyonu notu |
| Amato & Keith 1991 | ✅ CONFIRMED | Boşanma meta; alan-özgü küçük d (baba-çocuk ilişkisi d=−.26, medyan .14); "baba yokluğu" ayrı literatür değil, boşanma domaini |
| Malcová ve ark. 2004 | ✅ CONFIRMED | 5/5: anne T1DM %2.0 vs %0.5, baba %4.4 vs %0.8, tiroid çocuk %10 vs %1.9; "otoimmün" etiketi hafif genelleme (spesifik T1DM/tiroid) |
| Rogosa & Willett 1983 | ✅ CONFIRMED | Fark-skoru güvenilirlik formülü + yüksek ρ_XY → düşük ρ_DD ilkesi doğrulandı |
| Kowal & Kramer 1997 | ✅ CONFIRMED | Çocukların çoğu PDT'yi meşru algılar; meşru algılananın olumsuz etkisi yok |
| McHale ve ark. 2000 | ✅ CONFIRMED | N=385; adalet algısı, PDT büyüklüğünden daha tutarlı biçimde iyi-oluş/kardeş-pozitifliğiyle ilişkili |
| Edwards & Parry 1993 | ✅ CONFIRMED | Fark-skoru yerine polinom regresyon; kısıt dayatma yasağı doğrulandı |
| Laird & De Los Reyes 2013 | ✅ CONFIRMED | Informant fark-skoru → polinom regresyon önerisi doğrulandı |
| Van Gampelaere ve ark. 2020 | ✅ CONFIRMED | Yalnız anneler↑distres (stres/depresyon/kaygı); her iki ebeveyn↓duyarlılık; yalnız babalar↓korumacılık; suboptimal glisemik kontrol→↑maternal distres |
| Ganzeboom & Treiman 1996 | ✅ CONFIRMED | ISEI eğitim+meslekte en verimli; **gelirde üç ölçü ~eşit** (nüans eklendi) |
| Downey 1995 | ✅ CONFIRMED | Resource dilution: sibship↑→kaynak↓→başarı↓; kaynak kontrolüyle etki sıfıra/yarıya iner (Table 3) |
| Coldwell, Pike & Dunn 2008 | ✅ CONFIRMED | Fark skorları favoritizm skorlarından daha güçlü yordayıcı |
| **Eradus ve ark. 2024** | 🔧 CORRECTED | Değerler doğrulandı (düşmanlık r=.176 > sıcaklık r=.122); üstünlük **birincil analizde anlamlı** (F=6.618, p=.011), duyarlılıkta marjinal (p=.052) — "anlamsız" deme |
| **McHale & Pawletko 1992** | 🔧 CORRECTED (high) | PDT engelli-bağlamda↑ (doğru); ama "buffering/zayıf-bağ" YANLIŞ — bağlam-bağımlı/ters ilişki; buffering çapası Kowal-Kramer'a taşındı |
| **Sharpe & Rossiter 2002** | 🔧 CORRECTED (high) | Tekil "d≈0.28" yok; içe-yönelim d≈0.41, dışa-yönelim d≈0.15 (PMID 35950954); 0.28 ortalama |
| **Prikken ve ark. 2019** | 🔧 CORRECTED (high) | Operatif mediyatör **psikolojik kontrol**, aşırı koruma DEĞİL; dolaylı etki anne .107/baba .061 |
| **Rohrer ve ark. 2015** | 🔧 CORRECTED | "r<0.02" makalede yok (F/P raporlar); zekâ avantajı hem objektif IQ hem öz-bildirimde (~%10 SD/basamak) |
| **Conger ve ark. 2010** | ⛔ NOT_FOUND | Narratif decade-review; standardize β nokta-değeri yok → β≈.20-.40 atfı kaldırıldı |

**Doğrulama sonucu — üç yorumsal etki:** (1) §99 buffering hipotezi McHale-Pawletko'ya değil algılanan-adalet mekanizmasına (Kowal-Kramer/McHale 2000) dayanmalı. (2) §110 aşırı-koruma odağı ihtiyatlı: Prikken'de T1DM klinik çıktısının operatif mediyatörü psikolojik kontroldür. (3) SESOI |r|≈.10 ampirik olarak sağlam — PDT etkileri tam-metin doğrulı r≈.08–.18 aralığında (Eradus/Buist), |r|≈.10 alt-orta banda oturur.

---

## 1.6. YENİ ANALİZ YÜZEYLERİ — Planın Atladığı, Veride Hazır *(v0.2)*

Aşağıdaki dört yüzey `FINAL_REFERENCE__*` içinde hazır, literatürde merkezî, v0.1'de yok:

**(A) Anne istihdamı × ebeveynlik.** `calisma_durumu` (temiz, dengeli, n=152/89) tek başına — `cift_kazanc` girdisi olmanın ötesinde — moderatör olarak kullanılmadı. Anne istihdamı prestij-SES'ten ayrık bir zaman/rol/özerklik boyutudur. Model: `EMBU_P ~ calisma_durumu + ses_latent_z + grup` ve EMBU-C long lme4. **Tier B.** *(Not: baba istihdamı near-constant → yalnız `cift_kazanc` üzerinden.)*

**(B) Eğitim homogamisi & eğitim-ekseni DRM.** `egitim_fark` (=|anne_edu − baba_edu|) HAZIR. (i) Homogami ana etkisi: eğitim uyumsuzluğu → EMBU/Beck. (ii) **Eğitim-ekseni DRM (§101 kurtarması):** `gnm` ile anne-eğitim (köken) × baba-eğitim (varış) → EMBU-C/SRQ; salience ağırlığı w. n=241'de 6×6 seyrek → eğitimi **3-düzeye** (düşük/orta/yüksek) daralt; keşifsel + geniş CI. **Tier B/C.**

**(C) SIOPS vs ISEI vs EGP üçlü ölçüm-yarışı.** Ganzeboom-Treiman (1996): ISEI çıktı-öngörüsünde en verimli tekil gösterge, SIOPS prestij-algısını, EGP ilişkisel-sınıfı yakalar. `es_siops08`/`aile_siops08` hiç kullanılmadı. Aynı EMBU çıktısında üçünü **commonality analizi + AIC** ile yarıştır: ebeveynlikte prestij mi (ISEI/SIOPS) yoksa ilişkisel sınıf mı (EGP) ek varyans açıklıyor? Kohn-Goldthorpe teorik sorusunun doğrudan testi. **Tier B (keşifsel).**

**(D) Beck-aracı Aile-Stres-Modeli (FSM) — en güçlü plan-uyumlu ek.** Conger FSM: ekonomik baskı → ebeveyn distresi → sıcaklık↓/sertlik↑. Verideki **Beck çıktısı bu zinciri doğrudan test etmeyi sağlar:** `materyal yoksunluk (material_z, ters) → beck_total → EMBU_P` (lavaan + BCa bootstrap; VanderWeele mediator-outcome confounder duyarlılığı). **Not (§1.5.5 doğrulama):** Conger, Conger & Martin (2010) bir *narratif decade-review*'dur ve zinciri (ekonomik zorluk→baskı→ebeveyn distresi→çatışma→bozulan ebeveynlik→çocuk uyumsuzluğu) yalnız niteliksel tanımlar; **standardize β nokta-değeri raporlamaz** → plan bu kaynaktan sayısal yol büyüklüğü iddia etmez; büyüklük beklentisi (küçük-orta) orijinal ampirik FSM-SEM çalışmalarına aittir ve bu tezin kendi kestirimiyle raporlanır. Bu, §102 (materyal facet) ile §104 (distres yolu) arasındaki köprüdür. **Tier A/B.**

**(E) Diğer küçük ama veride-hazır etkileşimler:** `same_sex` × PDT (§109 uzantısı; Kim-McHale 2006 same/mixed-sex kanıtı), `age_gap` non-lineer (spline/kuadratik) kardeş yakınlık-çatışması (§108/§109).

---

## 2. FAZ III İÇİNDEKİLER (v0.2)

**KISIM XXXVI — DİFERANSİYEL EBEVEYNLİK ETKİ MODELLEMESİ**
- 96. PDT büyüklüğü & yönü: işaretli/mutlak algı-farkı skoru (**ρ_DD güvenilirlik + RSA**)
- 97. PDT → Kardeş İlişkisi yol modeli (Buist/Eradus çerçevesi, aile-clustered/APIM)
- 98. SRQ-gömülü doğrudan kayırma: anne-vs-baba kanal + **MTMM/Operations-Triad** iki-informant uyumu
- 99. Meşruiyet/bağlam moderasyonu: PDT × Grup + **algılanan adalet aracı** (Kowal-Kramer); **TOST buffering**

**KISIM XXXVII — SOSYAL TABAKALAŞMA GENİŞLETMESİ**
- 100. EGP sosyal sınıf-gradyanlı ebeveynlik (EGP-3 → EMBU-P/C) + **SIOPS/ISEI/EGP yarışı (§1.6-C)**
- 101. **Eğitim-ekseni** Diagonal Reference Model (meslek-DRM kimliklenemez → §1.5-C2)
- 102. Materyal yoksunluk faceti (**mevcut `material_z` ayrıştırması**) + **Beck-aracı FSM (§1.6-D)**
- 102b. **Anne istihdamı × ebeveynlik (§1.6-A)** — yeni

**KISIM XXXVIII — ANNE SOMATİK KOMORBİDİTE VE AİLE SAĞLIK YÜKÜ**
- 103. Anne otoimmün komorbidite — **betimsel prevalans (test edilemez, §1.5)**
- 104. Anne komorbidite (**ikili**) → bakım-veren yükü → ebeveynlik/Beck
- 105. **İki-gösterge** maternal-distres (antidepresan × Beck; mental-kayıt dejenere)
- 106. Eş/baba & aile sağlık yükü kovaryatı + negatif-kontrol maruziyeti

**KISIM XXXIX — AİLE YAPISI VE KARDEŞ KONSTELASYONU**
- 107. Baba yokluğu / tek-ebeveyn — **betimsel (n≈3, §1.5)**
- 108. Doğum sırası & kardeş konstelasyonu → algılanan ebeveynlik (within-family)
- 109. Kardeş SRQ diadik karşılıklılığı (reciprocity/mutuality) + `same_sex`/`age_gap` uzantısı

**KISIM XL — DM-SPESİFİK MARUZİYET YOĞUNLUĞU (DM-only, ağır kısıtlı)**
- 110. Yaşam-oranı maruziyet (`dm_yili`/`cocuk_yas`) × aşırı koruma — **duyarlılık katmanı (metrik doğrulanmamış, §1.5/EK)**
- 111. Tanı gelişim-penceresi × kardeş maruziyeti (tasarım-sinyali eskizi)

**KISIM XLI — DİSİPLİN, YENİDEN-ÜRETİLEBİLİRLİK, RAPORLAMA**
- 112. OSF Layer 4 & Tip 3 sapma satırı
- 113. Yeni R modülleri (**R/51+**, düzeltildi) + `_targets.R` entegrasyonu + test/audit
- 114. Öncelik kademeleri (Tier A/B/C/D) & fizibilite-güç dürüstlük notu
- 115. Tedbir-ve-hatalar aktif denetim listesi (Faz III'e özel)
- EK — **Evidentia ile varlık-doğrulı literatür çapaları** (referans-kapısı tam-metin doğrulaması bekliyor)

---

# KISIM XXXVI — DİFERANSİYEL EBEVEYNLİK ETKİ MODELLEMESİ

> **Literatür bağlamı (tam-metin doğrulı — §1.5.5):** Kardeş diferansiyel muamelesi (parental differential treatment, PDT) ebeveynlik literatürünün en sağlam bulgularından biridir; etki büyüklükleri **tutarlı biçimde küçüktür** ve **algılanan adalet/meşruiyet** ile modere olur. İki meta-analiz yakınsar:
> - **Eradus, Leijten, Melendez-Torres, Foo & Oliver (2024)**, *J Fam Psychol* 38(3):387–399, DOI 10.1037/fam0001194 (PMID 38271066) — 215 ES / 13 örneklem / 19 yayın. **Tam-metin doğrulı havuzlanmış r:** göreli PDT genel r=.141 [.077, .205]; diferansiyel *sıcaklık* r=.122 [.055, .190]; diferansiyel *düşmanlık* r=.176 [.106, .244]; *içselleştirme* r=.084 [.016, .151] (ihmal edilebilir); *dışsallaştırma* r=.183 [.117, .248] (içselleştirmenin >2 katı). Düşmanlık, sıcaklıktan **birincil analizde anlamlı biçimde güçlü** (F(1,213)=6.618, p=.011; yalnız aykırı-değer düzeltilmiş duyarlılıkta marjinale iner, p=.052).
> - **Buist, Deković & Prinzie (2013)**, *Clin Psychol Rev* 33(1):97–106, DOI 10.1016/j.cpr.2012.10.007 (PMID 23159327) — 34 çalışma, N=12.257, 85 ES. **Tam-metin doğrulı ESr (Table 2):** diferansiyel muamele → içselleştirme r=.14***, dışsallaştırma r=.18***; sıcaklık → −.12**/−.14***; çatışma → .27***/.28***. Sıralama **çatışma (orta) > sıcaklık ≈ diferansiyel muamele (küçük)**. Moderatörler (yalnız içselleştirme yolları): erkek-çift oranı↑ (β=.68, p<.05), yaş farkı↓ (β=−.72, p<.05), gelişimsel dönem (Q=13.82, p<.001: çocuklar r=.22 vs ergenler r=.08).
>
> **Kronik hastalık = meşrulaştırıcı bağlam** kanıtı — DÜZELTİLMİŞ okuma (§1.5.5): **McHale & Pawletko (1992)**, *Child Dev* 63(1):68–81, DOI 10.2307/1130902 — engelli-kardeş bağlamında PDT'nin **DAHA YÜKSEK** olduğu doğrulandı (context×status: yardım F(1,60)=17.27, disiplin F(3,58)=5.40; engelli çocuk daha çok negatif-sevgi/güç, daha az pozitif-sevgi). ⚠️ Ancak makale PDT-uyum bağının *zayıfladığını* (buffering/de-identifikasyon) **bulmaz**; bunun yerine muamelenin **bağlam-bağımlı, hatta ters** anlamını gösterir (ör. pozitif sevgi engelli-kardeş çocukta DAHA ÇOK anksiyeteyle, karşılaştırma çocuğunda DAHA AZ ile ilişkili, F(7,54)=7.02, p<.01). Yani T1DM "buffering" hipotezi bu çalışmayla değil, **algılanan-adalet mekanizmasıyla** (aşağıda Kowal-Kramer, McHale 2000) çapalanmalıdır. + **Quittner & Opipari (1994)**, *Child Dev* 65(3):800–814, DOI 10.2307/1131419 (kistik fibroz). **Kronik-hastalıklı kardeş uyum riski** çapası: **Sharpe & Rossiter (2002)**, *J Pediatr Psychol* 27(8):699–710, DOI 10.1093/jpepsy/27.8.699 — DÜZELTME (§1.5.5): tekil "d≈0.28" raporlanmaz; alan-özgü **içe-yönelim d≈0.41, dışa-yönelim d≈0.15** (kaynak: 2023 güncelleme meta-analizi PMID 35950954; 0.28 bu ikisinin aritmetik ortalaması).

## 96. PDT büyüklüğü & yönü — algı-farkı skoru

**96.1 Boşluk.** §63 concordance-ICC "iki çocuk ne kadar benzer algılıyor" der; ama diferansiyel muamelenin **büyüklüğü** (`|Δ|`) ve **yönü** (işaretli Δ = kim daha sıcak/daha reddedilmiş algılıyor) ne bir sonuç ne de bir yordayıcı olarak modellenmedi.

**96.2 Yöntem.**
- Aile düzeyinde, her EMBU-C alt ölçeği için: `pdt_signed = embu_c_idx_mean − embu_c_sib_mean`; `pdt_abs = |pdt_signed|`.
- **Fark-skoru güvenilirlik uyarısı — SOMUTLAŞTIRILDI (v0.2).** Klasik test kuramında (Lord–Novick; **Rogosa & Willett, 1983**, *J Educ Meas* 20(4):335–343, DOI 10.1111/j.1745-3984.1983.tb00211.x; köken **Overall & Woodward, 1975**, DOI 10.1037/h0076158) D = X − Y için:

  ρ_DD = (σ²_X·ρ_XX + σ²_Y·ρ_YY − 2·ρ_XY·σ_X·σ_Y) / (σ²_X + σ²_Y − 2·ρ_XY·σ_X·σ_Y)

  Eşit varyansta (σ_X≈σ_Y) sadeleşir: **ρ_DD = [(ρ_XX + ρ_YY)/2 − ρ_XY] / (1 − ρ_XY)**.
  Burada X = indeks, Y = kardeş EMBU-C algısı; ρ_XY = kardeşler-arası algı korelasyonu. Diferansiyel-ebeveynlik olgusunun doğası gereği kardeşler benzer algılar (ρ_XY yüksek) → fark neredeyse güvenilmez olabilir: ρ_XX=ρ_YY=.80, ρ_XY=.60 → **ρ_DD=.50**; ρ_XY=.75 → **ρ_DD=.20**. **Zorunlu:** gözlenen ρ_XY (§63 ICC'den) + hesaplanan ρ_DD her alt ölçek için raporlanır; ρ_DD düşükse ham-fark yalnız betimsel, çıkarım disattenüe/latent modele taşınır.
- **Birincil model — RSA/polinom (LDS DEĞİL, v0.2 kararı).** Fark skorunu bağımlı/bağımsız değişken olarak dayatmak yerine iki bileşeni (X, Y) ayrı prediktör tutan **polinom regresyon + yüzey-tepki analizi (RSA)** (Edwards & Parry, 1993, *AMJ* 36(6):1577, DOI 10.2307/256822; Edwards, 2001 "Ten Difference Score Myths", *ORM* 4(3):265, DOI 10.1177/109442810143005; informant-farkı bağlamında birebir uygulama: **Laird & De Los Reyes, 2013**, *J Abnorm Child Psychol* 41(1):1–14, DOI 10.1007/s10802-012-9659-y). **LDS elenir** çünkü McArdle latent-fark (2009, *Annu Rev Psychol* 60:577, DOI 10.1146/annurev.psych.60.110707.163612) **boylamsal değişim** içindir; bizim pdt tek-zamanlı, kardeş-arası **kesitsel** discrepancy'dir. n=241 → 5 terim (X, Y, X², XY, Y²) + kesişim = 6 parametre; ~40 gözlem/parametre → yeterli. Yüzey parametreleri **a1–a4 bootstrap %95 GA** ile; blok-anlamlılık testi. Ölçüm-hatası düzeltmesi latent-polinom (Edwards 2007, DOI 10.1177/1094428107308920) **duyarlılık** katmanı (n=241 çok-göstergede sınırda). ⚠️ **Trafimow (2015)** (DOI 10.1080/23311835.2015.1064626) nüansı dipnotlanır: düşük ρ_DD her bağlamda güçsüzlük demek değildir.
- **Yordayıcı olarak:** `pdt_abs ~ group_f + ses_latent_z + age_gap_z + same_sex + cocuk_sayisi_z` (aile-düzeyi OLS + robust SE). "DM ailelerinde diferansiyel algı daha büyük mü?"
- **Yön analizi:** DM grubunda hasta çocuk (indeks) mı daha çok sıcaklık/koruma algılıyor? → işaretli Δ'nın grup-içi işaret testi + %95 GA.

**96.3 Çıktı.** 4 alt ölçek × (RSA yüzeyi + büyüklük modeli + yön testi); ρ_DD tablosu; etki büyüklüğü (Cohen's d fark, %95 GA) + forest. **Tier A.**

**96.4 Tedbir.** Çoklu karşılaştırma (4 alt ölçek × 2 estimand) → Holm; ortalama+medyan; ρ_DD dipnotu; korelasyonel dil. **SESOI:** iki meta-analiz PDT etkilerini küçük gösterdiği için "diferansiyel etki yok/kardeşler uyumlu" gibi null iddialar için **önceden-kayıtlı eşdeğerlik sınırı |r|≈.10 (≈ d 0.20)** ile TOST (Lakens, 2017, DOI 10.1177/1948550617697177; Lakens, Scheel & Isager, 2018, DOI 10.1177/2515245918770963).

## 97. PDT → Kardeş İlişkisi yol modeli

**97.1 Yöntem.** `srq_ho_conflict_mean` ve `srq_ho_rivalry_mean` (indeks + kardeş, long) sonuç; `pdt_abs` (RSA-tercihli, latent duyarlılık) yordayıcı; aile-clustered (lme4 random intercept `aile_no_f`) veya lavaan aile-düzeyi. Kovaryatlar: SES, yaş farkı, aynı cinsiyet, grup.
- Hipotez yönü (literatür): daha büyük diferansiyel muamele → daha yüksek çatışma/rekabet, daha düşük sıcaklık (Buist 2013; Eradus 2024).
- **Güçlendirme (v0.2):** "sibling barricade"/sosyal karşılaştırma çerçevesi (**Feinberg et al., 2000**, *Child Dev* 71(6):1611, DOI 10.1111/1467-8624.00252) — her iki çocuğun sonucunu her iki çocuğun muamelesiyle modelleyen **APIM/dyadik** kurulum (H2 `R/17` APIM altyapısı yeniden kullanılır). Dyadik ebeveyn-çocuk ilişkisi kontrol edilmeli (**Shanahan et al., 2008**, *J Marriage Fam* 70(2):480, DOI 10.1111/j.1741-3737.2008.00495.x). Mekanizma modeli (moderated indirect): **Loeser, Whiteman & McHale, 2016**, *J Child Fam Stud* 25, DOI 10.1007/s10826-016-0429-2.

**97.2 Çıktı.** Standartlaştırılmış yol katsayıları + %95 GA; aile-içi ICC raporu; APIM aktör/partner tablosu. **Tier A.**

**97.3 Tedbir.** Kesitsel → "öngörüyor" değil "ilişkili"; ters-nedensellik (kötü kardeş ilişkisi → diferansiyel algı) açıkça tartışılır; koşullu bağımlılık ≠ nedensellik.

## 98. Doğrudan kayırma (favoritism) — anne-vs-baba kanal + iki-informant üçgenleme

**98.1 Boşluk (v0.2 düzeltmesiyle).** §1.5-C1: kanonik `srq_ho_rivalry_mean` **birebir** anne-kayırma (14,30,46) + baba-kayırma (13,29,45) maddelerinin ortalamasıdır — yani doğrudan, iki-informantlı, self-report bir PDT ölçütü veride mevcut ama **anne-vs-baba kanalları ve iki-çocuk perspektifi ayrıştırılmadı**.

**98.2 Yöntem.**
- **İki kanal:** `mat_partiality = mean(srq_14,30,46)`, `pat_partiality = mean(srq_13,29,45)` — hem `srq` (indeks) hem `srq_sib` (kardeş) için (madde eşlemesi `srq_first_order_map()`/`srq_higher_order_map()` ile doğrulanır — **R/06 değil R/10**).
- İki çocuğun kayırma algısı uyumu: her kanal için ICC(2,1) + Bland-Altman (H5/`R/20` altyapısı).
- Grup + yön: DM'de hasta çocuk lehine kayırma algısı yükseliyor mu? (işaretli).
- **Çapraz-yöntem üçgenleme (MTMM/Operations-Triad):** self-report kayırma (SRQ, yöntem-2) ↔ türetilmiş algı-farkı (§96 EMBU-C, yöntem-1) aynı trait'i (diferansiyel ebeveynlik) ölçen iki işlemci. **Campbell & Fiske (1959)** MTMM (DOI 10.1037/h0046016) + **De Los Reyes et al. (2013) Operations Triad** (*Annu Rev Clin Psychol* 9:123, DOI 10.1146/annurev-clinpsy-050212-185617): converging (korele + aynı yön) → sağlam ortak yapı; **diverging (sistematik ayrışır ama her ikisi yorumlanabilir) → ÖLÇÜM HATASI DEĞİL**, geçerli vantaj-noktası farkı (çocuğun algıladığı vs annenin bildirdiği kayırma farklı gerçeklikler); compensating → ortak-yöntem yanlılığı. Yakınsama κ/ICC + RSA yön-uyumuyla ampirik test edilir; ayrışma otomatik "hata" ilan edilmez.

**98.3 Çıktı.** Anne/baba kayırma-alt-skoru betimsel + grup + iki-informant uyum tablosu + EMBU-C-PDT ile yakınsama (MTMM) matrisi. **Tier A** (veride hazır, literatürde merkezî).

**98.4 Tedbir.** Her kanal yalnız **3 madde** → düşük güvenilirlik; yeni alt-skorların ω'sı ayrıca raporlanır, yorum ihtiyatlı (Coldwell, Pike & Dunn, 2008, DOI 10.1111/j.1467-9507.2007.00440.x: fark skorları favoritizm skorlarından daha güçlü yordayıcı — yön kararı ampirik).

## 99. Meşruiyet/bağlam moderasyonu — PDT × Grup + algılanan adalet

**99.1 Boşluk & mantık.** Kowal-Kramer geleneği: diferansiyel muamele *meşru/adil* algılandığında kardeş ilişkisine zararı azalır (**Kowal & Kramer, 1997**, *Child Dev* 68(1):113, DOI 10.2307/1131929; **Kowal, Kramer, Krull & Crick, 2002**, *J Fam Psychol* 16(3):297, DOI 10.1037/0893-3200.16.3.297; **McHale et al., 2000**, *Soc Dev* 9(2):149, DOI 10.1111/1467-9507.00117 — iyi-oluşu yordayan PDT *miktarı* değil algılanan *adalet*tir). **T1DM, hasta çocuğa yönelik farklı muameleyi meşrulaştıran bir bağlam olabilir** (buffering çapası: yukarıdaki adalet-mekanizması; Solmeyer & McHale, 2015, DOI 10.1111/famp.12166). ⚠️ **Doğrulama notu (§1.5.5):** McHale-Pawletko (1992) buffering'i (uyum-bağının zayıflaması) DEĞİL, muamelenin bağlam-bağımlı/ters anlamını gösterir → bu öngörü onunla değil algılanan-adalet geleneğiyle temellenir; kronik-bağlamda PDT'nin *yükseldiği* kısmı McHale-Pawletko'dan alınır. Öngörü: PDT→çatışma yolu **DM grubunda daha zayıf** (buffering) — ancak ters yön (bağlam PDT'nin anlamını değiştirir/güçlendirir) de eşit-olası ve TOST/etkileşim ile ayrık test edilir.

**99.2 Yöntem.** §97 modeline `pdt_abs × group_f` etkileşimi; basit-eğim DM vs Kontrol; emmeans grup-içi yol.
- **KRİTİK KISIT (v0.2).** Literatür buffering'in *proksimal* mekanizmasının **algılanan adalet** olduğunu, hastalık-statüsünün yalnız *distal* proxy olduğunu gösterir. Kanonik formda **ayrık "adil mi?" maddesi YOKTUR** (form kontrolüyle doğrulandı) → meşruiyet yalnız hastalık-bağlamı proxy'siyle temsil edilir; bu, mekanizma testinin değil **yalnız moderasyon-varlığı** testinin yapılabildiği anlamına gelir ve açıkça sınırlama olarak yazılır. (Not: SRQ kayırma-algısı §98 buffering'in kısmi proxy'si olabilir — keşifsel.)

**99.3 Çıktı.** Etkileşim katsayısı + %95 GA + basit-eğim grafiği. **Tier B.**

**99.4 Tedbir.** Etkileşim testleri düşük güçlü → **simr güç karakterizasyonu + SESOI-temelli TOST** (|r|≈.10) zorunlu: "buffering = zarar yok" iddiası null-anlamsızlıkla DEĞİL, önceden-kayıtlı eşdeğerlik sınırıyla kanıtlanır. "Meşruiyet" yorumu spekülatif etiketiyle; adalet-maddesi yokluğu açık sınırlama.

---

# KISIM XXXVII — SOSYAL TABAKALAŞMA GENİŞLETMESİ

> **Literatür bağlamı (Evidentia-doğrulı):** Sosyal sınıf ↔ ebeveynlik prestij-puanına indirgenemez; **sınıf konumu** niteliksel farklı ebeveynlik örüntüleriyle ilişkilidir. Çapalar: **Kohn (1963)**, *AJS* 68(4), DOI 10.1086/223403 + **Kohn & Schooler (1969)**, *ASR* 34(5):659, DOI 10.2307/2092303 (sınıf → mesleki-koşullar → öz-yönelim/itaat değerleri); **Conger, Conger & Martin (2010)**, *JMF* 72(3):685, DOI 10.1111/j.1741-3737.2010.00725.x (Family Stress Model kanonik derleme); **Bradley & Corwyn (2002)**, *Annu Rev Psychol* 53:371, DOI 10.1146/annurev.psych.53.100901.135233 (SES çok-boyutlu); **Erikson, Goldthorpe & Portocarero (1979)**, *BJS* 30(4):415, DOI 10.2307/589632 (EGP şeması); **Ganzeboom, De Graaf & Treiman (1992)**, *Soc Sci Res* 21(1):1, DOI 10.1016/0049-089x(92)90017-b (ISEI) + **Ganzeboom & Treiman (1996)**, *Soc Sci Res* 25(3):201, DOI 10.1006/ssre.1996.0010 (ISEI vs SIOPS vs EGP crosswalk; tam-metin doğrulı: ISEI eğitim+meslek çıktısında en verimli — meslek-statü aktarımı adj R² SIOPS .342/ISEI .382/EGP .333 — ama **gelir** öngörüsünde üçü yaklaşık eşit .20 civarı, §1.5.5); **Sobel (1981)**, *ASR* 46(6):893, DOI 10.2307/2095086 (+ 1985, DOI 10.2307/2095383) ve **van der Waal, Daenekindt & de Koster (2017)**, *Int J Public Health* 62(9), DOI 10.1007/s00038-017-1018-x (DRM); **Evans (2004)**, *Am Psychol* 59(2):77, DOI 10.1037/0003-066x.59.2.77 (+ Evans & English, 2002, DOI 10.1111/1467-8624.00469 — crowding, prestijden ayrık facet); **Hoff & Laursen (2019)**, *Handbook of Parenting* 3. bs., DOI 10.4324/9780429401459-13 (Hoff-Laursen-Tardif 2002 güncellemesi).

## 100. EGP sosyal sınıf-gradyanlı ebeveynlik + ölçüm-yarışı

**100.1 Yöntem.** `aile_egp7` → **EGP-3'e** (hizmet 1-2 / ara 3-5 / işçi-rutin 6-7; n dağılımı §1.5 önceden raporlandı). Sonuç: EMBU-P (anne) aile-düzeyi OLS + EMBU-C (çocuk) long lme4; sınıf faktörü + yaş/cinsiyet kovaryatı. **Yorumsal uyarı (§1.5-C2):** `aile_egp7 = es_egp7` (baba sınıfı) → "baba-sınıfı → anne-ebeveynlik" okuması.
- **Ölçüm-yarışı (§1.6-C).** ISEI (sürekli), SIOPS (prestij), EGP-3 (ilişkisel) aynı EMBU çıktısında **commonality + AIC** ile yarıştırılır. Literatür beklentisi (Ganzeboom-Treiman): ISEI en verimli özet; EGP yalnız doğrusal-olmayan eşik kırılmaları varsa ek varyans. 7-kategori df-maliyeti n=241'de yüksek → EGP-3.

**100.2 Çıktı.** Sınıf-gradyanı (emmeans marjinal ortalama + %95 GA) + ISEI-vs-SIOPS-vs-EGP inkremental R²/AIC tablosu. **Tier B.**

**100.3 Tedbir.** **Simpson denetimi zorunlu** — EGP grupla ağır confounded (§1.5: sınıf-7 Kontrol-ağırlıklı, sınıf-6 DM-ağırlıklı); grup-içi + havuzlanmış ayrı raporlanır. 22 boş (yapısal, emekli/işsiz baba) → eksik-veri notu. Sınıf etiketleri betimsel; ekolojik yanılgı.

## 101. Eğitim-ekseni Diagonal Reference Model (meslek-DRM kimliklenemez)

**101.1 Yöntem (v0.2 yeniden-çerçeve).** §1.5-C2: `aile_isei08/egp7 = es_isei08/egp7` (241/241) + ayrı anne-mesleği yok → **meslek-DRM kimliklenemez**. DRM yalnız **eğitim ekseninde**: `gnm` ile anne (`egitim_durumu`, köken) ve baba (`es_egitim_durumu`, varış) → çocuk çıktısı (EMBU-C/SRQ); köken-ağırlık (salience) parametresi w. "Ebeveynlik daha çok anne mi baba eğitim konumuna mı bağlı?" + homogami (`egitim_fark`) ana etkisi.

**101.2 Çıktı.** DRM ağırlık w (%95 GA) + sapma testi. **Tier C** (keşifsel). ⚠️ **n=241 bir 6×6 DRM için ciddi yetersiz** — başarılı uygulamalar binlerle çalışır (ör. TILDA ~8.000, McLoughlin et al. 2022, DOI 10.1093/geronb/gbac122). Eğitimi **3-düzeye** daralt (3 köşegen hücre); w'nin CI'si geniş olacak.

**101.3 Tedbir.** DRM güç-yoğun; yakınsama/kimliklenebilirlik denetimi zorunlu; yakınsamazsa kategorik interaksiyon fallback + "gelecek çalışma" etiketi.

## 102. Materyal yoksunluk faceti + Beck-aracı FSM

**102.1 Mantık (v0.2 düzeltmesiyle).** §1.5-C3: `material_index`/`material_z`/`kalabalik_indeksi` ZATEN mevcut (`R/11`). §102 = `ses_latent`'i facet'lerine ayrıştırıp materyal-z'yi **prestij bloğu üzerine artımsal** test etmek — Conger FSM'de materyal koşullar ebeveynliğe prestij-değer yolundan *farklı* bir yoldan (ekonomik baskı → distres → sıcaklık↓/reddetme↑) bağlanır (Evans).

**102.2 Yöntem.**
- **Hiyerarşik regresyon (çift-sayım kaçınarak):** blok-1 = prestij bloğu (`edu_z + isei_z`), blok-2 = `material_z` (deprivation = −material_z) → EMBU/Beck. `ses_latent`'i blok-1'de KULLANMA (material_z'yi zaten içerir).
- **Beck-aracı FSM (§1.6-D) — en güçlü ek:** `−material_z → beck_total → EMBU_P` (lavaan + BCa bootstrap; VanderWeele mediator-outcome confounder duyarlılığı, `R/23`/`R/41` altyapısı). Yol büyüklüğü küçük-orta beklenir; Conger 2010 zinciri niteliksel tanımlar (nokta-katsayı yok, §1.5.5) → sayısal β bu kaynaktan iddia edilmez.

**102.3 Çıktı.** İnkremental ΔR² + katsayı tablosu + FSM yol diyagramı (dolaylı etki %95 BCa GA). **Tier A.**

**102.4 Tedbir.** Kalabalıklık↔prestij yüksek kolinearite → **VIF raporu**; iki facet'i "aynı şey" saymama; `kalabalik_indeksi` mevcut formül (`cocuk_sayisi/(ev_oda_sayisi+1)`) korunur (v0.1'in yetişkin-eklemeli alternatifi değil — iç-tutarlılık).

## 102b. Anne istihdamı × ebeveynlik *(yeni, §1.6-A)*

**102b.1 Yöntem.** `calisma_durumu` (temiz, dengeli, n=152/89) moderatör: `EMBU_P ~ calisma_durumu * grup + ses_latent_z + anne_yas_z` (aile-düzeyi) ve EMBU-C long lme4. Anne istihdamı prestijden ayrık zaman/rol/özerklik boyutu (Kohn öz-yönelim geleneğiyle bağlanır).

**102b.2 Çıktı.** İstihdam ana etkisi + etkileşim + %95 GA. **Tier B.**

**102b.3 Tedbir.** Baba istihdamı near-constant → yalnız `cift_kazanc`; korelasyonel dil.

---

# KISIM XXXVIII — ANNE SOMATİK KOMORBİDİTE VE AİLE SAĞLIK YÜKÜ

> **Literatür bağlamı (Evidentia-doğrulı):** (a) Bakım-veren yükü/kronik ebeveyn hastalığı ebeveynlik davranışını etkiler — **Pearlin, Mullan, Semple & Skaff (1990)**, *Gerontologist* 30(5):583, PMID 2276631 (stres-süreç modeli); pediatrik meta-nicelleme **Pinquart (2018)**, *Stress Health* 34(2):197, PMID 28834111 (düşük ebeveyn ruh sağlığı = ebeveynlik stresinin en güçlü korelatı); Türk validasyonu **Demirtepe-Saygılı & Bozo (2011)**, *Psychol Health* 26(5):585, PMID 21038170. (b) **Paylaşılan otoimmün diatez:** **Malcová et al. (2004)**, *Cas Lek Cesk* 143(9):625, PMID 15532904 — T1DM annede otoimmün %2.0 vs %0.5, tiroid çocukta %10 vs %1.9. (c) Maternal depresyon→ebeveynlik meta: **Lovejoy, Graczyk, O'Hare & Neuman (2000)**, *Clin Psychol Rev* 20(5):561, PMID 10860167 (negatif davranış > geri çekilme > pozitif-zayıf; öz-bildirim ≈ tanı → **Beck→EMBU-P meşru**); mekanizma **Goodman & Gotlib (1999)**, *Psychol Rev* 106(3):458, PMID 10467895 (moderatörlerden biri açıkça *baba sağlığı* → §106 negatif-kontrolün kuramsal dayanağı); T1DM'e-özgü **Van Gampelaere et al. (2020)**, *Pediatr Diabetes* 21(2):395, PMID 31697435 (yalnız ANNELER daha çok distres) ve **Rumburg, Lord & Jaser (2017)**, *Pediatr Diabetes* 18(1):67, PMID 26712240. **Prior/benchmark:** **Pinquart (2013)**, *J Pediatr Psychol* 38(7):708, PMID 23660152 — doğrulanmış Hedges g: sıcaklık **g=−.22**, aşırı koruma **g=+.39**, otoriter **g=+.24**, ihmalkâr **g=+.51**.

## 103. Anne otoimmün komorbidite — betimsel prevalans *(test edilemez, §1.5)*

**103.1 Yöntem (v0.2 revize).** §1.5: `anne_hastalik_otoimmun=1` **yalnız 1 aile** (Kontrol'de). Malcová (2004) taban-oranı ~%2 → n=120 DM'de beklenen ~2–3; gözlenen 0 taban-oran sınırındadır. **Karıştırıcı testi güçsüz/yapısal imkânsız.** Yalnız:
- Betimsel prevalans DM vs Kontrol (otoimmün + `endokrin` birlikte; Fisher kesin, hücre çok küçük).
- Açık sınırlama: öz-bildirim formu klinik otoimmün panel (tiroid antikoru/çölyak serolojisi) değil → **eksik-tespit**; "paylaşılan diatez" hipotezi bu örneklemde **test edilemez**, gelecek çalışma klinik panel gerektirir.

**103.2 Çıktı.** Prevalans tablosu + "test edilemez" gerekçe metni. **Tier D.**

**103.3 Tedbir.** İmputation yok; "confounder yok" DEĞİL "örneklemde ölçülemedi"; Malcová baba T1DM'i anneden yüksek → negatif kontrol "hastalık yok" değil "aynı-diatez farklı-yol" çerçevesiyle (§106).

## 104. Anne komorbidite (ikili) → bakım-veren yükü → ebeveynlik/Beck

**104.1 Yöntem (v0.2 revize).** §1.5: `anne_hastalik_kategori_sayisi` %73 sıfır, maks 2 → "sürekli yük" yerine **ikili `anne_any_comorbid` (≥1 kategori, n≈61)**. Bu → Beck ve EMBU-P (sıcaklık↓/reddetme↑) aile-düzeyi. Opsiyonel basit aracılık: komorbidite → Beck → EMBU-P (lavaan + BCa; VanderWeele duyarlılık). Kuram: Pearlin stres-süreç; nicelleme Pinquart (2018).

**104.2 Çıktı.** İkili-komorbidite karşılaştırma + yol + etki büyüklüğü. **Tier C.**

**104.3 Tedbir.** Kesitsel aracılık = zayıf nedensel iddia; ters-yön (depresyon → daha çok bildirilen hastalık) açık tartışma; %73 sıfır → tavan/eksik-tespit uyarısı.

## 105. İki-gösterge maternal-distres yakınsaması

**105.1 Yöntem (v0.2 revize).** §1.5: `anne_hastalik_mental=1` yalnız 2 aile → **dejenere, çıkarılır**. Yakınsama **iki gösterge**: `anne_antidepresan` (temiz; DM %29 vs Kontrol %9) × `beck_total`. Nokta-biserial/tetrakorik korelasyon + grup farkı (antidepresan × grup χ²). Amaç: Beck'in tek-ölçüt olmasına karşı sağlamlık; H3/H4 antidepresan katmanının (CSR §11.3.3) desteklenmesi. **Not:** antidepresan grup-farkı başlı başına raporlanabilir bulgudur (maternal-distres yükünün grup-asimetrisi; Van Gampelaere ile tutarlı).

**105.2 Çıktı.** İki-gösterge uyum + antidepresan×grup tablosu. **Tier B−.**

**105.3 Tedbir.** İki gösterge de anne öz-bildirimi → ortak-yöntem varyansı; "latent distres" iddiası tek-göstergeye indiği için formatif etiketiyle.

## 106. Eş/baba & aile sağlık yükü + negatif kontrol

**106.1 Yöntem.** `es_hastalik_kategori_sayisi` (ikili) ve aile toplam-yük kovaryatı. **Negatif-kontrol mantığı (Goodman-Gotlib baba-moderatörü ile):** babanın somatik hastalığının çocuğun *anne* algısına (EMBU-C anne formu) etkisi olmamalı → beklenmedik ilişki, artık-karıştırma sinyali (Lipsitch negatif kontrol, CSR §13.4). ⚠️ Van Gampelaere (2020): baba distres/parenting anneden farklılaşır → negatif kontrol "sıfır beklenti" makul ama mutlak değil.

**106.2 Çıktı.** Negatif-kontrol katsayısı + %95 GA (sıfıra yakınlık beklentisi). **Tier C.**

---

# KISIM XXXIX — AİLE YAPISI VE KARDEŞ KONSTELASYONU

> **Literatür bağlamı (Evidentia-doğrulı):** **Furman & Buhrmester (1985)**, *Child Dev* 56(2):448, DOI 10.2307/1129733 (SRQ orijinali, 4 üst-boyut) + Buhrmester & Furman (1990, DOI 10.2307/1130750); cinsiyet-bileşimi **Kim, McHale, Osgood & Crouter (2006)**, *Child Dev* 77(6), DOI 10.1111/j.1467-8624.2006.00971.x (kız-kız düadda en yüksek yakınlık); diadik yöntem **Kenny, Kashy & Cook (2006)** *Dyadic Data Analysis* (Guilford) + **Kenny, Mohr & Levesque (2001)**, *Psychol Bull* 127(1):128, DOI 10.1037/0033-2909.127.1.128 (genelleştirilmiş vs diadik karşılıklılık); baba-yokluğu **Amato & Keith (1991)**, *Psychol Bull* 110(1):26, DOI 10.1037/0033-2909.110.1.26 + Amato (2001, DOI 10.1037/0893-3200.15.3.355); doğum sırası **Rohrer, Egloff & Schmukle (2015)**, *PNAS* 112(46):14224, DOI 10.1073/pnas.1506451112 (within-family; Big Five'da ~sıfır) + Damian & Roberts (2015, DOI 10.1016/j.jrp.2015.05.005); resource dilution **Downey (1995)**, *ASR* 60(5):746, DOI 10.2307/2096320 + **Hertwig, Davis & Sulloway (2002)**, *Psychol Bull* 128(5):728, DOI 10.1037/0033-2909.128.5.728.

## 107. Baba yokluğu / tek-ebeveyn — betimsel *(n≈3, §1.5)*

**107.1 Yöntem (v0.2 revize).** §1.5: `es_sag=0` n=1, `medeni_durum=2` n=2 → tek-ebeveyn n≈3. **Moderasyon tanımsız** (Amato küçük etki × near-zero alt-grup). Yalnız betimsel denge tablosunda raporlanır; H1/H3 modellerine kovaryat olarak bile girmez (near-constant). **Tier D.**

**107.2 Çıktı.** Betimsel n + "moderasyon yapılamaz" gerekçe. **Tier D.**

## 108. Doğum sırası & kardeş konstelasyonu

**108.1 Yöntem.** `katilimci_cocuk_sirasi`, `kardes_sirasi`, `cocuk_sayisi`, `age_gap_z`, `same_sex` → algılanan ebeveynlik (EMBU-C). **Within-family kontrast (birincil):** aynı ailede indeks vs kardeş EMBU-C farkı (aile-sabit-etki / conditional) — Rohrer/Damian yöntem dersi: between-family karıştırıcıları (sibship büyüklüğü, SES) otomatik kontrol eder, saf aile-içi bileşeni izole eder. Sibship büyüklüğü (kaynak-seyrelme, Downey/Hertwig) ana etkisi: `cocuk_sayisi` → EMBU-C sıcaklık/aşırı-koruma.

**108.2 Çıktı.** Sıra/aralık katsayı tablosu + within-family kontrast. **Tier B.**

**108.3 Tedbir.** Doğum sırası ile yaş yüksek confounded → yaş kontrolü zorunlu; birth-order etkileri literatürde **minik** (Rohrer) → küçük etki + geniş GA beklentisi, keşifsel; çoklu-karşılaştırma FDR.

## 109. Kardeş SRQ diadik karşılıklılığı (reciprocity/mutuality)

**109.1 Boşluk.** H2 APIM aktör-partner etkisi verir; **karşılıklılık** (iki kardeşin simetrik/asimetrik değerlendirmesi) ve **mütekabiliyet varyans ayrışımı** ayrı sunulmadı.

**109.2 Yöntem.** Ayırt-edilebilir düad (indeks/kardeş) için, her boyutta (sıcaklık & çatışma & rekabet) diadik karşılıklılık korelasyonu (intrapair) + **düad-ortalaması (common fate) vs düad-fark** varyans ayrışımı (Kenny-Mohr-Levesque; H5/`R/20`+`R/39` Olsen-Kenny altyapısı, bu kez kardeş-kardeş çiftine). Ayırt-edilebilirlik SRQ vs SRQ_sib rol-asimetrisini test eder.
- **Uzantı (§1.6-E):** `same_sex` × karşılıklılık (Kim-McHale 2006); `age_gap` non-lineer (spline). Benzerlik/fark etkileri için Dyadic RSA (Schönbrodt, Humberg & Nestler, 2018, DOI 10.1002/per.2169) keşifsel.

**109.3 Çıktı.** Karşılıklılık korelasyon + varyans ayrışımı tablosu. **Tier B.**

**109.4 Tedbir.** **"SRM" adı KULLANILMAZ** — Social Relations Model round-robin (kişi başı ≥3-4 partner) gerektirir; burada yalnız **diadik** mütekabiliyet (Kenny-Mohr-Levesque 2001 varyans ayrıştırması, TripleR uygulanamaz). Bu sınır açıkça yazılır.

---

# KISIM XL — DM-SPESİFİK MARUZİYET YOĞUNLUĞU (DM-only, ağır kısıtlı)


## 110. Yaşam-oranı maruziyet × aşırı koruma

**110.1 Yöntem.** `illness_life_ratio = dm_yili / cocuk_yas`. EMBU (aşırı koruma) ve SRQ ile ilişki; tanı-yaşı spline (§66/`R/27`) ile iç-tutarlı (oran vs süre vs tanı-yaşı üçlemesi).
- ⚠️ **KRİTİK KISIT (v0.2, EK/gap):** pediatrik kronik hastalıkta **doğrulanmış "proportion-of-life" maruziyet metriği literatürde BULUNAMADI** (hedefli PubMed/OpenAlex → yalnız generic burden-of-disease). Metrik teori-yüklü, doğrulanmamış → **duyarlılık analizi** olarak sunulur ve kanonik alternatiflerle **yan yana** raporlanır: (i) tanı-yaşı × güncel-yaş etkileşimi (Malik & Koot), (ii) süre (`dm_yili`) + yaş kovaryat (Mullins gelişimsel moderasyon). Oran birincil estimand olarak sunulmaz.

**110.2 Çıktı.** Oran-maruziyet + kanonik-alternatif karşılaştırma tablosu + %95 GA. **Tier B (DM-only, duyarlılık).**

## 111. Tanı gelişim-penceresi × kardeş maruziyeti — tasarım-sinyali eskizi

**111.1 Yöntem.** Kardeşin, indeksin tanısı anındaki yaşı (`kardes_yas − dm_yili`) → kardeş hangi gelişim penceresinde maruz kaldı? Kardeş SRQ/EMBU-C ile keşif. **Yalnız betimsel eskiz + gelecek-tasarım sinyali** — n ve karışıklık nedeniyle çıkarımsal test önerilmez.

**111.2 Çıktı.** Betimsel serpme + tasarım-önerisi metni. **Tier C (yalnız eskiz).**

---

# KISIM XLI — DİSİPLİN, YENİDEN-ÜRETİLEBİLİRLİK, RAPORLAMA

## 112. OSF Layer 4 & Tip 3 sapma satırı

Faz III, `02-sapma-tablosu.md`'ye **tek bütünleşik Tip 3 satırı** olarak eklenir (Faz II §47 modelini izler):

```markdown
| 3 | 2026-07-08 | Layer 1 + Layer 2 + Layer 3 | Faz I-II kapsamı (KISIM I-XXXV) | Faz III eklendi (KISIM XXXVI-XLI): kanonik bazda mevcut ama kullanılmamış değişken bloklarında keşifsel analizler — PDT-etki (RSA), sosyal sınıf (EGP/eğitim-DRM/ölçüm-yarışı), materyal yoksunluk + Beck-aracı FSM, anne komorbidite/istihdam, aile yapısı, kardeş konstelasyonu, diadik karşılıklılık; fizibilite-denetimiyle §103/§107 betimsele indirildi; mevcut n=241, YENİ VERİ YOK, kilit DEĞİŞMEZ | Tip 3 (major, post-hoc genişletme) | Sosyodemografik-klinik formun modele hiç girmemiş bloklarının literatür-temelli keşfi; H1-H4 confirmatory DEĞİŞMEZ | docs/analiz_planlari/06-sap-faz3-ek-plan.md v0.2; OSF Layer 4 amendment hedefi |
```

- OSF **Layer 4**: "Open-Ended Registration" — başlık *"T1DM-EBEVEYN — Faz III Post-Hoc Exploratory Amendment (Unused-Variable Surfaces)"*; ekli dosyalar: bu plan v0.2 + CSR + güncel sapma tablosu + **Evidentia evidence_packet log'u**; commit SHA hash-çapası.
- **Raporlama:** tüm tablo/şekil başlıklarında `[KEŞİFSEL · POST-HOC]`; tezde ayrı alt-bölüm; "doğruladı" değil "tutarlı yön / hipotez-üretici işaret".

## 113. Yeni R modülleri (**R/51+**) + `_targets.R` entegrasyonu

Saf fonksiyon `R/`, runner `scripts/R/`, doğrulama `tests/`. **Numaralandırma düzeltildi (§1.5-C4): mevcut ağaç R/00–R/50 dolu → yeni modüller R/51+.**

| Modül | Kapsam | Yeniden-kullandığı altyapı |
|---|---|---|
| `R/51_pdt_effect.R` | §96–99 PDT büyüklük/yön/RSA/yol/MTMM/moderasyon | `R/17` (APIM), `R/20` (ICC/Bland-Altman), `R/10` (SRQ map), `R/21` (TOST/simr) |
| `R/52_social_stratification.R` | §100–102b EGP/ölçüm-yarışı/eğitim-DRM/materyal/FSM/istihdam | `R/11` (SES kompozit: material_z, egitim_fark, cift_kazanc), `R/23`/`R/41` (mediation) |
| `R/53_maternal_comorbidity.R` | §103–106 komorbidite/distres/negatif-kontrol | `R/38` (antidepresan yolağı), `R/23` (mediation) |
| `R/54_family_structure_sibship.R` | §107–109 yapı/konstelasyon/karşılıklılık | `R/20`/`R/39` (Olsen-Kenny), `R/17` (APIM) |

Her modül için: `tar_target` hash-bağımlılığı `_targets.R` üzerinden; `format = "file"` kanonik CSV ihlal edilmez; `tests/` altında `stopifnot()` boyut/aralık + **ρ_DD/RSA parametre-sınırı** kontrolü; audit hattı (`scripts/R/09_reporting_standards_audit.R`) yeni çıktıları kapsar. `renv::status()` temiz + yeni bağımlılık (`gnm` [DRM], `RSA` veya `lavaan`-polinom) lock'a eklenir ve commit mesajında gerekçelenir.

## 114. Öncelik kademeleri & fizibilite-güç dürüstlük notu (v0.2 revize)

| Tier | Analizler | Gerekçe |
|---|---|---|
| **A — yüksek değer, düşük risk, veride hazır** | §96 PDT büyüklük/yön/RSA · §97 PDT→SRQ · §98 anne/baba kayırma + MTMM · §102 materyal facet + **Beck-aracı FSM** | n=241 aile-düzeyi yeterli; literatürde merkezî; ölçüm hazır |
| **B — değerli ama gücü/karmaşıklığı sınırlı** | §99 meşruiyet · §100 EGP + ölçüm-yarışı · §102b anne istihdamı · §104 komorbidite(ikili) · §108 konstelasyon · §109 karşılıklılık · §110 DM oran (duyarlılık) | Etkileşim/alt-grup gücü düşük → TOST + simr; keşifsel |
| **B− / C — sinyal/eskiz** | §101 eğitim-DRM (n-yetersiz) · §105 iki-gösterge distres · §106 negatif kontrol · §111 kardeş maruziyet | Ağır n/kimliklenebilirlik kısıtı |
| **D — test edilemez / betimsel** | §103 otoimmün (n=1) · §107 tek-ebeveyn (n≈3) | Yapısal güçsüz → betimsel prevalans + "gelecek çalışma" |

**Dürüstlük notu:** Faz III'ün çekirdeği **KISIM XXXVI (PDT-etki, RSA)**, **§102 materyal facet + Beck-aracı FSM** ve **§98 iki-informant kayırma üçgenlemesi**dir — en yüksek getirili, en düşük riskli, literatüre en doğrudan bağlı hat. **v0.2'nin en önemli katkısı fizibilite dürüstlüğüdür:** §103 (otoimmün) ve §107 (tek-ebeveyn) hücre-sayısı nedeniyle test edilemez ve betimsele indirildi — bunları "keşifsel analiz" diye sunmak jüri savunmasında zaaf olur; "veri sınırı + gelecek tasarım" olarak çerçevelenir.

## 115. Tedbir-ve-hatalar aktif denetim (Faz III'e özel)

- [ ] Her sürekli değişken ortalama **+ medyan**; her alt-grupta `n` açık.
- [ ] Fark-skoru (§96) **ρ_DD hesaplanıp raporlandı**; RSA/polinom birincil, LDS elendi (gerekçeli); Trafimow nüansı dipnot.
- [ ] Null iddialar (buffering, kardeş-uyumu) için **önceden-kayıtlı SESOI |r|≈.10 + TOST** — non-significant ≠ "etki yok".
- [ ] Çoklu karşılaştırma: her KISIM içinde aile-düzeyi FDR/Holm; KISIM'ler arası **birleştirme yok**.
- [ ] **Simpson denetimi (§100 zorunlu):** EGP grupla ağır confounded → grup-içi + havuzlanmış ayrı.
- [ ] Kolinearite: material_z↔prestij, doğum-sırası↔yaş, kalabalıklık↔SES → **VIF**.
- [ ] Ortak-yöntem varyansı: maternal iki-gösterge (§105) tek-kaynak uyarısı.
- [ ] **DRM (§101) yalnız eğitim ekseni** (meslek kimliklenemez); n-yetersizlik açık.
- [ ] **SES = baba-sınıfı** (aile_*08=es_*08) → "baba-sınıfı→anne-ebeveynlik" okuması yazılır.
- [ ] `illness_life_ratio` (§110) **doğrulanmamış metrik** → duyarlılık, kanonik alternatiflerle yan yana.
- [ ] Korelasyon dili nedensel dile kaymaz; kesitsel ters-nedensellik her yol modelinde tartışılır.
- [ ] Tüm çıktı `[KEŞİFSEL · POST-HOC]`; hiçbiri H1-H4 prior'ını değiştirmez (HARKing yasağı).
- [ ] False precision: ondalık hane verinin kesinliğiyle uyumlu.

## EK — Evidentia ile Varlık-Doğrulı Literatür Çapaları

> **Statü (v0.3):** Aşağıdaki künyeler **Evidentia ile VARLIK-doğrulı** (gerçek DOI/PMID) ve v0.3'te **20'lik çekirdek alt-küme tam-metinle claim-page doğrulaması geçti** (OpenAthens/Millet Kütüphanesi + Anna's Reader + Europe PMC; §1.5.5 defter: 14 CONFIRMED, 5 CORRECTED, 1 NOT_FOUND). Yine de Skill Kuralı 20 + CONVENTIONS §11 gereği: hiçbiri **`/referans-kapisi`** tam 6-adımı (PMID/DOI → tam-metin → claim-page → **Zotero item key → BibTeX key → references.bib**) tamamlanmadan tez prosesine girmez — v0.3 ilk üç adımı (varlık + tam-metin + claim-page) kapatır; Zotero/BibTeX mutabakatı bekler. Tam-metin erişilemeyen künyeler (§1.5.5 gap): Sharpe & Rossiter 2002 birincil (SciDB 404 → 2023 güncelleme PMID 35950954 ile), Lovejoy 2000 birincil (→ NBK215128 konsensüs raporu + abstract yön teyidi), Anderson & Coyne 1991 (DOI yok).

**PDT / kardeş diferansiyel muamele (§96–99):**
- Eradus et al. (2024) DOI 10.1037/fam0001194 · PMID 38271066 — PDT meta (215 ES)
- Buist, Deković & Prinzie (2013) DOI 10.1016/j.cpr.2012.10.007 · PMID 23159327 — meta (N=12.257)
- McHale & Pawletko (1992) DOI 10.2307/1130902 — engelli-kardeş bağlamında PDT DAHA YÜKSEK (doğrulandı); ⚠️ "buffering/zayıf-bağ" DEĞİL, bağlam-bağımlı/ters ilişki (§1.5.5 CORRECTED)
- Quittner & Opipari (1994) DOI 10.2307/1131419 — kistik fibroz
- Kowal & Kramer (1997) DOI 10.2307/1131929 · Kowal, Kramer, Krull & Crick (2002) DOI 10.1037/0893-3200.16.3.297 — adalet/meşruiyet
- McHale et al. (2000) DOI 10.1111/1467-9507.00117 · Shanahan et al. (2008) DOI 10.1111/j.1741-3737.2008.00495.x · Coldwell, Pike & Dunn (2008) DOI 10.1111/j.1467-9507.2007.00440.x · Loeser, Whiteman & McHale (2016) DOI 10.1007/s10826-016-0429-2 · Feinberg et al. (2000) DOI 10.1111/1467-8624.00252 · Solmeyer & McHale (2015) DOI 10.1111/famp.12166 · Sharpe & Rossiter (2002) DOI 10.1093/jpepsy/27.8.699 (⚠️ içe-yönelim d≈0.41 / dışa-yönelim d≈0.15; "0.28" ortalamadır — §1.5.5) · Kardeş meta güncelleme (2023) PMID 35950954

**Fark-skoru & çok-informant metodoloji (§96, §98):**
- Rogosa & Willett (1983) DOI 10.1111/j.1745-3984.1983.tb00211.x · Overall & Woodward (1975) DOI 10.1037/h0076158
- Edwards & Parry (1993) DOI 10.2307/256822 · Edwards (1994) DOI 10.1006/obhd.1994.1029 · (1995) DOI 10.1006/obhd.1995.1108 · (2001) DOI 10.1177/109442810143005 · (2007) DOI 10.1177/1094428107308920
- Trafimow (2015) DOI 10.1080/23311835.2015.1064626 (savunma/nüans)
- McArdle (2009) DOI 10.1146/annurev.psych.60.110707.163612 · McArdle & Hamagami (2001) DOI 10.1037/10409-005 (LDS — elendi)
- De Los Reyes & Kazdin (2004) DOI 10.1037/1040-3590.16.3.330 · (2005) DOI 10.1037/0033-2909.131.4.483 · De Los Reyes et al. (2013) DOI 10.1146/annurev-clinpsy-050212-185617 · Laird & De Los Reyes (2013) DOI 10.1007/s10802-012-9659-y
- Lakens (2017) DOI 10.1177/1948550617697177 · Lakens, Scheel & Isager (2018) DOI 10.1177/2515245918770963 · Campbell & Fiske (1959) DOI 10.1037/h0046016

**Sosyal sınıf & ebeveynlik (§100–102):**
- Kohn (1963) DOI 10.1086/223403 · Kohn & Schooler (1969) DOI 10.2307/2092303 · Conger, Conger & Martin (2010) DOI 10.1111/j.1741-3737.2010.00725.x (⚠️ narratif derleme — β nokta-değeri YOK, §1.5.5 NOT_FOUND) · Bradley & Corwyn (2002) DOI 10.1146/annurev.psych.53.100901.135233
- Erikson, Goldthorpe & Portocarero (1979) DOI 10.2307/589632 · Ganzeboom, De Graaf & Treiman (1992) DOI 10.1016/0049-089x(92)90017-b · Ganzeboom & Treiman (1996) DOI 10.1006/ssre.1996.0010
- Sobel (1981) DOI 10.2307/2095086 · (1985) DOI 10.2307/2095383 · van der Waal et al. (2017) DOI 10.1007/s00038-017-1018-x · McLoughlin et al. (2022) DOI 10.1093/geronb/gbac122
- Evans (2004) DOI 10.1037/0003-066x.59.2.77 · Evans & English (2002) DOI 10.1111/1467-8624.00469 · Hoff & Laursen (2019) DOI 10.4324/9780429401459-13

**Maternal distres & komorbidite (§103–106):**
- Pearlin et al. (1990) PMID 2276631 · Pinquart (2018) PMID 28834111 · Demirtepe-Saygılı & Bozo (2011) PMID 21038170 (Türk)
- Malcová et al. (2004) PMID 15532904 (paylaşılan diatez) · Lovejoy et al. (2000) PMID 10860167 · Goodman & Gotlib (1999) PMID 10467895
- Pinquart (2013) PMID 23660152 (**g benchmark: sıcaklık −.22, aşırı koruma +.39, otoriter +.24, ihmalkâr +.51**) · Van Gampelaere et al. (2020) PMID 31697435 · Rumburg et al. (2017) PMID 26712240 · Chen & Panebianco (2020) PMID 31818131

**Aile yapısı & diadik (§107–109):**
- Furman & Buhrmester (1985) DOI 10.2307/1129733 · Buhrmester & Furman (1990) DOI 10.2307/1130750 · Kim et al. (2006) DOI 10.1111/j.1467-8624.2006.00971.x
- Kenny, Mohr & Levesque (2001) DOI 10.1037/0033-2909.127.1.128 · Kenny, Kashy & Cook (2006) *Dyadic Data Analysis* (Guilford, ISBN 978-1572309869) · Schönbrodt, Humberg & Nestler (2018) DOI 10.1002/per.2169
- Amato & Keith (1991) DOI 10.1037/0033-2909.110.1.26 · Amato (2001) DOI 10.1037/0893-3200.15.3.355 · Rohrer et al. (2015) DOI 10.1073/pnas.1506451112 · Damian & Roberts (2015) DOI 10.1016/j.jrp.2015.05.005 · Downey (1995) DOI 10.2307/2096320 · Hertwig, Davis & Sulloway (2002) DOI 10.1037/0033-2909.128.5.728

**T1DM maruziyet (§110–111):**
- Prikken et al. (2019) DOI 10.1080/08870446.2018.1538451 (⚠️ operatif mediyatör = psikolojik kontrol, aşırı koruma DEĞİL; dolaylı etki anne .107/baba .061 — §1.5.5 CORRECTED) · Fales et al. (2014) DOI 10.1093/jpepsy/jsu003 · Mullins et al. (2007) DOI 10.1093/jpepsy/jsm044 · Hullmann et al. (2010) DOI 10.1007/s10880-010-9213-4 · Van Gampelaere et al. (2020) DOI 10.1111/pedi.12942 · Malik & Koot (2009) DOI 10.2337/dc08-1306 · Anderson et al. revised DFCS (2007) PMID 17372149
- ⚠️ **VERİ BULUNAMADI:** Anderson & Coyne (1991) "miscarried helping" seminal kitap-bölümü (DOI yok); doğrulanmış "proportion-of-life" maruziyet metriği (§110 zayıf-halka) → duyarlılık katmanı.

**gap_log (tam-metin/doğrulama boşlukları):**
- Tam-metin (openathens Tier-3) gated → Pinquart g'leri dışında sayısal etki büyüklükleri abstract düzeyi; PDT havuzlanmış r ve Amato per-domain d **tam-metinden** doğrulanacak.
- Semantic Scholar 429 rate-limit (CrossRef/PubMed/OpenAlex ile telafi edildi).
- Türk örneklemli EGP/ISEI × ebeveynlik ve Türkçe EMBU norm/geçerlik → **`academic-archival-distiller`/YÖK Tez** ile ayrıca taranmalı (aktarılabilirlik).
- Tüm dış-kanıt koşumu `./dmnitel log-ai-use` ile kayıt altına alınır (raw/identifiable = no).

---

**Tek cümlelik özet (v0.2):** Faz III, çalışmanın sosyodemografik-klinik formunda *zaten toplanmış ama hiçbir modele girmemiş* değişken bloklarını literatür-temelli (Evidentia-doğrulı çapalar), **fizibilite-dürüst** (hücre-sayısı denetimiyle §103/§107 betimsele indirildi) ve metodolojik olarak sağlam (ρ_DD güvenilirlik, RSA/polinom, SESOI-TOST, MTMM üçgenleme, Beck-aracı FSM) bir keşif çerçevesinde değerlendirir; H1–H4 doğrulayıcı çekirdeğe dokunmaz, DRM'yi kimliklenebilir eğitim eksenine taşır, mevcut SES altyapısını yeniden kullanır ve her çıktı `[KEŞİFSEL · POST-HOC]` kalır.
