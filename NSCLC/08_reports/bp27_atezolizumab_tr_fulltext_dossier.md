# BP27 Türkiye Atezolizumab — Tam-Metin Maksimum-Detay Çıkarım Dosyası

**Tarih:** 2026-07-24 · **Kapsam:** `problem.md` değerlendirmesi için bu turda incelenen ~54 makalenin tam-metin (full-text) kaskad-erişimli çıkarımı.
**Kaskad (yasal-öncelikli):** Minerva `fulltext_by_doi` → EPMC/PMC OA (`pubmed_fetch_fulltext` + Unpaywall) → annas-reader. **OpenAthens Tier-3 kullanılamadı** (`validated:false`; noVNC challenge çözülmeli). **anamnesis RAG ingest** anahtarsız (401) → tam metinler alt-ajan bağlamında damıtıldı.
**G-COPYRIGHT:** hedefli sayısal çıkarım; toptan verbatim yok (<25 kelime lokatör alıntıları). **No-fabrication:** her sayı PMID/DOI + lokatöre bağlı; erişilemeyen = `unverified`.

---

## 0. Kaskad kapsam raporu (54 makale)

| Erişim tier | Adet | Not |
|---|---|---|
| **Minerva Tier-1** (tam gövde, AI-inference hakları) | ~31 | Onkoloji korpusu güçlü kapsama |
| **EPMC/PMC OA Tier-2** | ~13 | TAIL, PACIFIC-alt, PIvOTAL, REFLECT, Fung, Bauman, TOG, İzmir, EMPOWER, Demiray, Teoman, Shi |
| **Unpaywall / annas Tier-3** | 2 | Dülger (Unpaywall CC-BY-NC-SA); Çiçek (annas) |
| **Abstract-only / gövde alınamadı (`unverified`)** | 5 | Aşağıda |

**Tam-metin alınamayan 5 (abstract-flagged):**
1. Nations 2020 SEER/DoD evre (Mil Med) — OUP paywall 403; Minerva 404, annas 404. DOI 10.1093/milmed/usaa218
2. Midha 2015 mutMapII gövde tabloları — PMC yalnız abstract; DOI PMID 26609494 (abstract doğrulandı)
3. Basdemirci 2022 KRAS (Indian J Cancer) — OA yok; PMID 34380837
4. Kilickap/Karadurmus ulusal nivolumab registry — T&F 403; DOI 10.1080/03007995.2024.2359026
5. Kapagan İstanbul prospektif 2L nivolumab — OA yok; DOI 10.1177/10781552251389883

Ayrıca tam-metin-içi tablo-bağlı birkaç değer `unverified`: Aslan 2025 erken-nüks kesin oranı; OAK ITT ORR n/%; TAIL alt-grup DoT.

---

## A. Birinci-basamak IO tedavi süresi (DoT / rwToT / RMST)

| Çalışma (PMID/DOI) | Popülasyon | Medyan DoT/rwToT | Landmark on-tx | RMST / kuyruk | OS / PFS |
|---|---|---|---|---|---|
| Velcheti 2022 (35205788; 10.3390/cancers14041041) | 1L pembro mono, PD-L1≥50, Flatiron; PS0-1 n=807 / PS2 n=237 | **7,4 ay** (6,3–8,1) PS0-1 / **2,1 ay** (1,4–2,8) PS2 | 24-ay %22,1 / %9,9 | 24-ay RMST **10,3 ay** (9,7–11,0) / 5,9 ay; ≥35 döngü %16 | rwToT-only; 2L %33 (PS0-1) |
| Liu/Burke 2021 (33911121; 10.1038/s41598-021-88453-8) | 1L pembro+peme-karbo, non-sq, PS0-1, n=283 | pembro **5,6 ay** (4,5–6,4) | 6-ay %47; 12-ay %29 | 12-ay RMST 6,3 ay | OS 16,5 ay; rwPFS 6,4 ay; TRR %56,5 |
| Liu/Burke 2023 (36755804; 10.1016/j.jtocrr.2022.100444) | 1L pembro+karbo/taksan, skuamöz, PS0-1, n=364 | pembro **6,5 ay** (5,6–7,6) | 12-ay %29,3; 24-ay %15,9 | medyan 9 doz | OS 15,3 ay; 12/24-ay OS %54,9/%37,3 |
| IMpower110 Herbst 2020 (32997907; 10.1056/NEJMoa1917346) | 1L atezo mono, PD-L1+, faz III, n=277 WT | **5,3 ay** (atezo) | — | TBP izinli | yüksek PD-L1 OS 20,2 vs 13,1 (HR 0,59); PFS 8,1 vs 5,0 |
| KEYNOTE-024 5-yıl Reck 2021 (33872070; 10.1200/JCO.21.00174) | 1L pembro mono PD-L1≥50, n=154 | **7,9 ay** (1 gün–30,2 ay) | ≥35 döngü %25,8 (39/151) | 35-döngü sonrası 3-yıl OS %81,4 | OS 26,3 vs 13,4; 5-yıl OS %31,9 vs %16,3 |
| KEYNOTE-407 5-yıl Novello 2023 (36735893; 10.1200/JCO.22.01990) | 1L pembro+kemo skuamöz, n=278 | ≥35 döngü %19,8 (prior medyan ~7,1 ay) | — | 35-döngü ORR %90,9 | OS HR 0,71; 5-yıl OS %18,4 vs %9,7 |
| KEYNOTE-189 5-yıl Garassino 2023 (36809080; 10.1200/JCO.22.01989) | 1L pembro+peme-platin non-sq, n=410 | ≥35 döngü %13,9 | 7 hâlâ peme'de | 35-döngü DoR 57,7 ay | OS HR 0,60; 5-yıl OS %19,4 vs %11,3 |
| POSEIDON Johnson 2023 (36327426; 10.1200/JCO.22.00975) | 1L durva±treme+kemo, n=338/338/337 | medyan **8 durva doz** (1–49); 5 treme dozu %66,1 | — | D+CT still-on 31 | D+CT OS 13,3 vs 11,7 (HR 0,86, NS); T+D+CT OS 14,0 (HR 0,77) |

**Sentez A:** ECOG 0-1'de 1L IO medyan DoT ~5,3–7,9 ay (mono üstte, RCT çapası KN024 7,9 ay ≈ RWE 7,4 ay); **medyan≠beklenen maruziyet** kesin doğrulandı (7,4→10,3 ay RMST, uzun-yanıtlı kuyruk = 24-ay %22 on-tx + ≥35 döngü %14–26). ECOG 2 → 2,1 ay çöküş. *Belgenin DoT hükmü tam-metinle sağlam.*

---

## B. Kötü performans (ECOG 2 vs 3-4) ICI

| Çalışma (PMID/DOI) | ECOG 2 | **ECOG 3(-4)** | Pnömonit / güvenlik |
|---|---|---|---|
| Ahmed 2020 (32089478; 10.1016/j.cllc.2020.01.001) | OS **8,3 ay**; PFS 5,1 ay (n=114) | **OS 1,5 ay; PFS 1,3 ay** (n=18); ORR %23,1 | irAE-steroid PS3 %22,2 (n küçük) |
| Katsura 2019 (31258716; 10.7150/jca.31217) | OS **95 gün** (PS2) | **PS3-4 OS 28 gün; BSC'ye üstün DEĞİL** HR 1,235 (P=0,516) | ağır pnömonit poor-PS **%25**; 1 grade-5 ölüm |
| Meyers 2023 (37090101; 10.1016/j.jtocrr.2023.100482) | ECOG≥2 havuz: OS **3,3 ay**; TTF 1,4 ay (n=231) | (≥2 birleşik) | hastane-içi ölüm RR 2,7; ≥2 → %25 tedavide hastane-içi ölüm |
| PePS2 Middleton 2020 (32199466; 10.1016/S2213-2600(20)30033-3) | **prospektif PS2**: DCB %37; PFS 4,4 ay; OS 9,8 ay | — (PS3 yok) | grade3-5 TRAE %15; grade-5 yok; hiperprogresyon yok |
| CheckMate 171 Felip 2020 (32028209; 10.1016/j.ejca.2019.11.019) | PS2 OS **5,2 ay** (n=103) | — (uygunluk ≤PS2) | grade3-4 TRAE PS2 %6,8 |
| CheckMate 153 Spigel 2019 (31121324; 10.1016/j.jtho.2019.05.010) | PS2 OS **4,0 ay**; DoT 1,4 ay; ölüm %89 (n=128) | — | grade3-5 select TRAE PS2 %9 |
| PICASO Facchinetti 2025 (40382877; 10.1016/j.lungcan.2025.108580) | **prospektif gerçek-yaşam PS2**: PFS 1,6 ay; OS 2,8 ay; mono-IO 1-yıl OS %20 (n=198) | — | ~⅓ IO alanların ilk taramadan önce progresyon/ölüm |
| Banna LIPS 2021 (34939342; 10.1111/1759-7714.14256) | PS2+PD-L1≥50: 1-yıl OS %32,3; PFS 3,3 ay; LIPS-poor 1-yıl OS %10,7 (n=128) | — | steroid+NLR bağımsız kötü prognoz |

**Sentez B:** ECOG 3-4 → BSC'ye üstünlük **yok** (Ahmed OS 1,5 ay; Katsura HR 1,235 P=0,516) + prospektif kanıt yok. ECOG 2 heterojen: prospektif-seçili (PePS2 OS 9,8 ay) vs seçilmemiş gerçek-yaşam (PICASO OS 2,8 ay; Meyers 3,3 ay) — fayda PD-L1≥50 / düşük-inflamatuar / tümör-yükü-driven alt-gruba yoğunlaşır. *ECOG 3 base-case 0 hükmü tam-metinle güçlendi; ECOG 2 ≠ ECOG 3.*

---

## C. Kemoterapi-sonrası / 2L atezolizumab (DoT dağılımı)

| Çalışma (PMID/DOI) | Medyan DoT | PFS / OS | Kuyruk & TBP | ECOG 2 |
|---|---|---|---|---|
| OAK Rittmeyer 2017 (27979383; 10.1016/S0140-6736(16)32517-X) | **3,4 ay** (0–26) | PFS 2,8 ay; OS 13,8 vs 9,6 (HR 0,73) | **>12 ay %21** (125/609) vs %2; **TBP %40** medyan 3 döngü (1–34); DoR 16,3 ay | PS2 dışlanmış |
| POPLAR Fehrenbacher 2016 (26970723; 10.1016/S0140-6736(16)00587-0) | **3,7 ay** (0–19) | PFS 2,7 ay; OS 12,6 vs 9,7 (HR 0,73) | DoR 14,3 ay; ongoing %57 vs %24 | PS2 dışlanmış |
| TAIL Ardizzoni 2021 (33737339; 10.1136/jitc-2020-001865) | **3,2 ay** (0–18,6); 5 döngü | PFS 2,7 ay; OS 11,1 ay; 12-ay %47,8 | discontinuation %77,9 (PD %54,1) | **ECOG 2 n=61 (%9,9)** |
| TAIL-final Ardizzoni 2022 (36450379; 10.1136/jitc-2022-005581) | **3,15 ay** (0–42,3); 5 döngü (1–60) | PFS 2,7 ay; OS 11,2 ay; 3-yıl OS %19,6 | OAK-benzeri 3-yıl OS %25,4 | **ECOG 2 OS 3,5 ay; 3-yıl OS %3,6** (en düşük) |

**Sentez C:** atezolizumab medyan maruziyeti ~3,2–3,7 ay ama **belirgin >12-ay kuyruk** (OAK %21 vs docetaxel %2) + **TBP %40** (medyan 3, ≤34 döngü) + döngü aralığı 60'a/42 aya uzanır. **Sabit 3-aylık DoT savunulamaz.** ECOG 2 keskin uçurum (TAIL-final OS 3,5 ay). *Belgenin OAK/TAIL sayıları birebir; DoT dağılım-şekli argümanı doğru.*

---

## D. Evre III KRT + durvalumab — progresyon dinamiği (erken-nüks oranı · payda · pencere)

| Çalışma (PMID/DOI) | Kohort | Erken-progresyon metriği | Oran | Payda | Pencere |
|---|---|---|---|---|---|
| PACIFIC Antonia 2017 (28885881; 10.1056/NEJMoa1709937) | durva kolu | PD en iyi yanıt | %16,5 | 473 | 14,5-ay medyan izlem |
| PACIFIC 5-yıl Spigel 2022 (35108059; 10.1200/JCO.21.01308) | durva kolu | PD nedeniyle bırakma | %31,3 | 476 | ~5 yıl |
| PACIFIC-R Girard 2023 (36307040; 10.1016/j.jtho.2022.10.003) | gerçek-yaşam durva-başlayan | PD nedeniyle bırakma (medyan 4,9 ay) | %26,9 | 1399 | 23,5-ay izlem |
| **Park Kore 2025** (40386716; 10.21037/tlcr-2024-1112) | durva-devam-eden (≥6 ay) | **nüks ≤6 ay** | **%18,0** (40/222) | 222 (survivor-enriched) | **6 ay** |
| **Aslan İsrail 2025** (40662350; 10.1111/1759-7714.70130) | durva-tedavili | erken-nüks ≤6 ay (oran tablo-bağlı) | `unverified` | 141 | 6 ay |

**Ek tam-metin derinlik:**
- PACIFIC: PFS 16,8 vs 5,6 ay (HR 0,52); yeni-lezyon %20,4 vs %32,1; **yeni beyin-met %5,5 vs %11,0**; pnömonit any %33,9.
- Spigel 5-yıl: OS 47,5 vs 29,1 ay; 5-yıl OS %42,9 vs %33,4; **PD-L1 TC<1% OS HR 1,15 (fayda yok)**; **subsekant IO %12,6 (durva) vs %29,1 (plasebo)** ← sıralı-IO daralması; %49 durva 12 ayı tamamladı; retedavi 34/476 (%7,1).
- PACIFIC-R: gerçek-yaşam PFS 21,7 ay; medyan durva süresi **334,5 gün (11 ay)**; yalnız %19,8 >12 ay; pnömonit/ILD %17,9 (kalıcı bırakma %9,5).
- Park: PD-L1<1% erken-nüks ile ilişkili (P=0,02); PD-L1≥50 koruyucu (OR 0,303).
- Aslan: **N3 PFS 5,1 ay vs N0-2 15,2 ay (HR 2,09)**; PTV≥350cm³ PFS 16,2 vs 30,9 ay; **34/175 (%19,4) post-KRT PD → durvalumaba ulaşamadı.**

**Sentez D:** "İlk-6-ay %18–31 progresyon" YALNIZ durva-başlayan çapasında; post-KRT inflow olarak düşük tahmin eder (payda: KRT-başlayan vs KRT-tamamlayan vs durva-başlayan). **Zaman-sıfırı=RT bitişi** doğru (immortal-time). Sıralı-IO: durva→sonraki IO %12,6 (Spigel) + durvalumab KÜB birincil dışlaması ⇒ durvalumab-alan Evre III TEC havuzundan çıkar.

---

## E. Evre/histoloji epidemiyoloji (kayıt)

- **Cangır 2022 TR** (36192076; 10.1016/j.jtho.2022.06.001; **Minerva tam-metin**): 2017 ulusal kayıt (14 il, %50,2 kapsam): **NSCLC %79,6; adeno %47,7; skuamöz %36,8; SCLC %16,5**; kadında adeno %68,9; **>%50 ileri evre, ~%30 lokal ileri** tanıda (evre-split figür-bağlı `partial`); ~9.500 rezeksiyon/yıl; durvalumab onaylı-geri ödemesiz; EGFR 12,1–16,7%, KRAS %26, ALK 3,4–8,3%, ROS1 0,4–1,9%.
- **Flores 2021 SEER** (34919136; 10.1001/jamanetworkopen.2021.37508): NSCLC evre I/II %28,2 vs III/IV %69,5; **evre kayması 2006→2016 III/IV %70,8→%66,1**; adeno %52,2 (→%59); Evre III medyan OS 12 ay, Evre IV 5 ay.
- **Nations 2020** (`unverified`, abstract): SEER NSCLC evre IV %40,5 / III %26,4 / I %20,6.
- **Adizie NLCA 2019** (31514942; 10.1016/j.clon.2019.07.020): İngiltere Evre III n=6.276 (IIIA 3.827/IIIB 2.449); **aktif tedavi yok %36; palyatif %34; küratif %30; kemo+radikal RT %11 (676); yalnız %4 durvalumab yolundan yararlanabilir**; eş-zamanlı %34 vs ardışık %66 KRT.
- **Hosoya 2019** (31201490; 10.1007/s00280-019-03885-4): Evre III'ün %20–30'u NSCLC; **%30–50 rezekte-edilemez**; KRT sonrası PACIFIC-uygun %77 (63/82) / tüm 98'de %64; uygunsuzların en sık nedeni progresyon/ölüm (%10).
- **Boys 2023** (36627112; 10.1111/1759-7714.14780): KRT-alan 126'da durvalumab-uygun **%56 / uygunsuz %44**; tüm 234 Evre III'ün yalnız %30'u uygun; non-skuamöz %62, driver-yok %86.
- **Bhamani SUMMIT 2025** (40154514; 10.1016/S1470-2045(25)00082-8): LDCT taramada evre I/II %79,3 (vs İngiltere rutin %30); cerrahi %77 — tarama evre kaymasını gösterir.
- Socinski 2016 (27296106): NSCLC >%85; skuamöz NSCLC'nin ~%25-30'u.

**Sentez E:** TR histoloji çapası (Cangır): NSCLC ~%80, adeno ~%48, skuamöz ~%37. Evre III NSCLC'nin ~%20-26'sı; **rezekte-edilemez III'ün gerçekte pek azı definitif KRT + durvalumab yoluna girer** (İngiltere: yalnız ~%4 Evre III durvalumab-yararlı) → biyolojik Evre III sayısı PACIFIC havuzunu büyük oranda abartır.

---

## F. Moleküler/biyobelirteç epidemiyoloji (uygunluk filtreleri)

**Türkiye driver prevalansı (non-skuamöz zengin):**
- EGFR: **%16,7** (adeno %20,3) Güler Tezel n=959 (28832323; 10.4274/balkanmedj.2017.0297); **%9,3** Dülger n=501 (10.4103/ijpm.ijpm_939_23); %11,4 Çiçek (30582673); %32 outlier Demiray/pyrosequencing (30984520).
- ALK **%5,3** / ROS1 **%2,4** (Dülger); ALK %8 / ROS1 %1 (Çiçek).
- KRAS %25–31 (Demiray, Basdemirci `unverified`); G12C TR-özgü yok; global %10-13 non-sq (Lim 37683526).
- **Kombine EGFR/ALK/ROS1 pozitif ~%17 (Dülger non-sq) → driver-negatif (IO-uygun) >%80.**

**PD-L1 katmanları (TR):**
- Dülger 22C3 n=501 (10.4103/ijpm.ijpm_939_23): **<%1 %30,8 / 1-49% %41,7 / ≥50 %27,5** (≥1% %69,2); non-AC ≥1% %73,4 > AC %67,2.
- Teoman SP263 EGFR-mutant-only n=176 (40870512): ≥1% %48,3; ≥50 %25,9 (pozitiflerin).
- **EGFR-mutant ↔ PD-L1 düşük/negatif** (Dülger p=0,0002; Teoman ekson21 p=0,008) — driver-negatif havuz = PD-L1-zengin havuz.

**Bölgesel çapa (PD-L1≥50 — kapsamlı kıyas, bkz. enrichment §I):** TR all-comer 22C3 **~%27,5 (Dülger)** ≈ **global all-comer EGFR/ALK-WT ~%27** (EXPRESS, Dietel 2019, 18 ülke, 22C3; all-comer %22, bölgeler %21-24 tekdüze; 10.1016/j.lungcan.2019.06.012). Çin %32,8 (Shi 40413619), İsrail %35-37 (Apter 39512773); Canaslan **%17,8 alt uçtadır** (metastatik-only, klon-NR, driver-zengin payda — 10.3390/genes16121446). Elma-elmaya (22C3 / all-comer / EGFR-WT) **TR ≈ global**; görünürdeki "%18 vs %30" farkı payda/assay/case-mix artefaktı (SP142 22C3'ten az boyar — Blueprint 10.1016/j.jtho.2018.05.013; "%30" taranmış-zenginleştirilmiş pivotal çapa, gerçek all-comer ~%22). PD-L1≥%1 TR/global ~%50-52.

**Sentez F:** TR driver prevalansı Kafkas-benzeri (düşük), IO-uygun non-skuamöz fraksiyon büyük (~%80). Ancak driver-negatif havuz aynı zamanda 1L IO'ya yönlendiği için 2L IO-naif atezo havuzunu daraltır. **BP27 çarpanı (§I):** 1L atezolizumab PD-L1≥50 monoterapi (SUT c)2 / KÜB) hedefi = **EGFR/ALK-WT ileri NSCLC'nin ~%25-30'u** (TR %27,5 ≈ global EGFR-WT %27) — **%17,8 kullanmak 1L PD-L1-yüksek havuzu ~%35 küçümser.** 2L atezolizumab (c)3) için PD-L1 eşiği **yoktur** (§H.6); bu çarpan yalnız 1L monoterapi havuzunu ilgilendirir.

---

## G. Basamak atrisyonu + Türkiye gerçek-yaşam

**Atrisyon çarpanları (payda ile):**
- SEER de novo Evre IV Kehl (10.1002/cam4.2854; **Minerva**): tanı→1L **%50,2**; 1L-bırakan→2L **%34,6** (2015 %42,4); 2L→2L-IO **%16,2**; tedavisizlerin %91,5'i 1 yılda öldü.
- PIvOTAL 7-ülke (28748556; 10.1111/ecc.12734): 1L→2L **%46–71**; 2L→3L %17–42; beyin-met tanıda %13–27; ECOG≥2 ~%20.
- REFLECT EGFR Avrupa (35173817): 1L-bırakan %33 hiç 2L almaz; yalnız %57 2L'ye maruz; CNS %22 başta→%37 toplam.
- REFLECT-Yunanistan (35929414; **Minerva**): 2L-yok %43; 2L→3L-yok %56; beyin-met %31,9.
- Fung/Rittberg post-1L-pembro Kanada (10.3390/curroncol30060402): **progresörlerin yalnız %21'i 2L aldı** (KEYNOTE-024 %53'e karşı ~%60 daha az); ECOG 0-1 %21 vs ≥2 %10; OS 2L+ 22,2 vs BSC 5,6 ay.
- Bauman ALK Flatiron (39197358): 1L-bırakan→2L %56; **%44 2L-yok; %22 2L öncesi öldü** (medyan 4,0 ay); 2L→3L-yok %49.

**Türkiye gerçek-yaşam:**
- İzmir Yavuz (40165351; **PMC**): **ECOG 0 %43,4 / 1 %34,3 / 2 %21,2**; evre IV %80,6; nivolumab 2L %99 (SGK: atezo 1L, nivo 2L — *kohort dönemi; **10/07/2025 SUT değişikliğiyle atezolizumab 2L de geri-ödemeli oldu**, bkz. aşağıdaki GÜNCELLEME + sentez Eksen 5 / enrichment §H.6*); PD-L1 ulaşıldı %54.
- TOG Alan 2L nivolumab n=196 (40731790; **PMC**): PFS **4,2 ay**; OS 12,4 ay; erkek %85,2; evre IV tanıda %50,5; PD-L1≥1% %35,2.
- Kilickap registry n=244 (`unverified`, abstract): 2L 1-yıl PFS %31,2 vs 3L %21,3; ORR %34,7 vs %27,3; bırakma-progresyon %57,4/%66,0.
- Kapagan İstanbul n=148 (`unverified`, abstract): PFS 5,3 ay; OS 15,8 ay.
- EMPOWER-Lung 1 TR-liderli BM alt-grubu (40323717; **PMC**): PD-L1≥50'de BM %12,2; 1L cemiplimab OS 52,4 vs kemo 20,7; kaynak: ileri NSCLC'nin ~%26'sı tanıda BM.

**Sentez G:** biyolojik progresyon havuzu → 2L ticari havuza ~yarıya iner (SEER ×0,45); 1L IO progresörlerinde ~%21'e düşer. Türkiye-lokal 2L IO çapası = nivolumab PFS 4,2–5,3 ay, ECOG≥2 ~%21; TR IO DoT ve durvalumab-PACIFIC gerçek-yaşam kohortu **yok** (uluslararası ödünç).

> **GÜNCELLEME (2026-07-27, TR birincil regülatif kapanış — enrichment §H.6):** Yukarıdaki TR gerçek-yaşam
> kohortları (İzmir/TOG Alan/Kilickap) **amendman-öncesi** SGK ortamını (2L IO = nivolumab) yansıtır. **SUT
> 10/07/2025 (RG 32952) 4.2.14.C yeni fıkra(3)** birincil metni (host-PDF + OCR, bütünlük PASS) ile durum
> değişti: **2. basamak metastatik KHDAK'de artık hem atezolizumab (c)3: ECOG 0-1, önceki 1-2 basamak kemo +
> progresyon, EGFR/ALK/ROS-neg, PD-L1 eşiği yok, ardışık-IO dışlaması) hem nivolumab (a)14) GERİ ÖDEMELİ**;
> **durvalumab Evre III (ç)2: PD-L1≥%1, KRT sonrası progresyonsuz, ≤12 ay)** ve atezolizumab 1L PD-L1≥50 (c)2)
> da SUT'a eklendi. → Atezolizumab 2L **hem ruhsatlı (KÜB) hem SGK geri-ödemeli**; "yalnız nivolumab" tezi
> 10/07/2025 itibarıyla geçersiz. Tüm ajanlarda **ardışık/önceki-IO dışlaması** (1L-IO veya durvalumab almış
> hasta sonraki basamakta IO geri-ödemesi alamaz) → 2L IO-naif TEC havuzunu daraltan asıl mekanizma budur.

---

## H. Tam-metin derinliğinin `problem.md` değerlendirmesine kattıkları

1. **DoT argümanı** artık RCT+RWE landmark on-treatment eğrileriyle (24-ay %22; ≥35 döngü %14-26; TBP %40) tam desteklenir — medyan≠maruziyet ve sabit-DoT-yanlışı kesinleşti.
2. **ECOG 3** — tam-metin ECOG 2/3 ayrımını netleştirdi (Ahmed PS3 OS 1,5 ay; Katsura PS3-4 BSC'ye üstün değil, HR 1,235); ECOG 2 fayda-alt-grubu (PD-L1≥50/LIPS-favorable) belgelendi.
3. **Evre III havuzu** — İngiltere NLCA tam-metni "yalnız ~%4 Evre III durvalumab-yararlı" + Hosoya/Boys post-KRT %23-44 uygunsuzluk → biyolojik Evre III ≫ PACIFIC/TEC havuzu (belgenin tezini niceliksel doğrular).
4. **Sıralı-IO daralması** — PACIFIC 5-yıl subsekant-IO %12,6 vs %29,1 + durvalumab KÜB birincil dışlaması ⇒ up-front IO downstream IO havuzunu ~yarılar (Fung: progresör→2L %21).
5. **TR epidemiyoloji** — Cangır tam-metni ulusal histoloji %'lerini (NSCLC %79,6/adeno %47,7) doğruladı; ulusal evre-split hâlâ figür-bağlı `partial`.

## I. Kalan boşluklar ve kapatma yolu (2026-07-27 güncellendi)
- ✅ **ÇÖZÜLDÜ (host-PDF):** Nations (10.1093/milmed/usaa218), Basdemirci (10.4103/ijc.IJC_766_19), Kilickap
  (10.1080/03007995.2024.2359026) tam-metin + Kapagan abstract (EBSCO) — kullanıcı host-PDF'leriyle
  bütünlük-kontrollü ingest edildi (enrichment §G). **Kalan tek abstract-only: Midha 2015 (PMID 26609494,
  DOI-siz PMC).**
- ✅ **ÇÖZÜLDÜ (host-PDF + OCR):** TR birincil regülatif metin — TİTCK KÜB (atezo/durva) + SUT 10/07/2025
  (RG 32952) 4.2.14.C fıkra(3); atezolizumab 2L + durvalumab Evre III geri-ödeme birincil doğrulandı (§H).
- Türkiye ulusal evre-tanı dağılım tablosu (HSGM Türkiye Kanser İstatistikleri PDF) → hâlâ birincil PDF gerek;
  ancak IJC 2026 (10.1002/ijc.70628) akciğer 5-yıl sağkalımını (<%15) L2 ile ekledi (§G.5).
- Türkiye durvalumab-PACIFIC gerçek-yaşam kohortu + TR IO DoT eğrisi → literatürde hâlâ yok (yerel MEDULA/EHR gerek);
  ESTIMATE (TR 1L pratik) + Canaslan (TR klinikogenomik) L2 ile 1L tarafı kısmen çapalandı (§G.1–G.2).

---
*Bu dosya, `problem.md` değerlendirmesinin tam-metin kanıt tabanıdır. Sayılar `04_extraction/` çıkarım-CSV'sine ve `06_synthesis/` sentezine izlenebilir; abstract-only değerler açıkça `unverified` işaretlidir.*
