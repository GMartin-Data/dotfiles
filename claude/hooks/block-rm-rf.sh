#!/usr/bin/env bash
# PreToolUse hook — Block destructive rm flags (-r/-R/-f, --recursive/--force).
#
# IMPORTANT: the `if: "Bash(rm *)"` scope in settings.json is best-effort and
# FAIL-OPEN — Claude Code runs this hook on compound commands (pipes, &&, $(),
# leading assignments) whenever it cannot prove they are NOT rm. So the hook
# MUST re-verify that an actual `rm` command word is present before judging
# flags; otherwise it false-positives on cp -r, ls -lr, grep --recursive, etc.
#
# Strategy: split the command on shell separators / substitutions, locate the
# `rm` command word in each segment (rm or */rm, after optional VAR=val and
# launchers like sudo/xargs), and inspect ONLY the tokens that follow rm.
set -euo pipefail

COMMAND=$(jq -r '.tool_input.command // empty')

verdict=$(printf '%s\n' "$COMMAND" \
    | sed -E 's/\$\(/\n/g; s/`/\n/g; s/[;&|]+/\n/g' \
    | awk '
    {
        n = split($0, tok, /[[:space:]]+/)
        rmi = 0
        for (i = 1; i <= n; i++) {
            t = tok[i]
            if (t == "") continue
            if (t ~ /^[A-Za-z_][A-Za-z0-9_]*=/) continue          # VAR=val
            if (t == "rm" || t ~ /\/rm$/) { rmi = i; break }      # rm command word
            if (t == "xargs" || t == "sudo" || t == "time" || \
                t == "env" || t == "nice" || t == "nohup") continue  # launcher
            break                                                  # other command
        }
        if (rmi == 0) next
        for (j = rmi + 1; j <= n; j++) {
            f = tok[j]
            if (f == "") continue
            if (f == "--recursive" || f == "--force") { print "BLOCK"; exit }
            if (f ~ /^-[A-Za-z]*[rRf][A-Za-z]*$/) { print "BLOCK"; exit }
        }
    }')

if [ "$verdict" = "BLOCK" ]; then
    echo "BLOCKED: rm with recursive/force flags is not allowed. Use rm with explicit paths." >&2
    exit 2
fi

exit 0
