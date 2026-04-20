# Claude Code — Architecture

Configuration Claude Code versionnée dans ce dotfiles. La structure suit le layout natif `~/.claude/` et sépare ce qui est **chargé automatiquement** de ce qui est **invoqué à la demande**.

---

## Vue d'ensemble des composants

| Composant | Emplacement | Chargement | Rôle |
|---|---|---|---|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Chaque session, toujours | Conventions universelles (identité, langue, commits) |
| `settings.json` | `~/.claude/settings.json` | Lu au démarrage | Permissions, hooks, plugins, statusline |
| `rules/` | `~/.claude/rules/*.md` | À la demande, glob-scoped | Conventions techniques par stack (Python, dbt, Terraform) |
| `commands/` | `~/.claude/commands/*.md` | Explicite (`/nom`) | Slash commands — gestes rituels en contexte principal |
| `skills/` | `~/.claude/skills/<name>/` | Explicite (découverte par description) | Workflows spécialisés multi-étapes |
| `agents/` | `~/.claude/agents/*.md` | Explicite (délégation) | Subagents avec contexte isolé |
| `hooks/` | `~/.claude/hooks/*` | Événementiel (SessionStart, PreToolUse, PostToolUse) | Automatismes déclenchés par l'harness |
| `agent-memory/` | `~/.claude/agent-memory/<agent>/` | Lu/écrit par subagents | Mémoire custom portable (pas l'auto memory native) |
| `templates/` | `~/.claude/templates/*.md` | Jamais par Claude | Starters pour bootstrapper les `CLAUDE.md` projet |

---

## Principes de chargement

Trois modes différents coexistent. Savoir lequel s'applique évite deux anti-patterns : **pollution** (charger ce qui n'est pas pertinent) et **latence d'invocation** (ne rien charger quand il faut agir).

**Automatique au démarrage** : `CLAUDE.md` et `settings.json`. Ce qui y figure impacte toutes les sessions. À garder minimal.

**À la demande par glob** : `rules/*.md` via le frontmatter `globs:`. Claude charge la règle uniquement quand il touche un fichier qui matche — mais une fois chargée, elle reste active toute la session.

**Explicite** : commands, skills, agents sont invoqués par l'utilisateur (slash, nom de skill) ou par Claude (délégation agent). Rien n'est chargé implicitement.

**Événementiel** : `hooks/` déclenchés par l'harness (pas par Claude) selon les événements déclarés dans `settings.json` (`SessionStart`, `PreToolUse`, `PostToolUse`).

---

## Rules vs Templates — distinction clé

Les deux contiennent de la doctrine technique, mais ne jouent pas le même rôle.

| | `rules/` | `templates/` |
|---|---|---|
| Lu par Claude Code ? | Oui, glob-scoped | Jamais |
| Portée | Toutes sessions sur la machine | Un projet spécifique |
| Usage | Chargement auto par Claude | `cp` vers le `CLAUDE.md` projet |
| Évolution | Édition directe du fichier | Édition des placeholders après copie |

Ajouter une nouvelle `rule/` = fichier dans `rules/` + symlink dans `install.sh`.
Ajouter un nouveau template = fichier dans `templates/` (le dossier entier est symlinké, rien à faire dans `install.sh`).

---

## Commands vs Skills vs Agents — quand utiliser lequel

- **Command** : geste rituel court qui doit s'exécuter **en contexte principal** (ex. `/progress`, `/catchup`). Le rapport ou la décision doit rester visible pour l'utilisateur.
- **Skill** : workflow spécialisé invoqué par description, avec plusieurs étapes et potentiellement ses propres ressources (ex. `code-mentor`, `dp-coach`).
- **Agent** : délégation avec contexte isolé — utile quand la tâche génère beaucoup de tokens qu'on ne veut pas polluer le contexte principal (ex. `tech-watch-scorer` qui produit un JSON lourd).

Règle : migrer par **nécessité**, pas par conformité à un pattern.

---

## Composants actuels

**Commands** (7) : `catchup`, `claude-md`, `immunize`, `learning-tracker`, `prd`, `progress`, `tech-watch`

**Skills** (3) : `coach-pedagogique`, `code-mentor`, `dp-coach`

**Agents** (2) : `learning-tracker` (stateful, mémoire persistante), `tech-watch-scorer` (stateless)

**Rules** (3) : `python.md`, `dbt-sql.md`, `terraform.md`

**Templates** (4) : `python-uv.md`, `dbt-uv.md`, `terraform.md`, `pro-banking.md` (overlay)

**Hooks** (5) :
- `learning-tracker-brief.py` — SessionStart, dashboard vélocité passif
- `block-force-push.sh` — PreToolUse sur `git push*`
- `block-rm-rf.sh` — PreToolUse sur `rm *`
- `protect_env.py` — PreToolUse (Bash/Read/Edit/Write) sur `.env`
- `ruff-check.sh` — PostToolUse sur Write/Edit

---

## Usage — bootstrapper un projet

**Projet Python/uv**
```bash
mkdir my-project && cd my-project
uv init
cp ~/.claude/templates/python-uv.md ./CLAUDE.md
# Éditer les placeholders [PROJECT_NAME], etc.
```

**Projet pro (bancaire) — concaténer l'overlay**
```bash
cp ~/.claude/templates/python-uv.md ./CLAUDE.md
cat ~/.claude/templates/pro-banking.md >> ./CLAUDE.md
```

**Projet dbt**
```bash
cp ~/.claude/templates/dbt-uv.md ./CLAUDE.md
```

---

## Conventions de symlink

| Type | Stratégie | Raison |
|---|---|---|
| `CLAUDE.md`, `settings.json` | Individuel | Fichiers uniques |
| Commands, hooks, rules | Individuel | Le dossier cible peut contenir des fichiers gérés par Claude Code |
| Skills, templates, agent-memory | Dossier entier | Contrôle complet du contenu côté dotfiles |
| Agents | Mixte | Fichiers individuels + dossier `scripts/` partagé |

---

## Mémoire des subagents

`agent-memory/` est une mémoire **custom versionnée**, distincte de l'auto memory native de Claude Code (qui vit dans `~/.claude/projects/<project>/memory/` et n'est pas portable).

Chaque subagent stateful a son sous-dossier. Le chemin de `MEMORY.md` doit être **explicite** dans le prompt du subagent. Détails et convention de curation : [`agent-memory/README.md`](agent-memory/README.md).

---

## Évolutions possibles

- Rules additionnelles (Dockerfile, YAML CI, etc.)
- `/claude-md` interactif proposant un choix de template au bootstrap
- Utiliser `@import` dans les `CLAUDE.md` projet pour référencer des docs partagées
