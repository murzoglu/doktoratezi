"""Claim verification orchestrator (Layer 2).

`verify_message` is the single entry point used by the Stop hook and by CI.
It runs a cheap, always-available grounding check, then escalates to the
configured heavy verifiers (Lynx / RAGAS) only when context is supplied and a
backend is wired. Returns {"ok": bool, "reason": str, "signals": {...}}.

Design principle: fail-open on infrastructure errors (never wedge the agent
loop), fail-closed only on a *confident* grounding failure.
"""
from __future__ import annotations
import os
import re
import sys
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from reliability.verify.lynx_client import check_faithfulness  # noqa: E402
from reliability.verify.ragas_faithfulness import faithfulness_score  # noqa: E402

NUMERIC = re.compile(r"\b\d+(?:[.,]\d+)?\s?%|\$\s?\d|\b\d+(?:[.,]\d+)?\s?(mg|ml|kg|mmol|patients|hastada|aile(?:den)?|görüşme|gorusme|kod|(?:makro\s+)?tema|madde(?:si)?|cocuk|çocuk|katilimci|katılımcı|satir|satır|sutun|sütun)\b", re.IGNORECASE)
SOURCE = re.compile(r"https?://|doi\.org|arxiv|\bPMID\b|\[\d+\]|\(20\d\d\)", re.IGNORECASE)
RAGAS_FLOOR = float(os.environ.get("RAGAS_FAITHFULNESS_FLOOR", "0.7"))


def verify_message(
    answer: str,
    question: str = "",
    contexts: Optional[List[str]] = None,
) -> dict:
    signals: dict = {}

    # 1. Cheap local grounding: unsourced quantitative claims.
    sentences = re.split(r"(?<=[.!?])\s+", answer)
    unsourced = [s for s in sentences if NUMERIC.search(s) and not SOURCE.search(s)]
    signals["unsourced_numeric_claims"] = len(unsourced)

    # 2. RAGAS faithfulness (only if context supplied and ragas installed).
    if contexts:
        score = faithfulness_score(question, answer, contexts)
        if score is not None:
            signals["ragas_faithfulness"] = round(score, 3)
            if score < RAGAS_FLOOR:
                return {"ok": False,
                        "reason": f"RAGAS faithfulness {score:.2f} < floor {RAGAS_FLOOR}.",
                        "signals": signals}

        # 3. Lynx PASS/FAIL (only if a backend is configured).
        lynx = check_faithfulness(question, "\n".join(contexts), answer)
        signals["lynx"] = lynx
        if lynx.get("configured") and lynx.get("score") == "FAIL":
            return {"ok": False,
                    "reason": "Lynx flagged the answer as unfaithful to context.",
                    "signals": signals}

    if unsourced:
        return {"ok": False,
                "reason": f"{len(unsourced)} quantitative claim(s) lack a source marker.",
                "signals": signals}

    return {"ok": True, "reason": "passed grounding checks", "signals": signals}


if __name__ == "__main__":
    import json
    print(json.dumps(verify_message(
        "Lynx outperformed GPT-4o by 8.3% on PubMedQA.", ), indent=2))
