#!/usr/bin/env bash
# Prepare a temporary CWD with the fixtures required by a given eval id.
# Usage: ./setup-eval-cwd.sh <eval-id>
# Prints the absolute path of the created CWD on stdout.

set -euo pipefail

TEMPLATE_PATH="${CRUFT_TEMPLATE_PATH:-$HOME/python-project-template-v2}"

usage() {
    cat >&2 <<EOF
Usage: $0 <eval-id>

Eval ids (see claude-md.eval.json):
  trigger-positive-cruft-instance       Fresh Cruft instance from \$TEMPLATE_PATH
  trigger-negative-user-global-conventions  Minimal empty CWD
  trigger-edge-existing-claude-md       CWD with a pre-existing CLAUDE.md + src/

Env vars:
  CRUFT_TEMPLATE_PATH   Override template path (default: ~/python-project-template-v2)
EOF
    exit 2
}

if [[ $# -ne 1 ]]; then
    usage
fi

EVAL_ID="$1"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
CWD="/tmp/claude-md-eval-${EVAL_ID}-${TIMESTAMP}"

case "$EVAL_ID" in
    trigger-positive-cruft-instance)
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
        # cruft create generates the project in a subdirectory named after the
        # cookiecutter project_slug; we run non-interactively and accept defaults.
        # The user may need to answer prompts depending on the template config.
        cruft create "$TEMPLATE_PATH" --output-dir "$CWD" >&2
        # Move generated project content to CWD root for a clean test environment.
        GENERATED_DIR="$(find "$CWD" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
        if [[ -n "$GENERATED_DIR" && -d "$GENERATED_DIR" ]]; then
            shopt -s dotglob
            mv "$GENERATED_DIR"/* "$CWD/"
            rmdir "$GENERATED_DIR"
        fi
        ;;

    trigger-negative-user-global-conventions)
        mkdir -p "$CWD"
        ;;

    trigger-edge-existing-claude-md)
        mkdir -p "$CWD/src"
        touch "$CWD/CLAUDE.md"
        ;;

    *)
        echo "error: unknown eval id '$EVAL_ID'" >&2
        usage
        ;;
esac

echo "$CWD"
