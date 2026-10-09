# Plan — skill `tech-watch` : transfert Claude.ai → Claude Code et correctifs serveur

> **Statut : brouillon du 2026-10-09, à valider par Greg.** Source : `handover.md`
> (passation Claude.ai, items S1–S6 / K1–K12 / E1–E10). Ce plan ne reformule pas
> la passation : il la vérifie contre le code (§0), tranche ce qui manque (§1),
> fixe l'arborescence (§2) et le découpage (§3).

## Contexte

Deux artefacts, deux dépôts :

| Artefact | Où il est aujourd'hui | État |
|---|---|---|
| Skill `tech-watch` (SKILL.md + `references/{sources.yaml, scoring-criteria.md, report-template.md}`) | **Claude.ai uniquement** — aucun des quatre fichiers n'existe sur disque (`find ~`, hors `.trash`) | **À exporter par Greg** (format `.skill` = zip, précédent `~/Téléchargements/conventions-interview.skill`) |
| Serveur MCP | `~/mcp-server-code/` — dépôt git **sans remote**, dernier commit `826c3ce` (2026-03-14, « switch to SSE transport ») | Lu en entier : `tools/{github,arxiv,youtube}.py`, `server_http.py` (déployé), `server.py` (stdio, cible des tests d'intégration), 43 tests |
| Déploiement | Cloud Run `mcp-servers-prod` / `tech-watch-mcp` / `europe-west1`, révision `tech-watch-mcp-00007-5kt`, image bâtie par le `Dockerfile` (`uvicorn server_http:app`) | Endpoint `/sse` **public, répond 200** sans auth (`curl` 2026-10-09) |
| Accès depuis Claude Code | Connecteur claude.ai `tech-watch` présent mais **non authentifié** (seuls `authenticate`/`complete_authentication` exposés) ; aucun `mcpServers` local | K12 confirmé : rien ne tourne ici aujourd'hui |
| Ancien pipeline Claude Code | `claude/commands/tech-watch.md` + `claude/agents/tech-watch-scorer.md` + `claude/agents/scripts/fetch-sources.py` (avril 2026, 5 usages, dernier il y a ~200 j d'après l'audit evals) | **Homonyme** de la skill à importer — collision `/tech-watch` à régler (§1 D2) |
| Rapport de test « Claude Mods » (`tech-watch-claude-mods-2026-10-09.md`) | Introuvable sur disque | Optionnel — référence E1 |

## 0. Ce que la lecture du code confirme (2026-10-09)

Toutes les `HYPOTHÈSE` côté serveur sont levées. Références `fichier:ligne` dans `~/mcp-server-code/`.

| Item | Passation | Après lecture | Preuve |
|---|---|---|---|
| S1 | HYPOTHÈSE | **CONFIRMÉ** | `tools/github.py:32-33` : header `Authorization` posé si token non vide, aucun repli ; `server_http.py:29` : log « FOUND » sur simple présence |
| S2 | CONFIRMÉ | **CONFIRMÉ + précisé** | `tools/github.py:39` `'sort': 'stars'` ; `updated_at` **est récupéré** (`:59`) mais **jamais émis** par le formateur `server_http.py:65-76` ; `item.get('language', 'Unknown')` ne couvre pas `null` → « Language: None » |
| S3 | CONFIRMÉ (URL) / HYPOTHÈSE (filtre client) | **CONFIRMÉ les deux** | `tools/arxiv.py:29` `f"all:{query}"` ; `:32` `sortBy=submittedDate` ; `:45-59` filtre de date **côté client** après fetch — avec `max_results=5`, les 5 plus récents contenant *un* des mots, puis filtre |
| S4 | CONFIRMÉ (tri) / HYPOTHÈSE (appel) | **CONFIRMÉ les deux** | `tools/youtube.py:41` `'order': 'date'` ; un seul appel `search.list`, pas de `videos.list` ; aucun `html.unescape` ; `relevanceLanguage: 'en'` déjà présent (`:45`) |
| S5 | HYPOTHÈSE | **CONFIRMÉ** | outils → `[{'error': True, 'message': …}]` ; `server_http.py:57-60` → `return f"Error: {msg}"` (idem YouTube `:108-111`, arXiv `:158-161`) |
| S6 | HYPOTHÈSE | **CONFIRMÉ + aggravé** | 27 unitaires mockent `httpx` et vérifient la forme ; **16 d'intégration ciblent `server.py` (stdio), pas `server_http.py` (déployé)** — deux entrées dupliquent le formatage, le code déployé n'est couvert par aucun test |
| K12 | HYPOTHÈSE | **CONFIRMÉ** | aucun `mcpServers` tech-watch dans `~/.claude.json` ; connecteur claude.ai en attente d'OAuth ; endpoint Cloud Run public donc déclarable en direct |

Deux points **non vérifiés** (à faire au moment de coder, pas avant) : syntaxe exacte de `submittedDate:[… TO …]` et de `sortBy=relevance` dans le manuel arXiv ; paramètres `order=relevance`, `videoDuration`, et coût quota de `videos.list` (1 unité contre 100 pour `search.list`) dans la doc YouTube Data v3.

## 1. Décisions à prendre (recommandation en gras) — une par tour

| # | Question | Options | Recommandation |
|---|---|---|---|
| D1 | Où vit le code serveur ? | (a) rester dans `~/mcp-server-code`, lui donner un remote GitHub privé ; (b) l'absorber dans `dotfiles/claude/mcp/tech-watch/` comme `dbt-enveloppe` | **(a) — tranché le 2026-10-09** : `git@github.com:GMartin-Data/tech-watch-mcp.git` (privé), `main` et `fix/search-quality` poussées après scan de l'historique (aucun secret ; `.env` jamais suivi). Motif décisif : la source avait déjà été perdue une fois (1er commit « recover source from Cloud Build ») — c'est une unité de déploiement (Dockerfile, Cloud Run) avec sa propre histoire ; `dbt-enveloppe` est dans les dotfiles parce qu'il s'installe localement. Le remote comble le risque « aucune copie hors machine ». Les dotfiles pointent vers lui dans le README |
| D2 | Sort de l'ancien trio (`commands/tech-watch.md`, `agents/tech-watch-scorer.md`, `scripts/fetch-sources.py`) ? | (a) retirer les trois à l'import de la skill (`git rm` + `install.sh`) ; (b) renommer l'ancienne command le temps de la transition ; (c) garder les deux | **(a)**, mais **à la phase 4 seulement** (après evals vertes) ; d'ici là la skill est importée sous `claude/skills/tech-watch/` sans symlink actif, testée via `--mcp-config`/`--settings` ou un plugin de session. Précédent command→skill : `claude-md` (2026-09) |
| D3 | Comment Claude Code atteint le serveur ? | (a) déclaration directe `claude mcp add --transport sse tech-watch <url>` au scope user ; (b) OAuth du connecteur claude.ai ; (c) stdio local `uv run python server.py` | **(a)** pour l'usage, **(c)** pour les tests de la skill en mode dégradé (E3 : token bidon) et pour tester une correction avant déploiement. (b) écarté : couche OAuth inutile devant un endpoint public |
| D4 | Branches ? | feature branches dans les deux dépôts, `/code-review` avant merge (précédent `feat/dbt-agent`, PR #5) | **oui** — `feat/tech-watch-skill` (dotfiles), `fix/search-quality` (serveur) |
| D5 | Où vit la passation ? | `docs/handoff/` (convention du `.gitignore`, jetable) ou `tasks/tech-watch-2026-10/handover.md` (committé, précédent `dbt-agent-2026-10/spec.md`) | **`tasks/`** — le plan la référence par ID pendant tout le chantier |
| D6 | Déploiement Cloud Run : par qui ? | Claude lance `gcloud run deploy --source .` après validation ; ou Greg lance | **Claude, après go explicite par déploiement** (action sortante) ; variables d'env conservées par `deploy` (ne pas toucher aux secrets) |

## 2. Arborescence cible

```
dotfiles/
├── claude/skills/tech-watch/            # import verbatim en phase 0, réécrit en phase 3
│   ├── SKILL.md
│   └── references/
│       ├── sources.yaml
│       ├── scoring-criteria.md
│       └── report-template.md
├── claude/evals/tech-watch/             # E1–E10 : fixtures + README (patron claude/evals/claude-md)
├── tasks/tech-watch-2026-10/
│   ├── handover.md                      # passation, figée
│   ├── plan.md                          # ce fichier ; résultats de phase ajoutés en §5+
│   └── baseline/                        # sorties E1–E10 « avant », datées
└── install.sh                           # phase 4 : lien skills/tech-watch, retrait command + agent + script

~/mcp-server-code/                        # D1 (a) : remote ajouté
├── tools/{github,arxiv,youtube}.py       # S1–S4
├── server_http.py                        # S5 ; S6 : tests d'intégration déplacés sur cette entrée
└── tests/
```

## 3. Phases et critères

Chaque phase s'arrête sur son critère ; rien n'enchaîne sans qu'il soit observé.
Test-first sur le serveur (contrat testable) ; evals avant/après sur la skill.

### Phase 0 — Import et référence (dépend de l'export de la skill par Greg)

1. Décompresser le `.skill` dans `claude/skills/tech-watch/` **sans modification** ; commit `feat(tech-watch): import skill from claude.ai verbatim`.
2. Déclarer le serveur (D3a), vérifier les noms qualifiés d'outils (`mcp__tech-watch__search_*`) et le nom de l'outil web dans Claude Code (`WebSearch`, pas `web_search`).
3. Exécuter la **référence** : E1, E2, E6 en vrai ; E3 via stdio local avec `GITHUB_TOKEN=invalid` ; E5/E7 en sondes `claude -p` sur le déclenchement ; E4, E8, E9, E10 décrits en fixtures mais **joués seulement si le budget le permet** (une veille complète ≈ 25 pages ouvertes). Sorties dans `baseline/`.

**Critère** : la skill tourne de bout en bout dans Claude Code au moins une fois (E1), et chaque E joué a une sortie datée dans `baseline/`.

### Phase 1 — Serveur (test-first, un commit par item, indépendant de la phase 0)

Ordre : **S3 → S2 → S4 → S5 → S1 → S6**. Pour chaque item : test qui échoue (preuve montrée) → go → correction → vert.

| Item | Décision d'implémentation proposée |
|---|---|
| S3 | Si la requête contient `:` de champ ou `AND/OR/ANDNOT` → passée brute ; sinon expression `all:"<query>"` quand ≥ 2 mots, `all:<mot>` sinon. Plage `submittedDate` côté API, `sortBy=relevance`. Paramètre optionnel `categories: list[str]`. Liens `https` |
| S2 | `sort` paramétrable (`best-match` par défaut), `days_back` optionnel → qualificatif `pushed:>YYYY-MM-DD`, sortie avec `created_at`/`pushed_at`, `language or "n/a"` |
| S4 | `order=relevance` + `publishedAfter` conservé ; second appel `videos.list(part=statistics,contentDetails)` → vues, durée ISO 8601 ; `html.unescape` ; `videoDuration` optionnel (`medium` par défaut ? **à trancher avec Greg** : écarte les Shorts mais aussi les vidéos < 4 min) |
| S5 | Lever une exception (`ToolError` FastMCP ou équivalent vérifié dans la version de `mcp` installée) au lieu de `return "Error: …"` ; « 0 résultat » reste un succès |
| S1 | Sur `401` : **un** retry sans header, résultat préfixé d'un avertissement ; sonde `/rate_limit` au démarrage → log « absent / rejeté / valide ». Pas de boucle |
| S6 | Tests d'intégration rebranchés sur `server_http.py` (client FastMCP in-memory) ; `server.py` stdio : **à supprimer ou à réduire à un wrapper** — proposition, à valider |

**Critère** : chacun de S1–S5 a un test rouge avant / vert après ; suite complète verte ; appels de reproduction du §9 de la passation rejoués en stdio local avec les résultats attendus (`dbt-core` top 3, ≥ 4/5 arXiv pertinents, vidéo officielle présente).

### Phase 1 bis — Revue avant production (ajoutée le 2026-10-09)

`/code-review high` sur `main..fix/search-quality`, **en session dédiée** (CWD
`~/mcp-server-code`, précédent dbt), triage un finding par tour, correctifs
test-first, un commit par finding. La revue précède le déploiement : un bug
trouvé après coup forcerait une seconde révision en production. Seconde revue
prévue sur `feat/tech-watch-skill` avant la PR dotfiles (phase 4) — une revue
par dépôt, chacune avant que sa branche ne sorte.

### Phase 2 — Déploiement (après la phase 1 bis)

`gcloud run deploy tech-watch-mcp --source . --region europe-west1 --project mcp-servers-prod` (D6, après go). Vérification : les appels du §9 rejoués **contre l'endpoint déployé**.

**Critère** : révision `00008+` active, mêmes résultats qu'en local, variables d'env intactes (`describe --format` sur les **noms** seulement).

### Phase 3 — Skill (après la phase 2 : ne pas inscrire de contournements)

Ordre proposé, du structurel au cosmétique : K12 (portabilité, noms d'outils, absence du serveur) → K8 (description + déclencheurs FR/EN + négatifs) → K2/K9 (requêtes par outil) → K4 (filtre rapide avant comptage Tier 3) → K6 (enrichissement budgété, « non vérifié ») → K7 (sources primaires d'abord, contradictions) → **K5 (grille)** → K10 (dédup élargi, homonymes) → K3 (état par source, pied de page généré) → K11 (slug, langue, emplacement) → K1 (limitations réécrites depuis les comportements réels **post-correction**).

K5 est l'item le plus lourd et le plus discutable : la nouvelle grille sera proposée **dans un tour dédié**, validée avant écriture.

**Critère** : E1–E10 rejoués, comparés à `baseline/` ; chaque critère d'acceptation K* coché avec preuve.

### Phase 4 — Clôture

Retrait de l'ancien trio (D2a), `install.sh` + README des dotfiles, `claude/evals/tech-watch/README.md`, `/code-review` sur les deux branches, PR, merge. Checkpoint `/progress`.

## 4. Risques et points ouverts

- **Quota YouTube** : 10 000 unités/jour ; `search.list` = 100, `videos.list` = 1 → l'enrichissement S4 coûte ~1 % de plus. Pas de risque.
- **Verrou GitHub** : plusieurs `401` d'affilée → `403` temporaire sur le compte. Le retry S1 est unique et sans boucle ; les tests mockent, jamais d'appel réel avec token invalide **sauf** E3 en stdio local (1 appel).
- **Coût des evals** : une veille complète ≈ 25 fetches + 3 appels MCP ; E1–E10 complets ×2 (avant/après) ≈ 20 veilles. Phase 0 joue un sous-ensemble (§3).
- **Collision de nom** `/tech-watch` command ↔ skill tant que D2 n'est pas exécuté : la skill importée n'est **pas symlinkée** avant la phase 4.
- **`server.py` stdio** : couvert par les tests mais pas déployé ; `server_http.py` déployé mais pas testé. S6 inverse cela — décision explicite attendue sur le sort de `server.py`.
- **Dépendances `mcp>=1.20`** : vérifier la version installée dans `.venv` avant de choisir le mécanisme d'erreur S5.

## 5. Résultats de la phase 1 (serveur, branche `fix/search-quality`)

| Item | Commit | Rouge → vert | Critère **[Observé]** |
|---|---|---|---|
| S3 | `fix(arxiv)` 2026-10-09 | 6 tests (ImportError, `sortBy`, `http`) → 49/49 | `AI agent evaluation` : 4/5 pertinents (5ᵉ adjacent, UAV) ; requête experte `all:… AND cat:cs.AI` → 200 (était 400) ; liens `https` ; `zzqxjkwv` → `[]`. Syntaxe `submittedDate:[…]`, `sortBy=relevance`, parenthèses vérifiées en live avant d'écrire les tests |

| S2 | `fix(github)` 2026-10-09 | 9 tests (ImportError, `sort=stars`, `TypeError`, `KeyError: created_at`, `None`) → 58/58 | `dbt` → **`dbt-labs/dbt` n° 1** (`dbt-core` est redirigé 301 vers ce nom) ; `claude mods` + `days_back=30` → 10/10 dépôts sur le sujet (l'homonyme `ccproxy` sort) ; sortie MCP : `📅 Created: 2016-03-10 · Last push: 2026-10-09`. Premier fichier de tests sur `server_http.py` (entrée déployée) |
| — | `chore` `c86d054` | — | `.gitignore` ajouté, 4 fichiers `.pytest_cache` dé-versionnés (décision Greg) |
| S4 | `fix(youtube)` 2026-10-09 | 9 tests (ImportError, `order=date`, 1 appel au lieu de 2, `&amp;`, `KeyError: views`, `......`) → 67/67 | Params vérifiés dans la doc officielle (context7) : `order`, `publishedAfter`, `videoDuration` (short <4 min), `videos.list part=statistics,contentDetails`. **Critère live (vidéo officielle présente) reporté à la phase 2** : la clé n'existe que sur Cloud Run (décision Greg). Deux tests hérités alignés sur le 2ᵉ appel |

| S5 | `fix(server)` 2026-10-09 | 4 tests (`DID NOT RAISE ToolError`, `isError` faux) + 2 gardes vertes → 73/73 | Via le client MCP en mémoire du SDK (`mcp.shared.memory`) : échec amont → `isError=True` avec le message ; `[]` → `isError=False`, « Found 0 … ». Mécanisme seul, texte des messages inchangé |

| S6 | `refactor(server)` 2026-10-09 (option **(a)**, décision Greg) | 12 tests d'intégration réécrits (client MCP en mémoire) ; `server.main()` → stdio | **69/69** ; `server_http.py` → `server.py`, ancien stdio bas niveau et `test_server.py` racine supprimés ; Dockerfile `uvicorn server:app` ; README réécrit. **Transport stdio réel vérifié** : serveur lancé par un client MCP, 3 outils listés, `categories` exposé (manquait depuis S3 — rattrapé), appel arXiv → `isError: False`. Piège rencontré : fixture async pytest + cancel scope anyio → session ouverte dans chaque test |
| — | `chore(ruff)` | — | `known-first-party` déclaré : le hook ruff ne signale plus les imports locaux correctement groupés |

| S1 | `fix(github)` 2026-10-09 | 10 tests (8 erreurs de setup sur `_token_rejected`, `KeyError: name`, `github_token_status` absent) → **79/79** | Sonde `/rate_limit` → `absent`/`valid`/`rejected`/`unverifiable` ; 401 avec token → **un** retry sans header, avertissement en tête de sortie (`⚠️ … without authentication`), token mémorisé comme rejeté jusqu'au redémarrage ; log de session via le `lifespan` FastMCP. Smoke stdio **[Observé]** : `🦑 GitHub token: ⚠️ absent (unauthenticated: 10 searches/min)` |

**Ordre modifié (décision Greg)** : S6 avant S1, pour ne pas écrire deux fois dans le module serveur.

**Phase 1 close** (2026-10-09) : S1–S6 traités test-first, 43 → 79 tests, 7 commits sur `fix/search-quality`. Reste à vérifier en phase 2 contre l'endpoint déployé : critère S4 (vidéo officielle « Claude Code mods » présente, vues et durée affichées) et sonde du token réel (`valid` attendu).

Choix S2 validés par Greg : `days_back` optionnel (défaut `None`), qualificatif `pushed:>` ; `sort` optionnel (défaut meilleure correspondance).

Choix S3 validés par Greg : multi-mots = `AND` des termes (expression exacte sur guillemets explicites) ; `categories` optionnel ; filtre de date client supprimé.

Dette adjacente **signalée, non corrigée** : `tests/unit/test_arxiv.py` porte ~48 avertissements ruff hérités (W293, I001, SIM117) — un commit `style` séparé si Greg le souhaite.

### Phase 1 bis — Revue avant production (2026-10-09, session dédiée, CWD serveur)

`/code-review high` sur `main..fix/search-quality` : 10 findings triagés, **6 commits de correctifs** test-first, puis PR #1 mergée (`574d580`, 13:22 UTC), `main` = `origin/main`. **79 → 97 tests verts** (relancé depuis les dotfiles : `97 passed`).

| Commit | Finding corrigé |
|---|---|
| `8a3418a` `fix(youtube)` | Le message de `HTTPStatusError` embarquait l'URL, donc `key=<YOUTUBE_API_KEY>` — renvoyé aux clients et écrit dans les logs Cloud Run. Message rebâti depuis le statut + `reason`/`message` de Google ; branche `if 'error' in data` morte retirée |
| `11c8cdb` `fix(github)` | Sonde `/rate_limit` rejouée à **chaque connexion SSE** (lifespan par connexion) et verdict `rejected` jamais répercuté sur les recherches. Une sonde par processus (cache module), rejet mémorisé d'emblée |
| `1862247` `fix(youtube)` | `_fetch_details` « best effort » seulement sur `HTTPError` : corps non-JSON ou durée inconnue faisait échouer toute la recherche |
| `590f0e3` `fix(server)` | `Annotated[type, "text"]` ignoré par pydantic : aucune description ni enum dans les `inputSchema`, `query=""` atteignait l'amont. `Field(description=…)`, `Field(min_length=1)`, `Literal[…]` |
| `00a2ce7` `fix(arxiv)` | `agent "trust layer"` découpé sur les espaces en termes `all:` déséquilibrés |
| `484b140` `fix(youtube)` | `channelTitle` non décodé ; description tronquée avant décodage (coupe possible dans une entité) |

Signalé, non corrigé (PR #1) : pas de log dans `tools/` quand l'enrichissement YouTube se dégrade ; une `query` d'espaces passe `min_length=1` ; ruff hérité dans `tests/`.

### Phase 2 — Déploiement (2026-10-09, go Greg)

`gcloud run deploy tech-watch-mcp --source .` depuis `main` (`574d580`) → révision **`tech-watch-mcp-00008-mp2`** (13:35 UTC), 100 % du trafic ; précédente `00007-5kt`. Variables d'env intactes (`GITHUB_TOKEN`, `YOUTUBE_API_KEY` — noms seulement). `requirements.txt` vérifié identique à `uv export --frozen` avant le build. Repli : `gcloud run services update-traffic tech-watch-mcp --region europe-west1 --project mcp-servers-prod --to-revisions tech-watch-mcp-00007-5kt=100`.

Vérifications **[Observé]** contre `https://tech-watch-mcp-ocbwcs6sjq-ew.a.run.app/sse` (client SSE du SDK `mcp`, script de session) :

| Critère | Résultat |
|---|---|
| 3 outils, nouveaux params | `search_github_repos` (`days_back`, `sort` enum), `search_youtube_videos` (`order`, `video_duration` enums, `language`), `search_arxiv_papers` (`categories`) ; description sur chaque param, `minLength=1` sur `query` |
| GitHub `dbt` | `dbt-labs/dbt` n° 1 (⭐ 13 981), `Created: 2016-03-10 · Last push: 2026-10-09`, aucun avertissement 401 |
| arXiv `AI agent evaluation` (30 j) | 5 résultats, 4/5 pertinents (5ᵉ UAV, adjacent) — identique au local |
| **S4 live** | « Mods in Claude Code: change how Claude Code works », chaîne **Claude**, n° 2/10, 341 916 vues, **3:21** ; vues et durée sur les 10 vidéos |
| Validation (590f0e3) | `sort='popular'` et `query=''` → `isError=True` (pydantic), aucun appel amont dans les logs |
| Sonde du token réel | logs de la révision : `🦑 GitHub token: ✅ valid`, `🎬 YouTube API key: ✅ found` ; une seule sonde pour les 5 appels (cache par processus, 11c8cdb) |

Note S4 : la vidéo officielle dure 3:21, donc `video_duration="medium"` (≥ 4 min) l'aurait **exclue** — confirme le choix de laisser la skill filtrer sur `duration_seconds` plutôt que le paramètre API (K4/K5, phase 3).

**Trouvé en lisant les logs, non corrigé (hors revue)** : httpx journalise chaque requête au niveau INFO avec son URL complète, donc `youtube/v3/search?…&key=<YOUTUBE_API_KEY>` est écrit dans les logs Cloud Run à chaque recherche YouTube. **Antérieur à ce chantier** : déjà présent dans les logs de `00007-5kt` (entrée du 2026-10-09 07:34 UTC). 8a3418a n'a couvert que les messages d'erreur. Correctif d'une ligne côté serveur, `logging.getLogger("httpx").setLevel(logging.WARNING)` dans `utils/logger.py`, test-first puis révision `00009`. Rejoint le risque « endpoint public » : clé lisible par quiconque lit les logs du projet.

**Phase 2 close** (2026-10-09) : critère observé — révision `00008` active, mêmes résultats qu'en local, variables intactes.

## 6. Ce que Greg doit fournir

1. **Bloquant pour les phases 0, 3, 4** : l'export de la skill depuis Claude.ai (`.skill`, ou les quatre fichiers collés).
2. Optionnel : le rapport `tech-watch-claude-mods-2026-10-09.md` (référence E1).
3. Les décisions D1–D6, une par tour, au fil des phases.
