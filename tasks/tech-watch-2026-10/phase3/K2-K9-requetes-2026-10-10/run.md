# K2 / K9 — requêtes par outil — rejeu E2 et E1 du 2026-10-10

Items (`handover.md` §7) : K2, la normalisation en « 2-4 keywords » déclenchait
le défaut arXiv (levé côté serveur par S3) et une seule requête servait les
trois outils ; K9, gabarits Tier 2 en expression exacte sur toute la requête,
opérateur `site:a OR site:b` non garanti, outil nommé `web_search`. Critères :
K2 = plus d'arXiv hors sujet sur une requête multi-mots (E2, ≥ 4/5) ; K9 = les
recherches Tier 2 renvoient des résultats sur une requête de quatre mots.

## Changement (validé par Greg, trois choix explicites)

- `references/sources.yaml` réécrit : Tier 1 avec une règle de requête par
  outil et les paramètres à passer explicitement (arXiv `max_results=20`,
  `days_back=30`, `categories=[cs.AI, cs.LG, cs.CL, cs.SE, cs.DB]` ; GitHub
  `max_results=20`, `days_back=30`, pas de `sort` ; YouTube `max_results=15`,
  `days_back=30`, `order=relevance`, `language=en`, pas de `video_duration`) ;
  Tier 2 = trois `WebSearch` (général `{query} {année}`, communauté `{query}`
  + `allowed_domains` substack/dev.to/hashnode/medium, pratique `{query}
  tutorial OR guide`) ; Tier 3 converti en `WebSearch` + `allowed_domains`,
  **Papers With Code remplacé par Hugging Face (Papers + Blog)** (archivé en
  2025, redirigé vers HF ; une seule entrée car `WebSearch` filtre par domaine,
  pas par chemin), entrée DEV.to/Hashnode retirée (doublon du Tier 2
  communauté), Import AI / Ahead of AI par domaines. Règle de guillemets en
  tête : noms propres et expressions figées seulement.
- `SKILL.md` étapes 1–4 : une requête par outil avec deux exemples (« AI agent
  evaluation », « Claude Code mods »), paramètres explicites, Tier 2 et Tier 3
  renvoyés au YAML.

## Montage

`run-eval.sh e2-k9 "/tech-watch AI agent evaluation"` et `run-eval.sh e1-k9
"/tech-watch Claude Mods"`, montage fork (agent réel, serveur `00009`), Opus.

## Résultats **[Observé]**

| Mesure | E2 référence (09/10) | E2 rejeu (10/10) | E1-k12 (10/10, avant K2/K9) | E1 rejeu (10/10) |
|---|---|---|---|---|
| Requête arXiv | `AI agent evaluation` | `"agent evaluation"` + 5 catégories | `Claude Mods` | `"Claude Code" mods` + catégories → 0 (accepté, pas de relance) |
| Requête GitHub | `AI agent evaluation` | `agent evaluation framework` | `Claude Mods` | `claude code mods` |
| Requête YouTube | `AI agent evaluation` | `AI agent evaluation`, `language=en` | `Claude Mods` | `Claude Code mods` |
| `max_results` | 20 / 15 / 10 | 20 / 20 / 15 | omis (10 / 10 / 10) | 20 / 20 / 15 |
| Tier 2 | 3 gabarits entre guillemets | 9 / **10** / 9 liens (communauté via `allowed_domains`) | — | 9 / **10** / 9 liens (en référence E1, le gabarit `site:… OR …` rendait 0) |
| Durée / coût | 114 s, 0,64 $ | 125 s, 0,49 $ | 121 s, 0,50 $ | 128 s, 0,46 $ |
| Rapport | 20 sources | 20 (10 arXiv, 8 GitHub, 2 YouTube, 0 web) | 20 (10 YT, 7 GH, 3 web) | 20 (10 YT, 10 GH, 0 web), **en français** |

**E2, lecture stricte du top 5 arXiv** : Trust Layer for Agent Evaluation ·
Certified Selective Automation of LLM Agent Evaluation · Context-dependent
agent evaluation · EIO-Agents (semantic layer for AI agent evaluation) · Agent
Evaluation Reliability (leaderboards) → **5/5** (référence : 3/5, UAV et
Qwen-Planner dans le top 5). Sur les 20 : ≈ 15 sur le sujet, 1 hors sujet
(passerelle MCP médicale), 4 adjacents (choix collectif, simulateurs vocaux,
agents de code, revue d'allocation). **K2 : réussi.**

**K9** : chaque recherche Tier 2 renvoie 9 à 10 liens sur une requête de
trois ou quatre mots, filtre de domaine respecté. **Réussi.**

**E1** : GitHub `claude code mods` → 20 dépôts, l'homonyme `0xDarkMatter/claude-mods`
toujours dans la liste serveur (1/20, comme avant) mais **écarté** par la skill
et cité en mise en garde dans « Trends » (K10 à faire, mais second run de suite
où il est écarté). Aucun Short.

## Observations pour la suite

- **K7 (à traiter juste après)** : sur E1, les pages officielles Anthropic
  (billet de lancement, `docs/en/plugins/mods/*`) ne sont pas remontées par les
  trois recherches Tier 2 (seules les versions `de`/`it` des docs apparaissent)
  et le rapport n'en cite **aucune**, alors que E1-k12 les classait (80 et 77).
  La variance du moteur et le plafond de 20 sources suffisent à les faire
  tomber : K7 doit ajouter une recherche ciblée sur les sources primaires, pas
  s'en remettre au Tier 2 général.
- **K5/K6** : E2 classe 0 source web (comme en référence : éliminées faute de
  date) — le Tier 2 rend désormais des liens, mais la grille les jette.
- **K3** : aucune ligne « Method notes » dans l'en-tête cette fois (elle était
  spontanée en E1-k12) ; pied de page figé inchangé.
- **K11** : rapport E1 rédigé en français cette fois (E1-k12 en anglais) —
  langue instable d'un run à l'autre tant que la skill ne la fixe pas.

Transcripts : `claude/evals/results/tech-watch-{e1,e2}-k9-2026-10-10/` (gitignorés).
Rapports copiés ici : `E2-tech-watch-ai-agent-evaluation-2026-10-10.md`,
`E1-tech-watch-claude-code-mods-2026-10-10.md`.
