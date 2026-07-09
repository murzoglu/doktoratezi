# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 02 — GENEL BİLGİLER |
| Bölüm başlığı | GENEL BİLGİLER |
| Üretim dosyası | `chapters/02_genel_bilgiler.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/02_genel-bilgiler.md` |
| Sertifikasyon tarihi | 2026-07-07 |
| Sertifikasyonu uygulayan | Claude Code (Opus 4.8) — sertifikasyon tekrar denetimi |
| Uygulama onayı | `verildi` — "manuel inceleme ok" (2026-07-07) |
| Onay veren | Araştırmacı (kullanıcı) |

## Kapı 0: Kapsam ve Gizlilik — PASS

- [x] Bölüm dosyası + hazırlık briefi + kanonik format talimatnamesi okundu.
- [x] Ham veri / transcript / credential rapora taşınmadı; harici servislere yalnız bibliyografik künye gönderildi.

## Kapı 1: Derin Literatür ve Künye Evreni — PASS (re-certification)

- Orphan-citation taraması: 0 orphan (tüm `@key`'ler `references.bib`'te).
- Retired-key kullanımı: yok — YÖK-tez kaynakları (§3.8.2 gereği kaynak olamaz) dergi karşılıklarıyla değiştirilmiş (`ozguven2025parentalCollab`, `ceran2024selfmgmt`, `cetintas2021dfis`, `senCelasin2018plbss`, `yuksel2024qol`, `adal2015psychosocial`); tek korunan tez istisnası `apalaci1996yoktez` (KİA/SRQ Türkçe uyarlama birincil kaynağı, danışman kararı).
- citation-verifier (axis A) örneklemi: `dimeglio2018t1d`, `ada2026children`, `haller2024ispadScreeningStaging`, `ziegler2013isletAutoantibodies`, `pinquart2013`, `deLosReyes2015`, `furmanBuhrmester1985srq`, `eviz2026turkiyeCare` → hepsi çözülüyor, metadata birebir, **retraction yok**.

Kapı 1 kararı: **PASS**

## Kapı 2: Full-Text, Zotero — PASS (re-certification)

Bölümde kullanılan tüm citation'lar ledger'da `cite-ok` (DOI/PMID + full-text route + Zotero item + BibTeX + claim notu). 2026-07-06 zenginleştirmesinde eklenen dört PMC-OA kaynak (`fang2025techDisparities`, `lansingBerg2014selfRegulation`, `ferro2022informantAgreement`, `wong2023dyadicSatisfaction`) çift AI-reliability geçmiş.

Kapı 2 kararı: **PASS**

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu — PASS

- [x] Resmi başlık: `# GENEL BİLGİLER` (ana başlık büyük harf).
- [x] Başlık hiyerarşisi (§1.3): 8 tematik `##` (Title Case, bağlaçlar küçük) + `###` (sentence case) + `####` (yalnız ölçüm-araç alt başlıkları, sentence case). En çok 4 düzey — tavanda, aşmıyor. Her `##` altında ≥2 alt başlık; bağlayıcı geçiş paragrafları mevcut.
- [x] Bölüm işlevi: genelden özele kuramsal + ampirik arka plan; yorum/sonuç çıkarımından kaçınılmış (§3.4). Gereç ve Yöntem'e geçiş hazırlanmış.
- [x] Nedensel dil disiplini: gözlemsel/meta-analitik kaynaklarda "ilişkili/olabilir" hedge dili tutarlı; §Yorum Sınırları'nda kanıt düzeyi ayrımı açıkça beyan edilmiş.
- [x] Tüm `@key`'ler `references.bib` içinde; ondalık virgül; sayaç binlik ayırıcı doğru.

Bu oturum düzeltmesi: bir near-definitional causal ifade yumuşatıldı ("...değişmesine yol açar" → "yol açabilir", §Türkiye bağlamı teknoloji erişimi).

Kapı 3 kararı: **PASS**

## Kapı 4: Türkçe İmla, Akış ve Mantık — PASS

sci-audit **axis G** (certification strictness) — rapor: `raporlar/02_genel_bilgiler-tr-sciaudit.md`

- Errors (blocker): **0**
- Warnings (major): 67 — çoğunluğu `sentence-long`/`sentence-too-long` (yoğun akademik anlatım). `causal-overclaim` işaretlerinin tümü triaj sonrası **yanlış pozitif / iyi huylu**:
  - `kanıtlar` (×2, L95/L129): "kanıt" **ismi**, yüklem hedge'li ("düşündürür", "olabileceğini göstermektedir").
  - `sağlar` (×8): "olanak sağlar" = metodolojik olanak/imkân (veri nedensel iddiası değil).
  - `neden olur` (L425): bölümün **kaçınılması gereken dil örneği** olarak tırnak içinde verdiği ifade (nedensel disiplin paragrafı).
  - `şey` (L135): "başına bir şey gelmesi kaygısı" = aşırı-koruma yapısının deyimsel ifadesi.
- G5 blocker: yok.

Kapı 4 kararı: **PASS** (causal işaretler yanlış pozitif olarak belgelendi; blocker yok)

## Kapı 5: AI-Reliability ve Teknik Doğrulama — PASS

| Eksen | Sonuç |
|---|---|
| A referans bütünlüğü | 8 referans örneklemi çözüldü, metadata birebir, retraction yok |
| B claim grounding | claim-refuter: bu bölümdeki 3 yüksek-etkili sayı (`ziegler2013` %69,7 [65,1–74,3]/%14,5/%0,4; `buchberger2016` %30,04 [16,33–43,74]; `dundar2023` 13,1/10⁵ AAPC +%8,3) → **hepsi SUPPORTED**, kaynak özetiyle birebir |
| C istatistik iç-tutarlılık | Kaynaklı epidemiyoloji sayıları B'de doğrulandı; türetilmiş test yok |
| D halüsinasyon sinyalleri | Uydurma kaynak/sayı yok; `english-term-leak: Framework` = OSF tanımı (§1.5 uyumlu, yanlış pozitif) |
| E raporlama-kılavuzu | Genel Bilgiler için ayrı kılavuz yok |
| F AI-şeffaflık | Yöntem'de LLM beyanı mevcut |

Repo/veri invaryantı: `doktoratezi-ai-audit` **142/142**; `t1dm-qual-ai-audit` **55/55**; `git diff --check` temiz; `quarto check` OK.
AI-use log: güncellendi.

Kapı 5 kararı: **PASS**

## Bloklayıcılar ve Çözüm

Yok.

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

Final notu: Tüm teknik kapılar PASS. Kullanıcı 2026-07-07'de açık uygulama onayı verdi ("manuel inceleme ok", Nihai Karar Kuralı #5) → **`certified-final`**. Bu oturumda 02. bölüm dosyası **değiştirilmedi**; onay öncesi Kapı 4 (sci-audit axis G: 0 error / 67 warning — hepsi triaj sonrası yanlış pozitif/gerekçeli) ve Kapı 5 (doktoratezi-ai-audit 142/142, t1dm-qual-ai-audit 55/55, `git diff --check` temiz, `quarto check` OK) taze delille yeniden doğrulandı.
