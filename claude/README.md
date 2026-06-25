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

**Commands** (9) :
- `adr` — crée un ADR atomique (mode interview ou capture), avec supersession bidirectionnelle
- `catchup` — reconstruit le contexte de travail après `/clear` ou reprise de session
- `claude-md` — interview structurée produisant un CLAUDE.md projet (détection d'instance Cruft/PRD)
- `grill` — revue adverse d'un PRD/PLAN avant gel ; lève implicites et tensions, ne modifie aucun artefact
- `immunize` — consolide `lessons-inbox.md` : promeut les patterns récurrents, archive le bruit
- `planning` — génère PLAN.md (architecture cible + phases) à partir de PRD + CLAUDE.md
- `prd` — interview structurée produisant un PRD (détection d'instance Cruft)
- `progress` — sauvegarde un checkpoint d'avancement dans `progress.md` (human-in-the-loop)
- `tech-watch` — pipeline de veille techno : fetch, score et classe des sources

> Cinq commands ont un sous-dossier compagnon (`commands/<name>/`) qui matérialise la **progressive disclosure**. Deux types d'assets y vivent : `evals/` (corpus de tests A→B→A — interne au repo, non symlinké) pour `adr`, `claude-md`, `grill`, `planning`, `prd` ; et `reference/` (assets runtime — chargés par la command à l'exécution, symlinké) pour `claude-md` uniquement. Pattern symétrique à celui des skills, mais conservé en command pour préserver l'invocation explicite.

### Ajouter une command — checklist multi-fichiers

Créer une command touche **quatre lieux**. En oublier un laisse une dérive silencieuse (command absente d'un bootstrap neuf, ou doc périmée). À refaire à chaque ajout :

1. **Source** — écrire `claude/commands/<name>.md` (+ `commands/<name>/evals/` si corpus de tests).
2. **Symlink** — déclarer la ligne `link` dans `install.sh`, puis créer le symlink effectif (`ln -sfn`).
3. **README racine** — ajouter `<name>` à la ligne `**Commands**` de `README.md` (listing nominal court).
4. **README claude** — ajouter une puce `<name> — <glose d'une ligne>` à la liste `**Commands** (N)` de ce fichier, **incrémenter le compteur `(N)`**, et étendre la note des sous-dossiers compagnons si la command a un `evals/`.

Test de parité (sortie vide = OK) :

```bash
diff <(ls claude/commands/*.md | xargs -n1 basename | sed 's/\.md$//' | sort) \
     <(grep -oP 'commands/\K[a-z-]+\.md' install.sh | sed 's/\.md$//' | sort -u)
```

### Ajouter une skill — checklist multi-fichiers

Une skill est un **dossier** (`skills/<name>/SKILL.md`), pas un fichier — sinon les quatre lieux sont les mêmes qu'une command. En oublier un laisse la même dérive silencieuse :

1. **Source** — écrire `claude/skills/<name>/SKILL.md` (frontmatter `name`/`description` + corps). Le dossier entier est l'unité ; les assets compagnons y vivent.
2. **Symlink** — déclarer la ligne `link` du **dossier** dans `install.sh` (bloc Skills), puis créer le symlink effectif (`ln -sfn`).
3. **README racine** — ajouter `<name>` à la ligne `**Skills**` de `README.md` (listing nominal court).
4. **README claude** — ajouter une puce `<name> — <glose>` sous la famille pertinente de la liste `**Skills** (N)` de ce fichier, et **incrémenter le compteur `(N)`**.

Test de parité (sortie vide = OK) :

```bash
diff <(ls -d claude/skills/*/ | xargs -n1 basename | sort) \
     <(grep -oP 'skills/\K[a-z-]+' install.sh | sort -u)
```

**Skills** (5) :

Couche learning, non-overlap (cf. [responsibility-matrix](../docs/methodology/responsibility-matrix.md), section Couche learning) :
- `teach` — enseigne un concept/compétence ; colonne vertébrale stateful (workspace dédié, human-triggered)
- `code-mentor` — déchiffre du code *existant* par questionnement socratique ; produit des flashcards Anki
- `coach-pedagogique` — accompagne la *livraison* d'un vrai artefact par scaffolding dégressif (niveaux 1-4)
- `dp-coach` — drille une sous-compétence par exécution + analyse déterministe du code (deliberate practice)

Revue :
- `code-review` — première passe sur le diff (bugs, sécurité, invariants, conventions) ; **surcharge** la bundled, signale sans appliquer (cf. [ADR-0010](../adr/0010-surcharge-code-review-user-scope.md))

**Agents** (1) : `tech-watch-scorer` (stateless)

**Rules** (3) : `python.md`, `dbt-sql.md`, `terraform.md`

**Templates** (4) : `python-uv.md`, `dbt-uv.md`, `terraform.md`, `pro-banking.md` (overlay)

**Hooks** (4) :
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
- Utiliser `@import` dans les `CLAUDE.md` projet pour référencer des docs partagées
- Factoriser un `cruft-reader` partagé entre `/prd` et `/claude-md` (différé YAGNI tant que la duplication reste minime)
