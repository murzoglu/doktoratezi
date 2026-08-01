# galileo-audit Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** sci-audit'in yanında, Roche-kapalı Galileo üzerinden bağımsız GPT-5.4 judge (A) + gemini-embedding-2 semantik-tutarlılık (B) + eval-harness (C) denetim katmanını, three-tier gate ile kurmak.

**Architecture:** Minerva↔evidentia deseni denetim tarafında: dependency-free stdio köprü (`scripts/eval/galileo_bridge.py`) Galileo REST'ini araçlara açar, proje `.mcp.json`'da `galileo-audit` MCP sunucusu olarak kaydolur, t1dm-tez-rehberi Faz 3.6'da advisory/soft-block pass olarak çağrılır. sci-audit plugin'i değişmez.

**Tech Stack:** Python 3 (stdlib `urllib`/`json` — dependency-free, Minerva köprüsü gibi), Galileo REST API (Roche-kapalı), MCP stdio (JSON-RPC 2.0), Markdown/YAML doküman + config.

## Global Constraints

- **Deployment:** Roche-kapalı (Azure OpenAI GPT-5.4 + Vertex gemini in-tenant). Kaynak: spec §2.
- **KVKK:** Galileo'ya **yalnız manuskript metni + getirilen literatür + references.bib** gider; ham katılımcı/aile-düzeyi/transkript/kimlikleyici **ASLA**. Kaynak: spec §7.
- **Kimlik:** `${GALILEO_API_KEY}`, `${GALILEO_CONSOLE_URL}`, `${GALILEO_JUDGE_MODEL}`=gpt-5.4, `${GALILEO_TEXT_EMBEDDING_MODEL}`=gemini-embedding-2, `${GALILEO_PROJECT}` — yalnız `os.environ`'dan; **değer asla basılmaz/commit edilmez**. `.env` Read/Bash **deny** — dokunulmaz.
- **Dependency-free:** köprü yalnız Python stdlib kullanır (Minerva köprüsü gibi); pip paketi eklenmez.
- **three-tier gate:** HARD (sci-audit, değişmez) / SOFT-block (Galileo eşikleri, insan-override'lı) / advisory. Eşik defaults: `groundedness<0,60`, `faithfulness<0,60`, nicel iddia `citation_support=unsupported`, çelişki `sim≥0,85+judge-onaylı`, büyük Claude↔GPT bütünlük çelişkisi. Kaynak: spec §5.
- **Dokunulmaz:** sci-audit/evidentia plugin iç dosyaları, `.claude/settings.json permissions.deny`, `.env`, ham veri katmanları.
- **Commit:** repo kuralı #14 — yalnız açık kullanıcı isteğiyle; `git add .` yok. Commit adımları tamamlık için gösterilir; yürütmede tek yetkili commit'te toplanır.
- **DISCOVERY CONTINGENCY:** Galileo REST yüzeyi Task 1'de canlı keşfedilir. Task 2–7'nin **araç kontratları (imza + dönüş şeması) ve canlı smoke-test'leri** bu planda kesindir; Galileo API-çağrı **iç-plumbing'i** Task 1'in keşfettiği kontrata göre yazılır ve her araç kendi canlı smoke-test'iyle doğrulanır (Minerva GraphQL keşfi gibi). Bu bir placeholder değil, doğrulanmamış dış-API entegrasyonunun doğru TDD kalıbıdır: test (oracle) tam, plumbing teste yakınsar.

## File Structure

| Dosya | Sorumluluk | Durum |
|---|---|---|
| `scripts/eval/galileo_bridge.py` | Dependency-free köprü: env kimlik + Galileo REST çağrıları + araç fonksiyonları (A/B/C) + MCP stdio sunucu | YENİ, **gitignored** |
| `scripts/eval/thesis_eval_run.py` | Batch harness (C): bölüm+kanıt dataset kurar, `galileo_eval_run` çağırır | YENİ, **gitignored** |
| `.claude/galileo.local.md` | Config + soft-block eşikleri (evidentia.local.md muadili) | YENİ, **gitignored** |
| `.mcp.json` | `galileo-audit` MCP sunucu girişi | MODIFY (zaten gitignored) |
| `.gitignore` | bridge + runner + galileo.local.md ignore | MODIFY |
| `.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md` | §"Galileo Bağımsız Judge + Semantik Katman" doktrini | MODIFY |
| `.claude/skills/t1dm-tez-rehberi/SKILL.md` | Faz 3.6 galileo advisory/soft-block adımı | MODIFY |
| `CONVENTIONS.md` (+ audit ikizi) | denetim-katmanı extension notu | MODIFY |
| `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | soft-block girdisi + override defter kaydı | MODIFY |

Not: köprü gitignored olduğundan tracked pytest yazılmaz; doğrulama **canlı smoke** (Minerva gibi, `/tmp` script'leri) iledir.

---

### Task 1: Phase 0 — Galileo REST kontrat keşfi (dependency-free)

**Files:**
- Create: `/tmp/galileo_probe.py` (geçici keşif script'i, repoya girmez)
- Create: `docs/superpowers/specs/2026-07-11-galileo-api-contract.md` (keşif raporu — gitignored: `*galileo*`? HAYIR, bu spec değil rapor; **gitignored yap:** ekle `.gitignore`'a `docs/superpowers/specs/2026-07-11-galileo-api-contract.md` çünkü iç hostname/endpoint taşıyabilir)

**Interfaces:**
- Produces: keşif raporu — Task 2+ köprü plumbing'i bunun kontratına (auth şeması, judge/scorer endpoint, embedding endpoint, routing) dayanır.

- [ ] **Step 1: Env değişken ADLARININ varlığını doğrula (değer basmadan)**

Run: `python3 -c "import os; ks=['GALILEO_API_KEY','GALILEO_CONSOLE_URL','GALILEO_JUDGE_MODEL','GALILEO_TEXT_EMBEDDING_MODEL','GALILEO_PROJECT']; print({k:(k in os.environ) for k in ks})"`
Expected: her anahtar için `True`/`False` (değer BASILMAZ). En az API_KEY + CONSOLE_URL True olmalı; değilse BLOCKED → kullanıcıya sor.

- [ ] **Step 2: Yaz — `/tmp/galileo_probe.py` (dependency-free REST keşfi)**

```python
import os, json, urllib.request, urllib.error
BASE = os.environ.get("GALILEO_CONSOLE_URL","").rstrip("/")
KEY  = os.environ.get("GALILEO_API_KEY","")
def _get(path, hdr=None):
    req = urllib.request.Request(BASE+path, headers=hdr or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read(4000).decode("utf-8","replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(800).decode("utf-8","replace")
    except Exception as e:
        return None, str(e)[:200]
# 1) OpenAPI / health discovery (do not print secrets)
for p in ["/openapi.json","/api/openapi.json","/healthz","/api/health","/v2/health"]:
    s,b = _get(p); print(p, "->", s, (b[:120] if isinstance(b,str) else b))
# 2) auth scheme probe (Bearer vs api-key header)
for hdr in [{"Authorization":"Bearer "+KEY}, {"Galileo-API-Key":KEY}, {"api-key":KEY}]:
    s,_ = _get("/api/v2/projects", hdr); print("auth", list(hdr)[0], "->", s)
print("DISCOVERY DONE")
```

Run: `python3 /tmp/galileo_probe.py`
Expected: en az bir endpoint 200/2xx; çalışan auth şeması (Bearer/api-key) belirlenir. Değer sızmaz.

- [ ] **Step 3: Judge + embedding endpoint keşfi**

`/tmp/galileo_probe.py`'ye ekle: keşfedilen OpenAPI'den (veya Galileo dokümentasyon kalıplarından) (a) scorer/evaluate/run endpoint'i ve (b) embedding endpoint'i (varsa) için minik POST denemeleri — trivial input ("The sky is blue." context="The sky is blue.") ile groundedness benzeri bir metrik + tek cümle embedding. Her denemede status + yanıt-şekli (anahtarlar) yazdır (içerik değil).

Run: `python3 /tmp/galileo_probe.py`
Expected: judge/scorer çağrısının döndürdüğü skor-şeması + embedding çağrısının döndürdüğü vektör-boyutu (veya "embedding endpoint yok, yalnız internal" notu) belirlenir.

- [ ] **Step 4: Yaz — keşif raporu `docs/superpowers/specs/2026-07-11-galileo-api-contract.md`**

Raporda: paket/REST tabanı, çalışan auth şeması, judge/scorer çağrı imzası (path, gövde, dönüş şeması), embedding çağrı imzası veya yokluğu, custom-rubric desteği, Roche-kapalı routing teyidi. **Hostname/endpoint taşır → gitignore.**

- [ ] **Step 5: `.gitignore`'a keşif raporunu ekle**

`.gitignore`'a: `docs/superpowers/specs/2026-07-11-galileo-api-contract.md`

- [ ] **Step 6: Doğrula + Commit**

Run: `git check-ignore docs/superpowers/specs/2026-07-11-galileo-api-contract.md && echo IGNORED`
Expected: `IGNORED`.
```bash
git add .gitignore
git commit -m "chore(galileo): API contract discovery report git-ignored"
```

---

### Task 2: Köprü çekirdeği — kimlik + config + connectivity

**Files:**
- Create: `scripts/eval/galileo_bridge.py`
- Create: `.claude/galileo.local.md`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: Task 1 keşif raporu (auth şeması, REST tabanı).
- Produces: `_galileo_base()`, `_key(name)`, `_request(url,hdr,method,body)`, `load_config()`, `t_galileo_stats(params)` — Task 3–7 bunları kullanır.

- [ ] **Step 1: `.gitignore`'a köprü + config ekle**

```gitignore
# Galileo bağımsız denetim katmanı (operatör-yerel, iç altyapı)
scripts/eval/galileo_bridge.py
scripts/eval/thesis_eval_run.py
.claude/galileo.local.md
```

- [ ] **Step 2: Yaz — `.claude/galileo.local.md` (config + eşikler)**

```markdown
---
enabled: true
judge_model_env: GALILEO_JUDGE_MODEL
embedding_model_env: GALILEO_TEXT_EMBEDDING_MODEL
project_env: GALILEO_PROJECT
soft_block:
  groundedness_min: 0.60
  faithfulness_min: 0.60
  contradiction_sim_min: 0.85
  citation_support_required: true
---

# Galileo Bağımsız Denetim — Proje Config (T1DM-Tez)

sci-audit'in YANINDA bağımsız GPT-5.4 judge + gemini-embedding-2 semantik katman.
three-tier gate: HARD (sci-audit) / SOFT-block (yukarıdaki eşikler, insan-override'lı)
/ advisory. KVKK: Galileo'ya yalnız manuskript + literatür + references.bib; ham veri asla.
Doktrin: `.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md`
§"Galileo Bağımsız Judge + Semantik Katman".
```

- [ ] **Step 3: Yaz — `galileo_bridge.py` çekirdeği (Task 1 auth şemasına göre)**

Çekirdek: env-kimlik okuyucu (`_key`), `_galileo_base()` (CONSOLE_URL normalize), `_request()` (urllib, Task 1'de doğrulanan auth header), `load_config()` (`.claude/galileo.local.md` frontmatter parse), `t_galileo_stats({})` → `{ok, project, judge_model, embedding_model, routing}` (değer değil, ad/erişilebilirlik). **Değer basılmaz.** [Plumbing Task 1 kontratına göre yazılır.]

- [ ] **Step 4: Canlı smoke — connectivity**

Run: `python3 -c "import importlib.util as u; s=u.spec_from_file_location('g','scripts/eval/galileo_bridge.py'); m=u.module_from_spec(s); s.loader.exec_module(m); print(m.t_galileo_stats({}))"`
Expected: `{ok: true, ...}` — Roche-kapalı bağlantı doğrulanır, env değeri sızmaz.

- [ ] **Step 5: Config + ignore doğrula**

Run: `python3 -c "import yaml; d=yaml.safe_load(open('.claude/galileo.local.md').read().split('---')[1]); assert d['enabled'] and d['soft_block']['groundedness_min']==0.60; print('cfg OK')"` ve `git check-ignore scripts/eval/galileo_bridge.py .claude/galileo.local.md`
Expected: `cfg OK` + iki yol ignore'lu.

- [ ] **Step 6: Commit**

```bash
git add .gitignore
git commit -m "feat(galileo): bridge core + local config (git-ignored infra)"
```

---

### Task 3: A — `galileo_judge` (GPT-5.4 bağımsız judge)

**Files:**
- Modify: `scripts/eval/galileo_bridge.py`

**Interfaces:**
- Consumes: Task 2 `_request`, `load_config`, Task 1 scorer kontratı.
- Produces: `t_galileo_judge(params) -> dict`. `params={text:str, section_type:str, evidence?:str}`. Dönüş: `{scores:{faithfulness:float, groundedness:float, citation_support:str, marmara_compliance:float, hallucination_risk:float}, rationale:str, flagged_spans:[str]}` (0–1 skorlar).

- [ ] **Step 1: Kontrat + smoke oracle sabitle (bu adım tam belirtilidir)**

Smoke: iki paragraf — (P1) kanıta dayalı ("Kanıt: X %22,4. Paragraf: X %22,4'tür."), (P2) uydurma ("Paragraf: X %90'dır." kanıt %22,4). Beklenen: `groundedness(P1) > 0.8` ve `groundedness(P2) < 0.5`; `citation_support(P2)="unsupported"`.

- [ ] **Step 2: Yaz — `t_galileo_judge` (Task 1 scorer endpoint'ine göre)**

Galileo scorer/evaluate çağrısını `${GALILEO_JUDGE_MODEL}` ile kur; input=evidence, output=text; 5-boyut skoru + gerekçe + span'ları dönüş şemasına eşle. [Plumbing Task 1 kontratına göre.]

- [ ] **Step 3: Canlı smoke — grounded vs ungrounded**

Run: `/tmp/galileo_judge_smoke.py` (P1/P2'yi `m.t_galileo_judge` ile çağırır, skorları basar).
Expected: Step 1 oracle sağlanır (P1 groundedness yüksek, P2 düşük + unsupported). Sağlanmazsa plumbing'i düzelt, tekrar et.

- [ ] **Step 4: Commit**

```bash
git commit -am "feat(galileo): A - independent GPT-5.4 judge tool"
```

---

### Task 4: B — semantik-tutarlılık araçları (gemini-embedding-2)

**Files:**
- Modify: `scripts/eval/galileo_bridge.py`

**Interfaces:**
- Consumes: Task 2 çekirdek, Task 1 embedding kontratı (veya embedding yoksa judge-tabanlı fallback).
- Produces: `t_galileo_consistency({texts:[str]}) -> {pairs:[{a:int,b:int,sim:float,type:str}]}`; `t_galileo_bib_dedup({entries:[{key,title,doi?}]}) -> {duplicates:[{a,b,sim}]}`; `t_galileo_claim_source_match({claim,source_text}) -> {score:float}`.

- [ ] **Step 1: Smoke oracle sabitle**

Smoke: (a) iki çelişen kısa metin → `consistency` bir `type="contradiction"` çifti; (b) references.bib'ten aynı makalenin iki varyantı → `bib_dedup` bir dup; (c) claim↔ilgili kaynak → `score>0.7`, claim↔alakasız → `score<0.3`.

- [ ] **Step 2: Yaz — üç semantik araç**

Embedding endpoint varsa cosine + eşik; contradiction için embedding + judge-onay (Task 3 judge ile ikili sınıflama). Embedding endpoint YOKSA (Task 1 böyle bulduysa): tümü judge-tabanlı semantik karşılaştırmaya düşer (fallback, raporda not). [Plumbing Task 1'e göre.]

- [ ] **Step 3: Canlı smoke**

Run: `/tmp/galileo_sem_smoke.py`
Expected: (a) contradiction çifti, (b) bib dup, (c) skorlar oracle'ı sağlar.

- [ ] **Step 4: Commit**

```bash
git commit -am "feat(galileo): B - semantic consistency tools (embedding)"
```

---

### Task 5: C — eval-harness

**Files:**
- Modify: `scripts/eval/galileo_bridge.py`
- Create: `scripts/eval/thesis_eval_run.py`

**Interfaces:**
- Consumes: Task 2–3 (`_request`, judge).
- Produces: `t_galileo_eval_run({dataset:[{input,output}], metrics:[str]}) -> {run_id:str, url?:str}`; `thesis_eval_run.py` CLI: bölüm dosyası + kanıt → dataset kurar, çağırır.

- [ ] **Step 1: Smoke oracle**

Smoke: 2-satırlık trivial dataset → `run_id` döner (experiment loglanır).

- [ ] **Step 2: Yaz — `t_galileo_eval_run` + `thesis_eval_run.py`**

Galileo experiment/run endpoint'ine dataset gönder; runner bölüm paragraflarını + (varsa) kanıtı dataset'e çevirir. **KVKK: yalnız manuskript/literatür.** [Plumbing Task 1'e göre.]

- [ ] **Step 3: Canlı smoke**

Run: `python3 scripts/eval/thesis_eval_run.py --dry-check` (trivial dataset loglar).
Expected: `run_id` döner; Galileo'da experiment görünür.

- [ ] **Step 4: Commit**

```bash
git add scripts/eval/thesis_eval_run.py
git commit -m "feat(galileo): C - eval harness + thesis runner"
```

---

### Task 6: three-tier gate sınıflandırıcı

**Files:**
- Modify: `scripts/eval/galileo_bridge.py`

**Interfaces:**
- Consumes: Task 3–4 dönüşleri + Task 2 `load_config` eşikleri.
- Produces: `classify_gate(judge_result, consistency_result, config) -> {hard:[], soft_block:[], advisory:[]}`.

- [ ] **Step 1: Smoke oracle (tam belirtili)**

- `groundedness=0.5` (<0,60) → `soft_block` içinde bir kayıt.
- `citation_support="unsupported"` → `soft_block`.
- contradiction `sim=0.9`+confirmed → `soft_block`.
- bib dup → `advisory`.
- HARD (decimal/uydurma-künye) sci-audit'e ait → bu fn üretmez (yalnız soft/advisory).

- [ ] **Step 2: Yaz — `classify_gate`**

```python
def classify_gate(judge, consistency, cfg):
    sb = cfg["soft_block"]; soft=[]; adv=[]
    sc = (judge or {}).get("scores", {})
    if sc.get("groundedness", 1) < sb["groundedness_min"]:
        soft.append({"type":"groundedness_low","value":sc.get("groundedness")})
    if sc.get("faithfulness", 1) < sb["faithfulness_min"]:
        soft.append({"type":"faithfulness_low","value":sc.get("faithfulness")})
    if sb.get("citation_support_required") and sc.get("citation_support")=="unsupported":
        soft.append({"type":"citation_unsupported"})
    for p in (consistency or {}).get("pairs", []):
        if p.get("type")=="contradiction" and p.get("sim",0) >= sb["contradiction_sim_min"]:
            soft.append({"type":"cross_chapter_contradiction","pair":[p["a"],p["b"]],"sim":p["sim"]})
        elif p.get("type")=="redundancy":
            adv.append({"type":"redundancy","pair":[p["a"],p["b"]]})
    return {"hard":[], "soft_block":soft, "advisory":adv}
```

- [ ] **Step 3: Canlı/birim smoke**

Run: `/tmp/galileo_gate_smoke.py` (sentetik judge/consistency dict'leriyle `classify_gate` çağırır).
Expected: Step 1 oracle'ın her maddesi doğru kovaya düşer.

- [ ] **Step 4: Commit**

```bash
git commit -am "feat(galileo): three-tier gate classifier (soft-block thresholds)"
```

---

### Task 7: MCP kaydı (`galileo-audit`)

**Files:**
- Modify: `.mcp.json`

**Interfaces:**
- Consumes: `galileo_bridge.py` (Task 2–6 araçları).

- [ ] **Step 1: `.mcp.json`'a galileo-audit sunucusu ekle**

Mevcut `minerva-evidence` girişinin yanına `galileo-audit`: `command: python3`, `args: ["${CLAUDE_PROJECT_DIR}/scripts/eval/galileo_bridge.py"]`, `env` bloğu `${GALILEO_API_KEY}` / `${GALILEO_CONSOLE_URL}` / `${GALILEO_JUDGE_MODEL}` / `${GALILEO_TEXT_EMBEDDING_MODEL}` / `${GALILEO_PROJECT}` / `${CURL_CA_BUNDLE}` forward eder.

- [ ] **Step 2: MCP stdio protokol smoke (subprocess, restart gerekmeden)**

Run: JSON-RPC handshake (`initialize` + `tools/list`) `galileo_bridge.py`'ye pipe et (Minerva test kalıbı).
Expected: serverInfo + araç listesi (galileo_judge, galileo_consistency, galileo_bib_dedup, galileo_claim_source_match, galileo_eval_run, galileo_stats). Not: native `mcp__galileo-audit__*` araçları yalnız Claude Code restart'ında görünür.

- [ ] **Step 3: Commit**

```bash
git add .mcp.json
git commit -m "feat(galileo): register galileo-audit MCP server"
```

---

### Task 8: Repo-katmanı doktrin + kablolama

**Files:**
- Modify: `.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md`
- Modify: `.claude/skills/t1dm-tez-rehberi/SKILL.md`
- Modify: `CONVENTIONS.md` + `plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/CONVENTIONS.md`
- Modify: `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`

**Interfaces:**
- Consumes: Task 2–7 araç adları + three-tier eşikleri.

- [ ] **Step 1: Doktrin bölümü ekle (manuskript-denetimi-sciaudit.md)**

`§"Galileo Bağımsız Judge + Semantik Katman"`: extension deseni (plugin değişmez), 6 araç, three-tier gate + eşikler, KVKK (yalnız manuskript/literatür), Roche-kapalı, env-adları (değer yok), Faz 3.6 devreye girişi. Doğrula: `grep -n 'Galileo Bağımsız Judge' <dosya>`.

- [ ] **Step 2: SKILL Faz 3.6'ya galileo adımı ekle**

Faz 3.6 (sci-audit) sonrası: "galileo-audit advisory/soft-block pass — bağımsız GPT-5.4 judge + semantik-tutarlılık; three-tier: HARD sci-audit değişmez, SOFT-block `certified-final`'i durdurur (insan-override kayıtlı), advisory rapor. Doktrin: köprü §Galileo." Doğrula: `grep -n 'galileo' SKILL.md`.

- [ ] **Step 3: conventions extension notu (iki ikiz)**

Her iki CONVENTIONS'a: "Denetim katmanı extension `galileo-audit` (Roche-kapalı Galileo: GPT-5.4 judge + gemini-embedding-2), sci-audit'in YANINDA, gitignored köprü `scripts/eval/galileo_bridge.py`; three-tier gate; KVKK yalnız manuskript/literatür. Doktrin: manuskript-denetimi-sciaudit.md §Galileo." İkizde karşılık blok varsa parite.

- [ ] **Step 4: sertifikasyon playbook — soft-block girdisi**

`bolum-finalizasyon-sertifikasyon-playbook.md`'ye: galileo SOFT-block bir sertifika girdisidir; soft-block varsa bölüm en fazla `provisional-pass`; `certified-final` yalnız düzeltme veya sertifika-defterine (`tez-yazim/04_kalite-kontrol/sertifikalar/`) yazılan açık override gerekçesiyle. Doğrula: `grep -n -i 'galileo\|soft-block' <dosya>`.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md .claude/skills/t1dm-tez-rehberi/SKILL.md CONVENTIONS.md plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/CONVENTIONS.md tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md
git commit -m "docs(galileo): Faz 3.6 wiring + doctrine + soft-block certification"
```

---

### Task 9: Final entegrasyon doğrulaması + lint

**Files:**
- Modify: `docs/superpowers/specs/2026-07-11-galileo-audit-integration-design.md` (lint)

**Interfaces:**
- Consumes: tüm task'lar.

- [ ] **Step 1: Uçtan uca entegrasyon smoke**

Run:
```bash
python3 -c "import importlib.util as u; s=u.spec_from_file_location('g','scripts/eval/galileo_bridge.py'); m=u.module_from_spec(s); s.loader.exec_module(m); print('stats', m.t_galileo_stats({}).get('ok'))"
python3 -c "import yaml; yaml.safe_load(open('.claude/galileo.local.md').read().split('---')[1]); print('cfg OK')"
git check-ignore scripts/eval/galileo_bridge.py scripts/eval/thesis_eval_run.py .claude/galileo.local.md
grep -q 'Galileo Bağımsız Judge' .claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md && echo doctrine OK
grep -q -i 'galileo' .claude/skills/t1dm-tez-rehberi/SKILL.md && echo skill OK
```
Expected: `stats True`, `cfg OK`, üç yol ignore'lu, `doctrine OK`, `skill OK`.

- [ ] **Step 2: KVKK guard doğrulaması**

Köprü invocation-contract'ının yalnız `text`/`evidence`/`bib` alanları aldığını (ham-veri alanı geçmediğini) gözden geçir + doktrinde KVKK cümlesinin varlığını doğrula. Run: `grep -c -i 'yalnız.*literatür\|ham.*veri.*asla\|KVKK' .claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md`. Expected: ≥1.

- [ ] **Step 3: Spec lint temizliği**

Design + bu plan spec'lerinde MD022/031/032/060 uyarılarını boş-satır/tablo-boşluğu ile temizle (yalnız whitespace). 

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/specs/2026-07-11-galileo-audit-integration-design.md docs/superpowers/plans/2026-07-11-galileo-audit-integration.md
git commit -m "chore(galileo): final integration verify + spec lint"
```

---

## Self-Review

**1. Spec coverage:**
- spec §4 köprü + A/B/C araçları → Task 2/3/4/5 ✓
- spec §4 config `.claude/galileo.local.md` → Task 2 ✓
- spec §5 three-tier gate + eşikler → Task 6 (classify_gate) + Task 2 (config) ✓
- spec §8 Phase 0 API keşfi → Task 1 ✓
- spec §9 doktrin/kablolama (manuskript §Galileo, Faz 3.6, conventions, sertifikasyon) → Task 8 ✓
- spec §7 KVKK/governance → Global Constraints + Task 9 Step 2 ✓
- spec §4 MCP kayıt → Task 7 ✓
- spec §10 test/kabul → her task canlı smoke + Task 9 ✓

**2. Placeholder scan:** Kontratlar (imza+dönüş), canlı smoke oracle'ları ve `classify_gate` tam kodludur. Galileo API-plumbing'i "DISCOVERY CONTINGENCY" altında Task 1 kontratına bağlıdır — bu placeholder değil, doğrulanmamış dış-API için TDD kalıbı (test tam, plumbing teste yakınsar). Minerva precedent'iyle aynı.

**3. Tip/isim tutarlılığı:** `t_galileo_judge`/`t_galileo_consistency`/`t_galileo_bib_dedup`/`t_galileo_claim_source_match`/`t_galileo_eval_run`/`t_galileo_stats` + `classify_gate` + `load_config` adları Task 2→9 boyunca tutarlı; `.claude/galileo.local.md` eşik anahtarları (`groundedness_min` vb.) Task 2 config ↔ Task 6 classify_gate arasında birebir.

**Not (bağımlılık):** Task 1 keşfi embedding endpoint bulamazsa Task 4 judge-tabanlı fallback'e düşer (planda belirtili); bu bir plan boşluğu değil, keşfe-bağlı dallanmadır.
