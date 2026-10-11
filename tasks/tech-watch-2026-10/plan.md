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
| D3 | Comment Claude Code atteint le serveur ? | (a) déclaration directe `claude mcp add --transport sse tech-watch <url>` au scope user ; (b) OAuth du connecteur claude.ai ; (c) stdio local `uv run python server.py` ; (d) subagent `tech-watch` avec `mcpServers` inline (patron `agents/dbt.md`), skill en `context: fork` + `agent: tech-watch` | **(d) — tranché le 2026-10-09**, objection Greg (context-engineering) après un essai de (a) : au scope user, chaque session de chaque projet ouvrait une connexion SSE et chargeait les 3 outils pour une skill utilisée quelques fois par mois ; (a) retiré le jour même (`claude mcp remove tech-watch -s user`). (d) ne connecte le serveur que pendant le run et isole les fetches de la veille dans le fork. Vérifié dans la doc : `mcpServers` inline n'existe que sur les subagents (ignoré en silence dans `SKILL.md`) ; non documenté, **à sonder en phase 3 (K12)** : le serveur inline est-il connecté quand une skill fork le subagent. Référence de la phase 0 : serveur fourni à la session seule par `--mcp-config`, skill verbatim. **(c)** reste pour E3 (token bidon) et les tests avant déploiement. (b) écarté : couche OAuth inutile devant un endpoint public |
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

**Trouvé en lisant les logs, corrigé le jour même (hors revue)** : httpx journalise chaque requête au niveau INFO avec son URL complète, donc `youtube/v3/search?…&key=<YOUTUBE_API_KEY>` était écrit dans les logs Cloud Run à chaque recherche YouTube. **Antérieur à ce chantier** : déjà présent dans les logs de `00007-5kt` (entrée du 2026-10-09 07:34 UTC). 8a3418a n'a couvert que les messages d'erreur ; la ligne vient du logger `httpx` lui-même, relayé par le handler racine que le SDK `mcp` installe au démarrage.

| Étape | Résultat **[Observé]** |
|---|---|
| Branche `fix/httpx-request-logging`, test-first | `test_youtube_api_key_never_reaches_the_logs` (session MCP en mémoire + vrai client httpx sur `MockTransport`) : rouge sur `INFO httpx: HTTP Request: GET …&key=AIzaSECRET…`, vert après la ligne `logging.getLogger("httpx").setLevel(logging.WARNING)` dans `setup_logger`. **98 tests verts** |
| PR #2 mergée `9fccf2b` | 1 ligne de code + 1 test ; pas de `/code-review` (taille), travail mené depuis la session dotfiles par chemins absolus |
| Révision **`tech-watch-mcp-00009-qgq`**, 100 % | recherche `Claude Code mods` → 3 vidéos avec vues/durée ; logs de la révision : `Searching YouTube` → `Found 3 videos` **sans ligne `HTTP Request`**, 0 entrée contenant `key=` (contre une par appel sur `00008`). Sonde `✅ valid` inchangée |

Reste à la main de Greg : les logs des révisions ≤ `00008` contiennent la clé (rétention Cloud Logging 30 j par défaut) — rotation de `YOUTUBE_API_KEY` dans la console Google puis `gcloud run services update --update-env-vars` si l'on veut fermer le risque, et non seulement le tarir.

**Phase 2 close** (2026-10-09) : critère observé — révision `00009` active (`00008` validée puis remplacée par le correctif httpx), mêmes résultats qu'en local, variables intactes.

### Phase 0 — Import et référence (2026-10-09 → 2026-10-10, export reçu le 09)

| Étape | Résultat **[Observé]** |
|---|---|
| 1. Import | `~/Téléchargements/tech-watch-skill.zip` (4 fichiers, datés du 2026-10-08 14:18) décompressé dans `claude/skills/tech-watch/`, tailles identiques à l'archive, **aucun symlink** (D2a). Commit `e9609c3` |
| 2. Serveur | D3 (a) essayé (`claude mcp add --scope user`, `✔ Connected`) puis **retiré le jour même** sur objection de Greg (context-engineering) ; D3 révisé en **(d)** : subagent à `mcpServers` inline + skill en `context: fork`, à construire en phase 3 (K12). Noms vérifiés par sonde en session neuve : `mcp__tech-watch__search_{arxiv_papers,github_repos,youtube_videos}`, outil web `WebSearch`. Commit `cef27c1` |
| 3. Référence | 6 scénarios joués ou actés, sorties datées dans `baseline/<E>-<slug>-<date>/` (rapport tel quel + `run.md` : montage, appels, verdict, observations). **Critère de phase rempli** : la skill tourne de bout en bout (E1, 171 s, 20 sources) |

Montage des runs (réutilisable en phase 3) : `claude/evals/tech-watch/run-eval.sh <id> "<prompt>"` — sandbox `/tmp/claude-eval-tech-watch-<id>` selon le patron batch A (`CLAUDE_CONFIG_DIR` isolé : copie verbatim de la skill, global `CLAUDE.md`, aucun hook, ancienne command et agent absents), serveur fourni à la session seule par `--mcp-config` + `--strict-mcp-config`, `--model opus` ; variables `EXTRA_ARGS` (sondes `--max-turns 2`), `FIXTURE_DIR`, `MCP_JSON` (E3 : stdio local, `fixtures/e3/`). Tableau des appels par `extract-run.sh`. Transcripts dans `claude/evals/results/tech-watch-<id>-<date>/`, **gitignorés** comme le batch A.

| E | Attendu (passation §8) | Observé | Verdict |
|---|---|---|---|
| E1 « Claude Mods » | Sources officielles dans la tranche haute ; aucun Short | Docs officielles 80 et billet 77 en « High value », tranche haute menée par une vidéo communautaire (97) et trois catalogues (92) ; 7 vidéos de 3:21 à 12:47 | **Échec / Réussi** (K5 reproduit ; S4 tient) |
| E2 « AI agent evaluation » | ≥ 4 arXiv pertinents sur 5 | Top 5 : 3 sûrs + Qwen-Planner (adjacent) + UAV (non) ; 9 arXiv retenus, tous sur le sujet | **Réussi** sous la lecture des phases 1–2 (3/5 en lecture stricte) ; K2 réussi |
| E3 GitHub 401 (+ YouTube sans clé en local) | État par source en en-tête ; pied de page fidèle | En-tête « Partially degraded mode » détaillé par source ; pied de page figé « arXiv · GitHub · YouTube · Web search » ; S1 : avertissement + 20 dépôts, une seule sonde 401 | **Réussi / Échec** (K3 reproduit côté pied de page) ; S1 réussi |
| E5 non-déclenchement | La skill ne se déclenche pas | « What is RAG? » : 0 outil ; « Summarize this document » (fixture `fixtures/e5/notes.md`, sujet proche d'une veille) : `Read` seul | **Réussi** ×2 |
| E6 homonymes (acté sur E1, décision Greg) | Les dépôts sans rapport sont écartés | Serveur : 1 homonyme sur 20 (`0xDarkMatter/claude-mods`, contre 2/10 avant S2) ; la skill l'a **retenu** à 72, étiqueté « adjacent » | **Échec** (K10 reproduit) |
| E7 déclenchement FR | La skill se déclenche | `Skill tech-watch` au tour 1 sur « Fais-moi une veille sur… » et « Veille techno sur… » | **Réussi** ×2 |

Non joués : E4 (`days_back=60`), E8 (pages illisibles), E9 (contradiction), E10 (bruit massif) — décrits dans la passation, une veille complète chacun (≈ 0,9 $, 3 min), à jouer si besoin avant ou après la phase 3. Coût de la série jouée ≈ 3,9 $.

Décisions Greg (track léger) : **Opus 5.5 pour toute la série E1–E10** (E1 avait tourné sur Opus par défaut du CLI alors que Fable était annoncé ; tier frontière des evals, à ne rouvrir qu'en cas de fort désaccord) ; E6 acté sur E1 sans rejeu ; fixture E5 validée après explication.

Observations transverses pour la phase 3 (détail dans chaque `run.md`) :
- **K5** : la grille élimine le Tier 2 en entier faute de date (E2 : 0 source web classée) et fait dépendre le rang des sources primaires d'une interprétation refaite à chaque run (E1 docs 80 → E3 docs 88, même requête). Six dépôts à égalité à 89 (E3). Ajustements hors grille déclarés par le modèle (petites chaînes, « lead magnet »).
- **K6** : 0 à 6 pages ouvertes par veille, jamais 25 ; données non vérifiées déclarées comme telles en tête de rapport (bon comportement obtenu sans règle).
- **K3** : état par source en en-tête obtenu spontanément, pied de page figé par le gabarit.
- **K4** : Tier 3 jamais déclenché, le compte se fait avant filtrage.
- **K12** : Claude Code synchronise la skill du compte claude.ai dans chaque session (`skills/synced/<org>_<user>/tech-watch`, exposée `anthropic-skills:tech-watch`), identique à l'export aujourd'hui ; **dès que la version fichier divergera, deux skills coexisteront** — retirer ou renommer la skill côté claude.ai au moment de la phase 3. Point non documenté à sonder en ouverture de phase 3 : le `mcpServers` inline d'un subagent est-il connecté quand une skill le fork.
- **K8** : ni faux positif ni faux négatif sur Opus ; les sondes E5/E7 servent de garde de non-régression à l'enrichissement de la description.

**Phase 0 close** (2026-10-10).

### Phase 3 — Skill (ouverte le 2026-10-10)

#### K12 — portabilité (2026-10-10)

Sonde du point non documenté, trois variantes (`claude/evals/tech-watch/probe-k12.sh`,
détail dans `phase3/K12-probe-2026-10-10.md`) :

| Variante | Résultat **[Observé]** |
|---|---|
| Skill `context: fork` → agent à `mcpServers` inline (SSE `00009`) | **Serveur connecté** : pool = liste `tools:` de l'agent (3 outils MCP + `WebSearch` + `Read`), `search_github_repos("dbt")` → `dbt-labs/dbt`. 12 s, 0,05 $ |
| Témoin sans fork | Aucun `mcp__tech-watch__*` dans la session principale, `RESULT: UNAVAILABLE` |
| Serveur injoignable (`.invalid`) | Le fork démarre, outils MCP **silencieusement absents** (ni `stderr`, ni ligne système) ; pool = `WebSearch`, `Read` |

Conséquences inscrites :

| Fichier | Changement |
|---|---|
| `claude/agents/tech-watch.md` (nouveau) | Agent cible de D3 (d) : `tools: mcp__tech-watch__*, WebSearch, WebFetch, Read, Write, Edit` (liste tirée du run E1 de référence : `Bash`, `Glob`, `Grep` jamais utiles), `model: opus`, serveur SSE inline, corps court (suivre la skill, règle « outils absents = serveur injoignable », résumé final pour l'humain) |
| `claude/skills/tech-watch/SKILL.md` | `context: fork` + `agent: tech-watch` ; `web_search` → `WebSearch` (5 occurrences) ; dernière limitation étendue à « outils **absents** de la liste ou en échec », annonce en première ligne de la réponse + note « Degraded mode » en en-tête |
| `claude/evals/tech-watch/run-eval.sh` | Montage fork : copie de l'agent dans `config/agents/`, **plus de `--mcp-config` / `--strict-mcp-config`** (le mode strict bloque aussi les serveurs du frontmatter d'un subagent — doc sub-agents), `AGENT_MD` remplace `MCP_JSON`, `--allowedTools` étendu (`Skill`, `Agent`, `Edit`, `Bash` : les 11 refus du run E1 de référence) |
| `fixtures/e3/agent-stdio-invalid-token.md` | Remplace `mcp-stdio-invalid-token.json` : même serveur stdio local, `GITHUB_TOKEN=invalid`, sous forme d'agent (syntaxe `env:` du frontmatter **à vérifier au rejeu E3**) |

**Critère K12 observé** : E1 rejoué sous le montage fork
(`phase3/E1-claude-mods-fork-2026-10-10/`) — 12 appels sans refus, `references/`
résolus dans le fork, arguments transmis, rapport de 20 sources écrit dans le
CWD, 121 s et 0,50 $ (contre 171 s et 0,92 $ en référence). Verdict E1 inchangé
(K5 reproduit, aucun Short), comme attendu avant K5. Notes pour la suite : sans
`max_results` explicite les outils rendent 10 résultats (K2/K9) ; l'homonyme E6
écarté cette fois par variance, pas par règle (K10).

Points pour Greg :
1. ~~**`model: opus` figé dans l'agent** — aligné sur la décision « Opus 5.5 pour la
   série E1–E10 » ; le choix pour l'usage réel (Fable par défaut, Opus en
   repli) reste à trancher avant la phase 4.~~ — **Tranché par Greg le
   2026-10-11 : Opus conservé** pour l'usage réel. Tarif 2,5 fois moindre que
   Fable (4 $ / 20 $ contre 10 $ / 50 $ par million de tokens, soit ≈ 1 $ la
   veille contre ≈ 2,5 $) ; règles de la skill calibrées et validées sur Opus
   seulement (≈ 30 runs, aucun sur Fable), donc livrer ce qui a été testé. Le
   pin `model: opus` suit l'alias, les evals restent rejouables. Aucun
   changement de fichier.
2. ~~**Skill claude.ai à retirer ou renommer maintenant**~~ — **supprimée par
   Greg le 2026-10-10** (Customize > Skills > … > Delete ; recommandation :
   supprimer plutôt que renommer, car le déclenchement se fait sur la
   description, pas sur le nom). Sonde **[Observé]** dans un sandbox neuf
   (`run-eval.sh sync-check`, `--max-turns 1`) : 23 skills synchronisées
   depuis le compte, aucune `tech-watch` ; `slash_commands` à l'init ne liste
   que la `tech-watch` fichier. Le doublon n'existe plus ; le zip d'origine
   reste dans `~/Téléchargements` et le verbatim dans `e9609c3`.

#### K8 — description et déclencheurs (2026-10-10)

`SKILL.md` : description réécrite sur le patron maison (fonction, six
phrases-types FR/EN citées, « Do not use for » avec les quatre cas négatifs) ;
section « Negative cases » du corps supprimée (remontée dans la description, où
elle filtre avant déclenchement). Détail et transcripts :
`phase3/K8-declenchement-2026-10-10.md`.

| Sonde | Rejeu **[Observé]** | Verdict |
|---|---|---|
| E5a `What is RAG?` | 0 outil, réponse directe | Réussi |
| E5b `Summarize this document: notes.md` | `Read` seul | Réussi |
| E7a « Fais-moi une veille sur… » | `Skill tech-watch` au tour 1, veille menée par le fork (0,75 $) | Réussi |
| E7b « Veille techno sur… » | `Skill tech-watch` au tour 1, veille menée par le fork, puis `error_max_turns` au tour 3 de la session principale (artefact) | Réussi |

**Critère K8 observé** : E5 ×2 et E7 ×2 identiques à la référence, la
description enrichie n'a créé ni faux positif ni faux négatif sur Opus.

Montage : sous le fork, `--max-turns` ne borne pas le subagent, une sonde E7
coûte une veille entière. Ajout de `fixtures/k8/agent-stub.md` (agent `tech-watch`
bouchon, Haiku, sans serveur, répond `PROBE: … Arguments received: …`) :
validé sur E7a (0,15 $, 8 s, args transmis). Recette des rejeux E5/E7 :
`AGENT_MD` = bouchon, `--max-turns 1`.

#### K2 / K9 — requêtes par outil (2026-10-10)

Proposition validée par Greg (catégories arXiv `cs.AI, cs.LG, cs.CL, cs.SE,
cs.DB` ; YouTube `language=en` sauf demande en français ; Papers With Code
remplacé par Hugging Face Papers). `sources.yaml` réécrit (règle de requête et
paramètres explicites par outil Tier 1 ; Tier 2 = trois `WebSearch`, la
communautaire par `allowed_domains` ; Tier 3 converti en `WebSearch` +
`allowed_domains`, DEV.to/Hashnode retiré car doublon du Tier 2) ; `SKILL.md`
étapes 1–4 (une requête par outil, deux exemples). Détail et rapports :
`phase3/K2-K9-requetes-2026-10-10/`.

| Critère | Rejeu **[Observé]** | Verdict |
|---|---|---|
| K2 / E2 : ≥ 4 arXiv pertinents sur 5 | `"agent evaluation"` + catégories → **5/5** en lecture stricte (référence 3/5) ; ≈ 15/20 sur le sujet | **Réussi** |
| K9 : Tier 2 renvoie des résultats sur quatre mots | 9 / 10 / 9 liens par recherche sur E2 comme sur E1 ; la recherche communautaire rendait 0 en référence | **Réussi** |
| E1 (contrôle) | `claude code mods` → 20 dépôts, homonyme écarté par la skill, aucun Short ; **aucune page officielle Anthropic dans le rapport** (non remontées par le Tier 2 ce run) | inchangé sur K5 ; **à traiter en K7** |

#### K4 — filtre rapide avant comptage, Tier 3 (2026-10-10)

Règle validée par Greg (coupe vidéo < 3 min binaire ; adjacents hors du compte
des 12 ; sujet E10 au choix de Claude) : `SKILL.md` étapes 4 (filtre
on-topic / adjacent / off-topic sur titre et description, vidéos < 180 s et
résultats sans titre écartés), 5 (dédoublonnage, remonté avant le comptage
après E10b) et 6 (Tier 3 si on-topic uniques < 12, par priorité, arrêt à 12 ou
à épuisement). Détail, trois rapports : `phase3/K4-tier3-2026-10-10/`.

| Run E10 | Comptes **[Observé]** | Tier 3 |
|---|---|---|
| MCP elicitation | 63 bruts, 38 on-topic | non, motivé (« on-topic >= 12 ») |
| Apache Iceberg variant type | 42 bruts, 21 on-topic (14 uniques) | non — a révélé le comptage avant dédoublonnage, corrigé |
| Apache Iceberg row lineage | 94 bruts, 11 on-topic (7 uniques), 47 adjacents, 36 off-topic | **oui, 6 entrées, épuisé sans atteindre 12** |

**Critère K4 observé** : 83 résultats adjacents ou hors sujet n'ont pas dispensé
du Tier 3. Coût des trois runs : 1,87 $.

Point pour Greg (contenu, pas mécanisme) : le Tier 3 de `sources.yaml` est
entièrement orienté IA et n'a rien rendu sur un sujet data engineering — à
compléter par des domaines data, ou à laisser au modèle le soin de proposer
des domaines par sujet.

#### K6 — enrichissement budgété, « non vérifié » (2026-10-10)

Règle validée par Greg (budget 10 pages, échecs compris ; Tier 1 jamais ouvert ;
E8 par retrait de `WebFetch`) : `SKILL.md` étape 7 (candidats web on-topic
seulement, une ouverture par URL sans relance, trois valeurs extraites,
provenance admise = outil Tier 1, page ouverte, chemin d'URL, sinon
`unverified`) ; `report-template.md` admet `unverified` pour date et autorité.
Outil : `claude/evals/tech-watch/check-dates.py` (provenance de chaque date de
source web depuis le transcript). Détail : `phase3/K6-enrichissement-2026-10-10/`.

| Run | **[Observé]** | Verdict |
|---|---|---|
| E8a, `WebFetch` retiré | « 0 pages opened out of a budget of 10 … `unverified` for all 20 unique web candidates », aucune relance, aucune date inventée | Réussi |
| E8b, normal | 10 pages sur 10, 10 URL distinctes, 0 échec ; 4 pages sans année → `unverified` ; aucune date inventée | Réussi |

**Critère K6 observé** sur les deux runs. Limite : aucune source web dans les
deux top 20 (non vérifiée = 59 max, vérifiée = 85 max, contre 84–97 pour le
Tier 1), donc le marquage par source n'est attesté qu'en en-tête — visible dès
que K5 laissera passer le web. Confirmé pour K7 : les pages officielles
Anthropic ne remontent pas par le Tier 2 général (deux runs de suite).

#### K7 — sources primaires d'abord, contradictions (2026-10-10)

Règle validée par Greg (bloc « Primary sources » hors classement ; contradiction
écartée si dans le titre, sinon gardée et signalée ; 3 pages du budget
réservées ; AWS et Azure ajoutés aux propriétaires connus à sa demande) :
`SKILL.md` étape 3 (propriétaire du sujet, `WebSearch` sur ses domaines, page
localisée → page `en`, ouverture en premier), étapes renumérotées 1–10 ;
`sources.yaml` section `primary_sources.known_owners` (9 propriétaires) ;
`report-template.md` bloc « Primary sources ». Détail :
`phase3/K7-sources-primaires-2026-10-10/`.

| Critère | Rejeu E1 **[Observé]** | Verdict |
|---|---|---|
| Sources primaires citées quand elles existent | Recherche ciblée exécutée avant le Tier 2 ; billet, docs `en` et changelog ouverts en premier (3 des 10 pages) ; bloc « Primary sources » à 3 entrées + 4 pages officielles non ouvertes. Quatre runs auparavant n'avaient que des docs localisées | **Réussi** |
| E9, contradiction signalée ou écartée | Article dev.to datant le lancement au 3 octobre contre le 1er dans l'annonce : signalé dans « Trends » (source hors top 20) | **Réussi** (opportuniste ; à rejouer sur une source classée) |

Coût 0,77 $, 206 s (+1 recherche, +3 pages). Top 20 toujours 100 % Tier 1 : K5.

#### K5 — grille de notation (2026-10-10, tour dédié)

Grille validée par Greg (autorité par nature A/B/C/D, créateurs et dépôts
communautaires en C ; date `unverified` à 5 et adjacents hors classement ;
seuil 60 strict avec note de couverture, clause de repli supprimée) :
`scoring-criteria.md` réécrit (fraîcheur relative à la fenêtre, dépôt sur sa
date de création sinon push plafonné à 10, profondeur par type, tranches
renommées, égalités par engagement) ; gabarit (autorité par lettre, section
« Adjacent, not ranked ») ; `SKILL.md` étape 9. Détail et deux rapports :
`phase3/K5-grille-2026-10-10/`.

| Critère | Rejeu **[Observé]** | Verdict |
|---|---|---|
| E1 : docs et annonce dans la tranche la plus haute, aucun Short | bloc « Primary sources » à 3 entrées ; vidéo officielle Claude n° 1, **A Primary 94**, seule au-dessus de 85 ; vidéos-listes communautaires de 97 à **85** ; **3 sources web classées** (première fois depuis K12) ; dépôts sur leur date de création ; 0 Short | **Réussi** |
| E4 : sources de 31 à 60 jours non éliminées (`days_back=60`) | sources de 37–39 jours à 77 (fraîcheur 10), de 30 jours à 82 ; dépôt ancien maintenu plafonné (80 au lieu de 90) ; 2 échecs de `WebFetch` laissés `unverified` | **Réussi** |

Coût 1,36 $. À surveiller : frontière B/C (jugement du modèle, E4 tout en B)
et plateau à 85 des vidéos-listes (levier engagement ou seuil de tranche, non
touché).

#### K10 — homonymes, dédoublonnage élargi (2026-10-10)

Règle validée par Greg (test de date adossé à la source primaire ; plafond de
2 entrées par auteur, chaîne ou organisation ; réécritures sans apport en D) :
`SKILL.md` étape 5 (tests de date et de sens → étiquette `homonym`, compte en
en-tête) et étape 6 (variantes d'une page, teaser/complet, plafond par auteur,
repli dans le résumé) ; `scoring-criteria.md` D étendu. Détail et deux
rapports : `phase3/K10-homonymes-2026-10-10/`.

| Run | **[Observé]** | Verdict |
|---|---|---|
| E1a, règle initiale | 10 homonymes dont `0xDarkMatter/claude-mods` ; **mais** le test de date (référence = annonce du 1er octobre) a écarté 4 dépôts de la préversion de mi-septembre, dont le plus étoilé du sujet — signalé par le modèle lui-même | critère rempli, dommage collatéral |
| Correctif | référence = **plus ancienne** date établie par une source primaire (préversion comprise) ; préversion mentionnée sans date → test de date sauté | — |
| E1b, règle corrigée | test de date sauté (motif explicite), 5 homonymes au test de sens, `0xDarkMatter` absent du rapport, dépôts de la préversion de retour (62–64, sous le plafond), aucun auteur à plus d'une entrée, dépôt compagnon replié | **Réussi** (E6) |

Coût 1,52 $.

#### K3 — état par source, pied de page dérivé (2026-10-10)

Format proposé puis validé par Greg (pied de page **dérivé** du tableau plutôt
que supprimé) : `report-template.md` en-tête à lignes fixes (métadonnées avec
`Topic` et propriétaire ; tableau d'état par source à 6 lignes, statuts fermés
`ok` / `empty` / `degraded` / `failed` / `absent` / `not run` ; lignes
`Pipeline`, `Enrichment`, `Date test`, `Notes` ≤ 5 puces), pied de page
`Sources used` = lignes à `In report` ≥ 1, section « Header rules » ;
`SKILL.md` étape 10 et limitation « Degraded mode » (un ou plusieurs outils,
tableau au lieu d'une note). Détail et rapport :
`phase3/K3-etat-par-source-2026-10-10/`.

| Run | **[Observé]** | Verdict |
|---|---|---|
| E3 (stdio local, `GITHUB_TOKEN=invalid` par `env:` du frontmatter, pas de clé YouTube) | Tableau : GitHub `degraded` (401, repli github.com 10 résultats, 6 nouveaux) 20/19/15, YouTube `failed` (repli youtube.com, 10 résultats, aucun classable) –/–/0, arXiv `empty`, Tier 3 `not run`, Owner domains 10/–/3 ; pied de page `Sources used: GitHub · Web (Tier 2) · Owner domains` ; `Date test: skipped` motivé | **Réussi** (E3, les deux attendus) |
| Correctif après le run | `Pipeline` 68 contre une somme de lignes à 58 : les résultats de repli comptent désormais dans la ligne de l'outil remplacé, `–` seulement sans demande ni repli | signalé, non rejoué (comptes, pas statuts) |

Coût 0,83 $. Syntaxe `env:` du `mcpServers` inline **vérifiée** (avertissement
« rejected (401) », pas « absent »). Observations : tranche Essential vide sans
YouTube (K5) ; deux dépôts Anthropic en bloc primaire sans ouverture (K7) ;
résumé de chat en français, rapport en anglais (K11).

#### K11 — slug, langue, emplacement, livraison (2026-10-10)

Deux décisions Greg, une par tour : **rapport en anglais fixe** (résumé de chat
dans la langue de la demande) ; **dossier fixe `/home/martin/tech-watch/`**,
créé si absent, chemin de la demande prioritaire. Règles : `SKILL.md` étape 1
(slug = sujet normalisé, minuscules, ASCII, tirets) et étape 10 (nom
`tech-watch-{slug}-{date}.md`, `-{days}d` hors fenêtre 30, même nom = remplace,
emplacement, langue) ; `agents/tech-watch.md` et fixture E3 (dossier, première
ligne de chat `Report: <chemin> — n ranked + m primary — normal | degraded: …`) ;
`run-eval.sh` réécrit le dossier en `cwd/tech-watch/` du sandbox sans le
pré-créer. Détail et deux rapports : `phase3/K11-sortie-2026-10-10/`.

| Run | **[Observé]** | Verdict |
|---|---|---|
| E1 `/tech-watch Claude Mods` | `cwd/tech-watch/tech-watch-claude-code-mods-2026-10-10.md`, dossier créé par `Write`, rapport anglais, première ligne `Report: … — 20 ranked + 3 primary — normal`, résumé français | **Réussi** |
| E7a `Fais-moi une veille sur les mods de Claude Code` | **même nom de fichier**, dossier créé, rapport anglais (titre en français : gabarit `{query}`), ligne `Report:` produite par le fork puis **paraphrasée par la session principale** (chemin relatif, comptes conservés) | **Réussi** (critère K11) ; livraison partielle sous déclenchement en langage naturel, fonctionnement du fork |
| Correctif après les runs | titre du gabarit = sujet normalisé, demande tapée en métadonnée `Request` | signalé, non rejoué |

Coût 1,82 $. À reporter : permission `Write` hors CWD en session interactive
(phase 4, `install.sh` / README) ; paraphrase de la livraison (K1).

#### K1 — limitations réécrites d'après les comportements observés (2026-10-10)

Texte validé par Greg, sans run : chaque ligne adossée à une fiche de la
phase 3 (traçabilité dans `phase3/K1-limitations-2026-10-10.md`). Supprimées,
jamais reproduites : arXiv `301`, YouTube « < 48 h », paywall. Réécrites :
GitHub 401 (un retry sans auth, 10 recherches/min, avertissement en tête,
`degraded`), serveur injoignable (outils absents sans erreur, K12 `down`).
Nouvelles : YouTube sans clé (`failed`, repli non classable, Essential
possiblement vide), arXiv `empty` sur un sujet produit, `WebFetch` absent ou
budget épuisé (`unverified`, plafond 59), lecture tronquée ≈ 100 000
caractères, paraphrase de la ligne `Report:` sous déclenchement en langage
naturel. Laissé dehors faute d'observation : permission `Write` hors CWD
(phase 4). **Critère rempli** (chaque limitation reproductible). Coût 0 $.

#### Rejeu final E1–E7 (2026-10-11, fichiers finaux)

Sept sandboxes en parallèle (`run-eval.sh`, Opus, serveur `00009` ; E3 en
stdio local avec `GITHUB_TOKEN=invalid` ; E5/E7b sur le bouchon,
`--max-turns 1` ; E7a en veille complète). Détail, quatre rapports :
`final-replay-2026-10-11/`.

| E | Référence | Rejeu final **[Observé]** | Verdict |
|---|---|---|---|
| E1 | docs 80, billet 77 — échec ; aucun Short | bloc « Primary sources » à 3 entrées, vidéo officielle n° 1 A Primary 94, Essential = 10 ; 15 vidéos de 3:21 à 17:27 | **Réussi** ×2 |
| E2 | 3/5 strict | 4/5 strict (le 3ᵉ au sens « théorie des jeux », signalé par le modèle), 13 arXiv classés | **Réussi** |
| E3 | en-tête libre ; pied figé — échec | GitHub `degraded` 30/29/12 (repli compté dans la ligne), YouTube `failed` 10/10/0, `Pipeline` = somme des lignes ; pied `GitHub · Web (Tier 2) · Owner domains` ; ligne de chat `degraded: GitHub (…), YouTube (…)` | **Réussi** ×2 |
| E5 | réussi ×2 | e5a 0 outil ; e5b `Read` seul | **Réussi** ×2 |
| E6 | `0xDarkMatter` à 72 — échec | n° 9 côté serveur, écarté au test de sens dans E1, E3 et E7a | **Réussi** |
| E7 | réussi ×2 | e7a `Skill` au tour 1, veille complète, même fichier que E1 ; e7b `Skill` au tour 1, ligne `PROBE:` | **Réussi** ×2 |

Observés au passage : titre K11 au sujet normalisé et ligne `Request` sur les
quatre rapports ; comptes de repli K3 ; **E9 sur une source classée** (E3,
rang 4, dev.to datant l'annonce au 3 octobre : gardée et étiquetée
`⚠️ Contradicts …`), ce qui couvre le point en suspens. Coût 3,94 $.

Points pour Greg (détail dans la fiche) : dates dev.to sans année lues comme
2026 et déclarées (aucune date inventée ; `check-dates.py` ne connaît pas les
graphies `10/7/2026`, `Oct 06, 2026`, jour-mois seul) ; égalités sans signal
d'engagement départagées par un critère inventé (E1, E2) ; `Owner domains` à
`not run (…)` sur un sujet sans propriétaire (E2).

**Critère de la phase 3 observé** : E1–E10 rejoués (E4, E8, E10 en K5, K6, K4),
comparés à `baseline/` ; chaque critère K* coché avec preuve.

**Phase 3 close** (2026-10-10, rejeu final le 2026-10-11) : 11 items sur 11.

## 6. Ce que Greg doit fournir

1. ~~**Bloquant pour les phases 0, 3, 4** : l'export de la skill depuis Claude.ai (`.skill`, ou les quatre fichiers collés).~~ **Reçu le 2026-10-09** (`tech-watch-skill.zip`), importé en `e9609c3`.
2. Optionnel : le rapport `tech-watch-claude-mods-2026-10-09.md` (référence E1).
3. Les décisions D1–D6, une par tour, au fil des phases.
