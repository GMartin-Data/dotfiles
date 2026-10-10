## Dernière mise à jour
Date : 2026-10-10 11:56
Session : 08467072-cb71-4adb-bde3-d8c9315a577a

## Tâches complétées

- **Phase 0 close** (`plan.md` §5, commit `cbef0a2`) :
  - Import verbatim de l'export claude.ai (`tech-watch-skill.zip`, 4 fichiers)
    dans `claude/skills/tech-watch/`, **sans symlink** (D2a) — `e9609c3`.
  - **D3 révisé en (d)** : scope user essayé puis retiré le jour même sur
    objection de Greg (context-engineering) ; cible = subagent `tech-watch` à
    `mcpServers` inline + skill en `context: fork`, à construire en phase 3.
    Noms vérifiés par sonde : `mcp__tech-watch__search_*`, `WebSearch` — `cef27c1`.
  - **Référence E1–E7** dans `tasks/tech-watch-2026-10/baseline/<E>-<slug>-<date>/`
    (rapport tel quel + `run.md`). Verdicts : E1 échec/réussi (K5 reproduit,
    aucun Short) · E2 réussi (lecture phases 1–2) · E3 réussi/échec (en-tête
    par source OK, pied de page figé) · E5 réussi ×2 · E6 échec (K10, acté sur
    E1) · E7 réussi ×2. Coût ≈ 3,9 $.
  - Outillage réutilisable : `claude/evals/tech-watch/run-eval.sh` (sandbox
    isolé patron batch A, `--mcp-config` session, Opus pinné, `EXTRA_ARGS`,
    `FIXTURE_DIR`, `MCP_JSON`), `extract-run.sh`, fixtures `e3/` (stdio, token
    bidon) et `e5/notes.md`. Transcripts dans `claude/evals/results/`
    (gitignorés).
- Branche `feat/tech-watch-skill` : 19 commits, **non poussée**.

## En cours

- Rien. La phase 3 s'ouvre dans une session neuve.

## Prochaines étapes

1. **Phase 3 — skill**, ordre du plan §3 : K12 d'abord (sonde du point non
   documenté : le `mcpServers` inline d'un subagent est-il connecté quand une
   skill le fork ; agent `tech-watch` sur le patron `agents/dbt.md` ; skill en
   `context: fork` ; `web_search` → `WebSearch` ; retirer ou renommer la skill
   côté claude.ai dès que la version fichier diverge, car Claude Code la
   synchronise sous `anthropic-skills:tech-watch`), puis K8 → K2/K9 → K4 → K6
   → K7 → **K5 en tour dédié** → K10 → K3 → K11 → K1. Observations transverses
   à relire avant : `plan.md` §5 « Phase 0 ».
2. Rejeu E1–E7 après chaque lot via `run-eval.sh`, comparaison à `baseline/`.
   E4, E8, E9, E10 : non joués, une veille complète chacun, selon budget.
3. **Phase 4** : retrait de l'ancien trio command + agent + script (D2a),
   `install.sh`, README, `claude/evals/tech-watch/README.md`, `/code-review`
   sur la branche, PR.
4. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles). Écarts à la passation : E3 joué avec
  YouTube également en panne (pas de clé en local) ; E6 acté sur E1 ; série
  sur Opus 5.5 et non Fable.

## Décisions prises

- Track léger, sans ADR — décisions Greg (2026-10-09 → 10) :
  - **D3 (d)** subagent inline plutôt que scope user (`plan.md` §1).
  - **Opus 5.5 pour toute la série E1–E10** ; ne rouvrir qu'en cas de fort
    désaccord.
  - E6 acté sur le run E1, sans rejeu ; fixture E5 à sujet « proche d'une
    veille » validée après explication.
  - Transcripts non committés (précédent batch A, `claude/evals/results/`
    gitignoré).

## Blocages

- Aucun côté chantier. Hors chantier, inchangés : endpoint Cloud Run `/sse`
  public sans auth ; rotation de `YOUTUBE_API_KEY` (logs des révisions
  ≤ `00008`) à la main de Greg.

---

## Checkpoint précédent — 2026-10-09 16:21
Session : 71570f5a-6005-4fcb-a082-dd041048698a

## Tâches complétées

- **Phase 1 bis (revue) close** — menée en session dédiée sur `~/mcp-server-code` :
  `/code-review high` sur `main..fix/search-quality`, 10 findings triagés,
  6 commits de correctifs test-first (clé YouTube hors des messages d'erreur,
  sonde du token une fois par processus, `_fetch_details` best-effort sur toute
  erreur, `Field`/`Literal` dans les schémas + refus de `query=""`, phrase
  entre guillemets dans une requête arXiv, `channelTitle` décodé). PR #1 mergée
  (`574d580`), 79 → 97 tests. Détail commit par commit : `plan.md` §5.
- **Phase 2 (déploiement) close** — go Greg, D6 : `gcloud run deploy --source .`
  depuis `main` → révision `tech-watch-mcp-00008-mp2`, puis `00009-qgq`
  (voir ci-dessous), 100 % du trafic, variables d'env intactes (noms
  vérifiés). **Vérifications live [Observé]** contre l'endpoint SSE via le
  client du SDK `mcp` : 3 outils avec descriptions, enums et `minLength` ;
  `dbt` → `dbt-labs/dbt` n° 1 sans avertissement 401 ; arXiv 4/5 pertinents ;
  **critère S4 live rempli** (« Mods in Claude Code », chaîne Claude, n° 2/10,
  341 916 vues, 3:21) ; `sort='popular'` et `query=''` → `isError` sans appel
  amont ; logs de révision `🦑 GitHub token: ✅ valid`. Repli documenté dans
  `plan.md` §5 (`update-traffic --to-revisions …00007-5kt=100`).
- **Fuite de la clé YouTube dans les logs Cloud Run trouvée et corrigée** :
  httpx journalisait chaque requête au niveau INFO avec l'URL complète
  (`…&key=<YOUTUBE_API_KEY>`), antérieur au chantier (déjà sur `00007`).
  Branche `fix/httpx-request-logging` menée **depuis cette session dotfiles**
  (chemins absolus) : test rouge (session MCP en mémoire + `MockTransport`,
  la ligne `HTTP Request … key=AIzaSECRET` capturée) → logger `httpx` au
  niveau `WARNING` dans `setup_logger` → 98 tests verts. PR #2 mergée
  (`9fccf2b`), révision **`00009-qgq`** déployée ; logs vérifiés : recherche
  YouTube sans ligne `HTTP Request`, 0 entrée `key=`.
- Plan tenu à jour : `plan.md` §5 (phase 1 bis, phase 2, fix httpx), commits
  `f8d0411` et `8aa493c` sur `feat/tech-watch-skill` (8 commits docs,
  **non poussée**).

## En cours

- Rien côté serveur : `main` = `origin/main` (`9fccf2b`), suite verte, prod
  sur `00009`. Le chantier bascule sur la skill (phase 0), qui attend l'export.

## Prochaines étapes

1. **Phase 0 — bloquée par Greg** : export de la skill depuis Claude.ai
   (`.skill` ou les 4 fichiers `SKILL.md` + `references/`) → import verbatim
   dans `claude/skills/tech-watch/`, déclaration MCP (D3a : `claude mcp add
   --transport sse tech-watch https://tech-watch-mcp-ocbwcs6sjq-ew.a.run.app/sse`),
   référence E1–E10 dans `baseline/`. **Session neuve** (`/clear` + `/catchup`)
   une fois l'export disponible : `plan.md` §3 phase 0.
2. Phases 3–4 (skill K1–K12 dans l'ordre du plan, K5 en tour dédié ; evals ;
   retrait de l'ancien trio `/tech-watch` command + agent + script — D2a ;
   seconde `/code-review` sur `feat/tech-watch-skill`, PR) : `plan.md` §3.
3. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles). Écarts à la passation : S6 étendu à la
  fusion des deux entrées serveur ; ordre S6 avant S1 ; revue insérée avant
  le déploiement ; correctif httpx (hors passation) livré en révision `00009`.

## Décisions prises

- Track léger, sans ADR — décisions Greg :
  - **Phase 2 (D6)** : go donné le 2026-10-09 ; déploiements `00008` puis
    `00009` lancés par Claude, variables d'env non touchées.
  - **Fix httpx traité depuis la session dotfiles**, branche de fix + PR #2
    sans `/code-review` (1 ligne de code + 1 test) — exception ponctuelle à
    « une session par dépôt », motivée par la taille.
  - Les logs des révisions ≤ `00008` contiennent la clé : **rotation de
    `YOUTUBE_API_KEY` laissée à la main de Greg** (console Google puis
    `gcloud run services update --update-env-vars`).
  - Reprise de la skill dans un **contexte frais** après ce checkpoint.
- Rappel des décisions de la phase 1 (D1 remote privé, S6 (a) module unique,
  choix S2/S3/S4, S6 avant S1) : `plan.md` §1 et §5.

## Blocages

- **Export de la skill** depuis Claude.ai (à la main de Greg) — bloque les
  phases 0, 3, 4.
- Risque hors chantier maintenu : endpoint Cloud Run `/sse` **public sans
  auth** (quota YouTube exposé) — à traiter séparément (IAM ou clé en header).
  S'y ajoute la rotation de la clé YouTube (logs historiques), optionnelle.

---

## Checkpoint précédent — 2026-10-09 13:51
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

