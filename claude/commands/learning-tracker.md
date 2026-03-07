---
description: Suivi de progression d'apprentissage Claude Code — brief (dashboard) ou debrief (mise à jour)
allowed-tools: Read
argument-hint: [brief|debrief suivi d'une description]
---

# Learning Tracker

Mode : $ARGUMENTS

## Dispatch

Utilise le Task tool pour invoquer le sous-agent :
- subagent_type: learning-tracker
- description: Suivi de progression apprentissage Claude Code
- prompt: "$ARGUMENTS"

Ne fais RIEN d'autre. Transmets le résultat du sous-agent tel quel.