## Dernière mise à jour
Date : 2026-10-11 12:09
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

---

## Checkpoint précédent — 2026-10-11 09:31
Session : 728a4194-3ef1-4992-b8d4-be183eeec06e

## Tâches complétées

- **Rejeu final E1–E7 sur les fichiers finaux** (`tasks/tech-watch-2026-10/final-replay-2026-10-11/`,
  section « Rejeu final » dans `plan.md` §5) : sept sandboxes en parallèle,
  `run-eval.sh`, Opus, serveur `00009` (E3 en stdio local, `GITHUB_TOKEN=invalid` ;
  E5a/E5b/E7b sur le bouchon, `--max-turns 1` ; E7a en veille complète).
  **Six scénarios sur six réussis** : E1 (bloc « Primary sources » à 3 entrées,
  vidéo officielle n° 1 A Primary 94, 15 vidéos de 3:21 à 17:27), E2 (4/5
  arXiv strict), E3 (GitHub `degraded` 30/29/12 avec repli compté dans la
  ligne, YouTube `failed` 10/10/0, pied `GitHub · Web (Tier 2) · Owner
  domains`), E5 ×2, E6 (`0xDarkMatter` n° 9 côté serveur, écarté au test de
  sens), E7 ×2. Les deux échecs de la référence (E1, E3) et l'échec acté E6
  sont corrigés par règle. Coût 3,94 $.
- Observés au passage : titre K11 au sujet normalisé et ligne `Request` sur
  les quatre rapports ; comptes de repli K3 cohérents (`Pipeline` = somme des
  lignes) ; **E9 sur une source classée** (E3, rang 4, dev.to datant l'annonce
  au 3 octobre : gardée et étiquetée `⚠️ Contradicts …`), point en suspens
  couvert.
- **Critère de la phase 3 observé** : E1–E10 rejoués (E4, E8, E10 en K5, K6,
  K4), comparés à `baseline/`.
- **Décision Greg : agent sur Opus pour l'usage réel** (actée dans `plan.md` §5,
  K12 point 1) : tarif 2,5 fois moindre que Fable, règles validées sur Opus
  seulement. Aucun changement de fichier.
- Branche `feat/tech-watch-skill` : **50 commits d'avance sur `main`, non
  poussée**, arbre propre (`791e863` rejeu, `8da810d` décision Opus).

## En cours

- Rien. La phase 4 s'ouvre dans une session neuve.

## Prochaines étapes

1. **Phase 4** (`plan.md` §3) : retrait de l'ancien trio command + agent
   `tech-watch-scorer` + script (D2a : `claude/commands/tech-watch.md`,
   `claude/agents/scripts/`, lignes correspondantes d'`install.sh`) ; liens
   `install.sh` pour `claude/skills/tech-watch/` et `claude/agents/tech-watch.md` ;
   README des dotfiles ; `claude/evals/tech-watch/README.md` (montage fork,
   `run-eval.sh`, fixtures, `check-dates.py`, recette E5/E7 au bouchon) ;
   permission `Write(/home/martin/tech-watch/**)` ou `--add-dir` dans la
   configuration livrée (en session interactive, `Write` hors CWD demande une
   permission — observé en K11) ; `/code-review` sur la branche, triage, PR.
2. Points pour Greg issus du rejeu final (fiche `final-replay-2026-10-11/run.md`,
   « Observations ») : dates dev.to sans année lues comme 2026 et déclarées
   (statu quo ou `unverified` ; `check-dates.py` à élargir aux graphies
   `10/7/2026`, `Oct 06, 2026`, jour-mois seul, et au bloc « Primary
   sources ») ; égalités sans signal d'engagement départagées par un critère
   inventé (E1, E2 — règle K5) ; `Owner domains` à `not run (…)` sur un sujet
   sans propriétaire (E2 — à figer dans « Header rules » ou laisser).
3. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- Aucun (pas de PRD, repo dotfiles). Écarts à la passation sur l'ensemble de
  la phase 3 : E10 sur 3 sujets, E8 simulé par retrait de `WebFetch`, E9
  d'abord opportuniste puis observé sur une source classée au rejeu final,
  Papers With Code remplacé par Hugging Face Papers, DEV.to/Hashnode retirés
  du Tier 3, E1 + E7a joués ensemble pour K11.

## Décisions prises

- Track léger, sans ADR — décisions Greg du 2026-10-11 :
  - **Agent `tech-watch` sur Opus pour l'usage réel** (`plan.md` §5, K12
    point 1) ; le pin `model: opus` suit l'alias.
  - Rejeu final lancé en parallèle (sept sandboxes), E7a en veille complète
    pour observer la ligne `Request`.
- Décisions de la phase 3 (K12 → K1, 2026-10-10) : `plan.md` §5, une
  sous-section par item.
- **Points en suspens pour Greg** (consignés dans `plan.md` §5) : Tier 3 de
  `sources.yaml` orienté IA, inutile sur un sujet data ; frontière B/C au
  jugement du modèle ; plateau à 85 des vidéos-listes et égalités sans signal
  d'engagement ; `check-dates.py` incomplet (graphies, bloc « Primary
  sources ») ; sans YouTube, la tranche Essential peut rester vide ; dates
  dev.to sans année ; `Owner domains` sans propriétaire.

## Blocages

- Aucun côté chantier. Hors chantier : endpoint Cloud Run `/sse` public sans
  auth ; rotation de `YOUTUBE_API_KEY` (logs des révisions ≤ `00008`) à la
  main de Greg — tous deux à traiter dans le dépôt `~/mcp-server-code`, hors
  de cette branche.
