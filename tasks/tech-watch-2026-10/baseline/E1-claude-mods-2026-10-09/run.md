# E1 — « Claude Mods » — référence du 2026-10-09 (skill verbatim, serveur `00009`)

Scénario E1 (`handover.md` §8) : fonctionnalité produit récente. **Attendu** :
sources officielles dans la tranche haute, aucun Short. Items couverts : K5, K7, S4.

## Montage

Skill importée verbatim (`e9609c3`), jamais modifiée. Serveur Cloud Run révision
`tech-watch-mcp-00009-qgq` (phase 2 close). Isolation selon le patron
`claude/evals/claude-md/setup-eval-cwd.sh` : `CLAUDE_CONFIG_DIR` dédié, aucun
hook, l'ancienne command `/tech-watch` et l'agent `tech-watch-scorer` absents
(vérifié par sonde avant le run), global `claude/CLAUDE.md` présent comme en
usage réel, serveur fourni à la session seule par `--mcp-config` +
`--strict-mcp-config` (connecteurs claude.ai et context7 écartés).

```bash
RUN=/tmp/claude-eval-tech-watch-e1
# config/ : skills/tech-watch (copie verbatim), CLAUDE.md (global), .credentials.json (lien),
#           .claude.json (copie), settings.json = {}
# mcp.json : {"mcpServers":{"tech-watch":{"type":"sse","url":"https://tech-watch-mcp-ocbwcs6sjq-ew.a.run.app/sse"}}}
cd $RUN/cwd && CLAUDE_CONFIG_DIR=$RUN/config claude -p "/tech-watch Claude Mods" \
  --mcp-config $RUN/mcp.json --strict-mcp-config \
  --allowedTools "WebSearch,WebFetch,mcp__tech-watch,Read,Write,Glob,Grep" \
  --output-format stream-json --verbose < /dev/null > $RUN/transcript.jsonl
```

Constat de montage : Claude Code synchronise les skills du compte claude.ai dans
chaque session (`skills/synced/<org>_<user>/tech-watch`, exposée comme
`anthropic-skills:tech-watch`). Contenu identique octet pour octet à l'export au
moment du run (`diff -r`), donc sans effet ici. **À traiter en phase 3 (K12)** :
dès que la version fichier diverge, deux skills `tech-watch` coexisteront.

## Résultat brut

| Mesure | Valeur [Observé] |
|---|---|
| Début / fin | 17:20:57 → 17:23:50 (Paris), `duration_ms` 171 016 |
| Sortie | `exit 0`, `subtype: success`, 30 tours, 125 lignes de transcript |
| Modèle | **`claude-opus-5-5`** (défaut du CLI dans la config isolée, `settings.json` vide), Haiku pour les sous-appels `WebSearch`/`WebFetch` du harnais |
| Coût | 0,92 $ (Opus 0,86 + Haiku 0,05) ; 16 636 tokens de sortie dont 4 139 de réflexion |
| Rapport | `tech-watch-claude-mods-2026-10-09.md` (copié tel quel ici), 20 sources, fenêtre 30 j, en anglais |

Appels d'outils, dans l'ordre :

| # | Outil | Argument |
|---|---|---|
| 1 | `ToolSearch` | chargement des 3 outils MCP + `WebSearch` + `WebFetch` |
| 2–4 | `Read` | `sources.yaml`, `scoring-criteria.md`, `report-template.md` (chemins `references/` résolus) |
| 5 | `search_arxiv_papers` | `query="Claude Mods", days_back=30` → **0 article** |
| 6 | `search_github_repos` | `query="Claude Mods", days_back=30, max_results=20` → 20 dépôts, `karanb192/awesome-claude-code-mods` n° 1 |
| 7 | `search_youtube_videos` | `query="Claude Mods", days_back=30, max_results=15` → 15 vidéos, n° 1 hors sujet (« Claude Slides », 1:45) |
| 8–10 | `WebSearch` | `"Claude Mods" 2026` · `site:substack.com OR site:dev.to OR site:hashnode.dev` (vide) · `tutorial guide walkthrough` |
| 11–16 | `WebFetch` | blog officiel, docs `mods/overview`, developersdigest, pasqualepillitteri (**erreur réseau**), levelup.gitconnected (**403**), stationx |
| 17 | `WebSearch` | Pluto Security (recherche ciblée) |
| 18 | `Write` | rapport |
| 19 | `Bash` | `python3 -I` pour déplacer un bloc — **refusé** (non autorisé) |
| 20–29 | `Edit` ×10 | renumérotation [10]–[19] — **refusés** (`Edit` absent de `--allowedTools`) |

Tier 3 non déclenché (20 + 15 résultats Tier 1 comptés comme « pertinents » avant filtrage).

## Verdict contre E1

| Attendu | Observé | Verdict |
|---|---|---|
| Sources officielles dans la tranche haute | Tranche « Essential » (85–100) : vidéo Better Stack **97**, dépôt `anthropics/claude-code/mods` 95, vidéo officielle Claude 94, trois catalogues communautaires 92, vidéos listicles 89. **Docs officielles `mods/overview` et `mods/create` : 80, billet de lancement : 77**, tous en « High value » | **Échec** (K5 reproduit ; même ordre de grandeur que le test claude.ai : docs 80, annonce 74, dépôt communautaire 90) |
| Aucun Short | 7 vidéos retenues, durées 3:21 à 12:47 ; le Short et les hors-sujet du Tier 1 écartés grâce aux durées et vues désormais renvoyées par le serveur (S4) | **Réussi** |

## Observations utiles pour la phase 3

- **K5** : « Score reason » des catalogues = fraîcheur (« pushed today ») + correspondance exacte ; les sources primaires plafonnent par la grille (autorité réservée aux plateformes). Le modèle le dit lui-même dans sa réponse finale (« le barème favorise GitHub et YouTube »). Il a abaissé l'autorité des vidéos « aimant à prospects » **hors grille**, par jugement.
- **K7** : les sources primaires ont été trouvées (docs, blog, dépôts officiels) mais par la recherche web générale ; aucune contradiction signalée en tant que telle, seule la divergence des dates de septembre est notée dans « Trends ».
- **K6** : 6 pages ouvertes sur 20 sources (pas 25). Pluto et Pebblous résumés depuis les extraits de recherche, dit explicitement ; date de Pluto « per StationX, not verified ». Les deux dépôts Anthropic : métadonnées non récupérées, dit explicitement.
- **K3** : l'en-tête porte une ligne d'état par source ajoutée hors gabarit (arXiv 0, GitHub 20, YouTube 15) ; le pied de page cite « arXiv » alors qu'arXiv n'a rien fourni.
- **K4** : Tier 3 jugé inutile sur 35 résultats bruts, avant tout filtrage.
- **K10 / E6** : l'homonyme `0xDarkMatter/claude-mods` est **retenu** (72, « adjacent », étiqueté `naming-collision`) au lieu d'être écarté. Dédoublonnage explicite des docs localisées et des dépôts d'un même auteur.
- **K11** : slug `claude-mods` en minuscules, rapport en anglais « comme le gabarit », réponse de chat en français ; emplacement = CWD.
- **K12** : les trois outils MCP et `WebSearch` ont été trouvés sans aide malgré le nom `web_search` dans la skill ; chemins `references/` résolus. Le rapport s'est terminé sur une question à l'humain (correction du classement de [19]) : en `-p`, c'est la fin du run.
- **S3** : `Claude Mods` → 0 article arXiv (sémantique `AND`), contre 5 hors sujet avant correction.

## Artefacts du run à corriger pour les rejeux

1. `--allowedTools` doit inclure `Edit` et `Bash` (ou `--permission-mode acceptEdits`) : 11 refus, défaut de classement [19] laissé dans le rapport.
2. Pinner le modèle (`--model …`) : ce run a tourné sur Opus 5.5 alors que Fable était annoncé. Les rejeux « après » doivent utiliser le même modèle que cette référence, ou E1 doit être rejoué sur Fable.
3. Transcript complet, `stderr.log`, `mcp.json` et `run-e1.sh` : `claude/evals/results/tech-watch-e1-2026-10-09/` (dossier gitignoré, précédent batch A ; copie du sandbox `/tmp/claude-eval-tech-watch-e1`). Le tableau des appels ci-dessus vient de `claude/evals/tech-watch/extract-run.sh <transcript.jsonl>`.
