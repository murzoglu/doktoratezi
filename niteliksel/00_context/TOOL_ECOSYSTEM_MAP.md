# Araç Ekosistem Haritası — T1DM Karma Tez Yazım Süreci

Sürüm: 1.3 · 2026-07-08 · Kapsam: iki repo (`T1DM Niteliksel` + `doktoratezi`),
iki harness (Claude Code + Codex CLI). Operasyonel kurallar için:
`00_context/TALIMATNAME_TEZ_YAZIM.md` (Claude) · `00_context/CODEX_PLAYBOOK.md` (Codex).

v1.3 değişikliği: `sci-audit@cureonics-marketplace` v0.2.0 doktoratezi
`tez-yazim` Kapı 4/5 kurallarına göre kanonik manüskript adli denetimi ve
Türkçe bilimsel yazım/imla katmanı olarak benimsendi. Eski repo-local
`tr_sciaudit.py` scaffold'u kullanılmaz; KVKK/ham veri/quote-parity repo
ai-audit katmanında kalır.

v1.2 değişikliği: Claude Code'daki `evidentia` plugin v1.7.0 ve flagship
`medical-research` v8.5.0 temel alındı: native-first, no-web/OSINT tier,
semantic coverage, retrieve-don't-dump ve clean-copy sözleşmesi eklendi.
`psyarxiv-osf` proje config'i hazır ama endpoint 404 bloklu; fallback
`Paper Search` + `openalex`.

v1.1 değişikliği: iki rehber skill (`niteliksel-arastirma-rehberi-t1dm`,
`t1dm-tez-rehberi`) ile Evidentia çekirdeği arasındaki entegrasyon açıkça
haritalandı (Bölüm 3a). Skill'lerin iç kanıt köprüsü:
`niteliksel-arastirma-rehberi-t1dm/references/13-mcp-ve-skill-baglantilari.md`
ve `t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`.

Durum etiketleri: **✅ bağlı** (Claude oturumunda hazır) · **🔶 koşullu**
(yalnız görev sinyaliyle açılır) · **🧩 Codex-yanı** (bu harness'ta bağlı değil)
· **⛔ default-off** (tez süreci dışı).

## 1. Katman şeması

```
Kullanıcı görevi
  └─ Talimatname + CLAUDE.md/AGENTS.md/CONVENTIONS.md   (model-düzeyi kurallar)
      └─ Hook katmanı (.claude/hooks ↔ .codex/hooks)     (deterministik kapılar)
          └─ Yerel toolkit (./dmnitel, zotero bridge)     (KVKK-güvenli yerel iş)
              └─ Skill/komut katmanı (/tez-oturum, rehber skiller)
                  └─ Ajan katmanı (distiller/Explore/synthesizer)
                      └─ MCP connector katmanı (kanıt, mevzuat, terminoloji)
```

## 2. Yerel araçlar (her iki harness, birincil)

| Araç | İş | Not |
|---|---|---|
| `./dmnitel ai-context` | Repo-özel güvenli tool-bridge özeti | Oturum ritüelinin 1. adımı (`/tez-oturum` içinde otomatik) |
| `./dmnitel route-tool --query` | Yerel nitel / dış kanıt / nicel-karma rota kararı | Belirsiz her işte önce bu |
| `./dmnitel cross-repo-status` | Karma tez iki-repo köprü raporu | Çıktı: `07_reports/cross_repo_thesis_bridge_status.md` |
| `./dmnitel lint-codebook` | Codebook CSV tutarlılığı | Kanonik: `codebook_v2.md`; v3.csv draft |
| `./dmnitel build-triadic-matrix` | Anne/T1DM çocuk/kardeş tema matrisi | Çıktı: `04_triadic_matrices/` |
| `./dmnitel check-quotes` | Anonim alıntı bütünlüğü | Transcript'i bağlama açmadan doğrular |
| `./dmnitel audit-coreq` | COREQ 32 madde kanıt denetimi | Yöntem+bulgular metinleri üzerinde |
| `./dmnitel find-negative-cases` | Negatif/alternatif vaka adayları | Tema yorumundan önce |
| `./dmnitel log-ai-use` | LLM/MCP kullanım günlüğü | `99_ai_use_log/ai_use_log.csv`; `/ai-kayit` sarmalar |
| `python3 scripts/util/zotero_env_bridge.py` | Zotero Web API (status/export) | `.env` → `ZOTERO_API_KEY`; anahtar asla yazdırılmaz |
| `python3 .codex/tools/codex_mcp_roster_redacted.py` | Codex MCP roster (token-redakteli) | Ham `codex mcp list` iki harness'ta da yasak |
| `06_tools/scripts/*.py` | DOCX→MD, transcript standardizasyon | `python-docx` gerekir; bazıları hedefi **üzerine yazar** |
| doktoratezi: `Rscript tests/test_*.R`, `targets::tar_make()`, `quarto render` | Nicel pipeline + render | `t1dm-tez-rehberi` skill yönetir |

## 3. Skill katmanı (Claude Code)

| Skill | Tez rolü | Durum |
|---|---|---|
| `niteliksel-arastirma-rehberi-t1dm` | RTA, codebook, COREQ/SRQR/JARS-Qual, KVKK/etik, refleksivite, jüri savunması — **nitel işin birincil kapısı** | ✅ |
| `t1dm-tez-rehberi` | Nicel R pipeline (H1–H5, EMBU/Beck/KİA) + tez yazımı (Quarto/APA); doktoratezi `.claude/skills/` içinde ~25 referans dosyası | ✅ |
| `evidentia` süiti v1.7.0 (`/evidentia`, `evidentia-connectors`, `evidentia-fulltext`, `evidentia-kol`, `evidentia-synthesize`, `medical-research` v8.5.0) | Native-first dış kanıt, semantic coverage, tam metin, KOL ve clean-copy sentez; web/OSINT fallback yok | ✅ (plugin) |
| `sci-audit@cureonics-marketplace` v0.2.0 (`/sci-audit:audit`, `check-turkish`, `audit-report`) | Manüskript adli denetimi axes A-F + Türkçe bilimsel yazım/imla axis G; doktoratezi `tez-yazim` Kapı 4/5 ile çalışır | ✅ (plugin) |
| `carbon-quarto-scientific` | Tez/CSR bölümlerinin Quarto+Carbon PDF/HTML render'ı | ✅ |
| `carbon-html-report` | Düz markdown→Carbon rapor (denetim raporları) | ✅ |
| `deep-research` | Çok-kaynaklı doğrulamalı literatür raporu (fan-out) | ✅ |
| `remember` | `.remember/` oturum devri (KVKK: yerelde kalır) | ✅ |
| `superpowers` süreç skilleri (`brainstorming`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `writing-plans`…) | Süreç disiplini; doğrulama-önce-iddia | ✅ |
| Repo plugin skilleri: `t1dm-qual-ai-audit` (55/55) · `doktoratezi-ai-audit` (142/142) | Repo-bilinçli AI-reliability denetimi; referanslı bölümde **ikisi birlikte** koşulur | ✅ (script olarak) |
| `dataviz`, `mermaid` (connector) | Şekil/diyagram standartları | 🔶 |
| `claude-api`, `update-config`, `skill-creator`, `plugin-dev:*` | Harness bakımı (talimatname/hook geliştirme) | 🔶 |

## 3a. Skill ↔ Evidentia ↔ dmnitel entegrasyonu (üç kollu kanıt hattı)

İki rehber skill ile Evidentia tek entegre hat olarak çalışır. Kanıt her zaman
üç koldan birine düşer; kol seçimi belirsizse önce `./dmnitel route-tool`.

```
Niteliksel/karma soru
  ├─ İç veri (RTA/codebook/COREQ/alıntı/triad) → ./dmnitel + niteliksel-arastirma-rehberi-t1dm
  ├─ Dış literatür/tam metin/citation/KOL      → EVIDENTIA v1.7 / medical-research v8.5 + OA/legal-OA/Paper Search + Anna's + Zotero + ledger
  └─ Nicel/karma köprü (H5, joint display, IRR)→ t1dm-tez-rehberi (paired doktoratezi)
```

| Kol | Birincil kapı | Skill köprü dosyası | KVKK sınırı |
|---|---|---|---|
| İç nitel veri | `./dmnitel` (ai-context, check-quotes, audit-coreq, build-triadic-matrix, find-negative-cases) | `niteliksel-arastirma-rehberi-t1dm/references/13-mcp-ve-skill-baglantilari.md` | Ham veri connector'a **gitmez**; transcript açılmaz |
| Dış literatür | Evidentia (`/evidentia`, `medical-research` v8.5, distiller ajanları) | her iki skill'in reference dosyaları (13… ve `literatur-kanit-evidentia.md`) + plugin `CONNECTORS.md` | Yalnız kamuya açık literatür; PII/transkript/anamnesis'e satır verisi yok; web fallback yok |
| Nicel/karma | `t1dm-tez-rehberi` + `./dmnitel cross-repo-status` | `t1dm-tez-rehberi/references/karma-yontem.md`, `h5-diadik-tutarlilik.md` | doktoratezi korumalı veri sınırı |

Kural: Dış literatür işinde **ham `PubMed`/`Paper Search`/`Consensus`/`YokTez`'e
doğrudan gidilmez** — Evidentia native-first hattı içinden çağrılır; her referans
§5'teki tam-metin+citation kapısından geçer. Skill devir tetikleyicileri ve güncel MCP
adları (eski→yeni: `Hukuki_Veritabanlar→Yarg`, `Mevzuat→Mevzuat_Bilgisi`,
`Sequential_Thinking→sequentialthinking`, `Fetch→WebFetch`) niteliksel skill'in
13 numaralı reference dosyasında tutulur.

## 4. Plugin katmanı (kullanıcı-düzeyi etkin)

Tez sürecinde aktif rol alanlar: `evidentia@cureonics-marketplace` (kanıt
motoru), `sci-audit@cureonics-marketplace` (manüskript adli denetimi + Türkçe
bilimsel yazım/imla), `superpowers` (süreç), `remember` (oturum devri),
`claude-md-management` (CLAUDE.md bakımı), `playwright` (render doğrulama),
`skill-creator`/`plugin-dev` (altyapı bakımı), `sourcegraph`/`serena` (kod arama).
Tez-dışı (⛔ açık istek olmadan kullanılmaz): `firebase`, `cloudflare`,
`firecrawl`, `frontend-design`, `mcp-server-dev`, `mcp-tunnels`, `ralph-loop`,
`github` (yalnız açık GitHub işi), LSP üçlüsü (yazılım işleri).
Repo-yerel plugin kayıtları: `.agents/plugins/marketplace.json` (nitel),
`plugins/doktoratezi-ai-audit` (nicel).

Sci-audit kapsam sınırı: axes A-F referans/claim/istatistik/halüsinasyon/
raporlama-kılavuzu/AI-şeffaflık; axis G Türkçe bilimsel yazım/imla. KVKK,
ham veri, quote-parity ve kanonik kilit denetimi `t1dm-qual-ai-audit`,
`doktoratezi-ai-audit` ve `dmnitel` katmanındadır.

## 5. Ajan katmanı (Agent tool)

| Ajan | Tez rolü |
|---|---|
| `medical-distiller` | Klinik/bilimsel kanıt retrieval'ını ana bağlamdan izole eder; tek damıtılmış zarf döndürür |
| `legal-distiller` | KVKK/mevzuat/etik kaynak taraması (Mevzuat, Yargı, Resmî Gazete) |
| `academic-archival-distiller` | YÖK tez + arşiv/akademik tarama |
| `evidentia:evidence-synthesizer` | Çok-eksenli ağır kanıt sentezi (D0–D6 tam koşum) — bağlam ekonomisi gerektiğinde |
| `Explore` | Repo/dosya keşfi (salt-okunur, geniş fan-out) |
| `Plan` / `feature-dev:code-architect` | Toolkit/hook mimari planlaması |
| `general-purpose` | Çok-adımlı karma görevler |
| `feature-dev:code-reviewer` / `code-explorer` | Toolkit kod incelemesi |
| `claude-code-guide` | Harness (hook/skill/MCP) soruları |
| `plugin-dev:*`, `statusline-setup` | Plugin/altyapı bakımı |

KVKK kuralı: ajanlara verilen görev tanımları da ham veri içeremez; ajanlar
korumalı dizinleri açamaz (permissions.deny ajan süreçlerine de uygulanır).

## 6. MCP connector envanteri

### 6a. Dış kanıt çekirdeği (tez literatürünün varsayılan kapısı)
| Connector | Rol | Durum |
|---|---|---|
| `pubmed-epmc` (+ `PubMed` connector) | PubMed/EuropePMC arama, metadata, **tam metin** (`pubmed_fetch_fulltext`), citation format | ✅ |
| `Paper Search` | arXiv/bioRxiv/medRxiv/Crossref/PubMed/Semantic Scholar arama + `download_*`/`read_*` tam metin | ✅ |
| `openalex` | Katalog, ID çözümleme, atıf grafiği, trend | ✅ |
| `semantic-scholar` | Makale/atıf/yazar | ✅ |
| `Consensus` · `Elicit` · `Scholar Gateway` | Sentez aramaları, sistematik derleme desteği | ✅ |
| `bioRxiv` | Preprint (hakemsiz — tezde etiketle) | 🔶 |
| `anamnesis` | Anonim/türetilmiş karar bağlamı, oturum hafızası (hybrid_query/semantic_search) | ✅ |
| `evidentia-kb` | Proje kanıt KB'si (kb_search/kb_upsert) | ✅ |
| `annas-reader` / Anna's Library | DOI/MD5 tam metin + claim kapısı — copyright-gated **fallback tam-metin kaynağı** (EPMC/legal-OA/Paper Search sonrası, Zotero'dan önce) | ✅ (bağlı, `ANNAS_MCP_API_KEY`) |
| `psyarxiv-osf` | OSF/PsyArXiv preprint + preregistration | 🔶 Proje `.mcp.json` config hazır, endpoint 404 bloklu; worker canlı olana kadar `Paper Search` + `openalex` + PubMed/EPMC fallback |
| Zotero MCP | Kütüphane/citation key | 🧩 Codex-yanı — Claude'da `scripts/util/zotero_env_bridge.py` |

### 6b. Türkiye akademik + mevzuat
| Connector | Rol | Durum |
|---|---|---|
| `YokTez MCP` | YÖK tez arama + sayfa-düzeyi markdown | ✅ |
| `YÖK Akademik` | TR akademisyen/jüri/KOL ağı | 🔶 |
| `Mevzuat Bilgisi` | KVKK/etik/sağlık mevzuatı madde doğrulaması (hukuki yorum yok) | 🔶 |
| `Yargı` | KVKK kurul kararları, içtihat | 🔶 |
| `Resmî Gazete` | Yönetmelik/tebliğ birincil kaynak | 🔶 |
| `DETSİS` | Kamu kurum kimlik/teşkilat doğrulama | 🔶 |
| `eric-mcp` | Eğitim/okul uyumu literatürü | 🧩 Codex-yanı — Claude'da `openalex`/`Elicit` filtreleri |

### 6c. Klinik terminoloji / regülasyon (yalnız terminoloji-kaynak doğrulaması)
`med-terminologies` (ICD/SNOMED/LOINC/MeSH/ATC) · `nlm-rxnorm` ·
`nih-clinicaltables` · `openfda` · `iuphar-gtopdb` · `drugddx` ·
`Clinical Trials` · `AdisInsight` · `NPI` — tümü 🔶; hasta-düzeyi öneri üretilmez.
`PopHIVE` 🔶 yalnız ABD surveyans (Türkiye'ye genellenmez). `titck-cache` 🧩 Codex-yanı.

### 6d. Teknik teslim + genel web
`serena` (kod sembol) ✅ · `playwright` plugin 🔶 (render/tarayıcı doğrulama) ·
`chrome-devtools` 🔶 · `PDF Viewer` 🔶 (tez-kılavuz PDF inceleme) ·
`Context7` 🔶 (kütüphane dokümanları) · `brave-search`/genel web 🔶 (yalnız
kullanıcı güncel web isterse; Evidentia akademik/klinik kanıtta web fallback
kullanmaz) · `Grep`/`sourcegraph` 🔶 (kod arama) ·
`Mermaid` 🔶 (diyagram) · `gh` CLI 🔶 (GitHub) · `Mem`/`Granola`/`Zoom` ⛔.

**Sourcegraph MCP** (plugin `sourcegraph@claude-plugins-official`, endpoint
`https://sourcegraph.com`, hesap doğrulandı 2026-07-06): `nls_search` /
`keyword_search` / `read_file` / `go_to_definition` / `find_references` /
`deepsearch` araçları + `sourcegraph:sg-search`, `sourcegraph:sg-file`
skill'leri. Token yalnız `doppler run -p cureohub -c dev_personal -- claude`
ile başlatılan oturumda enjekte olur; araçlar görünmüyorsa neden budur.
Router: `./dmnitel route-tool --query "kod arama"` → `code search MCP gate`.
⚠️ KVKK: Sourcegraph sorgusuna repo içeriği, nitel veri veya katılımcı metni
asla yazılmaz — yalnız dış/açık kaynak kod aranır.

### 6f. Bağlam yönetimi katmanı (bu harness'ta bağlı)
| Connector | Rol | Durum |
|---|---|---|
| `anamnesis` | Birincil bağlam yöneticisi: `corpus_stats` / `semantic_search` / `hybrid_query` / `ingest_document`; Evidentia semantic coverage + tam-metin RAG altyapısı | ✅ (`ANAMNESIS_MCP_API_KEY`) |
| `evidentia-kb` | Proje kanıt KB'si (`kb_search`/`kb_upsert`); doğrulanmış kaynak kimliği + semantic coverage booster | ✅ (`EVIDENTIA_KB_MCP_API_KEY`) |
| `memory` | Hafif oturum-içi knowledge graph; yerleşik memory dizinini tamamlar | ✅ (yerel stdio) |
| `qdrant` | Yerel vektör belleği; anonim/türetilmiş notlar (opsiyonel) | ✅ (yerel stdio) |
| `sequentialthinking` | Çok-adımlı refleksif akıl yürütme (tema-kod kararı); veri değil süreç | ✅ (yerel stdio) |

⚠️ **KVKK:** Bağlam MCP'lerine yalnız **anonim/türetilmiş** içerik `ingest`/`upsert`
edilir; ham transkript, aile/katılımcı satırı, PII ve `.remember/` içeriği taşınmaz.

### 6e. Default-off (tez oturumunda açılmaz)
Adobe, Canva, Figma, Firebase, Cloudflare, Supabase, GoDaddy, Borsa/Fon/Finmap/
IBKR, seyahat (Booking/Expedia/Kiwi/lastminute/Tripadvisor/THY/Uber), Spotify,
Gmail/Calendar/Drive, ThoughtSpot, Türk Patent, Ansvar/Open Law/Fedlex/
International Treaty/Health Policy (yabancı hukuk), Social Listening, MIDAS,
AdisInsight-dışı finans/pazar araçları. Yalnız açık, tez-dışı istekle.

## 7. Hook katmanı (deterministik kapılar)

| Olay | Nitel repo | Nicel repo (doktoratezi) | İşlev |
|---|---|---|---|
| SessionStart | `.claude/hooks/session_start.py` ↔ `.codex/hooks/…` | aynı ikiz | `CONVENTIONS.md` + talimatname özetini enjekte eder |
| UserPromptSubmit | ikiz | ikiz | Prompt'ta sır kalıbı → blok |
| PreToolUse (Bash) | ikiz | ikiz | Yıkıcı komut + korumalı yol deny-list'i (nitel: `01_raw_data/…`; nicel: `data/raw|identified|cleaned|backup|processed/`, `outputs/`, `_targets/`) |
| PostToolUse (Bash) | ikiz | ikiz | Çıktıda sır sızıntısı/hata imzası uyarısı |
| Stop | ikiz | ikiz | Kaynaksız sayısal iddia → tur devam; kaynak = URL/DOI/PMID/yıl/**repo dosya yolu** |
| permissions.deny | `.claude/settings.json` | `.claude/settings.json` | Ham veri + credential dosya-aracı erişimi (Read/Grep/Glob/Edit) kapalı |

Test yüzeyleri: `tests/test_claude_hooks.py` (16 sözleşme testi) ·
`tests/test_ai_reliability_hooks.py` → plugin 55/55 · doktoratezi plugin 142/142 ·
promptfoo offline gate 4/4 + 4/4 (`reliability/evals/`).

## 8. Playbook / talimatname dizini

| Belge | Rol |
|---|---|
| `00_context/KANONIK_TEZ_YAZIM_PLAYBOOK.md` | **Tek entegre operasyon kılavuzu** — talimatname + Codex playbook + bu harita + tez-yazim README/format + tam-metin kaskadı + iki skill köprüsü + Evidentia v1.7/`medical-research` v8.5 hattını tek yüzeyde birleştirir; tüm-MCP matrisi (§6) ve tam-metin araç kaskadı (§7) burada |
| `00_context/TALIMATNAME_TEZ_YAZIM.md` | **Claude Code zorunlu talimatname (bu repo)** |
| `00_context/CODEX_PLAYBOOK.md` | Codex ikizi |
| `doktoratezi/tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` | Claude Code zorunlu talimatname (nicel/yazım merkezi) |
| `doktoratezi/tez-yazim/README.md` | 10-adımlı resmi yazım sırası |
| `doktoratezi/tez-yazim/00_kaynak-kurallari/format-kontrati.md` | Biçim/istatistik/nitel-bulgular kontratları |
| `doktoratezi/tez-yazim/01_mimari/tez-yazim-ana-plani.md` | Faz 0–10 + Gap Register |
| `doktoratezi/tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` | 6-kapılı referans ledger'ı |
| `doktoratezi/tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | Kapı 0–5 bölüm sertifikasyonu |
| `doktoratezi/tez-yazim/06_kritik-kaynaklar/README.md` + manifest TSV | Kanonik kaynak seçim haritası |
| `CONVENTIONS.md` (iki repo) | Hook'la enjekte edilen AI-reliability sözleşmeleri |

## 9. Bakım kuralları

1. Yeni MCP/plugin/skill eklenince bu harita + ilgili talimatname aynı commit'te güncellenir.
2. Hook politikası değişince: iki harness ağacı (`.claude/hooks` ↔ `.codex/hooks`),
   iki repo ve testler birlikte güncellenir; `/nitel-dogrulama` PASS şartı.
3. Bağlantı durumu değişkendir (🔶/🧩 etiketleri oturuma göre oynar); citation
   öncesi kapı hangi harness'ta kapandıysa ledger'a o yazılır.
4. Bu harita envanterdir, yetki vermez: default-off bir aracın kullanımı için
   kullanıcının açık isteği gerekir.
