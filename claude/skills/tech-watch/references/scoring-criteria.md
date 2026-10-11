# Scoring Criteria

Score each ranked result 0–100 by summing the five criteria below. Only
on-topic results reach this step (SKILL.md, step 5): adjacent results are not
ranked, they are listed apart (at most 3) without a score; off-topic results
were dropped. Apply the criteria in order and stop early if a result clearly
cannot reach 60.

`W` = the window of the watch (`days_back`: 30 by default, 60 for niche or
slow-moving topics).

---

## 1. Relevance — 40 points

| Label (from step 5) | Points |
|---|---|
| exact: the source is about the topic | 40 |
| partial: the topic is one section among others | 25 |

## 2. Freshness — 20 points, relative to the window

| Age of the source | Points |
|---|---|
| ≤ W/4 (7 days for W=30, 15 for W=60) | 20 |
| ≤ W/2 | 15 |
| ≤ 3W/4 | 10 |
| ≤ W | 5 |
| > W | 0 |

Date to use: paper and video = publication date; repository = **creation date**
when the repository was created inside the window, otherwise last push date
with the result **capped at 10** (a maintained old project is not a new one);
web page = verified date (step 8), `unverified` = 5.

## 3. Authority — 20 points, by nature of the source, never by platform

| Level | Points | Who |
|---|---|---|
| **A** Primary | 20 | the topic owner: official docs, announcement, reference repository or spec, official channel or blog |
| **B** Expert | 14 | identified research group or organization, established engineering blog, conference talk, maintainer of a related project, editorially curated newsletter |
| **C** Community | 8 | personal blog, dev.to / Medium / Substack post, community repository, YouTube creator |
| **D** Low-signal | 0 | SEO page, listicle without original content, auto-generated or lead-magnet page, rewrite of an announcement or documentation without original content (no example, test or information absent from the primary source) |

arXiv papers are B by default, A when the group owns the topic. A YouTube
video or a GitHub repository is C unless its author qualifies for A or B.

A web page whose author or organization was not established at step 8 (not
opened: budget exhausted or fetch failed; or opened without an identifiable
author) is written `unverified` there and scores as **C** here. The domain
alone does not establish authority: an unopened page on the owner's domain is
still `unverified`. With date and length `unverified` too, such a page scores
at most 40 + 5 + 8 + 3 + 3 = 59 and is excluded by the threshold, which is
the cap the known limitations in SKILL.md rely on.

## 4. Depth — 10 points

| Type | Points |
|---|---|
| arXiv paper | 10 |
| web page > 1500 words | 10 — 600–1500 words: 6 — < 600 words or length `unverified`: 3 |
| video ≥ 20 min | 10 — 10–20 min: 7 — 3–10 min: 4 (shorter videos were dropped at step 5) |
| repository: reference implementation of the topic | 10 — other repository: 6 |

## 5. Engagement — 10 points

| Signal | Points |
|---|---|
| strong: stars > 500, views > 10k, or explicit citations | 10 |
| some: stars 100–500, views 1k–10k | 5 |
| none or unknown (do not penalize absence) | 3 |

---

## Threshold, cap, ties

- **Threshold: 60, strict.** Below 60 is excluded, whatever tiers were run. If
  fewer than 10 sources reach 60 after Tier 3, write a coverage note in the
  report header instead of filling in.
- **Cap: 20 sources.** Order by score; ties broken by the engagement signal
  (stars or views).

## Score bands

| Range | Label | Meaning |
|---|---|---|
| 85–100 | 🔴 Essential | Include prominently, likely to anchor NotebookLM analysis |
| 70–84 | 🟠 High value | Include, solid signal |
| 60–69 | 🟡 Worth including | Include if total results < 20 |
| < 60 | Excluded | Not listed |

---

## Score reasoning

For each included result, write a one-line `score_reason` naming the top 2
factors, with the authority level.
> Example: "Exact match + A Primary (official channel), published 8 days ago, 341k views"
> Example: "Exact match + C Community repository created 3 days ago, 163 stars"
