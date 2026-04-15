# Python + uv project conventions

## Stack
- Python 3.12+, uv (package manager), ruff (lint/format), pytest
- Pre-commit: ruff check + ruff format

## Git workflow
- **Branch strategy:** feature branches → PR → squash and merge to main
- **Commit messages in branch:** no format enforced, keep them descriptive
- **PR title IS the squash commit message.** It MUST be conventional commit format:
  `<type>(<scope>): <description>` — e.g. `feat(auth): add JWT refresh endpoint`
- Types: feat, fix, docs, style, refactor, perf, test, ci, chore
- Breaking change: add `!` after type/scope → `feat!: remove v1 API`

## Versioning
- python-semantic-release runs on every push to main
- It reads the squash commit (= PR title) to decide version bump:
  - `feat` → minor, `fix`/`perf` → patch, `!` → major
- **Never manually edit `project.version` in pyproject.toml** — semantic-release owns it

## When working on a task
1. Create a feature branch from main
2. Make atomic commits, run `uv run ruff check . && uv run pytest` before pushing
3. Open PR with conventional commit title
4. After review, squash and merge

## Commands
- `uv sync` — install/sync dependencies
- `uv run ruff check .` — lint
- `uv run ruff format .` — format
- `uv run pytest` — test
- `uv run ruff check --fix .` — autofix lint issues