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
Reduce the request to a 2-4 word topic, then derive one query per tool (rules and parameters in `references/sources.yaml`, Tier 1). Quote only proper nouns and fixed expressions, never the whole query.

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
- **off-topic**: word coincidence only (homonyms, repositories that predate the feature).

Drop at the same time, unlabeled: videos under 3 minutes (`duration_seconds` < 180: Shorts and teasers) and results without a usable title. Off-topic results leave the pipeline here: they are neither deduplicated nor scored. Keep the three counts (raw, on-topic, adjacent) for the report header.

### Step 6 - Deduplicate
Remove results pointing to the same content on different URLs. Keep the most authoritative URL.

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
Use the template in `references/report-template.md`.
Output filename: `tech-watch-{query}-{date}.md`

---

## Known limitations

- GitHub MCP tool requires auth token for > 60 req/hour; unauthenticated calls may fail silently - fall back to `WebSearch` site:github.com
- arXiv MCP tool may return a redirect error (HTTP 301) - known server issue, not a query problem; retry once or use `WebSearch` site:arxiv.org
- YouTube MCP tool depends on server index; videos < 48h old may not appear - fall back to `WebSearch` site:youtube.com "{query}"
- Paywalled content (Nature, IEEE, ACM) returns title/abstract only
- Reddit excluded: API requires paid auth since 2023
- If the three `mcp__tech-watch__*` tools are absent from your tool list (MCP server not connected) or all fail, continue with Tier 2 + Tier 3 web search only. Say so in the first line of your answer, and add a "Degraded mode" note in the report header (next to Sources count) naming the tools that were unavailable.
