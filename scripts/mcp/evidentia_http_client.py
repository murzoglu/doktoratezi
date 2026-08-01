#!/usr/bin/env python3
"""Evidentia HTTP MCP connector'ları için bağımlılıksız genel istemci.

OpenAthens (Tier 3, lisanslı kurumsal) ve Anna's (Tier 5, son çare) tam-metin
connector'ları Streamable-HTTP MCP server'larıdır (anamnesis ile aynı desen):
initialize → `mcp-session-id` başlığı → sonraki her çağrı bu session ile.
Yanıtlar SSE (`event: message` / `data: {...}`) çerçevesinde gelebilir.

Bu modül o protokolü tek sınıfta kapsüller ve Minerva rate-limit'te (429) tam-
metin kanıt hattının alternatif bandını sağlar.

Bağlı connector'lar (Evidentia plugin .mcp.json):
  openathens    → https://openathens.cureonics.com/mcp   (Bearer OPENATHENS_MCP_API_KEY)
                  araçlar: oa_resolve, oa_fetch_fulltext, oa_list_databases,
                           oa_batch_submit, oa_batch_result
  annas-reader  → https://annas.cureonics.com/mcp         (Bearer ANNAS_MCP_API_KEY)
                  araçlar: article_search, article_download, book_search, book_download

KVKK: bu gateway'lere YALNIZ literatür arama terimleri / DOI gider; katılımcı/
ham tez/aile-düzeyi veri, transkript veya kimlikleyici ASLA. Değerler loglanmaz.

Kullanım:
  python3 scripts/mcp/evidentia_http_client.py list openathens
  python3 scripts/mcp/evidentia_http_client.py list annas
  python3 scripts/mcp/evidentia_http_client.py call openathens oa_resolve '{"doi":"10.1111/pedi.13428"}'
"""
from __future__ import annotations

import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

PROTO = "2024-11-05"
HTTP_TIMEOUT = 90
_ROOT = Path(__file__).resolve().parents[2]

CONNECTORS = {
    "openathens": {
        "url": "https://openathens.cureonics.com/mcp",
        "key_env": "OPENATHENS_MCP_API_KEY",
    },
    "annas": {
        "url": "https://annas.cureonics.com/mcp",
        "key_env": "ANNAS_MCP_API_KEY",
    },
    "annas-reader": {
        "url": "https://annas.cureonics.com/mcp",
        "key_env": "ANNAS_MCP_API_KEY",
    },
}

_CTX = ssl.create_default_context()
_cab = os.environ.get("CURL_CA_BUNDLE") or os.environ.get("SSL_CERT_FILE")
if _cab and os.path.exists(_cab):
    try:
        _CTX.load_verify_locations(_cab)
    except Exception:  # noqa: BLE001
        pass


def load_dotenv() -> None:
    envf = _ROOT / ".env"
    if not envf.exists():
        return
    for line in envf.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class EvidentiaHTTPError(Exception):
    pass


def _parse_sse_or_json(body: str) -> dict:
    """SSE veya düz JSON gövdesinden ilk JSON-RPC nesnesini ayrıştır."""
    # düz JSON denemesi
    b = body.strip()
    if b.startswith("{"):
        try:
            return json.loads(b, strict=False)
        except json.JSONDecodeError:
            pass
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            line = line[5:].strip()
        if line.startswith("{"):
            try:
                return json.loads(line, strict=False)
            except json.JSONDecodeError:
                continue
    raise EvidentiaHTTPError("yanıt ayrıştırılamadı: %s" % body[:200])


class EvidentiaHTTPClient:
    """Genel Streamable-HTTP MCP oturumu (openathens | annas)."""

    def __init__(self, connector: str, retries: int = 3):
        if connector not in CONNECTORS:
            raise EvidentiaHTTPError("bilinmeyen connector: %s" % connector)
        cfg = CONNECTORS[connector]
        self.name = connector
        self.url = cfg["url"]
        self.api_key = os.environ.get(cfg["key_env"], "")
        if not self.api_key:
            raise EvidentiaHTTPError(
                "%s yok — load_dotenv() çağrıldı mı?" % cfg["key_env"])
        self.retries = retries
        self.session_id: str | None = None
        self._rpc_id = 0

    def _headers(self) -> dict:
        h = {
            "Authorization": "Bearer %s" % self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "t1dm-evidentia-http/1.0",
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
                    self.url, data=data, headers=self._headers(), method="POST")
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT, context=_CTX) as resp:
                    if capture_session:
                        sid = resp.headers.get("mcp-session-id")
                        if sid:
                            self.session_id = sid.strip()
                    body = resp.read().decode("utf-8", "replace")
                return _parse_sse_or_json(body)
            except urllib.error.HTTPError as e:
                last_exc = e
                if e.code in (429, 500, 502, 503, 504) and attempt < self.retries - 1:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                detail = ""
                try:
                    detail = e.read().decode("utf-8", "replace")[:200]
                except Exception:  # noqa: BLE001
                    pass
                raise EvidentiaHTTPError("HTTP %s: %s" % (e.code, detail)) from e
            except (urllib.error.URLError, TimeoutError) as e:
                last_exc = e
                if attempt < self.retries - 1:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise EvidentiaHTTPError("ağ hatası: %s" % e) from e
        raise EvidentiaHTTPError("beklenmeyen: %s" % last_exc)

    def _next_id(self) -> int:
        self._rpc_id += 1
        return self._rpc_id

    def connect(self) -> "EvidentiaHTTPClient":
        resp = self._post({
            "jsonrpc": "2.0", "id": self._next_id(), "method": "initialize",
            "params": {"protocolVersion": PROTO, "capabilities": {},
                       "clientInfo": {"name": "t1dm-evidentia-http", "version": "1.0"}},
        }, capture_session=True)
        if "error" in resp:
            raise EvidentiaHTTPError("initialize hatası: %s" % resp["error"])
        return self

    def list_tools(self) -> list[dict]:
        if self.session_id is None:
            self.connect()
        resp = self._post({
            "jsonrpc": "2.0", "id": self._next_id(), "method": "tools/list", "params": {}})
        if "error" in resp:
            raise EvidentiaHTTPError("tools/list hatası: %s" % resp["error"])
        return resp.get("result", {}).get("tools", [])

    def call(self, name: str, arguments: dict) -> Any:
        if self.session_id is None:
            self.connect()
        resp = self._post({
            "jsonrpc": "2.0", "id": self._next_id(), "method": "tools/call",
            "params": {"name": name, "arguments": arguments}})
        if "error" in resp:
            raise EvidentiaHTTPError("%s hatası: %s" % (name, resp["error"]))
        result = resp.get("result", {})
        content = result.get("content", [])
        if content and isinstance(content, list):
            text = content[0].get("text", "")
            try:
                return json.loads(text, strict=False)
            except (json.JSONDecodeError, TypeError):
                return text
        return result


def _main(argv: list[str]) -> int:
    load_dotenv()
    if len(argv) < 2:
        print(__doc__)
        return 1
    op = argv[0]
    conn = argv[1]
    try:
        c = EvidentiaHTTPClient(conn).connect()
    except EvidentiaHTTPError as e:
        print("BAĞLANTI HATASI: %s" % e, file=sys.stderr)
        return 2
    if op == "list":
        tools = c.list_tools()
        for t in tools:
            print("- %s: %s" % (t.get("name"), (t.get("description") or "")[:90]))
        print("toplam=%d" % len(tools))
        return 0
    if op == "call":
        name = argv[2]
        args = json.loads(argv[3]) if len(argv) > 3 else {}
        out = c.call(name, args)
        print(json.dumps(out, ensure_ascii=False, indent=2)[:4000])
        return 0
    print("bilinmeyen op: %s" % op, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
