# Evals — `/claude-md`

Corpus d'évaluation pour mesurer le **comportement post-invocation** de la slash-command `/claude-md` : pré-flight, Step 0, gates, allègement des phases.

## Doctrine

`/claude-md` est une slash-command : son déclenchement est explicite (l'utilisateur tape `/claude-md`), il n'y a pas de logique d'auto-invocation à tester. Les evals mesurent donc ce qui se passe **après** l'invocation :

- **Pré-flight** correct (lit `.cruft.json`, liste l'arbo, lit `PRD.md` quand ils existent)
- **Step 0** correct (gate replace/extend/abort si `CLAUDE.md` présent ; enchaîne sinon)
- **Skip criteria** respectés (pas d'interview standard quand instance pré-cadrée détectée)
- **Délégation aux fichiers `reference/`** au moment opportun (progressive disclosure effective)

Approche **Evaluation-Driven Development** (Anthropic, [best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)) : les evals sont la source de vérité pour mesurer si la command résout de vrais problèmes. On démarre minimal et on étoffe par nécessité observée — parallèle pytest-coverage, pas de couverture spéculative.

## Format

Chaque eval suit ce schéma :

```json
{
  "id": "<eval-id>",
  "class": "<preflight | step0_gate | ...>",
  "command": "/claude-md",
  "query": "<input utilisateur, généralement '/claude-md' nu>",
  "files": ["<fixtures nécessaires, chemins relatifs au CWD>"],
  "expected_behavior": [
    "<invariant observable 1>",
    "<invariant observable 2>"
  ]
}
```

- `class` : axe comportemental testé (pré-flight, gate Step 0, allègement, qualité d'output…)
- `query` : input utilisateur, le plus souvent `/claude-md` nu — éventuellement avec un argument (`/claude-md backend`)
- `files` : fixtures qui doivent exister dans le CWD au lancement de la session de test
- `expected_behavior` : invariants **observables** dans la transcription — pas une sortie exacte

## Classes comportementales

| Classe | Mesure | Exemple |
|---|---|---|
| `preflight` | Lecture correcte des artefacts d'instance, annonce d'allègement | `preflight-cruft-instance` |
| `step0_gate` | Gate replace/extend/abort quand CLAUDE.md préexiste | `step0-existing-claude-md` |
| `lightening` | Phases allégées effectivement court-circuitées (futur) | — |
| `output_quality` | Structure du CLAUDE.md généré (futur, plus coûteux à juger) | — |

Démarrage minimal : 2 evals (`preflight` + `step0_gate`). On ajoute par classe une fois qu'un cas réel le justifie.

## Fixtures

### Instance Cruft fraîche

- **Template source** : `~/python-project-template-v2` (repo local).
  ⚠️ Le suffixe `-v2` est **obligatoire**. Sans lui, le repo correspond à une ancienne tentative périmée qui fausserait les tests.
- **Création** : `cruft create ~/python-project-template-v2` (automatisé par `setup-eval-cwd.sh`)
- **Eval concernée** : `preflight-cruft-instance`

### CWD avec CLAUDE.md préexistant

- **Création** : `mkdir -p <cwd>/src && touch <cwd>/CLAUDE.md`
- **Eval concernée** : `step0-existing-claude-md`

Fixtures **éphémères** : créées à la demande sous `/tmp/`, jetées après test. La reproductibilité est garantie par l'état local de `~/python-project-template-v2`, pas par des snapshots versionnés ici.

## Exécution — protocole A → B → A

L'isolation contextuelle reste utile même sans logique d'auto-invocation : elle garantit un CWD propre (pas de fichiers parasites de la session A) et une transcription figée (l'auteur juge un artefact, pas un déroulé live).

| Rôle | Qui | CWD | Mission |
|---|---|---|---|
| **A (auteur)** | Session dans `~/dotfiles` | Projet | Monte les CWDs (`setup-eval-cwd.sh`), juge les transcriptions de B contre les `expected_behavior`, produit le rapport matrice |
| **B (exécutant)** | Session fraîche dans `/tmp/claude-md-eval-<id>-*/` | Fixture éphémère | Reçoit la query, exécute la command, produit la transcription |
| **Humain** | Toi | — | Canal de transmission (copie-colle les transcriptions vers A) |

### Séquence

```
[Session A — setup]
  1. A lance setup-eval-cwd.sh pour chaque eval-id
  2. A fournit à l'humain la liste des CWDs temporaires

[Sessions B — une par eval, contexte vierge chacune]
  1. cd <cwd temporaire> && claude
  2. Coller la query (généralement '/claude-md' nu)
  3. Laisser dérouler jusqu'à avoir vu les invariants attendus (Step 0, pré-flight,
     première question d'interview), puis couper
  4. Copier-coller l'intégralité de la transcription

[Retour session A — jugement]
  1. Coller les transcriptions une par une
  2. A coche chaque expected_behavior (✅ / ⚠️ / ❌)
  3. A produit le rapport matrice consolidé
```

### Frictions connues

- **`/catchup` ne restaure pas tout.** À la reprise de A après `/clear`, `/catchup` relit `progress.md` et le git log — pas ce README. Si le protocole a besoin d'un détail, il doit aussi être dans `progress.md`. Ce README porte la doctrine durable ; `progress.md` porte la feuille de route opérationnelle.

- **Durée de session B.** Les `expected_behavior` portent sur les premiers échanges (Step 0 → pré-flight → première question d'interview). Inutile de dérouler l'interview complète. Couper dès que les invariants sont observés ou clairement ratés.

- **Échec silencieux.** Si B reçoit `/claude-md` mais que la command rate un invariant (ex. saute Step 0, ne lit pas `.cruft.json`), elle peut continuer en générant du contenu. **C'est précisément un cas d'échec**, à signaler dans le rapport. L'absence d'un comportement attendu est un signal.

- **Consommation contexte de A.** Une campagne complète peut pousser A au-delà de 30-40 %. Accepter `/progress` + `/clear` en cours de campagne : le rapport partiel est sauvegardé, A reprise via `/catchup` continue avec les transcriptions restantes.

### Lancer une eval

```bash
# Depuis ~/dotfiles, en session A :
cd ~/dotfiles/claude/commands/claude-md/evals
./setup-eval-cwd.sh preflight-cruft-instance
# → imprime un chemin /tmp/claude-md-eval-preflight-cruft-instance-<timestamp>/

# Dans un terminal séparé, session B vierge :
cd /tmp/claude-md-eval-preflight-cruft-instance-<timestamp>
claude
# Puis taper : /claude-md
```

## Doctrine d'étoffage

Ajouter une eval **quand** :
- Une régression observée en usage réel rate un invariant non couvert → nouvelle classe ou nouveau fixture
- Un changement de modèle (Haiku/Sonnet/Opus) change le comportement → dupliquer une eval avec un champ `model`
- Une nouvelle gate ou un nouveau skip criterion est ajouté à `claude-md.md` → eval dédiée

Éviter :
- Les evals hypothétiques « au cas où » sans usage réel sous-jacent
- Les `expected_behavior` trop prescriptifs (décrire le **quoi observable**, pas le **comment**)
- La duplication entre evals : chaque eval doit cibler un invariant différent

## Axes futurs (non bloquants)

- **Allègement effectif** : eval `lightening-*` qui vérifie que les Phases 1, 2, 8, 11 sont court-circuitées (pas juste annoncées allégées)
- **Cross-modèles** : rejouer le corpus sur Haiku et Opus
- **PRD seul sans Cruft** : eval avec `PRD.md` mais pas de `.cruft.json` (chemin Phase 2 « Si PRD.md présent sans Cruft » dans `instance-aware-flow.md`)
- **Output quality** : evals `output_quality-*` jugées sur le CLAUDE.md final — plus coûteux car nécessite de dérouler l'interview entière

## État du corpus

| Command | Statut | Nombre d'evals | Dernière mise à jour |
|---|---|---|---|
| `/claude-md` | ✅ bootstrap (post-pivot command) | 2 | 2026-04-27 |
| `/prd` | ✅ bootstrap (post-pivot command) | 3 | 2026-04-27 |

Le corpus `/prd` vit sous `claude/commands/prd/evals/` — même doctrine, classes adaptées au flow PRD (`strict_mode_gate`, `block_validation`).
