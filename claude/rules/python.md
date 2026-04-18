---
paths:
  - "**/*.py"
---
# Python Conventions

- Docstrings: Google style
- Logging: structlog — never use print() for logging or debugging
- Type hints on all public function signatures
- Let ruff handle formatting — don't restate rules discoverable in pyproject.toml or pre-commit config
- Prefer pathlib over os.path
- Use `from __future__ import annotations` for modern type syntax in all modules
