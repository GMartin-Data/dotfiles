# Brief — Audit du process d'évaluation des skills et du frontmatter (2026-09)

Brief de mission rédigé le 2026-09-22 depuis la session d'apprentissage
`~/learning-to-build-skills` (skill `teach`), à instruire dans une session Claude Code
**lancée dans `~/dotfiles`**. Non commité : à relire par Greg avant usage. Le livrable
attendu est `tasks/skill-evals-audit-2026-09.md`, dans le style des revues de ce dossier
(verdict en tête, sections numérotées, recommandations numérotées, raisonnement explicite).

Pourquoi une session dédiée dans dotfiles : les sous-agents lancés depuis le workspace
d'apprentissage n'ont pas accès à `~/dotfiles` (refus de permission, vérifié), les commandes
git doivent résoudre sur ce repo, et un éventuel chantier s'exécutera ici. L'audit est un
critère de succès de la mission d'apprentissage (« auditer son écosystème à l'aune du
standard, savoir quoi migrer ») : une fois le verdict rendu, un learning record sera écrit
dans le workspace d'apprentissage à partir du livrable.

## 0. Les trois questions à trancher (demande de Greg, 2026-09-22)

1. **Process maison vs officiel.** Comparer le process d'évaluation de skills déjà présent
   dans dotfiles à l'outillage officiel dans sa version la plus récente, et dire s'il est
   indiqué de poursuivre avec la mouture maison ou de basculer sur l'officielle.
2. **Chantier frontmatter.** Dire s'il faut ouvrir un chantier de mise à jour des skills au
   vu de l'évolution des champs de frontmatter. Greg présume, à raison, que cette question
   est fortement corrélée à la première.
3. **Transmission.** Si chantier il doit y avoir, comment le transmettre à l'instance
   Claude Code de dotfiles. Ce brief est la première réponse ; la seconde est le routage
   des conclusions vers les bons documents (voir §2.3).

Greg attend « une analyse méticuleuse et un verdict aussi éclairé que bien explicité ».
Chaque affirmation du livrable doit être vérifiable : citer la commande ou l'URL.

## 1. Contexte acquis (tout vérifié le 2026-09-22)

### 1.1 Outillage officiel

- **`claude plugin eval`** est le runner d'evals officiel de Claude Code. Doc :
  https://code.claude.com/docs/en/plugin-evals.md. Exige **≥ 2.1.269** ; en dessous la
  commande répond « `plugin eval` is currently in early access » (observé sur 2.1.267).
  - Cas = `prompt.md` + `graders/*.md` (recommandé) ou `case.yaml` (`schema_version: "1.1"`,
    blocs `execution:` et `context:` avec `scaffold_script` / `history_file` / `add_dirs`).
  - Graders : `regex`, `tool_used` (avec `input_match`), `tool_order`, `file_exists`, `llm`
    (juge, vote 2 sur 3, modèle par défaut haiku), `baseline` ; `weight`, `arm`.
  - **`tool_used: Skill` est le test de déclenchement officiel** ; marqué with-only, exclu
    du score en mode deux bras.
  - `--ablation with-without` : bras avec / sans plugin, Δ = contribution du plugin.
  - **3 runs par cas par défaut** (`case.runs ?? 3`, `--runs` de 1 à 50), `--threshold`
    (défaut 1.0, exit 1 en dessous), `--max-cost-usd`, `--judge-model`, `--model`,
    `--mocks`, `--json`, `--report` HTML, `init --bare <name>` pour un cas vierge.
  - Résultats : `evals/results/<timestamp>/aggregate-result.json` + `report.html`.
  - **Cible = un plugin** (`plugin.json` ou `.claude-plugin/plugin.json`) ou la forme
    `name@skills-dir` ; un répertoire de skill nu n'est pas accepté. **Résolu** (pièce
    jointe §2) : « Any folder under a skills directory that contains a
    `.claude-plugin/plugin.json` manifest is loaded as a plugin named `<name>@skills-dir`
    on the next session, with no marketplace and no install step ». Manifest minimal :
    `{"name": "<dossier>"}`. Donc chaque skill de `claude/skills/` peut devenir une cible
    d'eval en ajoutant ce seul fichier dans son dossier ; `~/.claude/skills/` en entier ne
    devient pas un plugin. Détail à prendre en compte : dans un cas d'eval, `allowed_tools`
    doit lister `Skill` pour que la skill soit invocable (pièce jointe §1c).
  - Deux écarts de doc à ne pas prendre pour argent comptant : skills.md mentionne
    `--test-config` et `/evals --init`, absents de plugin-evals.md et de skill-creator ;
    `assertions` vs `expectations` diffèrent selon les sources (pièce jointe, fin).
- **`/skill-doctor`** (≥ 2.1.252, session interactive) : coût en contexte et fréquence
  d'usage par skill, skills jamais invoquées. Lit les métadonnées de session, ne lance
  aucune sonde : observabilité, pas test.
- **Frontmatter Claude Code** (https://code.claude.com/docs/en/skills.md) : 11 champs
  apparus depuis juillet 2026 — `disallowed-tools`, `arguments`, `agent`, `background`,
  `effort`, `paths`, `shell`, `metadata`, `hooks`, `license`, `compatibility`. Les deux
  derniers viennent de la spec Agent Skills (https://agentskills.io/specification), qui
  liste aussi `metadata` et `allowed-tools` (expérimental) en optionnels.
- Le doc **best-practices** (règles de description, checklist) est inchangé et dit
  toujours « there is not currently a built-in way to run these evaluations » — la doc
  plateforme n'a pas encore rattrapé le runner de Claude Code.
- Les evals **agentskills.io** (`evals/evals.json`, `with_skill/` vs `without_skill/`,
  `grading.json`, `benchmark.json`) et `skill-creator` évaluent la **qualité de sortie**
  avec la skill pré-chargée ; ils ne testent pas le déclenchement.
- **État local** : Claude Code passé de 2.1.267 (canal stable) à **2.1.278** via le canal
  `latest`. Commit dotfiles `40dc978` (`chore(claude): switch auto-update channel to
  latest`, poussé). Réversible ; retour sur stable prévu quand stable ≥ 2.1.269.

### 1.2 Résultats du labo de frontière (cobaye `converting-temperatures`)

Détail complet : `~/learning-to-build-skills/learning-records/0003-boundary-lab-name-anchoring.md`
et `~/learning-to-build-skills/reference/description-triggering.md`.

- Le modèle lit name + description **sémantiquement**, pas mot à mot : « Helps with
  temperatures. » déclenche 3/3 ; « kelvin », absent de la description, 3/3.
- Le **nom est un ancrage négatif**, pas un déclencheur positif : description tentaculaire
  + `converting-temperatures` → 0/3 hors sujet ; même description + `helper-one` → 2/3.
- Claude Code **liste la skill sous le nom du dossier**, pas du champ `name` (observé) ;
  la spec impose l'égalité des deux ; l'IDE le signale.
- **Hygiène de mesure** : sonder depuis un répertoire vide (2/3 faux positifs sinon) ; un
  grep sur la sortie est un grader faillible, `tool_used` observe l'appel d'outil.
- **Déclenchement ≠ qualité de sortie** : la skill déclenchée a converti des kelvins avec
  une formule absente de son corps.
- Variable cachée : flotte d'environ 25 skills, compétition faible.

### 1.3 Existant connu dans dotfiles (à relire ici, non relu le 2026-09-22)

- `claude/skills/feynman-mentor/evals/` : `evals.json`, `feynman-mentor.eval.json`,
  README, `setup-eval-cwd.sh`, datés du 2026-07-23. **Point de départ de la question 1.**
- Corpus : 6 skills dans `claude/skills/` (coach-pedagogique, code-mentor, code-review,
  dp-coach, feynman-mentor, teach) et 10 commands legacy dans `claude/commands/` (adr,
  catchup, claude-md, grill, immunize, planning, prd, progress, tech-watch) plus `shared/`.
  Les commands sont exposées comme skills par Claude Code (fusion documentée), mais restent
  au format legacy : la question 2 inclut ce qu'une migration apporterait.
- Erreur factuelle connue dans `feynman-mentor/SKILL.md` : `allowed-tools` présenté comme
  une restriction (c'est une pré-approbation ; la restriction est `disallowed-tools`). À
  corriger dans le chantier, pas avant le verdict.
- Précédent : le grisage d'`allowed-tools` par l'IDE en juillet était un retard du
  validateur (anthropics/claude-code #26795), pas une dépréciation. Vérifier contre spec et
  docs, pas contre l'IDE.
- Le cobaye `converting-temperatures` vit **hors du repo** (`~/.claude/skills/`, répertoire
  simple, pas un symlink) ; il est restauré à l'identique.

## 2. Critères de décision proposés

### 2.1 Question 1 — grille de comparaison

Comparer le process maison et `claude plugin eval` sur chaque ligne, avec preuve :

| Capacité | Maison (à établir) | `claude plugin eval` |
|---|---|---|
| Test de déclenchement | ? | `tool_used: Skill` |
| Assertions sur la sortie | ? | `regex`, `file_exists`, `llm` |
| Baseline / ablation | ? | `--ablation with-without`, Δ |
| Répétition, variance | ? | 3 runs par défaut |
| Contexte de départ (cwd, fichiers, historique) | `setup-eval-cwd.sh` ? | `context:` (scaffold, history_file, add_dirs) |
| Contrôle de coût | ? | `--max-cost-usd`, `--runs`, mocks |
| Rapport, exit code CI | ? | JSON + HTML, `--threshold` |
| Cible : skill personnelle nue | oui ? | non, plugin ou `name@skills-dir` |
| Portabilité hors Claude Code (SDK, API, autres agents) | ? | Claude Code seulement |
| Maturité, risque de rupture | stable ? | early access jusqu'à 2.1.269, version-gated |
| Charge de maintenance | ? | portée par Anthropic |

Verdicts possibles : **garder** la mouture maison, **basculer** sur l'officielle, ou
**hybride** (cas et assertions maison conservés comme matière, exécution par le runner
officiel). Inconnues à lever avant de trancher : (a) comment cibler une skill de
`claude/skills/` — emballer `claude/` en plugin, ou forme `name@skills-dir` ; (b) coût réel
d'une suite (mesurer sur un cas) ; (c) ce que le harness maison sait faire que le runner ne
sait pas.

### 2.2 Question 2 — inventaire frontmatter et seuil de chantier

Pour chacun des 16 artefacts : champs utilisés ; conformité spec (`name` = dossier,
description ≤ 1024 caractères, 3e personne, sans balise XML) ; champs Claude Code qui
résoudraient un problème connu (`when_to_use` pour le routage entre skills sœurs, `paths`,
`disallowed-tools`, `context: fork` + `agent`, `effort`, `hooks`, `arguments` pour les
commands) ; pour les 10 commands, ce que la migration en skill apporte réellement.

Seuil proposé : chantier **seulement si** (a) violation de spec, ou (b) un champ change un
comportement observable, ou (c) un champ résout une douleur documentée (routage, coût,
permissions). Sinon : mise à jour opportuniste au fil des retouches. Corrélation avec la
question 1 : si le verdict est « runner officiel », l'emballage en plugin est un changement
structurel qui absorbe naturellement la migration commands → skills ; les deux chantiers
n'en font alors qu'un.

### 2.3 Question 3 — routage des conclusions

Lire `docs/methodology/responsibility-matrix.md` et router : le livrable d'audit dans
`tasks/` (pattern du dossier) ; les décisions qui changent la façon de construire ou tester
les skills en ADR ; un chantier multi-phases en PLAN ; les règles durables dans le
CLAUDE.md concerné ; les leçons dans `tasks/lessons-inbox.md`. Le brief ne tranche pas ce
routage : c'est un point de replanification, la matrice fait foi.

## 3. Méthode proposée pour la session dotfiles

1. `/catchup`, puis lire `CLAUDE.md`, `progress.md`, la matrice de responsabilité.
2. Lire le rapport de doc officielle joint (§5) ; ne re-fetcher que ce qui doit être
   re-vérifié pour une affirmation du livrable.
3. Lire intégralement `claude/skills/feynman-mentor/evals/` et dater par `git log`.
4. Inventaire frontmatter, par sous-agent si utile (ils ont accès ici) :
   `for f in claude/skills/*/SKILL.md claude/commands/*.md; do echo "== $f"; sed -n '/^---$/,/^---$/p' "$f"; done`
5. Test pratique si peu coûteux : un `claude plugin eval` sur un emballage minimal du
   cobaye ou de `feynman-mentor`, `--runs 1 --ablation none --max-cost-usd <petit>`,
   pour confirmer le ciblage et mesurer le coût. Depuis un répertoire vide.
6. Rédiger `tasks/skill-evals-audit-2026-09.md` : verdict en tête, une section par
   question, recommandations numérotées, chaque affirmation citée.
7. Retour vers le workspace d'apprentissage : copier le verdict dans un learning record
   `0004-*.md` de `~/learning-to-build-skills/learning-records/`.

## 4. Contraintes

- **Aucune modification de skill ou de command avant validation du verdict par Greg.**
- Commits : Conventional Commits, directs sur `main` autorisés (exemption déclarée dans
  le CLAUDE.md de dotfiles), **sans trailer `Co-Authored-By`**.
- Sources Web re-vérifiées et datées ; jamais depuis la seule mémoire paramétrique.
- Autonomie graduée : un pas logique par tour sans critère de succès explicite ; expliquer
  avant de produire tout artefact qui touche aux skills.
- Ne pas toucher `~/.claude/settings.json` au-delà du commit `40dc978`.

## 5. Pièces jointes

- Rapport de doc officielle : `tasks/skill-evals-audit-2026-09-docs.md` (présent ; produit
  par un agent de recherche le 2026-09-22 : plugin-evals complet, plugins-reference
  « skills-directory plugins », frontmatter Claude Code intégral, spec Agent Skills,
  skill-creator et agentskills evals, tableau comparatif par capacité).
- `~/learning-to-build-skills/RESOURCES.md` : sources vérifiées et datées, écarts connus.
- `~/learning-to-build-skills/learning-records/0003-boundary-lab-name-anchoring.md`.
- `~/learning-to-build-skills/reference/description-triggering.md`.
- Script de sonde `probe.sh` : dans le scratchpad éphémère de la session du 2026-09-22 ;
  à recréer depuis le protocole de l'aide-mémoire si besoin (boucle `claude -p`, grep du
  marqueur, répertoire vide).
