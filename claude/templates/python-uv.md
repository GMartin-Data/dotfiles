# Project: [PROJECT_NAME]

## Overview
<!-- One paragraph: what this project does and why it exists -->

## Stack
- Python 3.12+, managed by uv
- Framework: [FastAPI / CLI / library — adapt]

## Commands
- `uv sync` — install/sync dependencies
- `uv run pytest` — run tests
- `uv run ruff check .` — lint
- `uv run ruff format .` — format
- `pre-commit run --all-files` — run all hooks

## Quality Gates
- pre-commit: ruff check + ruff format (mandatory)
- CI (GitHub Actions): ruff + pytest on every PR
- No merge without green CI

## Git
- Feature branches: `feat/short-description` or `fix/short-description`
- Commit messages inside the branch: no format enforced, keep them descriptive
- **PR title IS the squash commit message** — it MUST follow Conventional Commits: `<type>(<scope>): <description>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `ci`, `chore`
- Breaking change: add `!` after type/scope → `feat!: remove legacy endpoint`

## Versioning
- python-semantic-release runs on every push to `main` and reads the squash commit (= PR title) to decide the bump:
  - `feat` → minor, `fix`/`perf` → patch, `!` → major
- **Never manually edit `project.version` in `pyproject.toml`** — semantic-release owns it

## Architecture
<!-- Describe key modules, data flow, or domain concepts Claude needs to understand -->

## Project-Specific Rules
<!-- Anything unique to THIS project that overrides or extends shared conventions -->