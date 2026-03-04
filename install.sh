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
    ln -sf "$src" "$dst"
    echo "Linked: $dst → $src"
}

echo "=== Installation des dotfiles depuis $DOTFILES_DIR ==="

link "$DOTFILES_DIR/zsh/.zshrc"             "$HOME/.zshrc"
link "$DOTFILES_DIR/git/.gitconfig"         "$HOME/.gitconfig"
link "$DOTFILES_DIR/scripts/maintenance.sh" "$HOME/scripts/maintenance.sh"
link "$DOTFILES_DIR/vscode/settings.json"   "$HOME/.config/Code/User/settings.json"

echo ""
echo "=== Symlinks créés. ==="
echo "Lance 'source ~/.zshrc' pour recharger le shell."