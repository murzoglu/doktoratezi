# sci-audit 7-Eksen Manüskript Denetimi — GİRİŞ ve AMAÇ

- **Bölüm:** `chapters/01_giris_ve_amac.qmd` (21 satır, 7 paragraf gövde)
- **Denetim tarihi:** 2026-07-12
- **Strictness:** `certification`
- **Plugin:** sci-audit v0.2.1 (cureonics-marketplace), `hooks_enabled:false` (skill/komutlar normal çalışır)
- **Faz:** 3.6 (manüskript adli denetimi) — Faz 3 raporlama sonrası, kapanış öncesi
- **Kapsam:** Bu tur, ledger `zotero-ok` durumundaki iki yeni referansın (eckshtain2010, butner2009) eklendiği ve P4/P6 korelasyon dili düzenlemelerinin yapıldığı düzeltmeleri denetler.

## Özet Karar

| Eksen | Araç | error | warning | info | Sonuç |
|---|---|---:|---:|---:|---|
| A — Referans bütünlüğü | manuel + bib | 0 | 0 | 0 | ✅ PASS |
| B — Claim grounding | `claim_grounding.py` | 1* | 0 | 0 | ⚠️ false-positive (aşağıda) |
| C — İstatistik tutarlılık | `stats_forensics.py` | 0 | 0 | 0 | ✅ PASS |
| D — Halüsinasyon sinyalleri | `hallucination_signals.py` | 0 | 0 | 0 | ✅ PASS |
| E — Rehber uyumu (prescan) | `guideline_prescan.py` | 0 | 0 | 0 | ✅ PASS (bölüm-düzeyi) |
| F — AI şeffaflık | `ai_transparency.py` | 0 | 0 | 1 | ✅ PASS (bölüm-düzeyi info) |
| G — Türkçe yazım | `tr_sciaudit.py` | 0 | 7 | 1 | ✅ PASS (0 blocker) |

**Kabul (bridge doc §2 step 10):** Gerçek `error`/`blocker` = **0**. Axis B'deki tek "error" araç false-positive'idir (kanıt aşağıda); bölümde 16 nicel/olgusal iddianın tamamı kaynak taşır. **Bu tur temiz.**

> Davranış kuralı 21 gereği "certified-final" ilan EDİLMEZ; cite-ok kapanışı `/bolum-sertifika` iki-kol AI-reliability + tam sertifikasyon turunda tamamlanır.

---

## Eksen ayrıntıları

### A — Referans bütünlüğü (yanlış-atıf düzeltmesi doğrulandı)

Kullanıcının adversaryal doğrulama turunda yakaladığı yanlış-atıf düzeltmesi kanonik künyelerle **tam tutarlı**:

- **`butler2009` hem metinden hem `references.bib`'den tamamen kaldırılmış** (grep 0/0). Taslaktaki bu anahtar hatalıydı.
- **`eckshtain2010parentDepression`** — Eckshtain D (ilk yazar), 2010, *J Pediatr Psychol* 35(4):426-435, DOI `10.1093/jpepsy/jsp068`, **PMID 19710249**, PMCID PMC2902839. Yanlış "butler2009" bununla değiştirilmiş; P4'te doğru atıf.
- **`butner2009discrepancy`** — yazar listesinde **"Butler, Jorie M." 4. yazar** olarak yer alıyor; yani "Butler JM" ayrı bir kaynak değil, bu makalenin ortak yazarıydı. Künye DOI `10.1037/a0015363`, PMID 19413435, PMCID PMC2805180 ile tam. P6'da doğru atıf.

### B — Claim grounding (1 error = Pandoc `[@key]` false-positive)

Araç 1 `unsourced-claim` error verdi: satır 3 IDF Atlası cümlesi (`108.300`/`149.500`).

**Bu bir false-positive'dir.** Kök neden: aracın `SOURCE_MARKER` regex'i Pandoc author-year atıf sözdizimini (`[@key]`) tanımıyor — yalnız `[123]`, `(2021)`, DOI/PMID/URL, dosya yolu tanıyor. İlgili cümle `[@ogle2022idfAtlas]` kaynağını taşır.

**Kanıt:** `[@key]` → araç-tanır `(2021)` ile geçici değiştirilip yeniden çalıştırıldığında **error 0, claims_total 16, grounding_rate 1.0** — bölümdeki 16 nicel/olgusal iddianın tamamı kaynaklı. Metin hatası yok; bu, deterministik grounding-floor'un Quarto uyumsuzluğudur (gerçek kanıt eşleştirmesi `claim-extractor`+`claim-refuter` alt-ajanlarıyla yapılır).

### C — İstatistik tutarlılık (sayısız korelasyon dili doğrulandı)

`statcheck / GRIM / GRIMMER / SPRITE / CI / percentage / subgroup / effect-size` — **hepsi 0 bulgu**. Kullanıcının eklediği P4/P6 cümleleri makine-okunur inline istatistik içermiyor ("korelasyon dili, sayı yok" iddiası kanıtlandı).

### D — Halüsinasyon sinyalleri

0/0/0. Aşırı-kesinlik dili, atıfsız yöntem adı, bozuk ISBN/ORCID sağlaması vb. sinyal yok.

### E — Rehber uyumu (prescan)

Bölüm-düzeyi: yalnız `introduction` present (beklenen — tek bölüm). Tam JARS-Mixed/STROBE/COREQ item-item kontrolü tez montajında `/sci-audit:guideline-check` ile yapılır.

### F — AI şeffaflık

0 error, 1 info: bölüm düzeyinde AI-kullanım beyanı yok. Bu beklenen — beyan bölüm başında değil, tez düzeyinde (ICMJE/COPE/WAME) ele alınır.

### G — Türkçe yazım (0 blocker)

0 blocker / 7 warning / 1 info (resmi rapor: `01_giris_ve_amac-tr-sciaudit.md`). **Eklenen P4/P6 cümleleri (satır 9, 13) hiç uyarı almadı — temiz.** Uyarıların tümü mevcut metinden:

- 4× `sentence-long` (satır 7, 11, 17, 21) — uzun ama kaynaklı akademik cümleler; anlam bozukluğu değil.
- 1× `readability-very-hard` (Ateşman 3.03) — bilimsel yoğunluk gereği; kabul edilebilir.
- 2× `decimal-dot` (`108.300`, `149.500`) — **false-positive**: bunlar Türkçe binlik ayracı (tam sayı), ondalık değil. Araç binlik/ondalık ayracını ayırt edemiyor.
- 1× info `abbreviation-review` (IDF) — IDF ilk kullanımda açık: "Uluslararası Diyabet Federasyonu (*International Diabetes Federation*, IDF)". Uyumlu.

> Not: G5 (Türkçe metinde İngilizce ondalık nokta `p`) blocker'ı YOK — bölümde `p` değeri yok.

---

## Galileo çapraz kontrol (advisory, sci-audit'in yanında)

- `galileo_heading_cascade`: **pass** (0 error/0 warning, 1 başlık — Marmara §1.3 uyumlu).
- `galileo_reference_prose`: atıf yoğunluğu 13,0/1k kelime (17 atıf, 20 uniq anahtar) — sağlıklı; tek advisory bulgu `reporting_verb_monotony` (üslup; blocker değil).

## Kalan adım (cite-ok kapanışı)

İki yeni referans hâlâ `zotero-ok`. `certified-final` için bölüm kapanışında `/bolum-sertifika` çalıştırılmalı → iki-kol AI-reliability (`/tez-dogrulama` + `t1dm-qual-ai-audit`) + tam 7-eksen sci-audit → ledger `cite-ok`.
