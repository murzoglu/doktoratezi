# Kalite Kontrol — Otomatik Zorlama ve Kapsam Genişletme Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. TDD zorunlu: her kod adımı önce başarısız test, sonra minimal uygulama.

**Goal:** Tez yazım sürecindeki mevcut kalite-kontrol mekanizmalarının hiçbirinin atlanamamasını sağlamak; %66'sı manuel/advisory olan QC yüzeyini otomatik-ateşlenir ve tüm-gövde-kapsamlı hâle getirmek.

**Architecture:** Üç hamle: (1) kapsam genişletme — mevcut denetçileri (numeric-trace, causal-label, r-generator-literal, PII) CSR/ch05'ten tüm `chapters/*.qmd` gövdesine yay ve `tez_checklist_verify.py`'a yeni K-maddeleri ekle; (2) otomatik-ateşleme — 28-madde ana kapısını bir `--closing` moduna + git pre-commit'e + genişletilmiş Stop hook'una bağla; (3) orphan bağlama — hatta koşmayan denetçileri (doi_title_resolve, tr_sciaudit axis-G, targets file-tracking, librsvg preflight) checklist maddelerine dönüştür. Her hook değişikliği Codex ikizine (`​.codex/hooks/`) ve `tests/test_claude_hooks.py`'a birlikte işlenir.

**Tech Stack:** Python 3 (stdlib; ağ-bağımlı adımlar SKIP-dostu), Claude Code hook sözleşmesi (stdin JSON → stdout JSON / exit 2), git hooks (bash), `scripts/util/tez_checklist_verify.py` kayıt kaydı, `unittest`.

## Global Constraints

- **KVKK/veri sınırı:** Hiçbir kontrol `data/raw|identified|cleaned|backup` içeriğini VEYA `data/processed`/`outputs` satır düzeyini okumaz; yalnız varlık/metadata/metin. (`talimatname-claude-code.md` §2)
- **İkiz-ağaç kuralı:** Her `.claude/hooks/` değişikliği `​.codex/hooks/` ikizine + `tests/test_claude_hooks.py`'a birlikte işlenir; `chk_hooks_twin` (K5-HOK-01) iki kolun `*.py` küme eşitliğini zorlar → dosya adları BİREBİR aynı kalmalı.
- **Kayıt otoritesi script'tir:** Yeni kontrol önce `tez_checklist_verify.py` `_reg()` içine `add(...)` ile girer, sonra `tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md`'ye ID+mekanizma+araç satırı işlenir; `--audit-doc` 0 yetim vermelidir.
- **Salt-okuma orkestratör:** `tez_checklist_verify.py` hiçbir dosyayı değiştirmez; yeni denetçiler de salt-okuma (yan-etkisiz) olmalı.
- **Statü sözlüğü:** `Result(cid, status, evidence)`; status ∈ {PASS, FAIL, SKIP, MANUEL}; FAIL exit=1 (teslim engeli), MANUEL exit'i etkilemez.
- **Registry imzası:** `add(cid, eksen, katman, baslik, fn)`; `katman ∈ {"tez","bolum"}`; `fn(cid, ctx)` → `Result`; `ctx = {"fast": bool, "chapter": str|None, "closing": bool}` (`closing` bu planla eklenir).
- **Fail-open hook:** Hook'lar bozuk girdide çökmemeli (`_common.read_event` fail-open); yeni Stop kuralları da yanlış-pozitifte turu bloklamamalı.
- **Ağ-dostu:** Ağ gerektiren denetçiler (doi_title_resolve) `--fast`'te ve ağ yoksa SKIP döner, asla FAIL.

---

## File Structure

| Dosya | Sorumluluk | İşlem |
|---|---|---|
| `scripts/util/tez_checklist_verify.py` | 28→+N madde kayıt + `--closing` mod + gate-presence invariant | Modify |
| `scripts/util/csr_numeric_trace_audit.py` | (mevcut) ch04/ch05 hedef alır — arg yüzeyi hazır | Consume |
| `scripts/util/r_generator_literal_audit.py` | SCAN_DIRS'e chapters inline-chunk kapsamı | Modify |
| `scripts/util/csr_causal_label_audit.py` | (mevcut) `--csr <chapter>` hedef alır | Consume |
| `scripts/util/targets_file_tracking_audit.py` | YENİ — `_targets.R` `format="file"` linter (Kaide-2) | Create |
| `scripts/util/pii_value_scan.py` | YENİ — değer-şekilli PII (TC/tarih/hastane-ID) tüm manuskript | Create |
| `.claude/hooks/stop_verify.py` + `.codex/hooks/stop_verify.py` | tr-pvalue nokta-ondalık + `*-pending` ledger Stop kapısı | Modify (twin) |
| `.claude/hooks/pre_tool_use_policy.py` + twin | (Task 10) references.bib/chapters Write/Edit yazma-kapısı | Modify (twin) |
| `.claude/settings.json` + `.codex/hooks.json` | (Task 10) PreToolUse Write|Edit matcher | Modify (twin) |
| `scripts/util/install_git_hooks.sh` | YENİ — pre-commit kurucu (opt-in) | Create |
| `tests/test_claude_hooks.py` | Yeni Stop/PreToolUse davranış testleri | Modify |
| `tests/test_qc_coverage.py` | YENİ — yeni checklist maddeleri + linter'lar için test | Create |
| `tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md` | Yeni ID satırları + kapsama matrisi | Modify |
| `AGENTS.md` / `CLAUDE.md` | `--closing` + pre-commit + yeni kaide dokümantasyonu | Modify |

---

## Faz haritası (öncelik)

- **P0 — Otomatik ateşle:** Task 1 (`--closing`), Task 9 (Stop genişletme), Task 10 (references.bib yazma-kapısı), Task 11 (pre-commit).
- **P1 — Kapsamı gövdeye yay:** Task 2 (ch04 numeric), Task 3 (ch05 causal), Task 8 (PII breadth).
- **P2 — Orphan bağla:** Task 4 (targets file-tracking), Task 5 (librsvg), Task 6 (doi_title_resolve), Task 7 (axis G).
- **P3 — Derin katman + teslim:** Task 12 (sertifika tazeliği), Task 13 (karma cross-arm), Task 14 (galileo zorunlu-toplama), Task 15 (doc senkron + --audit-doc).

Uygulama sırası **güvenlik-önce**: additive checklist maddeleri (Task 2-8) workflow'u kırmaz (yalnız manuel checklist koşumunda ısırır) → önce onlar; runtime friction (Task 9-11) ikinci dalga, ikiz-ağaç + test ile.

---

### Task 1: `--closing` modu + gate-presence invariant

Kapanış koşumunun `--fast` ile sahte-yeşil vermesini ve eksik-araç/CSR'ın sessiz SKIP'e düşmesini engeller.

**Files:**
- Modify: `scripts/util/tez_checklist_verify.py` (main argparse + ctx + `chk_*` SKIP mantığı)
- Test: `tests/test_qc_coverage.py`

**Interfaces:**
- Produces: `ctx["closing"]: bool`; closing modda `--fast` reddi (exit 2); kayıtlı ağır denetçi SKIP → FAIL dönüşümü.

- [ ] **Step 1: Failing test**
```python
# tests/test_qc_coverage.py
import subprocess, sys, os
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
VERIFY = REPO / "scripts/util/tez_checklist_verify.py"
def run(args):
    return subprocess.run([sys.executable, str(VERIFY), *args],
        capture_output=True, text=True, cwd=str(REPO),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
def test_closing_refuses_fast():
    p = run(["--closing", "--fast"])
    assert p.returncode == 2, p.stdout + p.stderr
    assert "closing" in (p.stdout + p.stderr).lower()
```
- [ ] **Step 2: Run → FAIL** `python3 -m pytest tests/test_qc_coverage.py::test_closing_refuses_fast -v` → `--closing` bilinmiyor.
- [ ] **Step 3: Implement** — argparse'a `--closing` ekle; `if args.closing and args.fast: sys.stderr.write("--closing --fast ile birlikte kullanılamaz (kapanış tam denetim gerektirir)\n"); return 2`; `ctx["closing"]=args.closing`. Her ağır `chk_*` içindeki `return Result(cid, SKIP, ...)` dallarını `_skip_or_fail(cid, ctx, reason)` yardımcısına çevir: `def _skip_or_fail(cid, ctx, reason): return Result(cid, FAIL if ctx.get("closing") else SKIP, reason)` — yalnız araç/CSR/tool eksikliği SKIP'lerinde (render/pdf/renv/targets/csr/tool-missing), `--fast` SKIP'inde değil.
- [ ] **Step 4: Run → PASS**
- [ ] **Step 5: Commit** `git add scripts/util/tez_checklist_verify.py tests/test_qc_coverage.py && git commit -m "feat(qc): --closing modu + gate-presence invariant"`

---

### Task 2: K5-NUM-03 — Bulgular (ch04) sayısal iz + inline-chunk R literal kapsamı

Bulgular bölümünün kendi sayıları (BF/AUC/ICC/β) hiçbir sert kapıdan geçmiyordu (denetim madde B, doğrulandı: `csr_numeric_trace_audit` varsayılanı CSR, `r_generator_literal_audit` SCAN_DIRS=`["R","scripts/R"]`).

**Files:**
- Modify: `scripts/util/tez_checklist_verify.py` (`chk_numeric_trace_bulgular` + registry)
- Modify: `scripts/util/r_generator_literal_audit.py` (chapters inline-chunk tarayıcı)
- Test: `tests/test_qc_coverage.py`

**Interfaces:**
- Consumes: `csr_numeric_trace_audit.py --csr chapters/04_bulgular.qmd` (arg yüzeyi mevcut).
- Produces: `chk_numeric_trace_bulgular(cid, ctx) -> Result`; registry ID `K5-NUM-03`.

- [ ] **Step 1: Failing test**
```python
def test_k5_num_03_registered():
    p = run(["--list"])
    assert "K5-NUM-03" in p.stdout
```
- [ ] **Step 2: Run → FAIL**
- [ ] **Step 3: Implement** — `chk_numeric_trace_discussion`'ı şablon alarak `chk_numeric_trace_bulgular` ekle (`chapter="chapters/04_bulgular.qmd"`, out-* dosyaları `ch04_*`); `_reg()`'e `add("K5-NUM-03","AI-reliability/Teknik","tez","ch04 Bulgular sayısal iddia → CSV izi", chk_numeric_trace_bulgular)`. `r_generator_literal_audit.py`: yeni `--include-chapters` bayrağı → `SCAN_DIRS`'e ek olarak `chapters/*.qmd` içindeki ```` ```{r} ```` chunk'larını (regex `^```\{r[^}]*\}$ ... ^```$`) tarayıp aynı literal kuralını uygula.
- [ ] **Step 4: Run → PASS** + `python3 scripts/util/tez_checklist_verify.py --section K5-NUM-03` (canlı sonuç; FAIL çıkarsa gerçek kaynaksız sayı bulundu → ayrı ele al).
- [ ] **Step 5: Commit**

---

### Task 3: K5-CAU-02 — ch05 Tartışma nedensel-dil kapısı

Nedensel-dil denetimi yalnız CSR'de koşuyordu; gerçek Tartışma bölümü kapsam dışıydı (denetim madde G/breadth).

**Files:** Modify `tez_checklist_verify.py`; Test `tests/test_qc_coverage.py`
**Interfaces:** Consumes `csr_causal_label_audit.py --csr chapters/05_tartisma_ve_sonuc.qmd`; Produces `K5-CAU-02`.

- [ ] **Step 1: Failing test** `assert "K5-CAU-02" in run(["--list"]).stdout`
- [ ] **Step 2: Run → FAIL**
- [ ] **Step 3: Implement** — `chk_causal_label_discussion` (mevcut `chk_causal_label`'ı `--csr chapters/05_tartisma_ve_sonuc.qmd` ile çağır; script bu argümanı destekliyorsa; desteklemiyorsa Task 3a: `csr_causal_label_audit.py`'a `--csr` argümanı ekle, default korunur). Registry: `add("K5-CAU-02", "AI-reliability/Teknik", "tez", "ch05 Tartışma nedensel dil + etiket disiplini", chk_causal_label_discussion)`.
- [ ] **Step 4: Run → PASS** + canlı `--section K5-CAU-02`
- [ ] **Step 5: Commit**

---

### Task 4: K5-TRK-01 — `_targets.R` `format="file"` file-tracking linter (Kaide-2)

Kaide-2 (türetilmiş CSV/RDS okuyan hedef `format="file"` ile izlenir) hiçbir denetçiye bağlı değildi (orphan-rule).

**Files:** Create `scripts/util/targets_file_tracking_audit.py`; Modify `tez_checklist_verify.py`; Test `tests/test_qc_coverage.py`
**Interfaces:** Produces `targets_file_tracking_audit.py` (exit 0=temiz, 1=izlenmeyen dosya-okuma); `chk_targets_file_tracking` → `K5-TRK-01`.

- [ ] **Step 1: Failing test**
```python
def test_targets_file_tracking_tool_exists():
    assert (REPO/"scripts/util/targets_file_tracking_audit.py").exists()
def test_k5_trk_01_registered():
    assert "K5-TRK-01" in run(["--list"]).stdout
```
- [ ] **Step 2: Run → FAIL**
- [ ] **Step 3: Implement** — `targets_file_tracking_audit.py`: `_targets.R`'i oku; her `tar_target(...)` bloğunda gövde `read_csv|read.csv|readRDS|read_rds|fread` ile bir `data/processed/*` veya `outputs/*` yolu okuyorsa VE aynı hedef tanımında `format = "file"` yoksa (ya da yolu izleyen bir `format="file"` bağımlı-hedef yoksa) bulgu yaz. Salt-okuma, stdlib regex. `chk_targets_file_tracking`: `_run([sys.executable, tool])`; exit 0→PASS, 1→FAIL. Registry `add("K5-TRK-01","AI-reliability/Teknik","tez","_targets.R format=file dosya-izleme (Kaide-2)", chk_targets_file_tracking)`.
- [ ] **Step 4: Run → PASS**
- [ ] **Step 5: Commit**

---

### Task 5: R-SVG-01 — librsvg render önkoşulu

SVG-ağırlıklı figürler `rsvg-convert` yoksa sessizce boş rasterize olur ("render success" yalan) — denetim orphan.

**Files:** Modify `tez_checklist_verify.py`; Test `tests/test_qc_coverage.py`
**Interfaces:** Produces `chk_svg_preflight` → `R-SVG-01`.

- [ ] **Step 1: Failing test** `assert "R-SVG-01" in run(["--list"]).stdout`
- [ ] **Step 2: Run → FAIL**
- [ ] **Step 3: Implement** — `chk_svg_preflight`: `chapters/`+`docs/assets` altında `.svg` figür varsa `_which("rsvg-convert")`; yoksa `_skip_or_fail` (closing→FAIL, normal→FAIL çünkü offline ve deterministik: `return Result(cid, FAIL, "SVG figürü var ama rsvg-convert yok → boş rasterize riski")`); SVG yoksa SKIP. Registry `add("R-SVG-01","Render/Çıktı","tez","librsvg (rsvg-convert) önkoşulu — SVG boş-rasterize koruması", chk_svg_preflight)`.
- [ ] **Step 4: Run → PASS**
- [ ] **Step 5: Commit**

---

### Task 6: K1-DOI-01 — DOI yanlış-atıf çözümleme (orphan bağlama)

`doi_title_resolve.py` normal akışta hiç koşmuyordu; yanlış-atıf/retraction sızıntısı (denetim madde C).

**Files:** Modify `tez_checklist_verify.py`; Test `tests/test_qc_coverage.py`
**Interfaces:** Consumes `doi_title_resolve.py` (references.bib DOI'lerini Crossref başlığıyla karşılaştırır). Ağ-bağımlı → `--fast` ve ağ-yok'ta SKIP.

- [ ] **Step 1: Failing test** `assert "K1-DOI-01" in run(["--list"]).stdout`
- [ ] **Step 2: Run → FAIL**
- [ ] **Step 3: Implement** — `chk_doi_title`: `if ctx["fast"]: return Result(cid, SKIP, "--fast: DOI çözümleme atlandı")`; araç yoksa SKIP; `_run([sys.executable, tool, "--bib","references/references.bib","--fail-on-mismatch"], timeout=600)`; exit 0→PASS, ağ hatası (127/124/timeout işareti)→SKIP, mismatch exit→FAIL. Registry `add("K1-DOI-01","Kanıt/Literatür","tez","DOI↔başlık yanlış-atıf çözümleme (Crossref)", chk_doi_title)`. NOT: `doi_title_resolve.py`'da `--fail-on-mismatch` yoksa Task 6a olarak ekle (default davranış korunur).
- [ ] **Step 4: Run → PASS/SKIP**
- [ ] **Step 5: Commit**

---

### Task 7: K4-TRG-01 — Türkçe bilimsel-yazım Ekseni G deterministik çekirdek

"Zorunlu/kanonik" işaretli axis-G (G1–G6, ondalık-nokta-p blocker dahil) 28-madde paketinde yoktu (denetim madde D).

**Files:** Modify `tez_checklist_verify.py`; Test `tests/test_qc_coverage.py`
**Interfaces:** Consumes sci-audit `tr_sciaudit.py` (plugin içi; `${CLAUDE_PLUGIN_ROOT}` veya bilinen yol). Bulunamazsa **loud SKIP** (varlığı açıkça raporlanır, sessiz geçilmez).

- [ ] **Step 1: Failing test** `assert "K4-TRG-01" in run(["--list"]).stdout`
- [ ] **Step 2: Run → FAIL**
- [ ] **Step 3: Implement** — `chk_axis_g`: `tr_sciaudit.py`'ı sırayla ara: (a) `$CLAUDE_PLUGIN_ROOT`, (b) `~/.claude/plugins/**/sci-audit/**/tr_sciaudit.py` glob, (c) `/workspaces/CureoPrivate/plugins/sci-audit/**`. Bulunursa her `chapters/*.qmd` üzerinde `--lang tr --fail-on error` koştur (G5 nokta-ondalık-p blocker); exit≠0→FAIL. Bulunamazsa `_skip_or_fail(cid, ctx, "tr_sciaudit çekirdeği bulunamadı — axis G koşulamadı")` (closing→FAIL). Registry `add("K4-TRG-01","Türkçe/Akış","tez","Bilimsel-yazım Ekseni G çekirdeği (G1-G6, nokta-ondalık-p)", chk_axis_g)`.
- [ ] **Step 4: Run → PASS/SKIP**
- [ ] **Step 5: Commit**

---

### Task 8: K0-PII-03 — Değer-şekilli PII taraması (tüm manuskript)

PII taraması yalnız kolon-adı ve bölüm-dardı; 11-hane TC/doğum-tarihi/hastane-ID değer desenleri kapsanmıyordu (denetim madde H).

**Files:** Create `scripts/util/pii_value_scan.py`; Modify `tez_checklist_verify.py`; Test `tests/test_qc_coverage.py`
**Interfaces:** Produces `pii_value_scan.py` (exit 0=temiz, 1=aday PII değeri); `chk_pii_value_scan` → `K0-PII-03`.

- [ ] **Step 1: Failing test**
```python
def test_pii_value_scan_flags_tckn(tmp_path):
    import subprocess, sys
    f = tmp_path/"x.qmd"; f.write_text("Katılımcı TC 12345678901 olarak...", encoding="utf-8")
    p = subprocess.run([sys.executable, str(REPO/"scripts/util/pii_value_scan.py"), "--paths", str(f)],
        capture_output=True, text=True)
    assert p.returncode == 1
```
- [ ] **Step 2: Run → FAIL**
- [ ] **Step 3: Implement** — `pii_value_scan.py`: desenler = `\b[1-9]\d{10}\b` (TC, checksum opsiyonel), `\b\d{2}[./]\d{2}[./](19|20)\d{2}\b` (doğum tarihi), `\b(protokol|dosya|hasta)\s*no\s*[:=]?\s*\d{4,}\b`, Azure/api-key sınıfı `_common.SECRET_PATTERNS`. `--paths` verilen dosyaları, verilmezse `chapters/*.qmd`+`docs/CLINICAL-STUDY-REPORT-FINAL.md`+`00*`/`04`/`07`'yi tara. `chk_pii_value_scan` çağırır. Registry `add("K0-PII-03","Kapsam/Gizlilik","tez","Değer-şekilli PII (TC/tarih/hasta-ID) tüm manuskriptte yok", chk_pii_value_scan)`. **Yanlış-pozitif notu:** yıl (2024) ve n=241 gibi sayılar hariç tutulacak desen sıkılığı; şüpheli çıktı MANUEL değil FAIL (kasıtlı sıkı).
- [ ] **Step 4: Run → PASS**
- [ ] **Step 5: Commit**

---

### Task 9: Stop hook genişletme — tr-pvalue nokta-ondalık + `*-pending` ledger (twin + tests)

Turn-end'de otomatik ateşlenen tek kapı yalnız kaynaksız-sayıydı; §1.4 nokta-ondalık-p ve çözülmemiş ledger satırları turn-end'de yakalanmıyordu (denetim madde A/orphans).

**Files:**
- Modify: `.claude/hooks/stop_verify.py` **ve** `​.codex/hooks/stop_verify.py` (BİREBİR)
- Modify: `tests/test_claude_hooks.py`

**Interfaces:** Produces genişletilmiş Stop kararı; yeni bloklar mevcut `stop_hook_active` kaçışına ve fail-open sözleşmesine tabi.

- [ ] **Step 1: Failing test** (test_claude_hooks.py `StopVerifyTests`'e)
```python
def test_blocks_decimal_dot_pvalue(self):
    transcript = self.make_transcript("Etki anlamlıydı (p=0.032).")
    proc = run_hook("stop_verify.py",
        {"hook_event_name":"Stop","stop_hook_active":False,"transcript_path":transcript})
    self.assertEqual("block", stdout_json(proc).get("decision"))
def test_allows_comma_pvalue(self):
    transcript = self.make_transcript("Etki anlamlıydı (p=0,032) (outputs/tables/t.csv).")
    proc = run_hook("stop_verify.py",
        {"hook_event_name":"Stop","stop_hook_active":False,"transcript_path":transcript})
    self.assertTrue(stdout_json(proc).get("continue"))
```
- [ ] **Step 2: Run → FAIL** `python3 tests/test_claude_hooks.py`
- [ ] **Step 3: Implement (her iki ağaç aynı)** — `stop_verify.py`'a: `PVALUE_DOT = re.compile(r"\bp\s*[=<>]\s*0\.\d+", re.I)`; `main()` içinde `msg` üzerinde `if PVALUE_DOT.search(msg): block reason "§1.4: nokta-ondalık p değeri (p=0.NNN) — virgül kullan (p=0,NNN)"`. Ledger kontrolü: transcript'e değil, yalnız asistan mesajı `chapters/`/`references.bib` düzenlediğini iddia ediyorsa `referans-denetim-ledgeri.md`'de `-pending` satır sayısını oku; >0 ise `additionalContext` uyarısı (block değil — yanlış-pozitif riski; yalnız bilgilendirici). Yeni bloklar `stop_hook_active`'ten SONRA, mevcut mantıktan ÖNCE.
- [ ] **Step 4: Run → PASS** (twin dosya kümesi eşit kalmalı → `chk_hooks_twin` PASS)
- [ ] **Step 5: Commit** `git add .claude/hooks/stop_verify.py .codex/hooks/stop_verify.py tests/test_claude_hooks.py`

---

### Task 10: references.bib / chapters yazma-zamanı kapısı (FRICTION — onay ile aktifleştir)

`references.bib`'e doğrudan satır eklenebiliyordu; yazma-zamanı kapısı yok (denetim madde C, high). **Bu adım günlük düzenleme sürtünmesini artırır** → varsayılan uyarı-modu, blok-modu env bayrağıyla.

**Files:** Modify `.claude/hooks/pre_tool_use_policy.py` + twin; `.claude/settings.json` + `.codex/hooks.json` (Write|Edit matcher ekle); `tests/test_claude_hooks.py`
**Interfaces:** PreToolUse `Write|Edit` matcher; hedef `references/references.bib` VEYA `chapters/*.qmd` ise `bib_hygiene.py` HARD çıkarsa `permissionDecision:"deny"` (env `QC_BIB_WRITE_GATE=block`) yoksa `additionalContext` uyarısı.

- [ ] **Step 1-5:** RED test (Write event on references.bib with orphan cite → deny under block-mode) → implement matcher + hook branch → twin sync → settings matcher → test PASS → commit. **Aktifleştirme kullanıcı onayına tabi** (varsayılan uyarı-modu).

---

### Task 11: pre-commit kurucu (FRICTION — opt-in)

28-madde ana kapısı hiçbir git akışına bağlı değil (denetim madde A, doğrulandı). **Auto-abort commit sürtünmelidir** → kurucu script, elle çalıştırma.

**Files:** Create `scripts/util/install_git_hooks.sh`; Modify `AGENTS.md`/`CLAUDE.md` (kullanım)
**Interfaces:** `install_git_hooks.sh` → `.git/hooks/pre-commit` yazar: `chapters/*.qmd|references/references.bib` staged ise `python3 scripts/util/tez_checklist_verify.py --fast` çalıştırır, FAIL'de commit'i durdurur.

- [ ] **Step 1: Implement** `install_git_hooks.sh` (idempotent, `--uninstall` destekli).
- [ ] **Step 2: Doğrula** `bash scripts/util/install_git_hooks.sh && test -x .git/hooks/pre-commit`
- [ ] **Step 3: Commit** (kurulum kullanıcı onayıyla; repo rule: global hook auto-install yok → yalnız kurucu script eklenir, elle çalıştırılır).

---

### Task 12: T-CERT-01 — Sertifika tazeliği kapısı

`certified-final` güvene dayalı; bölüm sertifikadan sonra değişirse sessizce eskir (denetim madde F).

**Files:** Modify `tez_checklist_verify.py`; Test
**Interfaces:** `chk_cert_freshness`: her `chapters/NN.qmd` için `sertifikalar/<bolum>-*.md` (varsa) mtime/git-hash karşılaştır; bölüm sertifikadan yeni ise closing modda FAIL, normalde MANUEL. Registry `T-CERT-01`.

- [ ] **Step 1-5:** RED (`T-CERT-01` listede) → implement → PASS → commit.

---

### Task 13: Karma cross-arm retorik tarayıcı

Karma joint-display sözlüğü yalnız 2 bölüm × 6 ledger satırıyla sınırlı; "iki kol birbirini doğrular"/cross-arm nedensellik taranmıyor (denetim madde H).

**Files:** Modify `scripts/util/karma_ledger_check.py` (prose tarama) veya yeni `chk_cross_arm_rhetoric`; Test
**Interfaces:** `chapters/05` + §2-§5 nesrinde yasak cross-arm ibareler (`doğrular|kanıtlar|ispatlar` + nitel↔nicel öznesi) regex/lexicon; bulgu → FAIL. Registry `K1-KAR-01`.

- [ ] **Step 1-5:** RED → implement → PASS → commit.

---

### Task 14: Galileo zorunlu-toplama + full-thesis judge (advisory-logged)

En derin cross-document QC (galileo overclaim/HARKing/convergence/coherence) yalnız opt-in koşuyordu (denetim madde G/breadth).

**Files:** Modify `.claude/commands/bolum-sertifika.md` (Kapı 3/4 galileo zorunlu adımı); `scripts/eval/run_full_thesis_judge.py` wiring; Modify `tez_checklist_verify.py` (advisory-logged madde)
**Interfaces:** Sertifikasyon Kapı 3/4, her içerik bölümü + her joint-display satırı için galileo `convergence/harking/overclaim/coherence_judge` çağrısını zorunlu-topla; SOFT bulgu yazılı gerekçesiz kalırsa sertifika FAIL. Checklist'e `chk_semantic_judge_logged` (advisory; atlanmış koşum görünür).

- [ ] **Step 1-5:** RED → implement → PASS → commit. **Ağ/gateway bağımlı → SKIP-dostu, HARD asla judge'dan gelmez.**

---

### Task 15: Doküman senkron + `--audit-doc` 0 yetim

Yeni ID'ler master checklist'e ve otoritelere işlenir; `--audit-doc` senkron doğrulanır.

**Files:** Modify `tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md` (yeni ID satırları + kapsama matrisi + toplam sayı); `AGENTS.md` (yeni kaideler); `CLAUDE.md` (checklist komut örnekleri)
**Interfaces:** `python3 scripts/util/tez_checklist_verify.py --audit-doc` → `SENKRON` (0 yetim).

- [ ] **Step 1: Her yeni ID (K5-NUM-03, K5-CAU-02, K5-TRK-01, R-SVG-01, K1-DOI-01, K4-TRG-01, K0-PII-03, T-CERT-01, K1-KAR-01) için** master checklist'e madde + kapsama matrisi satırı ekle; "Toplam N kontrol" sayısını güncelle.
- [ ] **Step 2: Run** `python3 scripts/util/tez_checklist_verify.py --audit-doc` → `SENKRON` bekle.
- [ ] **Step 3: Commit**

---

## Self-Review

- **Spec coverage:** Etüt P0-P3'ün her maddesi bir task'e bağlı — madde A→Task 1/9/11, B→Task 2, C→Task 6/10, D→Task 7, E→Task 1, F→Task 12, G→Task 3/14, H→Task 8/13. ✔
- **Placeholder scan:** Kod adımları gerçek imza/komut taşıyor; büyük özellikler (Task 14) SKIP-dostu somut adımlarla. ✔
- **Type consistency:** Tüm yeni `chk_*` imzası `(cid, ctx)`; registry `add(cid, eksen, katman, baslik, fn)`; `Result(cid, status, evidence)` — mevcut kayıtla birebir. ✔
- **İkiz-ağaç:** Task 9/10 her iki hook ağacına + `chk_hooks_twin` küme-eşitliğine uyar (dosya adları değişmez, yalnız içerik). ✔

## Execution Handoff

Uygulama bu oturumda **Inline Execution** ile, güvenlik-önce sırada: önce additive/manuel-checklist maddeleri (Task 2-8, workflow'u kırmaz), sonra runtime friction (Task 9 güvenli; Task 10-11 onay ile). Her task: RED → GREEN → `--audit-doc` senkron → sonraki. Commit yalnız kullanıcı istediğinde.
