# CLAUDE.md — T1DM Niteliksel

> **Migrasyon notu (2026-07-09):** Nitel repo içeriği tek-repo çalışma modeli için
> `/mnt/thunderbolt/workspaces/doktoratezi/niteliksel` altına taşınmıştır.
> Bu alt-ağaç yeni canonical çalışma konumudur; eski bağımsız repo silinmemiştir.

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
- Temizlenmiş nitel tez metni:
  `02_processed/cleaned_text/thesis_qualitative_cleaned_current.md`
- Birleşik transcript: `02_processed/transcripts/all_transcripts_merged.md`
- **Güncel codebook: `03_analysis/codebook/codebook_v2.md`**
  (23 kod × 6 journal tema × 4 tez makro tema; v1 superseded).
  ⚠️ `codebook_v3.csv` bir Faz B **draft**'tır — v2 hâlâ kanonik.
- Methodology paketi: `03_analysis/methodology/` (COREQ, audit trail,
  positionality OM/BA, LLM beyanı, savunma argümanları).
- Canlı durum: `00_context/TRACKER.md` · Yol haritası: `00_context/ROADMAP_v1.md`.

## Tema yapısı (karıştırma)
- **Tez** = **4 makro tema**. **Journal** = **6 tema**. Değiştirilebilir değil —
  yeniden yazımdan önce hedef çıktıyı netleştir.

## İş akışı durumu
- Faz A (Kalite Pekiştirme) ✅ tamam.
- Bundan sonraki tez yazım sürecinin ana operasyon merkezi:
  `/mnt/thunderbolt/workspaces/doktoratezi/tez-yazim`.
- Bu repo tez yazımında yalnız nitel kolun ilişkili kesimleri için açılır:
  RTA/COREQ, audit trail, triadik tema kanıtı, seçilmiş anonim alıntı denetimi
  ve kanonik nitel sonuç raporu kontrolü.
- Tez yazımında nitel kolu temsil eden ana aktarım kaynağı, doktoratezi
  reposuna taşınmış kanonik nitel sonuç raporudur; ham transcript veya geniş
  nitel repo yeniden taraması varsayılan değildir.

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
