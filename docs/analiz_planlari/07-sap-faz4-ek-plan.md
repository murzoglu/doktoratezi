# EK İSTATİSTİK PLANI — FAZ IV (ARTIK DEĞİŞKEN YÜZEYLERİ · POST-HOC)

**Sürüm:** v0.4 (**YÜRÜTÜLDÜ / EXECUTED** — 2026-07-08; tüm KISIM'lar R/56-R/62 modülleriyle koşuldu, 49 `phase4_*.csv` üretildi, CSR-FINAL §16.8-16.15'e temiz-nihai biçimde entegre edildi) · **Tarih:** 2026-07-08
**v0.2 → v0.3 farkı:** Bağımsız ampirik veri-provenans probu (ham 482×158 + kanonik final) dört
bulgu üretti ve **hepsi kanonik CSV üzerinde birebir doğrulandı**: (1) **HbA1c MNAR seçilim** —
DM'de HbA1c varlığı AD kullanımıyla güçlü ilişkili (Fisher OR=4,56 [1,84–11,70], p=0,000466;
tam n=39/%32,5) → HbA1c bir *seçilmiş alt-örneklem*; (2) **anket yılı × grup ağır kollinearite**
(2023: DM108/K40, 2024: DM6/K36, 2025: DM6/K45; logistic p≈1,3e-12) → batch/temporal confound;
(3) **AD ↔ düşük güncel Beck** (9,56 vs 14,71; Welch p=0,000128) → AD tedavi/temas göstergesi,
şiddet değil (→ §130 **düzeltildi**); (4) **5 DM ailede dm_yili>çocuk yaşı + 1 negatif kardeş
tanı-yaşı** → mantık maskesi zorunlu. Sonuç: iki **yeni geçerlik-denetimi** eklendi (**KISIM XLIX**,
§134–135); §130 tedavi×şiddet 2×2'ye düzeltildi; §101/§122 rafine edildi. Bunlar **kullanılmayan
değişken değil, mevcut/planlı analizlerin geçerlik tehdidi** — CSR-düzeyi etkileri §1.8'de.
**Durum (v0.4):** ✅ **YÜRÜTÜLDÜ.** Fizibilite denetimi (§1.5) koşuldu (§1.5.2-SONUÇ), Evidentia
native-first tam-metin doğrulaması (EK) tamamlandı (6 çapa DOI/PMID-teyitli, `references.bib`'e
işlendi), tüm KISIM'lar R/56-R/62 saf-fonksiyon modülleriyle koşuldu (`scripts/R/57_phase4_audit.R`;
7 `phase4_*` targets hedefi, modül+regresyon testleri PASS,
49 `outputs/tables/phase4_*.csv` üretildi. Sonuçlar CSR-FINAL §16.8-16.15 (+§17.7/§18.1/§18.4/§12.5)
metnine temiz-nihai (aşamasız) biçimde entegre edildi. Sapma tablosu #4 (OSF Layer 5). Kanonik kilit
rev 2 DEĞİŞMEDİ; YENİ VERİ toplanmadı.
**v0.1 → v0.2 farkı:** İkinci-görüş post-hoc aday listesi (2026-07-08) kod-footprint'iyle
mutabık kılındı (§1.7). Çoğu madde **Faz III'te zaten kapsanmış** olarak işaretlendi (tekrar
açılmaz); **üç madde gerçekten yeni** çıktı ve eklendi: (a) **maternal mental-sağlık yükü →
ÇOCUK algı düzlemi** (AD + BDI≥17 klinik-risk stratumu → EMBU-C; grep `anne_antidepresan ×
embu_c` = **0 dosya**); (b) **informant discrepancy → SRQ** (R/33 discrepancy'yi *yordanan*
tutar, kardeş çıktısına *yordayıcı* bağlamaz); (c) **latent Beck-sınıfı dışsal doğrulaması**
(R/24 `predclass` standalone; EMBU-C/SRQ/AD ile çaprazlanmamış). Bunlar **KISIM XLVIII**
(§130–133) olarak eklendi ve §128 yürütme sırasında öne alındı.
**v0.1 kapsamı:** Ana SAP v3.0 (KISIM I–XVIII), Faz II (`04-sap-faz2-posthoc.md`, KISIM
XIX–XXXV) ve **Faz III (`06-sap-faz3-ek-plan.md`, KISIM XXXVI–XLI, §96–115) dışında** kalan;
kanonik bazda **mevcut/türetilmiş ama hiçbir modele hiç girmemiş** (veya yalnız kovaryat
olarak kullanılmış) değişken yüzeylerini disiplinli keşif çerçevesinde ele alır.

**Veri:** Mevcut `FINAL_REFERENCE__analysis_base_{family,long}.csv` (family: 241 satır × 288
kolon; long: 482 satır × 203 kolon; kilit SHA-256 doğrulandı,
`FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`). **Yeni veri toplanmaz. Kanonik kilit
DEĞİŞMEZ.**

**Epistemik statü:** Tüm analizler **[KEŞİFSEL · POST-HOC]** — Tip 3 sapma, OSF **Layer 5**
(yeni). H1–H4 doğrulayıcı kanıt kademeleri (CSR Bölüm 11) **DEĞİŞMEZ**; hiçbir Faz IV analizi
confirmatory prior'ı güçlendirmez (HARKing yasağı, Skill Davranış Kuralı 20). Faz III ile
**içerik olarak örtüşmez**: Faz III sosyodemografik-klinik formu taradı; Faz IV, *o taramanın
bile geride bıraktığı* ölçek-içi granülerlik, çocuk-düzeyi moderatör ve veri-geçerlik
yüzeylerini ele alır.

---

## 0. ÖN UYARI — Faz IV Ne DEĞİLDİR

- **Faz III'ün tekrarı değildir.** Faz III'ün kapadığı yüzeyler (materyal facet, EGP/ISEI/SIOPS
  yarışı, eğitim homogamisi, anne istihdamı, FSM, doğum sırası, `same_sex`/`age_gap`, anne-vs-baba
  kayırma §98, HbA1c ortak modeli, tanı yaşı DM alt-analizi) **yeniden açılmaz.**
- **H1–H4'ü yeniden açmaz.** Confirmatory estimand, outcome ve model aileleri sabittir.
- **Yeni ölçek/ölçüm/veri eklemez.** Yalnız `FINAL_REFERENCE__*` içinde hâlihazırda kayıtlı
  veya ondan aritmetik olarak türetilebilir alanları modeller.
- **Fizibilite tavanının ötesine geçmez.** §1.5 hücre-sayısı/güvenilirlik denetimi birkaç
  yüzeyi "çıkarımsal" iddiadan "betimsel/geçerlik-kontrolü"ne indirir; bu güç-dürüstlüğü
  Faz IV'ün jüri savunmasının çekirdeğidir.
- **Klinik öneri üretmez.** Her bulgu hipotez-üretici; bağımsız Türk kohortunda dış-validasyon
  olmadan yükseltilmez.

> **Neden gerekli?** Faz III sosyodemografik-klinik formu *blok düzeyinde* taradı; ancak üç
> yüzey geride kaldı: (1) **SRQ birinci-derece 16 faseti** (§117 partiality-hariç 14'ünü kullanır) kanonik CSV'ye türetilip kilitlendi
> (`derived_score_dictionary.csv`) ama tüm analiz kodunda `srq_fo_*` kullanımı **sıfırdır** —
> tüm modeller 4 üst-boyuta (warmth/status/conflict/rivalry) çöker ve özellikle **yön
> asimetrisini** (bakım/güç *kimden kime*) ortalayarak siler; (2) **çocuk cinsiyeti** ve **anne
> yaşı** onlarca modülde yalnız *kovaryat* olarak geçer, hiçbir yerde *odak* moderatör/yordayıcı
> değildir; (3) **komorbidite matrisinin kategori-detayı** (14 anne + 14 eş) ve **öz-bildirim
> ikili sağlık göstergeleri** betimsel/geçerlik düzeyinde bile sunulmadı.

---

## 1. BOŞLUK PROVENANSI — Hangi Değişken/Türetim × Neden Kullanılmadı

Kaynak: değişken envanteri (family 288 / long 203 kolon) × analiz kod footprint'i taraması
(`R/00`–`R/55` + `scripts/R/`, 2026-07-08). "Kullanım" sütunu grep-doğrulı.

| Değişken / türetim (kanonik) | Kod footprint'i | Faz III | Faz IV fırsatı |
|---|---|---|---|
| `srq_fo_*` + `srq_sib_fo_*` (16 birinci-derece faset × iki informant; §117 partiality-hariç 14) | **0 analiz dosyası** (yalnız R/10 türetim) | üst-boyut §98/§109 | **Yönlü bakım/güç asimetrisi + granüler faset profili (§116–117)** |
| `nurturance_by_sib` vs `nurturance_of_sib`; `dominance_by/of`; `admiration_by/of` | üst-boyut `status`/`warmth` **ortalıyor** (R/10 `srq_higher_order_map`) | ✗ | **Bakım/güç yönü (§116)** — kronik-hastalık diadının çekirdeği |
| `katilimci_cocuk_cinsiyet` / `cinsiyet_f` | kovaryat (R/16, R/52, mediation, multiverse) | kovaryat | **Cinsiyet-odaklı diferansiyel ebeveynlik moderasyonu (§119)** |
| `anne_yas` | 27 dosyada **yalnız `_z` kovaryat** | kovaryat | **Anne-yaşı substantif gradyanı (§120)** |
| `tani_yas` (tanı yaşı) | R/27, R/40, R/55 (DM alt-analiz) | §111 **eskiz** | **Gelişim-penceresi × ebeveynlik/kardeş (§121)** — eskizden çıkarımsala |
| `hba1c` (SES/komorbidite yordayıcısı olarak) | kovaryat (R/40:129, R/27:48) | ortak model | **Metabolik kontrolün sosyodemografik gradyanı (§122)** — odak estimand |
| `anne_hastalik_*` 12/14 + `es_hastalik_*` 14/14 sistem-özgü | **0 dosya** (yalnız `otoimmun`/`endokrin`/`kategori_sayisi` R/53) | kısmi | **14-kategori betimsel prevalans paneli (§123)** |
| `kronik_hastalik_durumu` / `esiniz_kronik_hastalik_durumu` (ikili öz-bildirim) | PS kovaryatı / standardizasyon (R/04,05,15) | ✗ | **Öz-bildirim ↔ kodlanmış komorbidite uyumu (§124)** — veri-geçerlik |
| Ebeveyn yaş farkı (`anne_dogum_tarihi` − `es_dogum_tarihi`) | **türetilmemiş** | ✗ | **Assortatif yaş-farkı kovaryatı/moderatörü (§125)** |
| İşaretli kardeş yaş-yönü (DM'li çocuk büyük/küçük) | `age_gap` mutlak kullanılıyor | ✗ | **İşaretli yön × bakım asimetrisi (§118, G1 uzantısı)** |

**Not — üst-boyut çökme mekanizması (kritik provenans):** `srq_higher_order_map()` (R/10)
`status` üst-boyutunu `nurturance_by + nurturance_of + dominance_by + dominance_of` (12 madde)
olarak tanımlar; bu tanım gereği **yön simetrikleştirilir** — "sağlıklı kardeş DM'li çocuğa
bakım veriyor" ile "DM'li çocuk kardeşe bakım veriyor" aynı skorda toplanır. Aynı biçimde
`warmth` içinde `admiration_by` + `admiration_of` yönü kaybolur. Faz IV §116 bu yönü, zaten
türetilmiş faset ortalamalarından **geri açar**; yeni ölçüm gerekmez.

---

## 1.7. İKİNCİ-GÖRÜŞ POST-HOC LİSTESİ MUTABAKATI *(2026-07-08)*

Bağımsız bir ikinci-görüş aday listesi kod-footprint'iyle karşılaştırıldı. Her madde üç statüden
birine düşer: **ZATEN FAZ III** (tekrar açılmaz), **FAZ IV v0.1** (bu planın ilk sürümünde
vardı), **YENİ v0.2** (mutabakattan sonra eklendi).

| İkinci-görüş maddesi | Statü | Konum / gerekçe |
|---|---|---|
| Maternal MH yükü (AD, BDI) → **EMBU-C çocuk algısı** + anne-çocuk discrepancy, AD=strata | **YENİ v0.2** | §130–131. Grep `anne_antidepresan × embu_c` = 0; R/33 discrepancy'yi yordanan tutar. En yüksek değer. |
| BDI≥17 eşiği × AD **birleşik klinik-risk profili** → EMBU-C reddetme/karşılaştırma | **YENİ v0.2** | §130. `beck_clinical≥17` (R/10:186) mevcut ama AD ile birleşik stratum → çocuk düzlemi yok. |
| Informant discrepancy (EMBU-P−EMBU-C) → **SRQ** çatışma/rekabet/sıcaklık | **YENİ v0.2** | §132. R/33 `F_diff ~ predictors` (yordanan); kardeş çıktısına yordayıcı bağ yok. |
| Latent Beck-sınıfı → EMBU-C discrepancy / SRQ / BDI-AD **çaprazlama** | **YENİ v0.2** | §133. R/24 `predclass` standalone; dışsal doğrulama yapılmadı. |
| Materyal yoksunluk → BDI → EMBU-P/C (FSM) | **ZATEN FAZ III** | §102 / §1.6-D (Beck-aracı FSM). Çift-sayım uyarısı orada. |
| PDT büyüklüğü/yönü → SRQ çatışma/rekabet/sıcaklık | **ZATEN FAZ III** | §96–97 (RSA/polinom + aile-clustered yol). |
| SRQ anne-vs-baba kayırma × EMBU-C farkı (MTMM) | **ZATEN FAZ III** | §98 (`pdt_favoritism_map` 14,30,46 / 13,29,45 + MTMM). |
| Eğitim homogamisi → BDI/EMBU/SRQ | **ZATEN FAZ III** | §1.6-B / §101 (eğitim-ekseni DRM). |
| Anne istihdamı × grup → EMBU/BDI | **ZATEN FAZ III** | §102b / §1.6-A. |
| Anne komorbidite var/yok → BDI/EMBU (ikili) | **ZATEN FAZ III** | §104 (ikili komorbidite). Betimsel 14-panel = **Faz IV §123**. |
| Kardeş yaş farkı / same_sex / doğum sırası / çocuk sayısı → SRQ/EMBU-C | **ZATEN FAZ III** | §108–109 + §1.6-E. İşaretli yön = **Faz IV §118**. |
| DM tanı yaşı / süre / **tanı-anında kardeş yaşı** → SRQ/EMBU-C | **FAZ IV v0.1** | §121. `kardes_tani_ani_yas` R/55'te betimsel türetilmiş (§111) → çıkarımsala taşınır. |
| HbA1c × EMBU/BDI/SRQ | **FAZ IV v0.1 (genişletildi)** | §122 — SES-gradyanına **ölçek-skoru korelatları** eklendi. |
| Yönlü/granüler SRQ faset (nurturance/dominance yönü) | **FAZ IV v0.1** | §116–117. |
| Çocuk cinsiyeti odaklı ebeveynlik; anne-yaşı gradyanı | **FAZ IV v0.1** | §119–120. |
| Öz-bildirim ↔ kodlanmış komorbidite uyumu | **FAZ IV v0.1** | §124. |
| Ebeveyn yaş farkı | **FAZ IV v0.1** | §125. |

**"Kaçınılması gerekenler" tam mutabakat:** İkinci-görüşün uyarıları (otoimmün n=1, mental n=2 →
AD×BDI; tek-ebeveyn n≈3 kovaryat değil; HbA1c n≈39 yalnız betimsel; meslek-DRM anne-vs-baba
kurulamaz) bu planın §1.5/§0 fizibilite disipliniyle **birebir örtüşür** — bağımsız doğrulama.

---

## 1.5. FİZİBİLİTE VE VERİ-GERÇEKLİK DENETİMİ *(ÖN-KOŞUL — çalıştırmadan önce)*

> **İlke (Faz III'ten devralınan):** Bir değişkenin kanonik bazda *bulunması* onun
> *modellenebileceğini* garanti etmez. Aşağıdaki denetim **çalıştırma öncesi zorunlu kapıdır**;
> yalnız agregat frekans/güvenilirlik çıkarır (satır-düzeyi PII dökülmez).

### 1.5.1 Faz III'ten bilinen sayımlar (yeniden-kullanılabilir)
`06-sap-faz3-ek-plan.md` §1.5.2'den doğrulı: `anne_hastalik_otoimmun` =1 yalnız **1 aile**;
`anne_hastalik_mental` =1 yalnız **2 aile**; `anne_hastalik_kategori_sayisi` 0:**177**/1:53/2:8
(maks 2, %73 sıfır); `calisma_durumu` çalışıyor **152**/hayır **89**; `es_calisma_durumu`
çalışıyor **227**/emekli **4**; doğum sırası ve `cocuk_sayisi` iyi varyanslı. CSR §12.5.1:
**HbA1c tam-veri n≈39** (yetersiz güç uyarısı) → §122 fiilen **betimsel/düşük-güçlü**.

### 1.5.2 Çalıştırma öncesi çıkarılacak YENİ agregat sorgular (henüz yok)
Aşağıdakiler bu plan onaylanınca kanonik CSV üzerinde **salt-okunur agregat** olarak
çıkarılacak; her biri ilgili KISIM'in fizibilite tavanını sabitler:

1. **SRQ 16 faset (§117 partiality-hariç 14) × iki informant α** (§116–117): her 3-maddelik faset için α;
   **α < .50 fasetler betimsele indirilir** (yön kontrastı yine sunulur, çıkarım yapılmaz).
2. **Çocuk cinsiyeti × grup çapraz-tablosu** (§119): hücre-dengesi + DM'li çocuğun cinsiyet
   dağılımı; herhangi bir grup×cinsiyet hücresi n<20 ise etkileşim betimsele iner.
3. **`tani_yas` dağılımı** (§121): erken (<6) / orta (6–10) / geç (>10) onset bantlarında
   DM-only hücre sayıları; bant n<15 ise 2-bant birleştir.
4. **`es_hastalik_*` 14 kategori frekansı × grup** (§123): anne paralel; tüm kategoriler
   betimsel prevalans olarak sunulur, hiçbiri tek başına çıkarımsal test edilmez.
5. **Öz-bildirim ↔ kodlanmış komorbidite 2×2** (§124): `kronik_hastalik_durumu` (Evet/Hayır)
   × (`anne_hastalik_kategori_sayisi > 0`); κ + gözlenen uyum. Eş için paralel.
6. **Ebeveyn yaş farkı dağılımı** (§125): `anne_yas − es_yas` (es yaşı `es_dogum_tarihi`'nden);
   `es_sag=0` satırlarında NA yönetimi; medyan/IQR + aşırı değer denetimi.
7. **AD × BDI≥17 birleşik risk-stratum hücreleri** (§130, v0.2): 3-düzey stratum × grup
   çapraz-tablosu (`anne_antidepresan` × `beck_clinical`); "AD+ ve BDI≥17" hücresi n<15 ise
   3-düzeyi 2-düzeye (herhangi-risk vs risksiz) birleştir.
8. **LCA sınıf büyüklükleri** (§133, v0.2): R/24 `predclass` × grup dağılımı; min-sınıf-oranı
   %10 altındaysa dışsal-doğrulama betimsele iner (3-step güç yetersiz).

### 1.5.2-SONUÇ FİZİBİLİTE KAPISI KOŞULDU *(2026-07-08, düzeltilmiş kanonik rev 2)*
Yukarıdaki 8 ön-koşul sorgusu düzeltilmiş veri üzerinde koşuldu (`faz4_feasibility.R`; salt-okunur agregat):

| # | Sonuç | Verdikt |
|---|---|---|
| 1 §116-117 SRQ faset α | asimetri çiftleri: nurturance α=.80–.86, dominance α=.58–.69, admiration α=.67–.74; **16 fasetin 14'ü α≥.50** | ✅ **ÇIKARIMSAL** (fasetler beklenenden güvenilir; yalnız 2 faset betimsel) |
| 2 §119 cinsiyet × grup | Kız DM66/Kontrol82, Erkek DM54/Kontrol39 (tüm hücre ≥39); DM'de erkek oranı ↑ (grup×cinsiyet ilişkili) | ✅ (confound-farkında) |
| 3 §121 tanı-yaşı (DM n=120) | <6:**34**, 6-10:**59**, >10:**27**; negatif 0 | ✅ **3-bant** (düzeltme sonrası temiz; birleştirme gerekmez) |
| 4 §123 eş komorbidite | endokrin11/kardiyo13/solunum8/kas8; çoğu tek-haneli; eş kat>0=47 | ⚠ **betimsel** (seyrek) |
| 5 §124 öz-bildirim↔kodlanmış | **κ=1,00** (anne 177/61; eş 191/47) — tam örtüşme | ⚠ **YENİDEN-ÇERÇEVE:** kodlanmış matris öz-bildirimden türetildiği için bağımsız değil → *kodlama-sadakati* teyidi (bağımsız geçerlik değil) |
| 6 §125 ebeveyn yaş farkı | supplement n=**240**, medyan −3,7 (baba ~3,7 yıl büyük), IQR[−6,2;−1,0], aralık[±15,4] | ✅ kovaryat |
| 7 §130 AD×BDI≥17 | AD−/<17=134, **AD−/≥17=59** (tedavisiz distres, güçlü), AD+/<17=39, **AD+/≥17=6 (küçük)** | ✅ küçük hücre birleştir (AD marks tedavi teyidi: tedavili annede BDI≥17 nadir) |
| 8 §133 LCA sınıf | **2 sınıf: 152 (%64, adaptif) / 86 (%36, riskli)**; ikisi de >%10 | ✅ dışsal doğrulama fizibl |

**Sonuç:** Planın çoğu maddesi **çıkarımsal-yeşil**; yalnız §122/§123 betimsel, §124 kodlama-sadakati olarak yeniden çerçevelendi. §116 (bayrak) beklenenden güçlü (α .58–.86). §121 düzeltmeden fayda gördü (n=115→120, 3 temiz bant). §134-135 zaten koşuldu (HbA1c MNAR OR=4,56; yıl×grup p≈1e-12).

### 1.5.3 Beklenen yeniden-sınıflandırmalar (ön-görü)
| § | Ön-görülen Tier | Gerekçe |
|---|---|---|
| §116 yönlü asimetri | **A/B** | fasetler türetilmiş; tek risk 3-madde ω |
| §117 granüler faset profili | **B** | 14 non-partiality faset × çoklu karşılaştırma → FDR zorunlu |
| §119 cinsiyet moderasyonu | **B** | dengeli beklenir; grup×cinsiyet×ölçek hücre denetimi |
| §120 anne-yaşı gradyanı | **B** | sürekli, iyi varyans; non-lineer spline |
| §121 onset penceresi | **C (DM-only)** | bant hücreleri küçük; geniş CI |
| §122 HbA1c gradyanı | **C/D — betimsel** | tam-veri n≈39 → düşük güç, betimsel |
| §123 komorbidite paneli | **D — betimsel** | çoğu kategori seyrek; yalnız prevalans |
| §124 kodlama-sadakati | **veri-audit** | κ=1,00 (kodlanmış öz-bildirimden türetilmiş) → çıkarımsal değil, kodlama-tutarlılık teyidi |
| §125 yaş farkı | **B — kovaryat** | türetilebilir; moderatör zayıf beklenir |
| §130 AD×BDI stratum → EMBU-C | **A/B** | AD n=46 temiz; stratum-hücre denetimi (§1.5.2-7) |
| §131 distres → discrepancy | **B** | R/33 altyapısı hazır; F_diff genişletmesi |
| §132 discrepancy → SRQ | **B** | aile-clustered; baba-ölçülmedi etiketi |
| §133 LCA dışsal doğrulama | **B** | sınıf-oranı denetimi (§1.5.2-8); BCH/3-step |

---

## 2. FAZ IV İÇİNDEKİLER

**KISIM XLII — YÖNLÜ KARDEŞ-İLİŞKİ MİMARİSİ (SRQ birinci-derece faset)**
- 116. Yönlü bakım/güç asimetrisi (`nurturance_by`/`of`, `dominance_by`/`of`, `admiration_by`/`of`)
       × grup — üst-boyutun sildiği yönü geri açma
- 117. 14-faset (non-partiality) granüler profil × grup: DM sinyali hangi fasette yoğunlaşıyor? (FDR-korumalı)
- 118. İşaretli kardeş yaş-yönü × bakım asimetrisi (DM'li çocuk büyük/küçük moderasyonu)

**KISIM XLIII — ÇOCUK-DÜZEYİ MODERATÖRLER**
- 119. Çocuk cinsiyeti odaklı diferansiyel ebeveynlik (cinsiyet × grup × EMBU-P/EMBU-C)
- 120. Anne yaşı substantif gradyanı (yaş → aşırı koruma/sıcaklık, non-lineer)

**KISIM XLIV — KLİNİK ZAMANLAMA VE METABOLİK BAĞLAM (DM-only, kısıtlı)**
- 121. Tanı gelişim-penceresi × ebeveynlik/kardeş (erken/orta/geç onset)
- 122. Metabolik kontrolün sosyodemografik gradyanı (HbA1c ← SES/komorbidite/aile yapısı) — betimsel

**KISIM XLV — AİLE SAĞLIK PROFİLİ VE VERİ-GEÇERLİK**
- 123. 14-kategori komorbidite betimsel prevalans paneli (anne + eş × grup)
- 124. Komorbidite kodlama-sadakati denetimi (öz-bildirim ↔ kodlanmış; κ=1,00 → veri-audit, çıkarımsal değil)

**KISIM XLVI — TÜRETİLEBİLİR YAPISAL DEĞİŞKENLER**
- 125. Ebeveyn yaş farkı (assortatif eşleşme kovaryatı/moderatörü)

**KISIM XLVIII — MATERNAL MENTAL SAĞLIK YÜKÜ → ÇOCUK DÜZLEMİ** *(v0.2 eklentisi — yürütme önceliği #1)*
- 130. AD × BDI≥17 birleşik klinik-risk stratumu → EMBU-C reddetme/karşılaştırma (çocuk algısı)
- 131. Maternal distres stratumu → anne-çocuk EMBU discrepancy (R/33 F_diff genişletmesi)
- 132. Informant discrepancy (EMBU-P−EMBU-C) → SRQ çatışma/rekabet/sıcaklık
- 133. Latent Beck-sınıfı dışsal doğrulaması → EMBU-C discrepancy / SRQ / AD yükü

**KISIM XLIX — SEÇİLİM VE BATCH GEÇERLİK DENETİMLERİ** *(v0.3 eklentisi — CSR-etkili, yürütme önceliği #1)*
- 134. HbA1c erişilebilirlik/eksiklik seçilim denetimi (MNAR; availability ~ AD/Beck/SES)
- 135. Alım-yılı / batch duyarlılığı (yıl×grup kollinearite; 2023-only + yıl-tabakalı)

**KISIM XLVII — DİSİPLİN, R MODÜLLERİ, RAPORLAMA**
- 126. OSF Layer 5 & Tip 3 sapma satırı
- 127. Yeni R modülleri (**R/56+**) + `_targets.R` entegrasyonu + test/audit
- 128. Öncelik kademeleri & fizibilite-güç dürüstlük notu
- 129. Tedbir-ve-hatalar aktif denetim listesi (Faz IV'e özel)
- EK — Evidentia varlık-doğrulı literatür çapaları (**tam-metin doğrulaması bekliyor**)

---

# KISIM XLII — YÖNLÜ KARDEŞ-İLİŞKİ MİMARİSİ

## 116. Yönlü bakım/güç asimetrisi — üst-boyutun sildiği yönü geri açma

**Boşluk:** `status` üst-boyutu (R/10) `nurturance_by + nurturance_of + dominance_by +
dominance_of` toplamıdır → yön simetrikleşir. Kronik-hastalık diadında **kimin kime bakım
verdiği / kimin baskın olduğu** kuramsal olarak asimetriktir (sağlıklı kardeş → DM'li çocuğa
"parentifikasyon"/bakım; DM'li çocuk → hastalık-merkezli statü).

**Yöntem:**
- İki türetilmiş faset ortalamasından **yön skoru**: `nurturance_asym = nurturance_of_sib −
  nurturance_by_sib` (pozitif = raporlayan çocuk kardeşe *veriyor*); `dominance_asym`,
  `admiration_asym` paralel. İndeks (`srq_*`) ve kardeş (`srq_sib_*`) için ayrı.
- **Model:** `nurturance_asym ~ group_f + role_f + (1|aile_no)` (long, aile-clustered).
  İndeks (DM'li) vs kardeş rolü ayrımı kritik: DM ailesinde yön kardeş rolüne göre değişiyor mu?
- **İki-informant çapraz-doğrulama:** indeks çocuğun "veriyorum" algısı ↔ kardeşin "alıyorum"
  algısı uyumu (Olsen-Kenny mantığı, §98 MTMM ile iç-tutarlı).

**Estimand:** rol/grup fonksiyonu olarak bakım/güç *yönü* (simetrik büyüklük değil).
**Etki büyüklüğü:** grup×rol için Cohen's d + %95 GA; SESOI |d|≈0.20.
**Tier (ön-görü):** A/B (ω denetimi sonrası). **Çapa:** Furman-Buhrmester 1985 (SRQ);
kronik-hastalık kardeş bakımı — Vermaes 2012 / Sharpe-Rossiter 2002 (Faz III doğrulı). *(EK: doğrulama bekliyor.)*

## 117. 14-faset (non-partiality) granüler profil × grup — DM sinyali nerede yoğunlaşıyor?

**Boşluk:** CSR 4 üst-boyutta grup farkını raporladı; hangi *alt-fasette* (intimacy, prosocial,
companionship, similarity, affection, quarreling, antagonism, competition…) belirdiği açık değil.

**⚠️ Kapsam (partiality-hariç):** `srq_first_order_map()` (R/10) **16 faset** üretir; test bunu doğrular.
§117 bunların **14 non-partiality fasetini** kapsar — `maternal_partiality` (mad. 14,30,46) ve
`paternal_partiality` (mad. 13,29,45) **Faz III §98 kayırma-kanalıdır** ve burada tekrar edilmez
(çift-analiz önlemi). Fizibilite kapısı §1.5.2-SONUÇ-1: 16 fasetin 14'ü α≥.50.
**Yöntem:** 14 non-partiality faset × grup için standardize ortalama fark forest'ı (long, aile-clustered);
**Benjamini-Hochberg FDR** (14 test); yalnız FDR-hayatta-kalan fasetler yorumlanır. α<.50
fasetler grafikte "düşük-güvenilir" işaretiyle betimsel kalır.
**Estimand:** faset-düzeyi grup farkı deseni (hipotez-üretici topografi).
**Tier:** B. **Çapa:** Brody 1998 (kardeş ilişki kalitesi çok-boyutluluğu). *(EK: doğrulama bekliyor.)*

## 118. İşaretli kardeş yaş-yönü × bakım asimetrisi

**Boşluk:** `age_gap` mutlak kullanılıyor; **DM'li çocuğun kardeşten büyük/küçük** olması
(işaretli) bakım yönünü moderatör olarak koşullamıyor.
**Yöntem:** `dm_older` (DM'li indeks > kardeş yaşı) ikili moderatör × `nurturance_asym` (§116).
`age_gap` işaretli + kuadratik. **Yalnız DM ailelerinde** anlamlı; Kontrol karşılaştırma tabanı.
**Tier:** B/C (hücre denetimi). **Çapa:** East-Rook / Brody yaş-hiyerarşisi. *(EK: doğrulama bekliyor.)*

---

# KISIM XLIII — ÇOCUK-DÜZEYİ MODERATÖRLER

## 119. Çocuk cinsiyeti odaklı diferansiyel ebeveynlik

**Boşluk:** `katilimci_cocuk_cinsiyet` H1/bazı modüllerde kovaryat; sistematik **cinsiyet × grup ×
ebeveynlik** odak analizi yok.
**Yöntem:** `EMBU_C_alt ~ cinsiyet_f * group_f + cocuk_yas_z + (1|aile_no)` (long) + EMBU-P
(anne raporu, family). Odak: cinsiyet×grup etkileşimi (DM'li kız vs erkek çocukta ebeveynlik
farklılaşıyor mu?). §1.5.2-2 hücre denetimi ön-koşul.
**Estimand:** çocuk cinsiyetinin ebeveynlik/algı üzerindeki koşullu (grup-içi) etkisi.
**Tier:** B. **Çapa:** Lytton-Romney 1991 (ebeveyn cinsiyet-sosyalizasyonu meta); Endendijk 2016. *(EK: doğrulama bekliyor.)*

## 120. Anne yaşı substantif gradyanı

**Boşluk:** `anne_yas` 27 modülde yalnız `_z` kovaryat; yaş→ebeveynlik *odak* gradyanı yok.
**Yöntem:** `EMBU_P_asiri_koruma ~ ns(anne_yas, 3) + ses_latent_z + group_f` (non-lineer spline);
sıcaklık/reddetme paralel. Simpson denetimi (grup×yaş-bandı).
**Estimand:** anne yaşının ebeveynlik boyutlarıyla (non-lineer) ilişkisi.
**Tier:** B. **Çapa:** Camberis 2016 / Barnes maternal-yaş & duyarlılık. *(EK: doğrulama bekliyor.)*

---

# KISIM XLIV — KLİNİK ZAMANLAMA VE METABOLİK BAĞLAM (DM-only)

## 121. Tanı gelişim-penceresi × ebeveynlik/kardeş

**Boşluk:** §111 yalnız "tasarım-sinyali eskizi"; `tani_yas` DM alt-analizde var ama onset-penceresi
ebeveynlik/kardeş moderatörü olarak çalıştırılmadı.
**Yöntem:** `onset_band` (erken<6 / orta6–10 / geç>10; fizibilite kapısı §1.5.2-SONUÇ-3: **düzeltilmiş
n=120'de bantlar 34/59/27 → 3-bant birleştirmesiz**) × EMBU-C aşırı koruma + SRQ bakım asimetrisi
(§116). **DM-only n=120**, geniş CI, betimsel-öncelikli.
**⚠️ "Tanıdan sonra doğan kardeş" duyarlılığı:** Düzeltilmiş kanonik'te indeks tarafında mantık
ihlali yoktur (dm_yili>cocuk_yas=0, negatif tanı-yaşı=0); ancak `kardes_tani_ani_yas < 0` **1 kayıt**
kalır. Bu bir **hata değil**, özel bir maruziyet durumudur: kardeş, indeks çocuğun tanısından *sonra*
doğmuştur (aileye hastalık zaten yerleşmişken). Ayrı etiketli kategori olarak **betimsel/duyarlılık
maskesiyle** tutulur (çıkarımsal banda sokulmaz); kardeş-maruziyeti yorumunda bu 1 aile ayrı raporlanır.
**Estimand:** tanı yaşının aile adaptasyonuyla ilişkisinin desen kestirimi.
**Tier:** C. **Çapa:** Northam onset-yaşı; Jaser/Whittemore psikososyal derleme. *(EK: doğrulama bekliyor.)*

## 122. Metabolik kontrolün sosyodemografik gradyanı — betimsel

**Boşluk:** HbA1c modellerde SES *kovaryatı*; "kimde kontrol daha kötü" (SES/komorbidite/aile
yapısı → HbA1c) *odak* estimand olarak sunulmadı.
**Yöntem:** İki yön birlikte: (i) **sosyodemografik korelatlar** `hba1c ~ ses_latent_z +
anne_hastalik_kategori_sayisi_ikili + tek_ebeveyn`; (ii) **ölçek-skoru korelatları** (ikinci-görüş
eklentisi) `hba1c` ↔ EMBU-C aşırı koruma / EMBU-P / BDI / SRQ çatışma betimsel korelasyon matrisi
(metabolik kontrol ile aile psikososyal ölçümlerini bağlar). DM-only.
⚠️ **CSR §12.5.1: tam-veri n≈39** → düşük güç; **betimsel korelasyon + geniş CI**, çıkarımsal
iddia yok, imputasyon yok; eksik-veri (structural + item) açıkça raporlanır.
**Estimand:** glisemik kontrolün sosyodemografik **ve psikososyal-ölçek** korelatlarının betimsel haritası.
**Tier:** C/D — betimsel. **Çapa:** Gallegos-Macias 2003 / Hilliard SES-glisemik gradyan. *(EK: doğrulama bekliyor.)*

---

# KISIM XLV — AİLE SAĞLIK PROFİLİ VE VERİ-GEÇERLİK

## 123. 14-kategori komorbidite betimsel prevalans paneli

**Boşluk:** R/53 yalnız `otoimmun`+`endokrin`+`kategori_sayisi` kullandı; 12 anne + 14 eş
sistem-özgü kategori (`kardiyovaskuler, solunum, gastrointestinal, renal, kas_iskelet, mental,
sinir, duyu, hematolojik, dermatolojik, neoplazm, diger`) hiç sunulmadı.
**Yöntem:** **Yalnız betimsel prevalans tablosu/ısı-haritası** (anne + eş × grup); çoğu kategori
seyrek (§1.5.1) → hiçbiri tek başına çıkarımsal test edilmez. Grup farkı yalnız `kategori_sayisi`
ikili düzeyinde (Faz III §104 ile iç-tutarlı) not edilir.
**Estimand:** aile sağlık yükünün betimsel profili (bağlamsal şeffaflık).
**Tier:** D — betimsel. **Çapa:** — (betimsel; literatür çapası gerekmez).

## 124. Komorbidite kodlama-sadakati denetimi *(analiz değil, veri-audit)*

**⚠️ Statü (fizibilite kapısı §1.5.2-SONUÇ-5):** Bu **bağımsız geçerlik çalışması DEĞİLDİR.**
Fizibilite kapısı `kronik_hastalik_durumu` (öz-bildirim ikili) ile `kategori_sayisi>0` (kodlanmış)
arasında **κ=1,00** (anne 177/61; eş 191/47) buldu — çünkü **kodlanmış 14-kategori matris zaten
öz-bildirim metninden türetilmiştir**; ikisi bağımsız ölçüm değildir. Dolayısıyla Kriegsman-tipi
"öz-bildirim ↔ tıbbi kayıt geçerliği" çapası **uygulanamaz** (bağımsız kayıt yok).
**Ne yapar:** İki türetim katmanının **kodlama-sadakatini** teyit eder — ikili bayrak ile kategori-
matrisi tutarlı mı (κ=1,00 → evet, kodlama hatasız). Herhangi bir uyuşmazlık (κ<1) veri-işleme
hatasına işaret ederdi.
**Estimand:** yoktur (çıkarımsal değil); veri-kalite/kodlama-tutarlılık teyidi.
**Tier:** — (veri-audit; Faz IV çıkarımsal setine sayılmaz). **Çapa:** — (bağımsız kayıt olmadığından
literatür çapası gerekmez; Kriegsman kaldırıldı).

---

# KISIM XLVI — TÜRETİLEBİLİR YAPISAL DEĞİŞKENLER

## 125. Ebeveyn yaş farkı (assortatif eşleşme) — ✅ FİZİBL (v0.4 kurtarma)

**Durum güncellemesi (v0.3 İNFİZİBL → v0.4 FİZİBL):** `es_dogum_tarihi` kanonik final CSV'de
%100 boştu; ancak **ham kaynakta (`Birleşik Veri...NİHAİ.csv`) 480/482 doludur** ve türetme
kaybıydı (B5, `08-veri-butunluk-denetimi.md` §7). Kurtarıldı →
`data/processed/SUPPLEMENT__es_yas_recovered.csv` (`aile_no, es_yas, ebeveyn_yas_farki`;
es_yas 240/241; aritmetik `anne_yas` ile 222/241 birebir doğrulı).
**Yöntem:** `ebeveyn_yas_farki` (= `anne_yas − es_yas`, supplement'ten) kovaryat/moderatör → EMBU-P +
Beck. ⚠️ **Plausibilite-maskesi zorunlu (B7):** es_yas 13–56,5 aralığında **13 = imkansız baba
yaşı** → `es_yas < 16 | > 70` dışla; 19 ham↔final tarih-sapması olan aile duyarlılıkta işaretlenir.
Aşırı değer 3-adım protokolü.
**Estimand:** ebeveyn yaş asimetrisinin ebeveynlik/distres ile (zayıf beklenen) ilişkisi.
**Tier:** B — kovaryat (moderatör zayıf; supplement + B7 maskesi ön-koşul). **Çapa:** — (yapısal).

---

# KISIM XLVII — DİSİPLİN, R MODÜLLERİ, RAPORLAMA

## 126. OSF Layer 5 & Tip 3 sapma satırı
Çalıştırma **onaylanırsa**: `02-sapma-tablosu.md`'ye #3 satırı (Tip 3, post-hoc keşifsel
genişletme, KISIM XLII–XLVI), OSF **Layer 5** "Open-Ended Registration" amendment. **Plan
aşamasında sapma satırı EKLENMEZ** (sapma = uygulanan değişiklik; henüz uygulanmadı).

## 127. Yeni R modülleri (R/56+) + `_targets.R`
Mevcut ağaç `R/00`–`R/55` dolu → Faz IV modülleri **`R/56`+**:
- `R/56_directional_sibship.R` (§116–118): saf fonksiyon; runner `scripts/R/56_phase4_*_audit.R`.
- `R/57_child_level_moderators.R` (§119–120).
- `R/58_onset_metabolic_context.R` (§121–122, DM-only).
- `R/59_family_health_validity.R` (§123–124).
- `R/60_derived_structural.R` (§125).
- `R/61_maternal_mh_child_plane.R` (§130–133, **v0.2**): AD×BDI stratum → EMBU-C; discrepancy →
  SRQ; LCA `predclass` dışsal doğrulama. R/24 (`run_lca`) ve R/33 (`F_diff`) çıktılarını girdi alır.
Her modül: `stopifnot()` testi (`tests/`), seed=20260708, `outputs/tables/phase4_*.csv`,
`_targets.R`'de `phase4_*_results` hedefi (`format="file"` kanonik CSV dokunulmaz).

## 128. Öncelik kademeleri & fizibilite-güç dürüstlük
Yürütme sırası (değer×fizibilite, v0.3): **§134 → §135 → §130 → §131 → §132 → §116 → §119 →
§133 → §124 → §117 → §120 → §125 → §118 → §121 → §122 → §123**. **Geçerlik-denetimleri
(§134–135) HER ŞEYDEN ÖNCE** — çünkü HbA1c-seçilim ve yıl-confound, bağımlı analizlerin (§122,
CSR §12.5) yorumunu koşullar. Maternal-MH → çocuk düzlemi (§130–132) en yüksek klinik değer;
§122/§123 betimsel; §121 DM-only düşük güç — hepsi açık güç-uyarısıyla.

## 129. Tedbir-ve-hatalar aktif denetim (Faz IV'e özel)
- [ ] Ortalama **ve** medyan (sürekli: yaş farkı, onset, HbA1c).
- [ ] Yön skorları (§116) işaret konvansiyonu açık yazıldı mı (of − by)?
- [ ] Çoklu karşılaştırma: §117 (14 non-partiality faset) FDR; §119 etkileşim ön-belirtilmiş.
- [ ] Simpson: §120 grup×yaş-bandı; §119 grup×cinsiyet.
- [ ] Korelasyon dili — nedensel dile kaymadı (§122 "gradyan/ilişkili", "neden" değil).
- [ ] Faset güvenilirliği: ω<.50 → betimsel indirim (§116–117).
- [ ] Structural missing (§122 HbA1c, §125 es_sag=0) açık NA, listwise değil.
- [ ] HARKing: hiçbir bulgu H1–H4 prior'ını güçlendirmiyor; tümü `[KEŞİFSEL·POST-HOC]`.
- [ ] AD strata dili: `anne_antidepresan` **kovaryat değil, stratum/moderatör** olarak yorumlanır (§130).
- [ ] BDI eşiği: `beck_clinical≥17` dikotomizasyonu bilgi kaybı → sürekli `beck_total` duyarlılığı da raporlanır (§130).
- [ ] Baba davranışı doğrudan ölçülmüyor: kayırma/discrepancy "çocuk algısı" olarak etiketlenir (§132).

---

# KISIM XLVIII — MATERNAL MENTAL SAĞLIK YÜKÜ → ÇOCUK DÜZLEMİ *(v0.2 eklentisi)*

> **Mantık:** CSR'da H3 (anne öz-bildirimi) üç-katmanlı **negatif**ken, çocuk algısı (H1) DM
> lehine reddetme sinyali verir — asimetri CSR §17.4/§17.7'de tartışıldı. İkincil görüşün
> isabetli tespiti: **anne mental-sağlık yükü** (antidepresan + BDI) CSR'da yalnız *anne
> düzlemine* (EMBU-P, caregiver burden — Faz III §104–105) bağlandı; **çocuk algı düzlemine**
> (EMBU-C reddetme/karşılaştırma + anne-çocuk discrepancy) ve **kardeş düzlemine** (SRQ) hiç
> taşınmadı. Bu KISIM o köprüyü kurar. Kod-doğrulaması: `anne_antidepresan × embu_c` = **0 dosya**;
> R/33 discrepancy'yi yalnız yordanan tutar; R/24 LCA sınıfı dışsal çıktıya çaprazlanmaz.

## 130. AD (tedavi/temas) × BDI (güncel şiddet) 2×2 → EMBU-C çocuk algısı *(v0.3 düzeltildi)*

**⚠️ v0.2 → v0.3 kritik düzeltme (ampirik doğrulı):** v0.2'de önerilen **monotonik 3-düzey
"risk gradyanı" YANLIŞTIR.** Kanonik CSV üzerinde bağımsız doğrulama (2026-07-08): DM'de AD
kullanan annelerde güncel Beck **daha düşük** (9,56 vs 14,71; Welch p=0,000128 — kaynak: grep
`FINAL_REFERENCE__analysis_base_family.csv` bağımsız hesap). Yani `anne_antidepresan=1`
**güncel yüksek depresyon DEĞİL, tedavi/klinik-temas/tarihsel-distres göstergesidir** (muhtemelen
tedaviyle kontrol altına alınmış). Dolayısıyla AD ve BDI **aynı yönde toplanamaz**.

**Boşluk:** `anne_antidepresan` (temiz sinyal: DM 35 / Kontrol 11, §1.5.1) ve `beck_clinical≥17`
(R/10:186) mevcut; ama çocuk algı düzlemine bağlanmadı.
**Yöntem (düzeltilmiş):** İki ekseni **ayrı** tut — `ad_f` (tedavi/temas: Evet/Hayır) ×
`beck_clinical` (güncel şiddet: ≥17/<17) = **2×2 tedavi-durumu × güncel-şiddet**:
- AD−/BDI<17 = distres yok, tedavi yok (referans)
- AD−/BDI≥17 = **tedavisiz güncel distres** (a priori en yüksek çocuk-risk hücresi)
- AD+/BDI<17 = tedavili/kontrollü (tarihsel distres)
- AD+/BDI≥17 = tedavili ama sürüyor
`embu_c_reddetme_mean ~ ad_f * beck_clinical + group_f + cocuk_yas_z + (1|aile_no)` (long);
karşılaştırma alt-ölçeği paralel. **AD kovaryat DEĞİL, tedavi-ekseni** olarak yorumlanır; sürekli
`beck_total` duyarlılığı da raporlanır. §1.5.2-7 hücre denetimi ön-koşul (hücreler dengesiz
beklenir — AD+/BDI≥17 seyrek).
**Estimand:** tedavi-durumu ve güncel-şiddetin *çocuğun* algıladığı reddetme/karşılaştırma ile
(etkileşimli) ilişkisi — özellikle "tedavisiz güncel distres" hücresi.
**Tier:** B (AD n=46 temiz ama 2×2 hücre dengesizliği güç düşürür). **Çapa:** Goodman-Gotlib
1999 (maternal depresyon → çocuk); Van Gampelaere 2020 (Faz III doğrulı). *(EK.)*

## 131. Maternal distres stratumu → anne-çocuk EMBU discrepancy

**Boşluk:** R/33 `F_diff` (anne-çocuk latent fark) yordanıyor ama **maternal-distres stratumu**
(§130) yordayıcı olarak girmedi.
**Yöntem:** R/33 `F_diff_reddetme ~ risk_stratum + group_f` genişletmesi — anne depresyon yükü
arttıkça anne-çocuk algı *uyumsuzluğu* (kim daha çok reddetme bildiriyor?) değişiyor mu?
İşaret yönü açık raporlanır (anne-fazla vs çocuk-fazla discrepancy).
**Estimand:** maternal distresin informant-uyumsuzluğu büyüklüğü/yönü ile ilişkisi.
**Tier:** B. **Çapa:** De Los Reyes 2015 (Operations Triad; distres → informant discrepancy). *(EK.)*

## 132. Informant discrepancy (EMBU-P − EMBU-C) → SRQ kardeş ilişkisi

**Boşluk:** R/33 discrepancy'yi *yordanan* tutar; **kardeş çıktısına (SRQ) yordayıcı** olarak
hiç bağlanmadı — H5 concordance'ın ötesinde ayrı estimand.
**Yöntem:** aile-düzeyi discrepancy skoru (|EMBU-P − EMBU-C indeks|, alt-ölçek başına) →
`srq_ho_conflict_mean` / `srq_ho_rivalry_mean` / `srq_ho_warmth_mean` (aile-clustered).
⚠️ Baba davranışı doğrudan ölçülmüyor → "çocuğun algı-uyumsuzluğu" etiketi; nedensel dil yok.
**Estimand:** anne-çocuk ebeveynlik-algı uyumsuzluğunun kardeş ilişki kalitesiyle ilişkisi.
**Tier:** B. **Çapa:** Coldwell-Pike-Dunn 2008 (Faz III doğrulı; fark skorları yordayıcı gücü). *(EK.)*

## 133. Latent Beck-sınıfı dışsal doğrulaması

**Boşluk:** R/24 (`run_lca`) anne Beck-semptom sınıflarını (`predclass`, §12.2) üretir ama
**standalone** bırakır; EMBU-C discrepancy / SRQ / AD yükü ile çaprazlanmaz → sınıfların
*dışsal geçerliği* test edilmedi.
**Sınıf yapısı (fizibilite kapısı §1.5.2-SONUÇ-8):** En iyi LCA modeli **2 sınıf** (3 değil): sınıf 1
n=**152** (%64; düşük Beck, yüksek sıcaklık, düşük negatif-ebeveynlik → *adaptif*), sınıf 2 n=**86**
(%36; yüksek Beck, düşük sıcaklık → *riskli*). İkisi de >%10 → dışsal doğrulama fizibl.

**⚠️ LCA girdi-sözleşmesi (pipeline kırılganlığı önlemi):** `predclass` final family CSV'de **yoktur**;
R/24 `run_lca` çıktısından gelir. §133 koşmadan önce bir **ara-tablo sözleşmesi** tanımlanır:
`aile_no, predclass, posterior_prob_c1..c2, entropy, max_posterior (atama-belirsizliği)`. Bu tablo
R/24 hedefinden türetilir ve `_targets.R`'de §133'ün **açık bağımlılığı** olarak bağlanır (yoksa
BCH/3-step hedefi raporda durur ama pipeline'da kırılır).
**Yöntem:** yukarıdaki ara-tablo → (i) EMBU-C reddetme discrepancy; (ii) SRQ çatışma; (iii) AD-kullanım
oranı. Sınıf ana etkisi + `group_f` çaprazı. **BCH/3-step** (sınıflandırma-hatası düzeltmeli) tercih;
düşük entropy'de basit modal atama duyarlılıkla.
**Estimand:** anne semptom-tipolojisinin çocuk/kardeş düzlemi çıktılarıyla dışsal geçerliği.
**Tier:** B. **Çapa:** Lanza-Cooper (LCA dışsal doğrulama, BCH/3-step). *(EK.)*

---

# KISIM XLIX — SEÇİLİM VE BATCH GEÇERLİK DENETİMLERİ *(v0.3 eklentisi — CSR-etkili)*

> **Statü ayrımı:** §134–135 diğer Faz IV maddelerinden farklıdır — bunlar **yeni bir ilişki
> keşfetmez, mevcut/planlı analizlerin geçerliğini denetler.** İkisi de kanonik CSV'de birebir
> doğrulanmış (v0.3 başlık) somut tehditlere yanıttır ve **CSR-düzeyinde de sonuç doğurur**
> (§1.8). Bu nedenle yürütme önceliği #1.

## 134. HbA1c erişilebilirlik/eksiklik seçilim denetimi (MNAR)

**Tehdit (doğrulı):** DM'de HbA1c yalnız **39/120 (%32,5)** ailede var ve varlığı `anne_antidepresan`
ile güçlü ilişkili: **Fisher OR=4,56 [1,84–11,70], p=0,000466** (AD var %57,1 vs AD yok %22,4
tamamlanma). HbA1c ham dosyada yok — sonradan klinik-kayıt entegrasyonuyla eklendi → varlık
klinik-izlem/temas göstergesi. Bu, HbA1c'nin "düşük n" değil **seçilmiş (MNAR) alt-örneklem**
olduğunu gösterir.
**Yöntem:** `hba1c_available ~ anne_antidepresan + beck_total + ses_latent_z + dm_yili_z +
cocuk_yas_z` (DM-only lojistik) — hangi değişkenler *ölçülme olasılığını* öngörüyor?
Seçilim yüzeyi tablolanır; HbA1c'li vs HbA1c'siz DM alt-örneklemleri Tablo-1 tarzı karşılaştırılır.
**Sonuç kuralı:** **Hiçbir HbA1c × ebeveynlik bulgusu (§122, CSR §12.5) bu seçilim yüzeyi
raporlanmadan yorumlanamaz.** Ağır seçilim → HbA1c analizleri betimsel/uyarılı kalır.
**⚠️ IPW/Heckman yalnız fizibilite-duyarlılığı (düzeltme DEĞİL):** Amaç seçilimi *göstermektir*,
telafi etmek değil. n=39 nedeniyle IPW **çalıştırılırsa** rapor zorunlu olarak şunları içerir:
**etkin örneklem boyutu (ESS)**, **maksimum ağırlık**, **ağırlık-budama (truncation) eşiği ve
budanan gözlem sayısı**. Bunlar olmadan IPW "düzeltme yapıldı" izlenimi verir; bu yanıltıcıdır —
n=39'da IPW gürültüyü büyütür. Heckman selection-model yalnız dağılımsal-varsayım duyarlılığı olarak,
exclusion-restriction açıkça tartışılarak sunulur.
**Estimand:** HbA1c ölçüm-varlığının seçilim mekanizması (MNAR karakterizasyonu) — *tanımlayıcı*.
**Tier:** A — geçerlik/seçilim denetimi. **Çapa:** Little-Rubin (MNAR); Heckman seçilim. *(EK.)*

## 135. Alım-yılı / batch duyarlılığı

**Tehdit (doğrulı):** anket yılı grupla **neredeyse kollinear**: 2023 DM108/K40, 2024 DM6/K36,
2025 DM6/K45; `group ~ yıl` logistic **p≈1,3e-12**. DM ağırlıkla 2023'te, Kontrol ağırlıkla
2024–25'te alınmış → **recruitment/batch temporal confound**. Ham-final tarih farkı 19 ailede.
**Yöntem:** Yıl **kör kovaryat OLARAK EKLENMEZ** (grupla kollinear → grup etkisini emer). Bunun
yerine üç katman: (i) **2023-only alt-örneklem** (her iki grup mevcut: DM108/K40) — H1–H3/H5 ana
etkilerinin replikasyonu; (ii) **yıl-tabakalı betimsel** (özellikle çocuk algısı/Beck); (iii)
duyarlılık: yıl-ayarlı model *yalnız* kollinearite tanısı (VIF/koşul-sayısı) ile birlikte, ihtiyatlı.
**Sonuç kuralı:** 2023-only'de ana etkiler yönce korunuyorsa güçlenir; kayboluyorsa "grup farkı
kısmen batch/dönem etkisiyle karışık" açıkça yazılır.
**Estimand:** grup etkilerinin alım-dönemi confound'una dayanıklılığı.
**Tier:** A — confound/batch denetimi (H1–H5'i *yorumlar*, değiştirmez). **Çapa:** — (tasarım/batch;
literatür çapası gerekmez).

---

## 1.8. CSR-DÜZEYİ ETKİLER *(v0.3 — plan dışı, karar bekliyor)*

§134–135 ve §130-düzeltmesi yalnız Faz IV keşfini değil, **mevcut CSR metnini** de etkiler.
Aşağıdakiler **öneri**dir; kanonik CSR'a dokunmadan önce onay bekler:

| Bulgu | CSR etkisi (önerilen) | Konum |
|---|---|---|
| HbA1c MNAR seçilim (OR 4,56) | §12.5.1'e seçilim-uyarısı; §18.4 eksik-veri sınırlılığına MNAR notu | CSR §12.5, §18.4 |
| Yıl × grup kollinearite (p≈1e-12) | §18.1 tasarım sınırlılığına **alım-dönemi confound** maddesi; 2023-only duyarlılık | CSR §18.1 |
| AD = tedavi/temas (şiddet değil) | §15.5 antidepresan yorumunun "güncel şiddet" değil "tedavi/temas" olarak rafine edilmesi | CSR §15.5 |
| 5+1 dm_yili mantık ihlali | §110/§12.5 dışlama notunun teyidi (zaten n=115); veri-entegrasyon audit satırı | CSR §12.5, audit trail |

**Not — eğitim ekseni rafinasyonu (§3 bulgu):** Eğitim→EMBU-P aşırı koruma sinyali sağlam
(p=2,52e-07, tam-kovaryatlı korunur); **eğitim farkı/homogami ana sinyal değil** (fark p≈0,10).
→ Faz III §101 eğitim-DRM ve §1.6-B homogami yerine **daha sade savunulabilir post-hoc**: ortalama/
anne eğitimi → EMBU-P aşırı koruma (grup + yıl + anne yaşı + materyal kontrollü). §101 buna göre
daraltılır (DRM keşifsel-ikincil kalır).

---

## EK — Evidentia ile Varlık-Doğrulı Literatür Çapaları *(tam-metin doğrulaması BEKLİYOR)*

> ⚠️ **Aşağıdaki künyeler ADAY çapadır** — Faz III §1.5.5 deseniyle, yürütme öncesi
> `referans-kapısı` (Evidentia native-first: PubMed/EPMC + OpenAlex + Anna's Reader) ile
> DOI/PMID doğrulaması + tam-metin quote↔iddia denetiminden geçirilecek. **Hiçbir sayısal
> büyüklük bu planda iddia edilmez**; yön/tema düzeyinde çapadır. Doğrulanamayan künye
> "VERİ BULUNAMADI" olarak işaretlenip düşürülür.

| § | Aday çapa (doğrulama bekliyor) | Rol |
|---|---|---|
| §116, §117, §118 | Furman & Buhrmester 1985 (SRQ kaynağı); Brody 1998 (kardeş ilişki kalitesi) | ölçek + boyutsallık |
| §116, §121 | Vermaes 2012 (kronik-hastalık kardeş uyumu meta); Sharpe & Rossiter 2002 (Faz III doğrulı) | kronik-hastalık kardeş bağlamı |
| §119 | Lytton & Romney 1991 (ebeveyn cinsiyet-sosyalizasyonu meta); Endendijk 2016 | cinsiyet-diferansiyel ebeveynlik |
| §120 | Camberis 2016; Barnes (maternal yaş × duyarlılık) | anne-yaşı gradyanı |
| §121 | Northam (onset-yaşı); Jaser / Whittemore 2012 (T1DM psikososyal derleme) | tanı-penceresi |
| §122 | Gallegos-Macias 2003; Hilliard (SES-glisemik gradyan) | metabolik-SES |
| §124 | — (κ=1,00: kodlanmış matris öz-bildirimden türetilmiş → bağımsız kayıt yok; Kriegsman KALDIRILDI) | kodlama-sadakati (çapa gerekmez) |
| §130, §131 | Goodman & Gotlib 1999 (maternal depresyon → çocuk); Van Gampelaere 2020 (Faz III doğrulı) | maternal-MH → çocuk |
| §131 | De Los Reyes 2015 (Operations Triad; distres → informant discrepancy) | discrepancy mekanizması |
| §132 | Coldwell, Pike & Dunn 2008 (Faz III doğrulı; fark skorları yordayıcı) | discrepancy → kardeş |
| §133 | Lanza & Cooper (LCA dışsal doğrulama, BCH/3-step) | latent sınıf geçerliği |

---

**Özet:** Faz IV, kanonik bazın **son artık yüzeyini** disiplinli keşfe açar: (v0.2 önceliği)
**maternal mental-sağlık yükünün çocuk/kardeş düzlemine köprülenmesi** (§130–133 — AD×BDI
stratumu → EMBU-C algısı, discrepancy → SRQ, LCA dışsal doğrulaması); ardından türetilmiş ama
modellenmemiş SRQ yön-asimetrisi (§116–118), çocuk-düzeyi odak moderatörler (§119–120), klinik
zamanlama/metabolik bağlam (§121–122), aile sağlık profili betimlemesi (§123) ve veri-geçerlik
kapısı (§124–125). İkinci-görüş listesinin diğer maddeleri **Faz III'te zaten kapsanmıştır**
(§1.7 mutabakat). Tümü **[KEŞİFSEL·POST-HOC]**, korelasyonel, OSF Layer 5; fizibilite denetimi
(§1.5) ve Evidentia doğrulaması (EK) ön-koşuldur. **Yürütme kararı beklemede.**
