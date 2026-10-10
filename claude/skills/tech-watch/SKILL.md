---
name: tech-watch
description: Technology monitoring - curated source search and scored ranking for a given tech topic.
context: fork
agent: tech-watch
---

# Tech Watch

Technology monitoring skill. Aggregates sources from curated channels, scores and ranks them, and produces a Markdown report optimized for NotebookLM import.

**Runtime**: the three `mcp__tech-watch__*` MCP tools (arXiv, GitHub, YouTube) + `WebSearch` / `WebFetch`. No Python script is executed.

---

## Workflow

### Step 1 - Normalize the query
Reduce to 2-4 focused keywords before running any tool.
> "latest stuff on AI agents and evaluation" -> "AI agent evaluation"

### Step 2 - Run Tier 1 tools (always)
Run the three MCP tools in parallel with the normalized query.
Default window: `days_back=30`. Use 60 for niche or slow-moving topics.

### Step 3 - Run Tier 2 web search (always)
Run 2-3 web searches after Tier 1. See `references/sources.yaml` for recommended queries.

### Step 4 - Run Tier 3 if needed
If Tier 1 + 2 return fewer than 12 relevant results, fetch directly from extended sources listed in `references/sources.yaml`.

### Step 5 - Deduplicate
Remove results pointing to the same content on different URLs. Keep the most authoritative URL.

### Step 6 - Score and rank
Apply the scoring criteria in `references/scoring-criteria.md`.
Minimum threshold: 60/100. Target: 15-20 sources in the final report.

### Step 7 - Generate the Markdown report
Use the template in `references/report-template.md`.
Output filename: `tech-watch-{query}-{date}.md`

---

## Negative cases - do NOT trigger this Skill

- "Summarize this document" -> work with provided content directly
- "What is RAG?" -> factual question, answer directly without search
- "Find me a YouTube video on X" -> single-source lookup, use `WebSearch` only
- "What happened in AI last week?" -> use `WebSearch` only, no full curation workflow needed

---

## Known limitations

- GitHub MCP tool requires auth token for > 60 req/hour; unauthenticated calls may fail silently - fall back to `WebSearch` site:github.com
- arXiv MCP tool may return a redirect error (HTTP 301) - known server issue, not a query problem; retry once or use `WebSearch` site:arxiv.org
- YouTube MCP tool depends on server index; videos < 48h old may not appear - fall back to `WebSearch` site:youtube.com "{query}"
- Paywalled content (Nature, IEEE, ACM) returns title/abstract only
- Reddit excluded: API requires paid auth since 2023
- If the three `mcp__tech-watch__*` tools are absent from your tool list (MCP server not connected) or all fail, continue with Tier 2 + Tier 3 web search only. Say so in the first line of your answer, and add a "Degraded mode" note in the report header (next to Sources count) naming the tools that were unavailable.
