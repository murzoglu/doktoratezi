#!/usr/bin/env python3
"""PostToolUse hook (Katman 1: deterministik kapı).

Bash komutu ÇALIŞTIKTAN sonra devreye girer. Yan etkiyi geri alamaz ama:
  1. Çıktıdaki yüksek-güvenli sır sızıntılarını işaretler (redaksiyon uyarısı).
  2. Bariz hata imzalarını (Traceback, FATAL, segfault) modele geri bildirir.

Geri bildirim sözleşmesi: hookSpecificOutput.additionalContext.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SECRET_PATTERNS, git_root, read_event  # noqa: E402

ERROR_SIGNATURES = ("Traceback (most recent call last)", "FATAL:", "segfault")

_WRITE_TOOLS = {"Write", "Edit", "MultiEdit"}


def _is_bib_target(event: dict) -> bool:
    """Write/Edit hedefi references/references.bib mi? (bib yazma-zamanı kapısı)"""
    if event.get("tool_name") not in _WRITE_TOOLS:
        return False
    ti = event.get("tool_input") or {}
    fp = (ti.get("file_path") or ti.get("filePath") or "").replace("\\", "/")
    return fp.endswith("references/references.bib") or fp.endswith("/references.bib") \
        or fp == "references.bib"


def bib_gate(event: dict) -> str | None:
    """references.bib düzenlendiyse bib_hygiene HARD'ını turn-içi geri-bildir.

    Etüt madde C: references.bib'e yazma-zamanı kapısı yoktu → tanımsız/yanlış
    atıf sızabiliyordu. PreToolUse düzenleme-sonrası içeriği göremediğinden kapı
    PostToolUse'da (düzenleme diske indikten sonra) `bib_hygiene.py all` koşar;
    HARD (tanımsız atıf → render kırar) varsa modele geri-bildirir. Fail-open.
    """
    if not _is_bib_target(event):
        return None
    root = git_root()
    tool = os.path.join(root, "scripts", "util", "bib_hygiene.py")
    if not os.path.exists(tool):
        return None
    try:
        proc = subprocess.run(
            [sys.executable, tool, "all"], cwd=root,
            capture_output=True, text=True, timeout=180,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except Exception:
        return None  # fail-open: kapıyı asla wedge etme
    if proc.returncode == 1:  # HARD
        out = (proc.stdout or "") + (proc.stderr or "")
        hard = len(re.findall(r"\bHARD\b", out))
        return (
            f"references.bib düzenlendi; bib_hygiene HARD={hard} (tanımsız/"
            "çözümsüz atıf render'ı kırar). /referans-kapisi ile kapatın ve "
            "referans-denetim-ledgeri.md'de cite-ok satırını doğrulayın."
        )
    return None


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

    bib_msg = bib_gate(event)
    if bib_msg:
        sys.stdout.write(json.dumps({"decision": "block", "reason": bib_msg}))
        sys.exit(0)

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
