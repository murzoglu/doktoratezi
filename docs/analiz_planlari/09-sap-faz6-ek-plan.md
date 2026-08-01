# Faz VI Ek Plan — Gelişimsel-Diadik Ölçüm Yüzeyi (Developmental–Dyadic Surface)

**Sürüm:** v0.2 (**YÜRÜTÜLDÜ / EXECUTED** — 2026-07-14) · **Tarih:** 2026-07-14
**Kapsam:** SAP KISIM LI (§142–151) — [KEŞİFSEL · POST-HOC]
**OSF katmanı:** Layer 7 (Open-Ended Registration amendment hedefi); sapma tablosu #6
**Kanonik baz:** `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` rev 2 (DEĞİŞMEZ)
**Modül:** `R/65_phase6_developmental_dyadic.R` (saf fonksiyon)
**Runner:** `scripts/R/59_phase6_developmental_dyadic_audit.R`
**Test:** `tests/test_phase6_developmental_dyadic.R` (`stopifnot`) — PASS
**Target:** `_targets.R` → `phase6_developmental_results` (`tar_validate` OK; kanonik CSV `format="file"` hash çapası; yeni veri girmez)
**Artefakt:** 14 `outputs/tables/phase6_*.csv`; n=241; 20 odak testin 7'si BH-FDR sonrası ayakta


---

## 0. Epistemik statü ve önceki fazlarla ilişki

Bu faz, Faz V (KISIM L, §136–141; [`docs/analiz_planlari/08-sap-faz5-ek-plan.md`](08-sap-faz5-ek-plan.md)) ile ilan edilen bütünleştirici keşfin **ardından, yazar/klinisyen talebiyle** eklenen bir katmandır. Odağı, önceki beş fazın (KISIM I–L) geride bıraktığı iki eksendir:

1. **Gelişimsel ölçüm ekseni** — çocuğun ebeveynlik algısının ve bu algının anne-raporuyla uyumunun, çocuğun *yaşına/bilişsel olgunluğuna* göre nasıl değiştiği. Önceki fazlar `cocuk_yas`'ı yalnız kovaryat veya düzey-yordayıcısı (H1 üç-yönlü) olarak kullandı; **algının/uyumun kendisinin yaş-koşullu geçerliği** hiç modellenmedi.
2. **Kronik-hastalık diadik yükü ekseni** — indeks çocuğun zamansal hastalık yükünün, *sağlıklı kardeşin algısına* ve *annenin distres zaman-çizgisine* taşınması. Önceki fazlar hastalık yükünü indeks-ebeveynlik (R/27) düzleminde ele aldı; **kardeş-algı düzlemine** ve **anne-distres zaman-çizgisine** taşımadı.

**Kurallar (tüm önceki fazlarla iç-tutarlı):** YENİ VERİ YOK; kanonik kilit DEĞİŞMEZ; H1–H5 confirmatory çekirdek DEĞİŞMEZ. Tüm çıktılar korelasyoneldir; **nedensel dil yasaktır** (kesitsel tasarım). Çoklu karşılaştırma her paragraf içinde **BH-FDR** ile ele alınır. **HARKing yasağı** (Skill Davranış Kuralı 20): hiçbir Faz VI bulgusu H1–H4 confirmatory prior'ını güçlendirmez. **Plan aşamasında `02-sapma-tablosu.md`'ye satır EKLENMEZ** (sapma = uygulanan değişiklik; yürütme onaylanınca #5 satırı + OSF Layer 7 amendment eklenir).

**Faz V ile köprü (kritik):** Faz V §137'nin çekirdek bulgusu — a-yolu (Beck→EMBU-P) anlamlı ama **b-yolu (EMBU-P→EMBU-C) tüm boyutlarda zayıf, hiçbiri anlamlı değil** ([`08-sap-faz5-ek-plan.md`](08-sap-faz5-ek-plan.md) §137) — Faz VI'nın çıkış hipotezidir: bu "null transmisyon" ortalamada mı sıfır, yoksa çocuğun yaşına göre gizleniyor mu? §142 bu soruyu doğrudan test eder.

---

## 1. Boşluk provenansı — Hangi eksen × neden kullanılmadı

Kaynak: KISIM I–L kapsamı (`03`–`08` planları) + `_targets.R` (R/00–R/64) hedef taraması.

| Eksen / türetim | Önceki kullanım | Faz VI fırsatı |
|---|---|---|
| `cocuk_yas` × anne-çocuk uyumu (H5) | H5/H5ext: Beck moderasyonu, MTMM, sibling-ICC ([`R/20`], R/39) — yaş yok | **§142 — uyumun gelişimsel moderasyonu** |
| `cocuk_yas` × b-yolu (EMBU-P→EMBU-C) | Faz V §137 yalnız ortalama b-yolu | **§142 — transmisyonun yaş-koşullu darboğazı** |
| `DM_Hasta_Kardes` vs `Kontrol_Kardes` × şiddet/süre | H1 rol kontrastı (düzey) | **§143 — koruma-genelleşme vs tükenme çerçevesi** |
| `beck_total` ~ `dm_yili` (Beck = *çıktı*) | Beck her yerde yordayıcı/aracı; tanı-zaman-çizgisinin çıktısı değil | **§144 — maternal distres adaptasyon eğrisi (DM-only)** |
| `srq_ho_warmth_mean` = *moderatör* | Faz V §136 SRQ = *çıktı* (Beck→SRQ null) | **§145 — kardeş sıcaklığı tampon/moderatör** |
| indeks-EMBU-C + kardeş-EMBU-C + anne-EMBU-P birlikte (triadik konfigürasyon) | LPA (R/24) aile-göstergeli tek-perspektif | **§146 — triadik aile-iklimi tipolojisi** |
| Bland-Altman bias **yönü** × grup | H5 Bland-Altman büyüklük/limitler ([`R/20`]); yön×grup yorumu ayrık değil | **§147 — uyumsuzluk yönü (suçluluk/sosyal istenirlik)** |

---

## 1.5. Fizibilite ve veri-gerçeklik denetimi *(ÖN-KOŞUL — yürütmeden önce zorunlu kapı)*

> **İlke (Faz III/IV/V'ten devralınan):** Bir eksenin kanonik bazda *bulunması* onun *modellenebileceğini* garanti etmez. Aşağıdaki denetim yürütme öncesi zorunludur; yalnız **agregat frekans/güvenilirlik** çıkarır (satır-düzeyi PII dökülmez).

### 1.5.1 Önceki fazlardan bilinen, yeniden-kullanılabilir sayımlar

| Değer | Kaynak |
|---|---|
| Tanı-yaşı bantları (DM n=120): <6:34 / 6–10:59 / >10:27 | [`07-sap-faz4-ek-plan.md`](07-sap-faz4-ek-plan.md) §1.5.2-SONUÇ-3 |
| `anne_antidepresan`=1: **46** (DM 35 / Kontrol 11) | [`06-sap-faz3-ek-plan.md`](06-sap-faz3-ek-plan.md) §1.5.2 |
| Faz V §137 b-yolu (EMBU-P→EMBU-C): tüm boyutlarda \|b\|≤0,10, anlamsız | [`08-sap-faz5-ek-plan.md`](08-sap-faz5-ek-plan.md) §137 |
| `kalabalik_indeksi` birleşik modelde bağımsız değil | [`08-sap-faz5-ek-plan.md`](08-sap-faz5-ek-plan.md) §138 |
| Örneklem: family 241×288 / long 482×203; lock rev 2 | [`docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`](../protokol/FINAL_REFERENCE_VERI_HARITASI.md) |

### 1.5.2 Yürütme öncesi çıkarılacak YENİ agregat sorgular (henüz yok)

Plan onaylanınca kanonik CSV üzerinde **salt-okunur agregat** olarak çıkarılacak; her biri ilgili §'nin fizibilite tavanını sabitler:

1. **§142 — `cocuk_yas` dağılımı × uyum-çifti kapsaması:** anne↔indeks diadında geçerli `embu_p`+`embu_c_idx` çifti olan aile sayısı; `cocuk_yas` medyan/IQR + yaş-terzil hücreleri. Etkileşim için terzil-başına n<40 ise yaş sürekli tutulur (bantlama yok).
3. **§144 — `dm_yili` dağılımı (DM-only):** medyan/IQR + histogram-benzeri agregat; spline knot yerleşimi için çeyreklikler; `beck_total` eksik-item sonrası geçerli n.
4. **§145 — `srq_ho_warmth_mean` × uyum kesişimi:** moderatör × H5-uyum çifti geçerli aile n'i; warmth dağılım çeyreklikleri.
5. **§146 — triadik tam-kayıt n'i:** anne-EMBU-P + indeks-EMBU-C + kardeş-EMBU-C üçünün de geçerli olduğu aile sayısı (LPA girdi tabanı); sınıf-oranı ≥%10 ön-koşulu Faz V/IV LCA desenine göre.
6. **§147 — Bland-Altman yön çifti:** anne↔indeks diadında işaretli bias hesaplanabilen aile n'i × `group_f` çapraz-tablosu.

### 1.5.3 Beklenen yeniden-sınıflandırmalar (ön-görü — 1.5.2 sonuçlarıyla kesinleşir)

| § | Ön-görülen Tier | Gerekçe |
|---|---|---|
| §142 yaş × uyum/transmisyon | **A/B** | n=482 çocuk-satırı / 241 diad; temiz sürekli moderatör; Faz V §137 ile doğrudan köprü |
| §143b koruma-genelleşme vs tükenme | **B** | rol kontrastı temiz (H1 tabanı); şiddet/süre ile ölçekleme keşifsel |
| §144 Beck ~ dm_yili | **C — DM-only** | n=120, kesitsel psödo-trajektuvar; spline df=3 |
| §145 kardeş sıcaklığı moderatör | **C** | etkileşim düşük güçlü; TOST + simr karakterizasyonu |
| §146 triadik tipoloji | **B/C** | sınıf-kararı hassas; entropy+BLRT+klinik yorumlanabilirlik |
| §147 uyum yönü × grup | **B** | n=241 diad; Bland-Altman altyapısı (R/20) hazır |

### 1.5.4 Yapısal düzeltmeler / kimliklenebilirlik notları

- **(D1) Uyum hangi diad?** H5 birincil diadı **anne ↔ indeks çocuk**tır ([`R/20`]). §142/§147 yaş/yön için indeks çocuğun `cocuk_yas`'ı kullanılır; anne↔kardeş diadı (H5ext sibling-ICC tabanı) **duyarlılık** katmanı olarak kardeşin yaşıyla paralel koşulur.
- **(D3) Beck konumu.** Beck yalnız index/anne satırında; §144 aile-düzeyi DM-only. Tek eksik item → `beck_total` NA kuralı korunur (Davranış Kuralı 5).
- **(D5) §138 çakışma önlemi.** Aşırı korumanın sosyodemografik gradyanı Faz V §138'de kapandı; §143'te aşırı koruma yalnız *kardeş × hastalık-yükü* ekseninde ele alınır, SES gradyanı tekrar açılmaz.

---

# KISIM LI — GELİŞİMSEL-DİADİK ÖLÇÜM YÜZEYİ

## §142. Çocuk yaşı × anne-çocuk uyumu ve transmisyon darboğazı [Tier A/B]

**Boşluk.** H5/H5ext uyumu Beck, MTMM ve sibling-ICC ile moderasyonladı; **çocuk yaşıyla** moderasyonlamadı. Faz V §137 b-yolunu (EMBU-P→EMBU-C) ortalamada zayıf buldu ama yaş-koşulunu test etmedi.

**Hipotez (gelişimsel).** Perspektif-alma kapasitesi yaşla artar → (i) anne-çocuk algı uyumu yaşla yükselir; (ii) §137'nin "null b-yolu" bir *ortalama* eseridir: transmisyon büyük çocukta pozitif, küçük çocukta ≈0 → ortalama alınca maskelenir.

**Yöntem.**
- **Uyum modeli:** H5 diadik uyum tahmincilerine (ICC bileşenleri, Bland-Altman içi-diad fark, k-katsayısı; [`R/20`]) `cocuk_yas` moderatörü. Aile-düzeyi: `abs_dyad_diff_altölçek ~ cocuk_yas_z + group_f + ses_latent_z` (düşük fark = yüksek uyum) + RSA-uyumlu duyarlılık.
- **Transmisyon modeli (Faz V §137 uzantısı):** her EMBU alt ölçeği için `embu_c_idx_mean ~ embu_p_mean * cocuk_yas_z + anne_yas_z + ses_latent_z + group_f` (family). Odak: `embu_p × cocuk_yas` etkileşimi (b-yolunun yaş-eğimi).
- **Duyarlılık:** anne↔kardeş diadı kardeş yaşıyla paralel (D1); sürekli yaş vs terzil (1.5.2-1'e göre).

**Estimand.** Çocuk yaşının, anne-çocuk algı uyumu ve anne-rapor→çocuk-algı transmisyonu üzerindeki (moderatör) etkisi.
**Etki büyüklüğü.** Etkileşim β + %95 GA; uyum için ΔICC; SESOI |r|≈,10 ([`06-sap-faz3-ek-plan.md`](06-sap-faz3-ek-plan.md) §96.4 standardı).
**Tedbir.** Çoklu karşılaştırma (4 alt ölçek × 2 model) → BH-FDR; ortalama+medyan; kesitsel → "gelişimsel eğim" ihtiyatlı, "olgunlaşıyor" değil "yaşla ilişkili"; ters-nedensellik (uyumlu diad → daha açık iletişim) tartışılır. Düşük etkileşim gücü → **simr karakterizasyonu + TOST** (null için |r|≈,10).
**Çapa (aday — referans-kapısı tam-metin doğrulaması bekliyor).** De Los Reyes & Kazdin informant-uyuşmazlığı çerçevesi; gelişimsel perspektif-alma literatürü. *(EK.)*

## §143. "Cam kardeş": indeks hastalık-yükü → sağlıklı kardeşin algısı [Tier C/D — betimsel]


**Yöntem (aile düzeyi, D2).**

**Estimand.** İndeks hastalık-yükünün, sağlıklı kardeşin algıladığı ebeveynlik boyutlarıyla (betimsel) ilişkisi ve yönü.
**Kritik uyarı.** Kesişim ≤39 (1.5.1) **ve MNAR seçilim** (OR≈4,56) → §143a **betimsel + geniş GA**, çıkarımsal iddia yok, **imputasyon yasak** (Davranış Kuralı 19). §143b daha güçlü (rol kontrastı temiz) ama ölçekleme kısmı DM-only düşük güçlü.
**Tedbir.** BH-FDR (3 boyut); ortalama+medyan; "seyrelme" nedensel değil ilişkisel; n her hücrede raporlanır.
**Çapa.** Kaynak-seyrelmesi — Downey (Faz III tam-metin doğrulı, [`06-sap-faz3-ek-plan.md`](06-sap-faz3-ek-plan.md) §1.5.5); kronik-hastalık kardeş uyum riski — Sharpe & Rossiter (aynı kaynak, düzeltilmiş: içe-yönelim d≈0,41 / dışa-yönelim d≈0,15).

## §144. Maternal distres zaman-çizgisi: Beck ~ tanıdan bu yana süre [Tier C — DM-only]

**Boşluk.** Beck her yerde yordayıcı/aracı; tanı-zaman-çizgisinin **çıktısı** olarak modellenmedi. `dm_yili` spline'ı yalnız *ebeveynlik* çıktısına kuruldu (R/27).

**Yöntem.** `beck_total ~ ns(dm_yili, 3) + anne_yas_z + ses_latent_z` (DM-only, n=120). Non-monotonik şekil (tanıya yakın dönemde yüksek distres olasılığı) betimsel tanımlanır; knot yerleşimi çeyreklik (1.5.2-3).
**Estimand.** Anne depresyon düzeyinin, çocuğun tanısından bu yana geçen süreyle (non-lineer) betimsel ilişkisi.
**Kritik uyarı.** **Kesitsel** → kişiler-arası psödo-trajektuvar; "aynı anne iyileşiyor" DENMEZ, yalnız "tanısı yeni olan anneler bu örneklemde daha yüksek distres bildiriyor". Eğrinin tepe-konumu **analizin çıktısıdır, önceden varsayılmaz.**
**Tedbir.** Ortalama+medyan; spline vs lineer LRT; grup yok (DM-only) → Simpson denetimi `anne_yas`-bandı ekseninde; sahte-kesinlik (df=3'ün ötesinde knot artırma yok).
**Çapa.** T1DM'de maternal distresin yükseldiği yön — Van Gampelaere ve ark. 2020 (Faz III tam-metin doğrulı, [`06-sap-faz3-ek-plan.md`](06-sap-faz3-ek-plan.md) §1.5.5: yalnız annelerde↑ stres/depresyon/kaygı; suboptimal glisemik kontrol→↑maternal distres). *Büyüklük/tepe iddiası bu kaynaktan türetilmez; tezin kendi kestirimidir.*

## §145. Kardeş sıcaklığı: tampon/moderatör modeli [Tier C]

**Boşluk.** Faz V §136 SRQ'yu *çıktı* yaptı (Beck→SRQ null); SRQ'yu *moderatör* yapan kurulum yok. Çocuk-düzeyi ruh sağlığı çıktısı olmadığından (bkz. §3 Sınırlılıklar) klasik "tampon→daha iyi çocuk" zinciri kurulamaz; bunun yerine **veride-mevcut** iki hedef moderasyonlanır.

**Yöntem.** `srq_ho_warmth_mean` (aile-düzeyi, iki çocuğun ortalaması + duyarlılıkta ayrı) moderatör:
- (i) **uyum üzerinde:** §142 anne-çocuk uyumu × kardeş-sıcaklığı — sıcak kardeş bağı olan ailelerde diad daha mı uyumlu?
- (ii) **transmisyon üzerinde:** §142 b-yolu × kardeş-sıcaklığı — sıcak ailede anne-rapor→çocuk-algı daha mı hizalı?

**Estimand.** Kardeş ilişki sıcaklığının, diadik uyum/transmisyon üzerindeki (moderatör) betimsel etkisi.
**Kritik uyarı.** Etkileşim düşük güçlü; çocuk-çıktısı yokluğu nedeniyle "koruyucu" yorumu spekülatiftir.
**Tedbir.** TOST (|r|≈,10) + simr; BH-FDR; "tampon" etiketine spekülatif damgası; nedensel dil yok.
**Çapa (aday — referans-kapısı bekliyor).** Kardeş-ilişkisi tampon/telafi literatürü. *(EK.)*

## §146. Triadik konfigürasyonel aile-iklimi tipolojisi [Tier B/C]

**Boşluk.** LPA/LCA (R/24) aile-göstergeli ve tek-perspektiflidir; **üç sesin birlikte konfigürasyonu** (anne-EMBU-P + indeks-EMBU-C + kardeş-EMBU-C) bir tipolojiye çevrilmedi. Bu, PDT (§96) ve concordance'ı (§63) tek bir klinik-yorumlanabilir nesnede birleştirir.

**Yöntem.** tidyLPA/mclust ile aile-profil analizi; göstergeler: anne + indeks + kardeş sıcaklık/reddetme/aşırı koruma standardize skorları. Sınıf-kararı: BIC + entropy + BLRT + LMR-LRT + **klinik yorumlanabilirlik** (beklenen tipler: *uyumlu-sıcak*, *indeks-kayrılan*, *kardeş-kayrılan*, *uyumsuz-soğuk*). Grup dağılımı (DM/Kontrol) sınıflar arası betimsel.
**Estimand.** Ailelerin, üç-perspektifli ebeveynlik-algı konfigürasyonuna göre betimsel tipolojisi.
**Kritik uyarı.** n=241'de çok-göstergeli LPA sınıf-kararı hassas; en az %10 sınıf-oranı ön-koşulu (1.5.2-5). Etiketler **betimsel, tanı değil** (Davranış Kuralı 16).
**Tedbir.** Tam sınıf-uydurma dağılımı + entropy raporlanır; cherry-pick yok; profil etiketi klinik öneri olarak sunulmaz.
**Çapa.** Latent profil seçim kriterleri — proje LPA standardı ([`R/24_latent_profile.R`] / skill `latent-degisken-yontemleri.md`).

## §147. Uyum yönü: Bland-Altman bias × grup [Tier B]

**Boşluk.** H5 Bland-Altman büyüklük/limitleri verir ([`R/20`]); **işaretli bias'ın grup-koşullu yorumu** (anne mı yoksa çocuk mu daha fazla sıcaklık/koruma bildiriyor, ve bu grupla değişiyor mu?) ayrık estimand değil.

**Yöntem.** Diad-düzeyi işaretli bias `anne − indeks` (alt ölçek başına) → betimsel yön + `group_f` karşılaştırması (t/Welch + Cohen d). Öngörü (hipotez, tek-yönlü değil): DM annelerinde suçluluk/sosyal-istenirlik kaynaklı **sıcaklık öz-yüceltmesi** (anne > çocuk) daha belirgin olabilir; ters yön eşit-olası ve TOST ile ayrık test edilir.
**Estimand.** Anne-çocuk algı-uyumsuzluğunun *yönünün* grupla betimsel ilişkisi.
**Tedbir.** BH-FDR (4 alt ölçek); "sosyal istenirlik" yorumu spekülatif damgalı (ayrık sosyal-istenirlik maddesi yok); ortalama+medyan; nedensel dil yok.
**Çapa.** İnformant vantaj-noktası farkı yön-yorumu — De Los Reyes Operations Triad + Coldwell-Pike-Dunn (Faz III/IV tam-metin doğrulı, [`06-sap-faz3-ek-plan.md`](06-sap-faz3-ek-plan.md) §1.5.5).

---

## §148. BH-FDR ve kapanış-uzlaşması

- Paragraf-içi BH-FDR: §142 (8 test: 4 alt ölçek × 2 model), §143 (3 boyut), §145 (2 hedef), §147 (4 alt ölçek). §144 tek model-ailesi; §146 tipoloji (test değil).
- **Kapanış (#4/#5) ile tutarlılık:** Faz VI, Faz V'in "yeni confirmatory sinyal yok" kapanışını **geçersiz kılmaz**; katkısı (i) §137 null-transmisyonuna gelişimsel açıklama (§142), (ii) az-işlenmiş diadik/kronik-yük yüzeylerinin belgelenmesi, (iii) klinik-yorumlanabilir bütünleştirici çerçevelerdir (§143 cam-kardeş, §146 tipoloji). Beklenen sonuçların çoğu ya mevcut örüntüyü **doğrular** ya da **bilgilendirici null**'dur.

## §149. Öncelik kademeleri (değer × fizibilite)

Yürütme sırası: **§142 → §147 → §146 → §144 → §143 → §145**.
- **§142** en yüksek getirili (temiz güç n=482, Faz V §137 ile doğrudan köprü, ölçüm-geçerliği jüri savunmasına hizmet).
- **§147** temiz (n=241 diad, R/20 altyapısı hazır).
- **§146/§144** orta (sınıf/df kararı hassas; §144 DM-only).
- **§143** en düşük güçlü (kesişim ≤39, MNAR) ama en yüksek klinik anlatı → **betimsel-öncelikli**.
- **§145** en zayıf (etkileşim gücü + çocuk-çıktısı yok) → keşifsel.

## §150. Disiplin — R modülü, targets, test, OSF

- **Modül:** `R/65_phase6_developmental_dyadic.R` (saf fonksiyon; dosya I/O yok). Girdi: R/20 (H5 uyum), R/23 (mediasyon/transmisyon altyapısı), R/24 (LPA) çıktıları + `df_family_ses`/`df_long_scored`/`df_family_scored`.
- **Runner:** `scripts/R/59_phase6_developmental_dyadic_audit.R` → `outputs/tables/phase6_*.csv`.
- **Test:** `tests/test_phase6_developmental_dyadic.R` (`stopifnot`); seed = 20260714.
- **Target:** `_targets.R` → `phase6_developmental_results` (+ per-§ CSV `format="file"`); kanonik `family_csv`/`long_csv` hash çapasına bağımlı; **kanonik CSV dokunulmaz.**
- **OSF:** yürütme onaylanınca Layer 7 amendment + `02-sapma-tablosu.md` #5 (Tip 3, post-hoc keşifsel).
- **renv/hash:** yeni paket eklenmez (mevcut yığın: lme4/lavaan/tidyLPA/mgcv-ns/effectsize/TOSTER/simr yeterli); `renv.lock` dokunulursa commit'te gerekçelenir.

## §151. Tedbir-ve-hatalar aktif denetim (Faz VI'ya özel)

- [ ] Kesitsel → nedensel dil yok; "gelişimsel eğim/adaptasyon eğrisi" ihtiyatlı, ters-nedensellik tartışılır (§142, §144).
- [ ] Çoklu karşılaştırma: her paragraf içi BH-FDR (§148).
- [ ] Simpson: §142 grup×yaş; §144 anne_yas-bandı; §147 grup içi/havuzlanmış.
- [ ] Null iddialar (§142 transmisyon, §145 tampon) **TOST + simr** ile, ham-anlamsızlıkla değil.
- [ ] Baba ebeveynlik davranışı ölçülmedi → §142/§147 "anne-çocuk ekseni", §146 "anne + çocuk algısı" etiketi.
- [ ] LPA etiketleri betimsel, klinik tanı/öneri değil (§146; Davranış Kuralı 16).
- [ ] HARKing: hiçbir bulgu H1–H4 prior'ını güçlendirmiyor; tümü `[KEŞİFSEL·POST-HOC]`.

---

## 2. Tez artefaktı haritası

| Belge | Konum | İçerik |
|---|---|---|
| Yöntem | `chapters/03_gerec_ve_yontem.qmd` keşifsel-katman enümerasyonu | Faz VI bir madde |
| Bulgular | `chapters/04_bulgular.qmd` §4.4.8 (yeni) | Sayısal bulgu + tablo göndermesi, [KEŞİFSEL] |
| CSR | `docs/CLINICAL-STUDY-REPORT-FINAL.md` §16.17 + §16.2 kanıt matrisi satırı | Ayrıntılı rapor + CSV provenansı |
| Tartışma | `chapters/05_tartisma_ve_sonuc.qmd` keşifsel-katman paragrafı + sınırlılık | Gelişimsel-diadik yorum, "öneri/hipotez-üretici düzeyde" |

## 3. Sınırlılıklar


---

## EK — Literatür çapaları (referans-kapısı tam-metin doğrulaması bekliyor)

Yürütme öncesi `/referans-kapisi` ile doğrulanacak; doğrulanmayan künye `references.bib`'e eklenmez (Davranış Kuralı 20; "VERİ BULUNAMADI" ise düşer). Faz III/IV/V'te zaten tam-metin doğrulı çapalar (Van Gampelaere 2020, Downey 1995, Sharpe & Rossiter 2002, Coldwell-Pike-Dunn 2008, De Los Reyes Operations Triad, Lakens TOST) yeniden-kullanılır; yalnız §142 (gelişimsel uyum/transmisyon) ve §145 (kardeş tampon) için yeni çapa doğrulaması gerekir.
