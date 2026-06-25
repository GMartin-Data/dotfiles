# User Conventions (Greg)

## Identity
- Data Engineer / AI Engineer
- OS: Linux (Ubuntu 22.04), Shell: zsh, Package manager: uv

## Communication
- Respond in user's language (default: French)
- All code, comments, docstrings, commits: English

## Version Control
- Commits: Conventional Commits format (enforced by pre-commit)
- Commit granularity: atomic per logical grouping (one purpose per commit, may span multiple files)
- Branch workflow: default to feature/fix branch → PR → main for any complex project. Exemptions (commits direct on main) must be declared in the project's CLAUDE.md

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

Four principles applied in synergy across the coding cycle: clarify → simplify → target → verify. Source: https://github.com/multica-ai/andrej-karpathy-skills.

- **Think Before Coding** — Before implementing, state assumptions explicitly. If multiple interpretations exist, surface them — never pick silently.
  **Why:** a silent interpretation costs a full rework; a clarifying question costs 30 seconds.
  **How to apply:** on any non-trivial request, list the ambiguities (scope, format, volume, fields) before writing the first line of code. (adopted 2026-05-27, from karpathy)

- **Simplicity First** — Minimum code that solves the problem. No unrequested features, abstractions, or error handling. No defense against impossible scenarios.
  **Why:** speculative abstractions (Factory, ABC for a single caller) and defensive error handling at internal boundaries are the two main sources of unhelpful complexity.
  **How to apply:** mental test — "would a senior engineer call this overcomplicated?" If yes, rewrite. Error handling belongs at real boundaries only (user input, external API). (adopted 2026-05-27, from karpathy)

- **Surgical Changes** — Touch only what is necessary. Do not refactor, reformat, or rename adjacent code. Remove orphans **you** created; flag preexisting dead code without deleting it.
  **Why:** a diff mixing fix + refactor + cleanup becomes unreviewable; line-to-request traceability disappears.
  **How to apply:** every changed line must trace to the user's request. Flag adjacent improvements (unused imports, poor naming) — never fix them silently. (adopted 2026-05-27, from karpathy)

- **Goal-Driven Execution** — Convert every task into a verifiable success criterion before coding. Reject vague goals ("make it work", "more secure").
  **Why:** without a pass/fail criterion, there is no stopping condition → the task drifts and demands constant clarifications.
  **How to apply:** transform the request into a test or measurement ("add validation" → "write tests for invalid inputs, make them pass"). For multi-step tasks, plan with a verification criterion per step. (adopted 2026-05-27, from karpathy)

- **Test-first (operational rule from Goal-Driven Execution)** — when a testable contract exists (function, API, module with assertable behavior), write the failing test → validate with user → make it pass. Skip for scripts, exploration, config, docs.
  **Why:** test-first exposes Claude's interpretation as a short, readable artifact (the test) before any implementation — amplifies the human's ability to catch interpretation drift early, and gives a trivial pass/fail stopping condition. User remains test-after; this rule is specific to Claude as an agent.
  **How to apply:** on any task with a testable contract, write the failing test first, surface it to the user for validation, then implement until green. For non-testable work (one-shot scripts, data exploration notebooks, YAML/TOML config, documentation), no test-first requirement. (adopted 2026-05-27, derived from karpathy-4)

## Global Do NOT
- Never bury an operational step in a parenthetical or subordinate clause — always promote it to its own paragraph with numbering or bold. The model (Sonnet or Opus) systematically skips steps nested in second-tier typography. (learned 2026-04, from dotfiles)
- When a spec prescribes a separation (one question at a time, binary criteria, behavior vs implementation, deliverables vs polish), never collapse the categories for the sake of efficiency — sequence them instead. The model systematically erases these boundaries whenever the UX seems to invite a shortcut. (learned 2026-04, from memory-grep)
- In a multi-phase workflow, always verify cross-phase consistency before final validation: v1 exclusions → risks → success criteria must form an unbroken, contradiction-free chain. Never treat each phase in isolation. (learned 2026-04, from memory-grep)
- Never assume a `.claudeignore` file or `.gitignore`-aware Read/Glob/Grep — the only official file-exclusion mechanism is `permissions.deny` in settings.json. Read/Glob/Grep see every file regardless of `.gitignore`. Any CLAUDE.md mentioning `.claudeignore` is factually wrong. (learned 2026-04, from dotfiles)
- In a multi-phase session, treat conventions decided mid-session (naming, language, allowed scopes, locked rules) as hard constraints for all subsequent phases — never as soft suggestions. If a later input violates a previously-locked convention, flag it explicitly and propose a fix rather than accepting it passively. (learned 2026-04, from dotfiles)
