# dotfiles

Configuration personnelle pour environnement de développement data engineering / AI engineering.
Optimisé pour **Crostini (ChromeOS, Debian 12 bookworm)** et **Ubuntu 22.04**.

---

## Contenu

| Fichier | Emplacement cible | Description |
|---|---|---|
| `zsh/.zshrc` | `~/.zshrc` | Shell Zsh + Oh My Zsh, plugins, aliases |
| `git/.gitconfig` | `~/.gitconfig` | Identité Git, GPG signing, aliases |
| `scripts/maintenance.sh` | `~/scripts/maintenance.sh` | Maintenance automatisée du conteneur |
| `vscode/settings.json` | `~/.config/Code/User/settings.json` | Configuration VS Code |

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