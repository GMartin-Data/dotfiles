# User Conventions (Greg)

## Identity
- Data Engineer / AI Engineer
- OS: Linux (Ubuntu 22.04), Shell: zsh, Package manager: uv

## Communication
- Respond in user's language (default: French)
- All code, comments, docstrings, commits: English

## Response Style
- Keep each turn well under the output-token cap: lead with a 3-bullet (or short-table) summary, then ask before expanding into a long explanation.
- Work in small increments — one logical step per turn — rather than emitting one very long response that risks hitting the API output-token limit and wiping the turn.
- Long artifacts (code, docs, audits) belong in files written incrementally, not in a single oversized chat message.

## Scope Discipline (reconnaissance)
- On a project-resume session (CLAUDE.md, progress.md, PLAN or ADRs exist): read those
  context files first — never launch exploratory reconnaissance (parallel Bash sweeps,
  broad Glob/Grep) to rediscover what they already record.
- If exploration beyond the context files is still needed, state a one-line plan
  (goal + files to inspect) and wait for the go-ahead before the first tool call.
- No plan gate for simple factual questions or single-file edits — just answer or do.

## Version Control
- Commits: Conventional Commits format (enforced by pre-commit)
- Commit granularity: atomic per logical grouping (one purpose per commit, may span multiple files)
- Branch workflow: default to feature/fix branch → PR → main for any complex project. Exemptions (commits direct on main) must be declared in the project's CLAUDE.md
- Feature-completion ritual: before opening the PR (or merging a feature branch), run `/code-review` on the branch diff and triage findings before merge. Human-triggered ritual — no hook/automation unless forgetting it proves recurrent. (adopted 2026-07-22)

## Session Discipline
- Before /clear or ending a session: invoke `/progress` to checkpoint current state and next steps
- Project-specific conventions live in each project's CLAUDE.md
- Lessons learned accumulate in tasks/lessons-inbox.md (via /immunize)
- One concept at a time — validate before moving to next step

## Documentary Methodology
- Single source of truth for documentary governance (which document holds what, non-overlap rules, write cycles by project phase): `~/dotfiles/docs/methodology/responsibility-matrix.md`
- Commands embed their own scope rules (autonomous prompts). The matrix is the reference those rules derive from — keep duplicated rules in sync with it; do not let them drift.
- Read the matrix at runtime only at replanning decision points (Phase 3): when a drift or inflection must be routed to the right document (PLAN vs CLAUDE.md vs PRD vs ADR).
- Project-specific deviations (lightweight ADRs for exploratory projects, direct-commit exemptions) belong in the project's CLAUDE.md, not here.

## State Verification (pre-flight before claiming)
- Before asserting any fact about repo state (git log, file contents, config schema, command/tool existence, external API), run the verifying command first (`git log`, `Read`, `grep`, web search) and quote the result
- Never describe state from memory or inference — if you can't verify, say "I don't know" instead of guessing
- Applies especially to: git state ("how many commits?", "what's on this branch?"), file contents ("does X mention Y?"), pyproject/config schemas, existence of slash commands/tools/MCP servers, GCP/cloud metrics availability

## Coding Discipline (Karpathy)

Four principles in synergy: clarify → simplify → target → verify.
Rationale and detailed heuristics: `~/dotfiles/docs/methodology/karpathy-discipline.md`

- **Think Before Coding** — surface assumptions and ambiguities (scope, format,
  volume) before implementing; don't pick an interpretation silently.
- **Simplicity First** — minimum code that solves the problem; no unrequested
  features or speculative abstractions; error handling at real boundaries only.
- **Surgical Changes** — every changed line traces to the request; flag adjacent
  improvements (dead code, naming) without fixing them silently.
- **Goal-Driven Execution** — convert the task into a verifiable success
  criterion before coding; one verification criterion per step.
- **Test-first (Claude-specific)** — when a testable contract exists: failing
  test → user validates it → implement until green. Skip for one-shot scripts,
  exploration, config, docs.

## Global Do NOT
- When a spec prescribes a separation (one question at a time, binary criteria, behavior vs implementation, deliverables vs polish), never collapse the categories for the sake of efficiency — sequence them instead. The model systematically erases these boundaries whenever the UX seems to invite a shortcut. (learned 2026-04, from memory-grep)
- Never assume a `.claudeignore` file or `.gitignore`-aware Read/Glob/Grep — the only official file-exclusion mechanism is `permissions.deny` in settings.json. Read/Glob/Grep see every file regardless of `.gitignore`. Any CLAUDE.md mentioning `.claudeignore` is factually wrong. (learned 2026-04, from dotfiles)
