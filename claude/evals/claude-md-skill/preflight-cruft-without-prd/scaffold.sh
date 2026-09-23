#!/usr/bin/env bash
# Fresh Cruft instance in the run workspace, no PRD.md: the conditional gate must abort.
set -euo pipefail

# The runner swaps HOME for a sandbox home: resolve the real one for the template and uv tools.
REAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
TEMPLATE="${CRUFT_TEMPLATE_PATH:-$REAL_HOME/python-project-template-v2}"
[[ -d "$TEMPLATE" ]] || { echo "template not found: $TEMPLATE (set CRUFT_TEMPLATE_PATH)" >&2; exit 1; }
CRUFT="$(command -v cruft || echo "$REAL_HOME/.local/bin/cruft")"
[[ -x "$CRUFT" ]] || { echo "cruft not installed (uv tool install cruft)" >&2; exit 1; }

"$CRUFT" create "$TEMPLATE" --output-dir "$PWD" --no-input >&2
generated="$(find "$PWD" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
shopt -s dotglob
mv "$generated"/* "$PWD"/
rmdir "$generated"
# The template generates no PRD.md today; guard the fixture against a future change.
rm -f "$PWD/PRD.md"
