#!/usr/bin/env bash
# Run one tech-watch eval in an isolated sandbox (claude-md batch A pattern), on the
# D3 (d) montage: the skill forks into the `tech-watch` subagent, whose frontmatter
# declares the MCP server inline. No --mcp-config / --strict-mcp-config: strict mode
# would also block servers declared in subagent frontmatter (documented).
# Usage: run-eval.sh <run-id> <prompt>
#   run-id  e.g. e2  -> sandbox /tmp/claude-eval-tech-watch-<run-id>, letters, digits,
#           dot, dash, underscore only; an existing sandbox with that id is wiped first
#           (a stale cwd/tech-watch/ would void the "agent creates the directory" check)
#   prompt  e.g. "/tech-watch AI agent evaluation"
# Sandbox layout: config/ (isolated CLAUDE_CONFIG_DIR: skill copy, agents/tech-watch.md,
# global CLAUDE.md, credentials symlink, .claude.json copy, empty settings), cwd/ (session
# working directory), cwd/tech-watch/ (report lands here: the agent's fixed output
# directory /home/martin/tech-watch is rewritten to it in the agent copy, and it is NOT
# pre-created, so each run also checks that the agent creates it), transcript.jsonl,
# stderr.log, exit_code.
# Env: MODEL (default opus, main session only - the fork runs on the agent's `model`),
#      EXTRA_ARGS (e.g. "--max-turns 2" for trigger probes),
#      FIXTURE_DIR (its contents are copied into cwd/ before the run),
#      AGENT_MD (agent file to use instead of claude/agents/tech-watch.md, e.g. the E3
#                fixture: local stdio server with an invalid GitHub token; or
#                fixtures/k8/agent-stub.md with "--max-turns 1" for trigger probes
#                E5/E7 - --max-turns bounds the main session only, not the fork).
set -uo pipefail
ID="${1:?run id required}"
PROMPT="${2:?prompt required}"
case "$ID" in
  *[!A-Za-z0-9._-]*|.|..|"") echo "run id must match [A-Za-z0-9._-]+ : '$ID'" >&2; exit 2 ;;
esac
RUN="/tmp/claude-eval-tech-watch-$ID"
MODEL="${MODEL:-opus}"
EXTRA_ARGS="${EXTRA_ARGS:-}"
FIXTURE_DIR="${FIXTURE_DIR:-}"
AGENT_MD="${AGENT_MD:-$HOME/dotfiles/claude/agents/tech-watch.md}"
SKILL_SRC="$HOME/dotfiles/claude/skills/tech-watch"
GLOBAL_MD="$HOME/dotfiles/claude/CLAUDE.md"

rm -rf "$RUN"
mkdir -p "$RUN/cwd" "$RUN/config/skills" "$RUN/config/agents"
cp -r "$SKILL_SRC" "$RUN/config/skills/"
sed "s#/home/martin/tech-watch/#$RUN/cwd/tech-watch/#g" "$AGENT_MD" > "$RUN/config/agents/tech-watch.md"
cp "$GLOBAL_MD" "$RUN/config/CLAUDE.md"
ln -sf "$HOME/.claude/.credentials.json" "$RUN/config/.credentials.json"
cp "$HOME/.claude.json" "$RUN/config/.claude.json"
echo '{}' > "$RUN/config/settings.json"
printf '%s\n' "$PROMPT" > "$RUN/prompt.txt"
[ -n "$FIXTURE_DIR" ] && cp -r "$FIXTURE_DIR"/. "$RUN/cwd/"

cd "$RUN/cwd" || exit 97
date -Is > "$RUN/started_at"
# shellcheck disable=SC2086  # EXTRA_ARGS is meant to be word-split
CLAUDE_CONFIG_DIR="$RUN/config" claude -p "$PROMPT" --model "$MODEL" $EXTRA_ARGS \
  --allowedTools "Skill,Agent,WebSearch,WebFetch,mcp__tech-watch,Read,Write,Edit,Bash,Glob,Grep" \
  --output-format stream-json --verbose < /dev/null > "$RUN/transcript.jsonl" 2> "$RUN/stderr.log"
echo $? > "$RUN/exit_code"
date -Is > "$RUN/ended_at"
