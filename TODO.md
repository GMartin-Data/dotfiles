# TODO — Workflow PRD/progress/catchup

## Évolution prévue : automatisation du checkpoint pré-clear

**Quand :** après ~10 cycles manuels du workflow PRD → CLAUDE.md → progress → catchup.

**Quoi :** évaluer un hook PreToolUse sur `/clear` qui force `/progress` avant le reset de contexte.

**Pourquoi attendre :** accumuler l'expérience des frictions réelles avant d'automatiser. Le workflow manuel permet aussi une revue de code formatrice.

**Réf :** discussion audit Module 0.3, session du 2025-03-06.