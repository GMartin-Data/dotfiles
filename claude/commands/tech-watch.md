---
description: Pipeline complet de veille technologique — fetch, score et classe des sources
allowed-tools: Read, Bash(cat:*), Bash(uv:*), Bash(python3:*)
---

# Tech Watch Pipeline

Topic : $ARGUMENTS

## Step 1 : Récupérer les sources brutes

Exécute le fetcher pour collecter les sources :
```
uv run ~/.claude/agents/scripts/fetch-sources.py "$ARGUMENTS" --days 20 --output tech-watch/raw-sources.json
```

Si le script échoue (code retour ≠ 0) : affiche l'erreur et STOP.
Si le fichier est produit mais contient 0 sources : signale qu'aucune source n'a été trouvée et STOP.

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