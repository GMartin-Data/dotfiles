## Dernière mise à jour
Date : 2026-10-11 22:57
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

---

## Checkpoint précédent — 2026-10-11 12:09
Session : 9820e7b9-f865-4bf1-8453-ee0d6b924790

## Tâches complétées

- **Chantier tech-watch clos — PR #6 mergée** (`0b5d243`, merge commit, branche
  distante conservée comme pour la PR #5) ; `plan.md` §5 « Phase 4 — Clôture »
  écrite et poussée sur `main` (`353f312`).
- **`/code-review 6 high`** (skill user-scope, session neuve) : 10 findings,
  triés un par tour, 9 traités en 10 commits, 1 écarté (note historique de
  `claude/evals/claude-md/README.md`, décision du matin). Détail et commits :
  `plan.md` §5 Phase 4 et corps de la PR #6.
- **Finding [1] HIGH clos de bout en bout** : endpoint Cloud Run `allUsers`
  sans auth, URL versionnée dans un repo public (~108 cloneurs uniques en 14
  jours). Décision du matin « acter + borner » (`max-instances` 20 → 2, alerte
  budget 10 €/mois, API Budgets activée) dépassée le jour même par le
  **bearer** : serveur `utils/auth.py` fail-closed (105 tests, révisions
  `00011` puis `00012` après rotation), agent en passerelle stdio `uvx
  mcp-proxy@0.13.0` avec `API_ACCESS_TOKEN` depuis `TECH_WATCH_MCP_TOKEN`
  (`~/.zshrc.local`, 600, sourcé par `zsh/.zshrc`). → `adr/0017`.
  Vérifié : `curl` 401/200, sondes K12 avec/sans token et `down`, E1 complet à
  travers la passerelle identique au rejeu final (0,86 $). Addendum daté dans
  `phase3/K12-probe-2026-10-10.md`.
- **Serveur** : branche `feat/bearer-auth` poussée, **PR #3 en brouillon**
  (https://github.com/GMartin-Data/tech-watch-mcp/pull/3), code déjà en
  production.
- **Incident** : première valeur du token affichée par erreur dans deux
  sorties de commande de la session (expansion `${VAR:-…}`, puis `ps`) ;
  token tourné aussitôt E1 terminé, ancienne valeur morte (401).
- Machine courante : `~/.zshrc.local` créé ; `install.sh` rejoué (purge
  vérifiée sur un lien mort planté, un lien étranger conservé, 29 liens sains).

## En cours

- Rien. La revue de la PR serveur #3 s'ouvre dans une session neuve, CWD
  `~/mcp-server-code` (cible `3` résolue par `gh` dans le repo courant).

## Prochaines étapes

1. **Session neuve dans `~/mcp-server-code`** : `/code-review 3 high`, triage,
   `gh pr ready 3`, merge ; puis `git pull` et vérifier que la révision Cloud
   Run `00012` correspond bien à `main`.
2. **ADR-0017** : passer `Status: Proposed` → `Accepted` (date, porte franchie :
   PR #6 mergée, E1 vert à travers la passerelle).
3. **Première veille réelle** en session interactive, depuis un terminal neuf
   (variable `TECH_WATCH_MCP_TOKEN` sourcée) : observer l'héritage de
   `Edit(~/tech-watch/**)` par le fork (sinon `permissionMode: acceptEdits`
   dans l'agent) et que l'en-tête s'arrête à `**Notes**:` (finding [2], non
   rejoué).
4. **Autre machine** : `git pull`, `install.sh` (purge des trois liens morts),
   `~/.zshrc.local` avec le token (README racine, « À réinstaller
   manuellement »).
5. Points pour Greg (`plan.md` §5 Phase 4) : règle des dates sans année
   (`check-dates.py` les montre en `fetched-noyear`, statu quo ou
   `unverified`) ; égalités sans signal d'engagement ; `Owner domains` sans
   propriétaire ; rotation de `YOUTUBE_API_KEY` (logs des révisions ≤ `00008`).
6. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- Aucun (pas de PRD, repo dotfiles). Écart au plan, consigné en §5 Phase 4 :
  « `/code-review` sur les deux branches » — la branche serveur née de la revue
  (`feat/bearer-auth`, PR #3) attend la sienne.

## Décisions prises

- **Bearer sur le serveur MCP tech-watch + passerelle stdio dans l'agent**
  → `adr/0017` (Proposed). Décision intermédiaire « acter + borner » non écrite,
  ses mitigations conservées en défense en profondeur.
- Track léger, sans ADR — décisions Greg du 2026-10-11 (triage) :
  - finding [3] : ligne d'autorité « non établie = C » dans la grille plutôt
    qu'une exclusion hors score ;
  - finding [6] : purge ciblée dans `install.sh` plutôt qu'une recette
    documentée ;
  - finding [10] : note historique conservée (décision du matin maintenue) ;
  - revue de la PR serveur #3 dans une session neuve, CWD serveur.
- **Claude, signalées** : pas de rejeu pour les correctifs de libellé ([2],
  [3], [7], [8]), à vérifier au prochain run complet ; `check-dates.py`
  signale `fetched-noyear` sans échouer, la règle reste à Greg.

## Blocages

- Aucun côté chantier. Hors chantier : rotation de `YOUTUBE_API_KEY` à la main
  de Greg (le blocage « endpoint public sans auth » est levé par ADR-0017).

---

## Checkpoint précédent — 2026-10-11 09:51
Session : dd4cb97a-540a-4afe-bc2a-f23ecd9b21d8

## Tâches complétées

- **Phase 4 ouverte — quatre items sur six faits**, trois commits atomiques sur
  `feat/tech-watch-skill`, **branche poussée** et **PR #6 ouverte en
  brouillon** (https://github.com/GMartin-Data/dotfiles/pull/6, corps : résumé
  du chantier, test plan, revue à faire avant passage en « ready ») :
  - `c94e36a` **D2a** : ancien trio retiré (`claude/commands/tech-watch.md`,
    `claude/agents/tech-watch-scorer.md`, `claude/agents/scripts/fetch-sources.py`) ;
    `install.sh` lie `skills/tech-watch` et `agents/tech-watch.md`, les lignes
    du trio et du dossier `scripts` sont supprimées ; manifeste du plugin,
    `README.md` (listes Commands/Skills/Subagents, pointeur vers le dépôt privé
    `GMartin-Data/tech-watch-mcp` = D1), `claude/README.md` (Commands 7,
    Skills 8 avec famille « Veille », Agents 2, Serveurs MCP 2, précédent
    command→skill) et `claude/agent-memory/README.md` alignés. Ajustement
    adjacent inclus : `block-dbt` manquait dans la liste des hooks du README.
    Vérifié : `bash -n`, tests de parité commands/skills/agents vides,
    `plugin.json` valide, aucune référence résiduelle hors `tasks/`,
    `progress.md` et transcripts figés.
  - `f18cdce` **permission** : `Edit(~/tech-watch/**)` dans
    `claude/settings.json`. Vérifié par le guide Claude Code : les règles de
    chemin ne sont consultées que pour `Edit` et `Read` (jamais `Write`),
    `/home/…` serait relatif au dossier du settings, `~/` est la forme
    portable.
  - `80e8cd0` **`claude/evals/tech-watch/README.md`** : scénarios E1–E10 et
    où chacun a été joué, outillage (`run-eval.sh`, `probe-k12.sh`,
    `extract-run.sh`, `check-dates.py`), fixtures, recettes du rejeu final,
    résultats, frictions, doctrine d'étoffage. Chaque chemin cité vérifié.
- **Machine courante** : `install.sh` rejoué (symlinks `~/.claude/skills/tech-watch`
  et `~/.claude/agents/tech-watch.md` créés), trois symlinks obsolètes retirés
  (`unlink`), aucun lien pendant. La skill `tech-watch` est chargée en session.

## En cours

- Rien. La revue de code s'ouvre dans une session neuve sur la PR #6 (choix
  Greg : contexte frais par précaution).

## Prochaines étapes

1. **Session neuve** : `/code-review 6` (PR #6 ; seconde revue prévue par la
   phase 1 bis du plan, une par dépôt), triage un finding par tour, correctifs
   commités et poussés sur la branche.
2. PR #6 : passer de brouillon à « ready » (`gh pr ready 6`), merge, puis
   `plan.md` §5 : sous-section « Phase 4 » (ce qui a été fait, revue, PR) et
   clôture du chantier.
3. **Première veille réelle** en session interactive : observer si la règle
   `Edit(~/tech-watch/**)` est héritée par le fork (non documenté — sinon
   `permissionMode: acceptEdits` dans l'agent, valable si la session
   principale est en `default`).
4. Points pour Greg issus du rejeu final (`final-replay-2026-10-11/run.md`,
   « Observations ») : dates dev.to sans année (statu quo ou `unverified` ;
   `check-dates.py` à élargir aux graphies `10/7/2026`, `Oct 06, 2026`,
   jour-mois seul, et au bloc « Primary sources ») ; égalités sans signal
   d'engagement départagées par un critère inventé (règle K5) ; `Owner
   domains` à `not run (…)` sur un sujet sans propriétaire.
5. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- Aucun (pas de PRD, repo dotfiles). Écart au plan : la phase 4 prévoyait
  `/code-review` « sur les deux branches » ; la branche serveur
  `fix/search-quality` a déjà eu sa revue en phase 1 bis, seule la branche
  dotfiles reste à revoir.

## Décisions prises

- Track léger, sans ADR — décisions du 2026-10-11 :
  - **Greg** : PR ouverte dans cette session, revue de code dans une session
    neuve (contexte frais) avec la PR pour cible. Ouverte en **brouillon**
    pour tenir le rituel « revue avant merge » du CLAUDE.md global.
  - **Claude, signalées** : règle `Edit(…)` plutôt que `Write(…)` (contrainte
    documentée) et plutôt que `additionalDirectories` (n'auto-approuve pas les
    écritures en mode `default`) ; `claude/evals/claude-md/README.md` ligne 79
    laissé tel quel (note historique sur `tech-watch-scorer`) ; `plan.md` non
    touché avant la fin de la phase 4.
- Décisions antérieures du chantier : `plan.md` §1 (D1–D6) et §5 (une
  sous-section par item K*).
- **Points en suspens pour Greg** (consignés dans `plan.md` §5) : Tier 3 de
  `sources.yaml` orienté IA ; frontière B/C au jugement du modèle ; plateau à
  85 des vidéos-listes ; égalités sans engagement ; `check-dates.py`
  incomplet ; tranche Essential vide sans YouTube ; dates sans année ;
  `Owner domains` sans propriétaire.

## Blocages

- Aucun côté chantier. Hors chantier, dépôt `~/mcp-server-code` : endpoint
  Cloud Run `/sse` public sans auth ; rotation de `YOUTUBE_API_KEY` (logs des
  révisions ≤ `00008`) à la main de Greg.

