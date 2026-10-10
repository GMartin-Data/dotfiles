# K4 — filtre rapide et déclenchement du Tier 3 — E10 du 2026-10-10

Item K4 (`handover.md` §7) : le Tier 3 se déclenchait sous 12 résultats
« pertinents », mais la pertinence n'était jugée qu'à la notation ; le bruit
comptait. Critère : dix résultats hors sujet ne dispensent pas du Tier 3.
Scénario E10 (§8) : bruit massif au Tier 1 → le Tier 3 se déclenche. Jamais
joué en phase 0 (pas de référence).

## Règle (validée par Greg, trois choix explicites)

`SKILL.md` : nouvelle **étape 4**, filtre rapide sur titre et description
(on-topic / adjacent / off-topic, même lecture que le critère 1 de la grille) ;
écartés sans étiquette : vidéos < 3 min (`duration_seconds` < 180, coupe
binaire, pas d'exception pour les chaînes officielles) et résultats sans titre
exploitable ; les off-topic sortent du pipeline. **Étape 5** dédoublonnage
(remonté avant le comptage après le run E10b, voir ci-dessous). **Étape 6** :
Tier 3 si **on-topic uniques < 12**, les adjacents ne comptent pas ; entrées
par priorité décroissante, chaque lot filtré et dédoublonné, arrêt à 12 ou à
épuisement. Trois comptes conservés pour l'en-tête (format : K3).
`sources.yaml` : `min_results_before_tier3` commenté, `min_video_duration_seconds: 180`.

## Montage

`run-eval.sh e10<x>-k4 "/tech-watch <sujet>"`, montage fork, Opus, serveur `00009`.
Trois sujets ont été nécessaires : les deux premiers, choisis par Claude et
validés, avaient trop de couverture web pour passer sous 12.

## Résultats **[Observé]**

| Run | Sujet | Tier 1 brut | Comptes en en-tête | Tier 3 | Durée / coût |
|---|---|---|---|---|---|
| E10a | MCP elicitation | arXiv 0 · GitHub 20 · YouTube 15 | 63 bruts · **38 on-topic** · 16 adjacents · 4 off-topic · 5 vidéos < 3 min | **non** (« on-topic >= 12 », explicite) | 158 s, 0,56 $ |
| E10b | Apache Iceberg variant type | arXiv 0 · GitHub 1 · YouTube 12 | 42 bruts · **21 on-topic (14 uniques)** · 10 adjacents · 2 off-topic · 9 écartés (4 vidéos < 3 min, 5 sans titre) | **non** (comptage **avant** dédoublonnage : 21 ≥ 12) | 196 s, 0,68 $ |
| E10c | Apache Iceberg row lineage | arXiv 0 · GitHub 1 · YouTube 8 | 94 bruts · **11 on-topic (7 uniques)** · 47 adjacents · 36 off-topic ou écartés | **oui** : les 6 entrées, par priorité, « exhausted without reaching 12 on-topic » | 153 s, 0,63 $ |

E10c, appels dans l'ordre : 3 outils MCP (`days_back=60`, « niche topic »,
choisi par le modèle) → 3 `WebSearch` Tier 2 → `WebSearch` `allowed_domains`
`huggingface.co` → 7 `WebFetch` → 5 `WebSearch` Tier 3 restants (anthropic.com,
deepmind.google, deeplearning.ai, importai + raschka, news.ycombinator.com) →
4 `WebFetch` → `Write`. Rapport : 8 sources (5 ≥ 60, 3 gardées sous le seuil
selon la clause « drop unless Tier 3 returns nothing better » de la grille),
note de couverture explicite.

**Verdict K4** : **réussi** — 83 résultats adjacents ou hors sujet n'ont pas
dispensé du Tier 3 ; sur les deux autres runs, le non-déclenchement est motivé
par le compte on-topic, pas par le brut.

## Ajustement en cours de route

E10b a révélé que le comptage précédait le dédoublonnage (21 on-topic bruts,
14 uniques) : les doublons gonflaient le compte. L'étape « Deduplicate » est
passée avant le comptage (étapes 5 et 6), et le seuil se lit sur les on-topic
**uniques**. E10c a tourné avec la règle finale.

## Observations pour la suite

- **Tier 3 orienté IA** : pour un sujet data engineering, les six entrées n'ont
  rien rendu d'on-topic, le modèle le dit lui-même. La liste de `sources.yaml`
  (HF, Anthropic, DeepMind, The Batch, newsletters IA, HN) ne couvre pas le
  périmètre data de Greg — **choix de contenu à lui soumettre** (ajouter des
  domaines data : blogs Apache, Dremio, dbt, Confluent… ou laisser le modèle
  proposer des domaines par sujet).
- **K5/K6** : les recherches web ne sont pas filtrées par date ; sur un sujet
  mince, la plupart des sources on-topic sont hors fenêtre et prennent 0 en
  fraîcheur. Le modèle le signale en tête et garde 3 sources sous le seuil.
- **K6** : 12 `WebFetch` sur E10a, 19 sur E10b, 11 sur E10c (dont 2 doublons
  d'URL) — budget d'enrichissement non borné.
- **K3** : l'en-tête porte désormais les comptes et les tiers exécutés
  (spontanément, trois formats différents sur trois runs) ; pied de page figé
  inchangé.
- Les guillemets sur `"row lineage"` et `"Apache Iceberg"` dans les requêtes web
  suivent la règle « expressions figées » ; recall suffisant (9–10 liens par
  recherche).

Transcripts : `claude/evals/results/tech-watch-e10{,b,c}-k4-2026-10-10/`
(gitignorés). Rapports copiés ici (`E10a-…`, `E10b-…`, `E10c-…`).
