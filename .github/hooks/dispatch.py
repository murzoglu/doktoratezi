#!/usr/bin/env python3
"""Copilot hook -> depo `.claude/hooks/` köprüsü.

Copilot CLI proje hook'larını **git kökündeki `.github/hooks/*.json`** dosyalarından
yükler ve Claude Code olay adlarını (`SessionStart`, `PreToolUse`, …) otomatik olarak
Copilot adlarına çevirip `_vsCodeCompat` bayrağını kendisi koyar. Bu sayede payload
biçimi Claude Code'unkiyle aynıdır ve `.claude/hooks/*.py` betikleri DEĞİŞMEDEN
çalışır. Geriye iki **çıktı sözleşmesi** farkı kalır; bu köprü onları çevirir:

  1. Bloklama: Claude'da `exit 2 + stderr` evrensel blok sinyalidir. Copilot bunu
     yalnız "uyarı" sayar (HookCommandWarningError) ve turu durdurmaz — yani sır
     taraması sessizce etkisizleşirdi. Burada exit 2, olaya uygun Copilot JSON
     kararına çevrilir.
  2. Bağlam enjeksiyonu: Claude `hookSpecificOutput.additionalContext` yazar;
     Copilot'un sessionStart/postToolUse çıktı dönüştürücüsü ise ÜST DÜZEY
     `additionalContext` okur. Burada alan üst düzeye taşınır.
     (`preToolUse` istisnadır: orada `hookSpecificOutput.permissionDecision`
     Copilot tarafından yerel olarak okunur.)

Betikler kopyalanmaz: depodaki `.claude/hooks/` tek doğruluk kaynağıdır
(ikizi `.codex/hooks/`). Depo parmak izi tutmazsa köprü sessizce çıkar.

Kullanım:
    dispatch.py <betik_adi> <copilot_olay_anahtari> [zaman_asimi_sn]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

# Depo parmak izi: bu üçü birden yoksa plugin bu ağaçta çalışmaz (fail-open).
FINGERPRINT = (".claude/hooks", "tez-yazim", "_targets.R")


def _candidate_dirs(payload: dict) -> list:
    seen, out = set(), []
    for cand in (
        payload.get("cwd"),
        os.environ.get("CLAUDE_PROJECT_DIR"),
        os.environ.get("COPILOT_PROJECT_DIR"),
        os.getcwd(),
    ):
        if cand and cand not in seen:
            seen.add(cand)
            out.append(cand)
    return out


def find_repo_root(payload: dict, script: str) -> str | None:
    """Payload cwd'sinden yukarı yürüyerek tez deposunu bul."""
    for start in _candidate_dirs(payload):
        cur = os.path.abspath(start)
        while True:
            if all(os.path.exists(os.path.join(cur, p)) for p in FINGERPRINT) and os.path.isfile(
                os.path.join(cur, ".claude", "hooks", script)
            ):
                return cur
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
    return None


def block_payload(event: str, reason: str) -> dict:
    """Claude exit-2 blokunu Copilot'un olay-özel karar biçimine çevir."""
    if event == "preToolUse":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    if event == "sessionStart":
        return {"additionalContext": reason}
    return {"decision": "block", "reason": reason}


def lift_additional_context(obj: dict) -> dict:
    """hookSpecificOutput.additionalContext -> üst düzey additionalContext."""
    hso = obj.get("hookSpecificOutput")
    if isinstance(hso, dict):
        ctx = hso.get("additionalContext")
        if ctx is not None and obj.get("additionalContext") is None:
            obj["additionalContext"] = ctx if isinstance(ctx, str) else json.dumps(ctx)
    return obj


def main() -> int:
    if len(sys.argv) < 3:
        sys.stderr.write("dispatch.py: <betik_adi> <copilot_olay_anahtari> [zaman_asimi_sn]\n")
        return 0

    script, event = sys.argv[1], sys.argv[2]
    try:
        budget = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    except ValueError:
        budget = 0.0

    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}

    root = find_repo_root(payload, script)
    if root is None:
        return 0  # Bu ağaç tez deposu değil: plugin etkisiz.

    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = root
    env["COPILOT_PROJECT_DIR"] = root
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    try:
        proc = subprocess.run(
            [sys.executable, os.path.join(root, ".claude", "hooks", script)],
            input=raw,
            text=True,
            capture_output=True,
            cwd=root,
            env=env,
            timeout=(budget - 2) if budget > 3 else None,
        )
    except subprocess.TimeoutExpired:
        sys.stderr.write(f"[copilot-tez-guard] {script} zaman aşımına uğradı; fail-open.\n")
        return 0
    except Exception as exc:  # noqa: BLE001 - hook asla turu çökertmemeli
        sys.stderr.write(f"[copilot-tez-guard] {script} çalıştırılamadı: {exc}\n")
        return 0

    if proc.stderr:
        sys.stderr.write(proc.stderr)

    out = proc.stdout.strip()
    parsed = None
    if out:
        try:
            parsed = json.loads(out)
        except json.JSONDecodeError:
            parsed = None

    if isinstance(parsed, dict):
        sys.stdout.write(json.dumps(lift_additional_context(parsed), ensure_ascii=False))
        return 0

    if proc.returncode == 2:
        reason = proc.stderr.strip() or f"{script} isteği engelledi."
        sys.stdout.write(json.dumps(block_payload(event, reason), ensure_ascii=False))
        return 0

    if out:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
