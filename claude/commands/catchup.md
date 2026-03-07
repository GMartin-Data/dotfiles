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

Ne supprime pas l'historique existant — ajoute en tête du fichier.
```

Justifications : `sonnet` parce qu'il faut analyser le contexte de la conversation courante et synthétiser. `${CLAUDE_SESSION_ID}` pour la traçabilité — tu pourras remonter quel checkpoint vient de quelle session. Le "montre-moi avant d'écrire" implémente le human-in-the-loop décidé en Module 0.3.

---

### Récapitulatif des actions

| Fichier | Action | Effort |
|---|---|---|
| `~/.claude/commands/prd.md` | Remplacer frontmatter + ajouter injection contexte | ~2 min |
| `~/.claude/commands/claude-md.md` | Ajouter frontmatter + injection contexte | ~2 min |
| `~/.claude/commands/immunize.md` | Ajouter `argument-hint` et `model` | ~1 min |
| `~/.claude/commands/catchup.md` | Créer (contenu complet ci-dessus) | ~1 min |
| `~/.claude/commands/progress.md` | Créer (contenu complet ci-dessus) | ~1 min |

### Structure cible après déploiement
```
~/.claude/commands/
├── catchup.md      ← NOUVEAU
├── claude-md.md    ← MODIFIÉ (frontmatter + injection)
├── immunize.md     ← MODIFIÉ (argument-hint + model)
├── prd.md          ← MODIFIÉ (frontmatter + injection)
└── progress.md     ← NOUVEAU