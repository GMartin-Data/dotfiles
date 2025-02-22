# Use Zsh as the default shell
export SHELL=/bin/zsh

# Initialize oh-my-zsh if installed; if not, install it
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "Installing oh-my-zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi

# Source oh-my-zsh
if [ -d "$HOME/.oh-my-zsh" ]; then
    source $HOME/.oh-my-zsh/oh-my-zsh.sh
fi

# Customize your prompt and plugins
ZSH_THEME="robbyrussell"
plugins=(git)