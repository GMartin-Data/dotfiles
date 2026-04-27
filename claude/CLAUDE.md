# User Conventions (Greg)

## Identity
- Data Engineer / AI Engineer
- OS: Linux (Ubuntu 22.04), Shell: zsh, Package manager: uv

## Communication
- Respond in user's language (default: French)
- All code, comments, docstrings, commits: English
- Commits: Conventional Commits format

## Session Discipline
- Before /clear or ending a session: invoke `/progress` to checkpoint current state and next steps
- Project-specific conventions live in each project's CLAUDE.md
- Lessons learned accumulate in tasks/lessons-inbox.md (via /immunize)
- One concept at a time — validate before moving to next step

## Global Do NOT
- Ne jamais formuler une étape opérationnelle dans une phrase parenthétique ou secondaire — toujours la mettre en paragraphe propre avec numérotation ou gras. Le modèle (Sonnet ou Opus) zappe systématiquement les étapes imbriquées dans une typographie de second plan. (learned 2026-04, from dotfiles)
- Quand une spec prescrit un découpage (une question à la fois, critères binaires, comportement vs implémentation, livrables vs polish), ne jamais fusionner les catégories sous prétexte d'efficacité — séquencer à la place. Le modèle écrase systématiquement ces frontières quand l'UX semble appeler un raccourci. (learned 2026-04, from memory-grep)
- Dans un workflow multi-phases, toujours vérifier la cohérence transverse avant validation finale : exclusions v1 → risques → critères de succès doivent former une chaîne sans trou ni contradiction. Ne pas traiter chaque phase en isolation. (learned 2026-04, from memory-grep)