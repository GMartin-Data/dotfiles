---
description: Reconstruit le contexte de travail après /clear ou reprise de session
allowed-tools: Read, Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git log:*)
model: haiku
---

## État Git
- Branche : !`git branch --show-current`
- Status : !`git status --short`
- Diff vs main : !`git diff --stat main 2>/dev/null || echo "Pas de branche main"`
- Derniers commits : !`git log --oneline -5 2>/dev/null || echo "Pas d'historique"`

## Artefacts projet
Lis ces fichiers s'ils existent :
- progress.md (source de vérité sur l'avancement)
- PRD.md (intention initiale, figé)
- CLAUDE.md (conventions)

## Ta tâche
Produis un résumé structuré en 3 parties :
1. **État actuel** — où en est le travail (branche, fichiers modifiés, dernière action)
2. **Prochaine étape** — la tâche immédiate à reprendre
3. **Décisions en suspens** — si progress.md mentionne des points ouverts

Sois concis. Pas de reformulation du PRD ou du CLAUDE.md — juste l'état et la direction.