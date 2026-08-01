# BP27 Türkiye atezolizumab (NSCLC) — Kanıta Dayalı Değerlendirme ve Sentez

**Tarih:** 2026-07-24 · **Girdi:** [`../problem.md`](../problem.md) · **Kanıt tablosu:**
[`../04_extraction/bp27_atezolizumab_tr_extraction.csv`](../04_extraction/bp27_atezolizumab_tr_extraction.csv)
· **Arama logu:** [`../02_search/bp27_atezolizumab_tr_search_log.md`](../02_search/bp27_atezolizumab_tr_search_log.md)

> **Bu koşumun türü.** Bir ticari/pazar-erişim belgesinin (`problem.md`) iddialarının
> **bağımsız, geniş-kapsam kanıt-doğrulaması**. Tam PRISMA F1–F8 sistematik derlemesi
> değildir (F1 PROSPERO protokolü, F3 tarama, F5 RoB, F6 GRADE, F7 tam HARD-gate /
> sci-audit / galileo yapılmadı — formalizasyon adımları aşağıda). Deterministik
> sayı-bütünlüğü kapıları (extraction_direction + context_source) çıkarım tablosunda
> **temiz** koştu.

---

## 0. Genel hüküm

`problem.md`, sunulan orijinal BP27 planına karşı Farid Bidgoli'nin itirazlarını
değerlendiren, metodolojik olarak **olağanüstü sağlam** bir belgedir. Bağımsız kanıt
taraması, belgenin **beş kök-neden teşhisini** (medyan≠maruziyet, gözlenen≠uygun,
stok≠akış, toplam pay≠segment payı, biyolojik progresyon havuzu≠ticari TEC havuzu) ve
Farid'in dört sorusuna verdiği hükümleri **büyük ölçüde doğrular**. Belgenin klinik
sayıları birebir doğrulandı; düzeltme gerektiren noktalar epidemiyolojik künye
hassasiyeti, tek bir metrik seçimi ve bir-iki nitelik ibaresidir — hükümlerin yönü
değil.

**Tek cümlelik sentez:** Belge doğru; kanıt onu destekliyor; düzeltmeler kozmetik/künye
düzeyinde, bir de "20–25% progresyon" priörünün payda-koşuluna dair önemli bir keskinleştirme.

---

## 1. Farid'in dört sorusu — kanıtla doğrulanmış hüküm

| Soru | Belgenin hükmü | Bağımsız kanıt hükmü | Dayanak |
|---|---|---|---|
| **S1 — 1L DoT <10 ay mı?** | Medyan açısından haklı; ama medyan≠beklenen maruziyet | **DOĞRULANDI.** 1L IO medyan DoT (ECOG 0–1) ~5,3–7,9 ay bandında; medyan vs 24-ay kısıtlı ortalama ayrımı gerçek | Velcheti 2022 (7,4 ay medyan / 10,3 ay RMST); Liu 2021 (5,6 ay); Velcheti/Burke 2022 (6,5 ay); IMpower110 (5,3 ay, kısmi); KEYNOTE-024 (7,9 ay) |
| **S2 — ECOG 3 ilave upside mi?** | Türkiye base-case'te hayır (KÜB/SUT ECOG 0–1) | **DOĞRULANDI, iki katmanlı.** (a) Ruhsat: ECOG 0–1 sınırı; (b) Klinik: ECOG 3'te ~6-hafta OS/PFS + prospektif kanıt yokluğu | TİTCK/SUT ECOG 0–1; Ahmed 2020 (ECOG3: OS 1,5 / PFS 1,3 ay); Katsura 2019 (PS3–4'te avantaj yok, %25 pnömonit); tüm prospektif çalışmalar ≤ECOG 2 |
| **S3 — %35 pay fazla mı düşük?** | Evet; hold-share ~%40; %35 erozyon senaryosu | **DOĞRULANDI (aritmetik iç-tutarlı).** 70%×57%=%39,9; %35 → mono-içi %50 (7 puan / %12,3 göreli kayıp) | Belgenin kendi sayıları; §6 rekonstrüksiyonu doğrulandı |
| **S4 — 2L kaç hasta, fırsat ne zaman biter?** | Statik yüzdeyle verilemez; legacy stok + aylık akış + tedavi kuyruğu ayrılmalı | **DOĞRULANDI.** Tek wash-out tarihi kavramsal hata; üç-bileşen ayrımı doğru; mutlak sayı claims/EHR/ünite birleşimi gerektirir | OAK/TAIL DoT dağılımı (3,2–3,4 ay + uzun kuyruk); PACIFIC progresyon zamanlaması; stok-akış mantığı |

---

## 2. Eksen bazında doğrulanmış kanıt

### Eksen 1 — 1L IO tedavi süresi (DOĞRULANDI)
Velcheti 2022 (Flatiron RWE, n=807, ECOG 0–1, PD-L1≥50%): medyan rwToT **7,4 ay**,
24-ay kısıtlı ortalama **10,3 ay** — belgede birebir. ECOG 2 (n=237): **2,1 ay / 5,9 ay**
(>3 kat düşüş — PS baskın modifiye edici). Kemo-IO: nonskuamöz 5,6 ay (Liu 2021),
skuamöz 6,5 ay (Velcheti/Burke 2022, 24. ayda %15,9 tedavide → uzun kuyruk). "Medyan ≠
beklenen maruziyet, RMST = ∫S(t)dt kullanılmalı" savı **kavramsal olarak doğru ve
kaynağa sadık**. *Sınır:* RWE künyeleri tek-sponsor/tek-veritabanı (Flatiron/Merck).
*Kısmi:* IMpower110 5,3 ay birincil NEJM'de okunamadı, ikincil kaynaktan doğrulandı.

### Eksen 2 — ECOG 3 / kötü PS (DOĞRULANDI + güçlendirildi)
Ahmed 2020 ECOG-3 (n=18): OS **1,5 ay**, PFS **1,3 ay** — birebir. Katsura 2019: PS3–4'te
BSC'ye üstünlük yok, ağır pnömonit %25 vs %2. **Kritik ek bulgu:** hiçbir prospektif ICI
çalışması ECOG 3 almıyor (PePS2, CheckMate 171/153 hepsi ≤ECOG 2) → "güvenilir havuz
değil" hem sayısal hem kanıt-yokluğu ile destekli. **Önemli nüans:** ECOG **2** ayrı,
daha savunulabilir havuz (PePS2 pozitif sinyal) ama OS ~yarıya iner (TAIL ECOG2 OS 3,5 ay)
— belge ECOG 2/3'ü doğru şekilde ayırmalı, birleştirmemeli. Not: Katsura yılı **2019**
(belgede 2020 olarak ima edilmiş → düzeltilmeli).

### Eksen 3 — 2L atezolizumab (DOĞRULANDI)
OAK: DoT **3,4 ay**, PFS **2,8 ay**, %21 >12 ay tedavide, %40 progresyon-sonrası devam —
**4/4 birebir**. TAIL: DoT 3,2 ay / PFS 2,7 ay / OS 11,1 ay; ECOG2 alt grubu belirgin
kötü (OS 3,5 ay). → **Sabit 3-aylık DoT savunulamaz**; sağ-çarpık dağılım (yüksek 0–3 ay
hazard + düşük 4–12 ay + küçük >12 ay kuyruk) tam KM eğrisinden modellenmeli. OAK,
Türkiye "kemoterapi sonrası lokal ileri/metastatik" atezolizumab ruhsat-ortamının
*birebir* kanıtıdır.

### Eksen 4 — Evre III KRT + durvalumab (DOĞRULANDI + önemli keskinleştirme)
PACIFIC/Spigel 5-yıl/PACIFIC-R/Park (Kore)/Aslan (İsrail) künyeleri ve sayıları
doğrulandı (Spigel sayfa 1301–1311 dahil). **En kritik bulgu — payda sorunu:** belgenin
"ilk 6 ayda %18–31 progresyon" alıntısı yalnız **durvalumab-başlatan** stratum içindir
(zaman-sıfır = durva ilk doz; payda = durvaya progresyonsuz ulaşanlar). Bunlar
**koşullu-sağkalan** popülasyondur. Doğru inflow paydası **KRT'yi tamamlayan tüm
hastalar** (zaman-sıfır = definitif RT bitişi) olduğunda 6-aylık rakam **çok daha
yüksektir** (~%40–55; PACIFIC plasebo-kolu KRT-only proxy). İki kohort arası %18 vs %31,2
farkı bile tanım kaynaklı (İsrail nüks-VEYA-ölüm sayıyor + erken-YE-kesenleri tutuyor;
Kore yalnız nüks sayıyor + erken-YE-kesenleri dışlıyor). → **Belgenin "payda açıkça
yazılmalı" uyarısı doğru; ama her stratumun paydası ayrı verilmeli — %18/%31,2/%40–55
aynıymış gibi havuzlanmamalı.** Ayrıca İsrail kohortunda **%19,4 hasta hiç durvaya
geçmiyor** (erken progresyon/uygunsuzluk) — tam bu grup 6-ay paydalarından düşüyor.
"Zaman-sıfır = RT bitişi" savı **doğru** (durva-başlangıcı sıfır alınırsa immortal-time/
seçilim yanlılığı; hedef-çalışma emülasyonu literatürüyle destekli).

### Eksen 5 — Türkiye ruhsat/geri ödeme (DOĞRULANDI — 10/07/2025 SUT birincil metniyle kapandı)

> **GÜNCELLEME (2026-07-27, birincil kapanış):** Aşağıdaki "portal/ikincil" ve `unverified`
> notları, **10/07/2025 SUT değişikliği (RG 32952) birincil metni** host-PDF'ten OCR ile
> çekilince **kapandı** (enrichment raporu §H.6; anamnesis `rg-sut-degisiklik-20250710`).
> Özet: MADDE 1, 4.2.14.C'ye yeni **fıkra (3)** ekledi (eski (ee)/(pp) mülga). **Atezolizumab 2L
> metastatik KHDAK artık SGK GERİ ÖDEMELİ** (bent c)3): ECOG 0–1, önceki 1–2 basamak kemo +
> progresyon, EGFR/ALK/ROS-neg, **PD-L1 eşiği yok**, ardışık/önceki-IO dışlaması — KÜB ile birebir.
> 2. basamakta **hem atezolizumab (c)3) hem nivolumab (a)14) geri-ödemeli** → "yalnız nivolumab"
> (Cangir 2022 + amendman-öncesi ~24/5/2025 snapshot) **10/07/2025'te GEÇERSİZ.** Durvalumab
> Evre III (ç)2: PD-L1≥%1, KRT sonrası progresyonsuz, monoterapi, ≤12 ay) SUT'a eklendi; "6 ay
> kuralı" hem KÜB hem SUT birincil metninde **yok** (uygunluk = progresyonsuzluk).
- **Durvalumab (IMFINZI) — BİRİNCİL KÜB'DEN DOĞRULANDI** (TİTCK KÜB onay 19/01/2026):
  PD-L1≥%1, rezeke edilemeyen lokal ileri KHDAK, platin bazlı KRT sonrası **progresyon
  görülmeyen**, monoterapi, **≤12 ay**; "daha sonraki basamaklarda PD-1/PD-L1
  kullanılamaz" (ardışık-IO dışlaması **label'da**); EGFR/ALK/ROS-1 dışlanır. Belge birebir.
- **Atezolizumab 2L (TECENTRIQ) — BİRİNCİL: hem KÜB hem SUT (çözüldü).** KÜB 2L endikasyonu
  (TİTCK onay 07/02/2026): ECOG 0–1, 1–2 basamak kemo + progresyon, nonskuamözde EGFR/ALK/ROS
  negatifliği, **PD-L1 eşiği YOK** (≥%50 yalnız 1L). **SUT birincil (10/07/2025, RG 32952,
  4.2.14.C fıkra(3) c)3):** aynı koşullarla **2L metastatik/lokal ileri KHDAK GERİ ÖDEMELİ** +
  "tedavi öncesi/sonrasında başka immünoterapi kullanılması halinde bedeli Kurumca karşılanmaz"
  (ardışık/önceki-IO dışlaması). → *koşul metni* artık **portal değil birincil SGK SUT** (§H.6).
- **"6 ay kuralı" — birincil olarak ÇÜRÜTÜLDÜ (iki kaynak):** durvalumab IMFINZI KÜB'ünde **VE**
  SUT 4.2.14.C ç)2'de zaman-penceresi kuralı **yok**; uygunluk = platin bazlı KRT sonrası
  **progresyon görülmemesi**. Belgenin "6 ay kuralı çıkarılmalı" savı **birincil doğrulandı**
  (reimbursement-tarafı dahil; artık `unverified` değil).
- **ECOG 3 base-case dışı:** ECOG 0–1 sınırından çıkar → doğrulandı.
- **Ardışık-IO etkileşimi:** Evre III'te durvalumab alan hasta, sonradan geri ödemeli
  farklı bir anti-PD-(L)1 (atezolizumab) **alamaz** — hem durvalumab KÜB'ü hem atezolizumab
  2L SUT bloğu bunu zorluyor. → Evre III durvalumab tüketimi 2L TEC havuzunu daraltır (belge doğru).

### Eksen 6 — Türkiye epidemiyolojisi (BAĞLAM; künye düzeltmesi gerekli)
IARC **GLOBOCAN 2022** (yetkili, anahtarsız API): Türkiye akciğer kanseri **insidans
41.032** (belirsizlik aralığı 36.224–46.478), **mortalite 38.505**, 5-yıl prevalans
54.335 — 1. sıra. **Belge "GLOBOCAN 2024 fact sheet: 37.846 / 31.674 / 49.303" diyor**;
bu güncel GLOBOCAN 2022 modellenmiş turundan farklı, üstelik ayrı bir "GLOBOCAN 2024" veri
turu **yoktur** (IARC'ın küresel turu GLOBOCAN 2022'dir; fact sheet'ler 2022 tabanlıdır).
→ **Künye "GLOBOCAN 2022" olarak düzeltilmeli.** Kaba üst-sınır yöntemi doğru; GLOBOCAN
2022 ile aralık ~6.600–8.700 Evre III NSCLC/yıl'a genişler (belgenin 6.100–8.000'ine
yakın, hafif daha yüksek). NSCLC %80–85 ve Evre III %20–25 oranları standart epidemiyoloji
(Cangır 2022 künyesi doğrulandı, PMID 36192076). **STONE (UHOD) MEDLINE/PMC-indeksli
değil** → bağımsız doğrulanamadı; belgenin kendi kapsamlı çekinceleri (pre-PACIFIC,
tek-modalite merkez, ulusal insidans değil) yerinde. *GLOBOCAN modellenmiş tahmindir,
gözlenmiş kayıt değildir; histoloji/evre ayrımı vermez — NSCLC%/Evre III% klinik
literatürden gelmeli (belge bunu doğru yapıyor).*

**PD-L1 TPS≥%50 prevalansı — TR vs global (kapsamlı kıyas, enrichment §I):** TR all-comer 22C3
**~%22–28** (Dülger 22C3 %27,5 en sağlam; Gürbüz %23,4; Söyler %22,2). Canaslan **%17,8 alt uçtadır**
(metastatik-only, klon-NR, driver-zengin payda) — TR'nin temsili değeri değildir; Teoman %12,5 yalnız
EGFR-mutant (havuzlanamaz). Global all-comer 22C3 **%22** (EXPRESS, 18 ülke; EGFR/ALK-WT **%27**);
KEYNOTE-024 ~%30 bir **taranmış-zenginleştirilmiş** çapadır (gerçek all-comer ~%22), IMpower110 SP142
"high" 22C3 ≥%50 ile **kıyaslanamaz**. **Payda-eşleşmeli (F7-B/D): TR all-comer 22C3 %27,5 vs global all-comer
22C3 %22 (EXPRESS) → TR üst uçta, anormal düşük DEĞİL;** global EGFR/ALK-WT %27 (TR-özgü EGFR-WT değeri yok →
çapa). → **BP27 uygunluk-şelalesi çarpanı:** 1L atezolizumab PD-L1≥50 monoterapi (SUT
c)2/KÜB) hedefi = **EGFR/ALK-WT ileri NSCLC'nin ~%25–30'u** (%17,8 değil; %17,8 ~%35 küçümser). PD-L1≥%1
(durvalumab Evre III eşiği) TR/global ~%50–52. 2L atezolizumab (c)3) PD-L1 eşiği **yok** (§H.6).

### Eksen 7 — Pazar-payı matematiği + dinamik model (DOĞRULANDI)
- **Aritmetik iç-tutarlı:** 52/57=%91,2 ima edilen mono ağırlık; 70%×57%=%39,9
  hold-share; 35/70=%50 mono-içi (7 puan kayıp, %12,3 göreli erozyon); 70%×35%=%24,5.
  Farid'in ~%40'ı doğru; %35 nötr base-case değil **erozyon senaryosu**.
- **Model metodolojisi sağlam:** RMST=∫₀^τ S_DoT(t)dt doğru; stok-akış ayrımı (legacy
  stok / aylık inflow / on-treatment kuyruk) doğru; 8-durumlu çok-durumlu model uygun;
  competing-risk uyarısı (PFS zaten progresyon-veya-ölüm içerir → çift-iskonto yapma)
  doğru; uygunluk waterfall'ı (çarpımsal koşullu olasılıklar) standart.

---

## 3. Belgeye önerilen somut düzeltmeler

| # | Düzeltme | Gerekçe | Önem |
|---|---|---|---|
| D1 | "GLOBOCAN 2024" → **"GLOBOCAN 2022"**; sayılar 41.032/38.505/54.335 (güncel tur) | Ayrı 2024 veri turu yok; sayılar farklı | Orta (künye doğruluğu) |
| D2 | Katsura **2019** (belge 2020 ima ediyor) | PMID 31258716, J Cancer 2019 | Düşük |
| D3 | "İlk 6 ayda %20–25 progresyon" → **stratum + payda etiketiyle**: durva-başlatan için ~%18–31; tüm-KRT/RT-bitişi paydasında ~%40–55 | İki kohort koşullu-sağkalan; paydalar havuzlanamaz | **Yüksek** (model sayısını yönlendirir) |
| D4 | ECOG 2 ile ECOG 3'ü açıkça ayır | ECOG 2 savunulabilir havuz; ECOG 3 değil | Orta |
| D5 | ✅ **KAPANDI** — Atezolizumab 2L birincil SGK SUT citation'ı eklendi: SUT 10/07/2025 (RG 32952) 4.2.14.C fıkra(3) c)3 (§H.6); medikaynak portalı artık gerekli değil | Birincil metin host-PDF + OCR ile çekildi, version-damgalı (RG 32952) | Çözüldü |
| D6 | IMpower110 5,3 ay için birincil-kaynak sınırını dipnotla | NEJM tam-metni kapalı, ikincil doğrulama | Düşük |

---

## 4. Belgenin ötesine geçen kanıt (genişletme)

- **1L uzun kuyruk kantifikasyonu:** KEYNOTE-024 5-yıl %25,8 hasta 35 kür tamamladı;
  KEYNOTE-407 %19,8; KEYNOTE-189 %13,9 — RMST savını güçlendirir.
- **ECOG 2 pozitif sinyali:** PePS2 (DCB %36–38, aşırı toksisite yok) — ECOG 2 havuzunun
  ECOG 3'ten neden ayrılması gerektiğini destekler.
- **Sonraki-basamak IO tüketimi:** Spigel 2022 — durva sonrası sonraki IO %12,6 vs plasebo
  %29,1; ardışık-IO dışlamasının 2L TEC havuzunu daralttığını sayısallaştırır.
- **PICASO (prospektif ECOG2):** medyan PFS 1,6 ay, ~1/3 ilk taramadan önce progresyon/ölüm
  — kötü-PS erken-drop-off'unu prospektif olarak doğrular.

---

## 5. Çözülemeyen / `unverified`

1. ✅ **ÇÖZÜLDÜ — SGK SUT birincil metni (atezolizumab 2L koşulları):** SUT 10/07/2025 (RG 32952)
   4.2.14.C fıkra(3) c)3 host-PDF + OCR ile çekildi (§H.6); atezolizumab 2L GERİ ÖDEMELİ,
   version-damgalı birincil metin.
2. ✅ **ÇÖZÜLDÜ — "6 ay kuralı" yokluğu:** hem IMFINZI KÜB hem SUT 4.2.14.C ç)2 birincil metninde
   zaman-penceresi kuralı yok → reimbursement-tarafı dahil dışlandı.
3. **STONE (UHOD):** PubMed/EPMC-indeksli değil → bağımsız doğrulanamadı.
4. **IMpower110 5,3 ay:** birincil NEJM tam-metni erişilemedi (ikincil doğrulama).
5. **who-gho** akciğer-özgü indikatör dönmedi (GLOBOCAN birincil epi kaynağı).
6. **"Hiç durvaya geçmeyen %" genellenebilir priörü:** yalnız tek kohort (%19,4, Aslan).

---

## 6. Formalizasyon adımları (bu koşumda YAPILMADI)

Tam PRISMA SR / teslim-manuskripti için: F1 PROSPERO protokolü (PICOTS + önceden-kayıt) ·
F3 tarama + PRISMA akış sayıları · F5 RoB (RCT→RoB2 / gözlemsel→ROBINS-I) · F6 GRADE
kesinlik profili · F7 tam `run_hard_gate.py` + `/sci-audit:audit --type prisma` +
galileo (claim_source_match / overclaim / harking). Bu koşum bunların yerine geçmez;
kanıt tabanını ve claim-by-claim doğrulamayı sağlar.
