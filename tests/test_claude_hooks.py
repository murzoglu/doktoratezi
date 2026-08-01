"""Contract tests for the Claude Code hook layer (.claude/hooks) — doktoratezi.

Mirrors the Codex hook guarantees (same deny-list semantics, secret scanning,
stop-gate) plus Claude-specific extensions (transcript-based last-message
recovery, repo-file-path source markers, permissions.deny wiring).

Run: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_claude_hooks.py
Twin: niteliksel/tests/test_claude_hooks.py
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

    def test_denies_pii_source_display(self):
        # Tier 1: PII/ön-temizlik kaynak dosyaları her komut ailesinde kapalı.
        for cmd in (
            "cat 'data/raw/Raw Data - Final.csv'",
            "grep aile data/identified/x.csv",
            "head data/cleaned/y.csv",
            "sed -n 1p data/backup/z.csv",
        ):
            self.assertIn("PII source data", self.deny_reason(cmd), cmd)

    def test_denies_interpreter_on_pii_and_credentials(self):
        self.assertIn("PII source data or credentials",
                      self.deny_reason("Rscript -e 'read.csv(\"data/raw/x.csv\")'"))
        self.assertIn("credentials or environment files", self.deny_reason("cat .env"))

    def test_denies_exfiltration_of_any_study_data(self):
        # Tier 3: de-identified olsa bile veriyi dışa-kopyalama/encode kapalı.
        for cmd in (
            "cp -r data/backup /tmp/x",
            "tar czf /tmp/d.tgz data/processed",
            "base64 outputs/tables/t1.csv",
            "scp data/processed/FINAL_REFERENCE__analysis_base_long.csv host:/tmp",
        ):
            self.assertIn("exfiltration guard", self.deny_reason(cmd), cmd)

    def test_denies_destructive_and_broad_ops(self):
        self.assertIn("force-delete", self.deny_reason("rm -rf /home/user/x"))
        self.assertIn("Broad staging", self.deny_reason("git add ."))
        self.assertIn("plaintext", self.deny_reason("codex mcp list"))

    def test_allows_analysis_on_deidentified_base(self):
        # Tier 2: kanonik işlenmiş baz + aggregate çıktı R/python + display'e açık.
        for cmd in (
            "Rscript -e 'targets::tar_make()'",
            "Rscript -e 'd<-read.csv(\"data/processed/FINAL_REFERENCE__analysis_base_family.csv\"); cor(d$anne_yas, d$cocuk_sayisi)'",
            "head data/processed/FINAL_REFERENCE__analysis_base_long.csv",
            "rg beck outputs/tables/t1.csv",
            "python3 -c 'import pandas as pd; pd.read_csv(\"outputs/tables/t.csv\")'",
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

    def test_blocks_decimal_dot_pvalue(self):
        # §1.4: gövde metninde nokta-ondalık p değeri (p=0.032) turn-end'de
        # bloklanır (Marmara ondalık virgül).
        transcript = self.make_transcript("Etki anlamlıydı (p=0.032).")
        proc = run_hook("stop_verify.py",
                        {"hook_event_name": "Stop", "stop_hook_active": False,
                         "transcript_path": transcript})
        self.assertEqual("block", stdout_json(proc).get("decision"))

    def test_allows_comma_pvalue(self):
        transcript = self.make_transcript(
            "Etki anlamlıydı (p=0,032) (outputs/tables/t.csv).")
        proc = run_hook("stop_verify.py",
                        {"hook_event_name": "Stop", "stop_hook_active": False,
                         "transcript_path": transcript})
        self.assertTrue(stdout_json(proc).get("continue"))


class PostToolUseBibGateTests(unittest.TestCase):
    def _mod(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "ptr_bibgate", HOOKS / "post_tool_use_review.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    def test_is_bib_target_true_for_references_bib(self):
        m = self._mod()
        self.assertTrue(m._is_bib_target(
            {"tool_name": "Edit",
             "tool_input": {"file_path": "references/references.bib"}}))
        self.assertTrue(m._is_bib_target(
            {"tool_name": "Write",
             "tool_input": {"file_path": "/abs/references/references.bib"}}))

    def test_is_bib_target_false_for_other(self):
        m = self._mod()
        self.assertFalse(m._is_bib_target(
            {"tool_name": "Write", "tool_input": {"file_path": "docs/x.md"}}))
        self.assertFalse(m._is_bib_target(
            {"tool_name": "Bash", "tool_input": {"command": "ls"}}))

    def test_references_bib_write_clean_passes(self):
        # Repo bib'i şu an HARD=0 → block yok (gate çalışır ama temiz geçer).
        proc = run_hook("post_tool_use_review.py",
                        {"hook_event_name": "PostToolUse", "tool_name": "Edit",
                         "tool_input": {"file_path": "references/references.bib",
                                        "old_string": "a", "new_string": "b"}})
        self.assertEqual(0, proc.returncode)
        self.assertNotEqual("block", stdout_json(proc).get("decision"))


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
        # Tier 1 + Tier 3: PII kaynakları, _targets store ve credential kapalı.
        for rule in (
            "Read(./data/raw/**)",
            "Read(./data/identified/**)",
            "Read(./data/cleaned/**)",
            "Read(./data/backup/**)",
            "Read(./_targets/**)",
            "Edit(./data/**)",
            "Read(./.env)",
        ):
            self.assertIn(rule, deny, rule)
        # Tier 2: de-identified analiz yüzeyi artık Read-deny DEĞİL (owner onayı).
        for rule in (
            "Read(./data/processed/**/*.csv)",
            "Read(./outputs/**/*.csv)",
        ):
            self.assertNotIn(rule, deny, rule)

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


class CopilotHookBridgeTests(unittest.TestCase):
    """.github/hooks — Copilot CLI zorlama katmanı ikizi.

    Copilot proje hook'larını git kökündeki `.github/hooks/*.json` dosyalarından
    yükler; Claude olay adlarını otomatik Copilot adlarına çevirip `_vsCodeCompat`
    bayrağını kendisi koyar. Bu yüzden yapılandırma `.claude/settings.json` ile
    aynı sözdizimindedir. Betikler kopyalanmaz: dispatch.py köprüsü depodaki
    `.claude/hooks/*.py` betiklerini çalıştırır ve iki çıktı sözleşmesi farkını
    (exit-2 bloku, additionalContext konumu) çevirir.
    """

    HOOKS_DIR = REPO / ".github" / "hooks"
    DISPATCH = HOOKS_DIR / "dispatch.py"

    # Claude olay adı -> (matcher, betik, timeout)
    EXPECTED = {
        "SessionStart": ("startup|resume|compact", "session_start.py", 30),
        "UserPromptSubmit": (None, "user_prompt_submit.py", 15),
        "PreToolUse": ("Bash", "pre_tool_use_policy.py", 15),
        "Stop": (None, "stop_verify.py", 120),
    }

    def hooks_config(self) -> dict:
        return json.loads((self.HOOKS_DIR / "hooks.json").read_text(encoding="utf-8"))

    def entries(self, event: str) -> list:
        """Claude'un iç içe {matcher, hooks:[...]} biçimini düzleştir."""
        out = []
        for block in self.hooks_config()["hooks"][event]:
            for entry in block["hooks"]:
                out.append((block.get("matcher"), entry))
        return out

    def dispatch(self, script: str, event_key: str, event: dict) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["python3", str(self.DISPATCH), script, event_key, "15"],
            input=json.dumps(event),
            capture_output=True,
            text=True,
            cwd=str(REPO),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            timeout=60,
        )

    def test_hooks_json_mirrors_claude_settings(self):
        """Beş Claude hook'unun tamamı aynı matcher/timeout ile taşınmış olmalı."""
        claude_hooks = json.loads(SETTINGS.read_text(encoding="utf-8"))["hooks"]
        copilot_hooks = self.hooks_config()["hooks"]
        self.assertEqual(set(claude_hooks), set(copilot_hooks), "olay kümesi ayrışmış")

        for event, (matcher, script, timeout) in self.EXPECTED.items():
            found = self.entries(event)
            self.assertEqual(1, len(found), event)
            block_matcher, entry = found[0]
            self.assertEqual(matcher, block_matcher, event)
            self.assertIn(script, entry["command"], event)
            self.assertEqual(timeout, entry["timeout"], event)

        # PostToolUse: Claude tarafındaki iki matcher (Bash + yazma araçları) korunur.
        post = {m: e["timeout"] for m, e in self.entries("PostToolUse")}
        self.assertEqual({"Bash": 15, "Write|Edit|MultiEdit": 200}, post)

    def test_every_referenced_script_exists(self):
        for event in self.hooks_config()["hooks"]:
            for _, entry in self.entries(event):
                script = entry["command"].split("dispatch.py\" ")[1].split()[0]
                self.assertTrue((HOOKS / script).is_file(), script)

    def test_dispatch_translates_exit2_into_deny(self):
        """Claude'un exit-2 bloku Copilot'ta uyarıya düşmemeli; deny'a çevrilmeli."""
        proc = self.dispatch(
            "pre_tool_use_policy.py",
            "preToolUse",
            {
                "hook_event_name": "PreToolUse",
                "cwd": str(REPO),
                "tool_name": "Bash",
                "tool_input": {"command": "cat data/raw/gizli.csv"},
            },
        )
        self.assertEqual(0, proc.returncode, proc.stderr)
        out = stdout_json(proc)
        self.assertEqual("deny", out["hookSpecificOutput"]["permissionDecision"])

    def test_dispatch_translates_prompt_block(self):
        proc = self.dispatch(
            "user_prompt_submit.py",
            "userPromptSubmitted",
            {
                "hook_event_name": "UserPromptSubmit",
                "cwd": str(REPO),
                "prompt": "anahtar sk-ant-" + "a" * 30,
            },
        )
        self.assertEqual("block", stdout_json(proc).get("decision"))

    def test_dispatch_lifts_additional_context_to_top_level(self):
        """Copilot sessionStart çıktı dönüştürücüsü ÜST DÜZEY additionalContext okur."""
        proc = self.dispatch(
            "session_start.py",
            "sessionStart",
            {"hook_event_name": "SessionStart", "cwd": str(REPO), "source": "startup"},
        )
        out = stdout_json(proc)
        self.assertIsInstance(out.get("additionalContext"), str)
        self.assertTrue(out["additionalContext"].strip())

    def test_dispatch_is_inert_outside_the_repo(self):
        """Köprü yanlışlıkla başka bir ağaçta çalışırsa hiçbir şey yapmamalı."""
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                ["python3", str(self.DISPATCH), "pre_tool_use_policy.py", "preToolUse", "15"],
                input=json.dumps(
                    {"cwd": tmp, "tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}
                ),
                capture_output=True,
                text=True,
                cwd=tmp,
                env={
                    k: v
                    for k, v in os.environ.items()
                    if k not in ("CLAUDE_PROJECT_DIR", "COPILOT_PROJECT_DIR")
                },
                timeout=30,
            )
            self.assertEqual(0, proc.returncode)
            self.assertEqual("", proc.stdout.strip())


class CopilotSurfaceParityTests(unittest.TestCase):
    """Claude ↔ Copilot yüzey paritesi: slash komut ve MCP roster'ı."""

    def test_slash_command_twins_are_complete(self):
        claude = {p.stem for p in (REPO / ".claude" / "commands").glob("*.md")}
        copilot = {
            p.name[: -len(".prompt.md")]
            for p in (REPO / ".github" / "prompts").glob("*.prompt.md")
        }
        self.assertEqual(claude, copilot, f"eksik ikiz: {claude ^ copilot}")

    def test_mcp_rosters_stay_in_sync(self):
        """Copilot CLI .mcp.json okur, VS Code Chat .vscode/mcp.json; ikisi eş tutulur."""
        cli_path, chat_path = REPO / ".mcp.json", REPO / ".vscode" / "mcp.json"
        if not (cli_path.is_file() and chat_path.is_file()):
            self.skipTest("MCP yapılandırmaları bu ağaçta yok (gitignore).")

        def names(path: Path, key: str) -> set:
            raw = "\n".join(
                line
                for line in path.read_text(encoding="utf-8").split("\n")
                if not line.lstrip().startswith("//")
            )
            return {k for k in json.loads(raw)[key] if not k.startswith("_")}

        self.assertEqual(
            names(cli_path, "mcpServers"),
            names(chat_path, "servers"),
            "MCP roster drift: yeni sunucu her iki dosyaya da eklenmeli.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

