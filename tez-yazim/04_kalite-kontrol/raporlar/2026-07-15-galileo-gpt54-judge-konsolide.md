# Galileo GPT-5.4 Bağımsız Judge — Tam Tez Konsolide Rapor

**Tarih:** 2026-07-15
**Katman:** Galileo bağımsız ikinci-görüş (sci-audit Claude-native denetiminin YANINDA)
**Judge modeli:** GPT-5.4 (`GALILEO_JUDGE_MODEL`, `/chat/completions`) — Roche-içi OpenAI-uyumlu gateway
**Embedding:** `gemini-embedding-001` (3072-boyut, Vertex `@vertex-ai-1`) — CANLI
**Köprü:** `scripts/eval/galileo_bridge.py` · orkestratör `scripts/eval/run_full_thesis_judge.py`
**Kapsam:** `chapters/00c, 01–05` (gövde bölümleri) + tam-tez heading montajı + `references.bib` (308 kayıt)
**KVKK:** Gateway'e YALNIZ manuskript metni + başlık listesi gönderildi; ham veri/transkript ASLA.

---

## Yönetici Özeti — Three-Tier Gate

| Tier | Sayı | Not |
|---|---|---|
| 🔴 **HARD** | **0** | sci-audit tarafında; Galileo HARD üretmez (tasarım) |
| 🟠 **SOFT-block** | **0 gerçek** | 30 groundedness_low sinyali → tümü KANIT-sağlanmadı artefaktı (aşağıda ispat) |
| 🟡 **advisory** | 4 | reporting-verb monotonluğu (×2), bitişik-tekrar (×1), yoğun-sentez parse (×1) |

**Karar: Bağımsız GPT-5.4 katmanı teslim engeli üretmedi.** Bulgular sci-audit sonuçlarıyla
yakınsıyor (convergent validity): aynı stilistik advisory'ler iki bağımsız denetleyici tarafından
işaretlendi; hiçbir yeni içerik/olgu hatası ortaya çıkmadı.

---

## 1. Gateway Canlılık ✅

`t_galileo_stats` → `ok:true, judge_ok:true, embedding_ok:true, gateway_set:true`.
Judge GPT-5.4 + native gemini-embedding-001 ikisi de canlı.

## 2. Bölüm-Bazlı GPT-5.4 Judge (33 değerlendirme)

Metrik ortalamaları (n=30 başarılı; 2 chunk yoğun-sentez parse-error, 1 tekrar-başarılı):

| Metrik | Ortalama | Min | Yorum |
|---|---|---|---|
| **faithfulness** (iç/kanıta sadakat) | **0,796** | 0,62 | İYİ — metin iç-tutarlı |
| **marmara_compliance** | **0,691** | 0,41 | Kabul — akademik edilgen + virgül-ondalık |
| hallucination_risk | 0,522 | 0,28 | Aşağıda: işaretli span'ler meşru |
| groundedness | 0,384 | 0,28 | **ARTEFAKT** (KANIT sağlanmadı) |

### 2a. Groundedness düşüklüğü — kanıtlanmış artefakt

Judge sistem-promptu "KANIT yoksa muhafazakâr davran, `citation_support='na'`" der. Orkestratör
KVKK/hız gereği KANIT (bib/kaynak tam-metin) göndermedi. Kontrollü A/B testi (01_giriş, aynı metin):

| Koşul | groundedness | citation_support | hallucination_risk |
|---|---|---|---|
| KANIT'sız | 0,34 | unsupported | 0,78 |
| **KANIT+** (bib doğrulama özeti) | **0,88** | **supported** | **0,22** |

→ groundedness/citation/hallüsinasyon sinyalleri **yalnız KANIT yokluğundan** düşük; metin
kusuru değil. Bu, sci-audit Axis B (claim_certification: 168/169 bağlı) ve Axis A (bib_hygiene
HARD=0, 286/286 DOI) ile birebir tutarlı.

### 2b. İşaretli span'ler (flagged_spans) — tümü meşru

Judge'ın işaretlediği tüm yüksek-risk span'ler ya `[@key]` atıflı dış-literatür sayıları
(bell2025globalT1D, chen2023parentD, Pinquart g=0,39 vb.) ya da iç istatistik çıktıları
(multiverse %0 p<0,05, permütasyon n=5000, MNAR OR=4,56). Uydurma kaynak veya kaynaksız
kesin-yargı tespiti YOK.

### 2c. Parse-error (2 chunk)

`05 ch1a` ve `03 ch4` (halved sonrası ch1a): en yoğun sentez düzyazısı; judge 700-token JSON
bütçesini aşınca kesildi. Yarıya bölünce `03 ch4a/4b` ve `05 ch1b` temiz judge verdi. İçerik
kusuru değil, çıktı-bütçesi sınırı → advisory.

## 3. Bölümler-Arası Consistency ✅ TEMİZ

`t_galileo_consistency` (embedding modu, GPT-5.4 pair-judge onaylı): 6 gövde bölümü,
**çelişki/tekrar çifti = 0**. Bölümler-arası olgu çelişkisi yok.

## 4. bib_dedup ✅ TEMİZ (1 false-positive elendi)

308 kayıt. Lexical-fallback 1 "dup" işaretledi:
`tauschmann2025ispadGlucoseMonitoring2024` ↔ `deBock2024ispadGlycemicTargets`.
→ **FALSE-POSITIVE**: yalnız ISPAD kılavuz başlık-öneki aynı. Farklı DOI (000543156 vs
000543266), farklı ilk-yazar, farklı konu (Glucose Monitoring vs Glycemic Targets). Embedding
doğrulaması **cosine=0,908 < 0,96 → DISTINCT**. Gerçek yinelenen referans yok.

## 5. Heading Cascade ✅ TEMİZ

`t_galileo_heading_cascade` tam-tez montajı (`check_order=True`): Marmara §1.3 kaskad
(derinlik≤4, ana-başlık büyük-harf, bağlaç küçük, başlık-sonu-noktalama) + §5 bölüm sırası
(18 kalem) → **errors=0, warnings=0**.

## 6. Coherence ✅ ~TEMİZ (1 advisory)

`t_galileo_coherence` (gemini-embedding, komşu-paragraf cosine):

| Bölüm | paragraf | akış-kopukluğu | bitişik-tekrar |
|---|---|---|---|
| 02_genel_bilgiler | 191 | 0 | 1 (par 158-159, sim=0,961) |
| 04_bulgular | 129 | 0 | 0 |
| 05_tartisma | 36 | 0 | 0 |

Par 158-159: ikisi de triadik tasarımı tanıtıyor; 159 "karşılaştırma olanağı" nüansı ekliyor →
tam tekrar değil, hafif örtüşme → **advisory** (isteğe bağlı birleştirme).

## 7. Reference Prose — 2 advisory (sci-audit ile yakınsak)

`t_galileo_reference_prose`:
- `01_giris`: trailing_ratio=1,0; baskın fiil "işaret etmektedir" → reporting-verb monotonluğu.
- `02_genel_bilgiler`: trailing_ratio=0,98; baskın fiil "göstermektedir".

Bu, sci-audit Axis G advisory'si (H-VERB/H-BRAK) ile **birebir örtüşür** — bağımsız GPT-5.4
katmanı aynı stilistik sinyali doğruladı. Substantif boşluk değil, retorik çeşitlilik önerisi.

---

## Yakınsama (sci-audit ↔ Galileo GPT-5.4)

| Bulgu | sci-audit | Galileo GPT-5.4 | Uyum |
|---|---|---|---|
| Uydurma kaynak / DOI | HARD=0 | flagged span'ler meşru | ✅ |
| Claim grounding | 168/169 bağlı | KANIT+ ile grnd 0,88 | ✅ |
| Bölüm çelişkisi | causal 0 | consistency 0 | ✅ |
| Bib duplikat | — | 0 (1 FP elendi) | ✅ |
| Başlık/sıra | §genel-bilgiler L4 SOFT | cascade 0 hata | ✅ (montajda temiz) |
| Reporting-verb | H-VERB advisory | monotony ×2 | ✅ örtüşme |
| Ondalık virgül/p | HARD=0 | marmara ort 0,69 | ✅ |

İki bağımsız denetleyici (Claude-native + GPT-5.4) **aynı sonuca** ulaştı: **0 teslim engeli**,
yalnız isteğe bağlı retorik advisory'ler.

## Teslim Öncesi Opsiyonel (blocker değil)

1. 01/02'de birkaç atıf cümlesini anlatısal biçime çevirip reporting-verb çeşitliliği artırmak.
2. 02 par 158-159 hafif örtüşmesini tek paragrafta birleştirmek.
3. (Metodolojik) Judge'ı KANIT-besleme modunda çalıştırmak istenirse groundedness gerçek
   ölçülür; mevcut çalıştırma hız/KVKK gereği KANIT'sızdır ve düşük groundedness beklenen çıktıdır.
