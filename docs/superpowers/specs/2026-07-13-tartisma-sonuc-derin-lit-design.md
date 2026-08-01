# TARTIŞMA ve SONUÇ — Derin-Literatür Yeniden Yazımı (Tasarım Spec'i)

> **Tarih:** 2026-07-13 · **Dal:** `feat/nitel-kanonik-lit-derinlestirme` ·
> **Hedef dosya:** `chapters/05_tartisma_ve_sonuc.qmd`
> **Bağlayıcı otorite:** `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md`,
> `marmara-tez-formati-talimatnamesi.md` §3.7/§6, bölüm brief'i
> `tez-yazim/03_bolum-hazirlik/05_tartisma-ve-sonuc.md`,
> literatür kaskadı `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`,
> nitel çerçeve `tez-yazim/05_entegrasyon/nitel-cikti-cercevesi.md`.

## 1. Amaç ve Kapsam

Bulgular bölümünde (`chapters/04_bulgular.qmd`, 4.1–4.8) ortaya konan **tüm neticeleri**
— birincil H1–H5, [KEŞFİSEL] genişletilmiş katmanlar, nitel 4 makro tema, karma joint
display — mümkün olan **en geniş tam-metin literatür** bağlamında bilimsel derinlikte
tartışan, akıcı (alt başlıksız) Marmara-uyumlu bir `TARTIŞMA ve SONUÇ` bölümü üretmek.

Her netice için dört soru yanıtlanır (kullanıcı 2. direktifi): **(1)** verinin anlamı
nedir; **(2)** bugüne dek yapılan araştırmalar ne söylüyor; **(3)** neler eksikti ve bu
veriyle neyi anlamlandırdık; **(4)** diğer çalışmalarla örtüşen/örtüşmeyen yönler +
bundan sonra ne yapılmalı. Özgün değer altı çizilerek geniş biçimde tartışılır.

### 1.1 Kapsam dışı (non-goals)

- Bulgu/istatistik **tekrarı** (Marmara §3.7 — yalnız yorum; tablo/şekle atıf yeterli).
- `GİRİŞ`/`GENEL BİLGİLER` arka-plan tekrarı.
- Nedensellik dili (kesitsel + olgu-kontrol tasarım — "ilişkili/öngörüyor" korunur).
- Keşfisel/post-hoc bulguyu doğrulanmış sonuç gibi konumlandırma.
- Nitel temayı nicel etki kanıtı, nicel sonucu nitel mekanizma kanıtı yapma.
- Ham transkript / satır-düzeyi / kimliklenebilir veri (KVKK — connector'lara gitmez).

## 2. Sabitlenen Kararlar (brainstorm)

| # | Karar | Değer |
|---|---|---|
| K1 | Mimari omurga | **Marmara-uyumlu tek akış** — alt başlık YOK; paragraf omurgası + geçiş cümleleri |
| K2 | Literatür derinliği | **Tüm katmanlar eşit-derin** — [KEŞFİSEL] epistemik disiplinle ("tutarlı/hipotez-üretici", asla "doğrulandı") |
| K3 | Referans kapısı sırası | **Taslak → toplu kapı** — önce tam-metin tarama + aday-atıflı taslak, sonra `/referans-kapisi` toplu |
| K4 | Hipotez sırası (M2) | **Bilgi-verici düzlemi**: çocuk (H1) → anne (H3) → depresyon-yolu (H4) → kardeş (H2) |
| K5 | Kanıt matrisi | **Kalıcı ara-artefakt** — `tez-yazim/02_kanit-haritalari/tartisma-kanit-matrisi.tsv` |
| K6 | Fan-out | **8 bulgu-kümesi** + fan-out sonrası çapraz kaynak-dedup/iddia-uzlaştırma |

## 3. Bulgu-kümesi Ayrıştırması (literatür fan-out birimleri)

Her küme = bir tam-metin literatür-tarama birimi (D0–D6) + akıştaki bir yorum hareketi.

| # | Küme | İç bulgu ankrajı | Literatür ekseni (en geniş) |
|---|---|---|---|
| **C1** | H1 çocuk algısı / reddetme | `apa_t06/t07`, CSR#h1-karar | Pinquart meta-analizleri, Rohner PARTheory kabul-red, çocuk↔ebeveyn bildirimi ayrışması, EMBU-C, kronik hastalık algılanan ebeveynlik |
| **C2** | H3 anne öz-rapor H₀ + sosyal istenirlik | `apa_t10/t11`, CSR#h3-karar | Streisand-Monaghan T1DM anne yükü/stres, sosyal istenirlik & savunmacı yanıt, öz-rapor↔gözlem farkı, "iyi anne" temsili, TOST/eşdeğerlik yorumu |
| **C3** | H4 maternal depresyon → ebeveynlik | `apa_t12`, CSR#h4-karar | Goodman & Lovejoy mediator meta-analizleri, depresyon-parenting yolları, T1DM'de maternal depresyon, latent SEM yorum sınırı |
| **C4** | H2 kardeş ilişkisi | `apa_t08/t09`, CSR#h2-karar | Kronik/pediatrik hastalıkta kardeş uyumu (Lummer-Aikey + meta-analizler), görünmez yük, SRQ Furman-Buhrmester, "kanıt yetersizliği ≠ eşdeğerlik" |
| **C5** | H5 + diadik / informant / triadik | `apa_t13`, CSR#h5-karar, CSR#sec-genel-hipotez-ozet | Diadik konkordans, ebeveyn-çocuk uyumu, çok-bilgi-verici ayrışması (De Los Reyes), Olsen-Kenny SRM, ICC agreement (Cicchetti/Koo-Li), Kenny-Kashy-Cook — **birincil karma katkı** |
| **C6** | Nitel 4 makro tema | `niteliksel/...report.md` tema 1–4 | Kronik hastalıkta aile deneyimi, hastalık müdahaleciliği, T1DM yaşanmışlık, damgalanma-normalleşme, aile sistemleri, kardeş görünmez yük, RTA yorum |
| **C7** | Keşfisel katmanlar | `apa_t14–t18`, phase2/exploratory | Aracılık (Imai-Keele-Tingley), LPA tipoloji, ağ/GGM (NCT), klinik risk skoru/DCA (Vickers-Elkin), HbA1c×ebeveynlik (ISPAD), taban-duyarlı IRT — **hepsi [KEŞFİSEL]** |
| **C8** | Psikometri / ölçüm (kesişen) | `apa_t*` psikometri, 4.2 | EMBU kısa-form faktör yapısı & güvenirlik, reddetme α=0,45, taban etkisi, ölçüm değişmezliği, Türkçe adaptasyon zorunluluğu |

## 4. Akış Omurgası (Marmara §3, alt başlıksız)

```
M1   Ana bulgu sentezi — çerçeveleme (tekrar değil, birkaç cümle)
M2   Hipotez yorumu (bilgi-verici düzlemi):
       H1 çocuk algısı → H3 anne öz-rapor → H4 depresyon-yolu → H2 kardeş
       (her biri: destek durumu AÇIK + benzer/farklı çalışma + olası neden + tedbir denetimi)
M3   H5 diadik + karma yenilik — nicel NE / nitel NEDEN (birincil katkı; özgün-değer omurgası)
M4   Nitel 4 tema yorumu + negatif vaka + refleksif okuma
M5   Karma bütünleştirme — joint display etiketleri (uyum/tamamlayıcılık/ayrışma/genişleme)
       [mevcut 05 'provisional' 4 meta-çıkarım + 4 köprü BURAYA konsolide]
M6   Keşfisel katmanların ihtiyatlı yorumu ([KEŞFİSEL]; "literatürle tutarlı/hipotez-üretici")
M7   Psikometrik / ölçüm çıkarımları (EMBU adaptasyon)
M8   Güçlü yönler
M9   Sınırlılıklar + sapma şeffaflığı
M10  Sonuç (amacın ne ölçüde gerçekleştiği)
M11  Öneriler (klinik/aile · araştırma · politika) — amaç-bulgu sınırlı
```

### 4.1 Konsolidasyon kararları

1. Mevcut 05'teki alt-başlıklı **"Karma-Kol Meta-Çıkarım" (satır 77–129, provisional)**
   bölümü akıcı **M5** hareketine eritilir; Bulgular 4.7 joint display'i *yorumlar*, tekrarlamaz.
2. `<!-- kaynak: dosya#ankraj -->` yorum-ankrajları **korunur** (izlenebilirlik); görünür
   metin akıcıdır.
3. Özgün-değer çerçevesi M3+M5 omurgası: *"birincil katkı tek bir T1DM ebeveynlik-farkı
   değil; hangi informant / hangi boyut / hangi deneyim düzleminde ayrışmanın
   gerçekleştiğinin haritalanması."*

## 5. Literatür Motoru (küme başına D0–D6, narratif derin-lit)

`literatur-kanit-evidentia.md` §0.3 kaskadı; **minerva-openathens-annas + anamnesis tam kapasite**:

```
D0  Kapsam ayrıştırma (PICO facet) + connector preflight (.claude/evidentia.local.md known_connected)
D1  Bibliyografik geniş tarama: pubmed-epmc, openalex, semantic-scholar (+ EPMC AFF:"Turkey")
D2  Semantik genişletme: minerva_literature_search
      (⚠ EN→hybrid/HyDE; TR→mode:semantic ZORUNLU), OpenAlex citation graph, evidentia-kb kb_search
D3* Relevance rerank + AFF/TR transferability curation (narratif mod: SR eleme-kapısı YOK)
D4  TAM METİN (annas'tan ÖNCE kurumsal bant):
      minerva_literature_fulltext_by_doi / minerva_rominedb_* → openathens (oa_fetch_fulltext)
      → annas-reader (hedefli çıkarım) → hepsi anamnesis.ingest_document
D5  Çapraz-doğrulama: claim-level XVAL (kritik iddiada ≥2 bağımsız / otoriter kaynak)
D6  anamnesis hybrid_query (çok-sorgulu) → damıtılmış, provenans-damgalı kanıt paketi
```

**KVKK guard'ı (ihlal edilemez):** connector'lara **yalnız literatür terimleri** gider;
katılımcı/ham/aile-düzeyi/transkript verisi asla. Nitel kanıt yalnız kanonik nitel sonuç
kaynağından: birincil `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd`
(tek kanonik temsil), gerekirse mekanik kopyası `niteliksel/qualitative_canonical_results_report.md`;
ham transkript / demografi satırı default değil.

**Tam-metin telif kapısı:** hedefli çıkarım; uzun verbatim / toptan çoğaltma yok (G-COPYRIGHT).

## 6. Kanıt Matrisi (kalıcı ara-artefakt)

`tez-yazim/02_kanit-haritalari/tartisma-kanit-matrisi.tsv` — küme-etiketli, satır başına
bir dış-literatür iddiası:

| alan | içerik |
|---|---|
| `kume` | C1–C8 |
| `claim` | tartışmada kullanılacak dış-literatür iddiası (TR) |
| `source_ids` | DOI / PMID / OpenAlex-ID |
| `bib_key` | `references.bib` @key (varsa) / yeni-aday |
| `bulgu_ankraj` | iç bulgu bağı (CSR#anchor / apa_tXX) |
| `population_fit` / `measurement_fit` | direct / partial / indirect + transfer notu |
| `fulltext_locator` | tam-metin route + sayfa/tablo (sayısal endpoint) |
| `iliski` | benzer / farklı / boşluk-doldurur |
| `confidence` | high / moderate / low |

Bu matris hem taslağı besler hem G-XVAL / G-BIB / G-RAG kapılarının kanıtıdır.

## 7. Referans Kapısı (Faz-C, taslak sonrası, toplu)

```
1. python3 scripts/util/bib_hygiene.py all   → ön-mutabakat (atıflı-tanımsız/alan/DOI/dup)
2. /referans-kapisi TOPLU                     → tüm yeni @key: DOI→tam-metin→Zotero(9ZFDHMZA)
                                                 →claim→iki-kol AI-reliability
3. references.bib + referans-denetim-ledgeri  → cite-ok işaretleme; zotero-refs koleksiyon senkron
```
Kapı kapanana dek atıflar taslakta **aday** (`<!-- cand -->`) işaretli.

## 8. Bilimsel Denetim + Kapı 0–5

```
sci-audit: A (uydurma/yanlış-atıf) · B (kaynaksız iddia) · C (istatistik — "bulgu tekrarı yok"
           kontrolü) · F (AI şeffaflık) · G (Türkçe bilimsel dil: edilgen 3.tekil, ondalık virgül)
Kapı 0 kapsam · 1 kanıt · 2 atıf · 3 nedensellik-sınırı · 4 karma-etiket · 5 finalizasyon
```
**Bağlayıcı yorum-kapıları (brief §2/§6):** bulgu/istatistik tekrarı YOK · nedensellik dili
YOK · nitel tema ≠ etki kanıtı · keşfisel ≠ doğrulanmış · öneriler amaç-bulgu sınırlı ·
alt başlık YOK.

## 9. Kademeli Yürütme (ultracode → Workflow fan-out; review checkpoint'leri)

```
Aşama 1  Faz-A fan-out (8 küme paralel) → her küme D0–D6, ana pencereye YALNIZ kanıt matrisi
         satırları döner (retrieve-don't-dump)                     → ⏸ KULLANICI İNCELE (matris)
Aşama 2  Çapraz kaynak-dedup + iddia-uzlaştırma → matris kilitlenir
Aşama 3  Faz-B taslak (akıcı Marmara M1–M11, aday-atıflı)          → ⏸ KULLANICI İNCELE (taslak)
Aşama 4  Faz-C bib_hygiene → /referans-kapisi toplu → sci-audit A–G → Kapı 0–5 → sertifika
```

Fan-out alt-ajanları KVKK guard'ına tabidir; nitel/karma kümeler (C5/C6) yalnız
de-identified kanonik nitel sonuç kaynağından (`niteliksel_kanonik_sonuclar.qmd`) besler.

## 10. Deliverables

- Yeniden yazılmış akıcı `chapters/05_tartisma_ve_sonuc.qmd` (alt başlıksız; düzinelerce
  tam-metin-doğrulanmış atıf; karma bütünleştirme; özgün-değer omurgası).
- `tez-yazim/02_kanit-haritalari/tartisma-kanit-matrisi.tsv` (kalıcı kanıt matrisi).
- `references.bib` + `referans-denetim-ledgeri.md` güncel (cite-ok).
- Sertifikalar: `/referans-kapisi`, `sci-audit` raporu, `tez-yazim/04_kalite-kontrol/sertifikalar/05-tartisma-ve-sonuc-sertifika-2026-07-13.md` (Kapı 0–5).

## 11. Başarı Kriterleri

- [ ] Her H1–H5 için destek durumu AÇIK + en geniş literatürle benzer/farklı yön + olası neden.
- [ ] Her netice (birincil + keşfisel + nitel) dört-soru çerçevesiyle (anlam/literatür/boşluk/gelecek) tartışıldı.
- [ ] Özgün değer (informant×boyut×deneyim ayrışma haritalaması) M3+M5'te açık.
- [ ] Karma bütünleştirme joint display etiketiyle; ayrışma teorik okundu, hata sayılmadı.
- [ ] Marmara §3.7: alt başlık yok, bulgu/istatistik tekrarı yok, nedensellik sınırı korundu.
- [ ] Tüm dış atıflar toplu `/referans-kapisi` cite-ok; bib_hygiene exit 0.
- [ ] sci-audit A–G blocker'sız; Kapı 0–5 + açık kullanıcı onayı.
- [ ] `quarto render` bölüm-izole hatasız.
