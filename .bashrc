# If this is an interactive shell and zsh is available, switch to zsh
if [ -n "$PS1" ] && [ -x "$(command -v zsh)" ]; then
    exec zsh
fi
