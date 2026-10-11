#!/usr/bin/env bash
# Summarise a `claude -p --output-format stream-json --verbose` transcript:
# one line per tool call (name + compacted input), then the final result stats.
# Usage: extract-run.sh <transcript.jsonl>
set -euo pipefail
T="${1:?transcript path required}"

echo "## Tool calls (in order)"
echo
jq -r '
  select(.type == "assistant")
  | .message.content[]?
  | select(.type == "tool_use")
  | "- `\(.name)` " + (
      if .name == "Skill" then (.input.skill // "" | tostring) + " " + (.input.args // "" | tostring)
      elif .name == "WebSearch" then (.input.query // "" | tostring)
      elif .name == "WebFetch" then (.input.url // "" | tostring)
      elif .name == "Write" then (.input.file_path // "" | tostring)
      elif .name == "Read" then (.input.file_path // "" | tostring)
      else (.input | tostring | .[0:160])
      end)
' "$T"

echo
echo "## Tool call counts"
echo
jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' "$T" \
  | sort | uniq -c | sort -rn | sed 's/^ *\([0-9]*\) \(.*\)$/- \2: \1/'

echo
echo "## Result"
echo
jq -r '
  select(.type == "result")
  | "- subtype: \(.subtype // "n/a")",
    "- is_error: \(.is_error // "n/a")",
    "- num_turns: \(.num_turns // "n/a")",
    "- duration_ms: \(.duration_ms // "n/a") (api: \(.duration_api_ms // "n/a"))",
    "- total_cost_usd: \(.total_cost_usd // "n/a")",
    "- usage: \(.usage // {} | tostring | .[0:300])",
    "- model usage keys: \((.modelUsage // {}) | keys | tostring)"
' "$T"

echo
echo "## Final assistant text (first 60 lines)"
echo
jq -r 'select(.type == "result") | .result // ""' "$T" | head -60
