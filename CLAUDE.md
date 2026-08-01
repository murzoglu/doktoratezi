# Doktora Tezi — Tip 1 Diyabet & Ebeveynlik Tutumu

Quarto + R doktora tezi: T1DM tanılı çocuklar, sağlıklı kardeşler ve annelerinde EMBU / Beck / KİA ölçek analizleri.

**Tez yazımı zorunlu talimatname:** [`tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md`](tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md) — tez yazım, bölüm, format, referans veya karma sentez içeren her işte bağlayıcıdır.

## Komutlar

```bash
# Tezi render et (chapters/ → outputs/quarto/)
quarto render

# Pipeline (targets) — path/raw manifest + hash kontrollü veri yükleme/skor/SES/eksik veri/Tablo 1/DAG/PS/H1-H5 + KISIM VI-LI (Faz I + Faz II-VI keşifsel/post-hoc) + APA figür+tablo
Rscript -e 'targets::tar_make()'

# EMBU stage runner'ları (sırasıyla)
Rscript scripts/R/01_embu_stage1_standardize.R
Rscript scripts/R/02_embu_stage2_likert4.R
Rscript scripts/R/03_embu_stage3_family.R

# Testler (stopifnot tabanlı, çıktı sessizse PASS)
Rscript tests/test_embu_stage1.R
Rscript tests/test_embu_stage2_likert4.R
Rscript tests/test_embu_stage3_family.R

# Kapsamlı tez kontrol checklisti (8 eksen, 28 madde; salt-okuma orkestratör)
python3 scripts/util/tez_checklist_verify.py --fast       # hızlı ön-uçuş (ağır kontroller SKIP)
python3 scripts/util/tez_checklist_verify.py              # tam denetim (render/PDF/renv/targets dahil)
python3 scripts/util/tez_checklist_verify.py --audit-doc  # belge<->script ID senkronu (yetim=exit 1)

# Ortak yazar DOCX round-trip (repoya erişimi olmayan ortak yazardan online
# "Değişiklikleri İzle" düzeltmesi almak; yalnız pandoc + Python stdlib)
python3 scripts/util/coauthor_docx_roundtrip.py export                    # render docx'i outbox/ altına hazırlar
python3 scripts/util/coauthor_docx_roundtrip.py import --edited inbox/donen.docx  # değişiklik+yorumları .qmd satırına eşleyen rapor üretir

# Paket yönetimi
Rscript -e 'renv::status()'
Rscript -e 'renv::restore()'
```

## Mimari

- `thesis.qmd` — kök Quarto belgesi, `chapters/` ön bölümler (`00a–00c`) + `01–07_*.qmd` bölümlerini include eder (çıktı: `outputs/quarto/`)
- `_targets.R` — `targets` orkestrasyonu. R kütüphanesi **66 modül** (`R/00_paths.R` … `R/65_phase6_developmental_dyadic.R`): hash kontrollü kanonik veri yükleme + türetilmiş skorlar + SES kompozitleri + eksik veri çerçeveleri + Tablo 1/SMD dengesi + Causal DAG + PS/IPTW/Matching + H1-H5 (`R/16-20`) + KISIM VI-XVIII genişletilmiş analizler (`R/21-31`) + **Faz II-VI SAP KISIM XIX-LI [keşifsel · post-hoc]** (`R/32-65`: trifaktör, informant discrepancy, cross-informant network, floor-aware IRT, ESEM, causal mediation, DAG PC/FCI, multiverse, bayesian meta, PDT, sosyal katmanlaşma, maternal komorbidite, aile yapısı, seçim/batch geçerlik, H3 robustluk, artık ilişkiler, gelişimsel diadik). **Kanonik modül/hedef listesi ve faz sınırları için tek doğruluk kaynağı `_targets.R`'dir.**
- `R/` — **kütüphane** (saf fonksiyonlar, `source()` ile yüklenir, side-effect yok)
- `scripts/R/` — **runner**'lar (R/ fonksiyonlarını çağırıp dosya yazar)
- `tests/` — her R/ modülü için karşılık (`stopifnot` ile assertion)
- `data/raw/Raw Data - Final.csv` — tarihsel ham veri girişi; analiz için doğrudan kullanılmaz
- `data/processed/FINAL_REFERENCE__analysis_base_family.csv` ve `data/processed/FINAL_REFERENCE__analysis_base_long.csv` — kilitli kanonik analiz baz CSV'leri
- `outputs/tables/`, `outputs/figures/`, `outputs/models/` — analiz artefaktları (gitignored)
- `references/references.bib` + `apa.csl` — bibliyografya
- `renv/` + `renv.lock` — paket reprodüksiyonu

## Kritik domain bilgisi

- **Veri yapısı:** 482 satır = **241 aile × 2 katılımcı** (1 indeks çocuk + 1 kardeş). DM indeks aile 120, kontrol indeks aile 121. Her satır bağımsız değildir → multilevel/aile-içi ICC zorunlu.
- **EMBU formları:** Final kanonda 29 P-soru + 29 C-soru vardır; `q01-q29` ebeveyn ve çocuk formunda aynı semantik sırayı temsil eder. Kanonik formlar için bkz. [`docs/protokol/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md`](docs/protokol/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md) ve [`docs/protokol/KANONIK_KISALTILMIS_EMBU_COCUK.md`](docs/protokol/KANONIK_KISALTILMIS_EMBU_COCUK.md).
- **Kanonik form öncesi EMBU karar geçmişi arşivdedir.** Eski madde mimarisi, standardizasyon/refinement notları ve Stage 1-3 CSV raporları `archive/2026-04-26_pre_canonical_embu/` altına taşınmıştır.
- **Likert standardı:** Final kanonik CSV'lerde EMBU-P ve EMBU-C itemları 4'lü Likert standardındadır.
- **Geçerli aralık dışı değerler** (ör. tipo `14`, `21`) Stage 1'de NA'ya çevrilir; kanonik form öncesi outlier raporları arşivdedir.
- **PII koruması:** `ad.*soyad` regex'iyle eşleşen kolonlar Stage 1'de düşürülür. `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/` `.gitignore`'da — **commit etmeyin**.
- **Aile anahtarı:** `aile_no` × `cocuk_no` birincil anahtar. Aileler arası eşleştirme `R/04_embu_stage3_family.R` üzerinden.

## Aktif analiz durumu (2026-08-01 itibarıyla)

- **Kanonik analiz baz kilidi yürürlükte.** Final CSV üzerinde herhangi bir değişiklikten önce [`data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`](data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock), kanonik P/C formları ve [`docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`](docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md) okunmalıdır.
- Kanonik form öncesi dokümantasyon aktif karar kaynağı değildir; yalnız karar geçmişi olarak arşivde tutulur.
- **Faz I (H1-H5 + KISIM VI-XVIII) yürürlükte; Faz II-VI SAP (KISIM XIX-LI, `R/32-65`) keşifsel/post-hoc katman olarak işaretlidir** (Faz II: `R/32-62`; Faz III-IV: OSF Layer 5; Faz V `R/64` §136-141; Faz VI `R/65` §142-151 — faz sınırları için bkz. `_targets.R`). Beck Depresyon ve KİA analizleri ana hatta entegredir (H4 Beck-parenting SEM `R/19`, ağ analizi `R/26`, klinik tanı uzantısı `R/46`).
- **Nitel kol tek repoda:** karma tezin niteliksel kolu artık ayrı repo değil; içerik kök `niteliksel/` alt-ağacına taşınmıştır (bkz. [`niteliksel/CLAUDE.md`](niteliksel/CLAUDE.md)). Bu kök nicel koldur.
- Yöntem kararlarının arşivi: `docs/method_archive/`.

## Claude Code katmanı (zorunlu)

- Deterministik zorlama devrededir: `.claude/settings.json` `permissions.deny`
  (`data/raw|identified|cleaned|backup/**` tam kapalı; `data/processed` +
  `outputs` satır-düzeyi formatları kapalı, `.lock`/veri-haritası metadata
  okunabilir; `_targets/**` ve credential dosyaları kapalı) ve `.claude/hooks/`
  beşlisi (SessionStart CONVENTIONS+talimatname enjeksiyonu, prompt sır
  taraması, Bash deny-list, çıktı incelemesi, kaynaksız-sayı Stop kapısı).
- Codex ikizi `.codex/hooks/`'tur; politika değişirse iki ağaç +
  `tests/test_claude_hooks.py` + plugin regresyonu birlikte güncellenir.
- Slash komutlar: `/tez-oturum` (oturum ritüeli), `/bolum-sertifika`
  (Kapı 0–5 sertifikasyonu), `/referans-kapisi` (7-adımlı citation kapısı,
  Adım 0 `bib_hygiene.py` ön-mutabakat), `/tez-literatur` (narratif derin-
  literatür kapısı), `/tez-dogrulama` (kapanış doğrulama paketi). Bulgular
  bölümü için iki kardeş zenginleştirme kapısı: `/anlatim-zenginligi` (nesir
  anlatım + referans; kanıt/figür/tablo dokunulmaz) ve `/veri-gosterimi-zenginligi`
  (veri-gösterim katmanı: R çıktısı↔metin mutabakatı, figür/tablo veri-tutarlılığı
  + estetik/Türkçe/tasarım, eksik-ama-yararlı yeni görsel, başlık/altyazı + betim
  netliği; kanıt _değeri_ dokunulmaz). İkisi de sayı/yön/anlamlılığı değiştirmez;
  eşgüdüm sırası (gösterim önce, anlatım sonra) ve devir protokolü
  [`tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md`](tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md).
- Kapsamlı tez kontrol checklisti: `scripts/util/tez_checklist_verify.py` (8
  eksen · 28 madde) mevcut denetim araçlarını (`bib_hygiene`,
  `karma_ledger_check`, `claim_certification`, `csr_*_audit`, `tr_corpus_audit`)
  alt-süreçle birleştiren salt-okuma orkestratördür; `--fast` hızlı ön-uçuş,
  `--section`/`--chapter` daraltma, `--audit-doc` belge↔script ID senkronu.
  İnsan-okunur master belge [`tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md`](tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md);
  ID'ler script kaydına birebir eşleşir (herhangi FAIL = teslim engeli).

## Sayısal bütünlük kaideleri (zorunlu)

Bir denetimde ortaya çıkan üç kök-neden hata sınıfını (BF₁₀ drift'i, LPA tablo↔metin
çelişkisi, imkânsız AUC optimizm düzeltmesi) tekrarlamamak için; sayısal bir sonuç
(BF, beta, ICC, AUC, CFI, entropi …) üreten her değişiklikte bağlayıcıdır. Otorite
[`AGENTS.md`](AGENTS.md) "Sayisal Butunluk Kaideleri" bölümüdür.

- **Kaynak-tekilliği:** APA tablo/metin üreten `R/` fonksiyonları istatistik değerini
  gömülü literal taşıyamaz; üretilmiş model/CSV artefaktından (`outputs/models/*`,
  `data/processed/*`) okur. Zorlama: `r_generator_literal_audit.py` → checklist
  **K5-LIT-01** kapısı (herhangi bulgu = FAIL).
- **Dosya-izleme:** Bir hedefin okuduğu türetilmiş CSV/RDS `_targets.R`'de
  `format = "file"` ile izlenir; kaynak artefakt değişince içerik-hash geçersizlemesi
  tetiklenir, stale değer okunmaz.
- **Tam senkron:** Model/veri her değiştiğinde tek runner değil tam `tar_make()`
  çalıştırılır; kapanışta `tar_outdated()` boş (0 hedef) olmalıdır.
- **Yön-mantığı testi:** Bir büyüklük yalnız hesaplanmış olmakla değil doğru yönde
  olmakla doğrulanır (optimizm düzeltilmiş AUC ≤ ham AUC; Savage-Dickey BF sınıf
  etiketi sayısal BF ile tutarlı). İlgili `tests/*` bu yön-savlarını içerir.
- **Seçim kuralı tutarlılığı:** LPA/model seçimi tek parsimoni kuralına
  (Raftery 1995 ΔBIC≤2) bağlıdır; APA tablosu ve gerekçe metni aynı profil/model
  sayısını gösterir.

## Yazım & dil

- Tez ana dili **Türkçe** (`lang: tr`); kod yorumları ve commit mesajları da Türkçe tercih edilir
- Resmi tez yazım, format, bölüm sırası, özet/summary, tablo/şekil ve kaynakça kararları için
  önce [`tez-yazim/README.md`](tez-yazim/README.md) ve [`docs/tez-kilavuz/`](docs/tez-kilavuz/)
  kullanılır; bu kaynaklar eski stil notlarına üstündür.
- Quarto exec defaults: `echo: false`, `warning: false`, `message: false`, `freeze: auto`
