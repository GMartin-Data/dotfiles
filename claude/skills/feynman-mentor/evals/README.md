# Evals — `feynman-mentor`

Corpus d'évaluation de la skill `feynman-mentor` : persona candide (signale les
trous d'une explication sans jamais les combler), auto-invocation sur triggers
français, non-collision avec le territoire de `teach`, garde-fou structurel
d'outils, et pont d'état ADR-0008 en fin de session.

**Contrat testé** : celui d'[ADR-0012](../../../../adr/0012-feynman-mentor-niche-verification-par-explication.md)
(niche « vérification de compréhension par explication » + 4 modalités
d'intégration à la couche learning), **pas** le SKILL.md importé tel quel.

**Corpus test-first — écrit rouge, passé vert.** Écrit AVANT l'adaptation du
SKILL.md (import claude.ai du 2025-12-29). Les evals suivantes échouaient
délibérément contre la version importée — c'était le « failing test » que
l'adaptation du 2026-07-23 a fait passer :

- `session-end-learning-record` — le SKILL.md n'a pas de section record ADR-0008
- `discovery-french-trigger` — les triggers actuels sont anglais
- `no-collision-teach-territory` — le trigger ambigu « teach me by explaining »
  est encore présent
- `no-web-lookup` (volet structurel) — aucune restriction d'outils au frontmatter
- `candide-never-fills-gaps` (volet format) — le template de feedback impose des
  titres anglais en dur ; le contrat exige la structure rendue dans la langue de
  la session

## Doctrine

`feynman-mentor` est une skill **auto-invocable** (`disable-model-invocation:
false`) : contrairement aux corpus de commands (`/grill`, `/adr`), la
**discovery est testable** — deux evals la couvrent, une positive (trigger
français) et une négative (non-collision avec `teach`).

- **`core_invariant`** : le cœur fragile de la skill. Le biais serviable du
  modèle pousse à définir, reformuler, compléter — exactement ce que le candide
  doit refuser. C'est l'invariant le plus exposé, il a deux evals (dont une
  sous demande d'aide explicite).
- **`discovery`** : l'auto-invocation se déclenche sur les phrases françaises
  d'usage réel, et ne se déclenche PAS sur « apprends-moi… » (territoire
  `teach`, flux inverse).
- **`no_side_effect`** : le persona non-informé est structurel — aucun outil web
  pour aller combler les trous, aucun fichier écrit.
- **`state_bridge`** : la fin de session émet un learning-record proposé
  (mécanique ADR-0008 : bloc copiable, flux unidirectionnel, jamais écrit hors
  CWD).

Approche **Evaluation-Driven Development** (Anthropic, best practices) : on
démarre minimal et on étoffe par nécessité observée — pas de couverture
spéculative. Le format de feedback en trois volets et le calibrage d'audience ne
sont couverts qu'incidemment (via `core_invariant`) : ils gagneront une eval
dédiée si une régression réelle les touche.

## Format

```json
{
  "id": "<eval-id>",
  "class": "<core_invariant | discovery | no_side_effect | state_bridge>",
  "skill": "feynman-mentor",
  "query": "<message utilisateur en français — langue d'interaction réelle>",
  "files": [],
  "expected_behavior": ["<invariant observable>", "..."]
}
```

Différences avec le schéma des commands : champ `skill` au lieu de `command` ;
`query` est un message naturel (jamais un `/feynman-mentor` forcé — sinon les
evals `discovery` ne mesurent rien) ; `files` toujours vide (les fixtures sont
portées par la query, la skill est purement conversationnelle).

## Classes comportementales

| Classe | Mesure | Evals |
|---|---|---|
| `core_invariant` | Signale les trous sans jamais définir, reformuler, compléter ni louer — même sur demande d'aide explicite | `candide-never-fills-gaps`, `candide-refuses-meta-help` |
| `discovery` | S'auto-invoque sur trigger français ; ne s'invoque PAS sur « apprends-moi… » | `discovery-french-trigger`, `no-collision-teach-territory` |
| `no_side_effect` | Zéro outil web (candide structurel), zéro fichier écrit | `no-web-lookup` |
| `state_bridge` | Fin de session → record ADR-0008 en bloc copiable, jamais en fichier | `session-end-learning-record` |

## Exécution

Deux moteurs possibles — le choix est l'objet du run live
[ADR-0009](../../../../adr/0009-rituel-evals-maison-vs-skill-creator.md)
(ce corpus est son déclencheur désigné) :

1. **Skill Creator officiel** (reco, Option C) : convertir les
   `expected_behavior` en `assertions` officielles (`evals/evals.json`) selon le
   pattern du pilote
   [`grill/evals/pilot-skill-creator/`](../../../commands/grill/evals/pilot-skill-creator/),
   puis run Executor/Grader. Les invariants hors-transcription (« aucun fichier
   écrit ») deviennent programmables (`ls`). Sur succès → ADR-0009 passe en
   Accepted.
2. **A→B→A manuel** (repli, Option B) : protocole identique aux corpus de
   commands — session A monte les CWDs (`setup-eval-cwd.sh <id>`), sessions B
   vierges dans chaque CWD, l'humain copie-colle les transcriptions, A juge
   contre les `expected_behavior`.

**Prérequis commun** : la skill doit être *discoverable* en session B (symlink
manuel — voir l'en-tête de `setup-eval-cwd.sh`), la query collée **verbatim**
(ne pas la préfixer de `/feynman-mentor`), et pour les classes `no_side_effect`
et `state_bridge`, vérifier après session que le CWD est resté vide.

### Frictions connues

- **Le trigger-eval officiel (`run_eval.py`) est un proxy biaisé pour les
  skills conversationnelles.** Il installe la description comme pseudo-command
  et mesure l'invocation formelle en `claude -p` — or les requêtes
  conversationnelles sous-déclenchent par construction (la doc officielle le
  dit : Claude ne consulte une skill que si la tâche semble la justifier).
  Constat du 2026-07-23 : proxy 0-1/3 sur le trigger positif, mais **3/3 en
  conditions réelles** (skill installée dans `~/.claude/skills/`, sessions
  `claude -p` fraîches, jugement sur le comportement candide observable). Pour
  la classe `discovery`, le protocole de référence est donc le test en
  conditions réelles ; le proxy reste utile pour la frontière négative (0/3
  constant sur « apprends-moi… », confirmé 3/3 en réel).

- **`no-collision-teach-territory` dépend de l'environnement de B.** Si la
  session B n'a pas la skill `teach` installée, on ne peut juger que la
  non-invocation de feynman-mentor — pas le routage effectif vers teach. Le
  deuxième volet est alors « non jugeable », pas un échec.
- **Les `core_invariant` se jugent sur la retenue, pas sur la production.** Une
  session B qui produit un feedback brillant mais glisse une seule reformulation
  (« autrement dit, tu veux dire que… ») est un ÉCHEC, même si tout le reste est
  conforme. Le juge doit chercher la fuite d'aide, pas la qualité du feedback.
- **`discovery` est sensible au contexte de session.** Un CLAUDE.md projet ou
  des skills parasites dans l'environnement de B peuvent altérer le routage.
  Le CWD éphémère vide limite ce bruit, mais l'environnement `~/.claude` de B
  reste celui de la machine — le noter dans le rapport si un résultat discovery
  surprend.

## Doctrine d'étoffage

Ajouter une eval **quand** :
- Une régression observée en usage réel rate un invariant non couvert
- Le calibrage d'audience (5-year-old / high schooler / smart adult) montre une
  dérive réelle → eval dédiée `calibration`
- Le contenu du learning-record proposé (format, champs) mérite un contrat
  précis après les premières vraies sessions → étoffer `state_bridge`

Éviter : les evals hypothétiques sans usage réel sous-jacent, les
`expected_behavior` prescrivant le *comment* au lieu du *quoi observable*, la
duplication entre evals.

## État du corpus

| Skill | Statut | Nombre d'evals | Classes | Dernière mise à jour |
|---|---|---|---|---|
| `feynman-mentor` | ✅ exécuté — 6/6 vert | 6 | `core_invariant`, `discovery`, `no_side_effect`, `state_bridge` | 2026-07-23 |

**Run du 2026-07-23** (run live ADR-0009, moteur officiel Skill Creator —
Option C actée) : 4 evals comportementales à **1.00** en with_skill contre
**17,5 %** de moyenne baseline (delta +0.82, benchmark officiel) ; frontière
`teach` étanche (proxy 0/3 ×2 itérations + réel 3/3) ; trigger positif français
vert **en conditions réelles** (3/3) après diagnostic du biais du proxy (voir
Frictions connues). Description durcie en itération 2 (clause pushy, guidance
officielle anti-under-triggering). Artefacts du run : workspace scratchpad de la
session du 2026-07-23 (éphémère — le README et `evals.json` portent la trace
durable).
