## Méta
- Première session : 2026-03-07
- Sessions totales : 4
- Sujets actifs : 1 | Complétés : 0 | Archivés : 3

## Sujets

### dotfiles-audit [ACTIF]
- Description : Audit structuré de ~/dotfiles/claude/ (8 phases prévues) contre les best-practices Claude Code 2026.
- Statut : Phase 6 (Meta & cohérence) terminée ✅ — Phase 7 (Exécution consolidée & rétrospective) à démarrer.
- Sessions : ~7 (depuis 2026-04-18)
- Premier contact : 2026-04-18
- Dernier contact : 2026-04-27
- Vélocité : ~3.5 sessions/semaine
- Prochaine étape : Phase 7 — vérifications finales, retrait ou conversion de AUDIT_PROGRESS.md en note rétrospective.
- Branches ouvertes :
  - Pattern "Sonnet améliore l'UX par-dessus la spec" (x2 cette session) : substitution libre/templatée, glissement territoire — mitigation efficace via split + cadenas verbatim. Candidat lessons-inbox (/immunize).
  - Doctrine "migrer par nécessité" validée bidirectionnellement (commands→skills→commands légitime). Candidat lessons-inbox.
  - Auto-invocation skills custom user-level non fiable : query mot-pour-mot ne garantit pas le trigger → slash-command est le bon primitif si usage user-driven. Candidat lessons-inbox.
  - Protocole A→B→A pertinent en mode command (justification : CWD propre + transcription figée).
  - Phase 6h différée : factorisation cruft-reader partagé /prd + /claude-md (YAGNI tant que duplication minime).
  - Test terrain hook SessionStart toujours non-réalisé (compteur réinitialisé par cette session).
  - Piste C Phase 2 : faire évoluer /claude-md pour détecter marqueur Cookiecutter (maintenu).
  - Point 5/6 Phase 3-4 : migration éventuelle dispatchers vers skill Mode C (toujours reporté).

### shanraisshan-exploration [ARCHIVÉ 2026-04-20 - réorienté]
- Acquis : socle Claude Code couvert (modules 0-4/8). Repo utilisé désormais comme référence ciblée, pas parcours linéaire.
- Détail : voir `completed-topics.md`.

### mcp-server-mastery [ARCHIVÉ 2026-04-20 - réorienté]
- Acquis : sobriété MCP intégrée (n'activer qu'au besoin réel). Étude désormais à la demande, conception MCP custom hors-périmètre.
- Détail : voir `completed-topics.md`.

### claude-code-sandboxing [ARCHIVÉ 2026-04-20 - réorienté]
- Acquis : piste sécurité identifiée, veille passive. Réactivation si besoin précis (incident, question ciblée).
- Détail : voir `completed-topics.md`.
