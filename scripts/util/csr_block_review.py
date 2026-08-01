#!/usr/bin/env python3
"""CSR parça-bazlı uçtan-uca denetim orkestratörü.

docs/CLINICAL-STUDY-REPORT-FINAL.qmd'yi 8 mantıksal bloğa ayırır ve her bloğa
beş denetim katmanını (claim_certification · GraphRAG · Minerva · sci-audit
axis G · R-chunk mantığı) uygular. Blok başına rapor + üst-özet INDEX üretir.

KVKK: dış servislere yalnız yayımlanmış literatür + manuskript metni gider;
satır düzeyi katılımcı verisi ASLA. Ham .qmd değiştirilmez (salt-okunur girdi).
Geçici blok alt-dosyaları işlem sonunda silinir.

Kullanım:
  python3 scripts/util/csr_block_review.py            # tam çalıştırma
  python3 scripts/util/csr_block_review.py --no-judge # judge olmadan (hızlı)
  python3 scripts/util/csr_block_review.py --no-net    # dış-servissiz (offline)
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UTIL = ROOT / "scripts" / "util"
MCP = ROOT / "scripts" / "mcp"
CSR = ROOT / "docs" / "CLINICAL-STUDY-REPORT-FINAL.qmd"
TMP_DIR = ROOT / "outputs" / "tmp" / "csr-blocks"
REPORT_DIR = ROOT / "outputs" / "reports" / "csr-review"
HEALTHCHECK = MCP / "audit_stack_healthcheck.py"
CLAIM_CERT = UTIL / "claim_certification.py"
GRAPHRAG = MCP / "graphrag_query.py"
MINERVA = MCP / "minerva_evidence_bridge.py"
EVIDENTIA_HTTP = MCP / "evidentia_http_client.py"
NUMERIC_AUDIT = UTIL / "csr_numeric_trace_audit.py"
# Blok claim_cert çalışmaları default numbers CSV'sini (alt-dosya satır no'suyla)
# üzerine yazar; R-chunk ekseni ham .qmd satır no'suna ihtiyaç duyduğundan
# tam-CSR numbers CSV'si ayrı, sabit bir yola bir kez üretilir.
NUMERIC_NUMBERS_CSV = TMP_DIR / "full_numbers.csv"
SCIAUDIT = (
    Path.home()
    / ".claude/plugins/marketplaces/cureonics-marketplace/plugins/sci-audit"
    / "skills/turkish-sci-style/scripts/tr_sciaudit.py"
)
PROTO = "2025-06-18"

# 8 mantıksal blok → ham bölüm numaraları (tasarım spesifikasyonu tablosu).
# literatür = GraphRAG uygulanır; diğerlerinde "uygulanamaz/boş".
BLOCKS = [
    {"nn": "01", "slug": "on-madde-sinopsis", "name": "Ön-madde ve Sinopsis",
     "sections": [1, 2, 3, 4, 5], "literature": False,
     "queries": []},
    {"nn": "02", "slug": "giris-hipotezler", "name": "Giriş ve Hipotezler",
     "sections": [6, 7], "literature": True,
     "queries": ["tip 1 diyabet ebeveynlik tutumu psikososyal arka plan",
                 "parental attitudes chronic illness child glycemic control hypotheses"]},
    {"nn": "03", "slug": "yontem", "name": "Yöntem",
     "sections": [8], "literature": False,
     "queries": []},
    {"nn": "04", "slug": "populasyon-psikometri", "name": "Popülasyon ve Psikometri",
     "sections": [9, 10], "literature": False,
     "queries": []},
    {"nn": "05", "slug": "birincil-hipotez", "name": "Birincil Hipotez Bulguları",
     "sections": [11], "literature": False,
     "queries": []},
    {"nn": "06", "slug": "kesifsel-ikincil", "name": "Keşifsel/İkincil Analizler",
     "sections": [12, 15, 16], "literature": True,
     "queries": ["aracılık tipoloji ağ analizi çok-informant tutarsızlık",
                 "mediation latent typology network multi-informant discrepancy"]},
    {"nn": "07", "slug": "robustluk-bayes", "name": "Robustluk ve Bayes",
     "sections": [13, 14], "literature": False,
     "queries": []},
    {"nn": "08", "slug": "tartisma-sonuc-ekler", "name": "Tartışma, Sonuç ve Ekler",
     "sections": [17, 18, 19, 20, 21, 22, 23], "literature": True,
     "queries": ["ebeveyn aşırı koruma metabolik kontrol literatür konumlandırma",
                 "parenting overprotection type 1 diabetes discussion limitations"]},
]


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


# ==========================================================================
# G1 — Bölümleme (code-fence-aware başlık-çapası)
# ==========================================================================
HEAD_RE = re.compile(r"^# (\d+)\.")
CHUNK_OPEN_RE = re.compile(r"^```\{")
FENCE_RE = re.compile(r"^```")


def scan_sections(lines: list[str]) -> dict[int, tuple[int, int]]:
    """Ham bölüm no → (başlangıç satırı, bitiş satırı, 1-tabanlı, dahil).

    Code-fence içindeki `#` R yorumları başlık sayılmaz.
    """
    in_fence = False
    heads: list[tuple[int, int]] = []  # (section_no, start_line)
    for i, line in enumerate(lines, start=1):
        s = line.rstrip()
        if FENCE_RE.match(s):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEAD_RE.match(s)
        if m:
            heads.append((int(m.group(1)), i))
    out: dict[int, tuple[int, int]] = {}
    for idx, (sec, start) in enumerate(heads):
        end = (heads[idx + 1][1] - 1) if idx + 1 < len(heads) else len(lines)
        out[sec] = (start, end)
    return out


def count_r_chunks(block_lines: list[str]) -> int:
    """Bloktaki açılan R chunk (```{r ...}) sayısı."""
    n = 0
    for line in block_lines:
        if CHUNK_OPEN_RE.match(line.rstrip()):
            n += 1
    return n


def count_narrative_words(block_lines: list[str]) -> int:
    """Code-fence dışı düzyazı sözcük sayısı (kaba)."""
    in_fence = False
    words = 0
    for line in block_lines:
        s = line.rstrip()
        if FENCE_RE.match(s):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        st = s.strip()
        if not st or st.startswith("#") or st.startswith("|") or st.startswith("!"):
            continue
        words += len(st.split())
    return words


# DOI'ler parantez içerebilir (ör. Elsevier 10.1016/S0272-7358(98)00100-7);
# bu yüzden ')' hariç tutulmaz, yalnız boşluk/tırnak/açılı-parantez sınır sayılır.
# Sondaki noktalama (.,;) ve dengesiz kapanış parantezi ayrıca kırpılır.
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>]+")


def _clean_doi(raw: str) -> str:
    d = raw.rstrip(".,;")
    # dengesiz kapanış parantezini kırp (cümle sonu ") " durumu)
    while d.endswith(")") and d.count("(") < d.count(")"):
        d = d[:-1]
    return d


def extract_block_dois(block_text: str) -> list[str]:
    """Blok metnindeki benzersiz DOI'ler (referans-varlık doğrulaması için)."""
    seen: list[str] = []
    for m in DOI_RE.finditer(block_text):
        d = _clean_doi(m.group(0))
        if d and d not in seen:
            seen.append(d)
    return seen


def extract_block_citations(block_text: str) -> list[str]:
    """Blok metnindeki citeproc anahtarları (@key). CSR APA-nesir kullandığından
    çoğu blok için boş dönebilir; bib katmanı bağımsızdır."""
    cite_re = re.compile(r"(?<![A-Za-z0-9])-?@([A-Za-z0-9][\w:.#$%&+?<>~/-]*)")
    return sorted({m.group(1) for m in cite_re.finditer(block_text)})


def build_blocks() -> list[dict]:
    """CSR'yi 8 bloğa böl, geçici alt-dosyaları yaz, meta döndür.

    Not: bloklar ham bölüm no'ya göre; blok 06 (12,15,16) blok 07 (13,14) ile
    iç içe geçtiğinden alt-dosya, o bloğun bölümlerinin satır aralıklarını
    sırayla birleştirir (ham .qmd değişmez).
    """
    raw = CSR.read_text(encoding="utf-8")
    lines = raw.splitlines()
    sec_map = scan_sections(lines)

    # Dosya-başı setup/idiomatik-çizim chunk'ı (bölüm 1'den önce) — spec gereği
    # blok 04'ün R-chunk ekseninde değerlendirilir; claim/sci alt-dosyasına
    # karışmaz (ayrı dosyaya yazılır).
    first_start = min(v[0] for v in sec_map.values()) if sec_map else len(lines)
    head_setup = "\n".join(lines[: first_start - 1]) + "\n"
    all_r_ranges = r_chunk_line_ranges(lines)

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    head_file = TMP_DIR / "00-head-setup.r.md"
    head_file.write_text(head_setup, encoding="utf-8")
    blocks: list[dict] = []
    for b in BLOCKS:
        segments: list[str] = []
        line_ranges: list[tuple[int, int]] = []
        for sec in b["sections"]:
            if sec not in sec_map:
                continue
            start, end = sec_map[sec]
            segments.extend(lines[start - 1:end])
            line_ranges.append((start, end))
        block_text = "\n".join(segments) + "\n"
        subfile = TMP_DIR / ("%s-%s.md" % (b["nn"], b["slug"]))
        subfile.write_text(block_text, encoding="utf-8")

        block_lines = block_text.splitlines()
        meta = dict(b)
        meta["line_ranges"] = line_ranges
        meta["subfile"] = subfile
        meta["r_chunks"] = count_r_chunks(block_lines)
        meta["words"] = count_narrative_words(block_lines)
        meta["citations"] = extract_block_citations(block_text)
        meta["dois"] = extract_block_dois(block_text)
        # Blok 04, dosya-başı setup chunk'ını R-chunk ekseninde de değerlendirir.
        meta["head_setup_file"] = head_file if b["nn"] == "04" else None
        # Blok satır aralığına düşen R-chunk gövde aralıkları (kod-literal ayrımı).
        meta["_r_ranges"] = [
            (a, bb) for (a, bb) in all_r_ranges
            if any(rs <= a <= re for rs, re in line_ranges)]
        blocks.append(meta)
        log("[blok %s] bölüm=%s satır=%s chunk=%d sözcük=%d" % (
            b["nn"], b["sections"], line_ranges, meta["r_chunks"], meta["words"]))
    return blocks


# ==========================================================================
# Katman 1 — claim_certification (numeric + causal + bib + judge)
# ==========================================================================
def run_claim_cert(subfile: Path, with_judge: bool) -> dict:
    cmd = [sys.executable, str(CLAIM_CERT), "--csr", str(subfile), "--json"]
    if with_judge:
        cmd.append("--with-judge")
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=str(ROOT))
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "verdict": "FAIL"}
    try:
        return json.loads(p.stdout)
    except (json.JSONDecodeError, ValueError):
        return {"error": (p.stderr or p.stdout)[:300], "verdict": "FAIL"}


# ==========================================================================
# Katman 2 — GraphRAG (yalnız literatür blokları; diğeri uygulanamaz)
# ==========================================================================
def run_graphrag(block: dict, enabled: bool) -> dict:
    if not block.get("literature"):
        return {"applicable": False, "reason": "literatür-ağırlıklı olmayan blok"}
    if not enabled:
        return {"applicable": True, "skipped": True, "reason": "--no-net"}
    qs = block.get("queries", [])
    if not qs:
        return {"applicable": True, "skipped": True, "reason": "sorgu yok"}
    primary, *rest = qs
    cmd = [sys.executable, str(GRAPHRAG), primary, "--k", "5", "--json"]
    if rest:
        cmd += ["--queries", ",".join(rest)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=200, cwd=str(ROOT))
        d = json.loads(p.stdout)
    except Exception as e:  # noqa: BLE001
        return {"applicable": True, "error": str(e)[:200]}
    chunks = d.get("chunks", [])
    disagree = [c for c in chunks
                if abs(_f(c.get("score")) - _f(c.get("galileo_score"))) >= 0.3]
    return {
        "applicable": True,
        "query": primary,
        "sub_queries": rest,
        "n_chunks": len(chunks),
        "graph_edges": d.get("retrieval", {}).get("graph_edges", 0),
        "top": [{"doc": c.get("doc_id"), "title": (c.get("title") or "")[:70],
                 "anamnesis": c.get("score"), "galileo": c.get("galileo_score"),
                 "fused": c.get("fused_score")} for c in chunks[:5]],
        "disagreements": len(disagree),
    }


# ==========================================================================
# Katman 3 — Minerva çapraz-doğrulama (mode:semantic)
# ==========================================================================
def _minerva_rpc(query: str, timeout: int = 90, retries: int = 3) -> list:
    """Minerva semantic arama; transient boş/hata durumunda geri-çekilmeli tekrar."""
    import time
    for attempt in range(retries):
        res = _minerva_rpc_once(query, timeout)
        if res:
            return res
        if attempt < retries - 1:
            time.sleep(2 * (attempt + 1))
    return []


def _minerva_rpc_once(query: str, timeout: int = 90) -> list:
    env = dict(__import__("os").environ)
    env["CLAUDE_PROJECT_DIR"] = str(ROOT)
    # .env yükle (değer basılmaz)
    envf = ROOT / ".env"
    if envf.exists():
        for line in envf.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    calls = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": PROTO, "capabilities": {},
                    "clientInfo": {"name": "csr-block-review", "version": "1.0"}}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
         "params": {"name": "minerva_literature_search",
                    "arguments": {"query": query, "mode": "semantic", "limit": 3}}},
    ]
    payload = "\n".join(json.dumps(c) for c in calls) + "\n"
    try:
        p = subprocess.run([sys.executable, str(MINERVA)], input=payload,
                           capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return []
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line, strict=False)
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and d.get("id") == 2:
            c = d.get("result", {}).get("content", [])
            if c:
                try:
                    return json.loads(c[0].get("text", "{}"), strict=False).get("results", [])
                except json.JSONDecodeError:
                    return []
    return []


def run_minerva(block: dict, enabled: bool) -> dict:
    if not enabled:
        return {"skipped": True, "reason": "--no-net"}
    # blok kritik iddiasından türetilmiş sorgu: literatür sorgusu varsa onu,
    # yoksa blok adından bir İngilizce/Türkçe karma terim kullan.
    q = (block.get("queries") or [None])[0] or (
        "type 1 diabetes children %s" % block["name"])
    results = _minerva_rpc(q)
    top = _f(results[0].get("score")) if results else 0.0
    out = {
        "query": q,
        "hits": len(results),
        "top_score": round(top, 3),
        "verified": top >= 0.6,
        "top_titles": [_minerva_label(r) for r in results[:3]],
    }
    # Embedding yolu 429/boş → RoMine DOI-getirme (getSingleArticle) ile
    # blok DOI'lerini gerçek-kayıt olarak doğrula. Bu band embedding'den
    # bağımsız çalışır; DOI'li bloklarda referans-varlık kanıtı sağlar.
    dois = block.get("dois", [])
    if out["hits"] == 0 and dois:
        dv = _minerva_doi_verify(dois[:24])
        if dv is not None:
            out["romine_doi"] = dv
            # RoMine kayıt bulduysa Minerva katmanı degrade-doğrulanmış sayılır.
            if dv.get("registered", 0) > 0:
                out["verified"] = True
    return out


def _minerva_doi_verify(dois: list) -> dict | None:
    """RoMine minerva_rominedb_get_article ile DOI-varlık doğrulaması.

    Her DOI için getSingleArticle çağrısı yapar; başlık dönerse 'kayıtlı'.
    Embedding (429) yolundan bağımsız kanıt bandıdır.
    """
    if not dois:
        return None
    rows = []
    registered = notfound = 0
    for d in dois:
        art = _minerva_get_article(d)
        title = (art or {}).get("title") if isinstance(art, dict) else None
        if title:
            registered += 1
            rows.append({"doi": d, "durum": "kayıtlı", "title": str(title)[:70]})
        else:
            notfound += 1
            rows.append({"doi": d, "durum": "yok", "title": ""})
    return {
        "checked": len(dois),
        "registered": registered,
        "not_found": notfound,
        "rows": rows,
    }


def _minerva_get_article(doi: str, timeout: int = 60) -> dict | None:
    """Tek DOI için RoMine getSingleArticle; künye sözlüğü veya None döndürür."""
    env = dict(__import__("os").environ)
    env["CLAUDE_PROJECT_DIR"] = str(ROOT)
    envf = ROOT / ".env"
    if envf.exists():
        for line in envf.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    calls = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": PROTO, "capabilities": {},
                    "clientInfo": {"name": "csr-block-review", "version": "1.0"}}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
         "params": {"name": "minerva_rominedb_get_article",
                    "arguments": {"doi": doi}}},
    ]
    payload = "\n".join(json.dumps(c) for c in calls) + "\n"
    try:
        p = subprocess.run([sys.executable, str(MINERVA)], input=payload,
                           capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return None
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line, strict=False)
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and d.get("id") == 2:
            c = d.get("result", {}).get("content", [])
            if c:
                try:
                    art = json.loads(c[0].get("text", "{}"), strict=False)
                    return art if isinstance(art, dict) and art else None
                except json.JSONDecodeError:
                    return None
    return None


def _minerva_label(r: dict) -> str:
    """Sonuç kaydından okunur bir etiket çıkar (alan adı değişkenliğine dayanıklı)."""
    for k in ("title", "Title", "doi", "DOI", "article_title", "name", "source"):
        v = r.get(k)
        if v:
            return str(v)[:70]
    # metin-benzeri ilk uzun alanı snippet olarak kullan
    for k, v in r.items():
        if isinstance(v, str) and len(v) > 10 and k.lower() not in ("id", "score"):
            return v[:70]
    return "(başlıksız kayıt)"


# ==========================================================================
# Katman 3b — Full-text kanıt (OpenAthens + Anna's): referans-varlık doğrulama
#             + Minerva 429'da literatür-konumlandırma yedeği
# ==========================================================================
def _load_evidentia_client():
    """evidentia_http_client modülünü tek sefer yükle (import-by-path)."""
    import importlib.util
    if getattr(_load_evidentia_client, "_mod", None) is None:
        spec = importlib.util.spec_from_file_location(
            "evidentia_http_client", str(EVIDENTIA_HTTP))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.load_dotenv()
        _load_evidentia_client._mod = mod
    return _load_evidentia_client._mod


def _annas_doi_status(text) -> str:
    """Anna's article_search çıktısını 'kayıtlı/yok/belirsiz'e indir."""
    s = str(text)
    low = s.lower()
    if "not found" in low or "no article resolved" in low:
        return "yok"
    if re.search(r"\[10\.\d{4,9}/", s):
        return "kayıtlı"
    return "belirsiz"


def run_fulltext(block: dict, enabled: bool, minerva_failed: bool,
                 sample: int = 8) -> dict:
    """OpenAthens + Anna's ile blok DOI'lerini doğrula; gerekiyorsa Minerva
    yerine literatür-konumlandırma sağla.

    KVKK: yalnız DOI + arama terimi gönderilir; katılımcı verisi asla.
    """
    if not enabled:
        return {"skipped": True, "reason": "--no-net"}
    try:
        m = _load_evidentia_client()
    except Exception as e:  # noqa: BLE001
        return {"error": "istemci yüklenemedi: %s" % str(e)[:120]}

    out: dict = {"role": "fallback" if minerva_failed else "tamamlayıcı"}

    # --- (a) referans-varlık doğrulaması (DOI'si olan bloklar) ---
    dois = block.get("dois", [])
    if dois:
        picked = dois[:sample]
        try:
            annas = m.EvidentiaHTTPClient("annas").connect()
        except Exception as e:  # noqa: BLE001
            return {"error": "annas bağlanamadı: %s" % str(e)[:120], **out}
        try:
            oa = m.EvidentiaHTTPClient("openathens").connect()
        except Exception:  # noqa: BLE001
            oa = None
        rows = []
        registered = notfound = ambiguous = oa_ok = 0
        for d in picked:
            try:
                a = annas.call("article_search", {"query": d})
                st = _annas_doi_status(a)
            except Exception:  # noqa: BLE001
                st = "belirsiz"
            oa_status = "?"
            if oa is not None:
                try:
                    r = oa.call("oa_resolve", {"doi": d})
                    oa_status = r.get("status", "?") if isinstance(r, dict) else "?"
                    if oa_status == "ok":
                        oa_ok += 1
                except Exception:  # noqa: BLE001
                    oa_status = "hata"
            if st == "kayıtlı":
                registered += 1
            elif st == "yok":
                notfound += 1
            else:
                ambiguous += 1
            title = ""
            a_s = str(a) if 'a' in dir() else ""
            mt = re.match(r"-\s*(.+?)\s+—", a_s)
            if mt:
                title = mt.group(1)[:70]
            rows.append({"doi": d, "annas": st, "openathens": oa_status,
                         "title": title})
        out.update({
            "doi_checked": len(picked),
            "doi_total": len(dois),
            "registered": registered,
            "not_found": notfound,
            "ambiguous": ambiguous,
            "oa_resolved": oa_ok,
            "rows": rows,
        })

    # --- (b) Minerva yedeği: literatür-konumlandırma (429'da) ---
    if minerva_failed:
        # Anna's İngilizce/DOI sorgularında çok daha isabetli; varsa İngilizce
        # alt-sorguyu (queries[1]) tercih et, yoksa birincil sorguyu kullan.
        qs = block.get("queries") or []
        q = (qs[1] if len(qs) > 1 else (qs[0] if qs else None))
        if q:
            try:
                annas = m.EvidentiaHTTPClient("annas").connect()
                res = annas.call("article_search", {"query": q, "limit": 3})
                lines = [ln.strip("- ").strip()
                         for ln in str(res).split("\n") if ln.strip()][:3]
                out["fallback_search"] = {"query": q, "hits": lines}
            except Exception as e:  # noqa: BLE001
                out["fallback_search"] = {"query": q, "error": str(e)[:120]}
    return out


# ==========================================================================
# Katman 4 — sci-audit axis G (Türkçe stil)
# ==========================================================================
def run_sciaudit(subfile: Path) -> dict:
    if not SCIAUDIT.exists():
        return {"error": "tr_sciaudit.py bulunamadı"}
    try:
        p = subprocess.run(
            [sys.executable, str(SCIAUDIT), str(subfile),
             "--strictness", "certification", "--format", "json"],
            capture_output=True, text=True, timeout=120)
        d = json.loads(p.stdout)
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}
    issues = d.get("issues", [])
    codes: dict[str, int] = {}
    for it in issues:
        codes[it.get("code", "?")] = codes.get(it.get("code", "?"), 0) + 1
    return {
        "atesman": d.get("metrics", {}).get("atesman_score"),
        "atesman_label": d.get("metrics", {}).get("atesman_label"),
        "n_issues": len(issues),
        "codes": codes,
        "errors": sum(1 for i in issues if i.get("severity") == "error"),
        "warnings": sum(1 for i in issues if i.get("severity") == "warning"),
    }


# ==========================================================================
# Katman 5 — R chunk mantığı ekseni
# ==========================================================================
def analyze_r_chunks(block: dict) -> dict:
    """Bloktaki R chunk'ları envanterle: label, kaynak (R/NN port mu inline mı),
    okuduğu CSV/artefakt, fallback/guarded işareti."""
    text = block["subfile"].read_text(encoding="utf-8")
    # Blok 04: dosya-başı setup/idiomatik-çizim chunk'ını da dahil et.
    head_file = block.get("head_setup_file")
    if head_file and head_file.exists():
        text = head_file.read_text(encoding="utf-8") + "\n" + text
    lines = text.splitlines()
    chunks: list[dict] = []
    in_chunk = False
    cur: dict = {}
    body: list[str] = []
    for line in lines:
        s = line.rstrip()
        if CHUNK_OPEN_RE.match(s):
            in_chunk = True
            cur = {"label": None, "reads": set(), "port": None, "guarded": False}
            body = []
            continue
        if in_chunk and FENCE_RE.match(s):
            in_chunk = False
            blob = "\n".join(body)
            cur["reads"] = sorted(cur["reads"])
            cur["guarded"] = bool(
                re.search(r"requireNamespace|tryCatch|fallback|if\s*\(\s*file\.exists",
                          blob))
            m = re.search(r"R/(\d+[_A-Za-z0-9]*)", blob)
            cur["port"] = ("R/%s" % m.group(1)) if m else "inline"
            chunks.append(cur)
            continue
        if in_chunk:
            body.append(s)
            lm = re.match(r"#\|\s*label:\s*(\S+)", s.strip())
            if lm:
                cur["label"] = lm.group(1)
            # doğrudan dosya okumaları (read_csv/here/outputs yolu)
            for rm in re.finditer(
                    r"read[_.]?csv2?\s*\(\s*[\"']([^\"']+)[\"']|"
                    r"here\s*\(\s*[\"']([^\"']+\.csv)[\"']|"
                    r"[\"']([^\"']*outputs/[^\"']+\.(?:csv|rds))[\"']", s):
                for g in rm.groups():
                    if g:
                        cur["reads"].add(g)
            # inline tribble/veri provenance: `kaynak: <tablo/artefakt>` yorumu
            km = re.search(r"kaynak:\s*([^)\n]+)", s)
            if km:
                cur["reads"].add("kaynak:" + km.group(1).strip().rstrip(".- "))
    return {
        "n": len(chunks),
        "chunks": chunks,
        "guarded": sum(1 for c in chunks if c["guarded"]),
        "csv_reads": sorted({r for c in chunks for r in c["reads"]}),
    }


def r_chunk_line_ranges(lines: list[str]) -> list[tuple[int, int]]:
    """Ham .qmd'de R chunk (```{r}) gövdelerinin satır aralıkları (1-tabanlı)."""
    ranges: list[tuple[int, int]] = []
    in_r = False
    start = 0
    for i, line in enumerate(lines, start=1):
        s = line.rstrip()
        if not in_r and CHUNK_OPEN_RE.match(s):
            in_r = True
            start = i
        elif in_r and FENCE_RE.match(s):
            in_r = False
            ranges.append((start, i))
    return ranges


def build_full_numbers_csv() -> bool:
    """Tam CSR üzerinde numeric-trace çalıştır; numbers CSV'sini ham .qmd satır
    no'suyla sabit yola yaz (R-chunk ekseni bu satır no'ya dayanır)."""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(NUMERIC_AUDIT), "--csr", str(CSR),
           "--out-numbers", str(NUMERIC_NUMBERS_CSV),
           "--out-claims", str(TMP_DIR / "full_claims.csv"),
           "--out-report", str(TMP_DIR / "full_numeric_report.md")]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=200, cwd=str(ROOT))
        return NUMERIC_NUMBERS_CSV.exists()
    except Exception:  # noqa: BLE001
        return False


def numeric_untraced_for_block(block: dict) -> list[dict]:
    """Blok satır aralığına düşen izlenemeyen (unmatched) sayıları
    csr_numeric_trace_numbers.csv'den çek. Not: CSV satır no ham .qmd'ye göredir."""
    if not NUMERIC_NUMBERS_CSV.exists():
        return []
    import csv as _csv
    ranges = block.get("line_ranges", [])

    def in_block(ln: int) -> bool:
        return any(a <= ln <= b for a, b in ranges)

    r_ranges = block.get("_r_ranges", [])

    def in_r_chunk(ln: int) -> bool:
        return any(a <= ln <= b for a, b in r_ranges)

    out: list[dict] = []
    try:
        with NUMERIC_NUMBERS_CSV.open(encoding="utf-8") as f:
            for row in _csv.DictReader(f):
                if row.get("match_status") != "unmatched":
                    continue
                try:
                    ln = int(row.get("line", "0"))
                except ValueError:
                    continue
                if in_block(ln):
                    out.append({"line": ln, "token": row.get("token"),
                                "value": row.get("value"),
                                "in_code": in_r_chunk(ln),
                                "excerpt": (row.get("claim_excerpt") or "")[:90]})
    except OSError:
        return []
    return out


def _f(x) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


# ==========================================================================
# G4 — Ön koşul: yığın sağlığı
# ==========================================================================
def run_healthcheck() -> tuple[bool, str]:
    try:
        p = subprocess.run([sys.executable, str(HEALTHCHECK)],
                           capture_output=True, text=True, timeout=300, cwd=str(ROOT))
    except subprocess.TimeoutExpired:
        return False, "healthcheck timeout"
    return p.returncode == 0, p.stdout.strip()


def check_fulltext_band() -> tuple[bool, str]:
    """Full-text yedek bandın (OpenAthens + Anna's) canlılığını doğrula.

    Minerva 429 degrade-modunda healthcheck kapısını yalnız bu bant sağlıklıysa
    geçmeye izin veririz: kanıt hattı kesintisiz kalır.
    """
    try:
        m = _load_evidentia_client()
    except Exception as e:  # noqa: BLE001
        return False, "istemci yüklenemedi: %s" % str(e)[:120]
    lines = []
    ok = True
    for conn in ("openathens", "annas"):
        try:
            c = m.EvidentiaHTTPClient(conn).connect()
            tools = c.list_tools()
            lines.append("[PASS] %-10s — tools=%d" % (conn.upper(), len(tools)))
        except Exception as e:  # noqa: BLE001
            ok = False
            lines.append("[FAIL] %-10s — %s" % (conn.upper(), str(e)[:80]))
    return ok, "\n".join(lines)


def minerva_only_failure(hc_out: str) -> bool:
    """Healthcheck çıktısında YALNIZ Minerva'nın FAIL olup olmadığını sapta."""
    fails = [ln for ln in hc_out.splitlines() if ln.strip().startswith("[FAIL]")]
    return len(fails) == 1 and "MINERVA" in fails[0]


# ==========================================================================
# G5 — Raporlama (blok başına + INDEX)
# ==========================================================================
def block_verdict(cc: dict, sci: dict, narrative_untraced: int) -> str:
    v = cc.get("verdict", "FAIL")
    # sci-audit error'ları ve düzyazıdaki izlenemeyen sayı WARN'a yükseltir.
    if v == "PASS" and (sci.get("errors", 0) > 0 or narrative_untraced > 0):
        return "WARN"
    return v


def _narrative_untraced(untraced: list) -> int:
    return sum(1 for u in untraced if not u.get("in_code"))


def render_block_report(block: dict, cc: dict, gr: dict, mv: dict, ft: dict,
                        sci: dict, rc: dict, untraced: list) -> str:
    icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
    verdict = block_verdict(cc, sci, _narrative_untraced(untraced))
    lyr = cc.get("layers", {})
    num = lyr.get("numeric", {})
    cau = lyr.get("causal", {})
    bib = lyr.get("bib", {})
    jud = lyr.get("judge", {})

    L: list[str] = []
    L.append("# CSR İnceleme — Blok %s: %s" % (block["nn"], block["name"]))
    ranges = " · ".join("%d–%d" % (a, b) for a, b in block["line_ranges"])
    L.append("Ham bölümler: %s · Satır: %s · R chunk: %d · Anlatı sözcük: %d" % (
        ", ".join("#%d" % s for s in block["sections"]), ranges,
        block["r_chunks"], block["words"]))
    L.append("")

    # 1. Claim Sertifikasyon
    L.append("## 1. Claim Sertifikasyon (numeric + causal + bib + judge)")
    L.append("- Karar: %s %s" % (icon.get(cc.get("verdict", "FAIL"), "❓"),
                                  cc.get("verdict", "FAIL")))
    if cc.get("error"):
        L.append("- HATA: %s" % cc["error"])
    L.append("- Sayısal: iddia=%d · tam-izli=%d · kısmi=%d · izsiz=%d · high-risk kaynaksız=%d" % (
        num.get("claims", 0), num.get("traced_all", 0), num.get("partial", 0),
        num.get("untraced", 0), num.get("high_risk_unmatched", 0)))
    L.append("- Nedensel: revize=%d · gözden-geçir=%d" % (
        cau.get("causal_revise", 0), cau.get("causal_review", 0)))
    L.append("- Etiket: hata=%d · gözden-geçir=%d" % (
        cau.get("label_errors", 0), cau.get("label_reviews", 0)))
    soft = (bib.get("soft_fields", 0) + bib.get("missing_doi", 0)
            + bib.get("bad_doi", 0) + bib.get("dup_doi", 0) + bib.get("dedup", 0))
    ckeys = ", ".join(block["citations"]) if block["citations"] else "(APA-nesir; @key yok)"
    L.append("- Bib: tanımsız(HARD)=%d · SOFT=%d · blok-atıf anahtarları=%s" % (
        len(bib.get("undefined", [])), soft, ckeys))
    if jud:
        L.append("- Judge: en-kötü-halüsinasyon=%.3f · en-düşük-groundedness=%.3f (örnek=%d)" % (
            jud.get("worst_hallucination", 0.0), jud.get("min_groundedness", 1.0),
            jud.get("n", 0)))
    else:
        L.append("- Judge: (çalıştırılmadı)")
    L.append("")

    # 2. GraphRAG
    L.append("## 2. GraphRAG Literatür Konumlandırma")
    if not gr.get("applicable"):
        L.append("- **Uygulanamaz** — %s" % gr.get("reason", ""))
    elif gr.get("skipped"):
        L.append("- Atlandı — %s" % gr.get("reason", ""))
    elif gr.get("error"):
        L.append("- HATA: %s" % gr["error"])
    else:
        L.append("- Sorgu: `%s`" % gr.get("query"))
        if gr.get("sub_queries"):
            L.append("- Alt-sorgular: %s" % ", ".join(gr["sub_queries"]))
        L.append("- Getirilen chunk=%d · graf-kenar=%d · uyuşmazlık bayrağı=%d" % (
            gr.get("n_chunks", 0), gr.get("graph_edges", 0), gr.get("disagreements", 0)))
        for t in gr.get("top", []):
            L.append("  - %s (anamnesis=%s · galileo=%s · füzyon=%s) — %s" % (
                t.get("doc"), t.get("anamnesis"), t.get("galileo"),
                t.get("fused"), t.get("title")))
    L.append("")

    # 3. Minerva
    L.append("## 3. Minerva Çapraz-Doğrulama")
    if mv.get("skipped"):
        L.append("- Atlandı — %s" % mv.get("reason", ""))
    else:
        L.append("- Sorgu (mode:semantic): `%s`" % mv.get("query"))
        L.append("- İsabet=%d · en-yüksek-skor=%s · doğrulandı=%s" % (
            mv.get("hits", 0), mv.get("top_score"), "evet" if mv.get("verified") else "hayır"))
        for t in mv.get("top_titles", []):
            L.append("  - %s" % t)
        rd = mv.get("romine_doi")
        if rd:
            L.append("- RoMine DOI-getirme (embedding 429 → getSingleArticle): "
                     "%d DOI denetlendi — kayıtlı=%d · yok=%d" % (
                         rd.get("checked", 0), rd.get("registered", 0),
                         rd.get("not_found", 0)))
            miss = [r for r in rd.get("rows", []) if r["durum"] != "kayıtlı"]
            if miss:
                L.append("  - ⚠️ RoMine'da bulunamayan DOI'ler:")
                for r in miss:
                    L.append("    - `%s`" % r["doi"])
            for r in [r for r in rd.get("rows", []) if r["durum"] == "kayıtlı"][:12]:
                ttl = (" — %s" % r["title"]) if r.get("title") else ""
                L.append("  - `%s` RoMine=kayıtlı%s" % (r["doi"], ttl))
    L.append("")

    # 3b. Full-text kanıt (OpenAthens + Anna's)
    L.append("## 3b. Full-text Kanıt (OpenAthens + Anna's)")
    if ft.get("skipped"):
        L.append("- Atlandı — %s" % ft.get("reason", ""))
    elif ft.get("error"):
        L.append("- HATA: %s" % ft["error"])
    else:
        L.append("- Rol: %s%s" % (
            ft.get("role", "?"),
            " (Minerva 429 → yedek bant)" if ft.get("role") == "fallback" else ""))
        if ft.get("doi_total"):
            L.append("- Referans-varlık doğrulaması: %d/%d DOI örneklendi — "
                     "kayıtlı=%d · bulunamadı=%d · belirsiz=%d · OpenAthens-çözüldü=%d" % (
                         ft.get("doi_checked", 0), ft.get("doi_total", 0),
                         ft.get("registered", 0), ft.get("not_found", 0),
                         ft.get("ambiguous", 0), ft.get("oa_resolved", 0)))
            rows = ft.get("rows", [])
            # Önce sorunlu (yok/belirsiz) satırları göster, sonra kayıtlıları.
            problem = [r for r in rows if r["annas"] != "kayıtlı"]
            clean = [r for r in rows if r["annas"] == "kayıtlı"]
            if problem:
                L.append("  - ⚠️ Doğrulanamayan DOI'ler:")
                for r in problem:
                    ttl = (" — %s" % r["title"]) if r.get("title") else ""
                    L.append("    - `%s` annas=%s · oa=%s%s" % (
                        r["doi"], r["annas"], r["openathens"], ttl))
            for r in clean[:12]:
                ttl = (" — %s" % r["title"]) if r.get("title") else ""
                L.append("  - `%s` annas=kayıtlı · oa=%s%s" % (
                    r["doi"], r["openathens"], ttl))
            if len(clean) > 12:
                L.append("  - … (+%d kayıtlı DOI daha)" % (len(clean) - 12))
        else:
            L.append("- Bu blokta DOI yok (referans-varlık doğrulaması uygulanmadı)")
        if ft.get("fallback_search"):
            fs = ft["fallback_search"]
            L.append("- Minerva-yedek literatür araması: `%s`" % fs.get("query"))
            if fs.get("error"):
                L.append("  - HATA: %s" % fs["error"])
            for h in fs.get("hits", []):
                L.append("  - %s" % h[:90])
    L.append("")

    # 4. sci-audit axis G
    L.append("## 4. sci-audit axis G (Türkçe stil)")
    if sci.get("error"):
        L.append("- HATA: %s" % sci["error"])
    else:
        L.append("- Ateşman=%s (%s) · toplam-bulgu=%d (error=%d · warning=%d)" % (
            sci.get("atesman"), sci.get("atesman_label"), sci.get("n_issues", 0),
            sci.get("errors", 0), sci.get("warnings", 0)))
        if sci.get("codes"):
            L.append("- Kod dağılımı: %s" % ", ".join(
                "%s=%d" % (k, v) for k, v in sorted(sci["codes"].items())))
    L.append("")

    # 5. R chunk mantığı
    L.append("## 5. R Chunk Mantığı")
    L.append("- Toplam chunk=%d · guarded/fallback=%d" % (rc.get("n", 0), rc.get("guarded", 0)))
    if rc.get("csv_reads"):
        L.append("- Okunan artefaktlar: %s" % ", ".join(rc["csv_reads"]))
    for c in rc.get("chunks", []):
        reads = ", ".join(c["reads"]) if c["reads"] else "—"
        L.append("  - `%s` → %s → okunan: %s%s" % (
            c.get("label") or "(etiketsiz)", c.get("port"), reads,
            " · guarded" if c.get("guarded") else ""))
    narr = [u for u in untraced if not u.get("in_code")]
    code_lit = [u for u in untraced if u.get("in_code")]
    L.append("- İzlenemeyen anlatı-sayısı (R-chunk riski, düzyazıda)=%d" % len(narr))
    for u in narr[:15]:
        L.append("  - satır %s: `%s` (%s) — %s" % (
            u["line"], u["token"], u["value"], u["excerpt"]))
    if len(narr) > 15:
        L.append("  - … (+%d daha)" % (len(narr) - 15))
    L.append("- Kod-literal izsiz sayı (chunk gövdesi; figür koordinatı vb., düşük risk)=%d"
             % len(code_lit))
    L.append("")

    # Blok Yargısı
    L.append("## Blok Yargısı")
    L.append("- Rozet: %s **%s**" % (icon.get(verdict, "❓"), verdict))
    fixes = build_fix_list(cc, sci, untraced, gr, ft)
    if fixes:
        L.append("- Öncelikli düzeltme maddeleri:")
        for i, fx in enumerate(fixes, 1):
            L.append("  %d. %s" % (i, fx))
    else:
        L.append("- Öncelikli düzeltme: (yok — temiz)")
    L.append("")
    return "\n".join(L)


def build_fix_list(cc: dict, sci: dict, untraced: list, gr: dict,
                   ft: dict | None = None) -> list[str]:
    out: list[str] = []
    for f in cc.get("fails", []):
        out.append("[FAIL] %s" % f)
    for w in cc.get("warns", []):
        out.append("[WARN] %s" % w)
    if ft and ft.get("not_found", 0) > 0:
        out.append("[REF] Anna's'ta bulunamayan %d DOI — Crossref/PMC ile doğrula "
                   "(uydurma referans riski)" % ft["not_found"])
    narr = _narrative_untraced(untraced)
    if narr:
        out.append("[WARN] R-chunk: %d düzyazı-sayısı CSV'ye izlenemedi — kaynağı doğrula" % narr)
    if sci.get("errors", 0):
        out.append("[STİL] sci-audit %d error (Türkçe ondalık/p-değeri) düzelt" % sci["errors"])
    if gr.get("applicable") and gr.get("disagreements", 0):
        out.append("[LİT] GraphRAG %d embedding-uyuşmazlığı — insan incelemesi" % gr["disagreements"])
    return out


def render_index(blocks_data: list[dict], hc_ok: bool, hc_out: str,
                 with_judge: bool, net: bool, degraded: bool = False,
                 ft_band_out: str = "") -> str:
    icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
    L: list[str] = []
    L.append("# CSR Parça-Bazlı Denetim — Üst-Özet İndeks")
    L.append("")
    L.append("Girdi: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (salt-okunur) · "
             "8 mantıksal blok × 5 katman (claim-cert · GraphRAG · Minerva/full-text · "
             "sci-audit · R-chunk)")
    L.append("Judge: %s · Dış servis: %s%s" % (
        "açık" if with_judge else "kapalı",
        "açık" if net else "kapalı (--no-net)",
        " · **Minerva degrade → OpenAthens + Anna's full-text bandı**" if degraded else ""))
    L.append("")

    # G4 healthcheck kanıtı
    L.append("## Ön Koşul — Yığın Sağlığı (5/5 PASS gerekli)")
    if hc_ok:
        L.append("- Sonuç: ✅ TÜMÜ PASS")
    elif degraded:
        L.append("- Sonuç: ⚠️ DEGRADE-MOD — Minerva 429 (tek başarısız); "
                 "full-text yedek bant (OpenAthens + Anna's) sağlıklı olduğundan "
                 "kanıt hattı kesintisiz kabul edildi ve kapı geçildi.")
    else:
        L.append("- Sonuç: ❌ BAŞARISIZ — plan durdu")
    L.append("")
    L.append("```")
    L.append(hc_out)
    L.append("```")
    if degraded and ft_band_out:
        L.append("")
        L.append("Full-text yedek bant (Minerva alternatifi):")
        L.append("```")
        L.append(ft_band_out)
        L.append("```")
    L.append("")

    # 8×5 skor matrisi
    L.append("## 8×5 Skor Matrisi")
    L.append("")
    L.append("| Blok | Claim | GraphRAG | Minerva | Full-text | sci-audit | R-chunk | Rozet |")
    L.append("|------|-------|----------|---------|-----------|-----------|---------|-------|")
    for bd in blocks_data:
        b = bd["block"]
        cc = bd["cc"]
        gr = bd["gr"]
        mv = bd["mv"]
        ft = bd.get("ft", {})
        sci = bd["sci"]
        rc = bd["rc"]
        untraced = bd["untraced"]
        cc_cell = "%s %s" % (icon.get(cc.get("verdict", "FAIL"), "❓"), cc.get("verdict", "FAIL"))
        if not gr.get("applicable"):
            gr_cell = "n/a"
        elif gr.get("skipped"):
            gr_cell = "atlandı"
        elif gr.get("error"):
            gr_cell = "hata"
        else:
            gr_cell = "chunk=%d/uyuşmaz=%d" % (gr.get("n_chunks", 0), gr.get("disagreements", 0))
        if mv.get("skipped"):
            mv_cell = "atlandı"
        else:
            mv_cell = "%.2f%s" % (mv.get("top_score", 0.0), "✓" if mv.get("verified") else "")
        if ft.get("skipped") or ft.get("error"):
            ft_cell = "atlandı" if ft.get("skipped") else "hata"
        elif ft.get("doi_total"):
            ft_cell = "DOI %d✓/%d✗" % (ft.get("registered", 0), ft.get("not_found", 0))
            if ft.get("role") == "fallback":
                ft_cell += " (yedek)"
        elif ft.get("role") == "fallback" and ft.get("fallback_search"):
            ft_cell = "yedek-arama"
        else:
            ft_cell = "DOI yok"
        sci_cell = "e%d/w%d" % (sci.get("errors", 0), sci.get("warnings", 0))
        rc_cell = "%d chunk/%d düzyazı-izsiz" % (rc.get("n", 0), _narrative_untraced(untraced))
        L.append("| %s %s | %s | %s | %s | %s | %s | %s | %s |" % (
            b["nn"], b["name"][:20], cc_cell, gr_cell, mv_cell, ft_cell, sci_cell, rc_cell,
            icon.get(bd["verdict"], "❓") + " " + bd["verdict"]))
    L.append("")

    # toplam sayaçlar
    tot_unsourced = sum(bd["cc"].get("layers", {}).get("numeric", {}).get("high_risk_unmatched", 0)
                        for bd in blocks_data)
    tot_causal_rev = sum(bd["cc"].get("layers", {}).get("causal", {}).get("causal_revise", 0)
                         for bd in blocks_data)
    tot_label_err = sum(bd["cc"].get("layers", {}).get("causal", {}).get("label_errors", 0)
                        for bd in blocks_data)
    tot_untraced_rc = sum(_narrative_untraced(bd["untraced"]) for bd in blocks_data)
    tot_code_lit = sum(len(bd["untraced"]) - _narrative_untraced(bd["untraced"])
                       for bd in blocks_data)
    tot_bib_soft = sum(
        (bd["cc"].get("layers", {}).get("bib", {}).get("soft_fields", 0)
         + bd["cc"].get("layers", {}).get("bib", {}).get("missing_doi", 0)
         + bd["cc"].get("layers", {}).get("bib", {}).get("bad_doi", 0)
         + bd["cc"].get("layers", {}).get("bib", {}).get("dup_doi", 0)
         + bd["cc"].get("layers", {}).get("bib", {}).get("dedup", 0))
        for bd in blocks_data)
    tot_sci_err = sum(bd["sci"].get("errors", 0) for bd in blocks_data)
    L.append("## Toplam Sayaçlar (blok raporları toplamı)")
    L.append("- Kaynaksız-sayı (high-risk unmatched): **%d**" % tot_unsourced)
    L.append("- Nedensel-revize (H1-H4 doğrulayıcı): **%d**" % tot_causal_rev)
    L.append("- Keşifsel-etiket-hatası: **%d**" % tot_label_err)
    L.append("- R-chunk düzyazı-izlenemeyen sayı: **%d** (kod-literal düşük-risk: %d)" % (
        tot_untraced_rc, tot_code_lit))
    tot_doi_checked = sum(bd.get("ft", {}).get("doi_checked", 0) for bd in blocks_data)
    tot_doi_reg = sum(bd.get("ft", {}).get("registered", 0) for bd in blocks_data)
    tot_doi_nf = sum(bd.get("ft", {}).get("not_found", 0) for bd in blocks_data)
    L.append("- Full-text DOI doğrulaması: **%d** örneklendi — kayıtlı=%d · "
             "bulunamadı=%d (uydurma-referans riski)" % (
                 tot_doi_checked, tot_doi_reg, tot_doi_nf))
    L.append("- Bib SOFT sorun (blok-bağımsız bib katmanı; bloklar arası tekrarlı): **%d**"
             % tot_bib_soft)
    L.append("- sci-audit stil error: **%d**" % tot_sci_err)
    L.append("")

    # en kritik bulgular
    L.append("## En Kritik Bulgular (blok-üstü öncelik)")
    crit: list[tuple[int, str]] = []
    for bd in blocks_data:
        b = bd["block"]
        for f in bd["cc"].get("fails", []):
            crit.append((0, "Blok %s: [FAIL] %s" % (b["nn"], f)))
        nu = _narrative_untraced(bd["untraced"])
        if nu >= 5:
            crit.append((1, "Blok %s: %d düzyazı-sayısı CSV'ye izlenemedi" % (b["nn"], nu)))
        if bd["sci"].get("errors", 0) >= 3:
            crit.append((2, "Blok %s: %d sci-audit stil error" % (b["nn"], bd["sci"]["errors"])))
        if bd.get("ft", {}).get("not_found", 0) > 0:
            crit.append((0, "Blok %s: Anna's'ta bulunamayan %d DOI — uydurma-referans riski" % (
                b["nn"], bd["ft"]["not_found"])))
    crit.sort(key=lambda x: x[0])
    if crit:
        for i, (_, msg) in enumerate(crit[:10], 1):
            L.append("%d. %s" % (i, msg))
    else:
        L.append("- (kritik bulgu yok)")
    L.append("")

    L.append("## Blok Raporları")
    for bd in blocks_data:
        b = bd["block"]
        L.append("- [Blok %s — %s](%s-%s.md) · %s %s" % (
            b["nn"], b["name"], b["nn"], b["slug"],
            icon.get(bd["verdict"], "❓"), bd["verdict"]))
    L.append("")
    return "\n".join(L)


# ==========================================================================
# main
# ==========================================================================
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-judge", action="store_true", help="Galileo judge'ı atla (hızlı)")
    ap.add_argument("--no-net", action="store_true", help="dış servisleri atla (offline)")
    ap.add_argument("--keep-tmp", action="store_true", help="geçici blok dosyalarını silme")
    ap.add_argument("--minerva-degraded", action="store_true",
                    help="Minerva 429 tek-başarısızsa ve full-text bant (OpenAthens+"
                         "Anna's) sağlıklıysa kapıyı geçir; Minerva yerine full-text kullan")
    args = ap.parse_args()
    with_judge = not args.no_judge
    net = not args.no_net

    # G4 — ön koşul kapısı
    log("[1/5] Ön koşul: yığın sağlığı kontrolü…")
    hc_ok, hc_out = run_healthcheck()
    ft_band_ok = False
    ft_band_out = ""
    degraded = False
    if not hc_ok:
        # Degrade-mod: yalnız Minerva 429 ve full-text bant sağlıklıysa geçir.
        if args.minerva_degraded and minerva_only_failure(hc_out):
            log("      Minerva tek-başarısız; full-text yedek bant kontrolü…")
            ft_band_ok, ft_band_out = check_fulltext_band()
            if ft_band_ok:
                degraded = True
                log("[ok] Degrade-mod: Minerva 429 → full-text bant (OpenAthens+Anna's) "
                    "sağlıklı; kapı geçildi")
            else:
                log("[DUR] Minerva 429 VE full-text bant da sağlıksız — plan durdu.")
        if not degraded:
            log("[DUR] Healthcheck 5/5 PASS değil — plan durdu.")
            REPORT_DIR.mkdir(parents=True, exist_ok=True)
            (REPORT_DIR / "00-INDEX.md").write_text(
                "# CSR İnceleme — DURDU\n\nHealthcheck 5/5 PASS değil"
                "%s.\n\n```\n%s\n```\n%s" % (
                    " ve degrade-mod koşulu sağlanmadı" if args.minerva_degraded else "",
                    hc_out,
                    ("\n**Full-text bant:**\n```\n%s\n```\n" % ft_band_out)
                    if ft_band_out else ""),
                encoding="utf-8")
            return 1
    else:
        log("[ok] Healthcheck 5/5 PASS")

    # G1 — bölümleme
    log("[2/5] Bölümleme: 8 mantıksal blok…")
    blocks = build_blocks()
    log("      tam-CSR numeric-trace (R-chunk ekseni için)…")
    if not build_full_numbers_csv():
        log("      uyarı: tam numbers CSV üretilemedi; R-chunk izsiz-sayı boş kalır")

    # G2/G3 — blok döngüsü
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    blocks_data: list[dict] = []
    for block in blocks:
        log("[3/5] Blok %s (%s) denetim katmanları…" % (block["nn"], block["name"]))
        cc = run_claim_cert(block["subfile"], with_judge)
        gr = run_graphrag(block, net)
        mv = run_minerva(block, net)
        minerva_failed = net and not mv.get("skipped") and mv.get("hits", 0) == 0
        # Referans bloğu (08) çok sayıda DOI taşır; daha geniş örneklem al.
        ft_sample = 24 if block["nn"] == "08" else 8
        ft = run_fulltext(block, net, minerva_failed, sample=ft_sample)
        sci = run_sciaudit(block["subfile"])
        rc = analyze_r_chunks(block)
        untraced = numeric_untraced_for_block(block)
        verdict = block_verdict(cc, sci, _narrative_untraced(untraced))
        report = render_block_report(block, cc, gr, mv, ft, sci, rc, untraced)
        out = REPORT_DIR / ("%s-%s.md" % (block["nn"], block["slug"]))
        out.write_text(report, encoding="utf-8")
        log("   → %s (%s)" % (out.relative_to(ROOT), verdict))
        blocks_data.append({"block": block, "cc": cc, "gr": gr, "mv": mv,
                            "ft": ft, "sci": sci, "rc": rc, "untraced": untraced,
                            "verdict": verdict})

    # G5 — INDEX
    log("[4/5] Üst-özet INDEX…")
    idx = render_index(blocks_data, hc_ok, hc_out, with_judge, net,
                       degraded=degraded, ft_band_out=ft_band_out)
    (REPORT_DIR / "00-INDEX.md").write_text(idx, encoding="utf-8")

    # temizlik
    if not args.keep_tmp:
        log("[5/5] Temizlik: geçici blok dosyaları siliniyor…")
        shutil.rmtree(TMP_DIR, ignore_errors=True)
    else:
        log("[5/5] --keep-tmp: geçici dosyalar korundu (%s)" % TMP_DIR.relative_to(ROOT))

    log("Tamam. Raporlar: %s" % REPORT_DIR.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
