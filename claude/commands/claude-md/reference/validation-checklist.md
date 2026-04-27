# CLAUDE.md — Checklist de validation finale

## Table des matières
- [Checklist](#checklist) — sections obligatoires vs conditionnelles à confirmer
- [Format du récapitulatif](#format-du-récapitulatif) — template présenté à l'utilisateur
- [Porte de génération](#porte-de-génération) — pas d'écriture sans « oui » explicite

## Quand lire ce fichier
À lire en fin d'interview, juste avant d'écrire un quelconque fichier CLAUDE.md. Ce fichier applique le contrat « confirmer avant de générer ».

---

## Checklist

### Sections obligatoires

- [ ] **Vue d'ensemble du projet** — Nom, structure, composants
- [ ] **Stack** — Langage, framework, package manager, test framework (par composant)
- [ ] **Conventions de code** — Style, nommage, linter/formatter (par langage)
- [ ] **Versioning** — Format de commit, workflow

### Sections conditionnelles

Inclure si discuté :

- [ ] **Approche de test** — TDD, couverture, pyramide, quoi tester
- [ ] **Langues** — Code vs docs vs commits
- [ ] **CI/CD** — Lint, tests, déploiement
- [ ] **Workflow IA** — Fichiers de contexte, suivi d'avancement, commandes
- [ ] **Infrastructure** — Base de données, logging, serveurs MCP
- [ ] **Fichiers à ignorer** — Contenu du .claudeignore
- [ ] **Points d'attention** — Secrets, quirks d'API, pièges

### Structure documentaire

- [ ] **Structure diagnostiquée** — Mono / Hiérarchique / Hybride
- [ ] **Liste des CLAUDE.md composants** — Si hiérarchique ou hybride
- [ ] **Liste des docs de référence** — Si hybride, avec triggers « When to read »

---

## Format du récapitulatif

Présenter le résumé ainsi :

```
Récapitulatif avant génération du CLAUDE.md :

1. Projet : [name] — [structure]
2. Composants : [list]
3. Stack :
   - [component 1] : [language, framework, pkg manager, tests]
   - [component 2] : ...
4. Conventions code :
   - [language 1] : [type hints, docstrings, naming, linter]
   - [language 2] : ...
5. Tests : [approach, coverage, pyramid, priorities]
6. Commits : [format, scopes, workflow]
7. Langues : code=[X], docs=[Y], commits=[Z]
8. CI/CD : [setup]
9. Infrastructure : [DB, logging, MCP]
10. Workflow IA : [context files, commands]
11. Points d'attention : [list]

Structure documentation :
[Display diagnosed structure]

project/
├── CLAUDE.md (racine)
├── [component 1]/
│   └── CLAUDE.md
├── [component 2]/
│   └── CLAUDE.md
└── .claude/
    └── reference/
        ├── [topic-1].md — "When [trigger]"
        └── [topic-2].md — "When [trigger]"

Confirmez-vous ces éléments ? (oui / corrections)
```

---

## Porte de génération

**Ne générer les fichiers CLAUDE.md qu'après un « oui » explicite ou équivalent.** En cas de corrections, mettre à jour les réponses de phase concernées et re-présenter le récapitulatif.
