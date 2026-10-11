#!/usr/bin/env bash
# K12 probe: is a subagent's inline `mcpServers` connected when a skill forks into it?
# Usage: probe-k12.sh <variant>   variant = fork | nofork | down
#   fork    skill forks into the agent whose inline server is the real Cloud Run endpoint
#   nofork  control: same probe body run inline in the main session (no agent, no server)
#   down    skill forks into an agent whose inline server URL is unreachable
# Sandbox /tmp/claude-eval-tech-watch-k12-<variant>: isolated CLAUDE_CONFIG_DIR with
# fixtures/k12/{agents,skills}, global CLAUDE.md, credentials symlink, .claude.json copy,
# empty settings. No --mcp-config: the only tech-watch declaration is the agent's inline one.
# Env: MODEL (default opus), EXTRA_ARGS.
set -uo pipefail
VARIANT="${1:?variant required: fork | nofork | down}"
AGENT="tech-watch.md"
case "$VARIANT" in
  fork)   SKILL="tech-watch-probe" ;;
  nofork) SKILL="tech-watch-probe-nofork" ;;
  down)   SKILL="tech-watch-probe"; AGENT="tech-watch-down.md" ;;
  *) echo "unknown variant: $VARIANT" >&2; exit 2 ;;
esac
RUN="/tmp/claude-eval-tech-watch-k12-$VARIANT"
MODEL="${MODEL:-opus}"
EXTRA_ARGS="${EXTRA_ARGS:-}"
FIX="$HOME/dotfiles/claude/evals/tech-watch/fixtures/k12"
GLOBAL_MD="$HOME/dotfiles/claude/CLAUDE.md"

rm -rf "$RUN"
mkdir -p "$RUN/cwd" "$RUN/config/agents" "$RUN/config/skills"
cp "$FIX/agents/$AGENT" "$RUN/config/agents/tech-watch.md"
cp -r "$FIX/skills/$SKILL" "$RUN/config/skills/"
cp "$GLOBAL_MD" "$RUN/config/CLAUDE.md"
ln -sf "$HOME/.claude/.credentials.json" "$RUN/config/.credentials.json"
cp "$HOME/.claude.json" "$RUN/config/.claude.json"
echo '{}' > "$RUN/config/settings.json"
PROMPT="/$SKILL"
printf '%s\n' "$PROMPT" > "$RUN/prompt.txt"

cd "$RUN/cwd" || exit 97
date -Is > "$RUN/started_at"
# shellcheck disable=SC2086  # EXTRA_ARGS is meant to be word-split
CLAUDE_CONFIG_DIR="$RUN/config" claude -p "$PROMPT" --model "$MODEL" $EXTRA_ARGS \
  --allowedTools "Skill,Agent,Task,mcp__tech-watch,Read,WebSearch" \
  --output-format stream-json --verbose < /dev/null > "$RUN/transcript.jsonl" 2> "$RUN/stderr.log"
echo $? > "$RUN/exit_code"
date -Is > "$RUN/ended_at"
