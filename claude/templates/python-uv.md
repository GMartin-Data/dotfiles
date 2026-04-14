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
- Squash and merge into main
- Semantic versioning via python-semantic-release

## Architecture
<!-- Describe key modules, data flow, or domain concepts Claude needs to understand -->

## Project-Specific Rules
<!-- Anything unique to THIS project that overrides or extends shared conventions -->