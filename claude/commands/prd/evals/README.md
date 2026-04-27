# Evals — `/prd`

Corpus d'évaluation pour mesurer le **comportement post-invocation** de la slash-command `/prd` : strict-mode gate, pré-flight Cruft, allègement des phases techniques, skip criteria.

## Doctrine

`/prd` est une slash-command : son déclenchement est explicite (l'utilisateur tape `/prd`), il n'y a pas de logique d'auto-invocation à tester. Les evals mesurent ce qui se passe **après** l'invocation :

- **Strict-mode gate** correct (si `PRD.md` existe → arrêt avec message standard, pas de gate replace/extend/abort)
- **Pré-flight** correct (lit `.cruft.json` quand présent, vérifie l'arbo réelle pour `dbt/` / `terraform/`)
- **Allègement des Phases 8 et 10** quand instance Cruft détectée
- **Skip criteria** des Phases 7, 9, 10 respectés selon les conditions explicites
- **Validation finale en 3 blocs** (cadrage / scope / exécution) — un bloc à la fois

Approche **Evaluation-Driven Development** (Anthropic, [best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)) : les evals sont la source de vérité pour mesurer si la command résout de vrais problèmes. On démarre minimal et on étoffe par nécessité observée — parallèle pytest-coverage, pas de couverture spéculative.

## Format

Chaque eval suit ce schéma :

```json
{
  "id": "<eval-id>",
  "class": "<strict_mode_gate | preflight | lightening | skip_criteria | block_validation | ...>",
  "command": "/prd",
  "query": "<input utilisateur, généralement '/prd' nu>",
  "files": ["<fixtures nécessaires, chemins relatifs au CWD>"],
  "expected_behavior": [
    "<invariant observable 1>",
    "<invariant observable 2>"
  ]
}
```

- `class` : axe comportemental testé
- `query` : input utilisateur, le plus souvent `/prd` nu — éventuellement avec un argument (`/prd custom-name.md`)
- `files` : fixtures qui doivent exister dans le CWD au lancement de la session de test
- `expected_behavior` : invariants **observables** dans la transcription — pas une sortie exacte

## Classes comportementales

| Classe | Mesure | Exemple |
|---|---|---|
| `strict_mode_gate` | Arrêt immédiat si fichier de sortie déjà présent | `strict-mode-existing-prd` |
| `preflight` | Lecture correcte de `.cruft.json`, vérification arbo, annonce d'allègement | `preflight-cruft-instance`, `no-preflight-empty-cwd` |
| `lightening` | Phases 8 et 10 effectivement court-circuitées, pas juste annoncées allégées (futur) | — |
| `skip_criteria` | Phases 7, 9, 10 skippées selon conditions explicites (futur) | — |
| `block_validation` | Validation finale présentée bloc par bloc, attente explicite entre chaque (futur) | — |
| `output_quality` | Structure du PRD généré (futur, plus coûteux à juger) | — |

Démarrage minimal : 3 evals (`strict_mode_gate` + 2 × `preflight` couvrant les deux branches). On ajoute par classe une fois qu'un cas réel le justifie.

## Fixtures

### CWD avec PRD.md préexistant

- **Création** : `mkdir -p <cwd> && echo "# PRD — placeholder" > <cwd>/PRD.md`
- **Eval concernée** : `strict-mode-existing-prd`

### Instance Cruft fraîche

- **Template source** : `~/python-project-template-v2` (repo local).
  ⚠️ Le suffixe `-v2` est **obligatoire**. Sans lui, le repo correspond à une ancienne tentative périmée qui fausserait les tests.
- **Création** : `cruft create ~/python-project-template-v2` (automatisé par `setup-eval-cwd.sh`)
- **Note** : si le template génère un `PRD.md` par défaut, le script le supprime — sinon le strict-mode gate bloquerait l'eval.
- **Eval concernée** : `preflight-cruft-instance`

### CWD vide

- **Création** : `mkdir -p <cwd>` (rien d'autre)
- **Eval concernée** : `no-preflight-empty-cwd`

Fixtures **éphémères** : créées à la demande sous `/tmp/`, jetées après test. La reproductibilité est garantie par l'état local de `~/python-project-template-v2`, pas par des snapshots versionnés ici.

## Exécution — protocole A → B → A

L'isolation contextuelle reste utile même sans logique d'auto-invocation : elle garantit un CWD propre (pas de fichiers parasites de la session A) et une transcription figée (l'auteur juge un artefact, pas un déroulé live).

| Rôle | Qui | CWD | Mission |
|---|---|---|---|
| **A (auteur)** | Session dans `~/dotfiles` | Projet | Monte les CWDs (`setup-eval-cwd.sh`), juge les transcriptions de B contre les `expected_behavior`, produit le rapport matrice |
| **B (exécutant)** | Session fraîche dans `/tmp/prd-eval-<id>-*/` | Fixture éphémère | Reçoit la query, exécute la command, produit la transcription |
| **Humain** | Toi | — | Canal de transmission (copie-colle les transcriptions vers A) |

### Séquence

```
[Session A — setup]
  1. A lance setup-eval-cwd.sh pour chaque eval-id
  2. A fournit à l'humain la liste des CWDs temporaires

[Sessions B — une par eval, contexte vierge chacune]
  1. cd <cwd temporaire> && claude
  2. Coller la query (généralement '/prd' nu)
  3. Laisser dérouler jusqu'à avoir vu les invariants attendus (gate, pré-flight,
     première question d'interview), puis couper
  4. Copier-coller l'intégralité de la transcription

[Retour session A — jugement]
  1. Coller les transcriptions une par une
  2. A coche chaque expected_behavior (✅ / ⚠️ / ❌)
  3. A produit le rapport matrice consolidé
```

### Frictions connues

- **`/catchup` ne restaure pas tout.** À la reprise de A après `/clear`, `/catchup` relit `progress.md` et le git log — pas ce README. Si le protocole a besoin d'un détail, il doit aussi être dans `progress.md`. Ce README porte la doctrine durable ; `progress.md` porte la feuille de route opérationnelle.

- **Durée de session B.** Les `expected_behavior` portent sur les premiers échanges (gate strict-mode → pré-flight → première question d'interview). Inutile de dérouler l'interview complète — `/prd` est plus longue que `/claude-md` (13 phases + 3 blocs de validation). Couper dès que les invariants sont observés ou clairement ratés.

- **Choix du modèle.** `/prd` fixe `model: opus` dans son frontmatter (cadrage stratégique). Les sessions B doivent tourner sur Opus pour refléter le comportement réel — un test sur Sonnet ou Haiku mesure autre chose.

- **Échec silencieux.** Si B reçoit `/prd` mais que la command rate un invariant (ex. saute le strict-mode gate, ne lit pas `.cruft.json`), elle peut continuer en générant du contenu. **C'est précisément un cas d'échec**, à signaler dans le rapport.

- **Consommation contexte de A.** Une campagne complète peut pousser A au-delà de 30-40 %. Accepter `/progress` + `/clear` en cours de campagne : le rapport partiel est sauvegardé, A reprise via `/catchup` continue avec les transcriptions restantes.

### Lancer une eval

```bash
# Depuis ~/dotfiles, en session A :
cd ~/dotfiles/claude/commands/prd/evals
./setup-eval-cwd.sh strict-mode-existing-prd
# → imprime un chemin /tmp/prd-eval-strict-mode-existing-prd-<timestamp>/

# Dans un terminal séparé, session B vierge :
cd /tmp/prd-eval-strict-mode-existing-prd-<timestamp>
claude
# Puis taper : /prd
```

## Doctrine d'étoffage

Ajouter une eval **quand** :
- Une régression observée en usage réel rate un invariant non couvert → nouvelle classe ou nouveau fixture
- Un changement de modèle (Opus → autre) change le comportement → dupliquer une eval avec un champ `model`
- Une nouvelle gate, un nouveau skip criterion ou un nouveau bloc de validation est ajouté à `prd.md` → eval dédiée

Éviter :
- Les evals hypothétiques « au cas où » sans usage réel sous-jacent
- Les `expected_behavior` trop prescriptifs (décrire le **quoi observable**, pas le **comment**)
- La duplication entre evals : chaque eval doit cibler un invariant différent

## Axes futurs (non bloquants)

- **Allègement effectif** : eval `lightening-*` qui vérifie que les Phases 8 et 10 sont court-circuitées (pas juste annoncées allégées) — ex. Phase 8 qui ne pose qu'**une seule question ouverte** au lieu de l'interview complète
- **Skip criteria** : evals dédiées par condition (interface = web → Phase 7 skippée ; "prototype" en Phase 6 → Phase 9 skippée ; 1 seul composant → Phase 10 skippée)
- **Block validation** : eval `block_validation-*` qui vérifie la séquence en 3 blocs séparés (cadrage / scope / exécution), un seul à la fois, attente explicite de validation
- **Cross-modèles** : rejouer le corpus sur Sonnet (mesurer la dégradation vs Opus baseline)
- **Output quality** : evals `output_quality-*` jugées sur le PRD final — plus coûteux car nécessite de dérouler l'interview entière + les 3 blocs de validation
- **Argument-hint** : eval avec `/prd custom-name.md` pour vérifier la prise en compte de `$ARGUMENTS`

## État du corpus

| Command | Statut | Nombre d'evals | Dernière mise à jour |
|---|---|---|---|
| `/claude-md` | ✅ bootstrap (post-pivot command) | 2 | 2026-04-27 |
| `/prd` | ✅ bootstrap (post-pivot command) | 3 | 2026-04-27 |
