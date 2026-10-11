# K10 — homonymes et dédoublonnage élargi — E6 sur E1, 2026-10-10

Item K10 (`handover.md` §7) : le dédoublonnage ne traitait que le même contenu
sur plusieurs URL ; re-uploads, reprises sans apport et dépôts homonymes
passaient. Critère = E6 (§8) : sur « claude mods », les dépôts sans rapport
sont écartés. Référence E6 (acté sur E1 du 09/10) : `0xDarkMatter/claude-mods`
**retenu** à 72. Depuis K4, écarté par jugement sur cinq runs, sans règle.

## Règle (validée par Greg, trois choix explicites)

`SKILL.md` étape 5 : deux tests binaires étiquettent `homonym` un résultat
dont seul le nom correspond — **test de date** (sujet daté, référence = date
établie par une source primaire) et **test de sens** (la description désigne
un autre objet) ; compte « homonyms » en en-tête. Étape 6 : une entrée par
contenu — variantes d'une page (localisées, `.md`, miroirs, republications),
teaser et version complète, **au plus 2 entrées par auteur, chaîne ou
organisation** (les autres repliées dans le résumé) ; une réécriture sans
apport n'est pas un doublon mais du faible signal. `scoring-criteria.md` :
définition de D étendue aux réécritures sans contenu propre.

## Montage

`run-eval.sh e1-k10` puis `e1b-k10`, `"/tech-watch Claude Mods"`, montage
fork, Opus, serveur `00009`.

## Résultats **[Observé]**

### E1a — règle initiale (184 s, 0,73 $) : critère rempli, dommage collatéral

| Mesure | Observé |
|---|---|
| Homonymes | **10**, dont `0xDarkMatter/claude-mods` (absent du rapport) |
| Test de date | référence = annonce du 2026-10-01 → **4 dépôts créés du 14 au 16 septembre écartés**, dont `karanb192/awesome-claude-code-mods` (456 ⭐, le plus étoilé du sujet, catalogue documentant ce que chaque mod lit, écrit, exécute ou envoie) |
| Signalé par le modèle | « The official overview mentions an early-access period (`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`) … The rule was applied as written; review this exclusion » |
| Dédoublonnage | dépôt compagnon de Nate Herk replié dans sa vidéo ; second dépôt `promptadvisers` replié ; plafond 2 par auteur tenu |

Défaut de la règle, pas du modèle : la date d'annonce est celle de la
disponibilité générale, pas de l'existence de la chose. Les mods ont eu une
préversion (« Function Hooks », mi-septembre, cf. StationX en E1 de référence).

**Correctif** (`SKILL.md`, étape 5) : la référence est la **plus ancienne**
date qu'une source primaire établit (préversion, accès anticipé, bêta, sinon
lancement) ; si une source primaire mentionne une période de préversion sans
la dater, le test de date est **sauté** et seul le test de sens s'applique.

### E1b — règle corrigée (220 s, 0,79 $)

| Mesure | Observé |
|---|---|
| Test de date | « skipped. The official overview mentions an early-access period … without dating it, so homonyms were judged on the meaning test alone » |
| Homonymes | **5** au test de sens ; `0xDarkMatter/claude-mods` présent dans les 20 dépôts du serveur, **absent du rapport** |
| Dépôts de la préversion | de retour dans le pipeline : `karanb192/awesome-claude-code-mods` noté 64, les trois autres 62 (hors fenêtre de 30 j, push plafonné) — sous le plafond de 20, cités dans la note de couverture |
| Plafond par auteur | aucun propriétaire GitHub à plus d'une entrée dans le top 20 ; dépôt compagnon de Nate Herk replié (« Companion repository: … ») |
| Composition | 16 vidéos et pages web, 4 dépôts ; 38 sources ≥ 60, plafond 20 |

**Verdict E6 / K10 : réussi** — les dépôts sans rapport sont écartés par
règle (test de sens), les dépôts de la préversion ne le sont plus, le
dédoublonnage élargi et le plafond par auteur sont appliqués.

## Observations pour la suite

- Le test de date reste utile pour un sujet à date d'existence nette (une
  version, un produit sans préversion publique) ; sur « Claude Mods » il est
  sauté, et c'est le bon comportement.
- Les dépôts de la préversion sortent du top 20 par la fenêtre de 30 jours
  (création hors fenêtre → push plafonné à 10) : une veille à 60 jours (E4)
  les remonterait. Comportement de la grille, pas du filtre.
- **K3** : « Date test: skipped … » et « Topic normalized to … (owner:
  Anthropic) » ajoutés à l'en-tête, format libre — à fixer.
- Deux pages lues tronquées (changelog, StationX), dites en en-tête (K6).

Transcripts : `claude/evals/results/tech-watch-e1{,b}-k10-2026-10-10/`
(gitignorés). Rapports copiés ici (`E1a-date-test-launch-…`,
`E1b-date-test-skipped-…`).
