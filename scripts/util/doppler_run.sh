#!/usr/bin/env bash
# Run a repository command with Doppler-injected secrets.
set -euo pipefail

project="${DOPPLER_PROJECT:-cureohub}"
config="${DOPPLER_CONFIG:-dev_personal}"

if (($# == 0)); then
  printf 'Usage: %s <command> [args...]\n' "${0##*/}" >&2
  exit 64
fi

if ! command -v doppler >/dev/null 2>&1; then
  printf 'doppler CLI is required.\n' >&2
  exit 69
fi

exec doppler run \
  --no-fallback \
  --project "$project" \
  --config "$config" \
  -- "$@"
