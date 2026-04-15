## PR Title (conventional commit format)

> **The PR title becomes the squash commit message on `main`.**
> It MUST follow [Conventional Commits](https://www.conventionalcommits.org/):
>
> `<type>(<scope>): <description>`
>
> Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `ci`, `chore`
> Breaking changes: add `!` after type/scope → `feat!: remove legacy endpoint`

## What

<!-- What does this PR do? Keep it brief. -->

## Why

<!-- Why is this change needed? Link issue if applicable. -->

## How to test

<!-- Steps to verify the change. -->

## Checklist

- [ ] PR title is in conventional commit format
- [ ] Tests pass (`uv run pytest`)
- [ ] Linting passes (`uv run ruff check .`)
- [ ] No unrelated changes