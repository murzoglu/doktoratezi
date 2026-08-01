#!/usr/bin/env python3
"""Stop hook (Katman 0+2: temellendirme + iddia doğrulama kapısı).

Tur biterken asistanın son mesajını inceler: yakınında kaynak işareti
(URL, DOI, PMID, atıf yılı, repo dosya yolu) olmayan sayısal/nicel iddia
varsa turu sürdürüp kaynak ister. Claude Code son mesajı event'e koymayabilir;
bu durumda transcript JSONL'inden okunur. Repo dosya yolu kaynak sayılır.

RELIABILITY_DEEP_VERIFY=1 ile reliability/verify derin katmanı da çalışır.
Codex ikizi: .codex/hooks/stop_verify.py.

Stop sözleşmesi: {"decision":"block","reason":...} turu reddetmez; reason ile
devam ettirir. stop_hook_active sonsuz döngüyü keser.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event  # noqa: E402

NUMERIC_CLAIM = re.compile(
    r"\b\d+(?:[.,]\d+)?\s?%|\b\d{4}\b|\$\s?\d|\b\d+(?:[.,]\d+)?\s?"
    r"(mg|ml|kg|mmol|patients|hastada|aile(?:den)?|cocuk|çocuk|katilimci|"
    r"katılımcı|satir|satır|sutun|sütun)\b",
    re.IGNORECASE,
)
SOURCE_MARKER = re.compile(
    r"https?://|doi\.org|arxiv|\bPMID\b|\[\d+\]|\(20\d\d\)|"
    r"[\w./~-]+\.(?:md|csv|tsv|py|R|qmd|Rmd|bib|ya?ml|json|toml|pdf|docx)\b|"
    r"`[^`]*[/.][^`]*`",
    re.IGNORECASE,
)
# §1.4 Marmara ondalık virgül: gövde metninde nokta-ondalık p değeri (p=0.NNN)
# turn-end'de bloklanır. sci-audit axis-G tr-pvalue blocker'ının turn-end
# muadili (plugin Stop hook'u bu repoda ayrı ateşlenmeyebilir).
PVALUE_DOT = re.compile(r"\bp\s*[=<>]\s*0\.\d", re.IGNORECASE)


def last_assistant_message(event: dict) -> str:
    msg = event.get("last_assistant_message")
    if isinstance(msg, str) and msg.strip():
        return msg
    transcript = event.get("transcript_path") or ""
    if not transcript or not os.path.exists(transcript):
        return ""
    try:
        with open(transcript, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except Exception:
        return ""
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") != "assistant":
            continue
        message = entry.get("message") or {}
        content = message.get("content")
        texts: list[str] = []
        if isinstance(content, str):
            texts.append(content)
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    texts.append(part.get("text") or "")
        joined = "\n".join(t for t in texts if t.strip())
        if joined.strip():
            return joined
    return ""


def main() -> None:
    event = read_event()

    if event.get("stop_hook_active"):
        sys.stdout.write(json.dumps({"continue": True}))
        sys.exit(0)

    msg = last_assistant_message(event)

    if PVALUE_DOT.search(msg):
        m = PVALUE_DOT.search(msg)
        sys.stdout.write(json.dumps({
            "decision": "block",
            "reason": (
                "§1.4 kapısı: nokta-ondalık p değeri (\"%s...\") — Marmara "
                "ondalık virgül kuralı gereği p=0,NNN yazın (nokta değil virgül)."
                % msg[m.start():m.start() + 12]
            ),
        }))
        sys.exit(0)

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
            pass  # fail-open

    if unsourced:
        preview = unsourced[0][:160]
        sys.stdout.write(json.dumps({
            "decision": "block",
            "reason": (
                "Verification gate: the following quantitative claim has no "
                "source marker — add a primary source, a repo file path, or "
                f"remove it: \"{preview}\""
            ),
        }))
        sys.exit(0)

    sys.stdout.write(json.dumps({"continue": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
