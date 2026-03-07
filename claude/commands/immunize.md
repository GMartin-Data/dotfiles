---
description: Consolide lessons-inbox.md — promeut les patterns récurrents, archive le bruit, immunise le workflow
argument-hint: [lesson-description]
allowed-tools: Read, Write, Bash(grep:*), Bash(wc:*), Bash(cat:*), Bash(date:*)
model: sonnet
---

## Objectif

Consolider `tasks/lessons-inbox.md` en appliquant le cycle immunitaire à trois niveaux :

- **Réponse innée** (inbox) → **Anticorps projet** (CLAUDE.md projet) → **Anticorps globaux** (~/.claude/CLAUDE.md)

## Pré-requis

Lire les fichiers suivants avant toute action :

1. `tasks/lessons-inbox.md`
2. Section `## Do NOT` du CLAUDE.md projet (racine)
3. Section `## Global Do NOT` de `~/.claude/CLAUDE.md`

Si l'inbox est vide, le signaler et s'arrêter.

## Procédure

### Étape 1 — Inventaire

Lire `tasks/lessons-inbox.md`. Compter les entrées. Afficher le résumé :
- Nombre total d'entrées
- Plage de dates (plus ancienne → plus récente)

### Étape 2 — Regroupement

Regrouper les entrées par pattern similaire (même type d'erreur, même règle sous-jacente).
Pour chaque groupe, indiquer :
- Nombre d'occurrences
- Dates des occurrences
- Règle sous-jacente commune

### Étape 3 — Décision par groupe

Pour chaque groupe, appliquer les règles suivantes dans l'ordre :

**A) Pattern récurrent (2+ occurrences) → Promotion**

Déterminer la portée :

1. **Spécifique au projet** (mentionne un outil, lib, API, convention propre au projet) :
   - Vérifier qu'aucune règle équivalente n'existe dans le CLAUDE.md projet
   - Si nouvelle : rédiger la règle, destination = CLAUDE.md projet section `## Do NOT`

2. **Générique** (pattern Python, git, code, workflow réutilisable tous projets) :
   - Lire `~/.claude/CLAUDE.md` section `## Global Do NOT`
   - **Cas A** : règle équivalente existe déjà en global → skip
   - **Cas B** : règle SIMILAIRE existe avec tag `(from [autre-projet])` → le pattern est confirmé cross-projet. Mettre à jour le tag en `(learned YYYY-MM, confirmed across projects)`
   - **Cas C** : aucune règle similaire en global → ajouter comme candidate avec tag `(learned YYYY-MM, from [nom-projet-actuel])`. Elle ne sera confirmée que quand un autre projet la remontera.

**B) Entrée unique, > 7 jours → Archivage**

Déplacer vers `tasks/lessons-archive.md` avec la date d'archivage.

**C) Entrée unique, ≤ 7 jours → Conservation**

Laisser dans l'inbox. Elle peut encore être confirmée par une nouvelle occurrence.

### Étape 4 — Plan d'action

Afficher un résumé structuré AVANT d'écrire :

```
=== IMMUNIZE PLAN ===

PROMOTIONS PROJET (→ CLAUDE.md ## Do NOT) :
- "Ne jamais [X] — utiliser [Y] à la place (learned YYYY-MM)"

PROMOTIONS GLOBALES (→ ~/.claude/CLAUDE.md ## Global Do NOT) :
- "Ne jamais [X] (learned YYYY-MM, from [projet])"

CONFIRMATIONS CROSS-PROJET :
- Mise à jour tag : "[règle]" → "(confirmed across projects)"

ARCHIVAGE (→ tasks/lessons-archive.md) :
- [YYYY-MM-DD] description

CONSERVATION (restent dans inbox) :
- [YYYY-MM-DD] description

=== FIN DU PLAN ===
```

Demander confirmation explicite avant de continuer.

### Étape 5 — Exécution

Après confirmation :

1. Ajouter les règles promues dans les CLAUDE.md respectifs
2. Ajouter les entrées archivées dans `tasks/lessons-archive.md`
3. Réécrire `tasks/lessons-inbox.md` avec uniquement les entrées conservées
4. Afficher le résumé final avec compteurs

## Format des règles promues

```
- Ne jamais [action interdite] — utiliser [alternative] à la place (learned YYYY-MM)
```

Pour les candidats globaux :
```
- Ne jamais [action interdite] — utiliser [alternative] à la place (learned YYYY-MM, from [projet])
```

Pour les confirmations cross-projet :
```
- Ne jamais [action interdite] — utiliser [alternative] à la place (learned YYYY-MM, confirmed across projects)
```

## Contraintes

- Ne jamais modifier une règle existante dans un CLAUDE.md
- Ne jamais supprimer une entrée sans l'archiver ou la conserver
- Maximum 20 règles dans `~/.claude/CLAUDE.md` section `## Global Do NOT`
- Si le cap global est atteint : signaler et demander quelle règle fusionner ou retirer
- Toujours demander confirmation avant d'écrire