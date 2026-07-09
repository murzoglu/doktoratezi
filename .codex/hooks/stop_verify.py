#!/usr/bin/env python3
"""Stop hook (Layers 0+2: grounding + claim verification gate).

When a turn ends, inspect the assistant's final message. By default it runs a
fast, dependency-free check: any numeric/quantitative claim that lacks a nearby
source marker (URL, DOI, arXiv id, citation) triggers a continuation asking the
agent to add sources. Set RELIABILITY_DEEP_VERIFY=1 to additionally route the
message through reliability/verify (Lynx / RAGAS / semantic entropy) — heavier
and needs a configured backend.

Stop contract: JSON on stdout. {"decision":"block","reason":...} does NOT
reject the turn — it continues Codex with `reason` as a new user prompt. We
guard against infinite loops with `stop_hook_active`.
"""
from __future__ import annotations
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event  # noqa: E402

NUMERIC_CLAIM = re.compile(r"\b\d+(?:[.,]\d+)?\s?%|\b\d{4}\b|\$\s?\d|\b\d+(?:[.,]\d+)?\s?(mg|ml|kg|mmol|patients|hastada|aile|cocuk|çocuk|katilimci|katılımcı|satir|satır|sutun|sütun)\b", re.IGNORECASE)
SOURCE_MARKER = re.compile(r"https?://|doi\.org|arxiv|\bPMID\b|\[\d+\]|\(20\d\d\)", re.IGNORECASE)


def main() -> None:
    event = read_event()

    # Avoid loops: if we already forced a continuation this turn, let it stop.
    if event.get("stop_hook_active"):
        sys.stdout.write(json.dumps({"continue": True}))
        sys.exit(0)

    msg = event.get("last_assistant_message") or ""

    # Fast, local grounding check.
    sentences = re.split(r"(?<=[.!?])\s+", msg)
    unsourced = [
        s for s in sentences
        if NUMERIC_CLAIM.search(s) and not SOURCE_MARKER.search(s)
    ]

    if os.environ.get("RELIABILITY_DEEP_VERIFY") == "1":
        try:
            root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            sys.path.insert(0, root)
            from reliability.verify.claim_check import verify_message  # type: ignore
            verdict = verify_message(msg)
            if not verdict.get("ok", True):
                sys.stdout.write(json.dumps({
                    "decision": "block",
                    "reason": "Verification gate: " + verdict.get("reason", "claims unsupported by sources.")
                }))
                sys.exit(0)
        except Exception:
            pass  # fail-open: never wedge the loop on a verifier error

    if unsourced:
        preview = unsourced[0][:160]
        sys.stdout.write(json.dumps({
            "decision": "block",
            "reason": (
                "Verification gate: the following quantitative claim has no "
                f"source marker — add a primary source or remove it: \"{preview}\""
            ),
        }))
        sys.exit(0)

    sys.stdout.write(json.dumps({"continue": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
