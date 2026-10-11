# K6 — enrichissement budgété, « non vérifié » — E8 du 2026-10-10

Item K6 (`handover.md` §7) : la notation exige date, longueur et engagement ;
la recherche web ne rend que titres et URL ; ≈ 25 pages ouvertes par veille,
plusieurs illisibles. Critère : toute date du rapport est soit vérifiée, soit
marquée non vérifiée. Scénario E8 (§8) : pages illisibles → dates marquées
« non vérifiée », aucune date inventée. Jamais joué en phase 0.

## Règle (validée par Greg, trois choix explicites)

`SKILL.md`, nouvelle **étape 7** entre dédoublonnage/Tier 3 et notation :
seuls les candidats web on-topic sont enrichis, **jamais les résultats Tier 1**
(le serveur rend date, étoiles, vues, durée) ; **budget 10 `WebFetch`**, une
ouverture par URL, pas de seconde tentative, les échecs comptent ; trois
valeurs extraites (date, longueur, auteur/organisation) ; provenance admise
pour une date = sortie d'outil Tier 1, page ouverte, chemin d'URL ; tout le
reste, estimation ou extrait de recherche compris, → `unverified`. Comptes
conservés pour l'en-tête. `report-template.md` : `📅 {publication_date |
unverified}`, autorité `unverified` admise, note sous le gabarit. Grille non
touchée (K5).

## Montage

`run-eval.sh e8-k6 "/tech-watch Claude Mods"` avec
`EXTRA_ARGS="--disallowedTools WebFetch"` (E8a : aucune page lisible, par
retrait de l'outil, choix Greg) ; `run-eval.sh e8b-k6` sans option (E8b :
conditions réelles, budget observé). Montage fork, Opus, serveur `00009`.
Contrôle des dates : `claude/evals/tech-watch/check-dates.py <rapport>
<transcript>` (classe chaque date de source web : `unverified`, chemin d'URL,
page ouverte, extrait de recherche, sans provenance).

## Résultats **[Observé]**

| Mesure | E8a — sans `WebFetch` | E8b — normal |
|---|---|---|
| Tier 1 / Tier 2 | arXiv 0 · GitHub 20 · YouTube 15 · web 28 | idem |
| Filtre (K4) | 55 on-topic (53 uniques), 1 adjacent, 1 off-topic, 6 sans titre | 54 on-topic (51 uniques), 7 écartés dont 1 vidéo < 3 min et 6 sans titre (**dont deux docs `code.claude.com` localisées**) |
| Enrichissement | « 0 pages opened out of a budget of 10, 0 failures. `WebFetch` was not available … date, length and authority stay `unverified` for all 20 unique web candidates » | **10 pages sur 10, 10 URL distinctes, 0 échec, 0 doublon** ; « 4 pages (dev.to) show a day and month but no year, so their date stays `unverified` » |
| Sources web dans le rapport | 0 (« caps them at 59/100 ») | 0 (« the best web articles peak at 85 and fall below the cut ») |
| Rapport | 20 sources : 14 YouTube, 6 GitHub | 20 sources : 13 YouTube, 7 GitHub |
| `check-dates.py` | 0 source web, 0 date sans provenance, exit 0 | 0 source web, 0 date sans provenance, exit 0 |
| Durée / coût | 124 s, 0,48 $ | 152 s, 0,60 $ |

**Verdict K6 : réussi.** Aucune date inventée dans les deux runs ; l'absence
de l'outil est constatée sans relance ni contournement et dite en en-tête ; le
budget est tenu à l'unité, sans URL ouverte deux fois (E10b en ouvrait 19 dont
2 doublons) ; une date incomplète reste `unverified` plutôt qu'estimée.

**Limite du montage** : dans les deux runs, aucune source web n'atteint le
top 20, donc la convention `📅 unverified` **par source** n'est pas observée
dans un rapport — elle n'est attestée que par l'en-tête. Le marquage sera
visible dès que la grille laissera passer des sources web (K5).

## Observations pour la suite

- **K5** : une source web non vérifiée plafonne à 59 (relevance 40 + fraîcheur
  0 + autorité 6 + profondeur 10 + engagement 3), vérifiée à 85 : la grille
  exclut structurellement le web du top 20 face à 35 résultats Tier 1 à 84–97.
  Les quatre runs E1 depuis K12 ont 0 à 3 sources web.
- **K7** : les pages officielles Anthropic (billet, docs EN) ne figurent pas
  dans les 28 résultats web de ce run non plus (E1-k9 idem) ; les docs
  localisées remontées sont écartées comme « sans titre ». Une recherche ciblée
  sur les sources primaires est nécessaire, pas optionnelle.
- **K3** : quatre lignes d'en-tête spontanées (counts, enrichment, selection,
  freshness basis), format différent à chaque run — le gabarit doit les fixer.
- **K10** : l'homonyme `0xDarkMatter/claude-mods` est l'unique off-topic des
  deux runs, écarté au filtre (troisième et quatrième runs de suite).

Transcripts : `claude/evals/results/tech-watch-e8{,b}-k6-2026-10-10/`
(gitignorés). Rapports copiés ici (`E8a-no-webfetch-…`, `E8b-normal-…`).
