# CLAUDE.md — Templates de sortie

## Table des matières
- [Root CLAUDE.md](#root-claudemd) — conventions projet au niveau racine
- [Child CLAUDE.md (composants)](#child-claudemd-composants) — delta par composant
- [Reference Documentation (si hybride)](#reference-documentation-si-hybride) — sujets transverses sous `.claude/reference/`

## Quand lire ce fichier
À lire après validation de la checklist finale, au moment d'écrire les fichiers. Choisir le(s) template(s) correspondant à la structure documentaire diagnostiquée en Phase 11.

---

## Root CLAUDE.md

Générer avec ces sections (omettre si N/A) :

```markdown
# CLAUDE.md — [project-name]

## Vue d'ensemble
[Brief description + pointers to key docs]

## Structure du projet
[Tree structure if relevant]

## Reference Documentation
[If hybrid approach — routing table]

| Document | When to Read |
|----------|--------------|
| `.claude/reference/[topic].md` | [trigger] |

## Conventions [Language] ([component])
### Environnement
### Style de code
### Exemple

## Tests
### Approche
### Pyramide (unit/integration/e2e)
### Couverture cible
### Fonctions à tester en priorité
### Ne pas tester

## Versioning
### Commits
### Workflow Git

## Langues
| Contexte | Langue |
|----------|--------|
| Code (commentaires, docstrings) | ... |
| Documentation | ... |
| Commits | ... |

## CI/CD

## Infrastructure
### Base de données
### Logging
### MCP Servers

## Workflow avec Claude
### Gestion du contexte
### Commandes fréquentes

## Fichiers à ignorer
[.claudeignore content or patterns]

## Points d'attention
[Warnings, secrets, pitfalls]
```

---

## Child CLAUDE.md (composants)

Plus court, focalisé sur le delta par rapport au root :

```markdown
# CLAUDE.md — [component]

## Environnement
[Language, framework, package manager specific to this component]

## Style de code
[Only if different from root]

## Commandes fréquentes
[Component-specific commands]
```

---

## Reference Documentation (si hybride)

Pour chaque sujet transverse, créer `.claude/reference/[topic].md` :

```markdown
# [Topic] — Best Practices

## When to Read
[Explicit trigger: "Read this when working on X"]

## [Content organized by subtopic]
```
