#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="${ROOT}/skills/codex-quota-optimizer"
DEST="${HOME}/.agents/skills/codex-quota-optimizer"
BIN_DIR="${HOME}/.local/bin"
CLI_SRC="${DEST}/scripts/cqo.py"
CLI_DEST="${BIN_DIR}/cqo"

if [[ ! -d "$SRC" ]]; then
  echo "Skill source not found: $SRC" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"

mkdir -p "$BIN_DIR"
chmod +x "$CLI_SRC"
ln -sfn "$CLI_SRC" "$CLI_DEST"

echo "Installed codex-quota-optimizer to $DEST"
echo "Installed optional cqo CLI to $CLI_DEST"
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
  echo "Note: add $BIN_DIR to PATH to run 'cqo' directly."
fi
echo "Restart Codex if the skill does not appear immediately."
