# K1 — limitations réécrites d'après les comportements observés — 2026-10-10

Item K1 (`handover.md` §7) : la section « Known limitations » annonçait pour
GitHub « 60 req/hour » et un échec silencieux, pour arXiv une erreur `301`,
pour YouTube l'absence des vidéos de moins de 48 h. Critère (§7) : chaque
limitation documentée est reproductible. Pas de run à rejouer : le critère se
vérifie sur les fiches de la phase 3, chaque ligne étant adossée à un run.

## Texte validé par Greg

`SKILL.md`, section « Known limitations », trois groupes (serveur et outils
Tier 1 ; recherche web et pages ; livraison), précédés de la règle « toute
ligne du tableau d'état non `ok` est nommée en première ligne de la réponse ».

## Traçabilité ligne par ligne

| Ligne | Sort | Preuve **[Observé]** |
|---|---|---|
| GitHub « 60 req/hour », échec silencieux | Réécrite : 401 explicite, un retry sans auth, 10 recherches/min, avertissement en tête des résultats, pas de retry côté skill | `baseline/E3-github-401-2026-10-10/` et `phase3/K3-etat-par-source-2026-10-10/` : `⚠️ GitHub token rejected (401); results fetched without authentication (10 searches/min instead of 30)` puis 20 dépôts |
| arXiv erreur `301` | Supprimée | jamais reproduite sur ≈ 25 runs |
| YouTube « vidéos < 48 h absentes » | Supprimée, remplacée par le comportement sans clé : `isError`, repli `youtube.com` sans date ni durée, vidéos non classables, tranche Essential possiblement vide | E3 référence (3 vidéos « not verified » classées, avant K6) ; rejeu K3 (10 vidéos de repli, 0 classée, « No source reached 85 ») |
| Paywall (Nature, IEEE, ACM) | Supprimée | jamais rencontrée |
| Reddit exclu | Gardée, avec le rappel que dev.to, Medium, Substack, Hashnode passent par le Tier 2 | `sources.yaml` ; K2/K9 (DEV.to/Hashnode retirés du Tier 3, doublon) |
| Serveur absent → « Degraded mode » si les trois outils échouent | Réécrite : outils absents de la liste, sans erreur nulle part, trois lignes `absent` | sonde K12 `down` : fork lancé, `WebSearch` et `Read` seuls, ni `stderr` ni message |
| arXiv à 0 sur un sujet produit | Nouvelle : `empty`, pas un échec, pas de retry ni d'élargissement | 0 article sur tous les runs « Claude Mods » (E1, E3, K5, K7, K10, K3, K11) ; 5/5 sur « AI agent evaluation » (E2, K2/K9) |
| `WebFetch` absent ou budget épuisé | Nouvelle : `unverified`, plafond 59, exclues et non jugées pauvres, compte dans `Notes` | E8 (K6) sans `WebFetch` ; K3 et K10 (« 11 web pages were not opened … score 59 ») |
| Lecture tronquée des pages longues | Nouvelle : ≈ 100 000 caractères, dire ce qui n'a pas été atteint | K10 (« first 100,000 characters of about 1,050,000 »), K3, K7 (changelog lu jusqu'à 2.1.288, entrée 2.1.287 non vue) |
| Paraphrase de la ligne `Report:` | Nouvelle : sous déclenchement en langage naturel, la session principale reformule le résultat du fork | E7a (K11) : ligne `Report:` produite par le fork, réponse « La veille est faite : … rapport dans `tech-watch/…` » |

Laissé dehors faute d'observation : la demande de permission pour écrire hors
du CWD en session interactive (`Write` vers `/home/martin/tech-watch/`),
reportée en phase 4 (`plan.md` §5, K11).
