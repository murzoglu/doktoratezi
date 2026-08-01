#!/usr/bin/env python3
"""PreToolUse hook (Layer 1: deterministic gate / guardrail).

Intercepts Bash commands BEFORE execution and denies a deny-list of
destructive operations. Codex's PreToolUse currently intercepts only the Bash
tool, and the model can still write a script to disk and run it, so treat this
as a high-value guardrail, NOT a complete enforcement boundary.

Deny contract: structured permissionDecision=deny (preferred) — Codex also
accepts exit code 2 + reason on stderr.
"""
from __future__ import annotations
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event  # noqa: E402

# --- Three-tier data governance (owner-approved revision 2026-07-13) ---
# Tier 1: PII/pre-cleaning source files — analysis never needs these; hard-block.
PII_SOURCE_PATH = r"\bdata/(raw|identified|cleaned|backup)(/|\b)"
# Tier 2: de-identified analysis surface (canonical processed base + aggregate
# outputs + targets store). Owner-authorized for R/python read + compute
# (de-identification completed in Stage 1) — absent from interpreter/display rules.
ANALYSIS_SURFACE_PATH = r"(\bdata/processed(/|\b)|\boutputs/|\b_targets(/|\b))"
# Tier 3: any study data — used only by the exfiltration guard (copy/archive/encode).
ANY_DATA_PATH = rf"({PII_SOURCE_PATH}|{ANALYSIS_SURFACE_PATH})"
CREDENTIAL_PATH = r"(^|[\s'\"=])(\.env(?:\.[\w-]+)?|[^\s'\";|&]*(credentials|client_secret|dr-murzoglu-doktora\.json)[^\s'\";|&]*)"

# Each entry: (compiled regex, human reason). Tune to your environment.
DENY_RULES = [
    # rm with BOTH recursive and force flags (any order: -rf, -fr, -r -f, ...)
    # targeting an absolute path, home, or glob. Relative paths (e.g. build/)
    # are intentionally allowed.
    (re.compile(r"\brm\s+-\w*[rf]\w*[rf]\w*\b[^|;&\n]*\s+(/[^\s]*|~|\*|\$HOME)(\s|$)"),
     "Recursive force-delete of an absolute/home/glob path"),
    (re.compile(r"\bgit\s+push\b.*--force(?!-with-lease)"), "Non-lease force push"),
    (re.compile(r"\bgit\s+push\b.*\b(main|master|release)\b.*--force"), "Force push to a protected branch"),
    (re.compile(r"\b(DROP|TRUNCATE)\s+TABLE\b", re.IGNORECASE), "Destructive SQL DDL"),
    (re.compile(r"\bDELETE\s+FROM\b(?!.*\bWHERE\b)", re.IGNORECASE), "Unbounded SQL DELETE (no WHERE)"),
    (re.compile(r"\b(mkfs|dd)\b.*\bof=/dev/"), "Raw device write / format"),
    (re.compile(r":\(\)\s*\{\s*:\|:&\s*\}\s*;:"), "Fork bomb"),
    (re.compile(r"\bcurl\b.*\|\s*(sudo\s+)?(bash|sh)\b"), "Piping remote script straight into a shell"),
    (re.compile(r"\bchmod\s+(-R\s+)?777\b"), "World-writable (777) chmod"),
    (re.compile(r"\bgh\s+repo\s+delete\b"), "GitHub repo deletion"),
    (re.compile(r"\bgit\s+add\s+(\.|-A|--all)(\s|$)"), "Broad staging; stage files by name"),
    (re.compile(rf"\b(cat|head|tail|less|more|sed|awk|grep|rg)\b[^|;&\n]*{PII_SOURCE_PATH}", re.IGNORECASE),
     "Direct shell display/search of PII source data (data/raw|identified|cleaned|backup)"),
    (re.compile(rf"\b(cat|head|tail|less|more|sed|awk|grep|rg)\b[^|;&\n]*{CREDENTIAL_PATH}", re.IGNORECASE),
     "Direct shell display/search of credentials or environment files"),
    (re.compile(rf"\b(python3?|Rscript|R\s+-e|node|ruby|perl)\b[^|;&\n]*({PII_SOURCE_PATH}|{CREDENTIAL_PATH})", re.IGNORECASE),
     "Interpreter command touches PII source data or credentials"),
    (re.compile(rf"\b(cp|scp|rsync|tar|zip|7z|gzip|xz|base64)\b[^|;&\n]*({ANY_DATA_PATH}|{CREDENTIAL_PATH})", re.IGNORECASE),
     "Copy/archive/encode of study data or credentials (exfiltration guard)"),
]


def extract_command(event: dict) -> str:
    candidates: list[str] = []

    def add(value: object) -> None:
        if isinstance(value, str) and value.strip():
            candidates.append(value)

    for key in ("command", "cmd"):
        add(event.get(key))

    for key in ("tool_input", "input", "params"):
        value = event.get(key)
        if isinstance(value, str):
            add(value)
        elif isinstance(value, dict):
            for nested_key in ("command", "cmd"):
                add(value.get(nested_key))

    return "\n".join(candidates)


def deny(reason: str) -> None:
    sys.stdout.write(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    sys.exit(0)


def main() -> None:
    event = read_event()
    command = extract_command(event)
    if re.search(r"\bcodex\s+mcp\s+list\b", command) and "codex_mcp_roster_redacted.py" not in command:
        deny(
            "Blocked by reliability policy: raw `codex mcp list` can expose plaintext "
            "tokens embedded in stdio server args. Use "
            "`python3 .codex/tools/codex_mcp_roster_redacted.py` instead."
        )
    for rule, reason in DENY_RULES:
        if rule.search(command):
            deny(f"Blocked by reliability policy: {reason}.")
    sys.exit(0)  # allow (exit 0, no output)


if __name__ == "__main__":
    main()
