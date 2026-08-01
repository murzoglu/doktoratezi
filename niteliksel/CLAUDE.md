# CLAUDE.md — T1DM Niteliksel

> **Migrasyon notu:** Nitel kol içeriği tek-repo çalışma modeli için karma tez
> reposunun kök `niteliksel/` alt-ağacına taşınmıştır. Bu alt-ağaç yeni canonical
> çalışma konumudur; ayrı bağımsız nitel kol artık yoktur. Nicel kol ve genel
> proje bağlamı için repo kökü ([`../CLAUDE.md`](../CLAUDE.md)) esastır.

Tip 1 Diyabet & Ebeveynlik Tutumu doktora tezinin **niteliksel kolu**. Yazılım
projesi değil — nitel araştırma korpusu, analiz tabloları, tez/makale taslakları
ve belge-işleme araçları. Detaylı repo rehberi: `00_context/REPO_CONTEXT.md`.
Ajan rehberi: `AGENTS.md` · AI-reliability sözleşmeleri: `CONVENTIONS.md` ·
Codex operasyon: `00_context/CODEX_PLAYBOOK.md` ·
**Claude Code zorunlu talimatname: `00_context/TALIMATNAME_TEZ_YAZIM.md`** ·
Araç ekosistem haritası: `00_context/TOOL_ECOSYSTEM_MAP.md`.

## ⚠️ Veri gizliliği (her şeyden önce)
- Ham görüşme metinleri özel nitelikli **sağlık + çocuk** verisidir (KVKK).
  Yönetim planı: `01_raw_data/ethics_protocol/kvkk_data_management_plan.md`.
- Ham katılımcı metnini alıntılama/dışa aktarma — yalnızca bilinçli seçilmiş,
  aile/rol koduyla anonimleştirilmiş alıntılar.
- İsim, doğum tarihi, adres, imzalı onam metni veya aile-düzeyi demografik
  satırları **memory'ye yazma**. Raporlamada aile numarası + rol etiketi kullan.

## Proje kimliği
- Tasarım: nitel tanımlayıcı + fenomenolojik duyarlılık, multi-informant
  **triad** (anne + T1DM'li çocuk + sağlıklı kardeş), Braun-Clarke refleksif
  tematik analiz (RTA), COREQ-uyumlu.
- Örneklem (niteliksel kol): **7 aile × 3 = 21 görüşme**.
  Aile kodları: 011, 014, 019, 020, 026, 201, 202.
- ⚠️ Bu **niteliksel** koldur (7 aile). Karma tezin **nicel** kolu ayrıdır
  (241 aile, R pipeline) → `t1dm-tez-rehberi` skill. İkisini karıştırma.

## Skill koordinasyonu
- `niteliksel-arastirma-rehberi-t1dm` — RTA, codebook, COREQ/SRQR/JARS-Qual,
  KVKK/etik, refleksivite, jüri savunması. **Niteliksel iş için birincil.**
- `t1dm-tez-rehberi` — karma tezin nicel R pipeline'ı + tez yazımı (Quarto/APA).
  Karma yapı gerektiğinde koordine et.

## MCP koordinasyonu
- Her tez yazım oturumu `./dmnitel route-tool --query "<soru>"` ve
  `./dmnitel ai-context` ile başlar; Anamnesis/context yalnız anonim/türetilmiş
  karar bağlamı için kullanılır.
- Literatür ve citation işleri: Evidentia v1.7.0 `medical-research` v8.5.0
  native-first hattıyla kaynak bul (web/OSINT fallback yok; bulunamayan kaynak
  gap olarak yazılır); PubMed/EPMC, OpenAlex/S2, Paper Search, YÖK ve RAG
  katmanları bu hat içinden kullanılır. Anna's Library/annas-reader copyright-gated
  tam metin fallback'idir; Zotero ile item key, BibTeX key ve `references.bib`
  mutabakatı yap.
- YÖK/akademik bağlam: `yoktez-mcp`, `yok-akademik` ve eğitim/okul özelinde
  `eric-mcp` koşullu kullanılır.
- KVKK, etik kurul veya sağlık mevzuatı: `mevzuat` ve `mevzuat-bilgisi`
  yalnız resmi madde doğrulaması için kullanılır; hukuki yorum üretilmez.
- Klinik terminoloji/ilaç/regülasyon: `openfda`, `med-terminologies`,
  `nlm-rxnorm`, `nih-clinicaltables`, `iuphar-gtopdb`, `drugddx` ve
  `titck-cache` yalnız tez terminolojisi ve kaynak doğrulaması için kullanılır.
- Render/GitHub/teknik teslim: `playwright`, `chrome-devtools`, `brave-search`,
  `github` ve `filesystem` yalnız açık teknik görevde kullanılır; raw data ve
  credential dosyaları açılmaz.
- Kod arama: `sourcegraph` MCP (dış/açık kaynak kod) + `serena` (yerel toolkit
  sembol). Sourcegraph token'ı yalnız `doppler run -p cureohub -c dev_personal
  -- claude` oturumunda yüklüdür; ⚠️ repo içeriği/nitel veri Sourcegraph
  sorgusuna asla yazılmaz. Detay: `00_context/TOOL_ECOSYSTEM_MAP.md` §6d.
- Manüskript adli denetimi ve Türkçe bilimsel yazım/imla:
  `sci-audit@cureonics-marketplace` v0.2.0 kullanılır. Kapı 4
  `/sci-audit:check-turkish`, Kapı 5 `/sci-audit:audit` +
  `/sci-audit:audit-report`; eski repo-local `tr_sciaudit.py` scaffold'u
  yeniden kurulmaz. KVKK/ham veri/quote-parity denetimi sci-audit kapsamında
  değildir, `dmnitel` + repo ai-audit katmanında kalır.
- `firebase`, `supabase`, `cloudflare-api`, `figma` ve OpenAI API key akışları
  tez yazımı için default değildir; yalnız açık platform/tasarım/API görevi
  varsa kullanılır.

## Kanonik aktif dosyalar

> ⚠️ **Kanon güncellemesi (2026-07-29, Task 1.4):** `new/` kanonu v2.0'ı geçersiz
> kılar. Eski `qualitative_canonical_results_report.md` ve `codebook_v2.md` dosyaları
> `archive/2026-07-29_pre_new_canon/` altına taşınmıştır (silinmemiş, git geçmişi korunuyor).
> Fark özeti: `03_analysis/reconciliation_v2_to_v3.md`.

- Temizlenmiş nitel tez metni:
  `02_processed/cleaned_text/thesis_qualitative_cleaned_current.md`
- Birleşik transcript: `02_processed/transcripts/all_transcripts_merged.md`
- **Kanonik codebook (v3.0): `03_analysis/codebook/codebook_v3.md`**
  (24 kod × 8 triadik eksen × 4 makro tema; v2.0 → arşivde).
  Destekleyen: `03_analysis/codebook/theme_architecture_v3.md` (4 makro / 17 alt + 8-eksen Rosetta).
- **Triadik ham veri:** `new/triadik_matris_extracted.csv`
  (aile_no · rol · triadik_eksen · verbatim_tr; KVKK — repo dışına çıkmaz).
- Methodology paketi: `03_analysis/methodology/` (COREQ, audit trail,
  positionality OM/BA, LLM beyanı, savunma argümanları — v2.0'dan korundu).
- Arşiv: `archive/2026-07-29_pre_new_canon/` (qualitative_canonical_results_report.md +
  codebook_v2.md — yalnız tarihsel başvuru).
- Canlı durum: `00_context/TRACKER.md` · Yol haritası: `00_context/ROADMAP_v1.md`.

## Tema yapısı (karıştırma)
- **Tez** = **4 makro tema**. **Journal** = **6 tema**. Değiştirilebilir değil —
  yeniden yazımdan önce hedef çıktıyı netleştir.

## İş akışı durumu
- Faz A (Kalite Pekiştirme) ✅ tamam.
- Bundan sonraki tez yazım sürecinin ana operasyon merkezi:
  `/workspaces/T1DM-Tez/tez-yazim`.
- Bu kol (niteliksel/) tez yazımında yalnız nitel kolun ilişkili kesimleri için açılır:
  RTA/COREQ, audit trail, triadik tema kanıtı, seçilmiş anonim alıntı denetimi
  ve kanonik nitel sonuç raporu kontrolü.
- Tez yazımında nitel kolu temsil eden ana aktarım kaynağı, nicel köke
  taşınmış kanonik nitel sonuç raporudur; ham transcript veya geniş
  nitel kol yeniden taraması varsayılan değildir.

## Claude Code katmanı (zorunlu)
- Tez yazımı, nitel kanıt, referans veya karma sentez içeren HER işte
  `00_context/TALIMATNAME_TEZ_YAZIM.md` **bağlayıcıdır** — önce onu uygula.
- Deterministik zorlama devrededir: `.claude/settings.json` `permissions.deny`
  (ham veri + credential Read/Edit kapalı) ve `.claude/hooks/` beşlisi
  (SessionStart konvansiyon enjeksiyonu, prompt sır taraması, Bash deny-list,
  çıktı incelemesi, kaynaksız-sayı Stop kapısı). Codex ikizi: `.codex/hooks/`.
  Politika değişirse iki ağaç + `tests/test_claude_hooks.py` birlikte güncellenir.
- Slash komutlar: `/tez-oturum` (oturum ritüeli), `/nitel-dogrulama` (kapanış
  doğrulama paketi), `/capraz-repo` (karma köprü), `/referans-kapisi`
  (6-adımlı citation kapısı), `/ai-kayit` (LLM kullanım günlüğü).

## Araçlar & gotcha'lar
- AI-reliability altyapısı: `reliability/` (evals / redteam / verify),
  `governance/` (NIST–ISO 42001 eşlemesi), `plugins/t1dm-qual-ai-audit`
  (referanslı bölüm değişikliklerinde zorunlu denetim kapısı — CONVENTIONS §14).
- **Yerel toolkit** `dm_niteliksel_toolkit/` → `./dmnitel <komut>` (harici API yok;
  ham veri connector'a gitmez). Komutlar: `init`, `ai-context`, `route-tool`,
  `cross-repo-status`, `lint-codebook`, `build-triadic-matrix`, `check-quotes`,
  `audit-coreq`, `find-negative-cases`, `log-ai-use`. Tam kullanım: `README.md`.
- Test: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`
  (toolkit kodu değişince önce ilgili dar test, sonra tümü).
- Toolkit çıktı dizinleri: `07_reports/`, `04_triadic_matrices/`,
  `06_manuscript_outputs/`, `99_ai_use_log/`.
- Eski scriptler: `06_tools/scripts/*.py` (docx→markdown, transcript standardizasyon).
- ⚠️ `python-docx` kurulu **değil** — DOCX scriptlerinden önce `pip install python-docx`.
- ⚠️ Birkaç eski script hedef Markdown'ı **üzerine yazar** — çalıştırmadan önce yedek
  al / `00_context/file_manifest_after_reorg.tsv` kontrol et.
- `06_tools/legacy_windows/` — Windows-path scriptleri; yeniden kullanımdan önce
  parametrele.

## Oturum sürekliliği
- Handoff buffer: `.remember/now.md`. Geçmiş: `.remember/` (recent / archive /
  today-*.done). ⚠️ `.remember/` KVKK kapsamındadır — memory'ye/harici MCP'ye taşıma.
