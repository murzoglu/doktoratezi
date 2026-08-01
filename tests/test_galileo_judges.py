#!/usr/bin/env python3
"""galileo_bridge judge uzantıları — classify_gate folding + kayıt testleri.

Ağ/gateway çağrısı YAPMAZ: classify_gate saf-mantık (sahte judge dict'leriyle),
geriye-uyum ve _TOOLS/_DISPATCH kaydını doğrular. Judge'ların canlı LLM çıktısı
final healthcheck smoke'ta ayrıca denetlenir.

Çalıştır: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_galileo_judges.py
"""
from __future__ import annotations

import importlib.util
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_MOD = os.path.join(os.path.dirname(_HERE), "scripts", "eval", "galileo_bridge.py")
_spec = importlib.util.spec_from_file_location("galileo_bridge", _MOD)
gb = importlib.util.module_from_spec(_spec)
sys.modules["galileo_bridge"] = gb
_spec.loader.exec_module(gb)

_TH = dict(gb._GATE_DEFAULTS)


def _gate(**kw):
    return gb.classify_gate({}, {}, cfg_thresholds=_TH, **kw)


class TestClassifyGateBackCompat(unittest.TestCase):
    def test_two_arg_still_works(self):
        out = gb.classify_gate({"scores": {}}, {})
        self.assertEqual(out["hard"], [])
        self.assertIn("soft_block", out)

    def test_hard_always_empty(self):
        out = _gate(harking={"harking_risk": 1.0, "post_hoc_as_prior": True},
                    overclaim={"overclaim_risk": 1.0, "causal_drift": True})
        self.assertEqual(out["hard"], [])


class TestHarking(unittest.TestCase):
    def test_high_risk_soft(self):
        out = _gate(harking={"harking_risk": 0.8})
        self.assertTrue(any(s["type"] == "harking_risk" for s in out["soft_block"]))

    def test_post_hoc_flag_soft(self):
        out = _gate(harking={"harking_risk": 0.1, "post_hoc_as_prior": True})
        self.assertTrue(any(s["type"] == "harking_risk" for s in out["soft_block"]))

    def test_missing_risk_not_flagged(self):
        # numz: eksik risk 0.0 sayılır → yanlış-pozitif yok
        out = _gate(harking={"rationale": "temiz"})
        self.assertFalse(any(s["type"] == "harking_risk" for s in out["soft_block"]))

    def test_none_no_signal(self):
        out = _gate()
        self.assertEqual(out["soft_block"], [])
        self.assertEqual(out["advisory"], [])


class TestOverclaim(unittest.TestCase):
    def test_causal_drift_soft(self):
        out = _gate(overclaim={"overclaim_risk": 0.2, "causal_drift": True})
        self.assertTrue(any(s["type"] == "overclaim_risk" for s in out["soft_block"]))

    def test_cherry_pick_advisory(self):
        out = _gate(overclaim={"overclaim_risk": 0.1, "cherry_pick": True})
        self.assertTrue(any(a["type"] == "multiverse_cherry_pick" for a in out["advisory"]))

    def test_clean_no_signal(self):
        out = _gate(overclaim={"overclaim_risk": 0.1})
        self.assertEqual(out["soft_block"], [])


class TestConvergence(unittest.TestCase):
    def test_over_integration_soft(self):
        out = _gate(convergence={"relationship": "uyum", "over_integration": True})
        self.assertTrue(any(s["type"] == "over_integration" for s in out["soft_block"]))

    def test_divergence_advisory(self):
        out = _gate(convergence={"relationship": "ayrışma", "over_integration": False})
        self.assertTrue(any(a["type"] == "qual_quant_divergence" for a in out["advisory"]))


class TestCoherenceJudge(unittest.TestCase):
    def test_broken_chain_soft(self):
        out = _gate(coherence_judge={"chain_intact": False, "coherence": 0.9})
        self.assertTrue(any(s["type"] == "narrative_coherence_low" for s in out["soft_block"]))

    def test_low_score_soft(self):
        out = _gate(coherence_judge={"chain_intact": True, "coherence": 0.3})
        self.assertTrue(any(s["type"] == "narrative_coherence_low" for s in out["soft_block"]))

    def test_intact_no_signal(self):
        out = _gate(coherence_judge={"chain_intact": True, "coherence": 0.9})
        self.assertEqual(out["soft_block"], [])


class TestRegistration(unittest.TestCase):
    def test_new_tools_registered(self):
        names = {t[0] for t in gb._TOOLS}
        for n in ("galileo_convergence_judge", "galileo_harking_judge",
                  "galileo_overclaim_judge", "galileo_coherence_judge"):
            self.assertIn(n, names, "%s _TOOLS'ta yok" % n)
            self.assertIn(n, gb._DISPATCH, "%s _DISPATCH'te yok" % n)

    def test_dispatch_callable(self):
        for n in ("galileo_convergence_judge", "galileo_harking_judge",
                  "galileo_overclaim_judge", "galileo_coherence_judge"):
            self.assertTrue(callable(gb._DISPATCH[n]))


if __name__ == "__main__":
    unittest.main()
