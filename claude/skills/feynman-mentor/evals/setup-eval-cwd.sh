#!/usr/bin/env bash
# Prepare a temporary CWD for a given feynman-mentor eval id.
# Usage: ./setup-eval-cwd.sh <eval-id>
# Prints the absolute path of the created CWD on stdout.
#
# All evals run in an EMPTY CWD: the skill is pure conversation, fixtures are
# carried by the query itself. The empty dir still matters — it isolates the
# session from any project CLAUDE.md and makes the "no file written" checks
# trivial (any file appearing in the CWD after session B is a failure).
#
# PREREQUISITE for session B: the skill must be discoverable for the discovery
# evals to be meaningful. The skill is registered in install.sh; verify the
# runtime symlink is active before the run (re-run install.sh if missing):
#   ls -l ~/.claude/skills/feynman-mentor

set -euo pipefail

usage() {
    cat >&2 <<EOF
Usage: $0 <eval-id>

Eval ids (see feynman-mentor.eval.json):
  candide-never-fills-gaps      jargon-laden explanation -> flags gaps, never defines
  candide-refuses-meta-help     vague explanation + explicit plea for help -> refuses
  no-web-lookup                 asks to verify against online docs -> no web tools
  discovery-french-trigger      French trigger phrase -> skill auto-invokes
  no-collision-teach-territory  "apprends-moi..." -> skill does NOT invoke
  session-end-learning-record   session stop -> copiable record, zero file written
EOF
    exit 2
}

if [[ $# -ne 1 ]]; then
    usage
fi

EVAL_ID="$1"

case "$EVAL_ID" in
    candide-never-fills-gaps | candide-refuses-meta-help | no-web-lookup | \
    discovery-french-trigger | no-collision-teach-territory | session-end-learning-record)
        ;;
    *)
        echo "error: unknown eval id '$EVAL_ID'" >&2
        usage
        ;;
esac

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
CWD="/tmp/feynman-eval-${EVAL_ID}-${TIMESTAMP}"
mkdir -p "$CWD"

echo "$CWD"
