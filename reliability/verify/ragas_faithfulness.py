"""RAGAS faithfulness wrapper (claim-to-context grounding score).

RAGAS decomposes an answer into atomic claims and checks each against the
retrieved context, returning a faithfulness score in [0, 1]. Requires a judge
LLM and embeddings configured per RAGAS docs (https://docs.ragas.io).

Install:  pip install ragas datasets
This wrapper degrades gracefully if ragas is not installed.
"""
from __future__ import annotations
from typing import List, Optional


def faithfulness_score(
    question: str,
    answer: str,
    contexts: List[str],
) -> Optional[float]:
    """Return a faithfulness score in [0,1], or None if RAGAS is unavailable."""
    try:
        from ragas import evaluate
        from ragas.metrics import faithfulness
        from datasets import Dataset
    except Exception:
        return None

    ds = Dataset.from_dict(
        {"question": [question], "answer": [answer], "contexts": [contexts]}
    )
    result = evaluate(ds, metrics=[faithfulness])
    try:
        return float(result["faithfulness"])
    except Exception:
        return None
