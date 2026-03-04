#!/bin/bash
# =============================================================================
# bootstrap.sh — Installation des outils sur une machine vierge (Crostini)
# =============================================================================

set -euo pipefail

echo "=== Bootstrap : installation des outils ==="
echo ""

# -----------------------------------------------------------------------------
# Paquets système
# -----------------------------------------------------------------------------
echo ">>> Paquets système..."
sudo apt-get update -q
# build-essential : compilateur C + make + headers — requis pour compiler les extensions
#                   natives de certains paquets Python (numpy, cryptography, psycopg2...)
# gnupg             : requis pour le commit signing Git et la gestion des clés GPG
sudo apt-get install -y -q \
    git \
    curl \
    wget \
    zsh \
    jq \
    fzf \
    ripgrep \
    fd-find \
    build-essential \
    gnupg

# yq (pas dans les dépôts Debian, installation via binaire officiel)
if ! command -v yq &>/dev/null; then
    echo ">>> Installation de yq..."
    sudo wget -qO /usr/local/bin/yq \
        https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
    sudo chmod +x /usr/local/bin/yq
fi

# fd (le binaire s'appelle fdfind sur Debian pour éviter un conflit de nom)
if command -v fdfind &>/dev/null && ! command -v fd &>/dev/null; then
    echo ">>> Création du symlink fd → fdfind..."
    mkdir -p "$HOME/.local/bin"
    ln -sf "$(which fdfind)" "$HOME/.local/bin/fd"
fi

# -----------------------------------------------------------------------------
# Zsh + Oh My Zsh
# -----------------------------------------------------------------------------
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo ">>> Installation de Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# Plugins Oh My Zsh
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

if [ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]; then
    echo ">>> Installation de zsh-autosuggestions..."
    git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions \
        "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
fi

if [ ! -d "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" ]; then
    echo ">>> Installation de zsh-syntax-highlighting..."
    git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting \
        "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
fi

if [ ! -d "$ZSH_CUSTOM/plugins/alias-tips" ]; then
    echo ">>> Installation de alias-tips..."
    git clone --depth=1 https://github.com/djui/alias-tips \
        "$ZSH_CUSTOM/plugins/alias-tips"
fi

# -----------------------------------------------------------------------------
# nvm + Node.js
# -----------------------------------------------------------------------------
if [ ! -d "$HOME/.nvm" ]; then
    echo ">>> Installation de nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    # shellcheck source=/dev/null
    \. "$NVM_DIR/nvm.sh"
    echo ">>> Installation de Node.js LTS..."
    nvm install 24
fi

# -----------------------------------------------------------------------------
# uv
# -----------------------------------------------------------------------------
if ! command -v uv &>/dev/null; then
    echo ">>> Installation de uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# -----------------------------------------------------------------------------
# Claude Code
# -----------------------------------------------------------------------------
if ! command -v claude &>/dev/null; then
    echo ">>> Installation de Claude Code..."
    npm install -g @anthropic-ai/claude-code
fi

# -----------------------------------------------------------------------------
# Outils à installer manuellement (trop complexes à automatiser de façon fiable)
# -----------------------------------------------------------------------------
echo ""
echo "⚠️  Les outils suivants nécessitent une installation manuelle :"
echo ""
echo "   Docker Engine"
echo "   → https://docs.docker.com/engine/install/debian/"
echo ""
echo "   Google Cloud CLI"
echo "   → https://cloud.google.com/sdk/docs/install"
echo ""
echo "   VS Code"
echo "   → https://code.visualstudio.com/docs/setup/linux"
echo ""

# -----------------------------------------------------------------------------
# Fin
# -----------------------------------------------------------------------------
echo "=== Bootstrap terminé ==="
echo "Lance maintenant : ./install.sh"