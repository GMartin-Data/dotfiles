#!/bin/bash
# =============================================================================
# install.sh — Création des symlinks vers les dotfiles
# =============================================================================

set -euo pipefail

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

link() {
    local src="$1"
    local dst="$2"
    mkdir -p "$(dirname "$dst")"
    ln -sfn "$src" "$dst"
    echo "Linked: $dst → $src"
}

echo "=== Installation des dotfiles depuis $DOTFILES_DIR ==="

# --- Zsh ---
link "$DOTFILES_DIR/zsh/.zshrc"             "$HOME/.zshrc"

# --- Git ---
link "$DOTFILES_DIR/git/.gitconfig"         "$HOME/.gitconfig"

# --- Scripts ---
link "$DOTFILES_DIR/scripts/maintenance.sh" "$HOME/scripts/maintenance.sh"

# --- VS Code ---
link "$DOTFILES_DIR/vscode/settings.json"   "$HOME/.config/Code/User/settings.json"

# --- Claude Code ---
link "$DOTFILES_DIR/claude/CLAUDE.md"           "$HOME/.claude/CLAUDE.md"
link "$DOTFILES_DIR/claude/settings.json"        "$HOME/.claude/settings.json"

# Commands (fichiers individuels — le dossier peut contenir des fichiers gérés par Claude Code)
link "$DOTFILES_DIR/claude/commands/claude-md.md"  "$HOME/.claude/commands/claude-md.md"
link "$DOTFILES_DIR/claude/commands/immunize.md"    "$HOME/.claude/commands/immunize.md"
link "$DOTFILES_DIR/claude/commands/prd.md"          "$HOME/.claude/commands/prd.md"
link "$DOTFILES_DIR/claude/commands/catchup.md"    "$HOME/.claude/commands/catchup.md"
link "$DOTFILES_DIR/claude/commands/progress.md"    "$HOME/.claude/commands/progress.md"
link "$DOTFILES_DIR/claude/commands/tech-watch.md"  "$HOME/.claude/commands/tech-watch.md"
link "$DOTFILES_DIR/claude/commands/learning-tracker.md" "$HOME/.claude/commands/learning-tracker.md"

# Hooks (fichiers individuels — même raison)
link "$DOTFILES_DIR/claude/hooks/block-force-push.sh" "$HOME/.claude/hooks/block-force-push.sh"
link "$DOTFILES_DIR/claude/hooks/block-rm-rf.sh"      "$HOME/.claude/hooks/block-rm-rf.sh"
link "$DOTFILES_DIR/claude/hooks/protect_env.py"      "$HOME/.claude/hooks/protect_env.py"
link "$DOTFILES_DIR/claude/hooks/ruff-check.sh"       "$HOME/.claude/hooks/ruff-check.sh"

# Skills (dossiers entiers — chaque skill est un dossier isolé qu'on contrôle)
link "$DOTFILES_DIR/claude/skills/code-mentor"  "$HOME/.claude/skills/code-mentor"
link "$DOTFILES_DIR/claude/skills/dp-coach"     "$HOME/.claude/skills/dp-coach"

# Agents (fichiers individuels)
link "$DOTFILES_DIR/claude/agents/tech-watch-scorer.md" "$HOME/.claude/agents/tech-watch-scorer.md"
link "$DOTFILES_DIR/claude/agents/learning-tracker.md" "$HOME/.claude/agents/learning-tracker.md"

# Agent memory (dossiers entiers)
link "$DOTFILES_DIR/claude/agent-memory/learning-tracker" "$HOME/.claude/agent-memory/learning-tracker"

echo ""
echo "=== Symlinks créés. ==="
echo "Lance 'source ~/.zshrc' pour recharger le shell."