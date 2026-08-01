#!/usr/bin/env python3
"""Tam-metin erişim kaskadı — referans iddia doğrulaması için yardımcı.

YÜRÜTME sırası (yasal-öncelik). Not: bu, tam-metin-erisim-kaskadi.md'deki
BÖLÜM-sırasından (kurumsal-öncelik: §T1 OpenAthens → §T1.5 Minerva → §T2 Anna
→ §T3 OA) FARKLI bir eksendir; ikisi de Minerva'yı annas ÖNCESİNE koyar. Üç
tam-metin FETCH kaynağı (openathens/minerva) ortak `_fulltext_ok` yordamıyla
tam paritede:
  1) PubMed/EPMC   yasal açık-erişim (pubmed_fetch_fulltext)       [HTTP MCP]
  2) OpenAthens    oa_resolve + oa_fetch_fulltext (lisanslı)       [HTTP MCP]
  3) Minerva       minerva_literature_fulltext_by_doi +            [stdio MCP]
                   minerva_rominedb_get_article (Roche korpus, annas ÖNCESİ)
  4) annas-reader  article_search + read_article (son çare arama)  [HTTP MCP]

Minerva yerel stdio köprüsüdür (minerva_evidence_bridge.py; ${GRAVITEE_*} env);
diğer üç kaynak HTTP MCP'dir. Hepsi kimlik/erişim yoksa graceful `ok:False` döner
(asla çökmez). Sadece salt-okuma sorgular; token/anahtar değeri ASLA yazılmaz.
KVKK: gateway'lere yalnız DOI/başlık gider, katılımcı/ham veri gitmez.
Kullanım:
  python3 scripts/mcp/fulltext_cascade.py --doi 10.xxxx/yyyy --title "..."
"""
from __future__ import annotations
import argparse
import json
import os
import re
import select
import subprocess
import sys
import urllib.request

TIMEOUT = 40

ENDPOINTS = {
    "openathens": ("https://openathens.cureonics.com/mcp", "OPENATHENS_MCP_API_KEY"),
    "pubmed": ("https://pubmed.caseyjhand.com/mcp", None),  # açık, auth yok
    "annas": ("https://annas.cureonics.com/mcp", "ANNAS_MCP_API_KEY"),
}

# Minerva yerel stdio köprüsü (HTTP değil); test için MINERVA_BRIDGE ile override.
MINERVA_BRIDGE = os.environ.get(
    "MINERVA_BRIDGE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "minerva_evidence_bridge.py"))
_GRAVITEE_KEYS = ("GRAVITEE_VECTORSTORE_GATEWAY", "GRAVITEE_ROMINEDB_GATEWAY")


def _gravitee_present() -> bool:
    """GRAVITEE kimlik env'de VEYA repo .env'inde var mı? (Minerva ön-kontrol).

    openathens/annas'ın token-yokluğu kısa-devresiyle simetri: kimlik yoksa
    alt-süreç spawn etmeden atla. Köprü .env'den yükleyebildiğinden env + .env
    ikisi de yoklanır (değer OKUNMAZ, yalnız anahtar varlığı; sızıntı yok).
    """
    if any(os.environ.get(k) for k in _GRAVITEE_KEYS):
        return True
    repo = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        with open(os.path.join(repo, ".env"), encoding="utf-8", errors="replace") as f:
            head = f.read()
        return any((k + "=") in head for k in _GRAVITEE_KEYS)
    except OSError:
        return False


def _sse_parse(raw: str):
    for ln in raw.splitlines():
        if ln.startswith("data:"):
            try:
                return json.loads(ln[5:].strip())
            except Exception:
                continue
    try:
        return json.loads(raw)
    except Exception:
        return None


class HttpMcp:
    """Streamable-HTTP MCP oturumu (initialize + session-id + tools/call)."""

    def __init__(self, url: str, token: str = ""):
        self.url = url
        self.token = token
        self.sid = None

    def _post(self, payload: dict, want_headers=False):
        body = json.dumps(payload).encode()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            # Cloudflare error 1010 varsayılan urllib UA imzasını yasaklar;
            # tarayıcı-benzeri UA ile geçilir (OpenAthens/Annas 403 düzeltmesi).
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        if self.sid:
            headers["mcp-session-id"] = self.sid
        req = urllib.request.Request(self.url, data=body, headers=headers)
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        raw = resp.read().decode()
        if want_headers:
            return raw, resp.headers
        return raw

    def open(self):
        raw, hdrs = self._post({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "fulltext-cascade", "version": "1"}},
        }, want_headers=True)
        self.sid = hdrs.get("mcp-session-id")
        # initialized bildirimi
        try:
            self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        except Exception:
            pass
        return _sse_parse(raw)

    def call(self, name: str, arguments: dict):
        raw = self._post({
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        })
        return _sse_parse(raw)


class StdioMcp:
    """stdio MCP oturumu (initialize + tools/call), satır-sınırlı JSON-RPC.

    HTTP `HttpMcp` ile aynı yüzey (open/call/_text_of uyumlu sonuç); Minerva
    köprüsü stdio konuştuğundan HTTP yerine alt-süreç spawn edilir.
    """

    def __init__(self, script: str):
        self.script = script
        self.proc = None

    def open(self):
        self.proc = subprocess.Popen(
            [sys.executable, self.script],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, env=os.environ.copy())
        self._send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                               "clientInfo": {"name": "fulltext-cascade",
                                              "version": "1"}}})
        init = self._recv()
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return init

    def _send(self, msg: dict):
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def _recv(self):
        # Duvar-saati koruması: HTTP kademelerinin TIMEOUT'u ile parite.
        # Köprü satır üretmeden takılırsa süresiz bloklanmayı önle.
        try:
            ready, _, _ = select.select([self.proc.stdout], [], [], TIMEOUT)
        except (ValueError, OSError):
            ready = [self.proc.stdout]  # select desteklenmezse readline'a düş
        if not ready:
            return None  # zaman aşımı → çağıran ok:False sayar
        line = self.proc.stdout.readline()
        if not line.strip():
            return None
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return None

    def call(self, name: str, arguments: dict):
        self._send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                    "params": {"name": name, "arguments": arguments}})
        return self._recv()

    def close(self):
        try:
            if self.proc:
                self.proc.stdin.close()
                self.proc.terminate()
                self.proc.wait(timeout=5)
        except Exception:
            pass


def _text_of(result: dict) -> str:
    if not result or "result" not in result:
        return ""
    parts = result["result"].get("content", [])
    return "\n".join(p.get("text", "") for p in parts if isinstance(p, dict))


def try_openathens(doi: str) -> dict:
    url, env = ENDPOINTS["openathens"]
    tok = os.environ.get(env, "")
    if not tok or not doi:
        return {"tier": "openathens", "ok": False, "note": "token/doi yok"}
    try:
        m = HttpMcp(url, tok)
        m.open()
        res = m.call("oa_resolve", {"doi": doi})
        resolved = _text_of(res)
        ft = m.call("oa_fetch_fulltext", {"doi": doi})
        body = _text_of(ft)
        ok = _fulltext_ok(body)  # fetch-kademesi ortak parite yordamı
        return {"tier": "openathens", "ok": ok, "resolved": resolved[:400],
                "fulltext_len": len(body), "sample": body[:600]}
    except Exception as e:
        return {"tier": "openathens", "ok": False, "note": str(e)[:160]}


def _norm(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _parse_hits(search_body: str) -> list:
    """Europe PMC arama metnini hit-blok listesine ayır; her blokta PMID/PMCID/DOI/başlık."""
    # Her hit '#### <başlık>' ile başlar
    blocks = re.split(r"\n#### ", search_body)
    hits = []
    for b in blocks[1:]:
        title = b.splitlines()[0].strip()
        pmid = (re.search(r"\*\*PMID:\*\*\s*(\d+)", b) or
                re.search(r"EPMC ID:\*\*\s*(\d+)", b))
        pmcid = re.search(r"(PMC\d+)", b)
        doi = re.search(r"\*\*DOI:\*\*\s*(\S+)", b)
        hits.append({
            "title": title,
            "pmid": pmid.group(1) if pmid else "",
            "pmcid": pmcid.group(1) if pmcid else "",
            "doi": (doi.group(1).strip() if doi else "").lower(),
        })
    return hits


def _select_hit(hits: list, want_doi: str, want_title: str) -> dict:
    """Sorgulanan DOI/başlıkla GERÇEKTEN eşleşen hit'i seç; yoksa boş döndür.

    EPMC, DOI eşleşmesi bulamayınca alakasız fallback sonuçları döndürebilir;
    bu yüzden ilk hit'i körlemesine kabul etmek yanlış-pozitif üretir.
    """
    from difflib import SequenceMatcher
    wd = (want_doi or "").lower().strip()
    wt = _norm(want_title)
    # 1) DOI birebir eşleşmesi
    if wd:
        for h in hits:
            if h["doi"] and h["doi"] == wd:
                return {**h, "match": "doi-exact"}
    # 2) Başlık yüksek benzerlik (>=0.85)
    if wt:
        best, best_r = None, 0.0
        for h in hits:
            r = SequenceMatcher(None, wt, _norm(h["title"])).ratio()
            if r > best_r:
                best, best_r = h, r
        if best and best_r >= 0.85:
            return {**best, "match": f"title-{best_r:.2f}"}
    # eşleşme yok → EPMC alakasız sonuç döndürmüş
    return {"title": "", "pmid": "", "pmcid": "", "doi": "", "match": "none"}


def _extract_ids(search_body: str, want_doi: str = "", want_title: str = "") -> dict:
    """Arama metninden DOİ/başlık-teyitli PMID/PMCID çıkar."""
    hits = _parse_hits(search_body)
    sel = _select_hit(hits, want_doi, want_title)
    return {"pmid": sel["pmid"], "pmcid": sel["pmcid"],
            "match": sel.get("match", "none"), "n_hits": len(hits)}


def _is_error_body(body: str) -> bool:
    """MCP hata / boş-sonuç metnini tespit et (yanlış-pozitif OK'u önler)."""
    head = body[:200].lower()
    if not body:
        return True
    if "mcp error" in head or "validation error" in head or "invalid arguments" in head:
        return True
    if "hata:" in head or "beklenmeyen hata" in head:  # Minerva ToolError metni
        return True
    if "articles returned:** 0" in body.lower():
        return True
    if "no full-text articles returned" in body.lower():
        return True
    return False


def _fulltext_ok(body: str, min_len: int = 200) -> bool:
    """Tam-metin FETCH kademeleri (openathens/minerva) ortak başarı yordamı.

    Üç kaynak paritesi: hata/boş-sonuç dedektörü + asgari içerik uzunluğu aynı
    eşikten geçer. (annas bir ARAMA/son-çare kademesidir; kendi search_len
    kontrolünü kullanır, bu yordama tabi değildir.)
    """
    return bool(body) and not _is_error_body(body) and len(body) > min_len


def try_pubmed(title: str, doi: str) -> dict:
    url, _ = ENDPOINTS["pubmed"]
    try:
        m = HttpMcp(url)
        m.open()
        # Europe PMC arama (DOI veya başlık ile) — şema: query + pageSize
        srch = m.call("pubmed_europepmc_search", {"query": doi or title, "pageSize": 5})
        sbody = _text_of(srch)
        ids = _extract_ids(sbody, want_doi=doi, want_title=title)
        pmid, pmcid = ids["pmid"], ids["pmcid"]
        match = ids["match"]
        # tam metin dene — pmcids/pmids/dois kabul eder; PMC > PMID > DOI önceliği
        ft_args = {}
        if pmcid:
            ft_args["pmcids"] = [pmcid]
        elif pmid:
            ft_args["pmids"] = [pmid]
        elif doi:
            ft_args["dois"] = [doi]
        fbody = _text_of(m.call("pubmed_fetch_fulltext", ft_args)) if ft_args else ""
        # abstract/metadata — şema: pmids (required); DOI kabul edilmez
        abody = ""
        if pmid:
            abody = _text_of(m.call("pubmed_fetch_articles", {"pmids": [pmid]}))
        ft_ok = bool(fbody) and not _is_error_body(fbody) and len(fbody) > 400
        ab_ok = bool(abody) and not _is_error_body(abody) and len(abody) > 200
        return {"tier": "pubmed-epmc", "ft_ok": ft_ok, "ab_ok": ab_ok,
                "pmid": pmid, "pmcid": pmcid, "match": match,
                "search_len": len(sbody), "fulltext_len": len(fbody),
                "abstract_len": len(abody),
                "search_sample": sbody[:400],
                "abstract": abody[:1400], "fulltext_sample": fbody[:400]}
    except Exception as e:
        return {"tier": "pubmed-epmc", "ok": False, "note": str(e)[:160]}


def try_annas(title: str, doi: str) -> dict:
    url, env = ENDPOINTS["annas"]
    tok = os.environ.get(env, "")
    if not tok:
        return {"tier": "annas", "ok": False, "note": "token yok"}
    try:
        m = HttpMcp(url, tok)
        m.open()
        q = doi or title
        res = m.call("article_search", {"query": q})
        body = _text_of(res)
        ok = bool(body) and not _is_error_body(body)  # üç kaynak ortak dedektör
        return {"tier": "annas", "ok": ok, "search_len": len(body), "sample": body[:800]}
    except Exception as e:
        return {"tier": "annas", "ok": False, "note": str(e)[:160]}


def try_minerva(title: str, doi: str) -> dict:
    """Minerva (Roche korpus) stdio köprüsü — annas ÖNCESİ tam-metin kademesi.

    DOI varsa vectorstore tam metni (`minerva_literature_fulltext_by_doi`);
    boş/hatalıysa rominedb (`minerva_rominedb_get_article`) ile dener. Yalnız
    başlık varsa doğrudan rominedb başlık araması. GRAVITEE env / köprü yoksa
    graceful `ok:False` (asla çökmez). KVKK: yalnız DOI/başlık gönderilir.
    """
    if not os.path.exists(MINERVA_BRIDGE):
        return {"tier": "minerva", "ok": False, "note": "köprü bulunamadı"}
    if not _gravitee_present():
        return {"tier": "minerva", "ok": False, "note": "gravitee kimlik yok"}
    if not (doi or title):
        return {"tier": "minerva", "ok": False, "note": "doi/başlık yok"}
    m = StdioMcp(MINERVA_BRIDGE)
    try:
        m.open()
        body, source = "", ""
        if doi:
            body = _text_of(m.call("minerva_literature_fulltext_by_doi",
                                   {"doi": doi}))
            source = "vectorstore"
            if _is_error_body(body) or len(body) < 200:
                b2 = _text_of(m.call("minerva_rominedb_get_article", {"doi": doi}))
                if b2 and not _is_error_body(b2) and len(b2) > len(body):
                    body, source = b2, "rominedb"
        else:
            body = _text_of(m.call("minerva_rominedb_get_article",
                                   {"title": title}))
            source = "rominedb"
        ok = _fulltext_ok(body)  # openathens ile birebir aynı yordam
        return {"tier": "minerva", "ok": ok, "source": source,
                "fulltext_len": len(body), "sample": body[:600]}
    except Exception as e:
        return {"tier": "minerva", "ok": False, "note": str(e)[:160]}
    finally:
        m.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doi", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--tier", default="pubmed,openathens,minerva,annas",
                    help="virgülle ayrık: pubmed,openathens,minerva,annas")
    args = ap.parse_args()

    out = {"doi": args.doi, "title": args.title[:80], "tiers": []}
    for t in args.tier.split(","):
        t = t.strip()
        if t == "openathens":
            out["tiers"].append(try_openathens(args.doi))
        elif t == "pubmed":
            out["tiers"].append(try_pubmed(args.title, args.doi))
        elif t == "minerva":
            out["tiers"].append(try_minerva(args.title, args.doi))
        elif t == "annas":
            out["tiers"].append(try_annas(args.title, args.doi))
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
