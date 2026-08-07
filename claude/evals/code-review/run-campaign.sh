#!/usr/bin/env bash
# Run the code-review de-scaffolding matrix: 2 variants × 2 tiers × 2 reps.
# Sequential; idempotent — a run directory holding a non-empty transcript.jsonl
# is skipped, so an interrupted campaign can be relaunched with the same
# workspace. Mirrors claude/evals/claude-md/run-batch.sh mechanics.
#
# Usage: run-campaign.sh <workspace-root> [run-id filter, e.g. A-fable-r1]
# Env:   RUN_TIMEOUT (seconds per run, default 900)
set -euo pipefail

CORPUS_DIR="$(cd "$(dirname "$0")" && pwd)"
WS="${1:?workspace root required}"
FILTER="${2:-}"
RUN_TIMEOUT="${RUN_TIMEOUT:-900}"
mkdir -p "$WS"

for VARIANT in A B; do
  for TIER in fable opus; do
    for REP in r1 r2; do
      ID="$VARIANT-$TIER-$REP"
      if [ -n "$FILTER" ] && [ "$ID" != "$FILTER" ]; then continue; fi
      RUN="$WS/$ID"
      if [ -s "$RUN/transcript.jsonl" ]; then
        echo "skip $ID (done)"
        continue
      fi
      rm -rf "$RUN"
      "$CORPUS_DIR/setup-eval-cwd.sh" "$VARIANT" "$RUN"
      echo ">>> $ID"
      set +e
      ( cd "$RUN/cwd" && CLAUDE_CONFIG_DIR="$RUN/config" timeout "$RUN_TIMEOUT" \
          claude -p "/code-review" --model "$TIER" \
          --output-format stream-json --verbose \
          --dangerously-skip-permissions \
          > ../transcript.jsonl 2> ../stderr.log )
      STATUS=$?
      set -e
      [ "$STATUS" -ne 0 ] && echo "$STATUS" > "$RUN/failed"
      # No-edit invariant: tracked diff and untracked set must be unchanged.
      git -C "$RUN/cwd" diff > "$RUN/post-run.diff"
      git -C "$RUN/cwd" status --porcelain > "$RUN/post-run.status"
      if cmp -s "$RUN/pre-run.diff" "$RUN/post-run.diff" \
         && cmp -s "$RUN/pre-run.status" "$RUN/post-run.status"; then
        echo "intact" > "$RUN/cwd-check"
      else
        echo "MODIFIED" > "$RUN/cwd-check"
      fi
      echo "<<< $ID (exit $STATUS, cwd $(cat "$RUN/cwd-check"))"
    done
  done
done
echo "campaign pass complete"
