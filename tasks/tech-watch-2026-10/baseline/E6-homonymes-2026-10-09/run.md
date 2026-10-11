# E6 — homonymes (« claude mods ») — référence du 2026-10-09, actée sur le run E1

Scénario E6 (`handover.md` §8) : homonymes. **Attendu** : les dépôts sans rapport
sont écartés. Items couverts : K10, S2.

**Pas de rejeu** (décision Greg, 2026-10-09) : la requête de E1 (`Claude Mods`,
`days_back=30`, `max_results=20`) est celle du scénario ; les preuves sont dans
`../E1-claude-mods-2026-10-09/` et son transcript
(`claude/evals/results/tech-watch-e1-2026-10-09/transcript.jsonl`).

## Ce que le serveur a renvoyé (S2, après correction)

20 dépôts, tri par meilleure correspondance, filtre `pushed:>` à 30 jours. Un
seul homonyme au sens strict : **`0xDarkMatter/claude-mods`** (n° 5, 56 ⭐),
boîte à outils de skills, agents, commands et hooks créée en novembre 2025, qui
porte le nom « claude-mods » sans contenir de mods au sens d'octobre 2026.
L'autre homonyme cité par la passation, `starbaser/ccproxy`, **n'apparaît plus**.
Les 19 autres portent sur le sujet, y compris les kits mixtes (`JohnnyVizz/claude-kit`,
`escapeboy/claude-code-kit`, `NarenDawar/narens-claude-toolkit`) qui listent des
mods parmi d'autres artefacts. Avant S2 : 2 homonymes sur 10 (`ccproxy`,
`0xDarkMatter/claude-mods`).

## Ce que la skill en a fait (K10)

| Attendu | Observé | Verdict |
|---|---|---|
| Les dépôts sans rapport sont écartés | `0xDarkMatter/claude-mods` **retenu** en source [20] à **72/100**, bande « High value », avec un résumé qui le qualifie lui-même d'« adjacent rather than on-topic » et l'étiquette `naming-collision` | **Échec** (K10 reproduit) : la skill a reconnu l'homonyme mais la règle « seuil 60, cible 15–20 sources » l'a gardé plutôt qu'écarté |

Dédoublonnage observé dans le même run : docs localisées fusionnées, deux dépôts
du même auteur (`karanb192/*`) fusionnés en une entrée, un re-upload de la vidéo
officielle absent des 15 vidéos renvoyées (le tri `relevance` de S4 l'a évité).

## Pour la phase 3

- K10 : ajouter une vérification de sens pour les résultats dont seul le nom
  correspond, et une règle d'exclusion explicite (un « adjacent » ne compte pas
  pour atteindre la cible de 15–20).
- Rejeu complet de E6 après K10, même requête, verdict sur l'absence de [20].
