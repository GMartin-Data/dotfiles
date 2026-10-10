---
name: tech-watch
description: K12 probe agent - declares the tech-watch MCP server inline so that a forked skill can reach it without any session-level declaration.
tools: mcp__tech-watch__*, WebSearch, Read
model: opus
mcpServers:
  - tech-watch:
      type: sse
      url: https://tech-watch-mcp-ocbwcs6sjq-ew.a.run.app/sse
---

You are the tech-watch probe agent. Follow the instructions you receive exactly, nothing more.
