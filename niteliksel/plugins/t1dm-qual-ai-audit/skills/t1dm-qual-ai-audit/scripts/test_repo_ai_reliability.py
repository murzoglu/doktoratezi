#!/usr/bin/env python3
"""Regression tests for the T1DM qualitative AI reliability scaffold."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_REQUIRED_FILES = (
    'CLAUDE.md',
    'AGENTS.md',
    '00_context/TRACKER.md',
    '00_context/REPO_CONTEXT.md',
    'dmnitel',
)
HOOK_EVENTS = {'SessionStart', 'UserPromptSubmit', 'PreToolUse', 'PostToolUse', 'Stop'}
QUAL_NUMERIC_CLAIMS = (
    'Nitel kol 21 görüşme içerir.',
    'Codebook 23 kod ve 6 tema içerir.',
    'Tez yapısı 4 makro tema kullanır.',
    'COREQ 32 maddesi tamamlandı.',
)


@dataclass
class Result:
    name: str
    ok: bool
    detail: str = ''


def qualitative_root() -> Path:
    for candidate in [Path.cwd().resolve(), *Path.cwd().resolve().parents]:
        if (candidate / 'dmnitel').exists() and (candidate / '00_context/TRACKER.md').exists():
            return candidate
    out = subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel'],
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()
    return Path(out)


def run_hook(script: Path, event: dict[str, Any], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.run(
        ['python3', str(script)],
        input=json.dumps(event),
        text=True,
        capture_output=True,
        cwd=cwd,
        env=env,
        check=False,
    )


def json_stdout(proc: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    return json.loads(proc.stdout or '{}')


def expect(name: str, condition: bool, detail: str = '') -> Result:
    return Result(name, condition, detail)


def permission_denied(proc: subprocess.CompletedProcess[str]) -> bool:
    if proc.returncode != 0:
        return False
    try:
        payload = json_stdout(proc)
    except json.JSONDecodeError:
        return False
    return (
        payload.get('hookSpecificOutput', {}).get('permissionDecision') == 'deny'
        or payload.get('permissionDecision') == 'deny'
    )


def test_repo_markers(repo: Path) -> list[Result]:
    return [
        expect(f'repo marker exists: {rel}', (repo / rel).exists())
        for rel in REPO_REQUIRED_FILES
    ]


def test_config(repo: Path) -> list[Result]:
    config = repo / '.codex/config.toml'
    hooks_json = repo / '.codex/hooks.json'
    promptfoo_config = repo / 'reliability/evals/promptfooconfig.yaml'
    grok_config = repo / 'reliability/evals/promptfooconfig.grok.yaml'
    dataset = repo / 'reliability/evals/golden/dataset.yaml'
    payload = tomllib.loads(config.read_text(encoding='utf-8'))
    hooks_payload = json.loads(hooks_json.read_text(encoding='utf-8'))
    events = set(hooks_payload.get('hooks', {}))
    promptfoo_text = promptfoo_config.read_text(encoding='utf-8')
    grok_text = grok_config.read_text(encoding='utf-8')
    dataset_text = dataset.read_text(encoding='utf-8')
    return [
        expect('codex config parses', True),
        expect('hooks enabled', payload.get('features', {}).get('hooks') is True),
        expect('no deprecated codex_hooks', 'codex_hooks' not in payload.get('features', {})),
        expect('hooks json has qualitative gate events', HOOK_EVENTS.issubset(events), str(events)),
        expect('offline promptfoo uses qualitative provider', 'file://providers/t1dm_qual_policy_provider.py' in promptfoo_text),
        expect('offline promptfoo avoids doktoratezi provider', 'doktoratezi_policy_provider.py' not in promptfoo_text),
        expect('grok promptfoo uses Grok provider', 'file://providers/grok_reasoning_provider.py' in grok_text),
        expect('grok promptfoo loads Grok key via provider', 'GROK_API_KEY' in grok_text),
        expect('golden dataset uses qualitative tracker case', '00_context/TRACKER.md' in dataset_text),
        expect('golden dataset uses transcript refusal case', 'all_transcripts_merged.md' in dataset_text),
        expect('golden dataset uses RTA language case', 'inter-coder reliability' in dataset_text),
        expect('golden dataset avoids quantitative final reference case', 'FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock' not in dataset_text),
    ]


def test_plugin_manifests(repo: Path) -> list[Result]:
    plugin_root = repo / 'plugins/t1dm-qual-ai-audit'
    plugin_json = json.loads((plugin_root / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    marketplace = json.loads((repo / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
    entry = next((item for item in marketplace.get('plugins', []) if item.get('name') == 't1dm-qual-ai-audit'), None)
    return [
        expect('plugin name matches folder', plugin_json.get('name') == plugin_root.name),
        expect('plugin version is semver', re.fullmatch(r'\d+\.\d+\.\d+', plugin_json.get('version', '')) is not None),
        expect('plugin skills path exists', (plugin_root / 'skills').is_dir()),
        expect('skill policy reference exists', (SKILL_ROOT / 'references/repo-audit-policy.md').exists()),
        expect('plugin interface has displayName', bool(plugin_json.get('interface', {}).get('displayName'))),
        expect('marketplace entry exists', entry is not None),
        expect('marketplace path points to plugin', entry is not None and entry.get('source', {}).get('path') == './plugins/t1dm-qual-ai-audit'),
        expect('marketplace policy complete', entry is not None and {'installation', 'authentication'}.issubset(entry.get('policy', {}))),
    ]


def test_user_prompt_submit(repo: Path) -> list[Result]:
    script = repo / '.codex/hooks/user_prompt_submit.py'
    cases = [
        ('plain prompt allowed', 'COREQ ve RTA audit trail kontrolü yap.', 0),
        ('OpenAI key blocked', 'sk-' + 'A' * 32, 2),
        ('Anthropic key blocked', 'sk-ant-' + 'A' * 40, 2),
        ('GitHub token blocked', 'ghp_' + 'A' * 36, 2),
        ('Google key blocked', 'AIza' + 'A' * 35, 2),
        ('private key blocked', '-----BEGIN OPENSSH PRIVATE KEY-----', 2),
    ]
    results: list[Result] = []
    for case_name, prompt, expected_exit in cases:
        proc = run_hook(script, {'prompt': prompt}, cwd=repo)
        results.append(expect(f'user prompt: {case_name}', proc.returncode == expected_exit, f'exit={proc.returncode} stderr={proc.stderr[:120]!r}'))
    return results


def test_pre_tool_use(repo: Path) -> list[Result]:
    script = repo / '.codex/hooks/pre_tool_use_policy.py'
    denied = [
        ('raw interview display', {'tool_input': {'command': 'cat 01_raw_data/interviews_docx/family_011/a.docx'}}),
        ('merged transcript search', {'tool_input': {'command': 'rg adalet 02_processed/transcripts/all_transcripts_merged.md'}}),
        ('remember display', {'tool_input': {'command': 'sed -n 1,10p .remember/remember.md'}}),
        ('raw mcp list', {'tool_input': {'command': 'codex mcp list'}}),
        ('alternate command field', {'command': 'head 02_processed/transcripts/all_transcripts_merged.md'}),
        ('input command field', {'input': {'command': 'rg anne 01_raw_data/interviews_docx'}}),
        ('tool_input string', {'tool_input': 'cat .remember/remember.md'}),
        ('broad staging', {'tool_input': {'command': 'git add .'}}),
    ]
    allowed = [
        ('redacted roster', {'tool_input': {'command': 'python3 .codex/tools/codex_mcp_roster_redacted.py'}}),
        ('tool bridge context', {'tool_input': {'command': './dmnitel ai-context'}}),
        ('route tool', {'tool_input': {'command': './dmnitel route-tool --query "COREQ audit"'}}),
        ('unittest discover', {'tool_input': {'command': 'PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests'}}),
    ]
    results: list[Result] = []
    for case_name, event in denied:
        proc = run_hook(script, event, cwd=repo)
        results.append(expect(f'pre tool denies: {case_name}', permission_denied(proc), proc.stdout[:180]))
    for case_name, event in allowed:
        proc = run_hook(script, event, cwd=repo)
        results.append(expect(f'pre tool allows: {case_name}', proc.returncode == 0 and proc.stdout == '', f'exit={proc.returncode} stdout={proc.stdout[:120]!r}'))
    return results


def test_post_tool_use(repo: Path) -> list[Result]:
    script = repo / '.codex/hooks/post_tool_use_review.py'
    cases = [
        ('traceback', {'tool_response': 'Traceback (most recent call last)'}, True),
        ('alternate output', {'result': {'stderr': 'FATAL: transcript parser failed'}}, True),
        ('secret leak', {'tool_response': 'token sk-' + 'A' * 32}, True),
        ('clean output', {'tool_response': 'all good'}, False),
    ]
    results: list[Result] = []
    for case_name, event, should_flag in cases:
        proc = run_hook(script, event, cwd=repo)
        flagged = 'additionalContext' in proc.stdout
        results.append(expect(f'post tool: {case_name}', flagged is should_flag, proc.stdout[:180]))
    return results


def test_stop_and_claim_check(repo: Path) -> list[Result]:
    stop_script = repo / '.codex/hooks/stop_verify.py'
    results: list[Result] = []
    unsourced = run_hook(stop_script, {'last_assistant_message': 'Nitel kol 7 aileden oluşur.'}, cwd=repo)
    sourced = run_hook(stop_script, {'last_assistant_message': 'Nitel kol 7 aileden oluşur [1].'}, cwd=repo)
    loop = run_hook(stop_script, {'stop_hook_active': True, 'last_assistant_message': 'Nitel kol 21 görüşme içerir.'}, cwd=repo)
    qualitative = run_hook(stop_script, {'last_assistant_message': 'Nitel kol 21 görüşme içerir.'}, cwd=repo)
    results.extend([
        expect('stop blocks unsourced family count', json_stdout(unsourced).get('decision') == 'block', unsourced.stdout[:180]),
        expect('stop allows sourced family count', json_stdout(sourced).get('continue') is True, sourced.stdout[:180]),
        expect('stop avoids loops', json_stdout(loop).get('continue') is True, loop.stdout[:180]),
        expect('stop blocks unsourced qualitative metric', json_stdout(qualitative).get('decision') == 'block', qualitative.stdout[:180]),
    ])

    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(repo)
    proc = subprocess.run(
        [
            'python3',
            '-c',
            (
                'from reliability.verify.claim_check import verify_message;'
                'import json;'
                'claims = [' + ','.join(repr(claim) for claim in QUAL_NUMERIC_CLAIMS) + '];'
                'print(json.dumps([verify_message(claim) for claim in claims], ensure_ascii=False))'
            ),
        ],
        cwd=repo,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    if proc.returncode != 0:
        results.append(expect('claim_check imports', False, proc.stderr[:240]))
    else:
        payload = json.loads(proc.stdout)
        results.append(expect('claim_check blocks qualitative numeric claims', all(item.get('ok') is False for item in payload), proc.stdout[:240]))
    return results


def test_session_start(repo: Path) -> list[Result]:
    script = repo / '.codex/hooks/session_start.py'
    proc = run_hook(script, {'source': 'startup'}, cwd=repo)
    context = json_stdout(proc).get('hookSpecificOutput', {}).get('additionalContext', '')
    return [expect('session start injects qualitative conventions', 'T1DM Niteliksel AI reliability conventions' in context, context[:180])]


def test_roster_redaction(repo: Path) -> list[Result]:
    path = repo / '.codex/tools/codex_mcp_roster_redacted.py'
    spec = importlib.util.spec_from_file_location('roster_redacted', path)
    if spec is None or spec.loader is None:
        return [expect('roster module loads', False)]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sample = 'sk-' + 'A' * 32 + ' github_pat_' + 'B' * 48
    redacted = module.redact(sample)
    return [
        expect('roster redacts OpenAI key', 'sk-[REDACTED]' in redacted),
        expect('roster redacts GitHub token', 'github_pat_[REDACTED]' in redacted),
    ]


def run_all() -> list[Result]:
    repo = qualitative_root()
    results: list[Result] = []
    results += test_repo_markers(repo)
    results += test_config(repo)
    results += test_plugin_manifests(repo)
    results += test_user_prompt_submit(repo)
    results += test_pre_tool_use(repo)
    results += test_post_tool_use(repo)
    results += test_stop_and_claim_check(repo)
    results += test_session_start(repo)
    results += test_roster_redaction(repo)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Emit machine-readable JSON.')
    args = parser.parse_args()

    results = run_all()
    failures = [result for result in results if not result.ok]
    if args.json:
        print(json.dumps([result.__dict__ for result in results], ensure_ascii=False, indent=2))
    else:
        for result in results:
            status = 'PASS' if result.ok else 'FAIL'
            suffix = f' -- {result.detail}' if result.detail else ''
            print(f'{status} {result.name}{suffix}')
        print(f'\n{len(results) - len(failures)}/{len(results)} passed')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
