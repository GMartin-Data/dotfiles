## Dernière mise à jour
Date : 2026-10-04 18:37
Session : 86755d4a-fc5f-4c9d-a934-6c8a09e318d9

## Tâches complétées

- **`progress.md` mis sous fenêtre glissante** (`df497e4`, poussé) : mesuré 4 361 lignes pour 22 checkpoints **tous depuis le 2026-09-02** (~200 lignes chacun — il n'y avait rien d'« antérieur à septembre » à archiver), tronqué au `/catchup` par le plafond de 25k tokens du Read, en plein milieu d'un checkpoint. Coupe : `progress.md` → 132 lignes (3 checkpoints), 19 checkpoints déplacés tels quels dans `tasks/progress-archive.md` (en-tête : jamais lu au `/catchup`). Règle ajoutée à `claude/commands/progress.md` (symlinké, actif) : après écriture, déplacer le surplus en tête de l'archive, sans condenser ; README mis à jour.
- Checkpoint précédent (17:02) commité et poussé (`327f1ef`).

## En cours

- Rien — ce checkpoint à committer sur `main` puis pousser ; première rotation de la fenêtre par la règle (le checkpoint du 10:30 part à l'archive).

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis `git push origin main`.
2. **À la main de Greg** : `./install.sh` post-merge, puis première tâche déléguée au subagent `dbt` sur un vrai projet (révision de l'effort à ce moment-là).
3. **Items dormants, event-driven et cycle `/insights` 2026-10-26** : tous dans `tasks/insights-actions.md`, section « Ordre du jour reconduit » (relogés le 2026-10-04 depuis les checkpoints — plus de report par référence ici).

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles).

## Décisions prises

- Track léger, sans ADR — décisions Greg :
  - **Fenêtre glissante de 3 checkpoints + archive** plutôt que « supprimer, git garde tout » (grep facile conservé) ; verbosité des checkpoints (~200 lignes) **non touchée**, le format fait son travail de reprise.

## Blocages

- Aucun.

---

## Checkpoint précédent — 2026-10-04 17:02
Session : 86755d4a-fc5f-4c9d-a934-6c8a09e318d9

## Tâches complétées

- **Chantier dbt agent clos — revue de code, triage, PR #5 mergée sur `main`** (`924e4fd`, merge commit, parents `2c3f55a` ← main et `1865d9d` ← branche ; `feat/dbt-agent` conservée sur `origin` pour l'historique) :
  1. **`/code-review high` en session dédiée** (décision Greg) : 10 findings. Chaque finding vérifié avant soumission (reproduction sur le hook ou l'enveloppe, sinon lecture), **triage un par tour**, correctifs **test-first** (rouge constaté → go → vert), **un commit par finding** : hook — mots-clés `if`/`do`/`!` et redirections (`fcafccd`), programmes inertes `pytest`/`ruff`/`mypy`/`pyright`/`pre-commit` derrière un lanceur (`fe5bca6`) ; enveloppe — kill du groupe de processus au timeout (`3f2c801`), chemins de sortie dbt résolus comme dbt (`DBT_ENGINE_*` > `dbt_project.yml` > défauts, `a8d196d`), stdout conservé sur `run_results` périmé (`2c37092`), `RefusalError` si le lanceur ne démarre pas (`ce0b637`), sélection normalisée entre `ls` et `build` (`37c8282`), rollback des répertoires de `codegen` (`31e0b15`), refactor `_status()` (`58692ba`) ; `install.sh` en français — exemption déclarée dans `CLAUDE.md` projet (`b4fea5d`). Suite : 205 → **233 tests verts**, shellcheck propre.
  2. **Deux claims de la revue invalidés par reproduction** : le blocage de l'enveloppe au timeout (faux sur POSIX, `wait()` après `kill`) ; la « traceback brute » sur `uv` absent (le SDK MCP la masque en `Error executing tool`, serveur vivant). Corrigés quand même, à moindre portée.
  3. **Livrable §7 écrit** (table des 10 findings : vérification, sort, commit), compteurs du §1/§2 mis à jour, statut du plan à jour ; README : hook et empreinte réécrits pour les findings 1, 3, 5.
  4. **PR #5 ouverte puis mergée** (`gh pr merge --merge`, décision Greg en séance) ; `main` local ramené à `924e4fd`.

## En cours

- Rien — ce checkpoint à committer sur `main` puis pousser.

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) sur `main`, puis `git push origin main`.
2. **À la main de Greg** : `./install.sh` (post-merge, test plan de la PR), puis première tâche déléguée au subagent `dbt` sur un vrai projet — critère de révision de l'effort (`high` → `medium`/`xhigh`) à ce moment-là.
3. **Hors chantier, hérité** : archiver les checkpoints antérieurs à septembre de `progress.md` (4 300+ lignes, tronqué au `/catchup`) ; faiblesses de `block-force-push.sh` (mot « force » non ancré) et `block-rm-rf.sh` (bloque `rm -f` sur un fichier unique, subi en séance) — signalées, non corrigées.
4. **Event-driven, non planifié** : 9ᵉ outil `dbt_docs_generate` ; exposer « modèle construit ou non » ; T20 à la première exécution concurrente ; le hook bloque `python - <<EOF … import dbt` (voulu, noté au livrable §7).
5. Points du cycle `/insights` 2026-10-26 et chantier evals Phase 4 : inchangés ; **à prendre en compte à la mesure du ratio méta/produit** : le chantier d'outillage dbt est désormais fermé.

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles). Écarts avec la spec dbt : livrable §3, inchangés par la revue.

## Décisions prises

- Track léger, sans ADR — décisions Greg, une par tour :
  - **10 findings sur 10 traités** (8 fix, 1 refactor, 1 exemption documentaire), y compris les deux requalifiés mineurs après reproduction (findings 6 et 8).
  - **Finding 5** : option (b) liste de programmes inertes plutôt qu'acter le fail-closed ; `python`/`sh` restent inspectés.
  - **Finding 10** : exemption `install.sh` en français déclarée dans `CLAUDE.md` projet plutôt que traduire (bloc neuf ou fichier entier).
  - **Merge par Claude** (revirement en séance : « j'aimerais en fait que tu merges »), merge commit, **branche distante conservée**.

## Blocages

- Aucun.

---

## Checkpoint précédent — 2026-10-04 15:34
Session : a9402681-d49d-4e6e-bbaf-04b0771d3cfc

## Tâches complétées

- **Étape 6 du plan dbt agent close — rejeu T0–T21 par le subagent réel, livrable écrit, branche poussée** (`feat/dbt-agent`, 14 commits poussés `d3aaf94..62ee6f1`, 0 d'avance) :
  1. **8 runs du subagent réel** (`claude -p` stream-json, Haiku en session principale, subagent `claude-opus-5-5`, 1,36 $) depuis le testbed ; lecture des événements `parent_tool_use_id` + `task_notification`. Boucle complète écrire → `parse` → `ls` → `build` → `show` → `codegen` sans refus non voulu ; refus de l'enveloppe (G4, G5, P1, H7) lus et respectés ; deux règles anticipées par l'agent (H3, H5). Lanceur et transcripts : `~/dbt-agent-testbed-results/step6/` (hors du projet dbt).
  2. **Trois décisions Greg, une par tour, toutes exécutées** : (a) subagents `dbt` concurrents interdits par la `description` — Claude Code tue le serveur inline partagé par nom quand l'un finit (`c7d8adb`) ; (b) empreinte de fichiers large conservée, contrat écrit au README ; (c) **`compile`/`show`/`codegen` passés sous la cible `ro`** (`98b483a`, test-first 3 rouges → 205 verts) parce que `--no-introspect` n'empêche pas `run_query` sur dbt-snowflake — garde K3 devenue structurelle, prouvée (`Insufficient privileges`, 0 table créée).
  3. **Point 9 du §6 [Observé]** : `! uv run … dbt --version` passe, la même commande par mon Bash est `BLOCKED`.
  4. **Tests bruts T1, T2, T10, T14, T17, T18 lancés par Greg** (`t_series.sh`), lus et étiquetés ; T21 [Observé] sur `dev` (Snowsight, 15 requêtes `dbt-agent`) et `ro` (44 `dbt-agent-ro`). T11/T12 actés hors périmètre ; T20 non implémenté, noté.
  5. **`effort: high` conservé** (décision Greg) malgré 0 « cale » sur 8 runs : banc trivial, révision au premier vrai projet.
  6. **Livrable de fin écrit** (`tasks/dbt-agent-2026-10/livrable.md`, brief §6) : fonctionne / écarté / 9 écarts à reporter dans la spec / table T0–T21 / usage / suites. Plan §16 complet, statut en tête à jour. README : paragraphe « Désinstaller l'agent dbt » (`62ee6f1`).
  7. **Testbed** : 5 modèles écrits par le subagent commités (`0434792`, dépôt local sans remote).

## En cours

- Rien — ce checkpoint à committer puis pousser (1 commit).

## Prochaines étapes

1. **Committer ce checkpoint** (`docs(progress)`) puis `git push origin feat/dbt-agent`.
2. **`/clear` → `/catchup` → `/code-review` sur le diff `feat/dbt-agent` → `main`, session dédiée** (décision Greg : la revue a sa propre session). Effort `high` au moins ; zones sensibles : `block-dbt.sh` (découpeur awk), `session.py`, `conditions.py`. Triage des findings un par tour, puis **PR** — merge commit (pas squash, pas rebase) pour que le rollback tienne en un `git revert -m 1`.
3. **Après merge, hors chantier** : archiver les checkpoints antérieurs à septembre de `progress.md` (4 275 lignes, ~108k tokens, tronqué au `/catchup`) ; signaler sans corriger : faiblesses de `block-force-push.sh` et `block-rm-rf.sh` (plan §15).
4. **Event-driven, non planifié** : 9ᵉ outil `dbt_docs_generate` ; exposer « modèle construit ou non » (constat 8) ; T20 à la première exécution concurrente ; révision de l'effort au premier vrai projet.
5. Points du cycle `/insights` 2026-10-26 et chantier evals Phase 4 : inchangés.

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles). Écarts avec la spec dbt : listés au livrable §3, à reporter dans `spec.md` au besoin.

## Décisions prises

- Track léger, sans ADR — décisions Greg, une par tour :
  - **Un seul subagent `dbt` à la fois** (phrase dans la `description`).
  - **Empreinte large conservée** plutôt que restreinte aux chemins dbt.
  - **Lecture sous `ro`, écriture sous `dev`** : `compile`, `show`, `codegen` rejoignent `show_inline` ; seul `build` reste sur `dev`.
  - **`effort: high` conservé**, révision reportée au premier vrai projet.
  - **T11/T12 actés hors périmètre** ; fichiers du subagent **commités dans le testbed**.
  - **Session dédiée au `/code-review`**, après push et checkpoint ; paragraphe de désinstallation écrit avant la revue (insensible à ses findings, et revu avec le reste).

## Blocages

- Aucun.

