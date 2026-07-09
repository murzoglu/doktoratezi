#!/usr/bin/env python3
"""Zotero Web API bridge that loads ZOTERO_API_KEY from a local .env file.

This is intentionally small and dependency-free. It complements the curated
Zotero Desktop helper, which only talks to the local Zotero app API on
127.0.0.1:23119. This bridge is for headless Web API status/search/BibTeX
export/citation insertion using an API key already present in .env.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


API_BASE = os.environ.get("ZOTERO_API_BASE", "https://api.zotero.org")
DEFAULT_ENV_PATHS = (
    ".env",
    "/mnt/thunderbolt/workspaces/doktoratezi/.env",
)
DEFAULT_BIB_PATH = "references/references.bib"
API_PAGE_LIMIT = 100


@dataclass(frozen=True)
class ZoteroContext:
    api_key: str
    env_file: Path | None
    user_id: str | None = None
    username: str | None = None


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def resolve_env_file(path: str | None) -> Path | None:
    candidates: list[Path] = []
    if path:
        candidates.append(Path(path))
    if os.environ.get("ZOTERO_ENV_FILE"):
        candidates.append(Path(os.environ["ZOTERO_ENV_FILE"]))
    candidates.extend(Path(item) for item in DEFAULT_ENV_PATHS)
    for candidate in candidates:
        expanded = candidate.expanduser()
        if expanded.exists():
            return expanded.resolve()
    return None


def build_context(args: argparse.Namespace) -> ZoteroContext:
    env_file = resolve_env_file(getattr(args, "env_file", None))
    if env_file:
        load_dotenv(env_file)
    api_key = os.environ.get("ZOTERO_API_KEY", "").strip().strip('"').strip("'").strip()
    if not api_key:
        raise SystemExit("ZOTERO_API_KEY is not set in environment or .env")
    return ZoteroContext(api_key=api_key, env_file=env_file)


def request(ctx: ZoteroContext, path: str, *, timeout: float = 20.0) -> tuple[Any, dict[str, str], str]:
    url = API_BASE.rstrip("/") + path
    req = urllib.request.Request(
        url,
        headers={
            "Zotero-API-Version": "3",
            "Zotero-API-Key": ctx.api_key,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            text = response.read().decode("utf-8", errors="replace")
            headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise SystemExit(f"Zotero Web API request failed: status={exc.code} detail={detail}")
    except Exception as exc:
        raise SystemExit(f"Zotero Web API request failed: {exc}")

    content_type = headers.get("Content-Type", "")
    if "json" in content_type.lower():
        return json.loads(text or "null"), headers, text
    return text, headers, text


def key_info(ctx: ZoteroContext) -> dict[str, Any]:
    payload, _headers, _text = request(ctx, "/keys/current")
    if not isinstance(payload, dict):
        raise SystemExit("Unexpected Zotero /keys/current response")
    return payload


def context_with_user(ctx: ZoteroContext) -> ZoteroContext:
    info = key_info(ctx)
    user_id = info.get("userID") or info.get("userId")
    username = info.get("username")
    if user_id is None:
        raise SystemExit("Zotero key is valid, but /keys/current did not return userID")
    return ZoteroContext(
        api_key=ctx.api_key,
        env_file=ctx.env_file,
        user_id=str(user_id),
        username=str(username) if username else None,
    )


def query(params: dict[str, str | int | None]) -> str:
    clean = {key: value for key, value in params.items() if value is not None}
    return urllib.parse.urlencode(clean)


def creators_from_item(data: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for creator in data.get("creators", []) or []:
        name = creator.get("name") or " ".join(
            part for part in [creator.get("firstName"), creator.get("lastName")] if part
        )
        if name:
            names.append(name)
    return names


def year_from_date(raw: str | None) -> str | None:
    if not raw:
        return None
    match = re.search(r"(\d{4})", raw)
    return match.group(1) if match else None


def summarize_item(item: dict[str, Any]) -> dict[str, Any]:
    data = item.get("data", item)
    return {
        "key": item.get("key") or data.get("key"),
        "itemType": data.get("itemType"),
        "title": data.get("title"),
        "creators": creators_from_item(data),
        "year": year_from_date(data.get("date")),
        "doi": data.get("DOI"),
        "url": data.get("url"),
    }


def extract_bibtex_keys(text: str) -> list[str]:
    return re.findall(r"@\w+\s*\{\s*([^,\s]+)", text)


def count_bibtex_entries(text: str) -> int:
    return len(extract_bibtex_keys(text))


def library_path(ctx: ZoteroContext) -> str:
    if not ctx.user_id:
        raise SystemExit("Missing Zotero userID")
    return f"/users/{urllib.parse.quote(str(ctx.user_id))}"


def export_bibtex(ctx: ZoteroContext, item_key: str | None = None, *, include_children: bool = False) -> str:
    if item_key:
        path = f"{library_path(ctx)}/items/{urllib.parse.quote(item_key)}?format=bibtex"
        _payload, _headers, text = request(ctx, path)
        return text

    endpoint = "items" if include_children else "items/top"
    start = 0
    chunks: list[str] = []
    while True:
        params = query(
            {
                "format": "bibtex",
                "sort": "title",
                "direction": "asc",
                "limit": API_PAGE_LIMIT,
                "start": start,
            }
        )
        _payload, headers, text = request(ctx, f"{library_path(ctx)}/{endpoint}?{params}")
        if text.strip():
            chunks.append(text.strip())
        total = int(headers.get("Total-Results") or "0")
        start += API_PAGE_LIMIT
        if not total or start >= total:
            break
    output = "\n\n".join(chunks)
    return output + "\n" if output else ""


def append_bib_entry(bib_path: Path, entry: str) -> tuple[str, bool]:
    keys = extract_bibtex_keys(entry)
    if not keys:
        raise SystemExit("Could not extract a BibTeX key from Zotero export")
    key = keys[0]
    existing = bib_path.read_text(encoding="utf-8", errors="replace") if bib_path.exists() else ""
    already_present = re.search(r"@\w+\s*\{\s*" + re.escape(key) + r"\s*,", existing) is not None
    if already_present:
        return key, False
    bib_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = existing.rstrip("\n") + "\n\n" if existing else ""
    bib_path.write_text(prefix + entry.strip() + "\n", encoding="utf-8")
    return key, True


def insert_citation(target: Path, citation: str, marker: str | None) -> None:
    text = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
    if marker:
        if marker not in text:
            raise SystemExit(f"Marker not found in {target}: {marker!r}")
        target.write_text(text.replace(marker, citation, 1), encoding="utf-8")
        return
    suffix = "" if not text or text.endswith("\n") else "\n"
    target.write_text(text + suffix + citation + "\n", encoding="utf-8")


def find_items(ctx: ZoteroContext, query_text: str, *, limit: int) -> list[dict[str, Any]]:
    params = query({"q": query_text, "limit": limit, "format": "json"})
    payload, _headers, _text = request(ctx, f"{library_path(ctx)}/items/top?{params}")
    if not isinstance(payload, list):
        raise SystemExit("Unexpected Zotero search response")
    return payload


def dump_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def cmd_status(args: argparse.Namespace) -> None:
    ctx = build_context(args)
    info = key_info(ctx)
    payload = {
        "ok": True,
        "env_file": str(ctx.env_file) if ctx.env_file else None,
        "key_loaded": bool(ctx.api_key),
        "userID": info.get("userID") or info.get("userId"),
        "username": info.get("username"),
        "access": info.get("access"),
    }
    dump_json(payload) if args.json else print(f"Zotero Web API OK userID={payload['userID']} username={payload['username']}")


def cmd_search(args: argparse.Namespace) -> None:
    ctx = context_with_user(build_context(args))
    rows = [summarize_item(item) for item in find_items(ctx, args.query, limit=args.limit)]
    if args.with_bibtex_keys:
        for row in rows:
            if row.get("key"):
                keys = extract_bibtex_keys(export_bibtex(ctx, row["key"]))
                row["bibtexKey"] = keys[0] if keys else None
    dump_json(rows) if args.json else print_items(rows)


def print_items(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        creators = ", ".join(row.get("creators") or [])
        print(
            f"{row.get('key') or '':10} "
            f"{row.get('itemType') or '':14} "
            f"{row.get('year') or '':4} "
            f"{row.get('title') or ''} | {creators}"
        )


def cmd_export_bibtex(args: argparse.Namespace) -> None:
    ctx = context_with_user(build_context(args))
    text = export_bibtex(ctx, args.item_key, include_children=args.include_children)
    if not args.out:
        print(text, end="" if text.endswith("\n") else "\n")
        return
    path = Path(args.out).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    dump_json({"path": str(path), "bytes": len(text.encode("utf-8")), "bibtex_entries": count_bibtex_entries(text)})


def cmd_cite(args: argparse.Namespace) -> None:
    ctx = context_with_user(build_context(args))
    item_key = args.item_key
    title = None
    if not item_key:
        matches = find_items(ctx, args.query, limit=1)
        if not matches:
            raise SystemExit(f"No Zotero Web API items matched query: {args.query}")
        summary = summarize_item(matches[0])
        item_key = summary.get("key")
        title = summary.get("title")
    entry = export_bibtex(ctx, item_key)
    citekey, added = append_bib_entry(Path(args.bib).expanduser().resolve(), entry)
    citation = f"\\cite{{{citekey}}}" if args.tex else f"[@{citekey}]"
    target = Path(args.tex or args.markdown).expanduser().resolve()
    insert_citation(target, citation, args.marker)
    dump_json(
        {
            "item_key": item_key,
            "title": title,
            "bibtex_key": citekey,
            "bib_path": str(Path(args.bib).expanduser().resolve()),
            "bib_entry_added": added,
            "edited_file": str(target),
            "inserted": citation,
        }
    )


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--env-file", help="Path to .env containing ZOTERO_API_KEY")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)

    status = subcommands.add_parser("status", help="Check Zotero Web API key from .env")
    status.add_argument("--json", action="store_true")
    add_common(status)
    status.set_defaults(func=cmd_status)

    search = subcommands.add_parser("search", help="Search Zotero Web API top-level items")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--with-bibtex-keys", action="store_true")
    search.add_argument("--json", action="store_true")
    add_common(search)
    search.set_defaults(func=cmd_search)

    export = subcommands.add_parser("export-bibtex", help="Export Zotero Web API items as BibTeX")
    export.add_argument("--item-key")
    export.add_argument("--include-children", action="store_true")
    export.add_argument("--out", default=DEFAULT_BIB_PATH)
    add_common(export)
    export.set_defaults(func=cmd_export_bibtex)

    cite = subcommands.add_parser("cite", help="Insert a citation and update a .bib file using Zotero Web API")
    source = cite.add_mutually_exclusive_group(required=True)
    source.add_argument("--item-key")
    source.add_argument("--query")
    target = cite.add_mutually_exclusive_group(required=True)
    target.add_argument("--tex")
    target.add_argument("--markdown")
    cite.add_argument("--bib", default=DEFAULT_BIB_PATH)
    cite.add_argument("--marker")
    add_common(cite)
    cite.set_defaults(func=cmd_cite)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
