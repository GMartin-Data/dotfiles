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

### Step 3 - Run Tier 2 web search (always)
Run the three `WebSearch` calls of `references/sources.yaml` (general, community with `allowed_domains`, practical).

### Step 4 - Run Tier 3 if needed
If Tier 1 + 2 return fewer than 12 relevant results, run the Tier 3 `WebSearch` calls of `references/sources.yaml`, highest priority first.

### Step 5 - Deduplicate
Remove results pointing to the same content on different URLs. Keep the most authoritative URL.

### Step 6 - Score and rank
Apply the scoring criteria in `references/scoring-criteria.md`.
Minimum threshold: 60/100. Target: 15-20 sources in the final report.

### Step 7 - Generate the Markdown report
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
