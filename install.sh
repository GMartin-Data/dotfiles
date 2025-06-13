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

echo "🎉 Done!"