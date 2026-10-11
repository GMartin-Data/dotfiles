---
name: tech-watch
description: K12 probe agent - declares the tech-watch MCP server inline (same stdio bridge and bearer as the real agent) so that a forked skill can reach it without any session-level declaration. Needs TECH_WATCH_MCP_TOKEN in the environment; without it the tools are absent.
tools: mcp__tech-watch__*, WebSearch, Read
model: opus
mcpServers:
  - tech-watch:
      type: stdio
      command: sh
      args: ["-c", 'API_ACCESS_TOKEN="${TECH_WATCH_MCP_TOKEN:?TECH_WATCH_MCP_TOKEN is not set}" exec uvx mcp-proxy@0.13.0 https://tech-watch-mcp-ocbwcs6sjq-ew.a.run.app/sse']
---

You are the tech-watch probe agent. Follow the instructions you receive exactly, nothing more.
