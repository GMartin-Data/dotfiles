# Evals — `/grill`

Corpus d'évaluation pour mesurer le **comportement post-invocation** de la
slash-command `/grill` : résolution d'entrée, garde-fou d'absence d'artefact,
anti-trivialité de la condition d'arrêt, état terminal du ledger (zéro OPEN), et
absence totale d'effet de bord sur le système de fichiers.

## Doctrine

`/grill` est une slash-command : son déclenchement est explicite (l'humain tape
`/grill` ou `/grill <chemin>`), il n'y a pas de logique d'auto-invocation à tester.
Les evals mesurent ce qui se passe **après** l'invocation :

- **Résolution d'entrée** : argument explicite prioritaire sur le fallback
  `prd.md`→`plan.md` (racine puis `docs/`)
- **Pré-flight** : aucun artefact trouvé → s'arrête et demande, ne grille jamais à vide
- **Anti-trivialité** : l'absence de section « Open questions » ne satisfait PAS la
  condition d'arrêt — les tensions inter-sections sont grillées dans tous les cas
- **État terminal du ledger** : une branche irrésolvable est marquée `DEFERRED` (pas
  laissée `OPEN`) et reflétée dans la liste de sortie ; le ledger finit à zéro OPEN
- **Aucun effet de bord** : produit un bloc copiable, n'écrit aucun fichier, n'édite
  pas l'artefact source, ne crée aucun ADR

La décision de conception qui sous-tend la délégation à `/adr` (ordre topologique,
relations suggérées, items autoportants, zéro fichier écrit) est tracée dans
[`adr/0003`](../../../../adr/0003-grill-delegue-adr-sans-invoquer.md). Les
`expected_behavior` ci-dessous en sont la traduction observable.

Approche **Evaluation-Driven Development** (Anthropic,
[best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)) :
les evals sont la source de vérité pour mesurer si la command respecte son contrat.
On démarre minimal et on étoffe par nécessité observée — pas de couverture
spéculative.

## Format

Chaque eval suit ce schéma :

```json
{
  "id": "<eval-id>",
  "class": "<preflight | anti_triviality | ledger_terminal_state | input_resolution | no_side_effect>",
  "command": "/grill",
  "query": "<input utilisateur : '/grill' ou '/grill <chemin>'>",
  "files": ["<fixtures nécessaires, chemins relatifs au CWD>"],
  "expected_behavior": [
    "<invariant observable 1>",
    "<invariant observable 2>"
  ]
}
```

- `class` : axe comportemental testé
- `query` : `/grill` nu (fallback) ou `/grill <chemin>` (argument explicite)
- `files` : fixtures qui doivent exister dans le CWD au lancement de la session B
  (un `prd.md`, parfois un decoy racine + une cible sous `docs/specs/`)
- `expected_behavior` : invariants **observables** dans la transcription — pas une
  sortie exacte

## Classes comportementales

| Classe | Mesure | Evals |
|---|---|---|
| `preflight` | Aucun artefact → s'arrête et demande, ne grille jamais à vide | `preflight-artifact-absent` |
| `anti_triviality` | Pas de section « Open questions » → grille quand même les tensions inter-sections ; ledger non vide | `no-open-questions-section` |
| `ledger_terminal_state` | Branche irrésolvable → `DEFERRED` (jamais `OPEN`), reflétée en sortie ; ledger finit à zéro OPEN | `deferred-branch-in-output` |
| `input_resolution` | Argument explicite prioritaire sur le fallback ; type déduit du fichier | `input-explicit-arg-over-fallback` |
| `no_side_effect` | Bloc copiable, zéro fichier écrit, source intouchée, aucun ADR créé, ordre topologique + invite visible | `output-no-file-written` |

## Fixtures

Toutes les fixtures sont **éphémères** : créées à la demande sous `/tmp/` par
`setup-eval-cwd.sh`, jetées après test. Aucun snapshot versionné.

### CWD vide

- **Création** : `mkdir -p <cwd>` (aucun artefact)
- **But** : déclencher le garde-fou d'absence (la command s'arrête et demande)
- **Eval concernée** : `preflight-artifact-absent`

### `prd.md` avec une tension inter-sections délibérée

- **Contenu** : un PRD `link-saver` **sans** section « Open questions », avec une
  **contradiction plantée** : les Contraintes interdisent tout appel réseau tiers
  en runtime, alors qu'un critère d'acceptation exige un résumé généré par un
  **service externe**. Une relecture linéaire la rate ; le grill doit la lever.
- **But** : vérifier que l'absence d'« Open questions » ne court-circuite pas la
  revue, et que `/grill` n'écrit aucun fichier
- **Evals concernées** : `no-open-questions-section`, `deferred-branch-in-output`,
  `output-no-file-written`

### `prd.md` racine (decoy) + `docs/specs/custom-prd.md` (cible explicite)

- **Contenu** : un PRD decoy à la racine (cible du fallback) **plus** un PRD réel
  sous `docs/specs/`, passé en argument explicite
- **But** : vérifier que l'argument explicite l'emporte sur le fallback — le decoy
  racine doit être ignoré
- **Eval concernée** : `input-explicit-arg-over-fallback`

## Exécution — protocole A → B → A

L'isolation contextuelle garantit un CWD propre (pas de fichiers parasites de la
session A) et une transcription figée (l'auteur juge un artefact, pas un déroulé
live).

| Rôle | Qui | CWD | Mission |
|---|---|---|---|
| **A (auteur)** | Session dans `~/dotfiles` | Projet | Monte les CWDs (`setup-eval-cwd.sh`), juge les transcriptions de B contre les `expected_behavior`, produit le rapport matrice |
| **B (exécutant)** | Session fraîche dans `/tmp/grill-eval-<id>-*/` | Fixture éphémère | Reçoit la query, exécute la command, produit la transcription |
| **Humain** | Toi | — | Canal de transmission (copie-colle les transcriptions vers A) |

### Séquence

```
[Session A — setup]
  1. A lance setup-eval-cwd.sh pour chaque eval-id
  2. A fournit à l'humain la liste des CWDs temporaires

[Sessions B — une par eval, contexte vierge chacune]
  1. cd <cwd temporaire> && claude
  2. Coller la query ('/grill' ou '/grill docs/specs/custom-prd.md')
  3. Suivre l'échange jusqu'à observer l'invariant, puis couper :
     - preflight  : couper dès l'arrêt + demande de chemin
     - anti_triviality / ledger : laisser dérouler jusqu'à la liste de sortie
       finale (c'est là que se lisent le ledger terminal et la branche DEFERRED)
     - no_side_effect : laisser produire la liste, puis vérifier hors session que
       prd.md est inchangé et qu'aucun fichier n'a été créé
  4. Copier-coller l'intégralité de la transcription

[Retour session A — jugement]
  1. Coller les transcriptions une par une
  2. A coche chaque expected_behavior (✅ / ⚠️ / ❌)
  3. A produit le rapport matrice consolidé
```

### Frictions connues

- **Le grill est interactif et long.** Contrairement à `/adr` (où l'invariant clé
  tombe tôt), les classes `anti_triviality` et `ledger_terminal_state` ne se jugent
  qu'à la **liste de sortie finale**. Il faut conduire l'échange jusqu'au bout
  (répondre aux questions du grill) pour observer le ledger terminal. Couper trop
  tôt masque l'état `DEFERRED` et le « zéro OPEN ».

- **`deferred-branch-in-output` demande une amorce.** Pour qu'une branche finisse
  `DEFERRED`, il faut qu'une question bute sur un input externe manquant. En session
  B, quand le grill pose la question correspondante (typiquement « le service de
  résumé externe est-il acceptable malgré la contrainte hors-ligne ? »), l'humain
  répond que **la décision dépend d'un arbitrage produit non encore rendu** — ce qui
  force le `DEFERRED`. Documenter cette amorce dans le rapport : c'est une condition
  du test, pas un écart.

- **`no_side_effect` se vérifie hors transcription.** L'invariant « aucun fichier
  écrit » ne se lit pas seulement dans le déroulé : après la session B, vérifier
  côté A que `prd.md` est byte-identique à la fixture et qu'aucun `*.md` nouveau
  n'est apparu dans le CWD. Une command qui « décrit » ne rien écrire mais écrit
  quand même est un échec.

- **`/catchup` ne restaure pas ce README.** À la reprise de A après `/clear`,
  `/catchup` relit `progress.md` et le git log — pas ce fichier. Si le protocole a
  besoin d'un détail opérationnel, le porter aussi dans `progress.md`. Ce README
  porte la doctrine durable.

- **Échec silencieux.** Si B reçoit `/grill` mais rate un invariant (ex. comble la
  trivialité en s'arrêtant faute d'« Open questions », laisse une branche OPEN,
  grille le decoy racine au lieu de l'argument explicite, ou écrit un fichier),
  elle peut continuer en produisant une liste plausible. **C'est précisément un cas
  d'échec**, à signaler dans le rapport.

### Lancer une eval

```bash
# Depuis ~/dotfiles, en session A :
cd ~/dotfiles/claude/commands/grill/evals
./setup-eval-cwd.sh input-explicit-arg-over-fallback
# → imprime un chemin /tmp/grill-eval-input-explicit-arg-over-fallback-<timestamp>/

# Dans un terminal séparé, session B vierge :
cd /tmp/grill-eval-input-explicit-arg-over-fallback-<timestamp>
claude
# Puis taper : /grill docs/specs/custom-prd.md
```

## Doctrine d'étoffage

Ajouter une eval **quand** :
- Une régression observée en usage réel rate un invariant non couvert → nouvelle
  classe ou nouveau fixture
- Le grill d'un **PLAN** (pas seulement d'un PRD) gagne un traitement distinct à
  tester → eval dédiée (aujourd'hui le corpus ne couvre que des fixtures PRD ; la
  condition d'arrêt PLAN — chaque décision archi confrontée à une alternative — n'a
  pas encore de fixture)
- Une nouvelle relation suggérée dans la liste de sortie (`Extends`, `Constrains`)
  mérite d'être vérifiée sur un fixture multi-décisions → eval dédiée

Éviter :
- Les evals hypothétiques « au cas où » sans usage réel sous-jacent
- Les `expected_behavior` trop prescriptifs (décrire le **quoi observable**, pas le
  **comment**)
- La duplication entre evals : chaque eval cible un invariant différent

## Axes futurs (non bloquants)

- **Fixture PLAN** : un `plan.md` avec une décision d'architecture non confrontée à
  une alternative, pour tester la condition d'arrêt spécifique au PLAN (chaque
  décision archi confrontée à ≥ 1 alternative)
- **Ordre topologique sur N≥3 ADR** : fixture où trois décisions s'enchaînent
  (A → B → C) pour vérifier que la liste de sortie les ordonne parents avant enfants
  et suggère les bonnes relations
- **Fallback `plan.md` quand `prd.md` absent** : eval vérifiant que le fallback
  descend bien à `plan.md` (et `docs/`) quand aucun `prd.md` n'existe

## État du corpus

| Command | Statut | Nombre d'evals | Classes | Dernière mise à jour |
|---|---|---|---|---|
| `/grill` | ✅ bootstrap | 5 | `preflight`, `anti_triviality`, `ledger_terminal_state`, `input_resolution`, `no_side_effect` | 2026-06-23 |

⚠️ **Corpus écrit, non encore exécuté en A→B→A.** Les 5 evals sont spécifiées mais
aucun run n'a validé le comportement réel de `/grill` contre elles. Le corpus ne
couvre que des fixtures PRD ; le grill d'un PLAN reste à doter d'un fixture.
