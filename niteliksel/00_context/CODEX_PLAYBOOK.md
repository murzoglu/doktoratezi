# T1DM Karma Tez Codex Playbook

> **Migrasyon notu (2026-07-09):** Bu playbook'un canonical kopyası artık
> `/mnt/thunderbolt/workspaces/doktoratezi/niteliksel` altındadır.
> Nitel araçlar bu alt-ağaçtan (`cd niteliksel && ./dmnitel ...`)
> çalıştırılır; üst tez yazım merkezi hâlâ `/mnt/thunderbolt/workspaces/doktoratezi/tez-yazim`dir.

Bu dosya bu workspace'teki nitel repo işlemleri için koruyucu operasyonel
playbook'tur. Bundan sonraki tez yazım sürecinin ana çalışma dizini
`/mnt/thunderbolt/workspaces/doktoratezi`, ana operasyon merkezi ise
`/mnt/thunderbolt/workspaces/doktoratezi/tez-yazim` klasörüdür. Bu nitel repo,
tezde yalnız nitel kolun ilişkili kesimleri yazılırken kaynak/denetim katmanı
olarak açılır.

## Resmi Tez Yazım Kaynakları

Tez yazımı, format, bölüm sırası, özet/summary, tablo/şekil ve kaynakça işlerinde
üst kaynak nicel repo içindeki yazım merkezidir:

- `/mnt/thunderbolt/workspaces/doktoratezi/tez-yazim/README.md`
- `/mnt/thunderbolt/workspaces/doktoratezi/tez-yazim/06_kritik-kaynaklar/README.md`
- `/mnt/thunderbolt/workspaces/doktoratezi/tez-yazim/00_kaynak-kurallari/format-kontrati.md`
- `/mnt/thunderbolt/workspaces/doktoratezi/docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf`
- `/mnt/thunderbolt/workspaces/doktoratezi/docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx`

Bu kaynaklar çakışırsa resmi `docs/tez-kilavuz` dosyaları format, başlık,
ondalık virgül, kaynakça ve bölüm sırası kararlarında eski repo notlarının
üzerindedir.

## Her Oturumun Başlangıcı

1. `CLAUDE.md`, `AGENTS.md`, `00_context/TRACKER.md`, `00_context/REPO_CONTEXT.md` ve bu dosyayı oku.
2. Soru net değilse önce `./dmnitel route-tool --query "<soru>"` çalıştır.
3. Tez yazımı veya format isteniyorsa çalışma merkezini `doktoratezi` olarak
   değiştir; önce `doktoratezi/tez-yazim/README.md`,
   `doktoratezi/tez-yazim/06_kritik-kaynaklar/README.md`,
   `doktoratezi/tez-yazim/01_mimari/tez-yazim-ana-plani.md` ve
   `doktoratezi/docs/tez-kilavuz` resmi kaynaklarını esas al.
4. Her tez yazım oturumunda `./dmnitel ai-context` ve Anamnesis/context kapısı ile
   anonim/türetilmiş çalışma bağlamını sabitle.
5. Karma tez, joint display, nicel-nitel sentez veya iki repo birlikte isteniyorsa
   `./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md`
   çalıştır.
6. Dış kaynak, tam metin, citation audit, YÖK/OSF/KOL gerekiyorsa Evidentia v1.7.0
   `medical-research` v8.5.0 çalışma sözleşmesine geç: native-first, semantic coverage,
   retrieve-don't-dump ve no-web/OSINT. Her referansta EPMC/legal-OA/Paper Search
   sonrası Anna's Library/annas-reader copyright-gated fallback kapısını denetle.
7. Manüskript adli denetimi, Türkçe bilimsel yazım/imla veya bölüm sertifikasyonu
   gerekiyorsa `sci-audit@cureonics-marketplace` v0.2.0 kapısını aç: Kapı 4
   `/sci-audit:check-turkish`, Kapı 5 `/sci-audit:audit` + `/sci-audit:audit-report`.
   Eski repo-local `tr_sciaudit.py` scaffold'u kurulmaz; KVKK/ham veri/quote-parity
   denetimi `dmnitel` ve iki repo ai-audit katmanında kalır.
8. Citation eklemeden önce Zotero item key, BibTeX key, DOI/PMID/ID, tam metin kanıtı ve
   claim/pasaj notunu `doktoratezi/tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`
   içinde kapat.
9. Referanslı bölüm kapanışında nitel ve nicel AI-reliability kontrollerini birlikte çalıştır.
10. Harici MCP/plugin sonucunu tez yazımında kullandıysan `./dmnitel log-ai-use ... --external-api-used yes`
   ile kayıt düş.

## Veri Sınırı

- Nitel repo korumalı alanları: `01_raw_data/`, `02_processed/transcripts/`, `01_deidentified/`,
  `00_raw_locked/`, `.remember/`.
- Nicel repo korumalı alanları: `data/raw/`, `data/identified/`, `data/cleaned/`,
  `data/backup/`, `data/processed/*`, `outputs/*`, `_targets/`.
- Bu alanlardan satır düzeyi içerik, aile düzeyi hassas detay, ham alıntı, demografi satırı,
  onam/protokol kişisel içeriği memory'ye veya harici MCP/RAG'e taşınmaz.
- Tezde yalnız araştırmacı tarafından seçilmiş anonim alıntı, kod/tema düzeyi türetilmiş bilgi,
  COREQ/audit trail/codebook çıktısı, kanonik nitel sonuç raporu ve nicel
  tarafta testlenmiş aggregate sonuç kullanılır.
- Nitel repo, kanonik sonuç raporu doktoratezi tarafına aktarıldıktan sonra
  genel tez yazımı için yeniden taranmaz; yalnız ilgili yöntem, bulgular,
  joint display, tartışma veya ek kesiminde kanıt denetimi gerekirse açılır.

## Araç Kayıt Defteri

| Araç | Ne zaman kullanılır | Denetim durumu |
|---|---|---|
| `./dmnitel ai-context` | Repo-özel güvenli tool bridge özeti | PASS |
| `./dmnitel route-tool` | Tool seçimi belirsiz her iş | PASS |
| `./dmnitel cross-repo-status` | Resmi kılavuz merkezli karma tez/joint display/iki repo yazım koordinasyonu | Unittest ile korunuyor |
| `./dmnitel lint-codebook` | Codebook CSV tutarlılığı | Unittest yüzeyi var |
| `./dmnitel build-triadic-matrix` | Kodlu segmentlerden triadik matris | Unittest yüzeyi var |
| `./dmnitel check-quotes` | Anonim alıntı bütünlüğü | Unittest yüzeyi var |
| `./dmnitel audit-coreq` | COREQ metin içi kanıt denetimi | Unittest yüzeyi var |
| `./dmnitel find-negative-cases` | Tema yorumu öncesi negatif/alternatif vaka arama | Unittest yüzeyi var |
| `./dmnitel log-ai-use` | Harici AI/MCP/plugin kullanım kaydı | Unittest yüzeyi var |
| `t1dm-qual-ai-audit` plugin/skill | Nitel repo hook, privacy, route, reliability denetimi | 55/55 PASS |
| `doktoratezi-ai-audit` plugin/skill | Nicel repo hook, raw-data, claim grounding denetimi | 142/142 PASS |
| Codex hooks | SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop guardrail | py_compile PASS, regression PASS |
| `codex_mcp_roster_redacted.py` | MCP roster kontrolü; raw `codex mcp list` yerine | PASS, token redaction doğrulandı |
| Promptfoo offline gate | Repo policy golden-case regression | Nitel 4/4 PASS, nicel 4/4 PASS |
| Anamnesis/context gate | Oturum bağlamı, karar geçmişi ve tez çalışma belleği | Anonim/türetilmiş context-only kullanım |
| Evidentia v1.7.0 / `medical-research` v8.5.0 | Dış literatür, YÖK/OSF/KOL, tam metin, semantic coverage ve clean-copy kanıt sentezi | Claude Code kaynak sözleşmesi: `CONNECTORS.md` + canonical cache; no-web-tier, native-first, gap-log |
| `sci-audit@cureonics-marketplace` v0.2.0 | Manüskript adli denetimi ve Türkçe bilimsel yazım/imla; Kapı 4 axis G, Kapı 5 axes A-F | Doktoratezi `tez-yazim` Kapı 4/5 üst kural; repo-local `tr_sciaudit.py` kopyası yok; KVKK/quote-parity kapsam dışı |
| Anna's Library / `annas-reader` | DOI/MD5 tam metin, OCR, sayfa/pasaj ve claim doğrulama | Copyright-gated fallback tam-metin kaynağı: EPMC/legal-OA/Paper Search sonrası, Zotero öncesi; citation öncesi kapanması zorunlu kapı |
| Zotero Web API bridge | `references.bib`, citation key, search/export/cite | Status PASS, key redacted |
| Zotero Desktop local API | Lokal full-text/attachment/connector | API kapalı; Zotero app açıkken kullanılabilir |
| `06_tools/scripts/*.py` | DOCX/Markdown dönüştürme ve transcript kalite işleri | Varsayılan değil; `python-docx` ve yedek kontrolü gerekir |
| `scripts/util/integrate_t1dm_qualitative_repo.py` | Nicel repodan nitel scaffold materyalizasyonu | Çalıştırma rutin değil; geniş overwrite/back-up yüzeyi var |
| `plugins/eric-mcp-server` | Eğitim/okul/akademik uyum literatürü için ERIC MCP | Nicel repo plugin yüzeyi; koşullu |

## Skill ↔ Evidentia Entegrasyonu (üç kollu kanıt hattı)

İki rehber skill ile Evidentia tek entegre hat olarak çalışır:

- **İç nitel veri** (RTA/codebook/COREQ/alıntı/triad) → `./dmnitel` +
  `niteliksel-arastirma-rehberi-t1dm`. Köprü: `references/13-mcp-ve-skill-baglantilari.md`.
  Ham veri connector'a gitmez.
- **Dış literatür/tam metin/citation/KOL** → Evidentia v1.7.0 `medical-research`
  v8.5.0 (Adım 0.4 semantic scope + native-first connector ladder + clean-copy)
  + EPMC/legal-OA/Paper Search + Anna's Library copyright-gated fallback + Zotero
  + ledger. Her iki skill de dış literatürü ham MCP'ye değil Evidentia'ya yönlendirir.
- **Manüskript adli denetimi/Türkçe imla** → `sci-audit@cureonics-marketplace`
  v0.2.0. Kapı 4 axis G (`/sci-audit:check-turkish`), Kapı 5 axes A-F
  (`/sci-audit:audit` + `/sci-audit:audit-report`). Bu katman KVKK/ham veri/
  quote-parity denetimini devralmaz; repo ai-audit katmanları ayrı çalışır.
- **Nicel/karma köprü** (H5, joint display, IRR) → `t1dm-tez-rehberi`. Köprü:
  `references/literatur-kanit-evidentia.md` + `karma-yontem.md`. Önce
  `./dmnitel cross-repo-status`.

Güncel MCP adları (eski→yeni): `Hukuki_Veritabanlar→Yarg`, `Mevzuat→Mevzuat_Bilgisi`,
`Sequential_Thinking→sequentialthinking`, `Fetch→WebFetch`.

## MCP ve Plugin Kapıları

Varsayılan Evidence MCP çekirdeği dış kanıt veya referans yönetimi gerektiğinde açılır:
`evidentia-skills`, `pubmed-epmc`, `paper-search`, `openalex`, `semantic-scholar`,
`psyarxiv-osf`, `yoktez-mcp`, `anamnesis`, `evidentia-kb`, `annas-reader`.
Claude Code tarafında tek doğruluk kaynağı
`/mnt/thunderbolt/workspaces/evidentia-cc/plugins/evidentia/CONNECTORS.md`;
`/mnt/thunderbolt/workspaces/evidentia-cc/plugins/evidentia/shared/canonical-cache-contract.md`
tek-fetch/retrieve-don't-dump disiplinini zorlar. Bu projede `psyarxiv-osf`
config hazır fakat endpoint 404 bloklu; worker düzelene kadar fallback
`paper-search` + `openalex`.

Anamnesis/context gate, ham veri taşımadan oturum bağlamını ve karar geçmişini
sabitler. Anna's Library/annas-reader, dış kaynakların tam metin ve claim
doğrulamasında Zotero'dan önce gelir; Zotero citation key/BibTeX mutabakatı
tam metin kapısı kapandıktan sonra yapılır.

Koşullu katmanlar:

- `life-science-research:research-router-skill`: genetik, varyant, protein, pathway,
  farmakoloji, klinik çalışma, omics/public dataset veya mekanistik T1DM biyolojisi.
- `zotero:Zotero`: Zotero library, citation key, BibTeX/RIS, `references.bib`,
  local full-text index ve citation insertion. Import/write için açık onay gerekir.
- `eric-mcp`: okul, eğitim, akademik uyum ve çocuk gelişimi literatürü.
- `openfda`, `med-terminologies`, `nlm-rxnorm`, `nih-clinicaltables`, `iuphar-gtopdb`,
  `drugddx`: ilaç, tanı, terminoloji, farmakoloji veya klinik tablo işleri.
- `mevzuat`, `mevzuat-bilgisi`, `titck-cache`: Türkiye mevzuatı, TITCK, ilaç/regülasyon işleri.
- `brave-search`, `chrome-devtools`, `playwright`, `github`, `firebase`, `supabase`,
  `cloudflare-api`, `figma`, `filesystem`, `qdrant`, `memory`, `sequentialthinking`,
  `biocontext_kb`, `meta-analysis-skills`, `openai-api-key-local-confirmation`,
  `pophive`, `yok-akademik`: sadece açık task gerektirirse kullanılır; tez literatür
  kaskadının parçası değildir.

## Görev Kapılı MCP Matrisi

| Kapı | MCP'ler | Kullanım | Sınır |
|---|---|---|---|
| Bağlam ve planlama | `anamnesis` (birincil: `corpus_stats`/`semantic_search`/`hybrid_query`/`ingest_document`; Evidentia semantic coverage + tam-metin RAG altyapısı), `evidentia-kb` (`kb_search`/`kb_upsert`), `memory`, `qdrant`, `sequentialthinking` | Oturum bağlamı, karar geçmişi, türetilmiş karar özeti persist, dış tam-metin RAG, kompleks plan ayrıştırma. | Yalnız anonim/türetilmiş `ingest`/`upsert`; raw transcript, demografi satırı, PII, `.remember/`, `.env`, credential yok; tam metin ham dökülmez, sınırlı retrieval yapılır. |
| Biyomedikal literatür | `evidentia-skills`, `pubmed-epmc`, `paper-search`, `openalex`, `semantic-scholar`, `psyarxiv-osf`, `evidentia-kb`, `annas-reader`, `biocontext_kb`, `meta-analysis-skills` | Literatür, full-text, DOI/PMID/PMCID, preprint, dış kanıt sentezi; `medical-research` v8.5 native-first/no-web-tier sözleşmesi. | EPMC/legal-OA/Paper Search/Anna's tam metin ve Zotero ledger kapanmadan citation yok; bulunamayan veri gap-log. |
| Türkiye akademik | `yoktez-mcp`, `yok-akademik`, `eric-mcp` | YÖK tezleri, Türkiye akademik bağlamı, okul/eğitim literatürü. | YÖK tam metinleri yalnız hedefli sayfa/pasaj düzeyinde özetlenir. |
| Klinik terminoloji/regülasyon | `openfda`, `med-terminologies`, `nlm-rxnorm`, `nih-clinicaltables`, `iuphar-gtopdb`, `drugddx`, `titck-cache` | İlaç, ATC/RxNorm, ICD/SNOMED, FDA/TITCK ve terminoloji doğrulaması. | Hasta düzeyi tedavi önerisi üretilmez. |
| Türkiye mevzuatı | `mevzuat`, `mevzuat-bilgisi` | KVKK, etik kurul, sağlık mevzuatı, yönetmelik ve tebliğ doğrulaması. | Hukuki tavsiye değil, resmi madde/kaynak doğrulaması. |
| Teknik teslim | `playwright`, `chrome-devtools`, `brave-search`, `github`, `filesystem` | Quarto/HTML/PDF render, screenshot, GitHub, güncel web ve dosya operasyonları. | Raw data ve credential dosyaları açılmaz; GitHub write açık talimat ister. |
| Platform/design default-off | `firebase`, `supabase`, `cloudflare-api`, `figma`, `openai-api-key-local-confirmation` | Tez dışı platform, tasarım, deploy veya API anahtarı işleri. | Tez yazımında varsayılan değil; yalnız açık teknik istekle. |

MCP roster 2026-06-30 tarihinde redacted komutla kontrol edildi; roster araçları enabled
görünüyor. Bazı araçlarda `Not logged in` veya `Unsupported` auth etiketi var; bu durum
araç çağrısı gerektiğinde ayrıca doğrulanmalıdır.

## İki Repo Yazım Modeli

| Tez bölümü | Nitel kaynak | Nicel kaynak | Tool gate |
|---|---|---|---|
| `GİRİŞ ve AMAÇ` / `GENEL BİLGİLER` | Kanonik nitel rapor gerekirse arka plan; geniş nitel repo taraması default değil | `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md`, CSR, SAP | Anamnesis + Evidentia + Anna's + Zotero + çift AI-reliability |
| `GEREÇ ve YÖNTEM` | COREQ, audit trail, positionality, LLM statement | `tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md`, `_targets.R`, veri haritası | Resmi kılavuz + kanonik nitel yöntem kanıtı |
| `BULGULAR` | Kanonik nitel sonuç raporu, 4 makro tema, quote integrity | `tez-yazim/03_bolum-hazirlik/04_bulgular.md`, H1-H5, EMBU/Beck/KIA | Repo artefaktı ve test kanıtı |
| `TARTIŞMA ve SONUÇ` | Negatif vaka, refleksivite, triadik yorum | `tez-yazim/03_bolum-hazirlik/05_tartisma-ve-sonuc.md`, Faz II post-hoc sınırları | Anamnesis + Evidentia + Anna's + nedensellik sınırı + çift AI-reliability |
| `KAYNAKLAR` / `EKLER` | COREQ, codebook, audit trail, LLM statement | `tez-yazim/03_bolum-hazirlik/06_kaynaklar-ekler.md`, references.bib, kanonik formlar | Anna's ledger + Zotero + format kontrol |

Yazımda nitel tema, nicel estimate gibi sunulmaz. Nicel sonuçlar nitel bulguların
mekanistik veya nedensel kanıtı değildir; karma yorum katmanı iki kolu yan yana getirir
ve kanıt türlerini açıkça ayırır.

## Doğrulama Paketi

Dar kapsamlı nitel değişiklik:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

Nitel AI/tool değişikliği:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py
npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml
python3 .codex/tools/codex_mcp_roster_redacted.py
```

Karma tez/cross-repo değişikliği:

```bash
./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

Nicel repo veri-yönetişimi kontrolü:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
Rscript tests/test_reproducibility_lock.R
Rscript tests/test_final_reference_loading.R
Rscript tests/test_data_governance.R
PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
```

## İş Bitirme Kriteri

- Hangi repo koluna dokunulduğu açık.
- Kullanılan kaynaklar dosya yolu ile izlenebilir.
- Ham veri sınırı korunmuş.
- Gerekli local test veya regression komutu exit 0 ile bitmiş.
- Harici MCP/plugin sonucu tez içeriğini etkilediyse `99_ai_use_log/ai_use_log.csv` güncellenmiş.
- Kullanıcı commit istemediyse stage/commit/push yapılmamış.
