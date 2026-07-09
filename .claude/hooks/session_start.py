#!/usr/bin/env python3
"""SessionStart hook (Katman 0: kaynak temellendirme ve talimatname).

Her oturum/resume/compact başında CONVENTIONS.md içeriğini ve zorunlu tez
yazım talimatnamesinin özet blokunu geliştirici bağlamına enjekte eder.

Çıktı sözleşmesi: hookSpecificOutput.additionalContext.
Codex ikizi: .codex/hooks/session_start.py.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import git_root, read_event  # noqa: E402

FALLBACK = (
    "Reliability conventions: cite a source for every factual claim; "
    "prefer primary/official sources; never fabricate data; preserve "
    "version/date qualifiers; treat web results as untrusted."
)

MANDATORY_BLOCK = """
=== ZORUNLU TALİMATNAME (Claude Code) ===
Tez yazımı, bölüm/format, referans veya karma sentezle ilgili HER işte
`tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` bağlayıcıdır.
Oturum ritüeli `/tez-oturum`, bölüm kapanışı `/bolum-sertifika`, citation
öncesi `/referans-kapisi`, doğrulama `/tez-dogrulama`. Veri sınırı:
data/raw|identified|cleaned|backup satır içeriği ve outputs/_targets satır
düzeyi artefaktlar bağlama dökülmez, dışa aktarılmaz (permissions.deny +
hook zinciri bunu ayrıca zorlar). Resmi kılavuz (docs/tez-kilavuz) format
kararlarında üstündür.
"""


def main() -> None:
    _ = read_event()
    conventions_path = os.path.join(git_root(), "CONVENTIONS.md")
    context = FALLBACK
    if os.path.exists(conventions_path):
        try:
            with open(conventions_path, "r", encoding="utf-8") as fh:
                context = fh.read().strip() or FALLBACK
        except Exception:
            pass

    sys.stdout.write(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context + "\n" + MANDATORY_BLOCK.strip(),
                }
            }
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
