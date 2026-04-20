## Dernière mise à jour
Date : 2026-04-20 19:15
Session : 191052df-cec4-49b9-b0f2-9080c5bdbc22

## Tâches complétées
- Phase 6.0 — README rewrites : claude/README.md réécrit (3 couches → 9 composants,
  principes de chargement, doctrine commands/skills/agents) + README.md racine aligné
  (tableau complet, hooks multi-événements) (commit c34c941)
- Phase 6b — Migration /prd command → skill : skills/prd/SKILL.md créé,
  commands/prd.md supprimé, install.sh mis à jour (commit 3cdb948)
- Phase 6c — Migration /claude-md command → skill : skills/claude-md/SKILL.md créé,
  !`cat CLAUDE.md` remplacé par Step 0 explicite (Read tool), install.sh mis à jour
  (commit 889dcaf)
- Phase 6d — Enrichissement skill prd : pré-flight .cruft.json détecte stack Cruft,
  allège Phase 8 (confirmation rapide) et Phase 10 (architecture pré-proposée),
  principe directeur "ne demander que ce qui mérite délibération" (commit 377ef10)

## En cours
- Rien (Phase 6 partielle close, pause avant session dédiée feature branch)

## Prochaines étapes
1. Session dédiée + feature branch `feat/claude-md-instance-aware` :
   - 6e : enrichir skill claude-md avec pré-flight symétrique (.cruft.json + arbo + PRD.md)
     — workflow instance → /prd → /claude-md validé
     — philosophie β : interview allégée (~4-5 phases sur ce qui reste indéterminé)
     — principe : "Cookiecutter a déjà demandé ce qui est décidable"
   - 6f : test E2E sur instance Cruft réelle (cruft create + workflow complet)
   - 6g : factorisation éventuelle ressource partagée cruft-reader (optionnel)
2. Mise à jour README.md racine et claude/README.md (skills maintenant 5 au lieu de 3)
3. Mise à jour AUDIT_PROGRESS.md Phase 6 (marquée ✅ quand 6e-6f clôturés)

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- Phase 6 élargie : /prd et /claude-md migrés en skills (scénario 3 — enrichissement
  concret dès maintenant, pas juste migration mécanique)
- Doctrine réaffirmée : "migrer par nécessité" — ces deux cas justifient la migration
  par complexité croissante (pré-flight, ressources multi-fichiers)
- Workflow projet validé : instance Cruft → /prd → /claude-md (une seule session Claude,
  contexte PRD chaud pour génération CLAUDE.md)
- Philosophie /claude-md in-project : β (interview allégée ~4-5 phases sur ce qui
  reste indéterminable depuis la stack)
- Référence AUDIT_PROGRESS.md retirée de claude/README.md (lien mort à terme)
- Session parallèle indépendante : OK pour développer une feature sans rapport sur
  feature branch séparée — contextes Claude et git isolés
- Push origin/main : à faire en fin de cette session

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-20 17:30
Session : e24c32e5-77f0-426c-939c-522bff3038b6

## Tâches complétées
- Audit learning-tracker.md (frontmatter) : memory: user retiré (inerte), "Task tool" → "Agent tool", chemin MEMORY.md explicité (commit 9727c82)
- Doctrine anti-croissance mémoire : format 3 lignes ARCHIVÉS, seuil 150 → 100 lignes, completed-topics.md créé (commit 7d17f8c)
- Audit scripts/ : fetch-sources.py (import os + docstrings Google), extract-json.py supprimé (code mort, 0 octet) (commit 009172a)
- Audit agent-memory/README.md : convention chemin, seuil per-subagent, tech-watch-scorer catalogué stateless (commit 59a24e0)
- Points 5/6 tranchés : 7/7 commands restent commands (grille à 3 questions validée sur tout le repo, aucun cas ambigu)
- Fiche pédagogique synthèse : fiche-grille-commands-vs-skills.md produite
- AUDIT_PROGRESS.md : Phase 5 marquée ✅, verdict 7/7 documenté
- Push de 7 commits Phase 5 vers origin/main (05785c5..59a24e0)

## En cours
- Rien (Phase 5 close, pause avant Phase 6)

## Prochaines étapes
1. Test terrain hook SessionStart (passif — attendre staleness dotfiles-audit > 24h)
2. Phase 6 — Meta & cohérence :
   a. claude/README.md : réécriture narratif "3 couches" → architecture réelle 8+ composants
   b. README.md racine : alignement post-audit
   c. install.sh : vérifier cohérence avec livrables Phase 5 (hook SessionStart, symlinks)

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- memory: user dans frontmatter subagent = code mort → retirer (même classe que permissionMode)
- Format strict ARCHIVÉS learning-tracker : 3 lignes max dans MEMORY.md, narratif → completed-topics.md
- Seuil curation MEMORY.md : 150 → 100 lignes (alerte précoce au régime normal d'un tracker actif)
- 7/7 commands du repo restent commands : doctrine "migrer par nécessité, pas par conformité" validée sur tout le périmètre
- learning-tracker (dispatcher) : reste command — geste rituel, Agent tool assure déjà la séparation de contexte
- tech-watch (dispatcher) : reste command — Step 4 rapport DOIT rester en contexte principal
- Push origin/main : effectué en fin de Phase 5

## Blocages
Aucun
