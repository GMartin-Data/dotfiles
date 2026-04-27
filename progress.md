## Dernière mise à jour
Date : 2026-04-27 14:15
Session : 9ef4eaf8-7f35-4453-9fc6-a48420a38dad

## Tâches complétées
- Refonte corpus evals /claude-md (doctrine command post-pivot) :
  - claude-md.eval.json : 3 evals (step0_gate + 2 × preflight) remplaçant
    les 3 evals should_trigger/should_not_trigger/ambiguous de l'époque skill
  - README.md : doctrine recentrée sur comportement post-invocation
    (pré-flight, Step 0, gates, allègement), protocole A→B→A simplifié
  - setup-eval-cwd.sh : IDs renommés, cas obsolète trigger-negative retiré
- Bootstrap corpus evals /prd (symétrique) :
  - prd.eval.json : 3 evals (strict_mode_gate + 2 × preflight)
  - README.md : doctrine miroir /claude-md, spécificités /prd
    (strict-mode gate, model: opus, 13 phases, 3 blocs de validation)
  - setup-eval-cwd.sh : 3 fixtures (PRD préexistant / Cruft fraîche / CWD vide)
- Campagne A→B→A vague 1 (gates) :
  - step0-existing-claude-md : ❌ run 1 (gate contournée sur CLAUDE.md vide)
    → fix Step 0 "vide ou non" → ✅ run 2 5/5
  - strict-mode-existing-prd : ✅ run 1 5/5
- Campagne A→B→A vague 2 (/claude-md préflight) :
  - preflight-cruft-instance run 1 : ⚠️ 4/5 (Bloc 2 dérive Phases 5+7)
    → fix split Bloc 1/Bloc 2 + cadenas verbatim → ✅ run 2 4/5
  - run 2 : ⚠️ 5/5 mais réflexe PRD-first manquant + glissement Phase 1
    → fix réflexe PRD-first (propose /prd si PRD absent)
  - run 3 : ⚠️ 5/6 glissement Phase 1 (question ouverte cadrage produit)
    → décision : gate conditionnelle Cruft+!PRD → arrêt (option B retenue)
    → reformulation invariant 6 (territoire CLAUDE.md vs territoire PRD)
  - preflight-cruft-without-prd : ✅ run 1 5/5
  - preflight-cruft-with-prd : ✅ run 1 6/6
- Campagne A→B→A vague 3 (/prd préflight) :
  - preflight-cruft-instance : ✅ run 1 5/5
  - no-preflight-empty-cwd : ✅ run 1 5/5
- 4 fixes doctrinaux appliqués à claude-md.md + instance-aware-flow.md
  (voir section Décisions prises)

## En cours
- Rien (campagne de test close, prêt pour merge)

## Prochaines étapes
1. Merge feat/claude-md-instance-aware → main + push
2. Mise à jour README.md racine et claude/README.md
   (skills : 3 restantes ; commands : prd et claude-md de retour)
3. AUDIT_PROGRESS.md Phase 6 → ✅ quand merge effectué
4. Commit séparé sur main : settings.json (effortLevel + cosmétique)
5. Phase 6g (reportée) : evals/prd/ lors d'une session dédiée /prd
   → déjà bootstrapé cette session, à tester en A→B→A dédié

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- Split Bloc 1 / Bloc 2 dans le pré-flight de claude-md.md :
  Bloc 1 = résumé libre (enrichissement pyproject/pre-commit autorisé),
  Bloc 2 = annonce d'allègement templatée verbatim (Phases 1,2,8,11)
  Raison : éviter que Sonnet substitue ses propres phases (5, 7) au lieu
  de pointer vers reference/instance-aware-flow.md
- Gate conditionnelle Cruft+!PRD → arrêt dans /claude-md :
  Si .cruft.json présent ET PRD.md absent → message d'arrêt "workflow
  Cruft → /prd → /claude-md". Si pas de Cruft → poursuit (cas dotfiles,
  scripts, projets existants). Symétrie doctrinale avec /prd (qui protège
  son output PRD.md).
- /prd n'a pas besoin de gate conditionnelle supplémentaire :
  La seule gate nécessaire est déjà existante (PRD.md déjà présent → arrêt).
  Cas Cruft sans PRD = scenario nominal de /prd (c'est précisément pourquoi
  on l'invoque).
- Frontière /claude-md vs /prd formalisée dans instance-aware-flow.md :
  Phase 1 = territoire CLAUDE.md (nom, structure) ; problème/utilisateurs/
  valeur = territoire /prd. Si PRD.md présent (gate passée), le cadrage
  produit est déjà figé — Phase 1 = checkpoint, pas ré-élicitation.
- Reformulation invariant 6 eval claude-md :
  "checkpoint pur" → "territoire CLAUDE.md (nom/structure) sans glisser
  sur territoire PRD (problème, utilisateurs, valeur)"

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-27 11:35
Session : 4eb7be93-c5d4-4178-93b4-a61f28867543

## Tâches complétées
- Campagne de test Phase 6f (protocole A→B→A) — 3 evals exécutées :
  - trigger-negative : ✅ 3/3 (negative space efficace, comportement nominal)
  - trigger-edge : 🟡 avant shims (skill non invoquée) → 🟡 après shims
    (skill invoquée via Skill tool, gap résiduel Step 0 sur CLAUDE.md vide)
  - trigger-positive : 🔴 auto-invocation toujours défaillante même avec
    query mot-pour-mot dans la description
- Diagnostic R0 — sentinelle instrumentée (non committée) : skill non
  déclenchée automatiquement dans les 2 cas critiques
- Création shims commands/claude-md.md + commands/prd.md → slash-commands
  /claude-md et /prd restaurées et fonctionnelles en session B
- Pivot doctrinal — retour skills → commands pour prd et claude-md :
  auto-invocation non désirée (usage exclusivement user-driven), progressive
  disclosure préservable en command, doctrine "migrer par nécessité" réaffirmée
- Migration complète (commit b3d7088) :
  skills/claude-md/ → commands/claude-md.md + commands/claude-md/{reference,evals}/
  skills/prd/SKILL.md → commands/prd.md
  install.sh mis à jour, symlinks skills périmés supprimés
- Corrections de cohérence post-migration : "SKILL.md" → "claude-md.md"
  dans reference/, "via la skill /progress" → "via `/progress`"
- Encart de dépréciation ajouté sur evals/README.md (doctrine EDD à refondre
  pour le modèle command — session dédiée prévue)
- Revert sentinelle diagnostique (non committé — Option B, sans trace git)

## En cours
- Rien (migration terminée, wrap-up en cours)

## Prochaines étapes
1. Session fraîche (après /clear) : tester /claude-md en session B vierge
   sur un CWD d'eval pour confirmer comportement post-invocation nominal
2. Refonte evals/README.md — nouvelle doctrine pour command :
   tester le comportement post-invocation (pré-flight, Step 0, gates,
   skip criteria), pas le déclenchement automatique
   → réécrire claude-md.eval.json en scénarios de comportement
3. Après validation comportement : merge feat/claude-md-instance-aware → main + push
4. Mise à jour README.md racine et claude/README.md
   (skills : 3 restantes ; commands : prd et claude-md de retour)
5. AUDIT_PROGRESS.md Phase 6 → ✅ quand merge effectué
6. Phase 6g (reportée) : evals/prd/ lors d'une session dédiée /prd

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- Auto-invocation des skills custom user-level = non fiable en pratique :
  même une query mot-pour-mot dans la description ne garantit pas le trigger
- /prd et /claude-md = rituels utilisateur exclusivement → slash-commands
  est le bon primitif (pas skills)
- Progressive disclosure et modularité restent disponibles en command
  (sous-dossier commands/claude-md/ avec reference/ et evals/)
- model: opus conservé pour /prd (recommandation Boris Cherny : cadrage
  stratégique mérite le modèle le plus capable)
- Shims minces supprimés : le corps complet vit directement dans commands/*.md
- settings.json non-committé : effortLevel + cosmétique, indépendant — commit
  séparé à faire sur main après merge
- evals/README.md conservé comme matériel legacy à refondre (B2) — pas jeté

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-22 17:00
Session : 0ac5cab2-512c-4df6-95da-4a99336f50b4

## Tâches complétées
- Phase 6e — Enrichissement skill claude-md instance-aware :
  pré-flight symétrique à /prd (détecte .cruft.json + arbo + PRD.md),
  progressive disclosure (3 reference files : instance-aware-flow.md,
  output-format.md, validation-checklist.md), SKILL.md allégé 405 → 231
  lignes (-43 %), traduit intégralement FR, Phase 11 dédupliquée
  (commit bb5ceef, branche feat/claude-md-instance-aware)
- Audit Context7 appliqué : best practices Anthropic officielles
  (token budget, progressive disclosure, frontmatter spec) +
  shanraisshan/claude-code-best-practice (14 champs frontmatter, trigger
  accuracy, évaluation lifecycle)
- Frontmatters enrichis symétriquement sur claude-md et prd :
  user-invocable, allowed-tools, paths, model (commit bb5ceef)
- Bootstrap eval suite claude-md : doctrine EDD, 3 queries (should_trigger /
  should_not_trigger / ambiguous_edge_case), setup-eval-cwd.sh
  (commit aa95ac0)
- Protocole A→B→A formalisé et gravé dans evals/README.md (rôles,
  frictions connues, séquence complète)
- AUDIT_PROGRESS.md mis à jour (Phase 6e ✅, 6f/6g/6h documentés)
- Mémoire persistée : project_cruft_template_path.md (pitfall -v2 suffix
  obligatoire : ~/python-project-template-v2, sans -v2 = ancienne tentative)

## En cours
- Rien (Phase 6e close, prête pour session de test)

## Prochaines étapes

### Session A (reprise via /catchup dans ~/dotfiles)
1. Relire evals/README.md section "Rôles & Protocole" pour se remettre
   dans le contexte du protocole de test
2. Lancer setup-eval-cwd.sh pour les 3 evals :
   ```
   cd ~/dotfiles/claude/skills/claude-md/evals
   ./setup-eval-cwd.sh trigger-positive-cruft-instance
   ./setup-eval-cwd.sh trigger-negative-user-global-conventions
   ./setup-eval-cwd.sh trigger-edge-existing-claude-md
   ```
   → note les 3 chemins /tmp/ retournés
3. Communiquer les 3 chemins pour lancer les sessions B

### Sessions B (3 × contexte vierge, une par eval)
Pour chaque eval-id :
1. cd <chemin /tmp/claude-md-eval-<id>-*/> && claude (nouvelle session)
2. Coller la query depuis evals/claude-md.eval.json (champ "query")
3. Laisser B répondre naturellement — ne pas guider ni annoncer qu'on teste
4. Couper dès que les 30 premières secondes d'interaction sont observées
   (pré-flight, annonce d'allègement, première question) — inutile de dérouler
   l'interview complète
5. Copier-coller l'intégralité de la transcription

### Retour session A (jugement)
1. Coller les transcriptions dans A une par une (pas toutes d'un coup)
2. A coche les expected_behavior (✅ / ⚠️ / ❌) pour chaque transcription
3. A produit le rapport matrice consolidé
4. Statuer ensemble sur les refinements SKILL.md si gaps identifiés

### Après la campagne de test (selon résultats)
- Si aucun gap → merge feat/claude-md-instance-aware → main, push
- Si gaps → session de refinement en mode A, re-test ciblé des items ❌/⚠️
- Phase 6g : bootstrap prd/evals/ (prochaine session touchant /prd)
- Phase 6h (optionnel) : cruft-reader partagé entre prd et claude-md
- Mise à jour README.md racine et claude/README.md (skills maintenant 5)
- AUDIT_PROGRESS.md Phase 6 → ✅ quand 6f validé

## Écarts vs PRD
Aucun (pas de PRD — AUDIT_PROGRESS.md fait office de feuille de route)

## Décisions prises
- Progressive disclosure appliquée à claude-md : SKILL.md = table des matières,
  contenu dense externalisé dans reference/ (doctrine officielle Anthropic)
- Contextes mutuellement exclusifs (Cruft détecté vs standard) dans fichiers
  séparés pour réduire le coût en tokens par invocation
- Frontmatter enrichi : allowed-tools inclut Bash pour claude-md (détection
  arbo) mais pas pour prd (Read seul suffisant) — différence intentionnelle
- Eval suite bootstrap : 3 queries minimum par doctrine YAGNI ; étoffage par
  nécessité observée (parallèle pytest-coverage), pas par anticipation
- Protocole test : A = auteur/juge (contexte projet), B = exécutant (CWD
  temporaire, contexte vierge), humain = canal de transmission. Isolation
  structurelle garantit absence de contamination (A ne voit B que via
  transcription capturée, jamais en live)
- setup-eval-cwd.sh force ~/python-project-template-v2 (avec -v2) comme
  valeur par défaut — protège contre le pitfall du template périmé
- settings.json non-commité : contient effortLevel: xhigh (réglé manuellement)
  + réordonnancement cosmétique de clés — indépendant de Phase 6e, à traiter
  séparément
- Phase 6f = test ciblé skill claude-md uniquement (pas un E2E complet du
  workflow Cruft → /prd → /claude-md — ça viendra après)

## Blocages
Aucun

---

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
