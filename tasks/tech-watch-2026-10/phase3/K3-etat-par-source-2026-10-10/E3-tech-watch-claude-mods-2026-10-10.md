# Tech Watch — Claude Mods
**Date**: 2026-10-10 | **Window**: 30 days | **Topic**: Claude Code mods (owner: Anthropic) | **Sources**: 20 ranked + 5 primary

| Source | Status | Raw | On-topic | In report |
|---|---|---|---|---|
| arXiv | empty | 0 | 0 | 0 |
| GitHub | degraded: GitHub token rejected (401); results fetched without authentication. Fallback `WebSearch` on github.com: 10 results, 6 new (2 of them Anthropic reference repositories) | 20 | 19 | 15 |
| YouTube | failed: YouTube API key not configured. Fallback `WebSearch` on youtube.com: 10 results, none rankable (no date, duration, views or channel available) | – | – | 0 |
| Web (Tier 2) | ok | 28 | 23 | 7 |
| Web (Tier 3) | not run (unique on-topic ≥ 12) | – | – | 0 |
| Owner domains | ok | 10 | – | 3 |

**Pipeline**: 68 raw → 62 on-topic, 0 adjacent, 5 homonyms, 1 dropped → 54 unique → 26 ≥ 60 → 20 ranked (cap 20).
**Enrichment**: 10/10 pages opened (3 primary), 0 failures, 2 truncated.
**Date test**: skipped (the Mods overview mentions an "early access" period without dating it; the changelog read was truncated before the entries that could date it).
**Notes**:
- Pipeline totals include the 20 fallback results (10 github.com, 10 youtube.com) and exclude the 10 owner-domain results, which are not labeled. Of the 54 unique items, 3 are primary (2 Anthropic repositories, the "Create a mod" docs page) and sit outside the ranking. The 2 Anthropic repositories came from the GitHub fallback, hence 5 primary sources for 3 in the Owner domains row.
- Cap cut 6 sources scoring 62–64: karanb192/awesome-claude-code-mods (456 stars, created 2026-09-15), JohnnyVizz/claude-kit, karanb192/claude-code-mods, darrell-tw/darrelltw-mods, galElmalah/claude-mods, hoobnn/awesome-claude-code-mods.
- Unopened pages cannot reach 60 (date and length `unverified` → 59 at best): 11 Tier 2 pages (4 Medium, 2 Substack, 1 dev.to, explainx, claudekit, braindetox, arte.itlibra), the ruvnet gist, issue anthropics/claude-code#91870, and all 10 YouTube fallback videos, including "Mods in Claude Code: change how Claude Code works" (https://www.youtube.com/watch?v=yUuFvL1lK4k), whose channel could not be verified as Anthropic's.
- Truncated reads: the Claude Code changelog (only 2.1.288–2.1.296 read, so the 2.1.287 launch entry was not seen) and the StationX guide (last 4% not read).
- Scoring interpretations: dev.to bylines show day and month only, year 2026 taken since the feature launched 2026-10-01; Kanaries is scored on its "Updated on" date; Developers Digest has no author on the page, authority `unverified` scored 0. Contradiction check was limited to titles and search snippets (step 8 extracts date, length and author only): none found among ranked sources. One unattributed github.com snippet states that mods are "still in early access" and need `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`, which the Mods overview contradicts (on by default, variable ignored since v2.1.287).

---

## Executive Summary
Anthropic launched mods for Claude Code on 2026-10-01: in-process JavaScript/TypeScript plugins ("function hooks") that can draw interface elements, rewrite or answer tool calls and prompts, and add commands, on by default from v2.1.287 in the terminal. Within ten days the ecosystem is dominated by small personal mod collections and several competing "awesome" catalogues, most of them created between 2026-10-02 and 2026-10-09, while the changelog shows near-daily mod API additions and guard-bypass fixes. The recurring tension across official and community sources is security: mods are not sandboxed and run with the user's full permissions, and the built-in organizational guard loads only on Team/Enterprise plans or managed machines.

---

## Primary sources

**Mods overview - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Establishes the definition (a plugin made of JS/TS event handlers running inside Claude Code), requirements (on by default; terminal v2.1.287 or later, Desktop app from v2.1.286), where mods run (CLI and Desktop Code tab draw; VS Code chat panel, `claude -p`, Agent SDK and cloud sessions run hooks without drawing), the security model (not sandboxed, runs with your permissions, `claude plugin validate` lists hooks and calls), and that the early-access variable `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` is ignored since v2.1.287.

**Customize Claude Code with mods in TypeScript** — 🔗 https://claude.com/resources/articles/claude-code-mods — 📅 2026-10-01
The announcement: "Today we're introducing mods", available in the Claude Code CLI and desktop app; mods are not sandboxed; on Team and Enterprise plans and on machines with managed settings the built-in `sec-default` mod loads first; `/diff` is now a mod.

**Claude Code changelog** — 🔗 https://code.claude.com/docs/en/changelog — 📅 2026-10-09 (latest entry read, 2.1.296)
Release notes 2.1.288 (2026-10-02) to 2.1.296 (2026-10-09) add mod APIs almost daily (`$.ui.selection`, `prompt.autocomplete`, prompt caching in `$.model.complete`, `isDeferred` in `$.tool.register`, `$.ui.notify`) and fix several cases where a user-installed mod could bypass or unload an organization's guard. Read truncated: the 2.1.287 entry was not seen.

**anthropics/claude-code-playground — claude-code/mods** — 🔗 https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods — 📅 unverified
Anthropic's sample mods referenced by the docs (`token-weather`, `blast-radius`, `replay-theater`), shared as they are, without support. Not opened; described from the Mods overview.

**anthropics/claude-code — mods** — 🔗 https://github.com/anthropics/claude-code/tree/main/mods — 📅 unverified
Public source of built-in mods (`diff`, `agents-md`, `sec-default`, `telemetry`), each a complete plugin with its hooks module and tests. Not opened; described from the Mods overview.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

No source reached 85.

---

### 🟠 High value (score 70–84)

**[1] Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples**
🔗 https://docs.kanaries.net/topics/AICoding/claude-code-mods
📅 2026-10-07 (updated; publication date not on page) | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Long tutorial (about 3,000 words) by Soren Atelier on Kanaries covering install options, the minimum version, how to test a mod, and 15 community examples. Its version claim (shipped in 2.1.287, on by default) matches the official docs.
**Score reason**: Exact match + C Community (company content site), updated 3 days ago, about 3,000 words
**Tags**: `tutorial`, `testing`, `community-examples`

**[2] Claude Code Mods Just Turned Agents Into a Platform**
🔗 https://dev.to/max_quimby/claude-code-mods-just-turned-agents-into-a-platform-5gc0
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Analysis by Max Quimby (originally published on AgentConn, original URL not retrieved) framing mods as middleware that intercepts tool calls and draws custom UI. Per the search snippet it takes a critical angle on the absence of a review process or sandbox.
**Score reason**: Exact match + C Community post, published 6 days ago, about 2,300 words
**Tags**: `analysis`, `platform`, `security`

**[3] Turning Claude Code into a Writing Harness with Claude Mods and an Output Style**
🔗 https://dev.to/shimo4228/turning-claude-code-into-a-writing-harness-with-claude-mods-and-an-output-style-1a73
📅 2026-10-03 | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Use-case write-up by Tatsuya Shimomoto combining mods with an output style to repurpose Claude Code for writing, with measurements taken on 2026-10-03. One of the few sources applying mods outside coding workflows.
**Score reason**: Exact match + C Community post, published 7 days ago, about 1,600 words
**Tags**: `use-case`, `writing`, `output-style`

**[4] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: "A collection of claude code mods" in TypeScript, 77 stars two days after creation. No further detail in the repository description.
**Score reason**: Exact match + C Community repository created 2 days ago, 77 stars
**Tags**: `mod-collection`, `typescript`

**[5] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 2026-10-03 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Collection of 100+ mods usable with Claude Code; the search snippet reports grouping into session, repository, workspace, utilities, workflow and desktop categories. Useful as a discovery index.
**Score reason**: Exact match + C Community repository created 7 days ago, 43 stars
**Tags**: `awesome-list`, `catalogue`

**[6] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Self-described evidence-graded index of Claude Code mods, plugins and hooks, in 20 languages, rebuilt every 2 hours. An automated catalogue rather than a hand-curated list.
**Score reason**: Exact match + C Community repository created 6 days ago, 39 stars
**Tags**: `awesome-list`, `automated-index`

**[7] promptadvisers/claude-mods-computer-use-threads**
🔗 https://github.com/promptadvisers/claude-mods-computer-use-threads
📅 2026-10-05 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Two mods: a Codex computer-use bridge and coordinated Claude sessions, with source, build prompts, setup and tests. Shows mods used for cross-agent and cross-session coordination.
**Score reason**: Exact match + C Community repository created 5 days ago, 11 stars
**Tags**: `multi-session`, `computer-use`, `codex`

**[8] aieo-product/claude_qamods**
🔗 https://github.com/aieo-product/claude_qamods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Mods that make Claude's questions easier to read and answer (qa-guide), targeting the AskUserQuestion dialog. An example of redrawing a part of Claude Code's own interface.
**Score reason**: Exact match + C Community repository created 6 days ago, 11 stars
**Tags**: `ui-redraw`, `askuserquestion`

**[9] AgriciDaniel/claude-mods-brain**
🔗 https://github.com/AgriciDaniel/claude-mods-brain
📅 2026-10-03 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Source-cited Obsidian knowledge base about Claude Code mods: how they work, how to build them, and how to check one before installing it. A documentation-style repository rather than code.
**Score reason**: Exact match + C Community repository created 7 days ago, 9 stars
**Tags**: `knowledge-base`, `obsidian`, `vetting`

**[10] ersinkoc/claude-mods**
🔗 https://github.com/ersinkoc/claude-mods
📅 2026-10-09 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: KOZMOS: live visual mods for Claude Code (CLI and desktop) with bands above the prompt, sidebars, a status ticker, companions, guards and sound. The most recent repository in the batch.
**Score reason**: Exact match + C Community repository created 1 day ago, 9 stars
**Tags**: `ui`, `mod-collection`, `desktop`

**[11] What are Claude Code mods? What they can draw and where they run in the desktop app**
🔗 https://dev.to/nakadadev/what-are-claude-code-mods-what-they-can-draw-and-where-they-run-in-the-desktop-app-58pc
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Explainer by Haruki Nakada focused on drawing capabilities and desktop behavior. Per the search snippet it notes that mods work in the terminal and the Desktop Code tab but not in the VS Code chat panel, and that the permission prompt cannot be redrawn, both consistent with the official docs.
**Score reason**: Exact match + C Community post, published 4 days ago, about 1,200 words
**Tags**: `explainer`, `desktop-app`, `ui`

**[12] Anthropic Launched Mods for Claude Code. Let's Build a Tiny One in TypeScript.**
🔗 https://dev.to/bobbyhalljr/anthropic-launched-mods-for-claude-code-lets-build-a-tiny-one-in-typescript-152h
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Hands-on walkthrough by Bobby Hall Jr building a minimal mod in TypeScript, about 1,200 words of prose plus code. A second worked example beside the official "Create a mod" tutorial.
**Score reason**: Exact match + C Community post, published 5 days ago, about 1,200 words
**Tags**: `tutorial`, `typescript`, `first-mod`

**[13] hamzafer/claude-code-mods**
🔗 https://github.com/hamzafer/claude-code-mods
📅 2026-10-02 (created) | ⭐ Authority: C Community | 📊 Score: 74/100
**Summary**: Plugins built on hooks that add live lines above the prompt, guards, panes and games: context bar, usage meter, Codex review watch, Markdown preview, Spotify now playing. The most starred of the personal collections created after launch.
**Score reason**: Exact match + C Community repository created 8 days ago, 177 stars
**Tags**: `mod-collection`, `typescript`, `ui`

**[14] Claude Code Mods: What They Are and How to Write One**
🔗 https://www.developersdigest.tech/blog/claude-code-mods-guide-2026
📅 2026-10-06 | ⭐ Authority: unverified | 📊 Score: 73/100
**Summary**: Guide explaining the three-file layout of a mod with a short example loaded through `--plugin-dir`. The search snippet describes it as a trimmed version of the official tutorial, so it may add little beyond the primary source.
**Score reason**: Exact match + authority unverified (no author on page, scored 0), published 4 days ago, about 1,800 words
**Tags**: `guide`, `file-layout`

**[15] zycck/claude-mods**
🔗 https://github.com/zycck/claude-mods
📅 2026-10-02 (created) | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Mods drawing live plan progress bars above the prompt. A single-purpose example of the band element.
**Score reason**: Exact match + C Community repository created 8 days ago, 42 stars
**Tags**: `band`, `progress-bar`

**[16] promptadvisers/claude-mods-starter-kit**
🔗 https://github.com/promptadvisers/claude-mods-starter-kit
📅 2026-10-02 (created) | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Ten mods with beginner guides, creation prompts, safe demos and a build-your-own template. Oriented toward generating mods by prompting rather than hand-writing them.
**Score reason**: Exact match + C Community repository created 8 days ago, 19 stars
**Tags**: `starter-kit`, `template`, `beginner`

**[17] nateherkai/claude-code-mods**
🔗 https://github.com/nateherkai/claude-code-mods
📅 2026-10-02 (created) | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Four mods: Cache Keeper, Recording Mode, Goal Meter and Collision Guard. Published the day after launch.
**Score reason**: Exact match + C Community repository created 8 days ago, 17 stars
**Tags**: `mod-collection`, `guards`

**[18] augiefra/claude-mods**
🔗 https://github.com/augiefra/claude-mods
📅 2026-10-02 (created) | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: One band above the prompt showing context in tokens, 5-hour and weekly limits against the clock, prompt cache countdown, session cost and running agents. Representative of the usage-monitoring mods that dominate the batch.
**Score reason**: Exact match + C Community repository created 8 days ago, 11 stars
**Tags**: `usage-meter`, `band`, `cost`

**[19] OneWave-AI/claude-code-mods**
🔗 https://github.com/OneWave-AI/claude-code-mods
📅 2026-10-02 (created) | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Ten open-source mods: live panes, bands, status lines and tool-call guards, including a burn meter, launch codes required before dangerous Bash commands, session wrapped, boss fight and code pet. Mixes utility and playful mods.
**Score reason**: Exact match + C Community repository created 8 days ago, 10 stars
**Tags**: `mod-collection`, `guards`, `gamification`

---

### 🟡 Worth including (score 60–69)

**[20] Claude Code Mods: The Complete Guide + 34 Videos (2026)**
🔗 https://app.stationx.net/articles/claude-code-mods
📅 unverified (page says "Updated October 2026") | ⭐ Authority: C Community | 📊 Score: 66/100
**Summary**: Very long guide (30-minute read) by Nathan House, founder of StationX, with a rollout timeline and a curated list of 34 videos. Per the search snippet it dates the launch to 2026-10-01 in v2.1.287 with a preview beforehand, consistent with the official sources; read truncated.
**Score reason**: Exact match + C Community (training company blog), about 10,000 words, date unverified
**Tags**: `guide`, `timeline`, `video-list`

---

## Trends identified

- Launch-driven burst: the announcement is dated 2026-10-01 and 14 of the 19 on-topic repositories returned by the GitHub tool were created between 2026-10-02 and 2026-10-09; three (karanb192 x2, darrell-tw, galElmalah) date from 2026-09-14 to 2026-09-16, consistent with the early-access period the docs mention without dating.
- Catalogues are appearing as fast as mods: at least four "awesome" indexes compete (karanb192, whyashthakker, wh000wh000, hoobnn), and two of them advertise scanning what each mod can read, write, run or send over the network, a community answer to the lack of sandboxing.
- Security is the common thread: the docs, the announcement and several community posts all stress that mods run unsandboxed with the user's permissions, and the changelog from 2.1.289 to 2.1.295 fixes multiple ways a user-installed mod could bypass or unload an organization's guard.
- The dominant mod type is a band above the prompt showing context, usage limits and cost (hamzafer, augiefra, zycck, OneWave-AI), followed by tool-call guards for risky shell commands, mirroring Anthropic's own samples `token-weather` and `blast-radius`.
- The API is moving quickly: new mod methods and events landed in almost every release between 2026-10-02 and 2026-10-09, so tutorials and collections from the first week may already lag the reference.

---

*Generated by tech-watch skill | Sources used: GitHub · Web (Tier 2) · Owner domains*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
