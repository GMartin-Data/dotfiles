# Parcours d'interview pour instance pré-cadrée

## Table des matières
- [Quand lire ce fichier](#quand-lire-ce-fichier)
- [Phase 1 — Vue d'ensemble (pré-remplie)](#phase-1--vue-densemble-pré-remplie)
- [Phase 2 — Stack (pré-remplie)](#phase-2--stack-pré-remplie)
- [Phase 8 — Workflow IA (pré-proposé)](#phase-8--workflow-ia-pré-proposé)
- [Phase 11 — Structure documentaire (diagnostiquée depuis l'arbo)](#phase-11--structure-documentaire-diagnostiquée-depuis-larbo)

## Quand lire ce fichier
À lire **uniquement si le pré-flight a détecté au moins un des éléments suivants** : un `.cruft.json`, un `PRD.md`, ou une arborescence de composants explicite (par ex. `src/` + `dbt/` + `terraform/`).

Ces quatre phases **remplacent** les phases de même numéro du SKILL.md. Les Phases 3, 4, 5, 6, 7, 9, 10 restent telles que définies dans SKILL.md — elles couvrent des conventions AI-driven non déductibles depuis le template ou le PRD.

Principe : Cookiecutter a déjà demandé ce qui est décidable à T0. L'interview ne porte que sur ce qui mérite délibération humaine.

---

## Phase 1 — Vue d'ensemble (pré-remplie)

Pré-remplir depuis les artefacts et demander une confirmation unique :

> « Projet détecté : **[project_name]** — composants : [liste depuis arbo]. Correct ? »

Sur « oui », passer à la Phase 2.

---

## Phase 2 — Stack (pré-remplie)

### Si Cruft détecté

La stack de base est connue. Afficher le résumé pré-rempli et ne demander que les compléments :

> « Stack de base depuis Cruft : Python [version] (uv), [dbt adapter si présent], [terraform provider si présent]. Confirmation + ajouts (framework web, ORM, libs spécifiques non capturés par le template) ? »

Sur « rien à ajouter », marquer la phase validée.

### Si PRD.md présent sans Cruft

Extraire la section « Stack technique » du PRD, pré-remplir, demander confirmation rapide.

---

## Phase 8 — Workflow IA (pré-proposé)

Pré-proposer un workflow par défaut cohérent avec l'instance :

> « Workflow IA pré-proposé :
> - Context files : PRD.md (intention figée), progress.md (état courant via /progress)
> - Progress tracking : progress.md mis à jour via skill /progress
> - Frequent commands : [lister d'après Cruft — ex. `uv run`, `dbt build`, `terraform plan`]
>
> Ajouts ou ajustements ? »

---

## Phase 11 — Structure documentaire (diagnostiquée depuis l'arbo)

Diagnostiquer directement depuis l'arborescence réelle listée au pré-flight (plus fiable que des réponses d'interview). Appliquer l'arbre de décision ci-dessous sur les dossiers détectés, puis présenter le diagnostic pour une validation unique — pas d'interview.

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

### Si approche hybride diagnostiquée

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
