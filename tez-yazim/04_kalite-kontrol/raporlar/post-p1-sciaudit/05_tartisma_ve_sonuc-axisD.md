{
  "axis": "D-hallucination-signals",
  "counts": {
    "error": 0,
    "warning": 1,
    "info": 0
  },
  "findings": [
    {
      "severity": "warning",
      "code": "universal-quantifier",
      "message": "Evrensel niceleyici; genelleme aşımı olabilir.",
      "evidence": "her zaman yansımayabileceği"
    }
  ],
  "scope_note": "Textual signals correlated with confabulation; NOT a truth verdict. For a consistency-based signal, run semantic_entropy.py with a sampler+NLI backend (a Claude subagent in-plugin)."
}
