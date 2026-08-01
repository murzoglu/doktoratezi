# Bölüm Finalizasyon Sertifikası

Durum: `provisional-pass`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 01 — GİRİŞ ve AMAÇ |
| Dosya | `chapters/01_giris_ve_amac.qmd` (21 satır, 7 paragraf) |
| Sertifika tarihi | 2026-07-12 |
| Strictness | `certification` |
| Önceki sertifika | `certified-final` (2026-07-07) — bu turdan sonra P4/P6 + iki referans eklendiği için yeniden sertifikasyon |

## Kapsam (bu tur)

2026-07-11 GİRİŞ zenginleştirmesi: P4 (maternal depresyon zinciri) + P6 (çok-bilgi-kaynağı) korelasyon dili (2 cümle) ve iki kanonik referansın (`eckshtain2010parentDepression`, `butner2009discrepancy`) eklenmesi. Yanlış-atıf düzeltmesi: taslak `butler2009` → kanonik Eckshtain D, 2010 (PMID 19710249); "Butler JM" aslında `butner2009discrepancy`'nin 4. yazarı.

## Kapı Sonuçları (0-5)

| Kapı | Kapsam | Kanıt | Sonuç |
|---|---|---|---|
| 0 | Kapsam/gizlilik | 20 `@key`, 0 orphan, PII taraması temiz | ✅ PASS |
| 1 | Literatür/orphan | Tüm anahtarlar `references.bib`'de çözülüyor (eckshtain+butner dahil) | ✅ PASS |
| 2 | Full-text/Zotero | İki yeni ref `zotero-ok`; PMC canlı tam metin; item-key pin (`JGTVK7JB`, `MW9KI6GD`) | ✅ PASS |
| 3 | Metin/kılavuz uyumu | Başlık `GİRİŞ ve AMAÇ` (§5 kanonik, lowercase `ve`); İngilizce-nokta `p` yok; AMA-11 in-text 20/20 | ✅ PASS |
| 4 | Türkçe imla/akış (sci-audit axis G) | 0 blocker / 7 warning / 1 info; P4/P6 cümleleri uyarısız | ✅ PASS |
| 5 | AI-reliability + render | aşağıda | ✅ PASS |

### Kapı 5 delili

| Kontrol | Sonuç |
|---|---|
| `doktoratezi-ai-audit` regresyon | **142/142 passed** |
| `test_claude_hooks.py` | **13/13** · hook `py_compile` OK |
| R veri yönetişimi (reproducibility_lock, final_reference_loading, data_governance) | EXIT 0 (stopifnot sessiz = PASS) |
| `t1dm-qual-ai-audit` (nitel kol) | **55/55 passed** |
| `quarto check` | OK (Quarto 1.9.38; Pandoc 3.8.3 / Sass / Deno / Typst OK) |
| GİRİŞ izole render (`--to html`, bib+csl) | **exit 0**; citation'lar CSL ile çözüldü |

## sci-audit 7-Eksen (Faz 3.6)

`tez-yazim/04_kalite-kontrol/raporlar/01_giris_ve_amac-sci-audit.md` — gerçek blocker = 0. Axis B'deki tek "error" araç false-positive'i (Pandoc `[@key]` sözdizimi tanınmıyor; `[@key]`→`(2021)` ile 16/16 grounded, rate 1.0). Axis G `decimal-dot` uyarıları Türkçe binlik ayracı false-positive'i.

## Neden `provisional-pass` (certified-final DEĞİL)

Tüm teknik/dil/referans kapıları PASS. Tek eksik kanıt: **tam-tez `quarto render thesis.qmd` exit 0**. Render, Bulgular bölümündeki APA tablo chunk'ında `outputs/tables/t01_sample_characteristics.csv` (gitignored artefakt) bulunamadığı için durdu. Bu artefaktlar `targets::tar_make()` ile üretilir (ağır brms/lavaan/mice pipeline) ve bu ortamda henüz üretilmedi. **GİRİŞ içeriğiyle ilgisizdir** — GİRİŞ'in izole render'ı exit 0.

**`cite-ok` / `certified-final`'e yükseltme koşulu:** `targets::tar_make()` tamamlanıp tam-tez `quarto render thesis.qmd` exit 0 verdiğinde, ledger iki ref `reliability-ok` → `cite-ok` taşınır ve bu sertifika `certified-final`'e güncellenir.

## Bu turda değiştirilen izlenen dosyalar

- `chapters/01_giris_ve_amac.qmd` — P4/P6 + butler2009→eckshtain2010 düzeltmesi (önceki oturum)
- `references/references.bib` — 2 kanonik künye (önceki oturum)
- `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` — iki ref → `reliability-ok`
- `tez-yazim/04_kalite-kontrol/raporlar/01_giris_ve_amac-sci-audit.md` — 7-eksen rapor
- `tez-yazim/04_kalite-kontrol/raporlar/01_giris_ve_amac-tr-sciaudit.md` — axis G resmi çıktı
- `plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/CONVENTIONS.md` — kök kanonik ile senkron (galileo-gemini + niteliksel monorepo taşıması); 2 FAIL'i giderdi

## Karar

Kullanıcı 2026-07-12'de **provisional-pass** onayı verdi. Davranış kuralı #21 gereği `certified-final` ilan edilmemiştir; tam-tez render kanıtı gelene kadar bölüm `provisional-pass` (`reliability-ok`) statüsündedir.
