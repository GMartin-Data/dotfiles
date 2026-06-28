#!/usr/bin/env bash
# PreToolUse hook — Block git push --force
set -euo pipefail

COMMAND=$(jq -r '.tool_input.command // empty')

# Match --force / --force-with-lease / -f only as isolated option tokens
# (a word starting with '-' after push), never as a substring of an argument
# such as a branch name (e.g. feat/x-frontmatter, release/v2-final).
#   (^|[[:space:]])      option token starts at line start or after a space
#   --force(-with-lease)? long forms (with optional -with-lease suffix)
#   -[a-z]*f[a-z]*       short option group containing f (-f, -fu, -uf, ...)
if echo "$COMMAND" | grep -qsw push \
   && echo "$COMMAND" | grep -qE '(^|[[:space:]])(--force(-with-lease)?|-[a-z]*f[a-z]*)([[:space:]]|$)'; then
    echo "BLOCKED: git push --force is not allowed. Use regular push." >&2
    exit 2
fi

exit 0
