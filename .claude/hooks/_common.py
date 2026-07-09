"""Shared helpers for Claude Code hooks (T1DM Niteliksel).

Claude Code passes one JSON object on stdin to every command hook. Common
fields: session_id, transcript_path, cwd, hook_event_name. Event-specific
fields: tool_name/tool_input/tool_response (PreToolUse/PostToolUse),
prompt (UserPromptSubmit), stop_hook_active (Stop).

Blocking conventions:
  - exit(2) + message on stderr  -> universal "block / feedback" signal
  - JSON on stdout               -> richer, event-specific decisions
    (hookSpecificOutput.permissionDecision, decision/reason, additionalContext)

Twin implementation: .codex/hooks/ carries the Codex-side equivalents.
Policy changes must land in BOTH trees; tests/test_claude_hooks.py and
tests/test_ai_reliability_hooks.py guard the two surfaces.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any, Dict

# High-precision secret patterns (low false-positive). Shared by the
# UserPromptSubmit gate and the PostToolUse output review.
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


def read_event() -> Dict[str, Any]:
    """Parse the single JSON object Claude Code writes to stdin. Fail-open."""
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Never hard-crash a hook on malformed input: that would block the
        # loop for the wrong reason. Emit nothing and let the session continue.
        return {}


def git_root() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
    except Exception:
        return os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())


def emit_json(obj: Dict[str, Any]) -> None:
    """Write a JSON decision to stdout and exit 0."""
    sys.stdout.write(json.dumps(obj))
    sys.exit(0)


def block(reason: str) -> None:
    """Universal block: exit code 2 with reason on stderr."""
    sys.stderr.write(reason)
    sys.exit(2)


def allow() -> None:
    sys.exit(0)
