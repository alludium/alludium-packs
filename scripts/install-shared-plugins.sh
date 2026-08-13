#!/usr/bin/env bash

set -euo pipefail

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI is required to install the shared Alludium plugin." >&2
  exit 1
fi

if codex plugin marketplace list --json | grep -Eq '"name"[[:space:]]*:[[:space:]]*"alludium"'; then
  codex plugin marketplace upgrade alludium
else
  codex plugin marketplace add alludium/alludium-claude-marketplace --ref main
fi

codex plugin add platform-investigation@alludium
