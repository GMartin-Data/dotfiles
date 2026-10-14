## Dernière mise à jour
Date : 2026-10-14 12:01
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

---

## Checkpoint précédent — 2026-10-11 22:57
Session : 5de2980a-ab5e-44ad-8a90-634ef8ddacde

## Tâches complétées

- **Revue de la PR serveur #3** (`/code-review 3 high`, session neuve CWD
  serveur, puis triage ici, un finding par tour) : 4 findings, 4 traités, 0
  écarté. [1] MEDIUM placeholder `.env.example` valide → vide, fail-closed
  (`31a9ad7`, message amendé sans trailers d'attribution, push forcé par Greg) ;
  [2] alias ASGI → `starlette.types` (`d5efb8b`) ; [3] warning de token absent
  déplacé au scope `lifespan`, jamais envoyé en stdio, 2 tests (`f6999f7`) ;
  [4] ADR → pas de nouvel ADR, pointeur README (`562bb68`).
- **PR #3 mergée** (`b9b4c31`, merge commit, branche conservée), corps mis à jour
  (test plan 107 tests, table de revue). GitGuardian vert.
- **Cloud Run redéployé** : révision `00013-twd` = `main` (401 sans en-tête,
  401 mauvais token, 200 bon token ; variables intactes ; aucun faux warning).
- **ADR-0017** : option G (OAuth MCP) ajoutée, rejetée, avec déclencheur de
  réouverture (`639ba6d`) ; puis `Proposed` → **`Accepted`** (`83f94bd`).
- **Rotation `YOUTUBE_API_KEY` faite** : nouvelle clé « tech-watch-mcp
  2026-10-11 » (restreinte à YouTube Data API v3) dans `youtube-tech-scraper`,
  révision `00014-2gv` ; empreintes des deux révisions différentes et non
  vides ; smoke test MCP vert avec l'ancienne clé supprimée ; « API key 1 »
  supprimée. Valeur jamais passée par le chat.
- Aucune PR ouverte ; `~/mcp-server-code` et `~/dotfiles` sur `main`,
  synchronisés avec `origin`, arbres propres.

## En cours

- Rien.

## Prochaines étapes

1. **Première veille réelle** en session interactive, depuis un terminal neuf
   (`TECH_WATCH_MCP_TOKEN` sourcée) : observer l'héritage de
   `Edit(~/tech-watch/**)` par le fork (sinon `permissionMode: acceptEdits`
   dans l'agent) et que l'en-tête s'arrête à `**Notes**:` (finding [2] de la
   PR #6, non rejoué).
2. **Autre machine** : `git pull`, `install.sh` (purge des trois liens morts),
   `~/.zshrc.local` (mode 600) avec `export TECH_WATCH_MCP_TOKEN=…`, valeur lue
   dans un terminal de la machine actuelle — jamais via le chat ni
   `gcloud … describe`.
3. **Points pour Greg** (`plan.md` §5 Phase 4), de préférence après la veille
   réelle : dates sans année (`check-dates.py` les montre en `fetched-noyear`,
   statu quo ou `unverified`) ; égalités sans signal d'engagement ; `Owner
   domains` sans propriétaire.
4. Cycle `/insights` du 2026-10-26 et items dormants :
   `tasks/insights-actions.md`.

## Écarts vs PRD

- Aucun (pas de PRD, repo dotfiles). L'écart au plan consigné en §5 Phase 4
  (« `/code-review` sur les deux branches ») est résolu : la branche serveur a
  eu sa revue.

## Décisions prises

- **Bearer sur le serveur MCP tech-watch + passerelle stdio** → `adr/0017`
  (Accepted 2026-10-11). Option G (OAuth MCP) rejetée dans le même ADR, perte du
  connecteur claude.ai assumée comme durable, déclencheur de réouverture nommé.
- Track léger, sans ADR — décisions Greg du 2026-10-11 :
  - finding [1] : placeholder vide, sans longueur minimale de token dans le
    middleware (règle spéculative) ;
  - finding [2] : correctif dans la PR plutôt que renvoi à `/simplify` ;
  - finding [3] : warning au `lifespan` (variante retenue plutôt que simple note
    de docstring) ;
  - finding [4] : durable + G rejetée, pas de nouvel ADR ;
  - redéploiement de `main` (option b) plutôt que laisser la prod sur
    `512773e` ;
  - rotation `YOUTUBE_API_KEY` faite le jour même (alternative « acter
    l'exposition » écartée) ; fenêtre de logs fuités : purge au plus tard le
    2026-11-08 (rétention `_Default` 30 jours).
- **Claude, signalée** : un commit a reçu des trailers d'attribution
  contraires à la règle mémoire « No Co-Authored-By » ; corrigé par amend, push
  forcé fait par Greg (le hook `block-force-push` bloque Claude). Brouillon de
  feedback mis en file locale (`/feedback`).

## Blocages

- Aucun.
