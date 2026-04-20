## Méta
- Première session : 2026-03-07
- Sessions totales : 3
- Sujets actifs : 1 | Complétés : 0 | Archivés : 3

## Sujets

### dotfiles-audit [ACTIF]
- Description : Audit structuré de ~/dotfiles/claude/ (8 phases prévues) contre les best-practices Claude Code 2026.
- Statut : Phase 5 (Agents) en cours — tech-watch-scorer audité et corrigé (commit 4e1e979), learning-tracker en cours de refonte active (hook SessionStart + rappel /progress en design).
- Sessions : ~6 (depuis 2026-04-18)
- Premier contact : 2026-04-18
- Dernier contact : 2026-04-20
- Vélocité : ~3 sessions/semaine
- Prochaine étape : implémentation hook SessionStart pour dashboard brief automatique, puis corps de learning-tracker.md + scripts Python + agent-memory/ (suite Phase 5).
- Branches ouvertes :
  - Piste C Phase 2 : faire évoluer /claude-md pour détecter marqueur Cookiecutter
  - Point 5/6 Phase 3-4 : migration éventuelle des dispatchers vers skill Mode C (reporté à la fin de Phase 5)
  - Méta-lesson : pattern "exploration systématique → besoin-driven" (candidat lessons-inbox via /immunize)

### shanraisshan-exploration [ARCHIVÉ - réorienté 2026-04-20]
- Parcours linéaire interrompu au module 4/8 (socle acquis : CLAUDE.md, hooks, commands, skills, subagents, orchestration, agent memory).
- Réorientation : le repo s'utilise désormais comme référence ciblée pendant l'audit dotfiles, pas comme parcours linéaire. Les modules 5-8 restent disponibles pour consultation au cas par cas si un besoin émerge.
- Modules absorbés :
  - Module 0 : Audit setup
  - Module 1 : Commands avancées
  - Module 2 : Skills & Subagents (hands-on tech-watch-scorer)
  - Module 3 : Orchestration Command → Agent → Skill
  - Module 4 : Agent Memory (hands-on learning-tracker)

### mcp-server-mastery [ARCHIVÉ - réorienté 2026-04-20]
- Roadmap interrompue après modules 1.1–1.4. Phase sécurité (module 2.1) non démarrée et retirée du périmètre.
- Leçon retenue et intégrée : sobriété MCP (n'activer qu'au besoin réel, pas par exploration systématique).
- Réorientation : les MCP servers s'étudient désormais à la demande — quand un besoin précis émerge. La conception d'un MCP custom reste hors-périmètre pour l'instant (pratique actuelle trop restreinte).

### claude-code-sandboxing [ARCHIVÉ - réorienté 2026-04-20]
- Workshop TP0-TP8 jamais démarré (0 session en 50 jours).
- Motivation initiale identifiée : curiosité + souci de sécurité général, pas un besoin concret actionnable.
- Réorientation : sujet déplacé en veille passive. Conscience que le sandboxing est une piste sécurité existante ; sera approfondi si un besoin précis émerge (incident, changement d'environnement, question sécurité ciblée).
- Acquis préservé : la piste est identifiée, pas besoin de "découvrir" son existence à nouveau.
