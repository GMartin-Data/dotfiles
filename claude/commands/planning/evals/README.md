# Evals — `/planning`

Corpus d'évaluation pour mesurer le **comportement post-invocation** de la
slash-command `/planning` : strict-mode gate, pré-flight de lecture des sources,
plafond d'interview, vocabulaire des granularités (palier MVP vs phase).

## Doctrine

`/planning` est une slash-command : son déclenchement est explicite (l'utilisateur
tape `/planning`), il n'y a pas de logique d'auto-invocation à tester. Les evals
mesurent ce qui se passe **après** l'invocation :

- **Strict-mode gate** correct (si `PLAN.md` existe → arrêt avec message
  semi-frozen, ne régénère pas, n'écrase pas la traçabilité ADR)
- **Pré-flight** correct (lit `PRD.md` ET `CLAUDE.md` ; arrêt si `PRD.md` absent ;
  avertit mais continue si seul `CLAUDE.md` manque)
- **Interview légère plafonnée** (3 questions max, une à la fois, pré-proposer un
  découpage dérivé du PRD, jamais une page blanche, jamais de question d'idéation)
- **Vocabulaire des granularités** (propose le découpage macro en « paliers MVP »,
  pas « milestones » ; distingue palier de valeur vs phase technique — cf.
  [`adr/0002`](../../../../adr/0002-mvp-palier-dans-plan.md))

Les règles de périmètre dérivent de la
[matrice de responsabilité documentaire](../../../../docs/methodology/responsibility-matrix.md)
(ligne PLAN.md). Les `expected_behavior` en sont la traduction observable.

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
  "class": "<strict_mode_gate | preflight | interview_cap | vocabulary>",
  "command": "/planning",
  "query": "<input utilisateur, généralement '/planning' nu>",
  "files": ["<fixtures nécessaires, chemins relatifs au CWD>"],
  "expected_behavior": [
    "<invariant observable 1>",
    "<invariant observable 2>"
  ]
}
```

- `class` : axe comportemental testé
- `query` : input utilisateur, le plus souvent `/planning` nu — éventuellement
  avec un argument (`/planning custom-name.md`)
- `files` : fixtures qui doivent exister dans le CWD au lancement de la session B
- `expected_behavior` : invariants **observables** dans la transcription — pas
  une sortie exacte

## Classes comportementales

| Classe | Mesure | Evals |
|---|---|---|
| `strict_mode_gate` | Arrêt immédiat si `PLAN.md` déjà présent (semi-frozen → ADR avant révision) | `strict-mode-existing-plan` |
| `preflight` | Lecture des sources : arrêt si `PRD.md` absent, lecture nominale PRD + CLAUDE sinon | `preflight-prd-absent`, `preflight-nominal` |
| `interview_cap` | Plafond strict 3 questions, une à la fois, pré-proposition dérivée, aucune idéation | `interview-cap-three-questions` |
| `vocabulary` | Découpage macro nommé « paliers MVP » (pas « milestones »), deux granularités distinctes | `interview-mvp-tiers-vocabulary` |

La classe `vocabulary` est née d'**ADR-0002** (MVP = palier de valeur dans le
PLAN). C'est le comportement le plus récent du corpus, encore non éprouvé par un
run — protéger le fragile, doctrine d'émergence.

## Fixtures

Toutes les fixtures sont **éphémères** : créées à la demande sous `/tmp/` par
`setup-eval-cwd.sh`, jetées après test. Aucun snapshot versionné.

Le script génère deux artefacts de base, réutilisés selon l'eval :

- **`PRD.md`-fixture** (`write_prd`) : un PRD `feed-aggregator` avec assez de
  substance pour dériver un découpage (problème, 3 user stories, périmètre cible /
  hors-cible, critères de succès). **Format aligné PRD=cible** (« Périmètre cible
  / Hors-cible », pas « v1 ») — cf. ADR-0001.
- **`CLAUDE.md`-fixture** (`write_claude_md`) : stack minimale (Python/uv, FastAPI,
  SQLite) + conventions, pour que l'architecture haut niveau ait une stack à
  référencer.

### CWD avec `PLAN.md` préexistant

- **Contenu** : `PLAN.md` (placeholder) + `PRD.md`
- **But** : déclencher le strict-mode gate (le PLAN existe déjà)
- **Eval concernée** : `strict-mode-existing-plan`

### CWD vide

- **Contenu** : rien
- **But** : `PRD.md` absent → la command s'arrête (le PLAN se dérive du PRD)
- **Eval concernée** : `preflight-prd-absent`

### CWD avec `PRD.md` + `CLAUDE.md`

- **Contenu** : les deux fixtures, pas de `PLAN.md`
- **But** : cas nominal — pré-flight lit les deux sources, puis interview de
  découpage
- **Evals concernées** : `preflight-nominal`, `interview-cap-three-questions`,
  `interview-mvp-tiers-vocabulary`

## Exécution — protocole A → B → A

L'isolation contextuelle garantit un CWD propre (pas de fichiers parasites de la
session A) et une transcription figée (l'auteur juge un artefact, pas un déroulé
live).

| Rôle | Qui | CWD | Mission |
|---|---|---|---|
| **A (auteur)** | Session dans `~/dotfiles` | Projet | Monte les CWDs (`setup-eval-cwd.sh`), juge les transcriptions de B contre les `expected_behavior`, produit le rapport matrice |
| **B (exécutant)** | Session fraîche dans `/tmp/planning-eval-<id>-*/` | Fixture éphémère | Reçoit la query, exécute la command, produit la transcription |
| **Humain** | Toi | — | Canal de transmission (copie-colle les transcriptions vers A) |

### Séquence

```
[Session A — setup]
  1. A lance setup-eval-cwd.sh pour chaque eval-id
  2. A fournit à l'humain la liste des CWDs temporaires

[Sessions B — une par eval, contexte vierge chacune]
  1. cd <cwd temporaire> && claude
  2. Coller la query (généralement '/planning' nu)
  3. Laisser dérouler jusqu'à avoir vu les invariants attendus (gate, pré-flight,
     première question de découpage / vocabulaire des paliers), puis couper
  4. Copier-coller l'intégralité de la transcription

[Retour session A — jugement]
  1. Coller les transcriptions une par une
  2. A coche chaque expected_behavior (✅ / ⚠️ / ❌)
  3. A produit le rapport matrice consolidé
```

### Frictions connues

- **`/catchup` ne restaure pas ce README.** À la reprise de A après `/clear`,
  `/catchup` relit `progress.md` et le git log — pas ce fichier. Si le protocole a
  besoin d'un détail opérationnel, le porter aussi dans `progress.md`. Ce README
  porte la doctrine durable ; `progress.md` porte la feuille de route.

- **Choix du modèle.** `/planning` fixe `model: opus` dans son frontmatter
  (dérivation stratégique du plan). Les sessions B doivent tourner sur Opus pour
  refléter le comportement réel — un test sur Sonnet ou Haiku mesure autre chose.

- **`vocabulary` se juge sur la proposition, pas le fichier final.** L'invariant
  de `interview-mvp-tiers-vocabulary` porte sur le vocabulaire employé pendant
  l'interview (Q3 « paliers MVP ») et dans la synthèse — inutile de dérouler
  jusqu'à l'écriture du `PLAN.md`. Couper dès que le vocabulaire est observé (ou
  raté : si B dit « milestones », c'est un échec).

- **Plafond d'interview = compter les questions.** `interview-cap-three-questions`
  exige de compter les questions posées par B. Si le découpage est évident depuis
  le PRD-fixture, B peut légitimement poser moins de 3 questions, voire zéro
  (proposition directe). Moins de 3 n'est PAS un échec ; plus de 3 l'est.

- **Échec silencieux.** Si B reçoit `/planning` mais rate un invariant (ex. saute
  le strict-mode gate, ouvre par une page blanche, rouvre l'idéation, dit
  « milestone »), elle peut continuer en générant du contenu. **C'est précisément
  un cas d'échec**, à signaler dans le rapport.

### Lancer une eval

```bash
# Depuis ~/dotfiles, en session A :
cd ~/dotfiles/claude/commands/planning/evals
./setup-eval-cwd.sh preflight-nominal
# → imprime un chemin /tmp/planning-eval-preflight-nominal-<timestamp>/

# Dans un terminal séparé, session B vierge :
cd /tmp/planning-eval-preflight-nominal-<timestamp>
claude
# Puis taper : /planning
```

## Doctrine d'étoffage

Ajouter une eval **quand** :
- Une régression observée en usage réel rate un invariant non couvert → nouvelle
  classe ou nouveau fixture
- Un changement de modèle (Opus → autre) change le comportement → dupliquer une
  eval avec un champ `model`
- Une nouvelle gate, un nouveau plafond ou une nouvelle règle de vocabulaire est
  ajouté à `planning.md` → eval dédiée

Éviter :
- Les evals hypothétiques « au cas où » sans usage réel sous-jacent
- Les `expected_behavior` trop prescriptifs (décrire le **quoi observable**, pas
  le **comment**)
- La duplication entre evals : chaque eval cible un invariant différent

## Axes futurs (non bloquants)

- **Output quality** : eval `output_quality-*` jugée sur le `PLAN.md` final —
  vérifier les 4 sections (architecture, phases, séquence, paliers MVP) et que
  chaque palier regroupe bien des phases. Plus coûteux (dérouler l'interview
  entière + écriture).
- **CLAUDE.md absent** : eval `preflight` sur la branche « avertir mais continuer »
  (PRD présent, CLAUDE absent → message + demande de confirmation, pas d'arrêt).
- **Cross-modèles** : rejouer le corpus sur Sonnet (mesurer la dégradation vs Opus
  baseline) — pertinent surtout pour `vocabulary` et `interview_cap`, sensibles au
  modèle.
- **Argument-hint** : eval avec `/planning custom-name.md` pour vérifier la prise
  en compte de `$ARGUMENTS`.

## État du corpus

| Command | Statut | Nombre d'evals | Classes | Dernière mise à jour |
|---|---|---|---|---|
| `/planning` | ✅ bootstrap + classe `vocabulary` (ADR-0002) | 5 | `strict_mode_gate`, `preflight` (×2), `interview_cap`, `vocabulary` | 2026-06-22 |

⚠️ **Corpus écrit, non encore exécuté en A→B→A.** Les 5 evals sont spécifiées
mais aucun run n'a validé le comportement réel de `/planning` contre elles.
