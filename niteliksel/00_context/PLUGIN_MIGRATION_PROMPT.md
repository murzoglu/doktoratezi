# sci-audit Plugin Migrasyon Komutu

AI-reliability sistemini (KAYNAK-1: bu repo) ve Türkçe bilimsel yazım denetimini
(KAYNAK-2: doktoratezi `tr_sciaudit.py`) genel amaçlı, claude.ai web-uyumlu bir
Claude Code marketplace plugin'ine dönüştüren komut. Marketplace reposundaki
Claude Code oturumuna yapıştırılır.

Hazırlanış: 2026-07-05. Kaynak envanteri bu tarihte doğrulandı:
- KAYNAK-1: `.claude/hooks/` beşlisi + `_common.py`, `.claude/settings.json`
  permissions.deny, `reliability/` (verify/evals/redteam), `governance/`,
  `plugins/t1dm-qual-ai-audit` (Codex formatında), `tests/test_claude_hooks.py`
  (90/90 geçiyor), `.codex/tools/codex_mcp_roster_redacted.py`.
- KAYNAK-2: `scripts/util/tr_sciaudit.py` (935 satır; deterministik çekirdek
  stdlib, `requests` yalnız opsiyonel provider'larda),
  `scripts/util/gecturk_selfhost_endpoint.py`, `requirements/tr-sciaudit.txt`
  (`setuptools<81` + `zemberek-python==0.2.3` + `requests`), doktrin:
  `tez-yazim/04_kalite-kontrol/turkce-bilimsel-yazim-denetimi.md`.

## 1) Oturum başlatma (iki kaynak repoya okuma erişimi şart)

```bash
cd /path/to/marketplace-repo
claude --add-dir "/mnt/thunderbolt/workspaces/T1DM Niteliksel" \
       --add-dir "/mnt/thunderbolt/workspaces/doktoratezi"
```

## 2) Yapıştırılacak komut

```text
Marketplace reposunda, LLM tarafından üretilmiş BİLİMSEL METİNLERİ hem ADLİ hem
DİLSEL olarak denetleyen genel amaçlı bir Claude Code plugin'i inşa et: "sci-audit".
İki kaynak repodan kod port edilir ama TÜM domain bağlamından (T1DM, tez, KVKK
dizin adları, dmnitel, doktoratezi'ye özgü yollar) tamamen arındırılır:
  KAYNAK-1: /mnt/thunderbolt/workspaces/T1DM Niteliksel        (reliability çekirdeği)
  KAYNAK-2: /mnt/thunderbolt/workspaces/doktoratezi            (Türkçe dil denetimi)
⚠️ Kaynaklardan yalnız kod/politika port edilir; katılımcı verisi/PII içeren hiçbir
dizin (01_raw_data/, 02_processed/transcripts/, 01_deidentified/, .remember/,
chapters/ içerikleri) okunmaz, örnek olarak dahi kopyalanmaz.

## Misyon — 7 denetim ekseni

Plugin, herhangi bir LLM'in ürettiği bilimsel metni (makale taslağı, tez bölümü,
derleme, rapor, abstract) denetler:
A. Referans bütünlüğü — uydurma/halüsinatif kaynak tespiti (DOI/PMID/arXiv ID
   gerçekten var mı; başlık-yazar-yıl-dergi metadata eşleşmesi; retraction).
B. İddia temellendirme — sayısal/olgusal iddiaların kaynağa bağlılığı
   (claim extraction → evidence matching; kaynaksız sayı = ihlal).
C. İstatistik tutarlılığı — p/test istatistiği/df uyumu (statcheck mantığı),
   GRIM, yüzde toplamları, etki büyüklüğü akla yatkınlığı.
D. Halüsinasyon sinyalleri — semantic entropy, aşırı-kesinlik dili,
   var-olmayan yöntem/araç adları.
E. Raporlama kılavuzu uyumu — türe göre PRISMA/CONSORT/STROBE/COREQ/SRQR/
   JARS/TRIPOD checklist denetimi.
F. AI-kullanım şeffaflığı — LLM katkı beyanı, disclosure eksikleri.
G. ★ TÜRKÇE BİLİMSEL DİL VE İMLA — metin dili Türkçe algılandığında (veya
   --lang tr) otomatik devreye girer. Kaynak: KAYNAK-2'deki
   scripts/util/tr_sciaudit.py (935 satır) + gecturk_selfhost_endpoint.py +
   requirements/tr-sciaudit.txt + doktrin dosyası
   tez-yazim/04_kalite-kontrol/turkce-bilimsel-yazim-denetimi.md.
   Alt katmanları:
   G1 biçimsel yazım: encoding artefaktları, noktalama boşlukları, tekrar eden
      sözcük, Türkçe karakter bozulması (ı/i, ş/s sinyalleri);
   G2 okunabilirlik/üslup: cümle-paragraf uzunluğu, Ateşman okunabilirlik skoru;
   G3 akademik register: birinci kişi, konuşma dili, İngilizce terim sızıntısı;
   G4 nedensellik/genelleme aşımı dili (korelasyonel bulguyu nedensel anlatma);
   G5 sayı biçimi: ondalık VİRGÜL kuralı, p-değeri yazım biçimi, APA-TR uyumu;
   G6 kısaltma/terim tutarlılığı: ilk-geçişte-açılım, whitelist, TDK doğrulama;
   G7 morfoloji (opsiyonel): Zemberek analizi.
Skorlama: her eksen 0-100 + kanıtlı bulgu listesi. tr_sciaudit'in
error/warning/info seviyeleri plugin'in blocker/major/minor'una eşlenir;
strictness modları (draft|certification) korunur; certification modunda
"error varsa kapı kapanmaz" (--fail-on error) davranışı rapor sonucuna yansır.

## claude.ai web optimizasyonu (bağlayıcı kısıtlar)

1. Çekirdek denetim SAF PYTHON stdlib — tr_sciaudit.py port edilirken
   `requests` çağrıları `urllib.request`e çevrilir (deterministik G1-G6 çekirdeği
   zaten stdlib). Ağır bağımlılıklar (zemberek-python, ragas, torch) OPSIYONEL
   katmana izole: yoksa graceful skip, raporda "atlandı/unavailable" işareti.
   ⚠️ Zemberek gotcha'sı taşınır: zemberek-python==0.2.3 `pkg_resources` için
   `setuptools<81` pin'i ister; bu yalnız CI/lokal venv katmanında kurulur.
2. Provider degrade matrisi (tr_sciaudit'in "güvenli fallback" sözleşmesi aynen):
   - Deterministik G1-G6 → her ortamda çalışır (web dahil), ağ gerektirmez.
   - TDK (sozluk.gov.tr/gts) → remote HTTP; web'de çalışır; hata = provider
     'error' statüsü, deterministik denetim sürer.
   - GECTurk self-host endpoint → web'de 'unavailable'; lokal/CI'da
     gecturk_selfhost_endpoint.py ile. Public API ASLA varsayılmaz.
   - Zemberek → paket varsa aktif, yoksa 'unavailable'; rapor bloklamaz.
   - LLM-yargıç: kaynaktaki Grok/xAI adapter'ı YERİNE web-native çözüm →
     Claude subagent (aşağıda style-judge agent). Grok adapter'ı yalnız
     CI-eval katmanında opsiyonel bırakılır (GROK_API_KEY yoksa metin
     gönderilmeden 'unavailable' — bu gizlilik sözleşmesi aynen korunur).
3. .mcp.json'daki tüm sunucular REMOTE (HTTP/SSE); stdio/yerel binary yasak.
4. Dosya yolları OS-bağımsız; ${CLAUDE_PLUGIN_ROOT} dışında mutlak yol yok.
5. Uzun metinler bölümlenip subagent'lara fan-out edilir; rapor dili =
   kullanıcının dili (şablon başlıkları EN+TR çifti).

## Plugin yapısı

plugins/sci-audit/
├── .claude-plugin/plugin.json        # name: sci-audit, 0.1.0, keywords:
│                                     # [scientific-integrity, hallucination,
│                                     # citations, turkish, imla, guardrails]
├── hooks/
│   ├── hooks.json                    # ${CLAUDE_PLUGIN_ROOT} yolları, 5 event
│   └── scripts/                      # KAYNAK-1 .claude/hooks/*.py port:
│       ├── _common.py                # stdin JSON sözleşmesi aynen
│       ├── session_start.py          # bilimsel-bütünlük + TR-yazım konvansiyon
│       │                             # enjeksiyonu (references/conventions.md)
│       ├── user_prompt_submit.py     # sır taraması aynen
│       ├── pre_tool_use_policy.py    # evrensel yıkıcı-komut kapısı
│       ├── post_tool_use_review.py   # çıktı sır/PII taraması
│       └── stop_verify.py            # ★ çift kapı: (a) kaynaksız sayısal iddia,
│                                     # (b) TR metinde ondalik NOKTA + İngilizce
│                                     # p-değeri biçimi gibi G5 blocker kalıpları
├── commands/
│   ├── audit.md                      # /sci-audit:audit — 7 eksen tam denetim
│   ├── verify-citations.md           # eksen A
│   ├── check-stats.md                # eksen C
│   ├── guideline-check.md            # eksen E
│   ├── check-turkish.md              # ★ eksen G solo: dosya/metin alır,
│   │                                 # strictness + provider bayrakları
│   │                                 # (--enable-zemberek/--enable-tdk vb.
│   │                                 # tr_sciaudit CLI sözleşmesi korunur)
│   ├── audit-report.md               # bulguları tek rapora derler
│   └── ai-log.md                     # denetim günlüğü (JSONL append)
├── agents/
│   ├── citation-verifier.md          # ref → MCP çözümleme
│   ├── claim-extractor.md            # bölüm → yapılandırılmış iddia listesi
│   ├── claim-refuter.md              # adversarial çürütücü
│   ├── stats-checker.md              # eksen C hesapları (script çağırır)
│   ├── guideline-mapper.md           # checklist ↔ metin eşlemesi
│   └── style-judge.md                # ★ TR bilimsel üslup LLM-yargıcı:
│                                     # tr_sciaudit'in Grok JSON rubriğini
│                                     # Claude-native uygular (register,
│                                     # akıcılık, nedensellik dili, terim
│                                     # tutarlılığı); deterministik bulgularla
│                                     # çelişirse deterministik kazanır
├── skills/
│   ├── sci-audit-orchestrator/       # ana skill: dil algılama (TR→G ekseni
│   │   ├── SKILL.md                  # otomatik), tür tespiti, bölümleme,
│   │   └── references/               # fan-out planı, skor birleştirme
│   │       ├── conventions.md
│   │       ├── report-template.md    # 7 eksenli şablon
│   │       └── guidelines/           # PRISMA/CONSORT/STROBE/COREQ/SRQR/
│   │                                 # JARS/TRIPOD madde listeleri
│   ├── citation-forensics/SKILL.md
│   ├── claim-grounding/              # KAYNAK-1 claim_check.py + ragas (ops.)
│   ├── stats-forensics/              # statcheck/GRIM stdlib implementasyonu
│   ├── hallucination-signals/        # KAYNAK-1 semantic_entropy.py port
│   └── turkish-sci-style/            # ★ eksen G skill'i
│       ├── SKILL.md                  # katman eşleme tablosu + provider
│       │                             # degrade matrisi + Ateşman formülü +
│       │                             # APA-TR sayı biçim kuralları dokümante
│       ├── scripts/
│       │   ├── tr_sciaudit.py        # KAYNAK-2'den port (urllib'e çevrilmiş,
│       │   │                         # Grok adapter'ı ayrıştırılmış)
│       │   └── gecturk_endpoint.py   # self-host GECTurk (lokal/CI kullanım)
│       └── references/
│           └── denetim-doktrini.md   # KAYNAK-2 doktrin dosyasından genelleştir
├── reliability/                      # CI-only: evals/ redteam/ + Grok eval
│   ├── requirements-core.txt         # (boş/stdlib notu)
│   └── requirements-optional.txt     # zemberek-python==0.2.3, setuptools<81,
│                                     # ragas, otel — hepsi opsiyonel katman
├── governance/nist-iso-42001-mapping.md
├── .mcp.json
├── tests/                            # hook testleri + stats/citation testleri +
│   ├── fixtures/sample-tr.md         # ★ TR fixture: bilerek ondalık nokta,
│   │                                 # İngilizce p biçimi, register ihlali,
│   │                                 # uydurma DOI + tutarsız p içeren örnek
│   └── fixtures/sample-en.md
└── README.md                         # CLI + claude.ai web kurulum, katman
                                      # tablosu, provider/MCP degrade matrisi

## MCP tam entegrasyonu

1. .mcp.json — REMOTE tip bilimsel çekirdek: pubmed/europepmc, openalex,
   crossref, semantic-scholar. Env-gated; anahtar ${ENV_VAR} ile, düz metin asla.
   Resmi remote endpoint'i olmayanı GÖMME → README'de "claude.ai connector
   olarak bağlayın" talimatı.
2. Eksen→MCP yönlendirme tablosu skill'lere gömülür: A → openalex+crossref+
   pubmed; B → pubmed/semantic-scholar; retraction → crossref+pubmed.
   G → TDK doğrudan HTTP (MCP değil); ileride tr-sciaudit-mcp (FastMCP/Cloud
   Run) deploy edilirse .mcp.json'a env-gated remote girdi olarak eklenecek
   şekilde yer tutucu + README bölümü hazırla.
3. MCP başarısızsa kontrol "unverified (MCP yok)" etiketi alır — skor cezası
   yok ama o bulgu blocker olamaz.
4. Audit skill'ine MCP-roster denetim adımı (KAYNAK-1
   .codex/tools/codex_mcp_roster_redacted.py deseni): token asla yazdırılmaz.

## Port + genelleştirme kuralları

1. Hook stdin JSON sözleşmesi ve exit-code/hookSpecificOutput davranışı aynen;
   Stop hook timeout 120 sn.
2. stop_verify.py çift kapısının G5 kalıpları .claude/sci-audit.local.md
   (YAML frontmatter) config'inden okunur; default: kaynaksız-sayı kalıpları +
   TR ondalık/p-değeri kalıpları. Config yoksa güvenli varsayılan.
3. tr_sciaudit.py port edilirken CLI arayüzü (--strictness, --format md|json,
   --out, --terms, --fail-on, --enable-*) KORUNUR — mevcut kullanıcı kas
   hafızası ve CI script'leri bozulmasın. Domain'e özgü whitelist'ler
   (tez kısaltmaları) koddan çıkıp config/terms parametresine taşınır.
4. KAYNAK-1 t1dm-qual-ai-audit SKILL.md'den yalnız denetim iskeleti alınır.
5. Testler: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s
   plugins/sci-audit/tests — çekirdek testler stdlib-only geçmeli; Zemberek
   testleri paket yoksa skipUnless ile atlanır.

## Marketplace + doğrulama

1. .claude-plugin/marketplace.json'a sci-audit girdisi.
2. plugin-dev:plugin-validator ile yapı doğrulaması.
3. Duman testi: /plugin marketplace add ./ → install → yeni oturumda
   (a) SessionStart enjeksiyonu, (b) sahte-sır prompt bloğu,
   (c) tests/fixtures/sample-en.md üzerinde eksen A+C bulguları,
   (d) tests/fixtures/sample-tr.md üzerinde /sci-audit:check-turkish →
   G1/G3/G5 bulgularının (ondalık nokta, register ihlali, p biçimi)
   yakalandığını ve TDK provider'ının degrade sözleşmesini göster.
4. README'ye claude.ai web kurulum bölümü + hangi eksenin hangi MCP/provider
   olmadan nasıl degrade olduğunu gösteren matris.

Tamamlanınca dosya ağacı + test çıktısı + duman testi bulgularını raporla;
commit'i ben onaylamadan atma.
```

## Tasarım kararları (neden böyle)

- **permissions.deny katmanı plugin'e taşınmadı:** Claude Code plugin'leri
  permission kuralı dağıtamaz; sci-audit domain-bağımsız olduğu için KVKK
  deny-listesi de kapsam dışı kaldı. (Önceki `ai-reliability-guard` iterasyonunda
  bunun için `/reliability-init` çözümü tasarlanmıştı; gerekirse o desene dön.)
- **Grok yargıç → Claude subagent (style-judge):** claude.ai web'de anahtarsız,
  web-native çözüm. Grok adapter'ının "anahtar yoksa metin hiç gönderilmez"
  gizlilik sözleşmesi CI katmanında aynen korunur.
- **Stop hook çift kapı:** kaynaksız-sayı adli kapısı ile G5 imla kapısı tek
  mekanizmada birleşti.
- **tr_sciaudit CLI sözleşmesi korunur:** doktoratezi Kapı 4 iş akışı ve mevcut
  `*-tr-sciaudit.md` rapor formatıyla uyum bozulmaz.
- **MCP'ler remote + degrade:** claude.ai web sandbox'ında stdio/npx yok;
  MCP'siz eksen "unverified" etiketiyle sürer, çökmez.
