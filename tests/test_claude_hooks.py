"""Contract tests for the Claude Code hook layer (.claude/hooks) — doktoratezi.

Mirrors the Codex hook guarantees (same deny-list semantics, secret scanning,
stop-gate) plus Claude-specific extensions (transcript-based last-message
recovery, repo-file-path source markers, permissions.deny wiring).

Run: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_claude_hooks.py
Twin: /mnt/thunderbolt/workspaces/T1DM Niteliksel/tests/test_claude_hooks.py
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOOKS = REPO / ".claude" / "hooks"
SETTINGS = REPO / ".claude" / "settings.json"


def run_hook(script: str, event: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(HOOKS / script)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        cwd=str(REPO),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        timeout=30,
    )


def stdout_json(proc: subprocess.CompletedProcess) -> dict:
    return json.loads(proc.stdout) if proc.stdout.strip() else {}


class PreToolUsePolicyTests(unittest.TestCase):
    def deny_reason(self, command: str) -> str:
        proc = run_hook(
            "pre_tool_use_policy.py",
            {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}},
        )
        self.assertEqual(0, proc.returncode)
        payload = stdout_json(proc)
        decision = payload.get("hookSpecificOutput", {}).get("permissionDecision", "")
        if decision == "deny":
            return payload["hookSpecificOutput"]["permissionDecisionReason"]
        return ""

    def test_denies_sensitive_data_display(self):
        for cmd in (
            "cat 'data/raw/Raw Data - Final.csv'",
            "head data/processed/FINAL_REFERENCE__analysis_base_family.csv",
            "grep aile data/identified/x.csv",
            "rg beck outputs/tables/t1.csv",
        ):
            self.assertIn("sensitive study data", self.deny_reason(cmd), cmd)

    def test_denies_interpreter_and_copy_on_sensitive_paths(self):
        self.assertIn("sensitive study data or credentials",
                      self.deny_reason("Rscript -e 'readr::read_csv(\"data/processed/FINAL_REFERENCE__analysis_base_long.csv\")'"))
        self.assertIn("sensitive study data or credentials",
                      self.deny_reason("cp -r data/backup /tmp/x"))
        self.assertIn("credentials or environment files", self.deny_reason("cat .env"))

    def test_denies_destructive_and_broad_ops(self):
        self.assertIn("force-delete", self.deny_reason("rm -rf /home/user/x"))
        self.assertIn("Broad staging", self.deny_reason("git add ."))
        self.assertIn("plaintext", self.deny_reason("codex mcp list"))

    def test_allows_pipeline_and_docs_commands(self):
        for cmd in (
            "Rscript -e 'targets::tar_make()'",
            "Rscript tests/test_data_governance.R",
            "quarto render",
            "cat tez-yazim/README.md",
            "git add CLAUDE.md",
            "ls outputs",
        ):
            self.assertEqual("", self.deny_reason(cmd), cmd)


class UserPromptSubmitTests(unittest.TestCase):
    def test_blocks_secret_prompt(self):
        proc = run_hook(
            "user_prompt_submit.py",
            {"hook_event_name": "UserPromptSubmit",
             "prompt": "anahtar: sk-ant-abc123def456ghi789jkl012mno345"},
        )
        self.assertEqual(2, proc.returncode)
        self.assertIn("secret", proc.stderr)

    def test_allows_normal_prompt(self):
        proc = run_hook(
            "user_prompt_submit.py",
            {"hook_event_name": "UserPromptSubmit", "prompt": "H5 diadik uyum bolumunu yaz"},
        )
        self.assertEqual(0, proc.returncode)


class StopVerifyTests(unittest.TestCase):
    def make_transcript(self, text: str) -> str:
        fd, path = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"type": "user", "message": {"content": "soru"}}) + "\n")
            fh.write(json.dumps({
                "type": "assistant",
                "message": {"role": "assistant",
                            "content": [{"type": "text", "text": text}]},
            }) + "\n")
        self.addCleanup(os.unlink, path)
        return path

    def test_blocks_unsourced_numeric_claim(self):
        transcript = self.make_transcript(
            "Örneklemde 241 aile vardır ve %30 kayıp gözlenmiştir."
        )
        proc = run_hook("stop_verify.py",
                        {"hook_event_name": "Stop", "stop_hook_active": False,
                         "transcript_path": transcript})
        self.assertEqual("block", stdout_json(proc).get("decision"))

    def test_repo_file_path_counts_as_source(self):
        transcript = self.make_transcript(
            "Örneklemde 241 aile vardır (docs/CLINICAL-STUDY-REPORT-FINAL.md)."
        )
        proc = run_hook("stop_verify.py",
                        {"hook_event_name": "Stop", "stop_hook_active": False,
                         "transcript_path": transcript})
        self.assertTrue(stdout_json(proc).get("continue"))

    def test_respects_stop_hook_active(self):
        proc = run_hook("stop_verify.py",
                        {"hook_event_name": "Stop", "stop_hook_active": True,
                         "last_assistant_message": "241 aile %30"})
        self.assertTrue(stdout_json(proc).get("continue"))


class SessionStartTests(unittest.TestCase):
    def test_injects_conventions_and_mandatory_block(self):
        proc = run_hook("session_start.py",
                        {"hook_event_name": "SessionStart", "source": "startup"})
        context = stdout_json(proc).get("hookSpecificOutput", {}).get("additionalContext", "")
        self.assertIn("ZORUNLU TALİMATNAME", context)
        self.assertIn("talimatname-claude-code.md", context)


class SettingsWiringTests(unittest.TestCase):
    def test_settings_json_wires_all_layers(self):
        data = json.loads(SETTINGS.read_text(encoding="utf-8"))
        hooks = data.get("hooks", {})
        for event in ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"):
            self.assertIn(event, hooks, event)
        deny = data.get("permissions", {}).get("deny", [])
        for rule in (
            "Read(./data/raw/**)",
            "Read(./data/identified/**)",
            "Read(./data/cleaned/**)",
            "Read(./data/backup/**)",
            "Read(./data/processed/**/*.csv)",
            "Read(./_targets/**)",
            "Read(./.env)",
        ):
            self.assertIn(rule, deny, rule)

    def test_lock_metadata_stays_readable(self):
        """data/processed altındaki .lock/.md metadata dosyaları deny'a girmez."""
        data = json.loads(SETTINGS.read_text(encoding="utf-8"))
        deny = data.get("permissions", {}).get("deny", [])
        self.assertNotIn("Read(./data/processed/**)", deny)

    def test_hook_scripts_compile(self):
        proc = subprocess.run(
            ["python3", "-m", "py_compile", *[str(p) for p in sorted(HOOKS.glob("*.py"))]],
            capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(0, proc.returncode, proc.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
