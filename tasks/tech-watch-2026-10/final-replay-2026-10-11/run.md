# Rejeu final E1–E7 — 2026-10-11 (fichiers finaux de la phase 3)

Critère de la phase 3 (`plan.md` §3) : E1–E10 rejoués, comparés à `baseline/`.
E4, E8 et E10 ont été joués en K5, K6 et K4 (fiches `phase3/`) ; E9 a été
observé de façon opportuniste en K7 sur une source hors classement. Ce rejeu
couvre E1, E2, E3, E5, E6, E7 sur les fichiers finaux de la branche
(`4f05854`), tous les correctifs de la phase 3 inclus, dont les deux « signalés,
non rejoués » (titre K11, comptes de repli K3).

## Montage

`claude/evals/tech-watch/run-eval.sh`, montage fork (skill `context: fork` →
agent `tech-watch`), Opus pinné, sept sandboxes lancés **en parallèle** à
09:09:28 (Paris), un seul script enveloppe (copie gitignorée :
`claude/evals/results/final-replay-2026-10-11.sh`).

| Run | Commande | Agent, serveur |
|---|---|---|
| e1-final | `run-eval.sh e1-final "/tech-watch Claude Mods"` | agent réel, SSE `00009` |
| e2-final | `run-eval.sh e2-final "/tech-watch AI agent evaluation"` | idem |
| e3-final | `AGENT_MD=fixtures/e3/agent-stdio-invalid-token.md run-eval.sh e3-final "/tech-watch Claude Mods"` | stdio local `~/mcp-server-code` (`9fccf2b`), `GITHUB_TOKEN=invalid`, pas de clé YouTube |
| e7a-final | `run-eval.sh e7a-final "Fais-moi une veille sur les mods de Claude Code"` | agent réel, SSE `00009` (veille complète, pour observer la ligne `Request`) |
| e5a-final | `AGENT_MD=fixtures/k8/agent-stub.md EXTRA_ARGS="--max-turns 1" run-eval.sh e5a-final "What is RAG?"` | bouchon Haiku |
| e5b-final | idem + `FIXTURE_DIR=fixtures/e5`, `"Summarize this document: notes.md"` | bouchon Haiku |
| e7b-final | idem, `"Veille techno sur l'évaluation des agents IA, 30 derniers jours"` | bouchon Haiku |

E6 se juge sur le run E1 (même requête), comme en référence.

## Résultat brut **[Observé]**

| Run | Sortie | Durée | Coût | Appels (fork) |
|---|---|---|---|---|
| e1 | `exit 0`, `success`, `stderr` vide | 222 s | 0,90 $ | 3 `Read`, 3 MCP, 4 `WebSearch`, 10 `WebFetch`, 1 `Write` |
| e2 | idem | 210 s | 0,79 $ | 3 `Read`, 3 MCP, 4 `WebSearch`, 10 `WebFetch`, 1 `Write`, 1 `Edit` |
| e3 | idem | 209 s | 0,83 $ | 3 `Read`, 3 MCP, 6 `WebSearch` (dont replis `github.com`, `youtube.com`), 10 `WebFetch`, 1 `Write` |
| e7a | `exit 0`, `success`, 2 tours principaux | 256 s | 1,02 $ | `Skill` puis, dans le fork, 3 `Read`, 3 MCP, 4 `WebSearch`, 10 `WebFetch`, 1 `Write`, 2 `Edit` |
| e5a | `exit 0`, 1 tour | 6 s | 0,14 $ | **aucun** |
| e5b | `error_max_turns` (attendu), 2 tours | 2 s | 0,13 $ | `Read notes.md` seul |
| e7b | `error_max_turns` (attendu), 2 tours | 3 s | 0,13 $ | `Skill tech-watch` au tour 1 |

Total ≈ 3,94 $. Aucun `Bash` dans aucun run ; le dossier `cwd/tech-watch/`
(absent avant chaque run) a été créé par `Write` dans les quatre veilles.
Rapports : `tech-watch-claude-code-mods-2026-10-11.md` (E1, E3, E7a : **même
nom**) et `tech-watch-ai-agent-evaluation-2026-10-11.md` (E2), copiés ici
préfixés `E1-`, `E2-`, `E3-`, `E7a-`.

## Verdicts contre les scénarios (`handover.md` §8)

| E | Attendu | Référence (`baseline/`) | Rejeu final **[Observé]** | Verdict |
|---|---|---|---|---|
| E1 | Sources officielles dans la tranche haute | docs à 80, billet à 77 (High value) — **échec** | Bloc « Primary sources » : billet (2026-10-01), docs `mods/overview`, docs `mods/create`, hors classement ; vidéo officielle Claude n° 1, **A Primary 94** ; Essential = 10 (Better Stack 88, Steve Kinney 87, sept vidéos-listes à 85) | **Réussi** |
| E1 | Aucun Short | réussi (filtre par durées) | 15 vidéos renvoyées, de 3:21 à 17:27 ; 12 classées ; rien sous 180 s | **Réussi** |
| E2 | ≥ 4 arXiv pertinents sur 5 | 3/5 strict | Ordre serveur : Trust Layer for Agent Evaluation · Certified Selective Automation of LLM Agent Evaluation · Context-dependent agent evaluation with orthogonal equilibrium learning (sens « théorie des jeux », signalé par le modèle dans `Notes`) · EIO-Agents · Agent Evaluation Reliability → **4/5 strict** (K9 : 5/5) ; 13 arXiv classés sur 20 | **Réussi** |
| E3 | État par source dans l'en-tête | réussi (ligne libre) | Tableau : GitHub `degraded: ⚠️ GitHub token rejected (401) … Fallback WebSearch on github.com: 10 of the 30 raw results, 6 new, none ranked` **30/29/12** ; YouTube `failed: YouTube API key not configured. Fallback … 10 links … none ranked` **10/10/0** ; arXiv `empty` ; Tier 3 `not run` ; Owner `ok` 10/–/3 ; `Pipeline` 68 = 0 + 30 + 10 + 28 | **Réussi** |
| E3 | Pied de page fidèle | **échec** (pied figé) | `Sources used: GitHub · Web (Tier 2) · Owner domains` (ni arXiv ni YouTube) ; première ligne de chat `Report: … — 20 ranked + 3 primary — degraded: GitHub (degraded, token 401), YouTube (failed, API key not configured); …` | **Réussi** |
| E5 | Pas de déclenchement | réussi ×2 | e5a : aucun outil, définition directe ; e5b : `Read notes.md` seul, aucun `Skill` | **Réussi** ×2 |
| E6 | Dépôts sans rapport écartés | **échec** (`0xDarkMatter/claude-mods` à 72) | `0xDarkMatter/claude-mods` n° 9 des 20 dépôts renvoyés par le serveur ; absent du classement de E1, nommé dans `Notes` comme homonyme au test de sens (« a 2025 collection of skills, agents and commands ») ; même sort en E3 et E7a (1 homonyme chacun) | **Réussi** |
| E7 | Déclenchement en français | réussi ×2 | e7a : `Skill tech-watch` au tour 1, args `mods de Claude Code`, veille complète ; e7b : `Skill tech-watch` au tour 1, `PROBE: … Arguments received: évaluation des agents IA, 30 derniers jours` | **Réussi** ×2 |

**Les six scénarios rejoués réussissent** ; les deux échecs de la référence
(E1 tranche haute, E3 pied de page) et l'échec acté E6 sont corrigés par règle.

## Correctifs « signalés, non rejoués » désormais observés

- **K11, titre** : `# Tech Watch — Claude Code mods` sur E1, E3 **et E7a**
  (en K11, E7a titrait en français) ; `# Tech Watch — AI agent evaluation` sur
  E2. Ligne `Request` : `"Claude Mods"` (E1, E3), `"mods de Claude Code"`
  (E7a), `"AI agent evaluation"` (E2). E1 et E7a : même nom de fichier.
- **K3, comptes de repli** : en E3, les 10 résultats du repli `github.com`
  s'ajoutent à la ligne GitHub (30 bruts), les 10 du repli `youtube.com` à la
  ligne YouTube (10/10/0 et non `–`), et `Pipeline` égale la somme des lignes
  (68 contre 68 annoncés ; en K3 : 68 annoncés pour 58 en lignes).

## E9 sur une source classée (observé, non provoqué)

E3, source **[4]** (dev.to, Bobby Hall Jr, rang 4 à 77) : gardée et étiquetée
`⚠️ Contradicts Customize Claude Code with mods in TypeScript (claude.com/blog):
the post dates Anthropic's announcement to October 3, 2026; the announcement
is dated October 1, 2026.` Règle K7 appliquée telle quelle : affirmation hors
titre → gardée et signalée. En E1 et E7a la même page est coupée par le
plafond (77, départage), donc sans drapeau. Le point en suspens « E9 à rejouer
sur une source classée » est **couvert**.

## Observations pour Greg

1. **Dates dev.to sans année.** Les pages affichent « Posted on Oct 5 » ; les
   trois runs lisent 2026 et le déclarent dans `Notes` (contenu postérieur au
   lancement du 1er octobre). `check-dates.py` les classe `UNSOURCED` ou
   `search` : le script ne connaît ni `10/7/2026` (Kanaries), ni `Oct 06, 2026`
   (jour sur deux chiffres, Substack), ni le jour-mois sans année. Vérifié dans
   les résultats `WebFetch` : **aucune date inventée**. Décision à prendre :
   accepter l'inférence d'année déclarée (statu quo) ou imposer `unverified` ;
   dans les deux cas, élargir les graphies du script (qui ne lit pas non plus le
   bloc « Primary sources », déjà noté).
2. **Égalités sans signal d'engagement.** E1 : trois pages à 77 pour deux
   places, départagées à la longueur ; E2 : cinq sources à 72 pour deux places,
   départagées par « pertinence exacte, puis date vérifiée ». Le modèle le dit
   et invente un critère à chaque fois (K5, règle d'égalité « par engagement »).
3. **`Owner domains` sur un sujet sans propriétaire** (E2) : statut
   `not run (…)` avec un motif long dans la cellule, après la recherche de
   découverte prescrite. Le gabarit ne nomme `not run` que pour le Tier 3 ;
   comportement raisonnable, à figer dans « Header rules » si souhaité.
4. **E1 ↔ E7a** : même composition (12 vidéos, 5 web, 3 dépôts, 39 ≥ 60, même
   top 2) ; E7a a ouvert le changelog comme troisième primaire au lieu de la page
   « Create a mod » (lecture tronquée à 2.1.288, dite en `Notes`). Paraphrase
   de la ligne `Report:` par la session principale (chemin relatif), comme en
   K11 et consigné en K1.
5. **E3** : tranche Essential vide sans YouTube (K5 / K1, attendu) ; la vidéo
   officielle est nommée dans `Notes` comme non classable, conformément à la
   limitation.
6. **Montage** : sept runs en parallèle sans incident (`stderr` vides) ;
   `check-dates.py` sur E2 n'a rien à vérifier (aucune page web classée).

Transcripts, `stderr.log`, `prompt.txt`, agent utilisé :
`claude/evals/results/tech-watch-{e1,e2,e3,e5a,e5b,e7a,e7b}-final-2026-10-11/`
(gitignorés).
