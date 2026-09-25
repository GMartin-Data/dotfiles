# Epistemics — confidence tiers & proof scale

> **Provenance.** Adapted from two pstack playbooks in `cursor/plugins`
> (MIT, Lauren Tan, 2026): `pstack/skills/why/references/epistemics.md`
> (confidence tiers, phrasing guide, sycophancy trap, documented null) and
> `pstack/skills/blast-radius/SKILL.md` (proof scale). Commit `889ec4b`,
> fetched 2026-09-25. The two scales are transcribed as-is; the framing and
> the examples are transposed from PR archaeology to this workflow (repo,
> config and external state; audits; repo reviews). Review:
> `tasks/pstack-review-2026-09.md` §3.1, §3.3, P2. Roadmap item A2 (T1,
> tier 1).
>
> Reference document only. It adds no rule: the global CLAUDE.md keeps the
> one-line State Verification principle and points here.

State Verification says: run the verifying command, quote its result, and if
nothing can verify it, say "I don't know". This document answers the two
questions underneath that rule — **how sure am I of this claim** (the
confidence tiers) and **how far did I prove the fact this action depends on**
(the proof scale). Two scales for one habit: never flatten uncertainty into
false certainty, and never let a convincing writeup stand in for a run.

## 1. Confidence tiers

Every claim about a state — a repo, a config, an external system, someone's
code, a past decision — sits in one of five tiers. The tier decides the
phrasing.

### Direct — explicit evidence answers the question

Something someone actually wrote, or a command actually printed, that says
it. Not "the code does X, so the author must have wanted X".

- `git status -sb` printed `## main...origin/main` — the branch is in sync.
- A commit message says "disable claude.ai skill sync: stale copies competed
  at auto-invocation".
- An ADR's Decision section states the choice and its reason.
- A doc page says "requires v2.1.273 or later".

Phrasing: confident, present tense, source adjacent. "X, because Y
(command output / commit / `file:line`)."

### Supported — several indirect pieces converge

No single source states it, but the pattern across sources makes it likely.

- A file's mtime equals the session start time, the key was removed the day
  before, and the reordering of the JSON keys matches the app's serializer —
  the app rewrote the file.
- Three notes from the same week all cite the same incident.

Phrasing: confident but visibly derived. "The evidence points strongly to X:
[the specific pieces]." Cite each piece.

### Inferred — a reasonable reading, nothing explicit

The reader must understand this is an interpretation, not a fact from the
record.

- Nothing documents the threshold, but it equals the default used elsewhere
  in the codebase — likely copied.
- The fix merged the same day the incident channel lit up — likely a hotfix.

Phrasing: hedged, with the chain made explicit. "Given A and B, C seems
likely because D."

### Speculative — plausible, thin evidence, alternatives fit as well

Worth presenting, clearly marked as a guess, next to its competitors.

- "This might be a workaround for a bug since fixed, but nothing
  contemporary says so."
- "The value may match an SLA commitment, but no SLA document references it."

Phrasing: explicitly speculative. "One possibility is X; we have no direct
evidence."

### Unknown — searched and found nothing

A valid and important result. Document it: "We searched X, Y and Z for A and
B and found no rationale." Be specific about what was searched (§4).

## 2. Phrasing guide

**Words that commit** — Direct or Supported only, with the citation adjacent:
"because", "the reason is", "was designed to", "fixes / addresses / solves",
"the team decided", and the plain "is" about a state ("the tree is clean"
only after `git status`).

**Words that hedge** — Inferred and Speculative: "appears to", "seems to",
"likely", "suggests", "is consistent with", "one reading is", "plausibly",
"may have been", "the evidence points toward".

**Words to avoid**: "obviously" and "clearly" (if it were, nobody would ask),
"of course", "just" (dismissive, hides uncertainty), "I think / I believe"
(you are synthesizing evidence, not giving an opinion — say "the evidence
suggests").

**Avoid rationalization.** Code that makes sense today may have been written
for reasons that no longer apply, or were wrong when written. Do not assume
the author did the right thing and work backward to justify it; do not assume
a consistent pattern was intentional when it may be copy-paste; do not turn
an absence of evidence into evidence of absence ("nobody mentioned security,
so it was not a concern").

## 3. The sycophancy trap

A question often embeds its hypothesis: "why is it done this way — for
performance, I assume?", "the tree is clean, right?". Do not confirm it.
Treat it as one candidate among others and check the evidence independently.
If the evidence supports it, say so with citations; if not, say so and
present what the evidence does support.

The user's guess is a prompt for investigation, not a conclusion to validate.

## 4. Contradictions and the documented null

**When sources disagree** (the ticket says compliance, the PR says tech
debt), surface both with their citations. Do not pick the one that fits the
tidier narrative: both may be true (the ticket motivated the work, the PR is
the author's framing), or one may be wrong. Let the reader decide.

**When evidence is missing**, an honest "we don't know" is a deliverable. It
tells the reader the answer is not in the obvious places, that a human (the
author, the owner) must be asked, or that the question can be dropped.
Filling the gap with a confident guess harms: they will act on it.

Name the gap concretely: the question, the sources searched, what was
searched for in each, and what came back (nothing, or only tangential
material). A search that finds nothing is an answer, as long as it says what
it searched.

## 5. Proof scale — the blast-radius posture

Before an action whose safety is not obvious — a deletion, a merge, a config
change, a "this cannot break anything" — isolate **the one fact its safety
depends on**. Most changes that look risky are safe because of a single fact
("this call only drops already-dead cache entries"). Find that fact and prove
it; if it holds, most of the maybes are cleared at once. Spend the time
there, not on a long list of risks.

**Do not trust your own writeup.** A writeup that sounds right reads as
convincing whether or not it is true. Hand back the proof, not the prose.

For each safety fact, get it as far down this list as is cheap, and say where
it stopped:

1. **You said so.** Worthless on its own.
2. **You pointed at the line.** A real `file:line`, or the library's own
   source.
3. **You showed the bad case cannot happen.** You walked the failure step by
   step and it does not reach.
4. **You ran it.** A command, script or test that calls the real thing and
   fails loud if you are wrong.
5. **You reproduced it in the running app.**

Anything short of rung 4 is **unproven** — write "unproven", not "settled".
Rung 4 is usually one small command or script that calls the exact function
you are worried about.

A local example: purging eight eval sandboxes under `/tmp`. The fact that
made deletion safe was "no git worktree is registered inside them". The proof
was `git worktree list` in both repos before the first `rm` (rung 4) — not
"they look like temp dirs" (rung 1).

Look where grep stops: a pinned library version, a local patch, a wire format
or DB column read by another language, a feature flag, code three hops
downstream. Never make up a caller or an API you did not see.

## 6. Calibration check before delivering

1. Does each claim have a citation (command output, `file:line`, commit)? If
   not, add one or move the claim to Inferred / Speculative.
2. Is the phrasing calibrated to the tier? A Direct claim may say "because";
   an Inferred one may not.
3. Am I treating the code as evidence of its own intent, or my writeup as
   evidence of its own safety? Neither is evidence — remove or reclassify.
4. Is there a "what we don't know" line? None at all is suspicious: either
   the evidence was unusually complete, or something is being swept under
   the rug.
5. For each fact an action's safety depends on: which rung was reached, and
   is "unproven" written wherever rung 4 was not?

## How the two scales relate

Tiers grade a claim about what *is*; rungs grade the proof of what will
*hold* once you act. State Verification's "run the verifying command and
quote it" is rung 4 backing a Direct claim. Both scales are descriptive: no
tagging obligation follows from this document — a rule such as "tag the tier
on every state assertion" would only come through `/immunize`, on an observed
lesson.
