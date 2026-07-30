#!/usr/bin/env bash
# Prepare a temporary CWD with the fixtures required by a given eval id.
# Usage: ./setup-eval-cwd.sh <eval-id>
# Prints the absolute path of the created CWD on stdout.
#
# The B session runs on the REAL user config: the symlinked payload already
# exposes the overhauled /immunize, and ~/.claude/CLAUDE.md is git-tracked, so
# any stray global write is visible and revertible. No CLAUDE_CONFIG_DIR
# isolation needed — unlike the claude-md corpus, these evals do not vary the
# payload. The interview script adds a guard turn: a plan containing a Global
# Do NOT write is refused, never applied.

set -euo pipefail

FIXTURES="$(cd "$(dirname "$0")/fixtures" && pwd)"

usage() {
    cat >&2 <<EOF
Usage: $0 <eval-id>

Eval ids (see immunize.eval.json):
  artifact-routing      inbox with a 2-occurrence lesson blaming hooks/check_partition.py
  global-gate           inbox with a 2-occurrence generic pattern (no global equivalent)
  add-mode              inbox with one old unique entry (tripwire if triage runs)
  insights-collision    inbox with an [INSIGHTS] card + one old unique lesson
  project-format        inbox with a 2-occurrence project-scoped dbt lesson
  triage-complet        composite: all populations at once (A->B->A gate run, ADR-0015)
EOF
    exit 2
}

[[ $# -eq 1 ]] || usage
EVAL_ID="$1"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
CWD="/tmp/immunize-eval-${EVAL_ID}-${TIMESTAMP}"

case "$EVAL_ID" in
    artifact-routing | global-gate | add-mode | insights-collision | project-format)
        mkdir -p "$CWD/tasks"
        cp "$FIXTURES/common/CLAUDE.md" "$CWD/CLAUDE.md"
        cp "$FIXTURES/$EVAL_ID/lessons-inbox.md" "$CWD/tasks/lessons-inbox.md"
        if [[ "$EVAL_ID" == "artifact-routing" ]]; then
            mkdir -p "$CWD/hooks"
            cp "$FIXTURES/artifact-routing/hooks/check_partition.py" "$CWD/hooks/"
        fi
        ;;

    triage-complet)
        mkdir -p "$CWD/tasks" "$CWD/hooks"
        cp "$FIXTURES/common/CLAUDE.md" "$CWD/CLAUDE.md"
        cp "$FIXTURES/triage-complet/lessons-inbox.md" "$CWD/tasks/lessons-inbox.md"
        cp "$FIXTURES/artifact-routing/hooks/check_partition.py" "$CWD/hooks/"
        # Fresh unique entry (<= 7 days): dated dynamically so replays keep it fresh.
        FRESH="$(date -d '2 days ago' +%F)"
        printf -- '- [%s] Le seed de `stations_ref` a été relancé en préprod avec le CSV de dev — 12 stations de test visibles dans le mart pendant une heure.\n' "$FRESH" >> "$CWD/tasks/lessons-inbox.md"
        ;;

    *)
        echo "error: unknown eval id '$EVAL_ID'" >&2
        usage
        ;;
esac

# The tri_destination criterion reads "versioned artifact": make it literally true.
git -C "$CWD" init -q
git -C "$CWD" add -A
git -C "$CWD" -c user.email=eval@local -c user.name=eval commit -qm "fixture: meteo-pipeline eval CWD"

echo "$CWD"
