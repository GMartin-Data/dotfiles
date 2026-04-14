# Claude Code — Architecture 3 couches

## Principe

La configuration Claude Code est structurée en 3 couches pour éviter deux anti-patterns :
- **Pollution** : des conventions Python chargées dans une session Terraform
- **Redondance** : des guidelines projet (CI, branching) dans la config user-level

Chaque couche a un scope et un mode de chargement différent.

---

## Layer 1 — `CLAUDE.md` (user-level)

**Chargé dans chaque session.** ~20 lignes.

Ne contient que ce qui est vrai pour **tous** les projets, toujours : identité, langue, conventional commits, discipline de session. Aucune convention technique spécifique à un langage ou un stack.

## Layer 2 — `rules/` (glob-scoped)

**Chargé à la demande**, uniquement quand Claude touche un fichier qui matche le glob déclaré dans le frontmatter.

| Fichier | Globs | Chargé quand… |
|---|---|---|
| `python.md` | `*.py` | Claude lit/édite du Python |
| `dbt-sql.md` | `*.sql, models/**/*.yml` | Claude touche du SQL ou des specs dbt |
| `terraform.md` | `*.tf, *.tfvars` | Claude touche du Terraform |

Ajouter une nouvelle règle = créer un fichier dans `rules/` + ajouter le symlink dans `install.sh`.

**Attention** : le chargement est par session, pas par fichier. Si Claude touche un `.py` dans un projet Terraform, `python.md` se charge pour toute la session.

## Layer 3 — `templates/` (starters projet)

**Jamais chargé par Claude Code.** C'est du stock pour l'utilisateur.

Chaque template est un point de départ pour le `CLAUDE.md` d'un nouveau projet. On le copie, on édite les placeholders, et il est ensuite versionné dans le repo projet.

| Template | Usage |
|---|---|
| `python-uv.md` | Projet Python avec uv, ruff, pytest, CI GitHub Actions |
| `dbt-uv.md` | Projet dbt Core installé via uv, Kimball, Snowflake/BQ |
| `terraform.md` | Projet IaC Terraform |
| `pro-banking.md` | Overlay contraintes bancaires (à concaténer) |

---

## Usage

### Nouveau projet Python/uv

```bash
mkdir my-project && cd my-project
uv init
cp ~/.claude/templates/python-uv.md ./CLAUDE.md
# Éditer les placeholders [PROJECT_NAME], etc.
```

### Projet pro (bancaire) — concaténer l'overlay

```bash
cp ~/.claude/templates/python-uv.md ./CLAUDE.md
cat ~/.claude/templates/pro-banking.md >> ./CLAUDE.md
```

### Nouveau projet dbt

```bash
cp ~/.claude/templates/dbt-uv.md ./CLAUDE.md
```

---

## Conventions de symlink

| Type | Stratégie | Raison |
|---|---|---|
| CLAUDE.md, settings.json | Individuel | Fichiers uniques |
| Commands, hooks, rules | Individuel | Le dossier peut contenir des fichiers ajoutés par Claude Code |
| Skills, templates, agent-memory | Dossier entier | Contrôle complet du contenu |
| Agents | Mixte | Fichiers individuels + dossier scripts partagé |

---

## Évolutions possibles

- Faire évoluer `/claude-md` pour proposer un choix de template interactif au bootstrap
- Ajouter des rules pour d'autres types de fichiers (Dockerfile, YAML CI, etc.)
- Utiliser `@import` dans les project CLAUDE.md pour référencer des docs partagées