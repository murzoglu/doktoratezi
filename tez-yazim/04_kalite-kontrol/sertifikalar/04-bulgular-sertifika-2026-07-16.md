# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 04 — BULGULAR |
| Bölüm başlığı | BULGULAR |
| Üretim dosyası | `chapters/04_bulgular.qmd` (973 satır) |
| Sertifikasyon tarihi | 2026-07-16 |
| Strictness | `certification` |
| Önceki sertifika | `04-bulgular-sertifika-2026-07-14.md` (`certified-final`) |
| Yeniden sertifikasyon nedeni | Bölüm bu oturumda iki-kol denetim (Opus 4.8 öz-denetim + Galileo/GPT-5.4 AI-hakem) sonrası 4 bulguyla düzenlendi: keşifsel-katman kapsam cümlesi, iki "120 spesifikasyon" geçişinin H1-EMBU-C/H3-EMBU-P etiketlenmesi, 8 ana hipotez figürü, sentez tablosu iç-kaynak yorumlarının doğrulanması. |
| Sertifikasyonu uygulayan | Ona (Claude Opus 4.8) — Kapı 0–5 yeniden denetimi |
| Uygulama onayı | **Kullanıcı açık onayı ("evet", 2026-07-16)** — `provisional-pass` → `certified-final` |

## Bu Oturumdaki Değişiklik Envanteri

`chapters/04_bulgular.qmd` üzerinde (git diff: +70/−5 satır):

1. **Bulgu 1 (major) — Keşifsel katman kapsamı (§421):** Raporlanmayan üç
   keşifsel Faz II analizi (FSM, ölçüm-değişmezliği/seçim-geçerliği,
   veri-güdümlü nedensel keşif [PC/FCI] yapı doğrulaması) için bölüm kapsamını
   netleştiren cümle eklendi — bu analizlerin çevrimiçi ek materyalde
   raporlandığı belirtildi (keşifsel bulgular öneri düzeyine çıkarılmaz notuyla).
2. **Bulgu 2 (minor) — "120 spesifikasyon" muğlaklığı:** İki çoklu-evren geçişi
   etiketlendi — biri H1 çocuk-algısı (EMBU-C) sonucuna (%75 anlamlı), diğeri
   H3 anne öz-bildirimi (EMBU-P) grup etkisine (%0 anlamlı) bağlandı.
3. **Bulgu 3 (minor) — Ana hipotez figürleri:** Tablo-öncelikli ilkeyle uyumlu
   olarak 8 birincil hipotez figürü ilgili tablolarından sonra yerleştirildi:
   `fig-smd-love` (fig-03), `fig-h1-forest` (fig-07), `fig-h2-apim` (fig-09),
   `fig-h3-stratified` (fig-10), `fig-h4-sem` (fig-11), `fig-mediation` (fig-14,
   [KEŞİFSEL]), `fig-bayesian-forest` (fig-24), `fig-bayesian-diagnostics`
   (fig-25). Her biri: carbon/primary SVG mevcut, tanım=1/atıf=1 dengeli.
4. **Bulgu 4 (bilgi) — Sentez tablosu iç-kaynak yorumları:** Sentez/joint-display
   tablosundaki 8 `<!-- kaynak: -->` yorumunun tümü doğrulandı — 6 CSR çapa
   (`#h1..h5-karar`, `#sec-genel-hipotez-ozet`), 6 nitel tema çapa
   (`#tema-1..4`, `#sec-capraz`) ve 2 Faz5/Faz6 SAP plan dosyası hedefe çözülüyor.

Sınır: Ham veri / transcript / demografi satırı / credential sertifikaya
**taşınmadı**; yalnız aggregate + anonim quote-ID bağlama alındı.

## Kapı 0: Kapsam ve Gizlilik — PASS

- [x] Bölüm dosyası + önceki sertifika + iki-kol denetim bulguları okundu.
- [x] Değişiklik envanteri git diff ile çıkarıldı (yukarıda).
- [x] Gizlilik sınırı korundu (satır-düzeyi veri/PII taşınmadı).

## Kapı 1: Derin Literatür ve İddia Haritası — PASS

- Findings **yorumsuz**; dış-literatür yalnız metot-çapası (substantif literatür
  Tartışma'da); repo-içi iddialar CSR/SAP/protokol/nitel-rapora izli.
- Bu oturumun düzenlemeleri **yeni dış atıf eklemedi**; eklenen içerik figür
  çağrıları, geçiş etiketleri ve kapsam cümlesidir.
- `bib_hygiene reconcile` (04): **HARD undefined = 0** (render kırılmaz).

Kapı 1 kararı: **PASS**

## Kapı 2: Full-Text, DOI ve Ledger Mutabakatı — PASS

- Bu oturumda yeni referans eklenmedi; metot-çapaları önceki sertifikada
  (`04-...-2026-07-14.md`) `cite-ok (identity-doğrulamalı)` olarak kapatılmıştı.
- **Sentez tablosu iç-kaynak doğrulaması (Bulgu 4):** 8 `<!-- kaynak: -->`
  yorumunun hedefleri birinci-elden doğrulandı:
  - CSR çapaları: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd#{h1,h2,h3,h4,h5}-karar`,
    `#sec-genel-hipotez-ozet` — 6/6 mevcut.
  - Nitel çapalar: `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#{tema-1,tema-2,tema-3,tema-4,sec-capraz}` — 6/6 mevcut.
  - SAP planları: `docs/analiz_planlari/08-sap-faz5-ek-plan.md`,
    `09-sap-faz6-ek-plan.md` — 2/2 mevcut.

Kapı 2 kararı: **PASS**

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu — PASS

- [x] **8 yeni figür çift-sunum kuralına uygun:** her figür ilgili tablosundan
  sonra, tanım (`{#fig-... }`) + metin-içi `@fig-...` atfı ile (tanım=1/atıf=1,
  8/8). `fig-mediation` doğru şekilde [KEŞİFSEL] etiketli.
- [x] **Figür yolları çözünüyor:** izole pandoc render'da 8 SVG
  `docs/assets/figures/carbon/primary/` altından `<img>` olarak gömüldü.
- [x] **Ondalık virgül** korundu; eklenen satırlarda İngilizce ondalık yok
  (fig numaraları fig-03/07/09/… dosya adı, ondalık istatistik değil).
- [x] H1–H5 ↔ keşifsel ↔ nitel ↔ karma katman ayrımı korundu; "120
  spesifikasyon" muğlaklığı H1-EMBU-C / H3-EMBU-P olarak netleştirildi.
- [x] Sentez tablosu iç-kaynak yorumları geçerli hedeflere işaret ediyor.

Kapı 3 kararı: **PASS**

## Kapı 4: Türkçe İmla, Akış ve Mantık — PASS

`tr_corpus_audit all --fail-on blocker` (04):

- **exit 0 — BLOCKER = 0** (yalnız H-* advisory: `H-ABBR-UNUSED` tek-dosya
  artefaktı, `H-TRANS`/`H-INFO` §3.6 yorumsuz-sunum beklentisi — kasıtlı).
- **Galileo coherence (8 figür akışı bozdu mu):** mean_adjacent_sim **0,731**
  (baseline 0,729), flow_breaks **[]**, redundant_pairs **[]**, 117 paragraf —
  figür eklemeleri akış sürekliliğini bozmadı.

Kapı 4 kararı: **PASS**

## Kapı 5: AI-Reliability ve Teknik Doğrulama — PASS

| Kontrol | Sonuç |
|---|---|
| `bib_hygiene reconcile` (04) | HARD=0 (render kırılmaz); exit 2 = yalnız baseline SOFT (`simonsohn2015specification` alan, `sumer2010` DOI — bu oturumda dokunulmadı; git diff ile kanıtlandı) |
| `tr_corpus_audit --fail-on blocker` (04) | **exit 0 — 0 blocker** |
| Galileo coherence | mean_adjacent_sim 0,731 / flow_breaks 0 / redundant_pairs 0 |
| İzole pandoc render (`--citeproc`, marmara-ama11.csl) | **exit 0 — 95 KB**; 8 figür `<img>` gömüldü, SVG yolları çözüldü; crossref-dışı ciddi uyarı yok (yalnız `fig-/tbl-/sec-` önek uyarıları, tam-tez render'ında çözülür) |
| `git diff --check` | **temiz** |

**AI-hakem (Galileo/GPT-5.4) delili (bu oturum):** H1 pasajı gerçek CSR
kanıt-bağlamıyla yeniden yargılandığında groundedness 0,28→0,84,
citation_support na→supported, hallucination_risk 0,72→0,22 — ilk düşük skorun
kanıt-bağlam artefaktı olduğu kanıtlandı.

Kapı 5 kararı: **PASS**

## Nihai Sertifika Kararı

| Kapı | Karar |
|---|---|
| Kapı 0 | PASS |
| Kapı 1 | PASS (yeni dış atıf yok; HARD=0) |
| Kapı 2 | PASS (8 iç-kaynak yorumu 14/14 hedefe çözüldü) |
| Kapı 3 | PASS (8 figür çift-sunum + yol çözünürlüğü) |
| Kapı 4 | PASS (0 blocker; coherence korundu) |
| Kapı 5 | PASS (render exit 0; git diff temiz) |
| **Nihai durum** | **`certified-final`** |

**Karar gerekçesi:** İki-kol denetimden çıkan dört bulgu uygulandı; tüm teknik
kapılar (0–5) bu oturumun güncel metniyle yeniden çalıştırıldı ve PASS verdi.
Düzenlemeler yeni major/blocker üretmedi (HARD=0, blocker=0, coherence
0,729→0,731). Kullanıcı bu yeniden-doğrulanmış metni **açık onayla ("evet",
2026-07-16)** onayladığından durum `certified-final`'a yükseltilmiştir.
