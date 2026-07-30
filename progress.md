## Dernière mise à jour
Date : 2026-07-30 08:10
Session : bda2bbe2-b0f1-4228-8a84-db121a429757

## Tâches complétées

- **CHANTIER PRIORITAIRE clos — exécution ADR-0015 de bout en bout, 4 commits
  poussés** (`4866965..8f3ee14`) :
  1. **Corpus `claude/evals/immunize/` écrit failing d'abord** : 5 evals — les
     4 angles du checkpoint + `project-rule-format-100-accurate` (ajout validé
     en séance) — fixtures `meteo-pipeline` à piège vérifiable (hook réellement
     buggé, tripwire > 7 j). Rouge par inspection validé par l'humain.
  2. **Refonte `claude/commands/immunize.md` → vert par inspection 5/5** :
     tri-destination, porte 3 issues, format 100 %-accurate, mode ajout,
     éviction event-driven, dérivation matrice. Écart mineur assumé : les
     candidates globales restent dans l'inbox taguées `[CANDIDATE-GLOBAL —
     eval pending]` jusqu'au verdict (disposition non spécifiée par l'ADR).
  3. **Sync** (`1e06cf8`) : section « Cycle immunitaire » de la matrice (table
     6 emplacements + 2 flux), `tasks/insights-actions.md` créé + 2 fiches
     migrées, en-tête inbox aligné, mémoire protocole /insights amendée,
     routine remote `trig_01CMHnwqgZYkdspEHeY3KsFj` mise à jour (2
     substitutions vérifiées à la réponse API, prochain run 2026-08-26).
  4. **Run réel A→B→A** (`d117bf5`) : **PASS 11/11** — composite
     `triage-complet` 6/6 (grader Sonnet isolé 5/6 + E6 requalifié ✅ sur
     preuve harnais déterministe), `add-mode` 5/5 déterministe. Sessions B
     Opus/high via driver partagé, garde anti-écriture-globale scriptée,
     hash du CLAUDE.md global vérifié intact avant/après.
  5. **ADR-0015 → `Accepted`** (`8f3ee14`).
- **Leçons de harnais fixées et documentées** (README du corpus) : `Edit`
  ajouté aux `allowed-tools` de la command (surfacé au premier run) ;
  `--permission-mode acceptEdits` requis en `-p` pour une command qui écrit
  (jamais vu sur grill/prd : zéro écriture) ; règle de grading « invariant
  post-confirmation = frontières `result` du driver, jamais les tours user
  (non échoés dans le flux) ».
- **Purge des 4 CWDs `/tmp/immunize-eval-*` faite** (commande manuelle humaine).

## En cours

- Rien — ce checkpoint à committer puis push.

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis push.
2. **Cycle /insights 2026-08-26** : observation règle graduée P2 + métrique
   ratio méta/produit (P3) + les 3 constats de la revue TODO.md. L'issue de
   rappel route désormais les fiches vers `tasks/insights-actions.md`.
   **SD1** : cycle 2026-09.
3. Adjacent signalé non corrigé : l'overview ignore le cycle immunitaire —
   index des ADRs arrêté à 0014, `/immunize` absent du graphe des outils
   (l'était déjà avant la refonte).
4. Dormant nouveau (ADR-0015) : déclencheurs d'éviction D5 au prochain
   changement de tier/modèle par défaut (rejeu corpus claude-md avec/sans) ;
   première traversée réelle de la porte globale au premier candidat
   générique de l'inbox réelle.
5. Mineur reporté : diagrammes overview §1/§5 non re-validés au parseur.
6. (dormant) Corpus batch A mode « insertion » au premier replay ;
   `/code-review` sur dbt/Terraform au prochain diff réel ; eval « lot sous
   carte blanche » si observé en usage réel ; fixture PLAN pour le corpus
   /grill.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **ADR-0015 `Accepted`** — porte franchie (rouge → vert par inspection, run
  réel PASS 11/11) → `adr/0015`.
- Choix de portée session :
  - 5ᵉ eval hors des 4 angles du checkpoint (`project-rule-format-100-accurate`,
    couvre D2-projet + D3) — validée par l'humain avec le rouge.
  - Run réel sur **config réelle**, sans isolation `CLAUDE_CONFIG_DIR` (le
    corpus ne varie pas le payload) ; filets : garde anti-écriture-globale
    dans le script de tours, hash global avant/après, global tracké git.
  - `--permission-mode acceptEdits` préféré à `--dangerously-skip-permissions`
    (précédent claude-md, config isolée lui) : auto-acceptation limitée au
    CWD, une écriture globale hors CWD resterait bloquée.
  - Arbitrage anti-grader E6 : ⚠️ requalifié ✅ sur preuve mécanique du flux
    brut (tours user jamais échoés ; les 4 écritures entre les frontières
    `result` des tours 1 et 2) — précédent DN5/deferred-branch reconduit,
    preuve déterministe cette fois.
  - D5 (éviction) et D7a (gouvernance) non couverts par eval de session —
    assumé au README du corpus (déclencheurs inter-sessions / sync doc).
  - Add-mode jugé sans grader : invariants 100 % mécaniques (diff filesystem
    + transcription de 4 events).

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-29 09:22
Session : 81686209-0d5a-4710-8d12-cfb00c1ba57c

## Tâches complétées

- **Purge des 5 CWDs `/tmp/grill-eval-*` faite** (commande manuelle humaine —
  item du checkpoint précédent clos).
- **Audit de redondance des skills pédagogiques** (dp-coach / coach-pedagogique
  vs teach) rendu en avis seul, rien consigné (demande humaine explicite) :
  pas de redondance de contrat (frontières ADR-0007/0012 tiennent sur
  4 discriminants), une zone grise surveillable (tasks in-browser de teach vs
  drills exécutés), le vrai sujet est le non-usage — critère ADR-0007
  (« un outil sans utilisateur n'est pas protégé »), décision sur données
  d'usage le cas échéant.
- **Audit `/immunize` vs fireside chat Cat Wu / Thariq** (relecture WebFetch de
  la source déjà exploitée pour P1-P3, angle neuf) : 1 collision (inbox
  colonisée par les fiches `[INSIGHTS]`, la règle « unique > 7 j → archive »
  archiverait une fiche en attente de revue dès début août), 2 tensions de
  fond (accumulation sans preuve ni éviction ; format prohibition « 90% true »),
  1 destination manquante (incident → eval), 1 scorie (`argument-hint` mort).
- **CHANTIER refonte cycle immunitaire ouvert — interview ADR menée à terme** :
  8 décisions tranchées une-question-à-la-fois (décision 7 scindée 7a/7b),
  toutes sur recommandation. **ADR-0015 rédigé** en `Proposed`
  (`adr/0015-cycle-immunitaire-refonte-post-p1.md`, Extends ADR-0009) —
  non commité à ce stade.

## En cours

- **CHANTIER refonte `/immunize`** — ADR-0015 `Proposed` rédigé, porte de
  validation fixée (corpus rouge → refonte → vert → run réel A→B→A →
  `Accepted`). Étape suivante : corpus d'evals failing. Ce checkpoint et
  l'ADR à committer.

## Prochaines étapes

1. **Committer** : `docs(adr)` ADR-0015 (Proposed) puis `docs(progress)` ce
   checkpoint ; push.
2. **CHANTIER PRIORITAIRE (session fraîche) — exécution ADR-0015** dans
   l'ordre canonique : corpus `claude/evals/immunize/` **failing d'abord**
   (rouge contre la command actuelle : tri-destination absente, porte absente,
   mode ajout absent, collision [INSIGHTS]) → refonte
   `claude/commands/immunize.md` jusqu'au vert → sync (section « Cycle
   immunitaire » de la matrice ; création `tasks/insights-actions.md` +
   migration des 2 fiches ; en-tête `lessons-inbox.md` ; protocole /insights
   là où il route ses fiches — mémoire projet + routine) → run réel A→B→A →
   ADR-0015 `Accepted`.
3. **Cycle /insights 2026-08-26** : observation règle graduée P2 + métrique
   ratio méta/produit (P3) + les 3 constats de la revue TODO.md. **SD1** :
   cycle 2026-09.
4. Mineur reporté : diagrammes overview §1/§5 non re-validés au parseur.
5. (dormant) Corpus batch A mode « insertion » au premier replay ;
   `/code-review` sur dbt/Terraform au prochain diff réel ; eval « lot sous
   carte blanche » si observé en usage réel ; fixture PLAN pour le corpus
   /grill.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Refonte du cycle immunitaire → `adr/0015`** (Proposed — porte de
  validation : evals rouge→vert + run réel avant `Accepted`).
- Choix de portée session :
  - Audit skills pédagogiques : avis rendu sans consignation (demande humaine).
  - ADR-0015 rédigé directement au format maison après interview in-fil
    (8 décisions AskUserQuestion), sans re-parcours `/adr`.
  - Interview : une question par tour, décision 7 scindée 7a/7b (règle des
    séparations prescrites).

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-29 08:49
Session : 4c7b48e5-1f64-42c8-b0ae-5b06d763ac9a

## Tâches complétées

- **Chantier PRIORITAIRE clos — 5 evals bootstrap `/grill` exécutées en A→B→A**
  (`8fac46c`) : driver partagé, sessions B Opus/high automatisées (4 en
  parallèle), tours conditionnels scriptés, graders Sonnet isolés, verdict par
  expectation. **PASS 21/22** : preflight 4/4 · no-open-questions 5/5 ·
  input-explicit 4/4 · output-no-file-written 5/5 (+ vérif filesystem :
  `prd.md` byte-identique, zéro fichier créé dans les 5 CWDs) ·
  deferred-branch 3/4 + 1 ⚠️ requalifié ✅ avec réserve (arbitrage humain).
  L'anti-pattern « corpus jamais exécuté » (ADR-0009) est levé : les 6 evals
  du corpus /grill ont toutes tourné au réel.
- **Constat systémique documenté (README §Frictions)** : la carte blanche
  scriptée (« sur toute autre question : je valide ta recommandation ») induit
  une résolution **en lot** de toutes les branches restantes en un tour,
  contre `grill.md` « une question à la fois » — observé sur les 3 runs
  interactifs. Règle de grading associée : la cadence tour-par-tour du ledger
  n'est pas observable sous script.
- **2 fixtures versionnées** : `resolve-normally-interview-script.md` (3 evals)
  et `deferred-amorce-interview-script.md` ; renvois README à jour, état du
  corpus passé à « ✅ exécuté (6/6) ».
- **Adjacent overview §2 clos** (`43f045a`) : « PRD et CLAUDE.md ne se parlent
  pas » qualifié **en contenu** — indépendance de contenu ≠ d'élaboration, le
  flux PRD → CLAUDE.md du §1 ordonne l'élaboration sans écriture croisée.
- **README root — carte documentaire ajoutée** (`b9801fe`) : section
  « Documentation » de pointeurs (matrice, overview, karpathy, adr/, corpus
  d'evals + driver, tasks/) — le README ne couvrait que le bootstrap machine,
  la couche méthodologique n'avait aucun point d'entrée depuis la racine.
  Pointeurs seuls, zéro règle réénoncée (doctrine non-overlap). Large refresh
  écarté : il dupliquerait la carte documentaire de l'overview.

## En cours

- Rien — ce checkpoint à committer puis push. Backlog immédiatement
  actionnable : zéro (que du daté et du dormant).

## Prochaines étapes

1. **Cycle /insights 2026-08-26** : observation règle graduée P2 + métrique
   ratio méta/produit (P3) + les 3 constats de la revue TODO.md. **SD1** :
   cycle 2026-09.
2. **Purge manuelle** des 5 CWDs `/tmp/grill-eval-*-20260729-083019` (hook
   block-rm-rf, précédent reconduit).
3. Mineur reporté : diagrammes overview §1/§5 non re-validés au parseur (mmdc
   absent — téléchargement Chromium disproportionné).
4. (dormant) Corpus batch A mode « insertion » au premier replay ;
   `/code-review` sur dbt/Terraform au prochain diff réel ; eval « lot sous
   carte blanche » si observé en usage réel ; fixture PLAN pour le corpus
   /grill.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

Aucun ADR cette session (exécution d'evals et sync doc). Choix de portée
session :

- **Arbitrage E1 `deferred-branch-in-output`** : ⚠️ du grader requalifié ✅
  avec réserve — le reproche (rafraîchissement groupé du ledger) est exact
  mais induit par le harnais (carte blanche scriptée), pas observable
  autrement en mode scripté. Option « documenter sans rejouer » validée par
  l'humain ; rejeu écarté car toute clause conditionnelle générique
  réinviterait le lot.
- **Scripts de tours mutualisés** (1 partagé par 3 evals + 1 amorce DEFERRED)
  plutôt qu'un script par eval — les tours sont conditionnels, seule l'amorce
  varie.
- **4 sessions B en parallèle** (background) après sanity check séquentiel du
  preflight — campagne bouclée en ~15 min sans incident.
- **README : section pointeurs plutôt que large refresh** — un README qui
  re-raconte le système recréerait le drift que la matrice combat ; son
  périmètre reste le bootstrap machine.
- **Hook block-rm-rf respecté** : purge des fixtures laissée à l'humain.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-29 08:13
Session : c6e8602d-da20-474c-8f22-76a163636eec

## Tâches complétées

- **4 chantiers clos, 4 commits poussés** (`971f43e..d569d8e`) :
  1. **Deny rules `settings.json` fixées** (`971f43e`, PRIORITAIRE du checkpoint
     précédent) : règles `Write(**/.env*)` invalides supprimées — les règles
     `Edit` existantes couvrent tous les outils d'édition. Vérifié : zéro
     warning au re-run `claude -p`.
  2. **`protect_env.py` — faux positif Bash corrigé** (`7001e83`, test-first
     complet) : la branche Bash ne bloque plus que si le token résolu (chemin
     complet capturé, `~` expansé, relatif au `cwd` du hook) pointe vers un
     fichier **existant** — une mention en prose (message de commit) n'est
     plus une référence. Rouge validé par l'humain, vert 12/12 (tests e2e
     stdin JSON → exit code, unitaires migrés), preuve live : le commit du fix
     lui-même contenait 4 fois le littéral bloqué la veille. Trous résiduels
     documentés (globs, expansion de variables, `cd` en milieu de commande).
  3. **Drift overview §1/§5 résolu** (`5502b59`) : prose et diagrammes alignés
     sur la matrice Phase 0 post-volet A (indépendance de contenu ≠
     d'élaboration, flux PRD → CLAUDE.md, ordre recommandé / imposé sur
     Cruft / libre hors produit) ; fausse flèche `/claude-md` → `/grill`
     du §5 corrigée au passage (grill ne lit jamais CLAUDE.md).
  4. **`setup-eval-cwd.sh` claude-md TTY-free** (`d569d8e`) : `--no-input`
     sur `cruft create` — le contournement `yes '' |` reconduit 2 sessions
     n'est plus nécessaire. Rouge/vert vérifiés stdin fermé, fixture conforme.
- **Fixtures `/tmp` purgées** (commande manuelle humaine ; les 11 anciennes
  avaient déjà disparu au reboot). Item clos.

## En cours

- Rien — ce checkpoint à committer puis push.

## Prochaines étapes

1. ~~Committer ce checkpoint~~ **Fait** (`250688f`) ; post-checkpoint : revue
   des déclencheurs TODO.md (`84b2371`, 3 constats routés au cycle /insights)
   et cet amendement.
2. **PRIORITAIRE (session fraîche) — exécuter les 5 evals bootstrap `/grill`
   en A→B→A** via le driver partagé (`claude/evals/drive-session.py`) :
   `preflight-artifact-absent`, `no-open-questions-section`,
   `deferred-branch-in-output`, `input-explicit-arg-over-fallback`,
   `output-no-file-written`. Sessions B pilotées, graders Sonnet isolés,
   verdict par expectation — protocole ADR-0009, précédent immédiat :
   `spike-routing` PASS 6/6 avec le même outillage. Décision 2026-07-29
   (post-checkpoint) : déclencheur dormant levé à la main — coût d'exécution
   effondré depuis la généralisation du driver, dernier corpus du parc jamais
   passé au réel (anti-pattern « corpus jamais exécuté », ADR-0009).
3. **Cycle /insights 2026-08-26** : observation règle graduée P2 + métrique
   ratio méta/produit (P3) + les 3 constats de la revue TODO.md. **SD1** :
   cycle 2026-09.
4. Adjacent signalé non corrigé : overview §2 « PRD et CLAUDE.md ne se
   parlent pas » — vrai en contenu, ambigu depuis que le §1 affiche le flux
   d'élaboration ; nuance « en contenu » candidate. Mineur : diagrammes §1/§5
   non re-validés au parseur (mmdc absent) — aperçu VS Code suffisant.
5. (dormant) Corpus batch A mode « insertion » au premier replay ;
   `/code-review` sur dbt/Terraform au prochain diff réel.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

Aucun ADR cette session (fixes et sync doc — pas de décision nouvelle durable).
Choix de portée session :

- **Sémantique `protect_env.py`** : bloquer sur existence réelle du fichier,
  pas sur la chaîne — garde-fou contre l'accès par inadvertance, pas sandbox ;
  trous résiduels assumés et documentés dans la docstring. Alternative écartée :
  exemption des contextes quotés (bypass réel via `bash -c`).
- **Tests migrés unitaire → e2e** (stdin JSON → exit code) : c'est le `cwd`
  du contrat hook qui porte la nouvelle sémantique.
- **Diagrammes non re-validés au parseur** : npx mermaid-cli = téléchargement
  Chromium disproportionné pour 2 retouches à constructions déjà présentes.
- **Hook block-rm-rf respecté** : purge des fixtures laissée à l'humain
  (précédent reconduit), y compris celles créées par la vérification du jour.
- **Adjacent §2 signalé sans correction** (Surgical Changes).

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-29 06:35
Session : 7fa1c297-cece-4de5-b36b-0999cb20ba0a

## Tâches complétées

- **CHANTIER routage SPIKE clos end-to-end, 5 commits poussés**
  (`527f24f..6299dd6`) :
  1. **ADR-0014 délibéré en interview** (6 décisions, toutes tranchées sur
     recommandation) puis rédigé — Extends ADR-0003.
  2. **Eval failing test-first** (`spike-routing-indeliberable-branch`, classe
     `spike_routing`) : fixture à deux pièges (branche indélibérable + tension
     délibérable — test de discrimination), rouge validé par inspection, puis
     `grill.md` conformé (5 retouches) — vert par inspection 6/6.
  3. **Sync matrice** (3 points : Phase 0, Phase 1, ligne `/grill`) +
     **overview** (débouchés §1/§5, index 14 ADRs, ligne des structurants).
  4. **Run réel A→B→A automatisé PASS 6/6** : session B Opus/high pilotée par
     le driver, 9 tours scriptés en réponses conditionnelles (l'ordre des
     questions du grill n'est pas prescrit — fixture versionnée au corpus),
     grader Sonnet isolé, preuve verbatim par expectation. Porte franchie →
     ADR-0014 `Accepted`.
  5. **Driver généralisé au 2ᵉ usage** (doctrine d'émergence volet B) :
     `claude/evals/drive-session.py` partagé, renvois `/prd` et `/grill` à jour.

## En cours

- Rien — ce checkpoint à committer puis push.

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis push.
2. **PRIORITAIRE (demande humaine)** : fixer les deny rules de
   `~/.claude/settings.json` — `Write(**/.env)` et `Write(**/.env.*)` ne
   matchent aucun outil (warning à chaque `claude -p`) ; forme correcte :
   `Edit(**/.env)` / `Edit(**/.env.*)` (les règles Edit couvrent tous les
   outils d'édition de fichiers).
3. Adjacents signalés non corrigés : drift overview §1/§5 (« ordre libre »
   CLAUDE.md/PRD vs matrice post-volet A recommandé/imposé/libre — l'overview
   prédate le volet A) ; fixtures `/tmp` à purger (2 grill + 7 prd +
   2 claude-md, hook block-rm-rf) ; `setup-eval-cwd.sh` claude-md suppose un TTY.
4. **Cycle /insights 2026-08-26** : observation règle graduée P2 + métrique
   ratio méta/produit (P3). **SD1** : cycle 2026-09.
5. (dormant) 5 evals bootstrap `/grill` jamais exécutées — candidates au driver
   partagé au prochain besoin ; corpus batch A mode « insertion » au premier
   replay ; `/code-review` sur dbt/Terraform au prochain diff réel.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Routage SPIKE dans /grill → `adr/0014`** (Accepted en fin de session —
  porte de validation : run réel A→B→A PASS 6/6).
- Choix de portée session :
  - Interview ADR question par question avec recommandation argumentée
    (6 décisions, toutes tranchées par l'humain sur la recommandation).
  - Rouge prouvé par inspection textuelle (pas de session brûlée) ; vert par
    inspection accepté pour l'implémentation, mais run réel exigé avant
    passage en `Accepted`.
  - Tours de session B scriptés en **réponses conditionnelles** (pas
    positionnelles) — l'ordre des questions du grill dépend de son arbre ;
    amorce de neutralité encodée dans la fixture.
  - Généralisation du driver déclenchée par le 2ᵉ usage, conformément à la
    doctrine d'émergence posée au volet B.
  - Priorisation du fix deny rules = demande humaine explicite en fin de session.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-29 05:35
Session : b89022fd-8221-4140-b428-b5ff54364b92

## Tâches complétées

- **Chantier volet B mené de bout en bout, 4 commits poussés**
  (`2b028f3..93c8681`) :
  1. **ADR-0013 délibéré en interview** (6 décisions structurantes) : canvas
     PRD fermé de 11 sections. Satellite `conventions/prd.md` créé (2ᵉ après
     adr.md — critère de création atteint) ; matrice amendée en 3 points
     (cellule PRD → renvoi sans énumération, ligne `/prd`, index satellites).
  2. **Refonte `/prd`** (`72b6766`) : phases Objectifs et Contraintes créées
     (test à deux axes appliqué en séance, routage annoncé), pré-flight Cruft
     supprimé, Risques → récolte d'open questions, contrôle inter-phases et
     blocs de validation réécrits, bandeau « la convention fait foi ».
  3. **Corpus `/prd` conformé et rejoué** : 4 evals (3 réécrites + 1
     `output_quality` interview scriptée 15 tours). Rouge par inspection
     contre HEAD, **vert 4/4 PASS** (sessions B Opus/high automatisées,
     4 graders Sonnet isolés).
  4. **Moisson `/claude-md` recâblée** (`c8bbb0b`) : harvest = problème/
     objectifs/utilisateurs/contraintes (plus jamais stack/archi), ligne
     Bloc 2, branche « PRD sans Cruft » d'instance-aware-flow réécrite ;
     fixture avec-PRD promue au format canonique. **Rejeu scopé 2/2 PASS**
     (gate 7/7 ; avec-PRD 6/6 après arbitrage anti-grader : le ⚠️ comparait
     le Bloc 2 à instance-aware-flow.md au lieu du template de la command).
  5. **Clôture** (`93c8681`) : ADR-0013 → `Accepted`, overview §7.3-B statué
     « Résolu », index 13 ADRs, renvoi satellite.
- **Outillage durable** : `drive-session.py` (driver turn-based pour
  `claude -p` stream-json — le pipe naïf livre tous les tours en bloc, 2 faux
  FAIL instruits puis requalifiés) ; flags de référence documentés au README
  (pin `model:` + `effortLevel: xhigh` de session = 400 en mode `-p`).

## En cours

- Rien — ce checkpoint à committer puis push.

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis push.
2. **CHANTIER routage SPIKE** (ordonnancement tranché cette session : après
   volet B) : ADR (Extends ADR-0003) → eval failing → grill.md → sync matrice.
3. **Cycle /insights 2026-08-26** : observation règle graduée P2 + métrique
   ratio méta/produit (P3). **SD1** : cycle 2026-09.
4. Adjacents signalés non corrigés : fixtures `/tmp/prd-eval-*` (×7) et
   `/tmp/claude-md-eval-*` (×2 nouvelles) — purge manuelle ou reboot (hook
   block-rm-rf) ; `setup-eval-cwd.sh` de claude-md suppose toujours un TTY
   (contournement `yes '' |` reconduit).
5. (dormant) Corpus batch A mode « insertion » au premier replay ;
   `/code-review` sur dbt/Terraform au prochain diff réel.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Format PRD canonique → `adr/0013`** (Accepted en fin de session — porte
  de validation : 6/6 evals vertes sur les deux corpus).
- Choix de portée session :
  - Interview ADR menée question par question avec recommandation argumentée
    (6 décisions, toutes tranchées par l'humain).
  - **Test-first avant commit rappelé par l'humain** sur la refonte `/prd` —
    la proposition de committer sans rejeu contredisait la contrepartie de
    l'exemption direct-sur-main ; plan de test validé puis exécuté.
  - Rejeu `/claude-md` scopé à 2 evals (step0 en amont du diff, hors périmètre).
  - Arbitrage anti-grader avec-PRD (précédent DN5) : ⚠️ requalifié ✅, preuve
    verbatim ligne 85 amendée.
  - Driver versionné dans le corpus `/prd` seul — généralisation au 2ᵉ usage
    (doctrine d'émergence).

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-28 20:35
Session : 52367291-8782-4293-b092-37d446601828

## Tâches complétées

- **Incohérences 7.1 et 7.2 corrigées** (`bbd9333`, `9224c6f`) : matrice —
  « Décisions prises » de progress.md = journal de pointeurs vers les ADRs
  (exemption track léger ADR-0011 explicitée) ; cocher un acceptance criterion
  = état, éditer le contenu = révision (nouveau bloc « Frontières floues » +
  parenthèse Phase 2). Prompt `/progress` aligné (placeholder pointeurs).
  Overview §7.1/§7.2 statués « Résolu ».
- **7.3 instruit par inspection croisée dotfiles + template-v2.** Chronologie
  reconstituée : gate du 2026-04-27 (`a34871a`, délibérée, eval-pinnée,
  campagne 6/6) ; matrice du 2026-06-22 écrite sans la voir (« n'importe quel
  ordre ») ; ADR-0011 du 2026-06-25 crée un deadlock (déclaration track léger
  → CLAUDE.md → gate → PRD que le track léger rend optionnel). Le template ne
  prescrit aucun ordre (P7.5 : pas de CLAUDE.md seedé) — la gate est une
  doctrine dotfiles pure.
- **Volet A résolu et livré** (`10c2a94`) : gate track-léger aware (override
  sur confirmation explicite, consignation ADR-0011 dans le CLAUDE.md généré —
  la déclaration exigée) ; matrice Phase 0 réécrite avec la règle de fond
  (indépendance de **contenu** ≠ d'**élaboration**, flux unidirectionnel
  PRD → CLAUDE.md : recommandé / imposé sur Cruft / libre hors produit) ;
  champ fantôme « phases d'implémentation » retiré du pré-flight ;
  « périmètre v1 » → « cible » (le sweep ADR-0001 n'avait jamais atteint
  claude-md.md) ; instance-aware-flow.md mis en cohérence (2 retouches).
- **Rejeu d'evals scopé, verdict 2/2 PASS** : eval gate amendée PASS 7/7
  (2 tours, chemin override inclus) ; non-régression avec-PRD PASS 6/6
  (⚠️ initial du grader = troncature de transcription, tranché par un tour
  supplémentaire) ; rouge prouvé par inspection textuelle (pas de session
  brûlée). Sessions B automatisées en `claude -p` stream-json (précédent
  batch A) au lieu du copier-coller humain ; grader Sonnet isolé.
- **Volet B requalifié — diagnostic initial inversé** : le pré-flight lit
  fidèlement le `/prd` réel (14 sections dont Stack technique, Architecture
  technique, Risques & Mitigations — `prd.md:277-338`) ; le fantôme est le
  « PRD allégé (8 sections) » de la matrice, jamais implémenté dans la
  command ni acté par ADR. Overview §7.3 statué (A résolu, B chantier).

## En cours

- Rien — ce checkpoint à committer. `claude/settings.json` : plus de modif en
  working tree (le retour Fable 5/xhigh a restauré l'état commité — le
  « revert naturel » prévu).

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis push.
2. **CHANTIER volet B (session fraîche — consistant)** : conformer `/prd` au
   PRD allégé de la matrice. Chemin : ADR « format PRD canonique » (les
   8 sections n'ont jamais été actées ; satellite `conventions/prd.md`
   candidat — son critère de création est atteint) → refonte format de sortie
   + Phases 8/10 de `/prd` → pré-flight `/claude-md` (« stack technique,
   architecture » restants) + branche Phase 2 « PRD sans Cruft »
   d'instance-aware-flow.md → les deux corpus d'evals. Pièces au dossier :
   le `/prd` réel n'a pas de section Open questions (où la règle 6 de la
   matrice route les risques non résolus).
3. **Prioriser volet B vs routage SPIKE** (en file : ADR → eval failing →
   grill.md → sync matrice) — décision d'ordonnancement à prendre.
4. Adjacents signalés non corrigés : `setup-eval-cwd.sh` suppose un TTY
   (`cruft create` sans `--no-input` ; contournement session : `yes '' |`) ;
   fixtures `/tmp/claude-md-eval-*` laissées (hook block-rm-rf), purge
   manuelle ou reboot.
5. **Cycle /insights 2026-08-26** : observation règle graduée P2 + métrique
   ratio méta/produit (P3). **SD1** : cycle 2026-09.
6. (dormant) Corpus batch A mode « insertion » au premier replay ;
   `/code-review` sur dbt/Terraform au prochain diff réel.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

Aucun ADR écrit cette session (choix assumé, premier point ci-dessous). Choix
de portée session :

- **Pas d'ADR pour 7.1/7.2/7.3-A** : formalisations d'intentions et de
  décisions déjà existantes (la gate date d'`a34871a`), pas de décisions
  nouvelles — l'intro §7 de l'overview reformulée en conséquence ; la trace
  durable vit dans les documents amendés eux-mêmes et leurs commits.
- **Interprétation 7.1 ratifiée en séance** : les choix de portée session
  (échouant au test des 6 mois) se notent directement — l'alternative
  (section 100 % pointeurs) contredisait la pratique et ADR-0011.
- **Verdict 7.3-A** : gate voulue (archéologie git) ; la matrice reçoit la
  règle de fond (élaboration/contenu) plutôt qu'une exception documentée ;
  l'override track léger ferme le deadlock en faisant du CLAUDE.md généré le
  porteur de la déclaration ADR-0011.
- **Rejeu scopé plutôt que campagne complète** : rouge décidable par
  inspection textuelle, vert non → 3 runs + grading isolé. Refus de différer
  fondé sur l'anti-pattern documenté « corpus jamais exécuté » (ADR-0009) et
  sur la contrepartie de l'exemption direct-sur-main.
- **7.3-A en un seul commit** (eval + command + références + matrice +
  overview) : un purpose, atomicité respectée.
- **Hook block-rm-rf respecté** : pas de contournement pour le nettoyage des
  fixtures.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-28 16:05
Session : 8ab937ba-56ef-4310-a873-5d5aa43741ea

## Tâches complétées

- **`docs/methodology/workflow-overview.md` écrit et commité** (`391eeab`,
  539 lignes, 12 diagrammes Mermaid). Vue dérivée non-normative, bandeau de
  préséance matrice. 7 sections : cycle de vie projet (4 diagrammes, un par
  phase), carte documentaire, graphe des outils (scindé projet / session),
  cycle de vie ADR (stateDiagram-v2), 4 chemins de lecture, renvois +
  index des 12 ADRs, incohérences relevées.
- **Section 4 ajoutée hors brief initial** : cycle de vie ADR (Proposed →
  Accepted → Superseded/Deprecated) + tableau des 5 relations. Comblait un
  angle mort — aucune des 4 sections prévues ne portait la machine à états.
- **Trois incohérences relevées et instruites une par une** (§7 du doc,
  signalées sans correction conformément au mandat).
- **Debug aperçu Mermaid VS Code** : non résolu, glitch intermittent.
  Écarté comme non bloquant — le doc rend correctement (12 blocs validés
  au parseur mermaid-cli 11).

## En cours

- Rien d'actif — doc commité, ce checkpoint à committer.
- Modif `claude/settings.json` toujours en working tree : switch de modèle
  volontaire, **ne jamais la committer** (consigne reconduite).

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`, progress.md seul).
2. **Corriger les incohérences 7.1 et 7.2 — décisions déjà prises, à appliquer
   en différé avec Fable 5** :
   - **7.1** — section « Décisions prises » de progress.md : n'y mettre qu'un
     **pointeur vers l'ADR**, jamais la décision elle-même (évite la
     duplication et le drift). À expliciter dans la matrice et/ou le prompt
     de `/progress`, qui dit aujourd'hui « liste des choix faits pendant cette
     session » — formulation qui invite à dupliquer.
   - **7.2** — cocher un acceptance criterion du PRD change **l'état**, pas
     **la cible** : seule l'édition du *contenu* (modifier, ajouter,
     supprimer un critère) exige un ADR. Distinction implicite, à formuler
     dans la matrice.
3. **7.3 — PRIORITAIRE, non résolu, à instruire avec Fable 5 sur les deux
   repos (dotfiles + template Cruft)**. Seul écart *factuel* des trois
   (7.1/7.2 étaient des intentions non écrites) :
   - **Volet A — gate bloquante.** La matrice affirme que CLAUDE.md et PRD
     se font « dans n'importe quel ordre ». Or `/claude-md` **interdit la
     poursuite** si `.cruft.json` est présent ET `PRD.md` absent. Sur instance
     Cruft, l'ordre PRD → CLAUDE.md est donc imposé, pas libre. Question
     ouverte : la gate est-elle voulue (→ amender la matrice) ou trop stricte
     (→ assouplir la command en avertissement) ? Souvenir perdu, d'où
     l'inspection croisée.
   - **Volet B — champs fantômes.** Le pré-flight de `/claude-md` lit le PRD
     pour en extraire « stack technique, architecture, phases
     d'implémentation » — précisément ce que la matrice **interdit** au PRD
     et que les 8 sections du PRD allégé ne contiennent pas. Lecture
     silencieusement vide sur tout PRD conforme ; résidu d'un format antérieur.
4. **Valider puis implémenter le routage SPIKE** dans l'ordre
   ADR → eval failing → grill.md → sync matrice.
5. **Cycle /insights 2026-08-26** : observation règle graduée P2 + métrique
   ratio méta/produit (P3).
6. **SD1** : réévaluation au cycle /insights 2026-09.
7. (dormant) Corpus batch A mode « insertion » au premier replay ;
   `/code-review` sur dbt/Terraform au prochain diff réel.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Ajout d'une 5e section au doc** (cycle de vie ADR) au-delà des 4 livrables
  du brief — validé en séance, comble un angle mort réel.
- **§3 scindé en deux diagrammes** (outils projet / outils de session) : le
  découpage suit une frontière réelle du workflow (Phases 0-1 vs Phase 2),
  et résout au passage un placement Dagre ingérable.
- **§1 éclaté en 4 diagrammes** (un par phase) plutôt qu'un graphe à
  4 subgraphs : les flèches inter-subgraphs rendaient le placement erratique.
- **Les incohérences restent des signalements** : les intentions dégagées en
  séance (7.1, 7.2) ne sont PAS écrites dans le doc — une vue non-normative
  ne tranche pas, elle signale. Leur formalisation passera par la matrice.
- **Track léger, précision PRD** : le PRD n'est pas exclu mais optionnel et
  allégé ; `/prd` reste disponible mais son interview est disproportionnée à
  ce niveau d'enjeu.
- **Glitch Mermaid écarté** : diagnostic non concluant (extension réinstallée,
  syntaxe validée, GPU testé) ; intermittent, sans impact sur le livrable.

## Blocages

- **Aperçu Mermaid VS Code intermittent** — non bloquant pour la production
  du doc, mais gêne la relecture visuelle. Piste non explorée : inspection
  DOM du canvas via `Developer: Open Webview Developer Tools` (la console
  ne montrait aucune erreur, seulement du bruit standard de webview).

---

## Dernière mise à jour
Date : 2026-07-28 14:39
Session : 66b3a267-c78b-42f6-a8ae-29e0b5914e89

## Tâches complétées

- **Analyse critique du transcript Pocock** (« prototype skill », concept de
  fidélité des discussions de design) vs workflow existant. Verdict : le critère
  d'escalade de fidélité comble un vrai angle mort (branches indélibérables en
  Phase 0/1) ; la plomberie Pocock (copy-paste prototype → prod, code-as-asset)
  contredit test-first et la matrice — « adopter le routage, pas le blanchiment ».
- **Design d'implémentation du routage SPIKE** proposé (non validé) : 3e tag
  `SPIKE` dans l'output de /grill + critère d'éligibilité (« un argument peut-il
  trancher, ou seulement une observation ? ») ; ledger `DEFERRED (→ spike [N])`
  sans 4e état ; exécution manuelle sur branche jetable (build before
  automating) ; capture via /adr (mode capture), la branche meurt. Chemin
  d'implémentation : ADR (Extends ADR-0003) → eval failing → grill.md → sync
  matrice → épreuve sur projet réel.
- **Session doc « workflow overview » cadrée** : `docs/methodology/workflow-overview.md`,
  vue dérivée **non-normative** (précédent karpathy-discipline.md), bandeau de
  préséance matrice, 4 livrables (cycle de vie, carte documentaire, graphe des
  outils, chemins de lecture), couche learning hors scope.
- **Prompt de session écrit** : `tasks/prompt-session-workflow-overview.md`
  (fichier jetable, périmètre de lecture vérifié contre le repo — non commité).

## En cours

- Rien d'actif — ce checkpoint à committer.
- Modif `claude/settings.json` = switch temporaire de modèle, volontaire —
  **ne jamais la committer** ; la laisser en working tree (revert naturel
  quand le switch ne servira plus).

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`, progress.md seul —
   exclure claude/settings.json) puis push.
2. **Session dédiée doc overview** : Opus 5, effort high, coller le prompt de
   `tasks/prompt-session-workflow-overview.md` ; supprimer le fichier après usage.
3. **Après la doc : valider puis implémenter le routage SPIKE** dans l'ordre
   ADR → eval failing → grill.md → sync matrice.
4. **Cycle /insights 2026-08-26** (issue automatique) : observation règle
   graduée P2 + métrique ratio méta/produit (P3).
5. **SD1** : réévaluation au cycle /insights 2026-09.
6. (dormant) Corpus batch A mode « insertion » au premier replay ;
   `/code-review` sur dbt/Terraform au prochain diff réel.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Verdict Pocock** : adopter le critère de routage (escalade de fidélité),
  rejeter le blanchiment (le livrable d'un spike est une décision ADR, jamais
  du code à transplanter — l'implémentation repart test-first).
- **Ordre des chantiers** : doc overview AVANT implémentation SPIKE — l'écriture
  du doc sert de revue du système avant de le modifier.
- **Statut du futur doc** : vue dérivée non-normative, la matrice garde la
  préséance ; zéro règle réénoncée.
- **Ledger /grill** (dans le design SPIKE, à confirmer) : réutiliser
  `DEFERRED (→ spike)` plutôt qu'un état `ROUTED` dédié — zéro concept nouveau.
- **Modèle pour la session doc** : Opus 5 / effort high — tâche scaffoldée à
  validation par étape, conforme à la stratégie de tiers (Fable réservé à un
  éventuel audit critique de la matrice, hors scope ici).

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-28 13:46
Session : 27552b11-42c8-468f-b3a8-48ae050b6aeb (suite — re-run DN2 clos, ~/explain commité)

## Tâches complétées

- **Re-run de confirmation DN2 exécuté et tranché** (règle de décision fixée
  avant run, K4) : 3 runs opus-sans supplémentaires (outillage batch A, payload
  post-P2), grader Sonnet isolé — **3/3 pass, 12/12 expectations**. Bilan
  cumulé opus-sans : 1 fail / 4 runs. Décision humaine : **maintien confirmé,
  question fermée** (fail réel observé, n=4 n'exclut pas un taux faible, coût
  faible vs valeur des séparations prescrites, pas de filet en session).
  Commits `b9331fe` (trace) + `8199b48` (clôture), poussés.
- **`~/explain` commité** (délégation humaine explicite, dérogation ponctuelle
  au « à ta main ») : digest Cookiecutter + procédure d'ajout de skill,
  commit `a49d0b0` poussé — les 4 autres éléments du repo laissés intacts.
  Item reporté depuis le 2026-07-22 : clos.
- **Backlog immédiatement actionnable : zéro.** Il ne reste que du daté
  (/insights 2026-08-26 : observation P2 + métrique P3 ; SD1 2026-09) et du
  dormant à déclencheur (mode insertion corpus au premier replay, /code-review
  dbt/Terraform, items TODO.md tous ❌ — grille revérifiée ce jour).

## En cours

Rien — seul ce checkpoint reste à committer.

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis push.
2. **Cycle /insights 2026-08-26** (issue automatique) : observation de la règle
   graduée P2 + proposition de la métrique ratio méta/produit (P3).
3. **SD1** : réévaluation au cycle /insights 2026-09.
4. **Corpus batch A (au premier replay)** : mode « insertion » désormais requis
   pour DN1/DN5 *et rejeu DN2* ; point ouvert : exposition des subagents.
5. (dormant) Éprouver `/code-review` sur dbt/Terraform au prochain diff réel.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Règle de décision DN2 fixée avant exécution** (3/3 pass → réouverture
  proposée ; ≥1 fail → maintien) — robuste au confound payload post-P2 (moins
  de renforts adjacents : un pass est plus probant, un fail pointait maintien
  dans les deux lectures).
- **Maintien DN2 malgré 3/3 pass** : honnêteté statistique — n=4 écarte un taux
  d'échec élevé, pas un taux faible (~10-25 %) ; le fail batch A était un
  comportement réel, pas un artefact de grading.
- **Première exécution live de la règle « Graduated autonomy »** (commitée le
  matin même) : chaîne setup → 3 runs → grading → application de la règle de
  décision enchaînée sans validation intermédiaire, critère pass/fail couvrant.
- **Commit `~/explain` limité aux 2 fichiers dotfiles** : les éléments des
  autres fils de travail (journal, rétro-todo, procédure armement) exclus.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-28 12:22
Session : 27552b11-42c8-468f-b3a8-48ae050b6aeb (P2 autonomie graduée — cadrage, verdicts, application)

## Tâches complétées

- **P2 (autonomie graduée) exécuté de bout en bout** : cadrage pédagogique
  (mécanisme symlink vérifié : édition du payload = effet immédiat), interview
  1-question-à-la-fois (axe + 3 verdicts, tous tranchés par l'humain), diff
  validé avant application, 2 commits poussés (`8ef1502`, `7b6dcc5`).
- **Axe de gradation acté : critère vérifiable** — la laisse s'allonge quand un
  critère pass/fail explicite couvre le chemin (test rouge, eval, diff attendu,
  commande de vérification) ; sinon un pas logique par tour. K4 = socle.
- **Verdicts appliqués au payload** (`8ef1502`) : RS1 compressée en préférence
  de style (motivation token-cap retirée) · RS2 réécrite en bullet « Graduated
  autonomy » · « one concept at a time » retirée de Session Discipline (fusion
  dans RS2 graduée). RS3 intacte (Cat. C).
- **Trace d'audit écrite** (`7b6dcc5`) : section « P2 » dans
  `tasks/claude-md-audit-2026-07.md` — méthode (pas d'eval possible sur des
  règles de confiance), table des verdicts, statut P2 avec observation ouverte.

## En cours

Rien — P2 clos côté édition, `main` poussée. Seul ce checkpoint reste à
committer. Reste ouverte : la case « observation à l'usage » du statut P2.

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis push.
2. **Observation à l'usage de la règle graduée** — pas de critère chiffré
   dédié ; effet observé aux cycles /insights (prochain : 2026-08-26).
3. **P3** : proposer la métrique ratio méta/produit au cycle /insights 2026-08-26.
4. **SD1** : réévaluation au cycle /insights 2026-09.
5. **Corpus batch A (au premier replay)** : mode « insertion » pour DN1/DN5 ;
   point ouvert : exposition des subagents au global.
6. (option) Re-run de confirmation DN2-opus-sans-règle.
7. (reportés) Committer `~/explain` ; éprouver `/code-review` sur dbt/Terraform.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Pas d'eval pour les règles Cat. D** : elles encodent un choix humain de
  confiance — aucune vérité indépendante de la préférence → interview de
  cadrage au lieu d'un batch avec/sans.
- **RS1 : ambiguïté corrélation/causalité documentée** — le `[VALIDÉ]` du cycle
  2026-07 portait sur une fenêtre incluant le pré-fix harness ; le gate
  « demander avant de développer » survit comme préférence, le chiffre
  « 3 bullets » assoupli.
- **One-concept : terrain entièrement couvert** — rythme → RS2 graduée,
  séparations prescrites → DN2 (maintenue P1), pacing pédagogique → skills
  learning. Retrait sec.
- **Placement chirurgical** : la règle graduée occupe l'emplacement de RS2 dans
  Response Style — pas de section `## Autonomy` dédiée (1 ligne ne justifie pas
  un header, payload en cours d'amincissement).
- **Un seul commit payload** : les 3 changements forment un groupement logique
  unique (RS2 absorbe one-concept, RS1 partage la section).
- `claude/settings.json` (Fable→Opus, xhigh→high) **toujours hors commit**
  (choix humain, précédent des sessions antérieures).

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-28 10:07
Session : 45677a2a-5bf6-402b-ac63-e269b7b5bd3e (audit CLAUDE.md — P1 batch A exécuté, verdicts appliqués, P1 clos)

## Tâches complétées

- **Corpus batch A écrit et validé** (`claude/evals/claude-md/`) : 5 fixtures
  format Skill Creator (DN1, DN2, DN5, SV1, K3) à tension délibérée, ancres
  verbatim `rules/*.md`, outillage durable — `setup-eval-cwd.sh` (isolation
  `CLAUDE_CONFIG_DIR`, pas de double injection, vérifié par sentinelle) et
  `run-batch.sh` (34 runs, idempotent, transcripts stream-json).
- **34 runs exécutés (0 échec technique)** + grading par 5 graders Sonnet
  indépendants (1/règle), verdict par expectation avec preuve.
- **Verdicts rendus (règle à 3 issues)** : DN1 **retrait** (8/8 sans règle,
  Haiku compris) ; DN2 **maintien** (fail Opus sans règle — question
  composée) ; DN5 **retrait** (6/6 par la spec, 1 arbitrage anti-grader
  documenté) ; SV1 **compression en 1 ligne probabiliste** (8/8, plan de
  triage) ; K3 **maintien + resserrage** (diff chirurgical acquis 6/6 sans
  règle ; signalement des adjacents 0/3 sans règle, Sonnet fail même avec).
- **Payload édité, 5 commits poussés** (`278aeab..a6415c3`) : `4890a4f`
  DN1+DN5 retirées · `8dc45c5` SV1 compressée · `5fed226` K3 resserrée ·
  `92d374d` corpus + verdicts · `a6415c3` clôture statut. **P1 clos.**
- Mémoire `user-model-tier-strategy` créée (Opus défaut, Fable complexe,
  Sonnet/Haiku dédiés — les 4 tiers restent en service).

## En cours

Rien — P1 clos, `main` poussée. Seul ce checkpoint reste à committer.

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis push.
2. **P2 (autonomie graduée)** — périmètre d'entrée : RS1, RS2, « one concept
   at a time » (Cat. D) ; SD1 réévaluée au cycle /insights 2026-09.
3. **P3** : proposer la métrique ratio méta/produit au cycle /insights 2026-08-26.
4. **Corpus (au premier replay)** : mode « insertion » pour DN1/DN5 (règles
   retirées du payload) ; point ouvert : exposition des subagents au global.
5. (option) Re-run de confirmation DN2-opus-sans-règle.
6. (reportés) Committer `~/explain` ; éprouver `/code-review` sur dbt/Terraform.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Arbitrage DN5-sonnet-sans requalifié pass** : E4 ne sanctionne que
  l'absorption *silencieuse* ; demander confirmation est le comportement le
  plus conforme à la règle (documenté au doc d'audit).
- **K3 resserrée sur le seul volet non acquis** (signalement) + « unused
  imports » ajouté (angle mort révélé par la fixture). Libellés validés par
  l'humain avant écriture.
- **SV1 : clause « I don't know » conservée** dans la ligne compressée (non
  testée par l'eval, mais peu coûteuse et cohérente).
- **Fixture K3 stockée en `.py.txt`** : le hook ruff bloquait à raison les
  imports inutilisés délibérés ; renommage en `.py` à l'assemblage du CWD.
- **Mécanisme avec/sans = `CLAUDE_CONFIG_DIR` isolé** (variante du payload en
  CLAUDE.md user-level, credentials symlinkés, zéro hook) — retenu contre le
  swap du symlink réel, trop risqué pour les sessions concurrentes.
- `claude/settings.json` (switch Opus + effort high) **toujours hors commit**
  (choix humain) ; la hiérarchie de tiers énoncée par l'humain confirme les
  4 tiers en service → design batch A inchangé.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-27 15:51
Session : d2a940f5-f097-46e2-84f6-cf91da3cfb08 (audit CLAUDE.md global — P1, batch B)

## Tâches complétées

- **Analyse workflow vs fireside chat équipe Claude Code** (Cat Wu / Thariq
  Shihipar, AI Engineer World's Fair, via simonwillison.net 2026-07-21) :
  3 insights retenus et priorisés — P1 audit du CLAUDE.md global par evals,
  P2 autonomie graduée, P3 ratio méta/produit.
- **P1 lancé — inventaire complet** : 17 règles auditées, 4 catégories (A garde-fou
  modèle → eval ; B sagesse mal placée → réécrire ; C fait → garder ; D → P2),
  dans `tasks/claude-md-audit-2026-07.md`. Triage validé par l'humain.
- **P1 batch B (Cat. B) exécuté — 2 commits** :
  1. `eec3141` — DN3 (cohérence cross-phase) retirée du global, relocalisée dans
     les contrôles pré-validation de `/prd` (jointures Phases 6/11/12) et
     `/planning` (cohérence PRD ↔ PLAN).
  2. `c9ac076` — section Karpathy compressée (~45 → ~15 lignes) ; version
     intégrale (Why/How, dates) → `docs/methodology/karpathy-discipline.md`.
- Mineur : alias `git` LC_ALL=C.UTF-8 (sortie git en anglais) — `429b890`, poussé.

## En cours

- **P1 batch A (evals)** : 5 fixtures avec/sans règle à spécifier (DN1, DN2, DN5,
  SV1, K3), moteur Skill Creator (ADR-0009 Option C), puis run et verdicts.
  Statut détaillé : `tasks/claude-md-audit-2026-07.md`.

## Prochaines étapes

1. ~~Batch A — décisions de design~~ **Tranchées post-checkpoint** (`df9f5d8`,
   section « Décisions de design — batch A » du doc d'audit) : corpus dans
   `claude/evals/claude-md/` ; tiers de benchmark = tiers réellement en service
   (Fable/Opus/Sonnet + Haiku ciblé sur DN1/SV1, vérifié par grep des pins
   `model:`) ; verdict à 3 issues (retrait / maintien global / relocalisation
   command-scope si échec limité aux tiers faibles).
2. **Batch A — exécution** (aucune décision ouverte) : écrire les 5 fixtures
   (doctrine maison : tension délibérée), run Skill Creator sur les tiers
   définis, verdict par règle selon la règle à 3 issues (les evals restent en
   garde de non-régression aux changements de modèle).
3. **P2 (autonomie graduée)** après clôture P1 — périmètre d'entrée : règles
   Cat. D (RS1, RS2, « one concept at a time » ; SD1 réévaluée cycle 2026-09).
4. **P3** : proposer la métrique ratio méta/produit au cycle /insights 2026-08-26.
5. (reportés) Committer `~/explain` ; éprouver `/code-review` sur diffs variés.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Priorisation P1 → P2 → P3** : P1 peu coûteux et prérequis de confiance de P2 ;
  P3 est le résultat attendu, mesuré avant d'être corrigé.
- **Batch B avant batch A** : B n'exige pas de preuve (relocalisations), établit
  la baseline que les evals de A doivent juger, et immunise P1 contre le frein
  manuel démontré (ADR-0009 : corpus jamais exécuté).
- **SV1 : Option A** — pas de réécriture avant verdict d'eval ; coût de faux
  retrait le plus élevé de l'inventaire, coût de maintien faible.
- **SD1 (Scope Discipline) exclue de l'audit** — adoptée la veille (action du
  cycle /insights 2026-07) ; réévaluation au cycle 2026-09, avec données.

## Blocages

Aucun. `claude/settings.json` modifié hors session (switch de modèle opéré par
l'humain dans une autre session) — volontairement laissé hors de ce commit.

---

## Dernière mise à jour
Date : 2026-07-26 11:14
Session : edf854f6-6e59-4338-9d10-5853f84ae96a (cycle /insights juillet — protocole v3 complet)

## Tâches complétées

- **Cycle mensuel /insights 2026-07-26 bouclé de bout en bout** (issue #2, ouverte
  à 7h34 par la routine `trig_01CMHnwqgZYkdspEHeY3KsFj`) :
  1. **Étape 1 — revue de juin** : critère token-limit **✅ atteint** (1 session
     perdue sur 28 vs 8/22, fenêtre incluant encore le pré-fix) → entrée
     `[INSIGHTS 2026-06-26]` taguée `[VALIDÉ]` + ligne de verdict datée.
  2. **Étape 2 — scoring** : 8 suggestions notées (grille Impact/Coût/Risque) ;
     top 3 = 🥇 scope discipline, 🥈 hook anti-trailer, 🥉 teaching style.
  3. **Étape 3 — choix** : 🥇 scope-discipline ; entrée `[INSIGHTS 2026-07-26]`
     écrite dans `tasks/lessons-inbox.md` (critère : zéro interruption en recon
     au rapport d'août ; revue 2026-08-26).
  4. **Étape 4 — application** : section `## Scope Discipline (reconnaissance)`
     ajoutée à `claude/CLAUDE.md` (gate limité à l'exploration multi-fichiers,
     clause anti-sur-gating pour questions simples). Commit `d4f15cd` poussé,
     issue #2 fermée automatiquement via `Closes #2` (vérifié CLOSED à 11h09).
- **Issue #1 vérifiée déjà CLOSED** (28/06, cycle précédent) — rien à faire.
- **Item « Revue action insights 2026-07-26 » du checkpoint précédent : clos.**

## En cours

Rien — cycle clos, `main` poussée, working tree clean. Seul ce checkpoint reste
à committer.

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis push.
2. **Prochain cycle /insights : 2026-08-26** (issue #3 via la routine). Critère à
   vérifier : zéro interruption utilisateur pendant une phase de reconnaissance.
   Candidates reportées si toujours pertinentes : 🥈 hook PreToolUse anti-trailer,
   🥉 section Teaching style.
3. **(reporté, à ta main)** Committer `~/explain` (digest + procédure d'ajout de skill).
4. **(reporté)** Éprouver `/code-review` sur diffs variés (dbt, Terraform).

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Cadence /insights maintenue mensuelle** : échantillon ~28 sessions nécessaire
  aux verdicts, discipline « une action/cycle » calibrée sur ce rythme, 2 cycles
  sur 2 validés. Option notée sans engagement : pulse de mi-parcours (~le 10,
  vérif du seul critère en cours, sans rapport ni action).
- **Section Scope Discipline ciblée recon uniquement** — le « smallest diff » du
  rapport n'est pas dupliqué (déjà couvert par Surgical Changes/Karpathy).
- **Un seul commit pour le cycle** (précédent `0dc22e6` du cycle de juin).

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-23 11:45
Session : e82b3af7-63bb-42a3-9cd8-4dc89894c389 (feynman-mentor — Phases 4-5 : code-review, triage, commits)

## Tâches complétées

- **Phase 4 — `/code-review` exécuté sur le diff non commité** (session fraîche,
  comme planifié). Périmètre couvert en entier : 6 fichiers modifiés + ADR-0012 +
  les 6 fichiers de la skill. Vérifications levées avant émission : cross-références
  ADR/format toutes valides, test de parité skills OK, compteurs cohérents (3 docs),
  liens relatifs fonctionnels via symlink, claim « pattern code-mentor » exact.
  Résultat : **2 findings MEDIUM, 0 CRITICAL/HIGH, aucun item (ADR)**.

- **Triage humain + corrections appliquées** (hors invocation skill — l'humain a
  tranché « Ok ») :
  1. `setup-eval-cwd.sh` : en-tête périmé réécrit (prétendait la skill non
     intégrée à install.sh ; risque de `rm` du symlink actif). Prérequis devenu
     « vérifier le symlink » au lieu de « le créer/supprimer à la main ».
  2. `adr/0012` : `Proposed` → `Accepted` (décision implémentée, matrice adossée,
     corpus 6/6 vert = porte de validation franchie ; cohérent avec le passage
     d'ADR-0009 à Accepted dans le même diff).

- **Phase 5 — 5 commits atomiques sur main** (découpage de l'esquisse respecté) :
  `0ff56f7` docs(adr) ADR-0012 + matrice · `c787ee0` feat(skills) feynman-mentor ·
  `eaa67bb` test(skills) corpus 6 evals · `cea4c14` docs(adr) accept ADR-0009 ·
  `2c26da6` docs(todo) clôture item Skill Creator.

- **Item TODO « Run live Skill Creator » clos** : ligne de grille annotée
  ✅ 2026-07-23, section retirée du corps (41 lignes — précédent `block-force-push`
  pour le retrait complet, précédent item (a) pour l'annotation de grille).

- **Question méta effort tranchée** : `/code-review` garde `effort: high` (valeur
  du frontmatter, calibrée 0 faux positif) — pas de `xhigh` en argument ; le
  `xhigh` de session reste un curseur séparé, à la main de l'humain.

## En cours

Rien — Phases 0-5 closes, la procédure d'ajout de skill est déroulée de bout en
bout. Seul `progress.md` (ce checkpoint) reste à committer, puis push.

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis **push des 6 commits**
   vers `origin/main` (rien n'est encore poussé).
2. **Revue action insights : 2026-07-26** — relire `[INSIGHTS 2026-06-26]`,
   vérifier le critère token-limit, taguer `[VALIDÉ]` si atteint. La routine
   remote ouvrira l'issue ce jour-là.
3. **(à ta main)** Committer `~/explain` (digest + procédure d'ajout de skill).
4. **Éprouver `/code-review` sur diffs variés** (dbt, Terraform) — ce run-ci
   était documentaire/shell ; le calibrage hors-Python reste à faire.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Effort de la revue = `high` du frontmatter** (pas l'`xhigh` de session) :
  régime calibré ADR-0010, diff majoritairement documentaire.
- **Les 2 findings acceptés tels quels** par l'humain, corrigés avant commit —
  ADR-0012 passé `Accepted` plutôt que maintenu `Proposed` en validation différée.
- **Clôture TODO par retrait complet** de la section (item entièrement consommé),
  pas d'annotation résiduelle dans le corps.
- **`progress.md` exclu des commits de feature** : le checkpoint part dans son
  propre commit de fin de session.
- **Horodatage** : anomalie relevée sans correction — le checkpoint précédent
  (même jour) affiche 12:15, postérieur à l'heure système actuelle (11:45).
  Historique laissé intact.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-23 12:15
Session : 0d7a14d7-fe41-40c5-91e1-b8ae985dddc4 (feynman-mentor — procédure complète + run live ADR-0009)

## Tâches complétées

- **Procédure d'ajout de skill documentée** : `~/explain/procedure-ajout-skill-dotfiles.md`
  (6 phases : cadrage → evals test-first → implémentation → tests → /code-review →
  livraison). Non commitée (repo ~/explain à la main de l'humain).

- **Skill `feynman-mentor` importée et cadrée (Phase 0)** : archive claude.ai
  (2025-12-29) extraite, lue intégralement, placée dans `claude/skills/feynman-mentor/`.
  Audit best practices (doc officielle Anthropic + shanraisshan) : conforme sur
  l'essentiel, 4 arbitrages levés et tranchés par l'humain — pont ADR-0008,
  `disable-model-invocation: false`, triggers reformulés (français, sans collision
  `teach`), `allowed-tools: Read` (candide structurel, pattern ADR-0010).

- **ADR-0012 créé** (Proposed, Extends ADR-0007) : 5ᵉ niche couche learning
  « vérification de compréhension par explication », 4 modalités d'intégration.
  Amendé en cours de session : template de feedback rendu dans la langue de session.

- **Matrice amendée** : 5ᵉ ligne couche learning, compteurs 4→5, précédent → « pas de
  sixième outil redondant ». Ordre canonique respecté (ADR → document → outil → eval).

- **Corpus d'evals écrit test-first** (`claude/skills/feynman-mentor/evals/`) :
  6 evals / 4 classes (`core_invariant` ×2, `discovery` ×2, `no_side_effect`,
  `state_bridge`), format maison + `setup-eval-cwd.sh` + README. Rouge par
  construction contre le SKILL.md importé.

- **SKILL.md adapté** : chaque changement trace vers une eval (triggers FR pushy,
  frontière négative teach, tool discipline, template trois volets en langue de
  session, section learning-record ADR-0008 quasi-inconditionnelle).

- **RUN LIVE Skill Creator exécuté — ADR-0009 tranché et acté `Accepted`** :
  découverte : les miroirs marketplace contiennent le moteur COMPLET (la « version
  légère » de juin est périmée). Chaîne exécutée intégralement : conversion
  `evals.json` officiel → 8 Executors (with/without) → 8 Graders → benchmark
  officiel **100 % vs 17,5 % baseline (delta +0.82)** → analyste → viewer statique.
  4 evals comportementales à 1.00.

- **Discovery arbitrée après diagnostic de proxy biaisé** : `run_eval.py` teste un
  pseudo-command en `claude -p` — inadapté aux skills conversationnelles (0-1/3).
  Contre-épreuve en conditions réelles (skill installée, 6 sessions fraîches) :
  **3/3 positif candide, 3/3 négatif sans candide → corpus 6/6 vert**. Friction
  documentée dans le README d'evals (protocole de référence classe `discovery` =
  conditions réelles).

- **Intégration Phase 2 complète** : `install.sh` (ligne link), README racine,
  `claude/README.md` (compteur 5→6 + glose), symlink actif, **test de parité OK**.

## En cours

Rien — Phases 0-3 closes, 6/6 vert. Phase 4 (audit) volontairement reportée en
session fraîche (29 % de contexte restant + indépendance du réviseur).

## Prochaines étapes

1. **[SESSION FRAÎCHE] Phase 4 — `/code-review` sur le diff NON COMMITÉ** (pas un
   diff de branche — exemption direct-sur-main). Périmètre exact :
   - Modifiés : `README.md`, `adr/0009` (statut), `claude/README.md`, matrice, `install.sh`
   - Untracked : `adr/0012-*.md`, `claude/skills/feynman-mentor/` (SKILL.md,
     references/, evals/ — dont evals.json officiel)
2. **Triage des findings**, puis **Phase 5 — commits atomiques**. Esquisse de
   découpage (à affiner au triage) :
   - `docs(adr): ADR-0012 + amendement matrice` (décision + document cible)
   - `feat(skills): add feynman-mentor` (skill + install.sh + READMEs)
   - `test(skills): feynman-mentor eval corpus` (evals/ maison + officiel)
   - `docs(adr): accept ADR-0009 after live Skill Creator run`
3. **`TODO.md` : clore l'item « Run live Skill Creator »** (déclencheur atteint et
   consommé cette session).
4. Reliquat inchangé : revue insights 2026-07-26 ; committer `~/explain` (digest +
   procédure) ; éprouver `/code-review` sur dbt/Terraform.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **ADR-0012 (Option C)** : 5ᵉ niche intégrée à la couche learning, 4 modalités.
- **ADR-0009 acté `Accepted`** (décision humaine) : run live concluant, moteur
  officiel = exécuteur, doctrine maison souveraine.
- **Record quasi-inconditionnel** (vs conditionnel chez code-mentor) : exigé par la
  modalité 1 d'ADR-0012 et l'eval `state_bridge`.
- **Triggers cités en français** (langue d'usage réelle), corps de description en
  anglais — matching sémantique, valeur illustrative.
- **Classe `discovery` : protocole de référence = conditions réelles** (proxy
  officiel biaisé pour les skills conversationnelles — documenté au README d'evals).
- **Workspace de run hors repo** (scratchpad) : un sibling dans `claude/skills/`
  aurait cassé le test de parité. Artefacts éphémères ; la trace durable vit dans
  le README d'evals.
- **Écart d'ordre assumé** (demande humaine) : intégration Phase 2 effectuée avant
  clôture complète de Phase 3 — défendable, le rouge résiduel était un problème de
  découvrabilité, pas de comportement.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-07-22 20:20
Session : 74a20185-8bbc-4a4d-971b-c289b9f06f6f (grill-matrice + rituel code-review + clôture TODO (a))

## Tâches complétées

- **Créneau `/grill` inscrit dans la matrice de responsabilité** (4 points chirurgicaux
  dérivés de `grill.md`, aucune règle inventée) : Phase 0 (grill du PRD avant gel),
  Phase 1 (grill du PLAN, un artefact par invocation), frontière négative Phase 3
  (jamais de re-grill d'un artefact gelé), ligne `/grill` dans « Conséquences
  architecturales pour les outils » avec lien ADR-0003. La matrice dit *quand* griller,
  la command garde le *comment*. Commit `41d9d12`.

- **Drift `claude/settings.json` analysé et ratifié** : `~/.claude/settings.json` est
  un symlink vers le repo → toute sauvegarde de réglage du CLI (`/model`, `/effort`…)
  écrit dans le working tree. Diff = passage à Fable 5 par défaut (choix humain) +
  réordonnancement de clés par le sérialiseur. Ratifié selon le précédent `0fc02e5`.
  Commit `8f3b895`.

- **Rituel `/code-review` de fin de feature adopté en convention** (CLAUDE.md global,
  section Version Control) : avant PR/merge d'une feature branch, `/code-review` sur
  le diff + triage des findings. Human-triggered, daté (adopted 2026-07-22).
  Commit `d26c0c0`.

- **Digest du template Cookiecutter écrit** : `~/explain/digest-python-project-template-cruft.md`
  (réappropriation post-dette de compréhension). Redécouvertes clés : 16 notes
  pédagogiques dans `~/notes-templating/`, 25 décisions v1 figées dans `_sources/`,
  v2 = reconstruction pédagogique du 2026-04-18 (20 commits). Non commité (repo
  `~/explain`, à la main de l'humain).

- **Analyse de couplage dotfiles ↔ template** : couplage unidirectionnel (dotfiles →
  template), conditionnel (détection `.cruft.json` dans les pré-flights `/prd` et
  `/claude-md`), à dégradation gracieuse. Verdict : les deux briques restent
  composables non couplées — utilisables l'une sans l'autre.

- **TODO item (a) clos — PR template migré vers le repo Cookiecutter** : contenu
  restauré depuis `744ba61^` à l'identique (pas de Jinja-isation), placé sous
  `{{ cookiecutter.project_slug }}/.github/`. PR #1 squash-mergée (`f2dc721`),
  branche supprimée, refs purgées. `TODO.md` mis à jour (grille + corps d'item).
  Commit dotfiles `0458aa1`.

- **Mémoire `feedback_no_coauthor` étendue** : jamais d'attribution Claude dans les
  corps de PR non plus (rejet humain du footer lors du `gh pr create`). Commits ET
  PR bodies, tous repos.

## En cours

Rien — working trees propres des deux côtés (dotfiles : 4 commits poussés
`41d9d12..0458aa1` ; template : `f2dc721` sur main). Seul le digest `~/explain`
reste non commité (choix humain).

## Prochaines étapes

1. **Revue action insights : 2026-07-26** — relire `[INSIGHTS 2026-06-26]`, vérifier
   le critère token-limit (< 8/22 sessions), taguer `[VALIDÉ]` si atteint. La routine
   remote ouvrira l'issue ce jour-là.
2. **(à ta main)** Committer le digest dans `~/explain`.
3. **Éprouver `/code-review` sur diffs variés** (dbt, Terraform) — le rituel
   nouvellement adopté générera les occasions naturelles.
4. **TODO.md — items différés restants** (aucun déclencheur atteint) : hook
   `/clear`→`/progress`, parité commands, skill `/pr` (volet b), audit workflow,
   run live Skill Creator.
5. Reliquat de fond inchangé : campagnes evals `/grill`/`/adr`/`/planning` (session
   dédiée à 0 %) ; re-router `methodology-trial` ; workspace teach ; (optionnel)
   MAJ mémoire `project_insights_routine.md`.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Pas de hook pour `/code-review`** : « feature achevée » n'est pas un événement
  détectable (commit/push/Stop misfirent tous) ; les hooks du repo sont des garde-fous
  déterministes bon marché, pas des revues coûteuses ; la skill n'est éprouvée que
  sur Python. Convention humaine = palier 1, symétrique de `/progress`-avant-`/clear`.
- **Pas d'entrée TODO palier 2** pour l'automatisation du rituel : zéro occurrence
  d'oubli — l'entrée naîtra à la première occurrence réelle (doctrine d'émergence).
- **Squelettes `claude/templates/` non retouchés** malgré leur présomption de
  bootstrap template : consommés manuellement uniquement (« Jamais par Claude » per
  README), zéro occurrence de friction — fix différé au premier projet hors-Cruft gêné.
- **Migration PR template à l'identique** (pas d'adaptation Jinja) : Surgical Changes,
  le contenu était déjà générique et aligné sur la stack du template.
- **Squash-merge pour la PR #1** : conforme à la doctrine du template lui-même
  (« PR title becomes the squash commit message »).

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-28 22:39
Session : 6e0d1aa1-def3-48c6-87b3-9b0e639c25fc (insights-cycle-juin + fix block-force-push)

## Tâches complétées

- **Cycle `/insights` de juin bouclé (protocole v3).** Issue de rappel #1 (créée
  le 26/06 par la routine remote) traitée de bout en bout : scoring 3 axes des 8
  suggestions du rapport `report-2026-06-28-221616.html`, top 3 proposé, UNE action
  retenue (`response-style-token-budget`). Étape 1 (relecture mois précédent) sautée
  — première exécution, pas de note antérieure. Note `[INSIGHTS 2026-06-26]` écrite
  dans `lessons-inbox.md` (critère : part de sessions wipe sur token-limit nettement
  < 8/22 ; revue 2026-07-26). Commit `0dc22e6`.

- **Action insights appliquée** : section `## Response Style` ajoutée au
  `claude/CLAUDE.md` global (résumé 3 bullets avant développement, increments courts,
  artefacts longs en fichiers) — attaque la friction n°1 du rapport (≥8/22 sessions
  perdues sur erreurs API « 500 output token maximum »). Synchro `~/.claude/CLAUDE.md`
  faite. Commit `0dc22e6`. Issue #1 fermée avec commentaire de clôture.

- **Routine remote `/insights` améliorée** (`trig_01CMHnwqgZYkdspEHeY3KsFj`, via
  RemoteTrigger) : le prompt demande désormais d'ajouter `Closes #N` au commit
  d'application (fermeture auto de l'issue au push) et d'afficher le numéro de l'issue
  créée. Reste activée, prochain run 26/07 7h30 Paris. (Friction identifiée ce cycle :
  fermeture #1 manuelle car le commit ne référençait pas l'issue.)

- **Fix `claude/hooks/block-force-push.sh` (TODO #6).** La regex matchait `-f`
  n'importe où après `push` → tout nom de branche contenant la sous-chaîne (`-frontmatter`,
  `-final`, `-feature`) bloqué à tort. Resserrée aux **tokens d'option** (word boundary) ;
  `--force-with-lease` désormais bloqué aussi (décision humaine). Test-first : harness
  15 cas validé rouge (11/15) → vert (15/15). Item retiré de `TODO.md`. Commit `595eef1`.
  Ferme la boucle ouverte par `f49a62d` (qui avait documenté ce faux positif).

## En cours

Rien — working tree propre, 2 commits sur main (`0dc22e6`, `595eef1`).

## Prochaines étapes

1. **Revue action insights** : 2026-07-26, relire `[INSIGHTS 2026-06-26]` et vérifier
   le critère (taguer `[VALIDÉ]` si atteint). La routine redéclenche une issue ce jour-là.
2. **(optionnel)** Mettre à jour la mémoire `project_insights_routine.md` pour documenter
   le mécanisme `Closes #N` ajouté au prompt de la routine.
3. **TODO.md — items différés restants** (tous conditionnels, aucun déclenché) : hook
   `/clear`→`/progress`, check de parité commands, migration PR template + skill `/pr`,
   audit workflow agentique, run live Skill Creator (ADR-0009).
4. Reliquat de fond inchangé : éprouver `/code-review` sur diffs variés ; re-router
   `methodology-trial` ; workspace teach ; campagnes evals `/grill`/`/adr`/`/planning`.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Une seule action insights ce cycle** (`response-style-token-budget`) : règle de
  discipline v3 non négociable. 🥈 audit des hooks et 🥉 flag des bugs de hooks reportés
  au prochain `/insights` si toujours pertinents.
- **`response-style-token-budget` placé dans `## Communication` voisinage** (nouvelle
  section `## Response Style` après Communication) : cohérence thématique forme des réponses.
- **`--force-with-lease` bloqué** par le hook (choix humain) : reste un push réécrivant
  l'historique distant → traité comme `--force`.
- **Correctif hook = resserrement regex, pas réécriture en parseur de tokens** : Simplicity
  First — la regex à word boundary couvre le contrat validé (15/15) sans sur-ingénierie.
  Limite résiduelle assumée et signalée : argument commençant littéralement par `-f`.
- **Fix `block-force-push` traité hors règle « une action/cycle »** : item `TODO.md`
  indépendant à déclencheur « bug reproductible », distinct du cycle insights.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-25 14:15
Session : e4803760-f2e4-4101-87e2-0fe29a19b618 (implement-code-review-reloaded — clôture)

## Tâches complétées

- **Documentation entièrement synchronisée** — audit des 5 pièces documentaires après
  livraison de la skill. Deux dérives corrigées : README racine oubliait `code-review`
  dans le listing Skills (ligne 104) ; README claude n'avait pas de checklist pour
  l'ajout d'une skill (seulement pour les commands). Ajout de la section « Ajouter une
  skill — checklist multi-fichiers » avec test de parité (`diff ls-d / grep install.sh`)
  vérifié fonctionnel. Tests de parité skills ET commands passent (sortie vide). Commit
  `a68ec63`.

- **`/immunize` exécuté** — consolidation de `tasks/lessons-inbox.md` (6 entrées,
  plage 2026-04-27 → 2026-05-26). 2 règles promues en `## Global Do NOT` (3 → 5) :
  (1) pas de `.claudeignore` / Read-Glob-Grep non `.gitignore`-aware, (2) conventions
  figées en session = contraintes dures pour les phases suivantes. 4 entrées archivées
  dans `tasks/lessons-archive.md` (créé). Inbox vidée. Commit `60308da`.

## En cours

Rien — working tree propre, `origin/main` à jour (`60308da`).

## Prochaines étapes

1. **`/insights` du 2026-06-26** (demain) — vérifier le critère de succès de la règle
   `State Verification` : la catégorie « Hallucinated state » doit avoir baissé ou
   disparu du top-3 friction. Entrée archivée dans `lessons-archive.md` pour traçabilité.
2. **Éprouver `/code-review` sur des diffs variés** (dbt, Terraform) — compléter le
   calibrage au-delà du cas Python search-work-app.
3. **(report session précédente)** Re-router `methodology-trial` ; workspace teach ;
   run live Skill Creator (→ trancher ADR-0009) ; campagnes evals `/grill`/`/adr`/`/planning`.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Checklist skill distincte de la checklist command** : une skill est un dossier
  (pas un fichier `.md`), le test de parité est différent — méritait sa propre section.
- **`lessons-archive.md` créé** (n'existait pas) : les 4 entrées y sont versées
  avec contenu intégral + note d'archivage, conformément à la contrainte
  « jamais supprimer sans archiver ».

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-25 12:50
Session : e4803760-f2e4-4101-87e2-0fe29a19b618 (implement-code-review-reloaded)

## Tâches complétées

- **Skill `/code-review` surchargée (user-scope) créée et livrée.** Première passe
  de revue qui surcharge la bundled `/code-review` (vérifié : skill user-scope >
  bundled sur nom identique). Signale uniquement, jamais d'auto-fix (`allowed-tools`
  sans Edit/Write → garde-fou structurel). Effort `high` par défaut. Encode mes
  conventions (structlog/pathlib/type-hints, Kimball/ref(), Terraform-variables), la
  frontière hooks/simplify (pas de redondance ruff), et la reconnaissance de la
  complexité délibérée (fail-closed, validation redondante à source unique).
  Délégation des findings `(ADR)` par instruction (pattern /grill, ADR-0003), jamais
  par invocation. Commit `03165b1`

- **ADR-0010 créé puis Accepted** : surcharge user-scope de /code-review. Mode
  capture (délibération dans le fil). 4 arbitrages tranchés : frontière revue/hooks/
  simplify · reconnaissance complexité délibérée · ledger→/adr par instruction ·
  effort high. Commits `272dc08` (Proposed) → `39edfe2` (Accepted, validé à l'usage).

- **État des lieux vérifié contre le réel** (v2.1.191) : /code-review signale par
  défaut (--fix requis pour appliquer), /simplify = cleanup-only séparé depuis
  v2.1.154. Hooks cartographiés (ruff = lint/format ; force-push/rm-rf/protect_env =
  runtime) — aucun ne fait de revue correction/sécurité du diff.

- **Calibrage contre un diff réel** (search-work-app, commit G2 `45b65b3`) : run n°1
  = 1 faux positif (None-coords, alors que _parse droppe déjà les None) ; correction
  ciblée « résoudre tout doute vérifiable avant d'émettre » ; run n°2 = 0 faux
  positif, complexité délibérée reconnue 3/3, 0 vrai finding raté. Commit `03165b1`

- **Intégration repo** : ligne symlink dans `install.sh`, listing skill dans
  `claude/README.md` (compteur 4→5, famille « Revue » distincte de la couche
  learning). Commit `03165b1`.

- **Run réel de la skill sur "geocode-failure hardening diff"** (search-work-app) :
  résolu à l'item backlog H1 **non implémenté** → la skill s'est arrêtée sans
  inventer de revue (procédure §1 respectée). A confirmé au passage que H1 vise un
  vrai défaut existant (geocode_city hors try/except → 500 brut au lieu du 502 D2).

## En cours

Rien — working tree propre, 3 commits poussés sur origin/main (`b75b414..39edfe2`).

## Prochaines étapes

1. **Éprouver `/code-review` à l'usage** sur de vrais diffs de projets variés
   (Python applicatif, dbt, Terraform) — vérifier la frontière hooks et le taux de
   faux positifs hors du cas search-work-app.
2. **(report des étapes de la session précédente, inchangées)** Re-router
   `methodology-trial` ; créer le workspace teach ; run live Skill Creator
   (→ trancher ADR-0009) ; campagnes evals A→B→A `/grill`, `/adr`, `/planning`.

## Décisions prises

- **Surcharge plutôt que command à nom distinct** (ADR-0010, Option B) : surcharge le
  réflexe /code-review sans doublon ; la skill user-scope l'emporte sur la bundled.
- **Signale, n'applique jamais** : garde-fou rendu structurel (pas d'Edit/Write dans
  allowed-tools), pas seulement déclaratif. Le fix-avec-nettoyage reste à /simplify.
- **Ledger→/adr par instruction, pas par invocation** : applique le précédent
  ADR-0003 (une command ne pilote pas une autre) à la famille des commands de revue.
- **Procédure durcie après calibrage** : interdiction des findings spéculatifs
  vérifiables dans le repo — résoudre le doute par lecture avant d'émettre.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-23 16:30
Session : 4e0e35cc-bdad-40fa-8836-fbf7fb421aec (learning-skill — suite)

## Tâches complétées

- **README claude/ enrichi** : listings Commands et Skills étoffés d'une glose
  d'une ligne par item (format Hooks étendu à Commands + Skills). Checklist
  « Ajouter une command » mise à jour (format liste-avec-glose). Compteurs et
  parité vérifiés. Commit `0412a99`

- **Contrôle web Skill Creator officiel (Anthropic)** — vérifié sur source
  primaire (`anthropics/claude-plugins-official`, SKILL.md officiel lu verbatim) :
  plugin Claude Code réel, annoncé 2026-03-03, 4 modes (Create/Eval/Improve/
  Benchmark), 4 sous-agents (Executor/Grader/Comparator/Analyzer). L'Evaluation
  Tool de la Console est un outil *distinct* (prompts à variables, pas harnais
  SKILL.md). Résultat : ton rituel A→B→A maison a reconstruit par anticipation
  la structure qu'Anthropic vient d'outiller (format `grill.eval.json` ≈
  `evals/evals.json` officiel).

- **ADR-0009 créé** (Proposed) : délibération rituel maison A→B→A vs Skill
  Creator officiel. Recommandation Option C (hybride : moteur officiel + doctrine
  maison souveraine). Réserve identifiée : inconnue (a) format, inconnue (b)
  exécution. Commit `53f4c2e`

- **Essai pilote de traductibilité** : eval maison `output-no-file-written`
  (invariant hors-transcription : « zéro fichier écrit ») converti au format
  `evals.json` officiel. Inconnue (a) levée favorablement : assertions officielles
  absorbent la doctrine maison, invariants hors-transcription deviennent
  *programmables* (sha256, ls). Frange irréductible : jugement de présentation →
  qualitatif (eval-viewer), non pass/fail. Inconnue (b) (exécution) : reste
  ouverte — plugin sur disque = version légère sans agents/scripts/eval-viewer.
  Corpus pilote versé dans `grill/evals/pilot-skill-creator/`. Commit `7fc6ff2`

- **TODO.md mis à jour** : entrée « Run live du Skill Creator officiel → trancher
  ADR-0009 ». Déclencheur : prochain besoin réel d'eval (teach éprouvé ou corpus
  /grill). Portée : run live valide le *moteur* une fois ; adoption par skill au
  fil de l'eau (pas big-bang). Commit `7fc6ff2`

- **Confrontation best practices shanraisshan** (skills) — vérifié : frontmatter
  conforme, corps aligné Pocock. Aucun chantier. Acté dans le commit teach.

## En cours

Rien — working tree propre (`docs/rpi-audit-findings.md` untracked, hors périmètre).

## Prochaines étapes

1. **Re-router `methodology-trial`** (archive `tasks/learning-tracker-archive/`)
   — prochaine étape : `/claude-md` sur memory-grep + Phase 1a implémentation.
2. **Créer le workspace teach** (repo dédié, `MISSION.md` à rédiger) — à la
   première vraie session d'apprentissage AI Engineer.
3. **Run live Skill Creator** (cf. `TODO.md`) — déclenché par prochain besoin
   d'eval réel ; sur succès → trancher ADR-0009 en Accepted (Option C).
4. **Campagne evals A→B→A `/grill`** — corpus spécifié, jamais exécuté.
5. **Campagne evals A→B→A `/adr` et `/planning`** — état inchangé.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **ADR-0009 laissé Proposed** (reco) : inconnue (b) exécution non levée —
  run live déclenché par besoin réel, pas à blanc.
- **TODO.md** = bonne destination pour le run live (chantier futur conditionnel) ;
  ADR-0009 = délibération ; pilote = preuve figée. Non-overlap respectée.
- **Adoption par skill** (teach/code-mentor/etc.) se fait au fil de l'eau après
  run live du moteur — pas en big-bang.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-23 14:45
Session : 4e0e35cc-bdad-40fa-8836-fbf7fb421aec (learning-skill)

## Tâches complétées

- **Refonte couche learning — architecture teach adoptée**. 5 ADRs (0004-0008,
  tous Accepted), 6 commits atomiques sur main. Handoff complet exécuté.

- **ADR-0004** : `reference/` en Markdown (chaîne PKM), `lessons/` HTML Tufte
  conservé. Seul écart assumé au design Pocock. Commit `5fb08d3` (groupe)

- **ADR-0005** : rétention unifiée via Anki — quiz HTML in-lesson reclassés
  fluency-only ; `teach` réutilise `code-mentor/scripts/anki-export.py` et son
  format sans duplication. Commit `5fb08d3`

- **ADR-0006** : `learning-records` = source d'état unique. `coach-pedagogique`
  garde son `PROGRESS.md` intra-projet (nature distincte : scaffolding-sur-
  livraison), émet en plus un record de synthèse unidirectionnel. Option A
  tranchée par l'humain. Commit `5fb08d3`

- **ADR-0007** (parent) : `teach` adopté comme colonne vertébrale stateful,
  `learning-tracker` tué, motif 4 outils / 1 état / 1 rétention, `dp-coach`
  conservé (niche distincte confirmée par l'humain). Commit `5fb08d3`

- **ADR-0008** : mécanique du pont d'état — record proposé/affiché en bloc
  copiable, jamais écrit hors CWD (symétrique au pattern existant code-mentor +
  précédent ADR-0003). Mécanique tranchée par l'humain. Commit `6e9d8a6`

- **Skill `teach` créée** (`claude/skills/teach/` — SKILL.md + 4 fichiers de
  format). Adaptée des 3 ADRs, pédagogie Pocock conservée verbatim ailleurs.
  Symlink runtime actif + déclaré dans `install.sh`. Commit `cb38733`

- **`learning-tracker` supprimé** : command, agent, hook SessionStart,
  entrée settings.json, 4 lignes install.sh, symlinks runtime. État (`MEMORY.md`
  + `completed-topics.md`) archivé dans `tasks/learning-tracker-archive/` avec
  README de provenance (suivi actif `methodology-trial` découvert à l'exécution
  — surfacé plutôt que détruit). Commit `2f3eced`

- **3 outils branchés sur le pont d'état** (`code-mentor`, `dp-coach`,
  `coach-pedagogique`) : chacun gagne une étape de fin de session proposant un
  learning-record copiable. Commit `6e9d8a6`

- **Matrice de responsabilité étendue** : section « Couche learning » ajoutée
  (table non-overlap 4 outils, 2 sources de vérité, backlinks ADRs). Commit
  `0929944`

- **Confrontation best practices shanraisshan** : frontmatter conforme (champs,
  caps, disable-model-invocation) + convention maison (3 skills existantes, même
  pattern). Corps aligné Pocock qui fait autorité. Aucun chantier supplémentaire.

## En cours

Rien — working tree propre (`docs/rpi-audit-findings.md` untracked, hors
périmètre).

## Prochaines étapes

1. **Re-router `methodology-trial`** (archive `tasks/learning-tracker-archive/`)
   — prochaine étape : `/claude-md` sur memory-grep + Phase 1a implémentation.
   Branches ouvertes : étapes 2-4 (ingestion API, webscraping, stack hors-Python).
   À coller dans progress.md du projet concerné ou ouvrir ce projet en session.
2. **Créer le workspace teach** pour la vraie mission AI Engineer (repo dédié,
   `MISSION.md` à rédiger) — déclenché à la première vraie session d'apprentissage.
3. **Campagne evals A→B→A `/grill`** — 5 evals spécifiées, aucune exécutée.
4. **Campagne evals A→B→A `/adr` et `/planning`** — état inchangé.

## Écarts vs PRD

Aucun (pas de PRD pour ce projet dotfiles).

## Décisions prises

- **Pont d'état (ADR-0006) — Option A** : learning-records source unique,
  `PROGRESS.md` de coach-pedagogique conservé comme état de nature distincte
  (scaffolding-sur-livraison), pont unidirectionnel par record de synthèse.
- **dp-coach** : survit comme niche distincte (exécution+analyse déterministe
  ≠ quiz conceptuel).
- **Mécanique pont (ADR-0008)** : record proposé/copié, jamais écrit hors CWD.
- **`MEMORY.md` learning-tracker** : archivé (pas détruit) — suivi `methodology-trial`
  actif découvert à l'exécution, décision d'archivage plutôt que de destruction.
- **Best practices** : acter le verdict (conforme), pas de chantier séparé.
- **`reference/` en Markdown** (ADR-0004) : seul écart assumé au design Pocock.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-23 11:45
Session : 68f0e867-7529-4404-85a1-e7ccf74c3cc5 (grill-implementation)

## Tâches complétées

- **ADR-0003 créé et acté** (`adr/0003-grill-delegue-adr-sans-invoquer.md`,
  Accepted) : `/grill` délègue à `/adr` par instruction (jamais par invocation
  programmatique). Pour N décisions : ordre topologique, relations suggérées
  (Refines/Extends/Constrains), items autoportants, bloc copiable + invite
  visible, zéro fichier écrit. Commit `a32be56`
- **`/grill` implémentée** (`claude/commands/grill.md`) : slash-command
  user-scope, famille méthodologique `/prd`/`/planning`/`/adr`. Revue adverse
  pré-gel d'un PRD ou PLAN — parcourt l'arbre de dépendances des décisions, lève
  implicites et tensions inter-sections. Entrée `$ARGUMENTS` + fallback
  `prd.md`→`plan.md`. Stop déterministe : ledger OPEN/RESOLVED/DEFERRED, zéro
  OPEN garanti. Anti-trivialité : l'absence de section « Open questions » ne
  court-circuite pas le grill. Symlink actif + déclaré dans `install.sh`.
  Commit `cbc1ccb`
- **Corpus evals `/grill`** : 5 evals (preflight-artifact-absent,
  no-open-questions-section, deferred-branch-in-output,
  input-explicit-arg-over-fallback, output-no-file-written) +
  `setup-eval-cwd.sh` + `README.md`. Fixture `prd.md` avec contradiction
  délibérée (Contrainte hors-ligne vs critère de résumé externe). Commit `0924d56`
- **`.gitignore` : `docs/handoff/` ignoré** — handoffs = notes de travail
  jetables (précédent `AUDIT_PROGRESS.md`). Commit `5832dc4`
- **`install.sh` : parité restaurée** — `adr.md` et `planning.md` manquaient ;
  un bootstrap neuf aurait laissé `/adr` et `/planning` sans symlink. 10/10
  commands source désormais déclarées. Commit `88020d2`
- **README synchronisés avec les 10 commands réelles** — `README.md` et
  `claude/README.md` listaient 7 commands ; ajout de `adr`, `grill`, `planning`,
  compteur `(7)`→`(10)`, et note des sous-dossiers compagnons corrigée (5
  commands ont un `evals/`, seul `claude-md` a un `reference/`). Commit `7311fcc`
- **Immunisation contre l'oubli multi-fichiers** — racine commune des oublis
  `install.sh`/README de cette session et des sessions `adr`/`planning` :
  ajouter une command est un geste multi-fichiers sans checklist. Palier 1 (fait)
  : checklist « Ajouter une command » + one-liner de parité dans
  `claude/README.md`. Palier 2 (différé) : check de parité automatisé versé à
  `TODO.md`, déclenché si l'oubli se reproduit malgré la checklist. Commit
  `b5d6236`

## En cours

Rien — 8 commits committés, working tree propre (seul
`docs/rpi-audit-findings.md` reste untracked, hors périmètre).

## Prochaines étapes

1. **Campagne evals A→B→A `/grill`** — 5 evals spécifiées, aucune encore
   exécutée. Protocole : `cd ~/dotfiles/claude/commands/grill/evals &&
   ./setup-eval-cwd.sh <id>` → session B fraîche → transcription → jugement en
   session A.
2. **Fixture PLAN pour les evals `/grill`** — le corpus ne couvre que des PRD ;
   la condition d'arrêt PLAN (chaque décision archi confrontée à ≥1 alternative)
   n'a pas encore de fixture.
3. **Campagne evals A→B→A `/adr` et `/planning`** — leurs corpus sont écrits
   mais jamais exécutés (état inchangé depuis session précédente).

## Écarts vs PRD

Aucun (pas de PRD pour ce repo de configuration).

## Décisions prises

- **Nom `grill` retenu** : collision vérifiée négative — absent de `claude
  --help`, des 5 skills bundled, et des commands existantes.
- **Source de vérité réelle** : `dotfiles/claude/commands/grill.md` (pas
  `~/.claude/commands/` — correction d'une imprécision du handoff ; `~/.claude/`
  ne contient que les symlinks).
- **Portée v1 : PRD et PLAN**, une invocation = un artefact, type déduit de la
  structure du fichier résolu (pas de flag `--prd`/`--plan`).
- **Persistance de la liste de sortie : option 2** (bloc copiable + invite
  visible), pas de fichier scratch versionné — évite un artefact zombie périmé
  dès le premier `/adr` créé (cf. ADR-0003).
- **`docs/handoff/` ignoré** (pas commité) : les handoffs de conception sont des
  notes de travail jetables une fois l'implémentation terminée.
- **`install.sh` mis à jour hors périmètre `/grill`** : l'écart
  `adr.md`/`planning.md` existait avant cette session ; corrigé en commit séparé.
- **Répartition checklist vs TODO selon la nature** : la checklist d'ajout de
  command est une *convention durable* (→ `claude/README.md`, faite maintenant car
  besoin déjà prouvé) ; le check automatisé est une *évolution différée
  conditionnelle* (→ `TODO.md`, YAGNI tant que la checklist suffit). Chaque chose
  où sa nature l'appelle, pas les deux dans `TODO.md`.

## Blocages

Aucun.

---

## Dernière mise à jour
Date : 2026-06-22 16:30
Session : 73071d5c-aa41-4162-ab7f-9a05242b3df4 (fix hook block-rm-rf)

## Tâches complétées
- **Fix `claude/hooks/block-rm-rf.sh`** : le hook bloquait des commandes non-`rm`
  (`cp -r`, `ls -lr`, `sort -r`, `grep --recursive`, `echo "rm -rf"`...).
  - **Cause racine** : le scope `if: "Bash(rm *)"` est best-effort et FAIL-OPEN
    (doc Claude Code) — Claude Code lance le hook sur les commandes composites
    (pipes, `&&`, `$()`, assignations en tête) dès qu'il ne peut PAS prouver
    qu'elles ne sont pas `rm`. Le commentaire du hook (« scoped, pas besoin de
    re-vérifier que c'est un rm ») reposait sur une prémisse fausse.
  - **Cause aggravante** : l'ancien regex scannait la commande ENTIÈRE → matchait
    tout flag `r/R/f` de n'importe quelle commande + les chaînes littérales
    `--force`/`--recursive`/`rm -rf` (contenu d'arguments grep/echo).
  - **Correctif** : le hook re-vérifie qu'un mot-commande `rm` est présent (split
    sur séparateurs shell + `$()`, repère `rm`/`*/rm` après `VAR=val` et lanceurs
    sudo/xargs/...), et n'analyse que les tokens APRÈS `rm`. `settings.json`
    laissé intact (le `if:` reste un pré-filtre best-effort ; la robustesse vit
    dans le hook). Commit `4104c0b`
  - **Validé 35/35** sur le hook réel (entrée JSON stdin) : toutes les formes
    destructrices restent bloquées (`rm -rf`/`-Rf`/`--force`, `sudo`/`xargs`/`$()`
    rm -rf) ; tous les faux positifs passent (`cp -r`, `ls -lr`, `grep -rf`,
    `rmdir`, `rm.bak`).

## En cours
- Rien — fix committé (`4104c0b`), working tree propre (seul
  `docs/rpi-audit-findings.md` reste untracked).

## Prochaines étapes
- Reprise du fil principal : voir checkpoint `adr-workflow-refonte` ci-dessous
  (campagne evals A→B→A en session dédiée, etc.).

## Décisions prises
- **Re-vérifier `rm` dans le hook plutôt que durcir le `if:`** : le `if:` étant
  fail-open par conception, on ne peut pas s'y fier comme garde ; le resserrer
  n'apporterait aucune garantie. La robustesse appartient au hook (la doc
  recommande « the script does its own validation »). Ne pas cumuler les deux.
- **Scope des cas-limites** : `xargs rm -rf` / `sudo rm -rf` → bloqués (rm réel) ;
  `rmdir` / `rm.bak` / `grep -rf` → passent (`rm` n'est pas le mot-commande, ou
  `-rf` n'appartient pas à `rm`).

## Blocages
Aucun.

---

## Dernière mise à jour
Date : 2026-06-22 15:45
Session : 73071d5c-aa41-4162-ab7f-9a05242b3df4 (adr-workflow-refonte)

## Tâches complétées
- **ADR-0001 créé et acté** (`adr/0001-prd-produit-cible.md`, Accepted) : PRD =
  produit cible, frozen = baseline versionnée révisable par ADR. Premier usage réel
  de `/adr`. Commit `91396bc`
- **`/prd` aligné sur ADR-0001** : ~8 occurrences "v1" → "cible", "frozen" →
  "baseline", "Évolutions futures (v2+)" → "Au-delà de la cible", frontière
  PRD↔/planning matérialisée dans le template. Commit `6ec98a3`
- **Matrice alignée sur ADR-0001** : ligne PRD (frozen→baseline, out-of-scope v1
  →hors-cible, ajout "découpage MVP/itérations" dans "Ne contient JAMAIS"),
  règle 5 + Phase 0 reformulées. Commit `94b174f`
- **ADR-0002 créé et acté** (`adr/0002-mvp-palier-dans-plan.md`, Accepted,
  Extends ADR-0001) : MVP = palier de valeur nommé dans le PLAN (modèle C —
  PLAN unique, deux granularités : palier MVP + phase). Commit `3adf29d`
- **Matrice : frontière MVP positive** ajoutée (sous-section "Où vivent les MVP",
  ligne PLAN mise à jour avec les deux granularités, lien ADR-0002). Mentions
  "/planning à créer" et "/adr à créer" corrigées (les deux existent). Commits
  `2522e3d` + `a35b83b`
- **`/planning` aligné sur ADR-0002** : "milestone" → "palier MVP" partout
  (intro, règles, Q3, synthèse, template), lien ADR-0002, résidu "v1" corrigé
  dans le pré-flight PRD. Commit `a32a06f`
- **Evals `/planning` : drift corrigé + coverage ADR-0002** : fixture PRD du
  setup-eval-cwd.sh alignée (Périmètre cible / Hors-cible) ; nouvel eval
  `interview-mvp-tiers-vocabulary` (classe `vocabulary`) couvrant le contrat
  palier MVP. Commits `8c3b66b` + `ef02125`
- **README d'eval pour `/adr` et `/planning`** créés (calqués sur
  prd/evals/README.md, adaptés au comportement réel de chaque command :
  modes/supersession/immutabilité pour /adr ; gate semi-frozen / classe
  vocabulary / model opus pour /planning). Les deux flaggés "écrit, non
  exécuté". Commit `3aac2ed`

## En cours
- Rien — 11 commits atomiques sur main, working tree propre (seul
  `docs/rpi-audit-findings.md` reste untracked, exclu volontairement)

## Prochaines étapes
1. **[CAMPAGNE DÉDIÉE — session A neuve] Exécuter les evals `/adr` (7) et
   `/planning` (5)** via protocole A→B→A. ⚠️ GOURMAND EN CONTEXTE : A doit
   ingérer 12 transcriptions opus intégrales → une campagne complète sature une
   session A (le README /prd estime déjà 30-40 % pour 3 evals). NE PAS lancer en
   fin de session — démarrer A à 0 %. Découper en deux vagues (adr 7, puis
   planning 5), checkpoint + /clear entre les deux. Protocole détaillé dans les
   README d'eval de chaque command.
2. **Amender `planning.md` / `adr.md` si un run A→B→A révèle un gap** — les evals
   sont le juge (le vocabulaire MVP de /planning est le plus fragile, jamais
   éprouvé).
3. **README d'eval racine / index** (optionnel) : `/prd` `/claude-md` ont un
   tableau "État du corpus" ; envisager un index unique des 4 corpus si la
   duplication devient gênante.
4. Reliquat sessions précédentes : methodology-trial Phase 1a memory-grep ;
   `/immunize` inbox.

## Écarts vs PRD
Aucun (pas de PRD.md dans ce repo)

## Décisions prises
- **ADR-0001 : PRD = produit cible, frozen = baseline versionnée** (pas immuable
  au sens ADR) : révision via ADR si la cible change, édition silencieuse
  interdite. Frozen ≠ immuable : gelé contre la dérive non-tracée, pas contre
  le changement légitime.
- **ADR-0002 : MVP = palier de valeur dans le PLAN (modèle C)** : PLAN unique,
  deux granularités ("palier MVP" = livrable à valeur utilisateur ; "phase" =
  brique technique). Rejet de A (conflation milestone/MVP) et B (multi-PLAN).
  Porte de sortie vers B via futur ADR de supersession si un projet réel l'exige.
- **ADR-0002 relation : Extends ADR-0001** (étend sans contredire ; ADR-0001
  reste Accepted intouché — ce n'est pas une supersession).
- **"frozen" redéfini comme baseline** : la matrice, /prd et /planning utilisent
  maintenant "baseline révisable par ADR" au lieu de "frozen" ou "gelé" — levée
  de l'ambiguïté immuable vs versionnée.
- **Classe d'eval `vocabulary` créée** pour /planning : teste le vocabulaire
  produit (palier MVP vs milestone), distinct de `interview_cap` (qui teste le
  plafond de questions). Doctrine d'émergence respectée — classe née d'un besoin
  réel (ADR-0002), pas par anticipation.
- **Ordre canonique de replanning respecté à chaque étape** : ADR → document
  cible → outil → eval. Deux chaînes complètes dans la session.

## Blocages
Aucun.

---

## Dernière mise à jour
Date : 2026-06-22 11:20
Session : 42307f88-526d-4e04-b0a1-d834575ee902 (enhance-workflow)

## Tâches complétées
- **Matrice de responsabilité documentaire déplacée vers emplacement canonique** : `docs/responsability-matrix.md` (vide, mal placé, mal orthographié) → `docs/methodology/responsibility-matrix.md`. Cohérence vérifiée avec CLAUDE.md + planning.md + auto-référence de la matrice. Commit `8c03a2e`
- **Convention ADR ajoutée** (`docs/methodology/conventions/adr.md`) : satellite de la matrice — immuabilité corps / mutabilité statut, 5 relations inter-ADR, numérotation. Commit `7e48387`
- **Section "Documentary Methodology" reformulée** dans claude/CLAUDE.md : la matrice est référence conceptuelle (pas Read runtime obligatoire) ; lecture runtime seulement au replanning Phase 3. Commit `2c9ddfe`
- **Commande `/planning` créée et rendue invocable** (symlink runtime manquant ajouté). Commit `10504d5`
- **`/prd` refactorée** : découpage en phases retiré du PRD (migré vers /planning), renumérotation Risques/Critères. Commit `4a851e9`
- **Commande `/adr` créée** (option 2 : création + supersession bidirectionnelle ; mode argument `--from-context` ; aucune trace de source dans l'artefact) + corpus 7 evals. Test-first respecté (evals validés avant code). Commit `fce314a`
- **Corpus 4 evals `/planning`** (bootstrap minimal, doctrine d'émergence) : gate, pré-flight PRD-absent/nominal, interview_cap. Commit `7de32b5`
- **Exemption direct-sur-main déclarée** : `~/dotfiles/CLAUDE.md` créé (manquait), désambiguïsé du payload `claude/CLAUDE.md`. Commit `1fab091`

## En cours
- Rien — 8 commits atomiques sur main, working tree propre (seul `docs/rpi-audit-findings.md` reste untracked, exclu volontairement)

## Prochaines étapes
1. **[CHANTIER DÉDIÉ — session vierge] Refonte conceptuelle PRD = produit cible** (et non PRD=v1). Décision de fond prise cette session, NON encore implémentée. ORDRE IMPOSÉ par la méthodo : (a) écrire un ADR actant le passage PRD=v1 → PRD=cible + conséquences sur le `frozen` et le découpage ; (b) SEULEMENT ensuite amender prd.md (~10 occurrences "v1") + matrice. Premier vrai cas d'usage de `/adr`.
2. **Exécuter les evals `/adr` (7) et `/planning` (4)** via protocole A→B→A — nécessite sessions B vierges + humain comme canal. Les deux commandes sont écrites/spécifiées mais PAS exécutées contre leur corpus.
3. **README d'eval pour `/adr` et `/planning`** (calqué sur prd/evals/README.md : doctrine + protocole + état du corpus). Absent pour les deux.
4. **Combler le trou v1→v2 dans la matrice** — sera traité par la refonte (étape 1) ou ratifié séparément.
5. Reliquat session précédente : methodology-trial Phase 1a memory-grep ; `/immunize` inbox.

## Écarts vs PRD
Aucun (pas de PRD.md dans ce repo)

## Décisions prises
- **Matrice : emplacement canonique** `docs/methodology/responsibility-matrix.md` (sous-dossier methodology/ + orthographe responsi-bility)
- **Rôle de la matrice** : référence conceptuelle dont les commandes dérivent leurs règles (prompts autonomes), PAS un Read runtime obligatoire ; Read seulement au replanning Phase 3
- **`/adr` périmètre** : option 2 (création + supersession bidirectionnelle), PAS option 3 (cycle complet) — le trivial (Status Accepted/Deprecated) reste manuel ; Simplicity First
- **`/adr` mode selon source** : argument explicite `--from-context` (déterminisme > détection floue), PAS auto-détection
- **`/adr` trace de source** : AUCUNE dans l'artefact (overlap avec git blame ; donnée fausse-par-construction si co-décision ; zone immuable)
- **Workflow dotfiles** : exemption direct-sur-main inconditionnelle (mono-user, pas de CI ; garde-fou = rituel evals, pas topologie git) — option 1, déterminisme
- **Evals = mécanisme de test des slash-commands** (Evaluation-Driven Development, Anthropic) : contrat comportemental observable, protocole A→B→A. C'est l'équivalent test-first pour un artefact-prompt
- **`/planning` bootstrap 4 evals** : protéger le fragile (interview_cap, attesté fragile par lesson one-question-at-a-time), pas l'important-mais-blindé (scope_guard, doublement défendu dans le prompt) — doctrine d'émergence
- **DÉCISION DE FOND (à instruire par ADR avant implémentation) : PRD = produit cible, MVP = itérations successives.** Colle au réel (client exprime besoin → PRD interprète → MVP raisonnables planifiés). Conséquences à peser : déstabilise le `frozen` du PRD, repose la question du document-par-itération.

## Blocages
Aucun. Note : la refonte PRD=cible (étape 1) est volontairement différée en session dédiée — pas un blocage, un séquençage discipliné (un concept à la fois).

---

## Dernière mise à jour
Date : 2026-05-27
Session : 638ff394-772d-467a-8266-5a8553a65dac (karpathy-inspired-guidelines)

## Tâches complétées
- **Évaluation comparative Karpathy vs Shanraisshan** : analyse méticuleuse des deux repos, verdict — Karpathy comme boussole conceptuelle, Shanraisshan comme auditeur d'implémentation (rôles distincts, non concurrents)
- **Présentation des 4 principes Karpathy** un par un avec exemples EXAMPLES.md : Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution
- **Décision d'intégration** : 4 principes en synergie (pas extraction partielle), option A (section dans CLAUDE.md user), format D1 distillé, position L1 entre State Verification et Global Do NOT
- **Uniformisation CLAUDE.md en anglais** : décision d'homogénéiser la langue (meilleur alignement training distribution modèle), traduction des 3 "Global Do NOT" existants avec relecture critique de chaque formulation
- **Intégration Karpathy dans CLAUDE.md user** : section "Coding Discipline (Karpathy)" ajoutée, 4 principes annotés `adopted 2026-05-27`, commit `3ec0bfe` poussé
- **Audit de conformité HumanLayer** : confrontation du CLAUDE.md résultant aux best practices humanlayer.dev — score 6/6, seule réserve actionnable = ligne 15 (état transitoire /pr skill)
- **Ajout section "Version Control"** : 3 règles (conventional commits + pre-commit, atomic granularity, branch workflow + distinguo complexe vs perso), déménagement de la ligne Conventional Commits hors Communication, commit `1031427` poussé
- **Ajout règle Test-first** dans Coding Discipline (Karpathy) : règle opérationnelle dérivée de Goal-Driven Execution, spécifique à Claude en tant qu'agent (user reste test-after), périmètre d'exemption explicité (scripts, exploration, config, docs), commit `1031427` poussé
- **Retrait ligne /pr "workflow under finalization"** du CLAUDE.md user (anti-pattern HumanLayer : état transitoire consomme attention permanente)
- **TODO.md enrichi** : enrichissement (β) entrée "Migrer PR template" pour couvrir aussi la skill `/pr` + ajout nouvelle entrée "Audit mettre de l'ordre dans le workflow agentique" avec condition de déclenchement (stabilité workflow, pas date), commit `70ef137` poussé

## En cours
- Rien — session clôturée proprement

## Prochaines étapes
1. **Finaliser le workflow agentique** (PR template, ADR, éléments workflow CLI à arbitrer) — condition de déclenchement pour l'audit TODO
2. **Créer skill `/pr`** une fois les 3 questions structurantes tranchées (où vivent ADR, quels artefacts en PR, template fixe vs modulaire) — cf. TODO.md entrée "Migrer PR template + skill /pr"
3. **Reprendre methodology-trial** : Phase 1a implémentation memory-grep (priorité non négociable avant Étape 2) — cf. progress.md entrée 2026-04-28
4. **Audit workflow agentique** après finalisation — cf. TODO.md entrée "Audit mettre de l'ordre"
5. **`/immunize`** à la prochaine passe (inbox en attente)

## Écarts vs PRD
Aucun (pas de PRD.md dans ce repo)

## Décisions prises
- Karpathy comme boussole conceptuelle (4 principes en synergie), Shanraisshan comme auditeur d'implémentation — rôles distincts
- CLAUDE.md user uniformisé en anglais (format natif modèle, meilleur alignement)
- Section "Coding Discipline (Karpathy)" : option A (dans CLAUDE.md), format D1 distillé, position L1
- Règle Test-first spécifique à Claude agent (user reste test-after) : option A (ligne dans CLAUDE.md user, dérivée de Karpathy 4)
- Section "Version Control" en position L1 (entre Communication et Session Discipline)
- Politique de tests : scope projet uniquement (Karpathy 4 couvre l'universel)
- Report skill `/pr` : workflow pas encore finalisé, créer la skill avant stabilisation ancrerait les décisions provisoires — audit post-finalisation
- TODO.md : fusion β (entrée PR template + skill `/pr` sous un item) + entrée audit séparée

## Blocages
Aucun

---

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

**Discipline anti-procrastination** : memory-grep doit être FINALISÉ (atteindre seuil de valeur, pas dogmatiquement exécuter PRD ligne par ligne) avant toute préparation skill-eval-runner. Comparer 2 projets terminés > comparer 1 demi-livrable + 1 nouveau projet.

1. **Étape 1 finalisation memory-grep** — non négociable avant pivot Étape 2 :
   - Phase 1a (squelette + scan + smoke test) côté ~/projects/memory-grep
   - Phase 1b (frontmatter parsing) — pain point originel
   - Phase 2 (output enrichi) — usage quotidien
   - **Retro post-Phase 2** : Phase 3 polish vaut-elle l'effort ou reportée ? Décision tranchée et tracée dans progress.md memory-grep
   - Phase 3 (polish) ou marquer "reportée" selon retro
2. **Préparation pré-`/prd` skill-eval-runner** :
   - Première tâche d'observation : lancer `claude -p "drill me on Python list comprehensions"` → observer sortie brute → décider stratégie détection triggering. **Ne pas lancer `/prd` avant.**
   - Corriger pitch sur 3 points : (a) supprimer "Stack imposée" → référence CLAUDE.md memory-grep + délibération via `/prd` Phase 2, (b) corriger volumétrie ~3h36/cycle, (c) trancher Cruft vs uv init manuel
3. **Étape 2 — `skill-eval-runner`** : `/prd` → `/claude-md` → implémentation (audit A→B→A si appétit)
4. **Étape 3 candidate — `prompt-companion`** (NotebookLM helper) : archétype I/O réseau + état + clipboard + interview interactive
5. **Étape 4 candidate — `ai-models-watcher`** ou pivot selon évolution
6. **Étape 5 (recommandé) — projet stress-test généralisabilité** hors-archétype Python CLI single-user (Go/Rust ou service longue durée API multi-component) — préserve hybride 60/40
7. **Audit cross-CLAUDE.md** (action correctrice friction #1 du 2026-04-28) : grep `.claudeignore` + `gitignore.*aware` sur tous les CLAUDE.md du repo
8. **`/immunize` à la prochaine passe** : inbox 6 entrées — surveiller récurrence
9. **`/insights` exploitable** : après finalisation memory-grep + skill-eval-runner (corpus de sessions de build suffisant)

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
