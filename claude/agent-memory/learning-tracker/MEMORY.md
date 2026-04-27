## Méta
- Première session : 2026-03-07
- Sessions totales : 7
- Sujets actifs : 1 | Complétés : 0 | Archivés : 4

## Sujets

### methodology-trial [ACTIF]
- Premier contact : 2026-04-27 | Dernier contact : 2026-04-27
- Sessions : 2 | Vélocité : ~2/sem (2 sessions sur 1 jour, semaine 1)
- Statut : Étape 1 PRD validée (memory-grep/PRD.md — 8 critères, 4 phases, 5 risques). /immunize exécuté côté dotfiles (2 règles promues, commit d8496b7). /claude-md sur memory-grep reporté. 3 entrées inbox en attente de promotion.
- Prochaine étape : /claude-md sur memory-grep + Phase 1a implémentation (session suivante). Puis choisir projet Étape 2.
- Branches ouvertes :
  - Étape 1 — CLI : `memory-grep` — PRD VALIDE ; /claude-md + Phase 1a implémentation à faire
  - Étape 2 — Ingestion API : choisir parmi `gh-prs-tracker`, `anthropic-models-watcher`, `dataset-gouv-fetcher`
  - Étape 3 — Webscraping : `hn-watch` ou `arxiv-skim`
  - Étape 4 (optionnelle) — Stack hors-Python pour stresser la généralisabilité
  - Inbox dotfiles : 3 entrées en attente (auto-invocation skills, doctrine bidirectionnelle, stories paraphrase)
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
