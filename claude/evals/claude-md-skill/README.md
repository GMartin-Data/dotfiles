# Evals — `claude-md` (runner officiel)

Corpus d'évaluation de la skill `claude/skills/claude-md/` : comportement
**post-invocation** — gate Step 0 sur un `CLAUDE.md` existant, gate
conditionnelle Cruft + PRD, pré-flight en deux blocs, ouverture de la Phase 1
sur instance. Pas de discovery : la skill est invoquée explicitement
(`/claude-md`), l'auto-invocation n'est pas un objet de test.

**Contrat testé** : les blocs `#### Test` du SKILL.md (Step 0, Gate
conditionnelle, Bloc 2 — Annonce d'allègement). Les blocs sont les graines des
cas : chaque rubrique `llm` cite la section et le bloc qu'elle vérifie, et un
cas ne teste rien que le SKILL.md ne prescrive. Les blocs des autres sections
(règles d'interaction, validation finale, après génération) attendent un cas
multi-tours (voir Doctrine d'étoffage).

**Moteur** : `claude plugin eval` ([ADR-0016](../../../adr/0016-moteur-evals-runner-officiel-mono-tour-driver-maison-interviews.md)).
Deuxième corpus porté sur ce moteur (Phase 3 de l'audit
`tasks/skill-evals-audit-2026-09.md`), après `feynman-mentor/`.

**Lignée** : corpus G1 (protocole manuel A→B→A) écrit le 2026-04-27 sous
`commands/claude-md/evals/` au pivot skill → command, jamais rejoué depuis ;
porté au runner le 2026-09-23 avec le pivot inverse command → skill. Les
trois cas sont mono-tour (ils s'arrêtent à la première question ou au message
d'arrêt) : règle R9 de l'audit, sous-ensemble mono-tour → runner à la
retouche de l'artefact.

## Packaging

- Plugin racine : `claude/` (`claude/.claude-plugin/plugin.json`, nom
  `dotfiles`). Chargé **uniquement** par `claude plugin eval` /
  `--plugin-dir`, jamais en session quotidienne. La skill sous test s'appelle
  `dotfiles:claude-md` ; le prompt `/claude-md` la résout sans préfixe
  (vérifié à la sonde). L'invocation par slash est **développée inline** dans
  le tour utilisateur, sans appel `Skill` : aucun indicateur
  `tool_used: Skill` n'est possible — la résolution se prouve par les graders
  de comportement eux-mêmes (message d'arrêt, blocs, gate).
- Dossier `claude-md-skill/` : suffixe imposé par la collision avec
  `claude/evals/claude-md/`, corpus batch A du **CLAUDE.md global** (G3,
  sans rapport avec cette skill).
- Fixtures par `context.scaffold_script` (`scaffold.sh` dans chaque dossier
  de cas — chemin relatif au cas, obligatoire) : exécuté avant **chaque run**
  dans le workspace vide, comme l'utilisateur, hors sandbox ; requiert
  `--scaffold` en ligne de commande. Les deux cas Cruft appellent
  `cruft create` sur `~/python-project-template-v2` (suffixe `-v2`
  obligatoire ; `CRUFT_TEMPLATE_PATH` pour surcharger). Le template ne génère
  ni `CLAUDE.md` ni `PRD.md` (vérifié 2026-09-23) ; le cas « sans PRD »
  supprime `PRD.md` par précaution.
- Résultats : `claude/evals/results/<timestamp>/` (gitignoré) ; les JSON qui
  font foi sont copiés dans `results/` de ce dossier (voir État).
- Prérequis : Claude Code ≥ 2.1.269, `cruft` (`uv tool install cruft`), le
  template local.

## Cas et classes

| Cas | Classe | `runs` | Graders | Question posée (une seule) |
|---|---|---|---|---|
| `preflight-cruft-without-prd` | `gate_conditional` | 3 | `regex` message d'arrêt, `track léger`, ¬Bloc 2 ; `file_exists` CLAUDE.md absent ; `llm` | Cruft sans PRD : message d'arrêt reproduit, puis attente sans pré-flight ni question ? |
| `preflight-cruft-with-prd` | `preflight` | 3 | `regex` ¬message d'arrêt, marqueur Bloc 2, `instance-aware-flow.md` ; `file_exists` ; `llm` | Cruft + PRD : deux blocs, Phases 1, 2, 8, 11 seules allégées, Phase 1 = une confirmation sur le territoire CLAUDE.md ? |
| `step0-existing-claude-md` | `step0_gate` | 3 | `tool_used` Write / Edit `0` ; `regex` fichier resté vide ; `regex` ¬Bloc 2 ; `llm` | CLAUDE.md vide présent : signalé vide, question remplacer / étendre / abandonner, rien d'autre ? |

## Règles de design (contrat du corpus)

Les règles 1 à 7 du corpus `feynman-mentor/` (README § Règles de design)
s'appliquent ; spécifiques ici :

1. **Seeds = blocs `#### Test` du SKILL.md.** Un cas dérive d'une ligne
   `situation → observable` d'un bloc ; une ligne sans cas est une dette
   visible, un cas sans ligne est hors contrat.
2. **Invocation explicite, `--ablation none`.** Le bras « sans » n'a pas de
   sens pour une skill invoquée par slash, et il n'existe pas d'indicateur de
   déclenchement (invocation développée inline, voir Packaging) : une
   invocation qui ne résout pas rougit tous les graders de comportement, ce
   qui est le verdict voulu.
3. **Tier Sonnet** (`--model claude-sonnet-5`) : le frontmatter pinne
   `model: sonnet`, le tier de session est sans effet sur cette skill. Fable
   et Opus ne redeviennent pertinents que si le pin saute.
4. **Accorder ce que l'invariant interdit** : `Write` sur les trois cas,
   `Edit` sur Step 0 (`--allow-tools Bash Write Edit`) — sans quoi « rien
   d'écrit avant la décision » est trivial. `Bash` reste nécessaire au
   pré-flight (arborescence).
5. **`regex` sur les marqueurs verbatim du SKILL.md seulement** (message
   d'arrêt, « allégées ou pré-remplies », `instance-aware-flow.md`,
   fichier vide) ; le contenu des blocs et le territoire des questions sont
   jugés par `llm`.
6. **`runs: 3` partout** : des gates déterministes en apparence, mais un run
   unique masque la variance (audit §3.3).
7. **Rubriques courtes, en « PASS si / FAIL seulement si », non-violations
   explicites.** Le juge du runner est *strict, sec et sans raisonnement*
   (système « strict, terse evaluation judge », réponse en un mot, trois
   votes) : une rubrique longue à conditions conjonctives rougit un
   comportement conforme (voir Frictions). Une question par grader `llm`,
   et dire noir sur blanc ce que la skill prescrit et qui pourrait passer
   pour une faute (ici : le résumé du PRD dans le Bloc 1).

## Exécution

Depuis un répertoire vide (le runner écrit `out/` et, avec `--keep-temp`, les
traces sous `/tmp/claude-eval-*`) :

```bash
# Sonde mécanique (1 cas, 1 run) — scaffold, résolution de /claude-md, graders
claude plugin eval ~/dotfiles/claude --trust-plugin --case preflight-cruft-without-prd \
  --ablation none --scaffold --runs 1 --model claude-sonnet-5 --judge-model sonnet \
  --allow-tools Bash Write --keep-temp --no-publish --json out.json

# Campagne (3 cas × 3 runs)
claude plugin eval ~/dotfiles/claude --trust-plugin --tag claude-md \
  --ablation none --scaffold --model claude-sonnet-5 --judge-model sonnet \
  --allow-tools Bash Write Edit -j 2 --max-cost-usd 3 --no-publish --json out.json
```

`--runs` en ligne de commande écrase le `runs` des cas ; ne le passer que pour
une sonde. Juge Sonnet (précédent feynman-mentor).

## Frictions connues

- **Le runner remplace `HOME` pour le scaffold** (`/tmp/claude-eval-*/home`,
  observé sur 2.1.280 — la doc dit le contraire) : `~/python-project-template-v2`
  ne résout pas, et `cruft` installé par `uv tool` sort du PATH. Les scripts
  résolvent le home réel par `getent passwd` et cherchent `cruft` dans
  `$REAL_HOME/.local/bin` à défaut du PATH ; testé en local sous `HOME`
  factice et `PATH=/usr/bin:/bin` avant la sonde.
- **`/claude-md` dans le prompt ne produit pas d'appel `Skill`** (sonde
  2026-09-23 : `Skill called 0x`, comportement pourtant conforme, 0,13 $ le
  run) : la slash-command est développée dans le message utilisateur. Le
  grader `skill-fired` du corpus feynman-mentor ne vaut que pour les
  déclenchements par description.
- **Le juge ne raisonne pas, et c'est mesurable.** Première campagne :
  `preflight-cruft-with-prd` rouge 3/3, juges unanimes (9 votes FAIL), tous
  les `regex` verts, réponses conformes à la lecture. Le gabarit du juge,
  extrait du binaire 2.1.280 : système « You are a strict, terse evaluation
  judge for coding-agent traces. », puis « You are grading the output of a
  coding agent against a criterion. / Criterion: … / Agent output
  (last_message): … / Respond with exactly one word: PASS or FAIL. » Rejoué
  à l'identique sur Sonnet 5 hors runner : 1 FAIL sur 3 ; rejoué en demandant
  la raison : PASS 7/7 avec justification clause par clause. La rubrique
  d'origine (une seule `llm`, quatre clauses conjonctives, deux listes de
  phases) a été scindée en deux graders courts (règle 7). Le runner ne
  restitue pas le raisonnement des juges : sur un rouge unanime avec regex
  verts, suspecter la rubrique avant la skill.
- **Le scaffold est rejoué avant chaque run** : `cruft create` (clone git du
  template) coûte quelques secondes par run, pas par cas.
- **`file_exists` porte sur les fichiers créés par Claude**, pas sur la
  fixture : `CLAUDE.md` absent des deux cas Cruft rend le grader non ambigu ;
  sur Step 0, où la fixture contient un `CLAUDE.md`, l'invariant passe par
  `regex` sur le contenu du fichier (`target: {source: file}`) plus
  `tool_used` Write / Edit à zéro.

## Doctrine d'étoffage

Ajouter un cas **quand** une régression observée en usage réel rate un
invariant non couvert, ou quand une ligne d'un bloc `#### Test` mérite sa
propre fixture. Axes identifiés, non couverts :

- **Allègement effectif** (`lightening`) : vérifier que les Phases 1, 2, 8,
  11 sont court-circuitées, pas seulement annoncées — multi-tours, donc
  driver maison `claude/evals/drive-session.py` (G3), pas le runner.
- **PRD sans Cruft** : branche « Si PRD.md présent sans Cruft » de
  `instance-aware-flow.md` — mono-tour, portable ici.
- **`skip:` visible** (règle 7) : une phase hors sujet doit laisser une ligne
  `skip: Phase N — <raison>` — gradable par `regex`, mais n'apparaît qu'en
  cours d'interview (G3).
- **Validation finale et après génération** : interview complète (G3, coûteux).
- **Cross-modèles** : seulement si le pin `model: sonnet` saute.

Éviter les cas hypothétiques, les rubriques prescrivant le *comment* au lieu
du *quoi observable*, la duplication entre cas.

## État du corpus

Campagne du 2026-09-23 (Claude Code 2.1.280, Sonnet 5 pour la skill et le
juge, **2,30 $** au runner pour 19 runs, plus ~0,5 $ de rejeux de juge hors
runner ; JSON figés sous `results/`, un fichier par passe). Deux passes : la
première (sonde + 9 runs) a validé la mécanique et rougi
`preflight-cruft-with-prd` sur sa rubrique, comportement conforme (voir
Frictions) ; la seconde a scindé la rubrique et rejoué ce cas, plus Step 0
pour un run à réponse vide.

| Cas | Sonnet | Source |
|---|---|---|
| `preflight-cruft-without-prd` | ✅ 1,0 (1,0 / 1,0 / 1,0) | passe 1 (`pass1-sonnet-campaign`) |
| `preflight-cruft-with-prd` | ✅ 1,0 (1,0 / 1,0 / 1,0), 18 votes PASS | passe 2 (`pass2-sonnet-with-prd-rubric-split`) ; passe 1 : 0,8 × 3 sous la rubrique v1 |
| `step0-existing-claude-md` | ✅ 1,0 (1,0 / 1,0 / 1,0) | passe 2 (`pass2-sonnet-step0-rerun`) ; passe 1 : 1,0 / 1,0 / 0,8 |

**Lecture des gris de la passe 1.** `with-prd` : rouge 3/3 sur la seule
rubrique `llm`, regex verts, réponses conformes à la lecture (Bloc 1 complet,
Bloc 2 verbatim, Phase 1 = une confirmation « Correct ? ») — rubrique
requalifiée, pas la skill. `step0` run 1 : réponse finale vide après 2 tours
(graders déterministes verts par vacuité, juge en erreur d'API) — non
reproduit sur 3 runs supplémentaires ; sans trace (`--keep-temp` absent),
inexpliqué, compté comme aléa unique à surveiller.

**Verdict** : 3 cas sur 3 verts sur le tier réel de la skill (Sonnet, pinné
au frontmatter). Le corpus vaut garde de non-régression de la migration
command → skill et première preuve « blocs `#### Test` → cas » (Phase 3 de
l'audit). Coût unitaire observé : ~0,10 $ le run Step 0, ~0,13 $ le run
gate, ~0,20 $ le run pré-flight complet.
