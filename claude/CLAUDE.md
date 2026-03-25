# Global Conventions

## Identity & Context
- Data Engineer / AI Engineer (junior, banking)
- Stack: Python 3.12+, SQL, dbt, Spark, Docker, GCP
- OS: Linux (Ubuntu 22.04)
- Shell: zsh
- Package manager: uv

## Communication
- Adapt language to user's language (default: French)
- Code, comments, docstrings: English
- Commit messages: English (Conventional Commits)

## Python Stack Choices
- Testing: pytest (never unittest)
- Logging: structlog (never print/logging)
- Docstrings: Google style
- Type hints: mandatory on all signatures

## Common Commands
- `uv sync` — install/sync dependencies
- `uv run pytest` — run tests
- `uv run ruff check .` — lint
- `uv run ruff format .` — format

## Git
- Conventional commits (feat/fix/docs/refactor/test/chore)
- Commit after each logical unit - never batch multiple concerns in one commit
- Force push and destructive rm are blocked by hooks

## Context Management
- Before /clear: always update PROGRESS.md with current state
- Use /rewind (Esc Esc) when Claude derails — don't correct in polluted context

## AI Workflow
- Project-specific conventions live in project CLAUDE.md (via /claude-md)
- Lessons learned accumulate in tasks/lessons-inbox.md (via /immunize)
- One concept at a time — never skip validation steps

## Global Do NOT
<!-- Populated by /immunize — max 20 entries -->