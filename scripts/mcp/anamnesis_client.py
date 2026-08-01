#!/usr/bin/env python3
"""anamnesis GraphRAG istemcisi — bağımlılıksız, stdlib-only.

anamnesis-mcp (https://anamnesis-mcp.cureonics.workers.dev/mcp) Streamable-HTTP
MCP server'ıdır: initialize → `mcp-session-id` başlığı → sonraki her çağrı bu
session ile. Yanıtlar SSE (`event: message` / `data: {...}`) çerçevesindedir.

Bu modül o protokolü tek sınıfta kapsüller ve GraphRAG substratının sekiz
aracını Python fonksiyonu olarak sunar:

  ingest_document   semantic-chunk + embed (bge-m3) + Vectorize/D1'e yaz
  semantic_search   HYBRID + MULTI-QUERY chunk retrieval
  hybrid_query      FLAGSHIP: chunk retrieval ∪ graph genişletme (provenance)
  upsert_triples    D1 bilgi grafiğine varlık-ilişki üçlüleri yaz
  graph_neighbors   Local GraphRAG: bir varlıktan n-hop komşuluk
  subgraph          verilen varlık kümesinin indüklenmiş alt-grafiği
  corpus_stats      indeks gözlemlenebilirliği (docs/chunks/nodes/edges)
  forget_document   doc_id ile sert-silme (teardown)

Embedding notu: anamnesis embedding'i worker-internal yapar (bge-m3 multilingual
+ bge-reranker cross-encoder, RRF füzyon). Dışarıdan vektör kabul etmez; bu
yüzden Galileo embedding retrieval'a ENJEKTE EDİLEMEZ — tamamlayıcı
ikinci-görüş re-rank/doğrulama için graphrag_query.py'de ayrıca kullanılır.

KVKK: anamnesis'e YALNIZ yayımlanmış literatür tam-metni + tez manüskript
paragrafları gider; ham katılımcı/aile-düzeyi/transkript/kimlikleyici ASLA.

Kimlik: ANAMNESIS_MCP_API_KEY (Bearer). Değer asla loglanmaz.
"""
from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ANAMNESIS_URL = "https://anamnesis-mcp.cureonics.workers.dev/mcp"
PROTO = "2024-11-05"
HTTP_TIMEOUT = 90
_ROOT = Path(__file__).resolve().parents[2]

_CTX = ssl.create_default_context()
_cab = os.environ.get("CURL_CA_BUNDLE") or os.environ.get("SSL_CERT_FILE")
if _cab and os.path.exists(_cab):
    try:
        _CTX.load_verify_locations(_cab)
    except Exception:  # noqa: BLE001
        pass


def load_dotenv() -> None:
    """os.environ'da yoksa repo kökü .env'i yükle (değer basılmaz).

    Interaktif-olmayan çağrılarda .bashrc auto-load devreye girmez; runner'lar
    bu fonksiyonu başta çağırmalıdır.
    """
    envf = _ROOT / ".env"
    if not envf.exists():
        return
    for line in envf.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class AnamnesisError(Exception):
    """anamnesis araç-yürütme veya taşıma hatası."""


def _parse_sse(body: str) -> dict:
    """SSE gövdesinden ilk JSON-RPC nesnesini ayrıştır."""
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            line = line[5:].strip()
        if line.startswith("{"):
            try:
                return json.loads(line, strict=False)
            except json.JSONDecodeError:
                continue
    raise AnamnesisError("SSE yanıtı ayrıştırılamadı: %s" % body[:200])


class AnamnesisClient:
    """anamnesis Streamable-HTTP MCP oturumu."""

    def __init__(self, api_key: str | None = None, retries: int = 3):
        self.api_key = api_key or os.environ.get("ANAMNESIS_MCP_API_KEY", "")
        if not self.api_key:
            raise AnamnesisError(
                "ANAMNESIS_MCP_API_KEY yok — load_dotenv() çağrıldı mı?"
            )
        self.retries = retries
        self.session_id: str | None = None
        self._rpc_id = 0

    # -- düşük seviye taşıma --------------------------------------------------
    def _headers(self) -> dict:
        h = {
            "Authorization": "Bearer %s" % self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            # Cloudflare (error 1010) urllib default UA'sını bloklar; açık UA gerekir.
            "User-Agent": "t1dm-graphrag/1.0 (+anamnesis-client)",
        }
        if self.session_id:
            h["mcp-session-id"] = self.session_id
        return h

    def _post(self, payload: dict, capture_session: bool = False) -> dict:
        data = json.dumps(payload).encode("utf-8")
        last_exc: Exception | None = None
        for attempt in range(self.retries):
            try:
                req = urllib.request.Request(
                    ANAMNESIS_URL, data=data, headers=self._headers(), method="POST"
                )
                with urllib.request.urlopen(
                    req, timeout=HTTP_TIMEOUT, context=_CTX
                ) as resp:
                    if capture_session:
                        sid = resp.headers.get("mcp-session-id")
                        if sid:
                            self.session_id = sid.strip()
                    body = resp.read().decode("utf-8", "replace")
                return _parse_sse(body)
            except urllib.error.HTTPError as e:  # noqa: PERF203
                last_exc = e
                if e.code in (429, 500, 502, 503, 504) and attempt < self.retries - 1:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                detail = ""
                try:
                    detail = e.read().decode("utf-8", "replace")[:200]
                except Exception:  # noqa: BLE001
                    pass
                raise AnamnesisError("HTTP %s: %s" % (e.code, detail)) from e
            except (urllib.error.URLError, TimeoutError) as e:
                last_exc = e
                if attempt < self.retries - 1:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise AnamnesisError("ağ hatası: %s" % e) from e
        raise AnamnesisError("beklenmeyen: %s" % last_exc)

    def _next_id(self) -> int:
        self._rpc_id += 1
        return self._rpc_id

    def connect(self) -> "AnamnesisClient":
        """initialize + session yakalama."""
        resp = self._post(
            {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTO,
                    "capabilities": {},
                    "clientInfo": {"name": "t1dm-graphrag", "version": "1.0"},
                },
            },
            capture_session=True,
        )
        if "error" in resp:
            raise AnamnesisError("initialize hatası: %s" % resp["error"])
        return self

    def call(self, name: str, arguments: dict) -> Any:
        """Bir aracı çağır; content[0].text içindeki JSON'u (varsa) döndür."""
        if self.session_id is None:
            self.connect()
        resp = self._post(
            {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            }
        )
        if "error" in resp:
            raise AnamnesisError("%s hatası: %s" % (name, resp["error"]))
        result = resp.get("result", {})
        content = result.get("content", [])
        if content and isinstance(content, list):
            text = content[0].get("text", "")
            try:
                return json.loads(text, strict=False)
            except (json.JSONDecodeError, TypeError):
                return text
        return result

    # -- yüksek seviye araç sarmalayıcıları -----------------------------------
    def corpus_stats(self) -> dict:
        return self.call("corpus_stats", {})

    def ingest_document(
        self,
        text: str,
        doc_id: str,
        title: str = "",
        source: str = "",
        metadata: dict | None = None,
    ) -> dict:
        args: dict = {"text": text, "doc_id": doc_id}
        if title:
            args["title"] = title
        if source:
            args["source"] = source
        if metadata:
            args["metadata"] = metadata
        return self.call("ingest_document", args)

    def hybrid_query(
        self, query: str, queries: list[str] | None = None, k: int = 6
    ) -> dict:
        args: dict = {"query": query, "k": k}
        if queries:
            args["queries"] = queries
        return self.call("hybrid_query", args)

    def semantic_search(
        self, query: str, queries: list[str] | None = None, k: int = 6
    ) -> dict:
        args: dict = {"query": query, "k": k}
        if queries:
            args["queries"] = queries
        return self.call("semantic_search", args)

    def upsert_triples(self, triples: list[dict]) -> dict:
        return self.call("upsert_triples", {"triples": triples})

    def graph_neighbors(self, entity: str, hops: int = 1) -> dict:
        return self.call("graph_neighbors", {"entity": entity, "hops": hops})

    def subgraph(self, entities: list[str]) -> dict:
        return self.call("subgraph", {"entities": entities})

    def forget_document(self, doc_id: str) -> dict:
        return self.call("forget_document", {"doc_id": doc_id})


if __name__ == "__main__":
    # Smoke: bağlan + korpus istatistiği
    load_dotenv()
    c = AnamnesisClient().connect()
    print("session_ok:", bool(c.session_id))
    print("corpus_stats:", json.dumps(c.corpus_stats(), ensure_ascii=False))
