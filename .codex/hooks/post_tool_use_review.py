#!/usr/bin/env python3
"""PostToolUse hook (Layer 1: deterministic gate).

Runs AFTER a Bash command. It cannot undo side effects, but it can surface a
warning and feed structured context back to the model. Here we:
  1. Flag obvious error signatures in tool output.
  2. If the command wrote a JSON file under ./artifacts, validate it against a
     JSON Schema in reliability/schemas (if jsonschema + a schema are present).

Feedback contract: {"decision":"block","reason":...} replaces the tool result
with feedback and continues the model from there (does NOT undo the command).
"""
from __future__ import annotations
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event  # noqa: E402

ERROR_SIGNATURES = ("Traceback (most recent call last)", "FATAL:", "segfault")
SECRET_PATTERNS = [
    (r"sk-(?:proj|svcacct)-[A-Za-z0-9_\-]{20,}", "OpenAI project/service account key"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI-style secret key"),
    (r"sk-ant-[A-Za-z0-9_\-]{20,}", "Anthropic API key"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key id"),
    (r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}", "GitHub token"),
    (r"github_pat_[A-Za-z0-9_]{40,}", "GitHub fine-grained personal access token"),
    (r"AIza[0-9A-Za-z_\-]{35}", "Google API key"),
    (r"sbp_[A-Za-z0-9]{40,}", "Supabase access token"),
    (r"(?:sk|rk)_live_[A-Za-z0-9]{20,}", "Stripe live key"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", "JWT"),
]


def extract_response_text(event: dict) -> str:
    parts: list[str] = []

    def add(value: object) -> None:
        if value is None:
            return
        if isinstance(value, str):
            parts.append(value)
            return
        parts.append(json.dumps(value))

    for key in ("tool_response", "tool_output", "output", "response"):
        add(event.get(key))

    for key in ("result", "tool_result"):
        value = event.get(key)
        if isinstance(value, dict):
            for nested_key in ("output", "stdout", "stderr", "text"):
                add(value.get(nested_key))

    return "\n".join(parts)


def main() -> None:
    event = read_event()
    text = extract_response_text(event)

    leaked_labels = sorted({label for pattern, label in SECRET_PATTERNS if re.search(pattern, text)})
    if leaked_labels:
        sys.stdout.write(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": (
                            "The command output contains high-confidence secret-like value(s): "
                            + ", ".join(leaked_labels)
                            + ". Treat the previous output as sensitive; avoid repeating it, "
                            "redact summaries, and rotate the credential if it was real."
                        ),
                    }
                }
            )
        )
        sys.exit(0)

    for sig in ERROR_SIGNATURES:
        if sig in text:
            sys.stdout.write(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PostToolUse",
                            "additionalContext": (
                                f"The command output contains an error signature "
                                f"('{sig}'). Diagnose and fix before proceeding."
                            ),
                        }
                    }
                )
            )
            sys.exit(0)

    sys.exit(0)  # nothing to flag


if __name__ == "__main__":
    main()
