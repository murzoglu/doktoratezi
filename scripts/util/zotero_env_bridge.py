#!/usr/bin/env python3
"""Zotero Web API bridge that loads ZOTERO_API_KEY from a local .env file.

This is intentionally dependency-free. It complements the curated
Zotero Desktop helper, which only talks to the local Zotero app API on
127.0.0.1:23119. This bridge is for headless Web API status/search/BibTeX
export/citation insertion/import and full-text attachment upload using an API
key already present in .env.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import mimetypes
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
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
    group_id: str | None = None
    group_name: str | None = None
    collection_key: str | None = None
    collection_name: str | None = None


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


def request(
    ctx: ZoteroContext,
    path: str,
    *,
    method: str = "GET",
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
    allow_statuses: set[int] | None = None,
    timeout: float = 20.0,
) -> tuple[Any, dict[str, str], str]:
    url = API_BASE.rstrip("/") + path
    merged_headers = {
        "Zotero-API-Version": "3",
        "Zotero-API-Key": ctx.api_key,
    }
    if headers:
        merged_headers.update(headers)
    req = urllib.request.Request(
        url,
        data=body,
        headers=merged_headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            text = response.read().decode("utf-8", errors="replace")
            headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        if allow_statuses and exc.code in allow_statuses:
            response_headers = dict(exc.headers.items())
            return detail, response_headers, detail
        raise SystemExit(f"Zotero Web API request failed: status={exc.code} detail={detail}")
    except Exception as exc:
        raise SystemExit(f"Zotero Web API request failed: {exc}")

    content_type = headers.get("Content-Type", "")
    if "json" in content_type.lower():
        return json.loads(text or "null"), headers, text
    return text, headers, text


def external_request(
    url: str,
    *,
    method: str = "GET",
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 30.0,
) -> tuple[Any, dict[str, str], str]:
    req = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
            response_headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise SystemExit(f"External request failed: status={exc.code} detail={detail}")
    except Exception as exc:
        raise SystemExit(f"External request failed: {exc}")

    text = raw.decode("utf-8", errors="replace")
    content_type = response_headers.get("Content-Type", "")
    if "json" in content_type.lower():
        return json.loads(text or "null"), response_headers, text
    return text, response_headers, text


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
        group_id=ctx.group_id,
        group_name=ctx.group_name,
        collection_key=ctx.collection_key,
        collection_name=ctx.collection_name,
    )


def list_groups(ctx: ZoteroContext) -> list[dict[str, Any]]:
    payload, _headers, _text = request(ctx, f"/users/{urllib.parse.quote(str(ctx.user_id))}/groups?format=json")
    if not isinstance(payload, list):
        raise SystemExit("Unexpected Zotero groups response")
    return payload


def summarize_group(group: dict[str, Any]) -> dict[str, Any]:
    data = group.get("data", group)
    return {
        "id": str(data.get("id") or group.get("id") or ""),
        "name": data.get("name"),
        "type": data.get("type"),
        "libraryEditing": data.get("libraryEditing"),
        "fileEditing": data.get("fileEditing"),
    }


def list_collections(ctx: ZoteroContext) -> list[dict[str, Any]]:
    start = 0
    rows: list[dict[str, Any]] = []
    while True:
        params = query({"format": "json", "limit": API_PAGE_LIMIT, "start": start})
        payload, headers, _text = request(ctx, f"{library_path(ctx)}/collections?{params}")
        if not isinstance(payload, list):
            raise SystemExit("Unexpected Zotero collections response")
        rows.extend(payload)
        total = int(headers.get("Total-Results") or "0")
        start += API_PAGE_LIMIT
        if not total or start >= total:
            break
    return rows


def summarize_collection(collection: dict[str, Any]) -> dict[str, Any]:
    data = collection.get("data", collection)
    return {
        "key": data.get("key") or collection.get("key"),
        "name": data.get("name"),
        "parentCollection": data.get("parentCollection"),
    }


def context_with_target_library(ctx: ZoteroContext, args: argparse.Namespace) -> ZoteroContext:
    ctx = context_with_user(ctx)
    group_id = getattr(args, "group_id", None)
    group_name = getattr(args, "group_name", None)
    collection_key = getattr(args, "collection_key", None)
    collection_name = getattr(args, "collection_name", None)
    library_name = getattr(args, "library", None)

    if group_id or group_name or library_name:
        wanted_name = group_name or library_name
        groups = [summarize_group(group) for group in list_groups(ctx)]
        if group_id:
            match = next((group for group in groups if group["id"] == str(group_id)), None)
        else:
            wanted = str(wanted_name).strip().casefold()
            match = next((group for group in groups if str(group.get("name") or "").strip().casefold() == wanted), None)
        if match:
            if str(match.get("libraryEditing") or "").lower() == "none":
                raise SystemExit(f"Zotero group library is not writable: {match.get('name')}")
            ctx = ZoteroContext(
                api_key=ctx.api_key,
                env_file=ctx.env_file,
                user_id=ctx.user_id,
                username=ctx.username,
                group_id=str(match["id"]),
                group_name=str(match.get("name") or match["id"]),
            )
        elif group_id or group_name:
            available = ", ".join(group.get("name") or group.get("id") or "?" for group in groups) or "no groups"
            raise SystemExit(f"Zotero group library not found: {wanted_name or group_id}. Available: {available}")
        elif library_name and not collection_name:
            collection_name = library_name

    if collection_key or collection_name:
        collections = [summarize_collection(collection) for collection in list_collections(ctx)]
        if collection_key:
            collection_match = next((collection for collection in collections if collection["key"] == str(collection_key)), None)
        else:
            wanted = str(collection_name).strip().casefold()
            collection_match = next(
                (collection for collection in collections if str(collection.get("name") or "").strip().casefold() == wanted),
                None,
            )
        if not collection_match:
            available = ", ".join(collection.get("name") or collection.get("key") or "?" for collection in collections) or "no collections"
            raise SystemExit(f"Zotero collection not found: {collection_name or collection_key}. Available: {available}")
        return ZoteroContext(
            api_key=ctx.api_key,
            env_file=ctx.env_file,
            user_id=ctx.user_id,
            username=ctx.username,
            group_id=ctx.group_id,
            group_name=ctx.group_name,
            collection_key=str(collection_match["key"]),
            collection_name=str(collection_match.get("name") or collection_match["key"]),
        )

    return ZoteroContext(
        api_key=ctx.api_key,
        env_file=ctx.env_file,
        user_id=ctx.user_id,
        username=ctx.username,
        group_id=ctx.group_id,
        group_name=ctx.group_name,
        collection_key=ctx.collection_key,
        collection_name=ctx.collection_name,
    )


def query(params: dict[str, str | int | None]) -> str:
    clean = {key: value for key, value in params.items() if value is not None}
    return urllib.parse.urlencode(clean)


def normalize_doi(value: str | None) -> str:
    if not value:
        return ""
    doi = value.strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    return doi.rstrip(" .")


def now_zotero_access_date() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def post_json(ctx: ZoteroContext, path: str, payload: Any) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    response, _headers, _text = request(
        ctx,
        path,
        method="POST",
        body=body,
        headers={"Content-Type": "application/json"},
    )
    if not isinstance(response, dict):
        raise SystemExit("Unexpected Zotero write response")
    failed = response.get("failed") or {}
    if failed:
        raise SystemExit(f"Zotero item write failed: {json.dumps(failed, ensure_ascii=False)[:500]}")
    return response


def created_key(response: dict[str, Any], index: str = "0") -> str:
    successful = response.get("successful") or {}
    record = successful.get(index)
    if not isinstance(record, dict):
        raise SystemExit(f"Zotero write response did not include successful index {index}")
    key = record.get("key") or (record.get("data") or {}).get("key")
    if not key:
        raise SystemExit("Zotero write response did not include an item key")
    return str(key)


def crossref_work(doi: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(normalize_doi(doi), safe="")
    payload, _headers, _text = external_request(f"https://api.crossref.org/works/{encoded}")
    if not isinstance(payload, dict) or not isinstance(payload.get("message"), dict):
        raise SystemExit(f"Crossref did not return metadata for DOI {doi}")
    return payload["message"]


def crossref_text(values: list[Any] | None) -> str:
    if not values:
        return ""
    first = values[0]
    if isinstance(first, str):
        return first
    return str(first)


def crossref_date(parts: dict[str, Any] | None) -> str:
    if not parts:
        return ""
    date_parts = parts.get("date-parts") or []
    if not date_parts or not isinstance(date_parts[0], list):
        return ""
    return "-".join(str(part) for part in date_parts[0] if part is not None)


def crossref_creators(authors: list[dict[str, Any]] | None) -> list[dict[str, str]]:
    creators: list[dict[str, str]] = []
    for author in authors or []:
        last_name = str(author.get("family") or "").strip()
        first_name = str(author.get("given") or "").strip()
        literal = str(author.get("name") or "").strip()
        if last_name:
            creators.append({"creatorType": "author", "firstName": first_name, "lastName": last_name})
        elif literal:
            creators.append({"creatorType": "author", "name": literal})
    return creators


def zotero_item_from_crossref(work: dict[str, Any], doi: str) -> dict[str, Any]:
    issn = work.get("ISSN") or []
    return {
        "itemType": "journalArticle",
        "title": crossref_text(work.get("title")),
        "creators": crossref_creators(work.get("author")),
        "abstractNote": re.sub(r"<[^>]+>", "", crossref_text(work.get("abstract"))),
        "publicationTitle": crossref_text(work.get("container-title")),
        "volume": str(work.get("volume") or ""),
        "issue": str(work.get("issue") or ""),
        "pages": str(work.get("page") or ""),
        "date": crossref_date(work.get("published-print") or work.get("published-online") or work.get("issued")),
        "DOI": normalize_doi(work.get("DOI") or doi),
        "ISSN": ", ".join(str(item) for item in issn),
        "url": str(work.get("URL") or f"https://doi.org/{normalize_doi(doi)}"),
        "libraryCatalog": "Crossref",
        "language": "en",
    }


def find_item_by_doi(ctx: ZoteroContext, doi: str) -> dict[str, Any] | None:
    target = normalize_doi(doi)
    if not target:
        return None
    lookup_ctx = ZoteroContext(
        api_key=ctx.api_key,
        env_file=ctx.env_file,
        user_id=ctx.user_id,
        username=ctx.username,
        group_id=ctx.group_id,
        group_name=ctx.group_name,
    )
    matches = find_items(lookup_ctx, target, limit=25)
    for item in matches:
        data = item.get("data", item)
        if normalize_doi(data.get("DOI")) == target:
            return item
    return None


def find_item_by_title_or_doi(ctx: ZoteroContext, title: str, doi: str) -> dict[str, Any] | None:
    target = normalize_doi(doi)
    normalized_title = re.sub(r"\s+", " ", title or "").strip().lower()
    if not normalized_title:
        return find_item_by_doi(ctx, doi)
    lookup_ctx = ZoteroContext(
        api_key=ctx.api_key,
        env_file=ctx.env_file,
        user_id=ctx.user_id,
        username=ctx.username,
        group_id=ctx.group_id,
        group_name=ctx.group_name,
    )
    matches = find_items(lookup_ctx, normalized_title[:180], limit=25)
    for item in matches:
        data = item.get("data", item)
        item_title = re.sub(r"\s+", " ", str(data.get("title") or "")).strip().lower()
        if normalize_doi(data.get("DOI")) == target or item_title == normalized_title:
            return item
    return find_item_by_doi(ctx, doi)


def create_item_from_doi(ctx: ZoteroContext, doi: str) -> dict[str, Any]:
    work = crossref_work(doi)
    existing = find_item_by_title_or_doi(ctx, crossref_text(work.get("title")), doi)
    if existing:
        return existing
    response = post_json(ctx, f"{library_path(ctx)}/items", [zotero_item_from_crossref(work, doi)])
    item_key = created_key(response)
    return get_item(ctx, item_key)


def get_item(ctx: ZoteroContext, item_key: str) -> dict[str, Any]:
    payload, _headers, _text = request(ctx, f"{library_path(ctx)}/items/{urllib.parse.quote(item_key)}")
    if not isinstance(payload, dict):
        raise SystemExit(f"Unexpected Zotero item response for {item_key}")
    return payload


def delete_item(ctx: ZoteroContext, item_key: str) -> dict[str, Any]:
    item = get_item(ctx, item_key)
    version = item.get("version") or (item.get("data") or {}).get("version")
    if version is None:
        raise SystemExit(f"Zotero item {item_key} did not include a version")
    _payload, headers, _text = request(
        ctx,
        f"{library_path(ctx)}/items/{urllib.parse.quote(item_key)}",
        method="DELETE",
        headers={"If-Unmodified-Since-Version": str(version)},
        timeout=60.0,
    )
    return {
        "deleted_item_key": item_key,
        "previous_version": version,
        "last_modified_version": headers.get("Last-Modified-Version"),
    }


def patch_item(ctx: ZoteroContext, item_key: str, data: dict[str, Any]) -> dict[str, Any]:
    item = get_item(ctx, item_key)
    version = item.get("version") or (item.get("data") or {}).get("version")
    if version is None:
        raise SystemExit(f"Zotero item {item_key} did not include a version")
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    _payload, headers, _text = request(
        ctx,
        f"{library_path(ctx)}/items/{urllib.parse.quote(item_key)}",
        method="PATCH",
        body=body,
        headers={
            "Content-Type": "application/json",
            "If-Unmodified-Since-Version": str(version),
        },
        timeout=60.0,
    )
    return {
        "item_key": item_key,
        "previous_version": version,
        "last_modified_version": headers.get("Last-Modified-Version"),
    }


def set_citation_key(ctx: ZoteroContext, item_key: str, citation_key: str) -> dict[str, Any]:
    item = get_item(ctx, item_key)
    data = item.get("data") or {}
    extra = str(data.get("extra") or "").strip()
    lines = [line for line in extra.splitlines() if not re.match(r"^\s*Citation Key\s*:", line, flags=re.I)]
    lines.append(f"Citation Key: {citation_key}")
    payload = patch_item(ctx, item_key, {"extra": "\n".join(line for line in lines if line).strip()})
    payload["citation_key"] = citation_key
    return payload


def add_item_to_collection(ctx: ZoteroContext, item_key: str, collection_key: str) -> dict[str, Any]:
    item = get_item(ctx, item_key)
    data = item.get("data") or {}
    collections = list(data.get("collections") or [])
    if collection_key not in collections:
        collections.append(collection_key)
    payload = patch_item(ctx, item_key, {"collections": collections})
    payload["collection_key"] = collection_key
    return payload


def get_children(ctx: ZoteroContext, parent_key: str) -> list[dict[str, Any]]:
    params = query({"format": "json", "limit": API_PAGE_LIMIT})
    payload, _headers, _text = request(
        ctx,
        f"{library_path(ctx)}/items/{urllib.parse.quote(parent_key)}/children?{params}",
    )
    if not isinstance(payload, list):
        raise SystemExit(f"Unexpected Zotero children response for {parent_key}")
    return payload


def summarize_child(item: dict[str, Any]) -> dict[str, Any]:
    data = item.get("data", item)
    return {
        "key": item.get("key") or data.get("key"),
        "itemType": data.get("itemType"),
        "linkMode": data.get("linkMode"),
        "title": data.get("title"),
        "filename": data.get("filename"),
        "contentType": data.get("contentType"),
        "url": data.get("url"),
    }


def child_exists(
    children: list[dict[str, Any]],
    *,
    item_type: str,
    title: str | None = None,
    url: str | None = None,
    filename: str | None = None,
) -> dict[str, Any] | None:
    for child in children:
        data = child.get("data", child)
        if data.get("itemType") != item_type:
            continue
        child_title = data.get("title") or data.get("note") or ""
        if title and title not in child_title:
            continue
        if url and data.get("url") != url:
            continue
        if filename and data.get("filename") != filename:
            continue
        return child
    return None


def create_note(ctx: ZoteroContext, parent_key: str, note_text: str, *, title: str = "Full-text access note") -> str:
    children = get_children(ctx, parent_key)
    child = child_exists(children, item_type="note", title=title)
    if child:
        return str((child or {}).get("key") or ((child or {}).get("data") or {}).get("key"))
    note_html = f"<h2>{html.escape(title)}</h2><p>{html.escape(note_text).replace(chr(10), '<br/>')}</p>"
    response = post_json(
        ctx,
        f"{library_path(ctx)}/items",
        [{"itemType": "note", "parentItem": parent_key, "note": note_html}],
    )
    return created_key(response)


def create_url_attachment(ctx: ZoteroContext, parent_key: str, url: str, *, title: str) -> str:
    children = get_children(ctx, parent_key)
    existing = child_exists(children, item_type="attachment", title=title, url=url)
    if existing:
        return str(existing.get("key") or (existing.get("data") or {}).get("key"))
    response = post_json(
        ctx,
        f"{library_path(ctx)}/items",
        [
            {
                "itemType": "attachment",
                "parentItem": parent_key,
                "linkMode": "linked_url",
                "title": title,
                "accessDate": now_zotero_access_date(),
                "url": url,
                "contentType": "text/html",
            }
        ],
    )
    return created_key(response)


def rewrite_bibtex_key(entry: str, forced_key: str | None) -> str:
    if not forced_key:
        return entry
    return re.sub(r"(@\w+\s*\{\s*)[^,\s]+", rf"\g<1>{forced_key}", entry, count=1)


def upload_file_attachment(ctx: ZoteroContext, parent_key: str, file_path: Path, *, title: str) -> str:
    resolved = file_path.expanduser().resolve()
    if not resolved.exists():
        raise SystemExit(f"Attachment file not found: {resolved}")
    content = resolved.read_bytes()
    filename = resolved.name
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    md5 = hashlib.md5(content).hexdigest()
    mtime = int(resolved.stat().st_mtime * 1000)

    children = get_children(ctx, parent_key)
    existing = child_exists(children, item_type="attachment", title=title, filename=filename)
    if existing:
        return str(existing.get("key") or (existing.get("data") or {}).get("key"))

    response = post_json(
        ctx,
        f"{library_path(ctx)}/items",
        [
            {
                "itemType": "attachment",
                "parentItem": parent_key,
                "linkMode": "imported_file",
                "title": title,
                "filename": filename,
                "contentType": content_type,
                "md5": md5,
                "mtime": mtime,
            }
        ],
    )
    attachment_key = created_key(response)
    upload_params = urllib.parse.urlencode(
        {
            "md5": md5,
            "filename": filename,
            "filesize": len(content),
            "mtime": mtime,
        }
    ).encode("utf-8")
    upload_init, _headers, _text = request(
        ctx,
        f"{library_path(ctx)}/items/{urllib.parse.quote(attachment_key)}/file",
        method="POST",
        body=upload_params,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "If-None-Match": "*",
        },
        allow_statuses={412},
        timeout=60.0,
    )
    if isinstance(upload_init, str) and "file exists" in upload_init.lower():
        return attachment_key
    if not isinstance(upload_init, dict):
        raise SystemExit("Unexpected Zotero file upload initialization response")
    if upload_init.get("exists"):
        return attachment_key

    upload_url = upload_init.get("url")
    upload_key = upload_init.get("uploadKey")
    prefix = upload_init.get("prefix") or ""
    suffix = upload_init.get("suffix") or ""
    upload_content_type = upload_init.get("contentType") or "application/octet-stream"
    if not upload_url or not upload_key:
        raise SystemExit("Zotero file upload initialization did not return upload URL/key")

    body = prefix.encode("utf-8") + content + suffix.encode("utf-8")
    external_request(
        str(upload_url),
        method="POST",
        body=body,
        headers={"Content-Type": str(upload_content_type)},
        timeout=120.0,
    )
    register_params = urllib.parse.urlencode({"upload": upload_key}).encode("utf-8")
    request(
        ctx,
        f"{library_path(ctx)}/items/{urllib.parse.quote(attachment_key)}/file",
        method="POST",
        body=register_params,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "If-None-Match": "*",
        },
        allow_statuses={412},
        timeout=60.0,
    )
    return attachment_key


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
    if ctx.group_id:
        return f"/groups/{urllib.parse.quote(str(ctx.group_id))}"
    if not ctx.user_id:
        raise SystemExit("Missing Zotero userID")
    return f"/users/{urllib.parse.quote(str(ctx.user_id))}"


def export_bibtex(ctx: ZoteroContext, item_key: str | None = None, *, include_children: bool = False) -> str:
    if item_key:
        path = f"{library_path(ctx)}/items/{urllib.parse.quote(item_key)}?format=bibtex"
        _payload, _headers, text = request(ctx, path)
        return text

    if ctx.collection_key:
        endpoint = f"collections/{urllib.parse.quote(ctx.collection_key)}/items"
        if not include_children:
            endpoint += "/top"
    else:
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
    endpoint = "items/top"
    if ctx.collection_key:
        endpoint = f"collections/{urllib.parse.quote(ctx.collection_key)}/items/top"
    payload, _headers, _text = request(ctx, f"{library_path(ctx)}/{endpoint}?{params}")
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
    ctx = context_with_target_library(build_context(args), args)
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
    ctx = context_with_target_library(build_context(args), args)
    text = export_bibtex(ctx, args.item_key, include_children=args.include_children)
    if not args.out:
        print(text, end="" if text.endswith("\n") else "\n")
        return
    path = Path(args.out).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    dump_json({"path": str(path), "bytes": len(text.encode("utf-8")), "bibtex_entries": count_bibtex_entries(text)})


def cmd_cite(args: argparse.Namespace) -> None:
    ctx = context_with_target_library(build_context(args), args)
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


def cmd_children(args: argparse.Namespace) -> None:
    ctx = context_with_target_library(build_context(args), args)
    rows = [summarize_child(item) for item in get_children(ctx, args.item_key)]
    dump_json(rows) if args.json else print_items(rows)


def cmd_upload_file(args: argparse.Namespace) -> None:
    ctx = context_with_target_library(build_context(args), args)
    attachment_key = upload_file_attachment(
        ctx,
        args.parent_key,
        Path(args.file),
        title=args.title,
    )
    payload = {
        "parent_item_key": args.parent_key,
        "attachment_key": attachment_key,
        "file": str(Path(args.file).expanduser().resolve()),
        "title": args.title,
    }
    dump_json(payload) if args.json else print(f"Uploaded attachment {attachment_key}")


def cmd_delete_item(args: argparse.Namespace) -> None:
    if not args.yes:
        raise SystemExit("Refusing to delete Zotero item without --yes")
    ctx = context_with_target_library(build_context(args), args)
    payload = delete_item(ctx, args.item_key)
    dump_json(payload) if args.json else print(f"Deleted Zotero item {args.item_key}")


def cmd_set_citation_key(args: argparse.Namespace) -> None:
    ctx = context_with_target_library(build_context(args), args)
    payload = set_citation_key(ctx, args.item_key, args.citation_key)
    dump_json(payload) if args.json else print(f"Set Zotero citation key {args.citation_key} on {args.item_key}")


def cmd_import_doi(args: argparse.Namespace) -> None:
    ctx = context_with_target_library(build_context(args), args)
    item = create_item_from_doi(ctx, args.doi)
    item_key = str(item.get("key") or (item.get("data") or {}).get("key"))
    if not item_key:
        raise SystemExit("Imported Zotero item did not include an item key")
    collection_membership = None
    if ctx.collection_key:
        collection_membership = add_item_to_collection(ctx, item_key, ctx.collection_key)
    citation_key_pin = None
    if args.bibtex_key:
        citation_key_pin = set_citation_key(ctx, item_key, args.bibtex_key)

    url_attachment_key = None
    file_attachment_key = None
    note_key = None
    if args.fulltext_url:
        url_attachment_key = create_url_attachment(
            ctx,
            item_key,
            args.fulltext_url,
            title=args.fulltext_url_title,
        )
    if args.attachment_file:
        file_attachment_key = upload_file_attachment(
            ctx,
            item_key,
            Path(args.attachment_file),
            title=args.attachment_title,
        )
    if args.note:
        note_key = create_note(ctx, item_key, args.note, title=args.note_title)

    entry = rewrite_bibtex_key(export_bibtex(ctx, item_key), args.bibtex_key)
    citekey = extract_bibtex_keys(entry)[0] if extract_bibtex_keys(entry) else None
    bib_added = False
    bib_path = None
    if not args.no_bib:
        bib_path = Path(args.bib).expanduser().resolve()
        citekey, bib_added = append_bib_entry(bib_path, entry)

    payload = {
        "doi": normalize_doi(args.doi),
        "item": summarize_item(item),
        "item_key": item_key,
        "bibtex_key": citekey,
        "bib_path": str(bib_path) if bib_path else None,
        "bib_entry_added": bib_added,
        "url_attachment_key": url_attachment_key,
        "file_attachment_key": file_attachment_key,
        "note_key": note_key,
        "collection_key": ctx.collection_key,
        "collection_name": ctx.collection_name,
        "collection_membership": collection_membership,
        "citation_key_pin": citation_key_pin,
        "children": [summarize_child(child) for child in get_children(ctx, item_key)],
    }
    dump_json(payload) if args.json else print(
        f"Zotero item {item_key}; BibTeX key {citekey}; file attachment {file_attachment_key or '-'}"
    )


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--env-file", help="Path to .env containing ZOTERO_API_KEY")
    parser.add_argument("--library", help="Target Zotero group library name, e.g. 'T1DM Thesis'")
    parser.add_argument("--group-name", help="Target Zotero group library name")
    parser.add_argument("--group-id", help="Target Zotero group id")
    parser.add_argument("--collection-name", help="Target Zotero collection name")
    parser.add_argument("--collection-key", help="Target Zotero collection key")


def cmd_groups(args: argparse.Namespace) -> None:
    ctx = context_with_user(build_context(args))
    rows = [summarize_group(group) for group in list_groups(ctx)]
    dump_json(rows) if args.json else dump_json(rows)


def cmd_collections(args: argparse.Namespace) -> None:
    ctx = context_with_target_library(build_context(args), args)
    rows = [summarize_collection(collection) for collection in list_collections(ctx)]
    dump_json(rows) if args.json else dump_json(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)

    status = subcommands.add_parser("status", help="Check Zotero Web API key from .env")
    status.add_argument("--json", action="store_true")
    add_common(status)
    status.set_defaults(func=cmd_status)

    groups = subcommands.add_parser("groups", help="List Zotero group libraries")
    groups.add_argument("--json", action="store_true")
    add_common(groups)
    groups.set_defaults(func=cmd_groups)

    collections = subcommands.add_parser("collections", help="List Zotero collections")
    collections.add_argument("--json", action="store_true")
    add_common(collections)
    collections.set_defaults(func=cmd_collections)

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

    children = subcommands.add_parser("children", help="List child notes/attachments for a Zotero item")
    children.add_argument("item_key")
    children.add_argument("--json", action="store_true")
    add_common(children)
    children.set_defaults(func=cmd_children)

    upload = subcommands.add_parser("upload-file", help="Upload an imported_file child attachment")
    upload.add_argument("--parent-key", required=True)
    upload.add_argument("--file", required=True)
    upload.add_argument("--title", required=True)
    upload.add_argument("--json", action="store_true")
    add_common(upload)
    upload.set_defaults(func=cmd_upload_file)

    delete = subcommands.add_parser("delete-item", help="Delete one Zotero item using item-version protection")
    delete.add_argument("item_key")
    delete.add_argument("--yes", action="store_true")
    delete.add_argument("--json", action="store_true")
    add_common(delete)
    delete.set_defaults(func=cmd_delete_item)

    citekey = subcommands.add_parser("set-citation-key", help="Pin a Zotero/BibTeX citation key in item Extra")
    citekey.add_argument("item_key")
    citekey.add_argument("citation_key")
    citekey.add_argument("--json", action="store_true")
    add_common(citekey)
    citekey.set_defaults(func=cmd_set_citation_key)

    import_doi = subcommands.add_parser("import-doi", help="Import/find a DOI item and attach full-text evidence")
    import_doi.add_argument("doi")
    import_doi.add_argument("--bib", default=DEFAULT_BIB_PATH)
    import_doi.add_argument("--bibtex-key")
    import_doi.add_argument("--no-bib", action="store_true")
    import_doi.add_argument("--fulltext-url")
    import_doi.add_argument("--fulltext-url-title", default="Full text URL")
    import_doi.add_argument("--attachment-file")
    import_doi.add_argument("--attachment-title", default="Full text attachment")
    import_doi.add_argument("--note")
    import_doi.add_argument("--note-title", default="Full-text access note")
    import_doi.add_argument("--json", action="store_true")
    add_common(import_doi)
    import_doi.set_defaults(func=cmd_import_doi)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
