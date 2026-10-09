## Dernière mise à jour
Date : 2026-10-09 13:51
Session : 847b86f0-f265-4644-aa61-225cbecc5943

## Tâches complétées

- **Chantier `tech-watch` ouvert** (transfert de la skill Claude.ai + correctifs
  du serveur MCP) : passation reçue et figée dans
  `tasks/tech-watch-2026-10/handover.md` ; plan dans `plan.md` du même dossier
  (vérification du code §0, décisions §1, arborescence §2, phases §3, risques
  §4, résultats §5). Branche `feat/tech-watch-skill` (dotfiles, 6 commits docs,
  **non poussée**).
- **Phase 1 (serveur) close** sur `~/mcp-server-code`, branche
  `fix/search-quality`, 9 commits test-first, **43 → 79 tests verts** :
  S3 arXiv (termes `AND`, `submittedDate` côté API, `relevance`, `categories`,
  `https`) · S2 GitHub (meilleure correspondance, `days_back` → `pushed:>`,
  dates émises, `n/a`) · S4 YouTube (`relevance`, `videos.list` → vues/durée,
  entités HTML, `…` seulement si tronqué) · S5 (`ToolError` → `isError=True`) ·
  S6 (`server_http.py` → `server.py` unique FastMCP, SSE + stdio ; ancien stdio
  bas niveau supprimé ; 12 tests d'intégration via le client MCP en mémoire ;
  Dockerfile, README réécrits) · S1 (sonde `/rate_limit` au démarrage de
  session, retry unique sans header sur 401, avertissement en tête de sortie,
  token rejeté mémorisé). Chores : `.gitignore`, `.gcloudignore`, config isort
  ruff. Toutes les `HYPOTHÈSE` serveur de la passation levées (plan §0).
- **Vérifications live [Observé]** : arXiv `AI agent evaluation` 4/5
  pertinents, requête experte 200 (était 400) ; GitHub `dbt` → `dbt-labs/dbt`
  n° 1 (`dbt-core` redirigé 301), `claude mods` 10/10 sur le sujet ; transport
  stdio réel (serveur lancé par un client MCP) ; log de session
  `🦑 GitHub token: ⚠️ absent`.
- **D1 tranché** : dépôt privé `git@github.com:GMartin-Data/tech-watch-mcp.git`
  créé, `main` et `fix/search-quality` poussées, branche par défaut `main` ;
  scan de l'historique propre (`.env` jamais suivi, 6 motifs = placeholders de
  tests). Motif : la source avait déjà été perdue une fois.

## En cours

- **Phase 1 bis — revue avant production**, à lancer dans une **session neuve,
  CWD `~/mcp-server-code`** : `/code-review high` sur `main..fix/search-quality`,
  triage un finding par tour, test-first, un commit par finding, push. Prompt
  d'ouverture donné en séance (lire `plan.md` §0/§3/§5 + `handover.md` §6 par
  chemin absolu ; ne pas toucher au plan ni à `progress.md`). Dette connue à
  ne pas redécouvrir : ruff hérité dans `tests/` (W293, SIM117).

## Prochaines étapes

1. Au retour de la revue (ici, `/clear` + `/catchup`) : relire
   `git -C ~/mcp-server-code log` et consigner la revue dans `plan.md` §5.
2. **Phase 2 — déploiement** (go explicite D6) : `gcloud run deploy
   tech-watch-mcp --source . --region europe-west1 --project mcp-servers-prod`
   (révision `00007-5kt` → `00008`, variables conservées) ; vérifs contre
   l'endpoint déployé : 3 outils + nouveaux params, `dbt`, arXiv, **critère S4
   live** (vidéo officielle « Claude Code mods », vues/durée), log
   `✅ valid` pour le vrai token. Repli : `update-traffic --to-revisions
   tech-watch-mcp-00007-5kt=100`.
3. **Phase 0 — bloquée par Greg** : export de la skill depuis Claude.ai
   (`.skill` ou les 4 fichiers `SKILL.md` + `references/`) → import verbatim
   dans `claude/skills/tech-watch/`, déclaration MCP (D3a : `claude mcp add
   --transport sse`), référence E1–E10 dans `baseline/`.
4. Phases 3–4 (skill K1–K12, evals, retrait de l'ancien trio `/tech-watch`
   command + agent + script — D2a, seconde `/code-review` sur
   `feat/tech-watch-skill`, PR) : `plan.md` §3.
5. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles). Écarts à la passation : S6 étendu à la
  fusion des deux entrées serveur (plan §5) ; ordre S6 avant S1 ; revue
  insérée avant le déploiement (phase 1 bis).

## Décisions prises

- Track léger, sans ADR — décisions Greg :
  - **Feature branches** dans les deux dépôts (D4) ; **passation dans
    `tasks/`** plutôt que `docs/handoff/` (D5).
  - **D1 (a)** : serveur dans son propre dépôt, remote privé (pas d'absorption
    dans `claude/mcp/`).
  - **S6 (a)** : un seul module `server.py` FastMCP pour SSE et stdio ;
    **S6 avant S1**.
  - S3 : multi-mots = `AND`, `categories` optionnel, filtre client supprimé ·
    S2 : `days_back` défaut `None`, `pushed:>` · S4 : pas de filtre Shorts côté
    API (la skill filtrera sur `duration_seconds`), critère live reporté à la
    phase 2 · S5 : mécanisme seul · S1 : sentinelle d'avertissement, sonde via
    `lifespan` (par connexion en SSE).
  - **`.gitignore` serveur** ajouté (cache dé-versionné).
  - **Revue avant déploiement**, en session dédiée ; cette session reste seule
    à écrire `progress.md` et le plan.

## Blocages

- **Export de la skill** depuis Claude.ai (à la main de Greg) — bloque les
  phases 0, 3, 4 ; pas la revue ni le déploiement.
- Risque hors chantier noté : endpoint Cloud Run `/sse` **public sans auth**
  (quota YouTube exposé) — à traiter séparément (IAM ou clé en header).

---

## Checkpoint précédent — 2026-10-08 14:10
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
- **`/model` et `/effort` persistent dans le repo** : une bascule ponctuelle vers
  Opus 5.5 / high a réécrit `claude/settings.json` (symlink global : `"model"`,
  bloc `modelSettings`) ; restauré par `git restore`, défaut resté sur Fable.

## En cours

- Rien. La tâche de fix annoncée en séance se traite sur claude.ai, hors de ce
  repo — rien à reprendre ici.

## Prochaines étapes

1. **Premier vrai test du subagent `dbt`** : event-driven, dans
   `tasks/insights-actions.md` « Ordre du jour reconduit » item 5 (déclencheur :
   un projet dbt tangible ; la révision de l'effort `high` y est rattachée).
2. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

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
