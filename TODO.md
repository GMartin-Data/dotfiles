# TODO — Workflow PRD/progress/catchup

## Évolution prévue : automatisation du checkpoint pré-clear

**Quand :** après ~10 cycles manuels du workflow PRD → CLAUDE.md → progress → catchup.

**Quoi :** évaluer un hook PreToolUse sur `/clear` qui force `/progress` avant le reset de contexte.

**Pourquoi attendre :** accumuler l'expérience des frictions réelles avant d'automatiser. Le workflow manuel permet aussi une revue de code formatrice.

**Réf :** discussion audit Module 0.3, session du 2025-03-06.

---

## Migrer PR template vers python-project-template

**Quoi :** `.github/pull_request_template.md` (anciennement dans `scaffolds/python-uv/`) doit vivre dans le repo Cookiecutter `GMartin-Data/python-project-template`, sous `{{ cookiecutter.project_slug }}/.github/`.

**Pourquoi :** un PR template relève du code-skeleton projet, pas des dotfiles AI. La doctrine "dotfiles = IA, template = code" impose cette migration.

**Comment :** ouvrir une PR dans le template avec le contenu de `scaffolds/python-uv/.github/pull_request_template.md` (supprimé de dotfiles lors du retrait de `scaffolds/` — récupérable via `git show <commit>^:scaffolds/python-uv/.github/pull_request_template.md`).

**Réf :** audit dotfiles du 2026-04-18, Phase 1.