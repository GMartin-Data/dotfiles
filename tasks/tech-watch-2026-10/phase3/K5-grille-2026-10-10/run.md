# K5 — grille de notation — rejeu E1 et E4 du 2026-10-10

Item K5 (`handover.md` §7), le plus lourd : fraîcheur « linéaire » par paliers
et nulle au-delà de 30 jours malgré `days_back=60`, indéfinie pour un dépôt ou
une doc sans date ; profondeur à deux valeurs ; autorité réservée aux
plateformes (vidéo-liste YouTube 20, doc officielle 12) ; adjacents à 73 comme
un exact ; clause « drop unless Tier 3 returns nothing better » contre le seuil
strict ; libellés confus. Critère : sur « Claude Mods », docs et annonce dans
la tranche la plus haute, aucun Short. Scénario E4 (§8) : avec `days_back=60`,
les sources de 31 à 60 jours ne sont pas éliminées d'office.

Constat accumulé avant K5 (sept runs depuis K12) : top 20 à 100 % vidéos et
dépôts ; web vérifié plafonné à 85, non vérifié à 59 ; fraîcheur des dépôts
calculée sur le dernier push (projets de 2020 à 97).

## Grille (validée par Greg, trois choix explicites) — `scoring-criteria.md` réécrit

| Critère | Règle |
|---|---|
| Pertinence 40 | exact 40, partiel 25 ; **adjacents non classés** (listés à part, 3 max, sans score) |
| Fraîcheur 20 | relative à la fenêtre W : ≤ W/4 → 20, ≤ W/2 → 15, ≤ 3W/4 → 10, ≤ W → 5 ; dépôt = date de création si dans la fenêtre, sinon dernier push **plafonné à 10** ; page web `unverified` → **5** |
| Autorité 20 | par nature : **A** primaire 20 (propriétaire du sujet) · **B** expert 14 · **C** communauté 8 (créateurs YouTube et dépôts communautaires compris) · **D** faible signal 0 ; arXiv = B par défaut |
| Profondeur 10 | par type : article 10 ; page web > 1500 mots 10 / 600–1500 → 6 / moins ou `unverified` → 3 ; vidéo ≥ 20 min 10 / 10–20 → 7 / 3–10 → 4 ; dépôt de référence 10 / autre 6 |
| Engagement 10 | inchangé (10 / 5 / 3) |
| Seuil | **60 strict**, clause de repli supprimée ; < 10 sources → note de couverture ; plafond 20 ; égalités par engagement |
| Libellés | tranches Essential / High value / Worth including sans « Tier » ; autorité affichée par lettre et nom |

Gabarit : `⭐ Authority: {A Primary | B Expert | C Community | D Low-signal}`,
section « Adjacent, not ranked » (omise si vide). `SKILL.md` étape 9 : seuil
strict, adjacents hors classement, note de couverture. `sources.yaml` :
commentaire du seuil.

## Montage

`run-eval.sh e1-k5 "/tech-watch Claude Mods"` et `run-eval.sh e4-k5
"/tech-watch AI agent evaluation, 60-day window"`, montage fork, Opus, serveur
`00009`, en parallèle.

## Résultats **[Observé]**

### E1 « Claude Mods » (183 s, 0,73 $)

| Attendu | E1-k7 (grille d'origine) | E1-k5 | Verdict |
|---|---|---|---|
| Docs et annonce dans la tranche la plus haute | bloc « Primary sources » (K7), top 20 sans source officielle classée | bloc « Primary sources » à 3 entrées **et** vidéo officielle Claude **n° 1, A Primary, 94** (3:21, 341 k vues) — seule source au-dessus de 85 | **Réussi** |
| Aucun Short | 1 vidéo < 3 min écartée à l'étape 5 | idem, 0 vidéo < 3 min classée | **Réussi** |
| Hiérarchie officiel > expert > communauté | vidéos-listes à 89–97 au-dessus de tout | vidéos-listes communautaires à **85** (40 + 20 + 8 + 7 + 10, chiffre prédit), article d'analyse it-connect **B Expert 83**, kanaries et dev.to C 81–82 | conforme |
| Sources web classées | 0 (sept runs de suite) | **3** (it-connect, kanaries, dev.to) ; 15 pages non ouvertes à 59, dites en note de couverture | conforme |
| Dépôts | fraîcheur sur le dernier push | **date de création** (`📅 2026-10-08 (created)`), 5 dépôts à 77 | conforme |
| Adjacents | — | 0 adjacent, section omise | conforme |

Composition du top 20 : 12 YouTube (dont 1 A), 5 GitHub, 3 web. Note de
couverture explicite (36 sources ≥ 60, plafond 20, égalités à 77 tranchées par
engagement).

### E4 « AI agent evaluation », fenêtre 60 jours (156 s, 0,63 $)

| Attendu | Observé | Verdict |
|---|---|---|
| Sources de 31 à 60 jours non éliminées | `days_back=60` passé aux trois outils ; sources du 1er au 3 septembre (37–39 jours) classées à **77** avec fraîcheur 10 (≤ 3W/4 = 45 j), source du 10 septembre à 82 (fraîcheur 15) | **Réussi** |
| Dépôt ancien maintenu | « Created 2025-08-04, last push 2026-10-10 » → **80** (push plafonné à 10 ; aurait eu 90 avant) | conforme |
| Vidéos < 3 min | 7 écartées à l'étape 5 | conforme |
| Sources primaires | propriétaire inconnu → recherche `official documentation OR announcement` (règle K7), « No primary source was opened, so no contradiction check could be applied » | conforme |
| Enrichissement | 10/10, **2 échecs** (redirection inter-hôte, 404) laissés `unverified`, sans relance | conforme K6 |

Composition : 15 arXiv, 5 GitHub, 2 YouTube, 1 web ; 9 adjacents listés à
part ; tous à « B Expert » (dépôts et vidéos compris : frontière B/C laissée
au jugement, voir ci-dessous).

**Verdict K5 : réussi** sur les deux critères (E1, E4).

## Observations pour la suite

- **Frontière B/C** : sur E4, le modèle a classé B les 5 dépôts et les 2
  vidéos (organisations ou labos identifiés) ; sur E1, C les créateurs et
  dépôts perso. Cohérent avec la règle, mais c'est l'endroit où le jugement
  pèse le plus : à surveiller au rejeu.
- **Plateau à 85** : cinq vidéos-listes communautaires fraîches et vues
  atteignent exactement 85, bas de la tranche Essential. Si Greg veut les
  pousser en High value, le levier est l'engagement (10 → 5 au-dessous de
  50 k vues) ou le seuil de tranche ; non touché.
- **K3** : en-tête à cinq lignes (request, queries, results, tiers, enrichment,
  coverage) produit spontanément — le gabarit doit le fixer, c'est le prochain
  item.
- **K10** : `0xDarkMatter/claude-mods` unique off-topic, écarté (cinquième run).
- **K11** : rapport E1 en anglais, résumé en français ; E4 idem.

Transcripts : `claude/evals/results/tech-watch-{e1,e4}-k5-2026-10-10/`
(gitignorés). Rapports copiés ici.
