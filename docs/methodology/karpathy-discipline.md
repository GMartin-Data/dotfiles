# Coding Discipline (Karpathy) — rationale & detailed heuristics

> **Provenance.** Full version of the "Coding Discipline (Karpathy)" section of
> the global CLAUDE.md (`claude/CLAUDE.md`), moved here during the 2026-07 audit
> (`tasks/claude-md-audit-2026-07.md`, items K1–K5). The global file keeps
> one-line principles; this document holds the Why / How-to-apply blocks —
> pedagogy for the human, not context for the model.
>
> Source: https://github.com/multica-ai/andrej-karpathy-skills

Four principles applied in synergy across the coding cycle: **clarify →
simplify → target → verify**.

## Think Before Coding

Before implementing, state assumptions explicitly. If multiple interpretations
exist, surface them — never pick silently.

**Why:** a silent interpretation costs a full rework; a clarifying question
costs 30 seconds.

**How to apply:** on any non-trivial request, list the ambiguities (scope,
format, volume, fields) before writing the first line of code. (adopted
2026-05-27, from karpathy)

## Simplicity First

Minimum code that solves the problem. No unrequested features, abstractions, or
error handling. No defense against impossible scenarios.

**Why:** speculative abstractions (Factory, ABC for a single caller) and
defensive error handling at internal boundaries are the two main sources of
unhelpful complexity.

**How to apply:** mental test — "would a senior engineer call this
overcomplicated?" If yes, rewrite. Error handling belongs at real boundaries
only (user input, external API). (adopted 2026-05-27, from karpathy)

## Surgical Changes

Touch only what is necessary. Do not refactor, reformat, or rename adjacent
code. Remove orphans **you** created; flag preexisting dead code without
deleting it.

**Why:** a diff mixing fix + refactor + cleanup becomes unreviewable;
line-to-request traceability disappears.

**How to apply:** every changed line must trace to the user's request. Flag
adjacent improvements (unused imports, poor naming) — never fix them silently.
(adopted 2026-05-27, from karpathy)

## Goal-Driven Execution

Convert every task into a verifiable success criterion before coding. Reject
vague goals ("make it work", "more secure").

**Why:** without a pass/fail criterion, there is no stopping condition → the
task drifts and demands constant clarifications.

**How to apply:** transform the request into a test or measurement ("add
validation" → "write tests for invalid inputs, make them pass"). For multi-step
tasks, plan with a verification criterion per step. (adopted 2026-05-27, from
karpathy)

## Test-first (operational rule from Goal-Driven Execution)

When a testable contract exists (function, API, module with assertable
behavior), write the failing test → validate with user → make it pass. Skip for
scripts, exploration, config, docs.

**Why:** test-first exposes Claude's interpretation as a short, readable
artifact (the test) before any implementation — amplifies the human's ability
to catch interpretation drift early, and gives a trivial pass/fail stopping
condition. User remains test-after; this rule is specific to Claude as an
agent.

**How to apply:** on any task with a testable contract, write the failing test
first, surface it to the user for validation, then implement until green. For
non-testable work (one-shot scripts, data exploration notebooks, YAML/TOML
config, documentation), no test-first requirement. (adopted 2026-05-27, derived
from karpathy-4)
