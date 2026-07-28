#!/usr/bin/env bash
# Run the batch A benchmark: every (rule × tier) pair from evals.json, each in
# {with, without} variant. Sequential; idempotent — a run directory that
# already holds a non-empty transcript.jsonl is skipped, so an interrupted
# batch can simply be relaunched with the same workspace.
#
# Usage: run-batch.sh <workspace-root> [RULE ...]   (optional rule filter)
# Env:   RUN_TIMEOUT (seconds per run, default 300)
set -euo pipefail

CORPUS_DIR="$(cd "$(dirname "$0")" && pwd)"
WS="${1:?workspace root required}"
shift || true
RUN_TIMEOUT="${RUN_TIMEOUT:-300}"
mkdir -p "$WS"

# Precompute the run matrix and one prompt file per rule.
python3 - "$CORPUS_DIR/evals.json" "$WS" <<'PY'
import json
import pathlib
import sys

ws = pathlib.Path(sys.argv[2])
evals = json.load(open(sys.argv[1]))["evals"]
with open(ws / "matrix.txt", "w") as m:
    for e in evals:
        (ws / f"prompt-{e['rule']}.txt").write_text(e["prompt"])
        for tier in e["tiers"]:
            print(e["rule"], tier, file=m)
PY

while read -r RULE TIER; do
  if [ "$#" -gt 0 ]; then
    printf '%s\n' "$@" | grep -qx "$RULE" || continue
  fi
  for VARIANT in with without; do
    RUN="$WS/$RULE-$TIER-$VARIANT"
    if [ -s "$RUN/transcript.jsonl" ]; then
      echo "skip $RULE $TIER $VARIANT (done)"
      continue
    fi
    rm -rf "$RUN"
    "$CORPUS_DIR/setup-eval-cwd.sh" "$RULE" "$VARIANT" "$RUN"
    echo ">>> $RULE $TIER $VARIANT"
    set +e
    ( cd "$RUN/cwd" && CLAUDE_CONFIG_DIR="$RUN/config" timeout "$RUN_TIMEOUT" \
        claude -p "$(cat "$WS/prompt-$RULE.txt")" --model "$TIER" \
        --output-format stream-json --verbose \
        --dangerously-skip-permissions \
        > ../transcript.jsonl 2> ../stderr.log )
    STATUS=$?
    set -e
    [ "$STATUS" -ne 0 ] && echo "$STATUS" > "$RUN/failed"
    ( cd "$RUN/cwd" && find . -path ./.git -prune -o -type f -print | sort ) > "$RUN/files-after.txt"
    echo "<<< $RULE $TIER $VARIANT (exit $STATUS)"
  done
done < "$WS/matrix.txt"

FAILED=$(find "$WS" -maxdepth 2 -name failed | wc -l)
echo "batch complete — $FAILED failed run(s)"
