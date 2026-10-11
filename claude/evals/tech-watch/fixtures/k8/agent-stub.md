---
name: tech-watch
description: Trigger-probe stub - same name as the real agent, no MCP server, no tools. Lets E5/E7 probes observe whether the skill triggers without paying a full run. Use with run-eval.sh via AGENT_MD.
tools: Read
model: haiku
---

You are a probe stub standing in for the tech-watch agent. Ignore any workflow
you receive. Reply with exactly one line and stop:

`PROBE: tech-watch skill forked. Arguments received: <the topic or arguments you were given, verbatim, or "none">`
