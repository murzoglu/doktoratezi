# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 03 — GEREÇ ve YÖNTEM |
| Bölüm başlığı | GEREÇ ve YÖNTEM |
| Üretim dosyası | `chapters/03_gerec_ve_yontem.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md` |
| Sertifikasyon tarihi | 2026-07-07 |
| Sertifikasyonu uygulayan | Claude Code (Opus 4.8) — sertifikasyon tekrar denetimi |
| Uygulama onayı | `verildi` — "manuel inceleme ok" (2026-07-07) |
| Onay veren | Araştırmacı (kullanıcı) |

## Kapı 0: Kapsam ve Gizlilik — PASS

- [x] Bölüm dosyası + kanonik format talimatnamesi + sertifikasyon playbook'u okundu.
- [x] Ham veri / transcript / demografi satırı / credential rapora **taşınmadı**. Nitel örneklem demografisi (aile-düzeyi) bilinçli olarak açılmadı (KVKK sınırı).

## Kapı 1: Derin Literatür ve Künye Evreni — PASS (re-certification)

- Orphan-citation: 0 orphan. Retired-key kullanımı: yok.
- Metodoloji referansları (`braunClarke2006/2019`, `malterud2016informationPower`, `tong2007coreq`, `eisikovits2010dyadic`, `taylorDeVocht2011separate`, `lincolnGuba1985`, `huBentler1999cutoff`, `chen2007invariance`, `muthenAsparouhov2012bsem`, `lakens2017equivalence`, `steegen2016multiverse`, `li2016ordinalCFA`, `putnickBornstein2016`, `mokkink2018cosmin`, `trizanoHermosilla2016omegaAlpha`) ledger'da kapalı.
- citation-verifier (axis A): `malterud2016informationPower`, `tong2007coreq`, `braunClarke2006thematic`, `furmanBuhrmester1985srq` çözüldü, metadata birebir; **`lincolnGuba1985` gerçek 1985 Sage kitabı olarak doğrulandı — uydurma DOI yok**. Retraction yok.

Kapı 1 kararı: **PASS**

## Kapı 2: Full-Text, Zotero — PASS (re-certification)

Ölçek/kılavuz/metodoloji citation'ları ledger'da `cite-ok`. `lincolnGuba1985` kitap olduğundan DOI'siz (doğru); tam metin gereksinimi kitap referansı olarak karşılanır.

Kapı 2 kararı: **PASS**

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu — PASS (bu oturumda düzeltildi)

- [x] Resmi başlık: `# GEREÇ ve YÖNTEM` (büyük harf, "ve" küçük).
- [x] **Başlık kapitalizasyonu düzeltildi (§1.3):** 11 adet üçüncü düzey `###` alt başlık Title Case → **sentence case**'e çevrildi (yalnız ilk sözcük büyük):
  `Dahil edilme ve dışlanma ölçütleri`, `Örneklem büyüklüğü ve güç analizi`, `Örnekleme yöntemi`, `Demografik ve tıbbi bilgi formu`, `Tanımlayıcı istatistikler ve grup dengesi`, `Eksik veri yönetimi`, `Nedensel çıkarım çerçevesi`, `Hipotez temelli modeller`, `Duyarlılık ve sağlamlık çözümlemeleri`, `Bayesçi paralel hat`, `Tamamlayıcı ve keşifsel çözümleme katmanları`.
  Resmi ölçek adları (`Kısaltılmış Algılanan Ebeveyn Tutumları Ölçeği – Çocuk/Ebeveyn Formu`, `Kardeş İlişkileri Anketi`, `Beck Depresyon Envanteri`) özel ad olarak büyük harf korundu. Böylece bölüm içi başlık biçimi tekdüze ve GENEL BİLGİLER ile tutarlı hâle geldi.
- [x] Bölüm işlevi (§3.5): tasarım, yer/tarih, evren/örneklem, örnekleme, değişkenler+tanımlar, veri toplama araçları, psikometrik değerlendirme, veri yönetimi, istatistiksel analiz (H1–H5), nitel kol, karma entegrasyon, refleksivite, raporlama standartları, etik, YZ beyanı — tekrarlanabilirlik düzeyinde.
- [x] **Etik (§3.5):** izin **tarih ve sayı** ile bölümde: KAEK 06.01.2023 / 09.2023.201; Enstitü YK 11.05.2023 / 2023/19-68. Onay belgesi Ekler'e atıflı.
- [x] H1–H5, Faz II/[KEŞİFSEL] ve nitel RTA amaçları ayrık; nitel tema ≠ nicel etki büyüklüğü.
- [x] İç aritmetik tutarlı: 120+120+121+121 = 482 çocuk gözlemi; 240 T1DM + 242 kontrol = 482; 241 aile; HbA1c 39/120 T1DM indeks (yapısal eksik doğru tanımlı).
- [x] Ölçek yapıları tutarlı: s-EMBU 29 madde/4 alt ölçek (9+7+8+5=29), özgün 23 madde/3 alt ölçek; KİA 48 madde; Beck 21 madde/0–63.

Kapı 3 kararı: **PASS**

## Kapı 4: Türkçe İmla, Akış ve Mantık — PASS

sci-audit **axis G** — rapor: `raporlar/03_gerec_ve_yontem-tr-sciaudit.md`

- Errors (blocker): **0**
- Warnings (major): 33 — `sentence-long` (yoğun metodoloji anlatımı); `decimal-dot` işaretleri **yanlış pozitif**: `3.01` (OpenEpi sürümü), `06.01`/`09.2023`/`11.05` (etik tarih ve protokol numaraları); `english-term-leak: Framework` = "*Open Science Framework* (OSF)" tanımı (§1.5 uyumlu). `colloquial: çok fazla` = KİA Likert çıpası ("çok çok fazla").
- G5 blocker (İngilizce ondalık `p`): yok.

Kapı 4 kararı: **PASS**

## Kapı 5: AI-Reliability ve Teknik Doğrulama — PASS (COREQ notu ile)

Manüskript adli denetimi (sci-audit axes A–F) + **COREQ-32 eşlemesi (E):**

| Eksen | Sonuç |
|---|---|
| A referans bütünlüğü | Metodoloji referansları çözüldü, retraction yok, `lincolnGuba1985` gerçek kitap |
| B claim grounding | Bölüm metodoloji-odaklı; sonuç sızıntısı yok (α, taban etkisi vb. Bulgular'a bırakılmış) |
| C istatistik iç-tutarlılık | Örneklem/rol aritmetiği iç-tutarlı (yukarıda) |
| D halüsinasyon | Uydurma araç/kaynak yok |
| **E COREQ-32** | **24 present / 5 partial / 3 missing** (guideline-mapper) |
| F AI-şeffaflık | §Yapay Zekâ Destekli Araç Kullanımı beyanı mevcut ve yeterli |

**COREQ ayrıntısı:**
- Domain 1 (araştırma ekibi/refleksivite, madde 1–8) ve Domain 2 (tasarım, madde 9–27): güçlü. Bilinçli tasarım tercihleri (pilot yok, kappa yok, transkript iadesi yerine görüşme-içi özetleme, doygunluk yerine bilgi gücü) sınırlılık olarak **açıkça** raporlanmış → COREQ uyumlu.
- **Metodüzeyi kısmi (3):** madde 7 (katılımcının araştırmacıyı tanıması — telefon davetinde "bilgilendirilerek" ifadesiyle kısmen karşılı), madde 13 (**yaklaşılan/reddeden aile sayısı verilmemiş** — gerekçeler nitel; sistematik kaydedilmediği zaten sınırlılık olarak yazılı), madde 16 (**nitel alt örneklem demografisi** yalnız kardeş yaş aralığı 7–12 ile sınırlı).
- **Domain 3 ertelenmiş (madde 28–32):** alıntı sunumu, member-checking, veri–bulgu tutarlılığı, tema açıklığı — bunlar **nitel BULGULAR** bölümünün alanıdır; `04_bulgular.qmd` şu an yalnız niceldir. Bu, GEREÇ ve YÖNTEM bölümünün **kusuru değil**, kapsam sınırıdır. Ayrıntılı 32-madde eşleştirme tablosu Ekler'e planlanmış.

Repo/veri invaryantı: `doktoratezi-ai-audit` **142/142**; `t1dm-qual-ai-audit` **55/55**; `git diff --check` temiz; `quarto check` OK. AI-use log güncellendi.

Kapı 5 kararı: **PASS** (blocker yok; açık COREQ maddeleri aşağıda bloklayıcı-olmayan olarak izlenir)

## Bloklayıcılar ve Çözüm

| Öğe | Durum | Çözüm |
|---|---|---|
| COREQ 13 (non-participation sayısı) | açık — bloklayıcı değil | Araştırmacı yaklaşılan/reddeden **anonim aile sayısını** eklemeli (fabrikasyon yapılmadı). |
| COREQ 16 (nitel alt örneklem demografisi) | açık — bloklayıcı değil | Araştırmacı **anonim agregat** ekleyebilir (indeks çocuk yaş aralığı, anne yaş aralığı, tanı süresi dağılımı, cinsiyet); KVKK gereği bu satır-düzeyi veri ajan tarafından açılmadı. |
| COREQ 28–32 (Domain 3) | ertelenmiş | Nitel BULGULAR + Ekler COREQ tablosu yazıldığında kapanır. |

## 2026-07-07 Yeniden Doğrulama — KİA/SRQ Türkçe kaynak düzenlemesi

Bu bölüm, önceki `provisional-pass` denetiminden **sonra** düzenlendi
(`chapters/03_gerec_ve_yontem.qmd` §Kardeş İlişkileri Anketi). Bu nedenle
onay öncesi etkilenen kapılar güncel metinle yeniden çalıştırıldı:

- **Değişiklik:** SRQ'nun Türkçe uyarlama kaynağı olarak Apalaçi (1996)
  [@apalaci1996yoktez] metne bağlandı; Aktaş (2017)
  [@aktas2017kardesIliskileriOlcegi] "ek/karşılaştırmalı kaynak" olarak
  korundu (kullanılan araç olarak sunulmadı). Bilinçli tez-yasağı istisnası
  (Marmara §3.8.2), kullanıcı onaylı.
- **Kapı 1–2:** Her iki key ledger'da `cite-ok`. Apalaçi YÖK Tez No. 52148 bu
  oturumda `get_yok_tez_thesis_details` ile yeniden doğrulandı (Boğaziçi Üni. /
  SBE / Psikoloji ABD, YL tezi, 1996; özet SRQ boyutlarını — sıcaklık/yakınlık,
  asimetri — Türkçe kullanımla teyit ediyor). Ledger kullanım sütunu GEREÇ ve
  YÖNTEM'i içerecek şekilde güncellendi (`apalaci1996yoktez`,
  `aktas2017kardesIliskileriOlcegi`, `furmanBuhrmester1985srq`).
- **Kapı 3:** Orphan-citation taraması temiz; her iki key `references.bib`'te;
  başlık/biçim değişmedi.
- **Kapı 4:** sci-audit axis G yeniden koşuldu — **0 error, 33 warning**
  (önceki sertifikayla birebir; düzenleme yeni uyarı üretmedi).
- **Kapı 5:** `doktoratezi-ai-audit` **142/142**, `t1dm-qual-ai-audit` **55/55**,
  `git diff --check` temiz, `quarto check` OK; citeproc çözümlemesi
  "(Apalaçi 1996)" ve "(AKTAŞ 2017)" biçiminde başarılı — kayıp atıf uyarısı yok.

Sonuç: düzenleme sonrası tüm kapılar PASS; sertifika güncel metinle geçerlidir.

## Nihai Sertifika Kararı

| Kapı | Karar |
|---|---|
| Kapı 0 | PASS |
| Kapı 1 | PASS |
| Kapı 2 | PASS |
| Kapı 3 | PASS (bu oturumda başlık biçimi düzeltildi) |
| Kapı 4 | PASS |
| Kapı 5 | PASS (COREQ Domain-3 nitel Bulgular'a ertelendi) |
| **Nihai durum** | **`certified-final`** |

Final notu: Metodoloji bölümü olarak tüm teknik kapılar PASS (düzenleme sonrası yeniden doğrulama yukarıda). Kullanıcı 2026-07-07'de açık uygulama onayı verdi ("manuel inceleme ok", Nihai Karar Kuralı #5) → **`certified-final`**. **Bloklayıcı olmayan, izlenen açık maddeler** certified-final'ı engellemez ama takipte kalır: COREQ 13 (yaklaşılan/reddeden anonim aile sayısı) ve COREQ 16 (nitel alt örneklem anonim agregat demografisi) araştırmacı girdisi bekler; COREQ Domain 3 (28–32) nitel BULGULAR yazıldığında kapanır. Bu maddeler fabrike edilmedi; KVKK gereği satır-düzeyi veri ajan tarafından açılmadı.
