#!/usr/bin/env python3
"""UserPromptSubmit hook (Katman 1: deterministik kapı).

Gönderilmek üzere olan prompt'u yüksek-güvenli sır kalıplarına (API anahtarı,
private key, token) karşı tarar. Bulursa prompt'u BLOKLAR; sır modele veya
log backend'ine hiç ulaşmaz.

Blok sözleşmesi: exit code 2 + stderr'e gerekçe.
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SECRET_PATTERNS, allow, block, read_event  # noqa: E402


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
