#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="${ROOT}/skills/codex-quota-optimizer"
DEST="${HOME}/.agents/skills/codex-quota-optimizer"

if [[ ! -d "$SRC" ]]; then
  echo "Skill source not found: $SRC" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"

echo "Installed codex-quota-optimizer to $DEST"
echo "Restart Codex if the skill does not appear immediately."
