"""Shared helpers for Codex hooks.

Codex passes one JSON object on stdin to every command hook. Common fields:
  session_id, transcript_path, cwd, hook_event_name, model
Turn-scoped events (PreToolUse/PostToolUse/UserPromptSubmit/Stop) also carry:
  turn_id
Event-specific fields are documented at https://developers.openai.com/codex/hooks

Blocking conventions used here:
  - exit(2) + message on stderr  -> universal "block / feedback" signal
  - JSON on stdout               -> richer, event-specific decisions
"""
from __future__ import annotations
import json
import sys
from typing import Any, Dict


def read_event() -> Dict[str, Any]:
    """Parse the single JSON object Codex writes to stdin. Fail-open on junk."""
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Never hard-crash a hook on malformed input: that would block the loop
        # for the wrong reason. Emit nothing and let Codex continue.
        return {}


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
