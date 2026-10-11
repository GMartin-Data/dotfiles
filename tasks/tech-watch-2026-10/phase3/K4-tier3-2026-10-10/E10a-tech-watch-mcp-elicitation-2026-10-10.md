# Tech Watch — MCP elicitation
**Date**: 2026-10-10 | **Window**: 60 days | **Sources**: 20

**Pipeline counts**: 63 raw results | 38 on-topic | 16 adjacent | 4 off-topic | 5 videos under 3 min dropped | Tier 3 not run (on-topic >= 12)
**Queries**: arXiv `"Model Context Protocol" elicitation` (0 papers, accepted) | GitHub `mcp elicitation` | YouTube `MCP elicitation` | Web `MCP elicitation 2026`, `MCP elicitation` (community domains), `MCP elicitation tutorial OR guide`
**Notes**: the 60-day window (niche topic) applies to the arXiv, GitHub and YouTube tools; web search is not date-filtered, so older web articles appear with a freshness score of 0. GitHub dates are last-push dates. Summaries of repositories and videos rely on their title and description only; web articles marked "fetched" were read.

---

## Executive Summary
MCP elicitation (a server pausing a tool call to ask the user for input through the client) has moved from a novelty of the 2025-06-18 spec to an everyday building block: recent activity is dominated by small "ask the user" tools, test harnesses for human-in-the-loop flows, and short explainers, not by research (zero arXiv papers in the window). The two structuring themes are security (form mode for non-sensitive context, URL mode for secrets and OAuth) and the 2026-07-28 spec's stateless multi-round-trip flow, which changes how elicitation is carried on the wire. Unexpectedly, engagement is very low everywhere (repositories with 0-1 stars, videos under 100 views): scores are driven by relevance and freshness, not by proven adoption, so treat the top entries as early signals.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] elicitly/elicitly**
🔗 https://github.com/elicitly/elicitly
📅 2026-10-10 (last push; created 2026-08-03) | ⭐ Authority: High | 📊 Score: 90/100
**Summary**: Human-in-the-loop for prompts and Agent Skills built on MCP elicitation: a local MCP server (`npx -y elicitly`) plus an embeddable toolkit (`@elicitly/tools`). Shows elicitation being packaged as a reusable product layer rather than a per-server feature. 1 star only.
**Score reason**: Direct match on query + GitHub repo pushed today
**Tags**: `human-in-the-loop`, `agent-skills`, `typescript`

**[2] victorperr/jev-mcp-elicitation-autopilot**
🔗 https://github.com/victorperr/jev-mcp-elicitation-autopilot
📅 2026-10-07 (last push; created 2026-09-29) | ⭐ Authority: High | 📊 Score: 90/100
**Summary**: Fork of the MCP Inspector that tests MCP servers' human-in-the-loop flows in CI, with a simulated user (TypeSafe's Jev) answering elicitation requests. Addresses the testing gap created by interactive tool calls. 0 stars.
**Score reason**: Direct match on query + GitHub repo pushed 3 days ago
**Tags**: `testing`, `ci`, `mcp-inspector`

**[3] dominicfarr/mcp-secuirty-working-notes-example**
🔗 https://github.com/dominicfarr/mcp-secuirty-working-notes-example
📅 2026-10-06 (last push; created 2026-10-01) | ⭐ Authority: High | 📊 Score: 87/100
**Summary**: Simple reference on the MCP security model expressed through client policies and server elicitation. Relevant as a worked example of elicitation used as a control point rather than a UX feature. 1 star.
**Score reason**: Direct match on query + GitHub repo pushed 4 days ago
**Tags**: `security`, `client-policies`, `python`

---

### 🟠 High value (score 70–84)

**[4] MCP Elicitation Explained Simply - Should the AI Ask First?**
🔗 https://www.youtube.com/watch?v=oKgb-QClGHk
📅 2026-09-21 | ⭐ Authority: High | 📊 Score: 77/100
**Summary**: Short explainer (3:29, @codemakesense) framing elicitation as the missing "are you sure" step before destructive agent actions, using a bulk order-cancellation example. 57 views.
**Score reason**: Direct match on query + YouTube video from 19 days ago
**Tags**: `explainer`, `confirmation`, `video`

**[5] mappedsky/elicitationtestermcp**
🔗 https://github.com/mappedsky/elicitationtestermcp
📅 2026-09-13 (last push; created 2026-09-11) | ⭐ Authority: High | 📊 Score: 75/100
**Summary**: An MCP server written in Go whose only purpose is to test how clients handle elicitation. Useful to check actual client support, which remains uneven. 0 stars.
**Score reason**: Direct match on query + GitHub repo, pushed 27 days ago
**Tags**: `testing`, `client-support`, `go`

**[6] MCP Elicitation in Python | Get User Input Dynamically**
🔗 https://www.youtube.com/watch?v=CK8Ey4-d6K4
📅 2026-08-12 | ⭐ Authority: High | 📊 Score: 73/100
**Summary**: 52-minute tutorial (Programming Guide, "Mastering MCP" series #5) on how MCP servers request user input dynamically in Python. The only long-form video on the topic in the window. 18 views.
**Score reason**: Direct match on query + full-length YouTube tutorial
**Tags**: `tutorial`, `python`, `video`

**[7] MCP Client Architecture and Elicitation**
🔗 https://www.youtube.com/watch?v=xdtcBom2GfQ
📅 2026-09-10 | ⭐ Authority: High | 📊 Score: 72/100
**Summary**: 3-minute overview (CycloStack) of host / client / server roles that traces a form elicitation retry. Its description also speaks of "deprecated roots and sampling", a claim not checked against the specification here. 39 views.
**Score reason**: Direct match on query + YouTube video from 30 days ago
**Tags**: `architecture`, `form-mode`, `video`

**[8] MCP elicitation explained (Nango)**
🔗 https://nango.dev/blog/mcp-elicitation-explained
📅 2026-09-11 | ⭐ Authority: Medium | 📊 Score: 70/100
**Summary**: Fetched, about 2,700 words. Covers the accept / decline / cancel responses, form mode (non-sensitive structured data via a restricted JSON Schema) and URL mode (external page for OAuth or secrets), using the 2026-07-28 spec's multi-round-trip pattern. Gives the timeline: form mode in 2025-06-18, URL mode in 2025-11-25, both supported in 2026-07-28.
**Score reason**: Direct match on query + in-depth vendor blog post (> 1500 words)
**Tags**: `form-mode`, `url-mode`, `spec-2026-07-28`

**[9] blhsing/codex-ask-user**
🔗 https://github.com/blhsing/codex-ask-user
📅 2026-08-18 (last push; created 2026-08-06) | ⭐ Authority: High | 📊 Score: 70/100
**Summary**: Brings native structured clarification questions to Codex via MCP elicitation. Illustrates the "ask-user tool" pattern being ported across coding agents. 0 stars.
**Score reason**: Direct match on query + GitHub implementation (older than 30 days)
**Tags**: `ask-user`, `codex`, `typescript`

**[10] m-doughty/MCP-Server-Tool-Ask**
🔗 https://github.com/m-doughty/MCP-Server-Tool-Ask
📅 2026-08-21 (last push; created 2026-08-09) | ⭐ Authority: High | 📊 Score: 70/100
**Summary**: Ask-the-user tool for the Raku `MCP::Server` library, built on server-side elicitation. Same pattern as [9], showing spread into smaller language ecosystems. 0 stars.
**Score reason**: Direct match on query + GitHub implementation (older than 30 days)
**Tags**: `ask-user`, `raku`, `server-side`

**[11] achappey/aihappey-mcp** (adjacent)
🔗 https://github.com/achappey/aihappey-mcp
📅 2026-10-10 (last push; created 2025-12-22) | ⭐ Authority: High | 📊 Score: 70/100
**Summary**: C# MCP backend for 400+ AI and business integrations where elicitation is one listed capability among tools, resources and unified auth. Not about elicitation itself; kept as an example of elicitation inside a large integration backend. 1 star.
**Score reason**: Adjacent topic, compensated by a GitHub repo pushed today
**Tags**: `adjacent`, `dotnet`, `integrations`

---

### 🟡 Worth including (score 60–69)

**[12] artemreva-hub/Otus.AI_For_Dev.Webinar14.MCP**
🔗 https://github.com/artemreva-hub/Otus.AI_For_Dev.Webinar14.MCP
📅 2026-08-19 (last push) | ⭐ Authority: High | 📊 Score: 67/100
**Summary**: Webinar companion code: an MCP server example combining elicitation and an MCP App. Small teaching sample. 0 stars.
**Score reason**: Direct match on query + GitHub source (older than 30 days)
**Tags**: `example`, `mcp-apps`, `typescript`

**[13] Sankarpratapsamanta/MCP_Elicitation**
🔗 https://github.com/Sankarpratapsamanta/MCP_Elicitation
📅 2026-08-15 (last push) | ⭐ Authority: High | 📊 Score: 67/100
**Summary**: Python repository named after the feature, with no description; content not inspected, relevance inferred from the name alone. 0 stars.
**Score reason**: Direct match on title + GitHub source (older than 30 days)
**Tags**: `example`, `python`, `unverified-content`

**[14] What is MCP Elicitation?**
🔗 https://www.youtube.com/watch?v=sxs4E6p3aFQ
📅 2026-08-31 | ⭐ Authority: High | 📊 Score: 67/100
**Summary**: 3:48 definition video (Standarity) on a tool server pausing mid-request. Its description dates elicitation to "the July 2026 update", which contradicts the other sources (introduced in 2025-06-18): treat its chronology with caution. 75 views.
**Score reason**: Direct match on query + YouTube source (older than 30 days, short)
**Tags**: `explainer`, `video`, `date-discrepancy`

**[15] MCP Elicitation — How A Tool Asks The User Mid-Run**
🔗 https://www.youtube.com/watch?v=b0TGe3pzldM
📅 2026-08-21 | ⭐ Authority: High | 📊 Score: 67/100
**Summary**: 3:53 breakdown (THE NBX STUDIO) of elicitation's two modes, starting from the case of a tool needing an API key that must not be requested in chat. 19 views.
**Score reason**: Direct match on query + YouTube source (older than 30 days, short)
**Tags**: `two-modes`, `secrets`, `video`

**[16] MCP Elicitation Security: Forms for Context, URLs for Secrets**
🔗 https://www.youtube.com/watch?v=zdZIWt1cCcQ
📅 2026-09-02 | ⭐ Authority: High | 📊 Score: 67/100
**Summary**: 4:06 explainer (Tertiary Courses) on choosing between the two input paths, warning that the wrong one sends a secret through the agent client. 7 views.
**Score reason**: Direct match on query + YouTube source (older than 30 days, short)
**Tags**: `security`, `url-mode`, `video`

**[17] MCP Elicitation: Human-in-the-Loop for MCP Servers**
🔗 https://dev.to/kachurun/mcp-elicitation-human-in-the-loop-for-mcp-servers-m6a
📅 2025-08-14 | ⭐ Authority: Medium | 📊 Score: 67/100
**Summary**: Fetched. Argues elicitation avoids splitting human-in-the-loop logic across frontend and backend tools, then builds a Mastra server plus assistant-ui chat demo asking accept / decline before dangerous shell commands; notes production needs shared storage for pending requests. Also republished on DZone (duplicate removed). Predates URL mode and the 2026-07-28 flow.
**Score reason**: Direct match on query + full tutorial on a community blog (outside window)
**Tags**: `tutorial`, `mastra`, `human-in-the-loop`

**[18] MCP URL-mode elicitation (WorkOS)**
🔗 https://workos.com/blog/mcp-url-mode-elicitation
📅 2026-01-09 | ⭐ Authority: Medium | 📊 Score: 65/100
**Summary**: Fetched, about 1,900 words. Explains URL mode: the user is sent to an external page for OAuth, credentials or payments so the data never crosses the client; the client's "accept" only confirms the request was presented, so the server must track completion itself. Tied to the 2025-11-25 spec update.
**Score reason**: Direct match on query + in-depth vendor blog post (outside window)
**Tags**: `url-mode`, `oauth`, `security`

**[19] How To Implement Elicitation With Model Context Protocol (The New Stack)**
🔗 https://thenewstack.io/how-to-implement-elicitation-with-model-context-protocol/
📅 2025-08 (per search summary; page body could not be fetched) | ⭐ Authority: Medium | 📊 Score: 65/100
**Summary**: Hands-on Python tutorial on accepting user input through elicitation instead of hard-coded tool parameters, including a client routing elicitation requests to a handler. Date and content come from the search result summary only.
**Score reason**: Direct match on query + full tutorial on a quality publication (outside window)
**Tags**: `tutorial`, `python`, `unverified-date`

**[20] MCP is dead (again)** (adjacent)
🔗 https://www.youtube.com/watch?v=gvVSLAMx4Wk
📅 2026-09-28 | ⭐ Authority: High | 📊 Score: 62/100
**Summary**: 4:45 commentary (Rafal Wilinski) on the recurring "MCP is dead" claims. Not about elicitation; returned by the elicitation query and kept only as ecosystem context. 71 views.
**Score reason**: Adjacent topic + YouTube video from 12 days ago
**Tags**: `adjacent`, `ecosystem`, `video`

---

## Trends identified

- **Elicitation is being productized as a generic "ask the user" tool**: [1], [9] and [10] all wrap it into a reusable clarification tool for different hosts and languages (Agent Skills, Codex, Raku), rather than using it ad hoc inside one server.
- **Testing interactive flows is the new pain point**: two independent projects created in September 2026 ([2], [5]) target automated or client-side testing of elicitation, which suggests client support is still uneven enough to need verification.
- **Security framing dominates the explanations**: [3], [8], [15], [16] and [18] converge on the same rule (form mode for non-sensitive context, URL mode for secrets, OAuth and payments). Two 2026 MCP Dev Summit sessions (New York in April, Mumbai in June; below threshold, not listed) treat elicitation as a governance and authorization issue.
- **The 2026-07-28 spec changes the transport of elicitation**: [8] describes a multi-round-trip pattern, and adjacent results (a "stateless MCP" demo with signed request state, an "MRTR elicitation" demo, a Japanese article on the stateless-first release candidate) point the same way: the server returns an input-required result and the client resends the call, instead of a server-initiated request on an open stream. Not verified against the official specification in this run; pre-2026 tutorials ([17], [19]) describe the older flow.
- **No research and almost no engagement**: 0 arXiv papers in 60 days, repositories at 0-1 stars, videos mostly under 100 views. The topic lives in practitioner content; the highest-ranked sources are fresh, not validated by adoption.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
