# TODO — Workflow PRD/progress/catchup

## Évaluation de maturité (2026-06-28)

Scoring des items différés avec la grille 3 axes du protocole `/insights` v3
(Impact 1-3 / Coût 1-3 / Risque 1-3, sans score composite), augmentée d'une colonne
**Déclencheur atteint ?** — un item à fort impact mais dont la condition n'est pas
remplie ne doit pas être lancé (automatisation spéculative, contraire à YAGNI /
build-before-automating).

| Item | Impact | Coût | Risque | Déclencheur atteint ? |
|---|:---:|:---:|:---:|---|
| Hook `/clear` → force `/progress` | 2 | 2 | 3 | ❌ ~10 cycles manuels non comptés |
| Check de parité commands automatisé | 1 | 2 | 1 | ❌ pas de 3ᵉ récurrence malgré la checklist |
| Migrer PR template + skill `/pr` | 2 | 3 | 2 | 🟡 (a) prêt / (b) bloqué (workflow non finalisé) |
| Audit « mettre de l'ordre » workflow | 3 | 3 | 2 | ❌ stabilité du workflow non atteinte |
| Run live Skill Creator → ADR-0009 | 2 | 3 | 2 | ❌ pas de besoin réel d'eval survenu |

**Verdict :** aucun item mûr à déclencher. Seul **(a)** de « Migrer PR template »
(déplacement du `pull_request_template.md` vers le repo Cookiecutter, indépendant de
la finalisation du workflow) a son déclencheur atteint — candidat « petit format »
au prochain passage. Décision 2026-06-28 : respecter tous les différés (la grille
confirme ce que les conditions de chaque item disaient déjà). Le fix
`block-force-push.sh` (seul item à déclencheur « bug reproductible ») a été traité
cette session, commit `595eef1`.

---

## Évolution prévue : automatisation du checkpoint pré-clear

**Quand :** après ~10 cycles manuels du workflow PRD → CLAUDE.md → progress → catchup.

**Quoi :** évaluer un hook PreToolUse sur `/clear` qui force `/progress` avant le reset de contexte.

**Pourquoi attendre :** accumuler l'expérience des frictions réelles avant d'automatiser. Le workflow manuel permet aussi une revue de code formatrice.

**Réf :** discussion audit Module 0.3, session du 2025-03-06.

---

## Migrer PR template vers python-project-template + créer skill `/pr`

**Quoi :**
- (a) `.github/pull_request_template.md` (anciennement dans `scaffolds/python-uv/`) doit vivre dans le repo Cookiecutter `GMartin-Data/python-project-template`, sous `{{ cookiecutter.project_slug }}/.github/`
- (b) skill `~/.claude/skills/pr/SKILL.md` pour les PR créées par Claude (qui n'utilisent pas le template GitHub natif via `gh pr create --body`)

**Pourquoi :**
- (a) un PR template relève du code-skeleton projet, pas des dotfiles AI — doctrine "dotfiles = IA, template = code"
- (b) `gh pr create --body "..."` non-interactif ignore le template GitHub natif → besoin d'un mécanisme propre à Claude

**Comment :**
- (a) ouvrir une PR dans le template avec le contenu récupérable via `git show <commit>^:scaffolds/python-uv/.github/pull_request_template.md` (supprimé de dotfiles lors du retrait de `scaffolds/`)
- (b) skill bloquée tant que la structure du template (ADR, TODOs agentiques, autres éléments workflow) n'est pas finalisée — voir audit workflow à venir

**Réf :** audit dotfiles du 2026-04-18 Phase 1 (point a) ; session karpathy-inspired-guidelines du 2026-05-27 (point b).

---

## Audit "mettre de l'ordre" dans le workflow agentique

**Quand :** une fois le workflow agentique formellement finalisé (PR template, ADR, skill `/pr` et autres éléments encore à arbitrer). Pas de date — c'est la stabilité qui déclenche, pas le calendrier.

**Quoi :** inventaire factuel des intentions/conventions/TODOs à travers les ~11 lieux possibles (CLAUDE.md user/projet, progress.md, lessons-inbox, TODO.md, MEMORY.md, skills, hooks, rules, routines, agents, commands). Identifier redondances, contradictions, télescopages. Décider de règles d'aiguillage stables (où va quoi).

**Pourquoi :** procéder par tâtonnements crée des décisions oubliées et des redécouvertes coûteuses. L'audit produit le repère stable nécessaire pour aiguiller les décisions futures sans réinventer à chaque fois.

**Réf :** discussion session karpathy-inspired-guidelines du 2026-05-27.

---

## Check de parité automatisé pour l'ajout d'une command

**Quand :** si l'oubli multi-fichiers se reproduit **malgré** la checklist manuelle (une 3e occurrence après celles de la session grill). Pas avant — la checklist est le palier léger, déjà en place.

**Quoi :** un garde-fou exécutable (script `scripts/check-commands-parity.sh`, voire hook PreToolUse/commit) qui vérifie la parité `claude/commands/*.md` ↔ lignes `link` d'`install.sh` ↔ ligne `**Commands**` des deux README, et échoue en listant les écarts.

**Pourquoi attendre :** YAGNI / build before automating. La checklist « Ajouter une command » de `claude/README.md` (palier 1, déjà écrite) est le test minimal. On n'écrit le garde-fou exécutable que si la discipline humaine prouve son insuffisance — sinon c'est de l'automatisation spéculative pour un repo mono-utilisateur.

**Comment :** le test de parité source ↔ install.sh est déjà esquissé dans la checklist de `claude/README.md` (one-liner `diff`). L'étendre aux deux README et l'empaqueter en script appelable. Décider à ce moment-là entre script manuel (`maintain`-style) et hook bloquant.

**Réf :** session grill-implementation du 2026-06-23 — trois oublis successifs (symlink `install.sh`, `README.md`, `claude/README.md`) en ajoutant `/grill`, racine commune avec les oublis `adr`/`planning` des sessions antérieures.

---

## Run live du Skill Creator officiel → trancher l'adoption (ADR-0009)

**Quand :** au **prochain besoin réel** de lancer un eval — soit `teach` une fois
éprouvé en usage, soit le corpus `/grill` (écrit mais jamais exécuté en A→B→A).
Pas avant, pas à blanc : c'est le besoin d'évaluer qui déclenche, pas le calendrier.

**Quoi :** installer la version **complète** du plugin
`skill-creator@claude-plugins-official` (le plugin présent sur disque est une
version légère : SKILL.md seul, sans `agents/grader.md`, `scripts/aggregate_benchmark`,
ni `eval-viewer/`), puis faire un vrai run Executor/Grader sur un eval converti.
Objectif : lever l'**inconnue (b) d'ADR-0009** — l'outil tient-il à l'exécution ?
(L'inconnue (a) — le format `assertions` exprime-t-il les invariants comportementaux
fins — a été levée favorablement par l'essai pilote du 2026-06-23, cf. corpus
`claude/commands/grill/evals/pilot-skill-creator/`.)

**Pourquoi attendre :** *build-before-automating* appliqué à mon propre outillage
d'evals. Le run live à blanc serait du yak-shaving : il se justifie quand il sert
une évaluation réellement voulue, pas pour valider l'outil dans le vide. Le vrai
chantier reste `teach` + la trajectoire AI Engineer ; l'outillage d'evals est un
méta-chantier qui ne doit pas le précéder.

**Comment :**
1. `/plugin install skill-creator@claude-plugins-official` (version complète) puis
   `/reload-plugins`.
2. Reprendre l'eval pilote déjà converti (`output-no-file-written`) et le faire
   tourner via les sous-agents ; vérifier que le grader sait exécuter l'assertion
   programmable `sha256 unchanged` et que l'eval-viewer rend le résultat.
3. **Portée :** le run live valide le *moteur* une fois pour toutes (il ne dépend
   pas de la skill testée). L'**adoption par skill** (teach, code-mentor,
   coach-pedagogique, dp-coach) se fait ensuite au fil de l'eau, chacune migrant
   son corpus quand elle est éprouvée — pas un big-bang.
4. Sur succès → passer **ADR-0009 en Accepted (Option C hybride)** : moteur officiel
   + doctrine maison (classes comportementales, fixtures à tension). Sur échec
   d'exécution → repli Option B documenté par amendement de 0009 avant Accepted.

**Réf :** ADR-0009 (Proposed) ; essai pilote de traductibilité du 2026-06-23
(session learning-skill) ; SKILL.md officiel vérifié dans
`anthropics/claude-plugins-official`.