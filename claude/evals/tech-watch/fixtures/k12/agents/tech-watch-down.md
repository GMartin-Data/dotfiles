---
name: tech-watch
description: K12 probe agent, server-down variant - same stdio bridge as the real agent, but the SSE URL points to an unreachable host.
tools: mcp__tech-watch__*, WebSearch, Read
model: opus
mcpServers:
  - tech-watch:
      type: stdio
      command: sh
      args: ["-c", 'API_ACCESS_TOKEN="${TECH_WATCH_MCP_TOKEN:?TECH_WATCH_MCP_TOKEN is not set}" exec uvx mcp-proxy@0.13.0 https://tech-watch-mcp-down.invalid/sse']
---

You are the tech-watch probe agent. Follow the instructions you receive exactly, nothing more.
