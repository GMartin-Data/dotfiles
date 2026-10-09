# Tech Watch — Claude Mods
**Date**: 2026-10-09 | **Window**: 30 days | **Sources**: 20

> Tier 1: GitHub (20 hits), YouTube (15 hits), arXiv (0 hits — no research papers on the topic yet). Tier 2: 3 web searches + 1 targeted security search. Tier 3 not needed. Localized doc pages and duplicate repos by the same author were deduplicated.

---

## Executive Summary
"Claude Mods" are a new Claude Code extension mechanism: JavaScript/TypeScript event handlers, shipped inside plugins, that run in Claude Code's own process and can observe, rewrite or take over tool calls, prompts and UI rendering. After a September early-access phase under the name "function hooks", the feature went on by default on 2026-10-01 (CLI v2.1.287, Desktop v2.1.286), and a community ecosystem appeared within days: catalogues, starter kits, and a wave of "N mods you need" videos. The unexpected finding is how fast security became the main counter-narrative: mods are not sandboxed, run with the user's full permissions, and the built-in guard only loads on Team/Enterprise or managed machines, while third-party reports argue install-time disclosure is insufficient.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: High | 📊 Score: 97/100
**Summary**: Better Stack's technical walkthrough of mods as small TypeScript plugins running inside Claude Code, covering behavior changes and custom drawing. A developer-oriented overview rather than a list of downloads (7:37, 37.5k views).
**Score reason**: Exact match on query from a technical channel, published 5 days ago with > 10k views
**Tags**: `claude-code`, `mods`, `typescript`, `overview`

**[2] anthropics/claude-code — `mods/` (source of built-in mods)**
🔗 https://github.com/anthropics/claude-code/tree/main/mods
📅 Undated (public since launch, ~2026-10-01) | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Public source for the mods Anthropic ships inside Claude Code: `diff` (the `/diff` pane), `agents-md`, `sec-default` (the organization guard) and `telemetry`. Each is a complete plugin with hooks module and tests, making this the reference implementation for anyone writing a mod. Link taken from the official docs; repo metadata was not fetched.
**Score reason**: First-party reference implementation on GitHub, exact match on topic
**Tags**: `official`, `reference-implementation`, `sec-default`, `built-in-mods`

**[3] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 94/100
**Summary**: Anthropic's official launch video on the Claude channel. Defines mods as functions you write that change what Claude Code renders, what goes into a prompt, and what happens around tool calls (3:21, 345k views).
**Score reason**: First-party announcement video, 4 days old, highest view count among on-topic videos
**Tags**: `official`, `launch`, `claude-code`, `video`

**[4] karanb192/awesome-claude-code-mods**
🔗 https://github.com/karanb192/awesome-claude-code-mods
📅 Created 2026-09-15, last push 2026-10-09 | ⭐ Authority: High | 📊 Score: 92/100
**Summary**: The largest community catalogue of public mods (417 stars), scanned from GitHub with a per-mod listing of what each can read, write, run or send over the network; browsable at mods.aidojo.si. StationX reports it grew from 359 to 1,740 mods between 2 and 4 October. The same author also maintains `karanb192/claude-code-mods` (builder skill + mods).
**Score reason**: Exact match, pushed today, de facto ecosystem index with capability audit
**Tags**: `catalogue`, `awesome-list`, `capability-scan`, `ecosystem`

**[5] hamzafer/claude-code-mods**
🔗 https://github.com/hamzafer/claude-code-mods
📅 Created 2026-10-02, last push 2026-10-09 | ⭐ Authority: High | 📊 Score: 92/100
**Summary**: A collection of working mods (167 stars): context bar, usage meter, Codex review watch, Markdown preview, Spotify now-playing, guards, panes and games. Useful as a set of concrete TypeScript examples spanning the main UI surfaces.
**Score reason**: Exact match with real implementations, actively pushed today
**Tags**: `examples`, `typescript`, `prompt-band`, `panes`

**[6] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 Created 2026-10-04, last push 2026-10-09 | ⭐ Authority: High | 📊 Score: 92/100
**Summary**: A second index of Claude Code mods, plugins and hooks that describes itself as "evidence-graded", available in 20 languages and rebuilt every 2 hours (31 stars). Complements [4] with a grading angle rather than a raw scan.
**Score reason**: Exact match, automated index pushed today
**Tags**: `catalogue`, `awesome-list`, `multilingual`, `automation`

**[7] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 92/100
**Summary**: Eric Tech explains what mods are and positions them as changing how Claude Code looks and works, "not just what it knows" (9:53, 9.3k views). One of the freshest explainer-style videos in the window.
**Score reason**: Exact match published yesterday, explainer format
**Tags**: `guide`, `customization`, `video`, `explainer`

**[8] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: Medium | 📊 Score: 89/100
**Summary**: Nate Herk's launch-week video presenting five mods (11:19, 216k views). His companion repo `nateherkai/claude-code-mods` contains four of them: Cache Keeper, Recording Mode, Goal Meter and Collision Guard. Promotional framing, but the mods are open source.
**Score reason**: Exact match with strong engagement; authority lowered for lead-magnet framing
**Tags**: `listicle`, `video`, `starter-mods`, `influencer`

**[9] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: Medium | 📊 Score: 89/100
**Summary**: Jay E (RoboNuggets) presents nine mods with a free PDF guide (12:47, 290k views). The most-viewed third-party video on the topic in the window, indicating reach beyond the developer core.
**Score reason**: Exact match published yesterday with 290k views; authority lowered for lead-magnet framing
**Tags**: `listicle`, `video`, `workflow`, `influencer`

**[10] anthropics/claude-code-playground — `claude-code/mods` (sample mods)**
🔗 https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods
📅 Undated (referenced from launch docs, ~2026-10-01) | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Anthropic's sample mods, shared as-is without support: `token-weather` (context forecast band), `blast-radius` (holds risky shell commands with proceed/cancel buttons) and `replay-theater` (`/replay` through the last turn's edits). Each README explains how it was built. Link taken from the official docs; repo metadata was not fetched.
**Score reason**: First-party sample code on GitHub, exact match on topic
**Tags**: `official`, `samples`, `blast-radius`, `token-weather`

**[11] Claude Code Mods: The Complete Guide + 34 Videos (2026)**
🔗 https://app.stationx.net/articles/claude-code-mods
📅 Updated October 2026 (research 3–4 Oct, fact-check 5 Oct) | ⭐ Authority: Medium | 📊 Score: 85/100
**Summary**: A 30-minute long-form guide with the most detailed timeline found: preview behind an opt-in flag in September, launch on 1 October in v2.1.287, then v2.1.288 and v2.1.289 fixes. It rescans the main catalogue (1,740 mods on 4 Oct, of which 537 can see every prompt and 212 reach the network) and summarizes Pluto Security's pre-release findings.
**Score reason**: Deep long-form coverage with original catalogue analysis, less than a week old
**Tags**: `guide`, `timeline`, `security`, `ecosystem-stats`

**[12] Claude Code Mods: What They Are and How to Write One**
🔗 https://www.developersdigest.tech/blog/claude-code-mods-guide-2026
📅 2026-10-06 | ⭐ Authority: Medium | 📊 Score: 85/100
**Summary**: An 8-minute practitioner guide: three-file mod built in about five minutes, `claude --plugin-dir` for one-session loading, and a decision table for mod vs settings hook vs skill vs MCP server. Stresses that settings hooks are not deprecated and recommends `claude plugin validate` and `allowManagedModsOnly`.
**Score reason**: Direct match with hands-on tutorial content, published 3 days ago
**Tags**: `tutorial`, `decision-table`, `hooks-vs-mods`, `security`

---

### 🟠 High value (score 70–84)

**[13] Mods overview — Claude Code Docs**
🔗 https://code.claude.com/docs/en/plugins/mods/overview
📅 Undated (live since launch, ~2026-10-01) | ⭐ Authority: High | 📊 Score: 80/100
**Summary**: The primary reference. Covers the handler model (observe / rewrite / answer), what a mod can reach, where hooks run versus where drawing appears (CLI, Desktop, VS Code, `claude -p`, cloud), built-in mods, kill switches (`--safe-mode`, `disableAllHooks`) and the official comparison with settings hooks, skills and MCP servers.
**Score reason**: Authoritative first-party documentation, exact match with full technical depth
**Tags**: `official`, `documentation`, `architecture`, `trust-model`

**[14] Create a mod — Claude Code Docs**
🔗 https://code.claude.com/docs/en/plugins/mods/create
📅 Undated (live since launch, ~2026-10-01) | ⭐ Authority: High | 📊 Score: 80/100
**Summary**: The official tutorial: build `first-mod`, which counts tool calls, shows the count beside the spinner and adds a `/tally` command. No Node.js, bundler or build step is needed since Claude Code loads `.js` and `.ts` directly; also covers asking Claude to write the mod for you.
**Score reason**: First-party step-by-step tutorial, exact match
**Tags**: `official`, `tutorial`, `first-mod`, `plugin-manifest`

**[15] Claude Code mods deny-rule gap — Pebblous report**
🔗 https://blog.pebblous.ai/report/claude-code-mods-deny-rule-gap/en/
📅 Undated (after 2026-10-01) | ⭐ Authority: Medium | 📊 Score: 80/100
**Summary**: A third-party analysis arguing that permission deny rules can be overridden in some cases, because a mod handling the final verdict on a tool call can replace that verdict. Consistent with the official docs' statement that a mod can sometimes approve a call a `deny` rule refuses. Summary based on the search snippet; the page was not read in full.
**Score reason**: Exact match on a specific security angle, post-launch analysis
**Tags**: `security`, `permissions`, `deny-rules`, `third-party-analysis`

**[16] Claude Mods Make Claude Code 10x More Powerful**
🔗 https://www.youtube.com/watch?v=kxZkkRtwV2A
📅 2026-09-18 | ⭐ Authority: High | 📊 Score: 79/100
**Summary**: Firecrawl's pre-launch video showing DOOM running inside Claude Code's terminal UI through what was then a hidden feature (4:40, 7.3k views). Valuable as early-access evidence of how far the rendering surface goes.
**Score reason**: Exact match and earliest video coverage, penalized for age (21 days) and short length
**Tags**: `early-access`, `demo`, `terminal-ui`, `video`

**[17] Customize Claude Code with mods — Claude blog**
🔗 https://claude.com/blog/claude-code-mods
📅 2026-10-01 | ⭐ Authority: High | 📊 Score: 77/100
**Summary**: The launch announcement. Mods hook into tool calls, permission requests and rendering, can run before, after or instead of them, and built-in features such as `/diff` are now mods that can be disabled or replaced. States the security model plainly: same machine access as Claude Code, not sandboxed, with `sec-default` loading first on Team/Enterprise and managed machines.
**Score reason**: First-party launch post, exact match, 8 days old
**Tags**: `official`, `announcement`, `launch`, `sec-default`

**[18] Claude Code function hooks security — Pluto Security**
🔗 https://pluto.security/blog/claude-code-function-hooks-security/
📅 2026-09-22 (date per StationX, not verified on the page) | ⭐ Authority: Medium | 📊 Score: 77/100
**Summary**: A pre-release security review (build 2.1.274) describing trust gaps: capabilities are not shown at install time, a test mod hooking everything reported zero hooks, and a mod could exfiltrate credentials and prompt history, spoof a credential prompt, or fetch remote code after review. Recommends treating a mod install like running an untrusted binary. StationX notes some findings are now documented as intended access. Summary based on search snippets.
**Score reason**: Original security research cited by later guides, penalized for age (17 days)
**Tags**: `security`, `supply-chain`, `function-hooks`, `research`

**[19] Claude Code Now Has Mods. Here Are 10 Worth Stealing**
🔗 https://www.youtube.com/watch?v=uvIopT_2sY0
📅 2026-10-02 | ⭐ Authority: Medium | 📊 Score: 89/100
**Summary**: Mark Kashef's launch-week video with ten mods and the prompts used to create them (11:19, 53k views). Its companion repo `promptadvisers/claude-mods-starter-kit` adds beginner guides, safe demos and a build-your-own template. Listed in this band because it overlaps heavily with [8] and [9].
**Score reason**: Exact match with open companion repo; authority lowered for lead-magnet framing
**Tags**: `listicle`, `starter-kit`, `video`, `prompts`

**[20] 0xDarkMatter/claude-mods**
🔗 https://github.com/0xDarkMatter/claude-mods
📅 Created 2025-11-27, last push 2026-10-07 | ⭐ Authority: High | 📊 Score: 72/100
**Summary**: A pre-existing toolkit (56 stars) of skills, agents, commands, rules, hooks and output styles for Claude Code that used the "claude-mods" name almost a year before the feature existed. Adjacent rather than on-topic: it does not contain mods in the October 2026 sense, and is a likely source of name confusion in search results.
**Score reason**: Adjacent topic sharing the name, actively maintained GitHub repo
**Tags**: `naming-collision`, `skills`, `settings-hooks`, `toolkit`

---

### 🟡 Worth including (score 60–69)

None retained — the target of 20 sources was reached above this band.

---

## Trends identified

- **Hidden feature to default-on in under a month**: sources agree on a September early-access phase under the name "function hooks" (opt-in flag `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`) followed by a default-on launch on 1 October. They disagree on the exact September dates (3 Sep, 9 Sep and 14 Sep are all cited), so the preview timeline should be treated as approximate.
- **The ecosystem is dominated by one UI surface**: most community repos converge on a band above the prompt showing context, usage limits, cost or cache countdown. Guards on tool calls and full panes are a clear second tier; anything else (games, stock tickers, Mermaid rendering) is novelty.
- **Security is the main counter-narrative, and it predates the launch**: official docs, the launch post, Pluto, Pebblous and StationX all centre on the same facts — no sandbox, user-level permissions, the ability to approve tool calls, and `sec-default` limited to Team/Enterprise or managed machines. The community answer is capability-scanning catalogues and `claude plugin validate`, not isolation.
- **Mods are written by Claude, not by hand**: the official docs, the built-in `plugin-authoring` skill and nearly every video present "describe it and Claude writes the mod" as the default path, which explains the catalogue growing from 359 to 1,740 entries in two days and raises the review burden.
- **Coverage is video- and repo-led, with no research yet**: arXiv returned nothing, the Substack/dev.to/Hashnode search returned nothing on those domains, and the highest-reach content is launch-week "N mods you need" videos tied to lead magnets. Mods are positioned as complementary to settings hooks, skills and MCP servers rather than as a replacement.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
