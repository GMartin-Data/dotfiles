# Scaffold : Python + uv

Infrastructure déterministe pour projets Python 3.12+ avec uv, ruff, pytest et versioning automatique.

## Contenu

| Fichier | Rôle |
|---|---|
| `.pre-commit-config.yaml` | Hooks locaux : ruff check (avec --fix) + ruff format |
| `.github/workflows/ci.yml` | CI sur chaque PR : lint + tests |
| `.github/workflows/release.yml` | Versioning automatique sur merge to main |
| `.github/pull_request_template.md` | Rappel du format conventional commit pour le titre |
| `pyproject-snippet.toml` | Section `[tool.semantic_release]` à copier dans pyproject.toml |
| `python-uv.md` | Template Claude Code → à copier dans `~/.claude/templates/` |

## Mise en place

```bash
# Depuis la racine du nouveau projet
cp -r ~/dotfiles/scaffolds/python-uv/.github .
cp ~/dotfiles/scaffolds/python-uv/.pre-commit-config.yaml .

# Coller la section semantic_release dans pyproject.toml
cat ~/dotfiles/scaffolds/python-uv/pyproject-snippet.toml >> pyproject.toml

# Installer les hooks
uv run pre-commit install
```

Vérifier que `pyproject.toml` contient bien `project.version` — c'est le champ que semantic-release lit et écrit.

## Workflow de versioning

Le système repose sur une chaîne linéaire :

```
titre PR (conventional commit)
    → squash and merge
        → commit unique sur main
            → python-semantic-release lit le commit
                → bump version + tag + changelog + GitHub Release
```

### Pourquoi le titre de la PR est critique

Avec squash and merge, GitHub utilise le **titre de la PR** comme message du commit résultant sur main. C'est ce commit unique que python-semantic-release analyse pour décider du bump.

Les commits individuels dans la branche n'ont aucun impact sur le versioning. Seul le titre compte.

### Format du titre

```
<type>(<scope>): <description>
```

Exemples :
- `feat(auth): add JWT refresh endpoint` → bump **minor**
- `fix(parser): handle empty input` → bump **patch**
- `feat!: remove v1 API` → bump **major**
- `docs: update README` → **pas de bump**
- `chore: upgrade dependencies` → **pas de bump**

### Mapping type → version

| Type | Bump |
|---|---|
| `feat` | minor (0.x.0) |
| `fix`, `perf` | patch (0.0.x) |
| `!` (breaking, sur n'importe quel type) | major (x.0.0) |
| `docs`, `style`, `refactor`, `test`, `ci`, `chore` | aucun |

### Ce que semantic-release fait sur main

À chaque push sur main, le workflow `release.yml` :

1. Clone le repo avec l'historique complet (`fetch-depth: 0`)
2. Analyse les commits depuis le dernier tag
3. Si un bump est détecté :
   - Met à jour `project.version` dans pyproject.toml
   - Commit le changement (`chore(release): v{version}`)
   - Crée un tag git
   - Met à jour CHANGELOG.md
   - Publie une GitHub Release

Si aucun commit ne déclenche de bump (que des `docs`, `chore`, etc.), rien ne se passe.

## CI

La CI (`ci.yml`) bloque le merge si :
- `ruff check .` échoue (lint)
- `ruff format --check .` échoue (formatage)
- `pytest` échoue

Elle utilise `uv sync --frozen` : si le lockfile est désynchronisé, la CI échoue. Pour ajouter une vérification explicite du lockfile, ajouter un step `uv lock --check` avant le sync.

## Pre-commit

Les hooks ruff tournent en local avant chaque commit. `ruff check` est lancé avec `--fix` et `--exit-non-zero-on-fix` : il corrige ce qu'il peut, mais échoue si des corrections ont été appliquées (pour que le développeur vérifie et re-stage).

Installation unique par projet :

```bash
uv run pre-commit install
```

## Choix de design

**Pas de publication PyPI.** Le workflow release crée un tag + GitHub Release mais ne publie pas sur PyPI. Si nécessaire, ajouter un job `publish` dans `release.yml` avec `uv build` + `uv publish` ou trusted publishing.

**Pas de matrice Python.** La CI teste uniquement Python 3.12. Si le projet doit supporter plusieurs versions, convertir le step `setup-python` en matrice.

**`uv sync --frozen` plutôt que `uv sync`.** En CI, on veut reproduire exactement le lockfile committé, pas résoudre à nouveau.

**Concurrency sur le job release.** Empêche deux runs parallèles de semantic-release si deux PRs sont mergées rapidement. Sans ça, risque de conflit sur le tag ou le commit de version.