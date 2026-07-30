# Evals /immunize — refonte ADR-0015

Corpus d'evals comportementales de la command `claude/commands/immunize.md`,
écrit **failing d'abord** (porte de validation ADR-0015 : rouge sur la command
actuelle → refonte → vert → run réel A→B→A → `Accepted`).

Format : `immunize.eval.json` (précédent : corpus `/grill`), expectations en
signal observable (fichiers écrits, structure du plan, arrêts), fixtures à
tension délibérée.

## Couverture des décisions ADR-0015

| Eval | Classe | Décisions ADR |
|---|---|---|
| `artifact-lesson-routes-to-artifact-fix` | `tri_destination` | D4 (routage par ancrage d'artefact) |
| `global-candidate-blocked-at-eval-gate` | `promotion_gate` | D2 (porte globale), D6 (verdict 3 issues), D3 (formulation) |
| `add-mode-append-then-stop` | `add_mode` | D7b (mode ajout) |
| `insights-fiche-relocated-not-archived` | `inbox_population` | D1 (inbox mono-population) |
| `project-rule-format-100-accurate` | `rule_format` | D2 (projet sans porte), D3 (100 %-accurate) |

Non couvert par eval de session : **D5** (éviction event-driven — déclencheurs
inter-sessions : changement de tier, cap atteint, suspicion documentée ;
s'éprouve au premier changement de modèle par rejeu du corpus claude-md) ;
**D7a** (gouvernance matrice — sync documentaire, pas comportement de command).

## Rouge — inspection contre la command actuelle (2026-07-30)

| Eval | Ancre du fail dans `immunize.md` (HEAD) |
|---|---|
| `artifact-…` | Étape 3-A : seules destinations = règle prose projet/global — la leçon hook serait promue en règle |
| `global-…` | Étape 3-A, Cas C : « aucune règle similaire en global → ajouter comme candidate » — écriture directe sans preuve d'eval |
| `add-mode-…` | `argument-hint` déclaré au frontmatter mais aucune branche dans la procédure — triage complet inconditionnel |
| `insights-…` | Étape 3-B : « Entrée unique, > 7 jours → Archivage » sans distinction de population |
| `project-format-…` | « Format des règles promues » : template unique « Ne jamais [X] — utiliser [Y] » |

Statut : rouge par inspection le 2026-07-30, refonte le même jour, **vert par
inspection 5/5** contre la command refondue, puis **run réel A→B→A PASS 11/11**
(section dédiée) — porte d'ADR-0015 franchie, ADR `Accepted` le 2026-07-30.

## Fixtures

Projet fictif `meteo-pipeline` (ingestion Open-Meteo → DuckDB → dbt).
Assemblage CWD : `fixtures/common/CLAUDE.md` → `CLAUDE.md` ;
`fixtures/<eval>/lessons-inbox.md` → `tasks/lessons-inbox.md` ;
`fixtures/artifact-routing/hooks/check_partition.py` → `hooks/check_partition.py`.

- `check_partition.py` porte réellement le bug incriminé (`findall` compte les
  mentions en commentaire comme des directives) — l'ancre artefact est
  vérifiable dans le CWD.
- L'en-tête des inbox reproduit le template actuel (pré-refonte) : le verdict
  se lit dans le comportement de la command, pas dans la fixture.
- Dates statiques (limite assumée du parc) : les tensions « > 7 j » restent
  vraies quand le temps avance ; la date de revue de la fiche `[INSIGHTS]`
  (2026-09-01) sera un jour dépassée — l'expectation n'en dépend pas (la
  relocalisation tient à la population, pas à l'âge).
- Eval `global-gate` : exige un payload global SANS règle équivalente au
  pattern « chemins relatifs sous scheduler » — le payload réel convient à ce
  jour.

## Outillage de run

- `setup-eval-cwd.sh <eval-id>` : assemble un CWD `/tmp/immunize-eval-*` —
  fixtures en place, `git init` + commit (l'ancre « artefact versionné » du
  critère tri_destination est littéralement vraie), entrée fraîche J-2 datée
  dynamiquement pour `triage-complet` (les replays la gardent fraîche).
- **Config réelle, pas d'isolation `CLAUDE_CONFIG_DIR`** : ces evals ne
  varient pas le payload, et la payload symlinkée expose la command du working
  tree. Filets : garde anti-écriture-globale dans le script de tours
  (`fixtures/triage-complet-interview-script.md`), hash de
  `~/.claude/CLAUDE.md` vérifié avant/après, global tracké git.
- Sessions B : `drive-session.py <in.jsonl> <out.jsonl> <cwd> --model opus
  --settings '{"effortLevel":"high"}' --permission-mode acceptEdits`.
  **`--permission-mode acceptEdits` est indispensable** : contrairement aux
  corpus grill/prd (zéro écriture), cette command écrit — sans le flag, le
  premier Edit est bloqué en `-p` (constaté au premier run). Propriété voulue :
  acceptEdits n'auto-accepte que dans le CWD, une écriture globale hors CWD
  resterait bloquée.
- Grading : les tours `[USER]` injectés ne sont **pas échoés** dans le flux
  stream-json de sortie — un invariant « écriture après confirmation » se
  prouve par les frontières de tours (events `result` : le driver n'envoie le
  message N+1 qu'après le `result` du tour N), jamais par la présence de tours
  user dans la transcription. Précédent : E6 du run réel, ⚠️ grader requalifié
  ✅ sur cette preuve.

## Run réel A→B→A (2026-07-30) — porte ADR-0015

Deux sessions B (Opus/high, pin `model: sonnet` de la command actif) :

| Run | Fixture | Tours | Verdict |
|---|---|---|---|
| `triage-complet` (composite, toutes populations) | `fixtures/triage-complet/` | 3 scriptés | **6/6** (grader Sonnet isolé 5/6 + E6 requalifié ✅ sur preuve harnais) |
| `add-mode` (mono-tour) | `fixtures/add-mode/` | 1 | **5/5** (déterministe : diff filesystem + transcription de 4 events) |

Vérifications filesystem du composite : `insights-actions.md` créé (fiche
intégrale + trace), `lessons-archive.md` créé (traces de routage par groupe),
CLAUDE.md projet +1 règle conditionnelle, inbox réécrite (candidate taguée +
fraîche), hook intact, `~/.claude/CLAUDE.md` byte-identique.

Leçon d'artefact surfacée par le premier run (et fixée) : l'append naturel
passe par **Edit**, absent des `allowed-tools` d'origine — ajouté au
frontmatter de la command.
