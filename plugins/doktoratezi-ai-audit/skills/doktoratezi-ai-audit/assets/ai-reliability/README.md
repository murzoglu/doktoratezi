# AI Reliability scaffold for a Codex repo

A drop-in scaffold that wires the **seven-layer reliability architecture** we
designed (consistency, accuracy, error-catchability) into a single Codex
project. No layer alone is sufficient; the value is in the combination.

> Honest framing: no tool guarantees error-freeness. LLM agents are
> probabilistic; even RAG does not eliminate unfaithfulness. The goal is
> defense-in-depth that drives the error rate down and makes residual errors
> **catchable and traceable**.

## One command

```bash
./setup.sh                 # wire into the current git repo
./setup.sh --global        # + install hooks for all repos (~/.codex)
./setup.sh --observability  # + start self-hosted Langfuse
```

Then, inside Codex once: run `/hooks` and **trust** the hooks (required because
hooks are trusted explicitly, and are experimental + disabled on Windows).

## Layer → file → purpose

| Layer | Where | What it does |
|---|---|---|
| 0 Source grounding & provenance | `CONVENTIONS.md`, `.codex/hooks/session_start.py` | Injects citation/primary-source/freshness discipline every session |
| 1 Deterministic gates & hooks | `.codex/config.toml`, `.codex/hooks/{user_prompt_submit,pre_tool_use_policy,post_tool_use_review}.py` | Pin model + reasoning effort; block secret pastes; deny destructive Bash; review output |
| 2 Claim verification | `reliability/verify/{claim_check,semantic_entropy,lynx_client,ragas_faithfulness}.py`, `.codex/hooks/stop_verify.py` | Decompose + check claims against sources; semantic-entropy & Lynx & RAGAS |
| 3 Triangulation | (pattern) verifier agent of a different model family reading `claim_check` | Break shared blind spots between generator and verifier |
| 4 Eval & regression | `reliability/evals/`, `.github/workflows/reliability-gate.yml` | Golden set + promptfoo assertions; CI blocks regressions |
| 5 Observability | `reliability/observability/{otel.env,docker-compose.langfuse.yml}` | OTel GenAI conventions; trace → prompt/model/dataset linkage |
| 6 Human-in-loop & governance | `reliability/redteam/`, `governance/nist-iso-42001-mapping.md` | Garak/promptfoo red-team; NIST/ISO/EU control map |

## Methods are sourced to primary literature

- **Semantic entropy** — Farquhar et al., *Nature* 630:625–630 (2024),
  doi:10.1038/s41586-024-07421-0. Detects the *confabulation* subset of
  hallucinations; ~5–10× compute cost (sampling).
- **Lynx** — Ravi et al., arXiv:2407.08488 (2024). Open-weights faithfulness
  evaluator; +8.3% over GPT-4o on PubMedQA (Patronus); ~87.4% on HaluBench
  (independently reported). Preprint + vendor; corroborated.
- **CiteGuard** — Choi et al., arXiv:2510.17853. Retrieval-augmented citation
  attribution; approaches but does not reach human performance (~68% vs ~69%).
  Preprint; figures shifted across versions — re-measure on your own set.

## What is runnable today vs. needs your keys

- **Runnable now:** all five hooks, secret scan, destructive-command deny-list,
  local grounding gate, promptfoo structure, OTel env, Langfuse self-host,
  governance map.
- **Needs your keys/hosting:** Lynx (self-host weights or Patronus API), RAGAS
  judge model, semantic-entropy sampler + NLI model, any hosted eval/observability
  provider (Galileo, Braintrust, Arize, Datadog).

## Known limits (read before trusting)

- Codex `PreToolUse`/`PostToolUse` intercept **only Bash** today, and the model
  can write a script to disk then run it — guardrail, not a hard boundary.
- A verifier sharing the generator's model family shares its blind spots.
- LLM-as-judge is systematically biased; use it as one filter, not the authority.
- OTel GenAI conventions are still in Development status; attribute names may change.
- OTel captures *what happened*, not *whether it was good* — always pair it with
  the evaluation layer.
