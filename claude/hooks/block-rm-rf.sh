#!/usr/bin/env bash
# PreToolUse hook — Block rm -rf
set -euo pipefail

COMMAND=$(jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -qE '\brm\s+.*-(rf|fr)\b|\brm\s+-(rf|fr)\b'; then
    echo "BLOCKED: rm -rf is not allowed. Use rm with explicit paths." >&2
    exit 2
fi

exit 0
