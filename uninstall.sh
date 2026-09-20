#!/usr/bin/env bash
set -euo pipefail

DEST="${HOME}/.agents/skills/codex-quota-optimizer"
CLI_DEST="${HOME}/.local/bin/cqo"

if [[ -L "$CLI_DEST" ]]; then
  TARGET="$(readlink "$CLI_DEST" || true)"
  if [[ "$TARGET" == *"/.agents/skills/codex-quota-optimizer/scripts/cqo.py" ]]; then
    rm -f "$CLI_DEST"
    echo "Removed $CLI_DEST"
  fi
fi

rm -rf "$DEST"
echo "Removed $DEST"
echo "Local CQO journal under ~/.cqo was preserved."
