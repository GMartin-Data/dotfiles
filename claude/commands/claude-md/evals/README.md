# Evals — `/claude-md`

> ⚠️ **Document en attente de refonte (2026-04-27).** Ce corpus a été conçu quand `claude-md` était une skill et instrumente la doctrine d'auto-invocation (`should_trigger` / `should_not_trigger` / `ambiguous_edge_case`). Suite au pivot doctrinal vers slash-command (qui est invoquée explicitement par l'utilisateur, donc sans logique de déclenchement à tester), la doctrine d'évaluation est entièrement à repenser autour du **comportement post-invocation** (pré-flight, Step 0, gates, skip criteria). À traiter dans une session dédiée. Le contenu ci-dessous est conservé comme matériel de base, mais ne reflète plus le design cible.

Corpus d'évaluation pour mesurer l'efficacité de la skill `claude-md` (trigger accuracy, instruction following, output quality).

## Doctrine

Approche **Evaluation-Driven Development** (Anthropic, [best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)) : les evals sont la **source de vérité** pour mesurer si la skill résout de vrais problèmes. On construit le corpus avant de documenter extensivement — et on l'étoffe par nécessité observée, pas par volonté de couverture.

Parallèle pytest-coverage : même logique d'accumulation incrémentale. Une régression observée en usage réel = une query à ajouter. Pas d'anticipation spéculative.

## Format

Chaque eval suit le schéma officiel Anthropic :

```json
{
  "skills": ["<skill-name>"],
  "query": "<prompt utilisateur simulé>",
  "files": ["<fixtures nécessaires, chemins relatifs>"],
  "expected_behavior": [
    "<invariant observable 1>",
    "<invariant observable 2>"
  ]
}
```

- `skills` : skills chargées dans le contexte du test
- `query` : prompt utilisateur, reflète un usage réel
- `files` : fixtures (repo vierge, `.cruft.json`, `PRD.md` existant, etc.)
- `expected_behavior` : invariants **observables** — pas une sortie exacte

## Classes de queries à couvrir

Anthropic recommande 3-5 queries par skill, réparties en trois classes :

1. **Should trigger** — cas clairs où la skill doit s'activer
2. **Should NOT trigger** — cas proches sémantiquement mais hors périmètre (teste le *negative space* de la description)
3. **Ambiguous edge cases** — cas intermédiaires où le comportement attendu est défini précisément

## Prérequis fixtures

Certaines queries nécessitent un **vrai environnement** (instance Cruft fraîche, CLAUDE.md pré-existant, etc.) — pas des mocks. Tester contre des fixtures simulées reviendrait à tester du code mort, puisque le pré-flight de la skill lit réellement `.cruft.json`, liste l'arbo, et lit `PRD.md`.

### Instance Cruft fraîche

- **Template source** : `~/python-project-template-v2` (repo local).
  ⚠️ Utiliser impérativement le suffixe `-v2`. Sans ce suffixe, le repo correspond à une ancienne tentative périmée qui fausserait les tests.
- **Création** : `cruft create ~/python-project-template-v2` dans un CWD temporaire
- **Queries concernées** : `trigger-positive-cruft-instance`

### CWD minimal avec CLAUDE.md pré-existant

- **Création** : `mkdir -p <cwd> && touch <cwd>/CLAUDE.md && mkdir <cwd>/src`
- **Queries concernées** : `trigger-edge-existing-claude-md`

### Aucune fixture (negative space)

- **Création** : CWD quelconque, même vide
- **Queries concernées** : `trigger-negative-user-global-conventions`

### Cycle de vie

Fixtures **éphémères** : créées à la demande, jetées après test. La reproductibilité est garantie par la version du template au moment du test (référencée via son état local `~/python-project-template-v2`), pas par des snapshots versionnés dans ce repo.

Pour automatiser la mise en place, utiliser le script `setup-eval-cwd.sh` fourni (cf. section Exécution).

## Exécution

**Il n'existe pas de runner natif Anthropic.** L'exécution se fait manuellement selon le pattern Claude A / Claude B (cf. section Rôles & Protocole ci-dessous).

Pour rejouer une eval :
1. **Monter le CWD** via le script fourni, depuis la session A :
   ```bash
   ./setup-eval-cwd.sh <eval-id>
   # exemple : ./setup-eval-cwd.sh trigger-positive-cruft-instance
   ```
   Le script crée un répertoire temporaire sous `/tmp/claude-md-eval-<id>-<timestamp>/` et imprime son chemin.
2. **Lancer une nouvelle session Claude Code** dans ce CWD — c'est la session B, contexte vierge, pas de continuation.
3. **Envoyer la `query`** telle quelle, telle que définie dans `claude-md.eval.json`.
4. **Capturer la transcription** produite par B (copier-coller l'output intégral).
5. **Transmettre la transcription à la session A** (retour dans `~/dotfiles`), qui coche les `expected_behavior` et produit le rapport matrice.

## Rôles & Protocole

Le protocole suit le triangle **A → B → A**, où A et B sont deux contextes isolés. La séparation n'est pas identitaire (« deux Claudes différents ») mais contextuelle : c'est l'isolation du contexte qui protège le test de la contamination cognitive.

### Les trois rôles

| Rôle | Qui | Contexte | Mission |
|---|---|---|---|
| **A (auteur)** | Session dans `~/dotfiles`, avec accès aux evals sur disque | Contexte projet, connaît les attentes | Conçoit la skill, monte les CWDs de test (via `setup-eval-cwd.sh`), juge les transcriptions de B contre les `expected_behavior` |
| **B (exécutant)** | Session dans `/tmp/claude-md-eval-<id>-*/`, contexte vierge | Aucune connaissance du projet dotfiles, aucune vue sur les evals | Reçoit la query nue, répond naturellement, **ne sait pas qu'elle teste** |
| **Humain** | Toi | Porte l'intention produit | Canal de transmission entre B et A (copie les transcriptions), valide ou amende le rapport matrice final |

### Pourquoi A peut juger B sans contamination

- A n'a pas produit la réponse de B : A ne peut pas rationaliser *a posteriori* ce qu'elle-même aurait écrit
- A n'a pas vu B « en live » : elle ne lit qu'un artefact figé (la transcription)
- B n'avait pas accès aux evals : sa réponse reflète un usage utilisateur réel, pas une satisfaction d'attentes
- L'isolation des CWDs garantit l'étanchéité structurelle, pas seulement intentionnelle

### Séquence complète d'une campagne de test

```
[Session A — setup]
  1. A lance setup-eval-cwd.sh pour chaque eval
  2. A fournit à l'humain la liste des CWDs temporaires
  3. A reste ouverte (ne pas /clear tant que la campagne n'est pas finie,
     sauf à s'appuyer sur /catchup au retour)

[Sessions B — une par eval, contexte vierge chacune]
  1. Humain : cd <cwd temporaire>, lance une nouvelle session Claude Code
  2. Humain : colle la query de l'eval
  3. B produit sa réponse naturelle (peut démarrer l'interview, poser des questions)
  4. Humain : laisse dérouler jusqu'à avoir vu assez pour juger les expected_behavior,
     puis coupe. Copie l'intégralité de la transcription.

[Retour session A — jugement]
  1. Humain colle les transcriptions dans A (une par une, pour gérer la longueur)
  2. A lit chaque transcription et coche les expected_behavior (✅ / ⚠️ / ❌)
  3. A produit le rapport matrice consolidé
  4. Humain relit le rapport et valide ou amende les cases ambiguës
  5. Décision : refinements à apporter à SKILL.md, ou corpus à étoffer
```

### Points d'attention (frictions connues)

- **`/catchup` ne restaure pas tout.** À la reprise de A après `/clear`, `/catchup` relit `progress.md` et le git log récent — pas les 3 fichiers `reference/` ni le contenu détaillé des evals. Si le protocole a besoin d'un détail, il doit être dans `progress.md`, pas seulement dans ce README. Ce README reste la doctrine **durable** ; `progress.md` est la **feuille de route opérationnelle** de la campagne.

- **Longueur des transcriptions.** Une session B qui déclenche correctement la skill peut produire plusieurs dizaines de lignes (interview complète). Coller les 3 transcriptions d'un coup dans A peut consommer 15-25 points de contexte. Préférer un traitement **séquentiel** : transcription 1 → jugement → transcription 2 → jugement → etc. L'humain peut aussi pré-élaguer ce qui est manifestement hors scope (small talk, détails non liés aux `expected_behavior`).

- **Durée de session B.** Les `expected_behavior` portent généralement sur les 30 premières secondes de B (détection de la skill, pré-flight, annonce d'allègement, première question). Il n'est **pas nécessaire** de dérouler l'interview complète. L'humain coupe dès qu'il a vu assez pour juger.

- **Échec silencieux de trigger.** Si B reçoit la query mais ne déclenche pas la skill (`trigger-positive-*` raté ou `trigger-negative-*` qui aurait dû rester inactif), B va répondre de manière générique, sans signaler qu'une skill était attendue. **C'est précisément un cas d'échec**, à noter comme tel dans le rapport matrice. L'absence de mention de la skill dans la transcription est un signal, pas un non-événement.

- **Consommation de contexte de la session A.** Une campagne complète (3 evals, 3 transcriptions, jugement) peut pousser A au-delà de 30-40 %. Accepter de `/progress` + `/clear` en cours de campagne est acceptable : le rapport matrice partiel est sauvegardé sur disque, la session A reprise via `/catchup` peut continuer avec les transcriptions restantes.

## Doctrine d'étoffage

Ajouter une query **quand** :
- La skill rate un trigger attendu en usage réel → nouvelle query *should trigger*
- Un false positive est observé (skill s'invoque à tort) → nouvelle query *should NOT trigger*
- Un edge case nouveau apparaît (combinaison non testée de fixtures) → nouvelle query *ambiguous*
- Un changement de modèle (Haiku/Sonnet/Opus) change le comportement → dupliquer une query existante en marquant le modèle dans un champ `model`

Éviter :
- Les queries hypothétiques « au cas où » sans usage réel sous-jacent
- Les `expected_behavior` trop prescriptifs (décrire le **quoi observable**, pas le **comment**)
- La duplication entre queries : chaque query doit cibler un invariant différent

## Axes futurs d'étoffage (non bloquants)

- **Cross-modèles** : rejouer le corpus sur Haiku et Opus, pas seulement Sonnet — l'efficacité varie par modèle
- **Coexistence** : tester la skill aux côtés de `prd` (et futurement d'autres skills) pour détecter les conflits de trigger
- **Isolation behavior** : vérifier que la skill fonctionne seule, sans `prd` ni autre skill chargée
- **Corpus élargi** : passer de 3 à 5-7 queries quand l'usage révèle de nouveaux cas
- **Profils de stack** : ajouter des queries dédiées quand la skill développe une logique dépendante d'un flag Cruft (ex. `use_dbt`, `use_terraform`). Tant que le comportement du pré-flight reste uniforme, la variation peut se faire par choix de réponses Cruft à l'exécution — pas par duplication dans le corpus JSON.

## État du corpus

| Skill | Statut | Nombre de queries | Dernière mise à jour |
|---|---|---|---|
| `claude-md` | ✅ bootstrap | 3 | 2026-04-22 |
| `prd` | ⏳ TODO | 0 | — |

**TODO** : créer `claude/skills/prd/evals/` avec un corpus équivalent lors de la prochaine session touchant à `/prd`. Même structure, mêmes classes de queries.
