# dotfiles

Configuration personnelle pour environnement de développement data engineering / AI engineering.
Optimisé pour **Crostini (ChromeOS, Debian 12 bookworm)** et **Ubuntu 22.04**.

---

## Contenu

| Fichier / Dossier | Emplacement cible | Description |
|---|---|---|
| `zsh/.zshrc` | `~/.zshrc` | Shell Zsh + Oh My Zsh, plugins, aliases |
| `git/.gitconfig` | `~/.gitconfig` | Identité Git, GPG signing, aliases |
| `scripts/maintenance.sh` | `~/scripts/maintenance.sh` | Maintenance automatisée du conteneur |
| `vscode/settings.json` | `~/.config/Code/User/settings.json` | Configuration VS Code |
| `vscode/extensions.txt` | — | Liste des extensions VS Code (installées par `bootstrap.sh`) |
| `claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | Conventions globales Claude Code |
| `claude/settings.json` | `~/.claude/settings.json` | Configuration Claude Code |
| `claude/commands/*.md` | `~/.claude/commands/` | Slash commands personnalisées |
| `claude/hooks/*` | `~/.claude/hooks/` | Hooks PreToolUse (protection + lint) |
| `claude/skills/` | `~/.claude/skills/` | Skills personnalisées (dossiers symlinkés) |
| `claude/agents/` | `~/.claude/agents/` | Subagents (fichiers individuels + scripts partagés) |
| `claude/agent-memory/` | `~/.claude/agent-memory/` | Mémoire persistante des subagents |
| `TODO.md` | — | Évolutions différées avec contexte et critères |

---

## Installation sur une machine vierge

```bash
git clone git@github.com:GMartin-Data/dotfiles.git ~/dotfiles
cd ~/dotfiles

# 1. Installer les outils
./bootstrap.sh

# 2. Créer les symlinks
./install.sh

# 3. Recharger le shell
source ~/.zshrc
```

## Installation sur une machine déjà configurée

```bash
git clone git@github.com:GMartin-Data/dotfiles.git ~/dotfiles
cd ~/dotfiles
./install.sh
source ~/.zshrc
```

---

## Stack

**Shell**
- Zsh + Oh My Zsh
- Plugins : git, zsh-autosuggestions, zsh-syntax-highlighting, z, sudo, fzf, history, docker, vi-mode, alias-tips

**Outils système**
- `jq` / `yq` — traitement JSON/YAML
- `fzf` — recherche floue interactive
- `ripgrep` — recherche dans les fichiers (alternative à grep)
- `fd` — recherche de fichiers (alternative à find)
- `btop` — moniteur système interactif (processus, CPU, mémoire, réseau, disque)

**Développement**
- Node.js via nvm
- Python via uv
- Claude Code
- Google Cloud CLI
- GitHub CLI (`gh`)
- Docker Engine

**Git**
- GPG signing actif (clé RSA 4096)
- SSH GitHub (`id_github_chromebook`)

---

## Claude Code

La configuration Claude Code est versionnée dans `claude/` et symlinkée vers `~/.claude/` par `install.sh`.

**Fichiers racine :**
- `CLAUDE.md` — conventions globales (identité, stack, style Python, règles Git, workflow AI)
- `settings.json` — configuration Claude Code (permissions, hooks, plugins, effort level)

**Slash commands (`commands/`) :**
- `catchup.md` — reprise de contexte après interruption
- `claude-md.md` — interview structuré pour créer un CLAUDE.md projet
- `immunize.md` — cycle immunitaire : lessons-inbox → CLAUDE.md projet → CLAUDE.md global
- `learning-tracker.md` — invocation du subagent de suivi d'apprentissage
- `prd.md` — interview structuré pour créer un PRD
- `progress.md` — checkpoint d'avancement avant `/clear`
- `tech-watch.md` — orchestration de la veille technologique

**Hooks PreToolUse (`hooks/`) :**
- `block-force-push.sh` — bloque `git push --force`
- `block-rm-rf.sh` — bloque `rm -rf`
- `protect_env.py` — protège les fichiers `.env`
- `ruff-check.sh` — lint automatique via Ruff

**Skills (`skills/`) :**
- `coach-pedagogique/` — coaching de développement structuré avec scaffolding dégressif
- `code-mentor/` — mentor Socratique avec génération de flashcards Anki
- `dp-coach/` — coach de pratique délibérée (Python, SQL)

**Subagents (`agents/`) :**
- `tech-watch-scorer.md` — scoring et classement de la veille technologique
- `learning-tracker.md` — suivi de progression d'apprentissage
- `scripts/` — scripts utilitaires partagés entre subagents

**Mémoire subagents (`agent-memory/`) :**
- `learning-tracker/MEMORY.md` — état persistant du suivi d'apprentissage

**Plugin à réinstaller manuellement :**
- `pyright-lsp@claude-plugins-official` — LSP Python pour Claude Code

---

## VS Code

- `vscode/settings.json` — configuration symlinkée vers `~/.config/Code/User/settings.json`
- `vscode/extensions.txt` — liste des extensions, installées automatiquement par `bootstrap.sh`

Pour mettre à jour la liste après ajout/suppression d'extensions :
```bash
code --list-extensions > ~/dotfiles/vscode/extensions.txt
```

---

## Configuration post-bootstrap

Après `bootstrap.sh`, ces outils nécessitent une authentification manuelle :

```bash
# GitHub CLI
gh auth login

# Google Cloud CLI
gcloud auth login
gcloud auth application-default login
```

---

## Outils à configurer manuellement

Ces outils ne sont pas couverts par `bootstrap.sh` — leur installation implique des dépôts tiers ou des étapes interactives :

| Outil | Documentation |
|---|---|
| Docker Engine | https://docs.docker.com/engine/install/debian/ |
| Google Cloud CLI | https://cloud.google.com/sdk/docs/install |
| VS Code | https://code.visualstudio.com/docs/setup/linux |

---

## Sauvegardes

Les éléments suivants ne sont **pas** dans ce dépôt et doivent être sauvegardés séparément :

| Élément | Méthode |
|---|---|
| Clé GPG privée | `gpg --export-secret-keys --armor KEY_ID > gpg-backup.asc` → stocker hors du conteneur |
| Clé SSH | Copier `~/.ssh/id_github_chromebook` sur support externe chiffré |

> ⚠️ Ne jamais versionner de clés SSH, GPG, tokens ou mots de passe — même dans un dépôt privé.

---

## Notes spécifiques à Crostini (ChromeOS)

- Ne jamais utiliser `sudo reboot` dans le conteneur (casse la VM)
- GPU désactivé (swrast par défaut, pas de virgl)
- Si la VM refuse de démarrer (`vm_start failed`), cliquer sur "Manage" dans l'interface Terminal
- Partager "My Files" avec Linux pour accéder à `/mnt/chromeos/MyFiles/`

---

## Maintenance

```bash
maintain        # alias → ~/scripts/maintenance.sh
```

Log consultable dans `~/.local/logs/maintenance.log`.

> ⚠️ Le nettoyage des volumes Docker est une tâche **manuelle** :
> `docker volume ls` / `docker volume prune` / `docker volume rm <nom>`