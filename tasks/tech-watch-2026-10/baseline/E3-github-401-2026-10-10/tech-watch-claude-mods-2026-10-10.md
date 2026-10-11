# Tech Watch — Claude Mods
**Date**: 2026-10-10 | **Window**: 30 days | **Sources**: 19 | **Partially degraded mode**: YouTube MCP unavailable (API key not configured) — videos sourced indirectly through a third-party index; GitHub MCP token rejected (401), results fetched unauthenticated; arXiv returned 0 papers.

> **Scoring notes**
> - First-party Anthropic docs/blog are scored as high authority (20 pts). The rubric only names arXiv/GitHub/YouTube for that band; this is an interpretation.
> - YouTube entries [6], [10], [15] and Anthropic repos [5], [11] were not queried directly: dates, views and stars are partly unverified, and freshness is scored conservatively (15 pts, i.e. "around launch").
> - Web articles [16] and [19] were scored from search snippets only (not fetched); exact dates not confirmed.

---

## Executive Summary
"Claude Mods" is the Claude Code extension mechanism that went generally available on 2026-10-01 (CLI v2.1.287, previewed in September as "Function Hooks"): JavaScript/TypeScript handlers shipped inside plugins that run *in-process* and can observe, rewrite or take over tool calls, prompts and UI rendering. In nine days a community ecosystem has formed on GitHub (catalogues, starter kits, dozens of "band above the prompt" meters and guards), while almost every serious write-up converges on the same caveat: mods are not sandboxed and run with the user's full permissions. The unexpected finding is how quickly the conversation moved from "what can I build" to supply-chain governance — capability-scanned catalogues and `claude plugin validate` audits appeared within the first week, and there is no academic literature yet.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] karanb192/awesome-claude-code-mods**
🔗 https://github.com/karanb192/awesome-claude-code-mods
📅 Created 2026-09-15, last push 2026-10-10 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Community catalogue of public Claude Code mods scanned from GitHub, listing for each mod what it can read, write, run or send over the network (browsable at mods.aidojo.si). The most-starred mods repository (449★) and the closest thing to a capability-audited index.
**Score reason**: Exact match on query + pushed today, highest star count in the niche
**Tags**: `catalogue`, `security-audit`, `awesome-list`

**[2] hamzafer/claude-code-mods**
🔗 https://github.com/hamzafer/claude-code-mods
📅 Created 2026-10-02, last push 2026-10-09 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: A working collection of mods (context bar, usage meter, Codex review watch, Markdown preview, Spotify now-playing, guards, panes, games). Good representative sample of what the community actually builds with the API (172★).
**Score reason**: Exact match, actively pushed within 7 days, concrete TypeScript implementations
**Tags**: `mods-collection`, `typescript`, `ui-bands`

**[3] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 Created 2026-10-04, last push 2026-10-10 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: "Evidence-graded" index of Claude Code mods, plugins and hooks, published in 20 languages and rebuilt every 2 hours. Complements [1] with an automated, graded view of the ecosystem (39★).
**Score reason**: Exact match + pushed today on GitHub
**Tags**: `catalogue`, `automated-index`, `awesome-list`

**[4] karanb192/claude-code-mods**
🔗 https://github.com/karanb192/claude-code-mods
📅 Created 2026-09-15, last push 2026-10-03 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: "Claude Mods and the tools to build them": a builder skill first, then mods. Dates back to the early-access (function hooks) period, so it shows the authoring workflow before and after GA (40★).
**Score reason**: Exact match + GitHub repo pushed within 7 days
**Tags**: `builder-skill`, `function-hooks`, `authoring`

**[5] anthropics/claude-code — `mods/` (source of built-in mods)**
🔗 https://github.com/anthropics/claude-code/tree/main/mods
📅 ~2026-10-01 (not verified) | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Public source of four of Claude Code's own built-in mods — `diff` (the `/diff` pane), `agents-md`, `sec-default` (the organisation policy guard) and `telemetry` — each a complete plugin with hooks module and tests. Reference implementations, and `sec-default` is the model for a policy-enforcing mod.
**Score reason**: First-party reference code for the exact topic, in a heavily starred repo
**Tags**: `first-party`, `reference-implementation`, `sec-default`

**[6] Claude Mods Is The Biggest Claude Code Upgrade Since Skills — Chase AI**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 Early October 2026 (exact date not verified) | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: The most-viewed video on the feature found in this run (174k views per the StationX index). Useful as the reference for how mods are being framed to the practitioner audience ("since Skills").
**Score reason**: Exact match + 174k views; duration unknown so depth scored low
**Tags**: `youtube`, `overview`, `practitioner`

**[7] Mods overview — Claude Code documentation**
🔗 https://code.claude.com/docs/en/plugins/mods
📅 ~2026-10-01 (living doc) | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: The canonical definition: a mod is a plugin whose hooks module registers handlers that can observe, rewrite or answer events. Covers what a mod can reach (files, secrets, session, auto-approval, model usage), where mods run (CLI and Desktop draw; VS Code, `claude -p`, cloud run hooks but draw nothing), how to turn them off (`--safe-mode`, `disableAllHooks`), built-in mods, and a mod vs settings hook vs skill vs MCP comparison table.
**Score reason**: Primary source, exact match, full technical depth
**Tags**: `official-docs`, `security-model`, `architecture`

**[8] Create a mod — Claude Code documentation**
🔗 https://code.claude.com/docs/en/plugins/mods/create
📅 ~2026-10-01 (living doc) | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Official tutorial building `first-mod`: counts tool calls, shows the count beside the spinner, adds a `/tally` command. Also documents the "ask Claude for a mod" route via the built-in `plugin-authoring` skill, reading generated type declarations, and `claude plugin validate`.
**Score reason**: Primary-source full tutorial on the exact topic
**Tags**: `official-docs`, `tutorial`, `plugin-authoring`

**[9] AgriciDaniel/claude-mods-brain**
🔗 https://github.com/AgriciDaniel/claude-mods-brain
📅 Created 2026-10-03, last push 2026-10-03 | ⭐ Authority: High | 📊 Score: 87/100
**Summary**: Source-cited Obsidian knowledge base about Claude Code mods: how they work, how to build them, how to vet one before installing. Low stars (9) but a format that maps directly onto NotebookLM ingestion.
**Score reason**: Exact match + 7-day-old GitHub repo; low engagement
**Tags**: `knowledge-base`, `obsidian`, `vetting`

**[10] The Future of Claude Code: Mods, Mutable Software, & Multiplayer Agents — Latent Space**
🔗 https://www.youtube.com/watch?v=IZAlq-V19U8
📅 ~2026-09-29, two days before launch (not verified directly) | ⭐ Authority: High | 📊 Score: 85/100
**Summary**: Pre-launch Latent Space episode framing mods within a larger "mutable software" direction for Claude Code. The only source in the set aimed at design intent and roadmap rather than how-to.
**Score reason**: Exact match from a high-signal channel; view count and length not verified
**Tags**: `youtube`, `podcast`, `product-direction`

**[11] anthropics/claude-code-playground — sample mods**
🔗 https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods
📅 ~2026-10-01 (not verified) | ⭐ Authority: High | 📊 Score: 85/100
**Summary**: Anthropic's unsupported sample mods, each a complete plugin with a README on how it was built: `token-weather` (context forecast band), `blast-radius` (holds `rm -rf`/force-push and shows impact), `replay-theater` (`/replay` of last turn's edits). Loadable with `--plugin-dir`.
**Score reason**: First-party sample code, exact match; engagement not measured
**Tags**: `first-party`, `samples`, `guards`

**[12] Claude Code Mods: The Complete Guide + 34 Videos (2026) — StationX**
🔗 https://app.stationx.net/articles/claude-code-mods
📅 Updated 2026-10 (fact-checked 2026-10-05) | ⭐ Authority: Medium | 📊 Score: 85/100
**Summary**: ~6–7k-word guide synthesising the official docs, 34 YouTube videos and the author's own mods. Argues for the lightest tool first (instruction → setting/status line → settings hook → mod), includes a force-push guard lab, and flags that the widely repeated Pluto Security findings were made on a pre-release build (2.1.274). Notes `sec-default` only loads on managed/Team/Enterprise setups.
**Score reason**: Exact match + long, fact-checked tutorial under 7 days old
**Tags**: `guide`, `security`, `video-index`

**[13] Claude Code Mods Just Turned Agents Into a Platform — Max Quimby (DEV)**
🔗 https://dev.to/max_quimby/claude-code-mods-just-turned-agents-into-a-platform-5gc0
📅 2026-10-04 | ⭐ Authority: Medium | 📊 Score: 85/100
**Summary**: Analytical piece: mods make the harness, not the model, the product, and the situation resembles early npm ("velocity first, governance later") more than an App Store. Points out there is no sandbox, review or signing, that `validate` does not check behaviour, and cites a study in which 26.1% of 31,132 agent skills had at least one vulnerability. Recommends private marketplaces and SHA pinning for teams.
**Score reason**: Exact match + ~2,500-word analysis published 6 days ago
**Tags**: `analysis`, `supply-chain`, `platform`

---

### 🟠 High value (score 70–84)

**[14] Customize Claude Code with mods — Anthropic blog**
🔗 https://claude.com/blog/claude-code-mods
📅 2026-10-01 | ⭐ Authority: High | 📊 Score: 82/100
**Summary**: The launch announcement. States that mods can run before/after/instead of/around events, rewrite prompts, block/rewrite/retry tool calls, approve or deny permissions, redact secrets, stack by load order and hot-reload; that built-ins like `/diff` now ship as mods; and that `sec-default` loads first on Team/Enterprise and managed installs.
**Score reason**: Primary announcement, exact match; short post, 9 days old
**Tags**: `announcement`, `first-party`, `admin-controls`

**[15] Anthropic Just Opened Up Claude Code — Mods vs Hooks vs Skills vs MCP — Solo Swift Crafter**
🔗 https://www.youtube.com/watch?v=bgJoDD8BYyc
📅 Early October 2026 (exact date not verified) | ⭐ Authority: High | 📊 Score: 82/100
**Summary**: Video focused on the positioning question most newcomers ask: when a mod is the right tool versus a settings hook, a skill or an MCP server. Pairs with the comparison table in [7].
**Score reason**: Exact match on YouTube; views and duration not verified
**Tags**: `youtube`, `comparison`, `hooks-vs-mods`

**[16] Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples — Kanaries**
🔗 https://docs.kanaries.net/topics/AICoding/claude-code-mods
📅 Early October 2026 (exact date not verified) | ⭐ Authority: Medium | 📊 Score: 80/100
**Summary**: Hands-on tutorial with a tested run: a command guard, a turn meter above the prompt and a `/pyenv` command, all passing `claude plugin validate` and 8 automated tests under `claude plugin test`. One of the few third-party guides that covers the testing loop.
**Score reason**: Exact match + full tutorial with test evidence
**Tags**: `tutorial`, `testing`, `community-examples`

**[17] JohnnyVizz/claude-kit**
🔗 https://github.com/JohnnyVizz/claude-kit
📅 Created 2026-10-04, last push 2026-10-04 | ⭐ Authority: High | 📊 Score: 79/100
**Summary**: Public bundle of Claude Code skills *and* mods (119★ in six days). Illustrates the emerging packaging pattern where mods ship alongside skills in one plugin kit rather than standalone.
**Score reason**: GitHub repo under 7 days old with fast traction; mods are only part of scope
**Tags**: `kit`, `skills-plus-mods`, `typescript`

---

### 🟡 Worth including (score 60–69)

**[18] Claude Code Mods: What They Can Do and What They Can Reach — CellCog**
🔗 https://cellcog.ai/blog/claude-code-mods/
📅 2026-10-02 | ⭐ Authority: Low | 📊 Score: 68/100
**Summary**: Compact (~1,100 words) restatement of the reach of a loaded mod and the documented controls (`validate`, `--safe-mode`, `disableAllHooks`, admin restrictions). Vendor blog with product promotion throughout; useful mainly as a short security digest.
**Score reason**: Exact match but short, promotional vendor post
**Tags**: `security`, `summary`, `vendor-blog`

**[19] Claude Code Gets Mods, Plugins That Rewrite the Agent — Pasquale Pillitteri**
🔗 https://pasqualepillitteri.it/en/news/19871/claude-code-mods-plugins
📅 Early October 2026 (exact date not verified) | ⭐ Authority: Low | 📊 Score: 68/100
**Summary**: News write-up that reports an early-access community review in which 14 of 31 public mods were capable of executing host processes, and notes the public source of Anthropic's four built-in mods. The figure is second-hand and should be traced to its origin before reuse.
**Score reason**: Exact match news piece; general-web authority, short
**Tags**: `news`, `early-access-audit`, `security`

---

## Trends identified

- **Security is the dominant frame, not capability.** Official docs, the launch post and every independent write-up lead with the same facts: no sandbox, full user permissions, ability to pre-approve tool calls and read secrets. The only hard limit repeatedly cited is that a mod cannot alter the permission prompt.
- **Audit tooling emerged with the ecosystem, not after it.** The top community repos are capability-scanned or evidence-graded catalogues rather than plain awesome-lists, and `claude plugin validate` (lists hooks and API calls statically) is the common vetting step — with several authors noting it shows what a mod *can* do, not what it does.
- **Most community mods are observability UI.** GitHub activity clusters on bands above the prompt (context/usage/cost meters, plan progress, cache countdown) and tool-call guards for destructive commands; behaviour-rewriting mods (model routing, prompt rewriting) are discussed far more than they are published.
- **Mods are positioned as the last resort in the extension ladder.** Both Anthropic's comparison table and third-party guides recommend instructions, settings hooks, skills or MCP first; a mod is justified by in-process state, drawing UI, or taking over an event.
- **Platform narrative, zero research coverage.** Commentary treats this as the harness becoming the product (built-ins such as `/diff` are now replaceable mods; "early npm" analogies), while arXiv has nothing on the topic yet and enterprise governance (`sec-default`, managed marketplaces, `allowManagedModsOnly`) is documented but little tested in public.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
