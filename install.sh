#!/bin/bash

echo "🚀 Installing development tools..."

# Install uv (Python package manager)
if ! command -v uv >/dev/null 2>&1; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv installed!"
else
    echo "✅ uv already installed"
fi

# Install jq (JSON processor)
if ! command -v jq >/dev/null 2>&1; then
    echo "📦 Installing jq..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y jq
    elif command -v brew >/dev/null 2>&1; then
        brew install jq
    else
        echo "❌ Could not install jq - no package manager found"
    fi
    echo "✅ jq installed!"
else
    echo "✅ jq already installed"
fi

# Install GitHub CLI
if ! command -v gh >/dev/null 2>&1; then
    echo "📦 Installing GitHub CLI..."
    if command -v apt-get >/dev/null 2>&1; then
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt-get update && sudo apt-get install -y gh
    elif command -v brew >/dev/null 2>&1; then
        brew install gh
    fi
    echo "✅ GitHub CLI installed!"
else
    echo "✅ GitHub CLI already installed"
fi

# Install tree (directory structure visualizer)
if ! command -v tree >/dev/null 2>&1; then
    echo "📦 Installing tree..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get install -y tree
    elif command -v brew >/dev/null 2>&1; then
        brew install tree
    fi
    echo "✅ tree installed!"
else
    echo "✅ tree already installed"
fi

# Install bat (better cat with syntax highlighting)
if ! command -v bat >/dev/null 2>&1; then
    echo "📦 Installing bat..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get install -y bat
    elif command -v brew >/dev/null 2>&1; then
        brew install bat
    fi
    echo "✅ bat installed!"
else
    echo "✅ bat already installed"
fi

# Install htop (interactive process viewer)
if ! command -v htop >/dev/null 2>&1; then
    echo "📦 Installing htop..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get install -y htop
    elif command -v brew >/dev/null 2>&1; then
        brew install htop
    fi
    echo "✅ htop installed!"
else
    echo "✅ htop already installed"
fi

echo "🎉 Done!"