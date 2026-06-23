# TODO — Workflow PRD/progress/catchup

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