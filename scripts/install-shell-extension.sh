#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/gnome-shell/extensions/capsule@rebuntu"
mkdir -p "$DEST"
install -m 0644 "$ROOT/capsule/shell/extension/extension.js" "$DEST/extension.js"
install -m 0644 "$ROOT/capsule/shell/extension/metadata.json" "$DEST/metadata.json"
printf 'Installed %s\nLog out and back in if GNOME Shell has not loaded the extension.\n' "$DEST"
printf 'Then run: gnome-extensions enable capsule@rebuntu\n'
