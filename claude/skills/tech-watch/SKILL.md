---
name: tech-watch
description: Technology monitoring (veille technologique) - multi-source search (arXiv, GitHub, YouTube, web), scoring and ranked Markdown report on a given tech topic. Use when the user asks for a tech watch or a curated survey of recent sources on a topic, in French or English - "fais-moi une veille sur X", "veille techno sur X", "qu'est-ce qui sort sur X en ce moment", "tech watch on X", "what's new around X this month", "curate recent sources on X". Do not use for a factual question ("What is RAG?"), summarizing content the user provides, a single-source lookup ("find me a YouTube video on X") or general news ("what happened in AI last week") - answer directly or use WebSearch alone.
context: fork
agent: tech-watch
---

# Tech Watch

Technology monitoring skill. Aggregates sources from curated channels, scores and ranks them, and produces a Markdown report optimized for NotebookLM import.

**Runtime**: the three `mcp__tech-watch__*` MCP tools (arXiv, GitHub, YouTube) + `WebSearch` / `WebFetch`. No Python script is executed.

---

## Workflow

### Step 1 - Normalize the topic, one query per tool
Reduce the request to a 2-4 word topic in English, then derive one query per tool (rules and parameters in `references/sources.yaml`, Tier 1). Quote only proper nouns and fixed expressions, never the whole query.

The normalized topic also gives the report's file slug, never the request as typed: lowercase, ASCII (accents stripped), every run of non-alphanumeric characters becomes one hyphen, no leading or trailing hyphen. "Claude Mods" and "les mods de Claude Code" both normalize to `Claude Code mods` and both give `claude-code-mods`.

| Request | Topic | arXiv | GitHub | YouTube |
|---|---|---|---|---|
| "latest stuff on AI agents and evaluation" | AI agent evaluation | `"agent evaluation"` + default categories | `agent evaluation framework` | `AI agent evaluation` |
| "veille sur les mods de Claude Code" | Claude Code mods | `"Claude Code" mods` (0 papers expected: accept) | `claude code mods` | `Claude Code mods` |

### Step 2 - Run Tier 1 tools (always)
Run the three MCP tools in parallel, each with its own query and with every parameter listed in `sources.yaml` passed explicitly (`max_results`, `days_back`, `categories`, `order`, `language`).
Default window: `days_back=30`. Use 60 for niche or slow-moving topics.

### Step 3 - Primary sources first (always)
Identify the owner of the topic: the vendor, maintainer or standards body (Anthropic for Claude Code mods, the Apache project for Iceberg, dbt Labs for dbt). Primary sources are its official documentation, its announcement or blog post, the reference repository or specification, and release notes.

- Run one `WebSearch` on the topic with `allowed_domains` restricted to the owner's domains (`references/sources.yaml`, `primary_sources`, lists known owners). If the owner is not known in advance, first run `{query} official documentation OR announcement` to find its domain.
- A localized page identifies the source: a result under `/docs/de/` designates the `/docs/en/` page; cite the English URL.
- Primary sources are opened first at step 8 (up to 3 of the 10 pages) and become the factual reference of the watch. They go in the report's `Primary sources` block, outside the ranking, with no threshold and no cap; if none exists, the block says so.

Contradictions, applied at step 9: a secondary source whose factual claim (version, availability, requirement, date) contradicts a primary source is **excluded** when the contradicted claim is in its title or is its main point, otherwise **kept and flagged** with a line `⚠️ Contradicts <primary>: <the point>` in its summary. Without an opened primary source, nothing is judged contradictory.

### Step 4 - Run Tier 2 web search (always)
Run the three `WebSearch` calls of `references/sources.yaml` (general, community with `allowed_domains`, practical).

### Step 5 - Quick relevance filter, then count
On title and description only (same reading as criterion 1 of the scoring grid), label every raw result from Tiers 1 and 2:
- **on-topic**: directly addresses the topic;
- **adjacent**: same field, different object (an agent framework, for a watch on agent evaluation);
- **off-topic**: word coincidence only. Two binary tests catch homonyms, results whose name matches the topic but not their object; both label the result `homonym`:
  - date test: when the topic is a dated thing (product, feature, version), the reference date is the **earliest** date a primary source of step 3 establishes for it: preview, early access or beta if documented, otherwise launch. Anything created or published before that date is off-topic. If a primary source mentions a preview or early-access period without dating it, skip the date test and rely on the meaning test alone. Not applicable to a practice or a concept.
  - meaning test: the description or metadata designates another object (`ccproxy` is a proxy; "Claude Models" is not "Claude Mods").

Drop at the same time, unlabeled: videos under 3 minutes (`duration_seconds` < 180: Shorts and teasers) and results without a usable title. Off-topic results leave the pipeline here: they are neither deduplicated nor scored. Keep the counts (raw, on-topic, adjacent, homonyms) for the report header.

### Step 6 - Deduplicate
One entry per content; keep the original, in English, under its canonical URL.
- Variants of one page: localized or translated pages, `.md` and HTML versions, mirrors, a personal post republished on dev.to or Medium, a re-uploaded video.
- Teaser and full version: a clip, trailer or excerpt of an episode or talk duplicates the full one; keep the full one.
- Same author, same topic: at most **2 entries per author, channel or organization** in the ranking; fold the others into the summary of the best-scored one ("companion repository: ...", "part 2 of the series").

A rewrite of an announcement or documentation without original content is not a duplicate: it is low-signal (authority D in the scoring grid).

### Step 7 - Run Tier 3 if unique on-topic < 12
Count unique on-topic results only; adjacent ones do not count. If fewer than 12, run the Tier 3 `WebSearch` calls of `references/sources.yaml` in priority order, filter and deduplicate each batch the same way, and stop as soon as the on-topic count reaches 12 or the list is exhausted. Ten off-topic results never replace Tier 3.

### Step 8 - Enrich web candidates (budgeted)
Only primary sources and on-topic web candidates from Tiers 2 and 3 are enriched. Never open Tier 1 results (github.com, youtube.com, arxiv.org): the tools already return their date, stars or views, duration and categories.

- Budget: **10 `WebFetch` per watch**, one per URL, no retry. A failure (403, network error, video page, commit history, unreadable content) consumes the budget and leaves the source `unverified`.
- Order: primary sources first (up to 3 of the 10 pages), then the candidates most likely to reach 60, official pages before blogs.
- Extract three values only: publication date, approximate length, author or organization. No summary at this step.
- A date is accepted from a Tier 1 tool output, from the fetched page itself, or from the URL path (`/2026/07/16/`). Anything else, including a plausible estimate or a search snippet, is not: write `unverified`. Same rule for length and authority.
- Keep the counts (pages opened out of the budget, failures) for the report header.

### Step 9 - Score and rank
Apply the scoring criteria in `references/scoring-criteria.md` to the on-topic results only, then the contradiction rule of step 3. Adjacent results are not ranked: list at most 3 of them apart, without a score.
Threshold: 60/100, strict. Cap: 20 sources. If fewer than 10 reach 60 after Tier 3, say so in a coverage note instead of filling in.

### Step 10 - Generate the Markdown report
Use the template in `references/report-template.md`. Its header is fixed: fill the source status table from what each tool and search actually returned at steps 2, 3, 4 and 7 (status vocabulary in the template), the `Pipeline` and `Enrichment` lines from the counts kept at steps 5 and 8, and derive the footer's `Sources used` from the table. Anything else goes under `Notes`.

- Filename: `tech-watch-{slug}-{YYYY-MM-DD}.md`, slug from step 1. When the window is not 30 days, insert `-{days}d` before the date: `tech-watch-ai-agent-evaluation-60d-2026-10-10.md`. Same name on the same day: the new report replaces the old one.
- Location: the output directory named by the agent you run in (`/home/martin/tech-watch/` in normal use), created if missing, unless the request names another directory.
- Language: the report is written in English whatever the language of the request (sources, template and scoring vocabulary are English). The chat summary is in the language of the request.

---

## Known limitations

Every line below was observed at least once on the 2026-10 eval runs
(`tasks/tech-watch-2026-10/`). Any row of the status table that is not `ok`
is named in the first line of your answer.

**MCP server and Tier 1 tools**
- Server unreachable: the three `mcp__tech-watch__*` tools are simply missing
  from your tool list, with no error anywhere. Continue with the web tiers and
  mark the three rows `absent`.
- GitHub token rejected (401): the server retries once without authentication
  (10 searches per minute instead of 30) and prefixes its results with
  `⚠️ GitHub token rejected (401) …`. The results are usable: row `degraded`,
  warning quoted in the status cell, rotation mentioned in your answer. Do not retry.
- YouTube key missing on the server: the tool returns `Error executing tool
  search_youtube_videos: YouTube API key not configured.` Row `failed`. The
  fallback `WebSearch` on `youtube.com` returns links without date, duration,
  views or channel: those videos stay `unverified`, cannot reach 60 and are not
  ranked. The official video, if any, is then only named in `Notes`, and the
  Essential band may be empty.
- arXiv returns 0 papers on product features and vendor tooling (Claude Code
  mods: 0 on every run). That is `empty`, not a failure: no retry, no wider query.

**Web search and pages**
- `WebFetch` is the only way to establish a date, length or author for a web
  result. Without it, or past the budget of 10 pages, web sources stay
  `unverified`, cap at 59 and are excluded, not judged poor. Say how many in `Notes`.
- A long page is read truncated after roughly 100,000 characters (the Claude
  Code changelog, about 1 MB, was read down to 2.1.288 only). Say what was not
  reached when it matters (a launch entry, a date).
- Reddit is not searched (API behind paid auth). dev.to, Medium, Substack and
  Hashnode are reached through Tier 2 only.

**Delivery**
- Under a natural-language trigger ("fais-moi une veille sur…"), the main
  session receives your `Report:` line as a tool result and rephrases it for
  the user (relative path observed). Under `/tech-watch …` it is delivered as is.
