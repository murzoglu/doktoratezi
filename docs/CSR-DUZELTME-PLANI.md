# CSR-FINAL — Madde-Madde Düzeltme Planı

**Hedef belge:** `docs/CLINICAL-STUDY-REPORT-FINAL.md`
**Üretim:** Tamlık + tutarlılık + bütüncüllük sertifikasyon denetimi → kanıt çıkarımı (6 ajan) → sentez → adversaryal doğrulama → editör spot-kontrolü.
**Durum:** Sertifikasyon HENÜZ verilemez. **8 majör bulgu (B1–B8) → 30 bloke alt-madde**; **12 minör bulgu → 20 alt-madde**. Her sayısal düzeltme gerçek kaynak `outputs/tables/*.csv` / `outputs/models/*` hücresine kadar doğrulandı.

## Nasıl kullanılır
Her madde: **Konum · Mevcut (find-anchor) · Düzeltme (kaynaklı) · Kaynak · Aksiyon · Efor**. `BLOKE` = sertifikasyonu engeller. `NEEDS-AUTHOR` = değer doldurulabilir ama bir karar/teyit yazara ait. Önce P01 (kod yeniden-üretim), sonra §13/§9 sayı tabloları, sonra atıf/tamlık, en son cilalama (önerilen sıra §6).

## ⚠️ Doğrulama notu — plana işlenen iki düzeltme
- **P48 (LPA-BIC) İPTAL.** `lpa_fit_indices.csv`: 3-sınıf BIC=3951,29 **gerçek minimum** (5-sınıf 3971,64 daha yüksek). Raporun "BIC en uygun 3-profil" iddiası **doğru**; değiştirilmemeli. (İsteğe bağlı: BLRT 4-sınıf p=.2475 + entropy 0,81 destekleyici kanıt olarak eklenebilir.)
- **P20 (§13.3) düzeltildi.** Gerçek `robust_sensemakr_evalue.csv`: RV_q=0,0606/0,0418/0,0798/0,0553 (raporun "0,04–0,08"ı doğru), RV_qa=0, partial_r2=0,0039/0,0018/0,0069/0,0032. Tek hatalar: yanlış "H1" etiketi + eksik 2 satır + aşırı koruma E-CI 1,10→1,58.

---

# BÖLÜM 1 — SERTİFİKASYONU BLOKE EDEN DÜZELTMELER

## B3 — H5 diadik tutarlılık: "≥3 strateji uyumlu" iddiası SAĞLANMADI (en kritik)

> **Bilimsel sonuç:** Yön düzeyinde DM>Kontrol yalnız **tek** stratejide (S4 Olsen-Kenny latent r, sadece reddetme, **zayıf DM-grup fit**: RMSEA 0,120 / SRMR 0,254) gözlenir. S1 (ICC) **4/4 ters yön** (Kontrol>DM); S5 (k) gruba ayrılmamış; S2 (RSA) tekil uyum skoru üretmez; S3 (CFM) reddetmede yakınsamamış. **"Metodolojik triangülasyon" şartı yerine gelmemiştir** — bulgu tek-strateji, tek-alt-ölçek sinyalidir. Bu, §2.3 / §11.5 / §15.6 / §17.2 / §19.1'i (Makale-1 birincil katkı konumlandırması dâhil) zincirleme etkiler (bkz. §5 Cascade).

| ID | Konum | Mevcut | Düzeltme | Kaynak | Aksiyon · Efor |
|---|---|---|---|---|---|
| **P01** | §11.5 tüm sayısal tablo | Değerler `phase2_h5ext_strategy_estimates.csv`'ten (source sütunu = "CSR §11.5 raporlanan degerler" — geri-besleme) | §11.5 tablosunu **gerçek model çıktılarından yeniden kur**: ICC→`h5_icc_bland_altman.csv`; latent r→`h5_dyadic_cfa_latent_corr.csv`(+fit); k→`h5_k_coefficient.csv`; CFM→`h5_common_fate_regressions.csv`(+fit); RSA→`h5_rsa_parameters.csv`(+status). Her stratejinin kapsamı (alt ölçek/grup) ve yakınsama durumu metinde açık. | geri-beslenmiş CSV **kullanılmaz** vs gerçek `h5_*.csv` | **yeniden-üret-kod · yüksek** |
| **P02** | §11.5.7 L727 | "Strateji 1 (manifest ICC) … DM<Kontrol" yön paketlemesi | **S1 ICC anne–indeks düad: 4/4 Kontrol>DM.** sıcaklık K 0,145/DM 0,027; aşırı koruma K 0,204/DM 0,009; **reddetme K 0,029/DM −0,006**; karşılaştırma K 0,103/DM 0,084. Hiçbir alt ölçekte DM>Kontrol değil (0/4). | `h5_icc_bland_altman.csv` (dyad=anne_idx) | sayı-değiştir · orta |
| **P03** | §11.5.4 L699-707 + §11.5.7 | "Havuzlanmış 0,19 / Kontrol 0,17 / DM 0,29 … fark 0,12" | true_concordance: **0,189 / 0,173 / 0,290; fark 0,117**. **UYARI ekle:** DM-grup fit zayıf (RMSEA=0,120; SRMR=0,254; CFI=0,984; χ²(15)=40,81, p<.001) → latent r kırılgan/aşırı-uyum riskli, tek alt ölçekle (reddetme) sınırlı. | `h5_dyadic_cfa_latent_corr.csv` + `..._fit_measures.csv` | ifade-yeniden-yaz · orta |
| **P04** | §11.5.5 L711 + §11.5.7 | "Strateji 5 (k) yön açısından Olsen-Kenny ile uyumlu" | **S5 k yalnızca havuzlanmış**; gruba ayrılmış k YOK → DM-vs-Kontrol yön oyu vermez. Havuzlanmış k: sıcaklık 1,01 [−7,03; 22,53]; aşırı 0,−16 [−0,95; 1,16]; reddetme −0,19 [−0,82; 1,68]; karşıl. 0,08 [−3,20; 11,86] (tüm GA'lar sıfırı kapsar). "Yön uyumu" iddiası kaldırılmalı. | `h5_k_coefficient.csv` (group kolonu yok) | ifade-yeniden-yaz · orta |
| **P05** | §11.5.3 L695 + §11.5.7 | "Dört alt ölçekte CFM grup yordayıcısı anlamsız sınırda" | **S3 CFM: reddetme YAKINSAMADI (Heywood)** — group_dm β=−0,051 ama SE=NA, p=NA, tüm fit NA → yorumlanmaz. Yakınsayan üçte group_dm: sıcaklık +0,026 (p=.49); **aşırı koruma +0,185 (p=.044, tek anlamlı)**; karşıl. +0,100 (p=.26). | `h5_common_fate_regressions.csv` + `..._fit_measures.csv` | etiket-düzelt · orta |
| **P06** | §11.5.2 L691 + §11.5.7 | "a1–a4 parametreleri … RSA yön düzeyinde Olsen-Kenny ile hizalı" | **S2 RSA yalnız sıcaklık+reddetme** (aşırı koruma/karşıl. YOK); n: pooled 238/Kontrol 121/DM 117. RSA **tekil uyum skoru üretmez** → yön oyu sayılamaz. Parametre seti **a1–a5 + b0–b5** (a1–a4 değil). Reddetme a4: pooled −13,96 (p=.012)/Kontrol −15,93 (p=.064)/DM −7,07 (p=.43). | `h5_rsa_parameters.csv` + `h5_rsa_status.csv` | ifade-yeniden-yaz · orta |
| **P07** | §11.5.7 L729 **+ §11.5.8 Karar Kutusu** | "'en az üç strateji uyumlu' kuralı (DM>Kontrol) sağlanmıştır" | **"En az 3 strateji DM>Kontrol" kuralı SAĞLANMAMIŞTIR.** Gerçek yön oyu en fazla 1 (S4, reddetme, zayıf fit). S1 ters (0/4), S5 yön vermez, S2 skor üretmez, S3 reddetme NA. Karar Kutusu da bu tek-strateji sinyaline göre yeniden yazılmalı; **"zayıf-orta yön kanıtı" ifadesi düşürülmeli** ("triangülasyon şartı sağlanmadı; bulgu çok-zayıf/belirsiz"). | tüm `h5_*.csv` çapraz | ifade-yeniden-yaz · yüksek |

## B1 — Sensitivite üçlüsü "tüm birincil bulgular" aşırı-iddiası

> Confirmatory üçlü (multiverse+TOST+sensemakr) **yalnız H3/EMBU-P**'ye uygulanmış. H1/EMBU-C sadece post-hoc [KEŞİFSEL]; H2/SRQ ve H4/SEM kapsam dışı.

| ID | Konum | Mevcut | Düzeltme | Kaynak | Aksiyon · Efor |
|---|---|---|---|---|---|
| **P18** | §2.2 L48 + §8.11 L383 | "Birincil bulguların **tamamı** için sensitivite üçlüsü … zorunlu uygulanmıştır" | Confirmatory üçlü **yalnız H3 (4 EMBU-P, n=241)**'e; sensemakr/E yalnız embu_p satırları. H1/EMBU-C yalnız **post-hoc keşifsel** multiverse + Bayes. **H2/SRQ ve H4/SEM kapsam dışı.** §8.11 cümlesi de H3'e daraltılmalı. | `robust_sensemakr_evalue.csv` (4 satır embu_p); `robust_target_summary.csv` | ifade-yeniden-yaz · orta |
| **P19** | §2.2 L386 + §13.1 L820 | Multiverse "dört outcome … birincil hipotezler için" | **Confirmatory multiverse=120 spec, tümü EMBU-P/H3.** Post-hoc AYRI: H1/EMBU-C 120 spec, H4 16 spec, "[KEŞİFSEL – POST-HOC]". **H2 hiçbir multiverse'te yok.** Kapsam matrisi açıkça yazılmalı. | `robust_multiverse_summary.csv`; `phase2_multi_target_summary.csv` (h1=120/h4=16) | tablo-doldur · orta |
| **P20** | §13.3 L838-841 tablo + L838 metin | "\| H1 reddetme \| 0,08 \| 1,59 \| 1,36 \|" ve "\| H3 birincil \| 0,04 \| 1,36 \| **1,10** \|"; "RV_q=0,04–0,08" | **"H1" etiketi yanlış — kaynak satır embu_p (H3); H1/EMBU-C sensemakr YOK.** Tabloyu **4 gerçek H3 satırı** yap (RV_q raporun doğru sütunu): H3 sıcaklık RV_q 0,06 / E 1,49 / E-CI **1,50**; H3 aşırı koruma 0,04 / 1,36 / **1,58**; H3 reddetme 0,08 / 1,59 / **1,38**; H3 karşıl. 0,06 / 1,45 / **1,52**. **"1,10" uydurma → 1,58.** "RV_q 0,04–0,08" **doğru, korunur** (RV_qa değil). | `robust_sensemakr_evalue.csv`: RV_q 0,0606/0,0418/0,0798/0,0553; E_point 1,489/1,359/1,590/1,449; E_ci 1,503/1,579/1,382/1,524 | etiket-düzelt · orta |
| **P21** | §13.2 + §2.2 L385 | TOST "her birincil etki için" | Confirmatory TOST yalnız **4 EMBU-P/H3**: sıcaklık=Indeterminate (.081), aşırı=Equivalent (.030), reddetme=Indeterminate (.110), karşıl.=Equivalent (.041). **H1/EMBU-C ve H2/SRQ için confirmatory TOST yok.** | `robust_tost_equivalence.csv` | ifade-yeniden-yaz · orta |

## B2 — §13.1 multiverse reddetme aralığı + "ispat" dili

| ID | Konum | Mevcut | Düzeltme | Kaynak | Aksiyon · Efor |
|---|---|---|---|---|---|
| **P22** | §13.1 L820 | "median d=−0,13 (%5–%95 aralığı **[−0,30; 0,05]**) … ihmal edilebilir kaldığını **ispatlamaktadır**" | Aralık **[−0,185; −0,058]** (29 spec'in %100'ü negatif, %0 p<.05; üst sınır sıfırın altında). **"ispatlamaktadır" → "göstermektedir".** Diğer 3 outcome pct_positive=1: sıcaklık 0,13 [0,089;0,144]; aşırı 0,10 [0,046;0,135]; karşıl. 0,085 [0,068;0,111]. | `robust_multiverse_summary.csv` (reddetme median −0,1317/q05 −0,1853/q95 −0,0578) | sayı-değiştir · orta |

## B5 — Tablo 1A/1C boş grup hücreleri (+ iki yanlış SMD)

| ID | Konum | Mevcut | Düzeltme | Kaynak | Aksiyon · Efor |
|---|---|---|---|---|---|
| **P08** | Tablo 1A L422 | Anne eğitim "— / — / 0,29" | Modal: Kontrol düzey 3 (%34,7) · DM düzey 1 (%30,8). Tam dağılım dipnotta (DM 7/37/28/26/18/4; Kontrol 6/28/23/42/18/4). SMD 0,29 doğru. | `table1_family_summary.csv`; `table1_smd_balance.csv` (abs_smd 0,293) | tablo-doldur · düşük |
| **P09** | Tablo 1A L423 | Eş eğitim "— / — / 0,32" | Kontrol mod düzey 3 (%35,5) · DM düzey 1/3 (%28,3). Dağılım dipnotta. SMD 0,32 (düzey 5) doğru. | `table1_family_summary.csv` (es_egitim) | tablo-doldur · düşük |
| **P10** | Tablo 1A L424 | Aile ISEI-08 "— / — / 0,23" | **Kontrol 31,35 · DM 34,49** (ort.; SD 14,83/12,50; n=219, eksik=22 dipnot). SMD 0,23 doğru. | `table1_family_summary.csv` (aile_isei08) | tablo-doldur · düşük |
| **P11** | Tablo 1A L425 | Eş ISEI-08 "— / — / 0,23" | Kontrol 31,35 · DM 34,49. **UYARI (NEEDS-AUTHOR):** kaynakta `es_isei08` ≡ `aile_isei08` birebir aynı → türetme/eşleme hatası olası; gerçek eş ISEI ayrı hesaplanmalı. | `table1_family_summary.csv` (es_isei08) | tablo-doldur · orta |
| **P12** | Tablo 1A L428 | Ev sahipliği "— / — / **0,07**" | Kontrol %46,3 (56/121) · DM %45,0 (54/120). **SMD 0,07 YANLIŞ → 0,03.** | `table1_smd_balance.csv` (abs_smd 0,0257) | tablo-doldur · düşük |
| **P13** | Tablo 1A L429 | Araba sahipliği "— / — / **0,11**" | Kontrol %44,6 (54/121) · DM %51,7 (62/120). **SMD 0,11 YANLIŞ → 0,14.** | `table1_smd_balance.csv` (abs_smd 0,1412) | tablo-doldur · düşük |
| **P14** | Tablo 1A L430 | Ev oda sayısı "— / — / 0,08" | Kontrol 1,72 · DM 1,67 (ort.; SD 0,64/0,60; n=240). SMD 0,08 doğru. | `table1_family_summary.csv` (ev_oda_sayisi) | tablo-doldur · düşük |
| **P15** | Tablo 1C L449 | Beck şiddet kategorisi "— / — / 0,11" | Kontrol mod Minimal (%40,5) · DM mod Hafif (%35,9). Dağılım dipnotta; n=238 (eksik=3). SMD 0,11 doğru. | `table1_family_summary.csv` (beck_severity) | tablo-doldur · düşük |
| **P16** | Tablo 1C L450 | Eş çalışma durumu "— / — / 0,14" | Kontrol %95,9 (116/121) · DM %92,5 (111/120). SMD 0,14 doğru. | `table1_family_summary.csv` (es_calisma) | tablo-doldur · düşük |

## B7 — §9.4 tanı yaşı strataları

| ID | Konum | Mevcut | Düzeltme | Kaynak | Aksiyon · Efor |
|---|---|---|---|---|---|
| **P17** | §9.4 L478 | "erken 22 / okul 64 / ergen 34" | **erken (<5y)=24 · okul (5–10y)=69 · ergen (≥10y)=27** (toplam 120). | `dm_strata_descriptive.csv` | sayı-değiştir · düşük |

## B4 — Üç kırık Türkiye-özgü atıf (PubMed PMID/DOI ile doğrulandı)

| ID | Konum | Mevcut | Düzeltme | Kaynak | Aksiyon · Efor |
|---|---|---|---|---|---|
| **P23** | Kaynakça L1359 (atıf §6.1 L183) | "Yeşilkayalı, E., & Başal, H. A. (2017). Anne-baba tutumları… derleme." | **Yeşilkaya, E., Cinaz, P., Andıran, N., … Craig, M. E. (2017). First report on the nationwide incidence and prevalence of Type 1 diabetes among children in Turkey. *Diabetic Medicine*, 34(3), 405–410.** DOI 10.1111/dme.13063. Metin-içi "Yeşilkaya ve diğerleri, 2017" **doğru, değişmez.** | PMID 26814362; prevalans 0,75/1000 (GA 0,74–0,76) | atıf-düzelt · düşük |
| **P24** | §6.1 L183 + Kaynakça L1357 | "Vuralli ve diğerleri, 2024" (insidans 13,1/100.000); ref = parenting review | Metin-içi → **"Dündar ve diğerleri, 2023"**. Ref: **Dündar, İ., Akıncı, A., Çamtosun, E., … (2023). Type 1 diabetes incidence trends in a cohort of Turkish children and youth. *Turkish Archives of Pediatrics*, 58(5), 539–545.** DOI 10.5152/TurkArchPediatr.2023.23036. **L476'daki "Vuralli 2024" de gözden geçirilmeli.** (NEEDS-AUTHOR: tek-il/Malatya kohortu; yazarın niyetlediği atıf teyit edilmeli.) | PMID 37670553; 13,1/10⁵ çocuk-yılı, AAPC %8,3 | atıf-düzelt · orta |
| **P25** | §8.3.1 L271 + Kaynakça L1355 | "Sümer, Gündoğdu-Aktürk ve Helvacı, 2010"; ref = Sümer & Güngör bağlanma makalesi | Metin-içi → **"Dirik, Yorulmaz ve Karancı, 2015"**. Ref: **Dirik, G., Yorulmaz, O., & Karancı, A. N. (2015). … S-EMBU'nun çocuk formunun Türkçe uyarlaması. *Türk Psikiyatri Dergisi*, 26(2), 123–130.** **NEEDS-AUTHOR:** (1) Dirik et al. 3 boyut doğrular — 4. "karşılaştırma" boyutunun kaynağı; (2) EMBU-P (ebeveyn formu) için ayrı uyarlama kaynağı gerekebilir. | PMID 26111288 | atıf-düzelt · orta |

## B6 — §9.1 STROBE katılımcı akışı

| ID | Konum | Mevcut | Düzeltme | Kaynak | Aksiyon · Efor |
|---|---|---|---|---|---|
| **P26** | §9.1 L409-411 | "241 aile dahil edilmiştir…" (akış sayısı yok) | Mevcut korunur + STROBE akış cümlesi: dahil-kriteri, anne onamı + 7–17 yaş muvafakati, **482 çocuk satırı (DM-İndeks 120, DM-Kardeş 120, Kontrol-İndeks 121, Kontrol-Kardeş 121)**. **[NEEDS-AUTHOR: taranan/uygun/reddeden/eksik-veri ile dışlanan aile sayıları kaynak kayıtlardan.]** | `FINAL_REFERENCE…lock` (241/482); protokol | bölüm-ekle · orta |

## B8 — BDI eşiği üç farklı tanımlı → tek kanona (≥17) bağla

| ID | Konum | Mevcut | Düzeltme | Kaynak | Aksiyon · Efor |
|---|---|---|---|---|---|
| **P27** | §8.3.3 L279 | "17 ve üzeri en az hafif, 21 orta…" | Kanonik tek eşik: **≥17 = klinik anlamlı depresif belirti (Hisli 1989 TR norm)**. L787'deki "17=moderate" çelişkisi giderilir; alt-bant etiketleri standardize değilse kaldırılır; **"14" TR normu değil.** | Hisli 1989; CSR iç tutarlılık (NEEDS-AUTHOR kanon onayı) | ifade-yeniden-yaz · orta |
| **P28** | Y4 L240 | "Beck total ≥ 17" | **≥17 KORUNUR** (kanon). Diğer konumlar buna hizalanır. | — | sayı-değiştir · düşük |
| **P29** | §17.3 L1016 | "BDI **≥ 14**" | **→ BDI ≥ 17 (Hisli 1989 TR normu).** | — | sayı-değiştir · düşük |
| **P30** | §12.4 L787 | "Beck ≥ 17, **'moderate depresyon' eşiği**" | ≥17 korunur; "(moderate)" alt-bant → **"(Hisli 1989 TR norm; klinik anlamlı eşik)"**. | — | ifade-yeniden-yaz · düşük |

---

# BÖLÜM 2 — MİNÖR DÜZELTMELER

| ID | Konum | Mevcut | Düzeltme | Kaynak | Aksiyon · Efor |
|---|---|---|---|---|---|
| **P31** | §11.3.1 L594 | Başlık "Standardize β / %95 GA" | **"Ham (standardize olmayan) β / %95 GA (ham)"** — basılan değerler `estimate`/ham GA, std_beta değil. (H4 tablosu da ham → ikisi de "ham".) | `h3_primary_group_effects.csv` | etiket-düzelt · düşük |
| **P32** | §11.3.1 L596 | Sıcaklık "0,07" | **0,06** [−0,07; 0,20] (estimate 0,0648). | aynı CSV | sayı-değiştir · düşük |
| P33 | §11.3.1 L597 | Aşırı koruma 0,06 | **Değişmez** (0,0603); yalnız başlık (P31). | aynı | — |
| **P34** | §11.3.1 L598 | Reddetme GA üst "0,03" | **0,02** (ham ci_high 0,0249). | aynı | sayı-değiştir · düşük |
| P35 | §11.3.1 L599 | Karşıl. 0,06 | **Değişmez** (0,0614). | aynı | — |
| **P36** | §11.3.1 L601 + §11.3.6 L635 | "standardize Cohen d \|d\|<0,17" | Tablo "ham" olunca → **"\|β_std\|<0,17"** (std_beta 0,125/0,080/−0,163/0,111; max 0,163<0,17 → iddia geçerli). | `h3_primary_group_effects.csv` (std_beta) | ifade-yeniden-yaz · düşük |
| **P37** | §11.4.2 L654 | Başlık "%95 GA (standardize)" | **"%95 GA (standardize olmayan)"** — kaynakta std.all için GA yok; basılan GA ham. | `h4_latent_sem_structural_paths.csv` | etiket-düzelt · düşük |
| P38-P41 | §11.4.2 L656-659 | β −0,28/0,08/0,33/0,28 + GA | **β (std.all) korunur**; GA'lar ham olarak etiketlenir (P37). p değerleri doğru. | aynı CSV | etiket-düzelt · düşük |
| **P42** | §14.1 L861 | "0,18 \| [0,05;**0,30**] \| 0,999 \| **%4** \| 8,12" | **"0,16 \| [0,05;0,26] \| 0,999 \| %12,7 \| 8,12"** — estimate 0,158, ci_hi 0,2586, rope_pct 0,127. | `bayes_h1_posterior.csv` | sayı-değiştir · düşük |
| **P43** | Ek A L1428-1435 | Madde sayıları sıcaklık 6 / aşırı 9 / karşıl. 6 | **sıcaklık 9 / aşırı 7 / karşıl. 5** (reddetme 8 sabit; toplam 29). EMBU-C aynı. | `psychval_reliability.csv` (n_items) | tablo-doldur · düşük |
| **P44** | Ek F.2 L1555 | "**113** CSV" | **114 CSV** (disk + kategori satır toplamı). (NEEDS-AUTHOR: 2.594 satır toplamı teyidi.) | disk sayımı | sayı-değiştir · düşük |
| **P45** | §10.1 L497 | EMBU-C reddetme **n=479** | Dipnot ekle ("3 satır tam-eksiklik nedeniyle düştü") **veya** 482'ye düzelt. (NEEDS-AUTHOR: 3-satır farkının nedeni.) | `psychval_reliability.csv` (n_complete=479) vs lock 482 | sayı-değiştir · düşük |
| **P46** | §12.1/12.2/12.3/12.4 başlıkları | İnline [KEŞİFSEL] yok | Her §12 alt-başlığına **"[KEŞİFSEL / İKİNCİL — doğrulayıcı değil]"** ekle (§18 ile tutarlılık). İçerik değişmez. | CSR §18 deseni | etiket-düzelt · düşük |
| **P47** | §11.4.3 L665 | "item collapse … sapma tablosunda belgelenmiştir" | İbareyi kaldır **veya (tercih)** `02-sapma-tablosu.md`'ye satır ekle. Şu hâliyle iddia yanlış (kayıt yok). | `02-sapma-tablosu.md` | ifade-yeniden-yaz · düşük |
| ~~P48~~ | ~~§12.2 L757~~ | ~~"BIC en uygun 3-profil"~~ | **İPTAL — rapor DOĞRU** (3-sınıf BIC 3951,29 = minimum). İsteğe bağlı: BLRT 4-sınıf p=.2475 + entropy 0,81 ekle. | `lpa_fit_indices.csv` | **değiştirme** |
| **P49** | §17.1 L996 | "Pinquart (**2017**)" kronik-hastalık | **(2013)** — kronik-hastalık meta 2013'tür (L185/L857/L894 zaten 2013). | PMID 23660152 | atıf-düzelt · düşük |
| **P50** | §12.1 L747 | a-yolu p=.033; b-yolu p=.19 | **a p=.0246; b p=.142** (yön/sonuç değişmez). | `mediation_simple_effects.csv` | sayı-değiştir · düşük |
| **P51** | §9.4 L476 | Hedefte "%18" | **%20,5 (8/39)** + dipnot: "yüzdeler HbA1c'si tescilli 39 DM-indeks üzerinden". %33/%49 bantları da 39 paydası üzerinden teyit. | `phase2_hba1c_dm_summary.csv` (n_under_7=8/39) | sayı-değiştir · orta |
| **P52** | §3 | AVE/CR/HTMT/NRI/IDI tanımlı-kullanılmamış; ISCO-08/TLI kullanılmış-tanımsız | Kullanılmayanları çıkar; **TLI = Tucker-Lewis İndeksi** ekle; ISEI-08 vs ISCO-08 ayrımını netleştir (Tablo 1A ISEI-08 → ISEI doğru). | CSR §3 + gövde | etiket-düzelt · düşük |

---

# BÖLÜM 3 — YAZAR GİRDİSİ GEREKEN (NEEDS-AUTHOR)

1. **P11** — `es_isei08 ≡ aile_isei08` birebir özdeşliği: veri-türetme hatası şüphesi; gerçek eş ISEI dağılımı ayrı hesaplanmalı. *(Veri bütünlüğü — potansiyel ek bulgu.)*
2. **P24** — Dündar 2023 doğru ama tek-il (Malatya) kohortu; yazarın niyetlediği bölgesel insidans atfı teyit.
3. **P25** — s-EMBU 4. "karşılaştırma" boyutunun ve ebeveyn-formu uyarlamasının kaynağı.
4. **P26** — taranan/uygun/reddeden/eksik-veri aile akış sayıları (kaynak kayıtlar).
5. **P27** — Hisli 1989 kesme puanı + alt-bant kanonu sabitlenmeli.
6. **P44** — 2.594 satır toplamı doğrulaması.
7. **P45** — 479 vs 482 (3 satır) farkının nedeni.
8. **P51** — HbA1c %33/%49 bantlarının 39 paydası üzerinden kesin sayıları.
9. **P52** — ISEI-08 vs ISCO-08 ayrımı + kullanılmayan kısaltma kararı.

---

# BÖLÜM 4 — KOD YENİDEN-ÜRETİM GEREKEN

- **P01** — `§11.5` H5 beş-strateji tablosu `phase2_h5ext_strategy_estimates.csv` geri-beslemesi terk edilip **gerçek `h5_*.csv` model çıktılarından** yeniden kurulmalı (ICC/latent-CFA/k/CFM/RSA + fit indeksleri + kapsam/yakınsama durumu). P02–P07 sayısal değerleri bu yeniden-kurmadan doğrudan oturur. *(Yeni R çıktısı değil — mevcut `h5_*.csv` hücreleri zaten var; tabloyu doğru kaynaktan yeniden derlemek yeterli.)*

---

# BÖLÜM 5 — H5 DÜŞÜRÜLDÜĞÜNDE ZİNCİRLEME GÜNCELLENECEK BÖLÜMLER (Cascade)

H5 "zayıf-orta yön kanıtı" → "triangülasyon şartı sağlanmadı / tek-strateji sinyali" düzeltmesi (P07) şu konumları **zorunlu** etkiler:

- **§2.3 Sinopsis** H5 satırı (L58) — karar metni güncelle.
- **§2.4 Genel Yargı** — H5'e dayanan diadik kopukluk anlatısı yumuşatılmalı.
- **§11.5.8 Karar Kutusu** (P07).
- **§15.6 H5 Tartışması** (L944-957) — "yön düzeyinde fark / metodolojik önem" çerçevesi.
- **§17.2 Çıkarımlar** H5 maddesi (L1008).
- **§19.1 Makale-1** (L1276-1282) — "H5 beş-strateji triangülasyonu birincil metodolojik katkı" konumlandırması yeniden düşünülmeli (en kritik dış etki).

---

## Özet sayılar
- **Sertifikasyon bloke eden alt-madde:** 30 (B1–B8) · **Minör:** 20 (m1–m13; P48 iptal, P33/P35 değişmez) · **NEEDS-AUTHOR:** 9 · **Kod yeniden-derleme:** 1 (P01).
- **Doğrulama:** 42 CSV-tabanlı sayısal değerin tümü gerçek kaynak hücreyle birebir eşleşti; 4 tıbbi atıf PubMed PMID/DOI ile doğrulandı; 2 ajan hatası (P48, P20) editör spot-kontrolünde düzeltildi.
- **Önerilen sıra:** P01 → P02-P07 → P18-P21 → P22 → P08-P17 → P42/P43/P44/P50/P51 → P27-P30 → P23-P25/P49 → P26 → P31-P41/P46/P47/P52.

---

# UYGULAMA DURUMU (CSR'ye fiilen işlendi)

**Yedek:** `docs/CLINICAL-STUDY-REPORT-FINAL.bak-precorrection.md`. **Diff:** 92 ekleme / 76 silme. **Doğrulama:** 2 workflow (kanıt-çıkarım + adversaryal denetim) + 3 elle grep pası; tüm eski-değer kalıntı taramaları 0.

## Uygulandı (plandaki maddeler)
B1 (P18–P21), B2 (P22), B3/H5 (P01–P07 + cascade §2.3/§2.4-değişmedi/§15.6/§17.2/§19.1), B4 (P23–P25), B5 (P08–P16), B6 (P26), B7 (P17), B8 (P27–P30); minörler P31–P47, P49–P52. **P48 İPTAL** (rapor doğruydu). **P20** editör spot-kontrolüyle düzeltilerek uygulandı (RV_q sütunu doğru; RV_qa karışıklığı önlendi).

## Uygulama sırasında bulunan VE düzeltilen EK kalıntılar (planın ötesinde)
1. **Ek A α/ω genişletmesi** — plan yalnız madde sayısını kapsıyordu; α/ω değerleri de (reddetme hariç 6 satır) kaynakla uyuşmuyordu → tüm Ek A tablosu `psychval_reliability.csv`'den yeniden yazıldı.
2. **§11.1.2 Bayes tablosu** — 4 satırın 2'si (aşırı koruma, karşılaştırma) hiç kestirilmemiş (`h1_bayesian_plan.csv`: "planned_preflight_only") → tablo gerçek 2 satıra indirildi + not; değerler düzeltildi (reddetme 0,18→0,16; sıcaklık −0,04→0,09).
3. **§14.1 H1-sıcaklık satırı** — işaret/pd/ROPE yanlıştı (−0,04/0,75/%72 → 0,09/0,90/%55).
4. **§11.1.1 prose** — Bayes reddetme + sıcaklık değerleri.
5. **Tablo 1C Anne kronik hastalık** — grup sütunları takas edilmişti (%24/%29 → %29/%24; kaynak Kontrol 28,9% / DM 24,2%).
6. **Tablo 1A çocuk sayısı** — "2,4" kaynakla uyuşmuyordu (medyan 3,00) → 3,0/3,0.
7. **§18 Faz II H5 cascade** — eski "zayıf-orta uyum yönü" dili 4 yerde (§18.2 Tablo 18.1, §18.6 metin + Tablo 18.5, §18.12 kanonik karar) → birincil verdiktle (triangülasyon karşılanmadı / tek-strateji sinyal) hizalandı.
8. **Üç ayrı "113 CSV"** (§2.3, §18.1, Ek F.2) → 114.

## Açık kalan YAZAR-AKSIYONLARI (uydurma yapılmadı; görünür not bırakıldı)
- **es_isei08 ≡ aile_isei08** özdeşliği — eş mesleki indeksin ayrı türetimi (Tablo 1A dipnotu).
- **L476 glisemik kohort referansı** — doğrulanamadı, bracket-not bırakıldı.
- **s-EMBU ebeveyn formu uyarlaması + 4. "karşılaştırma" boyutu** kaynağı (§8.3.1 notu; çocuk formu Dirik 2015 doğru yere işlendi).
- **STROBE tarama-akış sayıları** (taranan/red/dışlanan) — §9.1 not.
- **§11.4.3 item-collapse** sapma satırının `02-sapma-tablosu.md`'ye eklenmesi.
- **HbA1c %7–9 / >9 alt bantları** n=39 paydası üzerinden kesin sayıları (§9.4 not).
- **§20.1 yeniden-alfabetikleştirme** (Dirik, Dündar girişleri konumu).
- **§3 kullanılmayan kısaltmalar** (AVE/CR/HTMT/NRI/IDI) ve ISCO-08 — TLI eklendi.
- **2.594 satır toplamı** (Ek F.2) ve **n=479** 3-satır farkı (dipnot eklendi, neden teyidi).
