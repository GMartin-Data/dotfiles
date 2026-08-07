#!/usr/bin/env bash
# Assemble one eval run for the code-review de-scaffolding campaign (flag F3,
# tasks/code-review-fable-eval-2026-08.md).
#
# Usage: setup-eval-cwd.sh <A|B> <target-dir>
#
# Produces:
#   <target-dir>/cwd/     git repo fixture — base committed, worktree overlay
#                         left uncommitted (the diff under review)
#   <target-dir>/config/  scratch CLAUDE_CONFIG_DIR — real global payload +
#                         the skill variant under test as the only code-review
#                         skill; credentials symlinked, no hooks, no other skills
set -euo pipefail

CORPUS_DIR="$(cd "$(dirname "$0")" && pwd)"
PAYLOAD="$CORPUS_DIR/../../CLAUDE.md"
VARIANT="${1:?variant required (A|B)}"
TARGET="${2:?target dir required}"
case "$VARIANT" in A|B|B2) ;; *) echo "variant must be A|B" >&2; exit 1 ;; esac
[ -f "$CORPUS_DIR/variants/skill-$VARIANT.md" ] || { echo "missing variant file" >&2; exit 1; }

mkdir -p "$TARGET/cwd" "$TARGET/config/skills/code-review"

# 1. Scratch config: real payload as user CLAUDE.md, variant as the only skill.
cp "$PAYLOAD" "$TARGET/config/CLAUDE.md"
cp "$CORPUS_DIR/variants/skill-$VARIANT.md" "$TARGET/config/skills/code-review/SKILL.md"
ln -sf "$HOME/.claude/.credentials.json" "$TARGET/config/.credentials.json"
[ -f "$HOME/.claude.json" ] && cp "$HOME/.claude.json" "$TARGET/config/.claude.json"
echo '{"effortLevel":"xhigh"}' > "$TARGET/config/settings.json"

# 2. Fixture: committed base, then uncommitted worktree overlay.
for f in "$CORPUS_DIR"/fixtures/base/*.txt; do
  cp "$f" "$TARGET/cwd/$(basename "$f" .txt)"
done
(
  cd "$TARGET/cwd"
  git init -q -b main
  git -c user.name=eval -c user.email=eval@local add -A
  git -c user.name=eval -c user.email=eval@local commit -qm "base: usage-report module"
)
for f in "$CORPUS_DIR"/fixtures/worktree/*.txt; do
  cp "$f" "$TARGET/cwd/$(basename "$f" .txt)"
done

# 3. Reference state for the no-edit invariant check after the run.
git -C "$TARGET/cwd" diff > "$TARGET/pre-run.diff"
git -C "$TARGET/cwd" status --porcelain > "$TARGET/pre-run.status"
