## Dernière mise à jour
Date : 2026-10-26 08:57
Session : b905eafa-527b-4718-be1e-80446a0a5fd1

## Tâches complétées

- **Cycle /insights 2026-10-26 fait** (rapport
  `~/.claude/usage-data/report-2026-10-26-075720.html`, 48 sessions
  analysées sur 64, fenêtre 25/09 → 26/10), protocole v3, un point par
  tour :
  - fiche `check-before-delivery` **validée à n = 1** (une seule session
    `/teach` après le fix, Go leçon 0001 du 21/10, ligne `Checked:` présente
    avec 4 corrections, zéro correction utilisateur, leçon non encore
    exercée) ; `/immunize` de « forme > prohibition » reporté au 26/11 ;
  - roadmap hors repo : §6 P4 « archivé, n = 0 », T3 et ligne §3 alignées ;
  - option `candide-*` (~1,7 $) retirée de l'agenda → event-driven ; règle 7
    actée à n = 1 dans le seul README de `claude-md-skill` ;
  - ratio méta/produit : **46 % des tokens de sortie** (vs 28 %), signal muet
    car un chantier méta ouvert à chaque cycle ; condition conservée telle
    quelle ;
  - scoring 3 axes de 10 candidats, règle « une seule action » contestée
    (trois candidats à coût 1) puis confirmée ; **action unique S1** :
    `"attribution": false` dans `claude/settings.json`, test A/B en bac à
    sable concluant (trailer présent sans setting, absent avec ; l'instruction
    injectée bascule à chaud). Fiche `attribution-setting`, revue le
    2026-11-26.
  - Issue #7 fermée.
- **Cinq commits poussés** sur `main` (`131e073` → `fb00606`) : synthèse
  mods et checkpoint du 14/10 jamais poussés, setting d'attribution, cycle
  /insights, leçon inbox ADR-0008 venue de learning-dlt.
- Mémoire : `feedback_no_coauthor` pointe vers le setting ; mémoire roadmap
  et index mis à jour (§6 corrigé).

## En cours

- **Chantier mods ouvert, aucun code écrit** : premier mod = registre de
  contexte (observe-only, JSONL par session + script d'analyse pour
  `/insights`), sous `/coach-pedagogique`. Spec v0 dans
  `tasks/mods-2026-10/synthese.md` §8.
- `tasks/lessons-inbox.md` : une entrée à n = 1 (ADR-0008 ne couvre pas le
  workspace teach en CWD, dérogation learning-dlt), à trier au prochain
  `/immunize`.

## Prochaines étapes

1. **Branche `feat/context-ledger-mod`**, puis `/coach-pedagogique` avec le
   registre comme artefact. Premier tour du coach : objectif d'apprentissage
   (modèle événements / `$` / `next` / pinned / fail-open, pas les noms de
   champs) et calibrage du scaffolding selon l'aisance TypeScript (si bases à
   acquérir : `/teach` court avant). Optionnel avant : 30 min de
   `code-mentor` sur `examples/tool-call.ts` de la skill bundled
   `plugin-authoring`.
2. L'étape 1-2 du coach produit **`tasks/mods-2026-10/plan.md`** (paliers
   M0–M6, un critère de vérification par palier) **avant** tout fichier dans
   `claude/mods/`. Décisions à y prendre : mécanisme de chargement définitif
   (dossier de skills auto-chargé, `CLAUDE_CODE_PLUGIN_DIRS`, marketplace
   dossier — candidat ADR si 4ᵉ famille dans `install.sh` / README),
   emplacement du script d'analyse, chemin du JSONL (à côté de
   `~/.claude/usage-data/session-meta/` ?). Dev loop : `claude --plugin-dir
   ~/dotfiles/claude/mods/context-ledger`, pas le dossier `dev-mods`.
3. Rituel : `claude plugin test` + un run réel vérifié contre le JSONL ;
   `/code-review` sur le diff avant PR ; checklist multi-fichiers (famille
   `**Mods**` à créer dans les deux README) ; `validate` + `tsc` à chaque bump
   nocturne de Claude Code.
4. **Second mod, une autre semaine** : rédaction des secrets dans les
   résultats d'outils (incident 2026-10-11), spec dans la synthèse §5.
5. **Autre machine** : `git pull`, `install.sh` (purge des trois liens morts),
   `~/.zshrc.local` (mode 600) avec `export TECH_WATCH_MCP_TOKEN=…`, valeur
   lue dans un terminal de la machine actuelle — jamais via le chat ni
   `gcloud … describe`. Le setting `attribution: false` y arrive par le pull.
6. **Points tech-watch pour Greg** (`plan.md` §5 Phase 4) : dates sans année,
   égalités sans signal d'engagement, `Owner domains` sans propriétaire ;
   budget de 10 pages à mesurer sur deux ou trois sujets avant de toucher au
   seuil.
7. **Purge des logs fuités** (`YOUTUBE_API_KEY` ancienne, révisions ≤ `00008`)
   : effective au plus tard le 2026-11-08 ; vérification facultative après.
8. Cycle `/insights` du 2026-11-26 : item 1 de l'ordre du jour reconduit dans
   `tasks/insights-actions.md` (revue `attribution-setting`, `/immunize`
   « forme > prohibition » après deux ou trois leçons Go, constat 1 de
   `TODO.md` à fermer par renvoi au déclencheur mods, ratio à remesurer).

## Écarts vs PRD

- Aucun (pas de PRD, repo dotfiles).

## Décisions prises

- Track léger, sans ADR — cycle /insights du 2026-10-26 :
  - **Greg** : `check-before-delivery` validée à n = 1 avec réserve,
    `/immunize` reporté au 26/11 ; condition du signal méta/produit laissée
    telle quelle (compte de chantiers par cycle proposé, non retenu).
  - **Greg** : option `candide-*` non dépensée → event-driven ; règle 7 actée
    sans généralisation ; ligne §3 de la roadmap rayée.
  - **Greg** : règle « une seule action » maintenue après contestation ;
    **Claude** : l'amendement « une comportementale + une mécanique
    vérifiable le jour même » formulé, non adopté faute de cas (B1 et D ne
    tenaient pas au scoring : impact surnoté).
  - **Greg** : S1 setting plutôt que hook F1 (supprimer la cause, pas
    intercepter l'effet ; un seul mécanisme par règle). G (`/review-fix`) et
    H (rejeu headless) non retenus : boucle déjà encodée trois fois / chantier
    fermé, coût 3 ; conservés en event-driven avec déclencheur nommé.
  - **Claude, signalée** : facets et session-meta de `~/.claude/usage-data/`
    conservent des sessions de septembre dont les transcripts sont purgés ;
    la revue d'une fiche ne peut s'appuyer que sur les transcripts encore
    présents. Les 16 sessions `dbt-agent-testbed` sont des micro-tests
    (0,02 M tokens) : la lecture en tokens du ratio est la fiable.

## Blocages

- Aucun.

---

## Checkpoint précédent — 2026-10-14 12:01
Session : e8a211f1-b4e7-4c9e-85c2-fde9927c8923

## Tâches complétées

- **Étude des mods Claude Code** (veille du 12/10, skill bundled
  `plugin-authoring`, types `claude-code.d.ts` lus sur deux builds — 2.1.296
  le 13/10, 2.1.299 le 14/10 après mise à jour automatique nocturne, +556
  lignes) : anatomie, chargement, modèle d'événements, outillage
  (`validate`, `tsc`, `test`), fail-open, limites de dessin. Sept candidats
  évalués avec la grille I/C/R/déclencheur de `TODO.md`, scores valeur /
  complexité 1-10. Ce que les mods voient et contrôlent du contexte
  (`session.append`, `session.measure`, `$.session.usage({ breakdown })`,
  `session.compact`, `turn.step`) et trois limites (pas de fenêtrage par
  requête, compaction maison vs preserved thinking non prouvé, estimations).
  Livrable : **`tasks/mods-2026-10/synthese.md`** (8 sections, spec v0 du
  registre en §8).
- Brainstorming hors mods (structured outputs, idées de projets, deep
  research Jev) mené puis **non conservé** à la demande de Greg : deux notes
  `tasks/` supprimées avant commit.
- Rien écrit dans `~/.claude/dev-mods/` ; aucune question de hot-reload
  posée malgré deux chargements de `plugin-authoring`.
- `~/dotfiles` sur `main`, propre après commit de la synthèse et de ce
  checkpoint.

## En cours

- **Chantier mods ouvert** : premier mod = **registre de contexte**
  (observe-only, JSONL par session + script d'analyse pour `/insights`),
  mené sous `/coach-pedagogique` avec l'appropriation des mods comme
  objectif explicite. Aucun code écrit ; spec v0 dans la synthèse §8.

## Prochaines étapes

1. **Branche `feat/context-ledger-mod`** pour le code (docs déjà commitées
   sur `main`).
2. **Session suivante** : `/catchup` → lire `tasks/mods-2026-10/synthese.md`
   (§8) → optionnel : 30 min de `code-mentor` sur `examples/tool-call.ts` de
   la skill bundled `plugin-authoring` → `/coach-pedagogique` avec le registre
   comme artefact. Premier tour du coach : formuler l'objectif d'apprentissage
   (le modèle événements / `$` / `next` / pinned / fail-open, pas les noms de
   champs, périssables) et calibrer le niveau de scaffolding selon
   l'aisance en TypeScript (si bases TS à acquérir : `/teach` court avant).
3. L'étape 1-2 du coach produit **`tasks/mods-2026-10/plan.md`** (paliers
   M0–M6 de la spec v0, un critère de vérification par palier) **avant** tout
   fichier dans `claude/mods/`. Décisions à y prendre : mécanisme de
   chargement définitif (dossier de skills auto-chargé, `CLAUDE_CODE_PLUGIN_DIRS`,
   marketplace dossier — candidat ADR si 4ᵉ famille dans `install.sh` /
   README), emplacement du script d'analyse, chemin du JSONL (à côté de
   `~/.claude/usage-data/session-meta/` ?). Dev loop : `claude --plugin-dir
   ~/dotfiles/claude/mods/context-ledger`, pas le dossier `dev-mods`.
4. Rituel : `claude plugin test` + un run réel vérifié contre le JSONL ;
   `/code-review` sur le diff avant PR ; checklist multi-fichiers (famille
   `**Mods**` à créer dans les deux README).
5. **Second mod, une autre semaine** : rédaction des secrets dans les
   résultats d'outils (incident 2026-10-11, `session.append` porte
   `tool-result`, `$.env.get`), spec dans la synthèse §5.
6. **Autre machine** : `git pull`, `install.sh` (purge des trois liens morts),
   `~/.zshrc.local` (mode 600) avec `export TECH_WATCH_MCP_TOKEN=…`, valeur
   lue dans un terminal de la machine actuelle — jamais via le chat ni
   `gcloud … describe`.
7. **Points tech-watch pour Greg**, laissés en suspens par décision du 13/10
   (`plan.md` §5 Phase 4) : dates sans année, égalités sans signal
   d'engagement, `Owner domains` sans propriétaire ; budget de 10 pages à
   mesurer sur deux ou trois sujets avant de toucher au seuil.
8. **Purge des logs fuités** (`YOUTUBE_API_KEY` ancienne, révisions ≤ `00008`)
   : effective au plus tard le 2026-11-08 ; vérification facultative après.
9. Cycle `/insights` du 2026-10-26 (`tasks/insights-actions.md`) : remesurer
   le ratio méta/produit **avec le chantier mods déclaré ouvert**.

## Écarts vs PRD

- Aucun (pas de PRD, repo dotfiles).

## Décisions prises

- Track léger, sans ADR — session 2026-10-13/14 :
  - **Greg** : premier mod = registre de contexte, malgré une valeur
    estimée 3/10 aujourd'hui (6 si runs longs autonomes ; complexité 5) —
    choix assumé comme véhicule d'appropriation des mods et prérequis de
    toute automatisation de contexte ; déclencheur assumé = le premier run
    long planifié, pas une friction.
  - **Greg** : approche pédagogique (implémenter en s'appropriant) plutôt
    que livraison directe ; **Claude, acceptée** : instrument =
    `/coach-pedagogique` (niche « livraison d'un vrai artefact par
    scaffolding ») et non `/teach`.
  - **Greg** : brainstorming hors mods non conservé ; **Claude** : les deux
    notes supprimées, leur part mods reversée dans la synthèse.
  - **Claude, signalées** : mods de contrôle (taille des résultats
    d'outils, compaction maison) **seulement armés par une mesure du
    registre** ; règle de conception pour toute automatisation future
    « un run = un contexte, état transmis par fichier ou sortie structurée »
    à consigner dans un CLAUDE.md ou un plan, pas dans un mod ; dérive d'API
    constatée (bump nocturne) → `validate` + `tsc` à chaque bump.
  - Déclencheurs de réouverture (synthèse §7) : 2ᵉ oubli de `/progress`
    avant `/clear` → mod `command.run` ; sortie de l'early access → migration
    des guards réévaluée ; première friction de contexte → mods de contrôle.

## Blocages

- Aucun.

---

## Checkpoint précédent — 2026-10-12 15:39
Session : 0a5fa4bd-f832-46dc-af93-22fcefa3c3d6

## Tâches complétées

- **Première veille réelle faite** : `/tech-watch "Claude Code mods"` en session
  interactive, terminal neuf, `TECH_WATCH_MCP_TOKEN` sourcée, passerelle stdio
  avec bearer. Rapport :
  `~/tech-watch/tech-watch-claude-code-mods-2026-10-12.md` (216 lignes, 20
  classées + 3 primaires, 6 Essential, ~7,5 min, 65 k tokens côté fork,
  21 appels d'outils). arXiv vide (attendu), Tier 3 non lancé (53 uniques ≥
  seuil 12), 10/10 pages ouvertes, 13 pages web `unverified` (budget épuisé +
  un 403 Medium), StationX lu tronqué.
- **Observation 1 confirmée** : l'en-tête s'arrête à `**Notes**:` puis `---`
  (finding [2] de la PR #6, validé par un run réel).
- **Observation 2 sans symptôme** : le fork a écrit dans `~/tech-watch/` sans
  demande de permission remontée ni blocage. Le mécanisme (règle
  `Edit(~/tech-watch/**)` héritée ou autre chemin d'auto-approbation) n'est pas
  distingué, mais `permissionMode: acceptEdits` dans l'agent n'est pas
  nécessaire.
- `~/dotfiles` sur `main`, propre, synchronisé avec `origin` ; aucune PR
  ouverte.

## En cours

- Rien.

## Prochaines étapes

1. **Autre machine** : `git pull`, `install.sh` (purge des trois liens morts),
   `~/.zshrc.local` (mode 600) avec `export TECH_WATCH_MCP_TOKEN=…`, valeur lue
   dans un terminal de la machine actuelle — jamais via le chat ni
   `gcloud … describe`.
2. **Points pour Greg** (`plan.md` §5 Phase 4), maintenant qu'une veille réelle
   existe pour les illustrer : dates sans année (le run a lu « Oct 4 » dev.to
   comme 2026 en le justifiant dans les Notes — statu quo, règle à trancher :
   statu quo ou `unverified`) ; égalités sans signal d'engagement ; `Owner
   domains` sans propriétaire.
3. **Budget de 10 pages** : 13 pages web laissées `unverified` sur ce sujet
   dense. Friction à mesurer sur deux ou trois sujets différents avant de
   toucher au seuil — pas d'action maintenant.
4. **Purge des logs fuités** (`YOUTUBE_API_KEY` ancienne, révisions ≤ `00008`
   du serveur) : effective au plus tard le 2026-11-08 par rétention `_Default`
   30 jours ; rien à faire sauf vérification facultative après cette date.
5. Cycle `/insights` du 2026-10-26 et items dormants :
   `tasks/insights-actions.md`.

## Écarts vs PRD

- Aucun (pas de PRD, repo dotfiles).

## Décisions prises

- Track léger, sans ADR — session 2026-10-12 :
  - **Greg** : sujet de la première veille réelle = « Claude Code mods » ;
    checkpoint direct sans revue du top 6 Essential en chat.
  - **Claude, signalée** : observation 2 déclarée « sans symptôme » plutôt que
    « confirmée » — l'héritage de la règle `Edit(…)` par le fork n'est pas
    prouvé, seule l'absence du symptôme redouté l'est.

## Blocages

- Aucun.
