# Audit — process d'évaluation des skills et frontmatter (2026-09)

Audit instruit le 2026-09-22 dans `~/dotfiles`, sur brief
`tasks/skill-evals-audit-2026-09-brief.md` (pièce jointe
`tasks/skill-evals-audit-2026-09-docs.md`). Chaque affirmation cite sa preuve :
commande exécutée, fichier du repo, ou URL fetchée le 2026-09-22.

## 0. Verdict

**Q1 — Process maison vs officiel : hybride v2.** `claude plugin eval` (2.1.278)
devient le moteur d'exécution pour les **skills** et pour tout cas **mono-tour** ;
le harnais maison G3 (`claude/evals/drive-session.py` + scripts batch) reste le
moteur des **interviews multi-tours** (grill, prd, claude-md, planning, adr,
immunize) et de la **variation de payload global** (corpus claude-md). Le moteur
G2 (skill-creator, ADR-0009 Option C) est intégralement couvert par le runner et
s'éteint. ADR-0009 est à **étendre**, pas à renverser. Preuve : deux pilotes
(§3), 2,80 $ au total — les 6 invariants du corpus feynman-mentor s'expriment
sur le runner, l'isolation est native, l'ablation mesure la contribution de la
skill, et 3 runs révèlent une variance qu'un run unique masquait.

**Q2 — Chantier frontmatter : non, pas de chantier autonome.** Aucune violation
de spec sur les 15 artefacts (§4.2). Un seul champ nouveau franchit le seuil du
brief — `disallowed-tools` — et son effet est **limité au tour d'invocation**
(§4.3), donc il complète la prose et l'eval sans les remplacer. Le reste des
retouches utiles est absorbé par le chantier Q1 (migration `claude-md` en skill,
nettoyage opportuniste).

**Q3 — Transmission : ce fichier + routage matrice (§5).** Décision → ADR
(Extends 0009) ; chantier → brief `tasks/` phasé (§6) ; matrice, CLAUDE.md global
et CLAUDE.md projet inchangés ; trois leçons pour `tasks/lessons-inbox.md` ;
learning record 0004 côté workspace d'apprentissage.

Corrections au brief (§1.3 « non relu ») : 15 artefacts, pas 16 (6 skills + 9
commands — `ls claude/skills claude/commands`) ; le process maison ne se réduit
pas à `feynman-mentor/evals/` — il a trois générations (§2.1).

## 1. Périmètre, méthode, coûts

### 1.1 Sources

| Type | Source | Vérification |
|---|---|---|
| Doc runner | https://code.claude.com/docs/en/plugin-evals.md | pièce jointe §1 (fetch 2026-09-22) + `claude plugin eval --help` local |
| Doc plugins | https://code.claude.com/docs/en/plugins-reference.md | pièce jointe §2 |
| Doc skills | https://code.claude.com/docs/en/skills.md | pièce jointe §3 ; sections « synced skills » et « précédence des noms » re-fetchées en session |
| Spec Agent Skills | https://agentskills.io/specification | pièce jointe §4 |
| Version locale | `claude --version` → `2.1.278 (Claude Code)` | canal `latest` (`40dc978`) |
| Sandbox Linux | `which bwrap socat` → `/usr/bin/bwrap`, `/usr/bin/socat` | prérequis Bash du runner présents |
| Process maison | `adr/0009`, `adr/0015`, `claude/evals/*/README.md`, `claude/commands/*/evals/README.md`, `claude/skills/feynman-mentor/evals/`, `git log` | lus intégralement |

### 1.2 Contraintes respectées

- Aucune skill ni command du repo modifiée. Le pilote feynman a tourné sur une
  **copie** dans le scratchpad de session (`fm-plugin/`), cible chemin.
- Le cobaye `converting-temperatures` (`~/.claude/skills/`, hors repo) porte
  encore le manifest et `evals/` ajoutés pour le test — purge à la main de Greg
  (hook `block-rm-rf`). `sha256sum SKILL.md` avant test :
  `b3202f1de1c4f6567a58fc25fae8239c766d31f065b18489e5490c343b37b00b` (inchangé).
- `~/.claude/settings.json` : une seule clé ajoutée, validée par Greg —
  `syncClaudeAiSkills: false` (`2d75189`, §1.4).

### 1.3 Runs et coûts (`costUsd` des JSON de résultat)

| Run | Cible | Cas × bras × runs | Coût | Durée |
|---|---|---|---|---|
| cobaye #1 | `converting-temperatures@skills-dir` | 1 × 2 × 1 | 0,138 $ | 7 s |
| cobaye #2 (`--keep-temp`) | idem | 1 × 2 × 1 | 0,139 $ | 8 s |
| feynman suite | `fm-plugin` (chemin) | 6 × 2 × 1, juge Sonnet | 1,986 $ | 225 s |
| feynman re-run candide | `--case candide-never-fills-gaps` | 1 × 1 × 3 | 0,487 $ | 30 s |
| feynman re-run no-web | `--case no-web-lookup`, `history_file` | 1 × 1 × 1 | 0,054 $ | 20 s |
| **Total** | | 23 runs agent | **2,803 $** | |

Sondes annexes (`claude -p`, Haiku) : `/skill-doctor`, `/code-review` ×2 —
quelques cents.

### 1.4 Fait d'environnement traité en préalable

La sync claude.ai → terminal (« Syncing in terminal sessions requires Claude Code
v2.1.273 or later », skills.md) s'est activée le 2026-09-22 11:53 avec le passage
au canal `latest` : 22 skills dans `~/.claude/skills/synced/`, dont **9 copies
périmées** de skills maison (`manifest.json` : feynman-mentor `2025-12-29`,
coach-pedagogique `2026-04-13`, prd-interview, conventions-interview,
tech-watch, critical-analysis, dbt-learning-coach, discovery-guide,
kimball-data-mart). La copie synchronisée de feynman-mentor porte le trigger
« teach me by explaining » que le corpus maison a servi à éliminer. Pour `/nom`
tapé, la skill locale gagne (« the synced skill still runs as
`/anthropic-skills:<name>` ») ; pour l'auto-invocation, les deux descriptions
sont en contexte. Décision : `syncClaudeAiSkills: false` (« the next time it
starts it moves the skills it already synced to `~/.claude/skills/.trash/` »),
commit `2d75189`. Effet sur cet audit : nul pour le runner (session enfant
isolée, §2.4) ; réel pour les sondes en conditions réelles et l'usage quotidien.

## 2. Q1 — Process maison vs `claude plugin eval`

### 2.1 Le process maison a trois générations

> **Rappel — G1, G2, G3 sont des étiquettes de cet audit**, pas des noms du
> framework. Elles distinguent trois *moteurs d'exécution* successifs ; la
> doctrine (classes comportementales, fixtures à tension délibérée, invariants
> observables, étoffage par nécessité) est la même à travers les trois. Seul
> change « qui fait tourner la session B et qui juge ».

| | Session B pilotée par | Jugée par | Ce qui a motivé la suivante |
|---|---|---|---|
| **G1** A→B→A manuel | un humain (copie-colle la transcription vers A) | la session A | coût manuel : le corpus grill est resté six semaines sans exécution |
| **G2** skill-creator | des sous-agents du plugin officiel | un sous-agent Grader | ne sait ni piloter une interview multi-tours, ni isoler une config |
| **G3** moteur maison automatisé | `drive-session.py` (`claude -p`, tour par tour) + scripts batch | grader Sonnet isolé, ou inspection + filesystem | — c'est l'état actuel ; le runner officiel en couvre nativement la partie mono-tour |

| Gén. | Période | Mécanique | Corpus | Preuve |
|---|---|---|---|---|
| **G1** A→B→A manuel | juin | `*.eval.json` `{id, class, query, files, expected_behavior}` + `setup-eval-cwd.sh` ; l'humain copie-colle les transcriptions | adr, claude-md, grill, planning, prd (`claude/commands/*/evals/`) | ADR-0009 §Contexte ; README des corpus |
| **G2** skill-creator | 2026-07-23, un seul run | format officiel `evals/evals.json`, sous-agents Executor/Grader, with/without (Δ +0.82) ; proxy de trigger `run_eval.py` jugé biaisé → discovery testée en conditions réelles | feynman-mentor | `git log -- claude/skills/feynman-mentor/evals/` → `eaa67bb 2026-07-23` ; README §Frictions |
| **G3** moteur maison automatisé | 2026-07-28 → 08-07 | `drive-session.py` (tours conditionnels via `stream-json`, message N+1 après `result` N), `run-batch.sh` (34 runs avec/sans, `CLAUDE_CONFIG_DIR` isolé), `run-campaign.sh` (A/B × tiers × répétitions), `--permission-mode acceptEdits` + garde anti-écriture globale ; grading Sonnet isolé ou inspection + vérifs filesystem | claude-md, code-review, immunize (`claude/evals/`) ; grill (21/22) et prd rejoués | `git log -- claude/evals/` → `92d374d 07-28`, `e6a5b12 07-29`, `d117bf5 07-30`, `0b8be84 08-07` ; `progress.md` checkpoints 07-29 → 08-07 |

**Constat central** : la question « maison vs officiel » a déjà été tranchée une
fois — ADR-0009 (2026-06-23, `Accepted` après le run G2 du 07-23) retient
l'Option C « moteur officiel, doctrine maison ». Mais dès le 28 juillet la
pratique a construit G3 — parce que skill-creator ne sait ni piloter une
interview multi-tours ni isoler une config — **sans amendement de l'ADR**. Le
brief rouvre donc une question déjà instruite, avec un troisième concurrent qui
ressemble davantage à G3 qu'à G2. Ce que G3 a inventé à la main (isolation,
avec/sans, contexte de départ, verdicts par expectation), le runner le fait
nativement ; ce que G3 a de spécifique (tours conditionnels, variation du
payload global), le runner ne le fait pas.

### 2.2 Grille du brief, remplie

| Capacité | Maison (G3, et G2 quand différent) | `claude plugin eval` | Preuve runner |
|---|---|---|---|
| Test de déclenchement | G2 : proxy `run_eval.py` biaisé, protocole = conditions réelles (3/3) ; G3 : n/a (commands) | `tool_used: Skill` + `input_match`, `with-only` ; négatif via `min: 0, max: 0, arm: both` | pilote : `skill-fired` 1× / `skill-not-fired` 0× (§3.2) |
| Assertions sur la sortie | `expected_behavior` observables, grader Sonnet isolé ou inspection ; vérifs filesystem (`sha256`, `ls`, diff) scriptées | `regex`, `tool_used`, `tool_order`, `file_exists` gratuits ; `llm` (3 votes), `baseline` | pilote : 5 types utilisés, tous fonctionnels |
| Baseline / ablation | claude-md : payload avec/sans règle ; code-review : variantes A/B ; G2 : with/without | `--ablation with-without`, Δ par cas, `meanDelta` | cobaye Δ = 0,5 ; feynman Δ moyen 0,43 |
| Répétition, variance | code-review : 2 répétitions ; claude-md : 1/config ; G2 : 1 | `runs` défaut 3 (1-50), `--runs` | re-run candide 3 runs : 1 parfait, 2 gris (§3.2) |
| Contexte de départ | `setup-eval-cwd.sh` par corpus (fixtures, `git init`, config isolée) ; tours scriptés | `context.scaffold_script` (+ `--scaffold`), `add_dirs`, **`history_file`** (transcript repris) ; `append_system_prompt` | `history_file` testé : reprise OK, prompt = tour suivant |
| Multi-tours conditionnel | **oui** — `drive-session.py`, réponses conditionnelles (grill : 9 tours) | **non** — un seul tour user par cas ; `history_file` = transcript figé | doc `plugin-evals.md` §case.yaml ; `--help` |
| Variation du payload global | **oui** — `run-batch.sh` retire la règle du CLAUDE.md user-level | non nativement ; `append_system_prompt` est un substitut possible, **non vérifié** | doc §prompt.md frontmatter |
| Contrôle de coût | timeouts par run ; pas de plafond | `--max-cost-usd` (exit 2, `partial: true`), `costUsd` par run, `judgeCostUsd` | JSON de résultat |
| Rapport, exit code | tables manuelles dans les README ; scripts idempotents ; pas d'exit code | `aggregate-result.json` (`schemaVersion: 1`), `report.html` autonome, exit 0/1/2/130/143, `--threshold` | `exit=1` observé sous seuil 1.0 |
| Cible skill nue | oui (symlink ou config isolée) | manifest requis ; `<skill>/.claude-plugin/plugin.json` → `nom@skills-dir` ; ou plugin chemin | cobaye : résolu, skill nommée `nom:nom` |
| Cible command | oui (`claude -p "/cmd"`) | via `commands/` d'un plugin (« Skills as flat .md files ») — **non testé** | plugins-reference §layout |
| Isolation de l'environnement | `CLAUDE_CONFIG_DIR` (claude-md, code-review) ; config réelle pour immunize | **native** : `config/` vierge, `home/cwd` factice, skills perso et synced absentes | trace `init` : `skills` = builtins + plugin (§2.4) |
| Modèle | `--model` explicite ; effort via `--settings` | défaut = Opus 5 (`claude-opus-5[1m]` observé), **pas** le `model: Fable` des settings ; `--model` à pinner | trace `init.model` |
| Justification des juges | grader Sonnet : verdict + preuve verbatim | **votes seulement** (`judgeVotes`, `evidence` = réponse) ; ni le JSON ni `report.html` ne portent le raisonnement | `grep` du report : absent |
| Portabilité hors Claude Code | `claude -p` seulement | Claude Code seulement | — |
| Maturité, rupture | stable, maison | early access < 2.1.269 ; `schemaVersion` versionné ; écarts de doc (§7.2) | — |
| Maintenance | 1 driver + 4 setup + 2 batch scripts, à la charge du repo | portée par Anthropic | — |

### 2.3 Ce que le runner apporte (vérifié)

1. **Isolation native** — la trace `init` du bras « avec » ne liste que les
   builtins et `converting-temperatures:converting-temperatures` ; `plugins:
   [{source: converting-temperatures@inline}]` ; le bras « sans » : `plugins: []`,
   marqueur absent. G3 obtenait cela par `CLAUDE_CONFIG_DIR` monté à la main.
2. **Ablation propre** — le bras « sans » a donné 37,8 °C sans le marqueur : Δ
   mesure ce que la skill apporte, pas ce que le modèle sait.
3. **Répétition intégrée** — 3 runs par défaut ; la variance du `core_invariant`
   feynman (§3.2) n'est visible qu'avec.
4. **Graders déterministes gratuits** — `tool_used`, `regex`, `file_exists`
   couvrent les invariants « hors-transcription » que G1 vérifiait à la main
   (« aucun fichier écrit », « aucun outil web »).
5. **`history_file`** — répond au cas « skill déjà active » (§3.2, no-web-lookup).
6. **Coût, exit code, rapport** — 0,14 $ le cas en deux bras sur Opus ; 1,99 $
   la suite feynman ; `--threshold` + exit 1 = porte CI.
7. **Zéro script à maintenir** pour ce périmètre.

### 2.4 Ce que le runner ne fait pas (vérifié ou documenté)

1. **Interviews multi-tours conditionnelles** — un cas = un tour user. Les
   corpus grill (9 tours scriptés, réponses conditionnelles), prd, claude-md,
   planning, adr, immunize (composite 3 tours) ne sont pas portables tels quels.
   `history_file` fige l'historique ; il ne branche pas sur les questions de
   l'agent.
2. **Variation du payload global** — la variable du corpus claude-md est le
   CLAUDE.md user-level, pas un plugin. `append_system_prompt` pourrait
   l'approcher — à vérifier avant tout portage, pas dans cet audit.
3. **Raisonnement des juges absent** — `judgeVotes: [false, true, false]` et la
   réponse en `evidence`, rien d'autre. Le diagnostic d'un FAIL exige de relire
   la réponse (fait §3.2). Le grader Sonnet maison expliquait son verdict.
4. **Modèle par défaut = Opus**, pas Fable : toute campagne doit pinner
   `--model`, sinon on mesure un autre tier que le défaut de session (enjeu D5).
5. **Gating d'outils** — sans `--allow-tools`, WebFetch/WebSearch sont retirés :
   un invariant « n'appelle aucun outil web » devient trivial. Accordés
   (`--allow-tools WebFetch WebSearch`), ils testent la retenue du modèle — et le
   bras « sans » les a utilisés 3-4× (§3.2).
6. **Inventaire trompeur** — `claude plugin details converting-temperatures@skills-dir`
   rapporte « Skills (0) » pour un `SKILL.md` à la racine, que le runner charge
   pourtant. Le layout canonique `skills/<nom>/SKILL.md` est compté.

### 2.5 Verdict Q1 — hybride v2, corpus par corpus

| Corpus | Aujourd'hui | Cible | Raison |
|---|---|---|---|
| feynman-mentor (6) | G2, 1 run (07-23) | **runner** | pilote : 6/6 invariants exprimés, 3 runs, `history_file` ; G2 n'apporte plus rien |
| code-review (A/B × tiers) | G3 mono-tour | **runner** (à la prochaine campagne — déclencheur D5) | mono-tour, fixture par `scaffold_script`, variantes = deux dossiers de plugin ou `--tag` ; non testé |
| claude-md batch A (avec/sans règle) | G3 | **G3** | variable = payload global ; substitut `append_system_prompt` non vérifié |
| grill, prd, planning, adr, immunize | G1/G3 | **G3** pour les interviews ; runner pour les sous-ensembles mono-tour (preflight, strict-mode gate, résolution d'entrée) au fil des retouches | limite structurelle (§2.4.1) |

Doctrine inchangée (ADR-0009) : classes comportementales, fixtures à tension
délibérée, étoffage par nécessité observée, invariants observables — le moteur
est un détail d'exécution. Ce qui change : G2 disparaît, le runner prend la
place de G3 partout où un cas tient en un tour, et les README de corpus
documentent deux moteurs au lieu de trois.

## 3. Pilotes

### 3.1 Cobaye `converting-temperatures` — le mécanisme

Montage (hors repo) : `~/.claude/skills/converting-temperatures/.claude-plugin/plugin.json`
= `{"name": "converting-temperatures"}` ; un cas `evals/trigger-basic/prompt.md`
(`allowed_tools: [Skill]`, prompt organique « Il fait 100 °F à Phoenix
aujourd'hui, ça fait combien en Celsius ? ») ; trois graders : `tool_used: Skill`
(`input_match: '"skill"\s*:\s*"(?:[\w-]+:)?converting-temperatures"'`), `regex`
`37[.,][78]` (valeur), `regex` `converting-temperatures ACTIVE` (marqueur du corps
de la skill). Commande, depuis un répertoire vide :

```
claude plugin eval converting-temperatures@skills-dir --runs 1 --ablation with-without \
  --max-cost-usd 1 --no-publish --keep-temp --json <out>.json
```

| Bras | Skill appelée | Marqueur | Valeur | Score | Coût | Tours |
|---|---|---|---|---|---|---|
| avec | 1× (`converting-temperatures:converting-temperatures`) | oui | oui | 1,0 | 0,074 $ | 3 |
| sans | — | non | oui | 0,5 | 0,064 $ | 1 |

Δ = 0,5 ; `tool_used: Skill` reporté `scored: false` (indicateur with-only),
conforme à la doc. Le nom de commande dans la session enfant :
`converting-temperatures:converting-temperatures` (forme `plugin:skill`).
`plugin details` : « Skills (0) », `~0 tok` always-on — inventaire faux pour un
`SKILL.md` racine (§2.4.6). Trace `init` : `permissionMode: dontAsk`, outils =
set read-only, écritures scellées (`sealed/`, mode 000).

### 3.2 Pilote feynman-mentor — la portabilité d'un corpus maison

Montage (scratchpad, cible chemin, `--trust-plugin`) : `fm-plugin/.claude-plugin/plugin.json`
= `{"name": "feynman-mentor"}` ; `fm-plugin/skills/feynman-mentor/` = copie de
`claude/skills/feynman-mentor/` sans `evals/` (layout canonique) ; six
`fm-plugin/evals/<id>/case.yaml` traduisant `feynman-mentor.eval.json` :

| Cas maison (classe) | Traduction runner |
|---|---|
| `candide-never-fills-gaps` (core_invariant) | `tool_used: Skill` (indicateur) ; `regex not_contains` louanges ; 2 juges `llm` (jargon signalé sans définir ; trois volets, pas de reformulation) |
| `candide-refuses-meta-help` (core_invariant) | idem + `regex not_contains` marqueurs d'hypothèse d'intention ; 2 juges `llm` |
| `no-web-lookup` (no_side_effect) | `allowed_tools: [Skill, Read, WebFetch, WebSearch]` + `--allow-tools WebFetch WebSearch` ; `tool_used` WebFetch/WebSearch `min: 0, max: 0, arm: both` ; `file_exists "**/*" exists: false` ; juge `llm` (décline, ne corrige pas) |
| `discovery-french-trigger` (discovery +) | `tool_used: Skill` ; juge `llm` (setup candide, n'enseigne pas) |
| `no-collision-teach-territory` (discovery −) | `tool_used: Skill min: 0, max: 0, arm: both` ; juge `llm` (enseigne ou route, aucun persona candide) |
| `session-end-learning-record` (state_bridge) | `tool_used: Skill` ; `file_exists` absent ; `regex` `Source\s*:\s*feynman-mentor session` ; juge `llm` (bloc copiable + invite finale) |

Commande : `claude plugin eval fm-plugin --trust-plugin --runs 1 --ablation
with-without --judge-model sonnet -j 2 --max-cost-usd 5 --no-publish --keep-temp
--allow-tools WebFetch WebSearch --json …`. Résultat : 4/6 cas au seuil 1.0,
score global 0,81, Δ moyen 0,43, 1,99 $, 3 min 45, `exit=1`.

| Cas | avec | sans | Δ | Lecture |
|---|---|---|---|---|
| candide-never-fills-gaps | 0,33 | 0,33 | 0 | skill tirée ; 2 juges FAIL → diagnostic ci-dessous |
| candide-refuses-meta-help | 1,0 | 0,33 | +0,67 | invariant tenu ; le bras « sans » reformule |
| no-web-lookup | 0,5 | 0,25 | +0,25 | **skill non tirée** ; WebFetch 3×, le modèle corrige l'utilisateur → diagnostic |
| discovery-french-trigger | 1,0 | 0 | +1,0 | déclenchement 1/1 sur phrasé naturel, setup candide |
| no-collision-teach-territory | 1,0 | 1,0 | 0 | skill non tirée sur « apprends-moi », enseignement dans les deux bras |
| session-end-learning-record | 1,0 | 0,33 | +0,67 | bloc copiable, ligne `Source:`, zéro fichier ; le bras « sans » ne propose rien |

**Diagnostic 1 — `candide-never-fills-gaps`.** Réponse réelle du bras « avec » :
trois titres français, jargon signalé (`stateless`, `state`, `APIs REST`,
`PUT`), `basiquement` et le saut logique questionnés, aucune louange, invitation
finale. Les juges ont échoué sur mes rubriques : le SKILL.md *prescrit* de
restituer « ce qui a été compris » (une reformulation par construction) et ma
clause « FAIL on any reformulation » la sanctionnait. Défaut de calibrage de
rubrique, pas régression de la skill. Rubriques recalibrées (la restitution du
volet « compris » est requise ; une question qui contient la lecture naïve du
candide est une question) + `regex not_contains` des marqueurs d'hypothèse ;
re-run en **3 runs, un bras** :

| Run | Verdict | Cause |
|---|---|---|
| 0 | FAIL (juges 3/3 sur `flags-jargon`) | « converger, pour moi, ça veut dire s'approcher progressivement… » et « vous dites *sans* state, puis un state final » — le candide décode `stateless` et énonce un sens : **fuite d'aide** réelle, celle que le README maison demande au juge de traquer |
| 1 | FAIL (`regex`) | « Est-ce que tu veux dire que chaque répétition rapproche… ? ou que c'est identique dès la première fois ? » — forme interrogative attrapée par `tu veux dire que` : le regex est trop large pour un invariant sémantique |
| 2 | PASS 5/5 | — |

Score 0,87, 1 run parfait sur 3. Le run unique de juillet (1.00) masquait cette
variance ; elle révèle une zone grise du **contrat** de la skill (le candide
peut-il proposer une lecture naïve en forme de question ?) que ni le SKILL.md ni
les `expected_behavior` ne tranchent.

**Diagnostic 2 — `no-web-lookup`.** Le corpus maison présuppose la skill
*déjà active* (elle tournait pré-chargée sous G2). Sur phrasé naturel, « tu peux
vérifier sur la doc que c'est correct ? » est une demande d'exactitude, pas de
clarté : le non-déclenchement est conforme à la description. Traduction fidèle :
`context.history_file` = transcript de session du run `discovery-french-trigger`
(`config/projects/…/<session>.jsonl` du répertoire `--keep-temp`), le prompt
devenant le tour suivant. Re-run : **tous les graders scorés PASS** — décline
(« non, je ne peux pas et je ne dois pas… mon rôle n'est pas de dire si c'est
exact mais si c'est compréhensible »), WebFetch 0×, WebSearch 0×, zéro fichier,
juges 3/3 ; signale même le changement de sujet (window functions → CTE). Seul
l'indicateur `skill-fired` échoue — la skill a été invoquée dans l'historique,
pas dans le run — et sous `--ablation none` il est compté : score 0,8, `exit=1`.

### 3.3 Leçons de design de cas (à verser au README du corpus migré)

1. **Discovery et comportement post-invocation sont deux cas distincts.** Un
   prompt organique teste le déclenchement ; un invariant « skill active » se
   teste en `history_file`. Le corpus maison les confondait pour les skills
   (README : « discovery testable » — mais les autres classes supposaient
   l'invocation sans le dire).
2. **Pas d'indicateur `tool_used: Skill` sur un cas en transcript repris**, ni
   sous `--ablation none` (il y est scoré).
3. **Les rubriques `llm` se calibrent sur le SKILL.md, pas sur l'idéal** : ce
   que la skill prescrit (restituer le compris) ne peut pas être un FAIL.
4. **Un `regex` sur un invariant sémantique est un piège de précision** :
   réservé aux marqueurs sans ambiguïté (louanges, ligne `Source:`), jamais aux
   formulations (« tu veux dire que » est aussi une question).
5. **Un run cache la variance** : `runs: 3` minimum sur les classes
   `core_invariant` ; le seuil 1.0 par défaut rend un cas rouge sur un run gris,
   ce qui est la bonne alerte — puis lire la réponse, le JSON ne dit pas
   pourquoi.
6. **Accorder les outils que l'invariant interdit** (`--allow-tools`), sinon
   l'invariant est trivial.
7. **Pinner `--model`** (Fable et Opus, tiers frontière) ; le défaut est Opus.

## 4. Q2 — Frontmatter : inventaire, seuil, champs

### 4.1 Inventaire des 15 artefacts

Extraction : `awk` du bloc `---` de chaque fichier ; longueur de description
mesurée en caractères après repli des espaces ; datation `git log -1 -- <f>` ;
coût de listing et usage : `claude -p "/skill-doctor"` (2026-09-22).

| Artefact | Champs | Desc. (car.) | `model` | Dernier commit | Listing (tok/tour) | Usages · dernier |
|---|---|---|---|---|---|---|
| skills/coach-pedagogique | name, description, dmi:false | 402 | — | `6e9d8a6` 06-23 | ~140 | 3× · 160 j |
| skills/code-mentor | name, description, dmi:false | 428 | — | `890a1cc` 08-07 | ~140 | 3× · 180 j |
| skills/code-review | name, description, dmi:**true**, allowed-tools, **effort: high** | 273 | — | `e52643d` 08-07 | ~280 (*) | 13× · 12 j |
| skills/dp-coach | name, description, dmi:false | 309 | — | `1269d1c` 09-02 | ~100 | 3× · 41 j |
| skills/feynman-mentor | name, description, dmi:false, allowed-tools: Read | 741 | — | `c787ee0` 07-23 | ~250 | 1× · 54 j |
| skills/teach | name, description, dmi:**true**, argument-hint | 61 | — | `1269d1c` 09-02 | – (caché) | 42× · aujourd'hui |
| commands/adr | description, argument-hint, allowed-tools, model | 184 | opus | `fce314a` 06-22 | ~60 | 5× · 55 j |
| commands/catchup | description, allowed-tools, model | 69 | haiku | `a16acec` 03-09 | ~30 | 51× · aujourd'hui |
| commands/claude-md | description, argument-hint, allowed-tools, model | 149 | sonnet | `c8bbb0b` 07-29 | ~50 (+80 fantômes) | 15× · 55 j |
| commands/grill | description, argument-hint, allowed-tools, model | 217 | opus | `78a7e95` 07-29 | ~80 | 6× · 55 j |
| commands/immunize | description, argument-hint, allowed-tools, model | 164 | sonnet | `d117bf5` 07-30 | ~60 | 12× · 12 j |
| commands/planning | description, argument-hint, allowed-tools, model | 127 | opus | `eec3141` 07-27 | ~50 | 1× · 83 j |
| commands/prd | description, argument-hint, allowed-tools, model | 85 | opus | `72b6766` 07-28 | ~30 | 14× · 55 j |
| commands/progress | description, allowed-tools, model | 74 | sonnet | `bbd9333` 07-28 | ~30 | 65× · 3 j |
| commands/tech-watch | description, allowed-tools | 77 | — | `721b839` 04-20 | ~30 | 5× · 198 j |

`dmi` = `disable-model-invocation`. (*) La skill maison `code-review` est
cachée (`dmi: true`, comme `teach` qui affiche « – ») ; les ~280 tokens listés
sous ce nom sont l'entrée du **builtin** homonyme. Sonde `claude -p "/code-review"`
(Haiku, mini-repo à diff d'une ligne) : la sortie porte le ledger maison
(`HIGH · correction · report.py:4`), la frontière hooks et « première passe,
revue humaine due » → **`/code-review` tapé exécute la surcharge, ADR-0010
tient** (doc : « Your skill replaces the bundled command, but not its aliases »).
Angle mort non documenté : l'entrée de listing vue par Claude reste celle du
builtin.

**Commands fantômes** : `~/.claude/commands/claude-md/reference/*.md` (symlink
`install.sh` l. 47-49, workaround pour les fichiers de support) sont exposés
comme commands `claude-md:reference:output-format` (0×, jamais),
`claude-md:reference:validation-checklist` (0×, jamais),
`claude-md:reference:instance-aware-flow` (3×). ~80 tokens par tour, deux
entrées « never invoked » signalées par `/skill-doctor`.

Listing total des artefacts maison ≈ **1 400 tokens par tour** (dont 280 de
builtin sous le nom `code-review`). Ordre de grandeur modeste ; le levier n'est
pas là.

### 4.2 Conformité spec (agentskills.io) et Claude Code

| Critère | Résultat | Preuve |
|---|---|---|
| `name` = dossier | 6/6 skills | inventaire |
| `description` ≤ 1 024 car., non vide | 15/15 (max 741, feynman-mentor) | inventaire |
| `description` + `when_to_use` ≤ 1 536 car. (listing Claude Code) | 15/15, `when_to_use` inutilisé | skills.md §frontmatter |
| Pas de balise XML | 15/15 | `grep '<[a-zA-Z]'` |
| 3ᵉ personne | 14/15 — `teach` : « Teach the user… » (impératif) | inventaire ; sans effet : `dmi: true`, description hors routage |
| Frontmatter en ligne 1 | 15/15 | `awk` |

Aucune violation. Une **erreur factuelle de corps** connue (brief §1.3),
confirmée : `feynman-mentor/SKILL.md` l. « Tool discipline: you have no web
access by design (frontmatter restriction) » — `allowed-tools: Read` est une
pré-approbation (« Tools Claude can use without asking permission during the turn
that invokes this skill »), pas une restriction. Le pilote le montre : WebFetch
accordé, le candide a décliné **par la prose** (§3.2) ; le frontmatter ne fait
rien.

### 4.3 Les 11 champs nouveaux, un par un

Seuil du brief : chantier seulement si (a) violation de spec, (b) le champ
change un comportement observable, (c) le champ résout une douleur documentée.

| Champ | Douleur documentée en face ? | Verdict |
|---|---|---|
| **`disallowed-tools`** | oui — classes `no_side_effect` : feynman (aucun outil web, aucun fichier), grill (« n'écrit aucun fichier »), code-review (« signale uniquement ») sont de la prose vérifiée par eval | **retenu**, avec réserve : « The restriction clears when you send your next message » (skills.md) — pour une skill conversationnelle multi-tours, la garde ne couvre que le tour d'invocation. Complète la prose et l'eval ; ne les remplace pas. (b) partiel, (c) oui. |
| `when_to_use` | non — les descriptions portent déjà triggers et exclusions ; cap 1 536 non atteint ; sous-déclenchement non observé (discovery 1/1 au pilote, 3/3 en juillet) | écarté |
| `effort` | non — déjà utilisé par code-review ; les commands pinnées `opus` héritent l'effort de session (`xhigh`) ; G3 fixait `high` par `--settings` pour les evals, pas pour l'usage | écarté (option cosmétique) |
| `context: fork` + `agent` + `background` | non — tech-watch délègue déjà via `Agent` à `tech-watch-scorer` ; aucune douleur de contexte consignée | écarté |
| `paths` | non — aucune skill liée à un type de fichier (`/code-review` dbt/Terraform est un déclencheur dormant, pas une douleur) | écarté |
| `hooks` | non — la garde anti-écriture-globale d'immunize vit dans le harnais d'eval, pas en production ; douleur non documentée | écarté (à ressortir si une leçon d'artefact le réclame) |
| `arguments` | non — `$ARGUMENTS` suffit aux 7 commands à argument | écarté (cosmétique) |
| `shell` | n/a (bash) | écarté |
| `metadata`, `license`, `compatibility` | portabilité claude.ai/API uniquement ; aucune skill maison n'est packagée hors Claude Code | écarté |

Champ **existant** mal utilisé : `disable-model-invocation: false` explicite
sur 4 skills = valeur par défaut, bruit — nettoyage opportuniste. Aucune des 9
commands ne pose `dmi: true` : toutes sont auto-invocables par Claude. Le brief
ne signale pas de douleur ; la doctrine dit pourtant « human-triggered » pour
/progress, /immunize, /code-review (CLAUDE.md global) et « délégation par
instruction, jamais par invocation » (ADR-0003). Option à trancher hors audit,
pas un chantier : poser `dmi: true` sur les commands rituelles encoderait cette
doctrine et retirerait ~400 tokens de listing, au prix de descriptions absentes
du contexte (la connaissance survit via CLAUDE.md et la matrice).

### 4.4 Migration commands → skills : ce qu'elle apporte réellement

Doc : « Command files … support the same frontmatter except `name` and `paths` …
Prefer a skill for new work, since skills also support supporting files. »

| Gain | Réel pour ce repo ? |
|---|---|
| Fichiers de support natifs | **oui pour claude-md** : supprime le workaround `install.sh` l. 47-49 et les 2 commands fantômes jamais invoquées (§4.1) ; non pour les 8 autres (fichier unique) |
| Evals dans le dossier de l'artefact | oui — précédent feynman ; aujourd'hui `claude/commands/<cmd>/evals/` existe déjà à côté du `.md` (structure hybride) |
| Ciblage par le runner | **non requis** — un plugin charge aussi `commands/` (« Skills as flat .md files ») ; non testé |
| `name`, `paths` | sans objet |
| Coût | 9 fichiers à déplacer, `install.sh` (9 symlinks fichier → 9 symlinks dossier), renvois dans matrice/README/overview, evals à rejouer (G3 inchangé) |

Verdict : migrer **`claude-md` maintenant** (douleur documentée), les autres
**au fil des retouches** — c'est précisément le déclencheur armé R2+P3 de la
roadmap (blocs `## Test` + `skip:<raison>` « à la prochaine command créée ou
refondue ») : une migration en bloc le ferait tirer neuf fois d'un coup, contre
Surgical Changes.

### 4.5 Verdict Q2

Pas de chantier frontmatter autonome. Retouches, toutes absorbées par le
chantier Q1 ou opportunistes : `disallowed-tools` sur feynman-mentor, grill,
code-review (avec un cas runner qui le prouve, test-first) ; correction du corps
de feynman-mentor ; `claude-md` en skill ; suppression des `dmi: false`
redondants ; `teach` à la 3ᵉ personne si on y touche.

## 5. Q3 — Routage des conclusions (matrice de responsabilité)

Règle appliquée : « Architecture décisionnelle → ADR ; phases → PLAN (produit)
ou brief `tasks/` (précédents : `diagnosing-bugs-trial.md`,
`code-review-fable-eval-2026-08.md`) ; règles durables → CLAUDE.md ; leçons →
inbox ». Test décisif : « si je modifie ce contenu, quel autre document dois-je
toucher ? »

| Conclusion | Destination | Pourquoi là et pas ailleurs |
|---|---|---|
| Hybride v2 : runner pour skills et mono-tour, G3 pour interviews et payload ; G2 retiré ; règles de design de cas (§3.3) | **ADR-0016, Extends ADR-0009** (`/adr --from-context`) | décision durable qui change la façon de tester ; ADR-0009 reste vrai sur la doctrine, faux sur le moteur — Extends, pas Supersedes. ADR-0015 inchangé (immunize reste G3) |
| Chantier phasé (§6) | **ce fichier, §6** — pas de PLAN.md (dotfiles n'a ni PRD ni PLAN ; les campagnes vivent en brief `tasks/`) ; suivi dans `progress.md` | précédent des deux briefs cités ; un PLAN pour un repo de config violerait la matrice (PLAN = architecture produit) |
| Doctrine d'evals (classes, fixtures, étoffage) | **inchangée** (ADR-0009 §Décision) | rien à écrire |
| « Garde-fou = rituel d'evals » | **CLAUDE.md projet inchangé** ; `claude/CLAUDE.md` global inchangé | le moteur n'y figure pas |
| Section « Cycle immunitaire » (fixtures `claude/evals/claude-md/`) | **matrice inchangée** | corpus claude-md reste G3 |
| Deux moteurs au lieu de trois | README des corpus migrés + `claude/evals/README` s'il naît ; `claude/README.md` (catégorie « à réinstaller » : plugins) | source de vérité de l'exécution = README de corpus (ADR-0009) |
| 3 leçons : rubrique calibrée sur le SKILL.md ; discovery ≠ skill active ; run unique masque la variance | **`tasks/lessons-inbox.md`** via `/immunize "<leçon>"` — pas d'écriture directe | circuit normal ; toutes incriminent un artefact versionné (README de corpus) → routage artefact au triage |
| Angles morts de doc (§7.2) | annexe de ce fichier ; `RESOURCES.md` du workspace d'apprentissage | faits, pas décisions |
| Verdict pour la mission d'apprentissage | learning record `0004-*.md` du workspace `~/learning-to-build-skills` (Greg copie, flux unidirectionnel ADR-0008) | source unique de la progression = workspace teach |
| Pièces du pilote (6 `case.yaml`, 5 JSON) | `tasks/skill-evals-audit-2026-09/pilot/` — **à l'arbitrage de Greg** ; scratchpad éphémère sinon | précédent ADR-0009 : corpus pilote figé sous `grill/evals/pilot-skill-creator/` |

Interactions avec la roadmap d'adoption (`~/claude-audit-notes/adoption-roadmap.md`) :
- **A3 blinding** — satisfait nativement par le runner (CWD `/tmp/claude-eval-XXXXXX/home/cwd`, nom neutre) ; reste à faire pour G3 (`/tmp/grill-eval-*`).
- **R2+P3** — tire à la migration `claude-md` (première command refondue).
- **D5** (rejeu au changement de tier) — boucle `--model` sur le runner pour feynman/code-review ; G3 pour claude-md.
- **T4** (test-first des prompts) — renforcé : porte CI possible (`--threshold`, exit 1).

## 6. Recommandations, phasées

Ordre : décision, puis packaging vérifié, puis migration d'un corpus, puis
event-driven. Aucune écriture dans une skill ou une command avant R1 validé.

### Phase 0 — Décision (une session courte)

- **R1. ADR-0016, Extends ADR-0009** (`/adr --from-context` sur ce fichier) :
  moteur runner pour skills et cas mono-tour ; G3 conservé pour interviews et
  payload global ; G2 retiré ; règles de design de cas (§3.3) ; `--model` pinné
  sur les tiers frontière ; `runs: 3` sur `core_invariant`. ADR-0015 inchangé.
- **R2. Arbitrages de Greg** : (a) figer les pièces du pilote sous
  `tasks/skill-evals-audit-2026-09/pilot/` ; (b) option `dmi: true` sur les
  commands rituelles (§4.3) — hors chantier, à instruire séparément si retenue.

### Phase 1 — Packaging d'eval (½ session, ~0,5 $)

- **R3. Choisir l'unité « plugin » et la vérifier sur pièce.** Deux options :
  - **(a) `claude/` = un plugin, cible chemin** (recommandée) : manifest
    `claude/.claude-plugin/plugin.json`, eval dir `claude/evals/` (déjà là ; le
    runner ignore les sous-dossiers G3 sans `case.yaml`), commande
    `claude plugin eval ~/dotfiles/claude --trust-plugin …`. Couvre skills **et**
    commands (`commands/` = « Skills as flat .md files ») ; aucun effet sur les
    sessions quotidiennes (`claude/` n'est pas sous un skills dir ; les symlinks
    restent le mécanisme runtime). Skills nommées `<plugin>:<skill>` dans
    l'enfant — l'`input_match` du doc les couvre. **À vérifier** avant adoption
    (un run à 0,14 $ + `claude plugin details`) : `claude/settings.json` et
    `claude/hooks/` à la racine du plugin sont-ils interprétés comme composants
    (le layout plugin prévoit `settings.json` et `hooks/hooks.json`) ;
    `agents/tech-watch-scorer` chargé ; `CLAUDE.md` ignoré (« not loaded as
    project context »). Ajouter `claude/evals/results/` au `.gitignore`.
  - **(b) manifest par skill** (`nom@skills-dir`, testé sur le cobaye) : plus
    simple, mais la double identité en session quotidienne (skill nue + plugin
    `nom:nom`) n'est **pas vérifiée**, et les commands restent hors cible.
  - Repli si (a) échoue sur les effets de bord : plugin assemblé par script dans
    un répertoire temporaire (approche du pilote), cible chemin.

### Phase 2 — Migration feynman-mentor (1 session, 2-4 $)

- **R4. Porter le corpus** : 6 `case.yaml` (§3.2) dans l'eval dir retenu, leçons
  §3.3 appliquées (`history_file` régénéré depuis un run du plugin du repo —
  les chemins diffèrent ; `runs: 3` sur les deux `candide-*` ; pas d'indicateur
  `skill-fired` sur le cas repris). Retirer les fichiers G2 (`evals.json`,
  `feynman-mentor.eval.json`, `setup-eval-cwd.sh`), réécrire le README (moteur,
  commande, table d'état) ; campagne `--model` Fable **et** Opus ; verdicts au
  README.
- **R5. `disallowed-tools: WebFetch, WebSearch, Write, Edit`** sur feynman-mentor
  + réécriture du paragraphe « Tool discipline » (§4.2). Le cas `no-web-lookup`
  reste la garde du tour N (la prose fait le travail au-delà du tour 1).
- **R6. Trancher la zone grise du contrat** révélée par les 3 runs (§3.2) : le
  candide peut-il proposer une lecture naïve en forme de question ? Oui → la
  rubrique l'autorise explicitement ; non → une ligne dans les anti-patterns du
  SKILL.md et la rubrique le sanctionne. Décision de Greg, puis rejeu.

### Phase 3 — `claude-md` en skill (1 session)

- **R7.** `claude/skills/claude-md/{SKILL.md, reference/, evals/}` ; `install.sh`
  : un symlink de dossier remplace le symlink fichier + le workaround
  `reference/` ; suppression de `~/.claude/commands/claude-md*` ; renvois
  (matrice, overview, README). Corpus G3 rejoué (interview). Déclencheur R2+P3
  honoré : blocs `## Test` + `skip:<raison>` sur cette command et elle seule.

### Phase 4 — Event-driven

- **R8. Corpus code-review → runner à la prochaine campagne** (déclencheur D5) :
  fixture `usage-report` par `scaffold_script` (+ `--scaffold`, `--allow-tools
  Bash`), variantes A/B = deux dossiers de plugin ou deux tags, graders `regex`
  sur les identifiants D1-D4 / T5-T8 du ledger, `file_exists`/diff pour
  l'invariant no-edit, `--model` par tier.
- **R9. Sous-ensembles mono-tour des corpus d'interview** (preflight grill,
  strict-mode gates prd/planning, numérotation adr) → runner quand la command
  est retouchée ; le reste demeure G3.
- **R10. `disallowed-tools: Write, Edit, NotebookEdit`** sur grill (n'écrit
  jamais) et **`Write, Edit`** sur code-review (signale uniquement) —
  opportuniste, avec la même réserve de portée (tour d'invocation).

### Hygiène et transmission

- **R11.** Supprimer les 4 `disable-model-invocation: false` redondants ; `teach`
  à la 3ᵉ personne si retouché ; `.ruff_cache/` égarés dans `grill/evals/` et
  `prd/evals/` (sans effet git — ils portent leur propre `.gitignore`).
- **R12.** `claude/README.md` : noter `syncClaudeAiSkills: false` et le chemin
  de réinstallation des skills Anthropic utiles (`anthropics/skills` : pdf,
  docx, xlsx, pptx, skill-creator, mcp-builder) dans la catégorie « à
  réinstaller ».
- **R13.** Trois leçons dans l'inbox via `/immunize "<leçon>"` (§5).
- **R14.** Learning record `0004-*.md` dans `~/learning-to-build-skills` à partir
  du §0 (à la main de Greg).
- **R15.** Purge du cobaye : `~/.claude/skills/converting-temperatures/{.claude-plugin,evals}`
  et les résultats du scratchpad (hook `block-rm-rf` : à la main).
- **R16.** Retour au canal `stable` quand stable ≥ **2.1.273** (le seuil de la
  sync, plus haut que celui du runner 2.1.269) ; `syncClaudeAiSkills` reste.

## 7. Annexes

### 7.1 Commandes reproductibles

```
claude --version                                     # 2.1.278
claude plugin eval --help                            # options vérifiées
claude plugin details converting-temperatures@skills-dir
claude plugin eval converting-temperatures@skills-dir --runs 1 --ablation with-without \
  --max-cost-usd 1 --no-publish --keep-temp --json out.json
claude plugin eval <fm-plugin> --trust-plugin --runs 1 --ablation with-without \
  --judge-model sonnet -j 2 --max-cost-usd 5 --no-publish --keep-temp \
  --allow-tools WebFetch WebSearch --json out.json
claude plugin eval <fm-plugin> --trust-plugin --case candide-never-fills-gaps --runs 3 --ablation none …
claude plugin eval <fm-plugin> --trust-plugin --case no-web-lookup --runs 1 --ablation none …
claude -p "/skill-doctor" --output-format text
claude -p "/code-review" --model haiku --max-turns 8 --output-format text   # dans un mini-repo à diff
for f in claude/skills/*/SKILL.md claude/commands/*.md; do awk 'NR==1{next} /^---$/{exit} {print}' "$f"; done
```

Les traces d'un run `--keep-temp` vivent dans `/tmp/claude-eval-XXXXXX/`
(`out/trace.jsonl` = stream-json avec l'événement `init` ; `config/` = config
isolée ; `config/projects/…/<session>.jsonl` = transcript repris par
`history_file` ; `sealed/` = écritures du plugin, mode 000). Sans `--keep-temp`,
tout est purgé à la fin du run.

### 7.2 Écarts et angles morts de documentation (à reporter dans `RESOURCES.md`)

1. `skills.md` documente `claude plugin eval … --test-config <json>` et
   `/evals --init` ; ni `plugin-evals.md` ni `--help` (2.1.278) ne les
   connaissent (brief).
2. `assertions` vs `expectations` selon agentskills.io / skill-creator
   SKILL.md / `references/schemas.md` (brief).
3. `skills.md` lie skill-creator à `anthropics/claude-plugins-official`, pas
   `anthropics/skills` (brief).
4. **Nouveau** — `claude plugin details <nom>@skills-dir` rapporte « Skills (0) »
   pour un `SKILL.md` à la racine du dossier ; le runner le charge pourtant sous
   `nom:nom`.
5. **Nouveau** — une skill personnelle homonyme d'un builtin, cachée par
   `disable-model-invocation: true`, remplace bien la commande tapée (doc) mais
   l'entrée de listing vue par Claude reste celle du builtin (`/skill-doctor`
   ~280 tok sous `code-review`). Non documenté.
6. **Nouveau** — le résultat (`aggregate-result.json`, `--json`, `report.html`)
   ne contient pas le raisonnement des juges `llm` : `judgeVotes` + `evidence`
   (la réponse) seulement.
7. **Nouveau** — `plugins-reference.md` mentionne `claude plugin validate` ;
   absent de `claude plugin --help` en 2.1.278.
8. **Nouveau** — le champ racine `ablation` du JSON est vide ; la valeur est
   dans `suite.ablation`.
9. **Nouveau** — la sync claude.ai (≥ 2.1.273) n'est pas mentionnée dans les
   prérequis du runner ; sans effet sur lui (isolation), avec effet sur toute
   sonde en conditions réelles.
10. **Phase 1 (2026-09-22)** — le loader `commands/` d'un plugin est
    **récursif**, chaque `.md` devenant une command nommée par son chemin
    (`dotfiles:grill:evals:fixtures:…`) ; `plugins.md` ne parle que de « flat
    Markdown files ». Le champ `commands` du manifest remplace ce scan (doc
    conforme, vérifié) — c'est la parade retenue (`claude/.claude-plugin/plugin.json`).
11. **Phase 1 (2026-09-22)** — `claude plugin details` ne prend ni chemin ni
    option `--plugin-dir` propre ; le flag est global :
    `claude --plugin-dir <dir> plugin details <nom>`. Le message d'erreur le
    suggère sans préciser la position. L'inventaire ne compte pas les commands.

### 7.3 Artefacts du pilote (scratchpad de session, éphémères)

`fm-plugin/` (manifest, `skills/feynman-mentor/`, 6 `evals/*/case.yaml`,
`evals/no-web-lookup/history.jsonl`, `evals/results/<3 timestamps>/`) ;
`fm-result.json`, `fm-rerun-candide.json`, `fm-rerun-web.json` ;
`cobaye-result.json`, `cobaye-result-2.json`, `cobaye-cwd/evals/results/` ;
`cr-probe/` (mini-repo de la sonde code-review), `cr-probe-out.txt`. Figés dans
le repo seulement sur arbitrage R2(a).
