# Tasarım — `chapters/04_bulgular.qmd` Eksiksizlik + Marmara Mimarisi

**Tarih:** 2026-07-13 · **Bölüm:** BULGULAR (ana bölüm 4) · **Dal:** feat/nitel-kanonik-lit-derinlestirme
**Yaklaşım:** A — Yerinde cerrahi zenginleştirme (mevcut yorumsuz/doğru omurga korunur; boşluklar eklenir, mimari Marmara'ya cilalanır).

## 1. Amaç ve kilitli kararlar

Hedef: Bulgular bölümü, **nicel ve nitel kanonik sonuç dosyalarında raporlanmış TÜM bulguları eksiksiz** taşımalı ve **Marmara tez kılavuzu** mimarisine uymalı. Bulgu düzeyi **yorumsuz**; yorum/literatür/karma meta-çıkarım *Tartışma ve Sonuç*'ta kalır (marmara §3.6, §3.7).

Kullanıcı onaylı kararlar:
- **K1 — Kanonik kaynak:** en yeni `.qmd` çifti birincil; `.md` yalnız çapraz-doğrulama.
  - Nicel: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (§9–§16).
  - Nitel: `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` (MD kopya mekanik render, otorite değil).
- **K2 — Kapsam:** maksimal — tüm katmanlar (tanımlayıcı → psikometri → H1–H5 → [KEŞİFSEL] §12 → **[KEŞİFSEL·İKİNCİL] §15+§16 tam** → robustluk/Bayesçi → nitel → joint display → sentez).
- **K3 — Tablo/şekil yerleşimi:** her tablo/şekil **konu edildiği alt bölümde** (marmara §3.6/§1.6/§1.7); sondaki toplu "APA Tablo Seti" bloğu **kaldırılır**.
- **K4 — §15/§16:** 18 ikincil/bağlamsal bulgunun tamamı [KEŞİFSEL·İKİNCİL] alt bölümü olarak; phase2/exploratory şekilleriyle.
- **K5 — Başlık numaralandırma:** Marmara numaralı (`4.`, `4.1.`, `4.1.1.`; en çok dört düzey). Bu bölüme uygulanır; 01–03 bölümleriyle geçici tutarsızlık kabul (tez-geneli numaralandırma ayrı iştir → Bölüm 8).
- **K6 — Joint display:** iki tablo tek kanonik tabloya birleştirilir; "Provisional/TASLAK" etiketi kaldırılır (nihai-belge tonu).

## 2. Marmara mimari kuralları (uygulanacak)

- Sıra amaç/hipotezle uyumlu; tanımlayıcı → ölçüm/değerlendirme → karşılaştırma (marmara §3.6).
- **Aynı bulgu hem tablo hem şekil olarak sunulmaz.** Mevcut ilkeli kural korunur: katsayı-forest/yol şekilleri (fig-07/08/09/10/11/14/24/25) tabloya devredilmiştir; yalnız **görsel-özgü** şekiller (dağılım, yüzey, eğri, ağ, denge, taban, kalibrasyon) taşınır.
- Tablo başlığı **üstte**, şekil başlığı **altta**; kısaltma/simge/test/p **dipnotta** (§1.7/§1.6). Quarto'da `tbl-cap` (üst) ve şekil `![...]` (alt) bunu sağlar.
- Sayısal yazım (§1.4/§12): ondalık **virgül**, virgülden önce daima `0`; ortalama/yüzde **1 basamak**, test/oran **2 basamak**, `p` **3 basamak** (`p=0,038` / `p<0,001`). Tablo render'ında `apa_tr_decimal()` yardımcısı zaten çevirir; anlatı elde denetlenir.
- Program çıktılarının tamamı eklenmez; metinde özet, ayrıntı tablo/şekille.
- Başlık: ana 14 punto kalın büyük harf; alt başlık birinci düzey her sözcük ilk harfi büyük; ikinci+ düzey yalnız ilk sözcük; bağlaç (ve/ile) küçük; başlık sonu noktalama yok.

## 3. Hedef bölüm ağacı (numaralı, tablo/şekil yerleşimli)

> Not: `# 4. BULGULAR` ana başlık; alt başlıklar aşağıdaki numaralarla. `[KEŞİFSEL]`/`[KEŞİFSEL·İKİNCİL]` etiketleri başlık metninde korunur.

```
# 4. BULGULAR                                  (giriş paragrafı: ondalık, FDR, izlenebilirlik, KVKK)

## 4.1. Örneklem ve Tanımlayıcı Bulgular
   Tablolar: t01 (örneklem), t02 (kovaryat denge), t03 (eksik veri), t04 (eğilim skoru), t05 (SES)
   Şekiller: fig-01 STROBE, fig-02 DAG, fig-04 propensity-overlap, fig-05 ses-heatmap
            (+ fig-03 SMD-love [denge görseli], + fig-06 missing-pattern [eksik-örüntü görseli])
   GAP: tam eksik-veri profili (material %0,4; Beck total %1,2; DM yılı %50,2 yapısal; HbA1c %83,8 yapısal)

## 4.2. Ölçek ve Veri Kalitesi (Psikometrik Bulgular)
   Şekiller: psychval-01-reliability, psychval-02-floor (+ opsiyon psychval-03-cfa / -06-validity)
   FIX: "Tablo 5 (apa_t05)" yanlış-atıfı KALDIR (apa_t05 = SES). Güvenirliğin apa-tablosu YOK.
   GAP: 8 alt-ölçek α/ω anlatıya (EMBU-P sıcaklık 0,678/0,687; aşırı koruma 0,746/0,751; karşılaştırma
        0,703/0,724; EMBU-C sıcaklık 0,810/0,812; aşırı koruma 0,606/0,638; karşılaştırma 0,793/0,799;
        reddetme P 0,45/0,48 & C 0,72/0,75 zaten var)
   GAP: §10.5 spesifik kriter-geçerlik ρ (sıcaklık(P)×Beck −0,217 p<0,001; reddetme(P)×Beck 0,171 p=0,008;
        karşılaştırma(P)×Beck 0,261 p<0,001; karşılaştırma(C)×SRQ çatışma 0,303 p<0,001; ×SRQ sıcaklık
        −0,159 p<0,001; ×SRQ rekabet 0,143 p=0,002)

## 4.3. Birincil Hipotez Bulguları (H1–H5)
   ### 4.3.1. H1 — Çocuk Algısı (EMBU-C)      → t06, t07
        GAP: rol-özgül kontrast anlatıya (aşırı koruma DM-İndeks 0,198 [0,048;0,349] sıfırdan ayrık;
             reddetme DM-İndeks 0,154 / DM-Kardeş 0,135; sıcaklık DM-Kardeş 0,160)
   ### 4.3.2. H2 — Kardeş İlişkisi (KİA/SRQ)  → t08, t09
   ### 4.3.3. H3 — Anne Öz-Bildirimi (EMBU-P) → t10, t11
   ### 4.3.4. H4 — Anne Depresyonu → EMBU-P Latent Yapısal Eşitlik Modeli → t12
   ### 4.3.5. H5 — Diadik Tutarlılık          → t13 · Şekil fig-12 BA-grid, fig-13 RSA-surface

## 4.4. [KEŞİFSEL] Genişletilmiş Analiz Katmanları
   ### 4.4.1. [KEŞİFSEL] Aracılık            → t14
   ### 4.4.2. [KEŞİFSEL] Latent Profil ve Sınıf Analizi → t15 · fig-15 lpa-fit
   ### 4.4.3. [KEŞİFSEL] Ağ Analizi          → t16 · fig-16 network-graph, fig-17 network-nct
   ### 4.4.4. [KEŞİFSEL] Klinik Fayda        → t17 · fig-18 roc, fig-19 dca, fig-20 calibration, fig-21 cart-rf
   ### 4.4.5. [KEŞİFSEL] DM Klinik Alt-Analizler → t18
   ### 4.4.6. [KEŞİFSEL·İKİNCİL] İleri Psikometrik ve Bağlamsal Katman   (YENİ — §15+§16)
        §15 (9): trifaktör T-CFA (CFI 0,90/RMSEA 0,047); latent informant-discrepancy SEM (reddetme latent
                 r=0,025 [−0,134;0,185]); floor-aware IRT (index reddetme d=0,372; aşırı koruma latent
                 d 0,543 > manifest 0,370); reliability generalization (ω_h 0,660, ECV 0,409);
                 H1 çoklu-evren 120/120 medyan β=0,134, %75 p<0,05, t=4,084, permütasyon p=0,0002 (ANLAMLI);
                 meta-analitik pooling 0,139 [0,049;0,230] τ=0,106; klinik karar extended AUC 0,703, net
                 fayda 0,86; HbA1c×ebeveynlik Bayesçi (sıcaklık pd=0,944, karşılaştırma pd=0,946, n=39)
        §16 (9): PDT diferansiyel ebeveynlik (Holm 0/16; DM baba-kayırma d=−0,267 [−0,520;−0,013] p=0,039
                 düzeltilmemiş); sosyal tabakalaşma (EGP Holm ns; ISEI/SIOPS/EGP kolinear); anne komorbidite
                 (komorbid→Beck d=0,293 Holm ns; antidepresan DM %29,2 vs kontrol %9,1 χ²=14,45 V=0,248);
                 aile yapısı (diadik karşılıklılık r=0,177–0,384); DM maruziyet yoğunluğu (9 test 0 Holm);
                 anne mental sağlık→çocuk (güncel Beck≥17 → EMBU-C reddetme b=0,134 p=0,004, DM/antidepresandan
                 bağımsız; LCA riskli sınıf → reddetme-uyuşmazlığı p<0,001, kardeş çatışması p=0,006);
                 yönlü kardeş mimarisi (0/3 grup, 0/14 faset FDR); çocuk moderatör (cinsiyet×grup 0/8 Holm;
                 anne yaşı→aşırı koruma b=−0,026/yıl p=0,004); seçilim denetimi (HbA1c MNAR seçilim OR=4,56
                 p<0,001; yıl×grup V=0,585; H1 çocuk-reddetme farkı 2023-only'de zayıflar — dönem temkini)
        Şekiller: phase2_f01..f12 (trifactor, xinfo, floor_irt, h5_strat, h1_spec_curve, meta_forest,
                 xinfo_network, dx_age_spline, imai_sensitivity, dag_validation, ppc_replication, dca_heatmap);
                 expl_f01..f06 (reciprocity, pdt_direction, comorbidity, fsm, measurement_race, integrated_panel)
                 → görsel-özgü seçki; hepsi zorunlu değil, konu-eşlemeli 6–10 şekil.

## 4.5. Robustluk ve Bayesçi Doğrulama
   Tablolar: t19 (robustluk), t20 (duyarlılık), t21 (Bayesçi global)
   Şekiller: fig-22 spec-curve, fig-23 sensemakr-contour (+ opsiyon fig-24/25 yalnız görsel-özgüyse — mevcut
            kararda katsayı-forest olarak çıkarılmıştı; korunur)
   GAP: §13.5 H3 eksik-veri çerçeve sağlamlığı (Tamamlanmış N=219 / FIML N=241 / MI m=50 N=241; en büyük
        çerçeve-arası yayılım reddetme 0,006 SD; MNAR δ ızgarası −0,036→−0,037, p≈0,31)
   GAP: §13.6 H3 SES operasyonelleştirme sağlamlığı (latent CFA / Hollingshead / eşit-ağırlık / ham ISEI;
        reddetme β −0,039/−0,031/−0,038/−0,031; yayılım 0,008 SD)

## 4.6. Niteliksel Kol Bulguları
   ### 4.6.1. Niteliksel Örneklem ve Analitik Çerçeve
        GAP: analitik ölçek sayıları (7 aile triadı; 21 görüşme; anne 7 + T1DM çocuk 7 + kardeş 7;
             23 codebook kodu / 5 kategori; 116 araştırmacı-denetimli kodlanmış segment; 57 triadik matris
             satırı; rol quote dağılımı anne 55 / çocuk 36 / kardeş 25)
   ### 4.6.2. Tema 1 — Sağlıklı Kardeşin Görünmeyen Yükü
        GAP kod: KARDES_ILISKISI, BESLENME_KONTROL (mevcut: KARDES_GORUNMEZ_YUK, OFKE_ADALETSIZLIK, AILE_ICI_ADALET)
   ### 4.6.3. Tema 2 — Annenin Tıbbi Bakıcı Rolüne Kayması
        GAP quote: 014_mother_q002 · GAP kod: KAYGI_KIRILGANLIK, COCUK_OZERKLIK_OZBAKIM, AILE_DESTEGI, ILETISIM_CATISMA
   ### 4.6.4. Tema 3 — T1DM Tanılı Çocuğun İçeriden Deneyimi
        GAP quote: 026_t1dm_child_q002, 202_t1dm_child_q002
        GAP kod: RUTIN_TAKIP, BESLENME_KONTROL, AKRAN_CEVRE_DESTEGI, KARDES_ILISKISI
   ### 4.6.5. Tema 4 — Aynı Evde Üç Farklı Deneyim
        GAP: öne çıkan kod satırı TAMAMEN eksik → RUTIN_TAKIP, KAYGI_KIRILGANLIK, OFKE_ADALETSIZLIK,
             KARDES_GORUNMEZ_YUK, KARDES_ILISKISI, AILE_ICI_ADALET, COCUK_OZERKLIK_OZBAKIM
        GAP quote (her rol 5): anne +026_mother_q009, +011_mother_q007; çocuk +020_t1dm_child_q002,
             +014_t1dm_child_q002; kardeş +019_healthy_sibling_q003, +201_healthy_sibling_q001
   ### 4.6.6. Çapraz Bilimsel Neticeler                       (YENİ — 6 temalar-arası sonuç, YÜKSEK öncelik)
        (1) T1DM aile-düzeyi düzenleme rejimi üretir; (2) anne bakımı klinik+ahlaki sorumluluk olarak
        içselleştirir; (3) sağlıklı kardeş yükü çoğu zaman sessizdir; (4) çocuk normalleşme-farklılık
        arasında müzakere eder; (5) koruma/kontrol/adalet aynı davranışta birleşir; (6) triadik farklılık
        bilimsel sonuçtur, hata değildir.
   ### 4.6.7. Negatif Vaka, Sınırlayıcı Örüntüler ve Odak Aile Matrisi   (YENİ/konsolide)
        Tema 4 sistematik negatif-vaka (3-alan: karşıtlık işaretleri; "Normal" söylemi; Aile 201 rol temsili);
        odak aile matrisi (011=5, 202=5 odak; 201=1 en düşük) → Aile 201 aktarılabilirlik / bilgi gücü
        eşitsiz dağılım okuması (yorumsuz betim).

## 4.7. Karma Bulgulara Köprü (Joint Display)
   Tek kanonik tablo (6 satır: H1–H5 + Meta triadik informant asimetrisi); sütunlar: Odak | Nicel verdikt
   (yön+belirsizlik) | Nitel örüntü | İlişki türü | Yorum sınırı. Provenans ankrajları korunur (.qmd).
   "Provisional/TASLAK" etiketi ve ikinci tablo KALDIRILIR.

## 4.8. Genel Bulgu Sentezi
   Yorumsuz özet korunur; nitel çapraz-neticeler eklendikten sonra "dört makro tema + 6 çapraz netice"
   omurgasına hizalanır. Yorum cümlesi girmez.
```

## 4. Tablo yerleşim haritası (K3 — konu edildiği yere dağıt)

| Tablo | Yeni yeri | Tablo | Yeni yeri |
|---|---|---|---|
| t01 örneklem | 4.1 | t12 H4 SEM | 4.3.4 |
| t02 kovaryat denge | 4.1 | t13 H5 concordance | 4.3.5 |
| t03 eksik veri | 4.1 | t14 aracılık | 4.4.1 |
| t04 eğilim skoru | 4.1 | t15 LPA/bifaktör | 4.4.2 |
| t05 SES kompozit | 4.1 | t16 ağ | 4.4.3 |
| (güvenirlik: apa tablosu YOK → 4.2 anlatı+şekil) | 4.2 | t17 klinik | 4.4.4 |
| t06 H1 primary | 4.3.1 | t18 DM klinik | 4.4.5 |
| t07 H1 Bayesçi | 4.3.1 | t19 robustluk | 4.5 |
| t08 H2 aile-ortalama | 4.3.2 | t20 duyarlılık | 4.5 |
| t09 H2 APIM | 4.3.2 | t21 Bayesçi global | 4.5 |
| t10 H3 primary/IPTW | 4.3.3 | t22 sentez | 4.8 |
| t11 H3 duyarlılık | 4.3.3 | | |

Her tablo R chunk'ı (`apa_render_table("tNN_...")`) ilgili alt bölüme taşınır; `#| tbl-cap` üstte, `apa_tr_decimal()` render'ı korunur. Sondaki "## APA Tablo Seti" bölümü silinir.

## 5. Yapılacak düzeltmeler (mimari/tutarlılık)

- **F1:** Psikometri yanlış-atıfı (`Tablo 5 / apa_t05`) kaldırılır; güvenirlik 4.2'de anlatı + `psychval-01/02` şekilleriyle verilir.
- **F2:** Sondaki toplu "APA Tablo Seti" bloğu kaldırılır (22 R chunk konu bölümlerine dağılır).
- **F3:** İki joint-display tablosu tek kanonik tabloya birleştirilir; "Provisional/TASLAK" HTML yorumu ve etiket kaldırılır.
- **F4:** Marmara başlık numaralandırması (`4.`, `4.1.`, `4.1.1.`) uygulanır; kapitalizasyon/bağlaç/başlık-sonu-noktalama kuralları denetlenir.
- **F5:** Ondalık/`p` biçimi anlatıda §1.4/§12'ye göre denetlenir (ör. yüzde/ortalama 1 basamak; test/oran 2; p 3).
- **F6:** Şekil altyazıları alt konumda, `Şekil N.` kalıbı; tablo başlıkları üst; dipnotlar (kısaltma/test/p) eklenir.

## 6. Kısıtlar (ihlal edilemez)

- **Yorumsuz.** Hiçbir yorum/çıkarım/literatür-karşılaştırma cümlesi girmez (marmara §3.6; kılavuz §2).
- **İzlenebilirlik.** Her sayı CSR.qmd §9–§16 veya `outputs/tables/apa_t*.csv`'ye izlenir; **uydurma sayı yok** (Stop kapısı).
- **KVKK.** Nitel tarafta yalnız tema/alt tema/kod/quote-ID; ham transcript, aile demografisi, alıntı metni girmez.
- **Kanıt türü ayrımı.** Nitel tema nicel etki gibi yazılmaz; joint display kanıt türünü açık etiketler.
- **[KEŞİFSEL] disiplini.** §12 ve §15/§16 bulguları birincil hipotez sonucu gibi yazılmaz; etiket korunur.

## 7. Doğrulama planı (üretimden sonra)

- **Traceability cross-check:** her alt bölümün sayıları CSR.qmd / nitel .qmd ankrajına karşı doğrulanır (paralelleştirilebilir — alt bölüm başına bir doğrulama ajanı).
- **sci-audit 7-eksen** (`/sci-audit:audit chapters/04_bulgular.qmd --lang tr --strictness certification`): A referans, B claim-grounding, C istatistik (statcheck/GRIM/ondalık), D halüsinasyon, E kılavuz (JARS-Mixed), F AI-şeffaflık, G Türkçe imla (ondalık-nokta `p` = blocker).
- **Marmara format kontrol** (talimatname §12 checklist): başlık/tablo/şekil/ondalık/atıf.
- **Render dumanı:** `quarto render` bölüm chunk'larının (apa_render_table, şekil yolları) kırılmadığını doğrular.
- Bölüm finalizasyonu `bolum-sertifika` Kapı 0–5 + açık kullanıcı onayı olmadan **final değildir** (provisional-pass).

## 8. Kapsam dışı

- 01–03 ve 05 bölümlerinin numaralandırılması (tez-geneli `number-sections` kararı ayrı iş).
- Tartışma/yorum/literatür entegrasyonu (Bölüm 5'e ait).
- `outputs/tables` / `_targets` yeniden üretimi (kanonik CSV kilitli; bu iş yalnız `chapters/04_bulgular.qmd` yazımıdır).
- Yeni analiz veya yeni sayı üretimi (yalnız kanonik kaynaklardan aktarım).

## 9. Kabul ölçütü

- CSR.qmd §9–§16 ve nitel .qmd'deki her raporlanabilir bulgu bölümde temsil edilir (envanter boşluk listesi kapanır).
- 22 APA tablosu + görsel-özgü şekiller konu bölümlerine dağıtılmış; toplu blok yok; hiçbir bulgu hem tablo hem şekil değil.
- Marmara numaralı başlık + ondalık/atıf/başlık biçimi uyumlu.
- Nitel: 4 makro tema tam ankrajlı + 6 çapraz netice + negatif-vaka/odak matris + analitik ölçek.
- Joint display tek kanonik tablo; sentez yorumsuz.
- sci-audit blocker (özellikle axis G ondalık + axis A/B) sıfır.
