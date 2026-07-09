# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 01 — GİRİŞ ve AMAÇ |
| Bölüm başlığı | GİRİŞ ve AMAÇ |
| Üretim dosyası | `chapters/01_giris_ve_amac.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md` |
| Sertifikasyon tarihi | 2026-07-07 |
| Sertifikasyonu uygulayan | Claude Code (Opus 4.8) — sertifikasyon tekrar denetimi |
| Uygulama onayı | `verildi` — "manuel inceleme ok" (2026-07-07) |
| Onay veren | Araştırmacı (kullanıcı) |

## Kapı 0: Kapsam ve Gizlilik — PASS

- [x] Bölüm dosyası + hazırlık briefi okundu.
- [x] `docs/tez-kilavuz` + `format-kontrati.md` + kanonik `marmara-tez-formati-talimatnamesi.md` okundu.
- [x] Referans denetim ledgeri okundu (kaynak evreni).
- [x] Ham veri / transcript / satır düzeyi veri / credential rapora taşınmadı. Harici servislere yalnız yayımlanmış bibliyografik künye gönderildi.

## Kapı 1: Derin Literatür ve Künye Evreni — PASS (re-certification)

Kaynak evreni önceki oturumlarda kurulmuş ve `referans-denetim-ledgeri.md`'de kapatılmıştır. Bu tekrar denetiminde:

- Orphan-citation taraması: bölümdeki tüm `@key`'ler `references.bib`'te çözülüyor (0 orphan).
- Retired-key kullanımı: yok (§3.8.2 YÖK-tez kaynakları dergi karşılıklarıyla değiştirilmiş; metinde retired key kullanılmıyor).
- citation-verifier (axis A) örneklemi: `bell2025globalT1D`, `pinquart2013`, `deLosReyes2015`, `furmanBuhrmester1985srq`, `eviz2026turkiyeCare`, `ada2026children` (ortak) → hepsi çözülüyor, metadata birebir, **retraction/expression-of-concern yok**.

Kapı 1 kararı: **PASS**

## Kapı 2: Full-Text, Zotero — PASS (re-certification)

Bölümde kullanılan tüm citation'lar ledger'da `cite-ok`: DOI/PMID/ID + full-text route (PMC/OA · OpenAthens · Anna's) + Zotero item key + BibTeX key + claim notu ile kapalı. Bu oturumda yeni referans eklenmedi; tam metin rotaları yeniden açılmadı (mevcut ledger geçerli).

Kapı 2 kararı: **PASS**

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu — PASS

- [x] Resmi başlık: `# GİRİŞ ve AMAÇ` — ana başlık büyük harf, bağlaç "ve" küçük (§1.3).
- [x] **Alt başlık yok** — şablon kuralı (§3.3): Giriş ve Amaç bölümünde alt başlık kullanılmaz. Bölüm tek `#`, 0 `##`. Uyumlu.
- [x] Bölüm işlevi: problem → boşluk (triadik çok-bilgi-kaynaklı desenin yokluğu) → gerekçe → amaç + beş alt amaç (H1–H5). Amaç açık ve ölçülebilir.
- [x] H1–H5 tanımı Gereç ve Yöntem'deki modellerle tutarlı (çapraz doğrulandı).
- [x] Nitel/nicel kanıt türü ayrımı korunmuş; nitel = tamamlayıcı kanıt (etki tahmini değil).
- [x] Tüm `@key`'ler `references.bib` içinde.
- [x] Ondalık virgül; sayaç sayılarında binlik ayırıcı nokta (108.300 / 149.500 = doğru Türkçe biçim).

Kapı 3 kararı: **PASS**

## Kapı 4: Türkçe İmla, Akış ve Mantık — PASS

sci-audit **axis G** (deterministik `tr_sciaudit.py`, certification strictness) — rapor: `raporlar/01_giris_ve_amac-tr-sciaudit.md`

- Errors (blocker): **0**
- Warnings (major): 7 — 2× `decimal-dot` (108.300/149.500 = binlik ayırıcı, **yanlış pozitif**), 4× `sentence-long` (yoğun akademik anlatım, kabul), 1× `readability-very-hard` (bilimsel içerikle gerekçeli).
- G5 blocker (İngilizce ondalık-nokta `p`): yok.

Kapı 4 kararı: **PASS** (warning'ler gerekçeli kabul; blocker yok)

## Kapı 5: AI-Reliability ve Teknik Doğrulama — PASS

Manüskript adli denetimi (sci-audit axes A–F):

| Eksen | Sonuç |
|---|---|
| A referans bütünlüğü | Örneklem 6 referans çözüldü, metadata birebir, retraction yok |
| B claim grounding | claim-refuter: bu bölümdeki 3 yüksek-etkili sayı (`ogle2022idfAtlas` 108.300/149.500; `yesilkaya2016` 0,75‰ + 10,8/10⁵; `chen2023` %22,4/%31,5) → **hepsi SUPPORTED**, kaynak özetiyle birebir |
| C istatistik iç-tutarlılık | Bölümde türetilmiş istatistik yok (yalnız kaynaklı epidemiyoloji) |
| D halüsinasyon sinyalleri | Entity/sayı örüntüsü kaynaklı; uydurma kaynak/sayı bulunmadı |
| E raporlama-kılavuzu | Giriş bölümü için ayrı kılavuz yok |
| F AI-şeffaflık | Yöntem'de LLM beyanı mevcut |

Repo/veri invaryantı:

| Komut | Sonuç |
|---|---|
| `doktoratezi-ai-audit` | **142/142 passed** |
| `t1dm-qual-ai-audit` | **55/55 passed** |
| `git diff --check` | temiz |
| `quarto check` | Quarto 1.6.43, ortam OK |

AI-use log: `99_ai_use_log/ai_use_log.csv` güncellendi (harici bibliyografik API kullanımı; ham/kimliklenebilir bayrakları `no`).

Kapı 5 kararı: **PASS**

## Bloklayıcılar ve Çözüm

Yok. Açık bloklayıcı bulunmadı.

## Nihai Sertifika Kararı

| Kapı | Karar |
|---|---|
| Kapı 0 | PASS |
| Kapı 1 | PASS |
| Kapı 2 | PASS |
| Kapı 3 | PASS |
| Kapı 4 | PASS |
| Kapı 5 | PASS |
| **Nihai durum** | **`certified-final`** |

Final notu: Tüm teknik kapılar PASS. Bölümde açık bulgu/düzeltme kalmadı. Kullanıcı 2026-07-07'de açık uygulama onayı verdi ("manuel inceleme ok", Nihai Karar Kuralı #5) → **`certified-final`**. Bu oturumda 01. bölüm dosyası **değiştirilmedi**; onay öncesi Kapı 4 (sci-audit axis G: 0 error / 7 warning) ve Kapı 5 (doktoratezi-ai-audit 142/142, t1dm-qual-ai-audit 55/55, `git diff --check` temiz, `quarto check` OK) taze delille yeniden doğrulandı.
