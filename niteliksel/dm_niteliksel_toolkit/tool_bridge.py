from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .common import normalize_key


QUALITATIVE_REPO = str(Path(__file__).resolve().parents[1])
PAIRED_QUANTITATIVE_REPO = "/mnt/thunderbolt/workspaces/doktoratezi"
CODEX_PLAYBOOK = "00_context/CODEX_PLAYBOOK.md"
CROSS_REPO_STATUS_COMMAND = "./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md"
THESIS_WRITING_ROOT = f"{PAIRED_QUANTITATIVE_REPO}/tez-yazim"
CRITICAL_SOURCE_MANIFEST = f"{THESIS_WRITING_ROOT}/06_kritik-kaynaklar/README.md"
CRITICAL_SOURCE_MANIFEST_TSV = f"{THESIS_WRITING_ROOT}/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv"
OFFICIAL_THESIS_GUIDE = f"{PAIRED_QUANTITATIVE_REPO}/docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf"
OFFICIAL_THESIS_TEMPLATE = f"{PAIRED_QUANTITATIVE_REPO}/docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx"

EVIDENTIA_PLUGIN_VERSION = "1.7.0"
EVIDENTIA_FLAGSHIP_SKILL = "medical-research"
EVIDENTIA_FLAGSHIP_VERSION = "8.5.0"
EVIDENTIA_LOCAL_CONFIG = ".claude/evidentia.local.md"
EVIDENTIA_CONNECTOR_SOURCE = "/mnt/thunderbolt/workspaces/evidentia-cc/plugins/evidentia/CONNECTORS.md"
EVIDENTIA_CACHE_CONTRACT = "/mnt/thunderbolt/workspaces/evidentia-cc/plugins/evidentia/shared/canonical-cache-contract.md"

SCI_AUDIT_PLUGIN_NAME = "sci-audit@cureonics-marketplace"
SCI_AUDIT_PLUGIN_VERSION = "0.2.0"
SCI_AUDIT_LOCAL_CONFIG = ".claude/sci-audit.local.md"
SCI_AUDIT_CACHE_ROOT = "/home/mahirkurt/.claude/plugins/cache/cureonics-marketplace/sci-audit"
SCI_AUDIT_TURKISH_STYLE_SCRIPT = "skills/turkish-sci-style/scripts/tr_sciaudit.py"
SCI_AUDIT_TURKISH_RULES = f"{THESIS_WRITING_ROOT}/04_kalite-kontrol/turkce-bilimsel-yazim-denetimi.md"
SCI_AUDIT_CERTIFICATION_PLAYBOOK = f"{THESIS_WRITING_ROOT}/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md"

SCI_AUDIT_CLAUDE_CODE_SURFACE = [
    "/sci-audit:audit",
    "/sci-audit:check-turkish",
    "/sci-audit:verify-citations",
    "/sci-audit:check-stats",
    "/sci-audit:guideline-check",
    "/sci-audit:audit-report",
    "/sci-audit:ai-log",
]

SCI_AUDIT_TEZ_YAZIM_RULES = [
    f"{THESIS_WRITING_ROOT}/README.md",
    f"{THESIS_WRITING_ROOT}/00_kaynak-kurallari/README.md",
    f"{THESIS_WRITING_ROOT}/00_kaynak-kurallari/talimatname-claude-code.md",
    f"{THESIS_WRITING_ROOT}/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md",
    f"{THESIS_WRITING_ROOT}/00_kaynak-kurallari/format-kontrati.md",
    f"{THESIS_WRITING_ROOT}/01_mimari/yetkinlik-ve-arac-mimarisi.md",
    SCI_AUDIT_TURKISH_RULES,
    SCI_AUDIT_CERTIFICATION_PLAYBOOK,
]

SCI_AUDIT_WORKFLOW_RULES = [
    f"Kanonik arac `{SCI_AUDIT_PLUGIN_NAME}` v{SCI_AUDIT_PLUGIN_VERSION}; repo-local `tr_sciaudit.py` kopyasi veya eski `.venv-tr-sciaudit` scaffold'u kullanilmaz.",
    "Kapı 4: Turkce bilimsel yazim/imla icin axis G; `/sci-audit:check-turkish <dosya> --strictness certification` veya plugin-bundled CLI.",
    "Kapı 5: manuskript adli denetimi icin axes A-F; `/sci-audit:audit <dosya> --lang tr --strictness certification --type <coreq|srqr|strobe|prisma|jars>` ve `/sci-audit:audit-report`.",
    "AI-reliability katman siniri: sci-audit referans/claim/istatistik/halusinasyon/kilavuz/AI-seffaflik/Turkce imla denetler; KVKK, ham veri, quote-parity ve kanonik kilit repo ai-audit + dmnitel'dedir.",
    "Tez-yazim Kapı 0-5 sertifikasyon playbook'u, resmi Marmara format talimatnamesi ve kalite-kontrol listeleri ust kuraldir.",
    "Axis G deterministik cekirdek metni dis API'ye gondermez; TDK/Zemberek/GECTurk opsiyonel provider'lari guvenli degrade eder.",
    "Turkce metinde ondalik-nokta p degeri (`p<0.05`) blocker'dir; Marmara kuralina gore `p<0,001` / `p=0,038` kullanilir.",
]

DEFAULT_EVIDENTIA_SERVERS = [
    "evidentia-skills",
    "pubmed-epmc",
    "paper-search",
    "openalex",
    "semantic-scholar",
    "psyarxiv-osf",
    "yoktez-mcp",
    "anamnesis",
    "evidentia-kb",
    "annas-reader",
]

EVIDENTIA_CLAUDE_CODE_SURFACE = [
    "evidentia:start",
    "evidentia:medical-research",
    "/evidentia",
    "/evidentia-connectors",
    "/evidentia-fulltext",
    "/evidentia-kol",
    "/evidentia-synthesize",
]

EVIDENTIA_WORKFLOW_RULES = [
    f"Evidentia plugin v{EVIDENTIA_PLUGIN_VERSION}; flagship `{EVIDENTIA_FLAGSHIP_SKILL}` v{EVIDENTIA_FLAGSHIP_VERSION}.",
    "Native-MCP-first calisir: native MCP -> REST/legal OA -> belgelenmis bosluk; web/OSINT fallback yok.",
    "Adim 0.4 semantic scope scan + knowledge-map/evidentia-kb booster ile coverage_set uretilir; Adim 0.5 bunu yalniz genisletir.",
    "Tam metin ve buyuk cikti icin retrieve-don't-dump: once kanonik artefakt, sonra anamnesis corpus_stats -> ingest_document -> cok-sorgulu hybrid_query.",
    "Anna's Library full-text gate artik copyright-gated fallback katmanidir; EPMC/legal-OA/Paper Search sonrasi, Zotero ledger oncesi kapanir.",
    "Clean-copy doktrini: gorunen raporda connector/tool/axis/call telemetry sizmaz; operasyon izi yalniz OPS/VIZ sidecar mantiginda kalir.",
    "PsyArXiv/OSF bu projede .mcp.json ile hazir ama endpoint 404 bloklu; calisana kadar fallback Paper Search + OpenAlex.",
]

ANAMNESIS_CONTEXT_GATE = "Anamnesis context management gate"
ANNA_FULL_TEXT_GATE = "Anna's Library full-text gate"
DUAL_AI_RELIABILITY_GATE = "dual AI-reliability gate"
EVIDENTIA_GATE = "Evidentia external evidence gate"
SCI_AUDIT_GATE = "sci-audit manuscript audit gate"
CONTEXT_MEMORY_GATE = "context/memory MCP gate"
TURKISH_ACADEMIC_GATE = "Turkish thesis and academic MCP gate"
CLINICAL_TERMINOLOGY_GATE = "clinical terminology and regulatory MCP gate"
TURKISH_LEGISLATION_GATE = "Turkish legislation MCP gate"
TECHNICAL_DELIVERY_GATE = "technical delivery MCP gate"
CURRENT_WEB_GATE = "current web search MCP gate"
PLATFORM_DESIGN_GATE = "platform/design MCP gate"
CODE_SEARCH_GATE = "code search MCP gate"

SOURCEGRAPH_SESSION_COMMAND = "doppler run -p cureohub -c dev_personal -- claude"

TASK_GATED_MCP_LAYERS = [
    {
        "name": "context_memory",
        "servers": ["anamnesis", "memory", "qdrant", "sequentialthinking"],
        "purpose": "Oturum bağlamı, karar geçmişi, önceki güvenli çalışma notları, kompleks planlama ve Evidentia evidence_index sorguları.",
        "boundary": "Ham transcript, demografi satırı, .env, credential veya aile düzeyi hassas içerik gönderilmez; tam metin/büyük çıktı ham dökülmez, önce kanonik artefakt/ingest sonra sınırlı retrieval yapılır.",
    },
    {
        "name": "biomedical_literature",
        "servers": [
            "evidentia-skills",
            "pubmed-epmc",
            "paper-search",
            "openalex",
            "semantic-scholar",
            "psyarxiv-osf",
            "evidentia-kb",
            "annas-reader",
            "biocontext_kb",
            "meta-analysis-skills",
        ],
        "purpose": f"Biyomedikal literatür, tam metin, DOI/PMID/PMCID, preprint ve dış kanıt sentezi; Evidentia `{EVIDENTIA_FLAGSHIP_SKILL}` v{EVIDENTIA_FLAGSHIP_VERSION} native-first hattı.",
        "boundary": "Web/OSINT fallback yok; kaynak yapısal kanıtta yoksa gap yazılır. Tam metin + Zotero ledger kapanmadan citation yazılmaz.",
    },
    {
        "name": "turkish_academic",
        "servers": ["yoktez-mcp", "yok-akademik", "eric-mcp"],
        "purpose": "YÖK tezleri, Türkiye akademik bağlamı ve okul/eğitim literatürü.",
        "boundary": "YÖK tam metinleri telif ve alıntı sınırıyla özetlenir; uzun metin kopyalanmaz.",
    },
    {
        "name": "clinical_terminology_regulatory",
        "servers": [
            "openfda",
            "med-terminologies",
            "nlm-rxnorm",
            "nih-clinicaltables",
            "iuphar-gtopdb",
            "drugddx",
            "titck-cache",
        ],
        "purpose": "İlaç, ATC/RxNorm, ICD/SNOMED, FDA/TITCK ve klinik terminoloji doğrulaması.",
        "boundary": "Tedavi önerisi veya hasta düzeyi karar üretimi yapılmaz; tez terminolojisi ve kaynak doğrulamasıyla sınırlıdır.",
    },
    {
        "name": "turkish_legislation",
        "servers": ["mevzuat", "mevzuat-bilgisi"],
        "purpose": "KVKK, etik kurul, sağlık mevzuatı, yönetmelik, tebliğ ve resmi metin doğrulaması.",
        "boundary": "Hukuki yorum yerine resmi madde/kaynak doğrulaması yapılır.",
    },
    {
        "name": "technical_delivery",
        "servers": ["playwright", "chrome-devtools", "brave-search", "github", "filesystem"],
        "purpose": "Quarto/HTML/PDF render kontrolü, ekran görüntüsü, güncel web doğrulaması, GitHub ve dosya operasyonları.",
        "boundary": "Raw data ve credential dosyaları açılmaz; GitHub/write işlemleri açık talimat gerektirir.",
    },
    {
        "name": "platform_design_default_off",
        "servers": ["firebase", "supabase", "cloudflare-api", "figma", "openai-api-key-local-confirmation"],
        "purpose": "Tez dışı teknik platform, tasarım veya API anahtarı kurulum işleri.",
        "boundary": "Tez yazımında varsayılan kapı değildir; yalnız açık teknik istekle kullanılır.",
    },
    {
        "name": "code_search",
        "servers": ["sourcegraph", "serena"],
        "purpose": "Harici/açık kaynak kod arama (sourcegraph.com) ve yerel toolkit sembol navigasyonu (serena).",
        "boundary": (
            "Sourcegraph yalnız dış/açık kaynak kod içindir; repo içeriği, nitel veri veya KVKK kapsamındaki hiçbir "
            f"metin Sourcegraph'a gönderilmez. Token oturuma yalnız `{SOURCEGRAPH_SESSION_COMMAND}` ile enjekte olur."
        ),
    },
]

CONDITIONAL_PLUGIN_LAYERS = [
    {
        "name": "sci-audit",
        "entry_skill": SCI_AUDIT_PLUGIN_NAME,
        "purpose": "Tez/manuscript adli denetimi, referans-claim-istatistik-halusinasyon-kilavuz-AI seffaflik eksenleri ve Turkce bilimsel yazim/imla.",
    },
    {
        "name": "life-science-research",
        "entry_skill": "life-science-research:research-router-skill",
        "purpose": "Genetik, varyant, protein, pathway, farmakoloji, klinik calisma, omics/public dataset ve mekanistik T1DM biyolojisi.",
    },
    {
        "name": "zotero",
        "entry_skill": "zotero:Zotero",
        "purpose": "Zotero Web API arama/export, yerel Zotero kutuphanesi, BibTeX sync, citation insertion ve kaynakca mutabakati.",
    },
]

ZOTERO_WEB_BRIDGE = "scripts/util/zotero_env_bridge.py"
ZOTERO_DESKTOP_HELPER = "/home/mahirkurt/.codex/plugins/cache/openai-curated-remote/zotero/0.1.2/skills/zotero/scripts/zotero.py"

ZOTERO_COMMANDS = [
    f"python3 {ZOTERO_WEB_BRIDGE} status --json",
    f"python3 {ZOTERO_WEB_BRIDGE} search \"<query>\" --json --with-bibtex-keys",
    f"python3 {ZOTERO_WEB_BRIDGE} export-bibtex --out references/references.bib",
    f"python3 {ZOTERO_WEB_BRIDGE} cite --query \"<title>\" --markdown <draft.md> --bib references/references.bib --marker '<cite>'",
]

ZOTERO_DESKTOP_COMMANDS = [
    f"python3 {ZOTERO_DESKTOP_HELPER} status --json",
    f"python3 {ZOTERO_DESKTOP_HELPER} fulltext <attachment-key> --out <fulltext.txt>",
]

PROTECTED_INPUTS = [
    "01_raw_data/",
    "02_processed/transcripts/",
    "01_deidentified/",
    "00_raw_locked/",
    ".remember/",
]

SAFE_REPO_EVIDENCE = [
    "03_analysis/codebook/codebook_v2.md",
    "03_analysis/methodology/coreq_32_completed.md",
    "03_analysis/methodology/audit_trail.md",
    "03_analysis/methodology/llm_use_statement.md",
    "03_analysis/methodology/A1_information_power.md",
    "03_analysis/methodology/A9_triadic_methodology_literature.md",
    "07_reports/",
]

LOCAL_DMNITEL_COMMANDS = [
    {
        "name": "ai-context",
        "command": "./dmnitel ai-context",
        "purpose": "Ajan icin repo-ozel dmnitel + Anamnesis/context + Evidentia + t1dm-tez bridge ozetini guvenli bicimde verir.",
    },
    {
        "name": "route-tool",
        "command": './dmnitel route-tool --query "<soru>"',
        "purpose": "Soruya gore dmnitel, Evidentia veya paired doktoratezi/t1dm-tez akisini secer.",
    },
    {
        "name": "cross-repo-status",
        "command": CROSS_REPO_STATUS_COMMAND,
        "purpose": "Nitel ve nicel repo kaynaklarini resmi Marmara tez kilavuzu merkezli tek karma tez yazim akisi icin guvenli bicimde haritalar.",
    },
    {
        "name": "lint-codebook",
        "command": "./dmnitel lint-codebook 02_codebook/codebook.csv",
        "purpose": "Kod kitabi tutarliligi ve alan eksikleri.",
    },
    {
        "name": "build-triadic-matrix",
        "command": "./dmnitel build-triadic-matrix --coded-data <coded.csv> --output 04_triadic_matrices/<name>.csv",
        "purpose": "Anne, T1DM cocuk ve saglikli kardes rolleri icin tema/subtema matrisi.",
    },
    {
        "name": "check-quotes",
        "command": "./dmnitel check-quotes --source <deidentified-source> --quotes <quotes.csv>",
        "purpose": "Kullanilan anonim alintilarin kaynakla butunlugu.",
    },
    {
        "name": "audit-coreq",
        "command": "./dmnitel audit-coreq --methods <methods.md> --results <results.md>",
        "purpose": "COREQ 32 madde metin ici kanit denetimi.",
    },
    {
        "name": "find-negative-cases",
        "command": './dmnitel find-negative-cases --coded-data <coded.csv> --theme "<tema>"',
        "purpose": "Tema icin alternatif/negatif vaka adaylari.",
    },
    {
        "name": "log-ai-use",
        "command": './dmnitel log-ai-use --tool "<tool>" --model "<model>" --purpose "<amac>" --data-type "<anonim/turetilmis>" --output-summary "<ozet>"',
        "purpose": "Evidentia/Codex/MCP kullaniminin LLM beyan ve audit trail kaydi.",
    },
]


@dataclass(frozen=True)
class RouteResult:
    gate_order: list[str]
    recommended_actions: list[str]
    mcp_servers: list[str]
    plugin_layers: list[str]
    dmnitel_commands: list[str]
    zotero_commands: list[str]
    paired_repo: str | None
    warnings: list[str]
    audit_log: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "gate_order": self.gate_order,
            "recommended_actions": self.recommended_actions,
            "mcp_servers": self.mcp_servers,
            "plugin_layers": self.plugin_layers,
            "dmnitel_commands": self.dmnitel_commands,
            "zotero_commands": self.zotero_commands,
            "paired_repo": self.paired_repo,
            "warnings": self.warnings,
            "audit_log": self.audit_log,
        }


def build_bridge_context(output_format: str = "markdown") -> str:
    data = {
        "repo_profile": "t1dm_qualitative_thesis",
        "qualitative_repo": QUALITATIVE_REPO,
        "local_gate": "dmnitel + niteliksel-arastirma-rehberi-t1dm",
        "codex_playbook": CODEX_PLAYBOOK,
        "paired_quantitative_repo": PAIRED_QUANTITATIVE_REPO,
        "thesis_writing_root": THESIS_WRITING_ROOT,
        "official_thesis_sources": [OFFICIAL_THESIS_GUIDE, OFFICIAL_THESIS_TEMPLATE],
        "thesis_writing_entrypoints": [
            f"{THESIS_WRITING_ROOT}/README.md",
            CRITICAL_SOURCE_MANIFEST,
            CRITICAL_SOURCE_MANIFEST_TSV,
            f"{THESIS_WRITING_ROOT}/00_kaynak-kurallari/format-kontrati.md",
            f"{THESIS_WRITING_ROOT}/01_mimari/yetkinlik-ve-arac-mimarisi.md",
        ],
        "evidentia_plugin": {
            "version": EVIDENTIA_PLUGIN_VERSION,
            "flagship_skill": EVIDENTIA_FLAGSHIP_SKILL,
            "flagship_version": EVIDENTIA_FLAGSHIP_VERSION,
            "local_config": EVIDENTIA_LOCAL_CONFIG,
            "connector_source": EVIDENTIA_CONNECTOR_SOURCE,
            "cache_contract": EVIDENTIA_CACHE_CONTRACT,
            "claude_code_surface": EVIDENTIA_CLAUDE_CODE_SURFACE,
            "workflow_rules": EVIDENTIA_WORKFLOW_RULES,
        },
        "sci_audit_plugin": {
            "name": SCI_AUDIT_PLUGIN_NAME,
            "version": SCI_AUDIT_PLUGIN_VERSION,
            "local_config": SCI_AUDIT_LOCAL_CONFIG,
            "cache_root": SCI_AUDIT_CACHE_ROOT,
            "turkish_style_script": SCI_AUDIT_TURKISH_STYLE_SCRIPT,
            "claude_code_surface": SCI_AUDIT_CLAUDE_CODE_SURFACE,
            "tez_yazim_rules": SCI_AUDIT_TEZ_YAZIM_RULES,
            "workflow_rules": SCI_AUDIT_WORKFLOW_RULES,
        },
        "evidentia_default_mcp_servers": DEFAULT_EVIDENTIA_SERVERS,
        "task_gated_mcp_layers": TASK_GATED_MCP_LAYERS,
        "conditional_plugin_layers": CONDITIONAL_PLUGIN_LAYERS,
        "zotero_commands": ZOTERO_COMMANDS,
        "zotero_desktop_commands": ZOTERO_DESKTOP_COMMANDS,
        "safe_repo_evidence": SAFE_REPO_EVIDENCE,
        "protected_inputs": PROTECTED_INPUTS,
        "dmnitel_commands": LOCAL_DMNITEL_COMMANDS,
        "operational_order": [
            f"Once {CODEX_PLAYBOOK} dosyasini ana Codex playbook olarak kullan.",
            f"Tez yazim/format islerinde ana calisma merkezini {THESIS_WRITING_ROOT} olarak kabul et ve resmi docs/tez-kilavuz kaynaklarini ust kural yap.",
            f"Her tez yazim oturumunda klinik/nitel rapor, protokol, ham/kilitli veri ve olcek-form secimini once {CRITICAL_SOURCE_MANIFEST} ve manifest TSV ile yap.",
            "Once ./dmnitel route-tool ile sorunun yerel nitel, dis-kanit veya nicel-pipeline oldugunu ayir.",
            "Nitel repo yetkinliklerini yalniz tezde nitel kolun ilgili kesimleri yazilirken veya kanonik nitel sonuc raporu denetlenirken ac.",
            "Her tez yazim oturumunda ./dmnitel ai-context ve Anamnesis/context gate ile anonim/turetilmis baglami sabitle.",
            "Diger MCP'leri yalniz gorev sinyaliyle ac: YOK/ERIC akademik, mevzuat, klinik terminoloji/regulasyon, render/browser, GitHub veya teknik platform kapilari ayri tutulur.",
            f"Karma tez veya joint display sorularinda {CROSS_REPO_STATUS_COMMAND} ile iki-repo kaynak haritasini guncelle.",
            "Yerel nitel denetimde ./dmnitel komutlarini calistir; ham katilimci verisi dokme.",
            f"Dis literatur/tam metin/YOK/OSF/KOL gerekiyorsa Evidentia v{EVIDENTIA_PLUGIN_VERSION} / {EVIDENTIA_FLAGSHIP_SKILL} v{EVIDENTIA_FLAGSHIP_VERSION} hattini ac: native-first, no-web-tier, semantic coverage, retrieve-don't-dump.",
            f"Manuskript adli denetimi, Turkce imla/yazim, Kapı 4/5 veya bolum sertifikasyonu gerekiyorsa `{SCI_AUDIT_PLUGIN_NAME}` yuzeyini kullan; repo-local tr_sciaudit kopyasi olusturma.",
            "Genetik/varyant/protein/pathway/omics/farmakoloji/clinical trial sorularinda life-science-research plugin router'ini kosullu ac.",
            "Kaynakca, citation key, references.bib veya kutuphane senkronu gerekiyorsa once tam metin/claim ledger'ini kapat, sonra .env ZOTERO_API_KEY kullanan Zotero Web API bridge'ini kullan.",
            "Referansli bolum kapanisinda nitel ve nicel AI-reliability kontrollerini birlikte calistir.",
            "Nicel H1-H5, EMBU, Beck, KIA veya targets sorusu varsa paired doktoratezi repo + t1dm-tez-rehberi akisini kullan.",
            "Her harici AI/MCP kullanimini ./dmnitel log-ai-use ile kaydet.",
        ],
    }
    if output_format == "json":
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if output_format != "markdown":
        raise ValueError("format markdown veya json olmalıdır.")
    return _render_bridge_markdown(data)


def route_query(query: str) -> RouteResult:
    q = normalize_key(query)
    local_commands: list[str] = ["./dmnitel ai-context"]
    gate_order = ["dmnitel local gate", ANAMNESIS_CONTEXT_GATE]
    actions: list[str] = []
    mcp_servers: list[str] = []
    plugin_layers: list[str] = []
    zotero_commands: list[str] = []
    paired_repo: str | None = None
    warnings = [
        "Ham görüşme, transcript, demografi satırı, onam/protokol kişisel içeriği ve aile düzeyi hassas detay gönderme.",
        "Anamnesis/context araçlarına yalnız anonim/türetilmiş proje bağlamı gönder; raw data, .env veya credential gönderme.",
    ]
    mcp_servers.append("anamnesis")
    actions.append("Oturum bağlamını ./dmnitel ai-context ve Anamnesis/context gate ile sabitle; bağlam çıktısını karar ve kanıt düzeyinde tut.")

    if _has_any(q, ["codebook", "kod kitab", "kodkitab", "kodlama"]):
        local_commands.append("./dmnitel lint-codebook <codebook.csv>")
        actions.append("Kod kitabı tutarlılığını yerel dmnitel ile denetle.")
    if _has_any(q, ["coreq", "srqr", "jars-qual", "jars qual"]):
        local_commands.append("./dmnitel audit-coreq --methods <methods.md> --results <results.md>")
        actions.append("COREQ/SRQR/JARS-Qual iddialarını önce repo metinleriyle eşleştir.")
    if _has_any(q, ["alınt", "alinti", "quote", "alınti"]):
        local_commands.append("./dmnitel check-quotes --source <deidentified-source> --quotes <quotes.csv>")
        actions.append("Anonim alıntı bütünlüğünü yerel kaynakla doğrula.")
    if _has_any(q, ["triad", "triadik", "anne", "kardeş", "kardes", "multi-informant", "dyad"]):
        local_commands.append("./dmnitel build-triadic-matrix --coded-data <coded.csv> --output 04_triadic_matrices/<name>.csv")
        actions.append("Aile/rol karşılaştırmasını triadik matris üzerinden kur.")
    if _has_any(q, ["negatif vaka", "negative case", "aykırı vaka", "alternatif yorum"]):
        local_commands.append('./dmnitel find-negative-cases --coded-data <coded.csv> --theme "<tema>"')
        actions.append("Tema yorumu öncesi negatif/alternatif vaka adaylarını çıkar.")
    if _has_any(
        q,
        [
            "bağlam",
            "baglam",
            "context",
            "memory",
            "hafıza",
            "hafiza",
            "qdrant",
            "anamnesis",
            "karar geçmişi",
            "karar gecmisi",
            "sequential",
            "karmaşık plan",
            "karmasik plan",
        ],
    ):
        gate_order.append(CONTEXT_MEMORY_GATE)
        mcp_servers.extend(["memory", "qdrant", "sequentialthinking"])
        actions.append("Bağlam ve karar geçmişi için memory/qdrant/sequentialthinking kapısını aç; yalnız anonim/türetilmiş proje notları kullan.")
    needs_thesis_writing = _has_any(
        q,
        [
            "tez yazım",
            "tez yazimi",
            "tez-yazim",
            "tez kılavuz",
            "tez kilavuz",
            "tez-kilavuz",
            "marmara",
            "şablon",
            "sablon",
            "format",
            "özet",
            "ozet",
            "summary",
            "kaynaklar",
            "kaynakça format",
            "kaynakca format",
            "ama-11",
            "ondalık",
            "ondalik",
        ],
    )
    if needs_thesis_writing:
        gate_order.append("Marmara official thesis guide gate")
        paired_repo = PAIRED_QUANTITATIVE_REPO
        actions.append(
            f"Tez yazımını ana merkez olan {THESIS_WRITING_ROOT} içinde sürdür; docs/tez-kilavuz resmi kaynakları ve tez-yazim ana planı üst kuraldır."
        )
        actions.append(
            f"Klinik CSR, nitel sonuç raporu, protokol, ham/kilitli veri ve ölçek-form seçimini önce {CRITICAL_SOURCE_MANIFEST} ve manifest TSV üzerinden yap; dosyaları yazım alanına kopyalama."
        )
        actions.append("Nitel repo yetkinliklerini yalnız yöntem, bulgular, joint display, tartışma veya eklerde nitel kol kanıtı gerektiğinde kullan; kanonik nitel sonuç raporu varsayılan temsil kaynağıdır.")
    needs_critical_sources = _has_any(
        q,
        [
            "kritik dosya",
            "hayati dosya",
            "klinik çalışma sonuç raporu",
            "klinik calisma sonuc raporu",
            "nitel çalışma sonuç raporu",
            "nitel calisma sonuc raporu",
            "klinik çalışma protokol",
            "klinik calisma protokol",
            "ham veri",
            "ölçek",
            "olcek",
            "form",
            "kanonik dosya",
            "source manifest",
            "kaynak manifest",
        ],
    )
    if needs_critical_sources:
        paired_repo = PAIRED_QUANTITATIVE_REPO
        actions.append(
            f"Kritik tez kaynaklarını {CRITICAL_SOURCE_MANIFEST} ve {CRITICAL_SOURCE_MANIFEST_TSV} üzerinden seç; korumalı veri kaynaklarını yalnız yol/hash/aggregate düzeyinde kullan."
        )
    if _has_any(
        q,
        [
            "karma tez",
            "joint display",
            "mixed-method",
            "iki repo",
            "cross-repo",
            "nitel",
            "kanonik nitel",
            "qualitative",
        ],
    ):
        local_commands.append(CROSS_REPO_STATUS_COMMAND)
        actions.append("Karma tez yazımı için nitel ve nicel repo kaynak haritasını cross-repo status raporuyla güncelle.")

    needs_sci_audit = _has_any(
        q,
        [
            "sci-audit",
            "sci audit",
            "check-turkish",
            "tr_sciaudit",
            "turkish-sci-style",
            "bilimsel yazım",
            "bilimsel yazim",
            "türkçe imla",
            "turkce imla",
            "imla",
            "kapı 4",
            "kapi 4",
            "kapı 5",
            "kapi 5",
            "sertifikasyon",
            "bölüm finalizasyon",
            "bolum finalizasyon",
            "manüskript adli",
            "manuskript adli",
            "manuscript forensic",
            "halüsinasyon",
            "halusinasyon",
            "hallucination",
            "claim grounding",
            "referans bütünlüğü",
            "referans butunlugu",
            "istatistik iç tutarlılık",
            "istatistik ic tutarlilik",
        ],
    )
    if needs_sci_audit:
        gate_order.append(SCI_AUDIT_GATE)
        gate_order.append(DUAL_AI_RELIABILITY_GATE)
        plugin_layers.append(SCI_AUDIT_PLUGIN_NAME)
        paired_repo = PAIRED_QUANTITATIVE_REPO
        actions.append(
            f"Denetimlerde {SCI_AUDIT_PLUGIN_NAME} v{SCI_AUDIT_PLUGIN_VERSION} kullan; doktoratezi `tez-yazim` kuralları ve resmi Marmara format talimatnamesi üst kuraldır."
        )
        actions.append(
            "Kapı 4 için `/sci-audit:check-turkish <bolum>.qmd --strictness certification` çalıştır; deterministik CLI gerekiyorsa plugin-bundled `tr_sciaudit.py` kullan, repo-local kopya oluşturma."
        )
        actions.append(
            "Kapı 5 için `/sci-audit:audit <bolum>.qmd --lang tr --strictness certification --type <coreq|srqr|strobe|prisma|jars>` ve ardından `/sci-audit:audit-report --out <rapor>.md` kullan."
        )
        actions.append(
            f"Sci-audit raporlarını `{THESIS_WRITING_ROOT}/04_kalite-kontrol/raporlar/` ve bölüm sertifikasını `{THESIS_WRITING_ROOT}/04_kalite-kontrol/sertifikalar/` kuralına göre bağla; açık kullanıcı/danışman onayı yoksa en fazla provisional-pass yazılır."
        )
        warnings.append(
            "sci-audit repo/veri invaryantı denetlemez: KVKK, ham veri sınırı, quote-parity ve kanonik kilit için dmnitel + t1dm-qual-ai-audit + doktoratezi-ai-audit ayrı çalışır."
        )

    needs_evidentia = _has_any(
        q,
        [
            "literatür",
            "literatur",
            "evidentia",
            "pubmed",
            "europepmc",
            "doi",
            "tam metin",
            "fulltext",
            "yök",
            "yoktez",
            "osf",
            "psyarxiv",
            "citation",
            "referans",
            "reference",
            "atıf",
            "atif",
            "kol",
            "hakem",
            "jüri",
            "juri",
            "kanıt",
            "kanit",
            "braun",
            "clarke",
            "information power",
            "bilgi gücü",
            "bilgi gucu",
        ],
    )
    if needs_evidentia:
        gate_order.append(EVIDENTIA_GATE)
        mcp_servers.extend(DEFAULT_EVIDENTIA_SERVERS)
        plugin_layers.append("evidentia:medical-research")
        actions.append(
            f"Dış kanıt için Evidentia v{EVIDENTIA_PLUGIN_VERSION} / `{EVIDENTIA_FLAGSHIP_SKILL}` v{EVIDENTIA_FLAGSHIP_VERSION} hattını çalıştır; önce `{EVIDENTIA_LOCAL_CONFIG}`, CONNECTORS ve canonical-cache sözleşmesini uygula."
        )
        actions.append("Native-first çözümleme kullan: PubMed/EPMC, Paper Search, OpenAlex/S2, YÖK Tez, anamnesis/evidentia-kb ve tam metin katmanları; web/OSINT fallback yok, bulunamayan kaynak gap olarak yazılır.")
        actions.append("Adım 0.4 semantic scope scan ve Completeness Gate ile coverage_set kapat; ciddi sentezde `evidentia:evidence-synthesizer` veya `/evidentia-synthesize` ile bağlamı izole et.")
        actions.append("Tam metin/büyük çıktı için retrieve-don't-dump: corpus_stats kontrolü, tek ingest, çok-sorgulu hybrid_query ve provenance-damgalı sınırlı dilim kullan.")
    if _has_any(q, ["psyarxiv", "osf", "open science", "preprint", "preregistration", "pre-registration"]):
        warnings.append("PsyArXiv/OSF client config bu projede hazır ama endpoint hâlâ 404 bloklu; worker düzelene kadar preprint/preregistration fallback'i Paper Search + OpenAlex + PubMed/EPMC üzerinden yürüt.")
    if _has_any(q, ["okul", "akademik", "eğitim", "egitim", "school", "education"]):
        mcp_servers.append("eric-mcp")
        actions.append("Okul/eğitim sinyali nedeniyle ERIC katmanını koşullu aç.")
    needs_turkish_academic = _has_any(
        q,
        [
            "yök",
            "yok",
            "yoktez",
            "ulusal tez",
            "tez merkezi",
            "yök akademik",
            "yok akademik",
            "akademik profil",
            "danışman",
            "danisman",
            "tez no",
        ],
    )
    if needs_turkish_academic:
        gate_order.append(TURKISH_ACADEMIC_GATE)
        mcp_servers.extend(["yoktez-mcp", "yok-akademik"])
        actions.append("Türkiye tez/akademik bağlamı için YÖK Tez ve YÖK Akademik kapılarını kullan; tam metni yalnız hedefli sayfa/pasaj düzeyinde özetle.")

    needs_legislation = _has_any(
        q,
        [
            "kvkk",
            "mevzuat",
            "kanun",
            "yönetmelik",
            "yonetmelik",
            "tebliğ",
            "teblig",
            "resmi gazete",
            "etik kurul",
            "hasta hakları",
            "hasta haklari",
            "sut",
            "sgk",
        ],
    )
    if needs_legislation:
        gate_order.append(TURKISH_LEGISLATION_GATE)
        mcp_servers.extend(["mevzuat", "mevzuat-bilgisi"])
        actions.append("KVKK/etik/sağlık mevzuatı için mevzuat MCP kapılarını resmi madde doğrulaması amacıyla kullan; hukuki tavsiye üretme.")

    needs_life_science = _has_word(q, "gene") or _has_any(
        q,
        [
            "genetik",
            "variant",
            "varyant",
            "hla",
            "gwas",
            "protein",
            "pathway",
            "yolak",
            "autoimmunity",
            "otoimmun",
            "otoimmün",
            "beta cell",
            "islet",
            "adacik",
            "adacık",
            "omics",
            "transcriptomics",
            "proteomics",
            "metabolomics",
            "dataset",
            "public dataset",
            "pharmacology",
            "farmakoloji",
            "clinical trial",
            "nct",
            "mechanism",
            "mekanizma",
            "biomarker",
            "biyobelirteç",
            "biyobelirtec",
        ],
    )
    if needs_life_science:
        gate_order.append("life-science-research plugin gate")
        plugin_layers.append("life-science-research:research-router-skill")
        mcp_servers.extend(["biocontext_kb", "meta-analysis-skills"])
        actions.append("Biyomedikal entity/data derinleştirmesi için Life Science Research router'ını kullan; psikososyal bulgularla mekanistik kanıtı karıştırma.")

    needs_clinical_terminology = _has_any(
        q,
        [
            "ilaç",
            "ilac",
            "drug",
            "rxnorm",
            "atc",
            "snomed",
            "icd",
            "terminoloji",
            "terminology",
            "fda",
            "openfda",
            "titck",
            "farmakovijilans",
            "tıbbi cihaz",
            "tibbi cihaz",
            "klinik tablo",
        ],
    )
    if needs_clinical_terminology:
        gate_order.append(CLINICAL_TERMINOLOGY_GATE)
        mcp_servers.extend(
            [
                "openfda",
                "med-terminologies",
                "nlm-rxnorm",
                "nih-clinicaltables",
                "iuphar-gtopdb",
                "drugddx",
                "titck-cache",
            ]
        )
        actions.append("Klinik terminoloji/ilaç/regülasyon iddialarında terminoloji ve regülasyon MCP'lerini kaynak doğrulama için kullan; hasta düzeyi öneri üretme.")

    needs_zotero = _has_any(
        q,
        [
            "zotero",
            "references.bib",
            "bibtex",
            "ris",
            "citation key",
            "cite",
            "kaynakca",
            "kaynakça",
            "kütüphane",
            "kutuphane",
            "atıf",
            "atif",
            "bibliography",
            "reference manager",
        ],
    )
    if needs_zotero:
        gate_order.append("Zotero reference manager gate")
        plugin_layers.append("zotero:Zotero")
        zotero_commands.extend(ZOTERO_COMMANDS)
        actions.append("Doğrulanmış kaynakları Zotero Web API ve references/references.bib katmanıyla mutabıklaştır; Zotero import/write işlemleri açık onay gerektirir.")

    needs_full_text_reference_gate = needs_evidentia or needs_zotero or _has_any(
        q,
        [
            "anna",
            "annas",
            "annas-reader",
            "tam metin",
            "full text",
            "fulltext",
            "kaynak",
            "kaynakça",
            "kaynakca",
            "referans",
            "reference",
        ],
    )
    if needs_full_text_reference_gate:
        gate_order.append(ANNA_FULL_TEXT_GATE)
        mcp_servers.append("annas-reader")
        actions.append("Her referans için DOI/PMID/ID doğrula; EPMC/legal-OA/Paper Search ve gerekirse Anna's copyright-gated fallback ile tam metin kanıtı kapanmadan citation ekleme.")
        actions.append("Referans denetim ledger'ına citation key, Zotero item key, tam metin kanıtı, kullanılan claim ve sayfa/pasaj notunu yaz.")

    needs_ai_reliability = needs_full_text_reference_gate or _has_any(
        q,
        [
            "ai reliability",
            "ai-reliability",
            "güvenilirlik",
            "guvenilirlik",
            "reliability",
            "audit",
            "denetim",
        ],
    )
    if needs_ai_reliability:
        gate_order.append(DUAL_AI_RELIABILITY_GATE)
        actions.append("Referanslı bölüm kapanışında t1dm-qual-ai-audit ve doktoratezi-ai-audit kontrollerini birlikte çalıştır.")

    needs_technical_delivery = _has_any(
        q,
        [
            "render",
            "quarto render",
            "pdf",
            "html",
            "screenshot",
            "ekran görüntüsü",
            "ekran goruntusu",
            "tarayıcı",
            "tarayici",
            "chrome",
            "playwright",
            "github",
            "pull request",
            "issue",
            "commit",
            "git",
        ],
    )
    if needs_technical_delivery:
        gate_order.append(TECHNICAL_DELIVERY_GATE)
        mcp_servers.extend(["playwright", "chrome-devtools", "github", "filesystem"])
        actions.append("Render, browser, GitHub veya dosya operasyonlarında teknik delivery MCP kapısını kullan; raw data ve credential dosyalarını dışarı taşıma.")

    needs_current_web = _has_any(q, ["güncel", "guncel", "latest", "bugün", "bugun", "web search", "internet", "haber"])
    if needs_current_web:
        gate_order.append(CURRENT_WEB_GATE)
        mcp_servers.append("brave-search")
        actions.append("Güncel web doğrulaması için brave-search kapısını yalnız ikincil/current bilgi için kullan; Evidentia/literatür iddialarında web fallback yoktur, PubMed/OpenAlex/Paper Search/Anna's ve yapılandırılmış kaynaklar önceliklidir.")

    needs_platform_design = _has_any(
        q,
        [
            "firebase",
            "supabase",
            "cloudflare",
            "figma",
            "api key",
            "openai api",
            "deploy",
            "tasarım",
            "tasarim",
            "site",
            "dashboard",
        ],
    )
    if needs_platform_design:
        gate_order.append(PLATFORM_DESIGN_GATE)
        mcp_servers.extend(["firebase", "supabase", "cloudflare-api", "figma", "openai-api-key-local-confirmation"])
        actions.append("Platform/tasarım/API-key MCP'leri tez yazımı için varsayılan değildir; yalnız açık teknik görev varsa kullan.")

    needs_code_search = _has_any(
        q,
        [
            "sourcegraph",
            "kod arama",
            "kod aramasi",
            "code search",
            "açık kaynak kod",
            "acik kaynak kod",
            "open source kod",
            "sembol",
            "symbol",
            "kütüphane kaynak kodu",
            "kutuphane kaynak kodu",
            "serena",
        ],
    )
    if needs_code_search:
        gate_order.append(CODE_SEARCH_GATE)
        mcp_servers.extend(["sourcegraph", "serena"])
        actions.append(
            "Dış/açık kaynak kod araması için sourcegraph MCP'yi (nls_search/keyword_search/deepsearch), "
            "yerel toolkit sembol işleri için serena'yı kullan."
        )
        actions.append(
            f"Sourcegraph token'ı yalnız `{SOURCEGRAPH_SESSION_COMMAND}` ile başlatılan oturumda yüklüdür; "
            "araçlar görünmüyorsa oturumu Doppler ile yeniden başlat."
        )
        warnings.append(
            "Sourcegraph sorgularına repo içeriği, nitel veri, katılımcı metni veya KVKK kapsamındaki hiçbir parça yazılmaz; "
            "yalnız dış/açık kaynak kod aranır."
        )

    needs_quant = _has_any(
        q,
        [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "embu",
            "beck",
            "kia",
            "kİa",
            "srq",
            "hba1c",
            "targets",
            "_targets",
            "r pipeline",
            "quarto",
            "sap",
            "istatistik",
            "nicel",
            "bayes",
            "sem",
            "lavaan",
        ],
    )
    if needs_quant:
        gate_order.append("paired doktoratezi + t1dm-tez-rehberi")
        paired_repo = PAIRED_QUANTITATIVE_REPO
        actions.append("Nicel analiz, hipotez veya karma joint display kararı için paired doktoratezi repo bağlamını aç.")

    if not actions:
        actions.append("Önce repo kaynaklarını oku; ./dmnitel ai-context ile karar yüzeyini sabitle.")

    return RouteResult(
        gate_order=_prioritize_gate_order(gate_order),
        recommended_actions=_dedupe(actions),
        mcp_servers=_dedupe(mcp_servers),
        plugin_layers=_dedupe(plugin_layers),
        dmnitel_commands=_dedupe(local_commands),
        zotero_commands=_dedupe(zotero_commands),
        paired_repo=paired_repo,
        warnings=warnings,
        audit_log='./dmnitel log-ai-use --tool "<tool>" --model "<model>" --purpose "<amac>" --data-type "<anonim/turetilmis>" --output-summary "<ozet>" --external-api-used yes',
    )


def render_route(result: RouteResult, output_format: str = "markdown") -> str:
    if output_format == "json":
        return json.dumps(result.as_dict(), ensure_ascii=False, indent=2) + "\n"
    if output_format != "markdown":
        raise ValueError("format markdown veya json olmalıdır.")
    lines = ["# Dmnitel Tool Route", ""]
    lines.append("## Gate Order")
    lines.extend(f"- {item}" for item in result.gate_order)
    lines.append("")
    lines.append("## Recommended Actions")
    lines.extend(f"- {item}" for item in result.recommended_actions)
    lines.append("")
    lines.append("## Dmnitel Commands")
    lines.extend(f"- `{item}`" for item in result.dmnitel_commands)
    if result.mcp_servers:
        lines.append("")
        lines.append("## MCP Servers")
        lines.extend(f"- `{item}`" for item in result.mcp_servers)
    if result.plugin_layers:
        lines.append("")
        lines.append("## Plugin Layers")
        lines.extend(f"- `{item}`" for item in result.plugin_layers)
    if result.zotero_commands:
        lines.append("")
        lines.append("## Zotero Web API Commands")
        lines.extend(f"- `{item}`" for item in result.zotero_commands)
    if result.paired_repo:
        lines.append("")
        lines.append(f"Paired quantitative repo: `{result.paired_repo}`")
    lines.append("")
    lines.append("## Warnings")
    lines.extend(f"- {item}" for item in result.warnings)
    lines.append("")
    lines.append(f"Audit log: `{result.audit_log}`")
    return "\n".join(lines) + "\n"


def write_or_print(content: str, output: str | None) -> None:
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Rapor yazıldı: {path}")
        return
    print(content, end="")


def _render_bridge_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# T1DM Niteliksel AI Tool Bridge",
        "",
        f"Repo profile: `{data['repo_profile']}`",
        f"Qualitative repo root: `{data['qualitative_repo']}`",
        f"Local gate: `{data['local_gate']}`",
        f"Codex playbook: `{data['codex_playbook']}`",
        f"Paired quantitative repo: `{data['paired_quantitative_repo']}`",
        f"Thesis writing root: `{data['thesis_writing_root']}`",
        "",
        "## Official Thesis Sources",
    ]
    lines.extend(f"- `{path}`" for path in data["official_thesis_sources"])
    lines.append("")
    lines.append("## Thesis Writing Entrypoints")
    lines.extend(f"- `{path}`" for path in data["thesis_writing_entrypoints"])
    lines.extend(
        [
        "",
        "## Operational Order",
        ]
    )
    lines.extend(f"- {item}" for item in data["operational_order"])
    lines.append("")
    lines.append("## Evidentia Plugin Contract")
    evidentia = data["evidentia_plugin"]
    lines.append(
        f"- Plugin v{evidentia['version']} · flagship `{evidentia['flagship_skill']}` v{evidentia['flagship_version']}"
    )
    lines.append(f"- Local config: `{evidentia['local_config']}`")
    lines.append(f"- Connector source: `{evidentia['connector_source']}`")
    lines.append(f"- Cache contract: `{evidentia['cache_contract']}`")
    lines.append("")
    lines.append("## Evidentia Claude Code Surface")
    lines.extend(f"- `{item}`" for item in evidentia["claude_code_surface"])
    lines.append("")
    lines.append("## Evidentia Workflow Rules")
    lines.extend(f"- {item}" for item in evidentia["workflow_rules"])
    lines.append("")
    lines.append("## Sci-Audit Plugin Contract")
    sci_audit = data["sci_audit_plugin"]
    lines.append(f"- Plugin: `{sci_audit['name']}` v{sci_audit['version']}")
    lines.append(f"- Local config: `{sci_audit['local_config']}`")
    lines.append(f"- Cache root: `{sci_audit['cache_root']}`")
    lines.append(f"- Axis G CLI: `{sci_audit['turkish_style_script']}`")
    lines.append("")
    lines.append("## Sci-Audit Claude Code Surface")
    lines.extend(f"- `{item}`" for item in sci_audit["claude_code_surface"])
    lines.append("")
    lines.append("## Tez-Yazim Rules Adopted For Sci-Audit")
    lines.extend(f"- `{item}`" for item in sci_audit["tez_yazim_rules"])
    lines.append("")
    lines.append("## Sci-Audit Workflow Rules")
    lines.extend(f"- {item}" for item in sci_audit["workflow_rules"])
    lines.append("")
    lines.append("## Dmnitel Commands")
    for command in data["dmnitel_commands"]:
        lines.append(f"- `{command['command']}` — {command['purpose']}")
    lines.append("")
    lines.append("## Evidentia Default MCP Core")
    lines.extend(f"- `{server}`" for server in data["evidentia_default_mcp_servers"])
    lines.append("")
    lines.append("## Task-Gated MCP Layers")
    for layer in data["task_gated_mcp_layers"]:
        servers = ", ".join(f"`{server}`" for server in layer["servers"])
        lines.append(f"- **{layer['name']}**: {servers}")
        lines.append(f"  - Purpose: {layer['purpose']}")
        lines.append(f"  - Boundary: {layer['boundary']}")
    lines.append("")
    lines.append("## Conditional Plugin Layers")
    for plugin in data["conditional_plugin_layers"]:
        lines.append(f"- `{plugin['entry_skill']}` — {plugin['purpose']}")
    lines.append("")
    lines.append("## Zotero Web API Commands")
    lines.extend(f"- `{command}`" for command in data["zotero_commands"])
    lines.append("")
    lines.append("## Zotero Desktop Local API Commands")
    lines.extend(f"- `{command}`" for command in data["zotero_desktop_commands"])
    lines.append("")
    lines.append("## Safe Repo Evidence")
    lines.extend(f"- `{path}`" for path in data["safe_repo_evidence"])
    lines.append("")
    lines.append("## Protected Inputs")
    lines.extend(f"- `{path}`" for path in data["protected_inputs"])
    return "\n".join(lines) + "\n"


def _has_any(value: str, needles: list[str]) -> bool:
    return any(normalize_key(needle) in value for needle in needles)


def _has_word(value: str, word: str) -> bool:
    return normalize_key(word) in value.split()


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def _prioritize_gate_order(values: list[str]) -> list[str]:
    deduped = _dedupe(values)
    priority = [
        "dmnitel local gate",
        ANAMNESIS_CONTEXT_GATE,
        "Marmara official thesis guide gate",
        SCI_AUDIT_GATE,
        EVIDENTIA_GATE,
        ANNA_FULL_TEXT_GATE,
        "Zotero reference manager gate",
        DUAL_AI_RELIABILITY_GATE,
        CONTEXT_MEMORY_GATE,
        TURKISH_ACADEMIC_GATE,
        CLINICAL_TERMINOLOGY_GATE,
        TURKISH_LEGISLATION_GATE,
        TECHNICAL_DELIVERY_GATE,
        CURRENT_WEB_GATE,
        PLATFORM_DESIGN_GATE,
    ]
    ordered = [gate for gate in priority if gate in deduped]
    ordered.extend(gate for gate in deduped if gate not in ordered)
    return ordered
