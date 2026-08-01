# KANONİK TEZ YAZIM PLAYBOOK — T1DM Karma Doktora Tezi

Sürüm: 1.2 · 2026-07-08 · Kapsam: T1DM karma doktora tezinin **tüm tez yazım,
nitel kanıt, dış literatür/tam metin ve karma sentez oturumları**; iki-kol
(`T1DM Niteliksel` + `doktoratezi`), iki harness (Claude Code + Codex CLI),
üç rehber (`niteliksel-arastirma-rehberi-t1dm`, `t1dm-tez-rehberi`, `evidentia`)
ve `sci-audit@cureonics-marketplace` manüskript denetim katmanı.

Bu belge, daha önce ayrı ayrı yazılmış playbook/talimatnameleri **tek entegre
operasyon kılavuzunda** birleştirir. Kaynak belgeler ve rolleri §14'te listelenir.

---

## 0. Bu belge nedir, ne değildir (bağlayıcılık + öncelik)

**Nedir:** Tez yazımında hangi kolun açılacağını, hangi aracın/MCP'nin ne zaman
ve nasıl kullanılacağını, tam metin ve citation kapılarının nasıl kapatılacağını
tek yüzeyde toplayan **kanonik operasyon playbook'u**. Evidentia + iki rehber
skill'in **tek entegre kanıt hattı** olarak nasıl çalıştığını gösterir (§1, §5).

**Ne değildir:** Yeni bir politika kaynağı değildir. Deterministik zorlama
(hook'lar, `permissions.deny`, `stop_verify`) ve bağlayıcı süreç kuralı hâlâ
`00_context/TALIMATNAME_TEZ_YAZIM.md` (Claude) + `00_context/CODEX_PLAYBOOK.md`
(Codex) + `CONVENTIONS.md` içindedir. Bu belge onları **çelmez, birleştirir**.

**Öncelik sırası (çelişkide):**
1. Kullanıcının o oturumdaki açık talimatı.
2. `TALIMATNAME_TEZ_YAZIM.md` + hook zinciri (deterministik, bağlayıcı).
3. Bu kanonik playbook (entegre operasyon katmanı).
4. `CLAUDE.md` / `AGENTS.md` / genel repo notları.
5. Biçim, bölüm sırası, sayı/kaynakça: resmi `docs/tez-kilavuz/` **üstündür**.

**Drift önleme:** Politika değişikliği önce kaynak belgede (talimatname → Codex
ikizi → hook ağaçları + testler), sonra bu playbook güncellenir (§14). Bu belge
kaynak belgeleri **özetler ve indeksler**; hook-zorlamalı maddeleri yeniden
tanımlamaz.

---

## 1. Entegre Yapı — Katman Şeması (iki-kol · iki harness · üç rehber)

Her tez görevi aynı katman zincirinden geçer; üst katman alt katmanı yetkilendirir:

```
Kullanıcı görevi
 └─ Yönetişim: CLAUDE.md/AGENTS.md + TALIMATNAME + CONVENTIONS   (model-düzeyi kural)
     └─ Hook katmanı: .claude/hooks ↔ .codex/hooks               (deterministik kapı)
         └─ Yerel toolkit: ./dmnitel + zotero_env_bridge          (KVKK-güvenli yerel iş)
             └─ Skill/komut: /tez-oturum + üç rehber skill        (rota + metodoloji)
                 └─ Ajan katmanı: distiller / Explore / synthesizer (bağlam ekonomisi)
                     └─ MCP connector katmanı                       (kanıt · tam metin · mevzuat)
```

**Üç rehberin tek hat olması.** Evidentia bir üst-akıl değil, T1DM gate'inin
çağırdığı dış-kanıt altyapısıdır. Kol seçimi:

```
Tez/karma soru
 ├─ İç veri (RTA/codebook/COREQ/alıntı/triad)  → ./dmnitel + niteliksel-arastirma-rehberi-t1dm
 ├─ Dış literatür/tam metin/citation/KOL       → EVIDENTIA v1.7 / medical-research v8.5 + OA/legal-OA/Paper Search + Anna's + Zotero + ledger
 └─ Nicel/karma köprü (H1–H5, joint display, IRR)→ t1dm-tez-rehberi (nicel kök)
```

**Tek cümle kural:** *Kendi verimizden çıkan her şey `./dmnitel` + niteliksel
skill'de; dünyadan gelen her şey Evidentia'da; nicel/karma köprü
`t1dm-tez-rehberi`de.* Üç kol **bir paragrafta** buluşur ve kanıt türü açıkça
etiketlenir, örn.:

> "Tema 3'te görünen görünmez emek örüntüsü [iç, RTA]; kronik hastalıkta
> ebeveyn aşırı-korumacılığındaki sistematik artış [Evidentia: @pinquart2013]
> ile uyumlu; nicel kolda EMBU-P aşırı koruma farkı [nicel, H3] bu çerçevede
> okunur."

**Repo/harness bölüşümü:**

| Eksen | `T1DM Niteliksel` | `doktoratezi` |
|---|---|---|
| Rol | Nitel kol: RTA, codebook, COREQ, audit trail, triadik kanıt, kanonik nitel rapor | Yazım merkezi: `thesis.qmd`, `chapters/*.qmd`, H1–H5 pipeline, referans ledger'ı |
| Yerel gate | `./dmnitel` + `t1dm-qual-ai-audit` (55/55) | `tez-yazim/` + `doktoratezi-ai-audit` (142/142) |
| Korumalı veri | `01_raw_data/`, `02_processed/transcripts/`, `01_deidentified/`, `00_raw_locked/`, `.remember/` | `data/raw\|identified\|cleaned\|backup\|processed/`, `outputs/` satır-düzeyi, `_targets/` |

---

## 2. Oturum Ritüeli (her tez oturumunda zorunlu)

1. `/tez-oturum "<görev>"` → `./dmnitel ai-context` + `./dmnitel route-tool` +
   TRACKER özeti otomatik gelir.
2. Görevi §1'deki **üç koldan birine** yerleştir ve açıkça bildir.
3. Yazım/format/bölüm işiyse ana operasyon merkezi
   `repo kökü/tez-yazim`; önce `README.md`,
   `06_kritik-kaynaklar/README.md` + `kritik-dosya-manifesti.tsv` ve resmi
   `docs/tez-kilavuz/`. Çakışmada resmi kılavuz üstündür.
4. Karma tez / joint display / iki-kol sentezi → `/capraz-repo`
   (`./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md`).
5. Skill kapıları: nitel metodoloji → `niteliksel-arastirma-rehberi-t1dm`;
   nicel/karma → `t1dm-tez-rehberi`; dış literatür/tam metin → Evidentia (§8);
   manüskript adli denetimi/Türkçe imla → `sci-audit@cureonics-marketplace`
   v0.2.0; render → `carbon-quarto-scientific`.
6. Kapanış: `/remember` (KVKK: `.remember/` yerelde kalır);
   harici MCP kullanıldıysa `/ai-kayit` (§12).

---

## 3. KVKK Veri Sınırı — İhlal Edilemez

- Korumalı alanlar §1 tablosundaki iki-kol yolu + `.remember/`.
- Bu alanlardan **satır düzeyi içerik, aile düzeyi hassas detay, ham alıntı,
  demografi satırı, onam/protokol kişisel içeriği** bağlama dökülmez, memory'ye
  yazılmaz, **hiçbir harici MCP/RAG/connector/Evidentia/Anna's'a gönderilmez**.
- Alıntı bütünlüğü `./dmnitel check-quotes` ile (transcript **açmadan**); negatif
  vaka `./dmnitel find-negative-cases` ile.
- Teze yalnız: araştırmacı-onaylı **anonim alıntı** (aile no + rol etiketi),
  kod/tema düzeyi türetilmiş bilgi, COREQ/audit-trail/codebook çıktısı, kanonik
  nitel sonuç raporu girer.
- Bağlam MCP'lerine (`anamnesis`/`evidentia-kb`/`memory`/`qdrant`) yalnız
  **anonim/türetilmiş** karar bağlamı; `permissions.deny` + hook zinciri bunu
  ayrıca zorlar.

---

## 4. Bölüm → Kaynak → Kapı Matrisi (iki-kol yazım modeli)

| Tez bölümü | Nitel kaynak (`T1DM Niteliksel`) | Nicel kaynak (`doktoratezi`) | Zorunlu kapı |
|---|---|---|---|
| GİRİŞ ve AMAÇ / GENEL BİLGİLER | Kanonik nitel rapor (yalnız arka plan) | `tez-yazim/03_bolum-hazirlik/01…02*.md`, CSR, SAP | Referans kapısı (§9) + iki-kol AI-reliability |
| GEREÇ ve YÖNTEM | COREQ, audit trail, positionality, LLM beyanı (`03_analysis/methodology/`) | `03_gerec-ve-yontem.md`, `_targets.R`, veri haritası | Resmi kılavuz + kanonik yöntem kanıtı + sci-audit Kapı 4/5 |
| BULGULAR | Kanonik nitel sonuç raporu, 4 makro tema, quote integrity | `04_bulgular.md`, H1–H5 | Repo artefaktı + test kanıtı + sci-audit Kapı 4/5 |
| TARTIŞMA ve SONUÇ | Negatif vaka, refleksivite, triadik yorum | `05_tartisma-ve-sonuc.md`, post-hoc sınırları | Kanıt ayrımı + iki-kol AI-reliability + sci-audit Kapı 4/5 |
| KAYNAKLAR / EKLER | COREQ, codebook, audit trail, LLM beyanı | `06_kaynaklar-ekler.md`, `references.bib` | Ledger + Zotero + format kontrol |

**Kanıt ayrımı:** tez = **4 makro tema**, journal = **6 tema** — karıştırılmaz.
Nitel tema nicel estimate gibi sunulmaz; nicel sonuç nitel bulgunun nedensel
kanıtı yapılmaz; joint display iki kolu yan yana getirir, kanıt türünü açık yazar.

---

## 5. Üç Kollu Entegre Kanıt Modeli (çekirdek entegrasyon)

Bir kanıt ihtiyacı doğduğunda:

| Adım | İç veri kolu | Dış kanıt kolu | Nicel/karma kolu |
|---|---|---|---|
| 1. Sınıfla | RTA/codebook/COREQ/alıntı/triad mı? | Literatür/tam metin/citation/KOL mü? | H1–H5/EMBU/Beck/KİA/joint display mi? |
| 2. Kapı | `./dmnitel` (§6.1) + niteliksel skill | Evidentia native-first / `medical-research` v8.5 (§8) | `t1dm-tez-rehberi` + `cross-repo-status` |
| 3. KVKK | Ham veri connector'a gitmez | Yalnız kamuya açık literatür | doktoratezi korumalı veri sınırı |
| 4. Çıktı | Kod/tema/anonim alıntı | `references.bib` + `.qmd` + ledger | joint display / bulgu tablosu |

**Karışık soruda ikiye böl:** iç parçayı `./dmnitel` + niteliksel skill'le
yürüt, dış parçayı Evidentia'ya ver, nicel köprüyü `t1dm-tez-rehberi`ye devret,
**bir paragrafta birleştir ve her cümlede kanıt türünü etiketle**.

---

## 6. TÜM MCP KULLANIM MATRİSİ

Durum etiketleri: **✅ bağlı** (bu Claude oturumunda hazır) · **🔶 koşullu**
(yalnız görev sinyaliyle) · **🧩 Codex-yanı** (bu harness'ta bağlı değil, Claude
karşılığı verilir) · **⛔ default-off** (tez süreci dışı).

**Claude Code'da MCP çağırma mekaniği.** MCP araçları büyük ölçüde *deferred*
(ertelenmiş) sunulur: yalnız adları görünür, şeması yüklü değildir. Bir aracı
çağırmadan önce **`ToolSearch` ile şemasını yükle**
(`select:<tam_ad>` veya anahtar-kelime araması). Evidentia işleri `/evidentia:*`
slash-komutlarıyla; ağır fan-out ise distiller/synthesizer **ajanlarıyla**
(Agent tool) izole edilir. **Genel KVKK kuralı tüm bu katmana uygulanır: hiçbir
ham veri/transkript/PII herhangi bir MCP'ye gönderilmez.**

### 6.0 Nasıl okunur

Her satır: connector → **rol** → **ne zaman açılır (tetikleyici)** →
**nasıl çağrılır (giriş/örnek fonksiyon)** → **KVKK sınırı** → **durum**.

### 6.1 Yerel toolkit (birincil; harici API yok, ham veri connector'a gitmez)

| Araç | Rol / Ne zaman | Nasıl | Durum |
|---|---|---|---|
| `./dmnitel ai-context` | Oturum açılışı; repo-özel tool-bridge özeti | `/tez-oturum` içinde otomatik | ✅ |
| `./dmnitel route-tool --query` | Kol belirsizse **her işten önce** | `./dmnitel route-tool --query "<soru>"` | ✅ |
| `./dmnitel cross-repo-status` | Karma/joint display/iki-kol sentezi öncesi | `--output 07_reports/cross_repo_thesis_bridge_status.md` | ✅ |
| `./dmnitel lint-codebook` | Codebook CSV tutarlılığı | `./dmnitel lint-codebook 03_analysis/codebook/…csv` (kanonik `codebook_v3.md`) | ✅ |
| `./dmnitel build-triadic-matrix` | Anne/T1DM çocuk/kardeş tema matrisi | `--coded-data … --output 04_triadic_matrices/…` | ✅ |
| `./dmnitel check-quotes` | Anonim alıntı bütünlüğü (transcript **açmadan**) | `--source <deidentified> --quotes <csv>` | ✅ |
| `./dmnitel audit-coreq` | COREQ 32 madde metin-içi kanıt | `--methods … --results …` | ✅ |
| `./dmnitel find-negative-cases` | Tema yorumundan önce negatif/alternatif vaka | `--coded-data … --theme "<tema>"` | ✅ |
| `./dmnitel log-ai-use` | Her harici MCP/Evidentia koşumundan sonra **zorunlu** | `/ai-kayit` sarmalar; `99_ai_use_log/ai_use_log.csv` | ✅ |
| `python3 scripts/util/zotero_env_bridge.py` | Zotero Web API (status/search/export/import-doi) | `.env → ZOTERO_API_KEY`; anahtar asla yazdırılmaz; write/import açık onay | ✅ |
| `python3 .codex/tools/codex_mcp_roster_redacted.py` | Codex MCP roster (token-redakteli) | Ham `codex mcp list` iki harness'ta da yasak | ✅ |

### 6.2 Bağlam yönetimi MCP'leri (yalnız anonim/türetilmiş içerik)

| Connector | Rol / Ne zaman | Nasıl | Durum |
|---|---|---|---|
| `anamnesis` | **Birincil bağlam yöneticisi**; oturum açılışı + Evidentia semantic coverage ve tam-metin RAG altyapısı | `corpus_stats` → `ingest_document` (anonim/türetilmiş) → çok-sorgulu `hybrid_query`/`semantic_search`; `upsert_triples`/`graph_neighbors`/`subgraph` | ✅ (`ANAMNESIS_MCP_API_KEY`) |
| `evidentia-kb` | Proje kanıt KB'si; doğrulanmış kaynak kimliği + semantic coverage booster | `kb_search` / `kb_upsert` | ✅ (`EVIDENTIA_KB_MCP_API_KEY`) |
| `memory` | Hafif oturum-içi knowledge graph | yerel stdio | ✅ |
| `qdrant` | Yerel vektör belleği (anonim/türetilmiş notlar, opsiyonel) | yerel stdio | ✅ |
| `sequentialthinking` | Çok-adımlı refleksif akıl yürütme (tema-kod kararı); **veri değil süreç** | deferred; `ToolSearch` ile yükle | ✅ |

⚠️ Bu katmana `ingest`/`upsert` edilen içerik yalnız anonim/türetilmiş karar
bağlamıdır; ham transkript/PII/`.remember/` **taşınmaz**.

### 6.3 Dış kanıt akademik çekirdeği (tez literatürünün varsayılan kapısı)

Ham connector'a **doğrudan gidilmez** — Evidentia D0–D6 kaskadı içinden çağrılır (§8).

| Connector | Rol / Ne zaman | Nasıl (örnek fonksiyon) | Durum |
|---|---|---|---|
| `evidentia-skills` | Kaskad iskeleti (`start`, `medical-research`) | `/evidentia:start`; D0 preflight | ✅ |
| `pubmed-epmc` | PubMed/EuropePMC arama, metadata, **tam metin**, citation | `pubmed_search_articles` → `pubmed_fetch_articles` → `pubmed_fetch_fulltext`; `pubmed_europepmc_search` (AFF:"Turkey") | ✅ |
| `PubMed` (connector) | Alternatif PubMed arama + tam metin + copyright | `search_articles` / `get_full_text_article` / `get_copyright_status` | ✅ |
| `Paper Search` | arXiv/bioRxiv/medRxiv/Crossref/PubMed/Semantic tarama + tam metin | `search_*` → `read_*` / `download_*`; `get_crossref_paper_by_doi` | ✅ |
| `openalex` | Katalog, ID çözümleme, atıf grafiği, trend | `openalex_resolve_name` → `openalex_search_entities` → `openalex_get_citation_graph` | ✅ |
| `semantic-scholar` | Makale/atıf/yazar (ikincil; 429/500'de OpenAlex'e düş) | `search_papers` / `get_paper` / `get_paper_citations` | ✅ |
| `Consensus` | Sentez araması (numaralı atıf zorunlu) | `search` | ✅ |
| `Elicit` | Sistematik derleme/rapor desteği | `search_papers` / `create_systematic_review` | ✅ |
| `Scholar Gateway` | Semantik akademik arama | `semanticSearch` | ✅ |
| `psyarxiv-osf` | OSF/PsyArXiv preprint + preregistration | Proje `.mcp.json` config hazır, endpoint 404 bloklu; fallback `Paper Search` + `openalex` + PubMed/EPMC | 🔶 |
| `bioRxiv` | Preprint (hakemsiz — tezde etiketle); yalnız preprint sinyalinde | `search_preprints` / `get_preprint` | 🔶 |

### 6.4 Türkiye akademik katmanı

| Connector | Rol / Ne zaman | Nasıl | Durum |
|---|---|---|---|
| `YokTez MCP` | YÖK tez arama + sayfa-düzeyi markdown; TR tez boşluğu/özgünlük | `search_yok_tez_detailed` → `get_yok_tez_thesis_details` → (izinliyse) `get_yok_tez_document_markdown`; daraltma `list_yok_tez_anabilim_dali` → `search_yok_tez_by_anabilim_dali` | ✅ |
| `YÖK Akademik` | TR akademisyen/jüri/KOL ağı; yalnız KOL açıkça istenince | `yok_search` → `yok_get_full_profile` / `yok_get_collaborators` | 🔶 |
| `eric-mcp` | Eğitim/okul/akademik uyum/çocuk gelişimi sinyalinde | Codex-yanı; Claude'da `openalex`/`Elicit` filtreleri | 🧩 |

Ağır TR tez taraması için `academic-archival-distiller` ajanı (bağlam ekonomisi).

### 6.5 Mevzuat / etik (yalnız resmi madde doğrulaması; hukuki yorum yok)

| Connector | Rol / Ne zaman | Nasıl | Durum |
|---|---|---|---|
| `Mevzuat Bilgisi` | KVKK/etik/sağlık mevzuatı madde doğrulaması | `search_kanun` / `search_teblig` / `get_mevzuat_madde_tree` | 🔶 |
| `Yargı` | KVKK kurul kararları, içtihat | `search_kvkk_decisions` → `get_kvkk_document_markdown` | 🔶 |
| `Resmî Gazete` | Yönetmelik/tebliğ birincil kaynak | `rg_search` → `rg_get_item` | 🔶 |
| `DETSİS` | Kamu kurum kimlik/teşkilat doğrulama | `detsis_resolve_birim` → `detsis_get_kunye` | 🔶 |

Ağır mevzuat taraması için `legal-distiller` ajanı.

### 6.6 Klinik terminoloji / regülasyon (yalnız terminoloji-kaynak doğrulaması)

Hasta-düzeyi öneri **üretilmez**; yalnız tez terminolojisi/kaynak doğrulaması.

| Connector | Rol / Ne zaman | Durum |
|---|---|---|
| `med-terminologies` | ICD/SNOMED/LOINC/MeSH/ATC; kod/terim normalizasyonu | 🔶 |
| `nlm-rxnorm` · `nih-clinicaltables` · `openfda` | RxNorm/ICD-11/FDA; ilaç/kod/etiket sinyalinde (ICD-11 metin araması `openfda.icd11_search`) | 🔶 |
| `iuphar-gtopdb` · `drugddx` | Farmakoloji/DDI; mekanizma/etkileşim sinyalinde | 🔶 |
| `Clinical Trials` · `AdisInsight` | RCT/pipeline; müdahale/NCT sinyalinde | 🔶 |
| `PopHIVE` | **Yalnız ABD** sürveyans; Türkiye'ye genellenmez | 🔶 |
| `NPI Registry` | ABD sağlık sağlayıcı doğrulama (tezde nadir) | 🔶 |

### 6.7 Tam metin kolu

`annas-reader` / Anna's Library — DOI/MD5 tam metin + claim kapısı; copyright-gated
**fallback** tam-metin kaynağı (EPMC/legal-OA/Paper Search sonrası, Zotero'dan önce). ✅
(`ANNAS_MCP_API_KEY`). Ayrıntı ve tam sıralı kaskad → **§7**.

### 6.8 Teknik teslim + genel web (yalnız açık teknik görev)

| Connector | Rol / Ne zaman | Durum |
|---|---|---|
| `serena` | Kod sembol işleri (toolkit/hook) | ✅ |
| `playwright` (plugin) | Render/tarayıcı doğrulama; **OpenAthens tam metin login** (§7 T1) | 🔶 |
| `chrome-devtools` | İleri tarayıcı denetimi | 🔶 |
| `PDF Viewer` | `docs/tez-kilavuz/` PDF inceleme | 🔶 |
| `Context7` | Kütüphane/framework dokümanı (Quarto/R paketi) | 🔶 |
| `brave-search` / genel web | Yalnız kullanıcı güncel web isterse veya resmî sürüm sayfası gibi current bilgi gerekiyorsa; Evidentia akademik/klinik kanıtta web fallback kullanmaz | 🔶 |
| `Grep` (searchGitHub) · `Context7` | Kod/örnek arama | 🔶 |
| `Mermaid` | Tema haritası/diyagram (MD→SVG) | 🔶 |
| `gh` CLI | GitHub işleri (yalnız açık istek) | 🔶 |

### 6.9 Default-off (tez oturumunda açılmaz — yalnız açık, tez-dışı istek)

`Adobe`, `Canva`, `Figma`, `Firebase`, `Cloudflare`, `Supabase`, `GoDaddy`,
`Borsa`/`Fon`/`Finmap`/`IBKR`, seyahat (`Booking`/`Expedia`/`Kiwi`/`lastminute`/
`Tripadvisor`/`Turkish Airlines`/`Uber`), `Spotify`, `Gmail`/`Google Calendar`/
`Google Drive`, `Zoom`/`Granola`/`Mem`, `ThoughtSpot`, `Türk Patent`, `Social
Listening`, `MIDAS`, `Interactive Brokers`, yabancı hukuk (`Ansvar`/`Open Law`/
`Fedlex`/`International Treaty`/`Health Policy`). ⛔

> ⚠️ **Auth gerektiren (bu oturumda kullanılamaz):** `plugin:cloudflare:*`
> (api/builds/observability) OAuth ister; non-interactive oturumda yetkilendirilemez.

---

## 7. TAM METİN ARAÇ KASKADI

Tam metin, Evidentia `medical-research` v8.5 fulltext-retrieval sözleşmesinin
parçasıdır. Bir dış kaynak şu sıra tamamlanmadan **final citation** olarak tez
metnine giremez. Amaç tam metni bulmak değil, her citation adayını kimlik +
erişim + Zotero + BibTeX + claim iziyle kapatmaktır. Büyük tam metin bağlama
dökülmez; `anamnesis` ile tek ingest + sınırlı, provenance'lı retrieval yapılır.

### T0 — Preflight
- `.claude/evidentia.local.md` + Evidentia `CONNECTORS.md` +
  `shared/canonical-cache-contract.md` + `t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` okunur.
- `python3 scripts/util/zotero_env_bridge.py status --json` (Zotero yetkileri).
- OpenAthens: yalnız gerekiyorsa ortam değişkenlerinin **varlığı** doğrulanır
  (`OPENATHENS_USERNAME/PASSWORD/INSTITUTION/LOGIN_URL`,
  `MILLET_KUTUPHANESI_DATABASES_URL`); değerler asla yazdırılmaz.

### Sıralı kapı ve araçlar

| Kademe | Araç / MCP | Rol | Başarı kanıtı |
|---|---|---|---|
| **T1 PMC/EPMC açık erişim** | `PubMed` (`get_full_text_article`, `get_copyright_status`) | Açık erişim tam metin + lisans | PMCID, copyright status, EPMC full text |
| **T2 Legal OA / Unpaywall** | `pubmed-epmc` (`pubmed_fetch_fulltext`) | EuropePMC + Unpaywall legal-OA | DOI/PMID eşleşmesi, legal-OA locator |
| **T3 Paper Search full text** | `Paper Search` (`read_*` / `download_*`) | ArXiv/bioRxiv/medRxiv/PubMed/Semantic tam metin | kaynak ID, lisans/provenance, hedefli pasaj |
| **T4 Anna's Library** | `annas-reader` | DOI/MD5 doğrulanmış copyright-gated fallback | metadata uyumu + hedefli claim; toplu birebir çoğaltma yok |
| **T5 Wiley/OpenAthens/Zotero eki** | Wiley/OAuth veya kullanıcı kurumsal erişimi; Zotero attachment | Önceki yollar yetmezse claim-critical tam metin | yayıncı/lisanslı full text, Zotero URL/snapshot/attachment |
| **Zotero kapanış** | `zotero_env_bridge.py import-doi` (açık onayla) | item + attachment + note + BibTeX + `references.bib` mutabakatı | item key / attachment key / note key / BibTeX key |

> **Wiley (Cloudflare):** `onlinelibrary.wiley.com` kaynakları bot-korumalı; doğrudan
> Playwright "Just a moment..." duvarına takılır. Tam metin **T1 OpenAthens / Millet
> Kütüphanesi kurumsal oturumu Playwright ile** açılır; **OpenAthens parolası/credential
> hiçbir tool-çağrısına yazılmaz** (`browser_fill_form` value dahil). Otomatik kurulamazsa
> kullanıcı interaktif kapatır veya OA eşdeğeri seçilir. Ayrıntı: `doktoratezi/tez-yazim/
> 00_kaynak-kurallari/tam-metin-erisim-kaskadi.md` (T1/6).

```bash
# Zotero kapanış (kullanıcı onayı verildiyse):
python3 scripts/util/zotero_env_bridge.py import-doi <DOI> \
  --bibtex-key <citation_key> \
  --fulltext-url '<publisher_or_openathens_url>' --fulltext-url-title '<route>' \
  --attachment-file <local_fulltext_or_snapshot.pdf> --attachment-title '<title>' \
  --note '<short provenance note>' --json
```

### Ledger durumları (tam metin ekseni)
`candidate` → `full-text-ok` (veya erişilemezse `full-text-exception`) →
`zotero-ok` → `reliability-ok` → `cite-ok`. OA/legal-OA/Paper Search + Anna's
yolları tüketilmeden `full-text-exception` yazılamaz; `full-text-exception`
**final citation olamaz**.

### Yasaklar (tam metin)
`.env`/credential/token/cookie çıktısı yok · ham CSV/transkript/satır-veri tam
metin araçlarına gönderilmez · telifli metin uzun/toptan çoğaltılmaz · görülmeyen
tam metinden sayı/yöntem **uydurulmaz** · SciSpace/ResearchGate/genel web aynası
tek başına `full-text-ok` sayılmaz · Evidentia hattında Exa/Tavily/OSINT fallback yoktur.

---

## 8. Evidentia v1.7 / `medical-research` v8.5 Hattı (dış kanıt motoru)

**Ana gate her zaman T1DM'dir; Evidentia dış-kanıt altyapısıdır.** Ciddi
literatür işinde kısa yoldan çıkma; kanıt doygunluğuna kadar derinleş. Eski
`D0-D6` dili yalnız legacy shorthand'tır; güncel Claude Code sözleşmesi
`CONNECTORS.md` + `canonical-cache-contract.md` ile belirlenen native-first,
no-web/OSINT, semantic coverage ve clean-copy hattıdır.

| Aşama | Amaç | Araç kapsamı | Çıkış |
|---|---|---|---|
| **0. Preflight + local scope** | Roster, auth, PICO/ölçüm/coğrafya, OSF/HARKing | `evidentia-skills:start`, `.claude/evidentia.local.md`, `CONNECTORS.md` | local scope, connector kararı |
| **0.4 Semantic scope** | Kavram setini ve coverage_set'i kapat | knowledge-map + `evidentia-kb kb_search` booster | auditable coverage_set |
| **1. Bibliyografik geniş tarama** | Yayın evrenini yakala | PubMed/EPMC, Paper Search, OpenAlex, S2, YÖK Tez; CT/bioRxiv/ERIC koşullu | aday havuzu, dedupe ID |
| **2. Native-first çözümleme** | En iyi yapısal kaynağı seç | native MCP → REST/legal-OA → belgelenmiş boşluk | gap-log veya kanıt artefaktı |
| **3. Eleme/rerank/AFF-TR** | En güçlü + transfer edilebilir kanıt | çalışma tipi, örneklem, ölçüm, yaş, T1DM/TR uyumu, EPMC AFF loop | kanıt matrisi |
| **4. Tam metin + RAG** | Abstract'ın vermediği ayrıntı | §7 kaskadı → `anamnesis` corpus_stats/ingest/hybrid_query | sayısal endpoint, lokatör |
| **5. Çapraz-doğrulama + clean-copy** | Çelişki/terim/transfer riski ve tez entegrasyonu | claim-level XVAL; clean-copy, OPS/VIZ izolasyonu, Zotero/ledger | yazılabilir paragraf + BibTeX + gap kaydı |

**Giriş noktaları:** `/evidentia <soru>` (tek konu) · `/evidentia-synthesize`
(çok-belge derin) · `/evidentia-fulltext <DOI>` (sayısal endpoint) ·
`/evidentia-kol <alan>` (jüri/hakem) · `evidentia:evidence-synthesizer` ajanı
(ağır fan-out izolasyonu) · `medical-distiller`/`academic-archival-distiller`/
`legal-distiller` ajanları (bağlam ekonomisi).

**Kapsam kapısı (psikososyal):** varsayılan aktif çekirdek = akademik/RAG/tam-metin
(PubMed/EPMC, Paper Search, YÖK Tez, OpenAlex, S2, anamnesis, evidentia-kb,
annas-reader). `psyarxiv-osf` proje config'i hazır fakat endpoint 404 bloklu;
worker canlı olana kadar fallback `Paper Search` + `openalex`. İlaç/mevzuat/terminoloji/ABD-sürveyans katmanları
**yalnız açık sinyalle** açılır; tetiklenmemiş pasif connector yokluğu preflight
hatası değildir; tetiklenip erişilemeyen katman `gap_log`'a yazılır.

**Açık-bilim (HARKing) kuralı:** confirmatory (H1–H4) prior'lar ön-kayıtta
sabitlenir; Evidentia ile sonradan bulunan meta-analiz prior'ı **değiştiremez**
(yalnız `[KEŞİFSEL]` duyarlılık). Benchmark güncellemesi
`docs/analiz_planlari/PRE-REGISTRATION-DEVIATION-TABLE.md`'ye yazılır.

**Uydurma referans yasağı:** `references.bib`'e giren her künye
Evidentia-doğrulamalı gerçek PMID/DOI/NCT/YÖK-ID'ye iz sürer; doğrulanamayan
eklenmez ("VERİ BULUNAMADI").

---

## 9. Zorunlu Referans Kapısı (citation'dan önce) + Ledger

Her dış referans için `/referans-kapisi "<künye>"`. Sıra sabittir:

```
bağlam → bibliyografik kimlik (DOI/PMID/PMCID/OpenAlex/YÖK)
       → tam metin kanıtı (§7: EPMC/OA → legal-OA → Paper Search → Anna's)
       → Zotero mutabakatı (item key + BibTeX key; ikisi farklıdır)
       → claim/pasaj notu → ledger kaydı + iki-kol AI-reliability
```

**Ledger:** `doktoratezi/tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`.
**Durum akışı:** `candidate → full-text-ok/full-text-exception → zotero-ok →
reliability-ok → cite-ok`. Kapı kapanmadan referans metne girmez. Zotero'ya
yazma/import **açık onay** ister. Bir kaynak birden çok bölümde kullanılacaksa
ledger'daki **Bölüm sütunu genişletilir** ve kapanışta iki-kol AI-reliability
yeniden koşulur (yeni dış retrieval gerektirmez).

---

## 10. Doğrulama Paketi + İki-kol AI-reliability

Kapanışta `/nitel-dogrulama`:

```bash
# Manüskript adli denetimi + Türkçe imla (bölüm metni değiştiyse):
/sci-audit:check-turkish <bolum>.qmd --strictness certification
/sci-audit:audit <bolum>.qmd --lang tr --strictness certification --type <coreq|srqr|strobe|prisma|jars>
/sci-audit:audit-report --out <rapor>.md

# T1DM Niteliksel:
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py
python3 -m py_compile .codex/hooks/*.py .claude/hooks/*.py
# doktoratezi (referanslı bölüm kapanışında çift kural):
cd `git rev-parse --show-toplevel` && \
PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
# Quarto etkilendiyse:
quarto check && quarto render thesis.qmd
# AI/policy dosyası değiştiyse:
npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml
```

**İş "tamam" sayılmaz eğer:** dokunulan repo kolu açık değilse · kaynaklar dosya
yoluyla izlenebilir değilse · ham veri sınırı ihlal edildiyse · gerekli test
exit 0 ile bitmediyse · harici MCP tez içeriğini etkilediği hâlde `/ai-kayit`
güncellenmediyse · kullanıcı istemeden stage/commit/push yapıldıysa.

---

## 11. Bölüm Sertifikasyonu (doktoratezi Kapı 0–5)

Bir `chapters/*.qmd` bölümü ancak
`tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
kapıları PASS + sertifika + kullanıcının açık onayıyla **final** olur:

- **Kapı 0** kapsam/gizlilik → **1** derin literatür/künye evreni →
  **2** full-text/Zotero/Anamnesis → **3** metin/kılavuz uyumu →
  **4** Türkçe imla/akış (`sci-audit` axis G) → **5** AI-reliability/render
  (`sci-audit` axes A-F + repo ai-audit).

Sertifika `tez-yazim/04_kalite-kontrol/sertifikalar/<bolum>-sertifika-YYYY-MM-DD.md`.
Teknik kapılar geçse bile onay yoksa en fazla `provisional-pass`.

---

## 12. LLM / MCP Kullanım Beyanı

Harici AI/MCP/plugin çıktısı tez içeriğini etkilediyse oturum bitmeden
`/ai-kayit` → `./dmnitel log-ai-use … --external-api-used yes`. `--data-type`
daima "anonim/türetilmiş"; ham/kimliklenebilir bayrakları `no` (kod düzeyinde
zorlanır: `no` değilse `ValueError`). Kayıt
`03_analysis/methodology/llm_use_statement.md` beyanının temelidir.

---

## 13. Skill Devir Noktaları

| Soru | Devir |
|---|---|
| Karma yöntem / joint display / GRAMMS / MMAT | `t1dm-tez-rehberi/references/karma-yontem.md` |
| EMBU CFA/IRT, Beck/KİA psikometri | `t1dm-tez-rehberi/references/psikometri-pipeline.md` |
| H5 diadik tutarlılık (ICC/Bland-Altman/RSA/k) | `t1dm-tez-rehberi/references/h5-diadik-tutarlilik.md` |
| RTA 6-faz, COREQ/SRQR/JARS-Qual, KVKK, refleksivite, jüri | `niteliksel-arastirma-rehberi-t1dm` (ilgili `references/…md`) |
| Dış literatür/tam metin/citation/KOL | Evidentia süiti (§8) |
| Bölüm Quarto + Carbon render | `carbon-quarto-scientific` |
| Codebook / joint display / tema tablosu HTML | `carbon-html-report` |
| Oturum devri | `remember` (`.remember/` yerelde) |

---

## 14. Kaynak Belgeler ve Bakım Kuralları

**Bu playbook'un birleştirdiği kaynaklar (bağlayıcı otorite onlarda kalır):**

| Belge | Rol |
|---|---|
| `00_context/TALIMATNAME_TEZ_YAZIM.md` | Claude Code zorunlu talimatname (hook-zorlamalı) |
| `00_context/CODEX_PLAYBOOK.md` | Codex ikizi |
| `00_context/TOOL_ECOSYSTEM_MAP.md` | Araç/MCP/plugin/skill envanteri |
| `doktoratezi/tez-yazim/README.md` | 10-adımlı resmi yazım sırası |
| `doktoratezi/tez-yazim/00_kaynak-kurallari/format-kontrati.md` | Biçim/istatistik/nitel/karma kontratları |
| `doktoratezi/tez-yazim/00_kaynak-kurallari/tam-metin-erisim-kaskadi.md` | Tam metin kaskadı (§7 kaynağı) |
| `doktoratezi/tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` | 6-kapılı referans ledger'ı |
| `doktoratezi/tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | Kapı 0–5 sertifikasyonu |
| `doktoratezi/tez-yazim/04_kalite-kontrol/turkce-bilimsel-yazim-denetimi.md` | `sci-audit` axis G kanonik kullanım ve provider degrade kuralı |
| `niteliksel-arastirma-rehberi-t1dm/references/13-mcp-ve-skill-baglantilari.md` | Nitel-arm MCP/Evidentia köprüsü |
| `t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` | Nicel/karma Evidentia köprüsü + D0–D6 |
| `CONVENTIONS.md` (iki-kol) | Hook'la enjekte edilen AI-reliability sözleşmeleri |

**Bakım kuralları:**
1. Politika/hook değişikliği **önce kaynak belgede** (talimatname → Codex ikizi →
   `.claude/hooks` ↔ `.codex/hooks` + `tests/`), **sonra** bu playbook.
2. Yeni MCP/plugin/skill eklenince `TOOL_ECOSYSTEM_MAP.md` + bu playbook §6 aynı
   commit'te güncellenir.
3. Bu belge envanter+indekstir, **yetki vermez**: default-off/koşullu bir aracın
   kullanımı kullanıcının açık isteğini gerektirir.
4. Çelişkide §0 öncelik sırası uygulanır.

---

## Ek A — Bu Playbook'un GENEL BİLGİLER Bölümüne Uygulanışı (worked example)

`chapters/02_genel_bilgiler.qmd` bölümü bu entegre yapıyla şöyle güncellenir:

1. **Rota (§1–§5):** GENEL BİLGİLER = nicel/karma yazım kolu (merkez
   `doktoratezi/tez-yazim`) + dış kanıt kolu (Evidentia); iç nitel kol yalnız
   triadik tasarımın kavramsal gerekçesiyle temsil edilir (§2.19, §2.23).
2. **Referans disiplini (§9):** bölüme eklenen her kaynak ledger'da `cite-ok`
   olmalı. Zaten `cite-ok` olan ve GENEL BİLGİLER'e uygun kaynaklar (ör.
   `@pinquart2013` kronik hastalıkta ebeveynlik farkı; `@crandell2017`
   ebeveynlik boyutları ↔ psikososyal sonuç) yeni dış retrieval gerektirmeden,
   ledger Bölüm sütunu genişletilerek yeniden kullanılır.
3. **Tam metin (§7):** yeni bir kaynak gerekiyorsa T1→T5 kaskadı + Zotero
   kapanışı; erişilemezse `full-text-exception` = citation yok.
4. **Kanıt türü etiketi (§4–§5):** GENEL BİLGİLER kavram açıklar; bulgu, etki
   büyüklüğü, nitel tema **vermez** (format-kontratı).
5. **Kapanış (§10–§12):** iki-kol AI-reliability + `quarto render`; harici MCP
   kullanıldıysa `/ai-kayit`.
6. **Final (§11):** Kapı 0–5 sertifikasyonu + açık onay olmadan bölüm taslaktır.
