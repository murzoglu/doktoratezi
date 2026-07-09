"""Lynx faithfulness check — RAG context-faithfulness verdict.

Lynx is an open-source hallucination-evaluation model:
  Ravi, S.S. et al. (2024) "Lynx: An Open Source Hallucination Evaluation
  Model." arXiv:2407.08488.  Open weights:
  https://huggingface.co/PatronusAI/Llama-3-Patronus-Lynx-70B-Instruct
  (an 8B variant also exists for sub-second/self-host use).

Given (question, retrieved_context, answer), Lynx returns PASS/FAIL plus a
reasoning trace for whether the answer is faithful to the context.

Three backends, selected by env var (most-private first):
  LYNX_BACKEND=local    -> local HF/vLLM endpoint at LYNX_ENDPOINT  (self-host)
  LYNX_BACKEND=ollama   -> local Ollama model (LYNX_OLLAMA_MODEL)
  LYNX_BACKEND=patronus -> Patronus hosted API (PATRONUS_API_KEY)

All backends are optional. With none configured this returns {"configured": False}
so callers can fail-open instead of crashing.
"""
from __future__ import annotations
import json
import os
import urllib.request

PROMPT = """You are evaluating whether an ANSWER is faithful to the CONTEXT for a QUESTION.
Respond with strict JSON: {{"score": "PASS"|"FAIL", "reasoning": "<one sentence>"}}.
QUESTION: {q}
CONTEXT: {c}
ANSWER: {a}"""


def _post_json(url: str, payload: dict, headers: dict, timeout: int = 60) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def check_faithfulness(question: str, context: str, answer: str) -> dict:
    backend = os.environ.get("LYNX_BACKEND")
    prompt = PROMPT.format(q=question, c=context, a=answer)

    if backend == "local":
        endpoint = os.environ["LYNX_ENDPOINT"]  # OpenAI-compatible /v1/chat/completions
        out = _post_json(
            endpoint,
            {"model": os.environ.get("LYNX_MODEL", "patronus-lynx"),
             "messages": [{"role": "user", "content": prompt}], "temperature": 0},
            {"Content-Type": "application/json",
             "Authorization": f"Bearer {os.environ.get('LYNX_API_KEY', 'none')}"},
        )
        return _parse(out["choices"][0]["message"]["content"])

    if backend == "ollama":
        out = _post_json(
            os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate"),
            {"model": os.environ.get("LYNX_OLLAMA_MODEL", "patronus-lynx"),
             "prompt": prompt, "stream": False, "format": "json"},
            {"Content-Type": "application/json"},
        )
        return _parse(out.get("response", "{}"))

    if backend == "patronus":
        # Placeholder for the hosted evaluator call; consult Patronus docs for
        # the current endpoint/payload. Requires PATRONUS_API_KEY.
        return {"configured": True, "backend": "patronus",
                "note": "Wire the hosted evaluate() call per Patronus API docs."}

    return {"configured": False, "note": "Set LYNX_BACKEND to enable Lynx checks."}


def _parse(text: str) -> dict:
    try:
        obj = json.loads(text)
        return {"configured": True, "score": obj.get("score"),
                "reasoning": obj.get("reasoning")}
    except Exception:
        return {"configured": True, "score": "UNKNOWN", "raw": text[:300]}
