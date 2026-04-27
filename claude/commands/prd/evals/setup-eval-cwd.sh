#!/usr/bin/env bash
# Prepare a temporary CWD with the fixtures required by a given eval id.
# Usage: ./setup-eval-cwd.sh <eval-id>
# Prints the absolute path of the created CWD on stdout.

set -euo pipefail

TEMPLATE_PATH="${CRUFT_TEMPLATE_PATH:-$HOME/python-project-template-v2}"

usage() {
    cat >&2 <<EOF
Usage: $0 <eval-id>

Eval ids (see prd.eval.json):
  strict-mode-existing-prd      CWD with a pre-existing PRD.md (strict-mode gate)
  preflight-cruft-instance      Fresh Cruft instance from \$TEMPLATE_PATH
  no-preflight-empty-cwd        Empty CWD (no .cruft.json, no PRD.md)

Env vars:
  CRUFT_TEMPLATE_PATH           Override template path (default: ~/python-project-template-v2)
EOF
    exit 2
}

if [[ $# -ne 1 ]]; then
    usage
fi

EVAL_ID="$1"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
CWD="/tmp/prd-eval-${EVAL_ID}-${TIMESTAMP}"

case "$EVAL_ID" in
    strict-mode-existing-prd)
        mkdir -p "$CWD"
        cat > "$CWD/PRD.md" <<'EOF'
# PRD — placeholder

This is a placeholder PRD used as a fixture for the strict-mode-existing-prd
eval. Its content is intentionally minimal — the eval only cares that PRD.md
exists, not its content.
EOF
        ;;

    preflight-cruft-instance)
        if [[ ! -d "$TEMPLATE_PATH" ]]; then
            echo "error: template not found at $TEMPLATE_PATH" >&2
            echo "hint: set CRUFT_TEMPLATE_PATH or clone the template locally" >&2
            exit 1
        fi
        if ! command -v cruft >/dev/null 2>&1; then
            echo "error: cruft not installed (try: uv tool install cruft)" >&2
            exit 1
        fi
        mkdir -p "$CWD"
        cd "$CWD"
        cruft create "$TEMPLATE_PATH" --output-dir "$CWD" >&2
        # Move generated project content to CWD root for a clean test environment.
        GENERATED_DIR="$(find "$CWD" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
        if [[ -n "$GENERATED_DIR" && -d "$GENERATED_DIR" ]]; then
            shopt -s dotglob
            mv "$GENERATED_DIR"/* "$CWD/"
            rmdir "$GENERATED_DIR"
        fi
        # Strict-mode gate would block the eval if PRD.md exists in the template.
        if [[ -f "$CWD/PRD.md" ]]; then
            rm "$CWD/PRD.md"
        fi
        ;;

    no-preflight-empty-cwd)
        mkdir -p "$CWD"
        ;;

    *)
        echo "error: unknown eval id '$EVAL_ID'" >&2
        usage
        ;;
esac

echo "$CWD"
