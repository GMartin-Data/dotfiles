---
name: tech-watch-probe
description: K12 probe - checks whether the inline MCP server of the tech-watch subagent is connected when this skill forks into it.
context: fork
agent: tech-watch
---

Do exactly this, nothing else:

1. Under a heading `TOOLS`, list the name of every tool available to you, one per line.
2. Call the tool `mcp__tech-watch__search_github_repos` with `query="dbt"` and `max_results=1`.
   Under a heading `RESULT`, paste the tool's raw output verbatim.
   If the tool does not exist or the call fails, write `RESULT: UNAVAILABLE - <reason>` instead.
