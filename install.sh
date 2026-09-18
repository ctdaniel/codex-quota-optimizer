#!/usr/bin/env bash
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/.agents/skills/codex-quota-optimizer"
DEST="${HOME}/.agents/skills/codex-quota-optimizer"
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"
echo "Installed codex-quota-optimizer to $DEST"
echo "Restart Codex if the skill does not appear immediately."
