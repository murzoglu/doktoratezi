# BP2027 Türkiye NSCLC — Baz Veri ve Varsayım Defteri

> **Amaç.** Farid'in dört sorusunu geniş perspektife oturtarak, **mevcut koşullarda BP2027 Türkiye NSCLC
> hesaplamaları için baz alınması gereken bilimsel veri + varsayımları** tek, izlenebilir bir deftere
> toplar. Üretim: Workflow `wihtn85r8` (5 paralel şerit; run `wf_94dda128-58a`), 2026-07-27; kanıt tabanı
> anamnesis korpusu (179 doküman) + TİTCK KÜB + SUT 10/07/2025 primer + GLOBOCAN/EXPRESS.
>
> **Katman etiketi (kanıt≠bağlam):** **[E]** = L2 kanıt (birincil çalışma/tam-metin, etki/prevalans sayısı);
> **[C]** = bağlam (regülatif/epidemiyoloji/metodoloji — sayı besler ama etki-büyüklüğü değil); **[L]** =
> yalnız-yerel-veri (MEDULA/EHR/satış olmadan literatürle kapatılamaz). **RBŞ:** her değer kendi
> payda/assay/dönem kapsamında; uyumsuz paydalar havuzlanmaz. Ondalık ayırıcı virgül. Uydurma yok; çözülemeyen `L`.
>
> Tamamlayıcı belgeler: dossier [`bp27_atezolizumab_tr_fulltext_dossier.md`](bp27_atezolizumab_tr_fulltext_dossier.md);
> zenginleştirme [`bp27_atezolizumab_tr_science_skills_enrichment.md`](bp27_atezolizumab_tr_science_skills_enrichment.md) §A–I;
> sentez [`../06_synthesis/bp27_atezolizumab_tr_synthesis.md`](../06_synthesis/bp27_atezolizumab_tr_synthesis.md).

---

## 0. Yönetici özeti — üç katmanlı baz

BP2027 hesaplaması **üç ayrı güven katmanına** oturmalı; bunları karıştırmak problem.md'nin teşhis ettiği
beş metodolojik hatanın kaynağıdır:

1. **[E] Literatür-baz parametreler (savunulabilir priörler):** epidemiyoloji, moleküler/PD-L1 strata,
   DoT/RMST eğrileri, atrisyon çarpanları. Bunlar **başlangıç priörüdür** — TR'ye kalibre edilene kadar
   düşük/baz/yüksek olarak kullanılır.
2. **[C] Primer regülatif çerçeve (10/07/2025 SUT):** uygun + geri-ödemeli havuzun **üst sınırını** çizer.
   **En büyük 2027 değişikliği burada:** atezolizumab artık hem 1L (PD-L1≥50) hem 2L geri-ödemeli.
3. **[L] Yalnız-yerel-veri:** mutlak hasta sayısı, aylık kohort akışı, progresyon→TEC dönüşümü. **Hiçbir
   literatür katsayısı ikame edemez** (problem.md §13'ün kendi teşhisi); yalnız MEDULA + EHR + satış
   tekilleştirmesiyle hesaplanır.

**Değişmez kaideler:** (a) **gelir MEDYAN DoT ile değil RMST=∫S_DoT(t)dt ile**; (b) **biyolojik havuz ≠
geri-ödemeli TEC havuzu** — büyüklük progresyonda gerçek uygunluğa dönüşümden; (c) her yüzde **payda etiketiyle**;
(d) **zaman-sıfırı = definitif RT bitişi** (immortal-time yanlılığı); (e) ölüm **competing risk** (PFS'e çift-iskonto yok).

---

## 1. Huni-başı epidemiyoloji ve evre/histoloji [Lane A]

| Parametre | Baz | Düşük–Yüksek | Katman | Kaynak | Güven |
|---|---|---|---|---|---|
| TR akciğer kanseri insidansı (yıllık, iki cinsiyet) | **41.032** | 36.224–46.478 | C | GLOBOCAN 2022 (IARC, pop 792, cancer 15) | yüksek |
| — erkek / kadın | 33.039 / 7.993 | — | C | GLOBOCAN 2022 (M:F 4,1) | yüksek |
| NSCLC / akciğer kanseri | **%79,6** | %79,6 (TR) – %80–85 (global) | E | Cangir 2022 `10.1016/j.jtho.2022.06.001` | yüksek |
| SCLC / akciğer | %16,5 | ~%16–16,7 | E | Cangir 2022 | yüksek |
| Tanıda Evre IV | **~%50** | %50,5 – %56,5(uzak-met global) | E | Cangir "%>50 ileri"; TOG Alan `10.3390/medicina61071160` %50,5 | orta |
| Tanıda Evre III (lokal ileri) | **~%28** | %26,5 – ~%30 | E | Cangir "~%30"; TOG Alan %26,5 | orta |
| Tanıda Evre I / II | I %5,1 / II %17,9 | (tek kohort) | E | TOG Alan (n=196) | düşük |
| Histoloji: adeno / skuamöz (tüm akciğer) | %47,7 / %36,8 | adeno %47,7–51,8 | E | Cangir 2022 | yüksek |
| ECOG 0–1 (tanı-geneli) | **~%78** | %48 (ESTIMATE 1L) – %78 (İzmir dağılım) – %99 (Evre III KRT-seçili) | C/L | İzmir/Yavuz (0 %43,4/1 %34,3/2 %21,2); ESTIMATE `10.1080/14796694.2025.2527477` %48,1; Boys `10.1111/1759-7714.14780` | düşük |
| TR akciğer 5-yıl sağkalım (sonuç çapası) | **çoğu kayıtta <%15** | %10,7 (Edirne) – %19,4 (Trabzon) | E | Zahwe/Eser 2026 IJC `10.1002/ijc.70628` | yüksek |

**Düzeltme [C]:** problem.md §9'un "GLOBOCAN 2024 fact sheet: 37.846" ifadesi **atıf hatasıdır** — 37,88
aslında ASR/100.000'dır (sayı değil); ayrı bir "2024 turu" yoktur, güncel tur GLOBOCAN 2022'dir. **Kaba
Evre III tavanı bu yüzden 41.032 × %80–85 × %20–25 ≈ 6.600–8.700/yıl** (belgenin 6.100–8.000'ine yakın, hafif yukarı).

**Boşluk:** ulusal HSGM evre-dağılım tablosu ve 2027 insidans projeksiyonu yok (TÜİK nüfus projeksiyonu + ASR
varsayımıyla ayrı model gerekir). ECOG kaynağı (İzmir/Yavuz) korpusta doğrulanamadı; ESTIMATE %48,1 ile İzmir
%77,7 **farklı kohortlardır**, ortalanmamalı.

---

## 2. Moleküler ve PD-L1 biyobelirteç strata [Lane B]

| Parametre | Baz | Düşük–Yüksek | Katman | Kaynak (assay) | Güven |
|---|---|---|---|---|---|
| EGFR mutasyon (tüm NSCLC) | **%16** | %12–16,7 | E | Canaslan `10.3390/genes16121446`; Guler-Tezel `10.4274/balkanmedj.2017.0297` | yüksek |
| ALK füzyon | %5,0 | %3,4–8,3 | E | Canaslan; Cangir (FISH) | yüksek |
| ROS1 füzyon | ~%1,9 | %0,4–2,4 | E | Canaslan; Dülger | yüksek |
| KRAS total | ~%26 | %5,8–35,4 (bölgesel) | E | Cangir (n=1081); Basdemirci `10.4103/ijc.IJC_766_19` | orta |
| KRAS G12C | %2,6 | %2,6–3,1 (TR); global %10–13 | E | Canaslan; Lim `10.1016/j.lungcan.2023.107293` | düşük* |
| BRAF V600E / METex14 / HER2 | %3,2 / %2,5 / %1,4 | (tek kohort) | E | Canaslan | orta |
| **Hedeflenebilir toplam (ESCAT Tier I)** | **%28,3** | %28,3–35,9 | E | Canaslan (289/1023) | yüksek |
| **Sürücü-negatif (IO-uygun)** | **EGFR/ALK/ROS-WT ~%77; hiç-hedef-yok ~%72** | %64–79 | E | Canaslan (türetilmiş) | orta |
| **PD-L1 TPS≥50 — all-comer 22C3** | **%27,5** | %22–28 | E | **Dülger `10.4103/ijpm.ijpm_939_23` (22C3)** | yüksek |
| PD-L1 TPS≥50 — metastatik-only (alt-uç) | %17,8 | — | E | Canaslan (601, klon-NR) | orta |
| PD-L1 TPS≥50 — EGFR/ALK-WT | **~%27** | %24–27 | C | EXPRESS/Dietel 2019 `10.1016/j.lungcan.2019.06.012` (global 22C3) | orta |
| PD-L1 TPS≥1 | ~%52 | %52 (metastatik) – %69 (all-comer 22C3) | E | Canaslan; Dülger; EXPRESS %52 | orta |
| PD-L1 test oranı / NGS oranı | ~%56–59 / %51,6→>%90 | — | E | Canaslan; ESTIMATE | yüksek |

*G12C: TR %2,6 tek metastatik kohort + ~%52 NGS kapsamı → **eksik‑saptama** (gerçek muhtemelen global %10–13'e yakın).

**PD-L1 hükmü (§I ile tam; F7-B/D düzeltmesi — payda-eşleşmeli):** "**~%18**" (Canaslan) TR'nin temsili değeri
**değil**, alt ucudur (metastatik-only, klon-NR). **Payda-eşleşmeli kıyas:** TR all-comer 22C3 **%27,5** (Dülger)
vs **global all-comer 22C3 %22** (EXPRESS) → **TR üst uçta, anormal düşük değil**. Global EGFR/ALK-WT %27'dir ama
**TR-özgü EGFR/ALK-WT ≥50 değeri yoktur** → EXPRESS ile çapalanır (all-comer ve EGFR-WT paydaları **karıştırılmaz**).
Üç ≥50 değeri (%27,5 all-comer TR / %17,8 metastatik-only TR / %27 EGFR-WT global) **ortalanmaz** — her biri kendi paydasıyla.

---

## 3. Hat-akışı, DoT/RMST maruziyet, atrisyon (competing risk) [Lane C]

| Parametre | Baz | Düşük–Yüksek | Katman | Kaynak | Güven |
|---|---|---|---|---|---|
| TR 1L IO uptake (2020–2021, pre-2025) | **%11,5** (kombo %6 + mono %5,5) | — | E | ESTIMATE `10.1080/14796694.2025.2527477` | yüksek |
| **1L mono DoT — 24-ay RMST** *(gelir metriği)* | **10,3 ay** | 9,7–11,0 | E | Velcheti `10.3390/cancers14041041` | yüksek |
| — aynı, medyan rwToT (yanıltıcı) | 7,4 ay | 6,3–8,1; PS2 → 2,1 ay | E | Velcheti | yüksek |
| 1L kemo-IO DoT (medyan rwToT) | 5,6 ay (non-sq) / 6,5 ay (sq) | 4,5–7,6 | E | Liu/Velcheti `10.1038/s41598-021-88453-8`; Liu `10.1016/j.jtocrr.2022.100444` | yüksek |
| **2L atezolizumab DoT (OAK medyan)** | **3,4 ay** | 0–26; **>12 ay %21; TBP %40** | E | OAK `10.1016/S0140-6736(16)32517-X` | yüksek |
| 2L atezo TAIL (genel-pop) | PFS 2,7 ay; OS 11,2 ay | — | E | TAIL-final `10.1136/jitc-2022-005581` | yüksek |
| 2L nivolumab TR (IO-naif) | PFS 4,2 ay (DoT raporlanmadı) | 3,5–4,8 | E | TOG Alan `10.3390/medicina61071160` | orta |
| 2L nivo Fransa/EU DoT | 2,5–2,8 ay | 2,3–3,2 | E | Chouaid ESME `10.3390/cancers14246148` | yüksek |
| Metastatik → 1L dönüşüm | ~%50–60 | %50,2 (≥66y) – ~%60 | E | Kehl `10.1002/cam4.2854` | orta |
| 1L → 2L (kemo dönemi) | %46–71 (ülke-bağlı) | — | E | PIvOTAL `10.1111/ecc.12734` | yüksek |
| **1L → 2L (1L-IO SONRASI — atrisyon cezası)** | **%21–44** | — | E | Fung/Rittberg `10.3390/curroncol30060402` | yüksek |
| Ölüm-öncesi-2L (competing risk) | ~%10–22 | — | E | Bauman `10.1016/j.lungcan.2024.107919`; REFLECT `10.1177/17588359211059874` | orta |
| **2L'de IO-naif fraksiyon (TR)** | **~%100 şimdi → küçülüyor** | — | E | TOG Alan (2L'de 1L-IO %0) | yüksek |
| Evre III durvalumab DoT (RW) | 11,0 ay | (≤12 ay cap) | E | PACIFIC-R `10.1016/j.jtho.2022.10.003` | yüksek |
| Evre III ilk-6-ay erken progresyon | %18 (durva-başlatan) – %31 | %18–31 (durva-starter paydası) | E | Park `10.21037/tlcr-2024-1112`; İsrail `10.1111/1759-7714.70130` | orta |

**DoT hükmü:** ticari maruziyet **RMST ile** modellenir; 2L atezo'ya sabit 3-ay atanmaz — hazard yapısı 0–3 ay
yüksek bırakma / 4–12 ay düşük / >12 ay uzun-yanıt kuyruğu. **Atrisyon anahtarı:** 1L IO büyüdükçe 1L→2L dönüşüm
%21–44'e düşer (post-IO cezası) **ve** 2L'de IO-naif fraksiyon mekanik olarak küçülür.

---

## 4. 2027 regülatif + geri-ödeme + rekabet çerçevesi [Lane D] — **en büyük değişiklik**

**Geri-ödemeli NSCLC IO matrisi (SUT 10/07/2025, RG 32952, 4.2.14.C yeni fıkra(3); [C] primer):**

| Ajan (bent) | Basamak/ayar | Anahtar koşul | Katman |
|---|---|---|---|
| **Atezolizumab c)2** | **1L** metastatik | **PD-L1≥%50**, ECOG 0-1, EGFR/ALK/ROS-neg, ≤35 kür | C (RG 32952) |
| **Atezolizumab c)3** | **2L** lokal ileri/metastatik | önceki 1-2 kemoterapi + progresyon, ECOG 0-1, **PD-L1 eşiği YOK**, ardışık-IO dışlaması | C |
| **Nivolumab a)14** | **2L** | önceki **1** kemoterapi + progresyon, ECOG 0-1, ardışık-IO dışlaması | C |
| **Durvalumab ç)2** | **Evre III** | PD-L1≥%1, KRT sonrası progresyonsuz, monoterapi, ≤12 ay | C |
| Pembrolizumab b)1-4 | 1L (histoloji) / neoadjuvan | PD-L1 eşikleri (OCR bozuk → RG primer teyit) | C |

- **Ardışık/önceki-IO dışlaması TÜM ajanlarda** hard-coded → 1L-IO veya durvalumab almış hasta sonraki
  basamakta IO geri-ödemesi **alamaz** (sıralı-IO squeeze'in yasal temeli).
- **Ürün:** TECENTRIQ 1200mg/20mL (barkod 8699505763460) GERİ ÖDEMELİ, perakende 123.966,50 TL (2026-04-01);
  840mg formu ödemesiz; SC (Hybreza) TİTCK'te **yok**.
- **Boru hattı (2027 ufku, [C] CT.gov):** AVANZAR (Dato-DXd+durva 1L, NCT05687266, TR 5 merkez, birincil
  tamamlanma **2027-11** → 2027+ tehdit, 2027 içi geri-ödeme olayı değil); SKYSCRAPER-01 (tiragolumab+atezo,
  NCT04294810, tamamlandı ama anti-TIGIT OS başarısızlığı → 2027 filing olası değil, doğrula); SC atezolizumab
  (kolaylık, mekanizma değil; TR kaydı yok). TR-aktif atezolizumab-NSCLC çalışma ayak izi ≥15 (alt-sınır).

**Rekabet re-base'i (kritik):** problem.md §6'nın "atezo yalnız 2L nivolumab-egemen segmentte" premisi **artık
geçersiz** — atezo şimdi **1L PD-L1≥50 mono segmentini (pembrolizumab ile) VE 2L segmentini (nivolumab ile)**
paylaşıyor. Pazar-payı matematiği **iki ayrı payda** üzerinde yeniden kurulmalı. Segment-başı % = [L] (IQVIA/MEDULA).

---

## 5. Yalnız-yerel-veri parametreler + duyarlılık priörleri [Lane E]

Aşağıdakiler **[L]** — literatür ikame edemez; başlangıç priörü kanıt-doğrulanmış çarpanlardan verilir:

| Parametre | Priör (düşük/baz/yüksek) | Kapatma yolu |
|---|---|---|
| Aylık yeni IO-naif progresör (mutlak) | epi tavanı ~508–667/ay ÜST SINIR; waterfall sonrası ~25–100/ay | MEDULA + 8–12 merkez EHR (§13) |
| Legacy uygun-fakat-başlamamış stok | bilinmiyor (5-yıl prevalans **54.335** [GLOBOCAN 2022] = çok geniş tavan) | claims + PSP dedup |
| Aktif tedavi stoku OnTx_t | Σ başlangıç × S_tedavide(k) | ünite/sipariş kalibrasyonu |
| **Progresyon → gerçek TEC dönüşümü** | **güvenilir dış katsayı YOK**; "herhangi 2L sistemik" halkası %21 (Fung) / %30 (Liu) / %42 (STONE pre-IO) | merkez dosya: her kayıp nedeni kodlu |
| TR-native S_DoT(t) + RMST | uluslararası ödünç (1L mono RMST 10,3 ay; 2L atezo DoT ~3,15 ay) | TR claims 60-gün boşluk KM |
| KRT-sonrası ilk-6-ay progresyon | %15–18 / %20–25 / %30–35 (payda-etiketli) | Aalen-Johansen kümülatif insidans |
| TR durvalumab-PACIFIC RW kohortu | **TR'de yok** (STONE pre-durvalumab) | merkez dosya doğrulaması |
| ECOG 3 geri-ödemeli TEC | **0 / 0 / 0** (KÜB+SUT ECOG 0-1) | özel-ödeme ayrı senaryo |

**En etkili belirsizlik sürücüleri (öncelik):** (1) aylık IO-naif progresör sayısı, (2) durvalumab kullanım
oranı, (3) progresyonda ECOG 0-1 kalma, (4) progresyon→sistemik dönüşüm, (5) TEC seçim oranı, (6) uzun DoT kuyruğu.
**Kapatma tasarımı:** 8–12 yüksek-hacim merkez, son 24–36 ay ardışık hasta, zaman-sıfırı=RT bitişi, 8-durumlu
çok-durumlu model, her parametre düşük/baz/yüksek + %95 aralık + Monte Carlo.

---

## 6. Farid'in dört sorusuna geniş-perspektif cevap

- **Soru 1 (1L DoT <10 ay?):** Medyan evet (~5–8 ay) **ama gelir için RMST kullan** (1L mono 24-ay RMST 10,3 ay).
- **Soru 2 (ECOG 3 upside?):** Hayır — KÜB+SUT primer ECOG 0-1; ECOG 3 geri-ödemeli havuz = 0.
- **Soru 3 (%35 pay düşük mü?):** Aritmetik doğru **ama payda re-base'i şart** — atezo artık 1L+2L iki segmentte;
  eski mono-segment matematiği yeniden kurulmalı.
- **Soru 4 (2L kaç hasta / ne zaman biter?):** Mutlak sayı **[L]** (literatürle çözülemez). **Yapısal yeni gerçek:**
  2L'de atezo **ruhsatlı+geri-ödemeli** (10/07/2025), 2L havuz **şu an ~%100 IO-naif ama 1L IO/durvalumab
  büyüdükçe daralıyor**. Wash-out üçe ayrılır (legacy stok / incident inflow / aktif kuyruk); tek tarih yok.

---

## 7. Kapanış hüküm

BP2027'nin en tutarlı temeli: **[E] literatür priörleri + [C] 10/07/2025 primer regülatif çerçeve** ile üst-sınır
ve çarpanlar kurulur; **[L] mutlak akış** yalnız yerel MEDULA/EHR/satış tekilleştirmesiyle hesaplanır. **En kritik
2027 farkı regülatiftir:** atezolizumab artık hem 1L (PD-L1≥50, hedef ~EGFR/ALK-WT'nin %25–30'u) hem 2L (eşiksiz,
IO-naif havuz) geri-ödemeli — bu, hem fırsatı büyütür hem de ardışık-IO dışlaması nedeniyle 2L IO-naif havuzu
zamanla daraltır. Fırsatın büyüklüğü Evre III/IV hastaların **varlığından** değil, **progresyonda gerçek TEC
uygunluğuna dönüşümden** hesaplanmalıdır.

*Tüm sayılar kaynak-bağlıdır (DOI/PMID/RG 32952/GLOBOCAN/corpus doc_id); [E]/[C]/[L] katmanı ve payda her satırda
işaretlidir. Ayrıntılı per-parametre kayıt: Workflow `wihtn85r8` çıktısı + zenginleştirme §A–I.*
