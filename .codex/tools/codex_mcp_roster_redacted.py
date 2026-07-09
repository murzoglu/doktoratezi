#!/usr/bin/env python3
"""Print `codex mcp list` with high-confidence secrets redacted.

Use this instead of raw `codex mcp list` in this repo. Some stdio MCP servers
can place tokens in command arguments, and the Codex CLI may print those args.
"""

from __future__ import annotations

import re
import subprocess
import sys


REDACTIONS = [
    (re.compile(r"sk-(?:proj|svcacct)-[A-Za-z0-9_\-]{20,}"), "sk-proj-[REDACTED]"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "sk-[REDACTED]"),
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"), "sk-ant-[REDACTED]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AKIA[REDACTED]"),
    (re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}"), "ghp_[REDACTED]"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{40,}"), "github_pat_[REDACTED]"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "AIza[REDACTED]"),
    (re.compile(r"sbp_[A-Za-z0-9]{40,}"), "sbp_[REDACTED]"),
    (re.compile(r"(?:sk|rk)_live_[A-Za-z0-9]{20,}"), "live_[REDACTED]"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "xox[REDACTED]"),
    (
        re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
        "jwt_[REDACTED]",
    ),
]


def redact(text: str) -> str:
    for pattern, replacement in REDACTIONS:
        text = pattern.sub(replacement, text)
    return text


def main() -> int:
    proc = subprocess.run(
        ["codex", "mcp", "list"],
        text=True,
        capture_output=True,
        check=False,
    )
    sys.stdout.write(redact(proc.stdout))
    sys.stderr.write(redact(proc.stderr))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
