# ADR-0009 : Rituel d'evals maison (A→B→A) vs Skill Creator officiel d'Anthropic

Status: Accepted
Date: 2026-06-23

## Contexte

Le repo dispose d'un **rituel d'evals maison** pour mesurer le comportement
post-invocation des slash-commands / skills (corpus sous `claude/commands/*/evals/`,
protocole A→B→A). Il est le garde-fou qualité déclaré du repo (cf.
[`CLAUDE.md`](../CLAUDE.md) : « le garde-fou contre les changements risqués est le
rituel d'evals »).

Un contrôle web (2026-06-23) a établi qu'Anthropic a publié, le **3 mars 2026**, un
**Skill Creator officiel** — plugin Claude Code
(`anthropics/claude-plugins-official`), `/plugin install
skill-creator@claude-plugins-official`. Il outille un cycle Create / Eval / Improve
/ Benchmark via 4 sous-agents (Executor, Grader, Comparator, Analyzer), avec evals
versionnés en `evals/evals.json` et un eval-viewer HTML.

**Constat dirimant : la convergence est déjà structurelle, pas théorique.**

Le format maison de `grill.eval.json` —
`{id, class, query, files, expected_behavior}` — est un quasi-isomorphe du format
officiel `evals/evals.json` — `{id, prompt, expected_output, files, assertions}`.
Le README maison cite déjà explicitement l'« Evaluation-Driven Development
(Anthropic) » comme source. Autrement dit : le rituel maison a reconstruit à la
main, par anticipation, presque exactement la structure qu'Anthropic vient
d'outiller et d'automatiser.

Les différences réelles, vérifiées :

| Axe | Rituel maison A→B→A | Skill Creator officiel |
|---|---|---|
| Exécution | manuelle — l'**humain est canal de transmission** (copie-colle les transcriptions B→A) | **automatisée** — sous-agents parallèles, zéro copier-coller |
| Format evals | JSON maison `{class, expected_behavior}` (observables, pas sortie exacte) | JSON officiel `{expected_output, assertions}` |
| Isolation | CWD `/tmp` éphémère + session B vierge (`setup-eval-cwd.sh`) | workspace `iteration-<N>/eval-<ID>/[with_skill|without_skill]` |
| A/B | implicite (re-run après édition) | **Comparator** : A/B aveugle entre versions |
| Métriques | qualitatif / comportemental coché ✅⚠️❌ | **+ quantitatif** : pass rate, temps, tokens |
| Baseline sans-skill | non outillée | with_skill **vs** without_skill systématique |
| Dépendance | aucune (git, bash, sessions Claude Code) | plugin `claude-plugins-official` |
| Cible | commands ET skills | skills (transposable aux commands) |

Friction connue du rituel maison (de son propre README) : « le grill est interactif
et long », l'humain doit conduire chaque session B jusqu'au bout et copier-coller
l'intégralité de la transcription. C'est précisément ce coût manuel que
l'automatisation du Skill Creator supprime. À ce jour, le corpus `/grill` est
**écrit mais jamais exécuté en A→B→A** — signe que le coût manuel est un frein réel.

## Options considérées

- **Option A — Adopter le Skill Creator, migrer les corpus** : installer le plugin,
  convertir les `*.eval.json` maison au format `evals/evals.json`, exécuter via les
  sous-agents.
  - Avantage : supprime le coût manuel (le vrai frein — corpus non exécutés) ;
    baseline with/without-skill et A/B aveugle gratuits ; métriques quantitatives ;
    aligné sur l'outillage officiel maintenu par Anthropic. Les sous-agents sont
    exactement les rôles A→B→A que le rituel exécute à la main.
  - Inconvénient : dépendance à un plugin externe (vs zéro-dépendance actuel) ;
    `expected_output` exact-ish vs `expected_behavior` observable — possible perte
    d'expressivité sur les invariants comportementaux fins (« zéro fichier écrit »,
    « ledger à zéro OPEN ») ; cible « skills » alors qu'une partie du corpus vise
    des **commands** ; verrou de format si Anthropic fait évoluer le schéma.

- **Option B — Garder le rituel maison, statu quo** : continuer A→B→A manuel.
  - Avantage : contrôle total, versionné, zéro dépendance, expressivité
    comportementale (les `expected_behavior` capturent des invariants qu'un
    `expected_output` exact ne capture pas).
  - Inconvénient : le coût manuel est un frein démontré (corpus `/grill` jamais
    exécuté) ; réinvente un outillage désormais officiel ; pas de baseline
    with/without ni de métriques quantitatives.

- **Option C — Hybride : adopter l'exécuteur officiel, garder la doctrine maison
  (recommandée)** : utiliser le Skill Creator comme **moteur d'exécution**
  (automatisation, baseline, A/B, métriques), mais conserver la **doctrine d'evals
  maison** (classes comportementales, fixtures à tension délibérée, doctrine
  d'étoffage par nécessité observée, invariants observables). On mappe
  `expected_behavior` → `assertions` officielles ; on garde les fixtures et leur
  rationale dans les README maison.
  - Avantage : récupère l'automatisation (lève le seul vrai frein) sans jeter la
    valeur propre du rituel (les classes comportementales et les fixtures à tension
    sont l'actif intellectuel, pas le mécanisme de copier-coller). Le plugin est un
    détail d'exécution remplaçable ; la doctrine reste versionnée et souveraine.
  - Inconvénient : travail de mapping initial ; deux référentiels à garder cohérents
    le temps de la transition.

## Décision

**À TRANCHER PAR L'HUMAIN.** Recommandation : **Option C (hybride)**.

Rationale de la reco : le frein réel, démontré, est le **coût manuel** (un corpus
spécifié mais jamais exécuté faute de temps de copier-coller). Le Skill Creator
supprime exactement ce frein, et ses 4 sous-agents *sont* les rôles que le rituel
A→B→A joue déjà à la main — l'adopter n'est pas un changement de paradigme, c'est
l'automatisation d'un paradigme déjà adopté. Mais la **valeur propre** du rituel
maison n'est pas son mécanisme d'exécution (remplaçable) : ce sont les **classes
comportementales** et les **fixtures à tension délibérée** (un PRD avec une
contradiction plantée qu'une relecture linéaire rate). Cette valeur doit survivre
à l'adoption de l'outil. D'où l'hybride : moteur officiel, doctrine maison.

Réserve avant d'acter : valider sur pièce que les `assertions` officielles
expriment bien les invariants comportementaux fins du corpus maison (« zéro fichier
écrit », « ledger à zéro OPEN ») — sinon l'Option C perd une partie de son intérêt
et l'Option B redevient défendable. Un essai du plugin sur **un** eval `/grill`
(ou sur `teach`) trancherait cette réserve avant migration complète.

## Conséquences

(sous réserve de validation de l'Option C)

- Installer `skill-creator@claude-plugins-official` (plugin à réinstaller
  manuellement — déjà une catégorie connue dans les README dotfiles).
- Convertir un corpus pilote (`/grill` ou `teach`) au format `evals/evals.json`,
  mapper `expected_behavior` → `assertions`, et juger si l'expressivité tient.
- Mettre à jour `CLAUDE.md` (« garde-fou = rituel d'evals ») pour refléter le
  moteur d'exécution adopté, sans abandonner la doctrine.
- Les README de corpus restent la source de vérité de la **doctrine** (classes,
  fixtures, étoffage) ; le plugin n'est que l'exécuteur.
- Trade-off accepté : une dépendance externe entre dans la chaîne de qualité. Jugé
  acceptable car le plugin est un exécuteur remplaçable et la doctrine reste
  versionnée et souveraine.
- Si la réserve d'expressivité échoue à l'essai, repli sur Option B documenté par
  un amendement de cet ADR avant passage en `Accepted`.

## Essai pilote (2026-06-23) — inconnue (a) levée

La réserve « les `assertions` officielles expriment-elles les invariants
comportementaux fins ? » a été testée par conversion réelle de l'eval maison le
plus exigeant (`output-no-file-written`, classe `no_side_effect`) au format officiel
`evals.json`. Corpus figé :
[`claude/commands/grill/evals/pilot-skill-creator/`](../claude/commands/grill/evals/pilot-skill-creator/).

Résultat : **inconnue (a) levée favorablement.**
- Les 5 `expected_behavior` se traduisent ; l'invariant double « bloc + aucun
  fichier » se scinde en 2 assertions discriminantes (gain de granularité).
- Les invariants hors-transcription deviennent **programmables** (`sha256`, `ls`),
  ce que le SKILL.md officiel encourage — la friction manuelle du rituel maison
  (vérifier hors-transcription) s'automatise.
- **Frange irréductible** : « invite finale *visible et isolée* » est un jugement de
  présentation. Le SKILL.md officiel assume cette limite (« don't force assertions
  onto things that need human judgment ») → reste qualitatif (eval-viewer), pas
  pass/fail. C'est la seule part de la doctrine maison qui ne se réduit pas à une
  assertion.

**Inconnue (b) — l'outil tient-il à l'exécution ? — reste OUVERTE.** Le plugin
installé est une version légère (SKILL.md seul, sans `agents/`, `scripts/`,
`eval-viewer/`) ; aucun run Executor/Grader n'a été exécuté. Le run live est
planifié dans [`TODO.md`](../TODO.md) (« Run live du Skill Creator officiel »),
déclenché par le prochain besoin réel d'eval (teach éprouvé, ou corpus `/grill`).
Cet ADR passe en `Accepted` (Option C) **après** ce run live — pas avant.

## Notes de vérification (source primaire)

- Plugin officiel : `anthropics/claude-plugins-official`, chemin
  `plugins/skill-creator/skills/skill-creator/SKILL.md`. Page produit :
  `claude.com/plugins/skill-creator`. Annonce datée du 2026-03-03.
- Modes Create / Eval / Improve / Benchmark et sous-agents Executor / Grader /
  Comparator / Analyzer : confirmés depuis le SKILL.md officiel (pas seulement des
  blogs tiers).
- Evaluation Tool de la Console (`platform.claude.com/docs/en/test-and-evaluate/eval-tool`)
  est un outil **distinct** : eval de *prompts* à variables `{{}}` dans la Console,
  pas un harnais SKILL.md — hors périmètre de cet ADR.
