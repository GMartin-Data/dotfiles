## Sujets archivés ou complétés — narratif long

Ce fichier contient le contexte détaillé des sujets sortis de MEMORY.md (verbosité incompatible avec le seuil de 150 lignes).
MEMORY.md ne conserve qu'une trace courte (3 lignes max) avec pointeur vers ce fichier.

---

### dotfiles-audit [ARCHIVÉ - clôture 2026-04-27]

Audit structuré de ~/dotfiles/claude/ conduit du 2026-04-18 au 2026-04-27 (~8 sessions, ~3.5 sessions/semaine).

Phases couvertes :
- Phase 1 : Architecture (inventaire structure, conventions nommage)
- Phase 2 : Mémoire & config (agent-memory, settings, CLAUDE.md)
- Phase 3 : Commands & hooks (dispatchers, SessionStart hook)
- Phase 4 : Skills (structure, frontmatter, invocation)
- Phase 5 : Agents (subagents, orchestration)
- Phase 6 : Méta & cohérence (migration /prd et /claude-md commands→skills→commands, campagne evals A→B→A)
- Phase 6g : Campagne A→B→A /prd — 3 evals, 1 fix doctrinal prd.md
- Phase 7 : Exécution consolidée — AUDIT_PROGRESS.md supprimé, trace migrée vers commits + fiches ~/claude-audit-notes/ + lessons-inbox.md + MEMORY.md

Doctrines validées et intégrées :
- "Migrer par nécessité" bidirectionnelle : commands→skills ET skills→commands sont tous deux légitimes selon le cas d'usage. Pas de direction canonique unique.
- Protocole A→B→A pertinent en mode command (CWD propre + transcription figée garantissent la comparabilité).
- Auto-invocation skills custom user-level non fiable : query mot-pour-mot ne garantit pas le trigger → slash-command est le bon primitif si usage user-driven (candidat lessons-inbox, non encore promu).

Pattern "spec-skip" (promu Global Do NOT via /immunize, commit 2f2c5f3) :
- 3 occurrences observées : Sonnet ×2 sur /claude-md, Opus ×1 sur /prd.
- Comportement : le modèle zappe les étapes opérationnelles formulées en typographie secondaire (parenthèse, mention de second plan).
- Mitigation intégrée dans ~/.claude/CLAUDE.md : toujours formuler les étapes opérationnelles en paragraphe propre avec numérotation ou gras.

Branches ouvertes résiduelles (passives, aucune action immédiate requise) :
- 2 lessons restent en inbox (auto-invocation skills non fiable, doctrine "migrer par nécessité" bidirectionnelle) — à surveiller pour future promotion via /immunize.
- Test terrain hook SessionStart toujours non-réalisé — attente staleness >24h, passif.
- Phase 6h différée : factorisation cruft-reader partagé /prd + /claude-md (YAGNI tant que duplication minime).
- Piste C Phase 2 : /claude-md détecter marqueur Cookiecutter (maintenu, non prioritaire).
- Migration dispatchers vers skill Mode C (reporté indéfiniment).

---

### shanraisshan-exploration [ARCHIVÉ - réorienté 2026-04-20]

Parcours linéaire interrompu au module 4/8 (socle acquis : CLAUDE.md, hooks, commands, skills, subagents, orchestration, agent memory).

Réorientation : le repo s'utilise désormais comme référence ciblée pendant l'audit dotfiles, pas comme parcours linéaire. Les modules 5-8 restent disponibles pour consultation au cas par cas si un besoin émerge.

Modules absorbés :
- Module 0 : Audit setup
- Module 1 : Commands avancées
- Module 2 : Skills & Subagents (hands-on tech-watch-scorer)
- Module 3 : Orchestration Command → Agent → Skill
- Module 4 : Agent Memory (hands-on learning-tracker)

---

### mcp-server-mastery [ARCHIVÉ - réorienté 2026-04-20]

Roadmap interrompue après modules 1.1–1.4. Phase sécurité (module 2.1) non démarrée et retirée du périmètre.

Leçon retenue et intégrée : sobriété MCP (n'activer qu'au besoin réel, pas par exploration systématique).

Réorientation : les MCP servers s'étudient désormais à la demande — quand un besoin précis émerge. La conception d'un MCP custom reste hors-périmètre pour l'instant (pratique actuelle trop restreinte).

---

### claude-code-sandboxing [ARCHIVÉ - réorienté 2026-04-20]

Workshop TP0-TP8 jamais démarré (0 session en 50 jours).

Motivation initiale identifiée : curiosité + souci de sécurité général, pas un besoin concret actionnable.

Réorientation : sujet déplacé en veille passive. Conscience que le sandboxing est une piste sécurité existante ; sera approfondi si un besoin précis émerge (incident, changement d'environnement, question sécurité ciblée).

Acquis préservé : la piste est identifiée, pas besoin de "découvrir" son existence à nouveau.
