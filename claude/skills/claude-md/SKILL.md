---
name: claude-md
description: Cette skill doit être utilisée quand l'utilisateur demande à produire un CLAUDE.md projet, définir les conventions Claude Code d'un projet, formaliser la stack/les conventions/le workflow IA d'un repo existant, ou dit "génère le CLAUDE.md", "crée les conventions projet", "cadre l'IA pour ce projet". Détecte automatiquement les instances pré-cadrées (présence d'un `.cruft.json`, d'un `PRD.md` ou d'une arborescence explicite) pour alléger les phases Overview/Stack/Documentation Structure déjà déterminées par le template ou le PRD. Inclut la génération hiérarchique (root + sous-composants). Ne pas utiliser pour : éditer le CLAUDE.md user global (~/.claude/CLAUDE.md), rédiger un PRD (c'est la skill prd), ou mettre à jour des conventions techniques glob-scoped (cela vit dans rules/).
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Glob, Bash
paths: ["CLAUDE.md", "PRD.md", ".cruft.json"]
model: sonnet
---

# Interview Conventions

Processus d'interview structurée pour produire un CLAUDE.md complet (avec structure hiérarchique optionnelle) par questionnement incrémental.

---

## Step 0 — Lire le CLAUDE.md projet existant si présent

Avant de démarrer l'interview, lire `CLAUDE.md` à la racine du CWD (racine du projet). S'il existe, en résumer le contenu et demander à l'utilisateur s'il veut **remplacer**, **étendre** ou **abandonner**. S'il est absent, enchaîner directement sur le pré-flight.

---

## Pré-flight — détection d'instance (Cruft + PRD + arbo)

**Avant Phase 1**, collecter le contexte disponible sans poser de question :

1. **`.cruft.json`** — si présent à la racine du CWD, lire `context.cookiecutter` pour extraire : `project_name`, `python_version`, `license`, `branch_protection_profile`, et les flags `use_dbt` / `use_terraform`.
2. **Arborescence racine** — lister les dossiers présents (`src/`, `dbt/`, `terraform/`, `tests/`, `docs/`, `.github/`, etc.). L'arbo fait foi : un post-hook Cruft supprime les dossiers non retenus.
3. **`PRD.md`** — si présent, le lire pour récupérer : problème, utilisateurs, interface, stack technique, architecture, phases d'implémentation.

Si **aucun** de ces trois artefacts n'existe : procéder à l'interview standard complète (toutes les phases).

Si **au moins un** est présent : afficher le résumé détecté et annoncer l'allègement :

```
Instance pré-cadrée détectée :

- Cruft : [oui — Python X.Y, dbt/Terraform selon flags | non]
- PRD.md : [trouvé — projet [nom], interface [X], stack [Y] | absent]
- Composants détectés (arbo) : [liste : src/, dbt/, terraform/, ...]

Les phases suivantes seront **allégées ou pré-remplies** :
- Phase 1 (Vue d'ensemble), Phase 2 (Stack) → confirmation rapide depuis Cruft+PRD
- Phase 11 (Structure documentaire) → diagnostic direct depuis l'arbo
- Phase 8 (Workflow IA) → pré-rempli (progress.md, PRD.md)

Phases restant à cadrer intégralement (conventions AI-driven, non déductibles) :
- Phase 3 (Conventions de code) — type hints, docstrings, naming, linter
- Phase 4 (Approche de test) — TDD, couverture, pyramide
- Phase 6 (Langues) — code vs docs vs commits
- Phase 7 (CI/CD) — triggers, déploiement
- Phase 10 (Points d'attention) — secrets, pièges

Principe : Cookiecutter a déjà demandé ce qui est décidable à T0.
L'interview ne porte que sur ce qui mérite délibération humaine.
```

**Pour les Phases 1, 2, 8 et 11, suivre `reference/instance-aware-flow.md` au lieu du texte standard ci-dessous.** Les Phases 3, 4, 5, 6, 7, 9, 10 restent telles que définies ci-dessous.

---

## Règles d'interaction

1. **Une question à la fois** — ne jamais surcharger avec plusieurs questions
2. **Options A/B/C** — proposer des choix quand des alternatives discrètes existent
3. **Valider avant de continuer** — reformuler uniquement sur les réponses ambiguës
4. **YAGNI** — challenger le sur-engineering, garder les conventions minimales
5. **Par composant** — si projet multi-composants, demander les conventions pour chacun
6. **Adapter la langue** — matcher la langue de l'utilisateur pendant l'interview et dans la sortie

---

## Séquence d'interview

Progresser à travers les phases dans l'ordre. Ne skipper une phase que si elle est clairement hors sujet.

### Phase 1 — Vue d'ensemble du projet

(Si pré-flight a détecté une instance, suivre `reference/instance-aware-flow.md` pour cette phase.)

« Quel est le nom du projet et sa structure ? »
- Composant unique ou monorepo ?
- Lister les composants s'il y en a plusieurs (ex. backend, extension, CLI)

### Phase 2 — Stack (par composant)

(Si pré-flight a détecté une instance, suivre `reference/instance-aware-flow.md` pour cette phase.)

Pour chaque composant :
« Quelle est la stack de [composant] ? »
- Langage + version
- Framework
- Package manager
- Framework de test

### Phase 3 — Conventions de code (par langage)

Pour chaque langage présent dans le projet :
« Quelles sont tes conventions de code pour [langage] ? »
- Type hints / mode strict ?
- Format de docstring (Google, NumPy, JSDoc) ?
- Conventions de nommage (snake_case, camelCase, PascalCase) ?
- Linter / formatter ?
- Langue des commentaires ?

### Phase 4 — Approche de test

« Quelle est ton approche de test ? »
- TDD ? Si oui, strict ou light ?
- Cible de couverture ?
- Pyramide de test (ratio unit/integration/e2e) ?
- Quoi tester (happy path, erreurs, edge cases) ?
- Ce qu'il ne faut PAS tester (glue code, trivial) ?

### Phase 5 — Versioning

« Quel est ton workflow Git ? »
- Format de commit (conventional commits ?)
- Scopes si monorepo ?
- Qui commite ? (IA prépare, humain valide ?)
- Stratégie de branches ?

### Phase 6 — Langues

« Quelle langue pour quel contexte ? »
- Code (commentaires, docstrings)
- Documentation (README, PRD)
- Messages de commit

### Phase 7 — CI/CD

« Quel est ton setup CI/CD ? »
- CI : lint, tests, sur quels triggers ?
- CD : manuel ou automatique ? Plateforme ?

### Phase 8 — Workflow IA

(Si pré-flight a détecté une instance, suivre `reference/instance-aware-flow.md` pour cette phase.)

« Comment les assistants IA doivent-ils travailler sur ce projet ? »
- Fichiers de contexte à lire en premier ?
- Fichier de suivi d'avancement ?
- Fichiers à ignorer (.claudeignore) ?
- Commandes fréquentes ?

### Phase 9 — Infrastructure (si applicable)

« Le projet utilise-t-il l'un des éléments suivants ? »

**Base de données :**
- ORM / query builder ?
- Outil de migration ?
- Patterns de connexion (pooling, PRAGMAs) ?

**Logging :**
- Logging structuré (structlog, pino) ?
- Format (JSON, pretty) ?
- Politique de niveaux de log ?

**Serveurs MCP :**
- Quels serveurs MCP sont configurés ?
- Quand utiliser chacun ?

Skipper les sous-sections qui ne s'appliquent pas.

### Phase 10 — Points d'attention

« Des avertissements ou contraintes spécifiques ? »
- Gestion des secrets
- Quirks d'API
- Pièges connus
- Fichiers à ne jamais modifier

### Phase 11 — Structure documentaire (diagnostic)

(Si pré-flight a détecté une instance, suivre `reference/instance-aware-flow.md` pour cette phase — le diagnostic se fait alors directement depuis l'arborescence réelle.)

**Ne pas demander la préférence de l'utilisateur. Diagnostiquer automatiquement depuis les réponses des Phases 1-2 :**

```
Multi-composants avec stacks différentes ?
    │
    ├── NON → CLAUDE.md seul (+ .claude/reference/ si docs volumineuses)
    │
    └── OUI → Conventions partagées entre composants ?
                  │
                  ├── NON → Hiérarchique seul
                  │         (component/CLAUDE.md par composant)
                  │
                  └── OUI → Hybride
                            (hiérarchique + .claude/reference/)
```

**Si approche hybride diagnostiquée :**

Identifier quelles conventions sont :
- **Spécifiques à un composant** → iront dans `component/CLAUDE.md`
- **Transverses** → iront dans `.claude/reference/`

Présenter le diagnostic :
> « D'après la structure du projet, je vais générer :
> - Root CLAUDE.md avec les conventions globales
> - [component]/CLAUDE.md pour les conventions propres à [langage]
> - .claude/reference/ pour les patterns partagés : [liste]
>
> Cette structure te convient-elle ? »

**Conventions transverses typiques à chercher :**
- Stratégie de test (si même philosophie entre composants)
- Standards de logging (si format unifié)
- Patterns de déploiement
- Conventions de design d'API (si consommée entre composants)

---

## Validation finale

Avant d'écrire le moindre fichier, appliquer la checklist et présenter le récapitulatif à l'utilisateur. **Suivre `reference/validation-checklist.md`** pour le détail des sections à vérifier, le format de récapitulatif, et la porte de génération (pas d'écriture sans « oui » explicite).

---

## Format de sortie

Une fois la validation obtenue, écrire les fichiers selon les templates de **`reference/output-format.md`** (Root CLAUDE.md, Child CLAUDE.md par composant, fichiers `.claude/reference/` si structure hybride).

---

## Après génération

Après avoir créé le(s) fichier(s) CLAUDE.md :
1. Confirmer les chemins des fichiers
2. Si hiérarchique ou hybride, lister tous les fichiers créés
3. Suggérer de les ajouter au contrôle de version
4. Rappeler de créer `.claudeignore` si discuté
5. Si des serveurs MCP ont été mentionnés, rappeler de vérifier `claude mcp list`
