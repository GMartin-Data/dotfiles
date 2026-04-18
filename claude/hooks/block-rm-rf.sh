#!/usr/bin/env bash
# PreToolUse hook — Block destructive rm flags.
# Scope narrowed to `Bash(rm *)` via `if:` in settings.json, so we only
# need to detect dangerous flags — not re-verify this is an rm command.
#
# Dangerous flags for rm are: -r, -R (recursive), -f (force),
# and their long forms --recursive, --force.
# Note: -F is NOT an rm flag (it's used by other commands like git commit),
# so we treat force as lowercase f only.
set -euo pipefail

COMMAND=$(jq -r '.tool_input.command // empty')

# Each flag must be a standalone shell token: preceded by start-of-string
# or whitespace, and followed by end-of-string or whitespace.
# Combined-flag form requires at least one char from [rRf] in the token.
if echo " $COMMAND " | grep -qE -- '[[:space:]]-[a-zA-Z]*[rRf][a-zA-Z]*[[:space:]]|[[:space:]]--recursive([[:space:]=]|$)|[[:space:]]--force([[:space:]=]|$)'; then
    echo "BLOCKED: rm with recursive/force flags is not allowed. Use rm with explicit paths." >&2
    exit 2
fi

exit 0
