# ============================================================
# OH MY ZSH - Configuration de base
# ============================================================
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

# Plugins: git, autosuggestions, syntax-highlighting sont custom (installés dans $ZSH_CUSTOM)
# Les autres (z, sudo, fzf, history, docker, vi-mode) sont built-in Oh My Zsh
plugins=(git zsh-autosuggestions zsh-syntax-highlighting z sudo fzf history docker vi-mode alias-tips)

source $ZSH/oh-my-zsh.sh

# ============================================================
# SSH AGENT - Retient la passphrase en mémoire pour la session
# ============================================================
eval "$(ssh-agent -s)" > /dev/null 2>&1
ssh-add ~/.ssh/id_github_chromebook > /dev/null 2>&1

# ============================================================
# NVM - Node Version Manager
# ============================================================
export NVM_DIR="$HOME/.config/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# ============================================================
# UV - Gestionnaire de paquets Python (Astral)
# ============================================================
. "$HOME/.local/bin/env"

# ============================================================
# GOOGLE CLOUD SDK - CLI et autocomplétion
# ============================================================
if [ -f "$HOME/google-cloud-sdk/path.zsh.inc" ]; then . "$HOME/google-cloud-sdk/path.zsh.inc"; fi
if [ -f "$HOME/google-cloud-sdk/completion.zsh.inc" ]; then . "$HOME/google-cloud-sdk/completion.zsh.inc"; fi

# ============================================================
# ALIASES PERSONNELS
# ============================================================
alias maintain='bash ~/scripts/maintenance.sh'

# ============================================================
# GPG - Permet la saisie de passphrase dans le terminal
# ============================================================
export GPG_TTY=$(tty)
