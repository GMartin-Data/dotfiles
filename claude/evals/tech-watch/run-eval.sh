#!/usr/bin/env bash
# Run one tech-watch eval in an isolated sandbox (claude-md batch A pattern).
# Usage: run-eval.sh <run-id> <prompt>
#   run-id  e.g. e2  -> sandbox /tmp/claude-eval-tech-watch-<run-id>
#   prompt  e.g. "/tech-watch AI agent evaluation"
# Sandbox layout: config/ (isolated CLAUDE_CONFIG_DIR: skill copy, global CLAUDE.md,
# credentials symlink, .claude.json copy, empty settings), cwd/ (report lands here),
# mcp.json (session-only server declaration), transcript.jsonl, stderr.log, exit_code.
# Env: MODEL (default opus), EXTRA_ARGS (e.g. "--max-turns 2" for trigger probes),
#      FIXTURE_DIR (its contents are copied into cwd/ before the run),
#      MCP_JSON (path to an mcp config to use instead of the default SSE one).
set -uo pipefail
ID="${1:?run id required}"
PROMPT="${2:?prompt required}"
RUN="/tmp/claude-eval-tech-watch-$ID"
MODEL="${MODEL:-opus}"
EXTRA_ARGS="${EXTRA_ARGS:-}"
FIXTURE_DIR="${FIXTURE_DIR:-}"
MCP_JSON="${MCP_JSON:-}"
SKILL_SRC="$HOME/dotfiles/claude/skills/tech-watch"
GLOBAL_MD="$HOME/dotfiles/claude/CLAUDE.md"

mkdir -p "$RUN/cwd" "$RUN/config/skills"
cp -r "$SKILL_SRC" "$RUN/config/skills/"
cp "$GLOBAL_MD" "$RUN/config/CLAUDE.md"
ln -sf "$HOME/.claude/.credentials.json" "$RUN/config/.credentials.json"
cp "$HOME/.claude.json" "$RUN/config/.claude.json"
echo '{}' > "$RUN/config/settings.json"
if [ -n "$MCP_JSON" ]; then
  cp "$MCP_JSON" "$RUN/mcp.json"
else
  cat > "$RUN/mcp.json" <<'EOF'
{"mcpServers":{"tech-watch":{"type":"sse","url":"https://tech-watch-mcp-ocbwcs6sjq-ew.a.run.app/sse"}}}
EOF
fi
printf '%s\n' "$PROMPT" > "$RUN/prompt.txt"
[ -n "$FIXTURE_DIR" ] && cp -r "$FIXTURE_DIR"/. "$RUN/cwd/"

cd "$RUN/cwd" || exit 97
date -Is > "$RUN/started_at"
# shellcheck disable=SC2086  # EXTRA_ARGS is meant to be word-split
CLAUDE_CONFIG_DIR="$RUN/config" claude -p "$PROMPT" --model "$MODEL" $EXTRA_ARGS \
  --mcp-config "$RUN/mcp.json" --strict-mcp-config \
  --allowedTools "WebSearch,WebFetch,mcp__tech-watch,Read,Write,Edit,Bash,Glob,Grep" \
  --output-format stream-json --verbose < /dev/null > "$RUN/transcript.jsonl" 2> "$RUN/stderr.log"
echo $? > "$RUN/exit_code"
date -Is > "$RUN/ended_at"
