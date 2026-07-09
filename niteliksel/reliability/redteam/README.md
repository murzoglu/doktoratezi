# Red-teaming (Layer 6)

Two complementary tools. Run on a recurring schedule, not just at release.

## promptfoo red-team (OWASP-aligned, CI-native)
```bash
npx promptfoo@latest redteam run -c reliability/redteam/promptfoo-redteam.yaml
npx promptfoo@latest redteam report      # view findings
```

## NVIDIA Garak (50+ probe modules)
```bash
pip install garak
# Scan an OpenAI-compatible target for injection, jailbreak, leakage, toxicity:
garak --model_type openai --model_name gpt-5.2-codex \
      --probes promptinject,leakreplay,dan
```

Other options in this space: ARTKIT, DeepTeam. For regulated-domain checks
consider Patronus FinanceBench / CopyrightCatcher as targeted add-ons.

Always treat findings as inputs to your golden set: every successful attack
becomes a new regression test in `reliability/evals/golden/dataset.yaml`.
