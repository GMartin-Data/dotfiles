# E2 — « AI agent evaluation » — référence du 2026-10-09 (skill verbatim, serveur `00009`)

Scénario E2 (`handover.md` §8) : requête de recherche multi-mots. **Attendu** : au
moins 4 résultats arXiv pertinents sur 5. Items couverts : S3, K2.

## Montage

Identique à E1 (`../E1-claude-mods-2026-10-09/run.md`), avec les deux corrections
d'artefacts : **modèle pinné `--model opus`** (décision Greg du 2026-10-09 :
Opus 5.5 pour toute la série E1–E10, tier frontière des evals) et `Edit`, `Bash`
ajoutés à `--allowedTools`. Commande :
`claude/evals/tech-watch/run-eval.sh e2 "/tech-watch AI agent evaluation"`
(sandbox `/tmp/claude-eval-tech-watch-e2`, `MODEL=opus` par défaut).

## Résultat brut

| Mesure | Valeur [Observé] |
|---|---|
| Début / fin | 17:52:15 → 17:54:16 (Paris), `duration_ms` 113 878 |
| Sortie | `exit 0`, `subtype: success`, 12 tours, 59 lignes de transcript, aucun refus d'outil |
| Modèle | `claude-opus-5-5` (ligne d'init), Haiku pour les sous-appels `WebSearch` du harnais |
| Coût | 0,64 $ ; 11 650 tokens de sortie dont 3 672 de réflexion |
| Rapport | `tech-watch-ai-agent-evaluation-2026-10-09.md` (copié tel quel ici), 20 sources, fenêtre 30 j, en anglais |

Appels d'outils, dans l'ordre :

| # | Outil | Argument |
|---|---|---|
| 1 | `ToolSearch` | 3 outils MCP + `WebSearch` + `WebFetch` |
| 2–4 | `Read` | les trois fichiers `references/` |
| 5 | `search_arxiv_papers` | `query="AI agent evaluation", days_back=30, max_results=20` → 20 articles |
| 6 | `search_github_repos` | `days_back=30, max_results=15` → 15 dépôts |
| 7 | `search_youtube_videos` | `days_back=30, max_results=10` → 10 vidéos |
| 8–10 | `WebSearch` | les trois gabarits de `sources.yaml` |
| 11 | `Write` | rapport |

**Aucun `WebFetch`** : pas une page ouverte. Tier 3 non déclenché (« Tier 1 + 2 returned more than 12 relevant results »).

## Verdict contre E2

Les 20 articles dans l'ordre renvoyé par le serveur (tri `relevance`, requête
`all:AI AND all:agent AND all:evaluation`), jugés sur titre et extrait :

| Rang | Titre (abrégé) | Pertinence |
|---|---|---|
| 1 | Defining AI Agents: Criteria, Metrics, and Benchmarks | oui |
| 2 | Qwen-Planner-Agent: Closed-Loop AI-for-AI Framework | adjacent (cadre d'agent, pas d'évaluation) |
| 3 | Continuous Process-Level Evaluation for Enterprise AI Agent Skills | oui |
| 4 | EIO-Agents: The Missing Semantic Layer for AI Agent Evaluation | oui |
| 5 | Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs | non |
| 6–20 | SkinAgent (non) · Bounded Autonomy harness (oui) · PADMÉ meta-evaluation (oui) · Rater Effects (oui) · Measuring Scientific Intelligence (oui) · MSI-Bench (oui) · Accountability Engineering (adjacent) · VAmoS (oui) · Permission Scoping evaluation (oui, limite) · AI Scientists Coordinate (adjacent) · EvalResearchBench (oui) · Recursive self-improvement (adjacent) · Heuristic Learning competition (oui) · Share-of-Search e-commerce (non) · Medical MCP Gateway (non) | ≈ 12 oui, 4 adjacents, 4 non |

| Attendu | Observé | Verdict |
|---|---|---|
| ≥ 4 arXiv pertinents sur 5 | Top 5 : 3 sûrs + 1 adjacent (Qwen-Planner) + 1 hors sujet (UAV). Même ordre et même lecture qu'en phases 1 et 2 (« 4/5, 5ᵉ UAV »), où Qwen-Planner était compté pertinent | **Réussi sous la lecture des phases 1–2 ; 3/5 en lecture stricte.** Avant S3 : 5/5 hors sujet |
| K2 : la normalisation en 3 mots ne déclenche plus le défaut arXiv | 9 articles arXiv retenus dans le rapport, tous sur le sujet ; UAV, SkinAgent, Qwen-Planner écartés par la skill | **Réussi** |

## Observations utiles pour la phase 3

- **K6** : aucune page ouverte. Résumés arXiv « based on title and truncated abstract only », dit en tête de rapport. Les sources web du Tier 2 (Langfuse, IBM, Dataiku…) **toutes éliminées** faute de date vérifiable (0 point de fraîcheur, ≈ 65/100) : le Tier 2 n'a rien apporté au classement.
- **K5** : un talk de 1h51 à **100/100** ; `truera/trulens` (créé en 2020) à 97 grâce à la fraîcheur calculée sur le dernier push, dit par le modèle lui-même ; autorité des petites chaînes YouTube divisée par deux **hors grille** (« c'est mon ajustement, pas une règle de la grille ») ; `coze-dev/coze-loop` (plateforme généraliste) à 92.
- **K4** : « more than 12 relevant results » compté avant notation ; en pratique Tier 1 seul a fourni les 20 sources.
- **K3** : pied de page « arXiv · GitHub · YouTube · Web search » alors qu'aucune source web n'est classée.
- **K10** : dédoublonnage explicite d'un teaser de 25 s avec l'épisode complet ([3]).
- **K11** : rapport en anglais, question finale à l'humain sur la langue ; slug `ai-agent-evaluation`.
- **Grille réellement appliquée** : 12 sources en « Essential », 8 en « High value », bande 60–69 vide par construction (« only used when fewer than 20 sources score 70 or above »), interprétation du modèle, pas du gabarit.

## Fichiers

Transcript complet, `stderr.log`, `mcp.json`, `prompt.txt` et `run-eval.sh` : `claude/evals/results/tech-watch-e2-2026-10-09/` (gitignoré ; copie du sandbox `/tmp/claude-eval-tech-watch-e2`). Tableau des appels : `claude/evals/tech-watch/extract-run.sh <transcript.jsonl>`.
