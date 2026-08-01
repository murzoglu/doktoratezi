# Kalite-Kontrol Sistemi ve İyileştirmeler — Oturum Raporu

**Tarih:** 2026-07-22
**Kapsam:** Cureonics plugin/MCP kurulumu → tez QC mimarisi süreç etüdü → QC otomatik-zorlama + kapsam genişletme → **Minerva tam-metin kaskad entegrasyonu**
**Repo:** T1DM-Tez (Quarto + R doktora tezi)
**İlgili plan:** [`docs/superpowers/plans/2026-07-22-qc-otomatik-zorlama.md`](../plans/2026-07-22-qc-otomatik-zorlama.md)
**Commit:** QC katmanı `feat/qc-otomatik-zorlama-kapsam` dalı, `d35cf6a` (18 dosya, +1715/−24). **Minerva entegrasyonu (§8) bu commit'ten SONRA yapıldı ve HENÜZ commit edilmedi** (çalışma ağacında).

---

## 1. Yönetici Özeti

Bu oturumda üç iş yapıldı:

1. **Altyapı kurulumu:** `mahirkurt/CureoPrivate` plugin-marketplace'i klonlandı; `evidentia` (24 MCP) ve `sci-audit` (7 eksen + galileo) plugin'leri MCP'leriyle birlikte kuruldu/aktifleştirildi.
2. **Süreç etüdü:** Tez yazım sürecinin tüm QC mekanizmaları (araç/hook/script/komut/MCP) haritalandı; 12 kümede **217 mekanizma** çıkarıldı, 5 lensli çekişmeli açık-avıyla QC-atlama yüzeyleri tespit edildi.
3. **İyileştirme:** Etüt bulgularına göre QC **otomatik-ateşlenir** ve **tüm-gövde-kapsamlı** hâle getirildi — kapı sayısı **28 → 38**, TDD ile, iki hook ağacı senkron.

**Temel bulgu:** QC mimarisi *tasarımda* kapsamlı ama *icrada* neredeyse tamamen elleydi (217 mekanizmanın %66'sı manuel/advisory; turn-end'de otomatik ateşlenen tek kapı `stop_verify`'dı). İyileştirmeler bu boşluğu — kapsamı değil, **zorlama ve otomatik-ateşlemeyi** — hedefledi.

---

## 2. Kurulan Altyapı (Plugin + MCP)

### 2.1 Marketplace + Plugin'ler
- **Klon:** `CureoPrivate` → `/workspaces/CureoPrivate` (kardeş dizin; PAT `.env`'den okundu, ekrana basılmadı, remote token'dan arındırıldı).
- **Marketplace:** `cureonics-marketplace` yerel dizin olarak Claude Code'a eklendi.
- **Kurulan plugin'ler** (user scope, `✔ enabled`):
  - `evidentia` v2.3.2 — genel-amaçlı tıbbi literatür/kanıt motoru (PRISMA + full-text kaskadı + RAG).
  - `sci-audit` v0.2.1 — LLM-üretimi bilimsel metin adli/dilsel denetçisi (7 eksen).

### 2.2 MCP sunucuları (hepsi `✔ Connected`)
- **evidentia (20 sunucu):** anahtarsız çekirdek (pubmed-epmc, openalex, semantic-scholar, med-terminologies, nih-clinicaltables, nlm-rxnorm, iuphar-gtopdb, pophive, who-gho, globocan, ema, mevzuat-bilgisi, titck-cache, drugddx) + anahtarlı altılı (yok-akademik, openathens, annas-reader, anamnesis, openfda, evidentia-kb).
- **sci-audit:** `pubmed` (claude.com) + paylaşılan üç uç (dedup ile evidentia namespace'inden).
- **Anahtar kaynağı:** [`MCP-TALIMATLAR.md`](../../../MCP-TALIMATLAR.md) doğrulandı; ortamdaki `.env` altı anahtarı zaten sağladığından `${...}` env-expansion ile hepsi elle enjeksiyonsuz bağlandı.
- **Proje-kapsamlı MCP onayı:** `minerva-evidence`, `galileo-audit`, `zotero-refs`, `openathens`, `annas-reader` → `enabledMcpjsonServers` içinde açıkça onaylandı (yerel `settings.local.json`, commit-dışı).

---

## 3. Süreç Etüdü — Bulgular

**Yöntem:** 12-küme paralel haritalama + 5-lens çekişmeli gap-avı (17 alt-ajan iş akışı) + 3 kritik iddianın dosyadan bizzat doğrulanması.

### 3.1 Nicel tablo (217 mekanizma)
| Zorlama | Sayı | | Entegrasyon | Sayı |
|---|---|---|---|---|
| HARD-block | 43 | | fully-integrated | 97 |
| SOFT-block | 21 | | partial | 83 |
| advisory | 65 | | orphan | ~34 |
| manual | 79 | | unclear | 3 |
| none | 9 | | | |

→ **Diş taşıyan (HARD+SOFT): 64/217 (%29). Atlanabilir (manuel+advisory): 144/217 (%66).**

### 3.2 Doğrulanmış kritik açıklar
- **A —** 28-madde ana kapısı (`tez_checklist_verify.py`) hiçbir hook/pre-commit/Stop'a bağlı değildi (manuel-only). ✅ dosyadan doğrulandı.
- **B —** Bulgular bölümünün (`04_bulgular.qmd`) kendi sayıları hiçbir sert kapıdan geçmiyordu (`csr_numeric_trace` varsayılanı CSR; `r_generator_literal_audit` `SCAN_DIRS=["R","scripts/R"]`). ✅
- **C —** `references.bib`'e yazma-zamanı kapısı yoktu; DOI yanlış-atıf/tam-metin doğrulama araçları orphan.
- **D —** "Zorunlu/kanonik" Türkçe-yazım Ekseni G (`tr_sciaudit`) 28-madde pakette değildi.
- **E —** `--fast` kapanışı render/PDF/renv/targets kapılarını sessizce SKIP ediyordu.
- **F —** Bölüm sertifikası güvene dayalıydı; sertifikadan sonra değişen bölüm sessizce eskiyordu.
- **G —** En derin cross-document QC (galileo overclaim/HARKing/convergence/coherence) yalnız opt-in koşuyordu.
- **H —** Nedensel dil yalnız CSR'de; karma joint-display sözlüğü 2 bölüm × 6 satır; PII taraması kolon-adı + bölüm-dar.

---

## 4. Yapılan İyileştirmeler

QC kapısı **28 → 38**. Tüm eklemeler TDD (RED→GREEN) ile ve iki hook ağacı (Claude + Codex ikizi) senkron tutularak yapıldı.

### 4.1 Otomatik-ateşleme (etüt madde A, C, E, F)
| Mekanizma | Ne yapar | Dosya |
|---|---|---|
| `--closing` modu | Teslim koşumunda `--fast` reddedilir; eksik araç/CSR SKIP yerine FAIL (gate-presence invariant) | `tez_checklist_verify.py` |
| Stop §1.4 blocker | Turn-end'de nokta-ondalık `p=0.NNN` bloklanır (Marmara ondalık virgül) | `.claude/hooks/stop_verify.py` + `.codex/` ikizi |
| references.bib yazma kapısı | `Write\|Edit` → references.bib düzenlenince `bib_hygiene` HARD ise turn-içi bloklar | `post_tool_use_review.py` (ikiz) + `settings.json` + `.codex/hooks.json` |
| pre-commit kurucu | `chapters/*.qmd`/`references.bib` staged commit'te ana checklist'i çalıştırır, FAIL'de durdurur (opt-in, `--no-verify` bypass) | `scripts/util/install_git_hooks.sh` |

### 4.2 Kapsam genişletme (etüt madde B, D, H)
| ID | Kapı | Yeni denetçi |
|---|---|---|
| **K0-PII-03** | Değer-şekilli PII (11-hane TC, gg.aa.yyyy doğum tarihi, hasta/protokol no, telefon) tüm manuskript | `pii_value_scan.py` |
| **K5-NUM-03** | ch04 Bulgular kendi sayıları → CSV izi (kaynak-tekilliği) | `csr_numeric_trace_audit.py --csr chapters/04_bulgular.qmd` |
| **K5-CAU-02** | ch05 Tartışma nedensel dil + etiket disiplini | `csr_causal_label_audit.py --csr chapters/05...` |
| **K5-LIT-01 (genişletildi)** | Artık `chapters/*.qmd` inline `{r}` chunk'larını da tarar | `r_generator_literal_audit.py --include-chapters` |

### 4.3 Orphan bağlama (etüt madde D, F, C)
| ID | Kapı | Denetçi |
|---|---|---|
| **K5-TRK-01** | `_targets.R` `format="file"` dosya-izleme (Kaide-2) | `targets_file_tracking_audit.py` (yeni) |
| **R-SVG-01** | librsvg (`rsvg-convert`) render önkoşulu — SVG boş-rasterize koruması | inline |
| **K4-TRG-01** | Türkçe bilimsel-yazım Ekseni G çekirdeği (G1-G6, nokta-ondalık-p) | sci-audit `tr_sciaudit.py` |
| **K1-DOI-01** | DOI↔Crossref başlık eşleşmesi (yanlış-atıf) — `--closing`/ağ-bağımlı, SKIP-dostu | `doi_title_resolve.py` |

### 4.4 Derin katman + teslim (etüt madde F, G)
| ID | Kapı | Not |
|---|---|---|
| **K1-KAR-01** | Karma cross-arm aşırı-iddia yok (bir kol diğerini "doğrular" değil) | `cross_arm_rhetoric_audit.py` (yeni) |
| **T-CERT-01** | Bölüm sertifika tazeliği (bölüm sertifikadan sonra değişmemiş) | path bug'ı düzeltildi (gerçek dizin: `tez-yazim/04_kalite-kontrol/sertifikalar/`) |
| **K5-GAL-01** | Galileo tam-tez judge koşumu güncel (advisory; HARD asla judge'dan gelmez) | `run_full_thesis_judge.py --out` artefaktı |

**Galileo zorunlu-assembly:** `bolum-sertifika.md` Kapı 3/4 — galileo dörtlüsü (convergence/harking/overclaim/coherence) her içerik bölümü + joint-display satırı için zorunlu; eşik-üstü SOFT-block bulgusu Gap Register'a **yazılı gerekçe** düşülmeden `certified-final` yazılamaz (gerekçesiz = en fazla `provisional-pass`).

### 4.5 TDD sırasında yakalanıp düzeltilen yanlış-pozitifler
Kapıların meşru içerikte spurious FAIL üretmemesi için 4 FP giderildi:
1. **PII —** çalışma tarihi (etik onayı 11.05.2023) doğum tarihi sanılıyordu → yalnız doğum-bağlamlı tarih işaretlenir.
2. **PII —** yüksek-hassasiyet ondalık (3951.12345678901) 11-hane TC sanılıyordu → ondalık-nokta komşuluğu hariç.
3. **cross-arm —** olumsuz disiplin beyanı ("…doğrulayan olarak değil") işaretleniyordu → `değil`/olumsuz-fiil hariç.
4. **cross-arm —** Türkçe isim/fiil homografı (`kanıt`ların ≠ `kanıtla`mak) → yalnız açık fiil çekimleri.

---

## 5. Doğrulama Sonuçları

| Kontrol | Sonuç |
|---|---|
| `tez_checklist_verify.py --audit-doc` | **SENKRON (38 ID belge↔script birebir)** |
| `tests/test_qc_coverage.py` | **26/26 PASS** |
| `tests/test_claude_hooks.py` | **19/19 PASS** |
| K5-HOK-01 (iki-kol hook parite) | **PASS** |
| `tez_checklist_verify.py --fast` (38 madde) | **0 FAIL** (27 PASS / 6 SKIP-ağır / 5 MANUEL) |

Yeni denetçiler salt-okuma ve KVKK-uyumlu (yalnız metin/metadata; `data/raw|identified|cleaned|backup` ve satır-düzeyi `data/processed`/`outputs` okunmaz).

---

## 6. Eklenen/Değişen Dosyalar (18)

**Yeni:**
- `scripts/util/pii_value_scan.py`
- `scripts/util/targets_file_tracking_audit.py`
- `scripts/util/cross_arm_rhetoric_audit.py`
- `scripts/util/install_git_hooks.sh`
- `tests/test_qc_coverage.py`
- `docs/superpowers/plans/2026-07-22-qc-otomatik-zorlama.md`

**Değişen:**
- `scripts/util/tez_checklist_verify.py` (10 yeni kontrol + `--closing`)
- `scripts/util/r_generator_literal_audit.py` (`--include-chapters` + `--paths`)
- `scripts/eval/run_full_thesis_judge.py` (`--out`)
- `.claude/hooks/stop_verify.py` + `.codex/hooks/stop_verify.py`
- `.claude/hooks/post_tool_use_review.py` + `.codex/hooks/post_tool_use_review.py`
- `.claude/settings.json` + `.codex/hooks.json`
- `.claude/commands/bolum-sertifika.md`
- `tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md`
- `tests/test_claude_hooks.py`

---

## 7. Kalan / Sıradaki

- **Tamamlanmamış iş yok** — planın P0–P3'ü + iki ertelenen kalem (K1-DOI-01, galileo) + `r_generator` inline-chunk uzantısı bu oturumda kapandı.
- **Opsiyonel operasyonel adımlar:**
  - `feat/qc-otomatik-zorlama-kapsam` dalını `origin`'e push + PR (dışa aktarım → kullanıcı onayı gerekir).
  - Galileo tam-tez judge'ı bir kez koşup artefakt üretmek (`run_full_thesis_judge.py --out outputs/reports/galileo_full_thesis_judge.json`) → K5-GAL-01 PASS'a geçer.
  - Sertifikaları güncellemek (6 bölüm sertifikadan sonra değişmiş, 2 sertifikasız → T-CERT-01 MANUEL).
  - `--closing` modunda tam kapanış koşumu (ağ + ağır kapılar dahil) teslim öncesi.

---

## 8. Minerva Tam-Metin Entegrasyonu (parite tamam)

**Sorun (etüt sonrası tespit):** Roche Minerva tam-metin özellikleri evidentia D2/D4 doktrininde tanımlıydı ve MCP köprüsü canlıydı, ama tam-metin kaskadının deterministik yardımcısı (`fulltext_cascade.py`) ile Marmara-tarafı belgelerinde (kanonik kaskad, referans-kapısı) Minerva **atlanabiliyordu** — OpenAthens ve annas-reader ile paritede değildi.

**Yapılan — üç kaynak (OpenAthens · Minerva · annas-reader) tam parite:**

1. **Kod** ([`scripts/mcp/fulltext_cascade.py`](../../../scripts/mcp/fulltext_cascade.py)):
   - `StdioMcp` sınıfı (HTTP `HttpMcp` yüzeyiyle aynı) — Minerva stdio köprüsünü spawn eder, initialize + tools/call.
   - `try_minerva`: DOI → vectorstore tam metni (`minerva_literature_fulltext_by_doi`), boş/hatalıysa rominedb yedeği (`minerva_rominedb_get_article`); **annas ÖNCESİ** kademe.
   - **Parite sertleştirmesi (adversarial re-verify sonrası):** üç FETCH kaynağı (openathens/minerva) ortak `_fulltext_ok` yordamı (aynı hata-dedektörü + asgari-uzunluk eşiği); `StdioMcp` `select` ile `TIMEOUT`'lu; GRAVITEE kimlik yoksa **spawn'sız kısa-devre** (`_gravitee_present`, openathens/annas token-simetrisi).
   - Varsayılan `--tier`: `pubmed,openathens,minerva,annas`.
2. **Dokümanlar (5, tam senkron):** [`tam-metin-erisim-kaskadi.md`](../../../tez-yazim/00_kaynak-kurallari/tam-metin-erisim-kaskadi.md) (§T1.5 Minerva kapısı), [`referans-kapisi.md`](../../../.claude/commands/referans-kapisi.md) (Adım 3), [`yetkinlik-ve-arac-mimarisi.md`](../../../tez-yazim/01_mimari/yetkinlik-ve-arac-mimarisi.md) (L3 + madde 9 + yetkinlik tablosu + çıkış kriteri), [`evidentia-entegrasyon-cercevesi.md`](../../../tez-yazim/01_mimari/evidentia-entegrasyon-cercevesi.md) (§4 özet + tükenme kuralı), `literatur-kanit-evidentia.md` (§0.3 D4, §0.5 kademeli sıra, §0.7 tablo, §2 özet, access_route enum). Tüm kaynaklarda **sıra tutarlı**: OpenAthens → Minerva → annas.
3. **KVKK/güvenlik:** gateway'e yalnız DOI/başlık gider; GRAVITEE anahtar değeri asla yazılmaz; tam metin anamnesis'e ingest (teze verbatim kopya yok). Testlerle kilitlendi.

**Doğrulama:**
- TDD: [`tests/test_fulltext_cascade.py`](../../../tests/test_fulltext_cascade.py) **7/7** (sahte stdio-köprü fixture; ok/err/bridge-missing/no-leak/args-whitelist/preflight).
- **Canlı:** gerçek köprüyle DOI `10.1038/s41586-020-2649-2` → **24.691 karakter tam metin** (`ok:True, source:vectorstore`); üç tier birlikte canlı `ok=True`; korpus 25.155.544 makale.
- **İki turlu adversarial doğrulama iş akışı** (parite / doküman-kod senkronu / KVKK): 1. tur 10 bulgu (0 high) → düzeltildi; 2. tur KVKK **PARITY-COMPLETE**, kalan doküman-senkron/parite düşük bulguları da kapatıldı.

**By-design (bilinçli değiştirilmedi):** Köprünün tam-metni tam döndürmesi **anamnesis-ingest tasarımıdır**; verbatim-teze-kopya yasağı kullanım doktriniyle (RBŞ) yönetilir — köprüyü cap'lemek ingest akışını kırardı.

## 9. Fonksiyonel Durum — "her şey işlevsel mi?" → EVET (2026-07-22)

Uçtan uca fonksiyonel smoke (bu oturum sonu):

| Kontrol | Sonuç |
|---|---|
| Python derleme (12 yeni/değişen script) | ✅ 12/12 OK |
| `tests/test_fulltext_cascade.py` | ✅ 7/7 |
| `tests/test_qc_coverage.py` | ✅ 26/26 |
| `tests/test_claude_hooks.py` | ✅ 19/19 |
| `tez_checklist_verify.py --audit-doc` | ✅ SENKRON (38) |
| `tez_checklist_verify.py --fast` (38 madde) | ✅ 0 FAIL (27 PASS / 6 SKIP-ağır / 5 MANUEL) |
| İki-kol hook paritesi (K5-HOK-01) | ✅ PASS |
| pre-commit kurulu + installer sözdizimi | ✅ |
| Plugin MCP (evidentia + sci-audit) bağlı | ✅ 21 sunucu Connected |
| Minerva köprü canlı (stats) | ✅ 25.1M makale |
| Tam-metin kaskadı 3 tier canlı | ✅ openathens/minerva/annas `ok=True` |

**Sonuç:** Tüm otomatik kapılar ve tam-metin kaynakları işlevsel; FAIL yok. Elle doğrulama gerektiren kalemler yalnız tasarımca-MANUEL (KVKK fotoğraf, yer-tutucu, retorik, sertifika tazeliği) ve ağır-SKIP (render/PDF/renv/targets `--fast`'te) maddeleridir — bunlar bozukluk değil, kapsam-dışı/ön-koşul durumudur.

---

*Bu rapor bir dokümantasyon artefaktıdır; sır/veri içermez. Kanonik kural tanımlamaz — kural otoriteleri `AGENTS.md`, `talimatname-claude-code.md`, `tez-kontrol-checklisti.md` ve script kaydıdır.*
