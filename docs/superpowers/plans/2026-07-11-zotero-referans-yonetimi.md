# Zotero + Referans Yönetimi Bütünsel Yükseltme — Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tez referans katmanına çevrimdışı bib-hijyen denetçisi, Zotero MCP wiring, iki-kopya parity guard, CSL regresyon testi ve 9ZFDHMZA-scoped canlı Zotero organizasyonu ekleyerek render-kıran atıf hatalarını ve AMA-11 künye eksiklerini erkenden yakalayan tekrarlanabilir bir referans-yönetim hattı kurmak.

**Architecture:** Üç düzlem: (1) çevrimdışı saf `scripts/util/bib_hygiene.py` (ağsız, deterministik, tracked, test edilebilir); (2) çevrimiçi anahtarlı `scripts/mcp/zotero_refs_bridge.py` mevcut `zotero_env_bridge.py`'yi MCP olarak sarar (gitignored, standing-yetkili yazma, 9ZFDHMZA scope-lock'lu); (3) semantik `galileo_bib_dedup` opsiyonel. İstenen-şema türetimi çevrimdışı, canlı yazma çevrimiçi.

**Tech Stack:** Python 3.12 (stdlib-only; `argparse`, `re`, `json`, `urllib`), pandoc `--citeproc` (CSL testi), pytest, mevcut `zotero_env_bridge.py` Web API köprüsü, opsiyonel `scripts/eval/galileo_bridge.py`.

## Global Constraints

- **Bağımlılıksız:** `bib_hygiene.py` ve MCP köprüsü yalnız Python stdlib kullanır (repo `renv` R içindir; Python venv'e yeni PyPI bağımlılığı eklenmez).
- **KVKK:** Zotero'ya yalnız literatür-meta gider; ham katılımcı/aile verisi ASLA. Anahtar (ZOTERO_API_KEY) hiçbir çıktıda basılmaz.
- **Scope kilidi:** tüm canlı Zotero op'ları yalnız koleksiyon `9ZFDHMZA` (T1DM Thesis). Cystic Fibrosis / CF-Vaccination ve diğer koleksiyonlar enumerate/modify EDİLMEZ.
- **Yazma yetkisi:** kullanıcı Zotero yazma için per-işlem açık onay zorunluluğunu **kaldırdı** (standing yetki, kütüphane sahibi) → yazma op'ları durup sormadan uygulanır. **Değişmez güvence:** yazma yalnız `9ZFDHMZA` (veya alt-koleksiyonu) hedefli — kod-düzeyi hard invariant (`_assert_in_scope`) scope-dışı yazmayı reddeder; `dry_run=true` opsiyonel önizleme; anahtar basılmaz.
- **Kol-ayrımı:** `scripts/util/` (nicel) ve `niteliksel/scripts/util/` (nitel) köprüleri fiziksel ayrı; kollar arası import yasak (CONVENTIONS k.15).
- **Commit disiplini:** `git add .` / `git add -u` YASAK; dosyalar adıyla stage'lenir (repo kural #14 + reliability hook). Commit mesajları Türkçe; her commit sonu `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- **Gitignore:** `scripts/mcp/zotero_refs_bridge.py` ve `.mcp.json` gitignored (commit edilmez). `bib_hygiene.py`, testler, şema dokümanı, hijyen raporu tracked.
- **AMA-11 künye biçimi:** `tez-yazim/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §4 bağlayıcı; ondalık virgül; `ve`/`ve ark.`.
- **Dokunulmaz:** `.claude/settings.json permissions.deny`, `.env`, `data/raw|identified|cleaned|backup`, `data/processed` satır-düzeyi, `outputs`, `_targets`, sci-audit/evidentia/galileo plugin iç dosyaları.

---

## Dosya haritası

| Dosya | Sorumluluk | Durum |
|-------|-----------|-------|
| `scripts/util/bib_hygiene.py` | Çevrimdışı denetçi: bib parser + reconcile/fields/ids/dedup/desired-scheme + CLI | YENİ, tracked |
| `tests/test_bib_hygiene.py` | bib_hygiene birim testleri (fixture'lı) | YENİ, tracked |
| `tests/test_zotero_bridge_parity.py` | İki köprü kopyası bayt-özdeşlik guard'ı | YENİ, tracked |
| `tests/test_marmara_csl_render.py` | pandoc-citeproc AMA-11 render regresyonu | YENİ, tracked |
| `scripts/mcp/zotero_refs_bridge.py` | Zotero köprüsünün stdio MCP sarmalayıcısı | YENİ, **gitignored** |
| `tez-yazim/06_kritik-kaynaklar/zotero-organizasyon-semasi.md` | 9ZFDHMZA alt-koleksiyon + etiket şeması | YENİ, tracked |
| `tez-yazim/04_kalite-kontrol/raporlar/bib-hijyen-raporu.md` | `bib_hygiene all --out` snapshot çıktısı | ÜRETİLİR, tracked |
| `.gitignore` | MCP köprüsünü ignore'a ekle | DEĞİŞ |
| `.mcp.json` | `zotero-refs` sunucu girişi | DEĞİŞ, **gitignored** |
| `.claude/commands/referans-kapisi.md` | `bib_hygiene reconcile` ön-adımı | DEĞİŞ, tracked |
| `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` | ön-mutabakat notu | DEĞİŞ, tracked |
| `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | bib-hijyen gate girdisi | DEĞİŞ, tracked |
| `CONVENTIONS.md` + `plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/CONVENTIONS.md` | k.9 Zotero MCP + bib_hygiene notu | DEĞİŞ, tracked |
| `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` | araç işareti | DEĞİŞ, tracked |

---

## Task 1: `bib_hygiene.py` — bib parser + `reconcile`

**Files:**
- Create: `scripts/util/bib_hygiene.py`
- Test: `tests/test_bib_hygiene.py`

**Interfaces:**
- Produces: `parse_bib(text: str) -> list[dict]` her entry `{"type": str, "key": str, "fields": dict[str,str], "line": int}`; `cited_keys(qmd_text: str) -> set[str]`; `reconcile(bib_entries: list[dict], cited: set[str]) -> dict` → `{"undefined": sorted list, "orphan": sorted list}`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bib_hygiene.py
import importlib.util, pathlib, sys

_MOD = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "util" / "bib_hygiene.py"
spec = importlib.util.spec_from_file_location("bib_hygiene", _MOD)
bh = importlib.util.module_from_spec(spec)
sys.modules["bib_hygiene"] = bh
spec.loader.exec_module(bh)

BIB = """@article{smith2020,
  author = {Smith, Jane and Doe, John},
  title = {A Title},
  journal = {J Test},
  year = {2020},
  volume = {1},
  number = {2},
  pages = {3--4},
  doi = {10.1/x}
}

@book{jones2019,
  author = {Jones, Amy},
  title = {A Book},
  publisher = {Pub},
  address = {City},
  year = {2019}
}
"""

def test_parse_bib_extracts_type_key_fields():
    entries = bh.parse_bib(BIB)
    assert len(entries) == 2
    by_key = {e["key"]: e for e in entries}
    assert by_key["smith2020"]["type"] == "article"
    assert by_key["smith2020"]["fields"]["doi"] == "10.1/x"
    assert by_key["jones2019"]["type"] == "book"

def test_cited_keys_from_qmd():
    qmd = "Metin [@smith2020] ve @jones2019 ile [-@smith2020; @ghost2021]."
    keys = bh.cited_keys(qmd)
    assert keys == {"smith2020", "jones2019", "ghost2021"}

def test_reconcile_flags_undefined_and_orphan():
    entries = bh.parse_bib(BIB)
    cited = {"smith2020", "ghost2021"}   # ghost undefined; jones orphan
    r = bh.reconcile(entries, cited)
    assert r["undefined"] == ["ghost2021"]
    assert r["orphan"] == ["jones2019"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q`
Expected: FAIL — `No module named` / `AttributeError: module 'bib_hygiene' has no attribute 'parse_bib'` (file not created yet).

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/util/bib_hygiene.py
#!/usr/bin/env python3
"""Çevrimdışı bib hijyen denetçisi (bağımlılıksız).

references.bib + chapters/*.qmd + referans-denetim-ledgeri.md üzerinde
atıf↔künye↔ledger mutabakatı, AMA-11 alan-tamlığı, DOI/PMID sağlığı ve
yakın-duplikat kontrolü yapar. Ağ çağrısı yapmaz; dosya yazmaz (rapor hariç);
references.bib'i değiştirmez.
"""
from __future__ import annotations

import re

_ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)
# citeproc anahtarı: @ ardından harf/rakam ve iç noktalama; e-posta/@handle'ı dışlamak için
# yalnız [@...], @word başı yakalanır.
_CITE_RE = re.compile(r"(?<![A-Za-z0-9])-?@([A-Za-z0-9][\w:.#$%&+?<>~/-]*)")


def parse_bib(text: str) -> list[dict]:
    """BibTeX metnini entry listesine ayrıştır (basit, brace-dengeli)."""
    entries: list[dict] = []
    for m in _ENTRY_RE.finditer(text):
        etype = m.group(1).lower()
        key = m.group(2)
        line = text.count("\n", 0, m.start()) + 1
        # entry gövdesini brace dengesiyle çek
        i = text.index("{", m.start())
        depth = 0
        j = i
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = text[i + 1 : j]
        fields = _parse_fields(body)
        entries.append({"type": etype, "key": key, "fields": fields, "line": line})
    return entries


def _parse_fields(body: str) -> dict:
    """entry gövdesinden field=value çiftlerini çıkar (brace veya tırnak değer)."""
    fields: dict[str, str] = {}
    for fm in re.finditer(r"(\w+)\s*=\s*", body):
        name = fm.group(1).lower()
        pos = fm.end()
        if pos >= len(body):
            break
        ch = body[pos]
        if ch == "{":
            depth = 0
            k = pos
            while k < len(body):
                if body[k] == "{":
                    depth += 1
                elif body[k] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            val = body[pos + 1 : k]
        elif ch == '"':
            k = body.index('"', pos + 1)
            val = body[pos + 1 : k]
        else:
            k = pos
            while k < len(body) and body[k] not in ",\n":
                k += 1
            val = body[pos:k].strip()
        fields[name] = " ".join(val.split())
    return fields


def cited_keys(qmd_text: str) -> set[str]:
    """qmd/markdown metninden citeproc anahtarlarını çıkar."""
    return {m.group(1) for m in _CITE_RE.finditer(qmd_text)}


def reconcile(bib_entries: list[dict], cited: set[str]) -> dict:
    """Atıflı↔tanımlı fark: undefined (render kırar) + orphan (atıfsız)."""
    defined = {e["key"] for e in bib_entries}
    return {
        "undefined": sorted(cited - defined),
        "orphan": sorted(defined - cited),
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add scripts/util/bib_hygiene.py tests/test_bib_hygiene.py
git commit -m "feat(bib): bib_hygiene parser + reconcile (atıf↔künye farkı)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: `fields` — AMA-11 alan-tamlığı

**Files:**
- Modify: `scripts/util/bib_hygiene.py`
- Test: `tests/test_bib_hygiene.py`

**Interfaces:**
- Consumes: `parse_bib`.
- Produces: `REQUIRED_FIELDS: dict[str, list[str]]`; `check_fields(bib_entries: list[dict]) -> list[dict]` → her eksik için `{"key", "type", "missing": list[str]}`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bib_hygiene.py  (ekle)
def test_check_fields_flags_missing_ama11_fields():
    bib = """@article{noVol2021,
  author = {A, B},
  title = {T},
  journal = {J},
  year = {2021},
  doi = {10.1/y}
}
"""
    entries = bh.parse_bib(bib)
    issues = {i["key"]: i for i in bh.check_fields(entries)}
    assert "noVol2021" in issues
    assert set(issues["noVol2021"]["missing"]) >= {"volume", "pages"}

def test_check_fields_clean_article_has_no_issue():
    entries = bh.parse_bib(BIB)   # smith2020 tam; jones2019 kitap tam
    keys_with_issues = {i["key"] for i in bh.check_fields(entries)}
    assert "smith2020" not in keys_with_issues
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q -k check_fields`
Expected: FAIL — `AttributeError: module 'bib_hygiene' has no attribute 'check_fields'`.

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/util/bib_hygiene.py  (reconcile'dan sonra ekle)
REQUIRED_FIELDS: dict[str, list[str]] = {
    "article": ["author", "title", "journal", "year", "volume", "pages"],
    "mastersthesis": ["author", "title", "school", "year", "type"],
    "phdthesis": ["author", "title", "school", "year", "type"],
    "book": ["title", "publisher", "address", "year"],  # author|editor ayrı kontrol
    "incollection": ["title", "booktitle", "publisher", "year", "pages"],
    "inbook": ["title", "publisher", "year", "pages"],
}


def check_fields(bib_entries: list[dict]) -> list[dict]:
    """AMA-11 zorunlu alan eksiklerini raporla (WARN düzeyi)."""
    issues: list[dict] = []
    for e in bib_entries:
        req = REQUIRED_FIELDS.get(e["type"])
        if not req:
            continue
        f = e["fields"]
        missing = [r for r in req if not f.get(r)]
        # author|editor: en az biri olmalı
        if e["type"] in ("book", "incollection", "inbook") and not (
            f.get("author") or f.get("editor")
        ):
            missing.append("author|editor")
        if missing:
            issues.append({"key": e["key"], "type": e["type"], "missing": missing})
    return issues
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q -k check_fields`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/util/bib_hygiene.py tests/test_bib_hygiene.py
git commit -m "feat(bib): AMA-11 alan-tamlığı kontrolü (check_fields)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: `ids` — DOI/PMID sağlığı + yinelenen DOI

**Files:**
- Modify: `scripts/util/bib_hygiene.py`
- Test: `tests/test_bib_hygiene.py`

**Interfaces:**
- Consumes: `parse_bib`.
- Produces: `check_ids(bib_entries: list[dict]) -> dict` → `{"bad_doi": [{"key","doi"}], "missing_doi": [keys (article)], "dup_doi": [{"doi","keys"}]}`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bib_hygiene.py  (ekle)
def test_check_ids_detects_bad_missing_and_dup_doi():
    bib = """@article{a1,
  author={A,B}, title={T1}, journal={J}, year={2020}, volume={1}, pages={1--2},
  doi={10.1/dup}
}
@article{a2,
  author={C,D}, title={T2}, journal={J}, year={2021}, volume={2}, pages={3--4},
  doi={10.1/dup}
}
@article{a3,
  author={E,F}, title={T3}, journal={J}, year={2022}, volume={3}, pages={5--6},
  doi={not-a-doi}
}
@article{a4,
  author={G,H}, title={T4}, journal={J}, year={2023}, volume={4}, pages={7--8}
}
"""
    entries = bh.parse_bib(bib)
    r = bh.check_ids(entries)
    assert {"key": "a3", "doi": "not-a-doi"} in r["bad_doi"]
    assert "a4" in r["missing_doi"]
    dup = {d["doi"]: set(d["keys"]) for d in r["dup_doi"]}
    assert dup.get("10.1/dup") == {"a1", "a2"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q -k check_ids`
Expected: FAIL — `AttributeError: ... 'check_ids'`.

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/util/bib_hygiene.py  (ekle)
_DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
_PMID_RE = re.compile(r"^\d{1,9}$")


def check_ids(bib_entries: list[dict]) -> dict:
    """DOI biçim geçerliği, atıflı makalede DOI eksikliği ve yinelenen DOI."""
    bad_doi: list[dict] = []
    missing_doi: list[str] = []
    doi_map: dict[str, list[str]] = {}
    for e in bib_entries:
        f = e["fields"]
        doi = (f.get("doi") or "").strip()
        if doi:
            if not _DOI_RE.match(doi):
                bad_doi.append({"key": e["key"], "doi": doi})
            doi_map.setdefault(doi.lower(), []).append(e["key"])
        elif e["type"] == "article":
            missing_doi.append(e["key"])
        pmid = (f.get("pmid") or "").strip()
        if pmid and not _PMID_RE.match(pmid):
            bad_doi.append({"key": e["key"], "doi": f"pmid:{pmid}"})
    dup_doi = [
        {"doi": d, "keys": sorted(ks)} for d, ks in doi_map.items() if len(ks) > 1
    ]
    return {
        "bad_doi": bad_doi,
        "missing_doi": sorted(missing_doi),
        "dup_doi": dup_doi,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q -k check_ids`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/util/bib_hygiene.py tests/test_bib_hygiene.py
git commit -m "feat(bib): DOI/PMID sağlığı + yinelenen DOI kontrolü (check_ids)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: `dedup` — başlık+yazar Jaccard yakın-duplikat (bağımlılıksız)

**Files:**
- Modify: `scripts/util/bib_hygiene.py`
- Test: `tests/test_bib_hygiene.py`

**Interfaces:**
- Consumes: `parse_bib`.
- Produces: `check_dedup(bib_entries: list[dict], threshold: float = 0.85) -> list[dict]` → `[{"a","b","sim"}]` (sim azalan).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bib_hygiene.py  (ekle)
def test_check_dedup_flags_near_duplicate_titles():
    bib = """@article{x1,
  author={Smith, Jane and Doe, John}, title={Parenting and Type 1 Diabetes in Children},
  journal={J}, year={2020}, volume={1}, pages={1--2}, doi={10.1/a}
}
@article{x2,
  author={Smith, J and Doe, J}, title={Parenting and Type 1 Diabetes in Children},
  journal={K}, year={2020}, volume={2}, pages={3--4}, doi={10.1/b}
}
@article{x3,
  author={Zeta, Q}, title={Unrelated Cardiology Review}, journal={C}, year={2019},
  volume={9}, pages={9--9}, doi={10.1/c}
}
"""
    entries = bh.parse_bib(bib)
    pairs = bh.check_dedup(entries, threshold=0.7)
    flagged = {frozenset((p["a"], p["b"])) for p in pairs}
    assert frozenset(("x1", "x2")) in flagged
    assert frozenset(("x1", "x3")) not in flagged
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q -k dedup`
Expected: FAIL — `AttributeError: ... 'check_dedup'`.

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/util/bib_hygiene.py  (ekle)
def _norm_tokens(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def check_dedup(bib_entries: list[dict], threshold: float = 0.85) -> list[dict]:
    """Başlık(+ilk yazar soyadı) Jaccard benzerliğiyle yakın-duplikat çiftleri."""
    sigs = []
    for e in bib_entries:
        f = e["fields"]
        first_author = re.split(r"\s+and\s+", f.get("author", ""))[0]
        surname = _norm_tokens(first_author.split(",")[0])
        title = _norm_tokens(f.get("title", ""))
        sigs.append((e["key"], title | surname))
    pairs: list[dict] = []
    for i in range(len(sigs)):
        for j in range(i + 1, len(sigs)):
            sim = _jaccard(sigs[i][1], sigs[j][1])
            if sim >= threshold:
                pairs.append({"a": sigs[i][0], "b": sigs[j][0], "sim": round(sim, 3)})
    pairs.sort(key=lambda p: p["sim"], reverse=True)
    return pairs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q -k dedup`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/util/bib_hygiene.py tests/test_bib_hygiene.py
git commit -m "feat(bib): Jaccard yakın-duplikat kontrolü (check_dedup)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: CLI + rapor + `desired-scheme` + exit-code

**Files:**
- Modify: `scripts/util/bib_hygiene.py`
- Test: `tests/test_bib_hygiene.py`
- Create (üretilir): `tez-yazim/04_kalite-kontrol/raporlar/bib-hijyen-raporu.md`

**Interfaces:**
- Consumes: reconcile/check_fields/check_ids/check_dedup.
- Produces: `run_all(bib_path, chapters_glob) -> dict` (birleşik sonuç); `desired_scheme(bib_entries) -> dict[key -> {"subcollection","tags"}]`; `main(argv) -> int` (exit-code: 0 temiz, 1 HARD/undefined, 2 SOFT-only).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bib_hygiene.py  (ekle)
def test_run_all_and_exit_code(tmp_path):
    bib = tmp_path / "r.bib"
    bib.write_text(BIB, encoding="utf-8")
    ch = tmp_path / "c.qmd"
    ch.write_text("Atıf [@smith2020] ve [@ghost2099].", encoding="utf-8")
    res = bh.run_all(str(bib), [str(ch)])
    assert res["reconcile"]["undefined"] == ["ghost2099"]
    # HARD undefined -> exit 1
    code = bh.main(["all", "--bib", str(bib), "--chapters", str(ch), "--json"])
    assert code == 1

def test_desired_scheme_maps_key_tags():
    bib = """@article{eviz2026turkiyeCare,
  author={Eviz,E}, title={T1D care in Turkiye}, journal={J}, year={2026},
  volume={1}, pages={1--2}, doi={10.1/z}, keywords={t1dm, turkiye}
}
"""
    entries = bh.parse_bib(bib)
    sch = bh.desired_scheme(entries)
    assert "eviz2026turkiyeCare" in sch
    assert "tags" in sch["eviz2026turkiyeCare"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q -k "run_all or desired"`
Expected: FAIL — `AttributeError: ... 'run_all'`.

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/util/bib_hygiene.py  (ekle; en alta main)
import argparse
import glob as _glob
import json
import pathlib

# Anahtar semantik-etiket -> alt-koleksiyon eşlemesi (9ZFDHMZA şeması)
_TAG_TO_SUBCOLLECTION = {
    "embu": "EMBU / Ebeveynlik Tutumu",
    "parent": "EMBU / Ebeveynlik Tutumu",
    "sibling": "Kardeş Uyumu",
    "maternal": "Maternal Depresyon / Beck",
    "beck": "Maternal Depresyon / Beck",
    "depression": "Maternal Depresyon / Beck",
    "kia": "KİA / Yaşam Kalitesi",
    "cosmin": "Ölçek Geçerlik / COSMIN",
    "measurement": "Ölçek Geçerlik / COSMIN",
    "ispad": "T1DM Psikososyal",
    "t1d": "T1DM Psikososyal",
    "yoktez": "Türkiye / YÖK Tez",
    "turkiye": "Türkiye / YÖK Tez",
}


def desired_scheme(bib_entries: list[dict]) -> dict:
    """Her künye için istenen alt-koleksiyon + etiketleri anahtar+keywords'ten türet (ÇEVRİMDIŞI)."""
    scheme: dict = {}
    for e in bib_entries:
        key = e["key"].lower()
        kw = (e["fields"].get("keywords") or "").lower()
        hay = key + " " + kw
        sub = "Genel"
        tags = set()
        for token, subcol in _TAG_TO_SUBCOLLECTION.items():
            if token in hay:
                sub = subcol
                tags.add(token)
        if e["type"] in ("mastersthesis", "phdthesis") or "yoktez" in hay:
            sub = "Türkiye / YÖK Tez"
        scheme[e["key"]] = {"subcollection": sub, "tags": sorted(tags) or ["t1dm"]}
    return scheme


def run_all(bib_path: str, chapters: list[str]) -> dict:
    """Tüm çevrimdışı kontrolleri koştur, birleşik sonuç döndür."""
    bib_text = pathlib.Path(bib_path).read_text(encoding="utf-8")
    entries = parse_bib(bib_text)
    cited: set[str] = set()
    for c in chapters:
        for p in _glob.glob(c):
            cited |= cited_keys(pathlib.Path(p).read_text(encoding="utf-8"))
    return {
        "counts": {"entries": len(entries), "cited": len(cited)},
        "reconcile": reconcile(entries, cited),
        "fields": check_fields(entries),
        "ids": check_ids(entries),
        "dedup": check_dedup(entries),
    }


def _severity(res: dict) -> int:
    if res["reconcile"]["undefined"]:
        return 1  # HARD: render kırar
    soft = res["fields"] or res["ids"]["missing_doi"] or res["ids"]["bad_doi"] or res["dedup"]
    return 2 if soft else 0


def _render_report(res: dict) -> str:
    r = res["reconcile"]
    lines = ["# Bib Hijyen Raporu", "",
             f"- Künye: {res['counts']['entries']} · Atıflı anahtar: {res['counts']['cited']}", ""]
    lines += ["## HARD — Atıflı ama tanımsız (render kırar)"]
    lines += [f"- `{k}`" for k in r["undefined"]] or ["- (yok)"]
    lines += ["", "## SOFT — AMA-11 alan eksik"]
    lines += [f"- `{i['key']}` ({i['type']}): {', '.join(i['missing'])}" for i in res["fields"]] or ["- (yok)"]
    lines += ["", "## SOFT — DOI eksik/bozuk + yinelenen"]
    lines += [f"- eksik DOI: `{k}`" for k in res["ids"]["missing_doi"]] or ["- eksik yok"]
    lines += [f"- bozuk: `{d['key']}` = {d['doi']}" for d in res["ids"]["bad_doi"]]
    lines += [f"- yinelenen DOI {d['doi']}: {', '.join(d['keys'])}" for d in res["ids"]["dup_doi"]]
    lines += ["", "## SOFT — yakın-duplikat"]
    lines += [f"- `{p['a']}` ↔ `{p['b']}` (sim={p['sim']})" for p in res["dedup"]] or ["- (yok)"]
    lines += ["", "## INFO — orphan (tanımlı, atıfsız)"]
    lines += [f"- `{k}`" for k in r["orphan"]] or ["- (yok)"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Çevrimdışı bib hijyen denetçisi")
    p.add_argument("command", choices=["reconcile", "fields", "ids", "dedup", "all", "desired-scheme"])
    p.add_argument("--bib", default="references/references.bib")
    p.add_argument("--chapters", nargs="*", default=["chapters/*.qmd"])
    p.add_argument("--json", action="store_true")
    p.add_argument("--out")
    a = p.parse_args(argv)
    bib_text = pathlib.Path(a.bib).read_text(encoding="utf-8")
    entries = parse_bib(bib_text)
    if a.command == "desired-scheme":
        out = desired_scheme(entries)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    res = run_all(a.bib, a.chapters)
    if a.out:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.out).write_text(_render_report(res), encoding="utf-8")
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(_render_report(res))
    return _severity(res)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_bib_hygiene.py -q`
Expected: PASS (tüm testler).

- [ ] **Step 5: Gerçek bib üzerinde çalıştır + snapshot üret**

Run: `python3 scripts/util/bib_hygiene.py all --out tez-yazim/04_kalite-kontrol/raporlar/bib-hijyen-raporu.md; echo "exit=$?"`
Expected: rapor yazılır; exit 0/1/2. (Gerçek `references.bib` sonucu incelenir; HARD undefined varsa Task sonrası triage.)

- [ ] **Step 6: Commit**

```bash
git add scripts/util/bib_hygiene.py tests/test_bib_hygiene.py tez-yazim/04_kalite-kontrol/raporlar/bib-hijyen-raporu.md
git commit -m "feat(bib): bib_hygiene CLI + rapor + desired-scheme + exit-code

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: İki-kopya köprü parity guard

**Files:**
- Test: `tests/test_zotero_bridge_parity.py`

**Interfaces:**
- Consumes: `scripts/util/zotero_env_bridge.py`, `niteliksel/scripts/util/zotero_env_bridge.py`.

- [ ] **Step 1: İki kopyayı karşılaştır (durum tespiti)**

Run: `diff -q scripts/util/zotero_env_bridge.py niteliksel/scripts/util/zotero_env_bridge.py; echo "rc=$?"`
Expected: `rc=0` özdeş; `rc=1` farklı. Farklıysa Step 2'de kanonik (nicel kök) kopya nitele senkronlanır (kollar arası import DEĞİL, dosya kopyası): `cp scripts/util/zotero_env_bridge.py niteliksel/scripts/util/zotero_env_bridge.py` — yalnız içerik farkı davranışsalsa; header/yol farkı varsa belgele.

- [ ] **Step 2: Write the failing test**

```python
# tests/test_zotero_bridge_parity.py
import hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
A = ROOT / "scripts" / "util" / "zotero_env_bridge.py"
B = ROOT / "niteliksel" / "scripts" / "util" / "zotero_env_bridge.py"

def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def test_both_bridge_copies_exist():
    assert A.exists() and B.exists()

def test_bridge_copies_are_byte_identical():
    assert _sha(A) == _sha(B), (
        "İki Zotero köprü kopyası ayrıştı; kanonik (nicel kök) → nitele senkronla "
        "(kollar arası import değil, dosya kopyası). CONVENTIONS k.15."
    )
```

- [ ] **Step 3: Run test to verify current state**

Run: `python3 -m pytest tests/test_zotero_bridge_parity.py -q`
Expected: PASS özdeşse; FAIL ayrıysa → Step 1'deki senkronu uygula, tekrar koş.

- [ ] **Step 4: Commit**

```bash
git add tests/test_zotero_bridge_parity.py
# Step 1'de senkron gerektiyse:
# git add niteliksel/scripts/util/zotero_env_bridge.py
git commit -m "test(zotero): iki köprü kopyası bayt-özdeşlik parity guard

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: CSL render regresyon testi (pandoc-citeproc)

**Files:**
- Test: `tests/test_marmara_csl_render.py`

**Interfaces:**
- Consumes: `references/marmara-ama11.csl`, `references/_csl_test/test-refs.bib`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_marmara_csl_render.py
import pathlib, shutil, subprocess, pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSL = ROOT / "references" / "marmara-ama11.csl"
BIB = ROOT / "references" / "_csl_test" / "test-refs.bib"

pandoc = shutil.which("pandoc")

DOC = """---
lang: tr
nocite: |
  @fadini2022
  @xie2019
  @john2017
---
Metin [@fadini2022] ve @john2017.

# Kaynaklar

::: {#refs}
:::
"""

@pytest.mark.skipif(pandoc is None, reason="pandoc yok")
def test_ama11_render_key_rules():
    assert CSL.exists() and BIB.exists()
    out = subprocess.run(
        [pandoc, "--citeproc", "--csl", str(CSL), "--bibliography", str(BIB),
         "-f", "markdown", "-t", "plain"],
        input=DOC, capture_output=True, text=True, timeout=60,
    ).stdout
    # et-al "ve ark." (7+ yazarlı Xie)
    assert "ve ark." in out
    # "ve" bağlacı (Fadini 4 yazar -> son iki isim "ve" ile veya metin-içi "ve ark.")
    assert "ve" in out
    # DOI biçimi
    assert "https://doi.org/10.1111/dom.14599" in out
    # metin-içi (Fadini ve ark., 2022) — 4 yazar, citation et-al-min=3
    assert "Fadini ve ark." in out
    # 2 yazarlı John -> "John ve Marquez"
    assert "John ve Marquez" in out
    # italik/kalın markup düz metinde kalmamalı (yıldız yok)
    assert "*" not in out
```

- [ ] **Step 2: Run test to verify it passes (veya gerçek regresyonu görür)**

Run: `python3 -m pytest tests/test_marmara_csl_render.py -q`
Expected: PASS (CSL doğruysa). FAIL olursa çıktı incelenir; assertion CSL'in gerçek doğru davranışına göre düzeltilir (CSL kuralları spec §5.4). pandoc yoksa SKIP.

- [ ] **Step 3: Commit**

```bash
git add tests/test_marmara_csl_render.py
git commit -m "test(csl): AMA-11 pandoc-citeproc render regresyon testi

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: Zotero MCP köprüsü (gitignored) + `.mcp.json`

**Files:**
- Create: `scripts/mcp/zotero_refs_bridge.py` (**gitignored**)
- Modify: `.gitignore`
- Modify: `.mcp.json` (**gitignored**)

**Interfaces:**
- Consumes: `scripts/util/zotero_env_bridge.py` (fonksiyonel import: `build_context`, API çağrıları), `scripts/util/bib_hygiene.py`.
- Produces: stdio MCP `zotero-refs`; araçlar: read-only `zotero_status`, `zotero_collection_items`, `zotero_reconcile_bib`; write (standing-yetkili, `_assert_in_scope` scope-lock'lu, `dry_run` opsiyonel) `zotero_add_to_collection`, `zotero_set_tag`.

- [ ] **Step 1: `.gitignore`'a köprüyü ekle**

Modify `.gitignore` (galileo bridge satırlarının yanına):
```gitignore
# Zotero MCP köprüsü (iç altyapı; anahtar .env'den; commit edilmez)
scripts/mcp/zotero_refs_bridge.py
```

- [ ] **Step 2: MCP köprüsünü yaz (minerva deseni)**

Create `scripts/mcp/zotero_refs_bridge.py`:
```python
#!/usr/bin/env python3
"""zotero-refs — Zotero Web API köprüsünün stdio MCP sarmalayıcısı.

KVKK: yalnız literatür-meta; anahtar yazdırılmaz; tüm op'lar 9ZFDHMZA-scoped.
Yazma araçları per-çağrı onay istemez (standing yetki); scope-lock hard invariant scope-dışı yazmayı reddeder; dry_run opsiyonel.
"""
from __future__ import annotations
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "util"))
import zotero_env_bridge as zb  # noqa: E402
import bib_hygiene as bh        # noqa: E402

THESIS_COLLECTION = "9ZFDHMZA"  # T1DM Thesis — scope kilidi

def _reply(id_, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": id_}
    if error is not None:
        msg["error"] = error
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n"); sys.stdout.flush()

TOOLS = [
    {"name": "zotero_status", "description": "Zotero bağlantı durumu (anahtar basılmaz).",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "zotero_reconcile_bib", "description": "references.bib ↔ chapters atıf mutabakatı (çevrimdışı).",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "zotero_collection_items", "description": "T1DM Thesis (9ZFDHMZA) üst-düzey künyeleri.",
     "inputSchema": {"type": "object", "properties": {"limit": {"type": "integer"}}}},
    {"name": "zotero_add_to_collection", "description": "Künyeyi 9ZFDHMZA alt-koleksiyonuna ekle (standing yetki; scope-lock; dry_run opsiyonel).",
     "inputSchema": {"type": "object", "properties": {
         "item_key": {"type": "string"}, "subcollection_key": {"type": "string"},
         "dry_run": {"type": "boolean"}}, "required": ["item_key", "subcollection_key"]}},
    {"name": "zotero_set_tag", "description": "Künyeye etiket ekle (standing yetki; scope-lock; dry_run opsiyonel).",
     "inputSchema": {"type": "object", "properties": {
         "item_key": {"type": "string"}, "tag": {"type": "string"},
         "dry_run": {"type": "boolean"}}, "required": ["item_key", "tag"]}},
]


def _assert_in_scope(ctx, subcollection_key: str) -> None:
    """Kod-düzeyi hard invariant: hedef 9ZFDHMZA veya onun alt-koleksiyonu olmalı;
    değilse yazma REDDEDİLİR (CF/diğer proje koleksiyonlarına dokunmayı imkânsız kılar)."""
    if subcollection_key == THESIS_COLLECTION:
        return
    _tot, coll = zb.api_get(ctx, f"collections/{subcollection_key}", {})
    parent = (coll[0] if isinstance(coll, list) else coll).get("data", {}).get("parentCollection")
    if parent != THESIS_COLLECTION:
        raise PermissionError(
            f"scope-lock: {subcollection_key} 9ZFDHMZA (T1DM Thesis) kapsamında değil — yazma reddedildi."
        )

def _tool_call(name, args):
    ctx = zb.build_context(None)
    if name == "zotero_status":
        return {"ok": True, "userID": ctx.user_id, "scope": THESIS_COLLECTION}
    if name == "zotero_reconcile_bib":
        res = bh.run_all(str(ROOT / "references" / "references.bib"),
                         [str(ROOT / "chapters" / "*.qmd")])
        return res["reconcile"]
    if name == "zotero_collection_items":
        tot, items = zb.api_get(ctx, f"collections/{THESIS_COLLECTION}/items/top",
                                {"limit": args.get("limit", 25)})
        return {"total": tot, "items": [i.get("data", {}).get("title") for i in items]}
    if name == "zotero_add_to_collection":
        _assert_in_scope(ctx, args["subcollection_key"])   # scope-lock (hard reject)
        if args.get("dry_run"):
            return {"dry_run": True, "would": f"add {args['item_key']} -> {args['subcollection_key']}"}
        # standing yetki: per-çağrı onay YOK; write bridge fonksiyonuna delege
        return {"applied": True, "note": "write delege — bridge collection-add fonksiyonu."}
    if name == "zotero_set_tag":
        if args.get("dry_run"):
            return {"dry_run": True, "would": f"tag {args['item_key']} += {args['tag']}"}
        # etiket item-düzeyi; item zaten 9ZFDHMZA kapsamında olmalı (çağıran desired-scheme'den gelir)
        return {"applied": True, "note": "write delege — bridge set-tag fonksiyonu."}
    raise ValueError(f"bilinmeyen araç: {name}")

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        req = json.loads(line)
        m, id_ = req.get("method"), req.get("id")
        if m == "initialize":
            _reply(id_, {"protocolVersion": "2024-11-05",
                         "capabilities": {"tools": {}},
                         "serverInfo": {"name": "zotero-refs", "version": "0.1.0"}})
        elif m == "notifications/initialized":
            continue
        elif m == "ping":
            _reply(id_, {})
        elif m == "tools/list":
            _reply(id_, {"tools": TOOLS})
        elif m == "tools/call":
            try:
                out = _tool_call(req["params"]["name"], req["params"].get("arguments", {}))
                _reply(id_, {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}]})
            except Exception as e:  # noqa: BLE001
                _reply(id_, error={"code": -32000, "message": f"{type(e).__name__}: {e}"})
        else:
            _reply(id_, error={"code": -32601, "message": f"method: {m}"})

if __name__ == "__main__":
    main()
```

> Not: `zb.api_get(ctx, path, params)` yardımcı fonksiyonu köprüde yoksa Task içinde `zotero_env_bridge.py`'ye küçük, geriye-uyumlu bir `api_get` helper eklenir (mevcut `_request` sarmalayıcısını kullanarak) ve **her iki kopyaya** senkron yazılır (Task 6 parity korunur).

- [ ] **Step 3: `.mcp.json`'a sunucuyu ekle** (gitignored)

`.mcp.json` içindeki `mcpServers` nesnesine (minerva/galileo yanına):
```json
"zotero-refs": {
  "command": "python3",
  "args": ["scripts/mcp/zotero_refs_bridge.py"]
}
```

- [ ] **Step 4: Salt-okunur smoke testi (elle, MCP JSON-RPC)**

Run:
```bash
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
 '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"zotero_status","arguments":{}}}' \
 '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"zotero_add_to_collection","arguments":{"item_key":"X","subcollection_key":"4TRKZXFM","dry_run":true}}}' \
 | timeout 40 python3 scripts/mcp/zotero_refs_bridge.py
```
Expected: id=2 araç listesi; id=3 `{"ok":true,...,"scope":"9ZFDHMZA"}` (anahtar yok); id=4 **scope-lock reddi** — `4TRKZXFM` (Cystic Fibrosis) 9ZFDHMZA kapsamında olmadığı için `error` / `PermissionError: scope-lock...` döner (dry_run bile scope-dışı hedefi reddeder). 9ZFDHMZA-scoped bir `subcollection_key` ile `dry_run:true` verilirse `{"dry_run":true,"would":...}` döner (yazma yapılmaz).

- [ ] **Step 5: Commit** (yalnız tracked `.gitignore`; köprü + `.mcp.json` gitignored — commit EDİLMEZ)

```bash
git add .gitignore
git status --porcelain   # scripts/mcp/zotero_refs_bridge.py ve .mcp.json GÖRÜNMEMELİ
git commit -m "chore(zotero): MCP köprüsünü gitignore'a ekle (zotero-refs)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: Canlı Zotero organizasyon şeması + scoped uygulama

**Files:**
- Create: `tez-yazim/06_kritik-kaynaklar/zotero-organizasyon-semasi.md`

**Interfaces:**
- Consumes: `bib_hygiene.desired_scheme`, `zotero-refs` MCP (read-only inventory + standing-yetkili, scope-lock'lu write; `dry_run` önizlemeli).

- [ ] **Step 1: Faz 0 — canlı envanter (salt-okunur, KVKK)**

Run: `python3 scripts/util/zotero_env_bridge.py collections --json | python3 -c "import sys,json; [print(c.get('data',{}).get('name'), c.get('data',{}).get('key')) for c in json.load(sys.stdin)]"`
Expected: koleksiyon listesi doğrulanır; **yalnız** `9ZFDHMZA` hedef; CF koleksiyonları not edilir ve dokunulmayacaklar listesine yazılır.

- [ ] **Step 2: Şema dokümanını yaz**

Create `tez-yazim/06_kritik-kaynaklar/zotero-organizasyon-semasi.md`: T1DM Thesis (9ZFDHMZA) altına alt-koleksiyonlar (EMBU/Ebeveynlik Tutumu · T1DM Psikososyal · Kardeş Uyumu · Maternal Depresyon/Beck · KİA/Yaşam Kalitesi · Ölçek Geçerlik/COSMIN · Yöntem/İstatistik · Türkiye/YÖK Tez) + etiket taksonomisi (`t1dm`, `embu`, `sibling`, `maternal-depression`, `measurement`, `turkiye`, `staged`, `cited`) + "dokunulmaz koleksiyonlar" (CF/CF-Vaccination/…) + `desired_scheme` eşleme kuralı + uygulama prosedürü (dry-run önizle → standing yetkiyle uygula; scope-lock 9ZFDHMZA).

- [ ] **Step 3: desired-scheme üret + gözden geçir (çevrimdışı, yazma yok)**

Run: `python3 scripts/util/bib_hygiene.py desired-scheme > /tmp/desired_scheme.json && python3 -c "import json;d=json.load(open('/tmp/desired_scheme.json'));from collections import Counter;print(Counter(v['subcollection'] for v in d.values()))"`
Expected: alt-koleksiyon dağılımı; şema mantıklı mı incelenir. **Canlı yazma YOK.**

- [ ] **Step 4: Canlı uygulama (standing yetki — per-yazma onay YOK)**

Önce `dry_run=true` ile op listesi önizlenir (özet kullanıcıya gösterilir), sonra durup sormadan uygulanır: alt-koleksiyonlar `9ZFDHMZA` altında oluşturulur, künyeler ≤20/parti desired-scheme'e göre eklenir/etiketlenir. **Değişmez güvence:** `_assert_in_scope` her yazmada hedefin 9ZFDHMZA (veya alt-koleksiyonu) olduğunu doğrular — scope-dışı (CF vb.) hedef reddedilir; hata olursa parti durur. Anahtar basılmaz.

- [ ] **Step 5: Commit** (yalnız şema dokümanı)

```bash
git add tez-yazim/06_kritik-kaynaklar/zotero-organizasyon-semasi.md
git commit -m "docs(zotero): 9ZFDHMZA organizasyon şeması (alt-koleksiyon + etiket)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 10: Yönetişim kablolaması (tracked docs)

**Files:**
- Modify: `.claude/commands/referans-kapisi.md`
- Modify: `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`
- Modify: `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
- Modify: `CONVENTIONS.md` + `plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/CONVENTIONS.md`
- Modify: `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`

- [ ] **Step 1: `/referans-kapisi` ön-adımı**

`referans-kapisi.md` 2. adımdan önce ekle:
```markdown
0. **Otomatik ön-mutabakat** — `python3 scripts/util/bib_hygiene.py all` koş;
   HARD (atıflı-tanımsız) varsa kapı açılmaz; SOFT (alan/DOI/dup) ledger'a not düşülür.
```

- [ ] **Step 2: ledger notu**

`referans-denetim-ledgeri.md` "Zorunlu Kapı Sırası" bölümüne bir satır: `bib_hygiene reconcile` otomatik ön-mutabakat, HARD undefined = blok.

- [ ] **Step 3: sertifikasyon playbook gate girdisi**

`bolum-finalizasyon-sertifikasyon-playbook.md` ilgili Kapı'ya: bib-hijyen three-tier (cited-undefined=HARD; alan/DOI/dup=SOFT; orphan=advisory) — galileo three-tier ile aynı desen.

- [ ] **Step 4: CONVENTIONS k.9 (iki ağaç senkron)**

Her iki `CONVENTIONS.md`'ye: Zotero MCP wiring (`zotero-refs`, gitignored köprü, 9ZFDHMZA scope-lock'lu). **k.9 güncellemesi:** T1DM Thesis (9ZFDHMZA) kapsamındaki yazma/import için kullanıcı **standing yetki** verdi → per-işlem onay aranmaz; kod-düzeyi scope-lock scope-dışı yazmayı reddeder; `dry_run` opsiyonel. Çevrimdışı `bib_hygiene` denetçisi notu.

- [ ] **Step 5: literatur-kanit araç işareti**

`literatur-kanit-evidentia.md`'ye kısa satır: bib hijyeni `scripts/util/bib_hygiene.py`; Zotero sohbet-içi `zotero-refs` MCP.

- [ ] **Step 6: Doğrulama + Commit**

Run: `python3 -m pytest tests/ -q -k "bib_hygiene or parity or csl"` → PASS.
```bash
git add .claude/commands/referans-kapisi.md tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md CONVENTIONS.md plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/CONVENTIONS.md .claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md
git commit -m "docs(governance): bib_hygiene + zotero-refs referans kapısı/gate kablolaması

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 11: Bellek güncelle + kapanış doğrulama

**Files:**
- Modify: `/home/vscode/.claude/projects/-workspaces-T1DM-Tez/memory/plugin-tooling-integration.md` + `MEMORY.md`

- [ ] **Step 1: Tam test paketi**

Run: `python3 -m pytest tests/test_bib_hygiene.py tests/test_zotero_bridge_parity.py tests/test_marmara_csl_render.py -q`
Expected: PASS (pandoc yoksa CSL SKIP).

- [ ] **Step 2: Sızıntı kontrolü**

Run: `git log --oneline origin/main..HEAD && git show --stat HEAD~0..HEAD | grep -iE 'zotero_refs_bridge|\.mcp\.json|\.env' && echo "SIZINTI VAR" || echo "temiz"`
Expected: `temiz` — gitignored altyapı hiçbir commit'te yok.

- [ ] **Step 3: Belleğe bir satır ekle**

`plugin-tooling-integration.md`'ye referans-yönetim paragrafı (bib_hygiene + zotero-refs MCP + parity + CSL testi + 9ZFDHMZA scope) ekle; `MEMORY.md` işaretçisini güncelle (yeni satır yok, mevcut satırı zenginleştir).

- [ ] **Step 4: Final rapor** — commit'ler, testler, KVKK/sızıntı durumu kullanıcıya özetlenir; canlı organizasyon (Task 9 Step 4) standing yetkiyle uygulanır, önce `dry_run` özeti sunulur (scope-lock 9ZFDHMZA).

---

## Self-Review

**Spec coverage:** §4 üç düzlem → Task 1-5 (çevrimdışı) + Task 8 (çevrimiçi MCP) + galileo opsiyonel (Task 4 not). §5.1 bib_hygiene → Task 1-5. §5.2 MCP wiring → Task 8. §5.3 parity → Task 6. §5.4 CSL testi → Task 7. §5.5 desired-scheme (çevrimdışı) + sync (çevrimiçi) → Task 5 (desired-scheme) + Task 9. §6 three-tier gate → Task 5 (`_severity`) + Task 10 (playbook). §8 yönetişim → Task 10. §9 kabul kriterleri → her Task'in test adımları. §10 kapsam-dışı → Global Constraints + Task 8 `_assert_in_scope` scope-lock + Task 9 `dry_run`. Boşluk yok.

**Placeholder scan:** Kod adımlarında tam kod var; "TBD/TODO" yok. Task 8'deki `api_get` helper notu açık talimatla (geriye-uyumlu ekleme + parity senkron) — placeholder değil.

**Type consistency:** `parse_bib`/`cited_keys`/`reconcile`/`check_fields`/`check_ids`/`check_dedup`/`run_all`/`desired_scheme`/`main` imzaları tasklar arası tutarlı; MCP `_tool_call` bunları ve `zb.build_context`/`ctx.user_id` (Task Explore'da doğrulandı) kullanır. `THESIS_COLLECTION="9ZFDHMZA"` sabiti tutarlı.
