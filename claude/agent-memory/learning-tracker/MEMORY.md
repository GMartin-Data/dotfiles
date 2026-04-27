## Méta
- Première session : 2026-03-07
- Sessions totales : 6
- Sujets actifs : 1 | Complétés : 0 | Archivés : 4

## Sujets

### methodology-trial [ACTIF]
- Premier contact : 2026-04-27 | Dernier contact : 2026-04-27
- Sessions : 1 | Vélocité : n/a (démarrage)
- Statut : Campagne d'éprouvage de /prd + /claude-md + /progress + /immunize sur projets jouets multi-stacks. Session A en cours ; session B lance /prd sur memory-grep.
- Prochaine étape : Conclure Étape 1 (memory-grep CLI), capturer lessons dans tasks/lessons-inbox.md, /immunize.
- Branches ouvertes :
  - Étape 1 — CLI : `memory-grep` (~/projects/memory-grep, folder vide pur, mode no-preflight) — EN COURS
  - Étape 2 — Ingestion API : choisir parmi `gh-prs-tracker`, `anthropic-models-watcher`, `dataset-gouv-fetcher`
  - Étape 3 — Webscraping : `hn-watch` ou `arxiv-skim`
  - Étape 4 (optionnelle) — Stack hors-Python pour stresser la généralisabilité
- Objectifs précis :
  - /prd : qualité cadrage produit + allègement Cruft Phase 8/10
  - /progress : discipline checkpoint, lisibilité après /clear, robustesse "Écarts vs PRD"
  - /claude-md : pre-flight instance-aware, conventions techniques distinctes du cadrage produit
  - Workflow complet Cruft → /prd → /claude-md → cycle dev avec /progress + /immunize
- Capture : tasks/lessons-inbox.md au fil de l'eau. Sortie : lessons promues + raffinements specs /prd, /claude-md, /progress.

### dotfiles-audit [ARCHIVÉ 2026-04-27 - clôture]
- Acquis : audit ~/dotfiles/claude/ en 7 phases mené jusqu'au bout (architecture, mémoire, commands, hooks, skills, agents, méta+cohérence+consolidation). Doctrine "migrer par nécessité" bidirectionnelle validée. Pattern "spec-skip" promu Global Do NOT.
- Détail : voir `completed-topics.md`.

### shanraisshan-exploration [ARCHIVÉ 2026-04-20 - réorienté]
- Acquis : socle Claude Code couvert (modules 0-4/8). Repo utilisé désormais comme référence ciblée, pas parcours linéaire.
- Détail : voir `completed-topics.md`.

### mcp-server-mastery [ARCHIVÉ 2026-04-20 - réorienté]
- Acquis : sobriété MCP intégrée (n'activer qu'au besoin réel). Étude désormais à la demande, conception MCP custom hors-périmètre.
- Détail : voir `completed-topics.md`.

### claude-code-sandboxing [ARCHIVÉ 2026-04-20 - réorienté]
- Acquis : piste sécurité identifiée, veille passive. Réactivation si besoin précis (incident, question ciblée).
- Détail : voir `completed-topics.md`.
