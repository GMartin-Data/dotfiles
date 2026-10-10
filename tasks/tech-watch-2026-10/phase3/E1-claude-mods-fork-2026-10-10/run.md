# E1 — « Claude Mods » — rejeu du 2026-10-10 après K12 (montage fork)

Preuve du critère K12 : « la skill s'exécute de bout en bout dans Claude Code »
sous l'architecture cible D3 (d). Référence : `baseline/E1-claude-mods-2026-10-09/`.

## Montage

`claude/evals/tech-watch/run-eval.sh e1-k12 "/tech-watch Claude Mods"` — même
isolation qu'en phase 0, mais : `agents/tech-watch.md` copié dans la config
isolée (`claude/agents/tech-watch.md`, serveur SSE `00009` inline), skill avec
`context: fork` + `agent: tech-watch`, **aucun `--mcp-config` ni
`--strict-mcp-config`**, `--allowedTools` étendu à `Skill,Agent,…,Edit,Bash`.
Session principale `--model opus` ; le fork tourne sur le `model: opus` de
l'agent. Skill synchronisée depuis claude.ai présente dans le sandbox
(`anthropic-skills:tech-watch`, désormais **différente** du fichier) — c'est
bien la version fichier qui a tourné : le fork a eu lieu (pool d'outils = liste
de l'agent).

## Résultat brut **[Observé]**

| Mesure | Référence (2026-10-09) | Rejeu fork (2026-10-10) |
|---|---|---|
| Durée | 171 s | **121 s** |
| Coût | 0,92 $ | **0,50 $** (Opus + Haiku pour les sous-appels web) |
| Appels d'outils | 29 dont 11 refusés (`Edit`, `Bash`) | **12, aucun refus** |
| `ToolSearch` | 1 (outils MCP différés) | 0 : les outils MCP sont dans le pool du fork |
| `references/` | 3 `Read` résolus | 3 `Read` résolus (`config/skills/tech-watch/references/…`) |
| Arguments | — | `Claude Mods` transmis au fork, requête normalisée identique |
| Tier 1 | arXiv 0 · GitHub 20 · YouTube 15 (`max_results` explicites) | arXiv 0 · GitHub 10 · YouTube 10 (`max_results` **omis**, défaut serveur) |
| Tier 2 | 3 `WebSearch` + 1 ciblée, 6 `WebFetch` (2 en erreur) | 3 `WebSearch`, 2 `WebFetch` (blog + docs `mods/create`) |
| Rapport | 20 sources, en anglais, CWD | 20 sources (17 Essential, 3 High value), en anglais, CWD |
| Fin de run | question à l'humain (classement [19]) | résumé pour l'humain en français, première ligne « mode normal » (consigne du corps de l'agent) |

Appels, dans l'ordre : 3 outils MCP (`query="Claude Mods", days_back=30`) →
`Read` ×3 → `WebSearch` ×3 → `WebFetch` ×2 → `Write`. Tier 3 non déclenché
(« > 12 relevant results », compté avant filtrage — K4 inchangé).

## Verdict contre E1 (sans changement attendu : K5 et K7 non traités)

| Attendu | Observé | Verdict |
|---|---|---|
| Sources officielles dans la tranche haute | Docs `mods/create` **80** et billet **77** en « High value » ; tranche « Essential » = vidéos 92–97. Le modèle le dit lui-même (« la grille plafonne l'autorité des sources web à 12 points ») | **Échec** (K5 reproduit, identique à la référence) |
| Aucun Short | 10 vidéos retenues, aucune < 3 min | **Réussi** |

## Observations

- **K12 rempli** : fork + serveur inline + `references/` + arguments + rapport ;
  mode dégradé non sollicité (les trois outils ont répondu).
- **K2/K9** : sans `max_results`, les outils rendent 10 résultats ; la référence
  en demandait 20 et 15. À fixer dans les requêtes par outil.
- **K10 / E6** : l'homonyme `0xDarkMatter/claude-mods` est cette fois **écarté**
  (72, « adjacent », section « Excluded or deduplicated » ajoutée hors gabarit)
  — variance d'un run à l'autre, pas une correction ; K10 reste à faire.
- **K3** : en-tête = « Method notes » hors gabarit (état par outil, pages lues) ;
  pied de page figé « arXiv · GitHub · YouTube · Web search » alors qu'arXiv
  n'a rien fourni — inchangé.
- **K6** : 2 pages lues sur 20, déclaré en tête ; « 1 740 mods en trois jours »
  et la chronologie d'avant lancement signalés non vérifiés.
- Le résumé final en français vient du global `CLAUDE.md` (« Respond in user's
  language ») lu dans la session principale et transmis au fork.

Transcript : `claude/evals/results/tech-watch-e1-k12-2026-10-10/` (gitignoré).
