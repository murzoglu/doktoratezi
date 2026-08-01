# İki-Kol Karma Sentez Hazırlık Katmanı — Tasarım

**Tarih:** 2026-07-11
**Durum:** Onaylandı (kullanıcı: "uygun", 2026-07-11)
**Kol:** Karma (nicel + nitel entegrasyon)

## 1. Amaç

Tez yazım motoru, iki kanonik sonuç dosyasını **tek doğruluk kaynağı** alarak
izlenebilir joint-display + çapraz-kol meta-çıkarım üretebilsin ve tezin iki
kolunu en ideal biçimde birleştirebilsin.

**Kanonik girdiler (kullanıcı beyanı, 2026-07-11):**

| Kol | Dosya |
|---|---|
| Nicel | `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` |
| Nitel | `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` |

Bu iki dosya, karma sentezin baz aldığı sonuç kaynağıdır. Üretim tez metni ise
`chapters/04_bulgular.qmd` + `chapters/05_tartisma_ve_sonuc.qmd` dosyalarında
bu iki kaynaktan **yazılır**.

## 2. Sorun / mevcut durum

Keşifte saptanan boşluklar:

- **Nicel CSR nitel kola hiç değinmiyor.** CSR §17.1 / §17.9 "üç bilgi kaynağı /
  üç-informant asimetrisi" = üç *nicel* informant (anne/çocuk/kardeş); nitel kol
  değil. Nicel kol tamamen kendi içinde kapalı
  (`docs/CLINICAL-STUDY-REPORT-FINAL.qmd`, `nitel|qualitative|karma` grep = 0).
- **İki drift'e açık tablo var:** nitel dosyadaki `# Karma Tez Entegrasyonu`
  (`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd:476-497`) +
  `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md` iskeleti.
- **Mevcut plan çifte-bayat:** `nitel-nicel-joint-display-plan.md` eski kaynak
  `niteliksel/qualitative_canonical_results_report.md` (Markdown öncül) ve **var
  olmayan** `chapters/03_bulgular.qmd`'e işaret ediyor (gerçek dosyalar
  `chapters/04_bulgular.qmd` + `chapters/05_tartisma_ve_sonuc.qmd`).
- **Doldurulmuş, iki kanonik dosyaya izlenebilir tek joint-display + meta-çıkarım
  katmanı yok.**

## 3. Kanonik analitik çerçeve (değişmez — yeniden tartışılmaz)

Repo'da hâlihazırda kanonik (bkz. `tez-yazim/05_entegrasyon/README.md` §çekirdek,
`00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §6,
`.claude/skills/t1dm-tez-rehberi/references/karma-yontem.md`):

- **Convergent-parallel karma yöntem.** İki kol ayrı kanıt türüdür.
- Nitel tema nicel etki tahmini, nicel sonuç nitel temanın nedensel/mekanistik
  kanıtı **yapılmaz**.
- Nicel = *hangi boyut / ne kadar*; nitel = *neden / nasıl*.
- İlişki-türü sözlüğü: **uyum · tamamlayıcılık · ayrışma · açıklayıcı-genişleme**.

## 4. Kararlar (brainstorming forkları, 2026-07-11)

| Fork | Karar |
|---|---|
| Merkez çıktı | **Bütünsel katman** (doktrin + ledger + doldurulmuş joint-display + meta-çıkarım) |
| Yuva + drift | **Ayrı ledger + sentez belgesi**, ikisi `tez-yazim/05_entegrasyon/`; nitel tablo + iskele → pointer |
| Provenans/drift | **Ankraj-tabanlı pointer + drift-guard testi** (stdlib checker) |
| Kapsam | **Hazırlık + üretim bölümü taslağı** (04/05'e provisional taslak, Kapı 0-5 atlanmaz) |
| Ledger formatı | **TSV** (deterministik parse; `kritik-dosya-manifesti.tsv` idiomu) |

## 5. Mimari — bileşenler

### Bileşen 1 — Stabil ankrajlar (iki kanonik dosya)

Ankrajlanacak birleşme birimleri (tümü şu an ID'siz — doğrulandı):

**Nitel** (`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd`):

| Başlık | Satır | Eklenecek ankraj |
|---|---|---|
| `## Tema 1 — Sağlıklı Kardeşin Görünmeyen Yükü` | 343 | `{#tema-1}` |
| `## Tema 2 — Annenin Tıbbi Bakıcı Rolüne Kayması` | 369 | `{#tema-2}` |
| `## Tema 3 — T1DM Tanılı Çocuğun İçeriden Deneyimi` | 395 | `{#tema-3}` |
| `## Tema 4 — Aynı Evde Üç Farklı Deneyim` | 418 | `{#tema-4}` |

(Üst-bölümler `{#sec-capraz}`, `{#sec-karma}` zaten mevcut — yeniden eklenmez.)

**Nicel** (`docs/CLINICAL-STUDY-REPORT-FINAL.qmd`):

| Başlık | Satır | Eklenecek ankraj |
|---|---|---|
| `### 11.1.5 H1 Karar Kutusu` | 1682 | `{#h1-karar}` |
| `### 11.2.4 H2 Karar Kutusu` | 1762 | `{#h2-karar}` |
| `### 11.3.6 H3 Karar Kutusu` | 1856 | `{#h3-karar}` |
| `### 11.4.4 H4 Karar Kutusu` | 1919 | `{#h4-karar}` |
| `### 11.5.8 H5 Karar Kutusu` | 2008 | `{#h5-karar}` |
| `## 2.3 Sonuçların Yönetici Özeti` | 1049 | `{#sec-sinopsis-verdikt}` |
| `## 19.2 Hipotez Düzeyinde Özet Çıkarımlar` | 4390 | `{#sec-genel-hipotez-ozet}` |

Ankrajlar Quarto cross-ref sözdizimidir (`## Başlık {#id}`); render'a zararsız.

> **Not (uncommitted dosya):** `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` şu an
> working-tree'de kullanıcının commit'lenmemiş dosyasıdır. Ankraj eklemek ona
> dokunur; kullanıcının bu isteği (motoru bu dosyaya dayandır) bu edit'i
> yetkilendirir. Değişiklik yalnız başlık satırlarına `{#id}` ekler.

### Bileşen 2 — Yapılandırılmış kanıt-ledger

**Dosya:** `tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv`

Sekme-ayraçlı; başlık satırı + veri satırları. Sütunlar:

```
id	odak	nicel_verdikt_ozet	nicel_ankraj	nitel_oruntu_ozet	nitel_ankraj	iliski_turu	karma_yorum_siniri
```

- `nicel_ankraj` / `nitel_ankraj` = `dosya#ankraj` (ör.
  `docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h1-karar`).
- `*_ozet` = kaynaktan **kısa verbatim** verdikt/örüntü alıntısı (drift sentineli;
  6-14 kelime, tam metin değil).
- `iliski_turu` ∈ {`uyum`, `tamamlayıcılık`, `ayrışma`, `açıklayıcı-genişleme`}.
- `karma_yorum_siniri` = kol-aşırı yorum sınırı (nedensellik yok vb.).

**Satır kapsamı** (kaynak: nitel dosya joint-display tablosu
`…qmd:484-490` + `# Çapraz Bilimsel Neticeler` `…qmd:446-459` + CSR §17.9
`docs/CLINICAL-STUDY-REPORT-FINAL.qmd:4335`):

| id | odak | nicel ankraj | nitel ankraj |
|---|---|---|---|
| `h1-cocuk` | H1 çocuk algısı (EMBU-C) | `#h1-karar` | `#tema-3` |
| `h2-kardes` | H2 kardeş ilişkisi (KİA) | `#h2-karar` | `#tema-1` (+ Tema 4) |
| `h3-anne` | H3 anne öz-rapor (EMBU-P) | `#h3-karar` | `#tema-2` |
| `h4-beck` | H4 Beck → EMBU-P (SEM) | `#h4-karar` | `#tema-2` |
| `h5-diadik` | H5 diadik tutarlılık | `#h5-karar` | `#tema-4` |
| `meta-triad` | Triadik informant asimetrisi | `#sec-genel-hipotez-ozet` | `#sec-capraz` |

Kesin satır sayısı ve alıntı metinleri, ledger yazımında **kaynaktan** sabitlenir
(tahmini değil). Nitel dosya H2'yi Tema 1 **ve** Tema 4'e bağladığından
(`…qmd:487`), gerekirse ayrı satır (`h2-kardes-a`, `h2-kardes-b`) açılır.

### Bileşen 3 — Doldurulmuş sentez belgesi

**Dosya:** `tez-yazim/05_entegrasyon/karma-sentez-kanonik.md`

Prose, kanonik. Bölümler:

- **§0** Otorite zinciri + KVKK sınırı + kanonik-girdi beyanı (iki dosya).
- **§1** Joint-display (ledger'dan türetilmiş, **yorumsuz**, BULGULAR-hazır
  yan-yana tablo: odak · nicel verdikt · nitel örüntü · ilişki türü · yorum
  sınırı; her hücre ankraj-provenanslı).
- **§2** İlişki-türü gerekçelendirmesi (her satır için neden uyum/tamamlayıcılık/
  ayrışma/açıklayıcı-genişleme).
- **§3** Çapraz-kol meta-çıkarımlar (tek kolun tek başına vermediği sonuçlar;
  ör. H5 ön-kayıtlı triangülasyon-şartı-karşılanmadı [CSR `#h5-karar`] + Tema 4
  triadik-farklılık [nitel `#tema-4`] → anne↔çocuk algı ayrışması ölçüm hatası
  değil, rol-temelli deneyim farkı: nicel *büyüklük*, nitel *neden/nasıl*).
- **§4** TARTIŞMA köprü cümleleri (05'e enjekte edilecek taslak).
- **§5** Karma-özel sınırlılık (paralel örneklem farkı: nicel 241 aile
  [`CLAUDE.md` domain notu] vs nitel 7 aile [`niteliksel/CLAUDE.md`]; iki kol
  aynı bireyleri örneklemez → birleştirme yorum düzeyinde, istatistiksel
  genelleme değil).

### Bileşen 4 — Drift-guard checker

**Dosya:** `scripts/util/karma_ledger_check.py` (stdlib, bağımlılıksız)
**Test:** `tests/test_karma_ledger_check.py` (stdlib `unittest`, repo idiomu —
bkz. `tests/test_bib_hygiene.py`, `tests/test_zotero_bridge_parity.py`)

Davranış:
1. Ledger TSV'yi parse eder (başlık + satırlar; sütun sayısı doğrulaması).
2. Her satırın `nicel_ankraj` + `nitel_ankraj` alanından `dosya#ankraj` ayrıştırır.
3. Her ankraj için:
   - (a) `dosya` içinde `{#ankraj}` **var mı** → yoksa **HARD**.
   - (b) İlgili `*_ozet` verbatim alıntısı `dosya` içinde **geçiyor mu** →
     geçmiyorsa **SOFT** (kaynak değişti, ledger bayat).
4. `iliski_turu` sözlükte mi (uyum/tamamlayıcılık/ayrışma/açıklayıcı-genişleme) →
   değilse **SOFT**.

CLI: `python3 scripts/util/karma_ledger_check.py [--ledger PATH] [--json]`.
Exit kodları: **0** temiz · **1** HARD (kırık provenans) · **2** SOFT (drift/bayat).
Rapor: konsol özet (+ `--json` makine-okur). `_severity`/`_render_report`
deseni `bib_hygiene.py`'den ödünç.

KVKK: checker yalnız iki manuskript-düzeyi `.qmd` + ledger TSV'yi okur;
`data/*`/`outputs/*`/`_targets/*` **okumaz** (zaten `permissions.deny` kapsar).

### Bileşen 5 — Yönetişim bağlantısı

| Dosya | Değişiklik |
|---|---|
| `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md` | Bayat kaynakları düzelt (→ iki kanonik dosya; `chapters/03_bulgular.qmd` → `04_bulgular.qmd` + `05_tartisma_ve_sonuc.qmd`); iskelet tabloyu `karma-sentez-kanonik.md`'e pointer'a düşür; joint-display **alan sözlüğü** olarak kalır |
| `tez-yazim/05_entegrasyon/README.md` | Tek-otorite haritasına `karma-kanit-ledgeri.tsv` + `karma-sentez-kanonik.md` ekle; üretim zincirini iki kanonik dosyaya göre güncelle |
| `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` | `# Karma Tez Entegrasyonu` başına pointer notu ("kanonik karma sentez = `tez-yazim/05_entegrasyon/karma-sentez-kanonik.md`"); mevcut tablo içerik olarak kalır + Tema ankrajları (Bileşen 1) |
| `.claude/skills/t1dm-tez-rehberi/references/karma-yontem.md` | "Kanonik girdi + hazırlık katmanı" bölümü: iki dosya + ledger + sentez belgesi + checker akışı |
| `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | BULGULAR/TARTIŞMA sertifikasyonuna `karma_ledger_check.py` HARD=0 kapısı |

### Bileşen 6 — Üretim bölümü taslak enjeksiyonu

| Dosya | Enjeksiyon |
|---|---|
| `chapters/04_bulgular.qmd` | Joint-display tablosu (yorumsuz), `<!-- TASLAK / provisional-pass — kaynak: tez-yazim/05_entegrasyon/karma-sentez-kanonik.md -->` işaretli |
| `chapters/05_tartisma_ve_sonuc.qmd` | Meta-çıkarım köprü paragrafları (yorumlu), aynı işaret |

Kurallar: kol-aşırı nedensel dil yok · ondalık **virgül** (`p<0,001`) · metin-içi
atıf yazar-yıl "ve"/"ve ark." (AMA-11) · her sayı ankraj-provenanslı · **Kapı 0-5
atlanmaz** — enjeksiyon `provisional-pass` işaretlidir, final değildir.

## 6. Veri akışı

```
iki kanonik .qmd (+ Bileşen 1 ankraj)
        │
        ▼
karma-kanit-ledgeri.tsv  ──►  karma_ledger_check.py (guard: HARD/SOFT)
        │
        ▼
karma-sentez-kanonik.md  (§1 joint-display · §2 ilişki türü · §3 meta-çıkarım · §4 köprü · §5 sınırlılık)
        │
        ▼
04_bulgular.qmd (joint-display TASLAK)  +  05_tartisma_ve_sonuc.qmd (meta-çıkarım TASLAK)
```

Drift olduğunda checker SOFT/HARD verir → ledger + sentez belgesi güncellenir →
taslaklar yeniden türetilir.

## 7. Kısıtlar

- **KVKK:** yalnız iki manuskript-düzeyi dosya + türev katman. Ham
  görüşme/`data/*`/aile-düzeyi satır **girmez**; agregat verdikt + de-identified
  tema/örüntü + ankraj-provenans.
- **Kaynaksız-sayı Stop kapısı:** sentez belgesi + taslaklardaki her nicel değer
  ankraj-provenanslı (dosya#ankraj) olmalı.
- **Kapı 0-5:** üretim enjeksiyonları `provisional-pass`; sertifikasyon ayrı.
- **Dil:** Türkçe.
- **Ondalık:** virgül.

## 8. Test / doğrulama

- `tests/test_karma_ledger_check.py` — HARD (kayıp ankraj), SOFT (drift alıntı),
  temiz senaryo, TSV parse, ilişki-türü doğrulaması (stdlib unittest).
- Canlı: `python3 scripts/util/karma_ledger_check.py` → gerçek ledger üzerinde
  HARD=0.
- Hook regresyonu: `tests/test_claude_hooks.py` (bileşen değişikliği hook
  politikasına dokunmuyorsa etkilenmez; yine de koşulur).
- Quarto: iki kanonik `.qmd`'ye ankraj eklendikten sonra render bozulmaz
  (`quarto render` etkilenen dosyalarda — CSR standalone report).

## 9. Kapsam dışı (YAGNI)

- Final BULGULAR/TARTIŞMA prose'unun sertifikalı yazımı (Kapı 0-5 oturumu).
- Otomatik ledger extraction script (fork: reddedildi — prose/R-chunk kırılgan).
- Nitel ham veri / transcript entegrasyonu (KVKK sınırı).
- Nicel CSR'a nitel kol tartışması ekleme (CSR standalone kalır; birleştirme
  tez `chapters/` katmanında olur).

## 10. Dosya envanteri

**Yeni:**
- `tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv`
- `tez-yazim/05_entegrasyon/karma-sentez-kanonik.md`
- `scripts/util/karma_ledger_check.py`
- `tests/test_karma_ledger_check.py`

**Değiştirilen:**
- `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (7 ankraj)
- `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` (4 Tema ankrajı + pointer notu)
- `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md` (re-point + pointer)
- `tez-yazim/05_entegrasyon/README.md` (tek-otorite haritası)
- `.claude/skills/t1dm-tez-rehberi/references/karma-yontem.md` (kanonik girdi bölümü)
- `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` (Kapı adımı)
- `chapters/04_bulgular.qmd` (joint-display taslak)
- `chapters/05_tartisma_ve_sonuc.qmd` (meta-çıkarım taslak)
