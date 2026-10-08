## Dernière mise à jour
Date : 2026-10-08 14:10
Session : 445c822b-515b-4ca5-960f-37f1e011301f

## Tâches complétées

- **Précondition « `./install.sh` post-merge » vérifiée, non rejouée** : symlinks
  `agents/dbt.md`, `hooks/block-dbt.sh`, `mcp/dbt-enveloppe` en place depuis le
  2026-10-04 10:06 (posés sur la branche, pointent dans le working tree donc sur
  `main` fusionné) ; `.venv` présent, installation **editable** (`uv pip show`),
  donc les correctifs de la revue sont vivants ; lockfile inchangé depuis le
  2026-10-03 ; `uv sync --frozen --dry-run` ne ferait que ré-enregistrer le
  paquet local. `settings.json` : hook `block-dbt.sh` et `Bash(dbt *)` en deny
  actifs. La dernière case du test plan de la PR #5 est donc remplie pour sa
  moitié « installation » ; sa moitié « tâche réelle » est reportée (voir
  Décisions).
- Checkpoint du 2026-10-04 18:37 commité (`874190f`), `git lg` ajouté (`8289fba`).
- **Deuxième rotation de la fenêtre** : checkpoint du 2026-10-04 15:34 déplacé
  tel quel en tête de `tasks/progress-archive.md` (20 → 21 checkpoints archivés).

## En cours

- **Tâche de fix, à cadrer par Greg** (annoncée en séance, non encore décrite) —
  analyse méticuleuse demandée ; démarre après ce checkpoint.

## Prochaines étapes

1. Committer ce checkpoint (`docs(progress)`) sur `main`, puis `git push origin main`.
2. Cadrer la tâche de fix : énoncé, critère de succès vérifiable, fichiers
   concernés — avant tout outil d'exploration.
3. **Premier vrai test du subagent `dbt`** : event-driven, déplacé dans
   `tasks/insights-actions.md` « Ordre du jour reconduit » item 5 (déclencheur :
   un projet dbt tangible ; la révision de l'effort `high` y est déjà rattachée).
4. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles).

## Décisions prises

- Track léger, sans ADR — décision Greg :
  - **Test réel du subagent `dbt` reporté sine die** : aucun projet dbt tangible
    disponible ; l'item devient event-driven dans `insights-actions.md` plutôt
    qu'une « prochaine étape » reconduite sans déclencheur. `./install.sh` n'est
    pas rejoué (no-op idempotent, précondition déjà acquise).

## Blocages

- Aucun.

---

## Checkpoint précédent — 2026-10-04 18:37
Session : 86755d4a-fc5f-4c9d-a934-6c8a09e318d9

## Tâches complétées

- **`progress.md` mis sous fenêtre glissante** (`df497e4`, poussé) : mesuré 4 361 lignes pour 22 checkpoints **tous depuis le 2026-09-02** (~200 lignes chacun — il n'y avait rien d'« antérieur à septembre » à archiver), tronqué au `/catchup` par le plafond de 25k tokens du Read, en plein milieu d'un checkpoint. Coupe : `progress.md` → 132 lignes (3 checkpoints), 19 checkpoints déplacés tels quels dans `tasks/progress-archive.md` (en-tête : jamais lu au `/catchup`). Règle ajoutée à `claude/commands/progress.md` (symlinké, actif) : après écriture, déplacer le surplus en tête de l'archive, sans condenser ; README mis à jour.
- Checkpoint précédent (17:02) commité et poussé (`327f1ef`).
- **Perte de disponibilité révélée par la fenêtre, corrigée** (`aa3dc22`) : les items reconduits « inchangés » pointaient vers un checkpoint sorti de la fenêtre. Relogés dans `tasks/insights-actions.md` « Ordre du jour reconduit » (cellule de la matrice alignée) ; règle dans `/progress` : checkpoint de tête auto-suffisant, jamais de report par référence. Fenêtre maintenue à 3 (plafond utile = 5, le Read tronque à 25k tokens ; 3 ≈ 15k par reprise).

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
