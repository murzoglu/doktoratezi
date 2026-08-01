#!/usr/bin/env python3
"""Apply the 9ZFDHMZA organization scheme to the live Zotero thesis library.

DRY-RUN is the DEFAULT. Writes happen ONLY with --apply.
Scope-lock: only creates subcollections under 9ZFDHMZA; only modifies items
returned by the 9ZFDHMZA collection query; add-only (never removes existing
collections or tags).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve scripts/util on sys.path so we can import siblings
# ---------------------------------------------------------------------------
_SCRIPTS_UTIL = Path(__file__).resolve().parent
if str(_SCRIPTS_UTIL) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_UTIL))

import zotero_env_bridge as zb  # noqa: E402
import bib_hygiene  # noqa: E402

THESIS_COLLECTION = "9ZFDHMZA"


# ---------------------------------------------------------------------------
# Helper: normalize a DOI string to bare lowercase
# ---------------------------------------------------------------------------

def _norm_doi(raw: str) -> str:
    doi = (raw or "").strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
    return doi.strip()


# ---------------------------------------------------------------------------
# 1. Offline: load desired scheme keyed by DOI
# ---------------------------------------------------------------------------

def load_desired_by_doi(
    bib_path: str = "references/references.bib",
) -> dict[str, dict]:
    """Parse bib, run desired_scheme; return doi.lower() -> {"subcollection", "tags"}.

    Only entries that carry a doi field are included.  Offline -- no network.
    """
    text = Path(bib_path).read_text(encoding="utf-8")
    entries = bib_hygiene.parse_bib(text)
    scheme_by_key = bib_hygiene.desired_scheme(entries)

    fields_by_key: dict[str, dict] = {e["key"]: e["fields"] for e in entries}

    result: dict[str, dict] = {}
    for key, scheme_val in scheme_by_key.items():
        fields = fields_by_key.get(key, {})
        raw_doi = fields.get("doi", "")
        doi = _norm_doi(raw_doi)
        if doi:
            result[doi] = {
                "subcollection": scheme_val["subcollection"],
                "tags": scheme_val["tags"],
            }
    return result


# ---------------------------------------------------------------------------
# 2. Pure: build plan
# ---------------------------------------------------------------------------

def build_plan(desired_by_doi: dict[str, dict], items: list[dict]) -> dict:
    """PURE function -- build an org plan from desired-by-doi and live items.

    Args:
        desired_by_doi: doi.lower() -> {"subcollection": str, "tags": list[str]}
        items: list of Zotero item dicts (each has item["data"])

    Returns a dict with:
        "subcollections": sorted list of distinct subcollection names
        "assignments": list of assignment dicts per item
        "matched": count of items matched by DOI
        "unmatched_by_doi": count of items NOT matched (defaulted to Genel/t1dm)
    """
    assignments: list[dict] = []
    matched = 0
    unmatched_by_doi = 0

    for item in items:
        data = item.get("data", item)
        item_key = data.get("key", "")
        title = data.get("title", "")
        doi = _norm_doi(data.get("DOI") or "")

        existing_tags_set = {t["tag"] for t in (data.get("tags") or [])}

        if doi and doi in desired_by_doi:
            scheme_val = desired_by_doi[doi]
            subcollection = scheme_val["subcollection"]
            wanted_tags: list[str] = scheme_val["tags"]
            matched += 1
        else:
            subcollection = "Genel"
            wanted_tags = ["t1dm"]
            unmatched_by_doi += 1

        add_tags = [t for t in wanted_tags if t not in existing_tags_set]

        assignments.append({
            "item_key": item_key,
            "title": title,
            "subcollection": subcollection,
            "add_tags": add_tags,
            # already_in_sub requires knowing the subcollection key which is
            # resolved at apply time; set False here for the plan.
            "already_in_sub": False,
        })

    subcollections = sorted({a["subcollection"] for a in assignments})

    return {
        "subcollections": subcollections,
        "assignments": assignments,
        "matched": matched,
        "unmatched_by_doi": unmatched_by_doi,
    }


# ---------------------------------------------------------------------------
# 3. I/O: fetch items from 9ZFDHMZA collection
# ---------------------------------------------------------------------------

def fetch_thesis_items(ctx) -> list[dict]:
    """Paginate through all items in the 9ZFDHMZA collection."""
    uid = ctx.user_id
    items: list[dict] = []
    start = 0
    limit = 100
    while True:
        path = (
            f"/users/{uid}/collections/{THESIS_COLLECTION}"
            f"/items/top?limit={limit}&start={start}"
        )
        data, resp_headers, _text = zb.request(ctx, path)
        if isinstance(data, list):
            items.extend(data)
        # Total-Results header key may be capitalised differently by urllib
        total = 0
        for hk, hv in resp_headers.items():
            if hk.lower() == "total-results":
                try:
                    total = int(hv)
                except ValueError:
                    pass
                break
        start += limit
        if not total or start >= total:
            break
    return items


# ---------------------------------------------------------------------------
# 4. I/O: apply plan (called ONLY under --apply)
# ---------------------------------------------------------------------------

def apply_plan(ctx, plan: dict, items: list[dict]) -> dict:
    """Apply the plan to the live Zotero library.  ONLY called under --apply.

    ADD-only: preserves existing collections and tags; only adds the target
    subcollection key and new tags.

    Scope-lock: only creates subcollections whose parentCollection == 9ZFDHMZA,
    only modifies items returned by the 9ZFDHMZA query.

    Returns counts dict: subcollections_created, items_updated, skipped.
    """
    uid = ctx.user_id

    # GET existing subcollections of 9ZFDHMZA (paginated, like fetch_thesis_items)
    existing_subs: dict[str, str] = {}  # name -> key
    sub_start = 0
    sub_limit = 100
    while True:
        path = (
            f"/users/{uid}/collections/{THESIS_COLLECTION}/collections"
            f"?limit={sub_limit}&start={sub_start}"
        )
        data, sub_headers, _text = zb.request(ctx, path)
        if isinstance(data, list):
            for col in data:
                col_data = col.get("data", col)
                name = col_data.get("name", "")
                col_key = col_data.get("key", "") or col.get("key", "")
                if name and col_key:
                    existing_subs[name] = col_key
        sub_total = 0
        for hk, hv in sub_headers.items():
            if hk.lower() == "total-results":
                try:
                    sub_total = int(hv)
                except ValueError:
                    pass
                break
        sub_start += sub_limit
        if not sub_total or sub_start >= sub_total:
            break

    # Create missing subcollections (parentCollection == 9ZFDHMZA always)
    subcollections_created = 0
    for sub_name in plan["subcollections"]:
        if sub_name in existing_subs:
            continue
        body = json.dumps(
            [{"name": sub_name, "parentCollection": THESIS_COLLECTION}],
            ensure_ascii=False,
        ).encode("utf-8")
        resp, _h, _t = zb.request(
            ctx,
            f"/users/{uid}/collections",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"},
        )
        if isinstance(resp, dict):
            for _idx, col_obj in (resp.get("successful") or {}).items():
                if not isinstance(col_obj, dict):
                    continue
                col_data = col_obj.get("data", col_obj)
                created_name = col_data.get("name", sub_name)
                created_key = col_data.get("key", "") or col_obj.get("key", "")
                if created_name and created_key:
                    existing_subs[created_name] = created_key
                    subcollections_created += 1

    # Index items by key for fast lookup
    items_by_key: dict[str, dict] = {}
    for item in items:
        item_data = item.get("data", item)
        k = item_data.get("key", "")
        if k:
            items_by_key[k] = item

    items_updated = 0
    skipped = 0

    for assignment in plan["assignments"]:
        item_key = assignment["item_key"]
        target_sub_name = assignment["subcollection"]
        add_tags = assignment["add_tags"]

        target_sub_key = existing_subs.get(target_sub_name)
        if not target_sub_key:
            print(
                f"WARNING: '{target_sub_name}' alt-koleksiyon anahtarı çözülemedi"
                " — bu gruba item eklenmedi",
                file=sys.stderr,
            )
            skipped += 1
            continue

        item = items_by_key.get(item_key)
        if not item:
            skipped += 1
            continue

        item_data = item.get("data", item)
        existing_collections: list[str] = list(item_data.get("collections") or [])
        existing_tags: list[dict] = list(item_data.get("tags") or [])

        # ADD-only
        new_collections = list(dict.fromkeys(existing_collections + [target_sub_key]))
        existing_tag_names = {t["tag"] for t in existing_tags}
        new_tags = existing_tags + [
            {"tag": t} for t in add_tags if t not in existing_tag_names
        ]

        # Skip if nothing would change
        if (
            sorted(new_collections) == sorted(existing_collections)
            and len(new_tags) == len(existing_tags)
        ):
            skipped += 1
            continue

        zb.patch_item(
            ctx,
            item_key,
            {"collections": new_collections, "tags": new_tags},
        )
        items_updated += 1

    return {
        "subcollections_created": subcollections_created,
        "items_updated": items_updated,
        "skipped": skipped,
    }


# ---------------------------------------------------------------------------
# 5. main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Apply 9ZFDHMZA Zotero organization scheme.  "
            "DRY-RUN by default; pass --apply to write."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Write changes to Zotero (default: dry-run, read-only).",
    )
    parser.add_argument(
        "--bib",
        default="references/references.bib",
        help="Path to references.bib (default: references/references.bib)",
    )
    args = parser.parse_args(argv)

    # Offline: load desired scheme
    desired_by_doi = load_desired_by_doi(args.bib)

    # Build Zotero context (reads ZOTERO_API_KEY from env/.env)
    ctx = zb.build_context(argparse.Namespace(env_file=None))
    ctx = zb.context_with_user(ctx)

    # Fetch live items from the thesis collection
    items = fetch_thesis_items(ctx)

    # Build plan (pure)
    plan = build_plan(desired_by_doi, items)

    if not args.apply:
        # DRY-RUN: print summary, no writes
        sub_counts: dict[str, int] = {}
        for a in plan["assignments"]:
            sub_counts[a["subcollection"]] = sub_counts.get(a["subcollection"], 0) + 1

        print("=== DRY-RUN -- no writes ===")
        print(f"\nTotal items in {THESIS_COLLECTION}: {len(items)}")
        print(f"Matched by DOI:          {plan['matched']}")
        print(f"Unmatched (-> Genel):    {plan['unmatched_by_doi']}")
        print(f"\nSubcollections to ensure ({len(plan['subcollections'])}):")
        for sub in plan["subcollections"]:
            print(f"  {sub!r:<42} {sub_counts.get(sub, 0)} items")
        print("\nDRY-RUN -- no writes performed.")
        return 0

    # --apply path (writes)
    result = apply_plan(ctx, plan, items)
    print(f"subcollections_created: {result['subcollections_created']}")
    print(f"items_updated:          {result['items_updated']}")
    print(f"skipped:                {result['skipped']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
