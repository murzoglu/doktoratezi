# Governance mapping (Layer 6)

This scaffold's controls mapped to the three frameworks that dominate the 2026
regulatory surface. Use this when you need to show *defensible* process — which
matters in regulated (medical / pharma) deployments.

| This scaffold control | NIST AI RMF (GenAI Profile) | ISO/IEC 42001 | EU AI Act |
|---|---|---|---|
| Source grounding + citation enforcement (Layer 0) | MEASURE 2.x (validity, reliability) | 8.3 operational control | Art. 13 transparency |
| Deterministic hooks / deny-list (Layer 1) | MANAGE 2.x (risk treatment) | 8.1 operational planning | Art. 15 robustness |
| Claim verification: Lynx / RAGAS / semantic entropy (Layer 2) | MEASURE 2.3 (accuracy) | 9.1 monitoring | Art. 15 accuracy |
| Verifier-agent triangulation (Layer 3) | MANAGE 4.x | 8.1 | Art. 14 human oversight (assist) |
| Golden-set regression + CI gate (Layer 4) | MEASURE 4.x (feedback) | 9.1 / 10.x improvement | Art. 17 quality mgmt system |
| OTel traceability (Layer 5) | GOVERN 1.x (accountability) | 7.5 documented info | Art. 12 record-keeping / logging |
| Human-in-the-loop + red-team (Layer 6) | MAP / MANAGE | 6.1 risk assessment | Art. 14 human oversight; Art. 9 risk mgmt |

Notes
- Record-keeping (EU AI Act Art. 12) is satisfied operationally by the OTel
  GenAI spans, provided you retain traces with the run's prompt/model/dataset
  linkage.
- "Human oversight" is only partially automatable: the verifier and gates
  *assist* a human reviewer; they do not replace sign-off for high-risk outputs.
- This is an engineering-control map, not legal advice. Confirm applicability
  and current enforcement dates with counsel for your jurisdiction and risk tier.
