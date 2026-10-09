# Internal notes — agent evaluation review, 2026-10-07

Attendees: platform team (3), data engineering (2), one guest from the risk team.

## What we looked at

- Our support agent's weekly regression suite: 48 paired cases, 6 missing outcomes
  this week (timeouts on the ticketing API), 2 regressions on refund handling.
- The LLM judge rejected 11 of 48 answers; manual review agreed on 7. The judge
  prompt still penalises answers that ask a clarifying question, which the
  product team now wants to allow.
- Trajectory-level checks (tool order, argument validity) caught one case where
  the agent called `close_ticket` before `send_reply`. Final-answer scoring alone
  would have passed it.

## Decisions

1. Keep the paired-case suite as the release gate; add "asked a clarifying
   question" as an accepted outcome in the judge rubric.
2. Add a trajectory assertion on tool ordering for the three refund flows.
3. Re-run the suite on the candidate build before Friday; no release if more
   than one regression remains.

## Open questions

- Should we score the judge itself against a human-rated sample every month?
- Who owns the missing-outcome backlog when the upstream API is down?
- Do we need an external benchmark at all, given our cases are domain-specific?
