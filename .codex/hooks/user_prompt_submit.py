#!/usr/bin/env python3
"""UserPromptSubmit hook (Layer 1: deterministic gate).

Scans the prompt about to be sent for high-confidence secret patterns
(API keys, private keys, tokens). If found, BLOCKS the prompt so the secret
never reaches the model or any logging backend.

This is the canonical "scan prompts to block accidentally pasting API keys"
use case from the Codex hooks docs.

Block contract: exit code 2 + reason on stderr (also accepts the JSON
{"decision":"block","reason":...} shape).
"""
from __future__ import annotations
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event, block, allow  # noqa: E402

# High-precision patterns (low false-positive). Extend for your stack.
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
    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "Private key block"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", "JWT"),
]


def main() -> None:
    event = read_event()
    prompt = event.get("prompt", "") or ""
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, prompt):
            block(
                f"Blocked: prompt appears to contain a secret ({label}). "
                "Remove the credential before sending. Rotate it if it was real."
            )
    allow()


if __name__ == "__main__":
    main()
