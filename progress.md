## Dernière mise à jour
Date : 2026-04-28 (campagne methodology-trial — pivot candidats Étape 2+)
Session : (prolongation post-Étape 1, brainstorm candidats outils utiles écosystème Claude Code)

## Tâches complétées
- **Pivot stratégique campagne methodology-trial** : virage des candidats "stress-tests généralisabilité" vers candidats "outillage AI/Claude Code utile au quotidien", après triple gain identifié (connaissance écosystème + outillage perso + signal d'audit méthodologique sous charge réelle)
- **Modèle hybride 60/40 retenu** : 60% outils utiles haute densité signal, 40% stress-tests généralisabilité (préserver détection biais d'archétype)
- **Vérification écosystème Claude Code** via subagent `claude-code-guide` : confirmation existence `/insights` (slash command native d'audit usage local, postérieure au cutoff cutoff feb 2025) + `/usage` (alias `/stats`) + `/team-onboarding`. À utiliser plus tard quand corpus de sessions de build sera riche (post-Étape 2 minimum).
- **Décision de NE PAS lancer `/insights` maintenant** : signal trop pauvre actuellement (0 projet implémenté), risque de procrastination méthodologique déguisée
- **Brainstorm candidats Étape 2+ via interview ciblée** :
  - `gh-prs-tracker` ❌ écarté : pas de PRs réelles côté Greg (repos solo), outil mort-né
  - `ai-models-watcher` 🟡 reculé en candidat 4 : pertinent mais ROI modeste (changelogs Anthropic existent), fréquence d'usage faible
  - `prompt-companion` (NotebookLM helper) 🟡 reculé en candidat 3 : couvre pain points B (sélection prompts) + D (suivi qualité jamais fait), basé sur repo public `notebooklm-prompts` existant
  - `skill-eval-runner` ✅ **promu candidat 2** : pain point chiffré (~3h36/cycle 3 skills), proposal mature pré-existante (avril 2026), archétype radicalement opposé à memory-grep (subprocess + LLM-as-judge + parsing dynamique sortie `claude -p`), stress-test fort `/prd` `/claude-md` (5 trous explicites à combler)
- **Décision pivot candidat 2** : prompt-companion → skill-eval-runner

## En cours
- Rien (décision pivot prise, attente reprise Étape 1 implémentation memory-grep)

## Prochaines étapes
1. **Étape 1 finalisation memory-grep — non négociable avant tout pivot** : Phase 1a implémentation (uv init + structure memgrep/ + CLI Typer minimal + smoke test) — session ultérieure dédiée côté memory-grep. Anti-procrastination méthodologique.
2. (Optionnel) Phase 1b memory-grep (frontmatter parsing) si appétit
3. **Préparation pré-`/prd` skill-eval-runner** :
   - Première tâche d'observation : lancer `claude -p "drill me on Python list comprehensions"` (ou prompt équivalent dp-coach) → observer sortie brute → décider stratégie détection triggering. **Ne pas lancer `/prd` avant.**
   - Corriger pitch existant sur 3 points : (a) supprimer "Stack imposée" → référence CLAUDE.md memory-grep + délibération via `/prd` Phase 2, (b) corriger volumétrie ~3h36/cycle (pas ~9h, post-abandon track workflow-skills), (c) trancher Cruft vs uv init manuel
4. Étape 2 implémentation : `skill-eval-runner` (`/prd` → `/claude-md` → implémentation, audit A→B→A si appétit)
5. Étape 3 candidate : `prompt-companion` (NotebookLM helper) — archétype I/O réseau + état + clipboard + interview interactive, pain points B + D
6. Étape 4 candidate : `ai-models-watcher` ou pivot selon évolution
7. Étape 5 (recommandé) : projet stress-test généralisabilité hors-archétype Python CLI single-user (Go/Rust ou service longue durée API multi-component)
8. **Audit cross-CLAUDE.md** (action correctrice friction #1 du 2026-04-28) : grep `.claudeignore` + `gitignore.*aware` sur tous les CLAUDE.md du repo
9. **`/immunize` à la prochaine passe** : inbox 6 entrées (3 du 2026-04-27 + 3 du 2026-04-28) — surveiller récurrence

## Décisions prises
- **Pivot candidat 2 : prompt-companion → skill-eval-runner** justifié par :
  - Pain point chiffré récurrent (cycle validation skills, ~3h36/run de re-test) vs pain ressenti diffus (suivi qualité NotebookLM optionnel)
  - Cadrage plus mature (proposal pré-existante avec 5 trous explicites identifiés vs esquisse en session)
  - Archétype technique radicalement opposé à memory-grep (subprocess + LLM-as-judge + parsing dynamique vs scan filesystem statique read-only) → 6+ axes opposés
  - Stress-test plus fort `/prd` `/claude-md` (recursivité méta : eval-runner = outil qui teste des outils, expose Phases 4/7/10/11 sous angles inédits)
  - Synergie boucle vertueuse (outil qui améliore ta capacité à construire d'autres outils)
- **prompt-companion conservé candidat 3** : NotebookLM helper reste pertinent (pain point B + D réels, dogfooding 3-5×/semaine si NotebookLM utilisé), mais second à skill-eval-runner sur critères ROI mesuré + maturité cadrage
- **`gh-prs-tracker` définitivement abandonné** : signal pain point absent (Greg n'a pas de PRs en attente, repos solo), outil mort-né si construit
- **Modèle hybride 60/40** : éviter pivot 100% "outils Claude Code" qui créerait biais d'archétype invalidant la généralisabilité de la doctrine. Au moins 1 projet doit rester stress-test pur (non-Python ou multi-component longue durée).
- **Ordre d'exécution non négociable** : Phase 1a memory-grep AVANT toute préparation skill-eval-runner. Pas de "menu menu menu jamais cuisiner".

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-28 (campagne methodology-trial — Étape 1 CLAUDE.md ✅ + audit méthodologique)
Session : (catchup post-/clear, prolongée /claude-md memory-grep accompagné session A→B→A)

## Tâches complétées
- **Étape 1 — CLAUDE.md `memory-grep` produit** (côté ~/projects/memory-grep, hors dotfiles) :
  - 219 lignes, 13 sections (For AI — Read first / Session protocols / Filesystem Access, Stack, Project layout, Code conventions, Testing, Versioning, Languages, CI/CD, Out of scope, Constraints, Common commands)
  - Anglais strict (sauf zones FR explicites listées)
  - Commit baseline f3d4f38 `docs: initial CLAUDE.md and progress checkpoint` (CLAUDE.md + progress.md ensemble, PRD.md déjà committé séparément)
- **Audit méthodologique `/claude-md` accompagné en mode A→B→A** :
  - Fichier d'audit complet : `~/claude-audit-notes/methodology-trial-claude-md-memory-grep.md`
  - 11 phases d'interview auditées phase par phase
  - Bilan : 3 frictions critiques + 6 patterns positifs + 1 friction protocole méta
- **3 frictions critiques capturées dans `tasks/lessons-inbox.md`** :
  1. `.claudeignore` est une fiction + Read/Glob/Grep ne respectent pas `.gitignore` (CRITIQUE — implications cross-CLAUDE.md)
  2. Pré-flight `/claude-md` ne lit pas `MEMORY.md` projet/dotfiles (gap doctrinal)
  3. Conventions figées non appliquées comme contraintes dures cross-phases (2 occurrences même session)

## En cours
- Rien (Étape 1 entièrement close, pause avant Étape 2)

## Prochaines étapes
1. Étape 1 — finalisation memory-grep : Phase 1a implémentation (uv init + structure memgrep/ + CLI Typer minimal + smoke test) — session ultérieure dédiée côté memory-grep
2. **Audit cross-CLAUDE.md** : grep `.claudeignore` + `gitignore.*aware` sur tous les CLAUDE.md du repo dotfiles + projets externes connus (action correctrice friction #1)
3. **`/immunize` à la prochaine passe** : 3 nouvelles entrées 2026-04-28 dans inbox + 3 entrées 2026-04-27 préexistantes (6 total) — surveiller récurrence pour promotion vers `## Global Do NOT`. Pattern "conventions figées" déjà à 2 occurrences dans la même session = signal fort.
4. Étape 2 — Ingestion API : choisir parmi `gh-prs-tracker`, `anthropic-models-watcher`, `dataset-gouv-fetcher`
5. Étape 3 — Webscraping : `hn-watch` ou `arxiv-skim`
6. Étape 4 (optionnelle) — stack hors-Python pour stresser la généralisabilité

## Décisions prises
- **Protocole d'audit A→B→A pour `/claude-md`** validé sur memory-grep : 11 phases auditées en parallèle de l'exécution, friction protocole révélée (A invisible aux actions hors-interview de B → faux positifs possibles sur "inférences non sourcées"). Action correctrice : A demande confirmation avant flagger.
- **Capture audit dans `~/claude-audit-notes/`** (réutilisation convention existante pour audit dotfiles) plutôt que création d'un nouveau dossier
- **Granularité fine pour lessons-inbox** : 3 entrées séparées plutôt qu'une fusionnée — cohérent avec pratique précédente, `/immunize` fusionnera si pattern récurrent
- **Patterns positifs (6) NON ajoutés à lessons-inbox** : restent dans le fichier d'audit comme matériau pour enrichissement futur de la doctrine `/claude-md`. Lessons-inbox = règles à promouvoir, pas réservoir de bonnes pratiques.
- **Commit baseline avec scope vide** (`docs:` au lieu de `docs(claude-md):`) : refus du scope inventé, respect strict de la liste des 8 scopes figés en Phase 5.1 du CLAUDE.md memory-grep

## Blocages
Aucun

---

## Dernière mise à jour
Date : 2026-04-27 (campagne methodology-trial — Étape 1 PRD ✅ + /immunize)
Session : (catchup post-/clear, prolongée audit→methodology-trial)

## Tâches complétées
- Sujet learning-tracker `methodology-trial` ouvert (commit 78cced0) — campagne d'éprouvage de la méthodologie /prd + /claude-md + /progress + /immunize sur projets variés
- **Étape 1 — CLI `memory-grep` PRD validé** (côté ~/projects/memory-grep, hors dotfiles) :
  - PRD.md généré : 8 critères de succès, 4 phases d'implémentation (1a/1b/2/3), 5 risques, gestion d'erreurs 7 cas avec exit codes POSIX
  - Hypothèse case-sensitivity : tranchée smart-case post-PRD via `/prd` lui-même
  - Architecture Phase 10 correctement skippée (composant unique)
  - git init + /progress effectués côté memory-grep
- 7 frictions méthodologiques capturées dans tasks/lessons-inbox.md (commit 4351910)
- /immunize 2e passe (commit d8496b7) :
  - 2 nouvelles règles `## Global Do NOT` promues (groupes A "spec écrasée par UX" et B "cohérence transverse multi-phases")
  - 7 entrées inbox fusionnées en 2 règles
  - Inbox : 9 → 3 entrées | Global Do NOT : 1 → 3 règles | Cap : 3/20
- Subagent learning-tracker invoqué : `methodology-trial` sessions 1 → 2, méta sessions 6 → 7

## En cours
- Rien (campagne Étape 1 close, pause avant Étape 2)

## Prochaines étapes
1. Étape 1 — finalisation memory-grep : /claude-md projet + Phase 1a implémentation (squelette + scan + smoke test) — session ultérieure dédiée
2. Étape 2 — Ingestion API : choisir parmi `gh-prs-tracker`, `anthropic-models-watcher`, `dataset-gouv-fetcher`
3. Étape 3 — Webscraping : `hn-watch` ou `arxiv-skim`
4. Étape 4 (optionnelle) — stack hors-Python pour stresser la généralisabilité
5. Surveiller récurrence des 3 lessons inbox pour promotion future
6. Test terrain hook SessionStart (passif — staleness `methodology-trial`)

## Décisions prises
- Le pattern "le modèle écrase la doctrine quand l'UX appelle un raccourci" est promu en 3 règles distinctes du `## Global Do NOT` (typographie, découpage spec, cohérence transverse). Originellement issu de dotfiles + memory-grep, validé cross-contexte.
- Fusion préférée à la conservation d'entrées proches : 7 frictions distinctes regroupées en 2 règles synthétiques plutôt que promues séparément. Réduit le bruit cognitif au runtime.
- `claude/CLAUDE.md` (versionné dans dotfiles) **est** `~/.claude/CLAUDE.md` (symlink) : la doctrine /immunize "global vs projet" se collapse en une seule destination sur ce repo. Cas particulier du repo dotfiles lui-même.

## Blocages
Aucun

## Tâches complétées
- Merge `feat/claude-md-instance-aware` → main confirmé (commits aa95ac0 → 0ec5576)
- README.md racine et claude/README.md alignés avec le pattern command + companion folder (commit 0ec5576)
- settings.json committé séparément (commit 0fc02e5 : effortLevel xhigh, Opus default, theme dark-daltonized)
- /immunize exécuté sur tasks/lessons-inbox.md — aucune promotion (3 entrées 1× chacune, datées du même jour : règle 2+ occurrences non atteinte)
- MEMORY.md learning-tracker mis à jour (session 4, Phase 6 fermée, 4 branches ouvertes consignées) — commit 62145f2
- tasks/lessons-inbox.md committé (3 lessons Phase 6 datées 2026-04-27) — commit d8bffc7
- Push origin/main effectué (0ec5576..d8bffc7)
- **Phase 7 — Audit dotfiles clôturé** : AUDIT_PROGRESS.md supprimé (était gitignoré, action locale silencieuse). Trace utile déjà migrée : commits scopés, fiches `~/claude-audit-notes/`, lessons-inbox.md, MEMORY.md learning-tracker. Aucune mention "audit" dans les READMEs versionnés à nettoyer. Commit checkpoint 1e83e13.
- **Phase 6g — Campagne A→B→A `/prd` ✅** :
  - `setup-eval-cwd.sh` rendu non-interactif (`--no-input` + `--extra-context`) — commit 6c75347
  - 3 CWDs préparés, 3 sessions B exécutées sous Opus (model frontmatter)
  - Eval `strict-mode-existing-prd` : ✅ 5/5 (gate strict-mode propre)
  - Eval `preflight-cruft-instance` : ⚠️ 4.5/5 → ✅ après fix (étape "vérif arbo" tacite → spec durcie en 2 étapes numérotées explicites) — commit 8ba959d
  - Eval `no-preflight-empty-cwd` : ✅ 5/5 (cas négatif propre)
- Lesson `lessons-inbox.md` reformulée : pattern "modèle survole les étapes mal mises en relief" généralisé à modèle-agnostique (Sonnet ×2 + Opus ×1 = 3e occurrence) — commit 6369662

## En cours
- Rien — audit dotfiles entièrement clôturé (Phases 1-7 ✅, plus Phase 6g ✅)

## Prochaines étapes
1. Test terrain hook SessionStart (passif — staleness `dotfiles-audit`)
2. /immunize à la prochaine passe : promouvoir la lesson "spec-skip" (3e occurrence atteinte, règle 2+ largement franchie)
3. Mettre à jour le sujet learning-tracker `dotfiles-audit` → ARCHIVÉ à la prochaine ouverture

## Décisions prises
- Suppression AUDIT_PROGRESS.md plutôt que conversion en note rétrospective : redondant avec les fiches pédagogiques + commits + memory déjà en place
- Durcir `prd.md` immédiatement (pendant la campagne) plutôt que noter en TODO : contexte chaud, fix minimal, alignement avec `claude-md.md` déjà éprouvé
- Lesson `lessons-inbox.md` reformulée modèle-agnostique : l'observation Opus invalide l'attribution Sonnet-spécifique initiale ; le pattern vise la **typographie** de la spec (numérotation, paragraphes distincts), pas la taille du modèle
- Aucune promotion lessons-inbox cette passe — règle "2+ occurrences" respectée stricto sensu malgré pertinence forte
- Deux commits scopés séparés (learning-tracker / tasks) plutôt qu'un commit fourre-tout

## Blocages
Aucun

---

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
