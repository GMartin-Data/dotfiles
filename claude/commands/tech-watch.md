---
description: Pipeline complet de veille technologique — score et classe des sources brutes
allowed-tools: Read, Bash(cat:*), Bash(mkdir:*), Bash(python3:*)
---

# Tech Watch Pipeline

Topic : $ARGUMENTS

## Step 1 : Vérifier les sources brutes

Vérifie que `tech-watch/raw-sources.json` existe.
Si le fichier n'existe PAS : affiche un message d'erreur clair et STOP.
Le fichier doit être préparé manuellement avant de lancer cette command.

## Step 2 : Scoring des sources

Utilise le Task tool pour invoquer le scorer :
- subagent_type: tech-watch-scorer
- description: Score les sources sur le topic "$ARGUMENTS"
- prompt: Score les sources dans tech-watch/raw-sources.json sur le topic "$ARGUMENTS". Écris les résultats dans tech-watch/scores.json selon tes instructions de scoring.
- model: sonnet

Attends la complétion de l'agent.

## Step 3 : Vérifier le résultat

Vérifie que `tech-watch/scores.json` existe et contient du JSON valide :
`cat tech-watch/scores.json | python3 -m json.tool > /dev/null 2>&1`

Si le fichier n'existe pas ou le JSON est invalide : signale l'échec du scorer, ne pas inventer de données.

## Step 4 : Formater le rapport

Lis `tech-watch/scores.json`.

Produis un rapport lisible avec :
- Date et topic
- Top sources (score >= 80) en détail : titre, type, score, justification
- Sources retenues (60-79) : titre, type, score (une ligne chacune)
- Sources éliminées avec raison
- Statistiques : nombre total, retenues, éliminées, score moyen, score max

## Critical Requirements

1. **Task tool pour le scorer** : NE PAS utiliser bash pour invoquer l'agent.
2. **Séquentiel** : attendre la fin du Step 3 avant le Step 4.
3. **Pas d'invention** : si scores.json n'existe pas ou est invalide, signaler l'échec.
4. **$ARGUMENTS obligatoire** : si aucun topic n'est fourni, demander à l'utilisateur.