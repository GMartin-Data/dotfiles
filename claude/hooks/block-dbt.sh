#!/usr/bin/env bash
# PreToolUse hook — dbt is only ever run through the `dbt` subagent (MCP dbt-enveloppe).
#
# Registered WITHOUT an `if:` scope on purpose: `Bash(dbt *)` would miss
# `uv run dbt`, `python -m dbt`, `sh -c '…'` and absolute paths (permissions doc).
#
# Strategy, as in block-rm-rf.sh: split each line into simple commands, then
# judge the COMMAND POSITION of every segment so that quoted text
# (`git commit -m "… dbt build …"`, `grep "ls|dbt"`) passes. Quotes protect
# separators, but `$(` and backticks still open a segment inside double quotes.
# Behind a launcher (uv, python, sh, timeout, …) every remaining token is
# inspected, because launcher options cannot be told apart from the command
# they launch — fail-closed. Heredoc bodies fed to an ordinary command (cat,
# git, tee) are skipped; fed to a launcher (`bash <<EOF`) they stay inspected.
set -euo pipefail

COMMAND=$(jq -r '.tool_input.command // empty')

verdict=$(printf '%s\n' "$COMMAND" | awk '
    BEGIN {
        split("uv uvx pipx poetry pdm hatch pixi conda mamba run tool " \
              "sh bash zsh dash ksh exec command builtin eval " \
              "sudo env time nice nohup timeout stdbuf xargs", l, " ")
        for (k in l) LAUNCHERS[l[k]] = 1
        split("", seg)
        skip = ""; inspect = 0
    }
    function block() { print "BLOCK"; exit }
    function clean(t) { gsub(/^[\042\047({]+|[\042\047)}]+$/, "", t); return t }
    function is_launcher(t) { return (t in LAUNCHERS) || t ~ /(^|\/)python[0-9.]*$/ }
    function dbtish(t, loose) { return t == "dbt" || t ~ /\/dbt$/ || (loose && t ~ /^dbt\./) }
    function segments(line, seg,    i, c, q, cur, n, len) {
        n = 0; cur = ""; q = ""; len = length(line)
        for (i = 1; i <= len; i++) {
            c = substr(line, i, 1)
            if (q == "\047") { cur = cur c; if (c == q) q = ""; continue }
            if (c == "\\") { cur = cur c substr(line, i + 1, 1); i++; continue }
            if (c == "\047" && q == "") { q = c; cur = cur c; continue }
            if (c == "\042") { q = (q == "") ? c : ""; cur = cur c; continue }
            if (c == "`" || (c == "$" && substr(line, i + 1, 1) == "(")) {
                seg[++n] = cur; cur = ""; if (c == "$") i++; continue
            }
            if (q == "" && (c == ";" || c == "&" || c == "|")) { seg[++n] = cur; cur = ""; continue }
            cur = cur c
        }
        seg[++n] = cur
        return n
    }
    function heredoc_delim(seg,    d) {
        gsub(/<<<[^[:space:]]*/, " ", seg)                      # here-strings are not heredocs
        if (!match(seg, /<<-?[\042\047]?[A-Za-z_][A-Za-z0-9_]*[\042\047]?/)) return ""
        d = substr(seg, RSTART, RLENGTH); sub(/^<<-?/, "", d); gsub(/[\042\047]/, "", d)
        return d
    }
    function scan_loose(text,    n, tok, i) {
        n = split(text, tok, /[[:space:];&|`$(){}]+/)
        for (i = 1; i <= n; i++) if (dbtish(clean(tok[i]), 1)) block()
    }
    function analyze(seg, line,    n, tok, i, t, launch, bare, d) {
        launch = 0; bare = 0
        n = split(seg, tok, /[[:space:]]+/)
        for (i = 1; i <= n; i++) {
            t = clean(tok[i])
            if (t == "") continue
            if (t ~ /^[A-Za-z_][A-Za-z0-9_]*=/) continue             # VAR=val
            if (dbtish(t, launch)) block()
            if (is_launcher(t)) { launch = 1; bare = 1; continue }
            if (!launch) break                                       # ordinary command: arguments are data
            if (t !~ /^-/) bare = 0
        }
        d = heredoc_delim(seg)
        if (d != "") { skip = d; inspect = launch }
        else if (launch && bare) scan_loose(line)                    # `echo … | sh`: the script is elsewhere on the line
    }
    {
        if (skip != "") {
            t = $0; gsub(/^[[:space:]]+|[[:space:]]+$/, "", t)
            if (t == skip) { skip = ""; inspect = 0; next }
            if (inspect) scan_loose($0)
            next
        }
        n = segments($0, seg)
        for (s = 1; s <= n; s++) analyze(seg[s], $0)
    }')

if [ "$verdict" = "BLOCK" ]; then
    echo "BLOCKED: dbt is never run from Bash. Delegate dbt work to the \`dbt\` subagent (it runs dbt through the dbt-enveloppe MCP server)." >&2
    echo "For a command outside its scope (deps, docs generate, seed, snapshot, ...), ask the user to run it in their own terminal, e.g. \`! uv run dbt deps\`." >&2
    exit 2
fi

exit 0
