# Embedding + AI-Judge Genişletme — Tasarım (Spec)

**Tarih:** 2026-07-11
**Branch:** feat/karma-sentez-hazirlik
**Durum:** onaylandı → **UYGULANDI 2026-07-21** (galileo embedding artık CANLI: Azure
`text-embedding-3-large`; Şerit B aktive edildi). Uygulama özeti dosya sonunda §15.
**İlgili doktrin:** `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`,
`.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md`,
`.claude/galileo.local.md`, memory `plugin-tooling-integration`.

---

## 1. Amaç

Tez sürecinde **text-embedding**'i en etkin modelle en geniş biçimde kullanmak ve **AI-judge**'ı
en geniş biçimde entegre ederek süreçlerin doğruluğunu/tutarlılığını artırmak. Paylaşımlı iki
primitif (bir embedding beyni + genişletilmiş judge gate) üstüne dört tüketici kümesi bağlanır;
her şey mevcut bağımlılıksız-stdlib köprü doktrinine, KVKK sınırına ve doktrin-koruyan gate
mantığına sadık kalır.

## 2. Sabitlenmiş Kararlar (brainstorming çıktısı)

| # | Karar | Değer |
|---|---|---|
| Q1 | Embedding modeli | Gateway'in en güçlüsü hedef; galileo `/embeddings` = `text-embedding-3-large` (`.env`'de ayarlı) — **şu an bozuk**; düzelene kadar retrieval şeridi anamnesis `bge-m3`. |
| Q2 | Kapsam | Dört küme de: Referans bütünlüğü, Bölüm kalitesi, Karma sentez (aktif branch), Yorum disiplini. |
| Q3 | Gate duruşu | Doktrin korunur — LLM judge = SOFT-block/advisory (insan-override); yalnız deterministik embedding-eşik yeni HARD olabilir. sci-audit + repo hook'ları tek gerçek HARD. |
| Q4 | Doğrulama çıtası | Tam titizlik — etiketli kalibrasyon seti + altın-vaka eval harness + pytest + parity guard + yanlış-pozitif bütçesi. |

## 3. Mevcut Durum — Canlı Doğrulama (bu oturum testleri, 2026-07-11)

| Bileşen | Durum | Kanıt |
|---|---|---|
| Judge — galileo `gpt-5.4-2026-03-05` | ✅ CANLI | `/chat/completions` 200, geçerli grounded JSON; ayrı judge anahtarı (sha `44972e06`). |
| anamnesis `bge-m3` | ✅ CANLI | `corpus_stats`: docs=40, chunks=51, nodes=96, edges=64. |
| galileo ham `/embeddings` | ❌ BOZUK | `GALILEO_TEXT_EMBEDDING_API_KEY` (== test anahtarı, sha `db22e3cf`) her model-id değerinde `gpt-5-mini`'ye misroute → 400. |

**Teşhis (galileo embedding):** Anahtarın config'i (`override_params.model`) isteğin routing yoluna
girmiyor; efektif Azure deployment `gpt-5-mini` (sohbet modeli) → embeddings 400. Model-id değeri
(prefix'li/prefix'siz, `-1`'li/`-1`'siz, kanonik) fark etmedi. **Düzeltme senin/admin tarafında:**
anahtarı varsayılan deployment'ı `text-embedding-3-large-1` olan bir Azure virtual-key/config'e
bağlamak (override_params'a güvenmeden). Düzelince bu tasarımda tek kalibrasyonla otomatik terfi.

**Teknik ayrım:** anamnesis ham vektör API'si **değildir** (ingest + sıralı arama verir); galileo
`/embeddings` ham vektör (pairwise cosine matrisi için gerekli) verir. Tasarım iki modaliteyi
ayırır (Bölüm 5).

## 4. Mimari ve Modül Sınırları (izolasyon ilkesi)

### 4.1 `scripts/eval/semantic_core.py` (YENİ, stdlib)
- **Ne yapar:** Ham-vektör embedding beyni. `embed(texts)`, `cosine(a,b)`, `dedup_matrix(items)`,
  `redundancy_pairs(paras)`, `match_matrix(rowsA, rowsB)`.
- **Nasıl kullanılır:** Pluggable backend. Birincil = galileo `/embeddings` (`_load_cfg` deseniyle
  `.env`'den; model `.env`'de). Erişilemezse **temiz `EmbeddingUnavailable`** → asla çökmez, asla
  yanlış-HARD üretmez.
- **Bağımlılık:** yalnız stdlib (`urllib`, `ssl`, `json`, `math`, `hashlib`). Torch/sentence-
  transformers YOK.
- **KVKK guard:** yalnız manuskript/literatür stringi kabul; katılımcı/transkript/aile-düzeyi
  veri girişi reddedilir (assert + test).

### 4.2 `scripts/eval/galileo_bridge.py` (GENİŞLET; şu an 370 satır — `wc -l`)
- **Ne yapar:** Judge araçları (gpt-5.4). Mevcut: `galileo_judge`, `galileo_consistency`,
  `galileo_bib_dedup`, `galileo_claim_source_match`, `galileo_eval_run`, `galileo_stats`,
  `classify_gate`. Yeni: `galileo_convergence_judge`, `galileo_harking_judge`,
  `galileo_overclaim_judge`, `galileo_coherence_judge`.
- **Nasıl:** Embedding gerektiğinde `semantic_core`'u import eder (judge'ı embedding'e kilitlemez).
- **Bağımlılık:** stdlib + `semantic_core`.

### 4.3 `scripts/util/thesis_semantic.py` (YENİ, tracked CLI — `bib_hygiene.py` deseni)
- **Ne yapar:** Deterministik/CI-relevant kontroller: `bib-dup` (semantik), `redundancy` (bölüm
  tekrarı). Alt-komut + exit-code (0 temiz / 1 HARD-deterministik-eşik / 2 SOFT-advisory).
- **Nasıl:** `semantic_core` galileo canlıyken ham cosine; değilken **degrade** → string
  (`bib_hygiene`) + anamnesis sıralı-benzerlik notu (advisory), asla sessiz atlama.
- **Bağımlılık:** `semantic_core`, `bib_hygiene`.

### 4.4 anamnesis (ajan-orkestralı MCP, canlı)
- **Ne yapar:** Retrieval-şekilli semantik işler — ingest + `hybrid_query`/`semantic_search`.
- **Nasıl:** Skill/komut adımlarıyla ajan çağırır; python köprüsünden **çağrılmaz** (MCP protokolü).
- **Bağımlılık:** `ANAMNESIS_MCP_API_KEY` (env), KVKK guard (yalnız literatür/manuskript terimi).

## 5. İki Embedding Şeridi

- **Şerit A · retrieval (anamnesis, ŞU AN canlı):** bulgu↔literatür konumlandırma, bölümler-arası
  benzer-paragraf tespiti, tema↔yapı sıralı eşleme. Sıralı benzerlik skoru = sinyal.
- **Şerit B · ham-vektör (galileo `/embeddings` via `semantic_core`, düzeltme bekliyor):**
  deterministik cosine matrisleri — bib dedup, bölüm-tekrar skoru, tema↔yapı matrisi. Galileo
  düzelene kadar string + anamnesis-sıralı ile **degrade**; düzelince model `.env`'de hazır →
  yeniden kalibrasyon + `live-embedding` bayrağı ile otomatik terfi.

## 6. Judge Uzantıları (galileo gpt-5.4, CANLI) — hepsi SOFT/advisory

| Judge | Ne denetler | Bağlandığı yer |
|---|---|---|
| `claim↔source` (mevcut) | Atıf iddiayı gerçekten destekliyor mu | `/referans-kapisi` |
| `convergence` (yeni) | Joint-display satırı: uyum/tamamlayıcılık/ayrışma/genişleme + aşırı-entegrasyon | karma-sentez |
| `harking` (yeni) | Veri-sonrası prior güçlendirme / ön-kayıt sapması | prior/Tartışma |
| `overclaim` (yeni) | Korelasyon→nedensellik kayması, multiverse cherry-pick | Bulgular/Tartışma |
| `coherence` (yeni) | Tez-geneli amaç↔bulgu↔sonuç zinciri, bölümler-arası anlatı | `/tez-dogrulama` |

`classify_gate` yeni SOFT-block sinyalleriyle genişler; eşikler `.claude/galileo.local.md`.

## 7. Dört Küme × Katman

| Küme | Embedding | Judge (SOFT/advisory) | Kapı |
|---|---|---|---|
| Referans bütünlüğü | bib-dup (Şerit B; **HARD yalnız ≥ kalibre deterministik eşik**) + ledger↔bib uzlaştırma | claim↔source | `/referans-kapisi` |
| Bölüm kalitesi | bölüm-tekrar (Şerit B / anamnesis) | coherence | `/bolum-sertifika` + `/tez-dogrulama` |
| Karma sentez (aktif) | tema↔yapı eşleme (anamnesis / Şerit B) | convergence + aşırı-entegrasyon | karma-sentez dokümanları |
| Yorum disiplini | bulgu↔literatür (anamnesis) | HARKing + overclaim | Tartışma/prior |

## 8. Gate Duruşu (doktrin korunur)

- **HARD (değişmez):** sci-audit yedi eksen + repo hook zinciri + **yalnız** deterministik
  embedding-eşik (bib near-dup ≥ kalibre eşik).
- **SOFT-block (insan-override, kayıtlı):** tüm LLM judge sinyalleri; `certified-final`'i durdurur
  ama override edilebilir (`.claude/galileo.local.md`).
- **advisory:** düşük-riskli sinyaller (tekrar, üslup, sıralı-benzerlik ipuçları).

## 9. Doğrulama ve Kalibrasyon (tam titizlik)

- **`scripts/eval/calib/`** etiketli TR altın setleri: dup/non-dup bib · tekrar/farklı paragraf ·
  yakınsak/ayrışık tema-yapı · grounded/unsupported claim · HARKing/temiz. Eşikler
  `galileo.local.md`'ye işlenir (mevcut `gal_calib` deseni).
- **Eval harness:** `galileo_eval_run` altın-vakalarla genişler → precision/recall + **yanlış-
  pozitif bütçesi** raporu.
- **pytest** her yeni araç için + **köprü parity guard** (`tests/test_zotero_bridge_parity.py`
  deseni; nicel↔nitel köprü kopyaları byte-parity).
- **KVKK testi:** gateway'e yalnız manuskript/lit stringi çıktığını assert et; ham/katılımcı/
  transkript girişini reddet.
- **Degrade testi:** galileo embedding down → `semantic_core` temiz `unavailable`, CLI degrade,
  çökme/yanlış-HARD yok.

## 10. Config & Doküman Güncellemeleri

- `.claude/galileo.local.md`: yeni eşikler (`bib_dup_sim_min`, `redundancy_sim_min`,
  `convergence_*`, `harking_*`, `overclaim_*`) + embedding-durum notu güncelle.
- `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` §embedding şeridi.
- `.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md` §6 (judge uzantıları).
- memory `plugin-tooling-integration`: galileo embedding bozuk-durum + iki-şerit notu.
- `.mcp.json` `galileo-audit` aynı sunucuda yeni araçları expose eder.

## 11. Fazlama

1. **Faz 1 (canlı, hemen):** judge-tarafı uzantıları (tümü canlı) + anamnesis-retrieval kümeleri
   (Yorum disiplini bulgu↔lit, Bölüm kalitesi benzer-paragraf, Karma tema↔yapı sıralı).
2. **Faz 2 (galileo embedding düzelince):** Şerit B ham-vektör deterministik kontroller
   (`semantic_core` + `thesis_semantic` CLI); `live-embedding` bayrağı arkasında, otomatik terfi.
3. **Faz 3:** tam kalibrasyon setleri + eval harness + parity + KVKK/degrade testleri.

## 12. Kapsam Dışı (YAGNI)

- Yerel embedding modeli kurulumu (torch/sentence-transformers) — bağımlılıksız-stdlib doktrini +
  kullanıcı kararı gereği yapılmaz.
- Ayrı `GRAVITEE_AZURE_OPENAI` gateway'i — galileo gateway zaten Azure embedding roster'ını sunar;
  gereksiz.
- IRR/κ metriği olarak judge kullanımı — RTA reddeder (SKILL kural 17); judge yalnız "critical
  friend"/tutarlılık.
- Yeni HARD LLM-gate — doktrin gereği LLM judge asla HARD değildir.

## 13. Açık Bağımlılık

- **Galileo embedding fix (harici):** Şerit B'nin tam gücü, anahtarın `text-embedding-3-large-1`
  deployment'ına doğru bağlanmasına bağlı. Bu düzelene kadar Faz 1 (judge + anamnesis) tam çalışır;
  Şerit B degrade modda kalır.

## 14. Başarı Ölçütü

- Dört küme de en az bir canlı embedding (Şerit A) ve/veya judge sinyaliyle bağlı.
- Judge çıktıları three-tier `classify_gate`'e akıyor; HARD doktrini bozulmuyor.
- Kalibrasyon + eval + pytest + parity + KVKK/degrade testleri geçiyor; yanlış-pozitif bütçesi
  belgeli.
- KVKK invaryantı: gateway'e hiçbir ham/katılımcı verisi gitmiyor (test ile zorlanıyor).

---

## 15. Uygulama Özeti (2026-07-21 — UYGULANDI)

galileo embedding CANLI (Azure `text-embedding-3-large`, `azure-openai` gateway) olduğundan
Faz 1 + Faz 2 birlikte uygulandı:

- **`scripts/eval/semantic_core.py`** (YENİ) — `embed`/`cosine`/`dedup_matrix`/
  `redundancy_pairs`/`match_matrix` + `EmbeddingUnavailable` + KVKK tripwire (TC-kimlik/
  ad-soyad reddi). test: `tests/test_semantic_core.py` (13).
- **`scripts/util/thesis_semantic.py`** (YENİ CLI) — `bib-dup` (semantik near-dup; embedding
  yoksa `bib_hygiene` Jaccard'a degrade) + `redundancy` (bölüm-tekrarı; yoksa `tr_corpus_audit`
  coherence'a yönlendir). Exit 0/1/2; HARD yalnız `--strict` + cosine ≥ `bib_dedup_sim_min`.
  test: `tests/test_thesis_semantic.py` (9).
- **`scripts/eval/galileo_bridge.py`** (GENİŞLETİLDİ) — 4 judge: `galileo_convergence_judge`,
  `galileo_harking_judge`, `galileo_overclaim_judge`, `galileo_coherence_judge`; `classify_gate`
  geriye-uyumlu genişledi; `_GATE_DEFAULTS`'a `harking_min`/`overclaim_min`/`coherence_min`.
  test: `tests/test_galileo_judges.py` (16).
- **`scripts/util/karma_ledger_check.py`** (GENİŞLETİLDİ) — `--semantic` substring-drift rescue
  (parafraz-sadık=INFO; temellendirilmemiş=SOFT; embedding yoksa SOFT+not). Default OFF →
  davranış bit-aynı. test: `tests/test_karma_ledger_check.py` (+4, toplam 12).
- Config/doktrin: `.claude/galileo.local.md` (yeni eşikler + katman notu),
  `manuskript-denetimi-sciaudit.md` (§galileo 13 araç) güncellendi.

**Doktrin korundu:** HARD yalnız sci-audit + repo hook + deterministik embedding-eşik
(bib `--strict`); tüm LLM judge SOFT/advisory (`classify_gate` hard=[] her zaman). KVKK:
gateway'e yalnız manuskript/literatür; `semantic_core` tripwire ham-veri imzasını reddeder.

**Faz 3 (açık iş):** etiketli TR altın kalibrasyon setleri (`scripts/eval/calib/`) + eval-harness
precision/recall + yanlış-pozitif bütçesi + köprü parity guard. Mevcut eşikler
gemini-embedding-001 kalibrasyonundan miras (3-large de 3072-boyut → yaklaşık korunur);
backend değişimi sonrası yeniden-kalibrasyon önerilir.
