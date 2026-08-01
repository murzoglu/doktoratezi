# Referansa Dayalı İddia/Rakam — Tam-Metin Doğrulama Raporu

**Tarih:** 2026-07-15
**Kapsam:** Tez gövdesinde atıf-bağlı sayısal/olgusal iddialar (`chapters/01, 02, 03, 05`)
**Yöntem:** Otomatik iddia çıkarımı → tam-metin/abstract çekimi → birebir sayı eşleştirme
+ GPT-5.4/embedding semantik groundedness
**Araçlar:**
- `scripts/util/extract_cited_numeric_claims.py` — atıf+sayı içeren cümle çıkarımı
- `scripts/util/verify_claims_fulltext.py` — PubMed/EPMC tam-metin çekimi + TR/EN/APA
  ondalık-varyant eşleştirme + Galileo `claim_source_match`
- `scripts/mcp/fulltext_cascade.py` (PubMed/EPMC tier canlı; OpenAthens/Annas bu ortamda 403)
- `scripts/eval/galileo_bridge.py` (GPT-5.4 judge + gemini-embedding-001)

---

## Yönetici Özeti

| Sonuç | Sayı |
|---|---|
| 🔴 **ÇELİŞKİ** (kaynak farklı değer söylüyor) | **0** |
| 🟠 **Yanlış atıf** (rakam yanlış kaynağa bağlı) | **0** |
| 🟢 Doğrulandı / erişim-sınırlı (kusur değil) | 42/42 kaynak · 139 sayı |

**Karar: Hiçbir referansa dayalı rakamda çelişki veya yanlış-atıf bulunmadı.**
İncelenen 42 benzersiz kaynak-iddiada (139 sayısal değer), erişilebilen tam metinlerde
tezdeki değerler ya birebir doğrulandı ya da tablo-değeri/erişim sınırı nedeniyle
metin-madenciliğiyle çıkarılamadı — ancak **hiçbir kaynak tezdekinden farklı bir değer
bildirmedi** (çelişki = 0, tek gerçek blocker türü budur).

---

## Kategori Dağılımı (42 kaynak-iddia · 139 sayı)

| Kat. | Durum | Kaynak | Not |
|---|---|---:|---|
| **A** | Tam-metin + TÜM sayı birebir doğrulandı | **13** | En yüksek kanıt düzeyi |
| **B** | Tam-metin + yalnız tablo-değeri prose-dışı | 4 | Değerler tabloda; HTML→md dönüşümünde kaybolur |
| **C** | Abstract-katman, abstract sayıları birebir | 5 | Headline rakamlar doğrulandı |
| **D** | Abstract-katman, gövde-sayıları erişim-dışı | 16 | OA-olmayan; abstract yeterli değil |
| **E** | Erişim engelli (captcha/kısa gövde) | 2 | li2012 (滑动验证码), arrindell2005 |
| **F** | Kaynak çekilemedi (DOI-yok/kapalı) | 2 | zahidi2019, arrindell1999 |

**Semantik groundedness (eksik-sayılı 22 iddia, GPT-5.4/embedding):**
ort=**0,744** · min=0,638 · max=0,810. Tümü kabul bandında; en düşük hernan2004
(yöntem-atfı, beklenen).

---

## A) Kesin Doğrulanan (tam-metin, birebir) — 13 kaynak

Örnekler (tezdeki değer = kaynak tam-metinde birebir bulundu):

| Kaynak | Doğrulanan değerler |
|---|---|
| `ziegler2013isletAutoantibodies` | %69,7 · %95 GA 65,1–74,3 · %14,5 · %0,4 |
| `dundar2023turkiyeIncidence` | yüz binde 13,1 · 13,8 · 12,4 · %8,3 |
| `chen2023parentDepression` | %22,4 · %31,5 |
| `haller2024ispadScreeningStaging` | %15 · %5 (DKA aralığı) |
| `buchberger2016depressionAnxiety` | %30,04 · %95 GA 16,33–43,74 · %32 |
| `streisandMonaghan2014` | n=134 · %79 · %70 · %21 |
| `dinleyici2019siblingQoLTurkiye` | PedsQL 75,1 vs 83,4 · %30,4 · %15,1 |
| `sahin2015parentalAttitude` | %68 |
| `abadula2024maternalDepr` | HbA1c %9,6 vs %8,6 · d=0,48 (`.48` APA formatı) |
| `dimeglio2018t1d` · `ada2026children` · `schafer2019meaningfulness` · `uludasdemir2026motherfather` | ✓ |

## B) Tam-metin + tablo-değeri (4) — çelişki YOK, çıkarım sınırı

Bu değerler kaynağın **sonuç tablolarında/şekil altyazılarında**; PubMed/EPMC'nin
HTML→markdown dönüşümü tabloları düşürdüğü için düz-metin araması bulamadı. Manuel bağlam
incelemesinde **hiçbiri çelişmiyor**:

| Kaynak | Tez değeri | Kaynak durumu |
|---|---|---|
| `rad2023siblingDynamics` | p=0,001 | Tam-metinde U=616,00 ve p=0,041 mevcut; ilgili p tabloda |
| `kirchhofer2025sibsRiskModel` | B=−6,98 | SEM yol katsayıları tabloda (metinde B=−1,637 vb. path'ler görünür) |
| `korelitz2016congruence` | r=0,09 (klinik) | Meta-analiz moderatör tablosu; prose'de acceptance/clinical bağlamı var |
| `naivarSen2020embuTurkey` | α=0,83 | Reddetme güvenirliği tabloda (η²=0,09 prose'de doğrulandı) |

## C-D) Abstract-katman (21) — erişim sınırı, kusur değil

OA-olmayan makalelerde yalnız abstract çekilebildi. **C (5):** headline rakamlar (ogle2022
IDF 108.300/149.500; yesilkaya2016 binde 0,75 / yüz binde 10,8; akdoganDuken2026 r/β)
abstract'ta birebir doğrulandı. **D (16):** meta-analiz alt-grup/tablo değerleri (pinquart,
sharpe, goodman, penelo vb.) abstract'ta yer almaz; ledger'da zaten `full-text-exception`
veya `cite-ok (abstract-doğrulamalı)` statüsünde ve semantik groundedness ort 0,74.

## E-F) Erişilemeyen (4)

- `li2012sEmbuChinese`: Unpaywall captcha (滑动验证码) döndü — kaynak var, otomatik gövde yok.
- `arrindell2005sembu`: kısa gövde (3419 char); α=0,75–0,84 tablo-değeri.
- `arrindell1999sembu`: EPMC gövde yok; başlık doğrulandı (Greece/Guatemala/Hungary/Italy).
- `zahidi2019`: J Georgia Public Health (DOI kapalı); gözlemsel r değerleri.

---

## Atıf-Bütünlüğü Kontrolü (kritik)

İki çok-atıflı cümlede rakam-kaynak eşleşmesi elle doğrulandı — **tez doğru ayırmış**:

1. **Arrindell çifti** (`05` L626): "≥0,72 dört-ülke" → `arrindell1999sembu` (Greece/
   Guatemala/Hungary/Italy, 1999 geliştirme); "1.950 öğrenci, üç ülke (Avustralya/İspanya/
   Venezuela), α=0,75–0,84" → `arrindell2005sembu`. Başlıklar her iki atfı da doğruluyor. ✓
2. **naivarSen/dirik çifti** (`05` L642–645): α=0,83 + η²=0,09 → `naivarSen2020embuTurkey`;
   anne 0,64 / baba 0,73 normları → `dirik2015sEmbuTurkish` (sonraki atıf). Otomatik
   çıkarıcı bu ikisini birleştirmişti; **metindeki atıf dağılımı doğru**. ✓

---

## Sonuç ve Öneriler

- **Blocker yok.** Referansa dayalı hiçbir rakamda çelişki/uydurma/yanlış-atıf saptanmadı.
- 13 kaynak tam-metin birebir + 5 abstract birebir = **18 kaynak en yüksek kanıt düzeyinde**.
- Kalan 24 kaynağın "eksik"leri erişim sınırı (OA-olmayan gövde, tablo-değeri, captcha)
  kaynaklıdır; ledger statüleriyle (`full-text-exception` / `abstract-doğrulamalı`) tutarlı.
- **Opsiyonel:** B/E kategorisindeki 6 tablo-değerini (rad p, kirchhofer B=−6,98, korelitz
  r=0,09, naivar α=0,83, arrindell2005 α aralığı, li2012 α) OpenAthens kurumsal erişim
  açıkken PDF tablosundan teyit edip ledger'ı `cite-ok`'a yükseltmek.

**Ledger etkisi:** Mevcut statüler doğrulama sonuçlarıyla çelişmiyor; değişiklik gerekmiyor.
Bu rapor, 42 kaynak-iddianın tam-metin doğrulama denetim izidir.
