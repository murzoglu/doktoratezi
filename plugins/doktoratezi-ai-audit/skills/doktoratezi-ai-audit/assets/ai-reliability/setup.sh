#!/usr/bin/env bash
# =============================================================================
# AI Reliability scaffold — one-command bootstrap.
#
#   ./setup.sh                 # wire into the CURRENT git repo (.codex local)
#   ./setup.sh --global        # also install hooks into ~/.codex (all repos)
#   ./setup.sh --observability  # also start the self-hosted Langfuse stack
#
# Idempotent: safe to re-run. It never overwrites an existing config without
# backing it up to *.bak first.
# =============================================================================
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GLOBAL=0
OBS=0
for arg in "$@"; do
  case "$arg" in
    --global) GLOBAL=1 ;;
    --observability) OBS=1 ;;
    *) echo "unknown flag: $arg"; exit 1 ;;
  esac
done

say() { printf '\033[1;36m▶ %s\033[0m\n' "$1"; }
warn() { printf '\033[1;33m! %s\033[0m\n' "$1"; }

# --- 0. Preconditions --------------------------------------------------------
say "Checking prerequisites"
command -v python3 >/dev/null || { echo "python3 required"; exit 1; }
command -v git >/dev/null || { echo "git required"; exit 1; }
command -v codex >/dev/null || warn "codex CLI not found on PATH (hooks will still install)."
command -v npx >/dev/null || warn "npx not found — promptfoo evals need Node 20+."

# --- 1. Python environment ---------------------------------------------------
say "Setting up Python venv + deps"
python3 -m venv "$HERE/.venv"
# shellcheck disable=SC1091
source "$HERE/.venv/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet -r "$HERE/requirements.txt" || warn "Some deps failed; verifiers degrade gracefully."

# --- 2. Make hooks executable ------------------------------------------------
say "Marking hooks executable"
chmod +x "$HERE/.codex/hooks/"*.py

# --- 3. Wire .codex into the target repo -------------------------------------
backup() { [ -f "$1" ] && cp "$1" "$1.bak.$(date +%s)" && warn "backed up $1"; }

install_codex_layer() {
  local dest_dir="$1"
  mkdir -p "$dest_dir/hooks"
  backup "$dest_dir/config.toml"
  backup "$dest_dir/hooks.json"
  cp "$HERE/.codex/config.toml" "$dest_dir/config.toml"
  cp "$HERE/.codex/hooks.json"  "$dest_dir/hooks.json"
  cp "$HERE/.codex/hooks/"*.py  "$dest_dir/hooks/"
  chmod +x "$dest_dir/hooks/"*.py
  say "Installed Codex hooks into $dest_dir"
}

REPO_ROOT="$(git -C "$HERE" rev-parse --show-toplevel 2>/dev/null || echo "$HERE")"
install_codex_layer "$REPO_ROOT/.codex"
[ "$GLOBAL" -eq 1 ] && install_codex_layer "$HOME/.codex"

# --- 4. Enable the hooks feature flag ---------------------------------------
if command -v codex >/dev/null; then
  say "Enabling the hooks feature flag"
  codex features enable hooks 2>/dev/null \
    || codex features enable codex_hooks 2>/dev/null \
    || warn "Could not toggle via 'codex features'; the [features] block in config.toml already sets it."
  warn "First launch only: run /hooks inside Codex to REVIEW and TRUST these hooks."
fi

# --- 5. Optional: observability stack ---------------------------------------
if [ "$OBS" -eq 1 ]; then
  if command -v docker >/dev/null; then
    say "Starting self-hosted Langfuse (http://localhost:3000)"
    docker compose -f "$HERE/reliability/observability/docker-compose.langfuse.yml" up -d
  else
    warn "docker not found — skipping Langfuse."
  fi
fi

# --- 6. Smoke test -----------------------------------------------------------
say "Smoke-testing hooks and verifier"
python -m py_compile "$HERE/.codex/hooks/"*.py "$HERE/reliability/verify/"*.py
echo '{"hook_event_name":"UserPromptSubmit","prompt":"hello sk-ABCDEFGHIJKLMNOPQRSTUV"}' \
  | python3 "$HERE/.codex/hooks/user_prompt_submit.py" && echo "  (secret scan: did NOT block — unexpected)" \
  || echo "  (secret scan: correctly blocked a fake key)"

cat <<'NEXT'

✔ Done. Next steps:
  1. In Codex, run  /hooks  once and TRUST the hooks.
  2. source reliability/observability/otel.env   (before running agents)
  3. npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml
  4. Configure a verifier backend (LYNX_BACKEND=local|ollama|patronus) and
     export RELIABILITY_DEEP_VERIFY=1 to turn on heavy claim verification.
  5. Grow reliability/evals/golden/dataset.yaml — it is your reliability asset.

What is runnable now vs. needs your keys:
  • Runnable now: all 5 hooks, secret-scan, deny-list, local grounding gate,
    promptfoo structure, OTel env, Langfuse self-host, governance map.
  • Needs your keys/hosting: Lynx (self-host or Patronus), RAGAS judge model,
    semantic-entropy sampler + NLI model, any hosted eval provider.
NEXT
