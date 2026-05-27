# User Conventions (Greg)

## Identity
- Data Engineer / AI Engineer
- OS: Linux (Ubuntu 22.04), Shell: zsh, Package manager: uv

## Communication
- Respond in user's language (default: French)
- All code, comments, docstrings, commits: English
- Commits: Conventional Commits format

## Session Discipline
- Before /clear or ending a session: invoke `/progress` to checkpoint current state and next steps
- Project-specific conventions live in each project's CLAUDE.md
- Lessons learned accumulate in tasks/lessons-inbox.md (via /immunize)
- One concept at a time — validate before moving to next step

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

## Global Do NOT
- Never bury an operational step in a parenthetical or subordinate clause — always promote it to its own paragraph with numbering or bold. The model (Sonnet or Opus) systematically skips steps nested in second-tier typography. (learned 2026-04, from dotfiles)
- When a spec prescribes a separation (one question at a time, binary criteria, behavior vs implementation, deliverables vs polish), never collapse the categories for the sake of efficiency — sequence them instead. The model systematically erases these boundaries whenever the UX seems to invite a shortcut. (learned 2026-04, from memory-grep)
- In a multi-phase workflow, always verify cross-phase consistency before final validation: v1 exclusions → risks → success criteria must form an unbroken, contradiction-free chain. Never treat each phase in isolation. (learned 2026-04, from memory-grep)
