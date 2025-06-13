# 🛠️ Personal Dotfiles

My development environment configuration for GitHub Codespaces and local development.

## What's Included

### Shell Configuration

- **Zsh with Oh My Zsh** - Modern shell with Git integration
- **Automatic setup** - Installs missing dependencies automatically

### Development Tools

- **uv** - Fast Python package manager
- **jq** - JSON processor for API work
- **GitHub CLI (gh)** - GitHub operations from command line
- **tree** - Directory structure visualization
- **bat** - Better `cat` with syntax highlighting
- **htop** - Interactive system monitor

## Quick Start

### For GitHub Codespaces

1. Go to [GitHub Settings → Codespaces](https://github.com/settings/codespaces)
2. Enable "Automatically install dotfiles"
3. Select this repository: `GMartin-Data/dotfiles`
4. Set install command: `./install.sh`

New Codespaces will automatically include all tools!

### For Local Setup

```bash
git clone https://github.com/GMartin-Data/dotfiles.git
cd dotfiles
./install.sh
```

## Files

- `.bashrc` - Switches to Zsh automatically
- `.zshrc` - Zsh configuration with Oh My Zsh
- `install.sh` - Installs all development tools
- `README.md` - This file

## Usage

All tools install automatically. Key commands:

- `tree` - Show directory structure
- `bat filename` - View file with syntax highlighting
- `jq .` - Format JSON from clipboard
- `gh repo list` - List your GitHub repositories
- `htop` - Monitor system resources

## Adding More Tools

Edit `install.sh` and follow the pattern:

```bash
if ! command -v toolname >/dev/null 2>&1; then
    echo "📦 Installing toolname..."
    # installation commands here
    echo "✅ toolname installed!"
fi
```

## License

Free to use and modify for personal use.
