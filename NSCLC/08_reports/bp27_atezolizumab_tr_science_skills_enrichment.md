# BP27 Atezolizumab TR — GDM science-skills Deterministik Arka-Uç Zenginleştirmesi

> **Kapsam & doktrin.** Bu belge, [`NSCLC_PLAYBOOK.md`](../playbook/NSCLC_PLAYBOOK.md)
> §0'ın somut arka uçları olan **GDM science-skills** katmanını
> ([`references/05_science_skills_onkoloji.md`](../playbook/references/05_science_skills_onkoloji.md))
> BP27 atezolizumab TR değerlendirmesine uygular. **Kanıt ≠ bağlam bağlayıcıdır:**
> ClinicalTrials.gov = **kayıt-lead**; openFDA + mekanizma/Open Targets = **yalnız bağlam**
> (`source_tier=context`) — hiçbiri sentez/çıkarıma etki-büyüklüğü (HR/OS/PFS/ORR)
> beslemez. Etki sayıları yalnız L2 tam-metinden gelir ve
> [`bp27_atezolizumab_tr_fulltext_dossier.md`](bp27_atezolizumab_tr_fulltext_dossier.md)'de kalır.
> Bu belge tam-metin dossier'i **tamamlar**, değiştirmez.
>
> Üretim: Workflow `wmkg2iem2` (4 paralel şerit; run `wf_bfbf9293-c45`), 2026-07-25.
> Ondalık ayırıcı virgül. Uydurma NCT/DOI yok — tüm kimlikler canlı API'den doğrulandı.

---

## A. ClinicalTrials.gov kayıt taraması (L1 — kayıt-lead)

**Arka uç:** ClinicalTrials.gov v2 REST API (açık JSON, auth yok), WebFetch ile.
Etki/sonuç sayısı bilinçli dışlandı; yalnız kayıt meta-verisi.

### A.1 Pivotal çalışma NCT doğrulaması (9/9 canlı API'de teyit — hiçbiri tahmin değil)

| Çalışma | NCT | Faz | Durum | Sponsor |
|---|---|---|---|---|
| IMpower110 (atezo 1L) | NCT02409342 | 3 | COMPLETED | Hoffmann-La Roche |
| OAK (atezo 2L) | NCT02008227 | 3 | COMPLETED | Hoffmann-La Roche |
| POPLAR (atezo 2L) | NCT01903993 | 2 | COMPLETED | Hoffmann-La Roche |
| TAIL (atezo RW/uzun-dönem) | NCT03285763 | 4 | COMPLETED | Hoffmann-La Roche |
| PACIFIC (durva Evre III) | NCT02125461 | 3 | COMPLETED | AstraZeneca |
| POSEIDON (durva 1L) | NCT03164616 | 3 | **ACTIVE_NOT_RECRUITING** | AstraZeneca |
| KEYNOTE-024 (pembro 1L) | NCT02142738 | 3 | COMPLETED | MSD |
| KEYNOTE-189 (pembro 1L non-skuamöz) | NCT02578680 | 3 | COMPLETED | MSD |
| KEYNOTE-407 (pembro 1L skuamöz) | NCT02775435 | 3 | COMPLETED | MSD |

Ayrımlar (yanlış-eşleme önleme): global TAIL = NCT03285763 ≠ Japon **J-TAIL** = NCT03645330 (Chugai);
KEYNOTE-189 Japonya uzantısı = NCT03950674; KEYNOTE-407 Çin uzantısı = NCT03875092.
Kaynak: `https://clinicaltrials.gov/study/<NCT>`.

### A.2 Türkiye ayak izi (erişim-kanalı bağlamı)

- **Atezolizumab × NSCLC × Türkiye lokasyonu: totalCount = 15 çalışma.** IMpower110 (NCT02409342)
  ve OAK (NCT02008227) **TR merkezleri listeler** → Türkiye ruhsat/kayıt çalışmalarından bu yana
  atezolizumaba **çalışma-yoluyla erişim** teyitli.
  Kaynak: `clinicaltrials.gov/api/v2/studies?query.cond=non-small cell lung cancer&query.intr=atezolizumab&query.locn=Turkey&countTotal=true`.
- **NSCLC × Türkiye × herhangi kontrol-noktası (durva/nivo/pembro/atezo): totalCount = 126 çalışma**
  → hatırı sayılır bir TR kontrol-noktası klinik-çalışma altyapısı / çalışma-yoluyla-erişim kanalı.
- **TR örnekler:** NCT07279402 **TRIMPACT** ("Real-World First-Line Atezolizumab in Stage IV NSCLC
  PD-L1≥50%", **RECRUITING**, sponsor **Antalya Eğitim ve Araştırma Hastanesi** — yerli RWE üretimi);
  NCT04513925 SKYSCRAPER-03 (atezo+tiragolumab vs durva, Evre III, Faz 3); NCT04294810 SKYSCRAPER-01
  (Faz 3); NCT02031458 BIRCH (Faz 2, PD-L1+); durvalumab tarafı NCT04385368 (rezeke Evre II-III, Faz 3),
  NCT05687266 AVANZAR (Dato-DXd+durva 1L, Faz 3).

### A.3 Boru hattı (yayın-yanlılığı / süregelen)

- **Süregelen (RECRUITING|ACTIVE_NOT_RECRUITING) 2L / kemo-sonrası atezolizumab NSCLC: totalCount = 20**
  → OAK/POPLAR pivotalleri tamamlanmış olsa da geç-hat atezolizumab boru hattı hâlâ aktif.
  Örnek: NCT02486718 (Faz 3, kemo-sonrası), NCT04958811 (tiragolumab+atezo+bev, önceden-tedavili, Faz 2),
  NCT03782207 (atezo gerçek-dünya, önceden-tedavili), NCT04440735 (DSP107+atezo, Faz 1/2).

> **BP27'ye katkı (A):** Türkiye'de atezolizumaba erişim, **geri-ödeme dışı** kalsa bile
> (bkz. Cangir tam-metin: 2022'den beri 2L'de yalnız nivolumab geri-ödemeli) **klinik-çalışma +
> yerli RWE kanalıyla** fiilen mevcuttur; TRIMPACT gibi TR-öncülüğünde RWE çalışmaları PD-L1≥50 1L
> atezolizumab kullanımını yerelde belgeliyor. Bu, "ruhsat var ama geri-ödeme yok" boşluğunun
> hasta-erişimine yansımasını inceltir.

---

## B. openFDA regülatif bağlam (L5 — yalnız bağlam; etki sayısı beslemez)

**Arka uç:** openFDA MCP (`drug/drugsfda`, `drug/label`, `drug/event`). Caveat: FAERS sayıları
**kendiliğinden bildirim** — insidans/oran DEĞİL.

### B.1 Onay kilometre taşları

- **Atezolizumab / TECENTRIQ — BLA761034 (Genentech):** orijinal onay **2016-05-18** (Tip 1, ilk-sınıf
  anti-PD-L1). NSCLC-ilişkili altı EFFICACY eki **s033–s038 hep 2021-02-17** onaylı (tek birleşik etiket).
  2L metastatik NSCLC endikasyonu (platin-sonrası ilerleme, OAK temelli) **güncel etikette DURUYOR.**
  *Sınır:* openFDA drugsatfda endikasyon-düzeyi gönüllü geri-çekmeleri güvenilir kodlamaz; buradaki
  yokluk kanıt değildir. (Atezolizumab **ürotelyal** hızlandırılmış-onay geri-çekmesi ayrı, NSCLC-dışı bir meseledir.)
  Ayrıca 2024 subkutan form **TECENTRIQ HYBREZA** (BLA761347).
- **Durvalumab / IMFINZI — BLA761069 (AstraZeneca):** orijinal onay **2017-05-01**. **Rezekte edilemez
  Evre III NSCLC (PACIFIC, cCRT-sonrası)** = ek **s002, 2018-02-16**. Metastatik NSCLC (POSEIDON,
  +tremelimumab+platin) = s036, 2022-10-21. Rezektabl NSCLC neoadjuvan+adjuvan (AEGEAN) = s050, 2025-03-28.

### B.2 Güncel etiket NSCLC endikasyonları (bağlam)

- **Atezolizumab:** adjuvan (Evre II-IIIA, PD-L1 TC≥%1); 1L metastatik yüksek PD-L1 (TC≥%50 veya IC≥%10,
  EGFR/ALK yok); 1L non-skuamöz +bevacizumab/paklitaksel/karboplatin; 1L +nab-paklitaksel/karboplatin;
  **2L metastatik (platin-sonrası ilerleme).**
- **Durvalumab:** rezektabl NSCLC neoadjuvan+adjuvan (≥4 cm/nod+, EGFR/ALK yok); **rezeke edilemez Evre III
  (cCRT-sonrası ilerlememiş)**; metastatik (+tremelimumab+platin, EGFR/ALK yok).

### B.3 Uyarılar & güvenlik-sinyali bağlamı

- **Her iki ilaçta da Boxed Warning YOK.** Ortak PD-(L)1 sınıf uyarısı: immün-aracılı advers reaksiyonlar
  (pnömonit, kolit, hepatit, endokrinopati, dermatolojik, nefrit; durvalumab ek olarak **pankreatit**);
  infüzyon reaksiyonu; embriyo-fetal toksisite.
- **Atezolizumab FAERS ilk-8 bildirim terimi (kendiliğinden bildirim — insidans DEĞİL, son güncelleme 2026-04-28):**
  DEATH 4167 · OFF LABEL USE 3425 · DISEASE PROGRESSION 2076 · PYREXIA 1712 · DIARRHOEA 1681 · FATIGUE 1451
  · ANAEMIA 1308 · PNEUMONIA 1099. (Onkoloji popülasyonunda ölüm/etiket-dışı-kullanım/hastalık-ilerlemesi
  terimleri bildirim-artefaktı olarak baskındır; **oran olarak sunulamaz**.)

> **BP27'ye katkı (B):** FDA'da atezolizumab 2L metastatik NSCLC endikasyonu **hâlâ yürürlükte** —
> "atezolizumab 2L'den çekildi" algısı NSCLC için yanlıştır (çekilme ürotelyaldi). Asıl kısıt
> **regülasyon değil geri-ödeme** düzeyindedir (TR: 2L IO'da yalnız nivolumab geri-ödemeli). Sınıf-düzeyi
> immün-aracılı güvenlik profili atezo/durva için ortaktır (Boxed Warning yok).

---

## C. Mekanizma / hedef-hastalık bağlamı (L5 — yalnız bağlam)

**Arka uç:** IUPHAR Guide to PHARMACOLOGY (GtoPdb) + Open Targets GraphQL v4 (curl POST; WebFetch GET-only
olduğundan GraphQL için Bash kullanıldı).

- **atezolizumab** GtoPdb ligand 7990 (Antibody, onaylı; Binding pKd 9,0–10,0); **durvalumab** GtoPdb
  ligand 7985 (Antibody, onaylı; pKd 8,7) — her ikisi **anti-PD-L1**. (GtoPdb basitleştirilmiş etkileşim
  görünümü adlandırılmış CD274 hedefini döndürmedi; anti-PD-L1/CD274 mekanizması yerleşik bağlam olarak,
  OT CD274 antikor-tractability "Approved Drug"=true ile teyitli.)
- **Sürücü hedefleri (GtoPdb):** EGFR (1797, RTK) · ALK (1839, RTK) · ROS1 (1840, RTK) · KRAS (2824, enzim/GTPaz).
- **Open Targets ilişki skorları — NSCLC (MONDO_0005233):** EGFR **0,888** · KRAS **0,834** · ALK **0,813**
  · CD274/PD-L1 **0,702**. (EFO_0003060 null döndü; NSCLC OT'de MONDO_0005233'e çözülür.)
- **Tractability:** EGFR küçük-molekül + antikor "Approved Drug"=true; KRAS küçük-molekül (G12C) true;
  ALK küçük-molekül true; **CD274/PD-L1 antikor "Approved Drug"=true, küçük-molekül değil.**

> **BP27'ye katkı (C):** Mekanizma ayrımı — PD-L1 **antikor-tractable** (IO omurgası) iken EGFR/ALK/KRAS
> sürücüleri **küçük-molekül TKI hedefleri** — sürücü-pozitif hastaların IO-monoterapi uygunluğundan
> neden dışlandığının bağlamsal (sayısal-olmayan) gerekçesini pekiştirir; uygunluk-şelalesindeki
> "sürücü-negatif ~%80" adımının biyolojik zeminini verir.

---

## D. Atıf-snowball (L1 — lead; etki sayısı beslemez, L2 adayı)

**Arka uç:** OpenAlex atıf-grafiği + arama. Tohumlar: OAK, IMpower110, Cangir, Kilickap. Tüm DOI'ler
OpenAlex'ten verbatim; korpusta olan pivotaller + zaten dahil TR makaleleri hariç tutuldu.

**Yüksek öncelikli LOAD-BEARING L2 adayları (5):**

| Kayıt | Yıl | Neden yük-taşıyan | DOI |
|---|---|---|---|
| Türkiye metastatik NSCLC 1L pratik-örüntüleri (ulusal çok-merkez RWE) | 2025 | TR RWE tedavi-manzarası + hatta-erişim atrisyonu | 10.1080/14796694.2025.2527477 |
| Bridging East-West: TR metastatik NSCLC gerçek-dünya klinikogenomik | 2025 | TR mutasyon + gerçek-dünya tedavi/sonuç; PD-L1/sürücü prevalans | 10.3390/genes16121446 |
| Türkiye kanser sağkalımı 2008-2017 (popülasyon-temelli) | 2026 | Cangir insidansını **sağkalımla** tamamlar | 10.1002/ijc.70628 |
| LIST (Fransa RW nivolumab 2L + IO-rechallenge) | 2025 | Kilickap'ın tek ileri-atıfçısı; TR-dışı 2L IO komparatörü | 10.1007/s40487-025-00381-z |
| IO vs kemo-IO 1L, PD-L1 TPS≥50 (gerçek-dünya) | 2026 | IMpower110/EMPOWER stratumunda tedavi-seçimi RWE | 10.3390/jcm15062406 |

**Ek TR gerçek-yaşam 2L/IO & erişim kayıtları (7):** TR 2L nivolumab prognostik indeksler (2024, 10.3390/medicina60111792);
TR ≥65 yaş nivolumab etkinliği (2024, 10.3390/jcm13206263); Hb/RDW 2L-IO prognoz (2026, 10.19161/etd.1849122);
**TR akciğer kanseri geri-ödeme 10-yıl tek-merkez** (2025, 10.1002/cam4.71014 — erişim/geri-ödeme atrisyonu);
TR sigara-durumu × nivolumab yanıtı (2025, 10.18621/eurj.1733954); TR komorbidite yükü ulusal veritabanı
(2026, 10.3390/medicina62050845); TOG plevral mezotelyoma IO-vs-kemo (2025, 10.3390/medicina61040638).

> Not: EMPOWER-Lung1 5-yıl/3-yıl güncellemeleri ve serebral-metastaz alt-grubu, korpustaki EMPOWER-Lung1
> ile örtüştüğü için dışlandı; saf-laboratuvar/radyomik/polimorfizm atıfçıları kapsam-dışı bırakıldı.
> Kilickap tohumu **yalnız 1 ileri-atıf** taşıyor (LIST) → o dal tükendi.

> **BP27'ye katkı (D):** Değerlendirmenin kanıt tabanı, orijinal dossier'in ötesinde **2025-2026 taze TR
> RWE** ile genişliyor (pratik-örüntüleri, klinikogenomik, 10-yıl geri-ödeme, sağkalım). Bunlar **lead**tir;
> herhangi bir sayı teze/senteze girmeden önce L2 tam-metin doğrulaması şarttır (Kısıt-1 PDF akışıyla aynı disiplin).

---

## E. G-SKILL kapı kontrol listesi (bu katmana özgü)

| Kapı | Durum |
|---|---|
| **G-SKILL-WRAP** — her sorgu sarmalayıcı/MCP ile (elle-curl yalnız OT GraphQL POST zorunluluğu) | ✅ (CT.gov v2 API, openFDA MCP, GtoPdb MCP, OpenAlex MCP; OT yalnız GraphQL POST) |
| **G-SKILL-SRC** — kullanılan araç + kaynak URL/ID'ler listelendi | ✅ (her bulguda source; A.2/A.3'te tam API URL'leri) |
| **G-SKILL-TIER** — CT.gov=registry_lead; openFDA/OT/GtoPdb=context; snowball=lead; etki sayısı yalnız L2 | ✅ |
| **G-SKILL-SECRET** — anahtar yok/`~/.env` dışı (tümü anahtarsız açık API) | ✅ (hiçbir sır bu belgede değil) |
| **kanıt≠bağlam** — bağlam/lead şeritlerinden sentez tablosuna HR/OS/PFS/ORR yazılmadı | ✅ |
| **no-fabrication** — tüm NCT/DOI canlı API'den doğrulandı | ✅ (9/9 pivotal NCT teyit; DOI'ler OpenAlex verbatim) |

---

## F. Sonuç — zenginleştirmenin değerlendirmeye net katkısı

1. **Kayıt katmanı (yeni):** BP27 değerlendirmesi artık yalnız yayın-temelli değil; 9 pivotal NCT canlı
   doğrulandı ve **Türkiye'nin çalışma-yoluyla-erişim ayak izi ölçüldü** (atezo NSCLC 15, tüm-IO 126 TR
   çalışma; TRIMPACT yerli RWE). Bu, "ruhsat var, geri-ödeme yok" boşluğunu erişim-kanalı düzeyinde inceltir.
2. **Regülatif ayrım netleşti:** FDA'da atezolizumab **2L NSCLC endikasyonu duruyor**; kısıt geri-ödeme
   düzeyinde. Sınıf güvenliği (Boxed Warning yok, immün-aracılı AE) atezo/durva'da ortak.
3. **Mekanizma zemini:** OT ilişki/tractability, sürücü-negatif uygunluk mantığının biyolojik gerekçesini
   bağlamsal olarak sağlamlaştırır.
4. **Taze kanıt kuyruğu:** 5 yük-taşıyan + 7 destekleyici **2025-2026 TR RWE** kaydı L2 için sıraya alındı.

**Kısıt (dürüst):** Bu belgedeki hiçbir bağlam/lead değeri etki-büyüklüğü olarak kullanılamaz; snowball
adaylarının sayıları yalnız L2 tam-metin (Kısıt-1 disiplini) ile doğrulandıktan sonra değerlendirmeye girer.

---

## G. L2 tam-metin terfisi — yük-taşıyan lead'lerin DOĞRULANMIŞ bulguları

> §D'de "lead" olarak işaretlenen 5 yük-taşıyan kaydın L2 tam-metne terfisi (Workflow `wjnus112u`,
> run `wf_f6c4785b-556`; IJC ek olarak host-PDF ile). **5/5 tam gövde çekildi + DOI↔içerik bütünlüğü PASS +
> anamnesis'e ingest edildi** (corpus docs 170→175, chunks 1030→1067; `corpus_stats`). Bu bölümdeki sayılar
> artık **L2=kanıt** (lead değil); her biri tam-metin lokatörlü. Başlangıçta unfetchable olan IJC sağkalım
> makalesi, kullanıcının sağladığı host-tarafı PDF ile bütünlük-kontrollü kapatıldı (§G.5).

### G.1 ESTIMATE — TR ulusal 1L mNSCLC gerçek-yaşam (Future Oncology 2025) · `10.1080/14796694.2025.2527477`

Bütünlük PASS (Türkiye, 636 hasta, 12 merkez; tier=minerva, 5 chunk). **BP27 için en kritik L2 kazanımı:**

- **1L rejim dağılımı (başlangıç):** kombinasyon kemo %71,7 · hedefli %12,7 · mono-kemo %6,3 ·
  **kombinasyon IO %6 · mono-IO %5,5** · BSC %2,5 (First-line treatments/Table 2). → **TR'de 1L'de
  toplam IO kullanımı yalnız ~%11,5** (2020-2021 kohortu; geri-ödeme-kısıtlı gerçeklik). *(F7-C notu: bu
  altı kalemin OCR-toplamı %104,7 — Table 2 transkripsiyon/örtüşme artefaktı; yük-taşıyan değer kombo-IO %6 +
  mono-IO %5,5 = %11,5 bundan etkilenmez, ama tam partisyon RG/Table 2 birincilinden teyit edilmeli.)*
- PD-L1 test oranı %55,5; pozitiflik %42,8 (strata <1/1-49/≥50 planlandı ama uygulanmadı) (Table 3).
- EGFR %22,1; ALK ~%5 (Discussion). ECOG 0-1 yalnız %48,1 (Table 1). Adeno %74,7 / skuamöz %22,8.
- Tanı→1L medyan 29 gün. Veri sonunda mortalite %42,8; **hayatta kalanlarda mono-IO %23,9'a çıkıyor**
  (geç hat) (Table 4). Tanımlayıcı çalışma — PFS/OS/ORR raporlanmadı.

> **BP27 katkısı:** TR 1L IO gerçek-uptake'i (~%11,5) artık **L2 kanıt**la ölçülü — atezolizumab 1L
> PD-L1≥50 hedef-popülasyonunun geri-ödeme boşluğu nedeniyle fiili kullanıma ne kadar az yansıdığını gösterir.

### G.2 Bridging East-West (Canaslan) — TR klinikogenomik mNSCLC (Genes/MDPI 2025) · `10.3390/genes16121446`

Bütünlük PASS (Türkiye 7 bölge, N=1023; tier=EPMC/PMC PMC12733280, 5 chunk). **Uygunluk-şelalesi çarpanları için büyük-N TR çapa:**

- **Sürücü prevalansı:** EGFR %16,0 (ex19del %6,8, L858R %4,8) · ALK %5,0 · KRAS G12C %2,6 · ROS1 %1,9 ·
  BRAF V600E %3,2 · METex14 %2,5 · HER2 %1,4 · hedeflenebilir toplam **%28,3** (Results 3.3). →
  **sürücü-negatif ~%71,7** (IO-monoterapi uygunluğunun payda çarpanı).
- **PD-L1 TPS: <1% %47,8 · 1-49% %34,4 · ≥50% %17,8** (n=601) (Results 3.5). → 1L atezo/pembro-mono
  hedefi (PD-L1≥50) ~her 6 hastadan 1'i.
- Medyan OS 14,4 ay (takip 29,1 ay); NGS uptake %51,6 (2020 öncesi %5,2 → 2025 >%90). EGFR non-skuamöz
  %19,1 vs skuamöz %6,5.

> **BP27 katkısı:** Orijinal dossier'in sürücü-negatif (~%80, karışık kaynak) ve PD-L1≥50 tahminleri
> artık **tek büyük-N TR L2 kohortuyla** yerelleştirildi (sürücü-negatif ~%72; PD-L1≥50 ~%18).

### G.3 LIST — Fransa gerçek-yaşam nivolumab 2L + IO-rechallenge (Oncology and Therapy 2025) · `10.1007/s40487-025-00381-z`

Bütünlük PASS (Fransa, N=522, NCT04500535; tier=EPMC/PMC PMC12647469, 6 chunk). **TR-dışı 2L IO komparatörü:**

- Kohortlar: IO-naif 280 · IO-deneyimli (non-toksisite) 197 · (toksisite) 45; rechallenge alt-grubu 242.
- **2L+ nivolumab medyan PFS 3,2 / 2,7 / 3,9 ay; medyan OS 12,3 / 9,5 / 10,4 ay** (Abstract/Results).
- 12-ay TTD %17,7 / %14,4 / %16,7 (birincil endpoint). Kohort-1 12-ay PFS %17,1 / OS %52,1 / DCR %46,1
  (≈CheckMate 017/057). PD-L1 <%1 kohort-1'de %60,1; sürücü KRAS ~%33-40.

> **BP27 katkısı:** Gerçek-yaşamda 2L IO **dayanıklılığı mütevazı** (medyan PFS ~3 ay) — 2L atezolizumab
> DoT/maruziyet (medyan ≠ beklenen) argümanını harici bir kayıtla destekler; rechallenge beklenenden nadir.

### G.4 IO-mono vs kemo-IO, 1L PD-L1 TPS≥50 (J Clin Med/MDPI 2026) · `10.3390/jcm15062406`

Bütünlük PASS (**Türkiye**, İstanbul Medipol, N=65; tier=EPMC/PMC PMC13027139, 5 chunk):

- Kollar: kemo-IO (pembro+kemo) 36 · IO-mono (pembro) 29. Medyan PFS 24,2 ay; OS 34,6 ay; ORR %76,9; DCR %81,5.
- **Kollar arası PFS/OS farkı anlamlı değil** (PD-L1≥50 genelinde). TPS≥90 vs 50-89: PFS 33,3 vs 17,9 ay
  (p=0,037); OS 67,3 vs 19,8 ay (p=0,028); TPS≥90 bağımsız OS prognostik (Results 3.3).

> **BP27 katkısı:** TR PD-L1-yüksek 1L gerçek-yaşam sonuçları + PD-L1≥90 alt-stratumunun güçlü prognostik
> ayrımı — 1L IO-mono (atezo/pembro sınıfı) hedef-seçiminin yerel etkinlik zeminini verir.

### G.5 TR kanser sağkalımı 2008-2017, akciğer dahil (Int J Cancer 2026) · `10.1002/ijc.70628` — KAPATILDI (host-PDF)

Başlangıçta hiçbir online tier'da gövde yoktu; **kullanıcının sağladığı host-tarafı PDF ile bütünlük-kontrollü
kapatıldı** (Wiley/UICC; Zahwe, Eser, Bardot ve ark.; IARC SURVCAN-3+4; 8 TR popülasyon-temelli kayıt:
Antalya/Bursa/Edirne/Erzurum/Eskişehir/İzmir/Samsun/Trabzon; 16 chunk ingest). Bütünlük PASS.

- **Akciğer 5-yıl ASRS her iki dönemde de <%15 — beş baş kanser arasında EN DÜŞÜK** (Abstract; Sonuçlar/Şekil 1).
- 2013-2017 kayıt aralığı: **%10,7 (Edirne, en düşük) – %19,4 (Trabzon)** (Sonuçlar, akciğer paragrafı).
- **Yaş açığı TERS:** ≥65 yaşta +0,6 pp vs <65'te +3,2 pp iyileşme — akciğerde yaşlılar en az yararlanan grup
  (diğer kanserlerin tersine) (Abstract). Trabzon 2013-2017: <65 %27,8 vs ≥65 %12,6.
- Cinsiyet (Bursa 2013-2017): erkek %12,6 vs kadın %22,7 (+10,1 pp; kadın tüm illerde üstün).
- Dönem: Antalya %11,4→%15,4; Trabzon %15,4→%19,4; Samsun & Erzurum'da iyileşme yok.
- Kıyas: TR akciğer 5-yıl sağkalımı UK %17,4 ve Kanada %24,8'in (2010-2014) **altında**; sigara %31,6,
  vakaların ~%90'ı tütüne atfedilebilir (Tartışma).
- *Kapsam notu (no-fabrication):* 1-yıl/3-yıl akciğer ASRS yalnız Ek Bilgi'de (ana metinde 5-yıl raporlanmış);
  akciğer için evre-bazlı (lokalize/bölgesel/uzak) sağkalım yok (o kırılım yalnız kolorektal + meme) → uydurulmadı.

> **BP27 katkısı:** Cangir insidansı artık **sağkalımla** tamamlandı — TR'de akciğer kanseri 5-yıl sağkalımı
> hem mutlak düşük (<%15) hem de yüksek-gelir ülkelerinin gerisinde; bu, geç-evre baskınlığı + tedaviye-erişim
> boşluğunun sonuç düzeyindeki yansımasıdır ve BP27'nin "erken hat/erişim iyileştirmesi" gerekçesini destekler.

### G.6 L2 terfi kapıları

| Kapı | Durum |
|---|---|
| DOI↔içerik bütünlüğü (her makalede başlık+ülke teyidi) | ✅ 5/5 PASS (IJC host-PDF ile eklendi) |
| Kaynak-tekilliği (sayı yalnız tam-metinden, lokatörlü) | ✅ 68 bulgu, her biri paper::section |
| no-fabrication (gövde yoksa çıkarım yok; SI-only/eksik metrik atlandı) | ✅ IJC 1yr/3yr & akciğer-evre yok → atlandı |
| Kanıt katmanı (bu bölüm source_tier=evidence, §D lead'i geçersiz kılar) | ✅ 5 makale lead→evidence |
| corpus izlenebilirlik | ✅ docs 170→175, chunks 1030→1067 (`corpus_stats`) |

---

## H. TR BİRİNCİL regülatif doğrulama — KÜB + SUT primer metin (Yol 1)

> §B (openFDA = FDA/ABD) ve Cangir (ikincil) ile kapatılamayan **TR birincil regülatif boşluğu**
> kapatan koşum (Workflow `wi4z9y0tr`, run `wf_d9120764-f5d`). Kaynaklar: **TİTCK KÜB PDF'leri**
> (TECENTRIQ onay 07/02/2026; IMFINZI onay 19/01/2026) + **SUT** (bedesten `mevzuatId 112062`,
> konsolidasyon kesimi ~24/5/2025). Tüm alıntılar TR primer metinden **verbatim** (RBŞ: kapsam-içi,
> çarpıtmasız). L5 regülatif bağlam (`source_tier=context`). corpus docs 175→178, chunks 1067→1073.

### H.1 Atezolizumab / TECENTRIQ KÜB (birincil) — `barkod 8699505763460`, `kubkt::560dc0264acb`

**2. basamak KHDAK endikasyonu (Bölüm 4.1, verbatim):**
> "TECENTRIQ'in, performans durumu **ECOG 0-1** olan, **EGFR, ALK, ROS negatif**, semptomatik beyin
> metastazı olmayan, lokal ileri ve/veya metastatik KHDAK nedeniyle **daha önce 1-2 basamak kemoterapi
> almış ve progresyon gelişmiş** hastaların tedavisinde tekrar progresyona kadar kullanımı endikedir."

- **§3.1-3 / §5.1 ECOG 0-1 → CONFIRMED (primer):** endikasyon cümlesi ECOG 0-1 ile sınırlı.
- **§3.1-8 / §7.4 PD-L1 eşiği (2L) → CONFIRMED YOK (primer):** 2L cümlesinde PD-L1 ibaresi geçmez;
  kontrast olarak 1L monoterapi "PD-L1 TC≥%50 ya da IC≥%10" eşiği taşır → 2L'de eşik aranmadığı kanıtlı.
- **Ardışık-IO → NUANCED (primer):** "Tedavi sonu progresyonda diğer PD-1 ve PD-L1 inhibitörleri
  kullanılamaz" ibaresi **1L nab-paklitaksel+karboplatin kombinasyonu** endikasyonuna bağlıdır; **2L
  post-kemo endikasyonunda bu ibare yoktur** (kapsam çarpıtılmadan). Ürün düzeyi `GERİ ÖDEMELİ`
  (retail 123.966,5 TL) ama bu bayrak *hangi endikasyonun* ödendiğini söylemez (bkz. H.3).

### H.2 Durvalumab / IMFINZI KÜB (birincil) — `barkod 8699786770904`, `kubkt::d7c6f4051efe`

**Evre III endikasyonu (§4.1, verbatim):**
> "IMFINZI **PD-L1 düzeyi %1 ve üzeri** olan, rezeke edilemeyen lokal ileri KHDAK'de, **platin bazlı
> kemoradyoterapi sonrası progresyon görülmeyen** yetişkin hastaların tedavisinde **monoterapi** olarak endikedir."

- **§7.2 → CONFIRMED (primer):** PD-L1≥1 + post-cCRT progresyonsuz + monoterapi.
- **§3.1-7 "6 ay kuralı" → REFUTED (primer):** KÜB tam metin taramasında Evre III başlama için "6 ay /
  altı ay" **zaman-penceresi kuralı YOK**; uygunluk = **cCRT sonrası progresyon görülmemesi** durumudur.
  KÜB'deki tüm "6 ay/36 ay" dizeleri yalnız sağkalım istatistiği / adjuvan-nüks penceresi bağlamında.
  → problem.md §7.3'ün "6 ay kuralı çıkarılmalı" hükmü **primer kaynakla doğrulandı.**
- **Süre → CONFIRMED:** "Tedavi süresi fayda gören hastalarda 1 yıla kadar… progresyon geliştiğinde
  kesilmelidir"; Tablo 1: "progresyona, kabul edilemez toksisiteye kadar veya **maksimum 12 ay**."
- **Ardışık-IO → CONFIRMED (primer, KRİTİK):**
  > "**Durvalumab kullanan hastalarda daha sonraki basamaklarda PD-1 ve PD-L1 antikoru kullanılamaz.**
  > EGFR, ALK ve ROS-1 mutasyonu bulunan hastalarda IMFINZI kullanılamaz."
  → problem.md §7.2/§8.1'deki "durvalumab → sonraki TEC havuzundan çıkar" mantığının primer temeli.

### H.3 SUT geri-ödeme (birincil) — `mevzuatId 112062`, 4.2.14.C pp)(122), kesim ~24/5/2025

**EN KRİTİK BULGU — ruhsat ≠ geri-ödeme ayrımı primer kaynakla:**

- **KHDAK 2L'de geri-ödemeli tek PD-1/PD-L1 IO = NİVOLUMAB.** SUT konsolide tam metninde (924.237 karakter,
  grep) **atezolizumab 0 kez, durvalumab 0 kez** geçiyor. Nivolumab 2L KHDAK maddesi (verbatim):
  > "…**ECOG performans skoru 0-1** olan ve bilinen **EGFR, ALK, ROS mutasyonu olmayan**, daha önce **en
  > az bir basamak kemoterapi** tedavisi almış ve sonrasında **progresyon gelişmiş** lokal ileri ve/veya
  > metastatik KHDAK … tedavisinde **monoterapi olarak progresyona kadar** kullanılır."
- **Cangir 2022 "2L'de yalnız nivolumab geri-ödemeli" → CONFIRMED (primer SUT, bu kesim itibarıyla).**
- **§3.1-8 SUT'ta 2L IO için PD-L1 eşiği → CONFIRMED YOK** (nivolumab maddesinde PD-L1 aranmaz).
- **Ardışık-IO (SUT) → CONFIRMED:** "Nivolumab tedavisi sırasında veya sonrasında başka bir PD-1/PD-L1
  inhibitörü kullanılamaz. Nivolumab tedavisi öncesinde immünoterapi almış ve progrese olmuş hastalarda…
  bedeli Kurumca karşılanmaz."
- **DÜRÜST SINIR:** bedesten anlık görüntüsünün kesimi ~24/5/2025; problem.md'nin atıf yaptığı **10/07/2025
  SUT değişikliği bu snapshot'a YANSIMAMIŞ** → durvalumab Evre III geri-ödeme yolu (§7.2) ve olası
  atezolizumab güncellemeleri **bu kaynaktan doğrulanamadı**. Bu, kapatılması gereken kalan primer boşluktur.

### H.4 BP27 için ne değişiyor (net)

1. **Ruhsat ≠ geri-ödeme, artık primer:** Atezolizumab 2L KHDAK **KÜB'de ruhsatlı** (ECOG 0-1, 1-2 kemoterapi
   sonrası progresyon, EGFR/ALK/ROS-neg, PD-L1 eşiği yok) — ama **SUT bu kesimde 2L IO'yu nivolumaba veriyor.**
   BP27'nin "geri-ödemeli 2L TEC havuzu" varsayımı, ruhsat düzeyinde geçerli, **geri-ödeme düzeyinde bu SUT
   kesiminde nivolumab lehine** görünüyor → havuz tanımı bu ayrımla yeniden ifade edilmeli.
2. **"6 ay kuralı" primer olarak yok** (durvalumab KÜB) → problem.md §7.3 hükmü sağlam.
3. **Ardışık-IO dışlaması hem durvalumab KÜB hem SUT nivolumab maddesinde primer** → durvalumab/önceki-IO
   almış hastanın sonraki reçetesi geri-ödeme dışı; problem.md §8.1 kohort ayrımı doğrulandı.
4. **PD-L1 eşiği 2L'de yok** (hem KÜB hem SUT) → §3.1-8 primer teyit.

### H.5 Kapı & kapatılan iddia haritası

| problem.md iddiası | Önceki durum | H sonrası (primer) |
|---|---|---|
| §3.1-3 ECOG 0-1 (2L atezo) | ikincil (Cangir) | ✅ **CONFIRMED** KÜB + SUT verbatim |
| §3.1-7 durvalumab "6 ay kuralı" yok | mantıksal | ✅ **REFUTED** IMFINZI KÜB tam-metin |
| §3.1-8 2L PD-L1 eşiği yok | OAK/etiket | ✅ **CONFIRMED** KÜB (kontrast) + SUT nivolumab |
| §7.2 durvalumab Evre III koşulları | openFDA (ABD) | ✅ **CONFIRMED** IMFINZI KÜB verbatim |
| ardışık-IO → TEC havuzundan çıkış (§8.1) | yön | ✅ **CONFIRMED** KÜB + SUT primer |
| "2L'de yalnız nivolumab geri-ödemeli" (Cangir) | 2022 ikincil | ⚠️ **yalnız amendman-öncesi** (kesim 24/5/2025); **10/07/2025'te GEÇERSİZ** — bkz §H.6 |
| 10/07/2025 SUT değişikliği (durvalumab + atezolizumab 2L) | problem.md atfı | ✅ **CONFIRMED (primer, host-PDF)** — §H.6: atezo c)3 + durva ç)2 eklendi |

> **Kalan tek primer boşluk:** 10/07/2025 tarihli SUT değişikliğinin güncel konsolide metni (Resmî Gazete
> 20250710, sayı 32952) — bedesten snapshot'ı (kesim ~24/5/2025) bunu içermiyor. Durvalumab Evre III
> geri-ödeme yolu (§7.2) + olası atezolizumab güncellemesi bu tarihten sonra eklenmiş olabilir.
>
### H.6 10/07/2025 SUT değişikliği — PRIMER KAPATILDI (host-PDF) · **BP27 çekirdek bulgusu**

Resmî Gazete `20250710-13.pdf` (sayı 32952) `resmi-gazete-mcp` worker'ından item olarak doğrulandı ama gövdesi
worker sınırlarını aştı (219 sf > 200 OCR; 22,2 MB > 12 MB; sayfa-aralığı parametresi yok; PDF taranmış fax-image,
metin katmanı yok). **Kullanıcı host-PDF'i sağladı;** tesseract (`-l tur`) OCR + bütünlük PASS
(*"SGK Sağlık Uygulama Tebliğinde Değişiklik Yapılmasına Dair Tebliğ"*, RG 32952, 10.07.2025). anamnesis
doc_id `rg-sut-degisiklik-20250710` (corpus docs →179, chunks →1076). Alıntılar OCR-normalize (%/ilaç adı),
anlam korundu (RBŞ).

**MADDE 1** — 4.2.14.C'ye yeni **fıkra (3)** eklendi; eski **(ee)** ve **(pp)** bentleri **mülga** edilip tüm IO
konsolide edildi. 10/07/2025 itibarıyla KHDAK'de geri-ödemeli PD-(L)1 immünoterapi:

| Ajan (bent) | KHDAK basamak/ayar | Anahtar koşul |
|---|---|---|
| **Atezolizumab c)3** | **2. basamak** metastatik/lokal ileri | **ECOG 0-1, önceki 1-2 basamak kemoterapi + progresyon, EGFR/ALK/ROS-neg, PD-L1 eşiği YOK, ardışık/önceki-IO dışlaması** |
| Atezolizumab c)2 | 1. basamak metastatik | PD-L1 ≥%50, ECOG 0-1, en fazla 35 kür |
| Atezolizumab c)1 | Adjuvan (Evre II-IIIA) | PD-L1 TC≥%50, rezeksiyon+platin sonrası, ≤1 yıl |
| **Nivolumab a)14** | **2. basamak** metastatik/lokal ileri | ECOG 0-1, önceki **1** basamak kemoterapi + progresyon, EGFR/ALK/ROS-neg, ardışık/önceki-IO dışlaması |
| Nivolumab a)13 / a)15 | Neoadjuvan (3A) / 1L nivo+ipi (PD-L1<%50) | — |
| **Durvalumab ç)2** | **Evre III** rezeke edilemez | PD-L1≥%1, platin bazlı KRT sonrası progresyonsuz, monoterapi, ≤12 ay, ardışık-IO dışlaması |
| Pembrolizumab b)1-6 | 1L non-skuamöz / 1L skuamöz / 2L / neoadjuvan | (PD-L1 eşikleri OCR'da bozuk; primer metne bakılmalı) |

**c)3 (atezolizumab 2L) verbatim:** "Atezolizumab; ECOG performans durumu 0-1 olan, semptomatik beyin metastazı
olmayan, lokal ileri ve/veya metastatik küçük hücreli dışı akciğer kanseri nedeniyle **daha önce 1-2 basamak
kemoterapi almış ve progresyon gelişmiş** hastaların tedavisinde tekrar progresyona kadar kullanılması halinde
bedeli Kurumca karşılanır… **tedavi öncesi veya sonrasında başka bir immünoterapi tedavisi kullanılması halinde
bedeli Kurumca karşılanmaz.**"

> **BP27 ÇEKİRDEK DÜZELTMESİ:** §H.3'ün "**2L'de yalnız nivolumab geri-ödemeli**" bulgusu **amendman-öncesi**
> (bedesten kesim ~24/5/2025) durumdur. **10/07/2025 değişikliğiyle bu ARTIK GEÇERLİ DEĞİL:** 2. basamak
> metastatik KHDAK'de **hem atezolizumab (c)3) hem nivolumab (a)14) geri-ödemeli.** Yani atezolizumab 2L NSCLC
> **hem ruhsatlı (KÜB) hem SGK geri-ödemeli** (koşullar KÜB ile birebir: ECOG 0-1, 1-2 kemoterapi sonrası
> progresyon, EGFR/ALK/ROS-neg, PD-L1 eşiği yok). BP27'nin "geri-ödemeli 2L TEC havuzu" premisi **reimbursement
> düzeyinde de doğrulandı** (§H.4'ün aksine — o pre-amendman snapshot'a dayanıyordu). Ek: durvalumab Evre III
> (ç)2, §7.2 primer doğrulandı) + atezolizumab 1L PD-L1≥50 (c)2). **Tüm ajanlarda ardışık/önceki-IO dışlaması**
> → 1L-IO veya durvalumab almış hasta sonraki basamakta IO geri-ödemesi alamaz (§8.1 kohort ayrımı primer teyit).

> **Kalan primer boşluk: YOK.** problem.md'nin tüm regülatif iddiaları (§3.1-3/7/8, §5.1, §7.2, §7.3, §8.1)
> artık primer kaynakla (KÜB + SUT amendman) **kapalıdır**. Tek not: c)3 dâhil %/PD-L1 değerleri taranmış PDF'ten
> OCR-normalize edildi; hukuki-kanonik nüsha için RG 32952 PDF esastır.

---

## I. PD-L1 TPS≥%50 prevalansı — Türkiye vs global (kapsamlı kıyas + DÜZELTME)

> Kapsamlı araştırma (Workflow `wf5b9c8qd`, run `wf_fcf7fbab-ad2`; 3 şerit: TR prevalans · global benchmark ·
> metodolojik fark). **Kanıt≠bağlam:** prevalans sayıları L2 tam-metin/birincil (`evidence`); assay/scoring/
> metodoloji `context`. RBŞ: her kohort kendi paydası (assay/evre/histoloji/EGFR-durumu) ile aktarıldı;
> uyumsuz paydalar havuzlanmadı. **Bu bölüm §G.2'deki tekil "%17,8 (Canaslan)" değerini bağlamlandırır ve
> düzeltir** — o değer TR aralığının alt ucudur, TR'nin temsili değeri değildir.

### I.1 Türkiye kohortları (all-comer, PD-L1-test edilmiş payda)

| Kohort | Yıl | N | Assay | PD-L1 ≥%50 | PD-L1 ≥%1 | Payda / not | Kaynak |
|---|---|---|---|---|---|---|---|
| **Dulger** (Onur) | 2024 | 501 | **22C3** | **%27,5** (138/501) | %69,3 | tüm-test edilmiş NSCLC, tüm evre; adeno %69,1 | 10.4103/ijpm.ijpm_939_23 |
| Gürbüz | 2022 | 384 | NR | %23,4 (">%50") | %64,8 | ileri evre; kesim ">%50" (≥ değil) | 10.5578/tt.20229803 |
| Söyler | 2023 | 369 | NR | %22,2 (82/369, "high") | %49,1 | çok-merkez; "high-positive"=≥50 çıkarımı | 10.1007/s11239-022-02753-y |
| **Canaslan/Bridging** | 2025 | 601 | NR (klon) | **%17,8** | %52,2 | **yalnız metastatik** (601/1023); driver-zengin → düşük uç | 10.3390/genes16121446 |
| Teoman *(havuzlanmaz)* | 2025 | 176 | SP263 | %12,5 (22/176) | %48,3 | **yalnız EGFR-mutant** — EGFR-mut düşük PD-L1 taşır | 10.3390/medicina61081467 |
| ESTIMATE *(context)* | 2025 | 636 | NR | strata **yapılmadı** | poz. %42,8 (test %55,5) | ulusal; TPS strata toplanmadı | 10.1080/14796694.2025.2527477 |

**TR all-comer 22C3/standart PD-L1≥%50 ≈ %22–28** (Dulger 22C3 %27,5 en sağlam). Canaslan %17,8 alt uçtadır:
metastatik-only + klon-NR + driver-zengin payda. Teoman %12,5 EGFR-mutant-only → all-comer'la **havuzlanamaz**.

### I.2 Global benchmark'lar (L2 birincil)

| Kaynak | Payda | Assay | PD-L1 ≥%50 | Not |
|---|---|---|---|---|
| **EXPRESS** (Dietel 2019) — *en iyi all-comer çapa* | 2368 test edilmiş ileri NSCLC, 18 ülke | **22C3** | **%22** (530/2368); bölgeler %21–24 tekdüze; **EGFR/ALK-WT %27** | 10.1016/j.lungcan.2019.06.012 |
| KEYNOTE-024 (Reck 2016) | **taranmış** popülasyon | 22C3 | **~%30** (kanonik tarama çapası; NEJM paywall, OA-doğrulanmadı) | 10.1056/NEJMoa1606774 |
| KEYNOTE-042 (Mok 2019) | ≥%1 **kayıtlı** içinde alt-grup | 22C3 | ≥50 ≈ kayıtlının ~%47'si (payda ≥1) | 10.1016/S0140-6736(18)32409-7 |
| IMpower110 (Herbst 2020) | kayıtlı SP142 ≥%1 | **SP142** | "high" TC≥50 **VEYA** IC≥10 — **22C3 ≥%50 ile kıyaslanamaz** | 10.1056/NEJMoa1917346 |
| EMPOWER-Lung 1 (Sezer 2021) | yerel ≥%50 ön-seçili ITT | 22C3 | %79 merkezi-teyit (**prevalans değil**, konkordans) | 10.1016/S0140-6736(21)00228-2 |

**Global all-comer 22C3 ≈ %22 (EXPRESS); EGFR/ALK-WT ≈ %27; taranmış-pivotal ≈ %30.** "%30" bir **tarama/zenginleştirilmiş**
figürdür; gerçek all-comer ~%22'dir.

### I.3 Metodolojik fark sürücüleri (context) — "18 vs 30" neden?

1. **Payda/case-mix (en büyük kaldıraç):** "%30" taranmış/ileri/sigara-zengin/skuamöz-dahil; all-comer veya adeno-ağır
   veya erken-evre-karışık payda mekanik olarak düşürür (erken-evre non-skuamöz Brezilya %13,3 — 10.1093/oncolo/oyac167).
2. **Assay:** SP142 tümör hücresini 22C3/28-8/SP263'ten **sistematik az** boyar (Blueprint 1&2: 10.1016/j.jtho.2016.11.2228,
   10.1016/j.jtho.2018.05.013; Maule: PD-L1+ olguların 22C3 %95,2 vs SP142 %32,2 — 10.1136/jitc-2022-005573). 22C3/28-8/SP263
   TC skorunda değiştirilebilir; SP142 ve IC-skorlaması değil.
3. **Okuyucu değişkenliği ≥50 kesiminde assay değişkenliğini aşar** (Brunnström 2017 — 10.1038/modpathol.2017.59).
4. **Biyoloji:** EGFR/STK11 ↔ PD-L1 negatiflik; KRAS/TP53/MET ↔ PD-L1 yüksek (Schoenfeld/Hellmann 2020 — 10.1016/j.annonc.2020.01.065);
   adeno-ağır/driver-test edilmiş payda ↓. TR'de PD-L1 EGFR-WT'de ve non-adenoda daha yüksek (10.4103/ijpm.ijpm_939_23, p=0,0002/0,044).
5. **Pre-analitik:** arşiv/eski FFPE, kemik metastazı (çoğunlukla PD-L1-negatif), sitoloji/küçük biyopsi ↓.

### I.4 Hüküm ve BP27 etkisi

> **Payda-eşleşmeli kıyas (F7-B/D düzeltmesi):** TR all-comer 22C3 **%27,5** (Dulger) vs global all-comer 22C3
> **%22** (EXPRESS) → TR üst uçta. Global EGFR/ALK-WT %27'dir; **TR-özgü EGFR/ALK-WT ≥50 değeri yok** → EXPRESS
> ile çapalanır (all-comer ile EGFR-WT paydaları karıştırılmaz).
> Yani **TR anormal derecede düşük DEĞİL;** "%18 vs %30" görünümü büyük ölçüde (a) global tarafta yanlış çapa
> (%30 taranmış-zenginleştirilmiş; gerçek all-comer ~%22) + (b) TR tarafında alt-uç kohort seçimi (Canaslan
> metastatik-only, driver-zengin, klon-NR) + (c) assay/scoring/case-mix artefaktından kaynaklanır.
>
> **BP27 için doğru çarpan:** 1L atezolizumab (SUT c)2 / KÜB: PD-L1≥%50 monoterapi) **hedef payı, EGFR/ALK-WT
> ileri NSCLC'nin ~%25–30'u** (TR Dulger %27,5 + global EXPRESS EGFR-WT %27) olarak alınmalı — **%17,8 kullanmak
> 1L PD-L1-yüksek havuzu ~%35 küçümser.** PD-L1≥%1 (durvalumab Evre III eşiği) ise TR ve global ~%50–52.
> *Not:* 2L atezolizumab (c)3) için PD-L1 eşiği **yoktur** (§H) — bu çarpan yalnız 1L monoterapi havuzunu ilgilendirir.

**`unverified` (dürüst):** KEYNOTE-024 %30,2 ve KEYNOTE-042 599/1274 tam-metinleri paywall (OA-doğrulanmadı) →
kanonik-rapor değeri olarak işaretli; EXPRESS + Blueprint + Fujimoto + Maule abstract/tam-metin doğrulandı.
TR Gürbüz/Söyler PD-L1≥%50 değerleri abstract-düzeyi (kesim/klon tam-metinle teyit edilmeli).
