#!/usr/bin/env bash
# PostToolUse hook — Ruff linting feedback to Claude
set -euo pipefail

FILE_PATH=$(jq -r '.tool_input.file_path // empty')

# Only process Python files
if [[ "$FILE_PATH" == *.py ]]; then
    OUTPUT=$(ruff check "$FILE_PATH" 2>&1) || true
    if [[ -n "$OUTPUT" ]]; then
        echo "$OUTPUT" >&2
        exit 2
    fi
fi

exit 0
