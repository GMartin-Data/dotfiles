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

Statut : **rouge par inspection** — aucun run réel à ce stade ; le vert par
inspection puis le run réel A→B→A conditionnent le passage de l'ADR en
`Accepted`.

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

## Outillage de run (au passage vert / run réel)

- Setup CWD à écrire (adapter `setup-eval-cwd.sh` des corpus claude-md/grill :
  isolation `CLAUDE_CONFIG_DIR`, payload global contrôlé, fixtures en place).
- Evals 1/2/4/5 : la command demande confirmation avant écriture → sessions B
  pilotées par `claude/evals/drive-session.py` (tours scriptés). Eval 3
  (add-mode) : mono-tour.
