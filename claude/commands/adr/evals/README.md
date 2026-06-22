# Evals — `/adr`

Corpus d'évaluation pour mesurer le **comportement post-invocation** de la
slash-command `/adr` : numérotation déterministe, mode interview vs capture,
supersession bidirectionnelle, immuabilité du corps, absence de trace de source.

## Doctrine

`/adr` est une slash-command : son déclenchement est explicite (l'utilisateur tape
`/adr` ou `/adr --from-context`), il n'y a pas de logique d'auto-invocation à
tester. Les evals mesurent ce qui se passe **après** l'invocation :

- **Numérotation** dérivée du répertoire `adr/` (max + 1, jamais combler un trou,
  jamais demander le numéro à l'humain)
- **Mode interview** par défaut (faire émerger la décision par questions)
- **Mode capture** avec `--from-context` (relire le fil, ne pas ré-interviewer)
- **Supersession bidirectionnelle** (deux fichiers touchés : nouveau + ancien)
- **Immuabilité du corps** d'un ADR `Accepted` (refus d'édition directe, voie
  correcte = nouvel ADR)
- **Aucune trace de source** dans l'artefact (provenance pilote l'interaction,
  pas le fichier)

La convention de référence est
[`docs/methodology/conventions/adr.md`](../../../../docs/methodology/conventions/adr.md) :
`/adr` en dérive et n'invente aucune règle. Les `expected_behavior` ci-dessous
sont la traduction observable de cette convention.

Approche **Evaluation-Driven Development** (Anthropic,
[best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)) :
les evals sont la source de vérité pour mesurer si la command respecte son
contrat. On démarre minimal et on étoffe par nécessité observée — pas de
couverture spéculative.

## Format

Chaque eval suit ce schéma :

```json
{
  "id": "<eval-id>",
  "class": "<numbering | mode_interview | mode_capture | supersession | immutability | no_source_trace>",
  "command": "/adr",
  "query": "<input utilisateur : '/adr' ou '/adr --from-context'>",
  "files": ["<fixtures nécessaires, chemins relatifs au CWD>"],
  "expected_behavior": [
    "<invariant observable 1>",
    "<invariant observable 2>"
  ]
}
```

- `class` : axe comportemental testé
- `query` : `/adr` nu (mode interview) ou `/adr --from-context` (mode capture)
- `files` : fixtures qui doivent exister dans le CWD au lancement de la session B
  (le plus souvent un répertoire `adr/`, parfois pré-rempli d'ADR existants)
- `expected_behavior` : invariants **observables** dans la transcription — pas
  une sortie exacte

## Classes comportementales

| Classe | Mesure | Evals |
|---|---|---|
| `numbering` | Numéro dérivé du répertoire (max + 1, trou jamais comblé, padding 4) | `numbering-empty-adr-dir`, `numbering-with-gap` |
| `mode_interview` | Sans `--from-context` : fait émerger la décision par questions, n'extrait rien du fil | `mode-interview-default` |
| `mode_capture` | Avec `--from-context` : relit le fil, ne ré-interviewe pas | `mode-capture-from-context` |
| `supersession` | Opération bidirectionnelle : nouveau ADR + patch `Status` de l'ancien, corps ancien intouché | `supersession-bidirectional` |
| `immutability` | Refus d'éditer le corps d'un ADR `Accepted`, propose la voie correcte | `immutability-body-refused` |
| `no_source_trace` | En-tête limité aux champs canoniques, aucun `Decided-by`/`Source`/`Author` | `no-source-trace-in-output` |

Pas de classe `strict_mode_gate` : contrairement à `/prd` et `/planning`, `/adr`
n'écrase jamais un fichier de sortie — un ADR existant se **supersède**, il ne se
réécrit pas. C'est la classe `supersession` qui porte cette garantie.

## Fixtures

Toutes les fixtures sont **éphémères** : créées à la demande sous `/tmp/` par
`setup-eval-cwd.sh`, jetées après test. Aucun snapshot versionné.

### Répertoire `adr/` vide

- **Création** : `mkdir -p <cwd>/adr`
- **Evals concernées** : `numbering-empty-adr-dir`, `mode-interview-default`,
  `mode-capture-from-context`, `no-source-trace-in-output`

### `adr/` avec un trou de numérotation

- **Contenu** : `adr/0001-choix-stack.md` + `adr/0003-pattern-async.md` (le
  `0002` manque **volontairement**)
- **But** : vérifier que `/adr` attribue `0004` (max + 1), pas `0002` (le trou
  reste ouvert)
- **Eval concernée** : `numbering-with-gap`

### `adr/` avec un ADR-0007 `Accepted`

- **Contenu** : `adr/0007-pubsub-pour-async.md`, statut `Accepted`, corps complet
  (contexte / options / décision / conséquences)
- **But** : servir de cible à une supersession (le corps doit rester intouché,
  seul `Status` change) ou à une tentative d'édition de corps (qui doit être
  refusée)
- **Evals concernées** : `supersession-bidirectional`, `immutability-body-refused`

## Exécution — protocole A → B → A

L'isolation contextuelle garantit un CWD propre (pas de fichiers parasites de la
session A) et une transcription figée (l'auteur juge un artefact, pas un déroulé
live).

| Rôle | Qui | CWD | Mission |
|---|---|---|---|
| **A (auteur)** | Session dans `~/dotfiles` | Projet | Monte les CWDs (`setup-eval-cwd.sh`), juge les transcriptions de B contre les `expected_behavior`, produit le rapport matrice |
| **B (exécutant)** | Session fraîche dans `/tmp/adr-eval-<id>-*/` | Fixture éphémère | Reçoit la query, exécute la command, produit la transcription |
| **Humain** | Toi | — | Canal de transmission (copie-colle les transcriptions vers A) |

### Séquence

```
[Session A — setup]
  1. A lance setup-eval-cwd.sh pour chaque eval-id
  2. A fournit à l'humain la liste des CWDs temporaires

[Sessions B — une par eval, contexte vierge chacune]
  1. cd <cwd temporaire> && claude
  2. Coller la query ('/adr' ou '/adr --from-context')
  3. Pour les modes interview/capture et supersession/immutabilité : suivre
     l'échange jusqu'à observer l'invariant (première question, ou soumission
     pour validation, ou refus motivé) puis couper
  4. Copier-coller l'intégralité de la transcription

[Retour session A — jugement]
  1. Coller les transcriptions une par une
  2. A coche chaque expected_behavior (✅ / ⚠️ / ❌)
  3. A produit le rapport matrice consolidé
```

### Frictions connues

- **Modes interview / capture demandent une amorce.** `mode-capture-from-context`
  suppose une délibération déjà présente dans le fil de B. En session B vierge,
  l'humain doit d'abord coller une courte délibération (contexte + options +
  décision) AVANT de taper `/adr --from-context`, sinon il n'y a rien à capturer.
  Documenter cette amorce dans le rapport — c'est une condition du test, pas un
  écart.

- **Supersession = ne pas valider trop tôt.** L'invariant clé de
  `supersession-bidirectional` est que **deux** fichiers sont touchés. Couper la
  session B avant l'écriture effective masquerait le patch `Status` de l'ancien.
  Laisser dérouler jusqu'à la confirmation post-écriture (« les deux fichiers ont
  été touchés »).

- **Immuabilité = il faut une demande explicite.** `immutability-body-refused`
  exige que l'humain DEMANDE de modifier le corps de l'ADR-0007 `Accepted`. La
  query `/adr` seule ne déclenche rien — l'amorce est « modifie le contexte de
  l'ADR-0007 ». Le refus motivé est l'invariant.

- **`/catchup` ne restaure pas ce README.** À la reprise de A après `/clear`,
  `/catchup` relit `progress.md` et le git log — pas ce fichier. Si le protocole
  a besoin d'un détail opérationnel, le porter aussi dans `progress.md`. Ce README
  porte la doctrine durable.

- **Échec silencieux.** Si B reçoit `/adr` mais rate un invariant (ex. comble le
  trou de numérotation, écrit sans soumettre pour validation, laisse une trace de
  source), elle peut continuer en produisant un ADR. **C'est précisément un cas
  d'échec**, à signaler dans le rapport.

### Lancer une eval

```bash
# Depuis ~/dotfiles, en session A :
cd ~/dotfiles/claude/commands/adr/evals
./setup-eval-cwd.sh numbering-with-gap
# → imprime un chemin /tmp/adr-eval-numbering-with-gap-<timestamp>/

# Dans un terminal séparé, session B vierge :
cd /tmp/adr-eval-numbering-with-gap-<timestamp>
claude
# Puis taper : /adr
```

## Doctrine d'étoffage

Ajouter une eval **quand** :
- Une régression observée en usage réel rate un invariant non couvert → nouvelle
  classe ou nouveau fixture
- Une nouvelle relation inter-ADR (`Refines`, `Extends`, `Constrains`) gagne un
  traitement spécifique dans `adr.md` → eval dédiée (aujourd'hui seul
  `Supersedes` est couvert ; `Extends` est utilisé par ADR-0002 mais pas encore
  testé)
- Une transition de statut au-delà de `Accepted`/`Superseded` est ajoutée
  (`Deprecated`) → eval dédiée

Éviter :
- Les evals hypothétiques « au cas où » sans usage réel sous-jacent
- Les `expected_behavior` trop prescriptifs (décrire le **quoi observable**, pas
  le **comment**)
- La duplication entre evals : chaque eval cible un invariant différent

## Axes futurs (non bloquants)

- **Relation `Extends`** : eval vérifiant qu'un ADR qui en étend un autre
  (cas ADR-0002 → ADR-0001) écrit `Extends:` sans toucher au statut de l'ancien
  (l'ancien reste `Accepted`, pas de patch — différence nette avec `Supersedes`)
- **Relation `Refines`** : eval symétrique pour le raffinement sans contradiction
- **Transition `Deprecated`** : eval sur un ADR rendu obsolète sans remplaçant
  (contexte disparu) — seul `Status` change, pas de nouvel ADR lié
- **Capture multi-tours** : eval `mode_capture` où la délibération du fil s'étale
  sur plusieurs échanges, pour vérifier que `/adr` synthétise sans en omettre

## État du corpus

| Command | Statut | Nombre d'evals | Classes | Dernière mise à jour |
|---|---|---|---|---|
| `/adr` | ✅ bootstrap | 7 | `numbering` (×2), `mode_interview`, `mode_capture`, `supersession`, `immutability`, `no_source_trace` | 2026-06-22 |

⚠️ **Corpus écrit, non encore exécuté en A→B→A.** Les 7 evals sont spécifiées
mais aucun run n'a validé le comportement réel de `/adr` contre elles.
