# K7 — sources primaires d'abord, contradictions — rejeu E1 du 2026-10-10

Item K7 (`handover.md` §7) : aucune notion de source primaire ni d'exactitude ;
les pages officielles n'étaient trouvées que par la recherche web générale, et
un article contredisant la documentation (drapeau d'accès anticipé encore
requis) aurait obtenu 73, écarté hors grille. Critère : le rapport cite les
sources primaires quand elles existent et signale les contradictions.
Scénario E9 (§8) : contradiction signalée ou source écartée — non forçable par
montage, joué de façon opportuniste sur E1.

Diagnostic préalable **[Observé]** : depuis K9, les requêtes `"Claude Code"
mods` du Tier 2 ne remontent que des docs localisées (`/docs/de/`, `/docs/it/`)
sur quatre runs de suite (E1-k9, E8a, E8b, et E1-k7 hors recherche ciblée),
alors que `"Claude Mods" 2026` ramenait le billet et les docs `en` en
référence et en E1-k12.

## Règle (validée par Greg, trois choix explicites, plus AWS et Azure ajoutés à sa demande)

`SKILL.md`, nouvelle **étape 3** avant le Tier 2 : identifier le propriétaire
du sujet ; une `WebSearch` avec `allowed_domains` restreint à ses domaines
(`sources.yaml`, section `primary_sources.known_owners` : Anthropic, dbt Labs,
Apache, MCP, Snowflake, Databricks, AWS, Azure/Microsoft, Google Cloud ;
sinon recherche `{query} official documentation OR announcement` pour trouver
le domaine) ; une page localisée désigne la page `en` ; sources primaires
ouvertes en premier (jusqu'à 3 des 10 pages du budget K6) ; bloc **« Primary
sources »** dans le rapport, hors classement, sans seuil ni plafond, « No
primary source found » explicite sinon. **Contradiction** (étape 9) : source
secondaire écartée si l'affirmation contredite est dans son titre ou son
propos principal, sinon gardée et signalée `⚠️ Contradicts <primary>: …` ;
rien n'est jugé sans source primaire ouverte. Étapes renumérotées 1–10.
`report-template.md` : bloc « Primary sources » entre le résumé et le classement.

## Montage

`run-eval.sh e1-k7 "/tech-watch Claude Mods"`, montage fork, Opus, serveur `00009`.

## Résultats **[Observé]**

| Mesure | E1-k6 (E8b, avant K7) | E1-k7 |
|---|---|---|
| Recherche ciblée | — | `"Claude Code" mods`, `allowed_domains` claude.com, code.claude.com, docs.claude.com, anthropic.com, **exécutée avant le Tier 2** |
| Pages officielles remontées | docs `de`, `it` seulement | billet de lancement, docs `en` overview / create / api / admin / interface, changelog |
| Pages ouvertes | 10/10, aucune officielle | 10/10, **les 3 premières = sources primaires** (overview, billet, changelog), puis 7 articles |
| Bloc « Primary sources » | absent | 3 entrées avec URL, date (`unverified` pour la doc sans date, 2026-10-01 pour le billet, dernière entrée lue pour le changelog) et ce que chacune établit (version minimale 2.1.287, non sandboxé, variable d'accès anticipé ignorée…), plus 4 pages officielles « returned, not opened » |
| Contradiction | — | « Fact drift in secondary coverage »: un article dev.to date le lancement au 3 octobre contre le 1er dans l'annonce — **signalée** (dans « Trends », l'article étant hors top 20 par le plafond, donc sans ligne `⚠️` dans un résumé) |
| Top 20 | 13 YouTube, 7 GitHub | 13 YouTube, 7 GitHub (inchangé : K5) |
| Durée / coût | 152 s, 0,60 $ | 206 s, 0,77 $ (+1 recherche, +3 pages officielles) |

**Verdict K7 : réussi** — les sources primaires sont citées quand elles
existent (critère de la passation) ; une contradiction réelle est signalée
(E9 opportuniste : réussi sur ce run, à rejouer quand un cas connu existera).

## Observations pour la suite

- **K5** : les sources primaires ne concourent pas au classement, par choix ;
  le top 20 reste 100 % Tier 1, les trois meilleurs articles ouverts
  plafonnent à 85 contre 89 pour les dépôts. La grille est le dernier verrou.
- **E9** : la contradiction porte sur une source hors top 20 ; la règle « dans
  le titre → écartée / sinon signalée dans le résumé » n'a pas été exercée sur
  une source classée. À surveiller sur les rejeux.
- **K3** : l'en-tête porte désormais « Pages opened: 10/10 of the WebFetch
  budget, 0 failures » et une note de sélection, toujours en format libre.
- **Changelog** comme source primaire : lu partiellement (« the 2.1.287 entry
  itself was not reached »), dit explicitement — comportement K6 conforme.
- `check-dates.py` ne lit pas le bloc « Primary sources » (format en ligne
  `— 🔗 … — 📅 …`) : à étendre si l'on veut contrôler ces dates aussi.

Transcript : `claude/evals/results/tech-watch-e1-k7-2026-10-10/` (gitignoré).
Rapport copié ici : `E1-tech-watch-claude-code-mods-2026-10-10.md`.
