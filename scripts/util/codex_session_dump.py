#!/usr/bin/env python3
"""
~/.codex/sessions/ altındaki rollout JSONL dosyalarından Codex sohbetini
Markdown'a çevirir. VS Code Codex extension server overload veya
oturum açılamadığında lokal kurtarma için.

Kullanım:
    python3 codex_session_dump.py --list               # son 30 sohbet
    python3 codex_session_dump.py --list --grep tez    # başlık/içerik filtre
    python3 codex_session_dump.py <session-id-prefix>  # markdown çıkar
    python3 codex_session_dump.py <id> -o sohbet.md    # dosyaya yaz
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

CODEX_ROOT = Path.home() / ".codex" / "sessions"


def find_rollout(id_prefix: str) -> Path | None:
    matches = list(CODEX_ROOT.rglob(f"rollout-*{id_prefix}*.jsonl"))
    if not matches:
        return None
    if len(matches) > 1:
        print(f"[uyarı] {len(matches)} eşleşme; en yenisi seçiliyor", file=sys.stderr)
        matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0]


def iter_records(path: Path):
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    parts = []
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict):
                if "text" in c:
                    parts.append(c["text"])
                elif c.get("type") == "input_text" and "text" in c:
                    parts.append(c["text"])
    return "\n".join(parts)


def to_markdown(path: Path) -> str:
    out = [f"# Codex Session: {path.name}\n"]
    for rec in iter_records(path):
        rtype = rec.get("type")
        ts = rec.get("timestamp", "")
        payload = rec.get("payload", {})
        if rtype == "session_meta":
            cwd = payload.get("cwd", "?")
            instructions = payload.get("instructions", "")
            out.append(f"_started: {ts}_  ·  _cwd: `{cwd}`_\n")
            if instructions:
                out.append(f"<details><summary>system instructions</summary>\n\n```\n{instructions[:2000]}\n```\n</details>\n")
        elif rtype == "response_item":
            ptype = payload.get("type")
            if ptype == "message":
                role = payload.get("role", "?")
                text = extract_text(payload.get("content", []))
                if not text.strip():
                    continue
                out.append(f"\n---\n\n### {role}  · {ts}\n\n{text}\n")
            elif ptype == "function_call":
                name = payload.get("name", "?")
                args = payload.get("arguments", "")
                out.append(f"\n> **tool call** `{name}`  · {ts}\n```\n{args[:1500]}\n```\n")
            elif ptype == "function_call_output":
                output = payload.get("output", "")
                if isinstance(output, dict):
                    output = output.get("content", "") or json.dumps(output)[:1500]
                out.append(f"\n> **tool output**  · {ts}\n```\n{str(output)[:1500]}\n```\n")
            elif ptype == "reasoning":
                summary = payload.get("summary", [])
                texts = [extract_text(s) for s in summary] if isinstance(summary, list) else []
                joined = "\n".join(t for t in texts if t)
                if joined:
                    out.append(f"\n<sub>_reasoning · {ts}_</sub>\n<details>\n\n{joined}\n</details>\n")
        elif rtype == "event_msg":
            kind = payload.get("type", "")
            if kind == "user_message":
                text = payload.get("message", "")
                if text:
                    out.append(f"\n---\n\n### user · {ts}\n\n{text}\n")
            elif kind == "agent_message":
                text = payload.get("message", "")
                if text:
                    out.append(f"\n---\n\n### assistant · {ts}\n\n{text}\n")
    return "\n".join(out)


def list_sessions(grep: str | None, limit: int) -> None:
    rolls = sorted(CODEX_ROOT.rglob("rollout-*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    shown = 0
    for p in rolls:
        if shown >= limit:
            break
        # parse first user-ish text for preview
        first_user = ""
        for rec in iter_records(p):
            ptype = rec.get("payload", {}).get("type")
            role = rec.get("payload", {}).get("role")
            if ptype == "message" and role == "user":
                first_user = extract_text(rec["payload"].get("content", []))[:100]
                break
        sid = p.name.split("-", 7)[-1].replace(".jsonl", "") if "-" in p.name else p.stem
        # extract uuid (last 5 hyphenated groups)
        parts = p.stem.split("-")
        if len(parts) >= 5:
            sid = "-".join(parts[-5:])
        mtime = datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="minutes")
        line = f"{mtime}  {sid}  {first_user}"
        if grep and grep.lower() not in line.lower():
            continue
        print(line)
        shown += 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("session_id", nargs="?", help="session UUID (tam veya prefix)")
    ap.add_argument("--list", action="store_true", help="son sohbetleri listele")
    ap.add_argument("--grep", help="--list ile birlikte; başlık/önizlemede filtrele")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("-o", "--output", help="markdown'ı dosyaya yaz")
    args = ap.parse_args()

    if not CODEX_ROOT.exists():
        print(f"[hata] {CODEX_ROOT} yok", file=sys.stderr)
        return 1

    if args.list:
        list_sessions(args.grep, args.limit)
        return 0

    if not args.session_id:
        ap.print_help()
        return 2

    path = find_rollout(args.session_id)
    if not path:
        print(f"[hata] '{args.session_id}' eşleşen rollout bulunamadı", file=sys.stderr)
        return 1

    md = to_markdown(path)
    if args.output:
        Path(args.output).write_text(md)
        print(f"yazıldı: {args.output} ({len(md)} karakter)")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
