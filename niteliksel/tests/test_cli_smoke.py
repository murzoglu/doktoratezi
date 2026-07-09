"""CLI uçtan uca duman testi — 10 alt komut kayıtlı mı, dispatch + KVKK reddi çalışıyor mu."""
import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from dm_niteliksel_toolkit.cli import build_parser, main

EXPECTED_SUBCOMMANDS = {
    "init", "ai-context", "route-tool", "cross-repo-status", "lint-codebook",
    "build-triadic-matrix", "check-quotes", "audit-coreq", "find-negative-cases",
    "log-ai-use",
}


class CliRegistrationTests(unittest.TestCase):
    def test_all_ten_subcommands_are_registered(self):
        parser = build_parser()
        subparsers = next(
            a for a in parser._actions if hasattr(a, "choices") and a.choices
        )
        self.assertEqual(set(subparsers.choices), EXPECTED_SUBCOMMANDS)

    def test_missing_subcommand_exits_nonzero(self):
        with self.assertRaises(SystemExit):
            main([])


class CliDispatchTests(unittest.TestCase):
    def test_route_tool_dispatches_and_returns_zero(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["route-tool", "--query", "COREQ denetimi"])
        self.assertEqual(rc, 0)
        self.assertIn("Route", buf.getvalue())

    def test_log_ai_use_writes_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "ai_use_log.csv"
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main([
                    "log-ai-use", "--tool", "t", "--model", "m", "--purpose", "p",
                    "--data-type", "anonim/türetilmiş", "--output-summary", "s",
                    "--log", str(log),
                ])
            self.assertEqual(rc, 0)
            with log.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["tool"], "t")


class CliKvkkRejectionTests(unittest.TestCase):
    def test_log_ai_use_into_protected_path_exits_2(self):
        # assert_not_protected_write ValueError -> main parser.exit(2)
        with self.assertRaises(SystemExit) as ctx:
            main([
                "log-ai-use", "--tool", "t", "--model", "m", "--purpose", "p",
                "--data-type", "anonim/türetilmiş", "--output-summary", "s",
                "--log", "01_deidentified/leak.csv",
            ])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
