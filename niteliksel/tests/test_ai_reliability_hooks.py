import importlib.util
import sys
import unittest
from pathlib import Path


class AiReliabilityHookTests(unittest.TestCase):
    def test_plugin_regression_suite_passes(self):
        repo = Path(__file__).resolve().parents[1]
        script = repo / "plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py"
        spec = importlib.util.spec_from_file_location("t1dm_qual_ai_reliability_tests", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        failures = [result for result in module.run_all() if not result.ok]

        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
