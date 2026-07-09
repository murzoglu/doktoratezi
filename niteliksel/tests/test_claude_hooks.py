"""Contract tests for the Claude Code hook layer (.claude/hooks).

Mirrors the Codex hook guarantees: same deny-list semantics, same secret
scanning, same stop-gate behavior — plus the Claude-specific extensions
(transcript-based last-message recovery, repo-file-path source markers,
permissions.deny wiring in .claude/settings.json).
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
            "cat 01_raw_data/interviews_docx/aile_011.docx",
            "grep anne 02_processed/transcripts/all_transcripts_merged.md",
            "head 01_deidentified/family_011.md",
            "rg 'kod' 00_raw_locked/x.md",
        ):
            self.assertIn("sensitive study data", self.deny_reason(cmd), cmd)

    def test_denies_credential_display_and_interpreters(self):
        self.assertIn("credentials or environment files", self.deny_reason("cat .env"))
        self.assertIn("sensitive study data or credentials",
                      self.deny_reason("python3 parse.py 02_processed/transcripts/all.md"))
        self.assertIn("sensitive study data or credentials",
                      self.deny_reason("cp -r 01_raw_data/ /tmp/out"))

    def test_denies_destructive_and_broad_ops(self):
        self.assertIn("force-delete", self.deny_reason("rm -rf /home/user/x"))
        self.assertIn("Broad staging", self.deny_reason("git add ."))
        self.assertIn("plaintext", self.deny_reason("codex mcp list"))

    def test_allows_safe_commands(self):
        for cmd in (
            "./dmnitel ai-context",
            "ls 02_processed/cleaned_text",
            "cat 02_processed/cleaned_text/thesis_qualitative_cleaned_current.md",
            "git add CLAUDE.md",
            "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests",
            "python3 .codex/tools/codex_mcp_roster_redacted.py",
        ):
            self.assertEqual("", self.deny_reason(cmd), cmd)


class UserPromptSubmitTests(unittest.TestCase):
    def test_blocks_secret_prompt(self):
        proc = run_hook(
            "user_prompt_submit.py",
            {"hook_event_name": "UserPromptSubmit",
             "prompt": "su anahtari kullan: sk-ant-abc123def456ghi789jkl012mno345"},
        )
        self.assertEqual(2, proc.returncode)
        self.assertIn("secret", proc.stderr)

    def test_allows_normal_prompt(self):
        proc = run_hook(
            "user_prompt_submit.py",
            {"hook_event_name": "UserPromptSubmit", "prompt": "COREQ denetimini calistir"},
        )
        self.assertEqual(0, proc.returncode)


class PostToolUseReviewTests(unittest.TestCase):
    def test_flags_error_signature(self):
        proc = run_hook(
            "post_tool_use_review.py",
            {"hook_event_name": "PostToolUse", "tool_name": "Bash",
             "tool_response": "Traceback (most recent call last):\n  boom"},
        )
        payload = stdout_json(proc)
        self.assertIn("error signature",
                      payload.get("hookSpecificOutput", {}).get("additionalContext", ""))

    def test_flags_secret_leak(self):
        proc = run_hook(
            "post_tool_use_review.py",
            {"hook_event_name": "PostToolUse", "tool_name": "Bash",
             "tool_response": {"stdout": "token=ghp_" + "a" * 40}},
        )
        payload = stdout_json(proc)
        self.assertIn("secret-like",
                      payload.get("hookSpecificOutput", {}).get("additionalContext", ""))

    def test_silent_on_clean_output(self):
        proc = run_hook(
            "post_tool_use_review.py",
            {"hook_event_name": "PostToolUse", "tool_name": "Bash", "tool_response": "OK"},
        )
        self.assertEqual("", proc.stdout.strip())


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

    def test_blocks_unsourced_numeric_claim_from_transcript(self):
        transcript = self.make_transcript(
            "Analizde 21 görüşme kullanıldı ve katılımcıların %30 kadarı farklıydı."
        )
        proc = run_hook("stop_verify.py",
                        {"hook_event_name": "Stop", "stop_hook_active": False,
                         "transcript_path": transcript})
        payload = stdout_json(proc)
        self.assertEqual("block", payload.get("decision"))

    def test_repo_file_path_counts_as_source(self):
        transcript = self.make_transcript(
            "Analizde 21 görüşme kullanıldı (kaynak: 00_context/TRACKER.md)."
        )
        proc = run_hook("stop_verify.py",
                        {"hook_event_name": "Stop", "stop_hook_active": False,
                         "transcript_path": transcript})
        payload = stdout_json(proc)
        self.assertTrue(payload.get("continue"))

    def test_respects_stop_hook_active(self):
        proc = run_hook("stop_verify.py",
                        {"hook_event_name": "Stop", "stop_hook_active": True,
                         "last_assistant_message": "21 görüşme %30"})
        payload = stdout_json(proc)
        self.assertTrue(payload.get("continue"))

    def test_direct_last_message_field_still_supported(self):
        proc = run_hook("stop_verify.py",
                        {"hook_event_name": "Stop", "stop_hook_active": False,
                         "last_assistant_message":
                             "Örneklemde 7 aile bulunmaktadır ve bu önemlidir."})
        payload = stdout_json(proc)
        self.assertEqual("block", payload.get("decision"))


class SessionStartTests(unittest.TestCase):
    def test_injects_conventions_and_mandatory_block(self):
        proc = run_hook("session_start.py",
                        {"hook_event_name": "SessionStart", "source": "startup"})
        payload = stdout_json(proc)
        context = payload.get("hookSpecificOutput", {}).get("additionalContext", "")
        self.assertIn("AI reliability conventions", context)
        self.assertIn("ZORUNLU TALİMATNAME", context)
        self.assertIn("TALIMATNAME_TEZ_YAZIM.md", context)


class SettingsWiringTests(unittest.TestCase):
    def test_settings_json_wires_all_layers(self):
        data = json.loads(SETTINGS.read_text(encoding="utf-8"))
        hooks = data.get("hooks", {})
        for event in ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"):
            self.assertIn(event, hooks, event)
        deny = data.get("permissions", {}).get("deny", [])
        for rule in (
            "Read(./01_raw_data/**)",
            "Read(./02_processed/transcripts/**)",
            "Read(./01_deidentified/**)",
            "Read(./00_raw_locked/**)",
            "Read(./.env)",
        ):
            self.assertIn(rule, deny, rule)

    def test_hook_scripts_compile(self):
        proc = subprocess.run(
            ["python3", "-m", "py_compile", *[str(p) for p in sorted(HOOKS.glob("*.py"))]],
            capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(0, proc.returncode, proc.stderr)


if __name__ == "__main__":
    unittest.main()
