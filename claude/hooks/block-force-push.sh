#!/usr/bin/env bash
# PreToolUse hook — Block git push --force
set -euo pipefail

COMMAND=$(jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -qE 'push\s+.*(-f|--force)|push\s+(-f|--force)'; then
    echo "BLOCKED: git push --force is not allowed. Use regular push." >&2
    exit 2
fi

exit 0
