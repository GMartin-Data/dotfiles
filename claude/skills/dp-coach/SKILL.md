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

## Cas à ne pas déclencher

- "Review ce code existant" → code review, pas d'exercice DP
- "Explique-moi comment marche X" → tutorat général, pas d'entraînement par résolution
- "Aide-moi à déboguer Y" → assistance technique directe, pas de DP
- "Je veux apprendre le pattern Observer" → concept à comprendre, pas compétence à drill
- "Fais-moi un TP complet sur Python" → la skill cible UNE sous-compétence, pas un curriculum

## Limitations connues

- L'exécution du code utilisateur suppose un runtime disponible localement (Python, SQL via sqlite ou équivalent, bash). Pas de support pour langages nécessitant un setup complexe (compilation, dépendances externes lourdes)
- Le timeout d'exécution par défaut est court — un exercice dont la solution correcte prendrait >10s d'exécution est hors scope
- La détection "3+ passes → plus dur" est locale à la session : pas de mémoire entre invocations
- Le scoring pass/fail est binaire sur stdout — les exercices requérant une évaluation qualitative (ex. "écrire un code lisible") ne sont pas bien servis par cette skill
- Les drills sont limités aux banques présentes dans `references/` : Python et SQL pour le moment. Autres domaines (bash, regex, algorithmique pure) nécessiteraient une extension

## Anti-Patterns

- Mélanger plusieurs compétences dans un même exercice
- Donner des indices avant la tentative
- Donner la solution après le premier échec
- Exercices non-testables
- Félicitations génériques ("Bien joué !")
