# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 03 — GEREÇ ve YÖNTEM |
| Bölüm başlığı | GEREÇ ve YÖNTEM |
| Üretim dosyası | `chapters/03_gerec_ve_yontem.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md` |
| Sertifikasyon tarihi | 2026-07-16 |
| Önceki sertifika | `03-gerec-ve-yontem-sertifika-2026-07-07.md` (`certified-final`) |
| Yeniden sertifikasyon nedeni | Bölüm bu oturumda düzenlendi (güç analizi genişletmesi, STROBE akış atfı, analiz-planı tablosu, q25 kanonik kod, keşifsel katman geçiş cümlesi); 4 yeni referans eklendi. |
| Sertifikasyonu uygulayan | Ona (Claude Opus 4.8) — Kapı 0–5 yeniden denetimi |
| Uygulama onayı | **Kullanıcı açık onayı ("Uygun", 2026-07-16)** — bütünsel sertifikasyon kapsamında `certified-final`. |

## Bu Oturumdaki Değişiklik Envanteri

`chapters/03_gerec_ve_yontem.qmd` üzerinde (git diff: +19/−5 satır):

1. **Araştırma evreni ve örneklem (§30):** Kilitli kanonik veri tabanından aile
   düzeyi analiz tabanına geçişi özetleyen katılımcı akışına STROBE akış şeması
   atfı eklendi (`@vandenbroucke2007strobe`), `@fig-strobe-flow`'a çapraz-referans.
2. **Örneklem büyüklüğü ve güç analizi (§38–40):** Birincil (*a priori*) OpenEpi
   hesabı iki grup ortalama farkı olarak netleştirildi; SEM/APIM/çok-düzeyli
   modeller için tasarım-temelli iki güvence (küme sayısı `@maas2005sufficient`;
   retrospektif güç eleştirisi `@hoenigHeisey2001abusePower`) ve simülasyon-temelli
   hassasiyet (`simr`/`pwr`, `@green2016simr`) eklendi; n = 39 HbA1c katmanı
   keşifsel/betimsel konumlandırıldı.
3. **s-EMBU-C (§66):** Ters-puanlanan maddeye kanonik kod (`q25`) ve madde metni
   eklendi; s-EMBU-P'de karşılık gelen maddenin final kanonda ters-puanlanmadan
   kaydedildiği notu eklendi.
4. **Hipotez temelli modeller (§136–146):** `@tbl-analiz-plani` (H1–H5 ×
   sonuç × birincil model × kovaryat × çoklu düzeltme) eklendi.
5. **Keşifsel katmanlar (§170):** İki keşif kümesi arasındaki geçiş cümlesi
   yeniden yazıldı (örüntü-derinleştirme vs. ölçüm-modeli-genişletme ayrımı).

Bu oturumun **Kapı 3 düzeltmeleri:** `@tbl-analiz-plani` içindeki tanımsız
kısaltmalar (`RSA`, `CFM`, `dCFA`, `ANCOVA`, `SH`) metinle uyumlu açık
Türkçe adlara/biçimlere hizalandı (H3 "Kovaryans analizi … HC3 sağlam standart
hata"; H5 "ICC/Bland-Altman, yüzey tepki, ortak yazgı, diadik CFA, APIM").

Sınır: Ham veri / transcript / demografi satırı / credential sertifikaya
**taşınmadı**; nitel örneklem satır-düzeyi demografisi KVKK gereği açılmadı.

## Kapı 0: Kapsam ve Gizlilik — PASS

- [x] Bölüm dosyası + sertifikasyon playbook'u + önceki sertifika okundu.
- [x] Değişiklik envanteri git diff ile çıkarıldı (yukarıda).
- [x] Gizlilik sınırı korundu (satır-düzeyi veri/PII taşınmadı).

## Kapı 1: Derin Literatür ve Künye Evreni — PASS

- Bölümdeki 73 benzersiz atıf (fig/sec/tbl çapraz-ref önekleri hariç) taranıp
  `references/references.bib` (333 künye) ile bire-bir eşleştirildi:
  **orphan-citation = 0**, retired-key kullanımı yok.
- Bu oturumda eklenen 4 künye metadata doğrulandı:
  `maas2005sufficient`, `hoenigHeisey2001abusePower`, `green2016simr`,
  `vandenbroucke2007strobe` — hepsi tam alan setli (author/title/journal/
  year/volume/number/pages/doi).

Kapı 1 kararı: **PASS**

## Kapı 2: Full-Text, DOI ve Ledger Mutabakatı — PASS

- 4 yeni künyenin DOI'si **Crossref canlı API** ile doğrulandı; başlık/yıl/dergi
  birebir eşleşti:
  - `10.1027/1614-2241.1.3.86` → "Sufficient Sample Sizes for Multilevel Modeling", *Methodology* 2005 ✓
  - `10.1198/000313001300339897` → "The Abuse of Power", *The American Statistician* 2001 ✓
  - `10.1111/2041-210X.12504` → "SIMR: an R package…", *Methods in Ecology and Evolution* 2016 ✓
  - `10.1371/journal.pmed.0040297` → "Strengthening the Reporting of Observational Studies… (STROBE)", *PLoS Medicine* 2007 (PMC2020496 açık tam metin) ✓
- **Ledger güncellendi:** 4 künye `referans-denetim-ledgeri.md` ana tablosuna
  `cite-ok` (identity-doğrulamalı) durumuyla eklendi (kullanım sütunu = GEREÇ ve
  YÖNTEM). AI-reliability sütunları "bölüm kapanışında (WS-D)".
- `bib_hygiene reconcile` (03): **HARD undefined = 0**; orphan yalnız INFO
  (`mcneishWolf2020toplamPuan` — bib-tanımlı, bu bölümde atıfsız; blok değil).

Kapı 2 kararı: **PASS**

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu — PASS (bu oturumda düzeltildi)

- [x] Resmi başlık korundu: `# GEREÇ ve YÖNTEM`.
- [x] **Çapraz-referans hedefleri doğrulandı:** `@tbl-analiz-plani` (bu bölümde
  tanımlı+atıflı), `@fig-strobe-flow` (`04_bulgular.qmd:181`), `@sec-kesifsel-genisletme`
  (`04_bulgular.qmd:421`) — üçü de canlı hedefe bağlı.
- [x] **`@tbl-analiz-plani` sözdizimi** Pandoc JSON ile geçerli; 5 sütun × 5 satır
  (H1–H5). Tablo `04`'teki H1–H5 açıklamalarıyla tutarlı.
- [x] **Tanımsız kısaltma temizliği:** tabloda tek başına kalan `RSA/CFM/dCFA/
  ANCOVA/SH` metinle uyumlu açık adlara çevrildi; kalan tüm kısaltmalar
  (`BH-FDR/HC3/SES/ICC/CFA/APIM/WLSMV/SEM`) 00b veya metinde tanımlı.
- [x] **İç aritmetik tutarlı:** 120+120+121+121 = 482 çocuk gözlemi;
  240 T1DM + 242 kontrol = 482; 241 aile; HbA1c 39/120 T1DM indeks (yapısal eksik).
- [x] Ölçek yapıları tutarlı: s-EMBU 29 madde/4 alt ölçek (9+7+8+5); özgün 23/3;
  KİA 48; Beck 21 (0–63).
- [x] q25 eklemesi kanonik form dokümantasyonuyla uyumlu (ters-puanlama; s-EMBU-P
  farkı).

Kapı 3 kararı: **PASS**

## Kapı 4: Türkçe İmla, Akış ve Mantık — PASS

`tr_corpus_audit all` (axis H, sci-audit axis G eşdeğeri):

- **HARD (blocker): 0**
- **SOFT (major): 6** — `H1–H5` (kasıtlı hipotez notasyonu, §20) ve `JARS-`
  (§16). Tümü bu oturum öncesinden mevcut kasıtlı bilimsel notasyon.
- **advisory: 57** — çoğu `H-ABBR-UNUSED` (00b'de tanımlı, izole tek-bölüm
  denetiminde kullanılmayan; diğer bölümlerde kullanılıyor — tek-dosya artefaktı).
- **Baseline karşılaştırması (`git stash`):** baseline'da da HARD 0 / SOFT 6;
  bu oturum düzenlemeleri **yeni major/blocker üretmedi**, advisory 61→57'ye
  düştü (tanımsız kısaltma temizliği).
- **Ondalık kontrolü:** bu oturum eklenen satırlardaki tek `X.Y` deseni `3.01`
  (OpenEpi sürüm numarası, ondalık istatistik değil). İngilizce ondalık `p`/etki
  değeri yok; Türkçe virgül-ondalık standardı korundu.

Kapı 4 kararı: **PASS**

## Kapı 5: AI-Reliability ve Teknik Doğrulama — PASS

| Eksen | Sonuç |
|---|---|
| A referans bütünlüğü | 4 yeni künye Crossref-doğrulı; orphan 0; retraction yok |
| B claim grounding | Metodoloji-odaklı; sonuç sızıntısı yok (güç iddiaları CI/Bayes/TOST'a bağlı) |
| C istatistik iç-tutarlılık | Örneklem/rol aritmetiği ve tablo↔metin tutarlı |
| D halüsinasyon | Uydurma araç/kaynak yok; `simr`/`pwr`/OpenEpi gerçek araçlar |
| E kılavuz uyumu | STROBE akış-şeması atfı doğru bağlamda; COREQ notu (Domain-3 nitel Bulgular'a ertelidir, önceki sertifikadan devir) |
| F AI-şeffaflık | §Yapay Zekâ Destekli Araç Kullanımı beyanı mevcut |

- **Repo invaryant:** `doktoratezi-ai-audit` **144/144**; `t1dm-qual-ai-audit`
  **55/55**.
- **`git diff --check`:** temiz (bib EOF boş-satır düzeltildi).
- **Render doğrulaması:** `pandoc --citeproc` (marmara-ama11.csl) 03 bölümünü
  başarıyla derledi (EXIT 0, 102 KB); **eksik bib atıfı uyarısı yok**; 4 yeni
  referans, q25 ve analiz-planı tablosu çıktıda çözüldü. Üç uyarı yalnız Quarto
  çapraz-referans önekleri (`fig-/sec-/tbl-`) — tam tez render'ında çözülür.

Kapı 5 kararı: **PASS**

## Bloklayıcı Olmayan İzlenen Maddeler (önceki sertifikadan devir)

| Öğe | Durum | Çözüm |
|---|---|---|
| COREQ 13 (yaklaşılan/reddeden anonim aile sayısı) | açık — bloklayıcı değil | Araştırmacı girdisi bekler; fabrike edilmedi. |
| COREQ 16 (nitel alt örneklem anonim agregat demografisi) | açık — bloklayıcı değil | KVKK gereği satır-düzeyi veri açılmadı; anonim agregat araştırmacı girdisi bekler. |
| COREQ 28–32 (Domain 3) | ertelenmiş | Nitel BULGULAR + Ekler COREQ tablosu yazıldığında kapanır. |

## Nihai Sertifika Kararı

| Kapı | Karar |
|---|---|
| Kapı 0 | PASS |
| Kapı 1 | PASS |
| Kapı 2 | PASS |
| Kapı 3 | PASS (tablo tanımsız-kısaltma temizliği bu oturumda) |
| Kapı 4 | PASS (0 blocker; SOFT/advisory kasıtlı notasyon + tek-dosya artefaktı) |
| Kapı 5 | PASS (144/144 + 55/55; render temiz) |
| **Nihai durum** | **`certified-final`** |

**Karar gerekçesi:** Tüm teknik kapılar (0–5) bu oturumun güncel metniyle
yeniden çalıştırıldı ve PASS verdi; bu oturumun düzenlemeleri yeni
major/blocker üretmedi, advisory sayısını düşürdü. Playbook Nihai Karar
Kuralı gereği `certified-final` için gereken **açık kullanıcı uygulama onayı**
2026-07-16 tarihinde bütünsel sertifikasyon kapsamında ("Uygun") alınmıştır.
İzlenen COREQ maddeleri bloklayıcı değildir ve önceki sertifikadan
devralınmıştır.
