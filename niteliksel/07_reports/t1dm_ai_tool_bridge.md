# T1DM Niteliksel AI Tool Bridge

Repo profile: `t1dm_qualitative_thesis`
Local gate: `dmnitel + niteliksel-arastirma-rehberi-t1dm`
Codex playbook: `00_context/CODEX_PLAYBOOK.md`
Nicel kök: `/workspaces/T1DM-Tez`
Thesis writing root: `/workspaces/T1DM-Tez/tez-yazim`

## Official Thesis Sources
- `/workspaces/T1DM-Tez/docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf`
- `/workspaces/T1DM-Tez/docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx`

## Thesis Writing Entrypoints
- `/workspaces/T1DM-Tez/tez-yazim/README.md`
- `/workspaces/T1DM-Tez/tez-yazim/06_kritik-kaynaklar/README.md`
- `/workspaces/T1DM-Tez/tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv`
- `/workspaces/T1DM-Tez/tez-yazim/00_kaynak-kurallari/format-kontrati.md`
- `/workspaces/T1DM-Tez/tez-yazim/01_mimari/yetkinlik-ve-arac-mimarisi.md`

## Operational Order
- Once 00_context/CODEX_PLAYBOOK.md dosyasini ana Codex playbook olarak kullan.
- Tez yazim/format islerinde ana calisma merkezini /workspaces/T1DM-Tez/tez-yazim olarak kabul et ve resmi docs/tez-kilavuz kaynaklarini ust kural yap.
- Her tez yazim oturumunda klinik/nitel rapor, protokol, ham/kilitli veri ve olcek-form secimini once /workspaces/T1DM-Tez/tez-yazim/06_kritik-kaynaklar/README.md ve manifest TSV ile yap.
- Once ./dmnitel route-tool ile sorunun yerel nitel, dis-kanit veya nicel-pipeline oldugunu ayir.
- Nitel kol yetkinliklerini yalniz tezde nitel kolun ilgili kesimleri yazilirken veya kanonik nitel sonuc raporu denetlenirken ac.
- Her tez yazim oturumunda ./dmnitel ai-context ve Anamnesis/context gate ile anonim/turetilmis baglami sabitle.
- Diger MCP'leri yalniz gorev sinyaliyle ac: YOK/ERIC akademik, mevzuat, klinik terminoloji/regulasyon, render/browser, GitHub veya teknik platform kapilari ayri tutulur.
- Karma tez veya joint display sorularinda ./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md ile iki-kol kaynak haritasini guncelle.
- Yerel nitel denetimde ./dmnitel komutlarini calistir; ham katilimci verisi dokme.
- Dis literatur/tam metin/YOK/OSF/KOL gerekiyorsa Evidentia MCP cekirdegini ac ve Anna's Library full-text gate'i en onemli referans kapisi olarak kullan.
- Genetik/varyant/protein/pathway/omics/farmakoloji/clinical trial sorularinda life-science-research plugin router'ini kosullu ac.
- Kaynakca, citation key, references.bib veya kutuphane senkronu gerekiyorsa once tam metin/claim ledger'ini kapat, sonra .env ZOTERO_API_KEY kullanan Zotero Web API bridge'ini kullan.
- Referansli bolum kapanisinda nitel ve nicel AI-reliability kontrollerini birlikte calistir.
- Nicel H1-H5, EMBU, Beck, KIA veya targets sorusu varsa nicel kök + t1dm-tez-rehberi akisini kullan.
- Her harici AI/MCP kullanimini ./dmnitel log-ai-use ile kaydet.

## Dmnitel Commands
- `./dmnitel ai-context` — Ajan icin repo-ozel dmnitel + Anamnesis/context + Evidentia + t1dm-tez bridge ozetini guvenli bicimde verir.
- `./dmnitel route-tool --query "<soru>"` — Soruya gore dmnitel, Evidentia veya paired doktoratezi/t1dm-tez akisini secer.
- `./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md` — Nitel kol ve nicel kök kaynaklarini resmi Marmara tez kilavuzu merkezli tek karma tez yazim akisi icin guvenli bicimde haritalar.
- `./dmnitel lint-codebook 02_codebook/codebook.csv` — Kod kitabi tutarliligi ve alan eksikleri.
- `./dmnitel build-triadic-matrix --coded-data <coded.csv> --output 04_triadic_matrices/<name>.csv` — Anne, T1DM cocuk ve saglikli kardes rolleri icin tema/subtema matrisi.
- `./dmnitel check-quotes --source <deidentified-source> --quotes <quotes.csv>` — Kullanilan anonim alintilarin kaynakla butunlugu.
- `./dmnitel audit-coreq --methods <methods.md> --results <results.md>` — COREQ 32 madde metin ici kanit denetimi.
- `./dmnitel find-negative-cases --coded-data <coded.csv> --theme "<tema>"` — Tema icin alternatif/negatif vaka adaylari.
- `./dmnitel log-ai-use --tool "<tool>" --model "<model>" --purpose "<amac>" --data-type "<anonim/turetilmis>" --output-summary "<ozet>"` — Evidentia/Codex/MCP kullaniminin LLM beyan ve audit trail kaydi.

## Evidentia Default MCP Core
- `evidentia-skills`
- `pubmed-epmc`
- `paper-search`
- `openalex`
- `semantic-scholar`
- `psyarxiv-osf`
- `yoktez-mcp`
- `anamnesis`
- `evidentia-kb`
- `annas-reader`

## Task-Gated MCP Layers
- **context_memory**: `anamnesis`, `memory`, `qdrant`, `sequentialthinking`
  - Purpose: Oturum bağlamı, karar geçmişi, önceki güvenli çalışma notları ve kompleks planlama.
  - Boundary: Ham transcript, demografi satırı, .env, credential veya aile düzeyi hassas içerik gönderilmez.
- **biomedical_literature**: `evidentia-skills`, `pubmed-epmc`, `paper-search`, `openalex`, `semantic-scholar`, `psyarxiv-osf`, `evidentia-kb`, `annas-reader`, `biocontext_kb`, `meta-analysis-skills`
  - Purpose: Biyomedikal literatür, tam metin, DOI/PMID/PMCID, preprint ve dış kanıt sentezi.
  - Boundary: Anna's full-text ve Zotero ledger kapanmadan citation yazılmaz.
- **turkish_academic**: `yoktez-mcp`, `yok-akademik`, `eric-mcp`
  - Purpose: YÖK tezleri, Türkiye akademik bağlamı ve okul/eğitim literatürü.
  - Boundary: YÖK tam metinleri telif ve alıntı sınırıyla özetlenir; uzun metin kopyalanmaz.
- **clinical_terminology_regulatory**: `openfda`, `med-terminologies`, `nlm-rxnorm`, `nih-clinicaltables`, `iuphar-gtopdb`, `drugddx`, `titck-cache`
  - Purpose: İlaç, ATC/RxNorm, ICD/SNOMED, FDA/TITCK ve klinik terminoloji doğrulaması.
  - Boundary: Tedavi önerisi veya hasta düzeyi karar üretimi yapılmaz; tez terminolojisi ve kaynak doğrulamasıyla sınırlıdır.
- **turkish_legislation**: `mevzuat`, `mevzuat-bilgisi`
  - Purpose: KVKK, etik kurul, sağlık mevzuatı, yönetmelik, tebliğ ve resmi metin doğrulaması.
  - Boundary: Hukuki yorum yerine resmi madde/kaynak doğrulaması yapılır.
- **technical_delivery**: `playwright`, `chrome-devtools`, `brave-search`, `github`, `filesystem`
  - Purpose: Quarto/HTML/PDF render kontrolü, ekran görüntüsü, güncel web doğrulaması, GitHub ve dosya operasyonları.
  - Boundary: Raw data ve credential dosyaları açılmaz; GitHub/write işlemleri açık talimat gerektirir.
- **platform_design_default_off**: `firebase`, `supabase`, `cloudflare-api`, `figma`, `openai-api-key-local-confirmation`
  - Purpose: Tez dışı teknik platform, tasarım veya API anahtarı kurulum işleri.
  - Boundary: Tez yazımında varsayılan kapı değildir; yalnız açık teknik istekle kullanılır.

## Conditional Plugin Layers
- `life-science-research:research-router-skill` — Genetik, varyant, protein, pathway, farmakoloji, klinik calisma, omics/public dataset ve mekanistik T1DM biyolojisi.
- `zotero:Zotero` — Zotero Web API arama/export, yerel Zotero kutuphanesi, BibTeX sync, citation insertion ve kaynakca mutabakati.

## Zotero Web API Commands
- `python3 scripts/util/zotero_env_bridge.py status --json`
- `python3 scripts/util/zotero_env_bridge.py search "<query>" --json --with-bibtex-keys`
- `python3 scripts/util/zotero_env_bridge.py export-bibtex --out references/references.bib`
- `python3 scripts/util/zotero_env_bridge.py cite --query "<title>" --markdown <draft.md> --bib references/references.bib --marker '<cite>'`

## Zotero Desktop Local API Commands
- `python3 ~/.codex/plugins/cache/openai-curated-remote/zotero/0.1.2/skills/zotero/scripts/zotero.py status --json`
- `python3 ~/.codex/plugins/cache/openai-curated-remote/zotero/0.1.2/skills/zotero/scripts/zotero.py fulltext <attachment-key> --out <fulltext.txt>`

## Safe Repo Evidence
- `03_analysis/codebook/codebook_v2.md`
- `03_analysis/methodology/coreq_32_completed.md`
- `03_analysis/methodology/audit_trail.md`
- `03_analysis/methodology/llm_use_statement.md`
- `03_analysis/methodology/A1_information_power.md`
- `03_analysis/methodology/A9_triadic_methodology_literature.md`
- `07_reports/`

## Protected Inputs
- `01_raw_data/`
- `02_processed/transcripts/`
- `01_deidentified/`
- `00_raw_locked/`
- `.remember/`
