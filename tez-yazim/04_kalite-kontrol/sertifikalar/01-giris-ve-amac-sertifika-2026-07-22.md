# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 01 |
| Bölüm başlığı | GİRİŞ ve AMAÇ (Marmara §3.3) |
| Üretim dosyası | `chapters/01_giris_ve_amac.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md` |
| Sertifikasyon tarihi | 2026-07-22 |
| Sertifikasyonu uygulayan | Claude (bolum-sertifika kapısı) |
| Uygulama onayı | `verildi` — kullanıcı açık onayı ("onaylıyorum", 2026-07-22) |
| Onay veren | Kullanıcı (tez sahibi) |
| Önceki sertifika | `01-giris-ve-amac-sertifika-2026-07-16.md` (`certified-final`, onay "Uygun" 2026-07-16) |
| İçerik durumu | **2026-07-16'dan beri DEĞİŞMEMİŞ** (working-tree temiz; 01'e dokunan son commit'ler cert-dönemi). Bu koşum, standing certified-final'in kapsamlı yeniden-doğrulamasıdır. |

## Kapı 0: Kapsam ve Gizlilik — PASS

- Dosya + hazırlık briefi (`03_bolum-hazirlik/01_giris-ve-amac.md`) okundu. Bölüm işlevi = Marmara §3.3 (genel çerçeve + bilimsel boşluk + önem/katkı + açık amaç; **alt başlık kullanılmaz**).
- Kritik kaynak manifesti okundu. Ham veri / transcript / satır düzeyi klinik veri / credential rapora taşınmadı.

## Kapı 1: Derin Literatür ve İddia Haritası — PASS

- 20 dış iddia ekseni (T1DM epidemiyoloji → psikososyal aile etkisi → ebeveynlik davranışları → anne depresyonu → kardeş → çoklu bilgi kaynağı → Türkiye/boşluk → amaç) 20 benzersiz künyeye bağlı.
- **Orphan-claim yok:** sayısal literatür iddialarının tümü atıflı — IDF 108.300 / 149.500 (`@ogle2022idfAtlas`), Türkiye binde 0,75 / yüz binde 10,8 (`@yesilkaya2016turkiyeIncidence`), anne %31,5 / ebeveyn %22,4 (`@chen2023parentDepression`). Sayısal prevalans cümleleri kaynak popülasyonu + aktarılabilirlik çerçevesiyle verilmiş (brief §Yazım Sınırları).
- Ulusal boşluk iddiası "belirgin değildir / sınırlıdır" kalıbıyla, mutlak yokluk olmadan (§brief uyumlu).

## Kapı 2: Full-Text, Zotero ve Ledger — PASS

- Bölümdeki **20 atıfın 20'si `cite-ok`** (`referans-denetim-ledgeri.md`): adal2015psychosocial, bell2025globalT1D, butner2009discrepancy, ceran2024selfmgmt, chen2023parentDepression, crandell2017, deLosReyes2015, eckshtain2010parentDepression, eviz2026turkiyeCare, furmanBuhrmester1985srq, goodman2020parentingMediator, ludvigsen2026siblingT1D (satır 79 — PMC OA, cc-by, canlı tam metin), lummerAikey2021, ogle2022idfAtlas, ozguven2025parentalCollab, pinquart2013, trojanowski2021, whittemore2012, yesilkaya2016turkiyeIncidence, yuksel2024qol.
- `full-text-exception` yalnız `chanShorey2022`'de ve **bu bölümde kullanılmıyor** (ledger notu: "metinde kullanılmıyor"; citation yükü ludvigsen+lummer'a konsolide).
- **Şerit-B `bib-dup`:** HARD=0, advisory=0 (temiz).
- GİRİŞ atıflarında `full-text-pending` / `zotero-pending` / `reliability-pending` / `citation-without-full-text` = 0.

## Kapı 3: Bölüm Metni, Format ve İç Tutarlılık — PASS

- **Format §3.3:** alt başlık YOK (§1.3 ✓); tez-kaynağı (YÖK/tez) atıfı YOK (§4.2 ✓); ondalık virgül doğru (0,75; 10,8; %22,4; %31,5). "108.300 / 149.500" = **binlik ayıracı** (Türkçe nokta); axis-G `decimal-dot` uyarısı bu ikisinde **false positive** (tam sayı, ondalık değil).
- Bölüm işlevini eksiksiz yerine getiriyor: çerçeve → boşluk → H1-H5 gerekçe → nitel kol → karma yöntem → soru/amaç.
- **Galileo (Kapı 3 zorunlu assembly):**
  - `galileo_overclaim_judge` = **0,22** (advisory; causal_drift=false, cherry_pick=false). Not: "aracı rol"/"aracılığıyla" gözlemsel mediation literatüründe (goodman2020, eckshtain2010) nedenselliğe hafif yaklaşıyor ama "işaret etmektedir/olabileceğini" ile yumuşatılmış — SOFT-block eşiği altı, düzeltme gerektirmez.
  - `galileo_harking_judge` = **0,03**; post_hoc_as_prior=false (H1-H5 OSF ön-kayıtla örtüşüyor).
  - `galileo_convergence_judge` = relationship "belirsiz", **over_integration=false**, conf. 0,96 — GİRİŞ tasarım-gerekçesi (bulgu/joint-display yok), erken-uyum kurulmamış (doğru).

## Kapı 4: Türkçe İmla, Akış ve Mantık — PASS

- **sci-audit axis G (`tr_sciaudit.py`, certification): Errors (blocker) = 0 → PASS.** 7 major / 1 minor advisory: 2 `decimal-dot` = binlik-ayıracı false-positive (108.300/149.500); kalanı `sentence-long` (yoğun akademik giriş nesri).
- **Şerit-B `redundancy`:** semantik paragraf tekrarı = 0 (temiz).
- **`galileo_coherence_judge`:** chain_intact=**true**, coherence **0,86**. 5 advisory gap: hepsi ileri-bölüm bağımlılığı biçiminde ("giriş H1-H5 / aracılık / çoklu bilgi kaynağı ayrışması / kardeş rolü / karma entegrasyon kuruyor; bulgular-tartışma bunları kapamazsa zincir zayıflar"). GİRİŞ'in **iç zinciri sağlam**; gap'ler ayrı sertifikalanan downstream bölümlere ait — advisory.

## Kapı 5: AI-Reliability, Render ve Repo Doğrulaması — PASS (bir dokümante carve-out)

- `bib_hygiene all`: **HARD = 0** (exit 2 SOFT, repo-geneli; GİRİŞ-dışı) ✓
- `git diff --check` (01): temiz (içerik değişmemiş) ✓
- `quarto check`: OK (Quarto 1.9.38; tüm bağımlılıklar) ✓
- **Repo/veri invaryant (`doktoratezi-ai-audit`):** KVKK/ham-veri/quote-parity/kanonik-kilit/Stop-kaynaksız-sayı invaryantları **PASS**; koşum exit=1 yalnız **`.codex` iskele-parite driftı** (`.codex/hooks*`, `CONVENTIONS.md` "materialized matches asset" — çalışan ağaçtaki `CONVENTIONS.md`/`AGENTS.md` değişikliklerinden; önceden var, GİRİŞ-dışı repo-bakım). Dokümante carve-out (ÖZET sertifikasıyla aynı kalem).
- `run_full_thesis_judge.py` artefaktı yok → **K5-GAL-01 advisory SKIP** (per-bölüm galileo dörtlüsü koşuldu).

## Nihai Karar

| Kapı | Sonuç |
|---|---|
| Kapı 0 | PASS |
| Kapı 1 | PASS |
| Kapı 2 | PASS (20/20 cite-ok) |
| Kapı 3 | PASS (galileo overclaim 0,22 advisory; harking 0,03; convergence over_integration=false) |
| Kapı 4 | PASS (axis G 0 blocker; coherence 0,86; redundancy 0) |
| Kapı 5 | PASS* (*`.codex` iskele-driftı dokümante carve-out) |
| HARD bulgu | **YOK** |
| Açık kullanıcı onayı (bu tur) | **verildi** ("onaylıyorum", 2026-07-22) |
| **Nihai durum** | **`certified-final`** |

**Gerekçe:** Altı kapının tamamı teknik olarak PASS; HARD blocker yok; galileo dörtlüsü eşik-üstü SOFT-block üretmedi. İçerik 2026-07-16 `certified-final` sürümünden **değişmemiştir** (working-tree temiz). Bu turun kapsamlı yeniden-doğrulaması standing sertifikayı teyit etmiş ve kullanıcı açık onayı ("onaylıyorum", 2026-07-22) alınmıştır; bölüm bu tarih için `certified-final`'a yükseltilmiştir. Tek açık kalem `.codex` iskele-parite driftidir (GİRİŞ-dışı, KVKK/veri invaryantları PASS) — dokümante carve-out olarak kabul edilmiştir; ayrı repo-bakım adımıyla (Codex-ikizi yeniden senkron) kapatılmalıdır.

**`certified-final` ön-koşulu:** açık kullanıcı onayı (+ `.codex` iskele carve-out'un kabulü — veya ayrı repo-bakım adımıyla Codex-ikizi yeniden senkronu).

Advisory (bloklamaz): overclaim 0,22 (mediation kipleri — mevcut hedge yeterli); coherence ileri-bölüm bağımlılık gap'leri (downstream sertifikalarda kapanır).
