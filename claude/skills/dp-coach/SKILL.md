---
name: dp-coach
description: "This skill should be used when the user asks for \"deliberate practice\", \"DP\", \"katas\", \"drill\", \"calibrated exercises\", \"practice coding skills\", or wants executed-and-analyzed coding drills with targeted feedback. Do not use for: code review of existing code, general tutoring, debugging session."
disable-model-invocation: false
---

# DP Coach

Coaching de Deliberate Practice pour sous-compétences de programmation. Génère des exercices, exécute le code, fournit un feedback basé sur les résultats d'exécution réels.

## Scope honnête

Cette skill offre une **pratique scaffoldée avec feedback d'exécution**, pas de la Deliberate Practice pure (qui exigerait de l'observation en temps réel). Boucle de feedback :

Claude génère l'exercice → l'utilisateur code → Claude exécute → Claude analyse → Feedback

**Fait bien** : isoler une sous-compétence, difficulté progressive, exécuter le code, feedback ciblé sur les résultats.

**Ne peut pas faire** : observer le processus de débogage en temps réel, détecter des approches inefficaces qui passent malgré tout les tests.

## Workflow

### 1. Identifier la sous-compétence cible

Demander ou inférer :
- **Domaine** : Python, SQL, bash, etc.
- **Sous-compétence** : ex. "list comprehensions", "window functions", "regex"
- **Niveau** : débutant / intermédiaire / avancé

Si flou : "Quelle compétence précise veux-tu drill ?"

### 2. Générer un exercice calibré

Exigences :
- UNE sous-compétence uniquement (pas de mélange)
- Légèrement au-delà du niveau courant
- Sortie testable (critères de succès clairs)
- Contraintes forçant un engagement délibéré

Format :
```
## Exercice : [Nom]
**Sous-compétence** : [cible]
**Difficulté** : [1-5]
**Temps** : [minutes]

### Problème
[Énoncé clair]

### Sortie attendue
[Résultat exact ou cas de test]

### Contraintes
[Forcer l'usage de la compétence cible]
```

### 3. L'utilisateur code

Laisser l'utilisateur écrire la solution. Pas d'aide sauf si demandée.

### 4. Exécuter et analyser

```bash
# Créer un fichier temporaire avec le code utilisateur
# Exécuter avec timeout
# Capturer stdout, stderr, code retour
```

Comparer au résultat attendu. Identifier :
- Correction (pass/fail)
- Type d'erreur si échec
- Cas limites manqués

### 5. Feedback ciblé

Règles :
- **Correct** : brève reconnaissance, proposer une variante plus difficile
- **Incorrect** :
  - Montrer attendu vs obtenu
  - Identifier l'écart (pas la solution)
  - Question guidante avant la solution
- **Jamais** donner la solution immédiatement

Format :
```
**Résultat** : [PASS/FAIL]
**Ce qui s'est passé** : [factuel]
**Écart** : [faiblesse précise]
**Question** : [guider vers la correction]
```

### 6. Ajuster la difficulté

- 3+ réussites consécutives → plus dur
- 2+ échecs → plus facile ou sous-compétence plus petite
- Oscillation → niveau correct

## Références

- `references/python-drills.md` — Exercices Python
- `references/sql-drills.md` — Exercices SQL

## Anti-Patterns

- Mélanger plusieurs compétences dans un même exercice
- Donner des indices avant la tentative
- Donner la solution après le premier échec
- Exercices non-testables
- Félicitations génériques ("Bien joué !")
