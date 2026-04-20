---
description: Sauvegarde un checkpoint d'avancement dans progress.md (human-in-the-loop)
allowed-tools: Read, Write, Bash(git status:*), Bash(git diff:*), Bash(git branch:*)
model: sonnet
---

## État Git actuel
- Branche : !`git branch --show-current`
- Status : !`git status --short`
- Diff vs main : !`git diff --stat main 2>/dev/null || echo "Pas de branche main"`

## Session
ID : ${CLAUDE_SESSION_ID}

## Ta tâche

1. Lis `progress.md` s'il existe
2. Lis `PRD.md` s'il existe (pour détecter les écarts)
3. Analyse le contexte de travail courant (cette conversation)
4. Produis une mise à jour de progress.md avec ces sections :
```
## Dernière mise à jour
Date : [YYYY-MM-DD HH:MM]
Session : [CLAUDE_SESSION_ID]

## Tâches complétées
- [liste]

## En cours
- [tâche actuelle + état]

## Prochaines étapes
- [liste ordonnée]

## Écarts vs PRD
- [si divergence identifiée, sinon "Aucun"]

## Décisions prises
- [liste des choix faits pendant cette session]

## Blocages
- [si existants, sinon "Aucun"]
```

5. **Montre-moi la mise à jour AVANT d'écrire** — attends ma confirmation explicite
6. Écris dans `progress.md` (crée le fichier s'il n'existe pas)
7. **Si cette session a couvert un sujet d'apprentissage Claude Code** (skills, hooks, subagents, MCP, orchestration, agent memory, etc.), rappelle-moi gentiment de lancer `/learning-tracker debrief` pour mettre à jour MEMORY.md. Ne force pas — c'est une suggestion non-bloquante.

Ne supprime pas l'historique existant — ajoute en tête du fichier.