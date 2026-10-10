## Dernière mise à jour
Date : 2026-10-10 15:19
Session : c353e960-a614-4035-b178-7387d249e416

## Tâches complétées

- **Phase 3 — 8 items sur 11 clos**, chacun avec règle validée par Greg
  (un point par tour), rejeu d'eval contre le critère, fiche dans
  `tasks/tech-watch-2026-10/phase3/` et section dans `plan.md` §5 :
  - **K12** sonde du montage D3 (d) : le `mcpServers` inline d'un subagent est
    connecté quand une skill le fork ; serveur injoignable = outils absents
    sans erreur. `claude/agents/tech-watch.md` créé, `SKILL.md` en
    `context: fork` + `agent: tech-watch`. E1 rejoué sous le fork : 121 s, 0,50 $.
  - **K8** description enrichie (6 phrases-types FR/EN, cas négatifs remontés) ;
    E5 ×2, E7 ×2 identiques à la référence. Skill claude.ai **supprimée par
    Greg** (doublon synchronisé disparu, vérifié par sonde).
  - **K2/K9** une requête par outil, paramètres explicites, Tier 2/3 en
    `WebSearch` + `allowed_domains`, Papers With Code → Hugging Face ;
    E2 arXiv **5/5** strict (référence 3/5), Tier 2 9–10 liens par recherche.
  - **K4** filtre rapide on-topic / adjacent / off-topic, dédoublonnage avant
    comptage, Tier 3 si on-topic uniques < 12 ; E10 sur 3 sujets, déclenché
    sur « Apache Iceberg row lineage » (83 adjacents/off-topic n'ont pas
    dispensé du Tier 3).
  - **K6** enrichissement budgété (10 `WebFetch`, une par URL, Tier 1 jamais
    ouvert, `unverified` sinon) ; E8 sans `WebFetch` et run normal : aucune
    date inventée, budget tenu à l'unité. `check-dates.py` créé.
  - **K7** sources primaires d'abord (recherche sur les domaines du
    propriétaire, bloc « Primary sources » hors classement, règle de
    contradiction) ; E1 : billet, docs `en`, changelog ouverts en premier ;
    une contradiction réelle signalée (E9 opportuniste).
  - **K5** grille réécrite (autorité par nature A/B/C/D, fraîcheur relative
    à la fenêtre, dépôt sur sa date de création, seuil 60 strict) ; E1 :
    vidéo officielle n° 1 à 94, vidéos-listes de 97 à 85, 3 sources web
    classées ; E4 : sources de 31–60 j gardées.
  - **K10** tests d'homonymie (date, sens) et dédoublonnage élargi (plafond
    2 par auteur) ; correctif en cours de route (référence = plus ancienne
    date d'une source primaire, préversion comprise, sinon test sauté) ;
    E6 réussi, `0xDarkMatter/claude-mods` écarté par règle.
- Montage d'evals stabilisé : `run-eval.sh` sans `--strict-mcp-config` (bloque
  aussi les serveurs du frontmatter), `AGENT_MD` (E3 stdio, bouchon
  `fixtures/k8/agent-stub.md` pour E5/E7 avec `--max-turns 1`),
  `probe-k12.sh`, `check-dates.py`. Transcripts dans `claude/evals/results/`
  (gitignorés). Coût cumulé de la phase 3 ≈ 10 $ (≈ 20 runs).
- Branche `feat/tech-watch-skill` : **40 commits d'avance sur `main`, non
  poussée**, arbre propre.

## En cours

- Rien. Checkpoint pris à 35 % de contexte, par découpage : le lot « sortie »
  (K3, K11, K1) s'ouvre dans une session neuve sur les fichiers finaux.

## Prochaines étapes

1. **K3** — état par source : figer dans `report-template.md` un en-tête à
   format fixe (comptes, requêtes, tiers, enrichissement, couverture, date
   test — aujourd'hui 5 lignes spontanées, format différent à chaque run) et
   un pied de page généré d'après les sources réellement utilisées (figé
   « arXiv · GitHub · YouTube · Web search » depuis la référence). Rejeu E3 :
   `AGENT_MD=claude/evals/tech-watch/fixtures/e3/agent-stdio-invalid-token.md`
   (syntaxe `env:` du frontmatter à vérifier au passage), comparer à
   `baseline/E3-github-401-2026-10-10/`. Proposer le format avant d'écrire.
2. **K11** — slug, langue, emplacement (rapport en anglais ou français selon
   les runs, résumé en français ; slug observé `claude-code-mods` /
   `ai-agent-evaluation` ; emplacement = CWD).
3. **K1** — limitations réécrites d'après les comportements réels
   post-correction (S1 avertissement 401, serveur absent = outils absents,
   budget de pages, `unverified`).
4. Rejeu final E1–E7 via `run-eval.sh`, comparaison à `baseline/`, puis
   **phase 4** : retrait de l'ancien trio command + agent + script (D2a),
   `install.sh`, README, `claude/evals/tech-watch/README.md`, `/code-review`
   sur la branche, PR.
5. Items dormants et cycle `/insights` 2026-10-26 : `tasks/insights-actions.md`.

## Écarts vs PRD

- N/A (pas de PRD — repo dotfiles). Écarts à la passation : E10 a demandé
  3 sujets (les deux premiers trop couverts) ; E8 simulé par retrait de
  `WebFetch` ; E9 joué de façon opportuniste sur E1 ; Papers With Code
  remplacé (archivé) ; DEV.to/Hashnode retiré du Tier 3 (doublon Tier 2).

## Décisions prises

- Track léger, sans ADR — décisions Greg du 2026-10-10 (détail dans `plan.md`
  §5, phase 3) :
  - Skill claude.ai **supprimée** plutôt que renommée (le déclenchement se
    fait sur la description).
  - K2/K9 : catégories arXiv `cs.AI, cs.LG, cs.CL, cs.SE, cs.DB` ; YouTube
    `language=en` sauf demande FR ; Hugging Face Papers remplace Papers With Code.
  - K4 : coupe vidéo < 3 min binaire ; adjacents hors du compte des 12.
  - K6 : budget 10 pages échecs compris ; Tier 1 jamais ouvert ; E8 par
    retrait de `WebFetch`.
  - K7 : bloc « Primary sources » hors classement ; contradiction écartée si
    dans le titre, sinon signalée ; 3 pages réservées ; AWS et Azure ajoutés
    aux propriétaires connus.
  - K5 : autorité par nature A/B/C/D ; date `unverified` = 5, adjacents non
    classés ; seuil 60 strict avec note de couverture.
  - K10 : test de date adossé à la source primaire ; plafond 2 par auteur ;
    réécritures sans apport en D.
- Ajustements pris par Claude, signalés, non contestés : dédoublonnage avant
  comptage (K4) ; test de date sur la plus ancienne date primaire, sauté si
  préversion non datée (K10).
- **Points en suspens pour Greg** (consignés dans `plan.md` §5) : `model: opus`
  figé dans l'agent (choix pour l'usage réel avant la phase 4) ; Tier 3 de
  `sources.yaml` orienté IA, inutile sur un sujet data (compléter ou laisser
  le modèle proposer) ; frontière B/C au jugement du modèle ; plateau à 85
  des vidéos-listes (levier engagement ou seuil de tranche) ; E9 à rejouer
  sur une source classée ; `check-dates.py` ne lit pas le bloc « Primary sources ».

## Blocages

- Aucun côté chantier. Hors chantier, inchangés : endpoint Cloud Run `/sse`
  public sans auth ; rotation de `YOUTUBE_API_KEY` (logs des révisions
  ≤ `00008`) à la main de Greg.

---

## Checkpoint précédent — 2026-10-10 11:56
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
